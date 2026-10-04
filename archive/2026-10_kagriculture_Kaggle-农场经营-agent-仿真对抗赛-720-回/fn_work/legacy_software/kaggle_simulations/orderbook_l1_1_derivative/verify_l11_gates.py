"""verify_l11_gates（R11 L0）：四门编排与总台账（verify_summary.json）。

责任契约（沿 L1 verify_layer_s_gates 形制，门②④复用 L1 实现重定向）：
- verify(pkg_path, episodes_dir) -> {overall, h2h, lineage, equivalence, launch,
  evidence_dir, started, finished}；CLI `python verify_l11_gates.py <pkg_dir>
  [episodes_dir]`（exit 0=四门全绿，1=红，2=用法错）。
- 门① gate_h2h_vs_l1（本包）：v2 vs L1 16 局互胜 ≥0.55 + vs verbatim 8 局
  参考面（不进门）；
- 门② gate_lineage_strength（**L1 复用**）：v2 对三对手各 8 局无翻负——L1 门
  无 evidence_path 参数（落点为 L1 包内模块级常量），编排以 try/finally 临时
  改指本包 evidence/lineage_evidence.json 并还原，防复用跑批覆写 L1 包真台账；
- 门③ gate_equivalence_v2（本包）：两路重演三面裁决（appear≤2/逐局 ≥L1/
  死种≤$900/子集重验/五件构造用例）；
- 门④ gate_launch_fourgate_l1（**L1 复用**）：发射四门+截断附加断言，pkg_path
  换包复用（v2 末 callable 同名 _cxs_agent）。
- 全跑不短路：任一门红也继续跑完其余门；任一门不可执行（抛异常）→ 该门记
  {executed=False, error, passed=False}，整体必红，其余门照跑（fail-closed）。
- overall = 四门 passed 全 True。
- 台账：evidence 五件（h2h/h2h_ref/lineage/equivalence/launch 各自
  *_evidence.json，由各门自写，均落 <pkg>/evidence/）+ 本编排
  verify_summary.json——含各门 passed、overall、环境戳（python 版本/起止
  时间/v2/L1/verbatim 三 main 的 sha256）与 evidence 五件清单。
- 路径推导：v2 main=<pkg>/main.py；L1 main/verbatim main/三对手/语料缺省
  目录均由本文件位置相对推导，不手拼绝对路径。
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import sys
import time
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                    # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
for _path in (L1_DIR, HERE):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate_equivalence_v2       # noqa: E402  本包门③
import gate_h2h_vs_l1            # noqa: E402  本包门①
import gate_launch_fourgate_l1   # noqa: E402  L1 门④（复用，零改动）
import gate_lineage_strength     # noqa: E402  L1 门②（复用，零改动）

L1_MAIN = os.path.join(L1_DIR, "main.py")
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
USAGE = "usage: python verify_l11_gates.py <pkg_dir> [episodes_dir]"

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


@contextlib.contextmanager
def _lineage_evidence_redirect(target_path: str):
    """门②复用的 evidence 落点改指：L1 门②落点是 L1 包内模块级常量（无参可
    传），临时改指本包 target_path 并 try/finally 还原——防复用跑批覆写 L1 包
    真台账 lineage_evidence.json（只动进程内两模块属性，不触盘上 L1 目录）。"""
    old_dir, old_path = gate_lineage_strength.EVIDENCE_DIR, \
        gate_lineage_strength.EVIDENCE_PATH
    gate_lineage_strength.EVIDENCE_DIR = os.path.dirname(target_path)
    gate_lineage_strength.EVIDENCE_PATH = target_path
    try:
        yield
    finally:
        gate_lineage_strength.EVIDENCE_DIR = old_dir
        gate_lineage_strength.EVIDENCE_PATH = old_path


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


def verify(pkg_path=None, episodes_dir=None) -> dict:
    """顺序全跑四门①②③④→{overall, h2h, lineage, equivalence, launch,
    evidence_dir, started, finished}；写 evidence/verify_summary.json。

    pkg_path 缺省本目录（HERE=v2 包）；episodes_dir 即门③语料目录，缺省
    EPISODES_DIR_DEFAULT（相对推导）。任一门不可执行=整体 fail（fail-closed）
    但继续尝试其余门——四门 entry 全部落台账；五件 evidence 均落
    <pkg>/evidence/（门②经落点改指）。
    """
    started = _stamp()
    pkg_path = os.path.abspath(pkg_path) if pkg_path is not None else HERE
    episodes_dir = (os.path.abspath(episodes_dir) if episodes_dir
                    else EPISODES_DIR_DEFAULT)
    v2_main = os.path.join(pkg_path, "main.py")
    evidence_dir = os.path.join(pkg_path, "evidence")
    h2h_evidence = os.path.join(evidence_dir, gate_h2h_vs_l1.EVIDENCE_NAME)
    lineage_evidence = os.path.join(evidence_dir, "lineage_evidence.json")
    equivalence_evidence = os.path.join(
        evidence_dir, gate_equivalence_v2.EVIDENCE_NAME)
    launch_evidence = os.path.join(evidence_dir,
                                   "launch_check_evidence.json")
    evidence_files = {
        "h2h": h2h_evidence,
        "h2h_ref": os.path.join(evidence_dir,
                                gate_h2h_vs_l1.REF_EVIDENCE_NAME),
        "lineage": lineage_evidence,
        "equivalence": equivalence_evidence,
        "launch": launch_evidence,
    }

    # 门① h2h vs L1（缺省 16 局；另附 vs verbatim 8 局参考面，不进门）。
    h2h, res = _run_gate(
        "gate1 h2h vs L1",
        lambda: gate_h2h_vs_l1.run(v2_main, L1_MAIN, VERBATIM_MAIN,
                                   evidence_path=h2h_evidence))
    if res is not None:
        h2h.update({key: res.get(key) for key in ("n", "wins", "rate")})
        h2h["ref_face"] = res.get("ref_face")
        h2h["evidence_path"] = res.get("evidence_path")

    # 门② lineage strength（L1 复用；v2 对三对手各 8 局，evidence 落点改指
    # 本包——对手路径 sha 断裂 → 门内装载即抛 GateLineageError → fail-closed）。
    def _gate2():
        with _lineage_evidence_redirect(lineage_evidence):
            return gate_lineage_strength.run(v2_main, OPPONENTS,
                                             per_opponent_n=8)

    lineage, res = _run_gate("gate2 lineage strength (L1 reuse)", _gate2)
    if res is not None:
        lineage["per_opponent"] = {
            str(name): {key: (summ or {}).get(key) for key in _LINEAGE_KEYS}
            for name, summ in (res.get("per_opponent") or {}).items()}
        lineage["evidence_path"] = res.get("evidence_path")

    # 门③ equivalence v2（两路重演：appear≤2/逐局 ≥L1/死种≤$900/子集/五件用例）。
    equivalence, res = _run_gate(
        "gate3 equivalence v2",
        lambda: gate_equivalence_v2.run(episodes_dir, v2_main, L1_MAIN,
                                        VERBATIM_MAIN,
                                        evidence_path=equivalence_evidence))
    if res is not None:
        equivalence["form_face"] = (res.get("form_face") or {}).get("ok")
        equivalence["result_face"] = (res.get("result_face") or {}).get("ok")
        equivalence["appear_total"] = (res.get("form_face") or {}).get(
            "appear_total")
        equivalence["dead_seeds_total_value"] = (res.get("result_face")
                                                 or {}).get(
            "dead_seeds_total_value")
        for key in ("subset", "cases", "n_errors"):
            equivalence[key] = res.get(key)
        equivalence["evidence_path"] = res.get("evidence_path")

    # 门④ launch fourgate（L1 复用：发射四门+截断附加断言，pkg 换包重定向）。
    launch, res = _run_gate(
        "gate4 launch fourgate (L1 reuse)",
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
        "protocol": "verify-l11-gates/1.0",
        "pkg_path": pkg_path,
        "episodes_dir": episodes_dir,
        "gates_passed": {name: gates[name]["passed"] for name in _GATE_ORDER},
        "evidence_files": evidence_files,
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "python_full": sys.version,
        },
        "mains": {
            "v2_main": v2_main,
            "l1_main": L1_MAIN,
            "verbatim_main": VERBATIM_MAIN,
            "sha256": {
                "v2_main": _sha256_of(v2_main),
                "l1_main": _sha256_of(L1_MAIN),
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
