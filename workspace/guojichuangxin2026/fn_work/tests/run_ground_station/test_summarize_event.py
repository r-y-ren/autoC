"""R21 证据链摘要模板单测。"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from run_ground_station.register_pages import register_pages


def test_events_api_carries_summary(tmp_path):
    import json
    d = tmp_path / "runs" / "sc" / "r1" / "frames"
    d.mkdir(parents=True)
    (d / "frames.jsonl").write_text(json.dumps({"t": 0.0}) + "\n", encoding="utf-8")
    evs = [
        {"type": "state", "state": "S2", "advice": {"action": "返航"}},
        {"type": "sudden", "fault": "电机异常", "channels": ["att_track"], "latency_s": 0.5},
        {"type": "progressive", "risk": {"intervals": {"5": {"prob": 0.42, "lo": 0.3, "hi": 0.55}}},
         "baseline": {"energy": True}},
    ]
    (d.parent / "events.jsonl").write_text(
        "\n".join(json.dumps(e) for e in evs), encoding="utf-8")
    app = FastAPI()
    register_pages(app, str(tmp_path / "runs"))
    c = TestClient(app)
    r = c.get("/api/runs/r1/frames").json()
    assert len(r["events"]) == 3
    assert "状态转为 S2" in r["events"][0]["summary"]
    assert "电机异常" in r["events"][1]["summary"] and "证据" in r["events"][1]["summary"]
    assert "0.42" in r["events"][2]["summary"] and "共形" in r["events"][2]["summary"]
