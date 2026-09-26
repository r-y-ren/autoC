# -*- coding: utf-8 -*-
"""cash_guard_block（R19 运行时三件套，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
_r37_agent（尾块捕获入口，fail-safe）→ _r37_cash_guard（现金下限判定）→
_r37_defer_low_priority（触线顺延低优先级购买）。动作集合不变量：只顺延/
删减购买类单，不新增意图、不动 farmer/hands 单元指令（动物格 HARVEST/
FEED/CARE/移动/DROP/PLACE）与市场卖单（SELL）。本文件源文本由
inject_cash_guard_block 按函数 ast 抽取追加进包内——三函数须自包含
（价目等常量定义在函数体内），stdlib only。

跨批修订口径（2026-09-26 用户裁决；现金守卫三处过度扣单根因修复）：
①逐单价丢单保护：BUY_ANIMAL 顺延线=该单实际成本（qty×引擎单价），只拦
  引擎真会静默丢的（执行点现金 at[i] < 该单成本；引擎 _commit_unit 逐单位
  money<price 即中止该单、余量静默丢弃）。floors 形态={"d0_end": 12,
  "buy_animal": "exact_cost", "hard_min": 4, "prices": <可选核价表>}：
  buy_animal 恒为字符串 "exact_cost"（逐单价模式），prices=item→单价
  覆盖表（缺省=引擎价目转录 CROPS["seed"]/ANIMALS["cost"]）；d0 日终窗
  ≥12 与硬底线 4（夹持制）不变。
②执行点现金投影计入同列表卖单收入：at[i] 与动作后现金 end 计入同 market
  列表中位序在前（j<i）SELL 单预期收入（引擎 per-unit lockstep 结算：
  同列表先序单位先成交，slot j 整单先于 slot i 结算）；卖价估计=
  observation 市场价（market.prices[item]），读不到/非有限/非正→该单
  回退不计=保守；SELL qty 按面值（底版 clamp_sells 已按棚仓投影修剪卖单）。
③顺延账重发范围扩到 BUY_SEED：账中 BUY_ANIMAL/BUY_SEED 意图按顺延序
  （FIFO）重发进首个「可负担」空 [] 槽（执行点现金 ≥该单实际成本），
  种子缓买不再永久丢弃；无可负担空槽→留账随后续步重试，不阻塞后续意图。
"""
from __future__ import annotations

from typing import Any, Dict, Optional


