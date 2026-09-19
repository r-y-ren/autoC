# 【中文】round23_disaster_dtsp_probe.py —— 灾难局 DTSP 黎明决策离线重建
# ===========================================================================
# 问题（round-23 败局法证任务包 #2）：ep110634204 我方 28.8k、畜群峰值 5 头、
#   d7 后零买畜动作——孪生规划的黎明决策选了什么？是计划压制了扩建，
#   还是 v13.8 反应式同局也会停？
# 方法：复用现役 planner_offline_bench 的同机制管线（同孪生、同 Ω、同
#   投影器/选择器配置=trimmed_mean@0.25×pess0.75，即 P2.6 钉死默认）：
#   1) 逐黎明（d3/6/10/12/13/14/20）重建投影排序 + 稳健选择 → 选中计划
#      与畜群相关旋钮覆盖；
#   2) d10/d13 注入：truth / reactive(无覆盖) / DTSP(选中覆盖) 全季
#      rollout（对手=回放真实动作），输出终局资金 + 终局畜群头数；
#   3) 消融：同 d10 选中覆盖但剔除 herd_start_day/herd_day_shift/
#      animal_buy_last_day_shift（A 组）与 crew_late/fuse 姿态键（B 组），
#      定位压制扩建的具体旋钮组。
# 只读：不改 src/planner/bench 任何文件；输出仅 stdout + probes JSON。
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

REPLAY = os.path.join(SOFTWARE, "..", "references", "data", "online-replays",
                      "round23", "episode-110634204-replay.json")
OUT = os.path.join(SOFTWARE, "exports", "probes", "round23_forensics",
                   "disaster_dtsp_reconstruction.json")
ME_SEAT = 0
DAWNS_FULL = (3, 6, 10, 12, 13, 14, 20)
DAWNS_CHOICE_ONLY = (0, 1, 2, 4, 5, 7, 8, 9, 11)
HERD_KEYS = ("PLANNER_OVERRIDES.herd_start_day",
             "PLANNER_OVERRIDES.herd_day_shift",
             "PLANNER_OVERRIDES.animal_buy_last_day_shift")
POSTURE_KEYS = ("PLANNER_OVERRIDES.crew_late_day",
                "PLANNER_OVERRIDES.crew_late_cap",
                "PLANNER_OVERRIDES.fuse_money_floor")
PESS_DISCOUNT = 0.75
STRATEGY = "trimmed_mean"
TRIM = select.DEFAULT_TRIM_FRACTION


def final_herd(deps, replay, me_seat, inj_step, acts, overrides):
    """全季 rollout 后我方终局畜群头数（复用 bench 扫描器口径）。"""
    state = deps["build"](replay, inj_step)
    agent_fn, _applied, _skip = deps["v13_factory"](overrides)
    final, _taken = bench.rollout_with_replay_opponent(
        deps, state, me_seat, agent_fn, acts, inj_step)
    obs0 = state.seats[me_seat].observation
    farms = obs0.farms
    _crops, herd, _money, _q = bench.scan_farm(farms[me_seat])
    return {"final_money_me": round(float(final[me_seat]), 1),
            "final_money_opp": round(float(final[1 - me_seat]), 1),
            "final_herd_me": herd}


def projection_choice(deps, replay, inj_step):
    """同 bench 的投影段：排序 + 稳健选择，返回 (best_key, ranking, obs)。"""
    state_p = deps["build"](replay, inj_step)
    day = inj_step // 24
    obs_summary = bench.build_obs_summary_from_state(deps, state_p, ME_SEAT,
                                                     day)
    history = bench.extract_opponent_history(replay, 1 - ME_SEAT, inj_step)
    models = opponents.build_default_models(
        history=history, profile_path=None,
        pessimistic=opponents.PessimisticFill(price_discount=PESS_DISCOUNT))
    candidate_plans = plans.enumerate_plans(obs_summary)
    j_matrix = {}
    for spec in candidate_plans:
        scores = {}
        for model in models:
            scores[model.name] = plans.project_season(
                spec, obs_summary, model.supply_pressure(obs_summary))
        j_matrix[spec.key()] = scores
    selection = select.robust_select(j_matrix, strategy=STRATEGY,
                                     trim_fraction=TRIM)
    ranking = [(k, round(v, 1)) for k, v in selection["ranking"][:6]]
    return selection["best"], ranking, obs_summary


