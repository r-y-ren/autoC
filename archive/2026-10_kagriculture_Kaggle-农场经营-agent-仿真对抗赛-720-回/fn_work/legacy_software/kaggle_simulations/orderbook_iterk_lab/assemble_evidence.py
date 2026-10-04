# -*- coding: utf-8 -*-
"""assemble_evidence（iterk）：K1/K2 重访判决 → 证据文件
fn_docs/hybrid/results/2026-09-29-iter1-k.json（契约键同前；K2 段=ab 账本摘要）。

读 orderbook_iterk_lab/evidence/ 三件（build/judge/ab）汇总判据逐条与判决；
只写证据文件一处（任务指定路径）。
"""
from __future__ import annotations

import json
import os
import time

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(MODULE_DIR)
CAMPAIGN = os.path.dirname(os.path.dirname(os.path.dirname(KSIM)))
EVID = os.path.join(MODULE_DIR, "evidence")
OUT = os.path.join(CAMPAIGN, "fn_docs", "hybrid", "results",
                   "2026-09-29-iter1-k.json")


def _load(name):
    with open(os.path.join(EVID, name), encoding="utf-8") as fh:
        return json.load(fh)


def _pair_lite(agg):
    return {
        "n": agg.get("n_games"), "wins": agg.get("wins"),
        "losses": agg.get("losses"), "ties": agg.get("ties"),
        "h2h": agg.get("h2h"), "mean_margin": agg.get("mean_margin"),
        "ours": agg.get("ours"), "opp_side": agg.get("opp_side"),
        "margin_per_game": agg.get("margin_per_game"),
        "n_error_games": agg.get("n_error_games"),
        "replay_r30_26": {k: agg.get("replay_r30_26", {}).get(k)
                          for k in ("h2h", "wins", "losses", "ties",
                                    "mean_margin")},
        "neutral_672000_i37": {k: agg.get("neutral_672000_i37", {}).get(k)
                               for k in ("h2h", "wins", "losses", "ties",
                                         "mean_margin")},
    }


