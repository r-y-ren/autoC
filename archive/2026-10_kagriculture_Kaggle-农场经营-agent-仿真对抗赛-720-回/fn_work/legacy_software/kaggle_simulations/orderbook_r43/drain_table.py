# -*- coding: utf-8 -*-
"""build_drain_table（R26 L2）：期望排水表。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：对每条路线求其服务的
店对集合（基座锁存表反查），按引擎排水规则（每 4 步每店各 1 件/单品店×2+
每 24 步中心全品各 1；references/2026-09-28-engine-pricing-extraction.md 四节）
算逐品逐日期望排水量。
"""
from __future__ import annotations

from typing import Any, Dict, List

#: 引擎 SHOPS 表（kaggriculture.py L103-111，源码直读）
SHOPS: Dict[str, List[str]] = {
    "BAKERY": ["EGG", "WHEAT"],
    "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
TOWN_CENTER_PRODUCTS = ("CARROT", "EGG", "MELON", "MILK", "STRAWBERRY",
                        "TOMATO", "WHEAT", "WOOL")
SHOP_DRAINS_PER_DAY = 6          # 每 4 步一次 × 6 次/日
CENTER_DRAINS_PER_DAY = 1        # 每 24 步一次


def build_drain_table(latch: Any = None, config: Any = None) \
        -> Dict[str, Dict[str, float]]:
    """期望排水表。签名意图：输入: 锁存表（或 pair→route 映射）+配置 /
    输出: {route_id: {item: 日排水}} / 错误: 表缺即抛。
    """
    cfg = config if isinstance(config, dict) else {}
    if latch is None:
        from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
        base = ab._base_route_map()            # {pair_str(排序归一): route}
    elif isinstance(latch, dict):
        base = {"+".join(sorted(str(s) for s in k.split("+"))): int(v)
                for k, v in latch.items()}
    else:
        raise ValueError("latch 形态非法")
    if not base:
        raise ValueError("锁存表为空")

    route_pairs: Dict[int, List[str]] = {}
    for pair, route in base.items():
        route_pairs.setdefault(int(route), []).append(pair)

    table: Dict[str, Dict[str, float]] = {}
    for route, pairs in route_pairs.items():
        per_item: Dict[str, float] = {item: 0.0 for item in
                                      TOWN_CENTER_PRODUCTS}
        for pair in pairs:
            for shop in pair.split("+"):
                products = SHOPS.get(shop)
                if not products:
                    continue
                mult = 2 if len(products) == 1 else 1
                for item in products:
                    per_item[item] += SHOP_DRAINS_PER_DAY * mult
        for item in TOWN_CENTER_PRODUCTS:
            per_item[item] += CENTER_DRAINS_PER_DAY
        n = len(pairs)
        table[str(route)] = {k: round(v / n, 3) for k, v in per_item.items()}
    return table
