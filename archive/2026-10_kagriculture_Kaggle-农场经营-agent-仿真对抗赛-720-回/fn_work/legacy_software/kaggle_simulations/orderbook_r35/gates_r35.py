# -*- coding: utf-8 -*-
"""verify_r35_gates（R17 L1）：r35 全量门禁编排（fail-closed 全跑）。

复用 R16 管线重定向（零改动既有目录）：
- 门①四门（r30/v48 管线）：装载 last-callable（末 callable=agent——_HR
  包装后官方入口）/双席 DONE+每步 <1s/确定性双跑 sha/体积+身份链。
- 门② h2h vs r34a 在飞件（orderbook_2965_adopt/a，ref 56526029 同字节，
  先三方核对 build_manifest）：seated 通道双席位 16 局互胜 ≥0.55。
- 门③谱系：v48-pure/v4b 各 8 局无负。
- 门④饿死零容忍+子集（沿 L3/R16 口径）：26 局 strip 语料，starve 基线
  r32（L3 fine 在库件）+subset vs verbatim。
- 门⑤diff 审计：r35 对 r34a 变更集恰=并入项白名单（复跑）。
全跑不短路；任一门不可执行→{executed=False, passed=False}，整体必红。
evidence 落 orderbook_r35/evidence/ + verify_summary_r35.json。
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import sys
import time
from typing import Any, Dict, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
L1_DIR = os.path.join(KSIM, "orderbook_l1_derivative")
L3_DIR = os.path.join(KSIM, "orderbook_l3_derivative")
R34A_DIR = os.path.join(KSIM, "orderbook_2965_adopt", "a")
for _p in (L1_DIR, L3_DIR, os.path.join(KSIM, "orderbook_2965_adopt"), HERE,
           KSIM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_equivalence_l3 as _l3eq       # noqa: E402
import gate_equivalence_precision as _l1  # noqa: E402
import gate_equivalence_v3 as _v3         # noqa: E402
import gate_h2h_vs_verbatim as _h2h_base  # noqa: E402
import gate_launch_fourgate_l1 as _l1g    # noqa: E402
import gate_lineage_strength as _lin      # noqa: E402

from orderbook_r35 import build_r35 as _b35
from orderbook_r35 import phase_v as _pv

R34A_MAIN = os.path.join(R34A_DIR, "main.py")
R32_MAIN = os.path.join(L3_DIR, "main.py")               # starve 基线（L3 fine）
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative", "main.py")
OPPONENTS = {
    "v48-pure": os.path.join(KSIM, "opponents", "v48_main.py"),
    "v4b": os.path.join(KSIM, "v48_hybrid", "v4b", "main.py"),
}
EPISODES_DIR = os.path.normpath(os.path.join(
    KSIM, os.pardir, os.pardir, os.pardir, "fn_docs", "hybrid", "results",
    "replays-r30-26"))
R35_LAST_CALLABLE = "agent"
R34A_LAST_CALLABLE = "_cxd_agent"
H2H_WIN_THRESHOLD = 0.55
USAGE = "usage: python gates_r35.py [r35_pkg_dir]"


class GateR35Error(RuntimeError):
    """门禁 fail-closed 承载。"""


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _run_gate(label: str, thunk):
    t0 = time.perf_counter()
    print(f"[verify-r35] {label} running ...", flush=True)
    try:
        result = thunk()
    except (Exception, SystemExit) as exc:
        entry = {"passed": False, "executed": False,
                 "error": f"{type(exc).__name__}: {exc}",
                 "wall_s": round(time.perf_counter() - t0, 1)}
        print(f"[verify-r35] {label} NOT EXECUTABLE (fail-closed): "
              f"{entry['error']}", flush=True)
        return entry, None
    entry = {"passed": bool(result.get("passed")), "executed": True,
             "error": None, "wall_s": round(time.perf_counter() - t0, 1)}
    print(f"[verify-r35] {label} {'PASS' if entry['passed'] else 'FAIL'} "
          f"({entry['wall_s']}s)", flush=True)
    return entry, result


def _verify_ref_package(pkg_dir: str, what: str) -> Dict[str, Any]:
    import io
    import tarfile
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
        raise GateR35Error(f"{what} 身份链不符（manifest vs 盘上/tar）: {pkg_dir}")
    return {"what": what, "pkg": pkg_dir, "main_sha256": main_sha,
            "tar_sha256": tar_sha, "match": True}


# ---------------------------------------------------------------------------
# 门①四门
# ---------------------------------------------------------------------------
def _gate_launch_fourgate(pkg_dir: str) -> Dict[str, Any]:
    identity = _l1g._identity_chain(pkg_dir)
    gates = {"package": bool(identity["match"] and identity["tar_size_ok"])}
    result: Dict[str, Any] = {"gates": gates, "identity": identity}
    if not gates["package"]:
        result.update({"passed": False, "note": "identity chain mismatch"})
        return result
    import shutil
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
                and ev1.get("last_callable_name") == R35_LAST_CALLABLE)
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
        import shutil as _sh
        _sh.rmtree(check.TMP_DIR, ignore_errors=True)
    result["passed"] = bool(all(gates.values()))
    return result


# ---------------------------------------------------------------------------
# 门② h2h vs r34a 在飞件
# ---------------------------------------------------------------------------
def _gate_h2h_vs_r34a(r35_main: str, evidence_path: str) -> Dict[str, Any]:
    res = _h2h_base.run(
        r35_main, R34A_MAIN,
        evidence_path=evidence_path,
        l1_expected_names=frozenset({R35_LAST_CALLABLE}),
        verbatim_expected_names=frozenset({R34A_LAST_CALLABLE}))
    return {"passed": bool(res["passed"]), "n": res["n"], "wins": res["wins"],
            "losses": res["losses"], "ties": res["ties"], "rate": res["rate"],
            "threshold": H2H_WIN_THRESHOLD,
            "mean_margin": res.get("mean_margin"),
            "evidence_path": res["evidence_path"]}


# ---------------------------------------------------------------------------
# 门③谱系
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


def _gate_lineage(r35_main: str, evidence_path: str) -> Dict[str, Any]:
    with _lineage_redirect(evidence_path):
        res = _lin.run(r35_main, OPPONENTS, per_opponent_n=8)
    per = {name: {k: (summ or {}).get(k) for k in
                  ("n", "wins", "losses", "ties", "all_done")}
           for name, summ in (res.get("per_opponent") or {}).items()}
    return {"passed": bool(res["passed"]), "per_opponent": per,
            "evidence_path": res["evidence_path"]}


# ---------------------------------------------------------------------------
# 门④饿死零容忍+子集（沿 R16 口径）
# ---------------------------------------------------------------------------
def _gate_starve_subset(r35_main: str, evidence_path: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    replays = _l1._discover_replays(EPISODES_DIR, None)
    if not replays:
        raise GateR35Error(f"语料缺失：{EPISODES_DIR}")
    r35_fn = _l1._as_callable(r35_main)
    r32_fn = _l1._as_callable(R32_MAIN)
    vb_fn = _l1._as_callable(VERBATIM_MAIN)
    rows, starve_all, form_products = [], [], []
    n_errors = 0
    for path in replays:
        ep = _l1._episode_from_path(path)
        row: Dict[str, Any] = {"episode": ep}
        try:
            with _l3eq._normalized_classify():
                form = _l1.replay_action_diff(path, r35_fn, vb_fn)
            form_products.append(form)
            r35_term = _v3._seated_terminal(path, r35_fn)
            r32_term = _v3._seated_terminal(path, r32_fn)
            starve = _v3._starve_verdict(r35_term, r32_term)
            starve_all.append(starve)
            row.update({"error": None, "starve_ok": starve["ok"],
                        "n_starve_violations": len(starve["violations"])})
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
        "subset_detail": {k: subset.get(k) for k in
                          ("n_games", "n_ok", "violations")},
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
# 门⑤diff 审计（复跑 build 面白名单归因）
# ---------------------------------------------------------------------------
def _gate_diff_audit(r34a_main: str, r35_main: str,
                     evidence_path: str) -> Dict[str, Any]:
    audit = _b35.audit_diff_vs_r34a(r34a_main, r35_main)
    os.makedirs(os.path.dirname(evidence_path), exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return {"passed": bool(audit["ok"]),
            "attribution": audit["attribution"],
            "evidence_path": evidence_path}


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
_GATE_ORDER = ("launch", "h2h_vs_r34a", "lineage", "starve_subset", "diff_audit")


def verify_r35_gates(r35_pkg: Optional[str] = None) -> Dict[str, Any]:
    """五门 fail-closed 全跑 → verify_summary_r35.json。

    r35_pkg 缺省 HERE（orderbook_r35/；main.py/tar/manifest 直落包根）。
    r34a 在飞件身份链先核对（不符→h2h 记 error 面其余门照跑）。
    """
    pkg_dir = os.path.abspath(r35_pkg or HERE)
    r35_main = os.path.join(pkg_dir, "main.py")
    if not os.path.isfile(r35_main):
        raise GateR35Error(f"r35 未构建：{r35_main}（先跑 build_r35）")
    evidence_dir = os.path.join(pkg_dir, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    gates: Dict[str, Any] = {}

    gates["launch"], res = _run_gate(
        "launch fourgate (r30 pipeline)",
        lambda: _gate_launch_fourgate(pkg_dir))
    if res is not None:
        gates["launch"]["four"] = res["gates"]

    ref_identity = None
    ref_error = None
    try:
        ref_identity = _verify_ref_package(R34A_DIR, "r34a 在飞件（h2h 基线）")
    except Exception as exc:
        ref_error = f"{type(exc).__name__}: {exc}"

    gates["h2h_vs_r34a"], res = _run_gate(
        f"h2h vs r34a in-flight (>= {H2H_WIN_THRESHOLD}, 16 seated)",
        lambda: _gate_h2h_vs_r34a(
            r35_main, os.path.join(evidence_dir, "h2h_vs_r34a_evidence.json")))
    if res is not None:
        gates["h2h_vs_r34a"].update(
            {k: res.get(k) for k in ("n", "wins", "losses", "ties", "rate",
                                     "mean_margin")})
    if ref_error:
        gates["h2h_vs_r34a"]["ref_identity_error"] = ref_error
        gates["h2h_vs_r34a"]["passed"] = False

    gates["lineage"], res = _run_gate(
        "lineage v48/v4b x8 no-loss",
        lambda: _gate_lineage(
            r35_main, os.path.join(evidence_dir, "lineage_evidence.json")))
    if res is not None:
        gates["lineage"]["per_opponent"] = res.get("per_opponent")

    gates["starve_subset"], res = _run_gate(
        "starve zero-tolerance + subset (L3 caliber, 26 replays)",
        lambda: _gate_starve_subset(
            r35_main, os.path.join(evidence_dir, "starve_subset_evidence.json")))
    if res is not None:
        gates["starve_subset"].update(
            {k: res.get(k) for k in ("starve_free", "n_games", "n_errors",
                                     "n_starve_red_games", "subset")})

    gates["diff_audit"], res = _run_gate(
        "diff audit r35 vs r34a (whitelist)",
        lambda: _gate_diff_audit(
            R34A_MAIN, r35_main,
            os.path.join(evidence_dir, "diff_audit_r35_vs_r34a.json")))
    if res is not None:
        gates["diff_audit"]["attribution"] = res.get("attribution")

    overall = all(gates[name]["passed"] for name in _GATE_ORDER)
    summary = {
        "protocol": "verify-r35/1.0",
        "variant": "r35",
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
            "r34a_inflight": ref_identity or {"error": ref_error},
            "r34a_ref_submission": 56526029,
            "r32_starve_baseline": {"main": R32_MAIN,
                                    "sha256": _sha256_file(R32_MAIN)},
            "verbatim": {"main": VERBATIM_MAIN,
                         "sha256": _sha256_file(VERBATIM_MAIN)},
            "episodes_dir": EPISODES_DIR,
        },
        "mains": {"r35": r35_main, "sha256": _sha256_file(r35_main)},
    }
    summary_path = os.path.join(evidence_dir, "verify_summary_r35.json")
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"[verify-r35] overall={'PASS' if overall else 'FAIL'} -> {summary_path}",
          flush=True)
    return summary


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print(USAGE, file=sys.stderr)
        return 2
    summary = verify_r35_gates(argv[0] if argv else None)
    return 0 if summary["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
