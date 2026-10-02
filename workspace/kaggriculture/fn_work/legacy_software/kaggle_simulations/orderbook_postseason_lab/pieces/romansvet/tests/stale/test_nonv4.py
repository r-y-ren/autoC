"""NONV4: gated arms vs non-V melon openers (d2 tell, ENGINE_GATE_MELON_MIN=1, MAX=10).

Claims: the new knobs are OFF by default (NONV_WOOL_CARE False, NONV_MELON_SKIP None) and OFF is byte-identical;
`_herd_add_days` keeps HERDVRP1's one-head-per-step days for N <= window and repeats a day per head for N > window;
NONV_MELON_SKIP moves the melon target to NONV_MELON_TO inside its window only; the gate-set parser writes and restores
every NONV4 knob; the d2 classifier fires on 1-10 rival melon and never on the V opening (11-12) or an empty rival.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P

from test_endroute import _view, _digest
from test_budget_order import _macro
from test_engine_gate import _obs

MIX = np.array([4, 0, 0, 0, 4], np.int32)     # wheat 4 + melon 4 wanted today


def _dig(**b):
    return _digest(tuple(np.asarray(a) for a in P.build_day(np, _view(**b), _macro()._replace(plant_target=MIX))))


def test_off_by_default():
    assert P.NONV_WOOL_CARE is False and P.NONV_MELON_SKIP is None and P.NONV_MELON_TO == "TOMATO"
    assert P.HERD_ADD_COW == 0 and P.HERD_ADD_SHEEP == 0 and P.HERD_ADD_DAYS == (6, 12)


def test_herd_add_days_multiplicity():
    old = P.HERD_ADD_DAYS
    try:
        assert P._herd_add_days(2) == [6, 9] and P._herd_add_days(4) == [6, 7, 9, 11]   # HERDVRP1 unchanged
        P.HERD_ADD_DAYS = (2, 5)
        assert P._herd_add_days(2) == [2, 4] and P._herd_add_days(4) == [2, 3, 4, 5]
        assert P._herd_add_days(6) == [2, 2, 3, 4, 4, 5]                                # 6 head over 4 days
    finally:
        P.HERD_ADD_DAYS = old


def test_melon_skip_window_and_wool_care_off_parity():
    b5, b12 = dict(day=5, n_wh=4, money=5000), dict(day=12, n_wh=4, money=5000)
    off5, off12 = _dig(**b5), _dig(**b12)
    try:
        P.NONV_MELON_SKIP = (10, 19)
        assert _dig(**b5) == off5                 # outside the window: the OFF plan
        assert _dig(**b12) != off12               # d12: melon moved onto tomato
        P.NONV_MELON_SKIP = None
        P.NONV_WOOL_CARE = True
        assert _dig(**b5) == off5                 # no sheep on the view: the care rule has nothing to move
    finally:
        P.NONV_MELON_SKIP, P.NONV_WOOL_CARE = None, False
    assert _dig(**b5) == off5 and _dig(**b12) == off12


def test_gate_set_apply_restore():
    names = ("HERD_ADD_SHEEP", "HERD_ADD_DAYS", "NONV_WOOL_CARE", "NONV_MELON_SKIP", "NONV_MELON_TO")
    old = tuple(getattr(P, n) for n in names)
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = "HERD_ADD_SHEEP=4;HERD_ADD_DAYS=2:5;NONV_WOOL_CARE=True;NONV_MELON_SKIP=10:19;NONV_MELON_TO=WHEAT"
    try:
        P.engine_gate_apply(True)
        assert tuple(getattr(P, n) for n in names) == (4, (2, 5), True, (10, 19), "WHEAT")
        P.engine_gate_apply(False)
        assert tuple(getattr(P, n) for n in names) == old
    finally:
        P._ENGINE_GATE_BASE = None
        P.ENGINE_GATE_SET = ""


def test_d2_classifier():
    old = (P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX)
    try:
        P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX = 1, 10
        assert all(P.engine_gate_fires(_obs(2, m), 0) for m in (1, 5, 7, 10))
        assert not any(P.engine_gate_fires(_obs(2, m), 0) for m in (0, 11, 12))
    finally:
        P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX = old
