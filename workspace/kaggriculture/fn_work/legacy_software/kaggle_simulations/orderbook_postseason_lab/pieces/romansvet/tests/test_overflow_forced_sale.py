"""End-of-day destroys whatever the shed cannot hold. The planner projects
tonight's shed conservatively-LOW (PLANNER_V3_1 section 0.9) and force-sells
the cheapest marginal units today so that certain inflow survives. Forced
units bypass the reservation value and never touch reserved feed wheat or
fertilizer.
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

TABLE = spec.build_price_table()
FLOORED = spec.MARKET_I0 + 40_000       # every product is at the $1 floor here


def _view(shed, *, ripe=20, geese=0, tomato_inv=spec.MARKET_I0, wheat_inv=spec.MARKET_I0):
    """`ripe` tomatoes with one unit banked at the head of the sweep, then
    `geese` hungry geese; shed as given; market inventory per product."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_cons = z.copy()
    kind[:ripe] = spec.KIND_PLANT
    occ[:ripe] = spec.I_TOMATO
    t_yield[:ripe] = 1
    kind[ripe:ripe + geese] = spec.KIND_COOP
    occ[ripe:ripe + geese] = 0
    t_cons[ripe:ripe + geese] = 1
    sh = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in shed.items():
        sh[i] = n
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_TOMATO] = tomato_inv
    inv[spec.I_WHEAT] = wheat_inv
    return P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(1000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32))


def _many_hands(**kw):
    """Every task tile reached, so the inflow is the full crop. Twenty ripe
    tomatoes at 25 a unit pay ten hands' 143-coin fib bill many times over, so
    1.5's enumeration hires them all on its own."""
    return _macro(**kw)


def _sold(plan):
    op, arg, qty = plan[3:6]
    out = np.zeros(spec.N_PRODUCTS, np.int64)
    # Every turn of the day, not just `O.SELL_TURNS`: `plan.EARLY_SELL_ON` moves
    # lot 1 onto the BUY row, and the day's *total* is what this file is about
    # (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`).
    for t in range(spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(op[t, s]) == O.MO_SELL:
                out[int(arg[t, s])] += int(qty[t, s])
    return out


def test_certain_overflow_forces_the_cheapest_product_out():
    # shed 95 + 20 harvested units = 115: 15 must go, and floored tomato is
    # worth less at the margin than wheat at 25.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    assert int((plan[0] == O.OP_HARVEST).sum()) == 20
    sold = _sold(plan)
    assert sold[spec.I_TOMATO] == 15 and sold[spec.I_WHEAT] == 0


def test_forced_sale_bypasses_the_reservation():
    """Only the deficit leaves, on a board where a lower reservation would
    have sold far more of its own accord.

    The floored-tomato board cannot show that: at the $1 floor no reservation
    above zero would ever have sold anyway, so "15 units left" is the same
    answer twice. Here tomato is *scarce* (market inventory 4,000, first quote
    162,308), so a 200,000-coin reservation is the only thing holding it --
    drop the reservation and the value-gated allocation empties the shed.
    """
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=4_000)
    held = _sold(P.build_day(np, view, _many_hands(
        hold=np.full(spec.N_PRODUCTS, 200_000, np.int32)), TABLE))
    assert held.sum() == 15                       # exactly the shed's overshoot

    freed = _sold(P.build_day(np, view, _many_hands(
        hold=np.zeros(spec.N_PRODUCTS, np.int32)), TABLE))
    assert freed.sum() > 15                       # the reservation really was binding


def test_no_forced_sale_without_a_deficit():
    view = _view({spec.I_TOMATO: 75, spec.I_WHEAT: 5}, tomato_inv=FLOORED)      # 80 + 20 = 100 fits
    assert _sold(P.build_day(np, view, _many_hands(), TABLE)).sum() == 0


