"""arena._abnormal_reason 与 eval_contract.game_abnormal_reason 合并为单一实现（字段集分叉对齐后取并集语义）。

上游: R8, R9（详见 fn_docs/responsibility.md）
"""

from typing import Optional


def merge_abnormal_reason(game_record: dict) -> Optional[str]:
    raise NotImplementedError("unimplemented:fn:merge_abnormal_reason")
