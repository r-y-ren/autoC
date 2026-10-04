# -*- coding: utf-8 -*-
"""R17 测试面：run_r35 编排。"""
import json

import pytest

from orderbook_r35 import run_r35 as R


def test_run_full_flow(tmp_path, monkeypatch):
    monkeypatch.setattr(R._pv, "phase_v_adjudicate",
                        lambda: {"sheep": {"adopt": True,
                                           "params": {"sheep_buy": 8}},
                                 "tomato": {"adopt": False, "params": None},
                                 "route": {"adopt": True,
                                           "params": {"_V93_ROUTE_BY_RIVAL":
                                                      {"(1.0, 2)": 5}}},
                                 "errors": [],
                                 "evidence_path": "pv.json"})
    monkeypatch.setattr(R._b35, "R34A_MAIN", "/base/main.py")
    monkeypatch.setattr(R._b35, "build_r35",
                        lambda adopt, base, out: {
                            "ok": True, "adopted": {"ca_margin": True},
                            "main_sha256": "x", "main_bytes": 1,
                            "tar_sha256": "y", "tar_bytes": 2,
                            "diff_attribution": {}})
    monkeypatch.setattr(R._g35, "verify_r35_gates",
                        lambda pkg: {"overall": True,
                                     "gates_passed": {"launch": True}})
    result = R.run_r35_iteration(out_dir=str(tmp_path))
    assert result["launch_ready"] is True
    assert result["stage"]["phase_v"]["adopted"] == {
        "sheep": True, "tomato": False, "route": True}
    summary = json.loads((tmp_path / "evidence" / "run_summary.json").read_text())
    assert summary["protocol"] == "run-r35/1.0"


def test_run_fail_path_writes_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(R._pv, "phase_v_adjudicate",
                        lambda: {"sheep": {"adopt": False},
                                 "tomato": {"adopt": False},
                                 "route": {"adopt": False},
                                 "errors": [], "evidence_path": "pv.json"})
    def boom(adopt, base, out):
        raise RuntimeError("build down")
    monkeypatch.setattr(R._b35, "build_r35", boom)
    with pytest.raises(RuntimeError):
        R.run_r35_iteration(out_dir=str(tmp_path))
    fail = json.loads((tmp_path / "evidence" / "run_summary.json").read_text())
    assert fail["launch_ready"] is False
    assert "build down" in fail["error"]
    assert fail["stage"]["phase_v"] is not None


def test_main_skip_phase_v(tmp_path, monkeypatch, capsys):
    pv_path = tmp_path / "pv.json"
    pv_path.write_text(json.dumps({
        "sheep": {"adopt": False}, "tomato": {"adopt": False},
        "route": {"adopt": False}, "errors": []}))
    monkeypatch.setattr(R._b35, "R34A_MAIN", "/base/main.py")
    monkeypatch.setattr(R._b35, "build_r35",
                        lambda adopt, base, out: {
                            "ok": True, "adopted": {}, "main_sha256": "x",
                            "main_bytes": 1, "tar_sha256": "y", "tar_bytes": 2,
                            "diff_attribution": {}})
    monkeypatch.setattr(R._g35, "verify_r35_gates",
                        lambda pkg: {"overall": False,
                                     "gates_passed": {"launch": False}})
    rc = R.main(["--skip-phase-v", str(pv_path)], out_dir=str(tmp_path))
    assert rc == 1
    out = capsys.readouterr().out
    assert '"launch_ready": false' in out
