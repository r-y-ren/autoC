"""The global head's product residual (`policy.SHAPES`' `gp`).

The head used to see `glob_feat` and nothing else -- `gh = tanh(glob_feat @ g1
+ gb1)` -- so dev_frac, animal_share, the plant-mix sharpness, the land bias,
the saturation gate, the hire bias and the crew ramp all had to be the same
number on two boards whose per-product markets differed however sharply, as
long as the 24 global summaries agreed. `gp` reads the flattened per-product
summary (grow, sell, press) x 9 onto the global hidden width and adds it to
that pre-activation.

Three groups, the same three every appended block here has to pass:

* the layout: an append at the tail, nothing before it moved;
* the identity: at zero the block is inert *against the expression that was
  there before it*, which is written out longhand below rather than compared
  against itself, and a padded theta decides every recorded observation exactly
  as the short one does;
* numpy vs JAX, with the block trained off zero -- the trainer runs one backend
  and the submission the other, and every decoded quantity is a `floor` away
  from a different move.
"""
import os
import pathlib
import sys

import numpy as np
import pytest

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO

FIXTURE = ROOT / "tests" / "data" / "trajectory_obs.npz"
THETA = ROOT / "artifacts" / "theta.npy"

#: The layout `gp` appends to.
PRE_GP_N = 5508


# ------------------------------------------------------------------ layout

def test_layout_is_an_append():
    assert PO.N_PROD_SUMMARY == spec.N_PRODUCTS * (PO.N_ENC_OUT + 1) == 27
    assert PO.offset("gp") == PRE_GP_N, "gp must start where the old layout ended"
    # The block's own end, not `N_PARAMS`: `g11`/`gb11` (2026-09-09) has since
    # been appended past it, and pinning the tail here would fail every later
    # append by construction.
    assert PO.offset("gp") + PO.N_PROD_SUMMARY * PO.N_HEAD_HID == 6372
    names = [n for n, _ in PO.SHAPES]
    assert names[names.index("fs") + 1] == "gp"
    # No bias block: `gb1` is already the bias on this pre-activation.
    assert "gbp" not in dict(PO.SHAPES)
    # Every new coordinate is live -- `gp` feeds `gh`, and `gh` feeds outputs
    # `brain.decide` reads.
    assert PO.live_mask()[PO.offset("gp"):].all()


def test_pad_zero_extends_and_keeps_the_prefix():
    rng = np.random.default_rng(1)
    old = rng.normal(0.0, 0.3, PRE_GP_N).astype(np.float32)
    new = PO.pad(old)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:PRE_GP_N], old)
    assert not new[PO.offset("gp"):].any()


# ---------------------------------------------------------------- identity

def _inputs(seed):
    rng = np.random.default_rng(seed)
    return (rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_PROD_FEAT)).astype(np.float32),
            rng.normal(0.0, 1.0, PO.N_GLOBAL_FEAT).astype(np.float32),
            rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_DRAIN_FEAT)).astype(np.float32),
            rng.normal(0.0, 1.0, (spec.N_PRODUCTS, PO.N_FCAST_FEAT)).astype(np.float32))


