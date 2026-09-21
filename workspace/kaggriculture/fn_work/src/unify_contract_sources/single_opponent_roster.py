"""对手名册单源真值（11 对手池+网格口径），bots/__init__×2、STANDARD_MATRIX_ORDER、EXPECTED_ELO_ORDER、holdout_matrix_order、REQUIRED_OPPONENTS 全部改为引用。

上游: R8, R9（详见 fn_docs/responsibility.md）
"""


def single_opponent_roster() -> dict:
    raise NotImplementedError("unimplemented:fn:single_opponent_roster")
