"""DROP in `sim/units.py` against the real engine, on a scripted turn sequence.

The engine's DROP (`kaggriculture.py:343-356`) is shed-adjacent-only, dumps the
unit's **entire** inventory, obeys `shedCapacity` at drop time and **destroys**
the overflow. Units act before the same turn's market, so a harvest -> walk ->
DROP -> SELL chain completes inside one day -- which is what makes day 29
playable at all (`ops.LAST_SHED_DAY`).

Both backends are installed from one scenario dict and stepped with the same
hand-written script, then compared field by field after every turn. Nothing here
goes through the planner: the point is the mechanic, not the policy.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import jax.numpy as jnp
import numpy as np
import pytest
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as REF

from kagg3 import spec
from kagg3.agent import render
from kagg3.core import ops as O
from kagg3.sim import market, rollout
from kagg3.sim.state import build_tables, initial_state
from kagg3.sim.units import apply_units

BOARD = spec.BOARD
ITEMS = list(spec.ITEMS)
MU = spec.MAX_UNITS
MO = spec.MAX_MARKET_ORDERS
TPD = spec.TURNS_PER_DAY

# Far past every plant we install, so `decay_plants` never ticks a yield down
# under us; the scenarios below are about the shed, not about lifespans.
LONG_LIFE = 100_000


def _xy(tile):
    return tile % BOARD, tile // BOARD


class Scenario:
    """One board, installed identically in the engine and the simulator.

    `plants` maps a row-major tile id to (crop name, yield_units). `upos` is the
    unit positions in engine order (index 0 is the farmer). Seat 0 only -- seat 1
    stays on the engine's day-0 default and passes all game.
    """

    def __init__(self, plants, upos, shed=(), money=3000, planted_day=-12):
        self.plants = dict(plants)
        self.upos = list(upos)
        self.shed = dict(shed)
        self.money = money
        self.planted_day = planted_day

    # --- engine ---------------------------------------------------------
    def install_engine(self, env):
        obs = env.state[0].observation
        farm = obs["farms"][0]
        farm["money"] = float(self.money)
        farm["unlocked_quadrants"] = ["NW", "NE", "SW", "SE"]
        farm["tiles"] = [[None] * BOARD for _ in range(BOARD)]
        for tile, (crop, yld) in self.plants.items():
            x, y = _xy(tile)
            t = REF._new_plant(crop, self.planted_day, TPD)
            t["yield_units"] = int(yld)
            t["max_lifespan_step"] = LONG_LIFE
            farm["tiles"][y][x] = t
        farm["farmer"] = list(_xy(self.upos[0]))
        farm["hands"] = [list(_xy(p)) for p in self.upos[1:]]
        priv = env.state[0].observation["private"]
        priv["shed"] = {k: int(v) for k, v in self.shed.items()}
        priv["seeds"] = {c: 0 for c in spec.CROPS}
        priv["inventories"] = [{} for _ in self.upos]

    # --- simulator ------------------------------------------------------
    def install_sim(self, st):
        z = np.zeros((2, spec.N_TILES), np.int32)
        kind = np.asarray(st.kind).copy()
        occ = np.asarray(st.occ).copy()
        t_day = z.copy()
        t_yield = z.copy()
        t_cons = z.copy()
        t_life = (z - 1).copy()
        kind[0] = spec.KIND_EMPTY
        for tile, (crop, yld) in self.plants.items():
            kind[0, tile] = spec.KIND_PLANT
            occ[0, tile] = spec.CROPS.index(crop)
            t_day[0, tile] = self.planted_day
            t_yield[0, tile] = int(yld)
            t_cons[0, tile] = 1                  # `_new_plant`'s planting-day debt
            t_life[0, tile] = LONG_LIFE
        shed = np.asarray(st.shed).copy()
        for name, n in self.shed.items():
            shed[0, ITEMS.index(name)] = int(n)
        upos = np.asarray(st.upos).copy()
        for u, p in enumerate(self.upos):
            upos[0, u] = p
        money = np.asarray(st.money).copy()
        money[0] = self.money
        nquad = np.asarray(st.nquad).copy()
        nquad[0] = 4
        nhands = np.asarray(st.nhands).copy()
        nhands[0] = len(self.upos) - 1
        return st._replace(
            kind=jnp.asarray(kind), occ=jnp.asarray(occ), t_day=jnp.asarray(t_day),
            t_yield=jnp.asarray(t_yield), t_cons=jnp.asarray(t_cons),
            t_life=jnp.asarray(t_life), shed=jnp.asarray(shed), upos=jnp.asarray(upos),
            money=jnp.asarray(money), nquad=jnp.asarray(nquad), nhands=jnp.asarray(nhands))


def _script_arrays(script, n_units):
    """`script[turn][unit] = (op, arg, qty)` -> the planner's [MU, TPD] layout."""
    uop = np.zeros((MU, TPD), np.int32)
    ua = np.zeros((MU, TPD), np.int32)
    uq = np.zeros((MU, TPD), np.int32)
    for h, row in enumerate(script):
        for u in range(n_units):
            op, arg, qty = row[u]
            uop[u, h], ua[u, h], uq[u, h] = op, arg, qty
    return uop, ua, uq


