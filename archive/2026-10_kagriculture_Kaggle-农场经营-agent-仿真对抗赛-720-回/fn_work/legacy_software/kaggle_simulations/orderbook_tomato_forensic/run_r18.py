# -*- coding: utf-8 -*-
"""run_r18_iteration（R18 L0）：编排——Phase T 两件法证→cxtb 条件判决→
r36 条件构建→五门禁→出口三预绑定裁决（KILLED_T/NEGATIVE/POSITIVE）。

出口预绑定（requirements R18）：
- cxtb face 不活 且 麦簇全负 → KILLED_T（真凶面不在我方可优化谱系）；
- face 活或麦簇有点，但判决无胜点/构建门禁 FAIL → NEGATIVE（收档）；
- r36 构建且五门 overall=PASS → POSITIVE（launch_ready，交 S4 发射）。

CLI：`python run_r18.py [--skip-forensics <phase_t_summary.json>]`（两段式
实跑：法证重演耗时，可先跑法证后接判决/构建/门禁）。
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

from orderbook_tomato_forensic import build_r36 as _b36   # noqa: E402
from orderbook_tomato_forensic import forensic as _fx     # noqa: E402
from orderbook_tomato_forensic import gates_r36 as _g36   # noqa: E402

EVIDENCE_DIR = os.path.join(HERE, "evidence")


def _write_json(path: str, payload: Any) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def _adopt_manifest(cxtb: Dict[str, Any], wheat: Dict[str, Any]) -> Dict[str, Any]:
    stepped = (cxtb or {}).get("params_stepped")
    consts = (cxtb or {}).get("params_constants")
    return {
        "cxtb_stepped": {"adopt": bool((cxtb or {}).get("adopt_stepped")
                                       and stepped), **(stepped or {})},
        "cxtb_constants": {"adopt": bool((cxtb or {}).get("adopt_constants")
                                         and consts), **(consts or {})},
        "wheat_threshold": {"adopt": bool((wheat or {}).get("adopt")),
                            "threshold": (wheat or {}).get("threshold")},
    }


def _decide_verdict(face_alive: bool, adoptable: bool, built: bool,
                    gates_overall: Optional[bool]) -> Dict[str, Any]:
    if not built:
        if not face_alive:
            verdict = "KILLED_T"
            reason = "cxtb face 不活 + 无可并入项（两面惰性，额度保留）"
        else:
            verdict = "NEGATIVE"
            reason = "判决无胜点（两面惰性/判决负，额度保留）"
        return {"verdict": verdict, "launch_ready": False, "reason": reason}
    if gates_overall:
        return {"verdict": "POSITIVE", "launch_ready": True,
                "reason": "r36 构建且五门全绿（standing 发射前置达成）"}
    return {"verdict": "NEGATIVE", "launch_ready": False,
            "reason": "r36 构建但门禁 FAIL（不发射，额度保留）"}


def run_r18_iteration(phase_t_summary: Optional[Dict[str, Any]] = None,
                      out_dir: Optional[str] = None) -> Dict[str, Any]:
    """编排：法证两件→判决→条件构建→门禁→出口裁决；evidence 全落 run_summary。

    phase_t_summary 给定=复用既有法证结果（两段式实跑）；缺省现场跑。
    任一段 fail-closed 抛异常时仍落 run_summary（阶段态记录）后向上抛。
    """
    t0 = time.perf_counter()
    out_dir = out_dir or HERE
    stage: Dict[str, Any] = {"phase_t": None, "adjudication": None,
                             "build": None, "gates": None}
    try:
        if phase_t_summary is None:
            cxtb = _fx.forensic_cxtb_trigger()
            wheat = _fx.scan_wheat_step91()
            phase_t_summary = {"cxtb": cxtb, "wheat": wheat}
        else:
            cxtb = phase_t_summary["cxtb"]
            wheat = phase_t_summary["wheat"]
        stage["phase_t"] = {
            "face_alive": bool(cxtb.get("face_alive")),
            "fire_rate": cxtb.get("fire_rate"),
            "wheat_adopt": bool(wheat.get("adopt")),
            "wheat_best": wheat.get("best"),
            "evidence": [cxtb.get("evidence_path"), wheat.get("evidence_path")],
        }
        _write_json(os.path.join(EVIDENCE_DIR, "phase_t_summary.json"),
                    phase_t_summary)

        adjud = _fx.adjudicate_cxtb_variants(
            face_alive=bool(cxtb.get("face_alive")), forensic_result=cxtb)
        stage["adjudication"] = {
            "skipped": adjud.get("skipped"),
            "adopt_stepped": bool(adjud.get("adopt_stepped")),
            "adopt_constants": bool(adjud.get("adopt_constants")),
            "params": {k: adjud.get(k) for k in
                       ("params_stepped", "params_constants")},
            "evidence": adjud.get("evidence_path"),
        }

        manifest = _adopt_manifest(adjud, wheat)
        adoptable = any((manifest[k] or {}).get("adopt") for k in
                        ("cxtb_stepped", "cxtb_constants", "wheat_threshold"))
        built, gates = False, None
        if adoptable:
            build = _b36.build_r36_conditional(manifest, _b36.R34A_MAIN, out_dir)
            built = bool(build.get("ok"))
            stage["build"] = {k: build[k] for k in
                              ("ok", "adopted", "main_sha256", "main_bytes",
                               "tar_sha256", "tar_bytes", "last_callable",
                               "diff_attribution")}
            if built:
                gates = _g36.verify_r36_gates(out_dir)
                stage["gates"] = {"overall": gates["overall"],
                                  "gates_passed": gates["gates_passed"]}

        verdict = _decide_verdict(bool(cxtb.get("face_alive")), adoptable,
                                  built, (gates or {}).get("overall"))
        summary = {
            "protocol": "run-r18/1.0",
            "stage": stage,
            "adopt_manifest": manifest,
            **verdict,
            "wall_s": round(time.perf_counter() - t0, 1),
        }
        path = _write_json(os.path.join(out_dir, "evidence", "run_summary.json"),
                           summary)
        summary["run_summary_path"] = path
        return summary
    except Exception as exc:
        fail = {"protocol": "run-r18/1.0", "stage": stage,
                "verdict": "NEGATIVE", "launch_ready": False,
                "error": f"{type(exc).__name__}: {exc}",
                "wall_s": round(time.perf_counter() - t0, 1)}
        _write_json(os.path.join(out_dir, "evidence", "run_summary.json"), fail)
        raise


def main(argv=None, out_dir=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    summary_in = None
    if argv:
        if argv[0] != "--skip-forensics" or len(argv) != 2:
            print("usage: python run_r18.py [--skip-forensics <phase_t_summary.json>]",
                  file=sys.stderr)
            return 2
        with open(argv[1], "r", encoding="utf-8") as fh:
            summary_in = json.load(fh)
    result = run_r18_iteration(summary_in, out_dir=out_dir)
    print(json.dumps({k: result.get(k) for k in
                      ("stage", "verdict", "launch_ready", "wall_s")},
                     ensure_ascii=False, indent=1))
    return 0 if result["launch_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
