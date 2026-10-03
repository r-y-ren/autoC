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
        assert "急" in html and "ws" in html.lower() or "websocket" in html.lower()


def test_estop_changes_state():
    app = create_app()
    with TestClient(app) as c:
        before = c.get("/api/health").json()["state"]
        r = c.post("/api/estop").json()["state"]
        assert before == "armed" and r.startswith("fired")
