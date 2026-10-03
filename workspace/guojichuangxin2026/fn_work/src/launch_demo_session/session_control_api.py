"""控制台后端 API：发起/中止/注入/调强度/回放/状态查询（launch_demo_session 块）。"""
from __future__ import annotations

import json

SESSIONS: dict = {}          # id → 会话句柄（launch_demo_session 产出）
LAST_RUN: dict = {}          # {"id":..., "run_dir":...}


def mount_control_api(app):
    """把控制端点挂到 FastAPI app（register_pages 调用）。"""
    from fastapi.responses import JSONResponse, StreamingResponse

    def _err(msg, code=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=code)

    @app.post("/api/session/start")
    async def start(payload: dict = None):
        payload = payload or {}
        scenario = payload.get("scenario", "lowbat_headwind")
        duration = float(payload.get("duration_s", 8.0))
        try:
            from launch_demo_session.launch_demo_session import launch_demo_session
            handle = launch_demo_session({"scenario": scenario, "duration_s": duration},
                                         app.state.cfg if hasattr(app.state, "cfg") else {})
        except Exception as exc:
            return _err(str(exc))
        SESSIONS[handle["id"]] = handle
        LAST_RUN.update({"id": handle["id"], "run_dir": handle["run_dir"]})
        return {"ok": True, "id": handle["id"], "run_dir": handle["run_dir"],
                "state": handle["status"]()}

    @app.post("/api/session/inject")
    async def inject(payload: dict = None):
        payload = payload or {}
        sid = payload.get("id") or (max(SESSIONS) if SESSIONS else None)
        if sid not in SESSIONS:
            return _err(f"无会话 {sid}", 404)
        return SESSIONS[sid]["inject"](payload.get("level", "mid"))

    @app.post("/api/session/abort")
    async def abort(payload: dict = None):
        payload = payload or {}
        sid = payload.get("id") or (max(SESSIONS) if SESSIONS else None)
        if sid not in SESSIONS:
            return _err(f"无会话 {sid}", 404)
        SESSIONS[sid]["abort"]()
        return {"ok": True, "state": SESSIONS[sid]["status"]()}

    @app.get("/api/session/last")
    async def last():
        return JSONResponse(LAST_RUN or {"none": True})

    @app.get("/api/session/stream")
    async def stream():
        hub = getattr(app.state, "hub", None)
        if hub is None:
            return _err("无事件枢纽", 503)

        async def gen():
            q = hub.subscribe("event")
            try:
                while True:
                    try:
                        import asyncio
                        item = await asyncio.wait_for(q.get(), timeout=5.0)
                        yield f"data: {item}\n\n"
                    except Exception:
                        yield ": keepalive\n\n"
            finally:
                hub.unsubscribe("event", q)

        return StreamingResponse(gen(), media_type="text/event-stream")

    return app
