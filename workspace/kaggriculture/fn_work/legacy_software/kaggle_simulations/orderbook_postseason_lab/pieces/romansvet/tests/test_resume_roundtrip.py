"""A checkpoint must be the *whole* trainer state.

`--resume` on a multi-hour run has to continue the exact trajectory the
crashed process was on: the same theta, the same Adam moments, the same
ladder -- and the same *host* random stream. The numpy generator draws the
episode seeds, the warm starts and the market jitter, so a checkpoint that
leaves it out replays the seeds of generations 1..k after every resume and
the common-random-numbers scheme quietly loses its between-generation
resampling.

Checked the strong way: train k gens, checkpoint, train one more; a fresh
Trainer restored from that checkpoint and trained one more must land on the
byte-identical theta.
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

from kagg3.core import policy as PO
from kagg3.es import archetypes as A
from kagg3.es.train import NO_BEST, Config, Trainer

_CFG = {"pop": 4, "episodes": 2, "chunk": 8, "n_archetypes": 0, "warm_frac": 0.5}


def test_resume_continues_the_exact_trajectory(tmp_path):
    a = Trainer(Config(**_CFG), seed=3)
    a.generation(); a.generation()
    T.save_state(str(tmp_path), a, gen=2, elapsed=12.5)
    a.generation()

    b = Trainer(Config(**_CFG), seed=999)  # a different seed: nothing may leak from init
    gen, how, elapsed = T.load_resume(b, str(tmp_path))
    assert (gen, how, elapsed) == (2, "state.npz", 12.5)
    assert b.t == 2
    b.generation()

    assert np.array_equal(np.asarray(a.theta), np.asarray(b.theta))
    assert np.array_equal(np.asarray(a.m), np.asarray(b.m))
    assert a.rng.bit_generator.state == b.rng.bit_generator.state


def test_resume_carries_a_sigma_restart_without_pinning_the_flag(tmp_path):
    """`--restart-sigma-on-stall` doubles sigma once. A resume that dropped that
    would put the run straight back in the basin it climbed out of -- but a
    resume that restored the *absolute* sigma would silently ignore an operator
    who deliberately resumes with a bigger one. The restart count is what
    carries; the flag still sets the base.
    """
    a = Trainer(Config(**_CFG), seed=3)
    # A checkpoint that took one *stepping* restart: `sigma_steps` is what the
    # resume raises the multiplier to, and at the default 2.0 the two counters
    # move together (they part only at `--stall-sigma-mult 1.0`).
    a.sigma, a.sigma_restarts, a.sigma_steps, a.last_improve = 0.04, 1, 1, 7
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(**_CFG), seed=3)
    T.load_resume(b, str(tmp_path))
    assert (b.sigma, b.sigma_restarts, b.last_improve) == (0.04, 1, 7)

    c = Trainer(Config(**dict(_CFG, sigma=0.05)), seed=3)
    T.load_resume(c, str(tmp_path))
    assert c.sigma == 0.1


def test_the_ladder_s_names_round_trip_so_the_flags_land_on_the_right_rung(tmp_path):
    """`--rung-weight` and `--proxy-handicap` are stated by *name*.

    A resume restores the archetype **thetas** from the checkpoint, not from
    `--n-archetypes`, so without the names coming back with them a weighted
    resume would weight "rung 3" and not `mixed_ranch`, and the handicap would
    land on whichever slot happened to be ninth. The flags of the new
    invocation still win -- that is the rule `--sigma` already follows -- so it
    is the names that have to be stable, not the weights.
    """
    cfg = dict(_CFG, n_archetypes=len(A.NAMES), holdout_rungs=False, abs_pairs=4,
               rung_weight=(("rusher", 4.0), (A.PROXY_NAME, 3.0)),
               proxy_handicap=A.PROXY_HANDICAP, select_metric="score",
               select_coin_floor=1_000.0, collapse_floor=A.COLLAPSE_KEEP)
    a = Trainer(Config(**cfg), seed=3)
    assert a.archetype_names == list(A.NAMES)
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(**cfg), seed=3)
    T.load_resume(b, str(tmp_path))

    assert b.archetype_names == a.archetype_names
    want = [4.0 if n == "rusher" else 3.0 if n == A.PROXY_NAME else 1.0
            for n in A.NAMES]
    assert b.rung_weights.tolist() == want
    assert b.cfg.select_metric == "score"
    assert b.cfg.select_coin_floor == 1_000.0
    assert b.cfg.collapse_floor == A.COLLAPSE_KEEP
    # The handicap goes back on the proxy slot and on no other.
    i = b.archetype_names.index(A.PROXY_NAME)
    assert tuple(b.arch_handicap[i]) == A.PROXY_HANDICAP
    assert [tuple(h) for j, h in enumerate(b.arch_handicap) if j != i] \
        == [A.NO_HANDICAP] * (len(A.NAMES) - 1)
    # And the probe that gates the restored set played the handicapped game:
    # the two rungs share a theta, so a cold probe would have tied them.
    coins = dict(zip(b.archetype_names, b.archetype_coins))
    assert coins[A.PROXY_NAME] > coins["mixed_ranch"]
    assert coins[A.PROXY_NAME] == a.archetype_coins[i]


def test_a_checkpoint_without_names_falls_back_to_the_count(tmp_path):
    """Every `state.npz` written before 2026-08-26 has no `archetype_names`.

    Those runs are unweighted by construction (the flags did not exist), so
    there is nothing to *mis*-apply -- but a later resume of one has to decide
    what its rungs are called, and the only evidence is how many there are.
    When the count matches this invocation's `--n-archetypes` the labels
    `Trainer.__init__` built are the checkpoint's own ladder (`AR.NAMES` only
    ever grew at the end), so they stand; when it does not, nothing positional
    can be trusted and `reprobe_archetypes` falls back to `rung{i}` -- which is
    what then refuses a named weight rather than landing it on the wrong rung.
    """
    cfg = dict(_CFG, n_archetypes=2, holdout_rungs=False, abs_pairs=4)
    a = Trainer(Config(**cfg), seed=3)
    T.save_state(str(tmp_path), a, gen=1)
    d = dict(np.load(str(tmp_path / "state.npz")))
    del d["archetype_names"]
    np.savez(str(tmp_path / "state.npz"), **d)

    b = Trainer(Config(**cfg), seed=3)
    T.load_resume(b, str(tmp_path))
    assert b.archetype_names == list(A.NAMES[:2])       # the count agrees
    assert b.weighted_slots() is None

    # A weight naming a rung outside that ladder is still refused, names or no
    # names -- `--n-archetypes 2` is a two-rung run whatever it resumed from.
    b.cfg = b.cfg._replace(rung_weight=((A.NAMES[5], 2.0),))
    with pytest.raises(ValueError, match="no such rung"):
        b._bind_rungs()

    # Count disagrees: this build says three rungs, the checkpoint holds two.
    # Nothing positional survives that, so every name goes.
    c = Trainer(Config(**dict(cfg, n_archetypes=3)), seed=3)
    T.load_resume(c, str(tmp_path))
    assert len(c.archetypes) == 2
    assert c.archetype_names == ["rung0", "rung1"]
    c.cfg = c.cfg._replace(rung_weight=(("rusher", 2.0),))
    with pytest.raises(ValueError, match="no such rung"):
        c._bind_rungs()


#: Every parameter-indexed array a `state.npz` holds. All of them have to move
#: to the current layout together or the trainer resumes inconsistent.
PARAM_ARRAYS = ("theta", "champion", "m", "v", "best_abs_theta", "pool")


def _relayout(tmp_path, n):
    """Rewrite the checkpoint's parameter arrays to an `n`-parameter layout."""
    path = str(tmp_path / "state.npz")
    d = dict(np.load(path))
    for k in PARAM_ARRAYS:
        cur = d[k].shape[-1]
        d[k] = (d[k][..., :n] if n <= cur else
                np.concatenate([d[k], np.zeros(d[k].shape[:-1] + (n - cur,),
                                               d[k].dtype)], axis=-1))
    np.savez(path, **d)
    return d


