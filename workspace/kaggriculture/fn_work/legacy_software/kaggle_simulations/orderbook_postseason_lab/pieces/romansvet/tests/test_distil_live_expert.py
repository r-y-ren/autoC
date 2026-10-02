"""Focused contracts for LIVEEXPERT behaviour cloning."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "S/actionrl/distil_live_expert.py"
SPEC = importlib.util.spec_from_file_location("distil_live_expert", PATH)
D = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = D
SPEC.loader.exec_module(D)


def _synthetic_inputs():
    programs, traces = {}, {}
    params = D.HEAD.init_params(7, lay=D.HEAD.V1)
    for index in range(150):
        rows = []
        for day in range(30):
            feats = np.full(D.HEAD.N_FEAT, index / 200 + day / 1000,
                            np.float32)
            base = D.HEAD.greedy_acts(
                np, D.HEAD.forward(np, params, feats), D.HEAD.V1)
            acts = base.copy()
            if index < 41 and day == 10:
                acts[index % 5] = 8
            rows.append((day, feats, base, acts))
        traces[index] = rows
        if index < 41:
            programs[index] = {"overrides": [
                {"day": 10, "slot": index % 5, "value": 8}]}
    return programs, traces


def test_data_assembly_shapes_and_populations():
    programs, traces = _synthetic_inputs()
    data = D.assemble_dataset(programs, traces)
    assert data.expert_states == 41 * 30
    assert data.win_states == 109 * 30
    assert data.overrides.features.shape == (41, D.HEAD.N_FEAT)
    assert len(data.other_expert) == 41 * 30 * 18 - 41
    assert len(data.win_rehearsal) == 109 * 30 * 18
    assert np.all(data.overrides.labels == 8)


def test_loss_is_three_separately_normalised_terms():
    params = jax.tree_util.tree_map(jnp.asarray, D.HEAD.init_params(3))
    feats = np.zeros((3, D.HEAD.N_FEAT), np.float32)
    samples = D.Samples(feats, np.asarray([0, 8, 12], np.int32),
                        np.asarray([8, 4, 0], np.int32))
    total, terms = D.distil_loss(params, samples, samples, samples)
    assert np.isfinite(float(total))
    assert np.isclose(float(total),
                      float(terms[0] + 0.1 * terms[1] + terms[2]))


def test_one_tiny_epoch_updates_head_with_finite_loss():
    rng = np.random.default_rng(9)
    feats = rng.normal(size=(8, D.HEAD.N_FEAT)).astype(np.float32)
    sample = D.Samples(feats, np.zeros(8, np.int32),
                       np.full(8, 8, np.int32))
    data = D.Dataset(sample, sample, sample, 8, 8)
    params = jax.tree_util.tree_map(jnp.asarray, D.HEAD.init_params(11))
    before = np.asarray(params["w3"])
    state = D.adam_init(params)
    losses = []
    for batch in D.balanced_batches(data, 4, rng):
        params, state, loss, _ = D.train_step(params, state, *batch, 1e-3)
        losses.append(float(loss))
    assert len(losses) == 2 and np.isfinite(losses).all()
    assert not np.array_equal(before, np.asarray(params["w3"]))
