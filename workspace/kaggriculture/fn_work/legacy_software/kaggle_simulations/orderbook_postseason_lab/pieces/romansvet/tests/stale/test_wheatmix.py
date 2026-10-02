"""WHEATMIX1 switches [Q3_EARLY_ON, LATE_MELON_OFF_ON, MIX_RELAY_ON, CREW_CAP_ON]:
the four top teams' shared recipe (Q4TEAMS1).

Claims: all OFF by default and byte-identical to master 45763c18 on three days;
Q3_EARLY buys Q3 in d7-9 when lot-1 sales cover it; LATE_MELON_OFF drops the
day's melon plantings after LATE_MELON_DAY and nothing else; MIX_RELAY adds
wheat plantings (with their seed) on free Q1-3 tiles from d10 without moving
the planner's other crops, and is inert before d10; CREW_CAP clamps the hires.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board, _plants, _seeds, _land

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master digest (tests/test_q4_relay.py), same on all three days
SW = ("Q3_EARLY_ON", "LATE_MELON_OFF_ON", "MIX_RELAY_ON", "CREW_CAP_ON")


def _plan(view, pt=(2, 1, 0, 0, 0)):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=np.array(pt, np.int32))))


def _hires(pl):
    return int(np.sum(pl[3] == O.MO_HIRE))


def test_off_by_default():
    for s in SW:
        assert getattr(P, s) is False and s not in P.SWITCH_GENES
    assert P.LATE_MELON_DAY == 9 and P.MIX_RELAY_WATER == "min" and P.MIX_RELAY_FERT is False
    assert P.CREW_CAP == (12, 11) and P.MIX_RELAY_DAYS == (10, 26)


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_q3_early(monkeypatch):
    off = _plan(_board(8, 2, money=2500))
    monkeypatch.setattr(P, "Q3_EARLY_ON", True)
    on = _plan(_board(8, 2, money=2500))
    assert _land(on) == 1 and _land(off) == 0
    assert _land(_plan(_board(11, 2, money=2500))) == _land(off)   # outside d7-9: the planner's own rule


def test_late_melon_off(monkeypatch):
    pt = (2, 1, 0, 0, 2)
    off = _plan(_board(12, 3), pt)
    monkeypatch.setattr(P, "LATE_MELON_OFF_ON", True)
    on = _plan(_board(12, 3), pt)
    assert _plants(off)[spec.I_MELON] > 0 and _plants(on)[spec.I_MELON] == 0
    assert _plants(on)[:spec.I_MELON] == _plants(off)[:spec.I_MELON]
    assert _digest(_plan(_board(9, 3), pt)) == _digest(_plan_off(monkeypatch, _board(9, 3), pt))


def _plan_off(monkeypatch, view, pt):
    with monkeypatch.context() as m:
        m.setattr(P, "LATE_MELON_OFF_ON", False)
        return _plan(view, pt)


def test_mix_relay_adds_wheat(monkeypatch):
    off = _plan(_board(12, 3))
    monkeypatch.setattr(P, "MIX_RELAY_ON", True)
    on = _plan(_board(12, 3))
    add = [b - a for a, b in zip(_plants(off), _plants(on))]
    assert add[spec.I_WHEAT] >= 4 and add[1:] == [0, 0, 0, 0]
    assert _seeds(on)[spec.I_WHEAT] >= _seeds(off)[spec.I_WHEAT] + add[spec.I_WHEAT] - 8   # 8 = board's shed seed
    assert _hires(on) >= _hires(off)


def test_mix_relay_inert_before_window(monkeypatch):
    base = _digest(_plan(_board(8, 3)))
    monkeypatch.setattr(P, "MIX_RELAY_ON", True)
    assert _digest(_plan(_board(8, 3))) == base


def test_crew_cap(monkeypatch):
    monkeypatch.setattr(P, "MIX_RELAY_ON", True)
    monkeypatch.setattr(P, "CREW_CAP_ON", True)
    monkeypatch.setattr(P, "CREW_CAP", (1, 1))
    assert _hires(_plan(_board(12, 3))) <= 1
