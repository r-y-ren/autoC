# r4-P1 sticky per-worker target registry, keyed by player id and reset at
# each day roll (hour moves backwards).  Kept for compatibility with the
# champion task contract; v9 routes use the event-driven registry below.
_TARGETS = {}
_ROUTE_STATE = {}


def _route_state(player, day, hour, units, board):
    state = _ROUTE_STATE.get(player)
    if state is None or state.get("day") != day or hour <= state.get("hour", -1):
        state = {"day": day, "hour": hour, "home": {}, "routes": {},
                 "targets": {}, "cargo": {}, "red_signature": (),
                 "replans": 0}
        _ROUTE_STATE[player] = state
    state["hour"] = hour
    for ui, (x, y) in enumerate(units):
        state["home"].setdefault(ui, _quadrant_of(x, y, board))
        state["routes"].setdefault(ui, [])
        state["cargo"].setdefault(ui, {"phase": "idle", "item": None,
                                       "target": None})
    return state


def _sticky_state(player, day, hour):
    st = _TARGETS.get(player)
    if st is None or st.get("day") != day or hour <= st.get("hour", -1):
        st = {"day": day, "hour": hour, "assign": {}}
        _TARGETS[player] = st
    st["hour"] = hour
    return st


# 【中文】═══ r4-P1 状态价值调度器（冠军执行器）═══
# 两阶段分派（替代 r3 的 w/(1+dist) 贪心——实测它让远端红线格饿死：
# 每局 14-29 个 CARE 失误杂草全聚在距仓曼哈顿 6-9 格处，请求过的操作
# 全部成功、只是没人去远处）：
#   Phase A 红线一票否决：所有 red 任务按价值降序，逐个由"最近工人"
#     覆盖（缺载货的工人按"先绕仓库再过去"的距离计价+6）；不看权重、
#     每任务只认领一次；
#   Phase B 价值匹配：Score_ij = V_i - TRAVEL_MU×d - 跨象限惩罚
#     + 载货亲和（持有 need 物品的工人 +0.5V，缺货的 -0.5V）
#     + 粘滞奖励（延续上回合目标，抑制震荡），全局排序贪心认领。
# 执行段：走到目标格→执行；缺 need 物品先绕仓库取货（r4-P1 修复
# "空手走range喂料崩溃"）；没任务的工人做脚下免费操作否则 PASS；
# 末尾 R6 护栏：PLANT 数量永远 ≤ 手持种子数。
def _schedule_units_v72(obs, farm, private, day, tasks):
    """r4-P1 state-value scheduler.

    Two phases, replacing the r3 per-unit w/(1+dist) greedy that measurably
    starved distant red-line tiles (29 care-lapse weeds + escapes per game
    while every REQUESTED op succeeded):

      Phase A (red-line, one-vote veto, no weighting): death-tonight
      obligations -- FEED with streak >= 1 (or past FEED_RED_HOUR), WATER
      with streak >= 1 or planted today, last-day DROP returns -- are
      covered FIRST by a nearest-worker greedy in value order.  A
      wheatless worker assigned a red FEED still walks to the shed first
      (fetch detour priced into the distance below).

      Phase B (value matching): Score_ij = V_i - TRAVEL_MU*d_ij
      - CROSS_QUAD_PENALTY (zone stickiness) + item-carrier affinity
      + STICKY_BONUS for yesterday's-turn target (kills oscillation).
      Global greedy over (worker, task) pairs; each task claimed once so
      workers never pile onto one target.
    """
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    inventories = _get(private, "inventories", []) or []
    hour = _get(obs, "hour", 0)
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]
    sticky = _sticky_state(_get(obs, "player", 0), day, hour)["assign"]

    def unit_inv(i):
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    actions = []

    def executable(task, ui):
        eligible = task.get("units")
        if eligible is not None and ui not in eligible:
            return False
        need = task.get("need")
        if need and _get(unit_inv(ui), need, 0) <= 0:
            return False
        x, y = task["x"], task["y"]
        tile = tiles[y][x]
        kind = _get(tile, "kind", "") if isinstance(tile, dict) else None
        op = task["act"][0]
        if op in ("WATER", "FERTILIZE"):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            # engine DIG clears any non-animal tile; v7-R rotation-DIG
            # targets finished PLANTs (weeds remain the other target)
            return kind == "WEED" or kind == "PLANT"
        if op in ("BUILD_PASTURE", "BUILD_COOP"):
            return tile is None
        if op == "PLACE":
            structure = ANIMALS.get(task["act"][1], {}).get("structure")
            return isinstance(tile, dict) and _get(tile, "kind", "") == structure \
                and "animal" not in tile
        if op == "PICKUP":
            if not _shed_adjacent(units[ui][0], units[ui][1], board, quads):
                return False
            # a carrier holding a full chunk moves out to feed instead of
            # chain-grabbing every chunk at the shed (multi-carrier FEED)
            if task["act"][1:2] == ["WHEAT"] and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                return False
            return True
        if op == "DROP":
            return _shed_adjacent(units[ui][0], units[ui][1], board, quads) and any(
                n > 0 for n in unit_inv(ui).values()
                if isinstance(n, (int, float)))
        return True

    def tval(t):
        return t.get("v", t["w"])

    # ---------------- phase A: red-line nearest-match first ----------------
    claimed = set()
    assign = {}
    accesses = _shed_access(board, quads)
    reds = [t for t in tasks if t.get("red")]
    reds.sort(key=lambda t: -tval(t))
    by_key = {t["key"]: t for t in reds}
    # V-T4 red-line stickiness, V-T5 near-end hold: re-bind the previous
    # turn's red assignments first, but a held binding survives only while
    # the target is NEAR (d <= 4).  Forensics pair: ep 104585743 d8 h16-23
    # (no stickiness: nine workers oscillated between 18 red tiles for
    # eight hours, zero waterings) vs ep 104594916 d8-d11 (unconditional
    # stickiness: distant red bindings locked workers into long commutes,
    # the harvest starved, cash broke and all hands reset to zero).  The
    # distance cap keeps the anti-oscillation benefit without the commute
    # lock-in; far red targets still go to the nearest free worker each
    # turn.
    for ui, prev_key in list(sticky.items()):
        if ui in assign or ui >= len(units):
            continue
        t = by_key.get(prev_key)
        if t is None:
            continue
        if t.get("units") is not None and ui not in t["units"]:
            continue
        if _dist(units[ui][0], units[ui][1], t["x"], t["y"]) > 4:
            continue
        assign[ui] = t
        claimed.add(t["key"])
    for t in reds:
        if t["key"] in claimed:
            continue
        best = None
        for ui in range(len(units)):
            if ui in assign or (t.get("units") is not None
                                and ui not in t["units"]):
                continue
            ux, uy = units[ui]
            d = _dist(ux, uy, t["x"], t["y"])
            # a worker missing the carried item pays the shed detour it is
            # about to walk (route below); carriers keep their raw distance
            # so loaded units win red consumer tasks outright
            need = t.get("need")
            if need and _get(unit_inv(ui), need, 0) <= 0:
                via = min(_dist(ux, uy, ax, ay) + _dist(ax, ay, t["x"], t["y"])
                          for ax, ay in accesses)
                d = min(d, via) + 6
            if best is None or d < best[0]:
                best = (d, ui)
        if best is not None:
            assign[best[1]] = t
            claimed.add(t["key"])

    # ---------------- phase B: value matching with stickiness -------------
    # V-T5: home-sector soft penalty (tetsuya-style patrol continuity).  The
    # worker's first position of the day defines its home quadrant; work in
    # the OTHER quadrants pays the soft penalty on top of the distance
    # buckets below.  Red lines stay exempt (phase A above).
    home_quads = _route_state(_get(obs, "player", 0), day, hour, units,
                              board)["home"]
    pairs = []
    for ui in range(len(units)):
        if ui in assign:
            continue
        ux, uy = units[ui]
        uquad = _quadrant_of(ux, uy, board)
        home_quad = home_quads.get(ui) or uquad
        for t in tasks:
            if t["key"] in claimed:
                continue
            if t.get("units") is not None and ui not in t["units"]:
                continue
            d = _dist(ux, uy, t["x"], t["y"])
            # V-T5 distance buckets dominate value (see BUCKET_DOMINANCE):
            # near (0-1) / local (2-4) / far (5+).  A nearby modest task now
            # always beats a distant rich one; value ranks inside a bucket.
            bucket = 0 if d <= 1 else (1 if d <= 4 else 2)
            score = tval(t) - TRAVEL_MU * d - bucket * BUCKET_DOMINANCE
            if _quadrant_of(t["x"], t["y"], board) != uquad:
                score -= CROSS_QUAD_PENALTY
            if _quadrant_of(t["x"], t["y"], board) != home_quad:
                score -= CROSS_SECTOR_PENALTY_V9
            score += float(t.get("_v9_soft", {}).get(ui, 0.0))
            need = t.get("need")
            if need:
                if _get(unit_inv(ui), need, 0) > 0:
                    score += 0.5 * tval(t)   # carriers converge on consumers
                else:
                    score -= 0.5 * tval(t)   # wheatless units de-prioritized
            if t["act"][0] == "PICKUP" and t["act"][1:2] == ["WHEAT"] \
                    and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                score -= 0.5 * tval(t)       # loaded carriers leave the shed
            if sticky.get(ui) == t["key"]:
                score += STICKY_BONUS
            pairs.append((score, ui, t["key"]))
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    for score, ui, key in pairs:
        if ui in assign or key in claimed:
            continue
        for t in tasks:
            if t["key"] == key:
                assign[ui] = t
                claimed.add(key)
                break

    # ---------------- act --------------------------------------------------
    half = board // 2
    shed_avail = _get(private, "shed", {}) or {}
    for ui, (ux, uy) in enumerate(units):
        chosen = assign.get(ui)
        if chosen is None:
            # act on the current tile anyway when something is executable
            # here and unclaimed (free op, zero travel)
            best_here = None
            for t in tasks:
                if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                    continue
                if not executable(t, ui):
                    continue
                if best_here is None or tval(t) > tval(best_here):
                    best_here = t
            if best_here is not None:
                claimed.add(best_here["key"])
                sticky[ui] = None
                actions.append(list(best_here["act"]))
            else:
                sticky[ui] = None
                actions.append(["PASS"])
            continue
        sticky[ui] = chosen["key"]
        cx, cy = chosen["x"], chosen["y"]
        need = chosen.get("need")
        if (ux, uy) == (cx, cy):
            if executable(chosen, ui):
                actions.append(list(chosen["act"]))
                continue
        # missing the carried item: fetch it at the shed BEFORE walking out
        # (r4-P1 fix for the wheatless-walker churn that collapsed feeding)
        if need and _get(unit_inv(ui), need, 0) <= 0:
            near = min(accesses, key=lambda p: _dist(ux, uy, p[0], p[1]))
            if (ux, uy) != near:
                actions.append(_step_towards(ux, uy, near[0], near[1]))
                continue
            chunk = {"WHEAT": 5, "FERTILIZER": 4, "COW": 2, "SHEEP": 2,
                     "GOOSE": 2}.get(need, 1)
            n = min(chunk, _get(shed_avail, need, 0))
            if n > 0:
                actions.append(["PICKUP", need, n])
                continue
        if (ux, uy) != (cx, cy):
            actions.append(_step_towards(ux, uy, cx, cy))
        else:
            # standing on it, item fetched, but the op went stale this turn
            sx, sy = half - 1, half - 1
            actions.append(_step_towards(ux, uy, sx, sy))

    # R6 guard: never request more PLANTs of a crop than seeds held
    seeds = _get(private, "seeds", {}) or {}
    demand = {}
    for a in actions:
        if a and a[0] == "PLANT":
            demand[a[1]] = demand.get(a[1], 0) + 1
    for crop, n in demand.items():
        if n > seeds.get(crop, 0):
            keep = seeds.get(crop, 0)
            for i, a in enumerate(actions):
                if a and a[0] == "PLANT" and a[1] == crop:
                    if keep > 0:
                        keep -= 1
                    else:
                        actions[i] = ["PASS"]
    return actions


