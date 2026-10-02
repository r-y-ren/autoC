"""NVTSHIP1 [plan.ENGINE_GATE2_*]: a second, independent rival-class latch beside ENGINE_GATE.

Claims: OFF by default and inert (the runtime never writes its set); slot 1 alone behaves as before; with the live
M20z latch in slot 1 (d1, melon 0-0, >= 1 plant) and the NVT latch in slot 2 (d2, melon 1-10, >= 1 plant):
a zero-melon opener arms slot 1 only, a melon 1-10 opener arms slot 2 only, the V opening (12 melon) arms neither,
and a d0 zero-melon / d1 melon opener arms both (the latches are not exclusive by construction); a new game resets
both; the slot-2 set restores its own base values.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3.core import plan as P
from kagg3.agent import runtime as R

KEYS = ("ENGINE_GATE_ON", "ENGINE_GATE_DAY", "ENGINE_GATE_MELON_MIN", "ENGINE_GATE_MELON_MAX", "ENGINE_GATE_MIN_PLANTS",
        "ENGINE_GATE_SET", "_ENGINE_GATE_BASE", "ENGINE_GATE2_ON", "ENGINE_GATE2_DAY", "ENGINE_GATE2_MELON_MIN",
        "ENGINE_GATE2_MELON_MAX", "ENGINE_GATE2_MIN_PLANTS", "ENGINE_GATE2_SET", "_ENGINE_GATE2_BASE",
        "NONV_THETA_LIVE", "PLANT_ASK_ON")


def _obs(day, melon, other=0, player=0, hour=0):
    row = ([{"kind": "PLANT", "crop": "MELON"} for _ in range(melon)]
           + [{"kind": "PLANT", "crop": "WHEAT"} for _ in range(other)] + [None, "LOCKED"])
    return {"player": player, "day": day, "hour": hour,
            "farms": [{"tiles": [[None]], "hands": []}, {"tiles": [row], "hands": []}]}


@pytest.fixture(autouse=True)
def _restore():
    keep = {k: getattr(P, k) for k in KEYS}
    yield
    for k, v in keep.items():
        setattr(P, k, v)


def _arm_both():
    # slot 1 = the live M20z latch shape (its set replaced by one cheap flag), slot 2 = the NVT latch
    P.ENGINE_GATE_ON, P.ENGINE_GATE_DAY = True, 1
    P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX, P.ENGINE_GATE_MIN_PLANTS = 0, 0, 1
    P.ENGINE_GATE_SET, P._ENGINE_GATE_BASE = "PLANT_ASK_ON=True", None
    P.ENGINE_GATE2_ON, P.ENGINE_GATE2_DAY = True, 2
    P.ENGINE_GATE2_MELON_MIN, P.ENGINE_GATE2_MELON_MAX, P.ENGINE_GATE2_MIN_PLANTS = 1, 10, 1
    P.ENGINE_GATE2_SET, P._ENGINE_GATE2_BASE = "NONV_THETA_LIVE=True", None


def _play(monkeypatch, opening):
    """opening: {day: (melon, other)}; returns [(PLANT_ASK_ON, NONV_THETA_LIVE)] seen by build_day on days 0-4."""
    seen = []
    monkeypatch.setattr(R.parse, "parse_view", lambda *a, **k: None)
    monkeypatch.setattr(R.P, "build_day", lambda xp, v, m, **k: seen.append((P.PLANT_ASK_ON, P.NONV_THETA_LIVE)) or "plan")
    monkeypatch.setattr(R.render, "turn_action", lambda *a: {})
    for k in ("OVERFLOW_GUARD_ON", "ROUTE_VRP_ON", "END_GAME_ON", "MELON_COUNTER_ON", "PROGRAM_ENGINE_ON"):
        if hasattr(P, k):
            monkeypatch.setattr(P, k, False)
    rt = R.Runtime(lambda o, p, v: None)
    for d in range(5):
        m, o = opening.get(d, opening[max(k for k in opening if k <= d)])
        rt.act(_obs(d, m, o))
    return rt, seen


def test_off_by_default():
    assert P.ENGINE_GATE2_ON is False and P.ENGINE_GATE2_SET == "" and P._ENGINE_GATE2_BASE is None
    assert (P.ENGINE_GATE2_DAY, P.ENGINE_GATE2_MELON_MIN, P.ENGINE_GATE2_MELON_MAX) == (2, 1, 10)


def test_unset_slot2_never_writes(monkeypatch):
    base = (P.PLANT_ASK_ON, P.NONV_THETA_LIVE)
    P.ENGINE_GATE2_SET = "NONV_THETA_LIVE=True"            # a set without the switch: never applied
    rt, seen = _play(monkeypatch, {0: (5, 2)})
    assert seen == [base] * 5 and P._ENGINE_GATE2_BASE is None and rt.opp_engine2 is False


def test_slot1_alone_unchanged(monkeypatch):
    _arm_both(); P.ENGINE_GATE2_ON = False
    off = P.PLANT_ASK_ON
    _rt, seen = _play(monkeypatch, {0: (0, 12)})           # zero-melon opener
    assert [a for a, _ in seen] == [off, True, True, True, True]
    assert all(b is False for _, b in seen)


@pytest.mark.parametrize("opening,want1,want2", [
    ({0: (0, 12)}, True, False),           # zero-melon opener: M20z only
    ({0: (6, 10)}, False, True),           # melon 1-10 opener: NVT only
    ({0: (12, 0)}, False, False),          # the V opening: neither
    ({0: (0, 0), 1: (0, 12), 2: (4, 12)}, True, True),  # d0 zero melon, melon planted d1: both (not exclusive)
    ({0: (0, 0)}, False, False),           # no opening yet: MIN_PLANTS keeps both off
])
def test_both_latches(monkeypatch, opening, want1, want2):
    _arm_both()
    off = P.PLANT_ASK_ON
    rt, seen = _play(monkeypatch, opening)
    assert seen[0] == (off, False)                          # d0: nothing latched
    assert seen[1] == ((True if want1 else off), False)     # d1: slot 1 decides, slot 2 not yet
    assert all(s == ((True if want1 else off), want2) for s in seen[2:])
    assert (rt.opp_engine, rt.opp_engine2) == (want1, want2)
    rt.act(_obs(0, 0, 0))                                   # a new game resets both
    assert (P.PLANT_ASK_ON, P.NONV_THETA_LIVE) == (off, False)
    assert (rt.opp_engine, rt.opp_engine2) == (False, False)


def test_slot2_restores_its_own_base():
    P.NONV_THETA_LIVE = False
    P.ENGINE_GATE2_SET, P._ENGINE_GATE2_BASE = "NONV_THETA_LIVE=True", None
    P.engine_gate2_apply(False); assert P.NONV_THETA_LIVE is False
    P.engine_gate2_apply(True); assert P.NONV_THETA_LIVE is True
    P.engine_gate2_apply(False); assert P.NONV_THETA_LIVE is False
    assert P._ENGINE_GATE_BASE is None or all(n != "NONV_THETA_LIVE" for _, n, _ in P._ENGINE_GATE_BASE)


def test_g008_theta_loads_and_decodes(tmp_path):
    """The g008 class theta (PO.pad layout, 7,791) decodes through brain.decide from a path (numpy; the jitted sim has no latch)."""
    from pathlib import Path
    from kagg3.core import brain
    from test_archetypes import _obs as _pobs
    root = Path(__file__).resolve().parents[1]
    f = root / "S/nvtship1/centre_g008.npy"
    import os
    th = root / "S/winjudge/ship7692/theta7659.npy"
    if not th.exists():   # gitignored: read from the data root (main repo)
        th = Path(os.environ.get("KAGG3_DATA", "/mnt/e/_work/kaggriculture3")) / "S/winjudge/ship7692/theta7659.npy"
    if not f.exists() or not th.exists():
        pytest.skip("g008 / theta7659 not in this checkout")
    theta = np.load(th).astype(np.float32)
    o = _pobs(money=20_000, nquad=2, day=12)
    keep = (P.NONV_THETA, P._NONV_THETA_CACHE[:])
    try:
        P.NONV_THETA, P.NONV_THETA_LIVE = str(f), True
        a = brain.decide(np, theta, o)
        b = brain.decide(np, np.load(f).astype(np.float32), o)
        assert all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(a, b))
        P.NONV_THETA_LIVE = False
        c = brain.decide(np, theta, o)
        assert not all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(a, c))
    finally:
        P.NONV_THETA, P._NONV_THETA_CACHE[:] = keep[0], keep[1]
