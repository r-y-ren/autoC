# -*- coding: utf-8 -*-
"""R25 测试面：P2 终日清算组（判据=R25 ②原文：648 切换/停采购/−price×qty
降序清算序/712-718 全量出清/构造用例）。"""
from __future__ import annotations

from orderbook_r42 import endgame as eg


def _obs(step, shed, prices=None):
    return {"step": step, "private": {"shed": dict(shed)},
            "market": {"prices": prices or {"WHEAT": 40, "MILK": 100,
                                            "WOOL": 200}}}


def test_endgame_noop_before_648():
    action = {"market": [["BUY_PRODUCT", "WHEAT", 3], ["SELL", "WHEAT", 5]]}
    out = eg.apply_endgame_liquidation(_obs(600, {"WHEAT": 9}), action)
    assert out["ledger"].get("noop") is True
    assert out["action"] is action                       # 原动作不动


def test_endgame_liquidation_order_and_buys_stopped():
    """停 BUY 类、旧卖单被清算序取代、按 −price×qty 降序、均摊递增。"""
    action = {"market": [["BUY_PRODUCT", "WHEAT", 3], ["HIRE"],
                         ["SELL", "WOOL", 1], []]}
    out = eg.apply_endgame_liquidation(
        _obs(648, {"WOOL": 20, "MILK": 10, "WHEAT": 30}), action)
    m = out["action"]["market"]
    sells = [e for e in m if e and e[0] == "SELL"]
    assert all(not (e and str(e[0]).startswith("BUY")) for e in m)
    assert ["HIRE"] in m and [] in m                     # 非卖非买不动
    # 价值序：WOOL 200×lots 优先 MILK 100 再 WHEAT 40
    assert [e[1] for e in sells] == ["WOOL", "MILK", "WHEAT"]
    assert out["ledger"]["n_sells"] == 3
    # 均摊：remaining=71，lots=ceil(qty/71)
    assert sells[0][2] == 1 and sells[1][2] == 1 and sells[2][2] == 1


def test_endgame_forced_full_drain_712():
    """712-718 段全量出清。"""
    action = {"market": []}
    out = eg.apply_endgame_liquidation(
        _obs(712, {"WHEAT": 30, "MILK": 10}), action)
    m = out["action"]["market"]
    assert sorted((e[1], e[2]) for e in m) == [("MILK", 10), ("WHEAT", 30)]
    assert out["ledger"]["forced_full"] is True


def test_endgame_fail_safe():
    out = eg.apply_endgame_liquidation({"step": 700}, "not-a-dict")
    assert out["action"] == "not-a-dict" and out["ledger"]["failed"] is True
