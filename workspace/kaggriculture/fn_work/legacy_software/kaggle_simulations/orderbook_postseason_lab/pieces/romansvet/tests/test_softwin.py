"""`--select-metric softwin:<rung>:<tau>`: a win rate the record can climb.

`margin:<rung>` promotes the mean of (own - theirs), which is unbounded on
both sides: one blowout pair can carry a reading that lost every other game,
and a field of thirty agents scores that reading as a *loss*. `softwin` reads
the same rung through `tanh(margin / tau)` -- a smooth win rate in [-1, +1] --
so a game already won by 30k cannot pay for a game lost by 1k, while a tanh
rather than a step still leaves a slope for the record to climb.

The mean of a tanh is not the tanh of a mean, so this number cannot be
rebuilt from `AbsReport.mine` / `.theirs`: it has to be reduced where the
per-game array still exists. That is the thing worth testing, and the tests
below drive the real `absolute_report` through a stub evaluator whose margins
are a table written out in full, so "which games went into the mean" is
arithmetic rather than statistics.
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

from kagg3.es.train import (
    AbsReport,
    Config,
    Trainer,
    select_spec,
)

#: A two-rung ladder, no flow rung: this file is about the reduction, not
#: about which levels of the flow family a measurement plays.
NAMES = ["greedy_farmer", "mixed_ranch"]
PAIRS = 4           # fixed seed pairs; the first two select, the last two hold
TAU = 3000.0
SOFTWIN = f"softwin:{NAMES[1]}:{TAU:.0f}"
MARGIN = f"margin:{NAMES[1]}"

#: `own - theirs` for every game the stub plays, as [rung][pair][seat].
#:
#: Rung 0 is the shape the metric exists for: two blowout wins and two small
#: losses on the selection half, which a *margin* reads as a comfortable
#: +14,500 and a win rate reads as a coin flip. Rung 1 -- the one the metric
#: names -- loses its selection half narrowly and wins its holdout half, so
#: the two halves cannot be confused with each other.
GAPS = np.array([
    [[+30_000, +30_000], [-1_000, -1_000],      # rung 0, selection pairs
     [+500, +500], [+500, +500]],               # rung 0, holdout pairs
    [[-2_000, -4_000], [+1_000, -3_000],        # rung 1, selection pairs
     [+6_000, +2_000], [+3_000, +9_000]],       # rung 1, holdout pairs
], dtype=np.float64)


def _ev(tables, theta_c, theta_o, words, seat, nquad, money, flow=None):
    """A stand-in evaluator: the margin is `GAPS[rung, pair, seat]`, exactly.

    The rung comes back out of the opponent theta, the pair out of the seed
    word and the seat out of `seat`, so a measurement handed the wrong games
    reads a different table entry rather than a slightly different number.
    """
    o = np.asarray(theta_o)[:, 0].astype(np.int64)
    w = np.asarray(words).reshape(o.shape[0], -1)[:, 0].astype(np.int64)
    s = np.asarray(seat).astype(np.int64)
    theirs = np.full(o.shape, 100_000.0)
    return np.stack([theirs + GAPS[o, w, s], theirs], axis=1)


def _stub(metric, **cfg):
    """A `Trainer` carrying only what `absolute_report` reads.

    `__new__` rather than a real construction, for the reason
    `tests/test_abs_replicate.py` gives: building the real ladder would spend
    a minute probing archetypes to answer a question about arithmetic.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**dict({"select_metric": metric, "abs_pairs": PAIRS},
                           **cfg))
    tr.tables = None
    tr.t = 25
    tr.theta = np.zeros(3)
    tr.n = 3
    tr.archetype_names = list(NAMES)
    # `full(3, i)`, so the evaluator above can read the rung index straight
    # back off the opponent theta.
    tr.archetypes = [np.full(3, float(i)) for i in range(len(NAMES))]
    tr.archetype_coins = []
    tr.rung_weights = np.ones(len(NAMES))
    tr.arch_handicap = np.zeros((len(NAMES), 2), np.int32)
    tr.holdout_thetas = []
    tr.flow_rung = -1
    tr.abs_words = np.arange(PAIRS, dtype=np.float64).reshape(PAIRS, 1, 1)
    tr.n_abs_sel = PAIRS // 2
    tr._check_abs_select()
    tr.abs_draws = ()
    tr.evaluate = _ev
    return tr


def _mean_tanh(rung, pairs):
    """The number the report should carry, computed the long way round."""
    return sum(math.tanh(GAPS[rung, p, s] / TAU)
               for p in pairs for s in (0, 1)) / (2 * len(pairs))


# --------------------------------------------------------- parsing the spec

def test_the_spec_parses_every_form_of_select_metric():
    """One parser for the grammar, so the dozen readers cannot disagree."""
    assert select_spec("coins") == ("coins", None, None)
    assert select_spec("score") == ("score", None, None)
    assert select_spec("margin:kagg2_flow") == ("margin", "kagg2_flow", None)
    assert select_spec("softwin:kagg2_flow:3000") == \
        ("softwin", "kagg2_flow", 3000.0)
    # The tau is a float, not an int, and the rung keeps its underscores.
    assert select_spec("softwin:greedy_farmer:2.5e3").tau == 2500.0


