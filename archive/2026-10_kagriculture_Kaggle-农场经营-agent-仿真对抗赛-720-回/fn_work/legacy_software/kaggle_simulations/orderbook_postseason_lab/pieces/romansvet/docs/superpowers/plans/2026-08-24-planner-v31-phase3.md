# Planner V3.1 — Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Dispatch each task to a fresh **Opus** subagent (`model: "opus"`); the implementer sees only its own task plus the header, so every task repeats what it needs.

**Goal:** Land Phase 3 of `docs/PLANNER_V3_1.md` §8 — DROP in the simulator and the terminal rules re-derived through it (§4), the three verified modules M1 prospective land, M2 liquidity resequencing and M3 structure conversion (§5), the turn-time walk-and-cap lot guard (§3), and a per-parameter-sigma trial in the trainer — each measured against the frozen Phase-2 theta with its sign stated first.

**Architecture:** The simulator gains the two engine behaviours it lacked (DROP, PLACE-to-shed), transcribed exactly; the horizon constant that every terminal rule derives from moves from "banked by eod 28" to "harvested and dropped by turn 17 of day 29" (one turn before lot 3; the engine would also honour a same-turn DROP at 18, see Task 2); the planner gains a return leg, prospective tiles, a turn-2 land order funded by lot-1 revenue, DIG-based conversion, and a seventh plan array of per-lot price floors that both executors apply identically at turns 10 and 18. The trainer gains an optional separable-NES sigma vector. Nothing changes the genome: Phase 3 keeps the Phase-2 lineage and is measured on its frozen theta.

**Tech Stack:** Python 3, numpy, JAX (CPU for tests; GPU for training), kaggle_environments (the pinned engine), pytest, ruff.

**Spec:** `docs/PLANNER_V3_1.md` §3, §4, §5 (M1–M3), §6 (registry), §7, §8 (Phase 3 bullet). Audit record: `docs/PLANNER_V3_1_REVIEW.md`. Read both before starting a task.

**Prerequisites:** Phases 0–2 are fully landed — `git log --oneline | grep -c "Record the Phase-"` prints `3`. This plan quotes post-Phase-2 code by content: `ops.LAST_SHED_DAY`, `core/projector.py`, `core/valuation.py`, `core/loop.py`, `core/sell.py` (`allocate`, `best_lot`, `adjusted_marginals`, `N_LOTS`), `core/budget.py`, `plan.Prefix`/`_derive`/`build_day`/`_routes(xp, chain_op, chain_a, chain_q, n_ops, order, n_tasks, pick_masks, n_units, budget)`/`_market(xp, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, lots, n_hire)`, `Macro = (plant_target, animal_kind, animal_count, buy_land, hold, press, grow_mult)`, `DayView` with `mkt_inv/shops/t_bank`, the seven-field `build_day` locals named in each task's Interfaces block, `scripts/eval_vs_baselines.py --csv --seed-base`, `scripts/paired_ci.py`.

## Global Constraints

Every task's requirements implicitly include this section.

- Planner code is array-agnostic (`xp`), shape-static, int32; bounded loops through `core/loop.py`; `core/` never imports `jax` (the packager parses ASTs). `sim/` is JAX-only and may use `.at[]`.
- The simulator is a **transcription** of the pinned engine (`vendor/engine.lock.json`, sha `bc8a548…`): every new branch cites the engine lines it mirrors and is pinned by an engine-vs-sim test. Silent divergence is the failure mode §6 warns about; when a sim change is made, run `tests/test_sim_equivalence.py` and `tests/test_trained_equivalence.py` before committing.
- Equivalence-surface registry (§6): the sim resolves the market only on hours 0–2 (full path) and 10/18 (sell-only) — **no task in this plan adds a market turn**; M2 uses the free tenth slot of turn 2. Both seats keep an identical slot layout. Cross-unit same-tile same-turn disjointness holds.
- Terminal laws derive from one horizon parameter; after Task 2 that parameter is `ops.LAST_HARVEST_DAY` (29) for "a harvest can still sell" and `ops.LAST_SHED_DAY` (28) only for "an end-of-day banks into the shed". No other day constant appears in code.
- The genome is untouched (no `Macro` field, no decode transform, no theta layout change). Every task is measured on the frozen Phase-2 `artifacts/theta.npy` with a predicted sign stated before the run (Task 9).
- Every optimizer lands with a compile-time and throughput measurement (`python scripts/bench_sim.py` before/after, numbers in the commit message; >15% slowdown is reported and stops the task).
- Interpreter: every `python` in this plan means the repo's `.venv/bin/python` — the system `python` has neither JAX nor `kaggle_environments`.
- Tests: file header `os.environ.setdefault("JAX_PLATFORMS", "cpu")`, `sys.path.insert(0, "src")`; shared fixtures `tests/test_budget_order.py::_view/_macro`; run `python -m pytest tests/<file>.py -q`, full suite `python -m pytest -q`.
- Lint: `ruff check src tests scripts` clean before every commit. Commit per task on branch `fitness-shaping`, one-line sentence-case imperative message. Never commit `artifacts/`.

## Engine facts the tasks lean on (read from the pinned engine)

- `_apply_unit_action` (engine :312–415): shed ops resolve **before** the LOCKED guard. `DROP` (:343–356): requires `_is_shed_adjacent`; walks the unit's inventory dict **in insertion order** (= first-acquisition order, which the sim tracks in `inv_seq`); per item `room = capacity − sum(shed)`, deposits `min(n, room)`, then **deletes the item from the inventory whether or not it fit** — overflow is destroyed. `PICKUP` (:358–375) unchanged. `PLACE` (:377–410): if the item is an animal **and** the tile is a dict of the matching structure kind with no animal, place it (if held) and return — no fallthrough even when the animal is not held; otherwise, if shed-adjacent, deposit `n = min(action[2] (default 1), held, room)` of the item into the shed and **keep the excess in the inventory**.
- `_parse_order` (:631–650): a `SELL item 0` parses to `None` — an inert order that **keeps its queue index** (the lockstep loop is indexed by position) and counts toward `maxMarketOrdersPerTurn = 10` (`queues.append(q[:max_orders])`).
- `_process_market` (:544–630): orders resolve index by index; at each index HIRE/BUY_LAND resolve first in player order, then the SELL/BUY lockstep. A `BUY_LAND` at index 9 of turn 2 therefore resolves after the nine sells at indices 0–8 and is funded by their revenue (M2, no sim change: `rollout.run_day` runs the full market path on hours < 3 and `market.process_slot` handles `MO_BUY_LAND` in every slot).
- `_do_buy_land`: unlocks the quadrant synchronously inside the market phase; movement onto LOCKED tiles is legal; tile ops on them no-op. Units act **before** the market in every turn, so a tile unlocked at turn *t* accepts ops from turn *t+1*.
- `DIG` removes weeds, living plants and **empty** structures in both engine and sim (`units.py`: `do_dig = op == DIG & ~locked & (k != EMPTY) & ~has_an`).
- Day 29 has no end-of-day; the last executed step is 718 (day 29, turn 22). A unit's inventory on day 29 reaches the shed only through DROP; SELL lot 3 at turn 18 then sells it in the same day.
- The equivalence harness (`tests/test_sim_equivalence.py`) plays whole games with `agent_for(theta)` on both seats and compares every state field per day; it exercises whatever the planner emits.

## File map

| File | Responsibility after Phase 3 |
|---|---|
| `src/kagg3/sim/units.py` | unit-sequential shed block: PICKUP, DROP, PLACE-to-shed (Task 1) |
| `src/kagg3/core/ops.py` | `LAST_HARVEST_DAY = 29`, `DROP_DEADLINE_TURN = 17`, `RETURN_TURNS = 9` (Task 2) |
| `src/kagg3/core/valuation.py`, `brain.py`, `plan.py` | horizons on `LAST_HARVEST_DAY`; final-day rules: harvest/collect/return/DROP, lot 3 reserved for drops, capacity law (Tasks 2–3) |
| `src/kagg3/core/plan.py` | prospective tiles (Task 4); land at turn 2 funded by provisional lot-1 revenue (Task 5); DIG conversion/reclamation (Task 6); `mkt_floor` seventh plan array (Task 7) |
| `src/kagg3/core/guard.py` | **new** — `cap_row` walk-and-cap (Task 7) |
| `src/kagg3/agent/render.py`, `runtime.py`, `src/kagg3/sim/rollout.py` | zero-quantity SELL placeholders; the cap applied at turns 10/18 on both sides (Task 7) |
| `src/kagg3/es/train.py`, `scripts/train.py` | separable-NES sigma vector, checkpointed (Task 8) |
| `scripts/day_metrics.py` | **new** — §7 operational metrics from an engine replay (Task 9) |
| tests | `test_sim_drop.py`, `test_horizon_drop.py`, `test_return_leg.py`, `test_prospective_land.py`, `test_land_at_turn_two.py`, `test_dig_conversion.py`, `test_walk_and_cap.py`, `test_sigma_adapt.py`; `test_planner_op_coverage.py` rewritten (Task 1) |

Task order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. Tasks 1–3 form the DROP chain; 4 precedes 5 (M2 changes when prospective tiles unlock); 6, 7, 8 are independent of each other.

---

### Task 1: DROP and PLACE-to-shed in the simulator (§4, §6.4)

**Files:**
- Modify: `src/kagg3/sim/units.py` (the shed block of `apply_units`)
- Rewrite: `tests/test_planner_op_coverage.py`
- Test: `tests/test_sim_drop.py`

**Interfaces:**
- Produces: `apply_units` handles `OP_DROP` and the PLACE-to-shed fallthrough exactly; `tests/test_planner_op_coverage.py::UNIMPLEMENTED == frozenset()`. `tests/test_sim_drop.py` defines `_scripted(actions)`, `_pass`, `_engine_after(env, turn, player)` and `_sim_replay(...)` — the directed engine-vs-sim replay helpers Tasks 3, 5 and 7 reuse (import them from this file).

**Background.** The engine walks units in index order and each unit's shed op is atomic, so the room a DROP finds depends on every earlier unit's pickups and deposits in the same turn; the sim's cumulative-sum PICKUP shortcut is exact only while pickups are the sole shed op. Replace it with an unrolled walk over the eleven units: PICKUP takes `min(qty, shed[item])`; DROP deposits the whole inventory in first-acquisition order (`inv_seq`), item by item against the shrinking room, and zeroes the inventory regardless; PLACE-to-shed deposits `min(qty, held, room)` of one item and keeps the rest. The animal-placement branch keeps its precedence: an animal item on a matching empty structure never falls through, held or not. Day-0 cash cannot fill a shed, so overflow is pinned by a sim-only transcription test here and end-to-end by the equivalence games once Task 3 makes the planner drop on day 29.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sim_drop.py`:

