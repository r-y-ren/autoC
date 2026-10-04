# -*- coding: utf-8 -*-
"""phase_m —— R15 Phase M 市场地图法证（纯解析，重演零开销）。

复用（只调用）：R14 orderbook_surge_lab.phase_a.daily_netflow_decompose
——86 局逐日双席品项价/量/净收入/可卖库存重算（R15 不重写解析）。

两面分位口径（method_note 登记偏差与理由）：
  - own_pool 面（字面口径）：品项各 (局,日) 均价在自池（该品全语料全日
    均价集合）中的分位轨迹——刻画品项自身季内趋势；
  - structural 面（判据面）：各 (局,日) 品项 Markup=价/引擎基准价 在
    PLANTABLE 截面中的分位——"结构性高/低价"。字面 own-pool 面在平稳
    系列上均值数学上回归 ~50，35/65 阈值不可达（实测 86 局无品项过阈，
    会造成假性 KILLED）；结构性判据按 Markup 截面分位落地（基准价取
    twin 引擎 MARKET_PARAMS.base，运行时校验），供 rank_swap_pairs 消费。
  - 崩价品（structural_low）：Markup 截面分位均值 ≤ low_pct(35) 且
    家族供给密度高（家族成交量份额 ≥ supply_hi(0.20) 或 plantable 内
    top-2）——"长期低分位+全家族供给密度高"；
  - 稀缺品（structural_high）：Markup 截面分位均值 ≥ high_pct(65)。

供给密度：家族（双席）逐日成交量份额 vol(item)/vol(all) 的语料均值
（供给流入市场口径）；产能窗：我席 sellable(from) 逐日中位数>0 的日集
∩ to 品停时窗（day ≤ 29 − FIRST_YIELD_DAY[to]，首收获须落在 day 29 内）。
"""
from __future__ import annotations

from . import _base as B
from orderbook_surge_lab import corpus as _surge_corpus
from orderbook_surge_lab import phase_a as _surge_a

WINDOW_START_DAY = 8      # "长期"窗口起点（产线爬坡后）
LOW_PCT = 35.0            # Markup 截面分位"崩价"阈值
HIGH_PCT = 65.0           # Markup 截面分位"稀缺"阈值
SUPPLY_HI = 0.20          # 家族成交量份额"高"阈值
PRODUCE_MIN_DAYS = 3      # 产能窗 sellable>0 日数下限

# 引擎基准价兜底（twin 装载时校验；MARKET_PARAMS.base）
BASE_PRICE_FALLBACK = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60,
                       "STRAWBERRY": 120, "MELON": 250, "EGG": 50,
                       "MILK": 160, "WOOL": 200, "FERTILIZER": 100}


def engine_base_prices():
    """twin 引擎 MARKET_PARAMS.base（装载失败 → 兜底表并记 fallback 位）。"""
    try:
        import sys
        if B._SOFTWARE not in sys.path:
            sys.path.insert(0, B._SOFTWARE)
        from kaggle_simulations.agent.planner import twin
        mod = twin.load_engine().module
        return {k: float(v.get("base")) for k, v in mod.MARKET_PARAMS.items()}, True
    except Exception:
        return dict(BASE_PRICE_FALLBACK), False