def test_resume_zero_pads_a_checkpoint_written_under_an_older_layout(tmp_path):
    """New parameter blocks are only ever appended, so an older checkpoint is a
    prefix of the current layout and the missing tail is genes that did not
    exist when it was written. Refusing it -- which is what this used to do --
    throws away an opponent pool that takes hours to rebuild, for a tail that
    is exactly zero.

    4,386 is not a hypothetical: it is the layout every checkpoint on this
    machine was written under before the residual-drain block.
    """
    old_n = 4386
    a = Trainer(Config(**_CFG), seed=3)
    a.generation()
    T.save_state(str(tmp_path), a, gen=1)
    d = _relayout(tmp_path, old_n)

    b = Trainer(Config(**_CFG), seed=9)      # a different seed: nothing may leak
    gen, how, _ = T.load_resume(b, str(tmp_path))
    assert gen == 1 and f"zero-padded {old_n} -> {PO.N_PARAMS}" in how
    for name in ("theta", "champion", "m", "v", "best_abs_theta"):
        got = np.asarray(getattr(b, name))
        assert got.shape == (PO.N_PARAMS,), name
        assert np.array_equal(got[:old_n], d[name]), name
        assert not got[old_n:].any(), name
    assert all(np.asarray(x).shape == (PO.N_PARAMS,) for x in b.pool)
    # And it still trains: the padded coordinates are live, so they are
    # perturbed and updated like any other -- which is the whole point of
    # padding at load instead of at decode.
    b.generation()
    assert np.asarray(b.theta)[old_n:].any()


