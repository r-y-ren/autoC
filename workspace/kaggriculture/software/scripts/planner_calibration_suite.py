# 【中文】planner_calibration_suite.py —— DTSP 投影校准终局复裁工具集（P2.6）
# ===========================================================================
# 用途（P2.6 有界迭代授权，2026-09-19：只做校准与消融，不改判据不挑样本；
#   src/ 九模块零改动，twin.py 零改动，旗关等价必须保持）：
#   c1-ablation  定案实验①：强制全部注入点选 C1 档，oracle 面内网格
#                （配额×时点）逐点真孪生 rollout，测 C1 真实经济性。
#                结论二选一：C1 不经济（保守档序有据）或投影器评分看不见
#                C1 价值（修评分）。
#   timing-diag  定案实验②：统计投影 J 值对 timing_shift 的方差
#                （修正前应为零方差——时点轴失选的根因）。
#   d10-jmat     定案实验③：d10 注入点逐 plan×逐对手模型 J 矩阵摘要 +
#                旋钮组隔离 rollout（定位 -920 均值差来源：覆盖没生效
#                还是计划本身差）。
#   sweep        选参（留痕）：聚合策略 × 悲观折扣系数在 smoke 子集上
#                系统扫描；official 全集只在选参后以最终配置跑一次
#                （经 scripts/planner_offline_bench.py，防过拟合）。
# 公平性/确定性纪律：与 bench 同一孪生、同一对手（回放真实动作）、同一
#   注入点集合（official=14 局×d3/d10/d20）；oracle 网格与选参规则在跑前
#   钉死并写进输出（选参过程留痕）。stdlib-only、全离线、确定性排序。
# 输出只落 software/exports/probes/planner_bench/calibration/。
# ===========================================================================

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kaggle_simulations.agent.planner import opponents as opp_mod      # noqa: E402
from kaggle_simulations.agent.planner import plans                     # noqa: E402
from kaggle_simulations.agent.planner import select                    # noqa: E402
from scripts.planner_offline_bench import (                            # noqa: E402
    OFFICIAL_INJECTION_DAYS, OFFICIAL_ROUNDS, SMOKE_ROUNDS,
    build_obs_summary_from_state, extract_opponent_history,
    find_episodes, make_twin_deps, rollout_with_replay_opponent,
    select_injection_steps)

CALIB_DIR = os.path.join(SOFTWARE, "exports", "probes", "planner_bench",
                         "calibration")
DEFAULT_TEAM = "renyxin"
REPLAY_ROOT = os.path.join(SOFTWARE, "..", "references", "data",
                           "online-replays")

# ---- C1 oracle 网格（跑前钉死；配额×时点全覆盖、折扣取投影器一贯偏好
#      0.90；分支按 R2 规则由 opp_class 定格；开局面定 C=现役默认）----
C1_ABLATION_QUOTAS = (0.8, 1.0, 1.25)
C1_ABLATION_TIMINGS = (-2, 0, 2)
C1_ABLATION_DISCOUNT = 0.9

# ---- sweep 选参网格（跑前钉死；official 只在选定后跑一次）----
SWEEP_STRATEGIES = (
    ("trimmed_mean", 0.25, None),      # 现任默认
    ("trimmed_mean", 0.0, None),       # 全均值（不裁尾）
    ("worst_case", None, None),        # 纯悲观下界（首轮口径的对照）
    ("weighted", None,
     {"passive_extrapolation": 1.0, "frozen_style_pool:winner_balanced": 1.0,
      "frozen_style_pool:wheat_suppressor": 1.0,
      "pessimistic_fill": 0.5}),       # 悲观模型半权
)
SWEEP_DISCOUNTS = (0.75, 0.85, 0.90)
# 选参规则（跑前钉死）：① smoke 子集 primary 过线局数最多 → ② 全配置
# pooled mean Δ(DTSP−反应式) 最大 → ③ 网格序在前者（确定性，防挑参）。

