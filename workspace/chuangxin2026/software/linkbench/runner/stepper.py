"""步进计划：注入 spec → 功率档序列（GB 42590 §5.11：-5dB 起、5dB 步进至失效）。"""

from __future__ import annotations

from dataclasses import dataclass

from linkbench.shared.scenario import InjectionSpec


@dataclass
class Step:
    index: int
    style: str
    power_db: float        # 相对被测链路发射功率
    duration_s: float


def build_step_plan(spec: InjectionSpec) -> list[Step]:
    """生成 步进×样式 的完整执行序列（样式外层循环、功率内层步进）。"""
    raise NotImplementedError("unimplemented:fn:build_step_plan")


def apply_step(backend, step: Step) -> None:
    """把一步下发给干扰源后端（set_style/set_power/on）；失败 → 触发急停。"""
    raise NotImplementedError("unimplemented:fn:apply_step")
