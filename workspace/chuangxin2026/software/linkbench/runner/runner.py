"""R5 顶层：run_scenario —— GB 42590 §5.11 协议执行器（步进注入至失效，产三元曲线+报告）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class StepOutcome:
    step_index: int
    style: str
    power_db: float
    failed: bool
    failure_kind: str


@dataclass
class RunResult:
    run_dir: Path
    outcomes: list[StepOutcome] = field(default_factory=list)
    fail_levels: dict[str, float] = field(default_factory=dict)  # style → 失效电平
    nojam_false_alarm: bool = False                              # 对照场景误报=False 才算过
    report_path: Path | None = None


def run_scenario(scenario_path: str | Path) -> RunResult:
    """读场景 → 标定 → 步进执行 → 采集 → 失效判定 → 三元曲线+报告；
    任何异常先急停；支持断点续跑（run_dir 内 plan 进度）。"""
    raise NotImplementedError("unimplemented:fn:run_scenario")
