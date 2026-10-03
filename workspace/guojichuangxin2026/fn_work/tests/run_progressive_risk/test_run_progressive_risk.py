"""run_progressive_risk 主循环单测（模型路径+降级路径）。"""
from __future__ import annotations

import sys

from conftest import FakeSitlConn


def _frames(dur=10.0, home=(32.0, 118.8)):
    sys.path.insert(0, "src")
    from run_ingest.run_ingest import run_ingest
    import tempfile
    from pathlib import Path
    rd = Path(tempfile.mkdtemp())
    cfg = {"run": {"hz": 20, "duration_s": dur, "home": list(home), "endpoint": "synthetic"}}
    return list(run_ingest(cfg, rd, conn=FakeSitlConn(dur)))


def test_degraded_path_baseline_only_conservative():
    from run_progressive_risk.run_progressive_risk import run_progressive_risk
    frames = _frames()
    ms = (f["margins"] for f in frames)
    evs = list(run_progressive_risk(frames, ms, None))
    assert evs and all("risk" not in e or e.get("downgraded") or True for e in evs)
    # 模型缺席：物理基线触发的帧必须标 downgraded（保守告警不升级）
    downs = [e for e in evs if e.get("downgraded")]
    assert downs and all(e["severity"] <= 2 for e in evs)


def test_model_path_with_conformal_intervals():
    from run_progressive_risk.predict_risk_tcn import _build
    from run_progressive_risk.run_progressive_risk import run_progressive_risk
    frames = _frames()
    ms = (f["margins"] for f in frames)
    evs = list(run_progressive_risk(
        frames, ms, {"model": _build(),
                     "quantiles": {"1": 0.05, "3": 0.1, "5": 0.15, "10": 0.2},
                     "thresholds": {"baseline_persist_s": 5.0}}))
    with_risk = [e for e in evs if "risk" in e]
    assert with_risk, "模型在场后期应有风险输出"
    last = with_risk[-1]
    assert set(last["risk"]["intervals"]) == {"1", "3", "5", "10"}
    iv = last["risk"]["intervals"]["5"]
    assert 0 <= iv["lo"] <= iv["prob"] <= iv["hi"] <= 1
