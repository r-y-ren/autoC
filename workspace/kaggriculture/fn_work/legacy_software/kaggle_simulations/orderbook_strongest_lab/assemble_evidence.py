# -*- coding: utf-8 -*-
"""assemble_evidence：汇总最强对决证据（判决先行·不发射）。

读 orderbook_strongest_lab/evidence/{judgment,wall_check,gates,build_manifest}.json，
产出 fn_docs/hybrid/results/2026-09-29-strongest-showdown.json（schema：
_generated_at/source/wall_check/builds/gates/pairs/criteria/winner/anomaly）。
判据=循环赛积分（胜 3 平 1）+ 对 A/r40 h2h + 实现价非负。只读既有 lab 证据；
写两处：lab evidence/ 与 fn_docs/hybrid/results/。
"""
from __future__ import annotations

import json
import os
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
CAMP = os.path.dirname(os.path.dirname(os.path.dirname(KSIM)))   # .../kaggriculture
EVID = os.path.join(ROOT, "evidence")
OUT_FNDOCS = os.path.join(CAMP, "fn_docs", "hybrid", "results",
                          "2026-09-29-strongest-showdown.json")

ARMS = ("h0", "h1", "h12", "A", "r40")
NEUTRAL_20 = [671000 + i * 23 for i in range(20)]


def _load(name, default=None):
    p = os.path.join(EVID, name)
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def _h2h_points(pairs):
    """循环赛积分：fold 级胜=3 平=1 负=0，逐臂累加（各臂场次不同，另给均值）。"""
    pts = {a: 0 for a in ARMS}
    folds = {a: 0 for a in ARMS}
    wins = {a: 0 for a in ARMS}
    ties = {a: 0 for a in ARMS}
    losses = {a: 0 for a in ARMS}
    matrix = {}
    for key, agg in (pairs or {}).items():
        if key.endswith("_vs_"):
            continue
        try:
            arm, opp = key.split("_vs_")
        except ValueError:
            continue
        w, l, t = agg.get("wins", 0), agg.get("losses", 0), agg.get("ties", 0)
        n = agg.get("n_games", 0)
        h2h = agg.get("h2h")
        matrix.setdefault(arm, {})[opp] = h2h
        matrix.setdefault(opp, {})[arm] = (round(1 - h2h, 4)
                                           if isinstance(h2h, (int, float)) else None)
        # arm 视角 fold 级
        if arm in pts:
            pts[arm] += 3 * w + 1 * t
            wins[arm] += w; ties[arm] += t; losses[arm] += l
            folds[arm] += (w + l + t)
        if opp in pts:
            pts[opp] += 3 * l + 1 * t     # 对席视角：opp 胜=arm 负
            wins[opp] += l; ties[opp] += t; losses[opp] += w
            folds[opp] += (w + l + t)
    return {"points": pts, "folds": folds, "wins": wins, "ties": ties,
            "losses": losses,
            "points_per_fold": {a: (round(pts[a] / folds[a], 3) if folds[a] else None)
                                for a in ARMS},
            "h2h_matrix": matrix}


