# 件 A 日内新高变现运行时层（注入候选尾块；fail-open 三道）
# 双形态：文本内嵌态与 quote_context 同名空间（裸名调用）；独立导入态引模块。
try:
    quote_context  # 内嵌态已同名定义在前，直接沿用（不重绑）
except NameError:
    try:
        from quote_context import quote_context
    except Exception:
        try:
            from orderbook_r44.quote_context import quote_context
        except Exception:
            pass

# 宿主捕获（layer S 先例 main.py _CXD_HOST 同款 last-callable 捕获）：注入态本语句在追加块
# 首部执行——globals 最后 callable=基座尾部 agent（本层宿主）。排除 quote_context（共享件
# 在本块之前注入/独立导入态经 import 进入，均非宿主）与双下划线名（PEP 649 __annotate__
# 等模块样板）。独立导入态无可捕获宿主 → _DH_HOST=None，测试经 monkeypatch 本模块级
# _DH_HOST 注入假宿主。
_dh_last_callable = [
    v for k, v in list(globals().items())
    if callable(v) and k != "quote_context"
    and not (k.startswith("__") and k.endswith("__"))
]
_DH_HOST = _dh_last_callable[-1] if _dh_last_callable else None

# 触发品 7 品（WHEAT/FERTILIZER 不在变现面）——固定序遍历，无集合迭代序依赖。
_DH_ITEMS = ("EGG", "MILK", "WOOL", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
# 花费单口径（R27 槽位规则：BUY_SEED/BUY_PRODUCT/BUY_ANIMAL/HIRE/BUY_LAND）。
_DH_SPEND = ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "HIRE", "BUY_LAND")
# 当日新高跟踪器（跨步持久；step==0 复位）。
_DH_TRACKER = {}
# 追加单标记注册表 [{"item","qty","slot","step"}]（step==0 复位；gate_added_sells 消费；
# qty=本层追加量——并单时是并入量而非并后总量，谷底闸门按此量净扣保磁带余量）。
_DH_ADDED = []


def detect_dayhigh(ctx, base_action, tracker):
    """当日严格新高判定（7 品；quote<2 永不触发；父链在卖该品不触发）。输入: quote_context+基座动作+跟踪器 / 输出: 触发品集合 / 错误: 异常→空集

    输出=触发品集合的 {item: 触发价} 映射（plan_dayhigh_sells 的 price×qty 降序需要
    触发价；空集={}）。判据：quote>ctx["day_highs"]（截至上一步的当日最高，严格大于；
    无基线=当日首见不触发）∧ quote≥2 ∧ 父链当前未在卖该品（基座动作 market 里该品
    SELL 单 qty>0；qty 不可解析=保守视作在卖）。跟踪器维护（换日复位+逐品 max fold）
    与 quote_context 同语义幂等。
    """
    try:
        if not isinstance(ctx, dict):
            return {}
        day = ctx.get("day")
        quote = ctx.get("quote")
        highs = ctx.get("day_highs")
        if not isinstance(quote, dict) or not isinstance(highs, dict):
            return {}
        if not isinstance(base_action, dict):
            return {}
        market = base_action.get("market")
        if not isinstance(market, list):
            return {}
        if not isinstance(tracker, dict):
            return {}  # 跟踪器异常→空集（零动作）
        selling, unsure = set(), set()
        for order in market:
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                continue
            if order[0] != "SELL":
                continue
            item, raw = order[1], order[2]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                unsure.add(item)  # 同品 SELL 卖量不可解析=保守视作在卖
                continue
            if isinstance(raw, float):
                if not raw.is_integer():
                    unsure.add(item)
                    continue
                raw = int(raw)
            if raw > 0:
                selling.add(item)
        triggers = {}
        for item in _DH_ITEMS:  # 固定序，无集合迭代序依赖
            price = quote.get(item)
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                continue
            price = float(price)
            if price < 2.0:
                continue  # quote<2 永不触发
            base_high = highs.get(item)
            if base_high is None:
                continue  # 无基线（当日/跟踪首见）→无严格新高可言
            if not price > float(base_high):
                continue  # 严格新高
            if item in selling or item in unsure:
                continue  # 父链在卖该品不触发
            triggers[item] = price
        if isinstance(tracker, dict):
            t_highs = tracker.get("day_highs")
            if not isinstance(t_highs, dict):
                t_highs = {}
                tracker["day_highs"] = t_highs
            if tracker.get("day") != day:
                tracker["day"] = day
                t_highs.clear()  # 换日复位
            for item, price in quote.items():
                if isinstance(price, bool) or not isinstance(price, (int, float)):
                    continue
                price = float(price)
                prev = t_highs.get(item)
                if prev is None or price > prev:
                    t_highs[item] = price
        return triggers
    except Exception:
        return {}  # 跟踪器/结构异常→空集（零动作）


