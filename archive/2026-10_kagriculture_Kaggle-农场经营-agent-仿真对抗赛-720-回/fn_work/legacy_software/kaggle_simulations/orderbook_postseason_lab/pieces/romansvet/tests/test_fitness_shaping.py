"""What the ES objective is allowed to reward.

The objective was rebuilt on 2026-08-25 around an absolute target: earn at
least twice what the fixed evaluation opponent does, i.e. >= 300k coins, in a
contested market. Measured on the run that motivated it, the old objective
could not express that. `mean_win` saturated in ~100 generations and decayed
back to 0.5 (the pool is the policy's own lineage, so "beat your past selves"
is satisfiable at any absolute level); `abs` plateaued after ~30 minutes of a
13 h run; and the champion rule correlated **-0.17** with absolute strength.

These tests pin the properties that fix follows from: the anchor is now the
majority term and it is a *log* mean, the margin term keeps resolution over the
coin range the target actually sits in, and the shaping still separates
candidates the win bit calls equal. The head and aux biases are exempt from
weight decay and bounded by a clip instead, so that is pinned too.
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

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg3.core import policy as PO
from kagg3.es import archetypes as AR
from kagg3.es.train import (Config, Trainer, batch_mesh, bias_mask,
                            fitness_components, own_coin_score,
                            rank_normalise, shaped_advantage, win_scores)


def _legacy_components(mine, theirs, cfg, tape=None, bonus=None,
                       ep_weight=None):
    if bonus is None:
        rel = jax.nn.sigmoid((mine - theirs) / cfg.margin_scale)
    else:
        rel = jax.nn.sigmoid((mine - theirs + bonus) / cfg.margin_scale)
    if tape is not None:
        ours = mine if bonus is None else mine + bonus
        rel = jnp.where(tape, own_coin_score(ours, cfg), rel)
    own = jnp.log1p(jnp.maximum(mine, 0.0))
    if ep_weight is None:
        rel, own = rel.mean(axis=1), own.mean(axis=1)
    else:
        w = jnp.asarray(ep_weight, jnp.float32)
        w = w / jnp.sum(w)
        rel, own = (rel * w).sum(axis=1), (own * w).sum(axis=1)
    return own, rel


@pytest.mark.parametrize("weighted", [False, True])
def test_factored_fitness_components_are_byte_exact(weighted):
    mine = jnp.asarray([[10, 50, 90], [20, 40, 120]], jnp.float32)
    theirs = jnp.asarray([[8, 70, 80], [25, 30, 100]], jnp.float32)
    cfg = Config(d10_cash_weight=0.25)
    tape = jnp.asarray([False, True, False]) if weighted else None
    bonus = jnp.asarray([[1, 2, 3], [4, 5, 6]], jnp.float32) if weighted else None
    weight = jnp.asarray([2, 1, 3], jnp.float32) if weighted else None
    got = fitness_components(mine, theirs, cfg, tape, bonus, weight)
    want = _legacy_components(mine, theirs, cfg, tape, bonus, weight)
    for a, b in zip(got, want):
        aa, bb = np.asarray(a), np.asarray(b)
        assert aa.dtype == bb.dtype and aa.shape == bb.shape
        assert aa.tobytes() == bb.tobytes()
    reconstructed = (cfg.abs_weight * rank_normalise(got[0])
                     + (1.0 - cfg.abs_weight) * rank_normalise(got[1]))
    direct = shaped_advantage(mine, theirs, cfg, tape, bonus, weight)
    assert np.asarray(reconstructed).tobytes() == np.asarray(direct).tobytes()


def test_defaults_are_the_coin_objective():
    """The three numbers the rebuild turns on, pinned where a reader can see them."""
    cfg = Config()
    assert cfg.abs_weight == 0.6            # the anchor is the majority term
    assert cfg.margin_scale == 100_000.0    # resolution out to the 300k target
    assert cfg.arch_frac == 0.5             # half the slots face a real strategy


def test_the_win_tracking_flags_all_default_to_todays_behaviour():
    """The no-op guarantee for 2026-08-26's block.

    Every one of these is a *lever*, and the argument for each is a design
    argument the evidence does not settle (the plan grades the proxy's weight
    and tau "not established"). An unflagged run therefore has to be the run
    that came before them, or a training curve cannot be compared with the one
    beside it.
    """
    cfg = Config()
    assert cfg.rung_weight == ()                 # every rung an equal share
    assert cfg.proxy_handicap == AR.NO_HANDICAP  # the engine's own day 0
    assert cfg.select_metric == "coins"          # what best_abs.npy always meant
    assert cfg.select_coin_floor == 0.0
    assert cfg.collapse_floor == 0.0             # the second floor reports only
    assert AR.NO_HANDICAP == (1, 3_000)


def test_absolute_anchor_ranks_the_richer_of_two_equal_margins():
    # Same +5,000 margin, wildly different economies. A purely relative
    # objective scores these identically, which is what let self-play drift
    # scale-free: "beat the clone by 5k" is satisfiable at any absolute level.
    mine = jnp.asarray([[10_000.0], [60_000.0]])
    theirs = jnp.asarray([[5_000.0], [55_000.0]])

    adv = shaped_advantage(mine, theirs, Config())

    assert float(adv[1]) > float(adv[0])


def test_which_of_the_anchor_and_the_margin_wins_is_the_abs_weight_flag():
    """The one case where the two terms genuinely disagree, on both settings.

    Candidate 0 wins its game by 30k while earning 40k; candidate 1 earns 90k
    and loses by 5k. Under the *old* weights (0.65 on the margin) the winner
    ranked first, and a run could satisfy the objective at 40k a game forever;
    at today's 0.6 on the anchor the richer candidate wins, which is what
    "the target is stated in coins" means.

    It deliberately flips at the plan's proposed settings, and that is the
    point of asserting both branches rather than deleting one: `abs_weight` 0.3
    with tau 25k scores this pair -0.20 / +0.20 where today's scores it
    +0.10 / -0.10. A run switched to the win-tracking objective is *supposed*
    to prefer the near-tie over the rich loss -- the tournament pays for the
    sign of the margin and nothing else -- and a test that pinned only one
    branch would read as if one of the two were a bug.
    """
    mine = jnp.asarray([[40_000.0], [90_000.0]])
    theirs = jnp.asarray([[10_000.0], [95_000.0]])

    coins_first = shaped_advantage(mine, theirs, Config())
    assert float(coins_first[1]) > float(coins_first[0])
    assert [round(float(x), 2) for x in coins_first] == [-0.10, 0.10]

    wins_first = shaped_advantage(
        mine, theirs, Config(abs_weight=0.3, margin_scale=25_000.0))
    assert float(wins_first[0]) > float(wins_first[1])
    assert [round(float(x), 2) for x in wins_first] == [0.20, -0.20]


def test_the_relative_term_still_breaks_a_tie_on_coins():
    # Identical coins in every episode, so the anchor ranks these dead level and
    # only the margin can order them. The win term is a minority weight, not a
    # deleted one: the tournament is still head-to-head.
    mine = jnp.asarray([[50_000.0], [50_000.0]])
    theirs = jnp.asarray([[10_000.0], [90_000.0]])

    adv = shaped_advantage(mine, theirs, Config())

    assert float(adv[0]) > float(adv[1])


def test_the_anchor_is_a_log_mean_so_one_blowout_cannot_carry_a_candidate():
    # Equal *arithmetic* mean coins (100k), earned two ways: candidate 0 does it
    # on every seed, candidate 1 does it on one and collapses on the other. ES
    # ranks on the whole seed set or it chases outliers, and log1p is what makes
    # the mean insensitive to the tail. Margins are equal, so the relative term
    # cannot be the thing separating them.
    mine = jnp.asarray([[100_000.0, 100_000.0], [200_000.0, 0.0]])
    theirs = mine - 10_000.0

    adv = shaped_advantage(mine, theirs, Config())

    assert float(np.mean(np.asarray(mine)[0])) == float(np.mean(np.asarray(mine)[1]))
    assert float(adv[0]) > float(adv[1])


def test_margin_scale_keeps_resolution_over_the_target_coin_range():
    """The sigmoid has to still be sloped where the run is expected to live.

    At the old 25,000 the term is flat past about +-50k: margins of 100k, 200k
    and 300k map to 0.982, 0.9997 and 0.999994, a spread of 0.018, and the
    relative term degenerates into the win bit it was introduced to improve on.
    At 100,000 the same three margins spread over 0.22.
    """
    margins = jnp.asarray([100_000.0, 200_000.0, 300_000.0])
    wide = jax.nn.sigmoid(margins / Config().margin_scale)
    narrow = jax.nn.sigmoid(margins / 25_000.0)

    assert float(wide.max() - wide.min()) > 0.15
    assert float(narrow.max() - narrow.min()) < 0.05


def test_what_lowering_the_margin_scale_buys_and_what_it_costs():
    """The tau argument, as the slope per coin `s(1-s)/tau` at four margins.

    Today's 100k is nearly flat over the whole range a run visits (1.7e-6 to
    2.5e-6, a factor of 1.5), so a coin of margin against a rung that already
    collapsed is priced almost exactly as dearly as a coin in a game that is
    close. 25k concentrates the resolution inside +-50k of a tie and discounts
    the runaway wins several-fold. It is not about breaking ties; it is about
    refusing to pay for them -- and the flag exists because §3.1 of the plan
    could not distinguish the two settings against the real margin.
    """
    slope = lambda m, tau: float(jax.nn.sigmoid(m / tau)
                                 * (1 - jax.nn.sigmoid(m / tau)) / tau)
    #                       margin            where it occurs
    wide = {m: slope(m, 100_000.0) for m in (-49_000, 20_000, 100_000, 128_000)}
    narrow = {m: slope(m, 25_000.0) for m in wide}

    # -49k is the real kagg2 game and the calibrated proxy: 1.8x the resolution.
    assert narrow[-49_000] / wide[-49_000] == pytest.approx(1.84, rel=0.02)
    # +20k is the hardest rung against the weakest working checkpoint.
    assert narrow[20_000] / wide[20_000] > 3.0
    # And the blow-outs are what pays for it: +100k against `expander`, +128k
    # against `staple_bulk`, discounted 2.8x and 7.2x.
    assert narrow[100_000] / wide[100_000] == pytest.approx(0.36, rel=0.05)
    assert narrow[128_000] / wide[128_000] == pytest.approx(0.14, rel=0.05)
    # Today's tau is flat across the lot; the proposed one is not.
    assert max(wide.values()) / min(wide.values()) < 1.6
    assert max(narrow.values()) / min(narrow.values()) > 15


def test_margin_shaping_separates_candidates_the_win_bit_ties():
    # Both candidates win one game and lose one, on identical own coins, so
    # neither the win rate nor the anchor can tell them apart. Candidate 0 wins
    # by 20k where candidate 1 scrapes by on 1k.
    mine = jnp.asarray([[30_000.0, 10_000.0], [30_000.0, 10_000.0]])
    theirs = jnp.asarray([[10_000.0, 30_000.0], [29_000.0, 30_000.0]])

    win = win_scores(mine, theirs).mean(axis=1)
    adv = shaped_advantage(mine, theirs, Config())

    assert float(win[0]) == float(win[1]) == 0.5
    assert float(adv[0]) > float(adv[1])


def test_versus_pool_scores_wins_not_coins():
    """The ladder measurement is still a win rate -- it is an eviction rule.

    Champion selection left it on 2026-08-25 (see `_measure_champion`), but
    `_snapshot` still asks "which rung does the current theta beat most easily",
    and that is genuinely a head-to-head question.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config()
    tr.pool = [jnp.zeros(5), jnp.ones(5)]
    # Rich but always one coin short: a coin-based rule would love this policy.
    tr.evaluate = lambda tables, th, opp, words, seat, nq, mo: jnp.stack(
        [jnp.full(th.shape[0], 1e6), jnp.full(th.shape[0], 1e6 + 1.0)], axis=1)

    got = tr._versus_pool(jnp.zeros(5), jnp.zeros((4, 3, 4), jnp.uint32), None)

    assert got.shape == (2,)
    assert np.allclose(got, 0.0)


