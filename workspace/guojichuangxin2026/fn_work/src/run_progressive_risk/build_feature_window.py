"""最近 10s 帧+余量→定长特征张量（窗口不满返回 None）（run_progressive_risk 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def build_feature_window(buffer, window: dict):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:build_feature_window")
