# -*- coding: utf-8 -*-
"""R25 测试面：run_r42_iteration（预绑定分叉：判正+门绿+窗内→发射台账；
否则收档台账）。

写路径纪律（09-28 证据覆写事故教训）：测试一律经 evidence_dir 把台账写路径
钉死在 tmp——模板占位（"aa"*32/"bb"*32）不得落真实候选目录 evidence。
"""
from __future__ import annotations

import json

from orderbook_r42 import run_r42 as r42


def test_run_r42_positive_fork(monkeypatch, tmp_path):
    _b = {"main_path": str(tmp_path / "main.py"),
          "main_sha256": "aa" * 32, "tar_sha256": "bb" * 32,
          "audit": {"unattributed": []}}
    (tmp_path / "main.py").write_text("X = 1\n", encoding="utf-8")
    monkeypatch.setattr("orderbook_r42.build_r42.build_r42",
                        lambda *a, **k: _b)
    monkeypatch.setattr("orderbook_r42.judge_r25.judge_r25",
                        lambda *a, **k: {"overall": {"pass": True,
                                                     "h2h_vs_r40": 0.9}})
    monkeypatch.setattr("orderbook_r42.gates_r42.verify_r42_gates",
                        lambda *a, **k: {"overall": {"passed": True}})
    ev_dir = tmp_path / "evidence"
    out = r42.run_r42_iteration({"window_open": True,
                                 "out_dir": str(tmp_path),
                                 "evidence_dir": str(ev_dir),
                                 "judge": {}})
    assert out["verdict"]["verdict"] == "POSITIVE"
    led = json.loads((ev_dir / "launch_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["description"].startswith("public derivative")


def test_run_r42_negative_fork(monkeypatch, tmp_path):
    _b = {"main_path": str(tmp_path / "main.py"),
          "main_sha256": "aa" * 32, "tar_sha256": "bb" * 32,
          "audit": {"unattributed": []}}
    (tmp_path / "main.py").write_text("X = 1\n", encoding="utf-8")
    monkeypatch.setattr("orderbook_r42.build_r42.build_r42",
                        lambda *a, **k: _b)
    monkeypatch.setattr("orderbook_r42.judge_r25.judge_r25",
                        lambda *a, **k: {"overall": {"pass": False}})
    ev_dir = tmp_path / "evidence"
    out = r42.run_r42_iteration({"window_open": True,
                                 "out_dir": str(tmp_path),
                                 "evidence_dir": str(ev_dir),
                                 "judge": {}})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["gates"] == {"skipped": True, "overall": False}
    led = json.loads((ev_dir / "archive_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["verdict"] == "NEGATIVE"
    # 写面钉死：run_summary 也只落调用方 evidence_dir（真实目录零污染）
    assert (ev_dir / "run_summary.json").is_file()
