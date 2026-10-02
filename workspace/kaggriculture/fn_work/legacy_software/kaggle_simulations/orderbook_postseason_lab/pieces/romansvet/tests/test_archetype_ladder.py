"""Archetypes sit beside the self-play pool: faced every generation like a
rung, never evicted, never snapshotted over -- and now on a *fixed share* of
the episode slots.

The flat round-robin they used to share with the pool was the quiet half of the
self-play problem. With 12 pool rungs plus theta against 4 archetypes, about
three episodes in four faced the policy's own lineage, so the gradient was
mostly about beating clones while the yardstick was entirely about beating
strategies. `arch_frac` sets the split directly.

`Trainer.__init__` also probes every archetype before training starts: the
archetypes *are* the absolute yardstick, so a rung that earns nothing rescales
it silently. The old `wheat_farmer` was measured at 0 coins.

Since 2026-08-26 the file also covers the three things that turn "an equal
share of every rung" into a mixture: the largest-remainder **slot allocation**
`--rung-weight` divides the archetype block with, the **ninth rung**
(`kagg2_proxy`, `mixed_ranch` played from a handicapped opening) and the
**second liveness floor** -- `MIN_COINS` asks whether a rung can earn at all,
`COLLAPSE_KEEP` asks whether it still earns with a real policy on the board.
Every one of them is asserted inert at the defaults as well as live under its
flag, because "an unflagged run is the run that came before" is the property
that lets two training curves be compared.
"""
from __future__ import annotations

import copy
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import jax.numpy as jnp
import numpy as np
import pytest
import train as T

from kagg3.es.train import Config, Trainer, largest_remainder, opponent_slots
from kagg3.es import archetypes as A


def _tiny(**kw):
    # `holdout_rungs` off by default here: it adds two rungs to
    # `absolute_report`'s batch, and a second input shape is a second XLA
    # compile in a file that builds a dozen Trainers. The rungs have their own
    # tests, which turn it back on.
    return Config(pop=4, episodes=4, chunk=8, abs_pairs=2,
                  **dict({"holdout_rungs": False}, **kw))


def test_default_archetypes_are_the_first_named_ones():
    tr = Trainer(_tiny(n_archetypes=4), seed=0)
    assert len(tr.archetypes) == 4
    assert tr.archetype_names == list(A.NAMES[:4])
    for th, name in zip(tr.archetypes, A.NAMES):
        assert np.array_equal(np.asarray(th), A.archetype_theta(**A.named(name)))


def test_extra_archetypes_are_sampled_deterministically_from_the_seed():
    n = len(A.NAMES) + 2
    a = Trainer(_tiny(n_archetypes=n), seed=3)
    b = Trainer(_tiny(n_archetypes=n), seed=3)
    assert len(a.archetypes) == n
    assert a.archetype_names[-2:] == ["sampled0", "sampled1"]
    assert all(np.array_equal(np.asarray(x), np.asarray(y))
               for x, y in zip(a.archetypes, b.archetypes))


def test_candidates_are_pool_then_archetypes_then_theta():
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    c = tr.candidates()
    assert len(c) == len(tr.pool) + 2 + 1
    assert np.array_equal(np.asarray(c[-1]), np.asarray(tr.theta))


def test_zero_archetypes_is_the_old_ladder():
    tr = Trainer(_tiny(n_archetypes=0), seed=0)
    assert tr.archetypes == []
    assert tr.archetype_coins == []
    assert len(tr.candidates()) == len(tr.pool) + 1


