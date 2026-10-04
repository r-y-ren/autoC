# Endgame defects across boards: starvation and the unsold end-state

Follow-up to `docs/strategy/2026-09-14-episode-108806196-close-loss.md` s7 items 1-2 (three sheep
starved at d28h23; ~687 coins of unsold end-state): how often, how expensive, what mechanism.

## Source

The judge legs keep **no per-game replays** (`grep -rl "starv\|end_state"` over `S/livec S/topb2
S/lossflip S/nexthigh S/nextband` returns nothing - only per-board coin CSVs), so these counts are from the **sim**. `S/endgame/endgame_probe.py` (new) reuses the `S/simscreen/screen.py` /
`S/melon_decomp/ledger.py` construction verbatim: theta
`artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (= B) + the shipped hr switch string, action-replay opponent seat, pinned recorded town, `shop_crn` on. Nothing under `src/` is touched - three
counter columns are bolted onto the sim `State`, and `eod.refresh_animals` is wrapped with an
exact copy of its own escape test. Boards: the first **40** of `S/simscreen/boards.json` = 20
LIVE-C hold-out tapes x both seats x first seed. Raw `S/endgame/raw_B.npz`, tables
`S/endgame/report.py`. On pinned-town tapes the sim is the engine to ~99.5 % (`sim-equals-engine-2026-09-06`); these are still not paired engine legs.

## 1. Starved animals (40 boards, B in the non-tape seat)

| | B | the tape seats (same 40 games) |
|---|---:|---:|
| boards with >= 1 escape | **40 / 40 (100 %)** | 2 / 40 (5 %) |
| animals lost per board, mean / max | **5.80 / 15** | 0.10 / 2 |
| total animals lost | 232 | 4 |
| animals alive at eod 28, mean | 11.90 | 16.90 |
| final money, mean | 107,142 | 102,733 |

Escapes by day (B, pooled; day 29 has no end-of-day, so none can happen there): d18 2, d20 8,
d21 16, d22 2, d23 12, d26 8, d27 66, **d28 118**. 79 % of escapes are on d27-d28, where `keep_val` is one or two nights of production (mechanism 1).
The 40 on d18-d26 are the ones worth a second look: those animals were refused their wheat with
3-11 days left. Animals fed per day (B) d24-d28: 13.00 / 14.88 / 12.10 / 11.65 / 5.53, against the
tape seats' 13.40 / 15.20 / 17.00 / 16.90 / 8.70.

## 2. Unsold end-state (valued at the board's own final quote)

| | B | the tape seats |
|---|---:|---:|
| boards with any unsold value | **40 / 40** | 4 / 40 |
| coins per board, mean / median / max | **426 / 343 / 1,426** | 10 / 0 / 195 |
| boards over 500 coins | 14 / 40 | 0 / 40 |
| of which standing mature crops | 385 | 0 |
| of which shed + in-hand stock | 41 | 10 |

Composition per board (B, mean). The shed/in-hand 41 coins are **6.80 FERTILIZER units** and
nothing else, on every board:

| standing | WHEAT | CARROT | TOMATO | STRAWBERRY |
|---|---:|---:|---:|---:|
| tiles | 2.3 | 0.3 | 2.4 | 2.0 |
| mature units | 4.95 | 0.80 | 0.80 | 0.20 |
| coins | 196.6 | 26.7 | 139.7 | 22.1 |

426 coins a board is ~10 % of B's mean margin on this set (+4,409). The 687 coins of the
episode-108806196 loss is the 91st percentile of this distribution, not an outlier. Escapes and
unsold value are close to uncorrelated across boards (r = 0.17), i.e. two independent defects.

Fertilizer is the **only** product left in the shed, and it is left on every board: the terminal
liquidation does sell the whole dawn-of-29 shed (`hold = LIQUIDATE`, `avail = view.shed`), which
is why wheat, eggs and milk end at zero. `eod.refresh_animals` re-arms `t_favail = 1` on every
alive animal at every end of day (`src/kagg3/sim/eod.py:143`), so at dawn on day 29 each of B's
~11.9 survivors carries a collectible unit and the route reaches 6.8 of them - collected after the
dawn allocation and offered by no row of the day.

## Mechanism 1 - starvation is a priced decision, not a defect

`plan.py:5087` `feed_want = has_animal & (t_water == 0) & (must_feed | bank_feed
| care_ok)`, then the value test (`plan.py:5132-5139`): `feed_value =
where(must_feed, keep_val + bank_val, bank_val) + care_val`, `feed_price` = the
hour-0 wheat quote for shed wheat or the buy-curve price for bought wheat,
`feed_pass = feed_want & (feed_value > feed_price)`. `keep_val`
(`plan.py:5120-5124`) is the animal's remaining production over the horizon,
minus the stock it holds today (harvested whether or not it is fed), capped at
`spec.ANIMAL_COST`. `plan.py:5092-5095` states the rule in the open: *"Feeding
as a value decision [EXACT-OPT, 1.4] ... One that fails is left to escape and
(0.8) not replaced."* `tests/test_feed_value.py:87`
(`test_a_worthless_animal_is_left_to_escape_and_not_replaced`) pins it.

Two horizon terms make late feeds fail it. `survival_pays = day < VAL.pay_day()` (`plan.py:4952`;
`pay_day()` = 29 under `HORIZON_DROP_ON`) zeroes `must_feed` / `care_ok` / `fires_tonight` on day
29 (`plan.py:5045-5046, 5086`); and on day 28 `keep_val` is one night of production at most while
`care_val` is 0 whenever `care_price > price[I_WHEAT]` fails (`plan.py:5085`). On the loss board
wool sat at the price floor of 1 from d17 against wheat at ~43, so that d28 feed bought ~1-3 coins
with a 43-coin wheat unit; the ration line `want_feed = feed_pass & (feed_rank < wheat_avail)`
(`plan.py:5486`, `tests/test_feed_rationing.py`) can only narrow the set further. So the three
starved sheep are a priced refusal, not a missed op. **No fix is proposed for defect 1.**
UNVERIFIED: whether an escape destroys *held* units (`eod.refresh_animals` zeroes `t_yield` on
escape, `sim/eod.py:139`) the route failed to harvest - a real loss the probe cannot separate from
a clean escape - and whether the 40 d18-d26 escapes are that same priced refusal.

## Mechanism 2 - the terminal day cannot sell what it collects

`terminal = day > O.LAST_SHED_DAY` (`plan.py:5950`) is day 29, and the sale draws on the **hour-0
shed alone**: `avail = view.shed[:N_PRODUCTS]` with every reservation void, `hold =
where(terminal, SELL.LIQUIDATE, macro.hold)` (`plan.py:6602-6624`), under the comment *"Shed
contents only: the day's harvest reaches the shed at end-of-day and is sold tomorrow morning, so
the hour-0 stock is exactly what the lots can draw on."* Day 29 has no tomorrow, so `DROP_ON` tops
lot 3 up with what the route banks (`plan.py:6720-6740`): `banked = where(covered & has_harv,
t_yield + 2*h_water, 0)`, `gain = where(drop_day, sum(oh*banked), 0)`, `lots += last_lot * gain`.
Two holes follow:

1. **Collected fertilizer is never offered.** `gain` reads `has_harv` = `OP_HARVEST` only;
   `has_coll` = `OP_COLLECT_FERT` (`plan.py:6654`) feeds the shed-overflow projection and nothing
   else. The one switch that puts collected fertilizer on a sell row, `SAME_DAY_FERT_ON`
   (`plan.py:6801-6819`), is **off** in the shipped hr string and gated `fert_day = (~terminal) &
   ...` (`plan.py:6404`) anyway. Yet `v_collect = price[I_FERT]` (`plan.py:5697`) still pays a
   day-29 COLLECT full price at admission, so the planner spends terminal turns collecting units
   no row of the day can sell.
2. **Standing mature crops.** The terminal crew must be home for the DROP: `turn_budget =
   SELL_TURNS[-1] + 1 - route_base` (`plan.py:6191`, ending at turn 19 instead of 24) and `labour
   -= n_units * EST_HOME` (`plan.py:6455`). Tiles the shortened routes miss keep their yield and
   are worth zero.

`tests/test_day29_endgame.py` owns this law (`:196`, `:143`).

## Proposed minimal fixes (NOT implemented)

**A. `TERMINAL_COLLECT_OFF` - stop buying unsellable fertilizer.** One clause: `v_collect =
where(terminal, 0, price[I_FERT])` (`plan.py:5697`), or `want_collect &= ~terminal`
(`plan.py:5140`), which also frees the pickup. A day-29 COLLECT then bids 0 at admission and
`_admit` spends the turn on the best remaining task - normally the deadline harvest the shortened
route dropped. Arithmetic: **6.8 unsellable collections a board**, so up to 6.8 turns freed; each
is worth the task it replaces, and B leaves 4.95 mature wheat units (196.6 coins) and 0.8 tomato
(139.7) standing. Expected **0 to ~+150 coins/board**, floor zero (the turn may buy nothing). NOT
additive - it re-allocates labour, so it must be measured paired. Test:
`tests/test_day29_endgame.py` (terminal admission) plus `tests/test_fert_carry.py` to pin that
earlier days do not move.

**B. `TERMINAL_FERT_ROW_ON` - offer the day-29 collection on lot 3.** Extend the `DROP_ON` top-up
at `plan.py:6737` with `gain[I_FERT] += sum(covered & has_coll)`, built exactly as
`SAME_DAY_FERT_ON` builds `sf_units` (`plan.py:6815`). Over-asking is free (every SELL is clipped
to the shed unit by unit in engine and sim), so a board that collects nothing cannot lose a coin.
Arithmetic: **+41 coins/board** (6.8 units x mean final quote 6.1) on 40/40 boards, zero
displacement - no turn moves. The smaller prize but the strictly additive one; A and B are
alternatives on the same 6.8 collections, not a stack. Test: `tests/test_day29_endgame.py` (a
day-29 view with a collecting animal must emit a FERTILIZER quantity on the lot-3 row);
`tests/test_drop_op.py` covers the DROP chain it rides on.

**C. The standing-crop residue (larger, NOT proposed).** Cost of leaving it: **385 coins a board**
(wheat 197, tomato 140) = 8.7 % of B's mean margin here. It is a *labour* shortfall: the terminal
budget ends at turn 19 and every unit is charged `EST_HOME`, so every fix re-allocates labour
(more day-29 hands, or a per-block return leg instead of a crew-wide one) and carries displacement
- the failure `MIDDAY_DROP_ON`'s post-mortem records (`plan.py:355-378`, -1,157/game). Cheapest
probe first: whether the day-29 hire enumeration is money-bound, since terminal coins are worth
nothing and a hand that lands one wheat harvest pays its fib bill.

## Status

FACT: the code mechanisms and citations above, and the probe counts. UNVERIFIED: every coin figure
is a mark-to-final-price valuation of an end state, not a realisable counterfactual; no paired
engine leg was run; 20 LIVE-C hold-out tapes are not the promotion sets.