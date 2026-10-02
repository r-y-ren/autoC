"""Q4DIG1 switches [plan.Q4_HERD_FIRST / Q4_HERD_DAYS, Q4_RELAY_BELOW_CARE, Q4_RELAY_E_CAP]: the land waits for the
herd budget, the relay is admitted below every herd task, and the relay's hands are capped at max(planner's crew, cap).

Claims: OFF by default and byte-identical to the recorded master days (tests/test_q4_relay.py digest); BELOW_CARE and
E_CAP are inert while `Q4_RELAY_ON` is off; HERD_FIRST with a zero herd horizon is the relay as it was, and a herd want
the purse cannot cover blocks the Q4 buy; BELOW_CARE with ample labour keeps the full relay ask; E_CAP never hires
fewer hands than the planner alone and a huge cap is the uncapped relay.
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
from test_q4_prog import _board, _plan, _plants, _land, PT
from test_q4_relay import DAYS, MASTER


def _hires(pl):
    return int(np.sum(pl[3] == O.MO_HIRE))


def _relay(monkeypatch, **kw):
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_SCHED", "FQ")
    for k, v in kw.items():
        monkeypatch.setattr(P, k, v)


def _plan_m(view, **kw):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=PT, **kw)))


def test_off_by_default():
    assert P.Q4_HERD_FIRST is False and P.Q4_HERD_DAYS == 3
    assert P.Q4_RELAY_BELOW_CARE is False and P.Q4_RELAY_E_CAP is None
    assert not any(k in P.SWITCH_GENES for k in ("Q4_HERD_FIRST", "Q4_RELAY_BELOW_CARE", "Q4_RELAY_E_CAP"))


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_relay_switches_inert_without_relay(monkeypatch, d, q, m, w):
    monkeypatch.setattr(P, "Q4_RELAY_BELOW_CARE", True)
    monkeypatch.setattr(P, "Q4_RELAY_E_CAP", 12)
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_herd_first_zero_horizon_is_relay(monkeypatch):
    _relay(monkeypatch)
    ref = _plan(_board(12, 3))
    monkeypatch.setattr(P, "Q4_HERD_FIRST", True)
    monkeypatch.setattr(P, "Q4_HERD_DAYS", 0)
    on = _plan(_board(12, 3))
    assert _land(ref) == 1 and _digest(on) == _digest(ref)


def test_herd_first_blocks_uncovered_buy(monkeypatch):
    _relay(monkeypatch)
    want = np.array([0, 3, 0], np.int32)
    ref = _plan_m(_board(12, 3), animal_want=want)
    monkeypatch.setattr(P, "Q4_HERD_FIRST", True)
    monkeypatch.setattr(P, "Q4_HERD_DAYS", 1000)          # a herd need no purse covers
    on = _plan_m(_board(12, 3), animal_want=want)
    assert _land(ref) == 1 and _land(on) == 0


@pytest.mark.parametrize("mode", [True, "own"])
def test_below_care_keeps_full_ask(monkeypatch, mode):
    off = _plan(_board(15, 4, money=20000))
    _relay(monkeypatch, Q4_RELAY_ADMIT=True, Q4_RELAY_BELOW_CARE=mode)
    on = _plan(_board(15, 4, money=20000))
    assert _plants(on)[spec.I_WHEAT] - _plants(off)[spec.I_WHEAT] == 13
    assert _plants(on)[1:] == _plants(off)[1:]


def test_e_cap(monkeypatch):
    _relay(monkeypatch, Q4_RELAY_ADMIT=True)
    free = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "Q4_RELAY_E_CAP", 99)
    assert _digest(_plan(_board(15, 4, money=20000))) == _digest(free)
    monkeypatch.setattr(P, "Q4_RELAY_E_CAP", 0)          # no relay hands at all: the planner's own crew
    cap0 = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "Q4_RELAY_ON", False)
    own = _plan(_board(15, 4, money=20000))
    assert _hires(own) <= _hires(cap0) <= _hires(free)
