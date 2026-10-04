# -*- coding: utf-8 -*-
"""verify_2965_gates（R16 L0）：双件 r34a/b 全量门禁编排（fail-closed 全跑）。

门面（复用既有管线重定向，零改动既有目录）：
- 门①四门（沿 r30/v48 管线重定向）：装载 last-callable（官方 -I 子进程语义，
  断言末 callable=_cxd_agent——layer S 已移除，链由 _cxd_agent 直出）/双席
  DONE+每步 <1s/确定性双跑 sha/体积+身份链（manifest sha 键集沿 r30）。
- 门② h2h vs r33 在飞件：seated 双席位 16 局互胜 ≥0.55（gate_h2h_vs_verbatim
  import 复用，期望装载身份 cand=_cxd_agent/opp=_cxs_agent；r33 在飞字节=
  orderbook_l3_derivative/variant_tuned{main.py,submission.tar.gz}，先对其
  build_manifest.json 三方核对，不符即红——fail-closed）。
- 门③谱系：v48-pure/v4b 各 8 局无负（gate_lineage_strength import 复用，
  evidence 落点进程内改指本包各件 evidence/）。
- 门④饿死零容忍+子集（沿 L3 口径重验）：26 局 strip 语料——
  starve：r34 vs r32（L3 fine 在库件=同钳制基座+layer S 的直接前驱）终态
  plants/shed/inventories 逐品项不减（_seated_terminal+_starve_verdict 复用）；
  subset：diff(r34 vs verbatim) 净回收 ≤ 原局未种下量（replay_action_diff+
  _netted_recovery_products+precision_subset_check 复用，空槽归一换装沿
  gate_equivalence_l3._normalized_classify）。r34b 另记 vs r34a 参考面
  （non-gating，常数面隔离观测）。
- 门⑤diff 审计：audit_diff_vs_2965 复跑（白名单外差异=红）。
全跑不短路：任一门红也继续跑完其余门；门不可执行（异常）→该门
{executed=False, error, passed=False}，整体必红。overall=五门 passed 全 True。
evidence 落 <包>/{a,b}/evidence/（各门自写）+verify_summary_r34{a,b}.json。
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from typing import Any, Dict, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                              # kaggle_simulations/
L1_DIR = os.path.join(KSIM, "orderbook_l1_derivative")
L2_DIR = os.path.join(KSIM, "orderbook_l2_derivative")
L3_DIR = os.path.join(KSIM, "orderbook_l3_derivative")
for _p in (L1_DIR, L2_DIR, L3_DIR, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_equivalence_l3 as _l3eq       # noqa: E402  空槽归一换装（S6 修订）
import gate_equivalence_precision as _l1  # noqa: E402  重演/子集部件（import 复用）
import gate_equivalence_v3 as _v3         # noqa: E402  终态/饿死部件（import 复用）
import gate_h2h_vs_verbatim as _h2h_base  # noqa: E402  h2h 主体（import 复用）
import gate_lineage_strength as _lin      # noqa: E402  谱系门（import 复用）
try:                                     # pytest（包名导入）与 CLI（脚本态）双装载面
    from orderbook_2965_adopt import build_adopt as _build  # noqa: E402
except ImportError:                      # pragma: no cover - 脚本态补 sys.path
    if KSIM not in sys.path:
        sys.path.insert(0, KSIM)
    from orderbook_2965_adopt import build_adopt as _build  # noqa: E402

R33_DIR = os.path.join(L3_DIR, "variant_tuned")          # r33 在飞件（tuned）
R32_MAIN = os.path.join(L3_DIR, "main.py")               # r32（L3 fine，starve 基线）
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative", "main.py")
OPPONENTS = {
    "v48-pure": os.path.join(KSIM, "opponents", "v48_main.py"),
    "v4b": os.path.join(KSIM, "v48_hybrid", "v4b", "main.py"),
}
EPISODES_DIR = os.path.normpath(os.path.join(
    KSIM, os.pardir, os.pardir, os.pardir, "fn_docs", "hybrid", "results",
    "replays-r30-26"))
R34_LAST_CALLABLE = "_cxd_agent"
R33_LAST_CALLABLE = "_cxs_agent"
H2H_WIN_THRESHOLD = 0.55
SUMMARY_NAME = "verify_summary_r34{label}.json"
USAGE = "usage: python gates_adopt.py [adopt_root]"


class GateAdoptError(RuntimeError):
    """门禁 fail-closed：装载/身份链/在飞件核对失败（整体不可执行=门红承载）。"""


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _run_gate(label: str, thunk):
    """跑一门（fail-closed 全跑不短路）：异常→{executed=False, passed=False}。"""
    t0 = time.perf_counter()
    print(f"[verify-r34] {label} running ...", flush=True)
    try:
        result = thunk()
    except (Exception, SystemExit) as exc:
        entry = {"passed": False, "executed": False,
                 "error": f"{type(exc).__name__}: {exc}",
                 "wall_s": round(time.perf_counter() - t0, 1)}
        print(f"[verify-r34] {label} NOT EXECUTABLE (fail-closed): "
              f"{entry['error']}", flush=True)
        return entry, None
    entry = {"passed": bool(result.get("passed")), "executed": True,
             "error": None, "wall_s": round(time.perf_counter() - t0, 1)}
    print(f"[verify-r34] {label} {'PASS' if entry['passed'] else 'FAIL'} "
          f"({entry['wall_s']}s)", flush=True)
    return entry, result


# ---------------------------------------------------------------------------
# 在飞件/基线件身份核对（对 build_manifest 三方核对，fail-closed）
# ---------------------------------------------------------------------------
def _verify_ref_package(pkg_dir: str, what: str) -> Dict[str, Any]:
    """对 <pkg_dir>/build_manifest.json 核对盘上 main/tar（沿 r30 身份链键集）。"""
    import tarfile
    import io
    manifest = json.load(open(os.path.join(pkg_dir, "build_manifest.json"),
                              encoding="utf-8"))
    main_path = os.path.join(pkg_dir, "main.py")
    tar_path = os.path.join(pkg_dir, "submission.tar.gz")
    main_sha, tar_sha = _sha256_file(main_path), _sha256_file(tar_path)
    with tarfile.open(fileobj=io.BytesIO(open(tar_path, "rb").read()),
                      mode="r:gz") as tar:
        names = tar.getnames()
        inner_ok = (names == ["main.py"]
                    and tar.extractfile("main.py").read()
                    == open(main_path, "rb").read())
    ok = (main_sha == manifest.get("main_sha256")
          and tar_sha == manifest.get("tar_sha256")
          and os.path.getsize(main_path) == manifest.get("main_bytes")
          and os.path.getsize(tar_path) == manifest.get("tar_bytes")
          and names == ["main.py"] and inner_ok)
    if not ok:
        raise GateAdoptError(f"{what} 身份链不符（manifest vs 盘上/tar）: {pkg_dir}")
    return {"what": what, "pkg": pkg_dir, "main_sha256": main_sha,
            "tar_sha256": tar_sha, "match": True}


# ---------------------------------------------------------------------------
# 门①四门（v48 单实现重定向；沿 gate_launch_fourgate_l1 先例）
# ---------------------------------------------------------------------------
def _gate_launch_fourgate(pkg_dir: str, evidence_dir: str) -> Dict[str, Any]:
    import gate_launch_fourgate_l1 as _l1g
    identity = _l1g._identity_chain(pkg_dir)
    gates = {"package": bool(identity["match"] and identity["tar_size_ok"])}
    result: Dict[str, Any] = {"gates": gates, "identity": identity}
    if not gates["package"]:
        result.update({"passed": False, "note": "identity chain mismatch"})
        return result
    check = _l1g._redirect_check(pkg_dir)
    try:
        g23 = check.gate2_gate3()
        obs_series = g23.pop("_obs_series_seed101", None)
        gates["full_episodes"] = bool(g23["gate2_full_episodes_ok"])
        gates["determinism"] = bool(g23["gate3_determinism_ok"])
        if obs_series is not None:
            g1 = check.gate1(obs_series)
            ev1 = g1.get("evidence") or {}
            gates["load"] = bool(
                g1.get("gate1_official_load_ok")
                and ev1.get("last_callable_name") == R34_LAST_CALLABLE)
            result["gate1"] = {
                "last_callable": ev1.get("last_callable_name"),
                "n_obs_replayed": g1.get("n_obs_replayed"),
                "mismatches": g1.get("isolated_vs_local_action_mismatches"),
                "non_stdlib_imports": ev1.get("non_stdlib_imports"),
            }
        result["gate2"] = {k: g23.get(k) for k in (
            "gate2_full_episodes_ok", "gate2_step_budget_ms")}
        result["gate3"] = {"gate3_determinism_ok": g23.get("gate3_determinism_ok"),
                           "gate3_hashes": g23.get("gate3_hashes")}
    finally:
        shutil.rmtree(check.TMP_DIR, ignore_errors=True)
    result["passed"] = bool(all(gates.values()))
    return result


# ---------------------------------------------------------------------------
# 门② h2h vs r33 在飞件
# ---------------------------------------------------------------------------
def _gate_h2h_vs_r33(r34_main: str, evidence_path: str) -> Dict[str, Any]:
    res = _h2h_base.run(
        r34_main, os.path.join(R33_DIR, "main.py"),
        evidence_path=evidence_path,
        l1_expected_names=frozenset({R34_LAST_CALLABLE}),
        verbatim_expected_names=frozenset({R33_LAST_CALLABLE}))
    return {"passed": bool(res["passed"]), "n": res["n"], "wins": res["wins"],
            "losses": res["losses"], "ties": res["ties"], "rate": res["rate"],
            "threshold": H2H_WIN_THRESHOLD,
            "evidence_path": res["evidence_path"]}


# ---------------------------------------------------------------------------
# 门③谱系（v48/v4b 各 8 局无负；evidence 落点进程内改指）
# ---------------------------------------------------------------------------
@contextlib.contextmanager
def _lineage_redirect(target_path: str):
    old_dir, old_path = _lin.EVIDENCE_DIR, _lin.EVIDENCE_PATH
    _lin.EVIDENCE_DIR = os.path.dirname(target_path)
    _lin.EVIDENCE_PATH = target_path
    try:
        yield
    finally:
        _lin.EVIDENCE_DIR = old_dir
        _lin.EVIDENCE_PATH = old_path


def _gate_lineage(r34_main: str, evidence_path: str) -> Dict[str, Any]:
    with _lineage_redirect(evidence_path):
        res = _lin.run(r34_main, OPPONENTS, per_opponent_n=8)
    per = {name: {k: (summ or {}).get(k) for k in
                  ("n", "wins", "losses", "ties", "all_done")}
           for name, summ in (res.get("per_opponent") or {}).items()}
    return {"passed": bool(res["passed"]), "per_opponent": per,
            "evidence_path": res["evidence_path"]}


# ---------------------------------------------------------------------------
# 门④饿死零容忍+子集（沿 L3 口径）
# ---------------------------------------------------------------------------
def _gate_starve_subset(r34_main: str, ref_main: Optional[str],
                        evidence_path: str) -> Dict[str, Any]:
    """26 局：starve=r34 vs r32 终态逐品项不减；subset=净回收≤未种下量。

    ref_main 给定时另记非门控参考面（r34b vs r34a 常数隔离观测）。"""
    t0 = time.perf_counter()
    replays = _l1._discover_replays(EPISODES_DIR, None)
    if not replays:
        raise GateAdoptError(f"语料缺失：{EPISODES_DIR}")
    r34_fn = _l1._as_callable(r34_main)
    r32_fn = _l1._as_callable(R32_MAIN)
    vb_fn = _l1._as_callable(VERBATIM_MAIN)
    ref_fn = _l1._as_callable(ref_main) if ref_main else None

    rows, starve_all, form_products = [], [], []
    n_errors = 0
    for path in replays:
        ep = _l1._episode_from_path(path)
        row: Dict[str, Any] = {"episode": ep}
        try:
            with _l3eq._normalized_classify():
                form = _l1.replay_action_diff(path, r34_fn, vb_fn)
            form_products.append(form)
            r34_term = _v3._seated_terminal(path, r34_fn)
            r32_term = _v3._seated_terminal(path, r32_fn)
            starve = _v3._starve_verdict(r34_term, r32_term)
            starve_all.append(starve)
            row.update({"error": None, "starve_ok": starve["ok"],
                        "n_starve_violations": len(starve["violations"])})
            if ref_fn is not None:
                ref_term = _v3._seated_terminal(path, ref_fn)
                row["ref_starve_ok"] = _v3._starve_verdict(r34_term,
                                                           ref_term)["ok"]
        except Exception as exc:
            n_errors += 1
            row.update({"error": f"{type(exc).__name__}: {exc}",
                        "starve_ok": False, "n_starve_violations": None})
        rows.append(row)
    starve_free = bool(rows) and n_errors == 0 and all(
        r.get("starve_ok") for r in rows)
    subset = _l1.precision_subset_check(
        _v3._netted_recovery_products(form_products))
    subset_ok = bool(subset.get("all_ok"))
    result = {
        "passed": bool(starve_free and subset_ok and not n_errors),
        "starve_baseline": "r32(L3 fine) 在库件",
        "starve_free": starve_free, "n_games": len(rows),
        "n_errors": n_errors,
        "n_starve_red_games": sum(1 for r in rows if r.get("starve_ok") is False),
        "subset": subset_ok,
        "per_game": rows,
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    os.makedirs(os.path.dirname(evidence_path), exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    result["evidence_path"] = evidence_path
    return result


# ---------------------------------------------------------------------------
# 门⑤diff 审计（复跑 build 面审计，白名单外=红）
# ---------------------------------------------------------------------------
def _gate_diff_audit(r34a_main: str, r34b_main: str,
                     evidence_path: str) -> Dict[str, Any]:
    src = _build.fetch_2965_source()
    audit = _build.audit_diff_vs_2965(r34a_main, r34b_main, src["path"])
    os.makedirs(os.path.dirname(evidence_path), exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return {"passed": bool(audit["ok"]),
            "attribution": {k: audit[k]["attribution"] for k in ("a", "b")},
            "evidence_path": evidence_path}


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
_GATE_ORDER = ("launch", "h2h_vs_r33", "lineage", "starve_subset", "diff_audit")


def _verify_one(label: str, pkg_dir: str, r34a_main: str, r34b_main: str) -> Dict[str, Any]:
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    r34_main = os.path.join(pkg_dir, "main.py")
    evidence_dir = os.path.join(pkg_dir, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    gates: Dict[str, Any] = {}

    gates["launch"], res = _run_gate(
        "launch fourgate (r30 pipeline)",
        lambda: _gate_launch_fourgate(pkg_dir, evidence_dir))
    if res is not None:
        gates["launch"]["four"] = res["gates"]

    gates["h2h_vs_r33"], res = _run_gate(
        f"h2h vs r33 in-flight (>= {H2H_WIN_THRESHOLD}, 16 seated)",
        lambda: _gate_h2h_vs_r33(
            r34_main, os.path.join(evidence_dir, "h2h_vs_r33_evidence.json")))
    if res is not None:
        gates["h2h_vs_r33"].update(
            {k: res.get(k) for k in ("n", "wins", "losses", "ties", "rate")})

    gates["lineage"], res = _run_gate(
        "lineage v48/v4b x8 no-loss",
        lambda: _gate_lineage(
            r34_main, os.path.join(evidence_dir, "lineage_evidence.json")))
    if res is not None:
        gates["lineage"]["per_opponent"] = res.get("per_opponent")

    ref_main = r34a_main if label == "b" else None
    gates["starve_subset"], res = _run_gate(
        "starve zero-tolerance + subset (L3 caliber, 26 replays)",
        lambda: _gate_starve_subset(
            r34_main, ref_main,
            os.path.join(evidence_dir, "starve_subset_evidence.json")))
    if res is not None:
        gates["starve_subset"].update(
            {k: res.get(k) for k in ("starve_free", "n_games", "n_errors",
                                     "n_starve_red_games", "subset")})

    gates["diff_audit"], res = _run_gate(
        "diff audit vs 2965 original",
        lambda: _gate_diff_audit(
            r34a_main, r34b_main,
            os.path.join(evidence_dir, "audit_diff_vs_2965.json")))
    if res is not None:
        gates["diff_audit"]["attribution"] = res.get("attribution")

    overall = all(gates[name]["passed"] for name in _GATE_ORDER)
    summary = {
        "protocol": "verify-2965-adopt/1.0",
        "variant": f"r34{label}",
        "overall": overall,
        "gates_passed": {name: gates[name]["passed"] for name in _GATE_ORDER},
        "gates": gates,
        "pkg_path": pkg_dir,
        "started": started,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "references": {
            "r33_inflight": _verify_ref_package(R33_DIR, "r33 在飞件"),
            "r32_starve_baseline": {
                "main": R32_MAIN, "sha256": _sha256_file(R32_MAIN)},
            "verbatim": {"main": VERBATIM_MAIN,
                         "sha256": _sha256_file(VERBATIM_MAIN)},
            "episodes_dir": EPISODES_DIR,
        },
        "mains": {"r34": r34_main, "sha256": _sha256_file(r34_main)},
    }
    summary_path = os.path.join(evidence_dir, SUMMARY_NAME.format(label=label))
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"[verify-r34] r34{label} overall={'PASS' if overall else 'FAIL'} "
          f"-> {summary_path}", flush=True)
    return summary


def verify_2965_gates(adopt_root: Optional[str] = None) -> Dict[str, Any]:
    """双件 fail-closed 全跑 → {a: summary, b: summary}。

    先核对 r33 在飞件身份链（不符即双件 launch 参照面记 error，其余门照跑）。
    """
    adopt_root = os.path.abspath(adopt_root or HERE)
    a_main = os.path.join(adopt_root, "a", "main.py")
    b_main = os.path.join(adopt_root, "b", "main.py")
    for p in (a_main, b_main):
        if not os.path.isfile(p):
            raise GateAdoptError(f"双件未构建：{p}（先跑 build_adopt）")
    return {
        "a": _verify_one("a", os.path.join(adopt_root, "a"), a_main, b_main),
        "b": _verify_one("b", os.path.join(adopt_root, "b"), a_main, b_main),
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print(USAGE, file=sys.stderr)
        return 2
    result = verify_2965_gates(argv[0] if argv else None)
    overall = result["a"]["overall"] and result["b"]["overall"]
    print(f"overall = a:{result['a']['overall']} b:{result['b']['overall']}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
