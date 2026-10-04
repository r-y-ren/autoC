"""The two final inference variants, sharing the same neural implementation."""

from __future__ import annotations

from pathlib import Path


class FinalAgent:
    def __init__(self, model: Path, variant: str, *, heuristic_settings: dict | None = None, warm: bool = True):
        from .neural import load_policy

        if variant not in {"A", "B"}:
            raise ValueError("variant must be A or B")
        self.policy = load_policy(model, warm=warm)
        if self.policy.config.sequential_patch != (variant == "B"):
            raise ValueError("model sequential_patch setting does not match the selected agent variant")
        self.variant = variant
        self.settings = heuristic_settings
        self.controller = None
        self.last_step = -1
        self.last_player = None

    def __call__(self, observation: dict, configuration=None) -> dict:
        step = int(observation.get("step", 24 * observation.get("day", 0) + observation.get("hour", 0)))
        player = int(observation["player"])
        if self.variant == "A":
            if (
                self.controller is None
                or step < self.last_step
                or (step == 0 and self.last_step >= 0)
                or player != self.last_player
            ):
                from kaggriculture.heuristics.postprocess import HeuristicController

                self.controller = HeuristicController(self.policy, self.settings)
            action = self.controller(observation)
        else:
            action = self.policy(observation)
        self.last_step, self.last_player = step, player
        return action
