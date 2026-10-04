"""Gate 2, on real trajectory observations rather than synthetic ones.

`test_gates.py::test_numpy_matches_jax_policy` compares the same decoded Macro,
but draws random weights and a synthetic board. That combination cannot find the
bug this file exists for. A random theta's sigmoids sit near 0.5 and a synthetic
shed is small, so `sigmoid * count` almost never lands near an integer. A trained
theta saturates its sigmoids and overflows the shed, which is precisely when the
product sits on a floor boundary and the two backends can disagree.

The failure this pins down: JAX on Ampere lowers float32 matmuls to TF32 tensor
cores by default, putting the policy's forward pass ~3.5e-3 away from numpy's.
Every quantity in `core/brain.py` is `floor(continuous * integer_count)`, so that
gap decides between N and N-1. Rare per decision, near-certain across a season --
the shipped agent would play moves the trained agent never would.

Two defences, and the test covers both because either alone is insufficient:
`kagg3.precision` pins JAX to true float32 (3.5e-3 -> ~2e-6), and
`brain.QUANT_EPS` snaps a product that is mathematically an exact integer onto
the right side. Widening the epsilon alone would only relocate the cliff.

Observations come from a fixture (40 seeds x 30 days x 2 seats) so the gate needs
no simulator and no GPU time; regenerate with scripts/collect_trajectory_obs.py.
"""
import os
import sys
import pathlib

import numpy as np
import pytest

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3 import precision  # noqa: F401  pins matmul precision at import
from kagg3.core import brain

FIXTURE = ROOT / "tests" / "data" / "trajectory_obs.npz"
THETA = ROOT / "artifacts" / "theta.npy"
INCUMBENT_B = ROOT / "artifacts" / "kagg2_games" / "thetas" / "flow193_g100_hr.npy"

pytestmark = pytest.mark.skipif(not FIXTURE.is_file(), reason="needs the trajectory fixture")


def _load():
    d = np.load(FIXTURE)
    # `trajectory_obs.npz` predates `PolicyObs`' opponent-clock fields, so build by
    # keyword over what the fixture carries and let the rest take their defaults.
    return [brain.PolicyObs(**{f: d[f][i] for f in brain.PolicyObs._fields
                               if f in d.files})
            for i in range(len(d["day"]))]


def test_matmul_precision_is_pinned():
    """The epsilon cannot carry this alone -- if the precision pin is dropped the
    gap goes back to ~3.5e-3, which no sane epsilon absorbs."""
    import jax
    assert jax.config.jax_default_matmul_precision == "highest"


@pytest.mark.parametrize("theta_path,variant", [
    pytest.param(THETA, "native", id="legacy", marks=pytest.mark.skipif(
        not THETA.is_file(), reason="needs the legacy trained theta")),
    pytest.param(INCUMBENT_B, "native", id="incumbent_b", marks=pytest.mark.skipif(
        not INCUMBENT_B.is_file(), reason="needs the incumbent B theta")),
    pytest.param(INCUMBENT_B, "padded", id="incumbent_b_padded", marks=pytest.mark.skipif(
        not INCUMBENT_B.is_file(), reason="needs the incumbent B theta")),
    pytest.param(INCUMBENT_B, "crop_mix", id="incumbent_b_crop_mix", marks=pytest.mark.skipif(
        not INCUMBENT_B.is_file(), reason="needs the incumbent B theta")),
])
def test_numpy_and_jax_agree_on_trajectory_observations(theta_path, variant):
    import jax
    import jax.numpy as jnp
    from kagg3.core import policy

    theta = np.load(theta_path).astype(np.float32)
    old = theta
    if variant != "native":
        theta = policy.pad(theta)
    if variant == "crop_mix":
        theta[policy.offset("cm"):] = np.random.default_rng(82).normal(
            0, 0.5, policy.N_PARAMS - policy.offset("cm"))
    obs = _load()
    assert len(obs) >= 1000, f"fixture too small to be meaningful: {len(obs)}"

    jdecide = jax.jit(lambda th, *fields:
                      brain.decide(jnp, th, brain.PolicyObs(*fields)))
    jtheta = jnp.asarray(theta)

    bad = []
    for i, o in enumerate(obs):
        m_np = brain.decide(np, theta, o)
        m_jx = jdecide(jtheta, *[None if v is None else jnp.asarray(v) for v in o])
        if variant == "padded":
            m_old = jdecide(jnp.asarray(old),
                           *[None if v is None else jnp.asarray(v) for v in o])
            for f, a, b in zip(m_jx._fields, m_old, m_jx):
                if not np.array_equal(np.asarray(a), np.asarray(b)):
                    bad.append(f"decision {i}: zero padding changed {f}")
        for f, a, b in zip(m_np._fields, m_np, m_jx):
            if not np.array_equal(np.asarray(a), np.asarray(b)):
                bad.append(f"decision {i}: {f} numpy={np.asarray(a)} jax={np.asarray(b)}")
    assert not bad, (
        f"{len(bad)} of {len(obs)} decisions disagree between backends:\n"
        + "\n".join(bad[:10]))
