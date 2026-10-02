from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "S/actionrl"))

import head as HEAD
import live_program as LP
import live_program_head as LPH
from kagg3 import spec
from kagg3.agent import parse


def _tile(kind, **kw):
    return {"kind": kind, **kw}


def _obs():
    empty = [[None for _ in range(spec.BOARD)] for _ in range(spec.BOARD)]
    ours, theirs = copy.deepcopy(empty), copy.deepcopy(empty)
    ours[0][0] = _tile("PLANT", crop="WHEAT", planted_day=9,
                       watered_today=False, consecutive_unwatered=0,
                       yield_units=7, fertilized_until_day=-1)
    theirs[9][9] = _tile("PLANT", crop="MELON", planted_day=3,
                         watered_today=False, consecutive_unwatered=0,
                         yield_units=11, fertilized_until_day=-1)
    farms = [
        {"money": 12345, "tiles": ours, "unlocked_quadrants": [0], "hands": []},
        {"money": 10000, "tiles": theirs, "unlocked_quadrants": [0], "hands": []},
    ]
    return {
        "day": 10, "hour": 0, "player": 0, "farms": farms,
        "private": {"shed": {}, "seeds": {}},
        "market": {"prices": {p: 100 for p in spec.PRODUCTS},
                   "inventory": {p: spec.MARKET_I0 for p in spec.PRODUCTS}},
        "town": {"unlocked_shops": []},
    }


def test_feature_shape_order_invariance_and_no_id_leakage():
    obs = _obs()
    x = parse.program_selector_features(obs, 0)
    assert x.shape == (115,)
    moved = copy.deepcopy(obs)
    moved["farms"][0]["tiles"][5][4] = moved["farms"][0]["tiles"][0][0]
    moved["farms"][0]["tiles"][0][0] = None
    moved["farms"][1]["tiles"][2][6] = moved["farms"][1]["tiles"][9][9]
    moved["farms"][1]["tiles"][9][9] = None
    moved.update(episode=999, seed=888, game_index=777,
                 final_ours=-1, final_theirs=10**9)
    np.testing.assert_array_equal(x, parse.program_selector_features(moved, 0))
    assert x[64] == 1.0                    # opponent purse / 1e4
    assert np.isclose(x[65], .2345)        # purse difference / 1e4
    assert x[-1] == 0.0


def test_abstain_is_exact_head_identity():
    params = HEAD.load(LP.LE.DEFAULT_HEAD)
    base = HEAD.numpy_fn(params)
    wrapped = LPH.numpy_fn(params)
    ns = HEAD.V1.N_SLOT
    wrapped.set_program(np.zeros((30, ns), bool), np.zeros((30, ns), np.int32))
    features = np.zeros(HEAD.N_FEAT, np.float32)
    fields = {"day": np.int32(10),
              "program_features": np.zeros(LP.N_FEATURE, np.float32)}
    a, b = base(features, fields), wrapped(features, fields)
    assert a.keys() == b.keys()
    for key in a:
        np.testing.assert_array_equal(a[key], b[key])


def test_cv_provenance_isolation():
    sources = [20, 36, 52, 57, 85, 87, 89, 102, 117, 122, 126, 128, 147]
    for fold in range(5):
        allowed = LP.allowed_for_fold(sources, fold)
        assert allowed[0]
        assert all(allowed[i] == (sources[i - 1] % 5 != fold)
                   for i in range(1, 14))


def test_exact_logit_tie_abstains():
    model = {"w1": np.zeros((115, 16), np.float32),
             "b1": np.zeros(16, np.float32),
             "w2": np.zeros((16, 14), np.float32),
             "b2": np.zeros(14, np.float32)}
    assert LPH.choose_program(model, np.zeros(115, np.float32)) == 0
