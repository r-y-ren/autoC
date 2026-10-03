"""run_link_consistency 主循环单测。

距离口径：主循环 GNSS 参考点=首个定位点（机站同址起飞），RSSI 模型对齐该定义：
rssi = -40 - 25*lg(d/10)，d = 5t（距首 fix 米数）。
已知限界（演示级，如实记录）：对数距离模型下 dB 残差随距离收窄，远距慢欺骗弱检出。
"""
from __future__ import annotations

import math


def _rssi(d):
    return -40 - 25 * math.log10(max(d, 1.0) / 10.0)


def _frames(spoof_after=None, n=280):
    frames = []
    for i in range(n):
        t = i * 0.05
        d = 5 * t
        rssi = -45.0 if (spoof_after is not None and t > spoof_after) else _rssi(d)
        frames.append({"t": t, "lat": 32.0 + d / 111320, "lon": 118.8, "rssi": rssi})
    return frames


def test_normal_flight_no_anomaly_after_warmup():
    from run_link_consistency.run_link_consistency import run_link_consistency
    evs = list(run_link_consistency(_frames()))
    checked = [e for e in evs if e["residual_db"] == e["residual_db"] and e["t"] > 8]
    assert checked and not any(e["anomaly"] for e in checked)   # 正常段零误报


def test_spoof_triggers_within_detection_window():
    from run_link_consistency.run_link_consistency import run_link_consistency
    evs = list(run_link_consistency(_frames(spoof_after=6)))
    alarmed = [e for e in evs if e["anomaly"]]
    assert alarmed, "欺骗应触发告警"
    assert 6.0 < alarmed[0]["t"] <= 11                          # 拟合窗滑出纯净段后检出