def test_resume_refuses_a_checkpoint_written_under_a_newer_layout(tmp_path):
    """The half of the old refusal that still stands: a longer theta carries a
    block this build has no decode for, and there is nothing safe to drop."""
    a = Trainer(Config(**_CFG), seed=3)
    T.save_state(str(tmp_path), a, gen=1)
    _relayout(tmp_path, PO.N_PARAMS + 8)
    b = Trainer(Config(**_CFG), seed=3)
    with pytest.raises(SystemExit, match="more than this build's"):
        T.load_resume(b, str(tmp_path))


def test_the_bare_npy_fallback_pads_too(tmp_path):
    """A run killed before its first `state.npz` leaves only the flat files, and
    those are the *oldest* checkpoints in the tree."""
    old_n = PO.N_PARAMS_LEGACY
    np.save(str(tmp_path / "theta.npy"), np.full(old_n, 0.5, np.float32))
    np.save(str(tmp_path / "pool.npy"), np.zeros((3, old_n), np.float32))
    b = Trainer(Config(**_CFG), seed=4)
    gen, how, _ = T.load_resume(b, str(tmp_path))
    assert gen == 0 and "legacy" in how
    assert np.asarray(b.theta).shape == (PO.N_PARAMS,)
    assert np.all(np.asarray(b.theta)[:old_n] == 0.5)
    assert not np.asarray(b.theta)[old_n:].any()
    assert [np.asarray(x).shape for x in b.pool] == [(PO.N_PARAMS,)] * 3


def test_legacy_resume_reports_no_elapsed(tmp_path):
    a = Trainer(Config(**_CFG), seed=3)
    np.save(str(tmp_path / "theta.npy"), np.asarray(a.theta))
    b = Trainer(Config(**_CFG), seed=4)
    gen, how, elapsed = T.load_resume(b, str(tmp_path))
    assert gen == 0 and elapsed == 0.0 and "legacy" in how
    assert np.array_equal(np.asarray(a.theta), np.asarray(b.theta))


#: `_CFG` has no ladder at all, and "the ladder did not change" is a claim about
#: rungs. Two hand-set rungs is the cheapest ladder that can actually change.
_LADDER = {**_CFG, "n_archetypes": 2, "abs_pairs": 2, "holdout_rungs": False}


