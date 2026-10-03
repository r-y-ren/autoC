"""WebSocket 推送枢纽：KPI/事件/状态实时下发到全部已连浏览器。"""

from __future__ import annotations


class WsHub:
    """订阅-广播：subscribe(ws) / broadcast(msg dict)；断连自动摘除。"""

    def __init__(self) -> None:
        self._clients: list = []

    async def subscribe(self, ws) -> None:
        raise NotImplementedError("unimplemented:fn:WsHub.subscribe")

    async def broadcast(self, msg: dict) -> None:
        raise NotImplementedError("unimplemented:fn:WsHub.broadcast")
