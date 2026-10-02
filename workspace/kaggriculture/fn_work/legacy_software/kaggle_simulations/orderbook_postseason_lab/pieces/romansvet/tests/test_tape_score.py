"""`--tape-score ours`: read a tape rung on our coins, not on a phantom margin.

A `--tape-rung` opponent is a planner archetype plus one recorded Kaggle seat's
market flow, and that flow is **exogenous**: `sim.market.apply_flow` credits the
seat with 25-48k a tape for products its board never grows. Calibrated against
the real engine on 2026-09-04 over the randomised flow family, the rung ranks
small theta changes 5/6 the way the engine does on *our* coins and 3/6 -- a coin
flip -- on the opponent's, and its margin objective is offset from the engine's
by a per-tape 4k to 41k. The cheapest fix is to stop reading the flow seat's
column on those rungs, which is what the flag does.

What is pinned here:

* the default (`margin`) is the objective that came before the flag, to the
  byte, on a ladder that *has* a tape rung -- `tape_episodes` hands
  `shaped_advantage` the `None` it defaults to;
* under `ours` a tape rung's contribution moves with our coins and is *exactly*
  invariant to the flow seat's, while an archetype rung on the same ladder
  keeps the margin term it always had;
* the mask marks both seats of every tape pair and nothing else;
* the yardstick's `score` column -- what `--select-metric score` promotes on --
  reads the same way, while the `mine` / `theirs` columns stay as measured;
* the signature carries the flag, so a resume across the switch retires the
  record it inherited rather than pretending it is a bar in the same units.
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
import train as T

from kagg3.es.train import (NO_BEST, TAPE_SCORES, Config, Trainer,
                            own_coin_score, shaped_advantage)

#: The ladder every test below runs on: one archetype, one tape rung appended
#: after it -- the shape `--tape-rung` actually produces.
NAMES = ["greedy_farmer", "tape_103254816"]
ARCH, TAPE = 0, 1
#: The tape's registered table id. Nothing here reads the table itself; what
#: matters is that `tape_slots` says slot 1 is a tape.
TABLE = 5

#: Four candidates x six episodes: three seed pairs, both seats of each. Pair 1
#: plays the tape rung and pairs 0 and 2 the archetype (`IDX`), so columns 2 and
#: 3 are the ones the flag is about. Four rather than two because the objective
#: is *rank* normalised: with two candidates every reordering is the same
#: reordering, and a fixture that coarse cannot tell an invariance from a tie.
MINE = 1e3 * np.array([[130., 128, 100, 102, 126, 124],
                       [128., 130, 118, 116, 124, 126],
                       [126., 124,  96,  98, 130, 132],
                       [124., 126, 122, 120, 132, 130]])
#: The flow seat is the rich one: it banks 90-160k on the tape columns off a
#: `TAPE_PLANNER` board that grows almost none of it.
THEIRS = 1e3 * np.array([[120., 140, 152, 106, 142, 142],
                         [156., 108, 160,  90, 176, 136],
                         [ 92., 136, 106, 148, 140, 102],
                         [126., 144, 134, 122, 146,  98]])
#: The largest per-tape offset the 2026-09-04 calibration measured between the
#: rung's margin and the engine's.
OFFSET = 41_000.0
#: Which rung each of the three pairs faces. `opponent_slots` indexes into
#: `pool + archetypes + [theta]` and the pool is empty here, so these are rung
#: indices already.
IDX = np.array([ARCH, TAPE, ARCH])


def _tr(tape_score="margin", tapes=((TAPE, TABLE),), **cfg):
    """A `Trainer` carrying only what the objective reads.

    `__new__` rather than a real construction, for `test_tape_rung`'s reason:
    what is under test is which column of `money` a rung's episodes are scored
    on, and building a ladder would spend a minute of archetype probing on it.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(tape_score=tape_score, **cfg)
    tr.pool = []
    tr.tape_slots = tuple(tapes)
    return tr


def _mask(tr, idx=IDX):
    return tr.tape_episodes(len(idx), idx)


# ------------------------------------------------------------- the defaults

def test_the_flag_defaults_to_the_objective_that_came_before_it():
    assert Config().tape_score == "margin"
    assert TAPE_SCORES == ("margin", "ours")


def test_a_tape_ladder_under_margin_is_the_objective_head_computed():
    """(1) Inert until asked for: no mask, and the same floats as the 3-arg call."""
    tr = _tr("margin")
    assert _mask(tr) is None, "the default must not build a mask at all"

    got = shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS), tr.cfg,
                           _mask(tr))
    head = shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS), tr.cfg)
    assert np.array_equal(np.asarray(got), np.asarray(head))


