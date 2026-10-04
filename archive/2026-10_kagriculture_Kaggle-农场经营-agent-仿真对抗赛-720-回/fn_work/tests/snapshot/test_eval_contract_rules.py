# test_eval_contract_rules.py —— 评估契约族规则固化（R1 基线）
# ===========================================================================
# 钉什么（kgenv/eval_contract.py + holdout_contract.py 合成配置）：
#   * 种子域隔离：development 101-104 / regression 201-208 / holdout 不得
#     与已知非 holdout 种子重叠（重叠即拒）；
#   * AB/BA 对称调度：build_ab_ba_schedule 的冻结输出（pair × seed × 双席）；
#   * holdout 历史种子黑名单：5 代 HISTORICAL_SEEDS_V* 尺寸链（38/46/54/62）
#     与 published 种子命中拒绝；generate_holdout_seeds 的确定性 stub 抽取；
#   * 异常局判定：game_abnormal_reason 的拒绝理由与合法局 None；
#   * canonical_sha256 的规范化哈希。
# 冻结值 2026-09-21 实测固化。
# ===========================================================================

import pytest

from kgenv import eval_contract as ec
from kgenv import holdout_contract as hc


# ---------------------------------------------------------------------------
# 种子域隔离（eval_contract）
# ---------------------------------------------------------------------------

def test_seed_domains_development_ok_and_rejected():
    ec.validate_seed_domain([101, 102, 103, 104], "development")
    with pytest.raises(ec.ContractError,
                       match="development seeds must stay within 101-104"):
        ec.validate_seed_domain([101, 105], "development")


def test_seed_domains_regression_ok_and_rejected():
    ec.validate_seed_domain(list(range(201, 209)), "regression")
    with pytest.raises(ec.ContractError,
                       match="regression seeds must stay within 201-208"):
        ec.validate_seed_domain([209], "regression")


def test_seed_domain_holdout_rejects_known_overlap():
    ec.validate_seed_domain([999_001, 999_002], "holdout")
    with pytest.raises(ec.ContractError, match=r"holdout contains "
                                               r"development/regression seeds: \[101\]"):
        ec.validate_seed_domain([101, 999_001], "holdout")
    with pytest.raises(ec.ContractError, match="holdout contains"):
        ec.validate_seed_domain([201], "holdout")


def test_seed_domain_uniqueness_and_domain_name():
    with pytest.raises(ec.ContractError, match="non-empty and unique"):
        ec.validate_seed_domain([101, 101], "development")
    with pytest.raises(ec.ContractError, match="unknown seed domain"):
        ec.validate_seed_domain([101], "prod")


# ---------------------------------------------------------------------------
# AB/BA 对称调度（eval_contract）
# ---------------------------------------------------------------------------

FROZEN_SCHEDULE = [
    {"a": "submission", "b": "starter", "p0": "submission",
     "p1": "starter", "seed": 101, "seat": "AB",
     "seed_domain": "development"},
    {"a": "submission", "b": "starter", "p0": "starter",
     "p1": "submission", "seed": 101, "seat": "BA",
     "seed_domain": "development"},
    {"a": "submission", "b": "starter", "p0": "submission",
     "p1": "starter", "seed": 102, "seat": "AB",
     "seed_domain": "development"},
    {"a": "submission", "b": "starter", "p0": "starter",
     "p1": "submission", "seed": 102, "seat": "BA",
     "seed_domain": "development"},
]


def test_ab_ba_schedule_frozen():
    schedule = ec.build_ab_ba_schedule(
        [("submission", "starter")], [101, 102], "development")
    assert schedule == FROZEN_SCHEDULE


def test_ab_ba_schedule_rejects_bad_pair_and_domain():
    with pytest.raises(ec.ContractError, match="invalid pair"):
        ec.build_ab_ba_schedule([("x", "x")], [101], "development")
    with pytest.raises(ec.ContractError, match="unknown seed domain"):
        ec.build_ab_ba_schedule([("a", "b")], [101], "production")


# ---------------------------------------------------------------------------
# holdout 历史种子黑名单（holdout_contract）
# ---------------------------------------------------------------------------

def test_historical_seed_blacklist_generations_frozen():
    # 五代黑名单尺寸链（模块内 assert 的行为面，固化防回归）。
    # V1 = {1,2,3,7,8,9,42}(7) ∪ dev 101-104(4) ∪ reg 201-208(8)
    #      ∪ 601-604(4) ∪ 701-704(4) = 27。
    assert len(hc.HISTORICAL_SEEDS) == 27
    assert len(hc.HISTORICAL_SEEDS_V2) == 38
    assert len(hc.HISTORICAL_SEEDS_V3) == 46
    assert len(hc.HISTORICAL_SEEDS_V4) == 54
    assert len(hc.HISTORICAL_SEEDS_V5) == 62
    # 各代追加的 published 种子确在黑名单内。
    assert 1434909129 in hc.HISTORICAL_SEEDS_V2      # attempt-1 published
    assert 1957338404 in hc.HISTORICAL_SEEDS_V2      # online episode seed
    assert 1118713940 in hc.HISTORICAL_SEEDS_V3      # attempt-2 published
    assert 734418350 in hc.HISTORICAL_SEEDS_V4       # attempt-3 published
    assert 1908158035 in hc.HISTORICAL_SEEDS_V5      # attempt-4 published
    assert hc.historical_seeds(3) == hc.HISTORICAL_SEEDS_V3


