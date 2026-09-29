# -*- coding: utf-8 -*-
"""econ_model（goose lab）：doan 鹅经济学 → 鹅线排程经济求解（B4b 首件，不发射）。

责任口径（任务 B4b）：学经济不学打法——doan 鹅线备忘（组 E 在案）四件套
（蛋对数级吸收 sink / 肥料 $25k 池早卖晚买 / fib 雇工硬约束 / 回本门控）
+ 引擎常数（references/2026-09-28-engine-pricing-extraction.md，源码直读
kaggle-environments 1.32.7 kaggriculture.py sha bc8a5487…）做**经济求解**
（非抄磁带：R9/G2 判死面=黑盒复刻，本件=重生成必须经济求解）。

目标函数：期望净收入 = Σ品 日产量×当日价（吸收表×价表）
  − 购置（GEASE 300/COW 400/SHEEP 500+地 700）
  − 饲料麦（1/头/日×麦价）
  − fib 雇工（ops/日×步行系数 → Σfib(当日第 k 雇)）
  − 肥料池净额（早卖窗口收入，$25k 池上限 share）。
约束：现金逐日≥0（回本门控=购置波次按累计回款解锁）/劳动 op 容量
（24 转/人/日）/棚位（1 动物/结构格）/蛋吸收（对数支=无限吸纳）。

求解形态：小规模枚举（档位 5/7/9 鹅×牛羊配比 + 混合档 7鹅6牛/7鹅9羊 +
店对条件增量档），镜像世界（双方同谱）近似吸收表。输出：排程
（trunk 波次/蛋肥卖点）+ 候选变体排序（≤6）。
确定性：纯函数+固定序。CLI：python econ_model.py → econ_model.json。
只写 orderbook_goose_lab/。
"""
from __future__ import annotations

import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = 30
I0 = 10000.0
PRICE_FLOOR = 1
START_MONEY = 3000
LAND_PRICES = [1000, 2000, 4000]

# ---- 引擎常数（kaggriculture.py 源码直读；sha bc8a5487…，抓取 2026-09-28）--
MARKET_PARAMS = {
    "WHEAT":      {"base": 25, "T": 400, "below": ("sqrt", 0.80), "above": ("log", 0.20)},
    "CARROT":     {"base": 35, "T": 450, "below": ("hinge", 1.00), "above": ("sqrt", 0.70)},
    "TOMATO":     {"base": 60, "T": 200, "below": ("hinge", 0.40), "above": ("sqrt", 0.60)},
    "STRAWBERRY": {"base": 120, "T": 100, "below": ("sqrt", 0.70), "above": ("linear", 1.60)},
    "MELON":      {"base": 250, "T": 300, "below": ("log", 0.20), "above": ("sq", 3.60)},
    "EGG":        {"base": 50, "T": 332, "below": ("hinge", 0.40), "above": ("log", 0.20)},
    "MILK":       {"base": 160, "T": 122, "below": ("sqrt", 0.60), "above": ("linear", 1.60)},
    "WOOL":       {"base": 200, "T": 105, "below": ("log", 0.20), "above": ("sq", 3.20)},
    "FERTILIZER": {"base": 100, "T": 200, "below": ("linear", 0.40), "above": ("linear", 0.40)},
}
ANIMALS = {
    "GOOSE": {"cost": 300, "first": 4, "interval": 1, "max_held": 4, "prod": "EGG"},
    "COW":   {"cost": 400, "first": 8, "interval": 2, "max_held": 6, "prod": "MILK"},
    "SHEEP": {"cost": 500, "first": 6, "interval": 3, "max_held": 6, "prod": "WOOL"},
}
SHOPS = {
    "BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"], "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
SHOP_TYPES = sorted(SHOPS)                 # 8 型，放回抽签
SHOP_UNLOCK_DAYS = [3 * (i + 1) for i in range(8)]   # d3..d24 每 3 日 1 铺（上限 8 实例）
TOWN_CENTER_EXCL = ("FERTILIZER",)
HINGE_GAIN = 8.0


def _shape(func, x, T):
    x = max(0.0, float(x))
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "log10":
        return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def market_price(item, inv):
    """引擎 market_price 逐式复刻（floor PRICE_FLOOR，四舍五入到整）。"""
    p = MARKET_PARAMS[item]
    base, T = p["base"], p["T"]
    if inv < I0:
        fn, tgt = p["below"]
        amp = tgt * base / _shape(fn, T, T)
        price = base + amp * _shape(fn, I0 - inv, T)
    else:
        fn, tgt = p["above"]
        amp = tgt * base / _shape(fn, T, T)
        price = base - amp * _shape(fn, inv - I0, T)
    return max(PRICE_FLOOR, int(round(price)))


