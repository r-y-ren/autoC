"""Focused CPU contracts for the greedy output-bias ES trainer."""
from __future__ import annotations

import os
import pathlib
import sys

import _pin

_pin.bootstrap()

import numpy as np
import pytest

ROOT = pathlib.Path(_pin.repo_root(__file__))
sys.path.insert(0, str(ROOT / "S" / "actionrl"))
es_head = pytest.importorskip("es_head")
HEAD = es_head.HEAD
H940 = ROOT / "S/actionrl/flow257_ppo_selfplay/head_940.npz"


@pytest.fixture(scope="module")
def reference():
    if not H940.exists():
        pytest.skip("head_940.npz not in this tree")
    return HEAD.load(H940)


def test_projection_is_slot_mean_free_and_zero_reproduces_greedy(reference):
    rng = np.random.default_rng(267)
    z = rng.normal(size=HEAD.V1.N_LOGIT).astype(np.float32)
    pz = es_head.project_mean_free(z)
    for off, n in zip(HEAD.V1.OFFSET, HEAD.V1.N_ACT):
        assert abs(float(pz[off:off + n].mean())) < 2e-7

    feats = rng.normal(size=(7, HEAD.N_FEAT)).astype(np.float32)
    got = es_head.greedy_actions(es_head.params_at(reference, np.zeros(92)), feats)
    want = es_head.greedy_actions(reference, feats)
    assert np.array_equal(got, want)


def test_reference_fitness_against_itself_is_exactly_zero():
    money = np.asarray([[10, 2], [4, 4], [-3, 8], [11, 10]], np.int32)
    fitness, gift, win_delta, _ = es_head.paired_fitness(money, money, 1.0)
    assert fitness == 0.0
    assert gift == 0.0
    assert win_delta == 0.0


def test_checkpoint_loads_and_matches_in_memory_actions(reference, tmp_path):
    rng = np.random.default_rng(9)
    z = es_head.project_mean_free(rng.normal(size=92).astype(np.float32)) * 0.03
    params = es_head.params_at(reference, z)
    path = tmp_path / "head_1.npz"
    HEAD.save(path, params, gen=1, sigma=0.03)
    loaded = HEAD.load(path)
    feats = rng.normal(size=(9, HEAD.N_FEAT)).astype(np.float32)
    assert np.array_equal(es_head.greedy_actions(params, feats),
                          es_head.greedy_actions(loaded, feats))


def test_fixes_genes_only_change_state_conditioned_plant_bin8(reference):
    rng = np.random.default_rng(302)
    feats = rng.normal(size=(6, HEAD.N_FEAT)).astype(np.float32)
    hidden = HEAD.trunk(np, reference, feats)
    mean = np.zeros(HEAD.N_HIDDEN, np.float32)
    components = np.eye(HEAD.N_HIDDEN, dtype=np.float32)[:4]
    coeff = np.arange(25, dtype=np.float32).reshape(5, 5) / 10
    fixed = es_head.fixes_params(reference, coeff, mean, components)
    before = HEAD.forward(np, reference, feats)
    after = HEAD.forward(np, fixed, feats)
    want = np.concatenate([np.ones((len(feats), 1), np.float32), hidden[:, :4]], 1) @ coeff.T
    changed = np.zeros(HEAD.V1.N_LOGIT, bool)
    for slot in range(5):
        index = HEAD.V1.OFFSET[slot] + 8
        changed[index] = True
        np.testing.assert_allclose(after[:, index] - before[:, index], want[:, slot],
                                   rtol=1e-5, atol=1e-5)
    np.testing.assert_array_equal(after[:, ~changed], before[:, ~changed])


def test_fixes_sigma_crosses_expert_targets_at_one_percent():
    reference = HEAD.init_params(7, lay=HEAD.V1)
    feats = np.zeros((100, HEAD.N_FEAT), np.float32)
    slots = np.arange(100, dtype=np.int32) % 5
    mean = np.zeros(HEAD.N_HIDDEN, np.float32)
    components = np.eye(HEAD.N_HIDDEN, dtype=np.float32)[:4]
    sigma, rate = es_head.calibrate_fixes_sigma(
        reference, feats, slots, mean, components, np.random.default_rng(9))
    assert sigma > 0
    assert rate >= 0.01


def test_fixes_checkpoint_retains_frozen_pcs(reference, tmp_path):
    mean = np.arange(HEAD.N_HIDDEN, dtype=np.float32)
    components = np.eye(HEAD.N_HIDDEN, dtype=np.float32)[:4]
    params = es_head.fixes_params(reference, np.arange(25), mean, components)
    path = tmp_path / "fixes.npz"
    HEAD.save(path, params, gen=5, sigma=1.0)
    loaded = HEAD.load(path)
    np.testing.assert_array_equal(loaded["fixes_pc_mean"], mean)
    np.testing.assert_array_equal(loaded["fixes_pc_components"], components)
    np.testing.assert_array_equal(loaded["fixes_coeff"], np.arange(25).reshape(5, 5))
