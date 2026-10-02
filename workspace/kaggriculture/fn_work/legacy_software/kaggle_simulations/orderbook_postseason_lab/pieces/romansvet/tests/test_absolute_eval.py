"""`mean_win` and `champ` used to be ladder-relative and sat near 0.5 by
construction. This is the number that says whether the policy is getting
*better*: coins against a fixed set of opponents on fixed seeds -- and since
2026-08-25 it is also what selects the champion and what `--promote` ships.

Three things that follow and are pinned here. The measurement reports both
sides per archetype, because a mean alone cannot separate "earned more" from
"the opponent collapsed". The fixed seeds are split, because selecting on 64
fixed games invites fitting those 64 and a held-out half is the only way to
see it. And selection reads coins, not the win bit: over the 13 h run that
motivated the change, the ladder rule correlated -0.17 with absolute strength.

Since 2026-08-26 the report also carries the **weighted expected tournament
score** and the *opponent* holdout, and selection can be pointed at either
number. Both are pinned here at both settings, because the whole claim of that
change is that an unflagged run is the run that came before it: `score` rides
in the same batch coins do and costs no extra rollout, `select_coin_floor`
refuses a candidate outright rather than merely ranking it lower, and the
held-out rungs never reach `candidates()` or any number selection reads.
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

import jax.numpy as jnp
import numpy as np
import pytest

from kagg3.es import archetypes as A
from kagg3.es.train import AbsReport, Config, Trainer


def _tiny(**kw):
    # `holdout_rungs` off unless a test asks for it: two more rungs is a second
    # input shape for the jitted evaluator, and a second shape is a second XLA
    # compile in a file that builds a Trainer per test.
    return Config(pop=4, episodes=4, chunk=8,
                  **dict({"abs_pairs": 2, "holdout_rungs": False}, **kw))


def _rep(coins, win=0.0, score=0.0):
    return AbsReport(coins=coins, win=win, mine=(), theirs=(), holdout=0.0,
                     holdout_win=0.0, score=score)


def test_absolute_eval_is_deterministic_for_a_theta():
    tr = Trainer(_tiny(n_archetypes=2), seed=0)
    a = tr.absolute_eval(tr.theta)
    b = tr.absolute_eval(tr.theta)
    assert a == b
    assert isinstance(a[0], float) and 0.0 <= a[1] <= 1.0


def test_absolute_eval_needs_archetypes():
    tr = Trainer(_tiny(n_archetypes=0), seed=0)
    coins, win = tr.absolute_eval(tr.theta)
    assert coins == 0.0 and win == 0.0
    rep = tr.absolute_report(tr.theta)
    assert rep.mine == () and rep.theirs == () and rep.holdout == 0.0


def test_the_report_decomposes_the_yardstick_per_archetype_and_both_sides():
    tr = Trainer(_tiny(n_archetypes=3), seed=0)
    rep = tr.absolute_report(tr.theta)
    assert len(rep.mine) == len(rep.theirs) == 3
    # The headline number is the mean of the per-archetype own-coin means; the
    # rungs are played equally often, so the two cannot disagree.
    assert rep.coins == pytest.approx(float(np.mean(rep.mine)), rel=1e-6)
    # The opponents are hand-set strategies, so they earn what the probe said
    # they earn, whatever the candidate does.
    assert min(rep.theirs) > 0.0


def test_the_holdout_half_is_a_different_set_of_games():
    tr = Trainer(_tiny(n_archetypes=2, abs_pairs=8), seed=0)
    assert tr.n_abs_sel == 4
    rep = tr.absolute_report(tr.theta)
    # Same policy, same opponents, different seeds: a real number, and not the
    # selection number by construction (that would mean the split did nothing).
    assert rep.holdout > 0.0
    assert rep.holdout != rep.coins
    assert 0.0 <= rep.holdout_win <= 1.0


def test_generation_measures_on_schedule_and_tracks_the_best():
    tr = Trainer(_tiny(n_archetypes=2, abs_every=2, champ_every=100), seed=0)
    r1 = tr.generation()
    assert r1[2] is None and r1[3] is None
    r2 = tr.generation()
    assert isinstance(r2[2], float) and isinstance(r2[3], AbsReport)
    assert tr.abs_history and tr.abs_history[-1][0] == tr.t
    assert tr.best_abs == r2[2]
    assert np.asarray(tr.best_abs_theta).shape == np.asarray(tr.theta).shape


def test_a_champion_measurement_also_counts_as_an_absolute_measurement():
    """One evaluation serves both schedules; only `abs` is gated on `abs_every`.

    The yardstick is fixed, so there is nothing to gain by playing it twice in
    the same generation -- but a measurement taken for the champion is still a
    measurement, and `best_abs` would be wrong to ignore it.
    """
    tr = Trainer(_tiny(n_archetypes=2, abs_every=100, champ_every=1), seed=0)
    _, _, abs_coins, rep = tr.generation()
    assert abs_coins is None                      # abs_every did not fire
    assert isinstance(rep, AbsReport)             # champ_every did
    assert tr.best_abs == rep.coins
    assert tr.champion_score == rep.coins


def test_champion_selection_reads_coins_not_the_win_bit():
    tr = Trainer.__new__(Trainer)
    tr.cfg, tr.history, tr.t = Config(), [], 10
    tr.champion, tr.champion_score, tr.theta = "init", -1.0, "rich"

    tr._measure_champion(_rep(300_000.0, win=0.0))
    assert tr.champion == "rich" and tr.champion_score == 300_000.0

    # Wins every game against the ladder and earns half as much. The old rule
    # would have promoted it.
    tr.theta = "poor"
    tr._measure_champion(_rep(150_000.0, win=1.0))
    assert tr.champion == "rich" and tr.champion_score == 300_000.0
    assert [h[0] for h in tr.history] == [10, 10]


# ------------------------------------------------------- score and the floor

def test_the_score_is_the_weighted_mean_of_the_per_rung_sigmoids():
    """`score` rides in the same batch coins do, at the same rung weights.

    It is the objective `GOAL.md` states -- expected tournament score, W in
    {0, 0.5, 1}, softened to keep a gradient -- and the yardstick has to report
    it at the mixture the gradient consumes or the two describe different
    ladders.
    """
    tr = Trainer(_tiny(n_archetypes=3, margin_scale=50_000.0,
                       rung_weight=(("rusher", 3.0),)), seed=0)
    margins = np.array([+50_000.0, -25_000.0, 0.0])

    def canned(tables, cand, opp, words, seat, nq, mo):
        i = np.arange(cand.shape[0]) % 3
        return jnp.stack([jnp.full(cand.shape[0], 80_000.0),
                          jnp.asarray(80_000.0 - margins[i])], axis=1)

    tr.evaluate = canned
    rep = tr.absolute_report(tr.theta)

    per = 1.0 / (1.0 + np.exp(-margins / 50_000.0))
    w = np.array([1.0, 3.0, 1.0])
    assert rep.score == pytest.approx(float(np.average(per, weights=w)))
    assert rep.holdout_score == pytest.approx(rep.score)      # same canned games
    assert rep.weights == (1.0, 3.0, 1.0)
    # A win rate cannot separate these three; the score can.
    assert rep.wins == (1.0, 0.0, 0.5)
    # And with the rungs switched off there is no opponent holdout at all.
    assert tr.holdout_thetas == [] and rep.holdout_rungs == ()


def test_selection_reads_coins_by_default_and_the_score_on_the_flag():
    tr = Trainer.__new__(Trainer)

    tr.cfg = Config()
    assert tr.selection_score(_rep(120_000.0, score=0.3)) == 120_000.0

    tr.cfg = Config(select_metric="score")
    assert tr.selection_score(_rep(120_000.0, score=0.3)) == 0.3


def test_the_coin_floor_blocks_a_high_score_low_coin_candidate():
    """The guard against the mutual-destruction optimum.

    A denial policy reaches a high score on a low absolute -- the diagnosis's
    own S6 scenario tops the coin ratio at 72k of its own coins, *below* what
    the scenarios that farm reach -- and in a Bradley-Terry field a 72k policy
    loses to every third agent farming 130k in a quiet game. `None` means "not
    selectable at all", so the incumbent stands rather than being replaced by
    a candidate the floor merely scores lower.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric="score", select_coin_floor=80_000.0)

    assert tr.selection_score(_rep(72_000.0, score=0.95)) is None
    assert tr.selection_score(_rep(80_000.0, score=0.40)) == 0.40
    # And with the floor off (the default) nothing is ever refused.
    tr.cfg = Config(select_metric="score")
    assert tr.selection_score(_rep(1.0, score=0.95)) == 0.95