```python
"""DROP and PLACE-to-shed, transcribed from the engine (PLANNER_V3_1 section
4): shed-adjacent only; DROP dumps the whole inventory in first-acquisition
order and destroys what does not fit; PLACE-to-shed deposits one item's
quantity and keeps the excess; an animal item on a matching empty structure
is placed, never deposited. Directed engine-vs-sim replays on day 0, plus a
sim-only overflow transcription (day-0 cash cannot fill a shed).
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

import jax.numpy as jnp
import numpy as np
from kaggle_environments import make

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.sim import rollout, units
from kagg3.sim.state import build_tables, initial_state

MU, TPD, MO = spec.MAX_UNITS, spec.TURNS_PER_DAY, spec.MAX_MARKET_ORDERS


def _scripted(actions):
    """actions[turn] -> {"farmer": [...], "hands": [...], "market": [...]} on day 0."""
    def agent(obs, config=None):
        t = int(obs["day"]) * TPD + int(obs["hour"])
        return actions.get(t, {"farmer": ["PASS"], "hands": [], "market": []})
    return agent


def _pass(obs, config=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _engine_after(env, turn, player=0):
    """(shed[12], farmer inventory[12]) after `turn` of day 0."""
    priv = env.steps[turn + 1][player].observation["private"]
    shed = np.zeros(spec.N_ITEMS, np.int32)
    for name, n in priv.get("shed", {}).items():
        shed[spec.ITEM_IX[name]] = n
    inv = np.zeros(spec.N_ITEMS, np.int32)
    for name, n in (priv.get("inventories") or [{}])[0].items():
        inv[spec.ITEM_IX[name]] = n
    return shed, inv


def _plan_arrays(unit_ops, market):
    """unit_ops[turn] = (op, arg, qty) for the farmer of seat 0;
    market[turn] = [(mo, arg, qty), ...] for seat 0; seat 1 passes."""
    uop = np.zeros((2, MU, TPD), np.int32)
    ua = np.zeros((2, MU, TPD), np.int32)
    uq = np.zeros((2, MU, TPD), np.int32)
    mop = np.zeros((2, TPD, MO), np.int32)
    ma = np.zeros((2, TPD, MO), np.int32)
    mq = np.zeros((2, TPD, MO), np.int32)
    for t, (op, a, q) in unit_ops.items():
        uop[0, 0, t], ua[0, 0, t], uq[0, 0, t] = op, a, q
    for t, orders in market.items():
        for s, (mo, a, q) in enumerate(orders):
            mop[0, t, s], ma[0, t, s], mq[0, t, s] = mo, a, q
    return tuple(jnp.asarray(x) for x in (uop, ua, uq, mop, ma, mq))


def _sim_replay(uop, ua, uq, mop, ma, mq, n_turns):
    """Day 0 of the simulator under hand-built arrays (rollout.run_day's turn
    body without the policy)."""
    tables = build_tables(jnp)
    st = initial_state(jnp)
    for h in range(n_turns):
        st = units.apply_units(jnp, st, jnp.int32(0), uop[:, :, h], ua[:, :, h], uq[:, :, h])
        if h < 3:
            st = rollout._market_turn(tables, st, mop[:, h], ma[:, h], mq[:, h])
        elif h in O.SELL_TURNS[1:]:
            st = rollout._market_turn(tables, st, mop[:, h], ma[:, h], mq[:, h], sell_only=True)
        st = rollout.town_consume(st)
        st = rollout.decay_plants(st)
        st = st._replace(step=st.step + 1)
    return st


def _both(unit_actions, unit_ops, market_actions, market_ops, last_turn):
    env = make("kaggriculture", configuration={"seed": 7})
    acts = {}
    for t in range(last_turn + 1):
        acts[t] = {"farmer": unit_actions.get(t, ["PASS"]), "hands": [],
                   "market": market_actions.get(t, [])}
    env.run([_scripted(acts), _pass])
    st = _sim_replay(*_plan_arrays(unit_ops, market_ops), n_turns=last_turn + 1)
    e_shed, e_inv = _engine_after(env, last_turn)
    return e_shed, e_inv, np.asarray(st.shed[0]), np.asarray(st.inv[0, 0])


W = spec.I_WHEAT


def test_pickup_walk_and_drop_returns_the_wheat():
    unit_actions = {2: ["PICKUP", "WHEAT", 20], 3: ["EAST"], 4: ["DROP"]}
    unit_ops = {2: (O.OP_PICKUP, W, 20), 3: (O.OP_EAST, 0, 0), 4: (O.OP_DROP, 0, 0)}
    market_actions = {1: [["BUY_PRODUCT", "WHEAT", 20]]}
    market_ops = {1: [(O.MO_BUY_PRODUCT, W, 20)]}
    e_shed, e_inv, s_shed, s_inv = _both(unit_actions, unit_ops, market_actions, market_ops, 4)
    assert e_shed.tolist() == s_shed.tolist() and e_inv.tolist() == s_inv.tolist()
    assert int(s_shed[W]) == 20 and int(s_inv.sum()) == 0


def test_drop_away_from_the_shed_is_a_no_op():
    unit_actions = {2: ["PICKUP", "WHEAT", 20], 3: ["EAST"], 4: ["EAST"], 5: ["DROP"]}
    unit_ops = {2: (O.OP_PICKUP, W, 20), 3: (O.OP_EAST, 0, 0), 4: (O.OP_EAST, 0, 0), 5: (O.OP_DROP, 0, 0)}
    e_shed, e_inv, s_shed, s_inv = _both(unit_actions, unit_ops, {1: [["BUY_PRODUCT", "WHEAT", 20]]},
                                         {1: [(O.MO_BUY_PRODUCT, W, 20)]}, 5)
    assert e_shed.tolist() == s_shed.tolist() and e_inv.tolist() == s_inv.tolist()
    assert int(s_inv[W]) == 20


def test_place_to_shed_deposits_a_quantity_and_keeps_the_rest():
    unit_actions = {2: ["PICKUP", "WHEAT", 20], 3: ["PLACE", "WHEAT", 5]}
    unit_ops = {2: (O.OP_PICKUP, W, 20), 3: (O.OP_PLACE, W, 5)}
    e_shed, e_inv, s_shed, s_inv = _both(unit_actions, unit_ops, {1: [["BUY_PRODUCT", "WHEAT", 20]]},
                                         {1: [(O.MO_BUY_PRODUCT, W, 20)]}, 3)
    assert e_shed.tolist() == s_shed.tolist() and e_inv.tolist() == s_inv.tolist()
    assert int(s_shed[W]) == 5 and int(s_inv[W]) == 15


def test_an_animal_placed_off_its_structure_falls_through_to_the_shed():
    # the farmer stands on an empty tile (no structure): PLACE GOOSE deposits it
    unit_actions = {2: ["PICKUP", "GOOSE", 1], 3: ["PLACE", "GOOSE", 1]}
    unit_ops = {2: (O.OP_PICKUP, spec.I_GOOSE, 1), 3: (O.OP_PLACE, spec.I_GOOSE, 1)}
    e_shed, e_inv, s_shed, s_inv = _both(unit_actions, unit_ops, {1: [["BUY_ANIMAL", "GOOSE", 1]]},
                                         {1: [(O.MO_BUY_ANIMAL, 0, 1)]}, 3)
    assert e_shed.tolist() == s_shed.tolist() and e_inv.tolist() == s_inv.tolist()
    assert int(s_shed[spec.I_GOOSE]) == 1 and int(s_inv.sum()) == 0


def test_overflow_is_destroyed_in_first_acquisition_order():
    # sim-only transcription: 98 in the shed, the farmer holds 5 wheat (older)
    # and 3 eggs (newer); DROP fits 2 wheat, destroys the rest, empties the unit
    st = initial_state(jnp)
    st = st._replace(shed=st.shed.at[0, W].set(98),
                     inv=st.inv.at[0, 0, W].set(5).at[0, 0, spec.I_EGG].set(3),
                     inv_seq=st.inv_seq.at[0, 0, W].set(3).at[0, 0, spec.I_EGG].set(7))
    uop = jnp.zeros((2, MU), jnp.int32).at[0, 0].set(O.OP_DROP)
    z = jnp.zeros((2, MU), jnp.int32)
    out = units.apply_units(jnp, st, jnp.int32(0), uop, z, z)
    assert int(out.shed[0, W]) == 100 and int(out.shed[0, spec.I_EGG]) == 0
    assert int(out.inv[0, 0].sum()) == 0
    assert int(out.inv_seq[0, 0, W]) == units._BIG_SEQ and int(out.inv_seq[0, 0, spec.I_EGG]) == units._BIG_SEQ


def test_an_earlier_units_pickup_makes_room_for_a_later_units_drop():
    # sim-only: shed 100 wheat; unit 0 picks up 4, unit 1 (holding 4 eggs) drops
    st = initial_state(jnp)
    st = st._replace(shed=st.shed.at[0, W].set(100), nhands=st.nhands.at[0].set(1),
                     upos=st.upos.at[0, 1].set(int(spec.SHED_ACCESS_TILE[1])),
                     inv=st.inv.at[0, 1, spec.I_EGG].set(4),
                     inv_seq=st.inv_seq.at[0, 1, spec.I_EGG].set(2))
    uop = jnp.zeros((2, MU), jnp.int32).at[0, 0].set(O.OP_PICKUP).at[0, 1].set(O.OP_DROP)
    ua = jnp.zeros((2, MU), jnp.int32).at[0, 0].set(W)
    uq = jnp.zeros((2, MU), jnp.int32).at[0, 0].set(4)
    out = units.apply_units(jnp, st, jnp.int32(0), uop, ua, uq)
    assert int(out.shed[0, W]) == 96 and int(out.shed[0, spec.I_EGG]) == 4
    assert int(out.inv[0, 0, W]) == 4 and int(out.inv[0, 1].sum()) == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_sim_drop.py -q`
Expected: FAIL — the sim leaves the wheat in the inventory after DROP (`0 == 20` on the shed) and ignores PLACE-to-shed.

- [ ] **Step 3: Rewrite the shed block of `apply_units`**

In `src/kagg3/sim/units.py`, inside the `for p in range(2):` loop, move the tile reads that the shed block needs above it — cut these lines from the tile-operations section and paste them directly after `newpos = ...`:

```python
        tile = pos
        k = kind[p][tile]
        o = occ[p][tile]
        locked = k == spec.KIND_LOCKED
        is_pl = (k == spec.KIND_PLANT) & ~locked
        is_st = ((k == spec.KIND_COOP) | (k == spec.KIND_PASTURE)) & ~locked
        has_an = is_st & (o >= 0)
        free_st = is_st & (o < 0)
        is_empty = (k == spec.KIND_EMPTY)
        pa = xp.clip(arg - spec.I_GOOSE, 0, spec.N_ANIMALS - 1)
        a_struct = xp.asarray(spec.ANIMAL_STRUCT)[pa]
```

(delete the duplicate `pa`/`a_struct` lines further down.) Then replace the whole `# --- shed PICKUP ---` block (from its comment through `inv = inv.at[p].add(taken)`) with:

```python
        # --- shed ops: PICKUP, DROP, PLACE-to-shed (engine :343-410) --------
        # The engine walks units in index order and each unit's shed op is
        # atomic, so the room a DROP finds depends on every earlier unit's
        # pickups and deposits this turn. Eleven unrolled steps over [NI]
        # vectors reproduce that walk exactly. DROP dumps the whole inventory
        # in first-acquisition order against the shrinking room and empties
        # the unit whether or not everything fit; PLACE-to-shed deposits one
        # item's quantity and keeps the excess; an animal item on a matching
        # empty structure is placed by the tile branch below and never falls
        # through, held or not.
        shed_adj = xp.asarray(spec.IS_SHED_ADJACENT)[pos]
        place_match = (op == O.OP_PLACE) & (arg >= spec.I_GOOSE) & free_st & (k == a_struct)
        want_pick = (op == O.OP_PICKUP) & shed_adj & (qty > 0)
        want_drop = (op == O.OP_DROP) & shed_adj
        want_dep = (op == O.OP_PLACE) & ~place_match & shed_adj & (qty > 0)
        inv_before = inv[p]
        shed_p = shed[p]
        inv_p = inv[p]
        item_ix = xp.arange(NI, dtype=i32)
        for u in range(MU):
            it = xp.clip(arg[u], 0, NI - 1)
            is_it = item_ix == it
            take = xp.where(want_pick[u] & is_it, xp.minimum(qty[u], shed_p[it]), 0)
            shed_p = shed_p - take
            inv_u = inv_p[u] + take
            room = xp.maximum(spec.SHED_CAPACITY - xp.sum(shed_p), 0)
            # DROP: items in insertion order, each capped by what is still free
            order = xp.argsort(inv_seq[p][u])
            n_sorted = inv_u[order]
            cum = xp.cumsum(n_sorted)
            dep_sorted = xp.minimum(room, cum) - xp.minimum(room, cum - n_sorted)
            drop_dep = xp.where(want_drop[u], xp.zeros(NI, i32).at[order].set(dep_sorted), 0)
            # PLACE-to-shed: one item, min(qty, held, room)
            dep_n = xp.minimum(xp.minimum(qty[u], inv_u[it]), room)
            place_dep = xp.where(want_dep[u] & is_it, dep_n, 0)
            shed_p = shed_p + drop_dep + place_dep
            inv_u = xp.where(want_drop[u], 0, inv_u - place_dep)
            inv_p = inv_p.at[u].set(inv_u)
        shed = shed.at[p].set(shed_p)
        inv = inv.at[p].set(inv_p)
```

Below, the existing `do_place` line must read the post-shed inventory and the precomputed match: replace it with `do_place = place_match & (inv[p][xp.arange(MU), xp.clip(arg, 0, NI - 1)] > 0)`. Update the module docstring's second paragraph: "Shed operations are genuinely shared and order-dependent once DROP exists, so they are walked unit by unit in index order, exactly as the engine does."

- [ ] **Step 4: Rewrite the op-coverage pin**

In `tests/test_planner_op_coverage.py` set `UNIMPLEMENTED = frozenset()`, rewrite the module docstring to say both branches are now implemented (Phase 3, Task 1) and that the file pins the op *set* plus a static marker for each, delete `test_drop_is_confined_to_naming_and_rendering`, and add:

```python
def test_drop_and_place_to_shed_are_implemented_in_the_sim():
    src = (ROOT / "src" / "kagg3" / "sim" / "units.py").read_text()
    assert "want_drop" in src and "want_dep" in src, "the shed block lost its DROP / PLACE-to-shed branches"


def test_planner_place_always_carries_an_animal():
    # PLACE with a product item would be a shed deposit; the planner's PLACE
    # argument is the day's animal item and nothing else
    src = (ROOT / "src" / "kagg3" / "core" / "plan.py").read_text()
    place_lines = [ln for ln in src.splitlines() if "O.OP_PLACE" in ln and "xp.full" in ln]
    assert place_lines and all("a_item" in ln for ln in place_lines), place_lines
```

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_sim_drop.py tests/test_planner_op_coverage.py -q` — Expected: PASS (8 tests; the engine games take a few seconds each).
Run: `python -m pytest -q` — Expected: all pass; `test_sim_equivalence.py` still passes because the planner emits no DROP yet, and the PICKUP path must be bit-identical to before (`test_unit_pickups.py`, `test_gates.py`).
Run: `python scripts/bench_sim.py` here and on the previous commit; record both (eleven unrolled steps of 12-vectors inside the turn scan).
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/sim/units.py tests/test_sim_drop.py tests/test_planner_op_coverage.py
git commit -m "Implement DROP and PLACE-to-shed in the simulator, unit by unit as the engine does"
```

---

### Task 2: Re-derive the terminal rules through the DROP horizon (§4, §0.4)

**Files:**
- Modify: `src/kagg3/core/ops.py` (+`LAST_HARVEST_DAY`, `DROP_DEADLINE_TURN`, `RETURN_TURNS`), `src/kagg3/core/valuation.py` (every `O.LAST_SHED_DAY` → `O.LAST_HARVEST_DAY`), `src/kagg3/core/brain.py` (plant gate, `n_free_slots` clamp), `src/kagg3/core/plan.py` (`_derive`: `harvest_age`, `survival_pays`, `terminal` → `final`, purchase gates, per-product inflow; `build_day`: hold, lot-3 reservation), `src/kagg3/core/sell.py` (`allocate(..., open_lots=N_LOTS)`)
- Modify tests whose day-28/29 expectations change: `tests/test_day29_endgame.py`, `tests/test_feed_care_cadence.py`, `tests/test_deadline_harvest.py`, `tests/test_valuation.py`, `tests/test_animal_acquisition_bound.py`, `tests/test_fertilizer_value.py`, `tests/test_hire_enumeration.py`, `tests/test_sell_side.py`, `tests/test_budget_greedy.py`, `tests/test_admit_route.py` (each listed below with its new number)
- Test: `tests/test_horizon_drop.py`

**Interfaces:**
- Produces: `ops.LAST_HARVEST_DAY = 29` (a harvest on this day still sells: DROP by `DROP_DEADLINE_TURN = SELL_TURNS[-1] - 1 = 17`, sold in lot 3), `ops.RETURN_TURNS = 9` (worst-case walk to the nearest shed-access tile, 8, plus the DROP); `sell.allocate(xp, price_table, mkt_inv, shops, avail, hold, press, open_lots=N_LOTS)` (lots at index ≥ `open_lots` never take a unit); `_derive` locals `final = day >= O.LAST_HARVEST_DAY` (replaces `terminal`), `inflow_by_product` (int[9]) alongside the scalar `inflow`; `Prefix` gains `inflow_by_product`? — no: inflow needs `covered`, which is routing's output; it stays in `build_day` (see Task 3). `Prefix` gains `final`.

