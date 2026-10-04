"""`plan.HARVEST_FIRST_ON`: harvest ranks before pickup ranks, inside a block.

`BANK_BEFORE_LOT_ON`'s post-mortem (`scratchpad/bank/report.txt`) found the
real wall behind its own trigger: a block's ranks come off `task_order`'s
tier-then-score sweep, which interleaves HARVEST/COLLECT_FERT ranks (value-
producing, hands-filling) with FEED/FERTILIZE/PLANT ranks (consume something
the BUY row or a PICKUP already loaded) in whatever order the value model
happens to rank them -- 0 coins in hand at the best rank a DROP could still
reach by turn 10, against 505 coins the whole block eventually harvests.

This switch reorders each unit's *already-decided* block into a stable
two-group sweep -- every HARVEST/COLLECT_FERT rank first, then everything
else, then every FEED/FERTILIZE/PLANT rank last -- priced against a wall: a
block only takes the new order if its walk-plus-work still fits the turns it
already had. So the admitted tile set, pickup credit, hire credit and
`covered` never move; only when a tile is worked can change.

The `test_off_*` half is the identity half: off, `harvest_first` is `None`,
`_routes` compiles none of the reorder and every block decodes exactly as it
always did. The digest is `test_bank_before_lot.py`'s own OFF pin -- the
current shipped default (DROP, HORIZON_DROP, ROUTE_SPLIT, SURVIVAL_WATER,
TAIL_CARE, FEED_MANDATORY and EARLY_SELL at their defaults) -- since this
switch changes nothing about it either.
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
import pytest
from test_bank_before_lot import PIN
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "HARVEST_FIRST_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "HARVEST_FIRST_ON", True)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_shipped_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_routes_ignores_the_new_argument(off):
    """`P.HARVEST_FIRST_ON` off, `_routes` is called with `harvest_first=None`
    regardless of the caller -- smoke it directly, as `test_bank_before_lot.py`
    does for `bank`."""
    z = np.zeros((100, P.CHAIN_MAX), np.int32)
    chain_op = np.full((100, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain_op[:, 0] = O.OP_WATER
    picks = np.zeros((3, 100), bool)
    out = P._routes(np, chain_op, z, z, np.ones(100, np.int32),
                    np.arange(100, dtype=np.int32), np.int32(100), picks,
                    np.int32(3), np.int32(20), np.int32(0))
    assert len(out) == 9


# =========================================================================
# ON: the reorder, and its safety properties
# =========================================================================

def test_on_never_crashes_and_keeps_the_shape(on):
    """The switch is safe to run across the whole pin set: no crash, and the
    plan's shape is untouched. (`test_on_a_block_visits_its_harvest_before_its_feed`
    below proves the mechanism itself fires, directly; the 899009257 real-game
    census in `scratchpad/harvest_first/hf_probe.py` is what shows the rate on
    a real 30-day season -- 48% of active unit-days, once the reorder is also
    gated on not leaving the block's tail cursor farther from a shed access,
    which the small synthetic `PIN_SEEDS` boards do not reliably exercise.)"""
    for s in PIN_SEEDS:
        plan = _plan(*_seeded_case(s))
        op = np.asarray(plan[0])
        assert op.min() >= 0 and op.max() < O.N_OPS, s


def test_on_the_day_keeps_its_turn_budget(on):
    """The reorder costs turns already in the block's own window, not the
    tail of the day: the plan is still `TURNS_PER_DAY` wide."""
    from kagg3 import spec
    for s in PIN_SEEDS:
        plan = _plan(*_seeded_case(s))
        assert np.asarray(plan[0]).shape[1] == spec.TURNS_PER_DAY


def test_on_a_block_visits_its_harvest_before_its_feed(on):
    """The mechanism, direct: a hand-built block whose sweep order is
    FEED-then-HARVEST-then-FERTILIZE on three tiles a single unit can reach
    comes out of `_routes` HARVEST first and FERTILIZE last, off the same
    `chain_op`/`order` that (off) would visit them in sweep order."""
    z = np.zeros((100, P.CHAIN_MAX), np.int32)
    chain_op = np.full((100, P.CHAIN_MAX), O.OP_PASS, np.int32)
    # Three tiles, all reachable at zero walking distance from a unit's own
    # spawn stripe (SPAWN_X/SPAWN_Y put every unit on a shed-access tile, and
    # `order[0:3]` are `SERP_X[0:3]`/`SERP_Y[0:3]`'s own tiles): FEED, then
    # HARVEST, then FERTILIZE, one op each so every tile costs one turn.
    chain_op[0, 0] = O.OP_FEED
    chain_op[1, 0] = O.OP_HARVEST
    chain_op[2, 0] = O.OP_FERTILIZE
    n_ops = np.zeros(100, np.int32)
    n_ops[:3] = 1
    picks = np.zeros((3, 100), bool)
    picks[0, 0] = True   # FEED consumes the feed-wheat pickup kind
    picks[1, 2] = True   # FERTILIZE consumes the fertilizer pickup kind
    order = np.arange(100, dtype=np.int32)

    off_out = P._routes(np, chain_op, z, z, n_ops, order, np.int32(3), picks,
                        np.int32(1), np.int32(20), np.int32(0))
    on_out = P._routes(np, chain_op, z, z, n_ops, order, np.int32(3), picks,
                       np.int32(1), np.int32(20), np.int32(0),
                       harvest_first=True)

    move_codes = (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)
    off_ops = [int(x) for x in np.asarray(off_out[0])[0] if int(x) not in move_codes]
    on_ops = [int(x) for x in np.asarray(on_out[0])[0] if int(x) not in move_codes]
    assert off_ops == [O.OP_FEED, O.OP_HARVEST, O.OP_FERTILIZE]
    assert on_ops == [O.OP_HARVEST, O.OP_FEED, O.OP_FERTILIZE]
    # Pickup credit, hire credit and coverage are the tile set's, not the
    # visiting order's: unaffected.
    assert np.array_equal(np.asarray(off_out[3]), np.asarray(on_out[3]))
    assert np.array_equal(np.asarray(off_out[4]), np.asarray(on_out[4]))
    assert np.array_equal(np.asarray(off_out[5]), np.asarray(on_out[5]))


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests in this file were taken before the pair existed and still mean
#: what they meant -- "OFF, this file's switch leaves the planner it was cut
#: into alone" -- so the pair is pinned off here the way `EARLY_SELL_ON` and
#: `OPEN_PUMP_ON` were pinned off before it (`854b86b`).
#: `tests/test_tail_fill.py` and `tests/test_bank_before_lot.py` own the two.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