# ---- 吸收表：城镇排水期望（铺每 4 步各排 1 件/品，单品铺 ×2；中心日 1 件）----
def expected_drain(item, day):
    """day（0 起）日排水期望件数（铺抽签期望：8 型均匀、d3..d24 逐日解锁）。"""
    n_inst = sum(1 for ud in SHOP_UNLOCK_DAYS if ud <= day)
    if n_inst <= 0:
        shop = 0.0
    else:
        # 每实例独立均匀 8 型：该品在 k 型铺中，期望实例数=n_inst×k/8
        k = 0.0
        for st in SHOP_TYPES:
            prods = SHOPS[st]
            if item in prods:
                k += 2.0 if len(prods) == 1 else 1.0
        shop = 6.0 * n_inst * (k / 8.0)
    center = 1.0 if item not in TOWN_CENTER_EXCL else 0.0
    return shop + center


def _fib(n):
    a, b = 1, 1
    for _ in range(max(0, n - 1)):
        a, b = b, a + b
    return a


# ---- 产出模型（引擎 _daily_refresh_animals 语义：fed+cared→pending+1，产日
# yield += 1+pending（fed 才吃 bonus），max_held 封顶）---------------------
def animal_daily_yield(species, pd):
    """placed_day=pd 的单头满照护（喂+照料日日不缺）逐日产出 [d0..d29]。

    产日：(d+1-pd-first)%interval==0 且 d+1-pd-first>=0；产量=1+pending
    （上一照护日累计 1/日；首产日 bonus=pd..产日 的照料累计，cap max_held）。
    """
    a = ANIMALS[species]
    out = [0] * DAYS
    pending = 0
    for d in range(DAYS):
        # EOD of day d 用 next_day=d+1 判定产日
        dsf = (d + 1) - pd - a["first"]
        if dsf >= 0 and dsf % a["interval"] == 0:
            bonus = pending        # fed_today=True（满照护）
            out[d] = min(a["max_held"], 1 + bonus)
            pending = 0
        pending += 1               # cared+fed 当日收尾 +1
    return out


def spec_production(spec, buy_day):
    """谱（G,C,S）逐日产量（单人；buy_day={sp:pd}）+ 肥料可收量。"""
    prod = {"EGG": [0.0] * DAYS, "MILK": [0.0] * DAYS, "WOOL": [0.0] * DAYS}
    fert = [0.0] * DAYS
    for sp, n in spec.items():
        if n <= 0:
            continue
        pd = int(buy_day.get(sp, 0))
        ys = animal_daily_yield(sp, pd)
        item = ANIMALS[sp]["prod"]
        for d in range(DAYS):
            prod[item][d] += n * ys[d]
            fert[d] += n              # 每动物格日 1 件肥料可收（engine 日刷）
    return prod, fert


