"""Dump real trajectory PolicyObs to a fixture so the gate needs no simulator."""
import os, sys, functools
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")
import numpy as np, jax, jax.numpy as jnp
from kagg3 import spec
from kagg3.core import brain
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state, prices_of

theta = np.load("artifacts/theta.npy").astype(np.float32)
tables = build_tables(jnp)
hi_t, lo_t = eod.weed_threshold(); hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
thetas = jnp.stack([jnp.asarray(theta)] * 2)
run_day = jax.jit(functools.partial(rollout.run_day, tables))

seeds = [int(s) for s in sys.argv[1].split(",")]
cols = {f: [] for f in brain.PolicyObs._fields}
for seed in seeds:
    st = initial_state(jnp)
    for d in range(spec.N_DAYS):
        price = prices_of(jnp, tables, st.mkt_inv)
        for p in (0, 1):
            o = rollout.policy_obs(st, p, jnp.int32(d), price)
            for f, v in zip(o._fields, o):
                cols[f].append(np.asarray(v))
        st = run_day(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)),
                     hi_t, lo_t, thetas)

out = {f: np.stack(v) for f, v in cols.items()}
np.savez_compressed(sys.argv[2], **out)
print("wrote", sys.argv[2], "decisions:", len(out["day"]))