def test_a_missing_or_non_positive_tau_is_refused_with_the_form_spelled_out():
    """A tau of 0 divides by zero and a negative one flips the sign of the
    whole metric, so both are typos rather than settings. Refused where the
    string is parsed, which is where `scripts/train.py` refuses it too --
    before the run builds anything, not `--abs-every` generations in."""
    for bad in ("softwin:kagg2_flow", "softwin:", "softwin::3000"):
        with pytest.raises(ValueError, match="needs a rung name and a tau"):
            select_spec(bad)
    with pytest.raises(ValueError, match="not a number"):
        select_spec("softwin:kagg2_flow:wide")
    for bad in ("softwin:kagg2_flow:0", "softwin:kagg2_flow:-3000"):
        with pytest.raises(ValueError, match="must be positive"):
            select_spec(bad)
    # And the unknown metric still names every valid form, including this one.
    with pytest.raises(ValueError, match="softwin:<rung>:<tau>"):
        select_spec("winrate")


# ------------------------------------------------------- reading the number

def test_the_report_carries_the_mean_tanh_of_the_games_own_margins():
    """Per rung and per half, off the same games the coin means are read on --
    and *not* a tanh of the coin means, which is the whole point."""
    rep = _stub(SOFTWIN).absolute_report(np.zeros(3))
    assert rep.softwin == pytest.approx(
        (_mean_tanh(0, (0, 1)), _mean_tanh(1, (0, 1))))
    assert rep.holdout_softwin == pytest.approx(
        (_mean_tanh(0, (2, 3)), _mean_tanh(1, (2, 3))))

    # Rung 0's selection half: two 30k wins and two 1k losses. The margin
    # calls that +14,500 (a tanh of 1.000); the soft win rate calls it 0.34,
    # which is the reading a field of opponents would agree with.
    assert rep.mine[0] - rep.theirs[0] == pytest.approx(14_500.0)
    assert rep.softwin[0] == pytest.approx(0.3392, abs=1e-4)
    assert rep.softwin[0] != pytest.approx(
        math.tanh((rep.mine[0] - rep.theirs[0]) / TAU), abs=0.5)


def test_selection_and_the_holdout_twin_both_read_the_named_rungs_column():
    """`best_abs` and the `--best-gate both` half read the same quantity --
    an improvement measured in a soft win rate is not answered by coins."""
    tr = _stub(SOFTWIN)
    rep = tr.absolute_report(np.zeros(3))
    assert tr.selection_score(rep) == rep.softwin[1]
    assert tr.holdout_selection_score(rep) == rep.holdout_softwin[1]
    # The named rung, not the other one and not a headline.
    assert tr.selection_score(rep) != pytest.approx(rep.softwin[0])
    assert tr.selection_score(rep) < 0 < rep.coins

    # A report with no holdout half (too few `abs_pairs`) reads 0.0, which is
    # the rule `margin:` and the coin headline already follow.
    thin = rep._replace(holdout_softwin=())
    assert tr.holdout_selection_score(thin) == 0.0

    # A report measured under another metric has no column to read, and
    # falling back to the margin would select on a different quantity
    # entirely. It is an error, not a silent substitution.
    with pytest.raises(ValueError, match="no softwin column"):
        tr.selection_score(rep._replace(softwin=()))


# ------------------------------------------------------------- the zero diff

def test_the_margin_path_measures_and_selects_exactly_what_it_did_before():
    """(zero diff) Same games, same numbers, and the two new columns empty:
    a run that does not ask for a soft win rate does not pay for one."""
    margin = _stub(MARGIN).absolute_report(np.zeros(3))
    coins = _stub("coins").absolute_report(np.zeros(3))
    assert margin == coins                       # the metric moved nothing
    assert margin.softwin == () and margin.holdout_softwin == ()

    tr = _stub(MARGIN)
    assert tr.selection_score(margin) == margin.mine[1] - margin.theirs[1]
    assert tr.holdout_selection_score(margin) == \
        margin.holdout_mine[1] - margin.holdout_theirs[1]
    assert tr.selection_score(margin) == pytest.approx(-2_000.0)

    # And the softwin run plays the identical games: every field of the two
    # reports agrees except the columns the new metric adds.
    soft = _stub(SOFTWIN).absolute_report(np.zeros(3))
    assert soft._replace(softwin=(), holdout_softwin=()) == margin


def test_an_unknown_rung_is_refused_the_same_way_the_margin_form_is():
    """The rung lookup is shared, so `softwin:` inherits the check that costs
    a second at startup instead of `--abs-every` generations of a night run."""
    tr = _stub(f"softwin:no_such_rung:{TAU:.0f}")
    with pytest.raises(ValueError, match="names no such rung"):
        tr._check_select_rung(tr.archetype_names)
    with pytest.raises(ValueError, match="no_such_rung"):
        tr.select_rung_index()
    assert _stub(SOFTWIN).select_rung_index() == 1


def test_a_hand_built_report_reads_the_column_without_a_measurement():
    """The selectors read `AbsReport`, not the evaluator: a tracker or a
    scoreboard can hand them a report of its own."""
    rep = AbsReport(coins=130_000.0, win=0.5,
                    mine=(120_000.0, 140_000.0),
                    theirs=(100_000.0, 145_000.0),
                    holdout=128_000.0, holdout_win=0.5,
                    softwin=(0.8, -0.25), holdout_softwin=(0.7, -0.4))
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(select_metric=SOFTWIN)
    tr.archetype_names = list(NAMES)
    assert tr.selection_score(rep) == -0.25
    assert tr.holdout_selection_score(rep) == -0.4
    # The coin floor still guards it: a soft win rate bought by burning the
    # market down is refused for the same reason a margin is.
    tr.cfg = Config(select_metric=SOFTWIN, select_coin_floor=140_000.0)
    assert tr.selection_score(rep) is None
