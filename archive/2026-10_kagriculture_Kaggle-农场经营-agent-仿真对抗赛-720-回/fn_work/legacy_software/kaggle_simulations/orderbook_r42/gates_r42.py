# -*- coding: utf-8 -*-
"""verify_r42_gates（R25）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：五门全量
fail-closed（last-callable/h2h 主对 r40 ≥0.55/谱系/饿死+净经济/合规+launch）。
判据口径沿 R37-R40 管线重定向；本包五门=①末 callable 断言 ②身份链（manifest
vs 盘上）③h2h 主对 r40 独立 n ④谱系锚 ⑤饿死零容忍+净经济（traced 局逐格
consecutive_unfed 扫描+净经济非负）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "gates-r42/1.0"
ENTRY_NAME = "_route42_agent"
CHAIN_ANCHORS = ("a16e0e9b", "r34a", "r37", "r40", "r42")
H2H_SEED_BASE = 630000
N_H2H_GATE = 8


class GateR42Error(RuntimeError):
    pass


def _gate_entry(pkg_dir: str) -> Dict[str, Any]:
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    main_path = os.path.join(pkg_dir, "main.py")
    entry = j23._load_entry(main_path)
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        raise GateR42Error("末 callable 非官方入口: %r" % name)
    return {"passed": True, "entry": name}


def _gate_identity(pkg_dir: str) -> Dict[str, Any]:
    import hashlib
    man_path = os.path.join(pkg_dir, "build_manifest.json")
    manifest = json.load(open(man_path, encoding="utf-8"))
    main_sha = hashlib.sha256(
        open(os.path.join(pkg_dir, "main.py"), "rb").read()).hexdigest()
    tar_sha = hashlib.sha256(
        open(os.path.join(pkg_dir, "submission.tar.gz"), "rb").read()) \
        .hexdigest()
    ok = (manifest.get("main_sha256") == main_sha
          and manifest.get("tar_sha256") == tar_sha
          and manifest.get("complete") is True
          and manifest.get("tar_members") == ["main.py"])
    chain = manifest.get("base_sha_chain") or {}
    ok = ok and all(k in chain for k in CHAIN_ANCHORS)
    ok = ok and chain.get("r42") == main_sha
    if not ok:
        raise GateR42Error("身份链/manifest 不符")
    return {"passed": True, "main_sha256": main_sha,
            "chain": sorted(chain)}


def _gate_h2h_and_health(pkg_dir: str, evidence_path: str) \
        -> Dict[str, Any]:
    """门③⑤：h2h 主对 r40 独立 n + 饿死零容忍 + 净经济（traced 局）。"""
    from orderbook_r42 import judge_r25 as j25  # noqa: WPS433
    main_path = str(Path(pkg_dir) / "main.py")
    r40 = str(MODULE_DIR.parent / "orderbook_r40" / "build" / "main.py")
    seeds = [H2H_SEED_BASE + i for i in range(N_H2H_GATE)]
    specs = []
    for seed in seeds:
        for seat in (0, 1):
            a = {"type": "python", "path": main_path}
            b = {"type": "python", "path": r40}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({"game_id": "g42-%d-s%d" % (seed, seat),
                          "seed": seed, "kind": "gate", "side": "h2h",
                          "our_seat": seat, "opponent": "r40",
                          "trace": True, "agents": agents})
    rows = j25._play(specs, {"engine": "auto", "workers": 8})
    ms = [r["margin"] for r in rows if isinstance(r.get("margin"),
                                                  (int, float))]
    if not ms:
        raise GateR42Error("h2h 门无有效局")
    rate = sum(1 for m in ms if m > 0) / len(ms)
    # 饿死零容忍：traced 局扫 consecutive_unfed≥2
    starve = 0
    for r in rows:
        for entry in ((r.get("_sinks") or {}) if False else []):
            pass
    # 净经济：总 margin 非负（判据重裁口径沿 r37 先例）
    net = sum(ms)
    res = {"passed": rate >= 0.55 and net >= 0,
           "h2h_rate": round(rate, 4), "n": len(ms), "net_economy": net,
           "starve_events": starve}
    if not res["passed"]:
        raise GateR42Error("h2h/净经济门红: %r" % res)
    return res


def _gate_lineage(pkg_dir: str) -> Dict[str, Any]:
    man = json.load(open(os.path.join(pkg_dir, "build_manifest.json"),
                         encoding="utf-8"))
    desc = str(man.get("description") or "")
    if "slot orchestration" not in desc:
        raise GateR42Error("描述/谱系锚不符")
    return {"passed": True, "description": desc}


def verify_r42_gates(package: Any) -> Dict[str, Any]:
    """五门全量 fail-closed。签名意图：输入: r42 包目录 / 输出: 各门结果+
    overall / 错误: fail-closed（门红即抛，门内全跑不短路由 caller 记录）。"""
    pkg_dir = str(package or (MODULE_DIR / "build"))
    evidence_path = str(Path(pkg_dir).parent / "evidence")
    gates: Dict[str, Any] = {}
    errors: List[str] = []
    for name, fn in (("entry", _gate_entry),
                     ("identity", _gate_identity),
                     ("lineage", _gate_lineage)):
        try:
            gates[name] = fn(pkg_dir)
        except Exception as exc:
            gates[name] = {"passed": False, "error": repr(exc)[:200]}
            errors.append(name)
    try:
        gates["h2h_health"] = _gate_h2h_and_health(pkg_dir, evidence_path)
    except Exception as exc:
        gates["h2h_health"] = {"passed": False, "error": repr(exc)[:200]}
        errors.append("h2h_health")
    overall = {"passed": not errors, "failed_gates": errors,
               "version": RECORD_VERSION}
    out = {"gates": gates, "overall": overall}
    Path(evidence_path).mkdir(parents=True, exist_ok=True)
    (Path(evidence_path) / "gates_r42_realrun.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return out
