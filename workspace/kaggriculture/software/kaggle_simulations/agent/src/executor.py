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
    """M4 placeholder: per-turn mechanical execution + read-only assertions.

    Contract (scheduler §4): every worker standing on a station whose tile
    state is unfinished emits its action, else steps toward the next stop
    (no mid-season return legs, engine fact F6); d29 runs the DROP->SELL
    template; assertions (read-only, millisecond scale) verify D1
    completion-or-ETA and the EOD shed-budget projection; any failure
    triggers REPLAN-for-the-day with an idempotent gate (stop rebuilding
    when the rebuilt plan equals the old one).
    """
    raise NotImplementedError("L4 executor lands at M4 (scheduler design §7)")
