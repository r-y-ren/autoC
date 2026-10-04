"""Feed wheat and fertilizer are bought along the engine's price curve
(PLANNER_V3_1 section 0.10): every unit drains the market and re-quotes, and
the engine stops at the first unit the purse cannot pay. The walk must commit
exactly what the engine will honour.
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
from kagg3.core import projector as PJ
from kagg3.sim import market as M
from kagg3.sim.state import Tables

TABLE = spec.build_price_table()


def _view(n_hungry, money, wheat_inv=spec.MARKET_I0, shops=None):
    """`n_hungry` geese that must be fed today, no wheat in the shed, so the
    walk wants exactly `n_hungry` wheat."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:n_hungry] = spec.KIND_COOP
    occ = z - 1
    occ[:n_hungry] = 0
    t_cons = z.copy()
    t_cons[:n_hungry] = 1
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    inv[spec.I_WHEAT] = wheat_inv
    return P.DayView(
        day=np.int32(5), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        mkt_inv=inv, shops=np.zeros(spec.N_SHOPS, np.int32) if shops is None else shops)


def _wheat_bought(view):
    op, arg, qty = P.build_day(np, view, _macro(), TABLE)[3:6]
    row = O.TURN_BUY
    return sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[row, s]) == O.MO_BUY_PRODUCT and int(arg[row, s]) == spec.I_WHEAT)


def _purse(view):
    """What the BUY row actually gets to spend: `view.money` less the fib bill
    of the crew 1.5 hires and the coins `plan.cash_reserve` keeps back for
    tomorrow's. Read off the plan's own hire row, not assumed."""
    op = P.build_day(np, view, _macro(), TABLE)[3]
    n = int((op == O.MO_HIRE).sum())
    return int(view.money) - int(spec.HIRE_COST[:n].sum()) \
        - int(P.cash_reserve(np, np.int32(n), view.day))


def _engine_affords(view, n, money):
    inv1 = PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY)
    k, cost = M.buy_walk(np, Tables(price=TABLE), spec.I_WHEAT, int(inv1[spec.I_WHEAT]),
                         n, money, M.M_BUY_SOLO)
    return int(k), int(cost)


def test_walk_commits_what_the_curve_affords():
    # 30 hungry geese, 750 coins: the flat hour-0 price (25) would commit all
    # 30, but the curve rises as the market drains and the engine stops short.
    # The walk is priced against the *purse*, which is what is left of the 750
    # once the day has hired and reserved.
    view = _view(30, 750)
    purse = _purse(view)
    assert 0 < purse < 750
    k, cost = _engine_affords(view, 30, purse)
    assert k < 30 and cost <= purse
    assert _wheat_bought(view) == k


def test_a_rich_purse_still_buys_everything():
    view = _view(30, 100_000)
    assert _wheat_bought(view) == 30


def test_turn_zero_town_tick_is_charged():
    # Two bakeries drain wheat at turn 0 before the BUY row resolves at turn 1.
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("BAKERY")] = 2
    view = _view(30, 750, shops=shops)
    k, _ = _engine_affords(view, 30, 750)
    assert _wheat_bought(view) == k


def test_buy_quotes_are_the_engine_walk():
    tables = Tables(price=TABLE)
    rng = np.random.default_rng(0)
    for _ in range(40):
        item = int(rng.integers(0, spec.N_PRODUCTS))
        inv = int(rng.integers(spec.MARKET_I0 - 2000, spec.MARKET_I0 + 30000))
        n = int(rng.integers(0, spec.SHED_CAPACITY + 1))
        q = PJ.buy_quotes(np, TABLE, np.full(spec.N_PRODUCTS, inv, np.int32))[item]
        k, cost = M.buy_walk(np, tables, item, inv, n, 10**9, M.M_BUY_SOLO)
        assert int(np.cumsum(q)[k - 1]) == int(cost) if k > 0 else int(cost) == 0


def test_curve_pricing_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view, macro = _view(30, 750), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
