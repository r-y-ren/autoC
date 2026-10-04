"""The planner's sale is the reservation-value allocator (PLANNER_V3_1 1.2)
folded with the Phase-0 laws: feed wheat and fertilizer reservations, the
forced overflow sale, and day-29 liquidation at zero reservation.
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
from kagg3.core import sell as S

TABLE = spec.build_price_table()


def _view(shed, day=3, shops=None, geese_hungry=0):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    kind[:geese_hungry] = spec.KIND_COOP
    occ[:geese_hungry] = 0
    t_cons[:geese_hungry] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32) if shops is None else shops)


def _lot1_turn():
    """The turn the day's first lot rides. `plan.EARLY_SELL_ON` merges it into
    the BUY row (`O.EARLY_SELL_LOT1_TURN`) on any day the purchases and the lot
    together fit the engine's ten slots, which every board in this file does;
    off, it stands on `O.SELL_TURNS[0]` where it always did."""
    return O.EARLY_SELL_LOT1_TURN if P.EARLY_SELL_ON else O.SELL_TURNS[0]


def _sells(view, macro):
    """{turn: {product: qty}}, read over every turn of the day and not just
    `O.SELL_TURNS`: `plan.EARLY_SELL_ON` moves lot 1 onto the BUY row, and what
    the reservation lets the day sell is a total the switch does not change
    (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`)."""
    op, arg, qty = P.build_day(np, view, macro, TABLE)[3:6]
    out = {}
    for t in range(spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(op[t, s]) == O.MO_SELL:
                out.setdefault(t, {})[int(arg[t, s])] = int(qty[t, s])
    return out


def _total(sells, product):
    return sum(d.get(product, 0) for d in sells.values())


def test_zero_reservation_sells_the_shed():
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_EGG: 7}), _macro(hold=np.zeros(9, np.int32)))
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_EGG) == 7


def test_default_reservation_holds_everything():
    assert _sells(_view({spec.I_WOOL: 12}), _macro()) == {}


def test_reservation_gates_per_product():
    hold = np.full(9, 10_000, np.int32)
    hold[spec.I_EGG] = 0
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_EGG: 7}), _macro(hold=hold))
    assert _total(sells, spec.I_EGG) == 7 and _total(sells, spec.I_WOOL) == 0


def test_pressure_moves_a_yarn_town_sale_to_the_first_lot():
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("YARN_STORE")] = 1
    view = _view({spec.I_WOOL: 12}, shops=shops)
    late = _sells(view, _macro(hold=np.zeros(9, np.int32)))
    assert late.get(O.SELL_TURNS[-1], {}).get(spec.I_WOOL, 0) > late.get(_lot1_turn(), {}).get(spec.I_WOOL, 0)
    press = np.zeros(9, np.int32)
    press[spec.I_WOOL] = 1000
    early = _sells(view, _macro(hold=np.zeros(9, np.int32), press=press))
    assert early[_lot1_turn()][spec.I_WOOL] == 12


def test_feed_wheat_stays_reserved():
    view = _view({spec.I_WHEAT: 10}, geese_hungry=4)
    sells = _sells(view, _macro(hold=np.zeros(9, np.int32)))
    assert _total(sells, spec.I_WHEAT) == 6


def test_day_29_liquidates_at_zero_reservation():
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_MELON: 3}, day=29), _macro())   # default hold 10,000 is void
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_MELON) == 3


def test_day_29_liquidates_under_pressure_too():
    # a pressure gene above every quote makes every adjusted marginal negative;
    # the law still sells the whole shed [0.4]
    press = np.full(9, 5000, np.int32)
    sells = _sells(_view({spec.I_WOOL: 12, spec.I_FERT: 4}, day=29), _macro(press=press))
    assert _total(sells, spec.I_WOOL) == 12 and _total(sells, spec.I_FERT) == 4
    assert set(sells) == {_lot1_turn()}            # everything in the first lot


def _overflow_view(harvest_tonight=20, shed=None):
    """A shed the day's certain inflow overshoots: `shed` holds 95 units by
    default (90 tomato, 5 wheat) and `harvest_tonight` ripe tomatoes bank one
    unit each tonight. The market is deep in tomato, so the forced sale drains
    that product first."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:harvest_tonight] = spec.KIND_PLANT
    occ = z - 1
    occ[:harvest_tonight] = spec.I_TOMATO
    t_yield = z.copy()
    t_yield[:harvest_tonight] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in ({spec.I_TOMATO: 90, spec.I_WHEAT: 5} if shed is None else shed).items():
        sh[i] = n
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_TOMATO] = spec.MARKET_I0 + 40_000
    return P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(),
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(1000), nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32))


def test_forced_overflow_units_join_the_lot_the_allocator_chooses():
    # 95 in the shed, 20 harvested tonight, everything held: 15 must go anyway,
    # and they go where the *continued* allocation puts them [0.9], not into
    # some fixed lot. Derived: the board's tomato market sits 40,000 units
    # above I0, so every lot quotes the $1 floor and each unit's drop on the
    # later lots is 0 -- the three adjusted marginals tie at 1 and the tie
    # falls to the earliest lot, so all 15 land in lot 1, wherever
    # `plan.EARLY_SELL_ON` stands it.
    view = _overflow_view()
    il = S.lot_inventories(np, view.mkt_inv, view.shops)
    adj = S.adjusted_marginals(np, TABLE, il, np.zeros((S.N_LOTS, spec.N_PRODUCTS), np.int32),
                               np.zeros(spec.N_PRODUCTS, np.int32))
    assert adj[:, spec.I_TOMATO].tolist() == [1, 1, 1]
    sells = _sells(view, _macro())
    assert _total(sells, spec.I_TOMATO) == 15 and _total(sells, spec.I_WHEAT) == 0
    assert sells == {_lot1_turn(): {spec.I_TOMATO: 15}}


def test_macro_has_no_sell_decisions():
    for name in ("sell_qty", "sell_min", "sell_lots"):
        assert name not in P.Macro._fields
