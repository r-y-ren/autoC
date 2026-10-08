# R10 顶层：Web 操控台——REST+WS+静态单页（急停硬通道+selftest 自检）（责任文档：serve_console）
from __future__ import annotations

import threading
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.testclient import TestClient

from src.shared.estop import EstopManager

from src.serve_console.render_static_pages import STATUS_BAR_HTML, _CSS

_PAGE = _CSS + """
<header class="panel" style="max-width:960px"><h1>无人机链路抗干扰测评台</h1>
<span id="st">state: -</span></header>
""" + STATUS_BAR_HTML + """
<section class="panel"><h2>场景卡片</h2><div id="cards">加载中…</div>
<button class="btn btn-primary" onclick="api('/api/run','POST',{scenario:current})">开始</button>
<button class="btn" onclick="api('/api/stop','POST',{})">停止</button>
<button class="btn btn-danger" id="estop" onclick="api('/api/estop','POST',{})">急 停</button>
<span style="margin-left:10px"><a href="/reports">报告中心</a> · <a href="/help">帮助</a></span></section>
<section class="panel"><h2>实时数据</h2><div id="log" style="white-space:pre-wrap;font-family:ui-monospace,monospace;font-size:12px;max-height:220px;overflow:auto"></div></section>
<section class="panel"><h2>历史运行</h2><div id="runs">-</div></section>
<script>
let current=null;
async function api(p,m,b){const r=await fetch(p,{method:m,headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});return r.json()}
(async()=>{const s=await api('/api/scenarios','GET');const d=document.getElementById('cards');d.innerHTML='';
for(const n of s.scenarios){const b=document.createElement('button');b.className='btn';b.textContent=n;
b.onclick=()=>{current=n;document.querySelectorAll('#cards button').forEach(x=>x.style.borderColor='');b.style.borderColor='#4da3ff'};
d.appendChild(b)}})();
(async()=>{const r=await api('/api/runs','GET');document.getElementById('runs').textContent=JSON.stringify(r.runs)})();
const ws=new WebSocket((location.protocol==='https:'?'wss://':'ws://')+location.host+'/ws');
ws.onmessage=e=>{const m=JSON.parse(e.data);document.getElementById('st').textContent='state: '+m.state;
const L=document.getElementById('log');L.textContent+=(JSON.stringify(m.kpi||m)+'\n');L.scrollTop=L.scrollHeight};
</script></body></html>"""



def create_app():
    app = FastAPI(title="linkbench console")
    estop = EstopManager()  # 操控台与运行场景共享的硬急停通道
    state = {"run_thread": None, "last_result": None}

    @app.get("/api/health")
    def health():
        return {"ok": True, "state": estop.state}

    @app.get("/api/devices")
    def devices():
        from src.serve_console.probe_device_status import probe_device_status
        return {"devices": probe_device_status()}

    @app.get("/api/scenarios")
    def scenarios():
        d = Path(__file__).resolve().parents[2] / "scenarios"
        names = sorted(p.stem for p in d.glob("*.yaml")) if d.exists() else []
        return {"scenarios": names}

    @app.post("/api/run")
    def run(payload: dict):
        from src.execute_scenario.execute_scenario import execute_scenario
        name = str(payload.get("scenario", "smoke_loop"))
        d = Path(__file__).resolve().parents[2] / "scenarios"
        card = d / (name + ".yaml")

        def _work():
            try:
                state["last_result"] = execute_scenario(card, estop=estop)
            except Exception as exc:  # noqa: BLE001
                estop.fire("ui-run 异常: %s" % exc)

        th = threading.Thread(target=_work, daemon=True)
        state["run_thread"] = th
        th.start()
        return {"started": name}

    @app.post("/api/stop")
    def stop():
        estop.fire("ui-stop")
        return {"state": estop.state}

    @app.post("/api/estop")
    def estop_ep():
        estop.fire("ui-estop")
        return {"state": estop.state}

    @app.get("/api/runs")
    def runs():
        d = Path("runs")
        return {"runs": sorted(p.name for p in d.iterdir()) if d.exists() else []}

    @app.get("/api/runs/{name}/report")
    def run_report(name: str):
        p = Path("runs") / name / "report.md"
        if not p.exists():
            return {"error": "no report", "name": name}
        return {"name": name, "report": p.read_text(encoding="utf-8")}

    @app.post("/api/demo")
    def demo():
        from src.run_demo.run_demo import run_demo

        def _work():
            state["last_result"] = run_demo(quick=True)
        threading.Thread(target=_work, daemon=True).start()
        return {"started": True}

    @app.get("/", response_class=HTMLResponse)
    def page():
        return _PAGE

    # [改造←R13] 报告中心/帮助页 + runs 媒体目录（演进轮一增量挂载）
    from starlette.staticfiles import StaticFiles
    _runs = Path("runs")
    if _runs.exists():
        app.mount("/runs-media", StaticFiles(directory=str(_runs)), name="runsmedia")
    from src.serve_console.render_static_pages import render_static_pages
    render_static_pages(app)

    @app.websocket("/ws")
    async def ws_endpoint(ws: WebSocket):
        await ws.accept()
        try:
            while True:
                await ws.send_json({"type": "state", "state": estop.state,
                                    "kpi": {"link": "wifi", "per": 0.0}})
                import asyncio
                await asyncio.sleep(0.2)
        except WebSocketDisconnect:
            return

    return app


def serve_console(*, host: str = "0.0.0.0", port: int = 8000, selftest: bool = False):
    # selftest：四点无头自检（服务构建/健康/急停生效/WS 心跳）→返回退出码
    app = create_app()
    if selftest:
        with TestClient(app) as c:
            h = c.get("/api/health")
            assert h.status_code == 200 and h.json()["ok"]
            sc = c.get("/api/scenarios")
            assert sc.status_code == 200 and len(sc.json()["scenarios"]) >= 1
            e = c.post("/api/estop")
            assert e.status_code == 200 and e.json()["state"].startswith("fired")
            with c.websocket_connect("/ws") as ws:
                msg = ws.receive_json()
                assert "state" in msg
            dv = c.get("/api/devices").json()["devices"]
            assert len(dv) >= 6 and any(e["id"] == "b210" for e in dv)
            assert all(e["status"] in ("ok", "missing", "pending_manual", "manual_ok")
                       for e in dv)
        print("SELFTEST OK: health/scenarios/estop/ws/devices 五点全过")
        return 0
    import uvicorn
    uvicorn.run(app, host=host, port=port)
    return 0
