"""The sell allocator (PLANNER_V3_1 section 1.2): a unit is sold iff the best
adjusted lot marginal clears the reservation value; it goes to the lot whose
adjusted marginal -- next quote, minus timing pressure per lot of delay, minus
the externality on later lots -- is highest, ties to the earlier lot.
"""
from __future__ import annotations

import itertools
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
from kagg3.core import loop
from kagg3.core import ops as O
from kagg3.core import projector as PJ
from kagg3.core import sell as S

TABLE = spec.build_price_table()
I0 = np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)
NO_SHOPS = np.zeros(spec.N_SHOPS, np.int32)


def _shops(**counts):
    s = np.zeros(spec.N_SHOPS, np.int32)
    for name, n in counts.items():
        s[spec.SHOP_NAMES.index(name)] = n
    return s


def _only(product, n):
    a = np.zeros(spec.N_PRODUCTS, np.int32)
    a[product] = n
    return a


def _revenue(product, split, shops):
    """Projected coins of selling `split` = (n1, n2, n3) units of `product`,
    own earlier lots advancing the later inventories."""
    inv = np.stack([PJ.projected_inv(np, I0, shops, t) for t in O.SELL_TURNS])[:, product]
    total, sold_before = 0, 0
    for k, n in enumerate(split):
        start = int(inv[k]) + sold_before
        total += sum(int(TABLE[product, start + j - spec.PRICE_TABLE_LO]) for j in range(n))
        sold_before += n
    return total


def test_zero_pressure_zero_shops_is_indifferent_and_takes_the_earliest_lot():
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20),
                      np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
    assert lots[:, spec.I_WOOL].tolist() == [20, 0, 0]
    assert int(lots.sum()) == 20


def test_reservation_value_gates_the_quantity():
    hold = np.full(spec.N_PRODUCTS, 10_000, np.int32)
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20), hold, np.zeros(spec.N_PRODUCTS, np.int32))
    assert int(lots.sum()) == 0
    hold[spec.I_WOOL] = 190          # wool starts at 200 and falls; some units clear it, not all
    lots = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 20), hold, np.zeros(spec.N_PRODUCTS, np.int32))
    n = int(lots[:, spec.I_WOOL].sum())
    assert 0 < n < 20
    quotes = PJ.sell_quotes(np, TABLE, PJ.projected_inv(np, I0, NO_SHOPS, O.SELL_TURNS[0]))[spec.I_WOOL]
    assert n == int((quotes[:20] >= 190).sum())


def test_town_consumption_moves_the_sale_later():
    # a yarn store drains wool between lots, so later lots quote higher and win
    shops = _shops(YARN_STORE=1)
    lots = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 20),
                      np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
    assert int(lots[2, spec.I_WOOL]) > int(lots[0, spec.I_WOOL])
    assert int(lots[:, spec.I_WOOL].sum()) == 20


def test_pressure_pulls_the_sale_earlier():
    shops = _shops(YARN_STORE=1)
    press = _only(spec.I_WOOL, 1000)
    lots = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 20), np.zeros(spec.N_PRODUCTS, np.int32), press)
    assert lots[:, spec.I_WOOL].tolist() == [20, 0, 0]


def test_greedy_is_close_to_the_exhaustive_split():
    # bounded exhaustive check (the spec's verification-mode fallback)
    shops = _shops(YARN_STORE=2, BAKERY=1)
    for product, n in ((spec.I_WOOL, 12), (spec.I_MILK, 10), (spec.I_WHEAT, 15), (spec.I_FERT, 8)):
        lots = S.allocate(np, TABLE, I0, shops, _only(product, n),
                          np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
        got = _revenue(product, tuple(int(x) for x in lots[:, product]), shops)
        best = max(_revenue(product, s, shops) for s in itertools.product(range(n + 1), repeat=3)
                   if sum(s) == n)
        assert got >= 0.97 * best, (product, lots[:, product].tolist(), got, best)


def test_a_continued_allocation_equals_one_run_over_the_whole_quantity():
    # `allocate` can be continued: `lots0` carries the units already placed and
    # `avail` grows by the further quantity, so every extra unit is charged the
    # curve the ones before it left. That is what a forced-overflow sale wants
    # [0.9] and what the day scan cannot currently afford (see the test below),
    # so the property is pinned here rather than through `build_day`.
    #
    # A one-yarn-store town on wool with `press` = 8 genuinely splits the sale
    # (the town's four units of drain between lots buy about nine coins of
    # quote at this point on the curve, either side of the pressure), so the
    # board is not a degenerate all-in-one-lot answer.
    shops = _shops(YARN_STORE=1)
    hold = np.full(spec.N_PRODUCTS, S.LIQUIDATE, np.int32)
    press = _only(spec.I_WOOL, 8)
    whole = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 40), hold, press)
    assert whole[:, spec.I_WOOL].tolist() == [2, 4, 34]        # all three lots carry units
    first = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 25), hold, press)
    cont = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 40), hold, press,
                      lots0=first, rounds=spec.SHED_CAPACITY)
    assert cont.tolist() == whole.tolist()
    assert int(cont[:, spec.I_WOOL].sum()) == 40