#: Every named rung's probe coins in *this file's* `_tiny` Trainer
#: (`abs_pairs=2`, so 2 seeds x 2 seats).
#:
#: **Re-measured 2026-09-06 at 5c384af**: this table is the cold-ladder outcome
#: of the *current default planner*, taken from the file's own probe -- one
#: `Trainer(_tiny(n_archetypes=len(A.NAMES)), seed=0)`, `archetype_names` zipped
#: against `archetype_coins`. It was last pinned 2026-08-30 at 532a93e, and
#: roughly fifteen default-on rule changes have landed on `core/plan.py` since,
#: every one of them measured in paired real-engine games before it was
#: promoted: the melon opening and the row that sells it (9455854, c2d5729,
#: ef6aaa6, 001b988), the opening wheat pump (ff3fe12, 9041032, 117a465), the
#: day's first lot going out early (0772ed3), the survival-water / tail-care /
#: mandatory-feed trio (0c8bee8), the day's own fertilizer sold same-day
#: (6d8bf1d), the endgame tomato budget and late-straw cap (faea7ab), the
#: opponent's standing book priced into the plant mix (f557223 / 554069c), and
#: `ROUTE_SPLIT_ON` starting the block the BUY row does not feed (1d03376).
#: The ladder was *expected* to move under all of them and was never re-pinned.
#:
#: No per-commit attribution is claimed here -- fifteen probes of a twelve-rung
#: ladder is not a bisect anyone ran. What the numbers say is that the movement
#: is not a uniform rescale, which is the outcome a broken decode would give:
#: `rancher` +27,916, the `mixed_ranch` pair +24,661 and `rusher` +22,289 gain
#: while `expander` -43,034, `squeeze_seller` -12,403 and `value_farmer` -3,699
#: pay, with `staple_bulk` +1,354 and `patient_grower` -16 barely moving at all.
#: The rungs that hold stock and land it in bulk gained; `expander`, which
#: spends the opening on land, and `squeeze_seller`, whose delay price already
#: empties each day into its first lot, paid. That is the shape of a shared
#: demand curve moving under everyone at once -- these rules mostly buy a seat
#: that already has something to sell a better hour to sell it in -- and not
#: the shape of a decode sliding the whole scale, which would move every rung
#: the same way.
#:
#: **The top of the cold ladder changed hands.** `expander` held it at 95,643
#: and is now sixth at 52,609; the `mixed_ranch` pair tops it at 104,701.5 and
#: `rancher` is third. That order is what
#: `test_mixed_ranch_is_the_eighth_slot_and_the_top_of_the_cold_yardstick`
#: asserts, and it matters more than the coins: the archetypes *are* the
#: absolute yardstick, so the rung that tops them is what a champion is scored
#: against. `es/archetypes.py` quotes the 4-pair figures its own knob tuning is
#: measured on, and they are not these.
#:
#: A re-pin is only ever right when a *rule* moved, as it did here. The
#: inertness argument below is the other reading of a moved entry, and it is
#: the likelier one: if nothing in the engine changed, fix the decode.
#:
#: `kagg2_proxy` is here at `mixed_ranch`'s number to the coin, and that is the
#: assertion, not a coincidence: the ninth rung is the eighth one's theta byte
#: for byte, and `archetype_coins` is the **cold** probe, so the two can only
#: differ if the alias in `es/archetypes.py` drifts. What the handicap does to
#: it is pinned separately, in
#: `test_kagg2_proxy_is_the_ninth_slot_and_is_mixed_ranch_until_handicapped`.
#:
#: Pinned as a table rather than as a floor because the archetypes *are* the
#: absolute yardstick: a decode change that slid the whole scale would still
#: clear `MIN_COINS` and would silently rescale champion selection with it.
LADDER = {
    "expander": 52_609.0,
    "rusher": 68_384.0,
    "rancher": 93_482.5,
    "patient_grower": 29_592.25,
    "value_farmer": 57_674.25,
    "squeeze_seller": 12_618.25,
    "staple_bulk": 17_264.0,
    "mixed_ranch": 104_701.5,
    "kagg2_proxy": 104_701.5,
}


@pytest.fixture(scope="module")
def full_ladder():
    """One Trainer holding every named rung, built once for the file.

    Constructing a `Trainer` probes its archetypes, and the probe compiles a
    fresh XLA program every time -- `make_evaluator` returns a per-instance
    `jax.jit`, so nothing is shared between instances. Four tests below want
    the same nine-rung ladder and none of them writes to it.
    """
    return Trainer(_tiny(n_archetypes=len(A.NAMES)), seed=0)


def test_every_archetype_clears_the_liveness_floor(full_ladder):
    # The thinnest margin on the ladder is `squeeze_seller`, and it is thinner
    # than it was: 25,021 coins at the 2026-08-30 pin, 12,618 at this one
    # against a 10,000 floor. Still a floor test, not a table -- `LADDER` is
    # the table -- but the rung that would trip it first is now this close.
    assert len(full_ladder.archetype_coins) == len(A.NAMES)
    assert min(full_ladder.archetype_coins) >= A.MIN_COINS


def test_the_whole_ladder_is_pinned_rung_by_rung(full_ladder):
    """All nine, to the coin.

    This is also the assertion any later gene claiming to be inert at zero
    theta has to pass. `archetype_theta` builds `np.zeros(PO.N_PARAMS)`, so an
    appended parameter block is all zeros for every rung: if the block really
    decodes to a no-op, every rung walks exactly the plan it walked before and
    this table does not move by a coin. If one entry moves, the gene is not
    inert -- fix the decode, do not re-pin the table.

    `g7`/`gb7` (the market-saturation gate) is the one appended block that
    claims the opposite: `tanh(0) == 0` is the *shipped default*, not a no-op,
    so it was expected to move this table and did. A block that moves it
    without saying so in `policy.SHAPES` is still the bug this test is for.
    """
    tr = full_ladder
    assert tr.archetype_names == list(A.NAMES)
    got = dict(zip(tr.archetype_names, tr.archetype_coins))
    for name, want in LADDER.items():
        assert got[name] == pytest.approx(want, rel=1e-3), name


