"""市场层（引擎镜像定价/三门卖出/MK-3 批次/MK-5 载体/sellrace 前移旗关/买地饲料种子畜群四重门/committed_spend），按现状迁移；_note_buys 死 shim 不迁。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def plan_market_orders(inventory: dict, price_projection: dict, budget: dict) -> list:
    raise NotImplementedError("unimplemented:fn:plan_market_orders")