def test_unit_by_unit_placement_beats_a_bulk_placement_at_one_argmax():
    # What the sale block's bulk placement gives up, recorded as a number [0.9].
    # `plan.py` appends the whole deficit at one pre-forced argmax because
    # continuing the greedy costs a second 100-round allocator pass inside the
    # day scan (-5.2% episode throughput, over its benchmark gate); this is the
    # coin value of that decision, so a cheaper formulation has something to
    # beat. On a one-yarn-store town with
    # `press` = 3, ten wool start out worth [212, 215, 215] across the lots, so
    # a bulk placement would put all ten in lot 2 (the earliest maximum) and
    # walk that one curve down. The unit-by-unit greedy moves to lot 3 after
    # one unit.
    shops = _shops(YARN_STORE=1)
    press = _only(spec.I_WOOL, 3)
    hold = np.full(spec.N_PRODUCTS, S.LIQUIDATE, np.int32)
    inv_lots = S.lot_inventories(np, I0, shops)
    adj = S.adjusted_marginals(np, TABLE, inv_lots, np.zeros((S.N_LOTS, spec.N_PRODUCTS), np.int32), press)
    assert adj[:, spec.I_WOOL].tolist() == [212, 215, 215]
    assert int(adj[:, spec.I_WOOL].argmax()) == 1                 # where bulk would have put all ten

    lots = S.allocate(np, TABLE, I0, shops, _only(spec.I_WOOL, 10), hold, press,
                      rounds=spec.SHED_CAPACITY)
    assert lots[:, spec.I_WOOL].tolist() == [0, 1, 9]
    assert _revenue(spec.I_WOOL, (0, 1, 9), shops) == 2163
    assert _revenue(spec.I_WOOL, (0, 10, 0), shops) == 2091       # the bulk placement, 72 coins worse


def test_liquidation_sells_even_when_every_adjusted_marginal_is_below_it():
    """`hold = LIQUIDATE` is a *mode*, not a value comparison [LAW, 0.4].

    An adjusted marginal is a net number -- next quote, minus `press` per lot
    of delay, minus the externality on the later lots -- so it can fall below
    `LIQUIDATE = -COIN_CAP` on its own, and a gate written only as
    `best_adj >= hold` would then keep units the law says must go.

    The board is synthetic and says so: with lot inventories from
    `lot_inventories` the projection bounds the shortfall at roughly twice the
    price drop over four shop ticks (a few thousand coins at the table's
    steepest point), far above the sentinel. It is reachable only through the
    `inv_lots` argument, which is part of `allocate`'s interface, so it is
    pinned here rather than left to the table's numbers.

    The arithmetic, tomato: lots 1 and 2 sit at I0 (quote 60), lot 3 at the
    table's low end (quote 1,053,252) already holding 15,000 units, whose
    next quote is back at 60. Lot 3's own drop is 60 - 1,053,252 =
    -1,053,192, which lot 1 carries as its externality:
    adj = [60 - 1,053,192, 60 - 2**20 - 1,053,192, 60 - 2 * 2**20] =
    [-1,053,132, -2,101,708, -2,097,092] -- every one of them below
    LIQUIDATE = -1,048,576.
    """
    p = spec.I_TOMATO
    inv_lots = np.stack([np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32)] * S.N_LOTS)
    inv_lots[2, p] = spec.PRICE_TABLE_LO
    lots0 = np.zeros((S.N_LOTS, spec.N_PRODUCTS), np.int32)
    lots0[2, p] = 15_000
    press = _only(p, spec.COIN_CAP)
    hold = np.full(spec.N_PRODUCTS, S.LIQUIDATE, np.int32)

    adj = S.adjusted_marginals(np, TABLE, inv_lots, lots0, press)
    assert adj[:, p].tolist() == [-1_053_132, -2_101_708, -2_097_092]
    assert int(adj[:, p].max()) < S.LIQUIDATE          # the gate has to be the mode, not the value

    lots = S.allocate(np, TABLE, None, None, _only(p, 15_007), hold, press,
                      lots0=lots0, inv_lots=inv_lots)
    assert int(lots[:, p].sum()) == 15_007             # all seven further units go


