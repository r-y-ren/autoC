"""The Kaggle field's exogenous market flow: the second table, and the promise
that adding it moved nothing.

`kagg2_flow` replays one bot's supply mix. This rung replays the *field's* --
twelve Kaggle replays of games our champion lost, twelve different opponents,
measured 2026-08-30 by `scripts/replay_flow.py`. See `kagg3.es.kaggle_flow`'s
module docstring for the measurement and the numbers.

What is asserted here mirrors `tests/test_kagg2_flow.py`, in four parts:

* the **table** loads, is shaped and typed exactly like kagg2's, and its
  per-game season totals are the profiler's own `sellu_*` / `buyprod_*` columns
  (checked against `scripts/replay_profile.py` on one replay when the replays
  are on this machine, and against the hand-checked numbers regardless);
* **off is off** -- a run without `--kaggle-flow` emits the 3-column control
  word, which is the `apply_flow` program that ran before this table existed,
  and a 4-column word pointed at kagg2's table reproduces it to the coin;
* **on is on** -- the table's units reach the market inventory, and they are
  the Kaggle table's units and not kagg2's;
* the **ladder** appends the rung after `kagg2_flow`, so no existing rung index
  or `--rung-weight` changes meaning, and a Trainer carrying both trains.
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

from kagg3 import spec
from kagg3.es import archetypes as AR
from kagg3.es import kagg2_flow as K2F
from kagg3.es import kaggle_flow as KGF
from kagg3.sim import market
from kagg3.sim.state import build_tables, initial_state

#: The replay the profiler cross-check runs on: the smallest of the twelve, so
#: the test costs one JSON parse and two market reconstructions (~3 s).
CHECK_REPLAY = "flow30d_g2520_L_102757134.json"

#: What that replay's opponent seat ("small fry in the underworld", seat 1)
#: actually put on the market, per product, over the season. Hand-checked once
#: against `scripts/replay_profile.py`'s `sellu_<P>` / `buyprod_<P>` columns on
#: 2026-08-30 and pinned here, so the arithmetic is asserted even on a machine
#: that does not carry the 360 MB of replays.
CHECK_SELL = {"WHEAT": 428, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 279,
              "MELON": 102, "EGG": 0, "MILK": 215, "WOOL": 132,
              "FERTILIZER": 217}
CHECK_BUY = {"WHEAT": 183, "FERTILIZER": 0}


def _replay_path():
    """`replays/<CHECK_REPLAY>` at the repo root, or at any parent of it.

    The replays are 360 MB and are not in the repo, so this is allowed to come
    back empty; the parent walk is for a git worktree, whose `ROOT` is three
    levels under the checkout that holds them.
    """
    here = ROOT
    while True:
        p = os.path.join(here, "replays", CHECK_REPLAY)
        if os.path.isfile(p):
            return p
        up = os.path.dirname(here)
        if up == here:
            return None
        here = up


# ---------------------------------------------------------------- the table

def test_table_shape_and_dtype_match_kagg2s():
    for tab in (KGF.KAGGLE_FLOW, KGF.KAGGLE_BUY):
        assert tab.shape == K2F.KAGG2_FLOW.shape == (spec.N_DAYS, spec.N_PRODUCTS)
        assert tab.dtype == K2F.KAGG2_FLOW.dtype == np.int32
        assert (tab >= 0).all()
    assert KGF.RUNG_NAME == "kaggle_flow" != K2F.RUNG_NAME


def test_totals_are_the_tables_own_sums():
    assert KGF.SELL_TOTALS == tuple(int(x) for x in KGF.KAGGLE_FLOW.sum(0))
    assert KGF.BUY_TOTALS == tuple(int(x) for x in KGF.KAGGLE_BUY.sum(0))
    assert KGF.SELL_TOTALS == tuple(KGF.TABLE["sell_totals"])
    assert KGF.BUY_TOTALS == tuple(KGF.TABLE["buy_totals"])
    assert KGF.MAX_DAY_UNITS == int(max(KGF.KAGGLE_FLOW.max(),
                                        KGF.KAGGLE_BUY.max()))


def test_provenance_is_a_field_and_not_a_bot():
    """Twelve games of twelve *different* opponents. That is the whole point:
    a rung averaged over one bot's twelve games is that bot."""
    assert KGF.N_GAMES == 12
    assert len(KGF.SOURCES) == KGF.N_GAMES == len(set(KGF.SOURCES))
    assert len(KGF.OPPONENTS) == KGF.N_GAMES
    assert "OurTeam" not in KGF.OPPONENTS
    assert KGF.MEASURED >= "2026-08-30"