**Background (§4, "re-derive every terminal rule").** With DROP, a day-29 harvest→DROP→sell-at-18 chain is legal, so eod-28 production is monetizable and every horizon shifts by one day: `fires_between(..., LAST_HARVEST_DAY)`, the plant gate `day + first <= 29`, the harvest clamp `clip(29 − planted_day, first, max)`, survival pays through day 28 (`day < 29`), CARE pays if its fire's harvest day is ≤ 29, the acquisition bound counts fires through day 29 and collections through day 29. Day 29 itself is **final**, not terminal: nothing *after* it pays, so no purchase, no feed, no *survival* watering, no planting, no CARE — but harvests, collections, the return leg and DROP are wanted, and so are the two same-day chains §0.4 keeps on the last harvest day and §4 re-derives through the horizon: an in-window WATER that raises a one-time crop's same-day harvest [LAW], and the value-conditional FERTILIZE→WATER→HARVEST chain [EXACT-OPT] (its fertilizer must already be in the shed — nothing is bought). Neither rule needs new code: `survival_pays` turns off survival water only, and the bonus/fertilizer rules already test the harvest against `LAST_HARVEST_DAY`; hands may be hired for them (the enumeration values them), the hour-0 shed is sold in lots 1–2 at zero reservation, and lot 3 is reserved for what the units drop (Task 3 fills it). `LAST_SHED_DAY` (28) survives only where an end-of-day is literally required: none of the planner's rules — it stays in `ops.py` for the sim-facing docstrings and the valuation's fertilizer-collection count (a collection on day `c` needs the animal alive at eod `c−1`; the last useful collection is day 29, i.e. `LAST_HARVEST_DAY − day` future collections).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_horizon_drop.py`:

```python
"""With DROP the horizon moves one day (PLANNER_V3_1 section 4): day-29
harvests sell through DROP and lot 3, so eod-28 production is monetizable and
every terminal rule re-derives from LAST_HARVEST_DAY = 29. Day 29 is final --
nothing after it pays -- but harvesting, collecting and dropping do.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import valuation as V

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
I = np.int32


def test_horizon_constants():
    assert O.LAST_HARVEST_DAY == 29 and O.LAST_SHED_DAY == 28
    assert O.DROP_DEADLINE_TURN == O.SELL_TURNS[-1] - 1 == 17
    assert O.RETURN_TURNS == 9


def test_valuation_counts_day_29_harvests():
    # goose placed day 0 seen day 5: eggs on days 6..29 = 24, fertilizer 24
    assert int(V.animal_value(np, BASE, I(0), I(0), I(0), I(0), I(5))) == 24 * 50 + 24 * 100
    # tomato planted day 20 fertilized on day 28: the fire at eod 28 pays now
    ha = I(int(np.clip(O.LAST_HARVEST_DAY - 20, 8, 8)))
    assert int(V.fert_marginal_value(np, BASE, I(20), I(0), I(spec.I_TOMATO), I(28), ha)) == 60
    # wheat planted day 26 harvests on day 29 at age 3 -> 3 units
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(26))) == 3
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(28))) == 0


def _view(day, plants=(), animals=(), shed=None, money=3000):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_day, t_cons, t_yield = z - 1, z.copy(), z.copy(), z.copy()
    for pos, c, planted, cons, y in plants:
        kind[pos], occ[pos], t_day[pos], t_cons[pos], t_yield[pos] = spec.KIND_PLANT, c, planted, cons, y
    for pos, a, placed, cons, y in animals:
        kind[pos], occ[pos], t_day[pos], t_cons[pos], t_yield[pos] = spec.ANIMAL_STRUCT[a], a, placed, cons, y
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in (shed or {}).items():
        sh[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(), t_cons=t_cons,
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _ops(view, **macro):
    unit_op = P.build_day(np, view, _macro(**macro))[0]
    return {op: int((unit_op == op).sum()) for op in (O.OP_WATER, O.OP_FEED, O.OP_CARE, O.OP_HARVEST, O.OP_PLANT)}


def test_survival_work_runs_on_day_28_again():
    # a tomato that fires at eod 28 and a goose that lays at eod 28 are worth keeping alive
    view = _view(28, plants=[(0, spec.I_TOMATO, 20, 1, 0)], animals=[(1, 0, 24, 1, 0)], shed={spec.I_WHEAT: 5})
    ops = _ops(view)
    assert ops[O.OP_WATER] == 1 and ops[O.OP_FEED] == 1


def test_day_29_harvests_but_neither_feeds_nor_waters_for_survival():
    view = _view(29, plants=[(0, spec.I_TOMATO, 20, 1, 2)], animals=[(1, 0, 24, 1, 1)], shed={spec.I_WHEAT: 5})
    ops = _ops(view)
    assert ops[O.OP_HARVEST] == 2 and ops[O.OP_WATER] == 0 and ops[O.OP_FEED] == 0 and ops[O.OP_CARE] == 0


def test_day_29_still_waters_a_one_time_crop_for_its_same_day_bonus():
    # wheat planted 26 is in its watering window at age 3: WATER then HARVEST
    # on the final day pays one more unit (0.4's same-day chain, shifted by 4)
    view = _view(29, plants=[(0, spec.I_WHEAT, 26, 0, 2)])
    ops = _ops(view)
    assert ops[O.OP_WATER] == 1 and ops[O.OP_HARVEST] == 1


def test_day_29_buys_nothing_and_plants_nothing():
    view = _view(29, shed={spec.I_WHEAT: 5}, money=5000)
    macro = _macro(buy_land=np.int32(1), animal_count=np.int32(2),
                   plant_target=np.array([5, 0, 0, 0, 0], np.int32))
    plan = P.build_day(np, view, macro)
    op, qty = plan[3], plan[5]
    assert int(qty[O.TURN_BUY].sum()) == 0 and int((op[O.TURN_BUY] != O.MO_NONE).sum()) == 0
    assert int((plan[0] == O.OP_PLANT).sum()) == 0


def test_day_29_sells_the_shed_in_the_first_two_lots():
    view = _view(29, shed={spec.I_WOOL: 12, spec.I_EGG: 7})
    op, arg, qty = P.build_day(np, view, _macro())[3:6]     # default hold 10,000 is void on the final day
    sold = {t: {int(arg[t, s]): int(qty[t, s]) for s in range(spec.MAX_MARKET_ORDERS) if int(op[t, s]) == O.MO_SELL}
            for t in O.SELL_TURNS}
    assert sum(sold[O.SELL_TURNS[0]].values()) + sum(sold[O.SELL_TURNS[1]].values()) == 19
    assert sum(sold[O.SELL_TURNS[2]].values()) == 0            # lot 3 is for what the units drop (Task 3)


def test_plant_gate_and_free_slots_read_the_new_horizon():
    theta = np.zeros(PO.N_PARAMS, np.float32)
    z = np.zeros(100, np.int32)
    obs = brain.PolicyObs(
        day=np.int32(27), money=np.int32(3000), opp_money=np.int32(3000),
        kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        opp_kind=np.full(100, spec.KIND_EMPTY, np.int32), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))
    assert int(brain.decide(np, theta, obs).plant_target[spec.I_WHEAT]) > 0        # 27 + 2 <= 29
    assert int(brain.decide(np, theta, obs._replace(day=np.int32(28))).plant_target[spec.I_WHEAT]) == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_horizon_drop.py -q`
Expected: FAIL — `AttributeError: module 'kagg3.core.ops' has no attribute 'LAST_HARVEST_DAY'`.

- [ ] **Step 3: The constants**

Append to `src/kagg3/core/ops.py` after `LAST_SHED_DAY = 28`:

```python
# With DROP (PLANNER_V3_1 section 4) a harvest on day 29 still sells: the
# unit walks back to a shed-access tile, DROPs by DROP_DEADLINE_TURN and lot
# 3 sells it at SELL_TURNS[-1]. So the last day whose harvest can monetize is
# 29, and every terminal rule derives from it; LAST_SHED_DAY survives only
# where an end-of-day is literally required.
LAST_HARVEST_DAY = 29
# Units act before the market inside a turn, so a DROP at SELL_TURNS[-1]
# itself would also sell (verified, section 4); the deadline is held one turn
# earlier as a deliberate margin. Raising it to SELL_TURNS[-1] is a one-line,
# measurable change, not a law.
DROP_DEADLINE_TURN = SELL_TURNS[-1] - 1
# Worst-case return leg on the final day: eight moves from a corner to the
# nearest shed-access tile, plus the DROP.
RETURN_TURNS = 9
```

- [ ] **Step 4: Move every planner horizon to `LAST_HARVEST_DAY`**

In `src/kagg3/core/valuation.py` replace every `O.LAST_SHED_DAY` with `O.LAST_HARVEST_DAY` (in `animal_value`, `fert_marginal_value`, `new_plant_units`, `crop_remaining_value`; the fertilizer-collection term `xp.maximum(O.LAST_SHED_DAY - day, 0)` becomes `xp.maximum(O.LAST_HARVEST_DAY - day, 0)` — a collection on day 29 is dropped and sold the same day). Update the module docstring's calendar conventions accordingly.

In `src/kagg3/core/brain.py` replace `P.O.LAST_SHED_DAY` with `P.O.LAST_HARVEST_DAY` in `n_free_slots` and in the `can_mature` gate.

In `src/kagg3/core/plan.py::_derive`:
- `harvest_age = xp.clip(O.LAST_HARVEST_DAY - view.t_day, c_first, c_mxd)`;
- `survival_pays = day < O.LAST_HARVEST_DAY`;
- the Phase-1 `mandatory` term `((day >= O.LAST_SHED_DAY) & want_harvest)` becomes `((day >= O.LAST_HARVEST_DAY) & want_harvest)`;
- `h_next <= O.LAST_SHED_DAY` (CARE) and `bank_h <= O.LAST_SHED_DAY` (feed bank) become `<= O.LAST_HARVEST_DAY`;
- the acquisition block: `VAL.fires_between(xp, day, a_first, a_int, day + 1, O.LAST_HARVEST_DAY)`, `ub_fert = xp.maximum(O.LAST_HARVEST_DAY - day, 0)`, `ub_feeds = xp.maximum(O.LAST_HARVEST_DAY - day, 0) // 2`;
- rename the parameter `terminal` to `final` throughout `_derive` and `build_day` (`final = day >= O.LAST_HARVEST_DAY` in `build_day`); `money = xp.where(final, 0, ...)` stays (nothing bought on the final day); add `buy_land = xp.where(final, 0, buy_land)` right after the land grant, `plant_eff = xp.where(final, 0, plant_eff)` after `plant_eff = ...`, and `a_want = xp.where(final, 0, a_want)` after `a_want = ...`;
- add `final=final` to `Prefix` (new last field `final: object`).

In `src/kagg3/core/plan.py::build_day`:
- delete the three `unit_op = xp.where(terminal, O.OP_PASS, unit_op)` suppression lines (day-29 ops are wanted now);
- the hire enumeration's `n_hire = xp.where(terminal, 0, h_star)` becomes `n_hire = h_star` (the enumeration prices day-29 harvests);
- `hold = xp.where(final, SELL.LIQUIDATE, macro.hold)` stays **as Phase 2 wrote it** — `SELL.LIQUIDATE`, never `0`: an adjusted marginal can be ≤ 0 under `press`, and a `0` reservation would then leave units in the shed that Task 3's capacity law assumes are gone; the allocator call becomes `SELL.allocate(xp, price_table, view.mkt_inv, view.shops, avail, hold, macro.press, open_lots=xp.where(final, SELL.N_LOTS - 1, SELL.N_LOTS))`.

In `src/kagg3/core/sell.py::allocate` add the parameter `open_lots=N_LOTS` and, inside `body`, mask closed lots out of the argmax: after `adj = adjusted_marginals(...)` add `adj = xp.where(lot_ix < open_lots, adj, -(1 << 30))`; document: "`open_lots` closes the trailing lots — the final day reserves lot 3 for what the units drop".

- [ ] **Step 5: Update the tests whose numbers shift by a day**

Each of these pinned a 28-based horizon; update to the value the new horizon gives (all arithmetic is the same formulas with 29):
- `tests/test_valuation.py`: goose day 5 → `24 * 50 + 24 * 100`; the day-28 goose → replace with day 29 → 0; `fires_between(..., I(6), I(28))` vectorised test → keep (explicit bounds); tomato fertilized on day 28 planted 20 → now `60`; `test_fires_on_and_next_fire_after` unchanged.
- `tests/test_deadline_harvest.py`: wheat planted 25 → harvests on day 29 at age 4 (its max): `_view(day=29, ...)` gives `[WATER, HARVEST]`, day 28 gives `WATER` only; melon planted 17 → age 12 on day 29: harvest on 29, not 28; `test_brain_free_slots_count_the_deadline_tile` → 100 on day 29, 99 on day 28; `test_plant_gate_reads_the_horizon` → wheat plants on day 27, not 28.
- `tests/test_animal_acquisition_bound.py`: day 25 goose → 1 egg (day 29) + 4 fert − 300 − 2 × 25 = +100 → **bought**; the rejection cases move a day later: use day 26 for the rejected goose (0 eggs + 3 × 100 − 300 − 1 × 25 = −25) and day 25 for the accepted one; the fertilizer-price flip at day 26 (109 → +2, 108 → −1); sheep: placed 21 → wool day 27 → accepted, placed 24 → first wool day 30 → 5 × 100 − 500 − 2 × 25 → rejected.
- `tests/test_feed_care_cadence.py`: `test_no_survival_work_on_the_last_shed_day` → day 29 (was 28); `test_survival_work_still_runs_on_day_27` → day 28; `test_no_care_when_the_payout_is_past_the_horizon` → day 28 (payout day 30).
- `tests/test_fertilizer_value.py`: `test_day_28_same_day_chain_is_value_conditional` → the late wheat planted 26 on day 29 (harvest age 3).
- `tests/test_hire_enumeration.py`: `test_the_terminal_day_hires_nobody` → replace with `test_the_final_day_hires_for_its_harvest`: 100 ripe melons on day 29 → hires > 0.
- `tests/test_sell_side.py::test_day_29_liquidates_at_zero_reservation` → totals unchanged (12 wool, 3 melon) but assert they land in lots 1–2 only.
- `tests/test_budget_greedy.py::test_new_plant_units_at_the_spec_numbers`: wheat day 25 → 4 (age 4 on day 29), day 26 → 3, day 28 → 0; tomato day 19 → fires 27, 28, 29 → 3.
- `tests/test_admit_route.py::test_crop_remaining_value_at_the_spec_numbers`: the "cannot be harvested" case → wheat planted 28 seen 29 (age 1 < first) → 0.
- `tests/test_day29_endgame.py`: `test_day_29_emits_no_unit_ops` → replace with `test_day_29_emits_only_harvest_collect_and_return_ops` (asserted fully in Task 3; here assert no FEED/PLANT/BUILD/PLACE/PICKUP/CARE — WATER and FERTILIZE stay legal inside a same-day harvest chain); `test_day_29_hires_and_buys_nothing` → buys nothing (hires are allowed); `test_day_29_liquidates_the_whole_shed` → sold in lots 1–2.

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_horizon_drop.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass with the updated numbers; `test_sim_equivalence.py` passes (the planner now emits day-29 harvests but no DROP yet — harvested units sit in inventories at the end, which the harness compares field by field on both sides).
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add -A src/kagg3/core/ops.py src/kagg3/core/valuation.py src/kagg3/core/brain.py src/kagg3/core/plan.py src/kagg3/core/sell.py tests/
git commit -m "Re-derive every terminal rule from the DROP horizon: day-29 harvests sell"
```

---

### Task 3: The return leg, DROP emission and the capacity law (§4)

**Files:**
- Modify: `src/kagg3/core/plan.py` (`_routes`: final-day budget, return leg; `build_day`: per-product inflow, lot 3, capacity-limited admission)
- Modify: `tests/test_day29_endgame.py` (the Task-2 placeholder assertion becomes exact)
- Test: `tests/test_return_leg.py`

**Interfaces:**
- Consumes: `O.DROP_DEADLINE_TURN`, `O.RETURN_TURNS`, `Prefix.final`, `covered`, `d.chain_op`, `an_prod`/`crop` (per-tile product indices — expose `Prefix.product` int[100]: the product a tile's harvest yields, `crop` for plants, `an_prod` for animals, `I_FERT` placeholder for others).
- Produces: `_routes(..., final)` (extra trailing keyword `final=False`): on the final day every unit's budget is `DROP_DEADLINE_TURN + 1 − ROUTE_BASE` (16 turns), each block is charged `RETURN_TURNS`, and after its last tile the unit walks to the nearest shed-access tile and emits `OP_DROP`; `build_day` locals `inflow_by_product` (int[9]) and, on the final day, `lots[2] = inflow_by_product`; admission on the final day also stops at `SHED_CAPACITY − Σ shed[9:12] − Σ lots[1]` harvested-plus-collected units (capacity law); the hour-0 allocation (`wheat_reserved`, `avail`, `hold`, `lots = SELL.allocate(...)`) is hoisted above the admission because the law reads `lots[1]`.

**Background (§4).** DROP destroys what does not fit, so the plan must guarantee shed room before a DROP executes: on day 29 the hour-0 shed is sold in lots 1–2 (Task 2), but a unit whose block ends early DROPs as soon as turn 3, while lot 2's units are still in the shed until turn 10 — so the room a DROP can count on is `SHED_CAPACITY − animal items − Σ lots[1]`, and admission caps the day's harvested and collected units at that. (Early drops could also ride lot 2; not done here — lot 3 sells every drop, the conservative room keeps DROP from destroying anything.) The return leg: the nearest shed-access tile from `(x, y)` is `(clip(x, 4, 5), clip(y, 4, 5))`, at most 8 moves away; charging a constant `RETURN_TURNS = 9` keeps the block cost monotone in `e` (the exact walk is shorter or equal, so the DROP always lands by turn 17). Units carrying nothing still walk back and DROP — a no-op the engine ignores — which keeps the plan shape-static; the value of those turns is zero on the final day anyway.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_return_leg.py`:

```python
"""On the final day every unit harvests, walks back to a shed-access tile and
DROPs by turn 17 so that lot 3 sells what it carried (PLANNER_V3_1 section
4); admission never harvests more than the shed can take.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _final(ripe, crop=spec.I_TOMATO, units=1, shed=None, money=3000):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_yield = z - 1, z.copy()
    for pos in ripe:
        kind[pos], occ[pos], t_yield[pos] = spec.KIND_PLANT, crop, units
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in (shed or {}).items():
        sh[i] = n
    return P.DayView(
        day=np.int32(O.LAST_HARVEST_DAY), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(4), price=BASE.copy())


