# Drain-aware sell reservation — design + measurement

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax. This plan composes with `docs/superpowers/plans/2026-08-25-land-value-mixed-herd.md`, which is being implemented concurrently; **read section 6 before starting.**

**Status: SPECIFIED, GATED.** The measurement below says the feature does **not** pay at kagg3's current sell volumes and *does* pay, by 244–381 %, once volume passes ~0.6× the town's season drain — which is the volume the land/herd plan exists to reach. Ship it only when the trigger in §5.0 fires.

---

## 1. Market mechanics (from the reimplementation)

### 1.1 Town drain: per product, per turn

Two consumers, both applied after every turn's market phase (`sim/rollout.py:65-71`):

```
shop   = (shops @ SHOP_CONSUME) * (step % SHOP_SELL_INTERVAL == 0)     # every 4 steps
center = TOWN_CENTER_CONSUME    * (step % TOWN_CENTER_SELL_INTERVAL == 0)   # every 24
mkt_inv -= shop + center
```

* `SHOP_CONSUME[shop, product]`, `spec.py:174-179` — single-product shops consume **2**/tick, multi-product shops **1**/tick each.
* `TOWN_CENTER_CONSUME`, `spec.py:183-184` — **1 of every product except fertilizer**, once a day.
* Intervals `spec.py:206-208`: `SHOP_SELL_INTERVAL = 4`, `TOWN_CENTER_SELL_INTERVAL = 24`, `SHOP_UNLOCK_INTERVAL = 3`.
* Shops unlock at end-of-day when `(day+1) % 3 == 0` and `nshops < 8` (`sim/eod.py:151-161`), starting from **zero** (`sim/state.py:131-132`). So `nshops` by day is `[0,0,0,1,1,1,2,…,7,8,8,8,8,8,8]` — 8 shops only from day 24.

Six shop ticks a day plus one centre tick (`core/projector.py:102-109`). **Expected season drain, random shop draw** (measured, `spec.SHOP_CONSUME.mean(axis=0)`):

| | wheat | carrot | tomato | strawb | melon | egg | milk | wool | fert |
|---|---|---|---|---|---|---|---|---|---|
| units/tick per random shop | 0.625 | 0.375 | 0.25 | 0.5 | **0** | 0.25 | 0.375 | 0.25 | **0** |
| units/day at 8 shops | 31 | 19 | 13 | 25 | **1** | 13 | 19 | 13 | **0** |
| **season total (30 d)** | **525** | **327** | **228** | **426** | **30** | **228** | **327** | **228** | **0** |

**No shop consumes melon or fertilizer.** Melon's whole season drain is the 30 town-centre ticks; fertilizer's is exactly zero. Everything below turns on this.

### 1.2 Price response to inventory

`spec.market_price` (`spec.py:134-149`), tabulated once into `price[9, 85001]` (`spec.py:293-322`), read on device by gather only:

```
inv < I0 :  price = base + below_target*base/shape(f,T,T) * shape(f, I0-inv, T)
inv >= I0:  price = base - above_target*base/shape(f,T,T) * shape(f, inv-I0, T)
price = max(1, round(price))                        # PRICE_FLOOR = 1
```

`I0 = MARKET_I0 = 10000` for every product (`spec.py:84`); the parameter rows are `spec.py:91-101`.

**"Selling above base" therefore requires exactly one thing: market inventory below 10,000 at the moment of the sale.** Units of deficit `D = I0 - inv` needed:

| | wheat | carrot | tomato | strawb | melon | egg | milk | wool | fert |
|---|---|---|---|---|---|---|---|---|---|
| D for quote > 1.00× base | 1 | 7 | 5 | 1 | 1 | 9 | 1 | 1 | 3 |
| **D for quote ≥ 1.20× base** | **21** | **84** | **96** | **8** | **284** | **158** | **14** | **99** | **98** |

Strawberry (8) and milk (14) reach 1.2× on a day and a half of drain; melon needs 284 units of a drain that yields 30 a season, i.e. **melon can never quote 1.2× base**, and fertilizer never leaves base except downward.

### 1.3 What the engine caps, and how the walk is priced

