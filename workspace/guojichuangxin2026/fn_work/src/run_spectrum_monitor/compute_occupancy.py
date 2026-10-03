"""功率谱帧（不问来源）→信道占用率（双口径）+告警位（run_spectrum_monitor 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def compute_occupancy(frame, channel_table, baseline):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:compute_occupancy")
