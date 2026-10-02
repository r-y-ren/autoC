import os, sys, time
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE","false")
sys.path.insert(0,"src")
import numpy as np, jax, jax.numpy as jnp
from kagg3 import spec
from kagg3.core import policy as PO
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables

tables = build_tables(jnp)
hi_t, lo_t = eod.weed_threshold(); hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)

def one(thetas, words):
    money, _, _ = rollout.episode(tables, thetas, words, hi_t, lo_t)
    return money

batched = jax.jit(jax.vmap(one))
rng = np.random.default_rng(0)

for B in [int(x) for x in (sys.argv[1:] or ["64","256","1024"])]:
    th = jnp.asarray(np.stack([np.stack([PO.init_theta(rng), PO.init_theta(rng)]) for _ in range(B)]))
    seeds = rng.integers(0, 2**31-1, B)
    w = jnp.asarray(np.stack([np.stack([eod.host_stream(int(s), d) for d in range(spec.N_DAYS)]) for s in seeds]))
    t0 = time.time(); out = batched(th, w); out.block_until_ready(); t1 = time.time()
    t2 = time.time(); out = batched(th, w); out.block_until_ready(); t3 = time.time()
    steps = B * spec.EPISODE_STEPS
    print(f"B={B:5d}  compile+run {t1-t0:6.1f}s   run {t3-t2:6.2f}s   "
          f"{B/(t3-t2):8.1f} eps/s   {steps/(t3-t2)/1e6:6.2f} M turn-steps/s")
