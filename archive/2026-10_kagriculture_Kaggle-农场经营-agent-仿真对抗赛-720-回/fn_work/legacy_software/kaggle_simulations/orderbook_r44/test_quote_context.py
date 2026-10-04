# -*- coding: utf-8 -*-
"""R27 测试面：quote_context（判新高基线语义/换日复位/跟踪器持久/缺字段→None）。"""
from __future__ import annotations

from orderbook_r44 import quote_context as qc


def test_quote_context():
    """形状与基线语义：day=step//24；day_highs=截至上一步的当日最高（不含当前报价）；
    quote=公开报价；base=引擎 base 九品全表；跟踪器跨调用持久并 fold 当前报价。"""
    tr = {}
    ctx = qc.quote_context(
        {"step": 30, "market": {"prices": {"EGG": 55.0, "WHEAT": 25}}}, tr)
    assert ctx["day"] == 1
    assert ctx["quote"] == {"EGG": 55.0, "WHEAT": 25.0}
    assert ctx["day_highs"] == {}  # 首见无基线（判新高基线不含当前报价）
    assert ctx["base"] == {
        "WHEAT": 25.0, "CARROT": 35.0, "TOMATO": 60.0, "STRAWBERRY": 120.0,
        "MELON": 250.0, "EGG": 50.0, "MILK": 160.0, "WOOL": 200.0,
        "FERTILIZER": 100.0}
    assert tr == {"day": 1, "day_highs": {"EGG": 55.0, "WHEAT": 25.0}}
    # 跨调用持久：次步基线=截至上一步的当日最高
    ctx2 = qc.quote_context({"step": 31, "market": {"prices": {"EGG": 60.0}}}, tr)
    assert ctx2["day"] == 1
    assert ctx2["day_highs"] == {"EGG": 55.0, "WHEAT": 25.0}
    assert ctx2["quote"] == {"EGG": 60.0}
    assert tr["day_highs"] == {"EGG": 60.0, "WHEAT": 25.0}  # fold 后含当前
    # 非更高价不抬跟踪（max 语义）
    qc.quote_context({"step": 32, "market": {"prices": {"EGG": 50.0}}}, tr)
    assert tr["day_highs"]["EGG"] == 60.0


def test_quote_context_day_change_reset():
    """换日复位：day=step//24 跨日边界后 day_highs 清空重建。"""
    tr = {}
    qc.quote_context({"step": 23, "market": {"prices": {"EGG": 55.0}}}, tr)
    assert tr == {"day": 0, "day_highs": {"EGG": 55.0}}
    ctx = qc.quote_context({"step": 24, "market": {"prices": {"EGG": 10.0}}}, tr)
    assert ctx["day"] == 1
    assert ctx["day_highs"] == {}  # 换日复位：昨日高点不带入今日基线
    assert tr == {"day": 1, "day_highs": {"EGG": 10.0}}


def test_quote_context_sequence():
    """序列输入按步序处理：中间步 fold，末步返回基线（含前步、不含末步）。"""
    tr = {}
    ctx = qc.quote_context([
        {"step": 24, "market": {"prices": {"EGG": 10.0}}},
        {"step": 25, "market": {"prices": {"EGG": 20.0}}},
        {"step": 26, "market": {"prices": {"EGG": 15.0}}},
    ], tr)
    assert ctx["day"] == 1
    assert ctx["day_highs"] == {"EGG": 20.0}  # 前两步 fold 后的高点
    assert ctx["quote"] == {"EGG": 15.0}
    assert tr["day_highs"] == {"EGG": 20.0}
    # 跨日序列：末步换日→基线清空
    ctx2 = qc.quote_context([
        {"step": 47, "market": {"prices": {"EGG": 30.0}}},
        {"step": 48, "market": {"prices": {"EGG": 3.0}}},
    ], tr)
    assert ctx2["day"] == 2
    assert ctx2["day_highs"] == {}


def test_quote_context_missing_fields():
    """缺字段→None；解析期零副作用（跟踪器不动）。"""
    tr = {"day": 0, "day_highs": {"EGG": 1.0}}
    assert qc.quote_context({"market": {"prices": {"EGG": 2.0}}}, tr) is None
    assert qc.quote_context({"step": 1}, tr) is None
    assert qc.quote_context({"step": 1, "market": {}}, tr) is None
    assert qc.quote_context({"step": 1, "market": {"prices": []}}, tr) is None
    assert qc.quote_context(None, tr) is None
    assert qc.quote_context([], tr) is None
    assert qc.quote_context("obs", tr) is None
    assert tr == {"day": 0, "day_highs": {"EGG": 1.0}}  # 零副作用
    # 非数值价目跳过（不属缺字段）；step 整值 float 可用、非整值→None
    ctx = qc.quote_context(
        {"step": 1.0, "market": {"prices": {"EGG": "x", "WHEAT": 2.5}}}, tr)
    assert ctx["quote"] == {"WHEAT": 2.5}
    assert qc.quote_context({"step": 1.5, "market": {"prices": {}}}, tr) is None
