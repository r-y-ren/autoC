"""Preload the search controller, then hand over at final-day dawn."""

from __future__ import annotations

import ctypes
import importlib.util
import sys
import traceback
from collections.abc import Callable
from pathlib import Path

MIN_START_OVERAGE = 10.0
KAGGLE_OVERAGE = 60.0


class SearchHandoff:
    def __init__(self, directory: Path, start_day: int | None = 29) -> None:
        self.directory = directory
        self.start_day = start_day
        self.module = None
        self.library = None
        self.started = False
        self.failed = False

    def load(self):
        if self.module is None:
            path = self.directory / "main.py"
            spec = importlib.util.spec_from_file_location("_kaggriculture_endgame", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module._load_search_policy(None)
            self.library = ctypes.CDLL(str(self.directory / "terminal_search.so"))
            self.module = module
        return self.module

    def __call__(self, observation: dict, policy_turn: Callable[[], dict]) -> dict:
        if self.start_day is None or self.failed:
            return policy_turn()
        day = int(observation.get("day", 0))
        overage = float(observation.get("remainingOverageTime", KAGGLE_OVERAGE))
        if day < self.start_day:
            action = policy_turn()
            if day == self.start_day - 1 and self.module is None:
                if overage < MIN_START_OVERAGE:
                    self.failed = True
                    return action
                try:
                    self.load()
                except Exception:
                    self.failed = True
                    traceback.print_exc(file=sys.stderr)
            return action
        if not self.started and overage < MIN_START_OVERAGE:
            self.failed = True
            return policy_turn()
        if "step" not in observation:
            observation = {**observation, "step": day * 24 + int(observation.get("hour", 0))}
        try:
            action = self.load().agent(observation, None)
        except Exception:
            self.failed = True
            traceback.print_exc(file=sys.stderr)
            return policy_turn()
        self.started = True
        return action
