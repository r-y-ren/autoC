# 件 B 谷底闸门运行时层（纯减法；磁带基座原卖单豁免）
# 双形态：文本内嵌态与 quote_context 同名空间（裸名调用）；独立导入态引模块。
import inspect  # 元数自适应宿主调用（stdlib-only）
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

# 宿主捕获（layer S 先例 _CXD_HOST 同款 last-callable 捕获）：注入态本语句在追加块
# 首部执行——AB 形态下 dayhigh 层在前，globals 最后 callable=_dayhigh_agent（本层宿主，
# 门因此过滤含追加单的最终列表）；B 单形态下=基座尾部 agent。排除 quote_context（共享
# 件非宿主）与双下划线名（PEP 649 模块样板）。独立导入态 → _GG_HOST=None，测试经
# monkeypatch 本模块级 _GG_HOST 注入假宿主。
_gg_last_callable = [
    v for k, v in list(globals().items())
    if callable(v) and k != "quote_context"
    and not (k.startswith("__") and k.endswith("__"))
]
_GG_HOST = _gg_last_callable[-1] if _gg_last_callable else None

# 删除台账（跨步留痕；step==0 复位）。
_GG_REMOVED = []


def gate_added_sells(observation, action, added_marks):
    """谷底闸门：我方层加挂 SELL 逐单判 quote<base_of(item) 即删；磁带原卖单豁免不动；删除台账留痕。错误: 标记缺失→保守视作磁带单=不删

    返回 {"market": 过滤后市场单列表, "removed": 删除台账}。语义固化（纯减法）：
    - 只处理 added_marks（{"item","qty","slot","step"}）对得上的 SELL 单；标记缺失
      （None/空）→零删除；标记 step 非本步/槽位越界/单形对不上/qty 不可解析→该标记
      跳过（保守视作磁带单）；无标记的单一律豁免不动（磁带基座原卖单 Q2 边界）；
    - quote<base_of(item) 才删，且只净扣标记的追加量 qty：整单恰为追加量→整单删除，
      并单（追加量并进磁带单）→只扣追加量保住磁带余量；quote/base 取不到→不删；
    - 删除台账逐条 {"item","qty","slot","step"}（qty=实际删除量，slot=原槽位）；
      多标记按槽位降序处理，删除不移位；零删除返回原 market 对象（零足迹）。
    """
    market = action.get("market") if isinstance(action, dict) else None
    if not isinstance(market, list):
        return {"market": market, "removed": []}
    if not isinstance(added_marks, (list, tuple)) or not added_marks:
        return {"market": market, "removed": []}  # 标记缺失→保守不删
    raw_step = observation.get("step") if isinstance(observation, dict) else None
    if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
        return {"market": market, "removed": []}  # 本步未知→保守不删
    step = int(raw_step)
    ctx = quote_context(observation, None)  # 一次性上下文（本层无跨步状态）
    if (ctx is None or not isinstance(ctx.get("quote"), dict)
            or not isinstance(ctx.get("base"), dict)):
        return {"market": market, "removed": []}
    valid = []
    for mark in added_marks:
        if not isinstance(mark, dict):
            continue
        if mark.get("step") != step:
            continue  # 非本步标记（陈旧槽位）→跳过
        slot, qty, item = mark.get("slot"), mark.get("qty"), mark.get("item")
        if (isinstance(slot, bool) or not isinstance(slot, int)
                or slot < 0 or slot >= len(market)):
            continue
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            continue
        if not isinstance(item, str):
            continue
        valid.append((slot, item, qty))
    if not valid:
        return {"market": market, "removed": []}
    valid.sort(key=lambda t: (-t[0], t[1], -t[2]))  # 槽位降序，删除不移位
    new_market = list(market)
    removed = []
    for slot, item, qty in valid:
        order = new_market[slot]
        if order is None:
            continue  # 该槽已删（同轮重复标记）
        if not (isinstance(order, (list, tuple)) and len(order) >= 3
                and order[0] == "SELL" and order[1] == item):
            continue  # 槽位/单形对不上→保守不删
        raw = order[2]
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            continue  # 保守不删
        if isinstance(raw, float):
            if not raw.is_integer():
                continue
            raw = int(raw)
        if raw <= 0:
            continue  # 无可删量
        quote = ctx["quote"].get(item)
        base = ctx["base"].get(item)
        if quote is None or base is None:
            continue  # 保守不删
        if not (float(quote) < float(base)):
            continue  # quote≥base 不删（谷底才删）
        drop = min(qty, raw)
        rest = raw - drop
        if rest <= 0:
            new_market[slot] = None  # 整单=追加量→整单删除
        else:
            new_market[slot] = ["SELL", item, rest]  # 并单：磁带余量豁免不动
        removed.append({"item": item, "qty": drop, "slot": slot, "step": step})
    if not removed:
        return {"market": market, "removed": []}  # 零删除=原对象零足迹
    return {"market": [o for o in new_market if o is not None],
            "removed": removed}


def _glutgate_agent(observation, configuration=None):
    """运行时包装：捕获宿主末 callable→gate_added_sells 过滤→返回；异常→原动作；step==0 复位"""
    # 元数自适应宿主调用：真宿主 r40 末函数 _route40_agent(observation) 只收 1 参，
    # layer S 链先例宿主收 (observation, configuration) 2 参。inspect.signature().bind
    # 只探不调定形态（探错不会执行宿主体；每次调用都探=同宿主同参恒定形态，且换宿主
    # 即生效）；元数不可判→2 参先例形态。真调用仍在 try 之外（layer S 先例：宿主
    # 自身故障不吞）。
    _host_form2 = True
    try:
        _sig = inspect.signature(_GG_HOST)
        try:
            _sig.bind(observation, configuration)
        except TypeError:
            _sig.bind(observation)  # 1 参形态（r40 真宿主）
            _host_form2 = False
    except Exception:
        _host_form2 = True  # 元数不可判→2 参先例形态
    if _host_form2:
        action = _GG_HOST(observation, configuration)
    else:
        action = _GG_HOST(observation)
    try:
        step = int(observation.get("step", 0))
        if step == 0:
            _GG_REMOVED.clear()  # 复位删除台账
        if not isinstance(action, dict):
            return action
        added = globals().get("_DH_ADDED")  # AB 形态=dayhigh 注册表；B 单形态缺省→保守零删
        res = gate_added_sells(observation, action, added)
        removed = res.get("removed") if isinstance(res, dict) else None
        if not removed:
            return action  # 零删除=同对象零足迹（B 单臂等价面恒等）
        _GG_REMOVED.extend(removed)
        return dict(action, market=res["market"])
    except Exception:
        return action  # 内部异常吞掉回退宿主动作（同对象）
