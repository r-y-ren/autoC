"""`plan.LATE_STRAW_CAP_ON`: stop planting the contested crop late.

The finding (2026-09-05, `scratchpad/lossanat/`): against the six 1950-2110
band tapes the opponent's book is fixed -- 264 STRAWBERRY every game, win or
loss -- and 73 % of the win/loss separation lands on days 26-29. On the boards
we win we sell 162 units of strawberry; on the boards we lose, 255 head-on into
theirs, and the day-22 price is 60 against 98. The cap is at the PLANTING
decision, because by the time a sell rule could refuse the unit the seed, the
tile and twelve days of crew are already spent.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the same pin `test_endgame_tomato.py` uses.
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
from test_endgame_tomato import MIX, _planted
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _seeded_case
from test_route_early import _view as _base_view

from kagg3 import spec
from kagg3.core import plan as P

_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")


def _day(view=None, mix=MIX, **kw):
    return _plan(view if view is not None else _base_view(**kw),
                 _macro(plant_target=np.asarray(mix, np.int32),
                        crew_target=np.int32(6)))


def _mix_out(view, mix=MIX):
    macro = _macro(plant_target=np.asarray(mix, np.int32), crew_target=np.int32(6))
    return [int(x) for x in np.asarray(
        P._late_straw_cap(np, view, macro).plant_target)]


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "LATE_STRAW_CAP_ON", True)


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """OFF every expression re-evaluates to the one it replaced, so a theta
    trained before the switch decodes byte for byte."""
    monkeypatch.setattr(P, "LATE_STRAW_CAP_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_on_plants_no_strawberry_from_the_cap_day(on):
    """From `LATE_STRAW_CAP_DAY` the mix has no strawberry in it, and the day
    plants none."""
    view = _base_view(day=P.LATE_STRAW_CAP_DAY)
    assert _mix_out(view)[spec.I_STRAWBERRY] == 0
    assert spec.I_STRAWBERRY not in _planted(_day(view))


def test_on_keeps_the_total_and_the_other_crops_proportions(on):
    """A mix change and not a development change: the share strawberry would
    have taken goes to the crops the brain also chose, so the day's tile, seed
    and labour budget is sized against the same number."""
    got = _mix_out(_base_view(day=P.LATE_STRAW_CAP_DAY))
    assert sum(got) == int(np.sum(MIX))
    assert got[spec.I_WHEAT] >= MIX[spec.I_WHEAT]
    assert got[spec.I_CARROT] >= MIX[spec.I_CARROT]
    assert got[spec.I_MELON] >= MIX[spec.I_MELON]


def test_on_leaves_the_days_before_the_cap_alone(on, monkeypatch):
    """Before the cap day the midgame's cash crop is untouched -- the
    opponent's book has not reached the market yet."""
    view = _base_view(day=P.LATE_STRAW_CAP_DAY - 1)
    assert _mix_out(view) == [int(x) for x in MIX]
    fired = _digest(_day(view))
    monkeypatch.setattr(P, "LATE_STRAW_CAP_ON", False)
    assert fired == _digest(_day(view))


def test_on_leaves_a_strawberry_only_mix_alone(on):
    """No proportion to fill into: dropping the tiles outright would be a
    development change made by a mix rule, so the day keeps its mix."""
    only = np.zeros(spec.N_CROPS, np.int32)
    only[spec.I_STRAWBERRY] = 6
    assert _mix_out(_base_view(day=P.LATE_STRAW_CAP_DAY), mix=only) == list(only)


def test_on_does_not_touch_the_tiles_already_carrying_strawberry(on):
    """The planting decision, not the sell rule: only `plant_target` moves."""
    view = _base_view(day=P.LATE_STRAW_CAP_DAY)
    macro = _macro(plant_target=MIX.copy(), animal_want=np.array([2, 1, 1], np.int32),
                   crew_target=np.int32(6))
    out = P._late_straw_cap(np, view, macro)
    assert out._replace(plant_target=macro.plant_target) == macro


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
