# -*- coding: utf-8 -*-
"""apply_endgame_liquidation（R25 P2 终日清算器）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：step≥648 切换清算
模式（停 BUY 类、仓内可卖品按 −price×qty 降序出清）；steps 712-718 七拍显式
清算序；终拍滞留归零目标；异常→原动作。

【机制口径】E182 七拍清算序（references/2026-09-28-execution-faces-scan.md
二-6/8）；清算节奏=按剩余拍数均摊递增，712-718 段全量出清。
"""
from __future__ import annotations

import math
from typing import Any, Dict, List

LIQUIDATE_STEP = 648          # day27 起清算模式
END_STEP = 719                # 末拍
BUY_PREFIXES = ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "BUY_LAND")
SELL = "SELL"
MAX_ORDERS = 10


def apply_endgame_liquidation(observation: Dict[str, Any],
                              action: Dict[str, Any]) -> Dict[str, Any]:
    """终日清算器。签名意图：输入: observation, action / 输出: {action,
    ledger}（action.market 替换为清算段） / 错误: 异常→原动作。"""
    try:
        if not isinstance(action, dict):
            return {"action": action, "ledger": {"failed": True}}
        obs = observation if isinstance(observation, dict) else {}
        raw = obs.get("step")
        step = int(raw) if raw is not None else \
            int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))
        if step < LIQUIDATE_STEP:
            return {"action": action, "ledger": {"noop": True}}
        priv = obs.get("private") if isinstance(obs.get("private"), dict) \
            else {}
        shed = priv.get("shed") if isinstance(priv.get("shed"), dict) else {}
        market = obs.get("market") if isinstance(obs.get("market"), dict) \
            else {}
        prices = market.get("prices") if isinstance(market.get("prices"),
                                                    dict) else {}

        kept: List[Any] = []
        for e in (action.get("market") or []):
            if isinstance(e, (list, tuple)) and e and \
                    str(e[0]).startswith(BUY_PREFIXES):
                continue                             # 停采购类
            if isinstance(e, (list, tuple)) and len(e) >= 3 and \
                    str(e[0]) == SELL:
                continue                             # 旧卖单由清算序取代
            kept.append(list(e) if isinstance(e, (list, tuple)) else e)

        # 清算卖单：按 −price×qty 降序；节奏=ceil(库存/剩余拍数) 递增出清
        remaining = max(1, END_STEP - step)
        rows = []
        for item, qty in (shed or {}).items():
            try:
                q = int(qty)
            except (TypeError, ValueError):
                continue
            if q <= 0:
                continue
            px = prices.get(str(item), 0)
            px = float(px) if isinstance(px, (int, float)) else 0.0
            lots = min(q, int(math.ceil(q / float(remaining))))
            if step >= 712:
                lots = q                             # 七拍段全量出清
            if lots > 0:
                rows.append((-(px * lots), str(item), lots))
        rows.sort()
        sells = [[SELL, item, lots] for _v, item, lots in rows]
        out_market = (sells + kept)[:MAX_ORDERS]
        out_action = dict(action)
        # 清算序=卖单前部（保 10 槽内优先成交）
        out_action["market"] = (sells + kept)[:MAX_ORDERS]
        return {"action": out_action, "ledger": {
            "mode": "liquidation", "step": step,
            "n_sells": len(sells), "remaining_beats": remaining,
            "forced_full": step >= 712,
        }}
    except Exception:
        return {"action": action, "ledger": {"failed": True}}
