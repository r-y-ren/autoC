# -*- coding: utf-8 -*-
"""R27 测试面：件 B 谷底闸门（门删除/磁带豁免/标记缺失保守/并单磁带余量/agent 包装）。"""
from __future__ import annotations

from orderbook_r44 import glutgate_layer as gg


def _obs(step, prices, shed=None):
    """合成 observation 夹具（不跑真局）。"""
    return {"step": step, "player": 0,
            "market": {"prices": dict(prices), "inventory": {}},
            "private": {"shed": dict(shed or {}), "seeds": {},
                        "inventories": [{}, {}]}}


def test_gate_added_sells():
    """门删除语义：quote<base 的我方加挂 SELL 删；quote≥base 不删；磁带豁免；
    标记缺失/陈旧/对不上→保守不删；并单只净扣追加量；删除台账留痕。"""
    # 门删除：标记命中 quote<base（EGG 40<base 50）→整单删除+台账
    market = [["SELL", "EGG", 5]]
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0}), {"market": market},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] == []
    assert res["removed"] == [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}]
    # quote≥base 不删（零删除返回原 market 对象）
    market = [["SELL", "EGG", 5]]
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 50.0}), {"market": market},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] is market and res["removed"] == []
    # 磁带豁免：无标记的单即便 quote<base 也不动（MILK 100<base 160）
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0, "MILK": 100.0}),
        {"market": [["SELL", "EGG", 5], ["SELL", "MILK", 2]]},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] == [["SELL", "MILK", 2]]
    # 标记缺失→保守不删（None/空）
    market = [["SELL", "EGG", 5]]
    for marks in (None, []):
        res = gg.gate_added_sells(_obs(30, {"EGG": 40.0}), {"market": market}, marks)
        assert res["market"] is market and res["removed"] == []
    # 陈旧步标记（槽位属上一步）→跳过
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0}), {"market": market},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 29}])
    assert res["market"] is market and res["removed"] == []
    # 并单：只净扣标记追加量 3，磁带余量 7 豁免不动
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0}), {"market": [["SELL", "EGG", 10]]},
        [{"item": "EGG", "qty": 3, "slot": 0, "step": 30}])
    assert res["market"] == [["SELL", "EGG", 7]]
    assert res["removed"] == [{"item": "EGG", "qty": 3, "slot": 0, "step": 30}]
    # 槽位/单形对不上→保守不删
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0}), {"market": [["SELL", "MILK", 5]]},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] == [["SELL", "MILK", 5]] and res["removed"] == []
    # quote/base 取不到→不删（无报价/无 base 条目）
    res = gg.gate_added_sells(
        _obs(30, {}), {"market": [["SELL", "EGG", 5]]},
        [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] == [["SELL", "EGG", 5]] and res["removed"] == []
    res = gg.gate_added_sells(
        _obs(30, {"GOLD": 1.0}), {"market": [["SELL", "GOLD", 5]]},
        [{"item": "GOLD", "qty": 5, "slot": 0, "step": 30}])
    assert res["market"] == [["SELL", "GOLD", 5]] and res["removed"] == []
    # 多标记按槽位降序删除不移位，台账记录原槽位
    market = [["SELL", "EGG", 2], ["BUY_SEED", "WHEAT", 1], ["SELL", "MILK", 3]]
    res = gg.gate_added_sells(
        _obs(30, {"EGG": 40.0, "MILK": 100.0}), {"market": market},
        [{"item": "EGG", "qty": 2, "slot": 0, "step": 30},
         {"item": "MILK", "qty": 3, "slot": 2, "step": 30}])
    assert res["market"] == [["BUY_SEED", "WHEAT", 1]]
    assert sorted(res["removed"], key=lambda r: r["slot"]) == [
        {"item": "EGG", "qty": 2, "slot": 0, "step": 30},
        {"item": "MILK", "qty": 3, "slot": 2, "step": 30}]
    # 观测缺步/动作非 dict/市场非列表→保守零删除
    marks = [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}]
    market = [["SELL", "EGG", 5]]
    res = gg.gate_added_sells(None, {"market": market}, marks)
    assert res["market"] is market and res["removed"] == []
    res = gg.gate_added_sells(_obs(30, {"EGG": 40.0}), {"market": None}, marks)
    assert res["removed"] == []


def test_glutgate_agent():
    """运行时包装：注册表命中→过滤+删除台账；B 单形态（无注册表）零足迹；
    step==0 复位删除台账。"""
    action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "EGG", 5]]}
    gg._GG_REMOVED.clear()
    # AB 形态：_DH_ADDED 注册表经 globals() 命中→删我方加挂单
    gg._DH_ADDED = [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}]
    old_host, old_gate = gg._GG_HOST, gg.gate_added_sells
    try:
        gg._GG_HOST = lambda obs, cfg=None: action
        out = gg._glutgate_agent(_obs(30, {"EGG": 40.0}))
    finally:
        del gg._DH_ADDED
        gg._GG_HOST = old_host
    assert out is not action and out["market"] == []
    assert out["farmer"] == ["PASS"] and out["hands"] == []
    assert gg._GG_REMOVED == [{"item": "EGG", "qty": 5, "slot": 0, "step": 30}]
    assert action["market"] == [["SELL", "EGG", 5]]  # 宿主动作不动
    # B 单形态：无 _DH_ADDED 注册表→标记缺失→保守不删→同对象零足迹
    try:
        gg._GG_HOST = lambda obs, cfg=None: action
        out = gg._glutgate_agent(_obs(30, {"EGG": 40.0}))
    finally:
        gg._GG_HOST = old_host
    assert out is action
    # step==0 复位删除台账
    gg._GG_REMOVED.append({"item": "X", "qty": 1, "slot": 0, "step": 9})
    try:
        gg._GG_HOST = lambda obs, cfg=None: action
        out = gg._glutgate_agent(_obs(0, {"EGG": 40.0}))
    finally:
        gg._GG_HOST = old_host
    assert out is action and gg._GG_REMOVED == []
    assert old_gate is gg.gate_added_sells


def test_glutgate_agent_fail_safe(monkeypatch):
    """内部异常→宿主动作原样返回（同对象）。"""
    action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "EGG", 5]]}
    monkeypatch.setattr(gg, "_GG_HOST", lambda obs, cfg=None: action)
    monkeypatch.setattr(
        gg, "gate_added_sells",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError()))
    assert gg._glutgate_agent(_obs(30, {"EGG": 40.0})) is action
    # 观测非 dict（step 解析异常）→同对象回退
    monkeypatch.undo()
    monkeypatch.setattr(gg, "_GG_HOST", lambda obs, cfg=None: action)
    assert gg._glutgate_agent(None) is action
