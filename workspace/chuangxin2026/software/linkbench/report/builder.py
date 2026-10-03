"""R8 顶层：build_report —— run 目录 → report.md（数字全部本 run 实测可溯源）。"""

from __future__ import annotations

from pathlib import Path


def build_report(run_dir: str | Path) -> Path:
    """汇总场景/标定表/三元曲线/失效电平表/识别样例 + 固定仪器局限声明，产 report.md。"""
    raise NotImplementedError("unimplemented:fn:build_report")
