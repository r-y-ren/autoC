# Land value + mixed herd — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax. Dispatch each task to a fresh **Opus** subagent; the implementer sees only its own task plus this header, so every task repeats what it needs.

**Goal:** kill the two measured planner defects that the 2026-08-25 autopsy against `kagg2` isolated —

1. **Land is a blind gene and a pure cost.** `brain.decide` decides it with `buy_land = head[1] + aux[1]*afford > 0` (`src/kagg3/core/brain.py:271-273`); `plan._derive` deducts the price from the purse *before* `budget.grant` and gives the quadrant no value at all (`src/kagg3/core/plan.py:759-764`); and the 25 new tiles are invisible to the day that bought them because `free_slot` reads the hour-0 `view.kind` (`plan.py:678`) and `brain.n_free_slots` reads the hour-0 `obs.kind` (`brain.py:87-104`). 22 unit-turns per purchase are wasted (`docs/PLANNER_V3_1.md:513-514`) and the recorded land drain is **−77.5k on a free quadrant** (`docs/PLANNER_V3_1.md:582-584`).
2. **One animal kind per day.** `animal_kind = argmax(grow[EGG], grow[MILK], grow[WOOL])` (`brain.py:286-287`). At z = 0 the three `grow` scores are equal and `argmax` returns index 0, so an untrained policy buys **geese and nothing else** — for the whole season, on every board.

`kagg2` — the evaluation opponent — buys quadrant 2 on day 6 and quadrant 3 on day 11 (3,000 coins total), then runs **10 cows + 4 sheep + 34 strawberry + melon on 75 tiles with 12 hands for 170k**. Every one of those four facts is something this planner structurally cannot do today.

**Architecture:** land stops being a gene and becomes a priced, lumpy purchase compared two ways inside the day's own value model; the learned logit survives only as a **coin bias scaled to the quadrant price**, zero at z = 0. The quadrant's tiles become free slots on the day of purchase, on both the decision side (`brain.n_free_slots`) and the derivation side (`plan._derive`). `Macro.animal_kind` (scalar 0..2) is replaced by `Macro.animal_want` (int[3]); the single animal candidate list in `core/budget.py` becomes three, each priced on its own product's sales-window curve and its own fib-priced feed, so one day can buy 3 cows and 2 sheep. The intra-day schedule changes in exactly one place: `BUY_LAND` leaves the turn-1 BUY row (which the third animal slot needs) for the free tenth slot of turn 2, where lot-1 revenue funds it.

**Tech Stack:** Python 3, numpy, JAX (CPU for tests, GPU for training), `kaggle_environments` (pinned engine), pytest, ruff.

**Spec:** `docs/PLANNER_V3_1.md` §0.2, §0.3 (`:128-140`), §1.1, §1.3 (`:355-374`), §2 (`:427-445`), §5 M1/M2 (`:513-520`), §6 (`:531-555`), §7 (`:582-588`). Read §0.3, §1.3, §5 and §7 before starting a task.

**Relationship to the Phase-3 plan.** `docs/superpowers/plans/2026-08-24-planner-v31-phase3.md` Task 4 (M1 prospective land) and Task 5 (M2 land at turn 2) specify the two mechanical halves of item 1 and are **not yet implemented** (`brain.n_free_slots` still takes no `land` argument; `plan.SERP_QUAD` does not exist; `_market` still emits `MO_BUY_LAND` in the turn-1 group at `plan.py:1387`). Tasks 1 and 3 below **are** those two tasks, restated with the extra constraints this plan's valuation and mixed herd impose; land them from here and mark the Phase-3 entries done. Tasks 2, 4, 5 are new. Nothing here depends on Phase-3 Tasks 1–3 (DROP), 6, 7 or 8.

**Prerequisites:** Phases 0–2 landed. Another agent is concurrently adding a **structural hire-bill reserve** to `src/kagg3/core/plan.py`. Task 2 and Task 5 must not be started until that lands; Task 5 exists specifically to reconcile the two. Rebase before every task and re-read `_derive`'s purse block (`plan.py:681-700, 751-764`) rather than trusting the line numbers quoted here.

---

## Global constraints

Every task's requirements implicitly include this section.

- Planner code is array-agnostic (`xp` = numpy or `jax.numpy`), **shape-static**, int32, no data-dependent control flow; every bounded loop goes through `core/loop.py::repeat` exactly as `budget.grant`'s bisections do (`src/kagg3/core/budget.py:112, 133, 161`). `core/` never imports `jax`. This is what makes the numpy submission and the JAX trainer literally the same code path — **no branch in this plan may be expressed as a Python `if` on a traced value.**
- Every tie breaks the same way on both backends: `xp.argmax` takes the first maximum (lower index wins), `_rank_by` and `task_order` compare pairwise (`plan.py:303-312, 390-432`). New per-kind orderings inherit that: **goose < cow < sheep**, matching the candidate-list index order.
- Every coin value is clipped to `spec.COIN_CAP - 1` (`= budget.VALUE_CAP`, `spec.py:204`, `budget.py:52`) *before* it multiplies `grow_mult` (which reaches 4×) — the `< 2**20` rule of §2.
- Reductions pin `dtype=xp.int32`: `np.cumsum`/`np.sum` widen int32 to int64, `jnp` does not (`budget.py:33-35`).
- Both seats must present an identical market-slot layout on every market turn (`sim/market.py::assert_no_cross`, `:260-271`). The BUY row's slot layout stays a constant, never a decision (`plan.py:1389-1400`).
- `spec.MAX_MARKET_ORDERS = 10` (`spec.py:196`) and the engine truncates at `maxMarketOrdersPerTurn = 10` (engine `:551, :560`). **No turn may ever carry more than ten live orders.** This is the hard constraint that sequences Task 3 before Task 4.
- The simulator is a transcription of the pinned engine. No task here adds a market turn; the sim resolves the market only on hours 0–2 (full path) and 10/18 (sell-only) (`sim/rollout.py:148-157`).
- Throughput: run `.venv/bin/python scripts/bench_sim.py` before and after every task and put both numbers in the commit message. **A cumulative slowdown over 15% stops the plan** and the offending task is reformulated.
- Interpreter: every `python` means `.venv/bin/python`. Tests: header `os.environ.setdefault("JAX_PLATFORMS", "cpu")`, `sys.path.insert(0, "src")`; shared fixtures are `tests/test_budget_order.py::_view/_macro` (there is no `conftest.py`; 22 test files import `_macro` from that module). `ruff check src tests scripts` clean before every commit. One commit per task on branch `fitness-shaping`, one-line sentence-case imperative message. Never commit `artifacts/`.

## Engine and code facts these tasks stand on

Read from the pinned engine and the current source; every task may rely on these without re-deriving them.

