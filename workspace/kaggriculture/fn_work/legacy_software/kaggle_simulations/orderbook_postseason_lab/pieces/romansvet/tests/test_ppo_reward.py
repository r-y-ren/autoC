"""`ppo.terminal_reward` / `ppo.board_weights` [ACTIONRL12].

Run this file ALONE (`pytest -q tests/test_ppo_reward.py`): importing
`S/actionrl/ppo.py` applies the shipped switch string and sets
`plan.RESIDUAL_ON = True` at module level, which is the trainer's contract and
not a state other test modules should inherit.
"""
from __future__ import annotations

import os
import sys

import _pin

_pin.bootstrap()

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "S", "actionrl"))

ppo = pytest.importorskip("ppo")


def test_margin_weight_zero_is_the_win_term_alone():
    """`--margin-weight 0` leaves `+-1` and NOTHING else, paired or not.

    The whole point of flow265: every arm so far had `mwin` flat while the
    coin term moved by thousands, so the gradient was the coin's.
    """
    win = np.array([1.0, -1.0, 1.0])
    margin = np.array([12_345.0, -8_000.0, 0.0])
    d_ours = np.array([1_469.0, -200.0, 50.0])
    d_theirs = np.array([944.0, 30.0, -10.0])
    for paired, lam in ((False, 0.0), (True, 1.0), (True, 2.0)):
        r = ppo.terminal_reward(win, margin, d_ours, d_theirs, paired, lam,
                                0.0)
        assert np.array_equal(r, win)
    # ... and W = 1.0 is still the reward every earlier run trained on.
    assert np.allclose(
        ppo.terminal_reward(win, margin, d_ours, d_theirs, False, 0.0, 1.0),
        win + margin / 1e4)
    assert np.allclose(
        ppo.terminal_reward(win, margin, d_ours, d_theirs, True, 2.0, 1.0),
        win + (d_ours - 2.0 * d_theirs) / 1e4)
    # W scales the coin term only, linearly.
    assert np.allclose(
        ppo.terminal_reward(win, margin, d_ours, d_theirs, False, 0.0, 0.5),
        win + 0.5 * margin / 1e4)


def test_board_weights_floor_and_flip_ratio():
    """`max(P, 4 p0 (1 - p0))`, normalised: no board excluded, 4x at a flip."""
    p0 = np.array([0.0, 1.0, 0.5, 0.2, 0.8, 0.9])
    w = ppo.board_weights(p0, 0.25)
    assert np.isclose(w.sum(), 1.0)
    assert (w > 0).all()                       # the floor keeps every board
    raw = np.maximum(0.25, 4.0 * p0 * (1.0 - p0))
    assert np.allclose(w, raw / raw.sum())
    # a coin-flip board is worth 4 sure ones, and 0.2/0.8 is 0.64 -> ~2.6x
    assert np.isclose(w[2] / w[0], 4.0)
    assert np.isclose(w[3], w[4])
    assert np.isclose(w[3] / w[0], 0.64 / 0.25)
    # P = 0 is allowed and only zeroes the boards that carry no gradient
    w0 = ppo.board_weights(p0, 0.0)
    assert w0[0] == 0.0 and w0[1] == 0.0 and w0[2] > 0.0
