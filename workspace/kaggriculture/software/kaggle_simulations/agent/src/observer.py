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
    if st is not None and st.get("day") == day \
            and st.get("source") == "ch0":
        return dict(st.get("flow", {}))
    if st is None or st.get("day", -1) >= day:
        _MARKET_MEM[player] = {"day": day, "prices": dict(prices),
                               "flow": (st or {}).get("flow", {})}
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


def reset_observer():
    """OB-3.1: detach both seats' observer state (local tooling)."""
    _OPP_OBSERVER.clear()


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
        st = {"day": day, "hour": hour, "accounted_day": -1,
              "inv_prev": {}, "prices_prev": {}, "money_prev": None,
              "tile_yield_prev": {}, "held": {}, "flow_hist": {},
              "sold_today": {}, "bought_today": {}, "sold_floor": {},
              "conf": {}, "last_resid": {}, "prod_horizon": {},
              "quads_prev": None, "animals_prev": None}
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
                    st.setdefault("sold_floor", {})[o[1]] = \
                        st.get("sold_floor", {}).get(o[1], 0) + n
                else:
                    st["sold_today"][o[1]] = \
                        st["sold_today"].get(o[1], 0) + n
            elif o[0] == "BUY_PRODUCT" and o[1] in BASE_PRICE:
                st["bought_today"][o[1]] = \
                    st["bought_today"].get(o[1], 0) + n
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


def _opp_production_night(farm, day):
    """Overnight production estimate for the EOD of `day` (engine-exact for
    base units; the fertilized+watered doubling is not reconstructable from
    an hour-0 snapshot -- conf penalty covers it)."""
    out = {item: 0 for item in BASE_PRICE}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
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
                if dsf >= 0 and dsf % interval == 0 \
                        and dsf // interval < cd["max_yield"]:
                    if crop in out:
                        out[crop] += 1
            elif "animal" in tile:
                a = ANIMALS.get(_get(tile, "animal", ""), {})
                if not a:
                    continue
                placed = _get(tile, "placed_day", day)
                dsf = (day + 1) - placed - a["first_yield_day"]
                if dsf >= 0 and dsf % a["interval"] == 0:
                    prod = a.get("product", "")
                    if prod in out:
                        out[prod] += 1
    return out


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
            return  # already accounted today
        farms = _get(obs, "farms", []) or []
        opp = None
        for i, f in enumerate(farms):
            if i != player:
                opp = f
                break
        market = _get(obs, "market", {}) or {}
        inv = dict(_get(market, "inventory", {}) or {})
        prices_now = dict(_get(market, "prices", {}) or {})
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
        sold = st["sold_today"]
        bought = st["bought_today"]
        first_pass = st.get("initialized") is not True
        ch0_flow = {}
        ch1_implied = {}
        for item in BASE_PRICE:
            # ---- Ch0: exact integer flow (direct inventory read) ----
            opp_net = None
            if item in inv and item in prev_inv:
                our_net = sold.get(item, 0) - bought.get(item, 0)
                opp_net = (inv[item] - prev_inv[item]) - our_net \
                    + absorb.get(item, 0)
                ch0_flow[item] = float(opp_net)
            # ---- Ch1 cross-check: price-inversion implied delta ----
            if item in MARKET_PARAMS_EMB and item in prices_now \
                    and item in st.get("prices_prev", {}):
                ch1_implied[item] = \
                    _offset_from_price(item, prices_now[item]) - \
                    _offset_from_price(item, st["prices_prev"][item])
            # ---- Ch3: harvest ledger from public tiles ----
            y_now = st.get("_opp_yields", {}).get(item, 0)
            y_prev = st["tile_yield_prev"].get(item, 0)
            prod_est = st.get("_opp_prod", {}).get(item, 0)
            harvested = max(0, y_prev + prod_est - y_now)
            sold_units = sold.get(item, 0)
            if item == "WHEAT":
                fed_units = st.get("_opp_fed", 0)
                bought_units = bought.get("WHEAT", 0)
                if opp_net is not None:
                    bought_units = max(bought_units, -opp_net)
                    sold_units = max(0, opp_net)
                held_delta = harvested + bought_units - sold_units - fed_units
            elif item == "FERTILIZER":
                if opp_net is not None:
                    sold_units = max(0, opp_net)
                held_delta = -sold_units  # gather side unobservable
                st["conf"][item] = 0.5
            else:
                if opp_net is not None:
                    sold_units = max(0, opp_net)
                held_delta = harvested - sold_units
            st["held"][item] = max(0, st["held"].get(item, 0) + held_delta)
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
        # ---- Ch1 residual monitor (persistent non-zero = mirror/engine
        # mismatch or floor-price saturation -> conf downgrade) ----
        st["last_resid"] = {item: round(ch0_flow[item] - ch1_implied[item], 2)
                            for item in ch0_flow if item in ch1_implied}
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
        st["accounted_day"] = day
        st["initialized"] = True
        st["inv_prev"] = inv
        st["prices_prev"] = prices_now
        st["shops_prev"] = list(shops)
        st["money_prev"] = _get(opp, "money", None) if opp else None
        st["sold_today"] = {}
        st["bought_today"] = {}
        st["sold_floor"] = {}
        if opp is not None:
            yields = _opp_tile_yields(opp)
            st["_opp_yields"] = yields
            st["_opp_fed"] = yields.get("__fed__", 0)
            st["tile_yield_prev"] = {
                k: v for k, v in yields.items() if k != "__fed__"}
            st["_opp_prod"] = _opp_production_night(opp, day)
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

def est_opp_net(item, days=3):
    """Opponent net sell flow for `item`, mean over the last `days` days."""
    best = None
    for st in _OPP_OBSERVER.values():
        hist = st.get("flow_hist", {}).get(item, [])
        if hist:
            best = hist
    if not best:
        return None
    window = best[-max(1, int(days)):]
    return sum(window) / float(len(window))


def est_opp_held(item):
    """Estimated unmonetized opponent holding of `item` (decision-grade)."""
    for st in _OPP_OBSERVER.values():
        if item in st.get("held", {}):
            return st["held"].get(item, 0)
    return None


def est_opp_conf(item):
    """Confidence in [0,1] for `item` estimates (0 after any failure).

    Capped by OBS_HELD_CONF_CAP: the V0 offline validator's held-MAE table
    is frozen into per-item caps (observer §6: coefficients are decided
    OFFLINE from the corpus -- nothing is learned online)."""
    for st in _OPP_OBSERVER.values():
        if item in st.get("conf", {}):
            return min(st["conf"][item], OBS_HELD_CONF_CAP.get(item, 1.0))
    return 0.0


def est_opp_supply_horizon(item, horizon_days=7):
    """Held now + the production-side calendar's next `horizon_days` days
    (OB-3.4 real form: 在持 + 产期表未来产出，公开 tiles 缓存于日账)."""
    held = est_opp_held(item) or 0
    for st in _OPP_OBSERVER.values():
        daily = (st.get("prod_horizon") or {}).get(item)
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