- **Land unlock is synchronous and its outcome is known at hour 0.** `_do_buy_land` (engine `:712-725`) takes `n_extra = len(unlocked_quadrants) - 1`, charges `LAND_PRICES[n_extra]` (1000 / 2000 / 4000), appends `LAND_ORDER[n_extra]` (NE, SW, SE) and rewrites every `"LOCKED"` tile of that quadrant to `None` **inside the market phase of the order's own turn**. The sim is an exact transcription (`sim/market.py:112-124`). Both `spec.LAND_PRICES` and `spec.LAND_ORDER` are static (`spec.py:210-212`) and `view.nquad` is in the `DayView` (`plan.py:272`), so the identity, the price and the success of the purchase are all computable at hour 0 — `plan.py:763` already asserts exactly that success condition.
- **Units act before the market in every turn** (`sim/rollout.py:145-157`, engine turn order). A quadrant unlocked at turn *t* therefore accepts tile ops from turn *t+1*. With `BUY_LAND` on turn 1 and units PASSing on turns 0–1 (`plan.py:23-27`), all 22 route turns (`ROUTE_BASE = 2` .. 23, `ops.py:80-88`) are usable. With `BUY_LAND` moved to turn 2, the first route turn is lost and 21 remain.
- **Movement onto LOCKED tiles is legal; tile ops on them silently no-op** (engine `:328-330`, `sim/units.py:83`). A prospective op that the purchase failed to enable is therefore a wasted turn, not a crash — which is why the land grant must be *certain* before prospective tasks are queued.
- **`BUY_LAND` and `HIRE` are atomic orders** resolved once per slot index, in player order, before that index's SELL/BUY lockstep (engine `:571-581`; `sim/market.py:166-172`). They never couple across seats and never touch market inventory, so they are safe in any slot and safe opposite any other seat's order.
- **The turn-1 BUY row holds nine of ten slots today**: `B_WHEAT`(1) + `B_FERT`(1) + `B_SEEDS`(5) + `B_ANIMAL`(1) + `B_LAND`(1) (`plan.py:131-136, 1378-1412`). Three animal slots make eleven. `render.py:35` and `sim/rollout.py::compact_orders` (`:93-109`) drop `MO_NONE` slots, so only *live* orders reach the engine — but a day that genuinely wants all eleven would lose the eleventh, and `plan.py:684-690` records exactly that failure mode having already cost a land purchase once.
- **`BUY_ANIMAL` is one item per slot** (`sim/market.py:188-194`, engine `_commit_unit`). A mixed herd needs one slot per kind; there is no quantity-vector form.
- **Animal table** (`spec.py:61-71`): goose 300 coins / COOP / first fire age 4 / interval 1 / max_held 4 / EGG; cow 400 / PASTURE / 5 / 2 / 6 / MILK; sheep 500 / PASTURE / 6 / 3 / 6 / WOOL. Two structure kinds, three animals — **cow and sheep compete for the same pastures.**
- **Market steepness** (`spec.py:97-99`): EGG `T = 332`, MILK `T = 122`, WOOL `T = 105`. Milk and wool curves are ~3× steeper than egg's, so a single-kind herd saturates its own curve where a mixed one does not. This is the economic case for the mixed herd on top of the `argmax` bug.
- **The candidate values do not depend on the tile count.** `_candidates` (`plan.py:470-547`) builds `values`/`costs` from `_stream_rev` over `PJ.inv_at_day(...) + _pipeline_units(...)` and engine-curve quotes; only `wants` (`w_seed`, `w_anim`, `plan.py:525, 542`) reads the free-tile count. **This is the fact that makes Task 2 cheap**: the marginal value of 25 more tiles is a re-read of the *same* arrays at higher ranks, not a re-pricing.
- **`PJ.K = spec.SHED_CAPACITY + 1 = 101`** (`projector.py:28`) is every candidate list's length, and `grant` clips `wants` to it (`budget.py:78`). Per-kind animal wants are bounded by the board's 100 tiles, so K never binds; the clip stays as the guard it is.

## File map

| File | Responsibility after this plan |
|---|---|
| `src/kagg3/core/brain.py` | `n_free_slots(xp, obs, land=None)`; `decide` predicts the grant before sizing development; `animal_kind` argmax → a `_largest_remainder` split into `animal_want[3]`; `buy_land` 0/1 → `land_bias` in coins |
| `src/kagg3/core/plan.py` | `SERP_QUAD`; prospective free slots; `_land_value`; the two-way land compare above the greedy; per-kind animal derivation, placement, pickups and BUY slots; `_market` emits `MO_BUY_LAND` at `(TURN_SELL, MO-1)` |
| `src/kagg3/core/budget.py` | `N_LISTS` 8 → 10, `L_ANIMAL` → `L_ANIMAL0` + three kinds, five `SHED_LISTS`; new `marginal_gain` next to `topup` |
| `src/kagg3/core/ops.py` | `MAX_PICKUPS` 3 → 5; the turn-1/turn-2 schedule comment corrected (§6.2 of the spec) |
| `src/kagg3/core/policy.py` | `DEAD_HEAD` drops index 2 (animal-mix sharpness reactivated) |
| tests | new `test_prospective_land.py`, `test_land_value.py`, `test_land_at_turn_two.py`, `test_mixed_herd.py`, `test_cash_reserve.py`; **17 existing files updated** (see Task 6) |

**Task order: 1 → 2 → 3 → 4 → 5 → 6.** Task 1 must precede Task 2 (valuing tiles the day cannot use is valuing zero). Task 3 must precede Task 4 (it frees the tenth BUY slot). Task 5 must follow the concurrent reserve work. Task 6 is the measurement and closes the plan.

---

### Task 1: M1 — a quadrant bought this morning is developed this afternoon

**Files:**
- Modify: `src/kagg3/core/brain.py` (`n_free_slots`, `decide`), `src/kagg3/core/plan.py` (`SERP_QUAD`, `_derive`)
- Test: `tests/test_prospective_land.py` (new)

**Interfaces:**
- Consumes: `view.nquad`, `spec.LAND_ORDER`, `spec.LAND_PRICES`, `spec.TILE_QUAD`, `plan.SERP`.
- Produces: `plan.SERP_QUAD = spec.TILE_QUAD[SERP].astype(np.int32)`; `brain.n_free_slots(xp, obs, land=None)`; `_derive` locals `next_quad`, `prospective` (bool[100]), and a `free_slot` that includes them.

**Background.** Two halves, and shipping either alone does nothing. The *decision* head must count the prospective tiles, because `n_dev = floor(dev_frac * n_free)` and `plant_total = n_dev - animal_count` (`brain.py:279-283`) are both capped by `n_free_slots`, which today sees only currently-owned tiles — so `plant_target` can never exceed them and nothing is ever planted on new land whatever the planner does. The *derivation* must use them, because `free_slot = is_empty | is_weed | harvest_one` (`plan.py:678`) reads the hour-0 `kind` where the new quadrant is still `KIND_LOCKED`.

The ordering constraint inside `_derive` is the only subtlety: `free_slot`/`n_free` are computed at `:678-679` and consumed by `a_want` at `:730`, but the land grant is decided at `:763`. The grant depends only on `macro`, `view.nquad` and the purse — **not** on `free_slot` — so hoisting it above `:678` is acyclic. Hoist it; do not try to make `free_slot` depend on a decision that depends on `free_slot`.

`brain`'s prediction of the grant is necessarily approximate (it does not know the hire bill, the reserve, or Task 2's valuation). Over-asking is already safe on the placement side — `plant_here` is masked by `free_slot` (`plan.py:855`) — but it is **not** safe on the purchase side: `w_seed = max(plant_target - view.seeds, 0)` (`plan.py:525`) would buy seeds for tiles that do not exist. The comment at `plan.py:519-524` argues no clip is needed *because* `brain` sizes against the same predicate; that argument dies here. Add the clip.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_prospective_land.py`. Take the four tests from `docs/superpowers/plans/2026-08-24-planner-v31-phase3.md` Task 4 Step 1 verbatim (`test_plantings_land_on_the_new_quadrant_the_same_day`, `test_builds_land_on_the_new_quadrant_too`, `test_nothing_prospective_when_the_purse_cannot_pay`, `test_the_decision_head_counts_the_prospective_tiles`, plus the cross-backend check) — they are already written against the interface above. Add two:

```python
def test_seed_purchases_are_clipped_to_the_tiles_that_will_exist():
    """A macro asking for 40 plantings on a board with 25 prospective tiles and
    no owned free tile buys at most 25 seeds, not 40."""

