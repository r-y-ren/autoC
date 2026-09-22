"""等价判据执行器：封装"黄金哈希复验+快照套件复跑+旗关等价探针"三件的调用与结果汇总，输出单页裁决（pass/fail+逐项 name/passed/value），只编排不实现判据本体，任一判据不可执行即整体 fail（fail-closed）。

上游: R1（详见 fn_docs/responsibility.md）

实现要点：
- 默认判据 snapshot_suite：subprocess 跑 <战役根>/snapshot_tests（python -m pytest -q），
  解析末行汇总的 passed/failed/xfailed/xpassed/skipped/errors 计数，与冻结口径严格比对
  （W1 旧树=62 passed+4 xfailed；口径可经 gate_options["snapshot_suite"]["expect"] 覆盖，
  套件规模变更必须显式改口径，不许静默漂移）。可经 {"enabled": False} 显式关闭（skip）。
- 可选判据 flagoff_golden：调 software/scripts/planner_flagoff_golden.py --check 按退出码
  裁决（0=与 v13.8 黄金基线逐字节一致，非 0=旗关等价破坏）；仅在 gate_options 启用时执行，
  启用但不可执行（脚本缺失/golden JSON 缺失/超时）即该项 fail 且整体 fail（fail-closed）；
  本机 golden JSON gitignored 缺失时只要未启用就只是 skip，不算失败。
- gate_options 出现未知判据名 → 该项 fail 且整体 fail（fail-closed，不静默忽略）。
- 一切目标/套件路径经 discover_campaign_roots 发现（R20），模块内零字面战役路径/战役名。
- 裁决结构：{"overall": pass/fail, "criteria": [{name, status(pass/fail/skip), detail,
  values}, ...], "agent_load_path": 溯源, "campaign_root": 溯源}；skip 项的 detail 即原因。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from shared.discover_campaign_roots import (
    RootDiscoveryError,
    discover_campaign_roots,
)

__all__ = ["run_equivalence_gate"]

# W1 旧树冻结口径（fn_docs/responsibility.md R1：快照 62P+4xf）；其余门键缺省期望=0
_DEFAULT_SNAPSHOT_BASELINE = {"passed": 62, "xfailed": 4}
# 参与裁决的门键（skipped 只入 values 不设门：平台性 skip 归 R6 基线职能，不属等价面）
_GATE_KEYS = ("passed", "xfailed", "failed", "xpassed", "errors")
# 判据注册表：默认判据始终在场（可显式关闭），可选判据仅在 gate_options 启用时执行
_KNOWN_CRITERIA = ("snapshot_suite", "flagoff_golden")
# subprocess 超时（秒）：套件实测 ~37s、黄金探针 6 全季自博弈，均给足余量；可经选项覆盖
_SNAPSHOT_TIMEOUT_S = 600
_FLAGOFF_TIMEOUT_S = 1800
# pytest -q 末行汇总形如 "62 passed, 4 xfailed in 36.50s"
_SUMMARY_TOKEN_RE = re.compile(r"(\d+)\s+(passed|failed|xfailed|xpassed|skipped|errors?)\b")
_SUMMARY_DURATION_RE = re.compile(r"\bin\s+\d+(\.\d+)?s")
_COUNT_KEYS = ("passed", "failed", "xfailed", "xpassed", "skipped", "errors")


def _as_options(value):
    """gate_options 判据项归一：dict→原样拷贝；True/None→空选项；False→显式关闭。"""
    if isinstance(value, dict):
        return dict(value)
    return {"enabled": bool(value)}


def _parse_pytest_counts(text):
    """自 pytest -q 输出提取末行汇总计数；无法解析返回 None（调用方 fail-closed）。"""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for line in reversed(lines):
        if not _SUMMARY_DURATION_RE.search(line):
            continue
        tokens = _SUMMARY_TOKEN_RE.findall(line)
        if not tokens:
            continue
        counts = {key: 0 for key in _COUNT_KEYS}
        for number, kind in tokens:
            key = "errors" if kind.startswith("error") else kind
            counts[key] = int(number)
        return counts
    return None


def _criterion_snapshot_suite(campaign_root, options):
    """默认判据：快照安全网套件复跑 + 冻结口径比对（只编排，判据本体在套件内）。"""
    expect = dict(_DEFAULT_SNAPSHOT_BASELINE)
    expect.update(options.get("expect") or {})
    timeout_s = int(options.get("timeout_s") or _SNAPSHOT_TIMEOUT_S)
    suite_dir = campaign_root / "snapshot_tests"
    if not suite_dir.is_dir():
        suite_dir = campaign_root / "fn_work" / "snapshot_tests"  # 2026-09-23 大整合新位
    suite_dir = campaign_root / "fn_work" / "snapshot_tests"  # 2026-09-23 大整合新位
    values = {"suite": str(suite_dir)}
    if not suite_dir.is_dir():
        return "fail", values, "判据不可执行：快照套件目录缺失（fail-closed）"
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(suite_dir), "-q"],
            cwd=str(campaign_root),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return "fail", values, f"判据不可执行：套件超时（>{timeout_s}s，fail-closed）"
    values["exit_code"] = proc.returncode
    counts = _parse_pytest_counts(proc.stdout) or _parse_pytest_counts(proc.stderr)
    if counts is None:
        return "fail", values, "判据不可执行：pytest 汇总行无法解析（fail-closed）"
    values.update(counts)
    deviations = [
        f"{key}={counts.get(key, 0)}≠口径{want}"
        for key, want in sorted(expect.items())
        if counts.get(key, 0) != want
    ] + [
        f"{key}={counts[key]}≠口径0"
        for key in _GATE_KEYS
        if key not in expect and counts.get(key, 0) != 0
    ]
    if deviations:
        return "fail", values, "快照口径偏离: " + ", ".join(deviations)
    summary = ", ".join(f"{key}={counts.get(key, 0)}" for key in _GATE_KEYS)
    return "pass", values, f"快照口径一致（{summary}）"


def _criterion_flagoff_golden(software_root, options):
    """可选判据：旗关黄金哈希复验（--check 退出码语义：0=一致，非 0=破坏）。"""
    script = software_root / "scripts" / "planner_flagoff_golden.py"
    golden = software_root / "exports" / "probes" / "planner_flagoff" / "golden_v138.json"
    values = {"script": str(script), "golden": str(golden)}
    if not script.is_file():
        return "fail", values, "判据不可执行：旗关等价探针脚本缺失（fail-closed）"
    if not golden.is_file():
        return (
            "fail",
            values,
            "判据不可执行：本机 golden JSON 缺失（gitignored 基线未捕获；"
            "启用即 fail-closed，未启用不算失败）",
        )
    timeout_s = int(options.get("timeout_s") or _FLAGOFF_TIMEOUT_S)
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--check"],
            cwd=str(software_root),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return "fail", values, f"判据不可执行：探针超时（>{timeout_s}s，fail-closed）"
    values["exit_code"] = proc.returncode
    out_tail = (proc.stdout.strip().splitlines() or [""])[-1]
    if proc.returncode == 0:
        return "pass", values, f"旗关等价保持: {out_tail}"
    err_tail = (proc.stderr.strip().splitlines() or [""])[-1]
    return "fail", values, f"旗关等价破坏（exit={proc.returncode}）: {out_tail} {err_tail}".strip()


def run_equivalence_gate(agent_load_path, gate_options=None) -> dict:
    """执行等价判据集并输出单页裁决。

    Args:
        agent_load_path: 目标 agent 装载路径（裁决溯源登记；未提供/不存在=fail-closed 项，
            不阻断其余判据执行）。
        gate_options: 判据选项集 {判据名: True/False/{...}}。未知判据名=该项 fail 且整体
            fail；snapshot_suite 项可带 {"expect": {...口径覆盖}, "timeout_s": int,
            "enabled": False}；flagoff_golden 项可带 {"timeout_s": int}。

    Returns:
        {"overall": "pass"|"fail",
         "criteria": [{"name", "status", "detail", "values"}, ...],
         "agent_load_path": str|None, "campaign_root": str|None}
        —— 任一判据 fail（含不可执行/未知判据名）→ overall=fail；skip 不计失败，
        skip 项的 detail 即跳过原因。
    """
    options = dict(gate_options) if gate_options else {}
    unknown_names = [name for name in options if name not in _KNOWN_CRITERIA]
    criteria = []

    try:
        roots = discover_campaign_roots()
    except RootDiscoveryError as exc:
        criteria.append({
            "name": "root_discovery",
            "status": "fail",
            "detail": f"判据不可执行：三根发现失败（fail-closed）: {exc}",
            "values": {},
        })
        return {
            "overall": "fail",
            "criteria": criteria,
            "agent_load_path": None if agent_load_path is None else str(agent_load_path),
            "campaign_root": None,
        }

    # 目标 agent 装载路径溯源（fail-closed 项；不影响其余判据执行与汇报）
    agent_path_text = None
    if agent_load_path is None:
        criteria.append({
            "name": "agent_load_path",
            "status": "fail",
            "detail": "判据不可执行：目标 agent 装载路径未提供（fail-closed）",
            "values": {},
        })
    else:
        agent_path = Path(agent_load_path).expanduser()
        try:
            agent_path = agent_path.resolve()
        except OSError:
            agent_path = Path(agent_load_path).absolute()
        agent_path_text = str(agent_path)
        if not agent_path.exists():
            criteria.append({
                "name": "agent_load_path",
                "status": "fail",
                "detail": f"判据不可执行：目标 agent 装载路径不存在: {agent_path}（fail-closed）",
                "values": {},
            })

    snap_opts = _as_options(options.get("snapshot_suite", True))
    if not snap_opts.get("enabled", True):
        criteria.append({
            "name": "snapshot_suite",
            "status": "skip",
            "detail": "未启用（gate_options 显式关闭默认判据）",
            "values": {},
        })
    else:
        status, values, detail = _criterion_snapshot_suite(
            roots["campaign_root"], snap_opts)
        criteria.append({
            "name": "snapshot_suite", "status": status,
            "detail": detail, "values": values,
        })

    flagoff_opts = _as_options(options.get("flagoff_golden", False))
    if not flagoff_opts.get("enabled", True):
        criteria.append({
            "name": "flagoff_golden",
            "status": "skip",
            "detail": "未启用（可选判据；本机 golden JSON 缺失时未启用不算失败）",
            "values": {},
        })
    else:
        status, values, detail = _criterion_flagoff_golden(
            roots["software_root"], flagoff_opts)
        criteria.append({
            "name": "flagoff_golden", "status": status,
            "detail": detail, "values": values,
        })

    for name in unknown_names:
        criteria.append({
            "name": str(name),
            "status": "fail",
            "detail": "判据不可执行：未知判据名（fail-closed，不静默忽略；"
                      f"已知判据={list(_KNOWN_CRITERIA)}）",
            "values": {},
        })

    overall = "fail" if any(c["status"] == "fail" for c in criteria) else "pass"
    return {
        "overall": overall,
        "criteria": criteria,
        "agent_load_path": agent_path_text,
        "campaign_root": str(roots["campaign_root"]),
    }
