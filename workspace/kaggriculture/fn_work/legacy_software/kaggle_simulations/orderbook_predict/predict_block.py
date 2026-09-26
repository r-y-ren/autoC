# -*- coding: utf-8 -*-
"""predict_block（R21 运行时链，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
_predict_agent（单参官方入口，父层=_r37_agent 链）→ infer_rival_sells（净卖
反推：公开库存差分−自家成交−确定性城镇消费，$1 地板为下界）→ match_sellflow
（卖流库检索：首二店+step-2 身份指纹）→ extrapolate_sells（差分外推 1-2 步
写入 opponent_plan 容器）→ apply_dodge（预测倾销→我方卖单错峰/减量）。
置信不足→不动作 fail-safe；只动卖单时点/量。本文件源文本由
inject_predict_block 追加进包内（含内嵌库数据）。

实现口径（自包含：常数/小工具定义在各函数体内，stdlib only，注入底版
globals 零撞名；外部接线名 _PREDICT_PARENT/_PREDICT_LIBRARY 经 globals()
查找——注入层捕获行/内嵌库数据提供，测试可直接注入假父层与假库）。
"""
from typing import Any, Dict  # noqa: F401


def infer_rival_sells(observation: Dict[str, Any], own_fills: Any) -> Dict[str, Any]:
    """净卖反推（R21 L4）：market.inventory 差分−自家成交−确定性城镇消费
    →对手上一步净卖量/品类；$1 地板成交不入库存→下界标志；跨步账本供外推。

    引擎口径（kaggriculture.py）：步 S 的更新=双方成交（_process_market）后
    立即 _town_consume(S)——故观测差分 obs[S]→obs[S+1] 覆盖「步 S 的成交 +
    步 S 触发的城镇消费」；逆推式
      对手净卖 = 库存差分 + 城镇消费 − 自家净卖（sell−buy）。
    城镇消费（确定性，interval 取 4/24）：S % 4 == 0 时每 shop 实例对旗下
    各品扣 multiplier（单品类店 2、多品类店 1）；S % 24 == 0 时中心单全品
    （FERTILIZER 除外）各扣 1。自家 SELL 价>1 才入库存（引擎 _commit_unit：
    $1 成交不入库存）→ 不计入自家净卖，改记 floor_sells 佐证下界。
    下界标志：该品现/前步市场价 ≤ 1（地板）或自家账带 floor_sells
    （地板成交对公开库存不可见→净卖只少不多）。

    跨步账本 = 函数属性 infer_rival_sells._ledger（自包含）：
      {"step", "prev": {"step","inv","prices","shops"},
       "items": {item: {net_qty, lower_bound}}, "history": {item: [net_qty,...]}}
    仅当 prev.step == step−1（相邻步）才出账；步序跳跃/首步/step 0 只重建
    快照不出账。供 extrapolate_sells 差分外推。

    签名意图：输入: observation（逐步调用）+自有成交账
    {"sell":{item:qty},"buy":{item:qty}[,"floor_sells":{item:qty}]}（可 None）/
    输出: {item: {net_qty, lower_bound}}（净卖≠0 或下界品才入账）/
    错误: 字段缺失/畸形→空账 {} 不抛、账本不动。
    """
    try:
        if not isinstance(observation, dict):
            return {}
        market = observation["market"]
        inv_now = market["inventory"]
        if not isinstance(inv_now, dict):
            return {}
        prices_now = market.get("prices") or {}
        if not isinstance(prices_now, dict):
            prices_now = {}
        town = observation.get("town") or {}
        shops_now = list((town.get("unlocked_shops") or []) if isinstance(town, dict) else [])
        raw_step = observation.get("step")
        if raw_step is None:
            step = int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
        else:
            if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
                return {}
            step = int(raw_step)
    except Exception:
        return {}

    def _fills(key):
        try:
            sub = own_fills.get(key) or {}
            out = {}
            if isinstance(sub, dict):
                for k, v in sub.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        out[k] = abs(int(v))
            return out
        except Exception:
            return {}

    f_sell, f_buy, f_floor = _fills("sell"), _fills("buy"), _fills("floor_sells")

    try:
        ledger = infer_rival_sells._ledger
    except Exception:
        ledger = None
    if not isinstance(ledger, dict):
        ledger = {}
    prev = ledger.get("prev")
    prev = prev if isinstance(prev, dict) else None
    history = ledger.get("history")
    history = history if isinstance(history, dict) else {}

    result: Dict[str, Any] = {}
    if prev is not None and prev.get("step") == step - 1:
        inv_prev = prev.get("inv") or {}
        prices_prev = prev.get("prices") or {}
        shops_prev = prev.get("shops") or []
        # ---- 确定性城镇消费（步 step−1 触发；引擎 _town_consume 口径） ----
        consume: Dict[str, int] = {}
        s = step - 1
        shop_interval, center_interval = 4, 24
        if s % shop_interval == 0:
            for shop in shops_prev:
                products = {
                    "BAKERY": ("EGG", "WHEAT"),
                    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
                    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
                    "YARN_STORE": ("WOOL",),
                    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
                    "PET_CAFE": ("CARROT",),
                    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
                    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
                }.get(shop)
                if not products:
                    continue
                mult = 2 if len(products) == 1 else 1
                for item in products:
                    consume[item] = consume.get(item, 0) + mult
        if s % center_interval == 0:
            for item in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                         "EGG", "MILK", "WOOL"):
                consume[item] = consume.get(item, 0) + 1
        # ---- 逐品逆推 ----
        for item in set(list(inv_now.keys()) + list(inv_prev.keys())):
            try:
                diff = int(inv_now.get(item, 0)) - int(inv_prev.get(item, 0))
            except Exception:
                continue
            own_net = f_sell.get(item, 0) - f_buy.get(item, 0)
            net = diff + consume.get(item, 0) - own_net
            floor = f_floor.get(item, 0) > 0
            for p in (prices_now.get(item), prices_prev.get(item)):
                if isinstance(p, (int, float)) and not isinstance(p, bool) and p <= 1:
                    floor = True
            if net == 0 and not floor:
                continue
            result[item] = {"net_qty": int(net), "lower_bound": bool(floor)}
            hist = history.setdefault(item, [])
            if isinstance(hist, list):
                hist.append(int(net))
                if len(hist) > 64:
                    del hist[:-64]

    new_ledger = {"step": step,
                  "prev": {"step": step, "inv": dict(inv_now),
                           "prices": dict(prices_now), "shops": list(shops_now)},
                  "items": dict(result), "history": history}
    try:
        infer_rival_sells._ledger = new_ledger
    except Exception:
        pass
    return result


