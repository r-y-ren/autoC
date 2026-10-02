# DAWNSELL — the engine's sell-order rule, and what the dawn row is actually worth

2026-09-17, branch `dawnsell`, `S/dawnsell/`. **Real engine, not a model.** `S/dawnsell/tools/trace.py`
rebinds `kaggriculture._process_market` / `_commit_unit` in the worker (the `town_inject` technique;
nothing under site-packages is edited) and records every COMMITTED sell unit — seat, day, hour,
product, price — plus the dawn shed/hand stock and the market inventory quoted at the top of every
step. 44 ENG22 board-seats (22 fertilizer-engine tapes × 2 seats), pinned towns, shipped FT2 theta
and the 6 shipped switches. **Fidelity: bit-exact.** 107465299 reads 94,322 / 85,190 (seat 0) and
94,336 / 85,190 (seat 1) — the same coins as `S/lossflip/ft2_eng22.csv`, so the instrumentation does
not perturb the game. Rows: `S/dawnsell/rows/prize.txt`, `rows/tr/*.npz`, `rows/trace.log`.

Hour convention here is the **engine step index** (`step % 24`), not the replay's recorded hour
(= step + 1). `plan.py`'s comments use the recorded hour, so "our lot 1 at recorded hour 2" is
step/hour **1** below.

## 1. Q1 — THE ORDER RULE: order-SLOT, never seat

`kaggriculture.py:544 _process_market` — *"Per-unit lockstep: at each step, quote both players'
current-unit prices, then commit both."*

* Each seat's `action["market"]` list is truncated to `maxMarketOrdersPerTurn` = 10 (`:551`, `:557`).
* The outer loop walks **order-slot index** `i` (`:562`), taking slot `i` of BOTH seats together.
* HIRE / BUY_LAND are atomic and handled first, in player order (`:571-580`).
* Then the per-unit lockstep (`:583-628`): `quoted = [None, None]`; each live order's *next unit* is
  priced at `market_price(item, market["inventory"][item])` — the **same pre-commit inventory for
  both seats** (`:612` says so in the source) — and only then are both committed in player order
  (`:614-622`). `_commit_unit` (`:652`) adds the coin at the already-fixed price and raises supply by
  1 (`:657`, and not at all if the price hit `PRICE_FLOOR`).
* So within one order slot the quote moves **once per unit index, by the two seats' units combined**;
  `_refresh_prices` (`:629`) only rewrites the published `prices` dict afterwards.

Driven directly on a hand-built two-seat state (`S/dawnsell/tools/orderprobe.py`, WHEAT, virgin
market, solo unit prices 25,24,24,24,24,24,23,23):

| case | seat 0 | seat 1 |
|---|--:|--:|
| seat 0 sells 4, seat 1 idle | **97** | 0 |
| seat 1 sells 4, seat 0 idle | 0 | **97** |
| **both sell 4 in the same slot** | **96** | **96** |
| seat 0 sells all 8 alone | 191 | 0 |
| seat 0 slot 0, seat 1 slot 1 | **97** | 94 |
| seat 1 slot 0, seat 0 slot 1 | 94 | **97** |

**Simultaneous at one quote, seat-symmetric to the coin.** Two seats in the same slot split the curve
evenly (96/96); the 8-unit pot is 192 split vs 191 solo, i.e. splitting *helps* the pair by one coin
because both see each unit index's quote. The only thing that makes one player "first" is standing in
an **earlier order slot or an earlier turn** — and which seat sits there is irrelevant (rows 5 and 6
are mirror images). This is `plan.py:3169ff`'s reading of the engine, confirmed against the engine.

## 2. Q2 — the dawn census (44 board-seats, per board-seat means)

| | stock @h0 (u) | units sold | h0-1 u | h0-1 % | c/u h0-1 | c/u h2+ | already held @h0 % |
|---|--:|--:|--:|--:|--:|--:|--:|
| **ours (FT2)** | 54.8 | 1,414.5 | 826.4 | **58.4 %** | 69.1 | 120.2 | **90.2 %** |
| **theirs (engine class)** | 45.9 | 1,546.7 | 793.5 | **51.3 %** | 75.8 | 99.4 | **65.2 %** |

First sale hour of a selling day: **ours mean 1.05, median 1** (99.1 % of our selling days open in
h0-1); **theirs mean 1.34, median 0** (86.7 %). Like-for-like within a (day, product) that the seat
sold in both windows: ours h0-1 63.23 c/u vs h2+ 53.97 (**+9.26**), theirs 74.58 vs 77.41 (−2.83).
Per product the two dawn-dominated lines are FERTILIZER (ours 99.1 % of units in h0-1 vs their 48 %)
and MELON (99.5 % vs 27.4 %); the two we hold back are MILK (24.2 % vs 35.5 %) and STRAWBERRY
(26.6 % vs 60.6 %) — the steep curves, where our h2+ price is far above our h0-1 price (151.7 vs 87.6
strawberry, 132.5 vs 105.8 milk).

Two corrections to the record. (a) SELLRACE read our first legal market row as engine hour 2 and
their h0-1 share as 23.7 %; measured on the engine it is hour **1** for us and **51.3 %** of their
*committed* units in h0-1 on this engine-class set (SELLRACE counted units *ordered* across 82 tapes
of three legs, a different and wider population). (b) We are **not** behind the field at dawn: we
already put a larger share of our volume in h0-1 than they do.

## 3. Q3 — pricing the prize (two-purse, coins per board-seat)

