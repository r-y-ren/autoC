"""迁移登记——run_submission_agent · observe_opponent_state（B12，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/src/observer.py（旧树冻结，零字节变更）
源 sha256: dad268e123d47ba34f283f080ae29e0a8f9a77cd08146cccb8afd451568b06d1
剥离清单（R10 死码不迁）: 无——observer.py 无 R10 清单内符号；_opp_note_fills 按职责保留
  （仅离线语义：replay 工具在过渡校验后注入成交回执，线上观测不暴露）。本件零删改。
形态: 本文件 = 旧模块的迁移副本——下方源码可被 exec 进共享命名空间（装载序与
  拓扑位次见 load_agent_modules，对应 main.py _MODULE_ORDER 的 observer 位）；不引入
  import 式重排（会改变名字解析语义）。除本登记头与登记过的删改外源码逐字复制；
  依赖的共享命名空间符号由先序模块提供（exec 链语义）。
上游: R1, R10（fn_docs/responsibility.md 功能块 run_submission_agent）
"""

# ===========================================================================
# 【中文·模块导览】src/observer.py —— 被动观测通道（OBS v2 的落位壳）
# ---------------------------------------------------------------------------
# v10.9 职责：四个纯读函数——_farm_scan（公开农场经济扫描，模式门控与
#   对手画像的输入）、_count_crops/_species_counts（产能清点）、
#   _market_flow+_MARKET_MEM（日间价格移动反解净流量 EMA——注意这是
#   双方产销+城镇吸收的混合项，归因不出对手单方）。
# 新架构落位：opp_supply_observer_design v2 的宿主模块。
# 文档符合性审查：
#   ✗ 待办（OBS-1..5）——四通道估计器（Ch0 obs.market.inventory 直读/
#     Ch1 曲线反解校验/Ch2 钱账对账/Ch3 tile 整数记账）全部未实现；
#     est_* getter 与 _OPP_OBSERVER 旁路（fail-open）未建；
#   ○ 现有四函数是 Ch2/Ch3 的地基（OBS v2 定位"纯搬移，旁路化是
#     OBS-1 的事"）；仓库估计 ∫(产量−销量) 的整账能力尚无。
# 下游消费者（文档裁定，全部排队在 OBS 之后）：branch P1 对手开局
#   分类器、market 的 R_opp 干扰触发器与 _project_price 对手项、
#   P4 抢跑三档出清、时序战第 4 层对手上市日历（Ch3 轻量前置）。
# ===========================================================================


# 【中文】公开农场经济扫描：象限数、草莓/小麦格数（含草莓种植日历）、
# 按物种的在栏牲畜、雇工数、现金。obs.farms 是共享公开状态（只有仓库/
# 背包是私有的），扫描对手农场属于合法观察——这是模式门控的输入。
def _farm_scan(farm):
    """Public-farm economy scan: quadrants, strawberry/wheat tiles (with
    the strawberry planting calendar), placed herd by species, hands,
    money.  obs.farms is shared state (only sheds/inventories are
    private), so scanning the opponent's farm is legal observation."""
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    straw = wheat = herd = 0
    straw_days = []
    species = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop == "STRAWBERRY":
                    straw += 1
                    straw_days.append(_get(tile, "planted_day", 0))
                elif crop == "WHEAT":
                    wheat += 1
            elif "animal" in tile:
                herd += 1
                animal = _get(tile, "animal", "")
                if animal in species:
                    species[animal] += 1
    return {"quads": quads, "straw": straw, "wheat": wheat, "herd": herd,
            "straw_days": straw_days, "cows": species["COW"],
            "sheep": species["SHEEP"], "geese": species["GOOSE"],
            "hands": len(_get(farm, "hands", []) or []),
            "money": _get(farm, "money", 0.0)}


def _count_crops(farm):
    """Alive PLANT tiles per crop (for seed deficits)."""
    counts = {crop: 0 for crop in CROPS}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop in counts:
                    counts[crop] += 1
    return counts


def _species_counts(farm, private, herd_total):
    """Placed + shed + carried animals per species.  Herd totals handed in
    by abstract callers that carry no observable composition are attributed
    to the primary species (sheep) -- real observations never need this.
    """
    counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and "animal" in tile:
                animal = _get(tile, "animal", "")
                if animal in counts:
                    counts[animal] += 1
    shed = _get(private, "shed", {}) or {}
    for animal in counts:
        counts[animal] += _get(shed, animal, 0)
        for inv in (_get(private, "inventories", []) or []):
            if inv:
                counts[animal] += _get(inv, animal, 0)
    extra = int(herd_total) - sum(counts.values())
    if extra > 0:
        counts["SHEEP"] += extra
    return counts


