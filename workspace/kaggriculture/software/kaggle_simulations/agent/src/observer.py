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
    """EMA of the observed net inventory flow per item (units/day).

    The day-over-day price move, inverted through the engine curve, IS the
    market's net supply-minus-demand (ours + the opponent's production and
    sales, minus town consumption).  Positive flow = glut building.
    """
    st = _MARKET_MEM.get(player)
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
# 【中文】OBS-1..3 四通道对手供给观测器（opp_supply_observer_design v2，2026-09-02 落地）
# ---------------------------------------------------------------------------
# 工程契约（文档 §3）：
#   * 纯旁路 _OPP_OBSERVER——fail-open，任何异常整体吞掉并置 conf=0，绝不影响决策；
#   * 日账时序：每日首个动作回合做快照+差分+积分（与 _macro_plan 日缓存同型）；
#   * 只读接口一律 est_ 前缀（M-H NO-GO 边界：replay 私有字段仅离线校验器可读，
#     在线运行时只消费合法公开字段的估计值）；
#   * Ch0 obs.market.inventory 直读（引擎 :951-956 每回合赋给双方）为主通道，
#     Ch1 价格反解（_market_flow，上方原函数不动）降级为交叉校验；
#   * Ch2 钱账：Δmoney+可见支出=卖货收入（对手 money/hires/land/animals 公开）；
#   * Ch3 tile 记账：收割量/投喂量为公开整数账（yield_units/fed_today 逐 tile
#     可读），仓库估计 opp_held = Σ(收割+外购−卖出−投喂)（E2 棚溢出高估、
#     E5 种子跨日为已知有界误差，conf 联动下调）。
# 消费方（文档 §4）：P4 三档出清、争议线零囤货连续化、_project_price 对手项、
#   干扰触发器 R_opp——全部经 est_* getter，不直接读状态。
# ===========================================================================
_OPP_OBSERVER = {}


def _opp_observer_state(player, day, hour):
    """Get-or-create the per-player observer state; clock-back = new episode."""
    st = _OPP_OBSERVER.get(player)
    if st is None or day < st.get("day", day) or (
            day == st.get("day", day) and hour < st.get("hour", hour)):
        st = {"day": day, "hour": hour, "accounted_day": -1,
              "inv_prev": {}, "money_prev": None,
              "tile_yield_prev": {}, "held": {}, "flow_hist": {},
              "sold_today": {}, "bought_today": {}, "conf": {},
              "last_resid": {}}
        _OPP_OBSERVER[player] = st
    st["day"] = day
    st["hour"] = hour
    return st


def _opp_note_orders(player, day, hour, orders):
    """Bypass hook (fail-open): record OUR accepted SELL/BUY_PRODUCT units.

    E6: only quoted->1 SELLs add market inventory; floor-price sells move
    money but not inventory (both tracked here as one bucket -- the E1/E6
    correction lands with the offline validator, V0).
    """
    try:
        st = _opp_observer_state(player, day, hour)
        for o in orders or []:
            if not isinstance(o, list) or len(o) < 3 or not o[0]:
                continue
            if o[0] == "SELL" and o[1] in BASE_PRICE:
                n = o[2] if isinstance(o[2], (int, float)) else 0
                st["sold_today"][o[1]] = st["sold_today"].get(o[1], 0) + n
            elif o[0] == "BUY_PRODUCT" and o[1] in BASE_PRICE:
                n = o[2] if isinstance(o[2], (int, float)) else 0
                st["bought_today"][o[1]] = st["bought_today"].get(o[1], 0) + n
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
        shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        absorb = _town_daily_demand(shops)
        prev_inv = st["inv_prev"]
        sold = st["sold_today"]
        bought = st["bought_today"]
        for item in BASE_PRICE:
            # ---- Ch0: exact integer flow (direct inventory read) ----
            opp_net = None
            if item in inv and item in prev_inv:
                our_net = sold.get(item, 0) - bought.get(item, 0)
                opp_net = (inv[item] - prev_inv[item]) - our_net \
                    + absorb.get(item, 0)
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
            if opp_net is not None:
                hist = st["flow_hist"].setdefault(item, [])
                hist.append(opp_net)
                st["conf"].setdefault(item, 1.0)
        # ---- Ch2: money cross-check (revenue plausibility bookkeeping) ----
        if opp is not None and st["money_prev"] is not None:
            dm = _get(opp, "money", 0.0) - st["money_prev"]
            hands_now = len(_get(opp, "hands", []) or [])
            hire_spend = _FIB_CUM[hands_now] if hands_now < len(_FIB_CUM) \
                else 0
            st["ch2"] = {"dmoney": dm, "hire_spend": hire_spend}
        # roll snapshots for tomorrow
        st["accounted_day"] = day
        st["inv_prev"] = inv
        st["money_prev"] = _get(opp, "money", None) if opp else None
        st["sold_today"] = {}
        st["bought_today"] = {}
        if opp is not None:
            yields = _opp_tile_yields(opp)
            st["_opp_yields"] = yields
            st["_opp_fed"] = yields.get("__fed__", 0)
            st["tile_yield_prev"] = {
                k: v for k, v in yields.items() if k != "__fed__"}
            st["_opp_prod"] = _opp_production_night(opp, day)
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
    """Confidence in [0,1] for `item` estimates (0 after any failure)."""
    for st in _OPP_OBSERVER.values():
        if item in st.get("conf", {}):
            return st["conf"][item]
    return 0.0


def est_opp_supply_horizon(item, horizon_days=7):
    """Held now (production-side calendar is served by the daily snapshot)."""
    return est_opp_held(item)


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
                for k in range(a.get("max_held", 6)):
                    offset = first_ev + k * a["interval"] - day
                    if 0 <= offset < horizon:
                        prod = a.get("product", "")
                        if prod in cal:
                            cal[prod][offset] += 1
    return cal
    return flow
