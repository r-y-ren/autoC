# Planner V3.1 — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Dispatch each task to a fresh **Opus** subagent (`model: "opus"`); the implementer sees only its own task plus the header, so every task repeats what it needs.

**Goal:** Land every Phase-1 item of `docs/PLANNER_V3_1.md` §8 — the laws and near-laws that touch live-gene behaviour — one bisectable commit per item, then measure the frozen theta with each item's predicted sign stated before the run.

**Architecture:** All rules live in the shared planner (`src/kagg3/core/plan.py`) plus two array-agnostic helper modules: `core/projector.py` (extended with the buy side) and a new `core/valuation.py` (fire schedules and coin values of animals, crops and fertilizer applications). Both executors run the planner verbatim, so the sim changes only to plumb one more `DayView` field (`t_bank`, the pending CARE bonus). Four genes (`n_fertilize`, `fert_buy`, `feed_daily`, `care_on`) stop being read by the planner but stay in `Macro` and in `brain.decide`, so every checkpoint still decodes; masking them is Phase 2.

**Tech Stack:** Python 3, numpy, JAX (CPU for tests), pytest, ruff.

**Spec:** `docs/PLANNER_V3_1.md` — Phase 1 is §8's second bullet: §0.6 rationing, §0.8 animal-count semantics, §0.10 engine-curve pricing, §0.11 cadence + value-ranked fertilizer, §0.12 per-unit pickups, §0.2 animal bound, §0.4 day-28 value-conditional rules. Audit record: `docs/PLANNER_V3_1_REVIEW.md`. Read both before starting a task.

**Prerequisite:** the Phase-0 plan (`docs/superpowers/plans/2026-08-24-planner-v31-phase0.md`) is fully landed — `git log --oneline | grep "Record the Phase-0"` must hit. This plan quotes post-Phase-0 code by content, not by line number: `ops.LAST_SHED_DAY`, `DayView.mkt_inv`/`.shops`, `build_day(xp, view, macro, price_table=None)`, `core/projector.py`, the hoisted sale block, `_routes(...)` returning `covered`, and `task_order(..., tier)` all exist.

**Out of scope (later plans):** Phase 2 (§1.2–1.6 optimizers, §2 genome re-type and parameter masking, fresh lineage) and Phase 3 (§3, §4 DROP, M1–M3). §7 says architectural decisions need paired CIs over multiple training seeds; Phase 2 is gated on this plan's Task 9.

## Global Constraints

Every task's requirements implicitly include this section.

- Planner code is array-agnostic (`xp` = numpy or `jax.numpy`), shape-static, int32, no data-dependent Python control flow; pairwise ranking instead of sorting (see `task_order`, `_count_le` in `plan.py`).
- Tie-breaking: pairwise/lexicographic, ties to the lower serpentine index. Never pack a tier or a value into the int32 sort key.
- Market orders only on turns 0, 1, 2, 10, 18 (§6.1); no new market turns.
- Both seats keep an identical market slot layout (`sim/market.py::assert_no_cross`).
- `Macro` fields are **never removed** in Phase 1 and `brain.decide` is untouched: deleted genes are decoded and ignored (§8: "the current lineage keeps training with those heads decoded-but-ignored"). `artifacts/theta.npy` must still load and replay.
- Valuation prices are today's hour-0 quotes (`view.price`) — the Phase-1 "projected price". Opponent-dependent and multi-day value is [LEARNED] and arrives in Phase 2; say so in the docstring of every function that uses a price.
- Every day number derives from `O.LAST_SHED_DAY` (28); a harvest on day `h` sells on `h + 1`, so it is monetizable iff `h <= O.LAST_SHED_DAY`. A production fire at the end of day `e` becomes harvestable on `h = e + 1`.
- `core/` never imports `sim/`.
- Cross-unit same-tile same-turn disjointness (§6.3) must keep holding.
- Tests: file header `os.environ.setdefault("JAX_PLATFORMS", "cpu")`, `sys.path.insert(0, "src")`; fixtures follow `tests/test_budget_order.py`'s `_view`/`_macro`; filler tiles that must stay occupied hold an **ongoing** crop (`spec.I_TOMATO`/`spec.I_STRAWBERRY`); run `python -m pytest tests/<file>.py -q`, full suite `python -m pytest -q` (it includes the sim-vs-engine gates).
- Interpreter: every `python` in this plan means the repo's `.venv/bin/python` (or a shell with that venv activated) — the system `python` has neither JAX nor `kaggle_environments`, so the full suite and the engine evals cannot run under it.
- Lint: `ruff check src tests` clean before every commit. Commit per task on branch `fitness-shaping`, one-line sentence-case imperative message. Never commit `artifacts/`.

## Engine facts the tasks lean on (verified against the pinned engine and `sim/`)

- `BUY_PRODUCT` walks the curve: the j-th unit is quoted at `price[inv - 1 - j]`; the engine stops at the first unit the purse cannot pay (`sim/market.py::buy_walk`). Turn-1 inventory is the hour-0 inventory minus turn 0's shop tick and centre tick (`projector.projected_inv(..., O.TURN_BUY)`).
- Animal at eod of day `e` (`sim/eod.py::refresh_animals`, engine `_daily_refresh_animals`): unfed → `consecutive_unfed += 1`, escapes at 2; fires iff `(e + 1 - placed_day - first) >= 0` and `% interval == 0`; on a fire, `bonus = pending_care_bonus if fed_today else 0` is consumed, `yield = min(max_held, yield + 1 + bonus)`, the bank is zeroed; then `if cared_today and fed_today: bank += 1` (so a fire-day care banks toward the **next** fire); `fertilizer_available = True`.
- The observation carries `pending_care_bonus` on every animal tile (engine `_new_animal_tile` sets it to 0); the sim keeps it in `State.t_bank`.
- Ongoing crop at eod `e` (`refresh_plants`): fires iff `dsf = e + 1 - planted_day - first >= 0`, `dsf % interval == 0` and `dsf // interval + 1 <= max_yield` (so at most `max_yield` fires); `yield += 2 if watered_today and fertilized_until_day >= e else 1`, capped at `max_yield`. `FERTILIZE` sets `fertilized_until_day = max(old, day + 2)` — active on `day, day+1, day+2`.
- One-time crop: born with `yield = 1`; a watering at age in `[CROP_WINDOW_START, max_yield_day]` adds `+2` if fertilized else `+1`, capped at `CROP_MAX_YIELD`; harvested at `harvest_age = clip(LAST_SHED_DAY - planted_day, first, max_yield_day)` (Phase 0).
- `PICKUP` is silently dropped unless the unit stands on a shed-access tile; units spawn on one and the planner's pickups precede any movement.

## File map

| File | Responsibility after Phase 1 |
|---|---|
| `src/kagg3/core/projector.py` | + `buy_quotes` (Task 1) |
| `src/kagg3/core/valuation.py` | **new** — `fires_between`, `fires_on`, `next_fire_after`, `crop_fires_on`, `animal_value`, `fert_marginal_value` (Task 2) |
| `src/kagg3/core/plan.py` | engine-curve wheat/fert pricing; `animal_count` semantics; acquisition bound; value-ranked feed rationing (`_rank_by`); feed cadence, CARE rule, day-28 survival law; value-ranked fertilizer + fertilized fire-day watering; per-unit pickup accounting in `_routes`; `DayView.t_bank` |
| `src/kagg3/sim/rollout.py`, `src/kagg3/agent/parse.py` | plumb `t_bank` (Task 6) |
| `tests/test_buy_pricing.py`, `test_valuation.py`, `test_animal_count_semantics.py`, `test_animal_acquisition_bound.py`, `test_feed_rationing.py`, `test_feed_care_cadence.py`, `test_fertilizer_value.py`, `test_unit_pickups.py` | one per task; `tests/test_fert_source.py` and `tests/test_fert_reserved.py` are updated in Task 7 |

Task order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. Tasks 4–7 consume Task 2; Task 8 is independent of 2–7 but lands last because it rewrites `_routes`.

---

### Task 1: Engine-curve buy pricing for wheat and fertilizer (§0.10)

**Files:**
- Modify: `src/kagg3/core/projector.py` (append `buy_quotes`)
- Modify: `src/kagg3/core/plan.py` — the budget walk in `build_day` (the block from `p_wheat = ...` through the `for pos in range(N_BUDGET_CATS)` loop), plus a `_cum_take` helper
- Test: `tests/test_buy_pricing.py`

**Interfaces:**
- Consumes: `projector.projected_inv(xp, mkt_inv, shops, turn)`, `projector.K`, `price_table` (local in `build_day`), `O.TURN_BUY`.
- Produces: `projector.buy_quotes(xp, price_table, inv) -> int[9, K]` (price of the j-th unit bought solo); `plan._cum_take(xp, cum, k)` (`cum[k-1]`, 0 when `k == 0`); inside `build_day` the locals `inv_buy`, `buy_q`, `wheat_cum`, `fert_cum`. `p_wheat`/`p_fert` are removed; later tasks price wheat at `view.price[spec.I_WHEAT]`.

**Background.** Today the walk prices feed wheat and fertilizer at the flat hour-0 quote (`money // p_wheat`). The engine drains inventory one unit per unit bought and re-quotes, so the flat price under-charges by the curve's rise; the row then over-commits and the engine drops whatever sits in the last BUY slot (the same failure `test_hire_bill.py` documents for the hire bill). Walk the curve exactly as `sim/market.py::buy_walk` does. Cross-seat same-turn coupling (both seats buying wheat in the same slot) is the acknowledged residual.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_buy_pricing.py`:

```python
"""Feed wheat and fertilizer are bought along the engine's price curve
(PLANNER_V3_1 section 0.10): every unit drains the market and re-quotes, and
the engine stops at the first unit the purse cannot pay. The walk must commit
exactly what the engine will honour.
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
from kagg3.core import projector as PJ
from kagg3.sim import market as M
from kagg3.sim.state import Tables

TABLE = spec.build_price_table()


def _view(n_hungry, money, wheat_inv=spec.MARKET_I0, shops=None):
    """`n_hungry` geese that must be fed today, no wheat in the shed, so the
    walk wants exactly `n_hungry` wheat."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:n_hungry] = spec.KIND_COOP
    occ = z - 1
    occ[:n_hungry] = 0
    t_cons = z.copy()
    t_cons[:n_hungry] = 1
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_WHEAT] = wheat_inv
    return P.DayView(
        day=np.int32(5), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32) if shops is None else shops)


def _wheat_bought(view):
    op, arg, qty = P.build_day(np, view, _macro(), TABLE)[3:6]
    row = O.TURN_BUY
    return sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[row, s]) == O.MO_BUY_PRODUCT and int(arg[row, s]) == spec.I_WHEAT)


def _engine_affords(view, n, money):
    inv1 = PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY)
    k, cost = M.buy_walk(np, Tables(price=TABLE), spec.I_WHEAT, int(inv1[spec.I_WHEAT]),
                         n, money, M.M_BUY_SOLO)
    return int(k), int(cost)


def test_walk_commits_what_the_curve_affords():
    # 30 hungry geese, 750 coins: the flat hour-0 price (25) would commit all
    # 30, but the curve rises as the market drains and the engine stops short.
    view = _view(30, 750)
    k, cost = _engine_affords(view, 30, 750)
    assert k < 30 and cost <= 750
    assert _wheat_bought(view) == k


def test_a_rich_purse_still_buys_everything():
    view = _view(30, 100_000)
    assert _wheat_bought(view) == 30


def test_turn_zero_town_tick_is_charged():
    # Two bakeries drain wheat at turn 0 before the BUY row resolves at turn 1.
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("BAKERY")] = 2
    view = _view(30, 750, shops=shops)
    k, _ = _engine_affords(view, 30, 750)
    assert _wheat_bought(view) == k


def test_buy_quotes_are_the_engine_walk():
    tables = Tables(price=TABLE)
    rng = np.random.default_rng(0)
    for _ in range(40):
        item = int(rng.integers(0, spec.N_PRODUCTS))
        inv = int(rng.integers(spec.MARKET_I0 - 2000, spec.MARKET_I0 + 30000))
        n = int(rng.integers(0, spec.SHED_CAPACITY + 1))
        q = PJ.buy_quotes(np, TABLE, np.full(spec.N_PRODUCTS, inv, np.int32))[item]
        k, cost = M.buy_walk(np, tables, item, inv, n, 10**9, M.M_BUY_SOLO)
        assert int(np.cumsum(q)[k - 1]) == int(cost) if k > 0 else int(cost) == 0


def test_curve_pricing_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(30, 750), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_buy_pricing.py -q`
Expected: FAIL — `AttributeError: module 'kagg3.core.projector' has no attribute 'buy_quotes'` and `30 == k` (the walk commits 30).