# ---- 旋钮组（d10 隔离用；键面=plans.plan_to_knob_overrides 输出的前缀）----
KNOB_GROUPS = {
    "tier_gates": ("PLANNER_OVERRIDES.mode_volume_", "PLANNER_OVERRIDES.mode_scale_",
                   "PLANNER_OVERRIDES.d6_"),
    "caps": (".straw_quad_cap", ".straw_total_cap", ".wheat_money_quad",
             "STRAW_QUAD_CAP_REGIME", "STRAW_TOTAL_CAP_REGIME",
             "LINE_CAPS."),
    "sell": ("SELL_PLAN_HOLD_EDGE", "PLANNER_OVERRIDES.sell_price_discount",
             "PLANNER_OVERRIDES.sell_batch_mult",
             "PLANNER_OVERRIDES.p4_force_tier"),
    "timing": ("LAND_PLAN.", "SE_DUE_DAY", "PLANNER_OVERRIDES.herd_day_shift",
               "PLANNER_OVERRIDES.herd_start_day",
               "PLANNER_OVERRIDES.animal_buy_last_day_shift"),
    "branch": ("PLANNER_OVERRIDES.b_branch_force",),
    "p3": ("PLANNER_OVERRIDES.fuse_money_floor",
           "PLANNER_OVERRIDES.crew_late_"),
}


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_json(name, payload):
    os.makedirs(CALIB_DIR, exist_ok=True)
    path = os.path.join(CALIB_DIR, name)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2,
                  sort_keys=True)
    print(f"[calib] -> {path}")
    return path


def _load_episodes(args, rounds, days, limit):
    evaluable, skipped = find_episodes(REPLAY_ROOT, rounds, limit,
                                       args.team)
    out = []
    for ep in evaluable:
        with open(ep["path"], "r", encoding="utf-8") as handle:
            replay = json.load(handle)
        inj_steps = select_injection_steps(len(replay.get("steps") or []),
                                           days)
        if inj_steps:
            out.append((ep, replay, inj_steps))
        else:
            skipped.append({"episode": ep["episode"], "reason": "无注入步"})
    return out, skipped


def _forced_branch(obs_summary):
    """R2 同款分支定格（枚举规则镜像；opp_class 缺失回退 B2=标准序列）。"""
    branch_of = {"burst": "B1", "reduced": "B2", "deferred": "B2",
                 "melon_first": "B3"}
    return branch_of.get(obs_summary.get("opp_class"), "B2")


def _forced_mode(obs_summary):
    """R4 同款运行态定格（d12 现金 8k 分界）。"""
    if int(obs_summary.get("day", 0)) < 12:
        return "HEALTHY"
    return "HEALTHY" if float(obs_summary.get("money", 0.0)) >= 8000.0 \
        else "CATCHUP"


# --------------------------------------------------------------------------
# 模式 1：C1-only oracle 消融
# --------------------------------------------------------------------------


