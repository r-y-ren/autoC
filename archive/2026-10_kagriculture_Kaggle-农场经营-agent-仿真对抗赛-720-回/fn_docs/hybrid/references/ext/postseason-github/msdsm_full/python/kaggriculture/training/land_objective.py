"""Optional differentiable exploration terms for the fourth land purchase."""

from __future__ import annotations

import math

import jax
import jax.numpy as jnp

from kaggriculture.training.land_metrics import land_order_probability

DAY_COUNT = 30


def land4_objective_terms(
    logits: jax.Array,
    episode_step: jax.Array,
    owned_count: jax.Array,
    affordable: jax.Array,
    sample_mask: jax.Array,
    probability_bonus_coefficient: jax.Array,
    day_entropy_coefficient: jax.Array,
    *,
    absolute: bool,
) -> tuple[jax.Array, dict[str, jax.Array]]:
    """Reward fourth-land probability and diversity of its expected order day.

    Positive coefficients lower the minimized loss. Eligibility uses pre-resolver raw
    money, so a same-turn SELL-financed purchase is intentionally not counted.
    """
    zero = jnp.asarray(0.0, dtype=jnp.float32)

    def disabled(_: None) -> tuple[jax.Array, dict[str, jax.Array]]:
        return zero, {
            "land4_probability_bonus_loss": zero,
            "land4_day_entropy_loss": zero,
            "land4_eligible_count": zero,
            "land4_order_probability": zero,
            "land4_expected_order_day_normalized_entropy": zero,
            "land4_probability_bonus_coefficient": probability_bonus_coefficient,
            "land4_day_entropy_coefficient": day_entropy_coefficient,
        }

    def enabled(_: None) -> tuple[jax.Array, dict[str, jax.Array]]:
        log_probs = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
        order_probability = land_order_probability(log_probs, absolute=absolute)
        eligible = (
            sample_mask.astype(jnp.float32) * (owned_count == 3).astype(jnp.float32) * affordable.astype(jnp.float32)
        )
        eligible_count = jnp.sum(eligible)
        mean_probability = jnp.sum(eligible * order_probability) / jnp.maximum(eligible_count, 1.0)
        probability_loss = -probability_bonus_coefficient * mean_probability

        day = jnp.clip(episode_step // 24, 0, DAY_COUNT - 1)
        day_mass = jnp.sum(
            jax.nn.one_hot(day, DAY_COUNT, dtype=jnp.float32) * (eligible * order_probability)[:, None],
            axis=0,
        )
        total_mass = jnp.sum(day_mass)
        day_distribution = day_mass / jnp.maximum(total_mass, jnp.finfo(jnp.float32).tiny)
        safe_distribution = jnp.maximum(day_distribution, jnp.finfo(jnp.float32).eps)
        normalized_entropy = -jnp.sum(day_distribution * jnp.log(safe_distribution)) / math.log(DAY_COUNT)
        normalized_entropy = jnp.where(total_mass > 0, normalized_entropy, zero)
        day_entropy_loss = -day_entropy_coefficient * normalized_entropy
        return probability_loss + day_entropy_loss, {
            "land4_probability_bonus_loss": probability_loss,
            "land4_day_entropy_loss": day_entropy_loss,
            "land4_eligible_count": eligible_count,
            "land4_order_probability": mean_probability,
            "land4_expected_order_day_normalized_entropy": normalized_entropy,
            "land4_probability_bonus_coefficient": probability_bonus_coefficient,
            "land4_day_entropy_coefficient": day_entropy_coefficient,
        }

    active = (probability_bonus_coefficient != 0) | (day_entropy_coefficient != 0)
    return jax.lax.cond(active, enabled, disabled, None)
