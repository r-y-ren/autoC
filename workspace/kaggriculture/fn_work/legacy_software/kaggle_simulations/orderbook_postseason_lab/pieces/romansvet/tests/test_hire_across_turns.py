"""The hand ceiling is the engine's, not one turn's market queue.

`_do_hire` caps nothing: it charges `_fib(hires_today)`, appends a hand and
returns.  The only per-turn limit is `maxMarketOrdersPerTurn` (10), and
`hires_today` resets nightly, so the cumulative fib bill is the whole price of
a crew: 143 coins for ten hands, 376 for twelve, 986 for fourteen, 2,583 for
sixteen.  The old ceiling of ten was the *queue's*, not the engine's -- one
HIRE row in one turn -- and it cost the planner six hands a day against an
opponent that runs twelve.

So HIRE orders are split across two turns: turn 0 takes the first ten and turn
2 the rest, with the BUY row keeping turn 1 to itself and SELL lot 1 moving to
turn 3 to make room.  A hand hired in turn t is appended during turn t's market
phase, after that turn's unit actions, so it first acts in turn t + 1 and has
24 - (t + 1) actions left.  That is why the whole crew starts at
`ROUTE_BASE_WIDE` whenever the turn-2 row is used: every unit has to still be
standing on its spawn tile when the turn-2 hires pick theirs, or
`plan.SPAWN_SLOT` stops describing where they land.
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
from kaggle_environments.envs.kaggriculture import kaggriculture as REF
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: A market that pays the same for every unit at every inventory -- both the
#: quoted price the view carries and the whole table the planner projects with.
#: The hand ceiling is what these tests are about, so the price curve is taken
#: out of the argmax: with a flat quote a tile is worth the same wherever it
#: sits in the sweep, and the only thing that can stop the enumeration short of
#: the ceiling is the ceiling.
FLAT_QUOTE = 500
FLAT_TABLE = np.full((spec.N_PRODUCTS, spec.PRICE_TABLE_N), FLAT_QUOTE, np.int32)
FLAT_PRICE = np.full(spec.N_PRODUCTS, FLAT_QUOTE, np.int32)


def _busy_farm(n=100, money=100_000, day=13):
    """`n` thirsty ripe wheat tiles: WATER then HARVEST, two ops a tile.

    Thirsty (`t_cons = 1`) so the watering is survival work and the tile
    carries two ops rather than one -- 100 tiles then cost more turns than
    even seventeen units can walk, which is what makes the ceiling, and not
    the task list, the binding constraint.
    """
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_cons = z.copy()
    kind[:n], occ[:n], t_yield[:n], t_cons[:n] = spec.KIND_PLANT, spec.I_WHEAT, 6, 1
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(4), price=FLAT_PRICE.copy())


def _plan(view, **macro):
    return P.build_day(np, view, _macro(**macro), FLAT_TABLE)


def _hires(op):
    """Every HIRE the day emits, wherever it sits [1.5]."""
    return int((op == O.MO_HIRE).sum())


def _live_orders(op, turn):
    return int((op[turn] != O.MO_NONE).sum())


def test_the_ceiling_is_the_engines_cumulative_fib_bill():
    assert spec.MAX_HANDS == 16
    assert spec.MAX_UNITS == 17
    bills = P.HIRE_BILLS
    assert [int(bills[n]) for n in (10, 12, 14, 16)] == [143, 376, 986, 2583]


def test_a_day_with_work_for_them_hires_past_ten():
    op = _plan(_busy_farm())[3]
    # Both halves: past one turn's market queue, and all the way to the ceiling.
    assert _hires(op) > spec.MAX_MARKET_ORDERS
    assert _hires(op) == spec.MAX_HANDS


def test_the_hire_rows_are_turn_zero_and_turn_two():
    op = _plan(_busy_farm())[3]
    n = _hires(op)
    per_turn = [int((op[t] == O.MO_HIRE).sum()) for t in range(spec.TURNS_PER_DAY)]
    assert per_turn[O.TURN_HIRE] == min(n, spec.MAX_MARKET_ORDERS)
    assert per_turn[O.TURN_HIRE_WIDE] == max(n - spec.MAX_MARKET_ORDERS, 0)
    assert sum(per_turn) == n


def test_no_turn_ever_exceeds_the_engines_order_queue():
    """`_process_market` truncates each seat's queue to `maxMarketOrdersPerTurn`
    (10). An eleventh order in any turn is silently dropped, so the day's whole
    market schedule has to fit ten orders a turn -- with sixteen hires in it."""
    for view in (_busy_farm(), _busy_farm(n=8), _busy_farm(n=0)):
        op = _plan(view, land_bias=np.int32(spec.LAND_PRICES[0]))[3]
        for t in range(spec.TURNS_PER_DAY):
            assert _live_orders(op, t) <= spec.MAX_MARKET_ORDERS, f"turn {t}"


def test_a_wide_crew_waits_for_the_last_hire_turn():
    """Hands hired in turn 2 do not exist until turn 3, and the ones hired in
    turn 0 must not have *moved off* their spawn tiles before turn 2's hires
    pick theirs -- `_hire` reads the occupancy of the four access tiles.

    That is a law about movement and not about acting, which is the reading
    `ROUTE_SPLIT_ON` (default since 2026-09-03) takes: on a wide day a unit may
    spend turn 2 on a stationary PICKUP, whose BUY row resolved at turn 1, and
    still walk first at `ROUTE_BASE_WIDE`. So the pin is: nothing moves before
    the last hire row, nothing but a PICKUP happens at all, and the walk starts
    where it always did. A narrow day has no second row to wait for, so its
    only floor is `TURN_BUY` -- and turn 0 stays everybody's, hired or not."""
    MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)

    unit_op, _, _, op, _, _ = _plan(_busy_farm())
    assert _hires(op) > spec.MAX_MARKET_ORDERS
    early = unit_op[:, :O.ROUTE_BASE_WIDE]          # turns 0..2, the hire rows'
    assert not np.isin(early, MOVES).any()
    assert np.all((early == O.OP_PASS) | (early == O.OP_PICKUP))
    assert np.all(unit_op[:, :O.TURN_BUY] == O.OP_PASS)
    assert int((unit_op[:, O.ROUTE_BASE_WIDE] != O.OP_PASS).sum()) > 0

    unit_op, _, _, op, _, _ = _plan(_busy_farm(n=8))
    assert 0 < _hires(op) <= spec.MAX_MARKET_ORDERS
    assert np.all(unit_op[:, :O.TURN_BUY] == O.OP_PASS)
    assert int((unit_op[:, O.TURN_BUY] != O.OP_PASS).sum()) > 0
    assert not np.isin(unit_op[:, :O.ROUTE_BASE], O.OP_PICKUP).any()


