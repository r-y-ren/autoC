"""layer S 尾块模板（R10 运行时五函数的代码真值）。

被 append_layer_s_block 抽取源码注入 L1 main.py 尾部；独立可导入供
orderbook_l1_derivative/test_layer_s.py 单测（测试代码=上发代码，零漂移）。
契约见 fn_docs/hybrid/responsibility.md【R10 增补】。"""

# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）
_CXS_FROM = 648
_CXS_SEASON_END = 718

# PLANT 完成期限和（评审 2026-09-23 off-by-one 修正，误杀向）：引擎收获合法条件为
# 天粒度 day - planted_day >= first_yield_day（kaggressure.py L453），day=step//24，
# 718=day29 内最后有效动作步=最后可收获步 ⇒ PLANT@s 可完成种+收 ⇔
# s + first_harvest_steps(crop) <= 719（⟺ s//24 + fh//24 <= 29，引擎天粒度规则）。
# 旧右界 718 把 s=671（fh=48：27+2=29 恰可完成）误判不可完成。
_CXS_PLANT_DEADLINE_SUM = 719

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


# 宿主捕获（层 D 先例 main.py L6835 _CXD_HOST 同款 last-callable 捕获）：注入态本语句
# 在追加块首部执行——globals 最后 callable=基座尾部的 orderbook 版 _cxd_agent，即本层
# 宿主；它必须在 _cxs_agent（乃至本块任何 def）定义之前执行，否则捕获到本层自身函数。
# 双下划线名排除：模块样板 callable（如 PEP 649 的 __annotate__，Python 3.14 起随模块
# 首位插入 globals）不是宿主面——注入态它们先于一切用户 def 插入、本就不在末位，排除
# 无影响；独立导入态排除后无可捕获 callable → _CXS_HOST=None（宿主不存在），测试经
# monkeypatch 本模块级 _CXS_HOST 注入假宿主（_cxs_agent 的测试注入通道）。
_cxs_last_callable = [
    v for k, v in list(globals().items())
    if callable(v) and not (k.startswith("__") and k.endswith("__"))
]
_CXS_HOST = _cxs_last_callable[-1] if _cxs_last_callable else None


def _cxs_plan_view(observation):
    """内联 plan_view 适配器（_cxs_agent 职责面的内部实现，非独立职责函数）。

    把基座双路磁带折叠为截断层只读视图 {t: {"plants": {crop: n}, "buy_seed": {crop: n}}}：
    磁带取 _IMPL.chassis.routes，day27 起（t≥_CXS_FROM）走 2 号路——基座同款路由换算
    （侦察行号 2168/2342/2583/4888：routes[2 if t>=648 else route]）；步条目越界或非
    dict 视为空步。plants=farmer+hands 指令中 PLANT 且品项在 FIRST_HARVEST_STEPS 的
    逐品计数；buy_seed=market 中 BUY_SEED 订单 qty（max(0,int) 钳非负）逐品累加；
    空步不入表，整卷为空 → None。_IMPL 为基座模块级单例（注入态与本块同名空间）；
    独立导入测试态经 globals().get("_IMPL") 取得 None → 返回 None（不确定=零截断）。
    seat/step 解析失败、step<0、route 缺失或不在 routes、任何异常 → None。
    """
    try:
        impl = globals().get("_IMPL")  # 注入态=基座单例；独立导入态不存在
        if impl is None:
            return None
        ch = impl.chassis
        seat = int(observation.get("player", 0))
        step = int(observation.get("step", -1))
        native = ch.players.get(seat) or {}
        route = native.get("route")
        if step < 0 or route is None or route not in ch.routes:
            return None
        out = {}
        for t in range(step + 1, _CXS_SEASON_END + 1):
            tape = ch.routes[2 if t >= _CXS_FROM else route]
            a = tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}
            plants, buys = {}, {}
            for c in [a.get("farmer") or ["PASS"], *(a.get("hands") or [])]:
                if c and len(c) > 1 and c[0] == "PLANT" and c[1] in FIRST_HARVEST_STEPS:
                    plants[c[1]] = plants.get(c[1], 0) + 1
            for o in (a.get("market") or []):
                if o and len(o) >= 3 and o[0] == "BUY_SEED" and o[1] in FIRST_HARVEST_STEPS:
                    buys[o[1]] = buys.get(o[1], 0) + max(0, int(o[2]))
            if plants or buys:
                out[t] = {"plants": plants, "buy_seed": buys}
        return out or None
    except Exception:
        return None


