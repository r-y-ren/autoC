# -*- coding: utf-8 -*-
"""终局保果层（lead-protection，R8-v2，P4 家族）——双条件并集触发启用保守卖时锁胜：
【day>=15 且峰回撤 peak-lead>=2000 且 lead>=1500】 ∪ 【day>=24 且 lead>=3000】（v1 原条件）。
不触发形态与 v4b 逐字节一致（未触发=原对象返回）；注入缝=卖单干预（P1 先例）；基底五区零改动
（717-718 清仓脚本本体不动，只在 step<717 内调整卖时/卖量）；fail-safe：任何异常回退原卖单。
战后资产：只构建+离线验证，不上线（零提交冻结 ba1b44c）。
上游: R8-v2（详见 fn_docs/responsibility.md 增补段，2026-09-22 F5 修订）。

── 实现期口径登记（2026-09-22，F4a）──────────────────────────────────────
0. 前置事实一（对手资金可见性；引擎探针 tmp/probe_r8_obs_keys.py：
   kaggle_environments 1.32.7 "kaggriculture" 720 步双席全程实测）：obs 顶层键
   = day/farms/hour/market/player/private/remainingOverageTime/step/town；
   obs.farms 为双席数组，每席 {money, tiles, hands, farmer,
   unlocked_quadrants, hires_today}，**money 双席互见**（双席各自观测均含
   对方 money）⇒ 对手资金可得，estimate 走直读口径。
1. estimate 口径（返回 basis 三态）：
   * "farms_money_direct"（主口径）：lead = farms[me].money −
     farms[opp].money。与 R8 动机语料 fn_docs/results/
     2026-09-24-loss-timelines.json 的 margin 口径（farms money 差）同源。
   * "money_shed_proxy"（降级口径；真引擎不可达，仅为残缺观测防御）：
     任一席 money 不可读时——
       my_capital  = me_money(缺 0) + Σ my_shed[item]×price[item]
                     （我方资金+库存估值；价格取 obs.market.prices，缺项
                       回退 BASE_PRICE）
       opp_capital = opp_money(缺 0) + Σ_对手动物地块 BASE_PRICE[product]
                     / interval × days_left（对手产出代理；动物→产品/产距
                     誊抄自旧树 agent/src/constants.py L40-44：GOOSE→EGG/1、
                     COW→MILK/2、SHEEP→WOOL/3；days_left=30−day，连续口径
                     不取整）
     盲区登记：对手 shed（private 不可观）与在田作物不在代理内 → 对手侧
     下界 → lead 上偏（更易触发）；由 day≥24+lead≥3000 双门槛兜住，且该
     分支在真引擎（money 互见）不可达。
   * "unobservable"：双侧任何信号（money/shed/动物地块）全缺 → lead=None
     （视为未触发）。
2. 引擎卖单事实（twin 场景源 exports/probes/twin_fidelity/engine_cache/
   kaggriculture.py _process_market/_commit_unit 实读，2026-09-22）：SELL
   逐件**当步全额成交**（无成交风险），但每成交 1 件市场库存 +1、下一件
   报价单调下降（$1 地板件不再增库存）——大单倾倒的代价是价格而非成交；
   城镇吸收（商铺每 townShopSellInterval=4 步、镇中心每日）在步间恢复
   库存与价格。故"确保成交"的落地语义 = **按吸收节奏分批前移锁价**（防
   对手倾倒压塌我方后期卖价），而非对冲流动性不足。
3. plan 语义（触发帧内，纯函数无状态，跨时点经库存复发自然拆批）：
   * 透传：现有卖单一律原样保留（不删单不改量——F3 教训：v1 压制剧本
     承重卖单致 h2h 0-16 的失败类不再犯）。
   * 前移补发：仅保护时点 protective_hours=(6,12,18)（P1 SELL_PLAN_HOURS
     同款）发射；单线单帧量 ≤ split_qty_cap=4（单线日保护发射 3×4=12 ≤
     城镇日吸收下界 13 = 单产品店 6 抽×2 + 镇中心 1，自身压价最小化）；
     单帧补发线数 ≤ max_protect_lines=4（发射后单帧市单总数 ≤ 4+4=8 <
     引擎 maxMarketOrdersPerTurn=10）。
   * 投影门：价格投影输入形 {item: (p_now, p_future)}——p_future < p_now
     （曲线在跌，含对手倾倒形态）的线在**任意**保护时点尽早卖；p_future
     ≥ p_now（含无投影线）的线只在**当日末保护时点 18** 卖（日内锁定，
     不放弃稳定曲线的日内恢复）。
   * 让位：step ≥ terminal_step_start(717)（v19_terminal 717-718 两步
     清仓机）或 step 不可知（None）→ 不动任何单，原对象返回；本帧 tape
     已在卖的线不补发（同帧加卖只会把自己的成交价压得更低）。
   * build 侧投影构造：p_future = P1 同款官方曲线投影（
     MARKET_PARAMS_EMB 逐值誊抄），流量取市场过剩代理 glut_flow =
     min(flow_cap=1.0, max(0.0, (market.inventory[item] − MARKET_I0_EMB)
     / MARKET_I0_EMB))，horizon=projection_horizon_days=2 天——对手倾倒
     → 市场库存升 → glut_flow>0 → 投影下移 → 尽早卖（market.inventory
     双席公开，前置事实一证实）。已知近似（继承 P1 反解数学）：hinge 侧
     （CARROT/TOMATO/EGG）基价上方一带 y<0.96875 时 _offset_from_price
     取钳位解，roundtrip 有偏 → 该带内 falling 误判可能；影响仅限补发
     在日内哪个保护时点（h6/12 vs h18），不改变是否补发与量帽。
4. 触发形态（requirements R8 原文）：day≥24 且 lead≥3000（等值即触发）。
5. fail-safe：estimate 任何异常 → {"lead": None, "basis": "error"}（=未
   触发）；plan/build 任何异常 → 原对象返回（identity）。
6. 签名微调登记（对责任文档"签名意图"）：plan_protective_sells 增补
   keyword 参 step（717 让位判定）与 config；estimate_lead_margin 的
   day 参与降级代理剩余天数（主口径不使用）；build_lead_protection 的
   day 允许 None（缺省按 obs.step//24 回推）；其余形参不变。

── R8-v2 修订登记（2026-09-22，F5——判决实验：触发设计修订+双臂对照）────
0. 修订动机（v1 判决 FAIL 0/14 的尸检，gates/out/lead_protection_verdict.json）：
   语料 14 局峰值日分布 d6-d26，其中 9 局峰值日在 d17 以前——v1 触发面
   （day≥24 且 lead≥3000）在崩塌已完成后才可能在场，6 局重演遥测
   form_present_calls==0（P4 从未触发，重演 margin 与原局几乎逐位相同）。
   结论：触发过晚=杠杆未上膛。v2 把触发前移到"仍在领先但已从峰值回撤"
   的形态，并以双臂对照门直测杠杆符号。
1. 触发形态 v2（双条件并集，任一满足即 armed）：
   * 臂 A（回撤臂，新）：day≥15 且 峰回撤 peak−lead≥2000 且 lead≥1500
     （三槛等值即触发）——语义="仍领先 ≥1500 但已从运行峰值跌落 ≥2000"，
     即领先崩塌进行时（语料各局峰值日后的典型形态）。
   * 臂 B（原 v1 条件，保留）：day≥24 且 lead≥3000。
2. 峰值运行寄存器（臂 A 的跨回合状态）：dict {"peak_lead": float|None}，
   **编排处持有、经入参注入**（build 侧 register= 装配接线
   _V48H_P4_REGISTER，模块级 dict，每席每局独立装载天然隔离——P2 模块级
   streak 先例）；本模块保持纯函数：无模块级可变状态、无全局，寄存器与
   config 一律经参数传入。更新规则：lead 可估帧（不分早晚日）先并入寄存器
   peak=max(peak, lead) 再算回撤（新峰帧回撤=0，臂 A 不触发——语义正确：
   峰值帧无回撤）；寄存器 dict 原位更新（调用方引用即可跨回合续读）。
   register=None（缺省）→ 每次调用新建局部临时寄存器 → 峰=当前 lead →
   回撤恒 0 → 臂 A 恒不触发 → 并集退化为臂 B（v1 行为逐位保持，未传
   寄存器的既有调用零破坏——fail-safe 缺省）。
3. 签名变更登记（v2，对责任文档"签名意图"）：
   * build_lead_protection(observation, day, current_sells, config=None,
     register=None)——增补 keyword 参 config 与 register（峰值寄存器）。
   * plan_protective_sells(..., armed=False)——增补 keyword 参 armed：
     armed=True 时跳过 plan 内 lead≥trigger_lead_min 防御门（触发判定已由
     编排入口的并集完成；臂 A 触发时 lead 可低至 1500<3000）；armed=False
     （缺省）保持 v1 防御门（独立调用 plan 的既有用法零破坏）。
4. 逐帧成本登记：v2 的 estimate 在全部可观帧执行（峰跟踪不分早晚日），
   v1 仅 day≥24 帧调用——直接口径（双席 money 直读）为 O(1) 字段访问，
   无实质成本；plan 仍仅在 armed 帧后的保护时点（6/12/18）发射。
"""

