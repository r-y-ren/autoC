# ===========================================================================
# 【中文·模块导览】src/telemetry.py —— 影子遥测旁路（M1 记分卡扩展点）
# ---------------------------------------------------------------------------
# v10.9 职责：只观测不干预的诊断通道（_telemetry_* 系列 + 公共 API
#   set_telemetry_enabled/set_telemetry_sink/reset_telemetry/
#   telemetry_snapshot + scheduler_trace），sink 异常全吞，诊断永不弄废
#   提交回合。
# 新架构落位：scheduler 设计 §7 M1 记分卡的宿主——现有字段
#   （pass_count/cross_quadrant_switches/overdue 等）即 M1 基线雏形。
# 文档符合性审查：
#   ✓ 旁路性与 fail-open 契约在场（与 OBS 观测器同一工程模式）；
#   ✗ 待办（M1）——按 cls 完成率/D1 超期数/连续性口径/EOD 溢出量/
#     分类别"回合/资产单位"系数（容量定律定标的数据源，scheduler §2.6；
#     定标同时裁决开放问题：C1 的 crew 15 是否过量配置）。
# ===========================================================================

# --------------------------------------------------------------------------
# v9 local shadow telemetry (stdlib-only, action-transparent)
# --------------------------------------------------------------------------
# 【中文】本地"影子遥测"：只观测、不干预的纯旁路诊断通道。调用方可关闭
# 或注入 sink；sink 抛异常被吞掉，诊断永远不允许弄废一个提交回合。
# 以下 _telemetry_* 系列函数均服务于此目的，与策略决策完全解耦。
# Telemetry is deliberately a side channel.  It never mutates the observation,
# planner inputs, or returned action.  A caller may disable it or inject a
# process-local sink for replay tooling; a failing sink is ignored so a
# diagnostic cannot invalidate a submission turn.

TELEMETRY_ENABLED = True
_TELEMETRY_SINK = None
_TELEMETRY = {"players": {}}


def set_telemetry_enabled(enabled):
    """Enable/disable local shadow telemetry without changing strategy output."""
    global TELEMETRY_ENABLED
    TELEMETRY_ENABLED = bool(enabled)


def set_telemetry_sink(sink):
    """Inject a callable receiving one JSON-like turn event, or clear it."""
    global _TELEMETRY_SINK
    _TELEMETRY_SINK = sink if callable(sink) else None


def reset_telemetry():
    """Drop in-memory episode/day records and the optional sink reference."""
    global _TELEMETRY, _TELEMETRY_SINK
    _TELEMETRY = {"players": {}}
    _TELEMETRY_SINK = None


def telemetry_snapshot():
    """Return a detached snapshot suitable for local JSON serialization."""
    return copy.deepcopy(_TELEMETRY)


def _telemetry_day_template():
    return {
        "turns": 0,
        "moving_turns": 0,
        "effective_ops": 0,
        "valid_operations": 0,
        "movement_to_effective_ratio": 0.0,
        "pass_count": 0,
        "repeated_tasks": 0,
        "cross_quadrant_switches": 0,
        "cross_quadrant_choices": 0,
        "overdue": {"WATER": 0, "FEED": 0, "CARE": 0},
        "water_overdue": 0,
        "feed_overdue": 0,
        "care_overdue": 0,
        "zone_tasks_completed": {},
        "wheat_alive": 0,
        "wheat_harvested": 0,
        "external_feed_bought": 0,
        "minimum_cash": None,
        "shed_overflow": 0,
        "terminal_clearout": False,
        # ---- M1 scorecard (scheduler design §7 / §2.6, 2026-09-02) ----
        # ops_by_type: per-turn unit-op counts by op -- the numerator of the
        # per-asset-class turn coefficients that calibrate the capacity law
        # (24x(1+H)x0.75/2.4, branch plan §5.3).
        "ops_by_type": {},
        # asset_units: straw/wheat/melon tile=1, carrot=0.5, head=2 (the
        # capacity-law denominator), plus its raw components.
        "asset_units": 0.0,
        "asset_components": {"straw": 0, "wheat": 0, "melon": 0,
                             "carrot": 0, "herd": 0},
        "weed_tiles": 0,
        "herd_head": 0,
        # ---- M1/M2 scorecard: dawn mission shadow (scheduler §2/§7) ----
        # mission_hash is the M2 golden-hash anchor; d1_count/tier_counts
        # feed the cls-completion and D1-overdue scorecards; cap_util is
        # the capacity-law utilization band (branch §10.2, 65%-85%).
        "mission_hash": None,
        "d1_count": 0,
        "tier_counts": {},
        "cap_util": None,
        "cap_deficit": False,
        # ---- branch W2: fuse / backfill / peak-day (§8.2/§5.3/§2.6) ----
        "fused": False,
        "fuse_events": 0,
        "backfill_room": None,
        "peak_ok": None,
    }


