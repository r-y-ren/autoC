"""最近 10s 帧+余量→定长特征张量（窗口不满返回 None）（run_progressive_risk 块）。"""
from __future__ import annotations

FEATURE_NAMES = [
    "energy_norm", "nav_norm", "link_norm", "control_norm",
    "battery_remaining", "voltage", "rssi", "hdop", "sat_count",
    "roll", "pitch", "rollspeed", "yawspeed", "vz",
    "imu_rms", "imu_peak", "imu_band_energy", "imu_bias_change",
]


def build_feature_window(buffer, window: dict | None = None):
    """buffer: 帧列表（含 margins/imu 特征）；输出 np.ndarray[T,F]（NaN 保留）。

    掩码位转 NaN 指示列：margins 各类若 NaN → NaN（模型侧再补指示位）。
    """
    import numpy as np
    span = float((window or {}).get("span_s", 10.0))
    hz = int((window or {}).get("hz", 20))
    need = int((window or {}).get("min_frames", span * hz * 0.8))
    if len(buffer) < need:
        return None
    t_end = float(buffer[-1].get("t", 0.0))
    rows = [f for f in buffer if t_end - float(f.get("t", 0.0)) <= span]
    if len(rows) < need:
        return None
    out = []
    for f in rows:
        m = f.get("margins") or {}
        out.append([
            (m.get("energy") or {}).get("norm", float("nan")),
            (m.get("nav") or {}).get("norm", float("nan")),
            (m.get("link") or {}).get("norm", float("nan")),
            (m.get("control") or {}).get("norm", float("nan")),
            f.get("battery_remaining"), f.get("voltage"), f.get("rssi"),
            f.get("hdop"), f.get("sat_count"),
            f.get("roll"), f.get("pitch"), f.get("rollspeed"),
            f.get("yawspeed"), f.get("vz"),
            f.get("imu_rms"), f.get("imu_peak"), f.get("imu_band_energy"),
            f.get("imu_bias_change"),
        ])
    return np.asarray(out, dtype=float)