def test_the_prospective_mask_is_exactly_the_next_quadrant_in_land_order():
    """nquad=1 -> NE (LAND_ORDER[0]); nquad=2 -> SW; nquad=3 -> SE; nquad=4 -> nothing."""
```

- [ ] **Step 2: `brain.n_free_slots` counts the prospective quadrant**

Add a third parameter: `n_free_slots(xp, obs, land=None)`. When `land` is not None the count adds `xp.sum(((xp.asarray(spec.TILE_QUAD) == next_quad) & (obs.kind == spec.KIND_LOCKED)).astype(xp.int32)) * land`, with `next_quad = xp.asarray(spec.LAND_ORDER)[xp.clip(obs.nquad - 1, 0, 2)]`. Note `PolicyObs.kind` is in **raw tile order** (`sim/rollout.py:52`), so this uses `spec.TILE_QUAD` directly — not `SERP_QUAD`. Keep `land=None` returning today's answer bit-for-bit; `brain.features` (`brain.py:134`) keeps calling it that way so the *feature* vector is unchanged.

- [ ] **Step 3: `brain.decide` predicts the grant before sizing development**

Move the `land_cost` / `afford` / `buy_land` block (`brain.py:271-273`) **above** `n_free = n_free_slots(...)` (`brain.py:260`) and pass the prediction in:

```python
land_ok = ((buy_land > 0) & (obs.nquad < 4)
           & (obs.money.astype(i32) >= land_cost.astype(i32))).astype(i32)
n_free = n_free_slots(xp, obs, land=land_ok)
```

`dev_frac` (`brain.py:279`) then sizes on the enlarged count for free — including its `aux[2] * n_free / 25.0` term, which is what the "35 tiles idle all game" comment at `:277` was written for.

- [ ] **Step 4: `_derive` derives on the post-purchase view**

Add `SERP_QUAD = spec.TILE_QUAD[SERP].astype(np.int32)` beside `SERP_X`/`SERP_Y` (`plan.py:150-151`). In `_derive`, hoist the two land lines from `:763-764` to just above `free_slot` (`:678`), then:

```python
next_quad   = xp.asarray(spec.LAND_ORDER)[xp.clip(view.nquad - 1, 0, 2)]
prospective = (xp.asarray(SERP_QUAD) == next_quad) & (kind == spec.KIND_LOCKED) & (buy_land > 0)
free_slot   = is_empty | is_weed | harvest_one | prospective
```

Everything downstream — `n_free`, `a_want`, `slot_rank`, `build_here`, `plant_here` (`plan.py:679, 730, 845-857`) — then works the new tiles with no further change, and `_routes` reaches them because they are ordinary serpentine positions. **No route or schedule change: the tiles unlock at turn 1, units start at turn 2.**

- [ ] **Step 5: clip the seed want to the tiles that will exist**

In `_candidates` (`plan.py:525`), replace the unclipped want with a prefix clip against the planner's own post-decision capacity, using the same cumulative trick `plant_here` uses at `:854-856`:

```python
cap        = xp.maximum(n_free - n_build, 0)             # tiles left after the builds
want_raw   = xp.maximum(plant_target - view.seeds, 0)
before     = xp.cumsum(want_raw, dtype=i32) - want_raw
w_seed     = xp.clip(want_raw, 0, xp.maximum(cap - before, 0))
```

`n_free` and `n_build` must therefore be computed before `_candidates` is called; they already are (`plan.py:679, 849`) — reorder the call, do not recompute. Replace the now-false comment at `plan.py:519-524` with the reason the clip exists.

- [ ] **Step 6: verify**

`python -m pytest tests/test_prospective_land.py tests/test_free_land_urgency.py tests/test_archetypes.py tests/test_backend_agreement.py -q`, then the full suite. Record `scripts/bench_sim.py` before/after. Expected cost: one extra `[100]` compare and one cumsum — **under 1%**.

---

### Task 2: land valuation — a quadrant competes on coins, the logit is a bias

**Files:**
- Modify: `src/kagg3/core/budget.py` (`marginal_gain`), `src/kagg3/core/plan.py` (`_derive`), `src/kagg3/core/brain.py` (`land_bias` decode), `src/kagg3/core/policy.py` (docstring)
- Test: `tests/test_land_value.py` (new)

**Interfaces:**
- Consumes: `values`, `costs`, `wants` from `_candidates`; `PJ.K`; `budget.RATIO_SHIFT`, `budget.VALUE_CAP`; `plan.HIRE_BILLS`, `plan.EST_MOVES`.
- Produces: `budget.marginal_gain(xp, values, costs, wants, extra, rounds_cap, purse, lists) -> int` (net coins); `plan.LAND_TILES = spec.N_TILES // 4`, `plan.DEV_DAYS = 2`; `_derive` locals `land_value`, `land_bias`; `Macro.buy_land: int` (0/1) becomes `Macro.land_bias: int` (signed coins); `Prefix.buy_land` keeps its 0/1 meaning.

**Background — why a quadrant is worth far more than it costs, and why the model never saw it.** A quadrant is 25 tiles for 1,000 / 2,000 / 4,000 coins — 40 / 80 / 160 coins a tile. `tests/test_budget_order.py:85-94` already hand-computes what a tile earns on a blank day-0 board at the planner's own prices: one melon seed costs 80 and its six units fetch **1,611** coins; one goose costs 300 and nets **3,547** (25 eggs 1,172 + 28 fertilizer 2,725 − 14 feed wheat 350). Twenty-five melon tiles are ~38k gross against a 1,000-coin quadrant. **Land was never marginal; the model simply had no term for it** — `plan.py:759-764` deducts the price and books nothing, so the greedy that follows sees a smaller purse and no compensating asset, and `buy_land` could only ever look like a loss to the value model. That, not the price, is the shape of the −77.5k drain; the churn half of it (`buy → starve → escape → re-buy`) is already priced by §0.2, §0.8 and §1.4, all shipped.

**The formulation.** The candidates a quadrant admits are exactly the seed and animal ranks *beyond each list's pre-land want* — `values`/`costs` are identical either way (see the facts section), only `wants` moves. So:

```
land_value = Σ (value_k − cost_k) over the best-ratio candidates taken from
             ranks [want_pre[l], want_pre[l] + LAND_TILES) of the seed and
             animal lists, greedily against `purse − land_cost`,
             at most `n_eff` of them.
```

`value_k` is already the horizon-correct number: `v_seed` is `grow_mult × _stream_rev(price_table[c], inv_h[c], u_new[c], k)` where `u_new = VAL.new_plant_units(crop, day)` is the units a crop planted *today* yields by `LAST_SHED_DAY` and `inv_h` is `PJ.inv_at_day(mkt_inv, shops, first_p) + _pipeline_units(...)` — the sales-window inventory the §1.3 candidates already price against (`plan.py:499-517`). `v_anim` is §0.2's stream net of fib-priced feed (`plan.py:526-540`). Reusing them verbatim is what keeps land on the same yardstick as everything else it competes with, and gives the **derived last-useful-purchase-day for free**: `new_plant_units` returns 0 for a crop that cannot mature (melon after ~d18, wheat after d26) and `fires_between` empties for a late animal, so `land_value` collapses to zero on its own near the horizon — no day constant anywhere, exactly as `docs/PLANNER_V3_1.md:137-139` requires.

