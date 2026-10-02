"""A hungry animal is fed iff what it can still sell -- capped at what a
replacement costs, plus any pending CARE bank a fed fire day would cash --
beats the wheat's engine-curve price (PLANNER_V3_1 section 1.4). One that
fails is not fed and, with 0.8, not replaced.
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
from test_budget_order import _macro, geese

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ
from kagg3.core import valuation as V

# `plan` is imported above on purpose: `valuation.pay_day()` reads the horizon
# switch off `valuation._PLAN`, which `plan` binds at import time, and a module
# that reaches `valuation` without it reads the un-switched 28 (see df9013d).
TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(day, geese, *, wheat=10, egg=50, fert=100, t_bank=0, money=3000):
    """`geese` hungry geese placed on day 0 at the head of the sweep."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:geese] = spec.KIND_COOP
    occ = z - 1
    occ[:geese] = 0
    t_cons = z.copy()
    t_cons[:geese] = 1
    bank = z.copy()
    bank[:geese] = t_bank
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE.copy()
    price[spec.I_EGG], price[spec.I_FERT] = egg, fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=price, t_bank=bank)


def _counts(view, **macro):
    plan = P.build_day(np, view, _macro(**macro), TABLE)
    unit_op, op, arg, qty = plan[0], plan[3], plan[4], plan[5]
    row = O.TURN_BUY
    wheat = sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
                if int(op[row, s]) == O.MO_BUY_PRODUCT and int(arg[row, s]) == spec.I_WHEAT)
    animals = int(qty[row][op[row] == O.MO_BUY_ANIMAL].sum())
    return int((unit_op == O.OP_FEED).sum()), wheat, animals


def _value(view, a, day):
    """`valuation.animal_value` for the animal of kind `a` at the head of the
    sweep -- the flow `plan.py`'s `keep_val` is built from (`plan.py:4181`),
    before today's stock is taken out of it and before the replacement cap."""
    return int(V.animal_value(np, view.price, view.t_day, view.t_yield,
                              view.t_favail, np.full(100, a, np.int32),
                              np.int32(day))[0])


def _bank_fire(view, a, day):
    """Harvest day of the fire a bank standing this morning cashes on --
    `plan.py`'s own `bank_h` (`plan.py:4168`), which pays the bank only while
    it is at or before `valuation.pay_day()`."""
    return int(V.next_fire_after(np, view.t_day,
                                 np.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a],
                                 np.asarray(spec.ANIMAL_INTERVAL)[a],
                                 np.int32(day - 1))[0])


def test_a_paying_animal_is_fed():
    # `pay_day() - 1` goose: one egg (50) and one fertilizer (100) left, wheat
    # costs 25 -- the paying half of the pair below, on the same board.
    assert _counts(_farm(int(V.pay_day()) - 1, 1))[0] == 1


def test_a_worthless_animal_is_left_to_escape_and_not_replaced():
    """One egg and one fertilizer left in it, 20 coins against a 25-coin wheat:
    no feed, no wheat, no goose.

    The day is written off `valuation.pay_day()` and not as a hard-coded 27.
    `animal_value` counts every fire still harvestable by `pay_day()` and one
    fertilizer per day up to it, and `plan.HORIZON_DROP_ON` (5b0fcc4) moved
    that horizon from 28 to 29 -- so on day 27 the same goose is now worth
    2 x 10 + 2 x 10 = 40, clears the wheat, and is fed. The board this test is
    about is the one with a single fire and a single collection left, which is
    `pay_day() - 1`.
    """
    day = int(V.pay_day()) - 1
    view = _farm(day, 1, egg=10, fert=10, wheat=0)
    # The arithmetic first, so a further horizon move fails on the derivation.
    value = int(V.animal_value(np, view.price, view.t_day, view.t_yield,
                               view.t_favail, np.zeros(100, np.int32),
                               np.int32(day))[0])
    assert value == 10 + 10 < int(view.price[spec.I_WHEAT])
    assert _counts(view, animal_want=geese(0)) == (0, 0, 0)


def test_a_pending_bank_counts_toward_the_value():
    """A goose whose own flow cannot pay for its feed is fed for the bank.

    The day is written off `valuation.pay_day()` and not as a hard-coded 27:
    the goose worth 8 + 8 is the one with a single fire and a single
    collection left, which is `pay_day() - 1`. `plan.HORIZON_DROP_ON`
    (5b0fcc4) moved that horizon from 28 to 29, so on day 27 the same goose is
    worth 2 x 8 + 2 x 8 = 32, clears the wheat, and is fed with no bank at all
    -- which is not the board this test is about.

    16 < 25 alone; a bank of 2 eggs (16), cashed on the fire `bank_h` puts on
    the pay day itself, lifts the feed to 32.
    """
    day = int(V.pay_day()) - 1
    view = _farm(day, 1, egg=8, fert=8)
    wheat_price = int(view.price[spec.I_WHEAT])
    # The arithmetic first, so a further horizon move fails on the derivation.
    assert _value(view, 0, day) == 8 + 8 < wheat_price
    assert _counts(view)[0] == 0

    banked = _farm(day, 1, egg=8, fert=8, t_bank=2)
    assert _bank_fire(banked, 0, day) <= int(V.pay_day())
    assert 8 + 8 + 2 * 8 > wheat_price
    assert _counts(banked)[0] == 1