* SELL is capped at shed contents: `ncap = where(op == MO_SELL, minimum(n, shed_have), minimum(n, room))` — `sim/market.py:216-218`. `shed_have` is `shed[p, item]`, and the shed holds `SHED_CAPACITY = 100` items **in total** (`spec.py:195`), livestock included.
* The walk quotes unit *j* at `inv + j` and cumsums (`sim/market.py:50-75`). A unit sold at `PRICE_FLOOR` is paid for but **does not add to supply** (`market.py:72-74`), so the curve bottoms out rather than inverting.
* Both seats selling the same item in the same slot advance the shared inventory two units per round (`market.py:220-255`).
* The planner's sale draws on the **hour-0 shed only** (`core/plan.py:1233-1248`); today's harvest lands at end-of-day and is sold tomorrow.
* Sells resolve at turns 3/10/18, the buy/hire rows at turns 0-2 (`core/ops.py:91-105`). **No same-day sale can fund any purchase** (`docs/PLANNER_V3_1.md:347-351`) — lot proceeds carry to tomorrow. Between two lots the town removes only 2 shop ticks (`projector.ticks_before`, `projector.py:31-41`): at most 10 wheat / 8 strawberry / 6 milk, and **0 melon, 0 fertilizer**.

### 1.4 The reservation today

`brain.decide` (`core/brain.py:331-334`):

```
hold[p]  = floor(min(0.8 * _BASE[p] * softplus(sell[p])/softplus(0), COIN_CAP-1))
press[p] = floor(_BASE[p] * max(tanh(gate[p]), 0))
```

`_BASE` is a **constant read from `spec.DEFAULT_MARKET_PARAMS`** (`brain.py:24`), so under `spec.sample_market_params` the reservation is anchored to a price the market no longer has. `hold` crosses base at logit ≈ +0.32. `sell.allocate` (`core/sell.py:80-118`) gates each unit on `best_adj >= hold`, with `hold <= LIQUIDATE = -COIN_CAP` the day-29 mode (`sell.py:21-29, 48`; `plan.py:1255`). Shed overflow is force-sold past the reservation (`plan.py:1264-1355`).

---

## 2. Measurement — is the feature worth it?

All numbers: JAX sim, CPU, seeds 0/1/3/7 × both seats (8 games) unless stated.

### 2.1 What kagg3 actually realizes today

`mixed_ranch` vs the zero theta, revenue attributed by replaying the quote walk from the pre-lot inventory:

| | wheat | carrot | tomato | strawb | melon | egg | milk | wool | fert | total |
|---|---|---|---|---|---|---|---|---|---|---|
| units/season | 36 | 73 | 68 | 70 | **167** | 12 | 37 | 99 | **170** | 745 |
| revenue | 1,740 | 3,305 | 5,212 | 19,372 | **31,744** | 463 | 13,080 | 20,516 | **10,100** | **105,532** |
| realized price / base | **1.92** | 1.30 | 1.27 | **2.30** | **0.76** | 0.81 | **2.21** | 1.04 | **0.59** | 1.05 |

**The premise in `es/archetypes.py:85-96` is half wrong.** kagg3 does *not* dump at or below base — it realizes **1.05× base overall** and 1.9–2.3× on wheat, strawberry and milk, because the town drains those markets faster than kagg3 can fill them. Market inventory ends **below** its opening level on six of nine products (`endInv − I0`: wheat −718, strawberry −346, milk −442, wool −122, carrot −126, tomato −160), and the closing quotes are 1.2–2.3× base — the same signature the autopsy attributed to kagg2.

The whole loss is in the two products the town does not consume: **melon at 0.76× and fertilizer at 0.59× base, 40 % of revenue**. No reservation can fix those — their quote never recovers, so holding a unit costs a shed slot and buys nothing.

The trained incumbent is worse in exactly the same place. `artifacts/p2s0/best_abs.npy` vs `mixed_ranch`: melon ends at `I0 + 158`, **quote 0.00× base ($1 floor)**; fertilizer at `I0 + 360`, 0.28×.

### 2.2 ES has already searched the `hold` axis and returned zero

Decoded `hold / base`, per product:

| theta | day 3 | day 27 |
|---|---|---|
| zero (spec init posture) | 0.80 × 9 | 0.80 × 9 |
| `mixed_ranch` (`hold` knob −1) | 0.34–0.36 | 0.34–0.36 |
| **`p2s0/best_abs` (trained)** | **0.00–0.067** | **0.04–0.108** |