def test_forced_sale_drains_products_in_ascending_marginal_value():
    # wheat floored (cheapest) but only 5 spare: all 5 go, then 10 tomato.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, wheat_inv=FLOORED)
    sold = _sold(P.build_day(np, view, _many_hands(), TABLE))
    assert sold[spec.I_WHEAT] == 5 and sold[spec.I_TOMATO] == 10


def test_reserved_feed_wheat_is_never_forced():
    # 10 hungry geese eat 10 of the 10 wheat (an outflow, and a reservation):
    # 100 - 10 + 20 = 110, so 10 tomato go although wheat is cheaper.
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 10}, geese=10, wheat_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    assert int((plan[0] == O.OP_FEED).sum()) == 10
    sold = _sold(plan)
    assert sold[spec.I_WHEAT] == 0 and sold[spec.I_TOMATO] == 10


def test_inflow_counts_only_the_harvests_labour_reaches():
    """A hundred ripe tiles: three turns of estimate each is more than the
    eleven units 1.5 can hire have between them, so the day reaches a prefix of
    the sweep, and the deficit is exactly the *reached* yield over the 5 free
    slots, not the whole crop's. That is the property, and it still holds to
    the unit -- only the arithmetic under it moved.

    Re-based 2026-09-06 at 5c384af on the budget 1d03376 gave the day
    ("Start the block the BUY row does not feed", `ROUTE_SPLIT_ON` promoted to
    the default over +1,896 and +3,393 coins a game on 2 x 384 paired
    real-engine games). A block that owes no pickup no longer waits out the
    BUY row: it opens on turn 1 instead of turn 2, so the same eleven hands
    walk six tiles further into this sweep -- **93 harvests -> 99**, and the
    deficit with them, **88 -> 94**. Measured by flipping that one switch on
    this very board, which still reads 93/88 with it off, so nothing about the
    inflow accounting changed; the crew simply reaches more of the crop.

    What the extra labour does change is the *shape* of the sale. 94 units of
    deficit is more tomato than the shed holds: the forced sale draws on the
    hour-0 stock, so all 90 tomato go and the last 4 come out of the
    next-cheapest product with room to give, the 5 unreserved wheat. Asserted
    as the total plus that split rather than as tomato alone -- tomato alone
    now saturates, and a saturated number would stop tracking the inflow this
    test is named for.
    """
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, ripe=100, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _macro(), TABLE)
    n_reached = int((plan[0] == O.OP_HARVEST).sum())
    assert 0 < n_reached < 100
    sold = _sold(plan)
    assert sold.sum() == n_reached - 5
    # Floored tomato is cheapest at the margin, so it drains first and whole;
    # wheat covers only what 90 units of shed could not.
    assert sold[spec.I_TOMATO] == 90
    assert sold[spec.I_WHEAT] == n_reached - 5 - 90


def test_morning_buys_count_as_inflow_and_are_capped_by_shed_room():
    # 95 in the shed, 10 hungry geese, no wheat: the walk wants 10 wheat but
    # the market only takes what fits at turn 1 -- room is 5 -- so 5 are
    # bought, 5 geese are fed (the other 5 are not: no wheat exists for them),
    # and the wheat lands (100) and is eaten (95). Add 10 units of harvest and
    # 5 must go. Uncapped, the plan would book 10 in and 10 out and reach the
    # same 5 for the wrong reason.
    view = _view({spec.I_TOMATO: 95}, ripe=10, geese=10, tomato_inv=FLOORED)
    plan = P.build_day(np, view, _many_hands(), TABLE)
    op, arg, qty = plan[3:6]
    bought = sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
                 if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_WHEAT)
    assert bought == 5
    assert int((plan[0] == O.OP_FEED).sum()) == 5
    assert _sold(plan)[spec.I_TOMATO] == 5


