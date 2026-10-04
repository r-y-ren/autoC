# test_kgenv_rating_snapshots.py —— 评级/方差纯函数固化（R1 基线）
# ===========================================================================
# 钉什么（kgenv 三件纯函数面）：
#   * elo.py：EloTable 对固定对局输入序列的评级值——含**顺序敏感性**
#     （同一组 3 局对局两种顺序 → 两个不同的冻结值；这是回归门把 Elo
#     标记为 descriptive/order_sensitive 的依据）；
#   * bradley_terry.py：fit_ratings 批量拟合**顺序无关**（同一组对局两个
#     排列 → 完全相等的结果 dict），并冻结整份输出的 sha256 与关键标量；
#   * variance.py：Wilson 区间 / t 分位数 / margin_stats 固定输入冻结。
# 冻结值 2026-09-21 于 Python 3.14.7 实测固化。
# ===========================================================================

import hashlib
import json
import math

import pytest

from kgenv import bradley_terry, elo, variance

# ---------------------------------------------------------------------------
# Elo（顺序敏感）
# ---------------------------------------------------------------------------

ELO_GAMES_ORDER_1 = [("alice", "bob", 1.0),
                     ("alice", "carol", 0.5),
                     ("bob", "carol", 0.0)]
ELO_GAMES_ORDER_2 = [("bob", "carol", 0.0),
                     ("alice", "bob", 1.0),
                     ("alice", "carol", 0.5)]

FROZEN_ELO_ORDER_1 = {"alice": 1215.263693206478,
                      "bob": 1168.7701398146428,
                      "carol": 1215.9661669788793}
FROZEN_ELO_ORDER_2 = {"alice": 1215.2976013366472,
                      "bob": 1168.736306793522,
                      "carol": 1215.9660918698307}


def _elo_table(games):
    table = elo.EloTable()
    for a, b, score in games:
        table.record(a, b, score)
    return table


def test_elo_ratings_frozen_order_1():
    table = _elo_table(ELO_GAMES_ORDER_1)
    assert table.ratings == FROZEN_ELO_ORDER_1


def test_elo_ratings_frozen_order_2():
    table = _elo_table(ELO_GAMES_ORDER_2)
    assert table.ratings == FROZEN_ELO_ORDER_2


def test_elo_is_order_sensitive():
    """同一组对局、两种顺序 → 不同评级（两个冻结值互不相等）。"""
    assert FROZEN_ELO_ORDER_1 != FROZEN_ELO_ORDER_2
    assert _elo_table(ELO_GAMES_ORDER_1).ratings != \
        _elo_table(ELO_GAMES_ORDER_2).ratings


def test_elo_ranked_and_records_frozen():
    table = _elo_table(ELO_GAMES_ORDER_1)
    ranked = table.ranked()
    assert [(row["name"], row["rating"], row["played"]) for row in ranked] == [
        ("carol", 1216.0, 2), ("alice", 1215.3, 2), ("bob", 1168.8, 2)]
    assert table.wins["alice"] == {"W": 1, "L": 0, "T": 1}
    assert table.wins["bob"] == {"W": 0, "L": 2, "T": 0}
    assert table.win_rate("alice") == 0.75


def test_elo_update_pure_function_frozen():
    ra, rb = elo.update(1200.0, 1200.0, 1.0)
    assert ra == 1216.0 and rb == 1184.0
    assert elo.expected_score(1200.0, 1200.0) == 0.5


# ---------------------------------------------------------------------------
# Bradley-Terry / Davidson（批量顺序无关）
# ---------------------------------------------------------------------------


def _bt_game(a, b, reward_a, reward_b, seed, seat):
    winner = a if reward_a > reward_b else b
    return {"players": [a, b], "statuses": ["DONE", "DONE"],
            "contract_ok": True, "rewards": [reward_a, reward_b],
            "winner_label": winner, "seed": seed, "seat": seat}


def _bt_games():
    """4 agent 完全对称矩阵：5 个种子 × 6 对 × AB/BA = 60 局（全有胜负，
    走 bradley-terry 而非 davidson 分支；alpha>xena 完全分离 → 正则化
    诊断路径也被覆盖）。"""
    strength = {"alpha": 1.0, "xena": 0.2, "yuri": 0.4, "zoe": 0.6}
    names = sorted(strength)
    games = []
    for seed in (11, 22, 33, 44, 55):
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                wa = 100.0 + strength[a] * 3.0
                wb = 100.0 + strength[b] * 3.0
                games.append(_bt_game(a, b, wa, wb, seed, "AB"))
                games.append(_bt_game(b, a, wb, wa, seed, "BA"))
    return games


FROZEN_BT_SHA256 = ("4e230dd2383f0bb2e45adbd4c86f2cce4a57cab4"
                    "820880c779530bad71f17489")
FROZEN_BT_ABILITIES = {"alpha": 13.252073874631078,
                       "xena": -13.252073874630776,
                       "yuri": -4.3232592061554165,
                       "zoe": 4.323259206155114}


def test_bradley_terry_output_frozen():
    result = bradley_terry.fit_ratings(_bt_games(), bootstrap_samples=24)
    assert result["model"] == "bradley-terry"
    assert result["converged"] is True
    assert result["inference_status"] == "insufficient_data"
    assert {row["agent"]: row["ability"] for row in result["agents"]} == \
        FROZEN_BT_ABILITIES
    digest = hashlib.sha256(
        json.dumps(result, sort_keys=True).encode()).hexdigest()
    assert digest == FROZEN_BT_SHA256


def test_bradley_terry_batch_order_independent():
    """同一组对局两个排列 → 完全相等（dict 深比较，含全部浮点）。"""
    games = _bt_games()
    forward = bradley_terry.fit_ratings(games, bootstrap_samples=24)
    backward = bradley_terry.fit_ratings(list(reversed(games)),
                                          bootstrap_samples=24)
    assert forward == backward


def test_bradley_terry_rejects_abnormal_input():
    games = _bt_games()
    broken = dict(games[0], statuses=["DONE", "TIMEOUT"])
    with pytest.raises(Exception, match="abnormal"):
        bradley_terry.fit_ratings([broken])
    with pytest.raises(Exception, match="required"):
        bradley_terry.fit_ratings([])


# ---------------------------------------------------------------------------
# variance（Wilson / t / margin）
# ---------------------------------------------------------------------------


def test_wilson_ci_frozen():
    assert variance.wilson_ci(3, 4) == (0.3006, 0.9544)
    assert variance.wilson_ci(1, 1) == (0.2065, 1.0)
    assert variance.wilson_ci(0, 0) == (None, None)


def test_t95_frozen():
    assert variance.t95(4) == 3.182      # df=3
    assert variance.t95(2) == 12.706     # df=1
    assert math.isnan(variance.t95(1))   # n<2 → NaN


def test_margin_stats_frozen():
    stats = variance.margin_stats([100.0, -50.0, 25.0, 0.0])
    assert stats == {"n": 4, "mean": 18.8, "std": 62.5,
                     "ci95_lo": -80.7, "ci95_hi": 118.2,
                     "min": -50.0, "max": 100.0}
    assert variance.margin_stats([]) == {
        "n": 0, "mean": None, "std": None, "ci95_lo": None,
        "ci95_hi": None, "min": None, "max": None}
