# 操控台静态页：/reports 报告中心（列表+详情）与 /help 快速上手（R13）
from __future__ import annotations

from pathlib import Path

_CSS = ("<style>body{background:#0e1420;color:#dbe4f0;font-family:system-ui;max-width:960px;margin:auto}"
        ".panel{border:1px solid #263248;border-radius:10px;padding:12px;margin:10px}"
        "a{color:#4da3ff}img{max-width:100%}pre{background:#0a0f18;padding:8px;border-radius:8px;overflow:auto}</style>")
HELP_HTML = '<div class="panel"><h1>快速上手（五步）</h1>\n<ol>\n<li>确认设备已接好（或直接用"演示模式"，不插设备也能跑）</li>\n<li>在"场景卡片"里点一张卡（比如"国标·噪声干扰"）选中它</li>\n<li>点"开始"——下面实时数据区会滚动显示链路表现</li>\n<li>跑完后到<a href="/reports">报告中心</a>点开这次运行，看曲线和失效电平表</li>\n<li>任何时候出问题，点大红按钮"急停"——干扰立即停止</li>\n</ol>\n<p>提示：历史测试都能在报告中心两两对比；所有数字都来自当次实测，可复现。</p></div>'


def _md_to_html(text: str, run: str | None = None) -> str:
    out, table = [], []
    for ln in text.splitlines():
        if ln.startswith("|"):
            table.append(ln)
            continue
        if table:
            out.append("<pre>" + "\n".join(table) + "</pre>")
            table = []
        if ln.startswith("# "):
            out.append("<h1>" + ln[2:] + "</h1>")
        elif ln.startswith("## "):
            out.append("<h2>" + ln[3:] + "</h2>")
        elif ln.startswith("![") and "](" in ln:
            alt = ln[2:ln.index("]")]
            src = ln[ln.index("](") + 2:-1]
            if run:
                src = "/runs-media/%s/%s" % (run, src)
            out.append("<p><img alt='%s' src='%s'></p>" % (alt, src))
        elif ln.strip():
            out.append("<p>" + ln + "</p>")
    if table:
        out.append("<pre>" + "\n".join(table) + "</pre>")
    return "\n".join(out)


def render_static_pages(app) -> None:
    # 在既有 app 上挂 /reports 与 /help 两页（数据复用 runs/ 目录与既有 API）
    from fastapi.responses import HTMLResponse

    @app.get("/reports", response_class=HTMLResponse)
    def reports_page():
        d = Path("runs")
        names = sorted((p.name for p in d.iterdir() if (p / "report.md").exists()),
                       reverse=True) if d.exists() else []
        items = "\n".join('<li><a href="/reports/%s">%s</a></li>' % (n, n) for n in names) \
            or "<li>（暂无历史测试）</li>"
        return _CSS + '<div class="panel"><h1>报告中心</h1><ul>' + items + "</ul></div>"

    @app.get("/reports/{name}", response_class=HTMLResponse)
    def report_detail(name: str):
        p = Path("runs") / name / "report.md"
        if not p.exists():
            return _CSS + '<div class="panel"><h1>404</h1><p>没有这次运行：%s</p><p><a href="/reports">返回列表</a></p></div>' % name
        return _CSS + '<div class="panel"><a href="/reports">← 返回列表</a></div>' \
            + _md_to_html(p.read_text(encoding="utf-8"), run=name)

    @app.get("/help", response_class=HTMLResponse)
    def help_page():
        return _CSS + HELP_HTML
