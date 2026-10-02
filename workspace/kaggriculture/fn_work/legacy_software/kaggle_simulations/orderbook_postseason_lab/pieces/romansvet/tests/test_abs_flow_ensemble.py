"""The yardstick reads the flow rung at a *family* of levels, not at one.

`Trainer.absolute_report` played the `kagg2_flow` rung at the centre of its
randomisation -- scale 1.0, no day shift -- because a fixed measurement has to
be fixed. Fixed it was; representative it was not. Measured against the real
engine over eight archived thetas (`scripts/fidelity_scoreboard.py`,
2026-08-27):

* the centre's margin ranks them at Spearman **0.738**, and inverts the top
  three -- the three the campaign is actually choosing between;
* the mean over **ten** fixed draws of the same family ranks them at **0.976**
  (leave-one-out >= 0.96); four draws reach 0.929, every single fixed level
  0.76-0.88, and the CVaR/min of the ensemble 0.74-0.76.

So the fix is not more seeds and not a worse-case level: it is averaging over
the *opponent's* randomisation, which is the axis the centre was silently
pinning. `--abs-flow-draws K` does that, `--abs-flow-scale` / `--abs-flow-shift`
say which family, and `--abs-select` says how many of the fixed seed pairs the
resulting statistic is read on. All three are off by default, and the first
test here is that an unflagged run measures exactly what it measured before.

The evaluator is stubbed throughout: what is under test is which episodes the
report builds and how it reduces them, and a stub makes every one of those
arithmetic rather than statistical. `tests/test_kagg2_flow.py` is where the
control word meets the real engine.
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
    NO_BEST,
    Config,
    Trainer,
    cold_starts,
    flow_ensemble_draws,
    place_handicap,
    win_scores,
)

#: Two ordinary rungs and the flow rung, in the order a real run holds them
#: (the flow rung is an extra slot, appended past `--n-archetypes`).
NAMES = ["greedy_farmer", "mixed_ranch", K2F.RUNG_NAME]
FLOW = 2
#: Fixed seed pairs the stand-in yardstick plays. Four, so the two halves the
#: `--abs-select` tests talk about are two pairs each.
PAIRS = 4


def _ev(tables, theta_c, theta_o, words, seat, nquad, money, flow=None):
    """A stand-in evaluator: money as an exact function of the episode.

    Every input the report varies is in the answer, and none of them are in it
    twice, so a wrong mask or a wrong flow word cannot cancel out. `theta_o[0]`
    identifies the rung, `words[..., 0]` the seed pair (the stand-in's
    `abs_words` are just their own indices), `seat` the side, and the flow
    word's two level columns the ensemble member. `own` moves with the scale
    and `theirs` with the day shift, so a margin depends on both.
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


