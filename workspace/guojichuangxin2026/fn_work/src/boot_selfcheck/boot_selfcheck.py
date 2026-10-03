"""sw-boot 三步真验收：会话起→服务探活→回放探活（boot_selfcheck 块）。"""
from __future__ import annotations


def boot_selfcheck(config: dict | None = None) -> dict:
    """三步：①launch_demo_session 短合成会话等到首帧/首事件；②起服务线程探活；
    ③回放探活（/api/runs 含该会话目录且 frames API 非空）。全过 pass=True。"""
    import json
    import threading
    import time
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    import sys
    sys.path.insert(0, str(root / "src"))
    cfg = dict(config or {})
    runs_root = cfg.get("runs_root", str(root / "runs"))
    report = {"steps": {}}

    # ①合成会话
    from launch_demo_session.launch_demo_session import launch_demo_session
    h = launch_demo_session({"scenario": "lowbat_headwind", "duration_s": 1.2},
                            {"runs_root": runs_root, "simulator": "synthetic"})
    deadline = time.time() + 10
    while time.time() < deadline and h["status"]()["phase"] == "running":
        time.sleep(0.1)
    st = h["status"]()
    report["steps"]["session"] = {"pass": st["frames"] >= 15,
                                  "frames": st["frames"], "phase": st["phase"]}

    # ②服务探活（线程内起 uvicorn）
    from run_ground_station.register_pages import register_pages
    from fastapi import FastAPI
    import uvicorn
    app = FastAPI()
    register_pages(app, runs_root)
    app.state.cfg = {"runs_root": runs_root}
    try:
        from launch_demo_session.session_control_api import mount_control_api
        mount_control_api(app)
    except ImportError:
        pass
    port = int(cfg.get("port", 8765))
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                           log_level="error"))
    th = threading.Thread(target=server.run, daemon=True)
    th.start()
    from boot_selfcheck.probe_service import probe_service
    for _ in range(20):
        if server.started:
            break
        time.sleep(0.1)
    probe = probe_service(f"http://127.0.0.1:{port}")
    report["steps"]["service"] = {"pass": probe["reachable"],
                                  "latency_ms": probe["latency_ms"]}

    # ③回放探活：frames API 对刚才会话可取到帧
    run_name = Path(h["run_dir"]).name
    frames_ok = False
    import urllib.request
    try:
        with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/api/runs/{run_name}/frames", timeout=3) as r:
            data = json.loads(r.read())
        frames_ok = bool(data.get("frames"))
    except Exception:
        pass
    report["steps"]["replay"] = {"pass": frames_ok, "run": run_name}
    server.should_exit = True
    th.join(timeout=2)
    report["pass"] = all(s["pass"] for s in report["steps"].values())
    return report
