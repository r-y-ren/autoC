"""控制台页（功能完整优先：注入面板/状态区/时间轴/瀑布嵌入）（launch_demo_session 块）。"""
from __future__ import annotations


def render_console(context: dict) -> str:
    return """<!doctype html><html lang='zh'><head><meta charset='utf-8'>
<title>演示控制台 · 安航云盾</title><style>
body{background:#0b1220;color:#cfe3ff;font-family:system-ui;padding:20px}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:12px}
.panel{background:#111a2e;border:1px solid #24365e;border-radius:8px;padding:12px}
button{background:#1d4ed8;color:#fff;border:0;border-radius:6px;padding:8px 14px;margin:4px;cursor:pointer}
button.warn{background:#b91c1c} input[type=range]{width:70%}
#status{font-size:1.3em;font-weight:600} .muted{color:#7d93b8}
</style></head><body>
<h1>安航云盾 · 演示控制台</h1>
<div class='grid'>
<div class='panel'><h3>任务</h3>
<select id='scenario'><option>lowbat_headwind</option><option>motor_fail</option><option>link_degrade</option></select>
<button onclick='startSession()'>起飞</button>
<button class='warn' onclick='inject()'>注入故障</button>
<div>强度 <input type='range' id='level' min='0' max='2' value='1'></div>
<button onclick='abortSession()'>中止</button>
<div id='status' class='muted'>待命</div><div id='advice' class='muted'></div></div>
<div class='panel'><h3>频谱</h3><canvas id='waterfall' width='360' height='160'></canvas></div>
<div class='panel'><h3>事件时间轴</h3><ul id='events'></ul></div>
<div class='panel'><h3>回放</h3><button onclick='replay()'>回放最近会话</button>
<div id='replay'></div></div></div>
<script>
async function startSession(){await api('/api/session/start',{scenario:scenario.value})}
async function inject(){await api('/api/session/inject',{level:['low','mid','high'][level.value]})}
async function abortSession(){await api('/api/session/abort',{})}
async function replay(){const r=await fetch('/api/session/last');document.getElementById('replay').textContent=JSON.stringify(await r.json())}
async function api(path,body){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});document.getElementById('status').textContent=JSON.stringify(await r.json())}
const es=new EventSource('/api/session/stream');es.onmessage=e=>{const m=JSON.parse(e.data);if(m.state)document.getElementById('status').textContent=m.state;if(m.advice)document.getElementById('advice').textContent=m.advice?.action||'';if(m.event)document.getElementById('events').innerHTML+='<li>'+m.event+'</li>'}
</script></body></html>"""
