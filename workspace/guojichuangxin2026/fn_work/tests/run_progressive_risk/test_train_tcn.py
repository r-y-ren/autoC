"""train_tcn 单测（微型数据冒烟）。"""
from __future__ import annotations

import pytest

from conftest import FakeSitlConn


def _make_run(tmp, root, name, dur=10.0):
    import sys
    sys.path.insert(0, "src")
    from run_ingest.run_ingest import run_ingest
    from shared.open_run_dir import open_run_dir
    rd = open_run_dir(str(root), name, seed=1)
    cfg = {"run": {"hz": 20, "duration_s": dur, "home": [32.0, 118.8], "endpoint": "synthetic"}}
    list(run_ingest(cfg, rd, conn=FakeSitlConn(dur)))
    return rd


def test_train_smoke_and_roundtrip(tmp_path):
    from run_progressive_risk.build_feature_window import FEATURE_NAMES
    from run_progressive_risk.train_tcn import TrainError, make_dataset, train_tcn
    from shared.load_model_artifact import load_model_artifact
    dirs = [str(_make_run(tmp_path, tmp_path, f"run{i}")) for i in range(3)]
    samples = make_dataset(dirs, {"min_frames": 60})
    assert samples and all(s[1] in (0.0, 1.0) for s in samples)
    gids = {s[2] for s in samples}
    assert len(gids) == 3                                   # 架次分组保留
    out = train_tcn(dirs, {"epochs": 2, "out_dir": str(tmp_path / "ckpt"),
                           "min_frames": 60})
    assert out["params"] < 2_000_000 and len(out["history"]) == 2
    blob = load_model_artifact(out["checkpoint"], FEATURE_NAMES)   # 工件回读
    assert blob["kind"] == "tcn"
    with pytest.raises(TrainError):
        train_tcn([str(tmp_path / "empty")], {})           # 数据不足


def test_labels_need_danger_crossing(tmp_path):
    from run_progressive_risk.train_tcn import make_dataset
    short = str(_make_run(tmp_path, tmp_path, "short", dur=1.0))    # 电量不穿 25
    import pytest
    with pytest.raises(Exception):
        make_dataset([short], {"min_frames": 20})


def test_r17_probe_selection_recorded(tmp_path):
    """R17：训练报告含探针/TCN 选型对比（实证路线并跑）。"""
    from run_progressive_risk.train_tcn import train_tcn
    dirs = [str(_make_run(tmp_path, tmp_path, f"p{i}")) for i in range(3)]
    out = train_tcn(dirs, {"epochs": 1, "out_dir": str(tmp_path / "ckpt2"),
                           "min_frames": 60})
    sel = out["selection"]
    assert "winner" in sel and sel["winner"] in ("tcn", "probe")
    assert "best" in out and out["best"]["kind"] in ("tcn", "probe")
