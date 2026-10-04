# -*- coding: utf-8 -*-
"""R25 测试面：判决面（判据=R25 ①②③+总判原文：endgame 组/mirror 组）。"""
from __future__ import annotations

import pytest

from orderbook_r42 import judge_r25 as j25


def _row(seed, seat, margin, d29=None, strand=None, mirror=False,
         realized=None, seg_delta=None):
    return {"seed": seed, "seat": seat, "margin": margin,
            "reads": {"mirror": mirror, "d29_margin": d29,
                      "stranding": strand,
                      "seg": {"realized_px": realized,
                              "seg_delta": seg_delta}}}


def test_endgame_stats_pairing():
    """d29 中位/stranding 均值/翻车翻正；缺字段→UNKNOWN 不短路。"""
    ours = [_row(1, 0, 100, d29=500, strand=10), _row(2, 0, -50, d29=-200,
                                                     strand=30)]
    base = [{"seed": 1, "seat": 0, "margin": -10,
             "reads": {"d29_margin": -100, "stranding": 40}},
            {"seed": 2, "seat": 0, "margin": 60,
             "reads": {"d29_margin": 100, "stranding": 20}}]
    out = j25.endgame_stats(ours, base)
    assert out["d29_margin_median"] == 500   # 上中位口径
    assert out["base_d29_median"] == 100
    assert out["stranding_mean"] == 20 and out["base_stranding_mean"] == 30
    assert out["flips"] == 1                      # seed1 L→W
    assert out["verdict"] == "PASS"              # d29 中位不劣+stranding 降
    unk = j25.endgame_stats([], [])
    assert unk["verdict"] == "FAIL" or unk["d29_margin_median"] == "UNKNOWN"


def test_mirror_arm_stats():
    """镜像子集胜率≥0.55 ∧ credit 净加卖=0 → PASS。"""
    games = [_row(1, 0, 100, mirror=True), _row(2, 0, 200, mirror=True),
             _row(3, 0, -10, mirror=False)]
    ok_ledger = {"boosted_total": 10, "repaid_total": 6,
                 "balance_total": 4}
    out = j25.mirror_arm_stats(games, ok_ledger)
    assert out["n"] == 2 and out["win_rate"] == 1.0
    assert out["net_add_sell"] == 0.0
    assert out["verdict"] == "PASS"
    bad = {"boosted_total": 10, "repaid_total": 2, "balance_total": 4}
    assert j25.mirror_arm_stats(games, bad)["verdict"] == "FAIL"
    assert j25.mirror_arm_stats([], None)["net_add_sell"] == "UNKNOWN"
