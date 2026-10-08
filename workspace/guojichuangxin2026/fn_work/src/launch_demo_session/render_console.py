"""控制台页（R26 六区指挥中心布局；功能完整优先）（launch_demo_session 块）。"""
from __future__ import annotations

from shared.render_device_panel import render_device_panel


def render_console(context: dict) -> str:
    """六区：顶栏色带/地图航迹/数字仪表/注入面板/设备状态/事件时间轴；SSE 显示端过滤 sev=0。"""
    report = context.get("device_report") or {}
    panel = render_device_panel(report)
    return f"""<!doctype html><html lang='zh'><head><meta charset='utf-8'>
<title>演示控制台 · 安航云盾</title><style>
:root{{--bg:#0b1220;--panel:#111a2e;--line:#24365e;--txt:#cfe3ff;--dim:#7d93b8;
--ok:#22c55e;--warn:#eab308;--bad:#ef4444;--accent:#38bdf8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--txt);
font-family:system-ui,sans-serif;font-size:17px}}
.hd{{display:flex;align-items:center;gap:18px;padding:14px 22px;border-bottom:2px solid var(--line)}}
.hd h1{{font-size:22px;margin:0}}.band{{display:flex;gap:4px;margin-left:auto}}
.band span{{padding:5px 14px;border-radius:4px;font-size:13px;font-weight:600;opacity:.55}}
.band .s0{{background:#14532d}}.band .s1{{background:#4d7c0f}}.band .s2{{background:#a16207}}
.band .s3{{background:#c2410c}}.band .s4{{background:#b91c1c}}
.band span.on{{opacity:1;box-shadow:0 0 12px rgba(255,255,255,.35)}}
.wrap{{padding:16px 22px;display:grid;grid-template-columns:1.5fr 1fr;gap:14px}}
.col{{display:flex;flex-direction:column;gap:14px}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}}
.ptitle{{font-size:14px;color:var(--dim);letter-spacing:2px;margin:0 0 10px}}
.gauges{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.stat{{background:#0d1626;border:1px solid var(--line);border-radius:8px;padding:12px}}
.stat .k{{font-size:12px;color:var(--dim)}}.stat .v{{font-size:30px;font-weight:700}}
.bar{{height:10px;background:#0a1220;border-radius:5px;overflow:hidden;margin-top:6px}}
.bar i{{display:block;height:100%;background:var(--accent)}}
button{{background:#1d4ed8;color:#fff;border:0;border-radius:8px;padding:10px 18px;
margin:4px;font-size:16px;cursor:pointer}}button.warn{{background:#b91c1c}}
input[type=range]{{width:70%}}select{{background:#0d1626;color:var(--txt);
border:1px solid var(--line);border-radius:6px;padding:8px;font-size:15px}}
.badge{{display:inline-block;padding:3px 12px;border-radius:12px;font-size:13px;font-weight:600}}
.b-ok{{background:#14532d;color:#86efac}}.b-warn{{background:#713f12;color:#fde047}}
.b-mute{{background:#1e293b;color:#94a3b8}}
.dv-table{{width:100%;border-collapse:collapse;font-size:14px}}
.dv-table td{{padding:7px 8px;border-bottom:1px solid var(--line)}}
.dv-name{{font-weight:600}}.dv-note{{color:var(--dim);font-size:13px}}
.dv-title{{font-size:13px;color:var(--dim);letter-spacing:2px;margin:8px 0 4px}}
.timeline{{list-style:none;margin:0;padding:0;max-height:300px;overflow:auto}}
.timeline li{{padding:8px 10px;border-left:3px solid var(--line);margin:6px 0;
background:#0d1626;border-radius:0 6px 6px 0;font-size:14px}}
canvas{{width:100%;background:#081020;border:1px solid var(--line);border-radius:8px}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:6px 0}}
.card{{background:#0d1626;border:2px solid var(--line);border-radius:8px;padding:10px;
cursor:pointer;text-align:center;font-size:13px}}
.card.on{{border-color:var(--accent);box-shadow:0 0 10px rgba(56,189,248,.4)}}
.card b{{font-size:15px}}
.muted{{color:var(--dim)}}#status{{font-size:1.3em;font-weight:600}}
</style></head><body>
<div class='hd'><h1>安航云盾 · 演示控制台</h1>
<a href='/' style='margin-left:12px;color:#7d93b8'>仪表盘</a>
<div class='band'>{''.join(f"<span class='s{i}' id='band-s{i}'>{n}</span>" for i, n in enumerate(['S0 正常','S1 关注','S2 预警','S3 严重','S4 紧急']))}</div></div>
<div class='wrap'><div class='col'>
<div class='panel'><div class='ptitle'>任务地图 · 航迹</div><canvas id='maptrack' height='300'></canvas></div>
<div class='panel'><div class='ptitle'>飞行仪表</div><div class='gauges'>
<div class='stat'><div class='k'>风险等级</div><div class='v' id='g-risk'>S0</div>
<div class='bar'><i id='g-risk-bar' style='width:8%'></i></div></div>
<div class='stat'><div class='k'>剩余安全时间</div><div class='v' id='g-time'>—</div>
<div class='bar'><i id='g-time-bar' style='width:50%'></i></div></div>
<div class='stat'><div class='k'>返航能源余量</div><div class='v' id='g-energy'>—</div>
<div class='bar'><i id='g-energy-bar' style='width:50%'></i></div></div>
<div class='stat'><div class='k'>高度</div><div class='v' id='g-alt'>—</div>
<div class='bar'><i style='width:30%'></i></div></div>
<div class='stat'><div class='k'>地速</div><div class='v' id='g-speed'>—</div>
<div class='bar'><i style='width:30%'></i></div></div>
</div></div>
<div class='panel'><div class='ptitle'>事件时间轴（证据链）</div>
<ul class='timeline' id='events'></ul></div>
</div><div class='col'>
<div class='panel'><div class='ptitle'>故障注入 · 操控</div>
<input type='hidden' id='scenario' value='lowbat_headwind'>
<div class='cards'>
<div class='card on' data-scn='lowbat_headwind' onclick='pickScn(this)'>慢危险<br><b>低电量+逆风</b></div>
<div class='card' data-scn='motor_fail' onclick='pickScn(this)'>快危险<br><b>电机故障</b></div>
<div class='card' data-scn='link_degrade' onclick='pickScn(this)'>链路<br><b>频谱被挤占</b></div>
</div>
<button onclick='startSession()'>起飞</button>
<button onclick='flowStart()' style='background:#0f766e'>▶ 一键演示</button>
<button onclick='flowPause()'>⏸ 暂停</button>
<button onclick='flowResume()'>⏵ 继续</button>
<button class='warn' onclick='inject()'>注入故障</button>
<div>强度 <input type='range' id='level' min='0' max='2' value='1'></div>
<button onclick='abortSession()'>中止</button>
<div id='status' class='muted'>待命</div><div id='advice' class='muted'></div></div>
<div class='panel'><div class='ptitle'>频谱 waterfall</div><canvas id='waterfall' height='140'></canvas>
<div class='muted'>device=真机 / replay=回放</div></div>
<div class='panel'><div class='ptitle'>设备状态</div>{panel}</div>
<div class='panel'><div class='ptitle'>回放</div>
<button onclick='replay()'>回放最近会话</button><div id='replay' class='muted'></div></div>
</div></div>
<script>
const track=[];const MAXP=240;
function drawMap(){{const c=document.getElementById('maptrack'),x=c.getContext('2d');
 x.clearRect(0,0,c.width,c.height);
 x.strokeStyle='#1b2b4d';for(let i=1;i<6;i++){{x.beginPath();x.moveTo(0,i*c.height/6);
 x.lineTo(c.width,i*c.height/6);x.stroke();x.beginPath();x.moveTo(i*c.width/6,0);
 x.lineTo(i*c.width/6,c.height);x.stroke();}}
 if(track.length>1){{x.strokeStyle='#38bdf8';x.lineWidth=2;x.beginPath();
 x.moveTo(track[0][0],track[0][1]);for(const p of track)x.lineTo(p[0],p[1]);x.stroke();
 x.fillStyle='#fff';const q=track[track.length-1];
 if(track.length>1){{const pv=track[track.length-2],ang=Math.atan2(q[1]-pv[1],q[0]-pv[0]);
  x.save();x.translate(q[0],q[1]);x.rotate(ang);x.beginPath();
  x.moveTo(10,0);x.lineTo(-7,6);x.lineTo(-7,-6);x.closePath();x.fill();x.restore();}}
 else{{x.beginPath();x.arc(q[0],q[1],5,0,7);x.fill();}}}}}}
function setBand(s){{for(let i=0;i<5;i++)document.getElementById('band-s'+i)?.classList.remove('on');
 document.getElementById('band-s'+(s||0))?.classList.add('on');}}
async function startSession(){{const r=await api('/api/session/start',{{scenario:scenario.value,duration_s:12}});
 setStatus(JSON.stringify(r).slice(0,120));}}
async function inject(){{await api('/api/session/inject',{{level:['low','mid','high'][level.value]}});}}
async function abortSession(){{await api('/api/session/abort',{{}});}}
async function replay(){{const r=await fetch('/api/session/last');
 document.getElementById('replay').textContent=JSON.stringify(await r.json());}}
async function api(path,body){{const r=await fetch(path,{{method:'POST',
 headers:{{'Content-Type':'application/json'}},body:JSON.stringify(body)}});
 const j=await r.json();setStatus(JSON.stringify(j).slice(0,120));return j;}}
function pickScn(el){{document.querySelectorAll('.card').forEach(c=>c.classList.remove('on'));
 el.classList.add('on');document.getElementById('scenario').value=el.dataset.scn;}}
async function flowStart(){{const r=await api('/api/demo/flow/start',{{}});
 setStatus('一键演示：'+JSON.stringify(r.story));}}
async function flowPause(){{await api('/api/demo/flow/pause',{{}});}}
async function flowResume(){{await api('/api/demo/flow/resume',{{}});}}
function setStatus(t){{document.getElementById('status').textContent=t;}}
const es=new EventSource('/api/session/stream');
es.onmessage=e=>{{const m=JSON.parse(e.data);
 if(m.state){{const s=parseInt(m.state.slice(1))||0;setBand(s);
  document.getElementById('g-risk').textContent=m.state;
  document.getElementById('g-risk-bar').style.width=(8+s*23)+'%';}}
 if(m.advice){{document.getElementById('advice').textContent='建议：'+(m.advice.action||'');
  if(m.advice.reason)document.getElementById('advice').title=m.advice.reason;}}
 if(m.time!=null)document.getElementById('g-time').textContent=Math.round(m.time)+'s';
 if(m.nav){{const c=document.getElementById('maptrack');
  if(m.nav.alt!=null)document.getElementById('g-alt').textContent=Math.round(m.nav.alt)+'m';
  if(m.nav.speed!=null)document.getElementById('g-speed').textContent=m.nav.speed+'m/s';
  track.push([((m.nav.lon-118.8)*1e5%c.width+c.width)%c.width,
              (32.002-m.nav.lat)*1e5%c.height+c.height)%c.height]);
  if(track.length>MAXP)track.shift();drawMap();
  if(m.nav.energy!=null){{document.getElementById('g-energy').textContent=Math.round(m.nav.energy)+'%';
   document.getElementById('g-energy-bar').style.width=Math.max(4,Math.min(100,m.nav.energy))+'%';}}}}
 if(m.summary||m.event){{const li=document.createElement('li');
  li.textContent=m.summary||m.event;document.getElementById('events').prepend(li);}}
 if(m.occ){{document.getElementById('waterfall').title='占用率 '+JSON.stringify(m.occ);}}}};
drawMap();
</script></body></html>"""
