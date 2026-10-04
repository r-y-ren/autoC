"""milestone_monitor -- v48 混合候选（方案甲）P3 补丁叶：剧本健康监测（R4）。

独立 stdlib 模块（零 import，不依赖旧树 agent/src、不依赖 v48 基底）。
实现 requirements.md R4：d10-12 窗口资金/库存 vs 剧本预期里程碑比对；
偏离超阈 → **只调整卖单时点**（推迟非紧急卖单），绝不改产线步骤；
未偏离 = 原样返回（零动作，零影响证明钉住）。

==============================================================================
【里程碑预期表】（登记项 1；节奏依据 references/digests/public-bot-reverse-eng-20260920.md
§2.1/§3 的 v48 default 路由逐日表，实抓 2026-08-31，引擎 1.32.7）
==============================================================================
评估窗口：仅 day ∈ [10, 12]（R4 契约窗口；窗口外一律不评估不偏离）。

    | 日 | 资金预期 | 资金地板 | 象限(地) 预期/地板 | 雇工 预期/地板 | 牛群 预期/地板 | 棚仓 MELON 残留上限 |
    |----|---------|---------|-------------------|---------------|---------------|--------------------|
    | 10 | $6000   | $3000   | 3 / 2             | 12 / 10       | 11 / 9        | —（当日 flush，不查）|
    | 11 | $6000   | $3000   | 3 / 3             | 13 / 11       | 11 / 9        | 20                 |
    | 12 | $5000   | $2500   | 3 / 3             | 13 / 11       | 11 / 9        | 20                 |

预期值推导（digest 节奏表逐日算术，全部来自实抓源码精读，非模型记忆）：

1) 资金（digest §2.1 日终现金列 + §3 波次表）：
   - d1-d4 日终 $400-600（肥料日结现金流）；d0 一把花到 ~$190（§2.1 d0 行）。
   - d6：+SELL WOOL×24 ≈$5.0k −（BUY_LAND#1 $1000 + COW×5 $2000）→ d6 终 ≈$2.5k。
   - d7-d8：COW×2+×1（$1.2k）对冲肥料 5-6/日 → ≈$2.3k。
   - d9：+羊毛 22（≈$4.4k）+肥料 15（≈$1.5k）−外购麦×11 → 进 d10 结转 ≈$8k。
   - d10：+SELL MELON×48 ≈$12k −（BUY_LAND#2 $2000 + COW×2 $800 + crew12 日薪
     ≈$376 + 草莓/瓜种 ≈$0.4k）→ 健康局 d10 日终量级 $10k+，日内谷值 ≈$4.3k。
   - d11/d12：无大额 flush（d12 奶×6 ≈$1k + 肥料清仓 39 ≈$3.9k）。
   → 预期取健康日终的保守 4 折（d10/d11 $6000、d12 $5000），地板 = 预期×50%
     （d10/d11 $3000、d12 $2500）。只有"波次明显未落地"（瓜/毛 flush 双失败、
     双死价局）才会击穿——正常局日终/午后均在地板上方 ≥$1.3k 裕量。
2) 地块（digest §2.3/§3）：开局 1 块 + d6 NE + d10 SW = 3 象限。d10 地板 = 2
   （当日购买步骤执行前不误报），d11/d12 地板 = 3（地2 未兑现在此暴露）。
3) 雇工（digest §3 阶梯）：12(d10) → 13(d11)，日薪制、EOD 清零 → 观测值随时辰
   波动，容差 2（地板 d10=10、d11/12=11）且仅日后半评估（见阈值 3）。
4) 牛群（digest §2.1/§3 购买序列）：d4×1 + d6×5 + d7×2 + d8×1 = 9，d10 +2 = 11；
   容差 2（放置中途观测），地板 9——畜线整体未点火（双死价局 P2 否决后
   仅剩 d4×1）在此暴露。
5) MELON 残留（digest §4.1 清仓纪律"首产即卖、当日卖清"）：d10 flush 48 单后，
   d11/d12 棚仓 MELON 应 ≈0；残留 > 20（≈flush 的 4 成）判"卖单未兑现"
   （价格崩 / 吸收堵死 / 抛单被抢先）。d10 当日不查（flush 在途）。

观测形态（与基底 v23.state_encoder 同构，本模块独立重实现取值语义）：
    obs.player / obs.step / obs.farms[player].{money, tiles, hands,
    unlocked_quadrants} / obs.private.shed；tiles 为行×格，格 dict 的
    "animal" 键计畜（COW）。

==============================================================================
【阈值】（登记项 2）
==============================================================================
    MONEY_DEVIATION_RATIO = 0.5     # 资金低于预期 50% → 偏离（方向：仅低侧）
    LATE_DAY_STEP         = 12      # 资金/雇工仅 step%24 >= 12（日后半）评估，
                                    #   防日内"资本开支已执行、flush 未到账"的在途误报
    MELON_RESIDUAL_LIMIT  = 20      # d11/12 棚仓 MELON 残留上限（上表）
    CASH_FLOOR            = $600    # 紧急卖保留线（digest §6A"花到 ≤$600 过夜"、
                                    #   v48 d0 ~$190 的过夜底线语义）
偏离 = 任一启用检查击穿地板/上限（detail.failed 列名）。资金高于预期不构成偏离。

==============================================================================
【偏离时的调整面清单——只动卖单】（登记项 3）
==============================================================================
adjust_sell_timing(sells, deviation) 只做"推迟非紧急卖单"，调整面封闭在
SELL 订单列表内，**没有任何触点可以改动产线步骤**（本模块不接收、不输出
farmer/hands/非卖市场单；调用方按集成缝原样保留它们——测试钉住）。

紧急（保留，不推迟）判定，按序：
    U1  FERTILIZER 卖单——digest §2.1"肥料从 d1 起就是日结现金流"，是剧本的
        生存现金流，推迟即断粮；
    U2  调用方显式紧急标记——订单第 4 元素为真值（["SELL", item, qty, True]）；
    U3  现金缺口补足单——当 deviation.detail.money < CASH_FLOOR 时，按保守估值
        BASE_PRICE×量 从大到小保留最少张数，直至 money+估值 >= CASH_FLOOR
        （大单优先 = 以最少订单数补足缺口，最小化曲线冲击次数）。
其余卖单 = 非紧急 → 本回合不下（推迟）。推迟后的库存归宿（三重兜底，均不动）：
    (a) 生产周期再上市：肥料每日、奶每 2 日、毛每 3 日（digest §2.1 引擎常数）；
    (b) 窗口纪律：d13 起本模块归零，磁带卖单逐字恢复执行；
    (c) 718 终局清仓（v48 原生 v19_terminal，零改动区）是硬兜底——推迟的
        库存最坏也进入终局清算，不存在"永久滞留"路径。

BASE_PRICE（保守卖单估值用；引擎常数，与 v23.state_encoder.BASE_PRICE 同值，
digest §引用约定/engine factsheet，模块内独立重声明）：
    WHEAT 25 / CARROT 35 / TOMATO 60 / STRAWBERRY 120 / MELON 250 /
    EGG 50 / MILK 160 / WOOL 200 / FERTILIZER 100

==============================================================================
【集成缝】（登记项 4；F2 assemble_package 接入，本模块不实现装配）
==============================================================================
在混合 router 的 agent() 内、child 策略产出 result 之后接入（建议放在
preemption.apply 之后：反克隆搬单属于紧急语义，先于本监测定形，避免与本层
推迟互相改写；终局 terminal_market 在 step=718，晚于窗口，无交互）：

    deviation = milestone_monitor.assess_milestone_deviation(obs, day)
    sells_in  = [o for o in result["market"] if _is_sell(o)]   # 仅 SELL 子集
    kept      = milestone_monitor.adjust_sell_timing(sells_in, deviation)
    # 用 kept 按原相对顺序替换 result["market"] 中的 SELL 槽位；
    # 非 SELL 槽位（BUY_*，属 P2 economic_guard 的否决面）与 farmer/hands 原样保留。

两函数均为纯函数（同输入同输出，无状态、无随机、无时钟 → R5 确定性）。

==============================================================================
【回退规则】（登记项 5；fail-safe）
==============================================================================
    F1  assess 任何异常/畸形输入（obs=None、farms 空、字段不可解析、day 非数）
        → 返回 {"deviated": False, "detail": {"error": ...}}，绝不抛出；
    F2  adjust 任何异常（含 deviation.detail 畸形）→ 原样返回 sells；
    F3  窗口外（day ∉ [10,12]）→ 不评估 → 不偏离 → 零动作；
    F4  未偏离 → adjust 原样返回（同一对象，identity 钉住）；
    F5  无法识别的订单形态（非 ["SELL", item, qty] 序列）→ 保留不动（宁可漏推
        迟，不可错删）。
"""

