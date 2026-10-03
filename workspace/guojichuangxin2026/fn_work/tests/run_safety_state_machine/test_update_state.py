"""update_state 单测。"""
from __future__ import annotations

CFG = {"hysteresis": 0.05, "dwell_s": {"S1": 2.0, "S2": 2.0, "S3": 1.0, "S4": 0.0}}


def test_upgrade_needs_complete_evidence():
    from run_safety_state_machine.update_state import update_state
    ev = [{"type": "progressive", "severity": 3, "t": 10, "evidence": None}]
    s, rec = update_state("S0", ev, CFG)
    assert s == "S0" and rec.get("blocked")          # 证据不完整不升级


def test_sudden_direct_s4_and_pending_dwell():
    from run_safety_state_machine.update_state import update_state
    ev = [{"type": "sudden", "severity": 0, "t": 5, "fault": "电机异常"}]
    s, _ = update_state("S1", ev, CFG)               # 目标 S4，dwell=0 → 直达
    assert s == "S4"
    ev2 = [{"type": "progressive", "severity": 2, "t": 5, "evidence": {"m": 1}}]
    s2, rec2 = update_state("S0", ev2, CFG)          # 目标 S2，dwell=2 → pending
    assert s2 == "S0" and rec2.get("pending")


def test_downgrade_with_hysteresis():
    from run_safety_state_machine.update_state import update_state
    ev = [{"type": "progressive", "severity": 1, "t": 9, "evidence": {"x": 1}}]
    s, rec = update_state("S4", ev, CFG)
    assert s == "S1" and rec.get("degraded")         # 分值1−迟滞→round(0.95)=1
