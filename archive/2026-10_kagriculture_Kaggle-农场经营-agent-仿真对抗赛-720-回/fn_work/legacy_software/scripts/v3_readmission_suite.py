# 【中文】v3_readmission_suite.py —— DTSP v3 复裁门（三判据，2026-09-20）
# ===========================================================================
# 用途（round-24 法证终稿 v3 架构的上线复裁，任务包第 4 项）：v3 = K1
#   identity 守成档 + K2 钱包门档 + K3 land/herd 日程轴拆分 后，逐判据
#   复裁 v14.2-dtsp 候选的准入资格。三判据：
#   a) 原判据：planner_offline_bench --mode official（round20/21/22+
#      cmp-v92 注入集）主口径 >=9/14 局中位不劣 且 全集合 mean
#      Δ(DTSP-反应式)>0（P2.6 基线 12/14 +782.6——v3 不得回退）。
#   b) 新巨人局回归：round-24 的 9 局巨人败局，d0 全季口径（沿
#      round24_d0_counterfactual.py 协议：对手=回放真实动作、真值=线上
#      实际含 DTSP v2），v3 planner（逐黎明 runtime 决策、K=6×H=1d 运行
#      点不变）逐局挽回 >=10% 终局资金需 >=4/9 局。
#   c) 新胜局回归：round-24 的 13 胜局同口径，v3 对真值损伤 >5% 的局数
#      需 <=2。
# 投影耗时断言（预算纪律）：枚举变化后投影段（enumerate × Ω 投影 ×
#   robust_select）实测 <60ms（P2.6 实测 34.1ms 同数量级护栏）。
# CLI：--mode official（全三判据，全过 exit 0）| smoke（摇通：bench smoke
#   + 2 局 v3 rollout + 投影耗时断言，exit 0；判据值照实记录不做门禁）。
# 输出：exports/probes/planner_bench/v3_readmission.json（报告）。
# 纪律：stdlib-only、全离线、确定性（除时间治理器 deadline 降级——线上
#   同款规定动作，报告照实记录 wall 与 failopen 计数）。
# ===========================================================================

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402
from kaggle_simulations.agent.planner import opponents as _opponents   # noqa: E402
from kaggle_simulations.agent.planner import plans as _plans           # noqa: E402
from kaggle_simulations.agent.planner import runtime as _runtime       # noqa: E402
from kaggle_simulations.agent.planner import select as _select         # noqa: E402

ROOT = os.path.dirname(SOFTWARE)
REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT = os.path.join(SOFTWARE, "exports", "probes", "planner_bench",
                   "v3_readmission.json")
TEAM = "renyxin"
# round-24 巨人败局 9 局 / 胜局 13 局（round24_d0_counterfactual.py 同表）
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
WINS13 = (110681129, 110682284, 110683437, 110686759, 110690133,
          110691193, 110692292, 110693383, 110695554, 110696787,
          110697778, 110698875, 110790899)
# v3 运行点（任务包：K=6×H=1d 阶梯与时间治理器不变）
V3_RUNTIME_CONFIG = {
    "enabled": True,
    "seed": 1,
    "budget_cap_s": 0.85,
    "rollout_models": ("pessimistic_fill",),
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
}
GIANT_GATE_MIN_HITS = 4        # 判据 b：>=4/9 局挽回 >=10%
WIN_HURT_MAX = 2               # 判据 c：损伤 >5% 局数 <=2
RECOVER_PCT = 0.10
HURT_PCT = -0.05
PROJECTOR_BUDGET_S = 0.060     # 投影段耗时护栏（枚举变化后必须守住）