def test_the_mix_is_the_fields_and_not_kagg2s():
    """The table is a different market, and different in the ways the autopsy
    said it would be."""
    ix = spec.ITEM_IX
    assert not np.array_equal(KGF.KAGGLE_FLOW, K2F.KAGG2_FLOW)
    # The field keeps no geese and grows no tomatoes either -- those two
    # markets stay uncontested on Kaggle, which is what the autopsy found.
    assert KGF.KAGGLE_FLOW[:, ix["EGG"]].sum() == 0
    assert KGF.KAGGLE_FLOW[:, ix["TOMATO"]].sum() == 0
    # Wheat is still the only thing bought off the market...
    for i, name in enumerate(spec.PRODUCTS):
        if name != "WHEAT":
            assert KGF.KAGGLE_BUY[:, i].sum() == 0, name
    # ...but the churn is half kagg2's, and the field sells more berries.
    assert KGF.BUY_TOTALS[ix["WHEAT"]] < K2F.BUY_TOTALS[ix["WHEAT"]] / 1.5
    assert KGF.SELL_TOTALS[ix["STRAWBERRY"]] > K2F.SELL_TOTALS[ix["STRAWBERRY"]]
    # It liquidates: the busiest single day in the table is the last one.
    wheat = KGF.KAGGLE_FLOW[:, ix["WHEAT"]]
    assert int(wheat[spec.N_DAYS - 1]) == KGF.MAX_DAY_UNITS
    assert KGF.MAX_DAY_UNITS > K2F.MAX_DAY_UNITS


def test_walk_is_long_enough_for_the_busiest_day_of_either_table():
    """`FLOW_K` serves one program whichever table the control word picks, so
    it has to be sized off the max over both."""
    assert market.FLOW_K == 2 * max(K2F.MAX_DAY_UNITS, KGF.MAX_DAY_UNITS) + 1
    assert market.FLOW_K > 2.0 * KGF.MAX_DAY_UNITS - 1
    assert market.FLOW_K > 2.0 * K2F.MAX_DAY_UNITS - 1


def test_the_stacked_tables_are_the_two_measurements():
    assert market.FLOW_T_KAGG2 == 0 and market.FLOW_T_KAGGLE == 1
    assert np.array_equal(market._FLOW_SELL[market.FLOW_T_KAGG2], K2F.KAGG2_FLOW)
    assert np.array_equal(market._FLOW_SELL[market.FLOW_T_KAGGLE], KGF.KAGGLE_FLOW)
    assert np.array_equal(market._FLOW_BUY[market.FLOW_T_KAGG2], K2F.KAGG2_BUY)
    assert np.array_equal(market._FLOW_BUY[market.FLOW_T_KAGGLE], KGF.KAGGLE_BUY)


# ------------------------------------------------------- against the profiler

def test_one_replay_reproduces_the_hand_checked_totals():
    """`replay_flow.py`'s per-day tables sum to the season totals the profiler
    reports for the same seat -- against `replay_profile.py` itself when the
    replays are on this machine, and against the pinned numbers when they are
    not. The two share `_simulate_market`, so what this pins is that the
    per-day bucketing loses nothing and picks the right seat."""
    path = _replay_path()
    if path is None:
        pytest.skip(f"{CHECK_REPLAY} not on this machine (replays are not "
                    f"in the repo); the pinned totals below still stand")
    import replay_flow as RF

    team, (sell, buy) = RF.opponent_flow(path, "OurTeam")
    assert team != "OurTeam"
    for i, name in enumerate(spec.PRODUCTS):
        assert sum(row[i] for row in sell) == CHECK_SELL[name], name
        assert sum(row[i] for row in buy) == CHECK_BUY.get(name, 0), name

    import replay_profile as RP
    rows = RP.profile_replay(path, "OurTeam")
    opp = [r for r in rows if r["ours"] == 0][0]
    assert opp["team"] == team
    for name in spec.PRODUCTS:
        assert int(opp["sellu_%s" % name]) == CHECK_SELL[name], name
    assert int(opp["buyprod_WHEAT"]) == CHECK_BUY["WHEAT"]


