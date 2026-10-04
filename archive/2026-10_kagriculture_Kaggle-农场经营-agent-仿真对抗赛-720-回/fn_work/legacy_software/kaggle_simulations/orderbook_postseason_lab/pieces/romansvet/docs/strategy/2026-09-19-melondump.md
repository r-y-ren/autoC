# MELONDUMP — the −20,162 melon cell is an ARRIVAL gap, not a floor dump

2026-09-19, local, `master`. `S/melondump/{probe,report,cf}.py`: the full SELL/BUY order tape of
both seats with **the market book before every commit**, plus the dawn shed, on the ENGTAIL
instrument (ship7692 theta, WINJUDGE ESR string, HIBAND seeds, `town_hiband.json`). All 10 hiband
loss boards, seat 0, margins reproduce the leg to the coin (`−19,439 / −17,475 / −10,560 / …`) and
the melon PRICE cells reproduce ENGTAIL (`−20,162 / −9,738 / −9,048 / −5,270`).

## 0. VERDICT — we never dump first, and the book never comes back
`MELON` is `base 250, I0 10,000, T 300, above sq 3.6`: **158 units over I0 is `PRICE_FLOOR` 1**.
Nothing refills it (`NEXTMECH` LAW; the only decrements are 1-2 u/day of town buy-back, largest
one-day quote recovery observed **6 coins**). So the melon quote is a one-way ratchet and sale
*timing* cannot buy a coin — melon revenue is a path integral down one shared curve.

## 1. (1) THEIR dump precedes ours, wholesale — `110504774`
| d | 10 | 11 | 12 | 13 | 14 | 16 | 17 | 18 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **they sell** | 12 | 6 | 36 | 24 | 24 | 6 | 21 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **we sell** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 6 | 12 | 6 | 6 | 18 | 12 |
| dawn quote | 271 | 250 | 250 | 233 | 209 | 176 | 167 | 127 | **89** | 43 | 28 | **1** | 1 | 1 | 1 |

147 of their units walk the book from I0−11 to **I0+127 before our first melon unit exists**. Our
78 units then arrive into a quote of 89 and finish it. Pooled over 10 boards the melon sell-day
centroid is **us d23.0 vs them d11.3, +11.7 days late**; their realised price is 236-244.5/u on
8 of 10 boards. This is MELONRACE/MELONGIFT first-mover rent at its limit, not a sale defect.

## 2. (2) The hold counterfactual is NEGATIVE — priced on the recorded book
`110504774`: **65 of our 78 units cleared below 60/u for 718 coins**. The same units at the
*recorded* book of d+1 = **437 (−281)**, d+2 = **236 (−482)**. Across the 10 boards 100 units
cleared below 60 and the d+1 book is **at or below the realised price on 96 % of them**; pooled
hold value **−65/board (d+1), −87 (d+2)**. Holding a melon unit destroys it.

## 3. (3) The whole tail, and the unreachable oracle (`cf.py`)
8 of 10 hiband losses carry a melon price gap > 5k: `110504774` −20,162 · `110516257` −9,738 ·
`110556781` −9,048 · `110476108` −6,344 · `110491183` −5,701 · `110523904` −5,516 · `110485947`
−5,270 · `110571826` −5,196 (below the bar: `110540008` −4,593, `110460827` −3,465).
**ASAP** (our whole melon line sold on our first melon day, ahead of every later order of theirs)
reads ours **+418** / theirs **−1,074** = +1,492 margin a board, all of it on the two boards where
their tape still overlaps ours (`110556781` +7,087/−8,509, `110516257` +917/−2,233). **Unreachable:
our dawn melon shed EQUALS that day's melon sells on 60/60 board-days** — we already carry zero
melon overnight and sell at the first dawn lot (turn 1) on every board. The ASAP units do not
exist; it is the PLANSELECT/SELLDAY oracle shape again.

## 4. (4) The withhold mechanism exists, and the tape rejects it before a judge
`_sell_hold` (`plan.py:6317`) raises the per-product `hold` reservation to a price floor off the
terminal day; its two instantiations are `FERT_FLOOR_ON` (5882) and `CARROT_EARLY_HOLD_ON` (6017),
and `macro.hold` is the trained per-product reservation [SELLDAY §3]. No melon instantiation
exists; one is 4 lines. **Not flown**: a floor can only *withhold*, withheld melon is never sold
(§0, the book is a ratchet), an unsold unit is worth 0, and the un-depressed quote is handed to
their line [MELONGIFT]. `CARROT_EARLY_HOLD` measured exactly this and lost 8k. Spec, for the
record — `_sell_hold`, `if MELON_FLOOR_ON: gated = where(j == I_MELON, maximum(gated,
price_table[I_MELON, _I0_COL] * NUM // DEN), gated)`, `MELON_FLOOR_ON = False` (= today).

**MELON SALE-SIDE CLOSED at this band.** The cell is arrival: their melon is sold by d11-18, ours
ripens from d20. Everything reachable lives in the ENGTAIL volume half (roster and ASK), not here.

Repro: `bash S/melondump/run_all.sh` (10 boards, 20 s each), `report.py [--days] [ep]`, `cf.py`.
`raw/` gitignored.