def _market_arrays(orders):
    """`orders[turn] = [(mo, arg, qty), ...]` -> the planner's [TPD, MO] layout."""
    mop = np.full((TPD, MO), O.MO_NONE, np.int32)
    ma = np.zeros((TPD, MO), np.int32)
    mq = np.zeros((TPD, MO), np.int32)
    for h, row in orders.items():
        for s, (op, arg, qty) in enumerate(row):
            mop[h, s], ma[h, s], mq[h, s] = op, arg, qty
    return mop, ma, mq


def _engine_snapshot(env):
    obs = env.state[0].observation
    priv = env.state[0].observation["private"]
    shed = np.zeros(spec.N_ITEMS, np.int32)
    for name, n in priv["shed"].items():
        shed[ITEMS.index(name)] = n
    inv = np.zeros((MU, spec.N_ITEMS), np.int32)
    for u, d in enumerate(priv["inventories"]):
        for name, n in d.items():
            inv[u, ITEMS.index(name)] = n
    farm = obs["farms"][0]
    pos = [farm["farmer"]] + list(farm["hands"])
    yields = np.zeros(spec.N_TILES, np.int32)
    kinds = []
    for y, row in enumerate(farm["tiles"]):
        for x, t in enumerate(row):
            if isinstance(t, dict) and t.get("kind") == "PLANT":
                yields[y * BOARD + x] = t["yield_units"]
            kinds.append("." if t is None else ("#" if t == "LOCKED" else t.get("kind")))
    return {"shed": shed, "inv": inv, "money": int(farm["money"]),
            "upos": [p[1] * BOARD + p[0] for p in pos], "t_yield": yields,
            "kinds": kinds,
            "mkt_inv": np.array([obs["market"]["inventory"][n] for n in spec.PRODUCTS],
                                np.int32)}


def _sim_snapshot(st, n_units):
    kinds = []
    kind = np.asarray(st.kind[0])
    for i in range(spec.N_TILES):
        k = int(kind[i])
        kinds.append({spec.KIND_EMPTY: ".", spec.KIND_LOCKED: "#", spec.KIND_WEED: "WEED",
                      spec.KIND_PLANT: "PLANT", spec.KIND_COOP: "COOP",
                      spec.KIND_PASTURE: "PASTURE"}[k])
    return {"shed": np.asarray(st.shed[0]), "inv": np.asarray(st.inv[0]),
            "money": int(st.money[0]),
            "upos": [int(v) for v in np.asarray(st.upos[0])[:n_units]],
            "t_yield": np.asarray(st.t_yield[0]), "kinds": kinds,
            "mkt_inv": np.asarray(st.mkt_inv)}


def _run(scenario, script, orders, n_turns):
    """Play `n_turns` of day 0 in both backends; return the per-turn snapshots."""
    n_units = len(scenario.upos)
    uop, ua, uq = _script_arrays(script, n_units)
    mop, ma, mq = _market_arrays(orders)

    env = make("kaggriculture", configuration={"seed": 20260830})
    env.reset(2)
    scenario.install_engine(env)
    plan = (uop, ua, uq, mop, ma, mq)
    engine = []
    for h in range(n_turns):
        act = render.turn_action(plan, h, n_units - 1)
        env.step([act, {"farmer": ["PASS"], "hands": [], "market": []}])
        engine.append(_engine_snapshot(env))

    tables = build_tables(jnp)
    st = scenario.install_sim(initial_state(jnp))
    both_uop = jnp.stack([jnp.asarray(uop), jnp.zeros((MU, TPD), jnp.int32)])
    both_ua = jnp.stack([jnp.asarray(ua), jnp.zeros((MU, TPD), jnp.int32)])
    both_uq = jnp.stack([jnp.asarray(uq), jnp.zeros((MU, TPD), jnp.int32)])
    zmop = jnp.full((TPD, MO), O.MO_NONE, jnp.int32)
    z = jnp.zeros((TPD, MO), jnp.int32)
    cmop, cma, cmq = rollout.compact_orders(jnp.stack([jnp.asarray(mop), zmop]),
                                            jnp.stack([jnp.asarray(ma), z]),
                                            jnp.stack([jnp.asarray(mq), z]))
    sim = []
    for h in range(n_turns):
        st = apply_units(jnp, st, jnp.int32(0), both_uop[:, :, h], both_ua[:, :, h],
                         both_uq[:, :, h])
        if h < O.FULL_MARKET_TURNS:
            st = rollout._market_turn(tables, st, cmop[:, h], cma[:, h], cmq[:, h])
        elif h in O.SELL_TURNS:
            st = rollout._market_turn(tables, st, cmop[:, h], cma[:, h], cmq[:, h],
                                      sell_only=True, land=True)
        st = rollout.town_consume(st)
        st = rollout.decay_plants(st)
        st = st._replace(step=st.step + 1)
        sim.append(_sim_snapshot(st, n_units))
    return engine, sim