def test_kagg2_proxy_is_the_ninth_slot_and_is_mixed_ranch_until_handicapped(full_ladder):
    """The rung is not a theta, it is an *opening*.

    Its knobs are `mixed_ranch`'s byte for byte, so at the default
    `--proxy-handicap` (the engine's day 0) the two rungs are the same rung and
    the probe measures them to the coin. What separates them is the start
    `Trainer` gives this slot and no other -- and that is why the probe has to
    play it *with* the handicap, or it would gate a game the run never plays.

    Re-probed here rather than in a second `Trainer`: the batch shape is the
    same, so the handicapped probe reuses the compiled program.
    """
    tr = full_ladder
    assert tr.archetype_names[8] == A.PROXY_NAME == "kagg2_proxy"
    coins = dict(zip(tr.archetype_names, tr.archetype_coins))
    assert coins[A.PROXY_NAME] == coins["mixed_ranch"]
    assert coins[A.PROXY_NAME] >= A.MIN_COINS
    assert (tr.arch_handicap == np.asarray(A.NO_HANDICAP)).all()

    hcap = np.array(tr.arch_handicap)
    hcap[8] = A.PROXY_HANDICAP
    got = dict(zip(tr.archetype_names, tr._probe_archetypes(tr.archetypes, hcap)))

    # Every other rung is unmoved -- the handicap is one slot's start, not a
    # change to the probe -- and the proxy's own number is a different game.
    for name in A.NAMES[:8]:
        assert got[name] == coins[name], name
    assert got[A.PROXY_NAME] > coins[A.PROXY_NAME]
    assert got[A.PROXY_NAME] >= A.MIN_COINS


def test_mixed_ranch_is_the_eighth_slot_and_the_top_of_the_cold_yardstick(full_ladder):
    """The kagg2-shaped rung. It is eighth in `NAMES`, so `--n-archetypes 8` is
    what selects it -- and `kagg2_proxy`, the ninth, is its handicapped twin, so
    the two tie here at the default (unhandicapped) opening.

    Re-pinned 2026-09-06 at 5c384af, with `LADDER`: this is the order the
    *current default planner* plays the cold ladder in, and the top of it
    changed hands. The pair held it before the saturation-age harvest, lost it
    to `expander` there, and has it back -- 104,701.5 against `expander`'s
    52,609, which is now sixth. Behind them `rancher` 93,482.5 and `rusher`
    68,384 take third and fourth from `value_farmer` 57,674.25. See `LADDER`
    for the rule changes that were live in between and for why no one of them
    is credited with this.

    The order is the assertion, not the fact that any one rung tops the ladder
    -- the archetypes *are* the absolute yardstick, so which rung sets its
    ceiling is what a champion is scored against, and the name of that rung is
    a thing a run's absolute score cannot be read without.

    The coins here are this `_tiny` Trainer's own probe -- `abs_pairs=2`, so 2
    seeds x 2 seats -- and not the 4-pair numbers `es/archetypes.py` quotes.
    Both are asserted somewhere: the floor above is what a real run gates on,
    this pins the shape of the top of the yardstick, so a silent decode change
    cannot reshuffle it without a test noticing.
    """
    tr = full_ladder
    assert tr.archetype_names[7] == "mixed_ranch"
    # The pin is over the original nine rungs: the Kaggle-population rungs
    # appended after `kagg2_proxy` (2026-08-28) set a higher ceiling and are
    # ranked by their own tests.
    coins = {n: c for n, c in zip(tr.archetype_names, tr.archetype_coins)
             if n in A.NAMES[:9]}
    ranked = sorted(coins, key=coins.get, reverse=True)
    assert set(ranked[:2]) == {"mixed_ranch", "kagg2_proxy"}    # 104,701.5 apiece
    assert coins["mixed_ranch"] > coins["value_farmer"]         # 104,702 vs 57,674
    assert coins["mixed_ranch"] > coins["expander"]             # ... and vs 52,609
    # Third, fourth, fifth and sixth, and in that order.
    assert ranked[2] == "rancher"
    assert ranked[3] == "rusher"
    assert ranked[4] == "value_farmer"
    assert ranked[5] == "expander"
    assert coins["value_farmer"] == pytest.approx(57_674, rel=1e-3)


