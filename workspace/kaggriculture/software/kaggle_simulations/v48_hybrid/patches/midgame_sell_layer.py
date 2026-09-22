# -*- coding: utf-8 -*-
"""v48 混合候选（方案甲）P1 补丁叶：中期卖出层 v2（只补发收窄版）。

── v1→v2 变更登记（F3 h2h 0-16 FAIL 根因修复）─────────────────────────
根因（gates/gates_report.json 2026-09-22 批次）：v1 自 step24（d1）起接管
中期卖单，"囤→压制"规则压制了剧本承重卖单（d6 羊毛 flush / d10 瓜
flush×48 的点火资本序列）→ 终局 19-24k vs 基底 127-178k；h2h 对 v48
W0-L16、panel 全局 ratio 0.315。v2 变更（全部硬约束，逐条对应修复契约）：
  1. 剧本卖单不可触碰：tape 已排程的 SELL 单一律原样透传——不压制、
     不推迟、不改量（v1 的"囤判据→压制"分支删除）；含未来 N=3 天内有
     tape 卖单的产线也视为"承重线"不补发（供给曲线连坐：我的加卖会压
     剧本后续 flush 的价格）。
  2. 接管窗收窄到 d13+：v1 的 step<24 让位改为 day<13（最后点火 flush
     d10-12 之后，d13 前一律透传）。
  3. 只补发：仅对"tape 本步未卖且未来 N 天也无 tape 卖单"的清线
     （投影判定价≤清线）补发小额卖单，量=min(库存, 吸收表日帽,
     保守上限 supplement_qty_cap=6)；v1 的破产生命线倾销（替换式，违反
     本轮契约第 1 条）与流动性 tranche（囤态也发，违反第 3 条"仅清线"）
     两分支整体删除，登记为 v1 遗产。
  4. 反克隆/终局/d26+ 倾销段仲裁让位规则原样保留；fail-safe 与纯函数
     形态保留；P2/P3 补丁不动。接线层副作用的如实登记：统一让位探针
     （build.py `_v48h_native_sell_frame`）即本模块 should_defer_to_tape，
     故 P3 在 d0-12 也随窗让位（v1 为 step<24；F3 实测 P3 有效触发恒 0，
     该收窄无已观测行为差异）。

── 取材登记（全部只读，v1 登记原样保留）───────────────────────────────
语义源（我方旧树，只读取材、独立改写，不 import 旧树）：
  * software/kaggle_simulations/agent/src/market.py
      - _town_daily_demand（L53-73）   → 吸收表：商铺每 4 步抽一次（6 次/日，
        单产品店每次 2 件、多产品店每件 1 件）+ 镇中心每件非肥料品 1 件/日。
      - _shape_val/_price_at_offset/_offset_from_price/_project_price
        （L545-609）                   → 官方 1.32.7 嵌入曲线的投影数学。
      - _sell_plan_item（L851-867）    → 囤/清判据：价≤1 清；投影<现价（曲线
        在死）清；投影<现价×HOLD_EDGE(1.05) 清；否则囤。
      - _sell_plan_dawn（L1026-1162）  → 批次拆分规则：日量=min(供给,吸收)、
        批次按 SELL_PLAN_HOURS=(6,12,18) 拆、卖出行数≤4、计划时点发射。
  * software/kaggle_simulations/agent/src/constants.py（L45-67, L584-597）
      → BASE_PRICE / SHOPS / SHOP_DRAWS_PER_DAY=6 / CENTER_DRAWS_PER_DAY=1 /
        MARKET_PARAMS_EMB / MARKET_I0_EMB=10000 / HINGE_GAIN_EMB=8.0 /
        PRICE_FLOOR_EMB=1 / SELL_PLAN_HOLD_EDGE=1.05 /
        SELL_PLAN_LOOKAHEAD_DAYS=2（官方曲线表 99/99 校验镜像，逐值誊抄）。
基底（只读参照，不 import）：
  * software/kaggle_simulations/v48_derivative/main.py —— 卖单流=剧本回放 →
    v22/policy_library 槽位重排 → gold_floor 反克隆抢卖（clone_active_start=160,
    L1202 配置）→ v19_terminal 717-718 终局两步机。
架构图：references/digests/public-bot-reverse-eng-20260920.md（§1.2/§1.3/§4）。

── tape 卖单日历（承重线判定的数据源，v2 新增）────────────────────────
基底 `_V48_ROUTES`（main.py 内嵌 b85|zlib blob）含 6 个路由变体
（default/farm_fast/yarn_fast/yarn_second/yarn_third/bakery_capital），每变体
719 步逐动作表。本模块无法在纯函数形态下预知运行时实际走哪条路由（路由
选择依赖 gold_floor 分支条件），故取**六变体并集**作为 tape 卖单日历——
并集是任意实际路由卖单日集合的超集，"有 tape 卖单"判定恒保守（宁可少补
发，不误伤任何变体的承重 flush）。推导脚本与本表一致性由
test_midgame_sell_layer.py::test_tape_sell_days_matches_base_routes
从基底文件现场重推导复核。并集日历（day，day=step//24）：
    WHEAT       d5,9,17,21,24-29        MILK        d12-29（连续）
    WOOL        d6,9,10,12-29（连续）   STRAWBERRY  d13-29（连续）
    MELON       d10,11,21-25,28         CARROT      d14-19,29
    FERTILIZER  d1-3,5-29（近逐日）     EGG/TOMATO  全程无 tape 卖单
可见 d13-25 接管窗内的真实空窗极窄：MELON d13-17、WHEAT d13-16、
CARROT d20-25、EGG 任意日（tmp/probe_v2_opportunities.py 实测：纯 v48
轨迹上仅 WHEAT d13 空窗出现库存>0，3 种子×双席共 6 批、估收 ~2.8k）。
N=3 的依据：覆盖并集日历上相邻 tape 卖单的最大常态间隔对（WHEAT 13→17
隔 4 天、CARROT 19→29 隔 10 天按 d26+ 让位截断），3 天前瞻使 d13 的补发
距 WHEAT 下一次 tape 卖（d17）≥4 天，供给曲线在 flush 前有整段吸收窗。

── 集成缝说明（F2 assembler 注入点，v1 原样）───────────────────────────
窄缝 = 基底 main.py 的 agent()：捕获 _policy_out = _V48_POLICY(...)，在
既有 try 块内、return 之前插入
    _policy_out["market"] = apply_to_market_orders(obs, _policy_out["market"])
基底 except 兜底不动，本模块任何异常在该兜底之前就已回退剧本默认卖单。

── 仲裁与回退规则（v2 显式）────────────────────────────────────────────
v48 原生优先，以下帧直接原样返回 tape_default_sells（逐条拷贝，不改内容）：
  1. 终局帧：step >= 717（v19_terminal 717-718 两步机）。
  2. 终局倾销段：day >= 26（v48 剧本 d26-29 集中倾销节奏原生优先）。
  3. 反克隆抢卖激活帧（可观部分）：step >= clone_active_start(160) 且当前
     双方公开农场签名距离 ≤ 2.0（v19_terminal:L177-187 clone_distance 的
     单帧可观代理）。24 步 streak 锁存观测不可得，对整个 step≥160 窗口
     采用"当前近克隆即让位"的保守代理。
  4. 未激活帧：day < 13（v2：最后点火 flush d10-12 之后才接管；v1 的
     step<24 判定废除）。
fail-safe：计划器任何异常（含观测缺字段/类型坏值）→ 返回 tape_default_sells。

接管语义（激活帧内，PLANNER_ITEMS 七线不变；FERTILIZER/TOMATO 不在接管面）：
  * tape 本帧 SELL 单一律透传（v48 原生节奏优先——含 d6 毛/d10 瓜点火
    波次；v1 的囤态压制分支已删除）；
  * 承重线不补发：item 在 TAPE_SELL_DAYS 并集中 [day, day+N] 内有任一
    tape 卖单日 → 跳过（N=tape_lookahead_days=3；供给曲线连坐）；
  * 只补发：tape 本帧未卖该线 且 未来 N 天无 tape 卖单 且 投影判据=清
    且 库存>0 → 补发量 = min(库存, 吸收表日帽, supplement_qty_cap=6)，
    按 (6,12,18) 时点整点拆批发射（同线每帧至多一批），最多 4 条清仓线。
    保守上限 6 的取值依据：与 v1 C_liquidity tranche=6 同口径、低于
    gold_floor clone_maximum_batch=10，单线单日补发不超过城镇约半日吸收
    （单产品店日吸收 13），对后续 tape flush 的价格挤压最小。

与 market.py 的刻意偏差（纯函数化代价，均登记）：
  * 价格流 EMA（_market_flow）有状态 → 依赖注入 observation["flow"]（缺省
    0.0 = 投影持平，判据自然落"清"侧保守——v2 下仅影响空窗线是否补发）；
  * 防御姿态 streak 记忆与囤货上下限未移植（v2 不再有压制分支，囤/清
    判据只用于补发门）；
  * 批次发射"计划时点整点发射"（无状态确定性，R5），错过的时点视为
    该批当日放弃。
"""

