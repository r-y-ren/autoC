# kagg3 vs kagg2 — where the 70k goes

**Status: MEASUREMENT, no code changed.** Real engine, 48 games. This supersedes two
claims that earlier docs stand on: that `kagg2` wins by keeping supply under the drain
and selling above base (it does not — it realises **0.890× base** against us), and that
the melon/fertilizer leak is the loss (it is 29 % of it; **milk + strawberry are 83 %**).

---

## 0. What was run

| | |
|---|---|
| Agent | **`artifacts/p2s0/champion.npy`** — 4,386 params, the best theta present on this machine |
| Opponents | `starter` (engine built-in) and `../kaggriculture2/main.py` |
| Games | 12 seeds × 2 seats × 2 opponents = **48**, seed base 20260825, `kaggle_environments` on CPU |
| Telemetry | engine monkeypatched in-process (`_commit_unit`, `_process_market`, `_town_consume`, `_do_hire`, `_do_buy_land`): every committed market unit with its realised price, per-turn market inventory, per-day farm/shed/tile state for **both** seats |

Local checkpoint survey, 6 games vs `starter`, so the choice is on the record:
`p2s0/champion` **116.2k** > `p2s0/theta` 104.3k > `p2s0/best_abs` 97.2k >
`backup/remote/work1/measured/work1_g7240` 18.4k > `arch1.remote/best_abs` **8.3k**
(trained pre-Phase-2, does not decode against this planner). The remote `esfix1` /
`comb1` checkpoints at 137–151k are not on this machine and the host is out of scope, so
every number below sits **~12–15 % below the tracker's best lineage** (132.2k vs starter
here against esfix1's 150.8k) and the ratios, not the levels, are what transfer.

## 1. Headline

| | kagg3 | opponent | n |
|---|---|---|---|
| vs `starter` | **132,211** (sd 21,547) | 3,448 | 24 |
| vs `kagg2` | **62,046** (sd 15,621) | **111,035** | 24 |
| margin vs kagg2 | **−48,988** (sd 14,182) | best −25,842, worst −74,287 | **0 / 24 wins** |

Paired by seed **and** seat, the gap is **70,164 ± 6,087** (95 % CI 58,235 … 82,094).
No seat bias (seat 0 60,328 / seat 1 63,765).

**The ledger closes exactly**, which is what makes the rest of this document arithmetic
rather than interpretation:

```
                    3000 + sell revenue - market buys - hire - land = final coins
kagg3 vs starter    3000 +      168,767 -      25,508 -  7,048 - 7,000 = 132,211  ✓
kagg3 vs kagg2      3000 +       90,312 -      20,132 -  4,134 - 7,000 =  62,046  ✓
kagg2 (vs kagg3)    3000 +      156,252 -      37,907 -  5,977 - 4,333 = 111,035  ✓

GAP 70,164 = revenue lost 78,455 - spend avoided 8,291
```

The 8,291 of "saved" spend is a symptom (a poorer farm buys less), not a gain.

## 2. The single most important fact: kagg2's production is invariant, only its price moves

`kagg2` is a tape. Measured against `starter` (16 games) and against us (24 games):

| kagg2 | units sold | **base value** of the book | realised | **multiple** | final coins |
|---|---|---|---|---|---|
| vs `starter` | 1,707 | **174,163** | 216,228 | **1.242** | **170,553** |
| vs kagg3 | 1,731 | **175,516** | 156,252 | **0.890** | **111,035** |

It grows the same 175k of base value either way (±0.8 %). **kagg3 already denies it
59,976 coins of revenue and 59,518 of coins** — 35 % — purely by co-supplying the same
markets. Denial is not a new idea to be invented; it is the only thing currently working.

And it does **not** sell above base against us. Its per-unit realisations:
wheat 1.66×, carrot 1.29×, strawberry **0.99×**, melon 0.79×, milk **0.71×**, wool 0.95×,
fertilizer 0.58×. kagg3's are *higher* on strawberry (1.25×), milk (0.90×) and wool
(1.03×). **kagg2 does not take the better side of the quote; it sells 1.74× the units.**

## 3. Attribution of the 70,164

### (a) Revenue lost to lower quotes — **−49,031, 62 % of the revenue gap**

