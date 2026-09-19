# 【中文】round23_dtsp_engagement_probe.py —— DTSP 线上接合判定探针
# ===========================================================================
# 问题：round-23 线上各局，DTSP 覆盖是否真的生效？
# 判据：孪生内反应式（v13.8 无覆盖，对手=回放真实动作）从注入步推进到
#   终局，若 |reactive_final − truth| < 1.0（逐位一致带），则线上该局从
#   该黎明起的动作流与纯 v13.8 逐位一致 → DTSP 覆盖在该黎明后无行为差异
#   （未接合或选中计划与默认动作等价）；若显著偏离 → DTSP 在线生效。
# 口径注记：注入黎明之前的历史仍是线上真实轨迹（含 DTSP 已有影响）；
#   本探针判定的是"该黎明之后"的接合状态。d3/d10 双黎明窗采样。
# 只读探针；输出 stdout + probes JSON。
# ===========================================================================

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402
from kaggle_simulations.agent.planner import plans, select  # noqa: E402
from kaggle_simulations.agent.planner import opponents      # noqa: E402

REPLAY_DIR = os.path.join(SOFTWARE, "..", "references", "data",
                          "online-replays", "round23")
OUT = os.path.join(SOFTWARE, "exports", "probes", "round23_forensics",
                   "dtsp_engagement.json")
TEAM = "renyxin"
DAWNS = (3, 10, 20)
EPS = 1.0


def main():
    files = sorted(f for f in os.listdir(REPLAY_DIR)
                   if f.startswith("episode-") and f.endswith(".json"))
    deps = bench.make_twin_deps()
    rows = []
    for fn in files:
        with open(os.path.join(REPLAY_DIR, fn), "r", encoding="utf-8") as h:
            replay = json.load(h)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        if TEAM not in teams or teams[0] == teams[1]:
            continue
        me = teams.index(TEAM)
        truth = [float(x) for x in replay["rewards"]]
        acts = deps["transition_actions"](replay)
        rec = {"episode": os.path.splitext(fn)[0].replace("episode-", ""),
               "opponent": teams[1 - me], "margin": round(truth[me] - truth[1 - me]),
               "dawns": {}}
        for day in DAWNS:
            step = min(day * 24, len(acts) - 2)
            state = deps["build"](replay, step)
            agent_fn, _a, _s = deps["v13_factory"](None)
            final, _taken = bench.rollout_with_replay_opponent(
                deps, state, me, agent_fn, acts, step)
            diff = abs(float(final[me]) - truth[me])
            # 该黎明的投影选择（离线同机制重建）
            obs = bench.build_obs_summary_from_state(deps, state, me, day)
            hist = bench.extract_opponent_history(replay, 1 - me, step)
            models = opponents.build_default_models(
                history=hist, profile_path=None,
                pessimistic=opponents.PessimisticFill(price_discount=0.75))
            cands = plans.enumerate_plans(obs)
            jm = {s.key(): {m.name: plans.project_season(
                    s, obs, m.supply_pressure(obs)) for m in models}
                  for s in cands}
            sel = select.robust_select(jm, strategy="trimmed_mean")
            best = bench._spec_by_key(cands, sel["best"])
            ovr = plans.plan_to_knob_overrides(best)
            quota = ovr.get("LINE_CAPS.STRAWBERRY")
            rec["dawns"][str(day)] = {
                "reactive_minus_truth": round(float(final[me]) - truth[me], 1),
                "engaged": diff > EPS,
                "best_plan": sel["best"],
                "line_cap_straw": quota,
                "herd_day_shift": ovr.get("PLANNER_OVERRIDES.herd_day_shift"),
                "sell_discount": ovr.get(
                    "PLANNER_OVERRIDES.sell_price_discount"),
            }
            flag = "DTSP-ENGAGED" if diff > EPS else "v13.8-IDENTICAL"
            print(f"ep{rec['episode']} d{day:2d} {flag:14s} "
                  f"Δreactive-truth {diff:9.1f}  plan {sel['best']}")
        rows.append(rec)
    engaged = {"3": 0, "10": 0, "20": 0}
    for r in rows:
        for d in engaged:
            if r["dawns"][d]["engaged"]:
                engaged[d] += 1
    print(f"\n接合计数（{len(rows)} 局）: " +
          ", ".join(f"d{k}={v}/{len(rows)}" for k, v in engaged.items()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump({"rows": rows, "engaged_counts": engaged,
                   "eps": EPS, "dawns": list(DAWNS)},
                  h, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