def _r37_agent(observation: Dict[str, Any], base_action: Dict[str, Any]) -> Dict[str, Any]:
    """尾块捕获入口：取基座动作→交 _r37_cash_guard 调整→返回同构 action。

    动作集合不变量：只顺延/删减购买类单，不新增意图、不动 HARVEST/FEED/
    CARE/移动/DROP/PLACE 单元与卖单；任何异常→基座动作原样返回（fail-safe）；
    step==0 复位层内缓存（顺延账）。

    签名意图：输入: observation, base_action / 输出: 调整后 action /
    错误: 异常→入口兜底回退基座动作。

    结构定义（本层定形，_r37_cash_guard 对齐；R19 核心增量=顺延账跨步重试，
    顺延不是删除、是择机重发）：
    - floors 常数 = {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4}
      （跨批修订①：buy_animal 逐单价模式取代旧版平线 500；三键常数钉住）。
    - 顺延账缓存 = 本函数属性 _r37_agent._defer_ledger（list；条目同
      _r37_defer_low_priority 顺延账 {"op","item","qty","cost","slot"}，条目
      序=顺延序）。函数属性自包含、随源码注入不丢、不与注入底版 globals 撞名。
      step==0 复位（清空携带意图）；复位/出账/入账统一在流程成功后原子提交，
      任何异常→账保持调用前状态（账读写自身 try 包裹，可静默、不许抛）。
    - 执行点现金口径（跨批修订②，_r37_cash_guard/_project 同口径）：逐槽
      at[i]=当前资金−前序 HIRE fib 硬开销−前序保留购买单全价＋前序 SELL
      单预期收入（同列表位序在前、引擎 per-unit lockstep 先序单位先成交）；
      卖价=observation 市场价 market.prices[item]（读不到/非有限/非正→
      该单不计=保守）。
    - 每步流程：(a) step==0 复位账（先于重试，携带意图不再回填）；(b) 重试
      阶段（跨批修订③：范围=账中 BUY_ANIMAL 与 BUY_SEED）——按顺延序（FIFO）
      逐条重发进空 [] 槽：落首个「可负担」空槽（该槽执行点现金 ≥该单实际
      成本 qty×单价；修订②后 at 随槽序非单调，逐槽扫描不提前 break）；
      无空槽或无可负担空槽→该条留账、继续处理后续账条（低价意图
      不被高价意图饿死），意图不灭；不改槽位数、不挤掉任何既有单；(c) 守卫
      阶段——把（含回填的）action 交 _r37_cash_guard（floors 同上常数）；
      (d) 合并顺延账——回填成功的出账、守卫新顺延入账（交守卫动作 vs
      adjusted_action 逐槽 diff，被置 [] 的核价购买单按
      {"op","item","qty","cost","slot"} 重建，defer 同口径）；(e) 返回
      adjusted_action。
    - 回填判据与守卫逐单价丢单判据同口径同线（at[i] ≥该单成本 ⟺ 守卫不触
      buy_animal 丢单线）→ 回填单不会被逐单价保护误伤；若 d0_end 等更严
      下限仍要求顺延，回填单随 diff 回流入账、意图不灭。「不新增意图」=
      只重发账内既有购买意图、只落空 [] 槽；farmer/hands 与 HIRE/卖单
      一字节不动、槽位数恒定。
    - fail-safe：任何异常→返回 base_action 原对象（连同不动的账）。
    """
    try:
        # ---- 0. 顺延账读取（函数属性缓存；账操作静默） ----
        try:
            cache = _r37_agent._defer_ledger
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

        # ---- 3. 核价/执行点现金（口径同 _r37_cash_guard；修订①②） ----
        floors = {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4}
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

        def _sell_price(item):
            # 卖价估计=observation 市场价（修订②）；读不到/非有限/非正→0=保守。
            try:
                v = observation["market"]["prices"][item]
            except Exception:
                return 0.0
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return 0.0
            f = float(v)
            if f != f or f == float("inf") or f == float("-inf") or f <= 0.0:
                return 0.0
            return f

        def _sell_income(raw):
            try:
                if len(raw) < 3 or not isinstance(raw[1], str):
                    return 0.0
                qty = _strict_qty(raw[2])
                if qty is None:
                    return 0.0
                return qty * _sell_price(raw[1])
            except Exception:
                return 0.0

        def _hire_cost(n):
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        def _at_slots(mkt):
            # 逐槽执行点现金 at[]（修订②）：扣 HIRE fib 硬开销与保留购买单
            # 全价，加位序在前 SELL 单预期收入（引擎 per-unit lockstep：
            # 同列表先序单位先成交，slot j 整单先于 slot i 结算）。
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
                    elif op == "SELL":
                        cash += _sell_income(raw)
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

        # ---- 4. 重试阶段：账中 BUY_ANIMAL/BUY_SEED 择机重发（修订③） ----
        passed = base_action
        refilled_ids = set()
        if working:
            new_market = list(market)   # 回填只出新表，输入动作不被原地改动
            for entry in working:
                if not isinstance(entry, dict):
                    continue            # 账目形态不符→留账不动
                op = entry.get("op")
                if op not in ("BUY_ANIMAL", "BUY_SEED"):
                    continue            # 重发范围=购买类两族（修订③）；其余留账
                item = entry.get("item")
                qty = _strict_qty(entry.get("qty"))
                if qty is None:
                    continue            # 账目数量不可核价→留账不动
                cost = _price_of(op, item, qty)
                if cost is None:
                    continue            # 账目不可核价→留账不动
                at = _at_slots(new_market)
                free = None
                for i in range(len(new_market)):
                    if _is_empty(new_market[i]) and at[i] >= cost:
                        free = i        # 首个可负担空槽（at 非单调，不 break 早停）
                        break
                if free is None:
                    continue            # 无可负担空槽→留账（不阻塞后续账条）
                new_market[free] = [op, item, qty]
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
            _r37_agent._defer_ledger = merged
        except Exception:
            pass                        # 账操作失败可静默，不许抛

        # ---- 7. 出口：返回守卫 adjusted_action（同构 action） ----
        return guarded
    except Exception:
        return base_action


