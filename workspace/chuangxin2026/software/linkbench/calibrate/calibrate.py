"""R2 顶层：run_calibration —— 全频点×增益档标定，产 calibration.json + 单调性检查。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CalibrationResult:
    calibration_path: str
    monotonic_ok: bool          # 相邻档差值与设定步距偏差 ≤1dB
    max_deviation_db: float
    entries: int


def run_calibration(freq_hz_list: list[int], gain_list: list[float],
                    runs_dir: str = "runs") -> CalibrationResult:
    """逐频点逐增益档标定注入功率；结果落 calibration.json 并打印单调性检查。"""
    raise NotImplementedError("unimplemented:fn:run_calibration")