def _forward_pre_gp(p, prod, glob, drain, fcast):
    """`policy.forward` as it stood at 5,508 parameters, written out longhand.

    Comparing the new `forward` against itself with a zero block would prove
    nothing about the *expression*; this is the expression the champion was
    trained under.
    """
    x = np.concatenate([prod, np.broadcast_to(glob, (spec.N_PRODUCTS,
                                                     PO.N_GLOBAL_FEAT))], axis=1)
    pre = (x @ p.w1 + p.b1) + drain @ p.dh
    h = np.tanh(pre + fcast @ p.fh)
    scores = (h @ p.w2 + p.b2) + drain @ p.ds + fcast @ p.fs
    gh = np.tanh(glob @ p.g1 + p.gb1)
    crew = gh @ p.g8 + p.gb8
    return PO.Outputs(scores=scores, head=gh @ p.g2 + p.gb2, prio=gh @ p.g3 + p.gb3,
                      gate=(h @ p.w3 + p.b3)[:, 0], lots=(gh @ p.g4 + p.gb4)[0],
                      aux=gh @ p.g5 + p.gb5, dev=gh @ p.g6 + p.gb6,
                      sat=(gh @ p.g7 + p.gb7)[0], crew=crew,
                      hire=np.concatenate([crew[:1], gh @ p.g9 + p.gb9]),
                      ramp=gh @ p.g10 + p.gb10,
                      # Not `gh @ p.g11 + p.gb11`: this helper is the 5,508
                      # expression, and `g11` is zero in every theta it is
                      # handed, so the horizon logit it emitted was 0.0.
                      fwd=np.float32(0.0), crop_mix=np.zeros(spec.N_CROPS, np.float32))


@pytest.mark.parametrize("seed", range(8))
def test_padded_theta_reproduces_the_old_forward_exactly(seed):
    """(i) A 5,508 theta padded to `N_PARAMS` computes, bit for bit, what the
    pre-`gp` forward computed from the same inputs."""
    rng = np.random.default_rng(100 + seed)
    old = rng.normal(0.0, 0.3, PRE_GP_N).astype(np.float32)
    prod, glob, drain, fcast = _inputs(seed)
    p = PO.unpack(np, PO.pad(old))
    got = PO.forward(np, p, prod, glob, drain, fcast)
    want = _forward_pre_gp(p, prod, glob, drain, fcast)
    for f, a, b in zip(got._fields, got, want):
        assert np.array_equal(np.asarray(a), np.asarray(b)), f


def test_a_nonzero_residual_moves_the_global_outputs_only():
    """(ii) Off zero the block changes every head output -- and *only* those:
    the residual is downstream of the encoder, so the per-product scores and
    the timing pressure must not move."""
    rng = np.random.default_rng(4)
    old = rng.normal(0.0, 0.3, PRE_GP_N).astype(np.float32)
    prod, glob, drain, fcast = _inputs(3)
    base = PO.forward(np, PO.unpack(np, PO.pad(old)), prod, glob, drain, fcast)

    theta = PO.pad(old)
    theta[PO.offset("gp"):PO.offset("g11")] = rng.normal(0.0, 0.1, PO.N_PROD_SUMMARY * PO.N_HEAD_HID)
    got = PO.forward(np, PO.unpack(np, theta), prod, glob, drain, fcast)

    for f in ("scores", "gate"):
        assert np.array_equal(np.asarray(getattr(got, f)),
                              np.asarray(getattr(base, f))), f
    for f in ("head", "prio", "lots", "aux", "dev", "sat", "crew", "hire", "ramp"):
        assert not np.array_equal(np.asarray(getattr(got, f)),
                                  np.asarray(getattr(base, f))), f


def test_the_residual_reads_the_product_market_the_head_could_not_see():
    """The point of the block: two states whose `glob_feat` is identical and
    whose per-product markets differ now decode different global outputs."""
    rng = np.random.default_rng(9)
    theta = PO.pad(rng.normal(0.0, 0.3, PRE_GP_N).astype(np.float32))
    prod_a, glob, drain, fcast = _inputs(11)
    prod_b = prod_a[::-1].copy()          # same global summaries, permuted market

    for scale, want_same in ((0.0, True), (0.05, False)):
        theta[PO.offset("gp"):PO.offset("g11")] = rng.normal(0.0, 1.0, PO.N_PROD_SUMMARY
                                             * PO.N_HEAD_HID) * scale
        p = PO.unpack(np, theta)
        a = PO.forward(np, p, prod_a, glob, drain, fcast)
        b = PO.forward(np, p, prod_b, glob, drain, fcast)
        same = np.array_equal(np.asarray(a.head), np.asarray(b.head))
        assert same is want_same, f"scale {scale}: head same={same}"


