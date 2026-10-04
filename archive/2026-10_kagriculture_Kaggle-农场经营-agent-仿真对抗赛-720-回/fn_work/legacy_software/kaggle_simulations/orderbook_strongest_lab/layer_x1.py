# ---- 件 X1：d27 挂量墙卫生（纯同拍内整理） --------------------------------
# 形态：尾块注入件（构建时文本拼接进提交源，与基座同命名空间）；本文件为块体
# 片段，不含宿主捕获/入口（由 build_d27.py 组装）。仅用基座裸名
# （_xd7_projected 由共享段提供）；stdlib-only。
#
# 语义（任务口径 + tetsutani step950-953 同拍槽位卫生参考）：
# - 触发窗：step >= 624（窗外原样返回=同对象零足迹）；
# - qty<=0 SELL 死单清理（整条移除）；
# - 超库存死单清理：SELL 挂量按实存可卖 clamp（顺序口径：投射仓=同拍
#   PICKUP/DROP/PLACE 之后的仓 + 同拍更早的 BUY_PRODUCT/BUY_ANIMAL 入仓腿，
#   与基座 _clamp_sells 同口径；越库部分=死量清除）；
# - 同品碎单合并：并入最早同品 SELL 槽（量守恒，tetsutani 950/952 口径），
#   其后同品碎单移除；最早槽与碎单之间夹同品 BUY（洗仓腿）则不跨买合并
#   （保对倒卖腿的入仓资金，不挪到其入仓买腿之前）；
# - 非 SELL 条目（含 () 占位/空单/不确定挂量）原位保留；不改 farmer/hands；
# - 不动跨拍卖时（禁区红线 R23/R26：任何跨拍挪量不许——本层零跨拍操作）；
# - 无可改 → 返回原动作对象（同对象零足迹）。
_X1_REPORT = dict(calls=0, changed_turns=0, dropped_dead=0, clamped_orders=0,
                  clamped_qty=0, merged_fragments=0, merged_qty=0,
                  unparsed_kept=0, window_out=0, errors=0)


def _x1_reset():
    _X1_REPORT.update(calls=0, changed_turns=0, dropped_dead=0, clamped_orders=0,
                      clamped_qty=0, merged_fragments=0, merged_qty=0,
                      unparsed_kept=0, window_out=0, errors=0)


def _x1_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _x1_post(observation, action):
    """d27 挂量墙卫生（同拍内）：死单清理+超库存 clamp+同品碎单并最早槽。

    输入: 当前拍 observation+宿主动作 / 输出: 卫生后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _X1_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return action
        try:
            step = int((observation or {}).get("step", 0))
        except Exception:
            step = 0
        if step < 624:
            _X1_REPORT["window_out"] += 1
            return action
        avail = dict(_xd7_projected(observation, action))
        kept = []  # 元素=["other", entry] 或 ["sell", ["SELL", item, qty]]
        changed = False
        for entry in market:
            is_sell = (isinstance(entry, (list, tuple)) and len(entry) >= 3
                       and entry[0] == "SELL")
            if not is_sell:
                kept.append(["other", entry])
                if isinstance(entry, (list, tuple)) and len(entry) >= 3 \
                        and entry[0] in ("BUY_PRODUCT", "BUY_ANIMAL"):
                    q = _x1_qty(entry[2])
                    if q is not None and q > 0:
                        avail[entry[1]] = avail.get(entry[1], 0) + q
                continue
            item = entry[1]
            qty = _x1_qty(entry[2])
            if qty is None:
                kept.append(["other", entry])  # 挂量不确定→原样保留
                _X1_REPORT["unparsed_kept"] += 1
                continue
            if qty <= 0:
                changed = True  # qty<=0 死单清理
                _X1_REPORT["dropped_dead"] += 1
                continue
            have = avail.get(item, 0)
            n = qty if qty <= have else have
            if n < qty:
                changed = True  # 超库存死量清除
                _X1_REPORT["clamped_orders"] += 1
                _X1_REPORT["clamped_qty"] += qty - n
            if n <= 0:
                changed = True
                _X1_REPORT["dropped_dead"] += 1
                continue
            avail[item] = have - n
            target = -1
            for i, rec in enumerate(kept):
                if rec[0] == "sell" and rec[1][1] == item:
                    target = i
                    break
            if target >= 0:
                cross_buy = any(
                    rec[0] == "other" and isinstance(rec[1], (list, tuple))
                    and len(rec[1]) >= 3 and rec[1][0] in ("BUY_PRODUCT",
                                                           "BUY_ANIMAL")
                    and rec[1][1] == item for rec in kept[target + 1:])
                if not cross_buy:
                    kept[target][1] = ["SELL", item,
                                       _x1_qty(kept[target][1][2]) + n]
                    changed = True  # 同品碎单并入最早同品槽（量守恒）
                    _X1_REPORT["merged_fragments"] += 1
                    _X1_REPORT["merged_qty"] += n
                    continue
            if n == qty:
                kept.append(["sell", entry])  # 无可改→保留原条目对象
            else:
                kept.append(["sell", ["SELL", item, n]])
        out = [rec[1] for rec in kept][:10]  # 槽位上限 10（本层只减不增）
        if not changed:
            return action  # 同对象零足迹
        _X1_REPORT["changed_turns"] += 1
        return dict(action, market=out)
    except Exception:
        _X1_REPORT["errors"] += 1
        return action  # 异常吞掉回退原动作（同对象零足迹）
