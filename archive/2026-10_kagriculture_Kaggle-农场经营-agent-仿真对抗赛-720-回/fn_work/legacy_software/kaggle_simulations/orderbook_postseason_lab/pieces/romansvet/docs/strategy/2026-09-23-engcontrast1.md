# ENGCONTRAST1 — "crushing" vs "beaten" ENGINE subs (2026-09-23T01:40Z) — NO EXPLOITABLE PATTERN

Branch `engcontrast1` (from drydeath1 = master d34b04fc tree). Read-only analysis of the arm-B ENGINE leg (S/engcheck replays_B, games_B.tsv, selection.tsv, towns.json). Scripts `S/engcontrast1/{boards.py,summary.py,town.py}` → `boards.tsv` (per board per seat), `sales.tsv` (every SELL: day/hour/units/book price), `summary.txt` (held-73), `summary_faithful.txt`, `town.txt`.
C = crushers (ymg_aq, THIRD FARM, Kaggledew, KawattaTaido, mtmr_s1); B = beaten (MMPQ, Vadim, DSM, Majkel).

## 1. The per-sub split is a tape-fidelity artefact (the tape collapses), not a program difference
The Q3 "held" filter lets through collapsed tapes. Per-board drift is the tape seat's score minus the sub's live score.
**B wins 29/40. 26 of those 29 come from tapes that collapsed or drifted** (drift ≤ −8.5k; MMPQ drifts −55k/−65k/−53k/−46k on its "held" wins). C wins 6/50, of which 1 is on a drifted tape.
FAITHFUL = held AND drift ≥ −8,000 → 59 boards:
| set | n | W-L | theirs | ours | margin | their LIVE score | live W | drift |
|---|---|---|---|---|---|---|---|---|
| C held | 49 | 5-44 | 110,628 | 100,141 | −10,487 | 109,953 | 32 | +675 |
| B held | 24 | 13-11 | 100,597 | 119,343 | +18,746 | 113,119 | 17 | **−12,522** |
| C faithful | 46 | 5-41 | 110,880 | 100,405 | −10,475 | 109,516 | 30 | +1,364 |
| B faithful | 13 | 3-10 | 111,520 | 105,135 | −6,385 | 107,305 | 8 | +4,215 |
Faithful C−B: theirs **−640 t −0.11** (the crushers do NOT earn more). Ours −4,731 t −0.68. Margin −4,090 t −1.22. Wins 5/46 vs 3/13, Fisher p = 0.24. Their live strength is equal (+2,210 t 0.44; live win rate 65 % vs 62 %). **Every ENGINE sub beats us ~80-90 % on a faithful tape.** The "8-2" subs are open-loop collapses.

## 2. Production, faithful, per board (theirs C / B)
| item | C | B | item | C | B |
|---|---|---|---|---|---|
| wheat tiles d10-19 / d20-29 | 16.3 / 22.0 | 21.8 / 23.8 | melon plants (first day median) | 13.1 (d0) | 10.6 (d0) |
| strawberry tiles d10-19 / d20-29 | 27.8 / 12.2 | 21.5 / 7.7 | melon sold d10-19 / d20-29 | 66 / 12 | 56 / 6 |
| tomato tiles d20-29 | 6.7 | 9.4 | hires / idle hand-turns | 275 / 499 | 288 / 374 |
| cows / sheep / geese | 7.8 / 7.7 / 3.5 | 9.4 / 6.8 / 7.1 | fert harvested / applied / bought | 393 / 195 / 32 | 429 / 201 / 7 |
| wool sold d10-19 / d20-29 | 62 / 76 | 48 / 59 | egg sold d20-29 | 72 | 116 |
Revenue C−B: theirs −1,828 (price −7,005, volume +5,177). Ours −6,116 (price −4,683, volume −1,433): milk d10-19 −3,619, tomato d20-29 −3,603, strawberry +3,359. The crushers lean toward strawberry, wool and melon, the beaten subs toward wheat, tomato and eggs. The totals are equal. These are two fertilizer-ENGINE variants with the same purse, not a stronger class.

## 3. Our purse residual is TOWN DRAW
Our realised d10-29 price tracks shop coverage (shops open by d19 that buy the product). The correlation is 0.85 for milk, 0.87 for strawberry, 0.89 for wool and 0.71 for tomato. Faithful B boards drew more milk shops (2.23 vs 1.93) and more tomato shops (1.92 vs 1.52). Our tree already responds to this: we plant tomato at 7.1 vs 3.2 tiles d20-29 on B boards. The −4.7k is board draw at n = 13, and it is not significant.

## 4. Timing: crushers sell earlier in the day, and it costs us nothing
Units-weighted sale hour, d20-29, theirs C / theirs B / ours: wheat 6.2/9.6/5-6, egg 7.1/15.4/4-8, milk 9.5/12.0/15-16, fertilizer 4.9/9.6/3.2. Crushers dump 2-8 h earlier than B subs, a real and consistent program trait. It does not hurt us:
- On C boards, 49 % of our d10-29 units follow a same-day same-product crusher sale at an earlier hour (55 % on B).
- The book moves by **−65 coin/board** from their first sale to our sale on C boards. On B boards it is −1,200/board. Negative means our price is higher at our sale, because the book recovers.
There is no pre-emption rent to dodge. SELL_SPREAD/SLOTLOCK/SELLDAY stay closed.

## Levers (post-d2-classifier, deterministic, non-gift)
**None.** The crusher/beaten split is not a program difference we could respond to:
1. Most of the W-L split comes from tape collapse (26/29 B wins).
2. On faithful boards the purses are equal (theirs −640 t −0.1).
3. Our residual follows town shop coverage.
4. Crushers' earlier sale hours cost us ≤ 65 coin/board, so the timing ceiling is ≈ 0.
The crushers simply out-produce us exactly as the beaten subs do: the pooled d10-19 volume gap from ENGCHECK.
**Instrumentation fix:** judge ENGINE legs on FAITHFUL (held AND drift ≥ −8k, 59 boards; our tree 8-51), not held-73. Per-sub W-L on the ENGINE leg must not be read as sub strength.
