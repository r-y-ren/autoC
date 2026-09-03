# ===========================================================================
# 【中文·模块导览】src/solver.py —— L3 路线求解器（执行权威，M3 v3）
# ---------------------------------------------------------------------------
# M3 v3（2026-09-03，M5 披露后的 M3 follow-up 落地）：
#   * 现役船员求解（current-roster re-solve）：v2 的"黎明按计划船员预置"
#     是 625.1 在线局崩溃的根因——求解按 _crew_target 的 PLANNED 船员铺
#     路线，雇工没钱落地时幽灵路线上的 D1 义务整日搁浅（rewards ~20 vs
#     ~70k）。v3 每回合对"实际在场的 farmer+hands、实际站位、真实时钟"
#     重解：雇工落地（引擎事实：棚仓口空闲格 NWSE 序）当回合即入编，
#     钱不够少雇就按小船员求解，不存在幽灵。
#   * 逐回合任务新鲜化：喂给求解器的是本回合 _build_tasks 现铺、经
#     _enrich_mission_tasks 升格（cls/tier/deadline/deps）的任务表——
#     日中新义务（当日新种的浇水红线、红升级）当回合即入解，不再依赖
#     黎明冻结快照（v2 的另一搁浅源：mid-day 任务失效）。
#   * 广义载货腿：need 物品（麦/肥/畜）缺货自动在最近仓口插合成 PICKUP
#     腿；棚仓+随身皆空的无解任务先行剔除（当回合物理不可做）。
#   * D1 兜尾：死线内无人能接的 D1 不再静默丢弃——按最早可到工人尽力
#     追加（late 标记，feasible=False 照记）；引擎枯死/逃亡判在 EOD，
#     21/16 点死线是保守缓冲，晚到仍可能救回。
#   * EDF 死线优先 + 24 回合预算填充 + 2-opt 无死线尾段抛光的 v2 骨架
#     不变；确定性契约不变（全部选择键终结于 (finish/增量, worker, key)）。
# v72 两阶段调度器在 M4 门 A/B 验证期仍保留（A 臂=线上验证过的权威），
# 门过即删（M5 冻结删旧，scheduler §3.3/§7）。
# ===========================================================================
# 【中文·模块导览】src/solver.py —— L3 路线求解器（唯一执行权威，M3 v3）
# ---------------------------------------------------------------------------
# v72 两阶段调度器已随 M5 冻结删除（2026-09-03，scheduler §3.3/§7"删全部
# 过渡代码"）；其线上验证过的 pair 经济学——V−μ·d−距离桶支配−跨区惩罚+
# STICKY_BONUS 连续性——已移植进 v3 填充阶段的工人选择（参数沿用原常量）。
# M3 v3（2026-09-03，M5 披露后的 M3 follow-up）四要点：
#   1. 现役船员求解：每回合对"实际在场的 farmer+hands、实际站位、真实
#      时钟"重解——v2 按 PLANNED 船员预置的幽灵路线让未落地雇工的 D1
#      义务整日搁浅（625.1 在线局 rewards ~20 vs ~70k 的根因）；引擎事
#      实：雇工在棚仓口空闲格（NWSE 序）落地，当回合即入编。
#   2. 逐回合任务新鲜化：本回合 _build_tasks 现铺 + _enrich_mission_tasks
#      升格（cls/tier/deadline/deps）；日中新义务（当日新种的红线浇水、
#      红升级）当回合入解（v2 冻结黎明快照的搁浅源）。
#   3. 广义载货腿：缺 need 物品（麦/肥/畜）在最近仓口插合成 PICKUP 腿；
#      棚仓+随身皆空的无解任务当回合剔除。D1 兜尾：死线内无人能接的
#      D1 按"最早可到且真能服务"的工人尽力追加（引擎判死在 EOD，21/16
#      点死线是保守缓冲，晚到仍可能救回）。
#   4. EDF 死线优先（D1 覆盖从根保证）+ 24 回合预算填充（v72 pair 经济
#      学选工人）+ 2-opt 无死线尾段抛光。确定性契约：全部选择键终结于
#      (score/finish, worker, str(key))。
# M4 门披露（4 种子 A/B 台账 exports/probes/m4_switchover_ab.json）：
#   结构判据全过——硬逃亡 0 / EOD 溢出 0 / 确定性 / 全 DONE；经济均值
#   93%（种子 7/8/101 分别 +4.1%/+4.8%/-8.0%，种子 9 -22.7% 为通勤开销
#   与早局利用率的弥散差距，非机械缺陷）。按 2026-09-02 战役裁定"线上
#   公共局为唯一裁决轴"，经济性由线上探针裁决。
# _schedule_units 保留为公共派发入口（四层薄壳，供 entry 与历史测试）。
# ===========================================================================
# ===========================================================================
# 【中文】M3 路线求解器 v3（scheduler §3，2026-09-03 现役船员版）
# ---------------------------------------------------------------------------
# v2 教训（M5 披露定性）：黎明快照求解的三个搁浅源——①按 PLANNED 船员铺
# 幽灵路线（雇工未落地其 D1 整日搁浅）；②路线承诺依赖黎明冻结任务表（日
# 中新种的红线浇水、红升级永不入解）；③全员假位 farmer 出生点+假钟 0（
# ETA 与死线全部失真）。v3 每回合对真实世界重解：
#   * 船员 = farmer + 实际 hands，站位 = 实际站位，时钟 = 当前 hour；
#   * 任务 = 本回合现铺 + 全规格升格（enrich 后 schema 与任务包一致）；
#   * EDF 死线优先（D1 按 (deadline, key) 给"完成最早"且 slack≥0 者从
#     根上保证覆盖）+ 24 回合预算填充（增量成本最小）+ 2-opt 无死线尾段；
#   * 广义载货腿：缺 need 物品在最近仓口插合成 PICKUP 腿（麦5/肥4/畜2），
#     棚仓+随身皆空的任务当回合剔除；
#   * D1 兜尾：无人能按死线接的 D1 按"最早可到"尽力追加（late 标记），
#     引擎判死在 EOD，晚浇/晚喂仍可能救回；
#   * D1 终验：任何 D1 站 ETA 越线 → infeasible（保留站点，绝不静默丢）。
# 确定性契约：全部选择键终结于 (finish/增量, worker, key)。
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


