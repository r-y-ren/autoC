# 债务账本式卖提前运行时层（三件套之提前+账本；净量恒等硬不变量）
def _advance_agent(observation, configuration=None):
    """运行时包装：逐回合 settle_debts 先结账→select_advanceable→apply_advance_with_debt（门内）→台账；异常→原动作；step==0 复位账本"""
    raise NotImplementedError("unimplemented:fn:_advance_agent")
def select_advanceable(observation, tape_plan_view, ledger):
    """可提前量判定：磁带计划内≤k 拍∧已入仓∧quote≥2∧quote≥base∧非 dawn 拍∧非同拍 BUY_PRODUCT∧非当天 PICKUP 品∧非首计划卖单保护品；视界 clamp(measure_rival_lead+12,40,48)；窗口 192-695 外零动作。错误: 计划视图解析失败→空集"""
    raise NotImplementedError("unimplemented:fn:select_advanceable")
def apply_advance_with_debt(advance_orders, action, ledger):
    """提前执行+记账：插队首+等额记债到原 due_step（净量恒等）；台账逐笔。错误: 记账失败→该笔不提前"""
    raise NotImplementedError("unimplemented:fn:apply_advance_with_debt")
def settle_debts(action, ledger):
    """债务结算：due_step 从该品磁带卖单按债量抵扣（只减不加；债量>单量→清零+溢出告警）；跨步防重复。错误: 账本异常→不抵扣（不双卖优先）"""
    raise NotImplementedError("unimplemented:fn:settle_debts")
def measure_rival_lead(observation_history):
    """对手提前量：公开库存差分反推 rival_sold（删失口径 $1 地板只记下界）；输出近窗最大 lead（拍数）。错误: 数据不足→默认 40"""
    raise NotImplementedError("unimplemented:fn:measure_rival_lead")
