"""R4 顶层：record_run —— 三路数据（DUT-KPI ∥ 监测谱 ∥ 注入事件）统一采集落盘。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from linkbench.shared.scenario import ScenarioSpec


@dataclass
class RecordResult:
    run_dir: Path
    kpi_csv: Path
    events_jsonl: Path
    monitor_csv: Path | None
    coverage_ratio: float      # 三路时间轴覆盖率（验收 ≥0.99）


def record_run(scenario: ScenarioSpec, duration_s: float, run_dir: Path,
               *, with_injection=False) -> RecordResult:
    """统一采集：全部样本打 linkbench.shared.clock.now_ms 时间戳；
    异常 → 先经 EstopManager 停 TX 再抛出。"""
    raise NotImplementedError("unimplemented:fn:record_run")
