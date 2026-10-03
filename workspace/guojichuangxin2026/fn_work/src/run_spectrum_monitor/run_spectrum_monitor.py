"""频谱站主循环：经设备总线选源（设备/回放）→占用率+瀑布帧流（run_spectrum_monitor 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def run_spectrum_monitor(config, device_bus):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:run_spectrum_monitor")
