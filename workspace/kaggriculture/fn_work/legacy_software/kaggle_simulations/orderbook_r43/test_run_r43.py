# -*- coding: utf-8 -*-
"""R26 测试面：run_r43_iteration（预绑定分叉）。"""
from __future__ import annotations

import json

from orderbook_r43 import run_r43 as r43


def _mk_build():
    return {"main_path": "/tmp/x/main.py", "main_sha256": "aa" * 32,
            "tar_sha256": "bb" * 32, "placebo": False}


def test_run_r43_negative_fork(monkeypatch, tmp_path):
    monkeypatch.setattr("orderbook_r43.build_r43.build_r43",
                        lambda *a, **k: _mk_build())
    monkeypatch.setattr(
        "orderbook_r43.judge_r26.judge_r26",
        lambda *a, **k: {"pass": False, "arms": {}, "criteria": {}})
    out = r43.run_r43_iteration({"out_dir": str(tmp_path)})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["gates"] == {"skipped": True, "overall": False}


def test_run_r43_positive_fork(monkeypatch, tmp_path):
    monkeypatch.setattr("orderbook_r43.build_r43.build_r43",
                        lambda *a, **k: _mk_build())
    monkeypatch.setattr(
        "orderbook_r43.judge_r26.judge_r26",
        lambda *a, **k: {"pass": True, "arms": {}, "criteria": {}})
    monkeypatch.setattr("orderbook_r43.gates_r43.verify_r43_gates",
                        lambda *a, **k: {"overall": {"passed": True}})
    out = r43.run_r43_iteration({"out_dir": str(tmp_path)})
    assert out["verdict"]["verdict"] == "POSITIVE"
    led = json.loads((r43.MODULE_DIR / "evidence" /
                      "launch_ledger.json").read_text(encoding="utf-8"))
    assert led["entry"]["description"].startswith("public derivative")
