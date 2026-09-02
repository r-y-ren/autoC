# ===========================================================================
# 【中文·模块导览】src/solver.py —— v10.9 调度权威 + v9 影子路由（L3 前世）
# ---------------------------------------------------------------------------
# v10.9 职责：_schedule_units_v72 两阶段调度（Phase A 红线一票否决 +
#   Phase B 价值匹配贪心 Score=V−行走−跨区+亲和+粘滞）是现执行权威；
#   _route_tasks（v9 分区巡逻路由）仅在 V9_SHADOW_ROUTING=True 下影子
#   采集；_schedule_units 壳层兼顾 telemetry/trace；_TARGETS/_sticky_state
#   按消费方就近落位本模块（JOURNAL 2026-09-02 grep 裁决，偏离计划表
#   初判 mission，豁免条款行使）。
# 新架构落位：scheduler 设计 §3 路线求解器（分区+EDF×价值密度×老化+
#   2-opt 同类段抛光）的替换宿主；保证定理（§5 proved-or-flagged）在
#   本层落地后生效。
# 文档符合性审查：
#   ✓ 影子先行纪律已内建（V9_SHADOW_ROUTING 默认 True，执行权不动，
#     巡游奖励/事件重建代码现成——§3.3 处置表"吸收"项）；
#   ✗ 待办（M3）——黎明一次求解的路线承诺（含逐站 ETA/负载均衡指派）
#     尚不存在；现行逐回合贪心正是文档诊断的病根（idle-PASS ~50% vs
#     tetsuya 13%、连续性 47-57% vs 78%、任务无限饿死致荒草累积）；
#   ✗ 待办（M4/M5）——executor 接管后 Phase A/B 与 STICKY/CROSS_QUAD/
#     BUCKET 旋钮按 §3.3 处置表退役删除（结构替代参数）。
# ===========================================================================
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


# ===========================================================================
# 【中文】M3 路线求解器 v2（scheduler §3，2026-09-02 Phase-A 重做）
# ---------------------------------------------------------------------------
# W2 版教训（M3 分歧统计确诊）：黎明 h0 快照里雇工尚未补雇（引擎 EOD 清空
# 全员、h0-2 才 HIRE），按快照 roster 求解=孤身 farmer 的 24 回合预算对
# 7-33 件 D1 必然崩盘（影子 D1 覆盖 9.5% 的根因）；且簇-LPT 分区把 D1 集中
# 到象限主、单链 ETA 累计很快越线。v2 设计：
#   * 船员预置（§5.3 规则 1 劳力先行）：roster = farmer + 计划雇工数
#     （_crew_target），全员按 F6 黎明重置位于 farmer 出生点；
#   * EDF 死线优先分配：D1 按 (deadline, key) 逐件指给"完成最早"且
#     slack≥0 的工人（喂食腿预备成本计入 finish），从根上保证覆盖；
#   * 24 回合预算填充：非 D1 按 (deadline, 密度, key) 入"增量成本最小"
#     且预算内的工人；带死线的填充件 ETA 超线即丢弃（记 drop_reasons）；
#   * 喂食腿：cargo 记账（每腿 FEED_LEG_CHUNK 麦），缺货自动在最近的
#     仓口插合成 PICKUP 腿；任务表自带麦 PICKUP 计入 cargo；
#   * 2-opt 只抛光无死线尾段（D1 段的 EDF 序不动）；
#   * D1 终验：任何 D1 站 ETA 越线 → infeasible（保留站点，绝不静默丢）。
# 确定性契约：全部选择键终结于 (finish/增量, worker, str(key))。
# 影子件：执行权威仍在 _schedule_units_v72；M3 门=分歧统计
# （scripts/solver_shadow_stats.py：D1 覆盖 ≥ v72 红线零失误、PASS/连续性
# 不劣、确定性）。
# ===========================================================================

def _seg_len(seq, start):
    cx, cy = start
    total = 0
    for t in seq:
        total += _dist(cx, cy, t["x"], t["y"])
        cx, cy = t["x"], t["y"]
    return total


def _two_opt_segment(seg, start):
    """2-opt polish (strict improvement only; deterministic scan order)."""
    if len(seg) < 3:
        return list(seg)
    best = list(seg)
    best_len = _seg_len(best, start)
    improved = True
    passes = 0
    while improved and passes < TWO_OPT_MAX_PASSES:
        improved = False
        passes += 1
        for i in range(len(best)):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                cand_len = _seg_len(cand, start)
                if cand_len < best_len - 1e-9:
                    best, best_len = cand, cand_len
                    improved = True
    return best


