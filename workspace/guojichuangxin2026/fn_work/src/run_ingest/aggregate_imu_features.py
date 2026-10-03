"""短窗口高频 IMU→RMS/峰值/频带能量/偏置变化（run_ingest 块）。"""
from __future__ import annotations

import math

import numpy as np

_MIN_N = 16
_BAND_HZ = (5.0, 50.0)


def aggregate_imu_features(samples: list, window: dict | None = None) -> dict:
    """samples: [(t, gx,gy,gz, ax,ay,az)]；不足 _MIN_N → 四键全 NaN。"""
    if not samples or len(samples) < _MIN_N:
        return {k: math.nan for k in ("imu_rms", "imu_peak", "imu_band_energy", "imu_bias_change")}
    arr = np.asarray(samples, dtype=float)
    t, gyro, acc = arr[:, 0], arr[:, 1:4], arr[:, 4:7]
    gm, am = np.linalg.norm(gyro, axis=1), np.linalg.norm(acc, axis=1)
    rms = float(np.sqrt(np.mean(np.concatenate([gm, am]) ** 2)))
    peak = float(np.max(np.concatenate([gm, am])))
    # 频带能量：加计幅值序列一阶差分去趋势后 rfft，取 5–50Hz 占比
    _med = float(np.median(np.diff(t))) if len(t) > 1 else 0.0
    fs = 1.0 / _med if _med > 0 else 0.0
    band = math.nan
    if fs > 2 * _BAND_HZ[0] and np.ptp(t) > 0:
        spec = np.abs(np.fft.rfft(am - np.mean(am))) ** 2
        freqs = np.fft.rfftfreq(len(am), d=1.0 / fs)
        sel = (freqs >= _BAND_HZ[0]) & (freqs <= _BAND_HZ[1])
        band = float(spec[sel].sum() / (spec.sum() + 1e-12))
    half = len(gyro) // 2
    bias = float(np.linalg.norm(np.mean(gyro[:half], axis=0) - np.mean(gyro[half:], axis=0)))
    return {"imu_rms": rms, "imu_peak": peak, "imu_band_energy": band, "imu_bias_change": bias}
