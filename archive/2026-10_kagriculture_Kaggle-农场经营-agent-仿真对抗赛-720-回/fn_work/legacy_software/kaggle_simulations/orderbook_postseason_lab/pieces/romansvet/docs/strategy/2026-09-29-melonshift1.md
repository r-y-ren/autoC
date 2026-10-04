# MELONSHIFT1: PFS's own melons moved to d0-1 = the B8 plate again (herd -60-75 %, rival +13-19k); moved to d3-4 (P8d3) own +3.2k but the rival +4.6k; NONE (2026-09-29, 05:41Z-07:41Z)

Stream dir `S/melonshift1/`. Worktree `/mnt/e/_work/kagg3_wt_melonshift1` (sparse), branch `melonshift1` **0f27770a** on master 8d670dad (the live vrp20 code).
Judge: closed loop in the bit-exact fast env on the remote CPU (REACTCLONE1 / JUDGERIVAL1-3 harness), paired on the same (board, seat) games against a control
run in the same harness. No package was built: no cell reached any bar.

## Verdict: NONE
- **The shift as dispatched (d0-1 plate + no melon on d2..STOP) is B8/B6 again. It fails on every read.** 6 grid cells plus 2 constant-volume extras (STOP 29).
  - On g0capsfix: dmargin -13.6k to -17.1k (t -5.9 to -8.7), W 18 -> 15-17.
  - The rival gains +12.8k to +19.4k on g0capsfix, flood and live27, +6.6k to +12.9k on big, and +10.2k to +15.5k on the faithful live tapes.
  - Own coins: flat for 6 and 8 tiles (-1.8k to +3.0k); for 12 tiles, -8.2k to -9.7k on flood.
  - The herd at d9 falls 60-75 %: cows 2.8-4.0, sheep 0.0-0.3, geese 0-0.5, against 6.1 / 3.4 / 1.7.
  - **Mechanism:** the d0-1 plate changes PFS's d0 composition. It buys 2-3 cows instead of 4 cows + sheep + goose, and it orders BUY_LAND at d0 h3 in 20/20 games
    (the control buys its first quadrant on d5).
  - **The cut is a no-op through d9.** S8_9 = D10WAVE1's B8 on 20/20 closed-loop games and on 18/18 tapes: the plate already displaces PFS's d5-9 melons.
    After STOP the plan plants melon again, into a drained curve at 51-104 a unit.
- **"As early as cash allows" is a different body.** P8d3 is an 8-tile plate on d3-4, after the d0 herd purchase, using existing switches.
  - The d0 composition and the d5 quadrant are untouched. The d3-4 strawberry/wheat seeds become 9-10 melon seeds.
  - About 31 of the melons sell in d10-14 at 230.
  - Own coins rise: +3,154 (t 4.4) on 80 m40 games vs g0capsfix, +4,962 on big (t 3.8); +6 on live27; -1,500 on flood.
  - The rival also gains: +4.6k on m40, +5.3k on live27, +2.7k on flood, -2.0k on big.
  - dmargin by read: m40 -1,411 (t -1.36) with W 75 -> 80 (+5/-0 flips); live27 -5,340 (t -2.65), W 27 -> 26; flood -4,206 (t -1.7); big +6,987 (t 3.0).
  - Faithful tapes: own +729, rival +2,326, W 4 -> 2.
  - It fails CANDIDATE and PROMISING (live27 margin negative) and LIVE-TRIAL WORTHY:
    - herd at d9 5.2/2.6/1.2 < 6.1/3.4/1.7;
    - d10-14 melons +31 < +40;
    - flood own -1.5k < -1k.
- **Answer to the question:** no. The same melons planted d0-1 do not hold the herd (-60 to -75 % animals at d9), and the rival gains +13-19k. Planted d3-4 they hold most of
  the herd (-20 %) and raise own coins (+3.2k m40, +5.0k big), but they still pay the rival (+4.6k m40, +5.3k live27) and move only ~31 melons into d10-14.
  **CANDIDATE: none. PROMISING: none. LIVE-TRIAL WORTHY: none.** No package was built. The closest cell is P8d3.

