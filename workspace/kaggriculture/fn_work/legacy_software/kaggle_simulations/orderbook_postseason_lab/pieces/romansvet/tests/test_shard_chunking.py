"""The population chunker must schedule every (candidate, seed, seat) exactly once.

`_fitness` flattens pop x episodes into one batch, splits it into device-sized
chunks and pads the last one back up to a full chunk. That is pure index
bookkeeping around the evaluator, and a mistake in it -- a wrong pad value, a
missed trim, a chunk boundary off by one -- would not crash. It would quietly
score candidates against the wrong episodes, which looks exactly like ES failing
to learn.

So the evaluator is stubbed with a function of all four batched inputs and the
result is checked against a plain-numpy reference. Two host devices are forced
so the sharding path is the one under test, and the parameters include chunk
sizes that do not divide the batch.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_FLAGS", "--xla_force_host_platform_device_count=2")
sys.path.insert(0, "src")

import jax.numpy as jnp
import numpy as np
import pytest

from kagg3.es.train import Config, Trainer, batch_mesh


def _stub(tables, th, opp, words, seat, nq, mo):
    return th[:, 0] * 1000.0 + opp[:, 0] * 17.0 + words[:, 0, 0].astype(jnp.float32) + seat * 3.0


@pytest.mark.parametrize("pop,episodes,chunk", [
    (5, 3, 3),        # pad 1
    (7, 5, 5),        # pad 1
    (3, 1, 7),        # pad 3 -- chunk larger than the whole batch
    (5, 7, 3),        # pad 1
    (4, 4, 3),        # pad 0, the unchanged path
    (128, 64, 1024),  # the real training shape
])
def test_chunking_preserves_schedule(pop, episodes, chunk):
    tr = Trainer.__new__(Trainer)          # bypass __init__: no sim, no weights
    tr.cfg = Config(pop=pop, episodes=episodes, chunk=chunk)
    tr.mesh, tr.n_devices = batch_mesh()
    tr.evaluate = _stub

    rng = np.random.default_rng(0)
    thetas = jnp.asarray(rng.normal(size=(pop, 5)).astype(np.float32))
    n_pairs = max(episodes // 2, 1)
    opp = jnp.asarray(rng.normal(size=(n_pairs, 5)).astype(np.float32))
    # Small word values: the stub casts them to float32, and real uint32 words
    # would lose low bits there and make the comparison about rounding.
    words = jnp.asarray(rng.integers(0, 500, size=(n_pairs, 3, 4)).astype(np.uint32))

    got = np.asarray(tr._play(thetas, words, opp, None))

    ref = np.zeros((pop, episodes))
    for c in range(pop):
        for e in range(episodes):
            p, s = e // 2, e % 2
            ref[c, e] = (float(thetas[c, 0]) * 1000.0 + float(opp[p, 0]) * 17.0
                         + float(words[p, 0, 0]) + s * 3.0)

    assert np.allclose(got, ref, rtol=0, atol=1e-3)