- [ ] **Step 3: Add the buy side to the projector**

Append to `src/kagg3/core/projector.py`:

```python


def buy_quotes(xp, price_table, inv):
    """int[9, K]: price paid for the j-th unit (j = 0..K-1) of each product
    bought solo from inventory `inv`. Every unit drains one, so the j-th is
    quoted at `inv - 1 - j` -- the engine's walk, tabulated."""
    j = xp.arange(K, dtype=xp.int32)
    idx = xp.clip(inv.astype(xp.int32)[:, None] - 1 - j[None, :] - spec.PRICE_TABLE_LO,
                  0, spec.PRICE_TABLE_N - 1)
    return xp.take_along_axis(price_table, idx, axis=1)
```

- [ ] **Step 4: Walk the curve in the budget walk**

In `src/kagg3/core/plan.py` add next to `_count_le`:

```python
def _cum_take(xp, cum, k):
    """cum[k-1]: the total over the first k rounds of a quote walk (0 when k == 0)."""
    return xp.where(k > 0, cum[xp.clip(k - 1, 0, cum.shape[0] - 1)], 0)
```

In `build_day`, replace the two lines

```python
    p_wheat = xp.maximum(view.price[spec.I_WHEAT], 1)
    p_fert = xp.maximum(view.price[spec.I_FERT], 1)
```

with:

```python
    # Engine-curve buy pricing [LAW, 0.10]: BUY_PRODUCT walks the curve one
    # unit at a time from the hour-0 inventory advanced by the turn-0 town
    # tick, and stops at the first unit the purse cannot pay. A flat hour-0
    # price over-commits by the curve's rise, and the engine then drops
    # whatever sits in the last BUY slot. Cross-seat same-turn coupling is the
    # acknowledged residual.
    inv_buy = PJ.projected_inv(xp, view.mkt_inv, view.shops, O.TURN_BUY)
    buy_q = PJ.buy_quotes(xp, price_table, inv_buy)
    wheat_cum = xp.cumsum(buy_q[spec.I_WHEAT])
    fert_cum = xp.cumsum(buy_q[spec.I_FERT])
```

In the `for pos in range(N_BUDGET_CATS)` loop replace

```python
        c_wheat = xp.minimum(wheat_short, (money // p_wheat).astype(i32))
        c_fert = xp.minimum(fert_short, (money // p_fert).astype(i32))
```

with

```python
        c_wheat = xp.minimum(wheat_short, xp.sum((wheat_cum <= money).astype(i32)))
        c_fert = xp.minimum(fert_short, xp.sum((fert_cum <= money).astype(i32)))
```

and in the `money = money - (...)` update replace `is_w * c_wheat * p_wheat + is_f * c_fert * p_fert` with `is_w * _cum_take(xp, wheat_cum, c_wheat) + is_f * _cum_take(xp, fert_cum, c_fert)`.

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_buy_pricing.py -q` — Expected: PASS (5 tests).
Run: `python -m pytest -q` — Expected: all pass. `test_budget_order.py`/`test_learned_order.py` price purchases in a market at `MARKET_I0` with tiny quantities, where the curve is within a coin of flat; if one of them asserts an exact wheat count that the curve changes, update the number and say so in the commit message.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/projector.py src/kagg3/core/plan.py tests/test_buy_pricing.py
git commit -m "Price feed wheat and fertilizer purchases along the engine's curve"
```

---

### Task 2: The valuation module — fire schedules and coin values

**Files:**
- Create: `src/kagg3/core/valuation.py`
- Test: `tests/test_valuation.py`

**Interfaces (all array-agnostic, elementwise over tile vectors or scalars; all int32):**
- `fires_between(xp, t_day, first, interval, lo_day, hi_day) -> int` — count of harvest days `h = t_day + first + k*interval` (k ≥ 0) with `lo_day <= h <= hi_day`.
- `fires_on(xp, t_day, first, interval, h) -> bool` — whether a fire lands on harvest day `h`.
- `next_fire_after(xp, t_day, first, interval, day) -> int` — harvest day of the first fire whose eod is strictly after today's (i.e. `h >= day + 2`), the fire a CARE emitted today pays on.
- `crop_fires_on(xp, t_day, crop, h) -> bool` — `fires_on` for an ongoing crop, capped at its `CROP_MAX_YIELD` fires.
- `animal_value(xp, price, t_day, t_yield, t_favail, a, day) -> int` — remaining sellable production of a standing animal of kind `a`, in coins at `price`.
- `fert_marginal_value(xp, price, t_day, t_yield, crop, day, harvest_age) -> int` — coins one fertilizer application today adds to the crop on this tile.
- Consumers: Task 4 (`fires_between`), Task 5 (`animal_value`), Task 6 (`fires_on`, `next_fire_after`), Task 7 (`crop_fires_on`, `fert_marginal_value`).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_valuation.py`:

```python
"""Fire schedules and coin values (PLANNER_V3_1 sections 0.2, 0.6, 0.11) are
closed-form integer arithmetic over the engine's tables. Checked against a
brute-force replay of the end-of-day rules and against the spec's own numbers.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import valuation as V

PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)   # the default base prices
I = np.int32


def _brute_fires(t_day, first, interval, lo, hi):
    return sum(1 for h in range(lo, hi + 1)
               if h - t_day - first >= 0 and (h - t_day - first) % interval == 0)


def test_fires_between_matches_brute_force():
    rng = np.random.default_rng(0)
    for _ in range(300):
        t_day, first = int(rng.integers(0, 29)), int(rng.integers(1, 11))
        interval = int(rng.integers(1, 4))
        lo, hi = int(rng.integers(0, 30)), int(rng.integers(0, 30))
        got = int(V.fires_between(np, I(t_day), I(first), I(interval), I(lo), I(hi)))
        assert got == _brute_fires(t_day, first, interval, lo, hi), (t_day, first, interval, lo, hi)


def test_fires_between_is_vectorised_over_tiles():
    t_day = np.array([0, 5, 20], np.int32)
    got = V.fires_between(np, t_day, I(4), I(1), I(6), I(28))       # geese
    assert got.tolist() == [23, 20, 5]                                # h = 6..28, 9..28, 24..28


def test_fires_on_and_next_fire_after():
    # cow placed day 0: fires on harvest days 8, 10, 12, ...
    assert bool(V.fires_on(np, I(0), I(8), I(2), I(8)))
    assert not bool(V.fires_on(np, I(0), I(8), I(2), I(9)))
    assert not bool(V.fires_on(np, I(0), I(8), I(2), I(7)))
    # a CARE on day 9 pays on the first fire whose eod is after day 9's: day 12
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(9))) == 12
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(8))) == 10
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(2))) == 8      # before maturity: the first fire
    # goose (interval 1): always the day after tomorrow
    assert int(V.next_fire_after(np, I(0), I(4), I(1), I(10))) == 12


def test_crop_fires_stop_at_max_yield():
    tomato = I(spec.I_TOMATO)                     # first 8, interval 1, max_yield 4
    fires = [bool(V.crop_fires_on(np, I(0), tomato, I(h))) for h in range(6, 14)]
    assert fires == [False, False, True, True, True, True, False, False]   # 8..11 only


def test_animal_value_at_the_spec_numbers():
    # goose placed day 0, seen on day 5: 23 eggs at 50, 23 fertilizers at 100
    v = V.animal_value(np, PRICE, I(0), I(0), I(0), I(0), I(5))
    assert int(v) == 23 * 50 + 23 * 100
    # banked units and today's fertilizer count too
    v2 = V.animal_value(np, PRICE, I(0), I(2), I(1), I(0), I(5))
    assert int(v2) == int(v) + 2 * 50 + 100
    # a goose seen on day 28 has nothing left to sell
    assert int(V.animal_value(np, PRICE, I(0), I(0), I(0), I(0), I(28))) == 0


def test_fertilizer_value_at_the_spec_numbers():
    ha = lambda crop, t_day: I(int(np.clip(O.LAST_SHED_DAY - t_day, spec.CROP_FIRST_YIELD_DAY[crop],
                                              spec.CROP_MAX_YIELD_DAY[crop])))
    # tomato planted day 0 fertilized on day 8: fires 9, 10, 11 in the window -> +3
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(8), ha(2, 0))) == 3 * 60
    # on day 10 only fire 11 is left; on day 11 nothing
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(10), ha(2, 0))) == 60
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(11), ha(2, 0))) == 0
    # wheat planted day 0 fertilized on day 2: +2 (whole-window cap); carrot +1; melon 0
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_WHEAT), I(2), ha(0, 0))) == 2 * 25
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_CARROT), I(2), ha(1, 0))) == 35
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_MELON), I(6), ha(4, 0))) == 0
    # day-28 same-day chain on a wheat planted day 25 (harvest age 3): +1, never more
    assert int(V.fert_marginal_value(np, PRICE, I(25), I(3), I(spec.I_WHEAT), I(28), ha(0, 25))) == 25
    # an ongoing crop's fire at eod 28 is not monetizable
    assert int(V.fert_marginal_value(np, PRICE, I(20), I(0), I(spec.I_TOMATO), I(28), ha(2, 20))) == 0


def test_valuation_agrees_across_backends():
    import jax.numpy as jnp
    t_day = np.array([0, 3, 7, 12, 25], np.int32)
    crop = np.array([2, 0, 3, 4, 0], np.int32)
    ha = np.clip(O.LAST_SHED_DAY - t_day, spec.CROP_FIRST_YIELD_DAY[crop],
                 spec.CROP_MAX_YIELD_DAY[crop]).astype(np.int32)
    a = V.fert_marginal_value(np, PRICE, t_day, np.ones(5, np.int32), crop, I(9), ha)
    b = V.fert_marginal_value(jnp, jnp.asarray(PRICE), jnp.asarray(t_day), jnp.ones(5, jnp.int32),
                              jnp.asarray(crop), jnp.int32(9), jnp.asarray(ha))
    assert a.tolist() == np.asarray(b).tolist()
    c = V.animal_value(np, PRICE, t_day, np.zeros(5, np.int32), np.zeros(5, np.int32),
                       np.array([0, 1, 2, 0, 1], np.int32), I(9))
    d = V.animal_value(jnp, jnp.asarray(PRICE), jnp.asarray(t_day), jnp.zeros(5, jnp.int32),
                       jnp.zeros(5, jnp.int32), jnp.asarray(np.array([0, 1, 2, 0, 1], np.int32)), jnp.int32(9))
    assert c.tolist() == np.asarray(d).tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_valuation.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'kagg3.core.valuation'`.

- [ ] **Step 3: Write the module**

Create `src/kagg3/core/valuation.py`:

```python
"""Fire schedules and coin values, closed-form over the engine's tables.

PLANNER_V3_1 sections 0.2, 0.6 and 0.11 all need the same three questions
answered per tile without a loop: when does this animal or crop produce next,
how many monetizable productions are left, and what is one more input worth.
Everything here is int32 elementwise arithmetic so it vectorises over the 100
tiles and traces shape-static on both backends.

