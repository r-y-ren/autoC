# RuntimeFeed→WebSocket 帧流（责任文档演进轮三：serve_console/ws_stream_feed）
from __future__ import annotations


async def ws_stream_feed(ws, feed):
    # 桩——快照续推/≤10Hz 节流/idle 心跳/断连静默摘除
    raise NotImplementedError("unimplemented:fn:ws_stream_feed")
