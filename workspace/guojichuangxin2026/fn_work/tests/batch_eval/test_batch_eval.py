"""batch_eval 单测（synthetic 微量 1×1 跑通+归档断言）。"""
from __future__ import annotations

import json
from pathlib import Path


def test_micro_batch_synthetic_fallback(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    campaign = Path(__file__).resolve().parents[3]  # 归档根=战役 fn_docs/results（本次修正后的真值）
    monkeypatch.chdir(root)                       # 归档根相对战役根
    from batch_eval.batch_eval import batch_eval
    out = batch_eval(["motor_fail"], runs_per_scenario=1,
                     config={"runs_root": str(tmp_path / "runs"),
                             "retrain": False})
    assert out["data_source"] == "synthetic" and out["downgrade_note"]
    assert out["runs_total"] >= 1
    snap = Path(campaign / "fn_docs" / "results")
    assert snap.exists() and any(snap.glob("batch-*.json"))
    arch = list((campaign / "fn_docs" / "results" / "motor_fail_eval").iterdir())
    assert arch and (arch[0] / "metrics.jsonl").exists()
    # 只清本测试的微档（按名删除，绝不整目录 rmtree——正式批归档是数据资产）
    import shutil
    for a in arch:
        shutil.rmtree(a, ignore_errors=True)
    for f in snap.glob("batch-*.json"):
        f.unlink()