def test_a_blocked_candidate_cannot_take_best_abs_or_the_champion():
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric="score", select_coin_floor=80_000.0)
    tr.history, tr.t = [], 10
    tr.champion, tr.champion_score, tr.theta = "incumbent", 0.4, "denial"

    tr._measure_champion(_rep(50_000.0, score=0.99))

    assert tr.champion == "incumbent" and tr.champion_score == 0.4


def test_generation_tracks_best_abs_on_the_selected_metric():
    """End to end: with `select_metric score`, `best_abs` holds a score.

    The field keeps its name in `state.npz` so `--resume` stays compatible, and
    `log.jsonl` carries `sel_metric` so a tracker row can say which of the two
    numbers it is looking at.
    """
    tr = Trainer(_tiny(n_archetypes=2, abs_every=1, champ_every=100,
                       select_metric="score"), seed=0)
    _, _, abs_coins, rep = tr.generation()

    assert 0.0 <= tr.best_abs <= 1.0
    assert tr.best_abs == rep.score
    assert abs_coins == rep.coins and rep.coins > 1.0     # `abs` stays coins
    assert np.array_equal(np.asarray(tr.best_abs_theta), np.asarray(tr.theta))


def test_an_unknown_select_metric_is_refused_rather_than_silently_coins():
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric="margin")
    with pytest.raises(ValueError, match="expected 'coins', 'score' or 'margin:<rung>'"):
        tr.selection_score(_rep(1.0))