Write revenue as `base value produced × realised multiple`:

| | base value | multiple | revenue |
|---|---|---|---|
| kagg3 vs starter | 125,756 | **1.342** | 168,767 |
| kagg3 vs kagg2 | 103,831 | **0.870** | 90,312 |

```
price effect        103,831 × (0.870 − 1.342) = −49,031
production/mix      (103,831 − 125,756) × 1.342 = −29,424
                                          total = −78,455
```

Per product (units, revenue, realised/base; `d_vol` at the old unit price, `d_price` at
the new volume):

| product | u@starter | rev | p/base | u@kagg2 | rev | p/base | **Δrev** | Δvol | Δprice |
|---|---|---|---|---|---|---|---|---|---|
| **MILK** | 218.5 | 55,573 | 1.59 | 137.9 | 19,832 | **0.90** | **−35,740** | −20,489 | −15,252 |
| **STRAWBERRY** | 212.5 | 51,013 | 2.00 | 143.0 | 21,401 | **1.25** | **−29,613** | −16,684 | −12,928 |
| MELON | 91.6 | 22,071 | 0.96 | 60.8 | 7,564 | **0.50** | −14,507 | −7,431 | −7,076 |
| FERTILIZER | 237.9 | 17,763 | 0.75 | 209.4 | 9,723 | **0.46** | −8,040 | −2,125 | −5,915 |
| TOMATO | 30.7 | 2,458 | 1.34 | 30.0 | 2,230 | 1.24 | −228 | −53 | −175 |
| WOOL | 54.8 | 13,509 | 1.23 | 74.1 | 15,229 | 1.03 | +1,719 | +4,757 | −3,037 |
| WHEAT | 88.4 | 2,459 | 1.11 | 137.9 | 4,664 | 1.35 | +2,205 | +1,377 | +827 |
| CARROT | 74.5 | 2,590 | 0.99 | 114.8 | 4,719 | 1.17 | +2,129 | +1,400 | +729 |
| EGG | 20.1 | 1,331 | 1.33 | 87.9 | 4,949 | 1.13 | +3,619 | +4,492 | −873 |
| **TOTAL** | 1,028.8 | 168,767 | **1.34** | 995.7 | 90,312 | **0.87** | **−78,455** | −34,756 | −43,699 |

**Milk + strawberry are −65,353 of −78,455 (83 %).** Melon + fertilizer are −22,547
(29 %); the five other products give back +9,444. The `2026-08-26-drain-aware-reservation`
premise — "the loss is melon 0.76× + fertilizer 0.59×" — was measured against an
*archetype*, where nobody contests milk and strawberry. Against kagg2 it is second-order.

### (b) Volume kagg3 fails to sell — **zero. It is a mix shift, not a shortfall.**

kagg3 sells **996 units vs kagg2 and 1,029 vs starter** — the same. Nothing is stranded:
end-of-season unsold products **0.0 units in both matchups**, `overflow_destroyed` 0 (vs
kagg2) and 4 (vs starter), shed peaks at 92/100.

What moves is *which* units. Base value by product, starter → kagg2:
strawberry −8,340, milk −12,886, melon −7,708, fertilizer −2,846; wool +3,859, egg
+3,390, carrot +1,410, wheat +1,238. Net **−21,925 of base value on the same tile
count** — the planner's grow scores read the collapsed milk/strawberry quotes and
substitute into wool/egg/carrot/wheat, which is locally rational and globally
value-destroying. Concretely the herd flips:

| d29 herd | goose | cow | sheep |
|---|---|---|---|
| kagg3 vs starter | 0.5 | 9.6 | 4.1 |
| **kagg3 vs kagg2** | **3.8** | 4.1 | 2.0 |
| kagg2 | 0.0 | 8.6 | 5.3 |

A goose yields 4 egg/day ≈ **224 coins/animal-day** at the realised egg price; a cow
6 milk/2 days ≈ 432; a sheep 6 wool/3 days ≈ 412. kagg2 buys **no geese, ever**.

The supply/drain balance is what sets those quotes (mean units/game, vs kagg2):

