import os
import sys

import numpy as np

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "S", "actionrl"))

import jax.numpy as jnp

import head
import ppo


def test_loss_frac_one_samples_only_live_losses():
    rng = np.random.default_rng(7)
    pool = np.asarray([4, 8, 15, 16], np.int32)
    margins = np.asarray([100, -2, 0, -9], np.int32)
    chosen = ppo.sample_live_indices(rng, pool, margins, 100, 1.0)
    assert set(chosen.tolist()) <= {8, 16}


def test_incumbent_hinge_zero_at_requested_margin():
    logits = np.zeros((3, head.N_LOGIT), np.float32)
    incumbent = np.zeros((3, head.N_SLOT), np.int32)
    for slot in range(head.N_SLOT):
        logits[:, head.OFFSET[slot]] = 1.0
    got = ppo.incumbent_hinge(jnp.asarray(logits), jnp.asarray(incumbent),
                              jnp.ones(3), 1.0)
    assert float(got) == 0.0


def test_margin_weight_zero_removes_reference_margin_loss():
    incumbent = np.asarray([[10_000, 8_000]], np.int32)
    candidate = np.asarray([[10_000, 9_000]], np.int32)
    reward, gift, win, win_ref = ppo.reference_reward(
        candidate, incumbent, eta=3.0, gift_budget=0.0, margin_weight=0.0)
    np.testing.assert_array_equal(win, win_ref)
    assert gift[0] > 0.0
    np.testing.assert_array_equal(reward, 0.0)
