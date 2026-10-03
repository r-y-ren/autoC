"""原始 MAVLink 消息批→StateFrame（含质量掩码，不插值）（run_ingest 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def normalize_telemetry(messages: list):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:normalize_telemetry")
