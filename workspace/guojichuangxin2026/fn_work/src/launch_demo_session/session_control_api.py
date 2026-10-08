"""控制台后端 API：发起/中止/注入/调强度/回放/状态查询（launch_demo_session 块）。"""
from __future__ import annotations

import json

SESSIONS: dict = {}          # id → 会话句柄（launch_demo_session 产出）
LAST_RUN: dict = {}          # {"id":..., "run_dir":...}
FLOW: dict = {"running": False, "paused": False, "step": -1, "scenario": None,
              "story": [], "log": []}   # R28 一键演示流程状态
import threading as _threading
_FLOW_GATE = _threading.Event()
_FLOW_GATE.set()


def _flow_worker(app, steps):
    """一键演示时序器（嵌套线程体）：按故事线逐步 起飞→注入→等待→中止；步间可暂停。"""
    import time as _t
    from launch_demo_session.launch_demo_session import launch_demo_session as _launch
    FLOW.update(running=True, story=[s["scenario"] for s in steps], log=[])
    try:
        for i, s in enumerate(steps):
            while not _FLOW_GATE.is_set():
                FLOW["paused"] = True
                _FLOW_GATE.wait(timeout=1.0)
            FLOW.update(paused=False, step=i, scenario=s["scenario"])
            try:
                cfg = getattr(app.state, "cfg", {})
                h = _launch({"scenario": s["scenario"],
                             "duration_s": float(s.get("duration_s", 12.0))}, cfg)
                sid = f"flow-{i}"
                h["id"] = sid
                SESSIONS[sid] = h
                _t.sleep(float(s.get("inject_at_s", 4.0)))
                if not FLOW.get("aborted"):
                    h["inject"]("mid")
                _t.sleep(float(s.get("hold_s", 6.0)))
                h["abort"]()
                FLOW["log"].append({"step": i, "scenario": s["scenario"], "ok": True})
            except Exception as exc:
                FLOW["log"].append({"step": i, "scenario": s["scenario"], "error": str(exc)})
    finally:
        FLOW.update(running=False, paused=False)


def session_control_api(app):
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

    @app.post("/api/demo/flow/start")
    async def flow_start(payload: dict = None):
        """R28 一键演示：标准三场景故事线（可传 steps 定制时长）。"""
        payload = payload or {}
        if FLOW.get("running"):
            return _err("流程已在跑", 409)
        default = [{"scenario": "lowbat_headwind", "duration_s": 12, "inject_at_s": 4, "hold_s": 6},
                   {"scenario": "motor_fail", "duration_s": 12, "inject_at_s": 3, "hold_s": 6},
                   {"scenario": "link_degrade", "duration_s": 12, "inject_at_s": 3, "hold_s": 6}]
        steps = payload.get("steps") or default
        FLOW["aborted"] = False
        _FLOW_GATE.set()
        _threading.Thread(target=_flow_worker, args=(app, steps), daemon=True).start()
        return {"ok": True, "story": [s["scenario"] for s in steps]}

    @app.post("/api/demo/flow/pause")
    async def flow_pause():
        if not FLOW.get("running"):
            return _err("流程未在跑", 409)
        _FLOW_GATE.clear()
        FLOW["paused"] = True
        return {"ok": True, "state": {k: FLOW[k] for k in ("step", "scenario", "paused")}}

    @app.post("/api/demo/flow/resume")
    async def flow_resume():
        _FLOW_GATE.set()
        FLOW["paused"] = False
        return {"ok": True, "state": {k: FLOW[k] for k in ("step", "scenario", "paused")}}

    @app.get("/api/demo/flow")
    async def flow_status():
        return JSONResponse(FLOW)

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


mount_control_api = session_control_api   # 兼容别名（历史调用点）
