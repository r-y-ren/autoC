# -*- coding: utf-8 -*-
"""R25 测试面：P1 槽位编排组（判据=R25 ①原文：合并守恒/同品单槽化/清死单
防 abort/摆法择优/10 槽上限构造用例）。"""
from __future__ import annotations

import pytest

from orderbook_r42 import slot_orchestration as so


def _m(*entries):
    return [list(e) for e in entries]


# ---------------------------------------------- merge 组 --

def test_merge_same_item_orders_conservation_and_slot():
    """同品合并到首位置、腾位 [] 保槽位次、总量守恒、非 SELL 不动。"""
    orders = _m(["SELL", "WHEAT", 10], ["BUY_PRODUCT", "WHEAT", 3],
                ["SELL", "WHEAT", 5], ["HIRE"], ["SELL", "MILK", 2])
    out = so.merge_same_item_orders(orders)
    assert out["conserved"] is True and out["merged"] == 1
    got = out["orders"]
    assert got[0] == ["SELL", "WHEAT", 15]          # 首位置合单
    assert got[2] == []                             # 腾位保槽位次
    assert got[1] == ["BUY_PRODUCT", "WHEAT", 3]    # 买单不动
    assert got[3] == ["HIRE"]                       # HIRE 不动
    assert got[4] == ["SELL", "MILK", 2]
    assert so.merge_same_item_orders(orders)["orders"] == got   # 确定性


def test_merge_rejects_bad_input():
    with pytest.raises(TypeError):
        so.merge_same_item_orders("not-a-list")


# ---------------------------------------------- clear 组 --

def test_clear_dead_slots_abort_prevention():
    """死单清理（机制修正版，消融 B37 毒点）：不截量（磁带卖单可含本拍收成，
    截量=系统性少卖）；只清真零库存单与 qty<0；qty==0 留给旧件 hygiene。"""
    orders = _m(["SELL", "WHEAT", 10], ["SELL", "MILK", 5],
                ["SELL", "WOOL", 3], ["SELL", "EGG", 0],
                ["SELL", "CARROT", -2])
    stock = {"WHEAT": 4, "MILK": 0, "EGG": 9}
    out = so.clear_dead_slots(orders, None, stock)
    got = out["orders"]
    assert got[0] == ["SELL", "WHEAT", 10]    # 不截量（可能有本拍收成）
    assert got[1] == []                       # 库存 0 → 清（必 abort 占槽）
    assert got[2] == []                       # stock 无 WOOL=0 → 清
    assert got[3] == ["SELL", "EGG", 0]       # qty==0 不重复处理
    assert got[4] == []                       # qty<0 → 清
    assert out["cleared"] == 3 and out["trimmed"] == 0


def test_clear_dead_slots_fail_safe():
    """异常→原列表（fail-safe）。"""
    out = so.clear_dead_slots(object(), None, {"WHEAT": 1})
    assert out.get("failed") is True


# ---------------------------------------------- layout 组 --

def test_select_best_layout_prefers_high_price_first():
    """高单价卖单前置（逐单位衰减模型下为最优摆法）。"""
    pending = [(0, ["SELL", "WHEAT", 5], 40.0),
               (1, ["SELL", "MILK", 2], 100.0)]
    out = so.select_best_layout(pending)
    assert out["best"] == "price_desc"
    assert out["order"][0][1][1] == "MILK"
    assert out["scores"]["price_desc"] >= out["scores"]["original"]


def test_select_best_layout_missing_book_first_candidate():
    """缺盘口/空集→首候选（原序）。"""
    out = so.select_best_layout(None)
    assert out["best"] == "original"


# ---------------------------------------------- 编排主件 --

def test_apply_slot_orchestration_composition():
    """编排合成：合并+清死单+摆法（只动 SELL）；>10 单裁尾部空槽。"""
    obs = {"private": {"shed": {"WHEAT": 12, "MILK": 2}},
           "market": {"prices": {"WHEAT": 40, "MILK": 100}}}
    action = {"farmer": ["PASS"], "hands": [], "market": _m(
        ["SELL", "WHEAT", 10], ["SELL", "WHEAT", 5], ["SELL", "MILK", 2],
        ["BUY_PRODUCT", "WHEAT", 3], ["HIRE"])}
    out = so.apply_slot_orchestration(obs, action)
    m = out["action"]["market"]
    assert out["ledger"]["merged"] == 1          # 15 合一单（不截量）
    assert out["ledger"]["cleared"] == 0
    assert out["ledger"]["trimmed"] == 0
    assert out["ledger"]["layout"] == "price_desc"
    # MILK(100) 该排到卖单最前槽；买单/HIRE 原位不动
    assert m[0] == ["SELL", "MILK", 2]
    assert m[2] == ["SELL", "WHEAT", 15]
    assert m[3] == ["BUY_PRODUCT", "WHEAT", 3]
    assert m[4] == ["HIRE"]
    assert action["market"][0] == ["SELL", "WHEAT", 10]   # 原动作未被改写


def test_apply_slot_orchestration_cap_trim_and_fail_safe():
    """尾部空槽裁剪（>10）；垃圾输入→原动作。"""
    obs = {"private": {"shed": {"WHEAT": 5}}, "market": {"prices": {}}}
    action = {"market": _m(["SELL", "WHEAT", 5]) + [[]] * 11}
    out = so.apply_slot_orchestration(obs, action)
    assert len(out["action"]["market"]) == so.MAX_ORDERS   # 12→10
    assert out["ledger"]["trimmed_empties"] == 2
    bad = so.apply_slot_orchestration(obs, "not-a-dict")
    assert bad["action"] == "not-a-dict" and bad["ledger"]["failed"] is True
