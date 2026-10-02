"""PLANTASK1: funded Macro ask floor and optional fourth quadrant."""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_plant_fill_late import _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

PRE_SWITCH = "6a24864c"


PIN_BOARDS = (
    ("opening", dict(day=0, money=3_000, n_wh=0, nquad=1), {}),
    ("window", dict(day=14, money=22_000, n_wh=18, shed_wh=11, nquad=3),
     dict(crew_target=11)),
    ("late", dict(day=24, money=60_000, n_wh=28, shed_wh=40, shops=2, nquad=4),
     dict(crew_target=15, hire_bias=np.int32(-120))),
)


def _plan(view, macro):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro))


def _own_digests():
    return {name: _pin.digest(_plan(_view(**v), _macro(**m)))
            for name, v, m in PIN_BOARDS}


def test_off_defaults_and_byte_identity():
    assert P.PLANT_ASK_ON is False
    assert P.PLANT_ASK_FRAC == 0.5
    assert P.PLANT_ASK_DAYS == (10, 19)
    assert P.PLANT_ASK_QUAD is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=PRE_SWITCH)


def _ask_inputs(purse=10_000):
    values = np.zeros((P.BUD.N_LISTS, P.PJ.K), np.int32)
    costs = np.ones_like(values)
    values[P.BUD.L_SEED0 + spec.I_WHEAT] = 20
    values[P.BUD.L_SEED0 + spec.I_CARROT] = 80
    costs[P.BUD.L_SEED0:P.BUD.L_SEED0 + spec.N_CROPS] = \
        np.asarray(spec.CROP_SEED_COST)[:, None]
    return values, costs, np.int32(purse)


def test_ask_raises_total_and_uses_margin_rank(monkeypatch):
    monkeypatch.setattr(P, "PLANT_ASK_ON", True)
    monkeypatch.setattr(P, "PLANT_ASK_FRAC", 0.5)
    view = _view(day=12, money=20_000, nquad=3)
    target = np.zeros(spec.N_CROPS, np.int32)
    target[spec.I_WHEAT] = 2
    values, costs, purse = _ask_inputs()
    got = P._plant_ask(np, view, _macro(plant_target=target),
                       np.int32(20), values, costs, purse)
    assert int(got.plant_target.sum()) == 10
    assert int(got.plant_target[spec.I_CARROT]) == 8
    assert int(got.plant_target[spec.I_WHEAT]) == 2


def test_ask_is_seed_funded_and_windowed(monkeypatch):
    monkeypatch.setattr(P, "PLANT_ASK_ON", True)
    monkeypatch.setattr(P, "PLANT_ASK_FRAC", 1.0)
    values, costs, _ = _ask_inputs()
    target = np.zeros(spec.N_CROPS, np.int32)
    target[spec.I_WHEAT] = 1
    macro = _macro(plant_target=target)
    # CARROT is the ranked crop and costs 20 per seed: 60 coins fund 3 extras.
    live = P._plant_ask(np, _view(day=12), macro, np.int32(20),
                        values, costs, np.int32(60))
    assert int(live.plant_target.sum()) == 4
    before = P._plant_ask(np, _view(day=9), macro, np.int32(20),
                          values, costs, np.int32(10_000))
    assert np.array_equal(before.plant_target, target)


def test_quad_override_keeps_reach_and_cash_gates(monkeypatch):
    monkeypatch.setattr(P, "PLANT_ASK_ON", True)
    monkeypatch.setattr(P, "PLANT_ASK_QUAD", True)
    monkeypatch.setattr(P, "land_reach", lambda xp, n, w: xp.asarray(P.LAND_TILES, xp.int32))
    monkeypatch.setattr(P.BUD, "marginal_gain", lambda *a, **k: np.int32(0))
    target = np.zeros(spec.N_CROPS, np.int32)
    target[spec.I_WHEAT] = 1
    rich = _plan(_view(day=14, money=20_000, nquad=3),
                 _macro(plant_target=target, land_bias=np.int32(-1_000_000)))
    assert int((rich[3] == O.MO_BUY_LAND).sum()) == 1
    poor = _plan(_view(day=14, money=4_000, nquad=3),
                 _macro(plant_target=target, land_bias=np.int32(-1_000_000)))
    assert int((poor[3] == O.MO_BUY_LAND).sum()) == 0


if __name__ == "__main__":
    for _name, _digest in _own_digests().items():
        print(_name, _digest)
