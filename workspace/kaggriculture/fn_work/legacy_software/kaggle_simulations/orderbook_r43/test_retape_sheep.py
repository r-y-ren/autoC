# -*- coding: utf-8 -*-
"""R26 测试面：②羊线组（刀次不减/只删喂护/无毛线路由 skip 构造用例）。"""
from __future__ import annotations

from orderbook_r43 import retape_sheep as rs


def _pkg(sells_at=None, care_at=None):
    sells_at = sells_at or {}
    care_at = care_at or {}
    acts, seq = [], []
    for t in range(300):
        market = [["SELL", "WOOL", q] if q else []
                  for q in [sells_at.get(t)]]
        hands = [["CARE"]] if care_at.get(t) else []
        acts.append({"farmer": ["PASS"], "hands": hands,
                     "market": market})
        seq.append(len(acts) - 1)
    return {"actions": acts, "routes": {"1": seq}, "shops": []}


def test_sheep_lifecycle_no_wool_skip():
    """无羊毛窗路由→skip（零改动、账本记 skipped）。"""
    pkg = _pkg(care_at={200: True})
    out = rs.retape_sheep_lifecycle(pkg)
    assert out["knives"]["1"]["skipped"] is True
    assert out["knives"]["1"]["removed"] == 0
    seq = out["routes"]["routes"]["1"]
    pool = out["routes"]["actions"]
    assert pool[seq[200]]["hands"] == [["CARE"]]      # 推导失败→不动


def test_sheep_lifecycle_real_tape_smoke():
    """真带冒烟：羊毛刀次账全路由非负、变更全 kind=sheep_lifecycle。"""
    from orderbook_r37 import retape_sheep as r37
    from pathlib import Path
    text = Path("/tmp/kagr_root/fn_work/legacy_software/kaggle_simulations/"
                "orderbook_r40/build/main.py").read_text(encoding="utf-8")
    pkg = r37._decode_routes(text)
    out = rs.retape_sheep_lifecycle(pkg)
    for rid, k in out["knives"].items():
        assert k["wool_harvests"] >= 0
    assert all(c["kind"] == "sheep_lifecycle" for c in out["change_table"])