def test_a_same_ladder_resume_keeps_best_abs(tmp_path):
    """The other half of the reset rule: an unchanged yardstick keeps its best.

    `best_abs` is what `--promote` ships and what `--restart-sigma-on-stall`
    jumps back onto, so dropping it on every resume would throw away the run's
    single best iterate every time the box reboots. It is dropped only when the
    ladder it was earned against is not the ladder ahead -- and a change of
    `--rung-weight` alone is such a change, because the weights are what the
    headline coin count is a mean over.
    """
    a = Trainer(Config(**_LADDER), seed=3)
    a.best_abs, a.best_abs_theta = 150_646.0, a.theta + 1.0
    T.save_state(str(tmp_path), a, gen=1)

    b = Trainer(Config(**_LADDER), seed=999)
    T.load_resume(b, str(tmp_path))
    assert b.best_abs == 150_646.0
    assert np.array_equal(np.asarray(b.best_abs_theta), np.asarray(a.best_abs_theta))
    assert getattr(b, "best_reset_note", None) is None

    # Same rungs, one of them weighted 3x: a different mean, so a different bar.
    c = Trainer(Config(**{**_LADDER, "rung_weight": ((A.NAMES[0], 3.0),)}), seed=999)
    T.load_resume(c, str(tmp_path))
    assert c.best_abs == NO_BEST
    assert "weights" in c.best_reset_note and A.NAMES[0] in c.best_reset_note

    # And the operator can force it on an unchanged ladder -- a planner change
    # moves every coin count without touching a rung name.
    d = Trainer(Config(**_LADDER), seed=999)
    T.load_resume(d, str(tmp_path))
    assert d.best_abs == 150_646.0
    note = T.reset_best_if_ladder_changed(d, force=True)
    assert d.best_abs == NO_BEST and "--reset-best" in note
    assert np.array_equal(np.asarray(d.best_abs_theta), np.asarray(d.theta))


class _Ladder:
    """The three fields `ladder_signature` reads plus the two `best_abs` ones.

    A stand-in rather than a `Trainer`, so the *rules* can be tested without
    building and probing an archetype set per case.
    """

    def __init__(self, names, weights=None, handicap=None, **cfg):
        # `ladder_signature` reads `--select-metric` off the config now: the
        # yardstick is the pair (what is measured, against what).
        self.cfg = Config(**cfg)
        self.archetype_names = list(names)
        self.rung_weights = np.array([1.0] * len(names) if weights is None
                                     else [float(w) for w in weights])
        self.arch_handicap = (np.zeros((len(names), 2), np.int32) if handicap is None
                              else np.asarray(handicap, np.int32))
        self.theta = np.zeros(3)
        self.best_abs, self.best_abs_theta = 150_646.0, np.ones(3)


def test_the_reset_rule_case_by_case():
    """Every branch of `reset_best_if_ladder_changed`, on a stand-in ladder."""
    sig = T.ladder_signature

    # A cold start is not a resume: nothing recorded, nothing reset.
    cold = _Ladder(["a", "b"])
    assert T.reset_best_if_ladder_changed(cold) is None
    assert cold.best_abs == 150_646.0

    # A checkpoint that carries a signature: compared field by field.
    same = _Ladder(["a", "b"])
    same.ckpt_rungs, same.ckpt_ladder = 2, sig(_Ladder(["a", "b"]))
    assert T.reset_best_if_ladder_changed(same) is None

    hcap = _Ladder(["a", "b"], handicap=[[1, 87_000], [0, 0]])
    hcap.ckpt_rungs, hcap.ckpt_ladder = 2, sig(_Ladder(["a", "b"]))
    assert "handicap" in T.reset_best_if_ladder_changed(hcap)
    assert hcap.best_abs == NO_BEST

    grew = _Ladder(["a", "b", "kagg2_flow"])
    grew.ckpt_rungs, grew.ckpt_ladder = 2, sig(_Ladder(["a", "b"]))
    assert "rungs +kagg2_flow" in T.reset_best_if_ladder_changed(grew)

    # A checkpoint written before the signature existed: the rung count is all
    # there is, and it is enough for every ladder that actually grew here.
    old_same = _Ladder(["a", "b"])
    old_same.ckpt_rungs, old_same.ckpt_ladder = 2, None
    assert T.reset_best_if_ladder_changed(old_same) is None
    assert old_same.best_abs == 150_646.0

    old_grew = _Ladder(["a", "b", "kagg2_flow"])
    old_grew.ckpt_rungs, old_grew.ckpt_ladder = 2, None
    note = T.reset_best_if_ladder_changed(old_grew)
    assert "predates the ladder signature" in note and "2 -> 3" in note
    assert old_grew.best_abs == NO_BEST


