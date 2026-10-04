# TOMATOFILL1 (2026-09-25, 05:39-07:50Z): VRP-freed labour -> TOMATO fill plantings. NO SHIP (gift + displaced plantings)

Branch `tomatofill1` (master e9f09d19), worktree `/mnt/e/_work/kagg3_wt_tomatofill1`. Question (YIELD1): ENGINE seats plant
709 tomatoes vs our 315 per 59 boards at equal per-plant yield, so does filling the router's slack with TOMATO pay?
Tools `S/tomatofill1/`: dev.py (ROUTEFILL1 measure.py + SAFETY_S 1e9 + census), fresh.py, lane.sh, grid.sh, ctl.sh,
legs.sh, tape.sh/tapes_after.sh, pair.py, tpair.py, table.py; outputs in `out/`, bases in `base/`.

## 1. Support check + fixes (behind the fill knobs; defaults unchanged, "ii" never passes fills)
- `route_vrp.LIFE` had no TOMATO (KeyError). Added `TOMATO: 10`: ongoing crop, first yield at age 8, 4 productions on nights
  pd+7..pd+10. The window cap `day <= N_DAYS-2-LIFE` keeps fills at d18 or earlier so they finish all 4 productions by d28.
  Ledger tend: `EXTRA = {"TOMATO": 1.0}` turn/day on top of ROUTE_FILL_TEND covers fert + the repeat harvests.
- Seeds: `_seed_slot` bumps or adds a BUY_SEED row for any crop, so it works for TOMATO (cost 50). Fert, water and harvest
  after planting day are the planner's own (tile-state driven). Measured tomato death rate 0.14-0.28 per game vs base 0.28.
- **BUG, fixed: VERIFY (SALEPIN1, `ROUTE_VRP_VERIFY`, added after ROUTEFILL1) required the rewritten day's (tile, op) multiset
  to EQUAL the planner's.** Every fill day failed VERIFY and fell back to the planner's plan. Smoke on 3 boards: ii_fill CARROT
  gave 0 fills and 13-15 verify_fail per game (base: 0-1). So every ROUTE_FILL_* run after SALEPIN1 has been fill-free.
  `verify(..., fills)` now allows exactly one DIG / PLANT(crop) / WATER on each committed fill tile. After the fix: CARROT
  6-22 fills/game on the same 3 boards, verify_fail 0-1. Diagnostic counters fill_call/nocand/capbrk/seedbrk/noins go in `stats`.
- Byte-identity: master base 87-13 ledger (CONTEST1 dev_k0d0, which equals VRPREPAIR1 base_0/50 by md5). This tree's OFF arm
  matches it: md5 on 3 boards, then all 100 boards (+0/-0, identical money). CAP=0 controls of both modes also match on 100/100,
  so every delta below comes from the fills. Tests: test_route_fill.py + test_route_vrp.py pass (10 + 1 skip).

## 2. Grid, dev100 exact sim (LIVE250 0-99, simgap1 guard vs reacting V56, SAFETY_S 1e9 both arms; paired vs master base)
| cell (mode, TOMATO, DAYS, CAP) | W 87-13 -> | net flips | Δours (t) | Δtheirs (t) | Δmargin (t) | tom plantings/g | tom units harv/g | fills/g | hires/g | died/g |
|---|---|---|---|---|---|---|---|---|---|---|
| base (master) | 87 | 0 | 0 | 0 | 0 | 7.7 | 43.7 | 0 | 234.1 | 0.28 |
| ii_fill (3,13) 3 | 79 | +0/-8 = -8 | +497 (1.50) | +1,756 (6.08) | -1,259 (-5.11) | 11.2 | 75.8 | 6.1 | 234.1 | 0.18 |
| ii_fill (3,13) 6 | 79 | +0/-8 = -8 | +494 (1.50) | +1,762 (6.09) | -1,268 (-5.14) | 11.2 | 75.8 | 6.1 | 234.1 | 0.18 |
| ii_fill (10,25) 3 | 82 | +0/-5 = **-5** | -271 (-1.29) | +793 (4.55) | -1,064 (-5.91) | 10.0 | 66.4 | 5.0 | 234.0 | 0.14 |
| ii_fill (10,25) 6 | 82 | +0/-5 = **-5** | -273 (-1.30) | +828 (4.76) | -1,102 (-6.03) | 10.1 | 66.7 | 5.0 | 234.2 | 0.18 |
| hybrid (3,13) 3 | 76 | +0/-11 = -11 | +3 (0.01) | +2,348 (6.99) | -2,345 (-7.18) | 12.6 | 89.4 | 8.4 | 234.9 | 0.24 |
| hybrid (3,13) 6 | 75 | +0/-12 = -12 | +24 (0.06) | +2,344 (7.47) | -2,320 (-7.67) | 12.7 | 90.9 | 8.6 | 235.0 | 0.28 |
| hybrid (10,25) 3 | 79 | +0/-8 = -8 | -353 (-1.31) | +1,353 (5.71) | -1,706 (-6.44) | 10.9 | 74.4 | 6.4 | 233.7 | 0.20 |
| hybrid (10,25) 6 | 75 | +0/-12 = -12 | -379 (-1.45) | +1,546 (5.70) | -1,925 (-6.76) | 10.9 | 75.2 | 6.5 | 234.2 | 0.22 |
No cell has a single up-flip. The CAP barely binds: fills stop at the ledger limit (capbrk) and at the land limit (nocand).
Net plantings vs base per game (w/c/t/s/m), ii_fill (10,25) 3: -1.6/+0.9/+2.3/-0.4/-0.7; hybrid (3,13) 3:
-1.7/+2.2/+4.9/-1.1/-0.7. Each fill displaces about half a planner planting, and those are wheat, strawberry and melon.
Sale revenue moves -248 / -135 per game even with +23..+46 tomato units harvested.

