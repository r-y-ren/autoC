"""compute_physical_margins 单测。"""
from __future__ import annotations

import math


def _frame(**kw):
    base = {"lat": 32.0, "lon": 118.8, "battery_remaining": 90, "gps_fix": 6,
            "sat_count": 14, "hdop": 0.8, "rssi": -50.0,
            "rollspeed": 0.05, "pitchspeed": 0.05, "yawspeed": 0.05, "imu_rms": 1.0}
    base.update(kw)
    return base


def test_energy_margin_home_vs_far_lowbattery_headwind():
    from run_ingest.compute_physical_margins import compute_physical_margins
    near = compute_physical_margins([_frame()], home_position=(32.0, 118.8), wind_ms=0)
    far = compute_physical_margins(
        [_frame(lat=32.05, battery_remaining=20)], home_position=(32.0, 118.8), wind_ms=8)
    assert near["energy"]["raw"] > 40          # 近家满电：余量充足
    assert far["energy"]["raw"] < 0            # 远+低电+逆风：返航能源不足
    assert near["energy"]["norm"] > far["energy"]["norm"]


def test_nav_link_control_and_missing():
    from run_ingest.compute_physical_margins import compute_physical_margins
    m = compute_physical_margins([_frame()], home_position=(32.0, 118.8))
    assert 0 < m["nav"]["norm"] <= 1 and 0 < m["link"]["norm"] <= 1
    assert 0 < m["control"]["norm"] <= 1
    m2 = compute_physical_margins([_frame(rssi=None)])
    assert math.isnan(m2["link"]["raw"])       # 缺源→NaN 而非造数
