# -*- coding: utf-8 -*-
"""R23 测试面：run_r40（编排/分项总判/判负收档）。

5 例沿 B24 先例（orderbook_predict/test_run_r38.py）：①全链 mock 全绿
POSITIVE ②判红 NEGATIVE 收档+门禁不进（计数证明）③门禁红不发射 ④Error
留痕上抛 ⑤收档台账形态（archive_note 原文）。judge_r23 并行实现中——全组
monkeypatch 桩（接口=judge_r23(pkg, corpus, bench)→evidence 含六判据
overall）；SIX_ALL 六判据名=测试占位名（判定只读 overall.criteria+overall.
pass，与真名解耦）。
"""
import copy
import json
import os

import pytest

from orderbook_r40 import run_r40 as R

BUILD = {
    "main_path": "/x/r40/build/main.py",
    "main_sha256": "m" * 64, "tar_sha256": "t" * 64,
    "block_sha": "b" * 64, "library_sha256": "a" * 64,
    "sell_lots_change_sha256": "s" * 64,
    "manifest": {"description": "public derivative with route library and "
                                "late-season sell execution",
                 "base_sha_chain": {"a16e0e9b": "e" * 64, "r34a": "4" * 64,
                                    "r37": "3" * 64, "r40": "m" * 64}},
}
SIX_ALL = ("loss_replay_no_regression", "league_vs_top_ge_055",
           "seg_funds_d21_28_up", "realized_px_up", "fill_rate_up",
           "sim_consistency_30of30")
GREEN_JUDGE = {"overall": {"criteria": {k: True for k in SIX_ALL},
                           "pass": True, "verdict": "POSITIVE"},
               "corpus": {"n_loss_replays": 12}}
# 判红样例：2 绿 4 红（分项+总判红即判负，不许改判）
RED_JUDGE = {"overall": {"criteria": {"loss_replay_no_regression": False,
                                      "league_vs_top_ge_055": False,
                                      "seg_funds_d21_28_up": False,
                                      "realized_px_up": True,
                                      "fill_rate_up": True,
                                      "sim_consistency_30of30": False},
                         "pass": False, "verdict": "NEGATIVE"},
             "corpus": {"n_loss_replays": 12}}
GREEN_GATES = {"overall": True,
               "gates_passed": {"compliance": True, "launch": True,
                                "h2h_vs_r37": True, "lineage": True,
                                "starve": True}}
RED_GATES = {"overall": False,
             "gates_passed": {"compliance": True, "launch": True,
                              "h2h_vs_r37": False, "lineage": True,
                              "starve": True}}


def _patch_pipeline(monkeypatch, build=None, judgment=None, gates=None,
                    build_exc=None):
    calls = {"build": 0, "judgment": 0, "gates": 0, "judge_args": None}

    def fake_build(r37_main_path, out_dir=None):
        calls["build"] += 1
        if build_exc:
            raise build_exc
        assert r37_main_path == R.R37_MAIN
        assert out_dir is not None and out_dir.endswith("build")
        return copy.deepcopy(BUILD if build is None else build)

    def fake_judge(pkg_path, corpus, bench):
        calls["judgment"] += 1
        calls["judge_args"] = (pkg_path, corpus, bench)
        assert pkg_path == BUILD["main_path"]
        return copy.deepcopy(GREEN_JUDGE if judgment is None else judgment)

    def fake_gates(pkg_path, evidence_dir=None):
        calls["gates"] += 1
        assert pkg_path == BUILD["main_path"]
        assert evidence_dir is not None
        ev = copy.deepcopy(GREEN_GATES if gates is None else gates)
        ev["summary_path"] = os.path.join(evidence_dir, R.EVIDENCE_GATES)
        with open(ev["summary_path"], "w", encoding="utf-8") as fh:   # 自写台账
            json.dump(ev, fh, ensure_ascii=False)
        return ev

    monkeypatch.setattr(R._b40, "build_r40", fake_build)
    monkeypatch.setattr(R._j23, "judge_r23", fake_judge)
    monkeypatch.setattr(R._g40, "verify_r40_gates", fake_gates)
    return calls


def _ev(tmp_path, name):
    return json.loads((tmp_path / "evidence" / name).read_text())


def test_run_full_chain_orchestration(tmp_path, monkeypatch):
    """① 全链 mock 全绿：构建→判决（六判据）→门禁→POSITIVE；evidence+发射台账。"""
    calls = _patch_pipeline(monkeypatch)
    result = R.run_r40_iteration(out_dir=str(tmp_path))
    assert set(result) == {"build", "judgment", "gates", "verdict"}
    assert calls["build"] == 1
    assert calls["judgment"] == 1 and calls["gates"] == 1
    pkg_path, corpus, bench = calls["judge_args"]
    assert pkg_path == BUILD["main_path"]
    assert corpus == list(R.DEFAULT_CORPUS)     # 败局 12 局缺省语料
    assert len(corpus) == 12
    assert bench is None                        # 缺省=judge_r23 验收档
    assert result["verdict"]["verdict"] == "POSITIVE"
    assert result["verdict"]["launch_ready"] is True
    assert result["verdict"]["reason"] is None
    assert result["verdict"]["archive_ledger"] is None
    # evidence 三件：构建审计/判决/门禁台账
    assert _ev(tmp_path, R.EVIDENCE_BUILD)["build"]["main_sha256"] == "m" * 64
    assert _ev(tmp_path, R.EVIDENCE_JUDGMENT)["overall"]["pass"] is True
    assert _ev(tmp_path, R.EVIDENCE_GATES)["overall"] is True
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["protocol"] == "run-r40/1.0"
    assert run_summary["stage"]["build"]["main_sha256"] == "m" * 64
    assert run_summary["stage"]["build"]["library_sha256"] == "a" * 64
    assert run_summary["stage"]["judgment"]["pass"] is True
    assert run_summary["stage"]["judgment"]["n_criteria"] == 6
    assert run_summary["stage"]["gates"]["overall"] is True
    assert run_summary["verdict"]["standing_launch"]["ref"] == "PENDING"
    assert result["verdict"]["standing_launch"]["ledger_path"].endswith(
        R.EVIDENCE_LAUNCH)


