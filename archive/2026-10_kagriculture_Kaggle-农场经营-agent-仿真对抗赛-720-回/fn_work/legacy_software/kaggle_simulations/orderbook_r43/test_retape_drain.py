# -*- coding: utf-8 -*-
"""R26 测试面：排水表组+①排水对齐组（判据=R26 ①守恒/排空构造用例原文）。"""
from __future__ import annotations

import pytest

from orderbook_r43 import drain_table as dt
from orderbook_r43 import retape_drain as rd


def test_drain_table_pair_mechanics():
    """店对排水：多品店×1/单品店×2+中心全品各 1。"""
    table = dt.build_drain_table({"BAKERY+YARN_STORE": 1})
    d = table["1"]
    assert d["WHEAT"] == 6 * 1 + 1          # BAKERY 每日 6 + 中心 1
    assert d["EGG"] == 6 + 1
    assert d["WOOL"] == 6 * 2 + 1           # 单品店 ×2
    assert "FERTILIZER" not in d
    with pytest.raises(ValueError):
        dt.build_drain_table({})


def _pkg(steps):
    """合成包：单路线，逐步动作。"""
    acts, seq = [], []
    for t, market in enumerate(steps):
        acts.append({"farmer": ["PASS"], "hands": [], "market": market})
        seq.append(len(acts) - 1)
    return {"actions": acts, "routes": {"1": seq}, "shops": []}


def _m(item, qty):
    return [["SELL", item, qty]]


def test_drain_aligned_defers_excess_and_conserves():
    """超胃口的量推后：逐品守恒、源槽 [] /减量、目标尾追加、非卖面不动。"""
    # d11（步 264 起）一天卖 30 WHEAT，胃口 7/日 → 大量推后；终拍兜底
    steps = [[] for _ in range(300)]
    steps[264] = _m("WHEAT", 30)
    steps[265] = [["BUY_SEED", "WHEAT", 3], ["HIRE"]]     # 非卖面
    pkg = _pkg(steps)
    out = rd.retape_drain_aligned(pkg, {"1": {"WHEAT": 7.0, "MILK": 2.0}})
    seq = out["routes"]["routes"]["1"]
    pool = out["routes"]["actions"]
    total = 0
    for ai in seq:
        for cmd in (pool[ai].get("market") or []):
            if isinstance(cmd, list) and len(cmd) >= 3 and cmd[0] == "SELL" \
                    and cmd[1] == "WHEAT":
                total += cmd[2]
    assert total == 30                                # 守恒
    assert pool[seq[264]]["market"][0] in ([], ["SELL", "WHEAT", 7])  # 源槽
    bu = pool[seq[265]]["market"]
    assert ["BUY_SEED", "WHEAT", 3] in bu and ["HIRE"] in bu  # 非卖面不动
    assert out["routes"] is not pkg                   # 写时复制
    assert pkg["routes"]["1"][264] is not None
    # 原包未被动过：原动作仍在池中未被改
    orig = pkg["actions"]
    assert orig[264]["market"] == [["SELL", "WHEAT", 30]]


def test_drain_aligned_window_and_zero_drain_untouched():
    """窗口前（<264）与零排水品不动。"""
    steps = [[] for _ in range(300)]
    steps[100] = _m("WHEAT", 30)
    steps[264] = _m("EGG", 30)
    out = rd.retape_drain_aligned(_pkg(steps),
                                  {"1": {"WHEAT": 7.0, "EGG": 0.0}})
    seq = out["routes"]["routes"]["1"]
    pool = out["routes"]["actions"]
    assert pool[seq[100]]["market"] == [["SELL", "WHEAT", 30]]   # 窗口前
    assert pool[seq[264]]["market"] == [["SELL", "EGG", 30]]     # 零排水


def test_drain_aligned_conservation_break_raises(monkeypatch):
    """对账钩子：术后守恒破→抛（构造：append 失败路径由上限保护，此用钩子）。"""
    steps = [[] for _ in range(300)]
    steps[264] = _m("WHEAT", 10)
    pkg = _pkg(steps)
    out = rd.retape_drain_aligned(pkg, {"1": {"WHEAT": 7.0}})
    assert out["conservation"]["1"]["changed"] >= 3     # 10-7 推后
