"""A quadrant is priced in coins like everything else the day buys.

Before this, `buy_land` was a blind gene and land was a pure cost: `_derive`
deducted the price from the purse and booked the quadrant no value at all, so
the value model could only ever see a purchase as a loss and the learned logit
was the only thing that could ever ask for one. Here the quadrant is valued as
the candidates its 25 tiles admit -- the seed and animal ranks past each list's
pre-land want, priced on the very arrays the greedy is about to use -- and the
gene survives as a *coin bias* scaled to the quadrant's own price, zero at
z = 0. So a policy that has learned nothing buys land exactly when land pays.

The horizon comes out for free and without a day constant: `new_plant_units`
returns 0 for a crop that cannot mature and `fires_between` empties for a late
animal, so late in the season every candidate behind the wall is worth nothing
and the valuation collapses to zero on its own.
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
from kagg3.core import brain
from kagg3.core import budget as BUD
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import projector as PJ
from kagg3.core import valuation as VAL

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
PRICE_0 = int(spec.LAND_PRICES[0])
#: The last day on which the quadrant behind the wall is already worth nothing
#: and the day is still not terminal. Both are `valuation.pay_day()`'s: a crop
#: planted on `pay_day - 1` cannot mature and no animal placed then fires in
#: window, while `pay_day` itself is terminal and refused by a different rule.
#: `plan.HORIZON_DROP_ON` (5b0fcc4) moved that day from 28 to 29, which is what
#: took day 27 out of the dead zone -- written off the switch so both settings
#: stay pinned.
LATE = int(VAL.pay_day()) - 1


def _board(day=6, money=10_000, nquad=1, seeds=0):
    """NW owned and empty, every other quadrant LOCKED."""
    z = np.zeros(100, np.int32)
    kind = np.where(P.SERP_QUAD == 0, spec.KIND_EMPTY, spec.KIND_LOCKED).astype(np.int32)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=z - 1, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.full(spec.N_CROPS, seeds, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE.copy())


def _wheat(n):
    return np.array([n, 0, 0, 0, 0], np.int32)


def _land(view, macro):
    op, _, qty = P.build_day(np, view, macro)[3:6]
    return int(qty[op == O.MO_BUY_LAND].sum())


# --------------------------------------------------------------- the decision

def test_a_quadrant_that_pays_for_itself_is_bought_at_zero_bias():
    """25 tiles of wheat behind the wall, a purse that can stock them, and a
    gene that says nothing: the quadrant is bought on its coins alone."""
    macro = _macro(land_bias=np.int32(0), plant_target=_wheat(50))
    assert _land(_board(day=6), macro) == 1


def test_a_quadrant_late_in_the_season_is_refused_at_zero_bias():
    """`LATE`: `new_plant_units` is 0 for every crop and no animal's stream
    clears its price, so nothing behind the wall is worth a coin. No day
    constant is read -- the refusal is the valuation's. The day before still
    pays, so this is the valuation's own edge and not a blanket late-season
    refusal."""
    macro = _macro(land_bias=np.int32(0), plant_target=_wheat(50),
                   animal_want=geese(10))
    assert _land(_board(day=LATE), macro) == 0
    assert _land(_board(day=LATE - 1), macro) == 1


def test_a_saturated_positive_bias_buys_a_quadrant_the_valuation_refuses():
    """The gene can still insist: saturated positive it demands only that the
    quadrant not be worth *less* than its own price. `LATE` is the day the
    valuation refuses at zero bias, so the purchase here is the gene's."""
    macro = _macro(land_bias=np.int32(PRICE_0), plant_target=_wheat(50),
                   animal_want=geese(10))
    assert _land(_board(day=LATE), macro) == 1


def test_a_saturated_negative_bias_refuses_a_quadrant_zero_bias_buys():
    """One tile of headroom behind the wall is worth ~120 coins, which clears
    zero and does not clear a saturated-negative gene's 1,000-coin margin."""
    view = _board(day=6)
    yes = _macro(land_bias=np.int32(0), plant_target=_wheat(26))
    no = _macro(land_bias=np.int32(-PRICE_0), plant_target=_wheat(26))
    assert _land(view, yes) == 1
    assert _land(view, no) == 0


def test_the_gene_cannot_force_a_worthless_quadrant_past_affordability():
    """Saturated positive is still not a licence to overdraw."""
    macro = _macro(land_bias=np.int32(PRICE_0), plant_target=_wheat(50))
    assert _land(_board(day=6, money=500), macro) == 0
    # nor to buy a fifth quadrant
    assert _land(_board(day=6, nquad=4), macro) == 0


# ----------------------------------------------------------- the labour clamp

def test_land_value_is_zero_when_no_hand_can_reach_the_tiles():
    """A board whose owned tiles already exhaust the turn budget reaches none
    of the new ones, so the quadrant is worth nothing today."""
    assert int(P.land_reach(np, np.int32(1), np.int32(20))) == 0
    assert int(P.land_reach(np, np.int32(2), np.int32(50))) == 0


