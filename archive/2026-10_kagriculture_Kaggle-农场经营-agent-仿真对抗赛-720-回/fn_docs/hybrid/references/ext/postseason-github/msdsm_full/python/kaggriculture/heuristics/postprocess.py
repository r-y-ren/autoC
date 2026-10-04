"""Confidence-ordered action repair and storage rules used by Final A."""

from __future__ import annotations

import traceback
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from . import shed_patch, unit_rules
from .handoff import SearchHandoff

DEFAULTS = {
    "shed_night": True,
    "shed_final": True,
    "fertilize_mask": True,
    "same_tile": True,
    "seed_stock": True,
    "care_mask": True,
    "offboard_mask": True,
    "search_from_day": 29,
}


class Runtime:
    """Explicit neural helpers consumed by the original action-repair implementation."""

    def __init__(self, policy: Any) -> None:
        from kaggriculture.agents.neural import prepare_fixed_batch, decode_market_order
        from kaggriculture.observations.features import encode_observation
        from kaggriculture.actions.quantities import shed_after_unit_actions
        from kaggriculture.actions.catalog import UNIT_ACTIONS

        self.prepare_fixed_batch = prepare_fixed_batch
        self.decode_market_order = decode_market_order
        self.encode_observation = encode_observation
        self.shed_after_unit_actions = shed_after_unit_actions
        self.UNIT_ACTIONS = UNIT_ACTIONS
        self._final_turn = getattr(policy, "final_turn_action", None)

    def final_turn_action(self, observation: dict) -> dict | None:
        return self._final_turn(observation) if self._final_turn else None


class HeuristicController:
    """Keep failure and search state local to one agent / game."""

    def __init__(self, policy: Any, settings: dict | None = None) -> None:
        settings = settings or {}
        if unknown := settings.keys() - DEFAULTS.keys():
            raise ValueError(f"unknown heuristic settings: {sorted(unknown)}")
        self.settings = {**DEFAULTS, **settings}
        self.policy = policy
        self.runtime = Runtime(policy)
        self.failed = False
        search_root = Path(__file__).resolve().parents[1] / "search"
        self.handoff = SearchHandoff(search_root, self.settings["search_from_day"])

    def policy_turn(self, observation: dict) -> dict:
        if self.failed:
            return self.policy(observation)
        try:
            rules = frozenset(rule for rule in unit_rules.RULES if self.settings[rule])
            action = (
                unit_rules.decide(self.policy, observation, self.runtime, rules) if rules else self.policy(observation)
            )
            action = shed_patch.patch_action(
                observation,
                action,
                night=self.settings["shed_night"],
                final=self.settings["shed_final"],
            )
        except Exception:
            self.failed = True
            traceback.print_exc(file=sys.stderr)
            return self.policy(observation)
        self.policy.previous_action = deepcopy(action)
        return action

    def __call__(self, observation: dict) -> dict:
        return self.handoff(observation, lambda: self.policy_turn(observation))
