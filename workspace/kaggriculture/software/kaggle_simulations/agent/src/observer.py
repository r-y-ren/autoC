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