import math

# ---- 常量（自 constants.py 逐值誊抄；独立 stdlib 模块，不 import 旧树）----
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
              "FERTILIZER": 100}
SHOPS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
SHOP_DRAWS_PER_DAY = 6      # 24 / townShopSellInterval 4
CENTER_DRAWS_PER_DAY = 1    # 24 / townCenterSellInterval 24
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
HINGE_GAIN_EMB = 8.0
PRICE_FLOOR_EMB = 1

# 三门计划器接管面（FERTILIZER 走剧本日结现金流、TOMATO 无产出线，
# 均不接管）。
PLANNER_ITEMS = ("STRAWBERRY", "MELON", "WOOL", "MILK", "CARROT", "EGG",
                 "WHEAT")

# tape 卖单日历：基底 _V48_ROUTES 六路由变体的 SELL 单 day 并集（day=
# step//24）。推导：解 b85|zlib blob → 逐变体扫 market SELL → 按品并集。
# 一致性复核：test_midgame_sell_layer.py 从基底文件现场重推导逐值断言。
TAPE_SELL_DAYS = {
    "FERTILIZER": (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                   18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29),
    "WHEAT":      (5, 9, 17, 21, 24, 25, 26, 27, 28, 29),
    "WOOL":       (6, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                   24, 25, 26, 27, 28, 29),
    "MELON":      (10, 11, 21, 22, 23, 24, 25, 28),
    "MILK":       (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                   26, 27, 28, 29),
    "STRAWBERRY": (13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                   27, 28, 29),
    "CARROT":     (14, 15, 16, 17, 18, 19, 29),
    "EGG":        (),
    "TOMATO":     (),
}