@pytest.mark.skipif(not FIXTURE.is_file(), reason="needs the trajectory fixture")
def test_upgraded_theta_decides_identically():
    """`scripts/upgrade_theta.py`'s pad changes no decision, on every recorded
    observation in the fixture."""
    if not THETA.is_file():
        pytest.skip("needs a trained theta")
    old = np.load(THETA).astype(np.float32)
    assert old.shape[0] < PO.N_PARAMS, "this theta already carries the block"
    new = PO.pad(old)
    assert not new[PO.offset("gp"):].any(), "the appended block must be zeros"

    d = np.load(FIXTURE)
    present = [f for f in brain.PolicyObs._fields if f in d.files]
    n = len(d["day"])
    assert n >= 1000, f"fixture too small to be meaningful: {n}"
    bad = []
    for i in range(n):
        o = brain.PolicyObs(**{f: d[f][i] for f in present})
        a, b = brain.decide(np, old, o), brain.decide(np, new, o)
        for f, x, y in zip(a._fields, a, b):
            if not np.array_equal(np.asarray(x), np.asarray(y)):
                bad.append(f"decision {i}: {f}")
    assert not bad, f"{len(bad)} of {n} decisions moved:\n" + "\n".join(bad[:10])


# ------------------------------------------------------- backend agreement

def test_numpy_matches_jax_with_a_trained_residual():
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401  pins matmul precision at import

    rng = np.random.default_rng(21)
    theta = PO.pad(rng.normal(0.0, 0.3, PRE_GP_N).astype(np.float32))
    theta[PO.offset("gp"):PO.offset("g11")] = rng.normal(0.0, 0.1, PO.N_PROD_SUMMARY * PO.N_HEAD_HID)
    theta = theta.astype(np.float32)

    jf = jax.jit(lambda th, *fs: PO.forward(jnp, PO.unpack(jnp, th), *fs))
    jt = jnp.asarray(theta)
    p = PO.unpack(np, theta)
    worst = 0.0
    for seed in range(12):
        fs = _inputs(seed)
        a = PO.forward(np, p, *fs)
        b = jf(jt, *[jnp.asarray(f) for f in fs])
        for f, x, y in zip(a._fields, a, b):
            worst = max(worst, float(np.abs(np.asarray(x) - np.asarray(y)).max()))
    assert worst < 1e-5, f"numpy and JAX disagree by {worst}"


@pytest.mark.skipif(not FIXTURE.is_file(), reason="needs the trajectory fixture")
def test_numpy_matches_jax_on_the_decision_with_a_trained_residual():
    """The residual reaching a decision -- the integer cliffs are what this is
    for, and every head output it moves is floored to one."""
    import jax
    import jax.numpy as jnp
    from kagg3 import precision  # noqa: F401

    rng = np.random.default_rng(31)
    theta = PO.pad(np.load(THETA).astype(np.float32))
    theta[PO.offset("gp"):PO.offset("g11")] = rng.normal(0.0, 0.05, PO.N_PROD_SUMMARY
                                         * PO.N_HEAD_HID).astype(np.float32)
    theta = theta.astype(np.float32)

    d = np.load(FIXTURE)
    present = [f for f in brain.PolicyObs._fields if f in d.files]
    jd = jax.jit(lambda th, *fs: brain.decide(jnp, th, brain.PolicyObs(*fs)))
    jt = jnp.asarray(theta)
    bad = []
    for i in range(0, len(d["day"]), 37):
        o = brain.PolicyObs(**{f: d[f][i] for f in present})
        a = brain.decide(np, theta, o)
        b = jd(jt, *[None if v is None else jnp.asarray(v) for v in o])
        for f, x, y in zip(a._fields, a, b):
            if not np.array_equal(np.asarray(x), np.asarray(y)):
                bad.append(f"decision {i}: {f} numpy={np.asarray(x)} jax={np.asarray(y)}")
    assert not bad, "\n".join(bad[:10])
