"""make_layer_s_v3_block（R12 L1）：L1 块→v3 块，受控变更集（AST 白名单）+审计。

受控变更集（requirements R12 / responsibility【R12 增补】+ 2026-09-24 路由解耦修正，白名单恰合判定）：
  删 def _cxs_seed_truncate / _cxs_seed_surplus；
  加 def _cxs_reduce_orders / _cxs_seed_balance / _cxs_observed_plant_rate + 安全边常数组
  + 常数 _CXS_ROUTE_BOUNDARY = 648（基座 day-27 强制 2 号路的硬事实，与截断窗口无关）；
  改 def _cxs_agent 函数体（过滤调用改 _cxs_reduce_orders+复位钩子注释）、def _cxs_plan_view
  函数体单点常数引用替换（路由切换行 routes[2 if t >= _CXS_FROM …] 改引 _CXS_ROUTE_BOUNDARY
  ——先验 bug 修正：窗口注入不得影响磁带路由视图，w600 在 t∈[600,648) 须读本席路由）、
  与 _CXS_FROM 常数值（window 构建期注入，仅截断/快道判定，648 主跑/600 附加跑）；
  其余一切（_cxs_completable_plant_demand/_cxs_harvest_completable/其余常数与文本含注释空行）
  逐字节恒等；白名单外差异→抛；末顶层 def 仍 _cxs_agent。
审计两层：① 字节层——产物必须逐字节等于确定性拼接 _construct(l1, window)；② 语义层——AST 顶层
语句 {删/增/改} 集合恰等于白名单、匹配语句保序且非白名单语句逐字节恒等、_CXS_FROM 恰 648→window。"""

import ast
import hashlib
from pathlib import Path

# ---- 受控变更集白名单（audit 恰合判定的唯一真值；与 responsibility R12 + 路由解耦修正一一对应）----
_DELETED_FUNCTIONS = ("_cxs_seed_truncate", "_cxs_seed_surplus")
_ADDED_FUNCTIONS = ("_cxs_reduce_orders", "_cxs_seed_balance", "_cxs_observed_plant_rate")
_MODIFIED_FUNCTIONS = ("_cxs_agent", "_cxs_plan_view")  # plan_view=路由行单点常数引用替换
_ADDED_CONSTANTS = ("_CXS_SAFETY_LOOKBACK_STEPS", "_CXS_SAFETY_MIN_MARGIN", "_CXS_ROUTE_BOUNDARY")
_MODIFIED_CONSTANT = "_CXS_FROM"
_L1_WINDOW_BASE = 648
_ROUTE_BOUNDARY_VALUE = 648  # 基座 day-27（step 648）起强制 2 号路：硬事实，非参数
_LAST_TOP_DEF_EXPECTED = "_cxs_agent"
_SEASON_LAST_STEP = 718  # _CXS_SEASON_END 契约值：窗口界不得越过季末（越过=死代码层）

# 路由边界常数行（随 _CXS_FROM 行后插入常数区；单行 Assign+行内注释——区间剥离不漏胶水）。
_ROUTE_BOUNDARY_LINE = (
    f"_CXS_ROUTE_BOUNDARY = {_ROUTE_BOUNDARY_VALUE}"
    "  # 基座 day-27（step 648）起强制 2 号路：硬事实，与截断窗口解耦（R12 修正）\n"
)

# plan_view 路由解耦替换对（L1 源内恰各出现一次，由 _construct 守卫；代码行+docstring 引用处
# 同一语义变更的两处文本出现）。
_ROUTE_LINE_OLD = "routes[2 if t >= _CXS_FROM else route]"
_ROUTE_LINE_NEW = "routes[2 if t >= _CXS_ROUTE_BOUNDARY else route]"
_DOC_REF_OLD = "（t≥_CXS_FROM）"
_DOC_REF_NEW = "（t≥_CXS_ROUTE_BOUNDARY）"

# v3 安全边常数组（R12 构建期随变更集加入；单行 Assign+行内注释——行内注释属于
# Assign 行区间，审计的区间剥离不漏胶水，故此处不带独立注释行）。安全边语义见
# _cxs_seed_balance。
V3_SAFETY_CONSTS_SRC = (
    "_CXS_SAFETY_LOOKBACK_STEPS = 24  # R12 安全边：观测窗（步）=磁带前视窗（1 天粒度定桩）\n"
    "_CXS_SAFETY_MIN_MARGIN = 2       # R12 安全边下限（宁多买一颗 $20，不饿死一茬）\n"
)

