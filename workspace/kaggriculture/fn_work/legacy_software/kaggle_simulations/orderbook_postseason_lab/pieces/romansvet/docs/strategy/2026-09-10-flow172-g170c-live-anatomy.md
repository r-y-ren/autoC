# flow172_g170c — anatomy on the 55 held-out LIVE boards

2026-09-09. Engine CSVs are the verdict, sim descriptive (110 board-seats). Tooling
`S/g170clive/*.py`, verbatim forks of `S/g172live/*`. Predecessor:
`2026-09-10-flow172-g60-live-anatomy.md`. |g170c−g60| 2.38, orthogonal to every earlier
step (cos 0.045).

## 0. Engine

| theta | margin | win | ours | theirs |
|---|---|---|---|---|
| init (LIVE) | −286 | 34.5 % | 100,792 | 101,077 |
| g60 | +4,306 | 58.2 % | 104,164 | 99,858 |
| **g170c** | **+5,248** | **65.5 %** | 104,125 | **98,877** |

| pair | d-margin | t | dOURS | dTHEIRS | flips/drops |
|---|---|---|---|---|---|
| g170c−init | +5,534 | 10.9 | +3,333 | −2,201 | +36 / −2 |
| g60−init | +4,592 | 11.0 | +3,372 | −1,220 | +28 / −2 |
| **g170c−g60** | **+942** | **3.5** | **−39** | **−981** | +8 / 0 |

## 1. Fidelity — still a valid judge

g170c sim +5,353 / 65.5 % vs engine +5,248 / 65.5 %: mean |d| **171** (g60 154, init 283),
median 51, **W/L agreement 100 %**, corr **1.000**; own purse mean |d| 79. Delta g170c−g60
sim +959 vs engine +942, corr 0.994. Fidelity is g60-grade.

## 2. Two-purse — the new step is pure denial

g170c−g60, all 110: **+942 = −39 ours / −981 theirs**. Win boards (38) +1,024 = +177 / −847;
loss boards (72) +899 = −153 / −1,052; the 8 extra flips +3,519 = +1,286 / −2,229. Our purse is
flat (up on 60/110), theirs falls on 79/110. g60 over the live theta was 73 % growth; g170c
adds only denial on top of it.

## 3. What moved

Nothing structural: d0 basket identical (GOOSE 1 / COW 4 / SHEEP 1, WHEAT 9 / CARROT 10 seed),
pump 53, quads 3; HIRE d0–d3 identical, d4 4.00→4.20, season 272.8→274.8; d10 tiles move ≤0.5.
Execution runs *against* g60's lever: units 1,375→1,386, revenue 128,552→128,614,
**price/unit 93.47→92.80**, h1 99.4→97.8, h18 38.0→38.7. Ordered intent WHEAT +18.1 u/+699,
MELON −676, EGG −342, MILK +322, WOOL −268 — total −441, while **opponent revenue falls
127,307→126,282 on identical opponent units/rows (1,550/250)**: we pay 0.7 coins/unit of our
own price to take 1,025 off theirs.

## 4. Day band — d10–14 did not move

g170c−g60 opened per band: d5–9 +99, **d10–14 +226**, d15–19 −1,026, d20–24 +1,092
(theirs −460), d25–29 +568 (theirs −984). Against the live theta d10–14 is still −1,266
(g60 −1,492): the melon-pot hole of `2026-09-10-residual-loss20.md` is untouched.

## 5. Drops and tail

107117102 stays the only W→L board and deepens (+287 → −3,640 → **−4,629**), giving back g60's
half-repair. 107088554 (init −8,099) is now the deepest regression, −13,764 → **−19,595**, its
opponent purse *rising* +3,505 — denial backfiring. Worst-5 vs init −36,470 against g60's
−22,585, but only 12/110 negative (g60 14) — two fewer losers, a twice-deeper tail
(mean −4,378 vs −2,298). Against g60, 43/110 regress (mean −1,651) vs 67 forward (+2,606).

## 6. LOSS20 (second seed draw)

init −7,563 / 0 % → g60 −2,382 / 25 % → **g170c −1,742 / 35 %**; g170c−g60 +640 (t 1.8,
ours −163, theirs −803) — same denial signature, a third the size. g170c flips **7 tapes**
(107067869, 107068399, 107072760, 107089992, 107108124, 107116818, 107131313) to g60's 5; the
extra two are also two of the four extra live flips. All 20 tapes share one clone opening
(12 melon d0, 21–22 hires by d4, 72 melon dumped d10–14), so the opponent does not separate
them — **the base gap does**: the flipped seven average −2,747, six inside |3,600|, while all
13 that stay lost were already down over 6,500.

## 7. Verdict

+942/game over g60 (t 3.5) and +5,534 over the live theta at 65.5 % win, fidelity unchanged —
but a different kind of step: all denial, no own-purse gain, no structure change, no d10–14
repair, bought by pricing our own basket 0.7 coins/unit cheaper. It wins more boards while its
tail doubles. Ship for win rate; hold g60 if the tail matters.

## Not measured

Per-product opponent revenue (the −1,025 is unattributed); why 107088554 inverts; one seed per
board on live62; tapes cannot re-plan, so denial against an adaptive seat is unproven.
