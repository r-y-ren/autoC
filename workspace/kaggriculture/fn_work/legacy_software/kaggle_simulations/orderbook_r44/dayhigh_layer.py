# 件 A 日内新高变现运行时层（注入候选尾块；fail-open 三道）
def _dayhigh_agent(observation, configuration=None):
    """运行时包装：捕获宿主末 callable→取基座动作→detect_dayhigh→plan_dayhigh_sells→并入市场单列表+台账；异常→原动作；step==0 复位跟踪器"""
    raise NotImplementedError("unimplemented:fn:_dayhigh_agent")
def detect_dayhigh(ctx, base_action, tracker):
    """当日严格新高判定（7 品；quote<2 永不触发；父链在卖该品不触发）。输入: quote_context+基座动作+跟踪器 / 输出: 触发品集合 / 错误: 异常→空集"""
    raise NotImplementedError("unimplemented:fn:detect_dayhigh")
def plan_dayhigh_sells(trigger_items, inventory, market_orders):
    """追加单计划：可卖量=在仓可卖−本步已挂同品；price×qty 降序；并入最早同品 SELL 槽/不能并置首个花费单前；10 槽满弃追加。输出: 追加单+槽位安排+台账 / 错误: 库存不确定→该品零追加"""
    raise NotImplementedError("unimplemented:fn:plan_dayhigh_sells")
