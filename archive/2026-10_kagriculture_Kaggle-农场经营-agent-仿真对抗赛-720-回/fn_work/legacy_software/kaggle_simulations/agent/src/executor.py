# ===========================================================================
# 【中文·模块导览】src/executor.py —— L4 机械执行器（M4 起 LIVE，v1.3 全规格）
# ---------------------------------------------------------------------------
# 职责：沿路线逐站"到站且 tile 态未完成→发动作，否则走一步"（F1 曼哈顿
#   步进精确；F4 重复 WATER/FEED 是静默浪费，发射前查 tile 态跳过已完成
#   站；F8 缺 need 物品的站跳过——无麦 FEED 是静默 no-op）；
# 断言（只读，§5 proved-or-flagged）：
#   * D1 站点 ETA ≤ deadline（EXECUTOR_D1_ASSERT）；
#   * EOD 真投影 Σ(棚仓+随身+路线剩余 HARVEST 入仓−当日计划卖出)
#     ≤ SHED_CAPACITY（F6：随身日终自动归还、超容销毁——2026-09-04
#     激进波 B 起为完整前瞻投影；黎明当回合卖计划未建时按 0 卖出计，
#     误触发由幂等闸抑制、下回合自愈，EXECUTOR_EOD_ASSERT）；
# 断言失败 → REPLAN：派发器当回合做一次有界自适应重建（执行器上报 F4
#   已完成站集合，重建排除后按剩余工作重排路线；幂等闸 _replan_gate
#   保留为护栏，F7 下正确实现永不触发）。
# d29 内联清算（F10，_execute_routes is_last_day 分支）：早收→DROP（查
#   room）→SELL 随身清零；卖出单进 _D29_SELL_QUEUE 供市场层接线。
# M4/M5 沿革：2026-09-02 Phase-B 切换 → M5 审计发现接线缺陷（结果字典当
#   路线表传入，~97% 回合异常）→ 2026-09-03 M3 v3（现役船员重解）修复后
#   四层成为唯一执行路径，v72 与执行开关随 M5 冻结删除。
# PLACE 站点完成判据修复（M4 门普查发现：空畜栏被误判"已完成"，买入的
#   牲畜囤在棚仓永不安置）。

_REPLAN_MEM = {}
_EXEC_DONE_MEM = {}
_D29_SELL_QUEUE = {}


def _replan_signature(routes):
    parts = []
    for r in routes or []:
        stops = r.get("stops") or []
        keys = tuple(str(s.get("key") if isinstance(s, dict) else s)
                     for s in stops)
        parts.append((r.get("worker"), keys))
    return tuple(sorted(parts))


def _replan_gate(player, day, routes):
    """Idempotent REPLAN gate (§4.4): stop rebuilding when the rebuilt plan
    equals the old one -- under F7 a repeat is a bug signal, not noise."""
    sig = _replan_signature(routes)
    st = _REPLAN_MEM.get(player)
    if st is not None and st.get("day") == day and st.get("sig") == sig:
        return False
    _REPLAN_MEM[player] = {"day": day, "sig": sig}
    return True


def _executor_tiles(farm):
    tiles = _get(farm, "tiles", []) or []
    out = {}
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if isinstance(tile, dict):
                out[(x, y)] = tile
    return out