def test_every_return_is_int32_on_both_backends():
    # np.cumsum/np.sum widen an int32 input to int64 and np.argmax returns intp,
    # while jnp does neither -- the planner is int32 everywhere, so pin it.
    import jax.numpy as jnp
    shops = _shops(YARN_STORE=1)
    lots = np.zeros((S.N_LOTS, spec.N_PRODUCTS), np.int32)
    press = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 5
    avail = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 3
    hold = np.full(spec.N_PRODUCTS, 30, np.int32)
    args = (TABLE, I0, shops, lots, press, avail, hold)
    for xp, (tab, inv0, sh, lt, pr, av, hd) in ((np, args), (jnp, tuple(jnp.asarray(a) for a in args))):
        inv = S.lot_inventories(xp, inv0, sh)
        assert inv.dtype == xp.int32
        assert S.adjusted_marginals(xp, tab, inv, lt, pr).dtype == xp.int32
        assert S.allocate(xp, tab, inv0, sh, av, hd, pr).dtype == xp.int32
        assert S.allocate(xp, tab, inv0, sh, av, hd, pr, lots0=lt, inv_lots=inv,
                          rounds=4).dtype == xp.int32


def test_zero_pressure_zero_shops_takes_the_earliest_lot_on_jax_too():
    # The tie rule is a LAW of the planner, not a numpy accident: with no town
    # and no pressure every lot quotes alike and `argmax` must take the
    # earliest on both backends (jnp's argmax has the same first-maximum rule,
    # but nothing pinned it here).
    import jax.numpy as jnp
    zero = np.zeros(spec.N_PRODUCTS, np.int32)
    lots = S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(NO_SHOPS),
                      jnp.asarray(_only(spec.I_WOOL, 20)), jnp.asarray(zero), jnp.asarray(zero))
    assert np.asarray(lots)[:, spec.I_WOOL].tolist() == [20, 0, 0]


def test_allocator_agrees_across_backends_with_and_without_the_traced_loop():
    import jax.numpy as jnp
    shops = _shops(YARN_STORE=1, PET_CAFE=1)
    avail = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 3
    hold = np.full(spec.N_PRODUCTS, 30, np.int32)
    press = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 5
    a = S.allocate(np, TABLE, I0, shops, avail, hold, press)
    b = S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(shops),
                   jnp.asarray(avail), jnp.asarray(hold), jnp.asarray(press))
    assert a.tolist() == np.asarray(b).tolist()
    # Importing the simulator installs `lax.fori_loop` process-wide, so the
    # previous implementation is saved and put back: leaking it would make
    # every later test in the pytest process run a different loop than the one
    # it thinks it is testing.
    saved = loop._impl
    try:
        from kagg3.sim import rollout  # noqa: F401  -- installs lax.fori_loop
        assert loop._impl is not None
        c = S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(shops),
                       jnp.asarray(avail), jnp.asarray(hold), jnp.asarray(press))
        assert a.tolist() == np.asarray(c).tolist()
        d = S.allocate(np, TABLE, I0, shops, avail, hold, press)
        assert a.tolist() == d.tolist()
    finally:
        loop.install(saved)


def test_numpy_never_reaches_the_installed_traced_loop():
    # The submission runs numpy in the same process the simulator may have
    # loaded, and `core` must stay JAX-free there [global constraint]. Asserted
    # by mechanism rather than by the answer: a counting implementation is
    # installed, and numpy must not call it even once.
    calls = []

    def counting(n_iter, body, carry):
        calls.append(n_iter)
        for _ in range(n_iter):
            carry = body(carry)
        return carry

    saved = loop._impl
    try:
        loop.install(counting)
        out = S.allocate(np, TABLE, I0, NO_SHOPS, _only(spec.I_WOOL, 5),
                         np.zeros(spec.N_PRODUCTS, np.int32), np.zeros(spec.N_PRODUCTS, np.int32))
        assert calls == []
        assert out[:, spec.I_WOOL].tolist() == [5, 0, 0]
        # ... and the same implementation *is* reached from a non-numpy backend
        import jax.numpy as jnp
        S.allocate(jnp, jnp.asarray(TABLE), jnp.asarray(I0), jnp.asarray(NO_SHOPS),
                   jnp.asarray(_only(spec.I_WOOL, 5)), jnp.asarray(np.zeros(spec.N_PRODUCTS, np.int32)),
                   jnp.asarray(np.zeros(spec.N_PRODUCTS, np.int32)))
        assert calls == [PJ.K - 1]
    finally:
        loop.install(saved)
