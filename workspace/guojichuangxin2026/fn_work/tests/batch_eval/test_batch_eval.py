"""batch_eval 单测（synthetic 微量 1×1 跑通+归档断言）。"""
from __future__ import annotations

import json
from pathlib import Path


def test_micro_batch_synthetic_fallback(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.chdir(root)                       # 归档根相对战役根
    from batch_eval.batch_eval import batch_eval
    out = batch_eval(["motor_fail"], runs_per_scenario=1,
                     config={"runs_root": str(tmp_path / "runs"),
                             "retrain": False})
    assert out["data_source"] == "synthetic" and out["downgrade_note"]
    assert out["runs_total"] >= 1
    snap = Path(root / "fn_docs" / "results")
    assert snap.exists() and any(snap.glob("batch-*.json"))
    arch = list((root / "fn_docs" / "results" / "motor_fail_eval").iterdir())
    assert arch and (arch[0] / "metrics.jsonl").exists()
    # 清理本测试归档（保持 results 只留正式批）
    import shutil
    shutil.rmtree(root / "fn_docs" / "results" / "motor_fail_eval")
    for f in snap.glob("batch-*.json"):
        f.unlink()
