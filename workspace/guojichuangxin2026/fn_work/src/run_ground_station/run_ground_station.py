"""平台主入口：组装 app+起 uvicorn 服务（阻塞）（run_ground_station 块）。"""
from __future__ import annotations


def run_ground_station(config: dict, live_source=None):
    """config: {port, runs_root}；live_source 可选（EventHub 装配，控制台会话用）。"""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import uvicorn
    from fastapi import FastAPI

    from run_ground_station.pipe_events import EventHub
    from run_ground_station.register_pages import register_pages

    app = FastAPI(title="安航云盾地面管理平台")
    register_pages(app, config.get("runs_root", "runs"))
    app.state.hub = live_source if isinstance(live_source, EventHub) else EventHub()
    # 会话控制端点（R9）挂载
    try:
        from launch_demo_session.session_control_api import mount_control_api
        mount_control_api(app)
    except ImportError:
        pass                                    # B10 前后兼容：控制台端点后挂
    port = int(config.get("port", 8000))
    try:
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
    except OSError as exc:
        raise SystemExit(f"端口占用？{port}: {exc}") from exc
    return 0
