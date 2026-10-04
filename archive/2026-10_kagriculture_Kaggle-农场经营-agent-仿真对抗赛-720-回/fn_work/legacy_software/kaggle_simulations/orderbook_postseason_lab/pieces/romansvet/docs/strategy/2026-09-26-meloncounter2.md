# MELONCOUNTER2 (2026-09-26 08:41Z–12:30Z): counter crop on the rival's melon tile count, N tiles only

**Verdict.** No counter crop beats the melon.
- 9 cells (5 crops × far/next tiles) were run on the 26 firing loss-tape seats. Every flip is on one of the 3 known noise boards: lamdang −1.9k, sidazuo −4.2k, and mhw_113480538, a re-derive swing where theirs moves −23..−30k.
- Their d10-19 melon cell does not move in any cell (Δtheirs MELON ≈ 0). The counter only adds our own volume on N tiles.
- The best cell is **Tf** (tomato on the N farthest free tiles). On both seats it nets +4 (lamdang ×2, mhw ×2), with Δours **+1,765 (t 4.32)** and Δtheirs +66 (t 0.08), so it is gift-free on tapes. Δours is positive in all 4 draw classes, so the class lookup collapses to TOMATO everywhere.
- On the 6 reacting non-V bank openers it gifts: Δtheirs **+1,635 (t 7.35)** against Δours +620 (t 2.36), 0 flips (base 72-0).
- It passed the dispatch's package gate (tape net ≥ +3; V56 dev 0-99 fires 0/200; held 150-249 0/200; FRESH300 0/300), so **res940_vrp8 is PACKAGED** (md5 a6a4ca74).
- **I do not recommend uploading it.** Its flips are noise boards, and it gifts on the reacting bed.

Branch `meloncounter1` (worktree `/mnt/e/_work/kagg3_wt_meloncounter1`, from selfplay1 9deb54a7) and `ship_vrp8` 50106310 (from ship_vrp7).
- Everything ran LOCALLY: 8 workers until 10:35Z, then ≤3 after the coordinator's load cut.
- Config: SAFETY_S 1e9 + REPAIR_MS 1e7 in both arms, actTimeout 600, head_940, theta7659.
- The vrp7 config in-process (LE.SWITCHES + EMPTY_ROUTE_UNHIRE_ON + the M20z gate) reproduces the vrp7 package exactly: tomatos 95,199 / 93,343 (the SHIPNV1 package game), lucas +2.9k.

## Grid: class × counter × tile choice, 26 firing tape seats (orig seat, paired vs vrp7; `S/meloncounter2/out/grid_tapes_orig.md`)
Class = the **first shop draw**. Nothing is drawn on d0-2: the first unlock is d3 on all 30 tapes and all 50 dev boards, and it is visible at the d3 dawn, before the first counter planting, since no tile is free d1-2. The groups are by the crops each shop demands:
- **S** (strawberry): SMOOTHIE, ICE_CREAM, BRUNCH. 11 seats.
- **T** (tomato): PIZZA, FARMERS. 5 seats.
- **W**: BAKERY. 3 seats.
- **A** (animal/carrot): PET_CAFE, YARN. 7 seats.

Winner per class = net ≥ +2 with Δours > 0.

