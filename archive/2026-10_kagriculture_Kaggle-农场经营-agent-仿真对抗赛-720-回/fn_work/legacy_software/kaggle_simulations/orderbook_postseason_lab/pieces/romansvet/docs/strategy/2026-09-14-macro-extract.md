# MACRO-EXTRACT: what the top five do per day, and how much of it theta can say

**VERDICT: the crew ramp is fully expressible and B is the only thing standing in its way
(fit MAE 0.03 hands/day vs B's 2.19, and B's decoded ramp asks for 0 hands on days 0-5 while
ymg_aq hires 4 on day 0); the herd split is expressible (MAE 0.03-0.07 animals/day); the crop
programme is NOT — one theta fitted with no sigma limit on 180 real ymg_aq dawns reaches wheat
to 1.19 tiles/day but collapses carrot, strawberry and melon to ~0 (MAE 0.91 / 1.01 / 0.47 against
targets of 1.01 / 1.04 / 0.47), and the development total stays 3.3 tiles/day short.
Fertiliser application, sale day/hour/units and the wheat re-buy leg have NO decoder channel at all.**

Scope: replay-descriptive plus a decode fit. No simulator episode, engine game or outcome evidence.
Tools written for this: `S/macro_extract/{extract.py,summary.py,fit.py}`. Inputs: the 18 TOPB3
replays (`S/topb3/replays`, seats from `S/topb3/teams.csv`), `S/topledger3/raw_B.npz` for B.
Seed: `S/macro_extract/seed_ymg_aq.npy`, **md5 `3b6040a6a7a3034c9a8643062b7aae59`**
(1,500 Adam steps, lr 0.01, `MELON_GENE_ON=True`, `CROP_MIX_GAIN=256`, 7,020 coordinates).

## 1. Extraction

`extract.py` walks each replay hour by hour and writes `macro_<team>_<ep>_<seat>.json`, 30 day
records per seat: dawn board (tiles per crop, animals per kind, fertilised tiles, idle, locked,
money, nquad, shed, seeds, market inventory/prices, shop counts, `brain.n_free_slots`), the day's
new plantings per crop (`planted_day == d` at the next dawn, so it is the board's own record and not
an action count), new animals per kind, peak hand roster, hires, FERTILIZE ops, PLANT ops, every
market order (BUY_SEED / BUY_PRODUCT / BUY_ANIMAL / BUY_LAND / HIRE) and every SELL lot with its
hour and the quote standing when it was issued. The dawn PolicyObs is built with the shipped
`kagg3.agent.parse` path that `scripts/package_submission.py` uses, so a dawn recorded here is the
dawn our submission would decode on their board. 18 files, all 18 seats, no gaps.

**Roster fact that changes every hands number:** the hand roster is empty at every dawn and re-hired
inside the day (`hires_today`), so "hands at dawn" is 0 for everyone including B. The crew metric
below is the **peak roster inside the day**, which equals both `hires_today` and the HIRE order count
on every day checked.

## 2. Cross-team table (medians; 6 seats per top-five team, 12 B games on the ymg_aq tapes)

| metric | ymg_aq | DSM | Majkel1337 | our B |
|---|---:|---:|---:|---:|
| hands d0 | **4** | **4** | **4** | UNVERIFIED |
| hands d1 | 1 | 4 | 4 | UNVERIFIED |
| hands d5 | 4 | 6 | 6 | UNVERIFIED |
| hands d10 | **11** | **11** | **11** | UNVERIFIED |
| hands d20 | 11 | 11 | 11 | UNVERIFIED |
| hires per season | 278 | 286 | 286 | UNVERIFIED |
| wheat tiles d0 | 0 | 0 | 0 | 0 |
| wheat tiles d5 | 7 | 0 | 0 | 11 |
| wheat tiles d10 | **16.5** | **19** | **16.5** | **9** |
| wheat tiles d20 | **20** | **19** | **17.5** | **11** |
| day of first sheep | 1 | 1 | 1 | 1 |
| day of first wool sale | 6 | 6 | 6 | UNVERIFIED |
| cash dawn d5 | 489 | 382 | 350 | 1,415 |
| cash dawn d10 | 1,355 | 585 | 552 | 6,124 |
| cash dawn d15 | 18,590 | 25,849 | 23,531 | 7,805 |
| tiles d10 W/C/T/S/M | 16.5/0.5/0/26.5/11.5 | 19/0/2/18.5/12 | 16.5/0/0/23.5/12 | 9/0/0/22/6.5 |
| tiles d20 W/C/T/S/M | 20/0/6/25/3.5 | 19/0/15/17/0 | 17.5/2.5/8.5/24/0 | 11/0/3/28/9 |
| animals d10 G/C/S | 0/7.5/3 | 1/6/7 | 2/6/4 | 1.5/5.5/2 |
| animals d20 G/C/S | 0/7.5/3 | 1/6/7.5 | 2/6.5/7 | 4/6/4.5 |
| FERTILIZE ops per season | 138 | 156 | 145 | UNVERIFIED (B ledger records fertilised tiles, not ops) |
| SELL lots per season | 348 | 464 | 387 | UNVERIFIED |
| units sold per season | 2,516 | **10,516** | 1,572 | UNVERIFIED |
| WHEAT units bought per season | **1,145** | 237 | 266 | 141 (`S/topledger3` ledger) |

