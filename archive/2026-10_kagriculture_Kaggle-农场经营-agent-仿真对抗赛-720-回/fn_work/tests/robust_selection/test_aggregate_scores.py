# test_aggregate_scores.py —— aggregate_scores 自有单测（R3 值序裁切）
# ===========================================================================
# 覆盖（fn_docs/responsibility.md robust_selection/aggregate_scores 条目）：
#   ① 值序反例集——构造与期望值逐字复刻自 snapshot_tests/
#      test_counterexample_r3.py（65.0 / 22.5 / 55.0·62.5 三例），测试数据
#      全部字面构造，不 import 旧树；
#   ② 对照断言——名字序旧值（35.0 / 60.0 / 双 60.0 零效力）在新实现下
#      必须不再成立，反例集在新实现下取值序结果；
#   ③ trim=0 与全保留边界（floor 下取整边界、n=1 退化、最大裁切钳位）；
#   ④ 空集抛 ValueError；
#   ⑤ 旗面/参数约定不变——worst_case / weighted 语义与校验异常面。
# ===========================================================================

import pytest

from robust_selection.aggregate_scores import aggregate_scores

WB = "frozen_style_pool:winner_balanced"
WS = "frozen_style_pool:wheat_suppressor"
PE = "passive_extrapolation"
PF = "pessimistic_fill"

# 反例集逐字复刻自 snapshot_tests/test_counterexample_r3.py（期望值=值序裁切）
CASE_A = {WB: 60.0, WS: 100.0, PE: 10.0, PF: 70.0}
CASE_B = {WB: 80.0, WS: 5.0, PE: 40.0, PF: 1.0}
LO = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
HI = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}


# --------------------------------------------------------------------------
# ① 值序反例集（R3 快照反例三例，期望值=值序裁切）
# --------------------------------------------------------------------------

def test_value_order_case_a():
    # 值序 [10,60,70,100] → 裁 {10,100} → 保留 [60,70] → 65.0
    # （名字序 [100,60,10,70] → 裁 {100,70} → 保留 [60,10] → 35.0，旧缺陷值）
    assert aggregate_scores(CASE_A) == 65.0


def test_value_order_case_b_pessimistic_restored():
    # 值序 [1,5,40,80] → 裁 {1,80} → 保留 [5,40] → 22.5（悲观信号恢复效力）
    assert aggregate_scores(CASE_B) == 22.5


def test_pessimistic_score_moves_aggregate_under_value_order():
    # 值序：LO → 裁 {10,70} 保留 [50,60] → 55.0；
    #       HI → 裁 {50,70} 保留 [60,65] → 62.5。两者必须不同。
    assert aggregate_scores(LO) == 55.0
    assert aggregate_scores(HI) == 62.5
    assert aggregate_scores(LO) != aggregate_scores(HI)


# --------------------------------------------------------------------------
# ② 对照断言：名字序旧值在新实现下不再成立（反例集=值序结果，非旧值）
# --------------------------------------------------------------------------

def test_name_order_old_values_rejected():
    assert aggregate_scores(CASE_A) != 35.0    # 名字序旧值（旧码现行输出）
    assert aggregate_scores(CASE_B) != 60.0    # 名字序旧值
    # 旧"悲观模型零效力"（lo==hi==60.0）在值序裁切下必须失效
    assert not (aggregate_scores(LO) == aggregate_scores(HI) == 60.0)


def test_input_dict_order_irrelevant():
    # 确定性：键入顺序不影响聚合值（值序裁切的直接推论）
    assert aggregate_scores(CASE_A) == aggregate_scores(dict(reversed(list(CASE_A.items()))))


# --------------------------------------------------------------------------
# ③ trim=0 与全保留边界
# --------------------------------------------------------------------------

def test_trim_zero_is_plain_mean():
    # trim_fraction=0 → floor(4×0)=0 → 全保留 → 普通均值 240/4=60.0
    assert aggregate_scores(CASE_A, trim_fraction=0.0) == 60.0


def test_floor_boundary_keeps_all():
    # n=4、frac=0.1 → floor(0.4)=0 → 全保留（下取整边界）；均值仍 60.0
    assert aggregate_scores(CASE_A, trim_fraction=0.1) == 60.0
    # n=2、frac=0.25 → floor(0.5)=0 → 两值全保留 → (1+3)/2=2.0
    assert aggregate_scores({WS: 1.0, PF: 3.0}) == 2.0


def test_single_model_returns_value():
    # n=1 → trim 钳位为 0 → 退化为该值（全保留下界）
    assert aggregate_scores({PF: 42.5}) == 42.5


def test_max_trim_clamp_keeps_one():
    # n=5、frac=0.4 → floor(2.0)=2=min(2,(5-1)//2) → 每端各裁 2，仅留中位 3.0
    scores = {WS: 1.0, WB: 2.0, PE: 3.0, PF: 4.0, "passive_mirror": 5.0}
    assert aggregate_scores(scores, trim_fraction=0.4) == 3.0


# --------------------------------------------------------------------------
# ④ 空集抛
# --------------------------------------------------------------------------

def test_empty_scores_raises():
    with pytest.raises(ValueError, match="空 scores"):
        aggregate_scores({})


# --------------------------------------------------------------------------
# ⑤ 旗面/参数约定不变（策略面与校验异常面与旧码一致）
# --------------------------------------------------------------------------

def test_strategy_surface_unchanged():
    assert aggregate_scores(CASE_A, strategy="worst_case") == 10.0
    assert aggregate_scores(CASE_B, strategy="worst_case") == 1.0
    weights = {WB: 0.1, WS: 0.2, PE: 0.3, PF: 0.4}
    assert aggregate_scores(CASE_A, strategy="weighted",
                            weights=weights) == (0.1 * 60.0 + 0.2 * 100.0
                                                 + 0.3 * 10.0 + 0.4 * 70.0)


def test_parameter_validation_raises():
    with pytest.raises(ValueError, match="不在"):
        aggregate_scores(CASE_A, strategy="mean")
    with pytest.raises(ValueError, match="trim_fraction"):
        aggregate_scores(CASE_A, trim_fraction=0.5)
    with pytest.raises(ValueError, match="策略需要 weights"):
        aggregate_scores(CASE_A, strategy="weighted")
    with pytest.raises(ValueError, match="缺模型键"):
        aggregate_scores(CASE_A, strategy="weighted", weights={WB: 1.0})
