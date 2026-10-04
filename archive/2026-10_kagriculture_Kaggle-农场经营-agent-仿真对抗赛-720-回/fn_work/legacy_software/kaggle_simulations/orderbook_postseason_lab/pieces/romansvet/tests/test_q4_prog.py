"""`plan.Q4_PROG_ON` [Q4PROG1]: DSM's fourth-quadrant program.

Claims: OFF by default; ON is inert off the Q4 window (byte-identical plans);
ON buys Q4 in the window when the purse covers it and adds the Q4 target
census (d10: 4 wheat + 1 carrot) to the day's plantings with their seeds,
leaving every other crop's plantings unchanged; on an owned Q4 the deficit
against what Q4 already carries is planted (relay).
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
from test_endroute import _view, _digest

PT = np.array([2, 1, 0, 0, 0], np.int32)
Q4 = np.asarray(P.SERP_QUAD) == int(spec.LAND_ORDER[2])


def _board(day, nquad, money=9000, q4_wheat=0):
    v = _view(day=day, n_wh=8, money=money, shops=2, nquad=nquad)
    owned = [0] + [int(q) for q in spec.LAND_ORDER[:nquad - 1]]
    kind = v.kind.copy(); occ = v.occ.copy(); t_day = v.t_day.copy()
    kind[~np.isin(np.asarray(P.SERP_QUAD), owned)] = spec.KIND_LOCKED
    idx = np.flatnonzero(Q4 & (kind == spec.KIND_EMPTY))[:q4_wheat]
    kind[idx] = spec.KIND_PLANT; occ[idx] = spec.I_WHEAT; t_day[idx] = day - 1
    return v._replace(kind=kind, occ=occ, t_day=t_day)


def _plan(view):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=PT)))


def _plants(pl, mask=None):
    m = pl[0] == O.OP_PLANT
    return np.bincount(pl[1][m], minlength=spec.N_CROPS).tolist()


def _seeds(pl):
    op, a, q = pl[3:6]
    m = op == O.MO_BUY_SEED
    return np.bincount(a[m], weights=q[m], minlength=spec.N_CROPS).astype(int).tolist()


def _land(pl):
    return int(np.sum(pl[3] == O.MO_BUY_LAND))


def test_off_by_default():
    assert P.Q4_PROG_ON is False and P.Q4_BUY_DAYS == (10, 15)


@pytest.mark.parametrize("day,nquad", [(5, 3), (9, 3), (28, 4), (12, 2), (10, 2)])
def test_inert_off_window(monkeypatch, day, nquad):
    base = _digest(_plan(_board(day, nquad)))
    monkeypatch.setattr(P, "Q4_PROG_ON", True)
    assert _digest(_plan(_board(day, nquad))) == base


def test_buys_and_plants_d10(monkeypatch):
    off = _plan(_board(10, 3))
    monkeypatch.setattr(P, "Q4_PROG_ON", True)
    on = _plan(_board(10, 3))
    assert _land(off) == 0 and _land(on) == 1
    po, pn, so, sn = _plants(off), _plants(on), _seeds(off), _seeds(on)
    # seeds exactly; the prospective tiles are workable only after the land
    # turn, so the route may admit one planting fewer than it bought for.
    assert sn[spec.I_WHEAT] == so[spec.I_WHEAT] + 4
    assert sn[spec.I_CARROT] == so[spec.I_CARROT] + 1
    assert pn[spec.I_WHEAT] >= po[spec.I_WHEAT] + 3
    assert pn[spec.I_CARROT] == po[spec.I_CARROT] + 1


def test_no_buy_without_purse(monkeypatch):
    monkeypatch.setattr(P, "Q4_PROG_ON", True)
    assert _land(_plan(_board(10, 3, money=1500))) == 0


def test_relay_on_owned_q4(monkeypatch):
    off = _plan(_board(15, 4, q4_wheat=5))
    monkeypatch.setattr(P, "Q4_PROG_ON", True)
    on = _plan(_board(15, 4, q4_wheat=5))
    po, pn = _plants(off), _plants(on)
    add = [b - a for a, b in zip(po, pn)]
    assert add == [3, 3, 3, 3, 0]
