"""scenario 契约：YAML 场景卡 → 强类型对象（全平台唯一输入格式）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class InjectionSpec:
    """注入参数；power_*=相对被测链路发射功率的 dB 值（GB 42590 §5.11 口径）。"""
    styles: list[str]
    freq_hz: int
    bandwidth_hz: int
    params: dict = field(default_factory=dict)
    power_start_db: float = -5.0
    power_step_db: float = 5.0
    power_stop_db: float = 40.0
    step_duration_s: float = 30.0


@dataclass
class CriteriaSpec:
    per_threshold: float = 0.10
    sustain_s: float = 10.0
    disconnect_s: float = 30.0


@dataclass
class SafetySpec:
    max_tx_gain_db: float = 0.0


@dataclass
class RecordSpec:
    sigmf: bool = True
    ch2_monitor: bool = True


@dataclass
class ScenarioSpec:
    meta: dict
    dut_links: list[str]
    injection: InjectionSpec | None
    criteria: CriteriaSpec
    safety: SafetySpec
    record: RecordSpec


def load_scenario(path: str | Path) -> ScenarioSpec:
    """读场景 YAML → ScenarioSpec；schema 不合法 → 抛 ValueError（含字段名）。"""
    raise NotImplementedError("unimplemented:fn:load_scenario")


def validate_scenario(sc: ScenarioSpec) -> list[str]:
    """语义校验（频段范围/功率上下界/样式名合法/安全顶），返回错误清单（空=通过）。"""
    raise NotImplementedError("unimplemented:fn:validate_scenario")
