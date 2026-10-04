"""ENDWAVE1 [END_WAVE_ON]: the d23-27 end wave of 2-day crops on every free owned tile, crew = the non-wave argmax
(+END_WAVE_PLUS offered on a wave day), optional crew hold on d27-29.

Claims: OFF by default and byte-identical to master on three days; ON outside the wave window (hold None) is the same
plan; `_end_wave` adds exactly n_free - ask tiles, only wheat/carrot, only on the window, the crop filter holds; on a
wave day the plan plants more than OFF.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain as B
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master digest (tests/test_labour1.py)
PT = (2, 1, 0, 0, 0)


def _plan(view, pt=PT):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=np.array(pt, np.int32))))


def test_off_by_default():
    assert P.END_WAVE_ON is False and P.END_WAVE_DAYS == (23, 27) and P.END_WAVE_HOLD is None
    assert P.END_WAVE_CROPS == "BEST" and P.END_WAVE_PLUS == 1 and P.END_WAVE_CAP is None
    assert P._ew_pair("(21;27)") == (21, 27) == P._ew_pair((21, 27))
    assert "END_WAVE_ON" not in P.SWITCH_GENES


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_on_outside_window_identical(monkeypatch, d, q, m, w):
    monkeypatch.setattr(P, "END_WAVE_ON", True)
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def _wave(day, crops="BEST"):
    P_ct = _macro(plant_target=np.array([1, 0, 0, 0, 0], np.int32))
    v = _board(day, 3, money=60000)
    old = P.END_WAVE_CROPS
    P.END_WAVE_CROPS = crops
    try:
        out, extra = P._end_wave(np, v, P_ct, P.default_price_table())
    finally:
        P.END_WAVE_CROPS = old
    add = np.asarray(out.plant_target) - np.asarray(P_ct.plant_target)
    n_free = int(B.n_free_slots(np, v))
    return add, int(extra), n_free - 1 - int(np.sum(P_ct.animal_want))


@pytest.mark.parametrize("crops", ["BEST", "WHEAT", "CARROT"])
def test_end_wave_fills_free_tiles_short_crops_only(crops):
    add, extra, want = _wave(24, crops)
    assert extra == max(want, 0) > 0 and int(add.sum()) == extra
    assert add[2:].tolist() == [0, 0, 0] and (add >= 0).all()
    if crops == "WHEAT":
        assert add[spec.I_CARROT] == 0
    if crops == "CARROT":
        assert add[spec.I_WHEAT] == 0


@pytest.mark.parametrize("day", [22, 28, 29])
def test_end_wave_window_only(day):
    add, extra, _ = _wave(day)
    assert extra == 0 and add.tolist() == [0, 0, 0, 0, 0]


def test_wave_day_plants_more(monkeypatch):
    v = _board(24, 3, money=60000)
    off = _plan(v)
    monkeypatch.setattr(P, "END_WAVE_ON", True)
    on = _plan(v)
    n_off = int(np.sum(off[0] == O.OP_PLANT)); n_on = int(np.sum(on[0] == O.OP_PLANT))
    assert n_on > n_off


@pytest.mark.parametrize("day", [5, 24, 28])
def test_free_count_matches_brain(day):
    v = _board(day, 3, money=60000)
    assert int(P._ew_free(np, v)) == int(B.n_free_slots(np, v))
