"""RLACT1 [plan.RL_ACT_ON + S/actionrl/head.py layout "act"]: the head's two work outputs.

Claims: OFF by default; the ACT layout is WIDE + relay_n (0..6) + q4_buy (0/1) with no-op 0; a ZERO action
(relay_n 0, q4_buy 0, every other slot at its no-op) is the OFF plan byte for byte on the recorded days of
tests/test_q4_relay.py; relay_n = k adds exactly k admitted wheat PLANT ops (and their seed) on d12 when free
tiles and cash allow, and nothing else moves in the crop mix; relay_n is inert once wheat cannot mature;
q4_buy buys the fourth quadrant (only the fourth) when the purse covers it; the feature block is 4 columns
(RL_ACT_OBS pass/100, relay tiles free/40, wheat quote/100, rival wheat sold/50); widen_act keeps head_940's
greedy action on every old slot and puts 0 on the new ones.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import sys
from pathlib import Path

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board, _plan, _plants, _seeds, _land, PT

ROOT = Path(__file__).resolve().parents[1]
for _p in ("S/actionrl", "S/rlfast1"):
    if str(ROOT / _p) not in sys.path:
        sys.path.insert(0, str(ROOT / _p))
import head as H  # noqa: E402

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # tests/test_q4_relay.py master digest, same on all three days


def _head(lay, relay=0, buy=0):
    acts = np.asarray(lay.NOOP, np.int32).copy()
    if lay.name == "act":
        acts[20], acts[21] = relay, buy

    def fn(obs_features, macro_fields):
        return H.decode(np, acts, lay)
    return fn


def _arm(m, lay, relay=0, buy=0, rl=True):
    m.setattr(P, "RESIDUAL_ON", True)
    m.setattr(P, "RESIDUAL_FN", _head(lay, relay, buy))
    m.setattr(P, "RL_ACT_ON", rl)


def test_off_by_default():
    assert P.RL_ACT_ON is False and "RL_ACT_ON" not in P.SWITCH_GENES
    assert P.RL_ACT_RELAY_MAX == 6 and P.RL_ACT_N_FEAT == 4 and P.RL_ACT_OBS == (0, 0)
    assert H.ACT.N_SLOT == 22 and H.ACT.N_LOGIT == 134 and H.ACT.NOOP[20:] == (0, 0)
    assert H.ACT.SLOTS[:20] == H.WIDE.SLOTS and H.ACT.wide
    o = H.noop_override(np, H.ACT)
    assert int(o["relay_n"]) == 0 and int(o["q4_buy"]) == 0
    assert "relay_n" not in H.noop_override(np, H.WIDE)


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_zero_action_byte_identical(monkeypatch, d, q, m, w):
    view = _board(d, q, money=m, q4_wheat=w)
    assert _digest(_plan(view)) == MASTER
    with monkeypatch.context() as mp:
        _arm(mp, H.WIDE, rl=False)                       # RLFAST2's layout, switch OFF
        wide = _digest(_plan(view))
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT)                                  # RLACT1, zero action
        act = _digest(_plan(view))
    assert act == wide == MASTER


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5, 6])
def test_relay_n_k_admitted(monkeypatch, k):
    view = _board(12, 3, money=9000)
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT)
        base = _plan(view)
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT, relay=k)
        on = _plan(view)
    add = [b - a for a, b in zip(_plants(base), _plants(on))]
    assert add[spec.I_WHEAT] == k and add[1:] == [0, 0, 0, 0]
    assert _seeds(on)[spec.I_WHEAT] >= _seeds(base)[spec.I_WHEAT]
    assert _land(on) == _land(base)


def test_relay_on_owned_q4(monkeypatch):
    view = _board(15, 4, money=9000, q4_wheat=5)
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT)
        base = _plants(_plan(view))
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT, relay=4)
        on = _plants(_plan(view))
    assert on[spec.I_WHEAT] - base[spec.I_WHEAT] == 4 and on[1:] == base[1:]


def test_relay_inert_when_wheat_cannot_mature(monkeypatch):
    view = _board(27, 3, money=9000)
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT)
        base = _digest(_plan(view))
    with monkeypatch.context() as mp:
        _arm(mp, H.ACT, relay=6)
        assert _digest(_plan(view)) == base


def test_q4_buy(monkeypatch):
    for d, q, money, want in ((12, 3, 9000, 1), (12, 2, 9000, 0), (12, 3, 300, 0)):
        view = _board(d, q, money=money)
        with monkeypatch.context() as mp:
            _arm(mp, H.ACT)
            off = _land(_plan(view))
        with monkeypatch.context() as mp:
            _arm(mp, H.ACT, buy=1)
            on = _land(_plan(view))
        assert off == 0 and on == want, (d, q, money, off, on)


def test_feature_block(monkeypatch):
    view = _board(12, 3, money=9000)
    macro = _macro(plant_target=PT)
    monkeypatch.setattr(P, "RL_ACT_ON", True)
    monkeypatch.setattr(P, "RL_ACT_OBS", (37, 12))
    f = np.asarray(P._residual_features(np, view, macro))
    assert f.shape == (P.RESIDUAL_N_FEAT + P.RL_ACT_N_FEAT,)
    free = max(int(np.sum(view.kind == spec.KIND_EMPTY)) - int(PT.sum()), 0)
    want = np.array([0.37, free / 40.0, float(view.price[spec.I_WHEAT]) / 100.0, 12 / 50.0], np.float32)
    assert np.allclose(f[-4:], want)
    monkeypatch.setattr(P, "RL_ACT_ON", False)
    assert np.array_equal(np.asarray(P._residual_features(np, view, macro)), f[:P.RESIDUAL_N_FEAT])


def test_widen_act_greedy_identical():
    import widen as WD
    h940 = ROOT / "S/actionrl/flow257_ppo_selfplay/head_940.npz"
    if not h940.exists():
        pytest.skip("head_940 not in this checkout")
    nr = P.RESIDUAL_N_RIVAL
    pw = WD.widen(H.load(str(h940)), nr, H.V1, H.WIDE)
    pa = WD.widen_act(pw, P.RL_ACT_N_FEAT, H.WIDE, H.ACT, 3.0)
    assert pa["b3"].shape == (H.ACT.N_LOGIT,) and pa["w1"].shape[0] == pw["w1"].shape[0] + P.RL_ACT_N_FEAT
    rng = np.random.default_rng(0)
    for _ in range(20):
        x = rng.normal(size=pw["w1"].shape[0]).astype(np.float32)
        xa = np.concatenate([x, rng.normal(size=P.RL_ACT_N_FEAT).astype(np.float32)])
        gw = H.greedy_acts(np, H.forward(np, pw, x), H.WIDE)
        ga = H.greedy_acts(np, H.forward(np, pa, xa), H.ACT)
        assert np.array_equal(ga[:20], gw) and ga[20] == 0 and ga[21] == 0