def test_a_dead_named_archetype_refuses_to_train(monkeypatch):
    """The point of the probe: a 0-coin rung must stop the run, not join it.

    A named archetype is a hand-written table entry, so a failure there is a bug
    in the table and there is nothing to redraw. Simulated by moving the floor
    above every archetype rather than by shipping a broken one.
    """
    monkeypatch.setattr(A, "MIN_COINS", 1e12)
    with pytest.raises(ValueError, match="liveness probe failed"):
        Trainer(_tiny(n_archetypes=2), seed=0)


def test_a_restored_archetype_set_is_re_probed_and_can_be_refused():
    """`--resume` swaps the set after `__init__` probed it.

    Every checkpoint written before 2026-08-25 holds the 0-coin `wheat_farmer`,
    so resuming one would put the dead rung straight back into the yardstick.
    Restored rungs are not redrawn -- they are reported.
    """
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    good = tr.reprobe_archetypes()
    assert good == tr.archetype_coins and min(good) >= A.MIN_COINS

    # A rung that develops nothing and hires anyway.
    #
    # `dev = -30` drives `sigmoid(dev + free_urgency * n_free / 25)` under one
    # part in 10^7 on every board the season reaches, so `n_dev` floors to 0
    # every single day: no tile is ever developed, so nothing is ever planted
    # and no animal is ever placed. Checked directly, not inferred -- one
    # `rollout.episode` of this theta leaves a final board with 0 PLANT, 0
    # PASTURE and 0 COOP tiles, so there is nothing in the shed to sell on any
    # day, day 29's included.
    #
    # `dev` alone used to bottom out at 0 coins because the `land` knob spent
    # the whole purse on quadrants. It does not any more: it buys one 1,000
    # quadrant of `spec.STARTING_MONEY` 3,000 and stops, and a rung that earns
    # nothing but keeps 2,000 is only *poor*. So the purse is burned instead --
    # `hire_bias = 30` saturates the crew gene at `brain.HIRE_BIAS_MAX` 400
    # coins per hand, and the rung hires hands it has no work for until the
    # wage bill takes everything: **0 coins**, all four probe games, and 0 is
    # the floor rather than a number that happened to land there. That exact 0
    # is asserted below rather than inferred from the raise -- a refusal that
    # fired because the rung merely earned *little* would be a weaker test than
    # this file claims to be.
    #
    # Hand-built rather than drawn: `sample_archetype` cannot reach it (`dev`
    # is sampled from [-1, 6]), which is the point. A checkpoint's archetype
    # set is not a sample -- it is whatever the run that wrote it held, and the
    # pre-2026-08-25 checkpoints hold a rung exactly this dead.
    dead = A.archetype_theta(**dict(A.named("patient_grower"),
                                    dev=-30.0, hire_bias=30.0))
    tr.archetypes[1] = np.asarray(dead)
    with pytest.raises(ValueError, match="restored archetypes fail") as exc:
        tr.reprobe_archetypes()
    # The refusal quotes the coins it measured, so the "0" is read off the
    # probe rather than assumed -- and asserting it costs no second rollout.
    assert f"{tr.archetype_names[1]}=0 coins" in str(exc.value), str(exc.value)


# ------------------------------------------------------------------ slot split

def test_arch_frac_sets_the_share_of_slots_facing_an_archetype():
    idx = opponent_slots(16, n_pool=12, n_arch=4, arch_frac=0.5)
    is_arch = (idx >= 12) & (idx < 16)
    assert is_arch.sum() == 8
    # Every archetype is faced, and equally often: round-robin inside the group.
    assert sorted(np.bincount(idx[is_arch] - 12).tolist()) == [2, 2, 2, 2]


def test_the_non_archetype_slots_round_robin_the_pool_and_theta():
    idx = opponent_slots(16, n_pool=3, n_arch=4, arch_frac=0.5)
    other = idx[8:]
    # Pool rungs are 0..2 and theta is the last entry of `pool + arch + [theta]`.
    assert set(other.tolist()) == {0, 1, 2, 3 + 4}
    # The current parameters are always in the rotation: against a purely frozen
    # pool the win rate saturates between snapshots and the rank signal vanishes.
    assert (other == 7).sum() == 2


def test_arch_frac_zero_and_no_archetypes_are_the_flat_ladder():
    flat = opponent_slots(9, n_pool=2, n_arch=3, arch_frac=0.0)
    assert np.array_equal(flat, np.array([0, 1, 5, 0, 1, 5, 0, 1, 5]))
    none = opponent_slots(4, n_pool=2, n_arch=0, arch_frac=0.5)
    assert np.array_equal(none, np.array([0, 1, 2, 0]))


