"""single_opponent_roster 真实测试：5 处旧定义 + 2 处 scripts 网格的字面等值锚。

锚定值 = 实现期读旧树源逐字复刻（kgenv/bots/__init__.py、kgenv/
eval_contract.py:20、kgenv/regression.py:47、kgenv/holdout_contract.py、
scripts/check_eval_contract.py:27、scripts/iterate_gate.py:52——后者不
import 旧 scripts/，纯字面锚定；旧树活值对照归顶层 unify_contract_sources）。
"""

from __future__ import annotations

from unify_contract_sources import single_opponent_roster as roster
from unify_contract_sources.single_opponent_roster import single_opponent_roster

# ---- S1/S2: kgenv/bots/__init__.py（读源复刻） ---- #
STRONG_OPPONENTS_ANCHOR = ("cow_baron", "melon_hoarder", "expansionist")
ONLINE_STYLE_OPPONENTS_ANCHOR = (
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
    "wheat_straw_monster",
    "two_quad_denser",
)

# ---- S3: kgenv/eval_contract.py:20 STANDARD_MATRIX_ORDER（读源复刻） ---- #
STANDARD_MATRIX_ORDER_ANCHOR = (
    "submission", "cow_baron", "melon_hoarder", "expansionist",
    "baseline_wheat", "greedy_carrot", "starter", "random", "pass",
)

# ---- S4: kgenv/regression.py:47 EXPECTED_ELO_ORDER（读源复刻，m1 修订序） ---- #
EXPECTED_ELO_ORDER_ANCHOR = [
    "submission",
    "baseline_wheat",
    "greedy_carrot",
    "starter",
    "pass",
    "random",
]

# ---- S5: kgenv/holdout_contract.py 各世代矩阵（读源复刻；V1=STANDARD） ---- #
HOLDOUT_MATRIX_ORDERS_ANCHOR = {
    1: STANDARD_MATRIX_ORDER_ANCHOR,
    2: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified"),
    3: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch"),
    4: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch",
        "wheat_straw_monster"),
    5: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch",
        "wheat_straw_monster", "two_quad_denser"),
}

# ---- G1: scripts/check_eval_contract.py:27 REQUIRED_OPPONENTS（m2 网格，读源复刻） ---- #
CHECK_EVAL_GRID_ANCHOR = [
    "cow_baron",
    "melon_hoarder",
    "expansionist",
    "baseline_wheat",
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
]

# ---- G2: scripts/iterate_gate.py:52 REQUIRED_OPPONENTS 组装（读源复刻） ---- #
GATE_OPPONENTS_ANCHOR = ["cow_baron", "melon_hoarder"]
GUARD_OPPONENTS_ANCHOR = ["expansionist", "baseline_wheat"]
ITERATE_GATE_REQUIRED_ANCHOR = (
    GATE_OPPONENTS_ANCHOR + GUARD_OPPONENTS_ANCHOR
    + list(ONLINE_STYLE_OPPONENTS_ANCHOR))

# ---- 种子域/座位协议/网格密度（eval_contract 与 G1 口径，读源复刻） ---- #
DEVELOPMENT_SEEDS_ANCHOR = [101, 102, 103, 104]
REGRESSION_SEEDS_ANCHOR = [201, 202, 203, 204, 205, 206, 207, 208]
SEAT_PROTOCOL_ANCHOR = ["AB", "BA"]
GRID_GAMES_PER_OPPONENT_ANCHOR = 8  # 4 seeds x 2 seats


# --------------------------------------------------------------------------- #
# 11 对手池真值本体
# --------------------------------------------------------------------------- #
def test_opponent_pool_11_truth():
    assert roster.OPPONENT_POOL_11 == tuple(ITERATE_GATE_REQUIRED_ANCHOR)
    assert len(roster.OPPONENT_POOL_11) == 11
    assert len(set(roster.OPPONENT_POOL_11)) == 11  # 无重复
    # 三站点分组集合交叉印证：池 = 强敌 3 + baseline_wheat + 线上风格 7
    assert set(roster.OPPONENT_POOL_11) == (
        set(STRONG_OPPONENTS_ANCHOR) | {"baseline_wheat"}
        | set(ONLINE_STYLE_OPPONENTS_ANCHOR))


def test_group_anchors_match_old_tree_literals():
    assert roster.STRONG_OPPONENTS == STRONG_OPPONENTS_ANCHOR          # S1
    assert roster.ONLINE_STYLE_OPPONENTS == ONLINE_STYLE_OPPONENTS_ANCHOR  # S2
    assert roster.GATE_OPPONENTS == tuple(GATE_OPPONENTS_ANCHOR)
    assert roster.GUARD_OPPONENTS == tuple(GUARD_OPPONENTS_ANCHOR)


# --------------------------------------------------------------------------- #
# 5 处旧定义的字面等值锚
# --------------------------------------------------------------------------- #
def test_standard_matrix_order_anchor():  # S3
    assert roster.STANDARD_MATRIX_ORDER == STANDARD_MATRIX_ORDER_ANCHOR
    assert len(roster.STANDARD_MATRIX_ORDER) == 9
    assert roster.STANDARD_OFFICIAL_PAIRS_COUNT == 36  # C(9,2)


