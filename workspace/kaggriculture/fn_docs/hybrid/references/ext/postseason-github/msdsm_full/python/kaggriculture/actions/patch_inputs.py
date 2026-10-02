"""Observation twin of Rust patch inputs for submission and reference tests."""

from __future__ import annotations

from typing import Any

import numpy as np

from kaggriculture.heuristics.unit_rules import care_gains, fertilize_gains
from kaggriculture.actions.masks import MASK_STEM_SIZE, MAX_UNITS, UNIT_STEM_SIZE, UNIT_STEMS
from kaggriculture.actions.sequential import CROPS, PATCH_CONTEXT_SIZE


def observation_patch_inputs(observation: dict[str, Any]) -> dict[str, np.ndarray]:
    farm = observation["farms"][int(observation["player"])]
    private = observation["private"]
    positions = [farm["farmer"], *farm["hands"]][:MAX_UNITS]
    day = int(observation.get("day", int(observation.get("step", 0)) // 24))
    masks = np.ones((1, MASK_STEM_SIZE), dtype=np.bool_)
    units = masks[0, :UNIT_STEM_SIZE].reshape(MAX_UNITS, len(UNIT_STEMS))
    context = np.zeros((1, PATCH_CONTEXT_SIZE), dtype=np.int32)
    context[0, :MAX_UNITS] = -1
    size = len(farm["tiles"])
    for index, (x, y) in enumerate(positions):
        tile = farm["tiles"][y][x]
        context[0, index] = y * size + x
        if isinstance(tile, dict) and "animal" not in tile:
            context[0, MAX_UNITS + index] = {"COOP": 1, "PASTURE": 2}.get(tile.get("kind"), 0)
        for action, (dx, dy) in enumerate(((0, -1), (0, 1), (1, 0), (-1, 0))):
            units[index, action] = 0 <= x + dx < size and 0 <= y + dy < size
        inventories = private.get("inventories", [])
        held = inventories[index].get("FERTILIZER", 0) if index < len(inventories) else 0
        units[index, UNIT_STEMS.index(("FERTILIZE",))] = held > 0 and fertilize_gains(tile, day)
        units[index, UNIT_STEMS.index(("CARE",))] = care_gains(tile, day)
    context[0, -5:] = [max(0, private.get("seeds", {}).get(crop, 0)) for crop in CROPS]
    return {"legal_mask_stems": masks, "patch_context": context}
