# PLATENOLAND1: the d0-1 melon plate on the starting tiles with the d0 quadrant blocked keeps the cows but not the herd; the rival still gains +4-14k; NONE (2026-09-29, 07:21Z-09:21Z)

Stream dir `S/platenoland1/`. Worktree `/mnt/e/_work/kagg3_wt_platenoland1` (sparse), branch `platenoland1_0929` on master 8d670dad:
MELON_SHIFT (MELONSHIFT1 0f27770a -> 14d155ef) + LAND_DAY (LAND1 58422323 -> a5489c73) + the new gate `PLATE_NO_LAND_BEFORE` (**bf4191f2**).
Judge: closed loop in the bit-exact fast env on the remote CPU, paired on the same (board, seat) games with MELONSHIFT1's banked controls from the same harness.
No package was built: no cell reached any bar. No master, dist, trainer or GPU change; no upload.

## Verdict: NONE
- **Blocking the d0 quadrant works mechanically, and it does not save the herd.** With `PLATE_NO_LAND_BEFORE=5` + `LAND_DAY=5|99|0`,
  Q2 is bought on d5 in 20/20 games (the control's day; MELONSHIFT1's plate bought it at d0 h3 in 20/20). The h1 order keeps the 4 cows, but the plate
  now has only the 25 starting tiles and the 3,000 purse, and it takes what the herd needs anyway:
  - **N = 6:** h1 = wheat 11 + carrot 5 + **melon 3** + cow 4 + sheep 1 + goose 1. Dawn cash d1 **33** (control 213): the feed reserve is spent on
    melon seed. Of the 5.0 / 1.5 / 1.1 cows / sheep / geese bought d0-9, only **4.0 / 0.4 / 0.1** stand at d9: about one animal of each kind is
    lost (most likely starved: the purse cannot buy feed wheat on d1-2; the control loses none). Sheep and geese at d9 are no better than MELONSHIFT1's d0-quadrant plate (0.3 / 0.5).
  - **N = 8:** h1 = wheat 11 + carrot 3 + **melon 5** + cow 4 + goose 1, **no sheep**. Dawn cash d1 416. The herd at d9 is **5.2 / 0.8 / 0.9**
    (control 6.1 / 3.4 / 1.7): the sheep lane is gone: the herd bought d0-9 is 7.7 animals against the control's 11.3.
  - The plate is **tile- and cash-bound at 3-5 melons**: melon tile-days d0-9 are 27 (N6) and 45 (N8) against MELONSHIFT1's 113. Melons sold
    in d10-14: **18 @244 (N6) and 30 @240 (N8)**, both below the +40 bar.
- **Every cell loses margin vs g0capsfix, and the rival gains in every cell and on every read.** The rival gains +5.5k to +13.9k on g0capsfix
  (all of it in d15-29, our missing milk/wool/egg lanes); on flood +6.0k to +14.1k (N8 +6.0-7.1k, N6 +12.3-14.1k); on big +3.9k to +4.0k.