Thousands of generations against archetypes drawing `hold ∈ [−6, +6]` drove the trained reservation to **3–11 % of base**. Shifting `b2[1]` by +0.5 or +1.0 on `p2s0` changes **nothing** — final coins 93,374 / 93,374 / 93,370, every per-product volume identical to the tenth of a unit. The positive half of the knob is not merely unused; it is unreachable from where ES has settled.

### 2.3 Raising the reservation costs coins, and starves the farm

`mixed_ranch` vs zero, `hold` logit swept (8 games):

| hold logit | coins | sell revenue | morning spend | min cash after buys |
|---|---|---|---|---|
| −1.0 (shipped) | **74,855** | 100,895 | 29,040 | 5 |
| 0.0 | 74,536 | 100,565 | 29,029 | 5 |
| +0.8 | 66,691 | 89,402 | 25,711 | 5 |
| +1.5 | **38,469** | 44,922 | **9,453** | 4 |

At +1.5 the farm stops selling milk, wool, egg and fertilizer **entirely**, revenue halves, and the morning spend collapses to a third — the starvation the archetype docstring describes, reproduced.

### 2.4 A per-product reservation, on its own, buys nothing

Nine sharp bands on the value feature give an exact per-product `hold` vector. `mixed_ranch` vs zero, 8 games:

| reservation | coins |
|---|---|
| baseline (`hold` −1) | 74,536 |
| uniform 0.0× base (sell everything) | 74,883 |
| uniform 1.0× base | 41,593 |
| uniform 1.2× base | 37,442 |
| **1.0× on the seven drained products, dump melon + fert** | 74,417 |
| 1.1× / 1.2× / 1.4× on drained, dump melon + fert | 68,236 / 70,339 / 69,776 |
| 1.1× or 1.3× on wheat/strawberry/milk only | 74,883 (identical to 0.0×) |

The last row is the diagnostic: a 1.3×-base reservation on wheat, strawberry and milk **never binds**, because kagg3 already realizes 1.9–2.3× on them. Splitting melon and fertilizer out recovers the cash the uniform reservation destroyed (74,417 vs 41,593) but beats the dumping baseline by **nothing**.

Repeated on the biggest board reachable today — `p2s0/best_abs` vs `mixed_ranch` on a 4-quadrant / 20,000-coin warm start (`sim/state.initial_state`) — the split is worth **+664 to +673 coins, ≈ +1.2 %**, over the same-probe dumping control (56,848 → 57,467/57,512/57,521 at 1.0×/1.2×/1.5×). *Caveat, stated because the absolute numbers look wrong:* the nine-band probe overwrites encoder hidden units 20–37, which are trained weights in `p2s0` but zero in an archetype, so the warm-start row's **level** (56.8 k against the untouched theta's 89.1 k) is probe damage, not a finding. Only the differences within that row are valid, and the `mixed_ranch` table above — where the probe touches nothing the archetype uses — is the clean measurement. Per-product volumes there are still short of §2.5's crossovers: strawberry 117/270, milk 55/180, wool 81/150, wheat 102/360.

### 2.5 Where it does pay: the volume crossover

Single-product, 30-day model against the real drain schedule and the real table. "flat" = V/30 a day (what a zero reservation does with steady production); "drain-paced" = at most that day's drain, remainder pushed to day 29.

| product | season drain | **crossover V** | V / drain | gain at V = 2× drain |
|---|---|---|---|---|
| wheat | 525 | 360 | 0.69 | +10 % |
| carrot | 327 | 180 | 0.55 | +44 % |
| tomato | 228 | 120 | 0.53 | +51 % |
| **strawberry** | 426 | **270** | 0.63 | **+274 %** |
| melon | 30 | 60 | 2.00 | +1 % |
| egg | 228 | 120 | 0.53 | +9 % |
| **milk** | 327 | **180** | 0.55 | **+381 %** |
| **wool** | 228 | **150** | 0.66 | **+243 %** |
| fertilizer | 0 | never | — | 0 % |

**Rule: pacing starts paying at V ≈ 0.6 × the product's season drain, and is worth 2.4–3.8× at 2× drain.** Below the crossover, pacing is *worse* than flat — it front-loads the sale into the early season, when nothing has drained yet and the quote is still at base.

kagg3's own volumes against those crossovers (p2s0 vs mixed_ranch, per seat): strawberry 144/270 = 0.53, milk 148/180 = **0.82**, wool 51/150 = 0.34, wheat 59/360 = 0.16. **Milk is one land purchase away from the crossover; the rest are two to six times short.**

