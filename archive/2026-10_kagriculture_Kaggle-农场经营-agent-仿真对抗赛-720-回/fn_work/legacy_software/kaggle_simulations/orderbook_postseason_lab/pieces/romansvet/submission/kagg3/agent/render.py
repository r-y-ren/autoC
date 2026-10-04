"""Render planner op arrays into kaggle_environments action dicts."""

from __future__ import annotations

from .. import spec
from ..core import ops as O

_UNIT_SIMPLE = {
    O.OP_PASS: "PASS", O.OP_NORTH: "NORTH", O.OP_SOUTH: "SOUTH",
    O.OP_EAST: "EAST", O.OP_WEST: "WEST", O.OP_WATER: "WATER",
    O.OP_HARVEST: "HARVEST", O.OP_FERTILIZE: "FERTILIZE", O.OP_DIG: "DIG",
    O.OP_BUILD_COOP: "BUILD_COOP", O.OP_BUILD_PASTURE: "BUILD_PASTURE",
    O.OP_FEED: "FEED", O.OP_COLLECT_FERT: "COLLECT_FERTILIZER",
    O.OP_CARE: "CARE", O.OP_DROP: "DROP",
}


def unit_action(op: int, arg: int, qty: int):
    op = int(op)
    if op in _UNIT_SIMPLE:
        return [_UNIT_SIMPLE[op]]
    if op == O.OP_PLANT:
        return ["PLANT", spec.CROPS[int(arg)]]
    if op == O.OP_PICKUP:
        return ["PICKUP", spec.ITEMS[int(arg)], int(qty)]
    if op == O.OP_PLACE:
        return ["PLACE", spec.ITEMS[int(arg)], int(qty)]
    return ["PASS"]


def market_actions(mkt_op, mkt_a, mkt_q, turn: int):
    out = []
    for s in range(spec.MAX_MARKET_ORDERS):
        op = int(mkt_op[turn, s])
        if op == O.MO_NONE:
            continue
        if op == O.MO_HIRE:
            out.append(["HIRE"])
        elif op == O.MO_BUY_LAND:
            out.append(["BUY_LAND"])
        elif op == O.MO_BUY_SEED:
            out.append(["BUY_SEED", spec.CROPS[int(mkt_a[turn, s])], int(mkt_q[turn, s])])
        elif op == O.MO_BUY_ANIMAL:
            out.append(["BUY_ANIMAL", spec.ANIMALS[int(mkt_a[turn, s])], int(mkt_q[turn, s])])
        elif op == O.MO_BUY_PRODUCT:
            out.append(["BUY_PRODUCT", spec.PRODUCTS[int(mkt_a[turn, s])], int(mkt_q[turn, s])])
        elif op == O.MO_SELL:
            out.append(["SELL", spec.PRODUCTS[int(mkt_a[turn, s])], int(mkt_q[turn, s])])
    return out


def turn_action(plan, turn: int, n_hands: int):
    unit_op, unit_a, unit_q, mkt_op, mkt_a, mkt_q = plan
    farmer = unit_action(unit_op[0, turn], unit_a[0, turn], unit_q[0, turn])
    hands = [
        unit_action(unit_op[h + 1, turn], unit_a[h + 1, turn], unit_q[h + 1, turn])
        for h in range(n_hands)
    ]
    return {"farmer": farmer, "hands": hands,
            "market": market_actions(mkt_op, mkt_a, mkt_q, turn)}
