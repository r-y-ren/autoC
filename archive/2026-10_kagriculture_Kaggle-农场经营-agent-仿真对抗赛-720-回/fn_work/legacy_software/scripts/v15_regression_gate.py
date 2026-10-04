# 【中文】v15_regression_gate.py —— v15 波次剧本回归门（M-E3）
# ===========================================================================
# 判据（任务包 M-E3）：我方本地池 + round20-24 回放注入回归——
#   * 不塌方：注入 26 局中 reward < 45k 的局数 ≤ 2；
#   * escape 0：placed 畜群逐日递减（引擎无卖畜 → 递减即逃亡）计数 0；
#   * overflow 0：日终 shed+随身 ≥ 98（100 销毁悬崖警戒带）的天数 0
#     （销毁静默发生，EOD 满仓为工程代理口径，输出里如实标注）。
# 两个口径：
#   A 本地池哨兵（官方引擎 arena）：wave-forced 候选 vs cow_baron /
#     melon_hoarder / expansionist / baseline_wheat，seeds 101-104 双席位
#     ——候选对本地池不允许出现败局塌方（本地池弱于 v48，胜率本身无线上
#     预测力，只作"引擎在环不崩"的回归面）。
#   B 回放注入（孪生）：rounds 20-24 可评局（确定性序，≤26）wave 变体
#     d0 全季 rollout（对手=回放真实动作），测塌方/逃亡/满仓。
# 输出：exports/probes/v15_ignition/v15_regression_gate.json
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
ROOT = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kgenv.arena import (SUBMISSION_MAIN, episode_contract_ok,  # noqa: E402
                         load_submission_agent, run_episode)
from kgenv.bots.baseline import baseline_wheat_agent      # noqa: E402
from kgenv.bots.cow_baron import cow_baron_agent          # noqa: E402
from kgenv.bots.expansionist import expansionist_agent    # noqa: E402
from kgenv.bots.melon_hoarder import melon_hoarder_agent  # noqa: E402

import planner_offline_bench as bench                      # noqa: E402

OUT = os.path.join(SOFTWARE, "exports", "probes", "v15_ignition",
                   "v15_regression_gate.json")
POOL = {"cow_baron": cow_baron_agent, "melon_hoarder": melon_hoarder_agent,
        "expansionist": expansionist_agent,
        "baseline_wheat": baseline_wheat_agent}
POOL_SEEDS = (101, 102, 103, 104)
WAVE_OVERRIDES = {"PLANNER_ENABLED": True,
                  "PLANNER_OVERRIDES.wave_mode": True}
SHED_DANGER = 98
COLLAPSE_FLOOR = 45000.0


