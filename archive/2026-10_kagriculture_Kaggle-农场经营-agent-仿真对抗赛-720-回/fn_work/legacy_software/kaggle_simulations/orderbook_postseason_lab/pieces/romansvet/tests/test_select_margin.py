"""`--select-metric margin:<rung>`: promote on one rung's margin, not on coins.

A real-engine measurement across the five thetas ever scored against kagg2
(2026-08-27) is what this is for. The yardstick's rung-weighted coin total --
`--select-metric coins`, the rule every `best_abs.npy` on disk was written
under -- has **zero** rank correlation with the real margin against kagg2
(Spearman 0.00). The in-sim margin on the `kagg2_flow` rung alone ranks the
same five perfectly (Spearman +1.00, level bias under ~1.1k, slope ~0.6-0.8).
Every record both flow lineages promoted had earned more coins in-sim and lost
by more on the real engine: selection was reading the wrong half of the game.

Two things follow, and both are tested here:

* the metric has to be readable per rung, on **both** halves of the fixed seed
  set, or `--best-gate both` cannot ask its question about it;
* the "none yet" sentinel has to stop being `-1.0`. A margin is routinely
  negative -- the thetas above sit near -5,000 -- so a record starting at -1.0
  is a record no candidate can ever take, and the run would go its whole length
  never writing `best_abs.npy`.
"""
from __future__ import annotations

import math
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest
import train as T

from kagg3.es.train import NO_BEST, AbsReport, Config, Trainer
from kagg3.es import kagg2_flow as K2F

#: The ladder these tests talk about: two hand-set rungs and the flow rung, in
#: the order a real run holds them (the flow rung is an extra slot, appended).
NAMES = ["greedy_farmer", "mixed_ranch", K2F.RUNG_NAME]
#: The flag spelling an operator actually types.
MARGIN = f"margin:{K2F.RUNG_NAME}"


def _rep():
    """One measurement with a different story on every rung and every half.

    The flow rung is the interesting one: it *wins* the coin column (140k, the
    most of the three) while losing the margin (-5,000) -- which is exactly the
    shape the real-engine measurement found, and exactly what a coin-weighted
    selection cannot see.
    """
    return AbsReport(
        coins=130_000.0, win=0.5,
        mine=(120_000.0, 130_000.0, 140_000.0),
        theirs=(100_000.0, 90_000.0, 145_000.0),
        holdout=128_000.0, holdout_win=0.5,
        score=0.6, holdout_score=0.55,
        holdout_mine=(118_000.0, 129_000.0, 139_000.0),
        holdout_theirs=(101_000.0, 91_000.0, 141_000.0))


def _tr(metric, names=NAMES, **cfg):
    """A stand-in carrying only what the selection rules read."""
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric=metric, **cfg)
    tr.archetype_names = list(names)
    return tr


# ------------------------------------------------------- reading the margin

def test_selection_reads_the_named_rungs_margin_on_each_half():
    """(a) `own - theirs` on that rung, selection half and holdout half."""
    rep, tr = _rep(), _tr(MARGIN)
    assert tr.selection_score(rep) == 140_000.0 - 145_000.0
    assert tr.holdout_selection_score(rep) == 139_000.0 - 141_000.0

    # Not the coin total, not the weighted score, not another rung's margin.
    assert tr.selection_score(rep) == -5_000.0 != rep.coins
    assert _tr("margin:mixed_ranch").selection_score(rep) == 40_000.0
    assert _tr("margin:mixed_ranch").holdout_selection_score(rep) == 38_000.0


def test_the_other_two_metrics_are_untouched():
    """Zero-diff: `coins` and `score` still read the headlines they always did."""
    rep = _rep()
    assert _tr("coins").selection_score(rep) == rep.coins
    assert _tr("coins").holdout_selection_score(rep) == rep.holdout
    assert _tr("score").selection_score(rep) == rep.score
    assert _tr("score").holdout_selection_score(rep) == rep.holdout_score


def test_the_coin_floor_still_guards_a_margin_selection():
    """`--select-coin-floor` reads `rep.coins` whatever ranks the candidates.

    It is the guard against buying margin by burning the market down, which is
    precisely the failure a *margin* metric can be walked into, so it has to
    survive the change -- a blocked candidate is `None` and can take nothing.
    """
    rep, tr = _rep(), _tr(MARGIN, select_coin_floor=140_000.0)
    assert tr.selection_score(rep) is None
    assert _tr(MARGIN, select_coin_floor=100_000.0).selection_score(rep) == -5_000.0


def test_a_report_with_no_holdout_half_reads_zero_rather_than_raising():
    """`abs_pairs=2` leaves no holdout seeds; `holdout` reports 0.0 there and
    the per-rung twin has to agree instead of indexing off the end."""
    thin = _rep()._replace(holdout_mine=(), holdout_theirs=(), holdout=0.0)
    assert _tr(MARGIN).holdout_selection_score(thin) == 0.0