Ceiling, for scale: the town's whole season absorption priced at base is **206,190 coins** across both seats (525·25 + 327·35 + 228·60 + 426·120 + 30·250 + 228·50 + 327·160 + 228·200). kagg2 books 179,249 of it. Its edge is **volume on the drained, high-value products**, not price.

### 2.6 What a cash-constrained herd farm needs each morning

`mixed_ranch` vs zero, seed 0, coins committed at turns 0-2 (hire + buy row) versus the purse left after them:

| | value |
|---|---|
| morning bill, mean / median / p90 / max | **1,087 / 437 / 2,364 / 10,993** |
| cash after the buy row, min | **5 coins** |
| days with cash after buys < 500 | **18 of 30** |
| current reserve `HIRE_BILLS[n_hire+1]` at 13 hands | **986** (`plan.cash_reserve`, `plan.py:282-323`) |

The bill is bimodal: 0–200 coins on the 12 pre-herd days, then 1,000–2,900 through the build-out, with one 10,993 spike (day 14, the herd purchase). The existing reserve covers the **crew only** — it does not model seeds, feed wheat or animals, and it is the *whole* liquidity model the planner has. **Minimum liquidation to keep a herd farm solvent is therefore its own previous morning's bill: median 437, p90 2,364, worst case 11,000 coins.** That is the floor any positive reservation must clear before it withholds a unit, and it is the mechanism behind §2.3.

### 2.7 Verdict

The feature as an income improvement at today's volumes: **no** — every reachable positive reservation is neutral (−0.2 %) or costly (−8 % to −49 %). The feature as a **precondition for the volume the land/herd plan is chasing**: yes, worth +244 % to +381 % on strawberry/milk/wool once volume passes 0.6× drain. Build the mechanism, ship it inert, and turn it on against the trigger in §5.0.

---

## 3. Design

Three parts. Every one is zero at zero theta, so every incumbent decodes byte-identically.

### 3.1 Re-type the reservation onto the projected next-opportunity quote

The defect is not the *level* of `hold` but its **anchor**: `0.8 · base · softplus(sell)` prices "keep this unit" against a constant, while the thing it must beat is a quote that moves ±100 % over a season and moves in opposite directions for strawberry and fertilizer. One reservation vector cannot say "hold strawberry, dump fertilizer" — which is why §2.4's split needed nine hand-set bands, and why ES settled at ~0.

Add a **drift** term: the coins one unit gains by waiting for its next opportunity.

```python
# core/brain.py, decide(), after `hold` is computed
inv_now  = PJ.projected_inv(xp, obs.mkt_inv, obs.shops, O.SELL_TURNS[-1])   # today's last lot
inv_next = PJ.inv_at_day(xp, obs.mkt_inv, obs.shops, 1) + obs.shed[:NP_]    # tomorrow, own stock ahead
q_now    = price_table[pid, clip(inv_now  - PRICE_TABLE_LO, 0, N-1)]
q_next   = price_table[pid, clip(inv_next - PRICE_TABLE_LO, 0, N-1)]
patience = PATIENCE_MAX * xp.maximum(xp.tanh(out.drift), 0.0)     # [9], 0 at zero theta
hold     = _qfloor(xp, xp.clip(hold + patience * (q_next - q_now), 0, spec.COIN_CAP - 1)).astype(i32)
```

* `PJ.inv_at_day` and `PJ.projected_inv` already exist (`core/projector.py:44-60, 112-118`) and `_candidates` already calls `inv_at_day` on the buy side (`plan.py:579`), so the drain projection is machinery the day already pays for.
* `+ obs.shed[:9]` is the **self-limiting** term: a farm holding 40 strawberries quotes tomorrow's marginal 40 units deeper, so the reservation falls as the hoard grows. Documented approximation — it assumes today's whole stock is also sold tomorrow, which is conservative in the right direction.
* `PATIENCE_MAX = 5` (days of drift). Measured drift per day at the default table: strawberry +5, milk +5, wool +1..2, wheat +1, **melon +1 early → +0.3 late, fertilizer exactly 0**. So the same gene value means "hold strawberry" and "dump fertilizer" with **no per-product weight at all** — the shape comes from `SHOP_CONSUME`, not from theta.
* `brain.decide` needs the price table. It does not have one today. Pass it: `decide(xp, theta, obs, price_table=None)`, defaulting to `P.default_price_table()` (`plan.py:529`, already cached; `brain` already imports `plan as P` at `brain.py:18`, so no new import). **The one required call-site change is `sim/rollout.py:138`, which must pass `tables.price`** — training randomises the market (`spec.sample_market_params`) and the default table would be the wrong one. The other three call sites (`scripts/package_submission.py:119`, `plan_stats.py:41`, `validate_sim.py:33`) all run the default table and need no edit; the shipped `main.py` template is therefore unchanged, which keeps `test_submission_runs.py` and `test_trained_equivalence.py` honest.
* Bonus, free: because the drift reads the *actual* table, the reservation gains a component that tracks a randomised market, where `hold`'s `_BASE` anchor (§1.4) does not.
* `brain` needs `from . import projector as PJ`. No cycle: `projector` imports only `spec`, and `brain` already reaches it transitively through `plan`.
* `q_now` uses the **last** lot's projected inventory because `hold` is one scalar per product compared against `max` over the three lots' adjusted marginals (`sell.py:113-116`) — the last lot is the best today can do, so the drift measures waiting a day against today's *best*, not today's first.

