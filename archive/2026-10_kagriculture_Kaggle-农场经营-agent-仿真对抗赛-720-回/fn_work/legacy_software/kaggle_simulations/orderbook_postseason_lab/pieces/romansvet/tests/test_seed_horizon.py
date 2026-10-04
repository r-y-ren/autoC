"""Sales-window pricing of purchase candidates (PLANNER_V3_1 section 1.3,
gap review 2026-08-24): a seed's units are priced at the inventory the town
will have drained to by the crop's first harvest day, plus the supply the
farm has already committed. Opponent-free by construction.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
from test_budget_order import _macro, _purse_view, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ
from kagg3.core import valuation as V

I0 = spec.MARKET_I0
ONES = np.ones(spec.N_SHOPS, np.int32)


def test_daily_town_units_is_six_shop_ticks_plus_the_centre():
    assert PJ.daily_town_units(np, np.zeros(spec.N_SHOPS, np.int32)).tolist() == [1] * 8 + [0]
    assert PJ.daily_town_units(np, ONES).tolist() == [31, 19, 13, 25, 1, 13, 19, 13, 0]


def test_inv_at_day_drains_per_product_and_takes_a_vector_of_days():
    inv = np.full(spec.N_PRODUCTS, I0, np.int32)
    assert int(PJ.inv_at_day(np, inv, ONES, np.int32(10))[spec.I_STRAWBERRY]) == I0 - 250
    days = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    out = PJ.inv_at_day(np, inv, ONES, days)
    assert out.tolist() == (I0 - days * np.array([31, 19, 13, 25, 1, 13, 19, 13, 0])).tolist()
    assert int(PJ.inv_at_day(np, inv, ONES, np.int32(20))[spec.I_FERT]) == I0     # no town demand


def test_remaining_plant_units_counts_only_future_fires():
    I = np.int32
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(0))) == 4    # fires 10, 12, 14, 16
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(11))) == 3   # 12, 14, 16 remain
    assert int(V.remaining_plant_units(np, I(spec.I_STRAWBERRY), I(0), I(20))) == 0
    assert int(V.remaining_plant_units(np, I(spec.I_WHEAT), I(0), I(3))) == 4         # unharvested until age 4
    for c in range(spec.N_CROPS):
        for d in (0, 9, 17, 25):
            assert int(V.remaining_plant_units(np, I(c), I(d), I(d))) == int(V.new_plant_units(np, I(c), I(d)))


def _seed_buys(view, macro):
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    return {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
            if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}


#: What reaches the budget walk. `_purse_view` puts the day's own overhead --
#: the fib bill of the crew 1.5 hires and the reserve it keeps for tomorrow's
#: (`plan.cash_reserve`) -- on top of it, so these numbers stay the seeds'.
PURSE = 1000


def test_the_towns_drain_prices_the_first_harvest_day():
    # one of each shop, blank board, day 0: strawberry's four units sell at
    # I0 - 250 (1,010 coins, ratio 10.1) and melon's six at I0 - 10 (1,611,
    # ratio 20.1) -- opponent-free, melon still ranks first on a fresh board
    macro = _macro(plant_target=np.array([0, 0, 0, 30, 30], np.int32))
    view = _purse_view(PURSE, macro, shape=lambda v: v._replace(shops=ONES))
    seeds = _seed_buys(view, macro)
    assert seeds.get(spec.I_MELON, 0) == 12 and seeds.get(spec.I_STRAWBERRY, 0) == 0


def _with_melon_pipeline(v):
    kind, occ = v.kind.copy(), v.occ.copy()
    kind[:25], occ[:25] = spec.KIND_PLANT, spec.I_MELON
    return v._replace(kind=kind, occ=occ, shops=ONES)


def test_own_pipeline_un_ranks_a_gluttable_crop():
    # the same board with 25 melon tiles already growing (150 units by day
    # 10): the next melon seed's six units sell at I0 + 140 for 282 coins
    # (ratio 3.5) and ten strawberries take the purse instead
    macro = _macro(plant_target=np.array([0, 0, 0, 30, 30], np.int32))
    view = _purse_view(PURSE, macro, shape=_with_melon_pipeline)
    seeds = _seed_buys(view, macro)
    assert seeds.get(spec.I_STRAWBERRY, 0) == 10 and seeds.get(spec.I_MELON, 0) == 0

    # ... and by the mechanism, not just the answer: the 25 tiles are the whole
    # of the 150-unit pipeline, and `inv_h` is the town-drained inventory at
    # melon's first harvest day (day 10, one melon a day) plus that pipeline.
    is_plant = view.kind == spec.KIND_PLANT
    has_animal = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE)) & (view.occ >= 0)
    pipe = P._pipeline_units(np, view, is_plant, has_animal, np.int32(0))
    assert int(pipe[spec.I_MELON]) == 25 * 6
    first = np.int32(spec.CROP_FIRST_YIELD_DAY[spec.I_MELON])
    inv_h = PJ.inv_at_day(np, view.mkt_inv, view.shops, first) + pipe
    assert int(inv_h[spec.I_MELON]) == I0 - 10 + 150


def test_pipeline_units_counts_tiles_animals_fert_and_the_shed():
    view = _view(0)
    kind, occ, t_day = view.kind.copy(), view.occ.copy(), view.t_day.copy()
    kind[:3], occ[:3] = spec.KIND_PLANT, spec.I_STRAWBERRY                 # 3 x 4 units
    kind[3], occ[3] = spec.KIND_COOP, 0                                      # a goose placed day 0
    shed = view.shed.copy()
    shed[spec.I_WOOL] = 7
    view = view._replace(kind=kind, occ=occ, t_day=t_day, shed=shed)
    is_plant = view.kind == spec.KIND_PLANT
    # `build_day`'s own predicate: `occ` carries the animal kind on a stocked
    # coop or pasture and -1 on an empty one.
    has_animal = ((view.kind == spec.KIND_COOP) | (view.kind == spec.KIND_PASTURE)) & (view.occ >= 0)
    pipe = P._pipeline_units(np, view, is_plant, has_animal, np.int32(0))
    # The stream runs to `valuation.pay_day()`, not to `O.LAST_SHED_DAY`: with
    # `plan.HORIZON_DROP_ON` (5b0fcc4) a fire at eod 28 is harvestable on day 29
    # and the DROP chain sells it, so the goose lays one more sellable egg and
    # the pen yields one more collectable fertilizer.
    goose_eggs = int(V.fires_between(np, np.int32(0), np.int32(spec.ANIMAL_FIRST_YIELD_DAY[0]),
                                     np.int32(spec.ANIMAL_INTERVAL[0]), np.int32(1), np.int32(V.pay_day())))
    assert int(pipe[spec.I_STRAWBERRY]) == 12
    assert int(pipe[spec.I_EGG]) == goose_eggs
    assert int(pipe[spec.I_FERT]) == V.pay_day()
    assert int(pipe[spec.I_WOOL]) == 7