def match_sellflow(observation: Dict[str, Any], library: Any) -> Dict[str, Any]:
    """卖流库检索（R21 L4）：键=（unlocked_shops[:2] 组合，step-2 身份指纹），
    取当前步窗 ±w 的对手 SELL 分布；无键→回退全局分布；置信=样本数×集中度。

    库结构（与 build_sellflow_library 共同约定）：
      {"version", "keys": {f"{shop_pair}||{fingerprint}":
          {"n_episodes", "hist": {"<win>": {"<ITEM>":
              {"qty_sum","count","qty_max"}}}}},
       "global": {同 hist 形}}，win = step//48。
    键编码（本件钉住，兼容候选同查）：shop_pair=",".join(unlocked_shops[:2])；
    fingerprint=f"{round(float(money),3)}:{int(WHEAT inv)}"（step==2 的对手
    快照：farms[1−player].money + market.inventory.WHEAT；跨步身份存函数属性
    match_sellflow._identity，无快照回退当前观测值）。
    取窗：win=step//48，聚合 win−1..win+1（w=1）内各品直方。

    置信口径（简单可测）：
      样本因子 = min(1, n/10)，n=窗内 count 之和；
      集中度 = 最大单品 qty_sum / 全部 qty_sum（空分布=0）；
      confidence = 样本因子 × 集中度 ∈ [0,1]。

    签名意图：输入: observation+库 /
    输出: {"matches": {"items","wins","source","key","step"}, "confidence"} /
    错误: 库缺失/畸形→confidence=0（不抛）。
    """
    empty = {"items": {}, "wins": [], "source": "none", "key": None, "step": -1}
    try:
        if not isinstance(observation, dict):
            return {"matches": empty, "confidence": 0.0}
        raw_step = observation.get("step")
        if raw_step is None:
            step = int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
        else:
            step = int(raw_step)
        if not isinstance(library, dict) or not library:
            return {"matches": dict(empty, step=step), "confidence": 0.0}
        town = observation.get("town") or {}
        shops = list((town.get("unlocked_shops") or []) if isinstance(town, dict) else [])
        player = int(observation.get("player", 0))
        farms = observation.get("farms") or []
        rival = farms[1 - player] if len(farms) > 1 - player >= 0 else {}
        money = float((rival or {}).get("money", 0) or 0)
        inv = (observation.get("market") or {}).get("inventory") or {}
        wheat = int(inv.get("WHEAT", 0) or 0)
    except Exception:
        return {"matches": empty, "confidence": 0.0}

    # ---- step-2 身份指纹（跨步自包含；步序回跳/无快照时重抓） ----
    try:
        ident = match_sellflow._identity
    except Exception:
        ident = None
    if step == 2 or not isinstance(ident, dict) or int(ident.get("step", 10 ** 9)) > step:
        ident = {"step": step, "money": round(money, 3), "wheat": wheat}
        try:
            match_sellflow._identity = ident
        except Exception:
            pass
    fp_money, fp_wheat = ident.get("money", round(money, 3)), int(ident.get("wheat", wheat))

    try:
        keys = library.get("keys") or {}
        glob = library.get("global") or {}
        # 规范键=建库件口径（sellflow.py 真库真值）：shop_pair="|".join
        # （≥2 店）/"OPEN1:<s0>"（1 店）/"EARLY"（0 店）；fingerprint=
        # "m<int(money)>_w<int(wheat)>"。其余候选作容错同查。
        if len(shops) >= 2:
            sp_canon = "|".join(str(s) for s in shops[:2])
        elif len(shops) == 1:
            sp_canon = f"OPEN1:{shops[0]}"
        else:
            sp_canon = "EARLY"
        fp_canon = f"m{int(fp_money)}_w{int(fp_wheat)}"
        cand = [f"{sp_canon}||{fp_canon}"]
        shop_pair = ",".join(str(s) for s in shops[:2])
        for sp in (shop_pair, str(tuple(str(s) for s in shops[:2]))):
            for fp in (f"{fp_money}:{fp_wheat}", f"({fp_money}, {fp_wheat})"):
                cand.append(f"{sp}||{fp}")
        entry, source, key_used, n_episodes = None, "none", None, 0
        if isinstance(keys, dict):
            for c in cand:
                hit = keys.get(c)
                if isinstance(hit, dict) and isinstance(hit.get("hist"), dict):
                    entry, source, key_used = hit["hist"], "key", c
                    n_episodes = int(hit.get("n_episodes", 0) or 0)
                    break
        if entry is None and isinstance(glob, dict) and glob:
            entry, source = glob, "global"
        if entry is None:
            return {"matches": dict(empty, step=step), "confidence": 0.0}
        # ---- 窗口聚合（win=step//48，±1） ----
        cur_win = step // 48
        wins = [cur_win - 1, cur_win, cur_win + 1]
        items: Dict[str, Dict[str, int]] = {}
        n = 0
        for w in wins:
            bucket = entry.get(str(w), entry.get(w))
            if not isinstance(bucket, dict):
                continue
            for item, rec in bucket.items():
                if not isinstance(rec, dict):
                    continue
                try:
                    qs = int(rec.get("qty_sum", 0) or 0)
                    cnt = int(rec.get("count", 0) or 0)
                    qm = int(rec.get("qty_max", 0) or 0)
                except Exception:
                    continue
                agg = items.setdefault(str(item), {"qty_sum": 0, "count": 0, "qty_max": 0})
                agg["qty_sum"] += qs
                agg["count"] += cnt
                agg["qty_max"] = max(agg["qty_max"], qm)
                n += cnt
        total = sum(a["qty_sum"] for a in items.values())
        top = max((a["qty_sum"] for a in items.values()), default=0)
        concentration = (top / total) if total > 0 else 0.0
        confidence = min(1.0, n / 10.0) * concentration
        if source == "key" and n_episodes:
            pass  # n_episodes 为注记字段，置信只依样本数与集中度
        return {"matches": {"items": items, "wins": wins, "source": source,
                            "key": key_used, "step": step},
                "confidence": float(confidence)}
    except Exception:
        return {"matches": dict(empty, step=step), "confidence": 0.0}