def _assert_agrees(engine, sim):
    for h, (e, s) in enumerate(zip(engine, sim)):
        for k in e:
            assert np.array_equal(np.asarray(e[k]), np.asarray(s[k])), \
                f"turn {h}: {k} diverged\nengine={e[k]}\nsim={s[k]}"


# --- scenarios -------------------------------------------------------------
# Shed-access tiles on a 10x10 board: (4,4) (5,4) (4,5) (5,5) -> 44 45 54 55.
FARMER, H1, H2 = 44, 45, 54
NORTH, SOUTH, EAST, WEST = O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST
PASS, HARV, DROP = O.OP_PASS, O.OP_HARVEST, O.OP_DROP


@pytest.mark.parametrize("water_first", [True, False])
def test_shared_tile_water_and_harvest_follow_unit_order(water_first):
    """A later unit observes the earlier unit's yield change or cleared tile."""
    sc = Scenario({80: ("CARROT", 2)}, [80, 80], planted_day=-3)
    actions = [(O.OP_WATER, 0, 0), (HARV, 0, 0)]
    if not water_first:
        actions.reverse()
    engine, sim = _run(sc, [actions], {}, 1)
    _assert_agrees(engine, sim)
    harvester = 1 if water_first else 0
    assert sim[0]["inv"][harvester, spec.I_CARROT] == (3 if water_first else 2)
    assert sim[0]["kinds"][80] == "."


def test_shared_tile_cannot_be_harvested_twice_in_one_turn():
    sc = Scenario({80: ("TOMATO", 3)}, [80, 80])
    engine, sim = _run(sc, [[(HARV, 0, 0), (HARV, 0, 0)]], {}, 1)
    _assert_agrees(engine, sim)
    assert sim[0]["inv"][0, spec.I_TOMATO] == 3
    assert sim[0]["inv"][1, spec.I_TOMATO] == 0


def _harvest_walk_drop_sell(shed=(), money=3000, sell_qty=9, far_unit=False):
    """Three ripe crops one step off the shed, harvested, carried back, dropped
    and sold in the same turn. Optionally a fourth unit that DROPs while standing
    away from the shed, which must be a no-op in both backends."""
    plants = {43: ("WHEAT", 4), 46: ("TOMATO", 3), 64: ("CARROT", 5)}
    upos = [FARMER, H1, H2]
    if far_unit:
        plants[23] = ("STRAWBERRY", 2)
        upos.append(23)
    sc = Scenario(plants, upos, shed=shed, money=money)
    n = len(upos)

    def row(*ops):
        ops = list(ops) + [(PASS, 0, 0)] * (n - len(ops))
        return ops

    script = [
        row((WEST, 0, 0), (EAST, 0, 0), (SOUTH, 0, 0)),          # 0: step onto the crop
        row((HARV, 0, 0), (HARV, 0, 0), (HARV, 0, 0), (HARV, 0, 0)),
        row((EAST, 0, 0), (WEST, 0, 0), (NORTH, 0, 0)),          # 2: back to the shed
        row((DROP, 0, 0), (DROP, 0, 0), (DROP, 0, 0), (DROP, 0, 0)),
    ]
    orders = {O.SELL_TURNS[0]: [(O.MO_SELL, spec.I_WHEAT, sell_qty)]}
    return sc, script, orders


