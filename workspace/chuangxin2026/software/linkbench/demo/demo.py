"""R8 顶层：demo —— 一键演示编排（UI『一键演示』卡片与此同底层）。"""

from __future__ import annotations

from pathlib import Path


def demo(*, quick: bool = True) -> Path:
    """短场景注入 + 小样本推理 + 报告生成，返回 report.md 路径；
    quick=True 用合成数据路径（无硬件可演示）。"""
    raise NotImplementedError("unimplemented:fn:demo")
