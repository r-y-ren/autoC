"""layer S 尾块模板（R10 运行时五函数的代码真值）。

被 append_layer_s_block 抽取源码注入 L1 main.py 尾部；独立可导入供
orderbook_l1_derivative/test_layer_s.py 单测（测试代码=上发代码，零漂移）。
契约见 fn_docs/hybrid/responsibility.md【R10 增补】。"""

# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）
_CXS_FROM = 600
_CXS_ROUTE_BOUNDARY = 648  # 基座 day-27（step 648）起强制 2 号路：硬事实，与截断窗口解耦（R12 修正）
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
_CXS_SAFETY_LOOKBACK_STEPS = 24  # R12 安全边：观测窗（步）=磁带前视窗（1 天粒度定桩）
_CXS_SAFETY_MIN_MARGIN = 2       # R12 安全边下限（宁多买一颗 $20，不饿死一茬）


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
    磁带取 _IMPL.chassis.routes，day27 起（t≥_CXS_ROUTE_BOUNDARY）走 2 号路——基座同款路由换算
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
            tape = ch.routes[2 if t >= _CXS_ROUTE_BOUNDARY else route]
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


def _cxs_reduce_orders(observation, action, plan_view):
    """减量过滤主函数（v3，R12）：step≥_CXS_FROM 起逐品项把本回合 BUY_SEED 购买量减至目标保有 R。

    零足迹快道（原 market 对象原样返回，不复制、不调 plan_view）三者居一即返：
    observation["step"] < _CXS_FROM；market 缺失（→None）/非 list/为空；market
    无 BUY_SEED（订单匹配对齐 L1 surplus/truncate 式：list/tuple、len≥3、首元
    "BUY_SEED"，main.py L4680/L4694）。`[]`/None 空槽垫单归类为可忽略占位
    （R11 法证 669 形解析洞修正）：不构成品项、原位保留。
    慢道：按品项分组（BUY_SEED 出现序去重），对每品项以 kept_orders=本回合
    全部订单（目标保有量的判定对象=本回合订单）调 _cxs_seed_balance，并传当前步
    该品项 PLANT 数（引擎结算序：同 step 单位动作 PLANT 消耗 private.seeds 先于
    市场买单入账；解析与 L1 _current_plants 同款，解析失败 → 逐品项传 None →
    balance 返回 None）；R None（不确定）或 excess=本回合该品项总购买量−R ≤ 0
    （R≥购买总量）→ 该品项零动作。减量策略：从最后一张 BUY_SEED 往前逐单减
    min(qty, 剩余 excess)——减至 0 的单整单消失（≡R10 整单删形态），部分减的
    单以 [op, crop, 新 qty] 重写（只减不加，尾部字段如有则保留），其余订单与
    槽位顺序原样保留（无插入/无重排；有改动才建新表，零改动仍返回原对象）。
    本函数不做 try 吞噬（沿 L1）：任何异常向上抛，由 _cxs_agent 兜底回退基座
    动作（契约：错误处理在上层入口统一兜底）。
    """
    market = action.get("market")
    if observation["step"] < _CXS_FROM:
        return market
    if not isinstance(market, list) or not market:
        return market

    def _is_seed_order(order, crop):
        # 订单匹配对齐 L1 surplus/truncate 式（main.py L4680/L4694）；crop=None 表任意品项。
        if not isinstance(order, (list, tuple)) or len(order) < 3:
            return False
        if order[0] != "BUY_SEED":
            return False
        return crop is None or order[1] == crop

    def _current_plants(act):
        # 当前步各品项 PLANT 计数（与 _cxs_plan_view 同款解析：farmer+hands 指令、
        # ["PLANT", crop] 且品项在 FIRST_HARVEST_STEPS 逐品计数，缺省 PASS/空
        # hands 不视为畸形）；任何异常 → None（action 结构畸形=当前步消耗未知=
        # 逐品项 None → balance None → 零减量，零误杀纪律）。
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
    new_qty = [None] * len(market)  # None=该槽不动；int=减量后数量（0=整单消失）
    for crop in crops:
        r = _cxs_seed_balance(
            crop,
            observation,
            market,
            plan_view,
            None if plants_now is None else plants_now.get(crop, 0),
        )
        if r is None:
            continue  # None=不确定：该品项原样（宁多买）
        round_buy = 0
        for order in market:
            if _is_seed_order(order, crop):
                round_buy += order[2]  # balance 非 None 时全单 qty 已过严格数校验
        excess = round_buy - r
        if excess <= 0:
            continue  # R ≥ 本回合购买总量 → 上游零动作（只减不加）
        remaining = excess
        for i in range(len(market) - 1, -1, -1):  # 从最后一张 BUY_SEED 往前减
            if not _is_seed_order(market[i], crop):
                continue
            qty = market[i][2]
            cut = qty if qty <= remaining else remaining  # min(qty, 剩余 excess)
            new_qty[i] = qty - cut
            remaining -= cut
            if remaining <= 0:
                break
    if all(q is None for q in new_qty):
        return market  # 零改动：仍零足迹
    out = []
    for i, order in enumerate(market):
        if new_qty[i] is None:
            out.append(order)
        elif new_qty[i] > 0:
            out.append([*order[:2], new_qty[i], *order[3:]])  # 只改 qty，尾部字段如有保留
        # new_qty[i]==0 → 整单消失（不入表，位置序自然保持）
    return out


