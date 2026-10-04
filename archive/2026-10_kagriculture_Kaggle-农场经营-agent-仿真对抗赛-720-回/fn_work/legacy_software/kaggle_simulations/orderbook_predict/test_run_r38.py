# -*- coding: utf-8 -*-
"""R21 测试面：run_r38（编排/判负收档/全绿交发射）。"""
import copy
import json
import os

import pytest

from orderbook_predict import run_r38 as R

LIBRARY = {
    "library": {"version": "sellflow/1.0",
                "keys": {"k1": {"n_episodes": 1, "hist": {}},
                         "k2": {"n_episodes": 1, "hist": {}}},
                "global": {"n_episodes": 86, "hist": {}}},
    "build_audit": {"replay_dir": "/tmp/r33audit", "n_files": 86, "n_used": 86,
                    "n_skipped": 0, "total_events": 29470,
                    "sha256_of_library": "a" * 64},
}
BUILD = {
    "main_path": "/x/r38/build/main.py",
    "main_sha256": "m" * 64, "tar_sha256": "t" * 64,
    "block_sha": "b" * 64, "library_sha256": "a" * 64,
    "manifest": {"description": "public derivative with opponent sell "
                                "prediction (front-run + dodge)",
                 "base_sha_chain": {"r37": "3" * 64}},
    "r37_main_path": R.R37_MAIN, "r37_sha256": "3" * 64,
}
GREEN_JUDGE = {"overall": {"criteria": {"control_not_flipped": True,
                                        "late_flip_ge_third": True,
                                        "h2h_vs_r37_ge_055": True},
                           "pass": True, "verdict": "POSITIVE"},
               "corpus": {"n_entries": 36}}
RED_JUDGE = {"overall": {"criteria": {"control_not_flipped": False,
                                      "late_flip_ge_third": False,
                                      "h2h_vs_r37_ge_055": False},
                         "pass": False, "verdict": "NEGATIVE"},
             "corpus": {"n_entries": 36}}
GREEN_GATES = {"overall": True,
               "gates_passed": {"compliance": True, "launch": True,
                                "h2h_vs_r37": True, "lineage": True,
                                "starve": True}}
RED_GATES = {"overall": False,
             "gates_passed": {"compliance": True, "launch": True,
                              "h2h_vs_r37": False, "lineage": True,
                              "starve": True}}


def _patch_pipeline(monkeypatch, library=None, build=None, judgment=None,
                    gates=None, build_exc=None):
    calls = {"library": 0, "build": 0, "judgment": 0, "gates": 0,
             "judge_args": None}

    def fake_library(replay_dir):
        calls["library"] += 1
        assert replay_dir == "/tmp/r33audit"
        return copy.deepcopy(LIBRARY if library is None else library)

    def fake_build(r37_main_path, out_dir=None):
        calls["build"] += 1
        if build_exc:
            raise build_exc
        assert r37_main_path == R.R37_MAIN
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

    monkeypatch.setattr(R._sf, "build_sellflow_library", fake_library)
    monkeypatch.setattr(R._b38, "build_r38", fake_build)
    monkeypatch.setattr(R._jp, "judge_predict_replay", fake_judge)
    monkeypatch.setattr(R._g38, "verify_r38_gates", fake_gates)
    return calls


def _ev(tmp_path, name):
    return json.loads((tmp_path / "evidence" / name).read_text())


def test_run_full_chain_orchestration(tmp_path, monkeypatch):
    """① 全链 mock 全绿：建库→构建→判决→门禁→POSITIVE；evidence 四件+发射台账。"""
    calls = _patch_pipeline(monkeypatch)
    result = R.run_r38_iteration(out_dir=str(tmp_path))
    assert set(result) == {"library", "build", "judgment", "gates", "verdict"}
    assert calls["library"] == 1 and calls["build"] == 1
    assert calls["judgment"] == 1 and calls["gates"] == 1
    pkg_path, corpus, bench = calls["judge_args"]
    assert pkg_path == BUILD["main_path"]
    assert corpus == list(R.DEFAULT_CORPUS)     # 26 败局+10 对照（36 条目）
    assert len(corpus) == 36
    assert bench is None                        # 缺省=judge 验收档
    assert result["library"]["build_audit"]["n_used"] == 86
    assert result["verdict"]["verdict"] == "POSITIVE"
    assert result["verdict"]["launch_ready"] is True
    assert result["verdict"]["reason"] is None
    assert result["verdict"]["archive_ledger"] is None
    # evidence 四件：建库审计/构建审计/判决/门禁台账
    assert _ev(tmp_path, R.EVIDENCE_LIBRARY)["n_keys"] == 2
    assert _ev(tmp_path, R.EVIDENCE_BUILD)["build"]["main_sha256"] == "m" * 64
    assert _ev(tmp_path, R.EVIDENCE_JUDGMENT)["overall"]["pass"] is True
    assert _ev(tmp_path, R.EVIDENCE_GATES)["overall"] is True
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["protocol"] == "run-r38/1.0"
    assert run_summary["stage"]["build"]["main_sha256"] == "m" * 64
    assert run_summary["stage"]["judgment"]["pass"] is True
    assert run_summary["stage"]["gates"]["overall"] is True
    assert run_summary["verdict"]["standing_launch"]["ref"] == "PENDING"
    assert result["verdict"]["standing_launch"]["ledger_path"].endswith(
        R.EVIDENCE_LAUNCH)