__all__ = [
    "MILESTONE_TABLE",
    "WINDOW_FIRST_DAY",
    "WINDOW_LAST_DAY",
    "MONEY_DEVIATION_RATIO",
    "LATE_DAY_STEP",
    "CASH_FLOOR",
    "MELON_RESIDUAL_LIMIT",
    "BASE_PRICE",
    "assess_milestone_deviation",
    "adjust_sell_timing",
]

# ---------------------------------------------------------------------------
# 登记常量（依据见模块头）
# ---------------------------------------------------------------------------

WINDOW_FIRST_DAY = 10
WINDOW_LAST_DAY = 12
TURNS_PER_DAY = 24
LATE_DAY_STEP = 12
MONEY_DEVIATION_RATIO = 0.5
CASH_FLOOR = 600.0
MELON_RESIDUAL_LIMIT = 20

BASE_PRICE = {
    "WHEAT": 25.0,
    "CARROT": 35.0,
    "TOMATO": 60.0,
    "STRAWBERRY": 120.0,
    "MELON": 250.0,
    "EGG": 50.0,
    "MILK": 160.0,
    "WOOL": 200.0,
    "FERTILIZER": 100.0,
}

MILESTONE_TABLE = {
    10: {
        "money_expected": 6000.0,
        "quadrants_expected": 3,
        "quadrants_floor": 2,
        "hands_expected": 12,
        "hands_floor": 10,
        "cows_expected": 11,
        "cows_floor": 9,
        "melon_residual_limit": None,
    },
    11: {
        "money_expected": 6000.0,
        "quadrants_expected": 3,
        "quadrants_floor": 3,
        "hands_expected": 13,
        "hands_floor": 11,
        "cows_expected": 11,
        "cows_floor": 9,
        "melon_residual_limit": MELON_RESIDUAL_LIMIT,
    },
    12: {
        "money_expected": 5000.0,
        "quadrants_expected": 3,
        "quadrants_floor": 3,
        "hands_expected": 13,
        "hands_floor": 11,
        "cows_expected": 11,
        "cows_floor": 9,
        "melon_residual_limit": MELON_RESIDUAL_LIMIT,
    },
}

