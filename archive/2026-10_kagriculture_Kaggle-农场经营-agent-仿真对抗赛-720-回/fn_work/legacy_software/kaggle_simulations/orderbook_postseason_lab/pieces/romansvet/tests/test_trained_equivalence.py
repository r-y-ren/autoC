"""Gate 1, run against the theta that is actually about to ship.

`test_sim_equivalence.py` uses random weights, which barely develop the farm. A
trained policy buys all four quadrants, fills the board with animals, overflows
the shed and drives products to the $1 price floor -- so it reaches code paths
random weights never touch. Since `scripts/submit.py` runs the suite as its
pre-flight, this is what makes the exactness claim cover the shipped weights
rather than an arbitrary point in parameter space.
"""
import functools
import os
import sys

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.dirname(__file__))

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from kaggle_environments import make

from kagg3 import spec
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state
from test_sim_equivalence import _engine, _sim, agent_for

THETA = os.path.join(ROOT, "artifacts", "theta.npy")


@pytest.mark.parametrize("seed", [20260821, 123456])
def test_trained_policy_matches_engine(seed):
    if not os.path.exists(THETA):
        pytest.skip("no trained theta yet")
    theta = np.load(THETA).astype(np.float32)

    tables = build_tables(jnp)
    hi_t, lo_t = eod.weed_threshold()
    hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
    thetas = jnp.stack([jnp.asarray(theta)] * 2)
    run_day = jax.jit(functools.partial(rollout.run_day, tables))
    run_last = jax.jit(functools.partial(rollout.run_day, tables,
                                         n_turns=spec.TURNS_PER_DAY - 1, do_eod=False))

    env = make("kaggriculture", configuration={"seed": seed})
    env.run([agent_for(theta), agent_for(theta)])

    st = initial_state(jnp)
    for d in range(spec.N_DAYS):
        f = run_last if d == spec.N_DAYS - 1 else run_day
        st = f(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)), hi_t, lo_t, thetas)
        e, s = _engine(env, min((d + 1) * 24, len(env.steps) - 1)), _sim(st)
        for k in s:
            assert np.array_equal(np.asarray(e[k]), np.asarray(s[k])), \
                f"seed {seed} day {d}: field {k} diverged"

    # A trained policy should be developing the farm, not idling -- otherwise
    # this gate would be passing vacuously.
    assert env.steps[-1][0].observation["farms"][0]["money"] > 10_000
