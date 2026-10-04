# Planner V3.1 — Phase 0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Dispatch each task to a fresh **Opus** subagent (`model: "opus"`); the implementer sees only its own task plus the header, so every task repeats what it needs.

**Goal:** Land every Phase-0 item of `docs/PLANNER_V3_1.md` §8 — the pure [LAW] planner changes that are sign-safe under the frozen theta and touch no gene — and measure the frozen-theta effect at the end.

**Architecture:** Everything lives in the shared planner (`src/kagg3/core/plan.py`, `brain.py`, `ops.py`) plus one new array-agnostic module `src/kagg3/core/projector.py`. Both executors — the JAX simulator (`sim/rollout.py`) and the numpy submission (`agent/runtime.py`) — run that code verbatim, so the sim changes only to plumb two more fields into `DayView` and hand the planner its price table. Every new rule is shape-static int32 arithmetic under `xp`, with pairwise tie-breaking, exactly like the code around it.

**Tech Stack:** Python 3, numpy, JAX (CPU for tests), pytest, ruff.

**Spec:** `docs/PLANNER_V3_1.md` — Phase 0 is §8's first bullet: §1.1 price projector, §0.1 deadline-clamped harvest (with its plant-gate consistency), §0.5 lexicographic tiers (all survival feeds mandatory until §1.4), §0.7 fertilizer reservation, §0.9 overflow forced sale, the day-29 endgame from §0.4, and the stale-comment fix §6.2. Audit record: `docs/PLANNER_V3_1_REVIEW.md`. Read both before starting a task; the plan argues from the spec.

**Out of scope (later plans):** Phase 1 (§0.2, 0.4 day-28 rules, 0.6, 0.8, 0.10, 0.11, 0.12), Phase 2 (§1.2–1.6 optimizers + genome re-type, fresh lineage), Phase 3 (§3 walk-and-cap, §4 DROP, M1–M3). The spec gates each on the previous phase's measurements (§7, §8), so they are planned after Task 8's numbers are in.

## Global Constraints

Every task's requirements implicitly include this section.

- Planner code is array-agnostic: written against `xp` (numpy or `jax.numpy`), shape-static, no data-dependent Python control flow, no `searchsorted`/sorting inside `build_day` (use `_count_le` and pairwise compares — the file explains why in `task_order` and `_count_le`).
- Integer everywhere a decision is made; ties broken pairwise/lexicographically, ties to the lower index. **Never pack a tier into the int32 sort key** — `plan.py`'s packed key already fills ±1.15e9 (§0.5).
- Market orders only on turns 0, 1, 2, 10, 18: the sim resolves the market on hours 0–2 (full path) and 10/18 (sell-only) and silently drops orders elsewhere (§6.1). No new SELL turns (each costs ~6% of throughput).
- Both seats keep an identical market slot layout (`sim/market.py::assert_no_cross`).
- Theta layout, `Macro` fields, and `brain.decide` output semantics are **untouched** in Phase 0; `artifacts/theta.npy` must still load and replay. Genome changes are Phase 2.
- Cross-unit same-tile same-turn disjointness (§6.3) must keep holding; the router is not changed in this plan.
- `kagg3/__init__.py`'s precision pin is untouched.
- The number 28 appears in code only as `ops.LAST_SHED_DAY` (introduced in Task 1); every terminal rule derives from it (§0.4 "generalized horizon predicate").
- Tests: each file starts with `os.environ.setdefault("JAX_PLATFORMS", "cpu")` and `sys.path.insert(0, "src")` like the existing ones; fixtures follow `tests/test_budget_order.py`'s `_view`/`_macro` pattern; run from the repo root with `python -m pytest tests/<file>.py -q`; full suite `python -m pytest -q` (includes the sim-vs-engine equivalence gates `test_sim_equivalence.py`, `test_trained_equivalence.py`, `test_backend_agreement.py`, and `test_submission_runs.py`).
- Fixture gotcha (from `brain.n_free_slots`): a one-time crop past its harvest age counts as a *free* slot, so filler tiles meant to stay occupied must hold an **ongoing** crop (`spec.I_TOMATO` or `spec.I_STRAWBERRY`).
- Interpreter: every `python` in this plan means the repo's `.venv/bin/python` (or a shell with that venv activated) — the system `python` has neither JAX nor `kaggle_environments`, so the full suite and the engine evals cannot run under it.
- Lint: `ruff check src tests` clean before every commit.
- Commit per task on the current branch `fitness-shaping`; one-line sentence-case imperative messages like the repo's (`git log --oneline -5`). Never commit `artifacts/`.

## File map

| File | Responsibility after Phase 0 |
|---|---|
| `src/kagg3/core/ops.py` | op codes, schedule constants, **`LAST_SHED_DAY` horizon** (Task 1) |
| `src/kagg3/core/plan.py` | `DayView` (+`mkt_inv`, `shops`), `build_day(..., price_table)`, deadline harvest, two-tier `task_order`, hoisted sale block with reservations, terminal day, forced overflow sale |
| `src/kagg3/core/brain.py` | `n_free_slots` and the plant gate read the same horizon and clamp as the planner |
| `src/kagg3/core/projector.py` | **new** — opponent-free price projection: town ticks, projected inventory, sell quote curves, marginal quotes |
| `scripts/package_submission.py` | its explicit `INCLUDE` list gains `core/projector.py` (Task 4) — the archive is built from that list, not from the package tree |
| `src/kagg3/sim/rollout.py` | `day_view` carries `mkt_inv`/`shops`; `run_day` passes `tables.price` |
| `src/kagg3/agent/parse.py` | `parse_view` fills `mkt_inv`/`shops` from the observation |
| `tests/test_deadline_harvest.py`, `test_mandatory_tier.py`, `test_dayview_market.py`, `test_projector.py`, `test_day29_endgame.py`, `test_fert_reserved.py`, `test_overflow_forced_sale.py` | one test file per task |

Task order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Tasks 5–7 depend on 3 (and 7 on 4); Tasks 1–2 are independent of the rest but land first because later tasks use `LAST_SHED_DAY` and the tier.

---

### Task 1: Horizon constant, stale schedule comment, and the deadline-clamped harvest (§0.1, §6.2)

**Files:**
- Modify: `src/kagg3/core/ops.py:72-79` (schedule comment) and append the constant after `MAX_PICKUPS`
- Modify: `src/kagg3/core/plan.py:277-280` (`harvest_one`)
- Modify: `src/kagg3/core/brain.py:97-101` (`n_free_slots`) and `brain.py:289` (`can_mature`)
- Test: `tests/test_deadline_harvest.py`

**Interfaces:**
- Produces: `ops.LAST_SHED_DAY: int = 28`. Inside `build_day`: `harvest_age` (int[100]) and `harvest_one` (bool[100]) with the new semantics; later tasks read `harvest_one` unchanged.

**Background.** Verified (spec §0.1): the engine's HARVEST checks only `age >= first_yield_day` and `yield > 0`; `max_yield_day` is never checked; one-time crops are born with `yield_units = 1`; in-window waterings add +1/+2 before the same-day harvest. Today `plan.py:280` harvests one-time crops only at `age >= max_yield_day`, so a wheat planted on day 25 (max yield day 4 → day 29) decays unsold, though harvesting it on day 28 at age 3 sells 3 units. The rule:

    harvest_age*(c, t_day) = clip(LAST_SHED_DAY − t_day, CROP_FIRST_YIELD_DAY[c], CROP_MAX_YIELD_DAY[c])
    harvest_one: age >= harvest_age*

`t_day` is the **planting day**, so `harvest_age*` is the age the crop has on day 28, clamped into its yield window. Whenever `28 − t_day >= max_yield_day` this is exactly today's behaviour. The plant gate in `brain.py` (`day + CROP_FIRST_YIELD_DAY <= 28`) **stays** and now reads the same constant.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_deadline_harvest.py`:

```python
"""One-time crops harvest at max_yield_day -- or on the last shed day when the
season ends first (PLANNER_V3_1 section 0.1). HARVEST needs only
age >= first_yield_day and yield > 0, so a deadline harvest is legal, and
selling k >= 1 units strictly dominates the 0 an unsold crop is worth once
day 29 has no end-of-day to bank it.
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

WHEAT, MELON = spec.I_WHEAT, spec.I_MELON
_MOVES = (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _view(day, crop, planted_day, t_yield=1):
    """One one-time crop on serpentine position 0, everything else empty."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[0] = spec.KIND_PLANT
    occ = z - 1
    occ[0] = crop
    t_day = z.copy()
    t_day[0] = planted_day
    ty = z.copy()
    ty[0] = t_yield
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day,
        t_water=z.copy(), t_cons=z.copy(), t_yield=ty,
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _tile_ops(view):
    """The farmer's non-movement ops, in order. Only one tile has work."""
    unit_op = P.build_day(np, view, _macro())[0]
    return [int(o) for o in unit_op[0] if int(o) not in _MOVES]


def test_horizon_constant_is_the_last_shed_day():
    assert O.LAST_SHED_DAY == 28


def test_wheat_planted_day_25_harvests_on_day_28():
    # age 3 < max_yield_day 4, but 28 - 25 = 3 is all the calendar leaves:
    # the in-window watering still fires first, then the deadline harvest.
    assert _tile_ops(_view(day=28, crop=WHEAT, planted_day=25)) == [O.OP_WATER, O.OP_HARVEST]


def test_wheat_planted_day_25_still_waits_on_day_27():
    # age 2: the clamp age is 3, so no premature harvest -- day 28's watering
    # is worth one more unit.
    ops = _tile_ops(_view(day=27, crop=WHEAT, planted_day=25))
    assert O.OP_HARVEST not in ops
    assert O.OP_WATER in ops


def test_melon_planted_day_17_harvests_on_day_28_at_age_11():
    assert _tile_ops(_view(day=28, crop=MELON, planted_day=17, t_yield=6)) == [O.OP_WATER, O.OP_HARVEST]
    assert O.OP_HARVEST not in _tile_ops(_view(day=27, crop=MELON, planted_day=17))


def test_early_season_harvest_day_is_unchanged():
    # planted day 0: max_yield_day 4 is reachable, so the harvest waits for it
    assert O.OP_HARVEST not in _tile_ops(_view(day=3, crop=WHEAT, planted_day=0))
    assert O.OP_HARVEST in _tile_ops(_view(day=4, crop=WHEAT, planted_day=0))


def _obs(view):
    return brain.PolicyObs(
        day=view.day, money=np.int32(0), opp_money=np.int32(0),
        kind=view.kind, occ=view.occ, opp_kind=view.kind, opp_occ=view.occ,
        t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=view.price, shops=np.zeros(spec.N_SHOPS, np.int32))


def test_brain_free_slots_count_the_deadline_tile():
    # brain.n_free_slots and the planner must agree on when the tile frees.
    assert int(brain.n_free_slots(np, _obs(_view(day=28, crop=WHEAT, planted_day=25)))) == 100
    assert int(brain.n_free_slots(np, _obs(_view(day=27, crop=WHEAT, planted_day=25)))) == 99


def test_plant_gate_reads_the_horizon():
    # day + first_yield_day <= LAST_SHED_DAY is the gate: wheat (2) plants on
    # day 26, not 27. Decoded through brain.decide with a zero theta so the
    # crop split is uniform.
    from kagg3.core import policy as PO
    theta = np.zeros(PO.N_PARAMS, np.float32)
    free = _view(day=26, crop=WHEAT, planted_day=0)
    free = free._replace(kind=np.full(100, spec.KIND_EMPTY, np.int32),
                         occ=np.full(100, -1, np.int32), money=np.int32(3000))
    m26 = brain.decide(np, theta, _obs(free)._replace(money=np.int32(3000)))
    m27 = brain.decide(np, theta, _obs(free._replace(day=np.int32(27)))._replace(money=np.int32(3000)))
    assert int(m26.plant_target[WHEAT]) > 0
    assert int(m27.plant_target[WHEAT]) == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_deadline_harvest.py -q`
