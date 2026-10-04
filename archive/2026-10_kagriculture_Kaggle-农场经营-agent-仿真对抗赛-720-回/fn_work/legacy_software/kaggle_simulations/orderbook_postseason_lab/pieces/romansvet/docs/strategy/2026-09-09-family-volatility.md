# 2026-09-09 — Leg-family volatility: is the 10-tape gate refusing on noise?

Measure-only. Source: `~/stage_leg20/artifacts/flow166/real_gate.log` and
`.../flow167/real_gate.log` (copies + parser in
`S/famvol/{f166,f167}_real_gate.log`, `parse.py`, `analyse.py`, `extra.py`).
`real_gate.csv` holds only the LAST round's 96 rows — the per-round history is in the
`.log`, where each gate round is a `(record|periodic)` block (candidate) followed by an
`(incumbent)` block, then the `--- leg20:` verdict line. The parser reproduces every logged
`leg delta` and `all-games delta` exactly (±1 rounding), so the reconstruction is verified.

16 paired gate rounds today: flow166 g10/20/30/50/70/80/100/110/130/150/170/200,
flow167 g10/60/100/150. Seats are identical on pinned towns, so "20 games" = 10 boards and
the logged `leg delta` = 2 x (sum of the 10 per-tape mean-margin deltas).

## 1. Per-tape margin delta per round (per-game coins, candidate - incumbent)

| round | 228357 | 232167 | 268279 | 269242 | 400600 | 441481 | 441843 | 442685 | 443859 | 592028 | SUM x2 | ALL x2 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 166 g10 | −3,559 | 1,850 | 818 | 2,558 | 1,674 | −4,434 | −1,458 | −5,515 | 181 | 1,485 | −12,800 | −47,716 | refuse |
| 166 g20 | −7,040 | 1,413 | −2,094 | 784 | 1,846 | −3,579 | −2,613 | −5,408 | −4,261 | 2,443 | −37,018 | −39,512 | refuse |
| 166 g30 | −7,599 | 2,092 | 337 | 2,117 | 154 | −1,458 | −1,840 | −3,097 | −4,432 | 5,068 | −17,316 | +5,104 | refuse |
| 166 g50 | −3,031 | 3,734 | 5,842 | 984 | 4,174 | −1,051 | −188 | −4,053 | −6,705 | 2,324 | **+4,060** | +70,374 | ACCEPT |
| 166 g70 | 463 | −536 | −4,218 | −1,134 | −7,116 | 2,596 | −1,203 | 6,624 | 569 | −1,424 | −10,758 | +16,604 | refuse |
| 166 g80 | 2,470 | −932 | −3,656 | 1,426 | −817 | 3,295 | −1,052 | 4,034 | 239 | −463 | **+9,088** | +41,700 | ACCEPT |
| 166 g100 | −7,960 | −241 | −1,413 | −6,993 | 533 | 22 | −581 | 2,871 | 273 | −1,196 | −29,370 | −9,624 | refuse |
| 166 g110 | −5,032 | 1,070 | −469 | 383 | −1,396 | 928 | −742 | 4,996 | 973 | −942 | −462 | +50,552 | refuse |
| 166 g130 | −6,632 | −1,494 | −596 | 224 | −1,374 | −1,582 | −830 | 4,259 | 3,404 | −808 | −10,858 | +108,354 | refuse |
| 166 g150 | −6,454 | −417 | 1,067 | 160 | −1,536 | −4,510 | 1,095 | 6,838 | 4,146 | 1,826 | **+4,430** | +171,170 | ACCEPT |
| 166 g170 | 879 | 1,184 | 268 | 987 | 1,936 | −1,627 | 508 | 401 | 2,323 | −975 | **+11,768** | +16,430 | ACCEPT |
| 166 g200 | −544 | −505 | 1,068 | −7,699 | −3,448 | 809 | −1,880 | −3,333 | −4,059 | −375 | −39,932 | −9,482 | refuse |
| 167 g10 | −5,923 | 472 | 1,980 | −870 | 4,277 | −970 | 1,884 | −4,126 | −1,634 | 3,239 | −3,342 | +43,264 | refuse |
| 167 g60 | −1,002 | 1,779 | −175 | 474 | −1,060 | 3,855 | −1,121 | 2,381 | −4,010 | 982 | **+4,206** | +169,472 | ACCEPT |
| 167 g100 | −6,497 | −2,120 | 96 | −5,764 | 627 | −1,686 | 488 | −499 | −3,547 | 2,556 | −32,692 | +24,112 | refuse |
| 167 g150 | −2,017 | −1,905 | 413 | −1,686 | −999 | −641 | −1,051 | −5,822 | −5,889 | 2,058 | −35,078 | +40,800 | refuse |

