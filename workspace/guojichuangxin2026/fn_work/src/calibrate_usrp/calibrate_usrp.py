"""B210 标定流水（device 阶梯/回放参考表）（calibrate_usrp 块）。"""
from __future__ import annotations


class CalibError(Exception):
    """device 模式无 uhd/设备。"""


def calibrate_usrp(mode: str = "dryrun", config: dict | None = None):
    """dryrun：回放谱估底噪/参考增益表（标 replay）；device：增益阶梯实采（manual 前置）。

    标定表落 fn_docs/results/calibration/usrp_calib.json（capture_spectrum 的 cal 消费）。
    """
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    out_dir = root / "fn_docs" / "results" / "calibration"
    out_dir.mkdir(parents=True, exist_ok=True)

    if mode == "device":
        try:
            import uhd  # noqa: F401
        except ImportError as exc:
            raise CalibError(f"环境缺 uhd（设备到位后安装）: {exc}") from exc
        return {"mode": "device", "note": "实采阶梯属 manual 项（R14）——设备接入后执行"}

    import numpy as np
    fx = root / "fixtures" / "spectrum_replay.npz"
    if not fx.exists():
        sys_path_hack = root / "src"
        import sys
        sys.path.insert(0, str(sys_path_hack))
        from run_spectrum_monitor.sdr_check import _make_fixture
        _make_fixture(fx)
    z = np.load(fx)
    freqs, frames = z["freqs_hz"], z["frames_dbm"]
    idle = frames[: max(2, len(frames) // 3)]
    floor_db = float(np.percentile(idle, 50))
    noise_spread = float(np.std(idle))
    table = {"mode": "replay", "floor_db": round(floor_db, 1),
             "noise_spread_db": round(noise_spread, 2),
             "gain_db": 30.0, "cal_db": round(-floor_db - 30.0, 1),
             "freq_span": [float(freqs[0]), float(freqs[-1])],
             "note": "replay 参考表；device 实测待设备（manual）"}
    (out_dir / "usrp_calib.json").write_text(
        json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"table": str(out_dir / "usrp_calib.json"), **table}
