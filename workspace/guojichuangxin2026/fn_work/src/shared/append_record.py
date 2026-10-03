"""事件/度量记录 JSON 行落盘（进程内保序，度量键带前缀）（shared 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def append_record(run_dir, kind: str, payload: dict):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:append_record")
