"""`--train-only` and `--optimizer`: the two flags that stop a champion-seeded
run from random-walking away from the champion it was seeded with.

Adam's per-coordinate normalisation is the mechanism. `mhat / sqrt(vhat)` is
about 1 whether the gradient carried signal or noise, so *every* live
coordinate moves by roughly `lr` every generation, and after G generations the
run sits `lr*sqrt(G)` away from its start in each of 4,056 directions at once.
`--train-only` shrinks the set of directions; `--optimizer sgd` removes the
floor under the step. They are independent, and tested independently here.

No episode is played: the ES step is `Trainer.apply_gradient`, so a synthetic
gradient exercises the whole rule -- moments, bias correction, decoupled decay,
the bias clip and the mask -- in milliseconds.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import numpy as np
import pytest

import jax.numpy as jnp

from kagg3.core import policy as PO
from kagg3.es.train import Config, Trainer, bias_mask, train_mask


# --------------------------------------------------------------- train_mask


def test_all_is_the_run_that_came_before_the_flag():
    for spec in ("all", "", None):
        m = train_mask(spec)
        assert m.shape == (PO.N_PARAMS,) and m.dtype == np.float32
        assert np.all(m == 1.0)


def test_biases_is_exactly_what_bias_mask_marks():
    assert np.array_equal(train_mask("biases"), bias_mask())
    # gb2 (18) + gb5 (3) + gb6 (2), before `live_mask` takes the dead slots.
    assert int(train_mask("biases").sum()) == 23


def test_all_biases_is_every_rank_one_block():
    m = train_mask("all-biases")
    for name, shape in PO.SHAPES:
        off = PO.offset(name)
        block = m[off:off + int(np.prod(shape))]
        want = 1.0 if len(shape) == 1 else 0.0
        assert np.all(block == want), name
    # It is a superset of `biases`, which is the whole point of having both.
    assert np.all(m[train_mask("biases") > 0] == 1.0)


def test_block_names_select_exactly_those_blocks():
    m = train_mask("g8,gb8")
    n = sum(int(np.prod(dict(PO.SHAPES)[k])) for k in ("g8", "gb8"))
    assert int(m.sum()) == n
    off = PO.offset("g8")
    assert np.all(m[off:off + n] == 1.0)
    assert int(m[:off].sum()) == 0 and int(m[off + n:].sum()) == 0


def test_an_unknown_block_name_is_refused_not_silently_trained_empty():
    with pytest.raises(ValueError) as e:
        train_mask("gb2,gb42")
    assert "gb42" in str(e.value)
    with pytest.raises(ValueError):
        train_mask(",")


# ------------------------------------------------- the mask reaches the run


@pytest.fixture(scope="module")
def tiny_cfg():
    return Config(pop=8, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0)


def test_the_trainer_ands_the_subset_into_its_live_mask(tiny_cfg):
    live = PO.live_mask()
    base = Trainer(tiny_cfg, seed=0)
    assert np.array_equal(np.asarray(base.mask), live)
    assert base.n_live == int(live.sum())

    sub = Trainer(tiny_cfg._replace(train_only="biases"), seed=0)
    want = live * bias_mask()
    assert np.array_equal(np.asarray(sub.mask), want)
    # gb2 loses its 13 DEAD_HEAD slots and gb5 its dead aux column: 23 -> 9.
    assert sub.n_live == int(want.sum()) == 9


def test_a_subset_that_is_entirely_dead_is_refused_at_construction(tiny_cfg):
    # `g3`/`gb3` are zeroed wholesale by `live_mask`, so training "only" them
    # would train nothing at all -- an hours-long no-op, refused up front.
    with pytest.raises(ValueError):
        Trainer(tiny_cfg._replace(train_only="g3,gb3"), seed=0)


def test_an_unknown_optimizer_is_refused_at_construction(tiny_cfg):
    with pytest.raises(ValueError):
        Trainer(tiny_cfg._replace(optimizer="rmsprop"), seed=0)


# ------------------------------------------------------------ the step rule
#
# A stub trainer: `apply_gradient` reads `cfg`, `theta`, `mask`, `no_decay`,
# `m`, `v` and `adam_t` and nothing else, so the tests below run on shapes of
# 6 rather than on 4,848 and never touch the simulator.


def _stub(cfg, theta, mask=None, no_decay=None):
    tr = Trainer.__new__(Trainer)
    tr.cfg = cfg
    tr.theta = jnp.asarray(theta, jnp.float32)
    tr.n = tr.theta.shape[0]
    tr.mask = jnp.ones(tr.n) if mask is None else jnp.asarray(mask, jnp.float32)
    tr.no_decay = (jnp.zeros(tr.n) if no_decay is None
                   else jnp.asarray(no_decay, jnp.float32))
    tr.m = jnp.zeros(tr.n)
    tr.v = jnp.zeros(tr.n)
    tr.adam_t = 0
    tr.t = 0
    return tr


def test_train_only_leaves_the_rest_of_theta_bit_identical():
    # The deliverable in one assertion: a masked coordinate is not "nearly"
    # where it started after a few steps, it is *exactly* where it started --
    # no decay, no step, no drift. Six coordinates, two of them trainable.
    theta = np.array([1.0, -2.0, 0.5, 3.0, -0.25, 7.0], np.float32)
    mask = np.array([0, 1, 0, 1, 0, 0], np.float32)
    tr = _stub(Config(lr=0.05, weight_decay=0.01), theta, mask=mask)
    rng = np.random.default_rng(0)
    for _ in range(5):
        tr.apply_gradient(jnp.asarray(rng.normal(size=6).astype(np.float32)))
    out = np.asarray(tr.theta)
    frozen = mask == 0
    assert np.array_equal(out[frozen], theta[frozen])
    # ...and the two live ones did move, or the test would pass on a trainer
    # that had simply stopped working.
    assert np.all(np.abs(out[~frozen] - theta[~frozen]) > 1e-4)


def test_adam_steps_by_about_lr_however_small_the_gradient_is():
    # The failure mode the flags exist for, pinned as a fact: shrink the
    # gradient by 1,000x and Adam takes the same step. This is the baseline the
    # sgd test below is contrasted against.
    theta = np.zeros(4, np.float32)
    steps = []
    for scale in (1.0, 1e-3):
        tr = _stub(Config(lr=0.02, weight_decay=0.0), theta)
        tr.apply_gradient(jnp.full(4, scale, jnp.float32))
        steps.append(float(np.abs(np.asarray(tr.theta)).max()))
    assert steps[0] == pytest.approx(0.02, rel=1e-3)
    assert steps[1] == pytest.approx(steps[0], rel=1e-3)


def test_sgd_scales_its_step_with_the_gradient():
    theta = np.zeros(4, np.float32)
    cfg = Config(lr=0.02, weight_decay=0.0, optimizer="sgd")
    steps = []
    for scale in (1.0, 0.1, 1e-3):
        tr = _stub(cfg, theta)
        tr.apply_gradient(jnp.full(4, scale, jnp.float32))
        steps.append(float(np.abs(np.asarray(tr.theta)).max()))
    # m = (1 - beta1) * grad on the first step, and there is no bias
    # correction and no v: the step is exactly lr * (1 - beta1) * grad.
    assert steps[0] == pytest.approx(0.02 * (1 - cfg.beta1), rel=1e-4)
    assert steps[1] == pytest.approx(steps[0] * 0.1, rel=1e-3)
    assert steps[2] == pytest.approx(steps[0] * 1e-3, rel=1e-3)


def test_sgd_on_a_zero_gradient_moves_theta_by_decay_alone():
    theta = np.array([1.0, -2.0, 4.0], np.float32)
    tr = _stub(Config(lr=0.02, weight_decay=0.01, optimizer="sgd"), theta)
    for _ in range(3):
        tr.apply_gradient(jnp.zeros(3, jnp.float32))
    assert np.asarray(tr.theta) == pytest.approx(theta * 0.99 ** 3, rel=1e-5)
    # And with decay off, a zero gradient is a no-op -- which is precisely what
    # Adam does not give you.
    tr = _stub(Config(lr=0.02, weight_decay=0.0, optimizer="sgd"), theta)
    for _ in range(3):
        tr.apply_gradient(jnp.zeros(3, jnp.float32))
    assert np.asarray(tr.theta) == pytest.approx(theta, rel=1e-6)


def test_sgd_keeps_the_bias_clip_and_the_decay_exemption():
    theta = np.array([100.0, 100.0], np.float32)
    cfg = Config(lr=1.0, weight_decay=0.5, bias_clip=8.0, optimizer="sgd")
    tr = _stub(cfg, theta, no_decay=np.array([1.0, 0.0], np.float32))
    tr.apply_gradient(jnp.zeros(2, jnp.float32))
    out = np.asarray(tr.theta)
    assert out[0] == pytest.approx(8.0)      # clipped, not decayed
    assert out[1] == pytest.approx(50.0)     # decayed, not clipped


def test_the_adam_default_is_the_inline_step_it_replaced():
    # `apply_gradient` was lifted out of `generation`; this is the arithmetic
    # it was lifted from, spelled out again so a change to one fails here.
    cfg = Config(lr=0.02, weight_decay=0.003, bias_clip=8.0)
    theta = np.array([0.4, -1.2, 9.0], np.float32)
    no_decay = np.array([0.0, 0.0, 1.0], np.float32)
    tr = _stub(cfg, theta, no_decay=no_decay)
    rng = np.random.default_rng(7)
    m = np.zeros(3, np.float64)
    v = np.zeros(3, np.float64)
    want = theta.astype(np.float64)
    for t in range(1, 4):
        g = rng.normal(size=3)
        tr.apply_gradient(jnp.asarray(g.astype(np.float32)))
        m = cfg.beta1 * m + (1 - cfg.beta1) * g
        v = cfg.beta2 * v + (1 - cfg.beta2) * g ** 2
        step = want + cfg.lr * (m / (1 - cfg.beta1 ** t)) / (
            np.sqrt(v / (1 - cfg.beta2 ** t)) + cfg.eps_adam)
        want = np.where(no_decay > 0, np.clip(step, -cfg.bias_clip, cfg.bias_clip),
                        (1 - cfg.weight_decay) * step)
    assert np.asarray(tr.theta) == pytest.approx(want, rel=2e-5, abs=2e-6)


def test_a_checkpoint_crosses_between_the_two_optimisers_without_crashing():
    # `--resume` restores `m` and `v` whatever the flag says, so both moments
    # are always present; sgd simply stops reading `v` and leaves it as it
    # found it, and a run switched back to adam picks it up again.
    theta = np.zeros(3, np.float32)
    tr = _stub(Config(lr=0.02, weight_decay=0.0), theta)
    for _ in range(3):
        tr.apply_gradient(jnp.full(3, 0.5, jnp.float32))
    v_adam = np.asarray(tr.v).copy()
    assert np.all(v_adam > 0)

    tr.cfg = tr.cfg._replace(optimizer="sgd")     # resumed under --optimizer sgd
    tr.apply_gradient(jnp.full(3, 0.5, jnp.float32))
    assert np.array_equal(np.asarray(tr.v), v_adam)   # carried, never read
    assert np.all(np.isfinite(np.asarray(tr.theta)))

    tr.cfg = tr.cfg._replace(optimizer="adam")    # ...and back again
    tr.apply_gradient(jnp.full(3, 0.5, jnp.float32))
    assert np.all(np.asarray(tr.v) > v_adam)
    assert np.all(np.isfinite(np.asarray(tr.theta)))