def test_a_run_with_no_tape_rung_never_builds_a_mask_either():
    """`ours` on a ladder of archetypes is the ladder's own objective."""
    tr = _tr("ours", tapes=())
    assert _mask(tr) is None


def test_the_config_value_is_refused_at_construction():
    with pytest.raises(ValueError, match="tape_score 'theirs'"):
        Trainer(Config(tape_score="theirs", n_archetypes=0, pop=2, episodes=2))


# ------------------------------------------------------------------ the mask

def test_the_mask_marks_both_seats_of_every_tape_pair():
    m = np.asarray(_mask(_tr("ours")))
    assert m.shape == (2 * len(IDX),)
    assert list(m) == [False, False, True, True, False, False]


# ------------------------------------------------------------- the objective

def _blend(mine, theirs, cfg, tape):
    """The fitness, written out: HEAD's terms with `own_coin_score` on `tape`."""
    from kagg3.es.train import rank_normalise

    rel = 1.0 / (1.0 + np.exp(-(mine - theirs) / cfg.margin_scale))
    rel = np.where(tape, own_coin_score(mine, cfg, np), rel).mean(axis=1)
    own = np.log1p(np.maximum(mine, 0.0)).mean(axis=1)
    return (cfg.abs_weight * np.asarray(rank_normalise(jnp.asarray(own)))
            + (1.0 - cfg.abs_weight) * np.asarray(rank_normalise(jnp.asarray(rel))))


def test_ours_ignores_the_flow_seats_coins_on_the_tape_rung():
    """(2a) Exactly invariant to `theirs` there -- the phantom column is gone."""
    tr = _tr("ours")
    mask = _mask(tr)
    base = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS),
                                       tr.cfg, mask))

    # The flow seat is credited another 41k it never grew, on the tape columns.
    moved = THEIRS.copy()
    moved[:, 2:4] += OFFSET
    same = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(moved),
                                       tr.cfg, mask))
    assert np.array_equal(base, same)

    # And the same move *does* reorder the objective the flag replaces, so the
    # invariance above is the flag's doing and not an inert fixture.
    head = _tr("margin").cfg
    a = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS), head))
    b = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(moved), head))
    assert not np.array_equal(a, b)


def test_ours_still_moves_with_our_coins_on_the_tape_rung():
    """(2b) It is a *score*, not a mute: our column still ranks the candidates."""
    tr = _tr("ours")
    mask = _mask(tr)
    base = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS),
                                       tr.cfg, mask))
    assert base.argmin() == 2, "candidate 2 earns the least on the fixture"

    richer = MINE.copy()
    richer[2, 2:4] += 60_000.0        # candidate 2 earns more against the tape
    got = np.asarray(shaped_advantage(jnp.asarray(richer), jnp.asarray(THEIRS),
                                      tr.cfg, mask))
    assert got.argmax() == 2, "our coins on a tape rung have to be able to lead"


def test_the_archetype_rung_keeps_the_margin_term_it_always_had():
    """(2c) Only the tape episodes move: every other column is HEAD's."""
    tr = _tr("ours")
    mask = np.asarray(_mask(tr))
    got = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(THEIRS),
                                      tr.cfg, jnp.asarray(mask)))
    assert got == pytest.approx(_blend(MINE, THEIRS, tr.cfg, mask), abs=1e-6)

    # The archetype's opponent column is still read: move it by the same 41k
    # the tape column ignored and the objective reorders.
    moved = THEIRS.copy()
    moved[:, 4:6] += OFFSET
    other = np.asarray(shaped_advantage(jnp.asarray(MINE), jnp.asarray(moved),
                                        tr.cfg, jnp.asarray(mask)))
    assert not np.array_equal(got, other)


def test_the_own_coin_term_is_the_anchors_squash_on_the_margins_scale():
    """`sigmoid(log1p(mine) - log1p(scale))`, i.e. `(1+m) / (2+m+scale)`."""
    cfg = Config()
    m = np.array([0.0, 50e3, 100e3, 300e3])
    want = (1.0 + m) / (2.0 + m + cfg.margin_scale)
    assert own_coin_score(m, cfg, np) == pytest.approx(want)
    # Bounded like the margin term it stands in for, 0.5 at `margin_scale`, and
    # still sloping at 300k where `sigmoid(m / scale)` reads 0.95.
    assert own_coin_score(np.array([cfg.margin_scale]), cfg, np)[0] == \
        pytest.approx(0.5, abs=1e-5)
    assert 0.7 < float(own_coin_score(np.array([300e3]), cfg, np)[0]) < 0.8
    # The two array modules are one function.
    assert np.asarray(own_coin_score(jnp.asarray(m), cfg)) == \
        pytest.approx(want, rel=1e-6)


# -------------------------------------------------------------- the yardstick

PAIRS = 4


