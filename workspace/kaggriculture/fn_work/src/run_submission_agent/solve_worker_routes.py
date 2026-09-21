"""L3 路线求解（EDF+价值密度+2-opt 抛光+载货腿+D1 兜尾+自适应 REPLAN），按现状迁移；死件 _two_opt_segment/_dawn_crew_size/_schedule_units 不迁。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def solve_worker_routes(missions: list, workers: dict, capacity: dict) -> dict:
    raise NotImplementedError("unimplemented:fn:solve_worker_routes")
