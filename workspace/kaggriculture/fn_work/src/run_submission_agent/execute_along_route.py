"""L4 执行（沿线行走+到站动作+F4 跳过+D1/EOD 断言+幂等 REPLAN 门+d29 DROP→SELL），按现状迁移，断言失败走 fail-open。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def execute_along_route(routes: dict, obs: dict) -> list:
    raise NotImplementedError("unimplemented:fn:execute_along_route")