def test_only_the_hired_units_carry_a_route():
    """`render.turn_action` only renders `len(farm["hands"])` hand actions, and
    the simulator masks the same way, so a route on a unit the day never hired
    is dead weight the two backends have to agree about."""
    unit_op, _, _, op, _, _ = _plan(_busy_farm())
    n_units = 1 + _hires(op)
    assert n_units == spec.MAX_UNITS
    busy = [int((unit_op[u] != O.OP_PASS).sum()) for u in range(spec.MAX_UNITS)]
    assert all(b > 0 for b in busy[:n_units])
    # every unit's block fits the turns it actually has
    assert all(b <= spec.TURNS_PER_DAY - O.ROUTE_BASE_WIDE for b in busy)


def _engine_farm(money):
    return {"money": float(money), "hires_today": 0, "hands": [], "farmer": [4, 4]}


def _engine_hire_turn(farms, privates, orders):
    """Run `_process_market` on a synthetic two-seat state for one turn."""
    market = {"inventory": {n: spec.MARKET_I0 for n in spec.PRODUCTS},
              "prices": {n: 0 for n in spec.PRODUCTS}}

    class _Obs(dict):
        __getattr__ = dict.__getitem__

    class _S:
        def __init__(self, p):
            self.observation = _Obs(market=market, farms=farms, private=privates[p])
            self.action = {"market": orders[p]}

    class _Env:
        configuration = {}

    REF._process_market([_S(0), _S(1)], _Env())


def test_the_engine_really_hires_sixteen_from_a_starting_purse():
    """The ceiling is asserted against the engine itself, not against our
    transcription of it: sixteen HIRE orders split ten / six over two turns,
    resolved by `_process_market`, leave sixteen hands and 3000 - 2583 coins."""
    farms = [_engine_farm(spec.STARTING_MONEY), _engine_farm(spec.STARTING_MONEY)]
    privates = [{"inventories": [{}], "shed": {}, "seeds": {}} for _ in range(2)]
    hire = [["HIRE"]]
    _engine_hire_turn(farms, privates, [hire * 10, []])
    _engine_hire_turn(farms, privates, [hire * 6, []])
    assert len(farms[0]["hands"]) == 16
    assert farms[0]["money"] == spec.STARTING_MONEY - int(P.HIRE_BILLS[16])
    assert len(privates[0]["inventories"]) == 17


def test_a_wide_crew_agrees_across_backends():
    jnp = pytest.importorskip("jax.numpy")
    import jax

    view, macro = _busy_farm(), _macro()
    a = P.build_day(np, view, macro, FLAT_TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(FLAT_TABLE))
    assert _hires(np.asarray(a[3])) == spec.MAX_HANDS
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
