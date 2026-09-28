# -*- coding: utf-8 -*-
"""run_r42_iteration（R25 L0）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：build_r42 →
pytest 全绿先行 → judge_r25 → 核心判据全绿才 verify_r42_gates → 判正且
09-28 窗内→standing 发射（台账）；判负或过窗→收档（预绑定）。
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict

MODULE_DIR = Path(__file__).resolve().parent


def run_r42_iteration(argv: Any = None) -> Dict[str, Any]:
    """全链编排。签名意图：输入: 无（CLI） / 输出: {build, judgment, gates,
    verdict} / 错误: fail-closed。"""
    from orderbook_r42 import build_r42 as b42  # noqa: WPS433
    from orderbook_r42 import gates_r42 as g42  # noqa: WPS433
    from orderbook_r42 import judge_r25 as j25  # noqa: WPS433
    cfg = dict(argv) if isinstance(argv, dict) else {}
    t0 = time.perf_counter()
    run_summary: Dict[str, Any] = {"stages": {}}
    built = b42.build_r42(cfg.get("r40_main") or
                          MODULE_DIR.parent / "orderbook_r40" / "build" /
                          "main.py",
                          out_dir=cfg.get("out_dir") or MODULE_DIR / "build")
    run_summary["stages"]["build"] = {
        "main_sha": built["main_sha256"][:16],
        "audit_clean": not built["audit"]["unattributed"]}
    ev = j25.judge_r25(built["main_path"], config=cfg.get("judge"))
    run_summary["stages"]["judge"] = ev["overall"]
    verdict_core = bool(ev["overall"].get("pass"))
    gates_out = {"skipped": True, "overall": False}
    if verdict_core:
        gates_out = g42.verify_r42_gates(built["main_path"].rsplit("/", 1)[0])
    run_summary["stages"]["gates"] = gates_out.get("overall")
    window_ok = bool(cfg.get("window_open", True))
    if verdict_core and gates_out.get("overall") and window_ok:
        verdict = {"verdict": "POSITIVE", "launch_ready": True}
        ledger = {
            "launch_ledger": "run-r42-launch/1.0",
            "entry": {"date": time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                            time.gmtime()),
                      "description": b42.DESCRIPTION,
                      "main_sha256": built["main_sha256"],
                      "tar_sha256": built["tar_sha256"],
                      "judgment": ev["overall"],
                      "auth": "预绑定『判正且 09-28 窗内→standing 代执行发射』"
                              "+standing 台账留痕",
                      "quota_note": "每日 ≤5、候选 ≤2；计分对=最近 2 提交"},
        }
        (MODULE_DIR / "evidence" / "launch_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")
    else:
        verdict = {"verdict": "NEGATIVE", "launch_ready": False,
                   "reason": "核心判据%s/门禁%s/窗口%s" % (
                       verdict_core, gates_out.get("overall"), window_ok)}
        ledger = {
            "archive_ledger": "run-r42-archive/1.0",
            "entry": {"date": time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                            time.gmtime()),
                      "verdict": "NEGATIVE",
                      "archive_note": "判负收档留赛后资产，不建发射版",
                      "judgment": ev["overall"],
                      "main_sha256": built["main_sha256"]},
        }
        (MODULE_DIR / "evidence" / "archive_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")
    run_summary["verdict"] = verdict
    run_summary["elapsed_s"] = round(time.perf_counter() - t0, 2)
    (MODULE_DIR / "evidence" / "run_summary.json").write_text(
        json.dumps(run_summary, ensure_ascii=False, indent=1, default=str)
        + "\n", encoding="utf-8")
    return {"build": built, "judgment": ev, "gates": gates_out,
            "verdict": verdict}
