# ===========================================================================
# 【中文·模块导览】src/mission.py —— v10.9 任务生成（L2 今日任务包的前世）
# ---------------------------------------------------------------------------
# v10.9 职责：_build_tasks 把"本回合所有可做的事"铺成任务表（浇水/喂食/
#   照料/收割/种植/DIG/建造/放置/拾取归还），带 w 粗权重、v 价值估计、
#   red 红线标记、need 载货、units 工人资格；末日走特化分支。
# 新架构落位：scheduler 设计 §2 今日任务包（_build_mission）的重写宿主。
# 文档符合性审查（scheduler v1.3 逐项）：
#   ✗ 任务 schema 为旧代（w/v/red）——无 cls（OBLIGATION/YIELD/BONUS/
#     LOGISTICS）、deadline（D1 今夜必死/D2 宽限/D3 产钱窗口分级）、
#     deps、scenario 变体标签，M2 重写对象（黄金哈希锁定任务包）；
#   ✗ capex 时点收编未实现（种植配额+配对 WATER 同包出生，治
#     ep104585743 一天种 10 格 16 格枯死类）与三重前置检查（§2.7）；
#   ✗ EOD 预算不等式 Σ(棚仓+随身)≤100（§2.4）与卖出排程耦合（§2.5）
#     未实现；
#   ○ 价值估计函数族（_crop_future_value 系）在 market.py，重写任务包
#     时按 cls/deadline 重组而非丢弃；水窗护栏（V-T3）与末日模板是
#     现成可平移件。
# ===========================================================================


