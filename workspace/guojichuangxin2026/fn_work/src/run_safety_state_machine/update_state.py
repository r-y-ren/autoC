"""单步状态迁移判定（阈值+持续+证据完整性+迟滞）（run_safety_state_machine 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def update_state(current_state, event_window, cfg):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:update_state")
