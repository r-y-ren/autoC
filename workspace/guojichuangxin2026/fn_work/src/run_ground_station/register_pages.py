"""挂载五页路由与 API（功能完整优先，视觉打磨不阻塞）（run_ground_station 块）。"""
from __future__ import annotations

import json

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

    def _summarize_event(ev: dict) -> str:
        """证据→结论中文摘要（确定性模板，R21）。"""
        et = ev.get("type")
        if et == "state":
            adv = (ev.get("advice") or {}).get("action", "")
            return f"状态转为 {ev.get('state', '?')}。依据：{adv or '风险分值与持续时间条件满足'}。"
        if et == "sudden":
            ch = "、".join(ev.get("channels") or [])
            return (f"突发故障确认：{ev.get('fault', '未知')}（通道 {ch}，"
                    f"确认时延 {ev.get('latency_s', '?')}s）。证据：残差通道越阈并持续确认窗。")
        if et == "progressive":
            risk = (ev.get("risk") or {}).get("intervals", {})
            iv = risk.get("5") or {}
            base = ev.get("baseline") or {}
            trig = [k for k, v in base.items() if v]
            if iv:
                return (f"渐进风险：5 秒危险概率 {iv.get('prob', 0):.2f}"
                        f"（区间 {iv.get('lo', 0):.2f}~{iv.get('hi', 0):.2f}）。"
                        f"证据：物理余量收窄项 {'、'.join(trig) or '无'}；共形区间为统计保证口径。")
            return (f"渐进风险（降级通道）：物理余量收窄项 {'、'.join(trig) or '无'}。"
                    f"证据：四类余量低于阈值且持续达标。")
        return str(ev.get("t", ""))

    @app.get("/api/runs/{run}/frames")
    def api_frames(run: str, q: int = 0):
        for cand in Path(runs_root).glob(f"*/{run}/frames/frames.jsonl"):
            lines = cand.read_text(encoding="utf-8").splitlines()
            win = lines[q * 20:(q + 1) * 20]
            ev_fp = cand.parent.parent / "events.jsonl"
            evs = []
            if ev_fp.exists():
                for ln in ev_fp.read_text(encoding="utf-8").splitlines()[:200]:
                    try:
                        e = json.loads(ln)
                        evs.append({**e, "summary": _summarize_event(e)})
                    except Exception:
                        pass
            return JSONResponse({"frames": win, "next": q + 1 if win else None,
                                 "events": evs})
        raise HTTPException(404, f"run {run} 不存在")

    app.state.hub_state = state
    return app
