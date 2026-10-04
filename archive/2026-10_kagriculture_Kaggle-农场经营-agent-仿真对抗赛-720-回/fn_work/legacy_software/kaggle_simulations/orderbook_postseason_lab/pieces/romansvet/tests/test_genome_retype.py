"""PLANNER_V3_1 section 2: learned outputs are values in coins, not decisions.
`hold` is a reservation value (0.8 x base at z = 0, so the initial policy
sells -- asserted against the projector, not assumed), `press` an opponent
timing pressure (0 at z = 0), `grow_mult` a value multiplier (x1 at z = 0,
capped at x4, fixed-point). The four decisions the planner stopped reading in
Phase 1 no longer exist in the Macro.
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
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import projector as PJ

TABLE = spec.build_price_table()


def _obs_sell():
    """A small fresh-market observation: day 2, one quadrant, 5 of everything."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD == 0] = spec.KIND_EMPTY
    shed = np.zeros(spec.N_ITEMS, np.int32); shed[:spec.N_PRODUCTS] = 5
    return brain.PolicyObs(
        day=np.int32(2), money=np.int32(800), opp_money=np.int32(800),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.full(spec.N_PRODUCTS, 25, np.int32),
        shops=np.zeros(8, np.int32))


def _theta_with(sell=0.0, gate=0.0, grow=0.0):
    th = np.zeros(PO.N_PARAMS, np.float32)
    th[PO.offset("b2") + 1] = sell            # sell-score bias, every product
    th[PO.offset("b2") + 0] = grow            # grow-score bias
    th[PO.offset("b3")] = gate                # gate bias
    return th


def test_zero_theta_decodes_to_the_spec_init_posture():
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    expect_hold = np.floor(0.8 * brain._BASE + brain.QUANT_EPS).astype(np.int32)
    assert m.hold.tolist() == expect_hold.tolist()
    assert m.press.tolist() == [0] * spec.N_PRODUCTS
    assert m.grow_mult.tolist() == [brain.GROW_ONE] * spec.N_PRODUCTS


def test_the_initial_policy_sells():
    # day-1 projected marginals clear 0.8 x base: the first unit of every
    # product, sold in the last lot of a fresh market, fetches at least `hold`
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    inv = PJ.projected_inv(np, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
                           np.zeros(spec.N_SHOPS, np.int32), O.SELL_TURNS[-1])
    first_unit = PJ.sell_quotes(np, TABLE, inv)[:, 0]
    assert np.all(first_unit >= m.hold)


def test_transforms_are_monotone_and_bounded():
    lo = brain.decide(np, _theta_with(sell=-6.0, gate=-6.0, grow=-6.0), _obs_sell())
    mid = brain.decide(np, _theta_with(), _obs_sell())
    hi = brain.decide(np, _theta_with(sell=6.0, gate=6.0, grow=6.0), _obs_sell())
    assert np.all(lo.hold < mid.hold) and np.all(mid.hold < hi.hold) and np.all(lo.hold >= 0)
    assert np.all(lo.press == 0) and np.all(mid.press == 0) and np.all(hi.press > 0)
    assert np.all(hi.press <= brain._BASE)
    assert np.all(lo.grow_mult < mid.grow_mult) and np.all(hi.grow_mult == int(brain.GROW_MAX * brain.GROW_ONE))


def test_dead_decisions_are_gone_from_the_macro():
    for name in ("n_fertilize", "feed_daily", "care_on", "fert_buy"):
        assert name not in P.Macro._fields


