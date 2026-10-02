"""`plan.MARKET_PACK_ON`: present the whole morning market row on turn 0.

The engine truncates each seat's market queue to `maxMarketOrdersPerTurn` = 10
a turn (`kaggle_environments/envs/kaggriculture/kaggriculture.py:551,557`), and
that cap is the only reason the morning has two rows: ten hire slots plus ten
purchase slots do not fit one turn. A day that presents fewer than eleven
orders in total does fit, and then both rows go out at `O.TURN_HIRE`, turn 1
resolves nothing at all, and the whole crew -- the blocks that owe a PICKUP
included, since the goods reached the shed in turn 0's market phase -- starts
at `ops.ROUTE_BASE_PACK` instead of `O.ROUTE_BASE`.

Nothing about the purse moves with it: `SELL_TURNS` starts at 3, so no revenue
lands between turn 0 and turn 1 either way, and off the switch turn 1's unit
phase is all PASS -- so money and shed are identical at the moment the row
resolves, whichever turn it resolves on.

The `test_off_*` half is the identity half: off, `pack` is `None`, `_market`
emits the two rows on the two turns it always did and `route_base` is the
expression it always was. The digests are the whole six-array plan on
`test_route_early`'s seeded boards, taken off the tree at `a54f16f` -- the
commit before this switch, with the promoted stack (ROUTE_SPLIT, SURVIVAL_
WATER, TAIL_CARE, FEED_MANDATORY) at its shipped default, which is what this
file's fixtures leave alone.
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
from test_budget_order import _macro
from test_route_early import (PIN_SEEDS, _acting_units, _digest, _plan, _row,
                              _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MO = spec.MAX_MARKET_ORDERS


#: Only `MARKET_PACK_ON` moves between the halves. Unlike the digest files
#: before it this one pins the planner as it *ships* -- `ROUTE_SPLIT_ON`,
#: `SURVIVAL_WATER_ON`, `TAIL_CARE_ON` and `FEED_MANDATORY_ON` all on -- since
#: `a54f16f` is the promoted stack and the claim being made is that the switch
#: is inert on top of it.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MARKET_PACK_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "MARKET_PACK_ON", True)


#: A day the switch fits into one turn: four hands (the crew ramp names the
#: size outright) against a five-order row -- feed wheat for three hungry
#: geese, and one seed order per crop the target asks for.
PACKED = dict(crew_target=4, plant_target=(0, 2, 2, 2, 2))
#: The same board with eight hands. 8 + 5 is thirteen orders, so the day keeps
#: the two-row layout exactly.
UNPACKED = dict(crew_target=8, plant_target=(0, 2, 2, 2, 2))


def _case(crew_target, plant_target, land_bias=0, **kw):
    board = dict(day=10, money=9_000, n_coop=3, n_ripe=12, yld=5)
    board.update(kw)
    view = _view(**board)
    macro = _macro(plant_target=np.asarray(plant_target, np.int32),
                   crew_target=np.int32(crew_target),
                   land_bias=np.int32(land_bias))
    return view, macro


def _morning(plan):
    """The morning's live market orders, whichever of the two turns holds them."""
    return _row(plan, O.TURN_HIRE) + _row(plan, O.TURN_BUY) + _row(plan, O.TURN_HIRE_WIDE)


def _pack_plan(monkeypatch, on_, view, macro):
    monkeypatch.setattr(P, "MARKET_PACK_ON", on_)
    return _plan(view, macro)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `test_route_early.PIN_SEEDS`, taken
#: off a clean `a54f16f` tree. Regenerate only with a measured reason to move
#: the plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


# =========================================================================
# ON: the day that fits presents once and the crew starts a turn earlier
# =========================================================================

