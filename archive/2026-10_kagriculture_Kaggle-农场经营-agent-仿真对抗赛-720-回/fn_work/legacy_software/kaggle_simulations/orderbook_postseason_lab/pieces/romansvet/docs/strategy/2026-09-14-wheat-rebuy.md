# 2026-09-14 — WHEAT-REBUY: is the top-five's market re-buy a lever?

**VERDICT: a buy/sell round trip through the shared pot is EXACTLY zero coins
— not "approximately price-neutral", zero, by construction of the quote walk —
so the re-buy is neither a denial lever nor a wash we are missing: it is a
no-op the top five happen to run.** The one thing a buy *can* do to the other
seat is the CROSS (`sim/market.py:717-747`), and there it **helps the opposing
seller** (their units clear at the undepressed quote instead of walking the
curve down), so as a denial lever it points backwards. Paired, both arms lose
(tables in §5). The wheat price gap the top-5 ledger flagged (their 37.4
against our 34.3) is worth **~550 coins on the 174 net units we sell** and is a
*lot-depth* fact, not a re-buy fact: they dribble ≤ 40-unit lots across 24
hours, we dump 60+ units into one lot and walk our own price down.

Sim, descriptive, paired, CRN, action-replay opponent seat, theta B =
`flow193_g100_hr`, shipped `hr` switches. No engine game, no training arm, no
ladder claim.

## 1. MECHANISM — how a wheat price moves (source)

| fact | source |
|---|---|
| one price array per TOWN, indexed by absolute market inventory; **both seats quote off the same `st.mkt_inv[item]`** | `sim/state.py:65`, `sim/state.py:139` (`mkt_inv = MARKET_I0 = 10000`), `sim/market.py:590`, `:684` |
| `price = 25 + sqrt(10000 - inv)` below `I0` for WHEAT (`base 25, T 400, below sqrt, target 0.80`); `25 - 0.83·ln(1+x)` above | `spec.py:111` (`_MARKET_ROWS`), `spec.py:154-169` (`market_price`) |
| a SELL walks the quote **up** the inventory (`off = +j`) — each unit sold is cheaper than the last; a BUY walks it **down** (`off = -1-j`) — each unit bought is dearer than the last | `sim/market.py:69-76` (`_quotes`) |
| a sold unit adds supply only if it priced above the $1 floor; a bought unit removes one whatever it cost | `sim/market.py:84-95` (`sell_walk`), `:535` |
| a buy stops at the first unit the purse cannot cover | `sim/market.py:97-103` (`buy_walk`) |
| BUY_PRODUCT is clipped to the shed room (`SHED_CAPACITY = 100`) slot by slot | `sim/market.py:666`, `spec.py:215` |
| the inventory **persists across hours and days**; the only exogenous mover is the town — every shop instance every 4 steps, the town centre every 24 | `sim/rollout.py:137-143` (`town_consume`), `spec.py:227-228`, `spec.py:192-203` |
| two orders interact only when both touch market inventory on the same item | `sim/market.py:14-17`, `:660-754` |
| **the cross**: one seat's SELL against the other's BUY in the same slot — the seller is paid `P(inv)` and the buyer charged `P(inv-1)` **every round, with the inventory returning to `inv`** | `sim/market.py:717-747` |
| wheat is also an INPUT: `OP_FEED` burns one unit per animal fed | `sim/units.py:120-121`, `:170` |

**Does a buy raise the price for later sellers?** Yes — within the day and
into the next day, because `mkt_inv` is never reset. **Does a sell depress it
for them?** Yes, symmetrically. **Is the pot shared between the two seats?**
Yes: one `mkt_inv[9]` per board.

**But a round trip is worth exactly nothing.** The buy pays the table entries
`P(inv-1) … P(inv-n)` and the sell-back receives `P(inv-n) … P(inv-1)` — the
same `n` integers. `S/rebuy/wash_check.py` (`S/rebuy/wash_check.log`) walks the
real table:

