# r45 判决线（镜像压力板+反制臂；realized_price_stats 复用不立桩）
def judge_r45(package, corpus, config):
    """判决 v28：镜像压力板（克隆/指纹≥0.95 局专组）+Wool Front-Runner 反制臂+26 败局重演+胜局对照；五判据=净加卖恒等违例 0∧镜像胜率≥0.55∧实现价不降∧反制不翻车∧h2h≥0.55。输出: evidence JSON / 错误: 单局红计入不短路"""
    raise NotImplementedError("unimplemented:fn:judge_r45")
def verify_net_identity(traces, ledger):
    """净量恒等核验：逐局逐品对账'提前卖出量=到期抵扣量'，违例计数（判据=0）+明细。错误: 台账缺失→违例计 1（fail-closed）"""
    raise NotImplementedError("unimplemented:fn:verify_net_identity")
def run_mirror_counter_judgment(package, board_config):
    """压力面执行：镜像压力板+反制臂局组编排（seated 双席位、独立 seed n 报）。错误: 组不可跑→fail-closed 记红"""
    raise NotImplementedError("unimplemented:fn:run_mirror_counter_judgment")