@pytest.mark.parametrize("n_pairs,n_pool,n_arch,frac", [
    (32, 12, 4, 0.5), (32, 12, 6, 0.75), (1, 1, 1, 0.5), (7, 3, 2, 0.3),
    (32, 1, 4, 1.0), (5, 4, 0, 0.9),
])
def test_slots_are_always_a_valid_index_of_the_right_length(n_pairs, n_pool, n_arch, frac):
    idx = opponent_slots(n_pairs, n_pool, n_arch, frac)
    assert idx.shape == (n_pairs,)
    assert idx.min() >= 0 and idx.max() < n_pool + n_arch + 1


# --------------------------------------------------------- weighted allocation

def test_largest_remainder_always_spends_exactly_k_slots():
    for k in range(40):
        for w in ([1, 1, 1, 1], [3, 2, 1.5, 1, 1, 1, 1, 1, 1], [5, 1], [1e-6, 1]):
            take = largest_remainder(k, w)
            assert take.sum() == k, (k, w)
            assert (take >= 0).all()


def test_a_flat_weight_vector_allocates_exactly_as_the_round_robin_does():
    """The no-op guarantee, at the level that matters: counts per rung.

    `weights=None` keeps the interleaved layout byte for byte; an explicit flat
    vector lays the same *multiset* out as contiguous blocks. Anything else and
    "all weights 1" would not mean "unweighted".
    """
    for n_pairs, n_arch in ((16, 4), (16, 9), (7, 4), (33, 5)):
        k = round(0.5 * n_pairs)
        flat = opponent_slots(n_pairs, 12, n_arch, 0.5, np.ones(n_arch))
        rr = opponent_slots(n_pairs, 12, n_arch, 0.5)
        assert np.array_equal(np.bincount(flat[:k] - 12, minlength=n_arch),
                              np.bincount(rr[:k] - 12, minlength=n_arch))
        assert np.array_equal(np.sort(flat), np.sort(rr))
        assert np.array_equal(flat[k:], rr[k:])      # the pool half is untouched


def test_weights_move_the_share_and_the_plan_s_own_row_comes_out():
    """The allocation §3.3 of the plan tabulates, reproduced exactly.

    32 pairs, `arch_frac` 0.5 -> 16 archetype pairs over 9 rungs at
    `kagg2_proxy` 3, `mixed_ranch` 2, `value_farmer` 1.5 and 1 elsewhere:
    floors sum to 12 and the four largest remainders take the rest.
    """
    names = list(A.NAMES[:9])   # the plan's nine-rung ladder
    w = np.ones(len(names))
    w[names.index("kagg2_proxy")] = 3.0
    w[names.index("mixed_ranch")] = 2.0
    w[names.index("value_farmer")] = 1.5

    take = largest_remainder(16, w)

    got = dict(zip(names, take.tolist()))
    assert got["kagg2_proxy"] == 4        # 12.5% of 64 episodes, from nothing
    assert got["mixed_ranch"] == 3        # 9.4%, from 6.25%
    assert got["value_farmer"] == 2
    assert got["expander"] == 2           # first of the remainder tie
    assert sum(take) == 16
    # The two rungs carrying the kagg2 shape: 6.25% -> 21.9% of the episodes.
    assert (got["kagg2_proxy"] + got["mixed_ranch"]) / 32 == pytest.approx(0.21875)

    idx = opponent_slots(32, n_pool=12, n_arch=len(names), arch_frac=0.5, weights=w)
    assert np.array_equal(np.bincount(idx[:16] - 12, minlength=len(names)), take)


def test_a_zero_weight_rung_is_left_out_of_the_gradient_entirely():
    w = np.array([1.0, 0.0, 1.0])
    idx = opponent_slots(8, n_pool=2, n_arch=3, arch_frac=0.5, weights=w)
    assert (idx[:4] != 2 + 1).all()          # rung 1 never faced
    assert set(idx[:4].tolist()) == {2, 4}


@pytest.mark.parametrize("bad", [[-1.0, 1.0], [0.0, 0.0], [np.nan, 1.0]])
def test_a_meaningless_weight_vector_is_refused(bad):
    with pytest.raises(ValueError, match="non-negative|not all zero|finite"):
        largest_remainder(4, bad)


@pytest.fixture(scope="module")
def three_rungs():
    """A 3-rung Trainer, built once; `_clone` hands each test a private view.

    Same reason as `full_ladder`: the construction cost is an XLA compile, and
    every test below only *rebinds* attributes (the config, a canned evaluator,
    the probe coins) rather than mutating the ladder itself.
    """
    return Trainer(_tiny(n_archetypes=3), seed=0)


