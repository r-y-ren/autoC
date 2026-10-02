"""[RLFAST1] RESIDUAL_RIVAL_FEAT_ON: OFF = the frozen 64-vector; ON = the 64 + RESIDUAL_N_RIVAL public rival columns,
first 64 unchanged; a v1 head widened by S/rlfast1/widen.py (zero rows, WIDE layout) decodes the same greedy action."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from test_route_early import _seeded_case

from kagg3.core import plan as P

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "S/actionrl"))
sys.path.insert(0, str(ROOT / "S/rlfast1"))


def _view(seed=0):
    return next(x for x in _seeded_case(seed) if isinstance(x, P.DayView))


def test_off_is_64(monkeypatch):
    monkeypatch.setattr(P, "RESIDUAL_RIVAL_FEAT_ON", False)
    assert P._residual_features(np, _view()).shape == (P.RESIDUAL_N_FEAT,)


def test_on_appends_rival_columns(monkeypatch):
    v = _view()
    monkeypatch.setattr(P, "RESIDUAL_RIVAL_FEAT_ON", False)
    f0 = P._residual_features(np, v)
    monkeypatch.setattr(P, "RESIDUAL_RIVAL_FEAT_ON", True)
    f1 = P._residual_features(np, v)
    assert f1.shape == (P.RESIDUAL_N_FEAT + P.RESIDUAL_N_RIVAL,)
    assert np.array_equal(f1[:P.RESIDUAL_N_FEAT], f0)
    assert np.isclose(f1[P.RESIDUAL_N_FEAT], float(v.program_opp_money) / 1e4)
    assert P.program_selector_features(np, v).shape == (P.PROGRAM_N_FEAT,)


def test_widened_v1_head_is_greedy_identical():
    import head as H
    import widen as W
    rng = np.random.default_rng(0)
    p1 = {k: v for k, v in H.init_params(3, lay=H.V1).items()}
    p1["w3"] = rng.normal(size=p1["w3"].shape).astype(np.float32)
    p1["b3"] = rng.normal(size=p1["b3"].shape).astype(np.float32)
    pw = W.widen(p1, P.RESIDUAL_N_RIVAL, H.V1, H.WIDE)
    assert H.layout_of(pw) is H.WIDE
    for _ in range(200):
        f = rng.normal(size=P.RESIDUAL_N_FEAT).astype(np.float32)
        fw = np.concatenate([f, rng.normal(size=P.RESIDUAL_N_RIVAL).astype(np.float32)])
        d1 = H.decode(np, H.greedy_acts(np, H.forward(np, p1, f), H.V1), H.V1)
        dw = H.decode(np, H.greedy_acts(np, H.forward(np, pw, fw), H.WIDE), H.WIDE)
        for k in d1:
            assert np.array_equal(np.asarray(d1[k]), np.asarray(dw[k])), k
        assert int(np.sum(dw["ask_fill"])) == 0 and int(np.sum(dw["seed_buy"])) == 0
