# -*- coding: utf-8 -*-
"""make_evidence（fullplan lab）：汇总 B4c 全计划重建证据 →
fn_docs/hybrid/results/2026-09-29-goose-fullplan.json（任务规定证据位）。

节构：dissect / top_params / rebuild{schedule,labor,assertions} / feasibility /
pairs / econ_stats / criteria / verdict / anomaly。数据源=本 lab evidence/ +
头部剖析实抓（2026-09-29 12 局 19 席）。只写一次，确定性。
"""
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
OUT = KSIM_DIR.parents[2] / "fn_docs" / "hybrid" / "results" / "2026-09-29-goose-fullplan.json"

build = json.loads((HERE / "evidence" / "fullplan_build.json").read_text(encoding="utf-8"))
judge_p = HERE / "evidence" / "judge_fullplan.json"
judge = json.loads(judge_p.read_text(encoding="utf-8")) if judge_p.is_file() else {}

rg = build.get("route_gates") or []
feas = {
    "twin_seed": 780010,
    "gates": "现金 min_money≥0 / 劳动 realized(落位+滞留)≥基线 / 棚容 held≤结构格",
    "n_routes": len(rg),
    "n_pass": sum(1 for r in rg if r.get("ok")),
    "n_bad": build.get("n_bad_routes"),
    "rollbacks": build.get("rollbacks"),
    "realized_pairs": [{"route": r["route"], "base": r["realized_base"], "var": r["realized_var"]}
                       for r in rg[:12]],
    "conservation": build.get("audit"),
}

out = {
    "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "version": "goose-fullplan-evidence/1.0",
    "task": "B4c 鹅线全计划供养式重建（剖析→三件协同重生成→判决；不发射/不提交）",
    "dissect": {
        "sources": [
            "fn_docs/hybrid/results/2026-09-29-top-games-analysis.json（88 局头部池实抓）",
            "kaggle competitions replay 官方日包系（12 局 19 席头部回放逐拍剖析，2026-09-29 抓取）",
            "fn_docs/hybrid/results/2026-09-29-goose-line.json（B4b 判死档案=外科件/死因）",
        ],
        "sample": "12 局 19 席（MMPQ 5 / DSM 4 / DECEM 6 / VICTOR 4）",
        "buy_goose_day": "d6 主波 12/19 席、d8-9 次波 7/19、d10-11 收尾；总量 G 6-12 中位 10（支持 n=19）",
        "coop_pattern": "中央簇 x2-6 / y2-7 紧凑块（10×10 格；各队 bbox 均值 x2-6/y2-7）",
        "feed_care_rhythm": "FEED 12.5-14.9/日、CARE 12.4-14.6/日（中位；随 24-26 头畜群比例照护）",
        "egg_harvest_rhythm": "鹅格 HARVEST 5.3-6.1/日，最大间隙 2 日（19/19 席一致）",
        "egg_sell_point": "日产日卖；成交价/日均价 中位 1.00（p25 0.98 / p75 1.00，n=806 单）；qty 8/日",
        "labor_split_vs_wheat": "畜线 18-19% / 作物线 28-31% / 物流 46-47%（总 7.0k-7.7k ops/局）",
        "herd_money": "C7-8/G9-11/S3-8；WHEAT 153-201（涨队 169）/CARROT 28-56（涨队 31.5）；终局钱头部中位 105.7k",
    },
    "top_params": {
        "head_recipe": "GOOSE 9 + WHEAT 169 + CARROT 31.5（涨队）",
        "head_money_end": "105.7k（头部中位）",
        "target_type": "C7/G9-11/S6-8 按头部中位 + 我方 16-17 链劳动预算裁剪 → G10/C4/S2 型",
        "baseline_oc_c3": "C7/S6/G3 族（16-17 链）；WHEAT 163/CARROT 31（≈涨队配方带内）",
    },
    "rebuild": {
        "schedule": build.get("schedule"),
        "labor": {
            "rule": "FEED/CARE 工时不动（保命/照护 lever）；收蛋工时重排=鹅格 COLLECT_FERTILIZER"
                    "→HARVEST 补 ≤2 日缺口（%s 次转换，deficit 日 %s）；劳动闸=落位+滞留≥基线"
                    % (build.get("stats", {}).get("rhythm_converted"),
                       build.get("stats", {}).get("rhythm_deficit_days")),
            "labor_tables_sample": build.get("labor_tables"),
            "conversions": {"chains_to_goose": build.get("stats", {}).get("converted"),
                            "sell_qty_scaled": build.get("stats", {}).get("sell_qty_scaled"),
                            "sell_retargeted": build.get("stats", {}).get("sell_retargeted")},
        },
        "assertions": build.get("assert_regen"),
        "assert_probe": build.get("assert_probe"),
        "diff_scope": build.get("diff_scope"),
    },
    "feasibility": feas,
    "pairs": judge.get("pairs"),
    "econ_stats": judge.get("econ_stats"),
    "criteria": judge.get("criteria"),
    "verdict": judge.get("verdict"),
    "head_compare": judge.get("head_compare"),
    "budget": judge.get("budget"),
    "anomaly": [
        "孪生口径=solo gengame（对手 PASS）：牛奶/羊毛价不饱和，solo 钱变体可低于基线"
        "（twin 均值 %s）；判据以配对实测（真实对手）为准——EGG 过剩支 log 吸收在饱和"
        "市场占优（econ_model 镜像世界+头部鹅漂移实证）"
        % (round(sum((t.get("final_var") or 0) - (t.get("final_base") or 0)
                     for t in build.get("twin_money_sample") or [])
                 / max(1, len(build.get("twin_money_sample") or [])))),
        "tail 共享段 1 组跨路由差异（仅 route 2 尾被复用；HARVEST 物种无关=零风险，信息登记）",
        "EGG T=332 以引擎源码为准（任务提要 T=45 不符，B4b anomaly 同源）",
        "harness 噪声不修不管（任务边界）；终局钱 farms[obs.player] 口径",
    ],
    "build_manifest": build.get("manifest"),
    "pkg_dir": build.get("pkg_dir"),
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
print("wrote", OUT)
