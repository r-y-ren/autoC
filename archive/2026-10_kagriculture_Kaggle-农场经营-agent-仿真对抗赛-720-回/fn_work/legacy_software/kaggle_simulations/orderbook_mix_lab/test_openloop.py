# -*- coding: utf-8 -*-
"""R15 单测：openloop（mock replay：Δ 计算/对照复用+抽验/红=fail-closed/预算）。"""
import pytest

from orderbook_mix_lab import openloop as OL


def _corpus():
    losses = [{"episode": 1, "path": "/tmp/l1.json", "seat": 0, "res": "L"},
              {"episode": 2, "path": "/tmp/l2.json", "seat": 1, "res": "L"}]
    wins = [{"episode": 3, "path": "/tmp/w3.json", "seat": 0, "res": "W"},
            {"episode": 4, "path": "/tmp/w4.json", "seat": 1, "res": "W"}]
    return {"losses26": losses, "wins10": wins}


def _variants():
    return [{"id": "vA", "pair": {"from": "MELON", "to": "WHEAT"},
             "scale": 0.3, "main_path": "/tmp/vA/main.py"},
            {"id": "vB", "pair": {"from": "MELON", "to": "WHEAT"},
             "scale": 0.2, "main_path": "/tmp/vB/main.py"}]


def _run_once_fake(margins, fail_eps=(), incomplete_eps=()):
    """(ep, seat, main) → margin 表驱动；fail_eps 连续抛异常。"""
    def fake(replay, main_path, seat):
        ep = replay["episode"]
        if (ep, seat, main_path) in fail_eps:
            raise RuntimeError("boom")
        res = {"margin": margins[(ep, seat, main_path)],
               "status": ("INCOMPLETE" if (ep, main_path) in incomplete_eps
                          else "DONE")}
        return res
    return fake


def test_delta_and_control_reuse(monkeypatch):
    margins = {}
    # 对照（l3 main）：ep1 双席、ep2 双席、ep3/ep4 原席
    for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
        for s in seats:
            margins[(ep, s, "L3")] = 100.0 + ep * 10 + s
    for v in _variants():
        for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
            for s in seats:
                margins[(ep, s, v["main_path"])] = \
                    margins[(ep, s, "L3")] + 25.0
    monkeypatch.setattr(OL, "_run_once", _run_once_fake(margins))
    monkeypatch.setattr(OL, "load_r14_control",
                        lambda *a, **k: ({}, None))
    monkeypatch.setattr(OL._surge_corpus, "load_replay",
                        lambda p: {"episode": int(p.split("/")[2].split(".")[0]
                                                  .replace("l", "")
                                                  .replace("w", ""))})
    out = OL.openloop_replay_variants(_variants(), _corpus(), "L3")
    # Δ=25 全席；败局局级=min(25,25)=25；胜局=原席 25
    for vid, vrec in out["per_variant"].items():
        for ep, g in vrec["games"].items():
            assert g["game_delta"] == 25.0
    s = out["summary"]
    assert s["control_fresh"] == 6 and s["control_reused"] == 0
    # 变体重演数 = 2 变体 × (2 败局×2 席 + 2 胜局×1 席) = 12
    assert s["n_replays"] == 6 + 12


def test_r14_reuse_and_spot_check(monkeypatch):
    margins = {}
    for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
        for s in seats:
            margins[(ep, s, "L3")] = 100.0
    for v in _variants():
        for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
            for s in seats:
                margins[(ep, s, v["main_path"])] = 100.0
    monkeypatch.setattr(OL, "_run_once", _run_once_fake(margins))
    r14 = {(1, 0): 100.0, (1, 1): 100.0, (2, 0): 100.0, (2, 1): 100.0}
    monkeypatch.setattr(OL, "load_r14_control", lambda *a, **k: (r14, "ts"))
    monkeypatch.setattr(OL._surge_corpus, "load_replay", lambda p: {"episode": 1})
    out = OL.openloop_replay_variants(_variants()[:1], _corpus(), "L3")
    s = out["summary"]
    assert s["control_reused"] == 4 and s["reuse_ok"] is True
    assert len(s["spot_drift"]) == OL.SPOT_CHECK_N
    assert all(d["drift"] == 0.0 for d in s["spot_drift"])


def test_red_fail_closed(monkeypatch):
    margins = {(1, 0, "L3"): 100.0, (1, 1, "L3"): 100.0,
               (2, 0, "L3"): 100.0, (2, 1, "L3"): 100.0,
               (3, 0, "L3"): 100.0, (4, 1, "L3"): 100.0}
    vA = _variants()[0]
    for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
        for s in seats:
            margins[(ep, s, vA["main_path"])] = 120.0
    monkeypatch.setattr(OL, "_run_once",
                        _run_once_fake(margins,
                                       fail_eps={(1, 0, vA["main_path"])},
                                       incomplete_eps={(2, vA["main_path"])}))
    monkeypatch.setattr(OL, "load_r14_control", lambda *a, **k: ({}, None))
    monkeypatch.setattr(OL._surge_corpus, "load_replay",
                        lambda p: {"episode": 1})
    out = OL.openloop_replay_variants([vA], _corpus(), "L3")
    games = out["per_variant"]["vA"]["games"]
    assert games["1"]["red"] is True
    assert games["1"]["seats"]["seat0"]["red"] is True
    assert games["2"]["red"] is True     # INCOMPLETE → 红


def test_budget_stop(monkeypatch):
    margins = {}
    vA = _variants()[0]
    for ep, seats in ((1, (0, 1)), (2, (0, 1)), (3, (0,)), (4, (1,))):
        for s in seats:
            margins[(ep, s, "L3")] = 100.0
            margins[(ep, s, vA["main_path"])] = 110.0
    monkeypatch.setattr(OL, "_run_once", _run_once_fake(margins))
    monkeypatch.setattr(OL, "load_r14_control", lambda *a, **k: ({}, None))
    monkeypatch.setattr(OL._surge_corpus, "load_replay",
                        lambda p: {"episode": 1})
    out = OL.openloop_replay_variants([vA], _corpus(), "L3", budget=7)
    assert out["summary"]["budget_stopped"] is True
    assert out["summary"]["n_replays"] <= 7