Calendar conventions (see the plan's engine facts):

* A production fire at the end of day `e` is harvestable on `h = e + 1`;
  a harvest on day `h` reaches the shed at eod `h` and sells on `h + 1`, so
  it is monetizable iff `h <= ops.LAST_SHED_DAY`.
* An animal placed on `t_day` with `first`/`interval` fires on harvest days
  `t_day + first + k * interval`, k >= 0. An ongoing crop does the same but
  fires at most `CROP_MAX_YIELD` times.

Prices are today's hour-0 quotes -- the Phase-1 projection. Opponent impact
and multi-day drift are [LEARNED] and arrive with the Phase-2 genome.
"""

from __future__ import annotations

from .. import spec
from . import ops as O


def fires_between(xp, t_day, first, interval, lo_day, hi_day):
    """Number of harvest days `h = t_day + first + k*interval` (k >= 0) with
    `lo_day <= h <= hi_day`."""
    base = t_day + first
    lo = xp.maximum(lo_day, base)
    k0 = (lo - base + interval - 1) // interval                # lo >= base: non-negative
    k1 = xp.where(hi_day >= base, (hi_day - base) // interval, -1)
    return xp.maximum(k1 - k0 + 1, 0)


def fires_on(xp, t_day, first, interval, h):
    """Whether a fire lands on harvest day `h`."""
    d = h - (t_day + first)
    return (d >= 0) & (d % interval == 0)


def next_fire_after(xp, t_day, first, interval, day):
    """Harvest day of the first fire whose end-of-day is strictly after
    today's -- the fire a CARE emitted today pays on (a fire-day care banks
    toward the *next* fire; so does a care on a quiet day)."""
    base = t_day + first
    lo = xp.maximum(day + 2, base)
    k = (lo - base + interval - 1) // interval
    return base + k * interval


def crop_fires_on(xp, t_day, crop, h):
    """`fires_on` for an ongoing crop, which fires at most CROP_MAX_YIELD times."""
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    d = h - (t_day + first)
    return (d >= 0) & (d % interval == 0) & (d // interval <= mxy - 1)


def animal_value(xp, price, t_day, t_yield, t_favail, a, day):
    """Remaining sellable production of a standing animal of kind `a`, in
    coins at today's prices: the units it holds plus every fire still
    harvestable by LAST_SHED_DAY, times its product's price, plus one
    fertilizer per remaining day (today's if already available), times the
    fertilizer price. Assumes it is fed and harvested; that is the caller's
    rationing question, not this function's."""
    first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a]
    interval = xp.asarray(spec.ANIMAL_INTERVAL)[a]
    prod = xp.asarray(spec.ANIMAL_PRODUCT)[a]
    sellable_today = (day <= O.LAST_SHED_DAY).astype(xp.int32)
    units = t_yield * sellable_today + fires_between(xp, t_day, first, interval, day + 1, O.LAST_SHED_DAY)
    fert = xp.maximum(O.LAST_SHED_DAY - day, 0) + t_favail * sellable_today
    return units * price[prod] + fert * price[spec.I_FERT]


def fert_marginal_value(xp, price, t_day, t_yield, crop, day, harvest_age):
    """Coins one fertilizer application today adds on this tile [0.11].

    Fertilizer is active on day, day+1, day+2. Ongoing crop: +1 unit per fire
    in that window that is watered at its eod (the planner waters fertilized
    crops on fire days) and still monetizable, capped at the crop's last
    fire. One-time crop: each in-window watering in the fertilized days adds
    +2 instead of +1, clipped at CROP_MAX_YIELD against the yield the
    remaining unfertilized waterings would reach anyway -- so a crop that
    saturates without fertilizer (melon watered daily) is worth 0, and the
    day-28 same-day FERTILIZE->WATER->HARVEST chain is worth at most +1.

    Ongoing crops ignore `t_yield`: the planner harvests a crop whenever it
    holds units, so a fire is never clipped by CROP_MAX_YIELD in practice.
    """
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]

    base = t_day + first
    last_h = base + (mxy - 1) * interval
    hi = xp.minimum(xp.minimum(day + 3, O.LAST_SHED_DAY), last_h)
    n_ong = fires_between(xp, t_day, first, interval, day + 1, hi)

    d_h = t_day + harvest_age
    w_lo = xp.maximum(day, t_day + ws)
    n_water = xp.maximum(d_h - w_lo + 1, 0)                             # in-window waterings left
    n_fert = xp.maximum(xp.minimum(day + 2, d_h) - w_lo + 1, 0)         # ... of which fertilized
    gain_one = xp.minimum(mxy, t_yield + n_water + n_fert) - xp.minimum(mxy, t_yield + n_water)
    gain_one = xp.where(d_h <= O.LAST_SHED_DAY, gain_one, 0)

    units = xp.where(ongoing == 1, n_ong, gain_one)
    return units * price[crop]
```

- [ ] **Step 4: Run the tests**

Run: `python -m pytest tests/test_valuation.py -q` — Expected: PASS (7 tests).
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/valuation.py tests/test_valuation.py
git commit -m "Add closed-form fire schedules and coin values for animals, crops and fertilizer"
```

---

### Task 3: `animal_count = 0` means zero (§0.8)

**Files:**
- Modify: `src/kagg3/core/plan.py` — the `a_want = ...` line in `build_day`'s budget walk and the comment on `Macro.animal_count`
- Test: `tests/test_animal_count_semantics.py`

**Interfaces:**
- Produces: `a_want = xp.minimum(macro.animal_count, n_free + n_struct_free)`. Unchanged downstream: `a_avail = a_have + a_buy`, `place_here` (standing structures stocked first from what is in hand), `n_build`.

**Background.** Today `a_want = min(animal_count, n_free) + n_struct_free`: every empty structure is restocked whatever the gene says, which is exactly the buy→starve→escape→re-buy loop `kagg3-land-toxicity` measured. Law: the gene is the count of animals acquired today, structures free or not; standing structures are stocked before new ones are built. Animals already in the shed are placed regardless — placing stock is not an acquisition. **Predicted frozen-theta sign: non-positive.** The current theta learned under the old decode (a zero count still restocked), so it may under-request animals; it is stated before Task 9's run and is the retraining case Phase 2 makes.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_animal_count_semantics.py`:

```python
"""`animal_count` is the number of animals acquired today, full stop
(PLANNER_V3_1 section 0.8): zero restocks nothing, standing structures are
stocked before new ones are built, and stock already in the shed is placed
because placing is not an acquisition.
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


def _view(free_coops=2, geese_in_shed=0):
    """`free_coops` empty coops at the head of the sweep, everything else
    empty; 3,000 coins on day 0."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:free_coops] = spec.KIND_COOP
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = geese_in_shed
    return P.DayView(
        day=np.int32(0), kind=kind, occ=z - 1, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _counts(view, animal_count):
    plan = P.build_day(np, view, _macro(animal_count=np.int32(animal_count)))
    unit_op, op, qty = plan[0], plan[3], plan[5]
    bought = int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_ANIMAL].sum())
    return bought, int((unit_op == O.OP_PLACE).sum()), int((unit_op == O.OP_BUILD_COOP).sum())


def test_zero_acquires_nothing_even_with_empty_structures():
    assert _counts(_view(free_coops=2), 0) == (0, 0, 0)


def test_one_stocks_a_standing_coop_before_building():
    assert _counts(_view(free_coops=2), 1) == (1, 1, 0)


def test_three_stocks_both_coops_and_builds_one():
    assert _counts(_view(free_coops=2), 3) == (3, 3, 1)


def test_shed_stock_is_placed_without_being_counted():
    # two geese already bought sit in the shed: they go into the coops today
    # although the gene asks for no acquisition
    assert _counts(_view(free_coops=2, geese_in_shed=2), 0) == (0, 2, 0)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_animal_count_semantics.py -q`
Expected: FAIL — the first test buys 2 and places 2.

- [ ] **Step 3: Change the decode**

In `build_day` replace

```python
    a_want = xp.minimum(macro.animal_count, n_free) + n_struct_free
```

with

```python
    # `animal_count` is the day's acquisition, structures free or not [LAW,
    # 0.8]: zero restocks nothing. Standing structures are stocked before new
    # ones are built (`place_here` below), and stock already in the shed is
    # placed regardless -- placing is not an acquisition.
    a_want = xp.minimum(macro.animal_count, n_free + n_struct_free)
```

In the `Macro` docstring change the `animal_count` comment to `# int     animals to acquire today (stocks free structures first)`.

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_animal_count_semantics.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass (`test_budget_order.py`, `test_hire_bill.py`, `test_learned_order.py` build on blank boards with no free structures, where the two formulas agree).
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_animal_count_semantics.py
git commit -m "Make animal_count the day's acquisition: zero restocks nothing"
```

---

### Task 4: Animal acquisition upper-bound value test (§0.2)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `build_day` before the budget-walk loop, and `c_anim` inside it; import `valuation`
- Test: `tests/test_animal_acquisition_bound.py`

**Interfaces:**
- Consumes: `valuation.fires_between`, `a_kind`, `a_cost`, `a_want`, `a_have`, `view.price`, `O.LAST_SHED_DAY`.
- Produces: inside `build_day` the scalar bool `acquire_ok`; `c_anim` is zero when it is false. Stock on hand is still placed.

**Background (§0.2).** Reject buying animal kind `a` on day `d` iff an *optimistic* bound on its remaining value is non-positive:

    UB = (product units harvestable by LAST_SHED_DAY, at today's product price)
       + (fertilizer collections on days d+1 .. LAST_SHED_DAY, at today's fertilizer price)
       - animal cost - feed cost

A new animal is placed today (`t_day = d`) with `fed_today = 0`, so it is hungry on `d+1`, `d+3`, ...; it must survive through eod `LAST_SHED_DAY - 1` to yield the last collection, so feeds = `(LAST_SHED_DAY - d) // 2` at today's wheat price. Rejection on a non-positive optimistic bound is safe under the opponent-free projection; acceptance goes through the normal walk. Labour is deliberately left out. Only the *purchase* is gated; animals already in the shed are placed. Spec check (default prices): goose on day 25 → 0 eggs + 3×100 − 300 − 1×25 = −25 → reject; day 24 → 50 + 400 − 300 − 50 = +100 → buy.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_animal_acquisition_bound.py`:

```python
"""A late animal is bought only if an optimistic bound on what it can still
sell beats its cost and feed (PLANNER_V3_1 section 0.2). Numbers below are
the spec's own: a day-25 goose collects three fertilizers and lays no
sellable egg.
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


def _view(day, fert_price=100, geese_in_shed=0):
    z = np.zeros(100, np.int32)
    price = BASE.copy()
    price[spec.I_FERT] = fert_price
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = geese_in_shed
    return P.DayView(
        day=np.int32(day), kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1), price=price)


def _bought(view, kind, count=1):
    plan = P.build_day(np, view, _macro(animal_kind=np.int32(kind), animal_count=np.int32(count)))
    op, qty = plan[3], plan[5]
    return int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_ANIMAL].sum())


def test_day_25_goose_is_rejected():
    assert _bought(_view(25), 0) == 0


def test_day_24_goose_is_bought():
    assert _bought(_view(24), 0) == 1


def test_a_dearer_fertilizer_flips_the_day_25_goose():
    # 3 x 109 - 300 - 25 = +2
    assert _bought(_view(25, fert_price=109), 0) == 1
    assert _bought(_view(25, fert_price=108), 0) == 0


def test_sheep_needs_a_fire_in_the_calendar():
    # placed day 20: wool on day 26 (200) + 8 x 100 - 500 - 4 x 25 > 0
    assert _bought(_view(20), 2) == 1
    # placed day 23: first wool on day 29 -- 5 x 100 - 500 - 2 x 25 < 0
    assert _bought(_view(23), 2) == 0


def test_rejection_does_not_touch_stock_in_hand():
    unit_op = P.build_day(np, _view(25, geese_in_shed=1),
                          _macro(animal_kind=np.int32(0), animal_count=np.int32(1)))[0]
    assert int((unit_op == O.OP_BUILD_COOP).sum()) == 1
    assert int((unit_op == O.OP_PLACE).sum()) == 1
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_animal_acquisition_bound.py -q`
Expected: FAIL — the day-25 goose is bought (`1 == 0`).

- [ ] **Step 3: Gate the purchase**

Add `from . import valuation as VAL` to `plan.py`'s imports (next to `from . import projector as PJ`).

