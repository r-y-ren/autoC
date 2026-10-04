"""Liquidate market-sellable stock on the last actionable turn."""

from __future__ import annotations

from typing import Any

import numpy as np

from kaggriculture.actions.quantities import SHED_ACCESS, shed_after_unit_actions
from kaggriculture.actions.catalog import (
    EPISODE_STEPS,
    MARKET_ACTION_TO_ID,
    MARKET_SLOTS,
    PRODUCTS,
    SHED_CAPACITY,
    UNIT_ACTION_TO_ID,
)
from kaggriculture.actions.sell_quantity import ABSOLUTE_START, QUANTITY_COUNT


def final_turn_action(observation: dict[str, Any]) -> dict[str, Any] | None:
    if int(observation.get("step", -1)) != EPISODE_STEPS - 2:
        return None

    player = int(observation.get("player", -1))
    farms = observation.get("farms", [])
    if not 0 <= player < len(farms):
        return None

    farm = farms[player]
    positions = [farm.get("farmer", [-1, -1]), *farm.get("hands", [])]
    private = observation.get("private", {})
    inventories = private.get("inventories", [])
    room = max(0, SHED_CAPACITY - sum(max(0, int(n)) for n in private.get("shed", {}).values()))
    unit_actions = []
    for index, position in enumerate(positions):
        inventory = inventories[index] if index < len(inventories) else {}
        if tuple(position) not in SHED_ACCESS:
            unit_actions.append(["PASS"])
            continue
        remaining = room
        product_transfer = 0
        for item, count in inventory.items():
            transferred = min(max(0, int(count)), remaining)
            if item in PRODUCTS:
                product_transfer += transferred
            remaining -= transferred
        unit_actions.append(["DROP"] if product_transfer else ["PASS"])
        if product_transfer:
            room = remaining

    sellable = shed_after_unit_actions(observation, unit_actions)
    market = [["SELL", item, int(sellable[item])] for item in PRODUCTS if int(sellable.get(item, 0)) > 0]
    return {"farmer": unit_actions[0], "hands": unit_actions[1:], "market": market[:MARKET_SLOTS]}


def final_turn_ids(
    observation: dict[str, Any], unit_slots: int, *, absolute_sell: bool
) -> tuple[np.ndarray, np.ndarray]:
    action = final_turn_action(observation)
    if action is None:
        raise ValueError("final-turn encoding requires the last actionable observation")
    unit_ids = np.full(unit_slots, UNIT_ACTION_TO_ID[("PASS",)], dtype=np.int32)
    for index, order in enumerate([action["farmer"], *action["hands"]][:unit_slots]):
        unit_ids[index] = UNIT_ACTION_TO_ID[tuple(order)]
    market_ids = np.zeros(MARKET_SLOTS, dtype=np.int32)
    for slot, (_, item, quantity) in enumerate(action["market"]):
        if absolute_sell:
            if not 1 <= quantity <= QUANTITY_COUNT:
                raise ValueError("final-turn SELL quantity exceeds absolute head support")
            market_ids[slot] = ABSOLUTE_START + PRODUCTS.index(item) * QUANTITY_COUNT + quantity - 1
        else:
            market_ids[slot] = MARKET_ACTION_TO_ID[("SELL", item, "MAX")]
    return unit_ids, market_ids
