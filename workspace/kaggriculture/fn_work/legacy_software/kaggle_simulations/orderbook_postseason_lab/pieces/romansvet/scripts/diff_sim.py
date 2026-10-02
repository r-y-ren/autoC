"""Step the sim a day at a time and diff EVERY field against the engine."""
import os, sys, functools
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src"); sys.path.insert(0, "scripts")
import numpy as np, jax, jax.numpy as jnp
from kaggle_environments import make
from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import plan as P, policy as PO
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state
from validate_sim import agent_for

FIELDS = ["kind","occ","t_day","t_water","t_cons","t_yield","t_fert","t_cared","t_favail"]

def eng_snapshot(env, step_ix):
    st = env.steps[step_ix]; obs = st[0].observation; farms = obs["farms"]
    out = {"money": np.array([f["money"] for f in farms]),
           "mkt_inv": np.array([obs["market"]["inventory"][n] for n in spec.PRODUCTS]),
           "nquad": np.array([len(f["unlocked_quadrants"]) for f in farms]),
           "nshops": np.array(len(obs["town"]["unlocked_shops"]))}
    inv = np.argsort(P.SERP)
    per = {f: [] for f in FIELDS}
    for p in range(2):
        v = parse.parse_view({**obs, "private": st[p].observation["private"]}, p)
        for f in FIELDS:
            per[f].append(getattr(v, f)[inv])
        out[f"shed{p}"] = v.shed; out[f"seeds{p}"] = v.seeds
    for f in FIELDS: out[f] = np.array(per[f])
    return out

def sim_snapshot(st):
    out = {"money": np.asarray(st.money), "mkt_inv": np.asarray(st.mkt_inv),
           "nquad": np.asarray(st.nquad), "nshops": np.asarray(st.nshops),
           "shed0": np.asarray(st.shed[0]), "shed1": np.asarray(st.shed[1]),
           "seeds0": np.asarray(st.seeds[0]), "seeds1": np.asarray(st.seeds[1])}
    for f in FIELDS: out[f] = np.asarray(getattr(st, f))
    return out

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260821
    theta = PO.init_theta(np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 3))
    tables = build_tables(jnp)
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([agent_for(theta), agent_for(theta)])
    hi_t, lo_t = eod.weed_threshold(); hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
    thetas = jnp.stack([jnp.asarray(theta)]*2)
    run_day = jax.jit(functools.partial(rollout.run_day, tables))
    st = initial_state(jnp)
    run_last = jax.jit(functools.partial(rollout.run_day, tables,
                                         n_turns=spec.TURNS_PER_DAY - 1, do_eod=False))
    for d in range(spec.N_DAYS):
        f = run_last if d == spec.N_DAYS - 1 else run_day
        st = f(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)), hi_t, lo_t, thetas)
        e = eng_snapshot(env, min((d+1)*24, len(env.steps)-1)); s = sim_snapshot(st)
        diffs = [k for k in s if not np.array_equal(np.asarray(e[k]), np.asarray(s[k]))]
        if diffs:
            print(f"day {d}: DIFF in {diffs}")
            for k in diffs:
                ev, sv = np.asarray(e[k]), np.asarray(s[k])
                if ev.ndim <= 1:
                    print(f"   {k}: engine={ev}  sim={sv}")
                else:
                    idx = np.argwhere(ev != sv)
                    print(f"   {k}: {len(idx)} cells differ")
                    for i in idx[:5]:
                        p_, t_ = int(i[0]), int(i[1])
                        ctx = " ".join(f"{f}={e[f][p_][t_]}/{s[f][p_][t_]}" for f in FIELDS)
                        print(f"      p{p_} tile{t_} (x={t_%10},y={t_//10}) "
                              f"engine={ev[tuple(i)]} sim={sv[tuple(i)]}")
                        print(f"         eng/sim all fields: {ctx}")
            break
    else:
        print("EXACT MATCH across all 30 days")