In `build_day`, directly after `land_cost = ...` (before the walk's zero-initialisations), add:

```python
    # Animal acquisition: upper-bound value test [EXACT-OPT, 0.2]. A new
    # animal is placed today and hungry on day+1, day+3, ...; it must live
    # through eod LAST_SHED_DAY-1 for its last collection. Reject only on a
    # non-positive *optimistic* bound (today's prices, no labour), so the
    # rejection is safe under the opponent-free projection; acceptance goes
    # through the normal walk. Stock already in the shed is placed regardless.
    a_first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a_kind]
    a_int = xp.asarray(spec.ANIMAL_INTERVAL)[a_kind]
    a_prod = xp.asarray(spec.ANIMAL_PRODUCT)[a_kind]
    ub_units = VAL.fires_between(xp, day, a_first, a_int, day + 1, O.LAST_SHED_DAY)
    ub_fert = xp.maximum(O.LAST_SHED_DAY - day, 0)
    ub_feeds = xp.maximum(O.LAST_SHED_DAY - day, 0) // 2
    acquire_ok = (ub_units * view.price[a_prod] + ub_fert * view.price[spec.I_FERT]
                  - a_cost - ub_feeds * view.price[spec.I_WHEAT]) > 0
```

In the walk loop replace

```python
        c_anim = xp.minimum(xp.maximum(a_want - a_have, 0),
                            (money // a_cost).astype(i32))
```

with

```python
        c_anim = xp.where(acquire_ok,
                          xp.minimum(xp.maximum(a_want - a_have, 0), (money // a_cost).astype(i32)),
                          0).astype(i32)
```

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_animal_acquisition_bound.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass. Existing purchase tests run on day 0 with every price at 25, where a goose bounds at 25×25 + 28×25 − 300 − 14×25 = 675 > 0.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_animal_acquisition_bound.py
git commit -m "Reject animal purchases whose optimistic remaining value is non-positive"
```

---

### Task 5: Value-ranked feed rationing (§0.6)

**Files:**
- Modify: `src/kagg3/core/plan.py` — a `_rank_by` helper, `a_idx` in the survival section, the `feed_rank`/`want_feed` lines in the clamp section
- Test: `tests/test_feed_rationing.py`

**Interfaces:**
- Consumes: `valuation.animal_value`, `feed_want`, `wheat_avail`.
- Produces: `plan._rank_by(xp, mask, value) -> int[100]` (exclusive rank of each masked tile by descending `value`, ties to the lower index); `a_idx = xp.clip(occ, 0, spec.N_ANIMALS - 1)` defined right after `free_struct` in the survival section (Task 6 reuses it); `feed_value` (int[100]).

**Background (§0.6).** When feed wheat runs short, victims are chosen by replacement value — an animal's remaining sellable production capped at its cost — with the serpentine position as the final tiebreak, instead of serpentine position alone. (Fertilizer rationing becomes value-ranked by construction in Task 7.)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_feed_rationing.py`:

```python
"""When feed wheat runs short, the animals worth most are fed first
(PLANNER_V3_1 section 0.6): remaining sellable production capped at the
animal's cost, serpentine position as the final tiebreak.
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


def _view(animals, wheat, day=5):
    """`animals`: list of (serpentine position, animal index); all hungry,
    placed on day 0; `wheat` in the shed and no money to buy more."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    for pos, a in animals:
        kind[pos] = spec.ANIMAL_STRUCT[a]
        occ[pos] = a
        t_cons[pos] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _feed_turns(view, **macro):
    unit_op = P.build_day(np, view, _macro(**macro))[0]
    return [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_FEED)]


def test_the_costlier_animal_is_fed_when_one_wheat_is_left():
    # goose at position 0 (value capped at its 300 cost), sheep at position 50
    # (capped at 500). One unit, one wheat: only the sheep gets a FEED task.
    # Position 50 is tile (9, 5): 6 moves from the spawn at (4, 4), after the
    # wheat pickup at turn 2 -- FEED lands on turn 9. The goose at (0, 0)
    # would have been 8 moves away (turn 11).
    assert _feed_turns(_view([(0, 0), (50, 2)], wheat=1)) == [O.ROUTE_BASE + 1 + 6]


def test_ties_fall_to_the_lower_position():
    # two identical geese: the one at position 3 -- tile (3, 0), 5 moves --
    # is fed; position 7 is tile (7, 0), 7 moves away
    assert _feed_turns(_view([(7, 0), (3, 0)], wheat=1)) == [O.ROUTE_BASE + 1 + 5]


def test_rank_by_orders_by_value_then_index():
    mask = np.zeros(10, bool)
    mask[[1, 4, 6, 8]] = True
    value = np.array([0, 5, 0, 0, 9, 0, 5, 0, 1, 0], np.int32)
    rank = P._rank_by(np, mask, value)
    assert rank[4] == 0 and rank[1] == 1 and rank[6] == 2 and rank[8] == 3


def test_rank_by_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(2)
    for _ in range(20):
        mask = rng.random(100) < 0.5
        value = rng.integers(0, 4, size=100).astype(np.int32)
        a = P._rank_by(np, mask, value)
        b = np.asarray(P._rank_by(jnp, jnp.asarray(mask), jnp.asarray(value)))
        assert a[mask].tolist() == b[mask].tolist()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_feed_rationing.py -q`
Expected: FAIL — `AttributeError: module 'kagg3.core.plan' has no attribute '_rank_by'`; the sheep test feeds the goose.

- [ ] **Step 3: Rank by value**

Add to `plan.py` next to `_rank`:

```python
def _rank_by(xp, mask, value):
    """Exclusive rank of each `mask` entry by descending `value` among the
    masked entries, exact ties to the lower index (serpentine position).
    Pairwise, like `task_order`, so both backends agree on every tie."""
    both = mask[None, :] & mask[:, None]
    v = value.astype(xp.int32)
    idx = xp.arange(mask.shape[0], dtype=xp.int32)
    ahead = both & ((v[None, :] > v[:, None])
                    | ((v[None, :] == v[:, None]) & (idx[None, :] < idx[:, None])))
    return xp.sum(ahead.astype(xp.int32), axis=1)
```

In `build_day`'s survival section, directly after `free_struct = is_struct & (occ < 0)`, add:

```python
    a_idx = xp.clip(occ, 0, spec.N_ANIMALS - 1)
```

In the clamp section replace

```python
    feed_rank = _rank(xp, feed_want)
    want_feed = feed_want & (feed_rank < wheat_avail)
```

with

```python
    # Feed rationing by replacement value [EXACT-OPT, 0.6]: when wheat runs
    # short, the animals worth most -- remaining sellable production, capped
    # at what a replacement costs -- are fed first; serpentine position only
    # breaks exact ties.
    feed_value = xp.minimum(
        VAL.animal_value(xp, view.price, view.t_day, view.t_yield, view.t_favail, a_idx, day),
        xp.asarray(spec.ANIMAL_COST)[a_idx])
    feed_rank = _rank_by(xp, feed_want, feed_value)
    want_feed = feed_want & (feed_rank < wheat_avail)
```

- [ ] **Step 4: Run the tests and the full suite**

Run: `python -m pytest tests/test_feed_rationing.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass.
Run: `ruff check src tests`.

- [ ] **Step 5: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_feed_rationing.py
git commit -m "Ration feed wheat by the animals' remaining value, not their position"
```

---

### Task 6: Feed cadence, the CARE rule, and the day-28 survival law (§0.11, §0.4)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `DayView` (+`t_bank`), the survival section of `build_day` (`must_water`, `must_feed`, `feed_want`), the `want_care` line, the `Macro` docstring
- Modify: `src/kagg3/sim/rollout.py::day_view` (+`t_bank`), `src/kagg3/agent/parse.py::parse_view` (+`t_bank`)
- Modify: `tests/test_day29_endgame.py::test_day_28_is_not_terminal` (it asserts survival waterings on day 28, which this task's law removes)
- Test: `tests/test_feed_care_cadence.py`

**Interfaces:**
- Consumes: `valuation.fires_on`, `valuation.next_fire_after`, `a_idx` (Task 5), `want_feed`, `O.LAST_SHED_DAY`.
- Produces: `DayView.t_bank` (int[100], pending CARE bonus, default zeros); inside `build_day`: `survival_pays` (bool scalar), `an_first`/`an_int`/`an_held`/`an_prod` (per-tile animal tables), `fires_tonight`, `bank_feed`, `h_next`, `bank_carry`. `macro.feed_daily` and `macro.care_on` are no longer read anywhere in `plan.py`.

**Background.**
- *Feed cadence.* Production fires whether or not the animal is fed; feeding buys survival (every other day) and, on a fire day, the payout of a pending CARE bank. So: feed when hungry (`t_cons >= 1`) or when a fire lands tonight and `t_bank > 0`. `feed_daily` is deleted as a decision.
- *CARE (§0.11, complete conditions).* The bank increments only when cared **and** fed the same day (`want_care ⊆ want_feed`, kept); it pays at the first fire whose eod is after today's (`next_fire_after`), only if the animal is fed that day — which the cadence rule now guarantees whenever the bank is non-zero; the payout is `min(max_held, yield + 1 + bank)`, and the planner harvests an animal whenever it holds units, so the headroom test is `bank_carry + 2 <= max_held`, where `bank_carry` is `t_bank` on a quiet night and **0 on a fire night** — the eod consumes (fed) or wipes (unfed) the standing bank before today's care increments it (`eod.py`: fire → `bank = 0` → `bank += 1`); the marginal unit must clear the fire-day feed's wheat (labour is not priced in coins until §1.6). No CARE whose payout lands past `LAST_SHED_DAY`. `care_on` is deleted as a decision. §6.5: pre-maturity cares stay legal — the bank pays at the first fire — and are bounded by the same headroom test.
- *Day-28 survival law (§0.4).* Surviving into day `d+1` is worth something only if day `d+1`'s production can still sell, i.e. `d < LAST_SHED_DAY`. On day 28: no survival WATER (in-window waterings that raise a same-day harvest stay), no survival FEED, and the feed want leaves the budget walk (`feed_need` is then 0). Terminal day 29 is already fully suppressed by Phase 0.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_feed_care_cadence.py`:

```python
"""Feeding is survival plus cashing a CARE bank on a fire day; CARE is emitted
only when its payout is reachable, fed, under the cap and worth the wheat
(PLANNER_V3_1 section 0.11). Survival work stops on the last shed day
(section 0.4): nothing that lives into day 29 can still sell.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "src")

import numpy as np
from test_budget_order import _macro

from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(day, animals=(), plants=(), wheat=10, price=None):
    """`animals`: (position, kind, placed_day, t_cons, t_bank).
    `plants`: (position, crop, planted_day, t_cons)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_cons, t_bank = z.copy(), z.copy(), z.copy()
    for pos, a, placed, cons, bank in animals:
        kind[pos] = spec.ANIMAL_STRUCT[a]
        occ[pos] = a
        t_day[pos], t_cons[pos], t_bank[pos] = placed, cons, bank
    for pos, c, planted, cons in plants:
        kind[pos] = spec.KIND_PLANT
        occ[pos] = c
        t_day[pos], t_cons[pos] = planted, cons
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1),
        price=BASE.copy() if price is None else price, t_bank=t_bank)


def _ops(view, **macro):
    unit_op = P.build_day(np, view, _macro(**macro))[0]
    return {op: int((unit_op == op).sum()) for op in (O.OP_FEED, O.OP_CARE, O.OP_WATER)}


GOOSE_FED = (0, 0, 0, 0, 0)          # position 0, goose placed day 0, fed yesterday, no bank


def test_no_survival_work_on_the_last_shed_day():
    view = _farm(28, animals=[(0, 0, 0, 1, 0)], plants=[(1, spec.I_TOMATO, 0, 1)], wheat=0)
    ops = _ops(view)
    assert ops[O.OP_FEED] == 0 and ops[O.OP_WATER] == 0
    op, qty = P.build_day(np, view, _macro())[3], P.build_day(np, view, _macro())[5]
    assert int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_PRODUCT].sum()) == 0   # no feed wheat bought


def test_survival_work_still_runs_on_day_27():
    ops = _ops(_farm(27, animals=[(0, 0, 0, 1, 0)], plants=[(1, spec.I_TOMATO, 0, 1)]))
    assert ops[O.OP_FEED] == 1 and ops[O.OP_WATER] == 1


def test_a_pending_bank_is_fed_on_its_fire_day():
    # goose fires every night; fed yesterday, so not hungry -- fed only because a bank is pending
    assert _ops(_farm(10, animals=[(0, 0, 0, 0, 1)]))[O.OP_FEED] == 1
    assert _ops(_farm(10, animals=[(0, 0, 0, 0, 0)]))[O.OP_FEED] == 0


def test_feed_daily_gene_no_longer_forces_a_feed():
    assert _ops(_farm(10, animals=[GOOSE_FED]), feed_daily=np.int32(1))[O.OP_FEED] == 0


def test_care_is_emitted_when_it_pays():
    # hungry goose on day 10: fed, egg 50 > wheat 25, payout day 12, bank 0 -> CARE
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 1


def test_care_on_gene_no_longer_gates_it():
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)]), care_on=np.int32(0))[O.OP_CARE] == 1


def test_no_care_when_the_payout_is_past_the_horizon():
    # day 27: the care would pay on day 29
    assert _ops(_farm(27, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 0


def test_no_care_when_the_egg_is_worth_less_than_the_wheat():
    price = BASE.copy()
    price[spec.I_EGG] = 20
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 1
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)], price=price))[O.OP_CARE] == 0


def test_no_care_without_headroom_under_max_held():
    # cow placed day 0 seen on day 10 (fires on harvest days 8, 10, 12: none
    # tonight, so the bank carries): holds 6, bank 5 + this care + the base
    # unit would exceed it; bank 4 fits exactly
    assert _ops(_farm(10, animals=[(0, 1, 0, 1, 5)]))[O.OP_CARE] == 0
    assert _ops(_farm(10, animals=[(0, 1, 0, 1, 4)]))[O.OP_CARE] == 1


def test_a_fire_tonight_clears_the_bank_before_the_care_counts():
    # goose placed day 0, cared every day since: bank 3 on day 3, fires tonight.
    # The eod consumes that bank before today's care banks toward eod 4, so the
    # care still pays +1 and headroom is judged against 0, not 3.
    assert _ops(_farm(3, animals=[(0, 0, 0, 1, 3)]))[O.OP_CARE] == 1


def test_care_only_with_a_feed():
    # not hungry, no bank: no feed today, so no care either
    assert _ops(_farm(10, animals=[GOOSE_FED]))[O.OP_CARE] == 0


def test_pre_maturity_care_is_allowed_within_headroom():
    # cow placed day 8, day 9: first fire day 16 <= 28, bank 0 -> CARE
    assert _ops(_farm(9, animals=[(0, 1, 8, 1, 0)]))[O.OP_CARE] == 1


def test_parse_view_reads_the_pending_bank():
    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    tiles[0][0] = {"kind": "COOP", "animal": "GOOSE", "placed_day": 2, "fed_today": False,
                   "consecutive_unfed": 1, "yield_units": 0, "cared_today": False,
                   "fertilizer_available": True, "pending_care_bonus": 2}
    obs = {"day": 4,
           "farms": [{"tiles": tiles, "money": 100, "unlocked_quadrants": ["NW"], "hands": []}],
           "private": {"shed": {}, "seeds": {}},
           "market": {"prices": {n: 7 for n in spec.PRODUCTS},
                      "inventory": {n: spec.MARKET_I0 for n in spec.PRODUCTS}},
           "town": {"unlocked_shops": []}}
    v = parse.parse_view(obs, 0)
    k = int(np.flatnonzero(P.SERP == 0)[0])         # serpentine position of tile (0, 0)
    assert int(v.t_bank[k]) == 2


def test_sim_day_view_carries_the_bank():
    import jax.numpy as jnp
    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of
    st = initial_state(jnp)
    st = st._replace(t_bank=st.t_bank.at[0, 0].set(3))
    tables = build_tables(jnp)
    v = rollout.day_view(st, 0, jnp.int32(0), prices_of(jnp, tables, st.mkt_inv))
    assert int(np.asarray(v.t_bank).sum()) == 3
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_feed_care_cadence.py -q`
Expected: FAIL — `TypeError: DayView.__new__() got an unexpected keyword argument 't_bank'`.

- [ ] **Step 3: Plumb `t_bank`**

In `plan.py::DayView` append after `shops`:

```python
    # Pending CARE bonus per animal tile (engine `pending_care_bonus`); zero
    # for plants. Defaulted so hand-built views stay valid.
    t_bank: object = np.zeros(spec.N_TILES, np.int32)     # int[100]
```

In `rollout.py::day_view` add `t_bank=st.t_bank[p][g],` to the `DayView(...)` call.

In `parse.py::parse_view`: declare `t_bank = np.zeros(n, np.int32)` with the other tile arrays; in the animal branch add `t_bank[k] = t.get("pending_care_bonus", 0)`; pass `t_bank=t_bank` in the returned `DayView`. The test's `obs["market"]`/`obs["town"]` keys (`"inventory"`, `"unlocked_shops"`) must match what Phase 0's `parse_market`/`parse_town` read — check them against `parse.py` as landed and adjust the fixture, not the parser.

- [ ] **Step 4: Rewrite the cadence and the CARE rule**

In `build_day`'s survival section replace

```python
    must_water = view.t_cons >= 1
```

with

```python
    # Survival pays only if what survives can still sell [LAW, 0.4]: on
    # LAST_SHED_DAY nothing that lives into tomorrow is worth a turn or a
    # wheat, so survival waterings and feeds stop and the feed want leaves
    # the budget walk. In-window waterings that raise a same-day harvest stay.
    survival_pays = day < O.LAST_SHED_DAY
    must_water = (view.t_cons >= 1) & survival_pays
```

and replace

```python
    # Production fires whether or not the animal was fed, so feeding buys only
    # survival and the CARE bonus. Feed every other day unless told otherwise.
    must_feed = view.t_cons >= 1
    feed_want = has_animal & (view.t_water == 0) & (must_feed | (macro.feed_daily == 1))
```

with

```python
    # Production fires whether or not the animal was fed, so feeding buys
    # survival and, on a fire day, the payout of a pending CARE bank
    # (0.11: the bank is consumed only on a fed production day). Feed when
    # hungry, and on a monetizable fire day when a bank is waiting.
    an_first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a_idx]
    an_int = xp.asarray(spec.ANIMAL_INTERVAL)[a_idx]
    an_held = xp.asarray(spec.ANIMAL_MAX_HELD)[a_idx]
    an_prod = xp.asarray(spec.ANIMAL_PRODUCT)[a_idx]
    fires_tonight = has_animal & VAL.fires_on(xp, view.t_day, an_first, an_int, day + 1) & survival_pays
    must_feed = (view.t_cons >= 1) & survival_pays
    bank_feed = fires_tonight & (view.t_bank > 0)
    feed_want = has_animal & (view.t_water == 0) & (must_feed | bank_feed)
```

(`a_idx` is defined just above by Task 5; if it is missing, add `a_idx = xp.clip(occ, 0, spec.N_ANIMALS - 1)` after `free_struct`.)

In the clamp section replace

```python
    want_care = want_feed & (view.t_cared == 0) & (macro.care_on == 1)
```

with

```python
    # CARE [0.11]: banks +1 only when cared and fed today; pays on the first
    # fire after today's eod, if fed that day (the cadence above feeds every
    # fire day with a bank waiting); worth min(max_held, yield + 1 + bank),
    # and the animal is harvested whenever it holds units, so the headroom
    # test is bank_carry + 2 <= max_held -- where bank_carry is the bank that
    # will still be standing when today's care is added: on a fire night the
    # eod consumes (fed) or wipes (unfed) the current bank *before* the care
    # increments it (eod.py: fire -> bank = 0 -> bank += 1), so it is 0 then.
    # The unit must clear the fire-day wheat; labour is not priced in coins
    # until section 1.6.
    h_next = VAL.next_fire_after(xp, view.t_day, an_first, an_int, day)
    bank_carry = xp.where(VAL.fires_on(xp, view.t_day, an_first, an_int, day + 1), 0, view.t_bank)
    care_headroom = bank_carry + 2 <= an_held
    care_pays = view.price[an_prod] > view.price[spec.I_WHEAT]
    want_care = (want_feed & (view.t_cared == 0) & (h_next <= O.LAST_SHED_DAY)
                 & care_headroom & care_pays)
```

In the `Macro` docstring mark both fields: `feed_daily: object    # int     0/1  decoded, ignored by the planner since V3.1 0.11` and the same for `care_on`.

Phase 0's `tests/test_day29_endgame.py::test_day_28_is_not_terminal` waters five thirsty tomatoes on day 28 — exactly the survival work this law stops. Rename it `test_day_27_is_not_terminal`, build its view with `_view(27)`, and keep every assertion (five WATERs, three hires, no SELL); day 27 is the last day survival still pays.

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_feed_care_cadence.py -q` — Expected: PASS (14 tests).
Run: `python -m pytest -q` — Expected: all pass. `test_gates.py::test_no_tile_write_collisions` and the sim-equivalence gate exercise random boards with the new cadence; a failure there is a bug in this task.
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/plan.py src/kagg3/sim/rollout.py src/kagg3/agent/parse.py tests/test_feed_care_cadence.py
git commit -m "Feed for survival or a pending CARE bank; CARE only when its payout is reachable and paid"
```

---

### Task 7: Value-ranked fertilizer and fertilized fire-day watering (§0.11, §0.4 day-28 FERTILIZE)

**Files:**
- Modify: `src/kagg3/core/plan.py` — the `fert_short` line in the budget walk, the `n_fert_eff`/`want_fert` lines in the clamp section, a new `want_water` extension after them, the `Macro` docstring
- Modify: `tests/test_fert_source.py` (delete the two planner tests that drive `n_fertilize`/`fert_buy`; keep the `brain.decide` tests), `tests/test_fert_reserved.py` (fixture)
- Test: `tests/test_fertilizer_value.py`

**Interfaces:**
- Consumes: `valuation.fert_marginal_value`, `valuation.crop_fires_on`, `harvest_age` (Phase 0), `_rank_by` (Task 5), `fert_avail`, `fert_cum` (Task 1).
- Produces: inside `build_day`: `fert_val` (int[100]), `fert_cand` (bool[100]), `n_fert_want`, `fert_short` (now value-derived), `n_fert_eff = min(n_fert_want, fert_avail)`, `want_fert`, `crop_fire`, and `want_water` extended by fertilized fire-day waterings. `macro.n_fertilize` and `macro.fert_buy` are no longer read.

**Background (§0.11).** Today `want_fert` takes the first `n_fertilize` watered tiles in sweep order and buys the shortfall iff `fert_buy` — so it fertilizes melons (worth 0 under daily watering) ahead of tomatoes (up to +3 per application), the mechanistic reason "raising the fertilize gene measured strictly worse". Rule: value every tile's application with `fert_marginal_value`; fertilize (and buy the shortfall, curve-priced by Task 1) iff that value exceeds the fertilizer's opportunity price — today's fertilizer quote, the price a shed unit would sell for or a bought one costs at the margin. Rank candidates by value, serpentine tiebreak; never re-fertilize while an application is active (`t_fert >= day`): waiting for it to lapse covers strictly more days. Ongoing crops must be watered at the eod of a fertilized fire to collect the +1 — production fires regardless of watering, only the fertilized case pays — so a fertilized ongoing crop firing tonight is watered even when not thirsty. Day 28's FERTILIZE→WATER→HARVEST chain falls out of the same valuation (≤ +1, 0 without headroom).

- [ ] **Step 1: Write the failing tests**

Create `tests/test_fertilizer_value.py`:

```python
"""Fertilizer goes where one application is worth most (PLANNER_V3_1 section
0.11), never to a crop that saturates anyway, and only when the gain beats
the fertilizer's own price; the shortfall is bought on the same test. A
fertilized ongoing crop is watered on its fire night to collect the bonus.
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


def _farm(day, plants, fert=0, money=1000, price=None):
    """`plants`: (position, crop, planted_day, t_cons, t_fert)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_cons, t_fert, t_yield = z.copy(), z.copy(), z - 1, z.copy()
    for pos, c, planted, cons, fertilized_until in plants:
        kind[pos] = spec.KIND_PLANT
        occ[pos] = c
        t_day[pos], t_cons[pos], t_fert[pos] = planted, cons, fertilized_until
        t_yield[pos] = 0 if spec.CROP_ONGOING[c] else 1        # one-time crops are born with 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=t_fert, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1),
        price=BASE.copy() if price is None else price)


def _plan(view, **macro):
    return P.build_day(np, view, _macro(**macro))


def _fert_bought(plan):
    op, arg, qty = plan[3:6]
    return sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_FERT)


TOMATO_D8 = (5, spec.I_TOMATO, 0, 1, -1)      # planted day 0, thirsty (mandatory tier); day 8: three fires in the window
MELON_D6 = (0, spec.I_MELON, 0, 0, -1)        # in its watering window, not thirsty, saturates without fertilizer


def test_one_unit_goes_to_the_tomato_not_the_melon_ahead_of_it():
    unit_op, unit_a = _plan(_farm(8, [MELON_D6, TOMATO_D8], fert=1))[:2]
    fert_turns = np.flatnonzero(unit_op[0] == O.OP_FERTILIZE)
    assert len(fert_turns) == 1
    # the thirsty tomato is mandatory-tier, so it is visited first: position 5
    # = tile (5, 0), 1 + 4 = 5 moves from the spawn at (4, 4) after the pickup
    # at turn 2 -> FERTILIZE on turn 8. The melon (bonus watering only) comes
    # after; had it taken the unit, the tomato's turn would carry no FERTILIZE.
    assert int(fert_turns[0]) == O.ROUTE_BASE + 1 + 5


def test_nothing_is_fertilized_when_the_gain_is_below_the_fertilizer_price():
    price = BASE.copy()
    price[spec.I_FERT] = 200                     # 3 x 60 = 180 < 200
    unit_op = _plan(_farm(8, [TOMATO_D8], fert=1, price=price))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 0


def test_the_shortfall_is_bought_on_the_same_test():
    assert _fert_bought(_plan(_farm(8, [TOMATO_D8]))) == 1
    price = BASE.copy()
    price[spec.I_FERT] = 200
    assert _fert_bought(_plan(_farm(8, [TOMATO_D8], price=price))) == 0


def test_old_genes_are_ignored():
    unit_op = _plan(_farm(8, [MELON_D6], fert=3), n_fertilize=np.int32(3), fert_buy=np.int32(1))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 0
    assert _fert_bought(_plan(_farm(8, [MELON_D6]), n_fertilize=np.int32(3), fert_buy=np.int32(1))) == 0


def test_an_active_application_is_not_renewed():
    unit_op = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 1, 9)], fert=1))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 0


def test_fertilized_ongoing_crop_is_watered_on_its_fire_night():
    # not thirsty (t_cons 0), fertilized through day 9, fires tonight (day 8 -> harvest day 9)
    watered = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, 9)]))[0]
    assert int((watered == O.OP_WATER).sum()) == 1
    # no fertilizer and no money to buy any: the fire night is not watered
    unfertilized = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, -1)], money=0))[0]
    assert int((unfertilized == O.OP_WATER).sum()) == 0
    # freshly fertilized today counts too: FERTILIZE then WATER on the same tile
    ops = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, -1)], fert=1))[0][0]
    ops = [int(o) for o in ops if int(o) not in (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST, O.OP_PICKUP)]
    assert ops == [O.OP_FERTILIZE, O.OP_WATER]


def test_wheat_is_fertilized_only_when_its_price_carries_it():
    wheat_d2 = (5, spec.I_WHEAT, 0, 1, -1)       # +2 units
    assert int((_plan(_farm(2, [wheat_d2], fert=1))[0] == O.OP_FERTILIZE).sum()) == 0      # 2 x 25 < 100
    price = BASE.copy()
    price[spec.I_WHEAT] = 60                                                                  # 2 x 60 > 100
    assert int((_plan(_farm(2, [wheat_d2], fert=1, price=price))[0] == O.OP_FERTILIZE).sum()) == 1


def test_day_28_same_day_chain_is_value_conditional():
    late_wheat = (5, spec.I_WHEAT, 25, 0, -1)    # harvest age 3 = today; +1 unit at most
    price = BASE.copy()
    price[spec.I_FERT] = 20
    assert int((_plan(_farm(28, [late_wheat], fert=1, price=price))[0] == O.OP_FERTILIZE).sum()) == 1
    assert int((_plan(_farm(28, [late_wheat], fert=1))[0] == O.OP_FERTILIZE).sum()) == 0     # 25 < 100


def test_ranking_and_rationing_agree_across_backends():
    import jax
    import jax.numpy as jnp
    view = _farm(8, [MELON_D6, TOMATO_D8, (9, spec.I_TOMATO, 1, 1, -1)], fert=1)
    macro = _macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_fertilizer_value.py -q`
Expected: FAIL — no FERTILIZE is emitted (the `n_fertilize` gene is 0 in `_macro()`), and the melon test fertilizes the melon once `n_fertilize` is set.

- [ ] **Step 3: Value the applications and rank them**

In `build_day`'s budget walk replace

```python
    fert_short = xp.where(macro.fert_buy > 0,
                          xp.maximum(macro.n_fertilize - view.shed[spec.I_FERT], 0),
                          0).astype(i32)
```

(including the comment block above it about the measured 50k → 32k) with:

```python
    # Value-ranked fertilizer targeting [0.11]: one application is worth its
    # exact clipped marginal units at today's price -- 0 for a crop that
    # saturates anyway (melon watered daily), up to +3 for a tomato with three
    # fires in the window. Fertilize, and buy the shortfall, iff that beats the
    # unit's own price (what a shed unit sells for, what a bought one costs).
    # Never renew an active application: waiting for it to lapse covers
    # strictly more days. Simplification: the threshold is the flat hour-0
    # quote although the purchase itself walks the curve (0.10); the gap is
    # one unit's rise per bought unit and the shortfall is bounded by the
    # candidates, so it is labelled, not modelled.
    fert_val = VAL.fert_marginal_value(xp, view.price, view.t_day, view.t_yield, crop, day, harvest_age)
    fert_cand = is_plant & (view.t_fert < day) & (fert_val > view.price[spec.I_FERT])
    n_fert_want = xp.sum(fert_cand.astype(i32))
    fert_short = xp.maximum(n_fert_want - view.shed[spec.I_FERT], 0).astype(i32)
```

In the clamp section replace

```python
    n_fert_eff = xp.minimum(macro.n_fertilize, fert_avail)
    fert_rank = _rank(xp, want_water)
    want_fert = want_water & (fert_rank < n_fert_eff) & (view.t_fert < day)
```

with

```python
    n_fert_eff = xp.minimum(n_fert_want, fert_avail)
    fert_rank = _rank_by(xp, fert_cand, fert_val)
    want_fert = fert_cand & (fert_rank < n_fert_eff)

    # An ongoing crop fires whether or not it is watered; only the fertilized
    # case pays (+2 instead of +1), so a fertilized crop firing tonight is
    # watered even when it is not thirsty. FERTILIZE precedes WATER in the
    # chain, so today's application counts.
    crop_fire = (is_plant & (c_ongoing == 1) & survival_pays
                 & VAL.crop_fires_on(xp, view.t_day, crop, day + 1))
    want_water = want_water | (crop_fire & (view.t_water == 0) & ((view.t_fert >= day) | want_fert))
```

(`survival_pays` is Task 6's `day < O.LAST_SHED_DAY`; a fire at eod 28 is not monetizable.)

In the `Macro` docstring mark `n_fertilize` and `fert_buy` as `decoded, ignored by the planner since V3.1 0.11`.

- [ ] **Step 4: Retire the gene-driven tests**

In `tests/test_fert_source.py` delete `test_fertilize_above_stock_buys_nothing_when_fert_buy_is_off` and `test_fertilize_above_stock_buys_the_shortfall_when_fert_buy_is_on` (and the `_view`/`_fert_bought` helpers if nothing else uses them, plus any import — `P`, `O` — that becomes unused, or `ruff` fails F401); keep the `brain.decide`/`policy` tests (`test_fert_buy_decodes_from_aux_0`, `test_pre_g5_thetas_have_fert_buy_off`, `test_g5_block_is_the_last_and_zero_padding_is_inert`) — the gene still decodes. Rewrite the module docstring's first paragraph to: "`fert_buy` and `n_fertilize` still decode from theta (checkpoints must keep decoding identically) but the planner no longer reads them: since PLANNER_V3_1 0.11 fertilizer targets and purchases are value-ranked (see test_fertilizer_value.py)."

In `tests/test_fert_reserved.py` the fixture drove `want_fert` through `n_fertilize`. Replace `_view` and the three tests so the applications are value-driven:

```python
def _view(fert_in_shed, n_tomato=3, day=8):
    """`n_tomato` tomatoes planted on day 0 -- on day 8 each has three fires
    in a fertilizer window, worth 3 x 25 > the fertilizer's 25 -- and
    `fert_in_shed` fertilizer, no money to buy more."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:n_tomato] = spec.KIND_PLANT
    occ = z - 1
    occ[:n_tomato] = spec.I_TOMATO
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert_in_shed
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def test_planned_fertilizer_is_held_back_from_the_sale():
    view = _view(fert_in_shed=5)
    unit_op = P.build_day(np, view, _macro(sell_qty=_sell_all_fert()))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 3
    assert _fert_sold(view, _macro(sell_qty=_sell_all_fert())) == 2


def test_nothing_reserved_when_nothing_is_worth_fertilizing():
    # day 12: the tomatoes' last fire (day 11) is behind them
    assert _fert_sold(_view(fert_in_shed=5, day=12), _macro(sell_qty=_sell_all_fert())) == 5


def test_reservation_is_capped_by_what_the_day_can_spread():
    # 8 candidates, 5 in the shed, no money: n_fert_eff is 5, so none sells
    assert _fert_sold(_view(fert_in_shed=5, n_tomato=8), _macro(sell_qty=_sell_all_fert())) == 0
```

(`_fert_sold` and `_sell_all_fert` stay as they are.)

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_fertilizer_value.py tests/test_fert_source.py tests/test_fert_reserved.py -q` — Expected: PASS.
Run: `python -m pytest -q` — Expected: all pass (`test_day29_endgame.py` passes `n_fertilize`/`fert_buy` in its greedy macro; they are now inert, which the test does not depend on).
Run: `ruff check src tests`.

- [ ] **Step 6: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_fertilizer_value.py tests/test_fert_source.py tests/test_fert_reserved.py
git commit -m "Target fertilizer by exact marginal value and water fertilized crops on fire nights"
```

---

### Task 8: Per-unit pickups charged inside the block (§0.12)

**Files:**
- Modify: `src/kagg3/core/plan.py` — `_routes` (whole function), the route/pickup section of `build_day`, the module docstring's intra-day layout
- Test: `tests/test_unit_pickups.py`

**Interfaces:**
- Consumes: `_routes`'s current inputs; `blk`, `covered` (Phase 0's forced sale reads both — unchanged shapes).
- Produces: `_routes(...) -> (route_op, route_a, route_q, blk, covered, n_pick)` with `n_pick` int[MU] = pickup turns each unit spends; every unit's route budget is the constant `TPD - O.ROUTE_BASE` (22); `need_feed`/`need_fert`/`need_place`/`n_pickup` are removed from `build_day`.

**Background (§0.12).** Today the route budget is `22 − (number of pickup kinds the whole day needs)` for *every* unit, and every unit idles through the global pickup turns whether or not its block consumes anything. Verified change set: charge the pickup turns inside each block — with `D(s, e) = Σ_i [cpick[i, e] > cpick[i, s−1]]` the block `[s, e]` costs `L(e) = base + cum[e] − cum[s] + D(s, e)`, monotone in `e`, and the block ends at the largest `e` with `L(e) <= 22`, one `_count_le` pass (`load` is non-decreasing in `e` because `cum` and `D` are, and for `e < s` it is `base + cum[e] − cum[s] <= base` with `D = 0`, so the array is sorted). The one-tile feasibility check includes `D(s, s)`. Each unit picks up only what its own block consumes, one kind per turn from `ROUTE_BASE`, before its first move (PICKUP is silently dropped off the shed-access tiles). Caveats accepted by the spec: shed-contention ties shift from unit index to turn order when stock is short (totals stay covered by the walk's clamps), and a block boundary that splits one pickup kind across two units makes both pay a turn.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_unit_pickups.py`:

```python
"""A unit pays only for the pickups its own block consumes, inside its own
22-turn budget (PLANNER_V3_1 section 0.12); a unit whose block needs no
pickup starts walking at ROUTE_BASE instead of idling through the other
units' pickup turns.
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


def _farm(day, tiles, shed, money=1000):
    """`tiles`: dict position -> dict(kind=, occ=, t_day=, t_cons=, t_yield=, t_fert=)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_day, t_cons, t_yield, t_fert = z - 1, z.copy(), z.copy(), z.copy(), z - 1
    for pos, t in tiles.items():
        kind[pos] = t["kind"]
        occ[pos] = t.get("occ", -1)
        t_day[pos] = t.get("t_day", 0)
        t_cons[pos] = t.get("t_cons", 0)
        t_yield[pos] = t.get("t_yield", 0)
        t_fert[pos] = t.get("t_fert", -1)
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=t_fert, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _ripe_tomatoes(positions):
    return {p: dict(kind=spec.KIND_PLANT, occ=spec.I_TOMATO, t_yield=1) for p in positions}


def _feed_then_harvests():
    """A hungry goose at position 0 (mandatory, so the farmer's block starts
    there and needs a wheat pickup) and thirty ripe tomatoes behind it; two
    units."""
    tiles = {0: dict(kind=spec.KIND_COOP, occ=0, t_cons=1)}
    tiles.update(_ripe_tomatoes(range(1, 31)))
    return _farm(13, tiles, {spec.I_WHEAT: 1})


def test_only_the_unit_that_picks_up_pays_the_turn():
    unit_op = P.build_day(np, _feed_then_harvests(), _macro(n_hire=np.int32(1)))[0]
    assert int(unit_op[0, O.ROUTE_BASE]) == O.OP_PICKUP
    assert int(unit_op[0, O.ROUTE_BASE + 1]) in MOVES
    assert int(unit_op[1, O.ROUTE_BASE]) in MOVES              # no idle pickup turn
    assert int((unit_op[1] == O.OP_PICKUP).sum()) == 0


def test_three_kinds_are_picked_up_on_consecutive_turns_by_the_block_that_needs_them():
    # farmer's block: hungry goose (wheat), tomato worth fertilizing (fertilizer),
    # free coop with a goose in the shed (place); second unit: ripe tomatoes only
    tiles = {0: dict(kind=spec.KIND_COOP, occ=0, t_cons=1),
             1: dict(kind=spec.KIND_PLANT, occ=spec.I_TOMATO, t_day=5, t_cons=1),   # day 13: fires 14..16 in window
             2: dict(kind=spec.KIND_COOP)}
    tiles.update(_ripe_tomatoes(range(3, 33)))
    view = _farm(13, tiles, {spec.I_WHEAT: 1, spec.I_FERT: 1, spec.I_GOOSE: 1})
    unit_op, unit_a = P.build_day(np, view, _macro(n_hire=np.int32(1), animal_count=np.int32(1)))[:2]
    b = O.ROUTE_BASE
    assert [int(o) for o in unit_op[0, b:b + 3]] == [O.OP_PICKUP] * 3
    assert [int(a) for a in unit_a[0, b:b + 3]] == [spec.I_WHEAT, spec.I_FERT, spec.I_GOOSE]
    assert int(unit_op[0, b + 3]) in MOVES
    assert int(unit_op[1, b]) in MOVES
    assert int((unit_op[1] == O.OP_PICKUP).sum()) == 0


def test_every_unit_stays_inside_twenty_two_turns():
    for view, macro in ((_feed_then_harvests(), _macro(n_hire=np.int32(1))),
                        (_feed_then_harvests(), _macro(n_hire=np.int32(4)))):
        unit_op = P.build_day(np, view, macro)[0]
        for u in range(spec.MAX_UNITS):
            busy = int((unit_op[u, O.ROUTE_BASE:] != O.OP_PASS).sum())
            assert busy <= spec.TURNS_PER_DAY - O.ROUTE_BASE
            assert int((unit_op[u, :O.ROUTE_BASE] != O.OP_PASS).sum()) == 0


def test_pickups_precede_every_move():
    unit_op = P.build_day(np, _feed_then_harvests(), _macro(n_hire=np.int32(1)))[0]
    for u in range(2):
        row = [int(o) for o in unit_op[u]]
        if O.OP_PICKUP in row:
            last_pick = max(i for i, o in enumerate(row) if o == O.OP_PICKUP)
            first_move = min(i for i, o in enumerate(row) if o in MOVES)
            assert last_pick < first_move


def test_per_unit_pickups_agree_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _feed_then_harvests(), _macro(n_hire=np.int32(3))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_unit_pickups.py -q`
Expected: FAIL — `unit_op[1, ROUTE_BASE]` is `OP_PASS` (the second unit idles through the farmer's pickup turn).

- [ ] **Step 3: Rewrite `_routes`**

Replace the whole `_routes` function in `plan.py` with:

```python
def _routes(xp, chain_op, chain_a, chain_q, n_ops, score, tier, pick_masks, n_units, budget):
    """Split the task sweep across units and expand it into per-turn ops.

    Tiles are worked by descending (tier, score); whatever the turn budget
    cannot reach is left undone, so that order is what decides what gets
    dropped. A unit's pickup turns are charged inside its block [LAW, 0.12]:
    with D(s, e) the number of pickup kinds a block [s, e] consumes, the block
    costs L(e) = base + cum[e] - cum[s] + D(s, e) turns, monotone in e, and
    ends at the largest e with L(e) <= budget.

    Returns (route_op, route_a, route_q, blk, covered, n_pick): per-unit route
    arrays [MU, TPD], pickup quantities per kind [3, MU], the reached-tile mask
    in view space, and each unit's pickup turns [MU].
    """
    i32 = xp.int32
    idx = xp.arange(N_T, dtype=i32)

    task = n_ops > 0
    order = task_order(xp, task, score, tier)
    n_tasks = xp.sum(task.astype(i32))

    tx = xp.asarray(SERP_X)[order]
    ty = xp.asarray(SERP_Y)[order]
    tn = n_ops[order]
    cop, ca, cq = chain_op[order], chain_a[order], chain_q[order]
    cpick = xp.cumsum(pick_masks[:, order].astype(i32), axis=1)      # [3, 100]

    move = xp.concatenate([xp.zeros(1, i32),
                           xp.abs(tx[1:] - tx[:-1]) + xp.abs(ty[1:] - ty[:-1])]).astype(i32)
    seg = move + tn
    cum = xp.cumsum(seg)
    prev_x = xp.concatenate([tx[:1], tx[:-1]])
    prev_y = xp.concatenate([ty[:1], ty[:-1]])

    route_op, route_a, route_q, blk, n_pick = [], [], [], [], []
    start = xp.asarray(0, i32)
    for u in range(MU):
        sx, sy = xp.asarray(SPAWN_X[u], i32), xp.asarray(SPAWN_Y[u], i32)
        bud = xp.where(u < n_units, budget, xp.asarray(0, i32)).astype(i32)

        s = xp.minimum(start, N_T - 1)
        lo = xp.maximum(s - 1, 0)
        prev = xp.where(s > 0, cpick[:, lo], 0)                              # [3] owed before this block
        d_pick = xp.sum((cpick > prev[:, None]).astype(i32), axis=0)          # [100] D(s, e)
        base_move = xp.abs(sx - tx[s]) + xp.abs(sy - ty[s])
        base = base_move + tn[s]
        load = base + cum - cum[s] + d_pick                                   # L(e), sorted in e
        jmax = _count_le(xp, load, bud) - 1
        active = (start < n_tasks) & (load[s] <= bud) & (bud > 0)
        end = xp.where(active, xp.minimum(jmax, n_tasks - 1), s - 1)
        e = xp.maximum(end, 0)
        p_u = xp.where(active, d_pick[e], 0).astype(i32)

        cu = base + cum - cum[s]
        cu_prev = cu - xp.where(idx == s, base, seg)
        cu_masked = xp.where(idx < s, xp.asarray(-1, i32),
                             xp.where(idx <= end, cu, _BIG)).astype(i32)

        r = xp.arange(TPD, dtype=i32)
        j = xp.clip(_count_le(xp, cu_masked, r), 0, N_T - 1)
        within = r - cu_prev[j]
        mv = xp.where(j == s, base_move, move[j])
        px = xp.where(j == s, sx, prev_x[j])
        py = xp.where(j == s, sy, prev_y[j])
        dx, dy = tx[j] - px, ty[j] - py
        step_op = xp.where(within < xp.abs(dx),
                           xp.where(dx > 0, O.OP_EAST, O.OP_WEST),
                           xp.where(dy > 0, O.OP_SOUTH, O.OP_NORTH)).astype(i32)
        k = xp.clip(within - mv, 0, CHAIN_MAX - 1)

        working = active & (r < xp.where(active, cu[e], 0)) & (r < bud - p_u)
        is_step = within < mv
        route_op.append(xp.where(working, xp.where(is_step, step_op, cop[j, k]), O.OP_PASS).astype(i32))
        route_a.append(xp.where(working & ~is_step, ca[j, k], 0).astype(i32))
        route_q.append(xp.where(working & ~is_step, cq[j, k], 0).astype(i32))

        blk.append(xp.where(active, cpick[:, e] - prev, 0))
        n_pick.append(p_u)
        start = end + 1

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
            xp.stack(blk, axis=1), covered, xp.stack(n_pick))       # blk -> [3, MU]
```

- [ ] **Step 4: Rewrite the route and pickup section of `build_day`**

Replace the block that begins `# ---- route ---` (the `need_feed` … `n_units` lines) with:

```python
    # ---- route ------------------------------------------------------------
    # Every unit has the same route budget; the pickup turns its own block
    # consumes are charged inside that block by `_routes` [0.12], so a unit
    # whose block needs no pickup starts walking at ROUTE_BASE.
    budget = xp.asarray(TPD - O.ROUTE_BASE, i32)
    n_units = xp.asarray(1, i32) + n_hire
```

change the `_routes` call to unpack six values:

```python
    route_op, route_a, route_q, blk, covered, n_pick = _routes(
        xp, chain_op, chain_a, chain_q, n_ops, score, tier,
        xp.stack([want_feed, want_fert, m_place]), n_units, budget)
```

replace the route placement lines

```python
    t = xp.arange(TPD, dtype=i32)[None, :]
    r = t - (O.ROUTE_BASE + n_pickup)
    on_route = (r >= 0) & (r < budget)
```

with

```python
    t = xp.arange(TPD, dtype=i32)[None, :]
    r = t - (O.ROUTE_BASE + n_pick[:, None])
    on_route = (r >= 0) & (r < budget - n_pick[:, None])
```

and replace the `# ---- morning PICKUPs ---` block (through the end of its `for i in range(3)` loop) with:

```python
    # ---- morning PICKUPs --------------------------------------------------
    # Each unit picks up what its own block consumes, one kind per turn from
    # ROUTE_BASE, before it leaves its shed-access spawn tile (PICKUP is
    # silently dropped anywhere else).
    pk_active = (blk > 0).astype(i32)                                     # [3, MU]
    pk_turn = xp.cumsum(pk_active, axis=0) - pk_active + O.ROUTE_BASE     # [3, MU]
    pk_item = xp.stack([xp.asarray(spec.I_WHEAT, i32),
                        xp.asarray(spec.I_FERT, i32),
                        xp.asarray(spec.I_GOOSE, i32) + a_kind])
    for i in range(3):
        hit = (pk_active[i][:, None] > 0) & (t == pk_turn[i][:, None])
        unit_op = xp.where(hit, O.OP_PICKUP, unit_op)
        unit_a = xp.where(hit, pk_item[i], unit_a)
        unit_q = xp.where(hit, blk[i][:, None], unit_q)
```

Update the module docstring's layout table:

```
    turn 2 .. 2+P_u-1                                       unit u: PICKUP, one per kind its block consumes
    turn 2+P_u .. 23                                        unit u: walk its route

P_u is 0..3 per unit and is charged inside that unit's 22-turn block, so a
unit with nothing to pick up walks from turn 2.
```

- [ ] **Step 5: Run the tests and the full suite**

Run: `python -m pytest tests/test_unit_pickups.py -q` — Expected: PASS (5 tests).
Run: `python -m pytest -q` — Expected: all pass. `test_gates.py::test_no_tile_write_collisions` (block disjointness over random boards), `test_sim_equivalence.py` and `test_trained_equivalence.py` (the sim's `apply_units` resolves PICKUP on any turn, in unit order) are the gates that matter here; `test_overflow_forced_sale.py` still reads `blk` and `covered`.
Run: `ruff check src tests`.

- [ ] **Step 6: Measure compile time and throughput**

Run `python scripts/bench_sim.py` (read `--help`; use its defaults) on this commit and, in a worktree, on the Task-7 commit (`git worktree add /tmp/claude-0/kagg3-t7 HEAD~1`); record both numbers in the commit message; remove the worktree. A delta beyond 5% is reported, not optimised.

- [ ] **Step 7: Commit**

```bash
git add src/kagg3/core/plan.py tests/test_unit_pickups.py
git commit -m "Charge each unit's pickup turns inside its own block"
```

---

### Task 9: Verification and the frozen-theta measurement (§7)

**Files:**
- No source changes expected. Appends a "Phase-1 result" section to this plan.

**Interfaces:**
- Consumes: `artifacts/theta.npy` (the ES mean), `scripts/eval_vs_baselines.py` (seeds fixed by `default_rng(20260821)`; prints `mean coins` per opponent; runs the real engine through the numpy submission path).

**Predictions, stated before the run (§7 requires it; §8 requires a sign per item wherever theta may have learned compensations).**

| Task | Item | Predicted sign on frozen `theta.npy` | Why |
|---|---|---|---|
| 1 | 0.10 curve pricing | ≥ 0, small | the row no longer over-commits; the engine dropped the last BUY slot before |
| 3 | 0.8 animal_count | **≤ 0** | theta learned under "zero still restocks"; it may now under-acquire — the retraining case Phase 2 makes |
| 4 | 0.2 acquisition bound | ≥ 0 | late animals that could not pay back are no longer bought |
| 5 | 0.6 feed rationing | ≥ 0, small | only bites when wheat is short |
| 6 | 0.11 cadence + CARE, 0.4 day-28 | unknown, stated as ≥ 0 | `feed_daily` days become every-other-day feeds (less wheat, no extra escapes); CARE now pays or is not emitted; day-28 survival work stops |
| 7 | 0.11 fertilizer | ≥ 0 | the melon-before-tomato ranking is gone; theta had the gene near zero, so the value rule mostly *adds* paying applications |
| 8 | 0.12 pickups | ≥ 0 | up to 3 turns per unit per day returned to the route |

Net: absolute mean coins vs `starter` non-negative unless Task 3's regression dominates. `n = 16` seed pairs is a smoke test, not an architectural decision (§7).

- [ ] **Step 1: Full suite, lint, packaging**

Run: `python -m pytest -q` — Expected: all pass.
Run: `ruff check src tests` — Expected: clean.
Run: `python scripts/package_submission.py` then `python -m pytest tests/test_submission_runs.py -q` — Expected: PASS (the new `valuation.py` imports only `spec` and `ops`).

- [ ] **Step 2: Baseline numbers from the Phase-0 tree**

```bash
BASE=$(git log --format=%h --grep="Record the Phase-0" -n 1)
git worktree add /tmp/claude-0/kagg3-phase0 "$BASE"
cd /tmp/claude-0/kagg3-phase0
python scripts/eval_vs_baselines.py --theta /mnt/e/_work/kaggriculture3/artifacts/theta.npy --games 16 --opponents starter random
cd /mnt/e/_work/kaggriculture3
```

Record the `mean coins` and `mean margin` lines verbatim.

- [ ] **Step 3: Phase-1 numbers**

```bash
python scripts/eval_vs_baselines.py --theta artifacts/theta.npy --games 16 --opponents starter random
```

- [ ] **Step 4: Bisect if the delta is negative**

Each task is one commit. If the Phase-1 total vs `starter` is below the Phase-0 baseline by more than the run-to-run noise, run the same command on the commit after Task 3 and the commit after Task 7 (`git worktree add` each) to attribute the loss, and record which item carries it. **Do not tune**: a law that regresses a frozen theta is either the retraining case (Task 3, predicted) or a finding about the spec.

- [ ] **Step 5: Write the result into this plan and commit**

Append `## Phase-1 result (frozen theta.npy, n = 16 seed pairs × 2 seats)` with both tables, the delta, one line per prediction marked *held* / *did not hold*, and the bisection if it ran.

```bash
git worktree remove /tmp/claude-0/kagg3-phase0
git add docs/superpowers/plans/2026-08-24-planner-v31-phase1.md
git commit -m "Record the Phase-1 frozen-theta measurement"
```

---

## Self-review notes (written with the plan)

- **Spec coverage, Phase 1 (§8):** §0.10 → Task 1 (the `DayView`/table half landed in Phase 0); §0.6 → Task 5 (feed; fertilizer rationing is value-ranked by construction in Task 7); §0.8 → Task 3; §0.2 → Task 4; §0.11 → Tasks 6 (3-day window is already respected by `t_fert < day`; CARE conditions; `feed_daily`/`care_on` deleted) and 7 (value-ranked fertilizer; fertilized fire-day watering; `n_fertilize`/`fert_buy` deleted); §0.12 → Task 8; §0.4 day-28 rules → Task 6 (no survival FEED/WATER, feed want leaves the walk, no CARE past the horizon) and Task 7 (FERTILIZE value-conditional). §7/§8 measurement with per-item signs → Task 9.
- **Deliberate simplifications, labelled in code:** valuation prices are today's hour-0 quotes; CARE's labour cost is not priced in coins (§1.6, Phase 2); the acquisition bound assumes every fire is harvested; `animal_value` and the ongoing-crop branch of `fert_marginal_value` ignore `max_held`/`CROP_MAX_YIELD` accumulation (the planner harvests whenever units are held); the fertilizer threshold is the flat hour-0 quote while the purchase walks the curve.
- **Review 2026-08-24 (folded in):** the CARE headroom test reads the bank that *carries* into tonight's eod — 0 on a fire night, since the fire consumes or wipes the standing bank before today's care increments it — not the raw `t_bank`; the headroom test fixture is a cow on a quiet night, plus a goose-day-3 case pinning the fire-night behaviour.
- **Type consistency:** `_routes` returns 6 values from Task 8 on (5 before); `_rank_by(xp, mask, value)` (Task 5) is what Task 7 calls; `a_idx` is defined in Task 5 and read in Task 6; `survival_pays` is defined in Task 6 and read in Task 7; `fert_cum`/`wheat_cum` (Task 1) are read by the walk only; `DayView.t_bank` (Task 6) is the last field; `valuation` signatures match between Task 2 and Tasks 4–7.

---

## Phase-1 result (frozen theta.npy, n = 16 seed pairs × 2 seats)

Measured 2026-08-25 on branch `fitness-shaping`, HEAD `7afbb13` (Tasks 1–8 as nine commits `a10c762`…`c20d810` — Task 2 landed as two, `7fb32cc` plus docstring fix `9fa287e` — plus the packaging fix below), against the Phase-0 tree `6284e01`. Same frozen `artifacts/theta.npy` (the ES mean, not `champion.npy`), same seeds (`default_rng(20260821)`), same engine.

`python -m pytest -q` — 215 collected, 215 passed, exit 0 (8m32s). `ruff check src tests` — `Found 25 errors`, left unfixed: the same set as the plan's base `128ac83`, except one `RUF059` in the new `tests/test_fertilizer_value.py` that displaced a retired `C408`.

**Packaging fix (`7afbb13`).** `test_archive_is_self_contained` failed at `c20d810`: the new `core/valuation.py` was missing from `scripts/package_submission.py`'s explicit `INCLUDE`, so the archived planner raised `ImportError`, kaggle_environments swallowed it, and the farm finished on its starting 3,000 coins. With the entry added, `package_submission.py` then `pytest tests/test_submission_runs.py -q` → 11 passed.

`scripts/eval_vs_baselines.py --theta <theta> --games 16 --opponents starter random`, verbatim:

```
Phase 0, 6284e01 (worktree at that commit, this repo's theta.npy):
  vs starter   win 100.0%   mean coins     45442   mean margin    +41808   (n=32)
  vs random    win 100.0%   mean coins     40597   mean margin    +40594   (n=32)
Phase 1, 7afbb13:
  vs starter   win 100.0%   mean coins     46975   mean margin    +43333   (n=32)
  vs random    win 100.0%   mean coins     41513   mean margin    +41502   (n=32)
```

| opponent | Phase 0 `6284e01` (win / coins / margin) | Phase 1 `7afbb13` (win / coins / margin) | delta coins | delta margin |
|---|---|---|---|---|
| `starter` | 100.0 % / 45 442 / +41 808 | 100.0 % / 46 975 / +43 333 | **+1 533** (+3.4 %) | +1 525 |
| `random`  | 100.0 % / 40 597 / +40 594 | 100.0 % / 41 513 / +41 502 | +916 (noise, below) | +908 |

**Only the `starter` column is a measurement.** That row reproduced to the coin across two Phase-1 runs (an earlier run at `c20d810` printed the same `46975 / +43333`); the `random` row did not — `c20d810` printed `47109 / +47091`, and three repeat `--games 4` runs on this tree printed 44 526 / 42 329 / 39 979 mean coins. The built-in `random` agent is not reproducible under a fixed env seed, so its delta carries run-to-run variance larger than the effect being measured.

**Bisection not run** (Step 4): the Phase-1 total vs `starter` is *above* the Phase-0 baseline, so the negative-delta trigger never fired. Nothing was tuned.

### Predictions, scored

The run measures Tasks 1–8 jointly on one frozen theta, so §8's per-item signs are **not separable** — it can attribute the +1,533 neither to nor against any single item. What it does test is the net prediction, *"absolute mean coins vs `starter` non-negative unless Task 3's regression dominates"*: **held** (+1,533, +3.4 %).

- Task 1 (§0.10 curve pricing, ≥ 0) — *not separable*; not contradicted.
- Task 3 (§0.8 `animal_count`, ≤ 0) — *not separable*; the positive aggregate does not show whether it cost coins, so Phase 2's retraining case is neither confirmed nor retired.
- Task 4 (§0.2 acquisition bound, ≥ 0) — *not separable*; not contradicted.
- Task 5 (§0.6 feed rationing, ≥ 0) — *not separable*; not contradicted.
- Task 6 (§0.11 cadence + CARE, §0.4 day-28, ≥ 0) — *not separable*; not contradicted.
- Task 7 (§0.11 value-ranked fertilizer, ≥ 0) — *not separable*; not contradicted.
- Task 8 (§0.12 pickups, ≥ 0) — *not separable*; not contradicted.

**Task 8 sim bench** (`scripts/bench_sim.py`, from `c20d810`'s commit body; this tree vs `d05bd20`, two runs each): B=1024 compile 61.9/61.7 s vs 59.8/60.4 s, run 0.68/0.66 s vs 0.66/0.66 s (~1,527 vs ~1,557 eps/s) — +2.8 % compile, −1.9 % throughput, inside run-to-run noise. B=64/256 show ~+6 % run time at 0.3 s absolute, i.e. dispatch-bound, not sim-bound.

**Post-review re-measure (after the bank-feed rationing fix, commit `8b1e0b2`).** The final whole-branch review found that a bank-only feed was ranked by the animal's replacement value, so a wheat shortage could starve a hungry animal to cash a care bank; the fix values a bank-only feed at its payout alone. Re-running the same command on the fixed tree, verbatim:

```
  vs starter   win 100.0%   mean coins     47083   mean margin    +43434   (n=32)
  vs random    win 100.0%   mean coins     45964   mean margin    +45952   (n=32)
```

Only the `starter` column is reproducible (see above).
