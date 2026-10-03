"""estimate_distance_trend 单测。"""
from __future__ import annotations

import math


def _rssi(dist, a=-40.0, n=2.5):
    return a - 10 * n * math.log10(max(dist, 1.0) / 10.0)


def test_away_flight_positive_log_rate():
    from run_link_consistency.estimate_distance_trend import estimate_distance_trend
    buf = [(i * 0.2, _rssi(10 + 5 * i * 0.2)) for i in range(40)]  # 5 m/s 远离
    est = estimate_distance_trend(buf)
    assert est is not None and est["confidence"] > 0.9
    # 平均对数距离率 ≈ ln(d_end/d_start)/T = ln(5)/7.8 ≈ 0.206/s
    assert 0.1 < est["rate_rel_per_s"] < 0.35
    assert est["rssi_pred_end"] < est["rssi_start"]


def test_insufficient_or_noisy_returns_none():
    from run_link_consistency.estimate_distance_trend import estimate_distance_trend
    assert estimate_distance_trend([(0, -50), (0.1, -51)]) is None
    import random
    rnd = random.Random(7)
    assert estimate_distance_trend(
        [(i * 0.2, -50 + rnd.uniform(-15, 15)) for i in range(40)]) is None
