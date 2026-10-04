# 债务账本式卖提前运行时层（三件套之提前+账本；净量恒等硬不变量）
# 双形态：构建时 quote_context 源码拼接在前同命名空间（裸名调用）；独立导入态引模块。
# 注入形态沿 build_r45 契约：_ADV_HOST_AGENT 由注入块 CAPTURE_SRC 设置，块尾重绑保
# 末函数=_advance_agent；本文件不含 from __future__（注入态非模块首语句，沿 dayhigh 先例）。
import inspect

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

# 宿主捕获（注入态=CAPTURE_SRC 已设常量，守卫"已存在不覆盖"保捕获值；独立导入态补
# None 占位——测试经 monkeypatch 本模块级 _ADV_HOST_AGENT 注入假宿主）。
if "_ADV_HOST_AGENT" not in globals():
    _ADV_HOST_AGENT = None

# ---- 契约常量（k/视界/窗口缺省沿 build_r45 PARAM_DEFAULTS 同口径） ----------
_ADV_K = 4                      # 提前窗（拍）；config 可调（configuration["k"]）
_ADV_WINDOW = (192, 695)        # 动作窗口（含端点）：之外零动作
_ADV_HORIZON_FLOOR = 40         # 视界 clamp(measure_rival_lead()+12, 40, 48)
_ADV_HORIZON_CAP = 48
_ADV_HORIZON_MARGIN = 12
_ADV_MAX_ORDERS = 10            # 市场单槽上限（引擎 MAX_ORDERS 同值）
_ADV_HIST_MAX = 240             # 观测历史环上限（拍数口径足够覆盖近窗）
_ADV_LEAD_WINDOW = 48           # measure_rival_lead 近窗（拍）
_ADV_SEASON_END = 718           # 季末有效动作步（引擎 LAST_ACT_STEP）
_ADV_ROUTE_SWITCH = 648         # 磁带路由换算步（基座 routes[2 if t>=648 else route]）
_ADV_RIVAL_MIN = 2              # 对手卖量事件下界（只记下界口径：≥2 才记事件）
# 账本（跨步持久；step==0 复位）。形状（契约定死）：
# {"debts": [{"item","qty","due_step","advance_step"}], "settled": [...]}；
# 净量恒等=逐品 Σadvance=Σsettled（settled 行 {"item","qty","due_step",
# "advance_step","debt_idx"}，debt_idx 指向 debts 下标=跨步防重复抵扣的闭合标记）。
_ADV_LEDGER = {"debts": [], "settled": []}
_ADV_HISTORY = []               # measure_rival_lead 观测历史窗（逐拍追加 obs+own_sold）
# 城镇商店抽货表（引擎口径；town.unlocked_shops→4 拍/24 拍抽货换算用）
_ADV_SHOP_ITEMS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _advance_agent(observation, configuration=None):
    """运行时包装：逐回合 settle_debts 先结账→select_advanceable→apply_advance_with_debt（门内）→台账；异常→原动作；step==0 复位账本

    fail-safe 沿先例：宿主调用在 try 之外（宿主异常上抛）且**元数自适应**（inspect
    绑定 1 参/2 参调用形态——r40 基座末 callable=_route40_agent(observation) 只收 1
    参，二参硬调会整局崩）；层内任何异常→宿主原动作**原样返回（同一对象）**。
    流程固化：settle_debts 先结账（到 due_step 抵扣防双卖）→ select_advanceable
    选可提前量（谷底闸门 quote≥base 在生成口）→ apply_advance_with_debt 执行+记债
    （记账失败该笔不提前）→ 变更台账（debts/settled 逐笔）。step==0 复位账本+历史。
    计划视图：内嵌态经 globals().get("_IMPL") 读基座磁带（layer S plan_view 做法，
    独立导入态取 None→零提前）；k 经 configuration["k"] 可调（合法才覆写模块缺省）。
    """
    host = globals().get("_ADV_HOST_AGENT")
    arity = 2
    try:
        sig = inspect.signature(host)
        try:
            sig.bind(observation, configuration)
            arity = 2
        except TypeError:
            try:
                sig.bind(observation)
                arity = 1
            except TypeError:
                arity = 2
    except (TypeError, ValueError):
        arity = 2  # 不可 introspect 沿二参先例
    action = host(observation) if arity == 1 else host(observation, configuration)
    global _ADV_K
    try:
        step_raw = observation.get("step") if isinstance(observation, dict) else None
        if isinstance(step_raw, bool) or not isinstance(step_raw, (int, float)):
            return action
        step = int(step_raw)
        if step < 0:
            return action
        if step == 0:
            _ADV_LEDGER.clear()
            _ADV_LEDGER.update({"debts": [], "settled": []})
            del _ADV_HISTORY[:]  # 新局复位账本与观测历史
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list):
            return action
        # k 归一（config 可调：configuration["k"] 合法才覆写；非法保持模块现值）
        cfg_k = configuration.get("k") if isinstance(configuration, dict) else None
        if isinstance(cfg_k, bool):
            cfg_k = None
        if isinstance(cfg_k, (int, float)) and not isinstance(cfg_k, bool):
            if float(cfg_k).is_integer() and int(cfg_k) >= 1:
                _ADV_K = int(cfg_k)
        # 逐拍观测史（own_sold 先记宿主动作卖量，apply 后按终值回填）
        own = {}
        for o in market:
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
                if isinstance(o[1], str) and isinstance(o[2], (int, float)) \
                        and not isinstance(o[2], bool) and float(o[2]).is_integer():
                    own[o[1]] = own.get(o[1], 0) + max(0, int(o[2]))
        rec = dict(observation)
        rec["own_sold"] = own
        _ADV_HISTORY.append(rec)
        del _ADV_HISTORY[:-_ADV_HIST_MAX]
        # ① 先结账（step 经动作内标私有传递；账本异常→不抵扣，settle 内 fail-safe）
        tagged = dict(action)
        tagged["step"] = step
        sres = settle_debts(tagged, _ADV_LEDGER)
        base = sres.get("action") if isinstance(sres, dict) else tagged
        if not isinstance(base, dict):
            base = tagged
        market_changed = base.get("market") is not market
        # ② 计划视图（layer S plan_view 做法内联提取；失败→None→select 空集）
        view = None
        try:
            impl = globals().get("_IMPL")
            ch = getattr(impl, "chassis", None)
            tapes = getattr(ch, "routes", None)
            players = getattr(ch, "players", None)
            if isinstance(tapes, dict) and isinstance(players, dict):
                seat = 0
                try:
                    seat = int(observation.get("player", 0))
                except Exception:
                    seat = 0
                native = players.get(seat) or {}
                route = native.get("route") if isinstance(native, dict) else None
                if route in tapes:
                    view = {}
                    for t in range(step, min(step + _ADV_HORIZON_CAP,
                                             _ADV_SEASON_END + 1)):
                        tape = tapes[_ADV_ROUTE_SWITCH
                                     if _ADV_ROUTE_SWITCH in tapes and
                                     t >= _ADV_ROUTE_SWITCH else route]
                        if isinstance(tape, dict):
                            a = tape.get(t)
                        else:
                            try:
                                a = tape[t] if 0 <= t < len(tape) else None
                            except Exception:
                                a = None
                        if not isinstance(a, dict):
                            continue
                        sells, buys, picks = {}, {}, {}
                        for o in (a.get("market") or []):
                            if not isinstance(o, (list, tuple)) or len(o) < 3:
                                continue
                            if not isinstance(o[1], str):
                                continue
                            if isinstance(o[2], bool) or not isinstance(
                                    o[2], (int, float)) or not float(
                                    o[2]).is_integer():
                                continue
                            n = max(0, int(o[2]))
                            if o[0] == "SELL":
                                sells[o[1]] = sells.get(o[1], 0) + n
                            elif o[0] == "BUY_PRODUCT":
                                buys[o[1]] = buys.get(o[1], 0) + n
                        hands = a.get("hands")
                        if not isinstance(hands, (list, tuple)):
                            hands = []
                        for c in [a.get("farmer") or ["PASS"], *hands]:
                            if isinstance(c, (list, tuple)) and len(c) > 1 \
                                    and c[0] == "PICKUP" and isinstance(c[1], str):
                                picks[c[1]] = picks.get(c[1], 0) + 1
                        ent = {}
                        if sells:
                            ent["sells"] = sells
                        if buys:
                            ent["buy_product"] = buys
                        if picks:
                            ent["pickup"] = picks
                        if ent:
                            view[t] = ent
        except Exception:
            view = None  # 提取失败→None→select 空集（零提前，不弃结账）
        # ③ 选可提前量（条件集+谷底闸门在生成口）→ ④ 执行+记债（失败不提前）
        adv = select_advanceable(observation, view, _ADV_LEDGER)
        ares = apply_advance_with_debt(adv, base, _ADV_LEDGER)
        final = ares.get("action") if isinstance(ares, dict) else base
        if not isinstance(final, dict):
            final = base
        if final.get("market") is not base.get("market"):
            market_changed = True
        # 台账逐笔已在 debts/settled；回填 own_sold=终动作卖量（含提前单）
        own2 = {}
        for o in (final.get("market") or []):
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
                if isinstance(o[1], str) and isinstance(o[2], (int, float)) \
                        and not isinstance(o[2], bool) and float(o[2]).is_integer():
                    own2[o[1]] = own2.get(o[1], 0) + max(0, int(o[2]))
        rec["own_sold"] = own2
        if not market_changed:
            return action  # 零足迹快道：原对象原样返回
        return {k: v for k, v in final.items() if k != "step"}  # 剥私有步标
    except Exception:
        return action  # 内部异常吞掉回退宿主原动作（同对象零足迹）


