# flow172_g60 vs the live theta and vs flow166_g170 — anatomy on the 55 held-out LIVE boards

Date 2026-09-09. Sim only (arms-next @83cfe5c, shed-ordering fix), pinned-town action tapes,
110 board-seats (55 tapes x 2 seats), three thetas in one compiled program.
Tooling `S/g172live/anat3.py` (3-theta fork of `S/g170live/anat_live.py`) +
`S/g172live/analyze3.py`; engine-only cut `S/g172live/eng.py`.
Raw `S/g172live/anat.npz`, full dump `S/g172live/report.txt`, engine table `S/g172live/eng.txt`.

Thetas: `init` = flow135_g350_gpfwdfv_gb028 (the LIVE theta), `g170` = flow166_g170,
`g60` = flow172_g60 (= g170 + 60 generations on the fixed population, shed-fixed sim,
12-tape fresh gate). Seeds taken verbatim from the engine CSVs
`S/lossflip/{flow135_g350,flow166_g170,flow172_g60}_live62.csv`, so sim and engine are
paired board-for-board.

Theta space: |g170-init| L2 3.08, |g60-g170| L2 1.95, and the two steps are **orthogonal**
(cos 0.045) — the extra 60 generations are a new direction, not more of the same one.

## 0. Engine headline (the judge)

| theta | margin | win | ours | theirs | excl 107088554/107095149 |
|---|---|---|---|---|---|
| init (LIVE) | -286 | 34.5 % | 100,792 | 101,077 | +119 / 35.8 % |
| g170 | +2,482 | 52.7 % | 102,512 | 100,031 | +3,264 / 54.7 % |
| **g60** | **+4,306** | **58.2 %** | 104,164 | 99,858 | **+4,952 / 60.4 %** |

| pair | d-margin | t | d OURS | d THEIRS | win | flips | drops | boards up |
|---|---|---|---|---|---|---|---|---|
| g60 - init | +4,592 | 11.0 | +3,372 | -1,220 | 34.5 -> 58.2 % | +28 (14 tapes) | -2 (1 tape) | 96/110 |
| g170 - init | +2,767 | 5.8 | +1,721 | -1,047 | 34.5 -> 52.7 % | +22 (11 tapes) | -2 (1 tape) | 84/110 |
| **g60 - g170** | **+1,825** | **8.9** | **+1,652** | **-173** | 52.7 -> 58.2 % | +6 (3 tapes) | 0 | 94/110 |

## 1. Fidelity — the sim is a valid judge for all three thetas

| theta | sim margin / win | engine margin / win | mean abs d | median | max | >500 | W/L agree | corr |
|---|---|---|---|---|---|---|---|---|
| init | -240 / 34.5 % | -286 / 34.5 % | 283 | 61 | 1,930 | 18/110 | 100 % | 0.999 |
| g170 | +2,558 / 52.7 % | +2,482 / 52.7 % | 170 | 44 | 1,076 | 15/110 | 100 % | 1.000 |
| **g60** | **+4,394 / 58.2 %** | **+4,306 / 58.2 %** | **154** | **41** | 1,215 | 10/110 | 100 % | 1.000 |

Own-purse mean abs diff 143 / 86 / **48**; opponent-purse 185 / 149 / **125**.
Pooling the two seats per tape (most >500 rows are a seat-label swap, not error):

| theta | per-tape mean abs d | median | max | tapes >500 |
|---|---|---|---|---|
| init | 127 | 34 | 1,930 (107044716) | 2/55 |
| g170 | 124 | 35 | 1,076 (107048085) | 4/55 |
| g60 | **121** | 38 | 1,215 (107134203) | 3/55 |

Deltas: g60-init sim +4,633 vs engine +4,592 (corr 0.992); g60-g170 sim +1,836 vs engine +1,825
(corr 0.992, mean abs diff 104); g170-init sim +2,797 vs engine +2,767 (corr 0.995).
**g60 is the highest-fidelity of the three.**

## 2. Two-purse — g60 over the live theta is *more* growth-weighted than g170 was

Sim (engine in brackets, agreeing within ~60 coins everywhere).

### 2a. g60 - init (the live theta)