import math

# ---- 常量（自 constants.py / P1 补丁叶逐值誊抄；独立 stdlib 模块）----------
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
              "FERTILIZER": 100}
MARKET_PARAMS_EMB = {   # item: (base, T, below_f, below_t, above_f, above_t)
    "WHEAT":      (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT":     (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO":     (60, 200, "hinge", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON":      (250, 300, "log", 0.20, "sq", 3.60),
    "EGG":        (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK":       (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL":       (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
MARKET_I0_EMB = 10000
PRICE_FLOOR_EMB = 1

# 对手产出代理用：动物 → (产品, 产距天)（constants.py L40-44 逐值誊抄）
ANIMAL_PRODUCT_INTERVAL = {"GOOSE": ("EGG", 1), "COW": ("MILK", 2),
                           "SHEEP": ("WOOL", 3)}

DEFAULT_CONFIG = {
    "steps_per_day": 24,
    # -- R8-v2 触发面（双条件并集，任一满足即 armed）------------------------
    "trigger_day_min": 24,        # 臂 B（v1 原条件）：day>=24 触发
    "trigger_lead_min": 3000.0,   # 臂 B：lead>=3000 触发（等值即触发）
    "trigger_day_min_drawdown": 15,     # 臂 A（回撤臂）：day>=15 触发
    "trigger_drawdown_min": 2000.0,     # 臂 A：峰回撤 peak-lead>=2000
    "trigger_lead_min_drawdown": 1500.0,   # 臂 A：lead>=1500（仍领先）
    # ----------------------------------------------------------------------
    "terminal_step_start": 717,   # v19_terminal 717-718 两步清仓机（让位）
    "protective_hours": (6, 12, 18),   # P1 SELL_PLAN_HOURS 同款
    "last_protective_hour": 18,   # 稳定线只发当日末保护时点
    "split_qty_cap": 4,           # 单线单帧补发量帽（日 12 ≤ 吸收下界 13）
    "max_protect_lines": 4,       # 单帧补发线数帽（市单总数 ≤8<10）
    "projection_horizon_days": 2,   # P1 SELL_PLAN_LOOKAHEAD_DAYS 同款
    "projection_flow_cap": 1.0,     # glut_flow 上限
    "season_days": 30,              # days_left = season_days - day
}


# ---- 观测提取小件（P1 同款依赖注入式）------------------------------------
def _get(obj, key, default=None):
    try:
        return obj.get(key, default)
    except AttributeError:
        return default


def _num(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _farm_money(farms, seat):
    if not isinstance(farms, list) or not 0 <= seat < len(farms):
        return None
    return _num(_get(farms[seat] or {}, "money"))


# ---- 曲线数学（market.py L545-609 / P1 补丁叶逐段誊抄）--------------------
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
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _price_at_offset(item, off):
    base, T, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    if off < 0:
        amp = bt * base / max(_shape_val(bf, T, T), 1e-9)
        p = base + amp * _shape_val(bf, -off, T)
    else:
        amp = at * base / max(_shape_val(af, T, T), 1e-9)
        p = base - amp * _shape_val(af, off, T)
    return max(float(PRICE_FLOOR_EMB), p)


def _offset_from_price(item, price):
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


def project_price(item, price_now, flow, horizon):
    """E[R_future]：价格在 I0+off+flow×horizon 处的曲线值（P1 同款投影）。"""
    off = _offset_from_price(item, price_now)
    return _price_at_offset(item, off + flow * horizon)


# ---- 对手产出代理（降级口径专用）-----------------------------------------
def _opp_animal_flow_value(farms, seat, days_left, cfg):
    """对手可见动物地块的未来产出估值：Σ BASE_PRICE[product]/interval ×
    days_left（连续口径；对手 shed/在田作物不可观，登记为对手侧下界）。"""
    if not isinstance(farms, list) or not 0 <= seat < len(farms):
        return 0.0
    total = 0.0
    for row in _get(farms[seat] or {}, "tiles", []) or []:
        for tile in row or []:
            animal = _get(tile or {}, "animal", None) \
                if isinstance(tile, dict) else None
            if animal in ANIMAL_PRODUCT_INTERVAL:
                product, interval = ANIMAL_PRODUCT_INTERVAL[animal]
                price = float(BASE_PRICE.get(product, 0))
                total += price / float(interval) * float(days_left)
    return total


# ---------------------------------------------------------------------------
# ① 领先差估计
# ---------------------------------------------------------------------------
def estimate_lead_margin(observation, day):
    """领先差计算（口径登记见模块头）：主口径直读双席 money；降级代理
    我方资金+库存估值 vs 对手资金+动物产出代理；不可估 lead=None。

    输入: 回合观测 + day / 输出: {"lead": float|None, "basis": str} /
    错误: 任何异常吞掉 → {"lead": None, "basis": "error"}（=未触发）。
    """
    try:
        obs = observation if isinstance(observation, dict) else {}
        cfg = DEFAULT_CONFIG
        player = int(_get(obs, "player", 0) or 0)
        farms = _get(obs, "farms", None)
        me_money = _farm_money(farms, player)
        opp_money = _farm_money(farms, 1 - player)
        if me_money is not None and opp_money is not None:
            return {"lead": me_money - opp_money,
                    "basis": "farms_money_direct"}

        # 降级代理（真引擎不可达；盲区与偏向登记见模块头 1.）
        try:
            day_i = int(day)
        except (TypeError, ValueError):
            day_i = 0
        days_left = max(0, int(cfg["season_days"]) - day_i)

        private = _get(obs, "private", {}) or {}
        shed = _get(obs, "shed", None)
        if not isinstance(shed, dict):
            shed = _get(private, "shed", None)
        market = _get(obs, "market", {}) or {}
        prices = _get(obs, "prices", None)
        if not isinstance(prices, dict):
            prices = _get(market, "prices", {}) or {}

        inv_value = 0.0
        if isinstance(shed, dict):
            for item, qty in shed.items():
                q = _num(qty)
                if q and q > 0:
                    p = _num(_get(prices, item, None))
                    if p is None:
                        p = float(BASE_PRICE.get(item, 0))
                    inv_value += q * p

        animal_value = _opp_animal_flow_value(farms, 1 - player, days_left,
                                              cfg)
        signal = (me_money is not None or opp_money is not None
                  or inv_value > 0.0 or animal_value > 0.0)
        if not signal:
            return {"lead": None, "basis": "unobservable"}
        my_capital = (me_money or 0.0) + inv_value
        opp_capital = (opp_money or 0.0) + animal_value
        return {"lead": my_capital - opp_capital,
                "basis": "money_shed_proxy"}
    except Exception:
        return {"lead": None, "basis": "error"}


# ---------------------------------------------------------------------------
# ② 保守卖时计划
# ---------------------------------------------------------------------------
def _order_is_sell(order, item):
    return (isinstance(order, (list, tuple)) and len(order) >= 3
            and order[0] == "SELL" and order[1] == item)


def plan_protective_sells(inventory, price_projection, current_sells, lead,
                          step=None, config=None, armed=False):
    """保守卖时生成：透传现有卖单 + 保护时点分批前移补发（投影在跌尽早
    卖、稳定线当日末卖）；step>=717 清仓窗让位（不动任何单，原对象返回）；
    异常回退原单。armed=True 跳过 lead 防御门（R8-v2：触发判定已由编排
    入口的并集完成，臂 A 触发时 lead 可低至 1500<3000）；armed=False
    （缺省）保持 v1 防御门 lead>=trigger_lead_min。

    输入: inventory={item:qty} / price_projection={item:(p_now,p_future)} /
    current_sells=当帧卖单 / lead=领先差 / step=当前步（缺省=不可知，让位）
    / armed=触发已由上游判定
    输出: 调整后卖单（无补发=原对象；有补发=新列表，原单引用透传不改动）
    错误: 异常→原对象。
    """
    try:
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(config or {})
        if step is None:
            return current_sells                      # 步不可知 → 让位
        step_i = int(step)
        if step_i >= int(cfg["terminal_step_start"]):
            return current_sells                      # 717-718 清仓窗让位
        if lead is None:
            return current_sells
        lead_f = float(lead)
        if not armed and lead_f < float(cfg["trigger_lead_min"]):
            return current_sells                      # 非触发形态（防御位）

        hour = step_i % int(cfg["steps_per_day"])
        if hour not in tuple(cfg["protective_hours"]):
            return current_sells                      # 非保护时点零足迹

        selling_now = {o[1] for o in (current_sells or [])
                       if isinstance(o, (list, tuple)) and len(o) >= 3
                       and o[0] == "SELL"}
        proj = price_projection if isinstance(price_projection, dict) else {}
        inv = inventory if isinstance(inventory, dict) else {}

        candidates = []
        for item, qty in inv.items():
            if item in selling_now or item not in BASE_PRICE:
                continue
            q = _num(qty)
            if not q or q <= 0:
                continue
            pair = proj.get(item)
            falling = False
            if isinstance(pair, (list, tuple)) and len(pair) >= 2:
                p_now, p_future = _num(pair[0]), _num(pair[1])
                if p_now is not None and p_future is not None:
                    falling = p_future < p_now
            if not falling and hour != int(cfg["last_protective_hour"]):
                continue            # 稳定/无投影线只在当日末保护时点卖
            candidates.append((item, int(q)))
        # 先按原始库存排序（大库存线优先出清），再施拆批帽与线数帽
        candidates.sort(key=lambda kv: (-kv[1], kv[0]))

        emits = [["SELL", item, int(min(q, cfg["split_qty_cap"]))]
                 for item, q in candidates[:int(cfg["max_protect_lines"])]]
        if not emits:
            return current_sells                    # 无补发=零足迹原对象
        return list(current_sells or []) + emits
    except Exception:
        return current_sells


# ---------------------------------------------------------------------------
# ③ 编排入口
# ---------------------------------------------------------------------------
def _build_price_projection(obs, cfg):
    """{item: (p_now, p_future)}：p_now=market.prices；p_future=P1 曲线投影
    + 市场过剩流 glut_flow（对手倾倒→库存升→投影下移；登记见模块头 3.）。"""
    market = _get(obs, "market", {}) or {}
    prices = _get(obs, "prices", None)
    if not isinstance(prices, dict):
        prices = _get(market, "prices", {}) or {}
    inventory = _get(market, "inventory", None)
    if not isinstance(inventory, dict):
        inventory = {}
    horizon = float(cfg["projection_horizon_days"])
    flow_cap = float(cfg["projection_flow_cap"])
    out = {}
    for item, price in prices.items():
        if item not in MARKET_PARAMS_EMB:
            continue
        p_now = _num(price)
        if p_now is None:
            continue
        inv = _num(_get(inventory, item, None))
        base_inv = float(MARKET_I0_EMB)
        flow = 0.0
        if inv is not None and inv > base_inv and base_inv > 0:
            flow = min(flow_cap, (inv - base_inv) / base_inv)
        out[item] = (p_now, project_price(item, p_now, flow, horizon))
    return out


def build_lead_protection(observation, day, current_sells, config=None,
                          register=None):
    """编排入口（R8-v2）：estimate → 峰寄存器更新 → 双条件并集触发判定
    【day>=15 且 peak-lead>=2000 且 lead>=1500】∪【day>=24 且 lead>=3000】
    → plan_protective_sells(armed=True) → 返回；未触发/异常/无补发=原对象
    原样返回。register=编排处持有的峰寄存器 dict（{"peak_lead": float|None}），
    lead 可估帧原位并入 peak=max(peak, lead)；register=None → 局部临时
    寄存器（回撤臂退化，等价 v1 行为）——签名变更登记见模块头 v2 修订段 3.。

    输入: 回合观测（价格/库存/资金/市场库存）+ day（None 则按 obs.step//24
    回推）+ 当日卖单计划 + config（缺省 DEFAULT_CONFIG）+ register（峰寄存器）
    输出: 调整后卖单（未触发=原对象）
    错误: 内部异常吞掉并回退原单。
    """
    try:
        obs = observation if isinstance(observation, dict) else {}
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(config or {})
        step = _get(obs, "step", None)
        if day is None:
            day = step // int(cfg["steps_per_day"]) if isinstance(
                step, (int, float)) and not isinstance(step, bool) else None
        if day is None:
            return current_sells                  # 步不可知（v1 语义保持）
        day_i = int(day)

        est = estimate_lead_margin(obs, day_i)    # v2：全帧估计（峰跟踪）
        lead = est.get("lead") if isinstance(est, dict) else None
        lead_f = float(lead) if lead is not None else None

        # 峰值运行寄存器（编排处持有；不分早晚日并入，先并峰值再算回撤）
        reg = register if isinstance(register, dict) else {}
        peak = _num(reg.get("peak_lead", None))
        if lead_f is not None:
            peak = lead_f if peak is None or lead_f > peak else peak
            reg["peak_lead"] = peak
        drawdown = (peak - lead_f) if (peak is not None
                                       and lead_f is not None) else None

        arm_drawdown = (day_i >= int(cfg["trigger_day_min_drawdown"])
                        and lead_f is not None
                        and lead_f >= float(cfg["trigger_lead_min_drawdown"])
                        and drawdown is not None
                        and drawdown >= float(cfg["trigger_drawdown_min"]))
        arm_d24 = (day_i >= int(cfg["trigger_day_min"])
                   and lead_f is not None
                   and lead_f >= float(cfg["trigger_lead_min"]))
        if not (arm_drawdown or arm_d24):
            return current_sells                  # 未触发=零足迹原对象
        if step is not None and int(step) >= int(cfg["terminal_step_start"]):
            return current_sells                  # 717-718 清仓窗让位

        private = _get(obs, "private", {}) or {}
        shed = _get(obs, "shed", None)
        if not isinstance(shed, dict):
            shed = _get(private, "shed", None)
        if not isinstance(shed, dict):
            return current_sells                  # 无库存视图零足迹
        projection = _build_price_projection(obs, cfg)
        return plan_protective_sells(shed, projection, current_sells, lead,
                                     step=step, config=cfg, armed=True)
    except Exception:
        return current_sells
