"""The record has to be taken on games the optimiser could not have aimed at.

`--abs-flow-draws K` fixed the yardstick's flow levels forever, so that two
checkpoints' numbers stay comparable. Comparable they are; unaimable they are
not. `best_abs` is a **max** over a sequence of readings of the *same* K levels
on the *same* fixed seed pairs, so a long enough run stops selecting the theta
that plays the family well and starts selecting the one that plays those exact
games well. Measured 2026-08-27: at K=10 the record climbed +12.9k -> +17.8k
over 150 generations while the same theta's centre margin sat at ~-5k
throughout, and the theta the run called "best" scored **-3,255** against the
real engine where the run's own starting theta scored **+2,465**.

Two flags against that, and both are inert at their defaults:

* `--abs-fresh-draws` re-draws the K levels every measurement, from a stream
  seeded by the generation, so the level set that produced a lucky reading is
  gone before the next one;
* `--best-replicate N` refuses to record a candidate on the reading that
  selected it: the candidate is re-measured N times on levels **and** seed
  pairs it has never been read on, and the record is taken -- at that mean --
  only if the mean clears the bar too.

The evaluator and the measurement are stubbed throughout, for the reason
`tests/test_abs_flow_ensemble.py` gives: what is under test is which games the
report is told to play and how the record rule reduces them, and a stub makes
each of those arithmetic rather than statistical.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest
import train as T

from kagg3.es import kagg2_flow as K2F
from kagg3.es.train import (
    FRESH_SEED,
    NO_BEST,
    AbsReport,
    Config,
    Trainer,
    flow_ensemble_draws,
    fresh_flow_draws,
)

#: A ladder with the flow rung last, as a real run holds it.
NAMES = ["greedy_farmer", "mixed_ranch", K2F.RUNG_NAME]
FLOW = 2
PAIRS = 4

#: A real `Trainer` small enough to build in a test: no archetypes to probe,
#: two seed pairs, no held-out rungs. The same shape `tests/test_best_gate.py`
#: drives `generation()` with.
_CFG = {"pop": 4, "episodes": 2, "chunk": 8, "n_archetypes": 0,
        "abs_pairs": 2, "holdout_rungs": False}


def _rep(coins, hold=0.0, score=0.0, holdout_score=0.0):
    """A stub measurement: only the numbers the record rule reads are real."""
    return AbsReport(coins=coins, win=0.0, mine=(), theirs=(), holdout=hold,
                     holdout_win=0.0, score=score, holdout_score=holdout_score)


def _ev(tables, theta_c, theta_o, words, seat, nquad, money, flow=None):
    """A stand-in evaluator: money as an exact function of the episode.

    Same construction as `tests/test_abs_flow_ensemble.py` -- the rung, the
    seed word, the seat and the flow level are all in the answer and none of
    them twice, so a wrong seed set or a wrong level cannot cancel out.
    """
    o = np.asarray(theta_o)[:, 0].astype(np.int64)
    w = np.asarray(words).reshape(o.shape[0], -1)[:, 0].astype(np.int64)
    s = np.asarray(seat).astype(np.int64)
    f = (np.zeros((o.shape[0], 3), np.int64) if flow is None
         else np.asarray(flow).astype(np.int64))
    on = (f[:, 0] >= 0).astype(np.int64)
    mine = 100_000 + 1_000 * o + 100 * w + 10 * s + on * (f[:, 1] - 1_000)
    theirs = 50_000 + 500 * o + 7 * w + 3 * s + on * 200 * f[:, 2]
    return np.stack([mine, theirs], axis=1).astype(np.float64)


def _stub(t=25, **cfg):
    """A `Trainer` carrying only what the measurement helpers read.

    `__new__` rather than a real construction: these tests are about which
    levels and which seed pairs a measurement is handed, and building the real
    ladder would spend a minute of archetype probing to find out.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**dict({"abs_pairs": PAIRS, "kagg2_flow": True}, **cfg))
    tr.tables = None
    tr.t = t
    tr.theta = np.zeros(3)
    tr.n = 3
    tr.archetype_names = list(NAMES)
    tr.archetypes = [np.full(3, float(i + 1)) for i in range(len(NAMES))]
    tr.archetype_coins = []
    tr.rung_weights = np.ones(len(NAMES))
    tr.arch_handicap = np.zeros((len(NAMES), 2), np.int32)
    tr.holdout_thetas = []
    tr.flow_rung = FLOW
    tr.abs_words = np.arange(PAIRS, dtype=np.float64).reshape(PAIRS, 1, 1)
    tr.n_abs_sel = max(PAIRS // 2, 1)
    tr._check_abs_select()
    tr.abs_draws = tuple(flow_ensemble_draws(
        tr.cfg.abs_flow_draws, tr.cfg.abs_flow_scale, tr.cfg.abs_flow_shift))
    tr.evaluate = _ev
    tr.best_abs, tr.best_hold = NO_BEST, NO_BEST
    return tr


# ------------------------------------------------------------ zero diff

def test_the_config_defaults_are_the_yardstick_that_came_before_these():
    cfg = Config()
    assert cfg.abs_fresh_draws is False and cfg.best_replicate == 0


def test_flags_off_measures_the_fixed_draws_the_old_code_measured():
    """(zero diff) `measurement_draws` with the flag off is `abs_draws`, which
    is `flow_ensemble_draws` -- the exact list the fidelity table was computed
    on. Hard-coded as well as derived, so a change to the generator cannot pass
    through this test the way it would through a re-derivation.
    """
    for k in (0, 4, 10):
        tr = _stub(abs_flow_draws=k)
        assert tr.measurement_draws() == tuple(flow_ensemble_draws(k))
        # And it does not move with the generation, which is the whole property
        # the fixed set exists for.
        tr.t = 10_000
        assert tr.measurement_draws() == tuple(flow_ensemble_draws(k))
    assert _stub(abs_flow_draws=4).measurement_draws() == \
        ((541, 2), (675, 2), (743, -1), (967, -2))
    assert _stub().measurement_draws() == ()


def test_passing_the_run_s_own_draws_and_words_is_the_default_measurement():
    """The two new `absolute_report` arguments default to what the report read
    off `self` before they existed, so `generation`'s explicit call and every
    caller that passes neither build the same batch.
    """
    tr = _stub(abs_flow_draws=2)
    a = tr.absolute_report(tr.theta)
    b = tr.absolute_report(tr.theta, draws=tr.measurement_draws(),
                           words=tr.abs_words)
    assert a == b
    assert a.flow_levels == tr.abs_draws


# --------------------------------------------------------- fresh draws

def test_fresh_draws_move_every_measurement_and_stay_deterministic():
    """(1) A different set each generation, the same set for a given one.

    Determinism is not a nicety here: a resumed run has to re-draw the levels
    it would have drawn, or the same generation of the same run measures two
    different things either side of a restart.
    """
    tr = _stub(abs_flow_draws=4, abs_fresh_draws=True)
    tr.t = 25
    first = tr.measurement_draws()
    assert tr.measurement_draws() == first          # same gen, same levels
    assert len(first) == 4

    tr.t = 50
    second = tr.measurement_draws()
    assert second != first
    # Not merely a reordering: a fresh set is a fresh sample of the family.
    assert sorted(second) != sorted(first)

    # Still the family the flags name -- fresh moves the levels, not the ranges.
    lo, hi = Config().abs_flow_scale
    slo, shi = Config().abs_flow_shift
    for s, d in first + second:
        assert lo <= s <= hi and slo <= d <= shi

    # And it is a different stream from the fixed one, or the flag would be a
    # rename of the thing it replaces.
    assert first != tuple(flow_ensemble_draws(4))


def test_fresh_draws_are_a_pure_function_of_the_generation():
    """Two trainers that share nothing but the generation draw the same levels,
    which is what makes the number reproducible from `log.jsonl` alone."""
    a, b = _stub(abs_flow_draws=3, abs_fresh_draws=True), \
        _stub(abs_flow_draws=3, abs_fresh_draws=True, abs_select="hold")
    a.t = b.t = 175
    assert a.measurement_draws() == b.measurement_draws()
    assert a.measurement_draws() == tuple(fresh_flow_draws(3, 175))
    # The constant is the campaign's, not the fixed set's: the two streams have
    # to be distinguishable or "fresh" is only a relabelling.
    assert fresh_flow_draws(3, 175) != flow_ensemble_draws(3, seed=FRESH_SEED)


def test_the_fresh_family_still_follows_the_range_flags():
    up = _stub(abs_flow_draws=6, abs_fresh_draws=True,
               abs_flow_scale=(800, 1800), abs_flow_shift=(0, 4))
    up.t = 25
    assert all(800 <= s <= 1800 and 0 <= d <= 4 for s, d in up.measurement_draws())


def test_a_replicate_draws_from_a_stream_the_screen_never_touched():
    """(2) The replicate's levels are independent of the screening levels.

    Re-measuring on the very levels that produced a reading re-measures the
    luck, so a replicate that shared them would confirm every lucky screen.
    """
    tr = _stub(abs_flow_draws=4, abs_fresh_draws=True, best_replicate=3)
    tr.t = 25
    screen = tr.measurement_draws()
    reps = [tr.measurement_draws(i) for i in (1, 2, 3)]
    assert all(r != screen for r in reps)
    assert len({tuple(r) for r in reps}) == 3          # and of each other
    assert all(tr.measurement_draws(i) == reps[i - 1] for i in (1, 2, 3))


def test_a_replicate_is_freshened_even_when_the_screen_is_not():
    """`--best-replicate` without `--abs-fresh-draws`: the screen keeps the
    fixed set (so the run's headline column means what it meant), and the
    replicate is still drawn fresh -- replicating on the fixed levels would
    defeat the whole point of replicating."""
    tr = _stub(abs_flow_draws=4, best_replicate=2)
    tr.t = 25
    assert tr.measurement_draws() == tuple(flow_ensemble_draws(4))
    assert tr.measurement_draws(1) != tr.measurement_draws()
    assert tr.measurement_draws(1) == tuple(fresh_flow_draws(4, 25, 1))
    # At K=0 there is no family to draw from and both are empty; the replicate
    # then differs from the screen in its seed pairs alone.
    flat = _stub(best_replicate=2)
    assert flat.measurement_draws() == flat.measurement_draws(1) == ()


# ------------------------------------------------------- fresh seed pairs

def test_replicate_words_are_new_games_and_reproducible():
    """The other half of an independent measurement: the *pairs*.

    Fresh levels on the same 64 seed pairs still re-reads the games the
    screening reading was lucky on, so the replicate draws its pairs from a
    stream of its own.
    """
    tr = Trainer(Config(**_CFG), seed=0)
    tr.t = 25
    a = np.asarray(tr.replicate_words(1))
    assert a.shape == np.asarray(tr.abs_words).shape
    assert not np.array_equal(a, np.asarray(tr.abs_words))
    # Deterministic in (gen, replicate), and independent across both.
    assert np.array_equal(a, np.asarray(tr.replicate_words(1)))
    assert not np.array_equal(a, np.asarray(tr.replicate_words(2)))
    tr.t = 50
    assert not np.array_equal(a, np.asarray(tr.replicate_words(1)))


def test_the_words_argument_moves_which_games_are_played():
    """The override is wired all the way through the batch, not just accepted:
    the same theta on different seed pairs is a different reading."""
    tr = _stub(abs_flow_draws=2)
    other = np.arange(100, 100 + PAIRS, dtype=np.float64).reshape(PAIRS, 1, 1)
    a = tr.absolute_report(tr.theta)
    b = tr.absolute_report(tr.theta, words=other)
    assert a.mine != b.mine and a.theirs != b.theirs
    # And the *shape* of the report is unchanged -- same rungs, same split.
    assert len(a.mine) == len(b.mine) and a.flow_draws == b.flow_draws


# ----------------------------------------------------- the record rule

def _driver(readings, **cfg):
    """A trainer whose measurements are a scripted list. -> (tr, calls)

    `calls` records the `(draws, words)` each measurement was asked for, so a
    test can check that the replicates were played on other games and not
    merely counted.
    """
    tr = Trainer(Config(**dict(_CFG, abs_every=1, champ_every=100, **cfg)),
                 seed=0)
    it, calls = iter(readings), []
    def report(theta, draws=None, words=None):
        calls.append({"draws": None if draws is None else tuple(draws),
                      "words": None if words is None else np.asarray(words)})
        return _rep(*next(it))
    tr.absolute_report = report
    return tr, calls


def test_a_replicate_that_falls_back_leaves_the_record_untouched():
    """(3) The screening reading buys a re-measurement, not the record.

    The lucky-reading signature end to end: a screen far above the record whose
    replicates land back at the ordinary level. Nothing about `best_abs`,
    `best_abs_theta` or `best_hold` may move, and the generation has to count
    as a non-improvement (so the stall detector still sees the run as stalled).
    """
    tr, calls = _driver([(120_000.0, 100_000.0),    # taken, then replicated
                         (110_000.0, 99_000.0),
                         (112_000.0, 101_000.0),
                         (133_162.0, 90_000.0),     # the lucky screen
                         (100_500.0, 99_100.0),     # ... which does not hold up
                         (100_400.0, 99_000.0)],
                        best_replicate=2)
    tr.generation()
    kept, theta = tr.best_abs, np.asarray(tr.best_abs_theta)
    assert kept == pytest.approx(111_000.0)         # the replicate mean
    improved_at = tr.last_improve

    tr.generation()
    assert tr.best_abs == kept
    assert np.array_equal(np.asarray(tr.best_abs_theta), theta)
    assert tr.last_improve == improved_at
    assert tr.replicate_rejects == 1
    assert tr.last_replicate == {"screen": 133_162.0, "replicate": 100_450.0,
                                 "n": 2, "rejected": True}
    # The gate logs the number it decided on, which is the replicate mean.
    assert tr.last_best_gate == {"sel": 100_450.0, "hold": 99_050.0,
                                 "accepted": False}
    # Two extra measurements per candidate, and they were played on other games.
    assert len(calls) == 6
    for c in calls[1:3] + calls[4:6]:
        assert c["words"] is not None
    assert not np.array_equal(calls[4]["words"], calls[5]["words"])
    assert calls[0]["words"] is None and calls[3]["words"] is None


def test_acceptance_records_the_replicate_mean_and_not_the_screen():
    """(3) The recorded value is the unbiased one.

    Keeping the record at the screening value would leave the bar itself set by
    the luck -- the next honest candidate would have to beat a number no honest
    measurement produces -- so the ratchet has to be the replicate mean even
    when the candidate is accepted.
    """
    tr, _ = _driver([(120_000.0, 100_000.0),        # screen
                     (110_000.0, 101_000.0),        # replicates: still a record
                     (112_000.0, 103_000.0)],
                    best_replicate=2)
    tr.generation()
    assert tr.best_abs == pytest.approx(111_000.0)
    assert tr.best_hold == pytest.approx(102_000.0)
    assert tr.last_replicate["screen"] == 120_000.0
    assert tr.last_replicate["rejected"] is False
    assert tr.replicate_rejects == 0
    assert tr.last_improve == tr.t
    assert np.array_equal(np.asarray(tr.best_abs_theta), np.asarray(tr.theta))


def test_the_margin_applies_to_the_replicate_mean_too():
    """`--best-margin` is a bar the record has to clear, and after replication
    the number that has to clear it is the replicate mean. A screen that clears
    the bar and a mean that does not is exactly the case this refuses."""
    tr, _ = _driver([(100_000.0, 99_000.0),
                     (100_000.0, 99_000.0),
                     (105_000.0, 99_000.0),         # +5k on the screen
                     (100_400.0, 99_000.0)],        # +400 on the replicate
                    best_replicate=1, best_margin=2_000.0)
    tr.generation()
    assert tr.best_abs == 100_000.0
    tr.generation()
    assert tr.best_abs == 100_000.0 and tr.replicate_rejects == 1


def test_a_screen_that_does_not_clear_the_bar_is_never_replicated():
    """The cost is per accepted candidate, not per generation: a run that has
    stopped improving pays nothing at all for the flag."""
    tr, calls = _driver([(100_000.0, 99_000.0),
                         (100_000.0, 99_000.0),
                         (90_000.0, 80_000.0)],
                        best_replicate=1)
    tr.generation()
    tr.generation()
    assert len(calls) == 3
    assert tr.best_abs == 100_000.0
    assert tr.last_replicate is None
    # And the log still has a screening number to show for the generation.
    assert tr.last_best_gate == {"sel": 90_000.0, "hold": 80_000.0,
                                 "accepted": False}


def test_a_coin_floor_blocked_replicate_refuses_the_record():
    """`selection_score` gives `None` for a candidate under
    `--select-coin-floor`. A replicate that lands there failed the floor on
    games it was not tuned on, which is the floor doing its job, not a
    measurement to average."""
    tr, _ = _driver([(100_000.0, 99_000.0, 0.9, 0.9),
                     (100_000.0, 99_000.0, 0.9, 0.9),
                     (120_000.0, 99_000.0, 0.95, 0.9),
                     (40_000.0, 99_000.0, 0.99, 0.9)],
                    best_replicate=1, select_metric="score",
                    select_coin_floor=50_000.0)
    tr.generation()
    assert tr.best_abs == 0.9
    tr.generation()
    assert tr.best_abs == 0.9 and tr.replicate_rejects == 1
    assert tr.last_replicate["replicate"] is None
    assert tr.last_best_gate["accepted"] is False


def test_replication_off_is_the_rule_that_came_before_it():
    """(zero diff) With the flag off the screening reading takes the record,
    one measurement per generation, and nothing new appears on the trainer."""
    tr, calls = _driver([(100_000.0, 99_000.0), (133_162.0, 90_000.0)])
    tr.generation(); tr.generation()
    assert tr.best_abs == 133_162.0 and tr.best_hold == 90_000.0
    assert len(calls) == 2 and all(c["words"] is None for c in calls)
    assert tr.last_replicate is None and tr.replicate_rejects == 0


# ------------------------------------------------------- the signature

class _Ladder:
    """The fields `ladder_signature` and the reset rule read, as in
    `tests/test_abs_flow_ensemble.py`."""

    def __init__(self, **cfg):
        self.cfg = Config(**cfg)
        self.archetype_names = ["a", "b"]
        self.rung_weights = np.ones(2)
        self.arch_handicap = np.zeros((2, 2), np.int32)
        self.theta = np.zeros(3)
        self.best_abs, self.best_abs_theta = -4_200.0, np.ones(3)
        self.best_hold, self.champion_score = -4_500.0, -4_200.0


def test_flags_off_writes_the_signature_byte_for_byte():
    """(4) Neither flag may retire an inherited record on a run that does not
    pass them -- and `--best-replicate` may not retire one at all: it changes
    how a record is *taken*, not what the yardstick measures."""
    plain = T.ladder_signature(_Ladder())
    assert plain["flow_ensemble"] == {"k": 0, "draws": []}
    fixed = T.ladder_signature(_Ladder(abs_flow_draws=4))
    assert fixed["flow_ensemble"] == {
        "k": 4, "draws": [[s, d] for s, d in flow_ensemble_draws(4)]}
    assert T.ladder_signature(_Ladder(best_replicate=4)) == plain

    tr = _Ladder(abs_flow_draws=4, best_replicate=8)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, fixed
    assert T.reset_best_if_ladder_changed(tr) is None
    assert tr.best_abs == -4_200.0


def test_fresh_draws_carry_the_family_and_never_the_levels():
    """(1) `fresh: true` retires the record; the levels stay out of it, or the
    signature would differ from itself at every measurement."""
    sig = T.ladder_signature(_Ladder(abs_flow_draws=10, abs_fresh_draws=True))
    ens = sig["flow_ensemble"]
    assert ens["fresh"] is True and ens["k"] == 10
    assert ens["draws"] == []
    # The family the levels are drawn *from* is still part of the yardstick's
    # identity, so recentring it still retires the record (below).
    assert ens["family"] == [[500, 1500], [-2, 2]]

    tr = _Ladder(abs_flow_draws=10, abs_fresh_draws=True)
    tr.ckpt_rungs = 2
    tr.ckpt_ladder = T.ladder_signature(_Ladder(abs_flow_draws=10))
    note = T.reset_best_if_ladder_changed(tr)
    assert "flow ensemble draws fixed -> fresh" in note
    assert tr.best_abs == NO_BEST and tr.best_hold == NO_BEST

    # And back the other way, which is the resume that would otherwise inherit
    # a record earned against a moving target as a bar on a fixed one.
    back = _Ladder(abs_flow_draws=10)
    back.ckpt_rungs = 2
    back.ckpt_ladder = T.ladder_signature(
        _Ladder(abs_flow_draws=10, abs_fresh_draws=True))
    assert "fresh -> fixed" in T.reset_best_if_ladder_changed(back)


def test_recentring_a_fresh_family_still_retires_the_record():
    """The levels are not in the signature under `fresh`, so the family has to
    be -- `--abs-flow-scale 800:1800` is the same change to a drawn yardstick
    that it is to a fixed one, and "K 10 -> 10" would read as no change."""
    tr = _Ladder(abs_flow_draws=10, abs_fresh_draws=True,
                 abs_flow_scale=(800, 1800))
    tr.ckpt_rungs = 2
    tr.ckpt_ladder = T.ladder_signature(
        _Ladder(abs_flow_draws=10, abs_fresh_draws=True))
    note = T.reset_best_if_ladder_changed(tr)
    assert "flow ensemble family" in note and tr.best_abs == NO_BEST

    same = _Ladder(abs_flow_draws=10, abs_fresh_draws=True)
    same.ckpt_rungs = 2
    same.ckpt_ladder = T.ladder_signature(
        _Ladder(abs_flow_draws=10, abs_fresh_draws=True))
    assert T.reset_best_if_ladder_changed(same) is None


# ------------------------------------------------------- the round trip

def test_the_reject_count_round_trips(tmp_path):
    """(4) A resume that restarted the counter at zero would make the flag look
    free on the second segment of every long run -- the count of refused
    candidates is exactly the evidence that it is not."""
    a = Trainer(Config(**dict(_CFG, best_replicate=2)), seed=3)
    a.replicate_rejects = 7
    a.best_abs, a.best_hold = 133_162.0, 129_222.0
    a.best_abs_theta = a.theta + 1.0
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(**dict(_CFG, best_replicate=2)), seed=9)
    T.load_resume(b, str(tmp_path))
    assert b.replicate_rejects == 7
    assert b.best_abs == 133_162.0 and b.best_hold == 129_222.0

    # A checkpoint written before the field refused nothing, which is what 0
    # says -- and a fresh trainer starts there too.
    d = dict(np.load(os.path.join(str(tmp_path), "state.npz"), allow_pickle=False))
    del d["replicate_rejects"]
    np.savez(os.path.join(str(tmp_path), "state.npz"), **d)
    c = Trainer(Config(**_CFG), seed=9)
    c.replicate_rejects = 4
    T.load_resume(c, str(tmp_path))
    assert c.replicate_rejects == 0
    assert Trainer(Config(**_CFG), seed=1).replicate_rejects == 0


def test_a_resumed_run_re_draws_the_levels_it_would_have_drawn(tmp_path):
    """Fresh draws are state-free by construction -- they are a function of the
    generation -- so a resume measures at the same levels the killed process
    would have measured at, with nothing extra in the checkpoint."""
    a = Trainer(Config(**dict(_CFG, abs_flow_draws=4, abs_fresh_draws=True)),
                seed=3)
    a.generation()
    T.save_state(str(tmp_path), a, gen=1)
    a.generation()

    b = Trainer(Config(**dict(_CFG, abs_flow_draws=4, abs_fresh_draws=True)),
                seed=999)
    T.load_resume(b, str(tmp_path))
    b.generation()
    assert a.t == b.t
    assert a.measurement_draws() == b.measurement_draws()
    assert a.measurement_draws(1) == b.measurement_draws(1)
    assert np.array_equal(np.asarray(a.replicate_words(1)),
                          np.asarray(b.replicate_words(1)))
