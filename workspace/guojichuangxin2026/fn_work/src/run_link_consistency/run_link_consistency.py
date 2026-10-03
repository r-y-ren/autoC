"""链路一致性主循环：趋势估计→互检残差→证据双送（run_link_consistency 块）。"""
from __future__ import annotations

import math

from run_link_consistency.consistency_residual import consistency_residual
from run_link_consistency.estimate_distance_trend import estimate_distance_trend

_WARMUP_S = 4.0


def _dist_from_ref(lat, lon, ref):
    if None in (lat, lon, *ref):
        return None
    return math.hypot((lat - ref[0]) * 111320 * math.cos(math.radians(lat)),
                      (lon - ref[1]) * 111320)


def run_link_consistency(frames):
    """帧流生成器→一致性证据流；证据供 build_residuals 链路通道与链路健康度消费。

    供下游（R3 残差/状态机）消费，亦供 run_eval 采集误报：正常段 anomaly=False。
    """
    rssi_buf, dist_buf, calib, ref = [], [], [], None
    for f in frames:
        t = f.get("t", 0.0)
        if f.get("lat") is not None and ref is None:
            ref = (f["lat"], f.get("lon"))
        rssi_buf = [p for p in rssi_buf if t - p[0] <= 6.0]
        # 成熟度：起飞近距（<0.5s，约 2.5m 内）RSSI 饱和不可信，不进拟合窗
        if f.get("rssi") is not None and t >= 0.5:
            rssi_buf.append((t, f["rssi"]))
        d = _dist_from_ref(f.get("lat"), f.get("lon"), ref) if ref else None
        dist_buf = [p for p in dist_buf if t - p[0] <= 8.0]
        if d is not None:
            dist_buf.append((t, d))
        est = estimate_distance_trend(rssi_buf[-120:])
        ev = {"t": t, "anomaly": False, "residual_db": math.nan, "rssi_trend": est}
        if est is not None and len(dist_buf) >= 5 and t <= _WARMUP_S + dist_buf[0][0]:
            # 暖机段只积累正常残差校准样本
            probe = dict(est); probe["calib_residuals"] = []
            r = consistency_residual(probe, dist_buf)
            if r["residual_db"] == r["residual_db"]:
                calib.append(r["residual_db"])
            ev["residual_db"] = r["residual_db"]
        elif est is not None and len(dist_buf) >= 5:
            est2 = dict(est); est2["calib_residuals"] = calib
            ev.update(consistency_residual(est2, dist_buf))
        yield ev