def run_c1_ablation(args):
    deps = make_twin_deps()
    rounds = tuple(args.rounds.split(",")) if args.rounds else OFFICIAL_ROUNDS
    days = ([int(x) for x in args.injection_days.split(",")]
            if args.injection_days else list(OFFICIAL_INJECTION_DAYS))
    episodes, skipped = _load_episodes(args, rounds, days, args.limit)
    rows = []
    t0 = time.time()
    for ep, replay, inj_steps in episodes:
        acts = deps["transition_actions"](replay)
        for inj in inj_steps:
            day = inj // 24
            state = deps["build"](replay, inj)
            obs = build_obs_summary_from_state(deps, state, ep["me_seat"],
                                               day)
            # 反应式基线（v13.8 原样，同孪生同对手）
            reactive_final, _proxy, _sk = _rollout(deps, replay, ep, acts,
                                                   inj, None)
            # C1 oracle 网格：quota × timing（分支/运行态/出清按枚举规则定格）
            branch = _forced_branch(obs)
            mode = _forced_mode(obs)
            grid = []
            for quota in C1_ABLATION_QUOTAS:
                for shift in C1_ABLATION_TIMINGS:
                    grid.append(plans.PlanSpec(
                        opening="C", p1_branch=branch, capacity_tier="C1",
                        p3_mode=mode, p4_clear="LOW", quota_scale=quota,
                        timing_shift=shift,
                        sell_discount=C1_ABLATION_DISCOUNT))
            c1_results = []
            for spec in grid:
                final, _p, _s = _rollout(deps, replay, ep, acts, inj, spec)
                c1_results.append({
                    "plan": spec.key(),
                    "final_me": float(final[ep["me_seat"]]),
                })
            c1_best = max(c1_results, key=lambda r: (r["final_me"],
                                                     r["plan"]))
            # 投影器当前对 C1 最优实现的排序位置（全候选集内名次）
            rank_note = _projector_rank_of(obs, c1_best["plan"])
            rows.append({
                "episode": ep["episode"], "round": ep["round"],
                "step": inj, "day": day, "opponent": ep["opponent"],
                "truth_me": float(
                    (replay.get("rewards") or [0.0, 0.0])[ep["me_seat"]]),
                "reactive_me": float(reactive_final[ep["me_seat"]]),
                "c1_best_plan": c1_best["plan"],
                "c1_best_me": c1_best["final_me"],
                "c1_best_vs_reactive": c1_best["final_me"]
                - float(reactive_final[ep["me_seat"]]),
                "c1_best_vs_truth": c1_best["final_me"]
                - float((replay.get("rewards") or [0.0, 0.0])[ep["me_seat"]]),
                "c1_grid": sorted(c1_results, key=lambda r: r["plan"]),
                "projector_rank_of_c1_best": rank_note,
            })
            print(f"[c1] {ep['episode']} d{day} "
                  f"c1_best-reactive={rows[-1]['c1_best_vs_reactive']:+.0f} "
                  f"rank={rank_note['rank']}/{rank_note['of']}")
        del replay
    margins = [r["c1_best_vs_reactive"] for r in rows]
    wins = sum(1 for m in margins if m > 1.0)
    ties = sum(1 for m in margins if -1.0 <= m <= 1.0)
    losses = sum(1 for m in margins if m < -1.0)
    by_day = {}
    for r in rows:
        by_day.setdefault(r["day"], []).append(r["c1_best_vs_reactive"])
    verdict_stats = {
        "points": len(rows),
        "c1_beats_reactive": wins, "c1_ties_reactive": ties,
        "c1_loses_reactive": losses,
        "mean_margin": sum(margins) / len(margins) if margins else 0.0,
        "median_margin": statistics.median(margins) if margins else 0.0,
        "mean_margin_by_day": {str(d): sum(v) / len(v)
                               for d, v in sorted(by_day.items())},
        "grid_quotas": list(C1_ABLATION_QUOTAS),
        "grid_timings": list(C1_ABLATION_TIMINGS),
        "grid_discount": C1_ABLATION_DISCOUNT,
        "wall_seconds": round(time.time() - t0, 1),
        "decision_rule": (
            "mean/median margin 显著>0 且 wins 占优 => C1 有真实价值、"
            "投影器评分看不见（修评分）；margin <=0 或 wins 不占优 => "
            "C1 不经济（保守档序剔除/降权有据）。 ties=|Δ|<=1（GATE_EPS）"),
    }
    report = {"mode": "c1-ablation", "generated_at_utc": _now_iso(),
              "team": args.team, "configuration": {
                  "rounds": list(rounds), "injection_days": days,
                  "limit": args.limit},
              "verdict_stats": verdict_stats, "rows": rows,
              "skipped": skipped}
    _write_json("c1_ablation.json", report)
    print(f"[c1] verdict: wins/ties/losses = {wins}/{ties}/{losses}, "
          f"mean margin {verdict_stats['mean_margin']:+.0f}, "
          f"median {verdict_stats['median_margin']:+.0f}")
    return 0


def _rollout(deps, replay, ep, acts, inj, spec):
    """spec=None → 反应式原样；否则按 plan 覆盖。返回 (final, proxy, skipped)。"""
    if spec is None:
        overrides = None
    else:
        overrides = plans.plan_to_knob_overrides(spec)
    if not deps.get("v13_available", True):
        state = deps["build"](replay, inj)
        deps["run_to_end"](state, acts[inj:])
        return deps["final"](state), True, []
    try:
        agent_fn, _applied, skipped = deps["v13_factory"](overrides)
    except Exception as exc:                             # noqa: BLE001
        sys.stderr.write(f"[warn] v13.8 装载失败，降级回放代理: {exc}\n")
        state = deps["build"](replay, inj)
        deps["run_to_end"](state, acts[inj:])
        return deps["final"](state), True, []
    state = deps["build"](replay, inj)
    final, _taken = rollout_with_replay_opponent(
        deps, state, ep["me_seat"], agent_fn, acts, inj)
    return final, False, skipped


