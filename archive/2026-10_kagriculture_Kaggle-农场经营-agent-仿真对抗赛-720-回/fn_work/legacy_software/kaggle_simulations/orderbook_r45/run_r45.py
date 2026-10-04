# -*- coding: utf-8 -*-
"""run_r45_iteration（R28 指挥线：全链编排+读数门）。

责任契约（fn_docs/hybrid/responsibility.md【R28 增补】）：build_r45 产 r45
件（三件套白名单 diff 审计）→ pytest 全绿（R28 ①）→ judge_r45（镜像压力
板+反制臂+26 败局重演+胜局对照）→ 五判据核对 → 全绿才 verify_r45_gates
五门 → **读数门**（09-29 晨计分对两件中最低收敛 ≥1656 才交 standing 发射，
台账留痕；否则收档赛后资产）。错误: fail-closed（任一阶段红→NEGATIVE+
收档，不发射）。

发射动作留 CLI 缝：本编排只到"交 standing 发射（台账）"，实际提交由
kaggle CLI/standing 代执行（launch_decision.next_cli 登记）。
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "run-r45/1.0"
READING_GATE_BAR = 1656.0       # 09-29 晨计分对两件中最低收敛门槛（定桩）
DEFAULT_BASE_MAIN = (MODULE_DIR.parent / "orderbook_r40" / "build" / "main.py")
DEFAULT_OUT = MODULE_DIR / "build"
DEFAULT_EVIDENCE = MODULE_DIR / "evidence"
# 缺省 R28 ① 命令级测试面（含 B47 advance 层；可经 pytest_args 覆写）
DEFAULT_PYTEST_ARGS = ["-q", "test_build_r45.py", "test_judge_r45.py",
                       "test_gates_r45.py", "test_run_r45.py",
                       "test_advance_agent.py"]
# 透传 judge_r45 的扁平配置键（"judge" 子dict 优先）
_JUDGE_FORWARD = ("runner", "traces", "ledger", "baseline_realized_px",
                  "groups", "counter_config", "n_seeds", "seed_base",
                  "r40_main", "control", "source")


def run_r45_iteration(config=None):
    """编排：build_r45→pytest 全绿（R28①）→judge_r45→五判据→verify_r45_gates
    →读数门（09-29 晨计分对最低≥1656 才交 standing 发射[台账]，否则收档）。
    签名意图：输入: 无（CLI）+参数配置 / 输出: {build, judgment, gates, verdict,
    launch_decision} / 错误: fail-closed。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    t0 = time.perf_counter()
    ev_dir = Path(str(cfg.get("evidence_dir") or DEFAULT_EVIDENCE))
    base_main = str(cfg.get("base_main") or DEFAULT_BASE_MAIN)
    out_dir = str(cfg.get("out_dir") or DEFAULT_OUT)
    result: Dict[str, Any] = {
        "build": None, "judgment": None, "gates": None,
        "verdict": None, "launch_decision": None,
    }
    # stop=(reason, gate_info)：任一阶段红即置位，统一走唯一收档出口
    stop = None
    verdict_core = False
    gates_ok = False
    # ---- ①build_r45（三件套白名单 diff 审计；不产出即抛→收档） -----------
    try:
        from orderbook_r45 import build_r45 as b45  # noqa: WPS433
        build = b45.build_r45(base_main, cfg.get("params") or {}, out_dir)
        build.setdefault("ok", True)
        result["build"] = build
    except Exception as exc:
        result["build"] = {"ok": False,
                           "error": "%s: %s" % (type(exc).__name__, exc)}
        stop = ("构建红（三件不齐/审计白名单外/打包不确定）：%s" % exc, None)
    # ---- ②pytest 全绿（R28 ①命令级验收）---------------------------------
    if stop is None:
        if cfg.get("run_pytest", True):
            try:
                pytest_runner = cfg.get("pytest_runner")
                if pytest_runner is not None:
                    res = pytest_runner()
                    if isinstance(res, dict):
                        pytest_out = {"ok": bool(res.get("ok")),
                                      "detail": res}
                    elif isinstance(res, (list, tuple)):
                        pytest_out = {"ok": bool(res[0]),
                                      "detail": res[1] if len(res) > 1 else None}
                    else:
                        pytest_out = {"ok": bool(res), "detail": None}
                else:
                    args = list(cfg.get("pytest_args") or DEFAULT_PYTEST_ARGS)
                    proc = subprocess.run(
                        [sys.executable, "-m", "pytest"] + args,
                        cwd=str(MODULE_DIR), capture_output=True, text=True)
                    pytest_out = {"ok": proc.returncode == 0,
                                  "returncode": proc.returncode,
                                  "tail": (proc.stdout or "")[-400:]}
            except Exception as exc:
                pytest_out = {"ok": False,
                              "error": "%s: %s" % (type(exc).__name__, exc)}
            result["build"]["pytest"] = pytest_out
            if not pytest_out.get("ok"):
                stop = ("pytest 红（R28 ①命令级验收未过）：%s"
                        % json.dumps(pytest_out, default=str)[:200], None)
        else:
            result["build"]["pytest"] = {"ok": True, "skipped": True}
    # ---- ③judge_r45（镜像压力板+反制臂+败局重演+胜局对照）----------------
    if stop is None:
        judge_cfg: Dict[str, Any] = {k: cfg[k] for k in _JUDGE_FORWARD
                                     if k in cfg}
        judge_cfg.update(dict(cfg.get("judge") or {}))
        corpus = judge_cfg.pop("corpus", cfg.get("corpus"))
        judge_cfg.setdefault("evidence_path",
                             str(ev_dir / "judge_r45_realrun.json"))
        try:
            from orderbook_r45 import judge_r45 as j45  # noqa: WPS433
            ev = j45.judge_r45(dict(result["build"]), corpus, judge_cfg)
            result["judgment"] = ev
        except Exception as exc:
            result["judgment"] = {"verdict": "NEGATIVE",
                                  "error": "%s: %s" % (type(exc).__name__, exc)}
            stop = ("判决异常（fail-closed）：%s" % exc, None)
        verdict_core = ((result.get("judgment") or {}).get("verdict")
                        == "POSITIVE")
    # ---- ④verify_r45_gates 五门（判据全绿才跑）--------------------------
    if stop is None and verdict_core:
        pkg = dict(result["build"])
        for key, val in (("runner", cfg.get("runner")),
                         ("r40_main", cfg.get("r40_main")),
                         ("smoke_seeds", cfg.get("smoke_seeds")),
                         ("run_cfg", cfg.get("run_cfg")),
                         ("evidence_dir", str(ev_dir))):
            if val is not None:
                pkg.setdefault(key, val)
        try:
            from orderbook_r45 import gates_r45 as g45  # noqa: WPS433
            result["gates"] = g45.verify_r45_gates(pkg)
        except Exception as exc:
            result["gates"] = {"overall": {"passed": False},
                               "error": "%s: %s" % (type(exc).__name__, exc)}
        gates_ok = bool(((result["gates"] or {}).get("overall") or {})
                        .get("passed"))
    else:
        result["gates"] = {"skipped": True, "overall": {"passed": False}}
    if stop is None and not (verdict_core and gates_ok):
        stop = ("判负/门禁红（判决先行预绑定：判负不发射）：判据%s/门禁%s"
                % (verdict_core, gates_ok), None)
    # ---- ⑤读数门（09-29 晨计分对两件中最低收敛 ≥1656 才发射）------------
    gate_info: Dict[str, Any] = {}
    if stop is None:
        rg = cfg.get("reading_gate") if isinstance(cfg.get("reading_gate"),
                                                   dict) else {}
        threshold = rg.get("threshold", READING_GATE_BAR)
        try:
            threshold = float(threshold)
        except (TypeError, ValueError):
            threshold = READING_GATE_BAR
        readings = rg.get("readings")
        vals: List[float] = []
        if isinstance(readings, dict):
            for val in readings.values():
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    vals.append(float(val))
        gate_info = {"readings": readings, "threshold": threshold,
                     "n_valid": len(vals)}
        if len(vals) < 2:
            # 数据缺失（计分对两件不齐/非数值）→收档（fail-closed）
            stop = ("读数门数据缺失（计分对两件读数不齐）", gate_info)
        else:
            low = min(vals)
            gate_info["min_converged"] = low
            if low < threshold:
                stop = ("读数门未过（计分对最低收敛 %.1f < %.0f）"
                        % (low, threshold), gate_info)
    # ---- 唯一收档出口（fail-closed：不发射，留下一战役资产）--------------
    if stop is not None:
        reason, extra = stop
        decision = {"decision": "ARCHIVE", "reason": reason,
                    "reading_gate": extra or gate_info,
                    "next_cli": "收档赛后资产（不发射）"}
        result["launch_decision"] = decision
        verdict = result.get("verdict") or {}
        if not (verdict_core and gates_ok):
            verdict = {"verdict": "NEGATIVE", "criteria_ok": verdict_core,
                       "gates_ok": gates_ok, "launch_ready": False,
                       "reason": reason}
        else:
            # 判正+五门全绿但读数门未过/数据缺失→仍收档（读数门即保护）
            verdict = {"verdict": "POSITIVE", "criteria_ok": True,
                       "gates_ok": True, "launch_ready": False,
                       "reason": reason}
        result["verdict"] = verdict
        try:
            ev_dir.mkdir(parents=True, exist_ok=True)
            (ev_dir / "archive_ledger.json").write_text(json.dumps({
                "archive_ledger": "run-r45-archive/1.0",
                "entry": {
                    "date": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                    "verdict": verdict.get("verdict"),
                    "reason": reason,
                    "archive_note": "收档留下一战役资产"
                                    "（判负/门红/读数门未过）",
                    "judgment": (result.get("judgment") or {}).get("verdict"),
                    "main_sha256": (result.get("build") or {}).get("main_sha256"),
                }}, ensure_ascii=False, indent=1, default=str) + "\n",
                encoding="utf-8")
            decision["ledger_path"] = str(ev_dir / "archive_ledger.json")
        except Exception:
            pass  # 台账落盘失败不改判（判定已聚合）
        result["elapsed_s"] = round(time.perf_counter() - t0, 2)
        return result
    # ---- 判正+五门全绿+读数门过→交 standing 发射（台账留痕，CLI 缝）------
    low = gate_info.get("min_converged")
    threshold = gate_info.get("threshold", READING_GATE_BAR)
    result["verdict"] = {"verdict": "POSITIVE", "criteria_ok": True,
                         "gates_ok": True, "launch_ready": True,
                         "reason": "五判据全绿+五门全绿+读数门过"}
    decision = {
        "decision": "LAUNCH",
        "reason": "读数门过（计分对最低收敛 %.1f ≥ %.0f）" % (low, threshold),
        "reading_gate": gate_info,
        "action": "交 standing 发射（台账）",
        "next_cli": "standing 代执行（kaggle CLI 提交留 CLI 缝，不在本编排内）",
    }
    result["launch_decision"] = decision
    try:
        ev_dir.mkdir(parents=True, exist_ok=True)
        (ev_dir / "launch_ledger.json").write_text(json.dumps({
            "launch_ledger": "run-r45-launch/1.0",
            "entry": {
                "date": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                "description": ((result["build"].get("manifest") or {})
                                .get("description")),
                "main_sha256": result["build"].get("main_sha256"),
                "tar_sha256": result["build"].get("tar_sha256"),
                "judgment": {k: (result["judgment"] or {}).get(k)
                             for k in ("arms", "criteria", "verdict")},
                "gates": (result["gates"] or {}).get("overall"),
                "reading_gate": gate_info,
                "auth": "判正+五门全绿+读数门 ≥1656——交 standing 发射"
                        "（台账留痕；发射动作留 CLI 缝）",
            }}, ensure_ascii=False, indent=1, default=str) + "\n",
            encoding="utf-8")
        decision["ledger_path"] = str(ev_dir / "launch_ledger.json")
    except Exception:
        pass  # 台账落盘失败不改判（判定已聚合）
    result["elapsed_s"] = round(time.perf_counter() - t0, 2)
    return result
