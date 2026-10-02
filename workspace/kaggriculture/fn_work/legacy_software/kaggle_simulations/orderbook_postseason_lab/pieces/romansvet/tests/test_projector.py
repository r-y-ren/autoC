"""The opponent-free price projector (PLANNER_V3_1 section 1.1) is exact table
arithmetic: its quotes must equal the simulator's market walk unit for unit,
and its town-tick schedule must equal the rollout's.
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

from kagg3 import spec
from kagg3.core import projector as PJ
from kagg3.sim import market as M
from kagg3.sim.state import Tables

TABLE = spec.build_price_table()


def test_ticks_before_each_market_turn():
    assert PJ.ticks_before(0) == (0, 0)
    assert PJ.ticks_before(1) == (1, 1)      # turn 0's shop tick and centre tick
    assert PJ.ticks_before(2) == (1, 1)
    assert PJ.ticks_before(10) == (3, 1)     # shop ticks at 0, 4, 8
    assert PJ.ticks_before(18) == (5, 1)     # 0, 4, 8, 12, 16


def test_projected_inventory_matches_the_sim_town_tick():
    import jax.numpy as jnp

    from kagg3.sim import rollout
    from kagg3.sim.state import initial_state
    shops = np.zeros(spec.N_SHOPS, np.int32)
    shops[spec.SHOP_NAMES.index("BAKERY")] = 1
    shops[spec.SHOP_NAMES.index("YARN_STORE")] = 2
    st = initial_state(jnp)._replace(shops=jnp.asarray(shops))
    inv0 = np.asarray(st.mkt_inv)
    for turn in (1, 2, 10, 18):
        s = st
        for _ in range(turn):
            s = rollout.town_consume(s)._replace(step=s.step + 1)
        assert np.asarray(s.mkt_inv).tolist() == PJ.projected_inv(np, inv0, shops, turn).tolist()


def test_sell_quotes_match_the_engine_walk():
    tables = Tables(price=TABLE)
    rng = np.random.default_rng(0)
    for _ in range(60):
        item = int(rng.integers(0, spec.N_PRODUCTS))
        inv = int(rng.integers(spec.MARKET_I0 - 2000, spec.MARKET_I0 + 30000))
        n = int(rng.integers(0, spec.SHED_CAPACITY + 1))
        quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, inv, np.int32))
        qty = np.zeros(spec.N_PRODUCTS, np.int32)
        qty[item] = n
        _, revenue, _ = M.sell_walk(np, tables, item, inv, n, M.M_SELL_SOLO)
        assert int(PJ.sell_revenue(np, quotes, qty)[item]) == int(revenue)


def test_quotes_are_monotone_non_increasing():
    quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32))
    assert quotes.shape == (spec.N_PRODUCTS, PJ.K)
    assert np.all(np.diff(quotes, axis=1) <= 0)


def test_marginal_quote_is_the_next_unit():
    quotes = PJ.sell_quotes(np, TABLE, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32))
    sold = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    assert PJ.marginal_quote(np, quotes, sold).tolist() == [int(quotes[p, p]) for p in range(spec.N_PRODUCTS)]


def test_sell_revenue_is_int32_on_both_backends():
    """`np.cumsum` upcasts an int32 input to int64 while `jnp.cumsum` keeps
    int32, so `sell_revenue`'s accumulator dtype is pinned rather than
    inherited -- otherwise the numpy submission and the jitted sim would carry
    a different dtype into any decision path that consumes the revenue.
    """
    import jax.numpy as jnp
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
    qty = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 11        # 0 .. 88 units
    a = PJ.sell_revenue(np, PJ.sell_quotes(np, TABLE, inv), qty)
    b = PJ.sell_revenue(jnp, PJ.sell_quotes(jnp, jnp.asarray(TABLE), jnp.asarray(inv)),
                        jnp.asarray(qty))
    assert a.tolist() == np.asarray(b).tolist()
    assert int(a[-1]) > 0                                        # not a row of zeros
    assert a.dtype == np.int32 and np.asarray(b).dtype == np.int32


def test_projector_agrees_across_backends():
    import jax.numpy as jnp
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0 + 40, np.int32)
    shops = np.ones(spec.N_SHOPS, np.int32)
    a = PJ.sell_quotes(np, TABLE, PJ.projected_inv(np, inv, shops, 10))
    b = PJ.sell_quotes(jnp, jnp.asarray(TABLE), PJ.projected_inv(jnp, jnp.asarray(inv), jnp.asarray(shops), 10))
    assert a.tolist() == np.asarray(b).tolist()