**Cost note.** This is the only change that makes the positive half of the reservation reachable; it is worth nothing on its own until §5.0's trigger fires, and it is worth nothing to `mixed_ranch` (drift on melon+fert ≈ 0 and on the rest the reservation already never binds).

### 3.2 A liquidity floor inside the allocator

§2.3 and §2.6 say a reservation that withholds cash kills the farm before it earns a coin. The floor:

```python
# core/plan.py, _plan_and_stats, before SELL.allocate
# Today's own bill is the estimate of tomorrow's; today's sale is the only
# thing that can fund it (no same-day sale funds a purchase, PLANNER_V3_1 1.2).
spend_today   = (bills[n_hire] + granted purchase cost)      # already a local of `_derive`
cash_floor    = xp.where(terminal, 0, spend_today + cash_reserve(xp, n_hire, day))
liquidity_need = xp.maximum(cash_floor - purse_left_after_buys, 0).astype(i32)
lots = SELL.allocate(..., hold, macro.press, inv_lots=inv_lots, need=liquidity_need)
```

and in `sell.allocate`'s body, one extra scalar carry:

```python
def body(carry):
    lots, rev = carry
    adj, nxt = adjusted_marginals(xp, price_table, inv_lots, lots, press)   # nxt now returned
    best, best_adj = xp.argmax(adj, 0), xp.max(adj, 0)
    take = (xp.sum(lots, 0, dtype=i32) < avail) & ((best_adj >= hold) | liquidate | (rev < need))
    got  = xp.take_along_axis(nxt, best[None, :], 0)[0]
    return lots + ((lot_ix == best[None, :]) & take[None, :]).astype(i32), \
           rev + xp.sum(xp.where(take, got, 0), dtype=i32)
```

* `need = 0` (the default, and every existing caller) makes `rev < need` false on every round, so the allocation is **bit-identical to today's**. That is the regression that protects every incumbent and every archetype.
* Order: the greedy takes the highest adjusted marginal first, so the floor is met with the **fewest units**. For a farm whose binding constraint is 100 shed slots that is the right objective; document it rather than reversing it.
* `adjusted_marginals` gains a second return value. Two call sites (`sell.allocate`, `plan.py:1334`) plus `tests/test_sell_allocator.py`.
* The floor is void on the terminal day, where `hold = LIQUIDATE` already sells everything (`plan.py:1255`).

### 3.3 The gene

One appended encoder head, following the layout rule at `core/policy.py:66-68` ("every theta trained before this block is a prefix and unpacks with it zeroed", `unpack` zero-pads, `policy.py:113-126`):

```python
SHAPES += [("w4", (N_ENC_HID, 1)), ("b4", (1,))]        # +65 params: 4,386 -> 4,451
Outputs += drift: object        # [9], pre-activation, = (h @ p.w4 + p.b4)[:, 0]
```

* Per-product, off the **shared** encoder — same construction as `press` (`w3`/`b3`, `policy.py:70-72`), so it reads `base`/`T`/`above_target`/`demand` off its inputs rather than memorising the table, which is what makes `sample_market_params` bind (GOAL.md).
* `patience = 5 · max(tanh(drift), 0)`: exactly 0 at zero theta, one-sided and saturating like `press`, so the same test shape applies.
* `live_mask()` leaves it live; `N_DEAD` stays 825, `N_PARAMS` moves 4,386 → 4,451.
* `es/archetypes.py`: add `"patience"` to `KNOBS` (`archetypes.py:129`) and write it as `theta[PO.offset("b4")] = knobs.get("patience", 0.0)`, exactly as `press` uses `b3` (`archetypes.py:210`). **Do not add it to `sample_archetype` in the same commit** — see §5.