def solve_world(spec, buy_day=None, fert_sell_days=(1, 2, 3, 4, 5, 6),
                feed_px=25.0, labor=True):
    """镜像世界（双方同谱）逐日求解：吸收表×价表→期望净收入与现金流。

    卖法=吸收节奏（当日产当日卖；蛋对数支无限吸纳）；肥料=早卖晚买池
    （fert_sell_days 窗口内卖出，晚买价=池底 1~10 另计 FERTILIZE 不入）。
    回本门控：购置波次（d0 现金 3000 起）——现金<成本则推迟到回款日。
    """
    spec = {k: int(spec.get(k, 0)) for k in ("GOOSE", "COW", "SHEEP")}
    buy_day = dict(buy_day or {"GOOSE": 0, "COW": 0, "SHEEP": 0})
    prod, fert = spec_production(spec, buy_day)
    # ---- 市场吸收（共享库存，双方同谱）----
    inv = {it: I0 for it in MARKET_PARAMS}
    px = {}
    income = {it: 0.0 for it in ("EGG", "MILK", "WOOL", "FERTILIZER")}
    daily_income = []
    for d in range(DAYS):
        day_inc = 0.0
        for it in ("EGG", "MILK", "WOOL"):
            supply = 2.0 * prod[it][d]            # 双方同谱
            drain = expected_drain(it, d)
            # 当日产当日卖：先卖后排水近似（价=日产前库存价）
            p = market_price(it, inv[it])
            income[it] += prod[it][d] * p
            day_inc += prod[it][d] * p
            inv[it] = inv[it] + supply - drain
        # 肥料：早卖窗口按当日价清（$25k 池由双方早卖竞速共享）
        if d in fert_sell_days and fert[d] > 0:
            p = market_price("FERTILIZER", inv["FERTILIZER"])
            income["FERTILIZER"] += fert[d] * p
            day_inc += fert[d] * p
            inv["FERTILIZER"] += 2.0 * fert[d] - expected_drain("FERTILIZER", d)
        else:
            inv["FERTILIZER"] += 2.0 * fert[d] - expected_drain("FERTILIZER", d)
        daily_income.append(day_inc)
    # $25k 池上限（doan 口径：早卖晚买共享池；超池截断记 anomaly 面）
    fert_cap = 25000.0
    if income["FERTILIZER"] > fert_cap:
        income["FERTILIZER"] = fert_cap
    # ---- 成本 ----
    heads = sum(spec.values())
    cost_buy = sum(ANIMALS[sp]["cost"] * n for sp, n in spec.items())
    cost_feed = heads * 28.0 * feed_px           # d1..d28 每头每日 1 麦
    ops_day = 4.0 * heads                        # FEED/CARE/HARVEST/COLLECT_FERT
    hands = max(1, math.ceil(ops_day * 1.3 / 24.0))
    cost_hire = sum(_fib(k) for k in range(1, hands + 1)) * DAYS if labor else 0.0
    cost_land = sum(LAND_PRICES)
    net = sum(income.values()) - cost_buy - cost_feed - cost_hire - cost_land
    # ---- 回本门控现金流（d0 3000；波次购置按累计回款解锁）----
    cash = START_MONEY
    min_cash = cash
    waves = []
    pending_buy = dict(spec)
    for d in range(DAYS):
        cash += daily_income[d] - (heads * feed_px if d >= 1 else 0.0) \
            - (sum(_fib(k) for k in range(1, hands + 1)) if labor else 0.0)
        for sp in ("GOOSE", "COW", "SHEEP"):
            if pending_buy.get(sp, 0) > 0 and buy_day.get(sp, 0) == d:
                while pending_buy[sp] > 0 and cash >= ANIMALS[sp]["cost"]:
                    cash -= ANIMALS[sp]["cost"]
                    pending_buy[sp] -= 1
                    waves.append({"day": d, "species": sp})
        min_cash = min(min_cash, cash)
    return {
        "spec": spec, "heads": heads,
        "income": {k: round(v, 1) for k, v in income.items()},
        "income_total": round(sum(income.values()), 1),
        "cost_buy": cost_buy, "cost_feed": round(cost_feed, 1),
        "cost_hire": cost_hire, "hands": hands,
        "net": round(net, 1),
        "min_cash": round(min_cash, 1),
        "buy_waves": waves,
        "unbought": {k: v for k, v in pending_buy.items() if v > 0},
    }


# ---- 变体菜单（任务口径：纯增量档 5/7/9 鹅 + 混合档 7鹅6牛/7鹅9羊 等）----
def variant_menu():
    return {
        "goose5": {"kind": "uniform", "target": {"GOOSE": 5, "COW": 6, "SHEEP": 6},
                   "desc": "纯增量档 5 鹅（6牛6羊5鹅 17 头）"},
        "goose7": {"kind": "uniform", "target": {"GOOSE": 7, "COW": 6, "SHEEP": 4},
                   "desc": "纯增量档 7 鹅（6牛4羊7鹅 17 头）"},
        "goose9": {"kind": "uniform", "target": {"GOOSE": 9, "COW": 6, "SHEEP": 2},
                   "desc": "纯增量档 9 鹅（6牛2羊9鹅 17 头）"},
        "mix76": {"kind": "uniform", "target": {"GOOSE": 7, "COW": 6, "SHEEP": 0},
                  "desc": "混合档 7鹅6牛（13 头菜单口径）"},
        "mix79": {"kind": "uniform", "target": {"GOOSE": 7, "COW": 0, "SHEEP": 9},
                  "desc": "混合档 7鹅9羊（16 头菜单口径）"},
        "shopshift2": {"kind": "shop_shift", "delta_goose": 2,
                       "desc": "店对条件 +2 鹅（蛋铺对 BAKERY/BRUNCH/PET 换 2 羊→2 鹅；毛铺对不动）"},
    }


