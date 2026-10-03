"""capture_spectrum 单测（合成 IQ 流，不依赖 uhd）。"""
from __future__ import annotations

import numpy as np
import pytest

from run_spectrum_monitor.capture_spectrum import USRPError, capture_spectrum


def test_fft_frame_from_synthetic_iq():
    rng = np.random.default_rng(2)
    t = np.arange(256) / 20e6
    iq = (np.exp(2j * np.pi * 2e6 * t) + 0.1 * (rng.normal(size=256) + 1j * rng.normal(size=256)))
    frames = capture_spectrum(iter([iq.astype(np.complex64)] * 3),
                              {"fft": 256, "freqs_hz": np.linspace(2.43e9, 2.45e9, 256),
                               "frame_idx": 1})
    out = [f for f in frames]
    assert len(out) == 3 and out[0]["source"] == "device"
    peak_i = int(np.argmax(out[0]["power_dbm"]))
    assert abs(peak_i - 256 // 2 - 256 // 10) <= 4      # 2MHz 偏移在 +10% 频轴处成峰


def test_none_iq_raises_usrp_error():
    with pytest.raises(USRPError):
        next(capture_spectrum(iter([None]), {}))