def main():
    build = _load("build_k1_realrun.json")
    judge = _load("judge_k1_realrun.json")
    ab_led = _load("ab_k2_ledger_realrun.json")
    manifest = build["manifest"]

    pairs = judge["pairs"]
    k1_vs_h1 = pairs["k1_vs_h1"]
    k1_vs_wfr = pairs["k1_vs_wfr"]
    h1_vs_wfr = pairs["h1_vs_wfr"]

    # ---- 判据逐条 ----
    c1 = {
        "name": "K1 对反制臂胜率 ≥ H1 基线（防御有效）",
        "readings": {
            "k1_vs_wfr_h2h": k1_vs_wfr.get("h2h"),
            "h1_vs_wfr_h2h_baseline": h1_vs_wfr.get("h2h"),
            "k1_vs_wfr_WLT": [k1_vs_wfr.get("wins"), k1_vs_wfr.get("losses"),
                              k1_vs_wfr.get("ties")],
            "h1_vs_wfr_WLT": [h1_vs_wfr.get("wins"), h1_vs_wfr.get("losses"),
                              h1_vs_wfr.get("ties")],
            "k1_vs_wfr_mean_margin": k1_vs_wfr.get("mean_margin"),
            "h1_vs_wfr_mean_margin": h1_vs_wfr.get("mean_margin"),
            "k1_vs_wfr_realized_px": k1_vs_wfr.get("ours", {}).get(
                "realized_px_median"),
            "h1_vs_wfr_realized_px": h1_vs_wfr.get("ours", {}).get(
                "realized_px_median"),
            "k1_vs_wfr_terminal_money": k1_vs_wfr.get("ours", {}).get(
                "terminal_money_median"),
            "h1_vs_wfr_terminal_money": h1_vs_wfr.get("ours", {}).get(
                "terminal_money_median"),
        },
    }
    k1_h2h_wfr = float(k1_vs_wfr.get("h2h") or 0)
    h1_h2h_wfr = float(h1_vs_wfr.get("h2h") or 0)
    c1["verdict"] = ("PASS" if k1_h2h_wfr >= h1_h2h_wfr else "FAIL")

    c2 = {
        "name": "常规语料 K1 对 H1 h2h ≥ 0.5（零代价）",
        "readings": {
            "k1_vs_h1_h2h": k1_vs_h1.get("h2h"),
            "k1_vs_h1_WLT": [k1_vs_h1.get("wins"), k1_vs_h1.get("losses"),
                             k1_vs_h1.get("ties")],
            "k1_vs_h1_mean_margin": k1_vs_h1.get("mean_margin"),
            "k1_vs_h1_realized_px": k1_vs_h1.get("ours", {}).get(
                "realized_px_median"),
            "k1_vs_h1_terminal_money": k1_vs_h1.get("ours", {}).get(
                "terminal_money_median"),
        },
    }
    k1_h2h_h1 = float(k1_vs_h1.get("h2h") or 0)
    c2["verdict"] = "PASS" if k1_h2h_h1 >= 0.5 else "FAIL"

    ab_verdict = ab_led.get("verdict") or {}
    # 逐店对异质性（R24 口径）：每 (pair, arm) 格净翻胜
    cells = {}
    for u in ab_led.get("units") or []:
        for arm, m in (u.get("margins") or {}).items():
            if m is None:
                continue
            c = cells.setdefault((u.get("pair"), arm), [0, 0, 0])
            c[0] += 1
            c[1] += 1 if u["margin_control"] > 0 else 0
            c[2] += 1 if m > 0 else 0
    pos_cells = [{"pair": k[0], "arm": k[1], "n": v[0],
                  "win_control": v[1], "win_arm": v[2], "net": v[2] - v[1]}
                 for k, v in cells.items() if v[2] - v[1] > 0]
    c3 = {
        "name": "K2 路线表因果 A/B：任何替代臂净翻胜>0（有→该臂候选；无→H 表近最优复证）",
        "readings": {
            "net_flip_wins": ab_verdict.get("net_flip_wins"),
            "n_units_paired": ab_led.get("n_units_paired"),
            "n_units_treated": ab_led.get("n_units_treated"),
            "overall": (ab_led.get("arm_stats") or {}).get("overall"),
            "per_pair_cells_total": len(cells),
            "per_pair_cells_net_positive": pos_cells,
        },
        "verdict": ab_verdict.get("verdict"),
        "note": ("逐店对格 2/31 正（ICE_CREAM_SHOP+YARN_STORE，n=4，净 +2/臂）"
                 "——小样本异质性线索；臂级净翻胜全负（-34/-10），判据本体="
                 "臂级，verdict 不翻"),
    }

    budget = dict(judge.get("budget") or {})
    budget["k2_games"] = (ab_led.get("n_games_total")
                          or (ab_led.get("n_units_planned", 0)
                              + sum((ab_led.get("n_units_treated") or {}).values())))
    budget["total_games_all"] = (budget.get("total_games", 0)
                                 + budget.get("k2_games", 0))

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "iter1-k/1.0",
        "experiment": "iter1-k（K1 反制对手防御 + K2 路线表因果 A/B 旧策略重访）",
        "mode": "换底座换语境重访（底=H1 最强版；判决先行·不发射·不提交）",
        "source": judge.get("source"),
        "builds": {
            "h1_base": manifest["forms"]["h1_base"],
            "k1": manifest["forms"]["k1"],
            "k1_surgery_stats": manifest["stats"],
            "k1_semantics": manifest["semantics"],
            "counter_rebuild": (judge.get("source") or {}).get(
                "counter_rebuild"),
        },
        "layer_scope": {
            "k1": "最小磁带手术（剪毛刀 d17/20/23/26→d+1/d+2，d29 保留；量守恒零跨拍）",
            "k2": "尾块覆盖 step144 店对选路（day27 换线保留；末 callable 归一）",
        },
        "pairs": {k: _pair_lite(v) for k, v in pairs.items()},
        "shear_phase_table": judge.get("shear_phase_table"),
        "criteria": {"c1_counter_arm_not_dropped": c1,
                     "c2_zero_cost_vs_h1": c2,
                     "c3_route_ab_net_flip": c3},
        "k2": {
            "ab_ledger_summary": {
                "version": ab_led.get("version"),
                "config": ab_led.get("config"),
                "n_units_planned": ab_led.get("n_units_planned"),
                "n_units_paired": ab_led.get("n_units_paired"),
                "n_units_treated": ab_led.get("n_units_treated"),
                "arm_stats": ab_led.get("arm_stats"),
                "verdict": ab_verdict,
                "elapsed_s": ab_led.get("elapsed_s"),
                "ledger_path": ab_led.get("ledger_path"),
            },
        },
        "verdict": {
            "k1_dual_criterion": ("双向判据：c1 对反制臂 ≥ H1 基线 %s ∧ "
                                  "c2 对 H1 h2h ≥0.5 %s"
                                  % (c1["verdict"], c2["verdict"])),
            "k1": ("K1 防御有效且零代价" if (c1["verdict"] == "PASS"
                                           and c2["verdict"] == "PASS")
                   else ("K1 防御面不降但有代价（零代价失败）"
                         if c1["verdict"] == "PASS" else "K1 防御无效")),
            "k1_zero_cost": ("零代价成立" if c2["verdict"] == "PASS"
                             else "零代价失败（对 H1 h2h %s<0.5，均差 %s）"
                             % (k1_h2h_h1, k1_vs_h1.get("mean_margin"))),
            "k2": ab_verdict.get("verdict"),
            "overall": "；".join([
                "K1（双向）: c1 %s（反制臂 h2h %s vs 基线 %s）+ c2 %s"
                "（对 H1 h2h %s，均差 %s/局）→ %s"
                % (c1["verdict"], k1_h2h_wfr, h1_h2h_wfr, c2["verdict"],
                   k1_h2h_h1, k1_vs_h1.get("mean_margin"),
                   "过" if (c1["verdict"] == "PASS"
                            and c2["verdict"] == "PASS") else "不过"),
                "K2: %s" % (ab_verdict.get("verdict"),),
            ]),
        },
        "anomalies": [
            "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
            "harness 噪声：kaggle_environments 可选环境加载告警（open_spiel_env/cabt）——无关环境忽略",
            "K1 手术覆盖=部分：相位刀 427 中 147（34.4%）可错峰（H1 磁带 12 单元"
            "逐拍满编、空闲跑稀缺；d26→27/28 零可行走位）；d29 刀季末保留（量守恒）"
            "→相位对照表 d26/d29 不动属预期",
            "反制臂专组=中性块前 10 seeds（无败局回放 seeds）——k1_vs_wfr/h1_vs_wfr "
            "replay 切片 UNKNOWN 属设计口径",
            "K2 逐店对格 ICE_CREAM_SHOP+YARN_STORE 净 +2/臂（n=4）为唯一正格线索，"
            "样本过小不翻臂级 verdict",
            "WFR 重建差分：原件 SELL WOOL 48 无库存=幻影单零效果（R22 反制件偏弱根因）；"
            "重建加 4 羊真毛供给+集毛阈值 12，倒毛实测 12 单位/次×4-5 次/局",
        ],
        "budget": budget,
        "elapsed_s": judge.get("elapsed_s"),
        "evidence_paths": [
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/build_k1_realrun.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/judge_k1_realrun.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/sim_auth.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/pair_k1_vs_h1.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/pair_k1_vs_wfr.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/pair_h1_vs_wfr.json",
            "fn_work/legacy_software/kaggle_simulations/orderbook_iterk_lab/evidence/ab_k2_ledger_realrun.json",
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    print("wrote", OUT)
    print("verdict:", out["verdict"]["overall"])
    return out


if __name__ == "__main__":
    main()
