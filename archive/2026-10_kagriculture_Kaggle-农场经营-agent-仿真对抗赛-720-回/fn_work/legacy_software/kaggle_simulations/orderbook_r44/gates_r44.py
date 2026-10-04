# -*- coding: utf-8 -*-
"""verify_r44_gates（R27）：五门 fail-closed（对选定发射形态全跑不短路）。

责任契约（fn_docs/hybrid/responsibility.md【R27 增补】）：五门——
①装载 last-callable（官方语义；按 manifest.form 断言形态入口名）
②双席 DONE+单步<1s（seeds 101/102 完整局，每步 <1000ms）
③确定性双跑逐字节（同 seed 重跑动作流 sha256 一致）
④体积<100MB+sha 身份链（manifest↔盘上↔tar 成员；base_sha_chain
  …→r34a→r40→r44_*）
⑤h2h 主对 r40 ≥0.55 独立 n（同 seed 双席折叠、席位翻转不双计）。

复用（不改写）：①=orderbook_r40/judge_r23._load_entry（官方 last-callable
语义）；②③=orderbook_l1_derivative/gate_launch_fourgate_l1._redirect_check
（四门单实现 v48_derivative_launch_check 换包重定向）；⑤=orderbook_r43/
judge_r26._play（seated 双席位判决跑口）。错误 fail-closed：任一门异常/红
→该门 {passed: False, error}，overall 必红；全跑不短路。
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tarfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODULE_DIR = Path(__file__).resolve().parent
_KSIM = str(MODULE_DIR.parent)
if _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

RECORD_VERSION = "gates-r44/1.0"
ENTRY_BY_FORM = {"A": "_dayhigh_agent", "B": "_glutgate_agent",
                 "AB": "_glutgate_agent"}     # AB=glutgate 层在外=末 callable
STEP_BUDGET_MS = 1000.0                       # 官方每步 1s 预算
EPISODE_SEEDS = (101, 102)                    # 四门单实现同种子域
SIZE_CAP_BYTES = 100 * 1024 * 1024            # 体积门：<100MB
CHAIN_ANCHORS = ("a16e0e9b", "r34a", "r40")   # 身份链锚（…→r34a→r40→r44_*）
H2H_BAR = 0.55
H2H_SEED_BASE = 670000                        # 独立 n（与判决 660000 错开）
N_H2H_GATE = 8                                # 独立 seed 数（×双席折叠）


class GateR44Error(RuntimeError):
    """门禁 fail-closed 承载。"""


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _pkg_dir(package: Any) -> str:
    p = Path(str(package or (MODULE_DIR / "build")))
    if p.is_file() or p.suffix == ".py":
        p = p.parent
    return str(p)


def _read_manifest(pkg_dir: str) -> Dict[str, Any]:
    path = os.path.join(str(pkg_dir), "build_manifest.json")
    try:
        with open(path, encoding="utf-8") as fh:
            man = json.load(fh)
    except Exception as exc:
        raise GateR44Error("manifest 不可读: %r" % exc)
    if not isinstance(man, dict):
        raise GateR44Error("manifest 非对象")
    return man


def _run_episode(pkg_dir: str, seed: int) -> Dict[str, Any]:
    """单局缝：四门单实现换包重定向（gate_launch_fourgate_l1 先例）。
    返回 {seed, statuses, rewards, max_step_ms, action_stream_sha256, ...}。"""
    l1_dir = os.path.join(_KSIM, "orderbook_l1_derivative")
    if l1_dir not in sys.path:
        sys.path.insert(0, l1_dir)
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(str(pkg_dir))
    return check.run_full_episode(int(seed))


# ---------------------------------------------------------------- 五门 --
def _gate_load(pkg_dir: str) -> Dict[str, Any]:
    """门①官方 last-callable 装载：末 callable 须为 manifest.form 形态入口。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    man = _read_manifest(pkg_dir)
    form = str(man.get("form") or "")
    if form not in ENTRY_BY_FORM:
        raise GateR44Error("manifest.form 缺失/非法: %r" % form)
    entry = j23._load_entry(os.path.join(str(pkg_dir), "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_BY_FORM[form]:
        raise GateR44Error("末 callable 非 %s 形态入口 %s: %r"
                           % (form, ENTRY_BY_FORM[form], name))
    return {"passed": True, "form": form, "entry": name}


def _gate_health(pkg_dir: str) -> Dict[str, Any]:
    """门②双席 DONE+单步<1s：seeds 101/102 完整局全 DONE、每步 <1s、资金有限。"""
    eps = [_run_episode(pkg_dir, s) for s in EPISODE_SEEDS]
    details = []
    ok = True
    for ep in eps:
        statuses = list(ep.get("statuses") or [])
        rewards = list(ep.get("rewards") or [])
        step_ms = ep.get("max_step_ms")
        good = (statuses == ["DONE", "DONE"] and len(rewards) == 2
                and all(_is_num(r) and abs(float(r)) < 1e12 for r in rewards)
                and _is_num(step_ms) and float(step_ms) < STEP_BUDGET_MS)
        ok = ok and good
        details.append({"seed": ep.get("seed"), "statuses": statuses,
                        "max_step_ms": step_ms, "passed": good})
    if not ok:
        raise GateR44Error("双席 DONE/单步预算门红: %r" % details)
    return {"passed": True, "step_budget_ms": STEP_BUDGET_MS,
            "episodes": details}


def _gate_determinism(pkg_dir: str) -> Dict[str, Any]:
    """门③确定性双跑逐字节：同 seed 两次动作流 sha256 必须一致。"""
    e1 = _run_episode(pkg_dir, EPISODE_SEEDS[0])
    e2 = _run_episode(pkg_dir, EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    if not ok:
        raise GateR44Error("确定性双跑不一致: %r vs %r" % (h1, h2))
    return {"passed": True, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity(pkg_dir: str) -> Dict[str, Any]:
    """门④体积<100MB+sha 身份链：manifest↔盘上↔tar 成员逐字节+链锚。"""
    man = _read_manifest(pkg_dir)
    main_bytes = open(os.path.join(str(pkg_dir), "main.py"), "rb").read()
    tar_bytes = open(os.path.join(str(pkg_dir), "submission.tar.gz"),
                     "rb").read()
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    tar_sha = hashlib.sha256(tar_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        members = t.getnames()
        inner = t.extractfile("main.py").read() if members == ["main.py"] \
            else b""
    chain = man.get("base_sha_chain") or {}
    form = str(man.get("form") or "")
    chain_ok = (all(k in chain for k in CHAIN_ANCHORS) and (
        chain.get("r44") == main_sha
        or (form and chain.get("r44_" + form.lower()) == main_sha)))
    ok = (man.get("main_sha256") == main_sha
          and man.get("tar_sha256") == tar_sha
          and (man.get("complete") in (True, None))
          and members == ["main.py"] and inner == main_bytes
          and len(tar_bytes) <= SIZE_CAP_BYTES and chain_ok)
    if not ok:
        raise GateR44Error("身份链/体积/manifest 不符")
    return {"passed": True, "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / (1024 * 1024), 3),
            "chain": sorted(chain)}


def _gate_h2h(pkg_dir: str) -> Dict[str, Any]:
    """门⑤h2h 主对 r40 ≥0.55 独立 n：seated 双席同 seed 配对、翻转折叠。"""
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
    main_path = os.path.join(str(pkg_dir), "main.py")
    r40 = os.path.join(_KSIM, "orderbook_r40", "build", "main.py")
    specs = []
    for i in range(N_H2H_GATE):
        seed = H2H_SEED_BASE + i
        for seat in (0, 1):
            a = {"type": "python", "path": main_path}
            b = {"type": "python", "path": r40}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({"game_id": "g44-%d-s%d" % (seed, seat),
                          "seed": seed, "kind": "gate", "our_seat": seat,
                          "trace": False, "agents": agents})
    rows = j26._play(specs, {"engine": "auto", "workers": 8})
    pairs: Dict[Any, List[Dict[str, Any]]] = {}
    for r in rows or []:
        pairs.setdefault(r.get("seed"), []).append(r)
    wins = losses = ties = 0
    for seed in sorted(pairs):
        rs = pairs[seed]
        ms = [float(r["margin"]) for r in rs if _is_num(r.get("margin"))]
        if len(rs) != 2 or len(ms) != 2:
            losses += 1                     # 缺席/红局→败（fail-closed）
            continue
        score = sum(1.0 if m > 0 else 0.5 if m == 0 else 0.0
                    for m in ms) / 2.0
        if score >= 1.0:
            wins += 1
        elif score <= 0.0:
            losses += 1
        else:
            ties += 1
    n = len(pairs)
    rate = round((wins + 0.5 * ties) / n, 4) if n else 0.0
    res = {"passed": bool(n > 0 and rate >= H2H_BAR), "h2h_rate": rate,
           "bar": H2H_BAR, "n_independent": n, "n_games": len(rows or []),
           "wins": wins, "losses": losses, "ties": ties}
    if not res["passed"]:
        raise GateR44Error("h2h 主对 r40 门红: %r" % res)
    return res


# ---------------------------------------------------------------- 汇总 --
def verify_r44_gates(package: Any) -> Dict[str, Any]:
    """五门 fail-closed 全跑不短路。签名意图：输入: 选定形态包 / 输出:
    各门结果+overall / 错误: fail-closed。"""
    pkg_dir = _pkg_dir(package)
    gates: Dict[str, Any] = {}
    errors: List[str] = []
    for name, fn in (("load", _gate_load), ("health", _gate_health),
                     ("determinism", _gate_determinism),
                     ("identity", _gate_identity), ("h2h", _gate_h2h)):
        try:
            gates[name] = fn(pkg_dir)
        except Exception as exc:
            gates[name] = {"passed": False, "error": repr(exc)[:200]}
            errors.append(name)
    out = {"gates": gates,
           "overall": {"passed": not errors, "failed_gates": errors,
                       "version": RECORD_VERSION}}
    ev_dir = Path(pkg_dir) / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "gates_r44_realrun.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return out
