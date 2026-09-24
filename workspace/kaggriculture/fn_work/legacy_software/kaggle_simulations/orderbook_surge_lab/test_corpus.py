# -*- coding: utf-8 -*-
"""test_corpus —— corpus_select 组（发现/标注/胜局抽样可复现/fail-closed）。"""
import json

import pytest

from orderbook_surge_lab import corpus as C


def _mk_replay(ep, rewards=(120.0, 100.0), names=("renyxin", "oppA")):
    return {"info": {"EpisodeId": ep, "TeamNames": list(names)},
            "rewards": list(rewards), "steps": []}


@pytest.fixture
def tmp_corpus(tmp_path):
    for ep in (11, 2, 30):
        (tmp_path / f"episode-{ep}-replay.json").write_text(
            json.dumps(_mk_replay(ep)), encoding="utf-8")
    return tmp_path


# ---- 发现与标注 -------------------------------------------------------------
def test_discover_replays_sorted(tmp_corpus):
    found = C.discover_replays(str(tmp_corpus))
    assert [ep for ep, _ in found] == [2, 11, 30]
    assert all(p.endswith("episode-30-replay.json") for _, p in found[2:])


def test_discover_replays_bad_dir(tmp_path):
    with pytest.raises(OSError):
        C.discover_replays(str(tmp_path / "nope"))


def test_game_label_win_loss_error():
    assert C.game_label(_mk_replay(1))["res"] == "W"
    # renyxin 在 seat1：rewards[1]=90 < rewards[0]=120 → L，margin −30
    lab = C.game_label(_mk_replay(2, rewards=(120.0, 90.0),
                                  names=("x", "renyxin")))
    assert lab["seat"] == 1 and lab["res"] == "L" and lab["margin"] == -30.0
    lab = C.game_label(_mk_replay(3, names=("a", "b")))
    assert lab["error"]


# ---- 胜局抽样可复现 ----------------------------------------------------------
def test_win_sample_seed_reproducible():
    assert C.win_sample_seed() == C.win_sample_seed()
    assert isinstance(C.win_sample_seed(), int)


def test_sample_wins_deterministic_and_pools():
    pools = {"r32": [5, 6, 7, 8, 9], "r33": [1, 2, 3]}
    a, note_a = C.sample_wins(pools, 4)
    b, _ = C.sample_wins({k: list(v) for k, v in pools.items()}, 4)
    assert a == b
    assert len(a["r32"]) == 4 and len(a["r33"]) == 3  # 池小取 min
    assert note_a["per_tag"]["r32"]["pool"] == [5, 6, 7, 8, 9]
    assert "20260924r14" in note_a["seed_material"]


# ---- corpus_select ----------------------------------------------------------
def test_corpus_select_phase_a_only(tmp_corpus):
    sel = C.corpus_select(str(tmp_corpus))
    assert [e["episode"] for e in sel["phase_a"]] == [2, 11, 30]
    # 无报告时为轻量清单（episode/path；标签由 phase_a_attribution 补全）
    assert all(set(e) >= {"episode", "path"} for e in sel["phase_a"])
    assert sel["phase_b"] is None and sel["errors"] == []


def _report_entry(ep, res, treatable, tag=None):
    return {"episode": ep, "tag": tag, "res": res, "treatable": treatable,
            "seat": 0, "opp": "o", "margin": -1.0, "error": None}


def test_corpus_select_phase_b(tmp_corpus):
    # 11/2 胜局（r32/r33 池），30 败局可处置，2 号额外胜局不进 r 池
    report = {"per_game": [
        _report_entry(11, "W", False, "r32"),
        _report_entry(2, "W", False, "r33"),
        _report_entry(30, "L", True, "r32"),
        _report_entry(99, "L", True, None),  # 不在盘上 → 不入池不选择
        _report_entry(11, "W", False, "r32"),  # 重复无害（dict 覆盖）
    ]}
    sel = C.corpus_select(str(tmp_corpus), report)
    pb = sel["phase_b"]
    assert [g["episode"] for g in pb["losses"]] == [30]
    wins = [g["episode"] for g in pb["wins"]]
    assert wins == [2, 11]  # 数值升序（r32/r33 池各 1 全取）
    assert sel["sampling"]["per_tag"]["r32"]["picked"] == [11]
    assert sel["errors"] == []


def test_corpus_select_phase_b_error_entry_fail_closed(tmp_corpus):
    report = {"per_game": [_report_entry(30, "L", True),
                           {"episode": 11, "error": "boom"}]}
    sel = C.corpus_select(str(tmp_corpus), report)
    assert sel["errors"] and sel["errors"][0]["episode"] == 11
    assert [g["episode"] for g in sel["phase_b"]["losses"]] == [30]
