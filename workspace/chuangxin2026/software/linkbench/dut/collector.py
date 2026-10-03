"""R3 顶层：watch_links —— 监看被测链路（无干扰空跑核验用）。"""

from __future__ import annotations

from linkbench.dut.serial_link import DutSample


def watch_links(duration_s: float, on_sample=None) -> list[DutSample]:
    """监看全部已接链路 duration_s 秒；on_sample(sample) 回调逐条触发；
    串口断连 → 记 gap 事件不中断。返回样本列表。"""
    raise NotImplementedError("unimplemented:fn:watch_links")
