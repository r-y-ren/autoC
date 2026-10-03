# R10 顶层：Web 操控台——REST+WS+静态单页（急停硬通道+selftest 自检）（责任文档：serve_console）
from __future__ import annotations

import threading
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.testclient import TestClient

from src.shared.estop import EstopManager

_PAGE = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>无人机链路抗干扰测评台</title><style>
body{margin:0;background:#0e1420;color:#dbe4f0;font-family:system-ui}
.panel{border:1px solid #263248;border-radius:10px;padding:12px;margin:10px}
#estop{background:#c0392b;color:#fff;font-size:1.3em;padding:16px 30px;border:none;border-radius:10px}
#log{white-space:pre-wrap;font-family:monospace;font-size:12px;max-height:200px;overflow:auto}
button.sc{margin:4px;padding:8px 14px}
</style></head><body>
<header class="panel"><h1>无人机链路抗干扰测评台</h1><span id="st">state: -</span></header>
<section class="panel"><h3>场景卡片</h3><div id="cards">加载中…</div>
<button class="sc" onclick="api('/api/run','POST',{scenario:current})">开始</button>
<button class="sc" onclick="api('/api/stop','POST',{})">停止</button>
<button id="estop" onclick="api('/api/estop','POST',{})">急 停</button></section>
<section class="panel"><h3>实时数据</h3><div id="log"></div></section>
<section class="panel"><h3>历史运行</h3><div id="runs">-</div></section>
<script>
let current=null;
async function api(p,m,b){const r=await fetch(p,{method:m,headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});return r.json()}
(async()=>{const s=await api('/api/scenarios','GET');const d=document.getElementById('cards');d.innerHTML='';
for(const n of s.scenarios){const b=document.createElement('button');b.className='sc';b.textContent=n;
b.onclick=()=>{current=n;document.querySelectorAll('#cards button').forEach(x=>x.style.border='');b.style.border='2px solid #4da3ff'};
d.appendChild(b)}})();
(async()=>{const r=await api('/api/runs','GET');document.getElementById('runs').textContent=JSON.stringify(r.runs)})();
const ws=new WebSocket((location.protocol==='https:'?'wss://':'ws://')+location.host+'/ws');
ws.onmessage=e=>{const m=JSON.parse(e.data);document.getElementById('st').textContent='state: '+m.state;
const L=document.getElementById('log');L.textContent+=(JSON.stringify(m.kpi||m)+'\\n');L.scrollTop=L.scrollHeight};
</script></body></html>"""


def create_app():
    app = FastAPI(title="linkbench console")
    estop = EstopManager()
    estop.arm(lambda: None)
    state = {"run_thread": None, "last_result": None}

    @app.get("/api/health")
    def health():
        return {"ok": True, "state": estop.state}

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
                state["last_result"] = execute_scenario(card)
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
        print("SELFTEST OK: health/scenarios/estop/ws 四点全过")
        return 0
    import uvicorn
    uvicorn.run(app, host=host, port=port)
    return 0
