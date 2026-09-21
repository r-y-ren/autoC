"""active_candidate.json 降级历史台账的处置记录与时点闸（动作本身=09-30 收口后执行，时点未到即拒绝执行动作、只许记录）。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）
"""


def demote_active_candidate_ledger(current_snapshot: dict) -> dict:
    raise NotImplementedError("unimplemented:fn:demote_active_candidate_ledger")
