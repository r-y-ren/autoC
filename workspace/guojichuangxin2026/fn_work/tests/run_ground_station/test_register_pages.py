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


def test_r26_r27_command_center_and_devices(tmp_path):
    """R26 布局区元素 + R27 /api/devices 真值。"""
    c = _client(tmp_path)
    r = c.get("/").text
    for zone in ("风险仪表", "设备状态", "d-risk", "band-s0"):
        assert zone in r, zone
    tl = c.get("/timeline").text
    assert "事件流" in tl and "证据链" in tl
    wf = c.get("/waterfall").text
    assert "waterfall" in wf and "只收不发" in wf
    rp = c.get("/replay").text
    assert "scrub" in rp and "载入" in rp
    cs = c.get("/console").text
    for z in ("maptrack", "故障注入", "事件时间轴", "设备状态", "回放"):
        assert z in cs, z
    # R27 真值：合成源恒在、SDR 无 uhd→replay、待接入清单三件
    dev = c.get("/api/devices").json()
    names = {d["name"]: d["state"] for d in dev["devices"]}
    assert names["合成仿真源"] == "active"
    import importlib.util
    uhd_absent = importlib.util.find_spec("uhd") is None
    assert (names["USRP B210 频谱站"] == "replay") == uhd_absent   # 真值钉死
    assert len(dev["pending"]) == 3 and "真机实飞" in str(dev["pending"])


def test_r28_pages_data_wiring(tmp_path):
    """R28 三页数据接通：元素+真帧流到达。"""
    import json
    c = _client(tmp_path)
    dash = c.get("/").text
    assert "minitrack" in dash and "EventSource" in dash and "d-advice" in dash
    tl = c.get("/timeline").text
    assert "api/session/last" in tl and "evidence" in tl   # 自动载入+证据展开
    wf = c.get("/waterfall").text
    assert "api/spectrum/stream" in wf
    # 真帧流到达断言：SSE 前 2 帧含 occ/trace
    r = c.get("/api/spectrum/stream?max_frames=2")
    got = [json.loads(ln[5:]) for ln in r.text.splitlines() if ln.startswith("data:")]
    assert got and "occ" in got[0] and "trace" in got[0]