def main():
    with open(REPLAY, "r", encoding="utf-8") as h:
        replay = json.load(h)
    deps = bench.make_twin_deps()
    acts = deps["transition_actions"](replay)
    truth = [float(x) for x in replay["rewards"]]
    out = {"episode": 110634204, "me_seat": ME_SEAT, "truth": truth,
           "config": {"strategy": STRATEGY, "trim": TRIM,
                      "pessimistic": PESS_DISCOUNT},
           "dawns": {}, "rollouts": {}}

    # 1) 逐黎明：投影选择 + 选中计划的畜群相关覆盖
    for day in sorted(DAWNS_FULL + DAWNS_CHOICE_ONLY):
        step = min(day * 24, len(acts) - 2)
        best_key, ranking, obs = projection_choice(deps, replay, step)
        spec = bench._spec_by_key(plans.enumerate_plans(obs), best_key)
        ovr = plans.plan_to_knob_overrides(spec)
        herd_view = {k.split(".", 1)[1]: ovr.get(k) for k in ovr
                     if k.startswith("PLANNER_OVERRIDES.herd")
                     or k.startswith("PLANNER_OVERRIDES.animal")
                     or k in POSTURE_KEYS}
        rec = {"day": day, "best_plan": best_key,
               "opp_class": obs.get("opp_class"),
               "money": round(float(obs.get("money", 0)), 0),
               "herd": obs.get("herd"),
               "n_plans": len(plans.enumerate_plans(obs)),
               "herd_related_overrides": herd_view}
        if ranking:
            rec["projection_top6_pessimistic"] = ranking
        out["dawns"][str(day)] = rec
        print(f"d{day:2d} 选 {best_key}  opp_class={obs.get('opp_class')} "
              f"money={obs.get('money'):.0f} herd={obs.get('herd')}")
        print(f"     畜群相关覆盖: {herd_view}")

    # 2) d10/d13 注入四口径 + 消融
    for day in (10, 13):
        step = day * 24
        row = bench.evaluate_injection(
            deps, replay, ME_SEAT, step,
            {"episode": "110634204", "strategy": STRATEGY,
             "trim_fraction": TRIM, "weights": None,
             "pessimistic": opponents.PessimisticFill(
                 price_discount=PESS_DISCOUNT),
             "profile_path": None, "oracle": False, "oracle_top_k": 6})
        out["rollouts"][str(day)] = {"truth_me": row["truth_me"],
                                     "twin_noise": row["twin_noise"],
                                     "reactive_me": row["reactive_me"],
                                     "dtsp_me": row["dtsp_me"],
                                     "best_plan": row["best_plan"]}
        print(f"\nd{day} 注入: truth {row['truth_me']:.0f} twin_noise "
              f"{row['twin_noise']:.1f} reactive {row['reactive_me']:.0f} "
              f"dtsp {row['dtsp_me']:.0f} (plan {row['best_plan']})")
        # 全季 rollout 终局畜群（谁真的扩建了）
        spec = plans.enumerate_plans(bench.build_obs_summary_from_state(
            deps, deps["build"](replay, step), ME_SEAT, day))
        best = bench._spec_by_key(spec, row["best_plan"])
        ovr = plans.plan_to_knob_overrides(best)
        res = {}
        res["reactive"] = final_herd(deps, replay, ME_SEAT, step, acts, None)
        res["dtsp_full"] = final_herd(deps, replay, ME_SEAT, step, acts, ovr)
        ablation_a = {k: v for k, v in ovr.items() if k not in HERD_KEYS}
        res["dtsp_no_herd_knobs"] = final_herd(
            deps, replay, ME_SEAT, step, acts, ablation_a)
        ablation_b = {k: v for k, v in ovr.items() if k not in POSTURE_KEYS}
        res["dtsp_no_posture_knobs"] = final_herd(
            deps, replay, ME_SEAT, step, acts, ablation_b)
        out["rollouts"][str(day)]["herd_detail"] = res
        for name, r in res.items():
            print(f"     {name:24s} money {r['final_money_me']:9.0f} "
                  f"final herd {r['final_herd_me']}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1, default=str)
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