def _clone(tr, **cfg_kw):
    out = copy.copy(tr)
    out.cfg = tr.cfg._replace(**cfg_kw)
    out._bind_rungs()
    return out


def test_the_trainer_binds_weights_by_name_and_refuses_a_typo(three_rungs):
    weighted = _clone(three_rungs, rung_weight=(("rusher", 4.0),))
    assert weighted.rung_weights.tolist() == [1.0, 4.0, 1.0]
    assert weighted.weighted_slots() is weighted.rung_weights

    assert three_rungs.rung_weights.tolist() == [1.0, 1.0, 1.0]
    # None, not ones: it is what keeps an unflagged run on the byte-identical
    # interleaved row rather than on an equivalent one.
    assert three_rungs.weighted_slots() is None

    with pytest.raises(ValueError, match="no such rung"):
        _clone(three_rungs, rung_weight=(("mixed_ranch", 2.0),))
    # And from the flag end, before the run directory exists at all.
    with pytest.raises(SystemExit, match="no rung called"):
        T.parse_rung_weights(["mixed_ranch=2"], T.rung_names(3))


# ------------------------------------------------------- the collapse ceiling

def _canned(tr, theirs_per_rung, mine=100_000.0):
    """Give `tr` an evaluator that returns fixed coins per rung. -> the Trainer."""
    n = len(theirs_per_rung)
    theirs = np.asarray(theirs_per_rung, float)

    def canned(tables, cand, opp, words, seat, nq, mo):
        # `absolute_report` indexes the batch as `arange(total) % n_rungs`.
        i = np.arange(cand.shape[0]) % n
        return jnp.stack([jnp.full(cand.shape[0], mine),
                          jnp.asarray(theirs[i])], axis=1)

    tr.evaluate = canned
    return tr


def test_the_collapse_ceiling_flags_a_rung_that_folds_against_a_real_policy(three_rungs):
    """`MIN_COINS` asks "can it earn"; this asks "does it still earn *here*".

    Measured 2026-08-25, `staple_bulk` took 17,560 coins off the zero theta and
    **838** off the then-incumbent -- 4.8% -- while being an eighth of the
    yardstick and its single largest own-coin term. A rung that folds like that
    is not an opponent, it is a free win, and averaging it in rescales the
    number selection reads.
    """
    tr = _clone(three_rungs, collapse_floor=A.COLLAPSE_KEEP)
    tr.archetype_coins = [20_000.0] * 3
    _canned(tr, [16_000.0, 1_000.0, 16_000.0])

    rep = tr.absolute_report(tr.theta)

    assert [round(k, 3) for k in rep.keep] == [0.8, 0.05, 0.8]
    assert list(rep.live) == [True, False, True]
    assert rep.weights == (1.0, 0.0, 1.0)
    # The dropped rung leaves the mean rather than dragging it: 100k either
    # way here, but the *weights* are what a real gap would ride on.
    assert rep.coins == pytest.approx(100_000.0)


def test_the_collapse_ceiling_is_off_by_default_and_still_reported(three_rungs):
    tr = _clone(three_rungs)
    assert tr.cfg.collapse_floor == 0.0
    tr.archetype_coins = [20_000.0] * 3
    _canned(tr, [100.0] * 3, mine=90_000.0)

    rep = tr.absolute_report(tr.theta)

    assert list(rep.live) == [True] * 3            # nothing is dropped
    assert [round(k, 4) for k in rep.keep] == [0.005] * 3   # but it is visible


def test_every_rung_collapsing_falls_back_rather_than_measuring_nothing(three_rungs):
    tr = _clone(three_rungs, collapse_floor=0.5)
    tr.archetype_coins = [20_000.0] * 3
    _canned(tr, [100.0] * 3, mine=90_000.0)

    rep = tr.absolute_report(tr.theta)

    assert rep.coins == pytest.approx(90_000.0)
    assert list(rep.live) == [True] * 3
    assert all(k < 0.5 for k in rep.keep)          # reported as the near-miss


# ---------------------------------------------------------- the flags, refused

