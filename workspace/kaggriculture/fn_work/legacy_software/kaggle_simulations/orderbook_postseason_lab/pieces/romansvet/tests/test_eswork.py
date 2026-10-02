"""ESWORK1 gene block [plan.ESWORK_THETA]: WORK levers for ES over a frozen theta7659 + head_940.

Claims: None by default and not a SWITCH_GENE; zeros reproduce the shipped plan byte for byte (master digest on the three
WHEATMIX1 days, and None == zeros on d22/d26 floor days); a nonzero relay gene yields relay wheat plantings that the
admission keeps (planned == routed, MR_LAST census) with the relay's seed, and moves no other crop; the late ask floor adds
wheat (d20-25) / carrot (d26-27) and is inert outside d20-27; the EST_LEAD gene is inert before d10; the Q4 buy band maps
never / d12-13 / d11 / d10.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_endroute import _digest
from test_q4_prog import _board, _plants, _seeds
from test_budget_order import _macro

# inlined from tests/stale/test_wheatmix.py (parked by SRCSYNC1)
DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master digest, same on all three days


def _plan(view, pt=(2, 1, 0, 0, 0)):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=np.array(pt, np.int32))))


@pytest.fixture(autouse=True)
def _none_default(monkeypatch):
    """SHIP_VRP10_ESW ships the g30 theta as the module default; this file probes the gene block from None."""
    monkeypatch.setattr(P, "ESWORK_THETA", None)


def _th(**kw):
    v = np.zeros(P.ESWORK_D, np.float32)
    for k, x in kw.items():
        v[int(k[1:])] = x
    return v


def test_off_by_default():
    assert "ESWORK_THETA" not in P.SWITCH_GENES and P.ESWORK_D == 10   # shipped default (g30 theta) = tests/test_ship_vrp10_esw.py


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_zeros_byte_identical(monkeypatch, d, q, m, w):
    monkeypatch.setattr(P, "ESWORK_THETA", _th())
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


@pytest.mark.parametrize("d", [22, 26])
def test_zeros_equal_none_late(monkeypatch, d):
    base = _digest(_plan(_board(d, 3)))
    monkeypatch.setattr(P, "ESWORK_THETA", _th())
    assert _digest(_plan(_board(d, 3))) == base


def test_relay_gene_admitted(monkeypatch):
    off = _plan(_board(12, 3))
    monkeypatch.setattr(P, "ESWORK_THETA", _th(g0=4.0))
    P.MR_LAST[:] = [0, 0, 0]
    on = _plan(_board(12, 3))
    add = [b - a for a, b in zip(_plants(off), _plants(on))]
    assert 1 <= add[spec.I_WHEAT] <= 4 and add[1:] == [0, 0, 0, 0]
    planned, routed, _ = P.MR_LAST
    assert planned == add[spec.I_WHEAT] and routed == planned          # admitted = planned
    assert _seeds(on)[spec.I_WHEAT] >= _seeds(off)[spec.I_WHEAT] + add[spec.I_WHEAT] - 8   # 8 = board's shed seed


def test_relay_gene_band_and_window(monkeypatch):
    base8, base18 = _digest(_plan(_board(8, 3))), _digest(_plan(_board(18, 3)))
    monkeypatch.setattr(P, "ESWORK_THETA", _th(g0=6.0))       # d10-14 band only
    assert _digest(_plan(_board(8, 3))) == base8 and _digest(_plan(_board(18, 3))) == base18


def test_ask_floor(monkeypatch):
    off22, off26, off15 = (_plan(_board(d, 3)) for d in (22, 26, 15))
    monkeypatch.setattr(P, "ESWORK_THETA", _th(g4=1.0))
    on22, on26 = _plan(_board(22, 3)), _plan(_board(26, 3))
    assert _plants(on22)[spec.I_WHEAT] > _plants(off22)[spec.I_WHEAT]
    assert _plants(on26)[spec.I_CARROT] > _plants(off26)[spec.I_CARROT]
    assert _plants(on26)[spec.I_WHEAT] == _plants(off26)[spec.I_WHEAT]
    assert _digest(_plan(_board(15, 3))) == _digest(off15)


def test_est_lead_inert_before_d10(monkeypatch):
    base = _digest(_plan(_board(5, 2, money=3000)))
    monkeypatch.setattr(P, "ESWORK_THETA", _th(g5=3.0))
    assert _digest(_plan(_board(5, 2, money=3000))) == base
    assert int(P._est_lead(np, 12)) == P.EST_LEAD - 3 and int(P._est_lead(np, 9)) == P.EST_LEAD