def _lot3(plan):
    op, arg, qty = plan[3:6]
    t = O.SELL_TURNS[-1]
    return {int(arg[t, s]): int(qty[t, s]) for s in range(spec.MAX_MARKET_ORDERS) if int(op[t, s]) == O.MO_SELL}


def test_every_working_unit_drops_by_the_deadline():
    plan = P.build_day(np, _final(range(0, 60, 2)), _macro())
    unit_op = plan[0]
    for u in range(spec.MAX_UNITS):
        row = [int(o) for o in unit_op[u]]
        if O.OP_HARVEST in row:
            drops = [t for t, o in enumerate(row) if o == O.OP_DROP]
            assert len(drops) == 1 and drops[0] <= O.DROP_DEADLINE_TURN
            assert max(t for t, o in enumerate(row) if o == O.OP_HARVEST) < drops[0]
            assert all(o == O.OP_PASS for o in row[drops[0] + 1:])


def test_the_farmer_walks_back_from_the_corner():
    # the final day has 16 route turns per unit; a corner tile costs 8 moves +
    # 1 harvest + 9 return = 18 and cannot be worked, a tile 3 moves out can
    plan = P.build_day(np, _final([0]), _macro())
    assert int((plan[0] == O.OP_HARVEST).sum()) == 0
    plan = P.build_day(np, _final([41]), _macro())         # (1, 4): 3 moves from the spawn
    row = [int(o) for o in plan[0][0]]
    assert row[2:5] == [O.OP_WEST] * 3 and row[5] == O.OP_HARVEST
    assert row[6:9] == [O.OP_EAST] * 3 and row[9] == O.OP_DROP


def test_lot_three_sells_exactly_what_is_dropped():
    plan = P.build_day(np, _final(range(44, 50), units=2), _macro())      # six tiles on the spawn row
    n = int((plan[0] == O.OP_HARVEST).sum())
    assert n == 6
    assert _lot3(plan) == {spec.I_TOMATO: 12}


def test_admission_never_exceeds_the_room_the_shed_will_have():
    # 40 melons at 6 units: 240 units, but two geese in the shed leave 98 slots
    plan = P.build_day(np, _final(range(40), crop=spec.I_MELON, units=6, shed={spec.I_GOOSE: 2}), _macro())
    harvested = int((plan[0] == O.OP_HARVEST).sum()) * 6
    assert harvested <= spec.SHED_CAPACITY - 2
    assert sum(_lot3(plan).values()) == harvested


def test_room_discounts_what_lot_two_still_holds_when_units_drop_early():
    # 100 wool in the hour-0 shed: the final-day liquidation splits it over
    # lots 1-2, and lot 2's share is still in the shed when the first DROPs
    # land (turn 3 at the earliest), so admission must leave room for it
    plan = P.build_day(np, _final(range(40), crop=spec.I_MELON, units=6, shed={spec.I_WOOL: 100}), _macro())
    lot2 = int(plan[5][O.SELL_TURNS[1]].sum())
    assert lot2 > 0
    harvested = int((plan[0] == O.OP_HARVEST).sum()) * 6
    assert 0 < harvested <= spec.SHED_CAPACITY - lot2


def test_return_leg_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _final(range(0, 60, 2)), _macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

Route arithmetic for the corner test: position 41 is on row 4 (even, x runs 0→9), tile (1, 4); the spawn is (4, 4): three WEST moves (turns 2–4), HARVEST on turn 5, three EAST moves back (6–8), DROP on turn 9. Position 0 is tile (0, 0): 8 moves + 1 harvest + 9 return = 18 > 16.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_return_leg.py -q`
Expected: FAIL — no `OP_DROP` anywhere; lot 3 empty.

- [ ] **Step 3: The return leg in `_routes`**

Change the signature to `_routes(xp, chain_op, chain_a, chain_q, n_ops, order, n_tasks, pick_masks, n_units, budget, final=False)`. Inside the unit loop:

```python
        bud = xp.where(u < n_units, budget, xp.asarray(0, i32)).astype(i32)
        ret = xp.where(final, O.RETURN_TURNS, 0).astype(i32)
        ...
        load = base + cum - cum[s] + d_pick + ret                          # the return leg is charged up front
```

and after `working = ...`/the route appends, add the return leg before `blk.append(...)`:

```python
        # Final day: after the block's last tile, walk to the nearest
        # shed-access tile -- (clip(x, 4, 5), clip(y, 4, 5)), horizontal
        # first -- and DROP. Charged as RETURN_TURNS above, so it always
        # lands by the deadline; units carrying nothing DROP harmlessly.
        cu_end = xp.where(active, cu[e], 0)
        lx, ly = tx[e], ty[e]
        gx = xp.clip(lx, spec.HALF - 1, spec.HALF)
        gy = xp.clip(ly, spec.HALF - 1, spec.HALF)
        ddx, ddy = gx - lx, gy - ly
        dist = xp.abs(ddx) + xp.abs(ddy)
        back = final & active & (r >= cu_end) & (r <= cu_end + dist)
        k_back = r - cu_end
        back_op = xp.where(k_back < xp.abs(ddx),
                           xp.where(ddx > 0, O.OP_EAST, O.OP_WEST),
                           xp.where(k_back < dist,
                                    xp.where(ddy > 0, O.OP_SOUTH, O.OP_NORTH),
                                    O.OP_DROP)).astype(i32)
        route_op[-1] = xp.where(back, back_op, route_op[-1]).astype(i32)
```

(`route_op[-1]` is the row appended for this unit; `route_a`/`route_q` stay 0 on those turns.) The `working` mask must not overlap: it already requires `r < cu_end`.

In `build_day` pass the budget and the flag: `budget = xp.where(final, O.DROP_DEADLINE_TURN + 1 - O.ROUTE_BASE, TPD - O.ROUTE_BASE).astype(i32)` (define it after `final`), and `_routes(..., n_units, budget, final=final)`. The return leg must also be charged where turns are *estimated*: define `per_unit = xp.where(final, budget - O.RETURN_TURNS, budget).astype(i32)` next to `budget`, use `labour = (h + 1) * per_unit - O.MAX_PICKUPS` in the hire enumeration and `labour = n_units * per_unit - O.MAX_PICKUPS` in the admission (both replace `budget` there and nowhere else). Then add the capacity law right after `cum_est`:

```python
    # Capacity law [4]: DROP destroys what does not fit. The first DROPs land
    # from turn 3, before lot 2 sells at turn 10, so the room a unit can count
    # on is the capacity less the animal items (never sold) and lot 2's units
    # (still in the shed). Admit no more harvested + collected units than that.
    units_by_rank = xp.where(d.task, d.t_units + d.t_coll, 0)[order_v]
    cum_units = xp.cumsum(units_by_rank)
    room = (spec.SHED_CAPACITY - xp.sum(view.shed[spec.I_GOOSE:].astype(i32))
            - xp.sum(lots[1])).astype(i32)
    n_fit = xp.where(final, _count_le(xp, cum_units, room), N_T)
    n_admit = xp.minimum(xp.minimum(_count_le(xp, cum_est, labour), n_fit), n_tasks).astype(i32)
```

`lots` must exist here: move the hour-0 sale lines (`wheat_reserved`, `avail`, the two `_set1`s, `fert_reserved`, `hold`, `lots = SELL.allocate(...)`) from the sale block to just above the admission — they read only `_derive` outputs and `view`; the forced-overflow addition and the lot-3 fill below stay in the sale block. For that, `_derive` exposes three more `Prefix` fields: `t_units` (int[100]: units a tile's *harvest* yields today — `t_yield + bonus_today` for harvested plants, `t_yield` for harvested animals, 0 otherwise), `t_coll` (int[100]: 1 on a tile with a fertilizer COLLECT, else 0 — an animal tile can carry both) and `product` (int[100]: `crop` for plants, `an_prod` for animals, `I_FERT` for a collect-only tile). Compute them next to `v_harvest` in the task-value block:

```python
    t_units = (xp.where(harvest_one | harvest_ong, view.t_yield + bonus_today, 0)
               + xp.where(want_harv_animal, view.t_yield, 0)).astype(i32)
    t_coll = want_collect.astype(i32)
    product = xp.where(is_plant, crop, xp.where(has_animal, an_prod, spec.I_FERT)).astype(i32)