B's hand counts are **UNVERIFIED**: `raw_B.npz` snapshots the dawn, where the roster is empty by
construction, and no hire line exists in that ledger. What *is* measured is B's decoded ask
(`crew_target`, §4): 0.0 on days 0-5, 0.2 on d6, 5.0 on d8, 10.9 on d10.

### The three biggest "they do / we don't"

1. **Four hands on day 0, and a crew from d0 not d8.** All three teams hire 4 hands on day 0 and are
   at 11 by day 10; B's decoded crew ramp asks for **zero** hands until day 6 and only reaches 10.9
   at d10. 278-286 hires a season.
2. **Wheat as a standing board, not a crop.** 16.5-19 wheat tiles at d10 and 17.5-20 at d20 against
   B's 9 and 11 — and ymg_aq *additionally* buys 1,145 units of wheat off the market (price-neutral
   churn, `2026-09-14-top5-ledger.md` §4), 8x B's 141.
3. **Broke on purpose through d10.** They hold 350-1,355 coins at dawn d5/d10 (B: 1,415/6,124) and
   are 2.4-3.3x richer than B by d15 (18.6k-25.8k vs 7.8k). Cash is converted into hands and wheat
   tiles in the first ten days and the lead is taken back after d15.

Per-day medians for ymg_aq are printed by `summary.py`; the shape is a **d0 block** (12 wheat + 2
melon + 5 animals + 4 hands), a **d2-d6 second block** (11 wheat, then 6+10 strawberry and 3 melon
with the crew at 9), then **6-9 new wheat tiles every single day from d10 to d27** with carrot
joining at d22-d27. Nothing is planted on d28-d29.

## 3. Expressiveness fit (deliverable 2)