def test_on_packs_the_fitting_day_onto_turn_zero(on):
    """Four hires and a five-order purchase row is nine of the engine's ten
    slots, so both rows go out at turn 0, turn 1 carries nothing, and the block
    that owes a PICKUP takes it at turn 1 -- the row it waits on having
    resolved in turn 0's market phase. Turn 0 itself stays idle for everyone:
    the hire row resolves after turn 0's unit phase, so a unit that stepped
    there would move every hand `_spawn_hand` places [ops.ROUTE_BASE_PACK]."""
    plan = _plan(*_case(**PACKED))
    turn0, turn1 = _row(plan, O.TURN_HIRE), _row(plan, O.TURN_BUY)
    hires = [o for o, _, _ in turn0 if o == O.MO_HIRE]
    buys = [o for o, _, _ in turn0 if o != O.MO_HIRE]
    assert len(hires) == 4 and len(buys) == 5, (turn0, turn1)
    assert [o for o, _, _ in turn0[:4]] == [O.MO_HIRE] * 4, \
        "the hires must lead the row: the engine spends their coins first"
    assert turn1 == [] and _row(plan, O.TURN_HIRE_WIDE) == []

    unit_op = plan[0]
    picks = [(u, t) for u in range(spec.MAX_UNITS) for t in range(spec.TURNS_PER_DAY)
             if int(unit_op[u, t]) == O.OP_PICKUP]
    assert picks, "the board is meant to own a pickup"
    assert min(t for _, t in picks) == O.ROUTE_BASE_PACK
    assert _acting_units(plan, O.TURN_HIRE) == []


def test_on_leaves_the_day_that_does_not_fit_exactly_as_it_was(monkeypatch):
    """Eight hires beside the same five-order row is thirteen orders, which no
    turn takes, so the day keeps the two-row layout and the whole plan with
    it."""
    view, macro = _case(**UNPACKED)
    a = _pack_plan(monkeypatch, False, view, macro)
    b = _pack_plan(monkeypatch, True, view, macro)
    assert len(_row(a, O.TURN_HIRE)) == 8 and len(_row(a, O.TURN_BUY)) == 5
    assert _digest(a) == _digest(b)


def test_on_presents_every_order_and_never_more_than_the_engine_takes(monkeypatch):
    """Two things at once, because they are the same claim from both sides: the
    packed row is never longer than `MAX_MARKET_ORDERS` (past it the engine
    truncates in silence), and no order is lost on the way -- the morning's
    orders ON are the morning's orders OFF, the same multiset moved between
    turns. The BUY row is a fixed ten-slot layout with holes in it, so this is
    what the compaction in `_market` is for."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        a = _pack_plan(monkeypatch, False, view, macro)
        b = _pack_plan(monkeypatch, True, view, macro)
        for turn in range(spec.TURNS_PER_DAY):
            assert len(_row(b, turn)) <= MO, (s, turn)
        assert sorted(_morning(a)) == sorted(_morning(b)), s


def test_on_keeps_buy_land_on_its_sell_turn_and_the_crew_behind_the_unlock(on):
    """BUY_LAND is not in the row this switch packs and cannot be [M2]: it
    rides the spare tenth slot of `SELL_TURNS[0]`, the only place in the day a
    purchase the morning's own sale funds can sit. So a land day packs its
    hires and its purchases like any other and the quadrant still unlocks in
    `SELL_TURNS[0]`'s market phase -- `land_lead` grows by the turn
    `route_base` gave up, and no unit works a tile before `SELL_TURNS[0] + 1`.
    The morning PICKUPs are not tile work and do move up: they need the shed,
    not the land."""
    plan = _plan(*_case(crew_target=4, plant_target=(0, 0, 2, 0, 0),
                        land_bias=3_000, day=8, money=30_000, nquad=1))
    land = [(t, s) for t in range(spec.TURNS_PER_DAY) for s in range(MO)
            if int(plan[3][t, s]) == O.MO_BUY_LAND]
    assert land == [(O.SELL_TURNS[0], MO - 1)], land
    assert _row(plan, O.TURN_BUY) == [], "the board is meant to pack"

    unit_op = plan[0]
    worked = [(u, t) for u in range(spec.MAX_UNITS) for t in range(spec.TURNS_PER_DAY)
              if int(unit_op[u, t]) not in (O.OP_PASS, O.OP_PICKUP)]
    assert worked, "the board is meant to work"
    assert min(t for _, t in worked) >= O.SELL_TURNS[0] + 1


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (packing the whole row into one turn) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04: on day 0 the plan buys
#: `OPEN_PUMP_UNITS` wheat behind the hire row and sells it back from the BUY
#: row's head slot, to quote the class-A opening's own wheat off a drained pot.
#: It is pinned off for this file the way `0772ed3` pinned `EARLY_SELL_ON` off
#: for the modules it moved under: `plan` asserts OPEN_PUMP and
#: MARKET_PACK are mutually exclusive (both own turn 1), so the ON half here
#: cannot run with the new default live.
#: `tests/test_open_pump.py` owns both halves of the switch.
@pytest.fixture(autouse=True)
def _open_pump_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)


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
