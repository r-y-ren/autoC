"""批量评估执行器（R2/R3/R4 验收命令本体）（shared 块）。"""
from __future__ import annotations

import json
import statistics as stats


def _percentile(xs, q):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def _crit_frame(frame, scenario):
    """失控判据（提前量的尺子，requirements 术语表）：
    lowbat_headwind=battery_remaining<25；motor_fail=|roll|>0.3；link_degrade=rssi>-70 持续（失联代理）。"""
    if scenario == "lowbat_headwind":
        b = frame.get("battery_remaining")
        return b is not None and b < 25
    if scenario == "motor_fail":
        r = frame.get("roll")
        return r is not None and abs(r) > 0.3
    if scenario == "link_degrade":
        r = frame.get("rssi")
        return r is not None and r > -70      # 欺骗态强信号（失联代理判据）
    return False


def _lead_metrics(frames, evs, scenario):
    t_crit = next((float(f["t"]) for f in frames if _crit_frame(f, scenario)), None)
    sev = [e for e in evs if e.get("type") == "progressive"
           and int(e.get("severity", 0)) >= 1] or \
          [e for e in evs if e.get("type") in ("progressive", "sudden")]
    if t_crit is None or not sev:
        return {"lead_p10_s": None, "lead_median_s": None, "lead_hit_rate": None,
                "t_crit": t_crit, "note": "无判据触发或无预警事件"}
    leads = [max(0.0, t_crit - float(e["t"])) for e in sev
             if float(e["t"]) <= t_crit]
    if not leads:
        return {"lead_p10_s": None, "lead_median_s": None, "lead_hit_rate": 0.0,
                "t_crit": t_crit}
    return {"lead_p10_s": round(_percentile(leads, 0.10), 3),
            "lead_median_s": round(stats.median(leads), 3),
            "lead_hit_rate": round(sum(1 for x in leads if x >= 5.0) / len(leads), 3),
            "t_crit": t_crit, "n_events": len(leads)}


def run_eval(scenario: str, runs: int, seeds=None, config: dict | None = None):
    """批量评估：合成/PX4 会话→管线→按失控判据计时→指标入 metrics 分片。

    只写运行目录分片；不写战役顶层 metrics.json（merge_metrics 领地）。
    """
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "src"))

    from launch_demo_session.spawn_sitl import SyntheticSITL
    from run_ingest.replay_check import replay_check
    from run_ingest.run_ingest import run_ingest
    from run_link_consistency.run_link_consistency import run_link_consistency
    from run_progressive_risk.check_physical_baseline import check_physical_baseline
    from run_progressive_risk.run_progressive_risk import run_progressive_risk
    from run_safety_state_machine.run_safety_state_machine import run_safety_state_machine
    from run_sudden_fault.run_sudden_fault import run_sudden_fault
    from shared.append_record import append_record
    from shared.open_run_dir import open_run_dir

    if scenario not in SyntheticSITL.scenario_defs:
        raise SystemExit(f"场景未定义: {scenario}")
    cfg = dict(config or {})
    runs_root = cfg.get("runs_root", str(root / "runs"))
    all_metrics = {}
    for i in range(runs):
        seed = (seeds[i] if seeds and i < len(seeds) else 1000 + i)
        rd = open_run_dir(runs_root, f"{scenario}_eval", seed=seed)
        sitl = SyntheticSITL(scenario)
        sitl.inject_scenario(scenario, "mid", {})          # 评估口径：中档强度
        icfg = {"run": {"hz": 20, "duration_s": 12.0, "home": [32.0, 118.8],
                        "endpoint": "inproc"}}
        import itertools
        f_link, f_risk, f_mgn, f_sud, f_main = itertools.tee(
            run_ingest(icfg, rd, conn=sitl), 5)
        evs, frames_kept = [], []
        risk = run_progressive_risk(f_risk, (f["margins"] for f in f_mgn), None)
        sudden = run_sudden_fault(f_sud)
        link = run_link_consistency(f_link)
        sm = run_safety_state_machine(evs, [], {
            "position": (32.0, 118.8), "home": (32.001, 118.8),
            "battery_remaining": 80, "gps_ok": True, "link_ok": True, "alternates": []})
        for f in f_main:
            frames_kept.append(f)
            for ev in filter(None, (next(risk, None), next(sudden, None))):
                evs.append(ev)
                append_record(rd, "event", ev)
            out = next(sm)
            append_record(rd, "event", {"type": "state", "state": out["state"], "t": f["t"]})
            next(link, None)
        # 指标
        m = _lead_metrics(frames_kept, evs, scenario)
        sudden_evs = [e for e in evs if e.get("type") == "sudden"]
        m["confirm_p90_s"] = round(_percentile(
            [e["latency_s"] for e in sudden_evs if "latency_s" in e], 0.90), 3) \
            if sudden_evs and any(e.get("latency_s") is not None for e in sudden_evs) else None
        m["type_correct"] = sum(1 for e in sudden_evs
                                if e.get("fault") in ("电机异常", "电调异常", "链路瞬断"))
        m["type_total"] = len(sudden_evs)
        m["frames"] = len(frames_kept)
        m["replay_ok"] = replay_check(str(rd)) == 0
        for k, v in m.items():
            append_record(rd, "metric", {"key": f"{scenario}/{k}", "value": v,
                                         "note": "synthetic-mid"})
        for k, v in m.items():
            all_metrics.setdefault(k, []).append(v)
    summary = {"scenario": scenario, "runs": runs, "source": "synthetic-mid",
               "summary": {k: (round(stats.median(v), 3) if isinstance(v[0], (int, float))
                               and v[0] is not None else v[-1])
                           for k, v in all_metrics.items() if None not in v}}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return summary


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(prog="run_eval")
    p.add_argument("--scenario", required=True)
    p.add_argument("--runs", type=int, default=30)
    p.add_argument("--seeds", default=None)
    a = p.parse_args()
    raise SystemExit(0 if run_eval(a.scenario, a.runs) else 1)
