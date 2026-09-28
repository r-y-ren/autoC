# -*- coding: utf-8 -*-
"""R27 测试面：件 A 日内新高变现（detect 新高判定/plan 槽位计划/agent 运行时包装）。"""
from __future__ import annotations

from orderbook_r44 import dayhigh_layer as dh


def _obs(step, prices, shed=None):
    """合成 observation 夹具（不跑真局）：R27 用到 step/market.prices/private.shed。"""
    return {"step": step, "player": 0,
            "market": {"prices": dict(prices), "inventory": {}},
            "private": {"shed": dict(shed or {}), "seeds": {},
                        "inventories": [{}, {}]}}


def test_detect_dayhigh():
    """新高判定：严格新高触发/等值不触发/quote<2 永不触发/父链在卖不触发/
    7 品外不触发/无基线（当日首见）不触发。"""
    ctx = {"day": 1,
           "day_highs": {"EGG": 50.0, "MILK": 100.0, "WHEAT": 10.0},
           "quote": {"EGG": 60.0, "MILK": 100.0, "WHEAT": 30.0, "TOMATO": 2.0},
           "base": {}}
    tr = {"day": 1, "day_highs": dict(ctx["day_highs"])}
    assert dh.detect_dayhigh(ctx, {"market": []}, tr) == {"EGG": 60.0}
    # quote<2 永不触发（即便严格新高）
    ctx2 = {"day": 1, "day_highs": {"TOMATO": 1.0}, "quote": {"TOMATO": 1.5},
            "base": {}}
    assert dh.detect_dayhigh(ctx2, {"market": []},
                             {"day": 1, "day_highs": {}}) == {}
    # 父链在卖该品（qty>0）不触发
    assert dh.detect_dayhigh(ctx, {"market": [["SELL", "EGG", 3]]},
                             {"day": 1, "day_highs": {}}) == {}
    # 父链零量 SELL=占槽非在卖→仍触发
    assert dh.detect_dayhigh(ctx, {"market": [["SELL", "EGG", 0]]},
                             {"day": 1, "day_highs": {}}) == {"EGG": 60.0}
    # 无基线（当日/跟踪首见，day_highs 无该品条目）不触发
    ctx3 = {"day": 1, "day_highs": {}, "quote": {"EGG": 60.0}, "base": {}}
    assert dh.detect_dayhigh(ctx3, {"market": []},
                             {"day": 1, "day_highs": {}}) == {}
    # 7 品外（WHEAT）严格新高也不触发
    ctxw = {"day": 1, "day_highs": {"WHEAT": 10.0}, "quote": {"WHEAT": 30.0},
            "base": {}}
    assert dh.detect_dayhigh(ctxw, {"market": []},
                             {"day": 1, "day_highs": {"WHEAT": 10.0}}) == {}


def test_detect_dayhigh_tracker_and_errors():
    """跟踪器维护=换日复位+fold；异常→空集（零动作）。"""
    tr = {"day": 0, "day_highs": {"EGG": 999.0}}
    ctx = {"day": 1, "day_highs": {}, "quote": {"EGG": 60.0}, "base": {}}
    assert dh.detect_dayhigh(ctx, {"market": []}, tr) == {}
    assert tr == {"day": 1, "day_highs": {"EGG": 60.0}}  # 换日复位后重建
    assert dh.detect_dayhigh(None, {"market": []}, {}) == {}
    assert dh.detect_dayhigh({"day": 1, "quote": {}, "day_highs": {}},
                             "bad-action", {}) == {}
    assert dh.detect_dayhigh({"day": 1, "quote": {}, "day_highs": {}},
                             {"market": []}, None) == {}
    assert dh.detect_dayhigh({"day": 1, "quote": {}}, {"market": []}, {}) == {}


