"""合成 DUT：无硬件时的假链路数据源（headless 冒烟/UI 演示模式共用）。"""

from __future__ import annotations

from collections.abc import Iterator

from linkbench.dut.serial_link import DutSample


def fake_stream(link: str, duration_s: float, *, jam_profile: list[tuple[float, float]] | None = None,
                seed: int = 0) -> Iterator[DutSample]:
    """按 jam_profile=[(时刻s, PER), ...] 生成合成样本流（演示模式动画数据同源）。"""
    raise NotImplementedError("unimplemented:fn:fake_stream")
