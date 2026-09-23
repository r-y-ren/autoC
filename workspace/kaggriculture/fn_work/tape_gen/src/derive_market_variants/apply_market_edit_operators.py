"""apply_market_edit_operators（L1，R3）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

市场单编辑算子集（文档化；骨干 farmer+hands 走位流永不动——变体只改
market 列表）。三个算子（v48 先例：farm_fast=卖单 ±1-3 天时移、
bakery_capital=定点市场重写；本件泛化为算子×参数）：

1. ``shift_sells_by_days``（时点平移）：把窗口内 SELL 单整体平移
   days×72 步（1 天 = 72 步，日界步长实测）；落点钳位 [0,718]；落点
   槽位满（该步市场单 ≥10）时在 ±72 步（一天）内交错顺延安置，仍无
   空槽则记入 dropped（守恒破口入账本）。位移有界（≤1 天漂移），
   绝不回卷到磁带对面。非 SELL 单不动；安置序确定（目标步序+源序）。
2. ``scale_sell_quantities``（量缩放）：窗口内 SELL 单量
   q -> max(1, round(q×ratio))；非 SELL 单与其余步不动。
3. ``daily_sell_cap``（日帽）：按日（步 [72d, 72d+72)）逐品类累计卖量
   封顶 cap，超出部分按时间序截断（部分单减量、余单清零移除），截断量
   记入账本。

输出：{route, changes}——changes 为差分账本行（算子/参数/逐类计数/
窗口/守恒账）。确定性：同输入同输出，全排序。
"""

from __future__ import annotations

import copy

#: 游戏步/日（事件步实测：解锁落 72k 步）。
STEPS_PER_DAY = 72
#: 每步市场单槽上限（v48 动作编码 ≤10 单/步）。
MARKET_SLOTS = 10
#: 时移落点顺延搜索半径（步）= 1 天（位移有界，绝不回卷磁带对面）。
SHIFT_SLACK = 72

OPERATORS = ("shift_sells_by_days", "scale_sell_quantities",
             "daily_sell_cap")


def is_sell(order) -> bool:
    return isinstance(order, (list, tuple)) and len(order) >= 1 \
        and order[0] == "SELL"


def _clamp_band(route, band):
    start = max(0, int(band[0] if band else 0))
    end = min(len(route), int(band[1] if band else len(route)))
    return start, end


def _empty_changes(operator, params, band):
    return {
        "operator": operator,
        "params": params,
        "band": list(band) if band else None,
        "steps_touched": [],
        "orders": {"moved": 0, "rescaled": 0, "capped": 0, "dropped": 0},
        "quantity_before": 0,
        "quantity_after": 0,
    }


def _sell_quantity(order) -> int:
    try:
        return max(0, int(order[2]))
    except (IndexError, TypeError, ValueError):
        return 0


def _total_sell_quantity(route):
    return sum(_sell_quantity(o) for step in route for o in step["market"]
               if is_sell(o))


def _shift_sells(route, days, band):
    start, end = _clamp_band(route, band)
    delta = int(days) * STEPS_PER_DAY
    changed = _empty_changes("shift_sells_by_days", {"days": int(days)},
                             (start, end))
    moved = []            # (target_step, source_step, order) 源序
    for t in range(start, end):
        keep = []
        for order in route[t]["market"]:
            if is_sell(order):
                target = min(len(route) - 1, max(0, t + delta))
                moved.append((target, t, copy.deepcopy(order)))
                changed["orders"]["moved"] += 1
            else:
                keep.append(order)
        if len(keep) != len(route[t]["market"]):
            route[t]["market"] = keep
            changed["steps_touched"].append(t)
    # 落点安置：目标步序升序、源步序稳定；槽满在 ±72 步内交错顺延
    # （位移有界、不回卷）；无空槽才弃（守恒破口入账本）。
    moved.sort(key=lambda row: (row[0], row[1]))
    displacement_total = 0
    displacement_max = 0
    for target, source_t, order in moved:
        slot = _find_slot(route, target)
        if slot is None:
            changed["orders"]["dropped"] += 1
            continue
        route[slot]["market"].append(order)
        disp = abs(slot - target)
        displacement_total += disp
        displacement_max = max(displacement_max, disp)
        if slot not in changed["steps_touched"]:
            changed["steps_touched"].append(slot)
    changed["steps_touched"].sort()
    changed["displacement"] = {"total": displacement_total,
                               "max": displacement_max}
    return route, changed


