"""consistency_residual 单测（dB 域）。"""
from __future__ import annotations


def _est(rssi0, rssi1, t0=0.0, t1=8.0, calib=None):
    return {"rate_rel_per_s": 0.0, "confidence": 0.95, "t_start": t0, "t_end": t1,
            "rssi_start": rssi0, "rssi_pred_end": rssi1,
            "slope_dbps": (rssi1 - rssi0) / (t1 - t0), "calib_residuals": calib or []}


def _dists(rate=5.0, t0=0.0, t1=8.0, d0=10.0):
    n = 60
    return [(t0 + (t1 - t0) * i / n, d0 + rate * (t1 - t0) * i / n) for i in range(n + 1)]


def test_consistent_flight_small_residual():
    from run_link_consistency.consistency_residual import consistency_residual
    import math
    r0 = -40.0
    r1 = r0 - 25 * math.log10(50 / 10)   # 与 GNSS 距离变化完全一致的 RSSI 终值
    r = consistency_residual(_est(r0, r1), _dists())
    assert abs(r["residual_db"]) < 1.5 and not r["anomaly"]


def test_spoofed_flat_rssi_flags_anomaly():
    from run_link_consistency.consistency_residual import consistency_residual
    r = consistency_residual(_est(-40.0, -40.0), _dists())  # 距离×5 信号却不变
    assert r["residual_db"] > r["threshold_db"] and r["anomaly"]


def test_missing_source_nan():
    from run_link_consistency.consistency_residual import consistency_residual
    r = consistency_residual(None, _dists())
    assert r["residual_db"] != r["residual_db"] and not r["anomaly"]
