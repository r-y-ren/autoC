"""L1 宏观三模式+WHEAT_FARM 关+_plan_rollout 偿付门+阶段寄存器（P0-P5/d1/d6/d10/d14/d22/fuse/backfill）+_field_alloc 分区轮作；stage_* 四键显式化为保留轴（值面不变）。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def decide_macro_mode(registry: dict, cash: float, herd: dict, step: int) -> tuple:
    raise NotImplementedError("unimplemented:fn:decide_macro_mode")