def _dawn_crew_size(farm, day):
    """Planned crew for the dawn roster (§5.3 rule 1, labour-first).

    The h0 snapshot has NO hands (the engine clears them at EOD and the
    burst hires land at h0-2), so the solve roster must provision the
    PLANNED crew from _crew_target -- capacity that will exist by mid-morning.
    """
    herd = 0
    wheat = 0
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if "animal" in tile:
                herd += 1
            elif _get(tile, "kind", "") == "PLANT" \
                    and _get(tile, "crop", "") == "WHEAT":
                wheat += 1
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    try:
        planned = _crew_target(day, herd, wheat, quads, None)
    except Exception:
        planned = 0
    return max(0, int(planned))


def _solve_routes(farm, private, day, tasks, aging=None,
                  planned_hands=None):
    """Shadow M3 v2: EDF deadline-first allocation + per-worker 24-turn
    budget + dawn-crew provisioning + cargo-aware feed legs.

    Returns {"routes": [ {worker, sector, stops:[keys], tasks:[dicts],
    etas:[hours]} ], "feasible": bool, "dropped": [keys],
    "drop_reasons": {"no_fit": n, "eta": m}, "feed_legs": int}.
    Determinism: every selection key terminates in (metric, worker, key).
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    fx, fy = tuple(_get(farm, "farmer",
                        [board // 2 - 1, board // 2 - 1]))
    hands = _get(farm, "hands", []) or []
    if planned_hands is None:
        planned_hands = max(0, _dawn_crew_size(farm, day) - len(hands))
    # F6: everyone resets to spawn overnight; hired hands materialize at
    # the farmer's dawn position through the morning burst.
    units = [(fx, fy)] * (1 + len(hands) + int(planned_hands))
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]
    accesses = sorted(_shed_access(board, quads)) if board else []
    aging = aging or {}
    horizon = 24                        # per-worker daily turn budget
    inventories = _get(private, "inventories", []) or []

    def tkey(t):
        return str(t.get("key"))

    def density(t):
        v = float(t.get("v") or 0) * (1.0 + 0.25 * aging.get(t.get("key"), 0))
        return v / max(1.0, float(t.get("w") or 1))

    def is_feed(t):
        return (t.get("act") or [None])[0] == "FEED"

    def pickup_units(t):
        act = t.get("act") or []
        if act and act[0] == "PICKUP" and len(act) > 2 and act[1] == "WHEAT":
            try:
                return int(act[2] or 0)
            except (TypeError, ValueError):
                return 0
        return 0

    workers = list(range(len(units)))
    routes_seq = {w: [] for w in workers}      # ordered stop dicts
    clock = {w: 0 for w in workers}
    pos = {w: units[w] for w in workers}
    cargo = {w: 0 for w in workers}            # wheat carried
    for w in workers:
        # inventories[0] is the farmer's, [1..] the hands'
        if w < len(inventories) and inventories[w]:
            cargo[w] = int(_get(inventories[w], "WHEAT", 0) or 0)

    dropped = []
    drop_reasons = {"no_fit": 0, "eta": 0}
    feasible = True
    feed_legs_total = 0

    def leg_plan(w, t):
        """Feed-leg estimate for serving t from worker w's current state:
        (extra_cost, access) -- extra over the direct walk, plus the
        materialized leg stop position."""
        if not is_feed(t) or cargo[w] > 0 or not accesses:
            return 0, None
        best_acc, best_total = None, None
        px, py = pos[w]
        for ax, ay in accesses:
            total = _dist(px, py, ax, ay) + 1 + _dist(ax, ay, t["x"], t["y"])
            if best_total is None or (total, ax, ay) < (best_total,
                                                        best_acc[0],
                                                        best_acc[1]):
                best_total, best_acc = total, (ax, ay)
        direct = _dist(px, py, t["x"], t["y"])
        return max(0, best_total - direct), best_acc

    def append_stop(w, t, leg_extra=0, acc=None):
        nonlocal feed_legs_total
        if leg_extra > 0 and acc is not None:
            seq = len(routes_seq[w])
            routes_seq[w].append({
                "key": ("feedleg", w, seq), "op": "PICKUP",
                "x": acc[0], "y": acc[1],
                "act": ["PICKUP", "WHEAT", FEED_LEG_CHUNK],
                "v": 0, "w": 0, "cls": "LOGISTICS", "tier": None,
                "deadline": None, "deps": [], "synthetic": True})
            px, py = pos[w]
            clock[w] += _dist(px, py, acc[0], acc[1]) + 1
            pos[w] = acc
            cargo[w] += FEED_LEG_CHUNK
            feed_legs_total += 1
        px, py = pos[w]
        clock[w] += _dist(px, py, t["x"], t["y"]) + 1
        pos[w] = (t["x"], t["y"])
        routes_seq[w].append(t)
        cargo[w] += pickup_units(t)
        if is_feed(t):
            cargo[w] -= 1

    all_tasks = list(tasks or [])
    d1 = sorted((t for t in all_tasks
                 if t.get("tier") == "D1" or t.get("red")),
                key=lambda t: ((t["deadline"] if t.get("deadline")
                                is not None else 999), tkey(t)))
    # wheat PICKUPs lead the fill order (cargo enablers: fetch before the
    # mouths -- otherwise legs get synthesized for wheat that was coming)
    rest = sorted((t for t in all_tasks if t not in d1),
                  key=lambda t: (0 if pickup_units(t) > 0 else 1,
                                 0 if t.get("deadline") is not None else 1,
                                 t.get("deadline") or 0, -density(t), tkey(t)))

    # ---- phase 1: EDF allocation of D1 obligations -----------------------
    for t in d1:
        deadline = t.get("deadline")
        best = None
        for w in workers:
            leg_extra, acc = leg_plan(w, t)
            px, py = pos[w]
            finish = clock[w] + _dist(px, py, t["x"], t["y"]) + 1 + leg_extra
            if finish > horizon:
                continue
            if deadline is not None and finish > deadline:
                continue
            cand = (finish, w)
            if best is None or cand < best[0]:
                best = (cand, leg_extra, acc)
        if best is None:
            dropped.append(t.get("key"))
            drop_reasons["no_fit"] += 1
            feasible = False       # an obligation went uncovered
            continue
        (_finish, w), leg_extra, acc = best
        append_stop(w, t, leg_extra, acc)

    # ---- phase 2: budget fill by incremental cost -------------------------
    for t in rest:
        deadline = t.get("deadline")
        best = None
        for w in workers:
            leg_extra, acc = leg_plan(w, t)
            px, py = pos[w]
            finish = clock[w] + _dist(px, py, t["x"], t["y"]) + 1 + leg_extra
            if finish > horizon:
                continue
            if deadline is not None and finish > deadline:
                continue
            cand = (finish, w)
            if best is None or cand < best[0]:
                best = (cand, leg_extra, acc)
        if best is None:
            dropped.append(t.get("key"))
            drop_reasons["eta"] += 1
            continue
        (_finish, w), leg_extra, acc = best
        append_stop(w, t, leg_extra, acc)

    # ---- polish the UNDATED tail of each route (D1/EDF order untouched) ---
    routes = []
    for w in workers:
        seq = routes_seq[w]
        if not seq:
            routes.append({"worker": w, "sector": None, "stops": [],
                           "tasks": [], "etas": []})
            continue
        last_dated = -1
        for i, t in enumerate(seq):
            if t.get("deadline") is not None:
                last_dated = i
        head_seq = seq[:last_dated + 1]
        tail = seq[last_dated + 1:]
        if len(tail) >= 3:
            start_pos = (head_seq[-1]["x"], head_seq[-1]["y"]) \
                if head_seq else units[w]
            tail = _two_opt_segment(tail, start_pos)
        seq = head_seq + tail
        # final ETA pass (post-polish) + D1 terminal verification
        etas = []
        keep = []
        cx, cy = units[w]
        clock_w = 0
        for t in seq:
            clock_w += _dist(cx, cy, t["x"], t["y"]) + 1
            dl = t.get("deadline")
            if (t.get("tier") == "D1" or t.get("red")) and dl is not None \
                    and clock_w > dl:
                feasible = False       # kept, never silently dropped
            keep.append(t)
            etas.append(clock_w)
            cx, cy = t["x"], t["y"]
        routes.append({"worker": w,
                       "sector": _quadrant_of(cx, cy, board) if board
                       else None,
                       "stops": [t.get("key") for t in keep],
                       "tasks": keep, "etas": etas})
    return {"routes": routes, "feasible": feasible, "dropped": dropped,
            "drop_reasons": drop_reasons, "feed_legs": feed_legs_total}
