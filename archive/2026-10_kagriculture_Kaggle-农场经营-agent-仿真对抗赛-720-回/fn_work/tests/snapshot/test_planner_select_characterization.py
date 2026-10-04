# test_planner_select_characterization.py —— select.py 聚合/选择器行为固化（R1 基线）
# ===========================================================================
# 钉什么：software/kaggle_simulations/agent/planner/select.py 的
#   aggregate_scores / robust_select 在固定分数字典上的**当前输出**。
#   Ω=4 的真实模型名取自 planner/opponents.py（build_default_models）：
#     passive_extrapolation / frozen_style_pool:winner_balanced /
#     frozen_style_pool:wheat_suppressor / pessimistic_fill
# 名字序事实（本测试固化的核心）：sorted(scores.items()) 按模型名排序为
#   wheat_suppressor < winner_balanced < passive_extrapolation < pessimistic_fill
#   （'h'<'i'），n=4、trim_fraction=0.25 时每端裁 1 个 → 被裁的恰是
#   {wheat_suppressor, pessimistic_fill}——**与值无关**。悲观模型
#   （pessimistic_fill，名字序恒最后）在 trimmed_mean 聚合中恒被裁掉，
#   其分数变动对聚合值零影响（下方 test_pessimistic_fill_zero_effect 钉住）。
# 这就是 requirements.md R3 所述"现行名字序裁切行为"——R1 基线的一部分：
# 新结构修值序前，这些逐值断言必须原样跑绿；修值序后本文件随之更新
# （迁移约定见 README.md）。
# 冻结值全部手算复核（2026-09-21，Python 3.14.7 实测一致）。
# ---------------------------------------------------------------------------
# 【迁移记录 2026-09-21 · migrate_snapshot_suite（W1 收口）】本文件随套件
# 迁入 fn_work/tests/snapshot/：select 断言重定向至 fn_work/src/
# robust_selection（R3 值序裁切），受影响冻结值按值序口径刷新、逐处双
# 口径注记；其余冻结值（模块常量/worst_case/weighted/退化尺寸/输入
# 校验/K1 守成语义）不变。旧 snapshot_tests/ 原件不动（仍钉名字序旧值）。
# ===========================================================================

import pytest

# 【R3 重定向·迁移】select 实现 → fn_work/src/robust_selection（值序
# 裁切修复所在包）；函数名 robust_select→robust_selection（对齐包名，
# 调用点随迁改名）；受影响冻结值按值序口径刷新，逐处双口径注记。
from robust_selection.aggregate_scores import (
    AGGREGATION_STRATEGIES,
    DEFAULT_TRIM_FRACTION,
    aggregate_scores,
)
from robust_selection.robust_selection import (
    IDENTITY_TIEBREAK_TAU,
    robust_selection,
)

# 真实 Ω=4 模型名（opponents.build_default_models 的 J 矩阵键）。
WB = "frozen_style_pool:winner_balanced"
WS = "frozen_style_pool:wheat_suppressor"
PE = "passive_extrapolation"
PF = "pessimistic_fill"

# 名字序裁切的代表例：名字序=[ws:100, wb:60, pe:10, pf:70] → 裁
# {ws, pf} → 保留 [wb=60, pe=10] → (60+10)/2 = 35.0。
# 值序裁切（R3 修复后的正确语义）应为保留 [60,70] → 65.0（见
# test_counterexample_r3.py）。
CASE_A = {WB: 60.0, WS: 100.0, PE: 10.0, PF: 70.0}


def test_module_constants_frozen():
    assert AGGREGATION_STRATEGIES == ("trimmed_mean", "worst_case", "weighted")
    assert DEFAULT_TRIM_FRACTION == 0.25
    assert IDENTITY_TIEBREAK_TAU == 0.005


def test_aggregate_trimmed_mean_name_order_cut():
    # 【双口径注记】旧值 35.0（名字序裁切：值向量 [100.0(ws), 60.0(wb),
    # 10.0(pe), 70.0(pf)] → kept=[60.0,10.0]）/ 新值 65.0（值序裁切：
    # 排序 [10,60,70,100] → kept=[60,70]）/ 原因=R3 修复。
    assert aggregate_scores(CASE_A) == 65.0


def test_aggregate_worst_case_and_weighted():
    assert aggregate_scores(CASE_A, strategy="worst_case") == 10.0
    # 权重取二进制精确分数（0.125/0.25/0.5），冻结值无浮点噪声：
    # (0.125*60 + 0.25*100 + 0.125*10 + 0.5*70) / 1.0 = 68.75
    assert aggregate_scores(
        CASE_A, strategy="weighted",
        weights={WB: 0.125, WS: 0.25, PE: 0.125, PF: 0.5}) == 68.75


def test_aggregate_degenerate_sizes():
    # n=1：trim=min(0, 0)=0 → 该值本身。
    assert aggregate_scores({PF: 42.5}) == 42.5
    # n=2：trim=min(floor(2*0.25)=0, 0)=0 → 双值均值。
    assert aggregate_scores({"a": 1.0, "b": 3.0}) == 2.0