def item_price_percentile(daily_tables, base_prices=None):
    """单品项统计（两面分位）。

    输入：daily_tables = 逐局 daily_netflow_decompose 产物列表。
    输出：{item: {own_pct_mean, markup_pct_mean, own_pct_series_len,
    structural_low_price, structural_high_price, price_min/max,
    markup_median}}——structural 判定在 Markup 截面分位均值
    （days ≥ WINDOW_START_DAY 窗口）；own_pool 面为趋势证据。
    """
    if not daily_tables:
        return {}
    base_prices = base_prices or BASE_PRICE_FALLBACK
    pooled = {}
    for tab in daily_tables:
        for day in tab.get("days", []):
            for item, p in (day.get("px_mean") or {}).items():
                pooled.setdefault(item, []).append(float(p))
    own_pct_acc = {i: [] for i in pooled}
    markup_pct_acc = {i: [] for i in pooled}
    markup_acc = {i: [] for i in pooled}
    for tab in daily_tables:
        ep = tab.get("episode")
        for day in tab.get("days", []):
            if day.get("d", 0) < WINDOW_START_DAY:
                continue
            px = day.get("px_mean") or {}
            ratios = {}
            for item in B.PLANTABLE:
                p = px.get(item)
                if p is not None and base_prices.get(item):
                    ratios[item] = float(p) / float(base_prices[item])
            if len(ratios) >= 3:   # 截面分位需 ≥3 品在场
                order = sorted(ratios, key=lambda i: ratios[i])
                n = len(order)
                for rank, item in enumerate(order):
                    markup_pct_acc[item].append(100.0 * rank / (n - 1))
                    markup_acc[item].append(ratios[item])
            for item, p in px.items():
                series = pooled[item]
                below = sum(1 for x in series if x <= float(p))
                own_pct_acc[item].append(100.0 * below / len(series))
    out = {}
    for item, prices in pooled.items():
        own = own_pct_acc[item]
        mk = markup_pct_acc[item]
        own_mean = round(sum(own) / len(own), 1) if own else None
        mk_mean = round(sum(mk) / len(mk), 1) if mk else None
        mk_series = markup_acc[item]
        out[item] = {
            "own_pct_mean": own_mean,
            "markup_pct_mean": mk_mean,
            "n_window_obs": len(own),
            "structural_low_price": bool(mk_mean is not None
                                         and mk_mean <= LOW_PCT),
            "structural_high_price": bool(mk_mean is not None
                                          and mk_mean >= HIGH_PCT),
            "markup_median": round(sorted(mk_series)[len(mk_series) // 2], 3)
            if mk_series else None,
            "price_min": round(min(prices), 2),
            "price_max": round(max(prices), 2),
        }
    return out


def _supply_and_capacity(daily_tables):
    """家族成交量份额（供给密度）+ 我席（renyxin）逐品逐日 sellable 产能面。"""
    sales_share_acc = {}     # item -> [family vol share per (game,day)]
    our_daily = {}           # item -> {day: [sellable...]}（我席）
    for tab in daily_tables:
        our_seat = tab.get("our_seat")
        for day in tab.get("days", []):
            fam = {}
            mine = day["seats"][str(our_seat)]
            for seat in (0, 1):
                row = day["seats"][str(seat)]
                for item in set(row.get("vol_by_item") or {}):
                    v = float(row["vol_by_item"].get(item, 0))
                    if v > 0:
                        fam[item] = fam.get(item, 0.0) + v
            tot = sum(fam.values())
            for item, v in fam.items():
                if tot > 0:
                    sales_share_acc.setdefault(item, []).append(v / tot)
            if day.get("d", 0) >= WINDOW_START_DAY:
                for item in set(mine.get("vol_by_item") or {}) | set(mine.get("inv_end") or {}):
                    v = (float((mine.get("vol_by_item") or {}).get(item, 0))
                         + float((mine.get("inv_end") or {}).get(item, 0)))
                    if v > 0:
                        our_daily.setdefault(item, {}).setdefault(
                            day.get("d"), []).append(v)
    supply_share = {item: round(sum(v) / len(v), 4)
                    for item, v in sales_share_acc.items() if v}
    capacity = {}
    for item, per_day in our_daily.items():
        med = {d: sorted(v)[len(v) // 2] for d, v in per_day.items()}
        active = [d for d, v in med.items() if v > 0]
        capacity[item] = {
            "mean_daily_sellable": round(
                sum(sum(v) / len(v) for v in per_day.values())
                / max(1, len(per_day)), 2),
            "median_by_day": {str(d): round(v, 2)
                              for d, v in sorted(med.items())},
            "n_active_days": len(active),
        }
    return {"supply_share": supply_share, "capacity": capacity}


def rank_swap_pairs(item_stats):
    """崩价品 × 稀缺品置换对排序 + 产能窗图谱（空集 = KILLED 依据）。

    输入：item_stats = {"percentile", "supply_share", "capacity"}。
    输出：{"pairs": [{from, to, score, pct_gap, from_capacity,
    supply_share_from, window_days, window_n_days}],
    "crash_items", "scarce_items"}——score = 分位差/100 × 可置换产能。
    """
    pct = item_stats.get("percentile") or {}
    supply = item_stats.get("supply_share") or {}
    capacity = item_stats.get("capacity") or {}

    plantable = [i for i in B.PLANTABLE if i in pct
                 and pct[i].get("markup_pct_mean") is not None]
    ranked_supply = sorted(plantable,
                           key=lambda i: -supply.get(i, 0.0))
    top2 = set(ranked_supply[:2])
    crash = [i for i in plantable
             if pct[i]["structural_low_price"]
             and (supply.get(i, 0.0) >= SUPPLY_HI or i in top2)]
    scarce = [i for i in plantable if pct[i]["structural_high_price"]]

    pairs = []
    for src in crash:
        cap_src = capacity.get(src, {}).get("mean_daily_sellable") or 0.0
        med_src = capacity.get(src, {}).get("median_by_day") or {}
        src_days = sorted(int(d) for d, v in med_src.items() if v > 0)
        for dst in scarce:
            if dst == src:
                continue
            gap = pct[dst]["markup_pct_mean"] - pct[src]["markup_pct_mean"]
            deadline = 29 - B.FIRST_YIELD_DAY.get(dst, 0)
            window = [d for d in src_days if d <= deadline]
            pairs.append({
                "from": src, "to": dst,
                "score": round(gap / 100.0 * cap_src, 2),
                "pct_gap": round(gap, 1),
                "from_capacity": cap_src,
                "supply_share_from": supply.get(src),
                "markup_pct_from": pct[src]["markup_pct_mean"],
                "markup_pct_to": pct[dst]["markup_pct_mean"],
                "window_days": window,
                "window_n_days": len(window),
            })
    pairs.sort(key=lambda p: (-p["score"], p["from"], p["to"]))
    return {"pairs": pairs, "crash_items": crash, "scarce_items": scarce}


def phase_m_market_map(replay_dir):
    """市场地图编排：86 局 decompose → 品项分位/供给 → 置换对排序。

    输出：{items, swap_pairs_ranked, crash_items, scarce_items,
    capacity_windows, params, base_prices, n_games, n_ok, errors}——
    单局失败记录不中断（errors 面）。
    """
    base_prices, engine_ok = engine_base_prices()
    entries = _surge_corpus.discover_replays(replay_dir)
    daily_tables, errors = [], []
    for ep, path in entries:
        try:
            replay = _surge_corpus.load_replay(path)
            daily_tables.append(_surge_a.daily_netflow_decompose(replay))
        except Exception as exc:
            errors.append({"episode": ep,
                           "error": f"{type(exc).__name__}: {exc}"})
    pct = item_price_percentile(daily_tables, base_prices)
    sup = _supply_and_capacity(daily_tables)
    stats = dict(pct)
    for item, s in stats.items():
        s["supply_share"] = sup["supply_share"].get(item)
        if item in sup["capacity"]:
            s["capacity"] = sup["capacity"][item]
        hi_supply = (s["supply_share"] or 0.0) >= SUPPLY_HI
        ranked_supply = sorted(
            [i for i in stats if i in B.PLANTABLE],
            key=lambda i: -(stats[i].get("supply_share") or 0.0))
        top2 = set(ranked_supply[:2])
        s["structural_low"] = bool(s["structural_low_price"]
                                   and (hi_supply or item in top2))
        s["structural_high"] = bool(s["structural_high_price"])
    ranked = rank_swap_pairs({
        "percentile": stats, "supply_share": sup["supply_share"],
        "capacity": sup["capacity"]})
    windows = {f"{p['from']}->{p['to']}": p["window_days"]
               for p in ranked["pairs"]}
    return {
        "items": stats,
        "swap_pairs_ranked": ranked["pairs"],
        "crash_items": ranked["crash_items"],
        "scarce_items": ranked["scarce_items"],
        "capacity_windows": windows,
        "params": {"window_start_day": WINDOW_START_DAY,
                   "low_pct": LOW_PCT, "high_pct": HIGH_PCT,
                   "supply_hi": SUPPLY_HI, "produce_min_days": PRODUCE_MIN_DAYS},
        "base_prices": base_prices,
        "base_prices_from_engine": engine_ok,
        "n_games": len(entries), "n_ok": len(daily_tables), "errors": errors,
    }
