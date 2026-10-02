# Front-running the opponent's late rows — observability, cadence, arithmetic, spec

2026-09-11.  Read-only design pass on B's one live discriminator.  Nothing under `src/`
changed (`git diff --stat src/` empty); the build is `S/oppsell/plan.patch`, not applied.

**The question.**  `2026-09-11-b-toptier-ledger.md` §54-55: B's only discriminator against
the top tier is the opponent's REALISED late price — their d15-29 basket clears at 65 c/u
on the boards we win and 81 on the boards we lose, at flat volume, and our own c/u is
higher than theirs in every late band.  `OPP_SUPPLY_ON` prices that fact and loses,
because it only SHRINKS our lots against a forecast.  The untested opposite: TIME our late
lots to land in front of theirs.

## 1. Observability — what our seat can actually see.  VERDICT: the DAY is observable, the
## HOUR is not, and neither is needed.

* `plan.DayView` carries `mkt_inv` int[9] — the shared market inventory — and `price`
  int[9], at **hour 0 only**.  `src/kagg3/core/plan.py:3807-3837` (the NamedTuple),
  filled by the simulator at `src/kagg3/sim/rollout.py:66-77` and by the submission at
  `src/kagg3/agent/parse.py:82-95` (`mkt_inv=parse_market(obs)[0]`).  One reading per day:
  the day's plan is built once at dawn (`agent/runtime.Runtime.act`, quoted at
  `plan.py:1269-1274`), so **no expression inside `build_day` can see an intraday price
  move**.
* `DayView.opp_commit` int[9] — the other seat's standing tiles per product, animals
  mapped through `spec.ANIMAL_PRODUCT` — is already there and already filled by both
  paths (`plan.py:1596-1615` `opp_commitment`, `agent/parse.py:97-118`
  `parse_opp_commit`; the engine observation seats `obs.farms` whole).  This is the
  product-level "which crops are theirs" signal, at no plumbing cost.
