"""SHIP_VRP7 (res940_vrp7) = res940_vrp6 + the NONV2 "M20z" arm [NONV2/NONV3/SHIPNV1]: the ENGINE_GATE latch at the d1 dawn
on a rival with 0 MELON and >= 1 planting, then the MELONGENES plate (20 tiles) on every day d1..6. Ported from NONV2
(tests/test_nonv2.py on selfplay1): ENGINE_GATE_MIN_PLANTS, NONV_PLATE_LAST."""
from __future__ import annotations

import ast
from pathlib import Path

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P

from test_endroute import _view, _digest
from test_budget_order import _macro
from test_engine_gate import _obs

MIX = np.array([4, 0, 0, 4, 0], np.int32)     # wheat 4 + strawberry 4 wanted today
M20Z = "MELON_PLATE_TILES=20;MELON_PLATE_DAY=1;NONV_PLATE_LAST=6"


def _dig(**b):
    return _digest(tuple(np.asarray(a) for a in P.build_day(np, _view(**b), _macro()._replace(plant_target=MIX))))


def _obs_plants(day, melon, wheat, player=0):
    o = _obs(day, melon, player)
    o["farms"][1 - player]["tiles"][0] += [{"kind": "PLANT", "crop": "WHEAT"} for _ in range(wheat)]
    return o


def _source_defaults():
    # read from the file, not the module: other named test files (test_engine_gate) leave the gate globals mutated
    tree = ast.parse(Path(P.__file__).read_text())
    return {t.id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            for t in n.targets if isinstance(t, ast.Name) and isinstance(n.value, ast.Constant)}


def test_ship_vrp7_defaults():
    d = _source_defaults()
    assert d["EMPTY_ROUTE_UNHIRE_ON"] is True and d["ROUTE_VRP_REPAIR_ON"] is True     # vrp6 kept
    assert (d["ENGINE_GATE_ON"], d["ENGINE_GATE_DAY"], d["ENGINE_GATE_MELON_MIN"], d["ENGINE_GATE_MELON_MAX"],
            d["ENGINE_GATE_MIN_PLANTS"], d["ENGINE_GATE_SET"]) == (True, 1, 0, 0, 1, M20Z)
    # the plate itself stays OFF until the latch writes it
    assert d["MELON_PLATE_TILES"] == 0.0 and d["MELON_PLATE_DAY"] == 0.0 and d["NONV_PLATE_LAST"] is None


def test_tz_classifier(monkeypatch):
    for k, v in dict(ENGINE_GATE_MELON_MIN=0, ENGINE_GATE_MELON_MAX=0, ENGINE_GATE_MIN_PLANTS=1).items():
        monkeypatch.setattr(P, k, v)
    assert P.engine_gate_fires(_obs_plants(1, 0, 19), 0)          # 0m/19w (lucasboesen): fires
    assert not P.engine_gate_fires(_obs_plants(1, 0, 0), 0)       # empty farm: undecided
    assert not P.engine_gate_fires(_obs_plants(1, 5, 5), 0)       # non-V melon opener: not the Tz class
    assert not P.engine_gate_fires(_obs_plants(1, 12, 8), 0)      # V56 d1: 12m/8w


def test_latch_writes_window_and_restores():
    b5, b12 = dict(day=5, n_wh=4, money=5000), dict(day=12, n_wh=4, money=5000)
    off5, off12 = _dig(**b5), _dig(**b12)
    old_set = P.ENGINE_GATE_SET
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = M20Z
    try:
        P.engine_gate_apply(True)
        assert (P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST) == (20, 1, 6)
        assert _dig(**b5) != off5          # d5 is inside d1..6: the mix moves onto melon
        assert _dig(**b12) == off12        # d12 is outside the window
        P.engine_gate_apply(False)
        assert (P.MELON_PLATE_TILES, P.MELON_PLATE_DAY, P.NONV_PLATE_LAST) == (0.0, 0.0, None)
        assert _dig(**b5) == off5          # unlatched = the vrp6 program
    finally:
        P.engine_gate_apply(False)
        P._ENGINE_GATE_BASE = None
        P.ENGINE_GATE_SET = old_set
