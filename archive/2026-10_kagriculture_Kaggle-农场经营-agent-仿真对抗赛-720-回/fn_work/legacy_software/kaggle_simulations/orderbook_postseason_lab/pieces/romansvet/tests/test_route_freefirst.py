"""`plan.ROUTE_FREEFIRST_ON`: the morning wait, read per pickup kind.

`ROUTE_SPLIT_ON` already hands a block the turn between `O.TURN_BUY` and
`O.ROUTE_BASE` -- but only a block that owes **no PICKUP at all**, which is
the per-day test `_buy_row_units` names rather than a per-item one.  The
measured consequence is B's morning: 236.3 of 269.5 hour-1 unit-turns are PASS
and 210.4 units PICKUP at hour 2 (`docs/strategy/2026-09-14-turns.md`), i.e.
the held block is the pickup-owing one.

What the turn-1 BUY row actually feeds is a *kind*.  A unit collecting at
`O.TURN_BUY` draws last night's shed close, because turn 1's market phase runs
after turn 1's unit phase -- the ordering `_buy_row_units`' own docstring gives
for the seed.  So a block whose every owed kind has a zero purchase today is
fed by yesterday's stock and may collect at `O.TURN_BUY`; a block owing a kind
the day buys keeps the turn it has.  PLANT stays behind the row either way
(`free_first`).

OFF, the whole plan tuple is pinned against a pristine `git archive c5f68ac src`
tree, as `tests/test_prestock_v2.py` pins its own switch.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_prestock_v2 import PIN_BOARDS, _case, _digest, _pass_turns, _row

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _own_digests():
    return {cfg[0]: _digest(_plan(*_case(cfg))) for cfg in PIN_BOARDS}


def _head_digests():
    """The same four plans, built by a pristine `git archive c5f68ac src` tree in
    a subprocess -- the tree this switch was added to, not this file's own
    output."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


def _bought_items(plan):
    """The item ids the day's own BUY row delivers, in `PICK_ITEM` space."""
    out = set()
    for turn in range(O.FULL_MARKET_TURNS):
        for op, arg, qty in _row(plan, turn):
            if qty <= 0:
                continue
            if op == O.MO_BUY_PRODUCT:
                out.add(int(arg))
            elif op == O.MO_BUY_ANIMAL:
                out.add(int(spec.I_GOOSE + arg))
    return out


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert P.ROUTE_FREEFIRST_ON is False
    assert _own_digests() == _head_digests()


def test_off_keeps_every_pickup_behind_the_buy_row():
    """The state the switch widens: OFF, no unit touches a turn below
    `O.ROUTE_BASE` unless `ROUTE_SPLIT_ON` gave it one, and no PICKUP ever
    lands before `O.ROUTE_BASE`."""
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        early = plan[0][:, :O.ROUTE_BASE]
        assert not (early == O.OP_PICKUP).any(), cfg[0]


# =========================================================================
# ON: the turn, per kind
# =========================================================================

def test_on_drops_the_hour_0_1_pass_turns(monkeypatch):
    """The measurement the switch exists for.  The `stocked` board is a narrow
    day whose feed and fertilizer are already in the shed, so its blocks owe
    kinds the day does not buy and collect at `O.TURN_BUY`."""
    view, macro = _case(PIN_BOARDS[3])
    off = _pass_turns(_plan(view, macro), 0, 1)
    monkeypatch.setattr(P, "ROUTE_FREEFIRST_ON", True)
    on = _pass_turns(_plan(view, macro), 0, 1)
    assert on < off, (off, on)


def test_on_moves_no_unit_in_front_of_a_row_it_depends_on(monkeypatch):
    """The safety property.  Any PICKUP the switch pulls below `O.ROUTE_BASE`
    must be of an item today's own market rows do not deliver -- otherwise the
    unit would collect a quantity that does not exist yet."""
    monkeypatch.setattr(P, "ROUTE_FREEFIRST_ON", True)
    for cfg in PIN_BOARDS:
        plan = _plan(*_case(cfg))
        bought = _bought_items(plan)
        unit_op, unit_a = plan[0], plan[1]
        for u in range(unit_op.shape[0]):
            for t in range(O.ROUTE_BASE):
                if int(unit_op[u, t]) == O.OP_PICKUP:
                    assert int(unit_a[u, t]) not in bought, (cfg[0], u, t)
        # And never below the hire law's floor: a hand hired at `TURN_HIRE`
        # first acts at `TURN_BUY` [LAW, ops.ROUTE_BASE].
        acting = np.argwhere(unit_op != O.OP_PASS)
        if len(acting):
            assert int(acting[:, 1].min()) >= O.TURN_BUY, cfg[0]


def test_on_leaves_a_plant_first_block_where_it_was(monkeypatch):
    """A block whose first op is a PLANT on a seed-buying day is unchanged:
    `free_first` still holds it at `O.ROUTE_BASE`, because the seed bought at
    turn 1 is credited after turn 1's unit phase.  The `plant` board buys seed
    and owes no pickup, so the whole plan is identical."""
    view, macro = _case(PIN_BOARDS[0])
    off = _digest(_plan(view, macro))
    row = _row(_plan(view, macro), O.TURN_BUY)
    assert any(op == O.MO_BUY_SEED for op, _, _ in row), row
    monkeypatch.setattr(P, "ROUTE_FREEFIRST_ON", True)
    assert _digest(_plan(view, macro)) == off
    plan = _plan(view, macro)
    assert not (plan[0][:, :O.ROUTE_BASE] == O.OP_PLANT).any()


def test_on_is_inert_on_a_day_that_buys_what_the_blocks_collect(monkeypatch):
    """The other half of the gate.  The `feed` board's shed holds 4 wheat
    against 12 hungry geese, so the day buys the wheat its blocks pick up --
    and the switch must decline every one of them."""
    view, macro = _case(PIN_BOARDS[1])
    off = _digest(_plan(view, macro))
    assert spec.I_WHEAT in _bought_items(_plan(view, macro))
    monkeypatch.setattr(P, "ROUTE_FREEFIRST_ON", True)
    assert _digest(_plan(view, macro)) == off


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
