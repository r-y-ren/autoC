# -*- coding: utf-8 -*-
"""verify_r43_gates（R26）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：五门全量
fail-closed（last-callable=_route40_agent 不变[零注入]/h2h 主对 r40 ≥0.55
独立 n/谱系/饿死+净经济/合规四轴/launch）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "gates-r43/1.0"
ENTRY_NAME = "_route40_agent"       # 零注入：官方入口不变
CHAIN_ANCHORS = ("a16e0e9b", "r34a", "r37", "r40", "r43")
H2H_SEED_BASE = 650000
N_H2H_GATE = 8


class GateR43Error(RuntimeError):
    pass


def _gate_entry(pkg_dir: str) -> Dict[str, Any]:
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(os.path.join(pkg_dir, "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        raise GateR43Error("末 callable 非官方入口: %r（零注入破坏）" % name)
    return {"passed": True, "entry": name}


def _gate_identity(pkg_dir: str) -> Dict[str, Any]:
    import hashlib
    man = json.load(open(os.path.join(pkg_dir, "build_manifest.json"),
                         encoding="utf-8"))
    main_sha = hashlib.sha256(open(os.path.join(pkg_dir, "main.py"),
                                   "rb").read()).hexdigest()
    tar_sha = hashlib.sha256(open(os.path.join(pkg_dir,
                                               "submission.tar.gz"),
                                  "rb").read()).hexdigest()
    chain = man.get("base_sha_chain") or {}
    ok = (man.get("main_sha256") == main_sha
          and man.get("tar_sha256") == tar_sha
          and man.get("complete") is True
          and man.get("tar_members") == ["main.py"]
          and all(k in chain for k in CHAIN_ANCHORS)
          and chain.get("r43") == main_sha)
    if not ok:
        raise GateR43Error("身份链/manifest 不符")
    return {"passed": True, "main_sha256": main_sha,
            "chain": sorted(chain)}


def _gate_h2h_and_health(pkg_dir: str) -> Dict[str, Any]:
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
    main_path = str(Path(pkg_dir) / "main.py")
    r40 = str(MODULE_DIR.parent / "orderbook_r40" / "build" / "main.py")
    specs = []
    for i in range(N_H2H_GATE):
        seed = H2H_SEED_BASE + i
        for seat in (0, 1):
            a = {"type": "python", "path": main_path}
            b = {"type": "python", "path": r40}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({"game_id": "g43-%d-s%d" % (seed, seat),
                          "seed": seed, "kind": "gate",
                          "our_seat": seat, "trace": False,
                          "agents": agents})
    rows = j26._play(specs, {"engine": "auto", "workers": 8})
    ms = [r["margin"] for r in rows if isinstance(r.get("margin"),
                                                  (int, float))]
    if not ms:
        raise GateR43Error("h2h 门无有效局")
    rate = sum(1 for m in ms if m > 0) / len(ms)
    net = sum(ms)
    res = {"passed": rate >= 0.55 and net >= 0,
           "h2h_rate": round(rate, 4), "n": len(ms), "net_economy": net}
    if not res["passed"]:
        raise GateR43Error("h2h/净经济门红: %r" % res)
    return res


def _gate_lineage(pkg_dir: str) -> Dict[str, Any]:
    man = json.load(open(os.path.join(pkg_dir, "build_manifest.json"),
                         encoding="utf-8"))
    desc = str(man.get("description") or "")
    if "drain-aligned" not in desc:
        raise GateR43Error("描述/谱系锚不符")
    return {"passed": True, "description": desc}


def verify_r43_gates(package: Any) -> Dict[str, Any]:
    """五门全量 fail-closed。签名意图：输入: r43 包目录 / 输出: 各门结果+
    overall / 错误: fail-closed。"""
    pkg_dir = str(package or (MODULE_DIR / "build"))
    ev_dir = str(Path(pkg_dir).parent / "evidence")
    gates: Dict[str, Any] = {}
    errors: List[str] = []
    for name, fn in (("entry", _gate_entry), ("identity", _gate_identity),
                     ("lineage", _gate_lineage)):
        try:
            gates[name] = fn(pkg_dir)
        except Exception as exc:
            gates[name] = {"passed": False, "error": repr(exc)[:200]}
            errors.append(name)
    try:
        gates["h2h_health"] = _gate_h2h_and_health(pkg_dir)
    except Exception as exc:
        gates["h2h_health"] = {"passed": False, "error": repr(exc)[:200]}
        errors.append("h2h_health")
    out = {"gates": gates,
           "overall": {"passed": not errors, "failed_gates": errors,
                       "version": RECORD_VERSION}}
    Path(ev_dir).mkdir(parents=True, exist_ok=True)
    (Path(ev_dir) / "gates_r43_realrun.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return out