def _task_sector(task, board):
    try:
        return _quadrant_of(int(task["x"]), int(task["y"]), board)
    except (KeyError, TypeError, ValueError):
        return None


# 【中文】v9 主场象限影子路由：给每个任务按工人附加 _v9_soft 软分
# （同区 0 / 跨区 -惩罚；本区有活且远区价值未超出 CROSS_SECTOR_VALUE_EDGE
# 时再叠加惩罚）——只调分、绝不收窄资格图（硬过滤实测会淹没跨区高价值
# 工作、把经济困死）。路线批量按"距离优先"排序（价值优先实测是假巡逻，
# 破坏近端浇水节奏）。红线任务完全豁免，Phase A 仍是硬安全否决。
def _route_tasks(obs, farm, private, day, tasks):
    """Add v9 home-sector eligibility without changing task semantics.

    A worker with useful work in its home sector is not offered distant work
    unless the distant task beats the best local value by
    ``CROSS_SECTOR_VALUE_EDGE``.  Red-line tasks are intentionally exempt and
    keep their original eligibility so phase A remains a hard safety veto.
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units, _ = _telemetry_units(farm)
    player = _get(obs, "player", 0)
    state = _route_state(player, day, _get(obs, "hour", 0), units, board)
    copies = [copy.deepcopy(task) for task in tasks]
    active = {task.get("key") for task in copies}
    red_signature = tuple(sorted(repr(task.get("key")) for task in copies
                                 if task.get("red")))
    previous_red = state.get("red_signature", ())
    target_missing = any(key is not None and key not in active
                         for route in state["routes"].values() for key in route)
    changed = red_signature != previous_red or target_missing
    if changed:
        state["replans"] += 1
        state["routes"] = {ui: [] for ui in range(len(units))}
    state["red_signature"] = red_signature

    home = state["home"]
    normal = [task for task in copies if not task.get("red")]
    # Preserve the champion's full eligibility graph.  Sector routing is a
    # soft preference in the downstream score; hard filtering here caused
    # cross-sector high-value work to disappear and stranded the economy.
    original_units = {
        id(task): (set(task["units"]) if task.get("units") is not None
                   else set(range(len(units))))
        for task in normal
    }
    for task in normal:
        task["units"] = set(original_units[id(task)])

    for ui, (ux, uy) in enumerate(units):
        sector = home.get(ui, _quadrant_of(ux, uy, board))
        local = [task for task in normal if _task_sector(task, board) == sector
                 and ui in original_units[id(task)]]
        if local:
            best_local = max(float(task.get("v", task.get("w", 0)))
                              for task in local)
        else:
            best_local = 0.0

        # Attach worker-local soft scores rather than narrowing task
        # eligibility.  The legacy matcher still sees every legal task.
        for task in normal:
            task.setdefault("_v9_soft", {})[ui] = (
                0.0 if _task_sector(task, board) == sector
                else -CROSS_SECTOR_PENALTY_V9)
            if local and task.get("v", task.get("w", 0)) <= \
                    best_local + CROSS_SECTOR_VALUE_EDGE:
                task["_v9_soft"][ui] -= CROSS_SECTOR_PENALTY_V9

        # Retain a useful same-sector batch order in the route registry.  The
        # active task list is updated only on a completion/invalidity signal,
        # not rebuilt merely because the clock advanced one turn.
        current = state["routes"].setdefault(ui, [])
        if changed or not current:
            same = [task for task in copies
                    if not task.get("red") and
                    _task_sector(task, board) == sector and
                    (task.get("units") is None or ui in task["units"])]
            # Distance-first: a value-first head sent workers to far
            # high-value sector tasks (a false sweep) and broke the nearby
            # watering cadence -- measured as template_wheat/cow_baron seed
            # 101 regressions of -20k..-25k on both seats with water
            # pressure +22% (routing_tour, 2026-08-30).  Nearest-first is
            # the actual patrol: short hops, water stays local.
            same.sort(key=lambda task: (_dist(ux, uy, task["x"], task["y"]),
                                        -float(task.get("v", task.get("w", 0))),
                                        repr(task.get("key"))))
            state["routes"][ui] = [task.get("key") for task in same[:ROUTE_BATCH_SIZE]]

    # Route order is a deterministic tie breaker, while red lines still win
    # through the legacy scheduler's phase A.
    route_rank = {}
    for ui, route in state["routes"].items():
        for rank, key in enumerate(route):
            route_rank[(ui, key)] = rank
    for task in copies:
        task.setdefault("_v9_rank", {})
        if task.get("red"):
            continue
        for ui in range(len(units)):
            rank = route_rank.get((ui, task.get("key")))
            task["_v9_rank"][ui] = rank
            if rank is not None:
                task["_v9_soft"][ui] = task["_v9_soft"].get(ui, 0.0) + \
                    max(0.0, V9_TOUR_BONUS - rank * V9_TOUR_DECAY)
    return copies, state


# 【中文】调度入口：先跑 _route_tasks 生成影子路由推荐，但 V9_SHADOW_
# ROUTING=True 时执行权仍交冠军调度器 _schedule_units_v72（原任务表），
# 影子结果只进 _SCHEDULER_TRACE 供遥测对比。切换 False 才会用 routed
# 任务表执行——见上方 V9_SHADOW_ROUTING 处的回归证据（2026-08-30 确认
# 门禁撤销合并：88-0 属选择域运气，泛化域配对净 -258.9k）。
def _schedule_units(obs, farm, private, day, tasks):
    """Keep champion actions while collecting v9 route recommendations.

    The partitioned route is shadow-only until it passes outcome and efficiency
    gates.  The frozen scheduler remains the execution authority, so telemetry
    can be validated without risking the production behavior.
    """
    routed, state = _route_tasks(obs, farm, private, day, tasks)
    if V9_SHADOW_ROUTING:
        actions = _schedule_units_v72(obs, farm, private, day, tasks)
    else:
        actions = _schedule_units_v72(obs, farm, private, day, routed)
    player = _get(obs, "player", 0)
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units, _ = _telemetry_units(farm)
    sticky = _TARGETS.get(player, {}).get("assign", {})
    by_key = {task.get("key"): task for task in routed}
    assign = {}
    action_targets = {}
    cross = 0
    for ui, task_key in sticky.items():
        task = by_key.get(task_key)
        if task is None:
            continue
        assign[ui] = task_key
        action_targets[ui] = (task["x"], task["y"])
        if ui < len(units) and _task_sector(task, board) != \
                state["home"].get(ui):
            cross += 1
        cargo = state["cargo"].setdefault(ui, {"phase": "idle", "item": None,
                                               "target": None})
        need = task.get("need")
        if need and _get((_get(private, "inventories", []) or [{}])[ui]
                         if ui < len((_get(private, "inventories", []) or []))
                         else {}, need, 0) <= 0:
            cargo.update({"phase": "pickup", "item": need,
                          "target": task_key})
        elif need:
            cargo.update({"phase": "deliver", "item": need,
                          "target": task_key})
        else:
            cargo.update({"phase": "idle", "item": None,
                          "target": task_key})
    state["last_assign"] = dict(assign)
    _SCHEDULER_TRACE[player] = {
        "day": day,
        "assign": dict(assign),
        "action_targets": action_targets,
        "home_sector": dict(state["home"]),
        "cross_quadrant": cross,
        "red_assignments": sum(1 for key in assign.values()
                               if by_key.get(key, {}).get("red")),
        "replans": state["replans"],
        "cargo": copy.deepcopy(state["cargo"]),
    }
    return actions
