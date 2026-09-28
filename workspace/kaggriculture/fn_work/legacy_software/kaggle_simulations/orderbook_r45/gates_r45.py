# -*- coding: utf-8 -*-
"""verify_r45_gates（R28 门禁线）。

责任契约（fn_docs/hybrid/responsibility.md【R28 增补】）：五门 fail-closed
沿管线对 r45 包全跑不短路——①装载（last-callable=_advance_agent）②双席
DONE+单步 <1s ③确定性双跑 ④体积身份链（…→r40→r45）⑤h2h 主对 r40 ≥0.55
（seated 双席位、独立 seed n 报）。

复用（跨批契约）：装载=orderbook_r40/judge_r23._load_entry（官方 last-
callable 语义）；h2h 局跑与 seed 级折叠=orderbook_r45/judge_r45
.run_mirror_counter_judgment（同一实现，席位翻转不双计）；缺省门②③走
orderbook_l1_derivative/gate_launch_fourgate_l1 管线重定向（gate2_gate3），
测试可经 package dict 注入 runner（假局组夹具）。
"""
from __future__ import annotations

import hashlib
import io
import json
import tarfile
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "gates-r45/1.0"
ENTRY_NAME = "_advance_agent"
SIZE_CAP_BYTES = 100 * 1024 * 1024      # 包体上限（门④）
STEP_BUDGET_S = 1.0                     # 单步预算（门② <1s）
SMOKE_SEEDS = (101, 102)                # 双席自打 smoke seeds（r30 管线同款）
H2H_SEED_BASE = 650000
N_H2H_GATE = 8                          # h2h 门独立 seed 数（席位翻转不双计）
H2H_BAR = 0.55
MANIFEST_NAME = "build_manifest.json"
EVIDENCE_NAME = "gates_r45_realrun.json"