DEFAULT_CONFIG = {
    "steps_per_day": 24,
    "midgame_start_day": 13,     # v2：d13 起接管（d0-12 一律透传）
    "tape_lookahead_days": 3,    # v2：承重线前瞻窗 N（见模块头推导）
    "supplement_qty_cap": 6,     # v2：单线单帧补发保守上限（见模块头依据）
    "endgame_defer_day": 26,     # v48 d26-29 倾销段原生优先
    "terminal_step_start": 717,  # v19_terminal 717-718 两步机
    "clone_active_start": 160,   # gold_floor CloneSellPreemption 激活步
    "clone_distance_threshold": 2.0,
    "sell_plan_hours": (6, 12, 18),
    "max_clear_lines": 4,        # SELL_PLAN_MAX_LINES
    "lookahead_days": 2,         # SELL_PLAN_LOOKAHEAD_DAYS
    "hold_edge": 1.05,           # SELL_PLAN_HOLD_EDGE
}


# ---- 观测提取（依赖注入式：平面键与嵌套 kaggle 形态皆可）----------------
def _get(obj, key, default=None):
    try:
        return obj.get(key, default)
    except AttributeError:
        return default


def _extract(observation, cfg):
    """归一化观测；棚仓信息整体缺失时返回 None（fail-safe 透传剧本）。"""
    obs = observation if isinstance(observation, dict) else {}
    step = int(_get(obs, "step", 0))
    hour = step % int(cfg["steps_per_day"])
    day = step // int(cfg["steps_per_day"])

    market = _get(obs, "market", {}) or {}
    prices = _get(obs, "prices", None)
    if not isinstance(prices, dict):
        prices = _get(market, "prices", {}) or {}
    town = _get(obs, "town", {}) or {}
    shops = _get(obs, "unlocked_shops", None)
    if shops is None:
        shops = _get(town, "unlocked_shops", None)

    if "shed" in obs:
        shed = _get(obs, "shed", {}) or {}
    else:
        private = _get(obs, "private", {}) or {}
        shed = _get(private, "shed", None)
        if shed is None:
            return None           # 无库存视图 → 不接管
    flow = _get(obs, "flow", None)
    if not isinstance(flow, dict):
        flow = {}

    player = int(_get(obs, "player", 0) or 0)
    farms = _get(obs, "farms", None)
    money = _get(obs, "money", None)
    if money is None and isinstance(farms, list) and 0 <= player < len(farms):
        money = _get(farms[player] or {}, "money", None)

    return {"step": step, "day": day, "hour": hour, "prices": prices,
            "shed": shed, "shops": shops, "flow": flow, "money": money,
            "farms": farms if isinstance(farms, list) else None,
            "obs": obs}


