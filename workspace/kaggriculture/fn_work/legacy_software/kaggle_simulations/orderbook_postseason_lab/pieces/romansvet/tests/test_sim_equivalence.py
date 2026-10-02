"""Release gate 1: the JAX simulator reproduces kaggle_environments exactly.

Compares every state field, not just the reward, so a divergence that happens to
be reward-neutral still fails.
"""
import functools
import os
import sys

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from kaggle_environments import make

from kagg3 import spec
from kagg3.agent import parse, runtime
from kagg3.core import brain, plan as P, policy as PO
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables, initial_state

FIELDS = ["kind", "occ", "t_day", "t_water", "t_cons", "t_yield",
          "t_fert", "t_cared", "t_favail"]

# `t_life` and `t_bank` are checked against the raw engine tiles rather than
# through `parse.parse_view`. `DayView` has no `t_life` at all -- the planner
# never reads it, so `parse_view` has no field to hand back -- and it gained
# `t_bank` only in 0fc054d (filled from `pending_care_bonus`), long after
# FIELDS was built from what the view exposed, which is why both state fields
# went unchecked while the docstring claimed every one was compared. Reading
# the tile keeps the check independent of `parse_view`. Both drive future
# evolution (t_life expires plants in decay_plants, t_bank is the pending care
# bonus), so a mismatch is silent on the day it happens and compounds after.
EXTRA_FIELDS = ["t_life", "t_bank"]


@pytest.mark.parametrize("day_tiles", [False, True])
def test_episode_carries_previous_dawn_through_final_day(monkeypatch, day_tiles):
    """Exercise the actual JAX day scan without compiling the game mechanics."""
    def advance(tables, st, day, words, hi_t, lo_t, thetas, *,
                prev_mkt_inv, day_metrics, n_turns=24, do_eod=True, **kwargs):
        # Day d opens after a synthetic draw of d units on the preceding day.
        # A missing, current-day, or two-day-old history produces a cash error.
        error = jnp.sum(jnp.abs(prev_mkt_inv - st.mkt_inv - day))
        out = st._replace(mkt_inv=st.mkt_inv - day - 1,
                          money=st.money + error,
                          step=st.step + n_turns)
        assert do_eod == (n_turns == 24)
        return (out, jnp.zeros(2, jnp.int32)) if day_metrics else out

    monkeypatch.setattr(rollout, "run_day", advance)
    result = rollout.episode(None, None, jnp.zeros((30, 1), jnp.uint32),
                             None, None, day_tiles=day_tiles)
    initial = initial_state(jnp)
    np.testing.assert_array_equal(result[0], initial.money)
    np.testing.assert_array_equal(result[1], np.broadcast_to(initial.money, (30, 2)))
    assert int(result[2].step) == 29 * 24 + 23


def _engine_tile_extra(obs, p):
    """t_life / t_bank per tile, in raw row-major order to match sim state."""
    life = np.full(spec.N_TILES, -1, np.int32)
    bank = np.zeros(spec.N_TILES, np.int32)
    for y, row in enumerate(obs["farms"][p]["tiles"]):
        for x, t in enumerate(row):
            if isinstance(t, dict):
                i = y * spec.BOARD + x
                life[i] = t.get("max_lifespan_step", -1)
                bank[i] = t.get("pending_care_bonus", 0)
    return life, bank


def agent_for(theta):
    def f(obs, player, view):
        farm_o = obs["farms"][1 - player]
        vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
        po = brain.PolicyObs(
            day=np.int32(view.day), money=view.money,
            opp_money=np.int32(farm_o["money"]),
            kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
            t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
            nquad=view.nquad, opp_nquad=np.int32(len(farm_o["unlocked_quadrants"])),
            mkt_inv=parse.parse_market(obs)[0], price=view.price,
            shops=parse.parse_town(obs),
            # Public board state, and the sim seat passes it, so the engine
            # seat has to as well or the two forecasts differ.
            opp_t_day=vo.t_day, opp_t_yield=vo.t_yield)
        return brain.decide(np, theta, po)
    return runtime.make_agent(f)


def _engine(env, step_ix):
    st = env.steps[step_ix]
    obs = st[0].observation
    farms = obs["farms"]
    out = {"money": np.array([f["money"] for f in farms]),
           "mkt_inv": np.array([obs["market"]["inventory"][n] for n in spec.PRODUCTS]),
           "nquad": np.array([len(f["unlocked_quadrants"]) for f in farms]),
           "nshops": np.array(len(obs["town"]["unlocked_shops"]))}
    inv = np.argsort(P.SERP)
    per = {f: [] for f in FIELDS}
    for p in range(2):
        v = parse.parse_view({**obs, "private": st[p].observation["private"]}, p)
        for f in FIELDS:
            per[f].append(getattr(v, f)[inv])
        out[f"shed{p}"] = v.shed
        out[f"seeds{p}"] = v.seeds
    for f in FIELDS:
        out[f] = np.array(per[f])
    extra = [_engine_tile_extra(obs, p) for p in range(2)]
    out["t_life"] = np.array([e[0] for e in extra])
    out["t_bank"] = np.array([e[1] for e in extra])
    return out


