"""演示会话编排：建目录→拉 SITL→装配设备总线+管线→会话句柄（launch_demo_session 块）。"""
from __future__ import annotations

import json
import threading
import time
import uuid


class SessionError(Exception):
    """场景未定义/SITL 拉起失败（含可读原因给 UI）。"""


def launch_demo_session(request: dict, config: dict | None = None):
    """发起一次演示会话；返回句柄 {id, run_dir, status(), inject(level), abort()}。

    装配：设备总线（缺席自动回放）→ 合成/PX4 SITL → run_ingest 线程 →
    渐进/突发/链路管线+状态机 → 事件发布 hub（pipe_events）→ 运行目录归档。
    """
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "src"))
    cfg = dict(config or {})
    scenario = request.get("scenario", "lowbat_headwind")
    duration = float(request.get("duration_s", 8.0))
    runs_root = cfg.get("runs_root", str(root / "runs"))
    hub = cfg.get("hub")                       # 平台 EventHub（缺省隔离运行）

    from launch_demo_session.spawn_sitl import SitlError, spawn_sitl
    from run_device_bus.run_device_bus import run_device_bus
    from run_ground_station.pipe_events import EventHub
    from shared.open_run_dir import open_run_dir

    try:
        sitl = spawn_sitl({"name": scenario}, cfg.get("simulator", "synthetic"))
    except SitlError as exc:
        raise SessionError(f"SITL 拉起失败: {exc}") from exc
    bus = run_device_bus(cfg.get("modules", [{"name": "sdr", "type": "usrp"}]))
    hub = hub if isinstance(hub, EventHub) else EventHub()
    sid = uuid.uuid4().hex[:8]
    run_dir = open_run_dir(runs_root, scenario, seed=abs(hash(sid)) % 10_000,
                           config_snapshot={"scenario": scenario, "duration_s": duration})
    st = {"phase": "running", "state": "S0", "advice": None, "frames": 0,
          "source": {"spectrum": bus.source_mode.get("sdr", "replay")}}
    stop = threading.Event()

    def _emit(topic, payload):
        try:
            hub.publish_sync(topic, payload)
        except Exception:
            pass

    def _work():
        from run_ingest.run_ingest import run_ingest
        from run_link_consistency.run_link_consistency import run_link_consistency
        from run_progressive_risk.run_progressive_risk import run_progressive_risk
        from run_safety_state_machine.run_safety_state_machine import run_safety_state_machine
        from run_sudden_fault.run_sudden_fault import run_sudden_fault
        try:
            import itertools
            icfg = {"run": {"hz": 20, "duration_s": duration, "home": [32.0, 118.8],
                            "endpoint": "inproc"}}
            # tee 五路：接入流被 链路/渐进/突发/余量/主循环 各自独立迭代同一序列
            f_link, f_risk, f_mgn, f_sud, f_main = itertools.tee(
                run_ingest(icfg, run_dir, conn=sitl["conn"]), 5)
            evs, margins = [], []
            link = run_link_consistency(f_link)
            risk = run_progressive_risk(f_risk, (f["margins"] for f in f_mgn), None)
            sudden = run_sudden_fault(f_sud)
            sm = run_safety_state_machine(evs, margins, {
                "position": (32.0, 118.8), "home": (32.001, 118.8),
                "battery_remaining": 80, "gps_ok": True, "link_ok": True,
                "alternates": []})
            from shared.append_record import append_record
            for f in f_main:
                if stop.is_set():
                    break
                margins.append(f["margins"])
                st["frames"] += 1
                st["state"] = f.get("quality_mask") and st["state"]
                le = next(link, None)
                pe = next(risk, None)
                se = next(sudden, None)
                for ev in filter(None, (pe, se)):
                    evs.append(ev)
                    append_record(run_dir, "event", ev)
                    _emit("event", {"event": f"[{ev.get('type')}] "
                                             f"{ev.get('fault') or ''} sev={ev.get('severity', 0)} "
                                             f"t={ev.get('t')}"})
                out = next(sm)
                if out["state"] != st["state"] or out["advice"]:
                    st["state"], st["advice"] = out["state"], out["advice"]
                    _emit("event", {"state": out["state"],
                                    "advice": out["advice"]})
                    append_record(run_dir, "event", {"type": "state",
                                                     "state": out["state"],
                                                     "advice": out["advice"], "t": f["t"]})
            st["phase"] = "done"
        except Exception as exc:              # 会话级失败不炸平台
            st["phase"] = f"error: {exc}"
        finally:
            bus.close()

    th = threading.Thread(target=_work, daemon=True)
    th.start()

    def inject(level):
        from shared.inject_scenario_fault import InjectError, inject_scenario_fault
        try:
            r = inject_scenario_fault(sitl["conn"], scenario, level,
                                      {"phase": "in-flight", "at_s": None})
            return {"ok": True, **r}
        except InjectError as exc:
            return {"ok": False, "error": str(exc)}

    def status():
        return dict(st)

    def abort():
        stop.set()
        st["phase"] = "aborted"
        return st["phase"]

    return {"id": sid, "run_dir": str(run_dir), "status": status,
            "inject": inject, "abort": abort, "thread": th}