```

(Collections are one fertilizer each and are counted separately — `t_coll` in the room check, `has_coll` in the per-product inflow — because an animal tile's `product` is its own product, not fertilizer.)

Then, in the sale block, replace the scalar inflow with a per-product one and fill lot 3 on the final day:

```python
    has_harv = xp.sum((d.chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0
    has_coll = xp.sum((d.chain_op == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
    onehot = (d.product[:, None] == xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :]).astype(i32)
    inflow_by_product = (xp.sum(onehot * xp.where(covered & has_harv, d.t_units, 0)[:, None], axis=0)
                         + (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT).astype(i32)
                         * xp.sum((covered & has_coll).astype(i32)))
    inflow = xp.sum(inflow_by_product)
    ...
    lots = (lots + (lot_ix == forced_lot[None, :]).astype(i32) * forced[None, :]).astype(i32)
    # Final day: lot 3 sells what the units drop by turn 17 [4].
    last = (xp.arange(SELL.N_LOTS, dtype=i32) == SELL.N_LOTS - 1).astype(i32)[:, None]
    lots = xp.where(final, lots + last * inflow_by_product[None, :], lots).astype(i32)
```

(the Phase-0 overflow projection keeps using the scalar `inflow`; on the final day `proj_eod` is moot — no eod — and `forced` is zero because `SELL.LIQUIDATE` already put everything sellable in lots 1–2.)

In `tests/test_day29_endgame.py` make `test_day_29_emits_only_harvest_collect_and_return_ops` exact: the allowed op set on day 29 is `{PASS, moves, HARVEST, COLLECT_FERTILIZER, DROP, WATER, FERTILIZE}` — WATER and FERTILIZE only as part of a same-day harvest chain (Task 2): assert every WATER/FERTILIZE a unit emits is followed later in that unit's row by a HARVEST before its DROP, and that no FEED, CARE, PLANT, BUILD_*, PLACE or PICKUP appears.

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_return_leg.py tests/test_day29_endgame.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass. **`test_sim_equivalence.py` and `test_trained_equivalence.py` are the gate for this task**: every game now ends with DROPs into sheds that are often full, so Task 1's overflow semantics are exercised end to end; a divergence there is a bug in Task 1 or here, never in the engine.
Run: `python scripts/bench_sim.py` here and on the Task-2 commit; record both.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_return_leg.py tests/test_day29_endgame.py
git commit -m "Walk back and DROP on the final day so lot 3 sells the last harvest; cap it at the shed's room"
```

---

### Task 4: M1 — prospective post-purchase land tasks (§0.3, §5)

**Files:**
- Modify: `src/kagg3/core/brain.py` (`n_free_slots`, `decide`), `src/kagg3/core/plan.py` (`_derive`: prospective free slots)
- Test: `tests/test_prospective_land.py`

**Interfaces:**
- Consumes: `buy_land` (granted in `_derive` ahead of the greedy), `view.nquad`, `spec.LAND_ORDER`, `plan.SERP_QUAD` (re-add it: `SERP_QUAD = spec.TILE_QUAD[SERP].astype(np.int32)` — Phase 2 Task 6 deleted it), `free_slot`, `n_free`.
- Produces: `brain.n_free_slots(xp, obs, land=None)` — with `land` (0/1 scalar) the next quadrant's 25 tiles count as free; `brain.decide` predicts the land grant (`head[1]` logit, `nquad < 4`, `money >= land_cost`) and sizes `dev_frac`/`plant_total` on the enlarged count; `_derive` locals `next_quad`, `prospective` (bool[100]).

**Background (§0.3, M1).** The engine unlocks the quadrant synchronously in the market phase of the purchase turn; movement is never blocked by LOCKED; units act on every later turn. The quadrant identity (`LAND_ORDER[nquad − 1]`) and the purchase's success (affordability, asserted by the walk) are both known at hour 0, so the new quadrant's 25 tiles are free slots today — currently 22 turns are wasted per purchase. Two halves: the decision head must *count* them (otherwise `plant_target` never exceeds the old free tiles and nothing is planted there), and task derivation must *use* them. With BUY_LAND on turn 1 (until Task 5) the tiles accept ops from turn 2, i.e. from the first route turn.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_prospective_land.py`:

```python
"""A quadrant bought this morning is developed this afternoon (PLANNER_V3_1
section 0.3 / M1): the decision head counts its 25 tiles as free when it
predicts the grant, and task derivation plants and builds on them.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
NE = 1                                             # LAND_ORDER[0]


def _view(money=3000, seeds=0):
    """NW unlocked and fully planted with strawberries (no free tile), the rest LOCKED."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    occ = z - 1
    nw = P.SERP_QUAD == 0
    kind[nw] = spec.KIND_PLANT
    occ[nw] = spec.I_STRAWBERRY
    return P.DayView(
        day=np.int32(3), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.full(spec.N_CROPS, seeds, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _tiles_worked(plan, op):
    """Serpentine positions of the tiles where `op` is executed, from the route."""
    unit_op = plan[0]
    return int((unit_op == op).sum())


def test_plantings_land_on_the_new_quadrant_the_same_day():
    view = _view(seeds=10)
    with_land = P.build_day(np, view, _macro(buy_land=np.int32(1), plant_target=np.array([10, 0, 0, 0, 0], np.int32)))
    without = P.build_day(np, view, _macro(buy_land=np.int32(0), plant_target=np.array([10, 0, 0, 0, 0], np.int32)))
    assert _tiles_worked(with_land, O.OP_PLANT) == 10
    assert _tiles_worked(without, O.OP_PLANT) == 0


def test_builds_land_on_the_new_quadrant_too():
    view = _view(money=3000)
    plan = P.build_day(np, view, _macro(buy_land=np.int32(1), animal_count=np.int32(2)))
    assert _tiles_worked(plan, O.OP_BUILD_COOP) == 2 and _tiles_worked(plan, O.OP_PLACE) == 2


def test_nothing_prospective_when_the_purse_cannot_pay():
    view = _view(money=500, seeds=10)
    plan = P.build_day(np, view, _macro(buy_land=np.int32(1), plant_target=np.array([10, 0, 0, 0, 0], np.int32)))
    assert _tiles_worked(plan, O.OP_PLANT) == 0
    assert int(plan[5][O.TURN_BUY][plan[3][O.TURN_BUY] == O.MO_BUY_LAND].sum()) == 0


def test_the_decision_head_counts_the_prospective_tiles():
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD == 0] = spec.KIND_PLANT
    occ = np.where(kind == spec.KIND_PLANT, spec.I_STRAWBERRY, -1).astype(np.int32)
    obs = brain.PolicyObs(
        day=np.int32(3), money=np.int32(3000), opp_money=np.int32(3000),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))
    assert int(brain.n_free_slots(np, obs)) == 0
    assert int(brain.n_free_slots(np, obs, land=np.int32(1))) == 25
    # a theta whose land logit is high plans development on the prospective tiles
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 1] = 10.0
    m = brain.decide(np, theta, obs)
    assert int(m.buy_land) == 1 and int(m.plant_target.sum() + m.animal_count) > 0
    assert int(brain.decide(np, theta, obs._replace(money=np.int32(500))).plant_target.sum()) == 0


def test_prospective_land_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(seeds=10), _macro(buy_land=np.int32(1), plant_target=np.array([10, 0, 0, 0, 0], np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_prospective_land.py -q`
Expected: FAIL — no PLANT with land (`0 == 10`); `n_free_slots() got an unexpected keyword argument 'land'`.

- [ ] **Step 3: Count the prospective tiles in the decision head**

In `src/kagg3/core/brain.py` change `n_free_slots`:

```python
def n_free_slots(xp, obs: PolicyObs, land=None):
    """Tiles the planner will treat as developable today. With `land` (0/1)
    the next quadrant's tiles count too: the walk grants a requested,
    affordable quadrant ahead of everything else and the engine unlocks it in
    the purchase turn, so it is developed the same day (M1).
    ...
    """
    ...
    free = (obs.kind == spec.KIND_EMPTY) | (obs.kind == spec.KIND_WEED) | harvest_one
    n = xp.sum(free.astype(xp.int32))
    if land is not None:
        nxt = xp.asarray(spec.LAND_ORDER)[xp.clip(obs.nquad - 1, 0, 2)]
        pros = (obs.kind == spec.KIND_LOCKED) & (xp.asarray(spec.TILE_QUAD) == nxt)
        n = n + land.astype(xp.int32) * xp.sum(pros.astype(xp.int32))
    return n
```

In `decide`, move the `land_cost`/`afford`/`buy_land` lines above `n_free = n_free_slots(xp, obs)` and change that line to:

```python
    land_ok = (buy_land > 0) & (obs.nquad < 4) & (obs.money >= land_cost)
    n_free = n_free_slots(xp, obs, land=land_ok.astype(i32))
```

(`land_cost` there is float32; compare `obs.money.astype(xp.float32) >= land_cost`.)

- [ ] **Step 4: Use the prospective tiles in task derivation**

In `plan.py` re-add `SERP_QUAD = spec.TILE_QUAD[SERP].astype(np.int32)` next to `SERP_X`/`SERP_Y`. In `_derive`, directly after `purse = (purse - buy_land * land_cost).astype(i32)`, add:

```python
    # Prospective post-purchase land [LAW + module, 0.3 / M1]: the quadrant
    # is LAND_ORDER[nquad - 1], unlocked in the purchase turn, and units act
    # on every later turn -- its 25 tiles are free slots today.
    next_quad = xp.asarray(spec.LAND_ORDER)[xp.clip(view.nquad - 1, 0, 2)]
    prospective = (kind == spec.KIND_LOCKED) & (xp.asarray(SERP_QUAD) == next_quad) & (buy_land > 0)
    free_slot = free_slot | prospective
    n_free = xp.sum(free_slot.astype(i32))
```

Then, directly after those four lines, re-size the animal want on the enlarged count — `a_want = xp.minimum(macro.animal_count, n_free) + n_struct_free` (and `a_want = xp.where(final, 0, a_want)` again) — so the greedy, which runs after the land grant, can buy animals for the new quadrant; without this `test_builds_land_on_the_new_quadrant_too` fails (pre-purchase `n_free` is 0 there). (`slot_rank`, `n_build`, `plant_here` and `build_here` in the clamp section read `free_slot`/`n_free` after this point.)

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_prospective_land.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass; the equivalence games now plant on freshly bought quadrants and the engine accepts those ops from turn 2 because BUY_LAND resolves at turn 1.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/brain.py src/kagg3/core/plan.py tests/test_prospective_land.py
git commit -m "Develop a quadrant the day it is bought: count and use its tiles as free slots"
```

---

### Task 5: M2 — land funded by lot-1 revenue at turn 2 (§5, §6.1)

**Files:**
- Modify: `src/kagg3/core/plan.py` (`_derive`: provisional lot-1 revenue, land purse; `_market`: BUY_LAND in turn-2 slot 9; `build_day`: one idle turn on land days)
- Test: `tests/test_land_at_turn_two.py`

**Interfaces:**
- Consumes: `sell.allocate`, `feed_need`, `n_fert_want`, `view.shed`, `macro.hold/press`, `land_cost`, `money`; `n_pick` in `build_day`.
- Produces: `_derive` locals `avail_prov` (int[9]), `lots_prov` (int[3, 9]), `rev1` (int scalar: projected lot-1 revenue), `plan.LAND_REV_NUM, plan.LAND_REV_DEN = 3, 4` (the share of projected lot-1 revenue the grant may count on), the land grant `money + rev1 >= land_cost` where `rev1` is already discounted by that share, `purse = money - max(land_cost - rev1, 0)`; `_market` emits `MO_BUY_LAND` at `(TURN_SELL, MO - 1)` and never at `TURN_BUY`; `build_day` charges `buy_land` as one leading idle turn per unit (`lead = n_pick + d.buy_land`, route budget `budget - d.buy_land`).

**Background (M2).** Turn 2 carries nine SELL slots and one free; the engine resolves slots in order and the sim runs the full market path on hours < 3, so a BUY_LAND in slot 9 of turn 2 is legally funded by lot-1 revenue with no sim change. Funding must be *safe*: the provisional allocation uses `avail_prov = shed − feed_need·e_wheat − n_fert_want·e_fert` (the largest reservations the walk can make), so the final allocation — with reservations no larger — sells at least as much in lot 1. That is safe against *own* reservations only: the projection is opponent-free (§1.1), and the opponent's lockstep sales at the same turn 2 lower the later quotes seat 0 receives, so the engine can bank less than the projection. A BUY_LAND that then fails is not a marginal price miss — every M1 prospective op that day no-ops on LOCKED tiles with its seeds and animals already bought. So `rev1` counts only `LAND_REV_NUM/LAND_REV_DEN` (3/4) of the projected lot-1 revenue [HEURISTIC, measured in Task 9; the residual above that margin is the genes' to absorb, the §1.1 honesty rule]. The unlock now happens in the market phase of turn 2, after that turn's unit phase, so a unit standing on a prospective tile at turn 2 (three spawn tiles lie outside NW) would fail its op: every unit idles one turn on a land day. Moving *more* of the BUY row after the sells would need a new market turn and is out of scope (§6.1).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_land_at_turn_two.py`:

```python
"""BUY_LAND rides the free tenth slot of turn 2, after the nine sells, and is
funded by lot-1 revenue (PLANNER_V3_1 M2): a purse short of the land price
still buys the quadrant when the morning sale covers the gap, and the turn-1
purchases never spend what the land needs.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(money, wool=0, geese_hungry=0):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_cons = z - 1, z.copy()
    kind[:geese_hungry] = spec.KIND_COOP
    occ[:geese_hungry] = 0
    t_cons[:geese_hungry] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = wool
    return P.DayView(
        day=np.int32(3), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=t_cons,
        t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _land_slot(plan):
    op = plan[3]
    where = [(t, s) for t in range(spec.TURNS_PER_DAY) for s in range(spec.MAX_MARKET_ORDERS)
             if int(op[t, s]) == O.MO_BUY_LAND]
    return where


def test_land_is_ordered_after_the_sells_of_turn_two():
    plan = P.build_day(np, _view(3000), _macro(buy_land=np.int32(1)))
    assert _land_slot(plan) == [(O.TURN_SELL, spec.MAX_MARKET_ORDERS - 1)]


def test_the_morning_sale_funds_the_quadrant():
    # 600 coins and 20 wool (~4,000 at lot 1 with zero reservation, ~3,000 after
    # the 3/4 margin): land is bought
    plan = P.build_day(np, _view(600, wool=20), _macro(buy_land=np.int32(1), hold=np.zeros(9, np.int32)))
    assert _land_slot(plan) == [(O.TURN_SELL, spec.MAX_MARKET_ORDERS - 1)]
    # with everything held there is no lot-1 revenue and 600 cannot pay
    assert _land_slot(P.build_day(np, _view(600, wool=20), _macro(buy_land=np.int32(1)))) == []


def test_turn_one_purchases_leave_the_land_its_gap():
    # 1,100 coins, 4 hungry geese (4 wheat at ~25), no revenue: the greedy may
    # spend at most 100 at turn 1
    plan = P.build_day(np, _view(1100, geese_hungry=4), _macro(buy_land=np.int32(1)))
    op, arg, qty = plan[3:6]
    spent = sum(int(qty[O.TURN_BUY, s]) * int(BASE[int(arg[O.TURN_BUY, s])]) for s in range(spec.MAX_MARKET_ORDERS)
                if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT)
    assert 0 < spent <= 100
    assert _land_slot(plan) == [(O.TURN_SELL, spec.MAX_MARKET_ORDERS - 1)]


def test_units_idle_one_turn_on_a_land_day():
    z = np.zeros(100, np.int32)
    view = _view(3000)
    kind = view.kind.copy()
    kind[:10] = spec.KIND_PLANT
    occ = view.occ.copy()
    occ[:10] = spec.I_TOMATO
    t_yield = z.copy()
    t_yield[:10] = 1
    view = view._replace(kind=kind, occ=occ, t_yield=t_yield, day=np.int32(13))
    land = P.build_day(np, view, _macro(buy_land=np.int32(1)))[0]
    no_land = P.build_day(np, view, _macro(buy_land=np.int32(0)))[0]
    assert int(land[0, O.ROUTE_BASE]) == O.OP_PASS
    assert int(no_land[0, O.ROUTE_BASE]) != O.OP_PASS
    assert land[0, O.ROUTE_BASE + 1:].tolist()[:20] == no_land[0, O.ROUTE_BASE:].tolist()[:20]


def test_land_at_turn_two_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(600, wool=20), _macro(buy_land=np.int32(1), hold=np.zeros(9, np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_land_at_turn_two.py -q`
Expected: FAIL — BUY_LAND sits at `(TURN_BUY, 8)`; the 600-coin farm buys no land.

- [ ] **Step 3: Provisional lot-1 revenue and the land purse**

In `_derive`, replace the land grant lines

```python
    purse = money
    buy_land = ((macro.buy_land > 0) & (view.nquad < 4) & (purse >= land_cost)).astype(i32)
    purse = (purse - buy_land * land_cost).astype(i32)
```

with:

```python
    # Liquidity resequencing [M2]: BUY_LAND rides turn 2's free slot after the
    # nine sells, so lot-1 revenue can fund it. The provisional allocation
    # reserves the *most* the walk could (every passing feed's wheat, every
    # application's fertilizer), so the final lot 1 sells at least as much
    # and the engine sees at least `rev1`. Turn-1 purchases are then capped
    # so that money - spend + rev1 still covers the land.
    e_wheat = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_WHEAT).astype(i32)
    e_fert = (xp.arange(spec.N_PRODUCTS, dtype=i32) == spec.I_FERT).astype(i32)
    avail_prov = xp.maximum(view.shed[:spec.N_PRODUCTS].astype(i32)
                            - e_wheat * feed_need - e_fert * n_fert_want, 0)
    hold_now = xp.where(final, SELL.LIQUIDATE, macro.hold).astype(i32)
    lots_prov = SELL.allocate(xp, price_table, view.mkt_inv, view.shops, avail_prov, hold_now, macro.press,
                              open_lots=xp.where(final, SELL.N_LOTS - 1, SELL.N_LOTS))
    q1 = PJ.sell_quotes(xp, price_table, PJ.projected_inv(xp, view.mkt_inv, view.shops, O.SELL_TURNS[0]))
    # Opponent-free projection: the other seat's lockstep sales at turn 2 can
    # lower what lot 1 actually banks, and a failed BUY_LAND wastes the whole
    # prospective day (M1). Count only LAND_REV_NUM/LAND_REV_DEN of it.
    rev1 = ((xp.sum(PJ.sell_revenue(xp, q1, lots_prov[0])) * LAND_REV_NUM) // LAND_REV_DEN).astype(i32)
    buy_land = ((macro.buy_land > 0) & (view.nquad < 4) & (money + rev1 >= land_cost) & ~final).astype(i32)
    purse = (money - buy_land * xp.maximum(land_cost - rev1, 0)).astype(i32)
```

(`PJ.sell_revenue(xp, quotes, qty)` is Phase 0's projector function; Task 2's `open_lots` keyword on `allocate`. Define `LAND_REV_NUM, LAND_REV_DEN = 3, 4` next to `EST_MOVES` with a comment naming the residual.) Delete the Task-2 line `buy_land = xp.where(final, 0, buy_land)` — the grant now carries `~final`.

In `_market`, remove `B_LAND` from the turn-1 row (drop it from the `per_cat`/`DEFAULT_ORDER` iteration — keep the constant for the walk-side comment but build the turn-1 row from `(B_WHEAT, B_FERT, B_SEEDS, B_ANIMAL)`), and after the SELL loop add:

```python
    # BUY_LAND in the free tenth slot of turn 2, after the nine sells [M2]:
    # the engine resolves slots in order, so lot-1 revenue is already banked.
    land_slot = xp.arange(MO, dtype=i32) == MO - 1
    op = _row(xp, op, O.TURN_SELL,
              xp.where(land_slot & (buy_land > 0), O.MO_BUY_LAND, op[O.TURN_SELL]).astype(i32))
```

In `build_day`, charge the idle turn: after `n_pick` comes back from `_routes`, use `lead = (n_pick + d.buy_land).astype(i32)` in `r = t - (O.ROUTE_BASE + lead[:, None])` and `on_route = (r >= 0) & (r < budget - lead[:, None])`, pass `budget - d.buy_land` as the budget to `_routes` (and to the admission `labour`), and shift the pickup turns by the same lead: `pk_turn = xp.cumsum(pk_active, axis=0) - pk_active + O.ROUTE_BASE + d.buy_land` (pickups need the shed, not the land, but keeping every unit's schedule aligned is simplest and costs the same one turn).

Update the module docstring's intra-day layout: `turn 1: BUY_PRODUCT x2, BUY_SEED x5, BUY_ANIMAL x1` and `turn 2: SELL x9 (lot 1), BUY_LAND`, and the `ops.py` schedule comment likewise (it is now *correct* about BUY_LAND being on turn 2 — the Phase-0 fix moved it to turn 1; move it back with a note that M2 restored it deliberately).

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_land_at_turn_two.py tests/test_prospective_land.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass; `test_budget_order.py`'s land tests still hold (money 1,000 with no revenue → land granted, nothing else); `test_hire_bill.py` reads land from the turn-2 row now — update its `_buy_bill` to sum `BUY_LAND` from `O.TURN_SELL` as well; the equivalence games buy land at turn 2 and the engine's `_do_buy_land` at index 9 sees the lot-1 proceeds.
Run: `python scripts/bench_sim.py` here and on the Task-4 commit (a second allocator run per day); record both.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py src/kagg3/core/ops.py tests/test_land_at_turn_two.py tests/test_hire_bill.py
git commit -m "Order land after the turn-2 sells so lot-1 revenue funds it"
```

---

### Task 6: M3 — structure conversion and reclamation via DIG (§5)

**Files:**
- Modify: `src/kagg3/core/plan.py` (`_derive`: `free_slot` includes empty mismatched structures, `dig_here`, slot ranking prefers true free tiles)
- Test: `tests/test_dig_conversion.py`

**Interfaces:**
- Consumes: `free_struct`, `struct_ok`, `is_weed`, `plant_here`, `build_here`, `_rank_by`.
- Produces: `_derive` locals `reclaimable = free_struct & ~struct_ok` (an empty structure of the other kind), `free_slot = is_empty | is_weed | harvest_one | reclaimable`, `slot_rank = _rank_by(xp, free_slot, slot_pref)` with `slot_pref = 1` on tiles that need no DIG and `0` on structures, `dig_here = is_weed | (is_struct & (plant_here | build_here))`.

**Background (M3).** DIG removes living plants, weeds and empty structures in both engine and sim; only an occupied structure resists, and there is no other demolition op. So coop↔pasture conversion (DIG, BUILD the other kind, PLACE) and reclaiming a dead structure for a crop (DIG, PLANT, WATER) are two-turn operations the planner never had. Empty structures of the day's kind are still stocked directly (`struct_ok`); empty structures of the *other* kind join the free slots behind every true free tile, so they are dug only when the true free tiles run out — the value of the planting or placement pays for the extra turn through the admit stage, and the chain order DIG → BUILD → PLACE → PLANT → WATER is already the packing order.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_dig_conversion.py`:

```python
"""Empty structures of the wrong kind are dug and rebuilt or replanted
(PLANNER_V3_1 M3) once the true free tiles run out: coop <-> pasture
conversion and dead-structure reclamation are two-turn operations.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
MOVES = (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST, O.OP_PICKUP)


def _view(structures, free_tiles=0, seeds=0, geese=0):
    """`structures`: position -> kind (an empty coop or pasture). Every other
    tile holds a strawberry except `free_tiles` empty ones after them."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_PLANT, np.int32)
    occ = np.full(100, spec.I_STRAWBERRY, np.int32)
    for pos, k in structures.items():
        kind[pos], occ[pos] = k, -1
    n_struct = len(structures)
    for pos in range(n_struct, n_struct + free_tiles):
        kind[pos], occ[pos] = spec.KIND_EMPTY, -1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = geese
    return P.DayView(
        day=np.int32(5), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.full(spec.N_CROPS, seeds, np.int32),
        money=np.int32(0), nquad=np.int32(4), price=BASE.copy())


def _farmer_ops(plan):
    return [int(o) for o in plan[0][0] if int(o) not in MOVES]


def test_a_pasture_is_converted_into_a_coop_for_a_goose():
    view = _view({0: spec.KIND_PASTURE}, geese=1)
    ops = _farmer_ops(P.build_day(np, view, _macro(animal_kind=np.int32(0), animal_count=np.int32(1))))
    assert ops == [O.OP_DIG, O.OP_BUILD_COOP, O.OP_PLACE]


def test_a_dead_coop_is_reclaimed_for_a_crop():
    view = _view({0: spec.KIND_COOP}, seeds=1)
    ops = _farmer_ops(P.build_day(np, view, _macro(plant_target=np.array([1, 0, 0, 0, 0], np.int32))))
    assert ops == [O.OP_DIG, O.OP_PLANT, O.OP_WATER]


def test_true_free_tiles_are_used_before_any_structure_is_dug():
    view = _view({0: spec.KIND_COOP}, free_tiles=1, seeds=1)
    ops = _farmer_ops(P.build_day(np, view, _macro(plant_target=np.array([1, 0, 0, 0, 0], np.int32))))
    assert O.OP_DIG not in ops and ops == [O.OP_PLANT, O.OP_WATER]


def test_a_matching_empty_structure_is_stocked_not_dug():
    view = _view({0: spec.KIND_COOP}, geese=1)
    ops = _farmer_ops(P.build_day(np, view, _macro(animal_kind=np.int32(0), animal_count=np.int32(1))))
    assert ops == [O.OP_PLACE]


def test_conversion_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view({0: spec.KIND_PASTURE, 1: spec.KIND_COOP}, geese=2), \
        _macro(animal_kind=np.int32(0), animal_count=np.int32(2))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

Fixture note: `money=0`, so no purchases; the goose and the seed are already held, and strawberries are ongoing crops (occupied filler, per the fixture rule). Position 0 is tile (0, 0), eight moves from the spawn — the chain fits the 22-turn budget.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_dig_conversion.py -q`
Expected: FAIL — the pasture is neither dug nor built on (`[] == [DIG, BUILD_COOP, PLACE]`).

- [ ] **Step 3: Structures as free slots behind the true free tiles**

In `_derive`, after `struct_ok = ...` and `n_struct_free = ...`, redefine the free slots:

```python
    # Structure conversion and reclamation via DIG [M3]: an empty structure
    # of the other kind is a free slot behind every true free tile -- dug,
    # then built or planted on -- and a dead structure is reclaimed the same
    # way. Matching empty structures are stocked directly, never dug.
    reclaimable = free_struct & ~struct_ok
    free_slot = is_empty | is_weed | harvest_one | reclaimable
    n_free = xp.sum(free_slot.astype(i32))
    slot_pref = (~reclaimable).astype(i32)                 # true free tiles rank first
```

(this replaces the earlier `free_slot = is_empty | is_weed | harvest_one` and `n_free` lines; Task 4's prospective extension then reads `free_slot = free_slot | prospective` after the walk and must also extend `slot_pref` — prospective tiles are true free tiles: `slot_pref = xp.where(prospective, 1, slot_pref)`). In the clamp section replace `slot_rank = _rank(xp, free_slot)` with `slot_rank = _rank_by(xp, free_slot, slot_pref)`, and replace the DIG candidate `(is_weed, xp.full((N_T,), O.OP_DIG, i32), zero, zero)` with:

```python
        (dig_here,      xp.full((N_T,), O.OP_DIG, i32),          zero, zero),
```

where, just above `cands`, `dig_here = is_weed | (is_struct & (plant_here | build_here))`.

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_dig_conversion.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass; `test_animal_count_semantics.py` (free coops of the *matching* kind) is unaffected; the equivalence games exercise DIG on structures, which both engine and sim already implement.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_dig_conversion.py
git commit -m "Convert and reclaim empty structures with DIG once the free tiles run out"
```

---

### Task 7: The turn-time walk-and-cap lot guard (§3)

**Files:**
- Create: `src/kagg3/core/guard.py`
- Modify: `src/kagg3/core/plan.py` (`build_day` returns a seventh array `mkt_floor`; `_market` emits `MO_SELL` placeholders and floors), `src/kagg3/agent/render.py` (zero-quantity SELL kept), `src/kagg3/agent/runtime.py` (cap at turns 10/18), `src/kagg3/sim/rollout.py` (`compact_orders` on four arrays; cap before the sell-only market), `scripts/package_submission.py` (**add `("core/guard.py", "kagg3/core/guard.py")` to its explicit `INCLUDE` list** — the archive is built from that list, not the package tree, and a missing module makes the packaged agent throw on import, which the leaderboard scores as a silent 3,000 coins); `scripts/eval_vs_baselines.py` needs nothing (`runtime.act` owns the plan tuple)
- Modify tests that unpack six plan arrays: `tests/test_day29_endgame.py` (`unit_op, _, _, op, arg, qty = P.build_day(...)` → index the tuple), `tests/test_sim_equivalence.py` (add the two-theta game)
- Test: `tests/test_walk_and_cap.py`

**Interfaces:**
- Produces: `guard.cap_row(xp, price_table, mkt_inv, op_row, arg_row, qty_row, floor_row) -> int[MO]` (for every `MO_SELL` slot, the largest quantity ≤ planned whose every unit's live quote clears the floor); `build_day(...) -> (unit_op, unit_a, unit_q, mkt_op, mkt_a, mkt_q, mkt_floor)` with `mkt_floor` int32[TPD, MO] (`hold + press × lot_index` on SELL rows, 0 elsewhere); `_market(..., lots, n_hire, floors)` with `floors` int[3, 9]; SELL rows carry `MO_SELL` in all nine product slots (quantity possibly 0) so indices never shift; `render.market_actions` emits `["SELL", item, 0]` for a zero lot; `runtime.Runtime.act` caps at `hour in SELL_TURNS[1:]` from `parse.parse_market(obs)[0]`; `rollout.compact_orders(mop, ma, mq, mfloor)` and the cap applied per seat before `_market_turn(..., sell_only=True)`.

**Background (§3).** At turns 10 and 18 the executor observes the live market; it walks the current quote curve and caps the lot at the largest quantity whose marginal price clears the lot's planned adjusted floor — strictly stronger than zeroing on the first quote. Verified on both sides: the engine parses `SELL item 0` as an inert order that keeps its list index, and the sim's compaction and resolution agree — *provided the zeroed lot is emitted as a kept `SELL item 0` placeholder with `op = MO_SELL`*. Today a zero lot is `MO_NONE` and the renderer drops it, compacting the list and shifting the pairing of the two seats' orders. Both seats read the same pre-turn inventory (the agent's observation at turn *t* is the state after turn *t−1*'s town tick, which is `st.mkt_inv` at the start of the sim's turn body), so the cap is identical on both sides. An inert order still counts against the ten-order cap: nine sells plus M2's land order is exactly ten.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_walk_and_cap.py`:

```python
"""At turns 10 and 18 a lot is capped at the largest quantity whose live
quotes clear its planned floor (PLANNER_V3_1 section 3); a zeroed lot is
emitted as a kept SELL-0 placeholder so the two seats' orders stay paired.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.agent import render, runtime
from kagg3.core import guard
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ

TABLE = spec.build_price_table()
I0 = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
MO = spec.MAX_MARKET_ORDERS


def _row(product, qty, floor):
    op = np.zeros(MO, np.int32)
    arg = np.zeros(MO, np.int32)
    q = np.zeros(MO, np.int32)
    f = np.zeros(MO, np.int32)
    op[:spec.N_PRODUCTS] = O.MO_SELL
    arg[:spec.N_PRODUCTS] = np.arange(spec.N_PRODUCTS)
    q[product], f[product] = qty, floor
    return op, arg, q, f


def test_cap_is_the_count_of_units_clearing_the_floor():
    op, arg, q, f = _row(spec.I_WOOL, 20, 190)
    quotes = PJ.sell_quotes(np, TABLE, I0)[spec.I_WOOL]
    expect = int((quotes[:20] >= 190).sum())
    assert 0 < expect < 20
    got = guard.cap_row(np, TABLE, I0, op, arg, q, f)
    assert int(got[spec.I_WOOL]) == expect and int(got.sum()) == expect


def test_a_floor_nobody_clears_zeroes_the_lot_and_keeps_its_slot():
    op, arg, q, f = _row(spec.I_WOOL, 20, 10_000)
    got = guard.cap_row(np, TABLE, I0, op, arg, q, f)
    assert int(got.sum()) == 0
    actions = render.market_actions(op[None, :], arg[None, :], got[None, :], 0)
    assert actions[spec.I_WOOL] == ["SELL", "WOOL", 0] and len(actions) == spec.N_PRODUCTS


def test_a_lower_live_inventory_raises_the_cap():
    op, arg, q, f = _row(spec.I_WOOL, 20, 190)
    low = I0.copy()
    low[spec.I_WOOL] -= 30                                # the town ate thirty wool
    assert int(guard.cap_row(np, TABLE, low, op, arg, q, f)[spec.I_WOOL]) > \
        int(guard.cap_row(np, TABLE, I0, op, arg, q, f)[spec.I_WOOL])


def test_build_day_emits_floors_and_placeholders():
    z = np.zeros(100, np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = 12
    view = P.DayView(
        day=np.int32(3), kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32))
    hold = np.full(9, 150, np.int32)
    press = np.full(9, 7, np.int32)
    plan = P.build_day(np, view, _macro(hold=hold, press=press), TABLE)
    assert len(plan) == 7
    op, floor = plan[3], plan[6]
    for k, t in enumerate(O.SELL_TURNS):
        assert np.all(op[t, :spec.N_PRODUCTS] == O.MO_SELL)          # placeholders keep every index
        assert floor[t, :spec.N_PRODUCTS].tolist() == [150 + 7 * k] * spec.N_PRODUCTS
    assert int(floor[O.TURN_BUY].sum()) == 0


def test_forced_overflow_units_are_never_capped():
    # tests/test_sell_side.py's overflow fixture: 95 wool in the shed, 20
    # tomatoes harvested tonight, everything held -- 15 units are forced out.
    # The slot carrying them gets the LIQUIDATE floor, so a moving market
    # cannot push them back into a shed that has no room for them
    from kagg3.core import sell as S
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:20] = spec.KIND_PLANT
    occ = z - 1
    occ[:20] = spec.I_TOMATO
    t_yield = z.copy()
    t_yield[:20] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = 95
    view = P.DayView(
        day=np.int32(3), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32))
    plan = P.build_day(np, view, _macro(hold=np.full(9, 10_000, np.int32)), TABLE)
    op, qty, floor = plan[3], plan[5], plan[6]
    forced = [(t, s) for t in O.SELL_TURNS for s in range(spec.N_PRODUCTS) if int(qty[t, s]) > 0]
    assert sum(int(qty[t, s]) for t, s in forced) == 15
    assert all(int(floor[t, s]) == S.LIQUIDATE for t, s in forced)
    assert all(int(op[t, s]) == O.MO_SELL for t, s in forced)


def test_runtime_caps_the_later_lots_from_the_live_market():
    # a plan that sells 20 wool in lot 2 with floor 190; the live market at
    # turn 10 has absorbed 40 wool, so the cap bites
    z = np.zeros(100, np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = 20
    view = P.DayView(
        day=np.int32(3), kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32))
    hold = np.full(9, 10_000, np.int32)
    hold[spec.I_WOOL] = 190
    rt = runtime.Runtime(lambda obs, player, v: _macro(hold=hold))
    rt.plan = P.build_day(np, view, _macro(hold=hold), TABLE)
    rt.day = 3
    # move the whole wool lot into lot 2 by hand so the guard has something to cap
    mq = np.array(rt.plan[5]); mq[O.SELL_TURNS[0], spec.I_WOOL], mq[O.SELL_TURNS[1], spec.I_WOOL] = 0, 20
    rt.plan = rt.plan[:5] + (mq,) + rt.plan[6:]
    inv = {n: spec.MARKET_I0 for n in spec.PRODUCTS}
    inv["WOOL"] = spec.MARKET_I0 + 40
    obs = {"player": 0, "day": 3, "hour": O.SELL_TURNS[1],
           "farms": [{"tiles": [[None] * 10 for _ in range(10)], "money": 0, "unlocked_quadrants": ["NW"], "hands": []}],
           "private": {"shed": {"WOOL": 20}, "seeds": {}},
           "market": {"prices": {n: 1 for n in spec.PRODUCTS}, "inventory": inv},
           "town": {"unlocked_shops": []}}
    act = rt.act(obs)
    wool = [m for m in act["market"] if m[1] == "WOOL"]
    quotes = PJ.sell_quotes(np, TABLE, np.array([inv[n] for n in spec.PRODUCTS], np.int32))[spec.I_WOOL]
    assert wool == [["SELL", "WOOL", int((quotes[:20] >= 190).sum())]]


def test_cap_row_agrees_across_backends():
    import jax.numpy as jnp
    op, arg, q, f = _row(spec.I_WOOL, 20, 190)
    a = guard.cap_row(np, TABLE, I0, op, arg, q, f)
    b = guard.cap_row(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(op), jnp.asarray(arg),
                      jnp.asarray(q), jnp.asarray(f))
    assert a.tolist() == np.asarray(b).tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_walk_and_cap.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.core.guard'`.

- [ ] **Step 3: The guard**

Create `src/kagg3/core/guard.py`:

```python
"""The turn-time lot guard [PLANNER_V3_1 section 3]: at a later SELL turn the
executor walks the *live* quote curve and caps each lot at the largest
quantity whose every unit still clears the lot's planned adjusted floor. A
lot capped to zero stays in its slot as an inert `SELL item 0` so the two
seats' orders keep their pairing (the engine pairs by list index).

Both executors call this with the inventory the agent observes at that turn
-- the state after the previous turn's town tick -- so they cap identically.
"""

from __future__ import annotations

from .. import spec
from . import ops as O
from . import projector as PJ


def cap_row(xp, price_table, mkt_inv, op_row, arg_row, qty_row, floor_row):
    """int[MO]: `qty_row` with every SELL slot capped at the count of its
    first `qty` units whose live quote is >= its floor."""
    i32 = xp.int32
    quotes = PJ.sell_quotes(xp, price_table, mkt_inv)                  # [9, K]
    item = xp.clip(arg_row, 0, spec.N_PRODUCTS - 1)
    q_rows = quotes[item]                                              # [MO, K]
    j = xp.arange(PJ.K, dtype=i32)[None, :]
    clears = (q_rows >= floor_row[:, None]) & (j < qty_row[:, None])
    capped = xp.sum(clears.astype(i32), axis=1)
    return xp.where(op_row == O.MO_SELL, capped, qty_row).astype(i32)
```

(Quotes are non-increasing along the walk, so "count of clearing units" is the largest prefix that clears.)

- [ ] **Step 4: Floors and placeholders in the planner**

In `plan.py`:
- `_market(xp, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, lots, n_hire, floors)` allocates a fourth array `floor = xp.zeros((TPD, MO), dtype=i32)`; in the SELL loop emit placeholders and floors:

```python
    for k, turn in enumerate(O.SELL_TURNS):
        lot = lots[k].astype(i32)
        op = _row(xp, op, turn, xp.concatenate([xp.full((spec.N_PRODUCTS,), O.MO_SELL, i32), pad]))
        arg = _row(xp, arg, turn, arg_row)
        qty = _row(xp, qty, turn, xp.concatenate([lot, pad]))
        floor = _row(xp, floor, turn, xp.concatenate([floors[k].astype(i32), pad]))
```

and return `op, arg, qty, floor`. (M2's land order writes slot 9 of the same turn-2 row after this loop — unchanged.)
- In `build_day` compute `floors = (hold[None, :] + macro.press[None, :] * xp.arange(SELL.N_LOTS, dtype=i32)[:, None]).astype(i32)` **after** the forced-overflow addition, and exempt the forced units from the cap — they bypass reservation values by construction (§0.9) and a capped forced unit is destroyed at eod: `floors = xp.where((lot_ix == forced_lot[None, :]) & (forced[None, :] > 0), SELL.LIQUIDATE, floors).astype(i32)`; pass it; the return becomes `(unit_op, unit_a, unit_q) + mkt` with `mkt` now four arrays. Update the module docstring's shape list with `mkt_floor [24, 10]  planned adjusted price floor per SELL slot`.

In `agent/render.py::market_actions` the SELL branch already renders `int(mkt_q[turn, s])`; zero quantities now reach it because the op is `MO_SELL` — no code change, but add a comment: "a zero-quantity SELL is emitted on purpose: the engine parses it as an inert order that keeps its index (section 3)".

In `agent/runtime.py::Runtime.act`, after the plan is built/looked up and before rendering:

```python
        if hour in O.SELL_TURNS[1:]:
            unit_op, unit_a, unit_q, mkt_op, mkt_a, mkt_q, mkt_floor = self.plan
            inv = parse.parse_market(obs)[0]
            capped = guard.cap_row(np, P.default_price_table(), inv, mkt_op[hour], mkt_a[hour],
                                   mkt_q[hour], mkt_floor[hour])
            mkt_q = np.array(mkt_q, copy=True)
            mkt_q[hour] = capped
            plan = (unit_op, unit_a, unit_q, mkt_op, mkt_a, mkt_q, mkt_floor)
        else:
            plan = self.plan
        return render.turn_action(plan, hour, len(farm["hands"]))
```

(import `guard` and `ops as O`; `render.turn_action` unpacks the first six entries — change its first line to `unit_op, unit_a, unit_q, mkt_op, mkt_a, mkt_q = plan[:6]`.)

In `sim/rollout.py`: `compact_orders(mop, ma, mq, mfloor)` gathers all four with the same `sel`; `run_day` stacks `b[6]` as `mfloor` and, in `turn_body`'s later-sell branch, caps per seat before resolving:

```python
                lambda s2: _market_turn(tables, s2, mop[:, h], ma[:, h],
                                        jnp.stack([guard.cap_row(jnp, tables.price, s2.mkt_inv, mop[p, h], ma[p, h],
                                                                 mq[p, h], mfloor[p, h]) for p in range(2)]),
                                        sell_only=True),
```

(`from ..core import guard`). The cap reads `s2.mkt_inv` — the inventory at the start of the turn, before this turn's market — which is what the agent observed.

- [ ] **Step 5: Update the tuple consumers and add the two-theta equivalence game**

`tests/test_day29_endgame.py`: replace the six-way unpack with `plan = P.build_day(...)` and index it. In `tests/test_sim_equivalence.py` add:

```python
@pytest.mark.parametrize("seed", [20260821, 4242])
def test_sim_matches_engine_with_a_dumper_and_a_holder(seed):
    """Seat 1 dumps at zero reservation, seat 0 holds with timing pressure:
    the later lots of seat 0 are capped by the live market on both sides."""
    from kagg3.es import archetypes as A
    t0 = A.archetype_theta(hold=2.0, press=1.0, dev=3.0)
    t1 = A.archetype_theta(hold=-8.0, dev=3.0)
    tables = build_tables(jnp)
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([agent_for(t0), agent_for(t1)])
    hi_t, lo_t = eod.weed_threshold()
    hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
    thetas = jnp.stack([jnp.asarray(t0), jnp.asarray(t1)])
    run_day = jax.jit(functools.partial(rollout.run_day, tables))
    run_last = jax.jit(functools.partial(rollout.run_day, tables, n_turns=spec.TURNS_PER_DAY - 1, do_eod=False))
    st = initial_state(jnp)
    for d in range(spec.N_DAYS):
        f = run_last if d == spec.N_DAYS - 1 else run_day
        st = f(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)), hi_t, lo_t, thetas)
        e, s = _engine(env, min((d + 1) * 24, len(env.steps) - 1)), _sim(st)
        for k in s:
            assert np.array_equal(np.asarray(e[k]), np.asarray(s[k])), f"day {d}: field {k} diverged"
```

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_walk_and_cap.py -q` — Expected: PASS (7 tests).
Run: `python -m pytest -q` — Expected: all pass; the equivalence games (old and new) are the gate — the sim's cap and the runtime's cap must agree on every capped lot.
Run: `python scripts/package_submission.py && tar tzf dist/submission.tar.gz | grep guard && python -m pytest tests/test_submission_runs.py -q` — Expected: `kagg3/core/guard.py` listed and PASS (`guard.py` imports only `spec`, `ops`, `projector`; `test_archive_is_self_contained` is the only test that would catch a missing module).
Run: `python scripts/bench_sim.py` here and on the Task-6 commit; record both (two `cap_row` gathers per later-sell turn).
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add src/kagg3/core/guard.py src/kagg3/core/plan.py src/kagg3/agent/render.py src/kagg3/agent/runtime.py src/kagg3/sim/rollout.py scripts/package_submission.py tests/test_walk_and_cap.py tests/test_sim_equivalence.py tests/test_day29_endgame.py
git commit -m "Cap the later lots against the live market on both executors; keep zeroed lots as placeholders"
```

---

### Task 8: Per-parameter sigma — a separable-NES trial in the trainer (§8 "complement, not substitute")

**Files:**
- Modify: `src/kagg3/es/train.py` (`Config`, `Trainer.__init__`, `generation`), `scripts/train.py` (`--adapt-sigma`, checkpoint the sigma vector)
- Test: `tests/test_sigma_adapt.py`

**Interfaces:**
- Produces: `Config.adapt_sigma: bool = False`, `Config.sigma_lr: float = 0.0` (0 → the SNES default `(3 + ln n) / (5 √n)`), `Config.sigma_bounds: tuple = (0.2, 5.0)` (multipliers of `Config.sigma`); `Trainer.sigma` (float32[N_PARAMS], `cfg.sigma` on live coordinates, 0 on masked ones); `generation` perturbs with the vector and, when adapting, updates `log sigma` after the theta step; `scripts/train.py` saves/loads `sigma` in `state.npz`.

**Background.** `kagg3-es-converged` measured theta random-walking orthogonally at equal strength with small single-gene gains ES cannot resolve; §8 lists a per-parameter sigma trial "SNES/sep-CMA class — complement, not substitute". Separable NES keeps the isotropic estimator for the mean and adds one scalar step size per coordinate: with utilities `u_k` (the same rank-normalised advantages) and standard-normal draws `ε_k`, `∇_log σ = Σ_k u_k (ε_k² − 1)`; antithetic pairs share `ε²`, so the pair's utilities add. Step `log σ += η_σ/2 · ∇`, clipped to `[0.2, 5] × σ₀`. With `adapt_sigma=False` a generation is bit-identical to today's (the vector is the scalar broadcast). The trial is an A/B run under the Phase-2 protocol; nothing is promoted on this task.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sigma_adapt.py`:

```python
"""Separable-NES step sizes (PLANNER_V3_1 section 8, Phase 3): one sigma per
live coordinate, isotropic mean update unchanged, sigma updated from the
pairs' utilities after the theta step. Off, a generation is bit-identical.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import jax.numpy as jnp
import numpy as np

from kagg3.core import policy as PO
from kagg3.es.train import Config, Trainer

SMALL = dict(pop=4, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0)


def test_sigma_vector_starts_at_the_scalar_on_live_coordinates():
    tr = Trainer(Config(**SMALL, sigma=0.03), seed=0)
    s = np.asarray(tr.sigma)
    live = PO.live_mask() > 0
    assert np.all(s[live] == np.float32(0.03)) and np.all(s[~live] == 0)


def test_adaptation_off_is_bit_identical_to_the_scalar_trainer():
    a = Trainer(Config(**SMALL), seed=3)
    b = Trainer(Config(**SMALL, adapt_sigma=True), seed=3)
    a.generation()
    b.generation()
    assert np.array_equal(np.asarray(a.theta), np.asarray(b.theta))     # sigma moves after the theta step
    assert not np.array_equal(np.asarray(b.sigma), np.asarray(a.sigma))


def test_the_vector_path_reproduces_the_scalar_trainer_pinned_theta():
    # tests/data/sigma_scalar_gen1.npy is written once from the pre-Task-8
    # commit (Step 3a) -- the true "bit-identical to today" check; the test
    # above only compares the new code path against itself
    import pathlib
    ref = pathlib.Path("tests/data/sigma_scalar_gen1.npy")
    tr = Trainer(Config(**SMALL), seed=3)
    tr.generation()
    assert np.array_equal(np.asarray(tr.theta), np.load(ref))


def test_sigma_stays_within_bounds_and_dead_coordinates_stay_zero():
    tr = Trainer(Config(**SMALL, adapt_sigma=True, sigma=0.02, sigma_lr=5.0), seed=1)
    for _ in range(3):
        tr.generation()
    s = np.asarray(tr.sigma)
    live = PO.live_mask() > 0
    assert np.all(s[live] >= np.float32(0.2 * 0.02) - 1e-7) and np.all(s[live] <= np.float32(5.0 * 0.02) + 1e-7)
    assert np.all(s[~live] == 0)


def test_default_sigma_lr_is_the_snes_rate():
    tr = Trainer(Config(**SMALL, adapt_sigma=True), seed=0)
    n = int((PO.live_mask() > 0).sum())
    assert abs(tr.sigma_lr - (3.0 + np.log(n)) / (5.0 * np.sqrt(n))) < 1e-9
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_sigma_adapt.py -q`
Expected: FAIL — `AttributeError: 'Trainer' object has no attribute 'sigma'`.

- [ ] **Step 3a: Pin the scalar trainer's output before touching it**

On the current (pre-Task-8) commit run `python - <<'EOF'` with `Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, warm_frac=0.0), seed=3)`, one `generation()`, and `np.save("tests/data/sigma_scalar_gen1.npy", np.asarray(tr.theta))`. This is the reference the last test compares against; without it "bit-identical to today" is asserted, not tested.

- [ ] **Step 3: The sigma vector**

In `src/kagg3/es/train.py::Config` add:

```python
    adapt_sigma: bool = False   # separable-NES step sizes, one per live coordinate
    sigma_lr: float = 0.0       # 0 -> (3 + ln n_live) / (5 sqrt(n_live))
    sigma_bounds: tuple = (0.2, 5.0)   # multipliers of `sigma`
```

In `Trainer.__init__`, after `self.mask = ...`:

```python
        self.sigma = jnp.full(self.n, cfg.sigma, jnp.float32) * self.mask
        n_live = float(jnp.sum(self.mask))
        self.sigma_lr = cfg.sigma_lr if cfg.sigma_lr > 0 else (3.0 + np.log(n_live)) / (5.0 * np.sqrt(n_live))
```

In `generation` replace the perturbation and gradient lines with:

```python
        eps = perturbations(k, half, self.n) * self.mask
        thetas = jnp.concatenate([self.theta + self.sigma * eps,
                                  self.theta - self.sigma * eps])
        ...
        grad = jnp.where(self.mask > 0,
                         ((adv[:half] - adv[half:]) @ eps) / (cfg.pop * jnp.maximum(self.sigma, 1e-12)),
                         0.0)
```

and after `self.theta = jnp.where(self.mask > 0, (1.0 - cfg.weight_decay) * step, self.theta)` add:

```python
        if cfg.adapt_sigma:
            # Separable NES: antithetic pairs share eps^2, so their utilities add.
            u = adv[:half] + adv[half:]
            g_sigma = (u @ (eps ** 2 - 1.0)) / half
            lo, hi = cfg.sigma_bounds
            new = self.sigma * jnp.exp(0.5 * self.sigma_lr * g_sigma)
            self.sigma = jnp.where(self.mask > 0, jnp.clip(new, lo * cfg.sigma, hi * cfg.sigma), 0.0)
```

In `scripts/train.py`: add `ap.add_argument("--adapt-sigma", action="store_true", help="separable-NES step sizes (Phase 3 trial)")`, pass `adapt_sigma=args.adapt_sigma` into `Config`, save `sigma=np.asarray(tr.sigma)` in `save_state`, and in `load_resume` restore `tr.sigma = jnp.asarray(d["sigma"])` when the key exists.

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_sigma_adapt.py -q` — Expected: PASS (each test compiles one small episode on CPU).
Run: `python -m pytest -q` — Expected: all pass (`test_es_masking.py`'s generation test still leaves dead coordinates untouched — their sigma is zero).
Run: `ruff check src tests scripts`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/es/train.py scripts/train.py tests/test_sigma_adapt.py tests/data/sigma_scalar_gen1.npy
git commit -m "Add separable-NES per-parameter step sizes as an opt-in trainer trial"
```

---

### Task 9: Operational metrics and the Phase-3 measurement (§7)

**Files:**
- Create: `scripts/day_metrics.py`
- Produces: a "Phase-3 result" section appended to this plan; no promotion decision here beyond the frozen-theta ablation (the sigma trial's promotion follows the Phase-2 protocol).

**Interfaces:**
- Consumes: `artifacts/theta.npy` (the Phase-2 lineage's promoted theta), `scripts/eval_vs_baselines.py --csv --seed-base --opponents`, `scripts/paired_ci.py`, `artifacts/opponents/phase1/main.py` (frozen in Phase 2), `scripts/train.py --adapt-sigma --trunk-from`.

**Predictions, stated before the runs (§7).**

| Tasks | Item | Predicted sign on frozen Phase-2 theta | Why |
|---|---|---|---|
| 1–3 | DROP + horizon | ≥ 0, largest of the phase | day-29 harvests and eod-28 production sell; day-28 survival work resumes |
| 4 | M1 prospective land | ≥ 0 | 22 turns per purchase return to development |
| 5 | M2 land at turn 2 | ≥ 0 | quadrants bought a day earlier when the morning sale covers the gap; one idle turn per unit on land days is the only cost |
| 6 | M3 DIG conversion | ≥ 0, small | rare boards |
| 7 | §3 walk-and-cap | ≥ 0 vs a dumping opponent, ≈ 0 vs `starter` | only bites when prices move between hour 0 and turn 10/18 |
| 8 | sigma trial | unknown — an A/B training run, not an ablation | complement to the isotropic estimator |

- [ ] **Step 1: Operational metrics from an engine replay**

Create `scripts/day_metrics.py`:

```python
"""Operational metrics (PLANNER_V3_1 section 7) from one engine game of the
packaged numpy agent against a built-in opponent: per day, walking turns,
idle (PASS) turns, DROPs, units the shed refused (destroyed inventory), and
the unsold terminal inventory. Usage:

    python scripts/day_metrics.py --theta artifacts/theta.npy --seed 20260825 --opponent starter
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from kaggle_environments import make

from kagg3 import spec
from kagg3.agent import parse, runtime
from kagg3.core import brain

MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def _macro_fn(theta):
    def macro(obs, player, view):
        opp = obs["farms"][1 - player]
        vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
        po = brain.PolicyObs(
            day=np.int32(view.day), money=view.money, opp_money=np.int32(opp["money"]),
            kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
            t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
            nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
            mkt_inv=parse.parse_market(obs)[0], price=view.price, shops=parse.parse_town(obs))
        return brain.decide(np, theta, po)
    return macro


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default="artifacts/theta.npy")
    ap.add_argument("--seed", type=int, default=20260825)
    ap.add_argument("--opponent", default="starter")
    args = ap.parse_args()
    theta = np.load(args.theta).astype(np.float32)
    env = make("kaggriculture", configuration={"seed": args.seed})
    env.run([runtime.make_agent(_macro_fn(theta)), args.opponent])

    per_day = {}
    prev_inv, prev_shed = 0, 0
    for i, step in enumerate(env.steps[1:], start=1):
        act = env.steps[i - 1][0].action if isinstance(env.steps[i - 1][0].action, dict) else {}
        day = (i - 1) // spec.TURNS_PER_DAY
        rec = per_day.setdefault(day, {"walk": 0, "idle": 0, "drop": 0, "destroyed": 0})
        units = [act.get("farmer", ["PASS"])] + list(act.get("hands", []))
        for u in units:
            if u and u[0] in MOVES:
                rec["walk"] += 1
            elif not u or u[0] == "PASS":
                rec["idle"] += 1
            elif u[0] == "DROP":
                rec["drop"] += 1
        priv = step[0].observation["private"]
        held = sum(sum(inv.values()) for inv in priv.get("inventories", []))
        shed = sum(priv.get("shed", {}).values())
        # inventory that vanished without reaching the shed (DROP/eod overflow)
        if held < prev_inv and shed + held < prev_shed + prev_inv:
            rec["destroyed"] += (prev_shed + prev_inv) - (shed + held)
        prev_inv, prev_shed = held, shed
    final = env.steps[-1][0].observation
    unsold = sum(final["private"]["shed"].values()) if "private" in final else None
    for d in sorted(per_day):
        r = per_day[d]
        print(f"day {d:2d}  walk {r['walk']:3d}  idle {r['idle']:3d}  drop {r['drop']:2d}  destroyed {r['destroyed']:3d}")
    print(f"final money {final['farms'][0]['money']:.0f}   unsold terminal inventory {unsold}")
```

(Sales also lower the shed without destroying anything; the heuristic above only counts a drop in `shed + held` that coincides with a drop in `held`, i.e. an inventory that did not arrive. Market sales happen while `held` is unchanged, so they are excluded — except on turn 10, a legal DROP turn: a DROP and lot 2 in the same step over-count by the lot. Report `destroyed` as an upper bound and cross-check it against the sim's exact count if the two disagree materially.)

Run: `python scripts/day_metrics.py --theta artifacts/theta.npy` — Expected: 30 day lines and a final line. Commit: `git add scripts/day_metrics.py && git commit -m "Add a per-day operational-metrics replay"`.

- [ ] **Step 2: Frozen-theta ablation, per module**

The Phase-2 promoted theta is the frozen subject. Baseline: the Phase-2 final commit. Then each of the Task 3, 4, 5, 6 and 7 commits (Tasks 1–2 alone change no plan the engine sees differently until Task 3). For each commit `C`:

```bash
git worktree add /tmp/claude-0/kagg3-$C $C
cd /tmp/claude-0/kagg3-$C
python scripts/eval_vs_baselines.py --theta /mnt/e/_work/kaggriculture3/artifacts/theta.npy --games 32 --seed-base 20260826 \
    --opponents starter random /mnt/e/_work/kaggriculture3/artifacts/opponents/phase1/main.py --csv /mnt/e/_work/kaggriculture3/artifacts/phase3_$C.csv
git worktree remove /tmp/claude-0/kagg3-$C
```

then `python scripts/paired_ci.py artifacts/phase3_<task>.csv artifacts/phase3_<previous>.csv --opponent starter` between consecutive commits, and against the `phase1/main.py` opponent for Task 7 (the dumping incumbent is where the cap bites). Record every line.

- [ ] **Step 3: The sigma trial**

Two runs at the Phase-2 budget, same seed, trunk warm-started from the same theta:

```bash
nohup python scripts/train.py --run p3sig --seed 0 --gens $GENS --pop 128 --episodes 64 --chunk 8192 \
    --trunk-from artifacts/theta.npy --adapt-sigma > artifacts/p3sig.log 2>&1 &
nohup python scripts/train.py --run p3iso --seed 0 --gens $GENS --pop 128 --episodes 64 --chunk 8192 \
    --trunk-from artifacts/theta.npy > artifacts/p3iso.log 2>&1 &
```

(`GENS` as computed in Phase 2 Task 9; `--chunk 8192` = pop × episodes, the zero-padding ceiling — the script's default 256 pads every device call.) Multi-hour; evaluate both `theta.npy` files with the Phase-2 held-out protocol (`--seed-base 20260825 --games 32`, paired CI vs `starter` and head-to-head win rate against the incumbent). Promote only under the Phase-2 rule (CI excluding 0 on the positive side **and** > 50% head-to-head against the current shipped theta).

- [ ] **Step 4: Record and commit**

Append `## Phase-3 result` to this plan: the per-module paired CIs with each prediction marked *held* / *did not hold*, the `day_metrics.py` lines for the baseline and the final commit (walking turns, idle turns, drops, destroyed units, unsold terminal inventory — the last must be near zero after Task 3), the sigma trial's CIs and the promotion decision.

```bash
git add docs/superpowers/plans/2026-08-24-planner-v31-phase3.md
git commit -m "Record the Phase-3 measurement"
```

---

## Self-review notes (written with the plan)

- **Review corrections folded in (2026-08-24):** capacity room discounts lot 2 (early DROPs); day-29 same-day WATER/FERTILIZE chains kept per §0.4; `core/guard.py` added to the archive `INCLUDE`; final-day `hold` is `SELL.LIQUIDATE`, not 0; forced-overflow units exempt from the cap; `a_want` re-sized on prospective tiles; collections counted in the room check; M2 revenue margin; `--chunk 8192`; a pinned scalar-trainer reference for the sigma trial.
- **Spec coverage, Phase 3 (§8):** §4 DROP → Tasks 1 (sim, exact; PLACE fallthrough; equivalence suite + PLACE pin per §6.4), 2 (terminal rules re-derived through the horizon parameter), 3 (return leg, capacity law, lot 3); M1 → Task 4; M2 → Task 5 (turn-2 slot 9, no sim change, the "more of the buy row" extension explicitly out of scope per §6.1); M3 → Task 6; §3 walk-and-cap → Task 7 (renderer placeholder, sim-side guard in the sell-only path, dedicated equivalence game, the ten-order cap noted); per-parameter sigma → Task 8; §7 operational metrics and measurement → Task 9. §5's "Open" list (spatial placement near the shed, multi-kind animal days, harvest batching, cash reservation across days, harvest-at-cap-saturation) stays open by the spec's own labelling.
- **Design decisions the spec left open, labelled in code:** the return leg is charged at a constant worst case (9) to keep the block cost monotone; the capacity law limits admitted harvest and collection units to the room the final day's shed has *before lot 2 sells* (capacity − animal items − lot 2), because the first DROPs land from turn 3; `DROP_DEADLINE_TURN` is held one turn before lot 3 as a margin although same-turn DROP→SELL is verified; M2's funding uses a *provisional* allocation with maximal reservations and counts only 3/4 of the projected lot-1 revenue (the opponent's lockstep sales are the residual), and every unit idles one turn on a land day; M3 ranks true free tiles ahead of reclaimable structures rather than valuing the extra DIG turn explicitly; the cap floor is `hold + press × lot` (the externality term of the allocator is not part of the executed floor), with forced-overflow slots floored at `LIQUIDATE` so the cap never pushes an overflow unit back into the shed; day-29 WATER/FERTILIZE survive only inside a same-day harvest chain, per §0.4 re-derived through §4.
- **Type consistency:** `build_day` returns seven arrays from Task 7 on (every consumer listed); `_routes` gains `final=False` in Task 3; `_market` gains `floors` in Task 7 and moves land to turn 2 in Task 5; `sell.allocate` gains `open_lots` in Task 2 and Task 5 passes it; `Prefix` gains `final` (Task 2), `t_units`, `t_coll` and `product` (Task 3); the hour-0 `lots` is computed above the admission from Task 3 on; `plan.LAND_REV_NUM/LAND_REV_DEN` from Task 5; `ops.LAST_HARVEST_DAY`/`DROP_DEADLINE_TURN`/`RETURN_TURNS` from Task 2; `guard.cap_row` signature is identical on both executors; `Trainer.sigma` is a vector from Task 8 on and masked coordinates stay zero.