| cell | all: W-L (base 2-24) | net | Δours (t) | Δtheirs (t) | S net / Δours | T net / Δours | W net / Δours | A net / Δours | d10-19 cells moved (Δours / Δtheirs value per game) |
|---|---|---|---|---|---|---|---|---|---|
| Wf wheat far | 2-24 | +1 | +69 (0.09) | −440 (−0.68) | +1 / −262 | 0 / −2,359 | 0 / +1,565 | 0 / +1,682 | WHEAT +1,358/−421, MILK −77/−1,144 |
| Wn wheat next | 3-23 | +2 | −1,042 (−0.87) | +1,562 (1.44) | +2 / −388 | 0 / −5,649 | 0 / +1,421 | 0 / +164 | WHEAT +1,360/−814, STRAWBERRY −872/+675 |
| **Tf tomato far** | 3-23 | **+2** | **+1,957 (3.26)** | −121 (−0.11) | **+2 / +1,231** | 0 / +2,495 | 0 / +1,018 | 0 / +3,115 | TOMATO +702/−3, FERTILIZER −231/+112 |
| Tn tomato next | 1-25 | 0 | +375 (0.41) | **+6,645 (6.48)** | 0 / +754 | 0 / −128 | 0 / +531 | 0 / +72 | MILK −1,011/+5,150, TOMATO +3,747/−163 |
| Sf strawberry far | 1-25 | 0 | −958 (−1.73) | −430 (−1.10) | 0 / −713 | 0 / −3,373 | 0 / −860 | 0 / +339 | WOOL +200/+43 |
| Sn strawberry next | 1-25 | 0 | −4,674 (−4.81) | +3,029 (2.01) | 0 / −4,259 | 0 / −5,035 | 0 / −6,815 | 0 / −4,151 | MELON −1,883/+26, STRAWBERRY −866/+762 |
| **Cf carrot far** | 4-22 | **+3** | +373 (0.57) | −1,313 (−1.08) | **+3 / +844** | 0 / −905 | 0 / −261 | 0 / +820 | CARROT +1,387/−186, STRAWBERRY −437/+93 |
| Cn carrot next | 2-24 | +1 | −3,325 (−3.56) | +2,378 (1.22) | +1 / −3,852 | 0 / −2,939 | 0 / −3,054 | 0 / −2,890 | MILK −702/−7,104, CARROT +2,285/−502 |
| Mf melon far | 0-26 | **−1** | −973 (−3.20) | +306 (0.88) | 0 / −824 | 0 / −1,029 | −1 / −1,400 | 0 / −983 | MELON +194/+6 |
| Mn melon next | not run (load cut) | | | | | | | | the NONV2 M20 d1-6 plate is this cell on melon rivals: Δtheirs +17k |
| herd (N tiles → pens) | not run | | | | | | | | NONV4 a2/a4/a6 = the same d2 gate + 2/4/6 sheep d2-5: +4 on noise boards / gift +6.2-6.4k |

- **Winners.**
  - Only class S has any: Cf (+3, Δours +844) and Tf (+2, +1,231).
  - A, T and W: no cell flips a single game.
- **Every flip is a noise board.**
  - Tf: lamdang −1,867 → +4,658, and mhw −13,794 → +16,250 (theirs −23.1k).
  - Cf: lamdang, sidazuo, and mhw (theirs −25.5k).
  - Wn: lamdang and sidazuo. Wf: lamdang.
  - Cn: mhw (theirs −30.1k). Mf: tomatos +1.9k → −0.3k.
  - lamdang flips under every perturbation (NONV1). mhw is NONV4's +54k re-derive board.
- **The next-tile cells gift** (Tn Δtheirs t 6.5, Sn 2.0, Cn 1.2, Wn 1.4). "next" takes the tiles the planner would have planted, and the planner's own strawberry and milk supply drops.
- **The far cells leave the plan almost untouched.** Tf's plantings d2-19 are tomato 3.6 → 10.8, wheat 49.9 → 46.3, and strawberry, melon and carrot within ±0.6.
- **Seat check.** Base orig and flip seats are identical on 16/30 boards and within ±2.9k on the rest. From 10:35Z the remaining cells ran on the orig seat only, and Tf was completed on both seats.

**Tf, both seats (52):** 6-46 from 2-50, net **+4**, 0 W→L, Δours +1,765 (t 4.32), Δtheirs +66 (t 0.08). By class:
- S: +4, +1,274 (t 1.97).
- T: 0, +2,695 (t 3.41), Δtheirs +3,334 (t 1.76).
- W: 0, +861, Δtheirs +1,958 (t 3.57).
- A: 0, +2,261 (t 2.49).

## Step 1: reacting stand-in (vrp7 package + forced d0 melon plate, own gate OFF, clock lifted) vs vrp7, dev 0-24 both seats
| dose | games | W-L (ours) | margin mean / median | rival d2 melon | d10-19 MELON net cell / game | LASP d10-19 vol / price per game |
|---|---|---|---|---|---|---|
| t6 | 12 (stopped) | 12-0 | +11.7k / +12.5k | 3.0 | −1.1k | +6.4k / +0.9k |
| **t10** | 50 | 47-3 | +14.9k / +13.5k | 10.0 | **−13.4k** | +3.3k / +1.2k |
| t14 | 13 (stopped) | 13-0 | +26.0k / +29.5k | 7.0 | −3.0k | +14.3k / +0.7k |
| live (LIVEWATCH16) | 22 | 2-20 | median −13.1k | 4-10 | −14.8k | – |

