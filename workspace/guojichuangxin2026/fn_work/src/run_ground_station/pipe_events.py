"""实时流分发：订阅各发布端→WebSocket 广播（背压策略）（run_ground_station 块）。"""
from __future__ import annotations

import asyncio
import json


class EventHub:
    """进程内发布/订阅枢纽：事件全发、频谱帧可抽稀（每订阅者仅保最新）。"""

    def __init__(self):
        self._subs: dict[str, list[asyncio.Queue]] = {}
        self._latest_spectrum: dict[int, dict] = {}

    def subscribe(self, topic: str) -> asyncio.Queue:
        q = asyncio.Queue(maxsize=64)
        self._subs.setdefault(topic, []).append(q)
        return q

    def unsubscribe(self, topic: str, q):
        try:
            self._subs[topic].remove(q)
        except (KeyError, ValueError):
            pass

    def publish_sync(self, topic: str, payload: dict):
        """线程侧发布：直接入队（频谱满则挤掉旧帧）——供演示会话后台线程用。"""
        item = json.dumps({"topic": topic, **payload}, ensure_ascii=False, default=str)
        for q in self._subs.get(topic, []):
            try:
                q.put_nowait(item)
                if topic == "spectrum" and q.full():
                    q.get_nowait()
            except asyncio.QueueFull:
                pass

    async def publish(self, topic: str, payload: dict):
        dead = []
        for i, q in enumerate(self._subs.get(topic, [])):
            item = json.dumps({"topic": topic, **payload}, ensure_ascii=False,
                              default=str)
            if topic == "spectrum":
                try:
                    q.put_nowait(item)          # 满→丢旧帧策略：换最新
                    if q.full():
                        q.get_nowait()
                except asyncio.QueueFull:
                    dead.append(i)
            else:
                await q.put(item)               # 事件帧保送达
        for i in reversed(dead):
            self._subs[topic].pop(i)


def pipe_events(publishers, websocket_mgr):
    """装配：publishers {topic: 异步生成器}→逐条 hub.publish；返回启动协程。"""
    hub = websocket_mgr if isinstance(websocket_mgr, EventHub) else EventHub()

    async def pump(topic, agen):
        async for payload in agen:
            await hub.publish(topic, payload)

    async def run_all():
        await asyncio.gather(*(pump(t, g) for t, g in (publishers or {}).items()))

    return hub, run_all
