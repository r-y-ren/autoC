"""build_residuals 单测。"""
from __future__ import annotations

import math


def _f(t, roll=0.02, gap=False, **kw):
    d = {"t": t, "roll": roll, "pitch": 0.01, "vx": 5.0, "vy": 0.0,
         "lat": 32.0 + 5 * t / 111320, "lon": 118.8, "telem_gaps": [gap]}
    d.update(kw)
    return d


def test_normal_small_and_nan_channels():
    from run_sudden_fault.build_residuals import build_residuals
    hist = [_f(i * 0.05) for i in range(20)]
    r = build_residuals(hist)
    assert r["att_track"] < 0.2
    assert r["motor_consistency"] != r["motor_consistency"]  # 无电机数据→NaN 掩码
    assert r["telem_loss"] == 0.0


def test_attitude_step_and_telem_loss_step():
    from run_sudden_fault.build_residuals import build_residuals
    hist = [_f(i * 0.05, roll=0.5 if i >= 18 else 0.02) for i in range(20)]
    r = build_residuals(hist)
    assert r["att_track"] > 0.5
    hist2 = [_f(i * 0.05, gap=(i >= 15)) for i in range(20)]
    r2 = build_residuals(hist2)
    assert r2["telem_loss"] > 0.5
