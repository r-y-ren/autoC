"""assemble_and_gate（L0，R6）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

编排：build_candidate_package（换库字节重打包 v48 外壳）→
run_m1_m2_gates（M1 互胜 ≥0.45 + M2 五线）→ 裁决报告。

错误语义（R6）：任一门红**如实分档不抛**——
* PIPELINE_BROKEN：构建失败或门线不可执行（管线不成）；
* BELOW_LINE：管线跑通但门线未到（M1<0.45 或 M2 五线任一 FAIL）；
* GATES_PASS：全过。
门禁只读既有 search/final_selection.json 与 library/（T2/T3 链上件）；
产物落 fn_work/tape_gen/candidate/。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parents[1])
if _SRC_ROOT not in sys.path:            # 脚本直跑（pytest 经 conftest 已加）
    sys.path.insert(0, _SRC_ROOT)

from assemble_and_gate.build_candidate_package import (
    DEFAULT_OUTPUT_DIR as DEFAULT_CANDIDATE_DIR,
    PackageError,
    build_candidate_package,
)
from assemble_and_gate.run_m1_m2_gates import run_m1_m2_gates

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_GATE_REPORT = DEFAULT_CANDIDATE_DIR / "gates" / "m1m2_report.json"


def assemble_and_gate(payload=None):
    """意图级签名；真值在责任文档。

    payload 透传 build_candidate_package / run_m1_m2_gates（builders/
    runners 可注入供测试）；返回 {package, gates, grading, paths}。
    构建异常 → grading.overall=PIPELINE_BROKEN（错误入档，不抛）。
    """
    payload = dict(payload or {})
    builders = payload.get("builders") or {}
    gates_runners = payload.get("runners")

    package_manifest = None
    gates = None
    errors = []

    try:
        if "build_candidate_package" in builders:
            package_manifest = builders["build_candidate_package"](payload)
        else:
            package_manifest = build_candidate_package(payload)
    except (PackageError, ValueError, OSError) as exc:
        errors.append(f"build_candidate_package: {type(exc).__name__}: "
                      f"{exc}")

    if package_manifest is not None:
        gate_payload = dict(payload)
        gate_payload["package_main"] = package_manifest["paths"]["main"]
        gate_payload["package_tar"] = package_manifest["paths"]["tar"]
        # 门禁产物默认落 <候选包目录>/gates（payload 显式指定则从之）
        gate_payload["output_dir"] = payload.get("gates_output_dir") or \
            str(Path(package_manifest["paths"]["output_dir"]) / "gates")
        if gates_runners is not None:
            gate_payload["runners"] = gates_runners
        try:
            gates = run_m1_m2_gates(gate_payload)
        except Exception as exc:                    # noqa: BLE001
            errors.append(f"run_m1_m2_gates: {type(exc).__name__}: {exc}")

    if package_manifest is None or gates is None:
        grading = {"overall": "PIPELINE_BROKEN", "errors": errors}
    else:
        grading = dict(gates["grading"])

    result = {
        "package": (None if package_manifest is None else {
            k: package_manifest[k] for k in
            ("package_id", "base", "surgical_face", "library",
             "selection", "products", "paths")}),
        "gates": gates,
        "grading": grading,
        "paths": {
            "candidate_dir": str(payload.get("output_dir")
                                 or DEFAULT_CANDIDATE_DIR),
            "gate_report": str(payload.get("gate_report")
                               or DEFAULT_GATE_REPORT),
        },
    }
    if errors and "errors" not in result["grading"]:
        result["grading"] = dict(result["grading"], errors=errors)
    return result


def _cli() -> int:
    result = assemble_and_gate()
    print(json.dumps({"grading": result["grading"],
                      "package": None if result["package"] is None else
                      result["package"]["products"]},
                     ensure_ascii=False, indent=1))
    return 0 if result["grading"]["overall"] == "GATES_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(_cli())
