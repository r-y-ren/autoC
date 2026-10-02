"""The engine pairs market orders by *list index*, and the list it sees is
compacted: `agent/render.py` drops every MO_NONE slot. So when seat 0 sells
[WHEAT, CARROT, TOMATO] and seat 1 sells [WHEAT, TOMATO], the engine resolves
seat 1's TOMATO in the same lockstep round as seat 0's CARROT, and seat 0's
TOMATO a round later against the inventory seat 1 already raised.

The sim used to pair by raw slot instead, coupling the two TOMATO sales into one
shared quote walk -- a few coins' difference, visible only on a day where the
two seats sell different product *sets*. Surfaced 2026-08-22 by the labour-
priority gene, which changed a season's trajectory enough to land on such a day.
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
import jax.numpy as jnp
from kaggle_environments.envs.kaggriculture import kaggriculture as REF

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.sim import rollout
from kagg3.sim.state import build_tables, initial_state


def _engine_revenue(orders, shed, inv):
    """Run the engine's `_process_market` on a synthetic state; money per seat."""
    market = {"inventory": {n: int(inv[i]) for i, n in enumerate(spec.PRODUCTS)},
              "prices": {n: 0 for n in spec.PRODUCTS}}
    farms = [{"money": 0.0}, {"money": 0.0}]
    privates = [{"shed": {n: int(shed[p][i]) for i, n in enumerate(spec.PRODUCTS)},
                 "seeds": {}} for p in range(2)]

    class _Obs(dict):
        __getattr__ = dict.__getitem__

    class _S:
        def __init__(self, p):
            self.observation = _Obs(market=market, farms=farms, private=privates[p])
            self.action = {"market": orders[p]}

    class _Env:
        configuration = {}

    REF._process_market([_S(0), _S(1)], _Env())
    return np.array([farms[0]["money"], farms[1]["money"]])


def test_sim_pairs_market_orders_the_way_the_engine_does():
    W, C, T = spec.I_WHEAT, spec.I_CARROT, spec.I_TOMATO
    shed = np.zeros((2, spec.N_ITEMS), np.int32)
    shed[0, [W, C, T]] = [9, 1, 3]
    shed[1, [W, T]] = [10, 3]
    inv = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)

    orders = [[["SELL", "WHEAT", 9], ["SELL", "CARROT", 1], ["SELL", "TOMATO", 3]],
              [["SELL", "WHEAT", 10], ["SELL", "TOMATO", 3]]]
    want = _engine_revenue(orders, shed, inv)

    # The planner's row: nine fixed product slots, MO_NONE where nothing sells.
    mop = np.full((2, spec.MAX_MARKET_ORDERS), O.MO_NONE, np.int32)
    ma = np.zeros((2, spec.MAX_MARKET_ORDERS), np.int32)
    mq = np.zeros((2, spec.MAX_MARKET_ORDERS), np.int32)
    for p in range(2):
        for i in range(spec.N_PRODUCTS):
            mop[p, i] = O.MO_SELL if shed[p, i] > 0 else O.MO_NONE
            ma[p, i] = i
            mq[p, i] = shed[p, i]

    tables = build_tables(jnp)
    st = initial_state(jnp)._replace(shed=jnp.asarray(shed), mkt_inv=jnp.asarray(inv),
                                     money=jnp.zeros(2, jnp.int32))
    rows = rollout.compact_orders(jnp.asarray(mop), jnp.asarray(ma), jnp.asarray(mq))
    out = rollout._market_turn(tables, st, *rows)
    assert np.asarray(out.money).tolist() == want.tolist()
