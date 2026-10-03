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
    # R12：渐进场景输出 hit_rate 字段；降级模式（无模型）基线阈低于危险线→0.0 为诚实读数
    assert "lead_hit_rate" in s and "t_crit" in s
    import pytest
    with pytest.raises(SystemExit):
        run_eval("nope", runs=1, config={"runs_root": str(tmp_path)})


def test_r12_latency_from_inject_and_no_hitrate_for_sudden(tmp_path):
    from shared.run_eval import run_eval
    s = run_eval("motor_fail", runs=1, config={"runs_root": str(tmp_path)})
    frag = tmp_path / "motor_fail_eval"
    rd = sorted(frag.iterdir())[0]
    rows = [json.loads(x) for x in (rd / "metrics.jsonl").read_text().splitlines()]
    keys = {r["key"] for r in rows}
    assert "motor_fail/lead_hit_rate" not in keys       # R12：突发不落命中率键
    assert "motor_fail/lead_p10_s" not in keys         # 及提前量族
    assert "motor_fail/inject_at_s" in keys
    p90 = [r["value"] for r in rows if r["key"] == "motor_fail/confirm_p90_s"][0]
    assert 0.1 <= p90 <= 0.6, p90                        # 确认−注入（3.0s 生效）口径
    assert any(r.get("data_source") == "synthetic" for r in rows)


def test_r11_model_channel_and_degraded_note(tmp_path):
    from shared.run_eval import run_eval
    s1 = run_eval("lowbat_headwind", runs=1,
                  config={"runs_root": str(tmp_path / "deg"), "model": None})
    rd = sorted((tmp_path / "deg" / "lowbat_headwind_eval").iterdir())[0]
    note = [json.loads(x)["note"] for x in (rd / "metrics.jsonl").read_text().splitlines()][0]
    assert "degraded" in note                             # 模型缺席→降级标注
    # 模型注入：给个微型 Net（未训练也行，验通道启用）
    import sys
    sys.path.insert(0, "src")
    from run_progressive_risk.predict_risk_tcn import _build
    net = _build(); net.eval()
    s2 = run_eval("lowbat_headwind", runs=1,
                  config={"runs_root": str(tmp_path / "mdl"), "model": net,
                          "quantiles": {"1": 0.05, "3": 0.1, "5": 0.15, "10": 0.2}})
    rd2 = sorted((tmp_path / "mdl" / "lowbat_headwind_eval").iterdir())[0]
    evs = [json.loads(x) for x in (rd2 / "events.jsonl").read_text().splitlines()]
    assert any(e.get("type") == "progressive" and "risk" in e for e in evs)  # 模型通道出共形区间