## 2. Per-tape volatility (16 rounds, gate units = x2 the per-game delta)

| tape | mean | sd | range | neg rounds | sign disagrees with other-9 mean | share of \|delta\| |
|---|---|---|---|---|---|---|
| 105228357 | **−7,435** | 6,560 | 20,860 | **13/16** | 7/16 (44 %) | **18.1 %** |
| 105442685 | +69 | **8,832** | **25,320** | 8/16 | 8/16 (50 %) | **17.3 %** |
| 105443859 | −2,804 | 6,508 | 21,702 | 8/16 | 8/16 (50 %) | 12.6 % |
| 105269242 | −1,756 | 6,124 | 20,514 | 6/16 | 5/16 (31 %) | 9.2 % |
| 105400600 | −316 | 5,420 | 22,786 | 8/16 | **12/16 (75 %)** | 8.9 % |
| 105441481 | −1,254 | 4,824 | 16,730 | 10/16 | 8/16 (50 %) | 8.9 % |
| 105268279 | −92 | 4,457 | 20,120 | 7/16 | 10/16 (62 %) | 6.6 % |
| 105592028 | +1,975 | 3,726 | 12,984 | 7/16 | 10/16 (62 %) | 7.6 % |
| 105232167 | +680 | 3,155 | 11,708 | 8/16 | 8/16 (50 %) | 5.9 % |
| 105441843 | −1,323 | 2,272 | 8,994 | 12/16 | 6/16 (38 %) | 5.0 % |

**Volatile by the sd >= 5k bar (gate units):** `105442685`, `105228357`, `105443859`,
`105269242`, `105400600`. By the >=50 % sign-disagreement bar, 7 of 10 qualify — the bar is
useless here because the other-nine mean is itself near zero, which is the real finding:
**within a round, per-tape deltas have sd ~3,006 coins/game, so the SE of the 20-game leg sum
is ~17.7k coins.** Every accept today read +4,060…+11,768 — that is **0.2–0.7 SE**. The
`leg delta > 0` test is a coin flip at this sample size.