def verify_r45_gates(package):
    """五门全跑（装载/双席 DONE+<1s/确定性双跑/体积身份链/h2h 主对 r40≥0.55）。
    签名意图：输入: r45 包 / 输出: 各门+overall / 错误: fail-closed。
    package 收包目录/包 dict（build_r45 输出+可选 runner/r40_main/smoke_seeds
    注入钩子——测试假局组夹具）；五门全跑不短路，任一门异常→该门红（不抛）。"""
    # ---- 包归一 -----------------------------------------------------------
    if isinstance(package, dict):
        pkg = dict(package)
    elif isinstance(package, (str, Path)):
        p = Path(str(package))
        pkg = {"dir": str(p if p.is_dir() else p.parent)}
    elif package is None:
        pkg = {}
    else:
        pkg = {}
    pkg_dir = Path(str(pkg.get("dir") or pkg.get("out_dir")
                            or (MODULE_DIR / "build")))
    main_path = Path(str(pkg.get("main_path") or (pkg_dir / "main.py")))
    runner = pkg.get("runner")
    r40_main = str(pkg.get("r40_main") or (MODULE_DIR.parent
                                           / "orderbook_r40" / "build"
                                           / "main.py"))
    gates: Dict[str, Any] = {}
    failed: List[str] = []
    # ---- 门①装载（last-callable=_advance_agent） --------------------------
    try:
        from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
        entry = j23._load_entry(str(main_path))
        name = getattr(entry, "__name__", "")
        if name != ENTRY_NAME:
            raise RuntimeError("末 callable=%r（应为 %r）" % (name, ENTRY_NAME))
        gates["load"] = {"passed": True, "entry": name,
                         "main_path": str(main_path)}
    except Exception as exc:
        gates["load"] = {"passed": False, "error": repr(exc)[:200]}
        failed.append("load")
    # ---- 门②双席 DONE+<1s / 门③确定性双跑 -------------------------------
    smoke_seeds = pkg.get("smoke_seeds") or list(SMOKE_SEEDS)
    specs: List[Dict[str, Any]] = []
    for seed in smoke_seeds:
        for seat in (0, 1):
            ours = {"type": "python", "path": str(main_path)}
            others = {"type": "python", "path": str(main_path)}
            agents = [ours, others] if seat == 0 else [others, ours]
            specs.append({"game_id": "smoke-%s-s%d" % (seed, seat),
                          "seed": int(seed), "arm": "smoke_selfplay",
                          "kind": "gate", "our_seat": seat, "trace": False,
                          "agents": agents})
    try:
        if runner is not None:
            run1 = list(runner(specs, dict(pkg.get("run_cfg") or {})))
            run2 = list(runner(specs, dict(pkg.get("run_cfg") or {})))
            # 门②：双席 DONE + 单步 <1s（缺字段=fail-closed 红）
            bad = []
            for row in run1:
                ok = (isinstance(row, dict) and row.get("error") is None
                      and list(row.get("statuses") or []) == ["DONE", "DONE"]
                      and isinstance(row.get("max_step_s"), (int, float))
                      and not isinstance(row.get("max_step_s"), bool)
                      and float(row["max_step_s"]) < STEP_BUDGET_S)
                if not ok:
                    bad.append((row or {}).get("game_id")
                               if isinstance(row, dict) else None)
            if not run1:
                bad.append("no_rows")
            gates["seats_done"] = {
                "passed": not bad,
                "n": len(run1), "step_budget_s": STEP_BUDGET_S,
                "bad": bad[:20]}
            if bad:
                failed.append("seats_done")
            # 门③：同 seed 双跑动作流 sha256 逐一致
            sha1 = {r.get("game_id"): r.get("actions_sha256")
                    for r in run1 if isinstance(r, dict)}
            sha2 = {r.get("game_id"): r.get("actions_sha256")
                    for r in run2 if isinstance(r, dict)}
            mismatch = [gid for gid in sorted(set(sha1) | set(sha2),
                                              key=lambda x: str(x))
                        if not sha1.get(gid) or sha1.get(gid) != sha2.get(gid)]
            if not sha1:
                mismatch.append("no_rows")
            gates["determinism"] = {
                "passed": not mismatch, "n": len(sha1),
                "mismatch": mismatch[:20]}
            if mismatch:
                failed.append("determinism")
        else:
            # 缺省走 r30 管线（gate_launch_fourgate_l1 重定向：gate2_gate3）
            from orderbook_l1_derivative import gate_launch_fourgate_l1 as g41  # noqa: WPS433
            check = g41._redirect_check(str(pkg_dir))
            try:
                g23 = check.gate2_gate3()
            finally:
                import shutil as _sh
                _sh.rmtree(check.TMP_DIR, ignore_errors=True)
            done_ok = bool(g23.get("gate2_full_episodes_ok")) and \
                float(g23.get("gate2_step_budget_ms") or 1e9) < 1000.0
            gates["seats_done"] = {
                "passed": done_ok,
                "detail": {k: g23.get(k) for k in
                           ("gate2_full_episodes_ok", "gate2_step_budget_ms")}}
            if not done_ok:
                failed.append("seats_done")
            det_ok = bool(g23.get("gate3_determinism_ok"))
            gates["determinism"] = {
                "passed": det_ok,
                "detail": {k: g23.get(k) for k in
                           ("gate3_determinism_ok", "gate3_hashes")}}
            if not det_ok:
                failed.append("determinism")
    except Exception as exc:
        gates.setdefault("seats_done",
                         {"passed": False, "error": repr(exc)[:200]})
        gates.setdefault("determinism",
                         {"passed": False, "error": repr(exc)[:200]})
        for key in ("seats_done", "determinism"):
            if not gates[key].get("passed") and key not in failed:
                failed.append(key)
    # ---- 门④体积身份链（…→r40→r45） -------------------------------------
    try:
        from orderbook_r45 import build_r45 as b45  # noqa: WPS433
        man_path = pkg_dir / MANIFEST_NAME
        man = json.loads(man_path.read_text(encoding="utf-8"))
        main_bytes = (pkg_dir / "main.py").read_bytes()
        tar_bytes = (pkg_dir / "submission.tar.gz").read_bytes()
        main_sha = hashlib.sha256(main_bytes).hexdigest()
        tar_sha = hashlib.sha256(tar_bytes).hexdigest()
        members: List[str] = []
        inner_ok = False
        with tarfile.open(fileobj=io.BytesIO(tar_bytes),
                          mode="r:gz") as tar:
            members = tar.getnames()
            if members == ["main.py"]:
                inner_ok = tar.extractfile("main.py").read() == main_bytes
        chain = man.get("base_sha_chain") or {}
        checks = {
            "size_cap": len(tar_bytes) <= SIZE_CAP_BYTES,
            "members": members == ["main.py"],
            "inner_main": inner_ok,
            "main_sha": man.get("main_sha256") == main_sha,
            "tar_sha": man.get("tar_sha256") == tar_sha,
            "complete": man.get("complete") is True,
            "chain_anchors": all(k in chain for k in b45.CHAIN_ANCHORS),
            "chain_r45": chain.get("r45") == main_sha,
        }
        ok = all(checks.values())
        gates["identity"] = {"passed": ok, "checks": checks,
                             "main_sha256": main_sha,
                             "chain": sorted(chain)}
        if not ok:
            failed.append("identity")
    except Exception as exc:
        gates["identity"] = {"passed": False, "error": repr(exc)[:200]}
        failed.append("identity")
    # ---- 门⑤h2h 主对 r40 ≥0.55（独立 seed n，席位翻转不双计）-------------
    try:
        from orderbook_r45 import judge_r45 as j45  # noqa: WPS433
        board = {
            "groups": [{"arm": "h2h_r40", "n": N_H2H_GATE,
                        "seeds": [H2H_SEED_BASE + i for i in range(N_H2H_GATE)],
                        "opponent": {"type": "python", "path": r40_main}}],
            "runner": runner,
            "seed_base": H2H_SEED_BASE,
            "run_cfg": dict(pkg.get("run_cfg") or {}),
        }
        board_out = j45.run_mirror_counter_judgment(
            {"main_path": str(main_path)}, board)
        arms = [a for a in (board_out.get("arms") or [])
                if isinstance(a, dict) and a.get("arm") == "h2h_r40"]
        arm = arms[0] if arms else {}
        rate = arm.get("win_rate")
        ok = isinstance(rate, float) and not isinstance(rate, bool) \
            and rate >= H2H_BAR and int(arm.get("n") or 0) > 0
        gates["h2h_vs_r40"] = {
            "passed": ok, "win_rate": rate, "bar": H2H_BAR,
            "n_independent": arm.get("n"), "seats": "seated 双席位",
            "mean_margin": arm.get("mean_margin"),
            "error": arm.get("error")}
        if not ok:
            failed.append("h2h_vs_r40")
    except Exception as exc:
        gates["h2h_vs_r40"] = {"passed": False, "error": repr(exc)[:200]}
        failed.append("h2h_vs_r40")
    out = {"gates": gates,
           "overall": {"passed": not failed, "failed_gates": failed,
                       "version": RECORD_VERSION,
                       "generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                    time.gmtime())}}
    ev_dir = (Path(str(pkg.get("evidence_dir") or (pkg_dir.parent / "evidence"))))
    try:
        ev_dir.mkdir(parents=True, exist_ok=True)
        (ev_dir / EVIDENCE_NAME).write_text(
            json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
            encoding="utf-8")
        out["evidence_path"] = str(ev_dir / EVIDENCE_NAME)
    except Exception:
        pass  # 落盘失败不改判（门结果已聚合）
    return out