def test_the_fitted_handicap_and_the_held_out_levels_are_where_a_reader_finds_them():
    """Pinned so a planner merge that invalidates the fit has to say so.

    The handicap is a *measurement* -- what it reproduces of kagg2's
    suppression is a function of the planner, exactly as the rungs' coin
    figures are -- so the constants live beside the table that fitted them and
    a change to either has to move both.
    """
    assert A.PROXY_HANDICAP == (1, 87_000)
    assert A.NO_HANDICAP == (1, 3_000)
    assert A.COLLAPSE_KEEP == 0.25
    assert A.NAMES[8] == A.PROXY_NAME == "kagg2_proxy"
    # Two held-out rungs, two kinds of transfer, neither in the trained ladder.
    labels = [r[0] for r in A.HOLDOUT_RUNGS]
    assert labels == ["mixed_ranch@1:110000", "value_farmer@1:87000"]
    names = {r[1] for r in A.HOLDOUT_RUNGS}
    assert names <= set(A.NAMES) and A.PROXY_NAME not in names
    # The strategy probe rides on the trained handicap and moves with it.
    assert A.HOLDOUT_RUNGS[1][2] == A.PROXY_HANDICAP
    # The handicap probe is a level *up*, or it probes nothing.
    assert A.HOLDOUT_RUNGS[0][2][1] > A.PROXY_HANDICAP[1]


def test_a_rung_weight_is_refused_by_name_before_the_run_directory_exists():
    names = T.rung_names(9)
    assert T.parse_rung_weights(["kagg2_proxy=3", "mixed_ranch=2"], names) == \
        (("kagg2_proxy", 3.0), ("mixed_ranch", 2.0))
    assert T.parse_rung_weights(None, names) == ()

    with pytest.raises(SystemExit, match="no rung called"):
        T.parse_rung_weights(["kagg2_proxy=3"], T.rung_names(8))
    with pytest.raises(SystemExit, match="no rung called"):
        T.parse_rung_weights(["mixed_rnach=2"], names)
    with pytest.raises(SystemExit, match="expected NAME=WEIGHT"):
        T.parse_rung_weights(["mixed_ranch"], names)
    with pytest.raises(SystemExit, match="is not a number"):
        T.parse_rung_weights(["mixed_ranch=lots"], names)
    with pytest.raises(SystemExit, match="finite and non-negative"):
        T.parse_rung_weights(["mixed_ranch=-1"], names)
    with pytest.raises(SystemExit, match="more than once"):
        T.parse_rung_weights(["mixed_ranch=2", "mixed_ranch=3"], names)


def test_the_handicap_flag_is_parsed_and_bounded():
    assert T.parse_handicap("3:20000") == (3, 20_000)
    assert T.parse_handicap("1:87000") == A.PROXY_HANDICAP

    with pytest.raises(SystemExit, match="expected NQUAD:MONEY"):
        T.parse_handicap("87000")
    with pytest.raises(SystemExit, match="integers"):
        T.parse_handicap("1:87k")
    with pytest.raises(SystemExit, match="NQUAD must be 1"):
        T.parse_handicap("5:20000")
    # A handicap can only ever add, so an opening under the engine's own purse
    # is a typo rather than a request.
    with pytest.raises(SystemExit, match="at least the"):
        T.parse_handicap("1:100")


def test_rung_names_matches_what_the_trainer_will_label_its_slots(three_rungs):
    assert T.rung_names(0) == []
    assert T.rung_names(4) == list(A.NAMES[:4])
    assert T.rung_names(len(A.NAMES) + 2)[-2:] == ["sampled0", "sampled1"]
    # The flag is checked against this list before the run directory exists, so
    # it has to be the list the Trainer then builds.
    assert three_rungs.archetype_names == T.rung_names(3)


def test_a_generation_uses_the_split():
    """End to end: the opponent actually played is the one `opponent_slots` names."""
    tr = Trainer(Config(pop=4, episodes=8, chunk=8, abs_pairs=2,
                        n_archetypes=2, arch_frac=0.5), seed=0)
    seen = {}
    real = tr._play

    def spy(thetas, words, opp, tables, starts=None):
        seen["opp"] = np.asarray(opp)
        return real(thetas, words, opp, tables, starts)

    tr._play = spy
    tr.generation()
    opp = seen["opp"]
    assert opp.shape[0] == 4                       # episodes // 2 pairs
    arch = np.stack([np.asarray(a) for a in tr.archetypes])
    faced = sum(any(np.array_equal(o, a) for a in arch) for o in opp)
    assert faced == 2


# ------------------------------------------------------- the Kaggle-field rungs
#
# `wheat_clone` and `wool_specialist` are the two behavioural classes a replay
# autopsy of 64 leaderboard games found (2026-08-27; see the "the Kaggle field"
# block in `es/archetypes.py`). What they are worth to the ladder is what they
# *refuse* to do -- no carrot, no tomato, no goose, no egg -- because those are
# the three markets no opponent in 64 games contested, and a ladder made only
# of this planner's own shapes teaches the policy that every market is fought
# over.

