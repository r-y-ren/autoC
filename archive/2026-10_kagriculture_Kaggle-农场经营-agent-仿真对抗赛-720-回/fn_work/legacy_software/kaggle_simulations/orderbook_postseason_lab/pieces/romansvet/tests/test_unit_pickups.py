"""A unit pays only for the pickups its own block consumes, inside its own
22-turn budget (PLANNER_V3_1 section 0.12); a unit whose block needs no
pickup starts walking at ROUTE_BASE instead of idling through the other
units' pickup turns.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
from test_budget_order import _macro, geese

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _farm(day, tiles, shed, money=1000):
    """`tiles`: dict position -> dict(kind=, occ=, t_day=, t_cons=, t_yield=, t_fert=)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_day, t_cons, t_yield, t_fert = z - 1, z.copy(), z.copy(), z.copy(), z - 1
    for pos, t in tiles.items():
        kind[pos] = t["kind"]
        occ[pos] = t.get("occ", -1)
        t_day[pos] = t.get("t_day", 0)
        t_cons[pos] = t.get("t_cons", 0)
        t_yield[pos] = t.get("t_yield", 0)
        t_fert[pos] = t.get("t_fert", -1)
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=t_fert, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _ripe_tomatoes(positions):
    return {p: {"kind": spec.KIND_PLANT, "occ": spec.I_TOMATO, "t_yield": 1} for p in positions}


def _feed_then_harvests():
    """A hungry goose at position 0 (mandatory, so the farmer's block starts
    there and needs a wheat pickup) and thirty ripe tomatoes behind it; two
    units."""
    tiles = {0: {"kind": spec.KIND_COOP, "occ": 0, "t_cons": 1}}
    tiles.update(_ripe_tomatoes(range(1, 31)))
    return _farm(13, tiles, {spec.I_WHEAT: 1})


def test_only_the_unit_that_picks_up_pays_the_turn():
    unit_op = P.build_day(np, _feed_then_harvests(), _macro())[0]
    assert int(unit_op[0, O.ROUTE_BASE]) == O.OP_PICKUP
    assert int(unit_op[0, O.ROUTE_BASE + 1]) in MOVES
    assert int(unit_op[1, O.ROUTE_BASE]) in MOVES              # no idle pickup turn
    assert int((unit_op[1] == O.OP_PICKUP).sum()) == 0


def test_three_kinds_are_picked_up_on_consecutive_turns_by_the_block_that_needs_them():
    # farmer's block: hungry goose (wheat), tomato worth fertilizing (fertilizer),
    # free coop with a goose in the shed (place); second unit: ripe tomatoes only
    tiles = {0: {"kind": spec.KIND_COOP, "occ": 0, "t_cons": 1},
             # day 13: fires 14..16 in window
             1: {"kind": spec.KIND_PLANT, "occ": spec.I_TOMATO, "t_day": 5, "t_cons": 1},
             2: {"kind": spec.KIND_COOP}}
    tiles.update(_ripe_tomatoes(range(3, 33)))
    view = _farm(13, tiles, {spec.I_WHEAT: 1, spec.I_FERT: 1, spec.I_GOOSE: 1})
    unit_op, unit_a = P.build_day(np, view, _macro(animal_want=geese(1)))[:2]
    b = O.ROUTE_BASE
    assert [int(o) for o in unit_op[0, b:b + 3]] == [O.OP_PICKUP] * 3
    assert [int(a) for a in unit_a[0, b:b + 3]] == [spec.I_WHEAT, spec.I_FERT, spec.I_GOOSE]
    assert int(unit_op[0, b + 3]) in MOVES
    assert int(unit_op[1, b]) in MOVES
    assert int((unit_op[1] == O.OP_PICKUP).sum()) == 0


def test_every_unit_stays_inside_the_turns_it_has():
    """Turn 0 belongs to the hire row for everybody, and a unit's ops fit in
    what is left of the day. `TURN_BUY` and not `ROUTE_BASE` is the floor since
    `ROUTE_SPLIT_ON`: a block the BUY row does not feed steps out there, so the
    window it has to fit inside is 23 turns rather than 22 -- and a PICKUP,
    which needs that row resolved, still never lands before `ROUTE_BASE`."""
    for view, macro in ((_feed_then_harvests(), _macro()),
                        (_farm(13, _ripe_tomatoes(range(100)), {}), _macro())):
        unit_op = P.build_day(np, view, macro)[0]
        for u in range(spec.MAX_UNITS):
            busy = int((unit_op[u, O.TURN_BUY:] != O.OP_PASS).sum())
            assert busy <= spec.TURNS_PER_DAY - O.TURN_BUY
            assert int((unit_op[u, :O.TURN_BUY] != O.OP_PASS).sum()) == 0
            assert int((unit_op[u, :O.ROUTE_BASE] == O.OP_PICKUP).sum()) == 0


def test_pickups_precede_every_move():
    unit_op = P.build_day(np, _feed_then_harvests(), _macro())[0]
    for u in range(2):
        row = [int(o) for o in unit_op[u]]
        if O.OP_PICKUP in row:
            last_pick = max(i for i, o in enumerate(row) if o == O.OP_PICKUP)
            first_move = min(i for i, o in enumerate(row) if o in MOVES)
            assert last_pick < first_move


def test_per_unit_pickups_agree_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _feed_then_harvests(), _macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
