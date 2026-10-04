"""`task_order` is the pairwise ranker the admit stage uses (PLANNER_V3_1
1.6): descending tier, then descending value, exact ties by serpentine
position.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P


def test_task_order_ties_fall_to_serpentine_position():
    task = np.zeros(100, bool)
    task[[7, 3, 50, 12]] = True
    score = np.zeros(100, np.int32)
    order = P.task_order(np, task, score)
    assert list(order[:4]) == [3, 7, 12, 50]
    assert sorted(order.tolist()) == list(range(100))


def test_task_order_ranks_by_score_then_position():
    task = np.zeros(100, bool)
    task[[7, 3, 50, 12]] = True
    score = np.zeros(100, np.int32)
    score[50] = 2
    score[12] = 1
    score[7] = 1
    order = P.task_order(np, task, score)
    assert list(order[:4]) == [50, 7, 12, 3]


def test_task_order_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(0)
    for _ in range(20):
        task = rng.random(100) < 0.6
        score = rng.integers(-5, 6, size=100).astype(np.int32)   # plenty of ties
        a = P.task_order(np, task, score)
        b = np.asarray(P.task_order(jnp, jnp.asarray(task), jnp.asarray(score)))
        assert a.tolist() == b.tolist()
