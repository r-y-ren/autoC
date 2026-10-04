"""The end-of-day shed drop must discard the same units the engine discards.

The engine walks each unit's inventory dict in insertion order and stops adding
when the shed is full; which items survive an overflow is therefore a function
of *both* unit order and per-unit acquisition order. `eod.drop_inventories`
models that with a sort key per (unit, item).

Found 2026-08-22 while adding the sell price gate: a gated product stops being
sold, the shed fills, and then a seat-1 overflow kept the wrong item. The key
was built as `[MU, NI] + seq[2, MU, NI]`, i.e. both seats' keys flattened into
one 264-entry array, sorted, and used to index a 132-entry inventory -- JAX
clamps the out-of-range indices silently where numpy would raise. Nothing in
the suite ever filled a shed before.

The second half of the file is the planner's side of the same law:
`plan.SHED_OVERFLOW_ON`, the guard that keeps the projected end-of-day shed
inside `SHED_CAPACITY` by selling what would otherwise be discarded. Note what
the engine call above pins -- `_drop_inventories_to_shed(private,
spec.SHED_CAPACITY)` against `sum(shed)` -- the cap is a **total** over the
shed's twelve slots, not a per-item one.
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
import jax.numpy as jnp
from kaggle_environments.envs.kaggriculture import kaggriculture as REF

from kagg3 import spec
from kagg3.sim import eod
from kagg3.sim.state import initial_state

ITEMS = list(spec.ITEMS)


def _engine_drop(shed, inventories):
    private = {"shed": {ITEMS[i]: int(n) for i, n in enumerate(shed) if n},
               "inventories": [dict(inv) for inv in inventories]}
    REF._drop_inventories_to_shed(private, spec.SHED_CAPACITY)
    return np.array([private["shed"].get(n, 0) for n in ITEMS], np.int32)


def _sim_state(sheds, inventories, seqs):
    """`inventories[p]` is a list per unit of (item, n, seq) in acquisition order."""
    MU, NI = spec.MAX_UNITS, spec.N_ITEMS
    inv = np.zeros((2, MU, NI), np.int32)
    seq = np.full((2, MU, NI), 1 << 20, np.int32)
    for p in range(2):
        for u, items in enumerate(inventories[p]):
            for item, n, s in items:
                inv[p, u, ITEMS.index(item)] = n
                seq[p, u, ITEMS.index(item)] = s
    st = initial_state(jnp)
    return st._replace(shed=jnp.asarray(np.array(sheds, np.int32)),
                       inv=jnp.asarray(inv), inv_seq=jnp.asarray(seq))


def test_overflow_keeps_what_the_engine_keeps_for_both_seats():
    # Seat 1 is the one that used to go wrong: its keys were sorted in with
    # seat 0's. Give the two seats different acquisition orders so a shared
    # sort cannot be right for both.
    shed0 = np.zeros(spec.N_ITEMS, np.int32); shed0[ITEMS.index("WHEAT")] = 93
    shed1 = np.zeros(spec.N_ITEMS, np.int32); shed1[ITEMS.index("TOMATO")] = 92   # room 8: the cut lands inside unit 2
    inv0 = [[("EGG", 3, 410), ("FERTILIZER", 2, 412)],
            [("TOMATO", 4, 405), ("EGG", 1, 411)]]
    inv1 = [[("STRAWBERRY", 1, 429)],
            [("STRAWBERRY", 1, 421), ("FERTILIZER", 2, 426), ("EGG", 2, 427)],
            [("TOMATO", 1, 422), ("FERTILIZER", 1, 427), ("EGG", 1, 428)],
            [("TOMATO", 1, 417), ("FERTILIZER", 1, 422), ("EGG", 1, 423)]]
    st = _sim_state([shed0, shed1], [inv0, inv1], None)
    out = eod.drop_inventories(jnp, st)

    def as_dicts(inv):
        return [{item: n for item, n, _ in sorted(u, key=lambda t: t[2])} for u in inv]

    for p, (shed, inv) in enumerate([(shed0, inv0), (shed1, inv1)]):
        want = _engine_drop(shed, as_dicts(inv))
        assert np.asarray(out.shed[p]).tolist() == want.tolist(), f"seat {p}"
        assert int(np.asarray(out.shed[p]).sum()) == spec.SHED_CAPACITY


# =========================================================================
# `plan.SHED_OVERFLOW_ON`: sell the reservations the route never reaches
# =========================================================================
#
# Section 0.9's forced sale is the answer to most of the destruction above, and
# the switch does not replace it -- it repairs the one place it is blind. 0.9
# may draw only on `avail`, the hour-0 shed net of the day's reservations, and
# those reservations are sized on the *queued* demand: one wheat per
# `want_feed` tile, `n_fert_eff` applications. The route then picks up only what
# the blocks it reached consume (`blk`), which is exactly what `proj_eod`
# charges as `picks_out`. So stock reserved for a task the day never walks to is
# counted as staying in the shed by the projection and hidden from the sale by
# the reservation at the same time: nothing consumes it, nothing may sell it,
# and end-of-day destroys it to make room for the harvest.
#
# The boards below are that gap in the small: on `LAST_SHED_DAY` a harvest is
# mandatory-tier work, so the route sweeps the ripe tiles at the head of the
# board and never reaches the sixty hungry geese behind them -- whose sixty
# wheat stay reserved, unsold and doomed all the same.
#
# Selling is the only lever and there is no second choice: DROP discards the
# part of a load that does not fit exactly as `_end_of_day` does (`sim/units.py`
# `d_take` against the `take` this file pins above), so explicitly dropping the
# surplus banks the same coins as letting the night take it and costs the walk
# home on top. What the sale cannot reach stays in section 7's
# `overflow_destroyed`.
#
# Not measured in the real engine yet: OFF is the default, and OFF `lots` and
# the metric are the expressions they always were.

import pytest
from test_budget_order import _macro

from kagg3.core import ops as O
from kagg3.core import plan as P

LAST = O.LAST_SHED_DAY                                   # 28
WHEAT = 90                                               # what the shed holds
COOPS = 60                                               # ... of which this many are reserved

#: What `build_day_stats(...).overflow_destroyed` reads on `_view()` with the
#: switch OFF. It is a *projection*, not a count taken from a replay:
#: `_plan_and_stats` builds `proj_eod = sum(shed) - sold - picks_out + buys_in
#: + inflow`, `deficit = max(proj_eod - SHED_CAPACITY, 0)`, and reports
#: `overflow_destroyed = max(deficit - sum(forced), 0)` -- the part of tonight's
#: projected overflow that 0.9's forced sale could not absorb, because the shed
#: it may draw on is the hour-0 stock net of the day's *queued* reservations.
#: OFF, nothing in the plan reads it: it is the diagnostic the switch exists to
#: drive to zero.
#:
#: On this board it is arithmetic on one number, the day's harvest `inflow`:
#: shed 90, sold 30 (`WHEAT - COOPS`, all 0.9 may reach), no pickups and no
#: buys, cap 100. `proj_eod = 60 + inflow`, so `overflow_destroyed = inflow -
#: 40`, ten units per ripe tomato tile the route sweeps at `yld=10`.
#:
#: 30 until 1d03376 (`ROUTE_SPLIT_ON` promoted to the default, +1,896/+3,393
#: coins a game over 2 x 384 paired real-engine games): the crew's first block
#: no longer waits on a BUY row it does not need, so the one unit this empty
#: purse fields starts on turn 1 instead of turn 2 and reaches an eighth ripe
#: tile. `inflow` 70 -> 80 and the projection follows. That commit re-based
#: nine test files on the new budget and missed this one; nothing about the
#: overflow machinery moved, and the extra ten units are harvest *gained* --
#: on this contrived board they have nowhere to go, which is exactly the gap
#: the switch below closes (ON sells 40, not 30).
DOOMED = 40


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", True)


def _view(day=LAST, n_ripe=20, n_coop=COOPS, wheat=WHEAT, yld=10, lead_coops=0, money=0):
    """`n_ripe` ripe tomatoes at the head of the sweep, `n_coop` hungry geese
    behind them, `wheat` in the shed and nothing else.

    On `LAST_SHED_DAY` a harvest is mandatory-tier work [0.5], so the single
    unit the empty purse can field sweeps the ripe tiles and never reaches the
    coops -- while the day still reserves one wheat for every hungry animal.
    `lead_coops` moves that many coops in *front* of the ripe tiles, where the
    route does reach them, which is what pins the reservation the switch must
    keep."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_cons = z.copy()
    lo = lead_coops
    kind[:lo] = spec.KIND_COOP
    occ[:lo] = 0                                          # geese, unfed yesterday
    t_cons[:lo] = 1
    kind[lo:lo + n_ripe] = spec.KIND_PLANT
    occ[lo:lo + n_ripe] = spec.I_TOMATO
    t_yield[lo:lo + n_ripe] = yld
    hi = lo + n_ripe
    kind[hi:hi + n_coop] = spec.KIND_COOP
    occ[hi:hi + n_coop] = 0
    t_cons[hi:hi + n_coop] = 1
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(1),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _plan(view):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro()))