def load_replay(episode_id):
    path = os.path.join(REPLAY_DIR, f"episode-{episode_id}-replay.json")
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def rollout_v3_planner(deps, replay, me_seat, config):
    """v3 planner 全季 rollout（d0 口径）：官方动作流对手席 + 我方席 =
    v13.8 命名空间（runtime 黎明钩子逐黎明注入 v3 计划覆盖）。

    返回 dict：final_me / steps / dawns / failopens / plans（逐黎明选中
    计划键）/ policies（策略分布）。时间治理器按真实墙钟运行（与线上
    同款 0.85s 预算与 deadline 降级——诚实口径）。"""
    _runtime.reset_state()
    ns, _applied, _skipped = bench.build_v13_namespace(None)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    me = int(me_seat)
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while not state.env.done and taken < max_steps and taken < len(acts):
        obs = state.seats[me].observation
        day = int(getattr(obs, "day", taken // 24))
        hour = int(getattr(obs, "hour", taken % 24))
        _runtime.dawn_hook(obs, ns, config, player=me, day=day, hour=hour)
        mine = ns["agent"](obs)
        theirs = acts[taken][1 - me]
        deps["step"](state, [mine, theirs])
        taken += 1
    final = deps["final"](state)
    trace = _runtime.trace()
    dawns = trace.get("dawns") or []
    # 逐黎明选择溯源（诊断用：proj_best / rollout_best / selected /
    # 近平守成触发标记）——保留最近 60 黎明全量。
    provenance = [{
        "day": d.get("day"), "policy": d.get("policy"),
        "proj_best": d.get("proj_best"),
        "rollout_best": d.get("rollout_best"),
        "selected": d.get("selected"),
        "switched": d.get("switched"),
        "identity_tiebreak_proj": bool(
            d.get("identity_tiebreak_proj")),
        "identity_tiebreak_rollout": bool(
            d.get("identity_tiebreak_rollout")),
        "n_plans": d.get("n_plans"), "rung": d.get("rung"),
        "budget_s": d.get("budget_s"), "elapsed_s": d.get("elapsed_s"),
    } for d in dawns]
    return {
        "final_me": float(final[me]),
        "steps": taken,
        "dawns": len(dawns),
        "failopens": len(trace.get("failopens") or []),
        "engaged": bool(trace.get("engaged")),
        "plans": [d.get("selected") for d in dawns
                  if d.get("selected")],
        "policies": {},
        "rollouts": int(sum(d.get("rollouts", 0) for d in dawns)),
        "provenance": provenance,
    }


def measure_projector_segment():
    """投影段耗时（枚举 × Ω=4 投影 × robust_select）：合成 d0 开局态实测。
    返回 (elapsed_s, n_plans, proj_best)。断言 <60ms（预算纪律）。"""
    import importlib.util as _ilu
    from kaggle_simulations.agent.planner import twin as _twin
    gspec = _ilu.spec_from_file_location(
        "planner_flagoff_golden_v3readmit",
        os.path.join(SCRIPT_DIR, "planner_flagoff_golden.py"))
    gmod = _ilu.module_from_spec(gspec)
    sys.modules.setdefault("planner_flagoff_golden_v3readmit", gmod)
    gspec.loader.exec_module(gmod)
    obs_head = gmod.synthetic_season_head(11)["steps"][0][0]["observation"]
    bundle = _twin.load_engine()
    summary = _runtime.build_obs_summary(bundle.module, obs_head, 0, 0)
    models = _opponents.build_default_models()
    identity_key = _plans.identity_spec().key()
    t0 = time.perf_counter()
    candidates = _plans.enumerate_plans(summary)
    j_matrix = {}
    for spec in candidates:
        scores = {}
        for model in models:
            scores[model.name] = _plans.project_season(
                spec, summary, model.supply_pressure(summary))
        j_matrix[spec.key()] = scores
    selection = _select.robust_select(
        j_matrix, strategy="trimmed_mean",
        trim_fraction=_select.DEFAULT_TRIM_FRACTION,
        identity_key=identity_key)
    elapsed = time.perf_counter() - t0
    return elapsed, len(candidates), selection["best"]


def run_bench_criterion(mode):
    """判据 a：planner_offline_bench 主口径（official=门禁，smoke=摇通）。"""
    t0 = time.time()
    rc = bench.main(["--mode", mode])
    report_path = os.path.join(SOFTWARE, "exports", "probes",
                               "planner_bench", "bench_report.json")
    summary = {}
    if os.path.isfile(report_path):
        with open(report_path, "r", encoding="utf-8") as handle:
            summary = (json.load(handle).get("summary") or {})
    passed = bool(mode == "official" and rc == 0 and
                  summary.get("gates_all_pass"))
    return {"mode": mode, "bench_exit_code": rc,
            "wall_s": round(time.time() - t0, 1),
            "episodes_passed": summary.get("episodes_passed"),
            "episodes_evaluated": summary.get("episodes_evaluated"),
            "pooled_mean_dtsp_vs_reactive":
                summary.get("pooled_mean_dtsp_vs_reactive"),
            "passed": passed,
            "report": "exports/probes/planner_bench/bench_report.json"}


def run_d0_regression(deps, episodes, label, smoke_n=None):
    """判据 b/c 共用：d0 全季 v3 planner rollout（对手=回放真实动作）。"""
    rows = {}
    picked = list(episodes) if smoke_n is None else list(episodes)[:smoke_n]
    t_start = time.time()
    for ep in picked:
        replay = load_replay(ep)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        t0 = time.time()
        res = rollout_v3_planner(deps, replay, me, V3_RUNTIME_CONFIG)
        gain = (res["final_me"] - truth_me) / truth_me if truth_me else 0.0
        policies = {}
        for d in (_runtime.trace().get("dawns") or []):
            policies[d.get("policy", "?")] = \
                policies.get(d.get("policy", "?"), 0) + 1
        res["policies"] = policies
        rows[str(ep)] = {
            "opponent": teams[1 - me] if len(teams) > 1 else "?",
            "truth_me": truth_me, "truth_opp": truth_opp,
            "v3_final": round(res["final_me"], 1),
            "gain_pct": round(gain, 4),
            "beats_truth_opp": res["final_me"] > truth_opp,
            "dawns": res["dawns"], "engaged": res["engaged"],
            "failopens": res["failopens"], "rollouts": res["rollouts"],
            "n_plan_switches": len(set(res["plans"] or [])),
            "selection_provenance": res["provenance"],
            "wall_s": round(time.time() - t0, 1),
        }
        print(f"[v3-readmit:{label}] ep{ep} vs "
              f"{rows[str(ep)]['opponent'][:18]:18s} truth {truth_me:8.0f} "
              f"v3 {res['final_me']:8.0f} ({gain * 100:+6.1f}%) "
              f"failopen={res['failopens']} [{time.time() - t_start:.0f}s]")
        del replay
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="DTSP v3 复裁门（原判据 + 巨人局回归 + 胜局回归）")
    parser.add_argument("--mode", choices=("official", "smoke"),
                        default="smoke")
    args = parser.parse_args(argv)
    official = args.mode == "official"
    t_start = time.time()
    out = {"protocol": "v3-readmission/1.0",
           "mode": args.mode,
           "generated_at_utc": datetime.now(timezone.utc).isoformat(
               timespec="seconds"),
           "runtime_config": dict(V3_RUNTIME_CONFIG),
           "gates": {
               "giant_min_hits": GIANT_GATE_MIN_HITS,
               "win_hurt_max": WIN_HURT_MAX,
               "recover_pct": RECOVER_PCT, "hurt_pct": HURT_PCT,
               "projector_budget_s": PROJECTOR_BUDGET_S,
           },
           "d0_note": "对手=回放真实动作（非自适应）；truth=线上实际"
                      "（含 DTSP v2 逐黎明重规划）；v3=runtime 全管线"
                      "（identity 守成 + 钱包门 + 日程轴，K=6×H=1d 不变）"}

    # ---- 投影段耗时断言（预算纪律；两种模式都测）----
    elapsed, n_plans, proj_best = measure_projector_segment()
    out["projector_timing"] = {
        "elapsed_s": round(elapsed, 4), "elapsed_ms": round(elapsed * 1000, 1),
        "n_plans": n_plans, "proj_best": proj_best,
        "budget_s": PROJECTOR_BUDGET_S,
        "within_budget": elapsed < PROJECTOR_BUDGET_S,
    }
    print(f"[v3-readmit] projector segment {elapsed * 1000:.1f}ms "
          f"({n_plans} plans) budget {PROJECTOR_BUDGET_S * 1000:.0f}ms "
          f"-> {'OK' if elapsed < PROJECTOR_BUDGET_S else 'OVER'}")

    # ---- 判据 a：原判据（官方注入集）----
    out["criterion_a_official_bench"] = run_bench_criterion(args.mode)

    # ---- 判据 b/c：d0 全季 v3 planner 回归 ----
    deps = bench.make_twin_deps()
    smoke_n = 2 if not official else None
    out["criterion_b_giants"] = {
        "episodes": run_d0_regression(deps, TARGET9, "giants",
                                      smoke_n=smoke_n),
    }
    hits = [ep for ep, r in out["criterion_b_giants"]["episodes"].items()
            if r["gain_pct"] >= RECOVER_PCT]
    failopen_g = sum(r["failopens"] for r in
                     out["criterion_b_giants"]["episodes"].values())
    n_b = len(out["criterion_b_giants"]["episodes"])
    out["criterion_b_giants"].update({
        "n_recovered": len(hits), "recovered": hits, "failopens": failopen_g,
        "passed": official and len(hits) >= GIANT_GATE_MIN_HITS
        and n_b == len(TARGET9) and failopen_g == 0,
    })
    out["criterion_c_wins"] = {
        "episodes": run_d0_regression(deps, WINS13, "wins", smoke_n=smoke_n),
    }
    hurt = [ep for ep, r in out["criterion_c_wins"]["episodes"].items()
            if r["gain_pct"] < HURT_PCT]
    failopen_w = sum(r["failopens"] for r in
                     out["criterion_c_wins"]["episodes"].values())
    n_c = len(out["criterion_c_wins"]["episodes"])
    out["criterion_c_wins"].update({
        "n_hurt_over_5pct": len(hurt), "hurt": hurt, "failopens": failopen_w,
        "passed": official and len(hurt) <= WIN_HURT_MAX
        and n_c == len(WINS13) and failopen_w == 0,
    })

    a_pass = out["criterion_a_official_bench"]["passed"]
    b_pass = out["criterion_b_giants"]["passed"]
    c_pass = out["criterion_c_wins"]["passed"]
    timing_ok = out["projector_timing"]["within_budget"]
    out["overall_pass"] = bool(a_pass and b_pass and c_pass and timing_ok)
    out["wall_seconds"] = round(time.time() - t_start, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(out, handle, ensure_ascii=False, indent=1)
    print(f"\n[v3-readmit] 判据a official={a_pass} "
          f"({out['criterion_a_official_bench']['episodes_passed']}/"
          f"{out['criterion_a_official_bench']['episodes_evaluated']} "
          f"mean {out['criterion_a_official_bench']['pooled_mean_dtsp_vs_reactive']})")
    print(f"[v3-readmit] 判据b 巨人挽回 {len(hits)}/{n_b} "
          f"(需 >= {GIANT_GATE_MIN_HITS}) -> {b_pass}")
    print(f"[v3-readmit] 判据c 胜局损伤>5% {len(hurt)}/{n_c} "
          f"(需 <= {WIN_HURT_MAX}) -> {c_pass}")
    print(f"[v3-readmit] 投影段 {out['projector_timing']['elapsed_ms']}ms "
          f"-> {timing_ok}")
    print(f"[v3-readmit] overall={out['overall_pass']} "
          f"wall={out['wall_seconds']}s\n wrote {OUT}")

    if official:
        return 0 if out["overall_pass"] else 1
    return 0                      # smoke：摇通即 0（判据值照实记录）


if __name__ == "__main__":
    sys.exit(main())
