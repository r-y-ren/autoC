# test_break_ties_by_identity.py —— K1 近平守成 tie-break 行为固化（B2）
# ===========================================================================
# 钉什么：fn_work/src/robust_selection/break_ties_by_identity.py 的当前输出。
# 源语义=旧树 software/kaggle_simulations/agent/planner/select.py 的
# robust_select K1 守成闸片段（行为不变迁移，无修复项）；冻结锚点=
# snapshot_tests/test_planner_select_characterization.py
# test_robust_select_identity_tiebreak_k1_gate（K1 边际 1.5 < tau×1000=5.0
# → 恒选守成点）。本文件按迁移约定**字面构造**用例（直接给聚合值 dict），
# 不 import 旧树。
# 边界值浮点精确性（2026-09-21 实测）：0.005×1000.0 == 5.0、
# 1005.0-1000.0 == 5.0，边界断言无浮点噪声。
# ===========================================================================

from robust_selection.break_ties_by_identity import (
    IDENTITY_TIEBREAK_TAU,
    break_ties_by_identity,
)


def test_tau_constant_frozen():
    # 旧码模块常量冻结（characterization test_module_constants_frozen 同锚）。
    assert IDENTITY_TIEBREAK_TAU == 0.005


def test_identity_near_tie_within_tau_selects_identity():
    # ① 近平差 0.4%：challenger 1004.0 对 identity 1000.0，边际 4.0 <
    # tau×1000=5.0 → 恒选守成点。
    aggregates = {"challenger": 1004.0, "identity_hold": 1000.0}
    assert break_ties_by_identity(
        aggregates, identity_key="identity_hold") == "identity_hold"


def test_margin_beyond_tau_keeps_higher_score():
    # ② 差 0.6%：边际 6.0 ≥ 5.0 → 保留高分 challenger。
    aggregates = {"challenger": 1006.0, "identity_hold": 1000.0}
    assert break_ties_by_identity(
        aggregates, identity_key="identity_hold") == "challenger"


def test_boundary_at_tau_strict_less_than_does_not_switch():
    # ③ 边界 τ：边际恰等 gate（1005.0-1000.0 == 0.005×1000 == 5.0），
    # 旧码严格小于 `if margin < gate` → 不切换，保留 challenger。
    aggregates = {"challenger": 1005.0, "identity_hold": 1000.0}
    assert break_ties_by_identity(
        aggregates, identity_key="identity_hold") == "challenger"


def test_k1_characterization_margin_1_5_below_gate_5_0():
    # ③ 复刻 characterization 冻结用例（字面构造，不 import 旧树）：
    # K1 边际 1.5 < tau×1000=5.0 → 恒选守成点 identity_hold。
    aggregates = {"challenger": 1001.5, "identity_hold": 1000.0}
    assert break_ties_by_identity(
        aggregates, identity_key="identity_hold") == "identity_hold"


def test_identity_absent_returns_argmax():
    # ④ identity 缺席：identity_key=None（关闭守成，P2.6 行为）与
    # identity_key 不在 aggregates 内均原样返回 argmax，不抛错。
    aggregates = {"challenger": 1006.0, "other": 900.0}
    assert break_ties_by_identity(aggregates) == "challenger"
    assert break_ties_by_identity(
        aggregates, identity_key="identity_hold") == "challenger"


def test_identity_already_best_returned_unchanged():
    # 最优即 identity：守成闸条件 best_key != identity_key 不成立，原样返回。
    assert break_ties_by_identity(
        {"identity_hold": 1000.0, "other": 999.0},
        identity_key="identity_hold") == "identity_hold"


def test_gate_floor_for_small_identity_values():
    # 旧码 gate = tau×max(1.0, |identity|) 地板语义：|identity|<1 时退化为
    # 绝对阈值 tau=0.005——边际 0.004 切换、0.006 保留。
    assert break_ties_by_identity(
        {"challenger": 0.004, "identity_hold": 0.0},
        identity_key="identity_hold") == "identity_hold"
    assert break_ties_by_identity(
        {"challenger": 0.006, "identity_hold": 0.0},
        identity_key="identity_hold") == "challenger"


def test_non_identity_tie_breaks_on_lexicographic_key():
    # 旧码 ranking 规则继承：聚合值并列的非 identity 计划按 key 字典序取
    # 最小（"a_plan" < "b_plan"），输入 dict 顺序不影响结果。
    r1 = break_ties_by_identity(
        {"b_plan": 1006.0, "a_plan": 1006.0}, identity_key="identity_hold")
    r2 = break_ties_by_identity(
        {"a_plan": 1006.0, "b_plan": 1006.0}, identity_key="identity_hold")
    assert r1 == r2 == "a_plan"
