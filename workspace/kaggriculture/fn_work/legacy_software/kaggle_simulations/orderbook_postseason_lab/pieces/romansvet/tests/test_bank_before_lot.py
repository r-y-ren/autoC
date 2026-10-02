"""`plan.BANK_BEFORE_LOT_ON`: bank the morning's harvest before lot 2.

THE WALL the switch is cut against (`scratchpad/hour0b/report.txt`): the
champion's harvests ride home in the units' hands until `_end_of_day` dumps
them, so every lot of the day sells yesterday's shed -- and lot 1, on turn 1
under `EARLY_SELL_ON` mode "A", already carries virtually the whole of it. The
only way today's harvest reaches today's market is an explicit mid-day DROP.

The switch reuses `MELON_OPEN_ON`'s per-unit excursion inside `_routes` and
rewrites the trigger from a crop to a clock and a load: the DROP has to land on
or before `O.SELL_TURNS[1]`, the block has to be carrying `BANK_MIN_VALUE`
coins of harvest by then, the leg has to cost at most `BANK_MAX_TURNS` turns,
and nothing after the drop rank may still consume a PICKUP (OP_DROP empties the
unit's hands). What the excursion banks is added to lot 2's row, because
`SELL.allocate` runs once at dawn over the hour-0 shed and would otherwise sell
straight past it.

The `test_off_*` half is the identity half: off, `bank` is `None`, `_routes`
compiles no excursion and returns `banked` as `None`, and the lots are the
allocation they always were. The digests are the whole six-array plan on
`test_route_early`'s seeded boards, taken off the tree at `bdcf5f9` -- the
commit this switch was cut into -- with the shipped stack (DROP, HORIZON_DROP,
ROUTE_SPLIT, SURVIVAL_WATER, TAIL_CARE, FEED_MANDATORY **and EARLY_SELL**) at
its default, which is what this file's fixtures leave alone.
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
from test_route_early import (PIN_SEEDS, _digest, _plan, _seeded_case)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", True)


def _drops(plan):
    """[(unit, turn)] of every DROP the plan emits."""
    unit_op = np.asarray(plan[0])
    return [(int(u), int(t)) for u, t in np.argwhere(unit_op == O.OP_DROP)]


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `test_route_early.PIN_SEEDS`, taken
#: off the tree at `bdcf5f9` -- the commit before this switch -- so they pin the
#: pre-switch planner and not this file's own output. Unlike
#: `test_early_sell.py`'s and `test_fert_volume.py`'s, these are taken with the
#: shipped default of every other switch, `EARLY_SELL_ON` included: that is the
#: planner this one has to leave alone. Regenerate only with a measured reason
#: to move the plan.
PIN = ("b00faee2c2fa62fb", "efdb388e82cfc767", "233f9b98397829f1", "7a597ea77ef69364",
       "561174c8fc4cb1ca", "135b5ad85adc6080", "c0c62f92bf47d668", "51625374bbc8f568",
       "39c94535c69b69de", "3a45eec39c1f2ce8", "308028864d33232b", "26afc79decfc7a22")


def test_off_plan_is_byte_identical_to_the_shipped_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_routes_returns_no_banked_mask(off):
    """`bank` is `None`, so the ninth return value is too."""
    view, macro = _seeded_case(1)
    P.build_day(np, view, macro)          # smoke: the OFF path still builds
    z = np.zeros((100, P.CHAIN_MAX), np.int32)
    chain_op = np.full((100, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain_op[:, 0] = O.OP_WATER
    picks = np.zeros((3, 100), bool)
    out = P._routes(np, chain_op, z, z, np.ones(100, np.int32),
                    np.arange(100, dtype=np.int32), np.int32(100), picks,
                    np.int32(3), np.int32(20), np.int32(0))
    assert len(out) == 9 and out[8] is None


def test_off_drops_only_on_the_drop_day(off):
    """Off, the only DROP in the season is `DROP_ON`'s terminal return leg."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        if int(view.day) > O.LAST_SHED_DAY:
            continue
        assert _drops(_plan(view, macro)) == [], s