### 3.4 Shed overflow

Unchanged (`plan.py:1264-1355`). A higher reservation lowers `s_qty`, which *raises* `spare = avail - s_qty`, so the forced sale has strictly more to draw on and `overflow_destroyed` cannot rise. The overflow path ranks by ascending marginal quote, so a hoarding farm gives up its melon/fertilizer pile first — which is correct. Assert both properties (§5).

### 3.5 Throughput

Budget **≤ 3 %**, gate at 5 %, measured with `scripts/bench_sim.py 1024` on the training host, before and after, in every commit message.

| addition | cost |
|---|---|
| `w4`/`b4` encoder head | one `[9,64]·[64,1]` matvec = 576 MAC against the encoder's 20,736 |
| `inv_at_day(…, 1)` + two `[9]` gathers | ~30 flops; `_candidates` already calls `inv_at_day` (`plan.py:579`) |
| `allocate` revenue carry | one 9-wide `where`+`sum` and two scalar ops × 100 rounds, against `adjusted_marginals`' ~200 element-ops × 100 rounds → **+13 % of `allocate`** |

`allocate` is ~5 % of episode throughput (`plan.py:1326-1331` records a **second** full allocator pass at −5.2 %), so the carry is ≈ **−0.7 %**. Fallbacks, in order: (a) drop the `+ obs.shed` self-limit (one gather); (b) replace the in-loop revenue carry with a pre-pass that sets `hold = LIQUIDATE` on the single cheapest-marginal product when `liquidity_need > 0` — coarser, zero rounds cost.

---

## 4. Tasks

- [ ] **T1 — the gene, inert.** Append `w4`/`b4` to `policy.SHAPES`; add `drift` to `Outputs`/`forward`; `brain.decide` computes `patience` and adds `patience * (q_next - q_now)` to `hold`; thread `price_table` into `decide`. `archetypes.KNOBS` gains `"patience"`, `archetype_theta` writes `b4`. **Nothing else changes.** Gate: every existing test passes untouched, `test_archetype_ladder` probe coins identical to the pre-change table, bench ≤ 1 %.
- [ ] **T2 — the liquidity floor.** `adjusted_marginals` returns `(adj, nxt)`; `allocate` gains `need=0`; `_plan_and_stats` computes `liquidity_need` from `_derive`'s spend and `cash_reserve`. Gate: `need = 0` is bit-identical, bench ≤ 3 % cumulative.
- [ ] **T3 — measure the trigger.** Re-run §2.5's volume check against the land/herd plan's output (`scripts/eval_vs_baselines.py --stats`, per-product season volume). If no product clears 0.6 × its season drain, **stop here** — T4 stays unshipped and the mechanism sits inert.
- [ ] **T4 — retune, only past the trigger.** Sweep `patience` on `mixed_ranch` and on the incumbent (`scripts/gene_sweep.py`, extended to the new block); add `patience` to `sample_archetype`; re-record every archetype probe coin.

---

## 5. Test plan

### 5.0 The trigger (T3 gate)

Per product, over 8 games in both seats: **own season sell volume ≥ that product's crossover**, where crossover = 0.53–0.69 × the *realised* season town drain (§2.5). Compute the drain as `PJ.daily_town_units` summed over the realised `nshops` path — measure it, do not assume the random-draw expectation, because the shop draw swings wheat's season drain from 525 (expected) to 849 (measured, seed 0).

Today (p2s0 vs mixed_ranch, per seat), volume as a fraction of crossover: milk **0.82** (148/180), strawberry 0.53 (144/270), wool 0.34 (51/150), wheat 0.16 (59/360). **T4 does not ship until at least two products reach 1.0.**

### 5.1 New — `tests/test_drain_reservation.py`

