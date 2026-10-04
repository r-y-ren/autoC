"""Head-to-head win rate of one theta against every member of a saved pool.

Run in the simulator (opponents are policy-driven, so it is exact), both seats
per seed, so this is the same metric ES optimises but measured cleanly.
"""
import os, sys
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")
import numpy as np, jax.numpy as jnp
from kagg3.es.train import cold_starts, host_words, make_evaluator
from kagg3.sim import eod
from kagg3.sim.state import build_tables

if __name__ == "__main__":
    theta = np.load(sys.argv[1]).astype(np.float32)
    pool = np.load(sys.argv[2]).astype(np.float32)
    n_seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 32

    tables = build_tables(jnp)
    hi_t, lo_t = eod.weed_threshold()
    ev = make_evaluator(jnp.int32(hi_t), jnp.int32(lo_t))
    rng = np.random.default_rng(4242)
    seeds = rng.integers(0, 2 ** 31 - 1, n_seeds)
    words = jnp.asarray(host_words(seeds))

    print(f"theta vs {len(pool)} pool members, {n_seeds} seeds x 2 seats")
    for i, opp in enumerate(pool):
        c = jnp.asarray(np.tile(theta, (n_seeds * 2, 1)))
        o = jnp.asarray(np.tile(opp, (n_seeds * 2, 1)))
        w = jnp.concatenate([words, words])
        seat = jnp.asarray(np.concatenate([np.zeros(n_seeds), np.ones(n_seeds)]).astype(np.int32))
        nq, mo = cold_starts(n_seeds * 2)
        r = np.asarray(ev(tables, c, o, w, seat, jnp.asarray(nq), jnp.asarray(mo)))
        print(f"  vs pool[{i}]  win {r.mean()*100:5.1f}%")