def plan_dayhigh_sells(trigger_items, inventory, market_orders):
    """追加单计划：可卖量=在仓可卖−本步已挂同品卖量；price×qty 降序；并入最早同品 SELL 槽/不能并则置于首个花费单前；10 槽满弃追加。输出: 追加单列表+槽位安排+变更台账 / 错误: 库存不确定→该品零追加

    返回 {"orders","slots","ledger","market"}：orders=追加单（price×qty 降序，只含
    追加量）；slots=逐单在产出 market 列表的最终槽位；ledger=变更台账
    [{"item","qty","slot","merge"}]；market=并入后完整市场单列表。
    规则固化：只卖已有货不新增产量；可卖量=在仓可卖（shed 口径）−本步已挂同品 SELL
    卖量（不可解析=不确定→该品零追加；库存缺品/非整数/负数同）；并入最早同品 SELL
    槽（原单不改对象、产新单）；不能并=插到首个花费单之前（无花费单置表尾）；
    列表已满 10 单时插新→放弃该追加（宁缺勿挤，不挤掉原单），并入不占槽仍可执行。
    """
    base = list(market_orders) if isinstance(market_orders, (list, tuple)) else []
    out = {"orders": [], "slots": [], "ledger": [], "market": list(base)}
    if not isinstance(trigger_items, dict):
        return out
    if not isinstance(inventory, dict):
        return out  # 库存整体不确定→全部零追加

    # 逐品算可卖量（按品名升序处理，结果与触发集迭代序无关）
    plan_rows = []  # (item, price, avail, value)
    for item in sorted(trigger_items.keys()):
        price = trigger_items[item]
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            continue
        price = float(price)
        held = inventory.get(item)
        if isinstance(held, bool) or not isinstance(held, (int, float)):
            continue  # 库存不确定→该品零追加
        if isinstance(held, float):
            if not held.is_integer():
                continue
            held = int(held)
        if held < 0:
            continue  # 库存不确定→该品零追加
        already, unsure = 0, False
        for order in base:
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                continue
            if order[0] != "SELL" or order[1] != item:
                continue
            raw = order[2]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                unsure = True
                break
            if isinstance(raw, float):
                if not raw.is_integer():
                    unsure = True
                    break
                raw = int(raw)
            if raw < 0:
                unsure = True
                break
            already += raw
        if unsure:
            continue  # 本步已挂同品卖量不确定=可卖量不确定→零追加
        avail = held - already  # 可卖量守恒：追加后逐品合计≤在仓可卖
        if avail <= 0:
            continue
        plan_rows.append((item, price, avail, price * avail))
    # price×qty 降序；同值按品名升序（确定性，无集合迭代序依赖）
    plan_rows.sort(key=lambda r: (-r[3], r[0]))

    # 槽位安排：work 元素=[订单对象, 追加下标|None, 并入标记]
    work = [[order, None, False] for order in base]
    for idx, (item, price, avail, value) in enumerate(plan_rows):
        merged = -1
        for i, entry in enumerate(work):
            order = entry[0]
            if (isinstance(order, (list, tuple)) and len(order) >= 3
                    and order[0] == "SELL" and order[1] == item):
                merged = i  # 最早同品 SELL 槽
                break
        if merged >= 0:
            old = work[merged][0]
            work[merged] = [["SELL", item, int(old[2]) + avail], idx, True]
            continue
        if len(work) >= 10:
            continue  # 10 槽满→放弃该追加（不挤原单）
        pos = len(work)
        for i, entry in enumerate(work):
            order = entry[0]
            if (isinstance(order, (list, tuple)) and len(order) >= 1
                    and order[0] in _DH_SPEND):
                pos = i  # 首个花费单之前
                break
        work.insert(pos, [["SELL", item, avail], idx, False])

    market_out = [entry[0] for entry in work]
    slot_of = {}
    for slot, entry in enumerate(work):
        if entry[1] is not None:
            slot_of[entry[1]] = (slot, entry[2])
    orders_out, slots_out, ledger_out = [], [], []
    for idx, (item, price, avail, value) in enumerate(plan_rows):
        if idx not in slot_of:
            continue  # 10 槽满弃追加：不入台账
        slot, merged_flag = slot_of[idx]
        orders_out.append(["SELL", item, avail])
        slots_out.append(slot)
        ledger_out.append({"item": item, "qty": avail, "slot": slot,
                           "merge": merged_flag})
    return {"orders": orders_out, "slots": slots_out,
            "ledger": ledger_out, "market": market_out}


def _dayhigh_agent(observation, configuration=None):
    """运行时包装：捕获宿主末 callable→取基座动作→detect_dayhigh→plan_dayhigh_sells→并入市场单列表+台账；异常→原动作；step==0 复位跟踪器"""
    action = _DH_HOST(observation, configuration)  # 宿主调用在 try 之外（layer S 先例）
    try:
        step = int(observation.get("step", 0))
        if step == 0:
            _DH_TRACKER.clear()
            _DH_ADDED.clear()  # 复位当日新高跟踪器与变更台账
        ctx = quote_context(observation, _DH_TRACKER)  # 裸名调用（内嵌态同名空间）
        if ctx is None:
            return action
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list):
            return action
        triggers = detect_dayhigh(ctx, action, _DH_TRACKER)
        if not triggers:
            return action
        priv = observation.get("private")
        shed = priv.get("shed") if isinstance(priv, dict) else None
        plan = plan_dayhigh_sells(triggers, shed, market)
        if not plan or not plan["orders"]:
            return action
        for rec in plan["ledger"]:
            _DH_ADDED.append({"item": rec["item"], "qty": rec["qty"],
                              "slot": rec["slot"], "step": step})
        return dict(action, market=plan["market"])
    except Exception:
        return action  # 内部异常吞掉回退基座动作（同对象零足迹）