- **Best cell N8_9_d5** (8-tile plate, no melon d2-9, Q2 on d5):
  - g0capsfix, 20 games: own +2,130 (t 1.09), rival +7,286 (t 5.07), dmargin -5,156 (t -2.78), W 18 -> 17 (+0/-1).
    **Extended to 50 games** (boards 1-25 x 2 seats, vs D10WAVE1's `d10_ctl`): own **-2,618 (t -2.25)**, rival **+5,665 (t 5.47)**,
    dmargin **-8,283 (t -6.64)**, W 45 -> 37 (+0/-8). The 20-game own gain was noise. (The full 80-game rung for 4 cells, 240 games, did not fit:
    the shared 8-CPU remote ran at load 12-15 and ~27 s a game on 2 workers.)
  - flood: own **-7,048 (t -3.14)**, rival +6,458, dmargin -13,507 (t -4.28).
  - big: own **-410 (t -0.37)**, rival +3,976 (t 2.65), dmargin -4,386 (t -2.29).
  - Faithful live27 tapes (12 seats): own +563, rival **+6,979 (t 5.81)**, dmargin -6,416, W 2 -> 2. On tapes the rival's sales do not react,
    so its price gain is under-read there.
  - It fails every bar: margin < control -1k, flood own -7.0k < -1k, herd at d9 below the control, +30 melons < +40, tape rival +7.0k > +3k.
  - It is worse than MELONSHIFT1's P8d3 (the plate on d3-4 after the herd buy) on every shared read: P8d3 20-game g0capsfix dmargin +1,971,
    own +5,763; flood own -1,500; big own +4,962; faithful tape rival +2,326.
- **Q2 on d3 is worse than Q2 on d5 in every pair.** N8_9: dmargin -14,883 vs -5,156, own -6,135 vs +2,130. N6_9: -15,415 vs -18,035
  (N6 is dominated by the herd loss either way). The d3 quadrant is paid for out of the d4 purse (dawn d4 138 vs 844) and the geese go.
- **STOP = 29 (no melon after the plate) is the worst axis.** It costs our own coins **-9.5k (N8_d5) to -16.2k (N6_d5) in d15-29** vs g0capsfix
  (flood: -12.9k to -16.3k; big N8_d5: own -6.7k vs -0.4k) and does not shrink the rival's gain (N8_d5: +5.5k vs +7.3k; N6_d5: +12.0k vs +13.1k). Our late melons still sell at 140-158 a unit after a 3-5 tile plate,
  and MELON_SHIFT's cut does not hand the freed tiles to another crop (the day is sized against the smaller ask), so the tiles stand idle.
  Keep the late melons.
- **Named extras (context only; local faithful live27 tapes, each named in `checkpoint.txt` before it ran).** All three pay the rival more than P8d3:
  - `x_wf8` = the programme's own opening on the starting tiles (`MELON_SHIFT=8|9` + `WOOL_FIRST_ON` 2 cows / 3 sheep / 0 geese + Q2 on d6):
    h1 = wheat 11 + carrot 3 + melon 6 + cow 2 + sheep 3; 36 melons in d10-14. Faithful 13 seats: own -2,713, rival **+11,899 (t 7.2)**, dmargin -14,611,
    W 3 -> 1. Our cows hold the shared milk price down; two fewer cows hand it to the rival (REALLOC1's c2 cells said the same).
  - `x_n8sheep` = N8_9_d5 + `SHEEP_FIRST` 1 sheep (add): the purse swaps a cow for the sheep (h1 cow 3 + sheep 1), 48 melons in d10-14.
    Faithful 13: own +736, rival **+11,455 (t 5.2)**, dmargin -10,719.
  - `x_p8d3n7` = P8d3 + `PLATE_NO_LAND_BEFORE=7` (Q2 moved d5 -> d7 so the 1,000 pays the plate, not the d5-9 herd). Faithful 17: own -77,
    rival +3,342 (t 3.5), dmargin -3,419, against P8d3's +729 / +2,326 / -1,597 on the same tapes.
- **What the grid says.** The 3,000 d0 purse is fully spent on the herd, the seed and the feed reserve, and the 25 starting tiles are full. A d0-1 plate
  therefore displaces a herd animal (the sheep, a cow) or the feed reserve (animals starve), with or without the quadrant. The reacting rival sells
  into the milk / wool / egg units we stop supplying, in d15-29. The plate's 18-30 extra d10-14 melons (4-7k gross at 240) do not cover that.
- **CANDIDATE: none. PROMISING: none. LIVE-TRIAL WORTHY: none.** No package was built.
- **Next cell:** P8d3 (MELONSHIFT1's d3-4 plate, the only melon cell with own coins up on 80 games: +3,154, t 4.4) with the d5-9 herd held at the
  control's d9 herd (6 cows / 3 sheep / 2 geese) by HERD1's `HERD_PLAN` floor (worktree herd1 e20d57ab). The plate is then paid by the d3-4 strawberry/wheat
  seed alone, and the rival's +4.6k herd-lane gain is removed or confirmed. Judge on g0capsfix 80 games and flood. (COMBO1 runs the d0 plate with HERD_PLAN floors; this is the d3-4 plate.)

## 1. The grid (named before running, `checkpoint.txt` 07:35Z)
Cells: `MELON_SHIFT=N|STOP;PLATE_NO_LAND_BEFORE=D;LAND_DAY=D|99|0` with N in {6, 8}, STOP in {9, 29}, D in {5, 3} = 8 cells; tag `pn_N<N>_<STOP>_d<D>`.
References: the control PFS (`ms_ctl_*`, `d10_ctl`) and MELONSHIFT1's S8_9 with the land unblocked (`ms_S8_9_*`), both banked from the same harness;
`pn_id_*` are the identity runs on this tree. Screen = boards_m40 first 10 boards x 2 seats = 20 games per cell and rival.
Each rival block has two tables: the two purses with the window split (exact cash deltas vs the control; the control row shows levels) and the melon
units @ price; then the d0 state (dawn cash d1, the h1 market order in units per game, the Q2 / Q3 purchase days, the herd at d9 h12, our melon
tile-days d0-9 and our melons sold d10-14).

### vs g0capsfix (margin / flips)
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix | ms_ctl_gcf | 20 | 18->18 | +0/-0 | 109,563 | 84,533 | +25,030 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +2,715 / +2,791 / +101,057 | -1,946 / +23,852 / +59,627 | 0.0u@0 / 91.7u@179 | 46.3u@251 / 10.2u@231 |
| g0capsfix | ms_S8_9_gcf | 20 | 18->15 | +0/-3 | 112,571 | 103,971 | +8,600 | +3,008 (+2.01) | +19,439 (+12.72) | -16,431 (-7.28) | -3,181 / +7,860 / -1,672 | -287 / +968 / +18,758 | 78.0u@204 / 68.3u@51 | 45.4u@234 / 12.9u@116 |
| g0capsfix | pn_id_ctl_gcf | 6 | 6->6 | +0/-0 | 117,774 | 81,409 | +36,365 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +0 / +0 / +0 | +0 / +0 / +0 | 0.0u@0 / 84.0u@190 | 47.3u@251 / 7.7u@231 |
| g0capsfix | pn_id_S8_9_gcf | 6 | 6->6 | +0/-0 | 117,524 | 100,217 | +17,307 | -250 (-0.07) | +18,808 (+11.29) | -19,058 (-3.73) | -2,447 / +7,757 / -5,560 | -163 / +2,686 / +16,285 | 78.0u@206 / 58.0u@49 | 46.0u@231 / 16.5u@108 |
| g0capsfix | pn_N6_9_d5_gcf | 20 | 18->13 | +0/-5 | 104,625 | 97,630 | +6,995 | -4,938 (-5.86) | +13,097 (+7.88) | -18,035 (-8.62) | -1,795 / -2,263 / -880 | -99 / +770 / +12,426 | 18.0u@244 / 100.0u@153 | 40.6u@249 / 11.3u@224 |
| g0capsfix | pn_N6_29_d5_gcf | 20 | 18->4 | +0/-14 | 90,405 | 96,544 | -6,138 | -19,158 (-19.08) | +12,011 (+6.19) | -31,169 (-11.48) | -1,795 / -1,144 / -16,218 | -99 / +376 / +11,734 | 18.0u@244 / 0.0u@0 | 40.7u@249 / 11.2u@225 |
| g0capsfix | pn_N8_9_d5_gcf | 20 | 18->17 | +0/-1 | 111,693 | 91,819 | +19,875 | +2,130 (+1.09) | +7,286 (+5.07) | -5,156 (-2.78) | -366 / +1,364 / +1,133 | +69 / +169 / +7,048 | 30.0u@240 / 87.1u@140 | 41.7u@245 / 11.2u@212 |
| g0capsfix | pn_N8_29_d5_gcf | 20 | 18->16 | +0/-2 | 101,533 | 90,013 | +11,520 | -8,030 (-4.19) | +5,481 (+3.55) | -13,511 (-8.47) | -366 / +1,828 / -9,492 | +69 / -1,171 / +6,583 | 30.0u@240 / 0.0u@0 | 41.4u@245 / 10.5u@214 |
| g0capsfix | pn_N6_9_d3_gcf | 20 | 18->12 | +0/-6 | 107,764 | 98,149 | +9,615 | -1,799 (-1.06) | +13,616 (+6.59) | -15,415 (-5.50) | -1,820 / -2,127 / +2,148 | -26 / +1,103 / +12,540 | 18.0u@244 / 98.0u@158 | 41.0u@249 / 8.6u@226 |
| g0capsfix | pn_N6_29_d3_gcf | 20 | 18->8 | +0/-10 | 93,985 | 98,421 | -4,436 | -15,578 (-7.50) | +13,889 (+6.31) | -29,467 (-9.23) | -1,820 / -901 / -12,858 | -26 / +464 / +13,452 | 18.0u@244 / 0.0u@0 | 40.8u@249 / 8.8u@227 |
| g0capsfix | pn_N8_9_d3_gcf | 20 | 18->16 | +0/-2 | 103,428 | 93,281 | +10,148 | -6,135 (-8.67) | +8,748 (+6.91) | -14,883 (-11.14) | -973 / +433 / -5,594 | +258 / +22 / +8,468 | 30.0u@240 / 88.9u@144 | 41.1u@245 / 8.3u@215 |
| g0capsfix | pn_N8_29_d3_gcf | 20 | 18->14 | +0/-4 | 94,368 | 91,442 | +2,926 | -15,195 (-17.34) | +6,910 (+5.04) | -22,105 (-15.35) | -973 / +957 / -15,179 | +258 / -94 / +6,746 | 30.0u@240 / 0.0u@0 | 41.1u@245 / 8.0u@215 |

| cell | n state | dawn cash d1 | d0 h1 order (units/game) | Q2 day (bought; d0) | Q3 day (bought) | our COW/SHEEP/GOOSE d9 | our melon tile-days d0-9 | our melons d10-14 |
|---|---|---|---|---|---|---|---|---|
| ms_ctl_gcf | 20 | 213 | cow 4.0 goose 1.0 sheep 1.0 carr 8.0 whea 11.0 | 5.0 (20/20; d0 0) | 9.9 (20/20; d0 0) | 6.1/3.4/1.7 | 9.3 | 0.0u@0 |
| ms_S8_9_gcf | 20 | 976 | cow 2.0 goose 1.0 carr 3.0 melo 8.0 whea 11.0 | 0.0 (20/20; d0 20) | 7.8 (20/20; d0 0) | 3.1/0.3/0.5 | 113.0 | 78.0u@204 |
| pn_id_ctl_gcf | 6 | 213 | cow 4.0 goose 1.0 sheep 1.0 carr 8.0 whea 11.0 | 5.0 (6/6; d0 0) | 9.7 (6/6; d0 0) | 5.0/2.3/3.3 | 8.0 | 0.0u@0 |
| pn_id_S8_9_gcf | 6 | 976 | cow 2.0 goose 1.0 carr 3.0 melo 8.0 whea 11.0 | 0.0 (6/6; d0 6) | 7.7 (6/6; d0 0) | 3.0/0.0/1.0 | 113.0 | 78.0u@206 |
| pn_N6_9_d5_gcf | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.1 (18/20; d0 0) | 4.0/0.4/0.1 | 27.0 | 18.0u@244 |
| pn_N6_29_d5_gcf | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 5.0 (20/20; d0 0) | 10.9 (14/20; d0 0) | 4.0/0.4/0.1 | 27.0 | 18.0u@244 |
| pn_N8_9_d5_gcf | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 10.6 (20/20; d0 0) | 5.2/0.8/0.9 | 45.0 | 30.0u@240 |
| pn_N8_29_d5_gcf | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 10.7 (20/20; d0 0) | 5.2/0.8/0.9 | 45.0 | 30.0u@240 |
| pn_N6_9_d3_gcf | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 4.2 (20/20; d0 0) | 11.6 (19/20; d0 0) | 3.9/0.2/0.2 | 27.0 | 18.0u@244 |
| pn_N6_29_d3_gcf | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 4.2 (20/20; d0 0) | 11.3 (12/20; d0 0) | 3.9/0.2/0.2 | 27.0 | 18.0u@244 |
| pn_N8_9_d3_gcf | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 3.0 (20/20; d0 0) | 11.6 (20/20; d0 0) | 4.7/0.5/0.1 | 45.0 | 30.0u@240 |
| pn_N8_29_d3_gcf | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 3.0 (20/20; d0 0) | 11.7 (20/20; d0 0) | 4.7/0.5/0.1 | 45.0 | 30.0u@240 |

### The herd ledger d0-9 (g0capsfix games): animals bought vs standing at d9, and the dawn purse
| cell | n | animals bought d0-9 C/S/G | standing at d9 h12 C/S/G | lost C/S/G | dawn cash d1 / d2 / d3 / d4 / d5 |
|---|---|---|---|---|---|
| ms_ctl_gcf | 20 | 6.1/3.4/1.8 | 6.1/3.4/1.7 | 0.0/0.0/0.1 | 213 / 127 / 627 / 666 / 1,404 |
| ms_S8_9_gcf | 20 | 3.1/0.4/1.0 | 3.1/0.3/0.5 | 0.0/0.1/0.6 | 976 / 258 / 366 / 487 / 471 |
| pn_N6_9_d5_gcf | 20 | 5.0/1.5/1.1 | 4.0/0.4/0.1 | 1.0/1.1/1.0 | 33 / 33 / 622 / 702 / 845 |
| pn_N6_29_d5_gcf | 20 | 5.0/1.5/1.1 | 4.0/0.4/0.1 | 1.0/1.1/1.0 | 33 / 33 / 622 / 702 / 845 |
| pn_N8_9_d5_gcf | 20 | 5.2/1.4/1.1 | 5.2/0.8/0.9 | 0.1/0.6/0.2 | 416 / 388 / 729 / 844 / 911 |
| pn_N8_29_d5_gcf | 20 | 5.2/1.4/1.1 | 5.2/0.8/0.9 | 0.1/0.6/0.2 | 416 / 388 / 729 / 844 / 911 |
| pn_N6_9_d3_gcf | 20 | 4.9/1.3/1.2 | 3.9/0.2/0.2 | 1.1/1.1/1.0 | 33 / 33 / 622 / 702 / 384 |
| pn_N6_29_d3_gcf | 20 | 4.9/1.3/1.2 | 3.9/0.2/0.2 | 1.1/1.1/1.0 | 33 / 33 / 622 / 702 / 384 |
| pn_N8_9_d3_gcf | 20 | 4.7/0.9/1.1 | 4.7/0.5/0.1 | 0.0/0.4/1.0 | 416 / 388 / 729 / 138 / 804 |
| pn_N8_29_d3_gcf | 20 | 4.7/0.9/1.1 | 4.7/0.5/0.1 | 0.0/0.4/1.0 | 416 / 388 / 729 / 138 / 804 |

### vs flood (the dours read)
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flood | ms_ctl_fl | 20 | 20->20 | +0/-0 | 119,429 | 75,093 | +44,336 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +3,333 / +2,090 / +111,006 | -2,286 / +17,273 / +57,106 | 0.0u@0 / 90.0u@192 | 43.2u@252 / 6.5u@233 |
| flood | ms_S8_9_fl | 20 | 20->20 | +0/-0 | 120,063 | 92,654 | +27,410 | +634 (+0.24) | +17,560 (+11.31) | -16,926 (-5.14) | -4,130 / +12,454 / -7,689 | -210 / -215 / +17,985 | 78.0u@222 / 60.0u@76 | 43.6u@207 / 6.2u@120 |
| flood | pn_N6_9_d5_fl | 20 | 20->20 | +0/-0 | 116,099 | 89,231 | +26,868 | -3,330 (-1.26) | +14,138 (+6.62) | -17,468 (-5.04) | -2,334 / -1,174 / +178 | -363 / +1,831 / +12,670 | 18.0u@252 / 96.5u@145 | 46.5u@244 / 10.4u@222 |
| flood | pn_N6_29_d5_fl | 20 | 20->16 | +0/-4 | 104,585 | 89,028 | +15,558 | -14,844 (-4.97) | +13,935 (+6.72) | -28,779 (-6.39) | -2,334 / +366 / -12,876 | -363 / +938 / +13,359 | 18.0u@252 / 0.0u@0 | 44.3u@244 / 11.8u@223 |
| flood | pn_N8_9_d5_fl | 20 | 20->20 | +0/-0 | 112,381 | 81,552 | +30,829 | -7,048 (-3.14) | +6,458 (+4.83) | -13,507 (-4.28) | -1,210 / +2,860 / -8,699 | +364 / +1,624 / +4,470 | 30.0u@246 / 85.4u@128 | 49.9u@236 / 9.9u@205 |
| flood | pn_N8_29_d5_fl | 20 | 20->20 | +0/-0 | 105,849 | 82,078 | +23,771 | -13,580 (-6.77) | +6,985 (+5.93) | -20,565 (-7.49) | -1,210 / +3,900 / -16,270 | +364 / +157 / +6,464 | 30.0u@246 / 0.0u@0 | 48.1u@237 / 11.6u@203 |
| flood | pn_N6_9_d3_fl | 20 | 20->20 | +0/-0 | 118,293 | 87,356 | +30,937 | -1,136 (-0.38) | +12,263 (+6.24) | -13,400 (-3.42) | -2,689 / -307 / +1,860 | -381 / +966 / +11,678 | 18.0u@252 / 95.2u@147 | 47.2u@243 / 9.3u@222 |
| flood | pn_N6_29_d3_fl | 20 | 20->18 | +0/-2 | 108,052 | 87,648 | +20,405 | -11,377 (-3.96) | +12,555 (+6.59) | -23,932 (-5.97) | -2,689 / +985 / -9,673 | -381 / +708 / +12,228 | 18.0u@252 / 0.0u@0 | 47.1u@243 / 9.8u@222 |
| flood | pn_N8_9_d3_fl | 20 | 20->20 | +0/-0 | 114,588 | 82,197 | +32,392 | -4,841 (-1.79) | +7,104 (+3.52) | -11,945 (-3.27) | -959 / +1,897 / -5,778 | -113 / +900 / +6,316 | 30.0u@249 / 83.8u@133 | 49.0u@235 / 9.1u@203 |
| flood | pn_N8_29_d3_fl | 20 | 20->20 | +0/-0 | 107,659 | 81,056 | +26,603 | -11,770 (-4.38) | +5,963 (+2.50) | -17,733 (-4.72) | -959 / +2,372 / -13,183 | -113 / +169 / +5,906 | 30.0u@249 / 0.0u@0 | 47.8u@236 / 9.7u@205 |

| cell | n state | dawn cash d1 | d0 h1 order (units/game) | Q2 day (bought; d0) | Q3 day (bought) | our COW/SHEEP/GOOSE d9 | our melon tile-days d0-9 | our melons d10-14 |
|---|---|---|---|---|---|---|---|---|
| ms_ctl_fl | 20 | 213 | cow 4.0 goose 1.0 sheep 1.0 carr 8.0 whea 11.0 | 5.0 (20/20; d0 0) | 10.0 (20/20; d0 0) | 6.0/3.1/1.3 | 10.9 | 0.0u@0 |
| ms_S8_9_fl | 20 | 976 | cow 2.0 goose 1.0 carr 3.0 melo 8.0 whea 11.0 | 0.0 (20/20; d0 20) | 7.7 (20/20; d0 0) | 3.2/0.2/0.2 | 113.0 | 78.0u@222 |
| pn_N6_9_d5_fl | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.5 (16/20; d0 0) | 3.5/0.3/0.2 | 27.0 | 18.0u@252 |
| pn_N6_29_d5_fl | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.6 (10/20; d0 0) | 3.5/0.3/0.2 | 27.0 | 18.0u@252 |
| pn_N8_9_d5_fl | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.2 (20/20; d0 0) | 4.8/0.7/1.0 | 45.0 | 30.0u@246 |
| pn_N8_29_d5_fl | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.3 (20/20; d0 0) | 4.8/0.7/1.0 | 45.0 | 30.0u@246 |
| pn_N6_9_d3_fl | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 4.2 (20/20; d0 0) | 11.8 (20/20; d0 0) | 3.9/0.2/0.1 | 27.0 | 18.0u@252 |
| pn_N6_29_d3_fl | 20 | 33 | cow 4.0 goose 1.0 sheep 1.0 carr 5.0 melo 3.0 whea 11.0 | 4.2 (20/20; d0 0) | 11.6 (10/20; d0 0) | 3.9/0.2/0.1 | 27.0 | 18.0u@252 |
| pn_N8_9_d3_fl | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 3.0 (20/20; d0 0) | 11.2 (20/20; d0 0) | 4.7/0.4/0.1 | 45.0 | 30.0u@249 |
| pn_N8_29_d3_fl | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 3.0 (20/20; d0 0) | 11.4 (20/20; d0 0) | 4.7/0.4/0.1 | 45.0 | 30.0u@249 |

### vs big (the 2 best cells by g0capsfix dmargin)
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| big | ms_ctl_big | 20 | 20->20 | +0/-0 | 112,161 | 71,566 | +40,596 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +3,245 / +1,652 / +104,265 | -2,238 / +15,047 / +55,757 | 0.0u@0 / 83.8u@180 | 48.9u@250 / 11.9u@230 |
| big | pn_N8_9_d5_big | 20 | 20->20 | +0/-0 | 111,751 | 75,542 | +36,209 | -410 (-0.37) | +3,976 (+2.65) | -4,386 (-2.29) | -1,188 / +1,953 / -1,175 | -235 / +1,434 / +2,777 | 30.0u@242 / 77.2u@127 | 55.1u@235 / 9.8u@197 |
| big | pn_N8_29_d5_big | 20 | 20->20 | +0/-0 | 105,456 | 75,445 | +30,011 | -6,706 (-4.95) | +3,879 (+2.78) | -10,585 (-4.42) | -1,188 / +2,859 / -8,376 | -235 / +810 / +3,305 | 30.0u@242 / 0.0u@0 | 55.3u@235 / 10.2u@197 |

| cell | n state | dawn cash d1 | d0 h1 order (units/game) | Q2 day (bought; d0) | Q3 day (bought) | our COW/SHEEP/GOOSE d9 | our melon tile-days d0-9 | our melons d10-14 |
|---|---|---|---|---|---|---|---|---|
| ms_ctl_big | 20 | 213 | cow 4.0 goose 1.0 sheep 1.0 carr 8.0 whea 11.0 | 5.0 (20/20; d0 0) | 10.0 (20/20; d0 0) | 6.0/3.1/1.5 | 10.8 | 0.0u@0 |
| pn_N8_9_d5_big | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.2 (20/20; d0 0) | 5.0/0.6/0.9 | 45.0 | 30.0u@242 |
| pn_N8_29_d5_big | 20 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (20/20; d0 0) | 11.4 (20/20; d0 0) | 5.0/0.6/0.9 | 45.0 | 30.0u@242 |

### vs g0capsfix, the best cell on 50 games (boards 1-25 x 2 seats; control = D10WAVE1's d10_ctl, same harness)
| rival | cell | n | W ctl->cell | flips | ours | rival | margin | dours (t) | dtheirs (t) | dmargin (t) | d ours d0-9 / d10-14 / d15-29 | d rival d0-9 / d10-14 / d15-29 | our melon u@price d10-14 / d15-29 | rival melon u@price d10-14 / d15-29 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g0capsfix (m40 boards 1-25, 50 games) | d10_ctl | 80 | 75->75 | +0/-0 | 115,169 | 90,217 | +24,952 | +0 (+nan) | +0 (+nan) | +0 (+nan) | +2,670 / +2,227 / +107,271 | -2,094 / +23,386 / +65,926 | 0.0u@0 / 92.0u@176 | 45.7u@251 / 12.8u@227 |
| g0capsfix (m40 boards 1-25, 50 games) | pn_N8_9_d5_gcf50 | 50 | 45->37 | +0/-8 | 108,537 | 93,592 | +14,945 | -2,618 (-2.25) | +5,665 (+5.47) | -8,283 (-6.64) | -466 / +1,519 / -3,671 | -114 / -68 / +5,847 | 30.0u@240 / 87.6u@139 | 41.2u@245 / 11.5u@210 |

| cell | n state | dawn cash d1 | d0 h1 order (units/game) | Q2 day (bought; d0) | Q3 day (bought) | our COW/SHEEP/GOOSE d9 | our melon tile-days d0-9 | our melons d10-14 |
|---|---|---|---|---|---|---|---|---|
| d10_ctl | 0 | n/a |
| pn_N8_9_d5_gcf50 | 50 | 416 | cow 4.0 goose 1.0 carr 3.0 melo 5.0 whea 11.0 | 5.0 (50/50; d0 0) | 10.6 (50/50; d0 0) | 4.9/0.7/1.1 | 45.0 | 30.0u@240 |

### Faithful live27 tape check (MELONTRIAL1 / MELONSHIFT1 method: the cell as the vrp21_melon package's fired switch-set, file agent on the 18 fired live27 tapes, vs live = PFS)
On tapes the rival's sales do not react, so its price gain is under-read. `x_*` rows are named extras (context only).

#### l27_8_9_d5
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]; SELL MELON d10-14 [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 8 | +4/-0 | +9,336 (+2.25) | -3,988 (-0.72) | +13,323 (+1.43) |
| fired | 18 | 4 -> 8 | +4/-0 | +9,336 (+2.25) | -3,988 (-0.72) | +13,323 (+1.43) |
| fired, JC1-faithful both | 12 | 2 -> 2 | +0/-0 | +563 (+0.27) | +6,979 (+5.81) | -6,416 (-3.54) |


#### l27_8_9_d3
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]; SELL MELON d10-14 [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 5 | +4/-3 | +5,682 (+1.44) | -2,118 (-0.47) | +7,801 (+0.95) |
| fired | 18 | 4 -> 5 | +4/-3 | +5,682 (+1.44) | -2,118 (-0.47) | +7,801 (+0.95) |
| fired, JC1-faithful both | 12 | 2 -> 1 | +0/-1 | -1,574 (-0.92) | +6,808 (+8.17) | -8,383 (-4.46) |


#### l27_6_9_d5
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]; SELL MELON d10-14 [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 2 | +2/-4 | -458 (-0.13) | +9,596 (+2.18) | -10,055 (-1.37) |
| fired | 18 | 4 -> 2 | +2/-4 | -458 (-0.13) | +9,596 (+2.18) | -10,055 (-1.37) |
| fired, JC1-faithful both | 15 | 3 -> 0 | +0/-3 | -4,415 (-1.87) | +15,510 (+6.81) | -19,925 (-5.93) |


#### l27_8_29_d5
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]; SELL MELON d10-14 [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 5 | +4/-3 | +4,155 (+1.00) | -5,935 (-1.09) | +10,090 (+1.09) |
| fired | 18 | 4 -> 5 | +4/-3 | +4,155 (+1.00) | -5,935 (-1.09) | +10,090 (+1.09) |
| fired, JC1-faithful both | 12 | 2 -> 1 | +0/-1 | -4,427 (-2.23) | +4,739 (+3.19) | -9,166 (-3.67) |


#### l27_x_wf8
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]; SELL MELON d10-14 [36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 5 | +4/-3 | +4,733 (+1.20) | +2,453 (+0.51) | +2,280 (+0.28) |
| fired | 18 | 4 -> 5 | +4/-3 | +4,733 (+1.20) | +2,453 (+0.51) | +2,280 (+0.28) |
| fired, JC1-faithful both | 13 | 3 -> 1 | +0/-2 | -2,713 (-1.02) | +11,899 (+7.16) | -14,611 (-6.66) |


#### l27_x_n8sheep
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]; SELL MELON d10-14 [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 5 | +4/-3 | +8,768 (+2.18) | +817 (+0.16) | +7,951 (+0.90) |
| fired | 18 | 4 -> 5 | +4/-3 | +8,768 (+2.18) | +817 (+0.16) | +7,951 (+0.90) |
| fired, JC1-faithful both | 13 | 3 -> 1 | +0/-2 | +736 (+0.41) | +11,455 (+5.16) | -10,719 (-4.63) |


#### l27_x_p8d3n7
h1 / melon: fired h1 values [1, 19, 73, 190, 564, 661, 938, 2046]; mel_d1 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; SELL MELON d10-14 [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 36, 36, 36, 36]

| set | n | W live -> pkg | flips | dours (t) | dtheirs (t) | dmargin (t) |
|---|---|---|---|---|---|---|
| all 27 | 18 | 4 -> 3 | +2/-3 | +1,368 (+0.59) | +691 (+0.25) | +677 (+0.15) |
| fired | 18 | 4 -> 3 | +2/-3 | +1,368 (+0.59) | +691 (+0.25) | +677 (+0.15) |
| fired, JC1-faithful both | 17 | 4 -> 2 | +1/-3 | -77 (-0.04) | +3,342 (+3.45) | -3,419 (-1.48) |


## 2. Bars (as dispatched)
LIVE-TRIAL WORTHY = own >= control -1k on flood AND big, herd at d9 >= control, d10-14 melons >= +40, faithful-tape rival <= +3k, margin vs g0capsfix >= control -1k.
CANDIDATE = margin t >= 2 on g0capsfix with own >= control -1k on flood. PROMISING = one read t >= 2 with the others flat. Else NONE.
Reads: g0capsfix 20 games vs ms_ctl_gcf; flood 20 vs ms_ctl_fl; big 20 vs ms_ctl_big; tape = fired JC1-faithful live27 seats (dtheirs).

| cell | g0capsfix own / rival / dmargin (t) / W (flips) | flood own (t) / rival | big own (t) / rival | herd d9 C/S/G (ctl 6.1/3.4/1.7) | melons d10-14 (ctl 0) | tape rival (faithful) | verdict |
|---|---|---|---|---|---|---|---|
| N8_9_d5 | +2,130 / +7,286 / -5,156 (-2.78) / 18->17 (+0/-1) | -7,048 (-3.14) / +6,458 | -410 (-0.37) / +3,976 | 5.2/0.8/0.9 | +30 | +6,979 (+5.81) | NONE |
| N8_29_d5 | -8,030 / +5,481 / -13,511 (-8.47) / 18->16 (+0/-2) | -13,580 (-6.77) / +6,985 | -6,706 (-4.95) / +3,879 | 5.2/0.8/0.9 | +30 | +4,739 (+3.19) | NONE |
| N8_9_d3 | -6,135 / +8,748 / -14,883 (-11.14) / 18->16 (+0/-2) | -4,841 (-1.79) / +7,104 | - | 4.7/0.5/0.1 | +30 | +6,808 (+8.17) | NONE |
| N6_9_d3 | -1,799 / +13,616 / -15,415 (-5.50) / 18->12 (+0/-6) | -1,136 (-0.38) / +12,263 | - | 3.9/0.2/0.2 | +18 | - | NONE |
| N6_9_d5 | -4,938 / +13,097 / -18,035 (-8.62) / 18->13 (+0/-5) | -3,330 (-1.26) / +14,138 | - | 4.0/0.4/0.1 | +18 | +15,510 (+6.81) | NONE |
| N8_29_d3 | -15,195 / +6,910 / -22,105 (-15.35) / 18->14 (+0/-4) | -11,770 (-4.38) / +5,963 | - | 4.7/0.5/0.1 | +30 | - | NONE |
| N6_29_d3 | -15,578 / +13,889 / -29,467 (-9.23) / 18->8 (+0/-10) | -11,377 (-3.96) / +12,555 | - | 3.9/0.2/0.2 | +18 | - | NONE |
| N6_29_d5 | -19,158 / +12,011 / -31,169 (-11.48) / 18->4 (+0/-14) | -14,844 (-4.97) / +13,935 | - | 4.0/0.4/0.1 | +18 | - | NONE |

## Method
- **Worktree** `/mnt/e/_work/kagg3_wt_platenoland1` (sparse), branch `platenoland1_0929` from master 8d670dad: cherry-picks of MELONSHIFT1 0f27770a
  (`MELON_SHIFT="N|STOP"`, -> 14d155ef) and LAND1 58422323 (`LAND_DAY="q2|q3|reserve"`, -> a5489c73), plus **bf4191f2** `PLATE_NO_LAND_BEFORE=<day>`.
- **Why a new gate.** `LAND_DAY` only adds purchases (`max` with the shipped decision), so it cannot stop the d0 h3 BUY_LAND that the plate triggers.
  `PLATE_NO_LAND_BEFORE=D` zeroes `buy_land` on days < D in `_derive`, after every other land rule (program engine, Q4, LAND_DAY, Q4_VRP, MACRO_EXEC).
  The day is then planned on `wants_pre`, the 25 starting tiles, and the purse is not reduced by the land gap. `LAND_DAY="D|99|0"` then buys Q2 from day D
  on the first day the purse plus the day's projected sales covers the price; Q3 stays with the shipped valuation. None / 0 = OFF, one Python-false branch.
- **Identity.** OFF (the pnl1 tree, no switch) equals `ms_ctl_gcf` 6/6 and `d10_ctl` 6/6 on every money column (ours, theirs, h1, d10, d15, d18).
  `MELON_SHIFT=8|9` alone equals MELONSHIFT1's `ms_S8_9_gcf` 6/6 (first 3 m40 boards x 2 seats, vs g0capsfix).
- **Judge.** Closed loop on the remote CPU (the REACTCLONE1 / JUDGERIVAL1-3 harness `judgerival1/rcr.py` through MELONSHIFT1's state wrapper
  `melonshift1/ms_rc.py`, which logs the dawn cash, the h12 melon tiles, the d9 herd and the d0-12 market rows). The cells are paired on the same (board, seat)
  games with MELONSHIFT1's banked controls from the same harness: `ms_ctl_gcf` (20 g), `d10_ctl` (80 g), `ms_ctl_fl`, `ms_ctl_big`. flips = W changes vs the control;
  t = paired t. The windows are exact cash deltas: d0-9 = dawn d10 - 3,000, d10-14 = dawn d15 - dawn d10, d15-29 = final - dawn d15.
- **Cells.** `MELON_SHIFT=N|STOP;PLATE_NO_LAND_BEFORE=D;LAND_DAY=D|99|0` with the PFS OFF string; tag `pn_N<N>_<STOP>_d<D>`.

## Files
- `S/platenoland1/pn_worker.sh` (remote queue worker, one spec at a time from `queue.txt` under flock), `queue0.txt` / `queue1.txt` / `queue2.txt` (the grid and its reorders).
- `pn_an.py` (the tables: two purses, windows, melon u@price, dawn cash, h1 order, Q2/Q3 day, herd d9, melon tile-days), `mk_tables.sh` (pull + join + tables),
  `idcheck.py` (identity), `res/herd_ledger.md`, `res/table_{gcf,fl,big,gcf50}.md`, `res/rc/` (csv + sales ledger + state log per run, plus the banked controls).
- `pnl.patch` (the worktree plan.py diff vs master), `mkpkg.sh` / `tape.sh` (+ `_x` variants for the named extras), `pkgrun.py` / `tbl_l27.py` (MELONSHIFT1 copies),
  `res/pkg_l27_*.csv`, `res/tape_*.md`. The per-step action logs `res/acts_*.json` stay local (not committed).
- `checkpoint.txt` (clock, runs, numbers), `logs/`, `mkdoc.sh` (this doc).
