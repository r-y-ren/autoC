# PLANTDEATH1: why the executor's plantings die and yield less

**Date:** 2026-09-30, 09:03Z to ~09:30Z. Opus, xhigh, time box 75 min.

**Question:** on HOLD20 our deterministic MMPQ executor (crew tree cf1b9790, PROG_CREW_ON) plants as much wheat as MMPQ, but harvests 148 vs 173 times at 3.91 vs 4.68 units, with 28 weed episodes a game vs 8. Why do the plantings die and yield less, and what crew rule stops it?

**Verdict, in one paragraph.** A plant death in this engine has exactly two causes: two unwatered days in a row (dry) or an unharvested one-shot crop outliving its last yield day (decay). There is no trampling, and weed spawning on empty tiles is 1.2 a game. Our excess losses are: wheat dry deaths +13.9 a game (9.95 at age 2, after the deliberate age-1 skip, when no hand arrives on age 2 either), wheat planted on d26-27 and never harvested +9.1, carrot decay +5.0, wheat decay +2.9, strawberry dry +2.4. 78 % of the wheat dry deaths had no hand on the tile that day or the day before, and they sit on the far tiles (death rate 1 % at shed distance ≤ 3, 23-34 % at 7-8). The crew is labour-bound: it walks 141 unit-steps a day against MMPQ's 119 and waters/harvests/fertilises 21 fewer times. Every rule that forces the missed visits (critical-first, age-1 water, earlier critical urgency) or stops the far wheat (c_wmaxd 6 brings all deaths to MMPQ's 19-20 a game) is coins-neutral: the labour comes out of something else. The only rule consistent on both HOLD20 and TUNE20 is removing a loss that costs labour for nothing: no wheat planted after d26 (`c_wlast` 26), +0.0035 of the coins ratio pooled over 40 boards (t 2.02, 29/40 up, about +400 coins a board). The HOLD20-best cell (that plus far carrots harvested at age 2, `c_car2_d` 4) read +0.0123 (t 2.36) and did not replicate on TUNE20 (+0.002, t 0.42). The yield-per-harvest gap (0.77 units) is two-thirds fertiliser (0.96 vs 1.62 fertilised bonus waters per harvest) and one-third missed bonus waters (1.96 vs 2.29), because we harvest at age 3 (72 % of harvests vs 40 %), not at age 4.

## Setup

- **Harness:** S/plantdeath1/scripts/plantext.py. It runs the exact fast env (S/reactclone1/fastenv) on the mirrored MMPQ replays with MMPQ's tape (truth) or our executor (crew) in MMPQ's seat. Every step it diffs the raw tile arrays before and after the step and tracks each planting instance: crop, tile, plant step, the hour of each day's water (by age), every fertilise (step, age, before/after that day's water), every harvest (step, age, units), and the end with its engine cause. For dead instances it stores every unit op on the tile on the fatal day and the day before.
- **Causes (engine, sim.hpp):**
  - `dry0`: planting-day water missed (consecutive_dry starts at 1): never seen in either mode.
  - `dry2`: two unwatered days in a row (daily_refresh_plants at h23 -> WEED).
  - `decay`: a one-shot crop past max_yield_day, yield drained by 1 every 2 steps from h0 of day pd+max_yield_day+1 (wheat: h0 of age 5; carrot: age 4).
  - `open`: standing at game end; `dig`: dug by the crew (strawberry/tomato end of life).
- **Reproduction:** finals equal SEEDSTOCK1 / CREWSCHED1 exactly (e.g. 115338216 truth 89,248, crew 70,084). All knobs below default OFF; OFF is byte-identical (every instance, op census and final equal on HOLD20).
- **Wheat rules** (CropDef 10, 2, 4, 0, 6): planted with 1 unit, a water at age 2-4 adds 1 (2 if fertilised, which lasts day..day+2), cap 6, harvestable from age 2.

## (1) Death causes, per game (HOLD20, whole game)