- t10 reproduces the melon cell (−13.4k vs −14.8k live), but not the margin: +13.5k against −13.1k, the opposite sign.
- No dose is within 2× of the live margin, so the grid ran on the tapes and t10 was kept as a loss-class check only.
- The stand-in is our own crew (about 3.5 hands) buying the plate out of its herd purse (MELONVRP1). The live class runs 6.7 hands and Q3 on d8-9.

## Validation of the lookup (= TOMATO far for every class)
| leg | result |
|---|---|
| tapes, 26 firing seats × 2 | net **+4** (lamdang, mhw × 2 seats), 0 W→L, Δours +1,765 (t 4.32), Δtheirs +66 (t 0.08) |
| 6 reacting non-V bank agents, dev 0-5 × 2 seats | 72-0 → 72-0, net **0**, Δours +620 (t 2.36), **Δtheirs +1,635 (t 7.35)**, so our margin shrinks −1.0k per game (min margin +7.4k). d10-19: our TOMATO +1,469, STRAWBERRY −518, MELON −534. **Gift.** |
| V56 dev 0-99 × 2 seats (cut at d2) | rival d2 melon 12 on 200/200, **fires 0/200** |
| V56 held 150-249 × 2 seats / FRESH300 seat 0 | rival d2 melon 12 on 200/200 and 300/300; **fires 0/200 and 0/300** |
| stand-in t10 dev 0-24 | not run (load cut). Base is 47-3 there |
| package game (vrp8 main.py, lifted clock, lamdang orig) | 109,529 / 104,871 = the harness Tf row exactly |
| package game (live clock, same board) | at load ~30: 109,348 / 104,868, worst turn 1.30 s. Re-run at load ~15: **109,529 / 104,871** (= harness), 0 bad statuses, 719 turns, mean dawn 0.324 s, **worst turn 0.508 s** (vrp7 in SHIPNV1: 0.705 s) |

## Package (upload is the user's; not recommended)
- **`dist/submission_res940_vrp8.tar.gz`**: md5 **`a6a4ca744f4c87c9efa0cecb8a1b309a`**, 515,025 bytes.
- The branch is `ship_vrp8` 50106310, which is ship_vrp7 plus the ported hunks.
- The only files that differ from the extracted vrp7 are `kagg3/core/plan.py` and `kagg3/agent/runtime.py`.
- New defaults: `MELON_COUNTER_ON=True`, `MC_CROP="TOMATO"`, `MC_TILES="far"`.
- Built locally with umask 022 and the SHIPUA1 command (absolute theta7659 and head_940). head_940 and theta7659 are untouched.
- `tests/test_ship_vrp8.py` passes (3).

## Build (`src/kagg3/core/plan.py` + `src/kagg3/agent/runtime.py`, OFF byte-identical)
- **Latch.** At the MC_DAY=2 dawn, `plan.mc_fires` reads the rival's MELON tiles. It fires with N = that count when 1 ≤ N ≤ 10 and the rival has at least 1 planting (V opens 11-12 and never fires).
  - The crop comes from `MC_CROP`, or from `MC_LOOKUP` keyed by the first shop draw ("SHOP:CROP;…", with "*" and "NONE").
- **Tiles.** Reserved tiles are removed from the planner's `free_slot` for good and replanted with the counter crop.
  - "far": new tiles, up to N, come from the free tiles the planner's own placement leaves, farthest from the shed first. The plan is untouched.
  - "next": the nearest free tiles are taken before the planner, as many as the counter's seed can cover.
  - The reservation lapses once the crop can no longer mature.
- **Funding and labour.** Seed is walked from what the grant left, as in WHEATMIX1. The planting is valued at full units × quote in the mandatory tier. Hands are sized from the counter tiles' own tasks (12 ops per hand, at most 2).
- **OFF identity.** Base after the patch equals the pre-patch smoke (stand10@0: 92,700 / 85,101 and 92,007 / 84,786). The runtime and plan branches are Python-false when OFF.
- `tests/test_meloncounter.py`: 3 passed.

Files are in `S/meloncounter2/`:
- `mcleg.py`: judge with beds stand<k>, tapes, react, v56.
- `run.sh`, `queue.sh`, `grid_tapes.txt`.
- `table.py`: step1 and grid tables, with the Laspeyres split.
- `firecensus.py`: d2-cut fire census.
- `mk_standin.sh`: the stand-ins; the builds themselves are not committed.
- `tilediff.py`, `drive.py`.
- `out/`: every csv and the grid md tables.
