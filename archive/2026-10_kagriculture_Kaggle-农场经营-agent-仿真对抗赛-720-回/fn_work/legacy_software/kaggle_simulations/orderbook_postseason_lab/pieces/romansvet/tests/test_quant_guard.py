"""The cross-backend quantisation guard has to scale with the value it guards.

float32 agreement between numpy and XLA is relative, so an absolute epsilon
covers products only up to ~1,000 -- and `hold` is decoded in coins. Pinned to
the theta and the trajectory decision that first split the backends (numpy 484
against XLA 483, 2026-08-27).
"""
import os
import pathlib
import sys

import numpy as np
import pytest

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3 import precision  # noqa: F401  pins matmul precision at import
from kagg3.core import brain

FIXTURE = ROOT / "tests" / "data" / "trajectory_obs.npz"
THETA = ROOT / "tests" / "data" / "theta_hold_cliff.npy"
DECISION = 1656


def test_the_guard_is_relative_where_the_value_is_large():
    """The measured pair: both are 484 to the guard, neither to a bare floor."""
    lo, hi = np.float32(483.99982), np.float32(483.99990)
    assert np.floor(lo) == 483 and np.floor(hi) == 483
    assert brain._qfloor(np, lo) == 484
    assert brain._qfloor(np, hi) == 484


def test_the_guard_is_still_absolute_where_the_value_is_small():
    """Fractions and counts keep the 1e-4 they were tuned with."""
    assert brain._qfloor(np, np.float32(0.99995)) == 1
    assert brain._qfloor(np, np.float32(0.9998)) == 0
    assert brain._qfloor(np, np.float32(2.5)) == 2


def test_the_guard_never_reaches_a_genuine_decision():
    """At coin scale the shift is about a coin in a million: far under the half
    that would move an honest landing, and absorbed by the cap at the top."""
    x = np.float32(483.0)
    assert brain._qfloor(np, x + 0.4) == 483
    assert brain._qfloor(np, x + 0.6) == 483
    cap = np.float32(brain.spec.COIN_CAP - 1)
    assert brain._qfloor(np, cap) <= brain.spec.COIN_CAP   # the decode clips after this


@pytest.mark.skipif(not FIXTURE.is_file(), reason="needs the trajectory fixture")
def test_decision_1656_decodes_the_same_hold_on_both_backends():
    import jax
    import jax.numpy as jnp

    theta = np.load(THETA).astype(np.float32)
    d = np.load(FIXTURE)
    o = brain.PolicyObs(**{f: d[f][DECISION] for f in brain.PolicyObs._fields
                           if f in d.files})
    m_np = brain.decide(np, theta, o)
    m_jx = jax.jit(lambda th, *fs: brain.decide(jnp, th, brain.PolicyObs(*fs)))(
        jnp.asarray(theta), *[None if v is None else jnp.asarray(v) for v in o])
    assert int(np.asarray(m_np.hold)[8]) == 484
    for f, a, b in zip(m_np._fields, m_np, m_jx):
        assert np.array_equal(np.asarray(a), np.asarray(b)), f