def load_wave_forced():
    import importlib.util
    path = os.path.abspath(SUBMISSION_MAIN)
    spec = importlib.util.spec_from_file_location("v15_regression_candidate",
                                                  path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PLANNER_ENABLED = True
    module.PLANNER_OVERRIDES["wave_mode"] = True
    return module.agent


def run_pool():
    agent_fn = load_wave_forced()
    games = []
    for name, bot in sorted(POOL.items()):
        for seed in POOL_SEEDS:
            for seat in (0, 1):
                if seat == 0:
                    res = run_episode(agent_fn, bot, seed, collect_daily=False)
                else:
                    res = run_episode(bot, agent_fn, seed, collect_daily=False)
                mine = float(res["rewards"][seat])
                games.append({
                    "opponent": name, "seed": seed, "our_seat": seat,
                    "our_money": mine, "opp_money": float(res["rewards"][1 - seat]),
                    "win": mine > float(res["rewards"][1 - seat]),
                    "contract_ok": episode_contract_ok(res),
                })
                print(f"[pool] {name} seed={seed} seat={seat} "
                      f"ours={mine:.0f} {'WIN' if games[-1]['win'] else 'LOSS'}",
                      flush=True)
    return games


def rollout_track(deps, replay, me_seat, overrides):
    """d0 全季 rollout + 逃亡/满仓代理计数（循环与 bench 同构）。"""
    agent_fn, _a, _s = deps["v13_factory"](overrides)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    me_seat = int(me_seat)
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    prev_herd = None
    escapes = 0
    shed_danger_days = 0
    daily = []
    while not state.env.done and taken < len(acts) and taken < max_steps:
        obs = state.seats[me_seat].observation
        mine = agent_fn(obs)
        theirs = acts[taken][1 - me_seat]
        deps["step"](state, [mine, theirs])
        taken += 1
        if taken % 24 == 0:
            farms = state.seats[0].observation.farms
            farm = farms[me_seat]
            herd = 0
            for row in farm.get("tiles") or []:
                for tile in row or []:
                    if isinstance(tile, dict) and "animal" in tile:
                        herd += 1
            private = state.seats[me_seat].observation.private or {}
            shed = private.get("shed") or {}
            shed_n = sum(int(v) for v in shed.values()
                         if isinstance(v, (int, float)) and v > 0)
            carried = sum(int(n) for inv in (private.get("inventories") or [])
                          if inv for n in inv.values()
                          if isinstance(n, (int, float)) and n > 0)
            if prev_herd is not None and herd < prev_herd:
                escapes += prev_herd - herd
            prev_herd = herd
            if shed_n + carried >= SHED_DANGER:
                shed_danger_days += 1
            daily.append(float(farm.get("money", 0.0) or 0.0))
    final = deps["final"](state)
    return float(final[me_seat]), daily, escapes, shed_danger_days


def run_injections(limit=26):
    deps = bench.make_twin_deps()
    evaluable, skipped = bench.find_episodes(
        os.path.join(ROOT, "references", "data", "online-replays"),
        ("round20", "round21", "round22", "round23", "round24"), limit,
        "renyxin")
    rows = []
    for item in evaluable:
        t0 = time.time()
        with open(item["path"], "r", encoding="utf-8") as h:
            replay = json.load(h)
        truth_me = float(replay["rewards"][item["me_seat"]])
        base_final, _bd, b_esc, b_danger = rollout_track(
            deps, replay, item["me_seat"], None)
        wave_final, daily, escapes, shed_danger = rollout_track(
            deps, replay, item["me_seat"], WAVE_OVERRIDES)
        rows.append({
            "episode": item["episode"], "round": item["round"],
            "opponent": item["opponent"], "truth_me": truth_me,
            "base_final": round(base_final, 1),
            "wave_final": round(wave_final, 1),
            "delta_vs_base": round(wave_final - base_final, 1),
            "collapse": wave_final < COLLAPSE_FLOOR,
            "base_collapse": base_final < COLLAPSE_FLOOR,
            "escape_events": escapes, "shed_danger_days": shed_danger,
            "base_escape_events": b_esc, "base_shed_danger_days": b_danger,
            "wall_s": round(time.time() - t0, 1),
        })
        print(f"[inject] r{item['round']} ep{item['episode']} "
              f"truth {truth_me:8.0f} base {base_final:8.0f} "
              f"wave {wave_final:8.0f} esc={escapes} danger={shed_danger} "
              f"[{rows[-1]['wall_s']}s]", flush=True)
    return rows, skipped


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-pool", action="store_true")
    ap.add_argument("--injections", type=int, default=26)
    args = ap.parse_args()
    t0 = time.time()
    pool = [] if args.skip_pool else run_pool()
    injections, skipped = run_injections(args.injections)
    collapses = [r for r in injections if r["collapse"]]
    escapes_total = sum(r["escape_events"] for r in injections)
    danger_total = sum(r["shed_danger_days"] for r in injections)
    out = {
        "protocol": "v15-regression-gate/1.1",
        "pool": {"games": pool,
                 "losses": sum(1 for g in pool if not g["win"]),
                 "contract_fail": sum(1 for g in pool
                                      if not g["contract_ok"])},
        "injections": {"rows": injections, "n": len(injections),
                       "skipped": skipped,
                       "collapses": [r["episode"] for r in collapses],
                       "n_collapses": len(collapses),
                       "base_collapses": sum(1 for r in injections
                                             if r["base_collapse"]),
                       "wave_worse_than_base": sum(1 for r in injections
                                                   if r["delta_vs_base"] < 0),
                       "escape_events_total": escapes_total,
                       "base_escape_events_total": sum(
                           r["base_escape_events"] for r in injections),
                       "shed_danger_days_total": danger_total,
                       "base_shed_danger_days_total": sum(
                           r["base_shed_danger_days"] for r in injections),
                       "shed_danger_note": "overflow 为静默销毁的工程代理："
                                           "EOD shed+随身 ≥98 警戒带天数"},
        "gates": {
            "pool_no_contract_fail": all(g["contract_ok"] for g in pool)
            if pool else True,
            "collapse_le_2_of_26": len(collapses) <= 2
            and len(injections) >= 20,
            "escape_0": escapes_total == 0,
            "overflow_0_proxy": danger_total == 0,
        },
        "wall_total_s": round(time.time() - t0, 1),
    }
    out["all_passed"] = all(out["gates"].values())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    print(json.dumps({"gates": out["gates"],
                      "all_passed": out["all_passed"]}, ensure_ascii=False))
    print(f"out -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