# 【中文】市场记忆与投影：_market_flow 把逐日价格移动经曲线反解成每件
# 商品的净库存流 EMA（单位/天，正值=过剩在积累——已同时包含我方与对
# 手的产销量和城镇吸收）；_project_price 给出解析的 E[R_future] =
# 在偏移量上再推 flow×horizon 天后的曲线价。两者是止损判据"投影价低
# 于现价 → 曲线在死"的来源。
# per-player market memory: yesterday's prices -> observed net flow EMA
_MARKET_MEM = {}


def _market_flow(player, day, prices):
    """Net inventory flow per item (units/day).  Positive = glut building.

    OBS-2 seamless switch: when the observer's day account has run for
    this player-day it publishes the Ch0-EXACT flow (ΔMarketInv − our_net
    + absorb, integers) here under the same shape, and that is what every
    consumer (_project_price, curve gate, sell planner, interference)
    reads.  Legacy path (price inversion EMA, now the Ch1 cross-check
    signal) remains as the fallback when the observer is disabled or has
    not accounted the day yet.
    """
    st = _MARKET_MEM.get(player)
    if not OBSERVER_ENABLED:
        if st is not None and st.get("source") == "ch0":
            _MARKET_MEM.pop(player, None)
            st = None
    if st is not None and st.get("day") == day \
            and st.get("source") == "ch0":
        return dict(st.get("flow", {}))
    if st is None or st.get("day", -1) >= day:
        _MARKET_MEM[player] = {"day": day, "prices": dict(prices),
                               "flow": {}}
        return {}
    prev = st.get("prices", {})
    flow = {}
    for item, p_now in prices.items():
        if item not in MARKET_PARAMS_EMB or item not in prev:
            continue
        delta = (_offset_from_price(item, p_now)
                 - _offset_from_price(item, prev[item]))
        if delta == 0:
            flow[item] = 0.0
        else:
            ema = st.get("flow", {}).get(item, 0.0)
            flow[item] = 0.55 * delta + 0.45 * ema
    _MARKET_MEM[player] = {"day": day, "prices": dict(prices), "flow": flow}
    return flow


# ===========================================================================
# 【中文】OBS-1..3 四通道对手供给观测器（opp_supply_observer_design v2，
# 2026-09-02 W1 落地 + W2 完善波）
# ---------------------------------------------------------------------------
# 工程契约（文档 §3，W2 补齐项标注）：
#   * 纯旁路 _OPP_OBSERVER——fail-open，任何异常整体吞掉并置 conf=0；
#     [W2] 独立开关 OBSERVER_ENABLED / reset_observer / observer_snapshot
#     （照 telemetry 模式：OB-3.1 全席）；
#   * 日账时序：每日首个动作回合做快照+差分+积分；
#   * 只读接口一律 est_ 前缀（M-H NO-GO 边界：replay 私有字段仅离线校验器
#     可读——scripts/observer_v0_validator.py，在线只消费合法公开字段）；
#   * Ch0 obs.market.inventory 直读为主通道；[W2] Ch0 精确流写入 _MARKET_MEM
#     （OBS-2：_market_flow 无感切换，价格反解降级为 Ch1 交叉校验+残差监控
#     last_resid，持续非零=引擎/镜像失配或地板价饱和告警）；
#   * [W2] E1/E6 双口径 our_net：地板价（$1）卖出只动钱不动库存——
#     sold_floor 单列，Ch0 只记入库存的贡献件数；
#   * Ch2 钱账：[W2] 从"只记 Δmoney"升格为支出分解（雇工 fib/买地 Δ象限×
#     价格/新放畜 tile×cost/新种 tile×seed 上界/Ch0 负流×均价）→
#     sell_revenue 估计，供与 Ch0 卖出件数交叉验证（R_opp 误差界定基）；
#   * Ch3 tile 记账：收割/投喂公开整数账 → opp_held 积分（E2 棚溢出高估、
#     E5 种子跨日为有界误差，conf 联动）；[W2] prod_horizon 缓存 →
#     est_opp_supply_horizon 真实现（held+产期表未来产出，OB-3.4）。
# 消费方（文档 §4）：P4 三档出清、争议线零囤货连续化、_project_price 对手项
#   （经 Ch0 流）、干扰触发器 R_opp——全部经 est_* getter / _market_flow，
#   不直接读状态；V2 消费以 V0 门禁（scripts/observer_v0_validator.py）+
#   线上 A/B 为裁决轴。
# ===========================================================================
OBSERVER_ENABLED = True       # OB-3.1 独立开关（False=旁路全静默，flow 回退 EMA）
_OPP_OBSERVER = {}


