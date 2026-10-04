# -*- coding: utf-8 -*-
"""R23 运行时件（注入包内）。

责任契约：_route40_select（step144 续段选择）/_route40_wire_route（选路
接线：把选定路线写进基座模块级路由表）/apply_race_slots（同回合卖单竞速）/
apply_slot_hygiene（队列补洞）。本文件源文本由 inject_r40_block 追加进
包内（含内嵌续段库）。
"""
from __future__ import annotations

from typing import Any, Dict


def _route40_select(observation: Dict[str, Any], library: Any = None) -> Dict[str, Any]:
    """step144 续段选择：按当局开局长相族（前 144 步宏观指纹）查库选路线
    续段；无族命中→回退现行 _router 店对逻辑；只读选择不改磁带主体。

    签名意图：输入: observation+库 / 输出: {route, family, confidence} /
    错误: 库缺→回退默认路由。

    口径留档（与 route_library.build_route_library 两件共同约定）：
    - 族键="<hires>|<land_buys>|<tiles_by_crop>|<首二店>"：hires/land_buys=
      前 144 步（步标 0..143）farms[player].hands/unlocked_quadrants 计数正增量
      累计；tiles_by_crop=step144 当拍 crop 非空地块数（count 降序、作物名升序）
      渲染 "CROP:n,..."（空="NONE"）；首二店=step144 当拍 town.unlocked_shops[:2]
      以 "+" 连接（空="NONE"）。步标=observation["step"] 或 day*24+hour。
    - 触发：首拍 step>=144（正常即 step==144）按族键查库，命中且族有胜局
      best_route→{route: route_id, family: 族键, confidence: 族 win_rate}；
      结果跨步锁定（latched），step==0 或步标回退=新局复位。
    - 回退信号：route=None 表示回退现行 `_router` 店对逻辑（无族命中/族无胜局
      best_route/库缺/异常一律 {route: None, family: None 或族键, confidence: 0.0}；
      异常不锁定，后续好拍可重触发）。confidence=置信度（命中=族 win_rate）。
    - 本件只读选择不改表；选定路线的生效归 _route40_wire_route 接线件
      （表改写挂法见其 docstring，B32 再修订）。
    """
    import json

    def _jl(x):
        return json.loads(x) if isinstance(x, str) else x

    def _label(obs):
        raw = obs.get("step")
        if raw is not None:
            return int(raw)
        return int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))

    fallback = {"route": None, "family": None, "confidence": 0.0}
    try:
        step = _label(observation)
        st = getattr(_route40_select, "_fp_state", None)
        if st is None or step == 0 or step < st.get("last_step", -1):
            st = {"hires": 0, "land": 0, "hands_prev": None, "uq_prev": None,
                  "latched": None, "last_step": -1}
            _route40_select._fp_state = st
        st["last_step"] = step
        if st["latched"] is not None:
            return dict(st["latched"])
        farms = _jl(observation.get("farms"))
        if not isinstance(farms, list) or len(farms) != 2:
            raise ValueError("farms 形态非法")
        farm = farms[int(observation.get("player", 0))]
        hands = len(_jl(farm.get("hands")) or [])
        uq = len(_jl(farm.get("unlocked_quadrants")) or [])
        if step < 144:
            if st["hands_prev"] is not None:
                if hands > st["hands_prev"]:
                    st["hires"] += hands - st["hands_prev"]
                if uq > st["uq_prev"]:
                    st["land"] += uq - st["uq_prev"]
            st["hands_prev"], st["uq_prev"] = hands, uq
            return dict(fallback)
        crops = {}
        for row in (_jl(farm.get("tiles")) or []):
            if not isinstance(row, list):
                continue
            for cell in row:
                if isinstance(cell, dict) and cell.get("crop"):
                    c = str(cell["crop"])
                    crops[c] = crops.get(c, 0) + 1
        tiles_str = ",".join(
            "%s:%d" % (c, n) for c, n in
            sorted(crops.items(), key=lambda kv: (-kv[1], kv[0]))) or "NONE"
        shops = list(_jl((observation.get("town") or {}))
                     .get("unlocked_shops") or [])[:2]
        shops_str = "+".join(str(s) for s in shops) or "NONE"
        key = "%d|%d|%s|%s" % (st["hires"], st["land"], tiles_str, shops_str)
        lib = library
        if isinstance(lib, str):
            lib = json.loads(lib)
        if isinstance(lib, dict) and "families" not in lib and \
                isinstance(lib.get("library"), dict):
            lib = lib["library"]
        fam = (lib.get("families") or {}).get(key) if isinstance(lib, dict) else None
        if isinstance(fam, dict) and fam.get("best_route") is not None:
            out = {"route": fam["best_route"], "family": key,
                   "confidence": float(fam.get("win_rate", 0.0))}
        elif isinstance(fam, dict):
            out = {"route": None, "family": key, "confidence": 0.0}
        else:
            out = dict(fallback)
        st["latched"] = out
        return dict(out)
    except Exception:
        return dict(fallback)


