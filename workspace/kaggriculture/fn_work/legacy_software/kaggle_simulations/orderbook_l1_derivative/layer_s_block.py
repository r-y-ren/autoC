"""layer S 尾块模板（R10 运行时五函数的代码真值）。

被 append_layer_s_block 抽取源码注入 L1 main.py 尾部；独立可导入供
orderbook_l1_derivative/test_layer_s.py 单测（测试代码=上发代码，零漂移）。
契约见 fn_docs/hybrid/responsibility.md【R10 增补】。"""

# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）
_CXS_FROM = 648
_CXS_SEASON_END = 718

# 首收步数表（R9/bots 常数看护先例；wheel 现值交叉校验见 test_consts_crosscheck.py）
# 来源（2026-09-23 实读转录）：本机 vendored wheel kaggle_environments 1.32.7+nodeps，
#   模块 kaggle_environments/envs/kaggriculture/kaggriculture.py 模块级 CROPS 表的
#   first_yield_day 字段（单位=天）。换算式（1 天 = turnsPerDay 默认 24 步；719 步/30 天）：
#   FIRST_HARVEST_STEPS[crop] = CROPS[crop]["first_yield_day"] * 24
# 口径：从 PLANT 那步起到第一次 HARVEST 可得那步的步数差。引擎 day = step // 24，
#   PLANT 记 planted_day=当日，HARVEST 合法条件 day - planted_day >= first_yield_day
#   （kaggriculture.py L453），故"种下→首收"相隔 first_yield_day 整天 = *24 步级；
#   WHEAT/CARROT = 2 天 = 48 步，与契约预期一致。
FIRST_HARVEST_STEPS: dict = {
    "WHEAT": 48,        # first_yield_day=2  → 2*24
    "CARROT": 48,       # first_yield_day=2  → 2*24
    "TOMATO": 192,      # first_yield_day=8  → 8*24
    "STRAWBERRY": 240,  # first_yield_day=10 → 10*24
    "MELON": 240,       # first_yield_day=10 → 10*24
}


def _cxs_agent(observation, configuration=None):
    """运行时入口：捕获 last-callable 基座→取动作→step≥648 交截断；异常回退基座动作。"""
    raise NotImplementedError("unimplemented:fn:_cxs_agent")


def _cxs_seed_truncate(observation, action, plan_view):
    """纯减法过滤：逐品项按允许删除量删超额 BUY_SEED；品项不确定(None)→零截断。"""
    raise NotImplementedError("unimplemented:fn:_cxs_seed_truncate")