```
BUY n then SELL n back, nobody in between:
   inv 9856 n  20: pay    748 receive    748 net   +0
   inv 9856 n  40: pay   1510 receive   1510 net   +0
   inv 9856 n 100: pay   3888 receive   3888 net   +0
own 30 units sold with a 40-unit re-buy in front:  1092  (36.40/own unit)
own 30 units sold with no re-buy at all:           1092  (36.40/own unit)
```

Revenue depends only on the endpoints of the inventory path, so **no ordering
of one seat's own buys and sells changes that seat's coins**. Only two things
break the identity:

1. **Town drift.** Buy now, sell after the town has drained `C` units: worth
   `+0.20/unit` at `C = 4`, `+0.70/unit` at `C = 16` (wheat, inv 9856). A
   40-unit overnight carry is **+8 to +28 coins**.
2. **The cross.** Our BUY in the same slot as their SELL: their 40 units clear
   at `40 × P(inv) = 1480` instead of `1446` walking down (**+34 for them**),
   and our 40 cost `1480` instead of `1510` (**−30 for us**). Both seats gain;
   the pot pays. A buy is therefore a *gift* to a simultaneous seller, never a
   denial.

## 2. THE TAPE — what ymg_aq actually does (12 boards, `S/rebuy/analyze_tape.log`)

`S/macro_exec/extract.py` now extracts the purchase channel (`buy_target`,
`buy_hour`); `S/rebuy/analyze_tape.py` prices it off the CRN ledger
(`raw_headOFF.npz`, whose `buy_np/buy_cp/sold_np/sold_rp` are the coins that
actually changed hands).

Season, mean over the 12 ymg_aq boards:

| seat | wheat bought | paid | P_buy | wheat sold | received | P_sell | own units | net coins | per own unit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **ymg_aq** | 1,144.8 | 42,462 | **37.09** | 1,477.6 | 55,223 | **37.37** | 332.8 | +12,761 | **38.35** |
| **B (us)** | 140.8 | 4,683 | 33.25 | 314.7 | 10,801 | **34.33** | 173.9 | +6,118 | **35.20** |

The whole wheat-price gap is therefore worth `(38.35 − 35.20) × 174 ≈ 550`
coins a board — against a 38,000-coin end-of-season gap. *(Their 1,145 bought
units are not all churn: `OP_FEED` burns wheat, and a 17-head herd eats ~300
units a season. The rest is round trip.)*

## 3. TIMING — within-hour churn, not a carry and not feed

Per episode (six ymg_aq tapes, `artifacts/tape_actions_town/`):

| episode | `OP_FEED` (wheat eaten) | wheat bought | wheat sold | bought+sold in the SAME HOUR |
|---|---:|---:|---:|---:|
| 108790159 | 203 | 1,413 | 1,733 | 885 |
| 108806291 | 231 | 868 | 1,253 | 405 |
| 108807563 | 433 | 780 | 1,010 | 190 |
| 108814574 | 256 | 970 | 1,189 | 485 |
| 108820106 | 201 | 1,143 | 1,703 | 685 |
| 108826138 | 315 | 1,697 | 1,997 | 1,205 |
| **mean** | **273** | **1,145** | **1,481** | **642** |

So **872 of the 1,145 bought units are never eaten**, and **642 of them are
bought and sold back inside the same hour** — the two orders sit in different
slots of one market row (`sim/market.py` resolves slots in order, so the pair
is a solo buy walk followed by a solo sell walk down the same table entries).
This is not a cross-day carry (the overnight shed position is small) and not
input buying (feed is 273 units).

The hour structure, pooled over the six tapes (wheat units):

```
BUY  hours  0:55  1:33  2:57  3:26  4:150  6:30  7:29  8:94  9:31 10:69
           11:36 12:135 14:62 15:55 16:86 19:35 20:87 22:2  23:53
SELL hours  0:246 1:83  2:59  3:23  4:33  5:33  6:26  7:27  8:47  9:56
           10:70 11:46 12:61 13:55 14:69 15:58 16:10 17:92 19:53 21:194 23:67
```