def test_from_best_jumps_theta_and_clears_only_the_moments(tmp_path):
    """`--from-best` is the jump half of a stall restart, on demand.

    Theta becomes the checkpoint's `best_abs_theta` *bit for bit* -- a jump to
    an approximation of the best iterate is not a jump to the best iterate --
    and the Adam moments go, because they describe the basin being left. Every
    other field is the trajectory and stays: the generation, sigma and its
    restart count, `best_abs` itself, and both RNGs. `adam_t` is not one of
    them -- it counts steps on the moments, so it is zeroed with them.
    """
    a = Trainer(Config(**_CFG), seed=3)
    a.generation(); a.generation()
    a.best_abs, a.best_abs_theta = 133_162.0, a.theta * 0.5 + 0.125
    a.generation()                       # theta moves off the best afterwards
    a.sigma, a.sigma_restarts, a.last_improve = 0.04, 1, 2
    T.save_state(str(tmp_path), a, gen=3, elapsed=99.0)

    b = Trainer(Config(**dict(_CFG, sigma=0.02, stall_sigma_mult=1.0)), seed=999)
    gen, _, elapsed = T.load_resume(b, str(tmp_path))
    b.m = b.m + 1.0                      # non-zero moments, so the clear shows
    b.v = b.v + 1.0
    rng_before = b.rng.bit_generator.state
    note = T.jump_to_best(b, str(tmp_path))

    assert np.array_equal(np.asarray(b.theta), np.asarray(a.best_abs_theta))
    assert not np.array_equal(np.asarray(b.theta), np.asarray(a.theta))
    assert not np.asarray(b.m).any() and not np.asarray(b.v).any()
    # The bias-correction counter is part of the clear: it is what makes the
    # correction correct for the zeros `m`/`v` now hold.
    assert b.adam_t == 0 and b.t == 3
    assert (gen, elapsed, b.t) == (3, 99.0, 3)
    assert (b.sigma, b.sigma_restarts, b.best_abs) == (0.02, 1, 133_162.0)
    assert b.rng.bit_generator.state == rng_before
    assert "133,162.0" in note

    # Nothing to jump to: refused by name rather than silently starting from
    # the init theta the sentinel is paired with.
    c = Trainer(Config(**_CFG), seed=3)
    c.best_abs = NO_BEST
    with pytest.raises(SystemExit, match="no best_abs_theta yet"):
        T.jump_to_best(c, str(tmp_path))