| product | k3 sells | k2 net supply | realised drain | **excess** | end inv − I0 | k3 p/base |
|---|---|---|---|---|---|---|
| WHEAT | 137.9 | +58 | 492 | −377 | −377 | 1.35 |
| CARROT | 114.8 | +11 | 329 | −203 | −203 | 1.17 |
| TOMATO | 30.0 | **0** | 218 | −188 | −188 | 1.24 |
| EGG | 87.9 | **0** | 249 | −161 | −161 | 1.13 |
| WOOL | 74.1 | +169 | 282 | −39 | −58 | 1.03 |
| **STRAWBERRY** | 143.0 | **+242** | 330 | **+55** | +21 | 1.25 |
| **MILK** | 137.9 | **+248** | 307 | **+79** | +45 | 0.90 |
| **MELON** | 60.8 | +120 | 30 | **+150** | +148 | 0.50 |
| **FERTILIZER** | 209.4 | +258 | **0** | **+464** | +443 | 0.46 |

Four markets go over the drain; those four are exactly the four that lose money.
Tomato, egg and carrot have **679 units of drain nobody supplies**.

*Caveat on the drain column:* the per-day RNG (`kaggriculture.py:871`) is consumed by
weed spawns on every empty unlocked tile **before** `rng.choice` picks the day's shop, so
the shop draw is a function of both seats' empty-tile counts. Drain-at-base is 201,949
vs kagg2 and 212,824 vs starter — a 5 % confound on the same seeds, not a measurement error.

### (c) Scale — kagg3 is **bigger** than kagg2 and works **less** of it

| day 20 | quadrants | max hands | planted tiles | animals | **empty owned tiles** | worked / owned |
|---|---|---|---|---|---|---|
| kagg3 vs kagg2 | **4.0** | 12.0 | 37.2 | 24.5 | **34.4** | 61.7 / 100 = **62 %** |
| kagg2 | 3.3 | 12.0 | **62.1** | 15.2 | **5.3** | 77.3 / 83.3 = **93 %** |

- **Land**: kagg3 buys quadrant 2 on **day 1**, 3 on day 13, 4 on day 17 — **7,000 coins**
  for 100 tiles, 34 of them idle all season. kagg2 buys on days 7 and 12 for **4,333**.
- **Labour**: kagg2 is at 11–12 hands from **day 8**; kagg3 reaches 12 only at **day 17**.
  Season hand-days 229 (kagg3) vs **277** (kagg2). kagg3 hires *fewer* hands vs kagg2
  (229) than vs starter (247) — the cash it does not have.
- **Herd timing**: kagg2 has 12 animals by day 10 and holds 15 to the end. kagg3 has 7 at
  day 10, peaks at 24.6 around day 22, ends at 9.9. A cow placed on day 20 fires 4 fewer
  times than one placed on day 12.
- **Replanting stops**: kagg3's planted tiles fall 46.6 (d14) → 37.2 (d20) → **18.5 (d28)**.
  kagg2 holds 50–62 planted from day 12 to day 29. Same shape vs starter (51.6 → 22.5),
  so this is a planner defect, not a matchup effect.
- **Per-tile productivity**: 103,831 base value / 61.5 worked tiles = **1,689 per tile**
  for kagg3; 175,516 / 77.3 = **2,271** for kagg2. kagg2 is 1.34× more productive per
  worked tile *and* works 16 more of them.
- **The crop board at day 20** (planted tiles) — kagg2 grows two crops and nothing else:

  | | wheat | carrot | tomato | strawberry | melon | total |
  |---|---|---|---|---|---|---|
  | kagg3 vs kagg2 | 7.8 | 1.4 | 2.6 | 22.3 | 3.2 | **37.2** |
  | kagg3 vs starter | 2.0 | 0.2 | 3.1 | 31.7 | 7.3 | 44.2 |
  | **kagg2** | **29.2** | 0.0 | 0.0 | **32.9** | 0.0 | **62.1** |

- **Shed**: kagg3 peaks at 92/100 and holds 91 on day 29; kagg2 sits **at the 100 cap** on
  day 29. Neither is throwing away product (`overflow_destroyed` 0), but kagg2's shed is
  the binding constraint on its throughput and kagg3's is not — more evidence that kagg3's
  limit is upstream, on the board.

### (d) Purchase side — **not a cost. kagg3 buys slightly cheaper.**

