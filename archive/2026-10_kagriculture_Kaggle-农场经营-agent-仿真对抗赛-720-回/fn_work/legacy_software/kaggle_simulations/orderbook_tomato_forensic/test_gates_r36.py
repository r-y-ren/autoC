# -*- coding: utf-8 -*-
"""R18 测试面：gates_r36（fail-closed 全跑/身份链传导/未构建红）。
门主体经 monkeypatch 重定向，不跑真重演（真跑面由 S3 CLI 承载）。"""
import json

import pytest

from orderbook_tomato_forensic import gates_r36 as g36


def _make_pkg(tmp_path, last_callable="_cxd_agent"):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "main.py").write_text("def _cxd_agent(o, c=None):\n    return {}\n",
                                 encoding="utf-8")
    (pkg / "build_manifest.json").write_text(
        json.dumps({"schema": "orderbook_r36_manifest/1.0", "variant": "r36",
                    "last_callable": last_callable}), encoding="utf-8")
    return str(pkg)


def test_not_built_raises(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(g36.GateR36Error):
        g36.verify_r36_gates(str(empty))


def test_manifest_last_callable_guard(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "main.py").write_text("x=1\n", encoding="utf-8")
    (pkg / "build_manifest.json").write_text(
        json.dumps({"last_callable": "weird_agent"}), encoding="utf-8")
    with pytest.raises(g36.GateR36Error):
        g36.verify_r36_gates(str(pkg))


def _patch_gates(monkeypatch, results):
    """results: dict gate-name → (passed, payload)。缺省全绿。"""
    defaults = {
        "launch": (True, {"passed": True,
                          "gates": {"package": True, "load": True,
                                    "full_episodes": True, "determinism": True}}),
        "h2h": (True, {"n": 16, "wins": 10, "losses": 6, "ties": 0,
                       "rate": 0.625, "mean_margin": 120.0}),
        "lineage": (True, {"per_opponent": {
            "v48-pure": {"n": 8, "wins": 8, "losses": 0, "ties": 0,
                         "all_done": True},
            "v4b": {"n": 8, "wins": 8, "losses": 0, "ties": 0,
                    "all_done": True}}}),
        "starve": (True, {"starve_free": True, "n_games": 26, "n_errors": 0,
                          "n_starve_red_games": 0, "subset": True}),
        "diff": (True, {"attribution": {"wheat_step91_threshold(scan winner)": 1}}),
    }
    merged = dict(defaults)
    merged.update(results)
    monkeypatch.setattr(g36, "_gate_launch_fourgate",
                        lambda pkg, last: merged["launch"][1])
    monkeypatch.setattr(g36, "_gate_h2h_vs_r34a",
                        lambda main, last, ev: dict(passed=merged["h2h"][0],
                                                    **merged["h2h"][1]))
    monkeypatch.setattr(g36, "_gate_lineage",
                        lambda main, ev: dict(passed=merged["lineage"][0],
                                              **merged["lineage"][1]))
    monkeypatch.setattr(g36, "_gate_starve_subset",
                        lambda main, ev: dict(passed=merged["starve"][0],
                                              **merged["starve"][1]))
    monkeypatch.setattr(g36, "_gate_diff_audit",
                        lambda r34a, main, ev: dict(passed=merged["diff"][0],
                                                    **merged["diff"][1]))
    return merged


def test_all_green_overall_pass(tmp_path, monkeypatch):
    _patch_gates(monkeypatch, {})
    summary = g36.verify_r36_gates(_make_pkg(tmp_path))
    assert summary["overall"] is True
    assert all(summary["gates_passed"].values())
    assert summary["mains"]["last_callable"] == "_cxd_agent"


def test_fail_closed_runs_all_gates(tmp_path, monkeypatch):
    _patch_gates(monkeypatch, {
        "h2h": (False, {"n": 16, "wins": 8, "losses": 8, "ties": 0,
                        "rate": 0.5, "mean_margin": -166.5})})
    summary = g36.verify_r36_gates(_make_pkg(tmp_path))
    assert summary["overall"] is False
    assert summary["gates_passed"]["h2h_vs_r34a"] is False
    # fail-closed：其余门照跑
    assert summary["gates_passed"]["launch"] is True
    assert summary["gates_passed"]["diff_audit"] is True


def test_exec_failure_marks_not_executed(tmp_path, monkeypatch):
    def boom(pkg, last):
        raise RuntimeError("fourgate explode")
    monkeypatch.setattr(g36, "_gate_launch_fourgate", boom)
    _patch_gates(monkeypatch, {})
    monkeypatch.setattr(g36, "_gate_launch_fourgate", boom)
    summary = g36.verify_r36_gates(_make_pkg(tmp_path))
    assert summary["overall"] is False
    assert summary["gates"]["launch"]["executed"] is False
    assert "explode" in summary["gates"]["launch"]["error"]


def test_stepped_last_callable_accepted(tmp_path, monkeypatch):
    _patch_gates(monkeypatch, {})
    summary = g36.verify_r36_gates(_make_pkg(tmp_path, last_callable="_r36_agent"))
    assert summary["mains"]["last_callable"] == "_r36_agent"
    assert summary["overall"] is True