def _telemetry_player(player, day, hour):
    """Get a player-local telemetry state, resetting on a backwards clock."""
    key = str(player)
    state = _TELEMETRY["players"].get(key)
    if state is None or day < state.get("last_day", day) or (
            day == state.get("last_day", day) and
            hour < state.get("last_hour", hour)):
        state = {
            "episode": state.get("episode", 0) + 1 if state else 1,
            "last_day": day,
            "last_hour": hour,
            "last_task": {},
            "last_sector": {},
            "minimum_cash": None,
            "shed_overflow": 0,
            "wheat_harvested": 0,
            "external_feed_bought": 0,
            "days": {},
        }
        _TELEMETRY["players"][key] = state
    state["last_day"] = day
    state["last_hour"] = hour
    state["days"].setdefault(str(day), _telemetry_day_template())
    return state, state["days"][str(day)]


_TELEMETRY_UNIT_OPS = {
    "NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST",
    "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "FEED", "CARE",
    "COLLECT_FERTILIZER", "PICKUP", "DROP", "PLACE", "PASS",
}


def _telemetry_wheat_alive(farm):
    count = 0
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT" \
                    and _get(tile, "crop", "") == "WHEAT":
                count += 1
    return count


def _telemetry_inventory_total(private):
    total = 0
    for item, amount in (_get(private, "shed", {}) or {}).items():
        if isinstance(amount, (int, float)) and amount > 0:
            total += amount
    for inv in (_get(private, "inventories", []) or []):
        for item, amount in (inv or {}).items():
            if isinstance(amount, (int, float)) and amount > 0:
                total += amount
    return total


def _telemetry_units(farm):
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    units.extend(tuple(h) for h in (_get(farm, "hands", []) or []))
    return units, board