def _cxs_seed_truncate(observation, action, plan_view):
    """纯减法过滤主函数：step≥648 起逐品项按允许删除量删超额 BUY_SEED。

    零足迹快道（原 market 对象原样返回，不复制、不调 plan_view）三者居一即返：
    observation["step"] < _CXS_FROM；market 缺失（→None）/非 list/为空；market
    无 BUY_SEED（订单匹配对齐 surplus 式：list/tuple、len≥3、首元 "BUY_SEED"，
    main.py L4680/L4694）。
    慢道：按品项分组（BUY_SEED 出现序去重），对每品项以 kept_orders=本回合
    全部订单（先按"全保留"算额度：删除对象只可能是本回合订单）调
    _cxs_seed_surplus，并传当前步该品项 PLANT 数（引擎结算序：同 step 单位
    动作 PLANT 消耗 private.seeds 先于市场买单入账，故当前步种植消耗不属于
    未来供给——从本 action 的 farmer+hands 统计，["PLANT", crop] 解析与
    _cxs_plan_view 同款；解析失败（action 结构畸形）→ 逐品项传 None →
    surplus 返回 None → 零截断）；None（不确定）或 0（确证无额度）→
    该品项零截断。
    删除策略：按订单出现序从后往前逐单判定——删该单若累计删除+qty≤allowed
    则整单删除，否则跳过该单继续向前（只删整单、不减量改单：改单=加法面，
    违反纯减法纪律）；非 BUY_SEED 订单与其余槽位顺序原样保留（删除=列表
    移除，无插入/无重排；有删除才建新表，零删除仍返回原对象）。
    本函数不做 try 吞噬（唯一例外：当前步 PLANT 计数解析按契约吞异常转
    None）：任何其余异常向上抛，由 _cxs_agent 兜底回退基座动作
    （契约：错误处理在上层入口统一兜底）。
    """
    market = action.get("market")
    if observation["step"] < _CXS_FROM:
        return market
    if not isinstance(market, list) or not market:
        return market

    def _is_seed_order(order, crop):
        # 订单匹配对齐 surplus 式（main.py L4680/L4694）；crop=None 表任意品项。
        if not isinstance(order, (list, tuple)) or len(order) < 3:
            return False
        if order[0] != "BUY_SEED":
            return False
        return crop is None or order[1] == crop

    def _current_plants(act):
        # 当前步各品项 PLANT 计数（与 _cxs_plan_view 同款解析：farmer+hands
        # 指令、["PLANT", crop] 且品项在 FIRST_HARVEST_STEPS 逐品计数，缺省
        # PASS/空 hands 不视为畸形）；任何异常 → None（action 结构畸形=当前步
        # 消耗未知=逐品项 None → surplus None → 零截断，零误杀纪律）。
        counts = {}
        try:
            for cmd in [act.get("farmer") or ["PASS"], *(act.get("hands") or [])]:
                if cmd and len(cmd) > 1 and cmd[0] == "PLANT" and cmd[1] in FIRST_HARVEST_STEPS:
                    counts[cmd[1]] = counts.get(cmd[1], 0) + 1
        except Exception:
            return None
        return counts

    crops = []
    for order in market:
        if _is_seed_order(order, None) and order[1] not in crops:
            crops.append(order[1])
    if not crops:
        return market

    plants_now = _current_plants(action)
    keep = [True] * len(market)
    for crop in crops:
        allowed = _cxs_seed_surplus(
            crop,
            observation,
            market,
            plan_view,
            None if plants_now is None else plants_now.get(crop, 0),
        )
        if allowed is None or allowed <= 0:
            continue  # None=不确定 / 0=确证无额度：该品项零截断
        deleted = 0
        for i in range(len(market) - 1, -1, -1):  # 出现序从后往前逐单判定
            if not _is_seed_order(market[i], crop):
                continue
            qty = market[i][2]  # surplus 返回 int 时该品项全单 qty 已过严格数校验
            if deleted + qty <= allowed:
                keep[i] = False
                deleted += qty
    if all(keep):
        return market  # 零删除：仍零足迹
    return [order for i, order in enumerate(market) if keep[i]]


