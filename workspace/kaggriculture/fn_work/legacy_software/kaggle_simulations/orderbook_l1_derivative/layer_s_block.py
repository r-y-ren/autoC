"""layer S 尾块模板（R10 运行时五函数的代码真值）。

被 append_layer_s_block 抽取源码注入 L1 main.py 尾部；独立可导入供
orderbook_l1_derivative/test_layer_s.py 单测（测试代码=上发代码，零漂移）。
契约见 fn_docs/hybrid/responsibility.md【R10 增补】。"""

# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）
_CXS_FROM = 648
_CXS_SEASON_END = 718

# 首收步数表：实现期从 vendored wheel CROPS_INFO 转录并加交叉校验测试（R9/bots 常数看护先例）
FIRST_HARVEST_STEPS: dict = {}  # unimplemented:const:FIRST_HARVEST_STEPS


def _cxs_agent(observation, configuration=None):
    """运行时入口：捕获 last-callable 基座→取动作→step≥648 交截断；异常回退基座动作。"""
    raise NotImplementedError("unimplemented:fn:_cxs_agent")


def _cxs_seed_truncate(observation, action, plan_view):
    """纯减法过滤：逐品项按允许删除量删超额 BUY_SEED；品项不确定(None)→零截断。"""
    raise NotImplementedError("unimplemented:fn:_cxs_seed_truncate")


def _cxs_seed_surplus(crop, observation, kept_orders, plan_view):
    """零误杀核心：surplus=库存+保留单+磁带未来购买−可完成需求；解析失败→None。"""
    raise NotImplementedError("unimplemented:fn:_cxs_seed_surplus")


def _cxs_completable_plant_demand(crop, observation, plan_view):
    """逐品项未来可完成种+收的 PLANT 种子需求；plan_view 解析失败→None。"""
    raise NotImplementedError("unimplemented:fn:_cxs_completable_plant_demand")


def _cxs_harvest_completable(step, crop, first_harvest_steps=None):
    """纯时间测试：step+first_harvest(crop)≤718；常数缺失/异常→True（保守不截）。"""
    raise NotImplementedError("unimplemented:fn:_cxs_harvest_completable")
