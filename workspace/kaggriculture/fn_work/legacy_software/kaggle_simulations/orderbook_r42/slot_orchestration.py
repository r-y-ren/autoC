# -*- coding: utf-8 -*-
"""apply_slot_orchestration 及三子件（R25 P1 卖单槽位编排）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：step≥144 卖单窗逐拍
对自家 market 卖单列表：同品合并/死单清理（错位后移类，qty==0 归旧件）/
现金净卖单前置早槽/摆法择优 ≤4 候选；不动 HARVEST/买单/空槽位次语义；
V57 资金序不变量；异常→原动作。

【机制口径】（references/2026-09-28-execution-faces-scan.md 一-1~5 引擎一手）
- 槽位 lockstep：双方市场单按列表下标配对，同槽单位 1:1 交替成交；
- 逐单位按共享库存重报价：单内越靠后越便宜，成交价由全局流位置决定；
- maxMarketOrdersPerTurn=10 硬截断（超出直接丢弃）；死单（qty 0/仓空/钱
  不够 abort）不耗成交轮但占槽位，把后续真实卖单配对整体后移。
签名微调登记（batches.md 2026-09-28）：①合并/清理只动 SELL 项（买单/HIRE/
空槽不动），同品合并腾位以 [] 占位保槽位次；②select_best_layout 第二参=
公开市场态（观察无盘口字段，对手模型=同槽 1:1 交错内化进迷你模拟）；
③clear_dead_slots 第三参 stock=可卖库存，判据=会 abort 的卖单。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

MAX_ORDERS = 10          # maxMarketOrdersPerTurn（引擎硬截断）
DECAY_DEFAULT = 0.99     # 迷你模拟逐单位价格衰减（越靠后越便宜）
SELL = "SELL"


def _is_sell(entry: Any) -> bool:
    return isinstance(entry, (list, tuple)) and len(entry) >= 3 and \
        str(entry[0]) == SELL


def _copy(orders: Any) -> List[Any]:
    if not isinstance(orders, (list, tuple)):
        raise TypeError("orders 须为 list")
    return [list(e) if isinstance(e, (list, tuple)) else e for e in orders]


def merge_same_item_orders(orders: Any) -> Dict[str, Any]:
    """同品 SELL 合并：同品多单→首位置一张（qty 求和），腾位以 [] 保槽位次。

    只动 SELL；BUY_*/HIRE/空槽不动。守恒校验：合并前后逐品 SELL 总量恒等。
    签名意图：输入: 卖单列表 / 输出: {orders, merged, conserved} /
    错误: 守恒破或输入非法→抛。
    """
    out = _copy(orders)
    before: Dict[str, int] = {}
    seen: Dict[str, int] = {}
    merged = 0
    for i, e in enumerate(out):
        if not _is_sell(e):
            continue
        item = str(e[1])
        before[item] = before.get(item, 0) + int(e[2])
        if item in seen:
            first = seen[item]
            out[first] = list(out[first])
            out[first][2] = int(out[first][2]) + int(e[2])
            out[i] = []
            merged += 1
        else:
            seen[item] = i
    after: Dict[str, int] = {}
    for e in out:
        if _is_sell(e):
            after[str(e[1])] = after.get(str(e[1]), 0) + int(e[2])
    if before != after:
        raise ValueError("合并守恒破: %r vs %r" % (before, after))
    return {"orders": out, "merged": merged, "conserved": True}


def clear_dead_slots(orders: Any, last_fills: Any = None,
                     stock: Any = None) -> Dict[str, Any]:
    """死单清理（会 abort 的卖单：qty<0/库存 0/量超库存则截到库存）。

    qty==0 真占坑归旧件 hygiene 不重复；腾位以 [] 保槽位次。
    签名意图：输入: 卖单列表+上一拍成交回报+可卖库存 / 输出: {orders,
    cleared, trimmed} / 错误: 异常→原列表（fail-safe）。
    """
    try:
        out = _copy(orders)
        cleared = 0
        trimmed = 0
        stock_map: Optional[Dict[str, int]] = None
        if isinstance(stock, dict):
            stock_map = {}
            for k, v in stock.items():
                try:
                    stock_map[str(k)] = int(v)
                except (TypeError, ValueError):
                    continue
        for i, e in enumerate(out):
            if not _is_sell(e):
                continue
            item = str(e[1])
            try:
                qty = int(e[2])
            except (TypeError, ValueError):
                out[i] = []
                cleared += 1
                continue
            if qty < 0:
                out[i] = []
                cleared += 1
                continue
            if stock_map is not None:
                avail = stock_map.get(item, 0)
                if avail <= 0 and qty > 0:
                    out[i] = []
                    cleared += 1
                elif qty > avail > 0:
                    e2 = list(e)
                    e2[2] = avail
                    out[i] = e2
                    trimmed += 1
        return {"orders": out, "cleared": cleared, "trimmed": trimmed}
    except Exception:
        return {"orders": list(orders) if isinstance(orders, (list, tuple))
                else orders, "cleared": 0, "trimmed": 0, "failed": True}


def _entry_price(entry: Any, prices: Any) -> float:
    if isinstance(prices, dict):
        px = prices.get(str(entry[1]))
        if isinstance(px, (int, float)):
            return float(px)
    return 0.0


def select_best_layout(pending: Any, book: Any = None,
                       config: Any = None) -> Dict[str, Any]:
    """摆法择优：≤4 候选（原序/单价降序/价值降序/数量降序）逐候选迷你盘口
    模拟（同槽 1:1 交错内化、逐单位衰减重报价）取得分最优。

    签名意图：输入: 待发卖单（(idx, entry, price) 三元组序列）+公开市场态 /
    输出: {order, best, scores} / 错误: 异常→首候选（原序）。
    """
    try:
        cfg = config if isinstance(config, dict) else {}
        decay = float(cfg.get("decay", DECAY_DEFAULT))
        items = [tuple(x) for x in (pending or [])]

        def _score(layout: List[Tuple[Any, Any, Any]]) -> float:
            pos = 0
            total = 0.0
            for _idx, entry, px in layout:
                qty = max(0, int(entry[2]))
                for k in range(qty):
                    total += float(px) * (decay ** (pos + k))
                pos += qty
            return round(total, 6)

        cands = {
            "original": sorted(items, key=lambda t: t[0]),
            "price_desc": sorted(items, key=lambda t: (-float(t[2]), t[0])),
            "value_desc": sorted(
                items, key=lambda t: (-(float(t[2]) * max(0, int(t[1][2]))),
                                      t[0])),
            "qty_desc": sorted(items, key=lambda t: (-max(0, int(t[1][2])),
                                                     t[0])),
        }
        scores = {name: _score(layout) for name, layout in cands.items()}
        best = max(sorted(scores), key=lambda n: (scores[n], n == "original"))
        return {"order": cands[best], "best": best, "scores": scores}
    except Exception:
        first = sorted([tuple(x) for x in (pending or [])],
                       key=lambda t: t[0])
        return {"order": first, "best": "original", "scores": {},
                "failed": True}


def apply_slot_orchestration(observation: Dict[str, Any],
                             action: Dict[str, Any]) -> Dict[str, Any]:
    """卖单槽位编排主件：合并→清死单→摆法择优→空槽尾裁（>10 单时）。

    签名意图：输入: observation, action / 输出: {action, ledger} /
    错误: 异常→原动作（fail-safe）。
    """
    try:
        if not isinstance(action, dict):
            return {"action": action, "ledger": {"failed": True}}
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return {"action": action, "ledger": {"noop": True}}
        obs = observation if isinstance(observation, dict) else {}
        priv = obs.get("private")
        stock = priv.get("shed") if isinstance(priv, dict) else None

        step1 = merge_same_item_orders(market)
        step2 = clear_dead_slots(step1["orders"], None, stock)
        orders = step2["orders"]

        # 卖单槽内重排（只动 SELL 占位；买单/HIRE/空槽原位不动）
        sell_idx = [i for i, e in enumerate(orders) if _is_sell(e)]
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        pending = [(i, orders[i], _entry_price(orders[i], prices))
                   for i in sell_idx]
        layout = select_best_layout(pending, obs.get("market"))
        if not layout.get("failed") and sell_idx:
            for slot, (_i, entry, _px) in zip(sell_idx, layout["order"]):
                orders[slot] = entry

        # >10 单截断防御：仅裁尾部空槽（空槽被丢无害；其余项不动）
        trimmed_empties = 0
        while len(orders) > MAX_ORDERS and orders and orders[-1] == []:
            orders.pop()
            trimmed_empties += 1

        out_action = dict(action)
        out_action["market"] = orders
        return {"action": out_action, "ledger": {
            "merged": step1["merged"], "cleared": step2["cleared"],
            "trimmed": step2.get("trimmed", 0), "layout": layout.get("best"),
            "trimmed_empties": trimmed_empties,
            "over_cap": len(orders) > MAX_ORDERS,
        }}
    except Exception:
        return {"action": action, "ledger": {"failed": True}}
