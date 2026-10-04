"""`plan.ENGINE_PLATE_ADD` [ENGPLATE1]: an ADDITIVE melon plate for the
ENGINE-gated game.

Claims: OFF by default (0, day 4); inert unless `ENGINE_GATE_ON` (the value is
written only through `ENGINE_GATE_SET`, i.e. after the d2 latch); inert on any
day but `ENGINE_PLATE_DAY`; ON it adds exactly N MELON plantings and N MELON
seeds and leaves every other crop's plantings and seed buys unchanged.
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

PT = np.array([3, 2, 0, 0, 1], np.int32)


def _plan(day=4):
    return tuple(np.asarray(a) for a in P.build_day(
        np, _view(day=day, n_wh=8, money=8000, shops=2), _macro(plant_target=PT)))


def _plants(pl):
    m = pl[0] == O.OP_PLANT
    return np.bincount(pl[1][m], minlength=spec.N_CROPS).tolist()


def _seeds(pl):
    op, a, q = pl[3:6]
    m = op == O.MO_BUY_SEED
    return np.bincount(a[m], weights=q[m], minlength=spec.N_CROPS).astype(int).tolist()


def test_off_by_default():
    assert P.ENGINE_PLATE_ADD == 0 and P.ENGINE_PLATE_DAY == 4


@pytest.mark.parametrize("gate,add,day", [(True, 0, 4), (False, 8, 4), (True, 8, 5)])
def test_inert_legs_are_byte_identical(monkeypatch, gate, add, day):
    base = [_digest(_plan(d)) for d in (4, 5, 12)]
    monkeypatch.setattr(P, "ENGINE_GATE_ON", gate)
    monkeypatch.setattr(P, "ENGINE_PLATE_ADD", add)
    monkeypatch.setattr(P, "ENGINE_PLATE_DAY", day)
    got = [_digest(_plan(d)) for d in (4, 5, 12)]
    if add and gate:     # only the plate day moves
        assert got[0] == base[0] and got[2] == base[2] and got[1] != base[1]
    else:
        assert got == base


@pytest.mark.parametrize("n", [4, 8])
def test_additive(monkeypatch, n):
    off = _plan()
    monkeypatch.setattr(P, "ENGINE_GATE_ON", True)
    monkeypatch.setattr(P, "ENGINE_PLATE_ADD", n)
    on = _plan()
    po, pn, so, sn = _plants(off), _plants(on), _seeds(off), _seeds(on)
    mel = spec.I_MELON
    assert pn[mel] == po[mel] + n and sn[mel] == so[mel] + n
    assert [x for i, x in enumerate(pn) if i != mel] == [x for i, x in enumerate(po) if i != mel]
    assert [x for i, x in enumerate(sn) if i != mel] == [x for i, x in enumerate(so) if i != mel]
