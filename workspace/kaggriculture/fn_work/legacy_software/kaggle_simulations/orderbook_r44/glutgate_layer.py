# 件 B 谷底闸门运行时层（纯减法；磁带基座原卖单豁免）
def _glutgate_agent(observation, configuration=None):
    """运行时包装：捕获宿主末 callable→gate_added_sells 过滤→返回；异常→原动作；step==0 复位"""
    raise NotImplementedError("unimplemented:fn:_glutgate_agent")
def gate_added_sells(observation, action, added_marks):
    """谷底闸门：我方层加挂 SELL 逐单判 quote<base_of(item) 即删；磁带原卖单豁免不动；删除台账留痕。错误: 标记缺失→保守视作磁带单=不删"""
    raise NotImplementedError("unimplemented:fn:gate_added_sells")
