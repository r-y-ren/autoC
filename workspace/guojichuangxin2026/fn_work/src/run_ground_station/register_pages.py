"""挂载五页路由与 API（R26/R27 改造：统一指挥中心壳+设备状态）（run_ground_station 块）。"""
from __future__ import annotations

import json

_CSS = """
:root{--bg:#0b1220;--panel:#111a2e;--line:#24365e;--txt:#cfe3ff;--dim:#7d93b8;
--ok:#22c55e;--warn:#eab308;--bad:#ef4444;--accent:#38bdf8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);
font-family:system-ui,'Segoe UI',sans-serif;font-size:17px}
.hd{display:flex;align-items:center;gap:18px;padding:14px 22px;border-bottom:2px solid var(--line)}
.hd h1{font-size:22px;margin:0;letter-spacing:1px}
.band{display:flex;gap:4px;margin-left:auto}
.band span{padding:5px 14px;border-radius:4px;font-size:13px;font-weight:600;opacity:.55}
.band .s0{background:#14532d}.band .s1{background:#4d7c0f}.band .s2{background:#a16207}
.band .s3{background:#c2410c}.band .s4{background:#b91c1c}
.band span.on{opacity:1;box-shadow:0 0 12px rgba(255,255,255,.35)}
.wrap{padding:16px 22px;display:grid;grid-template-columns:1.6fr 1fr;gap:14px}
.col{display:flex;flex-direction:column;gap:14px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}
.ptitle{font-size:14px;color:var(--dim);letter-spacing:2px;margin:0 0 10px}
.gauges{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.stat{background:#0d1626;border:1px solid var(--line);border-radius:8px;padding:12px}
.stat .k{font-size:12px;color:var(--dim)}.stat .v{font-size:30px;font-weight:700}
.bar{height:10px;background:#0a1220;border-radius:5px;overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;background:var(--accent)}
button{background:#1d4ed8;color:#fff;border:0;border-radius:8px;padding:10px 18px;
margin:4px;font-size:16px;cursor:pointer}button.warn{background:#b91c1c}
button:hover{filter:brightness(1.15)}
input[type=range]{width:70%}
select{background:#0d1626;color:var(--txt);border:1px solid var(--line);
border-radius:6px;padding:8px;font-size:15px}
.badge{display:inline-block;padding:3px 12px;border-radius:12px;font-size:13px;font-weight:600}
.b-ok{background:#14532d;color:#86efac}.b-warn{background:#713f12;color:#fde047}
.b-mute{background:#1e293b;color:#94a3b8}
.dv-table{width:100%;border-collapse:collapse;font-size:14px}
.dv-table td{padding:7px 8px;border-bottom:1px solid var(--line)}
.dv-name{font-weight:600}.dv-note{color:var(--dim);font-size:13px}
.dv-title{font-size:13px;color:var(--dim);letter-spacing:2px;margin:8px 0 4px}
.timeline{list-style:none;margin:0;padding:0;max-height:340px;overflow:auto}
.timeline li{padding:8px 10px;border-left:3px solid var(--line);margin:6px 0;
background:#0d1626;border-radius:0 6px 6px 0;font-size:14px}
.timeline li .ev-sev1{border-color:#4d7c0f}.ev-sev2{border-color:#a16207}
.ev-sev3{border-color:#c2410c}.ev-sev4{border-color:#b91c1c}
.muted{color:var(--dim)}canvas{width:100%;background:#081020;border:1px solid var(--line);
border-radius:8px}
"""


def _page(title: str, body: str, active: int = 0) -> str:
    """R26 改造：统一指挥中心壳（CSS 变量/布局/顶栏 S0-S4 状态色带）。"""
    names = ["仪表盘", "事件时间线", "频谱瀑布", "回放", "控制台"]
    hrefs = ["/", "/timeline", "/waterfall", "/replay", "/console"]
    nav = "".join(
        f"<a href='{hrefs[i]}' style='color:{'#fff' if i == active else '#7d93b8'};"
        f"text-decoration:none;margin-left:14px'>{names[i]}</a>" for i in range(5))
    band = "".join(f"<span class='s{i}' id='band-s{i}'>{n}</span>"
                   for i, n in enumerate(["S0 正常", "S1 关注", "S2 预警", "S3 严重", "S4 紧急"]))
    return (f"<!doctype html><html lang='zh'><head><meta charset='utf-8'>"
            f"<title>{title} · 安航云盾</title><style>{_CSS}</style></head><body>"
            f"<div class='hd'><h1>安航云盾 · {title}</h1><nav>{nav}</nav>"
            f"<div class='band'>{band}</div></div>{body}</body></html>")


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


