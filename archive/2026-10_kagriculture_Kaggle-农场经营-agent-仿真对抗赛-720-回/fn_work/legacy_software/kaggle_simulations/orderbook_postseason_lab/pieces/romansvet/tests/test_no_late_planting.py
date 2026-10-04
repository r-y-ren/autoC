"""A crop that cannot be harvested and sold before the season ends is a pure
loss. Nothing is harvestable before day + CROP_FIRST_YIELD_DAY, and the last
day whose harvest still turns into coins is `valuation.pay_day()`. Rule:
day + first_yield_day <= pay_day.

That day is 28 while day 29 is dead -- the sale is decoded from the hour-0 shed,
so a day-29 harvest never reaches a lot -- and 29 with `plan.HORIZON_DROP_ON`
(5b0fcc4), where the day-29 DROP chain banks the harvest before the last market.
The tests below read the switch rather than the constant, so both settings are
pinned.

`_obs` deliberately cannot afford the next quadrant. M1 counts the tiles a
purchase would open as free before development is sized, so a farm with 1,000
coins in the bank would develop fifty tiles here rather than twenty-five and
every total below would move -- for reasons that have nothing to do with the
maturity mask these tests are about (`test_prospective_land.py` owns that).
Every weight but `gb2` is zero, so `head` is `gb2` exactly and the smaller
purse changes no other decode."""
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
from kagg3.core import brain
from kagg3.core import policy as PO
from kagg3.core import valuation as V


def _obs(day):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD == 0] = spec.KIND_EMPTY
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(100), opp_money=np.int32(10_000),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta_develop_all_crops():
    theta = np.zeros(PO.N_PARAMS, np.float32)
    gb2 = PO.offset("gb2")
    theta[gb2 + 5] = 10.0      # dev_frac -> 1
    theta[gb2 + 6] = -10.0     # animal_share -> 0
    return theta


def test_day_0_plants_every_crop():
    m = brain.decide(np, _theta_develop_all_crops(), _obs(0))
    assert np.all(m.plant_target > 0)


def test_day_20_skips_crops_that_first_yield_after_the_pay_day():
    m = brain.decide(np, _theta_develop_all_crops(), _obs(20))
    late = spec.CROP_FIRST_YIELD_DAY + 20 > V.pay_day()   # strawberry(10), melon(10)
    assert np.all(m.plant_target[late] == 0)
    assert np.all(m.plant_target[~late] > 0)
    # n_free=25, but sigmoid(10.0) is ~4.5e-5 short of 1 (true in float64 too
    # -- this isn't a float32 artifact), and that shortfall times 25 exceeds
    # QUANT_EPS (1e-4), so the pre-existing qfloor(dev_frac * 25) already
    # lands on 24, one below the naive 25 -- unrelated to this task's
    # masking. The invariant this asserts is that masking doesn't itself
    # lose any of that total: all 24 tiles land on the 3 crops that can
    # still mature.
    assert int(m.plant_target.sum()) == 24         # the tiles still get used


def test_the_last_maturing_day_plants_and_the_day_after_it_plants_nothing():
    # Wheat and carrot first yield on day + 2, so `pay_day - 2` is the last day
    # a seed is worth its coins and `pay_day - 1` is the first that is not.
    # 5b0fcc4 slid both by a day: the day that plants nothing is 28, not 27.
    H = V.pay_day()
    m = brain.decide(np, _theta_develop_all_crops(), _obs(H - 2))
    assert int(m.plant_target.sum()) == 24         # the two crops that still mature
    m = brain.decide(np, _theta_develop_all_crops(), _obs(H - 1))
    assert int(m.plant_target.sum()) == 0


def _theta_tiny_unmasked_mass():
    """Same as `_theta_develop_all_crops`, but also biases the shared
    product encoder so that the two crops which can still mature at day 26
    (wheat, carrot; first_yield_day=2) get a softmax weight around 1e-9
    relative to the three that cannot (tomato/strawberry/melon;
    first_yield_day 8/10/10) -- a tiny-but-nonzero total post-mask. This is
    the regime where flooring the renormalisation divisor at 1e-6 (instead
    of guarding only the exact-zero case) used to under-renormalise the
    surviving weights and starve `_largest_remainder` of `plant_total`.
    """
    theta = _theta_develop_all_crops()
    w1 = PO.offset("w1")
    b1 = PO.offset("b1")
    w2 = PO.offset("w2")
    # One hidden neuron (index 0) reads only prod_feat[10]
    # (= CROP_FIRST_YIELD_DAY / 12) and saturates the shared encoder's tanh
    # on either side of the wheat/tomato boundary; the grow-score column of
    # w2 then turns that saturation into a large score gap between crops
    # that can and cannot still mature.
    theta[w1 + 10 * 64 + 0] = -1000.0   # w1 row 10 (that feature), col 0
    theta[b1 + 0] = 400.0
    theta[w2 + 0 * 2 + 0] = -3.4        # w2 grow-score column (0 of 2), row 0
    return theta


def test_tiny_masked_mass_still_plants_the_full_total():
    # day 26: wheat/carrot (first_yield_day=2) can still mature (26+2<=28);
    # tomato/strawberry/melon (8/10/10) cannot.
    m = brain.decide(np, _theta_tiny_unmasked_mass(), _obs(26))
    late = spec.CROP_FIRST_YIELD_DAY + 26 > 28
    assert np.all(m.plant_target[late] == 0)
    assert np.all(m.plant_target[~late] > 0)
    assert int(m.plant_target.sum()) == 24     # full plant_total, not under-allocated