def test_judgment_red_no_gates_archive(tmp_path, monkeypatch):
    """② 判决红→NEGATIVE 收档+不进门禁（门禁计数 0）+不建发射版。"""
    calls = _patch_pipeline(monkeypatch, judgment=RED_JUDGE)
    result = R.run_r38_iteration(out_dir=str(tmp_path))
    assert calls["gates"] == 0                      # 不进门禁（计数证明）
    assert result["gates"]["skipped"] is True
    assert result["verdict"]["verdict"] == "NEGATIVE"
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["judgment_green"] is False
    assert result["verdict"]["gates_green"] is False
    assert "判决判据红" in result["verdict"]["reason"]
    assert result["verdict"]["standing_launch"] is None
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert (tmp_path / "evidence" / R.EVIDENCE_ARCHIVE).exists()   # 收档台账
    assert _ev(tmp_path, R.EVIDENCE_RUN)["stage"]["gates"] == {
        "skipped": True, "overall": False}


def test_gates_red_no_launch(tmp_path, monkeypatch):
    """③ 门禁红→不发射（判决全绿也只收档；n_judgment 传副证主对局数）。"""
    calls = _patch_pipeline(monkeypatch, gates=RED_GATES)
    result = R.run_r38_iteration(out_dir=str(tmp_path), n_judgment=12)
    assert calls["judgment"] == 1 and calls["gates"] == 1
    assert calls["judge_args"][2] == {"n_games_main": 12}
    assert result["gates"]["overall"] is False
    assert result["verdict"]["verdict"] == "NEGATIVE"   # 任一判据红即判负
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["judgment_green"] is True
    assert "门禁红" in result["verdict"]["reason"]
    assert "h2h_vs_r37" in result["verdict"]["reason"]
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert (tmp_path / "evidence" / R.EVIDENCE_ARCHIVE).exists()


def test_error_stops_and_records(tmp_path, monkeypatch):
    """④ Error 即停留痕：建库后构建红→run_summary 记 error 后上抛，判决/门禁不进。"""
    calls = _patch_pipeline(monkeypatch, build_exc=RuntimeError("build down"))
    with pytest.raises(RuntimeError, match="build down"):
        R.run_r38_iteration(out_dir=str(tmp_path))
    assert calls["library"] == 1 and calls["build"] == 1
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
    result = R.run_r38_iteration(out_dir=str(tmp_path))
    ledger = _ev(tmp_path, R.EVIDENCE_ARCHIVE)
    assert ledger["protocol"] == "run-r38-archive/1.0"
    assert ledger["archive_note"] == "判负收档留赛后资产，不建发射版"
    assert ledger["verdict"] == "NEGATIVE"
    assert ledger["launch_ready"] is False
    assert ledger["reason"].startswith("判决判据红")
    assert ledger["artifacts"]["main_sha256"] == "m" * 64
    assert ledger["artifacts"]["tar_sha256"] == "t" * 64
    assert ledger["artifacts"]["base_sha_chain"] == {"r37": "3" * 64}
    assert ledger["gates"] == {"skipped": True, "overall": False}
    assert ledger["gates_ledger"] is None          # 未进门禁无门禁台账
    assert result["verdict"]["archive_ledger"]["archive_note"] == (
        "判负收档留赛后资产，不建发射版")
    assert result["verdict"]["archive_ledger"]["ledger_path"].endswith(
        R.EVIDENCE_ARCHIVE)
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
