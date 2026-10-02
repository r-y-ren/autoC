"""Hands are hired by enumerated argmax (PLANNER_V3_1 section 1.5): the count
whose admitted task value minus its fib bill is highest, ties to fewer hands,
and the bill is reserved from the purse before anything is bought.

Affordable means "and still re-fieldable tomorrow" [LAW]: a count is a
candidate only if `HIRE_BILLS[h] + cash_reserve(h)` fits `view.money`, so a
farm down to its reserve cannot spend it on the crew. That roughly doubles the
purse a given crew needs, which is why the boards below that mean to hire
sixteen hands carry more than the fib bill alone.
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

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(ripe, crop, units, money=3000, day=13, thirsty=False):
    """`ripe` tiles carrying `units` of `crop`, ready to harvest.

    `thirsty` marks them unwatered yesterday, which adds a survival watering to
    each tile's chain -- two ops instead of one, so the board costs twice the
    turns and a full crew of seventeen units still cannot walk all of it.
    """
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_cons = z.copy()
    kind[:ripe] = spec.KIND_PLANT
    occ[:ripe] = crop
    t_yield[:ripe] = units
    t_cons[:ripe] = 1 if thirsty else 0
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=t_cons,
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(4), price=BASE.copy())


def _hires(view, **macro):
    """Every HIRE the day emits. Summed over the whole market block, not over
    `O.TURN_HIRE` alone: a crew past `MAX_MARKET_ORDERS` needs a second HIRE
    turn (`O.TURN_HIRE_WIDE`), and HIRE appears on no other turn."""
    op = P.build_day(np, view, _macro(**macro), TABLE)[3]
    return int((op == O.MO_HIRE).sum())


def test_no_work_hires_nobody():
    assert _hires(_farm(0, spec.I_WHEAT, 0)) == 0


def test_a_big_harvest_hires_every_hand():
    # A hundred thirsty melons at 1,500 each: water then harvest, so at
    # `n_ops + EST_MOVES = 3` a tile the board is 300 estimated turns, against
    # the 17 x (21 - EST_LEAD) = 272 a full crew of seventeen can admit -- more
    # work than the ceiling can reach, so the argmax runs into the ceiling and
    # every hand still pays its fib cost many times over.
    #
    # 6,000 coins, not the fixture's 3,000: sixteen hands cost 2,583 and imply
    # a 2,583-coin reserve, and the enumeration will not field a crew it cannot
    # re-field tomorrow.
    assert _hires(_farm(100, spec.I_MELON, 6, money=6000, thirsty=True)) == spec.MAX_HANDS


def test_the_reserve_caps_the_crew_a_thin_purse_can_field():
    """The same board on the fixture's own 3,000 stops at fourteen: fifteen
    hands are 1,596 and imply a 2,583-coin reserve, which is 4,179."""
    assert _hires(_farm(100, spec.I_MELON, 6, thirsty=True)) == 14


def test_the_argmax_stops_short_when_the_work_runs_out_first():
    """The ceiling only binds when the work outlasts it.

    The same hundred melons unwatered are one op a tile, so the board is
    100 x (1 + EST_MOVES) = 200 estimated turns. Each of h + 1 units admits
    `route_turns(h) - EST_LEAD` of them -- 17 up to ten hands, 16 past the
    turn-2 hire row -- so twelve hands admit 13 x 16 = 208 and cover the lot,
    eleven admit 192 and reach 96 tiles, and the thirteenth hand is bought for
    nothing and refused."""
    assert _hires(_farm(100, spec.I_MELON, 6)) == 12


def test_hands_are_hired_only_while_they_add_admitted_value():
    # Twelve ripe wheat tiles at 25. No pickup kind has any demand today, so
    # each unit's admit budget is 22 - 0 - EST_LEAD = 17 and a tile is
    # estimated at 1 op + EST_MOVES = 2: the farmer admits eight (16 <= 17),
    # a second hand covers all twelve, and a third would add nothing.
    # Scores: 8 x 25 - 0 = 200, 12 x 25 - 1 = 299, 12 x 25 - 2 = 298.
    assert _hires(_farm(12, spec.I_WHEAT, 1)) == 1


def test_the_purse_caps_the_bill():
    # Three coins: one hand costs 1 and reserves 2, which is exactly 3. Two
    # hands cost 2 and reserve 4, which is 6 -- so the second is refused on the
    # reserve, not on its own price.
    assert _hires(_farm(100, spec.I_MELON, 6, money=3)) == 1
    assert _hires(_farm(100, spec.I_MELON, 6, money=6)) == 2


def test_the_terminal_day_hires_nobody(monkeypatch):
    """The terminal day hires exactly what its own chain can still monetize.

    With `plan.DROP_ON` off -- the law this test was written against, before
    51e7b50 turned the day-29 end-game on by default -- day 29 emits no unit
    op at all, so no count admits any value and the 1.5 argmax stops at zero
    hands.

    On, which is the shipped default, the day-29 chain closes inside the day:
    HARVEST, walk to a shed access, DROP, and `SELL_TURNS[-1]` sells what the
    DROP banked, because units act before their turn's market
    (`valuation.pay_day()` = 29, `tests/test_day29_endgame.py`). A hundred ripe
    melons are then ordinary work -- and dearer work than on day 13, because
    every block also owes its walk home, so the board outlasts the ceiling and
    the enumeration buys the whole crew instead of the twelve hands
    `test_the_argmax_stops_short_when_the_work_runs_out_first` stops at.
    """
    board = _farm(100, spec.I_MELON, 6, day=29)
    assert _hires(board) == (spec.MAX_HANDS if P.DROP_ON else 0)
    monkeypatch.setattr(P, "DROP_ON", False)
    assert _hires(board) == 0


def _tie_board(units):
    """Nine ripe strawberries at a price of 1, one op each, on a purse that
    can pay any bill. `test_admit_route`'s `_farm` is not reused: this needs a
    custom product price and a non-zero purse."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    kind[40:49], occ[40:49], t_yield[40:49] = spec.KIND_PLANT, spec.I_STRAWBERRY, units
    price = BASE.copy()
    price[spec.I_STRAWBERRY] = 1
    return P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(1000), nquad=np.int32(4), price=price)


def test_an_exact_tie_goes_to_the_fewer_hands():
    """§1.5's tie rule, on a board built to tie exactly.

    Nine tiles, one op each, so each is estimated at 1 + EST_MOVES = 2 turns
    and no pickup kind has any demand: the farmer's admit budget of
    22 - 0 - EST_LEAD = 17 takes `17 // 2 = 8` of them and a second hand's 34
    takes all nine. The second hand therefore buys exactly one more tile, and
    `spec.HIRE_COST[1]` -- the second hire's fib price -- is exactly 1 coin.

    So with every tile worth 1 coin the two scores are `8 - 0` and `9 - 1`,
    both 8, and `argmax` takes the first maximum: no hands. Double every tile
    to 2 coins and the extra tile is worth 2 against the same 1-coin bill:
    `16 - 0` against `18 - 1`, and the hand is hired.
    """
    assert int(spec.HIRE_COST[1]) == 1
    assert _hires(_tie_board(1)) == 0
    assert _hires(_tie_board(2)) == 1


def test_macro_has_no_n_hire():
    assert "n_hire" not in P.Macro._fields


def test_enumeration_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _farm(30, spec.I_TOMATO, 1), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
