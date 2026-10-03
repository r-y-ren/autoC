"""SigMF 读写封装：平台所有射频录制/回放的唯一出入口（SigMF v1.2.0）。"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def write_sigmf(base_path: str | Path, iq: np.ndarray, annotations: list[dict]) -> Path:
    """写一对 sigmf-data/sigmf-meta；annotations=真值标注（样式/功率档/时间窗）。"""
    raise NotImplementedError("unimplemented:fn:write_sigmf")


def read_sigmf(base_path: str | Path) -> tuple[np.ndarray, dict]:
    """读录制 → (complex64 IQ, meta dict)；文件缺失/校验不过抛 ValueError。"""
    raise NotImplementedError("unimplemented:fn:read_sigmf")
