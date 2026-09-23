"""verify_layer_s_gates（R10/S3 L0）：四门编排与总台账（verify_summary.json）。

责任契约：
- verify(pkg_path, episodes_manifest) -> {overall, h2h, lineage, equivalence,
  launch, evidence_dir, started, finished}；CLI
  `python verify_layer_s_gates.py <pkg_dir> [episodes_dir]`（exit 0=四门全绿，
  1=红，2=用法错）。episodes_manifest 即 strip 语料目录（门③入参），缺省由本
  文件位置相对推导（与 gate_equivalence_precision._STRIP_DIR_DEFAULT 同一条
  相对路径，不手拼绝对路径）。
- 编排：门① h2h（缺省 8 seeds×双席位=16 局）→ 门② lineage（三对手×8 局）→
  门③ equivalence（seated 重演+子集判据+构造用例）→ 门④ launch（发射四门+
  附加断言）；**全跑不短路**——任一门红也继续跑完其余三门（台账要完整）。
- fail-closed：任一门不可执行（抛异常；如门②对手 main 路径 sha 断裂，门②
  自己装载即抛 GateLineageError）→ 该门记 {executed=False, error=…,
  passed=False}，整体必红，但其余门照跑。
- overall = 四门 passed 全 True（不可执行门的 passed=False 计入）。
- 台账：四门各自写 evidence/ 四件套（h2h/lineage/equivalence/launch
  *_evidence.json，由各门自写）；本编排在其上再写 evidence/verify_summary.json
  ——含各门 passed（gates_passed 显式映射 + 各门 entry）与 overall 判决、
  环境戳（python 版本/起止时间/L1 与 verbatim 两 main 的 sha256）。
- 路径推导：L1 main = <pkg>/main.py；verbatim main、三对手 main、语料缺省
  目录均由本文件位置（HERE/KSIM）相对推导，不手拼绝对路径。
- 汇总条目保持轻量（per_game/逐差步明细留在各门自己的 evidence 件里，
  verify_summary 只留裁决面：h2h 五数、lineage 每对手五数、equivalence
  equiv/subset/cases、launch 四门+差异步集合）。
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time

import gate_equivalence_precision
import gate_h2h_vs_verbatim
import gate_launch_fourgate_l1
import gate_lineage_strength

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                    # kaggle_simulations/
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative", "main.py")
OPPONENTS = {
    "v48-pure": os.path.join(KSIM, "opponents", "v48_main.py"),
    "v4b": os.path.join(KSIM, "v48_hybrid", "v4b", "main.py"),
    "hybrid-v2": os.path.join(KSIM, "v48_hybrid", "main.py"),
}
# strip 语料缺省目录：HERE 上溯四级到战役根再入 fn_docs（相对推导，勿手拼）。
EPISODES_DIR_DEFAULT = os.path.normpath(os.path.join(
    HERE, os.pardir, os.pardir, os.pardir, os.pardir,
    "fn_docs", "hybrid", "results", "replays-r30-26"))
SUMMARY_NAME = "verify_summary.json"
USAGE = "usage: python verify_layer_s_gates.py <pkg_dir> [episodes_dir]"

_H2H_KEYS = ("n", "wins", "losses", "ties", "rate")
_LINEAGE_KEYS = ("n", "wins", "losses", "ties", "all_done")
_GATE_ORDER = ("h2h", "lineage", "equivalence", "launch")


def _stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _sha256_of(path: str) -> str:
    """文件 sha256（环境戳用）；读失败记 error 串（不向上抛，戳面不拦裁决）。"""
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError as exc:
        return f"error: {type(exc).__name__}: {exc}"


def _run_gate(label: str, thunk):
    """跑一门：返回 (entry, result)。异常/SystemExit → {executed=False,
    passed=False, error}（fail-closed），result=None；正常 → entry 留 passed/
    wall_s，result 供调用方补充裁决面字段。"""
    t0 = time.perf_counter()
    print(f"[verify] {label} running ...", flush=True)
    try:
        result = thunk()
    except (Exception, SystemExit) as exc:  # 不可执行=门红，不拦其余门
        entry = {"passed": False, "executed": False,
                 "error": f"{type(exc).__name__}: {exc}",
                 "wall_s": round(time.perf_counter() - t0, 1)}
        print(f"[verify] {label} NOT EXECUTABLE (fail-closed): "
              f"{entry['error']}", flush=True)
        return entry, None
    entry = {"passed": bool(result.get("passed")), "executed": True,
             "error": None, "wall_s": round(time.perf_counter() - t0, 1)}
    print(f"[verify] {label} {'PASS' if entry['passed'] else 'FAIL'} "
          f"({entry['wall_s']}s)", flush=True)
    return entry, result


def verify(pkg_path=None, episodes_manifest=None) -> dict:
    """顺序全跑四门①②③④→{overall, h2h, lineage, equivalence, launch,
    evidence_dir, started, finished}；写 evidence/verify_summary.json。

    pkg_path 缺省本目录（HERE）；episodes_manifest 即门③语料目录，缺省
    EPISODES_DIR_DEFAULT（相对推导）。任一门不可执行=整体 fail（fail-closed）
    但继续尝试其余门——四门 entry 全部落台账。
    """
    started = _stamp()
    pkg_path = os.path.abspath(pkg_path) if pkg_path is not None else HERE
    episodes_dir = (os.path.abspath(episodes_manifest)
                    if episodes_manifest else EPISODES_DIR_DEFAULT)
    l1_main = os.path.join(pkg_path, "main.py")
    evidence_dir = os.path.join(pkg_path, "evidence")

    # 门① h2h vs verbatim（缺省 16 局：8 seeds×双席位）。
    h2h, res = _run_gate(
        "gate1 h2h vs verbatim",
        lambda: gate_h2h_vs_verbatim.run(l1_main, VERBATIM_MAIN, seeds=None))
    if res is not None:
        h2h.update({key: res.get(key) for key in _H2H_KEYS})
        h2h["evidence_path"] = res.get("evidence_path")

    # 门② lineage strength（v48-pure/v4b/hybrid-v2 各 8 局；对手路径 sha 断裂
    # → 门内装载即抛 GateLineageError → 上面的 fail-closed 记不可执行）。
    lineage, res = _run_gate(
        "gate2 lineage strength",
        lambda: gate_lineage_strength.run(l1_main, OPPONENTS,
                                          per_opponent_n=8))
    if res is not None:
        lineage["per_opponent"] = {
            str(name): {key: (summ or {}).get(key) for key in _LINEAGE_KEYS}
            for name, summ in (res.get("per_opponent") or {}).items()}
        lineage["evidence_path"] = res.get("evidence_path")

    # 门③ equivalence + precision（seated 重演逐字节 + 子集判据 + 构造用例）。
    equivalence, res = _run_gate(
        "gate3 equivalence precision",
        lambda: gate_equivalence_precision.run(episodes_dir, l1_main,
                                               VERBATIM_MAIN))
    if res is not None:
        for key in ("equiv", "subset", "cases"):
            equivalence[key] = res.get(key)
        equivalence["evidence_path"] = res.get("evidence_path")

    # 门④ launch fourgate（发射四门 + truncation-only 附加断言）。
    launch, res = _run_gate(
        "gate4 launch fourgate",
        lambda: gate_launch_fourgate_l1.run(pkg_path))
    if res is not None:
        launch["gates"] = res.get("gates")
        steps = (res.get("truncation_only_diff") or {}).get(
            "divergent_steps") or []
        launch["truncation_only_diff"] = {
            "ok": (res.get("truncation_only_diff") or {}).get("ok"),
            "n_divergent": len(steps),
            "min_divergent_step": min(steps) if steps else None,
            "divergent_steps": steps}
        launch["evidence_path"] = res.get("evidence_path")

    gates = {"h2h": h2h, "lineage": lineage,
             "equivalence": equivalence, "launch": launch}
    overall = all(gates[name]["passed"] for name in _GATE_ORDER)
    finished = _stamp()

    result = {"overall": overall, "h2h": h2h, "lineage": lineage,
              "equivalence": equivalence, "launch": launch,
              "evidence_dir": evidence_dir, "started": started,
              "finished": finished}

    os.makedirs(evidence_dir, exist_ok=True)
    summary = dict(result)
    summary.update({
        "protocol": "verify-layer-s-gates/1.0",
        "pkg_path": pkg_path,
        "episodes_dir": episodes_dir,
        "gates_passed": {name: gates[name]["passed"] for name in _GATE_ORDER},
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "python_full": sys.version,
        },
        "mains": {
            "l1_main": l1_main,
            "verbatim_main": VERBATIM_MAIN,
            "sha256": {
                "l1_main": _sha256_of(l1_main),
                "verbatim_main": _sha256_of(VERBATIM_MAIN),
            },
        },
    })
    summary_path = os.path.join(evidence_dir, SUMMARY_NAME)
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"[verify] overall={'PASS' if overall else 'FAIL'} "
          f"summary -> {summary_path}", flush=True)
    return result


def main(argv=None) -> int:
    """CLI：exit 0=四门全绿；1=红；2=用法错（参数个数 1-2：pkg_dir [episodes_dir]）。"""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not 1 <= len(argv) <= 2:
        print(USAGE, file=sys.stderr)
        return 2
    result = verify(argv[0], argv[1] if len(argv) > 1 else None)
    print(f"overall = {result['overall']}")
    print(f"evidence_dir = {result['evidence_dir']}")
    return 0 if result["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
