Stream: BRAINSTORM7 (remote-only)
Date: 2026-09-30 04:19Z - ~05:25Z (committed by DOCSYNC1; Round 1 verbatim from S/brainstorm7/2026-09-30-brainstorm7.md; astra review = docs/strategy/2026-09-30-astra-brainstorm13.md)
Verdict: Round 1 - new judge P48TAPE103 (103/103 byte-exact, W 28/103 live); no cell passes (X3k +711 t 1.26, sheep cut 2 +785 t 1.48, every Q4-in-PFS -5.2..-8.5k); PFS is tile-bound, not labour-bound

# BRAINSTORM7 — Round 1 (2026-09-30, 04:19Z to about 05:25Z, remote only; /mnt/e down)

Everything is on user@remote-host:/home/user/stage_r/brainstorm7. Scripts: idown.py (runs our tree in OUR seat of a real game, opponent = its tape), sum.py, lab.py, prof2.py, sal.py. Results: *.jsonl.
M = measurement, H = hypothesis.

## New instrument: P48TAPE103 (M)
- The anchor PFS tree (programme2r/tree, switches OFF) in our own seat of real P48-class games, with the P48 opponent replayed from its tape, reproduces **103/103 games byte-exactly**: ndiff 0 on every step and final money equal.
  - 34 games are from the live pair 56687235/56687774 (cls.tsv P48c+P48t).
  - 69 are from 56652418/56686302/56686308 (games.json fam P48).
- Live record on the panel: W 28/103. Each cell takes 8 s/game, so about 14 min for 103 games on 1 nice-19 process.
- Limit: the rival is open-loop. P48 is a timetable rulebook whose lots depend on stock, and only wool is price-gated, so its reaction channel is narrow. Still, the panel is a tape and not closed-loop.
- It replaces the p48c clone leg for P48 reads. On p16, PFS goes 32/32 vs the clone but 28/103 live.

## Cells read on P48TAPE (M, paired vs exact live)
| cell | n | dmargin | t | own | theirs | flips |
|---|---|---|---|---|---|---|
| X3k (STRAW_DEMAND latched, d3+ cohort by shops) | 34 | +407 | 0.50 | +72 | -335 | +0 -0 |
| X3k pooled | 103 | +711 | 1.26 | +511 | -199 | +0 -4 |
| sheep cut 2, latched (V-identical by latch) | 103 | +785 | 1.48 | +396 | -389 | +1 -3 |
| sheep cut 4, latched | 34 | +331 | 0.31 | -228 | -559 | +0 -2 |
| Q4_PROG DSM (buy d11) | 34 | -8,504 | -7.57 | -6,056 | +2,449 | +0 -3 |
| Q4_PROG W8C3 + 1 hand | 34 | -6,616 | -4.92 | -5,551 | +1,065 | +0 -2 |
| Q4_VRP d14 visible purse, reserve 1k (buys d15-16) | 34 | -5,160 | -5.34 | -6,626 | -1,465 | +1 -3 |
Nothing passes. Every Q4 variant in the PFS planner loses 5-8.5k of its own purse on P48 boards.

## PFS census (M)
**V56 m40 ctl (steps h12, n 40)**
- Tiles: nq 3 = 75 tiles from d10. PFS never buys Q4.
- Occupancy d13-21: 56 plants + 18 animals (C7/S8/G3) = 74/75.
- Crew: 10.4-12.3 hands over d11-28.
- Cash: 7.7k at d14, 25.5k at d17, 47.7k at d20. Cash never binds after d14.
- Strawberry ask by day on one board: d3-7 = 4/4/11/9/1, d10 5, d11-14 1-2, 0 after d14.

**Live P48 games (34), per day d10-28**
| metric | PFS | MMPQ |
|---|---|---|
| PASS | 25.1 | 0.77 |
| MOVE | 89.5 | |
| WATER | 43.3 | 58 |
| FERTILIZE | 10.1 | 12.9 |
| FEED per animal-day | 0.82 | 0.78 |
| CARE per animal-day | 0.75 | 0.74 |
| empty tiles at h0 | 2.5 | 3.3 |
| plants + animal tiles | 53.7 + 17.5 | |

- Yield per harvest is at the ceiling: wheat 5.82/6, strawberry 1.96/2 (fertilized), carrot 3.93/4, melon 6.00/6.
- V games (25) look the same.
- **So PFS is tile-bound, not labour-bound. Spare labour has nothing to produce.**

**Prices, V56 m40 ctl (ours, d18-29 vs d10-17)**
- Strawberry 101 (was 189), wool 135 (180), milk 106 (116). These are the glut products: strawberry linear 1.6, wool sq 3.2, milk linear 1.6.
- Egg 51 flat, wheat 35. These do not glut (spec rows EGG hinge/log 0.2, WHEAT sqrt/log 0.2).

## Q1: PFS-side cells (mechanism / displaces / judge / expected / kill)
1. **Shop-sized strawberry (running).** Cuts the d3-14 strawberry cohort. It displaces the d15-17 wall, the V56 invariant. Judges: V56 + P48TAPE. Expected 0..+1k (M: n 103 +711 t 1.26 with net flips -4, so NOISE with lost wins; STRAWDEMAND1R |t| < 1.5). Kill: P48TAPE t < 2 at n 103.
2. **Shop-sized sheep/wool.** Mechanism: cut sheep on latched P48 seats. It displaces the wool supply. M: cut 2 gives +785 t 1.48 with net flips -2 (n 103); cut 4 is -2 wins. Closed as noise.
3. **Geese/eggs on PFS.** Eggs do not glut (51 c/u at any volume), and a goose gives about 2 eggs/goose-day (PFS 68.6 u / 2.9 geese / 12 d).
   - (H) Net is about 60 c/goose-day after feed, so +300..+600 per goose bought by d10.
   - The goose takes a tile: 74/75 are used, and the buy falls at d8-10 when cash is 2.8-3.1k. That is the GOOSE1/GEESE1 failure: the tile and the cash come out of the d15-17 strawberry supply.
   - Late geese (bought d14+) produce only 11 days, about +300 each, and still need a freed tile.
   - Kill: a goose placed on a tile the strawberry cohort would otherwise hold.
