import os
import sys

import numpy as np

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "S", "actionrl"))

import jax
import jax.numpy as jnp

import head
import ppo


def _assert_override_equal(got, want):
    assert got.keys() == want.keys()
    for key in got:
        np.testing.assert_array_equal(np.asarray(got[key]), np.asarray(want[key]))


def test_opponent_greedy_jax_matches_numpy():
    learner = head.init_params(1)
    opponent = head.init_params(2)
    opponent["b3"] = opponent["b3"].copy()
    opponent["b3"][0] = 20.0
    f0 = np.linspace(-1, 1, head.N_FEAT, dtype=np.float32)
    f1 = np.linspace(1, -1, head.N_FEAT, dtype=np.float32)
    box = []
    fn = head.jax_fn(jnp, jax.random, learner, jax.random.PRNGKey(3), box,
                     opponent_params=opponent, learner_seat=jnp.int32(0),
                     greedy=True)
    fn(f0, None)
    got = fn(f1, None)
    want = head.numpy_fn(opponent)(f1, None)
    _assert_override_equal(got, want)
    assert len(box) == 1
    np.testing.assert_array_equal(np.asarray(box[0][0]), f0)


def test_identical_greedy_pair_has_zero_delta_and_reward():
    params = head.init_params(4)
    feats = np.stack([
        np.linspace(-0.5, 0.5, head.N_FEAT, dtype=np.float32),
        np.linspace(0.5, -0.5, head.N_FEAT, dtype=np.float32),
    ])
    acts = head.greedy_acts(np, head.forward(np, params, feats))
    ref_acts = head.greedy_acts(np, head.forward(np, params, feats))
    np.testing.assert_array_equal(acts, ref_acts)
    money = np.asarray([[12000, 9000], [7000, 7000]], np.int32)
    reward, gift, _, _ = ppo.reference_reward(money, money.copy(), 1.7, 0.0)
    np.testing.assert_array_equal(money - money, 0)
    np.testing.assert_array_equal(gift, 0.0)
    np.testing.assert_array_equal(reward, 0.0)


def test_learner_purse_order_for_both_seats():
    money = jnp.asarray([111, 222], jnp.int32)
    np.testing.assert_array_equal(ppo.learner_money(jnp, money, jnp.int32(0)),
                                  [111, 222])
    np.testing.assert_array_equal(ppo.learner_money(jnp, money, jnp.int32(1)),
                                  [222, 111])


def test_default_terminal_reward_is_old_formula():
    win = np.asarray([1.0, -1.0, 1.0])
    margin = np.asarray([2500.0, -800.0, 0.0])
    zeros = np.zeros_like(margin)
    got = ppo.terminal_reward(win, margin, zeros, zeros, False, 0.0, 1.0)
    np.testing.assert_array_equal(got, win + margin / 1e4)