def _r37_cash_guard(observation: Dict[str, Any], base_action: Dict[str, Any],
                    floors: Dict[str, Any]) -> Dict[str, Any]:
    """现金下限判定：识别当前步适用下限（①d0 日终窗 step23 前最后动作 ≥12；
    ②BUY_ANIMAL 逐单价丢单线=该单实际成本[修订①，引擎真会静默丢的
    at[i]<qty×单价 才触]）；触线→交 _r37_defer_low_priority，不触线原样
    放行；下限为可配置常数（判决标定，硬底线 4 不可破）。

    签名意图：输入: observation, base_action, floors /
    输出: {hit_floor, adjusted_action} / 错误: 状态读取失败→不干预原样返回。

    结构定义（本层定形，向下游 _r37_defer_low_priority 对齐）：
    - floors = {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4,
      "prices": <可选核价表>}（前三键皆必填）：
      d0_end=日终窗下限、buy_animal=BUY_ANIMAL 顺延线模式（恒为字符串
      "exact_cost"=逐单价模式[修订①]：顺延线=该单实际成本 qty×单价，只拦
      引擎真会静默丢的；其余形态含旧版平线数值一律视为配置错误→fail-safe
      不干预）、hard_min=硬底线。prices=可选 item→单价 覆盖表（缺省=引擎
      价目转录 CROPS["seed"]/ANIMALS["cost"]；仅接受 str 键+有限正数），
      覆盖表只对已知核价条目生效。硬底线 4（=d1 三张 HIRE 价 1+1+2）不可
      破，处置策略=夹持制：数值型（含负数）但 <4 一律夹到 4——effective
      hard_min=max(4, hard_min)，d0_end 再与之取 max；逐单价丢单线=该单
      实际成本（引擎丢单线恰=qty×单价，不叠加夹持——付得起的单不拦）；
      类型非法（bool/str/None/list…）或非有限（NaN/±inf）→ 配置错误→
      fail-safe 不干预。
    - d0 日终窗 = step 20..23（含）：step 读法沿主干 int(observation["step"])，
      turnsPerDay=24、d0=step//24==0（step 0..23），日终窗=d0 最后 4 拍
      （hour 20..23）；窗外不适用 d0_end。
    - 适用下限：①step 在 d0 日终窗 → d0_end；②base_action 含 BUY_ANIMAL
      单且执行点现金 at[i] < 该单实际成本 qty×单价（逐单价丢单线=引擎
      丢单线，item∈GOOSE/COW/SHEEP 且 qty 合法，与下游核价口径一致）→
      buy_animal。
      同命中取 d0_end（其处置=动作后现金下限+逐单丢单保护，覆盖
      buy_animal 处置；修订前「取 floor 大者」是平线 500 连坐动作后现金
      的过度扣单根因之一，废止）。
    - 现金核算口径与下游一致（修订②）：执行点现金 at[i] 与动作后现金 end
      = 当前资金 − HIRE fib 硬开销 − 保留购买单全价 ＋ 位序在前 SELL 单
      预期收入（同 market 列表、引擎 per-unit lockstep 先序单位先成交；
      卖价=observation 市场价 market.prices[item]，读不到→该单不计=保守）。
      触线：d0_end=动作后现金 end < floor；buy_animal=任一 BUY_ANIMAL 单
      at[i] < 该单逐单价线（单提交前口径）。触线→调下游并折返
      {"hit_floor": <命中的 {"floor","kind"}>, "adjusted_action": 顺延后
      action}；未触线零足迹 {"hit_floor": None, "adjusted_action":
      base_action 原对象}（下游不被调用）。
      hit_floor["floor"]：d0_end=floor_d0（end 下限）；buy_animal=被拦单
      逐单价线最大值（触发线留痕，处置判据在下游逐单核价）。
    - 异常（obs 缺字段/类型不对、floors 畸形、action 非 dict…）→ 不干预：
      {"hit_floor": None, "adjusted_action": base_action 原对象}。
    """
    try:
        # ---- 0. floors 配置校验+硬底线夹持（非法→抛，由尾兜底 fail-safe） ----
        if not isinstance(floors, dict):
            raise TypeError("floors must be a dict")
        cfg = {}
        for key in ("d0_end", "hard_min"):
            value = floors[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError("floors[%s] must be a number" % key)
            value = float(value)
            if value != value or value == float("inf") or value == float("-inf"):
                raise ValueError("floors[%s] must be finite" % key)
            cfg[key] = value
        # buy_animal 修订①：仅认 "exact_cost" 逐单价模式（旧版平线数值废止）。
        if floors["buy_animal"] != "exact_cost":
            raise ValueError("floors[buy_animal] must be 'exact_cost'")
        seed_price = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                      "STRAWBERRY": 100, "MELON": 80}
        animal_cost = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
        prices = dict(seed_price)
        prices.update(animal_cost)
        override = floors.get("prices")
        if override is not None:
            if not isinstance(override, dict):
                raise TypeError("floors[prices] must be a dict")
            for key, value in override.items():
                if not isinstance(key, str):
                    raise TypeError("floors[prices] keys must be str")
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise TypeError("floors[prices][%s] must be a number" % key)
                value = float(value)
                if value != value or value == float("inf") \
                        or value == float("-inf") or value <= 0.0:
                    raise ValueError("floors[prices][%s] must be finite > 0" % key)
                if key in prices:
                    prices[key] = value    # 覆盖表只对已知核价条目生效
        hard = max(cfg["hard_min"], 4.0)   # 硬底线 4 不可破
        floor_d0 = max(cfg["d0_end"], hard)

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

        def _strict_qty(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if isinstance(value, float):
                if not value.is_integer():
                    return None
                value = int(value)
            return value if value >= 1 else None

        def _sell_price(item):
            # 卖价估计=observation 市场价（修订②）；读不到/非有限/非正→0=保守。
            try:
                v = observation["market"]["prices"][item]
            except Exception:
                return 0.0
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return 0.0
            f = float(v)
            if f != f or f == float("inf") or f == float("-inf") or f <= 0.0:
                return 0.0
            return f

        def _sell_income(raw):
            try:
                if len(raw) < 3 or not isinstance(raw[1], str):
                    return 0.0
                qty = _strict_qty(raw[2])
                if qty is None:
                    return 0.0
                return qty * _sell_price(raw[1])
            except Exception:
                return 0.0

        parsed = []
        for raw in market:
            entry = None
            if isinstance(raw, (list, tuple)) and raw:
                op = raw[0]
                if op == "HIRE":
                    entry = {"op": "HIRE", "cost": None}
                elif op == "SELL":
                    entry = {"op": "SELL", "cost": None,
                             "income": _sell_income(raw)}
                elif len(raw) >= 3 and isinstance(raw[1], str):
                    qty = _strict_qty(raw[2])
                    if qty is not None and op == "BUY_SEED" and raw[1] in seed_price:
                        entry = {"op": "BUY_SEED", "cost": qty * prices[raw[1]]}
                    elif qty is not None and op == "BUY_ANIMAL" and raw[1] in animal_cost:
                        entry = {"op": "BUY_ANIMAL", "cost": qty * prices[raw[1]]}
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
            elif entry["op"] == "SELL":
                cash += entry["income"]    # 修订②：位序在前卖单收入计入
            else:
                cash -= entry["cost"]
        end = cash

        # ---- 3. 适用下限识别+触线判定（双命中取 d0_end，修订①口径） ----
        d0_hit = None
        if 20 <= step <= 23 and end < floor_d0:
            d0_hit = {"floor": floor_d0, "kind": "d0_end"}
        drop_lines = []
        for i, entry in enumerate(parsed):
            if entry is not None and entry["op"] == "BUY_ANIMAL":
                # 逐单价丢单线（修订①）=该单实际成本（引擎丢单线恰=qty×单价）。
                if at[i] < entry["cost"]:
                    drop_lines.append(entry["cost"])
        if d0_hit is None and not drop_lines:
            return {"hit_floor": None, "adjusted_action": base_action}
        # 同命中取 d0_end：其处置覆盖逐单丢单保护（详见 docstring）。
        hit_floor = d0_hit if d0_hit is not None else \
            {"floor": max(drop_lines), "kind": "buy_animal"}

        # ---- 4. 委派处置并折返（只判定+委派，本层不改单） ----
        out = _r37_defer_low_priority(observation, base_action, hit_floor,
                                      prices)
        return {"hit_floor": hit_floor, "adjusted_action": out["action"]}
    except Exception:
        return {"hit_floor": None, "adjusted_action": base_action}


def _r37_defer_low_priority(observation: Dict[str, Any], action: Dict[str, Any],
                            hit_floor: Any,
                            prices: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """触线处置：按低优先级顺延——先缓 BUY_SEED（MELON 80 金/粒优先，按订单
    尾序删缓），BUY_ANIMAL 逐单价丢单保护（修订①：该单执行点现金 < 该单实际
    成本 qty×单价 才整单顺延入账，保留意图不永久删除；旧版「不足 500 一律
    整单顺延」废止）；HIRE（4 金硬开销）与 FEED/CARE/卖单/动物格 HARVEST/
    DROP/PLACE 序一律不动；kind=d0_end 时处置后动作后现金须达触发下限，
    一次不够→继续顺延直至达标。

    签名意图：输入: observation, action, hit_floor[, prices] /
    输出: 顺延后 action+顺延账更新 / 错误: 异常→原动作。

    结构定义（本层定形，_r37_cash_guard 对齐）：
    - hit_floor = {"floor": <非负有限数>, "kind": "d0_end" | "buy_animal"}：
      kind=d0_end：floor=动作后现金 end 下限（observation 当前资金 −保留
      支出＋卖单收入 ≥ floor；保留支出=HIRE fib 递增硬开销+保留 BUY_SEED/
      BUY_ANIMAL 全价）；kind=buy_animal：floor=触发线留痕（被拦单逐单价线
      最大值，来自 _r37_cash_guard），处置判据为逐单核价、不施加 end 下限
      （动作后现金无引擎约束；平线连坐 end 是过度扣单根因之一，废止）。
    - prices = 可选 item→单价 覆盖表（None=引擎价目转录缺省；形态校验同
      _r37_cash_guard，非法→异常→不干预）。核价与逐单价线用同一表。
    - 返回 {"action": <顺延后 action>, "deferred": <顺延账>}；顺延账条目 =
      {"op": "BUY_SEED"|"BUY_ANIMAL", "item": <作物|牲畜>, "qty": <int 整单量>,
      "cost": <该单现金支出>, "slot": <原 market 槽位>}（条目序=顺延序）。
    - 顺延=被缓槽置 [] 空槽（保槽位数与位置语义，禁删槽）；无顺延（含尽力后
      仍不足）→ action 原对象返回（零足迹）。
    - 异常（action/hit_floor/prices/状态畸形、字段缺失）→ {"action": 原action,
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
        if kind not in ("d0_end", "buy_animal"):
            raise TypeError("hit_floor[kind] must be 'd0_end' or 'buy_animal'")

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
        # GOOSE300/COW400/SHEEP500；prices 覆盖表（修订①）只对已知条目生效。
        # HIRE=当日第 n 次 fib(n)（1,1,2,3,5…，三张=1+1+2=4 金硬开销）。数量
        # 纪律沿 layer_s _strict_count：int（非 bool）原样、整值 float 折 int，
        # bool/str/None/半值 float/非正 → 不核价不顺延（引擎 _parse_order 同
        # 口径丢弃）。SELL 单只计预期收入（修订②），永不顺延；BUY_PRODUCT/
        # BUY_LAND/空槽/未知 op 一律不核价不顺延（一个字节不动）。
        seed_price = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                      "STRAWBERRY": 100, "MELON": 80}
        animal_cost = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
        effective = dict(seed_price)
        effective.update(animal_cost)
        if prices is not None:
            if not isinstance(prices, dict):
                raise TypeError("prices must be a dict")
            for key, value in prices.items():
                if not isinstance(key, str):
                    raise TypeError("prices keys must be str")
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise TypeError("prices[%s] must be a number" % key)
                value = float(value)
                if value != value or value == float("inf") \
                        or value == float("-inf") or value <= 0.0:
                    raise ValueError("prices[%s] must be finite > 0" % key)
                if key in effective:
                    effective[key] = value
        # 硬底线 4 的夹持在 _r37_cash_guard 配置层（floor_d0）；本层逐单价
        # 丢单线=该单实际成本本身（引擎丢单线恰=qty×单价）。

        def _strict_qty(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return None
            if isinstance(value, float):
                if not value.is_integer():
                    return None
                value = int(value)
            return value if value >= 1 else None

        def _sell_price(item):
            # 卖价估计=observation 市场价（修订②）；读不到/非有限/非正→0=保守。
            try:
                v = observation["market"]["prices"][item]
            except Exception:
                return 0.0
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return 0.0
            f = float(v)
            if f != f or f == float("inf") or f == float("-inf") or f <= 0.0:
                return 0.0
            return f

        def _sell_income(raw):
            try:
                if len(raw) < 3 or not isinstance(raw[1], str):
                    return 0.0
                qty = _strict_qty(raw[2])
                if qty is None:
                    return 0.0
                return qty * _sell_price(raw[1])
            except Exception:
                return 0.0

        parsed = []
        for raw in market:
            entry = None
            if isinstance(raw, (list, tuple)) and raw:
                op = raw[0]
                if op == "HIRE":
                    entry = {"op": "HIRE", "item": None, "qty": 1, "cost": None}
                elif op == "SELL":
                    entry = {"op": "SELL", "item": raw[1] if len(raw) >= 2 else None,
                             "qty": None, "cost": None, "income": _sell_income(raw)}
                elif len(raw) >= 3 and isinstance(raw[1], str):
                    qty = _strict_qty(raw[2])
                    if qty is not None and op == "BUY_SEED" and raw[1] in seed_price:
                        entry = {"op": "BUY_SEED", "item": raw[1], "qty": qty,
                                 "cost": qty * effective[raw[1]]}
                    elif qty is not None and op == "BUY_ANIMAL" and raw[1] in animal_cost:
                        entry = {"op": "BUY_ANIMAL", "item": raw[1], "qty": qty,
                                 "cost": qty * effective[raw[1]]}
            parsed.append(entry)

        def _hire_cost(n):
            # 引擎 _fib/_hire_cost 同式：第 n 次（今日已雇 n 人）= fib(n)。
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        def _project(mask):
            # 逐槽执行点现金 at[]（引擎按槽位序结算；修订②：计入位序在前
            # SELL 单预期收入）与本动作后现金 end（只扣保留部分支出：HIRE
            # 必保 + 保留购买单照常花，卖单收入照常计）。
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
                elif entry["op"] == "SELL":
                    cash += entry["income"]
                else:
                    cash -= entry["cost"]
            return at, cash

        # ---- 2. 顺延循环：kind=d0_end 先按 end 下限缓（MELON 尾序→其余种子
        # 尾序→BUY_ANIMAL 整单）；随后 BUY_ANIMAL 逐单价丢单保护（修订①：
        # at[i] < 该单实际成本 才整单入账——引擎 _commit_unit 逐单位
        # money<price 即中止该单、余量静默丢弃，付得起的单不拦）。
        mask = [False] * len(parsed)
        deferred = []

        def _defer(slot):
            mask[slot] = True
            entry = parsed[slot]
            deferred.append({"op": entry["op"], "item": entry["item"],
                             "qty": entry["qty"], "cost": entry["cost"],
                             "slot": slot})

        while True:
            at, end = _project(mask)
            pick = None
            if kind == "d0_end" and end < floor:
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
                            and at[i] < entry["cost"]):
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
