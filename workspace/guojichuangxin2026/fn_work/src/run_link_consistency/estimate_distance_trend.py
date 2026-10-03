"""RSSI 时序→距离变化趋势估计（对数距离模型差分统计版）（run_link_consistency 块）。"""
from __future__ import annotations

import math

_MIN_N, _MIN_SPAN_S, _PATHLOSS_N = 5, 1.0, 2.5


def estimate_distance_trend(rssi_buffer, window: dict | None = None):
    """[(t, rssi)] → 拟合结果 dict；样本不足/拟合差→None。

    输出：rate_rel_per_s（平均对数距离变化率，正=远离）、confidence（R²）、
    rssi_start/rssi_pred_end（窗口起/终的拟合 RSSI）与 t_start/t_end——
    供 consistency_residual 做 dB 域互检。
    """
    import numpy as np
    pts = [(float(t), float(r)) for t, r in (rssi_buffer or []) if r is not None and r == r]
    # 近 4s 拟合窗：躲开起飞近距饱和段与陈旧样本（可由 window["fit_s"] 覆盖）
    fit_s = float((window or {}).get("fit_s", 4.0))
    if pts and (pts[-1][0] - pts[0][0]) >= fit_s:
        t_cut = pts[-1][0] - fit_s
        pts = [p for p in pts if p[0] >= t_cut]
    if len(pts) < max(_MIN_N, 8) or (pts[-1][0] - pts[0][0]) < max(_MIN_SPAN_S, 1.5):
        return None
    t, r = np.asarray(pts).T
    if float(np.ptp(t)) <= 0:
        return None
    k, b = np.polyfit(t, r, 1)
    pred = k * t + b
    ss_res = float(np.sum((r - pred) ** 2))
    ss_tot = float(np.sum((r - np.mean(r)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    if r2 < 0.3:
        return None
    return {"rate_rel_per_s": -float(k) * math.log(10) / (10.0 * _PATHLOSS_N),
            "confidence": r2,
            "t_start": float(t[0]), "t_end": float(t[-1]), "slope_dbps": float(k),
            "rssi_start": float(k * t[0] + b), "rssi_pred_end": float(k * t[-1] + b)}
