"""GAPFIX1 switch [GAP_FILL_RESID / GAP_FILL_LATE_RESID]: the share rule's `qfloor(dev_frac * n_free)` leaves the last
1-2 free tiles unasked every day (the farthest by DIST_SHED, live ep 113622191 tile (0,9) empty d10-20).

Claims: OFF by default and byte-identical to master on three days; ON lifts a total ask that leaves 1..k free slots
unasked to n_free, only inside the day window, only on crops that still mature, split by the day's own ask (all to
wheat when none is asked); a bigger gap is untouched unless the late window allows it.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import types

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain as B
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master digest (tests/test_labour1.py, tests/test_q4_relay.py)


def _plan(view, pt=(2, 1, 0, 0, 0)):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=np.array(pt, np.int32))))


def test_off_by_default():
    assert P.GAP_FILL_RESID == 0 and P.GAP_FILL_LATE_RESID == 0 and P.GAP_FILL_LATE_CROP is None
    assert P.GAP_FILL_DAYS == (1, 27) and P.GAP_FILL_LATE_DAYS == (20, 26)
    for s in ("GAP_FILL_RESID", "GAP_FILL_LATE_RESID"):
        assert s not in P.SWITCH_GENES


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def _view(day, n_free_tiles):
    return types.SimpleNamespace(day=np.int32(day), n_free=n_free_tiles)


def test_gap_fill(monkeypatch):
    monkeypatch.setattr(B, "n_free_slots", lambda xp, obs, land=None: np.int32(obs.n_free))
    monkeypatch.setattr(P, "GAP_FILL_RESID", 2)
    m = _macro(plant_target=np.array([2, 1, 3, 0, 0], np.int32))
    tot = int(np.sum(m.plant_target)) + int(np.sum(m.animal_want))
    for gap in (1, 2):
        add = np.asarray(P._gap_fill(np, _view(12, tot + gap), m).plant_target) - np.asarray(m.plant_target)
        assert int(add.sum()) == gap and (add >= 0).all()
    for n, d in ((tot + 3, 12), (tot, 12), (tot - 2, 12), (tot + 1, 0), (tot + 1, 28)):   # gap out of range / window
        assert np.asarray(P._gap_fill(np, _view(d, n), m).plant_target).tolist() == [2, 1, 3, 0, 0]
    # the late window fills a big gap; crops that cannot mature by pay_day get nothing
    monkeypatch.setattr(P, "GAP_FILL_LATE_RESID", 99)
    out = np.asarray(P._gap_fill(np, _view(24, tot + 9), m).plant_target) - np.asarray(m.plant_target)
    assert int(out.sum()) == 9 and out[spec.I_TOMATO] == 0 and out[spec.I_WHEAT] + out[spec.I_CARROT] == 9
    monkeypatch.setattr(P, "GAP_FILL_LATE_CROP", spec.I_CARROT)                         # late crop override: all to carrot
    oc = np.asarray(P._gap_fill(np, _view(24, tot + 9), m).plant_target) - np.asarray(m.plant_target)
    assert oc.tolist() == [0, 9, 0, 0, 0]
    oc2 = np.asarray(P._gap_fill(np, _view(12, tot + 2), m).plant_target) - np.asarray(m.plant_target)
    assert int(oc2.sum()) == 2 and oc2[spec.I_CARROT] <= 1                               # outside the late window: ask split
    monkeypatch.setattr(P, "GAP_FILL_LATE_CROP", None)
    m0 = _macro(plant_target=np.array([0, 0, 0, 0, 0], np.int32))                      # nothing asked: all to wheat
    t0 = int(np.sum(m0.animal_want))
    a0 = np.asarray(P._gap_fill(np, _view(12, t0 + 1), m0).plant_target)
    assert a0[spec.I_WHEAT] == 1 and int(a0.sum()) == 1