1. Zero theta decodes `hold == floor(0.8·base + QUANT_EPS)` on every obs, unchanged from `test_genome_retype.py:53-59`, and `test_the_initial_policy_sells` (`test_genome_retype.py:61-69`) still holds.
2. A `N_PARAMS_LEGACY`-length and a 4,386-length theta zero-pad to the *same* `Macro` as their padded selves (extends `test_genome_retype.py:86`).
3. `drift[FERTILIZER] == 0` for every `shops` vector — `daily_town_units[I_FERT] == 0` (`test_seed_horizon.py:29` already pins the row).
4. `drift[MELON]` equals exactly one centre tick's worth of quote.
5. One yarn store: `hold[WOOL] > hold[FERT]` at equal `sell`, at equal `patience`, with **no per-product theta term**.
6. `hold` is non-decreasing in `patience` on the seven drained products and `hold >= 0` everywhere; `patience` saturates one-sided like `press` (`test_genome_retype.py:71-78`).
7. Self-limit: raising `obs.shed[STRAWBERRY]` lowers `hold[STRAWBERRY]`.
8. numpy/JAX agreement on `hold` and on `allocate` (mirrors `test_sell_allocator.py:220-246`).

### 5.2 Extended

* `tests/test_sell_allocator.py` — `adjusted_marginals` returns `(adj, nxt)` with `nxt == PJ.marginal_quote` per lot; **`need = 0` reproduces every existing fixture bit-for-bit**; `need > 0` with a reservation above every marginal sells exactly enough to reach `need` and takes the highest adjusted marginals first; `need` above the whole shed's value sells the shed and terminates.
* `tests/test_sell_side.py` — day 29 still liquidates under both the drift and the floor (`:93-104`); feed wheat and fertilizer reservations survive a liquidity sale (`:87`).
* `tests/test_overflow_forced_sale.py` — high `patience` raises `deficit` but `overflow_destroyed` does not rise, and the forced walk still drains in ascending marginal value (`:108`).
* `tests/test_cash_reserve.py` — re-run `test_a_spend_everything_theta_is_never_stranded_for_the_season` and `test_the_farm_can_always_re_field_yesterdays_crew` (`:224`, `:248`) with a **high-`patience`** theta. This is the direct regression on §2.3's starvation: `hands[LAST_SHED_DAY] >= 1` and longest bare run ≤ 10.
* `tests/test_es_masking.py:26-36` — `m.shape == (4451,)`; `dead == 825` unchanged (the new block is live).
* `tests/test_genome_retype.py:86` — `SHAPES[-2:]` is now `["w4", "b4"]`, and a 4,386-long theta is inert.
* `scripts/gene_sweep.py` — `GENE_NAMES` covers the new block, or the sweep range is extended.

### 5.3 The archetype ladder re-check

`tests/test_archetype_ladder.py` runs `Trainer(...)` which probes every named archetype against the zero theta and refuses any under `MIN_COINS = 10,000` (`archetypes.py:385`, `train.py:349-380`), and `reprobe_archetypes` re-runs it on `--resume` (`train.py:382-410`). Two commits, in this order:

