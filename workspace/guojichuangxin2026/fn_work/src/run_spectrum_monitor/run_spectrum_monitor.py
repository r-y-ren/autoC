"""频谱站主循环：经设备总线选源（设备/回放）→占用率+瀑布帧流（run_spectrum_monitor 块）。"""
from __future__ import annotations

from run_spectrum_monitor.compute_occupancy import compute_occupancy
from run_spectrum_monitor.replay_spectrum_source import ReplayError, replay_spectrum_source


def run_spectrum_monitor(config: dict, device_bus, max_frames: int | None = None):
    """经总线 source_mode 选源：device→capture_spectrum，replay→replay_spectrum_source；

    帧经 bus.publish 路由（瀑布页），占用率逐帧产出；两源同一 compute_occupancy 管线。
    max_frames：评估/自检用限长；None=随迭代器耗尽。
    """
    import numpy as np
    spec_cfg = config.get("spectrum", {})
    replay_cfg = (config.get("devices", {}).get("replay") or {}).get("spectrum", "")
    baseline = {"alert_db": spec_cfg.get("alert_db", 6.0)}
    chan = spec_cfg.get("channels", [])
    mode = (device_bus.source_mode.get("sdr", "replay")
            if device_bus is not None else "replay")
    params = {"fft": spec_cfg.get("fft", 1024),
              "freqs_hz": None, "frame_idx": 0}
    if mode == "device" and device_bus.registry.get("sdr", {}).get("module"):
        from run_spectrum_monitor.capture_spectrum import USRPError, capture_spectrum, make_usrp_stream
        try:
            stream = make_usrp_stream(device_bus.registry["sdr"]["module"],
                                      {**spec_cfg})
            frames = capture_spectrum(stream, {**params, "freqs_hz": _freq_axis(spec_cfg)})
        except USRPError:
            mode = "replay"
    if mode == "replay":
        frames = replay_spectrum_source(replay_cfg)
    n = 0
    base_line = None
    for fr in frames:
        if base_line is None:
            baseline["power_dbm"] = fr["power_dbm"]      # 首帧为参考基线
            base_line = True
        occ = compute_occupancy(fr, chan, baseline)
        if device_bus is not None:
            device_bus.publish(fr)
        yield {"t_frame": n, "source": fr["source"], "occupancy": occ}
        n += 1
        if max_frames is not None and n >= max_frames:
            return


def _freq_axis(spec_cfg):
    import numpy as np
    rate, fc = float(spec_cfg.get("rate_hz", 20e6)), float(spec_cfg.get("center_hz", 2.44e9))
    return np.linspace(fc - rate / 2, fc + rate / 2, int(spec_cfg.get("fft", 1024)))