def test_a_full_shed_buys_nothing_shed_bound():
    # 100 in the shed: room is 0, so no wheat is bought and no feed is planned
    # even with cash and hungry geese; seeds are not shed items and still buy.
    view = _view({spec.I_TOMATO: 100}, ripe=0, geese=10, tomato_inv=FLOORED)
    macro = _many_hands(plant_target=np.array([2, 0, 0, 0, 0], np.int32))
    plan = P.build_day(np, view, macro, TABLE)
    op, qty = plan[3], plan[5]
    row = [(int(op[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s])) for s in range(spec.MAX_MARKET_ORDERS)]
    assert all(q == 0 for o, q in row if o == O.MO_BUY_PRODUCT)
    assert any(o == O.MO_BUY_SEED and q == 2 for o, q in row)
    assert int((plan[0] == O.OP_FEED).sum()) == 0


def test_a_scarce_product_is_not_passed_over_for_a_drained_one():
    """The ranking key must put *drained* products last, whatever a stocked
    product quotes. Scarcity makes quotes enormous -- tomato tops out at
    1,053,252 and passes 116,507 (the price at which `marg * 9 + pid` reaches
    a 1<<20 sentinel) once market inventory falls below 4,887. Town demand
    alone never digs that deep -- a shop eats at most 2 units of a product a
    tick, 6 ticks a day, and the eighth and last shop only unlocks on day 24,
    so a whole episode takes under 1,700 off the 10,000 the market starts
    with -- which is why the board below sets the inventory by hand. The
    sentinel is sized against the price table, not against a plausible
    inventory: with too small a one the argmin picks an empty product, the
    round buys nothing, and the shed overflows anyway -- the exact loss this
    block exists to prevent.

    The reservation has to clear the scarce quote (162,308 at inventory 4,000)
    or the value-gated allocation sells the tomato voluntarily and there is no
    deficit left to rank; 200,000 is well inside the decode's own ceiling of
    2**20 - 1 coins a unit.
    """
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=4_000)
    macro = _many_hands(hold=np.full(spec.N_PRODUCTS, 200_000, np.int32))
    sold = _sold(P.build_day(np, view, macro, TABLE))
    assert sold[spec.I_WHEAT] == 5 and sold[spec.I_TOMATO] == 10


def test_forced_sale_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _view({spec.I_TOMATO: 90, spec.I_WHEAT: 5}, tomato_inv=FLOORED)
    macro = _many_hands()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))


# --- `covered` is an interface, so its rank bound must be monotone -----------
# `_routes` walks `start` unit by unit. An inactive unit takes `end = s - 1`,
# so an ungated `start = end + 1` walks the bound *back* one rank whenever the
# active units already covered the board -- and the next unit that still has
# budget then re-works that tile and counts its pickups in `blk` a second time.
# `covered` is handed forward (section 5's harvest batching reads it), so it
# has to be right, not merely conservative.

def _full_board_routes(n_units, budget=1_000):
    """Every one of the 100 tiles carries one op and one pickup, visited in
    plain serpentine order, with enough turns to reach all of them."""
    chain_op = np.zeros((100, P.CHAIN_MAX), np.int32)
    chain_op[:, 0] = O.OP_WATER
    z = np.zeros((100, P.CHAIN_MAX), np.int32)
    picks = np.zeros((3, 100), bool)
    picks[0, :] = True
    _, _, _, blk, covered, _n_pick, _lead, _early, _banked = P._routes(
        np, chain_op, z, z, np.ones(100, np.int32), np.arange(100, dtype=np.int32),
        np.int32(100), picks, np.int32(n_units), np.int32(budget), np.int32(0))
    return covered, blk


@pytest.mark.parametrize("n_units", [1, 2, 3, 11])
def test_covered_holds_every_tile_when_labour_reaches_the_whole_board(n_units):
    covered, _ = _full_board_routes(n_units)
    assert int(covered.sum()) == 100


@pytest.mark.parametrize("n_units", [1, 2, 3, 11])
def test_covered_and_blk_count_the_same_tiles(n_units):
    covered, blk = _full_board_routes(n_units)
    assert int(covered.sum()) == int(blk.sum()) == 100