def _find_slot(route, target):
    """target 起在 ±SHIFT_SLACK 步内交错找空槽（+1,−1,+2,−2,…）；无则 None。"""
    n = len(route)
    if len(route[target]["market"]) < MARKET_SLOTS:
        return target
    for slack in range(1, SHIFT_SLACK + 1):
        for cand in (target + slack, target - slack):
            if 0 <= cand < n \
                    and len(route[cand]["market"]) < MARKET_SLOTS:
                return cand
    return None


def _scale_sells(route, ratio, band):
    start, end = _clamp_band(route, band)
    changed = _empty_changes("scale_sell_quantities",
                             {"ratio": float(ratio)}, (start, end))
    for t in range(start, end):
        touched = False
        new_market = []
        for order in route[t]["market"]:
            if is_sell(order) and _sell_quantity(order) > 0:
                q = max(1, int(round(_sell_quantity(order)
                                     * float(ratio))))
                new_order = [order[0], order[1], q] + list(order[3:])
                if new_order != list(order):
                    changed["orders"]["rescaled"] += 1
                    touched = True
                new_market.append(new_order)
            else:
                new_market.append(order)
        if touched:
            route[t]["market"] = new_market
            changed["steps_touched"].append(t)
    return route, changed


def _daily_cap(route, cap, band):
    start, end = _clamp_band(route, band)
    changed = _empty_changes("daily_sell_cap", {"cap": int(cap)},
                             (start, end))
    day_start = (start // STEPS_PER_DAY) * STEPS_PER_DAY
    for day in range(day_start, end, STEPS_PER_DAY):
        lo = max(start, day)
        hi = min(end, day + STEPS_PER_DAY)
        per_item = {}
        for t in range(lo, hi):
            touched = False
            new_market = []
            for order in route[t]["market"]:
                if is_sell(order) and len(order) >= 2:
                    item = str(order[1])
                    used = per_item.get(item, 0)
                    remaining = max(0, int(cap) - used)
                    q = min(_sell_quantity(order), remaining)
                    per_item[item] = used + q
                    if q != _sell_quantity(order):
                        changed["orders"]["capped"] += 1
                        touched = True
                    if q > 0:
                        new_market.append([order[0], order[1], q]
                                          + list(order[3:]))
                else:
                    new_market.append(order)
            if touched:
                route[t]["market"] = new_market
                changed["steps_touched"].append(t)
    return route, changed


def apply_market_edit_operators(payload=None):
    """意图级签名；真值在责任文档。

    payload：{route: [719 步], operator: 名, params: {days|ratio|cap},
    band: [start, end)|None}。
    返回 {route, changes}——route 为深拷贝编辑结果（原route不被串改）；
    changes 含 quantity_before/after 守恒账。未知算子/缺参 fail-closed。
    """
    payload = dict(payload or {})
    route = payload.get("route")
    operator = payload.get("operator")
    if not isinstance(route, list) or not route:
        raise ValueError("apply_market_edit_operators needs a non-empty "
                         "route (fail-closed)")
    if operator not in OPERATORS:
        raise ValueError(f"unknown market edit operator (fail-closed): "
                         f"{operator!r}; known: {OPERATORS}")

    working = copy.deepcopy(route)
    params = dict(payload.get("params") or {})
    band = payload.get("band")
    quantity_before = _total_sell_quantity(route)

    if operator == "shift_sells_by_days":
        if "days" not in params:
            raise ValueError("shift_sells_by_days needs params.days")
        working, changes = _shift_sells(working, params["days"], band)
    elif operator == "scale_sell_quantities":
        if "ratio" not in params:
            raise ValueError("scale_sell_quantities needs params.ratio")
        working, changes = _scale_sells(working, params["ratio"], band)
    else:
        if "cap" not in params:
            raise ValueError("daily_sell_cap needs params.cap")
        working, changes = _daily_cap(working, params["cap"], band)

    changes["quantity_before"] = quantity_before
    changes["quantity_after"] = _total_sell_quantity(working)
    return {"route": working, "changes": changes}
