"""compute_occupancy 单测（双源同一管线）。"""
from __future__ import annotations

import numpy as np


def _frame(busy, freqs):
    p = -95 + np.random.default_rng(3).normal(0, 1, len(freqs))
    if busy:
        sel = (freqs > 2.433e9) & (freqs < 2.447e9)
        p = p.copy(); p[sel] += 12
    return {"freqs_hz": freqs, "power_dbm": p, "source": "replay"}


def test_idle_vs_busy_separable_and_source_agnostic():
    from run_spectrum_monitor.compute_occupancy import compute_occupancy
    freqs = np.linspace(2.43e9, 2.45e9, 256)
    ch = [{"name": "ch6", "lo": 2.426e9, "hi": 2.448e9}]
    base = {"power_dbm": _frame(False, freqs)["power_dbm"], "alert_db": 6.0}
    idle = compute_occupancy(_frame(False, freqs), ch, base)
    busy = compute_occupancy(_frame(True, freqs), ch, base)
    assert idle["ch6"]["lift_db"] < 1 and busy["ch6"]["lift_db"] > 6
    assert busy["ch6"]["alert"] and not idle["ch6"]["alert"]
    # 来源无关：device 帧同一管线同结果
    fr2 = _frame(True, freqs); fr2["source"] = "device"
    assert compute_occupancy(fr2, ch, base)["ch6"]["lift_db"] == busy["ch6"]["lift_db"]
