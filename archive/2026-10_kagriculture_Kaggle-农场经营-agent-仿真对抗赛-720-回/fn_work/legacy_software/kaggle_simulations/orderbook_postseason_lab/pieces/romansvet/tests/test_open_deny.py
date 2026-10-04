"""`plan.OPEN_DENY_ON`: the top tier's opening board, and none of its dump day.

The opening splice measured today (`scratchpad/deny/report.txt`) says the
opponent's 17k does not go to a price collapse -- their unit prices *rise* -- it
goes to volume, because kagg2's day-1 board is the recorded tape's to the tile
and the market is one shared, town-replenished demand stream per product. Our
shipped day 0 reaches the melon curve on day 14 against their day 10; the
opening's day 0 puts us level, and level is enough.

`MELON_OPEN_ON` already builds that board and was rejected at -14,289 a game --
on the same twelve ledger games it leaves our coins alone and hands the
opponent 18,855 -- for what its post-mortem blames on the day the crop
saturates: an excursion that fires after a block's last melon rank, and a melon
row that walks our own quote down before the opponent arrives. So this switch
is that switch minus its dump day: the three sites that build the day-0 board
answer to either switch (`plan.open_board`), and the two that trade on
`MELON_OPEN_HARVEST_DAY` still read `MELON_OPEN_ON` alone.

The `test_off_*` half is the identity half, pinned on the same digests
`tests/test_melon_open.py` pins -- a clean `git archive aae13e0` export's, the
planner before either switch existed.
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
from test_melon_open import PIN, _melon_lots, _melon_view
from test_route_early import PIN_SEEDS, _digest, _plan, _row, _seeded_case, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)
    monkeypatch.setattr(P, "OPEN_DENY_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)
    monkeypatch.setattr(P, "OPEN_DENY_ON", True)


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03 and moves the day's
#: first lot off `O.SELL_TURNS[0]`. Pinned off here for the same reason
#: `tests/test_melon_open.py` pins it off: the digests below are the plan
#: before it, and this switch answers nothing about the lot's turn.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_leaves_the_day_zero_mix_alone(off):
    """The shipped day-0 mix is the network's, untouched."""
    view = _view(day=P.MELON_OPEN_DAY, money=3_000)
    macro = _macro(plant_target=np.asarray((10, 9, 0, 0, 0), np.int32))
    seeds = {arg: qty for op, arg, qty in _row(_plan(view, macro), O.TURN_BUY)
             if op == O.MO_BUY_SEED}
    assert seeds.get(spec.I_MELON, 0) == 0


def test_open_board_is_the_or_of_the_two_switches(monkeypatch):
    """The three day-0 sites answer to either switch; nothing else does."""
    for melon, deny, want in ((False, False, False), (True, False, True),
                              (False, True, True), (True, True, True)):
        monkeypatch.setattr(P, "MELON_OPEN_ON", melon)
        monkeypatch.setattr(P, "OPEN_DENY_ON", deny)
        assert P.open_board() is want, (melon, deny)


# =========================================================================
# ON: the day-0 board, and only the day-0 board
# =========================================================================

def test_on_day_zero_seed_row_carries_the_melon_and_drops_the_carrot(on):
    """The board this switch is for: twelve melon bought on day 0 out of the
    carrot, the wheat kept for the feed and the rotation."""
    view = _view(day=P.MELON_OPEN_DAY, money=3_000)
    macro = _macro(plant_target=np.asarray((10, 9, 0, 0, 0), np.int32))
    seeds = {arg: qty for op, arg, qty in _row(_plan(view, macro), O.TURN_BUY)
             if op == O.MO_BUY_SEED}
    assert seeds.get(spec.I_MELON, 0) == P.MELON_OPEN_TILES
    assert seeds.get(spec.I_WHEAT, 0) > 0
    assert seeds.get(spec.I_CARROT, 0) == 0


def test_on_dump_day_emits_no_melon_row_and_no_excursion(on):
    """The whole difference from `MELON_OPEN_ON`: the day the crop saturates is
    the day it always was. No mid-day DROP, no melon-only rows -- the two parts
    that measured -14,289 a game stay behind their own switch."""
    plan = _plan(_melon_view(), _macro(crew_target=np.int32(6)))
    assert _melon_lots(plan) == []
    assert not (np.asarray(plan[0]) == O.OP_DROP).any()


def test_on_leaves_every_other_day_alone(on):
    """Only `MELON_OPEN_DAY` is rewritten."""
    view = _view(day=P.MELON_OPEN_DAY + 1, money=3_000)
    macro = _macro(plant_target=np.asarray((10, 9, 0, 0, 0), np.int32))
    seeds = {arg: qty for op, arg, qty in _row(_plan(view, macro), O.TURN_BUY)
             if op == O.MO_BUY_SEED}
    assert seeds.get(spec.I_MELON, 0) == 0


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
