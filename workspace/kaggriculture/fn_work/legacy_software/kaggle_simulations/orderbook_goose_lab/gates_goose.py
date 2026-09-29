# -*- coding: utf-8 -*-
"""gates_goose（goose lab）：变体包四门体检（gates_strongest 同口径；不发射）。

四门：①装载 last-callable=_hs_agent（judge_r23._load_entry 官方语义）②双席
DONE+每步<1s（seeds 101/102 官方引擎完整局）③确定性双跑动作流 sha256 一致
④体积/身份：tar 成员恰 ['main.py']、内层=盘上、sha 对 manifest、**写时复制
恒等**（_R108_DATA blob 区间外与 H1 基底逐字节一致——手术只许动 blob）。
门内全跑不短路；任一门异常→{passed:False, error}。
复用（不改写）：orderbook_l1_derivative/gate_launch_fourgate_l1._redirect_check
+ orderbook_r40/judge_r23._load_entry。只写 orderbook_goose_lab/。
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
L1_DIR = KSIM_DIR / "orderbook_l1_derivative"
if str(L1_DIR) not in sys.path:
    sys.path.insert(0, str(L1_DIR))

H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
RECORD_VERSION = "gates-goose/1.0"
ENTRY_NAME = "_hs_agent"
STEP_BUDGET_MS = 1000.0
EPISODE_SEEDS = (101, 102)
SIZE_CAP_BYTES = 100 * 1024 * 1024
_BLOB_RE = re.compile(r"_R108_DATA=json\.loads\(zlib\.decompress\(base64\.b85decode\("
                      r"'([^']+)'\)\)\)")


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _gate_load(pkg):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(os.path.join(pkg, "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
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


def _gate_identity(pkg):
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
    # 写时复制恒等：blob 区间外与 H1 逐字节一致
    base = H1_MAIN.read_bytes()
    mo = _BLOB_RE.search(base.decode("utf-8"))
    mv = _BLOB_RE.search(main_bytes.decode("utf-8"))
    cow_ok = False
    if mo and mv:
        bo, bv = mo.group(1), mv.group(1)
        pre_ok = base[:mo.start(1)] == main_bytes[:mv.start(1)]
        suf_ok = base[mo.end(1):] == main_bytes[mv.end(1):]
        blob_changed = bo != bv
        cow_ok = pre_ok and suf_ok and blob_changed
    ok = bool(size_ok and members_ok and inner_ok and sha_ok and cow_ok)
    return {"passed": ok, "caliber": "写时复制恒等（blob 外逐字节=H1；blob 内替换）",
            "size_ok": size_ok, "tar_bytes": len(tar_bytes),
            "members_ok": members_ok, "inner_ok": inner_ok,
            "manifest_sha_ok": sha_ok, "copy_on_write_ok": cow_ok,
            "main_sha256": main_sha}


def run_gates(pkg):
    out = {}
    for name, fn in (("gate1_load", _gate_load),
                     ("gate2_health", _gate_health),
                     ("gate3_determinism", _gate_determinism),
                     ("gate4_identity", _gate_identity)):
        try:
            out[name] = fn(pkg)
        except Exception as exc:
            out[name] = {"passed": False,
                         "error": "%s: %s" % (type(exc).__name__, exc)}
    out["overall"] = bool(all(out[k].get("passed") for k in out if
                              k.startswith("gate")))
    return out


def main():
    build_dir = HERE / "build"
    results = {}
    for d in sorted(build_dir.iterdir()) if build_dir.is_dir() else []:
        if not (d / "main.py").is_file():
            continue
        t = run_gates(str(d))
        results[d.name] = t
        print(d.name, "overall:", t["overall"],
              {k: v.get("passed") for k, v in t.items()
               if k.startswith("gate")}, flush=True)
    (HERE / "evidence" / "goose_gates.json").write_text(
        json.dumps({"version": RECORD_VERSION, "gates": results},
                   ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return results


if __name__ == "__main__":
    main()