def _flat_trainer(**cfg_kw):
    """A Trainer whose game is flat, so every rank ties and the gradient is 0.

    Whatever moves theta in `generation` is then the update rule alone: decay on
    the ordinary coordinates, the clip on the exempt ones.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(pop=4, episodes=2, chunk=4, **cfg_kw)
    tr.mesh, tr.n_devices = batch_mesh()
    tr.tables = None
    tr.evaluate = lambda tables, th, opp, words, seat, nq, mo: jnp.full((th.shape[0], 2), 50_000.0)
    tr.n = 5
    tr.m, tr.v, tr.t, tr.adam_t = jnp.zeros(5), jnp.zeros(5), 0, 0
    tr.sigma = tr.cfg.sigma
    tr.sigma_restarts, tr.last_improve = 0, 0
    tr.key = jax.random.PRNGKey(0)
    tr.rng = np.random.default_rng(0)
    tr.archetypes = []
    tr.history = []
    return tr


def test_zero_gradient_generation_shrinks_theta_by_the_decay_factor():
    """Weight decay must be decoupled, i.e. applied to theta after the step.

    Added to the gradient it is invisible: measured on fix1, |wd*theta| is 1.0%
    of |grad| per coordinate, and Adam then normalises the sum, so the norm
    random-walked 15.2 -> 41.0 unchecked. Decoupled, the equilibrium is
    ||theta|| = lr*sqrt(n / (2*lambda)).
    """
    tr = _flat_trainer(weight_decay=0.003)
    tr.theta = jnp.asarray(np.arange(1, 6, dtype=np.float32))
    # All-ones: this five-parameter theta is not the real layout, so it has no
    # dead columns (section 2's mask is layout-derived). The masked update must
    # still shrink every coordinate by exactly the decay factor.
    tr.mask = jnp.ones(5, jnp.float32)
    tr.no_decay = jnp.zeros(5, jnp.float32)
    tr.pool = [tr.theta]
    before = np.asarray(tr.theta)

    tr.generation()

    assert np.allclose(np.asarray(tr.theta), before * (1 - 0.003), rtol=0, atol=1e-6)


def test_exempt_bias_coordinates_are_clipped_instead_of_decayed():
    """The head/aux biases keep their value and gain a box, not a shrink.

    Decay pins ||theta|| near 15.4 spread over 3,561 live coordinates, which
    leaves a head logit unable to pass about +-1.2 -- while the archetypes need
    +-10 to +-30 to saturate the land bias (a tanh on head[1]). A bias that
    cannot commit is clamped, not regularised.
    """
    tr = _flat_trainer(weight_decay=0.5, bias_clip=8.0)
    tr.theta = jnp.asarray(np.array([1.0, 20.0, -20.0, 4.0, 4.0], np.float32))
    tr.mask = jnp.ones(5, jnp.float32)
    tr.no_decay = jnp.asarray(np.array([0.0, 1.0, 1.0, 1.0, 0.0], np.float32))
    tr.pool = [tr.theta]

    tr.generation()

    got = np.asarray(tr.theta)
    assert got[0] == 0.5                       # decayed
    assert got[1] == 8.0 and got[2] == -8.0    # exempt, clipped into the box
    assert got[3] == 4.0                       # exempt, inside the box: untouched
    assert got[4] == 2.0                       # decayed


def test_bias_mask_covers_exactly_the_head_aux_and_dev_bias_blocks():
    m = bias_mask()
    assert m.shape == (PO.N_PARAMS,) and m.dtype == np.float32
    assert int(m.sum()) == PO.N_HEAD_OUT + PO.N_AUX_OUT + PO.N_DEV_OUT == 23
    for name in ("gb2", "gb5", "gb6"):
        off = PO.offset(name)
        n = int(np.prod(dict(PO.SHAPES)[name]))
        assert np.all(m[off:off + n] == 1.0)
    # The weights feeding those biases stay under decay: only the constant term
    # is exempt, so the exemption cannot inflate the whole head.
    for name in ("g2", "g5", "g6", "w1", "b2"):
        off = PO.offset(name)
        n = int(np.prod(dict(PO.SHAPES)[name]))
        assert np.all(m[off:off + n] == 0.0)


# ---------------------------------------------------- the decay is a flag now

def test_the_weight_decay_flag_reaches_the_config_and_the_log():
    """`--weight-decay` is not independent of `--lr`, so it has to be settable.

    Decoupled decay settles the weights at a norm of about
    `lr * sqrt(n / (2 * wd))` -- the point where the step's contribution and
    the decay's cancel. The default pair (lr 0.02, wd 0.003) sits at ~15.8 on
    this parameter count; an A/B that drops lr to 0.005 and leaves wd alone
    lands at ~4, so it has moved the norm the policy lives at as well as the
    step size, and whichever way the run then goes cannot be attributed to
    either. Holding the norm at lr 0.005 wants wd 0.0001875, which was not
    expressible before this flag.

    Driven through the script rather than through `Config`, because what is
    under test is the plumbing: the value has to survive argparse, reach the
    Config the Trainer is built from, and land in both files a tracker reads.
    `--gens 0` runs the whole startup path and no generations.
    """
    import json
    import shutil
    import subprocess

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run = "_wd_flag_check"
    out = os.path.join(root, "artifacts", run)
    shutil.rmtree(out, ignore_errors=True)
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(root, "scripts", "train.py"),
             "--run", run, "--gens", "0", "--pop", "2", "--episodes", "2",
             "--chunk", "2", "--abs-pairs", "2", "--n-archetypes", "0",
             "--no-holdout-rungs", "--lr", "0.005",
             "--weight-decay", "0.0001875"],
            capture_output=True, text=True,
            env=dict(os.environ, JAX_PLATFORMS="cpu"))
        assert r.returncode == 0, r.stderr[-3000:]

        # config.json is the invocation; the log header is what a tracker
        # comparing two runs' curves reads without the directory beside it.
        cfg = json.load(open(os.path.join(out, "config.json")))
        assert cfg["weight_decay"] == 0.0001875 and cfg["lr"] == 0.005
        with open(os.path.join(out, "log.jsonl")) as fh:
            head = json.loads(fh.readline())
        assert head["weight_decay"] == 0.0001875
        assert head["lr"] == 0.005 and head["sigma"] == 0.02
        # And on the one line an operator actually watches scroll past.
        assert "lr=0.005" in r.stdout and "wd=0.0001875" in r.stdout
    finally:
        shutil.rmtree(out, ignore_errors=True)

    # Unset is the decay every run before the flag trained under.
    assert Config().weight_decay == 0.003
