# CHURNPRICE1 — do fixed sale rows miss intra-day quote highs that top-5 seats catch? (2026-09-25, read-only)

Scripts + data: `S/churnprice1/` (pick.py, dl.sh, extract.py, tables.py, qpath.py, lane.sh, dev.py, pair.py; out/).
Replays: the 14 TOP5VSV1 episodes + the 18 latest vrp2/vrp3 live losses (LIVELOSS13 games_*.json, non-self-play, only 18
exist outside the 14) — 32 x HTTP 200, raw/ gitignored. Ledger = S/econcensus measure() on the locked engine, with
`_commit_unit` hooked per unit (seat, day, hour, op, item, unit price) and the recorded obs quote per turn.

## Fields
`observation.market.prices[item]` and `.inventory[item]` exist on EVERY step (24/day), shared by both seats: the quote
is fully observable intra-day. Price is a function of the one never-reset inventory: SELL +1 unit, BUY_PRODUCT -1, the
shop/town tick drains it (ticks after turns 0,4,8,...,20 -> post-tick highs on h1,5,9,13,17,21). SELL is from the shed
at any turn (no hand at market needed). "Quote at turn" = obs at the start of that turn (the book the order walks).
Seat classes: ours = OurTeam; top5 = DECEM / Mother-Goose / M&M&P&Q / Boey (DSM not in these games); opp = rest.

## Table A — realised / same-day max quote, sale-turn histogram (units-weighted, out/tableA.tsv, out/hist.tsv)
| item | class | units | realised | day max q | q at sale turn | real/max | q_turn/max | modal hours (share) |
|---|---|---|---|---|---|---|---|---|
| WHEAT | ours | 9277 | 34.6 | 36.6 | 35.6 | 0.945 | **0.972** | h1 .76, h21 .10 |
| WHEAT | top5 | 2845 | 34.9 | 36.0 | 35.2 | 0.968 | 0.977 | h22 .18, h0 .14, h1 .12 |
| WHEAT | opp | 17348 | 36.4 | 37.5 | 36.9 | 0.971 | 0.983 | h0 .13 (spread) |
| STRAWBERRY | ours | 5992 | 133.1 | 147.5 | 144.7 | 0.902 | **0.981** | h17 .71, h1 .27 |
| STRAWBERRY | top5 | 1656 | 158.3 | 167.7 | 162.8 | 0.944 | 0.971 | h0 .28, h1 .11, h23 .10 |
| STRAWBERRY | opp | 7309 | 119.0 | 135.9 | 125.4 | 0.876 | 0.923 | h0/h21/h19 ~.14 |
| WOOL | ours | 3975 | 133.3 | 155.8 | 148.0 | 0.856 | **0.950** | h17 .68, h1 .24 |
| WOOL | top5 | 1056 | 143.8 | 163.6 | 152.3 | 0.879 | 0.931 | h1 .17, h5 .10 |
| WOOL | opp | 6259 | 135.5 | 157.0 | 144.1 | 0.863 | 0.918 | h1 .14, h0 .13 |
| MILK | ours | 4738 | 115.8 | 131.2 | 128.0 | 0.882 | **0.975** | h17 .64, h1 .30 |
| MILK | top5 | 1423 | 125.1 | 138.9 | 129.9 | 0.901 | 0.935 | h23 .17, h1 .14, h21 .12 |
| MILK | opp | 6612 | 112.2 | 125.9 | 117.8 | 0.891 | 0.936 | h0 .15, h1 .13 |
| MELON | ours | 2149 | 162.0 | 174.2 | 173.7 | 0.930 | **0.997** | h1 .99 |
| MELON | top5 | 520 | 180.8 | 212.4 | 188.9 | 0.851 | 0.889 | h1 .17, h9 .15, h10 .10 |
| MELON | opp | 2297 | 236.2 | 259.0 | 242.1 | 0.912 | 0.935 | h10 .25, h0 .18 |
**Our sale turns already sit on the day's highest quote** (q_turn/max 0.95-0.997, above top5 0.89-0.98 and opp 0.92-0.98 on
every product). The day max falls on our rows (out/qpath.txt, days we sold): straw/wool/milk argmax h17 30-39 %, h1 20-29 %,
h13 12-21 %; wheat h0/h1 90 %; melon h1 97 %. h22/h23 (top5 modal for wheat/milk) quote 0.90 / 0.69 of the day max.
Our realised/max gap (0.86-0.95) is the order's own walk down the book (volume/depth), not timing. The top5 price edge
(straw 158 vs 133, melon 181 vs 162) is in the day-max column itself = board/inventory level, not turn choice.

## Table B — opponent market buys (out/tableB_{200,50,20}.tsv)
No opponent turn buys >= 200 units (max 89 u/turn; churn is spread, 8 seat-days >= 200 u/day, all Debmalya wheat).
>= 50 u/turn: 39 events, all WHEAT: quote +3.26 at t+1 (range +2..+5 on ~36), +0.08 at t+2, 0.00 at t+3 — the churner's own
resale eats the spike next turn. Ours sold 7 of 634 same-day wheat units in the window (2/39 events), top5 0 (no overlap),
opp 34 %. >= 20 u/turn: 114 events (112 wheat), +2.89 / +0.54 / +0.56; ours 27 % of same-day units in window, top5 8/15.
A ~+3 coin/unit one-turn wheat spike is the whole transient; nothing on straw/wool/milk/melon.

## Counterfactual (exact guard sim, SAFETY_S 1e9 both arms, dev boards 0-9 vs reacting V56, 4 lanes)
Base W 8/10. Arm `SHED_DUMP_ROW_ON=True` (one extra SELL row at turn 23 = top5 milk modal; the only existing
one-extra-row switch; turn 22 is ENDROUTE's, assert-blocked): **byte-identical 10/10** (W 8->8, flips 0, dours 0, dtheirs 0)
— the row only sells shed overflow and the VRP crew never overflows. A row that takes volume = SPREAD_ROWS (asserts on the
LOT4 turn 17; measured before, SPREAD6 REJECT -2,465 t -13.7) or NIGHTROW (h22 d20-28, REJECT); by Table A it would sell at
0.69-0.91 of the day max vs our current 0.95-1.0. Not built (read-only brief, no planner change).

## Verdict
**No lever.** The quote path is fully observable and has transient highs (post-tick h1/h13/h17, opp-buy wheat +3 for one
turn), but our fixed rows already sell on the day's max (0.95-0.997), better than top-5 seats (0.89-0.98). The top-5
strawberry/milk/melon price edge is the book level on their boards (day max +20..+38), not timing. Sale-timing axis stays
CLOSED; the residual is depth (walk-down 5-14 %), already measured by LOT4/SPREAD6/LOTDEPTH.