def _tr(**cfg):
    """A `Trainer` carrying only what `absolute_report` reads, plus the stub.

    `__new__` rather than a real construction: the ladder here is three named
    thetas of three numbers each, and building the real one would spend a
    minute of archetype probing to measure a stub.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**dict({"abs_pairs": PAIRS, "kagg2_flow": True}, **cfg))
    tr.tables = None
    tr.theta = np.zeros(3)
    tr.n = 3
    tr.archetype_names = list(NAMES)
    tr.archetypes = [np.full(3, float(i + 1)) for i in range(len(NAMES))]
    tr.archetype_coins = []
    tr.rung_weights = np.ones(len(NAMES))
    tr.arch_handicap = np.zeros((len(NAMES), 2), np.int32)
    tr.holdout_thetas = []
    tr.flow_rung = FLOW
    # The stand-in seed set: row `i` is the number `i`, which is what `_ev`
    # reads back out as the seed index.
    tr.abs_words = np.arange(PAIRS, dtype=np.float64).reshape(PAIRS, 1, 1)
    tr.n_abs_sel = max(PAIRS // 2, 1)
    tr._check_abs_select()
    tr.abs_draws = tuple(flow_ensemble_draws(
        tr.cfg.abs_flow_draws, tr.cfg.abs_flow_scale, tr.cfg.abs_flow_shift))
    tr.evaluate = _ev
    return tr


def _calls(tr):
    """Record every `evaluate` call the next report makes. -> list of kwargs."""
    seen = []

    def spy(tables, tc, to, words, seat, nquad, money, flow=None):
        seen.append({"n": np.asarray(to).shape[0],
                     "rung": np.asarray(to)[:, 0].astype(int),
                     "seat": np.asarray(seat).astype(int),
                     "seed": np.asarray(words).reshape(-1)[::1].astype(int),
                     "flow": None if flow is None else np.asarray(flow)})
        return _ev(tables, tc, to, words, seat, nquad, money, flow)

    tr.evaluate = spy
    return seen


# --------------------------------------------------------------- zero diff

def test_no_draws_is_the_measurement_that_came_before_them():
    """(a) K=0: one call, the same episodes, the flow rung at the centre.

    The batch is the whole claim -- everything downstream is a reduction of it
    -- so this pins the *call*, not just the numbers: one evaluator call of
    `2 * pairs * rungs` episodes with the flow rung's word at scale 1000 and
    shift 0, which is byte for byte what the report built before the ensemble
    existed.
    """
    tr = _tr()
    seen = _calls(tr)
    rep = tr.absolute_report(tr.theta)
    assert len(seen) == 1
    call = seen[0]
    assert call["n"] == 2 * PAIRS * len(NAMES)
    # The rung/seat/seed decomposition, exactly as it was: `k % r`, `(k // r) %
    # 2`, `k // (2 * r)`.
    k = np.arange(call["n"])
    assert np.array_equal(call["rung"], k % len(NAMES) + 1)
    assert np.array_equal(call["seat"], (k // len(NAMES)) % 2)
    assert np.array_equal(call["seed"], k // (2 * len(NAMES)))
    flow = call["flow"]
    isf = (k % len(NAMES)) == FLOW
    assert np.array_equal(flow[isf][:, 1:], np.tile([1000, 0], (isf.sum(), 1)))
    # The rung is the opponent, so its seat is `1 - seat`, and every other
    # episode is forced back to the off word.
    assert np.array_equal(flow[isf][:, 0], 1 - call["seat"][isf])
    assert (flow[~isf][:, 0] == -1).all()

    # And the three fields the ensemble added are inert.
    assert (rep.flow_draws, rep.flow_ens_margin, rep.flow_centre_margin) \
        == (0, 0.0, 0.0)


def test_no_draws_reduces_the_batch_by_the_old_masks():
    """(a) The other half of zero-diff: the same money array, the same means.

    `per`/`hold` grew a block mask (base episodes or ensemble episodes) and a
    subset mask (`--abs-select`). With no draws and the default subset both are
    the identity, and the report has to equal the old `sel & (rung == i)` /
    `~sel & (rung == i)` reduction of the very same games.
    """
    tr = _tr()
    seen = _calls(tr)
    rep = tr.absolute_report(tr.theta)
    r, n = len(NAMES), seen[0]["n"]
    money = _ev(None, None, np.stack([tr.archetypes[i] for i in seen[0]["rung"] - 1]),
                seen[0]["seed"].reshape(n, 1, 1), seen[0]["seat"], None, None,
                seen[0]["flow"])
    k = np.arange(n)
    sel = (k // (2 * r)) < tr.n_abs_sel
    for i in range(r):
        m, h = sel & (k % r == i), (~sel) & (k % r == i)
        assert rep.mine[i] == pytest.approx(money[m, 0].mean())
        assert rep.theirs[i] == pytest.approx(money[m, 1].mean())
        assert rep.holdout_mine[i] == pytest.approx(money[h, 0].mean())
        assert rep.holdout_theirs[i] == pytest.approx(money[h, 1].mean())
        assert rep.wins[i] == pytest.approx(
            np.asarray(win_scores(money[m, 0], money[m, 1])).mean())


def test_the_config_defaults_are_the_old_yardstick():
    cfg = Config()
    assert cfg.abs_flow_draws == 0 and cfg.abs_select == "sel"
    assert cfg.abs_flow_scale == (500, 1500) and cfg.abs_flow_shift == (-2, 2)
    assert flow_ensemble_draws(0) == []


# ------------------------------------------------------------- the ensemble

def test_two_draws_are_the_mean_of_the_two_readings():
    """(b) The reported flow margin is the mean of the draws' margins.

    Compared against the same report run at each draw on its own, which is the
    K=1 case of the very same code path -- so what this pins is that the K
    blocks do not contaminate each other and that the reduction over their
    union is the mean of their means (it is, because every draw contributes the
    same episodes).
    """
    two = _tr(abs_flow_draws=2)
    draws = two.abs_draws
    assert len(draws) == 2 and draws[0] != draws[1]
    rep = two.absolute_report(two.theta)
    assert rep.flow_draws == 2

    each = []
    for d in draws:
        one = _tr(abs_flow_draws=1)
        one.abs_draws = (d,)      # the same code path, one member of the list
        r1 = one.absolute_report(one.theta)
        each.append(r1.mine[FLOW] - r1.theirs[FLOW])
        assert r1.flow_ens_margin == pytest.approx(each[-1])

    assert rep.mine[FLOW] - rep.theirs[FLOW] == pytest.approx(np.mean(each))
    assert rep.flow_ens_margin == pytest.approx(np.mean(each))
    # Two genuinely different readings, or the mean would prove nothing.
    assert each[0] != pytest.approx(each[1])


def test_the_ensemble_replaces_the_flow_rung_and_leaves_the_others_alone():
    """The other rungs are the centre reading they always were, and the flow
    rung's centre is still measured -- it is just no longer what selects."""
    off, on = _tr(), _tr(abs_flow_draws=2)
    a, b = off.absolute_report(off.theta), on.absolute_report(on.theta)
    for i in range(len(NAMES)):
        if i == FLOW:
            continue
        assert (a.mine[i], a.theirs[i]) == (b.mine[i], b.theirs[i])
        assert a.holdout_mine[i] == b.holdout_mine[i]
    assert b.flow_centre_margin == pytest.approx(a.mine[FLOW] - a.theirs[FLOW])
    assert b.flow_ens_margin != pytest.approx(b.flow_centre_margin)
    # `mine`/`theirs` on the flow rung are the ensemble now: that is what makes
    # `--select-metric margin:kagg2_flow` select on the de-biased number
    # without a second reduction rule anywhere else.
    assert on.selection_score(b) is not None
    on.cfg = on.cfg._replace(select_metric=f"margin:{K2F.RUNG_NAME}")
    assert on.selection_score(b) == pytest.approx(b.flow_ens_margin)


