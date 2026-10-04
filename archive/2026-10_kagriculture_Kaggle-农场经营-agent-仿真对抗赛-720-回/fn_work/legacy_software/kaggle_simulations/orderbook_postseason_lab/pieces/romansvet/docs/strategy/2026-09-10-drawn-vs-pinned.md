# The today41 drawn win dip is a ceiling artefact on crippled tapes

*2026-09-09 — data agent. Files: `S/judge/flow166_g170_legs/today41_777001.csv` vs
`S/esf135c/cand_g350_today41_777001.csv` (41 tapes x 8 seeds x 2 seats = 656 rows, 328 boards);
pinned refs `S/lossflip/flow166_g170.csv` / `flow135_g350.csv` and the LIVE62 pair.
Working files in `S/drawncheck/` (`pertape.txt`, `ceiling.txt`, `tests.txt`, `pinned.txt`, `names.tsv`).*

## The read under test

flow166_g170 vs the g350 base on the drawn today41 leg:

* margin **+19 / game** (t 0.02, 328 boards, cluster-boot 95 % CI [-1,737, +1,831]) — dead level
* wins **294 -> 275 of 328** = **-5.8 pts**, cluster-boot 95 % CI [-11.0, -0.6], p(>=0) = 0.017
* board-level McNemar: 23 up / 42 down, exact two-sided **p = 0.025** (seat-level 46/84, p = 0.0011,
  but the two seats of a board agree on the winner in 98.5 % of boards, so seat rows are not
  independent; the board unit is the honest one)

So the dip is **not noise**: on this panel g170 really does win fewer boards.

## Where it lives: the base-100 % bucket, and nowhere else

Bucket the 41 tapes by the base theta's drawn win rate:

| base drawn win rate | tapes | boards | base w% | g170 w% | dwin | dmargin/board |
|---|---|---|---|---|---|---|
| 100 % | 20 | 160 | 100.0 | 85.0 | **-15.0** | **-2,530** (t -2.14) |
| 87.5 % | 14 | 112 | 87.5 | 87.5 | +0.0 | +2,338 (t +1.61) |
| 62.5-75 % | 6 | 48 | 66.7 | 72.9 | +6.2 | +1,227 |
| <=50 % | 1 | 8 | 50.0 | 75.0 | +25.0 | +11,290 |

Every one of the 19 net lost boards is in the 100 % bucket (-24 there, +5 in the two weak
buckets, 0 in the 87.5 % bucket). Per-tape corr(base win rate, dwin) = **-0.60**;
corr(dwin, dmargin) = +0.65.

The purse split is the two-purse redistribution signature, not a leak:

| bucket | d(own purse) | d(their purse) | d(margin) |
|---|---|---|---|
| base 100 % (n=160) | -462 | **+2,068** | -2,530 |
| base <100 % (n=168) | +600 | **-1,847** | +2,447 |

g170 denies less to tapes it already crushes and more to the tapes that actually threaten it.
Its own purse barely moves either way. Sum over the panel: zero.

## What "base wins 100 %" means on a drawn town

On this drawn panel the base theta wins **89.6 %** of boards. The same base theta on the pinned
panel wins **28.7 %** (45/157) and **30.6 %** on LIVE62 (19/62). The 100 %-bucket tapes are the
crippled end of the drawn-town artefact the tape-fidelity note describes: open-loop tapes replayed
on a *drawn* town lose their board and fold. A theta that beats a folded tape by 20 k instead of
23 k has told us nothing about Kaggle; a theta that beats it by -1 k instead of +1 k has told us
nothing either, and that is where all 24 down-flips sit (median |base margin| on flipped boards
5,783 vs 9,886 across the panel).

## The pinned tapes disagree, and they have no ceiling

Zero of the 41 today41 episode ids appear in any pinned set (drawn ids 1059-1060 xxxxx; pinned
1052-1071 xxxxx), and only two player names overlap, so there is **no per-tape drawn-vs-pinned
correlation to compute**. The two name matches are a wash (Hi Im Ryo +2,726, Brian Chua -348).

The panel-level pinned read answers the question anyway, because it can be split the same way:

| set | common | win | dmargin | flips |
|---|---|---|---|---|
| pinned 42+ | 157 | 45 -> 73 (**+17.8 pts**) | +3,786 (t 5.29) | 29 up / **1 down** |
| LIVE62 | 62 | 19 -> 30 (**+17.7 pts**) | +2,624 (t 4.21) | 12 up / **1 down** |

Split by whether the base won the pinned board:

* base **WON** (n=45): dmargin **+876**, g170 wins 44 of 45 — down-flip rate **2.2 %**
* base **LOST** (n=112): dmargin **+4,956**, g170 converts 29

The drawn 100 %-bucket down-flip rate is **15 %** (24/160). On pinned boards the base already
wins, g170 gives back essentially nothing. The regime where the drawn leg says g170 is worse is
the regime pinned says it is fine — and pinned is the population that decides the rating.

## Verdict

**(a) the drawn-town artefact, concentrated on crippled tapes.** The dip is statistically real on
the drawn panel (p = 0.025 clustered) but it is confined to the 20 tapes the base beats 8/8 on
drawn towns, it is a margin redistribution away from those tapes toward the contested ones, and
the pinned panel with the same theta shows the opposite on its own base-won boards (1 down-flip in
45). Two tapes carry a genuine within-tape signal (105958810 auhulu -14,810 t -3.50; 105975875
Borrun -6,848 t -3.13), balanced by five equally significant gains (105904738 +13,184 t 2.75,
105993413 +14,471 t 2.39, 105970534 +6,445 t 2.42, 105987532 +5,269 t 2.24, 105930341 +11,290 t
1.89). That is (b) at the tape level in both directions and (a) at the panel level. It is not (c).

## What the veto should do

**A drawn win-rate dip with a level margin must not veto, when the dip sits in the ceiling
bucket.** Concretely, for each drawn leg:

1. Compute the *base* theta's per-tape win rate on that leg. Tapes the base wins **8/8** are the
   crippled bucket; they carry no information about the live ladder (the base wins 90 % of drawn
   boards and 29 % of pinned ones).
2. Score the win-rate leg on the **contested** tapes only (base win rate < 100 %). On today41 that
   sub-leg is 21 tapes / 168 boards and reads **+3.0 pts** (+5 net wins) with **+2,447** margin —
   it does not veto.
3. Keep the full-panel *margin* floor as it is (no leg down by more than noise); margin is not
   ceiling-clipped, so it is the safe full-panel statistic.
4. When the contested sub-leg and the full leg disagree, the pinned/LIVE62 read breaks the tie. A
   drawn win dip that pinned does not reproduce on its own base-won boards is an artefact, and the
   calibration note (`docs/strategy/2026-09-09-kaggle-calibration.md`) already says drawn legs
   overstate the live win rate by ~34 pts and have twice manufactured t >= 4 with no Kaggle step.
