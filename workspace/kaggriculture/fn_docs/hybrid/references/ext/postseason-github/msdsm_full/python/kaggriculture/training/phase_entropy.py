"""Opening-only entropy weights and additive, padding-safe phase diagnostics."""

from __future__ import annotations

import math
from typing import Any

import jax
import jax.numpy as jnp

from kaggriculture.training.purchase_entropy import add_purchase_report

OPENING_ENTROPY_DEFAULTS = {"opening_entropy_steps": 48, "opening_entropy_multiplier": 1.0}
PHASES = (("opening", 0, 48), ("early", 48, 240), ("middle", 240, 480), ("late", 480, 719))
PHASE_PREFIX = "phase_entropy/"


def validate_opening_entropy(steps: int, multiplier: float) -> None:
    if not 0 <= steps <= 719 or not math.isfinite(multiplier) or multiplier < 0:
        raise ValueError("invalid opening entropy interval or multiplier")


def entropy_weights(episode_step: jax.Array, steps: int, multiplier: float) -> jax.Array:
    return jnp.where((episode_step >= 0) & (episode_step < steps), multiplier, 1.0).astype(jnp.float32)


def phase_sums(
    episode_step: jax.Array,
    sample_mask: jax.Array,
    unit_entropy: jax.Array,
    market_entropy: jax.Array,
    unit_normalized: jax.Array,
    market_normalized: jax.Array,
    unit_coefficient: jax.Array,
    market_coefficient: jax.Array,
    weights: jax.Array,
    extra_values: dict[str, jax.Array] | None = None,
) -> dict[str, jax.Array]:
    values = {
        "count": jnp.ones_like(unit_entropy),
        "unit_entropy": unit_entropy,
        "market_entropy": market_entropy,
        "unit_normalized_entropy": unit_normalized,
        "market_normalized_entropy": market_normalized,
        "unit_entropy_cost": -unit_coefficient * weights * unit_entropy,
        "market_entropy_cost": -market_coefficient * weights * market_entropy,
        "unit_coefficient": jnp.broadcast_to(unit_coefficient, weights.shape) * weights,
        "market_coefficient": jnp.broadcast_to(market_coefficient, weights.shape) * weights,
        **({} if extra_values is None else extra_values),
    }
    result = {}
    for phase, start, end in PHASES:
        mask = ((episode_step >= start) & (episode_step < end)).astype(jnp.float32) * sample_mask
        for name, value in values.items():
            result[f"{PHASE_PREFIX}{phase}/{name}"] = jnp.sum(value * mask)
    return result


def phase_report(totals: dict[str, float]) -> dict[str, Any]:
    report = {}
    for name, start, end in PHASES:
        prefix = f"{PHASE_PREFIX}{name}/"
        count = totals.get(prefix + "count", 0.0)
        if count == 0:
            continue
        report[name] = add_purchase_report(
            {
                "step_start": start,
                "step_end_inclusive": end - 1,
                "sample_count": round(count),
                **{
                    key.removeprefix(prefix): value / count
                    for key, value in totals.items()
                    if key.startswith(prefix) and key != prefix + "count"
                },
            }
        )
    return report
