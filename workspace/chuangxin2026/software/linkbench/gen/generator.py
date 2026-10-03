"""R1 顶层：generate_interference —— 场景注入段 → 射频发射 + SigMF 归档。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from linkbench.shared.scenario import InjectionSpec


@dataclass
class GenResult:
    ok: bool
    dry_run: bool
    sigmf_path: Path | None
    style_meta: dict      # {style, power_db, freq_hz, bandwidth_hz, time_window}
    errors: list[str]


def generate_interference(spec: InjectionSpec, *, dry_run: bool = False,
                          out_dir: Path | None = None,
                          backend: str = "b210") -> GenResult:
    """按注入 spec 逐样式发射并录制归档；dry_run=只产参数表不出射频。
    错误：参数越界/设备失联 → 立即停发，errors 非空，ok=False。"""
    raise NotImplementedError("unimplemented:fn:generate_interference")
