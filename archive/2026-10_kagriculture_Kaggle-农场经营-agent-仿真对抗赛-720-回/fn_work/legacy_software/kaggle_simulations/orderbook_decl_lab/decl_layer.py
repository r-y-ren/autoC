# ---- 件 DL：申报量-持货匹配（decl 层） -------------------------------------
# 形态：尾块注入件（构建时文本拼接进 oc_c3 提交源，与宿主同命名空间）；本文件为
# 块体片段，不含宿主捕获/入口（由 build_decl.py 组装）。仅用基座裸名
# （_xd7_projected 由 oc_c3 共享段提供，失败回退裸 shed）；stdlib-only。
#
# 语义（任务 decl 层口径）：
# - 对本步 SELL 单：qty = min(申报, 投射可卖沈存)——只申报自己真有的货，
#   消除 over-declaration 的部分成交/废单（引擎逐单位交割、断货即 abort 的
#   口径下，多申报部分必然烂在单里）；
# - 可卖沈存=基座 _clamp_sells 同序口径：_xd7_projected（同拍单位动作后、
#   市场成交前的仓）起底 + 同拍更早 BUY_PRODUCT/BUY_ANIMAL 入仓腿（上界，
#   引擎自限现金/仓容），逐单顺序扣减（同品多单合计不超可交付量）；
# - 变体 __DL_MODE__=0（decl）：无条件按上裁；
#   变体 __DL_MODE__=1（decl+补链）：该品缺口若未来有补货（在途手持/在耕
#   作物/产线动物，观测保守口径）→ 该品本步不动（保守）；无补货才裁；
# - 零跨拍、只裁申报不动时点、不改单集合与槽位（裁到 0 也留 ["SELL",item,0]
#   占槽——基座 _clamp_sells 同理：移空单会改变后序 lockstep 撮合列对齐）；
#   磁带 blob 零触碰；非 SELL 条目/挂量不确定条目原样保留；无可改→返回原
#   动作对象（同对象零足迹）；异常吞掉回退原动作（同对象零足迹）。
_DL_PARAMS = {
    "mode": __DL_MODE__,  # 0=decl；1=decl+补链
    "buy_legs": ("BUY_PRODUCT", "BUY_ANIMAL"),
}


def _dl_blank_item():
    return dict(sell_orders=0, requested_qty=0, posted_qty=0, truncated_orders=0,
                truncated_qty=0, zeroed_orders=0, unparsed_kept=0,
                restock_skipped_orders=0, restock_skipped_qty=0)


_DL_REPORT = dict(calls=0, changed_turns=0, errors=0, sell_orders=0,
                  requested_qty=0, posted_qty=0, truncated_orders=0,
                  truncated_qty=0, zeroed_orders=0, unparsed_kept=0,
                  restock_skipped_orders=0, restock_skipped_qty=0,
                  per_item={})


def _dl_reset():
    _DL_REPORT.update(calls=0, changed_turns=0, errors=0, sell_orders=0,
                      requested_qty=0, posted_qty=0, truncated_orders=0,
                      truncated_qty=0, zeroed_orders=0, unparsed_kept=0,
                      restock_skipped_orders=0, restock_skipped_qty=0)
    _DL_REPORT["per_item"] = {}