def test_from_best_still_jumps_when_this_run_s_yardstick_retires_the_record(tmp_path):
    """A yardstick change invalidates the number, not the iterate.

    `load_resume` runs `reset_best_if_ladder_changed` at its end, so by the
    time `main` reaches `--from-best` the record is already the sentinel on
    exactly the resumes that change the measurement -- adding a rung, or
    switching the flow rung to its ensemble. Refusing there would mean the one
    launch this is for (`--resume flow4 --from-best --abs-flow-draws 10`) could
    not start, so the retired theta is kept aside and the jump goes ahead.
    """
    a = Trainer(Config(**_CFG), seed=3)
    a.best_abs, a.best_abs_theta = 133_162.0, a.theta + 3.0
    T.save_state(str(tmp_path), a, gen=5)

    b = Trainer(Config(**dict(_CFG, abs_select="all")), seed=3)
    T.load_resume(b, str(tmp_path))
    assert b.best_abs == NO_BEST                 # the reset already fired
    note = T.jump_to_best(b, str(tmp_path))
    assert np.array_equal(np.asarray(b.theta), np.asarray(a.best_abs_theta))
    assert "133,162.0" in note and "retired" in note
    # The sentinel still pairs with "best_abs_theta is the current theta", so a
    # later `_maybe_restart` cannot land back on the iterate just left.
    assert np.array_equal(np.asarray(b.best_abs_theta), np.asarray(b.theta))

    # A checkpoint that never measured is still refused: there is no theta with
    # the label, only the init one the sentinel is paired with.
    c = Trainer(Config(**dict(_CFG, abs_select="all")), seed=3)
    T.load_resume(c, str(tmp_path))
    c.best_reset_from = NO_BEST
    with pytest.raises(SystemExit, match="no best_abs_theta yet"):
        T.jump_to_best(c, str(tmp_path))


def test_stall_restart_multiplier_is_a_flag_and_1_0_still_restarts():
    """`--stall-sigma-mult 1.0` keeps the step and takes only the jump.

    On this ladder the IPOP doubling is a collapse, not an escape -- 0.04 cost
    flow2 133k -> 98-118k abs -- so the multiplier has to be settable down to
    1.0, and at 1.0 the restart must still do the part that helps: theta back
    onto `best_abs_theta`, Adam cleared, the restart counted so it fires once.
    """
    for mult, want in ((1.0, 0.02), (2.0, 0.04), (1.5, 0.03)):
        tr = Trainer(Config(**dict(_CFG, sigma=0.02, restart_stall=5,
                                   stall_sigma_mult=mult)), seed=3)
        tr.best_abs_theta = tr.theta + 1.0
        tr.m, tr.v = tr.m + 1.0, tr.v + 1.0
        tr.t, tr.adam_t, tr.last_improve = 20, 20, 10
        before = np.asarray(tr.theta).copy()

        tr._maybe_restart()
        assert tr.sigma == pytest.approx(want)
        assert np.array_equal(np.asarray(tr.theta), before + 1.0)
        assert not np.asarray(tr.m).any() and not np.asarray(tr.v).any()
        assert tr.adam_t == 0 and tr.t == 20
        assert (tr.sigma_restarts, tr.last_improve) == (1, 20)

        # A second one is refused *while it would step the sigma up again* --
        # that is the run admitting it is over. At 1.0 there is no step-up to
        # run out of and the jump repeats; see the test below.
        tr.t = 40
        tr._maybe_restart()
        assert (tr.sigma, tr.sigma_restarts) == (pytest.approx(want),
                                                 2 if mult == 1.0 else 1)


def test_a_pure_jump_restart_may_fire_again_but_a_sigma_step_up_may_not():
    """At `--stall-sigma-mult 1.0` the restart *is* `--from-best`, on a timer.

    Nothing about "theta back onto `best_abs_theta`, Adam cleared" is
    single-use: it is the operation an operator performs by hand (stop, resume
    `--from-best`) whenever a run wanders below its own record, and a run that
    stalls twice wants it twice. What is single-use is the sigma step-up, which
    compounds -- `sigma * mult ** restarts` -- and at 2.0 reaches 0.08 by the
    third one, well past the 0.04 that cost flow2 a third of its abs.

    So the rule is attached to the sigma rather than to the counter, and the
    counter still has to earn each repeat: `last_improve` moves to `t` on every
    fire, so nothing happens again until a full `--restart-stall` has passed.
    """
    cfg = dict(_CFG, sigma=0.02, restart_stall=5, stall_sigma_mult=1.0)
    tr = Trainer(Config(**cfg), seed=3)
    tr.best_abs_theta = tr.theta + 1.0
    tr.t, tr.adam_t, tr.last_improve = 20, 20, 10

    tr._maybe_restart()
    assert (tr.sigma_restarts, tr.last_improve) == (1, 20)

    # Not yet: the stall counts from the restart, not from the last record.
    for t in (21, 24):
        tr.t = t
        tr._maybe_restart()
        assert tr.sigma_restarts == 1

    # A full stall later, again -- and the sigma has not moved a step.
    tr.t = 25
    tr.m, tr.v = tr.m + 1.0, tr.v + 1.0
    tr.best_abs_theta = tr.theta + 2.0
    was = np.asarray(tr.theta).copy()
    tr._maybe_restart()
    assert (tr.sigma_restarts, tr.last_improve) == (2, 25)
    assert tr.sigma == pytest.approx(0.02)
    assert np.array_equal(np.asarray(tr.theta), was + 2.0)
    assert not np.asarray(tr.m).any() and tr.adam_t == 0

    # A stepping restart still fires exactly once, however long the run
    # stalls after it.
    up = Trainer(Config(**dict(cfg, stall_sigma_mult=2.0)), seed=3)
    up.best_abs_theta, up.last_improve = up.theta + 1.0, 10
    for t in (20, 40, 80):
        up.t = t
        up._maybe_restart()
    assert (up.sigma_restarts, up.sigma) == (1, pytest.approx(0.04))


