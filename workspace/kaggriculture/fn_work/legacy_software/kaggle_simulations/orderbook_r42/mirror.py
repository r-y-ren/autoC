# -*- coding: utf-8 -*-
"""apply_mirror_gate（R25 P3 镜像门控）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：双方公开农场指纹
相等→卖窗提前 2 拍+credit 等额扣减（禁净加卖）；只用公开面不做对手行为预测；
指纹缺失→门不触发；异常→零动作。

【口径】指纹=公开农场面（unlocked_quadrants/tiles 形态[逐格 kind/crop/
animal]/手数/畜群数）逐坐标比对（haodou092 V81 口径，references/
2026-09-28-execution-faces-scan.md 二-7）；提前量=2 拍（T4 口径）；
credit 记账=提前量按品项从后续计划等额扣减。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

SELL = "SELL"
MIRROR_ADVANCE = 2            # 提前拍数（T4）
TRAIL_WINDOW = 24             # 尾窗（拍）
REVEAL_STEP = 144


def _fingerprint(farm: Any) -> Optional[str]:
    """公开农场指纹（仅公开面字段）；缺关键字段→None。"""
    if not isinstance(farm, dict):
        return None
    tiles = farm.get("tiles")
    uq = farm.get("unlocked_quadrants")
    hands = farm.get("hands")
    if tiles is None or uq is None or hands is None:
        return None
    try:
        grid = []
        for row in (tiles if isinstance(tiles, list) else []):
            line = []
            for cell in (row if isinstance(row, list) else []):
                if isinstance(cell, dict):
                    line.append([cell.get("kind"), cell.get("crop"),
                                 cell.get("animal")])
                else:
                    line.append(cell)
            grid.append(line)
        return json.dumps({"uq": sorted(str(x) for x in uq),
                           "grid": grid,
                           "hands": len(hands if isinstance(hands, list)
                                        else [])},
                          sort_keys=True, default=str)
    except Exception:
        return None


def apply_mirror_gate(observation: Dict[str, Any],
                      action: Dict[str, Any]) -> Dict[str, Any]:
    """镜像门控。签名意图：输入: observation, action / 输出: {action,
    ledger, credit} / 错误: 异常→零动作（原样）。"""
    try:
        state = getattr(apply_mirror_gate, "_state", None)
        obs = observation if isinstance(observation, dict) else {}
        raw = obs.get("step")
        step = int(raw) if raw is not None else \
            int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))
        if state is None or step == 0 or step < state.get("last_step", -1):
            state = {"mirror": False, "credit": {}, "sold": {},
                     "last_step": -1}
            apply_mirror_gate._state = state
        state["last_step"] = step

        # credit 偿还（全模式生效：提前卖过的量从后续卖单等额扣）
        market = action.get("market") if isinstance(action, dict) and \
            isinstance(action.get("market"), list) else []
        out_market: List[Any] = []
        credit = state["credit"]
        repaid = 0
        for e in market:
            if isinstance(e, (list, tuple)) and len(e) >= 3 and \
                    str(e[0]) == SELL:
                item = str(e[1])
                try:
                    qty = int(e[2])
                except (TypeError, ValueError):
                    out_market.append(list(e) if isinstance(e, (list, tuple))
                                      else e)
                    continue
                debt = int(credit.get(item, 0))
                if debt > 0:
                    cut = min(debt, qty)
                    qty -= cut
                    credit[item] = debt - cut
                    repaid += cut
                    if qty <= 0:
                        continue                     # 全额抵扣→删单
                e2 = list(e)
                e2[2] = qty
                out_market.append(e2)
                state["sold"][item] = state["sold"].get(item, 0) + qty
            else:
                out_market.append(list(e) if isinstance(e, (list, tuple))
                                  else e)

        # 镜像判定（latch）：公开农场指纹逐坐标相等
        farms = obs.get("farms")
        seat = int(obs.get("player", 0))
        if not state["mirror"] and isinstance(farms, list) and \
                len(farms) == 2:
            fp0 = _fingerprint(farms[seat])
            fp1 = _fingerprint(farms[1 - seat])
            if fp0 is not None and fp0 == fp1:
                state["mirror"] = True

        boosted = 0
        if state["mirror"]:
            priv = obs.get("private") if isinstance(obs.get("private"),
                                                    dict) else {}
            shed = priv.get("shed") if isinstance(priv.get("shed"), dict) \
                else {}
            have = {str(k): int(v) for k, v in (shed or {}).items()
                    if isinstance(v, (int, float))}
            listed: Dict[str, int] = {}
            for e in out_market:
                if isinstance(e, (list, tuple)) and len(e) >= 3 and \
                        str(e[0]) == SELL:
                    listed[str(e[1])] = listed.get(str(e[1]), 0) + \
                        int(e[2])
            for item in sorted(state["sold"]):
                rate = state["sold"][item] / float(TRAIL_WINDOW)
                if rate <= 0:
                    continue
                extra = int(round(MIRROR_ADVANCE * rate))
                room = have.get(item, 0) - listed.get(item, 0)
                extra = max(0, min(extra, room))
                if extra > 0:
                    out_market.append([SELL, item, extra])
                    credit[item] = int(credit.get(item, 0)) + extra
                    boosted += extra

        if not isinstance(action, dict):
            return {"action": action, "ledger": {"failed": True}}
        out_action = dict(action)
        out_action["market"] = out_market
        return {"action": out_action,
                "ledger": {"mirror": state["mirror"], "boosted": boosted,
                           "repaid": repaid, "step": step},
                "credit": dict(credit)}
    except Exception:
        return {"action": action, "ledger": {"failed": True}}