# =========================================================================
# ON: the excursion, and the row that meets it
# =========================================================================

def test_on_every_drop_lands_before_the_second_lot(on):
    """The whole point of the trigger: a DROP the turn-10 lot cannot see is a
    DROP that banks nothing today. A unit acts before its turn's market [LAW],
    so landing *on* `O.SELL_TURNS[1]` still makes the lot."""
    seen = 0
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        if int(view.day) > O.LAST_SHED_DAY:
            continue
        for _u, t in _drops(_plan(view, macro)):
            seen += 1
            assert t <= O.SELL_TURNS[1], (s, t)
    assert seen > 0, "no board in the pin set fires the excursion"


def test_on_a_dropping_unit_keeps_working_afterwards(on):
    """`MIDDAY_DROP_ON`'s post-mortem in one assertion: the excursion is a
    second block, not the end of the day. Every unit that DROPs has at least
    one live op after it."""
    fired = False
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        if int(view.day) > O.LAST_SHED_DAY:
            continue
        plan = _plan(view, macro)
        unit_op = np.asarray(plan[0])
        for u, t in _drops(plan):
            fired = True
            assert (unit_op[u, t + 1:] != O.OP_PASS).any(), (s, u, t)
    assert fired


def test_on_a_dropping_block_owes_no_pickup_after_the_drop(on):
    """OP_DROP dumps the whole inventory, so a block that still owes a FEED or
    a FERTILIZE may not bank in the middle of itself."""
    carried = (O.OP_FEED, O.OP_FERTILIZE, O.OP_PLACE)
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        if int(view.day) > O.LAST_SHED_DAY:
            continue
        plan = _plan(view, macro)
        unit_op = np.asarray(plan[0])
        for u, t in _drops(plan):
            after = unit_op[u, t + 1:]
            assert not any((after == op).any() for op in carried), (s, u, t)


def test_on_the_banked_units_are_offered_on_lot_two(on):
    """The second half. A day whose route banks something asks lot 2 for at
    least as much as the same day asks it off."""
    P.BANK_BEFORE_LOT_ON = False
    base = {s: _plan(*_seeded_case(s)) for s in PIN_SEEDS}
    P.BANK_BEFORE_LOT_ON = True
    lot2 = O.SELL_TURNS[1]
    moved = 0
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        if int(view.day) > O.LAST_SHED_DAY:
            continue
        plan = _plan(view, macro)
        if not _drops(plan):
            continue
        op_b, qty_b = np.asarray(base[s][3]), np.asarray(base[s][5])
        op_a, qty_a = np.asarray(plan[3]), np.asarray(plan[5])
        sold_b = qty_b[lot2][op_b[lot2] == O.MO_SELL].sum()
        sold_a = qty_a[lot2][op_a[lot2] == O.MO_SELL].sum()
        assert sold_a >= sold_b, (s, sold_b, sold_a)
        moved += int(sold_a > sold_b)
    assert moved > 0, "no board raised lot 2's ask"


def test_on_the_day_keeps_its_turn_budget(on):
    """The excursion costs its walk, not the tail of the day: no unit's last
    live turn moves past the end of the day, and the day is still 24 turns."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        plan = _plan(view, macro)
        assert np.asarray(plan[0]).shape[1] == spec.TURNS_PER_DAY


#: `plan.BANK_BEFORE_LOT_ON` is this file's own switch, but its OFF digests
#: also predate `plan.TAIL_FILL_ON`, which went on by default beside it on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: filler writes into PASS turns the excursion never claims, so pinning it off
#: here keeps the OFF pin meaning "the planner this switch was cut into" and
#: keeps `_worked`-style tile bookkeeping honest; `tests/test_tail_fill.py`
#: owns the filler.
@pytest.fixture(autouse=True)
def _tail_fill_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