# ------------------------------------------------------ naming a real rung

def test_an_unknown_rung_raises_at_construction():
    """(b) The ladder is bound in `__init__`, before a single rollout, so a
    typo costs a second rather than `--abs-every` generations of a night run."""
    cfg = Config(pop=4, episodes=4, chunk=8, abs_pairs=2, n_archetypes=2,
                 holdout_rungs=False, select_metric="margin:no_such_rung")
    with pytest.raises(ValueError, match="names no such rung"):
        Trainer(cfg, seed=0)


def test_the_check_names_the_ladder_it_looked_in():
    tr = _tr(MARGIN, names=["greedy_farmer"])
    with pytest.raises(ValueError, match="greedy_farmer"):
        tr._check_select_rung(tr.archetype_names)
    with pytest.raises(ValueError, match="--kagg2-flow"):
        tr._check_select_rung(tr.archetype_names)


def test_a_pending_anchor_passes_construction_and_binds_later():
    """`--rung-theta` anchors are appended *after* the Trainer exists, so
    `margin:<anchor>` has to survive the construction that cannot see them yet.
    """
    tr = _tr("margin:route1", names=["greedy_farmer"])
    tr.pending_rungs = ("route1",)
    tr._check_select_rung(tr.archetype_names)        # no raise: it is coming
    tr.archetype_names.append("route1")
    assert tr.select_rung_index() == 1


def test_a_bare_prefix_and_an_unknown_metric_both_report_the_valid_forms():
    rep = _rep()
    with pytest.raises(ValueError, match="needs a rung name"):
        _tr("margin:").selection_score(rep)
    with pytest.raises(ValueError, match="margin:<rung>"):
        _tr("marjin:kagg2_flow").selection_score(rep)
    with pytest.raises(ValueError, match="'coins', 'score'"):
        _tr("winrate").selection_score(rep)


# ---------------------------------------------------- the negative sentinel

def _record(best_abs=NO_BEST, best_hold=NO_BEST, **kw):
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric=MARGIN, **kw)
    tr.best_abs, tr.best_hold = best_abs, best_hold
    return tr


def test_a_negative_first_record_is_taken_and_a_less_negative_one_replaces_it():
    """(c) The whole point of `NO_BEST` being `-inf`.

    Under the old `-1.0` sentinel the first line here is `False` -- a policy
    that loses kagg2 by 5,000 is "worse than no record at all" -- and the run
    never writes `best_abs.npy` at all.
    """
    tr = _record()
    assert tr._accept_best(-5_000.0, -5_200.0) is True
    tr.best_abs, tr.best_hold = -5_000.0, -5_200.0

    assert tr._accept_best(-4_000.0, -4_500.0) is True   # less negative is better
    assert tr._accept_best(-6_000.0, -1_000.0) is False  # more negative is not
    assert tr._accept_best(-5_000.0, 0.0) is False       # a tie is not a record


def test_the_holdout_gate_works_in_negative_numbers_too():
    both = _record(best_abs=-5_000.0, best_hold=-5_200.0, best_gate="both")
    assert both._accept_best(-4_000.0, -5_100.0) is True    # both improved
    assert both._accept_best(-4_000.0, -9_000.0) is False   # sel up, hold down
    # And the first record of a `both` run is not gated against the sentinel.
    assert _record(best_gate="both")._accept_best(-9_000.0, -9_000.0) is True


def test_the_champion_follows_the_same_negative_record():
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric=MARGIN)
    tr.archetype_names, tr.champion_score = list(NAMES), NO_BEST
    tr.champion, tr.theta, tr.history, tr.t = "init", "candidate", [], 25
    tr._measure_champion(_rep())
    assert tr.champion == "candidate" and tr.champion_score == -5_000.0


def test_the_sentinel_is_logged_as_null_rather_than_as_a_number():
    """`-inf` is not JSON, and `-1.0` is a margin a real policy can post."""
    assert T._num(NO_BEST, 1) is None
    assert T._num(None, 6) is None
    assert T._num(-5_000.123, 1) == -5_000.1
    assert T._num(0.0, 1) == 0.0


def test_the_sentinel_round_trips_through_state_npz(tmp_path):
    """`np.float64(-inf)` survives `savez`; a pre-2026-08-27 `-1.0` is read
    forward to it, or a checkpoint that stopped before its first measurement
    would resume holding a record of minus one coin."""
    a = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, abs_pairs=2,
                       holdout_rungs=False), seed=3)
    assert a.best_abs == NO_BEST and a.champion_score == NO_BEST
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, abs_pairs=2,
                       holdout_rungs=False), seed=9)
    T.load_resume(b, str(tmp_path))
    assert b.best_abs == NO_BEST and not math.isfinite(b.champion_score)

    d = dict(np.load(str(tmp_path / "state.npz")))
    d["best_abs"], d["champion_score"] = np.float64(-1.0), np.float64(-1.0)
    np.savez(str(tmp_path / "state.npz"), **d)
    c = Trainer(Config(pop=4, episodes=2, chunk=8, n_archetypes=0, abs_pairs=2,
                       holdout_rungs=False), seed=9)
    T.load_resume(c, str(tmp_path))
    assert c.best_abs == NO_BEST and c.champion_score == NO_BEST