def test_the_ensemble_blocks_carry_the_handicap_and_the_seat_the_centre_does():
    """A draw's block is the flow rung's own episodes, laid out as the base
    block lays that rung out: both seats of every fixed pair, the rung as the
    *opponent* (so its word goes on `1 - seat` and its opening on `1 - seat`).
    Getting either backwards would point the flow at our own farm.
    """
    tr = _tr(abs_flow_draws=2)
    tr.arch_handicap = np.array([[1, 0], [1, 0], [3, 20_000]], np.int32)
    seen = _calls(tr)
    tr.absolute_report(tr.theta)
    call, r = seen[0], len(NAMES)
    base = 2 * PAIRS * r
    assert call["n"] == base + 2 * (2 * PAIRS)
    ext = slice(base, None)
    assert (call["rung"][ext] == FLOW + 1).all()
    # Both seats, every pair, once per draw.
    j = np.arange(2 * PAIRS)
    assert np.array_equal(call["seat"][ext], np.tile(j % 2, 2))
    assert np.array_equal(call["seed"][ext], np.tile(j // 2, 2))
    assert np.array_equal(call["flow"][ext][:, 0], 1 - call["seat"][ext])
    for i, (s, d) in enumerate(tr.abs_draws):
        blk = slice(base + i * 2 * PAIRS, base + (i + 1) * 2 * PAIRS)
        assert (call["flow"][blk][:, 1] == s).all()
        assert (call["flow"][blk][:, 2] == d).all()

    # The rung's opening is raised on the opponent's physical seat, in the
    # ensemble blocks exactly as in the base one. `place_handicap` is a
    # `maximum`, so a cold start reads it straight back.
    nq, mo = cold_starts(call["n"])
    nq, mo = place_handicap(nq, mo, 1 - call["seat"].astype(np.int64),
                            tr.arch_handicap[call["rung"] - 1])
    opp = np.arange(call["n"]), 1 - call["seat"]
    assert (nq[opp][ext] == 3).all() and (mo[opp][ext] == 20_000).all()


def test_a_run_without_the_flow_rung_ignores_the_draws_entirely():
    """`--abs-flow-draws` needs a rung to average; `scripts/train.py` refuses
    the flag without `--kagg2-flow`, and the report is inert if one arrives
    anyway (a resume into a ladder that never had the rung)."""
    tr = _tr(abs_flow_draws=4)
    tr.flow_rung = -1
    seen = _calls(tr)
    rep = tr.absolute_report(tr.theta)
    assert len(seen) == 1 and seen[0]["n"] == 2 * PAIRS * len(NAMES)
    assert rep.flow_draws == 0 and seen[0]["flow"] is None


def test_the_batch_is_split_once_it_outgrows_chunk_and_never_before():
    """One call while the batch is the size it always was -- a run without the
    ensemble must not start sharding a call that never sharded -- and shards of
    `--chunk` once the ensemble has grown it past that."""
    tr = _tr(abs_flow_draws=4, chunk=8)
    seen = _calls(tr)
    a = tr.absolute_report(tr.theta)
    base = 2 * PAIRS * len(NAMES)
    assert len(seen) > 1 and sum(c["n"] for c in seen) == base + 4 * 2 * PAIRS
    # The first shard is the whole un-grown batch: `chunk` cannot make the
    # measurement finer-grained than it was.
    assert seen[0]["n"] == base

    # And the split is only a split: the same numbers come out of it.
    whole = _tr(abs_flow_draws=4, chunk=100_000)
    b = whole.absolute_report(whole.theta)
    assert a.mine == b.mine and a.theirs == b.theirs
    assert a.flow_ens_margin == pytest.approx(b.flow_ens_margin)


# ------------------------------------------------------------- the levels

def test_the_levels_are_fixed_and_are_the_scoreboards():
    """The draws are the ones the fidelity table was computed on, in its order.

    Hard-coded rather than recomputed: the whole value of the statistic is that
    it does not move, and a test that re-derives it from the same generator
    would pass through any change to the generator.
    """
    assert flow_ensemble_draws(4) == [(541, 2), (675, 2), (743, -1), (967, -2)]
    assert flow_ensemble_draws(10) == [
        (541, 0), (675, 1), (743, 2), (967, 2), (1464, 1),
        (674, -1), (1299, 2), (797, -1), (1327, -1), (1383, 2)]
    # The scales are a prefix of one another and the shifts are not: `integers`
    # starts from wherever `uniform(k)` left the stream. So K is part of the
    # yardstick's identity, not a truncation of it -- which is why the ladder
    # signature carries the whole list and not just K.
    assert [s for s, _ in flow_ensemble_draws(4)] == \
           [s for s, _ in flow_ensemble_draws(10)][:4]
    assert [d for _, d in flow_ensemble_draws(4)] != \
           [d for _, d in flow_ensemble_draws(10)][:4]


def test_the_ranges_move_the_family_without_moving_the_stream():
    """`--abs-flow-scale 800:1800 --abs-flow-shift 0:4` recentres the family on
    scale 1.3 / shift +2, which is where the real engine's margins matched the
    sim's -- the same draws of the same generator, mapped elsewhere."""
    wide = flow_ensemble_draws(10)
    up = flow_ensemble_draws(10, (800, 1800), (0, 4))
    assert len(up) == 10
    assert all(800 <= s <= 1800 and 0 <= d <= 4 for s, d in up)
    # A pure shift of the scale axis: same width, same draws, +300 each.
    assert [s for s, _ in up] == [s + 300 for s, _ in wide]
    assert np.mean([s for s, _ in up]) == pytest.approx(1_287.0)

    with pytest.raises(ValueError, match="abs_flow_scale"):
        flow_ensemble_draws(4, (1500, 500))
    with pytest.raises(ValueError, match="abs_flow_shift"):
        flow_ensemble_draws(4, (500, 1500), (3, -3))


def test_a_degenerate_range_pins_the_level():
    """`--abs-flow-scale 1300:1300 --abs-flow-shift 2:2` is the single fixed
    level the ensemble replaced, moved -- worth having as an ablation, so it
    has to be expressible rather than refused."""
    assert flow_ensemble_draws(3, (1300, 1300), (2, 2)) == [(1300, 2)] * 3


# ------------------------------------------------------- which seeds select

def test_abs_select_moves_the_selected_subset_and_the_reported_one():
    """`sel` is the first half (today), `hold` swaps them, `all` is every pair.

    Under `all` the *reported* holdout stays the second half: it is no longer
    held out and cannot gate anything (`--best-gate both` is refused), but it
    is still the diagnostic column every tracker plots.
    """
    reps = {k: _tr(abs_select=k).absolute_report(np.zeros(3))
            for k in ("sel", "hold", "all")}
    a, b, c = reps["sel"], reps["hold"], reps["all"]

    # A straight swap: what `sel` selects on is what `hold` reports, and back.
    assert b.mine == a.holdout_mine and b.holdout_mine == a.mine
    assert b.theirs == a.holdout_theirs and b.holdout_theirs == a.theirs
    # `all` is the mean of the two halves (they are the same size), and its
    # holdout column is still the second half.
    for i in range(len(NAMES)):
        assert c.mine[i] == pytest.approx((a.mine[i] + a.holdout_mine[i]) / 2)
    assert c.holdout_mine == a.holdout_mine


def test_abs_select_all_is_refused_with_the_holdout_gate():
    """(the documented interaction) `all` puts the gate's holdout inside the
    selected set, so `--best-gate both` would compare a statistic with a piece
    of itself. Refused at construction rather than left a silent no-op."""
    with pytest.raises(ValueError, match="abs_select 'all' with best_gate"):
        _tr(abs_select="all", best_gate="both")
    # Either alone is fine, and so is `hold` with the gate -- there the two
    # halves are still disjoint, just the other way round.
    _tr(abs_select="all")
    _tr(abs_select="hold", best_gate="both")
    with pytest.raises(ValueError, match="expected 'sel', 'hold' or 'all'"):
        _tr(abs_select="holdout")


def test_abs_select_hold_needs_a_second_half():
    with pytest.raises(ValueError, match="the second half is empty"):
        _tr(abs_select="hold", abs_pairs=1)


def test_the_ensemble_and_the_subset_compose():
    """Both flags at once is the recommended launch shape (K=10, `all`), so the
    flow rung's number has to be the ensemble read over every pair."""
    tr = _tr(abs_flow_draws=2, abs_select="all")
    rep = tr.absolute_report(tr.theta)
    halves = [_tr(abs_flow_draws=2, abs_select=k).absolute_report(tr.theta)
              for k in ("sel", "hold")]
    assert rep.flow_ens_margin == pytest.approx(
        np.mean([h.flow_ens_margin for h in halves]))
    assert rep.flow_centre_margin == pytest.approx(
        np.mean([h.flow_centre_margin for h in halves]))


# ---------------------------------------------------------- the signature

class _Ladder:
    """The fields `ladder_signature` and the reset rule read, as in
    `tests/test_select_margin.py`."""

    def __init__(self, **cfg):
        self.cfg = Config(**cfg)
        self.archetype_names = ["a", "b"]
        self.rung_weights = np.ones(2)
        self.arch_handicap = np.zeros((2, 2), np.int32)
        self.theta = np.zeros(3)
        self.best_abs, self.best_abs_theta = -4_200.0, np.ones(3)
        self.best_hold, self.champion_score = -4_500.0, -4_200.0


def test_the_signature_carries_the_ensemble_and_the_subset():
    """(c) Switching either retires the inherited record.

    A margin against the centre and a margin against the ten-draw mean are
    numbers about two different opponents, thousands of coins apart on the same
    theta -- so an inherited best is not a bar the new run can clear or fail to
    clear, it is a bar about something else.
    """
    sig = T.ladder_signature(_Ladder())
    assert sig["flow_ensemble"] == {"k": 0, "draws": []}
    assert sig["abs_select"] == "sel"
    full = T.ladder_signature(_Ladder(abs_flow_draws=2))
    # K=2's own draws, not the first two of K=4's: `integers` starts from
    # wherever `uniform(k)` left the stream, so K is part of the identity.
    assert full["flow_ensemble"]["draws"] == [[541, 0], [675, -1]]

    for kw, want in (({"abs_flow_draws": 10}, "flow ensemble K 0 -> 10"),
                     ({"abs_select": "all"}, "abs seeds sel -> all")):
        tr = _Ladder(**kw)
        tr.ckpt_rungs, tr.ckpt_ladder = 2, T.ladder_signature(_Ladder())
        note = T.reset_best_if_ladder_changed(tr)
        assert want in note
        assert tr.best_abs is NO_BEST or tr.best_abs == NO_BEST
        assert tr.best_hold == NO_BEST and tr.champion_score == NO_BEST


def test_recentring_the_family_at_the_same_k_still_retires_the_record():
    """The levels, not just their count: `--abs-flow-scale 800:1800` is a
    different opponent at the same K, and "K 10 -> 10" would read as no change
    at all."""
    tr = _Ladder(abs_flow_draws=4, abs_flow_scale=(800, 1800))
    tr.ckpt_rungs = 2
    tr.ckpt_ladder = T.ladder_signature(_Ladder(abs_flow_draws=4))
    note = T.reset_best_if_ladder_changed(tr)
    assert "flow ensemble levels" in note and tr.best_abs == NO_BEST


def test_the_same_yardstick_still_carries_the_best_over():
    """Zero-diff: adding two fields to the signature must not reset every
    resume, and a checkpoint written before they existed was written by a run
    that read the centre on the selection half -- which is the default."""
    tr = _Ladder(abs_flow_draws=4)
    tr.ckpt_rungs, tr.ckpt_ladder = 2, T.ladder_signature(_Ladder(abs_flow_draws=4))
    assert T.reset_best_if_ladder_changed(tr) is None
    assert tr.best_abs == -4_200.0

    old = T.ladder_signature(_Ladder())
    del old["flow_ensemble"], old["abs_select"]
    plain = _Ladder()
    plain.ckpt_rungs, plain.ckpt_ladder = 2, old
    assert T.reset_best_if_ladder_changed(plain) is None
    assert T._read_signature(old)["flow_ensemble"] == {"k": 0, "draws": []}
    assert T._read_signature(old)["abs_select"] == "sel"
