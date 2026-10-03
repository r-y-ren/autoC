"""run_sudden_fault 主循环单测。"""
from __future__ import annotations


def _frames(fault_at=3.0, kind="motor", n=300):
    frames = []
    for i in range(n):
        t = i * 0.05
        f = {"t": t, "roll": 0.02, "pitch": 0.01, "vx": 5.0, "vy": 0.0,
             "lat": 32.0 + 5 * t / 111320, "lon": 118.8, "telem_gaps": [False]}
        if kind == "motor" and t >= fault_at:
            f["roll"] = 0.35 * (1 if (i % 4 < 2) else -1)  # 振荡
        if kind == "link" and t >= fault_at:
            f["telem_gaps"] = [True]
        frames.append(f)
    return frames


def test_motor_fault_event_with_latency():
    from run_sudden_fault.run_sudden_fault import run_sudden_fault
    evs = list(run_sudden_fault(_frames(fault_at=3.0, kind="motor")))
    assert evs, "电机故障应产生事件"
    ev = evs[0]
    assert ev["fault"] in ("电机异常", "电调异常")
    assert ev["latency_s"] >= 0 and ev["t_confirm"] >= 3.0
    assert ev["latency_s"] <= 0.6  # 200ms 级确认（P90 目标口径）


def test_link_burst_and_normal_silence():
    from run_sudden_fault.run_sudden_fault import run_sudden_fault
    evs = list(run_sudden_fault(_frames(fault_at=2.0, kind="link")))
    assert evs and evs[0]["fault"] == "链路瞬断"
    quiet = list(run_sudden_fault(_frames(fault_at=99.0, kind="motor")))  # 全程正常
    assert not quiet