def test_plan_dayhigh_sells():
    """可卖量守恒=在仓可卖−本步已挂同品卖量；price×qty 降序；库存/卖量不确定→零追加。"""
    base = [["SELL", "EGG", 4], ["BUY_SEED", "WHEAT", 1]]
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 10}, base)
    assert plan["orders"] == [["SELL", "EGG", 6]]
    assert plan["slots"] == [0]
    assert plan["ledger"] == [{"item": "EGG", "qty": 6, "slot": 0,
                               "merge": True}]
    assert plan["market"] == [["SELL", "EGG", 10], ["BUY_SEED", "WHEAT", 1]]
    assert base[0] == ["SELL", "EGG", 4]  # 原单不动
    # 已挂≥在仓（含等值）→零追加，不多卖
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 4},
                                 [["SELL", "EGG", 4]])
    assert plan["orders"] == [] and plan["market"] == [["SELL", "EGG", 4]]
    # price×qty 降序（MELON 300×2=600 > EGG 60×5=300）
    plan = dh.plan_dayhigh_sells({"EGG": 60.0, "MELON": 300.0},
                                 {"EGG": 5, "MELON": 2},
                                 [["BUY_SEED", "WHEAT", 1]])
    assert plan["orders"] == [["SELL", "MELON", 2], ["SELL", "EGG", 5]]
    assert plan["slots"] == [0, 1]
    assert plan["market"] == [["SELL", "MELON", 2], ["SELL", "EGG", 5],
                              ["BUY_SEED", "WHEAT", 1]]
    # 库存不确定→该品零追加（缺品/字符串/半值/负值）
    for inv in ({"EGG": "5", "MELON": 2}, {"EGG": 5.5, "MELON": 2},
                {"EGG": -1, "MELON": 2}, {"MELON": 2}):
        plan = dh.plan_dayhigh_sells({"EGG": 60.0, "MELON": 300.0}, inv, [])
        assert plan["orders"] == [["SELL", "MELON", 2]]
    plan = dh.plan_dayhigh_sells({"EGG": 60.0, "MELON": 300.0}, None, [])
    assert plan["orders"] == []  # 库存整体不确定→全部零追加
    # 同品已挂卖量不可解析=可卖量不确定→零追加
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 10},
                                 [["SELL", "EGG", "x"]])
    assert plan["orders"] == []


def test_plan_dayhigh_sells_slots():
    """并单槽序：并入最早同品 SELL 槽/不能并置首个花费单之前/无花费单置表尾/
    10 槽满弃追加（不挤原单）。"""
    # 并入最早同品 SELL 槽（同品多单取最早；可卖量 10−3=7 并入）
    base = [["SELL", "EGG", 1], ["BUY_PRODUCT", "WHEAT", 2], ["SELL", "EGG", 2]]
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 10}, base)
    assert plan["market"] == [["SELL", "EGG", 8], ["BUY_PRODUCT", "WHEAT", 2],
                              ["SELL", "EGG", 2]]
    assert plan["slots"] == [0] and plan["ledger"][0]["merge"] is True
    assert base[0] == ["SELL", "EGG", 1] and base[2] == ["SELL", "EGG", 2]
    # 不能并→置于首个花费单（HIRE/BUY_SEED/BUY_PRODUCT/BUY_ANIMAL/BUY_LAND）之前
    base = [["SELL", "WOOL", 1], ["HIRE", "h", 1], ["BUY_SEED", "WHEAT", 1]]
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 5}, base)
    assert plan["market"] == [["SELL", "WOOL", 1], ["SELL", "EGG", 5],
                              ["HIRE", "h", 1], ["BUY_SEED", "WHEAT", 1]]
    assert plan["slots"] == [1] and plan["ledger"][0]["merge"] is False
    # 无花费单→置表尾
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 5}, [["SELL", "WOOL", 1]])
    assert plan["market"] == [["SELL", "WOOL", 1], ["SELL", "EGG", 5]]
    # 10 槽满→放弃该追加（宁缺勿挤，不挤掉原单）
    base = [["SELL", "I%d" % i, 1] for i in range(10)]
    plan = dh.plan_dayhigh_sells({"EGG": 60.0}, {"EGG": 5}, base)
    assert plan["orders"] == [] and plan["ledger"] == []
    assert plan["market"] == base
    assert all(o == ["SELL", "I%d" % i, 1] for i, o in enumerate(base))