# ------------------------------------------------------- the opponent holdout

def test_the_held_out_rungs_are_reported_and_never_faced():
    """The holdout this run did not have: on *opponents*, not on seeds.

    The seed holdout tracks the selection half to a mean 1.1% over 30
    checkpoints -- it is working perfectly and answering a question nobody is
    asking. What a handicapped rung can be overfitted to is the handicap, and
    only a rung nothing trains on can say so.
    """
    tr = Trainer(_tiny(n_archetypes=2, holdout_rungs=True), seed=0)
    labels = [h[0] for h in tr.holdout_thetas]
    assert labels == [r[0] for r in A.HOLDOUT_RUNGS]

    # Never an opponent: not in the gradient's candidate list, and not in the
    # archetype set the yardstick's own mean is taken over.
    cands = [np.asarray(c) for c in tr.candidates()]
    for _, theta, _ in tr.holdout_thetas:
        assert not any(np.array_equal(np.asarray(theta), c) for c in cands)
    assert len(tr.archetypes) == 2

    rep = tr.absolute_report(tr.theta)
    assert len(rep.mine) == len(rep.theirs) == 2          # the trained rungs only
    assert [r[0] for r in rep.holdout_rungs] == labels
    for _, own, theirs, margin, win in rep.holdout_rungs:
        assert own > 0.0 and theirs > 0.0
        assert margin == pytest.approx(own - theirs)
        assert 0.0 <= win <= 1.0


def _stalled(**kw):
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**kw)
    tr.n = 3
    tr.sigma, tr.sigma_restarts = 0.02, 0
    tr.best_abs, tr.best_abs_theta = 100.0, jnp.ones(3)
    tr.theta = jnp.zeros(3)
    tr.m, tr.v = jnp.ones(3), jnp.ones(3)
    tr.last_improve, tr.t = 0, 40
    return tr


def test_restart_on_stall_doubles_sigma_once_from_the_best_theta():
    tr = _stalled(restart_stall=25)
    tr._maybe_restart()
    assert tr.sigma == 0.04 and tr.sigma_restarts == 1
    assert np.array_equal(np.asarray(tr.theta), np.ones(3))
    # The moments describe the basin just left; carried across they would spend
    # the next generations undoing the jump.
    assert not np.any(np.asarray(tr.m)) and not np.any(np.asarray(tr.v))
    # Once only, and the stall clock restarts with it.
    assert tr.last_improve == 40
    tr.t = 200
    tr._maybe_restart()
    assert tr.sigma == 0.04 and tr.sigma_restarts == 1


def test_a_stalled_run_restarts_through_generation():
    """The wiring, not just the rule: `generation` must call it on a flat report.

    With no archetypes the yardstick is a constant 0, so the first measurement
    sets `best_abs` and every one after it is a non-improvement -- a stall by
    construction, and the cheapest way to drive the branch end to end.
    """
    tr = Trainer(_tiny(n_archetypes=0, abs_every=1, champ_every=100, restart_stall=1), seed=0)
    tr.generation()
    assert (tr.best_abs, tr.last_improve, tr.sigma) == (0.0, 1, 0.02)
    gen1_theta = np.asarray(tr.best_abs_theta)

    tr.generation()

    assert tr.sigma == 0.04 and tr.sigma_restarts == 1
    assert np.array_equal(np.asarray(tr.theta), gen1_theta)
    assert not np.any(np.asarray(tr.m)) and not np.any(np.asarray(tr.v))


def test_restart_is_off_by_default_and_before_the_stall_window():
    off = _stalled()
    assert off.cfg.restart_stall == 0
    off._maybe_restart()
    assert off.sigma == 0.02 and off.sigma_restarts == 0

    early = _stalled(restart_stall=100)
    early._maybe_restart()
    assert early.sigma == 0.02 and np.array_equal(np.asarray(early.theta), np.zeros(3))
