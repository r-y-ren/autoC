"""aggregate_imu_features 单测。"""
from __future__ import annotations

import math

from conftest import make_imu


def test_full_window_features():
    from run_ingest.aggregate_imu_features import aggregate_imu_features
    samples = [make_imu(t * 0.01, i) for i, t in enumerate(range(100))]  # 100Hz×1s 含尖峰
    f = aggregate_imu_features(samples)
    assert all(f[k] == f[k] for k in f)          # 全部有限（非 NaN）
    assert f["imu_rms"] > 0 and f["imu_peak"] >= f["imu_rms"]
    assert 0.0 <= f["imu_band_energy"] <= 1.0
    assert f["imu_bias_change"] >= 0


def test_insufficient_window_nan():
    from run_ingest.aggregate_imu_features import aggregate_imu_features
    f = aggregate_imu_features([make_imu(i * 0.01, i) for i in range(5)])
    assert all(math.isnan(v) for v in f.values())