180 dawns = 6 ymg_aq boards (the `retention >= 0.95` set of `S/topledger3/boards.json`, all six
sim-exact per that report) x 30 days. Every theta-independent input (`features`,
`board_forecasts`, `production_forecast`, `forward_value`, `market_momentum`, `n_free`,
`can_mature`, the drain column) is computed once per dawn in numpy — confirmed theta-free by
inspection of `brain.features`, and consistent with `2026-09-14-melon-reachability.md` §3 ("features
do not depend on theta, so this is exact"). Only `policy.forward` and the decode arithmetic carry
gradient. The fit targets the **pre-quantisation** outputs: `_qfloor` and `_largest_remainder` are
removed, so `plant_soft = w * plant_total` and `crew_soft = crew_top * sig(...)` are real-valued.
`absorb` is `stop_gradient`-ed (a threshold), `land_ok` is pinned to the replay's own BUY_LAND.
Adam, all 7,020 coordinates, lr 0.01, 1,500 steps, no sigma limit. Loss 16.94 -> 4.54, still falling
at ~0.007/50 steps, i.e. **converged for the crew and herd channels and plateaued for the crop mix**.

| channel | target/day | B decode | fitted decode | MAE at B | MAE fitted | verdict |
|---|---:|---:|---:|---:|---:|---|
| `crew_target` (hands) | 9.26 | 8.36 | 9.25 | 2.19 | **0.03** | **EXPRESSIBLE** |
| `animal_want` GOOSE | 0.033 | 0.423 | 0.034 | 0.404 | **0.040** | **EXPRESSIBLE** |
| `animal_want` COW | 0.256 | 0.297 | 0.267 | 0.303 | **0.030** | **EXPRESSIBLE** |
| `animal_want` SHEEP | 0.222 | 0.454 | 0.189 | 0.475 | **0.066** | **EXPRESSIBLE** |
| `plant_target` WHEAT | 5.21 | 2.71 | 4.23 | 3.89 | 1.19 | **PARTLY** (70 % of the gap closed) |
| `plant_target` TOMATO | 0.322 | 0.320 | 0.073 | 0.296 | 0.251 | **PARTLY** (15 % closed) |
| `plant_target` CARROT | 1.006 | 1.099 | 0.096 | 1.263 | 0.912 | **PARTLY / collapses** |
| `plant_target` STRAWBERRY | 1.039 | 1.433 | 0.027 | 0.982 | 1.012 | **NOT** (fit drives it to 0) |
| `plant_target` MELON | 0.467 | 0.547 | 0.000 | 0.739 | 0.467 | **NOT** (fit drives it to 0) |
| development total `n_dev` | 8.56 | 7.78 | 5.23 | 4.79 | 4.03 | **PARTLY** (16 % closed) |
| fertiliser applications | 4.6 ops/day | — | — | — | — | **NOT EXPRESSIBLE — no channel** |
| sale day / hour / units | 11.6 lots/day | — | — | — | — | **NOT EXPRESSIBLE — no channel** |
| market wheat re-buy | 38 units/day | — | — | — | — | **NOT EXPRESSIBLE — no channel** |

**Why the crop channels fail and the crew one does not.** `crew_target` is a free three-parameter
logistic in the day (`ramp[0..2]`), so a 4-at-d0 / 11-at-d10 / 11-at-d20 ramp is a direct
parameterisation and the fit nails it to 0.03 hands. The five crops share **one** softmax over the
five grow scores (`crop_logits = grow[:5] * (1 + sig(head[7])*4)`, plus `cb`/`cm`), and the per-day
mix therefore has to come entirely out of the *features*. The ymg_aq programme is block-structured —
a pure-wheat day (d2: 11/0/0/0/0) and a pure-strawberry day (d3: 0/0/0/6/0) sit next to each other —
and the least-squares optimum for one theta is to put the whole softmax mass on the crop with the
largest total (wheat, 5.21/day) and zero the rest. That is exactly what the fit does: wheat 2.71 ->
4.23 while carrot/strawberry/melon go to 0.10/0.03/0.00. This is the *same* failure
`2026-09-14-melon-reachability.md` §4 named at training sigma ("decode gain versus an integer
boundary"), but measured **with no sigma limit at all**: it is not a step-size problem, it is that
one shared softmax cannot hold a day-indexed crop programme.

The development total is the second wall: `n_dev = sig(head[5] + aux[2]*n_free/25) * n_free` is
bounded by `n_free`, so on the days ymg_aq develops 12-22 tiles out of a board that our
`n_free_slots` counts as smaller, no value of `dev_frac` reaches the target — the fit closes only
16 % of that gap and the residual 4.03 tiles/day is a **capacity** residual, not an optimisation one.

## 4. Macro channels the top-five play that the decoder does not have (for EXEC-SCOPE)

1. **Sale timing.** `Macro` exposes `hold[9]` (reservation coins/unit) and `press[9]` (coins lost per
   lot of delay) and nothing else. There is no *day*, no *hour*, no *lot size* and no *per-product
   sale schedule*. ymg_aq issues 348 SELL lots a season at specific hours (first lot on day 0);
   none of that is a decodable quantity.
2. **Fertiliser.** 138-156 FERTILIZE ops a season, and `Macro` has no fertiliser field at all
   (`head[2]` was `n_fertilize` before 0.11 and is now the animal-mix sharpness). Application is a
   planner decision driven by the shed, not a decoded target.
3. **Market purchases of product.** ymg_aq's 1,145-unit wheat re-buy leg has no channel:
   `Macro`'s comment says input purchases are "absent on purpose — the executor derives those".
4. **Hands per day beyond the ramp.** `crew_target` is a *monotone logistic in the day* plus a
   per-bucket `hire_bias`. ymg_aq's median roster is 4, 1, 4, 4, 4, 4, 9, 5.5, 8, 9, 11 on d0-d10 —
   non-monotone, with a d1 dip to 1. The ramp cannot dip. (It fits the median to 0.03 because the
   *median* profile is near-monotone; per-board it cannot.)
5. **A day-indexed crop programme.** Per §3: blocks of one crop on consecutive days are not
   reachable through a single shared softmax. Either a day-conditioned mix bias (a `cb` that is a
   function of the day, as `hire_bias` already is a function of the day bucket) or an explicit
   per-day plan channel is required.
6. **Development beyond `n_free`.** Days where the target develops more tiles than `dev_frac` can
   grant; see §3's `n_dev` residual.

## 5. Files

- `S/macro_extract/extract.py` -> 18 x `macro_<team>_<ep>_<seat>.json`
- `S/macro_extract/summary.py` -> `summary.json` + the §2 table
- `S/macro_extract/fit.py` -> `seed_ymg_aq.npy` (md5 `3b6040a6a7a3034c9a8643062b7aae59`),
  `fit_report.json`, `fit_long.log`

**UNVERIFIED / not measured:** B's per-day hire counts, B's FERTILIZE ops, B's sale lots (the
`S/topledger3` ledger records dawn snapshots and per-product receipts, not hires or ops). Whether
`seed_ymg_aq.npy` plays better than B — it has had **no** simulator or engine game. It is an
initialisation, and §115 promotion stays outcome-only. SpaTaro and Crop Dusta were **not** extracted:
`S/toptier_0911/` does not exist in this tree (both appear only as opponents inside TOPB3 replays).
