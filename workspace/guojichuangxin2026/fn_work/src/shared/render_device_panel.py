"""设备状态面板 HTML（已接设备徽标+待接入清单；控制台与仪表盘共用）（shared 块）。"""
from __future__ import annotations

_BADGE = {"active": ("在线", "b-ok"), "device": ("真机在线", "b-ok"),
          "replay": ("回放降级", "b-warn"), "ready": ("就绪", "b-ok"),
          "pending": ("待设备", "b-mute"), "degraded": ("失健降级", "b-warn"),
          "off": ("缺席", "b-mute")}


def render_device_panel(device_report: dict) -> str:
    """device_report: {"devices":[{name,state,note}], "pending":[{name,status,note}]}。

    纯模板无副作用：state ∈ {active,device,replay,ready,pending,degraded,off}。
    输出两区 HTML 片段（已接设备徽标表 + 待接入清单表）。
    """
    devices = device_report.get("devices") or []
    pending = device_report.get("pending") or []
    rows = []
    for d in devices:
        label, cls = _BADGE.get(str(d.get("state", "off")), ("未知", "b-mute"))
        rows.append(
            f"<tr><td class='dv-name'>{d.get('name', '?')}</td>"
            f"<td><span class='badge {cls}'>{label}</span></td>"
            f"<td class='dv-note'>{d.get('note', '')}</td></tr>")
    pend = []
    for p in pending:
        pend.append(
            f"<tr><td class='dv-name'>{p.get('name', '?')}</td>"
            f"<td><span class='badge b-mute'>{p.get('status', '待设备')}</span></td>"
            f"<td class='dv-note'>{p.get('note', '')}</td></tr>")
    devices_html = "\n".join(rows) or "<tr><td colspan=3 class='dv-note'>无设备报告</td></tr>"
    pending_html = "\n".join(pend) or "<tr><td colspan=3 class='dv-note'>无待接入项</td></tr>"
    return f"""<div class="dv-panel" id="device-panel">
<div class="dv-block"><div class="dv-title">已接设备</div>
<table class="dv-table">{devices_html}</table></div>
<div class="dv-block"><div class="dv-title">待接入清单</div>
<table class="dv-table">{pending_html}</table></div>
</div>"""