def reset_observer(player=None):
    """Clear observer and market-flow state for one or all players."""
    if player is None:
        _OPP_OBSERVER.clear()
        _MARKET_MEM.clear()
    else:
        _OPP_OBSERVER.pop(player, None)
        _MARKET_MEM.pop(player, None)


def observer_snapshot(player=None):
    """OB-3.1: deep-copied observer state for diagnostics/telemetry."""
    import copy as _copy
    if player is None:
        return _copy.deepcopy(_OPP_OBSERVER)
    return _copy.deepcopy(_OPP_OBSERVER.get(player))


def _opp_observer_state(player, day, hour):
    """Get-or-create the per-player observer state; clock-back = new episode."""
    st = _OPP_OBSERVER.get(player)
    if st is None or day < st.get("day", day) or (
            day == st.get("day", day) and hour < st.get("hour", hour)):
        _MARKET_MEM.pop(player, None)
        st = {"day": day, "hour": hour, "accounted_day": -1,
              "snapshot_day": None, "snapshot_hour": None,
              "inv_prev": {}, "prices_prev": {}, "money_prev": None,
              "tile_yield_prev": {}, "held": {}, "flow_hist": {},
              "sold_today": {}, "bought_today": {}, "sold_floor": {},
              "requested_sell": {}, "requested_buy": {},
              "requested_floor_sell": {}, "filled_sell": {},
              "filled_buy": {}, "filled_floor_sell": {},
              "fill_known": False, "fill_incomplete": False,
              "fill_diagnostics": [],
              "order_basis": "requested", "account_window": {},
              "ch0_components": {}, "event_ledger": {},
              "harvest_today": {}, "unknown_loss_today": {},
              "eod_action_unknown": {},
              "held_inconsistency": {}, "conf": {}, "last_resid": {},
              "residual_hist": {}, "residual_streak": {},
              "confidence_reasons": {},
              "prod_horizon": {}, "quads_prev": None,
              "animals_prev": None}
        _OPP_OBSERVER[player] = st
    st["day"] = day
    st["hour"] = hour
    return st


def _opp_note_orders(player, day, hour, orders, prices=None):
    """Bypass hook (fail-open): record OUR accepted SELL/BUY_PRODUCT units.

    E1/E6 dual ledger: only quoted-above-$1 SELLs add market inventory;
    floor-price sells move money but NOT inventory, so they are bucketed
    separately (sold_floor) and excluded from the Ch0 inventory equation.
    """
    if not OBSERVER_ENABLED:
        return
    try:
        st = _opp_observer_state(player, day, hour)
        for o in orders or []:
            if not isinstance(o, list) or len(o) < 3 or not o[0]:
                continue
            n = o[2] if isinstance(o[2], (int, float)) else 0
            if o[0] == "SELL" and o[1] in BASE_PRICE:
                price = _get(prices or {}, o[1], 99)
                if price <= PRICE_FLOOR_EMB:
                    st.setdefault("requested_floor_sell", {})[o[1]] = \
                        st.get("requested_floor_sell", {}).get(o[1], 0) + n
                    st.setdefault("sold_floor", {})[o[1]] = \
                        st.get("sold_floor", {}).get(o[1], 0) + n
                else:
                    st.setdefault("requested_sell", {})[o[1]] = \
                        st.get("requested_sell", {}).get(o[1], 0) + n
                    st.setdefault("sold_today", {})[o[1]] = \
                        st.get("sold_today", {}).get(o[1], 0) + n
            elif o[0] == "BUY_PRODUCT" and o[1] in BASE_PRICE:
                st.setdefault("requested_buy", {})[o[1]] = \
                    st.get("requested_buy", {}).get(o[1], 0) + n
                st.setdefault("bought_today", {})[o[1]] = \
                    st.get("bought_today", {}).get(o[1], 0) + n
    except Exception:
        return


