"""BUY_LAND rides the spare tenth slot of the first SELL turn, after the nine
sells, and is funded by lot-1 revenue (PLANNER_V3_1 M2).

Two things move with it and either alone would justify the change:

* It frees a slot on the BUY row. Turn 1 carried nine orders --
  BUY_PRODUCT x2, BUY_SEED x5, BUY_ANIMAL x1, BUY_LAND -- and the mixed herd
  needs three animal slots, which makes eleven. The engine truncates each
  seat's queue at ten a turn, so the eleventh is silently lost.
* It is what makes a same-day sale able to fund anything at all. The whole BUY
  row resolves at turn 1, ahead of every sell turn, so before this the price of
  a quadrant had to be sitting in the purse at hour 0.

The plan called this "turn 2", which is where lot 1 sat when it was written;
`ops.SELL_TURNS[0]` is turn 3 now that the wide HIRE row occupies turn 2, and
turn 2 is still ahead of every sale.

The funding is a projection and it is guarded twice, because a BUY_LAND that
fails leaves every prospective op of the day no-oping on a still-LOCKED tile
with its seeds already bought. It is discounted (`LAND_REV_NUM /
LAND_REV_DEN`), since the opponent's lockstep sales at the same turn lower the
quotes this seat receives; and the hour-0 purse must still carry `1 /
LAND_OWN_DEN` of the price on its own, so no quadrant is ever bought entirely
on money that has not landed.

The turn is the unlock's: the quadrant opens in the market phase of
`SELL_TURNS[0]`, which runs *after* that turn's unit phase, so no unit may work
before the turn after it. That is charged as a **floor under the pickup turns**
rather than added to them -- a PICKUP needs the shed, not the land -- so a unit
with as many pickup kinds as the lead idles for nothing extra.
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

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
PRICE_0 = int(spec.LAND_PRICES[0])
MO = spec.MAX_MARKET_ORDERS
LAND_TURN = O.SELL_TURNS[0]
LEAD = LAND_TURN + 1 - O.ROUTE_BASE


def _view(money, wool=0, geese_hungry=0, ripe=0, day=6):
    """NW owned, every other quadrant LOCKED, so a purchase really unlocks 25."""
    z = np.zeros(100, np.int32)
    kind = np.where(P.SERP_QUAD == 0, spec.KIND_EMPTY, spec.KIND_LOCKED).astype(np.int32)
    occ, t_cons, t_yield = z - 1, z.copy(), z.copy()
    nw = np.flatnonzero(P.SERP_QUAD == 0)
    for i in nw[:geese_hungry]:
        kind[i], occ[i], t_cons[i] = spec.KIND_COOP, 0, 1
    for i in nw[geese_hungry:geese_hungry + ripe]:
        kind[i], occ[i], t_yield[i] = spec.KIND_PLANT, spec.I_TOMATO, 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = wool
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE.copy())


def _wants_land(**kw):
    """A macro whose gene insists on the quadrant, so these tests measure the
    schedule and the funding rather than the valuation (`test_land_value.py`)."""
    kw.setdefault("land_bias", np.int32(PRICE_0))
    return _macro(**kw)


def _no_land(**kw):
    kw.setdefault("land_bias", np.int32(-PRICE_0))
    return _macro(**kw)


def _land_slots(plan):
    op = plan[3]
    return [(t, s) for t in range(spec.TURNS_PER_DAY) for s in range(MO)
            if int(op[t, s]) == O.MO_BUY_LAND]


def test_land_is_ordered_after_the_sells_of_the_first_sell_turn():
    plan = P.build_day(np, _view(3000), _wants_land())
    assert _land_slots(plan) == [(LAND_TURN, MO - 1)]


def test_the_buy_row_never_carries_land():
    plan = P.build_day(np, _view(3000), _wants_land())
    assert not any(t == O.TURN_BUY for t, _ in _land_slots(plan))


def test_the_turn_one_row_now_has_two_free_slots():
    """The precondition the mixed herd needs: at most eight live BUY orders."""
    macro = _wants_land(animal_want=geese(3),
                        plant_target=np.array([2, 2, 2, 2, 2], np.int32))
    op = P.build_day(np, _view(20_000, geese_hungry=4), macro)[3][O.TURN_BUY]
    assert int((op != O.MO_NONE).sum()) <= MO - 2


def test_the_morning_sale_funds_the_quadrant():
    """800 coins and 20 wool against a 1,000-coin quadrant. Sold at lot 1 the
    wool is thousands even after the 3/4 margin, so the gap is covered; held,
    there is no revenue at all and 800 does not reach the price."""
    macro = _wants_land(hold=np.zeros(spec.N_PRODUCTS, np.int32),
                        plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    assert _land_slots(P.build_day(np, _view(800, wool=20), macro)) == [(LAND_TURN, MO - 1)]
    held = _wants_land(plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    assert _land_slots(P.build_day(np, _view(800, wool=20), held)) == []


def test_the_purse_must_still_carry_half_the_price_itself():
    """A quadrant funded entirely by a projection is the one whose failure is
    total -- seeds bought, ops queued, tiles still LOCKED -- so the hour-0
    purse has to carry `1 / LAND_OWN_DEN` of the price whatever the morning
    might fetch. 400 coins and a shed full of wool buys nothing."""
    macro = _wants_land(hold=np.zeros(spec.N_PRODUCTS, np.int32),
                        plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    assert _land_slots(P.build_day(np, _view(400, wool=60), macro)) == []
    assert P.LAND_OWN_DEN >= 2


def test_turn_one_purchases_leave_the_land_its_gap():
    """1,100 coins, four hungry geese and nothing to sell: whatever the greedy
    spends at turn 1, the land price is still in the purse when turn 3 comes."""
    view = _view(1100, geese_hungry=4)
    macro = _wants_land(plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    plan = P.build_day(np, view, macro)
    op, arg, qty = plan[3:6]
    spent = sum(int(qty[O.TURN_BUY, s]) * int(BASE[int(arg[O.TURN_BUY, s])])
                for s in range(MO) if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT)
    spent += sum(int(qty[O.TURN_BUY, s]) * int(spec.CROP_SEED_COST[int(arg[O.TURN_BUY, s])])
                 for s in range(MO) if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED)
    assert _land_slots(plan) == [(LAND_TURN, MO - 1)]
    assert spent <= 1100 - PRICE_0


def test_units_idle_until_the_quadrant_is_unlocked():
    view = _view(3000, ripe=10, day=13)
    land = P.build_day(np, view, _wants_land())[0]
    no_land = P.build_day(np, view, _no_land())[0]
    assert [int(x) for x in land[0, O.ROUTE_BASE:O.ROUTE_BASE + LEAD]] == [O.OP_PASS] * LEAD
    assert int(land[0, O.ROUTE_BASE + LEAD]) != O.OP_PASS
    assert int(no_land[0, O.ROUTE_BASE]) != O.OP_PASS


def test_every_unit_idles_not_just_the_farmer():
    """Three of the four shed-access spawn tiles lie outside NW, so a hand can
    spawn on a prospective tile and would otherwise work it a turn early."""
    view = _view(20_000, ripe=20, day=13)
    plan = P.build_day(np, view, _wants_land())
    unit_op, mkt_op = plan[0], plan[3]
    n_units = 1 + int((mkt_op == O.MO_HIRE).sum())
    assert n_units > 1, "the fixture hired nobody; it is not testing the hands"
    for u in range(n_units):
        idle = [int(x) for x in unit_op[u, O.ROUTE_BASE:O.ROUTE_BASE + LEAD]]
        assert idle == [O.OP_PASS] * LEAD, f"unit {u} acted before the unlock"


def test_the_terminal_day_buys_no_land_wherever_it_lives():
    view = _view(50_000, wool=40, day=spec.N_DAYS - 1)
    macro = _wants_land(hold=np.zeros(spec.N_PRODUCTS, np.int32))
    assert _land_slots(P.build_day(np, view, macro)) == []


def test_land_at_the_sell_turn_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _view(600, wool=20)
    macro = _wants_land(hold=np.zeros(spec.N_PRODUCTS, np.int32),
                        plant_target=np.array([50, 0, 0, 0, 0], np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
