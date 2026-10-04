"""`OPP_SUPPLY_ON`: the measured opponent supply curve in the projector.

Two things are worth a test. Off, nothing moved -- every projector still
returns the town-only expression whether or not the caller hands it a `day`.
On, the projection is the town-only expression plus the curve, cumulated to
the turn being projected, scaled by `OPP_SUPPLY_SCALE`, and identical on both
backends.
"""

from __future__ import annotations

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ
from kagg3.core import sell as S

I0 = spec.MARKET_I0
ONES = np.ones(spec.N_SHOPS, np.int32)
INV = np.full(spec.N_PRODUCTS, I0, np.int32)


def town_only(mkt_inv, shops, turn):
    """The expression `projected_inv` was before the switch existed."""
    shop, center = PJ.ticks_before(turn)
    return (mkt_inv.astype(np.int32)
            - shop * PJ.town_tick_units(np, shops)
            - center * np.asarray(spec.TOWN_CENTER_CONSUME))


@pytest.fixture
def curve(tmp_path):
    """A curve that is 1 unit of WHEAT every turn and 2 of MILK on hour 3."""
    s = np.zeros((spec.EPISODE_STEPS, spec.N_PRODUCTS), np.float32)
    s[:, spec.I_WHEAT] = 1.0
    s[3::spec.TURNS_PER_DAY, spec.I_MILK] = 2.0
    path = tmp_path / "S_test.npy"
    np.save(path, s)
    return str(path)


@pytest.fixture
def switch(curve, monkeypatch):
    """Turn the switch on against `curve`; pytest restores it after."""
    monkeypatch.setattr(P, "OPP_SUPPLY_ON", True)
    monkeypatch.setattr(P, "OPP_SUPPLY_PATH", curve)
    monkeypatch.setattr(P, "OPP_SUPPLY_SCALE", 1.0)
    return curve


# --------------------------------------------------------------------- off

def test_off_is_the_town_only_expression_with_or_without_a_day():
    assert not P.OPP_SUPPLY_ON, "the switch ships off"
    for turn in (0, O.TURN_BUY, *O.SELL_TURNS, O.TURN_PRESTOCK):
        want = town_only(INV, ONES, turn).tolist()
        assert PJ.projected_inv(np, INV, ONES, turn).tolist() == want
        for day in (0, 7, 29):
            assert PJ.projected_inv(np, INV, ONES, turn, day).tolist() == want
    days = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    want = PJ.inv_at_day(np, INV, ONES, days).tolist()
    assert PJ.inv_at_day(np, INV, ONES, days, 12).tolist() == want
    lots = S.lot_inventories(np, INV, ONES).tolist()
    assert S.lot_inventories(np, INV, ONES, day=12).tolist() == lots


def test_off_ignores_the_switch_when_no_day_is_passed(switch):
    """`day=None` is the other half of the off path: a caller that has not
    been taught the day still gets the opponent-free projection."""
    for turn in (O.TURN_BUY, *O.SELL_TURNS):
        assert (PJ.projected_inv(np, INV, ONES, turn).tolist()
                == town_only(INV, ONES, turn).tolist())


# ---------------------------------------------------------------------- on

def test_on_adds_the_curve_cumulated_through_the_projected_turn(switch):
    for day in (0, 11, 29):
        for turn in (0, 3, O.SELL_TURNS[-1]):
            got = PJ.projected_inv(np, INV, ONES, turn, day)
            add = got - town_only(INV, ONES, turn)
            # inclusive of `turn`: both seats' orders resolve in one phase
            assert int(add[spec.I_WHEAT]) == turn + 1
            assert int(add[spec.I_MILK]) == (2 if turn >= 3 else 0)
            assert int(add[spec.I_WOOL]) == 0


def test_on_scales(monkeypatch, switch):
    monkeypatch.setattr(P, "OPP_SUPPLY_SCALE", 0.5)
    add = (PJ.projected_inv(np, INV, ONES, 10, 5)
           - town_only(INV, ONES, 10))
    assert int(add[spec.I_WHEAT]) == 6            # rint(0.5 * 11)
    assert int(add[spec.I_MILK]) == 1             # rint(0.5 * 2)


def test_on_lifts_every_lot_and_the_later_lots_more(switch):
    base = S.lot_inventories(np, INV, ONES)
    lots = S.lot_inventories(np, INV, ONES, day=9)
    add = (lots - base)[:, spec.I_WHEAT]
    assert add.tolist() == [t + 1 for t in O.SELL_TURNS]
    assert add[0] < add[1] < add[2]


def test_on_adds_whole_days_to_the_horizon(switch):
    """`inv_at_day` walks whole days, so it takes the day totals: 24 units of
    wheat and 2 of milk a day, from the current day forward, clipped at the
    end of the season."""
    days = np.full(spec.N_PRODUCTS, 3, np.int32)
    add = PJ.inv_at_day(np, INV, ONES, days, 5) - PJ.inv_at_day(np, INV, ONES, days)
    assert int(add[spec.I_WHEAT]) == 3 * spec.TURNS_PER_DAY
    assert int(add[spec.I_MILK]) == 3 * 2
    far = np.full(spec.N_PRODUCTS, 20, np.int32)
    add = PJ.inv_at_day(np, INV, ONES, far, 25) - PJ.inv_at_day(np, INV, ONES, far)
    assert int(add[spec.I_WHEAT]) == 5 * spec.TURNS_PER_DAY     # clipped at day 30


def test_on_matches_between_numpy_and_jax(switch):
    jnp = pytest.importorskip("jax.numpy")
    a = PJ.projected_inv(np, INV, ONES, 10, 7)
    b = PJ.projected_inv(jnp, jnp.asarray(INV), jnp.asarray(ONES), 10,
                         jnp.asarray(7, jnp.int32))
    assert np.asarray(b).tolist() == a.tolist()
    days = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    a = PJ.inv_at_day(np, INV, ONES, days, 7)
    b = PJ.inv_at_day(jnp, jnp.asarray(INV), jnp.asarray(ONES),
                      jnp.asarray(days), jnp.asarray(7, jnp.int32))
    assert np.asarray(b).tolist() == a.tolist()


def test_shipped_curve_loads_and_is_the_right_shape():
    """The default curve the switch points at, as `extract_opp_supply` wrote
    it. Skipped where the artefact is not in the tree."""
    import os
    if not os.path.exists(P.OPP_SUPPLY_PATH):
        pytest.skip("artifacts/opp_supply not built here")
    s = np.load(P.OPP_SUPPLY_PATH)
    assert s.shape == (spec.EPISODE_STEPS, spec.N_PRODUCTS)
    assert s.sum() > 0        # the field is a net seller
