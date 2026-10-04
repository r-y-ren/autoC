# flow166_g170 vs the live theta — anatomy on the 55 held-out LIVE boards

Date 2026-09-09. Sim only (arms-next @83cfe5c, shed-ordering fix), pinned-town action tapes,
110 board-seats (55 tapes x 2 seats). Tooling `S/g170live/anat_live.py` + `analyze_live.py`;
raw `S/g170live/anat.npz`, full dump `S/g170live/report.txt`, extras `S/g170live/extra.txt`,
per-tape engine table `S/g170live/engine_tapes.txt`.
Thetas: `rec` = flow166_g170, `init` = flow135_g350_gpfwdfv_gb028 (the live theta).
Seeds taken verbatim from the engine CSVs `S/lossflip/flow166_g170_live62.csv` /
`flow135_g350_live62.csv`, so sim and engine are paired board-for-board.

## 1. Fidelity — the sim reproduces the engine read

| theta | sim margin / win | engine margin / win | mean abs diff | median | max | >500 |
|---|---|---|---|---|---|---|
| init | -240 / 34.5 % | -286 / 34.5 % | 283 | 61 | 1,930 | 18/110 |
| rec  | +2,558 / 52.7 % | +2,482 / 52.7 % | 170 | 44 | 1,076 | 15/110 |

W/L agreement 100 % on both thetas; corr(sim, engine) 0.999 / 1.000.
Delta: sim +2,797 vs engine +2,767, corr 0.995, mean abs diff 208.

Most of the >500 rows are a **seat-label swap**, not error: on seat-asymmetric tapes the sim's
seat 0/1 pair carries the same two values as the engine's seat 1/0 pair
(106985187, 106994269, 107055322, 107101394, 107023915, 107040955, 106964817).
Pooling seats per tape:

| theta | mean abs diff | median | max | tapes >500 |
|---|---|---|---|---|
| init | 127 | 34 | 1,930 (107044716) | 2/55 |
| rec  | 124 | 35 | 1,076 (107048085) | 4/55 |

Residual band 107018738 +409/+748, 107160628 +678/+641, 107134203 +363/+476 — shop-draw size.
**Verdict: the sim is a valid judge on this set.**

## 2. Two-purse — 62 % growth, 38 % denial; denial only where we were losing

Sim (engine numbers in brackets; they agree within 60 coins everywhere):

| set | n | base | g170 | d-margin | t | d OURS | d THEIRS | win |
|---|---|---|---|---|---|---|---|---|
| ALL | 110 | -240 | +2,558 | **+2,797** | 5.84 | **+1,745** | **-1,052** | 34.5 -> 52.7 % |
| WIN-boards (live won) | 38 | +12,108 | +13,359 | +1,252 | 1.91 | +1,197 | **-54** | 100 -> 94.7 % |
| LOSS-boards (live lost) | 72 | -6,756 | -3,143 | **+3,613** | 5.77 | +2,034 | **-1,579** | 0 -> 30.6 % |
| ALL excl 107088554/107095149 | 106 | +159 | +3,337 | +3,177 | 7.02 | +1,995 | -1,182 | 35.8 -> 54.7 % |

(engine: ALL +2,767 = +1,721 / -1,047; WIN +1,227 = +1,185 / -41; LOSS +3,580 = +2,003 / -1,577.)

- On the boards the live theta already won the gain is **pure growth** (their purse -54).
- The denial is entirely on the loss boards, and it is **price-only**: the opponents are
  action-replay tapes, so their units and rows cannot move — season totals 1,550.1 -> 1,550.3
  units in 250.4 -> 250.4 rows, price/unit 82.93 -> 82.25 (loss boards -1.00, win boards -0.06).
- Our purse: revenue +1,129 on +7.1 units (price/unit 92.03 -> 92.38); the remaining +616 is
  spend/held-inventory, not decomposed.

### Flips: broad gain, with the flips coming off small base margins

22 flipped board-seats = 11 tapes. Engine base margins (L->W):

    107035330 -6958 -> +3971      107008497 -2139 -> +1653
    106974180 -6385 -> +3004      107068399 -1118 ->  +977
    106968689 -4823 ->  +701      107016108  -338 -> +2395
    107131313 -3541 -> +3364      107116818  -295 -> +5061
    107072760 -2461 -> +5938      107108124  -167 -> +8379
    106985187 -2281/-1028 -> +8680 (both seats)

Median base -2,210; 14/22 inside |2,500|. But the gain is **not** a close-loss effect:

- 84/110 boards improve, 75 by more than +1,000, 16 lose more than -1,000.
- The 22 flips contribute +1,346 of the +2,767 mean; the other 88 boards contribute +1,422
  (mean +1,777 each). Excluding the flips, the two outliers and the drop board: 62/82 boards
  improve, mean +2,446.

