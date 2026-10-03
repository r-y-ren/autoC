"""pipe_events 单测（本地订阅收帧+背压策略）。"""
from __future__ import annotations

import asyncio
import json


def test_event_delivery_and_spectrum_thinning():
    from run_ground_station.pipe_events import EventHub, pipe_events

    async def main():
        hub = EventHub()
        qe, qs = hub.subscribe("event"), hub.subscribe("spectrum")
        for i in range(3):
            await hub.publish("event", {"i": i})
        for i in range(200):                      # 远超队列容量→只保最新
            await hub.publish("spectrum", {"i": i})
        events = [json.loads(qe.get_nowait()) for _ in range(3)]
        assert [e["i"] for e in events] == [0, 1, 2]     # 事件全发保序
        latest = None
        while not qs.empty():
            latest = json.loads(qs.get_nowait())
        assert latest["i"] >= 190                        # 频谱帧抽稀保最新

    asyncio.run(main())


def test_pipe_events_assembly_runs():
    from run_ground_station.pipe_events import pipe_events

    async def gen():
        for i in range(2):
            yield {"i": i}

    async def main():
        hub, run_all = pipe_events({"event": gen()}, None)
        q = hub.subscribe("event")
        task = asyncio.ensure_future(run_all())
        await asyncio.wait_for(task, 2)
        got = [json.loads(q.get_nowait())["i"] for _ in range(2)]
        assert got == [0, 1]

    asyncio.run(main())
