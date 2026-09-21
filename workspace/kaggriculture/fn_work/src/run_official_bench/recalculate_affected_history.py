"""对 G1 受影响历史结论用 seated 通道重算，产出双口径台账（局号/错位历史值 vs seated 重算值/结论是否翻转），单条失败记 SKIP 留因不中断。

上游: R2（详见 fn_docs/responsibility.md）
"""


def recalculate_affected_history(affected_conclusions: list) -> dict:
    raise NotImplementedError("unimplemented:fn:recalculate_affected_history")