Two distinct pathologies, not one:
* `105442685` is the **noise carrier** — mean +69, sd 8,832, range 25.3k, 17.3 % of all
  movement. It contributes nothing on average and dominates the variance (matches the g50/g150
  anatomies' ±11k swing).
* `105228357` is a **systematic drag** — negative in 13/16 rounds, mean −7,435, and 18.1 % of
  all movement. It is not volatile so much as permanently opposed: whatever both arms are
  learning, this one board hates it.

## 3. Re-verdict with volatile tapes removed / median instead of sum

Rule kept as `stat > 0 AND all-96 delta >= 0`. `*` = refuse→ACCEPT, `!` = ACCEPT→refuse.

| round | sum10 | median | −232167 | −268279 | −400600 | −441481 | −442685 | −443859 | −592028 | −all 5 vol | trimmed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 166 g10/20/30/100/200, 167 g100/150 | ref | ref | ref | ref | ref | ref | ref | ref | ref | ref | ref |
| 166 g50 | ACC | ACC | ref ! | ref ! | ref ! | ACC | ACC | ACC | ref ! | ref ! | ACC |
| 166 g70 | ref | ref | ref | ref | **ACC \*** | ref | ref | ref | ref | ref | ref |
| 166 g80 | ACC | ref ! | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC |
| 166 g110 | ref | ref | ref | **ACC \*** | **ACC \*** | ref | ref | ref | **ACC \*** | ref | ref |
| 166 g130 | ref | ref | ref | ref | ref | ref | ref | ref | ref | ref | ref |
| 166 g150 | ACC | ACC | ACC | ACC | ACC | ACC | ref ! | ref ! | ACC | ref ! | ACC |
| 166 g170 | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC | ACC |
| 167 g10 | ref | ref | ref | ref | ref | ref | **ACC \*** | ref | ref | ref | ref |
| 167 g60 | ACC | ACC | ACC | ACC | ACC | ref ! | ref ! | ACC | ACC | ref ! | ACC |

**No refusal is rescued by dropping the volatile tapes, by the median, or by the trimmed sum.**
The only refusals a single deletion flips are the marginal ones (g110 at −462, g70, 167 g10) and
each needs a *different* tape deleted. Meanwhile **4 of the 5 accepts break** under some single
deletion (only 166 g170 survives every variant), and dropping all five volatile tapes turns
g50, g150 and 167 g60 into refusals. Removing volatility does not make the family decide better;
it makes it decide differently, at random.

The three headline refusals are **broad, not carried by one board**: 166 g130 is negative on
7/10 tapes, 167 g100 on 6/10, 167 g150 on 8/10. The family genuinely dislikes them.

## 4. Which family statistic predicts the fresh-loss (LOSS12) engine reads?

LOSS12 = 12 never-trained Kaggle-loss tapes, 24 games, base = live `flow135_g350`.

| candidate | LOSS12 /game | sum10 | median10 | trimmed | excl. 5 volatile | excl. 442685 | all-96 |
|---|---|---|---|---|---|---|---|
| 166 g50 | +722 | +2,030 | +398 | +2,893 | −2,235 | +6,083 | +70,374 |
| 166 g80 | −509 | +4,544 | −112 | +4,166 | +2,844 | +510 | +41,700 |
| 166 g130 | +1,381 | −5,429 | −819 | −3,056 | −7,238 | −9,688 | +108,354 |
| 166 g150 | +1,879 | +2,215 | +614 | +1,831 | −5,199 | −4,623 | +171,170 |
| 166 g170 | +2,467 | +5,884 | +694 | +5,188 | +2,374 | +5,483 | +16,430 |
| 167 g60 | +676 | +2,103 | +150 | +2,258 | −1,649 | −278 | +169,472 |
| 167 g150 | +2,555 | −17,539 | −1,368 | −13,708 | −4,754 | −11,717 | +40,800 |

Spearman vs LOSS12, n=7 (incremental framing, i.e. what the gate actually reads):

| statistic | rho |
|---|---|
| median of 10 | **+0.04** |
| sum of 10 (the gate) | −0.25 |
| all-96 delta | −0.36 |
| trimmed sum (drop hi+lo) | −0.39 |
| sum excl. 5 volatile | −0.43 |
| sum excl. 105442685 | −0.43 |

Cumulative framing (candidate minus the gen-0 init, matching LOSS12's fixed base) gives the same
picture: sum10 −0.11, median +0.04, trimmed −0.11, excl-volatile −0.64.

**Every family statistic is <= 0 except the median, which is zero.** Trimming or deleting the
volatile tapes makes the ordering *worse*, not better. The critical |rho| at n=7, p=0.05 is
0.786, so nothing here is significant — but the family carries no positive information about
fresh-board generalisation in either direction of framing, while the two candidates the family
refused most emphatically (166 g130, 167 g150) are the two best on fresh boards.

Per-tape rho vs LOSS12 (cumulative) for interest: only `105592028` (+0.71) and `105442685`
(+0.29) lean positive; `105228357` is the most anti-predictive (−0.50) — the same board that
supplies the systematic drag.

## 5. Recommendation

**Replace the held-out gate set with the 12 fresh loss tapes (the flow168 design already on the
remote). Do not patch the 10-tape family.**

1. The family test has no power: SE of the leg sum ~17.7k, every accept 0.2–0.7 SE. It is not
   selecting candidates, it is sampling them.
2. Its failures are not a volatility artefact. Dropping the volatile boards, the median and the
   trimmed sum all leave the headline refusals refused, and each breaks accepts instead.
3. It does not track the only never-trained engine read we have: rho <= 0 for every variant.
4. If flow168's LOSS12 gate is delayed and the family must keep running, the least-bad patch is
   to **drop `105228357`** (negative in 13/16 rounds, 18 % of movement, rho −0.50 vs LOSS12 —
   it is a single board voting against both arms) and to **stop treating the family as a veto**:
   accept when `leg delta > -1 SE` and the all-96 delta is clearly positive, i.e. demote it from
   gate to screen, exactly as `net flips` already is.

**Caveat: n = 7 for the Spearman and 16 for the per-tape stats, from two arms of one day, with
correlated rounds (consecutive candidates share an incumbent).** The p-values are worthless; the
SE calculation in §2 is the load-bearing number and it does not depend on n=7. Treat §4 as
"the family fails to predict", not "the family predicts the opposite".