| crop, cause | MMPQ | crew | excess |
|---|---|---|---|
| wheat dry2, age 2 (skipped age 1, missed age 2) | 1.35 | 9.95 | +8.6 |
| wheat dry2, age 4 (missed ages 3 and 4) | 0.15 | 5.50 | +5.4 |
| wheat planted d26-27, never harvested (open) | 0.10 | 9.15 | +9.1 |
| carrot decay (age 4: watered age 2, not visited age 3) | 0.35 | 5.35 | +5.0 |
| wheat decay (age 5: not harvested on age 4) | 0.10 | 3.00 | +2.9 |
| strawberry dry2 | 1.60 | 4.00 | +2.4 |
| tomato dry2 | 1.85 | 1.85 | 0 |
| carrot dry2 | 0.70 | 0.85 | +0.2 |
| strawberry / tomato decay (end of life, 17 / 12 days) | 12.85 | 5.95 | -6.9 |
| weed spawns on empty tiles | 0.5 | 1.2 | +0.7 |

- **Wheat end of life:** plantings 174 vs 176; harvested 172.3 vs 148.1; lost 1.9 vs 27.6.
- **Hand visits on the fatal day (wheat dry2, 15.45 a game):**
  - 12.05 had no unit on the tile the fatal day or the day before;
  - 2.05 a visit only the day before;
  - 1.35 a hand arrived at h23 of the fatal day and FERTILISED instead of watering (the c_wfert order puts FERTILIZE before a critical WATER), and the plant died that night. All 1.6 fatal-day ops on our dying plants are h23 FERTILIZEs.
- **Where they die** (wheat planted d8+, per game; plantings / dry2 deaths):

| shed distance | MMPQ | crew |
|---|---|---|
| ≤ 3 | 64.4 / 0.1 | 37.2 / 0.4 |
| 4 | 40.2 / 0.4 | 42.4 / 2.7 |
| 5 | 28.4 / 0.3 | 35.8 / 3.1 |
| 6 | 15.2 / 0.5 | 25.3 / 3.8 |
| 7-8 | 9.9 / 0.3 | 20.3 / 5.4 |

- **Where the tiles go** (life-weighted mean shed distance, d8+): wheat 4.69 vs MMPQ 3.94; carrot 3.49 vs 4.65; tomato 4.17 vs 5.38; strawberry 3.86 vs 3.95. We give the near tiles to the demand crops and fill the far ones with wheat; MMPQ does the opposite for carrot and tomato.
- **What the hands do instead** (unit-steps per game-day, d10-27): MOVE 141.2 vs 118.8; WATER 50.6 vs 59.1; HARVEST 19.9 vs 26.4; FERTILIZE 8.3 vs 12.6; total 294 vs 297 (same crew). The 22 extra walking steps a day are the missing water/harvest/fertilise visits.

## (2) Yield per wheat harvest

| | MMPQ | crew |
|---|---|---|
| harvests / game | 172.2 | 148.1 |
| at age 2 / 3 / 4 | 21.8 / 69.2 / 81.2 | 8.7 / 106.8 / 32.6 |
| units at age 2 / 3 / 4 | 2.09 / 4.53 / 5.51 | 2.00 / 4.04 / 3.99 |
| bonus waters (age 2-4) per harvest | 2.29 | 1.96 |
| fertilised bonus waters per harvest | 1.62 | 0.96 |
| 1 + W + F (before the cap of 6) | 4.91 | 3.92 |
| units per harvest | 4.68 | 3.91 |