**The labour clamp** (`n_eff`). 25 tiles the day cannot reach are worth nothing today. A fresh tile's chain is PLANT+WATER or BUILD+PLACE — 2 ops (`plan.py:881-884`) — which the admit stage charges at `n_ops + EST_MOVES = 4` turns (`plan.py:114, 1100`). So:

```python
n_units     = _count_le(xp, xp.asarray(HIRE_BILLS), hire_bill) - 1 + 1   # 1 + h, from the bill
worked_pre  = xp.sum(is_plant.astype(i32)) + xp.sum(has_animal.astype(i32))
turns_free  = xp.maximum(n_units * (TPD - O.ROUTE_BASE - O.MAX_PICKUPS)
                         - worked_pre * (1 + EST_MOVES), 0)
n_eff       = xp.clip((turns_free // (2 + EST_MOVES)) * DEV_DAYS, 0, LAND_TILES)
```

`n_units` is recovered from `hire_bill` rather than passed in, because `HIRE_BILLS` is strictly increasing (`plan.py:241`) — no signature change, and pass A (bill 0) therefore values land at one unit, which under-counts and can only *refuse*, never over-buy. Note that on an early board `worked_pre` is small and even one unit clears 4–8 tiles, which at ~1,500 coins a melon tile still clears a 1,000-coin quadrant by an order of magnitude — the conservatism does not trap the day-6 purchase this plan is aimed at. Add the test that pins that.

**The bias.** `head[1]`/`aux[1]` are re-typed from a boolean to coins scaled by the quadrant's own price, so the transform is bounded and zero at z = 0:

```python
land_bias = _qfloor(xp, land_cost * xp.tanh(head[1] + aux[1] * afford)).astype(i32)
```

At z = 0 the bias is 0 and the planner buys land **iff it pays for itself** — the correct init posture, and the one §2's "the initial policy sells" assertion is the sell-side analogue of. Saturated positive the gene demands only `land_value > 0`; saturated negative it demands `land_value > 2 × land_cost`. It can never force a worthless quadrant nor refuse an arbitrarily valuable one. Keep `afford` and its `clip(-1, 4)` exactly as at `brain.py:272` — the clip's rationale (a raw ratio near 50 makes one sigma step a 2.5-logit swing) is unchanged.

**The decision.**

```python
buy_land = ((view.nquad < 4) & (purse >= land_cost)
            & (land_value + macro.land_bias > 0)).astype(i32)
```

`land_value` is already net of the price (the greedy runs on `purse − land_cost`), so comparing to 0 rather than to `land_cost` is deliberate — do not double-charge.

**The one labelled approximation, stated honestly [HEURISTIC].** The two-way compare of §1.3 is *grant* against *skip*; this computes the grant leg exactly and omits the skip leg's displacement term (what the last `land_cost` coins would otherwise have bought on the existing tiles). Computing it needs a second `budget.grant` — measured below as the reason it is omitted, not an oversight. Displacement is a multi-day question anyway (tomorrow's purse re-buys what today's land displaced), and §1.1's honesty rule assigns multi-day residue to the genes: the bias is scaled to `land_cost` precisely so a gene that has learned "land displaces too much early" can demand up to a 2× margin. Say so in the code comment, in those terms.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_land_value.py`:

```python
def test_a_quadrant_that_pays_for_itself_is_bought_at_zero_bias():
    """3,000 coins, day 6, 25 melon seeds' worth of value behind the wall:
    land_bias = 0 buys the quadrant."""

def test_a_quadrant_late_in_the_season_is_refused_at_zero_bias():
    """day 27: new_plant_units is 0 for every crop and fires_between is empty,
    so land_value is 0 and no bias of zero buys it. No day constant is read."""

def test_a_saturated_positive_bias_buys_land_worth_one_coin():
def test_a_saturated_negative_bias_refuses_land_worth_1_9x_its_price():
def test_land_value_is_zero_when_no_hand_can_reach_the_tiles():
    """A board whose owned tiles already exhaust the turn budget: n_eff == 0."""
def test_one_unit_still_clears_a_day_six_quadrant():
    """Pass A conservatism does not trap the purchase: hire_bill = 0 still buys."""
def test_land_bias_decodes_to_zero_at_theta_zero():
def test_land_value_agrees_across_backends():
```

- [ ] **Step 2: `budget.marginal_gain`**

Add next to `topup` (`budget.py:144-161`), sharing its tie rules verbatim:

```python
def marginal_gain(xp, values, costs, wants, extra, rounds_cap, purse, lists):
    """int: net coins (value less cost) of the best `rounds_cap` candidates
    from ranks [wants[l], wants[l] + extra) of the lists flagged in `lists`,
    taken best-ratio-first against `purse`.  Structurally `topup` with a
    shifted start and a bounded round count; `argmax` ties to the lower list,
    as there."""
