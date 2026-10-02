"""kagg2's measured market flow: what the real opponent puts on the market.

Why this exists
---------------
The ladder's `kagg2_proxy` rung reproduces kagg2's *opening* -- the melon race,
the two-quadrant dawn -- because it is a zero-theta preset of our own planner.
It does not reproduce kagg2's **supply mix**, and the supply mix is what sets
the quotes the policy is actually optimising against. Measured over the same
64 games (`~/scratch_price/price_sum.txt`), per game:

                     proxy rung        real kagg2
      MILK              78                256
      STRAWBERRY        71                245
      WOOL             140                155
      FERTILIZER       377                254
      EGG               92                  0
      WHEAT           -290 (net buyer)    sells 658, buys 595
      MELON             --                120 (72 u on d10, 33 u on d17)
      CARROT / TOMATO   --                  0

Milk and strawberry alone are 83% of the real-engine coin loss, so the gradient
is blind exactly where the money is, and a higher in-sim score has been
transferring *worse* (148,482 in sim -> -3.8k real; 150,085 -> -12.9k).

The fix here is not to fit a planner that behaves like kagg2 -- that is the
proxy rung, and it has been tried -- but to stop simulating the opponent's
market presence at all and replay the measured one instead. `sim.market.
apply_flow` walks these two tables against the live quote curve on each day, so
the *price path* the policy meets is kagg2's, unit for unit, whatever the rung's
own planner is doing on its board.

Provenance
----------
* Source games: 64 paired real-engine games (32 seeds x 2 seats), seed base
  **20260825**, our `artifacts/feed2/best_abs.npy` theta vs
  `~/scratch_gap/kagg2_main.py`, engine tree `~/scratch_plant_base`.
* Traced by `~/scratch_flow/flow_trace.py`, which is
  `~/scratch_gap/floor_trace.py`'s in-process `_commit_unit` hook with the
  commit bucketed by `step // 24` as well as by (player, op, item), so it is
  the same games those two files already describe -- the mean final-money
  margin reproduces at -4,127 and every per-product season total below matches
  `~/scratch_price/price_sum.txt` and `netprod.txt` to the unit.
* Table = mean units per day over the 64 games, rounded to int32. Rounding
  moves the season totals by at most 1.3 units in 1,700 (see `SELL_TOTALS`).
* Measured 2026-08-27.

Not a tape
----------
This table is a *centre*, not a script. Trained against verbatim, it would be
one more thing to overfit -- a policy that learns the day-10 melon dump to the
day is not a policy that beats kagg2, it is a policy that beats 2026-08-25's 64
seeds. `es.train.Trainer` therefore draws a **scale** (uniform in
`--kagg2-flow-scale`, default 0.5-1.5, one scalar per episode pair applied to
every product) and a **day shift** (uniform in +-`--kagg2-flow-jitter`, default
2 days, sliding the whole calendar) and hands them to `sim.market.apply_flow` in
its control word. The rung is then a family of kagg2-shaped opponents whose
*shape* is measured and whose level and timing are not.

The yardstick and the liveness probe deliberately run the centre (scale 1.0,
shift 0), so the reported number means the same thing in every run and in every
checkpoint, the way the fixed `abs_words` seed set does.

Only SELL and BUY_PRODUCT are here, and that is the whole of kagg2's market
footprint: in the engine (and in `sim.market.process_slot`) BUY_SEED and
BUY_ANIMAL are fixed-price orders that move the buyer's seeds/shed and its
money and never touch `market["inventory"]`, so they cannot move a quote. The
trace confirms the four ops kagg2 uses are SELL, BUY_PRODUCT, BUY_SEED and
BUY_ANIMAL; the last two are dropped here on purpose.
"""

from __future__ import annotations

import numpy as np

from .. import spec

#: Name of the ladder rung that plays this table; `--rung-weight` accepts it.
RUNG_NAME = "kagg2_flow"

_DAYS = spec.N_DAYS

