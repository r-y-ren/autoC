# Full-H30 post-sale cash decomposition

The completed `off_h30_cash` baseline passed OFF identity for all 60 H30 games
against `sell5off_B_livech.csv`. `S/postlot/explain_cash.py --off-tag
off_h30_cash` then checked all 30 frozen boards in both seats, complete 720-step
replays, final replay/CSV money, identical opponent identities and actions, and
cash-delta closure. It produced 5,865 changed cash transitions. This report is
H30-only; no H30B or other-family evidence is pooled into it.

## Family result and concentration

The decomposition exactly recovers the pilot means: own cash +134.87, opponent
cash +391.70, hence margin -256.83. Ten boards improve margin, ten worsen it,
and ten have identical paired final cash. The net loss is concentrated rather
than uniform.

| board | own delta | opponent delta | margin delta | opponent physical rows |
|---:|---:|---:|---:|---:|
| 818776373 | -870 | +2448 | **-3318** | 0 |
| 495341287 | -697 | +1375 | **-2072** | 0 |
| 306785256 | -1387 | +399 | **-1786** | 0 |
| 1196709180 | -1575 | +122 | -1697 | 24 |
| 213120026 | -1277.5 | +197.5 | -1475 | 0 |

The first three rows contribute -7,176 of the H30 board-summed net margin
change of -7,705, or 93.1%; positive boards offset further adverse rows. The
opponent gain is also concentrated. Boards 818776373 (+2448), 117862337
(+2312.5), and 1219841551 (+2185) contribute 13,891 of the 23,502 total
opponent coin increase across the 60 games, or 59.1%. Adding boards 495341287
and 2103701353 raises that share to 82.0%.

## Shared-market gain is the dominant opponent mechanism

The opponent submits exactly the same action sequence in all 60 pairs. Of its
3,694 changed cash transitions, 3,481 (94.2%) have at least one different
displayed pre-action price. Opponent cash deltas total +23,502. Of that total,
+18,666 (79.4%) occurs on turns where the controlled player's current market
order list is also identical; +4,836 occurs where that current list differs.
This is a temporal classification, not an order-level causal allocation: an
earlier changed controlled sale alters shared inventory and later quotes even
when both current order lists match.

The three worst margin boards have zero opponent physical-state differences at
every step. Their opponent gains therefore cannot be attributed to a changed
farm, inventory, or action trajectory. The preserved state differs in shared
market inventory/prices and controlled-player state, and the unchanged opponent
orders settle against that different market path.

Board 818776373 is the clearest driver. Both seats are identical at own -870 and
opponent +2448, with no opponent physical difference. Opponent cash is slightly
down through day 18 and then gains +2,564 over days 20–29, including +694 on day
29. Its largest single gain is +390 on the final liquidation at day 29 hour 21,
where the opponent order list is identical. In total, +2,228 of its +2,448 gain
occurs on rows with the same current controlled orders; only +220 coincides
with a changed current controlled list. The effect is a persistent quote path,
not opponent replanning.

Board 117862337 shows a seat-sensitive version of the same mechanism. Opponent
cash rises +3261 when we control seat 0 and +1364 when we control seat 1, while
opponent physical state and submitted actions remain exact in both games. The
same-current-controlled-order partitions are +3268 and +1471; rows with changed
current controlled orders contribute -7 and -107. In seat 0, days 25–29 add
+3039 and the final liquidation transition alone adds +1142. The seat gap is
therefore in the seat-dependent shared-market path, not a different opponent
program.

Board 1219841551 contributes +2185 opponent coins in each seat. Seat 0 has 48
late opponent physical rows, but +2181 of +2185 cash is already present before
the first physical difference at step 672. Seat 1 has no opponent physical
difference and the same +2185 outcome. The cash gain is therefore established
before that late weed state and replicated without it in the other seat.

## Own replanning explains the adverse side of the worst boards

Across H30, own changed cash transitions sum to +8,092: +9,338 occurs on rows
where our current market orders differ, while rows with the same current orders
sum to -1,246 from changed prices or other state. The positive aggregate hides
large board-level reversals.

On board 818776373, -869 of the -870 own result occurs on rows with changed own
market orders. Large negative replanning rows include day 9 (-1490), day 19
(-1015), day 22 (-1104), day 24 (-765), and day 29 (-534), partly offset by
large gains on days 8, 15, and 26. Concrete order changes include selling six
fewer milk at day 9 hour 18 (-1213 for the bundled transition), and later
selling fewer eggs and milk at day 19 hour 18 (-1324). The injected crop is
productive, but it changes later production and liquidation choices.

On board 495341287, changed-own-order rows sum to -801 while same-order rows
sum to +104, closing at -697. Its largest later losses include -816 when ON
sells two fewer strawberry and three fewer wool at day 22 hour 18, and -666
when it sells four fewer wool at day 28 hour 18. Meanwhile the unchanged
opponent collects +1375, including +870 on rows where our current order is the
same.

On board 306785256, changed-own-order rows account for -1391 of the -1387 own
result. At day 22 hour 1 the ON row sells two fewer strawberry and six fewer
melon, contributing -1283 for the bundled transition. The opponent gains +399,
of which +364 occurs on rows where our current market list matches. As on the
other two largest adverse boards, opponent physical state never differs.

These observations sharpen the four-board result without changing its limits.
Replay money records a whole turn after several interleaved orders, so a cash
delta cannot be assigned to one item inside a bundled transition. The
same-current-order partition measures persistence of the market path rather
than an isolated causal effect. The evidence supports neither promotion nor a
new variant. It identifies the full-H30 failure as a combination of unstable
controlled replanning on a few boards and a broad, late shared-price benefit to
unchanged opponent orders.