_URGENT_CASHFLOW_ITEMS = ("FERTILIZER",)


# ---------------------------------------------------------------------------
# 内部工具（取值语义与基底 v23.state_encoder.get 同构，独立重实现）
# ---------------------------------------------------------------------------

def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _to_number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _own_farm(observation):
    farms = list(_get(observation, "farms", []) or [])
    if not farms:
        raise ValueError("observation carries no farms")
    player = int(_get(observation, "player", 0) or 0)
    return farms[player] if 0 <= player < len(farms) else farms[0]


def _count_animals(farm, animal):
    count = 0
    for row in (_get(farm, "tiles", []) or []):
        if not isinstance(row, (list, tuple)):
            continue
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == animal:
                count += 1
    return count


# ---------------------------------------------------------------------------
# 1) 里程碑偏离评估
# ---------------------------------------------------------------------------

def assess_milestone_deviation(observation, day):
    """d10-12 窗口资金/库存 vs 剧本预期里程碑比对。

    返回 {"deviated": bool, "detail": {...}}；任何异常都折为
    {"deviated": False, "detail": {"error": ...}}（回退规则 F1，绝不抛出）。
    """
    try:
        return _assess(observation, day)
    except Exception as exc:  # fail-safe F1
        return {"deviated": False, "detail": {"error": f"{type(exc).__name__}: {exc}"}}


