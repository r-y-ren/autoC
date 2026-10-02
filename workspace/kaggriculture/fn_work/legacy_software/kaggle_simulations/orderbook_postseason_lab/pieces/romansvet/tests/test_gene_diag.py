"""The forward-admit gene on the gen line.

The gene (`g11`/`gb11`, decoded in `brain.decide` as `macro.forward_days`) was
dead in an earlier arm: the logistic it shipped with put it in a zone where no
perturbation at sigma 0.02 moved the horizon by a day, so the search had
nothing to select between and the block was 33 parameters of noise. The line
decode (`FWD_DAYS_GAIN`) was measured offline to wake it -- and "measured
offline" is exactly the kind of claim a live arm should not have to take on
trust.

So the trainer reports it. Two numbers, off the episodes the generation
already played and no rollout of their own:

* `fwd` -- the mean decoded horizon in days over (member, episode, day);
* `fwd>0` -- the fraction of *members* whose own mean is above zero.

The second is the one that says the gene is alive: a population where one
member decodes six days and 63 decode none has the same `fwd` as one where
every member sits at 0.09, and only the first is something a gradient can be
taken through. `/ctr` beside them is the centre theta's own horizon on the
fixed measurement boards, on the generations that take one.

The channel is `rollout.episode(day_tiles=True)`'s per-day rows -- the same
one `fill` and `rows/d` come down, widened by a column, so there is no second
trace path and no second decode.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import jax.numpy as jnp
import numpy as np
import pytest
import train as CLI

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO
from kagg3.es.train import Trainer, make_evaluator
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables

pytestmark = pytest.mark.skipif(not rollout.FWD_GENE,
                                reason="this layout carries no g11 block")

#: One fixed board, both seats playing the theta under test. The gene is a
#: property of the decode and not of the game, so one seed is a measurement and
#: not a sample.
SEED = 777_001


def _words(seed):
    return jnp.asarray(np.stack([eod.host_stream(int(seed), d)
                                 for d in range(spec.N_DAYS)]))


def _metrics(theta):
    """`(fwd, fwd>0)` for a one-member, one-episode population. -> (float, float)

    The very call `Trainer.generation` makes -- `make_evaluator(day_metrics=
    True)` then `Trainer.day_metric_means` -- with the population axis a
    singleton, so what is being read is the production path and not a
    re-implementation of it.
    """
    hi, lo = eod.weed_threshold()
    ev = make_evaluator(jnp.int32(hi), jnp.int32(lo), day_metrics=True)
    t = jnp.asarray(theta, jnp.float32)
    money = ev(build_tables(jnp), t[None], t[None], _words(SEED)[None],
               jnp.zeros(1, jnp.int32), jnp.ones((1, 2), jnp.int32),
               jnp.full((1, 2), spec.STARTING_MONEY, jnp.int32))
    assert money.shape[-1] == 12, "the gene's column is on the evaluator's row"
    out = Trainer.day_metric_means(money[None])
    assert len(out) == 6, "the four shaping means, then the gene's two"
    return out[4], out[5]


def _theta(**genes):
    """A zero theta with named scalar genes set. -> float32 [N_PARAMS]"""
    theta = np.zeros(PO.N_PARAMS, np.float32)
    for name, value in genes.items():
        theta[PO.offset(name)] = value
    return theta


class _Tr:
    """Just enough `Trainer` for the two reporting helpers."""

    def __init__(self, day_metrics, centre=None):
        self.last_day_metrics = day_metrics
        self.last_centre_fwd = centre


def test_a_zero_theta_reports_a_dead_gene():
    # `round(FWD_DAYS_GAIN * 0) = 0` is the whole inertness guarantee: every
    # theta written before the block is a prefix that decodes to a zero
    # horizon, and the diagnostic has to say so rather than round something up.
    fwd, frac = _metrics(_theta())
    assert fwd == 0.0
    assert frac == 0.0


def test_a_theta_that_decodes_a_horizon_reports_it():
    # `gb11 = 0.2` with `g11` still zero makes the pre-activation exactly 0.2
    # whatever the global head reads, so the horizon is
    # `floor(16 * 0.2 + 0.5) = 3` on every day of the season -- a number this
    # test can state, not merely a positive one.
    theta = _theta(gb11=0.2)
    assert int(brain.FWD_DAYS_GAIN * 0.2 + 0.5) == 3
    fwd, frac = _metrics(theta)
    assert fwd >= 1.0
    assert fwd == pytest.approx(3.0, abs=1e-3)
    assert frac == 1.0


def test_the_gen_line_and_the_log_carry_both_fields():
    tr = _Tr((-11_152.0, 44.81, 16.7, 6.6, 1.25, 0.25))
    line = CLI._fwd_line(tr)
    assert "  fwd 1.25" in line
    assert "  fwd>0 0.25" in line
    # The centre reading rides the same segment, and only on the generations
    # that measured one.
    assert "/ctr" not in line
    assert "/ctr 2.50" in CLI._fwd_line(_Tr(tr.last_day_metrics, 2.5))
    # `log.jsonl` carries all three as numbers.
    assert CLI._fwd_fields(_Tr(tr.last_day_metrics, 2.5)) == {
        "fwd_days": 1.25, "fwd_frac": 0.25, "fwd_days_centre": 2.5}
    # A stubbed evaluator (four means, no gene column) and a tree without the
    # block print nothing at all and log three nulls -- the gen line's older
    # columns are byte-identical there.
    assert CLI._fwd_line(_Tr((0.0, 0.0, 0.0, 0.0))) == ""
    assert CLI._fwd_line(_Tr(None)) == ""
    assert CLI._fwd_fields(_Tr(None)) == {
        "fwd_days": None, "fwd_frac": None, "fwd_days_centre": None}
    # ... and the segment is on the line the trainer actually prints.
    src = open(os.path.join(ROOT, "scripts", "train.py"), encoding="utf-8").read()
    assert "+ _fwd_line(tr)" in src
    assert "**_fwd_fields(tr)," in src