Expected: FAIL — `AttributeError: module 'kagg3.core.ops' has no attribute 'LAST_SHED_DAY'` on the constant test, and `[O.OP_WATER] != [O.OP_WATER, O.OP_HARVEST]` on the wheat/melon day-28 tests.

- [ ] **Step 3: Fix the schedule comment and add the horizon constant in `ops.py`**

Replace `src/kagg3/core/ops.py:72-79` (the block starting `# --- intra-day schedule layout`) with:

```python
# --- intra-day schedule layout (see docs/DESIGN.md) -----------------------
# turn 0 : HIRE x H
# turn 1 : BUY_PRODUCT x2, BUY_SEED x5, BUY_ANIMAL x1, BUY_LAND
# turn 2 : SELL x9 (lot 1)
# turns 10, 18 : SELL x9 (lots 2, 3)
# turns 2 .. 2+P-1 : units PICKUP (P = 0..3 pickup ops needed today)
# turns 2+P .. 23  : units walk their route
```

Append after `MAX_PICKUPS = 3`:

```python

# --- horizon ---------------------------------------------------------------
# The last day whose end-of-day still banks production into the shed. Day 29
# has no end-of-day (episodeSteps 720; step 718 is the last one executed), so
# a day-29 harvest never reaches the shed and the day-29 sale draws only on
# the hour-0 stock. Every terminal rule derives from this one number -- work
# is worth planning only if its payoff lands by this day's eod -- and DROP
# (PLANNER_V3_1 section 4) is the change that would move it.
LAST_SHED_DAY = 28
```

- [ ] **Step 4: Clamp the harvest age in `plan.py`**

Replace `src/kagg3/core/plan.py:277-280`:

```python
    # One-time crops are harvested exactly at max_yield_day: the bonus window
    # closes there and decay starts the day after.
    harvest_one = is_plant & (c_ongoing == 0) & (age >= c_mxd) & (age >= c_first)
```

with:

```python
    # One-time crops are harvested at max_yield_day -- or on the last shed day
    # when the season ends first. HARVEST needs only age >= first_yield_day and
    # yield > 0, so the harvest age is the age the crop will have on
    # LAST_SHED_DAY, clamped into its yield window: a wheat planted on day 25
    # sells 3 units on day 28 instead of decaying unsold at age 4 on day 29.
    harvest_age = xp.clip(O.LAST_SHED_DAY - view.t_day, c_first, c_mxd)
    harvest_one = is_plant & (c_ongoing == 0) & (age >= harvest_age)
```

