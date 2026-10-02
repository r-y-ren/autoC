# LIVE-C63 loss anatomy — all 24 losses of the live file (flow172_g940 + tail pair)

2026-09-10. **LIVE-C63** = the complete ≥2300 pool of live sub 56140532 (63 games, 24 L /
39 W = 61.9 %; `S/livec/ids.txt`), pinned towns `S/band2100p/town_schedules.json`. Theta
`flow172_g940.npy` + `OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON` via `S/drainpin/on2b.py
--seed-base 777001 --seed-per-opponent`, ids.txt order; ledgers from
`scripts/replay_profile.py` accumulators over 126 replays. Supersedes the 4-board
`2026-09-10-livec-loss-anatomy.md`.

## 0. Reproduction and the seat

**126/126 rows byte-exact** vs `S/lossflip/g940pair_livec.csv` (all 9 columns); 126 games =
**62.7 % W** against the ladder's 61.9 %. **Correction to the 4-board doc:** seats are *not*
always identical — **8 of 63 boards** differ, and 107467747 (live −486) **flips W/L**
(+563 / −1,212). Tables collapse to seat 0: **23 L / 40 W**.

## 1. Day bands — the d10–14 hole is a flat tax, the separator is d15–29

Revenue gap *ours − theirs*, mean ± SE, Welch t:

| band | LOSS (n=23) | WIN (n=40) | t |
|---|---|---|---|
| d0–9 | +1,199 ± 121 | +848 ± 161 | 1.75 |
| d10–14 | **−22,206 ± 389** | **−21,991 ± 302** | **−0.44** |
| d15–29 | +15,911 ± 904 | +28,341 ± 1,057 | **−8.94** |
| final margin | −4,496 ± 725 | +7,680 ± 1,030 | −9.67 |

d10–14 is the same −22 k either way — a flat tax, as TOPB records
(`2026-09-10-topb-loss-anatomy-g1000.md` §2). All 12,430 of the separation is d15–29:
**our purse 7,753 (62 %)**, theirs 4,677 (38 %).

## 2. Product × band — only two buckets are statistically separated

Gap (ours − theirs); of 27 product×band buckets only two clear |t| > 2 at n = 23/40.
`dOURS`/`dTHEIRS` = win-mean − loss-mean of each *level*.

| bucket | LOSS gap | WIN gap | t | dOURS | dTHEIRS |
|---|---|---|---|---|---|
| **WOOL d15–29** | −2,130 | +4,776 | **−3.98** | +11,827 | +4,921 |
| **TOMATO d15–29** | +831 | +5,640 | **−3.72** | +4,898 | +90 |
| MELON d10–14 | −17,440 | −17,374 | −1.00 | 0 | −66 |
| FERTILIZER (all) | −7,401 | −6,977 | −0.61 | +256 | −167 |

Melon is identical to the coin either way (we sell 87 u @ 162, d50 = 23; they 72 u @ 242,
d50 = 10) — a board-invariant tax. **Fertiliser is level**, so the 4-board "−7.9 k
displacement" is a constant, already closed as an income-line artifact
(`2026-09-09-fertilizer.md`: our 179 applications net **+16,815**). Units: wool 103 u @ 124
(L) vs 147 u @ 169 (W); tomato 7 u vs 38 u.

## 3. Do the 24 losses cluster? Yes — by the **town draw**, and not before day 10

Every board: 8 shops, 12 opponent melon tiles, 11 opponent hands, 3 quadrants — one clone
population; only the shop *mix* varies.

| board feature | LOSS | WIN | t | r with margin |
|---|---|---|---|---|
| towncons_TOMATO | 170 | 270 | **−3.71** | +0.29 |
| towncons_STRAWBERRY | 495 | 425 | **+2.39** | **−0.36** |
| towncons_WOOL | 180 | 255 | −1.65 | +0.26 |
| **our cash d9** | **6,165** | **6,163** | **0.01** | −0.07 |

Milk sink 391 vs 307 (t 2.36) and opponent rating 2,508 vs 2,474 (t 2.00) also tilt.
**No pre-day-10 feature predicts the loss:** best AUC(loss > win) is opponent rating 0.623,
their d9 cash 0.610, our d0–9 gap 0.589, our d9 cash **0.521**. A town-only least squares
(4 sinks) reaches R² = 0.28, right sign on 48/63 — real but weak. Losses are
*strawberry/milk-rich, tomato/wool-poor* towns, richer for **both** seats (straw d15–29: ours
36.6 k / theirs 33.0 k on losses vs 30.2 k / 26.1 k on wins).

**This disqualifies most of §2.** Our volume tracks the sink mechanically: r(wool sink, our
wool units) = **0.89**, r(tomato sink, our tomato units) = **0.79**, while their wool units
are flat at 180/183 (t −0.30). Regress our output on the sink and split the residuals:
tomato units t −1.21, tomato d15–29 revenue t −0.52 — **tomato is the town, not us**. Wool
*units* go level too (t −1.27); only wool **revenue at constant units** survives: −2,728 (L)
vs +1,568 (W), **t −2.40**.

## 4. Largest recoverable bucket

**Wool price in d15–29, ≈ 4.3 k/board** (sink-residual revenue at equal units; raw bucket
6.9 k, ~2.6 k of it the town). Two-purse: **own purse 70 %** (dOURS +11,827 vs dTHEIRS
+4,921) — they sell the same 180 units either way, so this is realisation, not denial. Our
wool median sell-day is 17.3 in both groups, so not timing drift; the loss boards' d20 wool
quote is 69 vs 104 — the same lot meets a shallower shelf.

**Archive: the turn and day halves are closed, the price half is not.**
`2026-09-10-verdicts.txt` 10:37Z `WOOL_FIRST_LOT_ON` (turn) — TOPB −17, LIVE55 89.1→81.8 %.
10:45Z/10:48Z `WOOL_SINK_HOLD_ON` (day) is a **no-op**: wool's hold decodes 0–87 against a
160–200 marginal, so the reservation never refuses. Sheep count is the `animal_want` gene
(`2026-09-09-herd-composition.md` Q1), a closed hand family. **Untouched:** splitting one wool
lot across two days when the sink is thin — neither lever expresses it.

**Smallest paired experiment:** `WOOL_SPLIT_CAP` — cap wool units per sell row at
`ceil(sink_units_per_day · k)`, carry the surplus to the next day (one clamp beside
`_sell_hold`'s `FERT_FLOOR` clause, `plan.py:3910-3917`; OFF byte-identical). Judge on the
**29 thin-wool boards** (towncons_WOOL ≤ 180, 11 L / 18 W), both seats, paired vs `g940pair`
at 777001 — 58 games, ~6 min. Bar: ALL Δmargin > 0, t ≥ 2, no board dropped; then all 63.
