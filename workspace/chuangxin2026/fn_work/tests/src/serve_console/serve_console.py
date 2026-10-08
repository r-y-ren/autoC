# serve_console 单测：selftest 四点 + 页面可达
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.serve_console.serve_console import create_app  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402


def test_health_scenarios_page():
    app = create_app()
    with TestClient(app) as c:
        assert c.get("/api/health").json()["ok"]
        assert len(c.get("/api/scenarios").json()["scenarios"]) >= 4
        html = c.get("/").text
        assert "急" in html and ("ws" in html.lower() or "websocket" in html.lower())


def test_estop_changes_state():
    app = create_app()
    with TestClient(app) as c:
        before = c.get("/api/health").json()["state"]
        r = c.post("/api/estop").json()["state"]
        assert before == "armed" and r.startswith("fired")


# ---- 演进轮二集成（R17/R18） ----


def test_r17_devices_endpoint():
    app = create_app()
    with TestClient(app) as c:
        devs = c.get("/api/devices").json()["devices"]
        assert len(devs) >= 6
        assert any(e["id"] == "b210" for e in devs)
        assert all(set(e) >= {"id", "name", "status", "detail", "ts"} for e in devs)


def test_r18_theme_and_status_bar_all_pages():
    app = create_app()
    with TestClient(app) as c:
        for path in ("/", "/reports", "/help"):
            html = c.get(path).text
            assert "device-bar" in html, path          # 状态栏挂载
            assert "--accent" in html, path            # 统一主题变量
            assert "dot " in html or "dot ok" in html or "dev-chips" in html, path
        home = c.get("/").text
        assert "急 停" in home and "btn-danger" in home  # 急停危险色醒目
        assert "报告中心" in home and "帮助" in home
