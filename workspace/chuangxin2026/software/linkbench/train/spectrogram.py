"""IQ → 谱图（识别模型输入；标签体系=六类+无干扰，复现 arXiv:2205.15001 口径）。"""

from __future__ import annotations

import numpy as np


def make_spectrogram(iq: np.ndarray, nfft: int = 256, hop: int | None = None) -> np.ndarray:
    """复基带 IQ → 幅度谱图矩阵 (freq × time)。"""
    raise NotImplementedError("unimplemented:fn:make_spectrogram")