**After T1/T2 — the ladder must not move at all.**
- `archetype_theta` builds `np.zeros(PO.N_PARAMS)` (`archetypes.py:183`), so the appended block is zero → `patience = 0` → every named archetype decodes identically. Assert it *numerically*: pin all eight probe coins in a table, not just `min >= MIN_COINS`. `test_mixed_ranch_is_the_eighth_slot_and_the_top_of_the_yardstick` already pins `value_farmer` and `mixed_ranch == max` (`:81`) — both must pass **unedited**. (The pin is **47,550**, not the 53,568 written here on 2026-08-26: the land valuation moved every rung and the ladder was recalibrated with it. "Unedited" means unedited *by this plan's work* — a pin that moves when the planner moves is doing its job.)
- `need = 0` on every archetype (they are not liquidity-constrained by the new path unless `patience > 0`), so `test_every_archetype_clears_the_liveness_floor` is unchanged.
- `reprobe_archetypes` must accept a pre-T1 checkpoint: its thetas are 4,386 long and `unpack` zero-pads (`test_a_restored_archetype_set_is_re_probed_and_can_be_refused`, `:98`).
- `scripts/train.py:40-44` refuses a theta whose length ≠ `N_PARAMS`; confirm the documented cold-start message still fires and `--warm-trunk` still works (`test_es_masking.py:75`).

**After T4 — the ladder moves and every number is re-recorded.**
- Re-measure and re-pin all eight probe coins. `mixed_ranch` must stay `max(coins)`.
- Adding `patience` to `sample_archetype` changes every drawn rung. `test_extra_archetypes_are_sampled_deterministically_from_the_seed` (`:42`) only checks determinism and still passes, but `test_every_archetype_clears_the_liveness_floor` must be re-run at `n_archetypes = len(NAMES) + 4` over **at least five seeds** — a drawn rung with high `patience` and a herd is exactly §2.3's 38,469-coin failure and can fall under 10,000. Mitigation, mirroring the existing rule that "every named archetype with `hold > 0` keeps `animal_share <= -1.5`" (`archetypes.py:105-112`): draw `patience` from `[0, 1.5]`, and only where `animal_share <= -1.5`.
- Re-run `scripts/ladder.py` and `scripts/eval_vs_baselines.py` against the real engine.

---

## 6. Risks

**R1 — the land/herd plan owns the throughput budget.** `2026-08-25-land-value-mixed-herd.md` budgets ~14 % against its own 15 % gate (its Tasks 1–5 at <1/3/4/6/0 %). This plan's 3 % takes the cumulative to ~17 %. **Sequence after it and re-measure from its post-merge baseline**, and treat §3.5's two fallbacks as expected, not contingency. If both plans land in full and the total exceeds 15 %, fallback (b) — the coarse cheapest-product liquidity pre-pass — removes this plan's whole in-loop cost.

**R2 — the concurrent plan's provisional `allocate` pass.** Its Task 3 adds a *second* `sell.allocate` call over `avail_prov` to project lot-1 revenue and decide land affordability (its `:264`, `:287`). That call passes `macro.hold`. A drain-aware `hold` therefore moves `rev1`, which moves whether land is bought. Two consequences: the land decision inherits the reservation's noise, and the provisional pass must be given `need = 0` (never the real `liquidity_need`), or the projection and the real allocation disagree. Both call sites must be updated in one commit.

**R3 — double-counting the cash reserve.** The concurrent plan pins a purse ordering LAW — `hire_bill`, then the reserve ("never spendable by anything below it"), then `land_cost`, then the greedy — and states "**do not add a second reserve model to `brain`**" (its Task 5). §3.2 obeys this: the floor lives in `plan._plan_and_stats`, reads the *existing* `cash_reserve` and the *existing* spend, and adds no second model. It must not migrate into `brain.decide`. If it ever does, `spend_today` and `cash_reserve` would both be charged against the same coins and the farm would over-sell.

**R4 — the mixed herd makes the failure mode worse before it makes it better.** The concurrent plan's Task 4 turns one animal kind per day into three, so the feed bill becomes heavier and multi-kind — precisely the mechanism `archetypes.py:89-93` blames for a positive `hold` starving the farm, and precisely what §2.3 measured. §3.2 is the antidote and must land in the *same* release as any nonzero default `patience`, never after it.

**R5 — both sides dripping: who gets the drain?** The drain is a shared, non-storable resource: 525 wheat and 426 strawberry a season, first-come. If both seats hold above base, the town's absorption goes to whoever sells **earlier in the turn order**, and lot 1 (turn 3) beats lot 3 (turn 18) by the whole day's drain. The allocator's tie-break already falls to the earliest lot (`sell.py:113-116`, `test_sell_allocator.py:53`), and `press` exists exactly to price this (`brain.py:334`). Two failure shapes to watch for: (i) a mutual stand-off where both seats hold, the drain lifts the price, and the *shed* forces both to dump on the same day — the forced-sale path then meets a doubled supply and both get the worst curve of the season; (ii) self-play collapse, where the pool learns to hold because its clones hold. Mitigation: `press` must be swept jointly with `patience` in T4, and the archetype ladder must retain at least three dumping rungs (`rusher`, `staple_bulk`, `value_farmer` all keep `hold <= -1`) so a holding policy is never trained only against holders.

**R6 — the premise this plan was opened on is wrong, and the doc that states it should be corrected.** `es/archetypes.py:85-96` says kagg3 "dumps at/below base". §2.1 measures 1.05× base overall and 1.9–2.3× on wheat/strawberry/milk, with inventory ending below `I0` on six of nine products — the same signature the autopsy read off kagg2's tape. The real gap to kagg2 is volume on the drained products plus a 40 %-of-revenue leak into melon and fertilizer, the two products with **zero shop demand**. That leak is a *grow*-side decision (`plan._candidates` already discounts the melon curve by own pipeline, `plan.py:576-590`, yet `mixed_ranch` still plants 167 melon at `grow_mult` 4×), not a sell-side one. Amend the docstring when T1 lands.