## 3. Legs (the 2 best cells = ii_fill (10,25) CAP 3 / CAP 6; bases = VRPREPAIR1 master-OFF base_100/150, FB)
| cell | leg | W | net flips | Δours (t) | Δtheirs (t) | Δmargin (t) |
|---|---|---|---|---|---|---|
| CAP 3 | held-out100 (100-199) | 86 -> 79 | +1/-8 = **-7** | +28 (0.14) | +736 (4.26) | -708 (-3.14) |
| CAP 6 | held-out100 | 86 -> 79 | +1/-8 = -7 | -11 (-0.05) | +804 (4.51) | -816 (-3.26) |
| CAP 3 | FRESH300 | 250 -> 227 | +3/-26 = **-23** | -230 (-1.96) | +769 (7.52) | -998 (-7.58) |
| CAP 6 | FRESH300 | 250 -> 227 | +3/-26 = -23 | -249 (-2.00) | +784 (7.62) | -1,033 (-7.45) |
| CAP 3 | band tapes dev50 (100 games, engine, base = VRPREPAIR1 master-OFF csv) | 86 -> 87 | +3/-2 = +1 | +411 (2.56) | +720 (**5.24**) | -309 (-1.91) |

## 4. VERDICT: NO SHIP. Mechanism = GIFT plus displaced plantings; not died, not labour
Every sim cell and leg loses: dev -5..-12, held -7, FRESH -23. Tapes are +1, but on a gift (theirs t 5.2). Theirs rises +0.7..+2.3k (t 4.3-7.6) in every cell, and
ours is flat or down. The fills do grow (+2.3..+4.9 net tomato plantings, +23..+46 units harvested, death rate no higher than
base), but (a) about half of each fill comes out of the planner's own next-day wheat/strawberry/melon plantings, so our
sale revenue falls, and (b) V56 profits from our shifted mix. The early window (3,13) gifts the most. This is the CARROTBID /
ROUTEFILL1 tile-reallocation shape again. Planting COUNT is land-bound (1-2 free tiles/day), and more tomato on the same
land re-mixes our output into V56's hands. TOMATO fill CLOSED. ROUTE_FILL_MODE stays "ii".
Side result, worth merging: the VERIFY fill fix. Without it every ROUTE_FILL_* experiment after SALEPIN1 is silently fill-free.

## 5. Reproduce
`bash S/tomatofill1/grid.sh` (8 cells x 2 halves, 4 lanes), `ctl.sh` (base census + CAP 0), `legs.sh`, `tapes_after.sh`;
`python3 S/tomatofill1/table.py`; `python3 S/tomatofill1/pair.py <lab> base/FB.tsv -- out/fresh_<cell>_*.tsv`.
Tape switch string (on2b cannot parse tuples; DAYS/CAP left at defaults): `ROUTE_FILL_MODE=ii_fill,ROUTE_FILL_CROP=TOMATO`.