# ---------------------------------------------------------------- off is off

def _blank_state(money=20_000):
    st = initial_state(jnp)
    return st._replace(money=jnp.int32([money, money]))


def test_a_four_wide_word_on_kagg2s_table_is_the_three_wide_word():
    """The table column is a select, not a rewrite: pointed at kagg2 it is the
    program a run without `--kaggle-flow` compiles, to the integer."""
    tables, st, day = build_tables(jnp), _blank_state(), jnp.int32(10)
    three = market.apply_flow(jnp, tables, st, day,
                              jnp.asarray([1, 1000, 0], jnp.int32))
    four = market.apply_flow(
        jnp, tables, st, day,
        jnp.asarray([1, 1000, 0, market.FLOW_T_KAGG2], jnp.int32))
    for a, b in zip(three, four):
        assert np.array_equal(np.asarray(a), np.asarray(b))


def test_the_kaggle_table_moves_the_market_by_its_own_units():
    """Day 10 of each table, side by side: the same day, two markets."""
    tables, st, day = build_tables(jnp), _blank_state(), jnp.int32(10)
    out = market.apply_flow(
        jnp, tables, st, day,
        jnp.asarray([1, 1000, 0, market.FLOW_T_KAGGLE], jnp.int32))
    d_inv = np.asarray(out.mkt_inv) - np.asarray(st.mkt_inv)
    want = (np.asarray(KGF.KAGGLE_FLOW[10], np.int64)
            - np.asarray(KGF.KAGGLE_BUY[10], np.int64))
    # Every unit on this day prices well above the $1 floor, so a sell advances
    # the inventory one for one and the net move is sells minus buys.
    assert np.array_equal(d_inv, want)
    assert not np.array_equal(
        d_inv, np.asarray(K2F.KAGG2_FLOW[10], np.int64)
        - np.asarray(K2F.KAGG2_BUY[10], np.int64))
    # The flow must not touch the other seat.
    assert (np.asarray(out.money) - np.asarray(st.money))[0] == 0


def test_an_off_episode_is_off_whatever_the_table_column_says():
    from kagg3.es.train import flow_control

    w = flow_control([-1, 1], 1234, 5, market.FLOW_T_KAGGLE)
    assert w.shape == (2, 4) and w.dtype == np.int32
    assert list(w[0]) == list(market.FLOW_OFF) + [market.FLOW_T_KAGG2]
    assert list(w[1]) == [1, 1234, 5, market.FLOW_T_KAGGLE]
    # No table asked for is the 3-column word, unchanged.
    assert flow_control([-1, 1], 1234, 5).shape == (2, 3)


# ---------------------------------------------------------------- the ladder

def test_rung_names_appends_kaggle_flow_after_kagg2_flow():
    import train as T

    assert T.rung_names(2) == list(AR.NAMES[:2])
    assert T.rung_names(2, True) == list(AR.NAMES[:2]) + [K2F.RUNG_NAME]
    assert T.rung_names(2, False, True) == list(AR.NAMES[:2]) + [KGF.RUNG_NAME]
    both = T.rung_names(2, True, True)
    assert both == list(AR.NAMES[:2]) + [K2F.RUNG_NAME, KGF.RUNG_NAME]
    # Turning the new rung on moves no existing index, which is what lets an
    # existing `--rung-weight` keep its meaning.
    assert both[:len(T.rung_names(2, True))] == T.rung_names(2, True)
    T.parse_rung_weights([f"{KGF.RUNG_NAME}=3"], both)
    with pytest.raises(SystemExit):
        T.parse_rung_weights([f"{KGF.RUNG_NAME}=3"], T.rung_names(2, True))


