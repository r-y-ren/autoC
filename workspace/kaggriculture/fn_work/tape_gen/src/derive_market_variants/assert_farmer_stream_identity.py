"""assert_farmer_stream_identity（L1，R3）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

farmer 流恒等断言：变体路由与骨干的 farmer+hands 走位流**逐字节恒等**
（719 步规范 JSON 逐步比较，市场单不计——市场编辑算子只许动 market）。
附带市场单差分账：逐步统计 market 变更（added/removed/changed 订单），
供差分账本消费。

返回恒等记录 {ok, checked_steps, first_divergence, farmer_sha256{a,b},
market_diff}；strict=True 时失配抛 AssertionError（fail-closed）。
"""

from __future__ import annotations

import hashlib
import json


def _movement_key(step: dict) -> str:
    return json.dumps({"farmer": step.get("farmer"),
                       "hands": step.get("hands") or []},
                      sort_keys=True, separators=(",", ":"))


def _market_key(order) -> str:
    return json.dumps(order, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _market_diff(route_a, route_b, limit: int = 64):
    """逐步市场差分（相对 route_a 视角：added/removed 样本 + 变更步总数）。"""
    diff = []
    n_changed = 0
    for t, (sa, sb) in enumerate(zip(route_a, route_b)):
        ma = [_market_key(o) for o in (sa.get("market") or [])]
        mb = [_market_key(o) for o in (sb.get("market") or [])]
        if ma == mb:
            continue
        n_changed += 1
        if len(diff) < limit:
            added = [json.loads(k) for k in ma if k not in mb]
            removed = [json.loads(k) for k in mb if k not in ma]
            diff.append({"step": t, "added": added, "removed": removed})
    return diff, n_changed


def assert_farmer_stream_identity(payload=None):
    """意图级签名；真值在责任文档。

    payload：{route, backbone（或 route_a/route_b 二选一）, strict=bool}。
    返回恒等记录；strict=True 且失配时 raise AssertionError。
    """
    payload = dict(payload or {})
    route = payload.get("route") or payload.get("route_a")
    backbone = payload.get("backbone") or payload.get("route_b")
    if not route or not backbone:
        raise ValueError("assert_farmer_stream_identity needs route and "
                         "backbone (fail-closed)")
    if len(route) != len(backbone):
        result = {
            "ok": False,
            "checked_steps": min(len(route), len(backbone)),
            "length_mismatch": [len(route), len(backbone)],
            "first_divergence": None,
            "farmer_sha256": {},
            "market_changed_steps": 0,
            "market_diff": [],
        }
        if payload.get("strict"):
            raise AssertionError(
                "farmer stream identity violated: length mismatch "
                f"{result['length_mismatch']}")
        return result

    first_div = None
    for t, (sa, sb) in enumerate(zip(route, backbone)):
        if _movement_key(sa) != _movement_key(sb):
            first_div = t
            break
    ha = hashlib.sha256("\n".join(_movement_key(s)
                                  for s in route).encode("utf-8"))
    hb = hashlib.sha256("\n".join(_movement_key(s)
                                  for s in backbone).encode("utf-8"))
    diff, n_changed = _market_diff(route, backbone)
    result = {
        "ok": first_div is None,
        "checked_steps": len(route),
        "first_divergence": first_div,
        "farmer_sha256": {"route": ha.hexdigest(),
                          "backbone": hb.hexdigest()},
        "market_changed_steps": n_changed,
        "market_diff": diff,
    }
    if payload.get("strict") and not result["ok"]:
        raise AssertionError(
            "farmer stream identity violated: first divergence at step "
            f"{first_div}")
    return result