# need 物品的合成腿粒度（与 v72 取货块一致；棚仓有多少取多少）
_NEED_CHUNK = {"WHEAT": 5, "FERTILIZER": 4, "COW": 2, "SHEEP": 2, "GOOSE": 2}


def _dawn_crew_size(farm, day):
    """Planned crew for the dawn roster (§5.3 rule 1, labour-first).

    Retired from the live path at v3: routes are solved for the crew that
    EXISTS (phantom-worker routes stranded their D1 duties -- the M5
    disclosure).  Kept for dawn diagnostics/tests only.
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
                  planned_hands=None, hour=0, unit_pos=None, sticky=None):
    """M3 v3: EDF deadline-first allocation + per-worker turn budget +
    generalized cargo legs.  Current-roster by default: the crew that
    EXISTS, at its ACTUAL positions, with the clock at the CURRENT hour
    (dawn diagnostics may still pass planned_hands to provision a planned
    crew from the farmer's spawn).

    Returns {"routes": [ {worker, sector, stops:[keys], tasks:[dicts],
    etas:[hours]} ], "feasible": bool, "dropped": [keys],
    "drop_reasons": {"no_fit": n, "eta": m, "late_best_effort": k},
    "feed_legs": int}.
    Determinism: every selection key terminates in (metric, worker, key).
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    inventories = _get(private, "inventories", []) or []
    shed = _get(private, "shed", {}) or {}
    available_shed = {item: max(0, int(value or 0))
                      for item, value in shed.items()
                      if isinstance(value, (int, float))}
    hour = max(0, int(hour))
    if unit_pos is not None:
        # current-roster solve: real units at their real positions
        units = [tuple(p) for p in unit_pos]
    else:
        fx, fy = tuple(_get(farm, "farmer",
                            [board // 2 - 1, board // 2 - 1]))
        hands = _get(farm, "hands", []) or []
        if planned_hands is None:
            planned_hands = max(0, _dawn_crew_size(farm, day) - len(hands))
        units = [(fx, fy)] * (1 + len(hands) + int(planned_hands))
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]
    accesses = sorted(_shed_access(board, quads)) if board else []
    aging = aging or {}
    horizon = 24                        # absolute end-of-day (engine h23)

    def tkey(t):
        return str(t.get("key"))

    def density(t):
        v = float(t.get("v") or 0) * (1.0 + 0.25 * aging.get(t.get("key"), 0))
        return v / max(1.0, float(t.get("w") or 1))

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
    clock = {w: hour for w in workers}
    pos = {w: units[w] for w in workers}
    cargo = {w: {} for w in workers}           # item -> carried count
    for w in workers:
        inv = inventories[w] if w < len(inventories) else {}
        for item in ("WHEAT", "FERTILIZER", "COW", "SHEEP", "GOOSE"):
            n = _get(inv, item, 0)
            if n:
                cargo[w][item] = int(n)

    # pre-filter: a task whose need item exists nowhere (shed + every
    # carrier) is physically undoable this turn -- exclude it outright
    def need_available(item):
        total = available_shed.get(item, 0)
        for w in workers:
            total += int(cargo[w].get(item, 0) or 0)
        return total > 0

    dropped = []
    material_deficits = []
    drop_reasons = {"no_fit": 0, "eta": 0, "late_best_effort": 0,
                    "material": 0}
    feasible = True
    feed_legs_total = 0
    late_tail = []                             # D1 obligations to best-effort

    def leg_plan(w, t):
        """Cargo-leg estimate for serving t from worker w's current state:
        (extra_cost, access) -- extra over the direct walk, plus the
        materialized leg stop position.  None when w cannot serve t."""
        item = t.get("need")
        if not item:
            return 0, None
        if cargo[w].get(item, 0) > 0:
            return 0, None                     # already carrying
        if available_shed.get(item, 0) <= 0 or not accesses:
            return None, None                  # nobody can restock w
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

    remaining_need = {}
    for task in tasks or []:
        item = task.get("need")
        if item:
            remaining_need[item] = remaining_need.get(item, 0) + 1

    def append_stop(w, t, leg_extra=0, acc=None):
        nonlocal feed_legs_total
        item = t.get("need")
        act = t.get("act") or []
        if act and act[0] == "PICKUP" and len(act) > 2:
            try:
                amount = min(int(act[2] or 0),
                             available_shed.get(act[1], 0))
            except (TypeError, ValueError):
                return False
            if amount <= 0:
                return False
            t = dict(t)
            t["act"] = list(act[:2]) + [amount]
            act = t["act"]
        if leg_extra > 0 and acc is not None:
            seq = len(routes_seq[w])
            chunk = min(_NEED_CHUNK.get(item, 1),
                        remaining_need.get(item, 1),
                        available_shed.get(item, 0))
            if chunk <= 0:
                return False
            routes_seq[w].append({
                "key": ("feedleg", w, seq), "op": "PICKUP",
                "x": acc[0], "y": acc[1],
                "act": ["PICKUP", item, chunk],
                "v": 0, "w": 0, "cls": "LOGISTICS", "tier": None,
                "deadline": None, "deps": [], "synthetic": True})
            px, py = pos[w]
            clock[w] += _dist(px, py, acc[0], acc[1]) + 1
            pos[w] = acc
            cargo[w][item] = cargo[w].get(item, 0) + chunk
            available_shed[item] -= chunk
            feed_legs_total += 1
        px, py = pos[w]
        clock[w] += _dist(px, py, t["x"], t["y"]) + 1
        pos[w] = (t["x"], t["y"])
        routes_seq[w].append(t)
        if act and act[0] == "PICKUP" and len(act) > 2:
            cargo[w][act[1]] = cargo[w].get(act[1], 0) + amount
            available_shed[act[1]] -= amount
        if item and act and act[0] in ("FEED", "PLACE", "FERTILIZE"):
            cargo[w][item] = max(0, cargo[w].get(item, 0) - 1)
            remaining_need[item] = max(0, remaining_need.get(item, 0) - 1)
        return True

    def worker_allowed(t, w):
        allowed = t.get("units")
        return allowed is None or w in allowed

    def mark_material_deficit(t):
        nonlocal feasible
        key = t.get("key")
        if key not in dropped:
            dropped.append(key)
            drop_reasons["material"] += 1
            material_deficits.append({
                "key": key, "item": t.get("need"),
                "tier": t.get("tier"), "reason": "material"})
        if t.get("tier") == "D1" or t.get("red"):
            feasible = False

    all_tasks = []
    for t in tasks or []:
        item = t.get("need")
        if item and not need_available(item):
            mark_material_deficit(t)
            continue
        all_tasks.append(dict(t))
    d1 = sorted((t for t in all_tasks
                 if t.get("tier") == "D1" or t.get("red")),
                key=lambda t: ((t["deadline"] if t.get("deadline")
                                is not None else 999), tkey(t)))
    # wheat PICKUPs lead the fill order (cargo enablers: fetch before the
    # mouths -- otherwise legs get synthesized for wheat that was coming);
    # then VALUE DENSITY first (v72-parity economics): a deadline-first
    # order let every D2/D3 WATER (deadline 21, v 24-42) outrank every
    # undated HARVEST/PLACE (v hundreds) -- measured on seed 7 as
    # 44 waters vs 1 harvest mid-game and a 5-day PLACE delay whose
    # late-placed animals went terminal-idle and escaped (6 at d28 EOD)
    rest = sorted((t for t in all_tasks if t not in d1),
                  key=lambda t: (0 if pickup_units(t) > 0 else 1,
                                 -density(t),
                                 0 if t.get("deadline") is not None else 1,
                                 t.get("deadline") or 0, tkey(t)))

    # ---- phase 1: EDF allocation of D1 obligations -----------------------
    for t in d1:
        if t.get("need") and not need_available(t["need"]):
            mark_material_deficit(t)
            continue
        deadline = t.get("deadline")
        best = None
        for w in workers:
            if not worker_allowed(t, w):
                continue
            leg_extra, acc = leg_plan(w, t)
            if leg_extra is None:
                continue                       # w cannot be restocked
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
            drop_reasons["no_fit"] += 1
            late_tail.append(t)                # best-effort below, never lost
            continue
        (_finish, w), leg_extra, acc = best
        if not append_stop(w, t, leg_extra, acc):
            mark_material_deficit(t)

    # ---- phase 2: budget fill, v72-parity pair economics ------------------
    # Sequential over tasks in value-density order; the WORKER choice ports
    # v72's proven phase-B score (V - TRAVEL_MU*d - distance-bucket
    # dominance - cross-quadrant penalty, the online-validated constants):
    # near modest work beats distant riches, which kept v72 watering local
    # tiles instead of commuting (seed 101 without this: 28 waters vs A's
    # 48 and 3x the mid-game money gap).  Queue time counts: d_eff = the
    # worker's finish-from-now, so a loaded worker loses to a free one.
    def tval(t):
        v = float(t.get("v") or 0) or float(t.get("w") or 0)
        return v * (1.0 + 0.25 * aging.get(t.get("key"), 0))

    for t in rest:
        if t.get("need") and not need_available(t["need"]):
            mark_material_deficit(t)
            continue
        deadline = t.get("deadline")
        best = None
        for w in workers:
            if not worker_allowed(t, w):
                continue
            leg_extra, acc = leg_plan(w, t)
            if leg_extra is None:
                continue
            px, py = pos[w]
            finish = clock[w] + _dist(px, py, t["x"], t["y"]) + 1 + leg_extra
            if finish > horizon:
                continue
            if deadline is not None and finish > deadline:
                continue
            d_eff = finish - hour
            bucket = 0 if d_eff <= 1 else (1 if d_eff <= 4 else 2)
            score = tval(t) - TRAVEL_MU * d_eff \
                - bucket * BUCKET_DOMINANCE
            if board and _quadrant_of(t["x"], t["y"], board) != \
                    _quadrant_of(px, py, board):
                score -= CROSS_QUAD_PENALTY
            # continuity: the worker already heading for this task keeps it
            # (per-turn re-solve churn -- v72's documented failure mode:
            # "nine workers oscillated between 18 red tiles for eight
            # hours, zero waterings" -- cured by the same bonus)
            if sticky is not None and sticky.get(w) == tkey(t):
                score += STICKY_BONUS
            cand = (-score, finish, w)
            if best is None or cand < best[0]:
                best = (cand, leg_extra, acc)
        if best is None:
            dropped.append(t.get("key"))
            drop_reasons["eta"] += 1
            continue
        _cand, leg_extra, acc = best
        w = _cand[2]
        if not append_stop(w, t, leg_extra, acc):
            mark_material_deficit(t)

    # ---- D1 best-effort tail: earliest-arrival worker, deadline waived ----
    # need-aware: a late FEED appended to a WHEATLESS worker is a silent
    # no-op at the tile (F8) -- the animal starves anyway.  Only workers
    # that can actually serve (carrying the item, or restockable via a
    # leg) are eligible; the need_available pre-filter guarantees at
    # least one exists whenever the task reached this far.
    for t in late_tail:
        best = None
        fallback = None
        for w in workers:
            px, py = pos[w]
            arrive = clock[w] + _dist(px, py, t["x"], t["y"]) + 1
            if fallback is None or (arrive, w) < fallback[0]:
                fallback = ((arrive, w), w)
            leg_extra, acc = leg_plan(w, t)
            if leg_extra is None:
                continue
            arrive += leg_extra
            if best is None or (arrive, w) < best[0]:
                best = ((arrive, w), w, leg_extra, acc)
        if best is not None:
            _a, w, leg_extra, acc = best
            t["late"] = True
            if not append_stop(w, t, leg_extra, acc):
                mark_material_deficit(t)
        elif fallback is not None:
            mark_material_deficit(t)
        drop_reasons["late_best_effort"] += 1
        feasible = False       # an obligation went uncovered by deadline

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
        clock_w = hour
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
            "drop_reasons": drop_reasons, "material_deficits": material_deficits,
            "feed_legs": feed_legs_total}


# per-player-day registry of the previous solve's per-worker first stop
# (continuity input for _solve_routes; day-rolled, harness-resettable)
_ASSIGN_MEM = {}


def _current_units(farm):
    """The crew that exists right now: farmer + hands at their actual
    positions (engine fact: hired hands materialize on the first free
    shed-access tile, NWSE order -- NOT at the farmer's spawn)."""
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer",
                        [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    return units


def _solve_and_execute(obs, farm, private, day, tasks):
    """Four-layer dispatcher (scheduler §2-§4, the M4 live path).

    Per turn: fresh task table (entry's _build_tasks) -> mission-schema
    enrichment -> current-roster solve at the real hour -> mechanical
    execution.  An assertion trip (D1 ETA / EOD overflow snapshot) rebuilds
    once from the live world this same turn (§4 REPLAN); the next turn
    re-solves from scratch anyway (current-roster discipline), so the
    rebuild is bounded and cannot loop.
    """
    hour = _get(obs, "hour", 0)
    player = _get(obs, "player", 0)
    st = _ASSIGN_MEM.get(player)
    if st is None or st.get("day") != day:
        st = {"day": day, "assign": {}}
        _ASSIGN_MEM[player] = st
    etasks = _enrich_mission_tasks(tasks, _mission_tile_map(farm), day)
    units = _current_units(farm)
    solved = _solve_routes(farm, private, day, etasks, planned_hands=0,
                           hour=hour, unit_pos=units, sticky=st["assign"])
    actions, replan = _execute_routes(obs, farm, private, day,
                                      solved.get("routes"))
    replan_repeat = False
    if replan:
        # §4 REPLAN: one bounded rebuild this turn from the same live world.
        # The first _execute_routes only returns actions -- farm/private are
        # unchanged -- so the re-solve is expected to be identical and the
        # executor's idempotent gate suppresses the repeat trip.  A second
        # surviving trip is a persistent assertion (F7 bug signal): surfaced
        # as replan_repeat in the trace, never looped on; the effective
        # remedy is the next turn's current-roster re-solve.
        solved = _solve_routes(farm, private, day, etasks, planned_hands=0,
                               hour=hour, unit_pos=units,
                               sticky=st["assign"])
        actions, replan2 = _execute_routes(obs, farm, private, day,
                                           solved.get("routes"))
        replan_repeat = bool(replan2)
    st["assign"] = {r.get("worker"): (r.get("tasks") or [{}])[0].get("key")
                    for r in solved.get("routes") or []}
    _SCHEDULER_TRACE[player] = {
        "day": day,
        "hour": hour,
        "feasible": bool(solved.get("feasible", True)),
        "dropped": list(solved.get("dropped") or []),
        "drop_reasons": dict(solved.get("drop_reasons") or {}),
        "material_deficits": [dict(item) for item in
                              (solved.get("material_deficits") or [])],
        "feed_legs": int(solved.get("feed_legs", 0) or 0),
        "replanned": bool(replan),
        "replan_repeat": replan_repeat,
    }
    return actions


def _schedule_units(obs, farm, private, day, tasks):
    """Public dispatch (name kept for entry + the historical tests): the
    four-layer pipeline is the ONLY scheduling path since M5 -- v72 was
    deleted with the transition code (scheduler §3.3/§7)."""
    return _solve_and_execute(obs, farm, private, day, tasks)
