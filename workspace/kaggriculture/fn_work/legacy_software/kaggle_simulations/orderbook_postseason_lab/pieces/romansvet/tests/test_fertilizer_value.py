"""Fertilizer goes where one application is worth most (PLANNER_V3_1 section
0.11), never to a crop that saturates anyway, and only when the gain beats
the fertilizer's own price; the shortfall is bought on the same test. A
fertilized ongoing crop is watered on its fire night to collect the bonus.
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
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(day, plants, fert=0, money=1000, price=None):
    """`plants`: (position, crop, planted_day, t_cons, t_fert[, t_yield]).

    `t_yield` defaults to the freshly planted tile -- 0 for an ongoing crop,
    1 for a one-time crop, which `_new_plant` seeds with a unit. A one-time
    tile that has *already been watered* has to say so: what a fertilizer is
    worth on it is the units it adds before `CROP_MAX_YIELD` clips them, and
    WATER banks one unit per in-window day, so a tile watered since its window
    opened is that many units nearer the clip than a fresh one.
    """
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_cons, t_fert, t_yield = z.copy(), z.copy(), z - 1, z.copy()
    for plant in plants:
        pos, c, planted, cons, fertilized_until = plant[:5]
        kind[pos] = spec.KIND_PLANT
        occ[pos] = c
        t_day[pos], t_cons[pos], t_fert[pos] = planted, cons, fertilized_until
        born = 0 if spec.CROP_ONGOING[c] else 1                # one-time crops are born with 1
        t_yield[pos] = plant[5] if len(plant) > 5 else born
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=t_fert, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1),
        price=BASE.copy() if price is None else price)


def _plan(view, **macro):
    return P.build_day(np, view, _macro(**macro))


def _fert_bought(plan):
    op, arg, qty = plan[3:6]
    return sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_FERT)


TOMATO_D8 = (5, spec.I_TOMATO, 0, 1, -1)      # planted day 0, thirsty (mandatory tier); day 8: three fires in the window
#: In its watering window, not thirsty, and saturates without fertilizer -- so
#: it is worth nothing to fertilize and is only here to be *passed*. Watered on
#: every in-window day it has had (the window opens at age `CROP_WINDOW_START`
#: = 6, so days 6 and 7): 1 born + 2 = 3 units standing on day 8, and the three
#: waterings left before its harvest (days 8, 9, 10) reach `CROP_MAX_YIELD` = 6
#: on their own. The explicit yield is load-bearing since eed96ed harvested a
#: one-time crop at `CROP_SATURATE_AGE` instead of `CROP_MAX_YIELD_DAY` -- age
#: 10 rather than 12 for a melon -- which left an *unwatered* melon two units
#: short at its harvest and made it the day's most valuable application (500
#: coins) instead of a worthless one.
MELON_D6 = (0, spec.I_MELON, 0, 0, -1, 3)


def test_one_unit_goes_to_the_tomato_not_the_melon_ahead_of_it():
    unit_op, unit_a = _plan(_farm(8, [MELON_D6, TOMATO_D8], fert=1))[:2]
    fert_turns = np.flatnonzero(unit_op[0] == O.OP_FERTILIZE)
    assert len(fert_turns) == 1
    # Which tile gets the unit is a *value* decision (`fert_rank`), not a route
    # one, and it is the tomato: three fires x 60 against the melon's nothing.
    # Both tiles are priced, so since the one-crossing route [1.6] they share
    # one route group and the sweep takes them in serpentine order -- the melon
    # at position 0 = (0, 0) first, then the tomato at position 5 = (5, 0).
    # PICKUP on turn 2, 4 + 4 = 8 moves to the melon, WATER on turn 11, five
    # steps east, FERTILIZE on turn 17. Had the melon taken the unit, the
    # tomato's visit would carry no FERTILIZE at all.
    assert int(fert_turns[0]) == O.ROUTE_BASE + 1 + 8 + 1 + 5


def test_nothing_is_fertilized_when_the_gain_is_below_the_fertilizer_price():
    price = BASE.copy()
    price[spec.I_FERT] = 200                     # 3 x 60 = 180 < 200
    unit_op = _plan(_farm(8, [TOMATO_D8], fert=1, price=price))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 0


def test_the_shortfall_is_bought_on_the_same_test():
    assert _fert_bought(_plan(_farm(8, [TOMATO_D8]))) == 1
    price = BASE.copy()
    price[spec.I_FERT] = 200
    assert _fert_bought(_plan(_farm(8, [TOMATO_D8], price=price))) == 0


def test_an_active_application_is_not_renewed():
    unit_op = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 1, 9)], fert=1))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 0


def test_fertilized_ongoing_crop_is_watered_on_its_fire_night():
    # not thirsty (t_cons 0), fertilized through day 9, fires tonight (day 8 -> harvest day 9)
    watered = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, 9)]))[0]
    assert int((watered == O.OP_WATER).sum()) == 1
    # no fertilizer and no money to buy any: the fire night is not watered
    unfertilized = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, -1)], money=0))[0]
    assert int((unfertilized == O.OP_WATER).sum()) == 0
    # freshly fertilized today counts too: FERTILIZE then WATER on the same tile
    ops = _plan(_farm(8, [(5, spec.I_TOMATO, 0, 0, -1)], fert=1))[0][0]
    ops = [int(o) for o in ops if int(o) not in (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST, O.OP_PICKUP)]
    assert ops == [O.OP_FERTILIZE, O.OP_WATER]


def test_wheat_is_fertilized_only_when_its_price_carries_it():
    wheat_d2 = (5, spec.I_WHEAT, 0, 1, -1)       # +2 units
    assert int((_plan(_farm(2, [wheat_d2], fert=1))[0] == O.OP_FERTILIZE).sum()) == 0      # 2 x 25 < 100
    price = BASE.copy()
    price[spec.I_WHEAT] = 60                                                                  # 2 x 60 > 100
    assert int((_plan(_farm(2, [wheat_d2], fert=1, price=price))[0] == O.OP_FERTILIZE).sum()) == 1


def test_day_28_same_day_chain_is_value_conditional():
    late_wheat = (5, spec.I_WHEAT, 25, 0, -1)    # harvest age 3 = today; +1 unit at most
    price = BASE.copy()
    price[spec.I_FERT] = 20
    assert int((_plan(_farm(28, [late_wheat], fert=1, price=price))[0] == O.OP_FERTILIZE).sum()) == 1
    assert int((_plan(_farm(28, [late_wheat], fert=1))[0] == O.OP_FERTILIZE).sum()) == 0     # 25 < 100


def test_ranking_and_rationing_agree_across_backends():
    import jax
    import jax.numpy as jnp
    view = _farm(8, [MELON_D6, TOMATO_D8, (9, spec.I_TOMATO, 1, 1, -1)], fert=1)
    macro = _macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
