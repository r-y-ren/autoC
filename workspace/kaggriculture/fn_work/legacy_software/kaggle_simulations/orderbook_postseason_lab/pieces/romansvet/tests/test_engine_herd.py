"""`plan.ENGINE_HERD_DEFER` [ENGHERD1]: a gated herd-purchase defer.

Claims: OFF by default (0, from day 2); inert unless `ENGINE_GATE_ON` (written
only through `ENGINE_GATE_SET`); inside the window d FROM..FROM+K the day buys
no animal and every seed buy is kept or grows (freed coin); outside the window
the day is byte-identical to OFF.
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
AW = np.array([2, 2, 2], np.int32)


def _plan(day=4, money=2500):
    return tuple(np.asarray(a) for a in P.build_day(
        np, _view(day=day, n_wh=8, money=money, shops=2), _macro(plant_target=PT, animal_want=AW)))


def _buys(pl, mo, n):
    op, a, q = pl[3:6]
    m = op == mo
    return np.bincount(a[m], weights=q[m], minlength=n).astype(int).tolist()


def test_off_by_default():
    assert P.ENGINE_HERD_DEFER == 0 and P.ENGINE_HERD_FROM == 2


def test_fixture_buys_animals():
    assert sum(_buys(_plan(), O.MO_BUY_ANIMAL, spec.N_ANIMALS)) > 0


@pytest.mark.parametrize("gate,k", [(True, 0), (False, 5)])
def test_inert_legs_are_byte_identical(monkeypatch, gate, k):
    base = [_digest(_plan(d)) for d in (3, 8, 12)]
    monkeypatch.setattr(P, "ENGINE_GATE_ON", gate)
    monkeypatch.setattr(P, "ENGINE_HERD_DEFER", k)
    assert [_digest(_plan(d)) for d in (3, 8, 12)] == base


@pytest.mark.parametrize("k", [3, 5])
def test_window(monkeypatch, k):
    base = {d: _plan(d) for d in (4, 2 + k, 3 + k)}
    monkeypatch.setattr(P, "ENGINE_GATE_ON", True)
    monkeypatch.setattr(P, "ENGINE_HERD_DEFER", k)
    for d in (4, 2 + k):
        on = _plan(d)
        assert sum(_buys(on, O.MO_BUY_ANIMAL, spec.N_ANIMALS)) == 0
        so, sn = _buys(base[d], O.MO_BUY_SEED, spec.N_CROPS), _buys(on, O.MO_BUY_SEED, spec.N_CROPS)
        assert all(b >= a for a, b in zip(so, sn))
    assert _digest(_plan(3 + k)) == _digest(base[3 + k])     # resumes after the window


def test_freed_coin_funds_only_the_plate(monkeypatch):
    """money 1600: the plate alone funds 0 extra melon (purse spent on the herd);
    with the defer the held animal coin buys the plate; other seeds unchanged."""
    monkeypatch.setattr(P, "ENGINE_GATE_ON", True)
    monkeypatch.setattr(P, "ENGINE_PLATE_ADD", 8)
    plate = _plan(4, 1600)
    monkeypatch.setattr(P, "ENGINE_HERD_DEFER", 3)
    both = _plan(4, 1600)
    sp, sb = _buys(plate, O.MO_BUY_SEED, spec.N_CROPS), _buys(both, O.MO_BUY_SEED, spec.N_CROPS)
    mel = spec.I_MELON
    assert sb[mel] >= sp[mel] + 4
    assert [x for i, x in enumerate(sb) if i != mel] == [x for i, x in enumerate(sp) if i != mel]
    assert sum(_buys(both, O.MO_BUY_ANIMAL, spec.N_ANIMALS)) == 0