def _opp_note_fills(player, day, hour, fills, complete=True):
    """Offline-only hook for reconstructed engine fills.

    Raw Kaggle observations do not expose fill results.  Replay tooling may
    inject shadow-attributed fills only after it has validated the transition.
    """
    if not OBSERVER_ENABLED:
        return
    try:
        st = _opp_observer_state(player, day, hour)
        if not complete:
            st["fill_incomplete"] = True
            st["fill_known"] = False
            return
        for row in fills or []:
            if not isinstance(row, dict):
                continue
            op = row.get("type")
            item = row.get("item")
            n = row.get("filled", 0)
            if item not in BASE_PRICE or not isinstance(n, (int, float)):
                continue
            if op == "SELL":
                first_price = row.get("first_price")
                is_floor = row.get("floor") or (
                    isinstance(first_price, (int, float)) and
                    first_price <= PRICE_FLOOR_EMB)
                key = "filled_floor_sell" if is_floor else "filled_sell"
                st[key][item] = st[key].get(item, 0) + n
            elif op == "BUY_PRODUCT":
                st["filled_buy"][item] = st["filled_buy"].get(item, 0) + n
            if row.get("abort") or n != row.get("requested", n):
                st["fill_diagnostics"].append({
                    "type": op, "item": item,
                    "requested": row.get("requested"), "filled": n,
                    "abort": row.get("abort")})
        st["fill_known"] = not st.get("fill_incomplete", False)
    except Exception:
        return


def _opp_tile_yields(farm):
    """Per-item yield_units totals over a farm's tiles (Ch3 snapshot)."""
    out = {item: 0 for item in BASE_PRICE}
    fed = 0
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            y = _get(tile, "yield_units", 0) or 0
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop in out:
                    out[crop] += y
            elif "animal" in tile:
                prod = _get(ANIMALS.get(_get(tile, "animal", ""), {}),
                            "product", "")
                if prod in out:
                    out[prod] += y
                if _get(tile, "fed_today", False):
                    fed += 1
    out["__fed__"] = fed
    return out