def _route40_wire_route(observation: Dict[str, Any], selection: Any) -> Dict[str, Any]:
    """接线件（B32 再修订「接线路由库再验一轮」）：把 _route40_select 选定
    路线写进基座模块级路由表，使基座 _router 真正锁存到 best_route（消融
    查明①此前空转：返回值无人消费，_router 照旧走店对表）。

    挂法留档（实测可达=模块级表改写；注入块与基座同一模块 globals）：
    - 基座 _router 于 step>=144 首拍按 shops=tuple(unlocked_shops[:2]) 店对
      锁存 state['route']：无 YARN→_R108_SHOP_ROUTES（缺省 100）/含 YARN→
      _R110_OLD_SHOPS（缺省 0），_V92_TABLE 再覆盖；'YARN_STORE' 在店对且
      rkey∈_V93_ROUTE_BY_RIVAL 时特例最终覆盖。本件由 _route40_agent 包装层
      在选路步（父层取动作之前，step144 或首拍）被调：①当拍店对键写进三张
      店对表=best_route；②_V93_ROUTE_BY_RIVAL 值全部重写为 best_route（键
      不动）——特例路径亦恒输出选定路线（其优先级在 _V92 之后，不中和会
      反覆盖）。店对键推导镜像 _router 表达式（_get 同义），保证同键命中。
    - 只改「选哪条路线」这一个决策面：无族命中/族无胜局（selection.route
      None）或 confidence≤0 或 route 非 int→表零改动（回退现状）；异常→
      原样 fail-safe；不碰磁带主体/动作链。step>=648 的 day27 强制 route=2
      属基座既有后段行为，不在本件面（不改）。
    - 新局复位：step==0 或步标回退→按 _wire_state["orig"] 逐项恢复四表原值
      （每局全新模块命名空间本就隔离，仍留复位防同空间复用）；每局只接线
      一次（wired 标记防跨拍重复登记原值）。
    - 状态自包含 _route40_wire_route._wire_state（函数属性，注入友好，
      _fp_state 同款）={last_step, wired, route, shops,
      orig:[(表, 键, 原在, 原值)]}。
    - 依赖面：globals() 无表/表非 dict→逐项跳过；无路由表命名空间（单测/
      假父层）恒 wired=False 零副作用。

    签名意图：输入: observation+selection（_route40_select 返回形）/
    输出: {"wired", "route", "shops"} 观测记录 / 错误: 异常→
    {"wired": False, "route": None, "shops": []}。
    """
    try:
        if not isinstance(observation, dict):
            raise TypeError("observation 非 dict")
        raw = observation.get("step")
        if raw is not None:
            step = int(raw)
        else:
            step = int(observation.get("day", 0)) * 24 + \
                int(observation.get("hour", 0))
        st = getattr(_route40_wire_route, "_wire_state", None)
        if st is None or step == 0 or step < st.get("last_step", -1):
            if isinstance(st, dict):
                for tbl, key, had, val in st.get("orig", []):
                    try:
                        if had:
                            tbl[key] = val
                        else:
                            tbl.pop(key, None)
                    except Exception:
                        pass
            st = {"last_step": -1, "wired": False, "route": None,
                  "shops": [], "orig": []}
            _route40_wire_route._wire_state = st
        st["last_step"] = step
        sel = selection if isinstance(selection, dict) else {}
        route = sel.get("route")
        conf = sel.get("confidence", 0.0)
        if not (isinstance(route, int) and not isinstance(route, bool)
                and float(conf) > 0):
            return {"wired": False, "route": None, "shops": []}
        if st["wired"]:
            return {"wired": True, "route": st["route"],
                    "shops": list(st["shops"])}
        town = observation.get("town")
        get = getattr(town, "get", None)
        ups = get("unlocked_shops", []) if callable(get) else []
        shops = tuple((ups or [])[:2])
        g = globals()
        orig = st["orig"]
        touched = 0
        for name in ("_R108_SHOP_ROUTES", "_R110_OLD_SHOPS", "_V92_TABLE"):
            tbl = g.get(name)
            if not isinstance(tbl, dict):
                continue
            orig.append((tbl, shops, shops in tbl, tbl.get(shops)))
            tbl[shops] = route
            touched += 1
        tbl = g.get("_V93_ROUTE_BY_RIVAL")
        if isinstance(tbl, dict) and tbl:
            for key in list(tbl):
                orig.append((tbl, key, True, tbl[key]))
                tbl[key] = route
            touched += 1
        if not touched:
            # 无路由表命名空间（单测/假父层）：零副作用恒 wired=False。
            st["orig"] = []
            return {"wired": False, "route": None, "shops": []}
        st["wired"] = True
        st["route"] = route
        st["shops"] = list(shops)
        return {"wired": True, "route": route, "shops": list(shops)}
    except Exception:
        return {"wired": False, "route": None, "shops": []}