def _stop_done(tile, act, day):
    """F4 dedup: a repeated WATER/FEED is a silent wasted turn; skip stops
    whose tile state shows the work already finished.  FERTILIZE dedup is
    day-relative (see that branch: the engine field is an absolute
    deadline that survives its own expiry)."""
    if not act:
        return False
    op = act[0]
    if op == "PLANT" or op.startswith("BUILD"):
        # these targets are EMPTY tiles at dawn; once the tile holds
        # anything (plant/structure) the stop is done
        return tile is not None
    if op == "PLACE":
        # PLACE targets an EMPTY STRUCTURE tile (a dict with no animal) --
        # sharing the BUILD branch here marks every PLACE stop as already
        # done, so bought animals squat in the shed forever (found by the
        # M4 gate census: herd=0 across the whole episode)
        return tile is not None and "animal" in tile
    if tile is None:
        return op == "DIG"           # dug weeds become empty tiles
    if op == "WATER":
        return bool(_get(tile, "watered_today", False))
    if op == "FEED":
        return bool(_get(tile, "fed_today", False))
    if op == "CARE":
        return bool(_get(tile, "cared_today", False))
    if op == "FERTILIZE":
        # engine semantics: fertilized_until_day is an ABSOLUTE deadline
        # (FERTILIZE sets max(old, day+2), vendored kaggriculture.py:481;
        # the value is never reset when the window lapses, :769-803), and
        # the engine's own yield checks compare it against the current day
        # (:442, :799).  A stale positive value is an EXPIRED window that
        # mission.py legitimately re-tasks -- testing mere positivity here
        # silently killed every re-fertilize stop (audit 2026-09-03).
        until = _get(tile, "fertilized_until_day", -1)
        return until is not None and until >= day
    if op == "DIG":
        return _get(tile, "kind", "") != "WEED"
    if op == "HARVEST":
        return _get(tile, "yield_units", 1) <= 0
    return False


def _remaining_harvest_inflow(routes, tile_map, day):
    """Route-remaining HARVEST inflow for the EOD projection (§4): every
    not-yet-finished harvest stop on today's routes counts its standing
    tile yield as projected end-of-day shed inflow."""
    inflow = 0
    for r in routes or []:
        for s in (r.get("tasks") or r.get("stops") or []):
            act = s.get("act") or [None]
            if not act or act[0] != "HARVEST":
                continue
            tile = tile_map.get((s.get("x"), s.get("y")))
            if tile is None or _stop_done(tile, s.get("act"), day):
                continue
            y = _get(tile, "yield_units", 0)
            if isinstance(y, (int, float)) and y > 0:
                inflow += int(y)
    return inflow


def _planned_sell_today(player, day):
    """Today's planned sell volume from the MK-2 dawn plan (0 when the
    plan is absent or stale -- the dawn turn runs before it is built)."""
    plan = sell_plan_shadow(player) or {}
    if plan.get("day") != day:
        return 0
    total = 0
    for line in (plan.get("lines") or {}).values():
        q = line.get("qty_today", 0) if isinstance(line, dict) else 0
        if isinstance(q, (int, float)) and q > 0:
            total += int(q)
    return total


