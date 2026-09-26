# -*- coding: utf-8 -*-
"""R19/R20 测试面：run_r37（编排/任一红即停/evidence 三件）。"""
import json
import os

import pytest

from orderbook_r37 import run_r37 as R

BUILD = {
    "main_path": "/x/r37/build/main.py",
    "main_sha256": "m" * 64, "tar_sha256": "t" * 64,
    "r34a_sha256": "r" * 64,
    "manifest": {"description": "public derivative with cash-floor guard "
                                "and earlier flock schedule",
                 "base_sha_chain": {"r34a": "r" * 64}},
    "diff_attribution": {"ok": True},
}
GREEN_REPLAY = {"overall": {"pass": True, "criteria": {"died": True}},
                "aggregate": {"disaster": {"n_games": 6}}}
GREEN_LEAGUE = {"overall": {"pass": True, "criteria": {"h2h": True}},
                "config": {"n_games_requested": 400}}
GREEN_GATES = {"overall": True,
               "gates_passed": {"compliance": True, "launch": True,
                                "h2h_vs_r34a": True, "lineage": True,
                                "starve": True},
               "summary_path": "/x/ev/gates_r37_realrun.json"}


def _patch_pipeline(monkeypatch, replay=None, league=None, gates=None,
                    build=None, build_exc=None):
    calls = {"build": 0, "replay": 0, "league": 0, "gates": 0}

    def fake_build(r34a_main_path, out_dir=None):
        calls["build"] += 1
        if build_exc:
            raise build_exc
        assert r34a_main_path == R.R34A_MAIN
        return dict(BUILD) if build is None else build

    def fake_replay(pkg_path, corpus):
        calls["replay"] += 1
        return dict(GREEN_REPLAY if replay is None else replay)

    def fake_league(r37_pkg, r34a_pkg, opponents, n_games):
        calls["league"] += 1
        assert r37_pkg == BUILD["main_path"]
        assert r34a_pkg == R.R34A_MAIN
        assert n_games == 400
        return dict(GREEN_LEAGUE if league is None else league)

    def fake_gates(pkg_path, evidence_dir=None):
        calls["gates"] += 1
        assert pkg_path == BUILD["main_path"]
        assert evidence_dir is not None
        return dict(GREEN_GATES if gates is None else gates)

    monkeypatch.setattr(R._b37, "build_r37", fake_build)
    monkeypatch.setattr(R._jr, "judge_cash_guard_replay", fake_replay)
    monkeypatch.setattr(R._jl, "judge_sheep_league", fake_league)
    monkeypatch.setattr(R._g37, "verify_r37_gates", fake_gates)
    return calls


def _ev(tmp_path, name):
    return json.loads((tmp_path / "evidence" / name).read_text())


def test_run_full_chain_orchestration(tmp_path, monkeypatch):
    """① 全链编排（mock 三阶段）：build→判决两件→门禁→发射；evidence 三件+台账。"""
    calls = _patch_pipeline(monkeypatch)
    result = R.run_r37_iteration(out_dir=str(tmp_path))
    assert set(result) == {"build", "judgments", "gates", "verdict"}
    assert calls == {"build": 1, "replay": 1, "league": 1, "gates": 1}
    assert set(result["judgments"]) == {"judge_cash_guard_replay",
                                        "judge_sheep_league"}
    # evidence 三件：build 审计/replay 判决/联赛判决
    assert "build" in _ev(tmp_path, R.EVIDENCE_BUILD)
    assert _ev(tmp_path, R.EVIDENCE_REPLAY)["overall"]["pass"] is True
    assert _ev(tmp_path, R.EVIDENCE_LEAGUE)["config"]["n_games_requested"] == 400
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["protocol"] == "run-r37/1.0"
    assert run_summary["stage"]["build"]["main_sha256"] == "m" * 64
    assert run_summary["stage"]["judgments"]["green"] is True


def test_judgment_red_no_gates_no_launch(tmp_path, monkeypatch):
    """② 判决红→不进门禁不发射（门禁段 skipped，无发射台账）。"""
    calls = _patch_pipeline(monkeypatch,
                            replay={"overall": {"pass": False,
                                                "criteria": {"died": False}}})
    result = R.run_r37_iteration(out_dir=str(tmp_path))
    assert calls["gates"] == 0                      # 不进门禁
    assert result["gates"]["skipped"] is True
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["verdict"] == "HOLD"
    assert result["verdict"]["standing_launch"] is None
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert _ev(tmp_path, R.EVIDENCE_RUN)["stage"]["gates"] == {
        "skipped": True, "overall": False}


def test_gates_red_no_launch(tmp_path, monkeypatch):
    """③ 门禁红→verdict 不发射（门禁照跑全量，发射段不进）。"""
    calls = _patch_pipeline(monkeypatch, gates={"overall": False,
                                                "gates_passed": {"launch": True,
                                                                 "starve": False},
                                                "summary_path": "/x/g.json"})
    result = R.run_r37_iteration(out_dir=str(tmp_path))
    assert calls["gates"] == 1
    assert result["gates"]["overall"] is False
    assert result["verdict"]["launch_ready"] is False
    assert result["verdict"]["verdict"] == "HOLD"
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()


def test_all_green_launch_ready_and_ledger(tmp_path, monkeypatch):
    """④ 全绿→launch_ready+台账留痕（launch_ledger standing 代执行记录）。"""
    _patch_pipeline(monkeypatch)
    result = R.run_r37_iteration(out_dir=str(tmp_path))
    assert result["verdict"]["launch_ready"] is True
    assert result["verdict"]["verdict"] == "LAUNCH"
    ledger = _ev(tmp_path, R.EVIDENCE_LAUNCH)
    assert "standing" in ledger["standing"]
    assert ledger["ref"] == "PENDING"
    assert ledger["artifacts"]["main_sha256"] == "m" * 64
    assert ledger["artifacts"]["tar_sha256"] == "t" * 64
    assert result["verdict"]["standing_launch"]["ledger_path"].endswith(
        R.EVIDENCE_LAUNCH)
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["verdict"]["launch_ready"] is True
    assert run_summary["verdict"]["standing_launch"]["ref"] == "PENDING"


def test_error_stops_and_records(tmp_path, monkeypatch):
    """Error 即停：构建红→run_summary 留痕后上抛，判决/门禁/发射全不进。"""
    calls = _patch_pipeline(monkeypatch,
                            build_exc=RuntimeError("build down"))
    with pytest.raises(RuntimeError, match="build down"):
        R.run_r37_iteration(out_dir=str(tmp_path))
    assert calls == {"build": 1, "replay": 0, "league": 0, "gates": 0}
    run_summary = _ev(tmp_path, R.EVIDENCE_RUN)
    assert run_summary["verdict"]["launch_ready"] is False
    assert "build down" in run_summary["error"]
    assert not (tmp_path / "evidence" / R.EVIDENCE_LAUNCH).exists()
    assert os.path.isdir(tmp_path / "evidence")