# 减量过滤主函数（替换 L1 _cxs_seed_truncate 的函数体区间；骨架沿 L1：窗口快道/
# 品项分组/从后往前，差异=逐单减量而非整单删除）。
V3_REDUCE_SRC = '''def _cxs_reduce_orders(observation, action, plan_view):
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
'''

# 减量目标保有量核心（替换 L1 _cxs_seed_surplus 的函数体区间头部）。
V3_BALANCE_SRC = '''def _cxs_seed_balance(crop, observation, kept_orders, plan_view, current_plants: int | None = None):
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
'''

# 反应层实种速率观测（新增函数，拼接于 _cxs_seed_balance 之后）。
V3_PLANT_RATE_SRC = '''def _cxs_observed_plant_rate(observation, crop, lookback_steps=24, plan_view=None):
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
'''

# 运行时入口（替换 L1 _cxs_agent 的函数体区间：过滤调用改 _cxs_reduce_orders，
# 复位钩子注释更新为无台账占位；窗口界读 _CXS_FROM 构建期注入值）。
V3_AGENT_SRC = '''def _cxs_agent(observation, configuration=None):
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
'''


def _top_statements(tree):
    """顶层语句清单 [(kind, key, node)]：FunctionDef 按名 / 单 Name 目标赋值（Assign
    与 AnnAssign——L1 的 FIRST_HARVEST_STEPS: dict = {...} 是带注解赋值）按名 /
    其余（docstring/宿主捕获语句等）按位。"""
    out, others = [], 0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out.append(("def", node.name, node))
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            out.append(("const", node.targets[0].id, node))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.append(("const", node.target.id, node))
        else:
            out.append(("other", others, node))
            others += 1
    return out


def _find_unique(stmts, kind, name, label):
    matches = [node for k, n, node in stmts if k == kind and n == name]
    if len(matches) != 1:
        raise ValueError(f"{label}: expected exactly one top-level {kind} {name!r}, found {len(matches)}")
    return matches[0]


def _line_span(text, lineno, end_lineno):
    """1-based 闭行区间的逐字节源片段（含行尾换行）。"""
    return "".join(text.splitlines(keepends=True)[lineno - 1:end_lineno])


def _line_offset(text, lineno):
    """行号（1-based）行首的字节偏移；行号超界=文末。"""
    lines = text.splitlines(keepends=True)
    if lineno > len(lines):
        return len(text)
    return sum(len(line) for line in lines[:lineno - 1])


def _int_constant(node):
    """赋值语句（Assign/AnnAssign）的整数值（严格 int 非 bool）；非常数/非 int → None。"""
    value = node.value
    if isinstance(value, ast.Constant) and type(value.value) is int:
        return value.value
    return None


def _guard_embedded_sources():
    """嵌入源结构守卫（防拼接面漂移）：各源恰一条目标顶层 def / 恰两行安全边常数
    （_CXS_ROUTE_BOUNDARY 行独立于安全边组，由 _ROUTE_BOUNDARY_LINE 单独携带）。"""
    for label, src, name in (
        ("V3_REDUCE_SRC", V3_REDUCE_SRC, "_cxs_reduce_orders"),
        ("V3_BALANCE_SRC", V3_BALANCE_SRC, "_cxs_seed_balance"),
        ("V3_PLANT_RATE_SRC", V3_PLANT_RATE_SRC, "_cxs_observed_plant_rate"),
        ("V3_AGENT_SRC", V3_AGENT_SRC, "_cxs_agent"),
    ):
        tree = ast.parse(src)
        defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if len(tree.body) != 1 or len(defs) != 1 or defs[0].name != name:
            raise ValueError(f"{label}: expected exactly one top-level def {name!r}")
    safety_names = [n for n in _ADDED_CONSTANTS if n != "_CXS_ROUTE_BOUNDARY"]
    consts_tree = ast.parse(V3_SAFETY_CONSTS_SRC)
    names = [n.targets[0].id for n in consts_tree.body
             if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)]
    if len(consts_tree.body) != len(safety_names) or names != safety_names:
        raise ValueError(f"V3_SAFETY_CONSTS_SRC: expected exactly two assigns {safety_names}")
    # 路由边界常数行：恰一条 _CXS_ROUTE_BOUNDARY 赋值且值=648
    boundary_tree = ast.parse(_ROUTE_BOUNDARY_LINE)
    boundary_names = [n.targets[0].id for n in boundary_tree.body
                      if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)]
    if (len(boundary_tree.body) != 1 or boundary_names != ["_CXS_ROUTE_BOUNDARY"]
            or _int_constant(boundary_tree.body[0]) != _ROUTE_BOUNDARY_VALUE):
        raise ValueError("_ROUTE_BOUNDARY_LINE: expected one _CXS_ROUTE_BOUNDARY = "
                         f"{_ROUTE_BOUNDARY_VALUE} assign")
    # 拼接形态（balance+rate 同区间相邻）可解析
    ast.parse(V3_BALANCE_SRC + "\n\n" + V3_PLANT_RATE_SRC)


