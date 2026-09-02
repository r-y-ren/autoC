# 【中文】L4 机械执行器脚手架（worker_route_scheduler_design.md §4，M4 启用）。
# 本阶段仅占位：ROUTE_EXECUTOR_ENABLED=False，且没有任何模块引用
# _execute_routes —— 构建产物与 v10.9 行为完全一致。启用前置：M3 求解器
# 影子分歧收敛（§7 里程碑），届时 executor 接管逐回合发动作与断言，
# _schedule_units_v72 退役（M5 冻结删除）。
# Scaffold for the L4 mechanical executor (scheduler design §4, enabled at M4).
# Disabled placeholder: zero callers reference _execute_routes in this phase,
# so the merged main.py stays behaviour-identical to the v10.9 reference.
ROUTE_EXECUTOR_ENABLED = False


def _execute_routes(obs, farm, private, day, routes):
    """L4 mechanical executor (scheduler design §4; enabled at M4).

    Walk-along-route semantics: a worker standing on its current stop whose
    tile state is unfinished emits the stop's action, else steps one cell
    toward it (engine fact F1: movement is unobstructed, Manhattan stepping
    is exact).  Assertions (read-only, §5 proved-or-flagged): every D1
    obligation is completed or its stop is still ETA-reachable; any failure
    returns a replan request instead of micro-reassigning.

    Returns (actions, replan) -- actions is a list per unit; M4 wires this
    into agent() behind ROUTE_EXECUTOR_ENABLED.
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer",
                        [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    hour = _get(obs, "hour", 0)
    actions = []
    replan = False
    for ui, route in enumerate(routes or []):
        stops = route.get("stops") or []
        pos = units[ui] if ui < len(units) else (0, 0)
        if ui >= len(units) or not stops:
            actions.append(["PASS"])
            continue
        target = stops[0]
        tx, ty = target["x"], target["y"]
        if pos == (tx, ty):
            actions.append(list(target["act"] or ["PASS"]))
        else:
            dx = 0 if tx == pos[0] else (1 if tx > pos[0] else -1)
            dy = 0 if ty == pos[1] else (1 if ty > pos[1] else -1)
            if dx:
                actions.append(["EAST"] if dx > 0 else ["WEST"])
            else:
                actions.append(["SOUTH"] if dy > 0 else ["NORTH"])
        # assertion: D1 stop still reachable before its deadline
        deadline = target.get("deadline")
        if deadline is not None:
            eta = hour + _dist(pos[0], pos[1], tx, ty) + 1
            if eta > deadline:
                replan = True
    return actions, replan
