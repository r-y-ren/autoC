# -*- coding: utf-8 -*-
"""run_r35_iteration（R17 L0）：编排——Phase V 三判决→build_r35→
verify_r35_gates→launch_ready；evidence 三件+门禁台账。

CLI：`python run_r35.py [--skip-phase-v evidence/phase_v_summary.json]`
（--skip-phase-V 接既有 Phase V 汇总 JSON，复用其并入清单直接进入构建——
两段式实跑用：先跑 phase_v（重演耗时），后接构建+门禁）。
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

from orderbook_r35 import build_r35 as _b35      # noqa: E402
from orderbook_r35 import gates_r35 as _g35      # noqa: E402
from orderbook_r35 import phase_v as _pv         # noqa: E402


def run_r35_iteration(phase_v_summary: Optional[Dict[str, Any]] = None,
                      out_dir: Optional[str] = None) -> Dict[str, Any]:
    """编排：Phase V 三判决 → build_r35 → verify_r35_gates → launch_ready。

    phase_v_summary 给定=复用既有判决（两段式实跑）；缺省现场跑
    phase_v_adjudicate。任一段 fail-closed 抛异常时仍落 run_summary
    （阶段态记录）后向上抛。
    """
    t0 = time.perf_counter()
    out_dir = out_dir or HERE
    stage = {"phase_v": None, "build": None, "gates": None}
    try:
        if phase_v_summary is None:
            phase_v_summary = _pv.phase_v_adjudicate()
        stage["phase_v"] = {
            "adopted": {k: bool(phase_v_summary.get(k, {}).get("adopt"))
                        for k in ("sheep", "tomato", "route")},
            "errors": phase_v_summary.get("errors"),
            "evidence_path": phase_v_summary.get("evidence_path"),
        }
        build = _b35.build_r35(phase_v_summary, _b35.R34A_MAIN, out_dir)
        stage["build"] = {k: build[k] for k in
                          ("ok", "adopted", "main_sha256", "main_bytes",
                           "tar_sha256", "tar_bytes", "diff_attribution")}
        gates = _g35.verify_r35_gates(out_dir)
        stage["gates"] = {
            "overall": gates["overall"],
            "gates_passed": gates["gates_passed"],
        }
        summary = {
            "protocol": "run-r35/1.0",
            "stage": stage,
            "launch_ready": bool(gates["overall"]),
            "wall_s": round(time.perf_counter() - t0, 1),
        }
        path = os.path.join(out_dir, "evidence", "run_summary.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        summary["run_summary_path"] = path
        return summary
    except Exception as exc:
        fail = {"protocol": "run-r35/1.0", "stage": stage,
                "launch_ready": False,
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        path = os.path.join(out_dir, "evidence", "run_summary.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(fail, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        raise


def main(argv=None, out_dir=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    summary_in = None
    if argv:
        if argv[0] != "--skip-phase-v" or len(argv) != 2:
            print("usage: python run_r35.py [--skip-phase-v <phase_v_summary.json>]",
                  file=sys.stderr)
            return 2
        with open(argv[1], "r", encoding="utf-8") as fh:
            summary_in = json.load(fh)
    result = run_r35_iteration(summary_in, out_dir=out_dir)
    print(json.dumps({k: result[k] for k in ("stage", "launch_ready", "wall_s")},
                     ensure_ascii=False, indent=1))
    return 0 if result["launch_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
