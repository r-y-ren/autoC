"""The budget must price against money the day will actually still have.

`build_day` seeds the budget with `view.money`, the purse at the *start* of the
day -- but hires resolve on TURN_HIRE, before TURN_BUY, and hiring is not one of
the budget's candidate lists. So the BUY row could commit the entire purse while
the hire bill had already spent part of it.

The engine resolves slots in the fixed layout order, and BUY_LAND used to sit
last in the BUY row, so land was structurally the slot that failed. Measured on
`order1`'s gen-650 champion, day 0, seed 20260821: hire bill 4, row total
exactly 3,000 against a 3,000 purse, and the day ended on 996 coins and one
quadrant -- land dropped for four coins, with the macro asking for the
quadrant.

M2 moved BUY_LAND out of that row and onto the spare slot of the first SELL
turn, so it is no longer the slot that fails -- but the arithmetic this file
pins is unchanged, and `_buy_bill` below now scans the whole market block
rather than the BUY row, because a helper that still read one turn would score
the land purchase at zero and pass by under-counting.

The count is the planner's own since section 1.5, so these tests read it back
off the emitted hire row instead of dictating it.
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
from test_budget_order import _macro, _view, geese

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _buy_bill(view, macro):
    """What the day's purchases actually cost, priced slot by slot.

    Every turn, not just `O.TURN_BUY`: since M2 the day's BUY_LAND rides the
    spare slot of `O.SELL_TURNS[0]`, and a scan of one row would score it at
    zero -- a silent under-count, which is the failure mode this whole file
    exists to catch."""
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    p = np.asarray(view.price)
    total = 0
    for turn in range(spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            o, ai, qi = int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s])
            if qi == 0:
                continue
            if o == O.MO_BUY_PRODUCT:
                total += qi * int(p[ai])
            elif o == O.MO_BUY_SEED:
                total += qi * int(spec.CROP_SEED_COST[ai])
            elif o == O.MO_BUY_ANIMAL:
                total += qi * int(spec.ANIMAL_COST[ai])
            elif o == O.MO_BUY_LAND:
                total += int(spec.LAND_PRICES[int(view.nquad) - 1])
    return total


def _hires(view, macro):
    """How many hands the plan's own enumeration hired [1.5], across both HIRE
    rows (turn 0 and, past `MAX_MARKET_ORDERS` hands, `O.TURN_HIRE_WIDE`)."""
    op = P.build_day(np, view, macro)[3]
    return int((op == O.MO_HIRE).sum())


def _hire_bill(n):
    return int(spec.HIRE_COST[:n].sum())


def _pump_units(view):
    """Wheat `plan.OPEN_PUMP_ON` puts on this view's BUY row [ff3fe12].

    The switch's own three conditions, restated so the arithmetic below is the
    switch's and not a copied number: the opening day, and a purse that clears
    `OPEN_PUMP_MIN_MONEY`. The units are bought at hour 0 and sold back at hour
    1, so they cost the day nothing -- but `_buy_bill` scans slots, and a slot
    that buys is a slot that buys. Zero with the switch off, which puts the
    identity below back on the bare purse."""
    if not (P.OPEN_PUMP_ON and int(view.day) == P.OPEN_PUMP_DAY
            and int(view.money) >= P.OPEN_PUMP_MIN_MONEY):
        return 0
    return int(P.OPEN_PUMP_UNITS)


# Land (1,000) plus five geese (5 x 300) is exactly 2,500, so a 2,500 purse is
# spent to the last coin by the grant -- which is the only situation where the
# missing hire bill can push the row past what the day can pay.
PURSE = int(spec.LAND_PRICES[0]) + 5 * int(spec.ANIMAL_COST[0])
MACRO = {"land_bias": np.int32(spec.LAND_PRICES[0]), "animal_want": geese(5)}


def _with_ripe_work(view, n=20):
    """`n` ripe tomatoes in front of the blank board. The hire count is the
    planner's own [1.5], so the fixture has to give the day work worth hiring
    for; already fertilized, so the harvests add labour and not purchases.

    The count is deliberately *not* pinned here -- the test reads it back off
    the emitted HIRE row and only asserts that the BUY row plus that bill fits
    the purse. What the fixture assumes is that it is non-zero, which the test
    asserts before using it."""
    kind, occ, t_yield, t_fert = (view.kind.copy(), view.occ.copy(),
                                  view.t_yield.copy(), view.t_fert.copy())
    kind[:n], occ[:n], t_yield[:n], t_fert[:n] = spec.KIND_PLANT, spec.I_TOMATO, 1, 13
    return view._replace(day=np.int32(13), kind=kind, occ=occ,
                         t_yield=t_yield, t_fert=t_fert)


def test_buy_row_leaves_room_for_the_hire_bill():
    # The day-0 shape that dropped land, reduced to its arithmetic.
    view = _with_ripe_work(_view(PURSE))
    macro = _macro(**MACRO)
    n = _hires(view, macro)

    assert _hire_bill(n) > 0, "test is vacuous if nothing is hired"
    assert _buy_bill(view, macro) + _hire_bill(n) <= PURSE


def _with_free_coops(view, n=5):
    """`n` empty coops on the blank board: the geese the grant buys are placed,
    one op a tile, so the whole day fits in the farmer's own route budget --
    22 turns less the one animal pickup the day owes [0.12] -- and 1.5's
    enumeration hires **nobody**: a second hand would admit no extra tile and
    only add its fib bill. The test asserts that count explicitly."""
    kind = view.kind.copy()
    kind[:n] = spec.KIND_COOP
    return view._replace(kind=kind)


def test_the_budget_still_spends_everything_when_nothing_is_hired():
    """The deduction must be the day's own two terms, not a blanket margin.

    Those terms are the hire bill (zero here -- nothing is hired) and the cash
    reserve, which at a crew of zero is `HIRE_BILLS[1]`: the single coin that
    lets tomorrow hire a hand at all (`plan.cash_reserve`,
    `test_cash_reserve.py`). Everything else still goes. Written as an identity
    rather than an inequality so a future margin cannot hide inside it: the
    purse handed to the greedy is `money - hire_bill - reserve`, exactly.

    The opening pump is the third term and it is not the greedy's: `_view` is a
    day-0 board, and since ff3fe12 `plan.OPEN_PUMP_ON` puts `OPEN_PUMP_UNITS`
    of wheat on the same hour-0 row and sells them straight back on the hour-1
    row, so `_buy_bill`'s slot-by-slot scan sees a purchase the day never
    spends. It is added to the identity rather than allowed to hide inside it,
    and derived from the switch so that turning the pump off restores the bare
    `PURSE`.
    """
    reserve = int(P.cash_reserve(np, np.int32(0), np.int32(0)))
    assert reserve == int(spec.HIRE_COST[0])
    view = _with_free_coops(_view(PURSE + reserve))
    macro = _macro(**MACRO)
    pump = _pump_units(view) * int(view.price[spec.I_WHEAT])

    assert _hires(view, macro) == 0
    assert _buy_bill(view, macro) == PURSE + pump