| | wheat bought | c/unit | fertilizer bought | c/unit |
|---|---|---|---|---|
| kagg3 vs starter | 139.5 | 38.5 | 1.1 | 89.0 |
| kagg3 vs kagg2 | 80.5 | **37.6** | 3.0 | 64.8 |
| kagg2 | 626.3 | 39.1 | 0 | — |

Seed and animal prices are engine constants and cannot move. The only market-priced
inputs are wheat and fertilizer, and both are **cheaper** when kagg2 is in the market —
its supply depresses the buy quote as much as the sell quote. kagg2's 626-unit wheat
purchase (24,508 coins) against its 684-unit wheat sale (28,321) nets it **+3,813**: the
"wheat treadmill" is feed logistics, not a profit centre.

One incoherence worth naming: kagg3 buys 3 fertilizer at 64.8 c/u in the same season it
sells 209 at 46.4 c/u. Worth −195 coins; a symptom of the reservation reading a constant
`_BASE`, not a lever.

### (e) Everything else

| item | vs starter | vs kagg2 | note |
|---|---|---|---|
| `value_dropped` (queued task value the route never does) | **39,414** | **21,827** | wasted labour, planner-side |
| `purchase_shortfall` (wanted candidates the greedy refused) | 15,487 | 11,116 | cash constraint |
| `overflow_destroyed` | 4 | 0 | non-issue |
| unsold products at day 29 | **0.0** | **0.0** | non-issue |
| animals bought / alive at d29 | 30.8 / 14.2 | 26.0 / **9.9** | **16 animals starve** in both |

**Herd attrition is the biggest un-named leak**: kagg3 pays 10,933–12,942 coins for
26–31 animals and finishes with 10–14. kagg2 buys 15.3 and finishes with 13.9 (loses
1.4). The deaths cluster on days 27–29, tracking the hand count collapsing (12 → 7.2 →
4.2 → 0) — the farm winds down its crew and the herd starves with it. Cost is bounded by
the missed fires, ≈ 15 animals × ~1.5 fires × ~170 c ≈ **4k**, not the 6.7k of sunk
capital (animals are unsellable either way).

### (f) Sell timing — measured, and it is worth **nothing**

kagg2 sells in **every one of the 24 turns**; 750 units (43 % of its revenue, 68,952
coins) land in turns **0–2**, before kagg3's first lot at turn 3. kagg3 sells only at
turns 3/10/18 (`ops.SELL_TURNS`).

Repricing kagg3's entire season book off each day's **hour-0** inventory — i.e. as if it
sold first, before kagg2 and before the day's drain — gives **89,159 against the actual
90,312: −1,153**. The town's six shop ticks a day recover roughly what kagg2's morning
block takes, so lot 1 at turn 3 is *already* the better side. Pricing the book at hour 23
instead costs 11,308, which is what "sell after everybody" is worth.

Re-timing the same volumes on the drain's own daily profile is **+3,273 (+4 %)**;
loading them all into the last ten days is **+464**. At kagg3's volumes the whole timing
axis is worth under 4 %.

## 4. Lever ranking

Marginal coins per extra season-unit, at kagg3's current margin (its own daily sell
profile, +10 % volume, kagg2's measured supply held fixed; model reproduces the measured
per-product revenue to ±13 %, worst case milk −29 %):

| product | base | **vs kagg2** | vs starter | drain | k3 units | k3/drain |
|---|---|---|---|---|---|---|
| **WOOL** | 200 | **+210.7** | +261.9 | 282 | 74.1 | **0.26** |
| **TOMATO** | 60 | **+93.0** | +67.5 | 218 | 30.0 | **0.14** |
| EGG | 50 | +55.3 | +56.8 | 249 | 87.9 | 0.35 |
| MELON | 250 | +44.1 | +196.8 | 30 | 60.8 | 2.02 |
| STRAWBERRY | 120 | +35.9 | +192.0 | 330 | 143.0 | 0.43 |
| CARROT | 35 | +34.6 | +22.8 | 329 | 114.8 | 0.35 |
| FERTILIZER | 100 | +25.7 | +50.7 | **0** | 209.4 | — |
| WHEAT | 25 | +24.9 | +23.9 | 492 | 137.9 | 0.28 |
| **MILK** | 160 | **−54.9** | +207.9 | 307 | 137.9 | 0.45 |

