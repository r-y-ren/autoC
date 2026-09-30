# -*- coding: utf-8 -*-
"""econ_solve（d1prod lab）：产线经济学 MILP/枚举求解（D1 头号主攻；不改既有代码）。

缺口（2026-09-29 corner-cases 实测）：实现价 0.787 vs 顶强 0.903 ——
FERT 0.4518（万级倾销 10.6k 件/32 局，d27-29 幻影千件单砸盘）/MILK 0.5669/
WOOL 0.5988 三谷底；终局钱 91k vs 头部 105.7k。奶毛供给管理暗线=我方倾销
给对手压价（撤供反而让对手价差受益，goose-fullplan +11.8k 判死教训）。

求解面（D5 私调蓝图 2026-09-30-d5-private-blueprint.json 取参，A 级=顶强 7 局
全量回放）：
- 肥料处置三谷底关键解：自用 FERTILIZE ~46% / 放量卖出 ~54%（qmed 0.29-0.33
  低中位放量，不囤不等价峰）——引擎核验（kaggriculture.py sha bc8a5487）：
  FERTILIZE 消耗棚存 1 袋、3 日有效（day..day+2）、须同日 WATER 才 +2/日，
  窗口 (max_yield_day+1)//2..max_yield_day，封顶 max_yield；
- 奶毛投放=平台持续 3-4 日一波 20-45u，非脉冲（LP 对照验证）；
- 买畜时序 COW d0-1→SHEEP 两波→GOOSE d6-9 入 COOP；畜群构成留自适应自由度
  （勿写死比例）；蛋/麦经济=吸收曲线×日价（EGG 过剩支 log=sink）。

方法：
1) 双人逐日市场模型（双方共享库存×引擎价式逐式复刻×城镇排水吸收表），
   枚举 (G_add, mw_trim, fert_u) × 对手画像 {oc_c3 现状, 顶强 D5} ——
   目标 ①三谷底品产出-消化-投放平衡 ②蛋/麦经济 ③终局钱→105.7k 带，
   多目标=Pareto（终局钱/边际/实现价）；
2) 投放节奏 MILP（scipy linprog，价曲线分段线性）：脉冲 vs 平台 vs LP 最优
   ——D5 "平台非脉冲" 命题定量对照；
3) 输出 ≤8 变体定义（build_prod.py 消费）。

确定性：纯函数+固定序。CLI：python econ_solve.py。只写 orderbook_d1prod_lab/。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import econ_model as em  # noqa: E402  （引擎价式/吸收表复刻，只读复用）

DAYS = em.DAYS
BASE_PRICES = {k: v["base"] for k, v in em.MARKET_PARAMS.items()}

# ---- 产线事实（oc_c3 磁带 route0-5 剖析 + D5 蓝图）----
TAPE_ARCH = {"GOOSE": 3, "COW": 7, "SHEEP": 6}      # 路由混合中位 ≈16 头
TAPE_FERT_COLLECT_PER_DAY = 17.0                     # d8-26 平台（逐日实测）
TAPE_FERT_SELFUSE_NOW = 61.0 / 367.0                 # route0 现状 0.166
WHEAT_PLANTS = 163
# 肥料自用产率：+1/日×3 日（须同日 WATER）×窗口命中率×(1-封顶率)
THETA_BASE = {"low": 1.0, "mid": 1.5, "high": 2.2}   # 产麦件数/袋（孪生实测校准）
CROP_REALIZED = 41.09                                 # WHEAT 成交均价（corner-cases 实测）
# 作物基线净额（校准常数）：baseline(u=0,g=0) 应复现 oc_c3 实测终局钱 88.9k
# （judge_additive 32 局 farms[obs.player] 均值）——自用肥边际在其上叠加。
CROP_BASE_NET = 58000.0
# 自用肥机会帽：60 作物格×~6 窗口日/3 日效期 ≈ 120 袋/局（D5 顶强 46%≈饱和位）
FERT_OPPORTUNITY_CAP = 120.0

# ---- D5 蓝图产线参数（evidence 节引用）----
D5 = {
    "source": "fn_docs/hybrid/results/2026-09-30-d5-private-blueprint.json（A 级=顶强 7 局全量回放）",
    "fert_disposition": "自用 FERTILIZE ~46% / 卖出 ~54%（qmed 0.29-0.33 低中位放量，不囤不等价峰）",
    "buy_timing": "COW d0-1 抢建→SHEEP 两波（d3-6/d9-15）→GOOSE d6-9 入 COOP；COOP/PASTURE 聚象限 0-1",
    "rhythm": "d6 首剪毛 12-24u→d9+ 持续；d8 奶爬坡→d12-24 平台；d12-14 蛋起；d29 清仓",
    "herd_adaptive": "畜群构成留自适应自由度（顶强 COW 主导 29 / SHEEP 主导 39 大摆，勿写死比例）",
    "mw_release": "奶毛投放=平台持续 3-4 日一波 20-45u，非脉冲",
}


# ============================================================ 双人市场模型 ==
def day_release_stream(spec, buy_day, fert_u, days=DAYS):
    """逐日产出流（EGG/MILK/WOOL=HARVEST 即投；FERT=收集量×(1-u) 放量）。

    自用肥带机会帽（FERT_OPPORTUNITY_CAP：窗口×格数/效期；超帽部分回落放量）。
    """
    prod, fert = em.spec_production(spec, buy_day)
    out = {"EGG": [0.0] * days, "MILK": [0.0] * days, "WOOL": [0.0] * days,
           "FERTILIZER": [0.0] * days, "fert_selfused": [0.0] * days}
    for it in ("EGG", "MILK", "WOOL"):
        out[it] = [float(prod[it][d]) for d in range(days)]
    budget = float(fert_u) * sum(fert)          # 目标自用袋数
    budget = min(budget, FERT_OPPORTUNITY_CAP)  # 机会帽
    for d in range(days):
        use = min(fert[d] * float(fert_u), budget)
        budget -= use
        out["fert_selfused"][d] = use
        out["FERTILIZER"][d] = fert[d] - use
    return out


def simulate_world(us, them, theta="mid", days=DAYS):
    """双人共享库存逐日求解：双方同价成交（逐式复刻引擎价）→ 各自收入/边际。

    us/them = {"spec":{G,C,S}, "buy_day":{sp:d}, "fert_u":u}
    返回：双方收入/成本/终局钱、实现价、逐品价径、库存轨迹。
    """
    th = THETA_BASE[theta] if isinstance(theta, str) else float(theta)
    streams = {"us": day_release_stream(us["spec"], us.get("buy_day"), us["fert_u"], days),
               "them": day_release_stream(them["spec"], them.get("buy_day"), them["fert_u"], days)}
    inv = {it: em.I0 for it in em.MARKET_PARAMS}
    rev = {"us": 0.0, "them": 0.0}
    rev_item = {"us": {}, "them": {}}
    qty_item = {"us": {}, "them": {}}
    daily = {"us": [], "them": []}
    px_path = {it: [] for it in ("EGG", "MILK", "WOOL", "FERTILIZER")}
    fert_income = {"us": 0.0, "them": 0.0}
    crop_income = {"us": 0.0, "them": 0.0}
    for d in range(days):
        for p in ("us", "them"):
            daily[p].append(0.0)
        for it in ("EGG", "MILK", "WOOL", "FERTILIZER"):
            r_us = streams["us"][it][d]
            r_th = streams["them"][it][d]
            # 自冲击定价：放量按盘口前值→放量后均值（库存+r/2 二阶近似；
            # 大放量不吃幻影"放量前整单价"——万级倾销现实校正）
            run = 0.0
            for p, r in (("us", r_us), ("them", r_th)):
                if r > 0:
                    p_avg = em.market_price(it, inv[it] + run + r / 2.0)
                    rev[p] += r * p_avg
                    rev_item[p][it] = rev_item[p].get(it, 0.0) + r * p_avg
                    qty_item[p][it] = qty_item[p].get(it, 0.0) + r
                    daily[p][d] += r * p_avg
                    if it == "FERTILIZER":
                        fert_income[p] += r * p_avg
                    run += r
            px_path[it].append(em.market_price(it, inv[it]))
            drain = em.expected_drain(it, d)
            inv[it] = inv[it] + r_us + r_th - drain
        # 自用肥→作物边际（+θ 产件×作物实现价；按自用袋数计）
        for p in ("us", "them"):
            bags = streams[p]["fert_selfused"][d]
            if bags > 0:
                gain = bags * th * CROP_REALIZED
                crop_income[p] += gain
                daily[p][d] += gain
    # 成本（两侧同构；购置按谱、饲料麦=头×28×麦价（模型麦价=吸收表近似）、fib 雇工、地）
    def cost_of(plan):
        spec = plan["spec"]
        heads = sum(spec.values())
        c_buy = sum(em.ANIMALS[sp]["cost"] * n for sp, n in spec.items())
        wheat_px = em.market_price("WHEAT", em.I0 + 0.5 * WHEAT_PLANTS)
        c_feed = heads * 28.0 * wheat_px
        import math
        ops_day = 4.0 * heads
        hands = max(1, math.ceil(ops_day * 1.3 / 24.0))
        c_hire = sum(em._fib(k) for k in range(1, hands + 1)) * days
        return c_buy + c_feed + c_hire + sum(em.LAND_PRICES)
    out = {"theta": th, "px_path": px_path}
    for p, plan in (("us", us), ("them", them)):
        c = cost_of(plan)
        net = rev[p] + crop_income[p] + CROP_BASE_NET - c
        realized_num = sum(rev_item[p].values())
        realized_den = sum(qty_item[p].get(it, 0.0) * BASE_PRICES[it] for it in qty_item[p])
        # 作物线混入实现价（corner-cases 实测作物实现比 1.55；谷底三品为畜/肥线）
        crop_val = crop_income[p] + CROP_BASE_NET
        realized_num += crop_val
        realized_den += crop_val / 1.55
        out[p] = {
            "spec": plan["spec"], "fert_u": plan["fert_u"],
            "income_sell": round(rev[p], 1),
            "income_crop_from_fert": round(crop_income[p], 1),
            "income_total": round(rev[p] + crop_income[p] + CROP_BASE_NET, 1),
            "cost": round(c, 1), "net": round(net, 1),
            "realized_px": round(realized_num / realized_den, 4) if realized_den else None,
            "per_item": {it: {"qty": round(qty_item[p][it], 1),
                              "rev": round(rev_item[p][it], 1),
                              "avg_px": round(rev_item[p][it] / max(1e-9, qty_item[p][it]), 1)}
                         for it in sorted(qty_item[p])},
            "fert_income": round(fert_income[p], 1),
        }
    out["margin"] = round(out["us"]["net"] - out["them"]["net"], 1)
    return out


# ============================================================ 投放节奏 MILP ==
def release_lp(item, prod, days=DAYS, mode="lp"):
    """给定产出流+分段线性价曲线：投放节奏求解（pulse/plateau/lp 对照）。

    LP：max Σ r_d·p_d，s.t. 0≤r_d≤stock_d，Σr_d=Σprod（期末清仓）；
    p_d 为库存路径线性化的分段线性（网格 6 断点，逐段 slope=引擎支形导数）。
    """
    import numpy as np
    from scipy.optimize import linprog
    stock = 0.0
    caps = []
    for d in range(days):
        stock += prod[d]
        caps.append(stock)
    caps = np.array(caps, dtype=float)
    total = float(sum(prod))
    if mode == "pulse":
        r = [0.0] * days
        r[days - 1] = total
        r = np.array(r)
    elif mode == "plateau":
        r = np.full(days, total / days)
    else:
        # 分段线性价格近似 + 棚容硬约束（F6：棚+随身≤100，溢出销毁→"不囤"是容量强制）
        inv0 = em.I0
        grid_inv = [max(0.0, inv0 + k * 400.0) for k in range(6)]
        grid_px = [em.market_price(item, g) for g in grid_inv]
        p_hi, p_lo = grid_px[0], grid_px[-1]
        k = (p_hi - p_lo) / max(1.0, grid_inv[-1] - grid_inv[0])
        c = np.array([-(p_hi - k * (caps[d] / 2.0)) for d in range(days)])
        A_ub, b_ub = [], []
        for d in range(days):                     # 累计投放 ≤ 累计产出（不超卖）
            row = [0.0] * days
            for j in range(d + 1):
                row[j] = 1.0
            A_ub.append(row)
            b_ub.append(caps[d])
        cum = 0.0
        for d in range(days):                     # 棚容：累计未投 ≤ 100
            cum += prod[d]
            row = [0.0] * days
            for j in range(d + 1):
                row[j] = -1.0
            A_ub.append(row)
            b_ub.append(-(cum - 100.0))
        A_eq = [[1.0] * days]
        b_eq = [total]
        res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                      A_eq=np.array(A_eq), b_eq=np.array(b_eq),
                      bounds=[(0.0, None)] * days, method="highs")
        r = res.x if res.success else np.full(days, total / days)
    # 评估：真实逐式价 + 自冲击（放量按库存+r/2 均价）
    inv = em.I0
    rev = 0.0
    pxs = []
    for d in range(days):
        pxs.append(em.market_price(item, inv))
        rd = float(r[d])
        if rd > 0:
            rev += rd * em.market_price(item, inv + rd / 2.0)
        inv = inv + rd - em.expected_drain(item, d)
    held = 0.0
    shed_ok = True
    for d in range(days):
        held += prod[d] - float(r[d])
        if held > 100.5:
            shed_ok = False
    return {"mode": mode, "revenue": round(rev, 1),
            "release": [round(float(x), 2) for x in r],
            "px_path": pxs, "total_qty": round(total, 1),
            "shed_feasible": bool(shed_ok)}


# ============================================================ 枚举主求解 ==
def enumerate_solve():
    """(G_add, mw_trim, fert_u) 网格 × 对手画像 → 多目标 Pareto。"""
    buy_day = {"GOOSE": 6, "COW": 0, "SHEEP": 3}   # D5：COW 抢建/SHEEP 早波/GOOSE d6-9
    opp_profiles = {
        "oc_c3_now": {"spec": {"GOOSE": 3, "COW": 7, "SHEEP": 6},
                      "buy_day": {"GOOSE": 10, "COW": 6, "SHEEP": 8}, "fert_u": 0.0},
        "top_d5": {"spec": {"GOOSE": 10, "COW": 7, "SHEEP": 6},
                   "buy_day": {"GOOSE": 6, "COW": 0, "SHEEP": 3}, "fert_u": 0.46},
    }
    rows = []
    for g_add in (0, 2, 4, 6, 8, 10):
        for trim in (0, 1, 2):
            if g_add + trim > 10:
                continue
            for u in (0.0, 0.23, 0.46, 0.60):
                spec = {"GOOSE": TAPE_ARCH["GOOSE"] + g_add,
                        "COW": TAPE_ARCH["COW"],
                        "SHEEP": TAPE_ARCH["SHEEP"] - trim}
                us = {"spec": spec, "buy_day": buy_day, "fert_u": u}
                res = {}
                for on, op in opp_profiles.items():
                    res[on] = simulate_world(us, op, theta="mid")
                row = {
                    "spec": spec, "g_add": g_add, "mw_trim": trim, "fert_u": u,
                    "vs_oc_c3": {"net_us": res["oc_c3_now"]["us"]["net"],
                                 "margin": res["oc_c3_now"]["margin"],
                                 "realized_px": res["oc_c3_now"]["us"]["realized_px"]},
                    "vs_top_d5": {"net_us": res["top_d5"]["us"]["net"],
                                  "margin": res["top_d5"]["margin"],
                                  "realized_px": res["top_d5"]["us"]["realized_px"]},
                }
                row["score_own"] = row["vs_oc_c3"]["net_us"]
                row["score_margin"] = min(row["vs_oc_c3"]["margin"], row["vs_top_d5"]["margin"])
                row["score_px"] = min(row["vs_oc_c3"]["realized_px"] or 0,
                                      row["vs_top_d5"]["realized_px"] or 0)
                rows.append(row)
    rows.sort(key=lambda r: -(0.5 * r["score_own"] + 0.3 * r["score_margin"] * 0.01
                              + 20000.0 * r["score_px"]))
    return rows


def pareto(rows, keys=("score_own", "score_margin", "score_px")):
    front = []
    for r in rows:
        dom = False
        for q in rows:
            if q is r:
                continue
            if all(q[k] >= r[k] for k in keys) and any(q[k] > r[k] for k in keys):
                dom = True
                break
        if not dom:
            front.append(r)
    return front


# ============================================================ 变体定义 ==
def variant_menu(rows):
    """≤8 变体（build_prod 消费）：四家族=奶毛减投/蛋麦配比/肥料循环利用/26 头加法系。"""
    def find(g, t, u):
        for r in rows:
            if r["g_add"] == g and r["mw_trim"] == t and abs(r["fert_u"] - u) < 1e-9:
                return r
        return None
    menu = [
        ("fert46", 0, 0, 0.46, "肥料循环利用：自用 FERTILIZE 46%/放量 54%（D5 配比解）"),
        ("fert23", 0, 0, 0.23, "肥料循环利用半档：23% 自用（敏感性下界）"),
        ("fert60", 0, 0, 0.60, "肥料循环利用加档：60% 自用（敏感性上界）"),
        ("mwtrim1", 0, 1, 0.0, "奶毛减投：1 条晚波 SHEEP 链→GOOSE（WOOOL 投放-1，蛋吸收补）"),
        ("mwtrim2", 0, 2, 0.0, "奶毛减投 2 档：2 链换（谷底加深对冲）"),
        ("gadd6", 6, 0, 0.0, "蛋麦配比：+6 GOOSE（麦田 163 供养带内），D5 波次 d6-9"),
        ("gadd10", 10, 0, 0.0, "26 头加法系：+10 GOOSE（16→26 头），D5 波次 d6-9 入 COOP"),
        ("fert46_gadd6", 6, 0, 0.46, "组合：D5 肥配比 +6 GOOSE（蛋麦+肥料双解）"),
    ]
    out = {}
    for vid, g, t, u, desc in menu:
        r = find(g, t, u)
        out[vid] = {"id": vid, "desc": desc, "g_add": g, "mw_trim": t, "fert_u": u,
                    "econ": ({"vs_oc_c3": r["vs_oc_c3"], "vs_top_d5": r["vs_top_d5"]}
                             if r else None),
                    "family": ("fert" if g == 0 and t == 0 else
                               "mw_trim" if t > 0 else
                               "additive26" if g >= 10 else "egg_wheat")}
    return out


def main():
    t0 = time.perf_counter()
    rows = enumerate_solve()
    front = pareto(rows)
    # 投放节奏 MILP 对照（D5 命题：平台非脉冲）
    buy_day = {"GOOSE": 6, "COW": 0, "SHEEP": 3}
    prod_milk = day_release_stream({"GOOSE": 3, "COW": 7, "SHEEP": 6}, buy_day, 0.0)["MILK"]
    prod_wool = day_release_stream({"GOOSE": 3, "COW": 7, "SHEEP": 6}, buy_day, 0.0)["WOOL"]
    lp = {
        "MILK": {m: release_lp("MILK", prod_milk, mode=m) for m in ("pulse", "plateau", "lp")},
        "WOOL": {m: release_lp("WOOL", prod_wool, mode=m) for m in ("pulse", "plateau", "lp")},
    }
    lp_cmp = {it: {m: lp[it][m]["revenue"] for m in lp[it]} for it in lp}
    variants = variant_menu(rows)
    out = {
        "version": "d1-econ-solve/1.0",
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gap_baseline": {
            "realized_px_us": 0.7869, "realized_px_top": 0.903,
            "troughs": {"FERTILIZER": 0.4518, "MILK": 0.5669, "WOOL": 0.5988},
            "fert_dump_qty_per_32games": 10616, "terminal_money_us": 91000,
            "terminal_money_top": 105700,
            "src": "fn_docs/hybrid/results/2026-09-29-corner-cases.json realized_base"},
        "d5_params": D5,
        "engine_facts": {
            "fertilize": "消耗棚存 1 袋；fertilized_until_day=day+2（3 日有效）；须同日 "
                         "WATER 才 +2/日（否则 +1）；窗口 (max_yield_day+1)//2..max_yield_day；"
                         "封顶 max_yield（kaggriculture.py:430-481/795-800）",
            "collect": "每动物格日 1 袋（不累积）；COLLECT_FERTILIZER→棚存",
            "egg_sink": "EGG 过剩支 log（amp 1.722）=对数级吸收；WOOL 过剩支 sq=二次崩塌；"
                        "MILK 过剩支 linear 1.60",
            "fert_pool": "FERT 城镇排水=0（TOWN_CENTER 排除/无铺消化）——只进不出=线性砸盘",
        },
        "method": {
            "grid": "G_add∈{0,2,4,6,8,10}×mw_trim∈{0,1,2}×fert_u∈{0,0.23,0.46,0.60}",
            "world": "双人共享库存逐日（引擎价式逐式复刻+城镇吸收表）×对手画像 "
                     "{oc_c3 现状 u=0/顶强 D5 u=0.46}",
            "multi_objective": "Pareto（终局钱/双画像边际/实现价）；胜率=硬通货留判决层",
            "milp": "scipy.optimize.linprog 投放节奏（价曲线分段线性 6 断点）",
        },
        "econ_top10": rows[:10],
        "pareto_front": [{"spec": r["spec"], "fert_u": r["fert_u"],
                          "g_add": r["g_add"], "mw_trim": r["mw_trim"],
                          "vs_oc_c3": r["vs_oc_c3"], "vs_top_d5": r["vs_top_d5"]}
                         for r in front[:12]],
        "release_lp_compare": lp_cmp,
        "release_lp_detail": {it: {m: {k: v for k, v in lp[it][m].items() if k != "release"}
                                   for m in lp[it]} for it in lp},
        "variants": variants,
        "anomaly": [
            "θ（自用肥产率/袋）=1.5 中值（引擎 +1/日×3 日×窗口命中×(1-封顶)）；"
            "低 1.0/高 2.2 敏感性在 solve_world(theta=) 可复算——孪生实测（build 阶段）校准",
            "双人模型为日粒度近似（同日双方同价成交）；日内次序/幻影单墙不建模——"
            "配对实测（新标准面板）为最终裁决",
            "饲料麦价=吸收表近似常数；奶毛投放节奏 MILP 为单人对照（对手固定放量）",
        ],
        "elapsed_s": round(time.perf_counter() - t0, 3),
    }
    path = HERE / "evidence" / "econ_solve.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
                    encoding="utf-8")
    print("top:", json.dumps(rows[0]["spec"]), "u=", rows[0]["fert_u"],
          "own=", rows[0]["score_own"], "margin=", rows[0]["score_margin"],
          "px=", rows[0]["score_px"], flush=True)
    print("lp:", json.dumps(lp_cmp), flush=True)
    for vid, v in variants.items():
        print(vid, v["family"], v["econ"] and v["econ"]["vs_oc_c3"], flush=True)
    return out


if __name__ == "__main__":
    main()