def _projector_rank_of(obs, plan_key):
    """当前投影器全候选集排序中 plan_key 的名次（1=最优；trimmed_mean）。"""
    cands = plans.enumerate_plans(obs)
    models = opp_mod.build_default_models()
    jmat = {}
    for spec in cands:
        scores = {}
        for model in models:
            scores[model.name] = plans.project_season(
                spec, obs, model.supply_pressure(obs))
        jmat[spec.key()] = scores
    ranking = select.robust_select(jmat, strategy="trimmed_mean")["ranking"]
    rank = next((i + 1 for i, (k, _v) in enumerate(ranking)
                 if k == plan_key), None)
    return {"rank": rank, "of": len(ranking),
            "top3": [k for k, _v in ranking[:3]]}


# --------------------------------------------------------------------------
# 模式 2：时点轴方差诊断
# --------------------------------------------------------------------------


def run_timing_diag(args):
    deps = make_twin_deps()
    rounds = tuple(args.rounds.split(",")) if args.rounds else OFFICIAL_ROUNDS
    days = ([int(x) for x in args.injection_days.split(",")]
            if args.injection_days else list(OFFICIAL_INJECTION_DAYS))
    episodes, skipped = _load_episodes(args, rounds, days, args.limit)
    rows = []
    for ep, replay, inj_steps in episodes:
        for inj in inj_steps:
            day = inj // 24
            state = deps["build"](replay, inj)
            obs = build_obs_summary_from_state(deps, state, ep["me_seat"],
                                               day)
            cands = plans.enumerate_plans(obs)
            models = opp_mod.build_default_models(
                history=extract_opponent_history(replay, 1 - ep["me_seat"],
                                                 inj))
            zero_var = 0
            spread_max = 0.0
            checked = 0
            for spec in cands:
                if spec.timing_shift != 0:
                    continue
                base = spec
                vals = []
                for shift in plans.TIMING_SHIFTS:
                    moved = plans.PlanSpec(
                        opening=base.opening, p1_branch=base.p1_branch,
                        capacity_tier=base.capacity_tier,
                        p3_mode=base.p3_mode, p4_clear=base.p4_clear,
                        quota_scale=base.quota_scale,
                        timing_shift=shift,
                        sell_discount=base.sell_discount)
                    agg = select.aggregate_scores({
                        m.name: plans.project_season(
                            moved, obs, m.supply_pressure(obs))
                        for m in models}, strategy="trimmed_mean")
                    vals.append(agg)
                checked += 1
                spread = max(vals) - min(vals)
                spread_max = max(spread_max, spread)
                if spread == 0.0:
                    zero_var += 1
            rows.append({
                "episode": ep["episode"], "round": ep["round"],
                "step": inj, "day": day,
                "n_timing_families": checked,
                "zero_variance_families": zero_var,
                "max_j_spread_across_timing": spread_max,
            })
        del replay
    total = sum(r["n_timing_families"] for r in rows)
    zero = sum(r["zero_variance_families"] for r in rows)
    report = {
        "mode": "timing-diag", "generated_at_utc": _now_iso(),
        "team": args.team,
        "summary": {
            "timing_families_checked": total,
            "zero_variance_families": zero,
            "zero_variance_share": (zero / total) if total else 0.0,
            "max_j_spread": max((r["max_j_spread_across_timing"]
                                 for r in rows), default=0.0),
        },
        "rows": rows, "skipped": skipped,
    }
    _write_json("timing_diag.json", report)
    print(f"[timing] zero-variance {zero}/{total} families, "
          f"max spread {report['summary']['max_j_spread']:.1f}")
    return 0


# --------------------------------------------------------------------------
# 模式 3：d10 J 矩阵 + 旋钮组隔离
# --------------------------------------------------------------------------


def _overrides_drop_groups(overrides, drop_groups):
    """从覆盖映射中剔除指定旋钮组（组内键回默认=反应式语义）。"""
    prefixes = tuple(p for g in drop_groups for p in KNOB_GROUPS[g])
    out = {}
    for key, value in overrides.items():
        if key.startswith(prefixes) or any(key == p.rstrip("_")
                                           for p in prefixes):
            continue
        if key == "SELL_PLAN_HOLD_EDGE" and "sell" in drop_groups:
            continue
        out[key] = value
    return out


