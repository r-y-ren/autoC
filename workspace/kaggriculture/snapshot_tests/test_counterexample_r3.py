# test_counterexample_r3.py —— trimmed_mean 名字序裁切 vs 值序裁切反例（R3 快照反例）
# ===========================================================================
# 缺陷（requirements.md R3 / 行为清单 G2）：select.py:42 的
#   values = [float(v) for _, v in sorted(scores.items())]
# 按模型**名字序**排序后做 trim，裁掉的序统计量与值大小无关 → 悲观模型
# （pessimistic_fill 名字序恒最后）恒被裁，投影段折扣零效力。
# 正确语义：按**值序**裁切（sort values，两端各裁 floor(n×frac) 个）。
#
# 本文件构造"名字序裁切 ≠ 值序裁切"的分数集，断言**值序裁切**的正确
# 聚合结果——旧代码上该断言失败（strict xfail，套件仍绿）；新结构修复
# 后 XPASS 会让 strict 套件变红 = 提示 R3 已修、应把本反例与
# test_planner_select_characterization.py 的冻结值一起迁移更新。
# 同时保留一个普通断言固化旧代码当前行为（名字序），保绿并作为差分
# 对照面。
# ===========================================================================

import pytest

from kaggle_simulations.agent.planner.select import aggregate_scores

WB = "frozen_style_pool:winner_balanced"
WS = "frozen_style_pool:wheat_suppressor"
PE = "passive_extrapolation"
PF = "pessimistic_fill"


def _value_order_trimmed_mean(scores, trim_fraction=0.25):
    """R3 修复后的正确语义参照实现（值序裁切），仅测试内使用。

    n=4、frac=0.25 → 两端各裁 1 个：去掉最大值与最小值，取剩余均值。
    """
    import math
    values = sorted(float(v) for v in scores.values())
    n = len(values)
    trim = min(math.floor(n * trim_fraction), (n - 1) // 2)
    kept = values[trim:n - trim] if trim else values
    return sum(kept) / len(kept)


# 反例集 A：名字序=[ws:100, wb:60, pe:10, pf:70]
#   名字序裁切 → 裁 {ws=100, pf=70} → 保留 [60, 10] → 35.0（现行输出）
#   值序裁切   → 裁 {10, 100}       → 保留 [60, 70] → 65.0（正确输出）
CASE_A = {WB: 60.0, WS: 100.0, PE: 10.0, PF: 70.0}

# 反例集 B：悲观模型给出全场最低分，名字序裁切把它（而非真正的最小值
# 所在的 wheat_suppressor=5.0）裁掉：
#   名字序=[ws:5, wb:80, pe:40, pf:1] → 裁 {ws=5, pf=1} → 保留 [80,40] → 60.0
#   值序   → 裁 {1, 80} → 保留 [5, 40] → 22.5（悲观信号恢复效力）
CASE_B = {WB: 80.0, WS: 5.0, PE: 40.0, PF: 1.0}


@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：旧 select.py 按名字序裁切（悲观模型恒被裁），"
           "新结构改为值序裁切后此测试应 XPASS")
def test_value_order_trimmed_mean_case_a():
    assert aggregate_scores(CASE_A) == 65.0


@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：旧 select.py 按名字序裁切（悲观模型恒被裁），"
           "新结构改为值序裁切后此测试应 XPASS")
def test_value_order_trimmed_mean_case_b_pessimistic_restored():
    assert aggregate_scores(CASE_B) == 22.5


@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：值序裁切下悲观模型分数变动必须改变聚合值；"
           "旧代码（名字序恒裁 pessimistic_fill）无感，新结构应 XPASS")
def test_pessimistic_score_moves_aggregate_under_value_order():
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    # 值序：lo → 裁 {10,70} 保留 [50,60] → 55.0；
    #       hi → 裁 {50,70} 保留 [60,65] → 62.5。两者必须不同。
    assert aggregate_scores(lo) == 55.0
    assert aggregate_scores(hi) == 62.5
    assert aggregate_scores(lo) != aggregate_scores(hi)


# ---------------------------------------------------------------------------
# 对照断言：旧代码当前行为（名字序裁切），普通断言保绿。
# 修复 R3 时这三条会变红——届时按 README 迁移约定更新冻结值。
# ---------------------------------------------------------------------------

def test_current_name_order_behavior_case_a():
    assert aggregate_scores(CASE_A) == 35.0


def test_current_name_order_behavior_case_b():
    assert aggregate_scores(CASE_B) == 60.0


def test_current_pessimistic_zero_effect():
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    assert aggregate_scores(lo) == aggregate_scores(hi) == 60.0


def test_reference_implementation_sanity():
    # 测试内参照实现自检：与手算冻结值一致（防参照实现本身写错）。
    assert _value_order_trimmed_mean(CASE_A) == 65.0
    assert _value_order_trimmed_mean(CASE_B) == 22.5
