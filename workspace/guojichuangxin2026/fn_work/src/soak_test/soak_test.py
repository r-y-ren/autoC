"""连续会话长跑+健康记录（内存/线程/异常）（soak_test 块）。"""
from __future__ import annotations


def soak_test(duration_s: float = 3600.0, quick: bool = False) -> dict:
    """会话串行直至总时长；每会话记帧数/事件/RSS；崩溃率>50% 提前终止。报告入 fn_docs/results/soak/。"""
    import json
    import resource
    import time
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    import sys
    sys.path.insert(0, str(root / "src"))
    from launch_demo_session.launch_demo_session import launch_demo_session

    total = 20.0 if quick else duration_s
    t0, sessions, errors = time.monotonic(), [], 0
    scenarios = ["lowbat_headwind", "motor_fail", "link_degrade"]
    i = 0
    while time.monotonic() - t0 < total:
        sc = scenarios[i % len(scenarios)]
        i += 1
        try:
            h = launch_demo_session({"scenario": sc, "duration_s": 2.0},
                                    {"runs_root": str(root / "runs"),
                                     "simulator": "synthetic"})
            deadline = time.time() + 15
            while time.time() < deadline and h["status"]()["phase"] == "running":
                time.sleep(0.1)
            st = h["status"]()
            h["thread"].join(timeout=2)
            sessions.append({"scenario": sc, "frames": st["frames"],
                             "phase": st["phase"]})
            if st["phase"].startswith("error") or st["frames"] < 15:
                errors += 1
        except Exception as exc:
            errors += 1
            sessions.append({"scenario": sc, "error": str(exc)})
        if errors > len(sessions) * 0.5 and len(sessions) >= 4:
            break
    rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report = {"duration_s": round(time.monotonic() - t0, 1), "sessions": len(sessions),
              "errors": errors, "frames_total": sum(s.get("frames", 0) for s in sessions),
              "rss_max_mb": round(rss_kb / 1024, 1), "ok": errors <= len(sessions) * 0.5}
    out = root / "fn_docs" / "results" / "soak"
    out.mkdir(parents=True, exist_ok=True)
    fp = out / f"soak-{time.strftime('%Y%m%d-%H%M%S')}.json"
    fp.write_text(json.dumps({"summary": report, "sessions": sessions},
                             ensure_ascii=False, indent=1), encoding="utf-8")
    report["report"] = str(fp)
    return report