def _cxs_seed_surplus(crop, observation, kept_orders, plan_view, current_plants: int | None = None):
    """零误杀核心（v2 净需求覆盖，R11）：surplus=max(0,库存−当前步PLANT消耗)+保留单−可完成需求；磁带未来购买不计；解析失败→None。

    v2 相对 L1 的唯一口径变更：磁带未来 BUY_SEED 一律不再计入供给（R11 净需求
    覆盖）。删去磁带未来供给后本函数更保守（供给变小→删得更少）——这正确：
    磁带单由各自回合同判定守护，回买单（本回合订单）在同口径下被正确评估。
    demand = _cxs_completable_plant_demand(crop, observation, plan_view)，
    其 None → 本函数 None；v2 需求只调一次 plan_view（供给不再读磁带，无 L1
    的二次调用一致性交叉核对，也不必再读 observation["step"]）。供给两路相加
    （held_effective = max(0, 库存 − current_plants)，超扣钳 0 不为负）：
      1) 有效库存种子 observation["private"]["seeds"].get(crop, 0) 减当前步
         PLANT 消耗。字段路径取基座同款（orderbook_derivative/main.py：
         tomato 门 L6775 obs['private']['seeds'].get('TOMATO', 0)；CARROT2
         层 L4607/L4693 int(priv["seeds"].get("CARROT", 0))）；基座的 int()
         宽 coercion 收紧为严格数型（bool/字符串数字/半值 float 均视为类型
         异常）；字段缺失/类型异常 → None。current_plants：None=未知 →
         直接返回 None（引擎结算序同 step 单位动作 PLANT 消耗 private.seeds
         先于市场买单入账，当前步种植消耗不属于未来供给，消耗未知即供给
         不确定）；0=确证当前步无该品种植；非负整数校验（bool/str/半值
         float/负数 → None）。
      2) kept_orders 中 ["BUY_SEED", crop, qty] 之和（本回合保留单），订单
         匹配对齐基座式 len(o)>=3 and o[:2]==["BUY_SEED", crop]（main.py
         L4680/L4694）。kept_orders 非 list/tuple，或任一订单非 list/tuple、
         长度<3（无论操作类型——无法确认该单不是本品项）、本品项 BUY_SEED
         的 qty 非整数（bool/str/None/半值 float 同拒）→ None：解析不完整=
         不确定=零截断。
    返回 int=允许删除的本品项 BUY_SEED 数量 = min(max(0, 供给−需求),
    kept_orders 本品项购买量)（删除对象只可能是本回合订单）；None=不确定=
    上游对该品项零截断；0=确证无剩余（与 None 异义）。其余任何读取/解析
    异常 → None（零误杀：一切不确定→None→上游零截断）。
    """
    if current_plants is None:
        return None  # 当前步 PLANT 消耗未知=供给不确定=零误杀纪律→None

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
        # 当前步 PLANT 消耗：非负整数（bool/str/半值 float → _strict_count 抛；
        # 负数 → 显式 None）
        plants_now = _strict_count(current_plants)
        if plants_now < 0:
            return None

        # 需求（v2 唯一一次 plan_view 消费点：可完成 PLANT 种子需求）
        demand = _cxs_completable_plant_demand(crop, observation, plan_view)
        if demand is None:
            return None

        # 库存（observation 非 dict / 字段缺失 / 类型异常 → None）
        if not isinstance(observation, dict):
            return None
        priv = observation.get("private")
        if not isinstance(priv, dict):
            return None
        seeds = priv.get("seeds")
        if not isinstance(seeds, dict):
            return None
        held = _strict_count(seeds.get(crop, 0))

        # 保留单：畸形订单一律 None（宁可保守：无法解析的订单集合不能作截断依据）
        if not isinstance(kept_orders, (list, tuple)):
            return None
        kept_buy = 0
        for order in kept_orders:
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                return None
            if order[0] == "BUY_SEED" and order[1] == crop:
                kept_buy += _strict_count(order[2])

        held_effective = held - plants_now  # 当前步 PLANT 先于买单入账：扣减
        if held_effective < 0:
            held_effective = 0  # 超扣钳 0（plants>held 不得产生负供给）
        supply = held_effective + kept_buy  # v2 净口径：磁带未来购买一律不计
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
    """纯时间测试：step+first_harvest(crop)≤719；常数缺失/异常→True（保守不截）。

    step s 的 crop PLANT 可完成"种+收" ⇔ s + first_harvest_steps(crop) ≤
    _CXS_PLANT_DEADLINE_SUM(719)（引擎天粒度收获规则 day - planted_day >=
    first_yield_day（L453）+ 最后动作步 718 的推导见常数注释；评审 2026-09-23
    修正，旧界 718 为 off-by-one 误杀）。first_harvest_steps=None 时用模块级
    FIRST_HARVEST_STEPS；表缺失/作物不在表/任何类型或运行异常 → True
    （零误杀：不确定=来得及=不构成截断理由）。
    """
    try:
        table = FIRST_HARVEST_STEPS if first_harvest_steps is None else first_harvest_steps
        return step + table[crop] <= _CXS_PLANT_DEADLINE_SUM
    except Exception:
        return True


