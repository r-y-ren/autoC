"""Fertilizer the day's FERTILIZE tasks will pick up is held back from the sale
(PLANNER_V3_1 section 0.7), mirroring the feed-wheat reservation: sell lot 1
fires at turn 2 while the fertilizer pickup can slide to turn 3.
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


def _view(fert_in_shed, n_tomato=3, day=8):
    """`n_tomato` tomatoes planted on day 0 -- on day 8 each has three fires
    in a fertilizer window, worth 3 x 25 > the fertilizer's 25 -- and
    `fert_in_shed` fertilizer, no money to buy more."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:n_tomato] = spec.KIND_PLANT
    occ = z - 1
    occ[:n_tomato] = spec.I_TOMATO
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert_in_shed
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


NO_HOLD = np.zeros(spec.N_PRODUCTS, np.int32)      # sell whatever the market will take


def _fert_sold(view, macro):
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    # Every turn of the day, not just `O.SELL_TURNS`: `plan.EARLY_SELL_ON` moves
    # lot 1 onto the BUY row, and the day's *total* is what this file is about
    # (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`).
    return sum(int(qty[t, s]) for t in range(spec.TURNS_PER_DAY)
               for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[t, s]) == O.MO_SELL and int(arg[t, s]) == spec.I_FERT)


def test_planned_fertilizer_is_held_back_from_the_sale():
    view = _view(fert_in_shed=5)
    unit_op = P.build_day(np, view, _macro(hold=NO_HOLD))[0]
    assert int((unit_op == O.OP_FERTILIZE).sum()) == 3
    assert _fert_sold(view, _macro(hold=NO_HOLD)) == 2


def test_nothing_reserved_when_nothing_is_worth_fertilizing():
    # day 12: the tomatoes' last fire (day 11) is behind them
    assert _fert_sold(_view(fert_in_shed=5, day=12), _macro(hold=NO_HOLD)) == 5


def test_reservation_is_capped_by_what_the_day_can_spread():
    # 8 candidates, 5 in the shed, no money: n_fert_eff is 5, so none sells
    assert _fert_sold(_view(fert_in_shed=5, n_tomato=8), _macro(hold=NO_HOLD)) == 0
