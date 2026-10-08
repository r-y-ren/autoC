"""R26 事件降噪：SSE 流仅 sev≥1 或 state/advice/nav。"""
from __future__ import annotations

import time

from launch_demo_session.launch_demo_session import launch_demo_session
from run_ground_station.pipe_events import EventHub


def test_stream_only_noteworthy(tmp_path):
    hub = EventHub()
    got = []
    q = hub.subscribe("event")
    h = launch_demo_session({"scenario": "lowbat_headwind", "duration_s": 3.0},
                            {"runs_root": str(tmp_path), "simulator": "synthetic",
                             "hub": hub})
    deadline = time.time() + 15
    while time.time() < deadline and h["status"]()["phase"] == "running":
        time.sleep(0.1)
    while not q.empty():
        got.append(q.get_nowait())
    import json
    msgs = [json.loads(g) for g in got]
    assert msgs, "应有推送（nav/事件）"
    for m in msgs:
        assert ("nav" in m or "state" in m or "advice" in m
                or m.get("sev", 0) >= 1), f"违规推送(降噪失效): {m}"
    assert any("nav" in m for m in msgs)          # 1Hz 航迹帧在
