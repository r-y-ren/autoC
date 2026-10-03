"""R7 顶层：predict_styles —— 录制 → 样式预测（与真值并列打印）。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StylePrediction:
    sigmf_base: str
    predicted: str
    truth: str | None
    probabilities: dict[str, float]


def predict_styles(model_path: str, sigmf_base: str) -> list[StylePrediction]:
    """对单条录制分段预测样式；truth 取自 annotations 真值（无则 None）。"""
    raise NotImplementedError("unimplemented:fn:predict_styles")
