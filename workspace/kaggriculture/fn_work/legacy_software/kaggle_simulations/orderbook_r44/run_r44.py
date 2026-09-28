# -*- coding: utf-8 -*-
"""run_r44_iteration（R27 L0）：全链编排（任一红→收档，预绑定）。

责任契约（fn_docs/hybrid/responsibility.md【R27 增补】）：build_r44_variant
产三形态件（A/B/AB）→ pytest 全绿（R27 ①）→ judge_r44 三形态同局配对+单件
消融+安慰剂 → pick_launch_form 择优 → verify_r44_gates 五门（对选定形态）
→ 判正→standing 发射（台账留痕+计分对核对）；任一红→收档（预绑定）。
输出 {build×3, judgment, launch_form, gates, verdict}；fail-closed。

发射面：发射动作不在本批实现（launch=人工/后续执行面）；本编排到「交发射
（台账）」为止。计分对纪律：本件=第 2 发，挤 r37 保 r40→对={r34a-new
56637411, 本件}。
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
_KSIM = str(MODULE_DIR.parent)
if _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

RECORD_VERSION = "run-r44/1.0"
FORMS = ("A", "B", "AB")
DESCRIPTIONS = {
    "A": "public derivative with day-high realization",
    "B": "public derivative with glut gate",
    "AB": "public derivative with day-high realization / glut gate"}


def _run_pytest(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """R27 ① 构造面全绿门：子进程跑 orderbook_r44 测试面，全绿才放行。"""
    target = str(cfg.get("pytest_target") or MODULE_DIR)
    cmd = [str(c) for c in (cfg.get("pytest_cmd")
                            or [sys.executable, "-m", "pytest", target,
                                "-q"])]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              cwd=str(MODULE_DIR))
    except Exception as exc:
        return {"passed": False, "cmd": cmd, "error": repr(exc)[:200]}
    return {"passed": proc.returncode == 0, "returncode": proc.returncode,
            "cmd": cmd, "tail": (proc.stdout or proc.stderr or "")[-400:]}


def run_r44_iteration(config: Any = None) -> Dict[str, Any]:
    """全链编排。签名意图：输入: 无（CLI）+形态/参数配置 / 输出: {build,
    judgment, launch_form, gates, verdict} / 错误: fail-closed。"""
    from orderbook_r44 import build_r44 as b44  # noqa: WPS433
    from orderbook_r44 import gates_r44 as g44  # noqa: WPS433
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    cfg = dict(config) if isinstance(config, dict) else {}
    t0 = time.perf_counter()
    r40_main = str(cfg.get("r40_main") or _KSIM + "/orderbook_r40/build/"
                   "main.py")
    out_root = Path(cfg.get("out_root") or _KSIM)
    ev_dir = Path(cfg.get("evidence_dir") or MODULE_DIR / "evidence")

    build: Dict[str, Any] = {}
    tests: Dict[str, Any] = {"skipped": True}
    judgment: Dict[str, Any] = {"skipped": True}
    launch: Dict[str, Any] = {"skipped": True}
    gates_out: Dict[str, Any] = {"skipped": True,
                                 "overall": {"passed": False}}
    reason = None

    # 阶段①构建×3（A/B/AB）
    try:
        for form in FORMS:
            out_dir = Path(cfg.get("out_dirs", {}).get(form)
                           if cfg.get("out_dirs") else
                           out_root / ("orderbook_r44_" + form.lower()))
            res = b44.build_r44_variant(r40_main, form, str(out_dir))
            if not isinstance(res, dict) or not res.get("main_path"):
                raise RuntimeError("build_r44_variant 返回缺 main_path: %r"
                                   % (res,))
            build[form] = dict(res)
            build[form].setdefault("out_dir", str(out_dir))
            build[form].setdefault("description", DESCRIPTIONS[form])
    except Exception as exc:
        reason = "build: %s" % repr(exc)[:200]

    # 阶段②pytest 全绿（R27 ①）
    if reason is None:
        tests = _run_pytest(cfg)
        if not tests.get("passed"):
            reason = "pytest 未全绿: returncode=%r" % tests.get("returncode")

    # 阶段③判决+择优
    if reason is None:
        try:
            packages = {f: str(build[f]["main_path"]) for f in FORMS}
            judgment = j44.judge_r44(
                packages, cfg.get("corpus"),
                dict(cfg.get("judge") or {}, r40_main=r40_main,
                     evidence_path=str(ev_dir / "judge_r44_realrun.json")))
            launch = j44.pick_launch_form(judgment)
        except Exception as exc:
            reason = "judgment: %s" % repr(exc)[:200]

    # 阶段④五门（对选定形态）
    if reason is None:
        if judgment.get("verdict") != "POSITIVE" \
                or not launch.get("launch_form"):
            reason = "判决未正/无发射形态: verdict=%r launch=%r" % (
                judgment.get("verdict"), launch.get("launch_form"))
        else:
            try:
                pkg_dir = build[launch["launch_form"]].get("out_dir") or str(
                    Path(build[launch["launch_form"]]["main_path"]).parent)
                gates_out = g44.verify_r44_gates(pkg_dir)
                if not (gates_out.get("overall") or {}).get("passed"):
                    reason = "门禁红: %r" % (gates_out.get("overall"),)
            except Exception as exc:
                reason = "gates: %s" % repr(exc)[:200]
                gates_out = {"skipped": False,
                             "overall": {"passed": False},
                             "error": repr(exc)[:200]}

    # 判正→standing 发射（台账+计分对核对）；任一红→收档（预绑定）
    selected = launch.get("launch_form")
    date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    judgment_brief = {k: judgment.get(k) for k in
                      ("arms", "criteria", "verdict")}
    ev_dir.mkdir(parents=True, exist_ok=True)
    if reason is None:
        verdict = {"verdict": "POSITIVE", "launch_ready": True,
                   "launch_form": selected,
                   "scoring_pair": launch.get("scoring_pair"),
                   "auth": "预绑定『判正→standing 发射』+台账留痕+计分对"
                           "核对；发射动作交人工/后续执行面（本批不实施）"}
        ledger = {"launch_ledger": "run-r44-launch/1.0",
                  "entry": {"date": date, "form": selected,
                            "description": build[selected].get("description"),
                            "main_sha256": build[selected].get("main_sha256"),
                            "tar_sha256": build[selected].get("tar_sha256"),
                            "judgment": judgment_brief,
                            "gates": gates_out.get("overall"),
                            "scoring_pair": launch.get("scoring_pair"),
                            "auth": verdict["auth"]}}
        (ev_dir / "launch_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")
    else:
        verdict = {"verdict": "NEGATIVE", "launch_ready": False,
                   "reason": reason, "launch_form": selected}
        ledger = {"archive_ledger": "run-r44-archive/1.0",
                  "entry": {"date": date, "verdict": "NEGATIVE",
                            "archive_note": "任一红→收档（预绑定）",
                            "reason": reason,
                            "judgment": judgment_brief,
                            "launch_form": selected,
                            "archived_forms": launch.get("archived_forms")}}
        (ev_dir / "archive_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")

    return {"build": build, "judgment": judgment, "launch_form": launch,
            "gates": gates_out, "tests": tests, "verdict": verdict,
            "elapsed_s": round(time.perf_counter() - t0, 2)}
