# -*- coding: utf-8 -*-
"""predict_block（R21 运行时链，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
_predict_agent（单参官方入口，父层=_r37_agent 链）→ infer_rival_sells（净卖
反推：公开库存差分−自家成交−确定性城镇消费，$1 地板为下界）→ match_sellflow
（卖流库检索：首二店+step-2 身份指纹）→ extrapolate_sells（差分外推 v2：
限频六道门+量级档+credit 减记，1-2 步钩子写入 opponent_plan 容器）→
apply_dodge（v2 门：预测倾销价<base→deny，action 原样零改动）。
置信不足→不动作 fail-safe；门只出 allow/deny 信号不改动作。开火门/credit
自供给校准 09-27（B27 调参再战，拦截数据 evidence/fire_calibration.json）：
克隆门放宽为「克隆 或 置信≥0.3 且历史门过」、plan 段缺→自家近 48 步实卖净额
自供给，六道门常数零改动（详见 _predict_agent docstring）。本文件源文本由
inject_predict_block 追加进包内（含内嵌库数据）。

实现口径（自包含：常数/小工具定义在各函数体内，stdlib only，注入底版
globals 零撞名；外部接线名 _PREDICT_PARENT/_PREDICT_LIBRARY 经 globals()
查找——注入层捕获行/内嵌库数据提供，测试可直接注入假父层与假库）。
"""
from typing import Any, Dict  # noqa: F401


