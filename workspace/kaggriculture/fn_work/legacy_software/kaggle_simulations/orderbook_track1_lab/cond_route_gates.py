# -*- coding: utf-8 -*-
"""cond_route_gates：件 C 四门快速体检（gates_strongest 同口径；判决先行·不发射）。

四门：①装载 last-callable（末 callable=_hs_agent）②双席 DONE+单步<1s（seeds
101/102 官方 kaggriculture 引擎完整局，每步 <1000ms）③确定性双跑逐字节（同
seed 重跑动作流 sha256 一致）④体积<100MB+sha 身份（tar 成员恰 ['main.py']、
内层 main 与盘上 c_main 一致、sha 对 build_manifest、H1 基座字节前缀恒等）。

复用（不改写）：②③=orderbook_l1_derivative/gate_launch_fourgate_l1._redirect_check
换包重定向（DERIV_MAIN 指到 build_cond/c_main.py）+ v48_derivative_launch_check
.run_full_episode；①=orderbook_r40/judge_r23._load_entry（官方 last-callable
语义）。门内全跑不短路；任一门异常→该门 {passed: False, error}，overall 必红。
只写 orderbook_track1_lab/build_cond/evidence/。
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

RECORD_VERSION = "cond-route-gates/1.0"
ENTRY_NAME = "_hs_agent"
STEP_BUDGET_MS = 1000.0
EPISODE_SEEDS = (101, 102)
SIZE_CAP_BYTES = 100 * 1024 * 1024
PKG = MODULE_DIR / "build_cond"
C_MAIN = PKG / "c_main.py"
TAR_PATH = PKG / "submission.tar.gz"
MANIFEST_PATH = PKG / "build_manifest.json"
EVID_PATH = PKG / "evidence" / "gates_cond.json"


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _gate_load():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(str(C_MAIN))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
    return {"passed": True, "entry": name}


def _redirect():
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(str(PKG))
    check.DERIV_MAIN = str(C_MAIN)          # 换包：件 C 装载点
    check.OUT_DIR = str(PKG / "evidence")
    check.TMP_DIR = str(PKG / "evidence" / "tmp_launch")
    return check


def _run_episode(seed):
    return _redirect().run_full_episode(int(seed))


def _gate_health():
    eps = [_run_episode(s) for s in EPISODE_SEEDS]
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


def _gate_determinism():
    e1 = _run_episode(EPISODE_SEEDS[0])
    e2 = _run_episode(EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": ok, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity():
    main_bytes = C_MAIN.read_bytes()
    tar_bytes = TAR_PATH.read_bytes()
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    size_ok = len(tar_bytes) < SIZE_CAP_BYTES
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = (main_sha == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest() == man.get("tar_sha256"))
    base = Path(man["base_main"]).read_bytes()
    prefix_ok = main_bytes.startswith(base)
    id_ok = main_bytes != base and len(main_bytes) > len(base)
    ok = all([size_ok, members_ok, inner_ok, sha_ok, prefix_ok, id_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok,
            "base_prefix_identical": prefix_ok,
            "byte_identical_to_H1_base": main_bytes == base,
            "base_main_sha256": hashlib.sha256(base).hexdigest()}


def main():
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": ["python3 orderbook_track1_lab/cond_route_build.py",
                                "python3 orderbook_track1_lab/cond_route_gates.py"],
                   "episode_seeds": list(EPISODE_SEEDS),
                   "pkg": str(PKG)},
        "gates": {},
    }
    for gname, fn in (("load", _gate_load), ("health", _gate_health),
                      ("determinism", _gate_determinism),
                      ("identity", _gate_identity)):
        try:
            out["gates"][gname] = fn()
        except Exception as exc:
            out["gates"][gname] = {"passed": False, "error": repr(exc)[:200]}
        print(gname, out["gates"][gname].get("passed"),
              out["gates"][gname].get("error", ""), flush=True)
    out["overall_passed"] = all(g.get("passed")
                                for g in out["gates"].values())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")
    print("OVERALL gates passed:", out["overall_passed"], flush=True)
    return out


if __name__ == "__main__":
    main()
