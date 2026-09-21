"""对手供给四通道日账（精确流发布/残差降信/钱账分解/tile 记账）与 est_* getter，按现状迁移，通道失败降信不抛。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def observe_opponent_state(obs: dict, step: int) -> None:
    raise NotImplementedError("unimplemented:fn:observe_opponent_state")