#: Every layout this repo has shipped a theta under, each a *prefix* of the
#: current one -- which is the whole reason new blocks are only ever appended
#: (see `policy.SHAPES`). 4,518 is the residual-drain layout and 4,386 the one
#: before it; 4,617 is the one every champion on this machine is written under
#: (`artifacts/theta.npy`, `artifacts/theta_flow9_g15975_champion.npy`), i.e.
#: the layout the crew/herd-mix block appends to.
#: 4,749 -- the layout the hire-bias day buckets append to -- is deliberately
#: absent: zero-padding that one is *not* inert, because `policy.unpack` copies
#: its season-constant `hire_bias` into the four buckets instead of zeroing
#: them. `tests/test_crew_and_herd_mix.py` pins that pad, which is the same
#: claim this list makes for every layout whose tail really is a no-op.
#: 4,980 is the layout the production-forecast block (`fh`/`fs`) appends to,
#: i.e. what every flow13x checkpoint is written under; 5,508 is what `gp`
#: appends to, 6,372 what the forward-admit gene (`g11`/`gb11`) does and 6,405
#: what the forward-value block (`fv`) does.
SHIPPED_LAYOUTS = (PO.N_PARAMS_LEGACY, 4287, 4386, 4518, 4584, 4617,
                   4848, 4980, 5508, 6372, 6405)


def test_every_block_is_appended_and_zero_padding_is_inert():
    # The tail in order, so a block inserted anywhere but the end fails here
    # rather than silently invalidating every checkpoint.
    # Anchored at `dh` rather than at the tail: the tail is where the next
    # block lands, so a negative slice would fail here every time one is
    # appended -- which is the append this test is meant to allow.
    names = [n for n, _ in PO.SHAPES]
    assert names[names.index("dh"):] == ["dh", "ds", "g6", "gb6", "g7",
                                         "gb7", "g8", "gb8", "g9", "gb9",
                                         "g10", "gb10", "fh", "fs", "gp",
                                         "g11", "gb11", "fv"]
    for n in SHIPPED_LAYOUTS:
        short = np.ones(n, np.float32)
        padded = np.concatenate([short, np.zeros(PO.N_PARAMS - n, np.float32)])
        a = brain.decide(np, short, _obs_sell())
        b = brain.decide(np, padded, _obs_sell())
        for x, y in zip(a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y))


def test_every_macro_field_is_int32_on_both_backends():
    # The planner is int32 end to end (global constraint), and every `Macro`
    # field feeds an index, a ratio or a comparison inside `build_day`. numpy
    # widens an int32 reduction to int64 and `np.floor` returns float64, so
    # nothing here is inherited -- and until now nothing asserted it either.
    import jax
    import jax.numpy as jnp
    obs = _obs_sell()
    th = _theta_with(sell=1.5, gate=0.7, grow=-0.4)
    for xp, t, o in ((np, th, obs),
                     (jnp, jnp.asarray(th), jax.tree_util.tree_map(jnp.asarray, obs))):
        m = brain.decide(xp, t, o)
        for name, v in zip(P.Macro._fields, m):
            assert np.asarray(v).dtype == np.int32, (xp.__name__, name, np.asarray(v).dtype)


def test_every_prefix_field_is_int32_or_bool_on_both_backends():
    # `Prefix` is what the hire enumeration and the admit/route stages index
    # and stack; `n_ops` and the three `chain_*` arrays came out int64 on numpy
    # until they were pinned at their source in `_derive`.
    import jax
    import jax.numpy as jnp
    from test_budget_order import _macro, _view
    view, macro = _view(3000), _macro()
    for xp, v, m in ((np, view, macro),
                     (jnp, jax.tree_util.tree_map(jnp.asarray, view),
                      jax.tree_util.tree_map(jnp.asarray, macro))):
        zero = xp.asarray(0, xp.int32)
        d = P._derive(xp, v, m, xp.asarray(TABLE), zero, False, zero)
        for name, a in zip(P.Prefix._fields, d):
            dt = np.asarray(a).dtype
            assert dt in (np.int32, np.bool_), (xp.__name__, name, dt)


def test_decode_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    th = _theta_with(sell=1.5, gate=0.7, grow=-0.4)
    obs = _obs_sell()
    a = brain.decide(np, th, obs)
    b = brain.decide(jnp, jnp.asarray(th), jax.tree_util.tree_map(jnp.asarray, obs))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
