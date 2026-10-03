"""replay_spectrum_source 单测。"""
from __future__ import annotations

import numpy as np
import pytest

from run_spectrum_monitor.replay_spectrum_source import ReplayError, replay_spectrum_source


def _fixture(tmp, n=8):
    f = tmp / "fx.npz"
    np.savez(f, freqs_hz=np.linspace(2.43e9, 2.45e9, 64),
             frames_dbm=-95 + np.random.default_rng(1).normal(0, 1, (n, 64)))
    return f


def test_frames_equivalent_and_loop(tmp_path):
    gen = replay_spectrum_source(str(_fixture(tmp_path)))
    f1, f2 = next(gen), next(gen)
    assert f1["source"] == "replay" and f1["topic"] == "spectrum"
    assert f1["power_dbm"].shape == f2["power_dbm"].shape     # 帧格式等价（与设备帧同构）


def test_missing_and_bad_format(tmp_path):
    with pytest.raises(ReplayError):
        next(replay_spectrum_source(str(tmp_path / "nope.npz")))
    bad = tmp_path / "bad.npz"
    bad.write_text("junk", encoding="utf-8")
    with pytest.raises(ReplayError):
        next(replay_spectrum_source(str(bad)))
