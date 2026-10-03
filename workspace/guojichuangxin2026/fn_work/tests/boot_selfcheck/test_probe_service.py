"""probe_service 单测。"""
from __future__ import annotations

import threading

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_reachable_and_refused():
    from boot_selfcheck.probe_service import probe_service
    from run_ground_station.register_pages import register_pages
    app = FastAPI()
    register_pages(app, "runs")
    port = 8791
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                           log_level="error"))
    threading.Thread(target=server.run, daemon=True).start()
    import time
    for _ in range(30):
        if server.started:
            break
        time.sleep(0.1)
    ok = probe_service(f"http://127.0.0.1:{port}", retries=1)
    assert ok["reachable"] and ok["latency_ms"] >= 0
    server.should_exit = True
    bad = probe_service("http://127.0.0.1:1", timeout_s=0.2, retries=1)
    assert bad["reachable"] is False