def test_judgment_red_no_gates_archive(tmp_path, monkeypatch):
    """② 六判据红→NEGATIVE 收档+不进门禁（门禁计数 0）+不建发射版。"""
    calls = _patch_pipeline(monkeypatch, judgment=RED_JUDGE)
    result = R.run_r40_iteration(out_dir=str(tmp_path))
    assert calls["gates"] == 0                      # 不进门禁（计数证明）
    assert result["gates"]["skipped"] is True
    assert result["verdict"]["verdict"] == "NEGATIVE"
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["judgment_green"] is False
    assert result["verdict"]["gates_green"] is False
    assert "六判据红" in result["verdict"]["reason"]
    assert result["verdict"]["standing_launch"] is None
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert (tmp_path / "evidence" / R.EVIDENCE_ARCHIVE).exists()   # 收档台账
    assert _ev(tmp_path, R.EVIDENCE_RUN)["stage"]["gates"] == {
        "skipped": True, "overall": False}
    red = _ev(tmp_path, R.EVIDENCE_RUN)["stage"]["judgment"]["red"]
    assert red == ["loss_replay_no_regression", "league_vs_top_ge_055",
                   "seg_funds_d21_28_up", "sim_consistency_30of30"]


def test_gates_red_no_launch(tmp_path, monkeypatch):
    """③ 门禁红→不发射（六判据全绿也只收档；bench 副证配置透传 judge）。"""
    calls = _patch_pipeline(monkeypatch, gates=RED_GATES)
    bench = {"n_league": 300}
    result = R.run_r40_iteration(out_dir=str(tmp_path), bench=bench)
    assert calls["judgment"] == 1 and calls["gates"] == 1
    assert calls["judge_args"][2] == bench
    assert result["gates"]["overall"] is False
    assert result["verdict"]["verdict"] == "NEGATIVE"   # 任一红即判负
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["judgment_green"] is True
    assert "门禁红" in result["verdict"]["reason"]
    assert "h2h_vs_r37" in result["verdict"]["reason"]
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert (tmp_path / "evidence" / R.EVIDENCE_ARCHIVE).exists()


def test_error_stops_and_records(tmp_path, monkeypatch):
    """④ Error 即停留痕：构建红→run_summary 记 error 后上抛，判决/门禁不进。"""
    calls = _patch_pipeline(monkeypatch, build_exc=RuntimeError("build down"))
    with pytest.raises(RuntimeError, match="build down"):
        R.run_r40_iteration(out_dir=str(tmp_path))
    assert calls["build"] == 1
    assert calls["judgment"] == 0 and calls["gates"] == 0
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["verdict"]["launch_ready"] is False
    assert "build down" in run_summary["error"]
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert not (tmp_path / "evidence" / R.EVIDENCE_ARCHIVE).exists()
    assert os.path.isdir(tmp_path / "evidence")


def test_negative_archive_ledger_shape(tmp_path, monkeypatch):
    """⑤ 判负收档台账形态：archive_note 原文+件身份+reason，不建发射版。"""
    _patch_pipeline(monkeypatch, judgment=RED_JUDGE)
    result = R.run_r40_iteration(out_dir=str(tmp_path))
    ledger = _ev(tmp_path, R.EVIDENCE_ARCHIVE)
    assert ledger["protocol"] == "run-r40-archive/1.0"
    assert ledger["archive_note"] == "判负收档留赛后资产，不建发射版"
    assert ledger["verdict"] == "NEGATIVE"
    assert ledger["launch_ready"] is False
    assert ledger["reason"].startswith("六判据红")
    assert ledger["artifacts"]["main_sha256"] == "m" * 64
    assert ledger["artifacts"]["tar_sha256"] == "t" * 64
    assert ledger["artifacts"]["library_sha256"] == "a" * 64
    assert ledger["artifacts"]["sell_lots_change_sha256"] == "s" * 64
    assert ledger["artifacts"]["base_sha_chain"] == {"a16e0e9b": "e" * 64,
                                                     "r34a": "4" * 64,
                                                     "r37": "3" * 64,
                                                     "r40": "m" * 64}
    assert ledger["artifacts"]["description"].startswith("public derivative")
    assert ledger["gates"] == {"skipped": True, "overall": False}
    assert ledger["gates_ledger"] is None          # 未进门禁无门禁台账
    assert result["verdict"]["archive_ledger"]["archive_note"] == (
        "判负收档留赛后资产，不建发射版")
    assert result["verdict"]["archive_ledger"]["ledger_path"].endswith(
        R.EVIDENCE_ARCHIVE)
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
