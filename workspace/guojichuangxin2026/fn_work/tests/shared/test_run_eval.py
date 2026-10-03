"""run_eval 单测（回放/合成模式跑通最小次数；R2/R3/R4 验收命令本体）。"""
from __future__ import annotations

import json


def test_motor_fail_two_runs_metrics(tmp_path):
    from shared.run_eval import run_eval
    summary = run_eval("motor_fail", runs=2,
                       config={"runs_root": str(tmp_path)})
    assert summary["scenario"] == "motor_fail" and summary["runs"] == 2
    s = summary["summary"]
    assert s.get("frames", 0) >= 100                     # 12s×20Hz
    assert s.get("type_total", 0) >= 1                   # 突发事件已检出
    assert s.get("confirm_p90_s") is None or s["confirm_p90_s"] <= 1.5
    dirs = sorted((tmp_path / "motor_fail_eval").iterdir())
    frag = json.loads((dirs[0] / "metrics.jsonl").read_text().splitlines()[0])
    assert frag["key"].startswith("motor_fail/")


def test_lowbat_lead_metrics_and_bad_scenario(tmp_path):
    from shared.run_eval import run_eval
    summary = run_eval("lowbat_headwind", runs=1,
                       config={"runs_root": str(tmp_path)})
    s = summary["summary"]
    assert "lead_p10_s" in s or s.get("t_crit") is None  # 指标产出（或如实无判据）
    import pytest
    with pytest.raises(SystemExit):
        run_eval("nope", runs=1, config={"runs_root": str(tmp_path)})
