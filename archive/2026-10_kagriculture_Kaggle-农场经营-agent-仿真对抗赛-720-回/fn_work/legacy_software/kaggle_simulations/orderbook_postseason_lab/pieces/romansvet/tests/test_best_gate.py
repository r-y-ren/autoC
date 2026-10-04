"""`best_abs` is a max over a noisy sequence, so the record it keeps is a lucky
reading of it.

The absolute measurement splits 64 fixed seed pairs in half: the first selects,
the second is only reported. Taking the max over the selection half alone means
the record is biased upward by whatever the luckiest draw of the run was worth.
Measured on flow2: the record at gen 2230 read 133,162 sel against 129,222 hold
-- a -3,940 gap, where an ordinary reading nearby was -1,033. That ~3k is seed
luck, and `best_abs.npy` -- what `--promote` ships -- is the theta that got it.

`--best-gate both` refuses a record whose holdout half fell, and `--best-margin`
makes the record cost something to take. Both default to the old rule, and the
first test here is that an unflagged run is the run that came before them.
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

_CFG = {"pop": 4, "episodes": 2, "chunk": 8, "n_archetypes": 0,
        "abs_pairs": 2, "holdout_rungs": False}


def _rep(coins, hold, score=0.0, holdout_score=0.0):
    """A stub measurement: only the four numbers the gate reads are real."""
    return AbsReport(coins=coins, win=0.0, mine=(), theirs=(), holdout=hold,
                     holdout_win=0.0, score=score, holdout_score=holdout_score)


def _gate(best_abs=100_000.0, best_hold=-math.inf, **kw):
    """A stand-in carrying just the record, so the *rule* is tested on its own."""
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**kw)
    tr.best_abs, tr.best_hold = best_abs, best_hold
    return tr


# ------------------------------------------------------------- the old rule

def test_the_default_gate_is_exactly_strictly_greater_on_the_selection_half():
    """Zero-diff: `sel` mode with no margin must accept a reading iff it beats
    the record, whatever the holdout did. The hold-down case is the one
    `--best-gate both` exists to refuse, and it has to be *accepted* here or
    every checkpoint written so far was written under a different rule.
    """
    tr = _gate(best_abs=100_000.0, best_hold=99_000.0)
    for sel, hold in [(100_001.0, 1.0),        # up on sel, hold collapsed
                      (133_162.0, 129_222.0),  # the flow2 record itself
                      (100_000.0, 500_000.0),  # a tie is not an improvement
                      (99_999.0, 500_000.0)]:
        assert tr._accept_best(sel, hold) == (sel > tr.best_abs)

    # And a candidate `select_coin_floor` blocked outright never takes it.
    assert tr._accept_best(None, 500_000.0) is False


def test_the_config_defaults_are_the_old_behaviour():
    cfg = Config()
    assert cfg.best_gate == "sel" and cfg.best_margin == 0.0


def test_an_unknown_gate_is_refused_rather_than_silently_sel():
    tr = _gate(best_gate="hold")
    with pytest.raises(ValueError, match="expected 'sel' or 'both'"):
        tr._accept_best(200_000.0, 200_000.0)


# --------------------------------------------------------------- `both`

def test_both_refuses_a_record_whose_holdout_half_fell():
    """The lucky-seed signature: sel up, hold down. Flat or up is a real gain."""
    tr = _gate(best_abs=129_000.0, best_hold=129_222.0, best_gate="both")

    assert tr._accept_best(133_162.0, 129_221.0) is False   # hold down by 1
    assert tr._accept_best(133_162.0, 129_222.0) is True    # hold flat
    assert tr._accept_best(133_162.0, 130_000.0) is True    # hold up
    # Still a max on the selection half: a holdout gain alone is not a record.
    assert tr._accept_best(128_999.0, 500_000.0) is False


def test_the_first_record_of_a_run_is_not_gated_against_a_sentinel():
    """`best_hold` starts at -inf, so `both` cannot refuse the first reading --
    there is nothing yet for it to have generalised worse than."""
    tr = _gate(best_abs=NO_BEST, best_gate="both")
    assert tr._accept_best(0.0, 0.0) is True


def test_both_reads_the_holdout_of_whichever_metric_selects():
    """`--select-metric score` selects on a bounded score, so the half that
    checks it has to be the holdout *score* -- a coin count does not answer
    whether a score improvement generalised."""
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric="score")
    assert tr.holdout_selection_score(_rep(1.0, 2.0, 0.6, 0.55)) == 0.55
    tr.cfg = Config()
    assert tr.holdout_selection_score(_rep(1.0, 2.0, 0.6, 0.55)) == 2.0


# --------------------------------------------------------------- the margin

def test_the_margin_refuses_an_improvement_that_only_half_clears_it():
    tr = _gate(best_abs=100_000.0, best_hold=90_000.0, best_margin=2_000.0)

    assert tr._accept_best(101_000.0, 95_000.0) is False   # +margin/2
    assert tr._accept_best(102_000.0, 95_000.0) is False   # exactly +margin
    assert tr._accept_best(102_001.0, 95_000.0) is True

    # It applies in `both` too, and the two conditions are independent: the
    # margin refuses the first of these even though the holdout rose, and the
    # holdout refuses the last even though the margin was cleared.
    tr.cfg = tr.cfg._replace(best_gate="both")
    assert tr._accept_best(101_000.0, 95_000.0) is False
    assert tr._accept_best(102_001.0, 95_000.0) is True
    assert tr._accept_best(102_001.0, 89_999.0) is False


# ------------------------------------------------------------- the wiring

def _stub_gen(tr, readings):
    """Drive `generation()` over a scripted sequence of measurements."""
    it = iter(readings)
    tr.absolute_report = lambda theta, **_: _rep(*next(it))
    for _ in readings:
        tr.generation()


def test_generation_records_the_holdout_of_the_theta_it_kept():
    """End to end through `generation`: `both` keeps the first reading, refuses
    the lucky one, and `best_hold` tracks the record's own holdout rather than
    the best holdout ever seen."""
    tr = Trainer(Config(**dict(_CFG, abs_every=1, champ_every=100,
                               best_gate="both")), seed=0)
    _stub_gen(tr, [(100_000.0, 99_000.0),      # first: taken
                   (133_162.0, 90_000.0),      # sel up, hold down: refused
                   (110_000.0, 99_000.0)])     # sel up, hold flat: taken

    assert tr.best_abs == 110_000.0 and tr.best_hold == 99_000.0
    assert tr.last_best_gate == {"sel": 110_000.0, "hold": 99_000.0,
                                 "accepted": True}
    assert tr.last_improve == tr.t

    # The same sequence under the default gate keeps the lucky reading, which
    # is the behaviour this flag was added to be able to turn off.
    sel = Trainer(Config(**dict(_CFG, abs_every=1, champ_every=100)), seed=0)
    _stub_gen(sel, [(100_000.0, 99_000.0), (133_162.0, 90_000.0),
                    (110_000.0, 99_000.0)])
    assert sel.best_abs == 133_162.0 and sel.best_hold == 90_000.0


# ------------------------------------------------------------- the round trip

def test_best_hold_round_trips_and_old_checkpoints_fall_back(tmp_path):
    """`best_hold` is half of one claim -- "this theta scored this" -- so it has
    to come back with `best_abs`, or a resumed `both` run gates its next record
    against a fresh `-inf` and waves it through.
    """
    a = Trainer(Config(**_CFG), seed=3)
    a.best_abs, a.best_hold = 133_162.0, 129_222.0
    a.best_abs_theta = a.theta + 1.0
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(**_CFG), seed=9)
    T.load_resume(b, str(tmp_path))
    assert (b.best_abs, b.best_hold) == (133_162.0, 129_222.0)
    assert np.array_equal(np.asarray(b.best_abs_theta), np.asarray(a.best_abs_theta))

    # Every state.npz written before the gate existed has no `best_hold`. -inf
    # is the honest "not measured": the first record of the resumed run is
    # taken on its selection number alone, as the run that wrote it would have,
    # and every record after that is gated against a real holdout.
    d = dict(np.load(str(tmp_path / "state.npz")))
    del d["best_hold"]
    np.savez(str(tmp_path / "state.npz"), **d)

    c = Trainer(Config(**_CFG), seed=9)
    T.load_resume(c, str(tmp_path))
    assert c.best_abs == 133_162.0 and c.best_hold == -math.inf

    # A ladder change drops the record, and the holdout is part of the record:
    # it was earned against the yardstick that just went away.
    c.ckpt_rungs, c.ckpt_ladder = 2, None       # a 2-rung checkpoint, 0 here
    c.best_hold = 129_222.0
    assert T.reset_best_if_ladder_changed(c) is not None
    assert c.best_abs == NO_BEST and c.best_hold == NO_BEST