def test_validate_holdout_seeds_rejects_blacklist_hit():
    with pytest.raises(hc.ContractError,
                       match="holdout seeds overlap historical evidence"):
        hc.validate_holdout_seeds(
            [555000001, 1434909129, 555000003, 555000004, 555000005,
             555000006, 555000007, 555000008], attempt_index=2)
    with pytest.raises(hc.ContractError, match="overlap historical"):
        hc.validate_holdout_seeds(
            [1908158035] + [5550000 + i for i in range(7)],
            attempt_index=5)


def test_validate_holdout_seeds_shape_rules():
    fresh = [555000001, 555000002, 555000003, 555000004,
             555000005, 555000006, 555000007, 555000008]
    hc.validate_holdout_seeds(fresh, attempt_index=2)     # 8 唯一正整数
    with pytest.raises(hc.ContractError, match="exactly 8 unique"):
        hc.validate_holdout_seeds(fresh[:7], attempt_index=2)
    with pytest.raises(hc.ContractError, match="unique"):
        hc.validate_holdout_seeds([1] * 8, attempt_index=2)
    with pytest.raises(hc.ContractError, match="positive"):
        hc.validate_holdout_seeds([-1] + fresh[:7], attempt_index=2)


def test_generate_holdout_seeds_deterministic_stub_frozen():
    """确定性 randbelow stub：跳过黑名单 {10005,10007} 后的抽取序列。"""
    draws = iter([5, 7, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23])
    seeds = hc.generate_holdout_seeds(lambda n: next(draws), count=8,
                                      excluded={10005, 10007})
    assert seeds == [10009, 10011, 10013, 10015,
                     10017, 10019, 10021, 10023]


def test_holdout_expected_games_chain_frozen():
    # pairs × 8 seeds × AB/BA：attempt1=36 对→576；attempt5=66 对→1056。
    assert hc.holdout_expected_games(1) == 576
    assert hc.HOLDOUT_EXPECTED_GAMES == 576
    assert hc.holdout_expected_games(5) == 1056
    assert hc.candidate_expected_games(1) == 128
    assert hc.candidate_expected_games(5) == 176


# ---------------------------------------------------------------------------
# 异常局判定（eval_contract）
# ---------------------------------------------------------------------------

def _normal_game(winner="submission"):
    rewards = [10.0, 5.0] if winner == "submission" else [5.0, 10.0]
    return {"players": ["submission", "starter"], "seed": 101,
            "seat": "AB", "seed_domain": "development",
            "statuses": ["DONE", "DONE"], "contract_ok": True,
            "winner_label": winner, "rewards": rewards}


def test_game_abnormal_reason_valid_game_none():
    assert ec.game_abnormal_reason(_normal_game()) is None


def test_game_abnormal_reason_rejection_reasons_frozen():
    non_done = dict(_normal_game(), statuses=["DONE", "TIMEOUT"])
    assert ec.game_abnormal_reason(non_done) == \
        "non-DONE statuses ['DONE', 'TIMEOUT']"
    bad_winner = dict(_normal_game(), winner_label="starter")
    assert ec.game_abnormal_reason(bad_winner) == \
        "winner_label is inconsistent with players/rewards"
    no_contract = dict(_normal_game(), contract_ok=False)
    assert ec.game_abnormal_reason(no_contract) == "contract_ok is not true"
    missing = {k: v for k, v in _normal_game().items() if k != "rewards"}
    assert ec.game_abnormal_reason(missing).startswith(
        "missing required game fields")
    # winner_label=None 而 rewards 不等：先被 winner_label 一致性门拦下
    # （"tie requires equal rewards" 仅在 expected=None 且 rewards 不等时
    # 可达——数值 rewards 下前者必先触发，此处固化实际生效的判序）。
    tie_lie = dict(_normal_game(), winner_label=None)
    assert ec.game_abnormal_reason(tie_lie) == \
        "winner_label is inconsistent with players/rewards"
    bad_seat = dict(_normal_game(), seat="AA")
    assert ec.game_abnormal_reason(bad_seat) == "invalid seat 'AA'"
    wrong_domain = dict(_normal_game(), seed_domain="holdout")
    assert ec.game_abnormal_reason(
        wrong_domain, expected_domain="development") == \
        "game seed_domain differs from top-level seed_domain"
    wrong_seed = dict(_normal_game(), seed=999)
    assert ec.game_abnormal_reason(
        wrong_seed, allowed_seeds={101, 102}) == \
        "game seed is outside configured seed set"


def test_assert_games_normal_raises_with_index():
    with pytest.raises(ec.ContractError,
                       match="abnormal game 0: non-DONE statuses"):
        ec.assert_games_normal([dict(_normal_game(),
                                     statuses=["ERROR", "ERROR"])])


# ---------------------------------------------------------------------------
# 规范化哈希
# ---------------------------------------------------------------------------

def test_canonical_sha256_frozen():
    assert ec.canonical_sha256({"b": 1, "a": 2}) == \
        "d3626ac30a87e6f7a6428233b3c68299976865fa5508e4267c5415c76af7a772"
    # 键序无关：两种插入序同一哈希。
    assert ec.canonical_sha256({"a": 2, "b": 1}) == \
        ec.canonical_sha256({"b": 1, "a": 2})


def test_standard_matrix_order_frozen():
    assert ec.STANDARD_MATRIX_ORDER == (
        "submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "greedy_carrot", "starter", "random", "pass")
    assert len(ec.STANDARD_OFFICIAL_PAIRS) == 36
    assert sorted(ec.DEVELOPMENT_SEEDS) == [101, 102, 103, 104]
    assert sorted(ec.REGRESSION_SEEDS) == list(range(201, 209))