def extrapolate_sells(inference: Any, matches: Any, plan: Any) -> Dict[str, Any]:
    """差分外推（R21 L4）：净卖推断+卖流匹配合成对手未来 1-2 步预期 SELL 单
    （["SELL",item,qty]）写入 opponent_plan 容器对应步位。

    契约：plan=按步索引的 dict 列表（基座 _front_run 契约 plan[step]["market"]
    单形状）。合成规则（简单可测）：
      候选品 = 推断净卖>0 的品 ∪ 库分布有量（count>0 且 qty_sum>0）的品；
      qty = 净卖（net_qty>0）否则 库均单量 round(qty_sum/count)；≤0 不写；
      步位 = 当前步+1 与 +2（当前步取推断账 "step"，缺→匹配结果 "step"，
      仍缺→不写）；同槽已有该品 SELL 单→量取 max 合并（不重复堆单）。
    置信 < 0.5 → 全部不写（fail-safe 不动作）。

    inference 兼容两形：推断账 {"step","items":{item:{net_qty,lower_bound}},
    ...}（infer_rival_sells._ledger）或净卖映射 {item:{net_qty,...}}。
    matches = match_sellflow 输出 {"matches":…, "confidence":…}。

    签名意图：输入: 推断账+匹配结果+plan 容器 /
    输出: {"written": [{"step","item","qty"}], "skipped": [{"item","reason"}]} /
    错误: 容器畸形/槽位畸形→该处不写不抛。
    """

    def _skip(items, reason):
        return [{"item": i, "reason": reason} for i in items]

    try:
        conf, dist, match_step = 0.0, {}, None
        if isinstance(matches, dict):
            conf = float(matches.get("confidence", 0.0) or 0.0)
            inner = matches.get("matches")
            if isinstance(inner, dict):
                match_step = inner.get("step", matches.get("step"))
                dist = inner.get("items") if isinstance(inner.get("items"), dict) else {}
            else:
                match_step = matches.get("step")
        inf_step = None
        if isinstance(inference, dict) and isinstance(inference.get("items"), dict):
            inf_map = inference["items"]
            inf_step = inference.get("step")
        elif isinstance(inference, dict):
            inf_map = {k: v for k, v in inference.items()
                       if isinstance(v, dict) and "net_qty" in v}
        else:
            inf_map = {}
    except Exception:
        return {"written": [], "skipped": [{"item": "*", "reason": "bad_input"}]}

    candidates = []
    try:
        for item, rec in inf_map.items():
            try:
                if int(rec.get("net_qty", 0) or 0) > 0:
                    candidates.append(str(item))
            except Exception:
                continue
        for item, rec in dist.items():
            try:
                if int(rec.get("count", 0) or 0) > 0 and int(rec.get("qty_sum", 0) or 0) > 0 \
                        and str(item) not in candidates:
                    candidates.append(str(item))
            except Exception:
                continue
    except Exception:
        candidates = []

    if not isinstance(plan, list):
        return {"written": [], "skipped": _skip(candidates or ["*"], "bad_plan")}
    step = inf_step if inf_step is not None else match_step
    if step is None:
        return {"written": [], "skipped": _skip(candidates or ["*"], "no_step")}
    if conf < 0.5:
        return {"written": [], "skipped": _skip(candidates or ["*"], "low_confidence")}

    written, skipped = [], []
    for item in candidates:
        try:
            net = int(inf_map.get(item, {}).get("net_qty", 0) or 0)
            rec = dist.get(item) or {}
            cnt = int(rec.get("count", 0) or 0)
            qs = int(rec.get("qty_sum", 0) or 0)
            rate = int(round(qs / cnt)) if cnt > 0 else 0
            qty = net if net > 0 else rate
        except Exception:
            skipped.append({"item": item, "reason": "bad_record"})
            continue
        if qty <= 0:
            skipped.append({"item": item, "reason": "no_qty"})
            continue
        placed = 0
        for t in (int(step) + 1, int(step) + 2):
            if t < 0 or t >= len(plan):
                continue
            slot = plan[t]
            if not isinstance(slot, dict):
                continue
            market = slot.get("market")
            if market is None:
                market = []
                slot["market"] = market
            if not isinstance(market, list):
                continue
            merged = False
            for order in market:
                if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL" \
                        and order[1] == item:
                    try:
                        order[2] = max(int(order[2] or 0), int(qty))
                    except Exception:
                        pass
                    merged = True
                    break
            if not merged:
                market.append(["SELL", item, int(qty)])
            written.append({"step": t, "item": item, "qty": int(qty)})
            placed += 1
        if placed == 0:
            skipped.append({"item": item, "reason": "bad_slot"})
    return {"written": written, "skipped": skipped}


