"""SigMF 录制校验：格式合法 + 真值标注齐全。"""

from __future__ import annotations


def validate_recording(sigmf_base: str) -> list[str]:
    """校验单条录制（sigmf 库校验 + annotations 必含 style/power/时间窗），返回错误清单。"""
    raise NotImplementedError("unimplemented:fn:validate_recording")
