"""Release gate 1: the JAX simulator must reproduce kaggle_environments exactly.

Runs the same theta in both seats, in both the reference engine and the sim, on
the same episode seed, and compares the per-day money trajectory.
"""
import os, sys, time
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

import numpy as np
import jax.numpy as jnp
from kaggle_environments import make

from kagg3 import spec
from kagg3.agent import runtime, parse
from kagg3.core import brain, policy as PO
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables


def agent_for(theta):
    def f(obs, player, view):
        farm_o = obs["farms"][1 - player]
        vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
        po = brain.PolicyObs(
            day=np.int32(view.day), money=view.money,
            opp_money=np.int32(farm_o["money"]),
            kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
            t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
            nquad=view.nquad, opp_nquad=np.int32(len(farm_o["unlocked_quadrants"])),
            mkt_inv=parse.parse_market(obs)[0], price=view.price,
            shops=parse.parse_town(obs),
            opp_t_day=vo.t_day, opp_t_yield=vo.t_yield)
        return brain.decide(np, theta, po)
    return runtime.make_agent(f)


def engine_daily(theta, seed):
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([agent_for(theta), agent_for(theta)])
    out = []
    for d in range(spec.N_DAYS):
        obs = env.steps[min(d * 24 + 24, len(env.steps) - 1)][0].observation
        out.append([f["money"] for f in obs["farms"]])
    return np.array(out), env


def sim_daily(theta, seed, tables):
    words = np.stack([eod.host_stream(seed, d) for d in range(spec.N_DAYS)])
    hi_t, lo_t = eod.weed_threshold()
    thetas = jnp.stack([jnp.asarray(theta), jnp.asarray(theta)])
    money, daily, st = rollout.episode(tables, thetas, jnp.asarray(words),
                                       jnp.int32(hi_t), jnp.int32(lo_t))
    return np.asarray(daily), st


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260821
    rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    theta = PO.init_theta(rng)
    tables = build_tables(jnp)

    t0 = time.time()
    eng, env = engine_daily(theta, seed)
    t1 = time.time()
    sim, st = sim_daily(theta, seed, tables)
    t2 = time.time()
    print(f"engine {t1-t0:.1f}s   sim {t2-t1:.1f}s")

    print(" day |    engine p0 |       sim p0 |    engine p1 |       sim p1")
    bad = None
    for d in range(spec.N_DAYS):
        mark = "" if np.array_equal(eng[d], sim[d]) else "  <-- MISMATCH"
        if mark and bad is None:
            bad = d
        if d < 8 or mark or d >= spec.N_DAYS - 2:
            print(f" {d:3d} | {eng[d,0]:12.0f} | {sim[d,0]:12.0f} | "
                  f"{eng[d,1]:12.0f} | {sim[d,1]:12.0f}{mark}")
    print("first divergence:", bad if bad is not None else "NONE - exact match")
