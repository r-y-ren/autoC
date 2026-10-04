# Which channel hands the top tier money? g300 vs the live theta, TOPB vs LIVE55

2026-09-10. Engine csvs verdict; sim (`S/toptransfer/`) descriptive, opponent purse to ~70 coins.

## 0. Engine, paired vs `flow135_g350`

dTHEIRS, g60 / g170c / **g300** — TOPB (40 seats) +1,092 / +974 / **+921**; TOPB pairs +526 / +413 /
**+689**; LIVE55 (124) −1,137 / −2,154 / **−2,421**. g300 on TOPB: dOURS +4,087, dMARG +3,166
(pair +3,730). Sim: opponent purse **+913** / **−2,314** — a 3.3 k swing.

## 1. Price, and only price — not a contested resource

Opponent units sold move by **−0.03** of 1,550 (LIVE55) and **+0.17** of 1,589 (TOPB); their
price/unit moves 82.93→81.35 and 81.58→82.10. Revenue −2,451 / **+848**, split qty/price
−2 / −2,449 and +14 / **+834**.

TOPB opponent hands (11.00→11.00), quads (2.25→2.25), tiles (±0.05) and herd (−0.04) are unchanged:
no shop stock, land, animal or hire is taken, and their SELL tape fills identically.

## 2. Opponent revenue delta by band and product (sim, coins/board-seat)

| band | d0–9 | d10–14 | d15–19 | **d20–29** |
|---|---|---|---|---|
| LIVE55 | +37 | −270 | −90 | **−2,128** |
| TOPB | +61 | −145 | −209 | **+1,141** |

Identical to d19; the sign flips over the last ten days, where TOPB tapes sell 43 % of their volume.
Their units allocated to products by tape intent, at the day's quote:

| product | LIVE55 | TOPB | their units L→T | d20–29 Δquote L→T |
|---|---|---|---|---|
| WOOL | **+992** | **+1,454** | 394 → 557 | −0.42 → **+15.19** |
| MELON | +107 | **+551** | 150 → 239 | +19.96 → +13.84 |
| MILK | −3,092 | −2,034 | 386 → 479 | −11.98 → −5.68 |
| STRAWBERRY | −773 | −1,098 | 384 → 450 | −1.87 → −3.83 |

Rest of the basket: −369 / −378. The split is a proxy (level reconciles to −729 / +1,010, and it
under-reads TOPB by 2.4 k); bands, units and fill are measured.

## 3. The three channels

1. **WOOL abstention, +1,454.** 7.8 fewer wool units (−8.8 in d10–14); inventory −9.2, quote +13
   (d10–19), **+15.2 (d20–29)**. The band's late wool quote recovers (−0.42); the top tier's does
   not, and it sells 41 % more of it.
2. **MELON abstention, +551.** −11.4 units in d15–19, quote +2; the top tier dumps 160 melon units
   in d20–29 against the band's 74.
3. **MILK denial, −2,034 vs the band's −3,092.** We move milk to h11.5 and add volume; inventory
   +8.3, quote −17. TOPB milk is already flooded (quote 116 vs 141), so the push buys ~1 k less.

All three are **price effects of our own sell-mix abstention**. The gift half nearly doubles
(+1,099 → +2,005) while the denial half shrinks (−3,865 → −3,132): our abstention lands in the two
dear, late products the top tier is over-weighted in.

## 4. What flow181's top-tier weighting can and cannot fix

**Can:** price the abstention. The withdrawn wool/melon units come back as carrot (+39.9) and egg
(+20.6) — free against the band, ~2 k against the top tier. A top-tier rung makes the ES see that
cost; the fix is cheap — re-enter wool/melon late, or return the 125 units g300 moved h1→h18.

**Cannot:** (a) 0.9 k of an 8.4 k TOPB deficit — our own purse (+4,087) is the campaign; (b) gift
and denial ride the *same* price curve, so a non-adaptive seat cannot flood the band's milk and
leave the top tier's wool cheap; (c) d10–14, the melon-pot hole, stays untouched
(`2026-09-11-flow172-g300-live-anatomy.md` §4); (d) at n=20 the gate-field overfit of
`es-noise-floor-2026-09-05` applies — weight TOPB, judge elsewhere.
