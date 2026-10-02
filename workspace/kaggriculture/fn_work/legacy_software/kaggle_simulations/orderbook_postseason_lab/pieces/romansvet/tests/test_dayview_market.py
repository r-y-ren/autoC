"""The planner projects prices itself (PLANNER_V3_1 section 1.1), so a DayView
carries the hour-0 market inventory and the town's shops, and build_day takes
the price table the simulator prices with. Defaults keep old fixtures valid.
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
from test_budget_order import _macro, _view

from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import plan as P


def test_dayview_defaults_are_a_fresh_market():
    v = _view(3000)
    assert v.mkt_inv.tolist() == [spec.MARKET_I0] * spec.N_PRODUCTS
    assert v.shops.tolist() == [0] * spec.N_SHOPS


def test_default_price_table_is_cached_and_exact():
    t = P.default_price_table()
    assert t is P.default_price_table()
    assert t.shape == (spec.N_PRODUCTS, spec.PRICE_TABLE_N)
    assert np.array_equal(t, spec.build_price_table())


def test_the_shared_defaults_are_read_only():
    """The defaults are singletons shared by identity across every view and every
    default-table `build_day`, so an in-place write must raise, not spread."""
    v = _view(3000)
    assert v.mkt_inv is _view(1).mkt_inv and v.shops is _view(1).shops
    assert not v.mkt_inv.flags.writeable
    assert not v.shops.flags.writeable
    assert not P.default_price_table().flags.writeable


def test_build_day_default_table_matches_the_explicit_one():
    view, macro = _view(3000), _macro(plant_target=np.array([3, 0, 0, 0, 0], np.int32))
    a = P.build_day(np, view, macro)
    b = P.build_day(np, view, macro, spec.build_price_table())
    for x, y in zip(a, b):
        assert np.array_equal(x, y)


def _obs():
    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    return {
        "day": 4,
        "farms": [{"tiles": tiles, "money": 1234, "unlocked_quadrants": ["NW"], "hands": []}],
        "private": {"shed": {"WHEAT": 2}, "seeds": {}},
        "market": {"prices": {n: 7 for n in spec.PRODUCTS},
                   "inventory": {n: spec.MARKET_I0 - 5 for n in spec.PRODUCTS}},
        "town": {"unlocked_shops": ["BAKERY", "BAKERY", "YARN_STORE"]},
    }


def test_parse_view_carries_market_inventory_and_shops():
    v = parse.parse_view(_obs(), 0)
    assert v.mkt_inv.tolist() == [spec.MARKET_I0 - 5] * spec.N_PRODUCTS
    assert int(v.shops[spec.SHOP_NAMES.index("BAKERY")]) == 2
    assert int(v.shops[spec.SHOP_NAMES.index("YARN_STORE")]) == 1
    assert int(v.shops.sum()) == 3


def test_sim_day_view_carries_the_state_market():
    import jax.numpy as jnp

    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of

    st = initial_state(jnp)
    st = st._replace(mkt_inv=st.mkt_inv - 3, shops=st.shops.at[0].set(2))
    tables = build_tables(jnp)
    v = rollout.day_view(st, 0, jnp.int32(0), prices_of(jnp, tables, st.mkt_inv))
    assert np.asarray(v.mkt_inv).tolist() == [spec.MARKET_I0 - 3] * spec.N_PRODUCTS
    assert int(v.shops[0]) == 2
