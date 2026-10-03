"""run_ground_station 单测（app 组装层，不起真端口）。"""
from __future__ import annotations


def test_assemble_app_with_control_api_mountable(tmp_path):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from run_ground_station.pipe_events import EventHub
    from run_ground_station.register_pages import register_pages

    app = FastAPI()
    register_pages(app, str(tmp_path))
    app.state.hub = EventHub()
    c = TestClient(app)
    assert c.get("/").status_code == 200
    assert isinstance(app.state.hub, EventHub)