(`age >= harvest_age` implies `age >= c_first` because the clip's lower bound is `c_first`.)

- [ ] **Step 5: Make `brain.py` read the same clamp and horizon**

In `src/kagg3/core/brain.py::n_free_slots`, replace:

```python
    harvest_one = is_pl & (ong == 0) & (age >= mxd) & (age >= first)
```

with:

```python
    harvest_age = xp.clip(P.O.LAST_SHED_DAY - obs.t_day, first, mxd)
    harvest_one = is_pl & (ong == 0) & (age >= harvest_age)
```

In `brain.decide`, replace the `can_mature` line:

```python
    can_mature = (obs.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY) <= 28).astype(xp.float32)
```

with:

```python
    can_mature = (obs.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY)
                  <= P.O.LAST_SHED_DAY).astype(xp.float32)
```

and update the comment above it: "day 29 is the last playable day" → "LAST_SHED_DAY is the last day whose harvest is sold".

- [ ] **Step 6: Run the new tests and the full suite**

Run: `python -m pytest tests/test_deadline_harvest.py -q` — Expected: PASS (8 tests).
Run: `python -m pytest -q` — Expected: all pass. `test_no_late_planting.py` pins the plant gate and must still pass unchanged; `test_sim_equivalence.py`/`test_trained_equivalence.py` still pass because both backends share the planner.
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add src/kagg3/core/ops.py src/kagg3/core/plan.py src/kagg3/core/brain.py tests/test_deadline_harvest.py
git commit -m "Clamp one-time harvests to the last shed day and name the horizon"
```

---

### Task 2: Two-tier lexicographic labour ordering (§0.5)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `task_order` (~line 200), the labour-priority section of `build_day` (~line 456-465), `_routes` signature (~line 488)
- Modify: `tests/test_task_priority.py` — fixture `_thirsty_plants_then_weeds` and its three tests (they assert a learned weight can outrank survival waterings, which the tier now forbids)
- Test: `tests/test_mandatory_tier.py`

**Interfaces:**
- Consumes: `harvest_one` from Task 1; `O.LAST_SHED_DAY`.
- Produces: `task_order(xp, task, score, tier=None)` — `tier` int[100], higher first, compared *before* `score`; `_routes(xp, chain_op, chain_a, chain_q, n_ops, score, tier, pick_masks, n_units, budget)`; inside `build_day` a bool[100] `mandatory`.

**Background.** `_routes` works tiles in descending learned score and drops whatever the turn budget cannot reach. Work that is lost for good if skipped today must not depend on a learned weight: deadline harvests (a one-time crop at its clamp age, and every harvest on the last shed day), survival waterings (`must_water`), survival feeds (Phase-0 interim: *all* survival feeds, until §1.4's value test ships). Pairwise compare `(tier, key)`; the packed key cannot take one more bit (Global Constraints).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_mandatory_tier.py`:

```python
"""Labour ordering is two-tier (PLANNER_V3_1 section 0.5): work that is lost
for good if skipped today -- survival waterings, survival feeds, deadline
harvests -- outranks every learned score, and the score only orders within a
tier. Compared lexicographically, never packed into the int32 key.
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


def _board(kind, day=5, shed=None, **tiles):
    z = np.zeros(100, np.int32)
    t = dict(occ=z - 1, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
             t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy())
    t.update(tiles)
    return P.DayView(
        day=np.int32(day), kind=kind, **t,
        shed=np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed,
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _weeds_head():
    """40 weeds at the head of the sweep. One unit and ~22 route turns never
    get past them unless something promotes a tile at the tail (position 99,
    tile (0, 9), nine moves from the farmer's spawn tile (4, 4))."""
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:40] = spec.KIND_WEED
    return kind


def _weed_prio():
    prio = np.zeros(P.N_PRIO, np.int32)
    prio[P.PRIO_WEED] = 100                    # 10,000 points per weed
    return prio


def test_survival_watering_outranks_a_weed_weighted_sweep():
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_TOMATO                    # ongoing crop, no harvest yet
    t_cons = np.zeros(100, np.int32)
    t_cons[99] = 1                             # weeds tonight unless watered
    unit_op = P.build_day(np, _board(kind, occ=occ, t_cons=t_cons), _macro(prio=_weed_prio()))[0]
    assert (unit_op[0] == O.OP_WATER).sum() == 1


def test_survival_feed_outranks_the_learned_score():
    kind = _weeds_head()
    kind[99] = spec.KIND_COOP
    occ = np.full(100, -1, np.int32)
    occ[99] = 0                                # a goose
    t_cons = np.zeros(100, np.int32)
    t_cons[99] = 1                             # unfed yesterday: escapes tonight
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 1
    unit_op = P.build_day(np, _board(kind, occ=occ, t_cons=t_cons, shed=shed),
                          _macro(prio=_weed_prio()))[0]
    assert (unit_op[0] == O.OP_FEED).sum() == 1


def test_deadline_harvest_outranks_the_learned_score():
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_WHEAT
    t_day = np.zeros(100, np.int32)
    t_day[99] = 25
    t_yield = np.zeros(100, np.int32)
    t_yield[99] = 3
    unit_op = P.build_day(np, _board(kind, day=28, occ=occ, t_day=t_day, t_yield=t_yield),
                          _macro(prio=_weed_prio()))[0]
    assert (unit_op[0] == O.OP_HARVEST).sum() == 1


def test_a_plain_harvest_is_not_mandatory():
    # An ongoing crop's harvest on day 13 can wait; the weed weight still wins.
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_TOMATO
    t_yield = np.zeros(100, np.int32)
    t_yield[99] = 1
    unit_op = P.build_day(np, _board(kind, day=13, occ=occ, t_yield=t_yield),
                          _macro(prio=_weed_prio()))[0]
    assert (unit_op[0] == O.OP_HARVEST).sum() == 0


def test_tier_beats_score_in_task_order():
    task = np.zeros(100, bool)
    task[[10, 20, 30]] = True
    score = np.zeros(100, np.int32)
    score[10], score[20] = 1000, 500
    tier = np.zeros(100, np.int32)
    tier[30] = 1
    order = P.task_order(np, task, score, tier)
    assert list(order[:3]) == [30, 10, 20]
    assert sorted(order.tolist()) == list(range(100))


def test_score_still_orders_within_a_tier():
    task = np.zeros(100, bool)
    task[[10, 20]] = True
    score = np.zeros(100, np.int32)
    score[20] = 5
    tier = np.ones(100, np.int32)
    assert list(P.task_order(np, task, score, tier)[:2]) == [20, 10]


def test_no_tier_equals_zero_tier():
    # The pre-tier ordering itself is still pinned by test_task_priority.py's
    # task_order tests, which call it without a tier.
    rng = np.random.default_rng(3)
    task = rng.random(100) < 0.6
    score = rng.integers(-5, 6, size=100).astype(np.int32)
    assert P.task_order(np, task, score).tolist() == \
        P.task_order(np, task, score, np.zeros(100, np.int32)).tolist()


def test_task_order_with_tier_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(1)
    for _ in range(20):
        task = rng.random(100) < 0.6
        score = rng.integers(-5, 6, size=100).astype(np.int32)
        tier = (rng.random(100) < 0.3).astype(np.int32)
        a = P.task_order(np, task, score, tier)
        b = np.asarray(P.task_order(jnp, jnp.asarray(task), jnp.asarray(score), jnp.asarray(tier)))
        assert a.tolist() == b.tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_mandatory_tier.py -q`
Expected: FAIL — `TypeError: task_order() takes 3 positional arguments but 4 were given` on the direct tests; `0 == 1` on the three build_day tests.

- [ ] **Step 3: Add the tier to `task_order`**

Replace `task_order` in `src/kagg3/core/plan.py` with:

```python
def task_order(xp, task, score, tier=None):
    """Indices listing every `task` tile first, by descending `tier`, then
    descending `score`, exact ties by ascending index (serpentine position);
    idle tiles follow in index order.

    `tier` is the mandatory flag of 0.5: a tier-1 task outranks every tier-0
    task whatever its score, so the learned score only orders within a tier.
    Compared pairwise as (tier, key) -- the packed key already fills int32
    (see PRIO_MAX), so the tier cannot be folded into it.

    Ranked pairwise rather than sorted: both backends then agree on every tie,
    and a 100x100 compare is far cheaper to compile than a sorting network.
    """
    n = task.shape[0]
    idx = xp.arange(n, dtype=xp.int32)
    t = task.astype(xp.int32)
    if tier is None:
        tier = xp.zeros(n, xp.int32)
    tr = tier.astype(xp.int32)
    # One unique integer key per tile: score first, lower index wins a tie.
    # |score| stays well under 2^31 / 128 (see PRIO_SCALE and the feature
    # ranges), so the key cannot wrap.
    key = score.astype(xp.int32) * 128 + (127 - idx)
    ahead = ((tr[None, :] > tr[:, None])
             | ((tr[None, :] == tr[:, None]) & (key[None, :] > key[:, None]))) & task[None, :]
    rank_t = xp.sum(ahead.astype(xp.int32), axis=1)
    n_true = xp.sum(t)
    rank_f = xp.cumsum(1 - t) - (1 - t) + n_true
    dest = xp.where(task, rank_t, rank_f)
    if hasattr(idx, "at"):
        return xp.zeros(n, xp.int32).at[dest].set(idx)
    out = np.zeros(n, np.int32)
    out[np.asarray(dest)] = np.arange(n, dtype=np.int32)
    return out
```

- [ ] **Step 4: Build the mandatory tier in `build_day` and thread it through `_routes`**

In `build_day`, directly after `score = xp.sum(feat * macro.prio.astype(i32)[None, :], axis=1)`, add:

```python
    # Mandatory tier [LAW, 0.5]: whatever the learned score says, work that is
    # lost for good if skipped today goes first -- deadline harvests (a
    # one-time crop at its clamp age, every harvest on the last shed day),
    # survival waterings and survival feeds. Interim until section 1.4 ships:
    # every survival feed is mandatory, not only the ones that pay.
    mandatory = (harvest_one
                 | ((day >= O.LAST_SHED_DAY) & want_harvest)
                 | (is_plant & must_water & (view.t_water == 0))
                 | (want_feed & must_feed))
    tier = mandatory.astype(i32)
```

Change the `_routes` call to pass it:

```python
    route_op, route_a, route_q, blk = _routes(
        xp, chain_op, chain_a, chain_q, n_ops, score, tier,
        xp.stack([want_feed, want_fert, m_place]), n_units, budget)
```

Change `_routes`'s signature and its `task_order` call:

```python
def _routes(xp, chain_op, chain_a, chain_q, n_ops, score, tier, pick_masks, n_units, budget):
    """Split the task sweep across units and expand it into per-turn ops.

    Tiles are worked by descending (tier, score); whatever the turn budget
    cannot reach is left undone, so that order is what decides what gets
    dropped.
    """
    ...
    order = task_order(xp, task, score, tier)
```

- [ ] **Step 5: Update `tests/test_task_priority.py` to the tier law**

Its fixture `_thirsty_plants_then_weeds` gives 30 plants a *survival* watering and asserts a weed weight can put weeds ahead of them. Survival waterings are mandatory now, so the fixture switches to ordinary harvests (an ongoing crop with one unit banked, past its first yield day). Replace the fixture:

```python
def _ripe_plants_then_weeds():
    """30 ongoing crops with a unit ready to harvest at the head of the sweep,
    10 weeds at its tail, one unit. 22 route turns cover ~7 tiles (8 moves to
    position 0, then 2 turns per tile), so the sweep order alone decides
    whether any weed is ever dug. Harvests, not
    survival waterings: those are mandatory-tier since PLANNER_V3_1 0.5 and
    no learned weight may outrank them (see test_mandatory_tier.py)."""
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:30] = spec.KIND_PLANT
    kind[90:] = spec.KIND_WEED
    occ = np.full(100, -1, np.int32)
    occ[:30] = spec.I_TOMATO                  # ongoing crop, first yield day 8
    t_yield = np.zeros(100, np.int32)
    t_yield[:30] = 1
    return _view(kind, occ=occ, t_yield=t_yield)._replace(day=np.int32(13))
```

and in the three tests that use it (`test_zero_weights_sweep_in_serpentine_order`, `test_weed_weight_digs_weeds_before_watering`, `test_sweep_weight_can_reverse_the_serpentine`) rename the fixture call and replace `O.OP_WATER` with `O.OP_HARVEST`; rename the second test to `test_weed_weight_digs_weeds_before_harvesting` and its comment "plants wait" stays true.

- [ ] **Step 6: Run the tests and the full suite**

Run: `python -m pytest tests/test_mandatory_tier.py tests/test_task_priority.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass (`test_gates.py` checks block disjointness over random boards; the tier only permutes the order, blocks stay contiguous and disjoint).
Run: `ruff check src tests`.

- [ ] **Step 7: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_mandatory_tier.py tests/test_task_priority.py
git commit -m "Order labour by (mandatory tier, score): survival and deadline work first"
```

---

### Task 3: `DayView` carries the market; `build_day` takes the price table

**Files:**
- Modify: `src/kagg3/core/plan.py` — `DayView` (~line 146), new `default_price_table()`, `build_day` signature
- Modify: `src/kagg3/sim/rollout.py` — `day_view`, `run_day`
- Modify: `src/kagg3/agent/parse.py` — `parse_view`
- Test: `tests/test_dayview_market.py`

**Interfaces:**
- Produces: `DayView.mkt_inv` (int[9], absolute hour-0 market inventory; default `np.full(9, spec.MARKET_I0)`), `DayView.shops` (int[8], instance count per shop in `spec.SHOP_NAMES` order; default zeros); `plan.default_price_table() -> np.ndarray int32[9, PRICE_TABLE_N]` (cached); `build_day(xp, view, macro, price_table=None)` where `price_table` is `int32[9, spec.PRICE_TABLE_N]` (`tables.price` in the sim; `None` → the default table). Inside `build_day` the local `price_table` is always a real `xp` array after the prologue.

**Background.** §1.1's projector needs the hour-0 market inventory, the town's shop counts and the engine's price table. The sim has all three in `State`/`Tables` (training tables may be market-randomised — the planner must project with the *same* table the sim prices with, so `run_day` passes `tables.price`); the submission reads inventory and shops from the observation (`parse_market`, `parse_town` already exist) and uses the default table. Defaults on the new fields keep every existing fixture and caller valid.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_dayview_market.py`:

```python
"""The planner projects prices itself (PLANNER_V3_1 section 1.1), so a DayView
carries the hour-0 market inventory and the town's shops, and build_day takes
the price table the simulator prices with. Defaults keep old fixtures valid.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro, _view

from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import plan as P


def test_dayview_defaults_are_a_fresh_market():
    v = _view(3000)
    assert v.mkt_inv.tolist() == [spec.MARKET_I0] * spec.N_PRODUCTS
    assert v.shops.tolist() == [0] * spec.N_SHOPS


def test_default_price_table_is_cached_and_exact():
    t = P.default_price_table()
    assert t is P.default_price_table()
    assert t.shape == (spec.N_PRODUCTS, spec.PRICE_TABLE_N)
    assert np.array_equal(t, spec.build_price_table())


def test_build_day_default_table_matches_the_explicit_one():
    view, macro = _view(3000), _macro(plant_target=np.array([3, 0, 0, 0, 0], np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(np, view, macro, spec.build_price_table())
    for x, y in zip(a, b):
        assert np.array_equal(x, y)


def _obs():
    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    return {
        "day": 4,
        "farms": [{"tiles": tiles, "money": 1234, "unlocked_quadrants": ["NW"], "hands": []}],
        "private": {"shed": {"WHEAT": 2}, "seeds": {}},
        "market": {"prices": {n: 7 for n in spec.PRODUCTS},
                   "inventory": {n: spec.MARKET_I0 - 5 for n in spec.PRODUCTS}},
        "town": {"unlocked_shops": ["BAKERY", "BAKERY", "YARN_STORE"]},
    }


def test_parse_view_carries_market_inventory_and_shops():
    v = parse.parse_view(_obs(), 0)
    assert v.mkt_inv.tolist() == [spec.MARKET_I0 - 5] * spec.N_PRODUCTS
    assert int(v.shops[spec.SHOP_NAMES.index("BAKERY")]) == 2
    assert int(v.shops[spec.SHOP_NAMES.index("YARN_STORE")]) == 1
    assert int(v.shops.sum()) == 3


def test_sim_day_view_carries_the_state_market():
    import jax.numpy as jnp
    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of
    st = initial_state(jnp)
    st = st._replace(mkt_inv=st.mkt_inv - 3, shops=st.shops.at[0].set(2))
    tables = build_tables(jnp)
    v = rollout.day_view(st, 0, jnp.int32(0), prices_of(jnp, tables, st.mkt_inv))
    assert np.asarray(v.mkt_inv).tolist() == [spec.MARKET_I0 - 3] * spec.N_PRODUCTS
    assert int(v.shops[0]) == 2
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_dayview_market.py -q`
Expected: FAIL — `AttributeError: 'DayView' object has no attribute 'mkt_inv'`, `no attribute 'default_price_table'`, `TypeError: build_day() takes 3 positional arguments`.

- [ ] **Step 3: Extend `DayView` and `build_day` in `plan.py`**

Append two defaulted fields to `DayView` (after `price`):

```python
    price: object       # int[9]  current market prices
    # Hour-0 market, for the planner's own price projection (projector.py).
    # Defaulted to a fresh market so hand-built views stay valid.
    mkt_inv: object = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)   # int[9]
    shops: object = np.zeros(spec.N_SHOPS, np.int32)                         # int[8]
```

(Keep the existing "money is int32" comment below the class body.)

Add above `build_day`:

```python
_DEFAULT_TABLE = None


def default_price_table() -> np.ndarray:
    """The engine's default price table, built once. The sim passes its own
    (possibly market-randomised) `tables.price`; the submission and hand-built
    views use this."""
    global _DEFAULT_TABLE
    if _DEFAULT_TABLE is None:
        _DEFAULT_TABLE = spec.build_price_table()
    return _DEFAULT_TABLE
```

Change the signature and prologue:

```python
def build_day(xp, view: DayView, macro: Macro, price_table=None):
    """Whole-day plan. See the module docstring for the returned shapes.

    `price_table` is int32 [N_PRODUCTS, PRICE_TABLE_N] -- `tables.price` in the
    simulator so the planner projects with the very table the market prices
    with; None selects the engine default.
    """
    i32 = xp.int32
    if price_table is None:
        price_table = xp.asarray(default_price_table())
```

- [ ] **Step 4: Plumb the sim and the submission**

In `src/kagg3/sim/rollout.py::day_view` add to the `DayView(...)` call:

```python
        price=price, mkt_inv=st.mkt_inv, shops=st.shops,
```

and in `run_day`:

```python
    built = [P.build_day(jnp, day_view(st, p, day, price), plans[p], tables.price)
             for p in range(2)]
```

In `src/kagg3/agent/parse.py::parse_view` add to the returned `DayView(...)`:

```python
        price=np.array([obs["market"]["prices"][n] for n in spec.PRODUCTS], np.int32),
        mkt_inv=parse_market(obs)[0],
        shops=parse_town(obs),
```

(`runtime.py` needs no change: it calls `build_day` without a table and gets the default.)

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_dayview_market.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass, including `test_submission_runs.py` (the packaged agent parses real observations) and `test_sim_equivalence.py`.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/plan.py src/kagg3/sim/rollout.py src/kagg3/agent/parse.py tests/test_dayview_market.py
git commit -m "Give the planner the hour-0 market and the price table it will project with"
```

---

### Task 4: The price projector (§1.1)

**Files:**
- Create: `src/kagg3/core/projector.py`
- Modify: `scripts/package_submission.py` — the explicit `INCLUDE` list (~line 32-48)
- Test: `tests/test_projector.py`

**Interfaces:**
- Produces (all array-agnostic, `xp` first):
  - `projector.K: int = spec.SHED_CAPACITY + 1` (quote-walk length, 101)
  - `ticks_before(turn: int) -> (n_shop_ticks: int, n_center_ticks: int)` — Python ints
  - `town_tick_units(xp, shops) -> int[9]`
  - `projected_inv(xp, mkt_inv, shops, turn: int) -> int[9]` — opponent-free inventory when the market resolves at `turn`, before any own order that turn
  - `sell_quotes(xp, price_table, inv) -> int[9, K]` — price of the j-th unit sold solo
  - `sell_revenue(xp, quotes, qty) -> int[9]`
  - `marginal_quote(xp, quotes, sold) -> int[9]` — price the next unit fetches after `sold` units
- Consumers: Task 7 (`projected_inv`, `sell_quotes`, `marginal_quote`); Phase 1/2 add the buy side and lot-2/3 own-impact advancement here.

**Background (verified facts, §1.1).** Price is monotone non-increasing in inventory for all nine products across the whole table; town consumption raises prices (each shop instance consumes `SHOP_CONSUME` every `SHOP_SELL_INTERVAL` turns, the centre one of everything but fertilizer once a day); a sale at the floor pays but does not add supply — and because the table is monotone, quoting `price[inv + j]` for the j-th unit stays exact past the floor (the same trick `sim/market.py::_quotes` uses); buys drain supply. Turn order inside `rollout.run_day`: unit ops, market, then town tick — so the market at turn *t* sees the ticks of turns 0..t−1: shop ticks at every multiple of 4, the centre at turn 0. `core/` must not import `sim/` (the sim imports `core`), so the three-line quote walk is restated here rather than imported.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_projector.py`:

```python
"""The opponent-free price projector (PLANNER_V3_1 section 1.1) is exact table
arithmetic: its quotes must equal the simulator's market walk unit for unit,
and its town-tick schedule must equal the rollout's.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import projector as PJ
from kagg3.sim import market as M
from kagg3.sim.state import Tables

TABLE = spec.build_price_table()


def test_ticks_before_each_market_turn():
    assert PJ.ticks_before(0) == (0, 0)
    assert PJ.ticks_before(1) == (1, 1)      # turn 0's shop tick and centre tick
    assert PJ.ticks_before(2) == (1, 1)
    assert PJ.ticks_before(10) == (3, 1)     # shop ticks at 0, 4, 8
    assert PJ.ticks_before(18) == (5, 1)     # 0, 4, 8, 12, 16


def test_projected_inventory_matches_the_sim_town_tick():
    import jax.numpy as jnp
    from kagg3.sim import rollout
    from kagg3.sim.state import initial_state
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("BAKERY")] = 1
    shops[spec.SHOP_NAMES.index("YARN_STORE")] = 2
    st = initial_state(jnp)._replace(shops=jnp.asarray(shops))
    inv0 = np.asarray(st.mkt_inv)
    for turn in (1, 2, 10, 18):
        s = st
        for _ in range(turn):
            s = rollout.town_consume(s)._replace(step=s.step + 1)
        assert np.asarray(s.mkt_inv).tolist() == PJ.projected_inv(np, inv0, shops, turn).tolist()


def test_sell_quotes_match_the_engine_walk():
    tables = Tables(price=TABLE)
    rng = np.random.default_rng(0)
    for _ in range(60):
        item = int(rng.integers(0, spec.N_PRODUCTS))
        inv = int(rng.integers(spec.MARKET_I0 - 2000, spec.MARKET_I0 + 30000))
        n = int(rng.integers(0, spec.SHED_CAPACITY + 1))
        quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, inv, np.int32))
        qty = np.zeros(spec.N_PRODUCTS, np.int32)
        qty[item] = n
        _, revenue, _ = M.sell_walk(np, tables, item, inv, n, M.M_SELL_SOLO)
        assert int(PJ.sell_revenue(np, quotes, qty)[item]) == int(revenue)


def test_quotes_are_monotone_non_increasing():
    quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32))
    assert quotes.shape == (spec.N_PRODUCTS, PJ.K)
    assert np.all(np.diff(quotes, axis=1) <= 0)


def test_marginal_quote_is_the_next_unit():
    quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32))
    sold = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    assert PJ.marginal_quote(np, quotes, sold).tolist() == [int(quotes[p, p]) for p in range(spec.N_PRODUCTS)]


def test_projector_agrees_across_backends():
    import jax.numpy as jnp
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0 + 40, np.int32)
    shops = np.ones(spec.N_SHOPS, np.int32)
    a = PJ.sell_quotes(np, TABLE, PJ.projected_inv(np, inv, shops, 10))
    b = PJ.sell_quotes(jnp, jnp.asarray(TABLE), PJ.projected_inv(jnp, jnp.asarray(inv), jnp.asarray(shops), 10))
    assert a.tolist() == np.asarray(b).tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_projector.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.core.projector'`.

- [ ] **Step 3: Write the module**

Create `src/kagg3/core/projector.py`:

```python
"""Opponent-free price projection: exact own-impact table arithmetic.

PLANNER_V3_1 section 1.1. Verified facts this module stands on:

* price is monotone non-increasing in inventory for every product over the
  whole table (0 violations in 85,001 entries per row);
* the town raises prices: every shop instance consumes SHOP_CONSUME each
  SHOP_SELL_INTERVAL turns, the centre consumes one of everything but
  fertilizer once a day (turn 0);
* a sale at PRICE_FLOOR pays the seller but does not add to supply -- and
  since the table is monotone, quoting `price[inv + j]` for the j-th unit is
  still exact once the floor is reached (the walk in sim/market.py leans on
  the same fact);
* buys always drain supply.

Opponent impact is absent by construction -- that is the genes' job.

Array-agnostic (`xp` = numpy or jax.numpy). Turn arguments are Python ints,
so the tick counts fold at trace time. `core` must not import `sim` (the sim
imports `core`), which is why the quote walk is restated here.
"""

from __future__ import annotations

from .. import spec

#: Longest quote walk: one order never moves more than a shed's worth.
K = spec.SHED_CAPACITY + 1


def ticks_before(turn: int) -> tuple[int, int]:
    """(shop ticks, centre ticks) fired before the market resolves at `turn`.

    A turn runs unit ops, then market orders, then the town tick, so the ticks
    of turns 0 .. turn-1 have fired: shop ticks at every multiple of
    SHOP_SELL_INTERVAL, the centre tick at turn 0 (step % 24 == 0).
    """
    turn = int(turn)
    shop = (turn + spec.SHOP_SELL_INTERVAL - 1) // spec.SHOP_SELL_INTERVAL
    center = 1 if turn >= 1 else 0
    return shop, center


def town_tick_units(xp, shops):
    """int[9]: units the town's shops remove per shop tick."""
    return shops.astype(xp.int32) @ xp.asarray(spec.SHOP_CONSUME)


def projected_inv(xp, mkt_inv, shops, turn: int):
    """int[9]: market inventory when the market resolves at `turn`, from the
    hour-0 inventory, opponent-free and before any own order that turn."""
    shop, center = ticks_before(turn)
    return (mkt_inv.astype(xp.int32)
            - shop * town_tick_units(xp, shops)
            - center * xp.asarray(spec.TOWN_CENTER_CONSUME))


def sell_quotes(xp, price_table, inv):
    """int[9, K]: price paid for the j-th unit (j = 0..K-1) of each product
    sold solo from inventory `inv` -- the engine's quote walk, tabulated."""
    j = xp.arange(K, dtype=xp.int32)
    idx = xp.clip(inv.astype(xp.int32)[:, None] + j[None, :] - spec.PRICE_TABLE_LO,
                  0, spec.PRICE_TABLE_N - 1)
    return xp.take_along_axis(price_table, idx, axis=1)


def sell_revenue(xp, quotes, qty):
    """int[9]: revenue of selling `qty[p]` units along `quotes[p]`."""
    cum = xp.cumsum(quotes, axis=1)
    q = xp.clip(qty.astype(xp.int32), 0, K - 1)
    last = xp.take_along_axis(cum, xp.maximum(q - 1, 0)[:, None], axis=1)[:, 0]
    return xp.where(q > 0, last, 0)


def marginal_quote(xp, quotes, sold):
    """int[9]: what the next unit fetches after `sold[p]` units have gone."""
    s = xp.clip(sold.astype(xp.int32), 0, K - 1)
    return xp.take_along_axis(quotes, s[:, None], axis=1)[:, 0]
```

- [ ] **Step 3b: Ship the module in the submission archive**

`scripts/package_submission.py` builds the archive from an **explicit** `INCLUDE` list (`("core/plan.py", "kagg3/core/plan.py")`, …), not from the package tree. Task 7 makes `plan.py` import `projector`, so an archive without it fails on import — and a broken archive scores a silent 3,000 coins on the leaderboard. Add, directly after the `core/plan.py` entry:

```python
    ("core/projector.py", "kagg3/core/projector.py"),
```

- [ ] **Step 4: Run the tests**

Run: `python -m pytest tests/test_projector.py -q` — Expected: PASS (6 tests).
Run: `python scripts/package_submission.py && tar tzf dist/submission.tar.gz | grep projector` — Expected: `kagg3/core/projector.py` listed, no "forbidden import" complaint (the module imports only `spec`).
Run: `python -m pytest tests/test_submission_runs.py -q` — Expected: PASS, and specifically `test_archive_is_self_contained`: the other tests there put `src/` on `sys.path` and import the *repo*'s `kagg3`, so only that one (subprocess, repo unreachable) proves the archive carries the module.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/projector.py scripts/package_submission.py tests/test_projector.py
git commit -m "Add the opponent-free price projector: town ticks and tabulated sell quotes"
```

---

### Task 5: Day-29 endgame — terminal liquidation in the last lot (§0.4 day-29 law)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `build_day` (terminal flag, hire/purse gating, unit-op suppression, **the sale block hoisted out of `_market`**), `_market` signature
- Test: `tests/test_day29_endgame.py`

**Interfaces:**
- Consumes: `O.LAST_SHED_DAY` (Task 1).
- Produces inside `build_day`: `terminal` (bool scalar, `day > O.LAST_SHED_DAY`), `n_hire` (int32 scalar, replaces every `macro.n_hire` read), `wheat_reserved`, `avail` (int[9], hour-0 sellable stock net of reservations), `s_qty` (int[9], the day's gated sale). New `_market(xp, macro, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, s_qty, n_hire, terminal)` — no longer reads `view`, no longer computes the sale. Tasks 6 and 7 insert between `avail` and the `_market` call.

**Background.** Verified (§0.4): day 29 has no end-of-day, so a day-29 harvest never reaches the shed and the day-29 sale draws only on the hour-0 shed. Law: suppress every hire and BUY, emit no unit ops, liquidate the entire hour-0 shed ignoring reservation values (terminal value of anything unsold is exactly zero). Lot placement: verified in §1.2, opponent-free selling later within the day is uniformly weakly better on every town-consumed product and exactly indifferent for fertilizer — the exact split under that projection is *everything in the last lot* (turn 18), which the current earliest-first splitter cannot express, so the terminal day places lots itself. All of this is the `xp.where` on one scalar, so it traces shape-static.

**Label the two halves honestly.** *What* is sold (everything, gates and reservations void) is [LAW]. *Where* it is placed (all at 18) is [HEURISTIC] under the opponent-free projection — the spec's own §1.2 label — and §0.4's text says "across the three lots". The heuristic's known failure mode: an opponent who also liquidates on day 29 sells into the same turn-18 market, and `sim/market.py::_inventory_orders` then resolves the two seats through its *coupled* path, which the projection excludes by construction; the override also discards whatever timing the live `sell_lots` gene had learned for that day. Phase 0 adopts all-at-18 because it is the exact optimum of the only model Phase 0 has, and Task 8 step 4b runs the self-play check; the vs-opponent sign is a Phase-2 lineage question (§7). Write the code comment with that label, not as a law.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_day29_endgame.py`:

```python
"""Day 29 has no end-of-day (PLANNER_V3_1 section 0.4): nothing a unit does can
still monetize, purchases are dead money, and the hour-0 shed is all there is
left to sell -- so it all goes, gates and reservations ignored, in the last lot
(verified: opponent-free, all-at-18 weakly dominates every split).
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

SHED = {spec.I_WHEAT: 10, spec.I_EGG: 7, spec.I_MELON: 3, spec.I_FERT: 4, spec.I_GOOSE: 1}


def _view(day):
    """Five thirsty tomatoes at the head of the sweep, a stocked shed, cash."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:5] = spec.KIND_PLANT
    occ = z - 1
    occ[:5] = spec.I_TOMATO
    t_cons = z.copy()
    t_cons[:5] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in SHED.items():
        shed[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(5000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _greedy_macro():
    """Asks for everything: hires, land, seeds, animals, fertilizer, feeding --
    and gates every sale behind an unreachable price."""
    return _macro(n_hire=np.int32(3), buy_land=np.int32(1),
                  plant_target=np.array([5, 0, 0, 0, 0], np.int32),
                  animal_count=np.int32(2), n_fertilize=np.int32(2), fert_buy=np.int32(1),
                  feed_daily=np.int32(1), care_on=np.int32(1),
                  sell_min=np.full(spec.N_PRODUCTS, 10_000, np.int32), sell_lots=np.int32(3))


def _sold(op, arg, qty, turn):
    return {int(arg[turn, s]): int(qty[turn, s])
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) == O.MO_SELL}


def test_day_29_emits_no_unit_ops():
    unit_op = P.build_day(np, _view(29), _greedy_macro())[0]
    assert np.all(unit_op == O.OP_PASS)


def test_day_29_hires_and_buys_nothing():
    op, _, qty = P.build_day(np, _view(29), _greedy_macro())[3:6]
    assert np.all(op[O.TURN_HIRE] == O.MO_NONE) and int(qty[O.TURN_HIRE].sum()) == 0
    assert np.all(op[O.TURN_BUY] == O.MO_NONE) and int(qty[O.TURN_BUY].sum()) == 0


def test_day_29_liquidates_the_whole_shed_in_the_last_lot():
    op, arg, qty = P.build_day(np, _view(29), _greedy_macro())[3:6]
    for turn in O.SELL_TURNS[:-1]:
        assert _sold(op, arg, qty, turn) == {}
    # gate and feed reservation ignored; the goose is not a market product
    assert _sold(op, arg, qty, O.SELL_TURNS[-1]) == {
        spec.I_WHEAT: 10, spec.I_EGG: 7, spec.I_MELON: 3, spec.I_FERT: 4}


def test_day_28_is_not_terminal():
    unit_op, _, _, op, arg, qty = P.build_day(np, _view(28), _greedy_macro())
    assert int((unit_op == O.OP_WATER).sum()) >= 5      # 5 survival waterings, plus plant-then-water
    assert int((op[O.TURN_HIRE] == O.MO_HIRE).sum()) == 3
    for turn in O.SELL_TURNS:
        assert _sold(op, arg, qty, turn) == {}          # everything gated


def test_terminal_plan_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(29), _greedy_macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_day29_endgame.py -q`
Expected: FAIL — day-29 unit ops contain WATER, the hire row has 3 hires, and the last-lot sale is `{}`.

- [ ] **Step 3: Gate the day in `build_day`**

Right after `day = view.day` in `build_day`, add:

```python
    # Terminal day [LAW, 0.4]: past LAST_SHED_DAY nothing a unit does can
    # still monetize, purchases are dead money, and the hour-0 shed is all
    # there is left to sell. One scalar, applied with `where` so the plan
    # stays shape-static.
    terminal = day > O.LAST_SHED_DAY
    n_hire = xp.where(terminal, 0, macro.n_hire).astype(i32)
```

Then replace every later read of `macro.n_hire` in `build_day` with `n_hire` (the `hire_bill` `where` and `n_units = xp.asarray(1, i32) + n_hire`), and gate the purse so the walk buys nothing:

```python
    money = xp.where(terminal, 0, xp.maximum(view.money - hire_bill, 0)).astype(i32)
```

After the morning-PICKUP loop (just before the market call), suppress unit ops:

```python
    unit_op = xp.where(terminal, O.OP_PASS, unit_op).astype(i32)
    unit_a = xp.where(terminal, 0, unit_a).astype(i32)
    unit_q = xp.where(terminal, 0, unit_q).astype(i32)
```

- [ ] **Step 4: Hoist the sale out of `_market`**

Replace the `mkt = _market(...)` call at the end of `build_day` with:

```python
    # ---- the sale ---------------------------------------------------------
    # Shed contents only: the day's harvest reaches the shed at end-of-day and
    # is sold tomorrow morning, so the hour-0 stock is exactly what the lots
    # can draw on. Feed wheat is held back, and a product priced below its
    # gate this morning is held entirely. On the terminal day every
    # reservation is void and the whole shed goes.
    wheat_reserved = xp.where(terminal, 0, xp.sum(want_feed.astype(i32))).astype(i32)
    avail = view.shed[:spec.N_PRODUCTS].astype(i32)
    avail = _set1(xp, avail, spec.I_WHEAT,
                  xp.maximum(avail[spec.I_WHEAT] - wheat_reserved, 0))
    s_qty = xp.minimum(macro.sell_qty, avail)
    s_qty = xp.where(view.price >= macro.sell_min, s_qty, 0)
    s_qty = xp.where(terminal, avail, s_qty).astype(i32)

    mkt = _market(xp, macro, wheat_buy, fert_bought, seed_buy, a_buy, a_kind,
                  buy_land, s_qty, n_hire, terminal)
    return (unit_op, unit_a, unit_q) + mkt
```

Rewrite `_market`'s signature, hire row and SELL section:

```python
def _market(xp, macro, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land,
            s_qty, n_hire, terminal):
    """Fixed market schedule (see the module docstring). `s_qty` is the day's
    sale per product, already gated and reserved by the caller."""
    i32 = xp.int32
    op = xp.zeros((TPD, MO), dtype=i32)
    arg = xp.zeros((TPD, MO), dtype=i32)
    qty = xp.zeros((TPD, MO), dtype=i32)
    slot = xp.arange(MO, dtype=i32)

    # turn 0 -- hire the day's hands.
    op = _row(xp, op, O.TURN_HIRE, xp.where(slot < n_hire, O.MO_HIRE, O.MO_NONE))
    qty = _row(xp, qty, O.TURN_HIRE, xp.where(slot < n_hire, 1, 0))
```

(the turn-1 block is unchanged), and replace everything from `# SELL turns -- liquidate.` to the end of the function with:

```python
    # SELL turns. Split into `sell_lots` lots, the remainder going to the
    # earliest lots; lots past `sell_lots` are empty. The terminal day takes
    # the last lot alone [HEURISTIC, opponent-free]: selling later in the day
    # is weakly better on every town-consumed product and exactly indifferent
    # for fertilizer (verified, PLANNER_V3_1 1.2), so under that projection
    # the exact split of a liquidation is "everything at 18". An opponent
    # dumping into the same turn is outside the projection.
    pad = xp.zeros(MO - spec.N_PRODUCTS, i32)
    arg_row = xp.concatenate([xp.arange(spec.N_PRODUCTS, dtype=i32), pad])
    n_lots = xp.clip(macro.sell_lots, 1, len(O.SELL_TURNS)).astype(i32)
    base_lot = s_qty // n_lots
    rem = s_qty - base_lot * n_lots
    last = len(O.SELL_TURNS) - 1
    for k, turn in enumerate(O.SELL_TURNS):
        lot = xp.where(k < n_lots, base_lot + (k < rem).astype(i32), 0)
        lot = xp.where(terminal, s_qty if k == last else 0, lot).astype(i32)
        op = _row(xp, op, turn,
                  xp.concatenate([xp.where(lot > 0, O.MO_SELL, O.MO_NONE).astype(i32), pad]))
        arg = _row(xp, arg, turn, arg_row)
        qty = _row(xp, qty, turn, xp.concatenate([lot, pad]))
    return op, arg, qty
```

Also update the module docstring's layout table: `turn 0  market: HIRE x n_hire (none on the terminal day)`.

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_day29_endgame.py -q` — Expected: PASS (5 tests).
Run: `python -m pytest -q` — Expected: all pass; `test_sell_head.py`, `test_hire_bill.py`, `test_budget_order.py` exercise the hoisted sale and hire row and must be unaffected. If a sim-equivalence replay diverges on day 29, the cause is the sell-only path not seeing turn 18 — it does (`rollout.run_day` resolves `SELL_TURNS[1:]` with `sell_only=True`, and the last day runs 23 turns), so treat any divergence as a bug in this task, not the sim.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_day29_endgame.py
git commit -m "Liquidate the shed in the last lot on day 29 and emit nothing else"
```

---

### Task 6: Fertilizer reserved from the sale (§0.7)

**Files:**
- Modify: `src/kagg3/core/plan.py` — the sale block from Task 5 (between `avail` and `s_qty`)
- Test: `tests/test_fert_reserved.py`

**Interfaces:**
- Consumes: `n_fert_eff` (int32 scalar, already computed in the clamp section of `build_day`), `avail`, `terminal` (Task 5).
- Produces: `fert_reserved` (int32 scalar) inside `build_day`; `avail[I_FERT]` net of it. Task 7 reads `avail` after this.

**Background.** Verified race (§0.7): the day's FERTILIZE tasks pick their fertilizer up at turn 2 — or turn 3 when a feed pickup precedes it — while sell lot 1 fires at turn 2, so a sale can take the very units the plan will spread. `wheat_reserved` already guards feed wheat the same way; fertilizer mirrors it with `n_fert_eff` (the fertilizations the budget actually resourced).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_fert_reserved.py`:

```python
"""Fertilizer the day's FERTILIZE tasks will pick up is held back from the sale
(PLANNER_V3_1 section 0.7), mirroring the feed-wheat reservation: sell lot 1
fires at turn 2 while the fertilizer pickup can slide to turn 3.
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


def _view(fert_in_shed, n_thirsty=3):
    """`n_thirsty` tomatoes that must be watered today (so they can take
    fertilizer), `fert_in_shed` fertilizer in the shed."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:n_thirsty] = spec.KIND_PLANT
    occ = z - 1
    occ[:n_thirsty] = spec.I_TOMATO
    t_cons = z.copy()
    t_cons[:n_thirsty] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert_in_shed
    return P.DayView(
        day=np.int32(5), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _fert_sold(view, macro):
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    return sum(int(qty[t, s]) for t in O.SELL_TURNS for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[t, s]) == O.MO_SELL and int(arg[t, s]) == spec.I_FERT)


def _sell_all_fert():
    q = np.zeros(spec.N_PRODUCTS, np.int32)
    q[spec.I_FERT] = 100
    return q


def test_planned_fertilizer_is_held_back_from_the_sale():
    view = _view(fert_in_shed=5)
    unit_op = P.build_day(np, view, _macro(n_fertilize=np.int32(3), sell_qty=_sell_all_fert()))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 3
    assert _fert_sold(view, _macro(n_fertilize=np.int32(3), sell_qty=_sell_all_fert())) == 2


def test_nothing_reserved_when_nothing_is_fertilized():
    assert _fert_sold(_view(fert_in_shed=5), _macro(sell_qty=_sell_all_fert())) == 5


def test_reservation_is_capped_by_what_the_day_can_spread():
    # 8 requested, 5 in the shed, no purchase: n_fert_eff is 5, so none sells
    # -- and the reservation never goes negative.
    assert _fert_sold(_view(fert_in_shed=5, n_thirsty=8),
                      _macro(n_fertilize=np.int32(8), sell_qty=_sell_all_fert())) == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_fert_reserved.py -q`
Expected: FAIL — `5 == 2` on the first test (the sale takes all five).

- [ ] **Step 3: Reserve it**

In `build_day`'s sale block (Task 5), after the wheat line and before `s_qty = xp.minimum(...)`, add:

```python
    # The day's FERTILIZE tasks pick their fertilizer up at turn 2 or 3, after
    # sell lot 1 has fired at turn 2 [LAW, 0.7] -- reserve it like feed wheat.
    fert_reserved = xp.where(terminal, 0, n_fert_eff).astype(i32)
    avail = _set1(xp, avail, spec.I_FERT,
                  xp.maximum(avail[spec.I_FERT] - fert_reserved, 0))
```

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_fert_reserved.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass (`test_fert_source.py` covers the purchase side and is unaffected).
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_fert_reserved.py
git commit -m "Reserve the day's fertilizer from the sale, as feed wheat already is"
```

---

### Task 7: Shed-overflow forced sale, conservative-LOW, post-gate (§0.9)

**Files:**
- Modify: `src/kagg3/core/plan.py` — the budget walk (shed-room clamp on the three shed-bound buys), `_routes` (return the covered-tile mask), `build_day` (forced sale between the gated `s_qty` and the `_market` call), import `projector`
- Test: `tests/test_overflow_forced_sale.py`

**Interfaces:**
- Consumes: `projector.projected_inv`, `sell_quotes`, `marginal_quote` (Task 4); `price_table`, `view.mkt_inv`, `view.shops` (Task 3); `avail`, `s_qty`, `terminal` (Tasks 5–6); `chain_op` (int[100, CHAIN_MAX]), `blk` (int[3, MU]), `wheat_buy`, `fert_bought`, `a_buy`.
- Produces: `_routes(...)` now returns a fifth value `covered` (bool[100], view/serpentine space: tiles whose whole chain the day's labour executes); `build_day` locals `room`, `inflow`, `proj_eod`, `deficit`, `forced` (int[9]); `s_qty` includes `forced`; `wheat_buy`, `fert_bought`, `a_buy` together never exceed the hour-0 shed room.

**Background (§0.9).** End-of-day dumps every unit inventory into the shed and *destroys* what does not fit (`sim/eod.py::drop_inventories` zeroes the inventories after the capped take). Project tonight's shed **conservatively-LOW**, counting only certain inflow: the banked `t_yield` of harvests the route actually reaches (today's in-window watering bonuses excluded), one fertilizer per reached COLLECT, and this morning's buys (they land in the shed at turn 1) — against every certain outflow: the planned sale and the pickups the reached tasks consume (`blk`: feed wheat, spread fertilizer, placed animals). Whatever still does not fit is sold today on top of the gated sale, **bypassing the gate**, lowest marginal value first — Phase-0's value is the projected marginal sale price (turn-2 inventory) after the planned sale. Because quotes fall as a product is sold down, the cheapest product stays cheapest until it is spent, so draining products in ascending marginal quote is exactly the unit-by-unit greedy and takes nine static rounds. Forced sales draw only on hour-0 stock net of reservations, so a day whose certain inflow alone exceeds the shed still overflows (harvest batching is an open module, §5).

**Shed room caps the morning buys [LAW]** (found in review, `sim/market.py:176-210`, engine-equivalent): BUY_PRODUCT and BUY_ANIMAL are each clipped to `room = SHED_CAPACITY − sum(shed)` *at turn 1* — before lot 1 fires at turn 2, so no same-day sale makes room. The budget walk today ignores this (`wheat_avail = shed + wheat_buy`), so on a nearly full shed it plans feeds and fertilizations whose inputs the engine never delivers, and a projector that took the walk's `buys_in` at face value would over-project the shed and force-sell gated units the engine would never have dropped — a loss, not sign-safe. Both are fixed in one place: clamp the walk's three shed-bound buys by a running `room`, in the same style as the purse. The engine's fixed slot order may spend the room on a different category than the walk's `macro.order` did, but the total never exceeds room, so the row is honoured in any slot sequence — the same argument `_market` already makes for money. Seeds and land are not shed items and stay unclamped.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_overflow_forced_sale.py`:

```python
"""End-of-day destroys whatever the shed cannot hold. The planner projects
tonight's shed conservatively-LOW (PLANNER_V3_1 section 0.9) and force-sells
the cheapest marginal units today so that certain inflow survives. Forced
units bypass the price gate and never touch reserved feed wheat or fertilizer.
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

TABLE = spec.build_price_table()
FLOORED = spec.MARKET_I0 + 40_000       # every product is at the $1 floor here


def _view(shed, *, ripe=20, geese=0, tomato_inv=spec.MARKET_I0, wheat_inv=spec.MARKET_I0):
    """`ripe` tomatoes with one unit banked at the head of the sweep, then
    `geese` hungry geese; shed as given; market inventory per product."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_cons = z.copy()
    kind[:ripe] = spec.KIND_PLANT
    occ[:ripe] = spec.I_TOMATO
    t_yield[:ripe] = 1
    kind[ripe:ripe + geese] = spec.KIND_COOP
    occ[ripe:ripe + geese] = 0
    t_cons[ripe:ripe + geese] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_TOMATO] = tomato_inv
    inv[spec.I_WHEAT] = wheat_inv
    return P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(1000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32))


def _many_hands(**kw):
    """Ten hands, so every task tile is reached and the inflow is the full crop."""
    return _macro(n_hire=np.int32(spec.MAX_HANDS), **kw)


def _sold(plan):
    op, arg, qty = plan[3:6]
    out = np.zeros(spec.N_PRODUCTS, np.int64)
    for t in O.SELL_TURNS:
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(op[t, s]) == O.MO_SELL:
                out[int(arg[t, s])] += int(qty[t, s])
    return out


def test_certain_overflow_forces_the_cheapest_product_out():
    # shed 95 + 20 harvested units = 115: 15 must go, and floored tomato is
    # worth less at the margin than wheat at 25.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    assert int((plan[0] == O.OP_HARVEST).sum()) == 20
    sold = _sold(plan)
    assert sold[spec.I_TOMATO] == 15 and sold[spec.I_WHEAT] == 0


def test_forced_sale_bypasses_the_price_gate():
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    macro = _many_hands(sell_min=np.full(spec.N_PRODUCTS, 10_000, np.int32))
    assert _sold(P.build_day(np, view, macro, TABLE))[spec.I_TOMATO] == 15


def test_no_forced_sale_without_a_deficit():
    view = _view({spec.I_TOMATO: 75, spec.I_WHEAT: 5}, tomato_inv=FLOORED)      # 80 + 20 = 100 fits
    assert _sold(P.build_day(np, view, _many_hands(), TABLE)).sum() == 0


def test_forced_sale_drains_products_in_ascending_marginal_value():
    # wheat floored (cheapest) but only 5 spare: all 5 go, then 10 tomato.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, wheat_inv=FLOORED)
    sold = _sold(P.build_day(np, view, _many_hands(), TABLE))
    assert sold[spec.I_WHEAT] == 5 and sold[spec.I_TOMATO] == 10


def test_reserved_feed_wheat_is_never_forced():
    # 10 hungry geese eat 10 of the 10 wheat (an outflow, and a reservation):
    # 100 - 10 + 20 = 110, so 10 tomato go although wheat is cheaper.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 10}, geese=10, wheat_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    assert int((plan[0] == O.OP_FEED).sum()) == 10
    sold = _sold(plan)
    assert sold[spec.I_WHEAT] == 0 and sold[spec.I_TOMATO] == 10


def test_inflow_counts_only_the_harvests_labour_reaches():
    # One unit reaches a prefix of the 20 ripe tiles; the deficit is exactly
    # the reached yield over the 5 free slots, not the whole crop's.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _macro(), TABLE)
    n_reached = int((plan[0] == O.OP_HARVEST).sum())
    assert 0 < n_reached < 20
    assert _sold(plan)[spec.I_TOMATO] == n_reached - 5


def test_morning_buys_count_as_inflow_and_are_capped_by_shed_room():
    # 95 in the shed, 10 hungry geese, no wheat: the walk wants 10 wheat but
    # the market only takes what fits at turn 1 -- room is 5 -- so 5 are
    # bought, 5 geese are fed (the other 5 are not: no wheat exists for them),
    # and the wheat lands (100) and is eaten (95). Add 8 units of harvest and
    # 3 must go. Uncapped, the plan would book 10 in and 10 out and reach the
    # same 3 for the wrong reason.
    view = _view({spec.I_TOMATO: 95}, ripe=8, geese=10, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    op, arg, qty = plan[3:6]
    bought = sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
                 if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_WHEAT)
    assert bought == 5
    assert int((plan[0] == O.OP_FEED).sum()) == 5
    assert _sold(plan)[spec.I_TOMATO] == 3


def test_a_full_shed_buys_nothing_shed_bound():
    # 100 in the shed: room is 0, so no wheat is bought and no feed is planned
    # even with cash and hungry geese; seeds are not shed items and still buy.
    view = _view({spec.I_TOMATO: 100}, ripe=0, geese=10, tomato_inv=FLOORED)
    macro = _many_hands(plant_target=np.array([2, 0, 0, 0, 0], np.int32))
    plan = P.build_day(np, view, macro, TABLE)
    op, qty = plan[3], plan[5]
    row = [(int(op[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s])) for s in range(spec.MAX_MARKET_ORDERS)]
    assert all(q == 0 for o, q in row if o == O.MO_BUY_PRODUCT)
    assert any(o == O.MO_BUY_SEED and q == 2 for o, q in row)
    assert int((plan[0] == O.OP_FEED).sum()) == 0


def test_forced_sale_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    macro = _many_hands()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

Fixture arithmetic the implementer should be able to reproduce: with ten hands the hire bill is `HIRE_COST[:10].sum() = 143` of the 1,000 coins; each of the 11 units has a 22-turn budget (21 with a feed pickup), so all 20 ripe tiles (positions 0..19) and 10 geese are reached. With one unit and no pickups the farmer walks 8 moves to position 0, harvests (9 turns), then 2 turns per further tile: 7 tiles in 22 turns. In the morning-buys test the 5 wheat cost 125 ≤ 857 and are reserved, so they are not sellable either way; `test_reserved_feed_wheat_is_never_forced` has room 0 but needs no purchase (10 wheat already in the shed), so it is unaffected by the clamp.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_overflow_forced_sale.py -q`
Expected: FAIL — every `sold` is 0; the morning-buys test also fails on `bought == 5` (10 today) and the full-shed test on the wheat row (10 today).

- [ ] **Step 2b: Clamp the walk's shed-bound buys by hour-0 room**

In `build_day`, next to `money = xp.maximum(view.money - hire_bill, 0)`, add:

```python
    # Shed room caps every shed-bound buy at turn 1 [LAW]: the market clips
    # BUY_PRODUCT and BUY_ANIMAL to SHED_CAPACITY - sum(shed) slot by slot,
    # and lot 1 only fires at turn 2, so no same-day sale makes room. Seeds
    # and land are not shed items. Walked down like the purse.
    room = xp.maximum(spec.SHED_CAPACITY - xp.sum(view.shed.astype(i32)), 0).astype(i32)
```

Inside the `for pos in range(N_BUDGET_CATS)` loop, clamp the three candidates and walk the room down after the money line:

```python
        c_wheat = xp.minimum(xp.minimum(wheat_short, (money // p_wheat).astype(i32)), room)
        c_fert = xp.minimum(xp.minimum(fert_short, (money // p_fert).astype(i32)), room)
        c_anim = xp.minimum(xp.minimum(xp.maximum(a_want - a_have, 0),
                                       (money // a_cost).astype(i32)), room)
        ...
        room = room - (is_w * c_wheat + is_f * c_fert + is_a * c_anim)
```

(`c_seed` and `c_land` are untouched.) `wheat_avail`, `fert_avail`, `a_avail` and every task set downstream now clamp to what the engine will actually deliver, and `test_fert_source.py` / `test_budget_order.py` must still pass — their fixtures start from an empty shed, where `room = 100` never binds.

- [ ] **Step 3: Report the reached tiles from `_routes`**

At the end of `_routes`, after the unit loop (where `start` holds the rank after the last active block), replace the `return` with:

```python
    # Tiles the day's labour actually reaches: ranks below `start`, mapped
    # back to view (serpentine) tile space so the caller can read chains and
    # yields off it directly.
    cov_rank = xp.arange(N_T, dtype=i32) < start
    if hasattr(order, "at"):
        covered = xp.zeros(N_T, bool).at[order].set(cov_rank)
    else:
        covered = np.zeros(N_T, bool)
        covered[np.asarray(order)] = np.asarray(cov_rank)
    return (xp.stack(route_op), xp.stack(route_a), xp.stack(route_q),
            xp.stack(blk, axis=1), covered)          # blk -> [3, MU]
```

and update the call in `build_day` to unpack the fifth value:

```python
    route_op, route_a, route_q, blk, covered = _routes(
        xp, chain_op, chain_a, chain_q, n_ops, score, tier,
        xp.stack([want_feed, want_fert, m_place]), n_units, budget)
```

- [ ] **Step 4: Project the shed and force the sale**

Add `from . import projector as PJ` to `plan.py`'s imports (next to `from . import ops as O`).

In `build_day`'s sale block, after the Task-6 fertilizer reservation and the three `s_qty` lines (gated and terminal-overridden), insert before the `_market` call:

```python
    # ---- shed overflow: forced sale [LAW, 0.9] ---------------------------
    # End-of-day destroys whatever the shed cannot hold. Project tonight's
    # shed conservatively-LOW -- only inflow that is certain: the banked yield
    # of harvests the route reaches (today's watering bonuses excluded), one
    # fertilizer per reached COLLECT, this morning's buys -- against every
    # certain outflow: the planned sale and the pickups the reached tasks
    # consume. Whatever still does not fit is sold today on top of the gated
    # sale, cheapest marginal unit first. Forced sales draw only on the
    # hour-0 stock net of reservations, so a day whose certain inflow alone
    # exceeds the shed still overflows (harvest batching: open, section 5).
    has_harv = xp.sum((chain_op == O.OP_HARVEST).astype(i32), axis=1) > 0
    has_coll = xp.sum((chain_op == O.OP_COLLECT_FERT).astype(i32), axis=1) > 0
    inflow = (xp.sum(xp.where(covered & has_harv, view.t_yield, 0).astype(i32))
              + xp.sum((covered & has_coll).astype(i32)))
    buys_in = (wheat_buy + fert_bought + a_buy).astype(i32)   # <= hour-0 room by the walk's clamp
    picks_out = xp.sum(blk).astype(i32)           # wheat fed, fertilizer spread, animals placed
    proj_eod = xp.sum(view.shed.astype(i32)) - xp.sum(s_qty) - picks_out + buys_in + inflow
    deficit = xp.maximum(proj_eod - spec.SHED_CAPACITY, 0).astype(i32)

    # Rank by the projected marginal price after the planned sale (lot-1
    # inventory). Quotes fall as a product is sold down, so the cheapest
    # product stays cheapest until it is spent: draining products in ascending
    # marginal quote is the unit-by-unit greedy, in nine static rounds.
    spare = xp.maximum(avail - s_qty, 0).astype(i32)
    inv_lot1 = PJ.projected_inv(xp, view.mkt_inv, view.shops, O.SELL_TURNS[0])
    marg = PJ.marginal_quote(xp, PJ.sell_quotes(xp, price_table, inv_lot1), s_qty)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)
    forced = xp.zeros(spec.N_PRODUCTS, i32)
    left = deficit
    for _ in range(spec.N_PRODUCTS):
        key = xp.where(spare > 0, marg * spec.N_PRODUCTS + pid, _BIG)   # ties: lower index
        pick = xp.argmin(key)
        amt = xp.where(spare[pick] > 0, xp.minimum(left, spare[pick]), 0).astype(i32)
        hit = (pid == pick).astype(i32)
        forced = forced + hit * amt
        spare = spare - hit * spare[pick]
        left = left - amt
    s_qty = (s_qty + forced).astype(i32)
```

(`_BIG = 1 << 20` already exists in `plan.py`; `marg * 9 + 8` stays far below it. On the terminal day `s_qty == avail`, so `spare` is zero and nothing is forced.)

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_overflow_forced_sale.py -q` — Expected: PASS (9 tests).
Run: `python -m pytest -q` — Expected: all pass. Watch `test_backend_agreement.py` and `test_sim_equivalence.py` in particular: the `covered` scatter and the `take_along_axis` gathers are the new cross-backend surface.
Run: `ruff check src tests`.

- [ ] **Step 6: Measure the compile-time cost (§7: "every optimizer lands with a compile-time and throughput measurement")**

Run: `python scripts/bench_sim.py` with no arguments (it has no `--help`; positional args are batch sizes and default to `64 256 1024`; it prints `compile+run` and `run` per batch, and the first is the compile-time figure) once on this commit and once on the Task-6 commit (`git stash` is not enough — use `git worktree add /tmp/claude-0/kagg3-t6 HEAD~1` and run there). Record both numbers in the commit message. The expected delta is within noise; if it exceeds 5% of the Task-6 figure, report it and stop rather than optimising.

- [ ] **Step 7: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_overflow_forced_sale.py
git commit -m "Force-sell the cheapest units when tonight's certain inflow would overflow the shed; cap morning buys by shed room"
```

---

### Task 8: Verification and the frozen-theta measurement (§7)

**Files:**
- No source changes expected. Produces a measurement record appended to this plan (section "Phase-0 result" below) and a memory-worthy number.

**Interfaces:**
- Consumes: everything above, `artifacts/theta.npy` (the ES mean — never `champion.npy`), `scripts/eval_vs_baselines.py` (seeds fixed by `default_rng(20260821)`; prints `mean coins` per opponent; plays the real engine through the numpy submission path, so it exercises `parse_view` → `build_day` end to end).

**Predictions, stated before the run (§7 demands it).** Under the frozen `theta.npy`, per item: 0.1 deadline harvest ≥ 0 (units that decayed unsold are now sold); day-29 liquidation ≥ 0 (stock the theta held past day 28 is now sold); 0.9 forced sale ≥ 0 (units destroyed at eod are now sold); 0.7 fert reservation ≈ 0 (the theta rarely sells fertilizer it also spreads); 0.5 mandatory tier: sign unknown but small — the theta's `prio` weights were learned under the old ordering and may have encoded "skip survival work" compensations; shed-room clamp on morning buys (Task 7) ≈ 0 (coins the engine refused to take are now simply not planned). One *input* shift to name: Task 1 changes `brain.n_free_slots`, a network feature, on the days where the clamp binds (a wheat planted after d24, carrot after d25, melon after d16 now counts free one to four days earlier) — the frozen theta sees slightly different late-season features; predicted negligible. Net prediction: absolute mean coins vs `starter` non-negative, well inside one paired-CI of zero if the theta never reached these situations. This is a smoke test at `n = 16` seed pairs, not an architectural decision (§7).

- [ ] **Step 1: Full suite and lint on the final commit**

Run: `python -m pytest -q` — Expected: all pass.
Run: `ruff check src tests` — Expected: clean.

- [ ] **Step 2: Package and run the submission once**

Run: `python scripts/package_submission.py` — Expected: writes `dist/submission.tar.gz` with no "forbidden import" complaint (the new `projector.py` imports only `spec`). Confirm `kagg3/core/projector.py` is inside the archive (`tar tzf dist/submission.tar.gz | grep projector`) — the `INCLUDE` list is explicit (Task 4 step 3b), and a missing module makes the packaged agent fail on import, which the leaderboard scores as a silent 3,000 coins. Only `test_archive_is_self_contained` isolates the import path; the rest of that file imports the repo's `kagg3` and would pass with a broken archive.
Then: `python -m pytest tests/test_submission_runs.py -q` — Expected: PASS.

- [ ] **Step 3: Baseline numbers from the pre-Phase-0 tree**

```bash
git worktree add /tmp/claude-0/kagg3-base 42ef59a
cd /tmp/claude-0/kagg3-base
python scripts/eval_vs_baselines.py --theta /mnt/e/_work/kaggriculture3/artifacts/theta.npy --games 16 --opponents starter random
cd /mnt/e/_work/kaggriculture3
```

Record the `mean coins` and `mean margin` lines verbatim.

- [ ] **Step 4: Phase-0 numbers**

```bash
python scripts/eval_vs_baselines.py --theta artifacts/theta.npy --games 16 --opponents starter random
```

Record the same lines. Same seeds, same theta, same engine — the only difference is the planner.

- [ ] **Step 4b: Self-play check for the opponent-coupled items**

`starter`/`random` never compete for prices, so they cannot exercise the two Phase-0 choices that depend on the other seat: the day-29 all-at-18 placement (Task 5 — under `sim/market.py::_inventory_orders` two seats selling the same item on the same turn take the *coupled* path, exactly what the opponent-free projection excludes) and the mandatory tier. `scripts/ladder.py` runs theta-vs-pool in the simulator with both seats on the planner, so:

```bash
python -c "import numpy as np; np.save('/tmp/claude-0/pool1.npy', np.stack([np.load('artifacts/theta.npy')]))"
python scripts/ladder.py artifacts/theta.npy /tmp/claude-0/pool1.npy 32
```

Record the `win %` line. Prediction: 50% ± noise — both seats run the same Phase-0 planner, so this only detects a *sim-side* asymmetry or crash; the vs-opponent sign of the day-29 placement is not measurable under a frozen theta and is left for Phase 2's lineage comparison (§7). If the run errors, that is a Phase-0 bug (both seats must stay on the same market slot layout, `assert_no_cross`).

- [ ] **Step 5: Write the result into this plan**

Append a section `## Phase-0 result (frozen theta.npy, n = 16 seed pairs × 2 seats)` to this file with both tables, the delta, and one line per prediction above marked *held* / *did not hold*. If the delta vs `starter` is negative beyond noise, **do not tune anything** — the next step is a per-task bisection (each task is one commit) to name the item, reported to the user; the spec's laws are claims about the engine, and a regression means either the spec or the implementation is wrong, which is a finding, not a knob.

- [ ] **Step 6: Clean up and commit**

```bash
git worktree remove /tmp/claude-0/kagg3-base
git add docs/superpowers/plans/2026-08-24-planner-v31-phase0.md
git commit -m "Record the Phase-0 frozen-theta measurement"
```

---

## Self-review notes (written with the plan)

- **Spec coverage, Phase 0 (§8):** §1.1 → Task 4; §0.1 (+ plant-gate consistency) → Task 1; §0.5 (interim: all survival feeds) → Task 2; §0.7 → Task 6; §0.9 → Task 7; §0.4 day-29 → Task 5; §6.2 stale comment → Task 1. §7 measurement → Task 8 (compile-time in Task 7 step 6). Not in Phase 0 by the spec's own phasing: §0.4 day-28 rules, §0.2, 0.6, 0.8, 0.10–0.12, §§1.2–1.6, §2, §3, §4, §5.
- **Addition beyond the spec's list (review 2026-08-24):** the shed-room clamp on morning buys (Task 7 step 2b). Not named in `PLANNER_V3_1.md`, but it is a pure engine invariant (`sim/market.py:176-210`) with no gene, i.e. Phase-0 class by §8's own definition, and §0.9's sign-safety depends on it. Spec §0.9/§0.10 should pick it up in the next errata pass.
- **Deviation worth knowing:** §8 names "0.4's day-29 lot split" as a projector consumer and §0.4 says "across the three lots". §1.2's verified finding is that the opponent-free optimum *is* everything in the last lot, so Task 5 places the terminal lots directly — labeled [HEURISTIC], not [LAW] — and the projector's first consumer is §0.9 (Task 7). Task 8 step 4b is the self-play check; if a later lineage measurement shows a split beating all-at-18 in play, the projector already has what an allocator needs.
- **Review corrections folded in (2026-08-24):** `projector.py` added to the packaging list (Task 4 step 3b — `INCLUDE` is explicit, and an archive missing a module scores a silent 3,000; only `test_archive_is_self_contained` can see it); shed-room clamp (above); `bench_sim.py` has no `--help`; `n_free_slots` feature shift named in Task 8's predictions; docstring move counts corrected (position 99 is 9 moves from (4,4); one unit reaches ~7 tiles).
- **Type consistency:** `task_order(xp, task, score, tier=None)` (Task 2) is what `_routes` calls; `_routes` returns 5 values from Task 7 on (4 before); `_market(xp, macro, wheat_buy, fert_buy, seed_buy, a_buy, a_kind, buy_land, s_qty, n_hire, terminal)` from Task 5 on; `build_day(xp, view, macro, price_table=None)` from Task 3 on; `DayView.mkt_inv`/`.shops` from Task 3 on; `ops.LAST_SHED_DAY` from Task 1 on.

---

## Phase-0 result (frozen theta.npy, n = 16 seed pairs × 2 seats)

Measured 2026-08-24 on branch `fitness-shaping`, HEAD `163f1d5` (Tasks 1–7 landed as
nine commits — Task 3 split into `6261858`+`488f75b`, Task 7 into `e16edca`+`163f1d5` —
plus three separate doc/plan commits in the same range), against the pre-Phase-0 tree
`42ef59a`. Same frozen `artifacts/theta.npy` (3892 float32, the ES mean — not
`champion.npy`), same seeds (`default_rng(20260821)`), same engine rules; the sim's only
change is the planner-interface plumbing in `rollout.py` (`mkt_inv`/`shops`/`tables.price`,
3 lines) — the rest of the difference between the two rows of each table is the planner.

### Step 1 — suite and lint

```
python -m pytest -q      161 tests, 161 passed, exit 0
ruff check src tests     25 errors, none introduced by this plan
```

The suite prints no summary line because the repo's own `addopts = "-q"` (pyproject.toml)
plus the explicit `-q` makes pytest double-quiet; `--collect-only` reports 161 tests collected
and the run emits 161 passing dots and exits 0.

`ruff` on the files Phase 0 touched — `src/kagg3/core/{ops,plan,brain,projector}.py`,
`src/kagg3/sim/rollout.py`, `src/kagg3/agent/parse.py`, `scripts/package_submission.py`
and the seven new test files — is clean ("All checks passed!"). The two remaining hits in
`tests/test_task_priority.py` are `C408` on the `_view`/`_macro` fixture dicts at lines 35
and 47, present verbatim at `42ef59a`; the repo-wide 25 break down as 5 in `src/kagg3/es/archetypes.py`,
1 in `src/kagg3/sim/market.py`, those 2, and 17 across twelve older test files.

### Step 2 — packaging

```
python scripts/package_submission.py
dist/submission.tar.gz  0.05 MB  sha256=138f0538c7dc6e9c8e7f018d965df5a9af3e9f6e55df6d06baa8f045c57c144c
tar tzf dist/submission.tar.gz | grep projector  ->  kagg3/core/projector.py
python -m pytest tests/test_submission_runs.py -q  ->  11 dots, [100%], exit 0
  (re-run without the doubled -q for a summary line: 11 passed in 51.30s)
```

No "forbidden import" complaint, and `projector.py` is inside the archive — the failure
mode this guards against (a module missing from the explicit `INCLUDE` list) scores a
silent 3,000 coins on the leaderboard and only `test_archive_is_self_contained` can see it.

### Steps 3 and 4 — the two engine measurements

`scripts/eval_vs_baselines.py --theta <theta> --games 16 --opponents starter random`,
verbatim:

**Baseline, `42ef59a`** (run in a worktree at that commit, with this repo's `theta.npy`):

```
64 games in 42s  theta=/mnt/e/_work/kaggriculture3/artifacts/theta.npy
  vs starter   win 100.0%   mean coins     41986   mean margin    +38352   (n=32)
  vs random    win 100.0%   mean coins     35572   mean margin    +35572   (n=32)
```

**Phase 0, `163f1d5`:**

```
64 games in 50s  theta=artifacts/theta.npy
  vs starter   win 100.0%   mean coins     45442   mean margin    +41808   (n=32)
  vs random    win 100.0%   mean coins     41731   mean margin    +41727   (n=32)
```

| opponent | baseline `42ef59a` | Phase 0 `163f1d5` | delta (mean coins) |
|---|---|---|---|
| `starter` | 41 986 | 45 442 | **+3 456** (+8.2 %) |
| `random`  | 35 572 | 41 731 | **+6 159** (+17.3 %) |

| opponent | baseline margin | Phase 0 margin | delta (mean margin) |
|---|---|---|---|
| `starter` | +38 352 | +41 808 | **+3 456** |
| `random`  | +35 572 | +41 727 | **+6 155** |

Win rate is 100 % in both trees against both opponents, so the delta is a level shift in
coins, not a flip in any game. The script prints only the per-opponent aggregate over
n = 32 (16 seeds × 2 seats) — it keeps no per-game record — so no paired CI is available
without re-running both trees; what is reported above is what it prints.

### Step 4b — self-play check

```
python scripts/ladder.py artifacts/theta.npy /tmp/claude-0/pool1.npy 32
theta vs 1 pool members, 32 seeds x 2 seats
  vs pool[0]  win 2901781.2%
```

The run does not error, which is what this step is for: the Phase-0 planner completes the
self-play path on the GPU with no exception. The printed percentage is
not a win rate: `ladder.py` is stale with respect to `es/train.py::make_evaluator`, which
now returns raw `[mine, theirs]` coins rather than the win bit, so `r.mean() * 100` prints
100 × the mean final money. `ladder.py` is untouched by this plan (last modified in
`3c07bd3`, before the evaluator changed) — a pre-existing script bug, not a Phase-0 one.
Recovering the bit with `train.win_scores`' rule over the same call gives:

```
  vs pool[0]  win  50.0%   mean coins     29018   mean margin        +0   (n=64)
```

(`r.mean() = 29017.8` × 100 is `ladder.py`'s printed 2901781.2 %, confirming the
diagnosis.) JAX ran on `CudaDevice(id=0)`.

**The exact 50.0 % / margin +0 is not evidence of seat symmetry in the sim.** In
`es/train.py::make_evaluator`, `a = jnp.where(seat == 0, theta_c, theta_o)` and
`b = jnp.where(seat == 0, theta_o, theta_c)`; with `pool1.npy = [theta]`, `theta_c ==
theta_o`, so `a == b` for every row regardless of `seat` — `seat` only relabels which of
`money[0]`/`money[1]` is reported as "mine" after an identical `rollout.episode` call. For
a fixed seed the seat=0 row reports margin `A−B` and the seat=1 row `B−A`, so the
aggregate margin is exactly 0 and the aggregate win rate exactly 50 % by algebraic
cancellation, regardless of whether `money[0]` and `money[1]` actually differed. A real
per-seat/index bias in the engine would show up as `A_s ≠ B_s` for a given seed, and this
aggregate cancels that signal rather than ruling it out. Separately, `assert_no_cross`
(`src/kagg3/sim/market.py`) is called only from `tests/test_gates.py`, never from the
`rollout.episode`/`make_evaluator` path this script exercises, so it was **not** checked
by this run. What Step 4b actually establishes: the Phase-0 planner runs the self-play
path without error or exception on the GPU.

### Predictions, scored

The frozen-theta run measures all seven tasks (nine commits — Tasks 3 and 7 each split in
two) jointly; it cannot attribute the +3 456 to
any single item, and no per-task bisection was run because the delta is positive. Each
per-item prediction below is therefore scored only as far as this measurement can score it.

- **§0.1 deadline harvest ≥ 0** — *not individually measured*; not contradicted (the
  aggregate is positive). Attribution would need the per-task bisection.
- **§0.4 day-29 liquidation ≥ 0** — *not individually measured*; not contradicted.
- **§0.9 forced sale ≥ 0** — *not individually measured*; not contradicted.
- **§0.7 fertilizer reservation ≈ 0** — *not individually measured*; not contradicted.
- **§0.5 mandatory tier, sign unknown but small** — *not individually measured*; the
  joint sign is positive, so the feared "skip survival work" compensation baked into the
  theta's `prio` weights did not swamp the rest.
- **Shed-room clamp on morning buys (Task 7) ≈ 0** — *not individually measured*; not
  contradicted.
- **`brain.n_free_slots` input shift, negligible** — *not individually measured*; not
  contradicted. It is the one *input* change (a late-season slot counts free one to four
  days earlier), so it is the first suspect if a Phase-2 lineage measurement disagrees.
- **Net: mean coins vs `starter` non-negative** — **held**, decisively: +3 456 (+8.2 %),
  and +6 159 (+17.3 %) vs `random`.
- **Net: "well inside one paired-CI of zero *if* the theta never reached these
  situations"** — the conditional's antecedent is **false**: at +8.2 % and +17.3 % the
  frozen theta plainly *did* reach the situations Phase 0 changed. It was decaying stock
  it could have sold, and the engine was refusing or destroying units it had planned.
- **Step 4b: self-play 50 % ± noise** — **held, but trivially**: with one theta copy
  in both seats, `make_evaluator` sets `a == b` regardless of `seat`, so 50.0 % / margin +0
  follows by algebraic cancellation across the seat=0/seat=1 rows for each seed, not from
  anything the run measured about seat symmetry. The run's real content is that it
  completed without error or exception.

### Known cost

Task 7's compile-time measurement (`scripts/bench_sim.py`, compile + run): B = 64
38.7 s → 43.1 s (+11.4 %), B = 256 40.8 s → 44.6 s (+9.3 %), B = 1024 39.3 s → 44.4 s
(+13.0 %). Steady-state run throughput is unchanged at ~2 180 eps/s (the mean of Task 7's
seven per-batch throughput samples at B=1024 — 2,194/2,170/2,164 eps/s before, 2,229/2,137/
2,141/2,236 eps/s after — not a single measurement). This exceeds the
5 % compile-time gate the plan set for Task 7 and was reported rather than optimised
(controller ruling): a one-off ~4 s per compile against ~1.6 s generations is a rounding
error over a training run, and no market turns were added, which is the throughput cost
that would have mattered (~6 % each).

### Standing

This is the §7 smoke test at n = 16 seed pairs, not an architectural decision. It says the
Phase-0 planner does not regress a theta trained against the old one — the opposite, by a
wide margin — and that the self-play path runs without error on the GPU; it does not
establish seat symmetry in the simulator (Step 4b's 50 % / margin +0 holds by construction
under identical thetas — see above). The vs-opponent sign of
the day-29 all-at-18 placement is still not measurable under a frozen theta and is left to
Phase 2's lineage comparison.
