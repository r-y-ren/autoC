# R5 顶层：国标步进执行器——装载→步进→判失效→失效电平→产物与报告（责任文档：execute_scenario）
from __future__ import annotations

import csv
import json
import os
import time
from pathlib import Path

from src.build_report.build_report import build_report
from src.collect_dut_samples.collect_dut_samples import collect_dut_samples
from src.create_instrument_backend.create_instrument_backend import create_instrument_backend
from src.execute_scenario.check_failure import check_failure
from src.execute_scenario.plan_steps import plan_steps
from src.shared.estop import EstopManager
from src.shared.load_scenario import load_scenario


def _host_ms() -> int:
    return int(time.monotonic() * 1000)


def execute_scenario(scenario_path, *, estop=None):
    # 返回 {run_dir, outcomes, fail_levels, nojam_false_alarm, report_path}
    sc = load_scenario(scenario_path)
    speed = max(0.1, float(os.environ.get("LINKBENCH_SPEED", "1.0")))
    backend = os.environ.get("LINKBENCH_BACKEND", "mock")
    run_dir = Path("runs") / ("%s-%d" % (sc.name, int(time.time() * 1000)))
    run_dir.mkdir(parents=True, exist_ok=True)

    jammer, analyzer = create_instrument_backend(backend)
    if estop is None:
        estop = EstopManager()
    estop.arm(jammer.off)

    links = [{"type": "fake", "link": n,
              "rate_hz": max(10.0, 40.0 * speed),
              "jammer": jammer} for n in (sc.dut_links or ["wifi"])]

    kpi_rows, events, step_records = [], [], []

    def on_sample(s):
        kpi_rows.append({"ts_ms": _host_ms(), "link": s.link, "seq": s.seq,
                         "per": s.per, "tx_n": s.tx_n, "err_n": s.err_n,
                         "rssi_dbm": s.rssi_dbm, "arc_avg": s.arc_avg,
                         "plos_cnt": s.plos_cnt})

    try:
        if sc.injection is None:
            dur = max(0.2, 1.0 / speed)
            _samples, gaps = collect_dut_samples(links, dur, on_sample=on_sample)
            events.extend(gaps)
            window = kpi_rows
            failed, kind = check_failure(window, sc.criteria)
            nojam_false_alarm = bool(failed)
            step_records.append({"style": "nojam", "power_db": None,
                                 "t_start_ms": 0, "t_end_ms": _host_ms(),
                                 "failed": failed, "failure_kind": kind})
        else:
            nojam_false_alarm = False
            plan = plan_steps(sc.injection)
            for st in plan:
                t0 = _host_ms()
                jammer.set_style(st.style, dict(sc.injection.params or {}))
                jammer.set_power_db(st.power_db)
                jammer.on()
                events.append({"type": "injection", "style": st.style,
                               "power_db": st.power_db, "ts_ms": t0})
                eff = max(0.05, st.duration_s / speed)
                _s, gaps = collect_dut_samples(links, eff, on_sample=on_sample)
                events.extend(gaps)
                jammer.off()
                events.append({"type": "injection_off", "style": st.style,
                               "power_db": st.power_db, "ts_ms": _host_ms()})
                t1 = _host_ms()
                window = [r for r in kpi_rows if t0 <= r["ts_ms"] <= t1]
                failed, kind = check_failure(window, sc.criteria)
                rec = {"style": st.style, "power_db": st.power_db,
                       "t_start_ms": t0, "t_end_ms": t1,
                       "failed": failed, "failure_kind": kind}
                step_records.append(rec)
                if failed:
                    events.append({"type": "fail", "style": st.style,
                                   "power_db": st.power_db, "ts_ms": t1})
                    break  # 该样式已失效，进下一样式
    except Exception:  # noqa: BLE001 —— 任何异常先急停再抛
        estop.fire("execute_scenario 异常")
        raise

    (run_dir / "scenario.yaml").write_text(
        json.dumps({"name": sc.name}, ensure_ascii=False), encoding="utf-8")
    with (run_dir / "kpi.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts_ms", "link", "seq", "per", "tx_n", "err_n",
                    "rssi_dbm", "arc_avg", "plos_cnt"])
        for r in kpi_rows:
            w.writerow([r["ts_ms"], r["link"], r["seq"], r["per"], r["tx_n"],
                        r["err_n"], r["rssi_dbm"], r["arc_avg"], r["plos_cnt"]])
    with (run_dir / "events.jsonl").open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with (run_dir / "steps.jsonl").open("w", encoding="utf-8") as f:
        for st in step_records:
            f.write(json.dumps(st, ensure_ascii=False) + "\n")

    fail_levels = {}
    for st in step_records:
        if st.get("failed") and st.get("power_db") is not None:
            fail_levels.setdefault(st["style"], st["power_db"])
    report = build_report(run_dir)
    return {"run_dir": run_dir, "outcomes": step_records,
            "fail_levels": fail_levels, "nojam_false_alarm": nojam_false_alarm,
            "report_path": report}
