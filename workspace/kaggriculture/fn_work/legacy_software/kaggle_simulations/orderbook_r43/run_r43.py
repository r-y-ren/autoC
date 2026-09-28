# -*- coding: utf-8 -*-
"""run_r43_iteration（R26 L0）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：build_r43（组件
开关）→ pytest 全绿 → judge_r26（安慰剂+消融+配对）→ 全绿才五门 → 判正→
standing 发射（台账）；判负→收档（预绑定）。
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict

MODULE_DIR = Path(__file__).resolve().parent


def run_r43_iteration(argv: Any = None) -> Dict[str, Any]:
    """全链编排。签名意图：输入: 无（CLI）/组件开关 / 输出: {build,
    judgment, gates, verdict} / 错误: fail-closed。"""
    from orderbook_r43 import build_r43 as b43  # noqa: WPS433
    from orderbook_r43 import gates_r43 as g43  # noqa: WPS433
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
    cfg = dict(argv) if isinstance(argv, dict) else {}
    t0 = time.perf_counter()
    r40_main = cfg.get("r40_main") or MODULE_DIR.parent / "orderbook_r40" / \
        "build" / "main.py"
    out_dir = cfg.get("out_dir") or MODULE_DIR / "build"
    full = b43.build_r43(r40_main, out_dir=out_dir, config=cfg)
    arms = {"full": full["main_path"]}
    for arm, comp in (("placebo", {}), ("drain", {"drain": True}),
                      ("gran", {"gran": True}), ("sheep", {"sheep": True})):
        off = {"drain": False, "gran": False, "sheep": False}
        off.update(comp)
        sub = b43.build_r43(r40_main, out_dir=str(
            Path(str(out_dir)) / "ablation" / arm), config=off)
        arms[arm] = sub["main_path"]
    ev = j26.judge_r26(full["main_path"], config=dict(cfg.get("judge") or {},
                                                      arms=arms,
                                                      r40_main=str(r40_main)))
    verdict_core = bool(ev.get("pass"))
    gates_out = {"skipped": True, "overall": False}
    if verdict_core:
        gates_out = g43.verify_r43_gates(str(out_dir))
    window_ok = bool(cfg.get("window_open", True))
    if verdict_core and gates_out.get("overall") and window_ok:
        verdict = {"verdict": "POSITIVE", "launch_ready": True}
        ledger = {"launch_ledger": "run-r43-launch/1.0",
                  "entry": {"date": time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                  time.gmtime()),
                            "description": b43.DESCRIPTION,
                            "main_sha256": full["main_sha256"],
                            "tar_sha256": full["tar_sha256"],
                            "judgment": {k: ev.get(k) for k in
                                         ("arms", "criteria", "pass")},
                            "auth": "预绑定『判正→standing 发射』（max() "
                                    "语义窗口纪律修订已登记）+台账留痕"}}
        (MODULE_DIR / "evidence").mkdir(parents=True, exist_ok=True)
        (MODULE_DIR / "evidence" / "launch_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")
    else:
        verdict = {"verdict": "NEGATIVE", "launch_ready": False,
                   "reason": "判据%s/门禁%s/窗口%s" % (
                       verdict_core, gates_out.get("overall"), window_ok)}
        ledger = {"archive_ledger": "run-r43-archive/1.0",
                  "entry": {"date": time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                  time.gmtime()),
                            "verdict": "NEGATIVE",
                            "archive_note": "判负收档留下一战役资产",
                            "judgment": {k: ev.get(k) for k in
                                         ("arms", "criteria", "pass")},
                            "main_sha256": full["main_sha256"]}}
        (MODULE_DIR / "evidence").mkdir(parents=True, exist_ok=True)
        (MODULE_DIR / "evidence" / "archive_ledger.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=1, default=str)
            + "\n", encoding="utf-8")
    return {"build": full, "judgment": ev, "gates": gates_out,
            "verdict": verdict,
            "elapsed_s": round(time.perf_counter() - t0, 2)}
