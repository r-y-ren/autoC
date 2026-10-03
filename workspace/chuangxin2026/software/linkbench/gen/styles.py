"""六类干扰样式波形构建（复基带 IQ）。分类学锚点：IEEE COMST 2022 综述（见 docs 补充 §4.2）。"""

from __future__ import annotations

from collections.abc import Callable
import numpy as np

# 样式注册表：样式名 → 构建函数（gen/runner/ui 共用的唯一枚举来源）
STYLE_REGISTRY: dict[str, Callable[..., np.ndarray]] = {}


def build_cw(freq_hz: float, duration_s: float, sample_rate_sps: float) -> np.ndarray:
    """单音（CW）：单载波连续波。"""
    raise NotImplementedError("unimplemented:fn:build_cw")


def build_sweep(freq_hz: float, sweep_rate_hz_per_s: float, duration_s: float,
                sample_rate_sps: float) -> np.ndarray:
    """扫频：中心频率附近按速率来回扫。"""
    raise NotImplementedError("unimplemented:fn:build_sweep")


def build_chirp(freq_hz: float, bandwidth_hz: float, period_s: float, duration_s: float,
                sample_rate_sps: float) -> np.ndarray:
    """线性调频（chirp 锯齿）：市售非法干扰器的主流样式（GNSS 前车之鉴，DWP0013）。"""
    raise NotImplementedError("unimplemented:fn:build_chirp")


def build_bandlimited_noise(freq_hz: float, bandwidth_hz: float, duration_s: float,
                            sample_rate_sps: float, flatness_target_db: float = 4.0) -> np.ndarray:
    """带限噪声：EN 300 328 B.7 口径（99% 功率带宽=OCBW 的 120–200%、平坦度≤4dB）。"""
    raise NotImplementedError("unimplemented:fn:build_bandlimited_noise")


def build_partial_band(freq_hz: float, bandwidth_hz: float, frac: float, duration_s: float,
                       sample_rate_sps: float) -> np.ndarray:
    """部分频带：只占目标带宽的一段（SJR -19dB 即可失效的高效样式，COMST 锚点）。"""
    raise NotImplementedError("unimplemented:fn:build_partial_band")


def build_pulse(freq_hz: float, duty: float, duration_s: float,
                sample_rate_sps: float) -> np.ndarray:
    """脉冲：周期通断，危害随占空比上升。"""
    raise NotImplementedError("unimplemented:fn:build_pulse")
