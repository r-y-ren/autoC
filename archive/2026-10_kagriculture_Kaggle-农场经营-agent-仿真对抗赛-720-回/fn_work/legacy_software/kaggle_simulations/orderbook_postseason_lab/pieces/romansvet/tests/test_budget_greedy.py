"""The marginal-unit budget (PLANNER_V3_1 section 1.3): candidates from ten
monotone lists granted by value per coin down the purse, lumpy leftovers
topped up, wants and zero values respected.
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
from kagg3.core import budget as B
from kagg3.core import plan as P  # `V.pay_day()` below reads its horizon switch
from kagg3.core import projector as PJ
from kagg3.core import valuation as V

K = PJ.K


def test_single_list_buys_the_affordable_prefix():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[0, :4], costs[0, :4], wants[0] = [100, 90, 80, 70], [10, 11, 12, 13], 4
    assert B.grant(np, values, costs, wants, np.int32(33)).tolist() == [3, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert B.grant(np, values, costs, wants, np.int32(1000)).tolist() == [4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert B.grant(np, values, costs, wants, np.int32(0)).tolist() == [0] * B.N_LISTS


def test_two_lists_interleave_by_value_per_coin():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[0, :3], costs[0, :3], wants[0] = [50, 40, 30], [10, 10, 10], 3      # ratios 5, 4, 3
    values[7, :3], costs[7, :3], wants[7] = [90, 45, 20], [20, 20, 20], 3      # ratios 4.5, 2.25, 1
    # purse 50: 5 (10) -> 4.5 (20) -> 4 (10) -> 3 (10) = 50
    assert B.grant(np, values, costs, wants, np.int32(50)).tolist() == [3, 0, 0, 0, 0, 0, 0, 1, 0, 0]


def test_a_lumpy_item_that_does_not_fit_is_skipped_for_cheaper_ones():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[7, :1], costs[7, :1], wants[7] = [1000], [300], 1                  # ratio 3.3, unaffordable
    values[2, :5], costs[2, :5], wants[2] = [20, 20, 20, 20, 20], [10] * 5, 5  # ratio 2
    assert B.grant(np, values, costs, wants, np.int32(45)).tolist() == [0, 0, 4, 0, 0, 0, 0, 0, 0, 0]


def test_stream_rev_prices_every_candidate_not_just_a_sheds_worth():
    inv0 = np.int32(spec.MARKET_I0)
    k = np.arange(K, dtype=np.int32)
    rev = P._stream_rev(np, spec.build_price_table()[spec.I_MELON], inv0, np.int32(6), k)
    assert rev.shape == (K,)
    assert int(rev[0]) == 6 * 250
    assert np.all(rev[1:] <= rev[:-1]) and int(rev[K - 1]) > 0     # declining, never clipped to zero
    assert int(rev[30]) == sum(int(spec.build_price_table()[spec.I_MELON, inv0 + 180 + m - spec.PRICE_TABLE_LO])
                               for m in range(6))


def test_zero_value_candidates_are_never_bought():
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[2, :3], costs[2, :3], wants[2] = [0, 0, 0], [10, 10, 10], 3
    assert B.grant(np, values, costs, wants, np.int32(1000)).tolist() == [0] * B.N_LISTS


def test_total_cost_never_exceeds_the_purse():
    rng = np.random.default_rng(0)
    for _ in range(50):
        values = np.zeros((B.N_LISTS, K), np.int32)
        costs = np.ones((B.N_LISTS, K), np.int32)
        wants = rng.integers(0, 20, B.N_LISTS).astype(np.int32)
        for i in range(B.N_LISTS):
            values[i] = np.sort(rng.integers(0, 500, K))[::-1]
            costs[i] = np.sort(rng.integers(1, 60, K))
        purse = np.int32(rng.integers(0, 2000))
        n = B.grant(np, values, costs, wants, purse)
        assert np.all(n <= wants) and np.all(n >= 0)
        spent = sum(int(costs[i, :n[i]].sum()) for i in range(B.N_LISTS))
        assert spent <= int(purse)


def test_new_plant_units_at_the_spec_numbers():
    """The horizon a seed is priced against is `valuation.pay_day()`, not
    `O.LAST_SHED_DAY`: `plan.HORIZON_DROP_ON` (5b0fcc4) moved it from 28 to 29,
    so every late planting keeps one more in-window watering and the last
    plantable day slides with it. Written off the switch so both settings are
    pinned -- and the module imports `plan` for the binding `pay_day` reads."""
    I = np.int32
    H = V.pay_day()
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(0))) == 4        # born 1, watered ages 2, 3, 4
    assert int(V.new_plant_units(np, I(spec.I_MELON), I(0))) == 6        # saturates
    assert int(V.new_plant_units(np, I(spec.I_TOMATO), I(0))) == 4       # four fires
    # A late wheat harvests at `H - t_day` clamped into its window: one unit at
    # birth and one per in-window watering, four where the yield saturates.
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(25))) == min(4, H - 25)
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(H - 2))) == 2     # first yield day 2: the last one in
    assert int(V.new_plant_units(np, I(spec.I_WHEAT), I(H - 1))) == 0     # cannot mature
    assert int(V.new_plant_units(np, I(spec.I_TOMATO), I(19))) == H - 26  # fires 27, 28 and, at H = 29, 29


def test_room_caps_the_shed_lists_and_leaves_the_purse_to_the_others():
    """Shed room is a second budget, and it binds inside the greedy.

    Wheat, fertilizer and animals all land in the shed and share one room, so
    three lists each wanting three units chase two slots. Capping each list by
    the room and clipping afterwards would let the greedy pay for all nine and
    throw seven away; the room has to be carried through the threshold and the
    top-ups, so the coins it refuses stay in the purse for the seed list.
    """
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[B.L_WHEAT, :3], costs[B.L_WHEAT, :3], wants[B.L_WHEAT] = [100] * 3, [10] * 3, 3    # ratio 10
    values[B.L_FERT, :3], costs[B.L_FERT, :3], wants[B.L_FERT] = [90] * 3, [10] * 3, 3        # ratio 9
    values[B.L_ANIMAL0, :3], costs[B.L_ANIMAL0, :3], wants[B.L_ANIMAL0] = [80] * 3, [10] * 3, 3  # ratio 8
    values[B.L_SEED0, :5], costs[B.L_SEED0, :5], wants[B.L_SEED0] = [20] * 5, [10] * 5, 5     # ratio 2

    # two shed slots go to the two best-ratio shed units (wheat), and the 80
    # coins the room refused buy all five seeds instead of being stranded
    n = B.grant(np, values, costs, wants, np.int32(100), np.int32(2))
    assert n.tolist() == [2, 0, 5, 0, 0, 0, 0, 0, 0, 0]
    assert sum(int(n[i]) for i in B.SHED_LISTS) <= 2

    # room 0 shuts the three lists out entirely; the seeds still get served
    assert B.grant(np, values, costs, wants, np.int32(100), np.int32(0)).tolist() == \
        [0, 0, 5, 0, 0, 0, 0, 0, 0, 0]
    # and without a room the same purse goes to the three best ratios
    assert B.grant(np, values, costs, wants, np.int32(100)).tolist() == [3, 3, 1, 0, 0, 0, 0, 3, 0, 0]


def test_a_binding_room_does_not_push_the_other_lists_into_the_top_ups():
    """One global tau cannot say "few shed units, many seeds".

    The three shed lists have the best ratios (10 per coin) but only two shed
    slots, so the room-constrained threshold has to lift tau above them -- and
    the same tau then also shuts out the five seed lists at 2 per coin, whose
    units are not shed items at all. With one pass the whole seed grant fell to
    the top-ups, and those add at most one item a round: K = 101 rounds for
    505 wanted seeds, so 101 items total (99 seeds after the two wheat) instead
    of 505.

    The second threshold pass fixes it exactly: the shed lists stay frozen at
    the first pass's answer, the seeds are thresholded again on their own tau
    against the coins the shed lists did not spend (all 6,000 -- the first pass
    granted nothing), and 505 seeds at 10 coins = 5,050 fit. The 950 left then
    top up the two shed units the room allows.
    """
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    for lst in B.SHED_LISTS:
        values[lst, :3], costs[lst, :3], wants[lst] = [100] * 3, [10] * 3, 3        # ratio 10
    for c in range(spec.N_CROPS):
        lst = B.L_SEED0 + c
        values[lst, :], costs[lst, :], wants[lst] = 20, 10, K                       # ratio 2

    n = B.grant(np, values, costs, wants, np.int32(6000), np.int32(2))
    assert n[B.L_SEED0:B.L_SEED0 + spec.N_CROPS].tolist() == [K] * spec.N_CROPS
    assert sum(int(n[i]) for i in B.SHED_LISTS) == 2
    assert int(n[B.L_WHEAT]) == 2                       # the best-ratio shed units take the room
    spent = sum(int(costs[i, :n[i]].sum()) for i in range(B.N_LISTS))
    assert spent == 5 * K * 10 + 2 * 10 <= 6000
    # the old single-pass answer, for the record: 101 items in all
    assert int(n.sum()) == 5 * K + 2 > K


def test_a_want_past_the_list_length_is_clipped():
    # Each list is only K items long, so a larger want has nothing behind it --
    # and the top-up loop's `clip(n, 0, K - 1)` would otherwise re-read the
    # last item and grant it again.
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.zeros(B.N_LISTS, np.int32)
    values[B.L_SEED0, :], wants[B.L_SEED0] = 5, 10 * K
    n = B.grant(np, values, costs, wants, np.int32(10_000))
    assert int(n[B.L_SEED0]) == K


def test_grant_is_int32_on_both_backends():
    # numpy widens an int32 cumsum/sum to int64 and jnp does not; the purse and
    # every count the planner walks stay int32, so the reductions are pinned.
    import jax.numpy as jnp
    values = np.zeros((B.N_LISTS, K), np.int32)
    costs = np.ones((B.N_LISTS, K), np.int32)
    wants = np.full(B.N_LISTS, 3, np.int32)
    values[:, :3] = 100
    args = (values, costs, wants, np.int32(120))
    for xp, a in ((np, args), (jnp, tuple(jnp.asarray(x) for x in args))):
        assert B.grant(xp, *a).dtype == xp.int32


def test_grant_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(1)
    values = np.sort(rng.integers(0, 500, (B.N_LISTS, K)), axis=1)[:, ::-1].astype(np.int32)
    costs = np.sort(rng.integers(1, 60, (B.N_LISTS, K)), axis=1).astype(np.int32)
    wants = rng.integers(0, 30, B.N_LISTS).astype(np.int32)
    a = B.grant(np, values, costs, wants, np.int32(700))
    b = B.grant(jnp, jnp.asarray(values), jnp.asarray(costs), jnp.asarray(wants), jnp.int32(700))
    assert a.tolist() == np.asarray(b).tolist()
    # ... and with the shed room carried through both loops
    ar = B.grant(np, values, costs, wants, np.int32(700), np.int32(4))
    br = B.grant(jnp, jnp.asarray(values), jnp.asarray(costs), jnp.asarray(wants),
                 jnp.int32(700), jnp.int32(4))
    assert ar.tolist() == np.asarray(br).tolist()
    assert sum(int(ar[i]) for i in B.SHED_LISTS) <= 4


def test_grant_agrees_under_the_traced_loop_too():
    # Without the simulator loaded, `loop.repeat` unrolls the two bisections and
    # the top-ups as Python even on jnp -- which is *not* the code path the day
    # scan runs. Importing `kagg3.sim.rollout` installs `lax.fori_loop`, so this
    # exercises the traced body; the previous implementation is put back so the
    # install does not leak into the rest of the pytest process.
    import jax.numpy as jnp

    from kagg3.core import loop
    rng = np.random.default_rng(2)
    values = np.sort(rng.integers(0, 500, (B.N_LISTS, K)), axis=1)[:, ::-1].astype(np.int32)
    costs = np.sort(rng.integers(1, 60, (B.N_LISTS, K)), axis=1).astype(np.int32)
    wants = rng.integers(0, 30, B.N_LISTS).astype(np.int32)
    a = B.grant(np, values, costs, wants, np.int32(700), np.int32(4))
    saved = loop._impl
    try:
        from kagg3.sim import rollout  # noqa: F401  -- installs lax.fori_loop
        assert loop._impl is not None
        b = B.grant(jnp, jnp.asarray(values), jnp.asarray(costs), jnp.asarray(wants),
                    jnp.int32(700), jnp.int32(4))
        assert a.tolist() == np.asarray(b).tolist()
    finally:
        loop.install(saved)
