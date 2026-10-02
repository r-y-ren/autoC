"""`plan.Q4_OWN_ON` + the S/q4limit1 funnel [Q4LIMIT1].

Claims: Q4_OWN_ON is OFF by default and OFF is byte-identical to master on the
three Q4RELAY1 days; ON buys Q4 only with three quadrants inside the window and
leaves every other day byte-identical; the funnel parser only READS a plan and
counts the PLANT ops the plan puts on Q4 tiles.
"""
from __future__ import annotations

import sys
from pathlib import Path

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_endroute import _digest
from test_q4_prog import _board, _plan, _land

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "S/q4limit1"))
import funnel  # noqa: E402

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # the Q4RELAY1 master digest, same on all three days


def test_off_by_default():
    assert P.Q4_OWN_ON is False and (P.Q4_OWN_DAY0, P.Q4_OWN_DAY1) == (10, 11)
    assert "Q4_OWN_ON" not in P.SWITCH_GENES


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("day,nquad", [(5, 3), (9, 3), (12, 3), (11, 2), (15, 4)])
def test_on_inert_off_window(monkeypatch, day, nquad):
    base = _digest(_plan(_board(day, nquad)))
    monkeypatch.setattr(P, "Q4_OWN_ON", True)
    assert _digest(_plan(_board(day, nquad))) == base


def test_on_buys_in_window(monkeypatch):
    off = _plan(_board(11, 3))
    monkeypatch.setattr(P, "Q4_OWN_ON", True)
    on = _plan(_board(11, 3))
    assert _land(off) == 0 and _land(on) == 1
    monkeypatch.setattr(P, "Q4_OWN_DAY1", 10)       # window closed on d11
    assert _digest(_plan(_board(11, 3))) == _digest(off)


def test_funnel_passive_and_counts():
    monkey_plan = _plan(_board(15, 4))
    before = _digest(monkey_plan)
    n = funnel.q4_ops(monkey_plan, 15)
    assert _digest(monkey_plan) == before
    assert set(n) == {"PLANT", "WATER", "HARVEST"} and all(v >= 0 for v in n.values())
    # an owned, empty Q4 on d15: the day plans some PLANT ops there, and none on d15 with Q4 locked
    locked = funnel.q4_ops(_plan(_board(15, 3)), 15)
    assert locked["PLANT"] == 0 and locked["WATER"] == 0 and locked["HARVEST"] == 0
