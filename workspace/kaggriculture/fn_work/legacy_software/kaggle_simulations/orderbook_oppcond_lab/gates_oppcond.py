# -*- coding: utf-8 -*-
"""gates_oppcond：四形态四门体检（gates_strongest/cond_route 同口径；不发射）。

四门 × 形态（h1_base/oc_c1/oc_c2/oc_c1c2c3）：
①装载 last-callable（末 callable=_hs_agent；官方 last-callable 语义）
②双席 DONE+单步<1s（seeds 101/102 官方 kaggriculture 引擎完整局自打，
   每步 <1000ms、turns=720）
③确定性双跑（同 seed 重跑动作流 sha256 一致）
④体积<100MB+sha 身份（tar 成员恰 ['main.py']、内层 main 与盘上一致、
   sha 对 build_manifest、H1 基座字节前缀恒等；h1_base 期望字节恒等 H1）。
门内全跑不短路；任一红→overall 红。复用（不改写）：
gate_launch_fourgate_l1._redirect_check（换包重定向）+
v48_derivative_launch_check.run_full_episode。
只写 orderbook_oppcond_lab/build/<form>/evidence/ 与 evidence/gates.json。
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM = str(MODULE_DIR.parent)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)
L1_DIR = os.path.join(KSIM, "orderbook_l1_derivative")
if L1_DIR not in sys.path:
    sys.path.insert(0, L1_DIR)

RECORD_VERSION = "oppcond-gates/1.0"
ENTRY_NAME = "_hs_agent"
STEP_BUDGET_MS = 1000.0
EPISODE_SEEDS = (101, 102)
SIZE_CAP_BYTES = 100 * 1024 * 1024
BUILD = MODULE_DIR / "build"
EVID_PATH = MODULE_DIR / "evidence" / "gates.json"
FORMS = ("h1_base", "oc_c1", "oc_c2", "oc_c1c2c3")


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _redirect(pkg: Path):
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(str(pkg))
    check.DERIV_MAIN = str(pkg / "main.py")
    check.OUT_DIR = str(pkg / "evidence")
    check.TMP_DIR = str(pkg / "evidence" / "tmp_launch")
    return check


def _gate_load(pkg: Path):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(str(pkg / "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
    return {"passed": True, "entry": name}


def _run_episode(pkg: Path, seed):
    return _redirect(pkg).run_full_episode(int(seed))


def _gate_health(pkg: Path):
    eps = [_run_episode(pkg, s) for s in EPISODE_SEEDS]
    details = []
    ok = True
    for ep in eps:
        statuses = list(ep.get("statuses") or [])
        rewards = list(ep.get("rewards") or [])
        step_ms = ep.get("max_step_ms")
        turns = ep.get("turns_played")
        good = (statuses == ["DONE", "DONE"] and len(rewards) == 2
                and all(_is_num(r) and abs(float(r)) < 1e12 for r in rewards)
                and _is_num(step_ms) and float(step_ms) < STEP_BUDGET_MS
                and turns == 720)
        ok = ok and good
        details.append({"seed": ep.get("seed"), "statuses": statuses,
                        "turns_played": turns, "max_step_ms": step_ms,
                        "p99_step_ms": ep.get("p99_step_ms"),
                        "passed": good})
    return {"passed": ok, "step_budget_ms": STEP_BUDGET_MS,
            "episodes": details}


def _gate_determinism(pkg: Path):
    e1 = _run_episode(pkg, EPISODE_SEEDS[0])
    e2 = _run_episode(pkg, EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": ok, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity(pkg: Path, form: str):
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = Path(man["base_main"]).read_bytes()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = (main_sha == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest() == man.get("tar_sha256"))
    prefix_ok = main_bytes.startswith(base)
    is_base = main_bytes == base
    expect_base = (form == "h1_base")
    form_ok = (is_base == expect_base)
    ok = all([size_ok, members_ok, inner_ok, sha_ok, prefix_ok, form_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok,
            "base_prefix_identical": prefix_ok,
            "byte_identical_to_H1_base": is_base,
            "expect_byte_identical": expect_base,
            "base_main_sha256": hashlib.sha256(base).hexdigest()}


def main():
    t0 = time.perf_counter()
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": ["python3 orderbook_oppcond_lab/gates_oppcond.py"],
                   "forms": list(FORMS), "episode_seeds": list(EPISODE_SEEDS)},
        "forms": {},
    }
    overall = True
    for form in FORMS:
        pkg = BUILD / form
        gates = {}
        for name, fn in (("load", _gate_load), ("health", _gate_health),
                         ("determinism", _gate_determinism)):
            try:
                gates[name] = fn(pkg)
            except Exception as exc:
                gates[name] = {"passed": False,
                               "error": "%s: %s" % (type(exc).__name__, exc)}
        try:
            gates["identity"] = _gate_identity(pkg, form)
        except Exception as exc:
            gates["identity"] = {"passed": False,
                                 "error": "%s: %s" % (type(exc).__name__, exc)}
        gates["overall"] = all(g.get("passed") for g in gates.values())
        overall = overall and gates["overall"]
        out["forms"][form] = gates
        print(form, {k: gates[k].get("passed")
                     for k in ("load", "health", "determinism", "identity")},
              "overall", gates["overall"], flush=True)
    out["overall_passed"] = overall
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")
    print("overall_passed", overall, out["elapsed_s"], "s", flush=True)
    return out


if __name__ == "__main__":
    main()
