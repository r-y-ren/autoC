# -*- coding: utf-8 -*-
"""assemble_topform：顶端策略升级证据汇总（只读各 evidence/*.json + 内嵌蓝图
规则表），落 fn_docs/hybrid/results/2026-09-29-topform-upgrade.json。

schema：blueprint{rules,support}/builds/diff_audit/gates/pairs/behavior/
criteria/verdict/anomaly。
"""
from __future__ import annotations

import json
import os
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(KSIM)))  # .../kaggriculture
OUT = os.path.join(WORKSPACE, "fn_docs", "hybrid", "results",
                   "2026-09-29-topform-upgrade.json")
EVID = os.path.join(ROOT, "evidence")

# /tmp/topform 挖掘产物（临时区；关键数字已内嵌，文件仅供复核）
MINE = "/tmp/topform/sell_mining.json"
MINE2 = "/tmp/topform/sell_mining2.json"


def _load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


BLUEPRINT_RULES = [
    {
        "id": "B1",
        "name": "排水拍相位（drain-front quoting）",
        "condition": "非洗涤品 SELL 落在 t%4==0（town-shop 排水拍前谷底）",
        "action": "整单后置 +1 拍（t+1=%4==1 排水后峰值）；due 记账抵扣；"
                  "WHEAT/FERTILIZER（对倒腿）不动；整单不拆",
        "support": {
            "champion_24wins_orders": 9284,
            "champion_mod4_frac": {"0": 0.1486, "1": 0.2000, "2": 0.3742,
                                   "3": 0.2771},
            "champion_frac_mod4_2_3": 0.6513,
            "champion_frac_hour23": 0.1019,
            "champion_frac_hour0": 0.0343,
            "overlay_461wins_mod4_2_3_by_item": {
                "MILK": 0.830, "WOOL": 0.743, "STRAWBERRY": 0.734,
                "EGG": 0.679, "CARROT": 0.638, "WHEAT": 0.603,
                "TOMATO": 0.560, "MELON": 0.426, "FERTILIZER": 0.455},
            "overlay_461wins_hour23_by_item": {
                "EGG": 0.424, "CARROT": 0.363, "TOMATO": 0.358,
                "WHEAT": 0.149, "MILK": 0.059, "WOOL": 0.042},
            "h1_baseline_mod4_frac": {"0": 0.258, "1": 0.353, "2": 0.190,
                                      "3": 0.199},
            "h1_baseline_frac_hour0": 0.128,
            "h1_baseline_frac_hour23": 0.038,
            "price_phase_norm_by_mod4": {
                "note": "日均归一；%4==1=shop 排水后峰值，%4==0=排水前谷底",
                "WOOL": {"0": 0.9642, "1": 1.1064, "2": 0.9711, "3": 0.9583},
                "MILK": {"0": 0.9767, "1": 1.0651, "2": 0.9846, "3": 0.9736},
                "STRAWBERRY": {"0": 0.9869, "1": 1.0354, "2": 0.9923, "3": 0.9854},
                "CARROT": {"0": 0.9987, "1": 1.0013, "2": 1.0005, "3": 0.9995}},
            "engine_mechanics": (
                "kaggriculture.py _town_consume: step%4==0 shop 排水（单品类 "
                "x2/实例）、step%24==0 town-center 排水（各 -1）；_commit_unit: "
                "SELL 同拍即时按边际价成交（报价拍价格=成交价）"),
        },
        "implemented": True,
        "implementation": "step1009 构造点 _tf_post：t%4==0 整单后置 +1；"
                          "due[t+1] 记账；视界 H=1；quote 门=原生 suppress/"
                          "r36_debt 碰撞跳过 + 同拍 PICKUP 守卫 + 槽位守卫",
    },
    {
        "id": "B2", "name": "价格分位（price band）",
        "condition": "卖出时点相对当日价格分位",
        "action": "不设高分位门；连续变现（分位中带出货）",
        "support": {"sell_px_quantile_median": 0.4792,
                    "sell_px_quantile_mean": 0.4554,
                    "frac_q_ge_0.5": 0.4722, "frac_q_ge_0.75": 0.1595,
                    "day_new_high_frac": 0.2112,
                    "realized_vs_dayavg_qty_w": 0.985,
                    "realized_vs_base_qty_w": 0.9028},
        "implemented": False,
        "implementation": "已覆盖：内层 _r36_reserve 视界内贪婪前置（价格下限 "
                          "≥2）+ _sell_lead/min_sell_price 门；无需新增",
    },
    {
        "id": "B3", "name": "清仓式卖出（whole-lot liquidation）",
        "condition": "决定卖某品时",
        "action": "整单清仓（不碎单滴灌）",
        "support": {"qty_over_held_median": 1.0,
                    "frac_orders_ge_0999_held": 0.5173},
        "implemented": False,
        "implementation": "已覆盖：_r36_reserve 整单前置 + X1 同拍碎单合并/"
                          "幻影清理 + _clamp_sells",
    },
    {
        "id": "B4", "name": "单均量与散布（lot size & spread）",
        "condition": "常态卖单",
        "action": "小单散布（median 2 / p90 9；连续卖 burst≥3 仅 8.5%）",
        "support": {"champion_qty_mean": 4.0, "champion_qty_median": 2,
                    "champion_qty_p90": 9, "burst_ge3_frac": 0.0846,
                    "h1_qty_mean": 5.99, "h1_qty_median": 4,
                    "h1_qty_p90": 13},
        "implemented": False,
        "implementation": "不实现：拆单摊薄=跨拍拆并，撞守恒红线（零跨拍拆并）；"
                          "如实登记差异",
    },
    {
        "id": "B5", "name": "对手流前置（rival-flow pre-emption）",
        "condition": "对手同品卖流临近",
        "action": "在对手流前出货",
        "support": {"opp_same_item_sell_within_3t_after_ours": 0.319,
                    "opp_same_item_sell_within_3t_before_ours": 0.251,
                    "n_orders": 9284},
        "implemented": False,
        "implementation": "已覆盖：V9 RACE 竞速升级（horizon 8→24）+ _front_run "
                          "+ _r36_reserve 视界 40-48 前置 + _race_lost 判据",
    },
    {
        "id": "B6", "name": "变现阶梯（monetization ladder）",
        "condition": "各品首个卖单拍",
        "action": "按生产节奏分品启动变现（羊 d6 羊毛变现后弃）",
        "support": {"first_sell_step_medians": {
            "WHEAT": 2, "FERTILIZER": 27, "WOOL": 149, "MILK": 195,
            "MELON": 251, "EGG": 311, "STRAWBERRY": 330, "TOMATO": 476,
            "CARROT": 509.5}, "n_games": 24},
        "implemented": False,
        "implementation": "已覆盖：路线 tape 生产节奏自带（route 系列）",
    },
    {
        "id": "B7", "name": "末日清仓（day-29 clearance）",
        "condition": "day 29",
        "action": "折价清仓（realized/base 0.852 vs 常态 0.91-0.96）",
        "support": {"day29_ratio": 0.8522, "normal_ratio": 0.9615,
                    "n_orders": 9284},
        "implemented": False,
        "implementation": "已覆盖：_terminal_liquidation（>=718 全仓清）",
    },
]


