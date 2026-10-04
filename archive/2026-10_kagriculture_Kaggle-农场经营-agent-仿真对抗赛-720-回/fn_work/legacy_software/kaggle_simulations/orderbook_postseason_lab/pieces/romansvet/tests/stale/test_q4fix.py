"""Q4FIX1 switches [plan.Q4_RELAY_ADMIT / TPU / DENSITY / CARROT, Q4_MIX]: the Q4 relay's plant/water/harvest tasks in
the mandatory tier with Q4-only placement, two-pool admission (relay + planner's own-crew set first) and the relay
hands sized from the admitted relay turns on top of the planner's crew.

Claims: OFF by default and byte-identical to the recorded days of tests/test_q4_relay.py (master digest); every new
switch is inert while `Q4_RELAY_ON` is off; ADMIT plants the whole FQ ask on Q4 and never hires fewer hands than the
planner alone; the carrot share sows carrot on Q4; DSM density asks 8 on the first relay day; MIX keeps the relay.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_endroute import _digest
from test_q4_prog import _board, _plan, _plants
from test_q4_relay import DAYS, MASTER

NEW = dict(Q4_RELAY_ADMIT=True, Q4_RELAY_DENSITY="DSM", Q4_RELAY_CARROT=25, Q4_MIX=True, Q4_RELAY_SPARE=True)
Q4 = np.asarray(P.SERP_QUAD) == int(spec.LAND_ORDER[2])


def _hires(pl):
    return int(np.sum(pl[3] == O.MO_HIRE))



def _relay(monkeypatch, **kw):
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_SCHED", "FQ")
    for k, v in kw.items():
        monkeypatch.setattr(P, k, v)


def test_off_by_default():
    assert P.Q4_RELAY_ADMIT is False and P.Q4_RELAY_DENSITY is None and P.Q4_RELAY_CARROT == 0
    assert P.Q4_MIX is False and P.Q4_RELAY_TPU == 16 and P.Q4_RELAY_SPARE is False
    assert not any(k in P.SWITCH_GENES for k in NEW)


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_new_switches_inert_without_relay(monkeypatch, d, q, m, w):
    for k, v in NEW.items():
        monkeypatch.setattr(P, k, v)
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_admit_plants_full_ask_and_adds_hands(monkeypatch):
    off = _plan(_board(15, 4, money=20000))
    _relay(monkeypatch)
    fq = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "Q4_RELAY_ADMIT", True)
    on = _plan(_board(15, 4, money=20000))
    add = _plants(on)[spec.I_WHEAT] - _plants(off)[spec.I_WHEAT]
    assert add == 13                                  # the whole FQ first-day ask is admitted
    assert _plants(on)[1:] == _plants(off)[1:]        # the planner's own plantings are untouched
    assert _hires(on) >= _hires(off)
    assert _plants(on)[spec.I_WHEAT] >= _plants(fq)[spec.I_WHEAT]


def test_carrot_share(monkeypatch):
    off = _plan(_board(15, 4, money=20000))
    _relay(monkeypatch, Q4_RELAY_ADMIT=True, Q4_RELAY_CARROT=25)
    on = _plan(_board(15, 4, money=20000))
    add = [b - a for a, b in zip(_plants(off), _plants(on))]
    assert add[spec.I_CARROT] == 3 and add[spec.I_WHEAT] == 10


def test_dsm_density(monkeypatch):
    off = _plan(_board(15, 4, money=20000))
    _relay(monkeypatch, Q4_RELAY_ADMIT=True, Q4_RELAY_DENSITY="DSM")
    on = _plan(_board(15, 4, money=20000))
    assert _plants(on)[spec.I_WHEAT] - _plants(off)[spec.I_WHEAT] == 8


def test_mix_keeps_relay(monkeypatch):
    _relay(monkeypatch, Q4_RELAY_ADMIT=True)
    base = _plants(_plan(_board(15, 4, money=20000)))
    monkeypatch.setattr(P, "Q4_MIX", True)
    mix = _plants(_plan(_board(15, 4, money=20000)))
    assert mix[spec.I_WHEAT] >= base[spec.I_WHEAT] - 1


def test_spare_never_more_hands(monkeypatch):
    _relay(monkeypatch, Q4_RELAY_ADMIT=True)
    full = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "Q4_RELAY_SPARE", True)
    spare = _plan(_board(15, 4, money=20000))
    assert _hires(spare) <= _hires(full)