def _assess(observation, day):
    if observation is None:
        raise ValueError("observation is None")
    day_index = int(day)
    if not (WINDOW_FIRST_DAY <= day_index <= WINDOW_LAST_DAY):
        return {"deviated": False, "detail": {"window": False, "day": day_index}}

    step = int(_get(observation, "step", 0) or 0)
    late_day = (step % TURNS_PER_DAY) >= LATE_DAY_STEP
    farm = _own_farm(observation)

    money = _to_number(_get(farm, "money", 0.0))
    quadrants = len(_get(farm, "unlocked_quadrants", []) or [])
    hands = len(_get(farm, "hands", []) or [])
    cows = _count_animals(farm, "COW")
    private = _get(observation, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    melon_residual = (
        _to_number(shed.get("MELON")) if isinstance(shed, dict) else 0.0
    )

    row = MILESTONE_TABLE[day_index]
    checks = {}

    def register(name, expected, floor, actual, enabled):
        if enabled:
            checks[name] = {
                "expected": expected,
                "floor": floor,
                "actual": actual,
                "failed": bool(actual < floor),
            }

    # 资金：仅低侧偏离，且防日内在途误报（阈值 LATE_DAY_STEP）
    money_floor = round(row["money_expected"] * MONEY_DEVIATION_RATIO, 2)
    register("money", row["money_expected"], money_floor, money, late_day)
    # 地块：全日可查（d10 地板=2 容当日购买在途）
    register(
        "land_quadrants",
        row["quadrants_expected"],
        row["quadrants_floor"],
        quadrants,
        True,
    )
    # 雇工：EOD 清零制 → 仅日后半评估（阈值 LATE_DAY_STEP）
    register(
        "crew_hands", row["hands_expected"], row["hands_floor"], hands, late_day
    )
    # 牛群：全日可查（容差 2 = 放置中途）
    register("cow_herd", row["cows_expected"], row["cows_floor"], cows, True)
    # MELON 残留：仅 d11/12（d10 flush 在途不查），高侧偏离
    limit = row["melon_residual_limit"]
    if limit is not None:
        checks["melon_residual"] = {
            "expected": 0.0,
            "limit": limit,
            "actual": melon_residual,
            "failed": bool(melon_residual > limit),
        }

    failed = sorted(name for name, verdict in checks.items() if verdict["failed"])
    return {
        "deviated": bool(failed),
        "detail": {
            "window": True,
            "day": day_index,
            "step": step,
            "late_day": late_day,
            "money": money,
            "checks": checks,
            "failed": failed,
        },
    }


# ---------------------------------------------------------------------------
# 2) 卖单时点调整（只动卖单）
# ---------------------------------------------------------------------------

def adjust_sell_timing(sells, deviation):
    """偏离时推迟非紧急卖单；未偏离/异常 = 原样返回（回退规则 F2/F4）。"""
    try:
        if not isinstance(deviation, dict) or not deviation.get("deviated"):
            return sells
        return _adjust(sells, deviation)
    except Exception:
        return sells  # fail-safe F2


def _parse_sell(order):
    """识别 ["SELL", item, qty(, urgent)] 序列；不识别返回 None（保留不动，F5）。"""
    if not isinstance(order, (list, tuple)) or len(order) < 3:
        return None
    if order[0] != "SELL":
        return None
    item = str(order[1])
    try:
        quantity = float(order[2])
    except (TypeError, ValueError):
        return None
    if quantity <= 0:
        return None
    explicit_urgent = bool(len(order) >= 4 and order[3])
    return item, int(quantity), explicit_urgent


def _is_urgent(item, explicit_urgent):
    return explicit_urgent or item in _URGENT_CASHFLOW_ITEMS


def _adjust(sells, deviation):
    detail = deviation.get("detail")
    detail = detail if isinstance(detail, dict) else {}

    # U3 现金缺口：money 不可解析/缺失 → 不启用缺口保留（仅 U1/U2 生效）
    need = 0.0
    money = detail.get("money")
    if isinstance(money, (int, float)) and not isinstance(money, bool):
        if float(money) < CASH_FLOOR:
            need = CASH_FLOOR - float(money)

    parsed = [(_parse_sell(order), order) for order in sells]

    keep = set()
    if need > 0.0:
        candidates = []
        for index, (parts, _order) in enumerate(parsed):
            if parts is None or _is_urgent(parts[0], parts[2]):
                continue
            proceeds = BASE_PRICE.get(parts[0], 0.0) * parts[1]
            candidates.append((proceeds, index))
        candidates.sort(reverse=True)
        covered = 0.0
        for proceeds, index in candidates:
            if covered >= need:
                break
            keep.add(index)
            covered += proceeds

    return [
        order
        for index, (parts, order) in enumerate(parsed)
        if parts is None or index in keep or _is_urgent(parts[0], parts[2])
    ]