Every counterfactual reprices the same units of the same (board, day, product) on the engine's own
curve (`market_price`, `:192`) walked from `MINV[day*24]`, the inventory the engine quoted at the top
of hour 0. Because the anchor is common, **the day pot is exactly invariant to order** — `d_ours` is
`−d_theirs` to the coin in every row, so these are pure transfers, not pot changes.

| order | Δours | Δtheirs | **Δmargin** | t |
|---|--:|--:|--:|--:|
| OURS1 — all our units in front of all of theirs | +6,639 | −6,639 | **+13,278** | 11.7 |
| OURS1F — only what we already held at dawn moves up | +6,274 | −6,274 | +12,547 | 11.4 |
| REACH0 — their hour-0 block stays in front (reachable) | +2,165 | −2,165 | **+4,330** | 7.2 |
| **H1TOH0 — our existing hour-1 lot moves one hour earlier** | +2,013 | −2,013 | **+4,025** | 9.9 |
| REACH — their whole h0-1 block stays in front | +954 | −954 | +1,907 | 3.8 |
| THEM1 — the mirror, they take the whole front | −4,756 | +4,756 | −9,511 | −8.7 |

**Seat split: there is none.** OURS1 margin is +12,606 ± 1,590 when our seat id is 0 and
+13,951 ± 1,639 when it is 1 — one standard error apart, and §1 shows seat is not in the rule at all.
The reachable fraction is therefore identical in both seats: what gates it is the **row**, not the
seat. Of the +13,278 gross, only the +4,025 H1TOH0 row (30 %) is a move our day layout could make.

**And it is already paid for.** The same reprice measures the **day-tick premium** — actual season
revenue minus the same units repriced off the dawn shelf — at **ours +11,389 / theirs +6,977** per
board-seat. Selling later, into a shelf the town has drained, is worth roughly 2.8× the whole H1TOH0
transfer, and we collect more of it than they do. That is the mechanism `plan.py:3169ff` calls
"WHY TURN 0 IS NOT FREE": `_town_consume` (`:727-748`) fires *after* each step's market, and at step 0
both the once-a-day town centre and a shop tick bite, so turn 0's market is quoted off a shelf one
full day-tick **fuller** — a cheaper quote for a seller. The zero-row modes were measured in the real
engine on 2026-09-03: **Z −4,658/game, t −2.76** (ours −5,553 against theirs −894, and not one of four
legs positive), **Z1 −773, t −0.64**; `A0` (lot 1 packed behind turn 0's hires) measured LEVEL
(2026-09-17-sellrace.md §2). The +4,025 gross transfer is real; the net has been paid and lost.

## 4. Q4 — what would have to change, and what blocks it

Nothing about **late harvest** and nothing about a **cash buffer**: 90.2 % of the units we sell on a
day were already in the shed or a hand's inventory at the top of hour 0 (`_end_of_day` →
`_drop_inventories_to_shed`), against their 65.2 %, and a SELL never needs cash. The one thing that
would have to change is the **row layout of turn 0** — our lot would have to stand on turn 0 instead
of turn 1, which means giving up turn 0's hire row and accepting a later crew floor. Concretely the
blockers are: `src/kagg3/core/ops.py:108` `TURN_HIRE = 0` and `:120` `TURN_HIRE_WIDE = 2` (turn 0 is
the hire row, and `_process_market` truncates a seat's queue to 10 slots a turn, `kaggriculture.py:551`,
so a full hire row leaves nothing for the lot); `ops.py:109` `TURN_BUY = 1` with `:159`
`EARLY_SELL_LOT1_TURN = TURN_BUY`, which is what puts lot 1 on hour 1 today; `ops.py:126`
`SELL_TURNS = (3, 10, 18)`, the fallback rows a lot falls back to when `plan._market`'s `fits` test
fails; `ops.py:204` `FULL_MARKET_TURNS = 3` with the assert at `ops.py:270`
(`max(HIRE_TURNS) < FULL_MARKET_TURNS <= min(SELL_TURNS)`); and `ops.py:217` `ROUTE_BASE = 2` under
the assert at `ops.py:272` (`ROUTE_BASE == TURN_BUY + 1`, "a hand hired in turn t first acts in turn
t+1") — the crew-floor law that a turn-0 lot pushes out, already parameterised as `ops.py:247-248`
`ROUTE_BASE_Z = 2` / `ROUTE_BASE_Z_LATE = 3`. On the plan side the switch already exists:
`plan.py:3300` `EARLY_SELL_ON = True`, `plan.py:3303` `EARLY_SELL_MODE = "A"` with `"A0"`, `"Z"` and
`"Z1"` (`plan.py:3306-3312`) as the turn-0 variants, and `plan.py:2367` `BANK_BEFORE_LOT_ON` as the
only mid-day path that adds today's harvest to a later lot. So no new mechanism is needed — the lever
is one string, and every setting of it has been judged on the real engine and lost.

## 5. §115b
The reachable transfer is **+4,025 a board gross (t 9.9)**, but it is bought by forfeiting the
day-tick premium we currently collect (+11,389 ours per board-seat), and the two engine arms that buy
it read −4,658 (Z) and −773 (Z1). **No arm.** The dawn/order axis is closed for the same reason
SELLRACE closed it, now with the engine's own order rule and the seat question answered: the rule is
slot-based and seat-symmetric, so there is no seat-conditional gene to cut either.

Repro: `python S/dawnsell/tools/orderprobe.py` ;
`KAGG3_TOWN_SCHEDULE=S/eng22/town_schedules.json PYTHONPATH=src python S/dawnsell/tools/trace.py S/dawnsell/rows/tr 44 4` ;
`python S/dawnsell/tools/prize.py S/dawnsell/rows/tr`.
