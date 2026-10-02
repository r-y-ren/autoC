"""The shipped theta's land logit turns negative the moment a second quadrant
exists and stays there with 50k in the bank. aux[1] (the g5/gb5 block) adds a
cash-relative term, clipped to [-1, 4]: zero for every pre-g5 theta, so old
checkpoints decode unchanged.

The logit now decodes to a signed *coin bias* on the planner's own valuation
(`land_cost * tanh(z)`, `test_land_value.py`) rather than to a 0/1 decision, so
these tests read its sign: positive is "the gene wants a quadrant", zero or
negative is "it does not". The threshold arithmetic they pin is unchanged --
`tanh` is strictly increasing and zero at zero."""
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


def _obs(money, nquad):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < nquad] = spec.KIND_EMPTY
    shed = np.zeros(spec.N_ITEMS, np.int32)
    return brain.PolicyObs(
        day=np.int32(12), money=np.int32(money), opp_money=np.int32(money),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta(h1, a1):
    """Zero weights, so head == gb2 and aux == gb5 exactly; set both directly."""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 1] = h1
    theta[PO.offset("gb5") + 1] = a1
    return theta


def test_legacy_threshold_is_unchanged_when_aux_1_is_zero():
    rich, poor = _obs(50_000, 2), _obs(100, 2)
    assert int(brain.decide(np, _theta(-0.5, 0.0), rich).land_bias) < 0
    assert int(brain.decide(np, _theta(+0.5, 0.0), poor).land_bias) > 0


def test_positive_aux_1_buys_when_cash_dwarfs_the_price():
    # nquad 2 -> next quadrant costs 2000; 50k/2000 - 1 = 24, clipped to 4:
    # -0.5 + 0.5 * 4 = 1.5 > 0
    assert int(brain.decide(np, _theta(-0.5, 0.5), _obs(50_000, 2)).land_bias) > 0


def test_positive_aux_1_does_not_buy_when_cash_is_below_the_price():
    # 1000 / 2000 - 1 = -0.5 -> -0.5 + 0.5 * -0.5 = -0.75 < 0
    assert int(brain.decide(np, _theta(-0.5, 0.5), _obs(1_000, 2)).land_bias) < 0


def test_ratio_is_clipped_so_cash_cannot_dominate():
    # 10,000 / 2000 - 1 = 4 and 50,000 / 2000 - 1 = 24 must decode alike
    a = brain.decide(np, _theta(-2.1, 0.5), _obs(10_000, 2)).land_bias
    b = brain.decide(np, _theta(-2.1, 0.5), _obs(50_000, 2)).land_bias
    assert int(a) == int(b) < 0           # -2.1 + 0.5 * 4 = -0.1


def test_both_backends_agree():
    import jax.numpy as jnp
    obs = _obs(50_000, 2)
    th = _theta(-0.5, 0.5)
    a = brain.decide(np, th, obs).land_bias
    b = brain.decide(jnp, jnp.asarray(th), brain.PolicyObs(*[None if x is None else jnp.asarray(x) for x in obs])).land_bias
    assert int(a) == int(b)
