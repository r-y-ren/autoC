"""ACTOBS1 [plan.RL_ACT_ON]: the live agent fills `plan.RL_ACT_OBS` exactly as the run3 rollout measures it.

Agent side: `kagg3.agent.tell.ActObs`, driven by `agent.runtime.Runtime.act` (record every turn, dawn at hour 0).
Rollout side: `S/rlfast1/actobs_roll.RollObs`, driven the way `S/rlfast1/ppo_fast.play` drives it (dawn arrays +
the `v56sim.encode` rows both seats presented, hands before the turn). Engine games, both seats our runtime:
every day d >= 1 of every seat must agree to the int; day 0 is (0, 0) on both sides.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

from kagg3 import spec
from kagg3.agent import parse, runtime, tell
from kagg3.core import brain
from kagg3.core import plan as P

ROOT = Path(__file__).resolve().parents[1]
for _p in ("S/simv56", "S/rlfast1"):
    if str(ROOT / _p) not in sys.path:
        sys.path.insert(0, str(ROOT / _p))
import v56sim as V  # noqa: E402
import actobs_roll as AR  # noqa: E402

_TH = ROOT / "S/winjudge/ship7692/theta7659.npy"
THETA = np.load(_TH if _TH.exists() else ROOT / "submission/theta.npy").astype(np.float32)
SEEDS = (11, 2104521678, 1164543749)


def _macro(obs, player, view, prev_mkt_inv):
    """submission/main.py's `_macro`, verbatim in substance."""
    opp = obs["farms"][1 - player]
    vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
    return brain.decide(np, THETA, brain.PolicyObs(
        day=np.int32(view.day), money=view.money, opp_money=np.int32(opp["money"]),
        kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
        t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
        nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
        mkt_inv=parse.parse_market(obs)[0], price=view.price, shops=parse.parse_town(obs),
        opp_t_day=vo.t_day, opp_t_yield=vo.t_yield, prev_mkt_inv=prev_mkt_inv))


def _game(monkeypatch, seed, steps=None):
    """One engine game, both seats our Runtime. -> (turn log, per-seat {day: RL_ACT_OBS seen by build_day}, rts)."""
    from kaggle_environments import make
    seen = {}
    real = P.build_day

    def spy(*a, **k):
        seen["v"] = tuple(int(x) for x in P.RL_ACT_OBS)
        return real(*a, **k)
    monkeypatch.setattr(P, "build_day", spy)
    rts = {0: runtime.Runtime(_macro, pass_prev_mkt_inv=True), 1: runtime.Runtime(_macro, pass_prev_mkt_inv=True)}
    log, fed = [], {0: {}, 1: {}}

    def agent(obs, config=None):
        o = json.loads(json.dumps(obs))      # the observation as presented, frozen before the turn
        p = int(o.get("player", 0))
        seen.pop("v", None)
        act = rts[p].act(obs)
        if int(o["hour"]) == 0:
            fed[p][int(o["day"])] = seen.get("v")
        log.append((p, o, json.loads(json.dumps(act))))
        return act
    cfg = {"seed": int(seed), "actTimeout": 600, "runTimeout": 10 ** 6}
    if steps:
        cfg["episodeSteps"] = int(steps)
    env = make("kaggriculture", configuration=cfg)
    env.run([agent, agent])
    return log, fed, rts


def _rollout(log):
    """RollObs over the game's per-step arrays, called in ppo_fast.play's order -> {day: rlx [seat, 2]}."""
    by_step = {}
    for p, o, act in log:
        by_step.setdefault(int(o["day"]) * spec.TURNS_PER_DAY + int(o["hour"]), {})[p] = (o, act)
    ro, out = AR.RollObs(1), {}
    for step in sorted(by_step):
        seats = by_step[step]
        assert set(seats) == {0, 1}, step
        o0 = seats[0][0]
        d, h = int(o0["day"]), int(o0["hour"])
        if h == 0:
            inv = np.array([[o0["market"]["inventory"][n] for n in spec.PRODUCTS]])
            out[d] = ro.dawn(d, inv, V._counts(o0["town"]["unlocked_shops"])[None, :])[0]
        vu = np.zeros((1, 2, 3, spec.MAX_UNITS), np.int32)
        vm = np.zeros((1, 2, 3, spec.MAX_MARKET_ORDERS), np.int32)
        nh = np.zeros((1, 2), np.int64)
        for p in (0, 1):
            o, act = seats[p]
            vu[0, p], vm[0, p] = V.encode(act)
            nh[0, p] = len(o["farms"][p]["hands"])
        ro.turn(vu, vm, nh)
    return out


def test_parity_three_engine_games(monkeypatch):
    monkeypatch.setattr(P, "RL_ACT_ON", True)
    n_days = nz_pass = nz_riv = buy_days = 0
    diffs = []
    for seed in SEEDS:
        log, fed, _ = _game(monkeypatch, seed)
        roll = _rollout(log)
        assert sorted(roll) == list(range(spec.N_DAYS))
        for p in (0, 1):
            assert fed[p][0] == (0, 0) and tuple(roll[0][p]) == (0, 0)
            for d in range(1, spec.N_DAYS):
                agent_v, roll_v = fed[p][d], tuple(int(x) for x in roll[d][p])
                assert agent_v == roll_v, (seed, p, d, agent_v, roll_v)
                n_days += 1
                nz_pass += agent_v[0] > 0
                nz_riv += agent_v[1] != 0
        # how far the observable NET sits from the rival's own ordered wheat (both seats are ours here)
        for p in (0, 1):
            for d in range(1, spec.N_DAYS):
                s = b = 0
                for q, o, act in log:
                    if q == 1 - p and int(o["day"]) == d - 1:
                        s1, b1 = tell.wheat_orders(act.get("market"))
                        s, b = s + s1, b + b1
                buy_days += b > 0
                diffs.append(fed[p][d][1] - s)
    print(f"ACTOBS parity: {n_days} seat-days equal; pass>0 {nz_pass}, riv!=0 {nz_riv}; rival-buy days {buy_days}; "
          f"riv - rival ordered sells: mean {np.mean(diffs):+.2f} |max| {np.max(np.abs(diffs))} "
          f"exact {int(np.sum(np.asarray(diffs) == 0))}/{len(diffs)}")
    assert n_days == 3 * 2 * (spec.N_DAYS - 1) and nz_pass > 0 and nz_riv > 0


def test_off_byte_identical(monkeypatch):
    """OFF: the tracker is never built or called and RL_ACT_OBS stays (0, 0); ON (no head = zero action) presents
    the same actions turn for turn, so the tracker itself never moves play."""
    steps = 4 * spec.TURNS_PER_DAY + 1

    class Boom:
        def __init__(self, *a, **k):
            raise AssertionError("ActObs built with RL_ACT_ON off")
    assert P.RL_ACT_ON is False
    with monkeypatch.context() as m:
        m.setattr(tell, "ActObs", Boom)
        log_off, fed_off, rts = _game(m, SEEDS[0], steps)
    assert all(rt.actobs is None for rt in rts.values())
    assert all(v == (0, 0) for p in (0, 1) for v in fed_off[p].values())
    with monkeypatch.context() as m:
        m.setattr(P, "RL_ACT_ON", True)
        log_on, fed_on, _ = _game(m, SEEDS[0], steps)
    assert len(log_on) == len(log_off) > 2 * 3 * spec.TURNS_PER_DAY
    assert [a for _, _, a in log_on] == [a for _, _, a in log_off]
    assert any(v != (0, 0) for p in (0, 1) for v in fed_on[p].values())
