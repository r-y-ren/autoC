# RESERVEFIX1 (2026-09-30 18:54-20:05Z): does the unfunded-animal tile reservation cost plantings, and does removing it gain wins? Verdict: NONE (kill), no package

Stream dir `S/reservefix1/`. Code: branch `reservefix1_0930` off master fe602a07 (vrp26), sparse worktree /mnt/e/_work/kagg3_wt_reservefix1, commit 4e625481. Remote stage /home/user/stage_r/reservefix1 (pkg/rf = CONFIRM1's unpacked vrp26 package + the patched plan.py/runtime.py; pkg/rf5 = LATCHHERD1 fe00dbed files + the same patch; pkg/rf6 = fix-grid knobs). Judge: HARNESS2 v4 H mode (G25 wool gate), 2 remote workers, nice 19 + ionice idle, load < 12 at launch. V56: local 1 worker, S/vband1 vr.py. Master, shipped files and live packages untouched.

**Answer.**
- **The trigger's bug does not cost the shipped PFS a single planting it asked for.** On the 40 P48 screen seats (vrp26, OFF, census logged in shadow), an unfunded animal ask reserves fresh tiles on 40/40 games (4.35 tiles/game over d2-9, peak d7: 38/40 games, 2.80 tiles). But the reservation clips the brain's own plant target on **0 of 152 reservation days: 0.000 lost plantings/game** (kill number < 0.3). The same holds with LATCHHERD1's S1 floor on (R5: 0 of 245 days).
- **Why:** `brain.decide` sizes `plant_total = n_dev - sum(animal_want)` with `n_dev = dev_frac * n_free`. The target is already net of the animal ask and sits well under the free tiles (d4-6 free slots 13.8 / 29.8 / 17.9 against total targets 11.9 / 19.3 / 12.6; V56 m40: 0 of 132 days). The tiles the reservation holds are tiles the brain never asked to plant.
- **The d4-6 strawberry shortfall is PURSE-bound, not tile-bound.** Strawberry ask 6.6 / 16.2 / 10.1 against funded 3.7 / 8.4 / 6.1 = **14.7 unfunded strawberry plantings per game** on d4-6. Per-day purse table in section 5.
- **Releasing the tiles = planting beyond the brain's ask, and it loses.** Every cell that plants the freed tiles loses on the P48 screen: R1 -533 (t -1.83), R2 -519 (t -1.88), R3 -626 (t -1.91), R4 = R2 byte-identical, F1 -290, F3 -449. The one cell that plants nothing new (F2, held seed only) is a no-op, +10 (t 0.29).
- **On V56, R2:** v21 -597 (t -1.88), W 15 -> 14; m40 -269 (t -0.61), W 38 -> 39.
- **R5 (R2 + LATCHHERD1 S1H0, the coordinator's optional cell):** +28 (t 0.08) vs vrp26, with strawberry d15-17 -2.55 units (t -2.92).
  - Against S1H0's own rows: own -523 (t -2.15), strawberry plantings d4-7 **+0.00**, strawberry units d15-17 +0.03.
  - The fix recovers none of S1H0's strawberry loss. That loss is the purse the sheep take on d5-6, not a reserved tile. This refutes LATCHHERD1's mechanism 2 and its fix-grid item 1.
- **Next cell (for STRAWFUND1):** fund the d4-6 strawberry ask from the purse. On d5 the purse goes to the quadrant (land), the cow and 8.4 strawberry seeds at about 100 coins each (section 5). The guards must hold: late animal units d18-29, the V56 m40/v21 read, and THE INVARIANT.

## 1. The switch
- **`plan.SEED_ROOM_AFFORD_ON` (default False).** After the day's grant, on the final `_derive` pass (`ask_fill`, crew already chosen), `_seed_room_afford` re-counts the fresh-tile reservation on the funded herd:
  - `"grant"` (R2) counts `a_have + n_buy[animals]`, the planner's own purse net of the hire bill, the crew reserve, land and the planned seed spend.
  - `"dawn"` (R1) counts the heads affordable at the dawn purse, in list order.
- **The freed tiles** (`min(freed, spare room)`) join the plant target in its own mix (`_fill_plant`). Under `SEED_ROOM_AFFORD_STRAW` (R3) they go to strawberry on d4-7 instead.
- **Their seed** is bought from the unspent purse one marginal unit at a time, at its own rank (the `_ask_fill` ratio walk, bounded per crop by the new target). Every existing grant stands; no hire, land or animal moves.
- **R4** (`SEED_ROOM_AFFORD_PROG`) acts on programme seats only. A runtime latch at d2h0 fires when the rival holds 1-10 MELON plantings (the LATCHHERD1 rule).
- **Fix-grid knobs:**
  - `SEED_ROOM_AFFORD_DAYS` (F1 = d10-29).
  - `SEED_ROOM_AFFORD_BUY=False` (F2: held seed only).
  - `SEED_ROOM_AFFORD_MAX=1` (F3: at most one tile/seed a day).
- **Census:** `SEED_ROOM_AFFORD_LOG` (dict) records per day the asks, the funded heads, cap_ask and cap_fund, the targets, plant_eff, builds and free slots, plus the per-list grant spend. It is computed in shadow when the switch is OFF and does not change play.
- **Code versions:**
  - The remote screen trees ran plan f65f513d (R1-R4) and 9eb6e121 (F1-F3).
  - The committed plan fc397a6d has identical play; it adds the knobs, the `fi` flag and the census spend fields.
  - runtime 81496e01.

## 2. Identity and guards
| check | result |
|---|---|
| OFF + census log (pkg/rf) vs HARNESS2 v26H rows, H mode | **40/40 exact**: sim_ours, sim_opp, ndiff, first divergence and sales ledger |
| OFF + census log, V56 m40 (local, tmp/rf_log) vs STACK1 v_hAC | **40/40 exact** on all 12 money columns (W 38/40); the same run feeds the section 5 V56 table |
| OFF + census log, local HARNESS2 H (res_daytab P48 run) vs v26H | **40/40 exact** |
| R4 latch on the P48 screen | fired 40/40 and before the first fix day (d5), so R4 = R2 byte-identical on all 40 seats |
| R5 LATCH_HERD latch | fired 40/40 |
| apply (per-game act p99, remote, load 8-10) | OFF median 311 ms, max 350. R1 314 / 367, R2 318 / 377, R3 307 / 355, R5 312 / 346, F1-F3 max 395. Max single call 876 ms (F2). Bar < 650 on p99: passed. |
| errors | V56 R2 o_err = t_err = 0 (61 games). hrun catches agent exceptions silently, as in LATCHHERD1; ON behaviour logs show normal play. |

## 3. Census (STEP 0): vrp26 OFF, 40 P48 screen seats, shadow computation
| window | games with an unfunded ask that reserves tiles | reserved tiles / game | brain-target plantings blocked / game | extra plantings the freed tiles could take with fundable seed / game (beyond the ask) |
|---|---|---|---|---|
| d2-9 | 40/40 (100 %) | 4.35 | **0.000** (0 of 92 reservation days) | 2.02 (wheat 1.60, carrot 0.20, strawberry 0.15, melon 0.08) |
| d4-7 | 40/40 | 4.08 | **0.000** | 1.77 (strawberry 0.12) |
| d0-29 | 40/40 | 6.88 | **0.000** (0 of 152) | 3.48 |

Notes:
- My first census line counted the last column as "lost plantings" (2.02/game). The screen then showed that those plantings are extra development, not the brain's ask.
- The correct measure (does the reservation clip `sum(plant_target)` below the target?) is 0 on OFF, on R2 (0 of 150) and on R5 with the S1 sheep floor (0 of 245).
- Per day (OFF, 40 seats; the unfunded ask is always the purse, never the value gate):
  - d5: 15 games, 0.38 reserved tiles.
  - d6: 28 games, 0.90.
  - d7: 38 games, 2.80.
  - d8: 12 games, 0.28.
  - d10: 7 games, 0.42.
  - d11: 18 games, 1.07.

## 4. Screen: named grid + fix grid (first 40 P48 seats of P48TAPE172, HARNESS2 v4 H, paired)
Columns as LATCHHERD1 (rows = arm minus vrp26 v26H rows; stress = net flips after a 2,300-coin adverse shift on the arm; straw = our strawberry units sold d15-17; animal = our egg+milk+wool units d18-29). All 40 pairs are faithful for every cell.

| cell | what | own (t) | rival (t) | margin vs vrp26 (t) | W 14 -> | flips (net) | stress | margin vs vrp25 (t) | net vs vrp25 | straw d15-17 (t) | animal d18-29 (t) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | dawn-purse reservation | -476 (-2.00) | +57 (+0.42) | **-533 (-1.83)** | 13 | +0 -1 (-1) | -3 | -423 (-1.46) | -1 | +0.05 (+0.12) | -2.1 (-0.87) |
| R2 | grant-funded reservation | -584 (-2.53) | -66 (-0.38) | **-519 (-1.88)** | 14 | +1 -1 (0) | -3 | -409 (-1.48) | 0 | +0.15 (+0.39) | -5.4 (-1.94) |
| R3 | R2, freed tiles to strawberry d4-7 | -331 (-1.87) | +295 (+0.93) | **-626 (-1.91)** | 13 | +0 -1 (-1) | -3 | -516 (-1.54) | -1 | +0.12 (+0.32) | -2.5 (-1.19) |
| R4 | R2 on programme seats | = R2 (fires 40/40) | | **-519 (-1.88)** | 14 | 0 | -3 | -409 | 0 | +0.15 | -5.4 |
| R5 | R2 + LATCHHERD1 S1H0 | -396 (-1.26) | -424 (-1.91) | **+28 (+0.08)** | 16 | +2 -0 (+2) | -2 | +138 (+0.42) | +2 | **-2.55 (-2.92)** | -1.9 (-0.76) |
| F1 | R2 from d10 | -119 (-0.49) | +171 (+1.43) | **-290 (-1.19)** | 13 | +0 -1 (-1) | -3 | -180 (-0.65) | -1 | +0.62 (+2.24) | -0.1 (-0.08) |
| F2 | R2, held seed only (no buy) | -14 (-0.29) | -24 (-0.85) | **+10 (+0.29)** | 14 | 0 | -3 | +120 (+0.96) | 0 | +0.25 (+1.71) | +0.1 (+0.28) |
| F3 | R2, at most 1 tile/day | -304 (-1.38) | +144 (+1.12) | **-449 (-1.70)** | 13 | +0 -1 (-1) | -3 | -339 (-1.26) | -1 | +0.47 (+1.26) | -6.6 (-2.88) |

- **No survivor** (own >= 0 and net flips >= 0): R1-R4 and F1/F3 have own < 0. R5's own is -396. F2 is a no-op (it buys 0 seeds; held seed is idle on only 0.04-0.09 tiles per game-day).
- Confirmation (P48 c132 + PQ4 18) was therefore not run.
- V56 was run for R2 only (below). R1/R3/R5/F cells are screen failures. R4 on V56 would be byte-identical wherever the latch does not fire.

**V56 (local, vr.py reacting V56 bank agent, seat 0, paired vs STACK1 hAC = vrp26):**
| cell | set | n | exact | W vrp26 -> arm | flips | margin (t) | own (t) | errors |
|---|---|---|---|---|---|---|---|---|
| R2 | v21 | 21 | 4 | 15 -> 14 | +0 -1 | -597 (-1.88) | -256 (-0.55) | 0 |
| R2 | m40 | 40 | 3 | 38 -> 39 | +1 -0 | -269 (-0.61) | -73 (-0.18) | 0 |

## 5. Where the d4-7 purse goes (vrp26 OFF, per game-day means)
This table was asked for by the coordinator for STRAWFUND1.
- "straw ask" is the brain's strawberry `plant_target`; "funded" is `plant_eff` (the seed the day holds or buys and plants), and "unfunded" is the difference.
- "planner purse" is what `budget.grant` may spend: dawn money - wages - reserve - land gap, where the gap is the land price less projected revenue.
- The spend columns are the grant's engine-curve coins per list. "Left" is unspent.
- "land" is the price of a quadrant bought that day, averaged over games.

### P48 screen 40 (HARNESS2 v4 H, vrp26 OFF) (40 games)
| day | straw ask | funded | unfunded | free slots | dawn purse | wages | reserve | land | planner purse | animals g/c/s (coins) | animals asked / bought (heads) | feed wheat | fert | seed wht | seed car | seed tom | seed str | seed mel | left |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d3 | 4.7 | 3.2 | 1.5 | 8.0 | 622 | 12 | 20 | 0 | 590 | 0 / 0 / 0 | 0.00 / 0.00 | 183 | 0 | 20 | 0 | 0 | 322 | 0 | 65 |
| d4 | 6.6 | 3.7 | 2.9 | 13.8 | 616 | 8 | 13 | 0 | 594 | 0 / 0 / 0 | 0.00 / 0.00 | 130 | 0 | 43 | 18 | 0 | 372 | 0 | 30 |
| d5 | 16.2 | 8.4 | 7.8 | 29.8 | 1398 | 11 | 19 | 1000 | 1165 | 0 / 220 / 0 | 0.93 / 0.55 | 0 | 0 | 27 | 2 | 0 | 842 | 24 | 50 |
| d6 | 10.1 | 6.1 | 4.0 | 17.9 | 1078 | 10 | 16 | 0 | 1052 | 15 / 160 / 25 | 1.40 / 0.50 | 107 | 0 | 10 | 7 | 2 | 608 | 86 | 32 |
| d7 | 2.0 | 1.0 | 1.0 | 12.0 | 665 | 17 | 28 | 0 | 621 | 22 / 110 / 12 | 3.17 / 0.38 | 186 | 0 | 28 | 5 | 0 | 98 | 76 | 83 |
| d8 | 1.2 | 1.2 | 0.1 | 10.8 | 1948 | 45 | 73 | 0 | 1830 | 120 / 310 / 738 | 2.95 / 2.65 | 28 | 0 | 33 | 1 | 0 | 120 | 106 | 375 |
| d9 | 0.5 | 0.5 | 0.0 | 5.2 | 1559 | 69 | 112 | 0 | 1379 | 98 / 70 / 162 | 0.82 / 0.82 | 0 | 0 | 21 | 0 | 0 | 52 | 40 | 935 |

- Strawberry seed is a flat 100 coins on d3-7.
- The d5 quadrant is bought on **40/40** games at 1,000. The grant is charged only the gap (price less projected same-day revenue): dawn 1,398 - wages 11 - reserve 19 - gap about 203 = 1,165.
- **Unfunded strawberry d4-6 = 2.9 + 7.8 + 4.0 = 14.7 plantings (1,470 coins) a game.**
- The purse the grant spent instead:
  - d4: feed wheat 130 and wheat/carrot seed 61.
  - d5: cow 220 (0.55 head), plus the land gap.
  - d6: animals 200, feed 107 and melon seed 86.
- The reservation for unfunded asks clips the brain's target on 0 of 152 days.

### V56 m40 (vr.py reacting V56, vrp26 OFF) (40 games)
| day | straw ask | funded | unfunded | free slots | dawn purse | wages | reserve | land | planner purse | animals g/c/s (coins) | animals asked / bought (heads) | feed wheat | fert | seed wht | seed car | seed tom | seed str | seed mel | left |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d3 | 4.2 | 3.0 | 1.2 | 8.0 | 611 | 12 | 20 | 0 | 579 | 0 / 0 / 0 | 0.00 / 0.00 | 180 | 0 | 28 | 0 | 0 | 300 | 0 | 71 |
| d4 | 4.0 | 4.0 | 0.0 | 13.2 | 613 | 12 | 20 | 0 | 581 | 0 / 0 / 0 | 0.00 / 0.00 | 92 | 0 | 70 | 5 | 0 | 400 | 0 | 14 |
| d5 | 10.6 | 8.7 | 1.9 | 27.0 | 1378 | 12 | 20 | 1000 | 1346 | 0 / 330 / 0 | 1.00 / 0.82 | 0 | 0 | 86 | 0 | 0 | 868 | 0 | 62 |
| d6 | 6.9 | 5.0 | 1.9 | 9.8 | 859 | 17 | 28 | 0 | 814 | 0 / 30 / 100 | 0.57 / 0.28 | 143 | 0 | 2 | 9 | 2 | 498 | 0 | 31 |
| d7 | 1.5 | 1.1 | 0.5 | 6.8 | 674 | 21 | 34 | 0 | 619 | 0 / 80 / 50 | 1.68 / 0.30 | 180 | 0 | 16 | 4 | 0 | 105 | 0 | 184 |
| d8 | 0.8 | 0.8 | 0.0 | 10.0 | 2138 | 49 | 80 | 0 | 2009 | 82 / 230 / 1188 | 3.45 / 3.23 | 0 | 0 | 42 | 0 | 0 | 75 | 0 | 392 |
| d9 | 0.8 | 0.8 | 0.0 | 9.8 | 1697 | 61 | 99 | 0 | 1537 | 112 / 180 / 450 | 2.25 / 1.73 | 0 | 0 | 37 | 1 | 0 | 82 | 134 | 540 |

- On the V56 boards the d4-6 strawberry ask is smaller and better funded: 4.0 / 10.6 / 6.9 against 4.0 / 8.7 / 5.0, so **3.8 unfunded plantings a game**.
- The d5 quadrant is bought on the same day at the same price.
- The d5 cow is bigger: 330 coins, 0.82 head.
- The reservation for unfunded asks: 39/40 games, 2.60 tiles d2-9 a game, and it clips the brain's target on **0 of 132 days**.

## 6. Behaviour ledger (arm minus OFF, same harness, per game; P48 screen 40)
| cell | games / days the fix acted | fix seed buys (crop) | plantings d2-9 | plantings d10-28 | herd g/c/s d10 | animals bought g/c/s | egg/milk/wool units d18-29 | own / rival |
|---|---|---|---|---|---|---|---|---|
| R1 | 36 games; d7 36, d6 5, d11 7 | wheat 1.40, carrot 0.12, straw 0.05 | wheat +0.32, straw +0.05, melon -0.15 | wheat +0.30, melon +0.28, straw -0.12 | -0.10 / -0.05 / 0 | -0.05 / +0.02 / +0.08 | -2.9 / +0.7 / +0.2 | -476 / +57 |
| R2 | 40; d5 15, d6 29, d7 38, d8 10, d11 17 | wheat 2.70, carrot 0.32, melon 0.30, straw 0.15 (d7 1.62) | wheat +0.35, straw +0.12, melon -0.12 | wheat +0.78, carrot +0.52 | -0.20 / -0.08 / -0.08 | -0.18 / +0.05 / -0.08 | **-6.1** / +0.8 / 0 | -584 / -66 |
| R3 | 40 | wheat 1.55, straw 0.57, carrot 0.18 | **straw +0.40**, melon -0.18 | wheat +0.70, carrot +0.70, straw -0.15 | -0.05 / -0.05 / -0.05 | -0.08 / -0.10 / -0.10 | -2.0 / -0.8 / +0.3 | -331 / **+295** |
| R5 vs OFF | 40 | wheat 2.72, straw 0.30 | wheat +1.25, **straw -0.50**, melon -0.38 | straw +0.48, wheat -0.55 | -0.08 / -0.15 / **+0.50** | -0.02 / -0.02 / +0.12 | -3.5 / +0.4 / +1.3 | -396 / -424 |
| F1 | 28 (d10+) | wheat 1.18 | 0 | wheat +0.55, carrot +0.42 | 0 / 0 / 0 | 0 / 0 / -0.22 | +0.1 / +0.2 / -0.3 | -119 / +171 |
| F3 | 40 | wheat 1.68 | wheat +0.38, straw +0.10 | carrot +0.25, melon +0.25 | -0.10 / -0.05 / +0.02 | -0.15 / -0.05 / 0 | -4.6 / -1.9 / -0.1 | -304 / +144 |

**What the ledger says**
1. **The freed tiles are not the constraint that binds the day.**
   - R2 buys 3.97 extra seeds a game, 1.62 of them wheat on d7. Only +0.33 of them are planted d2-9; the rest wait in the shed and are planted d10+.
   - The d7 crew has no spare turns for them: labour binds, not tiles.
2. **The seed spend delays the herd.**
   - R2 has geese -0.20 at d10 and -0.18 bought, which costs **egg units -6.1 d18-29** (-366 egg revenue).
   - This is THE INVARIANT again: a coin that leaves the early purse for extra wheat is paid for in late animal volume.
3. **Strawberry on the freed tiles does not reach the d15-17 wall.**
   - R3 plants +0.40 strawberry d2-9 for +0.12 units d15-17. The rival purse rises +295: our extra crops drag the shared curve.
4. **R5: the S1H0 strawberry loss is the sheep's purse.**
   - R5 vs S1H0: strawberry plantings d4-7 +0.00, units d15-17 +0.03, own -523 (t -2.15).
   - The d5-6 sheep (+0.45 sheep at d8) take the coins the strawberry seed needed. No tile was ever reserved against the strawberry ask.

## 7. Next cell (proposed, for STRAWFUND1)
**Target:** the d4-6 strawberry ask is 14.7 plantings/game short of funded (P48), with 14-30 free slots. The coins are the constraint.

**Where d5's purse goes (section 5):**
- the quadrant bought that day;
- the cow (0.43-0.55 heads, about 171-220 coins);
- about 100 coins per strawberry seed on the engine curve.

**Cells, one named grid:**
- (a) Strawberry list ahead of the animal lists in the d4-6 grant.
- (b) Defer the d5 quadrant to d8, when the dawn purse jumps to about 1.8-1.9k.
- (c) (a) + (b).

**Guards:**
- animal units d18-29 not below control, since the d5 cow is the late milk;
- V56 m40 >= 38/40, v21 >= 15/21;
- the strawberry d15-17 units must rise, not just the plantings. R3's +0.40 plantings gave only +0.12 units.

## 8. Files
- **Scripts (`S/reservefix1/`):**
  - `patch_plan.py` / `patch_rt.py`: the switch patch.
  - `hrun_rf.py` / `hrun_rf_local.py`: the HARNESS2 hrun plus the `lh` logs, RF_ARM and the per-day `rf` census.
  - `rf_census.py`: the census.
  - `rf_summ.py`: paired tables (= LATCHHERD1 lh_summ.py).
  - `rf_ledger.py`: the ledger.
  - `rf_daytab.py`: the section 5 table.
  - `vcmp.py`: V56 paired read.
  - `vchain.sh` and `lchain.sh`: the local chains.
- **Remote queue:** `remote/` (q.sh, launch.sh, queue.txt).
- **Rows:**
  - `rres/` has offH/R1-R5/F1-F3 screen rows and offL_scr40, the local OFF census with spend.
  - `res/` has the V56 csv plus m40_offlog_rf.jsonl.
- **Outputs:** `res_census_off40.txt`, `res_screen.txt`, `res_daytab.txt`.
- **Tree and notes:** `tmp/` holds the local package trees (not committed). Also `checkpoint.txt` and `slips.txt`, which has 2 slips: a `<(...)` process substitution in a local no-op diff, and a remote `2>/dev/null` in a wait loop. Both are logged and neither was repeated.