* **Their sales ARE inferable from the pot**, and the tree already does it once:
  `plan.py:1729-1733` (`open_pump_tell_keep0`) computes
  `theirs = spec.MARKET_I0 - mkt_inv[I_WHEAT] - OPEN_PUMP_UNITS` — the other seat's hour-0
  wheat draw, read straight off the inventory delta, because our own contribution is
  known.  The same arithmetic generalises: `mkt_inv` moves only by sales (+1 per unit
  priced above the floor, `sim/market.py::sell_walk`'s `adv`), buys (−1) and the town's
  deterministic tick (`sim/rollout.py:92-98`, `shops @ spec.SHOP_CONSUME` every
  `SHOP_SELL_INTERVAL = 4` steps plus `TOWN_CENTER_CONSUME` daily), and `view.shops` gives
  us the town term exactly.  So **their daily net units per product = Δmkt_inv + town
  drain − our own advancing units**, to the unit, except at the $1 floor where sales stop
  advancing inventory.
* What blocks that today is not observability but **state**: `build_day` is stateless per
  day and `DayView` has no yesterday.  A true per-day inference needs one optional field
  (`mkt_inv_prev`, defaulted like `opp_commit` is) plus four lines — one in
  `sim/state.py`, one in `sim/rollout.py::day_view`, one in `agent/parse.py`, one in
  `agent/runtime.py` to keep the last dawn's parse.  **Phase 2.**  Phase 1 needs none of
  it, because the cadence below turns out to need no per-board history at all.

**So: "opponent sold N units of crop X at hour h" is NOT inferable at runtime — h is
unobservable to the planner by construction.  "Opponent sold N units of crop X on day d"
is inferable to the unit with one new optional field.  "Crop X is theirs" is free today.**

## 2. Cadence — 6,383 opponent SELL rows, d15-29, 30 pinned tapes

`S/oppsell/cadence.md`, `cadence_rows.csv` (20 TOPB2 + the 10 fresh top-tier
1067968xx-1068038xx; `d,h = divmod(step, 24)`, `es/tape_actions.py:186`; mapping verified
two ways — 26 of 30 tapes put their biggest melon lot on day 10, and 106796826 decodes
d0h0/d0h1 verbatim as the T0a ledger's opening).

**There is no cadence to predict.**  All 30 tapes sell on all 15 late days — period 1, no
`k > 1` to fit — and use a median 23 of the 24 hours.  449 of 450 tape-days open with a
SELL in hours 0-2, in front of every turn we own (`ops.SELL_TURNS = (3, 10, 18)`; hours
0-2 are the HIRE/BUY rows, `FULL_MARKET_TURNS = 3`).  The best simple rule is the trivial
one: *"they sell before our turn 3, every late day"* — 449/450 = **99.8 %**, one rule for
all 30 tapes.

**But their day is not front-loaded, and that is the whole finding:**

| bucket | rows | units | share |
|---|---|---|---|
| h0-2 — before our lot 1 (t3) | 2,126 | 18,624 | 24.0 % |
| h3-9 — between lot 1 and lot 2 | 790 | 3,032 | 3.9 % |
| h10-17 — between lot 2 and lot 3 | 1,245 | 20,900 | 26.9 % |
| h18-23 — at or after our lot 3 | 2,222 | 35,157 | **45.2 %** |

172.7 u per tape-day; **131.3 u/day lands after our first lot and 78.1 u/day after our
last one.**  Per product (u/tape-day, h3-17 | h18-23+next h0-2): CARROT 22.9|6,
STRAWBERRY 17.5|12, WHEAT 4.3|16, MILK 3.3|21, WOOL 2.6|6, FERTILIZER 1.7|36, EGG 0.3|18,
TOMATO 0.1|3, MELON 0.3|1 — a scalar forecast would over-price EGG by the factor it
under-prices CARROT, which is why the spec carries two measured 9-vectors.

Caveat on the units: `mq` is the verbatim offered count (`es/tape_actions.py:158-160`),
so a row the engine clipped for want of stock counts whole (an upper bound, exactly
`OPP_SUPPLY`'s defect), and 488 end-of-season `q = 1000/100000` "sell the shed" sentinel
rows are excluded entirely, so the last days are under-counted.

## 3. Mechanism — the pot is a queue, and it never recovers

`mkt_inv` is a **monotone stock**.  A sale advances it once per unit priced above the
floor (`sim/market.py::sell_walk`'s `adv`); a buy and the town's tick subtract
(`sim/rollout.py:92-98`); **nothing ever pulls it back toward `I0`**.  Price is a pure
function of that stock (`spec.market_price`, `spec.build_price_table`).  So the only thing
that decides who gets a product's top rungs is who sells first, and "an hour before" and
"a day before" are nearly the same lever: the maximum town drain is 8-16 units per 4-turn
tick (`SHOP_CONSUME` at 8 instances) and far less on a real town.

The ladders are shallow — units above `I0` before the quote hits the $1 floor:

| | WOOL | STRAWBERRY | MILK | MELON | TOMATO | CARROT | FERT | WHEAT/EGG |
|---|---|---|---|---|---|---|---|---|
| depth | **59** | 62 | 76 | 158 | 529 | 842 | 493 | no floor |

One 40-unit lot is the entire WOOL curve (200 → 107 at 40 units, the figure `plan.py:1496`
already quotes).  Calibrated to the ledger's own realised prices (the inventory offset at
which a 40-unit lot averages the observed c/u): our d22-29 79 c/u sits at STRAWBERRY +2,
MILK +19, WOOL +25, MELON +111 above `I0`.  At those pots:

* **our 40 units first vs behind their 30**: STRAWBERRY 3,148 → 933 (**+2,215**),
  MILK 3,168 → 821 (**+2,347**), WOOL 3,219 → 94 (**+3,125**), MELON **+2,346**,
  TOMATO +144.  The loss is symmetric — their same 30 units lose exactly what we gain —
  so a matched product-day is worth **~4,400-6,300 of margin swing**.
* **priced on the measured buckets** (`coin_arith.txt` §7): moving our 40 units out of
  lot 3 into lot 1 gets us in front of their h3-17 injection — **+2,254 coins/day** summed
  over the eight products; selling today instead of carrying overnight gets us in front of
  their h18-23 + morning injection — **+4,120 coins/day**.
* **the target**: their 94.8k d15-29 revenue on the loss boards must fall to the 75.1k
  they take on the win boards — 16 c/u over ~1,171 units, **18.7k over 15 days = ~1,250
  coins/day of their revenue**.  One matched product-day of either half already exceeds
  that, so the lever does not need to fire often; it needs to fire without giving back
  more of ours than it takes of theirs.

## 4. Spec — `S/oppsell/plan.patch` (+163 lines, 2 hunks, plan.py only)

`git apply --check` passes; `py_compile` passes; helper smoke test in
`S/oppsell/helper_smoke.txt`.  Constants only — **no gene is appended**, so B's theta
decodes byte for byte and the `gene-slope-check` rule does not apply.  Genes are phase 3,
after a switch leg says the direction is real.

* `OPP_FRONTRUN_ON = False`, `OPP_FRONTRUN_FROM_DAY = 15`, `OPP_FRONTRUN_TURN = 18`,
  `OPP_FRONTRUN_MIN_COMMIT = 1`, `OPP_FRONTRUN_SCALE = 100` (percent, the dose).
* `OPP_FRONTRUN_DAY = (4, 23, 0, 18, 0, 0, 3, 3, 2)` — their h3-17 units per product per
  late day.  `opp_frontrun_inv` adds it to **the late lots only** (`turn >= 18`), gated on
  `view.opp_commit`, one line at the `SELL.lot_inventories` call site (`plan.py:6493`).
* `OPP_FRONTRUN_NIGHT = (16, 6, 3, 12, 1, 18, 21, 6, 36)` — their overnight units.
  `opp_frontrun_hold` charges the reservation `price(inv) − price(inv + NIGHT)` computed
  on today's real pot, applied after `_sell_hold` and never on the terminal day, one line
  at `plan.py:6479`.
* OFF returns the argument object itself in both helpers, so OFF allocates nothing and
  traces identically — the `open_pump_tell_keep0` pattern.

**Why this is not `OPP_SUPPLY_ON` re-run.**  That switch's own ledger says our coins fell
1,841 and *theirs rose 1,131*: it adds a cumulative forecast to **every** lot, lot 1
included, so the whole day's marginals sink, `sell.allocate`'s `best_adj` falls under
`hold`, and the unit is not moved forward — it is not sold.  Here lot 1's curve is
untouched, so `best_adj` is bounded below by the true lot-1 marginal and no unit that
would have sold today stops selling: **the allocation shifts instead of shrinking.**  It
also does the two things `plan.py:1497-1501` says a next attempt needs — the curve stops
at our last lot instead of carrying day 29's 779-unit liquidation, and it is per product
and gated on their actual board.

Test plan, arms, and the two-purse falsifier (`d_ours <= d_theirs` refuses): `S/oppsell/README.md`.

## 5. Honest risk

* **The literal lever in the brief is dead.**  "Land our lot just before theirs" cannot be
  done: they open every late day at hour 0-2 (449/450 tape-days) and our earliest sell
  turn is 3.  On **0 of 15 late days** does B have a sell turn strictly earlier than their
  modal hour.  If their supply were front-loaded this note would end here.
* What survives is the 76 % of their late units that land *after* our first lot, and the
  45 % that land after our last — a *within-our-own-lot-layout* ordering lever, not a
  race.  That is a weaker claim than the brief's and it should be read as one.
* Both halves are still a forecast, and a forecast is what killed `OPP_SUPPLY_ON`.  The
  DAY/NIGHT vectors are fitted on TOPB2 + the fresh ten, two of the three leg families;
  **LIVE-C H30/H30B are the only held-out read** and the promotion decision must rest on
  them.
* The hold cut is large on the steep products (the smoke test takes a 40-coin MILK
  reservation to 0 at a fresh pot).  A2/A3 can liquidate MILK and STRAWBERRY earlier than
  the theta intends; `SCALE=50` is the dose-response control, and a lever that only wins
  at half dose is a tuning artefact and is refused.
* Displacement is the standing prior: six hand levers and the whole wool and mix families
  died with this signature.  The two-purse split is not optional here.
