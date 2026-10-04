# -*- coding: utf-8 -*-
"""R15 单测：closedloop（mock 引擎：互胜/margin 分布/重跑一次/红局）。"""
import pytest

from orderbook_mix_lab import closedloop as CL


def _variants():
    return [{"id": "vA", "main_path": "/tmp/vA/main.py"},
            {"id": "vB", "main_path": "/tmp/vB/main.py"}]


def _mirror():
    return [{"episode": 11, "path": "/tmp/m11.json"},
            {"episode": 12, "path": "/tmp/m12.json"}]


def test_probe_rates_and_medians(monkeypatch):
    state = {"n": 0}

    def duel_fake(replay, variant_main, l3_main, variant_seat, **kw):
        # vA 全胜（margin>0）；vB 全负；定向 1 INCOMPLETE（红）
        vid = "vA" if "vA" in variant_main else "vB"
        ep = replay["episode"]
        if vid == "vA":
            m = 150.0 if variant_seat == 0 else 50.0
            status = "DONE"
        else:
            m = -80.0
            status = "INCOMPLETE" if (ep == 12 and variant_seat == 1) else "DONE"
        return {"margin": m, "finals": [0, 0], "status": status,
                "steps_n": 720, "wall_s": 0.01}

    monkeypatch.setattr(CL, "duel", duel_fake)
    monkeypatch.setattr(
        CL._surge_corpus, "load_replay",
        lambda p: {"episode": int(p.split("/")[-1].split(".")[0][1:])})
    out = CL.closedloop_probe(_variants(), _mirror(), "L3")
    va = out["per_variant"]["vA"]
    assert va["runs"] == 4 and va["wins"] == 4 and va["rate"] == 1.0
    assert va["median_margin"] == 100.0     # {150,50,150,50} 中位
    assert va["red_runs"] == 0
    vb = out["per_variant"]["vB"]
    assert vb["wins"] == 0 and vb["rate"] == 0.0
    assert vb["red_runs"] == 1              # ep12 定向 1 INCOMPLETE
    assert vb["margins"] == [-80.0, -80.0, -80.0]   # 红定向不计 margin
    assert out["summary"]["n_runs"] == 8


def test_probe_retry_once_then_red(monkeypatch):
    calls = {"n": 0}

    def duel_flaky(replay, variant_main, l3_main, variant_seat, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("first fails")
        return {"margin": 10.0, "finals": [0, 0], "status": "DONE",
                "steps_n": 720, "wall_s": 0.01}

    def duel_dead(replay, variant_main, l3_main, variant_seat, **kw):
        raise RuntimeError("always fails")

    monkeypatch.setattr(CL._surge_corpus, "load_replay", lambda p: {"episode": 11})
    monkeypatch.setattr(CL, "duel", duel_flaky)
    out = CL.closedloop_probe(_variants()[:1], _mirror()[:1], "L3")
    rec = out["per_variant"]["vA"]
    assert calls["n"] == 3                  # 首败重跑一次成功 + 第二定向 1 次
    assert rec["red_runs"] == 0 and rec["wins"] == 2 and rec["runs"] == 2
    monkeypatch.setattr(CL, "duel", duel_dead)
    out2 = CL.closedloop_probe(_variants()[:1], _mirror()[:1], "L3")
    rec2 = out2["per_variant"]["vA"]
    assert rec2["red_runs"] == 2 and rec2["margins"] == []


def test_obs_dict_shape():
    class Obs:
        pass

    class Seat:
        def __init__(self, priv, day, hour):
            o = Obs()
            o.private = priv
            o.day, o.hour = day, hour
            self.observation = o

    class State:
        seats = None

    s0, s1 = Seat({"shed": {}}, 3, 12), Seat({"shed": {}}, 3, 12)
    s0.observation.farms = [1]
    s0.observation.market = {"prices": {}}
    s0.observation.town = {"unlocked_shops": []}
    s0.observation.step = 77
    st = State()
    st.seats = [s0, s1]
    d = CL._obs_dict(st, 1)
    assert d["player"] == 1 and d["step"] == 77 and d["day"] == 3
    assert d["private"] == {"shed": {}}
