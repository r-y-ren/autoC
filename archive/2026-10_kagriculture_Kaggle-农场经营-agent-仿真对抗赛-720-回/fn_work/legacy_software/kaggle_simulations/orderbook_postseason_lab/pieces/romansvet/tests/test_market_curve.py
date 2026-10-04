"""The price curve, pinned at the points that decide strategy.

These numbers come from the engine's own `market_price`, and the whole port
gathers from a table built once on the host. If that table ever drifts, the
agent's economics change silently, so the values are pinned here rather than
only compared against the reference at a few sampled inventories.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from kaggle_environments.envs.kaggriculture import kaggriculture as REF

from kagg3 import spec
from kagg3.sim.state import floor_inventory


def test_table_matches_reference_over_operating_range():
    tbl = spec.build_price_table()
    rng = np.random.default_rng(0)
    check = np.concatenate([
        np.arange(spec.MARKET_I0 - 4000, spec.MARKET_I0 + 30000),
        rng.integers(spec.PRICE_TABLE_LO, spec.PRICE_TABLE_HI, 2000),
    ])
    for pi, name in enumerate(spec.PRODUCTS):
        mine = tbl[pi][spec.price_index(check)]
        ref = np.array([REF.market_price(name, int(v)) for v in check])
        bad = np.flatnonzero(mine != ref)
        assert len(bad) == 0, f"{name}: {len(bad)} mismatches, first at inv={check[bad[0]]}"


def test_readme_anchor_prices():
    """P(I0-T), P(I0+T), P(I0+2T) from the engine README's table."""
    tbl = spec.build_price_table()
    expected = {
        "WHEAT": (45, 20, 19), "CARROT": (70, 10, 1), "TOMATO": (84, 24, 9),
        "STRAWBERRY": (204, 1, 1), "MELON": (300, 1, 1), "EGG": (70, 40, 39),
        "MILK": (256, 1, 1), "WOOL": (240, 1, 1), "FERTILIZER": (140, 60, 20),
    }
    for pi, name in enumerate(spec.PRODUCTS):
        T = spec.DEFAULT_MARKET_PARAMS[name]["T"]
        I0 = spec.MARKET_I0
        got = tuple(int(tbl[pi][spec.price_index(I0 + d)]) for d in (-T, T, 2 * T))
        assert got == expected[name], f"{name}: got {got}, expected {expected[name]}"


def test_saturation_points():
    """How many units above I0 each product can absorb before hitting $1.

    Premium products collapse almost immediately -- strawberry after 62 units,
    wool after 59, milk after 76 -- while wheat and egg never floor at all
    within the tabulated range. That asymmetry is why the policy needs a
    per-product sell decision rather than a single 'sell everything' rule.
    """
    z = floor_inventory() - spec.MARKET_I0
    got = {name: int(z[i]) for i, name in enumerate(spec.PRODUCTS)}
    assert got["STRAWBERRY"] == 62
    assert got["WOOL"] == 59
    assert got["MILK"] == 76
    assert got["MELON"] == 158
    assert got["FERTILIZER"] == 493
    assert got["TOMATO"] == 529
    assert got["CARROT"] == 842
    # Log curves with a small above_target never reach the floor.
    assert got["WHEAT"] > 60000 and got["EGG"] > 60000