def apply_dodge(observation: Dict[str, Any], action: Dict[str, Any],
                predictions: Any) -> Dict[str, Any]:
    """避让（R21 L4）：预测对手 1-2 步内集中抛售某品（置信足）→我方本步该品
    SELL 单顺延（槽置 [] 保位次）或减量改单；否则零动作。

    判定（简单可测）：predictions={"confidence": float, "sells":
    [{"item","qty","steps"}]}（qty=该品未来 1-2 步合计预期抛售量，steps=抛售
    步位）。置信 ≥ 0.5 且该品合计 Q ≥ 3（集中抛售线）才动该品，否则零动作。
    动作（只动卖单时点/量）：仅扫 action["market"] 中 ["SELL", item, q]——
      Q ≥ q → 整单顺延：槽置 []（保位次），dodges 记
        {"op":"defer","item","qty","slot","due_step"}（due_step=预测抛售末步）；
      0 < Q < q → 减量改单 ["SELL", item, q−Q]，{"op":"reduce","qty":Q,
        "new_qty":q−Q,…}。
    不碰 BUY_*（买种养单）、farmer/hands（HARVEST/FEED/CARE）、槽位数与出口
    截断；非 SELL 与空槽原样。

    签名意图：输入: observation, action, 预测结果 / 输出:
    {"action": 调整后 action（零动作=原对象）, "dodges": 避让账} /
    错误: 异常→原 action 同对象+dodges=[]。
    """
    try:
        conf = 0.0
        sells = []
        if isinstance(predictions, dict):
            conf = float(predictions.get("confidence", 0.0) or 0.0)
            raw = predictions.get("sells")
            if not isinstance(raw, list):
                raw = predictions.get("written")
            if isinstance(raw, list):
                agg: Dict[str, Dict[str, Any]] = {}
                for rec in raw:
                    if not isinstance(rec, dict) or not rec.get("item"):
                        continue
                    item = str(rec["item"])
                    try:
                        q = abs(int(rec.get("qty", 0) or 0))
                    except Exception:
                        q = 0
                    steps = rec.get("steps")
                    if not isinstance(steps, list):
                        steps = [rec["step"]] if rec.get("step") is not None else []
                    slot = agg.setdefault(item, {"item": item, "qty": 0, "steps": []})
                    slot["qty"] += q
                    for s in steps:
                        if s not in slot["steps"]:
                            slot["steps"].append(s)
                sells = [v for v in agg.values() if v["qty"] > 0]
    except Exception:
        return {"action": action, "dodges": []}

    if conf < 0.5 or not sells:
        return {"action": action, "dodges": []}
    try:
        if not isinstance(action, dict):
            return {"action": action, "dodges": []}
        market = action.get("market")
        if not isinstance(market, list):
            return {"action": action, "dodges": []}
    except Exception:
        return {"action": action, "dodges": []}

    try:
        dodge_min_qty = 3
        new_market = list(market)
        dodges = []
        for pred in sells:
            item, total = pred["item"], int(pred["qty"])
            if total < dodge_min_qty:
                continue
            due = max(pred["steps"]) if pred["steps"] else -1
            for i, order in enumerate(market):
                if not (isinstance(order, list) and len(order) >= 3
                        and order[0] == "SELL" and order[1] == item):
                    continue
                try:
                    q = int(order[2] or 0)
                except Exception:
                    continue
                if q <= 0:
                    continue
                if total >= q:
                    new_market[i] = []
                    dodges.append({"op": "defer", "item": item, "qty": q,
                                   "slot": i, "due_step": due})
                else:
                    new_market[i] = ["SELL", item, q - total]
                    dodges.append({"op": "reduce", "item": item, "qty": total,
                                   "new_qty": q - total, "slot": i, "due_step": due})
        if not dodges:
            return {"action": action, "dodges": []}
        return {"action": dict(action, market=new_market), "dodges": dodges}
    except Exception:
        return {"action": action, "dodges": []}