def test_one_unit_still_clears_a_day_six_quadrant():
    """Pass A prices the day on a zero hire bill, so it values land at one
    unit's labour. That under-counts -- it can only refuse, never over-buy --
    and it does not trap the day-6 purchase this work is aimed at."""
    assert int(P.land_reach(np, np.int32(1), np.int32(0))) >= 4
    # the engine's own starting purse, on the engine's own starting board
    macro = _macro(land_bias=np.int32(0), plant_target=_wheat(50))
    assert _land(_board(day=6, money=spec.STARTING_MONEY), macro) == 1


def test_a_bigger_crew_reaches_the_whole_quadrant():
    assert int(P.land_reach(np, np.int32(spec.MAX_UNITS), np.int32(0))) == P.LAND_TILES


# ------------------------------------------------------------------- the bias

def test_land_bias_decodes_to_zero_at_theta_zero():
    theta = np.zeros(PO.N_PARAMS, np.float32)
    obs = _obs()
    assert int(brain.decide(np, theta, obs).land_bias) == 0


def test_the_bias_is_bounded_by_the_quadrant_price():
    """`land_cost * tanh(z)`: saturated either way it is one quadrant price,
    never more, so the gene can neither force a worthless quadrant nor refuse
    an arbitrarily valuable one."""
    for z, nquad in ((20.0, 1), (-20.0, 1), (20.0, 3), (-20.0, 3)):
        theta = np.zeros(PO.N_PARAMS, np.float32)
        theta[PO.offset("gb2") + 1] = z
        bias = int(brain.decide(np, theta, _obs(nquad=nquad)).land_bias)
        price = int(spec.LAND_PRICES[nquad - 1])
        assert abs(bias) <= price and abs(bias) >= price - 1, (z, nquad, bias)
        assert (bias > 0) == (z > 0)


def _obs(nquad=1, money=10_000):
    z = np.zeros(100, np.int32)
    kind = np.where(spec.TILE_QUAD < nquad, spec.KIND_EMPTY, spec.KIND_LOCKED).astype(np.int32)
    return brain.PolicyObs(
        day=np.int32(6), money=np.int32(money), opp_money=np.int32(3000),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), nquad=np.int32(nquad),
        opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))


# --------------------------------------------------------- budget.marginal_gain

def _synthetic(value_behind=100, cost=10, want=3, value_ahead=1000):
    """One live list (the wheat-seed list) whose first `want` ranks are dear
    and whose later ranks are worth `value_behind` each."""
    v = np.zeros((BUD.N_LISTS, PJ.K), np.int32)
    c = np.ones((BUD.N_LISTS, PJ.K), np.int32)
    w = np.zeros(BUD.N_LISTS, np.int32)
    lst = BUD.L_SEED0
    v[lst, :want] = value_ahead
    v[lst, want:] = value_behind
    c[lst, :] = cost
    w[lst] = want
    return v, c, w


def test_marginal_gain_starts_at_the_want_and_stops_at_the_round_cap():
    v, c, w = _synthetic()
    g = BUD.marginal_gain(np, v, c, w, np.full(BUD.N_LISTS, 5, np.int32),
                          np.int32(5), np.int32(10_000), BUD.LAND_LISTS)
    assert int(g) == 5 * (100 - 10)
    g2 = BUD.marginal_gain(np, v, c, w, np.full(BUD.N_LISTS, 5, np.int32),
                           np.int32(2), np.int32(10_000), BUD.LAND_LISTS)
    assert int(g2) == 2 * (100 - 10)
    # `extra` bounds it too
    g3 = BUD.marginal_gain(np, v, c, w, np.full(BUD.N_LISTS, 1, np.int32),
                           np.int32(5), np.int32(10_000), BUD.LAND_LISTS)
    assert int(g3) == 1 * (100 - 10)


def test_marginal_gain_never_spends_past_the_purse():
    v, c, w = _synthetic()
    g = BUD.marginal_gain(np, v, c, w, np.full(BUD.N_LISTS, 5, np.int32),
                          np.int32(5), np.int32(25), BUD.LAND_LISTS)
    assert int(g) == 2 * (100 - 10)


def test_marginal_gain_ignores_lists_it_is_not_given():
    v, c, w = _synthetic()
    g = BUD.marginal_gain(np, v, c, w, np.full(BUD.N_LISTS, 5, np.int32),
                          np.int32(5), np.int32(10_000), (BUD.L_WHEAT,))
    assert int(g) == 0


def test_marginal_gain_takes_the_best_ratio_first():
    v, c, w = _synthetic()
    other = BUD.L_SEED0 + 1
    v[other, :] = 400
    c[other, :] = 10                      # ratio 40 against the first list's 10
    w[other] = 0
    extra = np.zeros(BUD.N_LISTS, np.int32)
    extra[BUD.L_SEED0] = 5
    extra[other] = 1
    g = BUD.marginal_gain(np, v, c, w, extra, np.int32(1), np.int32(10_000),
                          BUD.LAND_LISTS)
    assert int(g) == 400 - 10


# ----------------------------------------------------------------- both backends

def test_land_value_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _board(day=6)
    macro = _macro(land_bias=np.int32(0), plant_target=_wheat(50),
                   animal_want=geese(4))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
