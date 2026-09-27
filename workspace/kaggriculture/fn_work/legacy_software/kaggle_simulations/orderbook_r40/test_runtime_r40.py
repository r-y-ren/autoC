# -*- coding: utf-8 -*-
"""R23 测试面：runtime_r40（续段选择/竞速/补洞三件）。

route 组（B29）：指纹累计 / step144 命中选路 / 无族回退 / step0 复位 /
异常回退。race/hygiene 组保持桩红（后续批次）。
"""
import json

import pytest  # noqa: F401

try:
    from orderbook_r40.runtime_r40 import _route40_select
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    from runtime_r40 import _route40_select

KEY_A = "2|1|WHEAT:5|BAKERY+FARMERS_MARKET"     # 累计口径命中键
KEY_ZERO = "0|0|WHEAT:5|BAKERY+FARMERS_MARKET"  # 零累计对照键（亦在库中）
KEY_NOWIN = "1|0|MELON:3|BAKERY+FARMERS_MARKET"
LIB = {
    "version": "routelib/1.0",
    "families": {
        KEY_A: {"n_games": 3, "win_rate": 2 / 3, "best_route": 5,
                "margin_mean": 833.3,
                "segments": {"5": {"n": 3, "win_rate": 2 / 3,
                                   "margin_mean": 700.0}}},
        KEY_ZERO: {"n_games": 1, "win_rate": 1.0, "best_route": 7,
                   "margin_mean": 1.0, "segments": {}},
        KEY_NOWIN: {"n_games": 1, "win_rate": 0.0, "best_route": None,
                    "margin_mean": -1.0, "segments": {}},
    },
    "default": {"n_games": 5, "win_rate": 0.6, "best_route": 5,
                "margin_mean": 0.0, "segments": {}},
    "defeat_worlds": {"milk_flow": {"families": [], "covered": False},
                      "wool_flow": {"families": [], "covered": False},
                      "goose_flow": {"families": [], "covered": False}},
    "build_audit": {"n_games": 5, "n_families": 3, "coverage": 2 / 3,
                    "uncovered_families": [KEY_NOWIN], "library_sha": "0" * 64},
}
FALLBACK = {"route": None, "family": None, "confidence": 0.0}


def _obs(t, hands=0, uq=1, crops=None, shops=()):
    tiles = [[{"kind": "PLANT", "crop": c} for c, n in sorted((crops or {}).items())
              for _ in range(n)]]
    return {"day": t // 24, "hour": t % 24, "player": 1,
            "farms": [{"money": 0.0, "hands": [], "unlocked_quadrants": ["NW"],
                       "tiles": [[]]},
                      {"money": 0.0, "hands": [[0, 0]] * hands,
                       "unlocked_quadrants": ["NW"] * uq, "tiles": tiles}],
            "market": {"inventory": {"WHEAT": 9989}, "prices": {}},
            "town": {"unlocked_shops": list(shops)}}


def _reset():
    _route40_select._fp_state = None


def _feed_key_a(lib=LIB):
    """喂出 KEY_A="2|1|WHEAT:5|BAKERY+FARMERS_MARKET" 的观察流（0..144）。"""
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t, hands=2 if t >= 1 else 0,
                             uq=2 if t >= 50 else 1), lib)
    return _route40_select(_obs(144, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), lib)


def test_route40_select_fingerprint_accumulates():
    """指纹累计：hires/land 跨步正增量入族键；冷启动对照落零累计键。"""
    res = _feed_key_a()
    assert res == {"route": 5, "family": KEY_A,
                   "confidence": pytest.approx(2 / 3)}
    _reset()
    cold = _route40_select(_obs(144, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert cold == {"route": 7, "family": KEY_ZERO,
                    "confidence": pytest.approx(1.0)}


def test_route40_select_step144_hit():
    """step144 命中选路：{route, family, confidence=族 win_rate} 且跨步锁定。"""
    res = _feed_key_a()
    assert res == {"route": 5, "family": KEY_A,
                   "confidence": pytest.approx(2 / 3)}
    assert _route40_select(_obs(145, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), LIB) == {
        "route": 5, "family": KEY_A, "confidence": pytest.approx(2 / 3)}
    assert _route40_select(_obs(300, hands=2, uq=2), LIB) == {
        "route": 5, "family": KEY_A, "confidence": pytest.approx(2 / 3)}
    assert _feed_key_a({"library": LIB})["route"] == 5     # 包装形态
    assert _feed_key_a(json.dumps(LIB))["route"] == 5      # 内嵌串形态


def test_route40_select_no_family_fallback():
    """无族回退：route=None 即回退 _router 店对逻辑；无胜局族同信号。"""
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t), LIB)      # hires=0/land=0
    res = _route40_select(_obs(144, crops={"CARROT": 9},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == FALLBACK
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t, hands=1 if t >= 1 else 0), LIB)
    res = _route40_select(_obs(144, hands=1, crops={"MELON": 3},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == {"route": None, "family": KEY_NOWIN, "confidence": 0.0}


def test_route40_select_step0_reset():
    """step0 复位：新局指纹重累计，旧局锁定不带入。"""
    assert _feed_key_a()["family"] == KEY_A
    _route40_select(_obs(0), LIB)          # 新局复位
    for t in range(1, 144):
        _route40_select(_obs(t, hands=3, uq=1), LIB)   # hires=3 → 非 KEY_A
    res = _route40_select(_obs(144, hands=3, uq=1, crops={"WHEAT": 5},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == FALLBACK                 # 若未复位会返回 KEY_A 锁定
    assert _feed_key_a()["family"] == KEY_A  # 复位后重累计可再次命中


def test_route40_select_exception_fallback():
    """异常/库缺回退：不抛、route=None、且不污染锁定。"""
    _reset()
    assert _route40_select(None, LIB) == FALLBACK
    assert _route40_select({"player": 1}, LIB) == FALLBACK
    assert _route40_select({"farms": "bad"}, LIB) == FALLBACK
    assert _route40_select(_obs(144, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]),
                           None) == FALLBACK
    assert _feed_key_a()["route"] == 5     # 异常后仍可正常命中


def test_apply_race_slots():
    raise NotImplementedError("unimplemented:fn:apply_race_slots")


def test_apply_slot_hygiene():
    raise NotImplementedError("unimplemented:fn:apply_slot_hygiene")
