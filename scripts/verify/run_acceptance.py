#!/usr/bin/env python3
"""S-05 验收执行器（run_acceptance）。

执行 workspace/blueprint.md 验收清单：
  - 带 cmd 的项：直接执行（shell），退出码判定 pass/fail，输出存证据文件
  - 不带 cmd 的项：manual 类 → pending_manual（移交用户）；其余 → pending（待 acceptor agent 核验）
  - 执行前先跑 merge_metrics.py 生成顶层 metrics.json（分片汇总）
  - 非 pass 结果累计 retry 计数，达到 max 触发熔断标记（升级人工）

产出：workspace/acceptance/run-<N>.json（过 acceptance.schema.json）
退出码：0=pass｜1=fail｜3=pending_*｜2=配置错误
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
STATE = ROOT / ".flow" / "state.json"


def load_blueprint() -> dict | None:
    bp = ROOT / "workspace" / "blueprint.md"
    if not bp.is_file():
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", bp.read_text(encoding="utf-8"), re.S)
    if not m:
        return None
    import yaml
    return yaml.safe_load(m.group(1))


def git_ref() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        return "n/a"


def read_retry() -> dict:
    try:
        st = json.loads(STATE.read_text(encoding="utf-8"))
        return st.get("retry") or {"count": 0, "max": 3, "tripped": False}
    except Exception:  # noqa: BLE001
        return {"count": 0, "max": 3, "tripped": False}


def write_retry(retry: dict) -> None:
    try:
        st = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        st = {}
    st["retry"] = retry
    st["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    st["updated_by"] = "run_acceptance"
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def next_run_no(acc_dir: Path) -> int:
    nums = [int(m.group(1)) for f in acc_dir.glob("run-*.json")
            if (m := re.match(r"run-(\d+)\.json$", f.name))]
    return max(nums, default=0) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description="验收执行器")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    bp = load_blueprint()
    if not bp or not (bp.get("acceptance") or {}).get("checklist"):
        print("[run_acceptance] workspace/blueprint.md 缺失或无 acceptance.checklist", file=sys.stderr)
        return 2

    acc_dir = ROOT / "workspace" / "acceptance"
    checklist = bp["acceptance"]["checklist"]

    if args.dry_run:
        for it in checklist:
            mode = "CMD" if it.get("cmd") else ("MANUAL" if it.get("category") == "manual" else "AGENT")
            print(f"  [{mode:5s}] {it.get('id')}: {it.get('item')}")
        print(f"[run_acceptance] dry-run：{len(checklist)} 项")
        return 0

    # 分片汇总（失败不阻断验收本身，但会体现在证据里）
    merge = ROOT / "scripts" / "verify" / "merge_metrics.py"
    if merge.is_file():
        subprocess.run([sys.executable, str(merge)], capture_output=True, timeout=30)

    ev_dir = acc_dir / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for it in checklist:
        rid, cat = it.get("id", "?"), it.get("category", "?")
        cmd = it.get("cmd")
        if cmd:
            proc = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True,
                                  text=True, timeout=600)
            ev = ev_dir / f"{rid}.log"
            ev.write_text(f"$ {cmd}\nexit={proc.returncode}\n\n{proc.stdout}\n{proc.stderr}",
                          encoding="utf-8")
            status = "pass" if proc.returncode == 0 else "fail"
            results.append({"id": rid, "category": cat, "status": status,
                            "evidence": str(ev.relative_to(ROOT))})
        elif cat == "manual":
            results.append({"id": rid, "category": cat, "status": "pending_manual",
                            "evidence": "manual（移交用户）"})
        else:
            results.append({"id": rid, "category": cat, "status": "pending",
                            "evidence": "待 acceptor agent 核验"})

    statuses = {r["status"] for r in results}
    if "fail" in statuses:
        result = "fail"
    elif "pending" in statuses:
        result = "pending_agent"
    elif "pending_manual" in statuses:
        result = "pending_manual"
    else:
        result = "pass"

    retry = read_retry()
    if result != "pass":
        retry["count"] = int(retry.get("count", 0)) + 1
    retry["tripped"] = retry["count"] >= int(retry.get("max", 3))
    write_retry(retry)

    n = next_run_no(acc_dir)
    record = {
        "campaign": {"competition_id": (bp.get("campaign") or {}).get("competition_id", "?"),
                     "blueprint_ref": git_ref()},
        "checklist": results,
        "result": result,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "retry_state": retry,
    }
    out = acc_dir / f"run-{n}.json"
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for r in results:
        print(f"  [{r['status']:14s}] {r['id']}")
    print(f"[run_acceptance] result={result} retry={retry['count']}/{retry['max']}"
          f"{' ⚠已熔断：停止自动重试，升级人工' if retry['tripped'] else ''}")
    print(f"[run_acceptance] 记录 → {out.relative_to(ROOT)}")
    if result == "fail":
        print("[run_acceptance] 下一步：acceptor 开失败工单 → init_state --phase deliver 修复 → 重跑")
    return {"pass": 0, "fail": 1}.get(result, 3)


if __name__ == "__main__":
    sys.exit(main())