The marginal unit of **milk is worth −55 coins** against kagg2 and +208 against starter.
The marginal unit of **wool is worth +211** and kagg3 supplies a quarter of wool's drain.

Ranked by expected coins, with the mechanism named:

| # | lever | evidence | **est. coins** | learnable by ES today? | in the plans? |
|---|---|---|---|---|---|
| 1 | **Work the idle tiles.** 34 empty owned tiles at d20; planted count decays 47→18 after d14. Refilling with the uncontested products (wheat/carrot/tomato/egg ×3) | §3(c), scenario S3 | **+19k** (62k→81k) | **No.** `dev_frac × n_free` sizes development, but nothing re-queues a tile whose crop died; this is `plan._derive` replant/route work | **No.** Neither plan covers replanting or route saturation |
| 2 | **Herd composition + timing.** Stop buying geese (224 c/animal-day vs a cow's 432); place the herd by d12 not d20; cap milk at the drain and take wool instead | §3(b), §4 margins | **+10–15k** | Partly — `animal_share`/`crowd` shift the mix, but `Macro.animal_kind` is one argmax, so a day cannot buy 3 cows + 2 sheep | **Yes** — `2026-08-25-land-value-mixed-herd` Task 4 is exactly this |
| 3 | **Product mix by contested-ness**, not by price level: melon 0.50×, fertilizer 0.46×, milk marginal −55 vs tomato +93, wool +211 | §3(a), §4 | **+8–12k** | **Partly.** `brain.features` col 6 carries opponent production per product; the grow score already reads it, but the trained theta responds by *fleeing* the flooded product rather than pricing the town's residual drain. A drain feature (`daily_town_units − own − opp`) would make it learnable | **No** |
| 4 | **Buy less land, hire earlier.** 7,000 on 4 quadrants with 34 idle vs kagg2's 4,333 on 3.3; kagg2 is at 11 hands on d8, kagg3 on d17 | §3(c) | **+5–8k** | **No** — `buy_land` is a bare logit and the quadrant is booked at zero value | **Yes** — land plan Tasks 1/2/3 (prospective tiles, `land_value`, turn-2 land) |
| 5 | **Keep the herd fed to day 29.** 16 of 26 animals starve, hands 12→0 over d27–29 | §3(e) | **+4k** | No — feed routing is fixed actuator logic | No |
| 6 | **Cut fertilizer volume.** 209 units at 46 c/u = 9,723 coins for 209 shed slots and 209 sell-slots on a product with **zero** town drain | §3(b) | **+2–4k** (as substitution) | Yes — `press`/`grow_mult` on FERTILIZER, and it is a byproduct so only the *sell* side is choosable | Partly (reservation plan §3.1's drift is exactly 0 on fertilizer) |
| 7 | Sell-lot timing / drain-paced reservation | §3(f) | **+3.3k at today's volume** | Yes (`hold`, and the reservation plan's `patience`) | **Yes** — and its own §5.0 trigger still does not fire: k3/crossover is milk 0.77, strawberry 0.53, wool 0.26, wheat 0.28 |
| 8 | Sell earlier in the day (turn 0 instead of 3) | §3(f) | **−1.2k** | n/a | n/a — **do not build this** |

Levers 1, 4 and 5 are all the same underlying defect seen three ways: **the planner buys
capacity it never staffs.** Land, animals and tiles are all acquired ahead of the labour
that would work them.

## 5. What 2× kagg2 costs, and whether the town can pay for it

### The drain is a price mechanism, not a coin pot

The often-quoted "206k absorbable at base" is **not** a cap on coins. Measured, the two
seats together booked **246,564** of revenue against a drain worth **201,949 at base** —
ratio **1.22**. Coins are minted at whatever the quote is; the drain only sets *where on
the curve* the quote sits, and the curve floors at 1 (and a floored sale does not even
add supply, so volume is unbounded at 1 c/u).

What the drain **does** cap is the number of units that can be sold at **≥ base**. Over a
season, `final_inv − I0 = (both seats' supply) − drain`, and a sale prices at or above
base only while `inv ≤ I0`. So the joint above-base volume is at most the drain — 201,949
coins at base, ≈ 245–270k at the 1.2–1.34× multiples a book *under* the drain actually
realises (kagg3 vs starter: 1.342; kagg2 vs starter: 1.242).

**For kagg3 to hold 200k while kagg2 holds 100k:** kagg3 needs `rev3 = 197,000 + spend3`,
and a book big enough to earn that costs ≈ 67k of seeds/animals/hands/land (the spend
model at 3× base value), so `rev3 ≈ 264k`; kagg2 at 100k needs `rev2 = 145,218`. Joint
revenue **409k against a 202k pot — 2.0× the town's whole above-base capacity**, with
kagg3 taking essentially all of it. It is not reachable.

### The reachable frontier

Scenarios below scale kagg3's measured daily sell profile per product, hold kagg2's
measured net supply fixed (its production is invariant, §2), and reprice **both** books
on the real curve. Calibrated so the baseline row reproduces the measured 90,312 /
156,252. kagg3's spend scaled as `31,265 × (baseV / 103,831)^0.7`; kagg2's fixed at 48,218.
The last column is the worked tiles the book needs at kagg3's measured 1,689 base/tile and
at kagg2's 2,271 — **kagg3 owns 100 and works 61**.

| scenario | base value | k3 rev | k2 rev | **k3 coins** | **k2 coins** | ratio | tiles @k3/@k2 rate |
|---|---|---|---|---|---|---|---|
| S0 measured | 104k | 90k | 156k | **62k** | **111k** | 0.56 | 61 / 46 |
| S1 no melon, fert ×0.5 | 78k | 78k | 161k | 55k | 116k | 0.47 | 46 / 34 |
| S3 uncontested ×3 (fill the idle tiles) | 131k | 115k | 153k | **81k** | 108k | 0.75 | 78 / 58 |
| S13 uncontested ×3, straw/milk ×2, wool ×3, no melon | 174k | 113k | 110k | 71k | 65k | **1.10** | 103 / 77 |
| S5 everything ×2 | 208k | 127k | 111k | **79k** | 66k | **1.20** | 123 / 91 |
| S8 book = the town's drain, every product | 212k | 123k | 101k | 75k | 56k | **1.33** | 126 / 94 |
| S6 everything ×3 | 311k | 137k | 82k | 72k | 37k | **1.96** | 184 / **137** |

Read off it:

1. **Beating kagg2 needs roughly 2× kagg3's base-value production (104k → 200–212k) and
   ~90 worked tiles at kagg2's per-tile rate.** That is inside the board: kagg2 already
   does 175k on 77 tiles. It requires closing both halves of §3(c) — 61 worked tiles → 90+,
   and 1,689 base/tile → ~2,270.
2. **Own-coin-maximising and win-maximising point in different directions.** S3 (fill the
   idle tiles with the products kagg2 ignores) is the best coins-per-tile lever, **+19k**,
   and still **loses**, because it leaves kagg2's 156k untouched. The winning scenarios all
   push volume into the *contested* products, where kagg3's own marginal unit is worth
   25–36 coins but costs kagg2 far more.
3. **The denial exchange rate is ≈ 1.5 : 1.** Going S0 → S5 gains kagg3 +37k of revenue
   and costs kagg2 −45k. That is why S5 beats S3 on the scoreboard while earning kagg3
   almost the same coins.
4. **2× is only in S6, and S6 is infeasible.** 311k of base value needs 137 worked tiles at
   *kagg2's* productivity; the board has 100. And S6's kagg3 finishes on **72k coins**, i.e.
   the 2× is won by demolishing the market (kagg2 to 37k), not by earning more.

### So: is 2× possible?

**Not on coins.** Against this opponent the realistic ceiling for kagg3's own purse is
≈ **80k** (S3/S5), because everything past ~200k of base value prices below 0.5×. The
ratio can reach ~1.3–1.35 (S8) at a feasible board and ~2.0 only at an infeasible one.

If the goal stays literal (kagg3 ≥ 2 × kagg2 in the same game), the only paths are:

* **Denial, priced.** Push volume into strawberry / milk / wool / melon *because* it
  costs kagg2 1.5 coins per coin it costs kagg3. Ratio 1.33 at S8, 1.96 at S6.
* **The uncontested drain, for kagg3's own purse.** Drain *minus current joint supply*:
  tomato 188 units (11.3k at base, and tomato prices **above** base — +93 c/u marginal),
  wheat 377 (9.4k), carrot 203 (7.1k), egg 161 (8.1k) — **929 units ≈ 36k at base that
  nobody is supplying**. kagg2 sells **zero** tomato and **zero** egg all season and 11
  carrot. kagg3 books 16,562 across those four today; scenario S3 takes it to ~40k.
  Headroom **+19 to +24k**, and it is the only headroom that does not depress its own price.
* Both together (S13/S5) is the frontier: ratio 1.10–1.20 at 77–91 tiles.

**Recommendation on the goal itself.** `GOAL.md` optimises **win rate**, not margin, and
the Bradley-Terry tournament discards coin margin entirely. The measured distance to a
*win* is 48,988 coins and is reachable (S5/S8/S13); the distance to 2× is not. The 2×
framing should be retired in favour of "beat kagg2 on ≥ 60 % of seeds", which S8's 1.33
ratio would deliver with room.

## 6. Corrections this forces on the two open plans

* **`2026-08-25-land-value-mixed-herd`** — its premise ("`kagg2` runs a ~2× farm … every
  one of those four facts is something this planner structurally cannot do") is **half
  wrong for this checkpoint**. kagg3 already reaches **4 quadrants** (kagg2 3.3), 12 hands
  (kagg2 12) and **24.6 animals** (kagg2 15.2). What it cannot do is *work* them: 34 idle
  tiles, planted count halving after day 14, 16 animals starved. Task 1 (prospective land)
  and Task 2 (`land_value`) are still right, but for the opposite reason from the one
  stated — the model must learn to **refuse** the 4,000-coin fourth quadrant it currently
  buys and leaves empty, not to buy land earlier. Task 4 (mixed herd) is confirmed by the
  goose measurement and should be prioritised over Tasks 1–3.
* **`2026-08-26-drain-aware-reservation`** — its §5.0 trigger correctly refuses to fire.
  Against kagg2 the volume fractions are wool 0.26, wheat 0.28, egg 0.35, carrot 0.35,
  strawberry 0.43, milk 0.45 of drain — all under the 0.53–0.69 crossover. Re-timing the
  whole book on the drain profile is **+3,273 (+4 %)**. Its §6/R6 correction stands but
  needs restating: the leak is **milk + strawberry (83 % of the gap)**, not melon +
  fertilizer (29 %), and the mechanism is a **contested** drain, not a zero drain.
* **`es/archetypes.py` docstring** — "`kagg2` keeps every product's supply under the
  town's own drain, so it sells … *above* base all season" is **false against a real
  opponent**: kagg2 realises **0.890×** here, and 1.242× only when unopposed. Its edge is
  1.74× the units at the *same* 90 c/u, off a book worth 175k at base to kagg3's 104k.
* **New feature the ES cannot currently see.** `brain.features` carries own production and
  opponent production per product, but nothing carries the town's *residual* drain
  (`PJ.daily_town_units − own_pipeline − opp_pipeline`). That single scalar per product is
  what separates "tomato pays +93 c/u" from "milk pays −55 c/u", and no combination of the
  existing knobs expresses it.

---

### Reproduction

Telemetry harness, analyses and the 48-game JSON are in this session's scratchpad
(`probe.py`, `an*.py`, `games.json`); nothing was added to `scripts/`. The harness
monkeypatches `kaggle_environments.envs.kaggriculture.kaggriculture` inside each worker
process only, and restores it in a `finally`. Re-run with:

```
.venv/bin/python probe.py --theta artifacts/p2s0/champion.npy \
    --games 12 --workers 6 --seed-base 20260825 --out games.json
```

Model caveat: §4 and §5 use a per-product season simulator that replays the real price
table, the measured per-day drain and kagg2's measured net supply. Replaying kagg3's own
measured profile through it reproduces the measured per-product revenue to **−13 % … +13 %**
(worst case milk −29 %, because kagg3 sells milk in one turn-18 lot and the model drains at
end of day). Scenario **differences** are trustworthy; scenario **levels** are calibrated
to the measured baseline and still carry that band.
