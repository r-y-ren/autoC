# -*- coding: utf-8 -*-
"""gates_strongest：三形态四门体检（gates_r44 同口径；判决先行·不发射）。

四门：①装载 last-callable（末 callable=_hs_agent）②双席 DONE+单步<1s（seeds
101/102 官方 kaggriculture 引擎完整局，每步 <1000ms）③确定性双跑逐字节（同
seed 重跑动作流 sha256 一致）④体积<100MB+sha 身份（tar 成员恰 ['main.py']、
内层 main 与盘上一致、sha 对 build_manifest、H 基座字节前缀恒等）。

复用（不改写）：②③=orderbook_l1_derivative/gate_launch_fourgate_l1._redirect_check
（四门单实现 v48_derivative_launch_check 换包重定向）+ check.run_full_episode；
①=orderbook_r40/judge_r23._load_entry（官方 last-callable 语义）。门内全跑
不短路；任一门异常→该门 {passed:False, error}，overall 必红。只写
orderbook_strongest_lab/（build/<form>/evidence 与 evidence/）。
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

RECORD_VERSION = "gates-strongest/1.0"
ENTRY_NAME = "_hs_agent"
STEP_BUDGET_MS = 1000.0
EPISODE_SEEDS = (101, 102)
SIZE_CAP_BYTES = 100 * 1024 * 1024
FORMS = ("h0", "placebo", "h1", "h12")
INJECTED_FORMS = ("placebo", "h1", "h12")


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _base_bytes():
    import tarfile as _tf
    tar_path = os.path.join(KSIM, "orderbook_haodou_adopt", "submission.tar.gz")
    with _tf.open(tar_path, mode="r:gz") as tar:
        return tar.extractfile("main.py").read()


def _gate_load(pkg, form):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(os.path.join(pkg, "main.py"))
    name = getattr(entry, "__name__", "")
    if form in INJECTED_FORMS and name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
    if form == "h0" and not name:
        return {"passed": False, "error": "h0 末 callable 空"}
    return {"passed": True, "entry": name}


def _run_episode(pkg, seed):
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(pkg)
    return check.run_full_episode(int(seed))


def _gate_health(pkg):
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


def _gate_determinism(pkg):
    e1 = _run_episode(pkg, EPISODE_SEEDS[0])
    e2 = _run_episode(pkg, EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": ok, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity(pkg, form):
    main_bytes = open(os.path.join(pkg, "main.py"), "rb").read()
    tar_bytes = open(os.path.join(pkg, "submission.tar.gz"), "rb").read()
    man = json.load(open(os.path.join(pkg, "build_manifest.json")))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = main_sha == man.get("main_sha256")
    base = _base_bytes()
    prefix_ok = main_bytes.startswith(base)
    if form == "h0":
        id_ok = main_bytes == base        # 原样重打包=字节恒等
    else:
        id_ok = main_bytes != base and len(main_bytes) > len(base)  # 注入尾块
    ok = all([size_ok, members_ok, inner_ok, sha_ok, prefix_ok, id_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok,
            "base_prefix_identical": prefix_ok,
            "byte_identical_to_H": main_bytes == base,
            "base_main_sha256": hashlib.sha256(base).hexdigest()}


def main():
    os.chdir(MODULE_DIR)
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": ["python3 orderbook_strongest_lab/build_strongest.py",
                                "python3 orderbook_strongest_lab/gates_strongest.py"],
                   "episode_seeds": list(EPISODE_SEEDS)},
        "forms": {},
    }
    overall_ok = True
    for form in FORMS:
        pkg = os.path.join(str(MODULE_DIR), "build", form)
        os.makedirs(os.path.join(pkg, "evidence"), exist_ok=True)
        res = {}
        for gname, fn in (("load", lambda p=pkg, f=form: _gate_load(p, f)),
                          ("health", lambda p=pkg: _gate_health(p)),
                          ("determinism", lambda p=pkg: _gate_determinism(p))):
            try:
                res[gname] = fn()
            except Exception as exc:
                res[gname] = {"passed": False, "error": repr(exc)[:200]}
        try:
            res["identity"] = _gate_identity(pkg, form)
        except Exception as exc:
            res["identity"] = {"passed": False, "error": repr(exc)[:200]}
        passed = all(g.get("passed") for g in res.values())
        overall_ok = overall_ok and passed
        res["overall"] = passed
        out["forms"][form] = res
        print(form, "gates:", {k: v.get("passed") for k, v in res.items()
                               if k != "overall"}, "overall", passed, flush=True)
        if not res["health"].get("passed"):
            print("  health detail:", json.dumps(res["health"].get("episodes"),
                                                 default=str), flush=True)
    out["overall_passed"] = overall_ok
    (MODULE_DIR / "evidence" / "gates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("OVERALL gates passed:", overall_ok, flush=True)


if __name__ == "__main__":
    main()
