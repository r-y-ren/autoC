"""挂载五页路由与 API（功能完整优先，视觉打磨不阻塞）（run_ground_station 块）。"""
from __future__ import annotations

_DARK = "background:#0b1220;color:#cfe3ff;font-family:system-ui,sans-serif;padding:24px"


def _page(title, body):
    return (f"<!doctype html><html lang='zh'><head><meta charset='utf-8'>"
            f"<title>{title} · 安航云盾</title></head>"
            f"<body style='{_DARK}'><h1>安航云盾 · {title}</h1>{body}</body></html>")


def register_pages(app, runs_root):
    """五页：/ 仪表盘、/timeline、/waterfall、/replay、/console；API：/api/state。"""
    from pathlib import Path

    from fastapi import HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse

    state = {"latest": {"state": "S0", "risk": None, "advice": None}}

    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return _page("仪表盘",
            "<div id='risk'>风险等级 S0</div><div id='time'>剩余安全时间 —</div>"
            "<div id='energy'>返航能源余量 —</div><a href='/console'>控制台</a>")

    @app.get("/timeline", response_class=HTMLResponse)
    def timeline():
        return _page("事件时间线", "<ul id='events'></ul><div id='evidence'></div>")

    @app.get("/waterfall", response_class=HTMLResponse)
    def waterfall():
        return _page("频谱瀑布", "<canvas id='waterfall'></canvas>")

    @app.get("/replay", response_class=HTMLResponse)
    def replay():
        return _page("回放", "<input id='run'><button>载入</button>"
                     "<div id='timeline'></div>")

    @app.get("/console", response_class=HTMLResponse)
    def console():
        from launch_demo_session.render_console import render_console
        return HTMLResponse(render_console({}))

    @app.get("/api/state")
    def api_state():
        return JSONResponse(state["latest"])

    @app.get("/api/runs")
    def api_runs():
        root = Path(runs_root)
        runs = sorted(str(p) for p in root.glob("*/*") if p.is_dir()) if root.exists() else []
        return JSONResponse({"runs": runs})

    @app.get("/api/runs/{run}/frames")
    def api_frames(run: str, q: int = 0):
        for cand in Path(runs_root).glob(f"*/{run}/frames/frames.jsonl"):
            lines = cand.read_text(encoding="utf-8").splitlines()
            win = lines[q * 20:(q + 1) * 20]
            return JSONResponse({"frames": win, "next": q + 1 if win else None})
        raise HTTPException(404, f"run {run} 不存在")

    app.state.hub_state = state
    return app
