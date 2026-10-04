"""Regression: the three animal lanes must not be built lane by lane.

`budget` grew to ten lists on 2026-08-26 (the mixed herd) and with them came
three-lane vectors -- what the BUY row's shed-room clamp grants per kind, what
the standing structures take, what gets built -- each assembled by an unrolled
Python loop over the kinds and a closing `xp.stack`. A stack of three
*different* expression chains lowers to an XLA `concatenate`, and when that
concatenate lands inside a vectorised elementwise fusion the sm_86 tile
emitter turns it into an `scf.if` on the lane index whose branches it then
fails to widen:

    error: loc("min.4155.1"): 'scf.if' op along control flow edge from
    Operation scf.yield to parent: successor operand type #0
    'tensor<1x1xi32>' should match successor input type #0 'tensor<4x1xi32>'

jaxlib 0.10.2, RTX 3090 (sm_86), driver 580.126.20, with no flag to fall back
to the older emitter. It is a codegen failure, not a numerical one: the whole
tree compiles on CPU and passes every gate there, and the GPU refuses the
module outright at `Trainer.__init__`'s archetype probe -- which is the first
thing a training run does. `plan._share` builds the three lanes with one
expression instead, so the fusion stays uniform.

The batch of 64 is the probe's own shape (8 archetypes x 4 seeds x 2 seats)
and it is what decides the 4-wide tile, so it is load-bearing here. Nothing
below this line runs without a GPU, and a smaller unit -- a vmapped
`build_day`, or `budget.grant` on its own -- does *not* reproduce it: the bad
fusion only forms inside the day scan.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

#: The archetype probe's batch: 8 rungs x PROBE_PAIRS seeds x 2 seats.
BATCH = 64


def _gpu_or_skip():
    jax = pytest.importorskip("jax")
    if not any(d.platform == "gpu" for d in jax.devices()):
        pytest.skip("no GPU device; this is a codegen gate, not a numerics one")


def test_a_batch_of_64_episodes_compiles_on_gpu():
    _gpu_or_skip()
    import jax.numpy as jnp

    from kagg3 import spec
    from kagg3.core import policy as PO
    from kagg3.es.train import cold_starts, host_words, make_evaluator
    from kagg3.sim import eod
    from kagg3.sim.state import build_tables

    hi_t, lo_t = eod.weed_threshold()
    evaluate = make_evaluator(jnp.int32(hi_t), jnp.int32(lo_t))
    words = jnp.asarray(host_words(np.arange(4)))
    nquad, money = cold_starts(BATCH)
    zero = jnp.zeros((BATCH, PO.N_PARAMS), jnp.float32)
    out = np.asarray(evaluate(
        build_tables(jnp), zero, zero,
        words[jnp.asarray(np.arange(BATCH) % 4)],
        jnp.asarray((np.arange(BATCH) % 2).astype(np.int32)),
        jnp.asarray(nquad), jnp.asarray(money)))
    assert out.shape == (BATCH, 2)
    # Not just "it compiled": the kernel has to have run the season. Seat and
    # seed both cycle with period 4 across the batch, so every block of four
    # rows is the same four games, and a season that never developed the farm
    # would not clear the engine's own starting purse.
    assert np.array_equal(out[:4], out[4:8]) and np.array_equal(out[:4], out[-4:])
    assert (out > spec.STARTING_MONEY).all(), out
