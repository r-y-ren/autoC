"""从回放任意步以显式 me_seat 重建双席状态并推演（修复原恒 seat0 注入），幂等/指纹校验语义保留。

上游: R2（详见 fn_docs/responsibility.md）
"""


def rollout_with_replay_opponent(replay, injection_point, agent_callable, me_seat: int) -> list:
    raise NotImplementedError("unimplemented:fn:rollout_with_replay_opponent")
