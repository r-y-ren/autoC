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
LEDGER_RECORDS = ("archive_ledger.json", "launch_ledger.json",
                  "run_summary.json")


def write_record(path: Any, payload: Dict[str, Any]) -> Path:
    """收档件只读守卫（09-28 证据覆写事故教训，判决机器台账写点单口径）。

    台账/汇总收档件（archive_ledger/launch_ledger/run_summary）已存在即视为
    已收档——拒绝写入（模板占位/新跑数据不得覆写历史判决证据）；需要重跑时
    先收档（git 记录）再移除旧件。新写落盘后置只读（0o444，收档件转只读）。
    测试一律经 evidence_dir 把写路径钉死在 tmp（写面隔离）。
    """
    p = Path(path)
    if p.name in LEDGER_RECORDS and p.exists():
        raise RuntimeError("收档件只读：%s 已存在，拒绝覆写历史判决台账" % p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1,
                           default=str) + "\n", encoding="utf-8")
    try:
        p.chmod(0o444)
    except OSError:
        pass
    return p


def run_r43_iteration(argv: Any = None) -> Dict[str, Any]:
    """全链编排。签名意图：输入: 无（CLI）/组件开关 / 输出: {build,
    judgment, gates, verdict} / 错误: fail-closed。"""
    from orderbook_r43 import build_r43 as b43  # noqa: WPS433
    from orderbook_r43 import gates_r43 as g43  # noqa: WPS433
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
    cfg = dict(argv) if isinstance(argv, dict) else {}
    t0 = time.perf_counter()
    ev_dir = Path(cfg.get("evidence_dir") or MODULE_DIR / "evidence")
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
        write_record(ev_dir / "launch_ledger.json", ledger)
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
        write_record(ev_dir / "archive_ledger.json", ledger)
    return {"build": full, "judgment": ev, "gates": gates_out,
            "verdict": verdict,
            "elapsed_s": round(time.perf_counter() - t0, 2)}