def test_expected_elo_order_and_frozen_pool_anchor():  # S4
    assert list(roster.EXPECTED_ELO_ORDER) == EXPECTED_ELO_ORDER_ANCHOR
    assert set(roster.FROZEN_POOL) == set(EXPECTED_ELO_ORDER_ANCHOR)


def test_holdout_matrix_orders_anchor():  # S5
    assert set(roster.HOLDOUT_MATRIX_ORDERS) == {1, 2, 3, 4, 5}
    for gen, anchor in HOLDOUT_MATRIX_ORDERS_ANCHOR.items():
        assert roster.HOLDOUT_MATRIX_ORDERS[gen] == anchor, gen
    assert len(roster.HOLDOUT_MATRIX_ORDERS[2]) == 9
    assert len(roster.HOLDOUT_MATRIX_ORDERS[3]) == 10
    assert len(roster.HOLDOUT_MATRIX_ORDERS[4]) == 11
    assert len(roster.HOLDOUT_MATRIX_ORDERS[5]) == 12
    # 世代递进 = 前世代扩一员（r3-1/r5-P6/v7.1 加入序）
    for gen in (3, 4, 5):
        prev = list(roster.HOLDOUT_MATRIX_ORDERS[gen - 1])
        assert list(roster.HOLDOUT_MATRIX_ORDERS[gen])[:-1] == prev, gen


# --------------------------------------------------------------------------- #
# 网格口径（G1 九对手网格 + 种子域 + 座位协议 + 密度）
# --------------------------------------------------------------------------- #
def test_grid_anchor():
    assert list(roster.GRID_REQUIRED_OPPONENTS) == CHECK_EVAL_GRID_ANCHOR
    assert len(roster.GRID_REQUIRED_OPPONENTS) == 9
    # m2 网格 = 11 池减 r5-P6/v7.1 两员（加入晚于网格冻结）
    assert set(roster.GRID_REQUIRED_OPPONENTS) == (
        set(roster.OPPONENT_POOL_11) - {"wheat_straw_monster",
                                        "two_quad_denser"})


def test_seed_domains_and_seat_protocol_anchors():
    assert list(roster.DEVELOPMENT_SEEDS) == DEVELOPMENT_SEEDS_ANCHOR
    assert list(roster.REGRESSION_SEEDS) == REGRESSION_SEEDS_ANCHOR
    assert list(roster.SEAT_PROTOCOL) == SEAT_PROTOCOL_ANCHOR
    assert roster.GRID_GAMES_PER_OPPONENT == GRID_GAMES_PER_OPPONENT_ANCHOR
    assert roster.GRID_GAMES_PER_OPPONENT == (
        len(roster.DEVELOPMENT_SEEDS) * len(roster.SEAT_PROTOCOL))


def test_auxiliary_ladder_anchor():
    assert roster.AUXILIARY_LADDER_OPPONENTS == (
        "greedy_carrot", "starter", "random", "pass")
    assert set(roster.STANDARD_MATRIX_ORDER) == (
        {"submission"} | set(roster.STRONG_OPPONENTS) | {"baseline_wheat"}
        | set(roster.AUXILIARY_LADDER_OPPONENTS))


# --------------------------------------------------------------------------- #
# 真值快照 dict
# --------------------------------------------------------------------------- #
def test_roster_dict_snapshot():
    truth = single_opponent_roster()
    assert truth["opponent_pool_11"] == roster.OPPONENT_POOL_11
    assert truth["strong_opponents"] == STRONG_OPPONENTS_ANCHOR
    assert truth["online_style_opponents"] == ONLINE_STYLE_OPPONENTS_ANCHOR
    assert truth["standard_matrix_order"] == STANDARD_MATRIX_ORDER_ANCHOR
    assert list(truth["expected_elo_order"]) == EXPECTED_ELO_ORDER_ANCHOR
    assert set(truth["frozen_pool"]) == set(EXPECTED_ELO_ORDER_ANCHOR)
    assert truth["holdout_matrix_orders"][5] == HOLDOUT_MATRIX_ORDERS_ANCHOR[5]
    assert list(truth["grid"]["required_opponents"]) == CHECK_EVAL_GRID_ANCHOR
    assert list(truth["grid"]["development_seeds"]) == DEVELOPMENT_SEEDS_ANCHOR
    assert list(truth["grid"]["seat_protocol"]) == SEAT_PROTOCOL_ANCHOR
    assert truth["grid"]["games_per_opponent"] == GRID_GAMES_PER_OPPONENT_ANCHOR
    assert list(truth["regression_seeds"]) == REGRESSION_SEEDS_ANCHOR
    # 快照为独立 dict：改返回值不污染模块常量
    truth["opponent_pool_11"] = ()
    assert roster.OPPONENT_POOL_11 != ()
