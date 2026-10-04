"""The planner-side section-7 metrics, replayed through one real engine game.

The submission's runtime calls its macro function exactly once per morning,
with the `DayView` it is about to hand `plan.build_day`. `collect` sits on
that hook, so `build_day_stats` sees the very view the plan was built from --
no second parse, no second model of the day -- and the game itself is
unchanged.

    python scripts/plan_stats.py --seed 7 --theta artifacts/theta.npy
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, "src")
import numpy as np

from kagg3.core.plan import DayStats

THETA_PATH = os.path.join("artifacts", "theta.npy")
FIELDS = DayStats._fields


def make_macro(theta):
    """The submission's own macro: decode `theta` against the engine obs."""
    from kagg3.agent import parse
    from kagg3.core import brain

    def macro(obs, player, view, prev_mkt_inv=None):
        opp = obs["farms"][1 - player]
        vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
        po = brain.PolicyObs(
            day=np.int32(view.day), money=view.money, opp_money=np.int32(opp["money"]),
            kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
            t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
            nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
            mkt_inv=parse.parse_market(obs)[0], price=view.price,
            shops=parse.parse_town(obs),
            opp_t_day=vo.t_day, opp_t_yield=vo.t_yield,
            prev_mkt_inv=prev_mkt_inv)
        return brain.decide(np, theta, po)

    return macro


def collect(macro_fn, out):
    """Wrap a macro function so each planned day's `DayStats` lands in `out`."""
    from kagg3.core import plan as P

    def macro(obs, player, view, prev_mkt_inv=None):
        m = macro_fn(obs, player, view, prev_mkt_inv)
        out.append(P.build_day_stats(view, m))
        return m

    return macro


def totals(days):
    """The per-game sums of `collect`'s output, in `DayStats` field order."""
    return tuple(int(sum(int(getattr(d, f)) for d in days)) for f in FIELDS)


def replay(seed, theta_path, opponent="starter", seat=0):
    """Play one game with `theta` in `seat` and return the three sums."""
    from kaggle_environments import make

    from kagg3.agent import runtime

    theta = np.load(theta_path).astype(np.float32)
    days = []
    me = runtime.make_agent(collect(make_macro(theta), days), pass_prev_mkt_inv=True)
    env = make("kaggriculture", configuration={"seed": int(seed)})
    env.run([me, opponent] if seat == 0 else [opponent, me])
    return totals(days)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default=THETA_PATH)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--opponent", default="starter")
    ap.add_argument("--seat", type=int, choices=(0, 1), default=0)
    args = ap.parse_args()

    sums = replay(args.seed, args.theta, args.opponent, args.seat)
    print(f"seed={args.seed} seat={args.seat} vs {args.opponent}  theta={args.theta}")
    for name, v in zip(FIELDS, sums):
        print(f"  {name:20s} {v:10d}")
