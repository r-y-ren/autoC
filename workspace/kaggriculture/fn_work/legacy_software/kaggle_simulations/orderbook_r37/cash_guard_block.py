# -*- coding: utf-8 -*-
"""cash_guard_block（R19 运行时三件套，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
_r37_agent（尾块捕获入口，fail-safe）→ _r37_cash_guard（现金下限判定：
d0 日终窗 ≥12 金[硬底线 4=d1 三张 HIRE 价 1+1+2]、BUY_ANIMAL 提交前 ≥500
金[引擎丢单线 400/400/500]）→ _r37_defer_low_priority（触线顺延低优先级
购买）。动作集合不变量：只顺延/删减购买类单，不新增动作、不动物格
HARVEST 与卖单。本文件源文本由 inject_cash_guard_block 追加进包内。
"""
from __future__ import annotations

from typing import Any, Dict


def _r37_agent(observation: Dict[str, Any], base_action: Dict[str, Any]) -> Dict[str, Any]:
    """尾块捕获入口：取基座动作→交 _r37_cash_guard 调整→返回同构 action。

    动作集合不变量：只顺延/删减购买类单，不新增动作、不动 HARVEST 与卖单；
    任何异常→基座动作原样返回（fail-safe）；step==0 复位层内缓存（顺延账）。

    签名意图：输入: observation, base_action / 输出: 调整后 action /
    错误: 异常→入口兜底回退基座动作。
    """
    raise NotImplementedError("unimplemented:fn:_r37_agent")


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