def test_each_bought_feed_is_priced_on_the_curve():
    """30 geese worth 27 coins each, no wheat in the shed: the curve starts at
    26 and rises, so only the feeds whose quote stays under the value pass.

    The day is `pay_day() - 1` -- one fire and one collection left, 17 + 10 --
    and no longer the hard-coded 27: `plan.HORIZON_DROP_ON` (5b0fcc4) moved
    the horizon to 29, and on day 27 the same goose is worth
    2 x 17 + 2 x 10 = 54, over every one of the 30 quotes, so the curve stops
    deciding anything. The threshold is read off `animal_value` rather than
    written down, so a further move fails on the derivation.
    """
    day = int(V.pay_day()) - 1
    view = _farm(day, 30, egg=17, fert=10, wheat=0)
    value = _value(view, 0, day)
    assert value == 17 + 10
    inv1 = PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY)
    quotes = PJ.buy_quotes(np, TABLE, inv1)[spec.I_WHEAT]
    expect = int((quotes[:30] < value).sum())
    assert 0 < expect < 30
    fed, wheat, _ = _counts(view)
    assert fed == expect and wheat == expect


def test_shed_wheat_is_priced_at_the_hour_zero_quote():
    # the same 30 geese with 30 wheat in the shed: every feed costs 25 < 27
    fed, wheat, _ = _counts(_farm(int(V.pay_day()) - 1, 30, egg=17, fert=10, wheat=30))
    assert fed == 30 and wheat == 0


def _beast(a, day, *, t_day=0, t_yield=0, t_favail=0, t_bank=0, prod_price=None,
           fert=100, wheat_price=None, wheat=10):
    """One hungry animal of kind `a` at the head of the sweep, placed on `t_day`.

    spec.ANIMAL_*: goose (first 4, interval 1, max_held 4, cost 300), cow
    (8, 2, 6, 400), sheep (6, 3, 6, 500). The structure kind follows
    `spec.ANIMAL_STRUCT`, so the fixture cannot get the pairing wrong.
    """
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[0] = int(spec.ANIMAL_STRUCT[a])
    occ = z - 1
    occ[0] = a
    t_cons = z.copy()
    t_cons[0] = 1                                     # hungry: escapes tonight unless fed
    yld = z.copy()
    yld[0] = t_yield
    fav = z.copy()
    fav[0] = t_favail
    bank = z.copy()
    bank[0] = t_bank
    td = z.copy()
    td[0] = t_day
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE.copy()
    price[spec.I_FERT] = fert
    if prod_price is not None:
        price[int(spec.ANIMAL_PRODUCT[a])] = prod_price
    if wheat_price is not None:
        price[spec.I_WHEAT] = wheat_price
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=td, t_water=z.copy(),
        t_cons=t_cons, t_yield=yld, t_fert=z - 1, t_cared=z.copy(), t_favail=fav,
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1), price=price, t_bank=bank)


def _fed(view):
    return int((P.build_day(np, view, _macro(), TABLE)[0] == O.OP_FEED).sum())


def _horizon_cow(day, **kw):
    """A cow (first yield 8, interval 2) placed so its fires straddle the
    monetization horizon: one on `pay_day() - 1`, the next on `pay_day() + 1`.

    That is `t_day` 0 with `plan.HORIZON_DROP_ON` on (fires 8, 10, ..., 28, 30)
    and the 1 this file had without it (9, 11, ..., 27, 29). The two bank tests
    below are placed on the parity, not on the constant.
    """
    return _beast(1, day, t_day=(int(V.pay_day()) - 9) % 2, **kw)


