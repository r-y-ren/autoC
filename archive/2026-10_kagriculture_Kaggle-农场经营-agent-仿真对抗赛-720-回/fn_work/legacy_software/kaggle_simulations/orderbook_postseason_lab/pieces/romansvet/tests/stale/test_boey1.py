"""BOEY1 switches [BOEY_NO_TOMATO_ON, BOEY_EARLY_WHEAT_DAYS, BOEY_Q2_DAY]: Boey's (rank 1-2) plant-mix and
Q2-day rules (docs/strategy/2026-09-26-boey1.md).

Claims: all OFF by default and byte-identical to selfplay1 cc94afdb on five days (digests computed from
`git archive cc94afdb`); NO_TOMATO moves the tomato target to wheat; EARLY_WHEAT moves carrot to wheat inside
its window only; Q2_DAY blocks the second quadrant before its day and nothing else.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board, _plants, _land

# (day, nquad, money, plant_target) -> digest of build_day on cc94afdb (pre-BOEY1 plan.py)
CASES = (((0, 1, 3000, (4, 3, 0, 0, 0)), "b882e29e5ac1ceea"), ((5, 1, 3000, (2, 1, 0, 0, 0)), "6443072e443be338"),
         ((6, 1, 3000, (2, 1, 0, 0, 0)), "6443072e443be338"), ((12, 3, 9000, (2, 1, 2, 0, 0)), "d80cc9b77e896890"),
         ((22, 3, 9000, (3, 2, 1, 0, 0)), "9aca36b8ed8d932f"))


def _plan(d, q, m, pt):
    return tuple(np.asarray(a) for a in P.build_day(np, _board(d, q, money=m), _macro(plant_target=np.array(pt, np.int32))))


def test_off_by_default():
    assert P.BOEY_NO_TOMATO_ON is False and P.BOEY_EARLY_WHEAT_DAYS is None and P.BOEY_Q2_DAY is None
    for s in ("BOEY_NO_TOMATO_ON", "BOEY_EARLY_WHEAT_DAYS", "BOEY_Q2_DAY"):
        assert s not in P.SWITCH_GENES


@pytest.mark.parametrize("case,dig", CASES)
def test_off_byte_identical(case, dig):
    assert _digest(_plan(*case)) == dig


def test_mix_helper(monkeypatch):
    m = _macro(plant_target=np.array((2, 3, 4, 0, 0), np.int32))
    monkeypatch.setattr(P, "BOEY_NO_TOMATO_ON", True)
    assert P._boey_mix(np, m, 12).plant_target.tolist() == [6, 3, 0, 0, 0]
    monkeypatch.setattr(P, "BOEY_NO_TOMATO_ON", False)
    monkeypatch.setattr(P, "BOEY_EARLY_WHEAT_DAYS", (0, 9))
    assert P._boey_mix(np, m, 3).plant_target.tolist() == [5, 0, 4, 0, 0]
    assert P._boey_mix(np, m, 10).plant_target.tolist() == [2, 3, 4, 0, 0]


def test_no_tomato_plans(monkeypatch):
    case = (12, 3, 9000, (2, 1, 2, 0, 0))
    off = _plants(_plan(*case))
    monkeypatch.setattr(P, "BOEY_NO_TOMATO_ON", True)
    on = _plants(_plan(*case))
    assert on[spec.I_TOMATO] == 0 and off[spec.I_TOMATO] > 0 and on[spec.I_WHEAT] >= off[spec.I_WHEAT]


def test_q2_day(monkeypatch):
    base5, base8 = _land(_plan(5, 1, 20000, (2, 1, 0, 0, 0))), _land(_plan(8, 1, 20000, (2, 1, 0, 0, 0)))
    monkeypatch.setattr(P, "BOEY_Q2_DAY", 6)
    assert _land(_plan(5, 1, 20000, (2, 1, 0, 0, 0))) == 0
    assert _land(_plan(8, 1, 20000, (2, 1, 0, 0, 0))) == base8
    assert base5 == 1 or base5 == 0
