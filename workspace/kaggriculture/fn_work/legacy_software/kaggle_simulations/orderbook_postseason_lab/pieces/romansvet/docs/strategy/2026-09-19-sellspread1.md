# SELLSPREAD1 2026-09-19 — the flat per-day sale quota, d19-29

## The premise (MAJKEL1)
Majkel1337 (3,279) and ymg_aq (3,077) play the SAME d0-5 plate; the clean
**+1,304 of wheat** between them is SHAPE, not volume — he sells 13-19 units
*every* day d19-24 at ~35 while ymg holds and dumps 235 units into d25-29 at
21-30. Every product quotes off a monotone curve in market inventory
(`spec.MARKET_ROWS`) and the town tick refills it overnight, so N units spread
over k days clear above the same N units through one row. That is LOT_SPLIT's
within-day depth bill read ACROSS days.

## The switch (`plan.SELL_SPREAD_ON`, OFF, branch `sellspread`)
From `SELL_SPREAD_DAY0` (19) the day's **voluntary** sale of WHEAT and
STRAWBERRY may draw on at most `max(stock // days_left, SELL_SPREAD_MIN)`
units, `days_left = SELL_SPREAD_END(29) - day + 1` counting today
(`plan._sell_spread_cap`, called at `plan.py:10626`). It is a cap on
`avail_vol`, the array `SELL.allocate` is greedy over — the hours
(`early_lot_turns()`), the reservation `hold`, the `press` term and the whole
day-29 ENDROUTE / ENDROUTE2 / ENDROUTE2_SPLIT / ENDROUTE_ROW2 family are the
ones that were already there, and the terminal day is exempt twice over
(`days_left == 1`, plus the `~terminal` gate).

**The design's one refusal:** the FORCED-OVERFLOW sale keeps reading the
UNCAPPED `avail` (`spare = max(avail - s_qty, 0)`, `plan.py:10799`). A quota
that also shrank `spare` would hold stock back INTO the night, which destroys
it — the quota may only refuse to put the whole shed on today's curve.

**Not a gene.** `SWITCH_GENES` is 18 wide and the shipped layout 7,692 floats;
a 19th column is a layout move every trained theta would be re-padded against.
Flown by module override only: `SW_EXTRA=,SELL_SPREAD_ON=True`.

## Byte-identity — PASS
`tests/test_sell_spread.py` 7/7. Whole-plan digests on 8 boards (d10/18/19/22/
25/27/28/29, `hold=0` so the voluntary allocation is non-empty) against a
pristine `git archive 380e0ce0 src` subprocess: **identical**, and identical
again with `SELL_SPREAD_DAY0`/`SELL_SPREAD_MIN` moved to (0,0)/(10,1)/(25,40)
while the switch is OFF. ON: d10/d18/d29 unmoved, the window moves, the quota
is monotone in the day, and the overflow board still clears.

## HIBAND (56 pinned live boards >= 2,700 seats, CRN vs `ship7692`) — HARD REJECT

| arm | dmargin | se | t | dours (t) | **dtheirs** (t) | bett/wors | win% | flips |
|---|---|---|---|---|---|---|---|---|
| `SELL_SPREAD_DAY0=19` | **-4,850** | 692 | **-7.01** | -1,818 (-4.14) | **+3,032 (+6.72)** | 4/52 | 73.2 -> 42.9 | +0/**-17** |
| `SELL_SPREAD_DAY0=22` | **-1,182** | 214 | **-5.52** | -336 (-2.30) | **+846 (+4.03)** | 11/43 | 73.2 -> 62.5 | +0/**-6** |

POOLED was never run: its precondition is HIBAND `dours > 0` and `dtheirs <= 0`,
and both arms fail both. Worst board -19,542 -> -24,594 (d19).

**DOSE-MONOTONE, and the loss is a GIFT.** Three days less quota is four fifths
less damage, so the harm IS the quota, not a bad edge day — and on both arms
THEIR purse rises more than ours falls (d19: they take +3,032 while we lose
-1,818). Withholding supply does not preserve our price, it hands the rival the
book: `mkt_inv` never resets and the town tick refills it overnight
(MELONDUMP's one-way ratchet), so their sales walk the curve down while we
hold, our held units meet a WORSE quote three days later, and the shelf we
declined to fill today is the shelf they fill instead.

**The premise was misread.** Majkel1337 sells 13-19 wheat every day d19-24
because he is still PRODUCING it — 177 wheat plantings against ymg's 139, 52
idle PASS turns against 296 — not because he caps a standing stock. A per-day
quota reproduces the *shape* of his stream with none of the volume behind it,
which is a strictly worse sale of the same inventory. The +1,304 is a
production ledger wearing a sale-timing costume.

## Verdict
**REJECT**, dose-monotone and gift-positive; the SALE-TIMING axis is now closed
in BOTH directions on the last days — LOTDEPTH rejected selling EARLIER inside
the day (-1,981), SELLSPREAD rejects selling LATER across days (-4,850), and
SELLDAY / SELLPROJ / SLOTLOCK / ENDSELL closed the rest. `SELL_SPREAD_ON` stays
False, byte-identical, layout-free (7,692 untouched, no gene column) on branch
`sellspread`, unmerged: it is a free, pinned coordinate should a WINRATE gate
ever want the opposite sign. What MAJKEL1 actually leaves standing is the
production half — wheat re-plant churn out of carrot tile-days, and idle turns
— which is the OPSCENSUS/VOLUMEHI axis, not this one.
