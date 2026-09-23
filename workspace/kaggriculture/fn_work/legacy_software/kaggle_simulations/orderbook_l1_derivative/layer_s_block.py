"""layer S 尾块模板（R10 运行时五函数的代码真值）。

被 append_layer_s_block 抽取源码注入 L1 main.py 尾部；独立可导入供
orderbook_l1_derivative/test_layer_s.py 单测（测试代码=上发代码，零漂移）。
契约见 fn_docs/hybrid/responsibility.md【R10 增补】。"""

# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）
_CXS_FROM = 648
_CXS_SEASON_END = 718

# 首收步数表（R9/bots 常数看护先例；wheel 现值交叉校验见 test_consts_crosscheck.py）
# 来源（2026-09-23 实读转录）：本机 vendored wheel kaggle_environments 1.32.7+nodeps，
#   模块 kaggle_environments/envs/kaggriculture/kaggriculture.py 模块级 CROPS 表的
#   first_yield_day 字段（单位=天）。换算式（1 天 = turnsPerDay 默认 24 步；719 步/30 天）：
#   FIRST_HARVEST_STEPS[crop] = CROPS[crop]["first_yield_day"] * 24
# 口径：从 PLANT 那步起到第一次 HARVEST 可得那步的步数差。引擎 day = step // 24，
#   PLANT 记 planted_day=当日，HARVEST 合法条件 day - planted_day >= first_yield_day
#   （kaggriculture.py L453），故"种下→首收"相隔 first_yield_day 整天 = *24 步级；
#   WHEAT/CARROT = 2 天 = 48 步，与契约预期一致。
FIRST_HARVEST_STEPS: dict = {
    "WHEAT": 48,        # first_yield_day=2  → 2*24
    "CARROT": 48,       # first_yield_day=2  → 2*24
    "TOMATO": 192,      # first_yield_day=8  → 8*24
    "STRAWBERRY": 240,  # first_yield_day=10 → 10*24
    "MELON": 240,       # first_yield_day=10 → 10*24
}


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
    """纯时间测试：step+first_harvest(crop)≤718；常数缺失/异常→True（保守不截）。

    step s 的 crop PLANT 可完成"种+收" ⇔ s + first_harvest_steps(crop) ≤
    _CXS_SEASON_END(718)。first_harvest_steps=None 时用模块级
    FIRST_HARVEST_STEPS；表缺失/作物不在表/任何类型或运行异常 → True
    （零误杀：不确定=来得及=不构成截断理由）。
    """
    try:
        table = FIRST_HARVEST_STEPS if first_harvest_steps is None else first_harvest_steps
        return step + table[crop] <= _CXS_SEASON_END
    except Exception:
        return True
