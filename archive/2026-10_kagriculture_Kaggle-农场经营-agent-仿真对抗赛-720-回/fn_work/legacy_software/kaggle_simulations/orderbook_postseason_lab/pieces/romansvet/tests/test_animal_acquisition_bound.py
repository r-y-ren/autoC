"""A late animal is bought only if an optimistic bound on what it can still
sell beats its cost and feed (PLANNER_V3_1 section 0.2).

The days are written off `valuation.pay_day()`, the last day whose work still
turns into coins, and not off `O.LAST_SHED_DAY` = 28: `plan.HORIZON_DROP_ON`
(5b0fcc4) moved the pay day to 29, and two of the bound's three terms moved
with it -- `ub_units` counts fires up to `pay_day()` and `ub_fert` one
fertilizer per day up to it, while `ub_feeds` deliberately stays a count of
feeds to `O.LAST_SHED_DAY` (`plan.py`, the `ub_feeds` block). So the goose
that collects three fertilizers, eats its wheat and lays no sellable egg is
the one placed on `pay_day - 3`: day 25 before the switch, 26 after it.
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
from test_budget_order import _macro, one_kind

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as V

# `plan` is imported at module scope on purpose: `valuation.pay_day()` reads
# the horizon switch off `valuation._PLAN`, which `plan` binds when it is
# imported, and a module that reaches `valuation` without it reads the
# un-switched 28 instead (see `df9013d` on `test_budget_greedy.py`).
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day, fert_price=100, geese_in_shed=0):
    z = np.zeros(100, np.int32)
    price = BASE.copy()
    price[spec.I_FERT] = fert_price
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = geese_in_shed
    return P.DayView(
        day=np.int32(day), kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1), price=price)


def _bought(view, kind, count=1):
    """Animals bought, over all three BUY_ANIMAL slots: 0.2's bound is per
    kind, so the fixture asks for one kind and reads the whole row back."""
    plan = P.build_day(np, view, _macro(animal_want=one_kind(kind, count)))
    op, qty = plan[3], plan[5]
    return int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_ANIMAL].sum())


def _last_egg_day():
    """The last day a goose may be placed and still lay a sellable egg: its
    first fire is `ANIMAL_FIRST_YIELD_DAY` = 4 harvest days out, and a harvest
    monetizes iff it lands on or before `pay_day()`. 25 with the horizon on,
    24 without it."""
    return V.pay_day() - int(spec.ANIMAL_FIRST_YIELD_DAY[0])


def _feed_coins(day):
    """What the bound charges the animal to eat: one wheat a day through
    `O.LAST_SHED_DAY`, which the horizon switch does not move."""
    return 25 * max(O.LAST_SHED_DAY - day, 0)


def test_the_goose_past_its_last_egg_day_is_rejected():
    # `pay_day - 3`: the first fire would land on `pay_day + 1`, so no egg is
    # sellable and the bound is three fertilizers against price and feed --
    # 3 x 100 - 300 - 2 x 25 = -50 with the horizon on, - 3 x 25 = -75 off.
    day = _last_egg_day() + 1
    assert 3 * 100 - int(spec.ANIMAL_COST[0]) - _feed_coins(day) <= 0
    assert _bought(_view(day), 0) == 0


def test_the_goose_that_still_lays_one_egg_is_bought():
    # `pay_day - 4`: one egg, on the pay day itself, and four fertilizers --
    # 50 + 4 x 100 - 300 - 3 x 25 = +75 with the horizon on, - 4 x 25 = +50 off.
    day = _last_egg_day()
    assert 50 + 4 * 100 - int(spec.ANIMAL_COST[0]) - _feed_coins(day) > 0
    assert _bought(_view(day), 0) == 1


def test_a_dearer_fertilizer_flips_the_rejected_goose():
    # The rejected goose's bound is `3 * fert - 300 - feed` and acceptance is
    # strict (`ub_coins > ANIMAL_COST`), so it flips at the first fertilizer
    # price clearing cost plus feed: 117 with the horizon on (feed 2 x 25,
    # 3 x 117 - 300 - 50 = +1), 126 without it (feed 3 x 25, +3).
    day = _last_egg_day() + 1
    flip = (int(spec.ANIMAL_COST[0]) + _feed_coins(day)) // 3 + 1
    assert _bought(_view(day, fert_price=flip), 0) == 1
    assert _bought(_view(day, fert_price=flip - 1), 0) == 0


def test_sheep_needs_a_fire_in_the_calendar():
    first = int(spec.ANIMAL_FIRST_YIELD_DAY[2])                 # 6, interval 3
    # `pay_day - 6`: the first wool lands on the pay day itself --
    # 200 + 6 x 100 - 500 - 5 x 25 = +675 with the horizon on, - 6 x 25 = +650 off.
    early = V.pay_day() - first
    assert 200 + 6 * 100 - int(spec.ANIMAL_COST[2]) - _feed_coins(early) > 0
    assert _bought(_view(early), 2) == 1
    # A day later the first wool is a day past the horizon: five fertilizers,
    # no wool -- 5 x 100 - 500 - 4 x 25 = -100 on, - 5 x 25 = -125 off.
    late = early + 1
    assert 5 * 100 - int(spec.ANIMAL_COST[2]) - _feed_coins(late) <= 0
    assert _bought(_view(late), 2) == 0


def test_rejection_does_not_touch_stock_in_hand():
    unit_op = P.build_day(np, _view(_last_egg_day() + 1, geese_in_shed=1),
                          _macro(animal_want=one_kind(0, 1)))[0]
    assert int((unit_op == O.OP_BUILD_COOP).sum()) == 1
    assert int((unit_op == O.OP_PLACE).sum()) == 1