Top patterns (age, water by age, fertilised at each bonus water; per game, units):
- MMPQ: (3, W.WW, FF) 50.3 @5; (4, W.WWW, FFF) 38.5 @6; (2, W.W) 18.3 @2; (4, W.WWW, wFF) 17.6 @6; (3, W.WW, ww) 14.6 @3; (4, W.WWW, www) 10.5 @4.
- crew: (3, W.WW, FF) 43.3 @5; (3, W.WW, ww) 36.5 @3; (3, W.WW, wF) 25.7 @4; (4, W.W.W, w-w) 15.4 @3; (4, W.W.W, F-F) 8.9 @5; (2, W.W) 8.7 @2; (4, W.WWW, FFF/wFF) 3.2 @6.
- **Decomposition of the 0.77 units:**
  - fertiliser: -0.66 (0.96 vs 1.62 fertilised waters per harvest; MMPQ's fertilised age-4 cycles at 6 units are 56 a game, ours 3);
  - missed bonus waters: -0.33 (28 of our harvests a game skip the age-3 water, W.W.W, vs 7);
  - MMPQ loses 0.23 to the cap of 6.
- **Harvest age:** 72 % of our harvests are at age 3 (the `c_unf3` rule takes unfertilised wheat out at 3 units), against MMPQ's 40 %; MMPQ carries 47 % to age 4 at 5.51 units. Both modes skip the age-1 water (MMPQ waters 9.8 of 174 plantings at age 1; mean water hours age 2 13.2 vs 12.8).

## (3) The rules, and their reads

Knobs in /mnt/e/_work/kagg3_wt_plantdeath1 (branch plantdeath1_0930 off cf1b9790), `src/kagg3/prog/direct.py`, all default OFF:
- `c_car2_d D`: a carrot on a tile at shed distance ≥ D is ripe at age 2 once watered that day (MMPQ harvests 12.75 carrots a game at age 2, 2 units; ours decays 4.5 a game unvisited on age 3).
- `c_wlast L`: no wheat planting after day L (we plant 15.7 wheat on d27, 7 never harvested; MMPQ plants 3.2).
- `c_wmaxd D`: from d8, no wheat on tiles at shed distance ≥ D.
- `c_far MASK`: the listed demand crops (1 carrot, 2 tomato, 4 strawberry, 8 melon) take the farthest free tile.
- `c_h23w`: at h23 WATER sorts before FERTILIZE on an unwatered plant.

HOLD20 paired vs crew (n 20; logs/cells_k1.txt, cells_k2.txt, cells_k3.txt; wDth = wheat dry+decay deaths, allD = all dry+decay deaths, per game):

| cell | coins | ≥ 0.90 | value | wDth | allD | wheat harv | u/h | wheat units | wheat open | carrot deaths | d(ratio), t, up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MMPQ | 1.000 | 20 | 1.000 | 1.6 | 19.0 | 172.2 | 4.68 | 806 | 0.1 | 1.1 | |
| crew | 0.847 | 6 | 0.783 | 18.4 | 36.5 | 148.1 | 3.91 | 579 | 9.2 | 6.2 | |
| c_skip1 0 (water age 1) | 0.844 | 5 | 0.785 | 19.4 | 37.4 | 144.2 | 3.82 | 552 | 9.8 | 5.3 | -0.003, -0.27, 9 |
| c_crit_h0 4 | 0.847 | 5 | 0.792 | 17.7 | 37.4 | 148.4 | 3.83 | 569 | 9.8 | 7.0 | +0.000, 0.02, 11 |
| critical-first from h14 | 0.840 | 4 | 0.778 | 12.2 | 26.6 | 154.9 | 3.89 | 602 | 10.4 | 6.4 | -0.007, -0.73, 11 |
| critical-first from h18 | 0.848 | 6 | 0.774 | 18.2 | 34.6 | 147.6 | 3.87 | 572 | 9.3 | 5.8 | +0.002, 0.25, 9 |
| c_h23w | 0.845 | 5 | 0.781 | 18.1 | 36.1 | 149.7 | 3.90 | 583 | 8.8 | 6.2 | -0.002, -0.67, 9 |
| c_wmaxd 7 | 0.847 | 6 | 0.785 | 13.3 | 30.6 | 143.3 | 3.93 | 564 | 8.6 | 5.2 | -0.000, -0.01, 11 |
| c_wmaxd 6 | 0.850 | 7 | 0.794 | **6.0** | **20.2** | 128.9 | 3.95 | 509 | 6.8 | 4.3 | +0.003, 0.47, 9 |
| c_far 1 (carrot far) | 0.841 | 6 | 0.784 | 18.2 | 35.3 | 167.9 | 3.89 | 654 | 9.5 | 6.2 | -0.006, -1.23, 6 |
| c_far 2 (tomato far) | 0.848 | 6 | 0.783 | 19.8 | 40.1 | 159.8 | 3.96 | 632 | 10.0 | 5.3 | +0.001, 0.19, 12 |
| c_far 3 | 0.831 | 6 | 0.777 | 18.6 | 39.8 | 176.2 | 3.96 | 697 | 8.9 | 7.7 | -0.016, -2.34, 6 |
| c_far 7 | 0.804 | 5 | 0.741 | 17.7 | 40.0 | 205.9 | 3.97 | **817** | 9.0 | 7.0 | -0.043, -3.61, 6 |
| c_car2_d 5 | 0.851 | 7 | 0.787 | 22.2 | 37.6 | 143.9 | 3.90 | 562 | 9.8 | 5.0 | +0.005, 1.17, 10 |
| c_car2_d 4 | 0.854 | 7 | 0.785 | 20.3 | 34.6 | 146.1 | 3.90 | 569 | 9.9 | 3.0 | +0.007, 1.48, 12 |
| c_car2_d 3 | 0.852 | 6 | 0.785 | 21.6 | 35.4 | 141.4 | 3.85 | 545 | 9.3 | 2.3 | +0.005, 1.11, 12 |
| c_car2_d 0.5 (all) | 0.849 | 5 | 0.787 | 21.5 | 35.4 | 138.0 | 3.86 | 533 | 9.2 | 2.3 | +0.002, 0.43, 8 |
| c_wlast 26 | 0.851 | 6 | 0.785 | 17.7 | 34.8 | 141.8 | 4.03 | 571 | 0.6 | 5.8 | +0.004, 1.34, 15 |
| c_wlast 25 | 0.846 | 6 | 0.781 | 16.3 | 32.5 | 133.2 | 4.04 | 538 | 0.1 | 5.7 | -0.001, -0.40, 10 |
| **c_car2_d 4 + c_wlast 26** | **0.859** | 7 | 0.788 | 19.0 | 32.9 | 140.5 | 4.01 | 563 | 1.4 | 3.0 | **+0.0123, t 2.36, 13/20, +1,425/board** |
| + c_wmaxd 7 | 0.854 | 6 | 0.789 | 13.1 | 26.7 | 133.2 | 4.07 | 542 | 0.6 | 2.7 | +0.007, 1.42, 14 |
| + c_h23w | 0.853 | 7 | 0.782 | 17.6 | 31.6 | 142.6 | 3.99 | 568 | 1.1 | 3.0 | +0.006, 1.24, 12 |

TUNE20 confirmation (the cell was chosen on HOLD20; logs/cells_t1.txt, logs/pooled40.txt):

| cell | TUNE20 coins | value | wDth | allD | wheat harv | u/h | wheat open | carrot deaths | TUNE20 d(ratio), t, up | pooled HOLD+TUNE n 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| MMPQ | 1.000 | 1.000 | 1.4 | 21.4 | 176.4 | 4.73 | 0.0 | 0.3 | | |
| crew | 0.784 | 0.780 | 19.9 | 38.8 | 136.8 | 3.85 | 10.1 | 5.7 | | |
| c_car2_d 4 | 0.781 | 0.785 | 20.8 | 37.1 | 132.0 | 3.83 | 8.2 | 3.9 | -0.003, -0.75, 11 | +0.0017, t 0.50, 23/40 |
| c_wlast 26 | 0.787 | 0.781 | 18.4 | 36.4 | 131.2 | 3.97 | 0.8 | 5.2 | +0.003, 1.64, 14 | **+0.0035, t 2.02, 29/40, +415/board** |
| c_car2_d 4 + c_wlast 26 | 0.786 | 0.788 | 19.8 | 35.5 | 125.9 | 3.96 | 0.6 | 3.6 | +0.002, 0.42, 11 | +0.0071, t 2.02, 24/40, +935/board |

The HOLD20 +0.0123 (t 2.36) does not replicate on TUNE20 (+0.002, t 0.42): it was the best of 21 cells read on the same 20 boards. The carrot part is noise (pooled t 0.50). Only `c_wlast 26` is positive on both sets (+0.004 and +0.003; pooled +0.0035, t 2.02, 29/40 up), about +400 coins a board, and it too was picked from several cells.

**Reading.**
- **Deaths are a symptom, not the lever.** The crew is labour-bound. Stopping the deaths by forcing the visit (critical-first h14: wheat deaths 18.4 -> 12.2, +23 wheat units) or by not planting the far wheat (c_wmaxd 6: all deaths 36.5 -> 20.2, MMPQ's 19.0) is coins-neutral (-0.007 / +0.003). The far wheat's survivors roughly pay for its deaths.
- **Wheat volume is not the lever either.** c_far 7 (demand crops to the far tiles, wheat near) lifts wheat to MMPQ's 817 units harvested and 488 sold, and loses 0.043 (t -3.61): carrot sales fall 99 -> 45 and strawberry 197 -> 118. On sales revenue the executor's gap to MMPQ is wheat -7.3k, carrot -5.0k, tomato -4.2k, melon -1.0k, egg -1.0k a game; the carrot and tomato parts are demand-crop acreage (42 vs 74 carrot, 13 vs 22 tomato plantings), not deaths.
- **What pays, barely, is dropping a loss that costs labour for nothing:** the d27 wheat that is planted and watered but never harvested (`c_wlast` 26). The carrot that decays after a wasted age-2 visit (`c_car2_d`) is saved (carrot deaths 6.2 -> 3.0) but at 2 units instead of 3, and the net is noise.

**The per-hand rules.**
1. **Stops the top cause (wheat dry at age 2 and 4, far tiles):** a dry-yesterday plant gets the nearest free hand before new work from h14. This is critical-first (`c_cf_h` 14). It cuts wheat deaths by a third (18.4 -> 12.2) and adds 23 wheat units, and it reads -0.007 (t -0.73). Not planting wheat at shed distance ≥ 6 (`c_wmaxd` 6) removes two-thirds of all deaths (36.5 -> 20.2, MMPQ 19.0) and reads +0.003 (t 0.47). Neither pays: the labour comes out of carrots, fertiliser and harvest elsewhere.
2. **Does pay, barely:** no wheat planting after d26. A d27 wheat needs a d29 harvest visit that the crew does not make 45 % of the time.
3. **Tried, noise:** a hand that waters a carrot at age ≥ 2 on a tile at shed distance ≥ 4 harvests it in the same visit (5.35 of our 42 carrots a game decay unvisited on age 3-4, against MMPQ's 0.35 of 74).
4. **Bug-like, fixed, neutral:** at h23, WATER comes before FERTILIZE (`c_h23w`). This removes the 1.35 h23 fertilise-then-die a game but reads -0.002.

**What the next builder should take.** Survival is not the executor's coins gap. The labour-bound crew loses the same coins whichever work it drops. Wheat volume is not the gap either (c_far 7 reaches MMPQ's wheat and loses 0.043). The revenue gap is wheat -7.3k, carrot -5.0k and tomato -4.2k a game. Its carrot and tomato parts are demand-crop acreage (plantings 42 vs 74 carrot, 13 vs 22 tomato). The yield gap is the fertilised age-4 wheat cycle: MMPQ has 56 a game at 6 units, we have 3, because `c_unf3` takes unfertilised wheat out at age 3. A cell must move the ratio on BOTH sets. HOLD20 alone selected a +0.012 that was noise.

## Files

- Scripts: S/plantdeath1/scripts/plantext.py (life-cycle extraction), ana.py (causes, visits, patterns), ana2.py (open plantings, distance, op mix, yield decomposition), cells.py (paired cells), patch.py (the knob patch).
- Logs: S/plantdeath1/logs/ana_h20.txt, ana2_h20.txt, cropdist_h20.txt, cells_k1.txt, cells_k2.txt, cells_k3.txt, cells_t1.txt, pooled40.txt.
- Code: /mnt/e/_work/kagg3_wt_plantdeath1 (branch plantdeath1_0930 off cf1b9790, commit 4e4b2b12), `src/kagg3/prog/direct.py`: `c_car2_d`, `c_wlast`, `c_wmaxd`, `c_far`, `c_h23w`, all default OFF, OFF byte-identical on HOLD20.
- Slips: none (checkpoint timestamps written from memory twice and corrected from `date -u`).
