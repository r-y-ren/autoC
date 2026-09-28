X = 1
Y = 2
import base64, json, zlib
_R108_DATA=json.loads(zlib.decompress(base64.b85decode('c-ozi!3u&v5Qg97KhHs}F5Na7Fw&IPijXCwj3UZVJBjb!Y!R5ZI_<wZ^L@;0gKS@)i(7?p+TfU#*SwU7SZNJIIAynktx3FQ<t48rr_dY(AZ&bA3210cOTWWWB*(~5`WNo2EodM#CadjEEoPyz&)R2>L0-?<v89&r)pE@`f%$UVN>}gwHCZ?d<{-DvZdAg{F8tAbOYAn9d1^%*M2ojcddlKa=fX8`q|qUlJi9+!xeetXTS9dz?ys@hC+1&^3I')))


# ============ r37 现金保底守卫尾块（自动生成，勿手改） ============
# 生成元：orderbook_r37/inject_guard.py::inject_cash_guard_block
# 源真值：orderbook_r37/cash_guard_block.py（三函数源码 ast 整段抽取）
# 命名方案：纯核 _r37_agent（双参数）→ 块内改名 _r37_guard_core（源文件
#   不改名，词边界全量改名含 _defer_ledger 函数属性账自引用，账随函数走）；
#   块尾单参数入口占名 _r37_agent——官方 runner 按模块 globals 最后一个
#   callable 当 agent（action = fn(observation)）。
# 捕获行：先于本块一切 def/import 执行，取注入时刻 globals 既有最后
#   callable=底版基座 agent（层 D _CXD_HOST / layer S _CXS_HOST 同款
#   last-callable 先例；双下划线名排除 Python 3.14 模块样板 __annotate__）。
#   刻意不用 _R37_PARENT：r34a 主干已绑该名并逐步调用，覆写会致链上递归。
# 自包含：stdlib only；typing 缺省填充置捕获行之后（Dict/Any 皆 callable，
#   不得抢 globals 末位）且不覆盖底版既有绑定。
# =================================================================

_R37_GUARD_CALLABLES = [v for k, v in list(globals().items())
                        if callable(v) and not (k.startswith("__") and k.endswith("__"))]
_R37_GUARD_PARENT = _R37_GUARD_CALLABLES[-1] if _R37_GUARD_CALLABLES else None

import typing as _r37_guard_typing
if "Any" not in globals():
    Any = _r37_guard_typing.Any
if "Dict" not in globals():
    Dict = _r37_guard_typing.Dict


