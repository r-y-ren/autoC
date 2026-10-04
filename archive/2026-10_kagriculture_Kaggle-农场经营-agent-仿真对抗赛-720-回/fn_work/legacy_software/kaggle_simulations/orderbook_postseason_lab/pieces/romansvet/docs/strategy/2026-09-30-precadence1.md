# PRECADENCE1 (2026-09-30): pre-empting the melon programme's sale cadence live, judged closed-loop on real P48 tapes

## Idea
P48LOSS1R's tape oracle 'pre3' sold our shed wool, milk and strawberry one step before each rival sale of that product. On P48 losses it read +988/game (t 3.5), with 9/84 flips. It needs the tape's next rival sale step. Its purse split was own -432 / theirs -1,420 on losses and own -1,098 / theirs -2,121 on wins, so it is pure denial and fails own >= 0 even as an oracle. This stream tests the live stand-in: the programme sells milk, wool and strawberry on h1/5/9/13/17/21 (RULEBOOK_P48 5.2), so we sell our stock at the cadence hour minus the lead, on latched programme seats only.

## What of the rival is observable
- `obs.farms[rival]`: `money`, `hands` (positions), `hires_today`, `farmer`, `unlocked_quadrants`, and `tiles` (crop or animal, `yield_units` = ripe units on the tile, `planted_day`, water and fertiliser state).
- The public pot: `market.inventory` and `market.prices`. With our own row known, the RIVAL_TELL identity (`agent/tell.py`) gives the rival's exact net sales one step behind.
- The rival's shed and carried inventories are NOT observable. The rule estimates the shed as drops in the rival's tile `yield_units` (collections and harvests of strawberry, cows and sheep) minus its net sales, floored at 0.

## Rule (`src/kagg3/agent/precadence.py`, switch `precadence.ON`, default OFF)
- Latch at d2 h0: the rival has 1..10 MELON tiles (P48LOSS1R latch A: 113/113 P48, 0/266 V, 0/25 Vx). Unlatched seats return the action unchanged, so V play is identical by construction.
- From d15, at hour (c - LEAD) for each cadence hour c: for each product in PRODUCTS, if the rival's estimated shed is >= 1 (wool also needs price >= 25, the P48 gate) and our shed is >= MIN_LOT, SELL all of our shed stock of it.
- WITHHOLD=1 also drops our WOOL sells at the cadence hour itself when the rival's wool gate is open.
- The hook is one `if _PC.ON` after `_pfs_act` in `Runtime.act`.