# 【中文】═══ 任务构建（把"本回合所有可做的事"铺成任务表）═══
# 返回 (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)。
# 任务统一结构：w 粗权重 / v 价值估计（Phase B 评分用）/ red 红线标记
# （Phase A 一票否决通道）/ need 需携带物品 / units 限定可执行工人。
# 任务来源与优先级梗概（数字=典型 w/v）：
#   末日(day29)：归还背包 DROP 120·红 + 终局收割 110；
#   生存红线：今夜枯死的浇水 98·红、断粮/过时未喂的 FEED 88-100·红、
#             满载工人回仓 PICKUP 96；
#   收获：连续产 4+/2+ 件 85/70（满格 tile 正在丢产量）、一次性成熟 80/
#             烂前抢救 95、畜产 5+/3+ 件 92/70；
#   建设与安置：建舍 46、放置栏中牲畜 82（未安置牲畜不产且占库容）；
#   种植：轮作作物 32 / 小麦 30（今种今浇的红线义务在浇水分支）；
#   维护：浇水（窗口内 42 / 连续产 40 / 保命 24）、施肥 34-36、
#             CARE 56、收粪 44；
#   杂草/轮作 DIG 22-23（仅深夜窗口，见 v7 旋钮）；
#   后勤：从仓库取小麦/牲畜/肥料的 PICKUP 94/40。
# 第 29 天走独立的"只清算"分支（无 capex、先还后卖、跳过不可行收获）。
def _build_tasks(obs, farm, private, day, plan=None):
    """Return (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)."""
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    builds, crop_map, n_animals, capacity = _field_alloc(farm, day, prices,
                                                         plan)
    seeds = _get(private, "seeds", {}) or {}
    shed = _get(private, "shed", {}) or {}
    inventories = _get(private, "inventories", []) or []
    wheat_on_units = sum(_get(inv, "WHEAT", 0) for inv in inventories if inv)
    species_on_units = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    fert_on_units = 0
    for inv in inventories:
        if not inv:
            continue
        for animal in species_on_units:
            species_on_units[animal] += _get(inv, animal, 0)
        fert_on_units += _get(inv, "FERTILIZER", 0)
    animals_to_feed = 0

    tasks = []

    def add(w, x, y, act, key, need=None, units=None, v=None, red=False):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key,
                      "need": need, "units": units,
                      "v": w if v is None else v, "red": red})

    last_day = day >= SEASON_DAYS - 1
    stop_feed = day >= ENDGAME_DAY        # FM-O4: doomsday stop-feeding
    hour = _get(obs, "hour", 0)           # v7-H: PLANT needs the EOD window
    if last_day:
        positions = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
        positions.extend(tuple(hand) for hand in (_get(farm, "hands", []) or []))
        accesses = _shed_access(board, _get(farm, "unlocked_quadrants", ["NW"]))

        for ui, (ux, uy) in enumerate(positions):
            inv = inventories[ui] if ui < len(inventories) else {}
            if sum(n for n in inv.values() if isinstance(n, (int, float)) and n > 0) <= 0:
                continue
            sx, sy = min(accesses, key=lambda pos: (_dist(ux, uy, *pos), pos[1], pos[0]))
            add(120, sx, sy, ["DROP"], ("return", ui), units={ui},
                v=60 * sum(n for n in inv.values()
                           if isinstance(n, (int, float)) and n > 0),
                red=True)
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or _get(tile, "yield_units", 0) <= 0:
                    continue
                if _get(tile, "kind", "") != "PLANT" and "animal" not in tile:
                    continue
                eligible = set()
                return_distance = min(_dist(x, y, *pos) for pos in accesses)
                for ui, (ux, uy) in enumerate(positions):
                    inv = inventories[ui] if ui < len(inventories) else {}
                    if any(n > 0 for n in inv.values() if isinstance(n, (int, float))):
                        continue
                    turns_needed = _dist(ux, uy, x, y) + 1 + return_distance + 1
                    if turns_needed <= 23 - hour:
                        eligible.add(ui)
                if eligible:
                    item = _get(tile, "crop", None)
                    price = BASE_PRICE.get(item if item in BASE_PRICE else
                                           ANIMALS.get(_get(tile, "animal", ""),
                                                       {}).get("product", ""), 0)
                    add(110, x, y, ["HARVEST"], ("harvest", x, y),
                        units=eligible, v=_get(tile, "yield_units", 0) * price)
        herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
            + sum(species_on_units.values())
        return tasks, 0, herd_total, len(crop_map["WHEAT"]), capacity

    # species still waiting in the shed (place tasks need carriers)
    placeable = {"SHEEP": _get(shed, "SHEEP", 0) + species_on_units["SHEEP"],
                 "COW": _get(shed, "COW", 0) + species_on_units["COW"],
                 "GOOSE": _get(shed, "GOOSE", 0) + species_on_units["GOOSE"]}
    # shed-occupancy harvest discount (P1 mandate: HARVEST value includes
    # the shed occupancy): harvesting into a nearly-full shed whose sell
    # gates are shut just moves the discard cliff closer -- measured
    # bankruptcy mechanism on scale_ranch BA seed 102: wool hoard filled
    # the 100-slot shed, income stopped, no wheat, 12 escapes)
    shed_count = sum(v for v in shed.values()
                     if isinstance(v, (int, float)))
    # 【中文】库容折扣：奶/产品价低于 0.75×base 且仓库 ≥70 格时，收获
    # 价值打折——向卖出门全关的满仓收货只是把 100 格丢弃悬崖提前搬近
    # （scale_ranch BA seed102 实测破产机制：毛囤满仓→收入断流→无麦
    # →12 头逃亡）；gate 打开（真实出价）则不打折。
    def _shed_factor(item_price, item_base):
        if shed_count <= 70:
            return 1.0
        # gates open at a real bid -> the goods can leave the shed again
        if item_price >= 0.75 * item_base:
            return 1.0
        return max(0.35, 1.0 - (shed_count - 70) / 50.0)

    # V-T3 guard state: workers for the per-tile water-window test, and the
    # day's confirmed new plantings (planted_day == day in the observation)
    # for the daily cap.
    plant_units = [tuple(_get(farm, "farmer",
                             [board // 2 - 1, board // 2 - 1]))]
    plant_units.extend(tuple(h) for h in (_get(farm, "hands", []) or []))
    planted_today = 0
    for _row in tiles:
        for _t in _row:
            if isinstance(_t, dict) and _get(_t, "kind", "") == "PLANT" \
                    and _get(_t, "planted_day", -1) == day:
                planted_today += 1
    plant_budget = max(0, PLANT_DAILY_CAP - planted_today)

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if pos in builds:
                    op = "BUILD_COOP" if builds[pos] == "COOP" else "BUILD_PASTURE"
                    add(46, x, y, [op], ("build", x, y), v=180)
                    continue
                crop = None
                for c, positions in crop_map.items():
                    if pos in positions:
                        crop = c
                        break
                if crop is not None and seeds.get(crop, 0) > 0 \
                        and day <= PLANT_LAST_DAY.get(crop, 24) \
                        and (not PLANT_EOD_GUARD
                             or hour <= PLANT_HOUR_MAX) \
                        and plant_budget > 0 \
                        and hour + min(_dist(ux, uy, x, y)
                                       for ux, uy in plant_units) + 2 <= 23:
                    # terminal value of planting TODAY; fresh plants must be
                    # watered the same day -- that obligation is red-flagged
                    # in the PLANT branch below via planted_day == day.
                    # v7-H: a fresh plant starts at streak 1 and dies at the
                    # evening refresh unwatered, so hour > PLANT_HOUR_MAX
                    # just burns the seed and factories a weed.
                    # V-T3: the min-distance clause is the same-day water
                    # window (walk + plant + water must fit before h23);
                    # plant_budget is the daily pulse cap.
                    cd = CROPS[crop]
                    price = _get(prices, crop, BASE_PRICE[crop])
                    ws0, we0 = _window(crop)
                    expect = min(cd["max_yield"], 2 * max(1, we0 - ws0 + 1))
                    net = expect * price - cd["seed"]
                    add(30 if crop == "WHEAT" else 32, x, y,
                        ["PLANT", crop], ("plant", x, y), v=max(30, net * 0.6))
                    plant_budget -= 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                if (pos in builds or any(pos in s for s in crop_map.values())) \
                        and hour >= WEED_DIG_HOUR_MIN:
                    # v7-W: reachable again -- _field_alloc now reserves
                    # reclaimable weeds into builds/crop_map (mode != none);
                    # v7-C2: late-day window only (see knobs above)
                    add(22, x, y, ["DIG"], ("dig", x, y), v=50)
                elif WEED_RECLAIM_MODE == "all" and \
                        hour >= WEED_DIG_HOUR_MIN and \
                        _quadrant_of(x, y, len(tiles)) in (
                            _get(farm, "unlocked_quadrants", ["NW"])
                            or ["NW"]):
                    # C3 pressure-test variant only: DIG even unplanned
                    # weeds (blocks the tile, but no downstream use yet)
                    add(18, x, y, ["DIG"], ("dig", x, y), v=40)
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "WHEAT")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                planned = pos in crop_map.get(crop, ())
                age = day - _get(tile, "planted_day", day)
                yu = _get(tile, "yield_units", 0)
                ws, we = _window(crop)
                in_window = ws <= age <= we
                futval = _crop_future_value(crop, tile, day)
                if ROTATION_DIG and cd["ongoing"] and planned \
                        and _ongoing_evenings_left(crop, tile, day) <= 0 \
                        and yu == 0 \
                        and day >= ROTATION_DIG_DAY \
                        and hour >= WEED_DIG_HOUR_MIN:
                    # v7-R: a finished, fully-harvested ongoing crop is
                    # dead weight -- stop paying water/fertilizer into it
                    # (the two task branches below are gated on futval > 0
                    # for ongoing crops) and free the tile back into the
                    # alloc (top-20 d20-28 DIG pattern).  Late-day window
                    # only: never displaces a live production task.
                    add(23, x, y, ["DIG"], ("dig", x, y), v=45)
                    continue
                if not _get(tile, "watered_today", False):
                    price = _get(prices, crop, BASE_PRICE[crop])
                    if _get(tile, "consecutive_unwatered", 0) >= 1 or \
                            _get(tile, "planted_day", day) == day:
                        # dies tonight (streak 1, or planted today: the
                        # engine starts every fresh plant at streak 1)
                        add(98, x, y, ["WATER"], ("water", x, y),
                            v=futval, red=True)
                    elif planned and cd["ongoing"] and futval > 0:
                        # ongoing crops: watering doubles fertilized output
                        # and keeps the 2-day survival streak clear.  v7-R:
                        # a finished crop (futval 0) is no longer watered.
                        add(40, x, y, ["WATER"], ("water", x, y),
                            v=max(0.3 * futval, price))
                    elif in_window and planned:
                        add(42, x, y, ["WATER"], ("water", x, y),
                            v=2 * price + 0.1 * futval)
                    elif age % 2 == 1 and futval > 0:
                        add(24, x, y, ["WATER"], ("water", x, y),
                            v=0.3 * futval)   # survival
                # FM-4 generalized: animal fertilizer feeds the rotation.
                # One-time crops at age 2 (the +2 window then lands inside
                # the 3-day fertilizer window); strawberry refreshed
                # whenever the 3-day window lapses (each production day
                # pays +2 instead of +1 while watered).  v7-R: never
                # fertilizes a finished ongoing crop.
                if planned and (not cd["ongoing"] or futval > 0) and \
                        _get(tile, "fertilized_until_day", -1) < day:
                    # v10: the engine pays fertilizer only on WATERED days
                    # inside the bonus window (window_start..max_yield_day);
                    # a 3-day fert window must therefore START at the yield
                    # window, not at age 2.  wheat/carrot windows open at
                    # age 2 (unchanged); melon's opens at 6 -- the old
                    # age-2 shot covered ages 2-4 and could never apply.
                    if cd["ongoing"] or \
                            age == (cd["max_yield_day"] + 1) // 2:
                        premium_boost = crop == "STRAWBERRY"
                        fert_dear = _get(prices, "FERTILIZER",
                                         BASE_PRICE["FERTILIZER"]) >= FERT_VALUE_GATE
                        if premium_boost or not fert_dear:
                            add(36 if cd["ongoing"] else 34, x, y, ["FERTILIZE"],
                                ("fert", x, y), need="FERTILIZER",
                                v=190 if premium_boost else 60)
                if yu > 0:
                    price = _get(prices, crop, BASE_PRICE[crop])
                    if cd["ongoing"]:
                        # v10 M-D: an ongoing tile lives exactly
                        # max_yield production events and accumulation
                        # caps at max_yield (engine _daily_refresh_plants:
                        # min(max_yield, yu + bonus)) -- every event that
                        # lands on a full tile is +2 gone forever.  Collect
                        # at 2+, escalating capped tiles above the one-shot
                        # mature band (a capped strawberry tile is losing
                        # production right now).
                        if yu >= 4:
                            add(85, x, y, ["HARVEST"], ("harvest", x, y),
                                v=yu * price
                                * _shed_factor(price, BASE_PRICE[crop]))
                        elif yu >= 2:
                            add(70, x, y, ["HARVEST"], ("harvest", x, y),
                                v=yu * price
                                * _shed_factor(price, BASE_PRICE[crop]))
                    elif age >= cd["max_yield_day"] + 1 or last_day:
                        # rot emergency: one-time crops decay to a weed from
                        # hour 0 of this day, ~1 unit per 2 turns
                        # V-T5: escalated to RED -- a rotting crop is as
                        # time-critical as a thirsty one (the v10.5 crash
                        # class: harvest starved behind red water commutes)
                        add(95, x, y, ["HARVEST"], ("harvest", x, y),
                            v=yu * price + 40, red=True)
                    elif age >= cd["max_yield_day"] and (
                            _get(tile, "watered_today", False) or
                            _get(obs, "hour", 0) >= 18):
                        add(80, x, y, ["HARVEST"], ("harvest", x, y),
                            v=yu * price + 30)
            elif "animal" in tile:
                animal = _get(tile, "animal", "COW")
                spec = ANIMALS.get(animal) or ANIMALS["COW"]
                product = spec["product"]
                price = _get(prices, product, BASE_PRICE[product])
                placed = _get(tile, "placed_day", day)
                prod_remains = _prod_evening_from(day, placed,
                                                  spec["first_yield_day"],
                                                  spec["interval"])
                # r4-P4lite: an animal with no production evening left,
                # no held yield and no escape exposure worth preventing
                # (day 26+: an escape now cannot cost a future harvest)
                # repays nothing for its wheat -- stop feeding it
                terminal_idle = (day >= 26 and not prod_remains
                                 and _get(tile, "yield_units", 0) <= 0)
                if not stop_feed and not terminal_idle:
                    if not _get(tile, "fed_today", False):
                        animals_to_feed += 1
                        streak = _get(tile, "consecutive_unfed", 0) >= 1
                        # escape risk outranks everything: escalate by
                        # streak/hour (r3 escalation hour kept)
                        if streak or _get(obs, "hour", 0) >= FEED_RED_HOUR:
                            w = 100
                            v = spec["cost"] + 2.5 * price   # asset at stake
                            red = True
                        else:
                            w = 88
                            # feed cashes tonight's production bonus (base 1
                            # lands regardless; fed consumes the care bonus)
                            # and keeps every CARE option alive (P0: 0-escape
                            # red line) -- above every water, below harvest
                            v = price + 300
                            red = False
                        add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT",
                            v=v, red=red)
                    if day <= SEASON_DAYS - 3 and not _get(tile, "cared_today", False) \
                            and _get(tile, "fed_today", False):
                        # CARE only pays when another production evening
                        # remains to consume the bonus (else value 0: skip)
                        if prod_remains:
                            add(56, x, y, ["CARE"], ("care", x, y),
                                v=price + 100)
                yu = _get(tile, "yield_units", 0)
                if yu >= 5:
                    add(92, x, y, ["HARVEST"], ("harvest", x, y),
                        v=(yu * price + price)
                        * _shed_factor(price, BASE_PRICE[product]))
                elif yu >= 3 or (yu > 0 and (last_day or stop_feed)):
                    add(70, x, y, ["HARVEST"], ("harvest", x, y),
                        v=(yu * price + (price if prod_remains else 0))
                        * _shed_factor(price, BASE_PRICE[product]))
                if _get(tile, "fertilizer_available", False):
                    add(44, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y),
                        v=85)
            elif kind in ("PASTURE", "COOP") and "animal" not in tile:
                animal = None
                if kind == "COOP" and placeable["GOOSE"] > 0:
                    animal = "GOOSE"
                elif kind == "PASTURE":
                    for candidate in ("SHEEP", "COW"):
                        if placeable[candidate] > 0:
                            animal = candidate
                            break
                if animal is not None and _get(obs, "hour", 0) <= 18:
                    # urgent: an unplaced animal produces nothing and squats
                    # in the shed (a 100-slot shared resource)
                    placeable[animal] -= 1
                    add(82, x, y, ["PLACE", animal], ("place", x, y),
                        need=animal, v=ANIMALS[animal]["cost"] + 120)

    board_half = board // 2
    shed_tile = (board_half - 1, board_half - 1)
    shed_available = {item: max(0, int(n)) for item, n in shed.items()}
    # ---- feed logistics: distribute the wheat across several carriers ----
    # (one carrier cannot FEED a 10-animal ring within 24 turns; chunks of 5
    # are grabbed by different units because a loaded carrier is barred
    # from picking up another chunk -- see executable() below.  Chunks are
    # raised whenever carried wheat falls short of the mouths, so multiple
    # carriers restock throughout the day.)
    if animals_to_feed > 0 and shed_available.get("WHEAT", 0) > 0:
        shortfall = animals_to_feed + 2 - wheat_on_units
        i = 0
        while shortfall > 0 and i < 4 and shed_available.get("WHEAT", 0) > 0:
            n = min(5, shortfall, shed_available["WHEAT"])
            if n <= 0:
                break
            add(96 - 8 * i, shed_tile[0], shed_tile[1], ["PICKUP", "WHEAT", n],
                ("pickup_w", i), v=300 - 20 * i,
                red=(i == 0 and _get(obs, "hour", 0) >= FEED_RED_HOUR))
            shortfall -= n
            shed_available["WHEAT"] -= n
            i += 1
    # ---- animal logistics: carry bought animals onto empty structures ----
    for animal in ("SHEEP", "COW", "GOOSE"):
        if shed_available.get(animal, 0) > 0 and species_on_units[animal] < 2 \
                and any(t["key"][0] == "place" and t["act"][1] == animal
                        for t in tasks):
            n = min(2, shed_available[animal])
            add(94, shed_tile[0], shed_tile[1], ["PICKUP", animal, n],
                ("pickup_a", animal), v=340)
            shed_available[animal] -= n
    # ---- fertilizer logistics for the rotation's fertilize tasks --------
    if any(t["key"][0] == "fert" for t in tasks) and \
            shed_available.get("FERTILIZER", 0) > 0 and fert_on_units < 3:
        n = min(4, shed_available["FERTILIZER"])
        add(40, shed_tile[0], shed_tile[1], ["PICKUP", "FERTILIZER", n],
            ("pickup_f", 0), v=220)
        shed_available["FERTILIZER"] -= n
    herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
        + sum(species_on_units.values())
    return tasks, animals_to_feed, herd_total, len(crop_map["WHEAT"]), capacity


# ===========================================================================
# 【中文】M2 任务包（scheduler 设计 §2，2026-09-02 影子落地）
# ---------------------------------------------------------------------------
# _build_mission：把现行 _build_tasks 的任务表（w/v/red 旧 schema）原位
# 注解成新 schema（cls/deadline），并产出 D1 集合与容量预检——影子件：
# agent() 不调用，黄金测试与 M3 求解器消费（scheduler §7 M2 门）。
# capex 时点收编（§2.3 events）留 M2 切换期——当前仍由市场层管理，三重
# 前置检查已在其位落地（market 侧）。
# ===========================================================================

_MISSION_DEADLINE_HOURS = {"WATER": 21, "FEED": 16, "CARE": 23,
                           "HARVEST": 21, "PLANT": 16}


def _mission_cls(task):
    """旧任务 → 新 cls 分级（scheduler §2.2 D1-D4）。"""
    op = (task.get("act") or [None])[0]
    if task.get("red"):
        return "OBLIGATION"       # 现行红线标记 = D1 今夜必死
    if op == "HARVEST":
        return "YIELD"
    if op in ("CARE", "DIG", "COLLECT_FERTILIZER"):
        return "BONUS"
    return "LOGISTICS"


def _build_mission(obs, farm, private, day, plan, tasks):
    """Shadow M2: annotate the live task table into the mission schema.

    Returns {"day", "cls_counts", "d1", "tasks", "capacity"} where d1 is
    the dies-tonight key set (scheduler §2.2) and capacity carries the
    labor-gate verdict (branch §5.3) for the M2/M3 harness.
    """
    hour = _get(obs, "hour", 0)
    out_tasks = []
    d1 = []
    cls_counts = {}
    for task in tasks or []:
        cls = _mission_cls(task)
        op = (task.get("act") or [None])[0]
        deadline = _MISSION_DEADLINE_HOURS.get(op)
        if cls == "OBLIGATION":
            deadline = _MISSION_DEADLINE_HOURS.get(op, 21)
        t = dict(task)
        t["cls"] = cls
        t["deadline"] = deadline
        t["deps"] = []
        out_tasks.append(t)
        cls_counts[cls] = cls_counts.get(cls, 0) + 1
        if cls == "OBLIGATION":
            d1.append(task.get("key"))
    cap_ok, util = _capacity_gate(farm, private)
    units, comps = _capacity_units(farm, private)
    return {"day": day, "hour": hour, "cls_counts": cls_counts,
            "d1": d1, "tasks": out_tasks,
            "capacity": {"ok": cap_ok, "util": round(util, 3),
                         "units": units, "components": comps}}
