# execute_scenario 端到端：合成链路双卡（国标失效电平 + 对照不误报）
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.execute_scenario.execute_scenario import execute_scenario  # noqa: E402

GB = """meta: {name: mini_gb, version: 1}
dut: {links: [wifi]}
injection:
  styles: [noise_bandlimited]
  freq_hz: 2422000000
  bandwidth_hz: 20000000
  params: {seed: 3}
  power_start_db: -5
  power_step_db: 5
  power_stop_db: 15
  step_duration_s: 0.3
criteria: {per_threshold: 0.5, sustain_s: 0.04, disconnect_s: 30}
safety: {max_tx_gain_db: 0}
record: {sigmf: true, ch2_monitor: true}
"""
CTRL = """meta: {name: mini_ctrl, version: 1}
dut: {links: [wifi]}
injection: null
criteria: {per_threshold: 0.5, sustain_s: 0.04, disconnect_s: 30}
safety: {max_tx_gain_db: 0}
record: {sigmf: false, ch2_monitor: false}
"""


@pytest.fixture(autouse=True)
def _fast(monkeypatch, tmp_path):
    monkeypatch.setenv("LINKBENCH_SPEED", "30")
    monkeypatch.chdir(tmp_path)  # runs/ 落临时目录


def test_gb_card_finds_fail_level(tmp_path):
    p = tmp_path / "mini.yaml"; p.write_text(GB, encoding="utf-8")
    res = execute_scenario(p)
    fl = res["fail_levels"]
    assert "noise_bandlimited" in fl and fl["noise_bandlimited"] <= 15
    assert res["nojam_false_alarm"] is False
    assert (res["run_dir"] / "report.md").exists()
    steps = [json.loads(ln) for ln in
             (res["run_dir"] / "steps.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(s["failed"] for s in steps)


def test_control_card_no_false_alarm(tmp_path):
    p = tmp_path / "ctrl.yaml"; p.write_text(CTRL, encoding="utf-8")
    res = execute_scenario(p)
    assert res["nojam_false_alarm"] is False
    assert res["fail_levels"] == {}