def _cxs_seed_balance(crop, observation, kept_orders, plan_view, current_plants: int | None = None):
    """零误杀核心（v3，R12）：目标保有量 R=max(0,需求−(有效库存+磁带未来购买))+反应层安全边；解析失败→None。

    返回 int=该品项本回合 BUY_SEED 的目标保有量 R（上游 _cxs_reduce_orders 按
    只减不加把本回合购买量减至 R；R≥本回合购买总量 → 上游零动作）；None=不确定
    =该品项原样（宁多买）；R=0 ≡ 确证全减（与 None 异义）。
    demand = _cxs_completable_plant_demand(crop, observation, plan_view)，其
    None → 本函数 None。供给口径沿 L1 三路（R11 门禁实证：磁带未来购买计入
    供给在回买方向安全），但本回合购买量不入供给式——目标保有量语义的等价式：
      R = max(0, demand − (held_effective + tape_future)) + 安全边
    （= "赤字 max(0, demand−供给+本回合量)"：本回合量在"供给=三路相加"式与
    赤字式中两侧相消，即不把本回合购买当供给重复计算。）
      1) 有效库存 held_effective = max(0, 库存 − current_plants)：字段路径取基座
         同款 observation["private"]["seeds"].get(crop, 0)（orderbook_derivative/
         main.py L6775/L4607/L4693）；严格数型校验（bool/字符串数字/半值 float
         视为类型异常）；current_plants=None=当前步消耗未知 → 直接 None（引擎
         结算序：同 step PLANT 消耗先于买单入账）；超扣钳 0 不为负。
      2) 磁带未来购买 tape_future：plan_view 结果中步 t>observation["step"] 各
         条目 buy_seed.get(crop, 0) 之和（纯函数优先：demand 已调一次 plan_view，
         这里再调一次，用与 demand 完全相同的求和语义重算需求交叉核对，两次
         结果不一致 → None）；结构与 demand 同规校验（畸形 → None）。
      3) 反应层安全边（R12 新增，治"买少"——法证 R11 670 形实种 2>磁带视 1，
         反应层种植磁带不可见）：margin = clamp(_cxs_observed_plant_rate(
         observation, crop, _CXS_SAFETY_LOOKBACK_STEPS, plan_view), 0,
         max(_CXS_SAFETY_MIN_MARGIN, demand))；速率不可解析 → None（不确定=
         该品项原样）。安全边有界（≤ max(2, demand)），多买方向=铁律安全向。
    kept_orders 解析沿 L1 供给路 2 的严格纪律，差异=R11 669 形修正：`[]`/None
    空槽垫单可忽略（跳过不计入 kept_buy 也不触发 None）；非空但 len<3 或畸形
    （非序列/qty 非整数）仍 → None（解析不完整=不确定）。kept_buy 本身不入 R
    等价式（本函数保留该解析走查=契约面：订单集不可解析时整品项不确定）。
    逐步自洽（R12 对规格"跨步台账"条款的实现简化，构建层与 JOURNAL 登记
    偏差）：无跨步台账——每步按当前库存/磁带/在田状态重算 R；减量语义下被减
    订单即时改变当步供给面（持有的种子留下、废单消失），逐步重算无重复计入。
    其余任何读取/解析异常 → None（零误杀：一切不确定 → None → 该品项原样）。
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

        # 保留单解析走查（契约面）：[]/None 空槽可忽略（669 形修正）；其余畸形一律 None
        if not isinstance(kept_orders, (list, tuple)):
            return None
        kept_buy = 0
        for order in kept_orders:
            if order is None or (isinstance(order, (list, tuple)) and len(order) == 0):
                continue  # 空槽垫单：可忽略占位（不计数、不触发不确定）
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                return None
            if order[0] == "BUY_SEED" and order[1] == crop:
                kept_buy += _strict_count(order[2])
        # kept_buy 不入 R 等价式（见 docstring：本回合量两侧相消），仅为解析校验

        held_effective = held - plants_now  # 当前步 PLANT 先于买单入账：扣减
        if held_effective < 0:
            held_effective = 0  # 超扣钳 0（plants>held 不得产生负供给）
        deficit = demand - (held_effective + tape_buy)
        if deficit < 0:
            deficit = 0  # 供给覆盖需求 → 赤字 0（R 退化为纯安全边）

        margin = _cxs_observed_plant_rate(
            observation, crop, _CXS_SAFETY_LOOKBACK_STEPS, plan_view)
        if margin is None:
            return None  # 观测速率不可解析=不确定=该品项原样（宁多买）
        cap = demand if demand > _CXS_SAFETY_MIN_MARGIN else _CXS_SAFETY_MIN_MARGIN
        if margin > cap:
            margin = cap  # clamp 上界：max(2, demand)
        if margin < 0:
            margin = 0  # clamp 下界 0（反应层少种不产生负安全边）
        return deficit + margin
    except Exception:
        return None


def _cxs_observed_plant_rate(observation, crop, lookback_steps=24, plan_view=None):
    """反应层实种速率观测（v3 新增，R12）：近 lookback 步实种数−磁带视计划种数；解析失败→None。

    观测面（R11 法证 670 形：反应层种植对磁带不可见，实种 2>磁带视 1——本函数
    是安全边 _cxs_seed_balance 的唯一数据源）：我方 farms 地块 tiles[y][x] 中
    kind=="PLANT" 且 crop 匹配且 planted_day ≥ 当前day − lookback_steps/24 的
    株数（引擎 kaggressure.py L220：PLANT 记 planted_day=当日，day=step//24 天
    粒度）。地块 None（空槽）/"LOCKED" 字串为 schema 合法占位可忽略；其余非
    dict 地块=结构畸形 → None；本品项 PLANT 地块缺 planted_day/非数 → None。
    磁带视面（规格设计自由条款：现算）：plan_view 形参（None=回退模块级
    _cxs_plan_view）结果中 step < t ≤ step+lookback_steps 的 plants 该品项
    计数和——与观测面等长的前视窗，速率同量纲比对（磁带计划数不含反应层
    超种，差>0 即超种证据）。返回 实种数−计划数（可为负：反应层少种时差为
    负，由上游 clamp 0）；任何读取/解析异常 → None（上游按不确定处理：宁多买）。
    """
    try:
        if not isinstance(observation, dict):
            return None

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

        step = _strict_count(observation.get("step"))
        seat = _strict_count(observation.get("player", 0))
        farms = observation.get("farms")
        if not isinstance(farms, (list, tuple)):
            return None
        farm = farms[seat] if 0 <= seat < len(farms) else None
        if not isinstance(farm, dict):
            return None
        tiles = farm.get("tiles")
        if not isinstance(tiles, (list, tuple)):
            return None
        threshold_day = step // 24 - lookback_steps / 24  # 天粒度阈值（可为半日）
        observed = 0
        for row in tiles:
            if not isinstance(row, (list, tuple)):
                return None
            for tile in row:
                if tile is None or isinstance(tile, str):
                    continue  # 空槽/"LOCKED" 占位可忽略（与订单 [] 同归类）
                if not isinstance(tile, dict):
                    return None  # 其余非 dict 地块=结构畸形=不确定
                if tile.get("kind") != "PLANT" or tile.get("crop") != crop:
                    continue
                planted_day = _strict_count(tile.get("planted_day"))
                if planted_day >= threshold_day:
                    observed += 1

        view = plan_view if plan_view is not None else _cxs_plan_view
        tape = view(observation)
        if not isinstance(tape, dict):
            return None
        planned = 0
        for t, entry in tape.items():
            if isinstance(t, bool) or not isinstance(t, (int, float)):
                return None
            if isinstance(t, float):
                if not t.is_integer():
                    return None
                t = int(t)
            if not (step < t <= step + lookback_steps):
                continue
            if not isinstance(entry, dict):
                return None
            plants = entry.get("plants", {})
            if not isinstance(plants, dict):
                return None
            planned += _strict_count(plants.get(crop, 0))
        return observed - planned
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
    """运行时入口（v3，R12；注入后为 main.py 最后 callable=官方入口）：宿主取动作→step≥_CXS_FROM 交减量层。

    先例=层 D main.py L6909：宿主调用在 try 之外——`action = _CXS_HOST(observation,
    configuration)`（_CXS_HOST=注入时基座最后 callable=orderbook 版 _cxd_agent）；宿主
    异常向上传播，宿主坏了不是本层责任。try 内三步（fail-safe：任何异常→原样返回
    宿主 action，绝不崩）：
      1) step==0 复位钩子（v3：本层无跨步台账——R12 逐步自洽设计，每步按当前
         观测重算目标保有量 R，无跨步状态可复位；保留占位注释，未来引入跨步
         状态时在此复位）；
      2) step≥_CXS_FROM（构建期注入 648/600）且 action 是 dict 且 action["market"]
         含 BUY_SEED（订单匹配对齐 L1：list/tuple、len≥3、首元 "BUY_SEED"）→
         _cxs_reduce_orders(observation, action, _cxs_plan_view)，返回
         dict(action, market=filtered)（内联 plan_view 适配器见上）；
      3) 其余一切情况（step<窗口界 / action 非 dict / market 缺失·非 list / 无
         BUY_SEED / 减量链异常）→ 原样返回宿主 action（同对象零足迹）。
    独立测试态 _CXS_HOST=None（宿主不存在）：测试经 monkeypatch 本模块 _CXS_HOST /
    _cxs_plan_view / _cxs_reduce_orders 注入假件（_cxs_agent 按名取模块全局，补丁即生效）。
    """
    action = _CXS_HOST(observation, configuration)  # 宿主调用在 try 之外（层 D L6909 先例）
    try:
        step = int(observation.get("step", 0))
        if step == 0:
            pass  # 复位钩子：本层无跨步台账（R12 逐步自洽）；未来引入跨步状态时在此复位
        if step >= _CXS_FROM and isinstance(action, dict):
            market = action.get("market")
            if isinstance(market, list) and any(
                isinstance(order, (list, tuple)) and len(order) >= 3 and order[0] == "BUY_SEED"
                for order in market
            ):
                filtered = _cxs_reduce_orders(observation, action, _cxs_plan_view)
                return dict(action, market=filtered)
        return action
    except Exception:
        return action
