"""run_spectrum_monitor 主循环单测（总线缺席→回放自动顶替）。"""
from __future__ import annotations

from pathlib import Path

import numpy as np


def _fx(tmp):
    f = tmp / "fx.npz"
    rng = np.random.default_rng(5)
    fft, n = 256, 40
    freqs = np.linspace(2.43e9, 2.45e9, fft)
    fr = -95 + rng.normal(0, 1.5, (n, fft))
    sel = (freqs > 2.433e9) & (freqs < 2.447e9)
    for i in range(n):
        if i >= n // 3:
            fr[i, sel] += 12
    np.savez(f, freqs_hz=freqs, frames_dbm=fr)
    return str(f)


def test_absent_device_falls_back_to_replay(tmp_path):
    from run_device_bus.run_device_bus import run_device_bus
    from run_spectrum_monitor.run_spectrum_monitor import run_spectrum_monitor
    cfg = {"spectrum": {"fft": 256, "channels": [{"name": "ch6", "lo": 2.426e9, "hi": 2.448e9}],
                        "alert_db": 6.0},
           "devices": {"replay": {"spectrum": _fx(tmp_path)}}}
    bus = run_device_bus([{"name": "sdr", "type": "usrp"}])
    got = list(run_spectrum_monitor(cfg, bus, max_frames=30))
    bus.close()
    assert all(g["source"] == "replay" for g in got)       # 缺席自动回放
    lifts = [v["lift_db"] for g in got for v in g["occupancy"].values()]
    assert max(lifts) - min(lifts) > 3                      # 拥塞段可辨