def _telemetry_record_turn(obs, farm, private, actions, tasks, trace, orders):
    """Record one observed decision and its planner shadow facts.

    Values are intentionally marked by the observation/action boundary: order
    quantities and task completions are requests visible locally before the
    engine applies them; wheat survival, cash, and shed pressure are observed
    state values from the same observation.
    """
    if not TELEMETRY_ENABLED:
        return
    try:
        player = _get(obs, "player", 0)
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        state, daily = _telemetry_player(player, day, hour)
        units, board = _telemetry_units(farm)
        operations = 0
        moving = 0
        passes = 0
        completed = {}
        wheat_harvested = 0
        action_targets = (trace or {}).get("action_targets", {})
        assigned = (trace or {}).get("assign", {})
        for ui, action in enumerate(actions or []):
            if not action:
                continue
            op = action[0]
            if op in MOVES:
                moving += 1
            elif op == "PASS":
                passes += 1
            elif op in _TELEMETRY_UNIT_OPS:
                operations += 1
                position = action_targets.get(ui)
                if position is None and ui < len(units):
                    position = units[ui]
                if position is not None and board:
                    zone = _quadrant_of(position[0], position[1], board)
                    completed[zone] = completed.get(zone, 0) + 1
                    if op == "HARVEST" and 0 <= position[1] < len(
                            _get(farm, "tiles", [])):
                        tile = _get(farm, "tiles", [])[position[1]][position[0]]
                        if isinstance(tile, dict) and \
                                _get(tile, "crop", "") == "WHEAT":
                            wheat_harvested += max(1, int(
                                _get(tile, "yield_units", 0) or 0))
            task_key = assigned.get(ui)
            if task_key is not None and state["last_task"].get(str(ui)) == task_key:
                daily["repeated_tasks"] += 1
            if task_key is not None:
                state["last_task"][str(ui)] = task_key
            if ui < len(units) and board:
                sector = _quadrant_of(units[ui][0], units[ui][1], board)
                previous = state["last_sector"].get(str(ui))
                if previous is not None and previous != sector:
                    daily["cross_quadrant_switches"] += 1
                state["last_sector"][str(ui)] = sector
        daily["turns"] += 1
        daily["moving_turns"] += moving
        daily["effective_ops"] += operations
        daily["valid_operations"] += operations
        daily["pass_count"] += passes
        ratio = daily["moving_turns"] / float(max(1, daily["effective_ops"]))
        daily["movement_to_effective_ratio"] = ratio
        # M1 scorecard: ops by type + action mix (turn-coefficient numerator)
        for action in actions or []:
            if action and isinstance(action, list) and action[0]:
                op = action[0]
                if op != "PASS":
                    daily["ops_by_type"][op] = \
                        daily["ops_by_type"].get(op, 0) + 1
        # M1 scorecard: asset units (capacity-law denominator) + weed count
        comps = {"straw": 0, "wheat": 0, "melon": 0, "carrot": 0, "herd": 0}
        weeds = 0
        for row in _get(farm, "tiles", []) or []:
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                kind = _get(tile, "kind", "")
                if kind == "PLANT":
                    crop = _get(tile, "crop", "")
                    if crop == "STRAWBERRY":
                        comps["straw"] += 1
                    elif crop == "WHEAT":
                        comps["wheat"] += 1
                    elif crop == "MELON":
                        comps["melon"] += 1
                    elif crop == "CARROT":
                        comps["carrot"] += 1
                elif kind == "WEED":
                    weeds += 1
                elif "animal" in tile:
                    comps["herd"] += 1
        daily["asset_components"] = comps
        daily["weed_tiles"] = weeds
        daily["herd_head"] = comps["herd"]
        daily["asset_units"] = float(comps["straw"] + comps["wheat"]
                                     + comps["melon"]
                                     + 0.5 * comps["carrot"]
                                     + 2 * comps["herd"])
        # M1/M2 scorecard: pull the dawn mission shadow (built once per
        # player-day by _mission_shadow_update in the entry bypass)
        try:
            mission = mission_shadow(_get(obs, "player", 0))
            if mission is not None and mission.get("day") == day:
                daily["mission_hash"] = mission.get("mission_hash")
                daily["d1_count"] = len(mission.get("d1") or [])
                daily["tier_counts"] = dict(mission.get("tier_counts") or {})
                daily["cap_util"] = (mission.get("capacity") or {}).get("util")
                daily["cap_deficit"] = \
                    mission.get("capacity_deficit") is not None
                daily["peak_ok"] = (mission.get("peak") or {}).get("ok")
        except Exception:
            pass
        # branch W2: fuse / backfill from the stage register (§8.2/§5.3)
        try:
            stage_state = stage_state_snapshot(_get(obs, "player", 0))
            daily["fused"] = bool(stage_state.get("fused"))
            daily["fuse_events"] = int(stage_state.get("fuse_events", 0))
            backfill = stage_state.get("backfill") or {}
            daily["backfill_room"] = backfill.get("room_units")
        except Exception:
            pass
        cross_choices = int((trace or {}).get("cross_quadrant", 0))
        daily["cross_quadrant_choices"] += cross_choices
        overdue = {"WATER": 0, "FEED": 0, "CARE": 0}
        for task in tasks or []:
            op = (task.get("act") or [None])[0]
            if op not in overdue:
                continue
            if task.get("red") or op == "CARE":
                overdue[op] += 1
        for op, count in overdue.items():
            daily["overdue"][op] += count
            daily[op.lower() + "_overdue"] += count
        for zone, count in completed.items():
            daily["zone_tasks_completed"][zone] = \
                daily["zone_tasks_completed"].get(zone, 0) + count

        money = _get(farm, "money", None)
        if isinstance(money, (int, float)):
            state["minimum_cash"] = money if state["minimum_cash"] is None \
                else min(state["minimum_cash"], money)
            daily["minimum_cash"] = state["minimum_cash"]
        overflow = max(0, _telemetry_inventory_total(private) - 100)
        state["shed_overflow"] = max(state["shed_overflow"], overflow)
        daily["shed_overflow"] = state["shed_overflow"]
        alive = _telemetry_wheat_alive(farm)
        state["wheat_harvested"] += wheat_harvested
        daily["wheat_alive"] = alive
        daily["wheat_harvested"] = state["wheat_harvested"]
        bought = 0
        for order in orders or []:
            if len(order) >= 3 and order[0] == "BUY_PRODUCT" \
                    and order[1] == "WHEAT" and isinstance(order[2], (int, float)):
                bought += order[2]
        state["external_feed_bought"] += bought
        daily["external_feed_bought"] = state["external_feed_bought"]
        terminal = day >= SEASON_DAYS - 1 and \
            _telemetry_inventory_total(private) <= 0 and \
            all(order and order[0] == "SELL" for order in (orders or []))
        daily["terminal_clearout"] = bool(terminal)
        episode = {
            "turns": sum(d.get("turns", 0) for d in state["days"].values()),
            "moving_turns": sum(d.get("moving_turns", 0) for d in state["days"].values()),
            "effective_ops": sum(d.get("effective_ops", 0) for d in state["days"].values()),
            "pass_count": sum(d.get("pass_count", 0) for d in state["days"].values()),
            "repeated_tasks": sum(d.get("repeated_tasks", 0) for d in state["days"].values()),
            "cross_quadrant_switches": sum(d.get("cross_quadrant_switches", 0)
                                             for d in state["days"].values()),
            "wheat_alive": alive,
            "wheat_harvested": state["wheat_harvested"],
            "external_feed_bought": state["external_feed_bought"],
            "minimum_cash": state["minimum_cash"],
            "shed_overflow": state["shed_overflow"],
            "terminal_clearout": bool(terminal),
        }
        event = {"kind": "turn", "player": player, "day": day,
                 "hour": hour, "metrics": copy.deepcopy(daily),
                 "episode": episode}
        sink = _TELEMETRY_SINK
        if sink is not None:
            try:
                sink(copy.deepcopy(event))
            except Exception:
                pass
    except Exception:
        # Diagnostics are fail-open by design.
        return
_SCHEDULER_TRACE = {}


def scheduler_trace():
    """Return the latest per-player routing decisions for local diagnostics."""
    return copy.deepcopy(_SCHEDULER_TRACE)
