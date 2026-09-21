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
# ===========================================================================

import pytest

from kaggle_simulations.agent.planner.select import (
    AGGREGATION_STRATEGIES,
    DEFAULT_TRIM_FRACTION,
    IDENTITY_TIEBREAK_TAU,
    aggregate_scores,
    robust_select,
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
    # 现行行为：按名字序裁切。Ω=4 → trim=floor(4*0.25)=1，
    # 名字序值向量 [100.0(ws), 60.0(wb), 10.0(pe), 70.0(pf)]
    # → kept=values[1:3]=[60.0, 10.0] → 35.0。
    assert aggregate_scores(CASE_A) == 35.0


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
    # G2/R3 的行为后果：pessimistic_fill 名字序恒最后 → 恒被裁。
    # 只改 pessimistic 分数（10.0 → 65.0，跨越保留段），聚合值纹丝不动。
    p1 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    p2 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    # 名字序 [ws:60, wb:50, pe:70, pf:*] → kept=[50.0, 70.0] → 60.0。
    assert aggregate_scores(p1) == 60.0
    assert aggregate_scores(p2) == 60.0
    # 对照：worst_case 聚合能感知 pessimistic 变动（缺陷仅在 trimmed_mean）。
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
        # 名字序 [ws:30, wb:20, pe:25, pf:22] → kept=[20,25] → 22.5。
        "plan_expand_herd": {WB: 20.0, WS: 30.0, PE: 25.0, PF: 22.0},
    }
    result = robust_select(j_matrix)
    assert result["best"] == "anchor_conservative"
    assert result["aggregates"] == {"anchor_conservative": 35.0,
                                    "plan_expand_herd": 22.5}
    assert result["ranking"] == [("anchor_conservative", 35.0),
                                 ("plan_expand_herd", 22.5)]
    assert result["strategy"] == "trimmed_mean"
    assert result["tie_break"] is None


def test_robust_select_tie_breaks_on_lexicographic_key():
    j_matrix = {"b_plan": dict(CASE_A), "a_plan": dict(CASE_A)}
    result = robust_select(j_matrix)
    assert result["best"] == "a_plan"
    assert result["tie_break"] is not None
    assert "2 个计划聚合值并列 35.0" in result["tie_break"]
    assert "'a_plan'" in result["tie_break"]


def test_robust_select_identity_tiebreak_k1_gate():
    # K1 近平守成：challenger 聚合 1001.5（名字序 kept=[wb:999, pe:1004]）
    # 对 identity_hold=1000.0 边际 1.5 < tau*1000=5.0 → 恒选守成点。
    j_matrix = {
        "identity_hold": {WB: 1000.0, WS: 1000.0, PE: 1000.0, PF: 1000.0},
        "challenger": {WB: 999.0, WS: 1002.0, PE: 1004.0, PF: 1005.0},
    }
    result = robust_select(j_matrix, identity_key="identity_hold")
    assert result["aggregates"] == {"challenger": 1001.5,
                                    "identity_hold": 1000.0}
    assert result["best"] == "identity_hold"
    assert result["tie_break"] is not None
    assert "K1 近平守成" in result["tie_break"]
    # ranking 保持原序（守成裁决不改 ranking）。
    assert result["ranking"][0] == ("challenger", 1001.5)


def test_robust_select_input_order_independent():
    # 输入 dict 顺序不影响结果（全排序显式键）。
    items = [("z_plan", dict(CASE_A)), ("a_plan", {WB: 20.0, WS: 30.0,
                                                   PE: 25.0, PF: 22.0})]
    r1 = robust_select(dict(items))
    r2 = robust_select(dict(reversed(items)))
    assert r1 == r2