```

Fixed `LAND_TILES = 25` rounds through `loop.repeat`; `rounds_cap` gates each round with `where`, never with a Python `if`. Carry `(n, left, gain)`; per round take `nxt = clip(wants + n, 0, PJ.K - 1)`, read `costs`/`values`/`ratio` with `take_along_axis`, mask with `(n < extra) & (r_next >= 0) & (c_next <= left) & (round < rounds_cap) & lists`, `argmax`, accumulate `gain += value - cost`. Clip `gain` to `[-VALUE_CAP, VALUE_CAP]`.

- [ ] **Step 3: `Macro.buy_land` → `Macro.land_bias`, decoded in `brain`**

Rename the field (`plan.py:194`) and update its comment to "signed coins the gene adds to the quadrant's computed value". Replace `brain.py:273` with the `tanh` decode above. `brain`'s prospective-tile prediction from Task 1 keeps a **boolean** notion of "land is a live candidate" — `land_ok = (land_bias > -land_cost) & (nquad < 4) & (money >= land_cost)`, i.e. "the gene has not vetoed it and it is affordable" — because `brain` cannot run the valuation. Task 1 Step 5's seed clip is what makes that approximation safe.

- [ ] **Step 4: wire it into `_derive`**

Order inside `_derive` is now a LAW and must be commented as one:
`hire_bill` (turn 0, already spent) → **reserve** (Task 5) → `land_cost` → the greedy's purse. Compute `values/costs/wants` *once*; call `marginal_gain` on the pre-land wants against `purse − land_cost`; decide `buy_land`; then recompute `w_seed`/`w_anim` on the post-land `n_free` (Task 1 already made `free_slot` depend on `buy_land`, so this is one re-evaluation of two small want vectors, not a re-pricing) and call `BUD.grant` once, as today.

- [ ] **Step 5: verify and measure**

`python -m pytest tests/test_land_value.py tests/test_budget_order.py tests/test_budget_greedy.py tests/test_hire_bill.py -q`, then the full suite. `scripts/bench_sim.py` before/after. **Budget: ≤ 3%.** `marginal_gain` is 25 rounds of a 10-wide argmax against `grant`'s 62 bisection reduces plus 101 top-up rounds, and it reuses `grant`'s arrays. If the measurement exceeds 3%, drop `DEV_DAYS` to 1 and re-measure before reformulating anything else. **A second `budget.grant` for the displacement term is out of budget: 3 grants per `_derive` × 2 passes is ~+18% on its own, over the 15% gate.** Record that number if you measure it.

---

### Task 3: M2 — `BUY_LAND` moves to turn 2, funded by lot-1 revenue

**Files:**
- Modify: `src/kagg3/core/plan.py` (`_derive`, `_market`, `_plan_and_stats`), `src/kagg3/core/ops.py` (schedule comment)
- Test: `tests/test_land_at_turn_two.py` (new)

**Interfaces:** exactly those of `docs/superpowers/plans/2026-08-24-planner-v31-phase3.md` Task 5 — `plan.LAND_REV_NUM, LAND_REV_DEN = 3, 4`; `_derive` locals `avail_prov`, `lots_prov`, `rev1`; the grant condition `money + rev1 >= land_cost` with `rev1` already discounted; `purse = money - max(land_cost - rev1, 0)`; `_market` emits `MO_BUY_LAND` at `(O.TURN_SELL, MO - 1)` and never at `TURN_BUY`; `build_day` charges one leading idle turn per unit on a land day (`lead = n_pick + d.buy_land`, route budget `turn_budget - d.buy_land`).

**Why it is in this plan at all.** Two independent reasons, and either alone would justify it:

1. **It frees the tenth BUY slot that Task 4 needs.** Turn 1 goes from nine slots to eight; three animal slots then make exactly ten. Without this task the mixed herd cannot be emitted at all.
2. **It is what makes an early second quadrant reachable.** `kagg2` buys quadrant 3 for 2,000 on day 11. Under the current schedule the whole BUY row resolves at turn 1, before every sell turn, so **no same-day sale can fund any purchase** (`docs/PLANNER_V3_1.md:519-522`) — 2,000 coins must be sitting in the purse at hour 0. With the land order after the nine sells of turn 2, the morning's lot-1 revenue pays for it.

**The two costs, both real.** The unlock now happens in the market phase of turn 2, *after* that turn's unit phase, so the first route turn is unusable on a land day: 21 turns instead of 22. And the funding is a projection — opponent lockstep sales at the same turn 2 lower the quotes seat 0 actually receives (§1.1 is opponent-free by construction). A `BUY_LAND` that then fails is not a marginal price miss: every prospective op that day no-ops on a still-LOCKED tile with its seeds and animals already bought. Hence `LAND_REV_NUM/LAND_REV_DEN = 3/4` and the provisional allocation over `avail_prov = shed − feed_need·e_wheat − n_fert_want·e_fert`, the *largest* reservations the walk can make, so the final allocation sells at least as much in lot 1.

**Interaction with Task 1 that the Phase-3 plan could not state.** `prospective` tiles are now workable from turn 3, not turn 2, and the leading idle turn is what expresses that. Verify it holds for **every** unit, not just unit 0: three of the four shed-access spawn tiles lie outside NW (`spec.SHED_ACCESS_XY`, `spec.py:244-248`), so a hand can spawn on a prospective tile and would otherwise attempt its op one turn early.

**Interaction with Task 2 that the Phase-3 plan could not state.** `land_value` is computed against `purse − land_cost`; with M2 the purse is `money + rev1`, so the valuation must be run *after* `rev1` is projected. A quadrant funded by revenue that has not landed yet is still worth exactly what its tiles will produce — the discount belongs on the *funding* side (3/4), never on the value.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_land_at_turn_two.py` from Phase-3 Task 5 Step 1 verbatim (`test_land_is_ordered_after_the_sells_of_turn_two`, `test_the_morning_sale_funds_the_quadrant`, `test_turn_one_purchases_leave_the_land_its_gap`, `test_units_idle_one_turn_on_a_land_day`), and add:

```python
def test_every_unit_idles_not_just_the_farmer():
    """A hired hand spawned outside NW does not touch a prospective tile at
    ROUTE_BASE."""

def test_the_turn_one_row_now_has_two_free_slots():
    """Precondition for Task 4: at most eight live orders on TURN_BUY."""
```

- [ ] **Step 2: implement** exactly as Phase-3 Task 5 Steps 2–4 specify.

- [ ] **Step 3: fix the stale schedule comment** at `ops.py:73-79` (§6.2 of the spec: it is wrong twice over — `BUY_LAND` was turn 1, not turn 0, and `BUY_ANIMAL` is ×1). Restate the row as it now is, and note in `plan.py`'s module docstring (`:21-36`) that a land day loses the first route turn.

- [ ] **Step 4: verify** `python -m pytest tests/test_land_at_turn_two.py tests/test_prospective_land.py tests/test_market_compaction.py tests/test_gates.py tests/test_day29_endgame.py -q`, then `tests/test_sim_equivalence.py` and `tests/test_trained_equivalence.py` — **these two are the ones that prove the engine accepts a `BUY_LAND` in a SELL turn's slot 9.** Then the full suite. `scripts/bench_sim.py`: one extra provisional `sell.allocate` pass; **budget ≤ 4%**, and if it exceeds that, reuse `inv_lots` from `_plan_and_stats` (`plan.py:1166`) rather than re-projecting.

---

### Task 4: the mixed herd — three animal candidate lists, three BUY slots

**Files:**
- Modify: `src/kagg3/core/brain.py`, `src/kagg3/core/budget.py`, `src/kagg3/core/plan.py`, `src/kagg3/core/ops.py`, `src/kagg3/core/policy.py`
- Test: `tests/test_mixed_herd.py` (new)

**Interfaces:**
- Produces: `Macro.animal_want: int[3]` replacing both `animal_kind` and `animal_count`; `budget.N_LISTS = 10`, `budget.L_ANIMAL0 = 7`, `budget.SHED_LISTS = (L_WHEAT, L_FERT, L_ANIMAL0, L_ANIMAL0+1, L_ANIMAL0+2)`; `Prefix.a_buy: int[3]` replacing `a_buy`/`a_kind`; `plan._market(..., a_buy, ...)` taking the vector; `ops.MAX_PICKUPS = 5`; `policy.DEAD_HEAD` without index 2.

**Background — what the argmax actually costs.** `animal_kind = argmax(stack([grow[EGG], grow[MILK], grow[WOOL]]))` (`brain.py:286-287`) picks **one kind for the whole day**, and `xp.argmax` returns the first maximum. At z = 0 all three `grow` scores are equal, so the answer is index 0 — goose — on every board, every day, for an untrained policy. Ranked on the planner's own coin arithmetic at hour-0 quotes on a blank day-0 board, that is the wrong answer: a goose nets 3,547 for 300 (ratio **11.8**, `tests/test_budget_order.py:85-94`), while a cow's 12 milk fires plus the same 28 fertilizer less the same 14 wheat nets ~5,015 for 400 (ratio **12.5**). Sheep are genuinely worse per coin at those prices (~8.5) — and the point is that the planner should be *computing* that, not resolving it by tie-break on a learned score that carries no coins.

The second half is the curve. `T` is 332 for egg but 122 for milk and 105 for wool (`spec.py:97-99`); `_stream_rev` walks each candidate's units down its own product's curve (`plan.py:355-365`), so fourteen animals of one kind saturate one curve where 10 cows + 4 sheep spread across two. `kagg2` runs exactly that split. Three lists in the greedy price it correctly with no new machinery: the greedy is a threshold over value-per-coin, so it takes cows until the marginal cow falls below the marginal sheep and then switches — which is the mixed herd, derived rather than declared.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_mixed_herd.py`:

```python
def test_a_day_buys_two_kinds_when_both_clear_the_threshold():
    """Purse for ~5 animals, pastures free: the row carries both COW and SHEEP
    quantities, not one kind."""

