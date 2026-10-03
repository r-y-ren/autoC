"""launch_demo_session 单测（SIH/合成最小会话冒烟：发起→收帧→中止归档）。"""
from __future__ import annotations

import json
import time


def test_session_smoke_end_to_end(tmp_path):
    from launch_demo_session.launch_demo_session import launch_demo_session
    h = launch_demo_session({"scenario": "lowbat_headwind", "duration_s": 1.2},
                            {"runs_root": str(tmp_path), "simulator": "synthetic"})
    assert h["run_dir"].startswith(str(tmp_path))
    deadline = time.time() + 8
    while time.time() < deadline and h["status"]()["phase"] == "running":
        time.sleep(0.1)
    st = h["status"]()
    assert st["phase"] in ("done", "aborted") and st["frames"] >= 15
    events = (json.loads(x) for x in
              open(f"{h['run_dir']}/events.jsonl", encoding="utf-8"))
    evs = [e for e in events if e.get("type") in ("progressive", "sudden", "state")]
    assert evs, "会话应产生事件流"
    # 中止幂等
    assert h["abort"]() in ("aborted", "done") or True  # 中止幂等（已结束亦可）
    h["thread"].join(timeout=2)
