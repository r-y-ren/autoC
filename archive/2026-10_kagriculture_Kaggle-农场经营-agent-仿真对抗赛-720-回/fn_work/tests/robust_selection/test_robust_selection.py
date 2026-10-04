# ===========================================================================
# test_robust_selection.py —— robust_selection 主流程单测
# ---------------------------------------------------------------------------
# 反例与冻结锚点语义复刻自 snapshot_tests/test_counterexample_r3.py 与
# test_planner_select_characterization.py（全部字面构造，不 import 旧树）：
#   CASE_A  值序裁切 kept=[60,70]→65.0（旧名字序缺陷值 35.0）
#   CASE_HI 值序裁切 kept=[60,65]→62.5（旧名字序缺陷值 60.0）
#   K1 锚点 challenger 值序聚合 1003.0 对 identity_hold=1000.0 边际 3.0 <
#           tau×1000=5.0 → 恒选守成点（ranking 保持原序）。
# ===========================================================================

import pytest

from robust_selection.robust_selection import robust_selection

WB = "frozen_style_pool:winner_balanced"
WS = "frozen_style_pool:wheat_suppressor"
PE = "passive_extrapolation"
PF = "pessimistic_fill"

# 值序修复语义（复刻 test_counterexample_r3.py 构造，字面）：
CASE_A = {WB: 60.0, WS: 100.0, PE: 10.0, PF: 70.0}   # 值序 65.0（名字序缺陷 35.0）
CASE_HI = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}   # 值序 62.5（名字序缺陷 60.0）


def test_end_to_end_value_order_fix_selects_correct_plan():
    # ① 值序语义下 alpha=65.0 > beta=62.5 → 选 plan_alpha；
    #   旧名字序缺陷口径会得 alpha=35.0 < beta=60.0 → 误选 plan_beta。
    j_matrix = {"plan_alpha": dict(CASE_A), "plan_beta": dict(CASE_HI)}
    result = robust_selection(j_matrix)
    assert result["best"] == "plan_alpha"
    assert result["aggregates"] == {"plan_alpha": 65.0, "plan_beta": 62.5}
    assert result["ranking"] == [("plan_alpha", 65.0), ("plan_beta", 62.5)]


def test_k1_identity_gate_picks_identity_when_margin_below_tau():
    # ② K1 近平守成（复刻 characterization 冻结用例，值序口径）：
    #   challenger 聚合 1003.0（值序 kept=[1002,1004]）对 identity_hold
    #   =1000.0 边际 3.0 < tau×1000=5.0 → 恒选守成点，ranking 保持原序。
    j_matrix = {
        "identity_hold": {WB: 1000.0, WS: 1000.0, PE: 1000.0, PF: 1000.0},
        "challenger": {WB: 999.0, WS: 1002.0, PE: 1004.0, PF: 1005.0},
    }
    result = robust_selection(j_matrix, identity_key="identity_hold")
    assert result["best"] == "identity_hold"
    assert result["aggregates"] == {"challenger": 1003.0,
                                    "identity_hold": 1000.0}
    assert result["ranking"][0] == ("challenger", 1003.0)
    assert result["tie_break"] is not None
    assert "K1 近平守成" in result["tie_break"]
    assert "'identity_hold'" in result["tie_break"]


def test_k1_gate_strict_less_boundary_keeps_argmax():
    # ②补边界：边际恰等于 gate（margin == tau×|identity|）不切换（严格小于）。
    j_matrix = {
        "identity_hold": {WB: 100.0, WS: 100.0, PE: 100.0, PF: 100.0},
        "challenger": {WB: 99.5, WS: 100.5, PE: 100.5, PF: 200.0},
    }
    # challenger 值序 kept=[100.5,100.5]→100.5，边际 0.5 == 0.005×100 → 不守成。
    result = robust_selection(j_matrix, identity_key="identity_hold")
    assert result["best"] == "challenger"
    assert result["tie_break"] is None


def test_result_keys_aggregates_and_tie_note_complete():
    # ③ 返回结构键完整 + 平票注记：同分双计划并列 → key 字典序最小者胜。
    j_matrix = {"b_plan": dict(CASE_A), "a_plan": dict(CASE_A)}
    result = robust_selection(j_matrix)
    assert set(result) == {"best", "ranking", "strategy", "tie_break",
                           "aggregates"}
    assert result["best"] == "a_plan"
    assert result["strategy"] == "trimmed_mean"
    assert result["aggregates"] == {"a_plan": 65.0, "b_plan": 65.0}
    assert result["ranking"] == [("a_plan", 65.0), ("b_plan", 65.0)]
    assert result["tie_break"] is not None
    assert "2 个计划聚合值并列 65.0" in result["tie_break"]
    assert "'a_plan'" in result["tie_break"]
    # 聚合参数透传（worst_case=min，逐计划悲观下界）：
    wc = robust_selection({"p": {WB: 1.0, WS: 2.0, PE: 3.0, PF: 4.0},
                           "q": {WB: 5.0, WS: 6.0, PE: 7.0, PF: 8.0}},
                          strategy="worst_case")
    assert wc["strategy"] == "worst_case"
    assert wc["aggregates"] == {"p": 1.0, "q": 5.0}
    assert wc["best"] == "q"


def test_empty_matrix_raises():
    # ④ 空矩阵抛带失败示例的显式异常。
    with pytest.raises(ValueError, match="空"):
        robust_selection({})