def test_dayhigh_agent():
    """运行时包装：新高→追加单并入动作+台账；step==0 复位跟踪器与台账；无触发零足迹。"""
    dh._DH_TRACKER.clear()
    dh._DH_ADDED.clear()
    action = {"farmer": ["PASS"], "hands": [],
              "market": [["BUY_SEED", "WHEAT", 3]]}
    monkey_host = lambda obs, cfg=None: action  # noqa: E731
    # 新高触发：追加单置于首个花费单之前+台账留痕
    dh._DH_TRACKER.update({"day": 1, "day_highs": {"EGG": 50.0}})
    import types
    old_host = dh._DH_HOST
    try:
        dh._DH_HOST = monkey_host
        out = dh._dayhigh_agent(_obs(30, {"EGG": 60.0}, shed={"EGG": 5}))
    finally:
        dh._DH_HOST = old_host
    assert out is not action
    assert out["market"] == [["SELL", "EGG", 5], ["BUY_SEED", "WHEAT", 3]]
    assert action["market"] == [["BUY_SEED", "WHEAT", 3]]  # 基座动作不动
    assert dh._DH_ADDED == [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}]
    # 无严格新高→原动作同对象
    dh._DH_TRACKER.update({"day": 1, "day_highs": {"EGG": 50.0}})
    dh._DH_ADDED.clear()
    try:
        dh._DH_HOST = monkey_host
        out = dh._dayhigh_agent(_obs(30, {"EGG": 50.0}, shed={"EGG": 5}))
    finally:
        dh._DH_HOST = old_host
    assert out is action
    assert dh._DH_ADDED == []
    # step==0 复位跟踪器与台账（陈旧高点/陈旧标记清空）
    dh._DH_TRACKER.update({"day": 7, "day_highs": {"EGG": 999.0}})
    dh._DH_ADDED.append({"item": "EGG", "qty": 1, "slot": 0, "step": 7})
    try:
        dh._DH_HOST = monkey_host
        out = dh._dayhigh_agent(_obs(0, {"EGG": 10.0}, shed={"EGG": 5}))
    finally:
        dh._DH_HOST = old_host
    assert out is action  # 当日首见无基线→零动作
    assert dh._DH_TRACKER == {"day": 0, "day_highs": {"EGG": 10.0}}
    assert dh._DH_ADDED == []


def test_dayhigh_agent_fail_safe(monkeypatch):
    """内部异常→基座动作原样返回（同对象）。"""
    dh._DH_TRACKER.clear()
    dh._DH_ADDED.clear()
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    monkeypatch.setattr(dh, "_DH_HOST", lambda obs, cfg=None: action)
    dh._DH_TRACKER.update({"day": 1, "day_highs": {"EGG": 50.0}})
    monkeypatch.setattr(dh, "detect_dayhigh",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError()))
    out = dh._dayhigh_agent(_obs(30, {"EGG": 60.0}, shed={"EGG": 5}))
    assert out is action
    monkeypatch.undo()
    monkeypatch.setattr(dh, "_DH_HOST", lambda obs, cfg=None: action)
    monkeypatch.setattr(dh, "detect_dayhigh", lambda *a, **k: {"EGG": 60.0})
    monkeypatch.setattr(dh, "plan_dayhigh_sells",
                        lambda *a, **k: (_ for _ in ()).throw(ValueError()))
    out = dh._dayhigh_agent(_obs(30, {"EGG": 60.0}, shed={"EGG": 5}))
    assert out is action
    # 观测缺字段（quote_context→None）→原动作
    monkeypatch.undo()
    monkeypatch.setattr(dh, "_DH_HOST", lambda obs, cfg=None: action)
    out = dh._dayhigh_agent({"player": 0})
    assert out is action