def select_advanceable(observation, tape_plan_view, ledger):
    """可提前量判定：磁带计划内≤k 拍∧已入仓∧quote≥2∧quote≥base∧非 dawn 拍∧非同拍 BUY_PRODUCT∧非当天 PICKUP 品∧非首计划卖单保护品；视界 clamp(measure_rival_lead()+12,40,48)；窗口 192-695 外零动作。错误: 计划视图解析失败→空集

    返回提前单集=有序列表 [{"item","qty","from_step","to_step"}]（from_step=原定拍
    due_step，to_step=当前拍；(from_step,item) 升序=确定性）。条件集逐条固化：
    - 窗口：step∈[192,695]（含端点），之外零动作；
    - 清晨结算拍 step%24==23 零动作；
    - 提前窗=min(k, 视界)：磁带计划内未来 (step, step+窗] 拍本就要卖的 SELL 量；
      k 缺省 4（模块 _ADV_K，config 可调）；视界=clamp(measure_rival_lead(近窗)+12,
      40, 48)（镜像检测只调视界永不加卖）；
    - 货已入仓：advanceable qty ≤ private.shed[item]（本次调用内逐品累计扣减）；
    - 报价门（谷底闸门）：quote≥2 ∧ quote≥base_of(item)（quote_context 同口径）；
    - 非同拍 BUY_PRODUCT：计划视图当前拍有 BUY_PRODUCT→零动作（整拍门）；
    - 非当天 PICKUP 品：计划视图当天（step//24 日内）有 PICKUP 的品整品排除；
    - 首计划卖单保护：逐品"未来最早计划卖单"受保护不提前，其后卖单才可提前；
    - 已提前净额：可提前量按 ledger debts 里同 (item,due_step) 已记债量净扣。
    tape_plan_view：callable(observation)→视图或 dict 视图（双形态）；视图形状
    {t: {"sells": {item: qty}, "buy_product": {...}, "pickup": {...}}}（t≥当前拍，
    缺键=无）。解析失败（非 dict/条目畸形/视图 None/调用异常）→空集（零动作）。
    """
    try:
        step_raw = observation.get("step") if isinstance(observation, dict) else None
        if isinstance(step_raw, bool) or not isinstance(step_raw, (int, float)):
            return []
        step = int(step_raw)
        if not (_ADV_WINDOW[0] <= step <= _ADV_WINDOW[1]):
            return []  # 窗口 192-695 之外零动作
        if step % 24 == 23:
            return []  # 清晨结算拍不提前
        # k 归一（模块缺省 4；非法回缺省）
        k = _ADV_K
        if isinstance(k, bool) or not isinstance(k, (int, float)) \
                or not float(k).is_integer() or int(k) < 1:
            k = 4
        k = int(k)
        # 视界 clamp(measure_rival_lead()+12, 40, 48)（数据不足 measure 自回 40）
        lead = measure_rival_lead(globals().get("_ADV_HISTORY") or [])
        if isinstance(lead, bool) or not isinstance(lead, (int, float)):
            lead = 40
        horizon = int(lead) + _ADV_HORIZON_MARGIN
        if horizon < _ADV_HORIZON_FLOOR:
            horizon = _ADV_HORIZON_FLOOR
        if horizon > _ADV_HORIZON_CAP:
            horizon = _ADV_HORIZON_CAP
        win = k if k < horizon else horizon
        # 计划视图（callable/dict 双形态；解析失败→空集零动作）
        pv = tape_plan_view
        if callable(pv):
            try:
                pv = pv(observation)
            except Exception:
                return []
        if pv is None:
            return []
        if not isinstance(pv, dict):
            return []
        entries = {}
        for t_raw, ent in list(pv.items()):
            if isinstance(t_raw, bool) or not isinstance(t_raw, (int, float)) \
                    or not float(t_raw).is_integer():
                return []
            t = int(t_raw)
            if not isinstance(ent, dict):
                return []
            parsed_ent = {}
            for key in ("sells", "buy_product", "pickup"):
                blob = ent.get(key)
                if blob is None:
                    continue
                if not isinstance(blob, dict):
                    return []
                clean = {}
                for item, qty in list(blob.items()):
                    if not isinstance(item, str) or not item:
                        return []
                    if isinstance(qty, bool) or not isinstance(qty, (int, float)) \
                            or not float(qty).is_integer() or int(qty) < 0:
                        return []
                    clean[item] = int(qty)
                parsed_ent[key] = clean
            entries[t] = parsed_ent
        # 同拍 BUY_PRODUCT（整拍门）→ 零动作
        if entries.get(step, {}).get("buy_product"):
            return []
        # 当天 PICKUP 品（整品排除）
        day_start = (step // 24) * 24
        day_end = day_start + 23
        picked = set()
        for t, ent in entries.items():
            if day_start <= t <= day_end:
                for item, qty in ent.get("pickup", {}).items():
                    if qty > 0:
                        picked.add(item)
        # 报价上下文（裸名调用；缺件/缺字段→空集零动作）
        ctx = quote_context(observation)
        if not isinstance(ctx, dict):
            return []
        quote = ctx.get("quote")
        base = ctx.get("base")
        if not isinstance(quote, dict) or not isinstance(base, dict):
            return []
        priv = observation.get("private") if isinstance(observation, dict) else None
        shed = priv.get("shed") if isinstance(priv, dict) else None
        if not isinstance(shed, dict):
            return []  # 库存不确定→零动作
        # 已提前净额（同 (item,due_step) 已记债量）
        booked = {}
        if isinstance(ledger, dict) and isinstance(ledger.get("debts"), list):
            for rec in ledger["debts"]:
                if not isinstance(rec, dict):
                    continue
                item = rec.get("item")
                due = rec.get("due_step")
                qty = rec.get("qty")
                if not isinstance(item, str) or not item:
                    continue
                if isinstance(due, bool) or not isinstance(due, (int, float)) \
                        or not float(due).is_integer():
                    continue
                if isinstance(qty, bool) or not isinstance(qty, (int, float)) \
                        or not float(qty).is_integer():
                    continue
                key = (item, int(due))
                booked[key] = booked.get(key, 0) + max(0, int(qty))
        # 逐品判定（品名升序=确定性）
        out = []
        items = set()
        for ent in entries.values():
            items.update(ent.get("sells", {}).keys())
        for item in sorted(items):
            price = quote.get(item)
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                continue
            price = float(price)
            if price < 2.0:
                continue  # quote<2 永不提前
            base_px = base.get(item)
            if isinstance(base_px, bool) or not isinstance(base_px, (int, float)):
                continue
            if price < float(base_px):
                continue  # 谷底闸门：quote≥base 才提前
            if item in picked:
                continue  # 当天 PICKUP 品排除
            held = shed.get(item, 0)
            if isinstance(held, bool) or not isinstance(held, (int, float)):
                continue
            if isinstance(held, float):
                if not held.is_integer():
                    continue
                held = int(held)
            if held < 0:
                continue  # 库存不确定→该品零提前
            # 窗内未来卖单（(step, step+win]）
            future = []
            for t, ent in entries.items():
                if not (step < t <= step + win):
                    continue
                qty = ent.get("sells", {}).get(item, 0)
                if qty > 0:
                    future.append((t, qty))
            future.sort()
            if not future:
                continue
            # 首计划卖单保护：逐品未来最早计划卖单不动
            remaining = int(held)
            for t, qty in future[1:]:
                if remaining <= 0:
                    break
                net = qty - booked.get((item, t), 0)
                if net <= 0:
                    continue  # 该单已提前完
                take = net if net < remaining else remaining
                out.append({"item": item, "qty": int(take),
                            "from_step": t, "to_step": step})
                remaining -= take
        return out
    except Exception:
        return []  # 计划视图/结构异常→空集（零动作）


def apply_advance_with_debt(advance_orders, action, ledger):
    """提前执行+记账：插队首+等额记债到原 due_step（净量恒等）；台账逐笔。错误: 记账失败→该笔不提前

    提前单插当前市场单列表**队首**（first-in-line 先例；多单保 select 给序整体置首）；
    **等额记债**到原 due_step：debts 行 {"item","qty","due_step":from_step,
    "advance_step":to_step}（契约定死四字段）。逐笔原子：先记账后插单，记账失败/
    单畸形/槽满（≤10 槽，宁缺勿挤不挤原单）→该笔不提前不记账。原 action 不改对象
    （产新 dict+新 market 列表；零提前时原对象原样返回）。返回 {"action","ledger",
    "applied","skipped"}（applied/skipped=逐笔台账）。
    """
    applied, skipped = [], []
    orders = list(advance_orders) if isinstance(advance_orders, (list, tuple)) else []
    if not isinstance(ledger, dict) or not isinstance(ledger.get("debts"), list):
        for od in orders:
            skipped.append({"order": od, "reason": "ledger_malformed"})
        return {"action": action, "ledger": ledger, "applied": [],
                "skipped": skipped}  # 账本异常→全部不提前
    if not isinstance(action, dict) or not isinstance(action.get("market"), list):
        for od in orders:
            skipped.append({"order": od, "reason": "action_malformed"})
        return {"action": action, "ledger": ledger, "applied": [],
                "skipped": skipped}
    market = action.get("market")
    head = []
    for od in orders:
        item = od.get("item") if isinstance(od, dict) else None
        qty = od.get("qty") if isinstance(od, dict) else None
        due = od.get("from_step") if isinstance(od, dict) else None
        to = od.get("to_step") if isinstance(od, dict) else None
        bad = (not isinstance(item, str) or not item
               or isinstance(qty, bool) or not isinstance(qty, (int, float))
               or not float(qty).is_integer() or int(qty) <= 0
               or isinstance(due, bool) or not isinstance(due, (int, float))
               or not float(due).is_integer()
               or isinstance(to, bool) or not isinstance(to, (int, float))
               or not float(to).is_integer())
        if bad:
            skipped.append({"order": od, "reason": "malformed"})
            continue
        qty, due, to = int(qty), int(due), int(to)
        if len(market) + len(head) >= _ADV_MAX_ORDERS:
            skipped.append({"order": od, "reason": "no_slot"})
            continue  # 10 槽满→不提前（宁缺勿挤，不挤原单）
        # 先记账（记账失败→该笔不提前）
        try:
            ledger["debts"].append({"item": item, "qty": qty,
                                    "due_step": due, "advance_step": to})
        except Exception:
            skipped.append({"order": od, "reason": "book_failed"})
            continue
        head.append(["SELL", item, qty])
        applied.append({"item": item, "qty": qty, "from_step": due,
                        "to_step": to})
    if not applied:
        return {"action": action, "ledger": ledger, "applied": [],
                "skipped": skipped}  # 零足迹：原对象原样返回
    return {"action": dict(action, market=head + list(market)),
            "ledger": ledger, "applied": applied, "skipped": skipped}


def settle_debts(action, ledger):
    """债务结算：due_step 从该品磁带卖单按债量抵扣（只减不加；债量>单量→清零+溢出告警）；跨步防重复。错误: 账本异常→不抵扣（不双卖优先）

    到期口径：debts 行 due_step≤当前拍（当前拍经 action["step"] 私有步标传入；
    步标缺失/非法→不抵扣）且未闭合者到期。抵扣：对该品 action market 里的磁带 SELL
    单按序**只减不加**；债量>单量→该单清零，剩余量记 settle_overflow 溢出告警。
    跨步防重复抵扣：settled 行带 debt_idx（debts 下标）=闭合标记，闭合债不再抵扣。
    净量恒等口径：settled 行 qty=**实际抵扣量**（健康流 Σadvance=Σsettled；溢出/漏拍
    的短口如实入账=恒等违例可见，judge verify_net_identity 计违例）。原 action 不改
    对象（产新 dict+新 market 列表）。返回 {"action","ledger","settled","warnings"}。
    """
    warnings = []
    step_raw = action.get("step") if isinstance(action, dict) else None
    market = action.get("market") if isinstance(action, dict) else None
    if isinstance(step_raw, bool) or not isinstance(step_raw, (int, float)) \
            or not float(step_raw).is_integer() or not isinstance(market, list):
        return {"action": action, "ledger": ledger, "settled": [],
                "warnings": warnings}  # 步不明/动作异常→不抵扣
    step = int(step_raw)
    if not isinstance(ledger, dict) or not isinstance(ledger.get("debts"), list) \
            or not isinstance(ledger.get("settled"), list):
        warnings.append({"kind": "ledger_malformed"})
        return {"action": action, "ledger": ledger, "settled": [],
                "warnings": warnings}  # 账本异常→不抵扣（宁可不提前也不双卖）
    try:
        closed = set()
        for row in ledger["settled"]:
            if isinstance(row, dict):
                idx = row.get("debt_idx")
                if isinstance(idx, int) and not isinstance(idx, bool):
                    closed.add(idx)
        # 逐债抵扣（debts 插入序=确定性）；同拍多债共享单量需累计
        spent = {}  # market 下标→本调用累计后余量
        rows_added = []
        for idx, debt in enumerate(ledger["debts"]):
            if idx in closed:
                continue  # 跨步台账防重复抵扣
            if not isinstance(debt, dict):
                continue
            item = debt.get("item")
            due = debt.get("due_step")
            qty = debt.get("qty")
            adv_step = debt.get("advance_step")
            if not isinstance(item, str) or not item:
                continue
            if isinstance(due, bool) or not isinstance(due, (int, float)) \
                    or not float(due).is_integer() or int(due) > step:
                continue  # 未到期/畸形不抵扣
            due = int(due)
            if isinstance(qty, bool) or not isinstance(qty, (int, float)) \
                    or not float(qty).is_integer() or int(qty) < 0:
                continue
            if isinstance(adv_step, bool) or not isinstance(adv_step, (int, float)) \
                    or not float(adv_step).is_integer():
                adv_step = None
            else:
                adv_step = int(adv_step)
            remaining = int(qty)
            deducted = 0
            for i, o in enumerate(market):
                if remaining <= 0:
                    break
                if not isinstance(o, (list, tuple)) or len(o) < 3:
                    continue
                if o[0] != "SELL" or o[1] != item:
                    continue
                if isinstance(o[2], bool) or not isinstance(o[2], (int, float)) \
                        or not float(o[2]).is_integer() or int(o[2]) < 0:
                    continue  # 单量不可解析→保守不动该单
                cur = spent.get(i)
                if cur is None:
                    cur = int(o[2])
                take = cur if cur < remaining else remaining
                if take <= 0:
                    continue
                spent[i] = cur - take
                remaining -= take
                deducted += take
            if remaining > 0:
                warnings.append({"kind": "settle_overflow", "item": item,
                                 "due_step": due, "debt_qty": int(qty),
                                 "deducted": deducted, "short": remaining})
            rows_added.append({"item": item, "qty": deducted, "due_step": due,
                               "advance_step": adv_step, "debt_idx": idx})
        if not rows_added:
            return {"action": action, "ledger": ledger, "settled": [],
                    "warnings": warnings}  # 无到期债：零足迹
        if spent:
            new_market = []
            for i, o in enumerate(market):
                if i in spent:
                    new_o = list(o) if isinstance(o, (list, tuple)) else list(o)
                    new_o[2] = spent[i]  # 只减不加；原单不改对象（产新单）
                    new_market.append(new_o)
                else:
                    new_market.append(o)
            action_out = dict(action, market=new_market)
        else:
            action_out = action  # 全部闭合但零抵扣：动作零改动
        ledger["settled"].extend(rows_added)
        return {"action": action_out, "ledger": ledger,
                "settled": rows_added, "warnings": warnings}
    except Exception:
        return {"action": action, "ledger": ledger, "settled": [],
                "warnings": warnings + [{"kind": "settle_error"}]}


def measure_rival_lead(observation_history):
    """对手提前量：公开库存差分反推 rival_sold（删失口径 $1 地板只记下界）；输出近窗最大 lead（拍数）。错误: 数据不足→默认 40

    输入=观测历史窗（obs 列表，逐拍可带 "own_sold" {item: qty}——本层逐拍自记）。
    差分口径（公开库存差分，v9 竞速先例同式）：相邻拍 (prev, curr)（curr.step==
    prev.step+1，断档不补=不填 0）逐品
        rival_sold = inv' − inv + town_draw − own_sold
    其中 town_draw=商店 4 拍抽货（单件店 +2/多件店 +1）+镇心 24 拍 +1（prev 拍口径）。
    **删失口径**：prev 拍报价≤3（$1 地地板带）→成交不入公开库存，该品该拍**跳过不记 0**
    （只记下界：实记值=对手卖量下界，阈 ≥2 才记事件）。lead 口径：逐事件取"我方同品
    下一次实卖拍−对手卖拍"（对手节奏领先我方的拍数），近窗（末 _ADV_LEAD_WINDOW 拍）
    取最大；样本不足/无事件/异常→默认 40。
    """
    try:
        if not isinstance(observation_history, (list, tuple)):
            return 40
        parsed = []
        for entry in observation_history:
            if not isinstance(entry, dict):
                parsed.append(None)  # 断档：相邻配对跳过（不填 0）
                continue
            step_raw = entry.get("step")
            market = entry.get("market")
            if isinstance(step_raw, bool) or not isinstance(step_raw, (int, float)) \
                    or not float(step_raw).is_integer() \
                    or not isinstance(market, dict):
                parsed.append(None)
                continue
            inv = market.get("inventory")
            prices = market.get("prices")
            if not isinstance(inv, dict) or not isinstance(prices, dict):
                parsed.append(None)
                continue
            town = entry.get("town")
            shops = town.get("unlocked_shops") if isinstance(town, dict) else None
            if not isinstance(shops, (list, tuple)):
                parsed.append(None)  # 抽货量不确定→该拍不可用（不填 0）
                continue
            own = entry.get("own_sold")
            if own is None:
                own = {}
            if not isinstance(own, dict):
                parsed.append(None)
                continue
            parsed.append((int(step_raw), inv, prices, list(shops), own))
        if len(parsed) < 2:
            return 40
        # 事件收集：对手卖拍（下界口径 ≥2）与我方实卖拍
        events = []
        own_turns = {}
        for rec in parsed:
            if rec is None:
                continue
            step, inv, prices, shops, own = rec
            for item, qty in own.items():
                if isinstance(item, str) and isinstance(qty, (int, float)) \
                        and not isinstance(qty, bool) and float(qty).is_integer() \
                        and int(qty) > 0:
                    own_turns.setdefault(item, set()).add(step)
        for i in range(len(parsed) - 1):
            prev, curr = parsed[i], parsed[i + 1]
            if prev is None or curr is None:
                continue
            if curr[0] != prev[0] + 1:
                continue  # 断档不补（不填 0）
            p_step, p_inv, p_prices, p_shops, p_own = prev
            c_inv = curr[1]
            # town_draw（prev 拍口径：商店 4 拍抽货+镇心 24 拍抽货）
            draw = {}
            if p_step % 4 == 0:
                for shop in p_shops:
                    items = _ADV_SHOP_ITEMS.get(shop, ())
                    for item in items:
                        draw[item] = draw.get(item, 0) + (
                            2 if len(items) == 1 else 1)
            if p_step % 24 == 0:
                for item in list(c_inv.keys()):
                    draw[item] = draw.get(item, 0) + 1
            for item in sorted(set(p_inv) | set(c_inv)):
                if item not in p_inv or item not in c_inv:
                    continue  # 缺品→不确定不记（不填 0）
                price = p_prices.get(item)
                if isinstance(price, bool) or not isinstance(price, (int, float)):
                    continue
                if float(price) <= 3.0:
                    continue  # $1 地板删失：不入公开库存→跳过不记 0（只记下界）
                pv = p_inv[item]
                cv = c_inv[item]
                if isinstance(pv, bool) or not isinstance(pv, (int, float)) \
                        or isinstance(cv, bool) or not isinstance(cv, (int, float)):
                    continue
                own_q = p_own.get(item, 0)
                if isinstance(own_q, bool) or not isinstance(own_q, (int, float)) \
                        or not float(own_q).is_integer() or int(own_q) < 0:
                    continue  # 我方卖量不确定→不记
                rival = (float(cv) - float(pv)
                         + float(draw.get(item, 0)) - float(int(own_q)))
                if rival >= float(_ADV_RIVAL_MIN):
                    events.append((p_step, item))  # 实记值=对手卖量下界
        if not events or not own_turns:
            return 40
        last = max(r[0] for r in parsed if r is not None)
        cutoff = last - _ADV_LEAD_WINDOW
        best = None
        for t, item in sorted(set(events)):
            if t <= cutoff:
                continue  # 近窗之外不计
            for t_o in sorted(own_turns.get(item, ())):
                if t_o > t:
                    cand = t_o - t
                    if best is None or cand > best:
                        best = cand
                    break
        return int(best) if best is not None else 40
    except Exception:
        return 40