## 3. Ranked diff (ordered sell qty x that day's quote, season mean per board)

| product | d qty | coins |
|---|---|---|
| WOOL | -13.1 | -2,561 |
| CARROT | +35.9 | +1,736 |
| MILK | +5.5 | +1,537 |
| MELON | -3.0 | -1,509 |
| WHEAT | -26.3 | -1,141 |
| EGG | +15.7 | +819 |
| FERTILIZER | -6.2 | -294 |
| STRAWBERRY / TOMATO | -2.5 / +1.0 | -92 / +76 |

By band: wool leaves d10-19 (61.3 -> 48.7 units) and melon leaves d10-19 (12.0 -> 5.1);
carrot arrives d20-29 (64.5 -> 93.6) and wheat leaves it (177.3 -> 142.6); milk/egg come
earlier (d0-9 18.0 -> 24.0 and 7.5 -> 9.1).

Structural moves — every one of them is the g50/g150 anatomy, now confirmed on held-out live
boards, and all are deterministic across all 110 boards:

- **d0 basket**: SHEEP 2 -> 1, COW 3 -> 4; seed WHEAT 10 -> 9, CARROT 9 -> 10.
- **Hiring earlier**: HIRE qty d0/d1/d2 4.00/1.00/2.11 -> 4.00/4.00/4.00 (4/4 by day 1);
  season 264.6 -> 271.1.
- **Fewer idle tiles d5-9**: idle 10.6 -> 7.8, planted 30.3 -> 33.5; wheat tiles 8.2 -> 11.2.
- **Sell rows to the evening**: h1 113.4 -> 105.8, h18 21.9 -> 32.2 (d10-19 h18 9.0 -> 13.7);
  SELL rows 139.6 -> 142.7, units/row 9.77 -> 9.61.
- **Late carrot**: tiles d25-29 6.1 -> 8.8, d20-24 3.1 -> 4.8; PLANT CARROT orders 27.8 -> 37.7.
- **Herd**: sheep 6.38 -> 5.96, goose 2.83 -> 3.18, cow 7.75 -> 7.42; coop tiles 2.8 -> 3.2,
  pasture 14.1 -> 13.4.
- Unchanged: d0 wheat pump (53 units), BUY_LAND 2, nquad 3, FEED count.

## 4. The dropped board — 107117102 (both seats), the only W->L

Engine +287 -> -7,328; sim +514 -> -7,215. **We grew (+4,769) and they grew more (+12,498).**
Their tape is fixed: 1,526 units in 304 rows in both runs, revenue 113,254 -> 125,839,
price/unit **74.22 -> 82.46**. Our side made the same d0 swap (SHEEP 2 -> 1, COW 3 -> 4) and cut
ordered wool 152 -> 79 units; carrot +62, egg +49, milk +40. Their cash pulls away from d16 and
the gap is +10.8k by d28. This is the denial-handed-back signature from the two-purse rule:
withdrawing our own wool supply lifted the price on their unchanged wool sales.
(107088554, excluded from the headline, is the same shape: theirs 103,374 -> 114,572 while ours
barely moves. 107095149 is the opposite — our own purse drops 115,233 -> 104,617.)

## 5. Where the margin opens

Cumulative d-margin at end of each band (sim, all 110 boards):

| band | opened in band | cum | d OURS | d THEIRS |
|---|---|---|---|---|
| d0-4 | +99 | +99 | +98 | -0 |
| d5-9 | **+1,240** | +1,339 | +1,382 | +43 |
| d10-14 | -1,042 | +297 | +190 | -107 |
| d15-19 | -348 | -51 | -94 | -43 |
| d20-24 | +1,248 | +1,198 | +499 | -698 |
| d25-29 | **+1,600** | +2,797 | +1,745 | -1,052 |

Two windows, two mechanisms:

- **d5-9 is growth** (+1,382 own cash by d9, their purse untouched) — the earlier hiring and the
  fewer idle tiles.
- **d20-29 is the price attack** (their purse -1,052, all of it after d19) plus the late-carrot
  own-purse gain. The mid-game dip d10-19 is largely a cash-measure artefact: standing inventory
  is not counted, and it comes back as revenue from d20.

Split: LOSS boards open +925 (d20-24) and +2,175 (d25-29); WIN boards +1,862 and +510.

## Not measured

- Per-product opponent revenue: only totals exist, so the -1,052 price denial cannot be pinned
  to a product.
- Executed (filled) sell quantities per product. The ranked table uses **ordered** qty at the
  day's quote and sums to -1,428, while realised revenue is +1,129 — the ranking is intent,
  not fills.
- The +616 residual of our purse gain (spend vs held inventory).
- Adaptive opponents: tapes cannot re-plan, so the denial channel here is price-only by
  construction and may not transfer to a live seat that would re-price or re-plan.
- One seed per board, no replication: the board/shop lottery is not separated from the effect.
