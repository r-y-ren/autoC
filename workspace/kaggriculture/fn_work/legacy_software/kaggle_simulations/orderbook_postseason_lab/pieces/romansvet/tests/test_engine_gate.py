"""`plan.ENGINE_GATE_ON` [ENGGATE1]: a per-game rival-class latch at d2.

Claims: OFF by default; the classifier is the REPLANTGATE band
`1 <= rival melon tiles <= 10`; apply(True)/apply(False) writes and restores
the module values exactly, so the whole-plan digests after a restore equal the
untouched ones; the runtime latches once at ENGINE_GATE_DAY, never before, and
resets on a new game.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P
from kagg3.agent import runtime as R

from test_endroute import _macro, _view, _digest

BOARDS = (dict(day=1, n_wh=4), dict(day=12, n_wh=8, shed_wh=20, shops=2),
          dict(day=24, n_wh=8, shed_wh=20, shops=2))
SET = "PLANT_ASK_ON=True;WHEAT_LATE_ASK=0.5;REPLANT_SAME_TURN_ON=True"


def _obs(day, melon, player=0, hour=0):
    tile = {"kind": "PLANT", "crop": "MELON"}
    row = [dict(tile) for _ in range(melon)] + [None, "LOCKED"]
    return {"player": player, "day": day, "hour": hour,
            "farms": [{"tiles": [[None]], "hands": []},
                      {"tiles": [row], "hands": []}]}


def _digests():
    return [_digest(tuple(np.asarray(a) for a in P.build_day(np, _view(**b), _macro())))
            for b in BOARDS]


def _reset(set_=SET):
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = set_


def test_off_by_default():
    assert P.ENGINE_GATE_ON is False and P.ENGINE_GATE_SET == ""
    assert P.ENGINE_GATE_DAY == 2
    assert (P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX) == (1, 10)


def test_classifier_band():
    assert not P.engine_gate_fires(_obs(2, 0), 0)
    assert P.engine_gate_fires(_obs(2, 1), 0)
    assert P.engine_gate_fires(_obs(2, 10), 0)
    assert not P.engine_gate_fires(_obs(2, 12), 0)       # the band clone
    assert not P.engine_gate_fires({"player": 0, "farms": [{}]}, 0)


def test_apply_restore_and_plan_parity():
    base = _digests()
    old = (P.PLANT_ASK_ON, P.WHEAT_LATE_ASK, P.REPLANT_SAME_TURN_ON)
    _reset()
    try:
        P.engine_gate_apply(True)
        assert (P.PLANT_ASK_ON, P.WHEAT_LATE_ASK, P.REPLANT_SAME_TURN_ON) == (True, 0.5, True)
        P.engine_gate_apply(False)
        assert (P.PLANT_ASK_ON, P.WHEAT_LATE_ASK, P.REPLANT_SAME_TURN_ON) == old
        assert _digests() == base
    finally:
        _reset("")


def test_runtime_latch(monkeypatch):
    seen = []
    monkeypatch.setattr(R.parse, "parse_view", lambda *a, **k: None)
    monkeypatch.setattr(R.P, "build_day", lambda xp, v, m: seen.append(P.PLANT_ASK_ON) or "plan")
    monkeypatch.setattr(R.render, "turn_action", lambda *a: {})
    monkeypatch.setattr(P, "OVERFLOW_GUARD_ON", False)
    monkeypatch.setattr(P, "ENGINE_GATE_ON", True)
    base = P.PLANT_ASK_ON
    _reset("PLANT_ASK_ON=True")
    try:
        rt = R.Runtime(lambda o, p, v: None)
        for d, m in ((0, 0), (1, 5), (2, 5), (3, 12), (4, 0)):
            rt.act(_obs(d, m))
        assert seen == [base, base, True, True, True]
        rt.act(_obs(0, 5))                               # a new game resets
        assert seen[-1] == base and rt.opp_engine is False
        seen.clear()
        rt2 = R.Runtime(lambda o, p, v: None)
        for d in range(5):
            rt2.act(_obs(d, 12))                         # band: never fires
        assert seen == [base] * 5
    finally:
        P.engine_gate_apply(False)
        _reset("")
