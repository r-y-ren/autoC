# ---- 件 KG：价格膝点量门（谷底三品 FERTILIZER/MILK/WOOL） ----------------
# 形态：尾块注入件（构建时文本拼接进 h1 提交源，与宿主同命名空间）；本文件为
# 块体片段，不含宿主捕获/入口（由 build_knee.py 组装）。仅用基座裸名
# （_xd7_projected 由 h1 共享段提供，失败回退裸 shed）；stdlib-only。
#
# 语义（任务 knee 层口径）：
# - 三品 FERTILIZER/MILK/WOOL 本步 SELL 单量按价格膝点截留：膝点=价崩拐点，
#   简单可实现口径=该品当前 quote < 0.7×base；quote>=0.7×base 全量挂卖；
# - 截留帽=min(沈存×30%, 步帽 X 件)（X=判决标定，两变体 __KG_STEP_CAP__）；
# - 截留不是挪卖：只减不挪、逐条保守、截掉的量留在棚里，由磁带后续卖单/
#   终局清算（712-718）自然出清——终局清算窗 step>=712 不截留（出清路径保真，
#   亦不干扰 E182 终局规划器 712-718 物理守卫）；
# - 零跨拍挪量（禁区红线 R23/R26）、磁带 blob 零触碰；非 SELL 条目/挂量
#   不确定条目原样保留；无可改→返回原动作对象（同对象零足迹）；
# - 异常吞掉回退原动作（同对象零足迹）。
_KG_PARAMS = {
    "items": ("FERTILIZER", "MILK", "WOOL"),
    "base_px": {"FERTILIZER": 100, "MILK": 160, "WOOL": 200},
    "knee_factor": 0.7,
    "keep_frac": 0.30,
    "step_cap": __KG_STEP_CAP__,
    "terminal_start": 712,
}


def _kg_blank_item():
    return dict(knee_quote_steps=0, sell_steps=0, trig_steps=0, sell_orders=0,
                requested_qty=0, posted_qty=0, truncated_orders=0,
                truncated_qty=0, dropped_orders=0, unparsed_kept=0,
                min_quote=None)


_KG_REPORT = dict(calls=0, changed_turns=0, steps_no_knee=0, window_out=0,
                  errors=0, truncated_orders=0, truncated_qty=0,
                  dropped_orders=0,
                  per_item={i: _kg_blank_item() for i in _KG_PARAMS["items"]})


def _kg_reset():
    _KG_REPORT.update(calls=0, changed_turns=0, steps_no_knee=0, window_out=0,
                      errors=0, truncated_orders=0, truncated_qty=0,
                      dropped_orders=0)
    for _item in _KG_PARAMS["items"]:
        _KG_REPORT["per_item"][_item] = _kg_blank_item()


def _kg_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _kg_get(obj, key, default=None):
    """观察字段读取（dict/Struct 双形态；异常→default）。"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    except Exception:
        return default


def _kg_post(observation, action):
    """价格膝点量门（同拍内）：三品挂量按 quote<0.7×base 截留至 min(沈存30%,X)。

    输入: 当前拍 observation+宿主动作 / 输出: 截留后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _KG_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return action
        try:
            step = int(_kg_get(observation, "step", 0) or 0)
        except Exception:
            step = 0
        if step >= int(_KG_PARAMS["terminal_start"]):
            _KG_REPORT["window_out"] += 1  # 终局清算窗 712-718 不截留
            return action
        prices = _kg_get(_kg_get(observation, "market", {}) or {},
                         "prices", {}) or {}
        shed = _kg_get(_kg_get(observation, "private", {}) or {},
                       "shed", {}) or {}
        try:
            avail = dict(_xd7_projected(observation, action))
        except Exception:
            avail = {k: int(v) for k, v in dict(shed).items()}
        trig = {}
        for item in _KG_PARAMS["items"]:
            quote = prices.get(item)
            if isinstance(quote, bool) or not isinstance(quote, (int, float)):
                continue
            base = float(_KG_PARAMS["base_px"].get(item, 0) or 0)
            if base <= 0:
                continue
            if float(quote) < float(_KG_PARAMS["knee_factor"]) * base:
                trig[item] = float(quote)
        if not trig:
            _KG_REPORT["steps_no_knee"] += 1
            return action
        allowance = {}
        for item, quote in trig.items():
            try:
                held = int(avail.get(item, 0) or 0)
            except Exception:
                held = 0
            cap = min(int(held * float(_KG_PARAMS["keep_frac"])),
                      int(_KG_PARAMS["step_cap"]))
            allowance[item] = max(0, cap)
            it = _KG_REPORT["per_item"].setdefault(item, _kg_blank_item())
            it["knee_quote_steps"] += 1
            if it["min_quote"] is None or quote < it["min_quote"]:
                it["min_quote"] = quote
        kept = []
        hit = set()
        changed = False
        for entry in market:
            is_sell = (isinstance(entry, (list, tuple)) and len(entry) >= 3
                       and entry[0] == "SELL")
            if not is_sell:
                kept.append(entry)  # 非 SELL 条目原位保留
                continue
            item = str(entry[1])
            qty = _kg_qty(entry[2])
            if qty is None or qty <= 0 or item not in trig:
                kept.append(entry)  # 挂量不确定/死单/膝点外→原样保留
                if item in trig and (qty is None or qty <= 0):
                    _KG_REPORT["per_item"][item]["unparsed_kept"] += 1
                continue
            hit.add(item)
            it = _KG_REPORT["per_item"][item]
            it["sell_orders"] += 1
            it["requested_qty"] += qty
            allow = allowance.get(item, 0)
            n = qty if qty <= allow else allow
            allowance[item] = allow - n
            if n < qty:
                changed = True
                it["truncated_orders"] += 1
                it["truncated_qty"] += qty - n
                _KG_REPORT["truncated_orders"] += 1
                _KG_REPORT["truncated_qty"] += qty - n
            if n <= 0:
                changed = True
                it["dropped_orders"] += 1
                _KG_REPORT["dropped_orders"] += 1
                continue
            it["posted_qty"] += n
            kept.append(entry if n == qty else ["SELL", item, n])
        for item in hit:
            it = _KG_REPORT["per_item"][item]
            it["sell_steps"] += 1
            if item in trig:
                it["trig_steps"] += 1
        if not changed:
            return action  # 同对象零足迹
        _KG_REPORT["changed_turns"] += 1
        return dict(action, market=kept)
    except Exception:
        _KG_REPORT["errors"] += 1
        return action  # 异常吞掉回退原动作（同对象零足迹）

# （入口 _kg_agent 由 build_knee.py 组装于块尾并做末函数归一）
