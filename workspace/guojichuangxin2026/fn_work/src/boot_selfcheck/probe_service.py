"""平台服务 GET 探活（可达性+延迟）（boot_selfcheck 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def probe_service(base_url: str, timeout_s: float = 2.0, retries: int = 3):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:probe_service")
