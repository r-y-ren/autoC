# Working the idle tiles — root cause, value, and the design

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax. This plan touches the same three files as `docs/superpowers/plans/2026-08-25-land-value-mixed-herd.md`, which is being implemented concurrently — **read §8 before starting any task.**

**Status: DESIGNED, MEASURED, not implemented.** No planner code was changed to produce any number below; every counterfactual is an in-process monkeypatch over the real `kaggle_environments` engine (§11).

This answers lever 1 of `2026-08-26-kagg3-vs-kagg2-diagnosis.md` — *"kagg3 owns 4 quadrants but works only 62 % of tiles"* — and **overturns its premise twice**. The idle tiles are not caused by the horizon, the hire enumeration, the cash reserve, the dev knobs or the land timing; and simply working them is worth **−6k to −23k**, not +19k. What pays is making the day's *route* cheap enough that the tiles the planner already asks for get reached.

---

## 1. Headline

**The day's labour is spent walking, and the walking is caused by the route order sweeping the board up to four times.**

`_plan_and_stats` builds the route order as `route_tier = d.tier * 2 + (d.tile_value > 0)` — four groups (mandatory-priced, mandatory-worthless, optional-priced, optional-worthless), each swept in serpentine order and **concatenated**. A group of *m* scattered tiles still spans the whole board, so *k* populated groups cost the crew *k* crossings of the worked span. Consecutive tiles inside a group are 100/*m* sweep positions apart instead of 100/(Σ*m*).

Two consequences, and the second is the expensive one:

1. **Moves.** 48.6 % of every unit-turn in the season is a move; 36.4 % does work.
2. **The admit estimate stops being true.** `cum_est` charges each tile `n_ops + EST_MOVES = n_ops + 2`. Under four crossings the real cost is higher, so admission lets in tiles the route cannot reach; the three `ADMIT_ROUNDS` cannot converge; and the shortfall is taken off the **value tail** — which is exactly where new plantings sit. **305 plantings are queued over a season and 141 are done.** 21,302 coins/season of queued task value is never worked.

Collapsing the four groups to two — with a one-line guard that keeps section 0.5's LAW intact — is worth, paired over 16 games in each matchup:

| | own coins | opponent | margin |
|---|---|---|---|
| vs `starter` | **+13,061 ± 7,932** (129,671 → 142,732) | 3,427 → 3,408 | **+13,080 ± 7,956** |
| vs `kagg2` | **+11,212 ± 9,228** (65,248 → 76,460) | 113,477 → 122,095 | +2,594 ± 8,774 |

It breaks exactly **one** behaviour test (a turn-index pin), costs no throughput, and needs no gene.

## 2. What was run

| | |
|---|---|
| Agent | `artifacts/p2s0/champion.npy`, 4,386 params — the best theta on this machine, the same one the diagnosis used |
| Opponents | `starter` and `../kaggriculture2/main.py` |
| Games | 8 seeds × 2 seats × 2 opponents = **32 per configuration**, seed base 20260825, `kaggle_environments` on CPU |
| Telemetry | the planner's own `_derive` / `task_order` / `_routes` re-run inside the macro hook on the very `DayView` the plan was built from, plus a wrapper on `budget.grant`. Per day: `n_free`, `plant_target`, granted wants, `h*`, `n_tasks`, `n_admit`, `covered`, per-unit move/op/pickup/idle turns, `value_dropped` |
| Baseline | reproduces the diagnosis: 129,671 vs `starter`, 65,248 vs `kagg2` against its 132,211 / 62,046 |

**Methodology warning, and it is not academic.** Every counterfactual is a monkeypatch on module globals. A `ProcessPoolExecutor` worker that has run one patch carries it into the next job. The first three measurement batches of this work were silently contaminated that way (they made the 4th quadrant look like a −13k mistake and end-of-season feeding like a −21k one; both are near zero). Every number in this document comes from a pool built with **`max_tasks_per_child=1`**.

## 3. The evidence

### 3.1 Where the season's unit-turns go

Champion, mean per game, 16 games each. "Visit" = a tile the route actually reaches.

| | vs `kagg2` | vs `starter` |
|---|---|---|
| unit-turns available | 5,559 | 5,964 |
| **moves** | **2,704 (48.6 %)** | **2,974 (49.9 %)** |
| — of which the approach walk from the shed | 1,355 (24.4 %) | 1,471 (24.7 %) |
| **ops** | **2,024 (36.4 %)** | **2,095 (35.1 %)** |
| pickups | 175 (3.1 %) | 175 (2.9 %) |
| idle (block ran out of reachable work) | 655 (11.8 %) | 719 (12.1 %) |
| tile-visits | 1,023 | 1,144 |
| **inter-tile moves per visit** | **1.32** | **1.31** |
| ops per visit | 1.98 | 1.83 |

The approach walk is **structural and irreducible**: the engine clears `farm["hands"] = []` at every end of day (`kaggriculture.py:880`) and re-spawns the whole crew on the four shed-access tiles at the board's centre, so every unit walks out from the middle every morning — 5.30 turns per active unit-day, and it does not move under any intervention tested.

The 1.32 inter-tile moves per visit is the part that is a defect. A serpentine sweep of a contiguous admitted set costs **1.00**.

### 3.2 The day is labour-bound from day 13, and it knows it

| (vs `starter` / vs `kagg2`) | days 0–11 | days 12–26 |
|---|---|---|
| fraction of days where the hire scan is **task**-bound (all queued work fits) | 0.90 / 0.96 | **0.11 / 0.11** |
| mean `h*` | rising 2 → 8 | 10.6 (kagg2) / 11.7 (starter), against `MAX_HANDS = 16` |

From day 13 on, the constraint is turns. And the resources the planner would need are all *sitting idle*:

| day | 14 | 17 | 20 | 24 | 29 |
|---|---|---|---|---|---|
| free tiles | 21 | 42 | 40 | 47 | 69 |
| money | 5,243 | 8,415 | 17,620 | 37,178 | 60,050 |
| **unplanted seeds in hand** | 7.2 | 12.2 | **24.0** | 21.8 | 18.8 |
| plantings queued / done | 10.6 / 6.1 | 22.7 / 4.0 | **16.9 / 3.0** | 9.8 / 1.1 | 0 / 0 |

`plant_target` is 12–21 tiles a day from day 16 to day 26. The board has the tiles. The purse has the money. The shed has the seed. **1.1–4.4 of them get planted.** Nothing is refusing to plant; the route never arrives.

### 3.3 The season's decay, in one line

Planted tiles 46.6 (d14) → 37.2 (d20) → 18.5 (d28) is not a decision. It is the arithmetic of a one-time crop turning its tile over while the replant is queued at the value tail every single day and dropped.

## 4. What is *not* the cause

Every candidate named in the brief, refuted with its own number.

| candidate | verdict | evidence |
|---|---|---|
| horizon / season-end stops planting too early for short crops | **no** | `can_mature` + `VAL.new_plant_units` are exact, not conservative: wheat and carrot are plantable through **day 26** (`harvest_age` clamps to 2, two units still bank), tomato through day 20, strawberry and melon through day 18. Measured `plant_target` is non-zero every day to day 26 and 0 from day 27. |
| the hire enumeration caps the crew below what the land needs | **no** | `h*` is 10.6–11.7 mid-season against `MAX_HANDS = 16`, and the enumeration's own score for a 16-hand day is **below** the chosen day's on every day from d14 (e.g. d20: 25,902 vs 23,943). Scoring hires as free (`HIRE_BILLS = 0`) lifts d20 occupancy 63.2 → 77.6 tiles and costs **−10,924 ± 12,177 (kagg2) / −11,115 ± 11,782 (starter)**. |
| the cash reserve starves seed purchases | **only before day 13** | season `purchase_shortfall` is 12,148 coins and lands on days 1–12 (purse 7–1,000 coins). From day 13 the purse is 3k–60k and unspent, and 19–24 seeds sit unplanted in hand. |
| `free_urgency` / `dev` knobs | **no** | they set `plant_target`, which is 12–21/day when 1–4 get planted. The knob is not the bottleneck it feeds. |
| land bought late with no crew plan | **second-order, and matchup-signed** | refusing the 4th quadrant: **−1,356 ± 5,548 (starter) / +5,080 ± 3,681 (kagg2)** on own coins, +4,317 ± 3,504 on kagg2 margin. Real, small, and a *learned* land value is the right home for it — which is `2026-08-25-land-value-mixed-herd` Task 2, not this plan. |
| the labour router does not reach far tiles | **yes — this is it** | 54 % of queued plantings unreached; 21,302 coins/season of queued value dropped; 1.32 inter-tile moves per visit against a 1.00 ideal. |
| the per-day action budget | **yes** | 36.4 % of unit-turns do work. |

### 4.1 And a correction the diagnosis needs: the product mix is already near a local optimum

The diagnosis ranks products by marginal coins **per unit against the residual town drain** (tomato +93, wool +211, milk −55) and concludes that the idle tiles should be filled with the uncontested crops. Measured, forcing exactly that **loses**:

| forced mix (all `plant_target` redirected) | own coins vs `starter` | own coins vs `kagg2` |
|---|---|---|
| wheat / carrot / tomato only ("uncontested") | **−38,932 ± 12,055** | **−19,072 ± 11,164** |
| melon + strawberry only ("high value") | −36,460 ± 10,907 | −15,734 ± 14,863 |
| strawberry only | −70,413 ± 13,590 | −36,599 ± 15,172 |

The binding resource is **unit-turns, not market depth**, so the yardstick is coins per unit-turn, not coins per unit. At kagg3's realised multiples against `kagg2`, a tile's whole life (`VAL` tables, seed cost netted):

| crop | units by d28 | ops over its life | tile-days | realised c/unit | **coins per op** |
|---|---|---|---|---|---|
| MELON | 6 | 12 | 13 | 125 (0.50× base) | **55.8** |
| STRAWBERRY | 4 | 14 | 17 | 150 (1.25×) | **35.7** |
| TOMATO | 4 | 11 | 12 | 74 (1.24×) | 22.5 |
| CARROT | 3 | 5 | 4 | 41 (1.17×) | 20.6 |
| WHEAT | 4 | 6 | 5 | 34 (1.35×) | 20.8 |

Melon still leads on labour at **0.50× base**, because six units off twelve ops beats four units off six. Against `starter` the spread is wider still (melon 113 c/op, strawberry 61, wheat 17). Filling idle tiles with the uncontested crops trades 36–56 c/op work for 21–23 c/op work, which is the −19k.

(These apply the season's *average* realised multiple to a marginal tile, so they overstate the marginal unit — the diagnosis's marginal table is the right instrument for one more *unit*. The three counterfactuals above test the ranking directly and confirm it.)

### 4.2 And a second correction: working the tiles, on its own, loses money

| intervention | d20 occupied tiles (base 72.6 / 63.2) | own coins vs `starter` | own coins vs `kagg2` |
|---|---|---|---|
| development promoted to the mandatory tier | **94.3 / 88.0** | **−23,312 ± 9,198** | **−6,041 ± 10,635** |
| development tile value ×3 (within tier) | 78.8 / 70.1 | −3,006 ± 7,604 | +10,087 ± 7,975 |
| `EST_MOVES = 1` (admit more) | 61.1 / 53.0 | −21,499 ± 10,810 | −751 ± 10,774 |
| hire as if free | 90.2 / 77.6 | −11,115 ± 11,782 | −10,924 ± 12,177 |

The first row is the diagnosis's lever 1 taken literally, and it is the worst of them: promoting development over the harvest gets 94 of 100 tiles occupied and loses 23k, because the route order discards value information entirely *within* a group — it is serpentine — so anything admitted ahead of a harvest spends the turns the harvest needed.

`EST_MOVES = 1` fails for the same reason from the other end: admitting tiles the route cannot reach interleaves junk into every unit's block.

## 5. The design

Four changes. **R1 and R2 are structural and free; R3 and R4 are genes that decode to a no-op at zero theta, so every incumbent checkpoint decodes to exactly R1+R2's behaviour.** R1/R2 do change the z = 0 policy — that is the point, and it is a fresh-lineage change compared lineage-vs-lineage, as `2026-08-25-land-value-mixed-herd` Task 6 already establishes for its own.

### R1 — the route crosses the worked span once *(structural, ≈0 % throughput)*

Two lines.

```python
# plan._derive, closing the task-value section (today ~plan.py:1030-1040)
tile_value = xp.clip(v_harvest + v_water + ... + v_place, 0, BUD.VALUE_CAP).astype(i32)
tier       = mandatory.astype(i32)
# A mandatory tile is never "worth nothing" [LAW, 0.5]. The route's last group
# is the work that is worth nothing, and a survival watering on a spent crop
# must not fall into it. One coin is enough: ordering *inside* a group is
# serpentine, so the floor only decides which group a tile is in.
tile_value = xp.maximum(tile_value, tier)
```

```python
# plan._plan_and_stats (today plan.py:1195)
route_tier = (d.tile_value > 0).astype(i32)        # was  d.tier * 2 + (d.tile_value > 0)
```

Two route groups — everything priced-or-mandatory, then the worthless remainder — instead of four. The admission order `order_v = task_order(xp, d.task, d.tile_value, d.tier)` is **untouched** and still reads `d.tier`, so 0.5's LAW keeps its teeth where it is enforceable: a mandatory tile is admitted ahead of every optional one, and `n_admit` is only ever *reduced*, from the value tail. The worthless group stays last, which is the protection `test_mandatory_tier.py`'s forty-weed boards exist for.

Measured (16 games per cell, paired 95 % CI):

| | own coins | margin |
|---|---|---|
| vs `starter` | 129,671 → **142,732**, **+13,061 ± 7,932** | +13,080 ± 7,956 |
| vs `kagg2` | 65,248 → **76,460**, **+11,212 ± 9,228** | +2,594 ± 8,774 |

Mechanism confirmed in the telemetry (vs `kagg2` / vs `starter`):

| | base | after R1 |
|---|---|---|
| inter-tile moves per visit | 1.32 / 1.31 | **1.00 / 1.02** |
| tile-visits per season | 1,023 / 1,144 | **1,260 / 1,371** (+23 % / +20 %) |
| `value_dropped` per season | 21,302 / 36,690 | **5,303 / 8,631** (−75 % / −76 %) |
| plantings done per season | 141 / 123 | 154 / 144 |

Throughput: one `xp.maximum` on `int32[100]`, one fewer multiply-add on `int32[100]`. Budget **≤0.5 %**; measure it anyway.

**Three alternatives, all measured, all rejected:**

* *Collapse to a single group* (`route_tier = 0`): +12,843 ± 8,089 / +11,146 ± 9,224 — the same coins, but it breaks **10 tests**, including every forty-weed LAW pin and `test_day_27_is_not_terminal`. The mandatory work genuinely is lost on adversarial boards. Not shippable.
* *Keep four groups, alternate the sweep direction per group* so the crew ends one group where the next begins (boustrophedon): **+680 ± 2,446 / −18 ± 190.** The cost is not the jump between groups; it is that each group spans the whole board however it is walked. **Do not build this.**
* *Drop only the `tile_value > 0` split, keep mandatory-first*: +2,220 ± 3,807 / +549 ± 549. The expensive split is the mandatory one, which is why R1 has to move that LAW rather than the other.

### R2 — the admit model, corrected to the one-crossing route *(structural, 0 % throughput)*

Once the route crosses once the measured inter-tile cost is exactly 1.00–1.02 moves per visit, so `EST_MOVES = 2` over-charges every tile by one — while the term it has been silently standing in for is not modelled at all: the per-unit walk from the shed-access spawn to the unit's block, **5.30 turns per active unit-day, 24.4 % of the whole season budget**, invariant across every configuration tested.

```python
EST_MOVES = 1        # exact for a single serpentine crossing (measured 1.00 / 1.02)
EST_LEAD  = 5        # the shed-to-block walk every unit pays every morning
                     # (measured 5.30 vs kagg2, 5.32 vs starter; the engine
                     # clears farm["hands"] nightly, so this is not amortisable)
...
turns_h = (h + 1) * (route_turns(h) - n_kinds0 - EST_LEAD)              # the hire scan
labour  = n_units * (turn_budget - _pickup_kinds(xp, d) - EST_LEAD)     # the admit stage
```

| | own coins | margin |
|---|---|---|
| vs `starter` | 129,671 → 141,525, **+11,854 ± 11,233** | +11,834 ± 11,232 |
| vs `kagg2` | 65,248 → **80,888**, **+15,640 ± 10,979** | +852 ± 8,151 |

The largest own-coin move in the sweep. **Both halves are corrections to the same model and neither is safe alone** — that is the measurement that proves they belong together: `EST_MOVES = 1` by itself is −21,499 ± 10,810 / −751 ± 10,774, and the lead charge by itself is −17,224 ± 8,946 / −4,414 ± 6,198.

`EST_LEAD` is a measured constant, not a bound, and that is safe by construction: it only ever *subtracts* from the budget, so it can under-admit and never over-admit, and the days it is wrong on (early, 1–3 units working next to the shed) are task-bound anyway — 0.90–0.96 of days 0–11 against 0.11 of days 12–26.

### R3 — `compact`: *where* the day develops *(gene, inert at zero, ≈1 %)*

`slot_rank = _rank(xp, free_slot)` and `place_rank = _rank(xp, struct_ok)` (`plan.py:926-928`) choose which free tiles get planted and built, **in sweep order**, so development scatters over the whole board — and the next 12–17 tile-days of watering and harvesting inherit that scatter.

```python
#: Manhattan distance from the shed-access block to each serpentine position.
DIST_SHED = (np.abs(SERP_X - 4.5) + np.abs(SERP_Y - 4.5)).astype(np.int32)   # 1 .. 9

compact   = _qfloor(xp, 9.0 * xp.tanh(aux_new)).astype(i32)      # 0 at z = 0
key       = compact * xp.asarray(DIST_SHED)                      # all-zero at z = 0
slot_rank = _rank_near(xp, free_slot, key)
```

`_rank_near(mask, key)` is the exclusive rank by ascending `key`, exact ties to the lower serpentine index. It must **not** be `_rank_by` — that is a `[100, 100]` pairwise compare and `task_order` already runs five of those per day. `key` has at most ten reachable values, so a static bucket count is enough:

```python
def _rank_near(xp, mask, key):
    """Exclusive rank of each `mask` entry by ascending `key`, ties to the
    lower index. `key == 0` everywhere reproduces `_rank` bit-for-bit, which
    is what makes the gene inert at z = 0."""
    i32 = xp.int32
    m = mask.astype(i32)
    lt = xp.zeros(N_T, i32)          # masked entries in a strictly lower bucket
    same = xp.zeros(N_T, i32)        # masked entries in the same bucket, lower index
    for b in range(DIST_MAX + 1):    # static, unrolled: 10 iterations
        inb = (key == b).astype(i32) * m
        cum = xp.cumsum(inb, dtype=i32) - inb
        same = same + (key == b).astype(i32) * cum
        lt = lt + (key > b).astype(i32) * xp.sum(inb, dtype=i32)
    return (lt + same).astype(i32)
```

Ten `[100]` cumsums and ten `[100]` reduces against `_rank`'s single cumsum — well under a single `task_order`. Budget **≤1.5 %**.

Measured with `compact` saturated, on top of the single-crossing route:

| | own coins | **margin** |
|---|---|---|
| vs `starter` | 129,671 → 138,062, +8,391 ± 7,490 | **+8,350 ± 7,490** |
| vs `kagg2` | 65,248 → 73,948, +8,700 ± 12,873 | **+14,062 ± 5,062** (margin −48,229 → **−34,168**) |

**The best all-round result in the sweep, and the only intervention that is significantly positive on margin in both matchups.** Without R1 it is +7,399 ± 7,844 / −7,217 ± 8,291 on coins and −7,868 ± 8,291 on kagg2 margin — it is a *complement* to R1, not a substitute, because clustering only pays once the sweep is a single crossing.

A gene rather than a constant because the sign of its own-coin effect flips by matchup, and `glob` already carries what it needs to condition on (`opp_plant`, `opp_animal`, `opp_nquad`, `opp_money`, `mean(price/base)`).

### R4 — `dev_weight`: *how much* labour development is worth *(gene, inert at zero, 0 %)*

`v_plant` / `v_place` price a new tile at its stream value under `grow_mult` — which is per-*product* and also sizes the purchase budget, so nothing today can say "spend more of this day's turns on development" without also buying more seed.

```python
dev_w   = _qfloor(xp, GROW_ONE * _unit_ratio(xp, head_new)).astype(i32)   # GROW_ONE at z = 0
v_plant = xp.clip(v_plant * dev_w // GROW_ONE, 0, BUD.VALUE_CAP)
v_place = xp.clip(v_place * dev_w // GROW_ONE, 0, BUD.VALUE_CAP)
```

`v_plant` is already clipped to `VALUE_CAP = 2**20 − 1` and `dev_w ≤ 4 × GROW_ONE = 1024`, so the product stays inside int32 before the clip — the `< 2**20` rule of §2 holds on the way out.

Measured at ×3 on top of R1:

| | own coins | **margin** |
|---|---|---|
| vs `starter` | +6,117 ± 7,179 | +6,106 ± 7,209 |
| vs `kagg2` | +4,896 ± 12,143 | **+9,341 ± 4,768** |

Again a complement: on its own it is −3,006 / +10,087 on coins and −2,992 / −3,214 on margin.

It must scale the **value**, never the tier: promoting development to the mandatory tier is −23,312 ± 9,198 / −6,041 ± 10,635 (§4.2). Development has to win the labour on coins, not outrank the harvest.

### R5 — where the two genes live

Append a new head block; **never reuse a `DEAD_HEAD` slot.**

```python
("g6", (N_HEAD_HID, 2)), ("gb6", (2,)),        # compact, dev_weight   (+66 params)
```

`policy.unpack` zero-pads every shorter theta (`policy.py:119-120`), so every incumbent decodes `compact = 0` and `dev_weight = GROW_ONE` — i.e. **exactly R1+R2's plan, bit-for-bit**. Reusing `head[2]`/`head[3]` would not: a masked coordinate holds whatever it held when masking began, which on a resumed or trunk-warmed run is not zero (`policy.py:170-178`), and `2026-08-25-land-value-mixed-herd` Task 4 reactivates `head[2]` for the animal mix anyway.

`N_PARAMS` 4,386 → 4,452, and `DEAD_HEAD` / `DEAD_AUX` are unchanged.

## 6. Value summary — every measurement in one table

16 games per cell (8 seeds × 2 seats), paired 95 % CI, champion theta.

| change | own Δ vs `starter` | own Δ vs `kagg2` | margin Δ vs `kagg2` | d20 occupied |
|---|---|---|---|---|
| **R1** route crosses once | **+13,061 ± 7,932** | **+11,212 ± 9,228** | +2,594 ± 8,774 | 80.9 / 70.2 |
| **R1+R2** admit model corrected | +11,854 ± 11,233 | **+15,640 ± 10,979** | +852 ± 8,151 | 78.9 / 65.1 |
| **R1+R3** `compact` saturated | +8,391 ± 7,490 | +8,700 ± 12,873 | **+14,062 ± 5,062** | 80.9 / 71.7 |
| **R1+R4** `dev_weight` ×3 | +6,117 ± 7,179 | +4,896 ± 12,143 | **+9,341 ± 4,768** | 87.1 / 76.6 |
| R3 alone | −7,217 ± 8,291 | +7,399 ± 7,844 | −7,868 ± 8,291 | 68.8 / 58.2 |
| R4 alone | −3,006 ± 7,604 | +10,087 ± 7,975 | −3,214 ± 7,270 | 78.8 / 70.1 |
| R2 alone (`EST_MOVES = 1`) | −21,499 ± 10,810 | −751 ± 10,774 | — | 61.1 / 53.0 |
| R2 alone (lead charge only) | −17,224 ± 8,946 | −4,414 ± 6,198 | — | 66.2 / 61.2 |
| refuse the 4th quadrant | −1,356 ± 5,548 | +5,080 ± 3,681 | +4,317 ± 3,504 | 65.0 / 56.7 |
| feed the herd to the end | +60 ± 118 | −979 ± 682 | −928 ± 708 | 72.6 / 63.2 |
| hire as if free | −11,115 ± 11,782 | −10,924 ± 12,177 | — | 90.2 / 77.6 |
| development is mandatory | −23,312 ± 9,198 | −6,041 ± 10,635 | — | 94.3 / 88.0 |
| boustrophedon sweep, four groups | +680 ± 2,446 | −18 ± 190 | — | 72.6 / 63.2 |
| uncontested crops only | −38,932 ± 12,055 | −19,072 ± 11,164 | — | 51.9 / 44.4 |
| melon + strawberry only | −36,460 ± 10,907 | −15,734 ± 14,863 | — | 85.2 / 64.9 |

**The coin story and the margin story point in different directions against `kagg2`.** R1/R2 buy own coins (+11–16k) and almost no margin (+0.9–2.6k, not significant), because the opponent's book moves with ours; R3/R4 buy margin (+9.3–14.0k, significant) at less coin, by pushing volume into the contested products where a coin costs `kagg2` more than it costs us — the 1.5 : 1 denial rate the diagnosis measured in §5. `GOAL.md` optimises **win rate**, so the genes are the half that wins games, and that is the argument for shipping them as genes and letting ES resolve the trade against the pool rather than picking a constant here.

**Against `kagg2` this plan does not, on its own, produce a win.** Best measured margin is **−34,168 (R1+R3)** against a base of −48,229 — a 29 % cut, 0/16 wins either way. The remaining 34k is the land / mixed-herd / product-mix work of the other two plans.

## 7. End of season — measured, and there is nothing to build

The brief asks for "plant only crops that finish before day 30, feed animals to day 29, wind the crew down only when nothing is left to do". All three are already right, and one is actively wrong.

1. **The planting horizon is exact, not conservative.** `brain.decide`'s `can_mature` (`brain.py:297`) plus `VAL.new_plant_units` stop each crop on the last day whose harvest still banks by `LAST_SHED_DAY = 28`: **wheat and carrot through day 26** (`harvest_age` clamps to 2 and two units still bank), tomato through day 20, strawberry and melon through day 18. Measured `plant_target` is non-zero every day to day 26 and exactly 0 from day 27. There is no short-crop conservatism to remove.
2. **Feeding the herd to the end costs coins.** Forcing every living animal fed (`animal_value + 600`, so `keep_val` saturates at `ANIMAL_COST` and every feed clears 1.4's test) is **−979 ± 682 vs `kagg2`** and **+60 ± 118 vs `starter`** — the wheat and, mostly, the turns are worth more than the last fires. The 16-of-26 attrition the diagnosis names is real and it is the *correct* answer; its estimate of **+4k for lever 5 is refuted**. Deaths cluster at eod 26–28 (−0.2 / −3.6 / −7.9 animals), and eod-28 deaths cost nothing at all because day 29 has no end of day.
3. **The board is not stranded on day 29.** Coins standing unharvested on tiles at day-29 hour 0: **281 vs `kagg2`, 889 vs `starter`** (379 / 1,432 under R1). `mandatory` already carries `(day >= LAST_SHED_DAY) & want_harvest` (`plan.py:1037`), and day 28's sweep banks essentially everything.
4. **The crew winds down because the work runs out.** `h*` falls 9.5 → 7.2 → 3.9 → 1.0 over days 26–29 while `value_dropped` on those days is 1,351 / 502 / 211 / 221 — the days it declines to staff are days whose unreached work is worth nothing. Forcing a big crew is −10.9k / −11.1k.

**The only end-of-season gain available is a consequence of R1**, and it is large: days 24–28 coverage rises from 42.6 to 58.0 tiles per day (vs `kagg2`) and the last week's `value_dropped` falls from 5,662 to 1,527 coins.

## 8. Composition

### 8.1 With `2026-08-25-land-value-mixed-herd` — same three files

| its task | where it collides | rule |
|---|---|---|
| Task 1 (prospective land) rewrites `free_slot` and hoists the land grant above it | `plan._derive`, the same block R1's `tile_value` floor and R3's `slot_rank` sit in | no logical conflict; **rebase before every commit and re-read the block** rather than trusting line numbers |
| Task 4 (mixed herd) rebuilds `place_rank` as one joint pass over three kinds (`_count_le(place_cum, place_rank)`) | R3 changes how `place_rank` is produced | **R3 lands after Task 4** and feeds `_rank_near`'s output into that same joint pass — the three kinds still read one rank vector |
| Task 4 takes `_pickup_kinds` from 3 to 5 | it is a second, independent cut to the same admit budget R2 corrects | today's mid-season mean is 2.6–2.8 kinds, so a unit's admit budget is 21 − 2.7 − 5 ≈ 13.3; at 5 kinds it is ≈ 11.5, another 14 %. **Re-measure `EST_LEAD` from the post-merge baseline**; the derived form `sum(task*DIST_SHED) // max(sum(task), 1)` (one extra `[100]` reduce) is the fallback if the constant stops fitting |
| Task 4 reactivates `head[2]` | R3/R4 must not use it | they append `g6`/`gb6` (R5) |
| Task 6 predicts a frozen-theta regression | R1/R2 cause one too | same treatment: fresh lineage, compared lineage-vs-lineage |
| its ~14 % throughput budget against a 15 % gate | the drain plan adds another 3 % | **R1 and R2 ship first and alone.** They are the two free ones (one `maximum`, one fewer multiply-add, two constant subtractions) and they carry +11–16k of the value. R3 (~1.5 %) and R4 (0 %) wait for the post-merge baseline. This plan's own gate is **≤10 %**; its expected cost is ≤2 %. |

### 8.2 With the residual-drain feature in `brain.features`

The feature adds a per-product column (`PJ.daily_town_units − own_pipeline − opp_pipeline`), which widens the shared encoder's input 12 → 13 and therefore **invalidates every incumbent theta's decode** — unlike R3/R4, it is a fresh lineage and must not be bundled with them in one commit if the incumbent lineage matters.

Two couplings, both about ordering:

* **Measure it after R1/R2, not before.** §4.1 shows the mix is already near a local optimum *at today's volume* — all three forced mixes lose 15–39k — so the feature's job is fine reallocation, not a mix flip. R1 raises tile-visits 23 % and base-value production with them, which is precisely when a residual drain starts to bind. Fitting the feature to the pre-R1 supply fits it to a farm that no longer exists.
* **The drain plan's own §5.0 trigger moves but does not fire.** Its volume-to-crossover fractions were milk 0.45, strawberry 0.43, wool 0.26, wheat 0.28. Scaling by R1's +23 % tile-visits puts them near 0.55 / 0.53 / 0.32 / 0.34 — still under 1.0, so **T4 still does not ship**. That is an estimate from tile-visits, not a measurement of per-product volume: re-run the trigger, do not assume it.

## 9. Test plan

### 9.1 New

`tests/test_route_traversal.py`

```python
def test_the_route_has_two_groups_not_four():
    """A board carrying mandatory, priced-optional and worthless work: every
    priced-or-mandatory tile is visited before any worthless one, and the
    serpentine position is non-decreasing inside each group -- one crossing."""

def test_a_mandatory_tile_is_never_worth_nothing():
    """`d.tile_value >= d.tier` elementwise, over 200 random views."""

def test_the_forty_weed_boards_still_work_the_mandatory_tile():
    """The three boards of test_mandatory_tier.py, through `build_day`."""

def test_the_admit_loop_converges():
    """On a board where today's route leaves admitted work unreached,
    `admitted & ~covered` is empty after ADMIT_ROUNDS."""

def test_route_arrays_agree_across_backends():
```

`tests/test_dev_locality.py`

```python
def test_compact_zero_reproduces_the_sweep_rank():
    """_rank_near(mask, zeros) == _rank(mask) on 500 random masks, numpy and
    JAX. This is the gene's inertness guarantee; if it fails, the archetype
    ladder moves and R5's zero-padding promise is void."""

def test_compact_saturated_develops_the_nearest_free_tile_first():
def test_ties_break_to_the_lower_serpentine_index():
def test_compact_decodes_to_zero_at_theta_zero():
def test_a_4386_long_theta_is_inert():
```

`tests/test_dev_weight.py` — `dev_weight == GROW_ONE` at z = 0; a saturated weight lifts a planting above a harvest in the **admission** order and never above a mandatory tile; the `v_plant * dev_w` product stays inside int32 at `VALUE_CAP`; int32 on both backends.

### 9.2 Updated — each a deliberate change, not a fix-up

Verified by running R1 as a monkeypatch over the eight test files that pin route, labour and end-of-season behaviour — `test_mandatory_tier.py`, `test_admit_route.py`, `test_task_priority.py`, `test_hire_enumeration.py`, `test_day29_endgame.py`, `test_deadline_harvest.py`, `test_planner_op_coverage.py`, `test_feed_rationing.py`: **R1 breaks exactly one behaviour test.** The full suite (and the two equivalence files) has not been run under the design; the implementer runs it.

| file | what changes |
|---|---|
| `tests/test_admit_route.py::test_the_route_sweeps_the_mandatory_tier_first` | **the one behaviour test R1 breaks.** Its watering moves from turn 11 to turn 14: two priced tiles nearer the spawn are now swept first. All three tiles are still worked. Re-derive the turn arithmetic in the docstring and re-target the assertion onto "every tile is worked, mandatory work is *admitted* first" plus the new indices. |
| `tests/test_admit_route.py` (rest) | every exact turn budget (`22 - 1 = 21` with 7 tiles admitted) moves with `EST_MOVES = 1` and `EST_LEAD = 5`. Re-derive; keep the invariants. |
| `tests/test_hire_enumeration.py` | `turns_h` gains `- EST_LEAD`; re-derive the pinned `h*`. |
| `tests/test_mandatory_tier.py` | **all six behaviour assertions pass unchanged** (verified). Only the module and `_weeds_head` docstrings need editing: the route has two tiers now, not three, and the mandatory tile leads the weeds because it is priced, not because it is mandatory. |
| `tests/test_day29_endgame.py`, `tests/test_deadline_harvest.py`, `tests/test_feed_rationing.py`, `tests/test_task_priority.py`, `tests/test_planner_op_coverage.py` | **pass unchanged** (verified). Run them anyway. |
| `tests/test_es_masking.py`, `tests/test_genome_retype.py`, `tests/test_gene_sweep.py`, `scripts/gene_sweep.py` | `N_PARAMS` 4,386 → 4,452 and two new decoded outputs. |
| `tests/test_sim_equivalence.py`, `tests/test_trained_equivalence.py`, `tests/test_backend_agreement.py` | unchanged in code, **mandatory to run** — they are the proof the numpy submission and the JAX trainer still emit the same route. |

### 9.3 Integration, with the numbers to falsify stated first

`scripts/eval_vs_baselines.py --csv --seed-base` on ≥32 matched seed pairs in **both seats** against `starter` and `../kaggriculture2/main.py`, then `scripts/paired_ci.py`. Each commit must reproduce its row of §6 inside the stated interval:

| commit | own vs `starter` | own vs `kagg2` | margin vs `kagg2` |
|---|---|---|---|
| R1 | +13,061 ± 7,932 | +11,212 ± 9,228 | +2,594 ± 8,774 |
| R1+R2 | +11,854 ± 11,233 | +15,640 ± 10,979 | +852 ± 8,151 |
| R1+R2+R3/R4 at z = 0 | **must equal R1+R2 exactly** | | |
| R1+R3, `compact` saturated | +8,391 ± 7,490 | +8,700 ± 12,873 | +14,062 ± 5,062 |
| R1+R4 at ×3 | +6,117 ± 7,179 | +4,896 ± 12,143 | +9,341 ± 4,768 |

Throughput: `scripts/bench_sim.py` before and after every commit, both numbers in the commit message. **This box's current baseline is 1,035.5 eps/s at B = 1024** (CPU, 12 cores; 362.3 at B = 256, 104.3 at B = 64). Gate **≤10 % cumulative for this plan**, re-measured against the land/herd plan's post-merge baseline rather than against this one.

### 9.4 Archetype ladder re-check — `MIN_COINS = 10,000` against the zero theta

`tests/test_archetype_ladder.py` builds a `Trainer`, which probes every named archetype against the zero theta and refuses any under `MIN_COINS` (`archetypes.py:385`, `train.py:349-380`); `reprobe_archetypes` re-runs it on `--resume` (`train.py:382-410`). **Three commits, in this order.**

**After R1/R2 — the ladder moves and every probe coin is re-recorded.** R1/R2 change the plan every zero-theta archetype walks. `test_every_archetype_clears_the_liveness_floor` and `test_mixed_ranch_is_the_eighth_slot_and_the_top_of_the_yardstick`'s `value_farmer == pytest.approx(53_568, rel=1e-3)` must both be re-measured and re-pinned to the new numbers. Pin all eight, in a table.

Prediction, stated before the run (§7's rule):

* **No rung falls below `MIN_COINS`.** R1/R2 never remove work; they cut the crossings that reach it, so a rung's admitted value is weakly larger. The rungs nearest the floor are the ones that develop nothing (`dev` strongly negative) and those are task-bound, not labour-bound — the change is inert for them.
* **`mixed_ranch` keeps the top slot and gains the most.** It is the only rung carrying `dev 10`, `free_urgency 3` and `land_cap 3`, i.e. the most development-hungry, and R1's gain is proportional to queued-but-unreached development (21.3k–36.7k coins/season on the champion).
* `value_farmer` rises from **47,550** (53,568 when this was written; the land valuation moved every rung and the ladder was recalibrated with it on 2026-08-26). **Re-pin the new figure; do not relax the assertion to an inequality** — an exact pin is what catches a later change that silently moves the yardstick.

Re-run at `n_archetypes = len(NAMES) + 4` over **≥5 seeds**, and confirm `reprobe_archetypes` still accepts a pre-R1 checkpoint (its thetas are 4,386 long and `unpack` zero-pads).

**After R3/R4 — the ladder must not move at all.** `archetype_theta` builds `np.zeros(PO.N_PARAMS)` (`archetypes.py:183`), so the appended `g6`/`gb6` block is zero, `compact = 0`, `dev_weight = GROW_ONE`, and every named archetype decodes to the same `Macro` and walks the same plan as after R1/R2. **Assert it numerically** — all eight probe coins equal to the post-R1/R2 table, not merely `min >= MIN_COINS`. If any moves, `_rank_near`'s zero case is not bit-identical to `_rank` and the gene is not inert; fix that, do not re-pin.

**A third commit, separately, for `sample_archetype`.** Do not add `compact`/`dev_weight` to the drawn knobs in the same commit as the decode. A drawn rung with a saturated `compact` and a herd is a new failure surface — it packs the structures against the shed and can leave the far half of the board unworkable — and the drawn rungs are exactly what `MIN_COINS` protects. Draw both from `[-1.5, 1.5]` and re-run the liveness probe over ≥5 seeds.

## 10. Risks

| risk | where it bites | mitigation |
|---|---|---|
| **R1 moves 0.5's LAW from the route to admission.** The sweep can now leave a mandatory tile for last if the route budget runs out mid-group | `test_mandatory_tier.py`'s adversarial boards | admission keeps `d.tier` and `n_admit` only shrinks from the value tail, so a mandatory tile is never the one cut; `ADMIT_ROUNDS = 3` then closes the gap between admitted and covered — measured, `value_dropped` falls 21,302 → 5,303 (kagg2) and 36,690 → 8,631 (starter). Watch it in `build_day_stats`. If a board is found where the loop does not converge, raise `ADMIT_ROUNDS` to 4 (one more shape-static round, ~2 %) rather than restoring the mandatory group |
| **`EST_LEAD` is a measured constant, not a bound** | R2, and again after the mixed herd takes `_pickup_kinds` to 5 | it only ever subtracts from the budget, so it under-admits and never over-admits; the days it is wrong on are task-bound (0.90–0.96 of days 0–11). Derived fallback in §8.1 |
| **The opponent's coins move with ours, and the seed does not control it** | every "own coins" figure vs `kagg2` | `kagg2` goes 113,477 → 122,095 under R1. The per-day RNG is consumed by weed spawns on every empty unlocked tile *before* `rng.choice` picks the day's shop (`kaggriculture.py:871`), so working more tiles changes the town's shop path for **both** seats. Always report the paired margin as well as own coins, and never attribute an opponent's coin change to competition alone |
| **Coins and margin disagree** | choosing between R1/R2 and R3/R4 | do not choose. R1/R2 are structural and unconditional; R3/R4 are genes, and ES resolves the trade against the pool. `GOAL.md` scores win rate |
| **Concurrent edits to `plan._derive`** | the land/herd agent owns that block | rebase before every task; §8.1's ordering rules; never trust a line number in this document without re-reading |
| **The next bottleneck is the shed, and it will look like a regression** | after R1 | under R1 the shed reaches 96–97/100 by day 26 (room 3–7) and the feed-wheat grant starts to be refused (want 2.2, got 1.0 on day 26). Shed room, not labour, is what binds after this plan — that is progress, not a defect, and it is where the *next* measurement should go |

## 11. Reproduction

Harness in this session's scratchpad (`idle/probe2.py` telemetry, `idle/exp.py` counterfactuals, `idle/agg.py` / `idle/agg2.py` / `idle/marg.py` / `idle/eos.py` analyses, `idle/rtplug.py` a pytest plugin that applies a route design to the whole suite). Nothing was added to `scripts/` and no file under `src/` was modified.

```bash
# per-day planner-internal telemetry, 8 seeds x 2 seats x 2 opponents
.venv/bin/python idle/probe2.py --theta artifacts/p2s0/champion.npy \
    --games 8 --workers 11 --patch base --out base.json
.venv/bin/python idle/agg.py base.json kaggriculture2

# the counterfactual sweep (one fresh process per game -- see section 2)
.venv/bin/python idle/exp.py --patches base rtiervm rtiervm_est1_lead rtiervm_val3 \
    --games 8 --workers 11 --out f5.json
.venv/bin/python idle/marg.py f5.json

# which pinned behaviours a route design breaks
PYTHONPATH=idle RTMODE=rtiervm .venv/bin/python -m pytest \
    tests/test_mandatory_tier.py tests/test_admit_route.py tests/test_task_priority.py \
    tests/test_hire_enumeration.py tests/test_day29_endgame.py \
    tests/test_deadline_harvest.py tests/test_planner_op_coverage.py \
    tests/test_feed_rationing.py -q -p rtplug
```

`rtiervm` is R1 exactly (mandatory value floor plus the two-group route); `rtiervm_est1_lead` is R1+R2; `rtiervm_val3` is R1+R4 at ×3; `rtiervm_near` is R1+R3 with `compact` saturated. `rtier1` (route collapsed to one group) and `boustro` (four groups, alternating direction) are the two rejected alternatives of §5/R1.

**Model caveat.** Every interval is 16 paired games, so a ±8k CI on a 65k purse is a wide instrument: the *signs* and the *large* effects (R1, the forced mixes, the mandatory-tier promotion) are safe, and the small ones (`noland4`, `feed28`, `boustro`) are pinned near zero rather than resolved. Confirm each shipping commit at ≥32 pairs before recording it.