def _opp_tile_state(farm):
    """Public production state keyed by tile coordinate."""
    out = {}
    for y, row in enumerate(_get(farm, "tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                item = _get(tile, "crop", "")
                identity = ("PLANT", item, _get(tile, "planted_day", None))
            elif "animal" in tile:
                animal = _get(tile, "animal", "")
                item = _get(ANIMALS.get(animal, {}), "product", "")
                identity = ("ANIMAL", animal,
                            _get(tile, "placed_day", None))
            else:
                continue
            if item in BASE_PRICE:
                out[(x, y)] = {
                    "item": item, "identity": identity,
                    "kind": identity[0], "crop": item if identity[0] == "PLANT" else None,
                    "yield": int(_get(tile, "yield_units", 0) or 0),
                    "watered": bool(_get(tile, "watered_today", False)),
                    "fed": bool(_get(tile, "fed_today", False)),
                    "cared": bool(_get(tile, "cared_today", False)),
                    "unwatered": int(_get(tile, "consecutive_unwatered", 0) or 0),
                    "max_lifespan_step": _get(tile, "max_lifespan_step", -1),
                }
    return out


def _opp_harvest_events(previous, current, production, step=None, eod=False):
    """Infer public harvest events between consecutive observations."""
    harvested = {item: 0 for item in BASE_PRICE}
    unknown_loss = {item: 0 for item in BASE_PRICE}
    for coord, before in (previous or {}).items():
        after = (current or {}).get(coord)
        produced = (production or {}).get(coord, 0)
        expected = before["yield"] + produced
        same_identity = after is not None and \
            after.get("identity") == before["identity"]
        expired = isinstance(step, (int, float)) and \
            before.get("max_lifespan_step", -1) >= 0 and \
            step >= before.get("max_lifespan_step", -1)
        decayed = expired and before.get("kind") == "PLANT" and \
            not CROPS.get(before.get("crop"), {}).get("ongoing", False)
        if same_identity:
            delta = max(0, expected - after["yield"])
            if decayed and after.get("yield", 0) < before.get("yield", 0):
                unknown_loss[before["item"]] += delta
            else:
                harvested[before["item"]] += delta
            continue
        disappeared = max(0, before["yield"])
        # A changed identity (including DIG/replant) is not evidence of
        # harvest.  Only an empty target can be a one-shot harvest candidate.
        one_shot = before.get("kind") == "PLANT" and \
            not CROPS.get(before.get("crop"), {}).get("ongoing", False)
        care_lapse = eod and before.get("unwatered", 0) >= 1 and \
            not before.get("watered", False)
        if after is None and one_shot and disappeared > 0 and \
                not expired and not care_lapse:
            harvested[before["item"]] += disappeared
        elif expected > 0:
            unknown_loss[before["item"]] += expected
    return harvested, unknown_loss


def _opp_production_night(farm, day, by_tile=False):
    """Production added by the end-of-day refresh after `day`."""
    out = {item: 0 for item in BASE_PRICE}
    tile_out = {}
    for y, row in enumerate(_get(farm, "tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                cd = CROPS.get(crop)
                if not cd or not cd["ongoing"]:
                    continue
                planted = _get(tile, "planted_day", day)
                interval = max(1, cd["interval"])
                dsf = (day + 1) - planted - cd["first_yield_day"]
                production_count = dsf // interval + 1 if dsf >= 0 else 0
                if dsf >= 0 and dsf % interval == 0 \
                        and production_count <= cd["max_yield"]:
                    fertilized = _get(tile, "watered_today", False) and \
                        _get(tile, "fertilized_until_day", -1) >= day
                    room = max(0, cd["max_yield"] -
                               int(_get(tile, "yield_units", 0) or 0))
                    if crop in out:
                        produced = min(room, 2 if fertilized else 1)
                        out[crop] += produced
                        tile_out[(x, y)] = produced
            elif "animal" in tile:
                a = ANIMALS.get(_get(tile, "animal", ""), {})
                if not a:
                    continue
                placed = _get(tile, "placed_day", day)
                dsf = (day + 1) - placed - a["first_yield_day"]
                if dsf >= 0 and dsf % a["interval"] == 0:
                    fed = bool(_get(tile, "fed_today", False))
                    bonus = int(_get(tile, "pending_care_bonus", 0) or 0) \
                        if fed else 0
                    room = max(0, a["max_held"] -
                               int(_get(tile, "yield_units", 0) or 0))
                    prod = a.get("product", "")
                    if prod in out:
                        produced = min(room, 1 + bonus)
                        out[prod] += produced
                        tile_out[(x, y)] = produced
    return tile_out if by_tile else out


def _opp_observer_update(obs, own_private):
    """Day-account pass (fail-open).  Once per day, first action turn."""
    if not OBSERVER_ENABLED:
        return
    try:
        player = _get(obs, "player", 0)
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        st = _opp_observer_state(player, day, hour)
        if st["accounted_day"] >= day:
            farms = _get(obs, "farms", []) or []
            opp = next((f for i, f in enumerate(farms) if i != player), None)
            if opp is not None:
                tiles = _opp_tile_state(opp)
                harvested, unknown = _opp_harvest_events(
                    st.get("_opp_tiles", {}), tiles, {},
                    step=_get(obs, "step", None), eod=False)
                for item, amount in harvested.items():
                    if amount:
                        st.setdefault("harvest_today", {})[item] = \
                            st.get("harvest_today", {}).get(item, 0) + amount
                for item, amount in unknown.items():
                    if amount:
                        st.setdefault("unknown_loss_today", {})[item] = \
                            st.get("unknown_loss_today", {}).get(item, 0) + amount
                yields = _opp_tile_yields(opp)
                st["_opp_yields"] = yields
                st["_opp_fed"] = yields.get("__fed__", 0)
                st["_opp_tiles"] = tiles
                if hour >= 23:
                    for coord, tile in tiles.items():
                        if tile.get("kind") == "ANIMAL" and \
                                (not tile.get("fed", False) or
                                 not tile.get("cared", False)):
                            st["eod_action_unknown"][tile["item"]] = \
                                "last_turn_care_or_feed_unobserved"
                st["_opp_prod"] = _opp_production_night(opp, day)
                st["_opp_prod_tiles"] = _opp_production_night(
                    opp, day, by_tile=True)
                st["last_public_hour"] = hour
            return
        farms = _get(obs, "farms", []) or []
        opp = None
        for i, f in enumerate(farms):
            if i != player:
                opp = f
                break
        market = _get(obs, "market", {}) or {}
        inv = dict(_get(market, "inventory", {}) or {})
        prices_now = dict(_get(market, "prices", {}) or {})
        yields_now = _opp_tile_yields(opp) if opp is not None else \
            {item: 0 for item in BASE_PRICE}
        tiles_now = _opp_tile_state(opp) if opp is not None else {}
        harvest_boundary, unknown_boundary = _opp_harvest_events(
            st.get("_opp_tiles", {}), tiles_now,
            st.get("_opp_prod_tiles", {}), step=_get(obs, "step", None),
            eod=True)
        harvest_by_item = dict(st.get("harvest_today", {}))
        unknown_loss_by_item = dict(st.get("unknown_loss_today", {}))
        for item, amount in harvest_boundary.items():
            harvest_by_item[item] = harvest_by_item.get(item, 0) + amount
        for item, amount in unknown_boundary.items():
            unknown_loss_by_item[item] = \
                unknown_loss_by_item.get(item, 0) + amount
        shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        # E3 calibration: the ΔInv window covers YESTERDAY (prev h0 -> now),
        # and shops unlock at EOD -- so the window's absorption must use the
        # shop set as of YESTERDAY's snapshot, not today's (unlock-day ±6/±12
        # mis-account, V0-diagnosed).  NB: shops_prev == [] is a VALID
        # yesterday-set -- an empty list must not fall through to today's.
        shops_prev = st.get("shops_prev")
        absorb = _town_daily_demand(
            shops_prev if shops_prev is not None else shops)
        prev_inv = st["inv_prev"]
        fill_known = bool(st.get("fill_known"))
        sold = st.get("filled_sell", {}) if fill_known else \
            (st.get("requested_sell") or st.get("sold_today", {}))
        bought = st.get("filled_buy", {}) if fill_known else \
            (st.get("requested_buy") or st.get("bought_today", {}))
        sold_floor = st.get("filled_floor_sell", {}) if fill_known else \
            (st.get("requested_floor_sell") or st.get("sold_floor", {}))
        st["order_basis"] = "filled" if fill_known else "requested"
        first_pass = st.get("initialized") is not True
        ch0_flow = {}
        ch0_components = {}
        event_ledger = {}
        ch1_implied = {}
        for item in BASE_PRICE:
            # ---- Ch0: exact integer flow (direct inventory read) ----
            opp_net = None
            if item in inv and item in prev_inv:
                inventory_delta = inv[item] - prev_inv[item]
                our_net = sold.get(item, 0) - bought.get(item, 0)
                absorbed = absorb.get(item, 0)
                opp_net = inventory_delta - our_net + absorbed
                ch0_flow[item] = float(opp_net)
                ch0_components[item] = {
                    "inventory_delta": inventory_delta,
                    "our_sell": sold.get(item, 0),
                    "our_buy": bought.get(item, 0),
                    "town_absorb": absorbed,
                    "opponent_net": float(opp_net),
                    "order_basis": st["order_basis"],
                }
            # ---- Ch1 cross-check: price-inversion implied delta ----
            if item in MARKET_PARAMS_EMB and item in prices_now \
                    and item in st.get("prices_prev", {}):
                ch1_implied[item] = \
                    _offset_from_price(item, prices_now[item]) - \
                    _offset_from_price(item, st["prices_prev"][item])
            # ---- Ch3: harvest ledger from public tiles ----
            y_now = yields_now.get(item, 0)
            y_prev = st["tile_yield_prev"].get(item, 0)
            prod_est = st.get("_opp_prod", {}).get(item, 0)
            raw_harvest = y_prev + prod_est - y_now
            aggregate_harvest = max(0, raw_harvest)
            if st.get("_opp_tiles"):
                harvested = harvest_by_item.get(item, 0)
                unknown_loss = unknown_loss_by_item.get(item, 0)
            else:
                harvested = aggregate_harvest
                unknown_loss = 0
            sold_units = max(0, opp_net) if opp_net is not None else 0
            bought_units = max(0, -opp_net) if opp_net is not None else 0
            fed_units = st.get("_opp_fed", 0) if item == "WHEAT" else 0
            if item == "FERTILIZER":
                held_delta = -sold_units  # gather side unobservable
                st["conf"][item] = 0.5
            elif opp_net is not None:
                held_delta = harvested - opp_net - fed_units
            else:
                held_delta = harvested - fed_units
            if item in st.get("eod_action_unknown", {}):
                st["confidence_reasons"][item] = \
                    st["eod_action_unknown"][item]
                st["conf"][item] = min(st["conf"].get(item, 1.0), 0.4)
            prior_held = st["held"].get(item, 0)
            raw_held = prior_held + held_delta
            if raw_harvest < 0 or raw_held < 0:
                st["held_inconsistency"][item] = \
                    st["held_inconsistency"].get(item, 0) + 1
            st["held"][item] = max(0, raw_held)
            event_ledger[item] = {
                "yield_prev": y_prev, "yield_now": y_now,
                "production_est": prod_est,
                "harvest_raw": raw_harvest,
                "harvest_aggregate": aggregate_harvest,
                "harvest_est": harvested, "unknown_loss": unknown_loss,
                "sold_est": sold_units, "bought_est": bought_units,
                "fed_est": fed_units, "held_before": prior_held,
                "held_delta": held_delta, "held_after": st["held"][item],
            }
            if opp_net is not None and not first_pass:
                hist = st["flow_hist"].setdefault(item, [])
                hist.append(opp_net)
                st["conf"].setdefault(item, 1.0)
        # ---- OBS-2: publish the Ch0 flow under _market_flow's shape ----
        # (seamless switch: every consumer reads the same {"item": units}
        # dict; the legacy EMA remains the fallback when the observer is
        # off or the day account has not run yet).  The FIRST pass is a
        # warm-up: snapshots only, no flow/held output (the day-0 window's
        # center-draw phase is not alignable -- E4, V0-diagnosed +1/item).
        if first_pass:
            st["held"] = {}
        elif ch0_flow or prev_inv:
            _MARKET_MEM[player] = {"day": day, "prices": dict(prices_now),
                                   "flow": ch0_flow, "source": "ch0"}
        # Ch1 cross-checks the price curve against raw market inventory
        # movement; opponent_net additionally removes our flow and town demand.
        st["last_resid"] = {
            item: round(ch0_components[item]["inventory_delta"] -
                        ch1_implied[item], 2)
            for item in ch0_components if item in ch1_implied}
        qualified_residual = not first_pass and not bought and not sold_floor
        if qualified_residual:
            for item, residual in st["last_resid"].items():
                hist = st["residual_hist"].setdefault(item, [])
                hist.append(abs(residual))
                del hist[:-7]
                if abs(residual) > 1.0:
                    streak = st["residual_streak"].get(item, 0) + 1
                    st["residual_streak"][item] = streak
                    if streak >= 2:
                        raw_conf = st["conf"].get(item, 1.0)
                        st["conf"][item] = max(0.0, raw_conf * 0.75)
                        st["confidence_reasons"][item] = "ch1_residual"
                else:
                    st["residual_streak"][item] = 0
        # ---- Ch2: money account with spend decomposition ----
        if opp is not None and st["money_prev"] is not None:
            dm = _get(opp, "money", 0.0) - st["money_prev"]
            hands_now = len(_get(opp, "hands", []) or [])
            hire_spend = _FIB_CUM[hands_now] if hands_now < len(_FIB_CUM) \
                else 0
            quads_now = len(_get(opp, "unlocked_quadrants", ["NW"]) or [])
            land_spend = 0
            if st.get("quads_prev") is not None and quads_now > \
                    st["quads_prev"]:
                land_spend = sum(LAND_PRICES_EMB[st["quads_prev"]:
                                                 quads_now])
            animals_now = 0
            plants_today = 0
            for row in _get(opp, "tiles", []) or []:
                for tile in row:
                    if not isinstance(tile, dict):
                        continue
                    if "animal" in tile:
                        animals_now += 1
                    elif _get(tile, "kind", "") == "PLANT" and \
                            _get(tile, "planted_day", -1) == day:
                        plants_today += 1
            animal_spend = 0
            if st.get("animals_prev") is not None:
                animal_spend = max(0, animals_now - st["animals_prev"]) * \
                    min(a["cost"] for a in ANIMALS.values())
            seed_spend_est = plants_today * \
                max(c["seed"] for c in CROPS.values())
            buy_spend_est = sum(
                max(0, -v) * _get(prices_now, k, BASE_PRICE.get(k, 0))
                for k, v in ch0_flow.items())
            st["ch2"] = {"dmoney": dm, "hire_spend": hire_spend,
                         "land_spend": land_spend,
                         "animal_spend_est": animal_spend,
                         "seed_spend_est": seed_spend_est,
                         "buy_spend_est": round(buy_spend_est, 1),
                         "sell_revenue_est": round(
                             dm + hire_spend + land_spend + animal_spend
                             + seed_spend_est + buy_spend_est, 1)}
            st["quads_prev"] = quads_now
            st["animals_prev"] = animals_now
        # roll snapshots for tomorrow
        st["account_window"] = {
            "from_day": st.get("snapshot_day"),
            "from_hour": st.get("snapshot_hour"),
            "to_day": day,
            "to_hour": hour,
            "shops": list(shops_prev if shops_prev is not None else shops),
            "warmup": first_pass,
            "had_buy": bool(bought),
            "had_floor_sell": bool(sold_floor),
            "order_basis": st["order_basis"],
        }
        st["ch0_components"] = ch0_components
        st["event_ledger"] = event_ledger
        st["accounted_day"] = day
        st["initialized"] = True
        st["snapshot_day"] = day
        st["snapshot_hour"] = hour
        st["inv_prev"] = inv
        st["prices_prev"] = prices_now
        st["shops_prev"] = list(shops)
        st["money_prev"] = _get(opp, "money", None) if opp else None
        for key in ("sold_today", "bought_today", "sold_floor",
                    "requested_sell", "requested_buy",
                    "requested_floor_sell", "filled_sell", "filled_buy",
                    "filled_floor_sell"):
            st[key] = {}
        st["fill_known"] = False
        st["fill_incomplete"] = False
        st["harvest_today"] = {}
        st["unknown_loss_today"] = {}
        if opp is not None:
            st["_opp_yields"] = yields_now
            st["_opp_fed"] = yields_now.get("__fed__", 0)
            st["_opp_tiles"] = tiles_now
            st["tile_yield_prev"] = {
                k: v for k, v in yields_now.items() if k != "__fed__"}
            st["_opp_prod"] = _opp_production_night(opp, day)
            st["_opp_prod_tiles"] = _opp_production_night(
                opp, day, by_tile=True)
            st["prod_horizon"] = _opp_production_calendar(opp, day,
                                                          horizon=7)
    except Exception:
        try:
            st = _OPP_OBSERVER.get(_get(obs, "player", 0))
            if st:
                st["conf"] = {k: 0.0 for k in BASE_PRICE}
        except Exception:
            pass


# ---- est_* read-only getters（唯一公共面，M-H 边界纪律）----

def _observer_state_for(player):
    """Resolve an observer state without guessing between multiple seats."""
    if player is not None:
        return _OPP_OBSERVER.get(player)
    if len(_OPP_OBSERVER) == 1:
        return next(iter(_OPP_OBSERVER.values()))
    return None


def est_opp_net(item, days=3, player=None):
    """Opponent net sell flow for `item`, mean over the last `days` days."""
    st = _observer_state_for(player)
    hist = (st or {}).get("flow_hist", {}).get(item, [])
    if not hist:
        return None
    window = hist[-max(1, int(days)):]
    return sum(window) / float(len(window))


def est_opp_held(item, player=None):
    """Estimated unmonetized opponent holding of `item`."""
    st = _observer_state_for(player)
    held = (st or {}).get("held", {})
    return held.get(item) if item in held else None


def est_opp_conf(item, player=None):
    """Confidence in [0,1] for `item` estimates (0 after any failure).

    Capped by OBS_HELD_CONF_CAP: the V0 offline validator's held-MAE table
    is frozen into per-item caps (observer §6: coefficients are decided
    OFFLINE from the corpus -- nothing is learned online)."""
    st = _observer_state_for(player)
    conf = (st or {}).get("conf", {})
    if item not in conf:
        return 0.0
    return min(conf[item], OBS_HELD_CONF_CAP.get(item, 1.0))


def est_opp_supply_horizon(item, horizon_days=7, player=None):
    """Held now plus public-tile production over the requested horizon."""
    st = _observer_state_for(player)
    held = ((st or {}).get("held", {}) or {}).get(item, 0)
    daily = ((st or {}).get("prod_horizon", {}) or {}).get(item)
    if daily:
        return held + sum(daily[:max(1, int(horizon_days))])
    return held


# 【中文】对手上市日历（branch plan §7.4 轻量前置，纯公开信息）：
def _opp_production_calendar(farm, day, horizon=7):
    """Daily NEW-harvestable units per item for the opponent (public tiles).

    Ongoing crops: one production evening per interval while production
    count < max_yield; animals: one per interval while within max_held.
    """
    cal = {item: [0] * horizon for item in BASE_PRICE}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                planted = _get(tile, "planted_day", day)
                interval = max(1, cd["interval"])
                first_ev = planted + cd["first_yield_day"] - 1
                for k in range(cd["max_yield"]):
                    offset = first_ev + k * interval - day
                    if 0 <= offset < horizon:
                        cal[crop][offset] += 1
            elif "animal" in tile:
                a = ANIMALS.get(_get(tile, "animal", ""), {})
                if not a:
                    continue
                placed = _get(tile, "placed_day", day)
                first_ev = placed + a["first_yield_day"] - 1
                prod = a.get("product", "")
                for k in range(a.get("max_held", 6)):
                    offset = first_ev + k * a["interval"] - day
                    # the same horizon guard the crop branch has: an
                    # out-of-window offset must be skipped, not indexed
                    # ( IndexError here killed whole shadow calls; the
                    # mis-indented pre-W2 form also wrote only the LAST
                    # event of each animal -- both silently wrong )
                    if 0 <= offset < horizon and prod in cal:
                        cal[prod][offset] += 1
    return cal