4. **Early tomato d8-12.** MMPQ 10.6 vs P48 1.0 tiles. PFS asks about 0. It would displace the d8-14 strawberry/wheat on a full farm. (H) 0..+1k. Kill: tomato tiles bought with d10 cash at 3.0k.
5. **Full labour / no PASS.** Dead by measurement: yields are at the ceiling and empty tiles are 2.5 at h0. Idle labour has no tiles.
6. **Wheat filler on free tiles.** Dead: 2.5 empty tiles at h0, the same as MMPQ's 3.3 structural harvest-replant lag.
7. **Late Q4 plus a filler (the only real capacity: 25 tiles from idle cash).** M: in PFS machinery every variant loses on P48TAPE34, -5.2k to -8.5k, own -5.6k to -6.6k. It would need a new executor that only plants wheat on the Q4 tiles.
   - (H) Arithmetic from d14: 25 tiles x 3 cycles x 5.8 u x 33 c = +14k gross, minus 4k land, seed and hires, so +4..+8k if it were executed cleanly.
   - Kill: Q4 wheat units d14-28 < 150, or own < 0 on P48TAPE.
8. **Feed-on-eve.** PFS feeds 0.82 per animal-day vs MMPQ 0.78. (H) Saving about 0.04 x 17 x 19 x 40 c = about 0.5k at most. Closed as too small.

## Q2: programme line
- A direct-emission executor reaching ratio >= 0.9 in 4 h is **implausible**.
  - PROGRAMME2R made 11 iterations (rb6-rb17) and moved 105.5k -> 106.5k (0.80 -> 0.804), with 2/20 games at >= 0.9.
  - The missing rules are literal and easy (6.1-6.4 order lists, 5.1 fixed lots, 6.5 precedence, 6.7 day shape).
  - The gap sits in per-hand scheduling (PASS 15.2 vs 0.9, WATER 49.9 vs 56.6), which a direct emitter must still route. MOVE is 31 % of PFS unit-actions.
- PFS already scores **0.934** in the same MMPQ seats. P48 scores 0.93 of MMPQ head-to-head (n 122). So the programme must beat 0.934 just to reach parity with PFS, and V56 reads 0/40 at 0.80.
- The 5 rules behind the 24k revenue gap:
  1. 2.14 wheat filler plus Q4 d10: wheat 592 vs 342 u, about -8k.
  2. 2.8/2.11 strawberry d6 wave (6 + 9.3 tiles per demand shop, just-in-time seeds): d15-17 50.0 vs 30.6 u, about -4k.
  3. 3.2/3.5 labour (h0 10-order fill, 12 hands, PASS ~0) plus 3.4 water: this drives turnover.
  4. 4.4 geese fill to about 22 animals plus 4.7 feed-on-eve: eggs 147 vs 92.5 u, about -2.7k.
  5. 2.12 tomato by demand-seq: d8-12 10.8 vs 6.8 tiles, (H) about -3..-5k.

## Q3: the frozen panel for 15:00Z (freeze at 08:00Z)
- **(a) V56 reacting.** vr.py seat 0 vs S/vband1/res/v56_ctl. Bars:
  - m40 W >= 37 and margin >= +6.9k (ctl 38, +7,862)
  - v21 W >= 12 (ctl 13)
  - d15-17 strawberry >= 47.5 (ctl 48.5)
  - d18-29 milk/wool/egg units >= ctl
- **(b) P48TAPE103.** Exact own-seat, 103 games, live W 28. Bars: dmargin t >= 2, net flips >= +1, zero wins lost beyond +1 gained, own >= 0.
- **(c) OTH own-seat tape** as a breakage guard (latch A fires on 36/58 OTH). This set is not built yet: 56 OTH games in games.json need an identity run.
- Pooled t >= 2 over (a) + (b) is required by the small-gains rule.
- **If nothing passes: upload nothing and keep 56687235 + 56687774 as the final pair.** Every read so far is under the bar or negative.

## Q4: ranked dispatches (remaining ~10 h)
1. **P48TAPE sweep (cheap, exact):** re-read every live candidate cell (STRAWDEMAND X3k/X5k, SPLITHEAD, PRICEDASK, TILELEASE, RIVALSUPPLY2, PACK22 options) on P48TAPE103 and build the OTH tape set.
   - Bar per cell: P48TAPE103 dmargin >= +1k, t >= 2, net flips >= +3, plus the V56 bars.
   - Cost: 14 min per cell on 1 process.
2. **Q4WHEAT exec (new executor, not the planner):** on d14, buy Q4 from idle cash (>= 4k + 1k reserve) and plant only wheat on Q4 tiles with +2 hands. The d0-13 PFS body stays untouched, so the d15-17 wall is intact by construction.
   - Bars: P48TAPE103 own >= +2k, t >= 2, flips >= +3; V56 m40 W >= 37, margin >= +6.9k.
   - Kill: Q4 wheat < 150 u or own < 0 at n 34.
   - Today's M says the planner route loses 5-8.5k, so only an isolated executor is worth 3 h.
3. **Programme line, research only:** PROGRAMME3R continues but is not a 15:00Z candidate unless fid20 ratio > 0.934 (PFS) and V56 m40 W >= 37. Rules 1-2 of Q2 come first.