Purchases cluster on **hours 4, 8, 12, 16, 20** — the `SHOP_SELL_INTERVAL = 4`
tick hours (`spec.py:227`) — and the sale of the same product follows one hour
later (buy 4:8 → sell 5:3, buy 8:19 → sell 9:1, …), a one-hour carry worth
+0.2/unit by §1's drift arithmetic, i.e. single-digit coins. Days 11-12 are the
extreme: 40 units bought and 40 sold in the *same hour*, six times a day.

**Nothing consumes the churned units.** Wheat is consumed only by `OP_FEED`
(`sim/units.py:120`), 273 units a season.

## 4. BUILD — two arms, both default off

* **`MACRO_MODE "rebuy"` (site 9)** — `plan.py:5887-5898`, inside
  `if MACRO_EXEC_ON and MACRO_SCHEDULE is not None:`; the schedule's
  `buy_target[day][WHEAT]` is a FLOOR on the day's turn-1 BUY row, applied by
  `plan._rebuy_extra` (`plan.py:4932`) with the engine's own two clips (shed
  room, purse-walked quotes). `macro_load` decodes the new key with a zero
  default, so the six existing modes read an all-zero row on an old JSON.
* **`REBUY_ON` / `REBUY_N` / `REBUY_DAYS` (default `False / 0 / (10, 25)`)** —
  `plan.py:4805-4821`, our own clock: `REBUY_N` extra wheat units on the same
  row, every day in the window. Nothing sells them explicitly; they sit in the
  shed overnight and tomorrow's `avail` (`plan.py:7103`, the dawn shed less the
  feed reservation) offers them to the lot allocator at the day's best lot.

**A `BUY_PRODUCT` action IS emittable** from the shipped action interface — the
turn-1 row already carries one (`plan.py:8437`). What is *not* emittable is the
tape's hour granularity (22 distinct buy hours against our turns 0/1/2 +
`SELL_TURNS`); see `S/rebuy/PATCH_NEEDED.md` for the smallest addition that
would buy one more hour, and why it cannot pay.

**Identity.** `S/macro_exec/extract.py` now writes `buy_target`/`buy_hour`
into `macro_ymg_aq*.json`; every pre-existing key is byte-unchanged, and
`plate0` re-run on the 12 ymg boards through the patched `plan.py` and the
updated JSON is **max |delta| = 0 over all 15 recorded arrays** against the
stored `raw_plate0.npz` — so site 9 and the new constants are inert on every
path that does not ask for them.

Tests: `tests/test_rebuy.py` (8, all pass) — OFF-tuple identity for the size
constant alone, the window, both engine clips, site 9's floor, an old schedule
decoding to an empty row, and `plate0` proven blind to the new key.
`tests/test_macro_exec.py` (29, all pass; one assertion extended to site 9).

## 5. PAIRED — both arms lose, and they PAY THE OPPONENT

Paired CRN, same boards, same seeds, same theta. OFF baselines are the stored
`raw_headOFF.npz` (12 ymg_aq) and `raw_melOFF.npz` (68 band).

### 12 ymg_aq boards

| arm | our coins Δ (t) | margin Δ (t) | THEIR coins Δ (t) | our wheat u @P | their wheat u @P | cash d10 / d15 | win % | flips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B (baseline) | 93,127 | −13,751 | 106,879 | 314.7 @ 34.33 | 1477.6 @ 37.37 | 6,032 / 7,376 | 0.0 | — |
| `rebuy20` | **−2,275** (−2.87) | **−2,113** (−3.31) | −162 (−0.60) | 434.8 @ 35.44 | 1478.0 @ 38.08 | 6,032 / 6,434 | 0.0 | 0 |
| `rebuy40` | **−2,544** (−2.93) | **−2,852** (−3.90) | +308 (+0.92) | 502.1 @ 35.89 | 1477.9 @ **38.32** | 6,032 / 6,294 | 0.0 | 0 |
| `MACRO_MODE rebuy` | **−2,404** (−3.21) | **−3,141** (−3.76) | +738 (+0.96) | 502.3 @ 36.31 | 1477.0 @ 38.13 | 5,922 / 7,138 | 0.0 | 0 |

### 68 band boards

