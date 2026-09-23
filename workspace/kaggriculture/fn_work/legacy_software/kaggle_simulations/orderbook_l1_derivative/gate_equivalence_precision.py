"""gate_equivalence_precision（R10 门③）：等价面+精准性三合一裁决。"""


def run(episodes_dir, l1_main, verbatim_main) -> dict:
    """(a)重演逐字节 (b)子集判据 (c)构造用例 →{equiv, subset, cases}；任一红即门红。"""
    raise NotImplementedError("unimplemented:fn:gate_equivalence_precision")


def replay_action_diff(replay_path, l1_main, verbatim_main) -> dict:
    """单局重演 diff：差异仅允许 BUY_SEED 消失形态；其他差异报首个位置。"""
    raise NotImplementedError("unimplemented:fn:replay_action_diff")


def precision_subset_check(replay_products) -> dict:
    """逐局逐品项：被截断购种量 ≤ 原版终局未种下量；violation 非空即红。"""
    raise NotImplementedError("unimplemented:fn:precision_subset_check")


def constructed_invariant_cases() -> dict:
    """三构造用例：有机会不截/无机会截/s671 边界磁带确无后续种植才截。"""
    raise NotImplementedError("unimplemented:fn:constructed_invariant_cases")
