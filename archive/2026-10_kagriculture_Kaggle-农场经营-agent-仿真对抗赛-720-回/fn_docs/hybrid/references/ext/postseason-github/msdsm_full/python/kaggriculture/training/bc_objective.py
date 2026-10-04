"""Replay CE with full-distribution entropy and a frozen initialization teacher."""

import math

import jax
import jax.numpy as jnp
import optax

from kaggriculture.model.policy import JaxModelConfig, own_unit_mask_from_features, policy_forward
from kaggriculture.training.objectives import categorical_entropy, categorical_teacher_kl


def head_metrics(
    logits: jax.Array, labels: jax.Array, active: jax.Array, teacher: jax.Array | None, axis_name: str | None = None
) -> dict:
    logits = logits.astype(jnp.float32)
    labelled = active & (labels >= 0)

    def denominator(mask: jax.Array) -> jax.Array:
        if axis_name is None:
            return jnp.maximum(mask.sum(), 1)
        # Subsequent pmean of gradients/metrics then equals the global slot-weighted mean.
        return jnp.maximum(jax.lax.psum(mask.sum(), axis_name), 1) / jax.lax.psum(1, axis_name)

    count = denominator(labelled)
    active_count = denominator(active)
    logs = jax.nn.log_softmax(logits)
    ce = -jnp.take_along_axis(logs, jnp.maximum(labels, 0)[..., None], -1)[..., 0]
    entropy = (categorical_entropy(logits) * active).sum() / active_count
    kl = (
        jnp.asarray(0.0) if teacher is None else (categorical_teacher_kl(logits, teacher) * active).sum() / active_count
    )
    return {
        "ce": (ce * labelled).sum() / count,
        "entropy": entropy,
        "normalized_entropy": entropy / math.log(logits.shape[-1]),
        "teacher_kl": kl,
        "accuracy": ((jnp.argmax(logits, -1) == labels) * labelled).sum() / count,
        "labels": labelled.sum(),
        "active_slots": active.sum(),
    }


def make_steps(
    model: JaxModelConfig,
    dtype: jnp.dtype,
    optimizer: optax.GradientTransformation,
    unit_entropy: float,
    market_entropy: float,
    teacher_kl: float,
):
    def loss(student: dict, teacher: dict, batch: dict):
        outputs = policy_forward(student, batch, model, dtype=dtype)
        reference = None
        if teacher_kl:
            reference = jax.lax.stop_gradient(policy_forward(teacher, batch, model, dtype=dtype))
        valid = batch["sample_mask"][:, None] > 0
        unit = head_metrics(
            outputs["unit_action"],
            batch["unit_action"],
            own_unit_mask_from_features(batch["features"]) & valid,
            None if reference is None else reference["unit_action"],
            "data",
        )
        market = head_metrics(
            outputs["market_action"],
            batch["market_action"],
            jnp.broadcast_to(valid, batch["market_action"].shape),
            None if reference is None else reference["market_action"],
            "data",
        )
        terms = {
            "bc_loss": unit["ce"] + market["ce"],
            "unit_entropy_loss": -unit_entropy * unit["entropy"],
            "market_entropy_loss": -market_entropy * market["entropy"],
            "teacher_kl_loss": teacher_kl * (unit["teacher_kl"] + market["teacher_kl"]),
        }
        total = sum(terms.values())
        return total, {
            **terms,
            "loss": total,
            "sample_count": batch["sample_mask"].sum(),
            **{f"unit_{k}": v for k, v in unit.items()},
            **{f"market_{k}": v for k, v in market.items()},
        }

    value_and_grad = jax.value_and_grad(loss, has_aux=True)

    def train(student: dict, state: tuple, teacher: dict, batch: dict, emit: bool):
        del emit
        (_, metrics), gradients = value_and_grad(student, teacher, batch)
        gradients = jax.lax.pmean(gradients, "data")
        metrics = jax.lax.pmean(metrics, "data")
        metrics["gradient_norm"] = optax.global_norm(gradients)
        updates, state = optimizer.update(gradients, state, student)
        return optax.apply_updates(student, updates), state, metrics

    def validate(student: dict, teacher: dict, batch: dict, emit: bool):
        del emit
        return jax.lax.pmean(loss(student, teacher, batch)[1], "data")

    return train, validate