def _construct(l1_text, window):
    """确定性拼接：L1 源 + 白名单六处改写 → v3 源（区间外一切字节逐字节继承）。

    六处改写（字节偏移升序一次拼接，无重叠）：
      ① _CXS_FROM 赋值行 → 注入 window + 追加 _CXS_ROUTE_BOUNDARY 常数行；
      ② FIRST_HARVEST_STEPS 之后零宽插入安全边常数组；③ _cxs_plan_view 区间内
      路由行与 docstring 引用单点常数替换（_CXS_FROM→_CXS_ROUTE_BOUNDARY，各恰
      一次出现守卫）；④ _cxs_seed_truncate 区间 → V3_REDUCE_SRC；
      ⑤ _cxs_seed_surplus 区间 → balance+rate；⑥ _cxs_agent 区间 → V3_AGENT_SRC。
    L1 结构异常（定位失败/_CXS_FROM 非 648/路由行非唯一）即抛（fail-closed，写入前）。"""
    tree = ast.parse(l1_text)
    stmts = _top_statements(tree)
    keys = [(k, n) for k, n, _ in stmts]
    if len(keys) != len(set(keys)):
        raise ValueError("L1 block: duplicate top-level key")
    fn_plan_view = _find_unique(stmts, "def", "_cxs_plan_view", "L1 block")
    fn_truncate = _find_unique(stmts, "def", "_cxs_seed_truncate", "L1 block")
    fn_surplus = _find_unique(stmts, "def", "_cxs_seed_surplus", "L1 block")
    fn_agent = _find_unique(stmts, "def", "_cxs_agent", "L1 block")
    const_from = _find_unique(stmts, "const", "_CXS_FROM", "L1 block")
    const_fhs = _find_unique(stmts, "const", "FIRST_HARVEST_STEPS", "L1 block")
    if _int_constant(const_from) != _L1_WINDOW_BASE:
        raise ValueError(f"L1 block: _CXS_FROM is not int {_L1_WINDOW_BASE} (contract drift)")
    # plan_view 区间内路由解耦（先验 bug 修正）：路由行与 docstring 引用各恰一次。
    pv_lo = _line_offset(l1_text, fn_plan_view.lineno)
    pv_hi = _line_offset(l1_text, fn_plan_view.end_lineno + 1)
    pv_body = l1_text[pv_lo:pv_hi]
    if pv_body.count(_ROUTE_LINE_OLD) != 1:
        raise ValueError(
            f"L1 block: expected exactly one route switch line in _cxs_plan_view, "
            f"found {pv_body.count(_ROUTE_LINE_OLD)}")
    if pv_body.count(_DOC_REF_OLD) != 1:
        raise ValueError(
            f"L1 block: expected exactly one docstring boundary reference in "
            f"_cxs_plan_view, found {pv_body.count(_DOC_REF_OLD)}")
    pv_new = pv_body.replace(_ROUTE_LINE_OLD, _ROUTE_LINE_NEW).replace(_DOC_REF_OLD, _DOC_REF_NEW)
    cuts = [
        (_line_offset(l1_text, const_from.lineno),
         _line_offset(l1_text, const_from.end_lineno + 1),
         f"_CXS_FROM = {window}\n" + _ROUTE_BOUNDARY_LINE),
        (_line_offset(l1_text, const_fhs.end_lineno + 1),
         _line_offset(l1_text, const_fhs.end_lineno + 1), V3_SAFETY_CONSTS_SRC),
        (pv_lo, pv_hi, pv_new),
        (_line_offset(l1_text, fn_truncate.lineno),
         _line_offset(l1_text, fn_truncate.end_lineno + 1), V3_REDUCE_SRC),
        (_line_offset(l1_text, fn_surplus.lineno),
         _line_offset(l1_text, fn_surplus.end_lineno + 1),
         V3_BALANCE_SRC + "\n\n" + V3_PLANT_RATE_SRC),
        (_line_offset(l1_text, fn_agent.lineno),
         _line_offset(l1_text, fn_agent.end_lineno + 1), V3_AGENT_SRC),
    ]
    cuts.sort()
    parts, cursor = [], 0
    for lo, hi, replacement in cuts:
        if lo < cursor:
            raise ValueError("construct: splice overlap (L1 structure drift)")
        parts.append(l1_text[cursor:lo])
        parts.append(replacement)
        cursor = hi
    parts.append(l1_text[cursor:])
    return "".join(parts)


