# CARROTFILL-MELON1 (2026-09-27 21:06Z-22:35Z): late carrot-only ii_fill on the 51 BAND MELON seats vs PFS -> NO SHIP

**Verdict: NO SHIP (fires, but moves nothing).** All 4 grid cells: −1 flip (+1/−2, the same three seats in every cell), paired Δours −71..−141 (t −0.55..−1.11), Δtheirs +72..+79 (t 1.16..1.26, sub-kill), family Δθ −6 (SE 10). The fill adds only ~1.05 carrot sowings per game (31.1 → 32.2 over d17-29). CAP 3 vs 8 makes no difference. Step 2 (BAND142) was not run because no cell reached +2 flips. The OPCENSUS-MELON1 reopen condition (carrot-only fill with paired Δours > 0) **fails**.

## Grid (all cells: `PLACEFEED_ON=True,PF_PUMPSAFE_ON=True,ROUTE_FILL_MODE=ii_fill,ROUTE_FILL_CROP=CARROT`, n = 51, done, none killed)

| cell | DAYS, CAP | W base→cell | flips +/− | Δours (t) | Δtheirs (t) | fam Δθ (SE) | carrot sow d17-29 base→cell | all sow d17-29 | empty/day d17-27 (dawn) | empty d27 dawn | fired (seats with more sowings) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c17_8 | (17,27), 8 | 14→13 | +1/−2 | −127 (−0.98) | +78 (+1.26) | −6 (10) | 31.14→32.25 | 103.8→105.0 | 1.87→1.55 | 6.86→6.33 | 33/51 |
| c20_8 | (20,27), 8 | 14→13 | +1/−2 | −71 (−0.55) | +72 (+1.16) | −6 (10) | 31.14→32.18 | 103.8→104.9 | 1.87→1.56 | 6.86→6.41 | 32/51 |
| c17_3 | (17,27), 3 | 14→13 | +1/−2 | −141 (−1.11) | +79 (+1.26) | −6 (9) | 31.14→32.24 | 103.8→104.9 | 1.87→1.56 | 6.86→6.33 | 33/51 |
| c20_3 | (20,27), 3 | 14→13 | +1/−2 | −86 (−0.67) | +72 (+1.16) | −6 (10) | 31.14→32.16 | 103.8→104.8 | 1.87→1.57 | 6.86→6.41 | 32/51 |

- Flips are identical in every cell: up = tape_hamedvakili_114125877; down = tape_leaveyou_114114006 and tape_smackaveli_113329149. 8/51 seats are score-identical to base.
- Sale volume barely moves: d10-19 units are unchanged (447), and all-game units go from 1,453 to 1,448-1,449.

## Why it moves nothing (mechanism, from `route_vrp.fill`)
- **Window:** the fill's last day is `min(DAYS[1], N_DAYS−2−LIFE[CARROT]=25)`, so (17,27) is really d17-25 and (20,27) is really d20-25. The empty tiles the census saw pile up on d25-28 (dawn empty: d25 ~4, d27 ~7-11, d28 ~14) and lie outside any carrot fill window.
- **Candidates:** fill candidates are only dawn `None`/WEED tiles that no planner stop uses. On d17-25, PFS has ~1.9 empty tiles at dawn (base mean 1.87). The planner replants same-day harvests itself, so the fill finds ~0.1 tiles/day. CAP (3 or 8) never binds.
- **So the census's "40 vs 25 carrots d20-29" gap cannot be reached by a spare-turn fill.** Closing it needs different land use on d20-25 (the top team's crop rotation), not idle-turn fills. This is the same "land full" finding as MELONVOL1 `wr`.

## Method
- Bed: 51 MELON seats of `S/bandleg1/boards_all.json`, orig seat, real engine. Harness = MELONVOL1 leg (bandleg1/ml1leg: SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, head_940, theta7659). Repo src == 942b46cb (0 diff). 2 workers, nice 10.
- Switches verified on 942b46cb: `ROUTE_FILL_MODE "ii"`, `ROUTE_FILL_CAP 3`, `ROUTE_FILL_CROP "WHEAT"`, `ROUTE_FILL_DAYS (10, 25)` (plan.py:7742-7745). CARROT is in `route_vrp.LIFE` (3). DAYS is passed as a tuple through `MV_TUPLES=ROUTE_FILL_DAYS=17:27`.
- Base = PFS `S/bandleg1/res/pfv1.csv` (W 14/51). Re-verified 2/2 seats score-exact (`res/ident.csv`). The new tile columns on those 2 seats equal the base-replay metric exactly.
- Kill rule: Δtheirs t >= 2 after n >= 27. It never fired.
- New columns (`tiles.py`):
  - `our_carrot_sow_d17_29` = distinct (tile, planted_day) CARROT plantings with planted_day 17-29;
  - `our_sow_d17_29` = the same count for all crops;
  - `our_empty_d17_27` = mean dawn `None`-tile count (census definition);
  - `our_empty_d27` = the dawn count on d27.
  Base values come from the MELONAUDIT1 replays (51/51 byte-exact to pfv1) → `res/base_tiles.csv`.
- Family Δθ = BANDLEG1 Part C method (pair.py, copied from MELONVOL1). Only MELON seats were run, so the other families have ΔWin 0. SE = 400× bootstrap.

## Re-run
```
bash S/carrotfillmelon1/run.sh ident c17_8 c20_8 c17_3 c20_3     # ~20 min/cell, 2 workers
cd S/carrotfillmelon1 && python tiles.py && python pair.py > res/pair.txt   # -> res/cells.tsv
FAMS=MELON,V,ZERO,OTHER bash S/carrotfillmelon1/run.sh <cell>     # BAND142 step 2 (not triggered)
```
Files: `S/carrotfillmelon1/{run.sh,leg.py,tiles.py,units.py,pair.py}`, `res/{ident,c17_8,c20_8,c17_3,c20_3}.csv`, `res/cells.tsv`, `res/pair.txt`, `res/base_tiles.csv`.