def main():
    mine = _load(MINE, {})
    mine2 = _load(MINE2, {})
    build = _load(os.path.join(EVID, "build_manifest.json"), {})
    diff_audit = _load(os.path.join(EVID, "diff_audit.json"), {})
    gates = _load(os.path.join(EVID, "gates.json"), {})
    judgment = _load(os.path.join(EVID, "judgment.json"), {})
    pairs = {}
    for name in ("h2_vs_h1", "h2_vs_r40"):
        p = _load(os.path.join(EVID, "pair_%s.json" % name))
        if p:
            pairs[name] = p

    h2_form = (build.get("forms") or {}).get("h2") or {}
    gates_lite = {
        "overall_passed": gates.get("overall_passed"),
        "forms": {f: {k: v.get("passed") for k, v in (gates.get("forms") or {}).get(f, {}).items()
                      if isinstance(v, dict) and "passed" in v}
                  for f in ("h2", "h1")},
        "footprint_probe": gates.get("footprint_probe"),
        "stream_readings": gates.get("stream_readings"),
        "budget": gates.get("budget"),
    }
    pairs_lite = {}
    for name, p in pairs.items():
        pairs_lite[name] = {
            k: p.get(k) for k in
            ("n_games", "wins", "losses", "ties", "h2h", "mean_margin",
             "margin_per_game", "ours", "opp_side", "wall", "phase",
             "n_error_games", "replay_r30_26", "neutral_672000_i53")
        }
        pairs_lite[name]["rows_lite"] = p.get("rows_lite")

    # ---- 判据逐条 ----
    main_pair = pairs.get("h2_vs_h1") or {}
    ref_pair = pairs.get("h2_vs_r40") or {}
    h2h = main_pair.get("h2h")
    realized_h2 = ((main_pair.get("ours") or {}).get("realized_px_median"))
    realized_h1 = ((main_pair.get("opp_side") or {}).get("realized_px_median"))
    zero_fp = bool((gates.get("footprint_probe") or {}).get("passed"))
    wins_flip = (main_pair.get("replay_r30_26") or {}).get("wins")
    wins_flip_ref = (main_pair.get("replay_r30_26") or {}).get("losses")
    criteria = [
        {"criterion": "h2h vs H1 >= 0.55（双席折叠 n=50）",
         "value": h2h,
         "passed": (isinstance(h2h, (int, float)) and h2h >= 0.55)},
        {"criterion": "实现价非负（H2 中位实现价 - H1 >= 0）",
         "value": {"h2": realized_h2, "h1": realized_h1},
         "passed": (isinstance(realized_h2, (int, float))
                    and isinstance(realized_h1, (int, float))
                    and realized_h2 - realized_h1 >= 0)},
        {"criterion": "零足迹（函数级硬门：非触发拍同对象 + 净卖量恒等 + "
                      "零跨拍拆并）",
         "value": (gates.get("footprint_probe") or {}).get("n_moves"),
         "passed": zero_fp},
        {"criterion": "胜局对照不翻负（26 败局组内 H2 wins>losses）",
         "value": {"wins": wins_flip, "losses": wins_flip_ref},
         "passed": (isinstance(wins_flip, (int, float))
                    and isinstance(wins_flip_ref, (int, float))
                    and wins_flip > wins_flip_ref)},
    ]
    verdict = "PASS" if all(c["passed"] for c in criteria) else "FAIL"

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "topform-upgrade/1.0",
        "experiment": ("顶端策略升级：榜一（Majkel1337）卖时蓝图提取 → 内生织入 "
                       "H1 内层（step1009 构造点）→ 门禁+判决；不发射不提交"),
        "source": {
            "blueprint_data": [
                "kaggle:leoprovorov/a-song-of-ice-and-fire-interactive-dashboards"
                "（461 胜局逐命令叠加 + 11 队分歧 + 64 店世界）",
                "kaggle:ashok205/top10-replay-dataset-archive（403 不可得，弃）",
                "kaggle replay API: Majkel1337 胜局全量回放 24 局抽样"
                "（/tmp/topform/majkel_replays，743MB 实抓）",
                "本地语料 fn_docs/hybrid/results/replays-r30-26（26 局 strip）",
                "官方引擎 kaggle-environments kaggriculture（成交/排水机制）"],
            "mining_outputs": {
                "sell_mining": MINE, "sell_mining2": MINE2},
            "judgment_commands": (judgment.get("source") or {}).get("commands"),
            "sim_auth": (judgment.get("source") or {}).get("sim_auth"),
        },
        "blueprint": {
            "rules": BLUEPRINT_RULES,
            "support": {
                "overlay_461wins_sell_cmd_instances": 180258,
                "replay_sample": {"n_games": (mine.get("replays") or {}).get("n"),
                                  "n_sells": (mine.get("replays") or {}).get("n_sells")},
                "per_match": (mine.get("overlay") or {}).get("per_match"),
                "land_relation": (mine.get("overlay") or {}).get("land_relation"),
                "counterfactual_phase_shift_qty_weighted": {
                    "note": "冠军实卖拍 t 平移到 t+shift 的同日价格比（qty 加权）"
                            "；自冲击污染（其自身卖单压价），仅作方向参考",
                    "-2": 1.0538, "-1": 1.0591, "+1": 0.9888, "+2": 0.9821,
                    "+3": 0.9852, "+4": 0.9750},
            },
        },
        "builds": build,
        "diff_audit": {k: diff_audit.get(k) for k in
                       ("anchor_function", "anchor_role", "h1_changed_line_band",
                        "prefix_identical", "suffix_identical", "checks",
                        "diff_lines")},
        "gates": gates_lite,
        "pairs": pairs_lite,
        "behavior": {
            "champion_target": {
                "frac_mod4_0": 0.1486, "frac_mod4_2_3": 0.6513,
                "frac_hour0": 0.0343, "frac_hour23": 0.1019,
                "qty_mean": 4.0, "liquidation_frac": 0.5173,
                "realized_vs_dayavg": 0.985},
            "h1_vs_h2": {k: (v.get("phase") or {}) for k, v in pairs_lite.items()},
            "realized_px": {k: (v.get("ours") or {}) for k, v in pairs_lite.items()},
        },
        "criteria": criteria,
        "verdict": verdict,
        "anomaly": {
            "judgment_abort": judgment.get("aborted"),
            "layer_stats_real_game_diag": {
                "note": "diag_h2 包装件实跑 1825501814（H2 镜像局）读取内生台账",
                "moves_per_game": 29, "moved_qty_per_game": 151,
                "changed_turns": 44, "skip_native": 2, "skip_stock": 7,
                "due_redeferred": 5, "residual_due": 0, "errors": 0},
            "post_hoc_diagnosis": [
                "①相位差是探针伪影：H1 在真实对局（vs H1/r40）中 frac_mod4_0 "
                "=0.1482/0.1485，已与冠军 0.1486 同水平；vs 被动 passer 探针的 "
                "0.258 不代表实战分布——B1 的前提差距在判决口径下不存在。",
                "②后置损害报价槽位：due 加回单落在目标拍单列表尾部，破坏链内 "
                "_s793_reorder/_v224_sales_first 的报价优先序；同拍既有卖单先吃"
                "库存，后置单常卖不全/吃边际低价。",
                "③方向反了：冠军实卖拍反事实 px(t-1)/px(t)=1.059（qty 加权）说明"
                "可转移方向是【提前】而非延后；提前方向已由内层 _sell_lead（1 拍"
                "提前+suppress）与 _r36_reserve（视界 40-48 贪婪前置+r36_debts "
                "抵扣）覆盖——'已覆盖'如实登记。",
                "④冠军 %4∈{2,3} 集中是生产节奏（PICKUP/入仓时点）驱动的可用性"
                "现象，不是可移植的价差时点；其 31.9% vs 25.1% 对手流前置同理"
                "已被 V9 RACE/_front_run 覆盖。"],
            "lesson_theorem_extension": (
                "教训定理第 5 同型：外挂挪量必负（R28/I2/K1）；内生+due 守恒+零"
                "足迹是必要条件而非充分条件——规则的经济方向必须先经反事实/小"
                "样本验证，卖时挪量（延后方向）内生式亦负（本实验 0-50-0 双对）。"),
        },
        "budget": judgment.get("budget"),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    print("wrote", OUT, "verdict", verdict, flush=True)
    print("criteria:", json.dumps(criteria, ensure_ascii=False, default=str),
          flush=True)


if __name__ == "__main__":
    main()
