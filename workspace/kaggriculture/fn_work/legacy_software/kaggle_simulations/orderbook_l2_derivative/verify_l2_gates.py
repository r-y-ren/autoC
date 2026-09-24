"""verify_l2_gates（R12 L0）：两窗各全套四门，取全绿最宽窗；fail-closed。

责任契约（沿 v2 verify_l11_gates 形制，门①②④复用既有实现重定向）：
- verify(pkg_root, episodes_dir) -> {overall, windows:{w648:{overall…},
  w600:{…}}, recommended, evidence_dir, started, finished}；CLI
  `python verify_l2_gates.py <pkg_root> [episodes_dir]`（exit 0=存在全绿窗即
  recommended 非 None，1=无，2=用法错）。
- 两窗（pkg_root 下 w648/ 与 w600/ 子目录，build_l2_candidate 双窗产物位）
  各跑四门：
  ① gate_h2h_vs_l1（R11 L11 包，import 复用）：cand=该窗 v3 main、对手仍 L1
     （seeds 缺省 16 局；另附 vs verbatim 8 局参考面不进门）；
  ② gate_lineage_strength（L1 复用）：该窗 v3 对三对手各 8 局无翻负——L1 门
     无 evidence_path 参数（落点为 L1 包内模块级常量），编排以 try/finally
     临时改指该窗 evidence/lineage_evidence.json 并还原，防复用跑批覆写 L1 包
     真台账；
  ③ gate_equivalence_v3（本包门③，window=该窗）；
  ④ gate_launch_fourgate_l1（L1 复用）：发射四门+截断附加断言，pkg_path 换包
     重定向（v3 末 callable 同名 _cxs_agent）。
- 全跑不短路：任一门红也继续跑完其余门（两窗×四门共八次全跑）；任一门不可
  执行（抛异常，如窗包 main 缺失）→ 该门记 {executed=False, error, passed=
  False}，该窗必红，其余门照跑（fail-closed）。
- recommended=全绿的最宽窗：宽度约定 600>648（w600 窗口更早激活、回收面更大）
  ——两窗全绿→w600；仅 648 绿→w648；仅 600 绿→w600；都红→None。窗 overall=
  该窗四门 passed 全 True。
- 台账：各窗 evidence/ 五件（h2h/h2h_ref/lineage/equivalence_w{window}/launch
  各自 *_evidence.json，由各门自写）+ 本编排顶层 evidence/verify_summary_v3.json
  ——两窗对比+推荐窗+环境戳（python 版本/起止时间/L1 与 verbatim 两 main 及
  两窗 v3 main 的 sha256）。
- 路径推导：L1 main/verbatim main/三对手/语料缺省目录均由本文件位置
  （HERE/KSIM）相对推导，不手拼绝对路径。
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
L11_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_1_derivative"))
for _path in (L1_DIR, L11_DIR, HERE):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate_equivalence_v3       # noqa: E402  本包门③
import gate_h2h_vs_l1            # noqa: E402  R11 门①（L11 包，import 复用）
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
SUMMARY_NAME = "verify_summary_v3.json"
USAGE = "usage: python verify_l2_gates.py <pkg_root> [episodes_dir]"

WINDOWS = (648, 600)                 # 跑序（自然读序）；目录名 f"w{window}"
_WIDTH_ORDER = ("w600", "w648")      # 宽→窄（600 更宽：窗口更早激活，回收面更大）
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
    传），临时改指该窗 target_path 并 try/finally 还原——防复用跑批覆写 L1 包
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


def _run_window(pkg_root: str, window: int, episodes_dir: str) -> dict:
    """单窗四门①②③④全跑（不短路）→ {window, overall, h2h, lineage,
    equivalence, launch, v3_main, evidence_dir, evidence_files}。"""
    wname = f"w{window}"
    pkg_win = os.path.join(pkg_root, wname)
    v3_main = os.path.join(pkg_win, "main.py")
    evidence_dir = os.path.join(pkg_win, "evidence")
    evidence_files = {
        "h2h": os.path.join(evidence_dir, gate_h2h_vs_l1.EVIDENCE_NAME),
        "h2h_ref": os.path.join(evidence_dir, gate_h2h_vs_l1.REF_EVIDENCE_NAME),
        "lineage": os.path.join(evidence_dir, "lineage_evidence.json"),
        "equivalence": os.path.join(
            evidence_dir, gate_equivalence_v3.EVIDENCE_NAME_TEMPLATE.format(
                window=window)),
        "launch": os.path.join(evidence_dir, "launch_check_evidence.json"),
    }

    # 门① h2h vs L1（缺省 16 局；另附 vs verbatim 8 局参考面，不进门）。
    h2h, res = _run_gate(
        f"gate1 h2h vs L1 [{wname}]",
        lambda: gate_h2h_vs_l1.run(v3_main, L1_MAIN, VERBATIM_MAIN,
                                   evidence_path=evidence_files["h2h"]))
    if res is not None:
        h2h.update({key: res.get(key) for key in ("n", "wins", "rate")})
        h2h["ref_face"] = res.get("ref_face")
        h2h["evidence_path"] = res.get("evidence_path")

    # 门② lineage strength（L1 复用；该窗 v3 对三对手各 8 局，evidence 落点
    # 改指本窗——对手路径 sha 断裂 → 门内装载即抛 GateLineageError → fail-closed）。
    def _gate2():
        with _lineage_evidence_redirect(evidence_files["lineage"]):
            return gate_lineage_strength.run(v3_main, OPPONENTS,
                                             per_opponent_n=8)

    lineage, res = _run_gate(f"gate2 lineage strength (L1 reuse) [{wname}]",
                             _gate2)
    if res is not None:
        lineage["per_opponent"] = {
            str(name): {key: (summ or {}).get(key) for key in _LINEAGE_KEYS}
            for name, summ in (res.get("per_opponent") or {}).items()}
        lineage["evidence_path"] = res.get("evidence_path")

    # 门③ equivalence v3（window=该窗；终局≥L1/死种≤$500/饿死零容忍/净回收
    # 子集/九件构造用例）。
    equivalence, res = _run_gate(
        f"gate3 equivalence v3 [{wname}]",
        lambda: gate_equivalence_v3.run(episodes_dir, v3_main, L1_MAIN,
                                        VERBATIM_MAIN, window=window,
                                        evidence_path=evidence_files["equivalence"]))
    if res is not None:
        equivalence["form_face"] = (res.get("form_face") or {}).get("ok")
        equivalence["result_face"] = (res.get("result_face") or {}).get("ok")
        equivalence["dead_seeds_total_value"] = (res.get("result_face")
                                                 or {}).get(
            "dead_seeds_total_value")
        equivalence["starve_free"] = (res.get("result_face") or {}).get(
            "starve_free")
        for key in ("subset", "cases", "n_errors"):
            equivalence[key] = res.get(key)
        equivalence["evidence_path"] = res.get("evidence_path")

    # 门④ launch fourgate（L1 复用：发射四门+截断附加断言，pkg 换包重定向）。
    launch, res = _run_gate(
        f"gate4 launch fourgate (L1 reuse) [{wname}]",
        lambda: gate_launch_fourgate_l1.run(pkg_win,
                                            evidence_path=evidence_files["launch"]))
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
    return {"window": window, "overall": overall,
            "h2h": h2h, "lineage": lineage,
            "equivalence": equivalence, "launch": launch,
            "v3_main": v3_main, "evidence_dir": evidence_dir,
            "evidence_files": evidence_files}


def verify(pkg_root=None, episodes_dir=None) -> dict:
    """两窗（w648/w600）各顺序全跑四门①②③④→{overall, windows, recommended,
    evidence_dir, started, finished}；写顶层 evidence/verify_summary_v3.json。

    pkg_root 缺省本目录（HERE=l2 包根，窗子目录 w648/w600）；episodes_dir 即
    门③语料目录，缺省 EPISODES_DIR_DEFAULT（相对推导）。recommended=全绿的
    最宽窗（宽度 600>648；都红→None）；overall=recommended 非 None。任一门
    不可执行=该窗 fail（fail-closed）但两窗四门全部照跑——八次调用全落台账。"""
    started = _stamp()
    pkg_root = os.path.abspath(pkg_root) if pkg_root is not None else HERE
    episodes_dir = (os.path.abspath(episodes_dir) if episodes_dir
                    else EPISODES_DIR_DEFAULT)
    windows: dict = {}
    for window in WINDOWS:
        wname = f"w{window}"
        print(f"[verify] ==== window {wname} ====", flush=True)
        windows[wname] = _run_window(pkg_root, window, episodes_dir)
    recommended = next((wname for wname in _WIDTH_ORDER
                        if windows[wname]["overall"]), None)
    overall = recommended is not None
    finished = _stamp()

    top_evidence_dir = os.path.join(pkg_root, "evidence")
    result = {"overall": overall, "windows": windows,
              "recommended": recommended,
              "evidence_dir": top_evidence_dir, "started": started,
              "finished": finished}

    os.makedirs(top_evidence_dir, exist_ok=True)
    summary = dict(result)
    summary.update({
        "protocol": "verify-l2-gates/1.0",
        "pkg_root": pkg_root,
        "episodes_dir": episodes_dir,
        "width_order": list(_WIDTH_ORDER),
        "windows_passed": {wname: windows[wname]["overall"]
                           for wname in windows},
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "python_full": sys.version,
        },
        "mains": {
            "l1_main": L1_MAIN,
            "verbatim_main": VERBATIM_MAIN,
            "windows": {wname: {"main": windows[wname]["v3_main"]}
                        for wname in windows},
            "sha256": {
                "l1_main": _sha256_of(L1_MAIN),
                "verbatim_main": _sha256_of(VERBATIM_MAIN),
                **{f"{wname}_main": _sha256_of(windows[wname]["v3_main"])
                   for wname in windows},
            },
        },
    })
    summary_path = os.path.join(top_evidence_dir, SUMMARY_NAME)
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"[verify] recommended={recommended} "
          f"overall={'PASS' if overall else 'FAIL'} "
          f"summary -> {summary_path}", flush=True)
    return result


def main(argv=None) -> int:
    """CLI：exit 0=存在全绿窗（recommended 非 None）；1=无；2=用法错
    （参数个数 1-2：pkg_root [episodes_dir]）。"""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not 1 <= len(argv) <= 2:
        print(USAGE, file=sys.stderr)
        return 2
    result = verify(argv[0], argv[1] if len(argv) > 1 else None)
    print(f"overall = {result['overall']}")
    print(f"recommended = {result['recommended']}")
    print(f"evidence_dir = {result['evidence_dir']}")
    return 0 if result["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