def _execute_routes(obs, farm, private, day, routes):
    """L4 mechanical executor (scheduler §4 full spec; enabled at M4).

    Walk-along-route semantics with F4 skip, D1-ETA and EOD-projection
    assertions, the idempotent REPLAN gate and the inline d29 DROP->SELL
    liquidation.  Finished stops (F4) are reported through _EXEC_DONE_MEM
    for the dispatcher's adaptive rebuild.  Returns (actions, replan);
    the dispatcher (_solve_and_execute) consumes this directly.
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer",
                        [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    hour = _get(obs, "hour", 0)
    tile_map = _executor_tiles(farm)
    inventories = _get(private, "inventories", []) or []
    actions = []
    done_keys = []
    replan = False
    player = _get(obs, "player", 0)
    is_last_day = day >= SEASON_DAYS - 1
    shed = _get(private, "shed", {}) or {}
    shed_total = sum(int(v) for v in shed.values()
                     if isinstance(v, (int, float)) and v > 0)
    accesses = sorted(_shed_access(board, _get(
        farm, "unlocked_quadrants", ["NW"]) or ["NW"])) if board else []
    for ui in range(len(units)):
        route = routes[ui] if ui < len(routes or []) else None
        pos = units[ui]
        inv = inventories[ui] if ui < len(inventories) else {}
        carried = {item: int(amount) for item, amount in (inv or {}).items()
                   if isinstance(amount, (int, float)) and amount > 0}
        if is_last_day and carried:
            carried_total = sum(carried.values())
            room = max(0, SHED_CAPACITY - shed_total)
            if not accesses or room < carried_total:
                actions.append(["PASS"])
                continue
            if not _shed_adjacent(pos[0], pos[1], board):
                sx, sy = min(accesses, key=lambda p: (
                    _dist(pos[0], pos[1], p[0], p[1]), p[0], p[1]))
                dx = 1 if sx > pos[0] else (-1 if sx < pos[0] else 0)
                dy = 1 if sy > pos[1] else (-1 if sy < pos[1] else 0)
                actions.append(["EAST"] if dx > 0 else ["WEST"] if dx < 0
                               else ["SOUTH"] if dy > 0 else ["NORTH"])
                continue
            actions.append(["DROP"])
            queued = _D29_SELL_QUEUE.setdefault(player, {})
            for item in sorted(carried):
                queued[item] = queued.get(item, 0) + carried[item]
                shed_total += carried[item]
            continue
        # a unit beyond the solved roster (hand materialized after the
        # solve) PASSes this turn; the next current-roster re-solve absorbs it
        if route is None:
            actions.append(["PASS"])
            continue
        # solver routes carry full stop dicts under "tasks"; hand-built
        # routes (tests) keep plain dicts under "stops"
        stops = route.get("tasks") or route.get("stops") or []
        if not stops:
            actions.append(["PASS"])
            continue
        idx = 0
        # F4: skip at-station stops whose tile state is already finished;
        # F8: skip stops this unit cannot legally serve (missing the
        # carried item -- a no-wheat FEED is a silent wasted turn)
        while idx < len(stops):
            target = stops[idx]
            tx, ty = target["x"], target["y"]
            if pos != (tx, ty):
                break
            item = target.get("need")
            if item and _get(inv, item, 0) <= 0:
                idx += 1
                continue
            if _stop_done(tile_map.get((tx, ty)), target.get("act"), day):
                if target.get("key") is not None:
                    done_keys.append(target.get("key"))
                idx += 1
            else:
                break
        if idx >= len(stops):
            actions.append(["PASS"])
            continue
        target = stops[idx]
        tx, ty = target["x"], target["y"]
        if pos == (tx, ty):
            actions.append(list(target.get("act") or ["PASS"]))
        else:
            dx = 0 if tx == pos[0] else (1 if tx > pos[0] else -1)
            dy = 0 if ty == pos[1] else (1 if ty > pos[1] else -1)
            if dx:
                actions.append(["EAST"] if dx > 0 else ["WEST"])
            else:
                actions.append(["SOUTH"] if dy > 0 else ["NORTH"])
        if EXECUTOR_D1_ASSERT:
            eta = hour
            ex, ey = pos
            for pending in stops[idx:]:
                eta += _dist(ex, ey, pending["x"], pending["y"]) + 1
                deadline = pending.get("deadline")
                is_d1 = pending.get("tier") == "D1" or pending.get("red")
                if pending.get("tier") is None and deadline is not None:
                    is_d1 = True
                if is_d1 and deadline is not None and eta > deadline:
                    replan = True
                    break
                ex, ey = pending["x"], pending["y"]
    # assertion: EOD budget projection (F6 auto-return destroys overflow).
    # True forward projection since the aggressive wave B (2026-09-04):
    # current shed + carried + route-remaining HARVEST inflow - today's
    # planned sell lines.  On the dawn turn the sell plan does not exist
    # yet, so the sell term is 0 there; a premature trip is suppressed by
    # the idempotent gate and self-heals on the next turn.
    if EXECUTOR_EOD_ASSERT:
        shed = _get(private, "shed", {}) or {}
        inventories = _get(private, "inventories", []) or []
        eod_total = sum(int(v) for v in shed.values()
                        if isinstance(v, (int, float)) and v > 0)
        for inv in inventories:
            if inv:
                eod_total += sum(int(v) for v in inv.values()
                                 if isinstance(v, (int, float)) and v > 0)
        eod_total += _remaining_harvest_inflow(routes, tile_map, day)
        eod_total -= _planned_sell_today(player, day)
        if eod_total > SHED_CAPACITY:
            replan = True
    _EXEC_DONE_MEM[player] = {"day": day, "keys": done_keys}
    if replan and not _replan_gate(player, day, routes):
        replan = False        # idempotent gate: same plan -> stop rebuilding
    return actions, replan