# ---- 反克隆可观代理（v19_terminal:L177-187 的单帧版本）------------------
def _farm_signature(farm):
    hands = len(_get(farm, "hands", []) or [])
    quadrants = _get(farm, "quadrants_owned",
                     _get(farm, "quadrants", 1)) or 1
    counts = {}
    for row in _get(farm, "tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            animal = _get(tile, "animal", "") or ""
            if animal:
                key = "ANIMAL:" + str(animal)
            else:
                key = str(_get(tile, "kind", "") or "EMPTY")
            counts[key] = counts.get(key, 0) + 1
    return int(hands), int(quadrants), counts


def clone_distance(observation):
    """双方公开农场签名距离（可观代理）：|手数差|+3×|象限差|+Σ|逐类地块差|。

    不可观（无双方农场）时返回正无穷（判不出近克隆 → 不触发该条仲裁）。
    """
    obs = observation if isinstance(observation, dict) else {}
    player = int(_get(obs, "player", 0) or 0)
    farms = _get(obs, "farms", None)
    if not isinstance(farms, list) or len(farms) < 2:
        return float("inf")
    sigs = [_farm_signature(f) for f in farms[:2] if f is not None]
    if len(sigs) < 2:
        return float("inf")
    (h0, q0, c0), (h1, q1, c1) = sigs
    dist = abs(h0 - h1) + 3 * abs(q0 - q1)
    for key in set(c0) | set(c1):
        dist += abs(c0.get(key, 0) - c1.get(key, 0))
    return float(dist)


# ---- 仲裁（v48 原生优先帧判定）------------------------------------------
def should_defer_to_tape(observation, config=None):
    """终局帧 / 终局倾销段 / 反克隆激活帧 / 未激活帧（day<13）→ True。"""
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(config or {})
    ctx = _extract(observation, cfg)
    step = ctx["step"] if ctx else int(_get(observation
                                            if isinstance(observation, dict)
                                            else {}, "step", 0))
    day = ctx["day"] if ctx else step // int(cfg["steps_per_day"])
    if day < int(cfg["midgame_start_day"]):     # v2：d<13 一律透传
        return True
    if step >= int(cfg["terminal_step_start"]):
        return True
    if day >= int(cfg["endgame_defer_day"]):
        return True
    if step >= int(cfg["clone_active_start"]):
        obs = observation if isinstance(observation, dict) else {}
        if clone_distance(obs) <= float(cfg["clone_distance_threshold"]):
            return True
    return False


# ---- 曲线数学（market.py L545-609 逐段改写）-----------------------------
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
    """E[R_future]：价格在 I0+off+flow×horizon 处的曲线值（解析投影）。"""
    off = _offset_from_price(item, price_now)
    return _price_at_offset(item, off + flow * horizon)


# ---- 三门语义核心 --------------------------------------------------------
def _town_daily_demand(unlocked_shops):
    """吸收表：每件商品城镇日吸收量（market.py L53-73 逐段改写）。"""
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


def _verdict(item, ctx, cfg):
    """囤/清判据（_sell_plan_item 语义；flow 缺省 0 → 投影持平 → 偏清）。"""
    price = _get(ctx["prices"], item, BASE_PRICE.get(item, 0))
    try:
        price = float(price)
    except (TypeError, ValueError):
        raise
    if price <= 1:
        return "clear"          # 地板段：没有任何可等的
    flow = float(_get(ctx["flow"], item, 0.0) or 0.0)
    proj = project_price(item, price, flow, float(cfg["lookahead_days"]))
    if proj < price:
        return "clear"          # 曲线在死（投影低于现价）
    if proj < price * float(cfg["hold_edge"]):
        return "clear"          # 囤的边际不足
    return "hold"


def tape_sells_within(item, day, horizon, config=None):
    """承重线判定：item 在 [day, day+horizon] 内是否有任一 tape 卖单日。

    日历取 TAPE_SELL_DAYS（六路由变体并集，见模块头）。含当日（day 本身）
    ——tape 若当日稍后步有卖单，同样属承重线（day 粒度不可分辨步）。
    """
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(config or {})
    horizon = int(horizon if horizon is not None
                  else cfg["tape_lookahead_days"])
    for d in TAPE_SELL_DAYS.get(item, ()):
        if day <= d <= day + horizon:
            return True
    return False


def _plan(ctx, tape_sells, cfg):
    """激活帧的接管主体（v2 只补发）：tape 全透传 + 空窗清线小额补发。"""
    keep = [list(order) for order in tape_sells]      # 剧本卖单一律透传
    sold_now = {order[1] for order in tape_sells}

    day = ctx["day"]
    horizon = int(cfg["tape_lookahead_days"])
    cap = int(cfg["supplement_qty_cap"])
    if isinstance(ctx["shops"], list):
        absorption = _town_daily_demand(ctx["shops"])
    else:
        absorption = None

    lines = []
    for item in PLANNER_ITEMS:
        if item in sold_now:                          # tape 本步已卖该线
            continue
        if tape_sells_within(item, day, horizon):     # 承重线：连坐不补发
            continue
        stock = _get(ctx["shed"], item, 0)
        if not isinstance(stock, (int, float)) or stock <= 0:
            continue
        if _verdict(item, ctx, cfg) != "clear":       # 只补发清线
            continue
        absorb = absorption.get(item, 1) if absorption else 1
        qty = min(int(stock), max(1, int(absorb)), cap)
        lines.append((item, qty))
    lines.sort(key=lambda kv: (-kv[1], kv[0]))

    hours = tuple(cfg["sell_plan_hours"])
    emits = []
    for item, qty in lines[:int(cfg["max_clear_lines"])]:
        slots = min(len(hours), qty)
        quotient, remainder = divmod(qty, slots)
        batches = [quotient + (1 if i < remainder else 0)
                   for i in range(slots)]
        for i, n in enumerate(batches):
            if n > 0 and i < len(hours) and hours[i] == ctx["hour"]:
                emits.append(["SELL", item, n])
                break               # 每线每帧至多一批（计划时点发射）
    return keep + emits


# ---- 入口（fail-safe 总兜底）---------------------------------------------
def _normalize_tape(tape_default_sells):
    out = []
    for order in tape_default_sells or []:
        if isinstance(order, (list, tuple)) and len(order) >= 3 \
                and order[0] == "SELL":
            out.append(["SELL", order[1], order[2]])
    return out


def plan_midgame_sells(observation, tape_default_sells, config=None):
    """按 v2 只补发语义产出本帧中期卖单。

    输入：observation = {step, prices, shed, money, unlocked_shops[, flow,
           farms, player]}（平面键或 kaggle 嵌套形态皆可）；
           tape_default_sells = 剧本默认卖单 [["SELL", item, qty], ...]。
    输出：本帧卖单列表（新对象，不改入参）= tape 透传 + 空窗清线补发。
    回退：仲裁帧 / 无库存视图 / 任何异常 → 原样返回 tape_default_sells。
    """
    try:
        sells = _normalize_tape(tape_default_sells)
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(config or {})
        if should_defer_to_tape(observation, cfg):
            return sells
        ctx = _extract(observation, cfg)
        if ctx is None:
            return sells
        return _plan(ctx, sells, cfg)
    except Exception:
        return _normalize_tape(tape_default_sells)


def apply_to_market_orders(observation, market_orders, config=None):
    """集成缝助手：对整张 market 单列表做接管（非 SELL 单原位保留）。

    供 assembler 在基底 agent() 返回前一行注入：
        out["market"] = apply_to_market_orders(obs, out["market"])
    """
    try:
        keeps, sells = [], []
        for order in market_orders or []:
            if isinstance(order, (list, tuple)) and order and \
                    order[0] == "SELL":
                sells.append(list(order))
            else:
                keeps.append(order)
        planned = plan_midgame_sells(observation, sells, config)
        return keeps + planned
    except Exception:
        return list(market_orders or [])