def apply_race_slots(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """同回合卖单竞速：我方 SELL 单前移至市场表前部槽（对手挂单前成交；
    沿空槽位次语义+V57 资金序不变量）；只动 SELL 槽序。

    签名意图：输入: observation, action / 输出: 调整后 action /
    错误: 异常→原动作。

    选型留档（B30b 保守法）：
    - 槽位语义：action["market"] 为位置性列表，空槽 [] 有意义；总槽数
      不变、不删不增单、不动物品/单量，只重排 SELL 槽序。
    - 前移规则：SELL 单按原序稳定前移，挤进本区段更靠前的空 [] 槽；
      区段=被非 SELL 单（HIRE/BUY*）锚定的最大连续槽区间。SELL↔非 SELL
      相对序逐位不变 = V57 资金序不变量天然成立（HIRE/BUY 不得挪到供资
      卖单前）；SELL 间换序方案弃用——换序可把供资卖单挤到其 BUY 之后，
      BUY 相对前移至供资卖单前即 V57 因果洞违例。
    - observation 保留签名位（竞速只需当拍槽位；对手挂单建模留后续）。
    - 异常/形态非法（action 非 dict、market 非列表、槽位非列表）→返回
      原动作对象。
    """
    try:
        if not isinstance(action, dict):
            raise TypeError("action 非 dict")
        market = action.get("market")
        if not isinstance(market, list):
            raise TypeError("market 非列表")
        for slot in market:
            if not isinstance(slot, list):
                raise TypeError("槽位非列表")
        new_market = []
        region: list = []

        def _flush_region():
            sells = [o for o in region if o and o[0] == "SELL"]
            empties = sum(1 for o in region if not o)
            new_market.extend(sells)
            new_market.extend([] for _ in range(empties))
            del region[:]

        for slot in market:
            if slot and slot[0] != "SELL":
                _flush_region()
                new_market.append(slot)
            else:
                region.append(slot)
        _flush_region()
        return {**action, "market": new_market}
    except Exception:
        return action


def apply_slot_hygiene(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """队列补洞：识别零执行占坑单（上一拍挂出未成交）→清坑+后位有效单前移
    补洞（空槽位次语义不破坏）；只动自家市场单。

    签名意图：输入: observation, action / 输出: 调整后 action+补洞账 /
    错误: 异常→原动作。

    口径留档（B30b 保守法）：
    - 返回 {"action": 调整后动作, "cleared": [{"slot","order"}…],
      "filled": [{"to","from","order"}…]}；异常→{"action": 原动作对象,
      "cleared": [], "filled": []}。
    - 跨步账本 apply_slot_hygiene._ledger（函数属性自包含，注入友好）：
      {last_step, orders{槽: tuple(单)}, money, inv}，记当拍调整前（注入链
      收到）的 market 意图快照+对账快照；step==0 或步标回退=新局复位
      （只重建账本，不清坑）；步标非严格 +1 连续→拿不准不清。
    - 零执行占坑单判定（五条全真才清，拿不准→不清）：①上一拍同槽挂出的
      单本拍仍原样在（逐元素相等）；②该拍成交对账无变化——farm money 与
      该单物品的 market.inventory 跨拍零变化且键俱在（精确相等）；③单形
      SELL/BUY*（BUY/BUY_PRODUCT/BUY_ANIMAL 带物品字段；HIRE/BUY_LAND
      原子单拿不准不清）；④步标连续；⑤qty==0 真占坑单（B32 消融机制修正：
      qty>0 站立单=排队限价单，上一拍未成交不=占坑——清之丢队列位次，实测
      单件 h2h 崩至 0.075；qty 非 int 0 一概不清）。
    - 清坑=置 [] 保位次（不删槽）；补洞=后位有效单链式前移填坑——每坑取
      其后最近的自家有效单（有效单=非空且未判为占坑）前移入坑，原槽置 []
      成新坑续填直至其后无有效单；空槽原地不动（只前移有效单），槽总数
      不变；移动保相对序→资金序（V57）不破坏；零执行单从未供资/耗资，
      清坑资金因果中性。只动 action["market"]（自家市场单）。
    """
    def _snap(obs):
        money = None
        inv = None
        try:
            farms = obs.get("farms")
            player = int(obs.get("player", 0))
            if isinstance(farms, list) and 0 <= player < len(farms):
                farm = farms[player]
                if isinstance(farm, dict):
                    money = farm.get("money")
            mkt = obs.get("market")
            if isinstance(mkt, dict):
                raw = mkt.get("inventory")
                if isinstance(raw, dict):
                    inv = dict(raw)
        except Exception:
            money, inv = None, None
        return money, inv

    try:
        if not isinstance(observation, dict):
            raise TypeError("observation 非 dict")
        if not isinstance(action, dict):
            raise TypeError("action 非 dict")
        market = action.get("market")
        if not isinstance(market, list):
            raise TypeError("market 非列表")
        for slot in market:
            if not isinstance(slot, list):
                raise TypeError("槽位非列表")
        raw = observation.get("step")
        if raw is not None:
            step = int(raw)
        else:
            step = int(observation.get("day", 0)) * 24 + \
                int(observation.get("hour", 0))
        money, inv = _snap(observation)
        st = getattr(apply_slot_hygiene, "_ledger", None)
        if st is None or step == 0 or step < st.get("last_step", -1):
            st = {"last_step": -1, "orders": {}, "money": None, "inv": None}
            apply_slot_hygiene._ledger = st
        contiguous = (step == st.get("last_step", -1) + 1)
        cur_orders = {k: tuple(o) for k, o in enumerate(market) if o}
        cleared = []
        holes = []
        if contiguous:
            for k in sorted(cur_orders):
                order = market[k]
                if st["orders"].get(k) != cur_orders[k]:
                    continue
                op = order[0]
                if not (isinstance(op, str) and
                        (op == "SELL" or op in ("BUY", "BUY_PRODUCT",
                                                "BUY_ANIMAL"))):
                    continue
                if len(order) < 2 or not isinstance(order[1], str):
                    continue
                # ⑤qty==0 真占坑单才清（B32 机制修正，见 docstring）。
                if len(order) != 3 or not isinstance(order[2], int) \
                        or isinstance(order[2], bool) or order[2] != 0:
                    continue
                item = order[1]
                prev_inv = st.get("inv")
                if not (isinstance(prev_inv, dict) and isinstance(inv, dict)
                        and item in prev_inv and item in inv):
                    continue
                if st.get("money") is None or money is None:
                    continue
                if st["money"] != money or prev_inv[item] != inv[item]:
                    continue
                cleared.append({"slot": k, "order": list(order)})
                holes.append(k)
        filled = []
        if holes:
            new_market = list(market)
            moved_from = set()
            frontier = list(holes)
            pos = 0
            while pos < len(frontier):
                h = frontier[pos]
                pos += 1
                src = None
                for j in range(h + 1, len(market)):
                    if j in holes or j in moved_from or not market[j]:
                        continue
                    src = j
                    break
                if src is None:
                    continue
                moved_from.add(src)
                filled.append({"to": h, "from": src,
                               "order": list(market[src])})
                new_market[h] = market[src]
                new_market[src] = []
                frontier.append(src)
            for h in holes:
                if not any(f["to"] == h for f in filled):
                    new_market[h] = []
            st["last_step"] = step
            st["orders"] = cur_orders
            st["money"] = money
            st["inv"] = inv
            return {"action": {**action, "market": new_market},
                    "cleared": cleared, "filled": filled}
        st["last_step"] = step
        st["orders"] = cur_orders
        st["money"] = money
        st["inv"] = inv
        return {"action": action, "cleared": [], "filled": []}
    except Exception:
        return {"action": action, "cleared": [], "filled": []}
