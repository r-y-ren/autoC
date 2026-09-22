# -*- coding: utf-8 -*-
# 【中文】h2h_gate.py —— run_h2h_gate + check_zero_new_anomalies（F3）
# ===========================================================================
# 契约：fn_docs/responsibility.md 功能块 verify_offline_gates。
#   * 混合（hybrid_all_on = 提交构建全开关 main.py）vs 纯 v48：
#     ≥16 局 = 8 种子 × AB/BA 双席（席位显式：me_kind 的 agent 落 me_seat）；
#   * 混合 vs v72 + vs kgenv 线上画像池 ≥2 bot：各 ≥8 局 = 4 种子 × 双席；
#   * 判据：对 v48 互胜（胜局比例 wins/n）≥ 0.65（并列计半胜的 kgenv
#     win_rate 一并登记）；
#   * 全部局 status=DONE；异常集对照纯 v48 自打基线（同种子域 8 局）
#     零新增（check_zero_new_anomalies）。
# 逐局记录 W-L-T、席位分层、逐局终局资金。产物：gates/out/h2h_gate.json。
# CLI：python gates/h2h_gate.py [--quick]（quick=每对手 1 种子冒烟）
# ===========================================================================
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

H2H_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)   # v15_h2h_v48 基线同种子域
EXT_SEEDS = (101, 102, 201, 202)
POOL_BOTS = ("pool:scale_ranch", "pool:wheat_straw_monster")
BASELINE_SEEDS = H2H_SEEDS                              # v48 自打异常基线同种子域

OPPONENTS = (
    # (对手 kind, 种子域, 局数下限)
    ("pure_v48", H2H_SEEDS, 16),
    ("v72", EXT_SEEDS, 8),
    *[("pool_bot:" + b.split(":", 1)[1], EXT_SEEDS, 8) for b in POOL_BOTS],
)


def _opp_kind_to_load(kind: str) -> str:
    return kind.replace("pool_bot:", "pool:", 1)


def _play_series(me_kind: str, opp_kind: str, seeds, seats=(0, 1)):
    games = []
    load_opp = _opp_kind_to_load(opp_kind)
    for seed in seeds:
        for seat in seats:
            t0 = time.perf_counter()
            rec = gc.run_seated_h2h(me_kind, load_opp, seed, seat)
            slim = {
                "seed": rec["seed"], "me_seat": rec["me_seat"],
                "me_money": rec["me_money"], "opp_money": rec["opp_money"],
                "margin": round(rec["me_money"] - rec["opp_money"], 1),
                "result": ("WIN" if rec["me_win"]
                           else "TIE" if rec["me_tie"] else "LOSS"),
                "statuses": rec["statuses"],
                "turns": rec["turns_played"],
                "anomaly_kinds": rec["anomaly_kinds"],
                "wall_s": round(time.perf_counter() - t0, 1),
            }
            games.append(slim)
            print(f"  [{me_kind} vs {opp_kind}] seed={seed} seat={seat} "
                  f"me={slim['me_money']:9.1f} opp={slim['opp_money']:9.1f} "
                  f"margin={slim['margin']:+10.1f} {slim['result']:4s} "
                  f"statuses={slim['statuses']} "
                  f"anoms={slim['anomaly_kinds'] or '-'} "
                  f"[{slim['wall_s']}s]", flush=True)
    return games


def _summarize(games):
    n = len(games)
    w = sum(1 for g in games if g["result"] == "WIN")
    l = sum(1 for g in games if g["result"] == "LOSS")
    t = sum(1 for g in games if g["result"] == "TIE")
    by_seat = {}
    for seat in (0, 1):
        sub = [g for g in games if g["me_seat"] == seat]
        by_seat[str(seat)] = {
            "games": len(sub),
            "wins": sum(1 for g in sub if g["result"] == "WIN"),
            "losses": sum(1 for g in sub if g["result"] == "LOSS"),
            "ties": sum(1 for g in sub if g["result"] == "TIE"),
        }
    return {
        "games": n, "wins": w, "losses": l, "ties": t,
        "win_fraction_strict": round(w / n, 4) if n else None,
        "win_rate_half_ties": round((w + 0.5 * t) / n, 4) if n else None,
        "by_seat": by_seat,
        "all_done": all(g["statuses"] == ["DONE", "DONE"] for g in games),
        "anomaly_kinds_seen": sorted({k for g in games
                                      for k in g["anomaly_kinds"]}),
        "avg_margin": round(sum(g["margin"] for g in games) / max(1, n), 1),
    }


