# ===========================================================================
# 【中文·模块导览】src/market.py —— 市场引擎镜像 + 订单编排（market v1.1 宿主）
# ---------------------------------------------------------------------------
# v10.9 保留件：①产能/吸收模型（_town_daily_demand/_prod_evening_from/
#   _ongoing_evenings_left/_crop_future_value/_buy_pace）；②市场引擎语义
#   镜像（_hire_cost fib 表、_market_price_emb 逐件曲线价、
#   _market_order_priority、plan_market_orders 官方语义预算仿真——
#   committed_spend 的唯一权威账本，MS-1.1）；③曲线数学（_shape_val/
#   _price_at_offset/_offset_from_price 反解/_project_price 投影）；
#   ④卖出三门态 _market_gates + 订单编排 _market_orders（买点已接
#   branch §5.4 三重前置检查：容量/曲线/现金门）。
# market v1.1 落地件（W1 波 + W2 完善波）：
#   §5 买侧两小件（机会性买入 <26 囤 4 天量 + BUY_CHUNK_MAX_UNITS 分批）；
#   §2.2 判据 _sell_plan_item（囤=投影≥现价×HOLD_EDGE 且未争议）+
#     争议线零囤货 _contested_items/_sell_overrides（只增清仓）+ P4 三档；
#   §2.1/2.2 MK-2 黎明卖出计划器 _sell_plan_dawn（影子：供给日历×吸收×
#     投影×EOD 预算×10 单配额→每线量/批/时点/防御姿态；MK-3 接管的门禁
#     =回放对账偏差达标+行为回归+线上，scripts/sell_plan_reconciliation.py）；
#   §3 MK-4 干扰影子 _interference_shadow（v1.1 修偏：R_opp=日历×
#     min(供给,吸收)×投影、对称 R_us 流+rollout 终值入日志、连续
#     INTERFERENCE_CONFIRM_DAYS 天确认、三闸布尔；ARMED=False 恒惰性）；
#   §4.4 防御检测-响应表 _DEFENSE_SHAPE（log 不理会/linear 短持穿越/
#     sq 立即止损，入计划器 defense 字段）。
# 延后项（见 JOURNAL）：运行时门退役（LIQUIDITY_FLOOR/DEAD_PRICE_FLOOR
#   作为纵深保留至三门有线上证据）；Ch0 投影切换（observer OBS-2/V0 门）；
#   MK-3 计划器接管、MK-5 干扰武装（载体+闸消费）。
# ===========================================================================

# 【中文】模块级会话状态（按玩家 id 分键——自对局校验时框架可能把本文件
# 一份实例同时充当两个座位）。时钟倒退 = 新对局开始，各状态字典在访问
# 函数里自动重置。_STATE 跟踪"已确认"的当日买畜步速（订单只是请求，
# 只有点数观测里畜群真的增加才消耗步速——防止被拒单浪费当日配额）。
# Module-level state keyed by player id (the framework may exec one copy of
# this file for both seats in self-play validation episodes).  Tracks the
# per-day animal purchase pace by confirming actual herd-count changes in
# the next observation; orders themselves never consume pace.
_STATE = {}



# 【中文】城镇日吸收量模型：从观测到的已解锁商铺集合推算每件商品每天
# 能被城镇吃掉多少单位。规则（官方引擎常量）：每家商铺每天抽 6 次货，
# 单商品商铺每次抽 2 件、多商品商铺每件 1 件；镇中心每天对每件非肥料
# 商品抽 1 件。零吸收的高级产品没有任何变现机制——只能越囤越多，卖出
# 门控会把它划入止损区而非等回涨（P2 卖出三态判据的来源）。
def _town_daily_demand(unlocked_shops):
    """Daily town absorption per item from the observed shop set (P2).

    Returns {item: units/day}; every non-fertilizer product also gets the
    town-center 1/day draw.  A zero-demand premium product (no shop, no
    center interest beyond the base 1) has NO absorption mechanism: its
    inventory can only grow while anyone produces, so the sell rule treats
    it as cut-loss territory instead of hold-for-recovery.
    """
    demand = {}
    for shop in unlocked_shops or []:
        products = SHOPS.get(shop)
        if not products:
            continue
        mult = 2 if len(products) == 1 else 1
        for item in products:
            demand[item] = demand.get(item, 0) + SHOP_DRAWS_PER_DAY * mult
    for item in BASE_PRICE:
        if item != "FERTILIZER":
            demand[item] = demand.get(item, 0) + CENTER_DRAWS_PER_DAY
    return demand