def test_a_resume_rebuilds_sigma_with_this_run_s_multiplier(tmp_path):
    """The restart *count* carries; the multiplier is the new invocation's.

    That is the same rule `--sigma` follows, and it is the whole point of the
    flag: an operator lowering the multiplier is doing it because the restart
    the checkpoint recorded was the wrong size, so the resume has to undo it
    rather than faithfully reproduce it.
    """
    a = Trainer(Config(**_CFG), seed=3)
    a.sigma, a.sigma_restarts, a.sigma_steps, a.last_improve = 0.04, 1, 1, 7
    T.save_state(str(tmp_path), a, gen=1)

    same = Trainer(Config(**dict(_CFG, sigma=0.02)), seed=3)   # mult defaults to 2.0
    T.load_resume(same, str(tmp_path))
    assert same.sigma == pytest.approx(0.04) and same.sigma_restarts == 1

    flat = Trainer(Config(**dict(_CFG, sigma=0.02, stall_sigma_mult=1.0)), seed=3)
    T.load_resume(flat, str(tmp_path))
    assert flat.sigma == pytest.approx(0.02) and flat.sigma_restarts == 1


def test_a_repeated_pure_jump_does_not_compound_a_later_multiplier(tmp_path):
    """The exponent is the count of restarts that *stepped* sigma.

    `--stall-sigma-mult 1.0` lets the restart repeat, so its count is a count
    of jumps rather than of doublings. A run that jumped five times and is then
    resumed with `--stall-sigma-mult 2.0` -- an operator changing their mind
    about the step, which is exactly what the flag is for -- has to come back
    at its own sigma, not at 32 times it.
    """
    a = Trainer(Config(**dict(_CFG, stall_sigma_mult=1.0, restart_stall=5)), seed=3)
    a.best_abs_theta = a.theta
    for t in (10, 20, 30, 40, 50):
        a.t = t
        a._maybe_restart()
    assert (a.sigma_restarts, a.sigma_steps) == (5, 0)
    T.save_state(str(tmp_path), a, gen=50)

    up = Trainer(Config(**dict(_CFG, sigma=0.02, stall_sigma_mult=2.0)), seed=3)
    T.load_resume(up, str(tmp_path))
    assert up.sigma == pytest.approx(0.02) and up.sigma_restarts == 5

    # A checkpoint written before the field meant "restarts that stepped": back
    # then the restart could only fire once, so the count is the exponent.
    d = dict(np.load(str(tmp_path / "state.npz"), allow_pickle=False))
    d["sigma_restarts"] = np.int64(1)
    del d["sigma_steps"]
    np.savez(str(tmp_path / "state.npz"), **d)
    old = Trainer(Config(**dict(_CFG, sigma=0.02)), seed=3)
    T.load_resume(old, str(tmp_path))
    assert old.sigma == pytest.approx(0.04) and old.sigma_steps == 1