def _dl_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _dl_get(obj, key, default=None):
    """观察字段读取（dict/Struct 双形态；异常→default）。"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    except Exception:
        return default


_DL_ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def _dl_restock_items(observation):
    """补链观测：未来补货源→品集合（保守口径，宁多勿漏）。

    源=①在途手持（private.inventories 任一手 qty>0，后续 DROP/PLACE 入仓）
    ②在耕作物（board 上 PLANT 该品，后续 HARVEST→DROP）
    ③产线动物（board 上 GOOSE/COW/SHEEP → EGG/MILK/WOOL + 动物每日
      fertilizer_available → FERTILIZER）。只读观察，不碰磁带 blob。
    """
    out = set()
    try:
        private = _dl_get(observation, "private", {}) or {}
        for inv in (_dl_get(private, "inventories", []) or []):
            for item, q in dict(inv or {}).items():
                try:
                    if int(q) > 0:
                        out.add(str(item))
                except Exception:
                    continue
        try:
            player = int(_dl_get(observation, "player", 0) or 0)
        except Exception:
            player = 0
        farms = _dl_get(observation, "farms", []) or []
        farm = farms[player] if 0 <= player < len(farms) else {}
        for row in (_dl_get(farm, "tiles", []) or []):
            for tile in (row or []):
                if not isinstance(tile, dict):
                    continue
                if _dl_get(tile, "kind") == "PLANT":
                    crop = _dl_get(tile, "crop")
                    if crop:
                        out.add(str(crop))
                elif _dl_get(tile, "animal") is not None:
                    prod = _DL_ANIMAL_PRODUCT.get(str(_dl_get(tile, "animal")))
                    if prod:
                        out.add(prod)
                    out.add("FERTILIZER")
    except Exception:
        pass
    return out


def _dl_post(observation, action):
    """申报量-持货匹配（同拍内）：本步 SELL 挂量裁到 min(申报, 可卖沈存)。

    输入: 当前拍 observation+宿主动作 / 输出: 裁量后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _DL_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return action
        restock = set()
        if int(_DL_PARAMS["mode"]) == 1:
            restock = _dl_restock_items(observation)
        try:
            avail = dict(_xd7_projected(observation, action))
        except Exception:
            shed = _dl_get(_dl_get(observation, "private", {}) or {},
                           "shed", {}) or {}
            avail = {k: int(v) for k, v in dict(shed).items()}
        kept = []
        changed = False
        for entry in market:
            is_sell = (isinstance(entry, (list, tuple)) and len(entry) >= 3
                       and entry[0] == "SELL")
            if not is_sell:
                kept.append(entry)  # 非 SELL 条目原位保留
                if isinstance(entry, (list, tuple)) and len(entry) >= 3 \
                        and entry[0] in _DL_PARAMS["buy_legs"]:
                    q = _dl_qty(entry[2])
                    if q is not None and q > 0:
                        item = str(entry[1])
                        avail[item] = avail.get(item, 0) + q  # 同拍更早入仓腿
                continue
            item = str(entry[1])
            qty = _dl_qty(entry[2])
            it = _DL_REPORT["per_item"].setdefault(item, _dl_blank_item())
            if qty is None or qty <= 0:
                kept.append(entry)  # 挂量不确定/死单→原样保留
                _DL_REPORT["unparsed_kept"] += 1
                it["unparsed_kept"] += 1
                continue
            _DL_REPORT["sell_orders"] += 1
            _DL_REPORT["requested_qty"] += qty
            it["sell_orders"] += 1
            it["requested_qty"] += qty
            if item in restock:
                _DL_REPORT["restock_skipped_orders"] += 1
                _DL_REPORT["restock_skipped_qty"] += qty
                it["restock_skipped_orders"] += 1
                it["restock_skipped_qty"] += qty
                kept.append(entry)  # 补链保守：有未来补货→不动
                have = avail.get(item, 0)
                avail[item] = have - min(qty, max(0, have))
                continue
            have = avail.get(item, 0)
            n = qty if qty <= have else have
            avail[item] = have - min(qty, max(0, have))
            if n < qty:
                changed = True
                _DL_REPORT["truncated_orders"] += 1
                _DL_REPORT["truncated_qty"] += qty - n
                it["truncated_orders"] += 1
                it["truncated_qty"] += qty - n
            _DL_REPORT["posted_qty"] += n
            it["posted_qty"] += n
            if n <= 0:
                _DL_REPORT["zeroed_orders"] += 1
                it["zeroed_orders"] += 1
                kept.append(["SELL", item, 0])  # 留槽不移（lockstep 列对齐）
                continue
            kept.append(entry if n == qty else ["SELL", item, n])
        if not changed:
            return action  # 同对象零足迹
        _DL_REPORT["changed_turns"] += 1
        return dict(action, market=kept)
    except Exception:
        _DL_REPORT["errors"] += 1
        return action  # 异常吞掉回退原动作（同对象零足迹）

# （入口 _dl_agent 由 build_decl.py 组装于块尾并做末函数归一）
