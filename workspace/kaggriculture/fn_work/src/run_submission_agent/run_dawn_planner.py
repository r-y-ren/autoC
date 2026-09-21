"""黎明 DTSP 钩子（预算治理→摘要→枚举≤120→投影×Ω4→robust_selection→rollout 阶梯→τ 双闸→注入/快照/幂等缓存；wave 候选恒排比较集首位），三道 fail-open 语义不变。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def run_dawn_planner(obs: dict, remaining_budget: dict) -> dict:
    raise NotImplementedError("unimplemented:fn:run_dawn_planner")
