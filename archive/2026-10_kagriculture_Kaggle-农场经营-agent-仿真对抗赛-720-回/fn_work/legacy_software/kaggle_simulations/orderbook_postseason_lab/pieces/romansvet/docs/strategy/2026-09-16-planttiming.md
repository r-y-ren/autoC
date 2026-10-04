# PLANTTIMING — "is today the best day" asked of PLANT: STOP BAR, ceiling is 0

2026-09-16 19:10–19:35Z, branch `planttiming` off master `dca4d21` (= the
SHIPPED FT2 package; module defaults in `plan.py` are the package). Third and
last instance of the `2026-09-16-fertengine.md` question, after
`2026-09-16-caretiming.md`.

## 1. VERDICT — **STOP at Q1. Nothing built, nothing judged. Family CLOSED.**

FERT_TIMING won because a fertilizer unit is *storable*: holding it costs
nothing and `fert_marginal_value` genuinely varies with the day. A **seed is
not storable in the ground** — deferring a planting shifts the whole tile
schedule forward and the tail falls off the day-29 sellable horizon. And the
one quantity a FERT_TIMING-shaped gate could compare is **constant in `k`**,
for the same reason CARETIMING's two were: the planner reads only *today's*
spot quote (`view.price`; no price history or forecast in any shipped
decision, `2026-09-16-momreview`), so the value it would compute for "plant
today" and "plant in `k` days" is **the same number**, minus whatever the
day-29 truncation removes.

| our-purse ceiling, coins/board | ENG22 (22) | V45 (5) | bar |
|---|---:|---:|---:|
| **GATE-REACHABLE (decision-day quote)** | **0** | **0** | +450 |
| perfect-foresight oracle, per-tile DP k≤3 | +646 | +224 | |
| perfect-foresight oracle, per planting | +1,068 | +342 | |
| **unrestricted (rule fires everywhere), k=1** | **−22,803** | **−21,660** | |
| unrestricted, k=2 / k=3 | −42,399 / −59,384 | −41,134 / −57,931 | |
| crop-swap upper bound (loose, no cascade charge) | +83,488 | +92,944 | |

The only column over +450 is a **perfect-foresight** read of the realised price
path, and it is provably unreachable: repricing the identical units at the
quote the planner actually sees on the decision day drives it to **exactly 0**
on both legs and both seats. The opponents' own oracle is the same size
(ENG22 +629, V45 +361) — nobody is harvesting it either.

**Mean Δ at k=1 is negative on every one of the 26 plant days** (ENG22 −27 to
−208, V45 −13 to −202), so no day-conditional or crop-conditional variant of
the rule has a positive expectation either.

## 2. Best-day fractions — the opposite shape to fertilizer

| plantings on the best day, per game | US | THEM |
|---|---:|---:|
| ENG22 (22 boards) | **81.6 %** (3,205/3,927) | 87.4 % (4,110/4,704) |
| V45 (5 boards) | **85.4 %** (760/890) | 86.1 % (1,025/1,190) |
| (fertilizer, for contrast — FERTENGINE) | 29 % | **91 %** |

"Best day" = today is the argmax over `k = 0..3` of the whole tile's remaining
schedule shifted by `k`, same crop, spot-priced, day-29 truncated. We are 6
points behind ENG22 and **level with V45** — and all of that residual is the
unforecastable price wiggle above, not a rule.

## 3. The instrument — 22 ENG22 + 5 V45 boards, both seats, real engine

`S/planttiming/probe.py` replays each turn's unit ops in the engine's own order
(farmer then hands) on a working copy, so a HARVEST reads the yield **after**
a WATER taken earlier in the same turn (`plan.py` packs WATER before HARVEST).
It emits raw events only: every PLANT that actually landed (the engine refuses
one on an occupied tile, `kaggriculture.py:420`), every HARVEST off a PLANT
tile linked to its planting by `(tile, crop, planted_day)`, the decay census,
and the daily start-of-day spot quote for all nine products.

`S/planttiming/report.py` does the counterfactual. Deferring planting *j* by
`k` shifts **every later planting on that tile** by `k` too, because
`_new_plant` (`:214`) stamps `planted_day` and
`max_lifespan_step = (day + max_yield_day + 1) * turns_per_day` off the plant
day — so the tile-idle cost is charged automatically by what falls off day 29,
and the ceiling is a per-tile DP over cumulative shifts, not a per-op sum.
Every unit is priced at the SPOT quote on the day it **lands**
(`2026-09-16-feedfire.md` standing lesson).

| per game, ENG22 | US | THEM |
|---|---:|---:|
| plantings that landed | 178.5 | 213.8 |
| realised value @ spot | 82,628 | 83,829 |
| plantings that never harvested / seed coins burnt | 3.8 / 61 | 5.7 / 111 |
| planted past its own first-yield day | **0.0** | 0.3 |
| WHEAT / CARROT / TOMATO / STRAWBERRY / MELON | 92 / 33 / 6 / 32 / 15 | 122 / 37 / 11 / 31 / 14 |

Our 3.8 dead plantings a game are day 25–27 tail fill (2.5 of them on day 27),
**none** of them planted past its own first-yield day — the horizon mask is
already exactly right, and a deferral gate only makes that bucket worse.

## 4. Q0 — the plant decision, verified

Confirmed: **a free tile is planted the first day a seed is available**, with
no valuation of the day at all. `free_slot` `plan.py:7595` (empty | weed |
harvested-this-turn, plus `prospective` at `:7952`), `fill_target =
macro.plant_target` `:7965`, `plant_eff = min(fill_target, seeds + seed_buy)`
`:8054`, `slot_rank = _rank_near(...)` `:8094`, `plant_here = free_slot &
(plant_rank >= 0) & (plant_rank < p_cum[-1])` `:8136`, crop by cumulative
boundary `:8163-8167`. It is a pure count-and-rank site: there is **no `val`
for a FERT_TIMING gate to compare** and none can be built from what the head
holds, which is why the gate-reachable ceiling is 0 rather than small.

## 5. Q2 / Q3 — not built

Stop bar met at Q1. No `PLANT_TIMING_ON`, no `PLANT_TIMING_DAYS`, no
`tests/test_planttiming.py`, no legs. **`plan.py` is untouched on this branch**
— the 7,428-int layout is undisturbed while `flow220_sw` trains.

## 6. Standing

* **PLANT day-choice is CLOSED**, on the mechanism: the payoff is day-invariant
  at the only price the planner can read, and the day-29 truncation makes every
  legal deferral weakly negative. With CARE and HARVEST (`caretiming`) this
  closes the best-day family on all four op classes; **FERTILIZER was the only
  one with a gap, and it is shipped.**
* **The crop-swap column is not a live lever here.** Its +83k is a loose upper
  bound that ignores the cascade and the labour, and the crop-mix family is
  already closed by `2026-09-16-cropmix.md` (`CROP_SCARCE_ON` −425/−69/−749)
  and `2026-09-16-jointlift.md` (extra wheat plantings never yield).
* **The live gap is VOLUME, not timing**: 178.5 plantings to ENG22's 213.8 and
  V45's 238.0, on 947 WATER ops to their 1,039 / 1,104. That is the crew, and
  `jointlift` already priced adding tiles without hands at −4,835.
* `S/planttiming/`: `run_all.sh` (`instrument` | `eng22` | `v45` | `pool`),
  `_probes.sh`, `probe.py`, `report.py`, `ledger_eng22.txt`, `ledger_v45.txt`,
  `raw/` (27 board json). Reproduce with
  `WORKERS=3 bash S/planttiming/run_all.sh instrument`.