def test_the_flags_need_the_rung():
    """A scale or a shift with no rung to shape is a flag the operator believes
    did something. Refused before anything is written, as every other flow
    shaping flag is."""
    import subprocess

    def run(*flags):
        return subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "train.py"),
             "--run", "_kaggle_flag_check", *flags],
            capture_output=True, text=True,
            env=dict(os.environ, JAX_PLATFORMS="cpu"))

    no_rung = run("--kaggle-flow-scale", "0.5:1.5")
    assert no_rung.returncode != 0
    assert "--kaggle-flow-scale without --kaggle-flow" in no_rung.stderr

    bad = run("--kaggle-flow", "--kaggle-flow-scale", "0.5:9.0")
    assert bad.returncode != 0 and "--kaggle-flow-scale 0.5:9.0" in bad.stderr

    weight = run("--rung-weight", f"{KGF.RUNG_NAME}=3")
    assert weight.returncode != 0 and KGF.RUNG_NAME in weight.stderr

    assert not os.path.exists(os.path.join(ROOT, "artifacts", "_kaggle_flag_check"))


def _cfg(**kw):
    from kagg3.es.train import Config
    return Config(pop=2, episodes=4, chunk=4, abs_pairs=2, n_archetypes=2,
                  holdout_rungs=False, kagg2_flow_jitter=0,
                  kagg2_flow_scale=(1.0, 1.0), **kw)


def test_a_trainer_with_both_rungs_runs_a_generation():
    """The two rungs are two extra slots, in order, each at no handicap and
    each alive against the zero theta -- and a generation off that ladder
    completes."""
    import train as T
    from kagg3.es.train import Trainer

    cfg = _cfg(kagg2_flow=True, kaggle_flow=True)
    tr = Trainer(cfg, seed=0)
    assert tr.archetype_names == T.rung_names(2, True, True)
    assert (tr.flow_rung, tr.kaggle_rung) == (2, 3)
    assert tuple(tr.arch_handicap[tr.kaggle_rung]) == AR.NO_HANDICAP
    assert tr.archetype_coins[tr.kaggle_rung] >= AR.MIN_COINS

    # The control word is 4 wide now, and each rung reads its own table.
    n_pairs = 2
    k2 = np.asarray(tr.episode_flow(n_pairs,
                                    np.full(n_pairs, len(tr.pool) + tr.flow_rung)))
    kg = np.asarray(tr.episode_flow(n_pairs,
                                    np.full(n_pairs, len(tr.pool) + tr.kaggle_rung)))
    assert k2.shape == kg.shape == (2 * n_pairs, 4)
    assert list(k2[:, 0]) == list(kg[:, 0]) == [1, 0, 1, 0]
    assert (k2[:, 3] == market.FLOW_T_KAGG2).all()
    assert (kg[:, 3] == market.FLOW_T_KAGGLE).all()
    off = np.asarray(tr.episode_flow(n_pairs, np.zeros(n_pairs, int)))
    assert (off == np.asarray(tuple(market.FLOW_OFF) + (market.FLOW_T_KAGG2,),
                              np.int32)).all()

    mean, best, abs_coins, rep = tr.generation()
    assert np.isfinite(mean) and np.isfinite(best)


def test_kaggle_flow_alone_is_a_ladder_too():
    """The rungs are independent: `--kaggle-flow` without `--kagg2-flow` is a
    one-flow-rung ladder whose table is the field's."""
    from kagg3.es.train import Trainer

    tr = Trainer(_cfg(kaggle_flow=True), seed=0)
    assert tr.archetype_names[-1] == KGF.RUNG_NAME
    assert (tr.flow_rung, tr.kaggle_rung) == (-1, 2)
    w = np.asarray(tr.episode_flow(2, np.full(2, len(tr.pool) + tr.kaggle_rung)))
    assert w.shape == (4, 4) and (w[:, 3] == market.FLOW_T_KAGGLE).all()
    assert list(w[:, 0]) == [1, 0, 1, 0]


