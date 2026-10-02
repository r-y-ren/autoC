"""On-policy opening purchase temperature, preserving quantity and total buy mass."""

from __future__ import annotations

import math
from typing import Any

import jax
import jax.numpy as jnp

from kaggriculture.training.purchase_entropy import (
    ITEM_COUNT,
    PURCHASE_END,
    PURCHASE_START,
    QUANTITY_COUNT,
    add_purchase_report,
    purchase_item_statistics,
)

PURCHASE_POLICY_PREFIX = "opening_purchase/"

PURCHASE_TEMPERATURE_DEFAULTS = {
    "purchase_temperature_initial": 1.0,
    "purchase_temperature_steps": 5,
    "purchase_temperature_decay_updates": 100,
    "purchase_temperature_start_update": 0,
    "purchase_temperature_schedule": "exponential",
}


def validate_purchase_temperature(
    initial: float, steps: int, decay_updates: int, start_update: int, schedule: str = "exponential"
) -> None:
    if not math.isfinite(initial) or initial < 1 or not 0 <= steps <= 719:
        raise ValueError("purchase temperature must be finite and >= 1, with steps in [0, 719]")
    if decay_updates <= 0 or start_update < 0:
        raise ValueError("temperature decay must be positive and its starting update nonnegative")
    if schedule not in ("exponential", "linear"):
        raise ValueError("unknown purchase temperature schedule")


def purchase_temperature(
    completed_updates: int, initial: float, decay_updates: int, start_update: int, schedule: str = "exponential"
) -> float:
    progress = min(max((completed_updates - start_update) / decay_updates, 0.0), 1.0)
    if schedule == "linear":
        return 1.0 + (initial - 1.0) * (1.0 - progress)
    if schedule != "exponential":
        raise ValueError("unknown purchase temperature schedule")
    return initial ** (1.0 - progress)


def temper_purchase_logits(logits: jax.Array, temperature: jax.Array) -> jax.Array:
    """Temperature is one effective value per observation (1 outside the opening)."""
    values = logits.astype(jnp.float32)

    def temper(_: None) -> jax.Array:
        grouped = values[..., PURCHASE_START:PURCHASE_END].reshape((*values.shape[:-1], ITEM_COUNT, QUANTITY_COUNT))
        item_logits = jax.nn.logsumexp(grouped, axis=-1)
        log_items = jax.nn.log_softmax(item_logits, axis=-1)
        heated_items = jax.nn.log_softmax(item_logits / temperature[:, None, None], axis=-1)
        correction = jnp.where(temperature[:, None, None] == 1, 0.0, heated_items - log_items)
        heated = (grouped + correction[..., None]).reshape((*values.shape[:-1], ITEM_COUNT * QUANTITY_COUNT))
        return jnp.concatenate((values[..., :PURCHASE_START], heated, values[..., PURCHASE_END:]), axis=-1)

    # Most reverse-time minibatches and post-opening inference need no item reductions.
    return jax.lax.cond(jnp.any(temperature != 1), temper, lambda _: values, None)


def behavior_outputs(outputs: dict[str, jax.Array], batch: dict[str, jax.Array]) -> dict[str, jax.Array]:
    if "purchase_temperature" not in batch:
        return outputs
    return {
        **outputs,
        "market_action": temper_purchase_logits(outputs["market_action"], batch["purchase_temperature"]),
    }


def opening_purchase_sums(
    raw_logits: jax.Array, heated_logits: jax.Array, batch: dict[str, jax.Array]
) -> dict[str, jax.Array]:
    mask = batch["sample_mask"].astype(jnp.float32) * (
        (batch["episode_step"] >= 0) & (batch["episode_step"] < batch["purchase_temperature_steps"])
    )
    result = {PURCHASE_POLICY_PREFIX + "count": mask.sum()}
    for label, logits in (("base", raw_logits), ("behavior", heated_logits)):
        stats = jax.lax.cond(
            jnp.any(mask != 0),
            purchase_item_statistics,
            lambda values: jax.tree.map(
                lambda spec: jnp.zeros(spec.shape, spec.dtype), jax.eval_shape(purchase_item_statistics, values)
            ),
            logits,
        )
        result.update(
            {f"{PURCHASE_POLICY_PREFIX}{label}/{name}": jnp.sum(value * mask) for name, value in stats.items()}
        )
    return result


def opening_purchase_report(totals: dict[str, float]) -> dict[str, Any]:
    count = totals.get(PURCHASE_POLICY_PREFIX + "count", 0.0)
    if not count:
        return {}
    return {
        "sample_count": round(count),
        **{
            label: add_purchase_report(
                {
                    key.removeprefix(f"{PURCHASE_POLICY_PREFIX}{label}/"): value / count
                    for key, value in totals.items()
                    if key.startswith(f"{PURCHASE_POLICY_PREFIX}{label}/")
                }
            )
            for label in ("base", "behavior")
        },
    }
