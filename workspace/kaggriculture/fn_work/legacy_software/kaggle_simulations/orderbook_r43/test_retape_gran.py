# -*- coding: utf-8 -*-
"""R26 测试面：③细颗粒组（守恒/阈值/摊不完回填构造用例）。"""
from __future__ import annotations

from orderbook_r43 import retape_gran as rg


def _pkg(steps):
    acts, seq = [], []
    for t, market in enumerate(steps):
        acts.append({"farmer": ["PASS"], "hands": [], "market": market})
        seq.append(len(acts) - 1)
    return {"actions": acts, "routes": {"1": seq}, "shops": []}


def test_granularity_splits_and_conserves():
    """大单拆块：30→6×5 摊后续拍；守恒；阈值下不动。"""
    steps = [[] for _ in range(20)]
    steps[3] = [["SELL", "WHEAT", 30]]
    steps[5] = [["SELL", "MILK", 8]]                 # 阈值下不动
    out = rg.retape_granularity(_pkg(steps))
    seq = out["routes"]["routes"]["1"]
    pool = out["routes"]["actions"]
    wheat = sum(cmd[2] for ai in seq
                for cmd in (pool[ai].get("market") or [])
                if isinstance(cmd, list) and len(cmd) >= 3 and
                cmd[0] == "SELL" and cmd[1] == "WHEAT")
    assert wheat == 30                                 # 守恒
    assert pool[seq[3]]["market"][0] == ["SELL", "WHEAT", 6]
    assert pool[seq[5]]["market"][0] == ["SELL", "MILK", 8]
    assert any(c["kind"] == "granularity" for c in out["change_table"])


def test_granularity_overflow_restored():
    """摊不完（max_forward 耗尽）→余量回填源槽，守恒不破。"""
    steps = [[] for _ in range(6)]
    steps[0] = [["SELL", "WHEAT", 60]]               # 只能摊 6 拍
    out = rg.retape_granularity(_pkg(steps), {"threshold": 12, "chunk": 6,
                                              "max_forward": 3})
    seq = out["routes"]["routes"]["1"]
    pool = out["routes"]["actions"]
    wheat = sum(cmd[2] for ai in seq
                for cmd in (pool[ai].get("market") or [])
                if isinstance(cmd, list) and len(cmd) >= 3 and
                cmd[0] == "SELL" and cmd[1] == "WHEAT")
    assert wheat == 60                                 # 守恒（回填生效）
