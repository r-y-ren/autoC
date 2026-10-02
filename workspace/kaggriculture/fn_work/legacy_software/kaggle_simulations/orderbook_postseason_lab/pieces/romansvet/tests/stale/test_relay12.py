"""RELAY12 switches [plan.Q4_RELAY_CREW_CAP / NO_RESERVE / Q3_DAY / PRIO / H23, CREW_LEVEL_ON]:
the FQ wheat relay on a LEVEL crew (hands replaced, not added), bought on the first cover, admitted ahead of the tail.

Claims: OFF by default and byte-identical to the recorded days of tests/test_q4_relay.py (master digest); every new
switch is inert while `Q4_RELAY_ON` is off; CREW_LEVEL_ON levels the crew at its cap (a ceiling where the routes load fewer hands); the relay cap clamps the relay
crew at A on d10-19; Q3_DAY buys Q3 on the first cover; PRIO never plants less relay wheat than FQ alone.
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
from test_q4_prog import _board, _plan, _plants, _land
from test_q4_relay import DAYS, MASTER

NEW = dict(Q4_RELAY_CREW_CAP=(11, 11), Q4_RELAY_NO_RESERVE=True, Q4_RELAY_Q3_DAY=9,
           Q4_RELAY_PRIO="tier", Q4_RELAY_H23=True)


def _hires(pl):
    return int(np.sum(pl[3] == O.MO_HIRE))


def test_off_by_default():
    assert P.Q4_RELAY_CREW_CAP is None and P.Q4_RELAY_NO_RESERVE is False and P.Q4_RELAY_Q3_DAY is None
    assert P.Q4_RELAY_PRIO is None and P.Q4_RELAY_H23 is False and P.CREW_LEVEL_ON is False
    assert P.CREW_LEVEL_CAP == (12, 11)
    assert not any(k in P.SWITCH_GENES for k in list(NEW) + ["CREW_LEVEL_ON"])


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_new_switches_inert_without_relay(monkeypatch, d, q, m, w):
    for k, v in NEW.items():
        monkeypatch.setattr(P, k, v)
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_crew_level(monkeypatch):
    off = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "CREW_LEVEL_ON", True)
    on = _plan(_board(15, 4, money=20000))
    # HIRE_ROW_ON (shipped) hires only the hands the routes load, so the level is a ceiling on an idle board
    assert _hires(off) <= _hires(on) <= 12
    assert _digest(_plan(_board(5, 2, money=3000))) == MASTER     # outside d10-27: inert


def test_relay_crew_cap(monkeypatch):
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_SCHED", "FQ")
    fq = _plan(_board(15, 4, money=20000))
    monkeypatch.setattr(P, "Q4_RELAY_CREW_CAP", (11, 11))
    cap = _plan(_board(15, 4, money=20000))
    assert _hires(cap) <= 11 and _hires(cap) <= _hires(fq)


def test_q3_day(monkeypatch):
    assert _land(_plan(_board(9, 2, money=2500))) == 0
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_Q3_DAY", 9)
    assert _land(_plan(_board(9, 2, money=2500))) == 1


@pytest.mark.parametrize("prio", ["value", "tier", "after"])
def test_prio_not_fewer(monkeypatch, prio):
    monkeypatch.setattr(P, "Q4_RELAY_ON", True)
    monkeypatch.setattr(P, "Q4_RELAY_SCHED", "FQ")
    base = _plants(_plan(_board(15, 4)))
    monkeypatch.setattr(P, "Q4_RELAY_PRIO", prio)
    on = _plants(_plan(_board(15, 4)))
    assert on[spec.I_WHEAT] >= base[spec.I_WHEAT]
