"""NVTHETA1 [plan.NONV_THETA]: a second planner theta, read by `brain.decide` only while the d2 gate has latched.

Claims: OFF by default (NONV_THETA None, NONV_THETA_LIVE False); `decide` is byte-identical to the shipped theta when
the switch is OFF, when the latch is unset (a gate that did not fire), and when the class theta equals the shipped one;
a latched game with a different class theta plans with it; the gate set writes and restores NONV_THETA_LIVE; the d2
tell never fires on the V opening (12 melon) and fires on 1-10.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

from pathlib import Path

import numpy as np
import pytest

from kagg3.core import brain
from kagg3.core import plan as P
from kagg3.es import archetypes as A

from test_archetypes import _obs as _pobs
from test_engine_gate import _obs as _gobs

ROOT = Path(__file__).resolve().parents[1]
_TH = ROOT / "S/winjudge/ship7692/theta7659.npy"
THETA = np.load(_TH if _TH.exists() else ROOT / "submission/theta.npy").astype(np.float32)
OBS = [_pobs(money=m, nquad=q, day=d) for m, q, d in ((3_000, 1, 2), (20_000, 2, 12), (60_000, 3, 22))]


def _same(a, b):
    return all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(a, b))


@pytest.fixture(autouse=True)
def _restore():
    keep = (P.NONV_THETA, P.NONV_THETA_LIVE, P.ENGINE_GATE_SET, P._ENGINE_GATE_BASE,
            P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX, P.ENGINE_GATE_MIN_PLANTS)
    P._NONV_THETA_CACHE[:] = [None, None]
    yield
    (P.NONV_THETA, P.NONV_THETA_LIVE, P.ENGINE_GATE_SET, P._ENGINE_GATE_BASE,
     P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX, P.ENGINE_GATE_MIN_PLANTS) = keep


def test_off_by_default():
    assert P.NONV_THETA is None and P.NONV_THETA_LIVE is False


def test_off_and_unlatched_are_byte_identical(tmp_path):
    other = A.archetype_theta(**A.named("expander"))
    base = [brain.decide(np, THETA, o) for o in OBS]
    P.NONV_THETA_LIVE = True; P.NONV_THETA = None                 # latched, switch OFF
    assert all(_same(b, brain.decide(np, THETA, o)) for b, o in zip(base, OBS))
    P.NONV_THETA_LIVE = False; P.NONV_THETA = other               # switch ON, gate did not fire
    assert all(_same(b, brain.decide(np, THETA, o)) for b, o in zip(base, OBS))
    f = tmp_path / "same.npy"; np.save(f, THETA)
    P.NONV_THETA_LIVE = True; P.NONV_THETA = str(f)               # latched, class theta = shipped
    assert all(_same(b, brain.decide(np, THETA, o)) for b, o in zip(base, OBS))


def test_latched_uses_the_class_theta(tmp_path):
    other = A.archetype_theta(**A.named("expander"))
    f = tmp_path / "nv.npy"; np.save(f, other)
    want = [brain.decide(np, other, o) for o in OBS]
    P.NONV_THETA_LIVE = True; P.NONV_THETA = str(f)
    got = [brain.decide(np, THETA, o) for o in OBS]
    assert all(_same(w, g) for w, g in zip(want, got))
    P.NONV_THETA_LIVE = False
    assert not all(_same(w, brain.decide(np, THETA, o)) for w, o in zip(want, OBS))


def test_padded_theta_decodes_the_same():
    from kagg3.core import policy as PO
    pad = PO.pad(THETA).astype(np.float32)
    assert all(_same(brain.decide(np, THETA, o), brain.decide(np, pad, o)) for o in OBS)


def test_gate_set_writes_and_restores_the_latch():
    P._ENGINE_GATE_BASE = None
    P.ENGINE_GATE_SET = "NONV_THETA_LIVE=True"
    P.engine_gate_apply(False)
    assert P.NONV_THETA_LIVE is False
    P.engine_gate_apply(True)
    assert P.NONV_THETA_LIVE is True
    P.engine_gate_apply(False)
    assert P.NONV_THETA_LIVE is False


def test_tell_skips_the_v_opening():
    P.ENGINE_GATE_MELON_MIN, P.ENGINE_GATE_MELON_MAX, P.ENGINE_GATE_MIN_PLANTS = 1, 10, 1
    assert not P.engine_gate_fires(_gobs(2, 12), 0)
    assert not P.engine_gate_fires(_gobs(2, 0), 0)
    assert all(P.engine_gate_fires(_gobs(2, n), 0) for n in (1, 5, 10))
