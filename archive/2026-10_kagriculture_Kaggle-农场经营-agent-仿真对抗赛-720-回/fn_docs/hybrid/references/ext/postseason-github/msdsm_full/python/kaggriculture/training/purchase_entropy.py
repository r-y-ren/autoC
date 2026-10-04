"""Quantity-marginalized purchase-item exploration, separate from buying frequency."""

from __future__ import annotations

import math
from typing import Any

import jax
import jax.numpy as jnp

from kaggriculture.actions.catalog import MARKET_ACTIONS

PURCHASE_ENTROPY_DEFAULTS = {
    "purchase_entropy_coefficient": 0.0,
    "purchase_entropy_steps": 48,
    "purchase_entropy_metrics": False,
}
PURCHASE_OPS = frozenset(("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"))
PURCHASE_ITEMS = tuple(dict.fromkeys(action[:2] for action in MARKET_ACTIONS if action[0] in PURCHASE_OPS))
PURCHASE_IDS = tuple(index for index, action in enumerate(MARKET_ACTIONS) if action[0] in PURCHASE_OPS)
PURCHASE_START, PURCHASE_END = PURCHASE_IDS[0], PURCHASE_IDS[-1] + 1
QUANTITY_COUNT = 100
ITEM_COUNT = len(PURCHASE_ITEMS)
TOMATO_ITEM_INDEX = PURCHASE_ITEMS.index(("BUY_SEED", "TOMATO"))
TOMATO_FLOOR_EPSILON = 1e-8
if PURCHASE_IDS != tuple(range(PURCHASE_START, PURCHASE_END)) or tuple(
    MARKET_ACTIONS[index] for index in PURCHASE_IDS
) != tuple((*item, quantity) for item in PURCHASE_ITEMS for quantity in range(1, QUANTITY_COUNT + 1)):
    raise RuntimeError("purchase entropy requires the frozen contiguous item/quantity catalog")


def validate_purchase_entropy(coefficient: float, steps: int) -> None:
    if not math.isfinite(coefficient) or coefficient < 0 or not 0 <= steps <= 719:
        raise ValueError("invalid purchase entropy coefficient or interval")


def purchase_item_statistics(logits: jax.Array) -> dict[str, jax.Array]:
    values = logits.astype(jnp.float32)
    grouped = values[..., PURCHASE_START:PURCHASE_END].reshape((*values.shape[:-1], ITEM_COUNT, QUANTITY_COUNT))
    item_logits = jax.nn.logsumexp(grouped, axis=-1)
    item_log_probability = jax.nn.log_softmax(item_logits, axis=-1)
    item_probability = jnp.exp(item_log_probability)
    entropy = -jnp.sum(item_probability * item_log_probability, axis=-1)
    buy_probability = jnp.minimum(
        jnp.exp(jax.nn.logsumexp(item_logits, axis=-1) - jax.nn.logsumexp(values, axis=-1)), 1.0
    )
    entropy = jnp.where(buy_probability > 0, entropy, 0.0)
    # This coefficient must not reward increasing purchase frequency merely to earn more entropy.
    weighted = jax.lax.stop_gradient(buy_probability) * entropy
    return {
        "purchase_item_entropy": entropy.mean(axis=-1),
        "purchase_item_normalized_entropy": entropy.mean(axis=-1) / math.log(ITEM_COUNT),
        "purchase_weighted_item_entropy": weighted.mean(axis=-1),
        "purchase_probability": buy_probability.mean(axis=-1),
        **{
            f"purchase_probability_{op.lower()}_{item.lower()}": (buy_probability * item_probability[..., index]).mean(
                axis=-1
            )
            for index, (op, item) in enumerate(PURCHASE_ITEMS)
        },
    }


def purchase_entropy_terms(
    logits: jax.Array, episode_step: jax.Array, coefficient: float, steps: int
) -> tuple[jax.Array, dict[str, jax.Array]]:
    metrics = purchase_item_statistics(logits)
    weight = jnp.where((episode_step >= 0) & (episode_step < steps), coefficient, 0.0).astype(jnp.float32)
    # Existing Market entropy sums slots; keep the added cost on that same scale.
    loss = -weight * logits.shape[-2] * metrics["purchase_weighted_item_entropy"]
    return loss, {**metrics, "purchase_item_entropy_loss": loss, "purchase_item_entropy_coefficient": weight}


def tomato_floor_terms(logits: jax.Array, coefficient: float, target: float) -> tuple[jax.Array, dict[str, jax.Array]]:
    """Apply the requested log-ratio hinge per slot, averaged over market slots."""
    grouped = logits.astype(jnp.float32)[..., PURCHASE_START:PURCHASE_END].reshape(
        (*logits.shape[:-1], ITEM_COUNT, QUANTITY_COUNT)
    )
    item_logits = jax.nn.logsumexp(grouped, axis=-1)
    log_q = jax.nn.log_softmax(item_logits, axis=-1)[..., TOMATO_ITEM_INDEX]
    # Evaluate log(q + epsilon) in log space to avoid underflow for rare items.
    gap = math.log(target) - jnp.logaddexp(log_q, math.log(TOMATO_FLOOR_EPSILON))
    per_slot = coefficient * jax.nn.relu(gap)
    loss = per_slot.mean(axis=-1)
    return loss, {
        "tomato_floor_loss": loss,
        "tomato_floor_active_fraction": (gap > 0).astype(jnp.float32).mean(axis=-1),
        "tomato_conditional_probability_slot_mean": jnp.exp(log_q).mean(axis=-1),
        "tomato_floor_target": jnp.full_like(loss, target),
        "tomato_floor_coefficient": jnp.full_like(loss, coefficient),
    }


def add_purchase_report(metrics: dict[str, Any]) -> dict[str, Any]:
    if "purchase_probability" not in metrics:
        return metrics
    result = {**metrics}
    buy_probability = result["purchase_probability"]
    conditional = result["purchase_weighted_item_entropy"] / buy_probability if buy_probability > 0 else None
    result["purchase_conditioned_item_entropy"] = conditional
    result["purchase_conditioned_item_normalized_entropy"] = (
        conditional / math.log(ITEM_COUNT) if conditional is not None else None
    )
    distribution = {}
    for op, item in PURCHASE_ITEMS:
        name = f"purchase_probability_{op.lower()}_{item.lower()}"
        mass = result.pop(name)
        distribution[f"{op}:{item}"] = mass / buy_probability if buy_probability > 0 else None
    result["purchase_item_distribution"] = distribution
    return result
