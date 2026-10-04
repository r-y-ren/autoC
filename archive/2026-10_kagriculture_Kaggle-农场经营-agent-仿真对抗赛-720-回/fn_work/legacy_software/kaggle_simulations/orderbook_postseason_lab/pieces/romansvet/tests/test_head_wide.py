"""`head.HEAD_LAYOUT`: the WIDE-ASK residual head [ACTIONRL11].

Three contracts.  (1) The v1 layout is what shipped: `head_940.npz` still
loads and still forwards 92 logits, so `res940` is untouched.  (2) The wide
layout's all-keep action decodes to `noop_override`, which is the identity
residual PPO starts from.  (3) A ZERO_BIAS wide head switched ON plans every
pinned board byte for byte the way the head-OFF planner does -- the same
`_digest`/`PIN` pin `test_residual.py` holds the v1 head to, plus a day sweep,
because `ask_fill` only wakes at `RESIDUAL_ASK_DAY0` and the pinned seeds do
not all reach it.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import os
import pathlib

import numpy as np
import pytest
from test_melon_plate import PIN
from test_budget_order import _macro
from test_route_early import (PIN_SEEDS, _digest, _plan, _seeded_case,
                              _view)

from kagg3.core import plan as P

HEAD = P._residual_head_module()
#: The SHIPPED head (sub 56370365 = res940).  Weights are not in git, so in a
#: fresh worktree this test skips; `KAGG3_ROOT` points it at the checkout that
#: does hold them.
_REL = "S/actionrl/flow257_ppo_selfplay/head_940.npz"
H940 = next((pathlib.Path(r) / _REL
             for r in (_pin.repo_root(__file__), os.environ.get("KAGG3_ROOT", ""))
             if r and (pathlib.Path(r) / _REL).exists()),
            pathlib.Path(_REL))


def _wide_on(monkeypatch, params=None):
    params = HEAD.init_params(0, lay=HEAD.WIDE) if params is None else params
    monkeypatch.setattr(P, "RESIDUAL_ON", True)
    monkeypatch.setattr(P, "RESIDUAL_FN", HEAD.numpy_fn(params))


# ------------------------------------------------------------------ (a) v1

def test_v1_layout_is_unchanged():
    assert HEAD.HEAD_LAYOUT == "v1" and HEAD.LAYOUT is HEAD.V1
    assert (HEAD.N_SLOT, HEAD.N_LOGIT) == (18, 92)
    assert HEAD.WIDE.N_SLOT == 20 and HEAD.WIDE.N_LOGIT == 125


@pytest.mark.skipif(not H940.exists(), reason="head_940.npz not in this tree")
def test_head_940_still_loads_as_v1():
    p = HEAD.load(str(H940))
    assert HEAD.layout_of(p) is HEAD.V1
    assert "_layout" not in p                      # the pytree stays weights
    lg = HEAD.forward(np, p, np.zeros(HEAD.N_FEAT, np.float32))
    assert lg.shape == (92,)
    assert HEAD.greedy_acts(np, lg).shape == (18,)


# ---------------------------------------------------------------- (b) wide

def test_wide_all_keep_decodes_to_noop():
    keep = np.asarray(HEAD.WIDE.NOOP, np.int32)
    got, want = HEAD.decode(np, keep), HEAD.noop_override(np, HEAD.WIDE)
    assert set(got) == set(want) == {"d_plant", "d_animal", "d_hire",
                                     "ask_fill", "seed_buy", "hold_num"}
    for k in got:
        assert np.array_equal(got[k], want[k]), k
    assert not np.any(got["d_plant"]) and not np.any(got["d_animal"])
    assert int(got["d_hire"]) == 0 and int(got["ask_fill"]) == 0
    assert int(got["seed_buy"]) == 0 and np.all(got["hold_num"] == 2)


def test_wide_zero_bias_head_is_the_keep_action(tmp_path):
    p = HEAD.init_params(0, lay=HEAD.WIDE)
    assert HEAD.layout_of(p) is HEAD.WIDE
    out = HEAD.numpy_fn(p)(P._residual_features(np, _seeded_case(3)[0]), {})
    want = HEAD.noop_override(np, HEAD.WIDE)
    for k in want:
        assert np.array_equal(out[k], want[k]), k
    f = tmp_path / "w.npz"                          # round-trips as wide
    HEAD.save(f, p)
    assert HEAD.layout_of(HEAD.load(f)) is HEAD.WIDE
    assert HEAD.act_hist(np.asarray(HEAD.WIDE.NOOP)[None, :])[9][0] == 1


# ------------------------------------------------------------ (c) identity

def test_wide_zero_bias_plans_the_pinned_boards_byte_for_byte(monkeypatch):
    _wide_on(monkeypatch)
    assert tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS[:2]) == PIN


def test_wide_zero_bias_matches_head_off_on_every_day(monkeypatch):
    """`ask_fill`/`seed_buy` are dead at the keep action on BOTH sides of the
    `RESIDUAL_ASK_DAY0` gate -- the pinned seeds do not all reach d10."""
    view, macro = _seeded_case(5)
    off = [_digest(_plan(view._replace(day=np.int32(d)), macro)) for d in range(30)]
    _wide_on(monkeypatch)
    on = [_digest(_plan(view._replace(day=np.int32(d)), macro)) for d in range(30)]
    assert on == off


# ------------------------------------------------------------ (d) the channels

def _wide_fn(ask=0, seed=0):
    def fn(feats, fields):
        return {"d_plant": np.zeros(5, np.int32), "d_animal": np.zeros(3, np.int32),
                "d_hire": np.int32(0), "ask_fill": np.int32(ask),
                "seed_buy": np.int32(seed), "hold_num": np.full(9, 2, np.int32)}
    return fn


@pytest.mark.parametrize("day,ask,want", [(11, 0, 6), (9, 4, 6), (11, 1, 25),
                                          (11, 2, 50), (11, 4, 100)])
def test_ask_fill_floors_the_day_ask_inside_the_window(monkeypatch, day, ask, want):
    """`k/4` of `n_free` (100 empty tiles on `_view`) as a FLOOR, d10+ only, all
    of it on the preferred crop -- 3 of [2,3,0,1,0] is CROP 1."""
    monkeypatch.setattr(P, "RESIDUAL_FN", _wide_fn(ask=ask))
    m, _, d_seed = P._residual_override(
        np, _view(day=np.int32(day)),
        _macro(plant_target=np.asarray([2, 3, 0, 1, 0], np.int32),
               animal_want=np.zeros(3, np.int32),
               hold=np.full(9, 10, np.int32)))
    assert int(np.sum(m.plant_target)) == want
    assert int(m.plant_target[1]) == 3 + want - 6 and int(d_seed) == 0


def test_the_wide_channels_reach_the_plan(monkeypatch):
    """Not a no-op: at d12 a full fill plus 4 seed units changes the day's
    plan, and the v1 clamps could not have produced it (+-4 tiles a crop)."""
    view = _view(day=np.int32(12))
    macro = _macro(plant_target=np.asarray([2, 3, 0, 1, 0], np.int32),
                   animal_want=np.zeros(3, np.int32),
                   hold=np.full(9, 10, np.int32))
    monkeypatch.setattr(P, "RESIDUAL_ON", True)
    monkeypatch.setattr(P, "RESIDUAL_FN", _wide_fn(ask=0, seed=0))
    keep = _digest(_plan(view, macro))
    monkeypatch.setattr(P, "RESIDUAL_FN", _wide_fn(ask=4, seed=4))
    assert _digest(_plan(view, macro)) != keep
