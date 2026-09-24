"""R15 Phase M 市场地图法证—骨架桩（fn-scaffold）。职责规约见 fn_docs/hybrid/responsibility.md 【R15 增补】。"""
def phase_m_market_map(replay_dir):
    """86 局逐日品项价/量/供给全景→市场地图+置换对排序；零合格对→KILLED 依据。"""
    raise NotImplementedError("unimplemented:fn:phase_m_market_map")


def item_price_percentile(daily_tables):
    """单品项全程价格分位轨迹+崩价/稀缺结构判定。"""
    raise NotImplementedError("unimplemented:fn:item_price_percentile")


def rank_swap_pairs(item_stats):
    """崩价品×稀缺品置换对按（分位差×可置换产能）排序+产能窗图谱。"""
    raise NotImplementedError("unimplemented:fn:rank_swap_pairs")