def test_held_units_do_not_pay_for_the_feed_that_does_not_buy_them():
    """The feed test is on FLOW, not stock [gap review, 1.4].

    `animal_value` counts what the animal holds today, and the planner
    harvests and collects that whether or not it feeds. A sheep on day 27 with
    two wool in hand at 1,000 each and one fertilizer available is worth 2,001
    coins of *stock* -- and 1 coin of flow: it has no fire left inside the
    horizon (fires land on days 6, 9, ..., 27) and one more day of fertilizer
    at a price of 1.

    So the feed is worth 1 against a 25-coin wheat and the animal is left to
    escape [0.8]. Counting the stock would have given
    `min(2 * 1000 + 2 * 1, 500) = 500` -- the replacement cap, well above the
    wheat -- and bought a feed for units already in the shed's hands. The
    harvest and the collection still happen: they are what the stock is.
    """
    view = _beast(2, 27, t_yield=2, t_favail=1, prod_price=1000, fert=1)
    plan = P.build_day(np, view, _macro(), TABLE)
    assert int((plan[0] == O.OP_FEED).sum()) == 0
    assert int((plan[0] == O.OP_HARVEST).sum()) == 1
    assert int((plan[0] == O.OP_COLLECT_FERT).sum()) == 1
    assert _counts(view)[1] == 0                       # and no wheat is bought for it

    # the same sheep with a fire still to come is fed: 1,000 coins of wool
    # plus a fertilizer, capped at the 500-coin replacement, beats 25.
    assert _fed(_beast(2, 24, t_yield=2, t_favail=1, prod_price=1000, fert=1)) == 1


def test_a_bank_only_counts_when_its_own_fire_lands_inside_the_horizon():
    """`bank_h <= pay_day()` is what keeps a doomed bonus out of the value.

    `bank_h` is the harvest day of the first fire whose end-of-day is at or
    after today's, and `_horizon_cow` places the cow so that on
    `pay_day() - 2` it is `pay_day() - 1` (inside the horizon) and on
    `pay_day() - 1` it is `pay_day() + 1` (outside: nothing harvested after
    the pay day ever reaches a market). The days were the hard-coded 26 and 27
    of a 28-day horizon; `plan.HORIZON_DROP_ON` (5b0fcc4) moved it to 29,
    which made day 27's `bank_h` payable -- this fixture's failure, and not a
    change in the rule it states.

    Prices are milk 4, fertilizer 10, wheat 25, and the bank is 20 units,
    which `min(t_bank, max_held - 1)` clips to 5.

      pay_day() - 1  flow = 0 fires x 4 + 1 fertilizer-day x 10 = 10; the bank
                     would add 5 x 4 = 20 and carry it to 30, past the 25-coin
                     wheat -- but its fire is a day too late, so it adds
                     nothing and 10 < 25.
      pay_day() - 2  flow = 1 fire x 4 + 2 fertilizer-days x 10 = 24, still
                     under the wheat on its own; the bank's fire is inside, so
                     it adds 20 and 44 > 25.
    """
    hi = int(V.pay_day())
    # The arithmetic first, so a further horizon move fails on the derivation.
    late = _horizon_cow(hi - 1, t_bank=20, prod_price=4, fert=10)
    wheat_price = int(late.price[spec.I_WHEAT])
    assert _value(late, 1, hi - 1) == 0 * 4 + 1 * 10 < wheat_price
    assert _bank_fire(late, 1, hi - 1) == hi + 1 > hi
    assert _fed(late) == 0

    early = _horizon_cow(hi - 2, t_bank=20, prod_price=4, fert=10)
    assert _value(early, 1, hi - 2) == 1 * 4 + 2 * 10 < wheat_price
    assert _bank_fire(early, 1, hi - 2) == hi - 1 <= hi
    assert 24 + min(20, int(spec.ANIMAL_MAX_HELD[1]) - 1) * 4 > wheat_price
    assert _fed(early) == 1
    # ... and without the bank that cow is not fed either, so the bank is what
    # tips it and not the extra fertilizer day.
    assert _fed(_horizon_cow(hi - 2, t_bank=0, prod_price=4, fert=10)) == 0


def test_a_bank_pays_at_most_max_held_minus_one_units():
    """A fed fire yields `min(max_held, yield + 1 + bank)`, so a bank of 20 on
    a cow (max_held 6) is worth 5 units, not 20.

    The same `pay_day() - 2` cow as above -- day 26 while the horizon was 28,
    which 5b0fcc4 moved to 29: flow 24, bank 20 units at 4 coins. Capped it is
    worth 5 x 4 = 20 and the feed is worth 44; uncapped it would be worth 80
    and the feed 104. A 50-coin wheat is between the two, so only the cap
    decides.
    """
    day = int(V.pay_day()) - 2
    capped = _horizon_cow(day, t_bank=20, prod_price=4, fert=10, wheat_price=50)
    held = int(spec.ANIMAL_MAX_HELD[1])
    # The arithmetic first, so a further horizon move fails on the derivation.
    assert _value(capped, 1, day) == 1 * 4 + 2 * 10
    assert _bank_fire(capped, 1, day) <= int(V.pay_day())
    assert 24 + min(20, held - 1) * 4 == 44 < 50 < 24 + 20 * 4 == 104
    assert _fed(capped) == 0
    assert _fed(_horizon_cow(day, t_bank=20, prod_price=4, fert=10,
                             wheat_price=40)) == 1


def test_feed_value_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _farm(27, 30, egg=17, fert=10, wheat=0), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
