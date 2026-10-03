"""cusum_detect 单测（阶跃检出时延断言）。"""
from __future__ import annotations


def test_step_detected_within_persist():
    from run_sudden_fault.cusum_detect import cusum_detect
    rows = [{"t": i * 0.05, "att_track": 0.0 if i < 20 else 1.0} for i in range(40)]
    hit = cusum_detect(rows)
    assert hit is not None and "att_track" in hit["channels"]
    assert hit["t"] <= 20 * 0.05 + 0.25  # 阶跃后 ~persist 拍内确认


def test_quiet_stream_none():
    from run_sudden_fault.cusum_detect import cusum_detect
    rows = [{"t": i * 0.05, "att_track": 0.05 * (i % 3)} for i in range(200)]
    assert cusum_detect(rows) is None