def _r37_guard_core(observation: Dict[str, Any], base_action: Dict[str, Any]) -> Dict[str, Any]:
    """尾块捕获入口：取基座动作→交 _r37_cash_guard 调整→返回同构 action。

    动作集合不变量：只顺延/删减购买类单，不新增动作、不动 HARVEST 与卖单；
    任何异常→基座动作原样返回（fail-safe）；step==0 复位层内缓存（顺延账）。

    签名意图：输入: observation, base_action / 输出: 调整后 action /
    错误: 异常→入口兜底回退基座动作。

    结构定义（本层定形，_r37_cash_guard 对齐；R19 核心增量=顺延账跨步重试，
    顺延不是删除、是择机重发——修「3 张 BUY_ANIMAL 被引擎静默丢弃」）：
    - 顺延账缓存 = 本函数属性 _r37_guard_core._defer_ledger（list；条目同
      _r37_defer_low_priority 顺延账 {"op","item","qty","cost","slot"}，条目
      序=顺延序）。函数属性自包含、随源码注入不丢、不与注入底版 globals 撞名。
      step==0 复位（清空携带意图）；复位/出账/入账统一在流程成功后原子提交，
      任何异常→账保持调用前状态（账读写自身 try 包裹，可静默、不许抛）。
    - 每步流程：(a) step==0 复位账（先于重试，携带意图不再回填）；(b) 重试
      阶段——账中 BUY_ANIMAL 意图按顺延序，若本步执行点现金达标（≥buy_animal
      线 500，与 _r37_cash_guard 同口径：当前资金−HIRE fib 硬开销−保留购买单
      全价，卖单收入不计）→ 重发进 market 空 [] 槽（market 序首个空槽起步，
      执行点现金随槽序单调不增故首空槽=最优执行点；不改槽位数、不挤掉任何
      既有单；无空槽或现金不达标→本步不重试、意图留账）；(c) 守卫阶段——把
      （含回填的）action 交 _r37_cash_guard（floors={"d0_end":12,
      "buy_animal":500,"hard_min":4}）调整；(d) 合并顺延账——回填成功的出账、
      守卫新顺延入账（交守卫动作 vs adjusted_action 逐槽 diff，被置 [] 的核价
      购买单按 {"op","item","qty","cost","slot"} 重建，defer 同口径）；
      (e) 返回 adjusted_action。
    - 回填判据与守卫 buy_animal 判据同口径同线（at≥500 ⟺ 守卫不触 buy_animal
      ）→ 回填单不会被 buy_animal 支误伤；若 d0_end 等更严下限仍要求顺延，回填
      单随 diff 回流入账、意图不灭。「不新增动作」=不引入账外新意图：回填只
      重发账内既有购买意图、只落空 [] 槽；farmer/hands（动物格 HARVEST/FEED/
      CARE/移动）与 HIRE/卖单一字节不动、槽位数恒定。
    - fail-safe：任何异常→返回 base_action 原对象（连同不动的账）。
    """
    try:
        # ---- 0. 顺延账读取（函数属性缓存；账操作静默） ----
        try:
            cache = _r37_guard_core._defer_ledger
        except Exception:
            cache = None
        if not isinstance(cache, list):
            cache = []

        # ---- 1. step 读取（口径同 _r37_cash_guard）+ step==0 复位 ----
        raw_step = observation["step"]
        if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
            raise TypeError("observation[step] must be a number")
        if raw_step != raw_step or raw_step == float("inf") \
                or raw_step == float("-inf"):
            raise ValueError("observation[step] must be finite")
        step_f = float(raw_step)
        if step_f != int(step_f):
            raise ValueError("observation[step] must be a whole number")
        step = int(step_f)
        working = [] if step == 0 else list(cache)

        # ---- 2. 状态读取（player/farms[seat]，口径同 _r37_cash_guard） ----
        seat = int(observation["player"])
        farm = observation["farms"][seat]
        money_raw = farm["money"]
        if isinstance(money_raw, bool) or not isinstance(money_raw, (int, float)):
            raise TypeError("farm[money] must be a number")
        money = float(money_raw)
        hires_raw = farm.get("hires_today", 0)
        if hires_raw is None:
            hires_raw = 0
        if isinstance(hires_raw, bool) or not isinstance(hires_raw, int) or hires_raw < 0:
            raise TypeError("farm[hires_today] must be a non-negative int")
        hires_today = hires_raw

        # ---- 3. 核价/执行点现金（口径同 _r37_cash_guard） ----
        floors = {"d0_end": 12, "buy_animal": 500, "hard_min": 4}
        hard = max(float(floors["hard_min"]), 4.0)   # 硬底线 4 不可破
        buy_line = max(float(floors["buy_animal"]), hard)
        seed_price = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                      "STRAWBERRY": 100, "MELON": 80}
        animal_cost = {"GOOSE": 300, "COW": 400, "SHEEP": 500}

        def _strict_qty(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if isinstance(value, float):
                if not value.is_integer():
                    return None
                value = int(value)
            return value if value >= 1 else None

        def _price_of(op, item, qty):
            if op == "BUY_SEED" and item in seed_price:
                return qty * seed_price[item]
            if op == "BUY_ANIMAL" and item in animal_cost:
                return qty * animal_cost[item]
            return None

        def _hire_cost(n):
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        def _at_slots(mkt):
            # 逐槽执行点现金 at[]：只扣 HIRE fib 硬开销与保留购买单全价，
            # 卖单收入不计（_project 同口径）。
            cash = money
            at = [cash] * len(mkt)
            hire_idx = 0
            for i, raw in enumerate(mkt):
                at[i] = cash
                if isinstance(raw, (list, tuple)) and raw:
                    op = raw[0]
                    if op == "HIRE":
                        cash -= _hire_cost(hires_today + hire_idx)
                        hire_idx += 1
                    elif len(raw) >= 3 and isinstance(raw[1], str):
                        qty = _strict_qty(raw[2])
                        if qty is not None:
                            cost = _price_of(op, raw[1], qty)
                            if cost is not None:
                                cash -= cost
            return at

        def _is_empty(slot):
            return isinstance(slot, (list, tuple)) and len(slot) == 0

        market = base_action.get("market")
        if market is None:
            market = []
        if not isinstance(market, list):
            raise TypeError("base_action[market] must be a list")

        # ---- 4. 重试阶段：账中 BUY_ANIMAL 择机重发（回填空 [] 槽） ----
        passed = base_action
        refilled_ids = set()
        if working:
            new_market = list(market)   # 回填只出新表，输入动作不被原地改动
            for entry in working:
                if not isinstance(entry, dict) or entry.get("op") != "BUY_ANIMAL":
                    continue            # 重试范围只 BUY_ANIMAL；其余留账不动
                item = entry.get("item")
                qty = _strict_qty(entry.get("qty"))
                if qty is None or item not in animal_cost:
                    continue            # 账目不可核价→留账不动
                free = None
                for i in range(len(new_market)):
                    if _is_empty(new_market[i]):
                        free = i
                        break
                if free is None:
                    break               # 无空槽→本步不重试，意图留账
                if _at_slots(new_market)[free] < buy_line:
                    break               # 现金不达标→留账（后续空槽现金只更少）
                new_market[free] = ["BUY_ANIMAL", item, qty]
                refilled_ids.add(id(entry))
            if refilled_ids:
                passed = dict(base_action, market=new_market)

        # ---- 5. 守卫阶段：（含回填的）动作交 _r37_cash_guard 终裁 ----
        out = _r37_cash_guard(observation, passed, floors)
        guarded = out["adjusted_action"]
        if not isinstance(guarded, dict):
            raise TypeError("adjusted_action must be a dict")

        # ---- 6. 合并顺延账：回填出账+守卫新顺延入账（diff 重建） ----
        try:
            merged = [e for e in working if id(e) not in refilled_ids]
            in_m = passed.get("market")
            out_m = guarded.get("market")
            if isinstance(in_m, list) and isinstance(out_m, list) \
                    and len(in_m) == len(out_m):
                for i, raw in enumerate(in_m):
                    if not _is_empty(out_m[i]):
                        continue
                    if not (isinstance(raw, (list, tuple)) and len(raw) >= 3
                            and isinstance(raw[1], str)):
                        continue
                    qty = _strict_qty(raw[2])
                    cost = _price_of(raw[0], raw[1], qty) if qty is not None else None
                    if cost is None:
                        continue        # 只收核价购买单（defer 同口径）
                    merged.append({"op": raw[0], "item": raw[1], "qty": qty,
                                   "cost": cost, "slot": i})
            _r37_guard_core._defer_ledger = merged
        except Exception:
            pass                        # 账操作失败可静默，不许抛

        # ---- 7. 出口：返回守卫 adjusted_action（同构 action） ----
        return guarded
    except Exception:
        return base_action


def _r37_cash_guard(observation: Dict[str, Any], base_action: Dict[str, Any],
                    floors: Dict[str, Any]) -> Dict[str, Any]:
    """现金下限判定：识别当前步适用下限（①d0 日终窗 step23 前最后动作 ≥12；
    ②BUY_ANIMAL 提交前 ≥500）；触线→交 _r37_defer_low_priority，不触线原样
    放行；下限为可配置常数（判决标定，硬底线 4 不可破）。

    签名意图：输入: observation, base_action, floors /
    输出: {hit_floor, adjusted_action} / 错误: 状态读取失败→不干预原样返回。

    结构定义（本层定形，向下游 _r37_defer_low_priority 对齐）：
    - floors = {"d0_end": 12, "buy_animal": 500, "hard_min": 4}（三键皆必填）：
      d0_end=日终窗下限、buy_animal=BUY_ANIMAL 提交前下限、hard_min=硬底线。
      硬底线 4（=d1 三张 HIRE 价 1+1+2）不可破，处置策略=夹持制：数值型（含
      负数）但 <4 一律夹到 4——effective hard_min=max(4, hard_min)，两下限再与
      之取 max（故 d0_end/buy_animal/hard_min 配 2 或 −100 均按 4 生效，hard_min
      配 20 则两下限至少 20）；类型非法（bool/str/None/list…）或非有限
      （NaN/±inf）→ 视为配置错误→fail-safe 不干预。
    - d0 日终窗 = step 20..23（含）：step 读法沿主干 int(observation["step"])，
      turnsPerDay=24、d0=step//24==0（step 0..23），日终窗=d0 最后 4 拍
      （hour 20..23）；窗外不适用 d0_end。
    - 适用下限：①step 在 d0 日终窗 → d0_end；②base_action 含可核价 BUY_ANIMAL
      单（item∈GOOSE/COW/SHEEP 且 qty 合法，与下游核价口径一致）→ buy_animal；
      同命中取更严（floor 大者，等值取 d0_end）。
    - 现金核算口径与下游一致：当前资金 − HIRE fib 硬开销 − 保留购买单全价，
      卖单收入不计。触线：d0_end=动作后现金 end < floor；buy_animal=任一
      BUY_ANIMAL 单执行点现金 at[i] < floor（单提交前口径）。触线→调下游并折返
      {"hit_floor": <命中的 {"floor","kind"}>, "adjusted_action": 顺延后 action}；
      未触线零足迹 {"hit_floor": None, "adjusted_action": base_action 原对象}
      （下游不被调用）。
    - 异常（obs 缺字段/类型不对、floors 畸形、action 非 dict…）→ 不干预：
      {"hit_floor": None, "adjusted_action": base_action 原对象}。
    """
    try:
        # ---- 0. floors 配置校验+硬底线夹持（非法→抛，由尾兜底 fail-safe） ----
        if not isinstance(floors, dict):
            raise TypeError("floors must be a dict")
        cfg = {}
        for key in ("d0_end", "buy_animal", "hard_min"):
            value = floors[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError("floors[%s] must be a number" % key)
            value = float(value)
            if value != value or value == float("inf") or value == float("-inf"):
                raise ValueError("floors[%s] must be finite" % key)
            cfg[key] = value
        hard = max(cfg["hard_min"], 4.0)   # 硬底线 4 不可破
        floor_d0 = max(cfg["d0_end"], hard)
        floor_ba = max(cfg["buy_animal"], hard)

        # ---- 1. 状态读取（obs 读法沿 _ig_guard_opening：player/farms[seat]） ----
        raw_step = observation["step"]
        if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
            raise TypeError("observation[step] must be a number")
        if raw_step != raw_step or raw_step == float("inf") \
                or raw_step == float("-inf"):
            raise ValueError("observation[step] must be finite")
        step = float(raw_step)
        if step != int(step):
            raise ValueError("observation[step] must be a whole number")
        step = int(step)

        seat = int(observation["player"])
        farm = observation["farms"][seat]
        money_raw = farm["money"]
        if isinstance(money_raw, bool) or not isinstance(money_raw, (int, float)):
            raise TypeError("farm[money] must be a number")
        money = float(money_raw)
        hires_raw = farm.get("hires_today", 0)
        if hires_raw is None:
            hires_raw = 0
        if isinstance(hires_raw, bool) or not isinstance(hires_raw, int) or hires_raw < 0:
            raise TypeError("farm[hires_today] must be a non-negative int")
        hires_today = hires_raw

        # ---- 2. 订单核价+执行点/动作后现金核算（与下游 _project 同口径） ----
        market = base_action.get("market")
        if market is None:
            market = []
        if not isinstance(market, list):
            raise TypeError("base_action[market] must be a list")
        seed_price = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                      "STRAWBERRY": 100, "MELON": 80}
        animal_cost = {"GOOSE": 300, "COW": 400, "SHEEP": 500}

        def _strict_qty(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if isinstance(value, float):
                if not value.is_integer():
                    return None
                value = int(value)
            return value if value >= 1 else None

        parsed = []
        for raw in market:
            entry = None
            if isinstance(raw, (list, tuple)) and raw:
                op = raw[0]
                if op == "HIRE":
                    entry = {"op": "HIRE", "cost": None}
                elif len(raw) >= 3 and isinstance(raw[1], str):
                    qty = _strict_qty(raw[2])
                    if qty is not None and op == "BUY_SEED" and raw[1] in seed_price:
                        entry = {"op": "BUY_SEED", "cost": qty * seed_price[raw[1]]}
                    elif qty is not None and op == "BUY_ANIMAL" and raw[1] in animal_cost:
                        entry = {"op": "BUY_ANIMAL", "cost": qty * animal_cost[raw[1]]}
            parsed.append(entry)

        def _hire_cost(n):
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        cash = money
        at = [cash] * len(parsed)
        hire_idx = 0
        for i, entry in enumerate(parsed):
            at[i] = cash
            if entry is None:
                continue
            if entry["op"] == "HIRE":
                cash -= _hire_cost(hires_today + hire_idx)
                hire_idx += 1
            else:
                cash -= entry["cost"]
        end = cash

        # ---- 3. 适用下限识别+触线判定（双命中取更严，等值取 d0_end） ----
        tripped = []
        if 20 <= step <= 23 and end < floor_d0:
            tripped.append({"floor": floor_d0, "kind": "d0_end"})
        for i, entry in enumerate(parsed):
            if entry is not None and entry["op"] == "BUY_ANIMAL" and at[i] < floor_ba:
                tripped.append({"floor": floor_ba, "kind": "buy_animal"})
                break
        if not tripped:
            return {"hit_floor": None, "adjusted_action": base_action}
        hit_floor = max(tripped, key=lambda h: (h["floor"], h["kind"] == "d0_end"))

        # ---- 4. 委派处置并折返（只判定+委派，本层不改单） ----
        out = _r37_defer_low_priority(observation, base_action, hit_floor)
        return {"hit_floor": hit_floor, "adjusted_action": out["action"]}
    except Exception:
        return {"hit_floor": None, "adjusted_action": base_action}


def _r37_defer_low_priority(observation: Dict[str, Any], action: Dict[str, Any],
                            hit_floor: Any) -> Dict[str, Any]:
    """触线处置：按低优先级顺延——先缓 BUY_SEED（MELON 80 金/粒优先，按订单
    尾序删缓），BUY_ANIMAL 现金不足 500 整单顺延至现金达标步重试（保留意图入
    顺延账，不永久删除）；HIRE（4 金硬开销）与 FEED/CARE/卖单/动物格 HARVEST
    序一律不动；处置后须满足触发下限，一次不够→继续顺延直至达标。

    签名意图：输入: observation, action, hit_floor /
    输出: 顺延后 action+顺延账更新 / 错误: 异常→原动作。

    结构定义（本层定形，_r37_cash_guard 对齐）：
    - hit_floor = {"floor": <非负有限数>, "kind": "d0_end" | "buy_animal"}：
      floor=处置后须满足的现金下限（observation 当前资金 − 保留部分支出 ≥
      floor；保留支出=HIRE fib 递增硬开销 + 保留 BUY_SEED/BUY_ANIMAL 全价，
      卖单收入不计）；kind=触发下限族（识别在 _r37_cash_guard，本层只校验形状）。
    - 返回 {"action": <顺延后 action>, "deferred": <顺延账>}；顺延账条目 =
      {"op": "BUY_SEED"|"BUY_ANIMAL", "item": <作物|牲畜>, "qty": <int 整单量>,
      "cost": <该单现金支出>, "slot": <原 market 槽位>}（条目序=顺延序）。
    - 顺延=被缓槽置 [] 空槽（保槽位数与位置语义，禁删槽）；无顺延（含尽力后
      仍不足）→ action 原对象返回（零足迹）。
    - 异常（action/hit_floor/状态畸形、字段缺失）→ {"action": 原action,
      "deferred": []}（不干预）。
    """
    try:
        # ---- 0. 形状/状态校验：任一不符即抛，由本函数兜底不干预 ----
        if not isinstance(action, dict):
            raise TypeError("action must be a dict")
        if not isinstance(hit_floor, dict):
            raise TypeError("hit_floor must be a dict")
        floor_raw = hit_floor.get("floor")
        if isinstance(floor_raw, bool) or not isinstance(floor_raw, (int, float)):
            raise TypeError("hit_floor[floor] must be a number")
        floor = float(floor_raw)
        if floor != floor or floor == float("inf") or floor < 0.0:
            raise ValueError("hit_floor[floor] must be finite and >= 0")
        kind = hit_floor.get("kind")
        if not isinstance(kind, str) or not kind:
            raise TypeError("hit_floor[kind] must be a non-empty str")

        market = action.get("market")
        if market is None:
            market = []
        if not isinstance(market, list):
            raise TypeError("action[market] must be a list")

        seat = int(observation["player"])
        farm = observation["farms"][seat]
        money_raw = farm["money"]
        if isinstance(money_raw, bool) or not isinstance(money_raw, (int, float)):
            raise TypeError("farm[money] must be a number")
        money = float(money_raw)
        hires_raw = farm.get("hires_today", 0)
        if hires_raw is None:
            hires_raw = 0
        if isinstance(hires_raw, bool) or not isinstance(hires_raw, int) or hires_raw < 0:
            raise TypeError("farm[hires_today] must be a non-negative int")
        hires_today = hires_raw

        # ---- 1. 订单核价（引擎口径，只认 BUY_SEED/BUY_ANIMAL/HIRE 三类） ----
        # 价目=引擎常数转录（kaggriculture.py CROPS["seed"]/ANIMALS["cost"]）：
        # 种子 WHEAT10/CARROT20/TOMATO50/MELON80/STRAWBERRY100，牲畜
        # GOOSE300/COW400/SHEEP500；HIRE=当日第 n 次 fib(n)（1,1,2,3,5…，
        # 三张=1+1+2=4 金硬开销）。数量纪律沿 layer_s _strict_count：int（非
        # bool）原样、整值 float 折 int，bool/str/None/半值 float/非正 → 不核
        # 价不顺延（引擎 _parse_order 同口径丢弃）。SELL/BUY_PRODUCT/BUY_LAND
        # /空槽/未知 op 一律不核价不顺延（一个字节不动）。
        seed_price = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                      "STRAWBERRY": 100, "MELON": 80}
        animal_cost = {"GOOSE": 300, "COW": 400, "SHEEP": 500}

        def _strict_qty(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if isinstance(value, float):
                if not value.is_integer():
                    return None
                value = int(value)
            return value if value >= 1 else None

        parsed = []
        for raw in market:
            entry = None
            if isinstance(raw, (list, tuple)) and raw:
                op = raw[0]
                if op == "HIRE":
                    entry = {"op": "HIRE", "item": None, "qty": 1, "cost": None}
                elif len(raw) >= 3 and isinstance(raw[1], str):
                    qty = _strict_qty(raw[2])
                    if qty is not None and op == "BUY_SEED" and raw[1] in seed_price:
                        entry = {"op": "BUY_SEED", "item": raw[1], "qty": qty,
                                 "cost": qty * seed_price[raw[1]]}
                    elif qty is not None and op == "BUY_ANIMAL" and raw[1] in animal_cost:
                        entry = {"op": "BUY_ANIMAL", "item": raw[1], "qty": qty,
                                 "cost": qty * animal_cost[raw[1]]}
            parsed.append(entry)

        def _hire_cost(n):
            # 引擎 _fib/_hire_cost 同式：第 n 次（今日已雇 n 人）= fib(n)。
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        def _project(mask):
            # 逐槽执行点现金 at[]（引擎按槽位序结算）与本动作后现金 end
            # （只扣保留部分支出：HIRE 必保 + 保留购买单照常花）。
            cash = money
            at = [cash] * len(parsed)
            hire_idx = 0
            for i, entry in enumerate(parsed):
                at[i] = cash
                if mask[i] or entry is None:
                    continue
                if entry["op"] == "HIRE":
                    cash -= _hire_cost(hires_today + hire_idx)
                    hire_idx += 1
                else:
                    cash -= entry["cost"]
            return at, cash

        # ---- 2. 顺延循环：先缓 BUY_SEED（MELON 尾序→其余种子尾序）→ BUY_ANIMAL
        # 整单，直至 end ≥ floor 或无单可缓；随后 BUY_ANIMAL 现金不足 500（引擎
        # 丢单线 400/400/500 的保守统一线）整单入账，保意图不永久删除。
        mask = [False] * len(parsed)
        deferred = []
        animal_line = 500

        def _defer(slot):
            mask[slot] = True
            entry = parsed[slot]
            deferred.append({"op": entry["op"], "item": entry["item"],
                             "qty": entry["qty"], "cost": entry["cost"],
                             "slot": slot})

        while True:
            at, end = _project(mask)
            pick = None
            if end < floor:
                for rung in ("melon", "seed", "animal"):
                    for i in range(len(parsed) - 1, -1, -1):
                        entry = parsed[i]
                        if mask[i] or entry is None:
                            continue
                        if rung == "melon" and entry["op"] == "BUY_SEED" \
                                and entry["item"] == "MELON":
                            pick = i
                            break
                        if rung == "seed" and entry["op"] == "BUY_SEED":
                            pick = i
                            break
                        if rung == "animal" and entry["op"] == "BUY_ANIMAL":
                            pick = i
                            break
                    if pick is not None:
                        break
            if pick is None:
                for i in range(len(parsed) - 1, -1, -1):
                    entry = parsed[i]
                    if (not mask[i] and entry is not None and entry["op"] == "BUY_ANIMAL"
                            and at[i] < animal_line):
                        pick = i
                        break
            if pick is None:
                break
            _defer(pick)

        # ---- 3. 出口：零顺延=原对象零足迹；有顺延=仅被缓槽置 []，其余原对象 ----
        if not deferred:
            return {"action": action, "deferred": []}
        new_market = [[] if mask[i] else raw for i, raw in enumerate(market)]
        return {"action": dict(action, market=new_market), "deferred": deferred}
    except Exception:
        return {"action": action, "deferred": []}


def _r37_agent(observation):
    '''单参数入口适配（官方 runner 语义：action = last_callable(observation)）。

    base_action = _R37_GUARD_PARENT(observation)（块首捕获的底版基座
    agent）取基座动作，再转调纯核 _r37_guard_core(observation, base_action)
    （cash_guard_block.py _r37_agent 的块内改名；fail-safe：纯核任何异常
    →基座动作原样返回）。命名方案见块首注释；本函数必须保持为模块
    globals 最后一个 callable（注入校验③钉住）。
    '''
    base_action = _R37_GUARD_PARENT(observation)
    return _r37_guard_core(observation, base_action)

