# -*- coding: utf-8 -*-
"""R27 测试面：run_r44_iteration 编排（fail-closed 传递/预绑定收档/
台账留痕+计分对核对）。"""
from __future__ import annotations

import json
from pathlib import Path

from orderbook_r44 import run_r44 as r44


def _mk_build(tmp_path, form):
    d = Path(tmp_path) / ("out_%s" % form.lower())
    d.mkdir(parents=True, exist_ok=True)
    (d / "main.py").write_text("def _stub(observation, configuration=None):\n"
                               "    return {}\n", encoding="utf-8")
    return {"main_path": str(d / "main.py"), "out_dir": str(d),
            "main_sha256": "aa" * 32, "tar_sha256": "bb" * 32}


def _evidence(verdict="POSITIVE", forms=None):
    forms = forms or {"A": "PASS", "B": "FAIL", "AB": "PASS"}
    totals = {"A": 3, "B": 2, "AB": 4}
    crit = {}
    for f, v in forms.items():
        crit[f] = {"achieved": totals[f] if v == "PASS" else totals[f] - 1,
                   "total": totals[f], "h2h": 0.6, "realized_px": 0.85,
                   "verdict": v}
    return {"verdict": verdict, "arms": [], "criteria": crit}


def _wire(monkeypatch, tmp_path, calls, judge=None, gates=None,
          pytest_ok=True):
    monkeypatch.setattr(
        "orderbook_r44.build_r44.build_r44_variant",
        lambda base, form, out: calls.append(("build", form))
        or _mk_build(tmp_path, form))
    monkeypatch.setattr(
        r44, "_run_pytest",
        lambda cfg: calls.append("pytest") or {"passed": pytest_ok,
                                               "returncode": 0})
    monkeypatch.setattr(
        "orderbook_r44.judge_r44.judge_r44",
        judge or (lambda *a, **k: calls.append("judge") or _evidence()))
    monkeypatch.setattr(
        "orderbook_r44.gates_r44.verify_r44_gates",
        gates or (lambda pkg: calls.append(("gates", pkg))
                  or {"gates": {}, "overall": {"passed": True}}))


def test_run_positive_fork(monkeypatch, tmp_path):
    """判正→standing 发射：台账留痕+计分对核对（第 2 发挤 r37 保 r40）。"""
    calls = []
    _wire(monkeypatch, tmp_path, calls)
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert set(out) >= {"build", "judgment", "launch_form", "gates",
                        "verdict"}
    assert sorted(out["build"]) == ["A", "AB", "B"]        # build×3
    assert out["verdict"]["verdict"] == "POSITIVE"
    assert out["verdict"]["launch_ready"] is True
    assert out["launch_form"]["launch_form"] == "AB"       # 择优（达成 4）
    gate_calls = [c for c in calls if c[0] == "gates"]
    assert gate_calls and gate_calls[0][1].endswith("out_ab")  # 选定形态包
    led = json.loads((tmp_path / "ev" / "launch_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["form"] == "AB"
    assert led["entry"]["description"].startswith("public derivative")
    assert led["entry"]["scoring_pair"]["pair"] == ["r34a-new 56637411",
                                                   "r44 本件"]
    assert "挤 r37 保 r40" in led["entry"]["scoring_pair"]["note"]


def test_run_negative_judgment_archives(monkeypatch, tmp_path):
    calls = []
    _wire(monkeypatch, tmp_path, calls, judge=lambda *a, **k: (
        calls.append("judge") or _evidence(
            "NEGATIVE", {"A": "FAIL", "B": "FAIL", "AB": "FAIL"})))
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["verdict"]["launch_ready"] is False
    assert out["gates"] == {"skipped": True, "overall": {"passed": False}}
    assert not [c for c in calls if c[0] == "gates"]      # 门不跑
    led = json.loads((tmp_path / "ev" / "archive_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["verdict"] == "NEGATIVE"
    assert led["entry"]["archived_forms"] == ["A", "B", "AB"]


def test_run_killed_verdict_passes_through(monkeypatch, tmp_path):
    """KILLED（安慰剂破防）fail-closed 传递→收档不发射。"""
    calls = []
    _wire(monkeypatch, tmp_path, calls,
          judge=lambda *a, **k: calls.append("judge") or _evidence("KILLED"))
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert "KILLED" in out["verdict"]["reason"]


def test_run_gates_red_fail_closed(monkeypatch, tmp_path):
    calls = []
    _wire(monkeypatch, tmp_path, calls,
          gates=lambda pkg: calls.append(("gates", pkg))
          or {"gates": {"h2h": {"passed": False}},
              "overall": {"passed": False, "failed_gates": ["h2h"]}})
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["verdict"]["launch_ready"] is False
    assert "门禁红" in out["verdict"]["reason"]


def test_run_build_red_short_circuits(monkeypatch, tmp_path):
    calls = []

    def _build(base, form, out):
        calls.append(("build", form))
        if form == "B":
            raise RuntimeError("diff 审计白名单外")
        return _mk_build(tmp_path, form)

    _wire(monkeypatch, tmp_path, calls)
    monkeypatch.setattr("orderbook_r44.build_r44.build_r44_variant", _build)
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert "build" in out["verdict"]["reason"]
    assert "pytest" not in calls and "judge" not in calls   # 后续阶段不跑
    assert out["judgment"] == {"skipped": True}


def test_run_pytest_red_short_circuits(monkeypatch, tmp_path):
    calls = []
    _wire(monkeypatch, tmp_path, calls, pytest_ok=False)
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert "pytest" in out["verdict"]["reason"]
    assert "judge" not in calls                             # R27 ① 红不进判决


def test_run_judge_raises_fail_closed(monkeypatch, tmp_path):
    calls = []

    def _boom(*a, **k):
        calls.append("judge")
        raise RuntimeError("judge boom")

    _wire(monkeypatch, tmp_path, calls, judge=_boom)
    out = r44.run_r44_iteration({"evidence_dir": str(tmp_path / "ev")})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert "judgment" in out["verdict"]["reason"]
    assert out["launch_form"] == {"skipped": True}
    assert (tmp_path / "ev" / "archive_ledger.json").is_file()