# 【中文】生产"夜晚"三件套：引擎在每日末刷新时结算产出，day 28 之后的
# 夜晚来不及变现。_prod_evening_from 判断"从今天起是否还有一个生产夜
# 晚落在变现地平线内"（买畜/停喂决策用）；_ongoing_evenings_left 精确
# 计算连续产作物还欠几个夜晚（engine 精确口径，仅供 v7-R 轮作 DIG 触
# 发用）；_crop_future_value 是排名级的剩余终局价值估计（任务价值 v 的
# 主要来源，对连续产作物故意不含 max_yield 封顶——见其英文注释）。
def _prod_evening_from(day, placed_day, first_yield, interval):
    """True when another production EVENING lands in [day, PROD_HORIZON_DAY].

    The engine produces at the end-of-day refresh of day D where
    D+1 = placed + first_yield + k*interval (k >= 0), i.e. the first
    production evening is placed + first_yield - 1; the yield is harvestable
    on D+1, so evenings after day 28 never cash out.
    """
    d0 = placed_day + first_yield - 1
    if d0 >= day:
        next_d = d0
    else:
        step = ((day - d0 + interval - 1) // interval) * interval
        next_d = d0 + step
    return next_d <= PROD_HORIZON_DAY


def _ongoing_evenings_left(crop, tile, day):
    """Engine-exact production evenings an ongoing crop still owes.

    The k-th production lands at the EOD refresh of day
    planted + first_yield - 1 + (k-1)*interval (engine checks
    next_day - planted - first_yield % interval == 0 with a
    production_count <= max_yield cap).  _crop_future_value above is a
    ranking-grade approximation with NO max_yield cap -- it keeps paying
    for finished strawberries to PROD_HORIZON_DAY, which is exactly the
    water/fertilizer waste the v7-R rotation removes; this helper is the
    precise trigger, used only there.
    """
    cd = CROPS[crop]
    planted = _get(tile, "planted_day", day)
    interval = max(1, cd["interval"])
    first_ev = planted + cd["first_yield_day"] - 1
    last_ev = first_ev + (cd["max_yield"] - 1) * interval
    if day > last_ev:
        return 0
    produced = 0
    ev = first_ev
    while ev < day:
        produced += 1
        ev += interval
    return max(0, cd["max_yield"] - produced)


def _crop_future_value(crop, tile, day):
    """Remaining terminal value of one alive PLANT tile (ranking-grade)."""
    cd = CROPS[crop]
    price = BASE_PRICE[crop]
    if cd["ongoing"]:
        # strawberry/tomato: one production evening per interval until the
        # horizon; watered+fertilized evenings pay +2 instead of +1
        d0 = _get(tile, "planted_day", day) + cd["first_yield_day"] - 1
        interval = max(1, cd["interval"])
        probe = d0
        while probe < day:
            probe += interval
        evenings = 0
        while probe <= PROD_HORIZON_DAY:
            evenings += 1
            probe += interval
        return evenings * price * 1.3
    # one-time crop: expected units at harvest * price
    yu = _get(tile, "yield_units", 0)
    age = day - _get(tile, "planted_day", day)
    ws, we = _window(crop)
    window_left = max(0, we - max(age, ws - 1))
    expect = min(cd["max_yield"], yu + 2 * window_left)
    return expect * price


# 【中文】买畜"确认步速"记账：BUY_ANIMAL 只是请求，市场可能因现金/库
# 容不足拒单；_buy_pace 只把后续观测中畜群点数的正增量记为"已确认"，防
# 止被拒的订单白白消耗当日购买配额；_note_buy_order 只登记未确认请求。
# 时钟倒退视为新对局并清零。
def _buy_pace(player, day, hour, herd_total):
    """Return confirmed animal purchases for this day.

    A BUY_ANIMAL order is only a request.  The market may reject it for lack
    of cash or shed capacity, so pace is advanced only by a positive
    herd-count delta observed on a later turn.  A backwards clock denotes a
    new episode.
    """
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour <= st.get("hour", -1):
        _STATE[player] = {"day": day, "hour": hour,
                          "last_herd": herd_total, "confirmed": 0,
                          "pending": 0}
        return 0
    delta = max(0, int(herd_total) - int(st.get("last_herd", herd_total)))
    if delta:
        st["confirmed"] = st.get("confirmed", 0) + delta
        st["pending"] = max(0, st.get("pending", 0) - delta)
    st["hour"] = hour
    st["last_herd"] = herd_total
    return st.get("confirmed", 0)


def _note_buy_order(player, day, hour, n):
    """Record an unconfirmed request without consuming the daily pace."""
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour < st.get("hour", -1):
        st = {"day": day, "hour": hour, "last_herd": 0,
              "confirmed": 0, "pending": 0}
        _STATE[player] = st
    st["hour"] = hour
    st["pending"] = st.get("pending", 0) + max(0, int(n))


def _note_buys(player, day, hour, n):
    """Compatibility shim for callers from the pre-confirmation strategy."""
    _note_buy_order(player, day, hour, n)
def _hire_cost(n_already_today):
    """Engine fib schedule: 1, 1, 2, 3, 5, 8, ... for the (n+1)-th hire."""
    a, b = 1, 1
    for _ in range(max(0, n_already_today)):
        a, b = b, a + b
    return a


# 【中文】市场语义镜像三件套（官方 1.32.7 引擎的逐字节复刻）：
#   _market_price_emb    按嵌入曲线表精确计算"当前库存"下的成交价；
#   _market_order_priority 订单单日优先级（终日只卖 > 买饲料 > 卖货 >
#                          d0 买畜 > 买地 > 雇工 > 买麦种 > 买畜 > 其他）；
#   plan_market_orders   对整张订单队列做官方语义的预算仿真：选前 10
#                          单、逐件按当前曲线价成交、现金/库容/雇工价
#                          全程记账，返回"会被引擎接受"的子集——入口
#                          agent() 用它做最后一道预算截断，确保提交的
#                          订单在真实引擎里逐单可成交。
def _market_price_emb(item, inventory):
    """Exact mirror of official market_price on the embedded curve table.

    Official 1.32.7 (vendored kaggriculture.py): below I0 the price uses the
    below-curve, above I0 the above-curve, floored at 1.  MARKET_PARAMS_EMB
    is pinned to the official table (99/99 spot-check in the r4-P2 notes).
    """
    base, t, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    i0 = MARKET_I0_EMB
    if inventory < i0:
        amp = bt * base / max(_shape_val(bf, t, t), 1e-9)
        return max(PRICE_FLOOR_EMB,
                   int(round(base + amp * _shape_val(bf, i0 - inventory, t))))
    amp = at * base / max(_shape_val(af, t, t), 1e-9)
    return max(PRICE_FLOOR_EMB,
               int(round(base - amp * _shape_val(af, inventory - i0, t))))


def _market_order_priority(order, day):
    """Selection priority only; accepted orders retain engine queue order."""
    if not isinstance(order, list) or not order:
        return -1
    op = order[0]
    item = order[1] if len(order) > 1 else None
    if day >= SEASON_DAYS - 1:
        return 100 if op == "SELL" else -1
    if op == "BUY_PRODUCT" and item == "WHEAT":
        return 95                 # starvation red line
    if op == "SELL":
        return 90                 # liquidity / terminal recovery
    if day == 0 and op == "BUY_ANIMAL":
        return 85                 # opening herd timing
    if op == "BUY_LAND":
        return 80
    if op == "HIRE":
        return 75
    if op == "BUY_SEED" and item == "WHEAT":
        return 70                 # feed rotation floor
    if op == "BUY_ANIMAL":
        return 60
    if op in ("BUY_SEED", "BUY_PRODUCT"):
        return 40
    return -1


def plan_market_orders(orders, money, shed_count, *, day=0, max_orders=10,
                       shed_capacity=100, hires_today=0, hands_count=0,
                       quadrants_owned=1, land_costs=None, prices=None,
                       shed_stock=None, seed_stock=None, market_inventory=None):
    """Select and budget one official-engine-compatible market queue.

    Selection is priority based, but the selected indices stay in their original
    order. Semantics mirror vendored engine 1.32.7 exactly: atomic HIRE/BUY_LAND;
    SELL/BUY_* commit ONE unit per lockstep round with the CURRENT curve price
    (BUY_PRODUCT is quoted at post-buy inventory; SELL revenue rises per unit,
    frees shed capacity and only adds supply above the $1 floor); a failed unit
    ends only its current order, and later queue columns may run.
    """
    max_orders = max(1, int(max_orders))
    ranked = []
    for index, order in enumerate(orders or []):
        priority = _market_order_priority(order, day)
        if priority >= 0:
            ranked.append((-priority, index))
    chosen = {index for _priority, index in sorted(ranked)[:max_orders]}
    selected = [(index, order) for index, order in enumerate(orders or [])
                if index in chosen]

    wallet = float(money)
    occupied = max(0, int(shed_count))
    hire_index = max(0, int(hires_today))
    land_index = max(0, int(quadrants_owned) - 1)
    land_costs = list(land_costs or (1000, 2000, 4000))
    prices = prices or {}
    stock_supplied = shed_stock is not None
    stock = {item: 0 for item in tuple(BASE_PRICE) + tuple(ANIMALS)}
    stock.update(shed_stock or {})
    seeds = {crop: 0 for crop in CROPS}
    seeds.update(seed_stock or {})
    inv = {item: MARKET_I0_EMB for item in BASE_PRICE}
    for item, value in (market_inventory or {}).items():
        if item in inv:
            inv[item] = int(value)
    accepted = []
    details = []
    spend = 0.0
    revenue = 0.0

    for index, order in selected:
        op = order[0]
        if op == "HIRE":
            cost = _hire_cost(hire_index)
            if wallet >= cost:
                wallet -= cost
                spend += cost
                hire_index += 1
                accepted.append(["HIRE"])
                details.append({"index": index, "order": list(order),
                                "filled": 1, "abort": None})
            else:
                details.append({"index": index, "order": list(order),
                                "filled": 0, "abort": "no_money"})
            continue
        if op == "BUY_LAND":
            cost = land_costs[land_index] if land_index < len(land_costs) else None
            if cost is None:
                details.append({"index": index, "order": list(order),
                                "filled": 0, "abort": "no_land"})
            elif wallet < cost:
                details.append({"index": index, "order": list(order),
                                "filled": 0, "abort": "no_money"})
            else:
                wallet -= cost
                spend += cost
                land_index += 1
                accepted.append(["BUY_LAND"])
                details.append({"index": index, "order": list(order),
                                "filled": 1, "abort": None})
            continue
        if op == "SELL":
            if len(order) < 3 or order[1] not in BASE_PRICE or \
                    not isinstance(order[2], (int, float)) or order[2] <= 0:
                continue
            item = order[1]
            available = stock.get(item, 0) if stock_supplied else int(order[2])
            filled = 0
            abort = None
            for _ in range(int(order[2])):
                if filled >= available:
                    abort = "no_stock"
                    break
                price = _market_price_emb(item, inv[item])
                wallet += price
                revenue += price
                filled += 1
                occupied = max(0, occupied - 1)
                stock[item] = stock.get(item, available) - 1
                if price > PRICE_FLOOR_EMB:
                    inv[item] += 1   # sales above $1 add market supply
            if filled > 0:
                accepted.append(["SELL", item, filled])
            details.append({"index": index, "order": list(order),
                            "filled": filled, "abort": abort})
            continue
        if op not in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL") or len(order) < 3:
            continue
        try:
            requested = int(order[2])
        except (TypeError, ValueError):
            continue
        if requested <= 0:
            continue
        item = order[1]
        if op == "BUY_SEED":
            unit_cost = CROPS.get(item, {}).get("seed")
            uses_shed = False
        elif op == "BUY_ANIMAL":
            unit_cost = ANIMALS.get(item, {}).get("cost")
            uses_shed = True
        else:
            if item not in ("WHEAT", "FERTILIZER"):
                continue
            unit_cost = None   # BUY_PRODUCT reprices every unit (official)
            uses_shed = True
        if op != "BUY_PRODUCT" and \
                (not isinstance(unit_cost, (int, float)) or unit_cost <= 0):
            continue
        filled = 0
        abort = None
        for _ in range(requested):
            if uses_shed and occupied >= shed_capacity:
                abort = "shed_full"
                break
            price = unit_cost if op != "BUY_PRODUCT" else \
                _market_price_emb(item, inv[item] - 1)  # post-buy quote
            if wallet < price:
                abort = "no_money"
                break
            wallet -= price
            spend += price
            filled += 1
            if uses_shed:
                occupied += 1
                stock[item] = stock.get(item, 0) + 1
            if op == "BUY_SEED":
                seeds[item] = seeds.get(item, 0) + 1
            if op == "BUY_PRODUCT":
                inv[item] -= 1

        if filled > 0:
            accepted.append([op, item, filled])
        details.append({"index": index, "order": list(order),
                        "filled": filled, "abort": abort})

    return {"accepted": accepted, "orders": details,
            "committed_spend": spend, "revenue": revenue,
            "remaining_money": wallet,
            "shed_count": occupied, "shed_stock": stock,
            "seed_stock": seeds,
            "hands_count": int(hands_count) + hire_index - max(0, int(hires_today)),
            "quadrants_owned": land_index + 1,
            "remaining_capacity": max(0, int(shed_capacity) - occupied),
            "market_inventory": inv,
            "truncated": len(selected) < len(orders or [])}


def buy_product_cost(item, qty, market_inventory=None):
    """Engine-exact BUY_PRODUCT cost for qty units (market §1.1, MS-1.1).

    The official semantics reprices EVERY unit at the post-buy inventory
    (plan_market_orders's per-unit loop): buying draws market inventory
    down unit by unit, so the price walks along the embedded curve.  This
    helper is the single source of that cost model -- the generation-side
    committed-spend ledger in _market_orders consumes it instead of a flat
    spot-price guess, keeping both ledgers in agreement by construction.
    """
    if item not in ("WHEAT", "FERTILIZER"):
        return 0.0
    inv = MARKET_I0_EMB
    if market_inventory is not None:
        try:
            inv = int(market_inventory.get(item, MARKET_I0_EMB))
        except (AttributeError, TypeError, ValueError):
            inv = MARKET_I0_EMB
    total = 0.0
    for _ in range(max(0, int(qty))):
        total += _market_price_emb(item, inv - 1)
        inv -= 1
    return total


def _affordable_buy_units(item, budget, obs, inventory_offset=0):
    """Per-unit affordable count under the engine-exact BUY_PRODUCT curve
    (MS-1.1): the same cumulative walk plan_market_orders performs, used at
    generation time so the queue's wallet view matches the simulator."""
    if budget <= 0:
        return 0
    inv = MARKET_I0_EMB
    market_inventory = _get(_get(obs, "market", {}) or {}, "inventory",
                            None)
    if market_inventory is not None:
        try:
            inv = int(market_inventory.get(item, MARKET_I0_EMB))
        except (AttributeError, TypeError, ValueError):
            inv = MARKET_I0_EMB
    inv -= max(0, int(inventory_offset))
    spend = 0.0
    units = 0
    while units < BUY_CHUNK_MAX_UNITS * 2:
        price = _market_price_emb(item, inv - 1)
        if spend + price > budget:
            break
        spend += price
        units += 1
        inv -= 1
    return units


# 【中文】牛奶逐日持有门槛（选择性干预）：基准 105——在双方都挤奶的
# 联合奶市里囤更高的价带只会把销售推迟成终盘压力倾销（实测变现 ~60/
# 件），日清 ≥105 完胜；赛季末段门槛递减（28 日 80）——第 29 天全场
# 清算地板价在等着所有人，低但为正的门槛优于囤进联合倾销。
def _milk_gate(day):
    """Milk hold-threshold by day (selective intervention, see _market_gates).

    Base 105: in a joint-dairy market (both players milking ~20+/day vs
    town consumption of ~5/day, measured mirror prices 97-135) holding for
    higher bands just deferred sales into eventual pressure dumps (measured
    realized ~60/unit).  Clearing daily at >= 105 dominates.  Decay
    late-season: the day-29 liquidation floor is coming for everyone, so
    clearing inventory at a lower-but-positive gate beats holding into the
    joint dump.
    """
    if day >= 28:
        return 80
    if day >= 26:
        return 90
    if day >= 24:
        return 100
    return 105


# 【中文】可选 LLM 顾问钩子：默认 None（关闭）时直接返回启发式门槛。
# 仅用于本地 A/B 实验（scripts/run_llm_ab.py）；任何失败/离谱回答都回
# 退启发式，绝不阻塞回合（合规的 Reasonableness Standard 由提供方自
# 律限流）。
def _llm_sell_gate(item, price, base_gate, context):
    """Optional LLM consultation for premium sell timing; default heuristic.

    The provider (if any) must answer with {"gate": int}. Any failure or
    absurd answer falls back to the heuristic gate. Never blocks the turn:
    providers are expected to enforce their own call budget/timeout
    (Reasonableness Standard).
    """
    if LLM_PROVIDER is None:
        return base_gate
    try:
        ans = LLM_PROVIDER.suggest(
            f"Item {item} trades at {price} (base {BASE_PRICE[item]}). "
            f"Return the minimum price we should accept for selling into a "
            f"glut-crashing market, as JSON {{\"gate\": int}}.", context)
        gate = int(_get(ans or {}, "gate", base_gate))
        if 1 <= gate <= BASE_PRICE[item] * 2:
            return gate
    except Exception:
        pass
    return base_gate


def _shape_val(func, x, T):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return x ** 0.5
    if func == "log":
        return math.log(1.0 + x)
    if func == "hinge":
        u = x / T if T and T > 0 else x
        return u + HINGE_GAIN_EMB * max(0.0, u - 1.0) ** 2
    return x


def _price_at_offset(item, off):
    """Engine price for inventory I0+off (off signed, glut positive)."""
    base, T, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    if off < 0:
        amp = bt * base / max(_shape_val(bf, T, T), 1e-9)
        p = base + amp * _shape_val(bf, -off, T)
    else:
        amp = at * base / max(_shape_val(af, T, T), 1e-9)
        p = base - amp * _shape_val(af, off, T)
    return max(float(PRICE_FLOOR_EMB), p)


def _offset_from_price(item, price):
    """Inverse of _price_at_offset (ranking-grade; hinge linearized)."""
    base, T, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    price = float(price)
    if price >= base:
        amp = bt * base / max(_shape_val(bf, T, T), 1e-9)
        y = max(0.0, (price - base) / max(amp, 1e-9))
        if bf == "linear":
            return -y
        if bf == "sqrt":
            return -(y * y)
        if bf == "log":
            return -math.expm1(min(y, 50.0))
        if bf == "sq":
            return -(y ** 0.5)
        # hinge: u + 8*(u-1)^2 = y (u = x/T); closed form past the knee
        if y <= 1.0:
            return -(y * T)
        u = (15.0 + math.sqrt(max(0.0, 32.0 * y - 31.0))) / 16.0
        return -(u * T)
    amp = at * base / max(_shape_val(af, T, T), 1e-9)
    y = max(0.0, (base - price) / max(amp, 1e-9))
    if af == "linear":
        return y
    if af == "sqrt":
        return y * y
    if af == "log":
        return math.expm1(min(y, 50.0))
    if af == "sq":
        return y ** 0.5
    return min(y, T)


def _project_price(item, price_now, flow, horizon):
    """Analytic E[R_future]: price at I0 + off + flow*horizon."""
    off = _offset_from_price(item, price_now)
    return _price_at_offset(item, off + flow * horizon)


# 【中文】═══ 选择性干预卖出门控（市场层核心）═══
# 每回合回答"现在卖什么、卖多少"，逐商品三态规则：
#   ① 强需求（有商铺在抽货）且价在门槛下 → 囤到门槛价再卖（城镇吸收
#      会让曲线均值回归；实测毛线店开抽时羊毛整季 240+）；
#   ② 零吸收（只剩镇中心 1/天）且观测到过剩流 → 止损出清，绝不把死
#      曲线扛到第 29 天清算地板价；
#   ③ 流动性/库容压力 → 0.5-0.6×base 的小批折价 tranche。
# r4-P2 升级：①倾销限速 cap() = 城镇吸收的 2×D+4（卖穿吸收只会砸崩
# 自己的下一批）；②解析投影 _project_price 参与止损判定。
# 决策框架：SELL <=> R_now ≥ E[R_future] - C_overflow - C_liquidity
#           - C_terminal（四项分别为：溢出成本/流动性成本/终局清算折价）。
# 各商品门槛/批量与曲线形状的对应关系见下方英文注释（原始证据）。
def _market_gates(day, prices, shed, herd, town_shops=None, money=None,
                  flow=None):
    """Selective-intervention sell decisions: what to SELL this turn, with
    the hoard / release / defend rule per item made explicit.

    r4-P2 upgrades (active when town_shops is provided -- the legacy
    4-argument call keeps the r3 semantics for the pinned tests):
      * DUMP-RATE LIMIT: every tranche is capped near the town's observed
        absorption (2*D + 4) -- selling far beyond what the shops redraw
        only crashes our own next tranche (P0 slippage -10.6..-35.9/u).
      * THREE-MODE rule per item:
          demand strong (shop draws) + price at/below gate -> HOLD for the
          gate (town absorption mean-reverts the curve; measured wool 240+
          all season whenever yarn stores draw);
          zero absorption (center 1/day only) + glut flow observed ->
          CUT-LOSS at max(0.35*base, low gate) instead of riding a dead
          curve into the day-29 floor;
          liquidity/overflow pressure -> small tranches at 0.5-0.6*base
          (C_liquidity/C_overflow in the SELL <=> R_now >= E[R_future]
          - costs rule).
      * ANALYTIC PROJECTION: E[R_future] from the embedded MARKET_PARAMS
        curves and the observed net-flow EMA (_market_flow).

    Curve rationale (official MARKET_PARAMS):
      * MILK base 160, LINEAR glut (T=122): hoard below _milk_gate, clear
        through at the band, big tranche at peaks, halve inside the band,
        drain before the 100-slot discard cliff (m2b logic, kept verbatim).
      * WOOL base 200, SQ glut (T=105: ~56 units above equilibrium reach
        the $1 floor -- the fastest crasher): realize in size at real bids
        (12 at 200+, 8 at the gate, 6 at 100+), CUT LOSSES down to a small
        buffer at WOOL_CUT_LOSS once the curve is dying (measured: yarn-
        store draws decide the whole wool market), dump tranches from
        day 26 (FM-O4).
      * STRAWBERRY base 120, LINEAR glut (T=100): gate 105, tranche 8,
        bounded hoard, endgame dump (the near-band premium: their held
        medians 221-250 come from hoarding, not from dumping daily).
      * MELON base 250, SQ glut (T=300): gate 180, tranche 8 -- realize
        BEFORE the volume farmers' 100+ unit flow floors the curve (the
        m1 engine's melon branch died holding for 250; cap stays 9 tiles
        because a 12-tile plan measurably crashed our own price).
      * CARROT base 35, SQRT glut (T=450, hinge below -- town spikes it
        when scarce): gate 28, generous tranche 15.
      * EGG base 50, LOG glut (crash-tolerant like wheat): gate 40,
        tranche 10.
      * FERTILIZER base 100, linear both sides, no town consumption (m2b):
        bounded hoard, gated release, unconditional from day 25.
      * WHEAT base 25, LOG glut: sell the surplus above the feed reserve
        from WHEAT_SELL_GATE (a real bid, not the floor).
    Returns a list of ["SELL", item, qty] market orders.
    """
    orders = []
    last_day = day >= SEASON_DAYS - 1
    endgame = day >= ENDGAME_DAY
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    demand = _town_daily_demand(town_shops) if town_shops is not None else None
    flow = flow or {}

    # V-T6 bankruptcy lifeline: a broke dawn cannot re-hire the crew that
    # earns it back (crash forensics ep 104594916: 12 hands -> 0 on d10 and
    # a 17-day stall while 8 wool sat in the shed behind shut gates).  Below
    # the emergency floor every tradable shed item dumps unconditionally --
    # hoard gates must never sit on the payroll.
    if money is not None and money < 200 and not last_day:
        for item in BASE_PRICE:
            n = shed.get(item, 0)
            if isinstance(n, (int, float)) and n > 0:
                orders.append(["SELL", item, int(n)])
        return orders

    def cap(qty, item):
        """Dump-rate limiter: town absorption 2*D + 4 (P2)."""
        if demand is None:
            return qty
        return max(4, min(qty, 2 * demand.get(item, 1) + 4))

    if last_day:
        # day 29: only bank money counts; liquidate every tradable shed item
        for item in BASE_PRICE:
            n = shed.get(item, 0)
            if isinstance(n, (int, float)) and n > 0:
                orders.append(["SELL", item, n])
        return orders

    # ---- MILK: hoard / release / defend (m2b, verbatim + P2 caps) --------
    milk = shed.get("MILK", 0)
    if milk > 0:
        gate = _llm_sell_gate("MILK", prices.get("MILK", BASE_PRICE["MILK"]),
                              _milk_gate(day), {"day": day, "shed": milk,
                                                "herd": herd})
        p = prices.get("MILK", BASE_PRICE["MILK"])
        if shed_count >= 70 and p >= 30:
            sell = max(0, milk - 15)
            if sell > 0:
                orders.append(["SELL", "MILK", cap(sell, "MILK")])
        elif p >= 145:
            orders.append(["SELL", "MILK", cap(min(milk, 24), "MILK")])
        elif p >= gate:
            orders.append(["SELL", "MILK", cap(min(milk, 20), "MILK")])
        elif demand is not None and money is not None and money < 1200 \
                and p >= 0.5 * BASE_PRICE["MILK"]:
            # C_liquidity: a broke dawn cannot hire the crew that earns it
            # back -- milk clears at a soft band when cash-starved
            orders.append(["SELL", "MILK", cap(min(milk, 6), "MILK")])

    # ---- WOOL: sq glut (T=105) -- follow the curve, never ride it down ---
    # Sheep flow (ours + the opponent's, 9-12 head across the pool) exceeds
    # base town consumption in most draws: wool either stays scarce (yarn
    # stores drawn -- observed 240+ all season) or floors (+56 units above
    # equilibrium is already $5).  P2: with a yarn store absorbing, the
    # 100-149 band HOLDS for the gate; with zero absorption the analytic
    # cut-loss fires as soon as the flow says the curve is dying.
    wool = shed.get("WOOL", 0)
    if isinstance(wool, (int, float)) and wool > 0:
        p = prices.get("WOOL", BASE_PRICE["WOOL"])
        yarn = demand is None or demand.get("WOOL", 1) >= 12
        if endgame or day >= 26:
            orders.append(["SELL", "WOOL", cap(min(wool, 12), "WOOL")])
        elif shed_count >= 78 and p >= 5:
            orders.append(["SELL", "WOOL", max(0, wool - 10)])
        elif wool > WOOL_HOARD_FLOOR:
            if p >= 200:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 12), "WOOL")])
            elif p >= WOOL_GATE:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 8), "WOOL")])
            elif p >= 100 and not yarn:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 6), "WOOL")])
            elif p >= WOOL_CUT_LOSS and (day >= 18 or wool > WOOL_HOARD_CAP):
                orders.append(["SELL", "WOOL", cap(min(wool - 4, 8), "WOOL")])
            elif demand is not None and not yarn and p >= 70 \
                    and _project_price("WOOL", p, flow.get("WOOL", 0.0), 7) < p:
                # zero absorption + dying curve: realize before the sq
                # cliff does it for us
                orders.append(["SELL", "WOOL", cap(min(wool - 4, 6), "WOOL")])

    # ---- premium rotation/herd goods: gated tranches + hoard bounds ------
    def premium(item, gate, tranche, hoard_floor, hoard_cap, low_gate,
                endgame_tranche):
        held = shed.get(item, 0)
        if not isinstance(held, (int, float)) or held <= hoard_floor:
            return
        p = prices.get(item, BASE_PRICE[item])
        if endgame:
            orders.append(["SELL", item, min(held, endgame_tranche)])
        elif shed_count >= 78 and p >= 5:
            # discard-cliff guard shared with milk
            orders.append(["SELL", item, max(0, held - 10)])
        elif p >= gate + 30:
            orders.append(["SELL", item, cap(min(held - hoard_floor,
                                                 tranche * 2), item)])
        elif p >= gate:
            orders.append(["SELL", item, cap(min(held - hoard_floor,
                                                 tranche), item)])
        elif held > hoard_cap and p >= low_gate:
            orders.append(["SELL", item, cap(min(held - hoard_cap,
                                                 tranche), item)])
        elif demand is not None:
            proj3 = _project_price(item, p, flow.get(item, 0.0), 3)
            if demand.get(item, 1) <= 1 and flow.get(item, 0.0) > 0 \
                    and proj3 < 0.9 * p and p >= low_gate:
                # zero absorption + measured glut: cut before the curve
                orders.append(["SELL", item,
                               cap(min(held - hoard_floor,
                                       max(4, tranche // 2)), item)])
            elif money is not None and money < 1200 \
                    and p >= 0.55 * BASE_PRICE[item]:
                orders.append(["SELL", item, cap(min(held - hoard_floor, 6),
                                                 item)])

    # v10 M-D: tranche 8 starved the premium band -- 4 town shops absorb
    # ~24u/day and the observed top-meta band sells 30-69u/day while still
    # realizing 175-206; the P2 cap() bound (2*D+4) still applies on top.
    premium("STRAWBERRY", STRAWBERRY_GATE, 16, STRAWBERRY_HOARD_FLOOR, 26,
            70, 12)
    premium("MELON", MELON_GATE, 8, MELON_HOARD_FLOOR, 14, 120, 8)
    premium("CARROT", CARROT_GATE, 15, CARROT_HOARD_FLOOR, 30, 22, 20)
    premium("EGG", EGG_GATE, 10, EGG_HOARD_FLOOR, 16, 30, 12)

    # ---- FERTILIZER: bounded hoard, gated release (m2b) ------------------
    # (v10 M-C continuous-monetization trial REVERTED: it sold the marginal
    # fertilizer the fields convert into strawberry/wheat units, collapsing
    # the dev paired net from +84k to +11.8k.  Manure monetization must
    # come from MORE COLLECTION, not from stripping the field reserve.)
    fert = shed.get("FERTILIZER", 0)
    if fert > 0:
        if day >= 25:
            orders.append(["SELL", "FERTILIZER", fert])
        elif fert > FERT_STOCK_CAP:
            orders.append(["SELL", "FERTILIZER", max(0, fert - FERT_FIELD_RESERVE)])
        elif prices.get("FERTILIZER", BASE_PRICE["FERTILIZER"]) >= FERT_GATE:
            sell = max(0, fert - FERT_FIELD_RESERVE)
            if sell > 0:
                orders.append(["SELL", "FERTILIZER", sell])
    return orders


# 【中文】═══ 市场订单编排（本回合买什么、卖什么）═══
# 下单顺序即优先级链：① 买地（NE d4+/SW d7+，保护基金互锁畜群；SW
# 过 d18 不再买——草莓窗已关、旧栏已满，2000 只会买成流动性）；VOLUME
# 的 SE(d10-14)；② 饲料安全垫（系统麦 < 待喂+3 就外购，护栏价 36、
# 饥饿止损价 85；affordability 门控防"钱=8 仍连发 24 回合废单"）；
# ③ 种子（小麦底仓优先；v9.2 维护门：麦价 ≥30 时在 d8-14 衰减窗内
# 补种；草莓不排在买地基金后面——d5 种下 d15 起每件 ~200 回报）；
# ④ 畜群（d0 爆发 2C+2S；此后"资金门 + 确认步速 + 物种死价冻结 +
# NPV 吸收上限"四重门，按相对缺口交错物种让牛赶上 d8 高价奶窗）；
# ⑤ 卖单（_market_gates 三态门控 + 小麦余量在真实出价 ≥26 时出清，
# 现金 <1000 的现金流回退允许 ≥20 就卖——门槛绝不能饿死资本计划）。
# v10 M-E 贯穿全程：committed_spend 同回合花费台账，让后面的门读到
# "引擎视角"的钱包（防一回合地+畜+种三连掏空）。
# ===========================================================================
# 【中文】market_strategy v1.1 落地块（2026-09-02）
# ---------------------------------------------------------------------------
# _sell_overrides：门控输出之上的有界覆盖（branch §7.2 争议线零囤货 +
#   market §2 卖出计划强制清 + §P4 三档抢跑）——只增清仓单、绝不抑制
#   门控已有的卖出；tranche 一律受 dump-rate 限速（2D+4，卖穿吸收只会
#   砸自己的下一批）。
# _sell_plan_item：囤 vs 清的一般判据（§2.2 规则 1）——囤的条件 =
#   投影价 ≥ 现价×SELL_PLAN_HOLD_EDGE 且线未争议；曲线在死（投影<现价）
#   或利润边际不足 → 清。
# _interference_shadow：干扰触发器影子（MK-4，INTERFENCE_ARMED=False 恒
#   只记录）——R_opp vs R_us 用双方公开日历 × 现价的 7 日窗口粗估。
# ===========================================================================
_INTERFERENCE_LOG = []


def _sell_plan_item(item, day, prices, flow, contested):
    """Sell-planner verdict per item: 'hold' | 'clear' (market §2.2)."""
    if item in (contested or set()):
        return "clear"
    price = _get(prices, item, BASE_PRICE.get(item, 0))
    if price <= 1:
        return "clear"          # floor segment: nothing to wait for
    f = (flow or {}).get(item, 0.0)
    # DTSP 惰性旋钮（P2.5，缺口 1）：卖出折扣系数——悲观成交裕度直接乘在
    # 曲线投影上（<1 更早清、>1 更愿囤）；旗关恒 1.0，判据与 v13.8 同值。
    proj = _project_price(item, price, f, SELL_PLAN_LOOKAHEAD_DAYS) \
        * _plan_knob("sell_price_discount", 1.0)
    if proj < price:
        return "clear"          # curve dying (projection below spot)
    if proj < price * SELL_PLAN_HOLD_EDGE:
        return "clear"          # hold-edge fails: carry risk unpaid
    return "hold"


def _contested_items(obs):
    """Contested lines from PUBLIC tiles (branch §7.2: opp crop tiles >=12;
    dairy lines contested at opp species >=8)."""
    farms = _get(obs, "farms", []) or []
    player = _get(obs, "player", 0)
    opp = None
    for i, f in enumerate(farms):
        if i != player:
            opp = f
            break
    contested = set()
    if opp is None:
        return contested
    counts = {"STRAWBERRY": 0, "WHEAT": 0, "MELON": 0, "CARROT": 0}
    cows = sheep = 0
    for row in _get(opp, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop in counts:
                    counts[crop] += 1
            elif "animal" in tile:
                a = _get(tile, "animal", "")
                if a == "COW":
                    cows += 1
                elif a == "SHEEP":
                    sheep += 1
    for crop, n in counts.items():
        if n >= 12:
            contested.add(crop)
    if cows >= 8:
        contested.add("MILK")
    if sheep >= 8:
        contested.add("WOOL")
    return contested


def _p4_clear_tier(item, player, plan=None):
    """Return the frozen d22 tier, or a live compatibility fallback."""
    # DTSP 惰性旋钮（P2.5，缺口 6 P4 出清档）：计划可强制三档之一——
    # 这是计划指令（非观测估计），越过 est_opp_conf 置信门；旗关恒 ""
    # 走原 d22 快照/实时估计路径。
    forced = _plan_knob("p4_force_tier", "")
    if forced in ("low", "mid", "heavy"):
        return forced
    snapshot = (plan or {}).get("p4_snapshot") or {}
    tiers = snapshot.get("tiers") or {}
    if item in tiers:
        return tiers[item]
    try:
        if est_opp_conf(item, player=player) < 0.5:
            return None
        held = est_opp_held(item, player=player)
    except Exception:
        return None
    if held is None:
        return None
    if held >= P4_HEAVY_HELD:
        return "heavy"
    if held >= P4_MID_HELD:
        return "mid"
    return "low"


def _p4_should_clear(item, day, player, plan=None):
    if not 25 <= day < ENDGAME_DAY:
        return False
    tier = _p4_clear_tier(item, player, plan)
    return tier == "heavy" or (tier == "mid" and day >= 26)


def _sell_overrides(obs, farm, private, day, prices, shed, town_shops,
                    existing_orders, plan=None):
    """Bounded overrides ON TOP of the gate output (never suppress sells)."""
    try:
        if day >= SEASON_DAYS - 1:
            return []           # d29 liquidation owns everything
        demand = _town_daily_demand(town_shops)
        player = _get(obs, "player", 0)
        contested = _contested_items(obs)
        flow = _market_flow(player, day, prices)
        dawn_lines = ((sell_plan_shadow(player) or {}).get("lines") or {})
        shed_count = sum(v for v in shed.values()
                         if isinstance(v, (int, float)) and v > 0)
        emergency = shed_count >= 78 or _get(farm, "money", 0) < 200
        sold_now = {o[1] for o in existing_orders
                    if isinstance(o, list) and o and o[0] == "SELL"}
        out = []

        # DTSP 惰性旋钮（P2.5，缺口 1 批量杠杆）：卖出批量 = 公式 ×
        # 批量乘数（HEAVY 出清档放大、LOW 收缩）；旗关恒 1.0 与 v13.8
        # 逐字节同值。
        _batch_mult = float(_plan_knob("sell_batch_mult", 1.0))

        def tranche(item, stock):
            cap = 2 * demand.get(item, 1) + 4
            if _batch_mult != 1.0:            # 旗关恒不走此支（保型别同值）
                cap = int(cap * _batch_mult)
            return max(0, min(int(stock), cap))

        for item in ("STRAWBERRY", "MELON", "WOOL", "MILK", "CARROT", "EGG"):
            stock = shed.get(item, 0)
            if not isinstance(stock, (int, float)) or stock <= 0:
                continue
            verdict = _sell_plan_item(item, day, prices, flow, contested)
            dawn_line = dawn_lines.get(item) or {}
            planned_hold = dawn_line.get("verdict") == "hold"
            dawn_price = float(dawn_line.get("spot_price", prices.get(
                item, BASE_PRICE.get(item, 1))) or 1)
            price_crash = prices.get(item, dawn_price) < 0.8 * dawn_price
            # P4 uses the d22 snapshot when present and falls back to the
            # existing live estimate for direct callers without a stage plan.
            p4_clear = _p4_should_clear(item, day, player, plan)
            if p4_clear:
                verdict = "clear"
            if planned_hold and not (emergency or item in contested or
                                     p4_clear or price_crash):
                continue
            if verdict == "clear" and item not in sold_now:
                n = tranche(item, stock)
                if n > 0:
                    out.append(["SELL", item, n])
                    sold_now.add(item)
        return out
    except Exception:
        return []               # fail-open: overrides never break ordering


# --------------------------------------------------------------------------
# 【中文】MK-2 黎明卖出计划器（market §2.1/§2.2，影子件）。
# 黎明一次计划：供给日历（自身公开 tiles 的 horizon=1 上市量 + 棚仓现货）
#   × 吸收表 × 曲线投影 × EOD 预算（scheduler §2.4 联动）× 10 单配额 →
#   每线 {verdict, qty_today, batches, hours, planned_price, defense}。
# 五规则落点：1 囤vs清判据=_sell_plan_item（投影≥现价×HOLD_EDGE 且未
#   争议）；2 争议线零囤；3 批量=min(当日量, 吸收, 库存+上市)；4 EOD
#   溢出→log 曲线小麦强制清（mission eod 事件联动）；5 10 单预算——
#   卖出行数≤SELL_PLAN_MAX_LINES、每线批数≤len(SELL_PLAN_HOURS)，
#   HIRE/BUY 优先序在 plan_market_orders 保持。
# 防御姿态（§4.4 检测-响应表）：flow 为负=被砸，按曲线形状分流
#   log 不理会 / linear 短持穿越 / sq 立即止损。
# 影子纪律：agent() 不消费（_sell_overrides/_market_gates 照旧）；
# MK-3 接管的门禁=回放对账偏差达标（scripts/sell_plan_reconciliation.py）
# + 行为回归 + 线上公共局。
# --------------------------------------------------------------------------
_SELL_PLAN_MEM = {}
_EOD_SELL_EMITTED = {}
_LINEAR_PRESSURE_MEM = {}
SELL_PLAN_HOURS = (6, 12, 18)
SELL_PLAN_MAX_LINES = 4
_DEFENSE_SHAPE = {"WHEAT": "log", "EGG": "log",
                  "STRAWBERRY": "linear", "MILK": "linear",
                  "WOOL": "sq", "MELON": "sq", "CARROT": "log"}


def _sell_plan_dawn(obs, farm, private, day, plan=None):
    """MK-2 dawn sell planner (SHADOW; market §2 full five-rule form)."""
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    absorb = _town_daily_demand(shops)
    contested = _contested_items(obs)
    player = _get(obs, "player", 0)
    flow = _market_flow(player, day, prices)
    shed = _get(private, "shed", {}) or {}
    harvestable = {item: 0 for item in BASE_PRICE}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            amount = _get(tile, "yield_units", 0)
            if not isinstance(amount, (int, float)) or amount <= 0:
                continue
            if _get(tile, "kind", "") == "PLANT":
                item = _get(tile, "crop", "")
            else:
                item = ANIMALS.get(_get(tile, "animal", ""), {}).get(
                    "product", "")
            if item in harvestable:
                harvestable[item] += int(amount)
    mission = mission_shadow(player) or {}
    eod_overflow = int((mission.get("eod") or {}).get("overflow", 0) or 0)
    wheat_carried = sum(
        _get(inv, "WHEAT", 0)
        for inv in (_get(private, "inventories", []) or []) if inv)
    feed_mouths = 0
    if day < ENDGAME_DAY:
        for row in _get(farm, "tiles", []) or []:
            for tile in row:
                if isinstance(tile, dict) and "animal" in tile and \
                        not _get(tile, "fed_today", False):
                    feed_mouths += 1
    wheat_shed_reserve = max(0, feed_mouths + WHEAT_FEED_RESERVE
                             - int(wheat_carried))

    lines = {}
    for item in ("STRAWBERRY", "MELON", "WOOL", "MILK", "CARROT", "EGG",
                 "WHEAT"):
        stock = shed.get(item, 0)
        inflow = harvestable.get(item, 0)
        stock = int(stock) if isinstance(stock, (int, float)) else 0
        # Only post-DROP shed stock is executable by this market phase.
        # Mature tile yield remains diagnostic inflow; HARVEST cannot be paired
        # with DROP in the same turn under the official one-action contract.
        supply = stock
        if item == "WHEAT" and not eod_overflow:
            supply = max(0, supply - wheat_shed_reserve)
        if supply <= 0:
            continue
        price = _get(prices, item, BASE_PRICE.get(item, 0))
        proj = _project_price(item, price, (flow or {}).get(item, 0.0),
                              SELL_PLAN_LOOKAHEAD_DAYS)
        verdict = _sell_plan_item(item, day, prices, flow, contested)
        # P4 uses the same stable d22 tier as the tactical override.
        if _p4_should_clear(item, day, player, plan):
            verdict = "clear"
        # rule 4: EOD overflow -> the log-curve wheat line clears first
        eod_forced = False
        if eod_overflow > 0 and item == "WHEAT" and stock > 0:
            verdict = "clear"
            eod_forced = True
        qty_today = 0
        batches = []
        if verdict == "clear":
            # rule 3: batch = min(当日量, 吸收, 库存+上市)。DTSP 惰性旋钮
            # （P2.5 缺口 1 批量杠杆）：吸收日帽 × sell_batch_mult——旗关
            # 恒 1.0，帽值与 v13.8 同型同值。
            _batch_mult = float(_plan_knob("sell_batch_mult", 1.0))
            day_cap = max(1, absorb.get(item, 1)) if absorb else \
                max(1, 2 * 1 + 4)
            if _batch_mult != 1.0:
                day_cap = max(1, int(day_cap * _batch_mult))
            if eod_forced:
                day_cap = max(day_cap, eod_overflow)
            qty_today = min(supply, day_cap)
            slots = min(len(SELL_PLAN_HOURS), qty_today)
            if slots > 0:
                quotient, remainder = divmod(qty_today, slots)
                batches = [quotient + (1 if i < remainder else 0)
                           for i in range(slots)]
        # defense posture (§4.4): POSITIVE flow = glut building / under
        # attack (EMA convention: supply piling up pushes the price down)
        f = (flow or {}).get(item, 0.0)
        pressure = f > 0
        shape = _DEFENSE_SHAPE.get(item, "log")
        if not pressure:
            defense = "none"
            _LINEAR_PRESSURE_MEM.pop((player, item), None)
        elif shape == "log":
            defense = "ignore"       # log 曲线砸不动（压舱石）
        elif shape == "linear":
            key = (player, item)
            previous = _LINEAR_PRESSURE_MEM.get(key) or {
                "day": -1, "streak": 0}
            if previous.get("day") == day:
                consecutive = previous.get("streak", 1)
            elif previous.get("day") == day - 1:
                consecutive = min(2, previous.get("streak", 1) + 1)
            else:
                consecutive = 1
            _LINEAR_PRESSURE_MEM[key] = {
                "day": day, "streak": consecutive}
            defense = "short_hold"
            # Linear exposure gets one bounded pressure day to recover; on a
            # second consecutive day the planner releases the stock.
            if consecutive == 1 and item not in contested and \
                    not eod_forced and not _p4_should_clear(item, day,
                                                             player, plan):
                verdict = "hold"
                qty_today = 0
                batches = []
        else:
            defense = "cut"          # sq 立即止损 + 产能转移
        if defense == "cut":
            verdict = "clear"
            if qty_today == 0 and supply > 0:
                qty_today = min(supply, max(1, absorb.get(item, 1)))
                batches = [qty_today]
        lines[item] = {"verdict": verdict, "qty_today": qty_today,
                       "batches": batches, "hours": SELL_PLAN_HOURS,
                       "planned_price": round(max(proj, 0.0), 2),
                       "spot_price": price, "defense": defense,
                       "eod_forced": eod_forced, "stock": stock,
                       "inflow": int(inflow)}
    # rule 5: at most SELL_PLAN_MAX_LINES clear lines keep batches today
    clear_items = sorted((k for k, v in lines.items()
                          if v["verdict"] == "clear" and v["batches"]),
                         key=lambda k: (-lines[k]["qty_today"], k))
    for k in clear_items[SELL_PLAN_MAX_LINES:]:
        lines[k]["batches"] = []
        lines[k]["qty_today"] = 0
    return {"day": day, "lines": lines,
            "eod_overflow": eod_overflow}


def _sell_plan_shadow_update(player, day, hour, obs, farm, private, plan):
    """Dawn bypass for the MK-2 sell planner (fail-open, once per day)."""
    st = _SELL_PLAN_MEM.get(player)
    if st is not None and st.get("day") == day \
            and hour >= st.get("hour", 0):
        return st.get("plan")
    try:
        plan_out = _sell_plan_dawn(obs, farm, private, day, plan)
    except Exception:
        plan_out = None
    _SELL_PLAN_MEM[player] = {"day": day, "hour": hour, "plan": plan_out}
    return plan_out


def sell_plan_shadow(player):
    """Read-only getter for the dawn sell plan (or None)."""
    st = _SELL_PLAN_MEM.get(player)
    return (st or {}).get("plan")


# --------------------------------------------------------------------------
# 【中文】MK-3 LIVE（market §2.1）：黎明批次发射 + MK-5 载体 1（§3.3）。
# 批次纪律：只在计划时点（hours[i] <= 当前 hour）发射、每批一次
# （_SELL_BATCH_EMITTED 去重）、门控/覆盖本回合已卖该线则跳过并记已发射
# （计划器为主、门控为有界战术覆盖）；发射量受棚仓现货与 dump-rate
# 限速（2×吸收+4）双钳。干扰载体 1：触发确认（连续 2 天）+ 暴露闸
# （对方顶线价值 ≥ 2× 我方同线暴露）+ 预算闸（零 capex 恒过）三闸全开
# 才倾销；投放量 = 杀伤表反解（目标价 0.75×base 的 offset − 当前 offset），
# 受现货钳制；日复判 = 触发消除自然收手。
# --------------------------------------------------------------------------
_SELL_BATCH_EMITTED = {}
_SELL_BATCH_ORDER_KEYS = {}
_EOD_SELL_ORDER_KEYS = {}
_INTERFERENCE_ORDER_KEYS = {}


def _remap_sell_order_source(source_order, merged_order):
    """Keep sell-source sidecars attached when same-item orders are merged."""
    source_id = id(source_order)
    merged_id = id(merged_order)
    for mapping in (_SELL_BATCH_ORDER_KEYS, _EOD_SELL_ORDER_KEYS,
                    _INTERFERENCE_ORDER_KEYS):
        for key, order_id in list(mapping.items()):
            if order_id == source_id:
                mapping[key] = merged_id


def _finalize_sell_plan_batches(player, day, source_orders, budget):
    """Commit planner and EOD sells only for units accepted by the budget."""
    details = (budget or {}).get("orders") or []
    by_order_id = {}
    for detail in details:
        index = detail.get("index")
        if isinstance(index, int) and 0 <= index < len(source_orders or []):
            by_order_id[id(source_orders[index])] = detail
    for key, state in list(_SELL_BATCH_EMITTED.items()):
        if key[0] != player or key[1] != day or state != "pending":
            continue
        order_id = _SELL_BATCH_ORDER_KEYS.get(key)
        matched = by_order_id.get(order_id)
        filled = max(0, int((matched or {}).get("filled", 0) or 0))
        plan = sell_plan_shadow(player) or {}
        line = (plan.get("lines") or {}).get(key[2]) or {}
        batches = line.get("batches") or []
        planned = max(0, int(batches[key[3]] or 0)) \
            if key[3] < len(batches) else 0
        remaining = max(0, planned - filled)
        if remaining == 0:
            _SELL_BATCH_EMITTED[key] = "committed"
        else:
            if key[3] < len(batches):
                batches[key[3]] = remaining
            _SELL_BATCH_EMITTED.pop(key, None)
        _SELL_BATCH_ORDER_KEYS.pop(key, None)
    for key, state in list(_EOD_SELL_EMITTED.items()):
        if key[0] != player or key[1] != day or state != "pending":
            continue
        matched = by_order_id.get(_EOD_SELL_ORDER_KEYS.get(key))
        requested = max(0, int(key[4] or 0))
        filled = max(0, int((matched or {}).get("filled", 0) or 0))
        if filled >= requested and requested > 0:
            _EOD_SELL_EMITTED[key] = "committed"
        else:
            _EOD_SELL_EMITTED.pop(key, None)
        _EOD_SELL_ORDER_KEYS.pop(key, None)
    for key, order_id in list(_INTERFERENCE_ORDER_KEYS.items()):
        if key[0] != player or key[1] != day:
            continue
        matched = by_order_id.get(order_id)
        filled = max(0, int((matched or {}).get("filled", 0) or 0))
        requested = max(0, int(key[3] or 0))
        if filled >= requested and requested > 0:
            for rec in reversed(_INTERFERENCE_LOG):
                if rec.get("day") == day:
                    rec["fired_vehicle1"] = {
                        "item": key[2], "qty": requested}
                    break
        _INTERFERENCE_ORDER_KEYS.pop(key, None)


def _sell_plan_batches_due(obs, day, hour, shed, existing_orders):
    """MK-3: emit dawn-planner batches whose planned hour has arrived."""
    try:
        if day >= SEASON_DAYS - 1:
            return []               # d29 liquidation owns everything
        player = _get(obs, "player", 0)
        plan = sell_plan_shadow(player)
        if plan is None or plan.get("day") != day:
            return []
        sold_now = {o[1] for o in existing_orders
                    if isinstance(o, list) and o and o[0] == "SELL"}
        shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        demand = _town_daily_demand(shops)
        out = []
        for item in sorted((plan.get("lines") or {})):
            line = plan["lines"][item]
            batches = line.get("batches") or []
            hours = line.get("hours") or ()
            stock = shed.get(item, 0)
            if not isinstance(stock, (int, float)) or stock <= 0:
                continue
            for bi, qty in enumerate(batches):
                key = (player, day, item, bi)
                if key in _SELL_BATCH_EMITTED:
                    continue
                if bi < len(hours):
                    due = hours[bi]
                elif hours:
                    due = hours[-1]
                else:
                    due = 24
                if hour < due:
                    continue
                if item in sold_now:
                    overlay = next((o for o in existing_orders
                                    if isinstance(o, list) and len(o) >= 3
                                    and o[0] == "SELL" and o[1] == item), None)
                    if overlay is not None:
                        _SELL_BATCH_EMITTED[key] = "pending"
                        _SELL_BATCH_ORDER_KEYS[key] = id(overlay)
                    break           # gate overlay owns this line this turn
                n = max(0, min(int(qty), int(stock),
                               2 * demand.get(item, 1) + 4))
                if n > 0:
                    order = ["SELL", item, n]
                    out.append(order)
                    _SELL_BATCH_EMITTED[key] = "pending"
                    _SELL_BATCH_ORDER_KEYS[key] = id(order)
                    sold_now.add(item)
                break               # one batch of this line per turn
        return out
    except Exception:
        return []                   # fail-open: never break ordering


def interference_confirmed(player, day):
    """Read-only view of the MK-4 trigger streak for the strategy layer's
    vehicle arming (aggressive wave C): the last INTERFERENCE_CONFIRM_DAYS
    records strictly before `day` must all be confirmed triggers."""
    streak = 0
    for rec in reversed(_INTERFERENCE_LOG):
        if rec.get("player") != player or rec.get("day", day) >= day:
            continue
        if rec.get("confirmed"):
            streak += 1
            if streak >= INTERFERENCE_CONFIRM_DAYS:
                return True
        else:
            return False
    return False


def _interference_v2_orders(obs, farm, private, day, plan=None):
    """MK-5 vehicle 2 (carrot ambush) dump leg (aggressive wave C): when
    the strategy layer armed the ambush (iv2_target_day pinned in the
    stage register) and the trigger is still confirmed, dump the whole
    carrot stock at/after the target day.  Rides the normal budget
    truncation; zero extra capex (the block was grown earlier)."""
    try:
        target = (plan or {}).get("iv2_target_day")
        if not target or day < int(target) or day >= SEASON_DAYS - 1:
            return []
        player = _get(obs, "player", 0)
        if not interference_confirmed(player, day):
            return []
        shed = _get(private, "shed", {}) or {}
        stock = shed.get("CARROT", 0)
        if not isinstance(stock, (int, float)) or stock <= 0:
            return []
        return [["SELL", "CARROT", int(stock)]]
    except Exception:
        return []


def _interference_orders(obs, farm, private, day, prices, plan=None):
    """MK-5 vehicle 1: dump OUR held stock of the opponent's top line.

    Zero-cost, same-day, reversible.  Gates (§3.5): trigger confirmed by
    the shadow (2 consecutive days), kill/exposure >= 2 on the opponent's
    strongest line, budget trivially satisfied (no capex).  Standdown is
    automatic: the trigger is re-evaluated daily.
    """
    try:
        if day >= SEASON_DAYS - 1 or day < DEAD_PRICE_FROM_DAY:
            _interference_shadow(obs, farm, day, prices, plan=plan)
            return []
        triggered = _interference_shadow(obs, farm, day, prices, plan=plan)
        if not triggered or not _INTERFERENCE_LOG:
            return []
        player = _get(obs, "player", 0)
        rec = next((row for row in reversed(_INTERFERENCE_LOG)
                    if row.get("player") == player and row.get("day") == day),
                   None)
        if rec is None or not rec.get("confirmed"):
            return []
        if rec.get("fired_vehicle1"):
            return []
        if any(key[0] == _get(obs, "player", 0) and key[1] == day
               for key in _INTERFERENCE_ORDER_KEYS):
            return []
        item = rec.get("top_opp_line")
        if not item or not rec.get("gate_exposure") \
                or not rec.get("gate_budget"):
            return []
        shed = _get(private, "shed", {}) or {}
        stock = shed.get(item, 0)
        if not isinstance(stock, (int, float)) or stock <= 0:
            return []
        # kill-table inverse: units needed to push the price to 0.75x base
        price = _get(prices, item, BASE_PRICE.get(item, 0))
        target = max(1, int(BASE_PRICE.get(item, 1) * 0.75))
        if price <= target:
            return []               # already at/below the kill level
        offset_target = _offset_from_price(item, target)
        offset_now = _offset_from_price(item, price)
        dump = int(max(0, offset_target - offset_now))
        if dump <= 0:
            return []
        dump = min(dump, int(stock))
        if dump <= 0:
            return []
        # The firing lock is committed only after the final budget pass accepts
        # the order; a rejected interference candidate must be retried.
        order = ["SELL", item, dump]
        _INTERFERENCE_ORDER_KEYS[(player, day, item, dump)] = id(order)
        return [order]
    except Exception:
        return []


def interference_shadow_log():
    """Read-only access to the MK-4 shadow log (diagnostics only)."""
    return list(_INTERFERENCE_LOG)


_INTERFERENCE_MEM = {}       # per-player consecutive-trigger memory


def _calendar_flow_value(farm, day, prices, absorb, flow, horizon=7):
    """R = Σ 日历(7d) × min(供给, 吸收) × 投影价（market §3.2 修偏版）。

    变现量被城镇吸收封顶（零吸收产品贡献 0——"零吸收没有任何变现
    机制"）；价用 SELL_PLAN_LOOKAHEAD_DAYS 投影而非现货快照。
    """
    if farm is None:
        return 0.0, {}
    cal = _opp_production_calendar(farm, day, horizon=horizon)
    total = 0.0
    per_item = {}
    for item, daily in cal.items():
        cap = absorb.get(item, 0) if absorb else 0
        realizable = sum(min(amt, cap) for amt in daily)
        if realizable <= 0:
            per_item[item] = 0.0
            continue
        price = _get(prices, item, BASE_PRICE.get(item, 0))
        proj = _project_price(item, price, (flow or {}).get(item, 0.0),
                              SELL_PLAN_LOOKAHEAD_DAYS)
        value = realizable * max(0.0, proj)
        per_item[item] = value
        total += value
    return total, per_item


def _interference_shadow(obs, farm, day, prices, plan=None):
    """MK-4 trigger ("shadow" is a historical name: vehicle 1 has been LIVE
    since INTERFERENCE_ARMED=True, Phase-D arming 2026-09-02; vehicles 2-4
    stay NO-GO).  This function only evaluates and logs -- it never emits
    orders itself; its return value gates the vehicle-1 dump orders.

    R_opp = 对手日历 × min(供给, 吸收) × 投影价（§3.2 原式）；R_us 用同式
    对称流（可比口径；文档原文的 R_us=_plan_rollout 终值是 12 日存量口径，
    与 7 日流量不可直接比——rollout 终值另行入日志供边际定标，解读记
    JOURNAL）。触发需连续 INTERFERENCE_CONFIRM_DAYS 天确认（防单日噪声）；
    三道风险闸布尔入日志（§3.5：杀伤/暴露≥2、干扰预算≤容量 15%、
    触发消除即收手=日复判）。
    """
    try:
        farms = _get(obs, "farms", []) or []
        player = _get(obs, "player", 0)
        opp = None
        for i, f in enumerate(farms):
            if i != player:
                opp = f
                break
        if opp is None:
            return False
        shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        absorb = _town_daily_demand(shops)
        flow = _market_flow(player, day, prices)
        r_opp, opp_lines = _calendar_flow_value(opp, day, prices, absorb,
                                                flow)
        r_us, our_lines = _calendar_flow_value(farm, day, prices, absorb,
                                               flow)
        raw_trigger = r_opp > r_us + INTERFERENCE_MARGIN

        # consecutive-day confirmation (§3.2); repeated turns within one day
        # reuse that day's decision and never advance or reset the streak.
        mem = _INTERFERENCE_MEM.get(player) or {
            "day": -1, "streak": 0, "raw_trigger": False}
        if mem.get("day") == day:
            streak = mem.get("streak", 0)
        elif raw_trigger:
            streak = mem.get("streak", 0) + 1 \
                if mem.get("day") == day - 1 else 1
        else:
            streak = 0
        _INTERFERENCE_MEM[player] = {
            "day": day, "streak": streak, "raw_trigger": raw_trigger}
        confirmed = raw_trigger and streak >= INTERFERENCE_CONFIRM_DAYS

        # gate 1: kill/exposure >= 2 on the opponent's strongest line (§3.5)
        top_item = max(opp_lines, key=lambda k: (opp_lines[k], k)) \
            if opp_lines else None
        kill_value = opp_lines.get(top_item, 0.0) if top_item else 0.0
        exposure = our_lines.get(top_item, 0.0) if top_item else 0.0
        gate_exposure = top_item is not None and exposure > 0 and \
            kill_value >= INTERFERENCE_EXPOSURE_RATIO * exposure
        current_hands = len(_get(farm, "hands", []) or [])
        scan = _farm_scan(farm)
        planned_hands = _crew_target(
            day, scan.get("herd", 0), scan.get("wheat", 0),
            len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]), plan)
        law_units = _capacity_law_max(max(current_hands, planned_hands))
        gate_budget = law_units * INTERFERENCE_BUDGET_FRAC >= 1.0

        # rollout terminal for margin calibration (not the trigger term)
        r_us_rollout = None
        try:
            scan = _farm_scan(farm)
            demand = absorb or {}
            p_straw = _get(prices, "STRAWBERRY", BASE_PRICE["STRAWBERRY"])
            roll = _plan_rollout(day, scan, plan or {}, prices, demand,
                                 p_straw)
            r_us_rollout = round(float(roll.get("terminal", 0.0)), 1)
        except Exception:
            r_us_rollout = None

        fired = None
        for index in range(len(_INTERFERENCE_LOG) - 1, -1, -1):
            prev = _INTERFERENCE_LOG[index]
            if prev.get("player") == player and prev.get("day") == day:
                fired = prev.get("fired_vehicle1")
                del _INTERFERENCE_LOG[index]
                break
        record = {
            "day": day, "r_opp": round(r_opp, 1),
            "r_us_flow": round(r_us, 1), "r_us_rollout": r_us_rollout,
            "raw_trigger": raw_trigger, "streak": streak,
            "player": player, "confirmed": confirmed,
            "top_opp_line": top_item, "gate_exposure": gate_exposure,
            "gate_budget": gate_budget, "capacity_units": law_units,
            "armed": INTERFERENCE_ARMED}
        if fired is not None:
            record["fired_vehicle1"] = fired
        _INTERFERENCE_LOG.append(record)
        if len(_INTERFERENCE_LOG) > 60:
            del _INTERFERENCE_LOG[:len(_INTERFERENCE_LOG) - 60]
        return confirmed and INTERFERENCE_ARMED
    except Exception:
        return False


def _market_orders(obs, farm, private, day, animals_to_feed, herd_total,
                   plan=None):
    money = _get(farm, "money", 0.0)
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    player = _get(obs, "player", 0)
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    last_day = day >= SEASON_DAYS - 1
    town_shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    if plan is None:
        plan = _DEFENSIVE_PLAN
    builds, crop_map, _placed, capacity = _field_alloc(farm, day, prices,
                                                       plan)

    orders = []
    # WHEAT_FARM keeps a conservative projected wallet while building the
    # same-turn queue.  The engine commits market orders sequentially, so
    # sizing later seeds/animals from the opening wallet can cross the hold
    # reserve after an earlier feed or land purchase succeeds.
    projected_money = money

    # ---- land plan (FM-O2): NE day 4+, SW day 7+; the fund is protected --
    # (working capital -- seeds/feed -- is never blocked: it pays for the
    # land; herd buys wait for the fund while it is pending).  The purchase
    # itself stays eligible every day after the due day -- the block on the
    # herd simply lapses so a slow season cannot deadlock the ranch.
    land_fund = 0
    land_pending = False
    # v10 M-E: same-turn spend ledger.  Every BUY_* order appended below
    # deducts here so later gates (feed, animals) price the wallet as the
    # engine will see it after this turn's queue, not the raw dawn money
    # (ep 103783585: land + 3 sheep + seeds in one turn drained 3256 to
    # 16 because the animal gate read the pre-land wallet).
    committed_spend = 0.0
    buy_product_units = 0
    # Capacity is reserved as orders are appended.  The engine commits the
    # queue sequentially, so every later capex gate must see earlier buys.
    reserved_units = 0.0

    def capacity_batch_limit(requested, unit_cost=1.0):
        requested = max(0, int(requested))
        while requested > 0 and not _capacity_gate(
                farm, private, reserved_units + requested * unit_cost,
                day, plan)[0]:
            requested -= 1
        return requested

    _land_ovr = (plan or {}).get("land_plan_override") or {}
    if quads in LAND_PLAN or quads in _land_ovr:
        due_day, fund = _land_ovr.get(quads) or LAND_PLAN[quads]
        # r4-P3: SW after day 18 cannot deploy a repaying asset (strawberry
        # phase over, pasture ring of NW+NE already holds 17 head) -- the
        # 2000 buys liquidity instead
        if quads == 2 and day > LAND_LATE_CUTOFF:
            land_fund = 0
        elif day >= due_day:
            land_fund = fund
            # branch §5.4 triple gate (labor + cash dims): a quadrant is 25
            # asset-unit tiles; the purchase may only land inside the
            # capacity law and leave the dawn cash invariant intact.
            cap_ok, _util = _capacity_gate(
                farm, private, reserved_units + 25.0, day, plan)
            # cash dim: the fund already embeds price + cushion, so the
            # invariant prices only the land COST against the floor+bill.
            if money >= fund and cap_ok \
                    and _cash_gate_ok(farm, LAND_PRICE[quads]):
                orders.append(["BUY_LAND"])
                committed_spend += LAND_PRICE[quads]
                reserved_units += 25.0
                if plan.get("wheat_farm"):
                    projected_money -= LAND_PRICE[quads]
            elif day < due_day + LAND_PEND_WINDOW:
                land_pending = True

    # r5-P4 volume quadrant: while the strawberry window is open, SE
    # (4000) becomes a buyable asset -- 25 more tiles at the 42-tile
    # strawberry field's realized band repay it several times over
    # (round-3 ledger: Renji's 42-tile field).  No herd-blocking fund:
    # the 14-head plan is already built by the day this can fire.
    # branch §5.4: SE passes the same labor/cash triple gate.
    d10_ready = plan.get("se_ready")
    if plan["volume"] and quads == 3 \
            and (d10_ready is None or d10_ready) \
            and SE_DUE_DAY <= day <= SE_BUY_LAST_DAY and money >= SE_FUND \
            and _capacity_gate(farm, private, reserved_units + 25.0,
                               day, plan)[0] \
            and _cash_gate_ok(farm, LAND_PRICE[3]):
        orders.append(["BUY_LAND"])
        committed_spend += LAND_PRICE[3]
        reserved_units += 25.0

    # ---- §2.3 feed precondition (scheduler design): the dawn mission
    # computes the D1/D2 mouth deficit and injects an h0 BUY_PRODUCT WHEAT
    # event -- an OBLIGATION, not an opportunity (stranded dawn wheat is
    # stranded red lines; the four-layer solver pre-filters FEED tasks it
    # cannot stock).  Consumed at hour <= 2 for the deficit not yet in the
    # system; the feed-security block below counts it via sys_wheat so the
    # two never double-buy.
    precond_wheat = 0
    precondition_covered = False
    if not last_day and _get(obs, "hour", 0) <= 2:
        _mission = mission_shadow(_get(obs, "player", 0)) or {}
        _sys_w = shed.get("WHEAT", 0) + sum(
            _get(inv, "WHEAT", 0)
            for inv in (_get(private, "inventories", []) or []) if inv)
        for _ev in _mission.get("events") or []:
            if _ev.get("why") != "feed_precondition" \
                    or _ev.get("op") != "BUY_PRODUCT":
                continue
            # idempotent across the h0-h2 window: once the bought wheat
            # has landed, system wheat covers the dawn deficit -> skip
            if _sys_w >= max(0, int(_ev.get("qty") or 0)):
                precondition_covered = True
                continue
            _short = _affordable_buy_units(
                "WHEAT", money - committed_spend - 60, obs,
                buy_product_units)
            _short = min(_short, max(0, int(_ev.get("qty") or 0)))
            if _short > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", _short])
                market_inventory = _get(_get(obs, "market", {}) or {},
                                        "inventory", None)
                shifted_inventory = dict(market_inventory or {})
                shifted_inventory["WHEAT"] = int(
                    shifted_inventory.get("WHEAT", MARKET_I0_EMB)) - \
                    buy_product_units
                committed_spend += buy_product_cost(
                    "WHEAT", _short, shifted_inventory)
                buy_product_units += _short
                precond_wheat += _short

    # ---- feed security (FM-O3 + m2b phantom guard): never let the herd
    # run short of wheat, counting what carriers already hold (a shed-only
    # check sees the morning pickup as a shortfall and re-buys what we just
    # sold -- measured -8k/season).  Guardrail: normal-state buys stop at
    # FEED_BUY_MAX_PRICE (profile avg 26-32); starvation cap 85 kept (dear
    # wheat is still cheaper than a lost animal).
    wheat_carried = sum(_get(inv, "WHEAT", 0)
                        for inv in (_get(private, "inventories", []) or []) if inv)
    sys_wheat = shed.get("WHEAT", 0) + wheat_carried + precond_wheat
    if animals_to_feed > 0 and not last_day \
            and sys_wheat < animals_to_feed + 3:
        cap = 85 if sys_wheat < animals_to_feed else \
            plan.get("feed_max_price", FEED_BUY_MAX_PRICE)
        if prices.get("WHEAT", 25) <= cap:
            # r5-P4 volume: the 42-tile field leaves little room for feed
            # wheat, so the daily guardrailed buy widens (Renji bought
            # 1501u/season; profiles 414-2732u)
            want = min((24 if plan["volume"] or plan.get("wheat_farm") else 16),
                       animals_to_feed + 8 - sys_wheat)
            wheat_px = prices.get("WHEAT", 25)
            if plan.get("wheat_farm"):
                unit_budget = max(1, cap + 1)
                affordable = max(
                    0, int((projected_money - WHEAT_FARM_HOLD_CASH) //
                           unit_budget))
                want = min(want, affordable)
            else:
                # v10 M-E: affordability gate -- ep 103783585 re-issued
                # BUY_PRODUCT WHEAT 10 for 24 straight turns at money=8
                # (all rejected); the herd still starved two days later
                # MS-1.1: per-unit walk along the embedded curve
                # (buy_product_cost) -- matches plan_market_orders exactly.
                want = min(want, _affordable_buy_units(
                    "WHEAT", money - committed_spend - 60, obs,
                    buy_product_units))
            if want > 0:
                # market §5 小件 2：BUY 抽货推高曲线——大单跨回合分批。
                want = min(want, BUY_CHUNK_MAX_UNITS)
                orders.append(["BUY_PRODUCT", "WHEAT", want])
                market_inventory = _get(_get(obs, "market", {}) or {},
                                        "inventory", None)
                shifted_inventory = dict(market_inventory or {})
                shifted_inventory["WHEAT"] = int(
                    shifted_inventory.get("WHEAT", MARKET_I0_EMB)) - \
                    buy_product_units
                committed_spend += buy_product_cost(
                    "WHEAT", want, shifted_inventory)
                buy_product_units += want
                sys_wheat += want
                if plan.get("wheat_farm"):
                    projected_money -= want * unit_budget

    # Cheap wheat can widen a real feed shortfall, but carrier-held wheat is
    # already system stock and must not trigger a phantom refill.
    if prices.get("WHEAT", 25) < OPPORTUNE_WHEAT_PRICE \
            and sys_wheat < animals_to_feed + 3 \
            and not last_day and not precondition_covered:
        hoard_target = animals_to_feed * OPPORTUNE_WHEAT_DAYS + 3
        shed_room = max(0, SHED_CAPACITY - int(shed_count) - buy_product_units)
        desired = min(max(0, hoard_target - sys_wheat),
                      BUY_CHUNK_MAX_UNITS, shed_room)
        affordable = _affordable_buy_units(
            "WHEAT", money - committed_spend - 60, obs,
            buy_product_units)
        extra = min(desired, affordable)
        if extra > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", extra])
            market_inventory = _get(_get(obs, "market", {}) or {},
                                    "inventory", None)
            shifted_inventory = dict(market_inventory or {})
            shifted_inventory["WHEAT"] = int(
                shifted_inventory.get("WHEAT", MARKET_I0_EMB)) - \
                buy_product_units
            committed_spend += buy_product_cost(
                "WHEAT", extra, shifted_inventory)
            buy_product_units += extra
            sys_wheat += extra

    # Consume mission EOD budget events once their planned hour arrives.  The
    # mission is cached for the day, so an explicit ledger prevents duplicate
    # SELL orders on h7..h23 while still allowing the current shed to clamp qty.
    mission = mission_shadow(player) or {}
    eod_events = [event for event in (mission.get("events") or [])
                  if event.get("why") == "eod_budget"
                  and event.get("op") == "SELL"
                  and int(event.get("h", 0) or 0) <= int(
                      _get(obs, "hour", 0) or 0)]
    for event in eod_events:
        event_key = (player, day, str(event.get("item")),
                     int(event.get("h", 0) or 0),
                     int(event.get("qty", 0) or 0))
        if event_key in _EOD_SELL_EMITTED:
            continue
        item = event.get("item")
        stock = shed.get(item, 0)
        qty = min(max(0, int(event.get("qty", 0) or 0)),
                  int(stock) if isinstance(stock, (int, float)) else 0)
        _EOD_SELL_EMITTED[event_key] = "pending"
        if qty > 0:
            order = ["SELL", item, qty]
            orders.append(order)
            _EOD_SELL_ORDER_KEYS[event_key] = id(order)

    # ---- seeds: the wheat feed floor first (m2b), then rotation crops
    # staged behind the pending land fund (FM-3 staging).  R3-3 exception:
    # strawberry is NOT staged behind the land fund once its phase opens --
    # the winners plant 6+ tiles on d5-11 while the NE/SW purchases proceed
    # on their own fund-gated schedule (planting d5 pays from d15 at
    # ~200/u; the one-day land delay it can cost repays many times over).
    # v9-W1 (round-5 online forensics 2026-08-30): the legacy
    # seeds<6->buy-12 cadence let the feed floor decay to zero by d20 in
    # every round-5 game; the spiral only detonated in DEAR-wheat seasons
    # (JIlong Zhou game: wheat 37-41 all season, field dead, 1067u external
    # feed at ~39.5/u = 42.2k spend, d12 cash 4).  An ungated buy-to-cap
    # measured -837.8k / disaster 0.0455 / baseline_wheat 0.625 on the dev
    # gate (2026-08-31 v9_w1_port_dev): in cheap seasons the 18-tile
    # refill burns the thin d4-12 wallet and ~27 extra ops/day crowd the
    # strawberry/melon labour line.  So the refill is gated to the failure
    # condition and maintains the feed floor.
    # v9.2 (round-6 forensics 2026-08-31): wheat ramps 25 -> 50+ in EVERY
    # game while the field decays in the d8-14 window at prices 29-34 --
    # the >= 35 gate only opened at d14-16 with the field already dead and
    # the wallet at 28-2000 (wallet-scaled batches bought ~0 seeds).  The
    # maintenance gate moves down to 30 so the refill acts inside the
    # decay window, while the genuinely cheap bands (< 30) keep the v7.2
    # legacy cadence byte-identical (round-6 win 103422278 sat at wheat
    # 22-24 on d8-12 and won without any refill).
    alive = _count_crops(farm)
    wheat_price_now = _get(prices, "WHEAT", 25)
    if not plan.get("wheat_farm") and day <= SEASON_DAYS - 7 \
            and wheat_price_now >= 30:
        wheat_cap_now = _wheat_cap(day, wheat_price_now)
        want_w = wheat_cap_now - alive.get("WHEAT", 0) - seeds.get("WHEAT", 0)
        # round-19 audit: a 26-tile / 2-day-cycle field needs ~13
        # replants/day; the old <6 -> 12 top-up oscillated into day-long
        # replant blackouts (d9-12 plants fell to 1-2/day, field 33 -> 3)
        floor_w = 13 if seeds.get("WHEAT", 0) < 13 else 0
        batch_w = min(24, max(floor_w, want_w))
        if day <= 2:
            batch_w = min(batch_w, 18)   # top plants 17.6 tiles on d0
            # (the 4-head opening + 500 reserve leave wallet room now)
        # working-capital class (like feed): scale to the wallet instead of
        # rejecting the whole order -- round-5 forensics showed d8-12
        # wallets of 4-629 cash starving a 10-coin seed under a flat 150
        # gate.
        batch_w = min(batch_w, max(0, int((money - 20) // 10)))
        if batch_w > 0:
            batch_w = capacity_batch_limit(batch_w, 1.0)
        if batch_w > 0:
            orders.append(["BUY_SEED", "WHEAT", batch_w])
            committed_spend += batch_w * CROPS["WHEAT"]["seed"]
            reserved_units += float(batch_w)
    elif not plan.get("wheat_farm") and seeds.get("WHEAT", 0) < 6 \
            and day <= SEASON_DAYS - 7 and money >= 150:
        batch_w = capacity_batch_limit(12, 1.0)
        if batch_w > 0:
            orders.append(["BUY_SEED", "WHEAT", batch_w])
            committed_spend += batch_w * CROPS["WHEAT"]["seed"]
            reserved_units += float(batch_w)
    if plan.get("wheat_farm") and not last_day \
            and day <= PLANT_LAST_DAY["WHEAT"]:
        alive_wheat = alive.get("WHEAT", 0)
        target_wheat = min(plan.get("wheat_total_cap", WHEAT_FARM_WHEAT_CAP),
                           WHEAT_FARM_WHEAT_CAP)
        wanted_wheat = max(0, target_wheat - alive_wheat -
                           seeds.get("WHEAT", 0))
        if wanted_wheat > 0 and \
                projected_money >= WHEAT_FARM_CASH_REDLINE + 10:
            batch = min(
                24, wanted_wheat,
                max(0, int((projected_money - WHEAT_FARM_CASH_REDLINE) //
                           CROPS["WHEAT"]["seed"])))
            if batch > 0:
                batch = capacity_batch_limit(batch, 1.0)
            if batch > 0:
                orders.append(["BUY_SEED", "WHEAT", batch])
                projected_money -= batch * CROPS["WHEAT"]["seed"]
                reserved_units += float(batch)
    if not last_day:
        crop_seed_sequence = ("STRAWBERRY",) if plan.get("wheat_farm") else \
            ("STRAWBERRY", "MELON", "CARROT")
        # V-T3: premium seed ORDERS stay inside the daily planting budget,
        # derived from the OBSERVATION (tiles planted today) so the gate is
        # idempotent -- the deterministic-agent contract forbids cross-call
        # ledgers (d8 pulse: the first milk cheque bought 10 strawberry
        # seeds at once and the afternoon could not water them).
        planted_today_orders = 0
        for _row in (_get(farm, "tiles", []) or []):
            for _t in _row:
                if isinstance(_t, dict) and _get(_t, "kind", "") == "PLANT" \
                        and _get(_t, "planted_day", -1) == day:
                    planted_today_orders += 1
        room_budget = max(0, PLANT_DAILY_CAP - planted_today_orders)
        for crop in crop_seed_sequence:
            lo, hi = CROP_PHASE[crop]
            if not (lo <= day <= hi):
                continue
            if prices.get(crop, BASE_PRICE[crop]) < CROP_FLOOR[crop]:
                continue  # red line: dead-price freeze
            # branch §5.4 curve dim (projection supersedes the spot freeze
            # above): never plant into a curve whose 2-day projection is
            # already under the floor.
            if not _curve_gate_ok(crop, _get(obs, "player", 0), day, prices):
                continue
            cap_for_crop = len(crop_map.get(crop, ()))
            if crop == "MELON" and "melon_total_cap" in plan:
                cap_for_crop = min(cap_for_crop,
                                   int(plan.get("melon_total_cap", 0)))
            want = cap_for_crop - alive[crop] - seeds.get(crop, 0)
            seed_gate = 250 if crop == "STRAWBERRY" else land_fund + 250
            wallet = projected_money if plan.get("wheat_farm") else money
            reserve_gate = max(seed_gate, WHEAT_FARM_HOLD_CASH) \
                if plan.get("wheat_farm") else seed_gate
            # V-T10 zero-inventory seed flow (tetsuya: buy == plant the
            # same day; his cheque never sits in seeds).  The batch SCALES
            # TO THE DISPOSABLE wallet -- the v10.8 self-play regression
            # (45-54k) traced to the d7 NE purchase + a full 16-seed batch
            # double-dipping one wallet while the herd build starved.
            wallet_for_seeds = wallet - (0.0 if plan.get("wheat_farm")
                                         else committed_spend)
            seed_affordable = max(0, int((wallet_for_seeds - reserve_gate) //
                                         CROPS[crop]["seed"]))
            batch = min(8, max(0, want), room_budget, seed_affordable)
            if plan.get("wheat_farm") or \
                    (crop == "STRAWBERRY" and plan["volume"]):
                # Opt-in wheat mode and VOLUME use wallet-scaled batches;
                # WHEAT_FARM also preserves its hold reserve after every
                # earlier same-turn purchase.  2026-09-04 激进模式：
                # 6/10 -> 8/16（建线密度对齐 top-20；钱包界
                # seed_affordable 仍逐单硬约束）。
                batch = min(16 if plan["volume"] else 8, max(0, want),
                            room_budget, seed_affordable)
            if batch > 0 and wallet >= reserve_gate + \
                    CROPS[crop]["seed"] * batch:
                batch = capacity_batch_limit(batch, 1.0)
            if batch > 0 and wallet >= reserve_gate + \
                    CROPS[crop]["seed"] * batch:
                orders.append(["BUY_SEED", crop, batch])
                committed_spend += CROPS[crop]["seed"] * batch
                reserved_units += float(batch)
                room_budget -= batch
                if plan.get("wheat_farm"):
                    projected_money -= CROPS[crop]["seed"] * batch

    # ---- herd (FM-O2 + R3-1/R3-2): mixed 14-head ranch, money-gated,
    # paced by CONFIRMED purchases (m2b), species-level dead-price freeze
    # (red line).  Day 0 is the r3 opening: the burst buys OPENING_HERD
    # outright (2C+2S = 1800 of the 3000 start; 116/116 top-20 seats and
    # 3/3 round-2 winners put 4-5 head on d0 -- the m3 1-sheep opening is
    # the fork the round-2 losses traced to), both species in one turn so
    # cows reach the day-8 milk window AND sheep the day-6 wool window.
    reserve = 800 if day <= 3 else (550 if day <= 7 else COW_BUY_RESERVE)
    if land_pending:
        reserve += land_fund
    pace = _animal_pace(day)
    target = _herd_target(day, 99)   # FM-O3: external feed releases autarky
    if plan.get("wheat_farm"):
        target = min(WHEAT_FARM_HERD_FLOOR, target)
    # r4-P3: state-driven ceiling above the plan when the marginal NPV,
    # market absorption and feed line all clear (cap 17 safety boundary)
    wheat_carried_early = sum(_get(inv, "WHEAT", 0)
                              for inv in (_get(private, "inventories", [])
                                          or []) if inv)
    sys_wheat_early = shed.get("WHEAT", 0) + wheat_carried_early
    absolute_ceiling = MODE_HERD_CAP_SCALE if plan.get("scale") \
        else HERD_CAP_NPV
    herd_ceiling = min(plan.get("herd_ceiling", absolute_ceiling),
                       absolute_ceiling)
    npv_ceiling = min(HERD_CAP, herd_ceiling)
    preferred_species = None
    if herd_total >= HERD_CAP and not plan.get("wheat_farm"):
        # r4-P3: the NPV ceiling EXTENDS the completed 14-head plan (never
        # accelerates it -- the day-0 burst and the r3 deadline stand)
        decision_ceiling, preferred_species = _npv_herd_decision(
            day, prices, herd_total,
            _species_counts(farm, private, herd_total),
            _town_daily_demand(town_shops), sys_wheat_early, plan=plan)
        npv_ceiling = min(herd_ceiling, decision_ceiling)
        target = max(target, npv_ceiling)
    bought = _buy_pace(_get(obs, "player", 0), day, _get(obs, "hour", 0),
                       herd_total)
    opening_bought = False
    _open_seq = OPENING_SHIFT_SEQ if OPENING_SHIFT else {0: OPENING_HERD}
    _seq_ovr = (plan or {}).get("opening_seq_override") or {}
    if _seq_ovr:
        # B1 catch-up stride (aggressive wave C): branch-level absolute
        # species targets merged over the base opening sequence; the
        # wallet (OPENING_RESERVE) and capacity gates below still bind.
        _open_seq = {k: dict(v) for k, v in _open_seq.items()}
        for _d, _spec in _seq_ovr.items():
            _m = dict(_open_seq.get(_d, {}))
            _m.update(_spec)
            _open_seq[_d] = _m
    if not last_day and day in _open_seq:
        _species_pre = _species_counts(farm, private, herd_total)
        spend = 0
        for animal in ("COW", "SHEEP"):
            want = max(0, _open_seq[day].get(animal, 0) - 0)
            if OPENING_SHIFT:
                want = max(0, _open_seq[day].get(animal, 0)
                           - _species_pre.get(animal, 0))
            cost = ANIMALS[animal]["cost"]
            n = min(want, int((money - spend - OPENING_RESERVE) // cost)) \
                if money - spend > OPENING_RESERVE else 0
            if n > 0:
                n = capacity_batch_limit(n, 2.0)
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                reserved_units += 2.0 * n
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
                spend += n * cost
                opening_bought = True
    # V-T1: under the opening shift the paced loop also stands down on
    # day 0 -- the whole day belongs to the wheat opening, no animals.
    _opening_shift_hold = OPENING_SHIFT and day == 0
    # DTSP 惰性旋钮（P2.5，缺口 2 买畜时点）：herd_start_day 门控节奏环
    # 起步日（计划可推迟扩栏起点）；旗关恒 0——day>=0 恒真，与 v13.8 同。
    _herd_start_day = _plan_knob("herd_start_day", 0)
    if not opening_bought and not _opening_shift_hold and not last_day \
            and day >= _herd_start_day \
            and herd_total < target \
            and shed_count < 88 and bought < pace:
        species = _species_counts(farm, private, herd_total)
        # interleave species by relative deficit so cows reach their day-8+
        # premium-milk window on time instead of queueing behind the sheep
        candidates = sorted((a for a in HERD_COMPOSITION if HERD_COMPOSITION[a] > 0),
                            key=lambda a: species[a] / float(HERD_COMPOSITION[a]))
        # branch §4.2 B1 产品分化：YARN_STORE 未解锁的爆发对手面前，羊线
        # 换牛线（plan["p1_species_pref"]，strategy._b_branch_adjust 注入）。
        _p1_pref = plan.get("p1_species_pref")
        if _p1_pref in ("COW", "SHEEP") and _p1_pref in candidates:
            candidates = [_p1_pref] + [a for a in candidates if a != _p1_pref]
        # branch §5.3/§5.4 labor dim：畜群扩张（步速循环）不得越过容量定律
        # ——黎明不变式 >0.85 拒购（任务包 capacity_deficit 的市场侧镜像）。
        _herd_cap_ok = _capacity_gate(farm, private, 0.0, day, plan)[0]
        if npv_ceiling > HERD_CAP and preferred_species is not None:
            candidates = [preferred_species]
        for animal in candidates:
            comp_cap = HERD_COMPOSITION[animal]
            if npv_ceiling > HERD_CAP:
                # P3 NPV branch: extend the selected species from its current
                # count, including composition-skewed states.
                comp_cap = species[animal] + npv_ceiling - herd_total
            if species[animal] >= comp_cap:
                continue
            if day > ANIMAL_BUY_LAST_DAY[animal] \
                    + _plan_knob("animal_buy_last_day_shift", 0):
                continue
            product = ANIMALS[animal]["product"]
            if day >= DEAD_PRICE_FROM_DAY:
                # r4-P2 shop-conditional scale-up: with a shop absorbing the
                # product the m2b 90-floor stands; with ZERO absorption (no
                # shop, center 1/day) the herd only scales at full base
                # price -- never into a market that cannot eat the flow
                demand = _town_daily_demand(town_shops)
                floor = DEAD_PRICE_FLOOR[product] \
                    if demand.get(product, 1) >= 2 \
                    else int(0.95 * BASE_PRICE[product])
                if prices.get(product, BASE_PRICE[product]) < floor:
                    continue  # dead-price freeze (demand-conditioned)
                # branch §5.4 curve dim：投影价替代现货快照——"现在过线、
                # 2 天后跌穿"的线现在就能看见（升级而非替换上面的地板）。
                if not _curve_gate_ok(product, _get(obs, "player", 0),
                                      day, prices):
                    continue
            cost = ANIMALS[animal]["cost"]
            # v10 M-E: price the wallet as the engine will see it after
            # this turn's earlier buys, and keep a post-purchase floor so
            # the dawn hire gate never loses the crew
            wallet = (projected_money if plan.get("wheat_farm")
                      else money) - (0.0 if plan.get("wheat_farm")
                                     else committed_spend)
            reserve_total = reserve + LIQUIDITY_FLOOR
            if wallet < cost + reserve_total:
                continue
            n = min(pace - bought, target - herd_total,
                    comp_cap - species[animal],
                    int((wallet - reserve_total) // cost))
            if npv_ceiling > HERD_CAP:
                demand = _town_daily_demand(town_shops)
                absorption_cap = int(
                    demand.get(product, 1) * ANIMALS[animal]["interval"] // 2)
                n = min(n, absorption_cap - species[animal])
            if n > 0 and _herd_cap_ok:
                n = capacity_batch_limit(n, 2.0)
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                if plan.get("wheat_farm"):
                    projected_money -= n * cost
                reserved_units += 2.0 * n
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
            break   # one species per turn

    # ---- selling: dawn plan owns normal timing; gates are tactical overlays --
    flow = _market_flow(_get(obs, "player", 0), day, prices)
    gate_orders = _market_gates(day, prices, shed, herd_total,
                                town_shops=town_shops, money=money,
                                flow=flow)
    dawn_plan = sell_plan_shadow(_get(obs, "player", 0)) or {}
    plan_lines = dawn_plan.get("lines") or {}
    protected_holds = {item for item, line in plan_lines.items()
                       if line.get("verdict") == "hold"}
    emergency = last_day or shed_count >= 78 or money < 200
    if protected_holds and not emergency:
        gate_orders = [order for order in gate_orders
                       if order[0] != "SELL" or order[1] not in protected_holds]
    orders.extend(gate_orders)
    # 【branch §7.2 / market §2 落地】争议线零囤货 + 卖出计划强制清 +
    # P4 三档抢跑——对门控输出做有界覆盖（只增清仓、不抑制既有卖出）。
    orders.extend(_sell_overrides(obs, farm, private, day, prices, shed,
                                  town_shops, orders, plan))
    # 【MK-3 LIVE】黎明卖出计划批次在计划时点驱动卖出（market §2.1：
    # 计划器为主，三门态降级为战术覆盖——上面 gates/overrides 的卖出
    # 已覆盖的线本回合跳过，批次记已发射）。
    orders.extend(_sell_plan_batches_due(
        obs, day, _get(obs, "hour", 0), shed, orders))
    # 【MK-5 武装】干扰触发器（market §3）：影子记录 + 载体 1（现有
    # 库存倾销，当天/零成本）在确认与三闸通过时发令；触发消除即收手
    # （日复判）。载体 2（萝卜伏击）于 2026-09-04 激进波 C 武装：战略层
    # 跨日钉定目标日后，到点全量倾销胡萝卜（走正常预算截断）；载体 4
    # （镜像产线）为田地分配动作，经 plan.iv4_mirror 在 _field_alloc
    # 落格，无需市场单；载体 3（一次性羊群）保持教义算术否决（15% 容量
    # ≈6 头 < 其暴露闸要求的杀伤量，§6.3）。
    orders.extend(_interference_orders(obs, farm, private, day, prices,
                                       plan))
    orders.extend(_interference_v2_orders(obs, farm, private, day,
                                          plan=plan))
    if last_day:
        # MK-3: drain the L4 d29 DROP->SELL queue (what the executor's
        # liquidation template actually moved into the shed this turn)
        queued_d29 = _D29_SELL_QUEUE.pop(_get(obs, "player", 0), None) or {}
        for item in sorted(queued_d29):
            n = queued_d29[item]
            shed_n = shed.get(item, 0)
            if isinstance(shed_n, (int, float)) and shed_n > 0 and n > 0:
                orders.append(["SELL", item, min(int(n), int(shed_n))])
        # Goods already carried can DROP before market processing in this turn,
        # so include them in liquidation. Failed/partial quantities remain legal
        # positive orders and simply commit up to actual shed availability.
        carried = {}
        for inv in (_get(private, "inventories", []) or []):
            for item, n in (inv or {}).items():
                if isinstance(n, (int, float)) and n > 0:
                    carried[item] = carried.get(item, 0) + n
        indexed = {order[1]: order for order in orders if order[0] == "SELL"}
        for item, n in carried.items():
            if item not in BASE_PRICE:
                continue
            if item in indexed:
                indexed[item][2] += n
            else:
                order = ["SELL", item, n]
                orders.append(order)
                indexed[item] = order
    # wheat: log glut curve; sell the surplus above the feed reserve at a
    # real bid (WHEAT_SELL_GATE), under the m2b pressure/late fallbacks
    if not last_day:
        reserve_w = animals_to_feed + WHEAT_FEED_RESERVE
        surplus = shed.get("WHEAT", 0) - reserve_w
        wheat_px = prices.get("WHEAT", 25)
        if surplus > 0 and (wheat_px >= WHEAT_SELL_GATE
                            or shed_count >= 70 or day >= 26
                            or (money < 1000 and wheat_px >= 20)):
            # money < 1000: cash-flow fallback -- the gate must never starve
            # the land/animal capex plan (measured: 42 wheat hoarded at $516
            # while the NE purchase window lapsed)
            orders.append(["SELL", "WHEAT", surplus])
    # Merge overlapping SELL overlays before the official ten-order budget.
    # Each item is emitted once and never exceeds the currently observed shed.
    merged = []
    sell_index = {}
    for order in orders:
        if not isinstance(order, list) or not order:
            continue
        if order[0] != "SELL" or len(order) < 3:
            merged.append(order)
            continue
        item = order[1]
        if item not in BASE_PRICE:
            continue
        qty = max(0, int(order[2] or 0))
        if item not in sell_index:
            sell_index[item] = len(merged)
            merged_order = ["SELL", item, qty]
            merged.append(merged_order)
            _remap_sell_order_source(order, merged_order)
        else:
            merged_order = merged[sell_index[item]]
            merged_order[2] += qty
            _remap_sell_order_source(order, merged_order)
    for item, idx in sell_index.items():
        stock = shed.get(item, 0)
        cap = int(stock) if isinstance(stock, (int, float)) and stock > 0 else 0
        merged[idx][2] = min(merged[idx][2], cap)
    return [order for order in merged
            if order[0] != "SELL" or order[2] > 0]
