"""The three day-window fitness-shaping terms, and their inertness guarantee.

A ledger over 88 live losses to the 2000-2200 band read two things end-of-game
coins cannot see:

* the lead is set on **day 10** -- the band plants ~11.5 melon on day 0 and
  sells 69 units on days 10-11, and in 69 of the 88 games the day-9 -> day-10
  coin swing was larger than the final margin;
* from day 10 on the band holds **56 planted tiles to our 47**, with 0.6 idle
  unlocked tiles to our 9.1.

A second ledger, over 30 recorded top-10 games (rating 2820-2940), reads the
*opposite* opening: those players are level or behind at day 10 (paired gap
-459) and win the second half on realised price -- income d15-29 +19k paired at
flat volume, carrot +28/unit, milk +17, wool +14, strawberry +14, sold through
2.1x our SELL rows in half-size slices (9.6 rows per selling day to our 4.5).
`--late-price-weight` is that one, and it pulls against `--d10-cash-weight` by
construction.

`--d10-cash-weight`, `--tile-fill-weight` and `--late-price-weight` are the
three terms that let the ES pay for any of it. Both default to 0.0, and 0.0 has to be *exactly* inert -- not
"a term multiplied by zero", which is a different floating-point expression and
would silently invalidate every curve this campaign has on disk. That is what
`test_zero_weights_are_the_old_expression` pins, and it is the load-bearing
test in this file.

The other two pin that the terms do something (a ranking that final coins call
a tie is broken by the day-10 purse) and that the quantity being paid for is
the sim's own reading (the evaluator's day-D column *is* `rollout.episode`'s
`daily[D]`, and the tile counts are the board's).
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

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg3 import spec
from kagg3.es import archetypes as AR
from kagg3.es.train import (LATE_PRICE_DAYS, TILE_FILL_DAYS, TILE_FILL_NDAYS,
                            Config, Trainer, make_evaluator, own_coin_score,
                            rank_normalise, shaped_advantage)
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables


def _bare(cfg):
    """A `Trainer` that is nothing but its config -- `fitness_bonus` needs no more."""
    tr = Trainer.__new__(Trainer)
    tr.cfg = cfg
    return tr


def _money(rng, pop=6, E=8):
    """A [pop, E, 11] evaluator result: the columns `day_metrics=True` emits."""
    fin = rng.integers(0, 300_000, (pop, E, 2))
    d10 = rng.integers(0, 40_000, (pop, E, 2))
    fill = rng.integers(-16 * 30, 16 * 60, (pop, E, 1))
    units = rng.integers(1, 400, (pop, E, 1))
    coins = units * rng.integers(20, 200, (pop, E, 1))
    units_o = rng.integers(1, 400, (pop, E, 1))
    coins_o = units_o * rng.integers(20, 200, (pop, E, 1))
    days = rng.integers(1, 16, (pop, E, 1))
    rows = days * rng.integers(1, 12, (pop, E, 1))
    cols = [fin, d10, fill, units, coins, units_o, coins_o, rows, days]
    return jnp.asarray(np.concatenate(cols, axis=2).astype(np.int32))


def _row(final=(120_000, 110_000), d10=(9_000, 9_000), fill=400,
         mine=(100, 4_000), theirs=(100, 4_000), rows=45, days=10):
    """One evaluator row, written out by name so a fixture reads as a claim."""
    return [final[0], final[1], d10[0], d10[1], fill,
            mine[0], mine[1], theirs[0], theirs[1], rows, days]


# ------------------------------------------------------------ (a) 0.0 is inert

def _old_shaped_advantage(mine, theirs, cfg, tape=None):
    """`shaped_advantage` as it stood before the day-10 terms, verbatim.

    Copied rather than imported on purpose: the point of the test is that the
    live function still *evaluates this text*, so the reference has to be the
    text and not a call back into the thing under test.
    """
    rel = jax.nn.sigmoid((mine - theirs) / cfg.margin_scale)
    if tape is not None:
        rel = jnp.where(tape, own_coin_score(mine, cfg), rel)
    rel = rel.mean(axis=1)
    own = jnp.log1p(jnp.maximum(mine, 0.0)).mean(axis=1)
    return (cfg.abs_weight * rank_normalise(own)
            + (1.0 - cfg.abs_weight) * rank_normalise(rel))


@pytest.mark.parametrize("margin_scale", [3_000.0, 100_000.0])
@pytest.mark.parametrize("tape_mask", [False, True])
def test_zero_weights_are_the_old_expression(margin_scale, tape_mask):
    """Bit for bit, on random inputs, at both weights' 0.0 default.

    `np.array_equal` and not `allclose`: an inert flag that moves the last bit
    of the advantage still reorders tied candidates, and ES *is* the ordering.
    """
    rng = np.random.default_rng(20260908)
    cfg = Config(margin_scale=margin_scale)
    assert (cfg.d10_cash_weight, cfg.tile_fill_weight) == (0.0, 0.0)

    for _ in range(8):
        money = _money(rng)
        mine, theirs = money[..., 0], money[..., 1]
        tape = (jnp.asarray(rng.integers(0, 2, mine.shape).astype(bool))
                if tape_mask else None)

        # The inertness is structural, not numeric: no bonus array is built.
        bonus = _bare(cfg).fitness_bonus(money)
        assert bonus is None

        got = np.asarray(shaped_advantage(mine, theirs, cfg, tape, bonus))
        want = np.asarray(_old_shaped_advantage(mine, theirs, cfg, tape))
        assert np.array_equal(got, want)
        # And the 4-argument call every earlier caller makes is the same array.
        assert np.array_equal(
            np.asarray(shaped_advantage(mine, theirs, cfg, tape)), want)


def test_a_zero_weight_beside_a_live_one_adds_nothing():
    """`--tile-fill-weight 0` inside a d10 arm is inert too, term by term."""
    rng = np.random.default_rng(4)
    money = _money(rng)
    only_d10 = _bare(Config(d10_cash_weight=0.5)).fitness_bonus(money)
    both = _bare(Config(d10_cash_weight=0.5,
                        tile_fill_weight=0.0)).fitness_bonus(money)
    assert np.array_equal(np.asarray(only_d10), np.asarray(both))
    want = 0.5 * np.asarray(money[..., 2] - money[..., 3], np.float32)
    assert np.array_equal(np.asarray(only_d10), want)


def test_the_tile_term_is_coins_per_net_tile():
    """`w` is the whole unit conversion: coins added = w * (the logged tiles)."""
    rng = np.random.default_rng(5)
    money = _money(rng)
    bonus = np.asarray(_bare(Config(tile_fill_weight=200.0)).fitness_bonus(money))
    fill = np.asarray(money[..., 4], np.float64) / TILE_FILL_NDAYS
    assert np.allclose(bonus, 200.0 * fill, rtol=1e-6)
    # The gen line logs that same mean, undivided by nothing else.
    assert Trainer.day_metric_means(money)[1] == pytest.approx(fill.mean())


def test_the_metrics_are_read_even_at_weight_zero():
    """The logged pair exists at the 0.0 default -- that is the whole point of it."""
    rng = np.random.default_rng(6)
    money = _money(rng)
    d10, fill, price, rows_per_day = Trainer.day_metric_means(money)
    assert d10 == pytest.approx(float(np.asarray(money[..., 2] - money[..., 3]).mean()))
    assert fill == pytest.approx(float(np.asarray(money[..., 4]).mean()) / TILE_FILL_NDAYS)
    m = np.asarray(money, np.float64)
    assert price == pytest.approx((m[..., 6] / m[..., 5] - m[..., 8] / m[..., 7]).mean(), rel=1e-5)
    assert rows_per_day == pytest.approx((m[..., 9] / m[..., 10]).mean(), rel=1e-5)
    # A 2-column stub (what a dozen tests hand `Trainer.evaluate`) says nothing
    # rather than raising -- but asking it to *shape* is an error, not a zero.
    assert Trainer.day_metric_means(jnp.zeros((3, 2, 2))) is None
    with pytest.raises(ValueError, match="day metrics"):
        _bare(Config(d10_cash_weight=1.0)).fitness_bonus(jnp.zeros((3, 2, 2)))
    with pytest.raises(ValueError, match="day metrics"):
        _bare(Config(late_price_weight=1.0)).fitness_bonus(jnp.zeros((3, 2, 2)))


# ------------------------------------------- (b) a live weight moves the rank

def test_d10_weight_breaks_a_final_margin_tie():
    """Two candidates, identical at the finish, different on day 10.

    Both end on the same coins against the same opponent coins, so the anchor
    and the margin are tied to the bit and `rank_normalise` gives them the same
    advantage -- which is exactly the ledger's complaint: the objective cannot
    see the thing that decided 69 of 88 games. With the weight on, the one that
    stood taller on day 10 ranks above the other.
    """
    # [pop=2, E=1, 11]: same final 120k vs 110k, day-10 purse 30k vs 12k.
    money = jnp.asarray(np.array([[_row(d10=(30_000, 9_000))],
                                  [_row(d10=(12_000, 9_000))]], np.int32))
    mine, theirs = money[..., 0], money[..., 1]

    off = Config(margin_scale=3_000.0)
    flat = np.asarray(shaped_advantage(mine, theirs, off, None,
                                       _bare(off).fitness_bonus(money)))
    assert flat[0] == flat[1]            # the tie the ledger is about

    on = Config(margin_scale=3_000.0, d10_cash_weight=0.5)
    adv = np.asarray(shaped_advantage(mine, theirs, on, None,
                                      _bare(on).fitness_bonus(money)))
    assert adv[0] > adv[1]

    # And the same for a full board against an empty one, at a tile weight.
    tiles = jnp.asarray(np.array([[_row(fill=16 * 40)],
                                  [_row(fill=16 * -5)]], np.int32))
    m2, t2 = tiles[..., 0], tiles[..., 1]
    fill_on = Config(margin_scale=3_000.0, tile_fill_weight=200.0)
    adv2 = np.asarray(shaped_advantage(m2, t2, fill_on, None,
                                       _bare(fill_on).fitness_bonus(tiles)))
    assert adv2[0] > adv2[1]
    assert np.asarray(shaped_advantage(m2, t2, off, None, None))[0] == \
        np.asarray(shaped_advantage(m2, t2, off, None, None))[1]


def test_the_bonus_reaches_a_tape_scored_episode():
    """`--tape-score ours` replaces the margin, so the bonus goes to `mine` there.

    Without this the shaping would be silent on the tape rungs the loss ledger
    was built from, which are a quarter of the episode slots on every arm this
    campaign runs.
    """
    money = jnp.asarray(np.array([[_row(d10=(30_000, 9_000))],
                                  [_row(d10=(12_000, 9_000))]], np.int32))
    mine, theirs = money[..., 0], money[..., 1]
    tape = jnp.ones(mine.shape, bool)          # every episode is a tape episode
    on = Config(margin_scale=3_000.0, d10_cash_weight=0.5)
    adv = np.asarray(shaped_advantage(mine, theirs, on, tape,
                                      _bare(on).fitness_bonus(money)))
    assert adv[0] > adv[1]
    # ... and stays inert on the same rung at weight 0.
    off = Config(margin_scale=3_000.0)
    flat = np.asarray(shaped_advantage(mine, theirs, off, tape, None))
    assert flat[0] == flat[1]


# ---------------------------------------------- (c) the read is the sim's own

def _words(seed):
    return jnp.asarray(np.stack([eod.host_stream(int(seed), d)
                                 for d in range(spec.N_DAYS)]))


# Jitted for the reason `test_kagg2_flow._episode` gives: an eager 30x24 scan
# compiles every primitive separately and segfaults the CPU backend.
@jax.jit
def _plain(tables, thetas, words, hi, lo):
    return rollout.episode(tables, thetas, words, hi, lo)


@jax.jit
def _with_tiles(tables, thetas, words, hi, lo):
    return rollout.episode(tables, thetas, words, hi, lo, day_tiles=True)


def test_day_metrics_are_the_sims_own_end_of_day_reading():
    """One real episode: the evaluator's day-D column *is* `daily[D]`.

    Also that turning the extra output on changes nothing about the game --
    final money, and the whole `daily` trajectory, come back identical.
    """
    tables = build_tables(jnp)
    hi, lo = eod.weed_threshold()
    hi, lo = jnp.int32(hi), jnp.int32(lo)
    words = _words(777_001)
    thetas = jnp.stack([jnp.asarray(AR.archetype_theta(**AR.named("wheat_clone"))),
                        jnp.asarray(AR.archetype_theta(**AR.named("mixed_ranch")))])

    money, daily, st = _plain(tables, thetas, words, hi, lo)
    money2, daily2, st2, tiles = _with_tiles(tables, thetas, words, hi, lo)
    assert np.array_equal(np.asarray(money), np.asarray(money2))
    assert np.array_equal(np.asarray(daily), np.asarray(daily2))

    # Five columns, plus the forward-admit gene's own on a tree that carries
    # the block (`rollout.FWD_GENE`, `tests/test_gene_diag.py`).
    assert tiles.shape == (spec.N_DAYS, 2, 5 + int(rollout.FWD_GENE))
    assert tiles.dtype == jnp.int32
    # The sale ledger only ever grows.
    led = np.asarray(tiles)[:, :, 2:5]
    assert (np.diff(led, axis=0) >= 0).all()
    assert (led[-1] > 0).all(), "both seats sold something over a season"
    # The last row is the final board, which the returned state also carries.
    kind = np.asarray(st2.kind)
    assert np.array_equal(
        np.asarray(tiles[-1, :, :2]),
        np.stack([(kind == spec.KIND_PLANT).sum(axis=1),
                  ((kind == spec.KIND_EMPTY) | (kind == spec.KIND_WEED)).sum(axis=1)],
                 axis=1))
    assert np.array_equal(np.asarray(tiles[-1, :, 2]), np.asarray(st2.sold_n))
    assert np.array_equal(np.asarray(tiles[-1, :, 3]), np.asarray(st2.sold_rev))
    assert np.array_equal(np.asarray(tiles[-1, :, 4]), np.asarray(st2.sold_rows))
    # A rollout that was not asked for the ledger does not keep one.
    assert not np.asarray(st.sold_n).any()
    # Nothing is double-counted and nothing is invented: every tile is locked,
    # idle, planted or placed.
    per_seat = np.asarray(tiles[-1, :, :2]).sum(axis=1)
    assert (per_seat <= spec.TILE_QUAD.shape[0]).all()

    for D in (0, 10, spec.N_DAYS - 1):
        ev = make_evaluator(hi, lo, day_metrics=True, d10_cash_day=D)
        for seat in (0, 1):
            row = np.asarray(ev(
                tables,
                thetas[seat][None], thetas[1 - seat][None], words[None],
                jnp.asarray([seat], jnp.int32),
                jnp.ones((1, 2), jnp.int32),
                jnp.full((1, 2), spec.STARTING_MONEY, jnp.int32))[0])
            assert row.shape == (11 + int(rollout.FWD_GENE),)
            assert row.dtype == np.int32           # no float promotion
            assert row[0] == np.asarray(money)[seat]
            assert row[1] == np.asarray(money)[1 - seat]
            # The claim under test: our day-D purse is the sim's own day-D row.
            assert row[2] == np.asarray(daily)[D, seat]
            assert row[3] == np.asarray(daily)[D, 1 - seat]
            d0, d1 = TILE_FILL_DAYS
            t = np.asarray(tiles)
            assert row[4] == (t[d0:d1 + 1, seat, 0] - t[d0:d1 + 1, seat, 1]).sum()
            # ... and the late window is the ledger's own difference.
            p0, p1 = LATE_PRICE_DAYS
            for col, out in ((2, 5), (3, 6)):
                assert row[out] == t[p1, seat, col] - t[p0 - 1, seat, col]
            for col, out in ((2, 7), (3, 8)):
                assert row[out] == t[p1, 1 - seat, col] - t[p0 - 1, 1 - seat, col]
            assert row[9] == t[p1, seat, 4] - t[p0 - 1, seat, 4]
            per_day = t[p0:p1 + 1, seat, 4] - t[p0 - 1:p1, seat, 4]
            assert row[10] == (per_day > 0).sum()
            assert 0 <= row[10] <= p1 - p0 + 1


def test_late_price_weight_breaks_a_final_margin_tie():
    """Same finish, same day 10, different realised price over days 15-29.

    The top-10 ledger's whole finding is that this is the axis their edge sits
    on, and end-of-game coins on a tape rung cannot separate the two rows
    below at all.
    """
    money = jnp.asarray(np.array(
        [[_row(mine=(200, 200 * 120), theirs=(200, 200 * 95))],
         [_row(mine=(200, 200 * 90), theirs=(200, 200 * 95))]], np.int32))
    mine, theirs = money[..., 0], money[..., 1]

    off = Config(margin_scale=3_000.0)
    assert _bare(off).fitness_bonus(money) is None
    flat = np.asarray(shaped_advantage(mine, theirs, off, None, None))
    assert flat[0] == flat[1]

    on = Config(margin_scale=3_000.0, late_price_weight=150.0)
    bonus = np.asarray(_bare(on).fitness_bonus(money))
    assert bonus[0] == pytest.approx(150.0 * (120 - 95))
    assert bonus[1] == pytest.approx(150.0 * (90 - 95))
    adv = np.asarray(shaped_advantage(mine, theirs, on, None,
                                      jnp.asarray(bonus)))
    assert adv[0] > adv[1]


def test_a_seat_that_sold_nothing_late_prices_at_zero():
    """Not NaN, and not "unmeasured": no late sale is the worst late price."""
    money = jnp.asarray(np.array([[_row(mine=(0, 0), theirs=(200, 200 * 95))]],
                                 np.int32))
    ours, opp = Trainer.realised_price(money)
    assert float(ours[0, 0]) == 0.0
    assert float(opp[0, 0]) == pytest.approx(95.0)
    bonus = np.asarray(_bare(Config(late_price_weight=1.0)).fitness_bonus(money))
    assert np.isfinite(bonus).all()
    assert bonus[0, 0] == pytest.approx(-95.0)


def test_rows_per_selling_day_is_logged_and_never_divides_by_zero():
    """The slicing diagnostic: 9.6 for the top ten, 4.5 for us."""
    money = jnp.asarray(np.array([[_row(rows=96, days=10)],
                                  [_row(rows=0, days=0)]], np.int32))
    got = Trainer.day_metric_means(money)
    assert got is not None
    assert got[3] == pytest.approx((9.6 + 0.0) / 2)


def test_the_three_weights_are_independent_and_additive():
    """Each term is its own summand, and any subset at 0 contributes nothing."""
    rng = np.random.default_rng(11)
    money = _money(rng)
    kw = dict(d10_cash_weight=0.5, tile_fill_weight=200.0,
              late_price_weight=150.0)
    total = np.asarray(_bare(Config(**kw)).fitness_bonus(money))
    parts = sum(np.asarray(_bare(Config(**{k: v})).fitness_bonus(money))
                for k, v in kw.items())
    assert np.allclose(total, parts, rtol=1e-5, atol=1e-3)


def test_the_evaluator_without_day_metrics_is_two_columns():
    """Off is off: the default evaluator emits the row it always emitted."""
    tables = build_tables(jnp)
    hi, lo = eod.weed_threshold()
    hi, lo = jnp.int32(hi), jnp.int32(lo)
    words = _words(777_002)
    th = jnp.asarray(AR.archetype_theta(**AR.named("wheat_clone")))
    ev = make_evaluator(jnp.int32(hi), jnp.int32(lo))
    row = np.asarray(ev(
        tables, th[None], th[None], words[None],
        jnp.zeros(1, jnp.int32), jnp.ones((1, 2), jnp.int32),
        jnp.full((1, 2), spec.STARTING_MONEY, jnp.int32)))
    assert row.shape == (1, 2)
