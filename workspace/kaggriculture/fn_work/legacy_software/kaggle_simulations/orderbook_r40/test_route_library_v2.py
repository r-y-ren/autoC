# -*- coding: utf-8 -*-
"""R24 测试面：fingerprint 组+库 v2 组（核验命令判据=R24 ①原文：
签名形状/禁入守卫红/族数≤12/族内 n≥5/兜底族构造用例/店对混入即红）。

fingerprint 组=B33（市场面三桶+守卫+跨口径同输出）；库 v2 组=B34。
"""
from __future__ import annotations

import copy

import pytest

from orderbook_r40 import fingerprint as fp


def _obs(px=None, inv=None, shops=("BAKERY", "FARMERS_MARKET"), step=144,
         money=1234.0, hands=3):
    prices = dict(fp.BASE_PRICES)
    if px:
        prices.update(px)
    inventory = {"CARROT": 9000, "EGG": 9000, "FERTILIZER": 9000,
                 "MELON": 9000, "MILK": 9000, "STRAWBERRY": 9000,
                 "TOMATO": 9000, "WHEAT": 10000, "WOOL": 9000}
    if inv:
        inventory.update(inv)
    return {
        "step": step, "player": 0, "day": step // 24, "hour": step % 24,
        "town": {"unlocked_shops": list(shops)},
        "market": {"prices": prices, "inventory": inventory},
        "farms": [{"money": money, "hands": [1] * hands,
                   "unlocked_quadrants": ["NW"], "tiles": []},
                  {"money": 999.0, "hands": [1], "unlocked_quadrants": ["NW"],
                   "tiles": []}],
    }


# ---------------------------------------------- fingerprint 组（B33） --

def test_fingerprint_signature_shape():
    """基准价+满库存→ 'L|H|L'（偏移 1.0 双 L；库存 10000 H）。"""
    assert fp.extract_world_fingerprint(_obs()) == "L|H|L"


def test_fingerprint_bands_and_boundaries():
    """热度档与边界（1.15 恰界=M、1.25 恰界=H）；库存档三段。"""
    sig = fp.extract_world_fingerprint(
        _obs(px={"WOOL": 400.0, "MILK": 160.0, "STRAWBERRY": 240.0,
                 "WHEAT": 25.0}, inv={"WHEAT": 5000}))
    assert sig == "H|L|H"
    edge = fp.extract_world_fingerprint(
        _obs(px={"WOOL": 230.0, "MILK": 184.0, "STRAWBERRY": 138.0,
                 "WHEAT": 28.75}, inv={"WHEAT": 9500}))
    # 均值 1.15 恰界→M；库存 9500→M
    assert edge == "M|M|M"
    edge2 = fp.extract_world_fingerprint(
        _obs(px={"WOOL": 250.0, "MILK": 200.0, "STRAWBERRY": 150.0,
                 "WHEAT": 31.25}, inv={"WHEAT": 9700}))
    # 均值 1.25 恰界→H；库存 9700 恰界→H
    assert edge2 == "H|H|H"


def test_fingerprint_ignores_shops_and_own_state():
    """解耦证明：店名/自家走法量变，签名不变（禁入维度不进签名）。"""
    a = _obs(shops=("BAKERY", "FARMERS_MARKET"), money=100.0, hands=1)
    b = _obs(shops=("YARN_STORE", "PIZZA_SHOP"), money=99999.0, hands=9)
    assert fp.extract_world_fingerprint(a) == fp.extract_world_fingerprint(b)


def test_fingerprint_guard_rejects_banned_tokens():
    """店对/route_id 混入即红（判据=R24 ①守卫用例原文）。"""
    with pytest.raises(ValueError):
        fp._guard_signature("BAKERY+YARN_STORE|M|L")
    with pytest.raises(ValueError):
        fp._guard_signature("H|M|105")
    with pytest.raises(ValueError):
        fp._guard_signature("L|route|L")
    assert fp._guard_signature("L|M|L") == "L|M|L"


def test_fingerprint_missing_fields_none():
    """字段缺失→None（不抛）；垃圾输入→None。"""
    obs = _obs()
    del obs["market"]["inventory"]
    assert fp.extract_world_fingerprint(obs) is None
    assert fp.extract_world_fingerprint([1, 2, 3]) is None
    assert fp.extract_world_fingerprint({"step": 144}) is None


def test_fingerprint_cross_caliber_same_output():
    """三口径同输出：观察 dict / (步,观察,动作) 序列 / 录像步对形态。"""
    obs = _obs(px={"WOOL": 300.0})
    want = fp.extract_world_fingerprint(obs)
    assert want is not None
    seq1 = [(100, _obs(step=100), None), (144, obs, None)]
    seq2 = [[_obs(step=143), copy.deepcopy(obs)]]
    assert fp.extract_world_fingerprint(seq1) == want
    assert fp.extract_world_fingerprint(seq2) == want


# --------------------------------------------- 库 v2 组（B34 桩保留） --

def test_build_route_library_v2():
    raise NotImplementedError("unimplemented:fn:build_route_library_v2")