def test_same_turn_harvest_drop_and_sell():
    """The whole chain the day-29 rule turns on: DROP banks in the unit phase,
    and that turn's SELL sees the banked stock."""
    sc, script, orders = _harvest_walk_drop_sell(sell_qty=4)
    engine, sim = _run(sc, script, orders, O.SELL_TURNS[0] + 1)
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["inv"].sum() == 0, "every dropped unit should be empty"
    # 4 wheat harvested, 4 sold in the same turn; the tomato and carrot stay.
    assert last["shed"][spec.I_WHEAT] == 0
    assert last["shed"][spec.I_TOMATO] == 3 and last["shed"][spec.I_CARROT] == 5
    assert last["money"] > sc.money, "the same-turn sale must have paid"


def test_drop_away_from_the_shed_is_a_no_op():
    sc, script, orders = _harvest_walk_drop_sell(sell_qty=4, far_unit=True)
    engine, sim = _run(sc, script, orders, O.SELL_TURNS[0] + 1)
    _assert_agrees(engine, sim)
    # Unit 3 never left tile 23, which is not shed-adjacent: it keeps its crop.
    assert engine[-1]["inv"][3][spec.I_STRAWBERRY] == 2


@pytest.mark.parametrize("room", [0, 1, 5, 8, 11])
def test_overflow_is_destroyed_in_the_engine_s_own_order(room):
    """DROP enforces `shedCapacity` at drop time and throws the excess away.

    The cut walks units in index order and, inside a unit, the inventory dict in
    first-acquisition order -- so which of the three crops survives depends on
    the room left, and a wrong walk order shows up as the wrong item kept.
    """
    pre = spec.SHED_CAPACITY - room
    sc, script, orders = _harvest_walk_drop_sell(shed={"MELON": pre}, sell_qty=0)
    engine, sim = _run(sc, script, orders, O.SELL_TURNS[0] + 1)
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"].sum() == pre + min(room, 12)
    assert last["inv"].sum() == 0, "DROP empties the unit even when it overflows"


def test_drop_before_the_walk_leaves_the_unit_empty_next_turn():
    """A second harvest after a DROP re-fills the same unit: `inv_seq` has to be
    reset by the drop, or the next overflow is walked in a stale order."""
    plants = {43: ("WHEAT", 4), 34: ("TOMATO", 6)}
    sc = Scenario(plants, [FARMER], shed={"MELON": spec.SHED_CAPACITY - 7})
    script = [
        [(WEST, 0, 0)],                 # 0: 44 -> 43
        [(HARV, 0, 0)],                 # 1: +4 wheat
        [(EAST, 0, 0)],                 # 2: back to 44
        [(DROP, 0, 0)],                 # 3: 4 wheat into the last 7 slots
        [(NORTH, 0, 0)],                # 4: 44 -> 34
        [(HARV, 0, 0)],                 # 5: +6 tomato
        [(SOUTH, 0, 0)],                # 6: back to 44
        [(DROP, 0, 0)],                 # 7: only 3 fit, 3 are destroyed
    ]
    engine, sim = _run(sc, script, {}, 8)
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"][spec.I_WHEAT] == 4
    assert last["shed"][spec.I_TOMATO] == 3
    assert last["shed"].sum() == spec.SHED_CAPACITY
    assert last["inv"].sum() == 0


# --- the planner's own day-29 chain, in the real engine ---------------------

def test_a_whole_season_with_drop_on_matches_the_engine(monkeypatch):
    """Gate 1, re-run with `plan.DROP_ON`.

    The scripted tests above pin the mechanic; this pins the *plan* -- day 29
    hires, harvests, walks every unit home, DROPs and sells into lot 3, and the
    simulator has to agree with kaggle_environments on every state field at
    every day boundary of the season that does it. The shipped theta is used
    because random weights barely develop the farm and leave day 29 with
    nothing ripe to walk home; the DROP count is asserted so the test cannot go
    quiet if the shipped theta ever stops exercising the chain.
    """
    import test_sim_equivalence as EQ
    from kagg3.core import plan as P

    theta_path = os.path.join(os.path.dirname(__file__), "..", "artifacts", "theta.npy")
    if not os.path.exists(theta_path):
        pytest.skip("no trained theta yet")
    monkeypatch.setattr(P, "DROP_ON", True)
    theta = np.load(theta_path).astype(np.float32)
    seed = 20260821
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([EQ.agent_for(theta), EQ.agent_for(theta)])
    drops = sum(
        1
        for st in env.steps
        for s_ in st
        for a in ([(s_.action or {}).get("farmer", ["PASS"])]
                  + list((s_.action or {}).get("hands", []) or []))
        if a and a[0] == "DROP")
    assert drops > 0, "the season never emitted a DROP"

    EQ._compare_season(theta, seed)