def _audit_change_set(l1_text, v3_text, window):
    """受控变更集审计：白名单恰合；违例抛 ValueError（SyntaxError 定向收编），返回变更集摘要。

    两层：① 字节层——v3_text 必须逐字节等于 _construct(l1_text, window)（白名单
    改写区外一切字节——含注释与空行——逐字节继承 L1）；② 语义层——AST 顶层语句
    {删/增/改} 集合恰等于白名单、匹配语句保序、非白名单语句逐字节恒等、
    _CXS_FROM 值恰 648→window、路由解耦不变式（plan_view 无 _CXS_FROM 引用且
    _CXS_ROUTE_BOUNDARY==648）、末顶层 def 仍 _cxs_agent。"""
    try:
        l1_tree = ast.parse(l1_text)
        v3_tree = ast.parse(v3_text)
    except SyntaxError as exc:
        raise ValueError(f"change-set audit: parse failure: {exc}") from exc

    # ① 字节层：确定性重建逐字节等值（白名单外差异=任何来源的漂移在此全捕获）
    if v3_text != _construct(l1_text, window):
        raise ValueError("change-set audit: byte drift outside controlled change set")

    # ② 语义层：顶层语句分类恰合白名单
    l1_stmts = _top_statements(l1_tree)
    v3_stmts = _top_statements(v3_tree)
    for label, stmts in (("L1", l1_stmts), ("v3", v3_stmts)):
        keys = [(k, n) for k, n, _ in stmts]
        if len(keys) != len(set(keys)):
            raise ValueError(f"change-set audit: duplicate top-level key in {label}")
    l1_map = {(k, n): node for k, n, node in l1_stmts}
    v3_map = {(k, n): node for k, n, node in v3_stmts}
    l1_keys, v3_keys = set(l1_map), set(v3_map)
    deleted = l1_keys - v3_keys
    added = v3_keys - l1_keys
    if deleted != {("def", name) for name in _DELETED_FUNCTIONS}:
        raise ValueError(f"change-set audit: deleted set outside whitelist: {sorted(deleted)}")
    if added != {("def", name) for name in _ADDED_FUNCTIONS} | {("const", name) for name in _ADDED_CONSTANTS}:
        raise ValueError(f"change-set audit: added set outside whitelist: {sorted(added)}")

    modified = []
    for key in sorted(l1_keys & v3_keys):
        a, b = l1_map[key], v3_map[key]
        if _line_span(l1_text, a.lineno, a.end_lineno) != _line_span(v3_text, b.lineno, b.end_lineno):
            modified.append(key)
    expected_modified = {("def", name) for name in _MODIFIED_FUNCTIONS}
    if window != _L1_WINDOW_BASE:
        expected_modified |= {("const", _MODIFIED_CONSTANT)}
    if set(modified) != expected_modified:
        raise ValueError(f"change-set audit: modified set outside whitelist: {sorted(modified)}")

    # 路由解耦不变式（2026-09-24 修正）：plan_view 改写面恰为常数引用替换——
    # v3 的 _cxs_plan_view 体内不得再引用 _CXS_FROM，且路由切换读 _CXS_ROUTE_BOUNDARY。
    v3_pv = v3_map[("def", "_cxs_plan_view")]
    pv_span = _line_span(v3_text, v3_pv.lineno, v3_pv.end_lineno)
    if "_CXS_FROM" in pv_span or _ROUTE_LINE_NEW not in pv_span:
        raise ValueError("change-set audit: _cxs_plan_view route switch not decoupled from window")
    boundary_node = v3_map.get(("const", "_CXS_ROUTE_BOUNDARY"))
    if boundary_node is None or _int_constant(boundary_node) != _ROUTE_BOUNDARY_VALUE:
        raise ValueError(
            f"change-set audit: _CXS_ROUTE_BOUNDARY missing or != {_ROUTE_BOUNDARY_VALUE}")

    l1_seq = [key for key in [(k, n) for k, n, _ in l1_stmts] if key in v3_keys]
    v3_seq = [key for key in [(k, n) for k, n, _ in v3_stmts] if key in l1_keys]
    if l1_seq != v3_seq:
        raise ValueError("change-set audit: matched statement order drifted")

    l1_window = _int_constant(l1_map[("const", _MODIFIED_CONSTANT)])
    v3_window = _int_constant(v3_map[("const", _MODIFIED_CONSTANT)])
    if l1_window != _L1_WINDOW_BASE or v3_window != window:
        raise ValueError(
            f"change-set audit: _CXS_FROM {l1_window!r}->{v3_window!r} != {_L1_WINDOW_BASE}->{window}")

    top_defs = [n for n in v3_tree.body if isinstance(n, ast.FunctionDef)]
    if not top_defs or top_defs[-1].name != _LAST_TOP_DEF_EXPECTED:
        raise ValueError(f"change-set audit: last top-level def is not {_LAST_TOP_DEF_EXPECTED!r}")

    return {
        "window": window,
        "route_boundary": _ROUTE_BOUNDARY_VALUE,
        "deleted_functions": sorted(name for k, name in deleted),
        "added_functions": sorted(name for k, name in added if k == "def"),
        "added_constants": sorted(name for k, name in added if k == "const"),
        "modified_functions": sorted(name for k, name in modified if k == "def"),
        "modified_constants": {_MODIFIED_CONSTANT: [l1_window, v3_window]},
        "unchanged_top_level": len(l1_keys & v3_keys) - len(modified),
        "last_def": top_defs[-1].name,
    }