# --------------------------------------------------- resume across a metric

class _Ladder:
    """The fields `ladder_signature` and the reset rule read. Same stand-in
    idea as `tests/test_resume_roundtrip.py`, kept local so this file states
    its own preconditions."""

    def __init__(self, metric="coins", names=("a", "b")):
        self.cfg = Config(select_metric=metric)
        self.archetype_names = list(names)
        self.rung_weights = np.ones(len(names))
        self.arch_handicap = np.zeros((len(names), 2), np.int32)
        self.theta = np.zeros(3)
        self.best_abs, self.best_abs_theta = 150_646.0, np.ones(3)
        self.best_hold, self.champion_score = 149_000.0, 150_646.0


def test_changing_the_select_metric_on_resume_drops_the_inherited_best():
    """(d) A coin total is not a bar a margin run can clear -- it is a bar it
    can never clear, and the run would go its whole length never writing
    `best_abs.npy`. The signature carries the metric so the existing reset
    path fires, and says which of the two changed."""
    tr = _Ladder(metric=MARGIN)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, T.ladder_signature(_Ladder(metric="coins"))
    note = T.reset_best_if_ladder_changed(tr)
    assert f"select metric coins -> {MARGIN}" in note
    assert "150,646.0" in note
    assert tr.best_abs == NO_BEST and tr.best_hold == NO_BEST
    # The champion selects on the very same rule, so it goes with the record
    # rather than sitting in `champion.npy` as an unbeatable coin total.
    assert tr.champion_score == NO_BEST
    assert np.array_equal(tr.best_abs_theta, tr.theta)


def test_the_same_metric_and_the_same_ladder_still_carry_the_best():
    """Zero-diff: adding a field to the signature must not reset every resume."""
    tr = _Ladder(metric=MARGIN)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, T.ladder_signature(_Ladder(metric=MARGIN))
    assert T.reset_best_if_ladder_changed(tr) is None
    assert tr.best_abs == 150_646.0


def test_a_signature_written_before_the_field_is_read_as_coins():
    """Every checkpoint on disk predates this field and every one of them was
    measured on coins, so that -- not "whatever this run selects on" -- is what
    a missing `select` means. Assuming the current metric instead would make
    the change invisible on exactly the checkpoints that need it caught."""
    assert T._read_signature({"names": [], "weights": [], "handicap": []}) \
        ["select"] == "coins"

    old = T.ladder_signature(_Ladder(metric="coins"))
    del old["select"]
    tr = _Ladder(metric=MARGIN)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, old
    assert "select metric coins -> " in T.reset_best_if_ladder_changed(tr)


def test_a_checkpoint_predating_the_signature_entirely_is_reset_by_the_metric():
    """The rung-count fallback used to be the whole test. A same-count ladder
    is still trusted -- but only for a run that selects on coins, which is what
    such a checkpoint was measured on."""
    same = _Ladder(metric="coins")
    same.ckpt_rungs, same.ckpt_ladder = 2, None
    assert T.reset_best_if_ladder_changed(same) is None

    moved = _Ladder(metric=MARGIN)
    moved.ckpt_rungs, moved.ckpt_ladder = 2, None
    note = T.reset_best_if_ladder_changed(moved)
    assert "predates the ladder signature" in note and MARGIN in note
    assert moved.best_abs == NO_BEST


def test_reset_best_still_forces_it_on_an_unchanged_ladder_and_metric():
    tr = _Ladder(metric=MARGIN)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, T.ladder_signature(_Ladder(metric=MARGIN))
    note = T.reset_best_if_ladder_changed(tr, force=True)
    assert "--reset-best" in note and tr.best_abs == NO_BEST


def test_from_best_refuses_a_checkpoint_whose_record_is_the_sentinel():
    """`--from-best` used to test `best_abs < 0`, which under a margin metric
    is most of a healthy run."""
    tr = _Ladder(metric=MARGIN)
    tr.best_abs, tr.n = -5_000.0, 3
    tr.m = tr.v = np.ones(3)
    tr.best_abs_theta, tr.sigma, tr.t = np.full(3, 7.0), 0.02, 41
    assert "-5,000.0" in T.jump_to_best(tr, "run")     # a negative best is a best
    assert np.array_equal(np.asarray(tr.theta), np.full(3, 7.0))

    tr.best_abs = NO_BEST
    with pytest.raises(SystemExit, match="no best_abs_theta yet"):
        T.jump_to_best(tr, "run")
