"""三元曲线绘制：①PER-vs-JSR ②吞吐/时延-vs-JSR ③失效事件时间线。"""

from __future__ import annotations

from pathlib import Path


def plot_triple_curves(kpi_csv: str | Path, out_dir: str | Path) -> list[Path]:
    """KPI CSV → 三张 PNG（命名 per_vs_jsr / throughput_latency / fail_timeline）。"""
    raise NotImplementedError("unimplemented:fn:plot_triple_curves")
