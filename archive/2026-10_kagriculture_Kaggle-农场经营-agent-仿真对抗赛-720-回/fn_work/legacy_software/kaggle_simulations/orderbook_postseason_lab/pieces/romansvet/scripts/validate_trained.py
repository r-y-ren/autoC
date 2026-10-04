"""Gate 1 against a *trained* policy.

Random weights barely develop the farm; a trained one buys all four quadrants,
runs a full board of animals, overflows the shed and drives products to the $1
floor. Those are exactly the paths where a port diverges, so the exactness gate
is far stronger here than with random theta.
"""
import functools, os, sys
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src"); sys.path.insert(0, "tests")
import numpy as np, jax, jax.numpy as jnp
from kaggle_environments import make
from kagg3 import spec
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state
from test_sim_equivalence import agent_for, _engine, _sim

if __name__ == "__main__":
    theta = np.load(sys.argv[1] if len(sys.argv) > 1 else "artifacts/theta.npy").astype(np.float32)
    seeds = [int(x) for x in (sys.argv[2:] or [20260821, 7, 123456, 999])]
    tables = build_tables(jnp)
    hi_t, lo_t = eod.weed_threshold(); hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
    thetas = jnp.stack([jnp.asarray(theta)] * 2)
    run_day = jax.jit(functools.partial(rollout.run_day, tables))
    run_last = jax.jit(functools.partial(rollout.run_day, tables,
                                         n_turns=spec.TURNS_PER_DAY - 1, do_eod=False))
    ok = True
    for seed in seeds:
        env = make("kaggriculture", configuration={"seed": seed})
        env.run([agent_for(theta), agent_for(theta)])
        st = initial_state(jnp)
        bad = None
        for d in range(spec.N_DAYS):
            f = run_last if d == spec.N_DAYS - 1 else run_day
            st = f(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)), hi_t, lo_t, thetas)
            e, s = _engine(env, min((d + 1) * 24, len(env.steps) - 1)), _sim(st)
            diff = [k for k in s if not np.array_equal(np.asarray(e[k]), np.asarray(s[k]))]
            if diff:
                bad = (d, diff); break
        money = [f["money"] for f in env.steps[-1][0].observation["farms"]]
        if bad:
            ok = False
            print(f"seed {seed}: DIVERGED day {bad[0]} fields {bad[1]}")
        else:
            print(f"seed {seed}: exact for all 30 days   (final coins {money[0]:.0f})")
    print("TRAINED-POLICY GATE:", "PASS" if ok else "FAIL")
