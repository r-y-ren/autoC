# -*- coding: utf-8 -*-
"""assemble_evidence（track1）：A/B 账本+变体审计+挖掘验证 → 战役 evidence JSON。

产出（任务指定形态）：fn_docs/hybrid/results/2026-09-29-track1-production-route.json
（_generated_at/source/route_scan{cells,arms,ledger 摘要}/prod_variants{variants,
feasibility,pairs}/criteria/verdict/anomaly）。只读本 lab 证据件，写一个 JSON。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
EVID_DIR = MODULE_DIR / "evidence"
CAMPAIGN_ROOT = MODULE_DIR.parents[3]
OUT_PATH = (CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results"
            / "2026-09-29-track1-production-route.json")

A_LEDGER = EVID_DIR / "ab_t1a_ledger_realrun.json"
B_LEDGER = EVID_DIR / "ab_t1b_ledger_realrun.json"
VAR_AUDIT = EVID_DIR / "tape_variants_audit.json"
MINE_VAL = EVID_DIR / "mine_validate.json"
AUTH = EVID_DIR / "sim_auth.json"
SEED_PLAN = EVID_DIR / "t1a_seed_plan.json"


def main():
    a = json.loads(A_LEDGER.read_text(encoding="utf-8"))
    b = json.loads(B_LEDGER.read_text(encoding="utf-8"))
    va = json.loads(VAR_AUDIT.read_text(encoding="utf-8"))
    mv = json.loads(MINE_VAL.read_text(encoding="utf-8"))
    auth = json.loads(AUTH.read_text(encoding="utf-8"))
    plan = json.loads(SEED_PLAN.read_text(encoding="utf-8"))

    # 路线细扫逐格表（cells）
    cells = {}
    for cell, arms in a["cell_table"].items():
        cells[cell] = {}
        for rk, agg in arms.items():
            cells[cell]["r%s" % rk] = {
                "route": agg["route"], "labels": agg["labels"],
                "n": agg["n"], "n_folds": agg["n_folds"],
                "n_达标": agg["n达标"],
                "mean_delta": agg["mean_delta"],
                "mean_margin_control": agg["mean_margin_control"],
                "mean_margin_arm": agg["mean_margin_arm"],
                "win_rate_control": agg["win_rate_control"],
                "win_rate_arm": agg["win_rate_arm"],
                "net_flip_wins": agg["net_flip_wins"],
                "flips_pos": agg["flips_pos"],
                "flips_neg": agg["flips_neg"],
            }

    # 产线变体表（variants/feasibility/pairs）
    variants = {}
    for vid, v in va["variants"].items():
        twin = v.get("feasibility") or {}
        checks = twin.get("checks") or []
        variants[vid] = {
            "factor": (v.get("spec") or {}).get("factor"),
            "desc": (v.get("spec") or {}).get("desc"),
            "surgery_stats": v.get("stats"),
            "conservation_ok": (v.get("audit") or {}).get("conservation_ok"),
            "conservation_note": (v.get("audit") or {}).get(
                "conservation_note"),
            "feasibility_verdict": twin.get("verdict"),
            "feasibility_checks_n": len(checks),
            "feasibility_checks_fail_n": sum(1 for c in checks
                                             if not c.get("ok")),
            "feasibility_sample": checks[:2],
            "kept": v.get("kept"),
            "in_ab": vid in (b["config"].get("variants") or []),
            "ab_stats": (b.get("variant_stats") or {}).get(vid),
        }

    route_scan = {
        "design": "逐店对邻域细扫：时机臂 generic(r105)/early(r9)/late(r103) "
                  "+ 结构邻域臂（alt=共享一店店对非基座路线众数，本基座∈{9,105}"
                  " 与时机臂重合按强制路线记账）+ 优先格结构邻域第二线 r122"
                  "（ICE_CREAM+YARN 目标门加密臂）；格=店对；每格 n≥8 配对单元"
                  "（挖掘定向加密 ICE_CREAM+YARN 及相邻格）",
        "caliber": "配对单元=(seed,seat)（K2 口径）；局次=game（fold=games/2 同报）；"
                   "净翻胜=win_arm−win_control；margin=终局 farms[our].money−"
                   "farms[opp].money（run_games banks 干净口径）",
        "seed_mining": {
            "method": "kaggsim gengame 磁带重放（H1/对手 step<144 实录动作流）"
                      "预测店对；K2 32 seeds 实测命中 "
                      "%d/%d（双席序均中）" % (mv["validation"]["match_any"],
                                              mv["validation"]["n_seeds"]),
            "validation": {k: mv["validation"][k] for k in
                           ("n_seeds", "match_seat0", "match_seat1",
                            "match_any", "match_both")},
            "seed_domain": plan.get("seed_domain"),
            "cell_match_rate_actual": a.get("cell_match_rate"),
        },
        "cells": cells,
        "arms": a["overall"],
        "ledger_summary": {
            "games": a["games"], "games_folds": a["games_folds"],
            "n_units_paired": a["n_units_paired"],
            "config": a["config"],
            "ledger_path": a.get("ledger_path") or str(A_LEDGER),
            "units_record_fields": ["seed", "seat", "opponent", "face",
                                    "pair", "route_control", "margin_control",
                                    "arms{route,labels,margin_arm,delta}"],
        },
        "verdict": a["verdict"],
    }

    prod_variants = {
        "design": "≤10 产线变体（构建期改 H1 解码磁带产线事件，写时复制+量守恒"
                  "+审计；G2 教训只做小幅单因子）：畜群配比 4（6牛11羊 arch 换链）"
                  "+ 作物配比 4（麦:萝卜 ±10/20%）+ 时点 2（买地/雇工 ±1 拍）",
        "tape_surgery": {
            "decode": "orderbook_r37.retape_sheep._decode_routes（_R108_DATA "
                      "blob）；写时复制 _cow_action/_commit_action；"
                      "_encode_routes 四重自检链",
            "conservation": "畜群换链保总量（混 7牛9羊=16 头菜单口径）；作物种植"
                            "总量守恒；时点仅平移；审计表逐事件 from/to",
            "prescreen_timing": va.get("timing_prescreen"),
        },
        "feasibility": {
            "method": "gengame 磁带重放孪生空跑（变体路由计划 vs 基线，3 路由"
                      "×2 seed）；三闸=现金（逐日 money≥0）/劳动（期末棚内滞留"
                      "畜==0 且落位+滞留==计划头数）/棚容（落位≤结构数×max_held）",
            "gate": "违规即弃（spec 口径）",
        },
        "variants": variants,
        "pairs": {
            "caliber": "变体 vs H1 原版配对（ab_r41/K2 净翻胜定义）：control=H1 "
                       "vs 对手 O，arm=变体 vs 同 O，同 seed+seat；终局钱 "
                       "farms[obs.player] 干净口径",
            "corpus": b["config"]["corpus"],
            "games": b["games"],
            "games_folds": b["games_folds"],
            "n_units_paired": b["n_units_paired"],
            "variants_run": b["config"]["variants"],
            "ledger_path": b.get("ledger_path") or str(B_LEDGER),
        },
        "verdict": b["verdict"],
    }

    criteria = {
        "route_scan": "任何臂净翻胜>0 且 n 达标（每格 n≥8 配对单元）的格=正臂格；"
                      "未达标格仅线索级",
        "prod_variants": "净翻胜>0 的变体为正臂；胜局对照不翻负（control 胜局"
                         "单元 variant margin<0 翻负数==0）",
        "feasibility": "每变体 feasibility 孪生空跑先行，劳动/现金/棚容违规即弃",
    }

    verdict = {
        "route_scan": a["verdict"],
        "prod_variants": b["verdict"],
        "combined": {
            "route_positive_cells": [
                "%s/r%d(%s) netflip=%+d n=%d" % (
                    p["cell"], p["route"], p["labels"][0],
                    p["net_flip_wins"], p["n"])
                for p in a["verdict"]["positive_cells"]],
            "prod_positive_variants": list(
                b["verdict"]["positive_variants"]),
            "summary": "路线：ICE_CREAM+YARN/r105(generic/alt) 正翻胜格成立"
                       "（n=16 达标，K2 线索 4 倍加密后复现 +1，钱效应 +%0.0f）；"
                       "其余格替代臂全负或零（H 表逐店对近最优主线成立）。"
                       "产线：%s" % (
                           next((c["r105"]["mean_delta"]
                                 for cell, c in cells.items()
                                 if cell == "ICE_CREAM_SHOP+YARN_STORE"
                                 and "r105" in c), 0.0),
                           b["verdict"]["verdict"]),
        },
    }

    anomaly = [
        "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
        "harness 噪声：kaggle_environments 可选环境加载告警——无关环境忽略",
        "world 非 seed 纯函数（weeds RNG 逐空格抽；idle 驱动 0/32 不可预测）——"
        "seed 挖掘改用 H1/对手实录磁带 gengame 重放，K2 32/32 命中、A 实跑 "
        "cell_match_rate=1.0",
        "结构邻域臂与时机臂重合：本基座 alt(邻域众数)∈{9,105}==early/generic，"
        "账本按强制路线记标签（共享处理跑，n 不双计）",
        "时点方向预筛：雇工 −1 拍=跨日界清手全季无工（孪生判死）、+1 拍亦判死"
        "（雇工流与日界强耦合，±1 拍均不可行→hire 变体弃）；买地 −1 拍部分路由"
        "走位错位判死、+1 拍过→land_shift=+1 拍",
        "畜群扩容手术（羊13/15、牛8）：换链后计划头数可对上但期末 1 头滞留棚"
        "（放置链残留）或丢 4 头（sheep15 四连换链崩链）——孪生劳动闸判弃；"
        "混 7牛9羊（−1 头菜单口径）计划 16/16 全落位=唯一存活畜群臂",
        "crop_wheat_p20：+20% 换项后 6 头畜买/放失败（早期现金极紧 min_money=27"
        " 基线，种子配比扰动挤死买畜）——孪生判弃；±10%/−20% 存活",
        "B 语料口径自释：任务『26 败局+新中性块 672000+i*41，n=16 双席/变体』"
        "按 n=16 双席 fold/变体执行，16 fold=8 败局回放（canonical 前 8）+8 新"
        "中性（672000+i*41 i=0..7）分层；败局余 18 fold 未入（预算 300 局次内 "
        "10 变体不可容 42 fold 全语料）",
        "B 局次口径：32 control 共享 + 32×5 变体=192 games（96 folds）≤300；"
        "A=248 games（124 folds）≤250",
    ]

    out = {
        "_generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "version": "track1-production-route/1.0",
        "source": {
            "base_main": str(k2_h1_path()),
            "base_main_sha256": "76b5f842249efa4c89ef841e51212d7cefc8862236"
                                "55683eeb6764974b22f337",
            "tools": ["orderbook_iterk_lab/ab_k2.py（尾块换 _IMPL.chassis."
                      "router/build_alt_table/_pair_key/_ab_play_batch 账本口径"
                      "复用扩展）", "orderbook_r40/ab_r41.py", "sim_bridge"
                      "（先认证 30/30）", "kaggsim gengame（挖掘+孪生）",
                      "orderbook_r37/retape_sheep（磁带编解码+写时复制）"],
            "sim_auth": {k: auth.get(k) for k in
                         ("consistency", "consistency_ok", "wall_speedup",
                          "engine")},
            "workers": 2,
            "commands": ["python3 orderbook_track1_lab/ab_t1a.py",
                         "python3 orderbook_track1_lab/tape_variants.py",
                         "python3 orderbook_track1_lab/ab_t1b.py",
                         "python3 orderbook_track1_lab/assemble_evidence.py"],
            "evidence_paths": [
                str(A_LEDGER), str(B_LEDGER), str(VAR_AUDIT), str(MINE_VAL),
                str(AUTH), str(SEED_PLAN)],
            "budget": {
                "A_cap_局次": 250, "A_games": a["games"]["total"],
                "A_folds": a["games"]["total"] // 2,
                "B_cap_局次": 300, "B_games": b["games"]["total"],
                "B_folds": b["games"]["total"] // 2,
                "auth_games_separate": 60,
                "mining_games_separate": 8,
            },
        },
        "route_scan": route_scan,
        "prod_variants": prod_variants,
        "criteria": criteria,
        "verdict": verdict,
        "anomaly": anomaly,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    print("written:", OUT_PATH)
    return out


def k2_h1_path():
    return (MODULE_DIR.parent / "orderbook_strongest_lab" / "build" / "h1"
            / "main.py")


if __name__ == "__main__":
    main()