def test_pessimistic_fill_zero_effect_under_name_order_cut():
    # 【双口径注记】旧值 p1==p2==60.0（G2/R3 行为后果：pessimistic_fill
    # 名字序恒最后 → 恒被裁，只改 pessimistic 分数聚合纹丝不动）/
    # 新值 p1=55.0、p2=62.5 且 p1!=p2（值序：p1 排序 [10,50,60,70] →
    # kept=[50,60]；p2 排序 [50,60,65,70] → kept=[60,65]——悲观分数
    # 恢复效力）/ 原因=R3 修复。
    p1 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    p2 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    assert aggregate_scores(p1) == 55.0
    assert aggregate_scores(p2) == 62.5
    assert aggregate_scores(p1) != aggregate_scores(p2)
    # 对照（值不变）：worst_case 聚合感知 pessimistic 变动。
    assert aggregate_scores(p1, strategy="worst_case") == 10.0
    assert aggregate_scores(p2, strategy="worst_case") == 50.0


def test_aggregate_input_validation_frozen():
    with pytest.raises(ValueError, match="空 scores"):
        aggregate_scores({})
    with pytest.raises(ValueError, match="不在"):
        aggregate_scores({PF: 1.0}, strategy="mean")
    with pytest.raises(ValueError, match="需要 weights"):
        aggregate_scores({PF: 1.0}, strategy="weighted")
    with pytest.raises(ValueError, match="缺模型键"):
        aggregate_scores({PF: 1.0, PE: 2.0}, strategy="weighted",
                         weights={PF: 1.0})
    with pytest.raises(ValueError, match="trim_fraction"):
        aggregate_scores({PF: 1.0}, trim_fraction=0.5)


def test_robust_select_ranking_and_aggregates_frozen():
    j_matrix = {
        "anchor_conservative": dict(CASE_A),
        # 【双口径注记】plan_expand_herd 旧值 22.5（名字序 [ws:30, wb:20,
        # pe:25, pf:22] → kept=[20,25]）/ 新值 23.5（值序 [20,22,25,30] →
        # kept=[22,25]）。
        "plan_expand_herd": {WB: 20.0, WS: 30.0, PE: 25.0, PF: 22.0},
    }
    result = robust_selection(j_matrix)
    # 【双口径注记】anchor_conservative 旧值 35.0 / 新值 65.0（值序裁切，
    # CASE_A 同源）/ 原因=R3 修复；排序与 best 结论不变（65.0 > 23.5）。
    assert result["best"] == "anchor_conservative"
    assert result["aggregates"] == {"anchor_conservative": 65.0,
                                    "plan_expand_herd": 23.5}
    assert result["ranking"] == [("anchor_conservative", 65.0),
                                 ("plan_expand_herd", 23.5)]
    assert result["strategy"] == "trimmed_mean"
    assert result["tie_break"] is None


def test_robust_select_tie_breaks_on_lexicographic_key():
    j_matrix = {"b_plan": dict(CASE_A), "a_plan": dict(CASE_A)}
    result = robust_selection(j_matrix)
    assert result["best"] == "a_plan"
    assert result["tie_break"] is not None
    # 【双口径注记】并列聚合值旧值 35.0 / 新值 65.0（值序裁切）/
    # 原因=R3 修复；决胜语义不变（key 字典序取 'a_plan'）。
    assert "2 个计划聚合值并列 65.0" in result["tie_break"]
    assert "'a_plan'" in result["tie_break"]


def test_robust_select_identity_tiebreak_k1_gate():
    # K1 近平守成：【双口径注记】challenger 聚合旧值 1001.5（名字序
    # kept=[999,1004]）/ 新值 1003.0（值序排序 [999,1002,1004,1005] →
    # kept=[1002,1004]）；对 identity_hold=1000.0 边际旧 1.5 / 新 3.0，
    # 均 < tau*1000=5.0 → 恒选守成点（K1 冻结语义不变）/ 原因=R3 修复。
    j_matrix = {
        "identity_hold": {WB: 1000.0, WS: 1000.0, PE: 1000.0, PF: 1000.0},
        "challenger": {WB: 999.0, WS: 1002.0, PE: 1004.0, PF: 1005.0},
    }
    result = robust_selection(j_matrix, identity_key="identity_hold")
    assert result["aggregates"] == {"challenger": 1003.0,
                                    "identity_hold": 1000.0}
    assert result["best"] == "identity_hold"
    assert result["tie_break"] is not None
    assert "K1 近平守成" in result["tie_break"]
    # ranking 保持原序（守成裁决不改 ranking）。
    assert result["ranking"][0] == ("challenger", 1003.0)


def test_robust_select_input_order_independent():
    # 输入 dict 顺序不影响结果（全排序显式键；无值变化，仅调用名随迁）。
    items = [("z_plan", dict(CASE_A)), ("a_plan", {WB: 20.0, WS: 30.0,
                                                   PE: 25.0, PF: 22.0})]
    r1 = robust_selection(dict(items))
    r2 = robust_selection(dict(reversed(items)))
    assert r1 == r2
