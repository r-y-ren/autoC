# -*- coding: utf-8 -*-
"""assemble_track2：证据汇总→fn_docs/hybrid/results/2026-09-29-track2-endogenous.json。

契约键（strongest-showdown 同族）：_generated_at/source/builds/gates/pairs/
criteria/winner/anomaly/elapsed_s + 本实验专项：diff_audit/hygiene_stats/
footprint_audit/budget/verdict。数字只引用 evidence/ 各实测件与 pairs 的
实测读数（数据纪律：不编造）。只读 track2_lab/evidence/，只写结果 JSON。
"""
from __future__ import annotations

import json
import os
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.join(ROOT, "evidence")
KSIM = os.path.dirname(ROOT)
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(KSIM)))
OUT = os.path.join(WORKSPACE, "fn_docs", "hybrid", "results",
                   "2026-09-29-track2-endogenous.json")


def _load(name, default=None):
    path = os.path.join(EVID, name)
    if not os.path.isfile(path):
        return default if default is not None else {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    build = _load("build_manifest.json")
    gates = _load("gates.json")
    judgment = _load("judgment.json")
    footprint = _load("footprint_audit.json")
    diff_audit = _load("diff_audit.json")
    pairs = {name: _load("pair_%s.json" % name)
             for name in ("inner_vs_outer", "inner_vs_base", "outer_vs_base")}

    def pair_head(agg):
        if not agg:
            return None
        return {"h2h": agg.get("h2h"), "wins": agg.get("wins"),
                "losses": agg.get("losses"), "ties": agg.get("ties"),
                "mean_margin": agg.get("mean_margin"),
                "realized_px_median": (agg.get("ours") or {})
                .get("realized_px_median"),
                "terminal_money_median": (agg.get("ours") or {})
                .get("terminal_money_median"),
                "n_error_games": agg.get("n_error_games")}

    heads = {k: pair_head(v) for k, v in pairs.items()}
    inner_vs_outer = pairs.get("inner_vs_outer") or {}
    inner_vs_base = pairs.get("inner_vs_base") or {}
    outer_vs_base = pairs.get("outer_vs_base") or {}

    # ---- 卫生对照（inner vs outer：挂单数/幻影数/单均量） ----
    def wall_window(agg, sub):
        w = (agg.get("wall") or {}).get(sub) or {}
        return {"orders_total": w.get("orders_total"),
                "phantom_orders_qty_gt_held": w.get("phantom_orders_qty_gt_held"),
                "avg_qty_per_order": w.get("avg_qty_per_order"),
                "qty_total": w.get("qty_total"),
                "max_qty": w.get("max_qty")}

    hygiene_stats = {
        "caliber": ("挂单墙=judgment trace wall_stats（两臂同语料同对手 base；"
                    "inner 取 inner_vs_base 我席，outer 取 outer_vs_base 我席）；"
                    "台账=gates 局 _X1_REPORT / _S1009_REPORT.hyg 实测计数"),
        "wall_inner_vs_outer": {
            sub: {
                "inner": wall_window(inner_vs_base, sub),
                "outer": wall_window(outer_vs_base, sub),
            } for sub in ("all_days", "step_ge_624", "d27", "step_670_695")},
        "ledger_counts_gate_episodes": {
            "outer_X1": gates.get("forms", {}).get("h1_outer", {})
            .get("hygiene_reports"),
            "inner_hyg": gates.get("forms", {}).get("h1_inner", {})
            .get("hygiene_reports"),
        },
        "semantics_parity": gates.get("semantics_parity"),
    }

    # ---- 判决 ----
    h_io = inner_vs_outer.get("h2h")
    verdict_endogenous_vs_outer = None
    if isinstance(h_io, (int, float)):
        if h_io >= 0.5:
            verdict_endogenous_vs_outer = ("内生不过负：inner vs outer h2h=%s"
                                           "≥0.5（同语义同读数下内生摆放不劣于"
                                           "外挂尾块）" % h_io)
        else:
            verdict_endogenous_vs_outer = ("内生过负：inner vs outer h2h=%s"
                                           "<0.5（外挂版更强）" % h_io)
    criteria = {
        "h2h_inner_vs_outer": h_io,
        "inner_not_negative_vs_outer": (isinstance(h_io, (int, float))
                                        and h_io >= 0.5),
        "h2h_inner_vs_base": inner_vs_base.get("h2h"),
        "h2h_outer_vs_base": outer_vs_base.get("h2h"),
        "outer_vs_base_replay_WLT": {
            k: (outer_vs_base.get("replay_r30_26") or {}).get(k)
            for k in ("wins", "losses", "ties", "h2h")},
        "outer_vs_base_neutral_WLT": {
            k: (outer_vs_base.get("neutral_672000_i43") or {}).get(k)
            for k in ("wins", "losses", "ties", "h2h")},
        "realized_px_nonneg": all(
            isinstance((p.get("ours") or {}).get("realized_px_median"),
                       (int, float)) and (p["ours"]["realized_px_median"] > 0)
            for p in (inner_vs_outer, inner_vs_base, outer_vs_base) if p),
        "gates_all_pass": gates.get("overall_passed"),
        "semantics_parity_pass": (gates.get("semantics_parity") or {})
        .get("passed"),
        "footprint_non_target_zero": footprint.get(
            "overall_non_target_zero_footprint"),
    }

    winner = {
        "main_judgment": "inner_vs_outer（内生版 vs 外挂版；h2h≥0.5=内生不过负）",
        "verdict": verdict_endogenous_vs_outer,
        "readings": heads,
    }

    anomaly = {
        "harness_noise": [
            "HP_TELEMETRY stdout 行（H 件自报 telemetry）——已知 harness 越界写"
            "副作用，不修不管",
            "kaggle_environments 加载 open_spiel_env/cabt 失败告警（无关环境，忽略）",
        ],
        "build_phase_defect_fixed": (
            "内生版初稿误用 _S1008_PARENT 作父调用（跳过 step1008 整层），"
            "足迹审计抓到非目标拍差异（s102 457/481/553/577）后修正为 "
            "_S1009_PARENT 并重建；最终形态审计=非目标拍零足迹。该缺陷是"
            "足迹审计有效性的正证。"),
        "debug_episodes_outside_scored_budget": (
            "缺陷定位期 exploratory 局（初版 gates 9 局 + 复现/消融/修复验证 "
            "8 局）为 harness 调试，不计入判决矩阵；计分预算仅 gates 9 + "
            "auth 60 + judgment 276 = 345 局次"),
        "n_error_games": {k: v.get("n_error_games")
                          for k, v in pairs.items() if v},
    }

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "experiment": ("track2 内生重构对照实验：X1 卫生层（同拍碎单合并+幻影"
                       "死单清理）内生版（织入 H1 内层 step1009 单列表构造点"
                       "函数体）vs 外挂版（现 H1 尾块）vs 无卫生基座"),
        "source": {
            "commands": ["python3 orderbook_track2_lab/build_track2.py",
                         "python3 orderbook_track2_lab/gates_track2.py",
                         "python3 orderbook_track2_lab/footprint_audit.py",
                         "python3 orderbook_track2_lab/judge_track2.py"],
            **(judgment.get("source") or {}),
        },
        "builds": build.get("forms"),
        "diff_audit": diff_audit,
        "gates": {
            "overall_passed": gates.get("overall_passed"),
            "forms": {f: {k: v for k, v in (gates.get("forms", {}).get(f) or {})
                          .items() if k in ("load", "health", "determinism",
                                            "identity", "overall")}
                      for f in ("h1_outer", "h1_inner", "h1_base")},
        },
        "pairs": heads,
        "pairs_full_files": {
            k: "fn_work/legacy_software/kaggle_simulations/"
               "orderbook_track2_lab/evidence/pair_%s.json" % k
            for k in pairs},
        "hygiene_stats": hygiene_stats,
        "footprint_audit": footprint,
        "budget": judgment.get("budget"),
        "criteria": criteria,
        "winner": winner,
        "verdict": verdict_endogenous_vs_outer,
        "anomaly": anomaly,
        "elapsed_s": judgment.get("elapsed_s"),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(out, ensure_ascii=False, indent=1,
                            default=str) + "\n")
    print("wrote", OUT)
    print("verdict:", verdict_endogenous_vs_outer)
    print("criteria:", json.dumps(criteria, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
