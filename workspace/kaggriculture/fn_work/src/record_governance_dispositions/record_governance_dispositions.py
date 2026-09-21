"""治理处置记录编排（双源归源/蓝图失效声明/active_candidate 降级），产出 fn_docs 处置记录。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）
"""


def record_governance_dispositions(disposition_list: list) -> None:
    raise NotImplementedError("unimplemented:fn:record_governance_dispositions")
