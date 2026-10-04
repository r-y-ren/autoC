"""`plan.CARE_FILL_ON` in the sim: a seeded, fed 8 COW + 4 SHEEP herd, off vs on.

The in-sim half of `docs/spikes/2026-09-04-care-fill.md`. It runs the same
seeded state through `sim/rollout.run_day` twice -- switch off, switch on --
and reports the CARE ops the plan emits, the milk and wool the engine's own
`refresh_animals` actually banks, and the coins at the end.

`run_day` is called with `do_eod=False` and `sim/eod.end_of_day` is split out
after it, so production can be read straight off the `t_yield` delta the eod
writes rather than inferred from a shed the day's sales have already drained.

The market is set to the census's crossover -- WHEAT 9000 (quote 57), MILK
10060 (34), WOOL 10040 (107) -- so `care_pays` (`price[product] >
price[WHEAT]`) refuses every cow and admits every sheep. That is the
fed-but-uncared animal-day the loss autopsy of ep 105393487 counts, and it is
the population this switch exists for.

    python scripts/care_fill_scenario.py          # the 4-day window
    CF_DAYS=6 python scripts/care_fill_scenario.py

Four days is the window the spike reports for the *ops*; the cares taken on
the last fed day of a window bank at that night's eod and cash at the fire two
days later, so six days is what it takes for the units to show up.
"""
import os, sys
os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")
import numpy as np
import jax.numpy as jnp
from kagg3 import spec
from kagg3.core import brain, ops as O, plan as P, policy as PO
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state, prices_of

SEED = 4041
DAYS = int(os.environ.get("CF_DAYS", "4"))
START_DAY = 10
#: milk 34 and wool 107 against wheat 57: `care_pays` (`price[product] >
#: price[WHEAT]`) refuses every cow and admits every sheep, which is the
#: census case the loss autopsy names -- fed animals the day will not care.
INV = {spec.I_WHEAT: 9000, spec.I_MILK: 10060, spec.I_WOOL: 10040}


def herd_state():
    st = initial_state(jnp, nquad=jnp.asarray([4, 4], jnp.int32),
                       money=jnp.asarray([8000, 8000], jnp.int32))
    serp = np.asarray(P.SERP)
    kind = np.asarray(st.kind).copy()
    occ = np.asarray(st.occ).copy()
    t_day = np.asarray(st.t_day).copy()
    t_cons = np.asarray(st.t_cons).copy()
    shed = np.asarray(st.shed).copy()
    mkt = np.asarray(st.mkt_inv).copy()
    for i, a in enumerate([1] * 8 + [2] * 4):          # 8 COW + 4 SHEEP
        tile = int(serp[i])
        kind[0, tile] = spec.ANIMAL_STRUCT[a]
        occ[0, tile] = a
        t_day[0, tile] = 1
        t_cons[0, tile] = 1                            # one night hungry: must_feed
    shed[0, spec.I_WHEAT] = 300
    for i, v in INV.items():
        mkt[i] = v
    return st._replace(kind=jnp.asarray(kind), occ=jnp.asarray(occ),
                       t_day=jnp.asarray(t_day), t_cons=jnp.asarray(t_cons),
                       shed=jnp.asarray(shed), mkt_inv=jnp.asarray(mkt),
                       nhands=jnp.asarray([6, 0], jnp.int32))


def run(on):
    P.CARE_FILL_ON = on
    tables = build_tables(jnp)
    theta = jnp.asarray(PO.init_theta(np.random.default_rng(SEED)))
    thetas = jnp.stack([theta, theta])
    words = jnp.asarray(np.stack([eod.host_stream(SEED, d)
                                  for d in range(spec.N_DAYS)]))
    z = jnp.int32(0)
    st = herd_state()
    cares = produced = 0
    for d in range(START_DAY, START_DAY + DAYS):
        day = jnp.int32(d)
        price = prices_of(jnp, tables, st.mkt_inv)
        built = P.build_day(jnp, rollout.day_view(st, 0, day, price),
                            brain.decide(jnp, theta,
                                         rollout.policy_obs(st, 0, day, price)),
                            tables.price)
        cares += int((np.asarray(built[0]) == O.OP_CARE).sum())
        pre = rollout.run_day(tables, st, day, words[d], z, z, thetas,
                              do_eod=False)
        occ0 = np.asarray(pre.occ)[0]
        y0 = np.asarray(pre.t_yield)[0]
        st = eod.end_of_day(jnp, pre, day, words[d], z, z)
        y1 = np.asarray(st.t_yield)[0]
        live = (occ0 >= 0) & ((np.asarray(pre.kind)[0] == spec.KIND_COOP)
                              | (np.asarray(pre.kind)[0] == spec.KIND_PASTURE))
        produced += int(np.maximum(y1 - y0, 0)[live].sum())
    return cares, produced, int(np.asarray(st.money)[0])


off = run(False)
on = run(True)
P.CARE_FILL_ON = False
print("             cares  produced  money")
print("OFF         ", off)
print("ON          ", on)
print("N (extra CARE ops)          =", on[0] - off[0])
print("M (extra milk/wool units)   =", on[1] - off[1])
print("coins                       =", on[2] - off[2])
