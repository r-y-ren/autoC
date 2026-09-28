# -*- coding: utf-8 -*-
"""retape_granularity（R26 L2 ③跨拍细颗粒）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：大额同拍 SELL
（超过阈值）按该品排水节奏拆分至相邻拍（目标单均量向 4.6-5.9 量级靠拢）；
逐品守恒；同拍内同品仍并单（只拆跨拍）。
【槽位纪律】拆分=源槽减量+目标步市场列表尾部追加；只拆不合。
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List

SELL = "SELL"
SPLIT_THRESHOLD = 12         # 超过才拆（单均量向 4.6-5.9 靠拢）
CHUNK_SIZE = 6
MAX_FORWARD = 6              # 最多向后摊 6 拍


def retape_granularity(routes: Any, drain_table: Any = None,
                       config: Any = None) -> Dict[str, Any]:
    """③跨拍细颗粒。签名意图：输入: 解码路由表+排水表+阈值配置 / 输出:
    {routes, 变更表 kind=granularity, 守恒账} / 错误: 守恒破即抛。
    """
    if not isinstance(routes, dict) or "routes" not in routes or \
            "actions" not in routes:
        raise ValueError("routes 须为解码路由包")
    cfg = config if isinstance(config, dict) else {}
    threshold = int(cfg.get("threshold", SPLIT_THRESHOLD))
    chunk = int(cfg.get("chunk", CHUNK_SIZE))
    max_forward = int(cfg.get("max_forward", MAX_FORWARD))
    pkg = {"actions": routes["actions"], "shops": routes.get("shops"),
           "routes": {rid: list(seq) for rid, seq in routes["routes"].items()}}
    pool = pkg["actions"]
    changes: List[Dict[str, Any]] = []
    conserve: Dict[str, Dict[str, int]] = {}

    def _cow(rid: str, step: int):
        old = pool[pkg["routes"][rid][step]]
        new = copy.deepcopy(old)
        pool.append(new)
        pkg["routes"][rid][step] = len(pool) - 1
        return new

    def _append_sell(rid: str, step: int, item: str, qty: int) -> bool:
        if step >= len(pkg["routes"][rid]):
            return False
        a = _cow(rid, step)
        m = a.setdefault("market", []) if isinstance(a, dict) else None
        if not isinstance(m, list):
            return False
        m.append([SELL, item, qty])
        return True

    def _sells(rid: str) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for ai in pkg["routes"][rid]:
            a = pool[ai]
            if not isinstance(a, dict):
                continue
            for cmd in (a.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and \
                        str(cmd[0]) == SELL:
                    out[str(cmd[1])] = out.get(str(cmd[1]), 0) + int(cmd[2])
        return out

    for rid, seq in pkg["routes"].items():
        before = _sells(rid)
        split = 0
        t = 0
        while t < len(seq):
            ai = seq[t]
            a = pool[ai]
            if not isinstance(a, dict):
                t += 1
                continue
            m = a.get("market")
            hit = False
            if isinstance(m, list):
                for j, cmd in enumerate(m):
                    if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                            and str(cmd[0]) == SELL and \
                            int(cmd[2]) >= threshold:
                        item = str(cmd[1])
                        qty = int(cmd[2])
                        keep = min(qty, chunk)
                        rest = qty - keep
                        a2 = _cow(rid, t)
                        a2["market"][j] = [SELL, item, keep]
                        step = t + 1
                        while rest > 0 and step <= t + max_forward:
                            take = min(rest, chunk)
                            if _append_sell(rid, step, item, take):
                                changes.append({"route": rid,
                                                "kind": "granularity",
                                                "item": item, "from_step": t,
                                                "to_step": step, "qty": take})
                                rest -= take
                                split += take
                            step += 1
                        if rest > 0:                       # 摊不完→原槽保留
                            a2["market"][j] = [SELL, item, keep + rest]
                        hit = True
            if hit:
                t += 2                     # 已处理本拍与最近后续拍
            else:
                t += 1
        after = _sells(rid)
        if before != after:
            raise RuntimeError("细颗粒守恒破 @%s: %r vs %r"
                               % (rid, before, after))
        conserve[str(rid)] = {"split": split}
    return {"routes": pkg, "conservation": conserve,
            "change_table": changes}
