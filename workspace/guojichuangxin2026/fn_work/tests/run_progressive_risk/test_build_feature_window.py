"""build_feature_window 单测。"""
from __future__ import annotations


def _f(t):
    return {"t": t, "battery_remaining": 80, "voltage": 14.8, "rssi": -50, "hdop": 0.8,
            "sat_count": 12, "roll": 0.02, "pitch": 0.01, "rollspeed": 0.1, "yawspeed": 0.0,
            "vz": 0.0, "imu_rms": 1.0, "imu_peak": 2.0, "imu_band_energy": 0.3,
            "imu_bias_change": 0.01,
            "margins": {"energy": {"norm": 0.8}, "nav": {"norm": 0.7},
                        "link": {"norm": 0.9}, "control": {"norm": 0.8}}}


def test_window_shape_and_insufficient():
    from run_progressive_risk.build_feature_window import FEATURE_NAMES, build_feature_window
    buf = [_f(i * 0.05) for i in range(200)]
    win = build_feature_window(buf)
    assert win is not None and win.shape[1] == len(FEATURE_NAMES) == 18
    assert win.shape[0] >= 160
    assert build_feature_window(buf[:100]) is None
