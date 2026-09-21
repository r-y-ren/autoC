"""官方装载语义下的单回合入口（obs→观察旁路→黎明钩子→宏计划→任务→四层求解→市场→雇工→排序→预算截断），内部异常全吞降级为 PASS，与现役行为逐字节等价。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def run_submission_agent(obs: dict) -> dict:
    raise NotImplementedError("unimplemented:fn:run_submission_agent")