def infer_rival_sells(observation: Dict[str, Any], own_fills: Any) -> Dict[str, Any]:
    """净卖反推 v2（R22 改2）：market.inventory 差分−自家成交−确定性城镇消费
    →对手上一步净卖量/品类；删失处理（$1 地板只记下界）+噪声门；跨步账本供外推。

    引擎口径（kaggriculture.py）：步 S 的更新=双方成交（_process_market）后
    立即 _town_consume(S)——故观测差分 obs[S]→obs[S+1] 覆盖「步 S 的成交 +
    步 S 触发的城镇消费」；逆推式
      D = 库存差分 + 城镇消费，U = 自家净卖（sell−buy），对手净卖 = D−U。
    城镇消费（确定性，interval 取 4/24）：S % 4 == 0 时每 shop 实例对旗下
    各品扣 multiplier（单品类店 2、多品类店 1）；S % 24 == 0 时中心单全品
    （FERTILIZER 除外）各扣 1。
    自家快照=**最终改单后**动作流：own_fills 参数即最终动作账（_predict_agent
    从最终 action 收账），杜绝 stale-snapshot trap（改单差额全记到对手头上）。
    自家 SELL 价>1 才入库存（引擎 _commit_unit：$1 成交不入库存）→ 不计入
    自家净卖，改记 floor_sells 佐证删失。

    删失处理（R22 改2）：$1 地板成交不入公开库存→公开库存差分低估对手卖量，
    地板截断后无有限上界。反推时该品满足任一删失/噪声条件——现/前步市场价
    ≤$3、推算 sold=max(0,D−U)<2（噪声门，不入精确账）、自家账带 floor_sells
    （$1 成交对公开库存不可见）——净卖**只记下界** {"net_qty": max(0,D−U),
    "lower_bound": True}，禁止当精确值、禁止填 0（下界为 0 即整条不入账）。
    非删失（价>$3 且 sold≥2 且无 floor 证据）→ 精确账 {"net_qty": D−U,
    "lower_bound": False}。

    跨步账本 = 函数属性 infer_rival_sells._ledger（自包含）：
      {"step", "prev": {"step","inv","prices","shops"},
       "items": {item: {net_qty, lower_bound}}, "history": {item: [net_qty,...]}}
    仅当 prev.step == step−1（相邻步）才出账；步序跳跃/首步/step 0 只重建
    快照不出账。供 extrapolate_sells 差分外推。

    签名意图：输入: observation（逐步调用）+自有最终成交账
    {"sell":{item:qty},"buy":{item:qty}[,"floor_sells":{item:qty}]}（可 None）/
    输出: {item: {net_qty, lower_bound}}（下界>0 或精确净卖才入账）/
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
            sold = max(0, net)
            # ---- 删失/噪声门：价≤$3 或 sold<2 或自家 floor_sells 证据 ----
            censored = f_floor.get(item, 0) > 0 or sold < 2
            for p in (prices_now.get(item), prices_prev.get(item)):
                if isinstance(p, (int, float)) and not isinstance(p, bool) and p <= 3:
                    censored = True
            if censored:
                if sold == 0:
                    continue  # 禁填 0：下界为 0 不入账（删失后无有限上界）
                rec = {"net_qty": int(sold), "lower_bound": True}
            else:
                if net == 0:
                    continue
                rec = {"net_qty": int(net), "lower_bound": False}
            result[item] = rec
            hist = history.setdefault(item, [])
            if isinstance(hist, list):
                hist.append(int(rec["net_qty"]))
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
    """卖流库检索 v2（R22 改3）：TOP-1 键匹配（只取命中的最优一键，不做多键
    展开）；远端信号（预测 1-4 回合后）需库条目带 history_hits≥3 且
    hit_rate≥0.70（库新字段）才采纳，否则 skipped；无键回退 library["global"]
    且置信降一档（×0.5）。

    库结构（与 build_sellflow_library 共同约定）：
      {"version", "keys": {f"{shop_pair}||{fingerprint}":
          {"n_episodes", "hist": {"<win>": {"<ITEM>":
              {"qty_sum","count","qty_max"}}}
           [,"history_hits": int, "hit_rate": float]}},
       "global": {同 hist 形 或入口形 {"n_episodes","hist"[,"history_hits",
           "hit_rate"]}}}，win = step//48。
    键编码（本件钉住，兼容候选同查）：shop_pair=",".join(unlocked_shops[:2])；
    fingerprint=f"{round(float(money),3)}:{int(WHEAT inv)}"（step==2 的对手
    快照：farms[1−player].money + market.inventory.WHEAT；跨步身份存函数属性
    match_sellflow._identity，无快照回退当前观测值）。
    取窗：win=step//48，聚合 win−1..win+1（w=1）内各品直方。
    TOP-1：候选键（规范键+兼容键）命中的入口按 n_episodes 最大取一（同分取
    候选序最前，"最优"=样本数最多），只聚合该一键，不做多键展开。
    历史置信门（远端 1-4 回合信号）：选中入口带 history_hits/hit_rate 新字段
    →须 history_hits≥3 且 hit_rate≥0.70（含界）才采纳；否则 source="skipped"、
    items 空、confidence=0。缺新字段=旧库条目沿 v1 采纳（门只对带字段条目生效）。
    无键→library["global"]（支持 bare-hist 与入口两形），置信 ×0.5 降一档。

    置信口径（简单可测）：
      样本因子 = min(1, n/10)，n=窗内 count 之和；
      集中度 = 最大单品 qty_sum / 全部 qty_sum（空分布=0）；
      confidence = 样本因子 × 集中度 ∈ [0,1]（global 再 ×0.5）。

    签名意图：输入: observation+库 /
    输出: {"matches": {"items","wins","source","key","step","skipped"},
           "confidence", "top1": {"key","source","adopted"}} /
    错误: 库缺失/畸形→confidence=0（不抛）。
    """
    empty = {"items": {}, "wins": [], "source": "none", "key": None,
             "step": -1, "skipped": True}
    top_none = {"key": None, "source": "none", "adopted": False}
    try:
        if not isinstance(observation, dict):
            return {"matches": empty, "confidence": 0.0,
                    "top1": dict(top_none)}
        raw_step = observation.get("step")
        if raw_step is None:
            step = int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
        else:
            step = int(raw_step)
        if not isinstance(library, dict) or not library:
            return {"matches": dict(empty, step=step), "confidence": 0.0,
                    "top1": dict(top_none)}
        town = observation.get("town") or {}
        shops = list((town.get("unlocked_shops") or []) if isinstance(town, dict) else [])
        player = int(observation.get("player", 0))
        farms = observation.get("farms") or []
        rival = farms[1 - player] if len(farms) > 1 - player >= 0 else {}
        money = float((rival or {}).get("money", 0) or 0)
        inv = (observation.get("market") or {}).get("inventory") or {}
        wheat = int(inv.get("WHEAT", 0) or 0)
    except Exception:
        return {"matches": empty, "confidence": 0.0, "top1": dict(top_none)}

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
        fp_canon = f"m{int(round(float(fp_money)))}_w{int(fp_wheat)}"  # 与建库 int(round()) 对齐
        cand = [f"{sp_canon}||{fp_canon}"]
        shop_pair = ",".join(str(s) for s in shops[:2])
        for sp in (shop_pair, str(tuple(str(s) for s in shops[:2]))):
            for fp in (f"{fp_money}:{fp_wheat}", f"({fp_money}, {fp_wheat})"):
                cand.append(f"{sp}||{fp}")
        # ---- TOP-1：候选命中里按 n_episodes 取最优一键（同分取候选序最前） ----
        best = None
        if isinstance(keys, dict):
            for idx, c in enumerate(cand):
                hit = keys.get(c)
                if isinstance(hit, dict) and isinstance(hit.get("hist"), dict):
                    n_hit = int(hit.get("n_episodes", 0) or 0)
                    if best is None or n_hit > best[0]:
                        best = (n_hit, idx, c, hit)
        entry, source, key_used, gate_src = None, "none", None, None
        if best is not None:
            _, _, key_used, gate_src = best
            entry, source = gate_src["hist"], "key"
        elif isinstance(glob, dict) and glob:
            if isinstance(glob.get("hist"), dict):
                gate_src, entry = glob, glob["hist"]
            else:
                gate_src, entry = glob, glob
            source = "global"
        if entry is None:
            return {"matches": dict(empty, step=step), "confidence": 0.0,
                    "top1": dict(top_none)}
        # ---- 历史置信门（远端 1-4 回合信号；带新字段条目才走门） ----
        if isinstance(gate_src, dict) and ("history_hits" in gate_src
                                           or "hit_rate" in gate_src):
            try:
                h_hits = int(gate_src.get("history_hits", 0) or 0)
                h_rate = float(gate_src.get("hit_rate", 0.0) or 0.0)
            except Exception:
                h_hits, h_rate = 0, 0.0
            adopted = h_hits >= 3 and h_rate >= 0.70
        else:
            adopted = True  # 旧库条目（无新字段）沿 v1 采纳
        top1 = {"key": key_used, "source": source, "adopted": bool(adopted)}
        if not adopted:
            return {"matches": {"items": {}, "wins": [], "source": "skipped",
                                "key": key_used, "step": step, "skipped": True},
                    "confidence": 0.0, "top1": top1}
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
        if source == "global":
            confidence *= 0.5  # 无键回退 global：置信降一档
        return {"matches": {"items": items, "wins": wins, "source": source,
                            "key": key_used, "step": step, "skipped": False},
                "confidence": float(confidence), "top1": top1}
    except Exception:
        return {"matches": dict(empty, step=step), "confidence": 0.0,
                "top1": dict(top_none)}


def extrapolate_sells(inference: Any, matches: Any, plan: Any,
                      credit: Any = None) -> Dict[str, Any]:
    """差分外推 v2（R22 改1/改2/改3）：限频六道门 + 量级档 + credit 减记。

    限频六道门（全过才写；任一不过→skipped 记因不写）：
      ①触发窗：step∈[336,646]（步号取 inference["step"]，缺→matches 步号，
        仍缺→不写 no_step）；
      ②开火门槛：近 2 回合（step+1+step+2）TOP-1 预测净卖 = 2×pred ≥ K=4；
        pred=推断净卖 net_qty（>0 时）否则 TOP-1 库均单量 round(qty_sum/count)；
      ③每步每品恰 1 单：目标步位已有该品 SELL 单→该步位跳过不堆单（dup）；
      ④量级带通：qty=min(该品棚存, 自家 48h 计划卖量余量) 且 4≤qty≤99
        （两端拒绝：带外不写 band；带内含界 4/99）；
      ⑤价门：min_sell_price=2 + base 价门——base=obs 市场价该品（传入账
        prices 段，缺→推断账 prev.prices）；预测倾销价<base→不写（price）、
        预测倾销价<2→不写（floor）；
      ⑥噪声门：matches.skipped（远端未过历史门）→不写（noise）。
    输出量级档：written 条目 {"item","qty","tier"}，**不写具体步位**；tier 按
    qty 分档 少<20 / 中 20-60 / 多>60；plan 写入沿 v1 的 1-2 回合步位
    （step+1/step+2）仅作 _front_run 钩子触发，tier 供抢跑量决策。
    credit 减记：每写一单，credit 账按 qty 扣减该品自家后续计划卖量
    （禁净加卖：credit≤0 不再写、累计写量 ≤ 计划量）。

    credit 账（传入账；credit 参数缺→函数属性 extrapolate_sells._credit；
    可为 callable；纯 credit 形 {item: 余量} 等价 {"plan": 该形}）：
      {"stock": {item: 棚存},              # observation["private"]["shed"] 口径
       "plan": {item: 48h 计划卖量余量},    # credit 记账本体（写单减记）
       "prices": {item: base 价},          # obs 市场价（缺该品→不写 fail-safe）
       "dump_prices": {item: 预测倾销价}}   # 缺省=base（放行）
    棚存/计划量/基价取不到→不写（fail-safe）。本件合同零改动（校准 09-27）：
    plan 段缺时的自供给归 _predict_agent 账面段（近 48 步自家实卖净额），
    直调本件仍按 fail-safe 不写。

    签名意图：输入: 推断账+匹配结果+plan 容器+credit 账（可选 credit=None）/
    输出: {"written": [{"item","qty","tier"}], "skipped": [{"item","reason"}],
           "credit_debited": [{"item","step","qty"}]} /
    错误: 容器畸形/槽位畸形/坏输入→不写不抛。
    """
    K = 4                      # 开火门槛：近 2 回合预测净卖下限（单位）
    WIN_LO, WIN_HI = 336, 646  # 触发窗（含界）
    QTY_LO, QTY_HI = 4, 99     # 量级带通（含界）
    MIN_SELL_PRICE = 2         # 机箱价地板

    def _skip(items, reason):
        return [{"item": i, "reason": reason} for i in items]

    def _account(raw):
        if callable(raw):
            try:
                raw = raw()
            except Exception:
                raw = None
        if not isinstance(raw, dict):
            raw = {}
        if any(k in raw for k in ("stock", "plan", "prices", "dump_prices")):
            stock = raw.get("stock") if isinstance(raw.get("stock"), dict) else {}
            plan_map = raw.get("plan") if isinstance(raw.get("plan"), dict) else {}
            prices = raw.get("prices") if isinstance(raw.get("prices"), dict) else {}
            dump = raw.get("dump_prices") if isinstance(raw.get("dump_prices"), dict) else {}
        else:
            stock, prices, dump = {}, {}, {}
            plan_map = raw  # 纯 credit 形 {item: 计划卖量余量}
        return stock, plan_map, prices, dump

    try:
        dist, match_step, noise = {}, None, False
        if isinstance(matches, dict):
            inner = matches.get("matches")
            if isinstance(inner, dict):
                match_step = inner.get("step", matches.get("step"))
                dist = inner.get("items") if isinstance(inner.get("items"), dict) else {}
                noise = bool(inner.get("skipped", False))
            else:
                match_step = matches.get("step")
        inf_step = None
        inf_prices: Dict[str, Any] = {}
        if isinstance(inference, dict) and isinstance(inference.get("items"), dict):
            inf_map = inference["items"]
            inf_step = inference.get("step")
            prev = inference.get("prev")
            if isinstance(prev, dict) and isinstance(prev.get("prices"), dict):
                inf_prices = prev["prices"]
        elif isinstance(inference, dict):
            inf_map = {k: v for k, v in inference.items()
                       if isinstance(v, dict) and "net_qty" in v}
        else:
            inf_map = {}
    except Exception:
        return {"written": [], "skipped": [{"item": "*", "reason": "bad_input"}],
                "credit_debited": []}

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
        return {"written": [], "skipped": _skip(candidates or ["*"], "bad_plan"),
                "credit_debited": []}
    step = inf_step if inf_step is not None else match_step
    try:
        if isinstance(step, bool) or not isinstance(step, (int, float)):
            raise TypeError("step")
        step = int(step)
    except Exception:
        return {"written": [], "skipped": _skip(candidates or ["*"], "no_step"),
                "credit_debited": []}

    raw_credit = credit if credit is not None else getattr(extrapolate_sells, "_credit", None)
    stock_map, plan_map, price_map, dump_map = _account(raw_credit)

    written, skipped, debits = [], [], []
    in_window = WIN_LO <= step <= WIN_HI
    for item in candidates:
        # ⑥噪声门：远端未过历史门的信号不写
        if noise:
            skipped.append({"item": item, "reason": "noise"})
            continue
        # ①触发窗
        if not in_window:
            skipped.append({"item": item, "reason": "window"})
            continue
        # ---- TOP-1 预测量（②开火门槛：近 2 回合 ≥K 单位） ----
        try:
            net = int(inf_map.get(item, {}).get("net_qty", 0) or 0)
        except Exception:
            net = 0
        rec = dist.get(item) or {}
        try:
            cnt = int(rec.get("count", 0) or 0)
            qs = int(rec.get("qty_sum", 0) or 0)
        except Exception:
            cnt, qs = 0, 0
        rate = int(round(qs / cnt)) if cnt > 0 else 0
        pred = net if net > 0 else rate
        if 2 * pred < K:
            skipped.append({"item": item, "reason": "below_k"})
            continue
        # ---- 账面量（④：qty=min(棚存, 自家 48h 计划卖量)） ----
        try:
            credit_left = plan_map.get(item)
            if credit_left is None:
                raise TypeError("plan")
            credit_left = int(credit_left)
        except Exception:
            skipped.append({"item": item, "reason": "no_account"})
            continue
        if credit_left <= 0:
            skipped.append({"item": item, "reason": "no_credit"})
            continue
        try:
            if stock_map.get(item) is None:
                raise TypeError("stock")
            stock_qty = int(stock_map[item])
        except Exception:
            skipped.append({"item": item, "reason": "no_account"})
            continue
        qty = min(stock_qty, credit_left)
        if qty < QTY_LO or qty > QTY_HI:
            skipped.append({"item": item, "reason": "band"})
            continue
        # ---- 价门（⑤：min_sell_price=2 + base 价门） ----
        base = price_map.get(item)
        if base is None:
            base = inf_prices.get(item)
        try:
            if base is None:
                raise TypeError("base")
            base = float(base)
        except Exception:
            skipped.append({"item": item, "reason": "no_account"})
            continue
        try:
            dump = float(dump_map.get(item, base))
        except Exception:
            skipped.append({"item": item, "reason": "price"})
            continue
        if dump < base:
            skipped.append({"item": item, "reason": "price"})
            continue
        if dump < MIN_SELL_PRICE:
            skipped.append({"item": item, "reason": "floor"})
            continue
        # ---- 写入（③每步每品恰 1 单 + credit 减记） ----
        placed, why = 0, None
        for t in (step + 1, step + 2):
            if credit_left <= 0:
                break
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
            dup = any(isinstance(o, list) and len(o) >= 3 and o[0] == "SELL"
                      and o[1] == item for o in market)
            if dup:
                why = "dup"
                skipped.append({"item": item, "reason": "dup"})
                continue
            q = min(stock_qty, credit_left)
            if q < QTY_LO or q > QTY_HI:
                why = "band"
                skipped.append({"item": item, "reason": "band"})
                continue
            market.append(["SELL", item, int(q)])
            plan_map[item] = credit_left - int(q)
            credit_left -= int(q)
            tier = "少" if q < 20 else ("中" if q <= 60 else "多")
            written.append({"item": item, "qty": int(q), "tier": tier})
            debits.append({"item": item, "step": t, "qty": int(q)})
            placed += 1
        if placed == 0 and why is None:
            skipped.append({"item": item, "reason": "bad_slot"})
    return {"written": written, "skipped": skipped, "credit_debited": debits}


def apply_dodge(observation: Dict[str, Any], action: Dict[str, Any],
                predictions: Any) -> Dict[str, Any]:
    """避让 v2（R22 改2）=**门**（删除 v1 "顺延置 []/减量改单" 语义——公开负
    结果先例：持货等峰值 −$1.2k~−$3.2k/局）：只做每品 allow/deny 判定，**action
    原样返回零改动**（不碰任何单，防御走价门不前拉、货到棚才卖）。

    判定（每品两分支）：base=observation["market"]["prices"][item]（obs 市场价
    该品）；预测倾销价=predictions["prices"][item]（或 sells/written 条目
    "price"，缺省=base=放行）；**预测倾销价 < base → "deny"**（该品本步不前拉
    不加卖，保留原计划卖单原样），否则 "allow"。
    输出 gates 供调用方（_predict_agent）执行 deny 品的写入作废/credit 回滚；
    本函数自身绝不改 action（同对象返回）。
    异常（observation 非 dict / predictions 畸形 / 评估抛错）→全 allow +
    原 action。

    签名意图：输入: observation, action, 预测结果 /
    输出: {"action": 原 action（同对象零改动）,
           "gates": {item: "allow"|"deny"}} /
    错误: 异常→全 allow+原动作。
    """
    items = []
    price_hint: Dict[str, Any] = {}
    try:
        if isinstance(predictions, dict):
            prices = predictions.get("prices")
            if isinstance(prices, dict):
                for k, v in prices.items():
                    items.append(str(k))
                    price_hint[str(k)] = v
            raw = predictions.get("sells")
            if not isinstance(raw, list):
                raw = predictions.get("written")
            for rec in raw or []:
                if isinstance(rec, dict) and rec.get("item"):
                    it = str(rec["item"])
                    if it not in items:
                        items.append(it)
                    if it not in price_hint and rec.get("price") is not None:
                        price_hint[it] = rec.get("price")
    except Exception:
        items, price_hint = [], {}
    gates: Dict[str, str] = {}
    try:
        market = (observation or {}).get("market") if isinstance(observation, dict) else None
        obs_prices = (market or {}).get("prices") if isinstance(market, dict) else {}
        obs_prices = obs_prices if isinstance(obs_prices, dict) else {}
        for item in items:
            base = obs_prices.get(item)
            dump = price_hint.get(item, base)
            if base is None or dump is None:
                gates[item] = "allow"
                continue
            gates[item] = "deny" if float(dump) < float(base) else "allow"
    except Exception:
        gates = {item: "allow" for item in items}
    return {"action": action, "gates": gates}


def _predict_agent(observation: Dict[str, Any]) -> Dict[str, Any]:
    """入口包装 v2（R22 改1-改3，单参官方入口，last-callable）：父层取动作 →
    detect_clone 判克隆 → 开火门（校准 09-27 放宽，见下）→ infer → match →
    extrapolate（限频六门+量级档+credit 减记）→ apply_dodge 门（deny 品的
    written 条目作废回滚 credit）→ 返回父层动作。

    开火门（校准 09-27，B27 调参再战；拦截数据=evidence/fire_calibration.json）：
    旧=is_clone 单通道（非克隆整链零写入；判决语料 43140 步仅放行 40 步
    0.09%，fire 合计 0 过度限频）→ 新=is_clone ∨（置信≥0.3 ∧ 历史门过）。
    依据拦截数据：置信≥0.7 面过全门候选仅 10 个（落不了健康区 100-1000），
    置信≥0.3 面 299 个/写单 ~403（判据 fire 面 ~260-350 落区）——置信阈随
    拦截分布由 0.7 设想校到 0.3（最小放松集：K=4/窗 336-646/带通 4-99/价门/
    噪声门/每步每品 1 单标定均非瓶颈，零改动）。
    credit 自供给（校准 09-27）：旧=plan 段缺→不写（账面量门 fail-safe；判决
    语料自供给缺位使候选 13165 个被 no_account 唯一卡死、fire 恒 0）→ 新=
    plan 段缺→按自家近 48 步实卖净额自供给（净额=Σ实卖−Σ同窗已开火，禁净
    加卖保留：Σ48h 写量 ≤ Σ48h 自家实卖；净额<带通下限 4 不供给；注入账
    plan 条目优先不覆盖，自供给项每步随窗净额刷新）。

    接线沿 v1：父层=注入层捕获变量 _PREDICT_PARENT、库=内嵌 _PREDICT_LIBRARY，
    均经 globals() 查找（测试可注入假父层/假库）。
    step==0 复位全账后不走链（复位拍原样返回，差分自 step 2 起算）：推断账
    （infer_rival_sells._ledger）、卖流身份
    （match_sellflow._identity）、相似度快照（detect_clone._stream）、plan 容器
    （_predict_agent._opponent_plan，槽形 {"market": [...]}）、credit 账
    （_predict_agent._credit）、自家成交账（_own_fills）、实卖流（_own_flow，
    自供给 credit 用）、自供给集（_self_plan）、门账（_dodge_log）与
    written 作废账（_written）。
    credit 账（可注入 _predict_agent._credit；形见 extrapolate_sells）：
    {"plan": {item: 计划余量}[, "dump_prices"/"stock"/"prices" 覆盖]}；棚存
    （observation["private"]["shed"]）与 base 价（observation["market"]
    ["prices"]）每步自 observation 补齐、账内覆盖优先；plan 段缺→自供给
    （校准 09-27，见上；自供给也取不到→不写 fail-safe）。
    链内 deny 回滚：apply_dodge 判 deny 的品→该品 written 条目作废、plan 钩子
    单撤回、credit 等额回滚（防净加卖账不残留）。返回动作=父层动作原样。
    任何异常→父层动作原样（fail-safe）；父层缺失/父层抛→PASS 兜底
    {"farmer":["PASS"],"hands":[],"market":[]}。
    """
    CONF_TH = 0.3   # 开火门置信阈（校准 09-27：0.7 设想→0.3，依据见 docstring）
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

        # ---- step==0 复位全账 ----
        if step == 0:
            try:
                infer_rival_sells._ledger = None
            except Exception:
                pass
            try:
                match_sellflow._identity = None
            except Exception:
                pass
            try:
                detect_clone._stream = None
            except Exception:
                pass
            _predict_agent._own_fills = {"sell": {}, "buy": {}, "floor_sells": {}}
            _predict_agent._own_flow = []
            _predict_agent._self_plan = set()
            _predict_agent._dodge_log = []
            _predict_agent._opponent_plan = []
            _predict_agent._credit = {}
            _predict_agent._written = []

        parent = globals().get("_PREDICT_PARENT")
        if not callable(parent):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        base_action = parent(observation)
        if step == 0:
            return base_action    # 复位拍不走链（校准 09-27 保 v2 step-0 口径）

        # ---- 自家成交账（供下一步 infer 差分）+实卖流（供自供给 credit） ----
        obs_private = observation.get("private") or {}
        obs_market = observation.get("market") or {}
        obs_prices = obs_market.get("prices") if isinstance(obs_market, dict) else None
        own_fills = getattr(_predict_agent, "_own_fills", None)
        if not isinstance(own_fills, dict):
            own_fills = {"sell": {}, "buy": {}, "floor_sells": {}}
        inference = infer_rival_sells(observation, own_fills)
        fills = {"sell": {}, "buy": {}, "floor_sells": {}}
        try:
            prices_obs = obs_prices if isinstance(obs_prices, dict) else {}
            market = base_action.get("market") if isinstance(base_action, dict) else None
            for o in market or []:
                if not (isinstance(o, list) and len(o) >= 3):
                    continue
                op, item = o[0], o[1]
                try:
                    q = abs(int(o[2] or 0))
                except Exception:
                    continue
                if op == "SELL":
                    p = prices_obs.get(item)
                    if isinstance(p, (int, float)) and not isinstance(p, bool) and p <= 1:
                        fills["floor_sells"][item] = fills["floor_sells"].get(item, 0) + q
                    else:
                        fills["sell"][item] = fills["sell"].get(item, 0) + q
                elif op == "BUY_PRODUCT":
                    fills["buy"][item] = fills["buy"].get(item, 0) + q
            _predict_agent._own_fills = fills
        except Exception:
            pass
        flow_rec = {"own": dict(fills.get("sell") or {}), "fired": {}}
        flow = getattr(_predict_agent, "_own_flow", None)
        if not isinstance(flow, list):
            flow = []
        flow.append(flow_rec)
        del flow[:-48]
        _predict_agent._own_flow = flow

        ledger = getattr(infer_rival_sells, "_ledger", None)
        infer_arg = ledger if isinstance(ledger, dict) and isinstance(ledger.get("items"), dict) \
            else inference
        library = globals().get("_PREDICT_LIBRARY")
        match = match_sellflow(observation, library)

        # ---- 开火门（校准 09-27）：克隆 或 高置信（置信≥0.3 且历史门过） ----
        clone = detect_clone(observation)
        is_clone = isinstance(clone, dict) and bool(clone.get("is_clone"))
        conf, noise = 0.0, True
        try:
            conf = float((match or {}).get("confidence") or 0.0)
            noise = bool(((match or {}).get("matches") or {}).get("skipped", True))
        except Exception:
            pass
        if not (is_clone or (conf >= CONF_TH and not noise)):
            return base_action

        plan = getattr(_predict_agent, "_opponent_plan", None)
        if not isinstance(plan, list):
            plan = []
        while len(plan) <= min(step + 2, 719):
            plan.append({"market": []})
        _predict_agent._opponent_plan = plan

        # ---- credit 账（传入账 + observation 补齐棚存/base 价 + 自供给） ----
        acct = getattr(_predict_agent, "_credit", None)
        if not isinstance(acct, dict):
            acct = {}
        obs_shed = obs_private.get("shed") if isinstance(obs_private, dict) else None
        stock = dict(obs_shed) if isinstance(obs_shed, dict) else {}
        if isinstance(acct.get("stock"), dict):
            stock.update(acct["stock"])
        prices = dict(obs_prices) if isinstance(obs_prices, dict) else {}
        if isinstance(acct.get("prices"), dict):
            prices.update(acct["prices"])
        plan_map = acct.get("plan")
        if not isinstance(plan_map, dict):
            plan_map = {}
            acct["plan"] = plan_map
        # ---- 自供给 credit（校准 09-27）：plan 段缺→近 48 步自家实卖净额 ----
        self_items = getattr(_predict_agent, "_self_plan", None)
        if not isinstance(self_items, set):
            self_items = set()
        eff: Dict[str, int] = {}
        try:
            for rec in flow[-48:]:
                if not isinstance(rec, dict):
                    continue
                for k, v in (rec.get("own") or {}).items():
                    eff[k] = eff.get(k, 0) + int(v)
                for k, v in (rec.get("fired") or {}).items():
                    eff[k] = eff.get(k, 0) - int(v)
        except Exception:
            eff = {}
        for item, val in eff.items():
            val = int(val)
            if item in self_items:
                plan_map[item] = max(0, val)     # 自供给项随窗净额刷新
            elif item not in plan_map and val >= 4:
                plan_map[item] = val             # 净额≥带通下限 4 才供给（禁净加卖）
                self_items.add(item)
        _predict_agent._self_plan = self_items
        dump_map = acct.get("dump_prices")
        if not isinstance(dump_map, dict):
            dump_map = {}
            acct["dump_prices"] = dump_map
        _predict_agent._credit = acct
        account = {"stock": stock, "plan": plan_map,
                   "prices": prices, "dump_prices": dump_map}

        ext = extrapolate_sells(infer_arg, match, plan, account)

        agg: Dict[str, Dict[str, Any]] = {}
        for rec in ext.get("written") or []:
            if not isinstance(rec, dict) or not rec.get("item"):
                continue
            item = str(rec["item"])
            slot = agg.setdefault(item, {"item": item, "qty": 0,
                                         "tier": rec.get("tier")})
            try:
                slot["qty"] += abs(int(rec.get("qty", 0) or 0))
            except Exception:
                pass
        pred_prices = {item: dump_map[item] for item in agg if item in dump_map}
        predictions = {"confidence": (match or {}).get("confidence", 0.0),
                       "sells": [v for v in agg.values() if v["qty"] > 0],
                       "prices": pred_prices}
        dodged = apply_dodge(observation, base_action, predictions)
        gates = dodged.get("gates")
        gates = gates if isinstance(gates, dict) else {}

        # ---- deny 回滚：written 条目作废 + plan 钩子单回滚 + credit 回滚 ----
        final_written = []
        for rec in ext.get("written") or []:
            if not isinstance(rec, dict) or not rec.get("item"):
                continue
            if gates.get(str(rec["item"])) == "deny":
                continue
            final_written.append(rec)
        for debit in ext.get("credit_debited") or []:
            if not isinstance(debit, dict) or not debit.get("item"):
                continue
            item = str(debit["item"])
            if gates.get(item) != "deny":
                continue
            try:
                t, q = int(debit.get("step")), int(debit.get("qty"))
            except Exception:
                continue
            slot = plan[t] if 0 <= t < len(plan) and isinstance(plan[t], dict) else None
            market = slot.get("market") if slot else None
            if isinstance(market, list):
                for order in list(market):
                    if isinstance(order, list) and len(order) >= 3 \
                            and order[0] == "SELL" and order[1] == item:
                        try:
                            if int(order[2] or 0) != q:
                                continue
                        except Exception:
                            continue
                        market.remove(order)
                        break
            try:
                plan_map[item] = int(plan_map.get(item, 0) or 0) + q
            except Exception:
                pass
        _predict_agent._written = final_written

        # ---- 实卖流记 fired（校准 09-27 自供给净额；deny 回滚的不计） ----
        try:
            fired_rec = flow_rec.get("fired")
            if not isinstance(fired_rec, dict):
                fired_rec = {}
                flow_rec["fired"] = fired_rec
            for debit in ext.get("credit_debited") or []:
                if not isinstance(debit, dict) or not debit.get("item"):
                    continue
                item = str(debit["item"])
                if gates.get(item) == "deny":
                    continue
                try:
                    q = abs(int(debit.get("qty", 0) or 0))
                except Exception:
                    continue
                fired_rec[item] = fired_rec.get(item, 0) + q
        except Exception:
            pass
        log = getattr(_predict_agent, "_dodge_log", None)
        if not isinstance(log, list):
            log = []
        for item in sorted(gates):
            log.append({"item": item, "gate": gates[item]})
        _predict_agent._dodge_log = log
        return base_action
    except Exception:
        return base_action if base_action is not None \
            else {"farmer": ["PASS"], "hands": [], "market": []}


def detect_clone(observation: Dict[str, Any]) -> Dict[str, Any]:
    """克隆/强匹配判定（R22 改4/改3 门）：step1 现金差<$0.5 或行为相似度
    ≥0.95（近 N=10 步动作流一致率）判克隆；任一字段缺失/边界值→保守返回
    非克隆（不 fire）；跨步快照自包含。

    判定（两规则任一命中 is_clone=True，trigger 记命中规则）：
      ①step1 现金镜像：obs["step"]==1 且 farms[1−player].money 与
        farms[player].money 差 < $0.5（严格；0.5 边界不 fire）；
      ②行为相似度：近 N=10 步动作流一致率 similarity ≥ 0.95（含界）。
    跨步快照 = 函数属性 detect_clone._stream（自包含，测试可注入）：
      {"agree": 一致步数, "total": 总步数, "window": [0/1,...]}——每次调用
    若双方席位动作字段在（farms[i]["action"]，dict/list 动作流）则 canonical
    归一判等追加 1/0，window 只留近 N=10 步并同步 agree/total；
    similarity = agree/total（total==0→0.0）；无动作字段的调用不推进快照
    （similarity 用既有缓存，快照即跨步证据）。
    保守口径：observation 非 dict / step、player、farms、双方 money 缺失、
    畸形（含 bool 冒充数）、席位越界 → 整体返回非克隆；现金差==0.5 边界
    → ①不 fire；异常→非克隆 {is_clone: False, similarity: 0.0, evidence: {}}。

    签名意图：输入: observation（逐步调用） / 输出: {is_clone, similarity,
    evidence} / 错误: 异常→非克隆。
    """
    try:
        if not isinstance(observation, dict):
            return {"is_clone": False, "similarity": 0.0, "evidence": {}}
        raw_step = observation.get("step")
        if raw_step is None:
            step = int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
        else:
            if isinstance(raw_step, bool) or not isinstance(raw_step, (int, float)):
                return {"is_clone": False, "similarity": 0.0, "evidence": {}}
            step = int(raw_step)
        player = observation.get("player")
        if isinstance(player, bool) or not isinstance(player, (int, float)):
            return {"is_clone": False, "similarity": 0.0, "evidence": {}}
        player = int(player)
        if player not in (0, 1):
            return {"is_clone": False, "similarity": 0.0, "evidence": {}}
        farms = observation.get("farms")
        if not isinstance(farms, list) or len(farms) <= 1 - player:
            return {"is_clone": False, "similarity": 0.0, "evidence": {}}
        own_seat, rival_seat = farms[player], farms[1 - player]
        if not isinstance(own_seat, dict) or not isinstance(rival_seat, dict):
            return {"is_clone": False, "similarity": 0.0, "evidence": {}}

        def _money(seat):
            m = seat.get("money")
            if isinstance(m, bool) or not isinstance(m, (int, float)):
                raise ValueError("money missing")
            return float(m)

        m_own, m_rival = _money(own_seat), _money(rival_seat)
    except Exception:
        return {"is_clone": False, "similarity": 0.0, "evidence": {}}

    try:
        cash_diff = abs(m_rival - m_own)
        try:
            st = detect_clone._stream
        except Exception:
            st = None
        st = st if isinstance(st, dict) else {}
        agree = int(st.get("agree", 0) or 0)
        total = int(st.get("total", 0) or 0)
        window = st.get("window") if isinstance(st.get("window"), list) else None

        def _norm(a):
            if isinstance(a, dict):
                return tuple(sorted((str(k), _norm(v)) for k, v in a.items()))
            if isinstance(a, (list, tuple)):
                return tuple(_norm(v) for v in a)
            return a

        own_act, rival_act = own_seat.get("action"), rival_seat.get("action")
        if own_act is not None and rival_act is not None:
            flag = 1 if _norm(own_act) == _norm(rival_act) else 0
            window = list(window or []) + [flag]
            window = window[-10:]  # 近 N=10 步
            agree, total = int(sum(window)), len(window)
            detect_clone._stream = {"agree": agree, "total": total,
                                    "window": window}
        similarity = (agree / total) if total > 0 else 0.0
        trigger = []
        if step == 1 and cash_diff < 0.5:
            trigger.append("cash")
        if total > 0 and similarity >= 0.95:
            trigger.append("similarity")
        evidence = {"step": step, "cash_diff": cash_diff, "agree": agree,
                    "total": total, "trigger": "+".join(trigger) or None}
        return {"is_clone": bool(trigger), "similarity": float(similarity),
                "evidence": evidence}
    except Exception:
        return {"is_clone": False, "similarity": 0.0, "evidence": {}}