def _plans(monkeypatch, view, guard):
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", guard)
    return _plan(view)


def _sold(view):
    """Everything the day sells, summed over the lots.

    Read over every turn of the day and not just `O.SELL_TURNS`:
    `plan.EARLY_SELL_ON` moves lot 1 onto the BUY row, and the day's *total*
    is what this file is about
    (`tests/test_early_sell.py::test_on_daily_total_sold_is_unchanged`)."""
    _, _, _, op, arg, qty = _plan(view)
    out = {}
    for turn in range(spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(op[turn, s]) == O.MO_SELL:
                out[int(arg[turn, s])] = out.get(int(arg[turn, s]), 0) + int(qty[turn, s])
    return out


def _picked_up(view, item):
    unit_op, unit_a, unit_q = _plan(view)[:3]
    return int(unit_q[(unit_op == O.OP_PICKUP) & (unit_a == item)].sum())


def _destroyed(view):
    return int(P.build_day_stats(view, _macro()).overflow_destroyed)


# ---------------------------------------------------------------- switch OFF

def test_off_sells_only_what_the_reservation_left(off):
    """The gap, pinned. Sixty of the ninety wheat are reserved for feeds the
    route never walks to, so 0.9 may force-sell only thirty -- and the night
    destroys `DOOMED` units of the harvest for want of exactly the room those
    sixty occupy. See `DOOMED` for what the number is and why it moved."""
    view = _view()
    assert _picked_up(view, spec.I_WHEAT) == 0, "the route must not reach a single feed"
    assert _sold(view) == {spec.I_WHEAT: WHEAT - COOPS}
    assert _destroyed(view) == DOOMED


def test_off_is_the_plan_it_always_was(monkeypatch):
    """OFF, `overflow_left` is `deficit - sum(forced)` and `lots` is untouched:
    the block adds no expression the plan can see."""
    view = _view()
    a = _plans(monkeypatch, view, False)
    b = _plans(monkeypatch, view, False)
    for i, (x, y) in enumerate(zip(a, b)):
        assert np.array_equal(x, y), f"plan array {i} is not stable"


# ---------------------------------------------------------------- switch ON

@pytest.mark.parametrize("view", [
    pytest.param(_view(yld=4), id="harvest-fits"),
    pytest.param(_view(day=13, yld=4), id="ordinary-day"),
    pytest.param(_view(day=spec.N_DAYS - 1), id="terminal-day"),
])
def test_the_switch_moves_no_day_that_does_not_overflow(monkeypatch, view):
    """`overflow_left` is zero wherever 0.9's deficit is zero -- including the
    terminal day, where the projection is gated off because there is no
    end-of-day left to destroy anything -- so the greedy adds nothing."""
    assert _destroyed(view) == 0
    a = _plans(monkeypatch, view, False)
    b = _plans(monkeypatch, view, True)
    for i, (x, y) in enumerate(zip(a, b)):
        assert np.array_equal(x, y), f"plan array {i} moved on a day that does not overflow"


def test_on_leaves_the_night_nothing_to_destroy(on):
    """What the switch is for: the projected end-of-day shed is back inside
    `SHED_CAPACITY`."""
    assert _destroyed(_view()) == 0


def test_on_sells_the_surplus_instead_of_dropping_it(monkeypatch):
    """Sold, not dropped -- and exactly the `DOOMED` units the night was going
    to take, out of the sixty the reservation was hiding."""
    view = _view()
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", False)
    off_sold = _sold(view)
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", True)
    on_sold = _sold(view)
    assert on_sold[spec.I_WHEAT] == off_sold[spec.I_WHEAT] + DOOMED
    assert not np.any(_plan(view)[0] == O.OP_DROP), \
        "the guard must reach the surplus through a lot, never through a DROP"


def test_on_keeps_the_reservation_of_every_task_the_route_reaches(on):
    """The reservation still holds where it means something. On an ordinary day
    a survival feed is mandatory-tier work, so the four coops in front of the
    ripe tiles are fed -- and the four wheat that PICKUP takes may never be
    sold out from under them, however hard the shed is overflowing."""
    view = _view(day=13, lead_coops=4, n_coop=0, yld=100)
    picked = _picked_up(view, spec.I_WHEAT)
    assert picked > 0, "the board must actually reach a feed"
    assert _destroyed(view) >= 0 and _sold(view).get(spec.I_WHEAT, 0) == WHEAT - picked, \
        "the guard offers everything the day does not consume, and not one unit more"


def test_the_sale_still_stops_at_the_shed(on):
    """The guard offers what nothing consumes and not one unit more: a harvest
    that overshoots the whole shed still overflows, and 0.9's report of it is
    what harvest batching (section 5) would have to read."""
    view = _view(yld=20)
    assert _sold(view) == {spec.I_WHEAT: WHEAT}, "the whole shed, and only the shed"
    assert _destroyed(view) > 0


def test_the_switch_moves_no_other_metric(monkeypatch):
    """It is a sale, not a labour decision: the route, the purchases and their
    two metrics are the ones the day already had."""
    view = _view()
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", False)
    a = P.build_day_stats(view, _macro())
    b_units = _plan(view)[:3]
    monkeypatch.setattr(P, "SHED_OVERFLOW_ON", True)
    b = P.build_day_stats(view, _macro())
    a_units = _plan(view)[:3]
    assert int(a.purchase_shortfall) == int(b.purchase_shortfall)
    assert int(a.value_dropped) == int(b.value_dropped)
    for i, (x, y) in enumerate(zip(a_units, b_units)):
        assert np.array_equal(x, y), f"unit array {i} moved"


# ---------------------------------------------------------------- backends

def test_the_overflow_plan_agrees_across_backends(on):
    """The block runs a nine-round argmin greedy over traced scalars; it must
    not split the two planner backends."""
    import jax.numpy as jnp

    view = _view()
    jview = view._replace(**{f: jnp.asarray(getattr(view, f))
                             for f in type(view)._fields})
    macro = _macro()
    jmacro = macro._replace(**{f: jnp.asarray(getattr(macro, f))
                               for f in type(macro)._fields})
    a = _plan(view)
    b = tuple(np.asarray(x) for x in P.build_day(jnp, jview, jmacro))
    for i, (x, y) in enumerate(zip(a, b)):
        assert np.array_equal(x, y), f"backends disagree on plan array {i}"