def test_at_theta_zero_the_planner_prefers_cows_to_geese():
    """The z=0 argmax bug, pinned: brain.decide on a zero theta no longer
    produces an all-goose want vector, and the granted row buys milk."""

def test_the_kind_split_follows_value_per_coin_not_the_grow_argmax():
    """Floor the milk market and the same board buys geese instead."""

def test_cow_and_sheep_compete_for_the_same_pastures():
    """Two free pastures, wants of 2 cows + 2 sheep: exactly two placements,
    lower list index first (cow before sheep)."""

def test_standing_structures_are_stocked_before_new_ones_are_built_per_kind():
    """0.8's rule survives the split, per structure kind."""

def test_five_pickup_kinds_are_charged_when_a_day_places_all_three():
def test_the_buy_row_holds_exactly_ten_slots_and_never_eleven():
def test_the_shed_room_clamp_walks_the_three_animal_slots_in_order():
def test_mixed_herd_agrees_across_backends():
```

- [ ] **Step 2: `brain.decide` splits instead of arg-maxing**

Delete `brain.py:286-287`. Replace with the machinery already used for crops at `:290-309`:

```python
wa = _softmax(xp, xp.stack([grow[spec.I_EGG], grow[spec.I_MILK], grow[spec.I_WOOL]])
                  * (1.0 + sig(head[2]) * 4.0))
animal_want = _largest_remainder(xp, wa, animal_count, spec.N_ANIMALS)
```

`animal_count` stays a local (`_qfloor(animal_share * n_dev)`, `:282`) and leaves the `Macro`; `plant_total = n_dev - xp.sum(animal_want)`. `head[2]` is the animal-mix sharpness — it is currently dead and maskable (`policy.py:165`), so reactivating it costs no new parameter block. Drop 2 from `DEAD_HEAD`, update `policy.py:35-37`'s docstring to "five decoded head outputs", and note in `docs/PLANNER_V3_1.md` §2 that the decoded count moves 32 → 33 and `head[2]` leaves the masking list.

- [ ] **Step 3: `budget.py` grows to ten lists**

`N_LISTS = 10`; `L_ANIMAL = 7` → `L_ANIMAL0 = 7`; `SHED_LISTS` gains the two new indices. `grant`'s body is already written over `N_LISTS` generically — the `shed` indicator is built by a loop over `SHED_LISTS` (`:88-89`) and every reduction is `axis=1` — so **no algorithmic change**. Two things do need attention: the module docstring says "Eight lists" and "three lists each wanting the whole room" (`:4, :17`), both now wrong; and `total(n)` sums ten rows of at most 1.07e8 (`:84`'s bound) = 1.07e9, still inside int32 but no longer with the margin the comment claims — restate the bound with the new count.

- [ ] **Step 4: `_candidates` builds three animal blocks**

The three-way static unroll at `plan.py:533-535` exists to avoid a dynamic `price_table[a_prod]` row read under `vmap`; it becomes the natural loop and the `xp.where` chain disappears — **the same three `_stream_rev` calls, one fewer select.** Per kind `a`: `u_a = min(ub_units[a], STREAM_MAX)`, product stream off `price_table[ANIMAL_PRODUCT[a]]`, the shared fertilizer stream, less `ub_feeds[a] * view.price[I_WHEAT]`, times `grow_mult[ANIMAL_PRODUCT[a]]`.

**Labelled approximation [HEURISTIC]:** all three kinds price their fertilizer stream from the same `inv_h[I_FERT]`, so a day buying all three over-values the herd's fertilizer by the cannibalisation between the lists. The grant is a threshold, not a sequence, so the offset is not knowable at pricing time; the bound is three lists × ~25 units on one curve, and `press`/`grow_mult` are the residual's owners (§1.1). Say exactly that in the comment.

- [ ] **Step 5: `_derive` goes per-kind**

Every `a_kind`-indexed scalar becomes a length-3 vector: `a_cost`, `a_struct`, `a_first`, `a_int`, `a_prod`, `ub_units`, `ub_fert`, `ub_feeds`, `ub_coins`, `acquire_ok` (`plan.py:720-749`); `a_have = view.shed[spec.I_GOOSE:spec.I_GOOSE + spec.N_ANIMALS]`.

`struct_ok` (`:723-724`) becomes per-kind: goose matches free COOPs, cow and sheep both match free PASTUREs. Because cow and sheep share a resource, the placement ranks must be assigned in **one pass in list order** (goose, cow, sheep), not per kind independently, or two kinds claim the same pasture. Use the same cumulative-boundary trick `plant_crop` uses (`:854-856`):

```python
a_avail    = a_have + a_buy                              # int[3]
place_cum  = xp.cumsum(a_avail, dtype=i32)
# per structure kind, rank the free structures, then read off which animal
# index that rank falls to
place_kind = xp.clip(_count_le(xp, place_cum, place_rank), 0, spec.N_ANIMALS - 1)
```

so `a_item` and `build_op` become per-tile arrays driven by `place_kind` rather than the single `a_kind` of `:869-870`. `n_build` (`:849-850`) is computed on `sum(a_avail)` against `n_free`, and `v_place`/`rev_place` (`:946-948`) read `ub_coins[place_kind]` and `grow_mult[a_prod[place_kind]]`.

The shed-room backstop (`:790-793`) walks the three animal slots in the engine's own slot order:
`a_buy[0] = min(n[L_ANIMAL0], room - wheat - fert)`, `a_buy[1] = min(n[L_ANIMAL0+1], room - wheat - fert - a_buy[0])`, `a_buy[2] = ...`.

Clip the wants jointly so the three kinds cannot claim more tiles than exist — the same prefix clip Task 1 Step 5 added for seeds, against `n_free + n_struct_free` (`:730`).

- [ ] **Step 6: five pickup kinds**

`pick_masks` (`plan.py:1101`) becomes `[want_feed, want_fert, m_place & (place_kind == 0), ... == 1, ... == 2]`; `_routes`'s `cpick` is `[5, 100]` and `blk` is `[5, MU]` (`:1291, 1342, 1361`); `pk_item` (`:1129-1131`) becomes the fully static `[I_WHEAT, I_FERT, I_GOOSE, I_COW, I_SHEEP]` — **simpler than today's dynamic `I_GOOSE + a_kind`**; the `for i in range(3)` at `:1132` becomes `range(5)`. `_pickup_kinds` (`:330-341`) now returns 0..5. `ops.MAX_PICKUPS = 5`, and its "documentation only" note stays true.

This costs real turns and that is correct, not a regression: a unit whose block places all three kinds owes three pickup turns, and the engine charges them. `plan.py:1103`'s `labour = n_units * (turn_budget - _pickup_kinds(d))` already accounts for it; the day will simply admit fewer tiles when it spreads three kinds across the sweep, which is the true cost of doing so.

- [ ] **Step 7: three BUY slots**

`plan.py:1386`'s `B_ANIMAL` entry becomes `([O.MO_BUY_ANIMAL] * 3, [0, 1, 2], [a_buy[a] for a in range(3)])`. Row width: 1 + 1 + 5 + 3 = **10**, land having left for turn 2 in Task 3. Assert it: add a module-level `assert len(ops_) <= MO` in `_market` — it is a Python-time check on a static layout, so it costs nothing and traces fine.

- [ ] **Step 8: verify** `python -m pytest tests/test_mixed_herd.py tests/test_animal_count_semantics.py tests/test_animal_acquisition_bound.py tests/test_unit_pickups.py tests/test_budget_greedy.py tests/test_admit_route.py -q`, then the full suite, then `tests/test_sim_equivalence.py`. `scripts/bench_sim.py`: `grant`'s arrays go 8 → 10 rows (+25% on two bisections and the top-up argmax) and `_routes` compares 5 rows instead of 3. **Budget ≤ 6%.**

---

### Task 5: land, the hire bill and the cash reserve

**Files:** Modify `src/kagg3/core/plan.py` (`_derive` purse block). Test: `tests/test_cash_reserve.py` (new).

**Background.** A concurrent agent is adding a **structural hire-bill reserve** — coins held back so tomorrow's crew is affordable. Land is the single largest lumpy purchase the planner makes (up to 4,000 coins) and, with Task 3, it can also draw on *projected* revenue. Unreconciled, a land purchase can leave the farm unable to hire tomorrow, which is precisely the "buy land, then cannot work it" failure the −77.5k drain is made of.

**The rule, and it is an ordering LAW, not a heuristic.** Inside `_derive` the purse is spent down in exactly this order, each step commented as such:

1. `hire_bill` — already spent at turn 0 before the BUY row resolves (`plan.py:681-692`).
2. **the reserve** — never spendable by anything below it.
3. `land_cost` — Task 2's grant, against what 1 and 2 left.
4. the greedy — `budget.grant`, against what 3 left.

Three consequences to implement and pin:

- **`land_value` must be computed against the post-reserve purse.** `marginal_gain`'s `purse` argument is `purse_after_reserve − land_cost`, not `money − land_cost`. A quadrant whose tiles the farm cannot stock without eating the reserve is worth less, and the valuation must see that rather than being corrected afterwards.
- **The reserve is held against `view.money` alone, never against `rev1`.** Task 3's projected lot-1 revenue may fund the *land gap* (it is a 3/4-discounted projection and a shortfall costs one purchase), but it may not fund the reserve, whose whole purpose is to be certain. Concretely: `reserve` comes off `view.money` before `rev1` is added, and `rev1` is only ever consumed by `max(land_cost - rev1, 0)`.
- **`brain`'s prospective-tile prediction is now doubly approximate** — it knows neither the reserve nor the valuation. Task 1 Step 5's seed clip and the joint animal-want clip from Task 4 Step 5 are what keep an over-optimistic prediction from turning into over-buying. Do not add a second reserve model to `brain`.

- [ ] **Step 1: Write the failing tests** in `tests/test_cash_reserve.py`:

```python
def test_land_never_eats_the_reserve():
    """Purse == reserve + land_cost - 1: no quadrant is bought."""