def run_d10_jmat(args):
    deps = make_twin_deps()
    rounds = tuple(args.rounds.split(",")) if args.rounds else OFFICIAL_ROUNDS
    episodes, skipped = _load_episodes(args, rounds, [10], args.limit)
    rows = []
    for ep, replay, inj_steps in episodes:
        for inj in inj_steps:                       # d10 → 恰 1 个
            day = inj // 24
            state = deps["build"](replay, inj)
            obs = build_obs_summary_from_state(deps, state, ep["me_seat"],
                                               day)
            hist = extract_opponent_history(replay, 1 - ep["me_seat"], inj)
            models = opp_mod.build_default_models(history=hist)
            cands = plans.enumerate_plans(obs)
            jmat = {}
            for spec in cands:
                scores = {}
                for model in models:
                    scores[model.name] = plans.project_season(
                        spec, obs, model.supply_pressure(obs))
                jmat[spec.key()] = scores
            strategies = {}
            for strat, trim, weights in SWEEP_STRATEGIES:
                sel = select.robust_select(jmat, strategy=strat,
                                           weights=weights,
                                           trim_fraction=trim or 0.25)
                strategies[f"{strat}@{trim}"] = {
                    "best": sel["best"],
                    "top5": [[k, round(v, 1)] for k, v in sel["ranking"][:5]]}
            # 反应式 + 覆盖恒等校验 + 旋钮组隔离（现任默认策略的选中计划）
            acts = deps["transition_actions"](replay)
            reactive_final, _p, _s = _rollout(deps, replay, ep, acts, inj,
                                              None)
            sel_default = select.robust_select(
                jmat, strategy="trimmed_mean")["best"]
            spec_sel = _spec_by_key(cands, sel_default)
            overrides = plans.plan_to_knob_overrides(spec_sel)

            def rollout_ov(ov):
                if not deps.get("v13_available", True):
                    st = deps["build"](replay, inj)
                    deps["run_to_end"](st, acts[inj:])
                    return deps["final"](st)
                try:
                    fn, _a, _s = deps["v13_factory"](ov)
                except Exception as exc:             # noqa: BLE001
                    sys.stderr.write(f"[warn] v13.8 装载失败: {exc}\n")
                    st = deps["build"](replay, inj)
                    deps["run_to_end"](st, acts[inj:])
                    return deps["final"](st)
                st = deps["build"](replay, inj)
                final, _t = rollout_with_replay_opponent(
                    deps, st, ep["me_seat"], fn, acts, inj)
                return final

            me = ep["me_seat"]
            full_final = rollout_ov(overrides)
            identity_final = rollout_ov({"PLANNER_ENABLED": True})
            no_tier_gates = rollout_ov(
                _overrides_drop_groups(overrides, ("tier_gates",)))
            no_caps = rollout_ov(_overrides_drop_groups(overrides, ("caps",)))
            no_sell = rollout_ov(_overrides_drop_groups(overrides, ("sell",)))
            no_timing = rollout_ov(
                _overrides_drop_groups(overrides, ("timing",)))
            rows.append({
                "episode": ep["episode"], "round": ep["round"], "day": day,
                "opponent": ep["opponent"],
                "reactive_me": float(reactive_final[me]),
                "flag_on_no_overrides_me": float(identity_final[me]),
                "coverage_identity_gap": float(identity_final[me])
                - float(reactive_final[me]),
                "selected_plan": sel_default,
                "dtsp_full_me": float(full_final[me]),
                "dtsp_vs_reactive": float(full_final[me])
                - float(reactive_final[me]),
                "isolation": {
                    "drop_tier_gates": float(no_tier_gates[me])
                    - float(reactive_final[me]),
                    "drop_caps": float(no_caps[me])
                    - float(reactive_final[me]),
                    "drop_sell": float(no_sell[me])
                    - float(reactive_final[me]),
                    "drop_timing": float(no_timing[me])
                    - float(reactive_final[me]),
                },
                "selector_variants": strategies,
                "j_matrix": {k: {m: round(v, 1) for m, v in sorted(s.items())}
                             for k, s in sorted(jmat.items())},
                "obs_snapshot": {
                    "money": obs["money"], "herd": obs["herd"],
                    "crops": obs["crops"],
                    "unlocked_quadrants": obs["unlocked_quadrants"],
                    "daily_demand": obs["daily_demand"],
                    "opp_class": obs["opp_class"],
                },
            })
            print(f"[d10] {ep['episode']} dtsp-reactive="
                  f"{rows[-1]['dtsp_vs_reactive']:+.0f} identity_gap="
                  f"{rows[-1]['coverage_identity_gap']:+.0f} "
                  f"iso={rows[-1]['isolation']}")
        del replay
    mean_gap = (sum(r["dtsp_vs_reactive"] for r in rows) / len(rows)
                if rows else 0.0)
    iso_means = {k: sum(r["isolation"][k] for r in rows) / len(rows)
                 for k in ("drop_tier_gates", "drop_caps", "drop_sell",
                           "drop_timing")} if rows else {}
    report = {
        "mode": "d10-jmat", "generated_at_utc": _now_iso(),
        "team": args.team,
        "summary": {
            "points": len(rows), "mean_dtsp_vs_reactive": mean_gap,
            "mean_isolation_vs_reactive": iso_means,
            "mean_coverage_identity_gap": (
                sum(r["coverage_identity_gap"] for r in rows) / len(rows)
                if rows else 0.0),
            "read_note": (
                "coverage_identity_gap≈0 => 旗开无覆盖=反应式（覆盖通道"
                "本身不引入行为漂移）；isolation.drop_X 是把选中计划的 X 组"
                "旋钮退回默认后的 Δ——哪个组的 drop 让 Δ 向 0 收敛最大，"
                "该组就是损失主要来源（覆盖生效但计划参数错）。"),
        },
        "rows": rows, "skipped": skipped,
    }
    _write_json("d10_jmat.json", report)
    print(f"[d10] mean dtsp-reactive {mean_gap:+.0f}; isolation means "
          f"{ {k: round(v) for k, v in iso_means.items()} }")
    return 0


