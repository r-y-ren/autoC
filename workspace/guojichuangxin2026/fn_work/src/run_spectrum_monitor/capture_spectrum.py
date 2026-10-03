"""设备模式：SDR 模块 IQ 采样+FFT→功率谱帧（source=device）（run_spectrum_monitor 块）。"""
from __future__ import annotations


class USRPError(Exception):
    """设备错误（上层转回放）。"""


def capture_spectrum(device_stream, params: dict | None = None):
    """device_stream: IQ 样本生成器（yield 复数 np 数组）——与总线 SDR 模块解耦可测。

    UHD 仅在设备侧适配器导入（模块化：缺 uhd 不影响本函数单测）。
    """
    import numpy as np
    fft_n = int((params or {}).get("fft", 1024))
    gain = float((params or {}).get("gain_db", 30.0))
    cal = float((params or {}).get("cal_db", -100.0))
    while True:
        try:
            iq = next(device_stream)
        except StopIteration:
            return
        if iq is None:
            raise USRPError("设备流中断（bus 将转回放）")
        spec = np.fft.fftshift(np.fft.fft(iq, n=fft_n))
        power = 20 * np.log10(np.abs(spec) / max(fft_n, 1) + 1e-12) + gain + cal
        yield {"topic": "spectrum", "source": "device",
               "freqs_hz": (params or {}).get("freqs_hz"), "power_dbm": power,
               "frame_idx": (params or {}).get("frame_idx", 0)}


def make_usrp_stream(module, params):
    """从总线 SDR 模块句柄构造 IQ 生成器（uhd 延迟导入）。"""
    try:
        import numpy as np
        import uhd
    except ImportError as exc:
        raise USRPError(f"环境缺 uhd/numpy: {exc}") from exc
    usrp = module["handle"]
    rate = float(params.get("rate_hz", 20e6))
    fc = float(params.get("center_hz", 2.44e9))
    fft_n = int(params.get("fft", 1024))
    usrp.set_rx_rate(rate)
    usrp.set_rx_freq(uhd.types.TuneRequest(fc))
    st = uhd.types.StreamCMD("STREAM_CONTINUOUS")
    st.stream_now = True
    md = uhd.types.RXMetadata()
    buf = np.zeros((fft_n,), dtype=np.complex64)
    streamer = usrp.get_rx_streamer(uhd.usrp.StreamArgs("fc32", "sc16"))
    streamer.issue_stream_cmd(st)
    while True:
        n = streamer.recv(buf, md)
        if n == 0 or md.error_code != "ERROR_CODE_NONE":
            yield None
            continue
        yield buf.copy()