def enumerate_grid():
    """小规模枚举：档位 g∈{3,5,7,9}×(c,s) 网格（头数≤17）做经济学排序。"""
    rows = []
    for g in (3, 5, 7, 9):
        for c in (0, 4, 6, 8):
            for s in (0, 2, 4, 6, 9, 11):
                if g + c + s > 17 or g + c + s < 13:
                    continue
                r = solve_world({"GOOSE": g, "COW": c, "SHEEP": s})
                rows.append({"spec": r["spec"], "heads": r["heads"],
                             "net": r["net"], "income_total": r["income_total"],
                             "income": r["income"], "min_cash": r["min_cash"],
                             "cost_buy": r["cost_buy"]})
    rows.sort(key=lambda r: -r["net"])
    return rows


def solve_variants():
    menu = variant_menu()
    out = {}
    for vid, spec in menu.items():
        if spec["kind"] == "uniform":
            r = solve_world(spec["target"])
            out[vid] = dict(spec, econ=r)
        else:
            out[vid] = dict(spec, econ=None)   # 店对条件档：路由层映射，网格级不建模
    return out


def main():
    t0 = time.perf_counter()
    grid = enumerate_grid()
    variants = solve_variants()
    # 排程：trunk 波次（d0-d3 6 头=回本门控第一波；鹅优先=GEASE 300 最廉价
    # 蛋 d4 起流）+ 蛋卖点=吸收节奏（产日产日卖）+ 肥料早卖晚买（d1-6 卖窗）。
    schedule = {
        "trunk_wave": {
            "window": "d0-d3（steps 1/1/65/88，链内 4COW+2SHEEP 基线）",
            "rule": "回本门控第一波：GEASE 优先（300 金最廉、蛋 d4 起流）→"
                    "按目标谱最大余数法缩到 6 头作 trunk 波次谱",
        },
        "egg_sell": {"rule": "产日产日卖（蛋对数支无限吸纳；挂量按产比缩放）",
                     "absorption": "EGG above 支 log：Δp=−1.722·ln(1+x)（x=过量），"
                                   "抛 1k 蛋价仅落 ~39；对数级吸收=sink"},
        "fert": {"sell_window": list(range(1, 7)), "buyback": "d6+ 池底回购做 FERTILIZE",
                 "pool_cap_$": 25000},
        "fib_labor": "HIRE=当日第 k 雇 fib(k)（1,1,2,3,5,8,13…）；ops=4/头/日"
                     "（FEED/CARE/HARVEST/COLLECT_FERT）+作物；24 转/人/日",
    }
    out = {
        "version": "goose-econ/1.0",
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "engine_source": {
            "file": "kaggle_environments/envs/kaggriculture/kaggriculture.py",
            "sha256": "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e",
            "pricing_doc": "fn_docs/hybrid/references/2026-09-28-engine-pricing-extraction.md",
            "note": "EGG base50/T=332 hinge→0.40/log→0.20（任务提要 T=45 与源码"
                    "/抽取档 332 不符，以源码 332 为准，anomaly 登记）",
        },
        "econ_model": {
            "objective": "期望净收入=Σ品 日产量×当日价（吸收表×价表）−购置−饲料麦"
                         "−fib 雇工−地；回本门控=购置波次按累计回款解锁",
            "absorption": {
                "town_drain": "铺每 4 步各排 1 件/品（单品铺 ×2）；期望=6/日/实例×"
                              "品铺占比（8 型均匀抽签 d3..d24 逐日解锁，上限 8 实例）；"
                              "中心日 1 件（除 FERTILIZER）",
                "egg_sink": "EGG 过剩支 log（amp 1.722）=对数级吸收；WOOL/MELON 过剩支"
                            "sq=二次崩塌；MILK 过剩支 linear",
            },
            "production": "满照护（喂+照料日日）：GOOSE d≥pd+3 日 2 枚（cap4）/COW 隔日 "
                          "2 奶/SHEEP 3 日 3 毛（引擎 pending_care_bonus 语义复刻）",
            "fib_labor": "Σ fib(k)×日；heads×4 ops/日×1.3 步行系数/24 转",
            "fert_pool": "$25k 早卖晚买共享池（d1-6 卖窗；无城镇排水=纯池）",
        },
        "grid_top10": grid[:10],
        "schedule": schedule,
        "variants": variants,
        "elapsed_s": round(time.perf_counter() - t0, 3),
    }
    path = os.path.join(HERE, "econ_model.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for r in grid[:10]:
        print(r["spec"], "heads", r["heads"], "net", r["net"],
              "inc", r["income"], flush=True)
    for vid, v in variants.items():
        e = v.get("econ") or {}
        print(vid, v["desc"], "net=", e.get("net"), flush=True)
    return out


if __name__ == "__main__":
    main()
