# ===========================================================================
# 【中文·模块导览】src/executor.py —— L4 机械执行器（M4 起 LIVE，v1.3 全规格）
# ---------------------------------------------------------------------------
# 职责：沿路线逐站"到站且 tile 态未完成→发动作，否则走一步"（F1 曼哈顿
#   步进精确；F4 重复 WATER/FEED 是静默浪费，发射前查 tile 态跳过已完成
#   站；F8 缺 need 物品的站跳过——无麦 FEED 是静默 no-op）；
# 断言（只读，§5 proved-or-flagged）：
#   * D1 站点 ETA ≤ deadline（EXECUTOR_D1_ASSERT）；
#   * EOD 投影 Σ(棚仓+随身) ≤ SHED_CAPACITY（F6：随身日终自动归还、超容
#     销毁——唯一静默损失源由 §2.4 前置消化，此处复核，EXECUTOR_EOD_ASSERT）；
# 断言失败 → REPLAN：派发器当回合以现世界重建一次（每回合现役重解使重
#   建有界不循环），_replan_gate 幂等闸保留为护栏（F7 下正确实现永不触发）。
# d29 模板（F10）：早收→DROP（查 room）→SELL 随身清零；卖出单进
#   _D29_SELL_QUEUE 供市场层接线。
# M4/M5 沿革：2026-09-02 Phase-B 切换 → M5 审计发现接线缺陷（结果字典当
#   路线表传入，~97% 回合异常）→ 2026-09-03 M3 v3（现役船员重解）修复后
#   四层成为唯一执行路径，v72 与执行开关随 M5 冻结删除。
# PLACE 站点完成判据修复（M4 门普查发现：空畜栏被误判"已完成"，买入的
#   牲畜囤在棚仓永不安置）。

_REPLAN_MEM = {}
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


def _stop_done(tile, act):
    """F4 dedup: a repeated WATER/FEED is a silent wasted turn; skip stops
    whose tile state shows the work already finished."""
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
        return _get(tile, "fertilized_until_day", -1) is not None \
            and _get(tile, "fertilized_until_day", 0) > 0
    if op == "DIG":
        return _get(tile, "kind", "") != "WEED"
    if op == "HARVEST":
        return _get(tile, "yield_units", 1) <= 0
    return False


def _d29_template(obs, farm, private):
    """d29 liquidation template (§4.2 / F10): walk to the shed mouth, DROP
    respecting room, queue SELL for everything dropped (carried goods
    cannot be sold in place).  Returns (actions, sell_items)."""
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer",
                        [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    accesses = sorted(_shed_access(board, _get(farm, "unlocked_quadrants",
                                               ["NW"]) or ["NW"])) \
        if board else []
    shed = _get(private, "shed", {}) or {}
    shed_total = sum(int(v) for v in shed.values()
                     if isinstance(v, (int, float)) and v > 0)
    inventories = _get(private, "inventories", []) or []
    actions = []
    sell = {}
    for ui, pos in enumerate(units):
        inv = inventories[ui] if ui < len(inventories) else {}
        carried = {k: int(v) for k, v in (inv or {}).items()
                   if isinstance(v, (int, float)) and v > 0}
        if not carried or not accesses:
            actions.append(["PASS"])
            continue
        if not _shed_adjacent(pos[0], pos[1], board):
            sx, sy = min(accesses, key=lambda p: (
                _dist(pos[0], pos[1], p[0], p[1]), p[0], p[1]))
            dx = 1 if sx > pos[0] else (-1 if sx < pos[0] else 0)
            dy = 1 if sy > pos[1] else (-1 if sy < pos[1] else 0)
            if dx:
                actions.append(["EAST"] if dx > 0 else ["WEST"])
            else:
                actions.append(["SOUTH"] if dy > 0 else ["NORTH"])
            continue
        # engine canonical form: BARE ["DROP"] -- the engine drops EVERY
        # carried item respecting room per item (overflow destroyed); we
        # only mirror what FITS into the sell queue
        actions.append(["DROP"])
        room = max(0, SHED_CAPACITY - shed_total)
        for item in sorted(carried):
            if room <= 0:
                break
            moved = min(carried[item], room)
            if moved > 0:
                sell[item] = sell.get(item, 0) + moved
                shed_total += moved
                room -= moved
    return actions, sell


def _execute_routes(obs, farm, private, day, routes):
    """L4 mechanical executor (scheduler §4 full spec; enabled at M4).

    Walk-along-route semantics with F4 skip, D1-ETA and EOD-projection
    assertions, the idempotent REPLAN gate and the d29 DROP->SELL template.
    Returns (actions, replan); the dispatcher (_solve_and_execute)
    consumes this directly.
    """
    player = _get(obs, "player", 0)
    if day >= SEASON_DAYS - 1:
        actions, sell = _d29_template(obs, farm, private)
        if sell:
            _D29_SELL_QUEUE[player] = sell
        return actions, False

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
    replan = False
    for ui in range(len(units)):
        route = routes[ui] if ui < len(routes or []) else None
        # a unit beyond the solved roster (hand materialized after the
        # solve) PASSes this turn; the next current-roster re-solve
        # absorbs it
        if route is None:
            actions.append(["PASS"])
            continue
        # solver routes carry full stop dicts under "tasks"; hand-built
        # routes (tests) keep plain dicts under "stops"
        stops = route.get("tasks") or route.get("stops") or []
        pos = units[ui]
        inv = inventories[ui] if ui < len(inventories) else {}
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
            if _stop_done(tile_map.get((tx, ty)), target.get("act")):
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
        # assertion: D1 stop still reachable before its deadline
        if EXECUTOR_D1_ASSERT:
            deadline = target.get("deadline")
            if deadline is not None:
                eta = hour + _dist(pos[0], pos[1], tx, ty) + 1
                if eta > deadline:
                    replan = True
    # assertion: EOD budget projection (F6 auto-return destroys overflow)
    if EXECUTOR_EOD_ASSERT:
        shed = _get(private, "shed", {}) or {}
        inventories = _get(private, "inventories", []) or []
        eod_total = sum(int(v) for v in shed.values()
                        if isinstance(v, (int, float)) and v > 0)
        for inv in inventories:
            if inv:
                eod_total += sum(int(v) for v in inv.values()
                                 if isinstance(v, (int, float)) and v > 0)
        if eod_total > SHED_CAPACITY:
            replan = True
    if replan and not _replan_gate(player, day, routes):
        replan = False        # idempotent gate: same plan -> stop rebuilding
    return actions, replan