## 1. PFS's melon timing and d0-1 affordability (`res/timing.md`)
Closed loop (control, 20 games vs g0capsfix) and live (the 9 unfired live27 seats, market rows = live):
- **d0 h1 buys the herd:** wheat 11 + carrot 8 + 4 cows + 1 sheep + 1 goose = 2,670 of the 3,000 start coins (closed loop and live identical). Dawn cash is 213 at d1
  and 127 at d2. No purchase at all on d1-2.
- **PFS's melons are a d5-19 drip:** 0 seeds in d0-4, 4.3-4.6 in d5-9, 5.4 in d10-12 (live 9.8 in d10-14), 1.7 after d15; 16 seeds live (x6 = 96 units = the 92 melons).
  Melon tiles standing at h12: 0 through d4, 3.4 at d9, 7.5 at d12, 12.8 at d15-17.
- **Affordability:** a d0-1 plate is paid only by displacing that herd (melon seed 80; 8 tiles = 640 coins = 1.6 cows). The shift saves nothing on d0-1: the melons it
  replaces would be bought from d5 on.

## 2. The shift: `MELON_SHIFT="N|STOP"` (new switch; no existing switch set can express it)
The existing plate switches (`MELON_PLATE_*`, `NONV_PLATE_LAST`, `MELON_DENY_PLATE`) only add melon on d0-2. `MELON_VETO_FLOOD_*` removes melon from a day onward
with no end day, and it runs before the learned residual (the head's +-4 `d_plant` can add melon back). So a new default-off switch was built (worktree commit 0f27770a):
- **d0-1 plate:** `_melon_plate`'s rebalance with N tiles on days 0 and 1. MELON is raised to min(N, plant_total). The tiles come off the other crops, wheat last.
  sum(plant_target) is preserved. With N=8 this is exactly D10WAVE1's B8 plate.
- **Cut:** MELON is taken out of the day's plant_target on days 2..STOP. The cut runs AFTER the residual, so it is the last word on melon. Freed tiles are not
  reassigned. Animals, fertiliser and every other crop stay the plan's.
- **OFF is bit-identical:** the worktree src with no MELON_SHIFT equals master `d10_ctl.csv` on 20/20 games (10 boards x 2 seats; every money column including the
  d10/d15/d18 checkpoints). The flood control equals JUDGERIVAL2's `jr2_pfs_fl.csv` on 20/20.

**The cut through d9 is a no-op after a plate.** S8_9 equals D10WAVE1's B8 on 20/20 closed-loop games vs g0capsfix. It equals MELONTRIAL1's B8 package on 18/18
fired live tapes. It equals mt_B8_fl on 18/20 flood games (S6_9 = mt_B6_fl on 14/20). Once 9-13 melon tiles stand from d0-1, the plan buys no melon on d2-9 anyway.
The plate already displaces PFS's d5-9 melons, so "plate + cut through d9" is the plate MELONTRIAL1 already measured. After STOP the plan plants melon again. Tiles
standing at h12 rise from 0-5 at d13 to 10-14 at d17-20. Those late melons sell into the curve the plate drained: 60-84 units at 51-96, against the control's
90-92 at 179-192.

**Where the herd goes (every plated game, both rivals):**
- The plated d0 h1 buys 3 cows (S6, S8) or 2 cows (S12), instead of 4 cows + 1 sheep + 1 goose. S8 keeps 1 goose.
- The plan orders BUY_LAND at d0 h3 in 20/20 plated games. The control buys its first quadrant on d5 in 20/20.
- Herd at d9 (cows/sheep/geese): 2.8-4.0 / 0.2-0.3 / 0-0.5, against the control's 6.1 / 3.4 / 1.7.
- Our egg/milk/wool units in d10-29 fall 10-25 %, and the rival sells into that lane.
- The herd budget is not simply spent on the melon seeds. The plate moves the plan's whole d0 composition: the quadrant comes 5 days early and the animals are cut.
  Dawn cash at d1 is 976-996 for S6/S8 against the control's 213.

## 3. The grid (named before running, `checkpoint.txt` 05:48Z)
Cells: `MELON_SHIFT=N|STOP` with N in {6, 8, 12} and STOP in {9, 14} = 6 cells. Named extras, each added to `checkpoint.txt` before it ran:
- 06:03Z: STOP = 29 = no melon after the plate, the true constant-volume shift, for N = 8 and 12.
- 06:26Z: **P8d3 / P12d3 = "as early as cash allows"**. The plate goes on d3-4, after PFS's d0 herd purchase, with existing switches only:
  `MELON_PLATE_TILES=8|12,MELON_PLATE_DAY=3,NONV_PLATE_LAST=4`, no cut. P8d3 was then followed up on all 40 boards, live27, flood, big and the tapes. Our seat = worktree src + the PFS OFF string + the cell. Rival named per row. flips = W changes vs the control;
t = paired t vs the control; windows d0-9 / d10-14 / d15-29 are exact cash changes (rcw.py dawn-d15 checkpoint); melon u@price from the sales ledger.
**Scale:** boards_m40 first 10 boards x 2 seats = 20 games per cell and rival, not 80. At 17 s/game on 2 workers the 120-min box held about 30 runs of 20 games.
Every cell's dmargin is at t -4 to -8 on 20 games, so a larger n would not change any verdict.

### vs g0capsfix (the margin/flips bar)
rival g0capsfix; control ms_ctl_gcf; melon tiles at h12 on d0 1 2 3 5 7 9 11 13 15 17 20
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 | our COW/SHEEP/GOOSE d9 | our egg/milk/wool units d10-29 | dawn cash d1/d2 | our melon tiles h12 (n state) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix | ms_ctl_gcf | 20 | 18->18 | +0/-0 | 109,563 | 84,533 | +25,030 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +2,715 / +2,791 / +101,057 | -1,946 / +23,852 / +59,627 | 0.0u@0 / 91.7u@179 | 46.3u@251 / 10.2u@231 | 6.1/3.4/1.7 | 102/156/125 | 213/127 | 0.0 0.0 0.0 0.0 0.2 2.1 3.4 5.7 10.2 12.8 12.8 10.6 (20) |
| g0capsfix | ms_S6_9_gcf | 20 | 18->16 | +0/-2 | 109,858 | 98,382 | +11,476 | +295 (+0.23) | +13,850 (+10.13) | -13,554 (-7.01) | -3,322 / +5,648 / -2,031 | +358 / +813 / +12,679 | 54.0u@222 / 83.9u@91 | 41.6u@245 / 12.8u@177 | 4.0/0.3/0.0 | 76/142/123 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 4.8 4.8 10.4 13.7 14.2 (20) |
| g0capsfix | ms_S6_14_gcf | 20 | 18->16 | +0/-2 | 109,313 | 99,123 | +10,190 | -250 (-0.17) | +14,590 (+11.67) | -14,840 (-7.80) | -3,322 / +6,084 / -3,012 | +358 / +686 / +13,546 | 54.0u@222 / 83.7u@96 | 41.6u@245 / 12.7u@176 | 4.0/0.3/0.0 | 94/143/125 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 4.8 0.0 1.4 11.9 14.1 (20) |
| g0capsfix | ms_S8_9_gcf | 20 | 18->15 | +0/-3 | 112,571 | 103,971 | +8,600 | +3,008 (+2.01) | +19,439 (+12.72) | -16,431 (-7.28) | -3,181 / +7,860 / -1,672 | -287 / +968 / +18,758 | 78.0u@204 / 68.3u@51 | 45.4u@234 / 12.9u@116 | 3.1/0.3/0.5 | 81/138/106 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 2.8 5.8 10.4 11.8 (20) |
| g0capsfix | ms_S8_14_gcf | 20 | 18->15 | +0/-3 | 112,043 | 103,955 | +8,088 | +2,480 (+1.79) | +19,422 (+13.71) | -16,942 (-8.34) | -3,181 / +7,936 / -2,276 | -287 / +680 / +19,029 | 78.0u@204 / 64.6u@57 | 45.4u@234 / 12.7u@117 | 3.1/0.3/0.5 | 96/137/112 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 0.0 0.2 9.1 11.4 (20) |
| g0capsfix | ms_S12_9_gcf | 20 | 18->16 | +0/-2 | 110,868 | 102,794 | +8,074 | +1,305 (+0.80) | +18,261 (+9.97) | -16,956 (-6.40) | -2,892 / +6,815 / -2,618 | +121 / -572 / +18,713 | 72.0u@221 / 73.3u@77 | 36.2u@232 / 12.8u@153 | 2.8/0.2/0.0 | 57/122/129 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.3 1.1 5.6 10.3 12.7 (20) |
| g0capsfix | ms_S12_14_gcf | 20 | 18->16 | +0/-2 | 111,299 | 101,334 | +9,965 | +1,736 (+1.13) | +16,801 (+9.70) | -15,065 (-5.87) | -2,892 / +7,340 / -2,712 | +121 / -539 / +17,220 | 72.0u@221 / 73.0u@79 | 36.2u@232 / 12.8u@155 | 2.8/0.2/0.0 | 62/125/132 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.8 9.1 12.6 (20) |
| g0capsfix | ms_S8_29_gcf | 20 | 18->17 | +0/-1 | 111,641 | 103,704 | +7,937 | +2,078 (+1.61) | +19,171 (+14.51) | -17,094 (-8.71) | -3,181 / +7,936 / -2,678 | -287 / +680 / +18,778 | 78.0u@204 / 0.0u@0 | 45.4u@234 / 12.9u@117 | 3.1/0.3/0.5 | 103/138/120 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 0.0 0.0 0.0 0.0 (20) |
| g0capsfix | ms_S12_29_gcf | 20 | 18->16 | +0/-2 | 108,764 | 100,112 | +8,652 | -800 (-0.56) | +15,579 (+10.14) | -16,379 (-7.76) | -2,892 / +7,340 / -5,247 | +121 / -539 / +15,998 | 72.0u@221 / 0.0u@0 | 36.2u@232 / 12.9u@155 | 2.8/0.2/0.0 | 70/126/135 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.0 0.0 0.0 (20) |
| g0capsfix | ms_P8d3_gcf | 20 | 18->20 | +2/-0 | 115,326 | 88,324 | +27,002 | +5,763 (+6.28) | +3,791 (+2.35) | +1,971 (+0.96) | +422 / +4,504 / +837 | -28 / +302 / +3,518 | 31.1u@230 / 92.5u@122 | 44.8u@251 / 14.7u@167 | 5.4/2.7/1.1 | 93/145/120 | 213/127 | 0.0 0.0 0.0 1.0 9.0 9.1 10.0 10.3 11.2 8.2 11.6 10.7 (20) |
| g0capsfix | ms_P12d3_gcf | 20 | 18->20 | +2/-0 | 115,508 | 88,572 | +26,936 | +5,945 (+4.24) | +4,039 (+2.73) | +1,906 (+1.12) | +508 / +4,118 / +1,318 | -39 / -217 / +4,295 | 32.5u@230 / 96.9u@118 | 44.7u@250 / 12.6u@161 | 4.9/1.9/1.0 | 96/138/124 | 213/127 | 0.0 0.0 0.0 1.0 10.0 10.3 10.6 10.8 11.1 6.9 11.2 11.2 (20) |

### vs g0capsfix, P8d3 on all 40 boards x 2 seats (80 games; control = D10WAVE1's `d10_ctl.csv`, same harness, state columns cover the first 20 games only)
rival g0capsfix (m40, 80 games); control d10_ctl; melon tiles at h12 on d0 1 2 3 5 7 9 11 13 15 17 20
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 | our COW/SHEEP/GOOSE d9 | our egg/milk/wool units d10-29 | dawn cash d1/d2 | our melon tiles h12 (n state) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix (m40, 80 games) | d10_ctl | 80 | 75->75 | +0/-0 | 115,169 | 90,217 | +24,952 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +2,670 / +2,227 / +107,271 | -2,094 / +23,386 / +65,926 | 0.0u@0 / 92.0u@176 | 45.7u@251 / 12.8u@227 | n/a | 113/155/148 | n/a | n/a (0) |
| g0capsfix (m40, 80 games) | ms_P8d3_gcf80 | 80 | 75->80 | +5/-0 | 118,323 | 94,782 | +23,540 | +3,154 (+4.42) | +4,565 (+5.69) | -1,411 (-1.36) | +425 / +4,430 / -1,701 | -92 / +510 / +4,147 | 31.1u@230 / 94.9u@119 | 45.2u@251 / 13.9u@164 | 5.2/2.6/1.2 | 92/143/149 | 213/127 | 0.0 0.0 0.0 1.0 9.0 9.2 10.2 10.5 11.2 7.5 11.7 11.0 (80) |

### vs flood (the dours read)
rival flood; control ms_ctl_fl; melon tiles at h12 on d0 1 2 3 5 7 9 11 13 15 17 20
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 | our COW/SHEEP/GOOSE d9 | our egg/milk/wool units d10-29 | dawn cash d1/d2 | our melon tiles h12 (n state) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flood | ms_ctl_fl | 20 | 20->20 | +0/-0 | 119,429 | 75,093 | +44,336 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +3,333 / +2,090 / +111,006 | -2,286 / +17,273 / +57,106 | 0.0u@0 / 90.0u@192 | 43.2u@252 / 6.5u@233 | 6.0/3.1/1.3 | 88/163/152 | 213/127 | 0.0 0.0 0.0 0.0 0.0 2.5 4.2 7.5 11.3 13.6 12.3 9.1 (20) |
| flood | ms_S6_9_fl | 20 | 20->20 | +0/-0 | 118,524 | 89,059 | +29,465 | -906 (-0.36) | +13,966 (+6.97) | -14,871 (-4.07) | -3,815 / +8,482 / -5,573 | -151 / +5 / +14,112 | 54.0u@237 / 75.0u@96 | 45.3u@223 / 11.0u@172 | 3.6/0.2/0.0 | 71/157/121 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 4.8 4.0 8.9 12.3 12.7 (20) |
| flood | ms_S6_14_fl | 20 | 20->20 | +0/-0 | 118,617 | 88,495 | +30,121 | -813 (-0.31) | +13,402 (+6.91) | -14,215 (-3.85) | -3,815 / +8,879 / -5,877 | -151 / +3 / +13,550 | 54.0u@237 / 72.5u@104 | 44.5u@224 / 12.2u@172 | 3.6/0.2/0.0 | 92/160/124 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 4.7 0.0 1.1 10.2 12.2 (20) |
| flood | ms_S8_9_fl | 20 | 20->20 | +0/-0 | 120,063 | 92,654 | +27,410 | +634 (+0.24) | +17,560 (+11.31) | -16,926 (-5.14) | -4,130 / +12,454 / -7,689 | -210 / -215 / +17,985 | 78.0u@222 / 60.0u@76 | 43.6u@207 / 6.2u@120 | 3.2/0.2/0.2 | 78/153/117 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 2.9 5.3 8.8 10.2 (20) |
| flood | ms_S8_14_fl | 20 | 20->20 | +0/-0 | 120,442 | 93,542 | +26,900 | +1,013 (+0.35) | +18,449 (+11.97) | -17,436 (-4.65) | -4,130 / +12,857 / -7,714 | -210 / -106 / +18,765 | 78.0u@222 / 60.2u@80 | 43.6u@207 / 6.2u@120 | 3.2/0.2/0.2 | 76/157/115 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 0.0 0.3 6.8 10.2 (20) |
| flood | ms_S12_9_fl | 20 | 20->20 | +0/-0 | 111,138 | 91,660 | +19,479 | -8,291 (-4.93) | +16,567 (+12.23) | -24,858 (-10.26) | -3,388 / +8,756 / -13,659 | +53 / +802 / +15,712 | 72.0u@236 / 66.2u@78 | 45.0u@194 / 6.7u@138 | 2.9/0.0/0.0 | 69/131/126 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.1 2.2 5.2 9.9 11.2 (20) |
| flood | ms_S12_14_fl | 20 | 20->20 | +0/-0 | 111,267 | 90,825 | +20,442 | -8,162 (-3.73) | +15,732 (+10.87) | -23,894 (-7.86) | -3,388 / +9,386 / -14,160 | +53 / +138 / +15,541 | 72.0u@236 / 63.8u@82 | 45.0u@194 / 7.4u@137 | 2.9/0.0/0.0 | 76/137/123 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.3 8.0 10.9 (20) |
| flood | ms_S8_29_fl | 20 | 20->19 | +0/-1 | 118,577 | 92,623 | +25,954 | -852 (-0.30) | +17,530 (+9.06) | -18,382 (-4.33) | -4,130 / +12,857 / -9,579 | -210 / -106 / +17,846 | 78.0u@222 / 0.0u@0 | 43.6u@207 / 6.2u@121 | 3.2/0.2/0.2 | 80/158/119 | 976/258 | 2.0 7.0 13.0 13.0 13.0 13.0 13.0 6.5 0.0 0.0 0.0 0.0 (20) |
| flood | ms_S12_29_fl | 20 | 20->18 | +0/-2 | 109,720 | 90,683 | +19,037 | -9,709 (-4.67) | +15,590 (+9.70) | -25,299 (-8.28) | -3,388 / +9,386 / -15,707 | +53 / +138 / +15,398 | 72.0u@236 / 0.0u@0 | 45.0u@194 / 7.3u@136 | 2.9/0.0/0.0 | 78/137/127 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.0 0.0 0.0 (20) |
| flood | ms_P8d3_fl | 20 | 20->20 | +0/-0 | 117,930 | 77,799 | +40,130 | -1,500 (-0.73) | +2,706 (+2.32) | -4,206 (-1.69) | -98 / +4,532 / -5,933 | -22 / +677 / +2,051 | 30.0u@233 / 94.2u@137 | 44.2u@250 / 5.9u@172 | 5.3/2.7/0.9 | 80/154/137 | 213/127 | 0.0 0.0 0.0 1.0 8.9 9.1 10.1 11.4 12.6 8.5 11.3 10.2 (20) |
| flood | ms_P12d3_fl | 20 | 20->20 | +0/-0 | 115,908 | 78,712 | +37,196 | -3,521 (-1.80) | +3,619 (+3.14) | -7,140 (-2.53) | -189 / +4,851 / -8,183 | +100 / +176 / +3,343 | 30.8u@230 / 97.8u@127 | 44.4u@251 / 8.6u@161 | 5.4/2.0/1.0 | 72/151/131 | 213/127 | 0.0 0.0 0.0 1.0 10.0 10.3 11.3 12.2 12.9 7.9 11.2 10.0 (20) |

### vs big (control + the 2 best non-B8 grid cells + P8d3; S6_9 ~ B6 and S8_9 = B8 have MELONTRIAL1's 80-game big rows: B6 own +1,097, B8 own -675, rival +8.9k / +12.1k)
rival big; control ms_ctl_big; melon tiles at h12 on d0 1 2 3 5 7 9 11 13 15 17 20
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 | our COW/SHEEP/GOOSE d9 | our egg/milk/wool units d10-29 | dawn cash d1/d2 | our melon tiles h12 (n state) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| big | ms_ctl_big | 20 | 20->20 | +0/-0 | 112,161 | 71,566 | +40,596 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +3,245 / +1,652 / +104,265 | -2,238 / +15,047 / +55,757 | 0.0u@0 / 83.8u@180 | 48.9u@250 / 11.9u@230 | 6.0/3.1/1.5 | 117/171/133 | 213/127 | 0.0 0.0 0.0 0.0 0.0 2.5 4.7 7.3 10.1 12.4 11.2 8.2 (20) |
| big | ms_S6_14_big | 20 | 20->20 | +0/-0 | 114,634 | 78,131 | +36,503 | +2,472 (+0.94) | +6,565 (+4.34) | -4,093 (-1.25) | -3,789 / +7,107 / -846 | -188 / +2,551 / +4,203 | 54.0u@228 / 71.2u@100 | 56.0u@221 / 1.9u@159 | 3.5/0.1/0.0 | 111/155/137 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 5.3 0.0 1.1 10.6 12.0 (20) |
| big | ms_S12_14_big | 20 | 20->18 | +0/-2 | 108,460 | 84,503 | +23,957 | -3,701 (-1.98) | +12,937 (+4.85) | -16,639 (-4.03) | -3,426 / +8,341 / -8,616 | -294 / +1,118 / +12,112 | 72.0u@225 / 66.3u@82 | 46.9u@208 / 4.8u@134 | 2.9/0.1/0.0 | 74/132/131 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.5 8.2 11.5 (20) |
| big | ms_P8d3_big | 20 | 20->20 | +0/-0 | 117,123 | 69,541 | +47,583 | +4,962 (+3.75) | -2,025 (-1.15) | +6,987 (+2.99) | -144 / +4,974 / +131 | +127 / +94 / -2,246 | 30.8u@228 / 91.5u@131 | 47.4u@250 / 6.0u@168 | 5.4/2.6/1.0 | 92/158/140 | 213/127 | 0.0 0.0 0.0 1.0 9.0 9.3 10.5 11.2 11.8 7.4 11.1 9.5 (20) |

### live27 seats vs g0capsfix (control + the 2 best non-B8 grid cells + P8d3; B6 / B8 = MELONTRIAL1 rows: own -1,938 / +178, rival +13.8k / +17.7k, W 27->21 / 27->22)
rival g0capsfix (live27); control ms_ctl_l27; melon tiles at h12 on d0 1 2 3 5 7 9 11 13 15 17 20
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 | our COW/SHEEP/GOOSE d9 | our egg/milk/wool units d10-29 | dawn cash d1/d2 | our melon tiles h12 (n state) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix (live27) | ms_ctl_l27 | 27 | 27->27 | +0/-0 | 112,235 | 84,293 | +27,942 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +2,987 / +2,553 / +103,695 | -2,374 / +23,729 / +59,938 | 0.0u@0 / 94.6u@176 | 45.8u@251 / 12.9u@228 | 6.4/3.3/1.6 | 120/160/145 | 213/127 | 0.0 0.0 0.0 0.0 0.2 1.9 3.5 5.3 9.4 12.8 13.4 11.4 (27) |
| g0capsfix (live27) | ms_S6_14_l27 | 27 | 27->20 | +0/-7 | 110,393 | 97,084 | +13,309 | -1,842 (-1.08) | +12,790 (+10.19) | -14,632 (-7.21) | -3,372 / +5,790 / -4,260 | +16 / +893 / +11,881 | 54.0u@224 / 89.4u@98 | 41.1u@244 / 9.6u@174 | 3.7/0.0/0.0 | 98/136/150 | 996/838 | 0.0 4.0 9.0 9.0 9.0 9.0 9.0 5.3 0.0 0.9 12.8 15.2 (27) |
| g0capsfix (live27) | ms_S12_14_l27 | 27 | 27->18 | +0/-9 | 111,364 | 100,037 | +11,327 | -870 (-0.38) | +15,744 (+7.83) | -16,614 (-5.67) | -3,121 / +6,808 / -4,558 | +84 / -606 / +16,265 | 72.0u@221 / 78.0u@80 | 35.8u@233 / 10.8u@152 | 2.8/0.1/0.0 | 67/117/165 | 26/110 | 4.0 12.0 12.0 12.0 12.0 12.0 12.0 0.0 0.0 0.6 9.7 13.5 (27) |
| g0capsfix (live27) | ms_P8d3_l27 | 27 | 27->26 | +0/-1 | 112,241 | 89,640 | +22,601 | +6 (+0.00) | +5,346 (+4.48) | -5,340 (-2.65) | +220 / +3,792 / -4,006 | +22 / -102 / +5,426 | 30.3u@229 / 99.3u@115 | 46.0u@251 / 13.8u@164 | 5.4/2.4/1.1 | 101/144/146 | 213/127 | 0.0 0.0 0.0 1.0 9.0 9.1 10.4 10.7 11.5 7.8 12.1 11.3 (27) |

### Faithful-seat tape check (MELONTRIAL1's method: the cell as the vrp21_melon package's fired switch-set, file agent on the 18 fired live27 tapes, vs live = PFS)
### l27_S8_9
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 3 | +2/-3 | +4,235 (+1.09) | +9,041 (+1.72) | -4,806 (-0.56) |
| fired | 18 | 4 -> 3 | +2/-3 | +4,235 (+1.09) | +9,041 (+1.72) | -4,806 (-0.56) |
| fired, JC1-faithful both | 15 | 3 -> 1 | +0/-2 | +192 (+0.07) | +15,398 (+8.32) | -15,206 (-4.96) |

### l27_S6_9
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 2 | +1/-3 | +2,700 (+0.84) | +7,033 (+1.80) | -4,333 (-0.65) |
| fired | 18 | 4 -> 2 | +1/-3 | +2,700 (+0.84) | +7,033 (+1.80) | -4,333 (-0.65) |
| fired, JC1-faithful both | 16 | 3 -> 1 | +0/-2 | +302 (+0.15) | +10,586 (+7.35) | -10,284 (-4.20) |

### l27_S6_14
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 2 | +1/-3 | +2,640 (+0.80) | +6,776 (+1.73) | -4,136 (-0.61) |
| fired | 18 | 4 -> 2 | +1/-3 | +2,640 (+0.80) | +6,776 (+1.73) | -4,136 (-0.61) |
| fired, JC1-faithful both | 16 | 3 -> 1 | +0/-2 | -84 (-0.04) | +10,205 (+6.77) | -10,289 (-4.04) |

### l27_S12_14
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 2 | +1/-3 | -588 (-0.20) | +12,259 (+3.58) | -12,846 (-2.41) |
| fired | 18 | 4 -> 2 | +1/-3 | -588 (-0.20) | +12,259 (+3.58) | -12,846 (-2.41) |
| fired, JC1-faithful both | 16 | 3 -> 1 | +0/-2 | -2,122 (-0.79) | +15,455 (+7.88) | -17,577 (-6.44) |

### l27_P8d3
| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 3 | +1/-2 | +2,178 (+1.13) | -272 (-0.10) | +2,451 (+0.57) |
| fired | 18 | 4 -> 3 | +1/-2 | +2,178 (+1.13) | -272 (-0.10) | +2,451 (+0.57) |
| fired, JC1-faithful both | 17 | 4 -> 2 | +0/-2 | +729 (+0.54) | +2,326 (+3.41) | -1,597 (-0.99) |

## 4. Bars
The bars are applied as dispatched: CANDIDATE = own >= control - 1k AND margin > control at t >= 2 on the 80-game g0capsfix read AND the live27 read.
PROMISING = t >= 1 on both. LIVE-TRIAL WORTHY = own >= control - 1k on flood AND big, herd at d9 >= control, d10-14 melons >= +40, faithful-tape rival <= +3k.

| cell | g0capsfix dmargin (t) | live27 dmargin (t) | own flood / big | herd d9 C/S/G vs ctl | melons d10-14 | tape rival (faithful) | verdict |
|---|---|---|---|---|---|---|---|
| S6_9 (~B6) | -13,554 (-7.01) | B6: -15,777 (-8.59) | -906 / B6 +1,097 | 4.0/0.3/0.0 vs 6.1/3.4/1.7 | +54 | +10,586 | NONE |
| S6_14 | -14,840 (-7.80) | -14,632 (-7.21) | -813 / +2,472 | 4.0/0.3/0.0 | +54 | +10,205 | NONE (closest d0-1 cell) |
| S8_9 (= B8) | -16,431 (-7.28) | B8: -17,525 (-10.20) | +634 / B8 -675 | 3.1/0.3/0.5 | +78 | +15,398 | NONE |
| S8_14 | -16,942 (-8.34) | - | +1,013 / - | 3.1/0.3/0.5 | +78 | - | NONE |
| S12_9 | -16,956 (-6.40) | - | -8,291 / - | 2.8/0.2/0.0 | +72 | - | NONE |
| S12_14 | -15,065 (-5.87) | -16,614 (-5.67) | -8,162 / -3,701 | 2.8/0.2/0.0 | +72 | +15,455 | NONE |
| S8_29 (extra) | -17,094 (-8.71) | - | -852 / - | 3.1/0.3/0.5 | +78 | - | NONE |
| S12_29 (extra) | -16,379 (-7.76) | - | -9,709 / - | 2.8/0.2/0.0 | +72 | - | NONE |
| **P8d3 (extra)** | -1,411 (-1.36) [80 g; W 75->80, +5/-0] | -5,340 (-2.65) | -1,500 / +4,962 | 5.4/2.7/1.1 vs 6.1/3.4/1.7 | +31 | +2,326 | NONE (closest: fails own flood by 0.5k, herd, melons +31) |
| P12d3 (extra) | +1,906 (+1.12) [20 g] | - | -3,521 / - | 4.9/1.9/1.0 | +33 | - | NONE |

## Files
- `S/melonshift1/res/timing.md` (step 1), `res/table_{gcf,fl,big,l27,tape}.md`, `res/rc/` (csv + sales ledger + state log per run).
- `ms_rc.py` is the state wrapper: dawn cash, melon tiles by day, herd at d9/d14, and market rows d0-12 per game.
- `rcrw2.py` is the current judgerival1/rcr.py plus the rcw.py d15 checkpoint, used for flood and big. The old d10wave1/rcrw.py predates the flood caretaker.
- `ms_chain2.sh` + `spec{A..E}.txt` are the remote chains; `ms_an.py` builds the tables; `mk_tables.sh` pulls results and writes the tables.
- `mkpkg.sh` / `tape.sh` / `tbl_l27.py` run the tape check. `melon_shift.patch` is the worktree plan.py diff.
