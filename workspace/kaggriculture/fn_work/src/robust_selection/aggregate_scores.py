"""逐计划聚合对手分数：按分数值序排序后裁切 trim 端点再聚合（修复原字典序裁切缺陷），聚合量与旗面不变。

上游: R3（详见 fn_docs/responsibility.md）
"""


def aggregate_scores(opponent_scores: dict, trim) -> float:
    raise NotImplementedError("unimplemented:fn:aggregate_scores")