| set | n | base | g60 | d-margin | t | d OURS | d THEIRS | growth share | win |
|---|---|---|---|---|---|---|---|---|---|
| ALL | 110 | -240 | +4,394 | **+4,633** | 11.19 | **+3,418** | **-1,216** | 73.8 % | 34.5 -> 58.2 % |
| WIN-boards (live won) | 38 | +12,108 | +15,093 | +2,985 | 5.79 | +2,793 | -192 | 93.6 % | 100 -> 94.7 % |
| LOSS-boards (live lost) | 72 | -6,756 | -1,254 | **+5,503** | 10.08 | +3,747 | **-1,756** | 68.1 % | 0 -> 38.9 % |
| ALL excl 107088554/107095149 | 106 | +159 | +5,038 | +4,880 | 12.06 | +3,507 | -1,372 | 71.9 % | 35.8 -> 60.4 % |

(engine: ALL +4,592 = +3,372 / -1,220; WIN +3,009 = +2,796 / -213; LOSS +5,427 = +3,676 / -1,751.)

Against g170's split (62 % growth / 38 % denial overall, 96 % growth on WIN, 56 % on LOSS),
**g60 is 74 % growth / 26 % denial**. The denial term is essentially unchanged in absolute size
(-1,216 vs g170's -1,052, both concentrated on loss boards); the whole improvement over g170 is
extra own-purse growth (+3,418 vs +1,745).

### 2b. g60 - g170 (what the extra 60 generations bought)

| set | n | base | g60 | d-margin | t | d OURS | d THEIRS | growth share | win |
|---|---|---|---|---|---|---|---|---|---|
| ALL | 110 | +2,558 | +4,394 | **+1,836** | 8.83 | **+1,673** | **-163** | **91.1 %** | 52.7 -> 58.2 % |
| WIN-boards | 38 | +13,359 | +15,093 | +1,733 | 4.88 | +1,596 | -138 | 92.0 % | 94.7 -> 94.7 % |
| LOSS-boards | 72 | -3,143 | -1,254 | +1,890 | 7.32 | +1,713 | -177 | 90.6 % | 30.6 -> 38.9 % |
| ALL excl 2 outliers | 106 | +3,337 | +5,038 | +1,702 | 8.32 | +1,512 | -190 | 88.8 % | 54.7 -> 60.4 % |

(engine: ALL +1,825 = +1,652 / -173; WIN +1,782; LOSS +1,847.)

**The g170 -> g60 step is 91 % pure growth and it is flat across win and loss boards**
(+1,733 vs +1,890) — no new denial channel, no concentration on the boards we were already
losing. Opponent season totals are unchanged by construction (1,550.3 -> 1,550.4 units in
250.4 rows) and their revenue moves only 127,516 -> 127,307.

## 3. Ranked diff — what the extra 60 generations changed (g60 - g170)

Ordered sell qty x that day's quote, season mean per board:

| product | d qty | coins |
|---|---|---|
| WHEAT | -8.3 | -359 |
| MELON | +1.8 | +347 |
| CARROT | +5.7 | +303 |
| WOOL | +2.0 | +303 |
| MILK | -2.6 | -296 |
| EGG | +3.9 | +201 |
| FERTILIZER | +4.3 | +162 |
| STRAWBERRY / TOMATO | -1.9 / -0.2 | +67 / -13 |
| **TOTAL** | **+4.7** | **+714** |

By band: d15-19 is where the intent moves (+1,047; strawberry +481, wool +411, melon +236,
wheat -175), then d20-24 +294 and d25-29 -358 (strawberry -336, carrot +229, wheat -175).

**The structural picture is the striking part: g60 changed almost no structure at all.**
Every opening decision that g170 had already moved is byte-identical in g60, on all 110 boards:

- d0 basket **identical** — GOOSE 1 / COW 4 / SHEEP 1, seed WHEAT 9 / CARROT 10.
- d0 wheat pump **identical** — 53 units. BUY_LAND 2, nquad 3 — identical.
- HIRE d0-d4 identical (4/4/4/5/4); only d5 moves 5.22 -> 5.33, season 271.1 -> 272.8.
- Tiles by band move by <=0.8 anywhere; planted d5-9 33.5 -> 34.2, idle 7.8 -> 7.2.
- PLANT orders: wheat -1.9, carrot +1.5, everything else <=0.2.
- Herd: sheep 5.96 -> 6.33, goose 3.18 -> 3.38, cow 7.42 -> 7.29.

What actually moved is **execution quality**, and it is almost all one lever:

| | g170 | g60 |
|---|---|---|
| ordered SELL rows at h1 | 105.8 | **99.4** |
| ordered SELL rows at h18 | 32.2 | **38.0** |
| SELL rows executed | 142.6 | 141.8 |
| sold units / revenue | 1,370 / 126,557 | 1,375 / **128,552** |
| **realised price per unit** | **92.38** | **93.47** |
| units per SELL row | 9.61 | 9.70 |
| opponent rev / units / rows | 127,516 / 1,550.3 / 250.4 | 127,307 / 1,550.4 / 250.4 |

**+1,995 of revenue on +5 units** — g60 sells the same basket at a 1.2 % better price by pushing
another 5.8 sell rows out of hour 1 into hour 18. This is the same direction g170 moved from the
live theta (h1 113.4 -> 105.8, h18 21.9 -> 32.2) taken a second step (h1 99.4, h18 38.0), even
though the two theta steps are geometrically orthogonal (cos 0.045).

For reference, g60 - init (the full two-step): WOOL -11.1 units / -2,258 coins,
CARROT +41.6 / +2,040, WHEAT -34.6 / -1,500, MILK +2.9 / +1,240, MELON -1.2 / -1,162,
EGG +19.6 / +1,020; d0 SHEEP 2 -> 1 / COW 3 -> 4, seed WHEAT 10 -> 9 / CARROT 9 -> 10,
HIRE d1/d2 1.00/2.11 -> 4.00/4.00, idle d5-9 10.6 -> 7.2, PLANT CARROT 27.8 -> 39.2,
h1 113.4 -> 99.4 / h18 21.9 -> 38.0, realised price/unit 92.03 -> 93.47.

## 4. Flips, the drop board, and the three extra flips over g170

**Flips vs the live theta (engine, L->W): 28 board-seats = 14 tapes.** g170 flipped 11 of them;
g60 keeps all 11 and adds three.

    tape        init      g170       g60
    107035330  -6958    +3971     +3868
    106974180  -6385    +3004     +6656
    106978129  -5567    -2460      +233   <- EXTRA
    106968689  -4823     +701     +1504
    107131313  -3541    +3364     +3798
    107018738  -3535    -1326     +1775   <- EXTRA
    107072760  -2461    +5938     +8167
    106985187  -2281    +8680     +9268
    107008497  -2139    +1653     +5712
    107044716  -1876    -2170      +649   <- EXTRA
    107068399  -1118     +977     +1344
    107016108   -338    +2395     +2753
    107116818   -295    +5061     +8220
    107108124   -167    +8379     +8983

Median flip base -2,371; 16/28 board-seats inside |2,500|, so the flips are not only a
close-loss effect. Decomposition of the +4,592: the 28 flips carry +1,887 of it, the other 82
boards +2,705 (mean +3,628 each). Excluding flips, the drop and the two outliers: 66/76 boards
still improve, mean +4,114. **The gain is broad, not flip-driven.**

**The three extra flips are growth, not denial** (sim purses, mean of the 6 board-seats):

    106978129   dOURS +2,357  dTHEIRS   -336
    107018738   dOURS +1,572  dTHEIRS -1,529
    107044716   dOURS +2,850  dTHEIRS    +31

**The drop board 107117102 (both seats) is inherited from g170 and half-repaired.**
Engine +287 (init) -> -7,328 (g170) -> -3,640 (g60): g60 gives back +3,688 of g170's -7,615.
It is still the only W->L board on the set, and it is still the denial-handed-back board
documented for g170 (our wool withdrawal lifted the price on their fixed wool sales).

Per-day cash on the three extra-flip tapes: g60 is *behind* g170 through d15 (-347 at d12) and
takes the lead from d18 (+512), d21 +1,367, d27 +1,825 — the evening-sell price effect again,
not an opening change (d0 basket and seeds identical, hire season 266.3 -> 271.0).
The drop board follows the same shape: g60 behind by -767 at d15, then +3,011 by d18.

## 5. Where the extra margin opens — d15 onward, entirely in our own purse

Cumulative d-margin at end of each band (sim, eod cash, all 110 boards):

| band | g60 - g170 opened | cum | d OURS | d THEIRS | | g60 - init opened | cum |
|---|---|---|---|---|---|---|---|
| d0-4 | +0 | +0 | +0 | +0 | | +99 | +99 |
| d5-9 | -13 | -13 | -7 | +5 | | +1,227 | +1,326 |
| d10-14 | -450 | -462 | -421 | +41 | | -1,492 | -166 |
| d15-19 | **+1,145** | +683 | +626 | -57 | | +798 | +632 |
| d20-24 | +675 | +1,358 | +989 | -369 | | **+1,923** | +2,556 |
| d25-29 | +478 | +1,836 | +1,673 | -163 | | **+2,078** | +4,633 |

The g170 -> g60 step has **no d0-9 component at all** (-13 by d9): it is entirely a
d15-29 effect, and 91 % of it is our own cash. That is the complement of the g170 -> init step,
whose first window was d5-9 growth (+1,240) from the earlier hiring. The d10-14 dip (-450) is
the cash-measure artefact — inventory held back from the morning row is not counted until it
sells in the evening from d15.

So the two steps stack cleanly:

- **g170 over live** = d5-9 hiring/board-fill growth + d20-29 price denial.
- **g60 over g170** = d15-29 sell-timing price gain, own purse only.

## 6. Downside

Worst-5 board-seats by d-margin vs the live theta:

| | worst five | sum | n negative | mean of negatives |
|---|---|---|---|---|
| g170 | 107088554 -10,564 (x2), 107117102 -7,615 (x2), 107040955 -6,709 | -43,067 | 26/110 | -3,828 |
| **g60** | 107088554 -5,665 (x2), 107117102 -3,927 (x2), 107023915 -3,401 | **-22,585** | **14/110** | **-2,298** |

g60's tail is roughly half of g170's on every measure: same two boards at the top of it, both
about half as deep, and 12 fewer losing boards. g60 repairs g170's two worst regressions
(107088554 +4,899, 107040955 +6,030/+6,046) rather than adding new ones.

Worst-5 of g60 against g170 itself: 107079367 -2,457 (x2), 107032494 -2,325 (x2),
107160628 -2,003. Only 16/110 board-seats go backwards (mean -1,021) against 94 forward
(mean +2,309); the deepest single regression is -2,457, well under the +5,887 best.
Quantiles of g60 - g170: 5 % -1,397, 25 % +384, 50 % +1,281, 75 % +3,144, 95 % +5,887.

## 7. Verdict — g60 is the *cleaner* candidate, not the more denial-heavy one

g60 is a strictly cleaner candidate than g170: it beats it by +1,825/game (t 8.9, engine) with
**91 % of that from our own purse**, it adds no new denial channel (d THEIRS -173 against
g170's -1,047 over the live theta), it changes no opening decision, it halves g170's downside
tail (26 -> 14 losing boards, worst-of-worst -10,564 -> -5,665), and it half-repairs g170's only
W->L drop. Overall against the live theta it is 74 % growth / 26 % denial versus g170's
62 / 38. The one lever behind it is a further shift of sell rows from hour 1 to hour 18,
worth ~+1.1 coins per unit realised.

## Not measured

- Per-product opponent revenue (only totals exist), so the residual -163 denial cannot be
  attributed.
- Executed (filled) sell quantities: the ranked table is **ordered** intent at the day's quote
  (sums to +714) while realised revenue is +1,995.
- The gap between our purse gain (+1,673) and realised revenue (+1,995) — spend vs held
  inventory — is not decomposed.
- Tapes cannot re-plan, so an evening-sell price gain against an adaptive live seat that would
  re-price is not established here.
- One seed per board, no replication; drawn-veto legs for g60 were still running at write time.
