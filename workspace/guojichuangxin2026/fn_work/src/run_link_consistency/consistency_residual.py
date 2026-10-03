"""RSSI 拟合终值与 GNSS 距离推算期望的 dB 域互检残差（IQR 自适应阈）（run_link_consistency 块）。"""
from __future__ import annotations

import math

import numpy as np

_PATHLOSS_N = 2.5
_FLOOR_DB = 5.0


def consistency_residual(trend_estimate, gnss_distances):
    """trend_estimate: estimate_distance_trend 输出；gnss_distances: [(t, dist_m)]。

    残差(dB) = RSSI 拟合终值 − 由 GNSS 距离变化推算的期望终值
    （期望 = rssi_start + 10n·lg(d_end/d_start)）；正=信号强于预期（中继/欺骗），
    负=弱于预期（干扰/遮挡）。阈：IQR 自适应（校准样本由 trend['calib_residuals'] 注入）。
    """
    bad = {"residual_db": math.nan, "threshold_db": math.nan, "anomaly": False}
    if not trend_estimate or not gnss_distances or len(gnss_distances) < 5:
        return bad
    ds = [(float(t), float(d)) for t, d in gnss_distances]
    t0, t1 = trend_estimate["t_start"], trend_estimate["t_end"]
    d0 = min(ds, key=lambda p: abs(p[0] - t0))[1]   # 取最近样本（端点对齐，避免窗均系统差）
    d1 = min(ds, key=lambda p: abs(p[0] - t1))[1]
    if d0 <= 0 or d1 <= 0 or t1 <= t0:
        return bad
    # 斜率差法：RSSI 实测斜率 − GNSS 距离变化蕴含的期望斜率，×窗长折回 dB
    gnss_slope = -10.0 * _PATHLOSS_N * math.log10(d1 / d0) / (t1 - t0)
    residual = float((trend_estimate.get("slope_dbps", 0.0) - gnss_slope) * (t1 - t0))
    calib = trend_estimate.get("calib_residuals") or []
    if len(calib) >= 8:
        q3, q1 = np.percentile([abs(x) for x in calib], [75, 25])
        threshold = max(_FLOOR_DB, float(q3 + 1.5 * (q3 - q1)))
    else:
        threshold = _FLOOR_DB
    return {"residual_db": residual, "threshold_db": threshold,
            "anomaly": abs(residual) > threshold}