| arm | our coins Δ (t) | margin Δ (t) | THEIR coins Δ (t) | our wheat u @P | their wheat u @P | cash d10 / d15 | win % | flips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B (baseline) | 104,092 | −192 | 104,284 | 322.0 @ 37.27 | 369.6 @ 38.45 | 5,803 / 7,759 | 42.6 | — |
| `rebuy20` | **−1,043** (−4.90) | **−1,560** (−6.24) | **+517** (+2.77) | 429.4 @ 38.39 | 369.5 @ 39.00 | 5,803 / 7,093 | 33.8 | 6, **all to them** |
| `rebuy40` | **−1,997** (−8.23) | **−3,811** (−13.44) | **+1,815** (+6.75) | 488.5 @ 38.77 | 369.6 @ **39.33** | 5,803 / 6,762 | 27.9 | 10, **all to them** |

**Δmargin is consistently worse than Δcoins**, and on the band the opponent's
coins rise with a t of +6.75. The re-buy raises *our* realised wheat price
(37.27 → 38.77) and *theirs too* (38.45 → 39.33) — a drained pot is a better
pot for every seller, and the seller who profits most is the one selling the
most units through it. It is a **subsidy to the opponent**, the exact opposite
of a denial lever.

## 6. ANATOMY — where the 2,544 coins go (`S/rebuy/anatomy_rebuy40.log`)

The market leg itself is, as §1 says, a wash: on the 12 ymg boards our own
wheat units net **+6,118 (B) → +6,271 (rebuy40)** — the whole season of extra
churn is worth **+153 coins** (the town drift and a few crossed slots), against
a −2,544 loss. The coins leave through the FARM:

| | B | rebuy40 |
|---|---:|---:|
| cash at dawn d15 | 7,376 | **6,294** |
| shed total at dawn d15 (cap 100) | 79.3 | **100.0** (full) |
| shed wheat at dawn d15 | 28.2 | **50.5** |
| animals at d15 | 17.1 | 16.2 |

Two costs, both structural:

1. **Shed crowding.** `SHED_CAPACITY` is 100 and the eod dump
   (`sim/eod.py:210` `drop_inventories`) is what puts a harvest into it. Half
   the shed is now wheat waiting to be re-sold, so the harvest that arrives
   that night has nowhere to go.
2. **Capital displacement.** 11,747 coins of wheat purchases (vs B's 4,683)
   pass through the same `budget.grant` purse that buys hands, seeds and
   animals; d15 cash is 1,082 coins lower and the d15 herd one head smaller.

## 7. VERDICT

* **Does the re-buy move the shared pot's price?** Yes — the pot is one
  `mkt_inv` per town and a buy raises the quote for everyone, that hour and the
  next day. But it moves it **for both seats**, and the opponent sells 1,478
  wheat units a season to our 315, so the price it buys is mostly *theirs*.
* **Is it a wash for the buyer?** Exactly, by construction: +0 coins on every
  round trip in the price table, +153 coins measured over a whole season of
  it. The top-5 ledger's "price-neutral churn" is a theorem, not a coincidence.
* **Is it a loss?** Yes, once the shed and the purse are charged: −1,043 to
  −2,544 coins a board, t −2.9 to −8.2, and −1,560 to −3,811 of margin.
* **Does it change the opponent's coins?** Yes, **upward** (+1,815, t +6.75 on
  the band). Δmargin < Δcoins on every arm; the lever is a gift.
* **Is the wheat price gap a lever at all?** The whole gap is worth ~550 coins
  a board (§2), and the half of it that is not "sell later, when the pot is
  thin" is **lot depth**: unit-weighted, ymg_aq clears **+0.99/unit above the
  dawn quote** and we clear **−0.51/unit below it**
  (`S/rebuy/depth_cost.log`) — they never put more than 40 units into one hour,
  and our day-29 liquidation puts 64.6 units into one lot at −3.82.

**Closed: the market-purchase channel.** The next wheat experiment worth
running is the depth one, not the purchase one: split our lot-1 volume across
`SELL_TURNS` (or add hours) so no single lot walks its own quote down. That is
`lot1/lot2/lot3`'s knob measured the other way and is bounded above by ~500
coins a board on wheat.
