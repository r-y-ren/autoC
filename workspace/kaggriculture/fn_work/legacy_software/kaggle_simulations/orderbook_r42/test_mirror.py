# -*- coding: utf-8 -*-
"""R25 测试面：P3 镜像门组（判据=R25 ③原文：指纹相等触发/不等不触发/
credit 净加卖 0/缺字段不触发/构造用例）。"""
from __future__ import annotations

from orderbook_r42 import mirror as mr


def _farm(uq=("NW",), grid=None, hands=2):
    return {"unlocked_quadrants": list(uq),
            "tiles": grid if grid is not None else
            [[{"kind": "FIELD", "crop": "WHEAT", "animal": None}, "LOCKED"]],
            "hands": [1] * hands}


def _obs(step, farm0, farm1, shed=None, player=0):
    return {"step": step, "player": player,
            "farms": [farm0, farm1],
            "private": {"shed": dict(shed or {})},
            "market": {"prices": {"WHEAT": 40}}}


def test_mirror_gate_triggers_on_equal_fingerprints():
    """指纹相等→触发镜像（latch）；卖出尾窗速率驱动提前量+credit 记账。"""
    f = _farm()
    obs0 = _obs(0, f, _farm(), {"WHEAT": 50})
    mr.apply_mirror_gate(obs0, {"market": []})           # 复位
    # 建立尾窗卖速：连续 24 拍每拍卖 2 WHEAT
    for t in range(1, 25):
        out = mr.apply_mirror_gate(
            _obs(t, f, _farm(), {"WHEAT": 50}),
            {"market": [["SELL", "WHEAT", 2]]})
    assert out["ledger"]["mirror"] is True
    assert out["ledger"]["repaid"] > 0                   # 稳态：前移被后续偿还
    out2 = mr.apply_mirror_gate(
        _obs(25, f, _farm(), {"WHEAT": 50}),
        {"market": [["SELL", "WHEAT", 2]]})
    assert out2["ledger"]["boosted"] > 0                 # 提前量生效
    assert out2["credit"].get("WHEAT", 0) > 0            # credit 记账


def test_mirror_gate_no_trigger_on_different_farms():
    f0, f1 = _farm(hands=2), _farm(hands=3)
    mr.apply_mirror_gate(_obs(0, f0, f1), {"market": []})
    out = mr.apply_mirror_gate(_obs(10, f0, f1, {"WHEAT": 5}),
                               {"market": [["SELL", "WHEAT", 2]]})
    assert out["ledger"]["mirror"] is False
    assert out["ledger"]["boosted"] == 0


def test_mirror_gate_credit_repay_no_net_add():
    """credit 偿还：提前卖的量从后续卖单等额扣（禁净加卖）。"""
    f = _farm()
    mr.apply_mirror_gate(_obs(0, f, _farm()), {"market": []})
    mr.apply_mirror_gate._state["mirror"] = True
    mr.apply_mirror_gate._state["credit"] = {"WHEAT": 5}
    mr.apply_mirror_gate._state["sold"] = {}
    out = mr.apply_mirror_gate(
        _obs(300, f, _farm(), {"WHEAT": 50}),
        {"market": [["SELL", "WHEAT", 4]]})
    sells = [e for e in out["action"]["market"]
             if isinstance(e, list) and e and e[0] == "SELL"]
    assert out["ledger"]["repaid"] == 4                  # 4 全额抵扣
    assert out["credit"]["WHEAT"] == 1                   # 余债留账
    # 原卖单 4 被抵扣删除（净加卖=0）；无新卖单超过原计划+抵扣
    assert all(e[2] <= 4 for e in sells)


def test_mirror_gate_missing_fields_no_trigger_and_fail_safe():
    out = mr.apply_mirror_gate(_obs(0, {"tiles": []}, {"tiles": []}),
                               {"market": []})
    assert out["ledger"]["mirror"] is False              # 缺字段不触发
    bad = mr.apply_mirror_gate({"step": 1}, "not-a-dict")
    assert bad["action"] == "not-a-dict" and \
        bad["ledger"]["failed"] is True