def test_the_field_rungs_are_appended_and_renumber_nothing():
    """The ladder is indexed by position in several places (`--n-archetypes`,
    the handicap row, `scripts/train.py`'s flag check), so the two new rungs
    are only safe at the end of `NAMES`."""
    assert A.NAMES[:9] == ("expander", "rusher", "rancher", "patient_grower",
                           "value_farmer", "squeeze_seller", "staple_bulk",
                           "mixed_ranch", "kagg2_proxy")
    assert A.NAMES[9:] == ("wheat_clone", "wool_specialist", "wheat_clone_v4")
    assert A.NAMES.index(A.PROXY_NAME) == 8
    assert len(A.NAMES) == len(A._NAMED)


def test_both_field_rungs_clear_the_liveness_floor(full_ladder):
    """The floor `Trainer` gates on, on the rungs this file added last.

    Read off the module's own ladder rather than a second Trainer: these two
    are in `NAMES`, so `full_ladder` already probed them, and a fresh Trainer
    would only buy a second XLA compile.
    """
    coins = dict(zip(full_ladder.archetype_names, full_ladder.archetype_coins))
    for name in ("wheat_clone", "wool_specialist", "wheat_clone_v4"):
        assert coins[name] >= A.MIN_COINS, (name, coins[name])


def _field_obs(day, nquad, money):
    """A board the season actually reaches, for the decode sweep below."""
    from kagg3 import spec
    from kagg3.core import brain

    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[spec.TILE_QUAD < nquad] = spec.KIND_EMPTY
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(money),
        kind=kind, occ=z - 1, opp_kind=kind.copy(), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.full(spec.N_CROPS, 50, np.int32),
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=np.asarray(brain._BASE, np.int32), shops=np.zeros(8, np.int32))


@pytest.mark.parametrize("name", ["wheat_clone", "wool_specialist",
                                  "wheat_clone_v4"])
def test_the_field_rungs_never_ask_for_a_carrot_a_tomato_or_a_goose(name):
    """The decode, over every board shape a season reaches.

    This is the whole invariant and not a sample of it: `prod_bias` is a
    staircase on `log1p(base)`, a constant of the market table, and both rungs
    set `crowd = 0`, so the three suppressed products sit 20 logits under wheat
    on *every* board -- a softmax weight of 2e-9, which `_largest_remainder`
    cannot round up, and a grow multiplier of 0, so the planner does not value
    the tile either.
    """
    from kagg3 import spec
    from kagg3.core import brain

    th = A.archetype_theta(**A.named(name))
    for day in (0, 5, 10, 20, 25):
        for nquad in (1, 2, 3):
            for money in (500, 20_000, 120_000):
                m = brain.decide(np, th, _field_obs(day, nquad, money))
                assert int(m.plant_target[spec.I_CARROT]) == 0
                assert int(m.plant_target[spec.I_TOMATO]) == 0
                assert int(m.animal_want[0]) == 0            # GOOSE
                assert int(m.grow_mult[spec.I_EGG]) == 0


def test_wheat_clone_plays_a_whole_sim_season_with_no_goose_and_no_carrot():
    """The same refusal, end to end in the simulator rather than in the decode.

    One episode against the zero theta, and the final board is the evidence
    the season leaves behind: a COOP is never demolished and an animal never
    leaves its tile, so "no coop and no goose at the end" is "none all season".
    """
    from kagg3 import spec
    from kagg3.es.train import host_words
    from kagg3.sim import eod, rollout
    from kagg3.sim.state import build_tables

    th = A.archetype_theta(**A.named("wheat_clone"))
    thetas = jnp.stack([jnp.asarray(th), jnp.zeros(th.shape, jnp.float32)])
    words = jnp.asarray(host_words([11])[0])
    hi_t, lo_t = eod.weed_threshold()
    money, _, st = rollout.episode(build_tables(jnp), thetas, words,
                                   jnp.int32(hi_t), jnp.int32(lo_t))

    kind, occ = np.asarray(st.kind)[0], np.asarray(st.occ)[0]
    assert (kind != spec.KIND_COOP).all()                     # no coop built
    is_animal = kind == spec.KIND_PASTURE
    assert not (is_animal & (occ == 0)).any()                 # no GOOSE placed
    is_plant = kind == spec.KIND_PLANT
    assert not (is_plant & (occ == spec.I_CARROT)).any()
    assert not (is_plant & (occ == spec.I_TOMATO)).any()
    # It planted, and only ever the three crops in its book. Not "wheat is on
    # the board": wheat is a one-time crop the rung replants every four days,
    # so the tiles standing on day 29 are the ongoing ones.
    assert is_plant.any()
    assert set(occ[is_plant].tolist()) <= {spec.I_WHEAT, spec.I_STRAWBERRY,
                                           spec.I_MELON}
    assert float(money[0]) >= A.MIN_COINS
