"""Buying a quadrant only pays if it gets planted. `dev_frac` was one number for
every day, so a freshly unlocked quadrant (25 free tiles) was developed at the
same trickle as a full farm's two free tiles. aux[2] (the g5/gb5 block) makes
the share of free tiles raise it; zero for pre-g5 thetas.

The free-tile count these read is M1's, so it depends on whether a quadrant is
in reach: `brain.decide` counts the tiles a purchase would open as free before
it sizes development. `_obs`' `money` is what selects that -- a farm that
cannot afford the next quadrant sees only what it owns -- and every weight but
`gb2`/`gb5` is zero here, so `head` is `gb2` exactly and no other feature can
move these numbers."""
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


#: Enough to buy the next quadrant (nquad 2 -> 2,000), and not enough.
RICH, POOR = 10_000, 100


def _obs(n_free_tiles, money=POOR):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < 2] = spec.KIND_PLANT          # 50 tiles owned, all planted
    free_ids = np.flatnonzero(spec.TILE_QUAD < 2)[:n_free_tiles]
    kind[free_ids] = spec.KIND_EMPTY
    # Crop 2 is CROP_ONGOING (spec.CROP_ONGOING[2] == 1), so the "already
    # planted" filler tiles never register as `n_free_slots`'s harvest_one
    # (a one-time-harvest crop like crop 0 would, at day 12, count every
    # already-planted filler tile as free too and swamp the free_ids signal
    # this test is built around).
    occ = np.where(kind == spec.KIND_PLANT, 2, -1).astype(np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    return brain.PolicyObs(
        day=np.int32(12), money=np.int32(money), opp_money=np.int32(10_000),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(2), opp_nquad=np.int32(2),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta(h5, a2):
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 5] = h5
    theta[PO.offset("gb5") + 2] = a2
    return theta


def _developed(theta, obs):
    m = brain.decide(np, theta, obs)
    return int(m.plant_target.sum() + m.animal_want.sum())


def test_legacy_dev_frac_is_unchanged_when_aux_2_is_zero():
    # sigmoid(0) = 0.5 of free tiles, whatever their number
    assert _developed(_theta(0.0, 0.0), _obs(2)) == 1
    assert _developed(_theta(0.0, 0.0), _obs(24)) == 12


def test_positive_aux_2_develops_more_of_a_big_free_block():
    # 24 free tiles: 0 + 3 * 24/25 = 2.88 -> sigmoid ~0.95 -> 22 of 24
    assert _developed(_theta(0.0, 3.0), _obs(24)) >= 22


def test_positive_aux_2_barely_changes_a_small_free_block():
    # 2 free tiles: 0 + 3 * 2/25 = 0.24 -> sigmoid 0.56 -> floor(1.12) = 1
    assert _developed(_theta(0.0, 3.0), _obs(2)) == 1


def test_a_quadrant_in_reach_is_counted_before_development_is_sized():
    """M1, from the head's side. The same board with the price of the next
    quadrant in the bank has 25 more free tiles, so a neutral `dev_frac`
    develops 13 of 27 instead of 1 of 2 -- which is the whole reason a bought
    quadrant can be planted the day it is bought."""
    assert _developed(_theta(0.0, 0.0), _obs(2, money=RICH)) == 13
    assert _developed(_theta(0.0, 0.0), _obs(24, money=RICH)) == 24
    # ... and the urgency term reads the enlarged block too
    assert _developed(_theta(0.0, 3.0), _obs(2, money=RICH)) >= 24
