# -*- coding: utf-8 -*-
"""gates_v89：v89_pure / v89_full 四门体检（gates_oppcond 同口径；不发射）。

四门 × 形态：
①装载 last-callable（v89_pure=gated_fixed_sell_agent / v89_full=_hs_agent）
②双席 DONE+单步<1s（seeds 101/102 官方 kaggriculture 引擎完整局，turns=720）
③确定性双跑（同 seed 重跑动作流 sha256 一致）
④体积<100MB+sha 身份（tar 成员恰 ['main.py']、内层 main 与盘上一致、
   sha 对 build_manifest、V89 基座字节前缀恒等；v89_pure 期望字节恒等 V89）。
门内全跑不短路；任一红→overall 红。复用（不改写）：
gate_launch_fourgate_l1._redirect_check（换包重定向）。
只写 orderbook_v89_lab/build/<form>/evidence/ 与 evidence/gates_v89.json。
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
for p in (KSIM, os.path.join(KSIM, "orderbook_l1_derivative")):
    if p not in sys.path:
        sys.path.insert(0, p)

RECORD_VERSION = "v89-gates/1.0"
STEP_BUDGET_MS = 1000.0
EPISODE_SEEDS = (101, 102)
SIZE_CAP_BYTES = 100 * 1024 * 1024
BUILD = MODULE_DIR / "build"
EVID_PATH = MODULE_DIR / "evidence" / "gates_v89.json"
FORMS = {"v89_pure": "gated_fixed_sell_agent", "v89_full": "_hs_agent"}


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _redirect(pkg: Path):
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(str(pkg))
    check.DERIV_MAIN = str(pkg / "main.py")
    check.OUT_DIR = str(pkg / "evidence")
    check.TMP_DIR = str(pkg / "evidence" / "tmp_launch")
    return check


def _gate_load(pkg: Path, expected_entry: str):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(str(pkg / "main.py"))
    name = getattr(entry, "__name__", "")
    if name != expected_entry:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, expected_entry)}
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


def _gate_identity(pkg: Path, form: str, base_bytes: bytes):
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = (hashlib.sha256(main_bytes).hexdigest() == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest() == man.get("tar_sha256"))
    prefix_ok = main_bytes.startswith(base_bytes)
    is_base = main_bytes == base_bytes
    expect_base = (form == "v89_pure")
    ok = all([size_ok, members_ok, inner_ok, sha_ok, prefix_ok,
              is_base == expect_base])
    return {"passed": ok,
            "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok,
            "v89_base_prefix_identical": prefix_ok,
            "byte_identical_to_v89_base": is_base,
            "expect_byte_identical": expect_base,
            "v89_base_sha256": hashlib.sha256(base_bytes).hexdigest()}


def main():
    t0 = time.perf_counter()
    forms = [a for a in sys.argv[1:] if a in FORMS] or list(FORMS)
    base_bytes = (BUILD / "v89_pure" / "main.py").read_bytes()
    out = {"version": RECORD_VERSION,
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "forms": {}, "overall_passed": True,
           "budget": {"gate_episodes": 0}}
    if EVID_PATH.exists():
        try:
            old = json.loads(EVID_PATH.read_text(encoding="utf-8"))
            out["forms"] = old.get("forms") or {}
            out["budget"] = old.get("budget") or out["budget"]
        except Exception:
            pass
    for form in forms:
        entry = FORMS[form]
        pkg = BUILD / form
        res = {"load": _gate_load(pkg, entry),
               "health": _gate_health(pkg),
               "determinism": _gate_determinism(pkg),
               "identity": _gate_identity(pkg, form, base_bytes)}
        out["budget"]["gate_episodes"] = int(
            out["budget"].get("gate_episodes") or 0) + 4
        res["passed"] = all(g.get("passed") for g in res.values()
                           if isinstance(g, dict))
        out["forms"][form] = res
        print(form, {k: v.get("passed") for k, v in res.items()
                     if isinstance(v, dict)}, flush=True)
    out["overall_passed"] = all(r.get("passed")
                                for r in out["forms"].values())
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    MODULE_DIR.joinpath("evidence").mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("overall:", out["overall_passed"], "->", EVID_PATH, flush=True)
    return out


if __name__ == "__main__":
    main()
