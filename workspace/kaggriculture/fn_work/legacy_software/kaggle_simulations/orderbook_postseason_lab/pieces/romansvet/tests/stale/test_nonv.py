"""NONV1: arms gated on the rival class (ENGINE_GATE latch at d2, `rival melon tiles <= 10` = non-V).

Claims: every new knob is OFF by default (NONV_EARLY_HANDS 0, ENGINE_PLATE_LAST None) and OFF is byte-identical;
the gate-set parser now takes `a:b` tuples (Q3_EARLY_DAYS=9:9) and restores them exactly; NONV_EARLY_HANDS moves
the plan only inside NONV_EARLY_DAYS; ENGINE_PLATE_LAST widens the ENGPLATE1 plate to a window; the MIN=0 classifier
fires on 0-10 rival melon tiles and never on the V opening's 12.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P

from test_endroute import _macro, _view, _digest
from test_engine_gate import _obs


def _dig(**b):
    return _digest(tuple(np.asarray(a) for a in P.build_day(np, _view(**b), _macro())))


def _reset(set_=""):
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = set_


def test_off_by_default():
    assert P.NONV_EARLY_HANDS == 0 and P.NONV_EARLY_DAYS == (2, 9)
    assert P.ENGINE_PLATE_LAST is None and P.ENGINE_PLATE_ADD == 0
    assert P.ENGINE_GATE_ON is False and P.ENGINE_GATE_SET == ""


def test_classifier_min0():
    old = P.ENGINE_GATE_MELON_MIN
    try:
        P.ENGINE_GATE_MELON_MIN = 0
        assert P.engine_gate_fires(_obs(2, 0), 0) and P.engine_gate_fires(_obs(2, 10), 0)
        assert not P.engine_gate_fires(_obs(2, 12), 0) and not P.engine_gate_fires(_obs(2, 11), 0)
    finally:
        P.ENGINE_GATE_MELON_MIN = old


def test_tuple_parse_apply_restore():
    boards = [dict(day=5, n_wh=4), dict(day=12, n_wh=8, shed_wh=20, shops=2)]
    base = [_dig(**b) for b in boards]
    old = (P.Q3_EARLY_ON, P.Q3_EARLY_DAYS, P.NONV_EARLY_HANDS, P.ENGINE_PLATE_LAST)
    _reset("Q3_EARLY_ON=True;Q3_EARLY_DAYS=9:9;NONV_EARLY_HANDS=2;ENGINE_PLATE_LAST=8")
    try:
        P.engine_gate_apply(True)
        assert (P.Q3_EARLY_ON, P.Q3_EARLY_DAYS, P.NONV_EARLY_HANDS, P.ENGINE_PLATE_LAST) == (True, (9, 9), 2, 8)
        P.engine_gate_apply(False)
        assert (P.Q3_EARLY_ON, P.Q3_EARLY_DAYS, P.NONV_EARLY_HANDS, P.ENGINE_PLATE_LAST) == old
        assert [_dig(**b) for b in boards] == base
    finally:
        _reset("")


def test_early_hands_window_only():
    # The raw crew count (HIRE_ROW off, so the HIRE row is n_hire): +k moves the plan inside d2-9 only.
    b_in, b_out = dict(day=5, n_wh=4), dict(day=12, n_wh=8, shed_wh=20, shops=2)
    keep = P.HIRE_ROW_ON
    try:
        P.HIRE_ROW_ON = False
        base_in, base_out = _dig(**b_in), _dig(**b_out)
        P.NONV_EARLY_HANDS = 2
        assert _dig(**b_out) == base_out          # d12 is outside d2-9: untouched
        assert _dig(**b_in) != base_in            # d5: the crew count grows
        P.NONV_EARLY_HANDS = 0
        assert _dig(**b_in) == base_in
    finally:
        P.NONV_EARLY_HANDS, P.HIRE_ROW_ON = 0, keep


def test_early_hands_trimmed_by_hire_row():
    # [NONV1 finding] Shipped HIRE_ROW hires only hands `_routes` loaded: on a board whose work the
    # crew already covers, +3 hands leave the whole day plan byte-identical (live: hands d2-9 3.72 -> 3.78).
    b = dict(day=5, n_wh=20, age=2)
    base = _dig(**b)
    try:
        P.NONV_EARLY_HANDS = 3
        assert P.HIRE_ROW_ON is True and _dig(**b) == base
    finally:
        P.NONV_EARLY_HANDS = 0


def test_plate_window():
    b5 = dict(day=5, n_wh=4)
    try:
        P.ENGINE_GATE_ON = True
        P.ENGINE_PLATE_ADD, P.ENGINE_PLATE_DAY = 4, 3
        single = _dig(**b5)                       # ENGPLATE1: plate on d3 only -> d5 untouched
        P.ENGINE_PLATE_LAST = 8
        assert _dig(**b5) != single               # window d3-8 plants on d5 too
        assert _dig(day=12, n_wh=8, shed_wh=20, shops=2) == _dig_off(day=12, n_wh=8, shed_wh=20, shops=2)
    finally:
        P.ENGINE_GATE_ON, P.ENGINE_PLATE_ADD, P.ENGINE_PLATE_DAY, P.ENGINE_PLATE_LAST = False, 0, 4, None


def _dig_off(**b):
    keep = (P.ENGINE_GATE_ON, P.ENGINE_PLATE_ADD, P.ENGINE_PLATE_LAST)
    P.ENGINE_GATE_ON, P.ENGINE_PLATE_ADD, P.ENGINE_PLATE_LAST = False, 0, None
    try:
        return _dig(**b)
    finally:
        P.ENGINE_GATE_ON, P.ENGINE_PLATE_ADD, P.ENGINE_PLATE_LAST = keep
