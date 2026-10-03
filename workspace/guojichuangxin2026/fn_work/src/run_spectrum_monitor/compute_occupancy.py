"""功率谱帧（不问来源）→信道占用率（双口径）+告警位（run_spectrum_monitor 块）。"""
from __future__ import annotations


def compute_occupancy(frame, channel_table, baseline):
    """双口径：能量占比 + 过阈子载波占比；告警=相对基线抬升超 alert_db。

    帧不问来源（device|replay 同管线）——模块化等价的实现落点。
    """
    import numpy as np
    freqs, power = frame.get("freqs_hz"), frame["power_dbm"]
    if freqs is None:
        freqs = np.arange(len(power), dtype=float)
    freqs = np.asarray(freqs, dtype=float)
    power = np.asarray(power, dtype=float)
    alert_db = float(baseline.get("alert_db", 6.0))
    base = np.asarray(baseline.get("power_dbm", power), dtype=float)
    out = {}
    for ch in channel_table or []:
        sel = (freqs >= ch["lo"]) & (freqs <= ch["hi"])
        if not sel.any():
            continue
        seg, bseg = power[sel], base[sel]
        energy_ratio = float(10 ** (seg / 10).sum() / max(1e-12, 10 ** (power / 10).sum()))
        floor = float(np.percentile(bseg, 50)) + 6.0
        over_ratio = float((seg > floor).mean())
        lift = float(np.mean(seg) - np.mean(bseg))
        out[ch["name"]] = {"energy": round(energy_ratio, 4),
                           "over_threshold": round(over_ratio, 4),
                           "lift_db": round(lift, 2),
                           "alert": lift > alert_db}
    return out