def test_no_flag_is_no_rung_and_the_word_the_run_always_had():
    """A run with only `--kagg2-flow` emits the 3-column word -- the same
    `apply_flow` program, not a defaulted column -- and a run with neither flag
    emits none at all."""
    from kagg3.es.train import Trainer

    tr = Trainer(_cfg(kagg2_flow=True), seed=0)
    assert KGF.RUNG_NAME not in tr.archetype_names
    assert tr.kaggle_rung == -1
    w = np.asarray(tr.episode_flow(2, np.full(2, len(tr.pool) + tr.flow_rung)))
    assert w.shape == (4, 3)
    assert np.asarray(tr.flow_words(np.ones(4, bool), np.zeros(4, np.int32),
                                    table=market.FLOW_T_KAGGLE)).shape == (4, 3)

    plain = Trainer(_cfg(), seed=0)
    assert (plain.flow_rung, plain.kaggle_rung) == (-1, -1)
    assert plain.flow_words(np.zeros(4, bool), np.zeros(4, np.int32)) is None
    assert plain.episode_flow(2, np.zeros(2, int)) is None


# ------------------------------------------- where the gradient's family sits

def _flow_trainer(seed=7, **cfg):
    """A `Trainer` carrying only what `episode_flow` reads, as in
    `tests/test_kagg2_flow.py` -- building the ladder to find out which numbers
    come off `self.rng` would spend a minute of archetype probing."""
    from kagg3.es.train import Config, Trainer

    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(**dict({"kagg2_flow": True, "kaggle_flow": True}, **cfg))
    tr.pool = []
    tr.flow_rung = 0 if tr.cfg.kagg2_flow else -1
    tr.kaggle_rung = 1 if tr.cfg.kaggle_flow else -1
    tr.rng = np.random.default_rng(seed)
    return tr


def test_the_kaggle_rung_shares_the_kagg2_familys_ranges_by_default():
    """Unset means *share*, not "some other default": the two rungs are the
    same kind of randomisation and there is no reason to state it twice."""
    n = 64
    tr = _flow_trainer(kagg2_flow_shift=(0, 4), kagg2_flow_scale=(1.2, 1.4))
    w = np.asarray(tr.episode_flow(n, np.ones(n, int)))   # every pair is kaggle
    assert (w[:, 3] == market.FLOW_T_KAGGLE).all()
    assert w[:, 2].min() >= 0 and w[:, 2].max() <= 4
    assert 1200 <= w[:, 1].min() and w[:, 1].max() <= 1400
    # A pair's two seats still share one draw.
    assert (w[0::2, 1] == w[1::2, 1]).all() and (w[0::2, 2] == w[1::2, 2]).all()


def test_its_own_ranges_apply_to_it_alone():
    n = 64
    tr = _flow_trainer(kagg2_flow_shift=(0, 0), kagg2_flow_scale=(1.0, 1.0),
                       kaggle_flow_shift=(3, 3), kaggle_flow_scale=(1.5, 1.5))
    kg = np.asarray(tr.episode_flow(n, np.ones(n, int)))
    assert (kg[:, 1] == 1500).all() and (kg[:, 2] == 3).all()
    k2 = np.asarray(tr.episode_flow(n, np.zeros(n, int)))
    assert (k2[:, 1] == 1000).all() and (k2[:, 2] == 0).all()
    assert (k2[:, 3] == market.FLOW_T_KAGG2).all()


def test_the_kaggle_draws_come_after_the_kagg2_ones():
    """A run without the second rung has to see the RNG stream it always saw:
    the kagg2 pair is drawn first, so it is a prefix either way."""
    from kagg3.es.train import Config

    n = 5
    both = np.asarray(_flow_trainer().episode_flow(n, np.zeros(n, int)))
    only = np.asarray(_flow_trainer(kaggle_flow=False)
                      .episode_flow(n, np.zeros(n, int)))
    assert both.shape == (2 * n, 4) and only.shape == (2 * n, 3)
    # Same kagg2 levels on the kagg2 rung, drawn off the same first two calls.
    assert np.array_equal(both[:, :3], only)

    ref = np.random.default_rng(7)
    lo, hi = Config().kagg2_flow_scale
    scale = np.rint(ref.uniform(lo, hi, n) * 1000).astype(np.int32)
    shift = ref.integers(-2, 3, n).astype(np.int32)
    assert list(only[:, 1]) == list(np.repeat(scale, 2))
    assert list(only[:, 2]) == list(np.repeat(shift, 2))
