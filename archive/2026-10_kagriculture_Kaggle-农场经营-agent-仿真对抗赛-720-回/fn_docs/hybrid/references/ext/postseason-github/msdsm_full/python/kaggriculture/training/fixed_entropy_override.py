"""Explicit, state-preserving changes to the fixed PPO entropy coefficient."""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Any

from kaggriculture.training.checkpointing import LoopState, policy_hash

FIXED_ENTROPY_FIELDS = frozenset(("entropy_coefficient", "entropy_coefficient_max"))


def validate_fixed_entropy_override(saved: dict[str, Any], current: dict[str, Any]) -> None:
    for config in (saved, current):
        if any(
            config.get(name) is not None for name in ("entropy_floor", "unit_entropy_target", "market_entropy_target")
        ):
            raise ValueError("fixed entropy override cannot change an adaptive controller")
    coefficient = current["entropy_coefficient"]
    maximum = current["entropy_coefficient_max"]
    if not math.isfinite(coefficient) or coefficient < 0 or not math.isfinite(maximum) or maximum < coefficient:
        raise ValueError("fixed entropy coefficient must be finite, non-negative and within its maximum")


def change_fixed_entropy(state: LoopState, coefficient: float) -> tuple[LoopState, dict[str, Any] | None]:
    if not math.isfinite(coefficient) or coefficient < 0:
        raise ValueError("fixed entropy coefficient must be finite and non-negative")
    if state.entropy_control is not None:
        raise ValueError("fixed entropy override cannot change an adaptive controller")
    if state.entropy_coefficient == coefficient:
        return state, None
    event = {
        "event": "fixed_entropy_coefficient_changed",
        "completed_updates": state.completed_updates,
        "previous_coefficient": state.entropy_coefficient,
        "unit_entropy_coefficient": coefficient,
        "market_entropy_coefficient": coefficient,
        "policy_sha256": policy_hash(state.params),
        "reference_sha256": policy_hash(state.reference_params),
        "optimizer_sha256": policy_hash(state.optimizer_state),
        "rng_sha256": policy_hash(state.rng),
        "seed_counter": state.seed_counter,
    }
    return replace(state, entropy_coefficient=coefficient), event
