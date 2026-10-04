"""H2: a floor under the fertilizer reservation (`plan.FERT_FLOOR_ON`).

Fertilizer's whole-season town drain is exactly zero, so every unit either
seat sells stays in that market and lowers every later quote -- both seats
between them drive it 435-468 units above I0 and the quote to 6-13 coins
(2026-08-30 profile of 192 real-engine games vs kagg2). The switch stops the
sale once the quote falls below a fraction of this game's own base.

The switch is OFF by default and these tests toggle it explicitly, so the
shipped decode is the one the champion theta was trained against.
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
import pytest
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

NO_HOLD = np.zeros(spec.N_PRODUCTS, np.int32)      # sell whatever the market will take
FERT_BASE = spec.DEFAULT_MARKET_PARAMS["FERTILIZER"]["base"]


@pytest.fixture
def floor_on(monkeypatch):
    monkeypatch.setattr(P, "FERT_FLOOR_ON", True)


def _view(glut, day=12, fert_in_shed=6):
    """Nothing planted (so nothing reserves fertilizer), `fert_in_shed` units
    to sell, and a fertilizer market `glut` units above its opening
    inventory."""
    z = np.zeros(100, np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = fert_in_shed
    mkt = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    mkt[spec.I_FERT] = spec.MARKET_I0 + glut
    price = np.array([spec.market_price(n, int(mkt[i]))
                      for i, n in enumerate(spec.PRODUCTS)], np.int32)
    return P.DayView(
        day=np.int32(day), kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0),
        nquad=np.int32(1), price=price, mkt_inv=mkt)


def _fert_sold(view):
    op, arg, qty = P.build_day(np, view, _macro(hold=NO_HOLD))[3:6]
    # Every turn of the day, not just `O.SELL_TURNS`: `plan.EARLY_SELL_ON` moves
    # lot 1 onto the BUY row, and the day's *total* is what this file is about
    # (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`).
    return sum(int(qty[t, s]) for t in range(spec.TURNS_PER_DAY)
               for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[t, s]) == O.MO_SELL and int(arg[t, s]) == spec.I_FERT)


#: A glut deep enough that the quote is under any floor the module can ship
#: (the curve is linear at 0.2 coins a unit, so 495 above I0 is the 1-coin
#: floor). Derived, not hard-coded, so tuning the fraction cannot rot the test.
DEEP = 495
SHALLOW = 0                                          # a fresh market quotes `base`


def test_switch_off_sells_into_the_floor(monkeypatch):
    """The default path is the champion's: a 6-coin quote still sells."""
    monkeypatch.setattr(P, "FERT_FLOOR_ON", False)
    assert _fert_sold(_view(glut=DEEP)) == 6


def test_switch_on_holds_fertilizer_once_the_quote_is_under_the_floor(floor_on):
    assert _fert_sold(_view(glut=DEEP)) == 0


def test_switch_on_still_sells_at_base(floor_on):
    """The gate is a price floor, not a ban: at the opening inventory the
    quote is `base`, which is above any fraction of itself."""
    assert P.FERT_FLOOR_NUM < P.FERT_FLOOR_DEN, "a floor at or above base is a ban"
    assert _fert_sold(_view(glut=SHALLOW)) == 6


def test_the_floor_is_a_fraction_of_this_game_s_base(floor_on):
    """Read off the price table, so a randomised market moves the floor with
    it rather than leaving it pinned to `DEFAULT_MARKET_PARAMS`."""
    table = np.asarray(P.default_price_table())
    hold = P._sell_hold(np, table, np.zeros(spec.N_PRODUCTS, np.int32), np.bool_(False))
    assert int(hold[spec.I_FERT]) == FERT_BASE * P.FERT_FLOOR_NUM // P.FERT_FLOOR_DEN
    assert [int(x) for x in np.delete(hold, spec.I_FERT)] == [0] * (spec.N_PRODUCTS - 1)


def test_the_terminal_day_still_liquidates(floor_on):
    """Day 29's shed is worth exactly zero unsold [LAW, 0.4]; the floor must
    not override that."""
    assert _fert_sold(_view(glut=DEEP, day=29)) == 6