def _predict_agent(observation: Dict[str, Any]) -> Dict[str, Any]:
    """入口包装（R21 L3，单参官方入口，last-callable）：父层取动作→推断账→
    match→extrapolate 写 opponent_plan 容器→apply_dodge 调整本步卖单→返回。

    接线：父层=注入层捕获变量 _PREDICT_PARENT、库=内嵌 _PREDICT_LIBRARY，
    均经 globals() 查找（本函数体内回退方案；测试可注入假父层/假库）。
    流程：step==0 复位（infer 账本、match step-2 身份、自家成交账、避让账、
    plan 容器 _predict_agent._opponent_plan，槽形 {"market": [...]}）→
    父层取动作 → infer_rival_sells（自家成交账=上一步本层最终动作的市场单：
    SELL 价>1 记 sell、$1 记 floor_sells、BUY_PRODUCT 记 buy）→ match_sellflow
    → extrapolate_sells（推断账+匹配结果写 plan 容器）→ apply_dodge（按 written
    聚合 {item:{qty 合计,steps}}+置信做避让）→ 返回调整后动作。
    只动卖单时点/量。任何异常→父层动作原样（fail-safe）；父层缺失/父层抛
    →PASS 兜底 {"farmer":["PASS"],"hands":[],"market":[]}。
    """
    base_action = None
    try:
        if not isinstance(observation, dict):
            raise TypeError("observation must be a dict")
        raw_step = observation.get("step")
        if raw_step is None:
            step = int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
        else:
            if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
                raise TypeError("observation[step] must be a number")
            step = int(raw_step)

        # ---- step==0 复位账与 plan 容器 ----
        if step == 0:
            try:
                infer_rival_sells._ledger = None
            except Exception:
                pass
            try:
                match_sellflow._identity = None
            except Exception:
                pass
            _predict_agent._own_fills = {"sell": {}, "buy": {}, "floor_sells": {}}
            _predict_agent._dodge_log = []
            _predict_agent._opponent_plan = []

        parent = globals().get("_PREDICT_PARENT")
        if not callable(parent):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        base_action = parent(observation)

        plan = getattr(_predict_agent, "_opponent_plan", None)
        if not isinstance(plan, list):
            plan = []
        while len(plan) <= min(step + 2, 719):
            plan.append({"market": []})
        _predict_agent._opponent_plan = plan

        own_fills = getattr(_predict_agent, "_own_fills", None)
        if not isinstance(own_fills, dict):
            own_fills = {"sell": {}, "buy": {}, "floor_sells": {}}

        inference = infer_rival_sells(observation, own_fills)
        ledger = getattr(infer_rival_sells, "_ledger", None)
        infer_arg = ledger if isinstance(ledger, dict) and isinstance(ledger.get("items"), dict) \
            else inference
        library = globals().get("_PREDICT_LIBRARY")
        match = match_sellflow(observation, library)
        ext = extrapolate_sells(infer_arg, match, plan)

        agg: Dict[str, Dict[str, Any]] = {}
        for rec in ext.get("written") or []:
            if not isinstance(rec, dict) or not rec.get("item"):
                continue
            slot = agg.setdefault(str(rec["item"]), {"item": str(rec["item"]),
                                                     "qty": 0, "steps": []})
            try:
                slot["qty"] += abs(int(rec.get("qty", 0) or 0))
            except Exception:
                pass
            try:
                if rec.get("step") is not None and rec["step"] not in slot["steps"]:
                    slot["steps"].append(rec["step"])
            except Exception:
                pass
        predictions = {"confidence": (match or {}).get("confidence", 0.0),
                       "sells": [v for v in agg.values() if v["qty"] > 0]}
        dodged = apply_dodge(observation, base_action, predictions)
        final_action = dodged.get("action", base_action)

        # ---- 自家成交账（供下一步 infer）+避让账 ----
        try:
            prices = (observation.get("market") or {}).get("prices") or {}
            fills = {"sell": {}, "buy": {}, "floor_sells": {}}
            market = final_action.get("market") if isinstance(final_action, dict) else None
            for o in market or []:
                if not (isinstance(o, list) and len(o) >= 3):
                    continue
                op, item = o[0], o[1]
                try:
                    q = abs(int(o[2] or 0))
                except Exception:
                    continue
                if op == "SELL":
                    p = prices.get(item) if isinstance(prices, dict) else None
                    if isinstance(p, (int, float)) and not isinstance(p, bool) and p <= 1:
                        fills["floor_sells"][item] = fills["floor_sells"].get(item, 0) + q
                    else:
                        fills["sell"][item] = fills["sell"].get(item, 0) + q
                elif op == "BUY_PRODUCT":
                    fills["buy"][item] = fills["buy"].get(item, 0) + q
            _predict_agent._own_fills = fills
        except Exception:
            pass
        log = getattr(_predict_agent, "_dodge_log", None)
        if not isinstance(log, list):
            log = []
        log.extend(dodged.get("dodges") or [])
        _predict_agent._dodge_log = log
        return final_action
    except Exception:
        return base_action if base_action is not None \
            else {"farmer": ["PASS"], "hands": [], "market": []}