def _ev_for(arch, tape):
    """A stand-in evaluator: `(mine, theirs)` by rung, so the fixture is exact.

    `theta_o[0]` identifies the rung -- `_abs` stacks each rung's theta as its
    own index -- and nothing else varies, so a per-rung column is readable
    straight off the report.
    """
    def ev(tables, theta_c, theta_o, words, seat, nquad, money, flow=None):
        o = np.asarray(theta_o)[:, 0].astype(np.int64)
        mine = np.where(o == TAPE, tape[0], arch[0]).astype(np.float64)
        theirs = np.where(o == TAPE, tape[1], arch[1]).astype(np.float64)
        return np.stack([mine, theirs], axis=1)
    return ev


def _abs(tape_score, arch=(120e3, 100e3), tape=(90e3, 140e3), **cfg):
    """The absolute report on that stand-in ladder. -> AbsReport"""
    tr = _tr(tape_score, abs_pairs=PAIRS, **cfg)
    tr.tables = None
    tr.theta = np.zeros(3)
    tr.n = 3
    tr.archetype_names = list(NAMES)
    tr.archetypes = [np.full(3, float(i)) for i in range(len(NAMES))]
    tr.archetype_coins = []
    tr.rung_weights = np.ones(len(NAMES))
    tr.arch_handicap = np.zeros((len(NAMES), 2), np.int32)
    tr.holdout_thetas = []
    tr.flow_rung = tr.kaggle_rung = -1
    tr.abs_words = np.arange(PAIRS, dtype=np.float64).reshape(PAIRS, 1, 1)
    tr.n_abs_sel = max(PAIRS // 2, 1)
    tr.abs_draws = ()
    tr.evaluate = _ev_for(arch, tape)
    return tr.absolute_report(tr.theta)


def test_the_yardstick_scores_a_tape_rung_on_our_coins_too():
    """(3) `--select-metric score` reads the rung the gradient reads."""
    cfg = Config()
    head, ours = _abs("margin"), _abs("ours")
    arch = 1.0 / (1.0 + np.exp(-(120e3 - 100e3) / cfg.margin_scale))

    assert head.score == pytest.approx(
        np.mean([arch, 1.0 / (1.0 + np.exp(-(90e3 - 140e3) / cfg.margin_scale))]))
    assert ours.score == pytest.approx(
        np.mean([arch, float(own_coin_score(np.array([90e3]), cfg, np)[0])]))

    # The coin columns are the diagnostic and stay as measured, both rungs.
    assert head.mine == ours.mine == (120e3, 90e3)
    assert head.theirs == ours.theirs == (100e3, 140e3)


def test_the_yardsticks_tape_column_ignores_the_flow_seat():
    """Move the flow seat 41k: `margin` follows it, `ours` does not."""
    a = _abs("ours", tape=(90e3, 140e3))
    b = _abs("ours", tape=(90e3, 99e3))
    assert a.score == pytest.approx(b.score)
    assert a.holdout_score == pytest.approx(b.holdout_score)

    c = _abs("margin", tape=(90e3, 140e3))
    d = _abs("margin", tape=(90e3, 99e3))
    assert c.score != pytest.approx(d.score)


# --------------------------------------------------------------- the resume

class _Ladder:
    """The fields `ladder_signature` and the reset rule read, as in
    `tests/test_abs_flow_ensemble.py`."""

    def __init__(self, **cfg):
        self.cfg = Config(**cfg)
        self.archetype_names = list(NAMES)
        self.rung_weights = np.ones(len(NAMES))
        self.arch_handicap = np.zeros((len(NAMES), 2), np.int32)
        self.theta = np.zeros(3)
        self.best_abs, self.best_abs_theta = 133_000.0, np.ones(3)
        self.best_hold, self.champion_score = 130_000.0, 133_000.0


def test_the_signature_retires_a_record_earned_under_the_other_rule():
    assert T.ladder_signature(_Ladder())["tape_score"] == "margin"
    assert T.ladder_signature(_Ladder(tape_score="ours"))["tape_score"] == "ours"

    tr = _Ladder(tape_score="ours")
    tr.ckpt_rungs, tr.ckpt_ladder = len(NAMES), T.ladder_signature(_Ladder())
    note = T.reset_best_if_ladder_changed(tr)
    assert "tape score margin -> ours" in note
    assert tr.best_abs == NO_BEST and tr.best_hold == NO_BEST


def test_a_checkpoint_written_before_the_field_still_resumes():
    """The zero-diff half: an older signature and an unflagged run compare equal."""
    old = T.ladder_signature(_Ladder())
    old.pop("tape_score")
    tr = _Ladder()
    tr.ckpt_rungs, tr.ckpt_ladder = len(NAMES), old
    assert T.reset_best_if_ladder_changed(tr) is None
    assert tr.best_abs == 133_000.0
