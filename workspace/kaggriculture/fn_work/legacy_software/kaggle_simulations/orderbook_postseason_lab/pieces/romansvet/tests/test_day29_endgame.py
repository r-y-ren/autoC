"""Day 29 has no end-of-day (PLANNER_V3_1 section 0.4): nothing a unit does can
still monetize, purchases are dead money, and the hour-0 shed is all there is
left to sell -- so it all goes, reservation values ignored. Which lots carry it
is the section-1.2 allocator's answer, not a constant: the reservation is set
to `sell.LIQUIDATE` and the same greedy that runs every other day places the
units by pressure and town ticks.
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

SHED = {spec.I_WHEAT: 10, spec.I_EGG: 7, spec.I_MELON: 3, spec.I_FERT: 4, spec.I_GOOSE: 1}


def _view(day):
    """Five thirsty tomatoes at the head of the sweep, one hungry goose behind
    them, a stocked shed, cash."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:5] = spec.KIND_PLANT
    kind[5] = spec.KIND_COOP
    occ = z - 1
    occ[:5] = spec.I_TOMATO
    occ[5] = 0                      # a goose, unfed yesterday
    t_cons = z.copy()
    t_cons[:6] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    for i, n in SHED.items():
        shed[i] = n
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(5000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _greedy_macro():
    """Asks for everything the macro still carries -- land, seeds, animals --
    and keeps `_macro`'s default reservation value of 10,000 coins a unit,
    which no quote on this board reaches. The reservation is therefore the only
    thing holding the sale back on an ordinary day; the terminal day voids
    it."""
    return _macro(land_bias=np.int32(spec.LAND_PRICES[0]),
                  plant_target=np.array([5, 0, 0, 0, 0], np.int32),
                  animal_want=geese(2))


def _ungated_macro():
    """The same day at zero reservation value, so the only thing that can hold
    a product back is a feed or fertilizer reservation."""
    return _greedy_macro()._replace(hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _stuffed_view(day):
    """A shed already at capacity with 20 ripe tiles behind it: off the
    terminal day the certain inflow alone forces units out."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:20] = spec.KIND_PLANT
    occ = z - 1
    occ[:20] = spec.I_TOMATO
    t_yield = z.copy()
    t_yield[:20] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_TOMATO] = spec.SHED_CAPACITY
    return _view(day)._replace(kind=kind, occ=occ, t_cons=z.copy(),
                               t_yield=t_yield, shed=shed)


def _sold(op, arg, qty, turn):
    return {int(arg[turn, s]): int(qty[turn, s])
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) == O.MO_SELL}


def _sold_all(op, arg, qty):
    """Everything the day sells, summed over the lots.

    Read over every turn of the day and not just `O.SELL_TURNS`:
    `plan.EARLY_SELL_ON` moves lot 1 onto the BUY row, and the day's *total*
    is what the liquidation law is about
    (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`)."""
    out = {}
    for turn in range(spec.TURNS_PER_DAY):
        for item, n in _sold(op, arg, qty, turn).items():
            out[item] = out.get(item, 0) + n
    return out


def _ripe_view(day):
    """The same board with twelve ripe tomatoes in front of it -- work a DROP
    day can actually monetize, and the reason `_view` alone cannot tell the two
    laws apart: it has nothing ripe, so day 29 idles under either switch."""
    v = _view(day)
    kind = v.kind.copy(); occ = v.occ.copy(); t_yield = v.t_yield.copy()
    kind[6:18] = spec.KIND_PLANT
    occ[6:18] = spec.I_TOMATO
    t_yield[6:18] = 3
    return v._replace(kind=kind, occ=occ, t_yield=t_yield)


def _walk(unit_op, u):
    """Where unit `u` stands after each of its ops, from its spawn tile."""
    x, y = int(P.SPAWN_X[u]), int(P.SPAWN_Y[u])
    out = []
    for op in unit_op[u]:
        dx, dy = O.MOVE_DELTA.get(int(op), (0, 0))
        x, y = x + dx, y + dy
        out.append((x, y))
    return out


def test_day_29_emits_no_unit_ops(monkeypatch):
    """With the switch off, the terminal law is the one it always was."""
    monkeypatch.setattr(P, "DROP_ON", False)
    for view in (_view(29), _ripe_view(29)):
        assert np.all(P.build_day(np, view, _greedy_macro())[0] == O.OP_PASS)


def test_day_29_works_nothing_that_cannot_monetize_even_with_drop(monkeypatch):
    """DROP gives day 29 its crew back, not a licence to develop.

    Nothing planted, built or placed on day 29 ever fires, and `_derive` prices
    all three at exactly 0 -- but a PLACE still puts its animal in the day's
    pickup kinds and charges *every* unit a turn for it. `_worth_a_turn` cuts
    them, so a board with nothing ripe still idles.
    """
    monkeypatch.setattr(P, "DROP_ON", True)
    assert np.all(P.build_day(np, _view(29), _greedy_macro())[0] == O.OP_PASS)


def test_day_29_harvests_walks_home_and_drops(monkeypatch):
    """The section-4 chain, end to end on the planner's own arrays."""
    monkeypatch.setattr(P, "DROP_ON", True)
    view = _ripe_view(29)
    unit_op, _, _, op, arg, qty = P.build_day(np, view, _greedy_macro())
    assert int((unit_op == O.OP_HARVEST).sum()) > 0, "day 29 must work its ripe tiles"
    # The crew is hired again, through the ordinary enumeration.
    assert int(qty[O.TURN_HIRE].sum()) > 0

    access = {tuple(xy) for xy in spec.SHED_ACCESS_XY}
    dropped = 0
    for u in range(spec.MAX_UNITS):
        turns = [t for t in range(spec.TURNS_PER_DAY) if int(unit_op[u, t]) == O.OP_DROP]
        if not turns:
            assert int((unit_op[u] != O.OP_PASS).sum()) == 0, \
                f"unit {u} worked but never banked its load"
            continue
        assert len(turns) == 1, f"unit {u} drops {len(turns)} times"
        t = turns[0]
        # A unit acts before its turn's market, so turn 18 itself still sells.
        assert t <= O.SELL_TURNS[-1], f"unit {u} drops at {t}, past the last lot"
        assert _walk(unit_op, u)[t] in access, f"unit {u} drops away from the shed"
        # The DROP is the last thing the unit does.
        assert np.all(unit_op[u, t + 1:] == O.OP_PASS)
        dropped += 1
    assert dropped > 0

    # ... and the last lot offers what the route banks, which the hour-0 shed
    # does not hold: `_view`'s shed carries no tomato at all.
    assert view.shed[spec.I_TOMATO] == 0
    assert _sold(op, arg, qty, O.SELL_TURNS[-1]).get(spec.I_TOMATO, 0) > 0
    # ... and no earlier row can carry it, wherever `plan.EARLY_SELL_ON` stands
    # the first lot: until the DROP the tomato is in a unit's hands, not the shed.
    assert sum(_sold(op, arg, qty, t).get(spec.I_TOMATO, 0)
               for t in range(O.SELL_TURNS[-1])) == 0


def test_day_29_hires_and_buys_nothing():
    op, _, qty = P.build_day(np, _view(29), _greedy_macro())[3:6]
    for turn in O.HIRE_TURNS:
        assert np.all(op[turn] == O.MO_NONE) and int(qty[turn].sum()) == 0
    # The BUY row is shared: `plan.EARLY_SELL_ON` packs the day's first lot in
    # behind the purchases, and on the terminal day the lot is the whole row. So
    # what the law says is that nothing on it is a *purchase*, not that it is empty.
    buy_row = op[O.TURN_BUY]
    assert np.all((buy_row == O.MO_NONE) | (buy_row == O.MO_SELL))
    assert int(qty[O.TURN_BUY][buy_row != O.MO_SELL].sum()) == 0
    # ... and no land, wherever the schedule puts it: the terminal day's SELL
    # rows are live, so this is asserted over the whole block rather than by
    # blanking a turn.
    assert not np.any(op == O.MO_BUY_LAND)


def test_day_29_liquidates_the_whole_shed():
    """Every unit leaves, whichever lots the allocator picks: reservation value
    and feed reservation are both void, and the goose is not a market product."""
    op, arg, qty = P.build_day(np, _view(29), _greedy_macro())[3:6]
    assert _sold_all(op, arg, qty) == {
        spec.I_WHEAT: 10, spec.I_EGG: 7, spec.I_MELON: 3, spec.I_FERT: 4}


def test_day_27_is_not_terminal():
    unit_op, _, _, op, arg, qty = P.build_day(np, _view(27), _greedy_macro())
    assert int((unit_op == O.OP_WATER).sum()) >= 5      # 5 survival waterings, plus plant-then-water
    assert int((unit_op == O.OP_FEED).sum()) == 1       # the goose still eats
    assert int(qty[op == O.MO_BUY_LAND].sum()) == 1     # M2: on the first SELL turn
    assert _sold_all(op, arg, qty) == {}                # every quote is under the reservation


def test_day_27_reserves_the_feed_wheat_that_the_endgame_sells():
    """The other half of the terminal law: on day 27 the goose's wheat is held
    back from an *ungated* sale, and once survival stops paying the reservation
    is void and all 10 go. With `HORIZON_DROP_ON` day 29 is a pay day, so day 28
    still feeds (section 0.4 through `valuation.pay_day`) and the reservation
    lifts only on the terminal day. Same board, same macro; only the horizon
    differs."""
    for day in (27, 28):
        sold = _sold_all(*P.build_day(np, _view(day), _ungated_macro())[3:6])
        assert sold[spec.I_WHEAT] == 9                  # 10 in the shed, 1 reserved
    d29 = _sold_all(*P.build_day(np, _view(29), _ungated_macro())[3:6])
    assert d29[spec.I_WHEAT] == 10


def test_day_29_forces_nothing_on_top_of_the_liquidation(monkeypatch):
    """The overflow projection (section 0.9) reads a route the terminal day
    plans for itself, so it is gated off: a full shed and 20 units of would-be
    inflow force nothing.

    What the day offers is the hour-0 shed, and the only thing on top of it is
    what day 29's own DROP banks into the last lot -- `DROP_ON`'s return-leg
    `gain`, added to `SELL_TURNS[-1]` by the same branch
    `test_day_29_harvests_walks_home_and_drops` reads. Since 1d03376 gave the
    block its split start the terminal crew has the turns to reach some of the
    twenty ripe tiles, so that gain is no longer zero; every row *before* the
    last lot is still the hour-0 shed and nothing else, which is where a live
    projection would have put its forced units. Pin the DROP off and the sale
    is exactly the hour-0 shed, the shape this test was written against.

    The same board one day earlier does force, so the gate is not vacuous.
    """
    op, arg, qty = P.build_day(np, _stuffed_view(29), _greedy_macro())[3:6]
    banked = _sold(op, arg, qty, O.SELL_TURNS[-1]).get(spec.I_TOMATO, 0)
    assert banked <= 20 and (banked > 0) == P.DROP_ON   # the DROP's own return leg
    assert _sold_all(op, arg, qty) == {spec.I_TOMATO: spec.SHED_CAPACITY + banked}
    assert sum(_sold(op, arg, qty, t).get(spec.I_TOMATO, 0)
               for t in range(O.SELL_TURNS[-1])) == spec.SHED_CAPACITY
    with monkeypatch.context() as m:
        m.setattr(P, "DROP_ON", False)
        assert _sold_all(*P.build_day(np, _stuffed_view(29), _greedy_macro())[3:6]) \
            == {spec.I_TOMATO: spec.SHED_CAPACITY}
    d28 = _sold_all(*P.build_day(np, _stuffed_view(28), _greedy_macro())[3:6])
    assert d28.get(spec.I_TOMATO, 0) > 0                # gated, but forced out


def test_terminal_plan_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(29), _greedy_macro()
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view), jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
