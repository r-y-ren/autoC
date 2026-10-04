# -*- coding: utf-8 -*-
"""retape_drain_aligned（R26 L2 ①排水对齐卖序）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：逐路线把 SELL 事件
时点重排到期望排水节奏；守恒铁律：逐品总卖出量恒等、终拍排空（stranding≈0）、
同拍同品并单语义保留；只动 SELL 的时点与单量拆分，不动 BUY/FEED/CARE/HARVEST。

【槽位纪律】（retape_sheep 742943 先例）：挪单=源槽换 [] 或减量 + 目标步市场
列表**尾部追加**（既有槽位不删不移不填——删/填改撮合配对）；只推后不提前
（"卖早=贱"行为面+资金序安全）。
"""
from __future__ import annotations

import copy
import math
from typing import Any, Dict, List, Tuple

WINDOW_START_STEP = 264      # d11 起（保护开局现金流）
TERMINAL_STEP = 716          # 终拍排空锚（其前未消化量全部落此）
CAP_MULT_DEFAULT = 1.0
SELL = "SELL"


def _sells_of(pool: List[Any], seq: List[int]) -> List[Tuple[int, int, str, int]]:
    """逐路线 SELL 收集：[(step, slot_idx, item, qty)]。"""
    out = []
    for t, ai in enumerate(seq):
        a = pool[ai]
        if not isinstance(a, dict):
            continue
        for j, cmd in enumerate(a.get("market") or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and \
                    str(cmd[0]) == SELL:
                out.append((t, j, str(cmd[1]), int(cmd[2])))
    return out


def retape_drain_aligned(routes: Any, drain_table: Any = None,
                         config: Any = None) -> Dict[str, Any]:
    """①排水对齐卖序。签名意图：输入: 解码路由表+排水表 / 输出: {routes,
    守恒账, 变更表 kind=drain_align} / 错误: 守恒破或非卖面被改即抛。
    """
    if not isinstance(routes, dict) or "routes" not in routes or \
            "actions" not in routes:
        raise ValueError("routes 须为解码路由包")
    cfg = config if isinstance(config, dict) else {}
    cap_mult = float(cfg.get("cap_mult", CAP_MULT_DEFAULT))
    window_start = int(cfg.get("window_start", WINDOW_START_STEP))
    terminal = int(cfg.get("terminal_step", TERMINAL_STEP))
    if drain_table is None:
        from orderbook_r43.drain_table import build_drain_table  # noqa: WPS433
        drain_table = build_drain_table()
    pkg = {"actions": routes["actions"], "shops": routes.get("shops"),
           "routes": {rid: list(seq) for rid, seq in routes["routes"].items()}}
    pool = pkg["actions"]
    changes: List[Dict[str, Any]] = []
    conserve: Dict[str, Dict[str, int]] = {}

    def _cow(rid: str, step: int) -> int:
        """写时复制：该步动作克隆入池并重指（池共享防污染）。"""
        old = pool[pkg["routes"][rid][step]]
        new = copy.deepcopy(old)
        pool.append(new)
        idx = len(pool) - 1
        seq_ = pkg["routes"][rid]
        seq_[step] = idx
        return new

    def _append_sell(rid: str, step: int, item: str, qty: int) -> None:
        a = _cow(rid, step)
        m = a.setdefault("market", []) if isinstance(a, dict) else None
        if not isinstance(m, list):
            raise RuntimeError("目标步市场列表形态非法 @%s:%d" % (rid, step))
        m.append([SELL, item, qty])

    for rid, seq in pkg["routes"].items():
        drain = (drain_table or {}).get(str(rid))
        if not drain:
            conserve[str(rid)] = {"changed": 0}
            continue
        term = min(terminal, len(seq) - 1)
        sells = _sells_of(pool, seq)
        before: Dict[str, int] = {}
        for _t, _j, item, qty in sells:
            before[item] = before.get(item, 0) + qty
        used: Dict[Tuple[int, str], int] = {}     # (day, item) 已售
        moved = 0
        for t, j, item, qty in sells:
            cap_day = drain.get(item, 0.0) * cap_mult
            if t < window_start or cap_day <= 0 or qty <= 0:
                continue
            day = t // 24
            avail = int(math.ceil(cap_day)) - used.get((day, item), 0)
            keep = min(qty, max(0, avail))
            defer = qty - keep
            if keep < qty:
                used[(day, item)] = used.get((day, item), 0) + keep
            else:
                used[(day, item)] = used.get((day, item), 0) + qty
            if defer <= 0:
                continue
            # 源槽：全延→[]；部分延→减量（写时复制）
            a = _cow(rid, t)
            slot = a["market"][j]
            if keep <= 0:
                a["market"][j] = []
            else:
                a["market"][j] = [SELL, item, keep]
            # 目标：向后找有当日余量的步；终拍兜底
            placed = 0
            step = t + 1
            while placed < defer and step <= term:
                d2 = step // 24
                if step >= term:
                    avail2 = defer - placed       # 终拍兜底不限量
                else:
                    avail2 = int(math.ceil(cap_day)) - \
                        used.get((d2, item), 0)
                take = min(defer - placed, max(0, avail2))
                if take > 0:
                    _append_sell(rid, step, item, take)
                    used[(d2, item)] = used.get((d2, item), 0) + take
                    changes.append({"route": rid, "kind": "drain_align",
                                    "item": item, "from_step": t,
                                    "to_step": step, "qty": take})
                    placed += take
                step += 1
            if placed < defer:
                _append_sell(rid, term, item, defer - placed)
                changes.append({"route": rid, "kind": "drain_align",
                                "item": item, "from_step": t,
                                "to_step": terminal, "qty": defer - placed})
            moved += defer
        after: Dict[str, int] = {}
        for _t, _j, item, qty in _sells_of(pool, pkg["routes"][rid]):
            after[item] = after.get(item, 0) + qty
        if before != after:
            raise RuntimeError("排水对齐守恒破 @%s: %r vs %r"
                               % (rid, before, after))
        conserve[str(rid)] = {"changed": moved}
    return {"routes": pkg, "conservation": conserve,
            "change_table": changes}