def _spec_by_key(cands, key):
    for spec in cands:
        if spec.key() == key:
            return spec
    raise RuntimeError(f"排序键 {key!r} 不在候选集")


# --------------------------------------------------------------------------
# 模式 4：聚合策略 × 悲观折扣 smoke 选参（留痕）
# --------------------------------------------------------------------------


def run_sweep(args):
    deps = make_twin_deps()
    rounds = tuple(args.rounds.split(",")) if args.rounds else SMOKE_ROUNDS
    days = ([int(x) for x in args.injection_days.split(",")]
            if args.injection_days else [3, 10, 20])
    episodes, skipped = _load_episodes(args, rounds, days, args.limit)
    points = []
    for ep, replay, inj_steps in episodes:
        acts = deps["transition_actions"](replay)
        for inj in inj_steps:
            day = inj // 24
            state = deps["build"](replay, inj)
            obs = build_obs_summary_from_state(deps, state, ep["me_seat"],
                                               day)
            hist = extract_opponent_history(replay, 1 - ep["me_seat"], inj)
            cands = plans.enumerate_plans(obs)
            reactive_final, _p, _s = _rollout(deps, replay, ep, acts, inj,
                                              None)
            points.append({
                "episode": ep["episode"], "round": ep["round"],
                "me_seat": ep["me_seat"], "inj": inj, "day": day,
                "replay": replay, "acts": acts, "obs": obs, "hist": hist,
                "cands": cands,
                "truth": float((replay.get("rewards") or [0.0, 0.0])
                               [ep["me_seat"]]),
                "reactive": float(reactive_final[ep["me_seat"]]),
            })
    print(f"[sweep] {len(points)} smoke 注入点 × {len(SWEEP_STRATEGIES) * len(SWEEP_DISCOUNTS)} 配置")
    configs = []
    for strat, trim, weights in SWEEP_STRATEGIES:
        for disc in SWEEP_DISCOUNTS:
            configs.append({"strategy": strat, "trim_fraction": trim,
                            "weights": weights, "pessimistic_discount": disc})
    results = []
    for cfg in configs:
        deltas = []
        per_point = []
        for pt in points:
            models = opp_mod.build_default_models(
                history=pt["hist"],
                pessimistic=opp_mod.PessimisticFill(
                    price_discount=cfg["pessimistic_discount"]))
            jmat = {}
            for spec in pt["cands"]:
                scores = {}
                for model in models:
                    scores[model.name] = plans.project_season(
                        spec, pt["obs"], model.supply_pressure(pt["obs"]))
                jmat[spec.key()] = scores
            sel = select.robust_select(jmat, strategy=cfg["strategy"],
                                       weights=cfg["weights"],
                                       trim_fraction=cfg["trim_fraction"]
                                       if cfg["trim_fraction"] is not None
                                       else 0.25)
            spec_best = _spec_by_key(pt["cands"], sel["best"])
            final, _p, _s = _rollout(deps, pt["replay"],
                                     {"episode": pt["episode"],
                                      "me_seat": pt["me_seat"]},
                                     pt["acts"], pt["inj"], spec_best)
            delta = float(final[pt["me_seat"]]) - pt["reactive"]
            deltas.append(delta)
            per_point.append({"episode": pt["episode"], "day": pt["day"],
                              "best": sel["best"], "delta": round(delta, 1)})
        mean_d = sum(deltas) / len(deltas) if deltas else 0.0
        med_d = statistics.median(deltas) if deltas else 0.0
        n_pass = sum(1 for d in deltas if d >= -1.0)
        results.append({"config": {k: v for k, v in cfg.items()},
                        "n_points": len(deltas), "n_point_pass": n_pass,
                        "mean_delta": mean_d, "median_delta": med_d,
                        "per_point": per_point})
        print(f"[sweep] {cfg['strategy']}(trim={cfg['trim_fraction']},"
              f"w={ 'pess0.5' if cfg['weights'] else '-'})×"
              f"pess={cfg['pessimistic_discount']}: "
              f"pass {n_pass}/{len(deltas)} mean {mean_d:+.0f}")
    # 选参规则（跑前钉死）：① 点过线数 ② mean Δ ③ 网格序。
    ranked = sorted(range(len(results)),
                    key=lambda i: (-results[i]["n_point_pass"],
                                   -results[i]["mean_delta"], i))
    winner = results[ranked[0]]
    report = {
        "mode": "sweep", "generated_at_utc": _now_iso(), "team": args.team,
        "selection_rule": (
            "① smoke 注入点 primary 过线数(DTSP>=反应式-1)最多 → "
            "② pooled mean Δ 最大 → ③ 网格序在前（防挑参）；"
            "official 全集只以最终配置跑一次"),
        "grid": {"strategies": [s[0] for s in SWEEP_STRATEGIES],
                 "trims": [s[1] for s in SWEEP_STRATEGIES],
                 "pessimistic_discounts": list(SWEEP_DISCOUNTS)},
        "smoke_points": len(points),
        "ranked_configs": [
            {"rank": i + 1, "config": results[idx]["config"],
             "n_point_pass": results[idx]["n_point_pass"],
             "mean_delta": results[idx]["mean_delta"],
             "median_delta": results[idx]["median_delta"]}
            for i, idx in enumerate(ranked)],
        "winner": winner,
        "all_results": results,
    }
    _write_json("sweep.json", report)
    print(f"[sweep] WINNER: {winner['config']} pass "
          f"{winner['n_point_pass']}/{winner['n_points']} "
          f"mean {winner['mean_delta']:+.0f}")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="DTSP P2.6 投影校准工具集（消融/诊断/选参，只读 src）")
    parser.add_argument("mode",
                        choices=("c1-ablation", "timing-diag", "d10-jmat",
                                 "sweep"))
    parser.add_argument("--team", default=DEFAULT_TEAM)
    parser.add_argument("--rounds", default=None,
                        help="缺省：c1/d10 用 official 四轮；sweep 用 smoke")
    parser.add_argument("--injection-days", default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="缺省：c1/d10=14、timing-diag=14、sweep=3")
    args = parser.parse_args(argv)
    if args.limit is None:
        args.limit = 3 if args.mode == "sweep" else 14
    return {"c1-ablation": run_c1_ablation,
            "timing-diag": run_timing_diag,
            "d10-jmat": run_d10_jmat,
            "sweep": run_sweep}[args.mode](args)


if __name__ == "__main__":
    sys.exit(main())
