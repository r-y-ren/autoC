# -*- coding: utf-8 -*-
"""R15 单测：corpus_r15（抽样可复现/早崩排除/镜像池判据/缺回放 fail-closed）。"""
import json

import pytest

from orderbook_mix_lab import _base as B
from orderbook_mix_lab import corpus_r15 as C15


def _audit(games):
    return {"games": games}


def _row(ep, tag="r33", res="L", margin=-100.0, ourF=100000.0, oppF=100100.0,
         seat=0):
    return {"episode": ep, "tag": tag, "res": res, "margin": margin,
            "ourF": ourF, "oppF": oppF, "seat": seat, "opp": "opp"}


@pytest.fixture
def hermetic(monkeypatch, tmp_path):
    """隔离语料目录（r32 4 胜+r33 5 胜+29 败[含 3 早崩]+镜像池边界局）。"""
    eps = []
    games = []
    # r32 胜局池 4
    for i, ep in enumerate((9001, 9002, 9003, 9004)):
        games.append(_row(ep, "r32", "W", 5000.0, 150000.0, 145000.0))
        eps.append(ep)
    # r33 胜局池 5
    for ep in (9101, 9102, 9103, 9104, 9105):
        games.append(_row(ep, "r33", "W", 6000.0, 160000.0, 154000.0))
        eps.append(ep)
    # r33 败局 22 局普通败局（合计 26：22+2 镜像+2 边界外败局）
    for k in range(22):
        ep = 9200 + k
        games.append(_row(ep, "r33", "L", -800.0 - 100 * k))
        eps.append(ep)
    # 3 早崩（在 EARLY_CRASH 名单）
    for ep in B.EARLY_CRASH:
        games.append(_row(ep, "r33", "L", -22000.0))
        eps.append(ep)
    # 镜像近亲池：|margin|<400 且资金差<2%
    for ep, m, our, opp in ((9301, -300.0, 100000.0, 100100.0),
                            (9302, -350.0, 99000.0, 99200.0)):
        games.append(_row(ep, "r33", "L", m, our, opp))
        eps.append(ep)
    # 边界外：margin 合格但资金差 3%（不入池）
    games.append(_row(9303, "r33", "L", -100.0, 100000.0, 103000.0))
    eps.append(9303)
    # 边界外：资金差合格但 |margin|≥400
    games.append(_row(9304, "r33", "L", -401.0, 100000.0, 100100.0))
    eps.append(9304)

    replay_dir = tmp_path / "replays"
    replay_dir.mkdir()
    for ep in eps:
        (replay_dir / f"episode-{ep}-replay.json").write_text("{}", "utf-8")
    monkeypatch.setattr(C15._surge_corpus, "discover_replays",
                        lambda rd: [(ep, f"{rd}/episode-{ep}-replay.json")
                                    for ep in sorted(eps)])
    monkeypatch.setattr(C15._surge_corpus, "load_tag_map", lambda: {})
    return {"replay_dir": str(replay_dir), "audit": _audit(games),
            "eps": eps}


def test_reproducible_sampling_and_exclusions(hermetic):
    a = C15.select_corpus_r15(hermetic["replay_dir"], hermetic["audit"])
    b = C15.select_corpus_r15(hermetic["replay_dir"], hermetic["audit"])
    assert [e["episode"] for e in a["losses26"]] == \
           [e["episode"] for e in b["losses26"]]
    assert [e["episode"] for e in a["wins10"]] == \
           [e["episode"] for e in b["wins10"]]
    # 26 败局 = 29 排 3 早崩
    assert len(a["losses26"]) == 26
    assert not (set(e["episode"] for e in a["losses26"]) & set(B.EARLY_CRASH))
    # 胜局 10 = r32 4 + r33 5（池不足 5 取 4；sample 序=随机序，比集合）
    assert len(a["wins10"]) == 9
    assert sorted(a["sampling"]["picked_wins"]["r32"]) == [9001, 9002, 9003, 9004]
    # 镜像池判据：9301/9302 入、9303（资金差 3%）/9304（|margin|≥400）不入
    assert set(a["sampling"]["mirror_pool"]) == {9301, 9302}
    assert set(e["episode"] for e in a["mirror"]) == {9301, 9302}


def test_missing_replay_fail_closed(hermetic, monkeypatch):
    eps = list(hermetic["eps"])
    eps.remove(9200)
    monkeypatch.setattr(C15._surge_corpus, "discover_replays",
                        lambda rd: [(ep, f"{rd}/episode-{ep}-replay.json")
                                    for ep in sorted(eps)])
    out = C15.select_corpus_r15(hermetic["replay_dir"], hermetic["audit"])
    assert any(err["episode"] == 9200 for err in out["errors"])
    assert all(e["path"] for e in out["losses26"])


def test_seed_derivation():
    s1 = B.rng_seed("20260925r15")
    assert s1 == B.rng_seed("20260925r15")
    assert s1 != B.rng_seed("20260924r14")
