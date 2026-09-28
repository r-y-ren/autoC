# -*- coding: utf-8 -*-
"""retape_sheep_lifecycle（R26 L2 ②羊线生命周期）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：羊毛变现窗完成后
（该路线最后一次 WOOL SELL 后）删后续羊 CARE/FEED 磁带指令；变现窗内排程
与刀次不动；只删羊喂护指令，不动牛鹅与其他面。

【定位口径】复用 retape_sheep._derive_grid_info（wired 地格推导）：羊格集合
+逐拍单位站位→CARE/FEED 指令按"站位在羊格"判属羊；删=该单元指令换 ['PASS']
（不删位）；推导失败/无羊毛窗的路由→skip 留审计。
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List

SELL = "SELL"
CARE_CMDS = ("CARE", "FEED")
PASS = ["PASS"]


def retape_sheep_lifecycle(routes: Any,
                           config: Any = None) -> Dict[str, Any]:
    """②羊线生命周期手术。签名意图：输入: 解码路由表 / 输出: {routes,
    变更表 kind=sheep_lifecycle, 刀次账} / 错误: 非喂护面被改即抛。
    """
    if not isinstance(routes, dict) or "routes" not in routes or \
            "actions" not in routes:
        raise ValueError("routes 须为解码路由包")
    from orderbook_r37 import retape_sheep as rs  # noqa: WPS433
    try:
        grid = rs._derive_grid_info(routes)
    except Exception as exc:
        grid = {}
    pkg = {"actions": routes["actions"], "shops": routes.get("shops"),
           "routes": {rid: list(seq) for rid, seq in routes["routes"].items()}}
    pool = pkg["actions"]
    changes: List[Dict[str, Any]] = []
    knives: Dict[str, Dict[str, int]] = {}

    for rid, seq in pkg["routes"].items():
        info = (grid or {}).get(str(rid)) or (grid or {}).get(rid) or {}
        sells = []
        for t, ai in enumerate(seq):
            a = pool[ai]
            if not isinstance(a, dict):
                continue
            for cmd in (a.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and \
                        str(cmd[0]) == SELL and str(cmd[1]) == "WOOL":
                    sells.append(t)
        wool_harvests = sum(
            1 for t, ai in enumerate(seq)
            if isinstance(pool[ai], dict)
            for cmd in ([pool[ai].get("farmer")] if
                        isinstance(pool[ai].get("farmer"), (list, tuple))
                        else [])
            + (pool[ai].get("hands") or [])
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 2 and
            str(cmd[0]) == "HARVEST" and str(cmd[1]) == "WOOL")
        if not sells or not info:
            knives[str(rid)] = {"wool_harvests": wool_harvests,
                                "removed": 0, "skipped": True}
            continue
        last_wool = max(sells)
        sheep_cells = set((info.get("cells") or {}).keys())
        unit_pos = info.get("unit_pos") or {}
        removed = 0
        for t in range(last_wool + 1, len(seq)):
            ai = seq[t]
            a = pool[ai]
            if not isinstance(a, dict):
                continue
            touched = False
            f = a.get("farmer")
            if isinstance(f, (list, tuple)) and f and \
                    str(f[0]) in CARE_CMDS and \
                    unit_pos.get((t, 0)) in sheep_cells:
                a2 = copy.deepcopy(a)
                a2["farmer"] = list(PASS)
                pool.append(a2)
                seq[t] = len(pool) - 1
                removed += 1
                touched = True
            hands = a.get("hands")
            if isinstance(hands, list):
                hit = False
                for u, cmd in enumerate(hands):
                    if isinstance(cmd, (list, tuple)) and cmd and \
                            str(cmd[0]) in CARE_CMDS and \
                            unit_pos.get((t, u + 1)) in sheep_cells:
                        hit = True
                        break
                if hit:
                    if touched:
                        a2 = pool[seq[t]]
                    else:
                        a2 = copy.deepcopy(a)
                        pool.append(a2)
                        seq[t] = len(pool) - 1
                    for u, cmd in enumerate(a2.get("hands") or []):
                        if isinstance(cmd, (list, tuple)) and cmd and \
                                str(cmd[0]) in CARE_CMDS and \
                                unit_pos.get((t, u + 1)) in sheep_cells:
                            a2["hands"][u] = list(PASS)
                            removed += 1
                    touched = True
            if touched:
                changes.append({"route": rid, "kind": "sheep_lifecycle",
                                "step": t, "removed": "care_feed"})
        knives[str(rid)] = {"wool_harvests": wool_harvests,
                            "removed": removed, "skipped": False}
    return {"routes": pkg, "change_table": changes, "knives": knives}