# Rows are PRODUCTS order; transposed to [day, product] below.
_SELL_BY_PRODUCT = [
    # WHEAT
    [3, 0, 0, 0, 0, 18, 0, 0, 0, 7, 21, 0, 0, 8, 0, 8, 13, 29, 1, 46,
     23, 25, 51, 107, 23, 95, 36, 35, 20, 88],
    # CARROT
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 3, 2, 0, 4, 3],
    # TOMATO
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # STRAWBERRY
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 3, 5, 12, 11,
     8, 25, 31, 29, 21, 31, 12, 26, 17, 9],
    # MELON -- the day-10 dump is 60 units in one day and the whole melon race
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 12, 0, 0, 0, 0, 6, 33, 9, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # EGG -- kagg2 keeps no geese
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # MILK
    [0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 6, 6, 6, 9, 15, 9, 7, 21, 5,
     26, 8, 19, 6, 21, 6, 21, 6, 21, 27],
    # WOOL
    [0, 0, 0, 0, 0, 0, 12, 0, 0, 8, 0, 0, 0, 2, 12, 7, 3, 13, 4, 12,
     1, 11, 5, 13, 6, 12, 3, 13, 6, 12],
    # FERTILIZER
    [0, 3, 0, 4, 4, 5, 5, 6, 6, 9, 10, 0, 16, 14, 20, 5, 20, 11, 4, 20,
     3, 4, 13, 15, 8, 2, 19, 9, 11, 9],
]

_BUY_BY_PRODUCT = [
    # WHEAT -- bought as feed, and the churn is most of kagg2's wheat volume
    [8, 5, 4, 0, 6, 2, 6, 3, 16, 12, 33, 16, 10, 9, 16, 2, 9, 22, 11, 47,
     18, 19, 36, 92, 27, 97, 40, 23, 6, 0],
    # CARROT
    [0] * _DAYS,
    # TOMATO
    [0] * _DAYS,
    # STRAWBERRY
    [0] * _DAYS,
    # MELON
    [0] * _DAYS,
    # EGG
    [0] * _DAYS,
    # MILK
    [0] * _DAYS,
    # WOOL
    [0] * _DAYS,
    # FERTILIZER -- 0.02 u/game in the trace, which rounds away
    [0] * _DAYS,
]

#: int32 [N_DAYS, N_PRODUCTS]: units kagg2 SELLS on each day, mean over the 64
#: games. Day-major so a rollout's day index is the leading gather.
KAGG2_FLOW = np.asarray(_SELL_BY_PRODUCT, dtype=np.int32).T.copy()
#: int32 [N_DAYS, N_PRODUCTS]: units kagg2 BUYS (BUY_PRODUCT) on each day. Same
#: shape as the sell table because a buy is a sell with the walk reversed; every
#: column but WHEAT is zero.
KAGG2_BUY = np.asarray(_BUY_BY_PRODUCT, dtype=np.int32).T.copy()

assert KAGG2_FLOW.shape == (_DAYS, spec.N_PRODUCTS)
assert KAGG2_BUY.shape == (_DAYS, spec.N_PRODUCTS)

#: Season totals of the rounded tables, for the provenance check in
#: `tests/test_kagg2_flow.py`. The un-rounded measurements, per game, are
#: wheat 658.2 / 595.1, carrot 12.4, tomato 0, strawberry 245.2, melon 119.8,
#: egg 0, milk 255.7, wool 154.9, fertilizer 253.6.
SELL_TOTALS = tuple(int(x) for x in KAGG2_FLOW.sum(0))
BUY_TOTALS = tuple(int(x) for x in KAGG2_BUY.sum(0))

#: Longest single-day order in either table (wheat, day 23). The quote walk in
#: `sim.market.apply_flow` is sized off this, and it is bigger than
#: `state.MAX_UNITS_PER_ORDER` -- kagg2 reaches these day totals across several
#: of its own order slots, and the table folds them into one.
MAX_DAY_UNITS = int(max(KAGG2_FLOW.max(), KAGG2_BUY.max()))

#: What the table actually realised in those 64 games, mean coins per game:
#: 147,243 from the sells and 25,861 spent on the buys, for 121,382 net market
#: coins against a mean final money of 101,280. The rung's own money in sim is
#: whatever the walk realises against the live curve, not this -- these are here
#: as the number to sanity-check it against.
REALISED_SELL_COINS = 147_243
REALISED_BUY_COINS = 25_861
REALISED_FINAL_MONEY = 101_280