def _sim(st):
    out = {"money": np.asarray(st.money), "mkt_inv": np.asarray(st.mkt_inv),
           "nquad": np.asarray(st.nquad), "nshops": np.asarray(st.nshops),
           "shed0": np.asarray(st.shed[0]), "shed1": np.asarray(st.shed[1]),
           "seeds0": np.asarray(st.seeds[0]), "seeds1": np.asarray(st.seeds[1])}
    for f in FIELDS + EXTRA_FIELDS:
        out[f] = np.asarray(getattr(st, f))
    return out


@pytest.mark.parametrize("seed,theta_seed", [
    (20260821, 3), (20260821, 11), (7, 0), (999_999, 5), (42, 17),
])
def test_sim_matches_engine(seed, theta_seed):
    theta = PO.init_theta(np.random.default_rng(theta_seed))
    _compare_season(theta, seed)


def _compare_season(theta, seed):
    """Play one season in both, compare every state field at every day boundary.

    Returns the engine's per-day hand count, so a caller can assert what the
    season actually exercised rather than hoping for it.
    """
    tables = build_tables(jnp)
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([agent_for(theta), agent_for(theta)])

    hi_t, lo_t = eod.weed_threshold()
    hi_t, lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
    thetas = jnp.stack([jnp.asarray(theta)] * 2)
    run_day = jax.jit(functools.partial(rollout.run_day, tables))
    run_last = jax.jit(functools.partial(rollout.run_day, tables,
                                         n_turns=spec.TURNS_PER_DAY - 1, do_eod=False))

    st = initial_state(jnp)
    for d in range(spec.N_DAYS):
        f = run_last if d == spec.N_DAYS - 1 else run_day
        st = f(st, jnp.int32(d), jnp.asarray(eod.host_stream(seed, d)), hi_t, lo_t, thetas)
        e, s = _engine(env, min((d + 1) * 24, len(env.steps) - 1)), _sim(st)
        for k in s:
            assert np.array_equal(np.asarray(e[k]), np.asarray(s[k])), \
                f"day {d}: field {k} diverged\nengine={e[k]}\nsim={s[k]}"
    return _hands_per_day(env)


def _hands_per_day(env):
    """Hands each seat holds at hour 4 -- after both HIRE rows have resolved
    (turns 0 and 2) and before anything can escape."""
    return [[len(env.steps[min(d * 24 + 4, len(env.steps) - 1)][0]
                 .observation["farms"][p]["hands"]) for d in range(spec.N_DAYS)]
            for p in range(2)]


def _wide_crew_theta():
    """A theta whose seasons really do hire past ten hands.

    Random weights barely develop a farm, so none of the cases above ever put
    more than a handful of hands on the board -- the second HIRE row, the late
    route base and every `MAX_UNITS`-shaped array in the state would go
    unexercised by gate 1 exactly where they are newest. This one develops
    every free tile (`dev_frac -> 1`), splits it evenly between crops and
    animals (`animal_share -> 0.5`), buys land whenever it can afford it, and
    liquidates rather than holding (a low sell score) so the coins come back
    to pay for the next quadrant. `gh` is zero at these weights, so the head is
    its bias exactly and the decode is the four numbers set here.
    """
    theta = np.zeros(PO.N_PARAMS, np.float32)
    gb2 = PO.offset("gb2")
    theta[gb2 + 1] = 8.0        # land bias, saturated positive
    theta[gb2 + 5] = 8.0        # dev_frac -> 1
    theta[gb2 + 6] = 0.0        # animal_share -> 1/2
    theta[PO.offset("b2") + 1] = -4.0    # sell score low -> reservation near zero
    return theta


@pytest.mark.parametrize("seed", [1164543749, 20260821])
def test_sim_matches_engine_with_a_wide_crew(seed):
    """Gate 1 on a season that hires past the old ten-hand ceiling.

    The engine caps nothing and the HIRE rows are split over turns 0 and 2, so
    a day can field up to seventeen units -- which changes the spawn walk, the
    per-unit route base, the `MAX_UNITS`-shaped inventory arrays and the
    end-of-day drop order. The assertion on the hand count is the point: it
    fails loudly if this season stops exercising a wide crew instead of
    quietly re-testing the narrow one.
    """
    hands = _compare_season(_wide_crew_theta(), seed)
    peak = max(max(h) for h in hands)
    assert peak >= 12, f"season never hired a wide crew (peak {peak})"
    assert peak <= spec.MAX_HANDS
