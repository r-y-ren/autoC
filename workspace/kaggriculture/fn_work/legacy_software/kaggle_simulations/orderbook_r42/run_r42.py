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


def run_r42_iteration(argv: Any = None) -> Dict[str, Any]:
    """全链编排。签名意图：输入: 无（CLI） / 输出: {build, judgment, gates,
    verdict} / 错误: fail-closed。"""
    from orderbook_r42 import build_r42 as b42  # noqa: WPS433
    from orderbook_r42 import gates_r42 as g42  # noqa: WPS433
    from orderbook_r42 import judge_r25 as j25  # noqa: WPS433
    cfg = dict(argv) if isinstance(argv, dict) else {}
    t0 = time.perf_counter()
    ev_dir = Path(cfg.get("evidence_dir") or MODULE_DIR / "evidence")
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
        write_record(ev_dir / "launch_ledger.json", ledger)
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
        write_record(ev_dir / "archive_ledger.json", ledger)
    run_summary["verdict"] = verdict
    run_summary["elapsed_s"] = round(time.perf_counter() - t0, 2)
    write_record(ev_dir / "run_summary.json", run_summary)
    return {"build": built, "judgment": ev, "gates": gates_out,
            "verdict": verdict}