def _cxs_agent(observation, configuration=None):
    """运行时入口（注入后为 main.py 最后 callable=官方入口）：宿主取动作→step≥648 交截断层。

    先例=层 D main.py L6909：宿主调用在 try 之外——`action = _CXS_HOST(observation,
    configuration)`（_CXS_HOST=注入时基座最后 callable=orderbook 版 _cxd_agent）；宿主
    异常向上传播，宿主坏了不是本层责任。try 内三步（fail-safe：任何异常→原样返回
    宿主 action，绝不崩）：
      1) step==0 复位层内缓存（本层当前无跨步缓存，留复位钩子注释）；
      2) step≥_CXS_FROM 且 action 是 dict 且 action["market"] 含 BUY_SEED（订单匹配
         对齐截断层/基座 L4680/L4694：list/tuple、len≥3、首元 "BUY_SEED"）→
         _cxs_seed_truncate(observation, action, _cxs_plan_view)，返回
         dict(action, market=filtered)（内联 plan_view 适配器见上）；
      3) 其余一切情况（step<648 / action 非 dict / market 缺失·非 list / 无 BUY_SEED /
         截断链异常）→ 原样返回宿主 action（同对象零足迹）。
    独立测试态 _CXS_HOST=None（宿主不存在）：测试经 monkeypatch 本模块 _CXS_HOST /
    _cxs_plan_view / _cxs_seed_truncate 注入假件（_cxs_agent 按名取模块全局，补丁即生效）。
    """
    action = _CXS_HOST(observation, configuration)  # 宿主调用在 try 之外（层 D L6909 先例）
    try:
        step = int(observation.get("step", 0))
        if step == 0:
            pass  # 复位钩子：本层当前无跨步缓存；未来引入跨步状态时在此复位
        if step >= _CXS_FROM and isinstance(action, dict):
            market = action.get("market")
            if isinstance(market, list) and any(
                isinstance(order, (list, tuple)) and len(order) >= 3 and order[0] == "BUY_SEED"
                for order in market
            ):
                filtered = _cxs_seed_truncate(observation, action, _cxs_plan_view)
                return dict(action, market=filtered)
        return action
    except Exception:
        return action