def run_h2h_gate(quick: bool = False) -> dict:
    """三门之一：seated h2h。返回结构化门结果（含逐对手汇总与判据）。"""
    print("== run_h2h_gate（seated 通道，AB/BA 双席显式）==", flush=True)
    t0 = time.perf_counter()
    base_sha = gc.sha256_file(gc.BASE_MAIN)
    if base_sha != gc.BASE_SHA256:
        raise SystemExit(f"基线 v48 sha 漂移: {base_sha}")

    report = {
        "protocol": "v48h-h2h-gate/1.0",
        "me": "hybrid_all_on",
        "baseline_pure_v48": {"path": gc.BASE_MAIN, "sha256": base_sha},
        "series": {},
    }

    for opp_kind, seeds, floor in OPPONENTS:
        use_seeds = seeds[:1] if quick else seeds
        print(f"-- hybrid vs {opp_kind}（seeds={use_seeds}, 双席）--",
              flush=True)
        games = _play_series("hybrid_all_on", opp_kind, use_seeds)
        summary = _summarize(games)
        summary["games_floor"] = floor
        summary["games_floor_ok"] = summary["games"] >= floor
        summary["records"] = games
        report["series"][opp_kind] = summary

    # ---- check_zero_new_anomalies：纯 v48 自打基线（同种子域）----
    print("-- 异常基线：纯 v48 自打（同种子域 8 局）--", flush=True)
    baseline_games = []
    for seed in (BASELINE_SEEDS[:1] if quick else BASELINE_SEEDS):
        t0g = time.perf_counter()
        fn0, fn1 = gc.load_agent(gc.BASE_MAIN), gc.load_agent(gc.BASE_MAIN)
        rec = gc.run_engine_game(fn0, fn1, seed)
        baseline_games.append({
            "seed": seed, "rewards": rec["rewards"],
            "statuses": rec["statuses"], "turns": rec["turns_played"],
            "anomaly_kinds": rec["anomaly_kinds"],
            "wall_s": round(time.perf_counter() - t0g, 1),
        })
        print(f"  [v48 x v48] seed={seed} rewards={rec['rewards']} "
              f"statuses={rec['statuses']} anoms={rec['anomaly_kinds'] or '-'}",
              flush=True)
    baseline_kinds = sorted({k for g in baseline_games
                             for k in g["anomaly_kinds"]})
    hybrid_kinds = sorted({k for s in report["series"].values()
                           for k in s["anomaly_kinds_seen"]})
    new_kinds = sorted(set(hybrid_kinds) - set(baseline_kinds))
    report["zero_new_anomalies"] = {
        "baseline": {"games": baseline_games, "kinds": baseline_kinds},
        "hybrid_games_kinds": hybrid_kinds,
        "new_kinds": new_kinds,
        "all_games_done": all(s["all_done"] for s in report["series"].values()),
        "passed": (not new_kinds)
        and all(s["all_done"] for s in report["series"].values()),
    }

    v48s = report["series"]["pure_v48"]
    report["gate"] = {
        "criterion": "vs pure_v48 win_fraction_strict (wins/n) >= 0.65; "
                     "games >= 16; all DONE; zero new anomaly kinds",
        "win_fraction_vs_v48": v48s["win_fraction_strict"],
        "win_rate_half_ties_vs_v48": v48s["win_rate_half_ties"],
        "games_vs_v48": v48s["games"],
        "games_floor_ok_all": all(s["games_floor_ok"]
                                  for s in report["series"].values()),
        "all_done": all(s["all_done"] for s in report["series"].values()),
        "zero_new_anomalies": report["zero_new_anomalies"]["passed"],
    }
    report["gate"]["passed"] = (
        v48s["win_fraction_strict"] is not None
        and v48s["win_fraction_strict"] >= 0.65
        and v48s["games"] >= 16
        and report["gate"]["games_floor_ok_all"]
        and report["gate"]["all_done"]
        and report["gate"]["zero_new_anomalies"])
    report["wall_s"] = round(time.perf_counter() - t0, 1)
    out = gc.write_json(os.path.join(gc.OUT_DIR, "h2h_gate.json"), report)
    print(f"h2h_gate passed = {report['gate']['passed']} "
          f"(vs v48: W{v48s['wins']}-L{v48s['losses']}-T{v48s['ties']} "
          f"互胜={v48s['win_fraction_strict']}) -> {out}", flush=True)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="v48_hybrid h2h gate (F3)")
    ap.add_argument("--quick", action="store_true",
                    help="每对手 1 种子冒烟（不构成门判据）")
    args = ap.parse_args()
    rep = run_h2h_gate(quick=args.quick)
    summary = {k: {kk: vv for kk, vv in v.items() if kk != "records"}
               for k, v in rep["series"].items()}
    print(json.dumps({"series": summary,
                      "zero_new_anomalies": rep["zero_new_anomalies"],
                      "gate": rep["gate"]},
                     ensure_ascii=False, indent=1))
    sys.exit(0 if rep["gate"]["passed"] else 1)
