# -*- coding: utf-8 -*-
"""R26 测试面：判决面（判据=R26 ②③原文：realized 组/安慰剂/消融）。"""
from __future__ import annotations

from orderbook_r43 import judge_r26 as j26


def _obs(day, px):
    return {"market": {"prices": px}}


def test_realized_price_stats_metric():
    """实现价口径：Σ(qty×卖时价)/Σ(qty×日均价)。"""
    states = [(0, _obs(0, {"WHEAT": 30}), {"market": [["SELL", "WHEAT", 10]]}),
              (1, _obs(0, {"WHEAT": 30}), {"market": []}),
              (25, _obs(1, {"WHEAT": 50}), {"market": [["SELL", "WHEAT", 2]]}),
              (718, {"market": {"prices": {"WHEAT": 40}},
                     "farms": [{"money": 100000.0}],
                     "private": {"shed": {"WHEAT": 3}}},
               {"market": []})]
    out = j26.realized_price_stats(states)
    # d0 卖 10@30（日均价 30）→比值 1；d1 卖 2@50（日均价 50）→比值 1
    assert out["realized_px"] == 1.0
    assert out["terminal_money"] == 100000.0
    assert out["stranding"] == 120.0           # 3×40


def test_realized_price_stats_bad_input():
    out = j26.realized_price_stats(None)
    assert out["realized_px"] == "UNKNOWN"


def test_terminal_money_per_player_two_sides_distinguishable():
    """P2 修后口径：同局双侧读数可区分（逐席 farms[obs.player].money）。

    同一局两个 traced sink（席 0 / 席 1 视角）末观察携带全场 farms
    [120000, 88000]——旧 farms[0] 恒读会双侧同值 120000（污染症状），
    修后各读本席：席 0→120000、席 1→88000。
    """
    farms = [{"money": 120000.0}, {"money": 88000.0}]
    sink0 = [(0, {"market": {"prices": {"WHEAT": 30}}, "player": 0,
                  "farms": farms}, {"market": []}),
             (718, {"market": {"prices": {"WHEAT": 40}}, "player": 0,
                    "farms": farms, "private": {"shed": {}}}, {"market": []})]
    sink1 = [(0, {"market": {"prices": {"WHEAT": 30}}, "player": 1,
                  "farms": farms}, {"market": []}),
             (718, {"market": {"prices": {"WHEAT": 40}}, "player": 1,
                    "farms": farms, "private": {"shed": {}}}, {"market": []})]
    out0 = j26.realized_price_stats(sink0)
    out1 = j26.realized_price_stats(sink1)
    assert out0["terminal_money"] == 120000.0     # 席 0 本席钱
    assert out1["terminal_money"] == 88000.0      # 席 1 本席钱（非 farms[0]）
    assert out0["terminal_money"] != out1["terminal_money"]   # 双侧可区分
    # 缺席号回落席 0（旧行为兼容）
    out_nop = j26.realized_price_stats(
        [(718, {"market": {"prices": {"WHEAT": 40}}, "farms": farms},
          {"market": []})])
    assert out_nop["terminal_money"] == 120000.0


def test_judge_criteria_bars(monkeypatch, tmp_path):
    """判据门槛：placebo 带/实现价/终局钱/h2h 汇总与 pass 聚合。"""
    fake_rows = {}

    def fake_play(specs, cfg):
        arm = list(specs)[0].get("arm")
        n = len(list(specs))
        rows = []
        for i in range(n):
            if arm == "placebo":
                rows.append({"margin": 100 if i % 2 == 0 else -100,
                             "reads": {"realized_px": 0.9,
                                       "terminal_money": 100000,
                                       "stranding": 0}})
            elif arm == "full":
                rows.append({"margin": 100 if i % 3 else -100,
                             "reads": {"realized_px": 0.9,
                                       "terminal_money": 110000,
                                       "stranding": 1}})
            else:
                rows.append({"margin": -100,
                             "reads": {"realized_px": 0.7,
                                       "terminal_money": 90000,
                                       "stranding": 10}})
        return rows

    monkeypatch.setattr(j26, "_play", fake_play)
    arms = {a: "/tmp/x.py" for a in j26.ARMS}
    ev = j26.judge_r26(None, config={"arms": arms, "n_seeds": 6,
                                     "evidence_path": str(tmp_path /
                                                          "e.json")})
    assert ev["arms"]["placebo"]["h2h"] == 0.5       # 恒等带内
    assert ev["criteria"]["placebo_identity"]["verdict"] == "PASS"
    assert ev["criteria"]["realized_px"]["verdict"] == "PASS"   # 0.9≥0.88
    assert ev["criteria"]["terminal_money"]["verdict"] == "PASS"
    assert ev["criteria"]["h2h"]["verdict"] == "PASS"           # 2/3≥0.55
    assert ev["pass"] is True