def test_a_cleared_moment_pair_takes_a_bias_corrected_first_step():
    """The step after a clear must be `lr`-sized, not 3.16 `lr`.

    Adam's bias correction divides by `1 - beta**k` to undo the zero-init of
    `m` and `v`. `k` has to be the number of steps *those moments* have taken:
    `_maybe_restart` and `--from-best` zero them thousands of generations in,
    and correcting them by `1 - beta**t` with `t` in the thousands divides by
    1, leaving `mhat/sqrt(vhat)` at `(1 - beta1)/sqrt(1 - beta2)` = 3.162 per
    coordinate. That is a 3.16x `lr` step on every live weight at once, decaying
    over ~2,000 generations; on flow2 it took ||theta|| 17.6 -> 46 (the
    weight-decay equilibrium is 15.8) and the policy was gone in five
    generations.

    With the moments zeroed, `mhat / sqrt(vhat)` is exactly `sign(g)`, so the
    update is `lr` per coordinate to within `eps_adam` -- and the decoupled
    decay is divided back out here because it is not part of the step.
    """
    cfg = Config(**dict(_CFG, restart_stall=0))
    tr = Trainer(cfg, seed=3)
    before = np.asarray(tr.theta).copy()
    # A long-running optimiser that has just had its moments cleared. 5,001 is
    # coprime with the abs / champion / pool schedules, so this generation is a
    # pure optimiser step.
    tr.m, tr.v = tr.m * 0.0, tr.v * 0.0
    tr.t, tr.adam_t = 5_000, 0
    tr.generation()
    assert (tr.t, tr.adam_t) == (5_001, 1)

    live = (np.asarray(tr.mask) > 0) & (np.asarray(tr.no_decay) == 0)
    # The decay is applied to `theta + step`, not to the step: divide it back
    # out and what is left is the update Adam asked for.
    moved = np.asarray(tr.theta)[live] / (1.0 - cfg.weight_decay) - before[live]
    took_a_step = np.abs(moved) > 1e-12
    assert took_a_step.mean() > 0.9, "the gradient was ~zero; test says nothing"
    assert np.abs(moved[took_a_step]) == pytest.approx(cfg.lr, rel=1e-4)

    # And the number the bug produced, spelled out, so a regression cannot pass
    # by moving the threshold: 0.1 / sqrt(0.001).
    inflated = (1 - cfg.beta1) / np.sqrt(1 - cfg.beta2)
    assert inflated == pytest.approx(3.1623, rel=1e-4)
    assert np.abs(moved[took_a_step]).max() < 2 * cfg.lr


def test_a_checkpoint_without_adam_t_falls_back_to_the_generation_count(tmp_path):
    """Old checkpoints have no `adam_t`; `t` is what they used.

    Their moments are the ones that produced their last step, so continuing
    with `adam_t = t` continues exactly the trajectory they were on.
    """
    a = Trainer(Config(**_CFG), seed=3)
    a.generation(); a.generation()
    a.t, a.adam_t = 700, 700
    T.save_state(str(tmp_path), a, gen=700)

    npz = os.path.join(str(tmp_path), "state.npz")
    d = dict(np.load(npz))
    assert "adam_t" in d
    del d["adam_t"]
    np.savez(npz, **d)

    b = Trainer(Config(**_CFG), seed=999)
    T.load_resume(b, str(tmp_path))
    assert (b.t, b.adam_t) == (700, 700)


def test_adam_t_round_trips_separately_from_the_generation_count(tmp_path):
    """A checkpoint written after a clear must not re-inflate on resume."""
    a = Trainer(Config(**_CFG), seed=3)
    a.generation()
    a.t, a.adam_t = 4_321, 7
    T.save_state(str(tmp_path), a, gen=4_321)

    b = Trainer(Config(**_CFG), seed=999)
    T.load_resume(b, str(tmp_path))
    assert (b.t, b.adam_t) == (4_321, 7)
