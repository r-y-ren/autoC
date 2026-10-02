"""`plan.Q4_RELAY_ON` [Q4RELAY1]: fixed low-labour Q4 wheat relay, gated at dawn
by the marginal Fibonacci hire price.

Claims: OFF by default and byte-identical to master 12ba21ac on three days
(d5 / d12 buy window / d15 owned Q4); ON buys Q4 in the window without moving
the planner's own plantings; on an owned Q4 the gated relay adds wheat and its
seeds; a prohibitive ROI makes ON inert.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_endroute import _digest
from test_q4_prog import _board, _plan, _plants, _seeds, _land

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master 12ba21ac digest, same on all three days


def test_off_by_default():
    assert P.Q4_RELAY_ON is False and P.Q4_RELAY_SCHED is None and P.Q4_RELAY_WATER == "min" and P.Q4_RELAY_FERT is False
    assert "Q4_RELAY_ON" not in P.SWITCH_GENES


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_buy_keeps_planner(monkeypatch):
    off = _plan(_board(12, 3))
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    on = _plan(_board(12, 3))
    assert _land(off) == 0 and _land(on) == 1
    assert _plants(on) == _plants(off) and _seeds(on) == _seeds(off)


def test_relay_on_owned_q4(monkeypatch):
    off = _plan(_board(15, 4, q4_wheat=5))
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    on = _plan(_board(15, 4, q4_wheat=5))
    add = [b - a for a, b in zip(_plants(off), _plants(on))]
    assert add[spec.I_WHEAT] > 0 and add[1:] == [0, 0, 0, 0]
    assert _seeds(on)[spec.I_WHEAT] >= _seeds(off)[spec.I_WHEAT] + add[spec.I_WHEAT]


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_prohibitive_roi_inert(monkeypatch, d, q, m, w):
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_ROI", 100.0)
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_fq_schedule(monkeypatch):
    off = _plan(_board(15, 4))
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_SCHED", "FQ")
    on = _plan(_board(15, 4))
    assert _plants(on)[spec.I_WHEAT] - _plants(off)[spec.I_WHEAT] == 13