def test_the_reserve_is_not_funded_by_projected_revenue():
    """Enough wool in the shed to cover the reserve on paper: the reserve is
    still held against hour-0 money, and the row shrinks accordingly."""
def test_the_whole_row_fits_money_plus_discounted_revenue_less_the_reserve():
    """Fuzz 200 random views/macros; assert
    hire_bill + reserve + buy_land*land_cost + grant_total
        <= view.money + discounted_rev1  on every one."""
def test_land_value_is_computed_after_the_reserve():
```

- [ ] **Step 2: implement the ordering**, and add the fuzz invariant of the third test as a permanent assertion in `tests/test_gates.py` alongside the existing `test_planner_never_emits_cross_orders` (`tests/test_gates.py:180-190`).

- [ ] **Step 3: verify** `python -m pytest tests/test_cash_reserve.py tests/test_hire_bill.py tests/test_hire_enumeration.py tests/test_land_value.py tests/test_gates.py -q`, then the full suite. Throughput: unchanged (arithmetic only).

---

### Task 6: measurement, and the tests that pinned the old behaviour

**Files:** the 17 test files below; `docs/PLANNER_V3_1.md` §2 accounting; commit message numbers.

**The prediction, stated before the runs** (§7's rule). Against the frozen theta this is a **regression**: `Macro` changes shape, `head[2]` reactivates, `buy_land`'s decode changes meaning, and the checkpoint's learned compensations through `head[1]` are invalidated. This is a fresh-lineage change and is compared lineage-vs-lineage, never checkpoint-for-checkpoint (§2's closing paragraph). What must be true *before* training, on the z = 0 policy and on the archetype ladder:

- a day-6 board with 3,000 coins buys quadrant 2 and plants on it the same day (`test_prospective_land.py`, `test_land_value.py`);
- a day-27 board buys nothing, with no day constant in the code (`test_land_value.py`);
- the z = 0 policy buys cows, not only geese (`test_mixed_herd.py`);
- `scripts/eval_vs_baselines.py --csv` shows `move_turns` unchanged or lower and `unsold` unchanged, while the seat's tile count rises — i.e. the new tiles are *worked*, not merely owned.

Then: `scripts/eval_vs_baselines.py --csv --seed-base` against the `kagg2` opponent on ≥ 32 matched seed pairs, `scripts/paired_ci.py` for the interval, and the ladder. **The flagship claim to falsify is §7's:** once the churn is priced and the tiles are usable, land value flips sign and the `kagg2` matchup — which hinges on quadrants 2–4 — moves.

- [ ] **Step 1: update the tests that pin the old behaviour.** The audit found these; every one is a deliberate change, not a fix-up.

**The shared fixture — do this first, it unblocks 22 files.** `tests/test_budget_order.py:47-57` `_macro`: `"animal_kind": np.int32(0), "animal_count": np.int32(0)` → `"animal_want": np.zeros(spec.N_ANIMALS, np.int32)`; `"buy_land": np.int32(0)` → `"land_bias": np.int32(0)`. `P.Macro(...)` is constructed in exactly two places repo-wide — here and `brain.py:337`.

*Land behaviour, now deliberately different:*

| File:line | What changes |
|---|---|
| `tests/test_budget_order.py:71-75` `test_a_requested_quadrant_is_granted_ahead_of_the_greedy` | **The central pin of the old design.** It asserts a 1,000-coin purse buys land and *not* the goose, i.e. land wins unconditionally on affordability. Rewrite as two tests: at `land_bias = 0` the quadrant wins only when `land_value > 0`, and a saturated-negative bias hands the purse to the goose. The file docstring ("Land is the exception: its value is a learned logit, not coins") is now false — rewrite it. |
| `tests/test_budget_order.py:78-82` | `buy_land=0` → a saturated-negative `land_bias`. |
| `tests/test_budget_order.py:119-125` `test_the_buy_row_layout_is_fixed_whatever_is_bought` | Expected live-op list changes twice: `BUY_LAND` leaves `TURN_BUY` (Task 3) and two more `BUY_ANIMAL` slots arrive (Task 4). |
| `tests/test_budget_order.py:179-181, 230-237` | `_buy_bill`'s `elif o == O.MO_BUY_LAND` stops matching on `TURN_BUY` — a **silent under-count**, not a failure. Make the helper scan every turn. The exact `spent == 700` equality then needs re-deriving. |
| `tests/test_hire_bill.py:8-12, 49-50, 67-68, 87-114` | The premise — "BUY_LAND last, so land was structurally the slot that failed" — dissolves. `PURSE = LAND_PRICES[0] + 5*ANIMAL_COST[0]` and `_buy_bill(...) == PURSE` exactly both need re-deriving against the turn-2 land order and Task 5's reserve. Keep the *invariant* (`buy_bill + hire_bill <= PURSE`); replace the exact figure. |
| `tests/test_day29_endgame.py:115-119` `test_day_27_is_not_terminal` | Reads `qty[TURN_BUY][op[TURN_BUY] == MO_BUY_LAND]`; land now lives at `(TURN_SELL, MO-1)`. Also: with Task 2, day 27 may legitimately *refuse* the quadrant — restate the test around a day whose `land_value` is positive, or assert on a different turn-27 purchase. |
| `tests/test_day29_endgame.py:101-104` | The terminal day must suppress land wherever it now lives. |
| `tests/test_free_land_urgency.py:51-68` | **Three exact-equality assertions** (`== 1`, `== 12`, `== 1`) on `plant_target.sum() + animal_count`, computed from an `n_free_slots` that counts only owned tiles. `_obs` has `nquad=2, money=10_000` — affordable — so Task 1 moves every one of them. Also `animal_count` is gone: use `animal_want.sum()`. |
| `tests/test_land_affordability.py:44-73` (5 tests) | These test the *decode*, so they survive Task 1 but not Task 2: `buy_land` is no longer 0/1. Retarget onto `land_bias`, keeping the `clip(-1, 4)` coverage. |
| `tests/test_archetypes.py:44-47, 72-86` | `int(m.buy_land) == 1` → a bias sign; `plant_target.sum() + animal_count` → `+ animal_want.sum()`; `lands == {0, 1}` diversity now measures bias sign, and the docstring's hard-coded affordability arithmetic needs rewriting. |
| `tests/test_market_compaction.py:53`, `tests/test_gates.py:180-190` | Must newly cover a `BUY_LAND` sharing turn 2 with nine SELLs — this is where a compaction or `assert_no_cross` mistake would surface. Extend rather than edit. |
| `tests/test_sim_equivalence.py`, `tests/test_trained_equivalence.py` | Unchanged in code, **mandatory to run**: they are the proof the engine accepts the new slot layout. |

*Animal behaviour, now deliberately different:*

| File:line | What changes |
|---|---|
| `tests/test_budget_greedy.py:24-30, 40, 49, 98-126, 128-161, 203` | **Twelve hard-coded 8-long grant vectors** (`[3,0,0,0,0,0,0,0]`, `[3,0,0,0,0,0,0,1]`, `[2,0,5,0,0,0,0,0]`, `[3,3,1,0,0,0,0,3]`, …) and docstrings saying "three lists chase two slots". Every one becomes 10 long with five shed lists. Largest single edit in the suite. |
| `tests/test_animal_acquisition_bound.py:38-69` | `_bought` passes `animal_kind=` and sums one `MO_BUY_ANIMAL` slot; the 0.2 bound is now per-kind. `test_rejection_does_not_touch_stock_in_hand` depends on `a_have = shed[I_GOOSE + a_kind]`. |
| `tests/test_animal_count_semantics.py:38-58` | Exact `(bought, n_place, n_build)` tuples on an all-goose board; the "stock standing structures before building" rule is now per structure kind. Add a cow/sheep pasture-contention case here rather than only in `test_mixed_herd.py`. |
| `tests/test_budget_order.py:85-98, 128-163, 184-237` | The hand-computed goose economics assume one animal list; `grow_mult[I_EGG] = 1024` now boosts one of three; "three shed-bound lists" becomes five. |
| `tests/test_unit_pickups.py:74-83` | Pins the three pickup kinds as `[I_WHEAT, I_FERT, I_GOOSE]` and `MAX_PICKUPS = 3`. Now five, with a static item list. |
| `tests/test_admit_route.py:203-212` | `int(P._pickup_kinds(np, d)) == 1` and the exact budget `22 - 1 = 21` with 7 tiles admitted — arithmetic survives, but re-verify against the new mask stack. |
| `tests/test_genome_retype.py:96-115` | Iterates `Macro._fields` and `Prefix._fields` asserting int32 on both backends. Both tuples change shape; the test is the guard that catches a float or int64 leak in the new decode — keep it and re-run on both backends. |
| `tests/test_feed_value.py:46-54`, `tests/test_hire_bill.py:67-68`, `tests/test_day29_endgame.py:23, 55-57` | `animal_count=` keyword and one-slot `MO_BUY_ANIMAL` sums. |
| `tests/test_es_masking.py:27-70` | `PO.live_mask()` and `N_DEAD` change when `head[2]` reactivates. |
| `tests/test_gene_sweep.py:25-30` | `gb5[1]` is still `land_afford`; the gene *layout* is unchanged, but re-run — the sweep's semantics now move a coin bias, not a boolean. |

- [ ] **Step 2: update `docs/PLANNER_V3_1.md`.** §2's table: the `buy_land` row becomes `land_bias` with the `land_cost × tanh(z)` transform; add the animal-mix sharpness row; decoded outputs 32 → 33; `head[2]` leaves the §2 masking list. §5's Open list loses "multi-kind animal days"; M1 and M2 move from *open modules* to *shipped*, each with the measured throughput number. §0.3's "Land *valuation* stays [LEARNED]" is superseded — restate as "[HEURISTIC] valuation with a [LEARNED] coin bias" and cite Task 2's approximation by name.

- [ ] **Step 3: measure and record.** `scripts/bench_sim.py` cumulative before/after (**gate: 15%**; per-task budgets above sum to ~14%, so an overrun in any one task must be reformulated rather than absorbed). Then `scripts/eval_vs_baselines.py --csv --seed-base` on ≥ 32 matched pairs vs `kagg2`, `scripts/paired_ci.py`, `scripts/ladder.py`. Put the paired interval and the four pre-training assertions from this task's preamble in the commit message.

---

## Risk register

| Risk | Where it bites | Mitigation |
|---|---|---|
| **Slot overflow** — eleven live orders on turn 1 | Task 4 without Task 3. The engine silently truncates at 10 (`:551, :560`) and the eleventh (land, today) is lost — already cost a purchase once (`plan.py:684-690`) | Task order 3 → 4, plus the static `assert len(ops_) <= MO` in `_market` and `test_the_buy_row_holds_exactly_ten_slots_and_never_eleven` |
| **Throughput** — `grant` 8 → 10 lists, `marginal_gain`, a provisional `allocate`, `_routes` 3 → 5 pick rows | The 15% gate | Per-task budgets (1%, 3%, 4%, 6%); `marginal_gain` deliberately replaces the second full `grant` (~+18% on its own); fallbacks named in each task |
| **Projected revenue that does not land** | Task 3: a failed `BUY_LAND` leaves every prospective op no-oping on LOCKED tiles with seeds already bought | 3/4 discount on `rev1`, provisional allocation over the *largest* reservations, and `test_the_morning_sale_funds_the_quadrant`'s negative case |
| **`brain` over-predicts the grant** | Task 1: `plant_target` sized on 25 tiles the planner then refuses | `plant_here` is masked by `free_slot`; Task 1 Step 5 clips `w_seed`; Task 4 Step 5 clips the animal wants. Loss is bounded and one-sided (seeds carry to tomorrow in `view.seeds`) |
| **Fertilizer double-counting across three animal lists** | Task 4 Step 4 | Labelled [HEURISTIC], bounded at three lists × ~25 units on one curve, residual owned by `press`/`grow_mult` per §1.1 |
| **Frozen-theta regression** | Task 6 | Predicted in writing before the run; fresh lineage, compared lineage-vs-lineage per §2 |
| **Concurrent edits to `plan.py`** | The reserve agent owns `_derive`'s purse block | Rebase before every task; Task 5 exists to reconcile; never trust the line numbers in this plan without re-reading |
