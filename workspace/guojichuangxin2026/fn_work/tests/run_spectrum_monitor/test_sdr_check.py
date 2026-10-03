"""sdr_check 单测（模块化实证：回放自检全链）。"""
from __future__ import annotations

from pathlib import Path


def test_sdr_check_pass(tmp_path, monkeypatch, capsys):
    import sys
    root = Path(__file__).resolve().parents[2]
    monkeypatch.chdir(root)
    from run_spectrum_monitor.sdr_check import sdr_check
    rc = sdr_check()
    out = capsys.readouterr().out
    assert rc == 0 and "PASS" in out
    assert (root / "sdr_check_report.json").exists()
    rep = __import__("json").loads((root / "sdr_check_report.json").read_text())
    assert rep["lift_separable"] and rep["source"] == "replay"
    (root / "sdr_check_report.json").unlink()
