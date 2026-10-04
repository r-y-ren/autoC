# flow172_g300 — anatomy on the 55 held-out LIVE boards

2026-09-10. Engine CSVs are the verdict, sim descriptive (110 board-seats). Tooling
`S/g300live/*.py`, forks of `S/g170clive/*`. The theta (md5 ee2874e7) was logged *g260*, so
`flow172_g260_{live62,loss20}.csv` are g300's; `_pair` = `TAIL_FILL_ON`+`BANK_BEFORE_LOT_ON`.
|g300−g170c| 2.61, cos 0.07 to the g170c step: orthogonal again.

## 0. Engine

| theta | margin | win | ours | theirs |
|---|---|---|---|---|
| init (LIVE g350) | −286 | 34.5 % | 100,792 | 101,077 |
| g60 | +4,306 | 58.2 % | 104,164 | 99,858 |
| g170c | +5,248 | 65.5 % | 104,125 | 98,877 |
| **g300** | **+5,681** | **69.1 %** | 104,437 | 98,755 |
| g170c_pair | +6,027 | 66.4 % | 104,766 | 98,739 |
| **g300_pair** | **+6,211** | **70.9 %** | 104,788 | 98,577 |

The step over g170c is under the LIVE55 noise floor (+229 t 0.64; pair +174 t 0.56), positive
on all four judges:

| judge | g170c_pair | g300_pair |
|---|---|---|
| LIVE55 (53) | +6,579 t 10.15 / 66.4 % | **+6,753 t 9.95 / 70.9 %** |
| LIVE-B (17) | +7,417 / 70.6 % | **+8,119 / 76.5 %** (t 2.58) |
| TOPB (20) | +3,174 t 1.92 | **+3,730 t 2.12** |
| LOSS20, raw | −1,742 / 35 % | −910 / 40 % |

## 1. Fidelity

Sim +5,762 / 69.1 % vs engine +5,681 / 69.1 %: mean |Δ| **200** (g170c 171), median 40, **W/L
agreement 100 %**, corr 0.999. Delta g300−g170c sim +409 vs engine +433, corr **0.983**.

## 2. Two-purse — back to growth

`g300 − g170c`, 110 seats: **+433 = +312 ours / −121 theirs**, spent where we lose — win boards
(38) −406, loss boards (72) **+876**. g170c's step was pure denial (−39/−981); this one is our
purse. Pair-to-pair that half is already banked, leaving +184 = +22/−161.

**TOPB — §61's defect survives.** vs init the lineage still *hands* the top tier money: theirs
+1,092 (g60) → +974 (g170c) → **+921 (g300)** → +689 (g300_pair), while taking 2.3–2.5 k off
the band. g300−g170c there = +474 = +420/−53, 11/20 boards up (107250536 +9,911, 107246551
−5,142); the 35→30 % win count is two near-ties.

## 3. What moved — nothing structural, again

d0 basket, pump 53, quads and HIRE d0–d3 identical; d4 4.20→4.31, season 274.8→276.9; tiles by
d10 move ≤0.5. Units 1,386→1,405, **price/unit 92.80→91.92** — g170c's cheaper-basket lever
again. SELL rows 140.2→143.1, all late (h18 +2.3, h10 +1.8, h1 −0.8). Intent **EGG +16.3
u/+848**, FERTILIZER +383, CARROT −263, WOOL −233, MELON −166; opponent units/rows unchanged
(1,550/250), revenue 126,282→126,095.

## 4. Day band — d10–14 still did not move

`g300−g170c` opens d0–9 +2, **d10–14 +45**, **d15–19 +359**, d20–24 +48, d25–29 −45: one band,
own-purse. Against the live theta d10–14 is still **−1,221** (g170c −1,266, g60 −1,492) — the
melon-pot hole of `2026-09-10-residual-loss20.md`, untouched by three generations.

## 5. Drops and tail — the doubled tail closed

107117102 stays the only W→L board vs init (+287 → −4,629 → **−4,780**; pair −1,948); 40 flips,
2 drops. **107088554 is half-repaired**, −19,595 → **−9,809** (ours +5,712 / theirs −4,074).
Worst-5 vs init **−21,627** (g170c −36,470, g60 −22,585); 15 negative boards at mean −2,069 vs
g170c's 12 at −4,378 — more losers, each half as deep. Pair vs init: deepest −2,235, mean
−1,408 (g170c_pair −4,035/−1,926). g170c's tail is undone; the new holes sit inside boards
already won (106962018 −9,091, still +46,535). Drops vs g170c: 107067869 (+1,346 → −3,352,
**opponent purse +3,730**), 107089992 (+930 → −1,956).

## 6. LOSS20 — it wins the coin flips, not the deep boards

init −7,563/0 % → g170c −1,742/35 % → **g300 −910/40 %**; step +832 t 1.15 = +421/−411. g300
flips **8**: keeps 6 of g170c's 7, adds three, gives back two.

| group | n | base | g170c | g300 |
|---|---|---|---|---|
| extra: 107081922/107092814/107140814 | 3 | −7,992 | −1,676 | **+1,083** |
| given back: 107067869/107089992 | 2 | −5,823 | +1,138 | −2,654 |
| held by both | 5 | −1,516 | +7,522 | +7,765 |
| never flipped | 10 | −10,806 | −6,969 | −5,496 |

Every board changing hands sat inside |2,100| under g170c (five of the six there); the 5 held by
>2 k stay won, the 9 lost by >3.2 k stay lost. All five are LIVE55 flips/drops too.

## 7. Verdict — **ship `g300_pair`**

Best or tied-best on every judge, and unlike g170c it does not buy win rate with a tail: the
deepest regression vs init falls 4,035 → 2,235. Prefer `g170c_pair` only if LIVE55's t 0.56 is
decisive — it should not be, with four judges agreeing in sign and the tail running the same
way. `g60_pair` is off the table (+4,306, 58.2 %). Caution unchanged: the lineage still adds
~0.7–0.9 k to the top tier's purse, so LIVE55 stays ~2x optimistic vs a 2,900 field.

## Not measured

Per-product opponent revenue; why 106962018 gives back 9.1 k on a board it wins by 46 k; one
seed per board; the denial half is unproven against an adaptive (non-tape) seat.
