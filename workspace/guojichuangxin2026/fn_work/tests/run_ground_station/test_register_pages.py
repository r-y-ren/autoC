"""register_pages 单测（五路由 200+关键元素）。"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient


def _client(tmp_path):
    from run_ground_station.register_pages import register_pages
    app = FastAPI()
    register_pages(app, str(tmp_path / "runs"))
    return TestClient(app)


def test_five_pages_and_state_api(tmp_path):
    c = _client(tmp_path)
    for path, needle in (("/", "风险等级"), ("/timeline", "事件时间线"),
                         ("/waterfall", "waterfall"), ("/replay", "回放"),
                         ("/console", "演示控制台")):
        r = c.get(path)
        assert r.status_code == 200 and needle in r.text, path
    assert c.get("/api/state").json()["state"] == "S0"
    assert c.get("/api/runs").json() == {"runs": []}


def test_frames_api_404_and_paging(tmp_path):
    import json
    c = _client(tmp_path)
    assert c.get("/api/runs/x/frames").status_code in (404, 400)
    d = tmp_path / "runs" / "sc" / "x" / "frames"
    d.mkdir(parents=True)
    (d / "frames.jsonl").write_text(
        "\n".join(json.dumps({"t": i * 0.05}) for i in range(50)), encoding="utf-8")
    r = c.get("/api/runs/x/frames")
    assert len(r.json()["frames"]) == 20 and r.json()["next"] == 1
