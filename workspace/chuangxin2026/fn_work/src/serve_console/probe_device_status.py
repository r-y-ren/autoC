# 设备状态探测：异构探测→同构状态清单（责任文档演进轮二：serve_console/probe_device_status）
from __future__ import annotations


def probe_device_status(timeout_s: float = 2.0) -> list:
    # 桩——签名意图详见 responsibility.md 演进轮二增量块
    # 返回 [{id, name, status: ok|missing|pending_manual|manual_ok, detail, ts}]
    raise NotImplementedError("unimplemented:fn:probe_device_status")
