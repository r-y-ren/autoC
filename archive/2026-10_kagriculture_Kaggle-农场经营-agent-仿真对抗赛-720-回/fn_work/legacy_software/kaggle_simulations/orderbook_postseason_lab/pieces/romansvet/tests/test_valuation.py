"""Fire schedules and coin values (PLANNER_V3_1 sections 0.2, 0.6, 0.11) are
closed-form integer arithmetic over the engine's tables. Checked against a
brute-force replay of the end-of-day rules and against the spec's own numbers.
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
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P          # binds `valuation._PLAN`, so `pay_day` reads the switch
from kagg3.core import valuation as V

PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)   # the default base prices
I = np.int32


def _brute_fires(t_day, first, interval, lo, hi):
    return sum(1 for h in range(lo, hi + 1)
               if h - t_day - first >= 0 and (h - t_day - first) % interval == 0)


def test_fires_between_matches_brute_force():
    rng = np.random.default_rng(0)
    for _ in range(300):
        t_day, first = int(rng.integers(0, 29)), int(rng.integers(1, 11))
        interval = int(rng.integers(1, 4))
        lo, hi = int(rng.integers(0, 30)), int(rng.integers(0, 30))
        got = int(V.fires_between(np, I(t_day), I(first), I(interval), I(lo), I(hi)))
        assert got == _brute_fires(t_day, first, interval, lo, hi), (t_day, first, interval, lo, hi)


def test_fires_between_is_vectorised_over_tiles():
    t_day = np.array([0, 5, 20], np.int32)
    got = V.fires_between(np, t_day, I(4), I(1), I(6), I(28))       # geese
    assert got.tolist() == [23, 20, 5]                                # h = 6..28, 9..28, 24..28


def test_fires_on_and_next_fire_after():
    # cow placed day 0: fires on harvest days 8, 10, 12, ...
    assert bool(V.fires_on(np, I(0), I(8), I(2), I(8)))
    assert not bool(V.fires_on(np, I(0), I(8), I(2), I(9)))
    assert not bool(V.fires_on(np, I(0), I(8), I(2), I(7)))
    # a CARE on day 9 pays on the first fire whose eod is after day 9's: day 12
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(9))) == 12
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(8))) == 10
    assert int(V.next_fire_after(np, I(0), I(8), I(2), I(2))) == 8      # before maturity: the first fire
    # goose (interval 1): always the day after tomorrow
    assert int(V.next_fire_after(np, I(0), I(4), I(1), I(10))) == 12


def test_crop_fires_stop_at_max_yield():
    tomato = I(spec.I_TOMATO)                     # first 8, interval 1, max_yield 4
    fires = [bool(V.crop_fires_on(np, I(0), tomato, I(h))) for h in range(6, 14)]
    assert fires == [False, False, True, True, True, True, False, False]   # 8..11 only


@pytest.mark.parametrize("horizon", [False, True])
def test_animal_value_at_the_spec_numbers(monkeypatch, horizon):
    """0.2's stream, counted to `pay_day()` and not to `LAST_SHED_DAY`.

    A goose fires at every end of day and the harvest of a fire at eod `e` is
    sellable on `e + 1`, so the count is one longer on the 29-day horizon and
    the last day that still holds a live goose moves with it."""
    monkeypatch.setattr(P, "HORIZON_DROP_ON", horizon)
    n = V.pay_day() - 5                        # goose placed day 0, seen on day 5
    assert n == 23 + (1 if horizon else 0)
    # n eggs at 50, n fertilizers at 100
    v = V.animal_value(np, PRICE, I(0), I(0), I(0), I(0), I(5))
    assert int(v) == n * 50 + n * 100
    # banked units and today's fertilizer count too
    v2 = V.animal_value(np, PRICE, I(0), I(2), I(1), I(0), I(5))
    assert int(v2) == int(v) + 2 * 50 + 100
    # A goose seen on day 28 has one more egg and one more fertilizer to sell
    # under the DROP horizon, and nothing at all without it; day 29 is empty
    # either way -- there is no day after it to harvest the eod-29 fire on.
    assert int(V.animal_value(np, PRICE, I(0), I(0), I(0), I(0), I(28))) == \
        (50 + 100 if horizon else 0)
    assert int(V.animal_value(np, PRICE, I(0), I(0), I(0), I(0), I(29))) == 0


@pytest.mark.parametrize("horizon", [False, True])
def test_fertilizer_value_at_the_spec_numbers(monkeypatch, horizon):
    """The harvest age the planner actually uses [0.1, section 4].

    `plan._derive` and `brain.n_free_slots` both build it as
    `clip(pay_day() - t_day, CROP_FIRST_YIELD_DAY, CROP_SATURATE_AGE)`, and
    neither half of that is what this test used to assume. The upper clamp is
    the **saturation** age, not `CROP_MAX_YIELD_DAY`: they agree for every crop
    but melon, whose last two window days add no units (age 10 against 12). The
    deadline is `valuation.pay_day()`, which `plan.HORIZON_DROP_ON` moves from
    28 to 29 -- so the two horizon-sensitive rows below are parametrized rather
    than pinned to `LAST_SHED_DAY`.
    """
    monkeypatch.setattr(P, "HORIZON_DROP_ON", horizon)
    H = V.pay_day()
    assert H == O.LAST_SHED_DAY + (1 if horizon else 0)
    ha = lambda crop, t_day: I(int(np.clip(H - t_day, spec.CROP_FIRST_YIELD_DAY[crop],
                                           spec.CROP_SATURATE_AGE[crop])))
    # tomato planted day 0 fertilized on day 8: fires 9, 10, 11 in the window -> +3
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(8), ha(2, 0))) == 3 * 60
    # on day 10 only fire 11 is left; on day 11 nothing
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(10), ha(2, 0))) == 60
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(0), I(spec.I_TOMATO), I(11), ha(2, 0))) == 0
    # wheat planted day 0 fertilized on day 2: +2 (whole-window cap); carrot +1
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_WHEAT), I(2), ha(0, 0))) == 2 * 25
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_CARROT), I(2), ha(1, 0))) == 35
    # melon saturates at age 10, two days before its window closes: a fertilizer
    # on day 6 buys nothing the remaining waterings do not already reach.
    assert int(spec.CROP_SATURATE_AGE[spec.I_MELON]) == 10 < int(spec.CROP_MAX_YIELD_DAY[spec.I_MELON])
    assert int(V.fert_marginal_value(np, PRICE, I(0), I(1), I(spec.I_MELON), I(6), ha(4, 0))) == 0
    # Same-day chain on a wheat planted day 25 -- harvest age 3 on the 28-day
    # horizon, 4 on the 29-day one: +1 either way, never more.
    assert int(ha(0, 25)) == 3 + (1 if horizon else 0)
    assert int(V.fert_marginal_value(np, PRICE, I(25), I(3), I(spec.I_WHEAT), I(28), ha(0, 25))) == 25
    # The two rows the horizon moves. A day-29 fertilizer pays only if day 29
    # sells, and an ongoing crop's fire at eod 28 monetizes only then too.
    assert int(V.fert_marginal_value(np, PRICE, I(25), I(3), I(spec.I_WHEAT), I(29), ha(0, 25))) == \
        (25 if horizon else 0)
    assert int(V.fert_marginal_value(np, PRICE, I(20), I(0), I(spec.I_TOMATO), I(28), ha(2, 20))) == \
        (60 if horizon else 0)


def test_valuation_agrees_across_backends():
    import jax.numpy as jnp
    t_day = np.array([0, 3, 7, 12, 25], np.int32)
    crop = np.array([2, 0, 3, 4, 0], np.int32)
    ha = np.clip(V.pay_day() - t_day, spec.CROP_FIRST_YIELD_DAY[crop],
                 spec.CROP_SATURATE_AGE[crop]).astype(np.int32)
    a = V.fert_marginal_value(np, PRICE, t_day, np.ones(5, np.int32), crop, I(9), ha)
    b = V.fert_marginal_value(jnp, jnp.asarray(PRICE), jnp.asarray(t_day), jnp.ones(5, jnp.int32),
                              jnp.asarray(crop), jnp.int32(9), jnp.asarray(ha))
    assert a.tolist() == np.asarray(b).tolist()
    c = V.animal_value(np, PRICE, t_day, np.zeros(5, np.int32), np.zeros(5, np.int32),
                       np.array([0, 1, 2, 0, 1], np.int32), I(9))
    d = V.animal_value(jnp, jnp.asarray(PRICE), jnp.asarray(t_day), jnp.zeros(5, jnp.int32),
                       jnp.zeros(5, jnp.int32), jnp.asarray(np.array([0, 1, 2, 0, 1], np.int32)), jnp.int32(9))
    assert c.tolist() == np.asarray(d).tolist()
