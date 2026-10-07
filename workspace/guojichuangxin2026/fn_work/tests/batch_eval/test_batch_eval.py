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


def test_r23_ensure_model_three_branches(tmp_path, monkeypatch):
    """R23：probe-sel/tcn-sel/回退三分支+note 内容。"""
    import json
    import pickle
    import sys
    import numpy as np
    sys.path.insert(0, "src")
    from batch_eval.batch_eval import _ensure_model
    from run_progressive_risk.train_tcn import _LinearProbe

    ck = tmp_path / "ckpt"
    ck.mkdir()
    w = np.zeros(54); b = 0.0
    probe = _LinearProbe(w, b, {"fill": [0.0] * 18}, {"1": 1.1, "3": 1.0, "5": 1.0, "10": 0.9},
                         [f"f{i}" for i in range(18)])
    with open(ck / "probe.pkl", "wb") as fh:
        pickle.dump({"probe": probe.state_dict(), "version": "v", "feature_names": probe.feature_names,
                     "kind": "probe"}, fh)
    # winner=probe
    (ck / "train_report.json").write_text(json.dumps({"best": {"path": str(ck / "probe.pkl"),
                                                               "kind": "probe"}}))
    model, q, note = _ensure_model({"ckpt_dir": str(ck)})
    assert note == "probe-sel" and isinstance(model, _LinearProbe)
    # winner=tcn 但工件缺失→回退重训（monkeypatch train_tcn 防长跑）→ note 带回退原因
    (ck / "train_report.json").write_text(json.dumps({"best": {"path": str(ck / "tcn.pt"),
                                                               "kind": "tcn"}}))
    monkeypatch.setattr("run_progressive_risk.train_tcn.train_tcn",
                        lambda d, c: {"checkpoint": str(ck / "probe.pkl"),
                                      "best": {"kind": "probe", "path": str(ck / "probe.pkl")}})
    model2, _, note2 = _ensure_model({"ckpt_dir": str(ck)})
    assert note2.startswith("retrain-") and "probe" in note2 and "broken" in note2
    # 强制重训
    monkeypatch.setattr("run_progressive_risk.train_tcn.train_tcn",
                        lambda d, c: {"checkpoint": str(ck / "probe.pkl"),
                                      "best": {"kind": "probe", "path": str(ck / "probe.pkl")}})
    _, _, note3 = _ensure_model({"ckpt_dir": str(ck), "retrain": True})
    assert "forced" in note3
