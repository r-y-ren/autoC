# PROGFIDELITY1 — seat-swap fidelity test of the ENGINE port (2026-09-23T04:41Z) — BROKEN

Branch `progfidelity1` (from engherd1 = master adc3a2ab tree). PROGRAM_ENGINE_ON ported from progeng4 8a17a06a (`git show 8a17a06a -- src tests | git apply --3way`, 1 conflict in plan.py: ENGHERD1 herd-defer block and program seed top-up kept in sequence). tests/test_program_engine.py pass. OFF parity: 3 boards, ledgers byte-identical to the unported tree.

**Leg** (S/progfidelity1/): `prep.py` takes the 59 FAITHFUL boards (engcontrast1 held and drift ≥ −8k) and cuts the OPPONENT seat (1 − eng_seat) from S/engtapes_0922 raw (TO.verify = 0 mismatches on 59/59). `run.py <arm>` puts the arm in the ENGINE's own seat against the recorded opponent (open loop), with exact seed and pinned town (engcheck towns.json). It hooks the engine (_commit_unit/_do_hire/_do_buy_land) for an executed ledger (money per step for both seats, market units at price, hires, land, executed plantings) in `ledger/<arm>/<ep>.json` (not committed, 29 MB). `report.py` → report.txt, purse_/cats_/diverge_<arm>.tsv. `cell.sh <arm>` runs it: 59 games ≈ 6 min at 6 workers.
**REAL** = the ENGINE's own tape in its seat: it reproduces the live purse on BOTH seats on **59/59 boards** (exact).

## Purse (ENGINE seat, mean over 59; curve = end of day)
| arm | final | % REAL (pooled / median) | ≥90 % boards | d1 | d5 | d10 | d15 | d20 | d25 | opp purse | W-L vs opp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REAL | 109,029 | 100 | — | 185 | 786 | 9,919 | 29,032 | 58,341 | 81,373 | 107,400 | 38-21 |
| IMIT@ENG | 95,892 | **88.0 / 84.8** | 22/59 | 333 | 593 | 14,905 | 22,050 | 48,827 | 72,460 | 119,410 (+12,010) | 5-54 |
| OURS@ENG | 109,256 | 100.2 / 93.8 | 38/59 | 168 | 1,040 | 2,738 | 13,720 | 52,424 | 81,087 | 100,875 (−6,525) | 15-44 |
The open-loop opponent tape collapses when the ENGINE seat plays differently. Opp purse falls more than 8k on 4 IMIT boards and 17 OURS boards, and those boards inflate the means. **On the boards where the opponent does not collapse:** IMIT (n = 55) Δpurse −15,648 (median −15,355), Δopp +17,304, 1 win vs REAL's 36. OURS (n = 42) Δpurse **−9,096** (median −8,908), Δopp +5,527, 2 wins vs REAL's 26.

## First divergence (> 500 coins vs REAL, ENGINE seat)
| arm | day histogram | top cause on that day (boards) |
|---|---|---|
| IMIT | d2 9, d3 16, d4 18, d5 1, d6 11, d8 4 | BUY_ANIMAL:COW 31, BUY_PRODUCT:WHEAT (feed) 20, other 8 |
| OURS | d2 32, d3 1, d4 20, d5-7 6 | BUY_PRODUCT:WHEAT 26, PLANT:MELON 16 (no d0 plate), SELL:WHEAT 12 |
IMIT's melon opening is FAITHFUL: 11.0 melon seeds on d0-1 vs REAL 9.4, and 11.8 melon plantings vs 12.9. The port breaks after the opening, in the herd, the feed and seed-to-plant execution.

## Top-5 IMIT fidelity defects (coin/board, IMIT − REAL, whole game)
1. **STRAWBERRY d20-29 sales −5,740** (97.8 vs 130.0 u). Strawberry plantings d10-19 are 4.1 vs 7.9 on the same seed buys (29.5 vs 30.0).
2. **WOOL d10-19 −5,308** (35 vs 60 u). The herd is short: sheep 5.1 vs 7.6. IMIT buys 1.0 sheep d2-9 vs 3.2, and cows d0-1 1.0 vs 2.4. The first divergence is the d2-4 cow buy on 31/59 boards.
3. **Stranded seed, CARROT −3,308 + TOMATO −3,393 (d20-29 sales).** Seeds are bought at parity (carrot 43.9 vs 43.5, tomato 11.0 vs 12.3), but IMIT plants only 24.0 carrot vs 43.1 and 6.7 tomato vs 12.0. It buys the seed and never plants it (carrot d20-29 14.3 vs 32.7).
4. **FERTILIZER loop −3.3k:** it sells 58.7 vs 106 u d10-19 (−1,861) and buys 24.7 vs 4.2 u d10-19 (−1,467). IMIT BUYS the fertilizer the ENGINE SELLS.
5. **Feed wheat and early wheat −1.5k direct, with knock-on losses:** BUY_PRODUCT:WHEAT 95 vs 168 u, wheat plantings d2-9 11 vs 25, hires d0-1 4.4 vs 7.3. Milk d2-9 is −1,510, which points to an underfed herd.
Offset: MILK d20-29 **+6,346** (110 vs 88 u; cows 8.5 vs 8.2 bought later). **IMIT gifts the opponent +12k** because it sells into their late books.

## OURS@ENG vs REAL (program gap, same seat and board)
On the 42 boards where the opponent does not collapse, our tree earns −9.1k in the ENGINE's seat. The gap is the known one (per-category figures over all 59 boards). Melon d10-19 is −11,162 (12 vs 65 u; 0 melon on d0-1 vs 9.4), recovered as +10,195 of late melon. Wheat is −6.7k (planted 99 vs 146; seed d10-29 68 vs 111). Wool d2-9 is −3,208 and tomato d20-29 −3,015, offset by wool d20-29 +6,252 and strawberry d10-19 +4,967. We skip the fertilizer buy (2.9 vs 26.6 u), hire 256 vs 278 and plant tomato 4.8 vs 12.

## Verdict: BROKEN (IMIT 88 % pooled, 84.8 % median, 22/59 ≥ 90 %; non-collapse −15.6k)
The program itself was never judged: the port loses 12-15k to the ENGINE's own tape in the ENGINE's own seat, and the loss starts d2-4. **Work list, in coin order:** (1) seed-to-plant execution: plant every bought carrot, tomato and strawberry seed (≈ −12k of d20-29 crop sales); (2) herd: match the d0-1 cows (2.4) and d2-9 sheep (3.2) and geese (2.2) buys; (3) fertilizer: sell the d10-19 surplus, do not buy it back; (4) feed-wheat buys (168 u) and d2-9 wheat plantings (25). Re-run `cell.sh IMIT` after each fix; the gate is ≥ 90 % of REAL on the non-collapse boards, and only then judge the program on the band legs.