def register_pages(app, runs_root):
    """五页路由与 API（含 R27 /api/devices）；R26 统一壳下的分区布局。"""
    from pathlib import Path

    from fastapi import HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse

    from shared.render_device_panel import render_device_panel

    state = {"latest": {"state": "S0", "risk": None, "advice": None}}

    def _device_report() -> dict:
        """设备真值报告（嵌套闭包，非登记单元）：总线探测+PX4 探测+待接入清单。"""
        import sys
        here = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(here))
        devices = [{"name": "合成仿真源", "state": "active", "note": "内置数据面"}]
        try:
            from batch_eval.probe_px4_env import probe_px4_env
            px = probe_px4_env({})
            devices.append({"name": "PX4 SIH 仿真器", "state": "ready" if px["ready"] else "pending",
                            "note": "真源就绪" if px["ready"] else "工具链未配置"})
        except Exception:
            devices.append({"name": "PX4 SIH 仿真器", "state": "pending", "note": "探测失败"})
        try:
            import uhd  # noqa: F401
            sdr_state, sdr_note = "device", "真机在线（只收不发）"
        except Exception:
            sdr_state, sdr_note = "replay", "uhd 缺席→回放降级（画面等价）"
        devices.append({"name": "USRP B210 频谱站", "state": sdr_state, "note": sdr_note})
        devices.append({"name": "Jetson Orin NX", "state": "pending", "note": "bench 脚本就绪·待设备"})
        pending = [
            {"name": "B210 真机联调", "status": "脚本就绪", "note": "calibrate_usrp --mode device"},
            {"name": "Orin NX 部署实测", "status": "脚本就绪", "note": "bench_edge --mode deploy"},
            {"name": "真机实飞（档 C）", "status": "待导师批", "note": "硬件采购表见材料包"},
        ]
        return {"devices": devices, "pending": pending}

    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return _page("仪表盘", f"""
<div class='wrap'><div class='col'>
<div class='panel'><div class='ptitle'>风险仪表</div><div class='gauges'>
<div class='stat'><div class='k'>风险等级</div><div class='v' id='d-risk'>S0</div>
<div class='bar'><i id='d-risk-bar' style='width:8%'></i></div></div>
<div class='stat'><div class='k'>返航能源余量</div><div class='v' id='d-energy'>—</div>
<div class='bar'><i id='d-energy-bar' style='width:50%'></i></div></div>
<div class='stat'><div class='k'>剩余安全时间</div><div class='v' id='d-time'>—</div>
<div class='bar'><i id='d-time-bar' style='width:50%'></i></div></div>
</div></div>
<div class='panel'><div class='ptitle'>设备状态</div>{render_device_panel(_device_report())}</div>
</div><div class='col'>
<div class='panel'><div class='ptitle'>快捷入口</div>
<a href='/console'><button>进入演示控制台</button></a>
<a href='/timeline'><button>事件时间线</button></a></div>
<div class='panel'><div class='ptitle'>口径注记</div>
<div class='muted'>数据面：合成源出事件指标 / PX4 真源验数据链路（每条记录标注来源）。</div></div>
</div></div>""", 0)

    @app.get("/timeline", response_class=HTMLResponse)
    def timeline():
        return _page("事件时间线", """
<div class='wrap'><div class='col'>
<div class='panel'><div class='ptitle'>事件流（带证据链摘要）</div>
<ul class='timeline' id='events'></ul></div></div>
<div class='col'><div class='panel'><div class='ptitle'>证据展开</div>
<div id='evidence' class='muted'>点击事件查看证据链</div></div></div></div>
<script>fetch('/api/state').then(r=>r.json()).then(s=>{
 if(s.state)document.getElementById('band-s'+s.state.slice(1))?.classList.add('on')})</script>""", 1)

    @app.get("/waterfall", response_class=HTMLResponse)
    def waterfall():
        return _page("频谱瀑布", """
<div class='wrap'><div class='col'>
<div class='panel'><div class='ptitle'>2.4GHz 遥测频段（只收不发）</div>
<canvas id='waterfall' height='320'></canvas>
<div class='muted'>来源标注：device=真机 / replay=回放（画面等价）</div></div></div>
<div class='col'><div class='panel'><div class='ptitle'>信道占用</div>
<div id='occ' class='muted'>等待帧流…</div></div></div></div>""", 2)

    @app.get("/replay", response_class=HTMLResponse)
    def replay():
        return _page("回放", """
<div class='wrap'><div class='col'>
<div class='panel'><div class='ptitle'>运行回放</div>
<input id='run' placeholder='运行目录名' style='background:#0d1626;color:#cfe3ff;
border:1px solid #24365e;border-radius:6px;padding:8px;width:60%'>
<button onclick='loadRun()'>载入</button>
<input type='range' id='scrub' min='0' max='100' value='0' style='width:100%'>
<ul class='timeline' id='rtimeline'></ul></div></div>
<div class='col'><div class='panel'><div class='ptitle'>证据链</div>
<div id='replay-evidence' class='muted'>拖动时间轴查看</div></div></div></div>
<script>
async function loadRun(){
 const r=await fetch('/api/runs/'+document.getElementById('run').value+'/frames');
 const j=await r.json();
 const ul=document.getElementById('rtimeline');ul.innerHTML='';
 (j.events||[]).forEach(e=>{ul.innerHTML+='<li>'+e.summary+'</li>'});
}
</script>""", 3)

    @app.get("/console", response_class=HTMLResponse)
    def console():
        from launch_demo_session.render_console import render_console
        return HTMLResponse(render_console({"device_report": _device_report()}))

    @app.get("/api/state")
    def api_state():
        return JSONResponse(state["latest"])

    @app.get("/api/devices")
    def api_devices():
        """R27：设备真值（registry+探测+待接入清单）。"""
        return JSONResponse(_device_report())

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
