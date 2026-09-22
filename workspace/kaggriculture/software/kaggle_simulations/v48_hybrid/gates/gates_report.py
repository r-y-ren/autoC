# -*- coding: utf-8 -*-
# 【中文】gates_report.py —— F3 汇总：三门 + 安全证明 → gates_report.json
# ===========================================================================
# 运行 run_h2h_gate（含 check_zero_new_anomalies）、run_panel_gate、
# verify_patch_safety（中性注入 + P2/P3 零影响 + P1 归因诊断），汇总为
# gates/gates_report.json + 控制台逐门 PASS/FAIL 表，并回填
# build_manifest.json 的 gate_results 占位（F3 设计回填点；仅改该字段，
# 其余键原样保留）。launch_fourgate 引用 F2 冒烟产物
# （tmp/probes/v48_hybrid_smoke.json，不重跑）。
# CLI：python gates/gates_report.py [--skip-run]（--skip-run 只重汇总
#   gates/out/ 既有门 JSON，不重跑对局）
# ===========================================================================
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

SMOKE_JSON = os.path.join(gc.HYB, "tmp", "probes", "v48_hybrid_smoke.json")
MANIFEST = os.path.join(gc.HYB, "build_manifest.json")


def load_launch_fourgate() -> dict:
    """F2 冒烟（发射四件套）结果引用。"""
    if not os.path.isfile(SMOKE_JSON):
        return {"source": SMOKE_JSON, "available": False,
                "status": "MISSING（F2 冒烟产物不在场，需重跑 "
                          "tmp/smoke_launch.py）"}
    with open(SMOKE_JSON, encoding="utf-8") as h:
        d = json.load(h)
    return {
        "source": "tmp/probes/v48_hybrid_smoke.json（F2 批次，引用不重跑）",
        "available": True,
        "status": "PASS" if d.get("all_gates_pass") else "FAIL",
        "gate1_official_load_ok": d.get("gate1_official_load",
                                        {}).get("gate1_official_load_ok"),
        "gate2_full_episodes_ok": d.get("gate2_full_episodes",
                                        {}).get("gate2_full_episodes_ok"),
        "gate3_determinism_ok": d.get("gate2_full_episodes",
                                      {}).get("gate3_determinism_ok"),
        "gate4_size_ok": d.get("package", {}).get("gate4_size_ok"),
    }


def collect(skip_run: bool = False) -> dict:
    if skip_run:
        with open(os.path.join(gc.OUT_DIR, "h2h_gate.json"),
                  encoding="utf-8") as h:
            h2h = json.load(h)
        with open(os.path.join(gc.OUT_DIR, "panel_gate.json"),
                  encoding="utf-8") as h:
            panel = json.load(h)
        with open(os.path.join(gc.OUT_DIR, "patch_safety.json"),
                  encoding="utf-8") as h:
            psafe = json.load(h)
    else:
        import h2h_gate
        import panel_gate
        import patch_safety
        h2h = h2h_gate.run_h2h_gate()
        panel = panel_gate.run_panel_gate()
        psafe = patch_safety.run_patch_safety()

    with open(MANIFEST, encoding="utf-8") as h:
        manifest = json.load(h)

    gates = {
        "h2h": {
            "status": "PASS" if h2h["gate"]["passed"] else "FAIL",
            "vs_v48": f"W{h2h['series']['pure_v48']['wins']}-"
                      f"L{h2h['series']['pure_v48']['losses']}-"
                      f"T{h2h['series']['pure_v48']['ties']} "
                      f"/ {h2h['series']['pure_v48']['games']} 局，"
                      f"互胜={h2h['gate']['win_fraction_vs_v48']}"
                      f"（判据≥0.65）",
            "vs_others": {k: f"W{v['wins']}-L{v['losses']}-T{v['ties']} "
                             f"/ {v['games']} 局"
                          for k, v in h2h["series"].items()
                          if k != "pure_v48"},
            "detail": h2h["gate"],
        },
        "panel": {
            "status": "PASS" if panel["gate"]["passed"] else "FAIL",
            "numbers": f"全局 ratio={panel['global_ratio']}，逐局="
                       f"{panel['gate']['per_game_ratios']}（判据≥0.98，"
                       f"语料=合成 {panel['corpus']['n_games']} 局）",
            "corpus_kind": panel["corpus"]["kind"],
            "detail": panel["gate"],
        },
        "zero_new_anomalies": {
            "status": "PASS" if h2h["zero_new_anomalies"]["passed"]
            else "FAIL",
            "numbers": f"基线自打 kinds="
                       f"{h2h['zero_new_anomalies']['baseline']['kinds']}，"
                       f"混合局 kinds="
                       f"{h2h['zero_new_anomalies']['hybrid_games_kinds']}，"
                       f"新增={h2h['zero_new_anomalies']['new_kinds']}，"
                       f"全 DONE="
                       f"{h2h['zero_new_anomalies']['all_games_done']}",
            "detail": {k: v for k, v in
                       h2h["zero_new_anomalies"].items()
                       if k != "baseline"},
        },
        "patch_safety": {
            "status": "PASS" if psafe["gate"]["passed"] else "FAIL",
            "neutral_injection": psafe["neutral_injection_proof"]["summary"],
            "p23_zero_impact": psafe["p23_zero_impact_proof"]["summary"],
            "detail": psafe["gate"],
        },
        "launch_fourgate": load_launch_fourgate(),
    }
    gates["launch_fourgate"]["status"] = gates["launch_fourgate"].get(
        "status", "MISSING")

    failed = [k for k, v in gates.items() if v.get("status") != "PASS"]
    return {
        "protocol": "v48h-gates-report/1.0",
        "generated_at": _dt.date.today().isoformat(),
        "identity": {
            "hybrid_main_sha256": manifest["main_py"]["sha256"],
            "hybrid_main_bytes": manifest["main_py"]["bytes"],
            "base_sha256": manifest["base"]["sha256"],
            "submission_tar_gz_sha256":
                manifest["submission_tar_gz"]["sha256"],
            "flags": manifest["flags"],
        },
        "gates": gates,
        "overall": {
            "status": "PASS" if not failed else "FAIL",
            "failed_gates": failed,
            "note": "判据=h2h 对 v48 互胜≥0.65 / panel ratio≥0.98 / "
                    "零新异常 / patch safety 双证明；launch_fourgate 引用 "
                    "F2 冒烟。panel 语料=引擎合成（官方语料面板为主力机"
                    "补测项）。",
        },
        "p1_attribution": psafe["p1_attribution_diagnostic"]["summary"],
        "artifact_paths": {
            "h2h": "gates/out/h2h_gate.json",
            "panel": "gates/out/panel_gate.json",
            "patch_safety": "gates/out/patch_safety.json",
        },
    }


