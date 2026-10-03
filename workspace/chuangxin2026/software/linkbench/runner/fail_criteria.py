"""失效判据：PER 持续越界 / 断连（EN 300 328 判据量级）。"""

from __future__ import annotations

from linkbench.shared.scenario import CriteriaSpec


def is_failed(kpi_window: list[dict], criteria: CriteriaSpec) -> bool:
    """最近 KPI 窗口是否满足失效判据（PER≥阈值持续 sustain_s 或断连≥disconnect_s）。"""
    raise NotImplementedError("unimplemented:fn:is_failed")


def failure_kind(kpi_window: list[dict], criteria: CriteriaSpec) -> str:
    """失效类型："per_sustained" | "disconnect" | ""（未失效）。"""
    raise NotImplementedError("unimplemented:fn:failure_kind")
