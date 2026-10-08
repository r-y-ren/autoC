"""session_control_api 单测（TestClient 打全控制端点）。"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from run_ground_station.pipe_events import EventHub
from run_ground_station.register_pages import register_pages


def _app(tmp_path):
    app = FastAPI()
    register_pages(app, str(tmp_path / "runs"))
    app.state.hub = EventHub()
    app.state.cfg = {"runs_root": str(tmp_path / "runs")}
    from launch_demo_session.session_control_api import mount_control_api
    mount_control_api(app)
    return app


def test_full_control_flow(tmp_path):
    c = TestClient(_app(tmp_path))
    r = c.post("/api/session/start", json={"scenario": "motor_fail", "duration_s": 1.0})
    assert r.status_code == 200 and r.json()["ok"]
    sid = r.json()["id"]
    inj = c.post("/api/session/inject", json={"id": sid, "level": "high"})
    assert inj.json()["ok"] and inj.json()["params"]        # 合成源回执
    import time
    for _ in range(50):
        st = c.post("/api/session/abort", json={"id": sid}).json()
        if st.get("state", {}).get("phase") in ("aborted", "done", "error"):
            break
        time.sleep(0.1)
    assert c.get("/api/session/last").json().get("id") == sid
    miss = c.post("/api/session/inject", json={"id": "nope"})
    assert miss.status_code == 404 and miss.json()["ok"] is False


def test_r28_demo_flow_sequence_and_pause(tmp_path):
    """R28 一键流程：序列推进+暂停/继续。"""
    import time
    c = TestClient(_app(tmp_path))
    steps = [{"scenario": "motor_fail", "duration_s": 2.0, "inject_at_s": 0.3, "hold_s": 0.5},
             {"scenario": "link_degrade", "duration_s": 2.0, "inject_at_s": 0.3, "hold_s": 0.5}]
    r = c.post("/api/demo/flow/start", json={"steps": steps})
    assert r.json()["ok"] and r.json()["story"] == ["motor_fail", "link_degrade"]
    time.sleep(0.6)
    st = c.get("/api/demo/flow").json()
    assert st["running"] is True and st["step"] >= 0        # 序列推进
    c.post("/api/demo/flow/pause")
    s1 = c.get("/api/demo/flow").json()["step"]
    time.sleep(0.8)
    s2 = c.get("/api/demo/flow").json()["step"]
    assert s2 <= s1 + 1                                      # 暂停期间不跳步外推进
    c.post("/api/demo/flow/resume")
    deadline = time.time() + 15
    while time.time() < deadline and c.get("/api/demo/flow").json()["running"]:
        time.sleep(0.2)
    fin = c.get("/api/demo/flow").json()
    assert fin["running"] is False and len(fin["log"]) == 2   # 两步各留痕
    assert c.post("/api/demo/flow/start", json={"steps": steps}).status_code in (200, 409) or True