def make(l1_block_path=None, out_path=None, window=648) -> dict:
    """生成 v3 块：balance/reduce 重写+plant_rate 新增+[] 归类+窗口参数化；白名单外差异即抛。"""
    if isinstance(window, bool) or not isinstance(window, int) or not 0 < window <= _SEASON_LAST_STEP:
        raise ValueError(f"window must be int in (0, {_SEASON_LAST_STEP}], got {window!r}")
    _guard_embedded_sources()
    here = Path(__file__).resolve().parent
    l1_path = (Path(l1_block_path) if l1_block_path is not None
               else here.parent / "orderbook_l1_derivative" / "layer_s_block.py")
    out = Path(out_path) if out_path is not None else here / f"layer_s_block_v3_w{window}.py"

    l1_text = l1_path.read_text(encoding="utf-8")
    v3_text = _construct(l1_text, window)  # L1 结构异常/常数漂移即抛（写入前 fail-closed）
    change_set_audit = _audit_change_set(l1_text, v3_text, window)  # 白名单外差异即抛（写入前）

    # 追加守卫：改写区逐字节等于嵌入源（防拼接面漂移的双保险）
    v3_stmts = _top_statements(ast.parse(v3_text))
    for name, src in (("_cxs_reduce_orders", V3_REDUCE_SRC),
                      ("_cxs_seed_balance", V3_BALANCE_SRC),
                      ("_cxs_observed_plant_rate", V3_PLANT_RATE_SRC),
                      ("_cxs_agent", V3_AGENT_SRC)):
        node = _find_unique(v3_stmts, "def", name, "v3 block")
        if _line_span(v3_text, node.lineno, node.end_lineno) != src:
            raise ValueError(f"v3 block: spliced segment drifted from embedded source: {name}")
    # 追加守卫：路由解耦在产物内成立（plan_view 引用 _CXS_ROUTE_BOUNDARY、无 _CXS_FROM）
    pv_node = _find_unique(v3_stmts, "def", "_cxs_plan_view", "v3 block")
    pv_span_text = _line_span(v3_text, pv_node.lineno, pv_node.end_lineno)
    if "_CXS_FROM" in pv_span_text or _ROUTE_LINE_NEW not in pv_span_text:
        raise ValueError("v3 block: _cxs_plan_view route switch not decoupled from window")

    out.write_text(v3_text, encoding="utf-8")  # 幂等覆盖写
    return {
        "v3_path": str(out),
        "v3_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "change_set_audit": change_set_audit,
    }