def backfill_manifest(report: dict) -> dict:
    """回填 build_manifest.json 的 gate_results 占位（仅该字段）。"""
    with open(MANIFEST, encoding="utf-8") as h:
        manifest = json.load(h)
    g = report["gates"]
    manifest["gate_results"] = {
        "status": report["overall"]["status"],
        "note": "F3 verify_offline_gates + verify_patch_safety 回填；"
                "细节 gates/gates_report.json，逐门 JSON 在 gates/out/",
        "h2h": {"status": g["h2h"]["status"],
                "win_fraction_vs_v48":
                    g["h2h"]["detail"]["win_fraction_vs_v48"],
                "games_vs_v48": g["h2h"]["detail"]["games_vs_v48"],
                "criterion": ">=0.65 over >=16 seated games"},
        "panel": {"status": g["panel"]["status"],
                  "global_ratio": g["panel"]["detail"]["global_ratio"],
                  "per_game_ratios": g["panel"]["detail"]["per_game_ratios"],
                  "corpus": g["panel"]["corpus_kind"],
                  "criterion": ">=0.98 per-game and global"},
        "zero_new_anomalies": {
            "status": g["zero_new_anomalies"]["status"],
            "new_kinds": g["zero_new_anomalies"]["detail"]["new_kinds"],
            "all_games_done":
                g["zero_new_anomalies"]["detail"]["all_games_done"]},
        "patch_safety": {"status": g["patch_safety"]["status"],
                         "neutral_injection_equivalent":
                             g["patch_safety"]["neutral_injection"][
                                 "all_streams_byte_equal"],
                         "p23_unexpected_divergence":
                             g["patch_safety"]["p23_zero_impact"][
                                 "n_unexpected_divergence"],
                         "p23_effective_triggers":
                             g["patch_safety"]["p23_zero_impact"][
                                 "effective_trigger_events"]},
        "launch_fourgate": {"status": g["launch_fourgate"]["status"],
                            "source": g["launch_fourgate"].get(
                                "source", "F2 smoke")},
        "failed_gates": report["overall"]["failed_gates"],
    }
    with open(MANIFEST, "w", encoding="utf-8") as h:
        json.dump(manifest, h, indent=2, sort_keys=True)
        h.write("\n")
    return manifest


def print_summary(report: dict) -> None:
    print("\n" + "=" * 74)
    print("v48_hybrid F3 门禁汇总（判据：互胜≥0.65 / ratio≥0.98 / "
          "零新异常 / 安全证明）")
    print("=" * 74)
    for name, g in report["gates"].items():
        status = g.get("status", "?")
        line = f"  [{status:4s}] {name}"
        if name == "h2h":
            line += f"：{g['vs_v48']}"
        elif name == "panel":
            line += f"：{g['numbers']}"
        elif name == "zero_new_anomalies":
            line += f"：{g['numbers']}"
        elif name == "patch_safety":
            n = g["neutral_injection"]
            p = g["p23_zero_impact"]
            line += (f"：中性注入 p000≡基底 streams_equal="
                     f"{n['all_streams_byte_equal']}（{n['n_seeds']} 种子）；"
                     f"P2/P3 全开≡p100 意外分叉="
                     f"{p['n_unexpected_divergence']}/{p['n_seeds']} 种子，"
                     f"有效触发 p2={sum(v['p2_vetoes'] for v in p['effective_trigger_events'].values())}"
                     f" p3={sum(v['p3_adjusts'] for v in p['effective_trigger_events'].values())}")
        elif name == "launch_fourgate":
            line += f"：{g.get('source', '')}"
        print(line)
    print("-" * 74)
    print(f"  总体 {report['overall']['status']}"
          + (f"（FAIL 门：{', '.join(report['overall']['failed_gates'])}）"
             if report["overall"]["failed_gates"] else ""))
    print(f"  P1 归因（诊断）：{json.dumps(report['p1_attribution'].get(
        'real_rewards', {}), ensure_ascii=False)}")
    print("=" * 74)


def main() -> int:
    ap = argparse.ArgumentParser(description="v48_hybrid F3 gates report")
    ap.add_argument("--skip-run", action="store_true",
                    help="只重汇总 gates/out/ 既有 JSON")
    args = ap.parse_args()
    report = collect(skip_run=args.skip_run)
    out = gc.write_json(os.path.join(gc.HYB, "gates", "gates_report.json"),
                        report)
    print_summary(report)
    backfill_manifest(report)
    print(f"report -> {out}")
    print(f"manifest gate_results 回填 -> {MANIFEST} "
          f"(status={report['overall']['status']})")
    return 0 if report["overall"]["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
