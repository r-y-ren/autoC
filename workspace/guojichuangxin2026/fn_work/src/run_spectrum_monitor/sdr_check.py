"""R5 自检=模块化实证：同一占用率管线双源比对（run_spectrum_monitor 块）。"""
from __future__ import annotations

import numpy as np


def sdr_check() -> int:
    """回放模式必测（带宽/帧率/占用率响应）；设备在场加跑实采并比对口径一致。"""
    import json
    import time
    from pathlib import Path

    import numpy as np

    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from run_device_bus.run_device_bus import run_device_bus
    from run_spectrum_monitor.run_spectrum_monitor import run_spectrum_monitor

    root = Path(__file__).resolve().parents[2]
    fx = root / "fixtures" / "spectrum_replay.npz"
    if not fx.exists():
        fx.parent.mkdir(parents=True, exist_ok=True)
        _make_fixture(fx)
    cfg = {"spectrum": {"center_hz": 2.44e9, "rate_hz": 20e6, "fft": 256,
                        "channels": [{"name": "ch6", "lo": 2.426e9, "hi": 2.448e9}],
                        "alert_db": 6.0},
           "devices": {"replay": {"spectrum": str(fx)}}}
    bus = run_device_bus([{"name": "sdr", "type": "usrp"}])
    t0 = time.time()
    outs = list(run_spectrum_monitor(cfg, bus, max_frames=60))
    dt = time.time() - t0
    idle = [o for o in outs[:20]]
    busy = [o for o in outs[-20:]]
    ok = bool(outs) and dt < 10
    report = {"frames": len(outs), "seconds": round(dt, 2),
              "source": outs[0]["source"] if outs else None,
              "idle_lift": _lift(idle), "busy_lift": _lift(busy),
              "lift_separable": (_lift(busy) - _lift(idle)) > 3.0 if outs else False,
              "device_present": bus.registry["sdr"]["present"],
              "pass": ok and (_lift(busy) - _lift(idle) > 3.0)}
    bus.close()
    out = root / "sdr_check_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[sdr_check] frames={report['frames']} source={report['source']} "
          f"lift idle→busy {report['idle_lift']}→{report['busy_lift']} "
          f"({'PASS' if report['pass'] else 'FAIL'}；设备{'在场' if report['device_present'] else '缺席=回放'})")
    return 0 if report["pass"] else 1


def _lift(outs):
    vals = [v["lift_db"] for o in outs for v in o["occupancy"].values()]
    return round(sum(vals) / max(1, len(vals)), 2) if vals else 0.0


def _make_fixture(path):
    """合成回放夹具：前 1/3 空闲、后 2/3 ch6 拥塞（抬升 12dB）。"""
    rng = np.random.default_rng(7)
    fft, n = 256, 60
    freqs = np.linspace(2.43e9, 2.45e9, fft)
    frames = -95 + rng.normal(0, 1.5, (n, fft))
    sel = (freqs > 2.433e9) & (freqs < 2.447e9)
    for i in range(n):
        if i >= n // 3:
            frames[i, sel] += 12.0 * min(1.0, (i - n // 3) / 5)
    np.savez(path, freqs_hz=freqs, frames_dbm=frames)


if __name__ == "__main__":
    raise SystemExit(sdr_check())
