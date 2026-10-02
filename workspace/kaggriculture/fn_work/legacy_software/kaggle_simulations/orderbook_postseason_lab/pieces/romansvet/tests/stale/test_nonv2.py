"""NONV2: arms gated on the rival class at the d1 dawn (ENGINE_GATE_DAY=1, rival melon tiles <= 10 = non-V).

Claims: the two new knobs are OFF by default (NONV_PLATE_LAST None, NONV_Q2_DAYS None) and OFF is byte-identical;
NONV_PLATE_LAST widens the MELONGENES plate rewrite from one day to a window and touches no day outside it;
NONV_Q2_DAYS buys Q2 inside its window only; the gate-set parser writes and restores both; the d1 latch is the
runtime's own (`day < ENGINE_GATE_DAY` resets, the first dawn at/after it decides once).
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import ops as O
from kagg3.core import plan as P

from test_endroute import _view, _digest
from test_budget_order import _macro
from test_engine_gate import _obs

MIX = np.array([4, 0, 0, 4, 0], np.int32)     # wheat 4 + strawberry 4 wanted today


def _plan(macro=None, **b):
    return tuple(np.asarray(a) for a in P.build_day(np, _view(**b), macro or _macro()._replace(plant_target=MIX)))


def _dig(**b):
    return _digest(_plan(**b))


def test_off_by_default():
    assert P.NONV_PLATE_LAST is None and P.NONV_Q2_DAYS is None
    assert P.MELON_PLATE_TILES == 0.0 and P.ENGINE_GATE_ON is False and P.ENGINE_GATE_SET == ""


def test_plate_window():
    b5, b12 = dict(day=5, n_wh=4, money=5000), dict(day=12, n_wh=4, money=5000)
    off5, off12 = _dig(**b5), _dig(**b12)
    try:
        P.MELON_PLATE_TILES, P.MELON_PLATE_DAY = 8, 1
        assert _dig(**b5) == off5                 # MELONGENES: the plate is d1 only -> d5 untouched
        P.NONV_PLATE_LAST = 6
        on5 = _plan(**b5)
        assert _digest(on5) != off5               # the window d1-6 moves d5's mix onto melon
        assert _dig(**b12) == off12               # d12 is outside the window
    finally:
        P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST = 0.0, 0.0, None
    assert _dig(**b5) == off5


def test_q2_window():
    b3, b8 = dict(day=3, n_wh=4, money=1100, nquad=1), dict(day=8, n_wh=4, money=1100, nquad=1)
    off3, off8 = _plan(**b3), _dig(**b8)
    try:
        P.NONV_Q2_DAYS = (2, 5)
        on3 = _plan(**b3)
        assert (on3[3] == O.MO_BUY_LAND).any()   # d3: the quadrant is bought inside the window
        assert _dig(**b8) == off8                 # d8: outside the window, the OFF plan
    finally:
        P.NONV_Q2_DAYS = None
    assert _digest(_plan(**b3)) == _digest(off3)


def test_gate_set_apply_restore():
    old = (P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST, P.NONV_Q2_DAYS, P.NONV_EARLY_HANDS, P.NONV_EARLY_DAYS)
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = ("MELON_PLATE_TILES=20;MELON_PLATE_DAY=1;NONV_PLATE_LAST=6;NONV_Q2_DAYS=2:5;"
                         "NONV_EARLY_HANDS=2;NONV_EARLY_DAYS=1:9")
    try:
        P.engine_gate_apply(True)
        assert (P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST, P.NONV_Q2_DAYS,
                P.NONV_EARLY_HANDS, P.NONV_EARLY_DAYS) == (20, 1, 6, (2, 5), 2, (1, 9))
        P.engine_gate_apply(False)
        assert (P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST, P.NONV_Q2_DAYS,
                P.NONV_EARLY_HANDS, P.NONV_EARLY_DAYS) == old
    finally:
        P._ENGINE_GATE_BASE = None
        P.ENGINE_GATE_SET = ""


def test_d1_classifier():
    # The V opening holds 12 melon at the d1 dawn (V56 dev 100/100, live V 0 fires); non-V tapes 0-7.
    old = P.ENGINE_GATE_MELON_MIN
    try:
        P.ENGINE_GATE_MELON_MIN = 0
        assert P.engine_gate_fires(_obs(1, 0), 0) and P.engine_gate_fires(_obs(1, 7), 0)
        assert not P.engine_gate_fires(_obs(1, 12), 0) and not P.engine_gate_fires(_obs(1, 11), 0)
    finally:
        P.ENGINE_GATE_MELON_MIN = old


def _obs_plants(day, melon, wheat, player=0):
    o = _obs(day, melon, player)
    o["farms"][1 - player]["tiles"][0] += [{"kind": "PLANT", "crop": "WHEAT"} for _ in range(wheat)]
    return o


def test_min_plants():
    # [NONV2] 3/61 V-opening bank agents reach the d1 dawn with 0 tiles and 3,000 coins: MIN_PLANTS=1 keeps them unlatched.
    old = (P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MIN_PLANTS)
    try:
        P.ENGINE_GATE_MELON_MIN = 0
        assert P.ENGINE_GATE_MIN_PLANTS == 0 and P.engine_gate_fires(_obs_plants(1, 0, 0), 0)   # OFF: melon-only test
        P.ENGINE_GATE_MIN_PLANTS = 1
        assert not P.engine_gate_fires(_obs_plants(1, 0, 0), 0)            # empty farm: undecided
        assert P.engine_gate_fires(_obs_plants(1, 0, 19), 0)               # 0m/19w (Lucas Boesen)
        assert P.engine_gate_fires(_obs_plants(1, 6, 8), 0)                # 6m/8w (10m/8w/$1 recipe at d1)
        assert not P.engine_gate_fires(_obs_plants(1, 12, 8), 0)           # V56 d1: 12m/8w
    finally:
        P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MIN_PLANTS = old