## Judge
P48TAPE103: the anchor PFS plays our seat in 103 real P48 games, with P48 replayed from its tape (fast engine; the control is exact 103/103, so the control margin = the live margin). The split was frozen before any read: TUNE = odd lines of p103.txt (n 51, md5 dea0a0b5) and HOLD = even lines (n 52, md5 3cc63964). Control sale units come from P48LOSS1R's exact ledger books; they match the runner's own snapshots on the OFF smoke game. The gate-reactive mode (GR=1, the coordinator's 07:31Z note) handles the rival's wool: a taped P48 wool sale at d15+ is dropped when the live price was >= 30 and the sim price is < 20. A cadence-hour hold (h = 1 mod 4) with live price < 20 and sim price >= 30 becomes a sale of all rival shed wool. After a drop, later taped wool sales sell max(tape lot, shed). These are the hard flips in P48SWEEP1R's wool.py.

## Diagnostics before the grid
- Rival sale steps on P48TAPE103, d15-29 (tape). Wool, milk and strawberry peak on h1/5/9/13/17/21, but they are spread over every hour. On the smoke game (115531916) the rival sold W/M/S at 226 steps, of which 149 were on h = 1 mod 4. Our rule fired 22 times on that game, and 10/22 fires were followed by a rival sale of the same product on the next step (precision 0.45). The oracle fires on all 226 steps, with small lots; the live rule cannot see those steps.
- Smoke, 1 game: OFF exact (ndiff 0), ON dmargin -1,455 (own -3,127, theirs -1,672).

## TUNE grid (n 51 per cell, complete 3 x 2 x 2 x 2; dmargin/own/theirs = arm - exact control, per game; units = our sold units vs the ledger control)
| cell (products / lead / min lot / withhold) | n | W ctl->arm | flips +/- | dmargin (t) | own (t) | theirs (t) | straw d15-17 u | animal d18-29 u | p99 max s |
|---|---|---|---|---|---|---|---|---|---|
| WM / 2 / 6 / 0 | 51 | 13->12 | +2/-3 | -351 (-1.32) | -815 (-3.57) | -464 (-2.64) | +0.04 | +3.47 | 0.595 |
| S / 1 / 6 / 0 | 51 | 13->13 | +2/-2 | -378 (-1.59) | -1070 (-4.63) | -692 (-3.88) | +0.00 | +1.12 | 0.506 |
| S / 1 / 3 / 0 | 51 | 13->13 | +2/-2 | -424 (-1.79) | -1138 (-5.01) | -714 (-4.02) | +0.00 | +1.04 | 0.485 |
| WM / 1 / 6 / 0 | 51 | 13->14 | +3/-2 | -477 (-1.89) | -1037 (-4.41) | -560 (-3.14) | +0.04 | +3.59 | 0.577 |
| S / 2 / 6 / 0 | 51 | 13->13 | +2/-2 | -479 (-2.05) | -1068 (-4.91) | -588 (-3.30) | +0.00 | +1.14 | 0.537 |
| WM / 2 / 3 / 1 | 51 | 13->13 | +2/-2 | -488 (-1.79) | -1020 (-4.29) | -532 (-2.74) | +0.00 | +3.35 | 0.466 |
| WM / 2 / 6 / 1 | 51 | 13->11 | +1/-3 | -494 (-1.62) | -811 (-3.44) | -316 (-1.67) | -0.06 | +2.75 | 0.539 |
| S / 2 / 3 / 0 | 51 | 13->13 | +2/-2 | -528 (-2.28) | -1137 (-5.34) | -609 (-3.44) | +0.00 | +1.14 | 0.506 |
| WM / 2 / 3 / 0 | 51 | 13->13 | +2/-2 | -558 (-2.02) | -1056 (-4.40) | -498 (-2.68) | +0.04 | +3.06 | 0.494 |
| WM / 1 / 6 / 1 | 51 | 13->12 | +2/-3 | -586 (-2.07) | -1008 (-4.33) | -422 (-2.22) | -0.08 | +2.84 | 0.598 |
| WM / 1 / 3 / 0 | 51 | 13->13 | +2/-2 | -614 (-2.46) | -1287 (-5.10) | -674 (-3.71) | +0.04 | +3.61 | 0.455 |
| WM / 1 / 3 / 1 | 51 | 13->13 | +2/-2 | -655 (-2.31) | -1304 (-4.88) | -650 (-3.48) | +0.00 | +3.41 | 0.493 |
| WMS / 2 / 6 / 0 | 51 | 13->13 | +3/-3 | -1030 (-2.77) | -2065 (-6.04) | -1035 (-3.60) | +0.04 | +3.29 | 0.543 |
| WMS / 2 / 6 / 1 | 51 | 13->14 | +4/-3 | -1110 (-2.77) | -1988 (-6.34) | -878 (-3.08) | -0.06 | +2.88 | 0.593 |
| WMS / 1 / 6 / 1 | 51 | 13->13 | +3/-3 | -1181 (-3.09) | -2179 (-7.22) | -998 (-3.53) | -0.08 | +2.88 | 0.565 |
| WMS / 1 / 6 / 0 | 51 | 13->12 | +2/-3 | -1185 (-3.22) | -2283 (-6.85) | -1098 (-3.85) | +0.04 | +3.84 | 0.600 |
| WMS / 2 / 3 / 1 | 51 | 13->13 | +2/-2 | -1248 (-3.43) | -2351 (-6.86) | -1103 (-3.71) | +0.00 | +3.35 | 0.521 |
| WMS / 2 / 3 / 0 | 51 | 13->12 | +2/-3 | -1296 (-3.50) | -2390 (-6.86) | -1094 (-3.69) | +0.04 | +3.02 | 0.450 |
| WMS / 1 / 3 / 0 | 51 | 13->12 | +2/-3 | -1453 (-4.04) | -2657 (-7.54) | -1204 (-4.14) | +0.04 | +3.96 | 0.523 |
| WMS / 1 / 3 / 1 | 51 | 13->12 | +2/-3 | -1501 (-4.06) | -2694 (-7.59) | -1193 (-4.12) | +0.00 | +3.51 | 0.528 |
| S / 1 / 6 / 1 | 51 | 13->9 | +2/-6 | -4241 (-4.36) | -2083 (-4.44) | +2157 (3.41) | +0.71 | -3.22 | 0.487 |
| S / 1 / 3 / 1 | 51 | 13->9 | +2/-6 | -4302 (-4.43) | -2162 (-4.67) | +2140 (3.38) | +0.71 | -3.22 | 0.582 |
| S / 2 / 6 / 1 | 51 | 13->10 | +3/-6 | -4423 (-4.51) | -2150 (-4.65) | +2273 (3.55) | +0.71 | -4.78 | 0.518 |
| S / 2 / 3 / 1 | 51 | 13->9 | +2/-6 | -4472 (-4.57) | -2221 (-4.86) | +2251 (3.51) | +0.71 | -4.78 | 0.473 |

- **Every one of the 24 cells is negative on both our own purse (t -3.4 to -7.6) and the margin.** The pre-sale costs our purse about twice what it takes from the rival: WMS cells run own -2.0k..-2.7k against theirs -0.9k..-1.2k. The fixed-hour dump in P48LOSS1R read -1.8k; the rival-stock predictor recovers only part of that.
- **Withholding wool gifts the rival.** WITHHOLD=1 on strawberry-only cells (wool not pre-sold) reads dmargin -4.2k..-4.5k (t -4.4..-4.6), theirs +2.1k..+2.3k (t +3.4..+3.6), net flips -3/-4. When we stay out of the wool book at their dump hour, P48 sells its wool into a thinner pot. On WMS/WM cells the wool has already been pre-sold, so the withhold changes little.
- Products by margin: WM cells read -351..-655 (own -0.8k..-1.3k); S cells without withhold read -378..-528 (own -1.07k..-1.14k); WMS cells read -1.03k..-1.50k (own -2.0k..-2.7k). Strawberry pre-sales cost our own purse the most. MIN_LOT 6 beats MIN_LOT 3 on margin in 11/12 pairs (fewer fires, smaller loss).
- d15-17 strawberry units are unchanged (|delta| <= 0.08 u). d18-29 animal units are +1..+5 u: pre-selling empties the shed, and the d29 end book loses less to overflow. The unit bars hold, but no cell has own >= 0.

## Frozen best (own AND margin): WM / lead 2 / min lot 6 / withhold 0
| set | n | W ctl->arm | flips | dmargin (t) | own (t) | theirs (t) | straw d15-17 | animal d18-29 | wool-gate flips | p99 max s |
|---|---|---|---|---|---|---|---|---|---|---|
| TUNE | 51 | 13->12 | +2/-3 | -351 (-1.32) | -815 (-3.57) | -464 (-2.64) | +0.04 | +3.47 | - | 0.595 |
| HOLD taped (stopped at 45/52) | 45 | 13->13 | +0/-0 | -663 (-2.52) | -1,499 (-5.61) | -836 (-4.60) | -0.04 | +5.31 | 0 (taped) | 0.612 |
| HOLD gate-reactive (GR=1) | 52 | 15->15 | +0/-0 | -742 (-3.09) | -1,395 (-5.94) | -653 (-4.26) | -0.04 | +7.56 | 41 events in 14/52 games (40 hold, 1 sell) | 0.571 |

- Paired GR vs taped on the 45 common HOLD games: margin -0.3/game. The reactive wool gate flips 41 decisions but barely moves the purses, because held wool is sold at the rival's next taped wool sale.
- HOLD bars: own >= 0 FAIL (-1.4k/-1.5k), t >= 2 FAIL (negative), net flips >= +2 FAIL (0), wool-gate divergences = 0 FAIL (41). apply p99 0.57-0.61 s < 0.65 (control p99 on the smoke game 0.36 s at the same load). The box ran at load 12-16 on 8 cores, so these timings are inflated.
- Not run (coordinator stop at 09:42Z, box at load 16): OTH58 (1/56 game done, latch did not fire, identical), PQ4TAPE, V identity run (v6.txt staged). V identity holds by construction: an unlatched seat returns the PFS action unchanged. The latch is P48LOSS1R latch A (0/266 V, 0/25 Vx), and OFF is byte-identical (smoke ndiff 0).

## Verdict: NONE. Sale timing on programme seats is CLOSED.
The oracle's +988 was a tape artefact of knowing the rival's exact next sale step. It was own-negative even then (-432 L, -1,098 W). The live cadence stand-in costs our purse -0.8k..-2.7k in every cell. Nothing is packaged.

Files: branch precadence1_0930 (switch code, default OFF); S/precadence1 (run.py = P48SWEEP1R runner + sale snapshots + GR mode, sum2.py, res/*.jsonl, grid_A/B.txt, tune.txt/hold.txt, frozen_best.txt, checkpoint.txt); remote /home/user/stage_r/precadence1.