def _cxs_seed_surplus(crop, observation, kept_orders, plan_view):
    """零误杀核心：surplus=库存+保留单+磁带未来购买−可完成需求；解析失败→None。

    返回 int=允许删除的本品项 BUY_SEED 数量 = min(max(0, 供给−需求),
    kept_orders 本品项购买量)（删除对象只可能是本回合订单）；None=不确定=
    上游对该品项零截断；0=确证无剩余（与 None 异义）。
    demand = _cxs_completable_plant_demand(crop, observation, plan_view)，
    其 None → 本函数 None。供给三路相加：
      1) 库存种子 observation["private"]["seeds"].get(crop, 0)。字段路径取基座
         同款（orderbook_derivative/main.py）：tomato 门 L6775
         obs['private']['seeds'].get('TOMATO', 0)；CARROT2 层 L4607
         priv = observation["private"] 后 L4693 int(priv["seeds"].get("CARROT", 0))；
         观测 schema 注记 L244 observation["private"]={"shed","seeds":{crop:n},
         "inventories"}。基座的 int() 宽 coercion 在此收紧为严格数型（bool/
         字符串数字/半值 float 均视为类型异常）；字段缺失/类型异常 → None。
      2) kept_orders 中 ["BUY_SEED", crop, qty] 之和，订单匹配对齐基座式
         len(o)>=3 and o[:2]==["BUY_SEED", crop]（main.py L4680/L4694）。
         kept_orders 非 list/tuple，或任一订单非 list/tuple、长度<3（无论操作
         类型——无法确认该单不是本品项）、本品项 BUY_SEED 的 qty 非整数
         （bool/str/None/半值 float 同拒）→ None：解析不完整=不确定=零截断。
      3) 磁带未来购买：plan_view 结果中步 t>observation["step"] 各条目
         buy_seed.get(crop, 0) 之和（当前步及更早不计）。step 缺失/非整数→None；
         步键/条目/plants/buy_seed/本品项计数的结构校验与 demand 同规（畸形→None）。
    纯函数优先：demand 内部已调一次 plan_view，这里再调一次读 buy_seed；用与
    demand 完全相同的求和语义从新结果重算需求，与 demand 返回值不等（两次调用
    结果不一致=非确定性 plan_view）→ None。其余任何读取/解析异常 → None。
    """

    def _strict_count(value):
        # 数量解析纪律（同 _cxs_completable_plant_demand）：int（非 bool）原样，
        # 整值 float 折 int；bool/str/None/半值 float 抛异常 → 外层定向 None。
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("count not numeric")
        if isinstance(value, float):
            if not value.is_integer():
                raise TypeError("count fractional")
            value = int(value)
        return value

    try:
        demand = _cxs_completable_plant_demand(crop, observation, plan_view)
        if demand is None:
            return None

        # 库存 + 当前步（observation 非 dict / 字段缺失 / 类型异常 → None）
        if not isinstance(observation, dict):
            return None
        priv = observation.get("private")
        if not isinstance(priv, dict):
            return None
        seeds = priv.get("seeds")
        if not isinstance(seeds, dict):
            return None
        held = _strict_count(seeds.get(crop, 0))
        step_now = _strict_count(observation.get("step"))

        # 磁带：纯函数优先再调一次 plan_view；结构与 demand 同规校验 + 重算交叉核对
        tape = plan_view(observation)
        if not isinstance(tape, dict):
            return None
        replay_demand = 0
        tape_buy = 0
        for t, entry in tape.items():
            if isinstance(t, bool) or not isinstance(t, (int, float)):
                return None  # 步键非数=结构不合法=不确定
            if isinstance(t, float):
                if not t.is_integer():
                    return None
                t = int(t)
            if not isinstance(entry, dict):
                return None
            plants = entry.get("plants", {})
            if not isinstance(plants, dict):
                return None
            units = _strict_count(plants.get(crop, 0))
            buys = entry.get("buy_seed", {})
            if not isinstance(buys, dict):
                return None
            qty = _strict_count(buys.get(crop, 0))
            if _cxs_harvest_completable(t, crop):
                replay_demand += units
            if t > step_now:
                tape_buy += qty
        if replay_demand != demand:
            return None  # 两次 plan_view 结果不一致（非确定性）→ 不确定

        # 保留单：畸形订单一律 None（宁可保守：无法解析的订单集合不能作截断依据）
        if not isinstance(kept_orders, (list, tuple)):
            return None
        kept_buy = 0
        for order in kept_orders:
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                return None
            if order[0] == "BUY_SEED" and order[1] == crop:
                kept_buy += _strict_count(order[2])

        supply = held + kept_buy + tape_buy
        allow = supply - demand
        if allow < 0:
            allow = 0
        if allow > kept_buy:
            allow = kept_buy
        return allow
    except Exception:
        return None


def _cxs_completable_plant_demand(crop, observation, plan_view):
    """逐品项未来可完成种+收的 PLANT 种子需求；plan_view 解析失败→None。

    demand(crop) = Σ_t plans[t]["plants"].get(crop, 0)，仅计入
    _cxs_harvest_completable(t, crop) 为 True 的步 t（种+收来得及才保护
    种子；来不及的步不计需求=允许截断超额供给）。零误杀纪律：plan_view
    不可调用 / 调用抛任何异常 / 返回 None / 结构不合法（外层非 dict、
    条目非 dict、plants 非 dict、本品项计数非数）→ None（不确定=上游
    零截断）。0=确证无未来需求，与 None 异义。buy_seed 不入本函数。
    """
    try:
        if not callable(plan_view):
            return None
        plans = plan_view(observation)
        if not isinstance(plans, dict):
            return None
        demand = 0
        for step, entry in plans.items():
            if not isinstance(entry, dict):
                return None
            plants = entry.get("plants", {})
            if not isinstance(plants, dict):
                return None
            units = plants.get(crop, 0)
            if isinstance(units, bool) or not isinstance(units, (int, float)):
                return None  # 计数非数=结构不合法=不确定
            if isinstance(units, float):
                if not units.is_integer():
                    return None
                units = int(units)
            if not _cxs_harvest_completable(step, crop):
                continue
            demand += units
        return demand
    except Exception:
        return None


def _cxs_harvest_completable(step, crop, first_harvest_steps=None):
    """纯时间测试：step+first_harvest(crop)≤718；常数缺失/异常→True（保守不截）。

    step s 的 crop PLANT 可完成"种+收" ⇔ s + first_harvest_steps(crop) ≤
    _CXS_SEASON_END(718)。first_harvest_steps=None 时用模块级
    FIRST_HARVEST_STEPS；表缺失/作物不在表/任何类型或运行异常 → True
    （零误杀：不确定=来得及=不构成截断理由）。
    """
    try:
        table = FIRST_HARVEST_STEPS if first_harvest_steps is None else first_harvest_steps
        return step + table[crop] <= _CXS_SEASON_END
    except Exception:
        return True