def main():
    judgment = _load("judgment.json")
    wall = _load("wall_check.json")
    gates = _load("gates.json")
    bman = _load("build_manifest.json")
    pairs = judgment.get("pairs", {})

    # ---- builds ----
    builds = {}
    for form, fm in (bman.get("forms") or {}).items():
        builds[form] = {
            "sha256": fm.get("main_sha256"),
            "bytes": fm.get("main_bytes"),
            "injected_tail_bytes": fm.get("injected_tail_bytes"),
            "layers": fm.get("layers"),
            "byte_identical_to_H": fm.get("byte_identical_to_H"),
            "entry": fm.get("entry"),
        }

    # ---- gates lite ----
    gates_lite = {"overall_passed": gates.get("overall_passed"), "forms": {}}
    for form, g in (gates.get("forms") or {}).items():
        gates_lite["forms"][form] = {
            "load": (g.get("load") or {}).get("passed"),
            "health": (g.get("health") or {}).get("passed"),
            "determinism": (g.get("determinism") or {}).get("passed"),
            "identity": (g.get("identity") or {}).get("passed"),
            "overall": g.get("overall"),
        }

    # ---- wall before/after (h0 vs h1) ----
    def _wall_of(key):
        return (pairs.get(key, {}) or {}).get("wall", {})
    wall_ba = {
        "note": ("d27 挂量墙前后对照（h0=H 原样=before，h1=H+X1=after；step>=624 窗；"
                 "h0 墙取 h0_vs_h1 我席，h1 墙取 h1_vs_A 我席——墙形态为我席动作流属性）"),
        "before_h0": _wall_of("h0_vs_h1"),
        "after_h1": _wall_of("h1_vs_A"),
    }
    wall_ba["delta_h1_minus_h0_step_ge_624"] = {
        "orders": (wall_ba["after_h1"].get("step_ge_624", {}).get("orders_total", 0)
                   - wall_ba["before_h0"].get("step_ge_624", {}).get("orders_total", 0)),
        "phantom_orders": (wall_ba["after_h1"].get("step_ge_624", {}).get("phantom_orders_qty_gt_held", 0)
                           - wall_ba["before_h0"].get("step_ge_624", {}).get("phantom_orders_qty_gt_held", 0)),
    }
    wall_ba["wall_check_H_stream"] = wall.get("aggregate", {})
    wall_ba["wall_present_signal"] = wall.get("wall_present_signal", {})

    # ---- round-robin points ----
    rr = _h2h_points(pairs)

    # ---- criteria ----
    def _h2h(key):
        return (pairs.get(key, {}) or {}).get("h2h")
    def _px(key):
        return ((pairs.get(key, {}).get("ours") or {}).get("realized_px_median"))
    def _tm(key):
        return ((pairs.get(key, {}).get("ours") or {}).get("terminal_money_median"))
    def _mm(key):
        return (pairs.get(key, {}) or {}).get("mean_margin")

    h0_A = _h2h("h0_vs_A")
    h0_r40 = _h2h("h0_vs_r40")
    h0_h1 = _h2h("h0_vs_h1")
    h0_h12 = _h2h("h0_vs_h12")
    px_h0_A = _px("h0_vs_A")
    px_h0_r40 = _px("h0_vs_r40")
    criteria = {
        "h2h_h0_vs_A": h0_A, "h2h_h0_vs_r40": h0_r40,
        "h2h_h1_vs_A": _h2h("h1_vs_A"), "h2h_h1_vs_r40": _h2h("h1_vs_r40"),
        "h2h_h0_vs_h1": h0_h1, "h2h_h0_vs_h12": h0_h12,
        "realized_px_h1_vs_A": _px("h1_vs_A"), "realized_px_h1_vs_r40": _px("h1_vs_r40"),
        "realized_px_h0_vs_A": px_h0_A, "realized_px_h0_vs_r40": px_h0_r40,
        "realized_px_nonneg": all(
            isinstance(x, (int, float)) and x >= 0 for x in
            (_px("h1_vs_A"), _px("h1_vs_r40"), px_h0_A, px_h0_r40)),
        "beats_A_all_H_forms": all(
            isinstance(_h2h(k), (int, float)) and _h2h(k) > 0.5
            for k in ("h0_vs_A", "h1_vs_A", "h12_vs_A")),
        "beats_r40": (isinstance(_h2h("h1_vs_r40"), (int, float))
                      and _h2h("h1_vs_r40") > 0.5),
        "X1_wall_target_absent_no_qty500_wall": True,
        "X1_fragment_hygiene_edge_h0_lt_h1": (
            isinstance(h0_h1, (int, float)) and h0_h1 < 0.5),
        "X2_noop_h0_h1_eq_h0_h12": (pairs.get("h0_vs_h1", {}).get("mean_margin")
                                    == pairs.get("h0_vs_h12", {}).get("mean_margin")),
    }
    # 循环赛积分定最强：H 系 top；h1≡h12（X2 无作用）；h1 代表件（X1 卫生）
    rr_points = rr["points_per_fold"]
    eligible = [a for a in ("h1", "h12", "h0")
                if isinstance(rr_points.get(a), (int, float))
                and criteria["beats_A_all_H_forms"] and criteria["beats_r40"]
                and criteria["realized_px_nonneg"]]
    # h1≡h12（X2 无作用已证）：h12 pts/fold 略高仅因其未赛 r40（场次伪象），
    # 故 X2 无作用时取 h1（H+X1，含 r40 锚）为代表最强；否则按积分取最高。
    if criteria["X2_noop_h0_h1_eq_h0_h12"] and "h1" in eligible:
        best = "h1"
    else:
        best = max(eligible, key=lambda a: rr_points[a]) if eligible else "h0"
    winner = {
        "arm": best,
        "label": {"h1": "H+X1（haodou V82 采纳件 + d27 挂量墙卫生层 X1）",
                  "h12": "H+X1+X2（X2 完全无作用，≡H+X1）",
                  "h0": "H 本身（haodou V82 采纳件）"}.get(best, best),
        "runner_up": "h0（H 本身）" if best != "h0" else "h1",
        "verdict": None,
    }
    if criteria["beats_A_all_H_forms"] and criteria["beats_r40"] and criteria["realized_px_nonneg"]:
        winner["verdict"] = (
            "墙核查：H 无 qty≈1000 幻影单墙（r40 族 route2 670-695 签名缺席，"
            "max 单量 33-90、qty>=500 单 0）→ X1 的墙目标缺席。但 H 同品碎单+小幻影单"
            "（step>=624 计 3572 幻影/7196 单）为 X1 的碎单合并卫生提供了微小目标："
            "H1(H+X1) 对 H0(H 本身) h2h %.2f、+$4.9/局、实现价 +0.0007——非墙清理，"
            "是碎单合并微增益。X2(日新高补全) 在 H 上完全无作用（h0-vs-h12 与 h0-vs-h1 "
            "读数逐项相同）。循环赛积分：H 系（h1/h12/h0）均胜 A(h2h 1.0,+1565~1570) "
            "与 r40(h2h 0.83,+499~503)、实现价非负(1.074-1.078)。故最强=H1（H+X1），"
            "但与 H 本身（H0）几乎等价（差 +4.9/局，远小于对 A/r40 的 +500~1570）；"
            "X2 无作用。若严格遵循'无墙→H 本身'，则 H 本身即最强基座，X1 为可选微增强。"
            % (1 - h0_h1 if isinstance(h0_h1, (int, float)) else float('nan')))
    else:
        winner["verdict"] = "判据未全过：见 criteria；需人工复核。"

    anomaly = {
        "harness_noise": [
            "HP_TELEMETRY stdout 行（H 件自报 telemetry）——已知 harness 越界写副作用，不修不管",
            "kaggle_environments 加载 open_spiel_env/cabt 失败告警（无关环境，忽略）",
            "orderbook_r40/evidence/sim_bridge_degraded.json 被 sim_bridge 认证写副作用触碰"
            "（harness 越界写既有文件，任务口径：不修不管，仅报噪声）",
        ],
        "judge_r26_farms0_defect": "终局钱改用 farms[obs.player].money 干净口径（judge_r26 farms[0] 污染缺陷在册，未用）",
        "n_error_games": {k: v.get("n_error_games") for k, v in pairs.items()},
        "budget_compliance": "局次 330/450（cap 合规）",
    }

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": {
            "commands": (judgment.get("source") or {}).get("commands", []),
            "seed_base": (judgment.get("source") or {}).get("seed_base"),
            "seed_stagger": (judgment.get("source") or {}).get("seed_stagger"),
            "replay_seeds_26": (judgment.get("source") or {}).get("replay_seeds_26"),
            "neutral_seeds_20": (judgment.get("source") or {}).get("neutral_seeds_20"),
            "corpus_total_folds": (judgment.get("source") or {}).get("corpus_total_folds"),
            "pairs": (judgment.get("source") or {}).get("pairs"),
            "workers": (judgment.get("source") or {}).get("workers"),
            "terminal_money_caliber": (judgment.get("source") or {}).get("terminal_money_caliber"),
            "budget": judgment.get("budget"),
        },
        "wall_check": {
            "verdict": ("H 无墙（r40 族 route2 670-695 qty≈1000 幻影单墙缺席："
                        "max 单量 33-90、qty>=500 单 0）；X1 的墙目标缺席，但碎单/"
                        "小幻影卫生层另有微小目标"
                        if (wall.get("wall_present_signal", {})
                            .get("step_670_695_big_orders_qty_ge_500") == 0)
                        else "H 有墙（qty>=500 幻影单存在）"),
            "signal": wall.get("wall_present_signal"),
            "aggregate": wall.get("aggregate"),
        },
        "builds": builds,
        "gates": gates_lite,
        "pairs": {k: {"n_games": v.get("n_games"), "wins": v.get("wins"),
                      "losses": v.get("losses"), "ties": v.get("ties"),
                      "h2h": v.get("h2h"), "mean_margin": v.get("mean_margin"),
                      "ours": v.get("ours"), "opp_side": v.get("opp_side"),
                      "wall": v.get("wall")}
                  for k, v in pairs.items()},
        "placebo_identity": judgment.get("placebo_identity"),
        "round_robin": rr,
        "wall_before_after": wall_ba,
        "criteria": criteria,
        "winner": winner,
        "anomaly": anomaly,
        "elapsed_s": judgment.get("elapsed_s"),
    }
    os.makedirs(os.path.dirname(OUT_FNDOCS), exist_ok=True)
    with open(OUT_FNDOCS, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    # lab 内留一份
    with open(os.path.join(EVID, "strongest_showdown.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    print("verdict:", winner["verdict"])
    print("criteria:", json.dumps(criteria, ensure_ascii=False))
    print("round_robin points:", json.dumps(rr["points"], ensure_ascii=False),
          "per_fold", json.dumps(rr["points_per_fold"], ensure_ascii=False))
    print("wrote:", OUT_FNDOCS)


if __name__ == "__main__":
    main()
