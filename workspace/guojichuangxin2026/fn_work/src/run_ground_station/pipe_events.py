"""实时流分发：订阅各发布端→WebSocket 广播（背压策略）（run_ground_station 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def pipe_events(publishers, websocket_mgr):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:pipe_events")
