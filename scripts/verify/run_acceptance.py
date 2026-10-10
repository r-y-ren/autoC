#!/usr/bin/env python3
"""S-05 验收执行器（run_acceptance）。

执行 <战役根>/blueprint.md 验收清单：
  - 带 cmd 的项：直接执行（shell），退出码判定 pass/fail，输出存证据文件
  - 不带 cmd 的项：manual 类 → pending_manual（移交用户）；其余 → pending（待 acceptor agent 核验）
  - 执行前先跑 merge_metrics.py 生成顶层 metrics.json（分片汇总）
  - 非 pass 结果累计该战役 retry 计数，达到 max 触发熔断标记（升级人工）

多战役（2026-09-01）：--campaign <cid> 指定战役；缺省时恰有一个登记战役则自动选中，
多战役并存则报错要求显式指定。retry 为战役级属性（写回 campaigns[cid].retry）；
v1 状态按平铺战役根处理，retry 保持在顶层（未迁移仓库兼容）。

产出：<战役根>/acceptance/run-<N>.json（过 acceptance.schema.json）
重试语义（T2.1 裁决）：**只有 result=fail 计入 retry**——pending（等待人工/核验）不是
"修复失败重试"，manual-heavy 战役不应因状态检查误触熔断。
cmd 超时：捕获 TimeoutExpired 记为该条 fail（证据注明 TIMEOUT），执行器不崩溃；
超时上限默认 600s，可用环境变量 AUTOC_CMD_TIMEOUT 覆盖（测试用）。
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "guard"))
import flow_state as fs  # noqa: E402

CMD_TIMEOUT = int(os.environ.get("AUTOC_CMD_TIMEOUT", "600"))


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
STATE = fs.state_file(ROOT)


def load_blueprint(camp_root: Path) -> dict | None:
    bp = camp_root / "blueprint.md"
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


def read_retry(cid: str, camp: dict) -> dict:
    """读取战役级 retry（v1 状态读顶层；budget 当前值实时同步）。"""
    if fs.is_v2(fs.load_state(ROOT)):
        retry = dict(camp.get("retry") or {})
    else:
        try:
            retry = dict(json.loads(STATE.read_text(encoding="utf-8")).get("retry") or {})
        except Exception:  # noqa: BLE001
            retry = {}
    retry.setdefault("count", 0)
    retry = fs.sync_retry(ROOT, retry)
    retry.setdefault("max", 3)
    retry.setdefault("tripped", False)
    return retry


def write_retry(cid: str, retry: dict) -> None:
    """写回 retry：v2 写 campaigns[cid].retry；v1 写顶层（保留旧字段）。"""
    state = fs.load_state(ROOT)
    if fs.is_v2(state) and cid in fs.campaigns(state):
        state["campaigns"][cid]["retry"] = retry
        state["campaigns"][cid]["updated_at"] = fs.now_iso()
        state["campaigns"][cid]["updated_by"] = "run_acceptance"
    else:
        state = state if isinstance(state, dict) else {}
        state["retry"] = retry
    state["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    state["updated_by"] = "run_acceptance"
    fs.save_state(ROOT, state)


def next_run_no(acc_dir: Path) -> int:
    nums = [int(m.group(1)) for f in acc_dir.glob("run-*.json")
            if (m := re.match(r"run-(\d+)\.json$", f.name))]
    return max(nums, default=0) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description="验收执行器（多战役）")
    ap.add_argument("--campaign", default=None, help="目标战役 id（缺省=唯一登记战役）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default=None,
                    help="波次左移用：只验收 id 匹配任一逗号分隔前缀的项（如 --only m1-,sw-）。"
                         "范围不覆盖全清单时 result 封顶 pending_agent，防局部通过误开归档闸门")
    args = ap.parse_args()

    state = fs.load_state(ROOT)
    cid, camp, err = fs.resolve_campaign(ROOT, state, args.campaign)
    if err:
        print(f"[run_acceptance] {err}", file=sys.stderr)
        return 2
    camp_root = fs.campaign_dir(ROOT, camp)

    bp = load_blueprint(camp_root)
    if not bp or not (bp.get("acceptance") or {}).get("checklist"):
        print(f"[run_acceptance] {camp_root.relative_to(ROOT)}/blueprint.md 缺失或无 acceptance.checklist",
              file=sys.stderr)
        return 2

    acc_dir = camp_root / "acceptance"
    checklist = bp["acceptance"]["checklist"]
    scoped = False
    if args.only:
        prefixes = [p.strip() for p in args.only.split(",") if p.strip()]
        full = list(checklist)
        checklist = [it for it in checklist
                     if any(str(it.get("id", "")).startswith(p) for p in prefixes)]
        scoped = len(checklist) < len(full)
        dropped = len(full) - len(checklist)
        print(f"[run_acceptance] 范围过滤：{len(checklist)}/{len(full)} 项（前缀 {prefixes}，范围外 {dropped} 项本run不验）")
        if not checklist:
            print("[run_acceptance] 过滤后无任何验收项", file=sys.stderr)
            return 2

    if args.dry_run:
        for it in checklist:
            mode = "CMD" if it.get("cmd") else ("MANUAL" if it.get("category") == "manual" else "AGENT")
            print(f"  [{mode:5s}] {it.get('id')}: {it.get('item')}")
        print(f"[run_acceptance] 战役 {cid}：dry-run {len(checklist)} 项" + ("（scoped）" if scoped else ""))
        return 0

    # 分片汇总（失败不阻断验收本身，但会体现在证据里）
    merge = ROOT / "scripts" / "verify" / "merge_metrics.py"
    if merge.is_file():
        margs = [sys.executable, str(merge)]
        if cid != "(legacy)":
            margs += ["--campaign", cid]
        subprocess.run(margs, capture_output=True, timeout=30)

    ev_dir = acc_dir / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for it in checklist:
        rid, cat = it.get("id", "?"), it.get("category", "?")
        cmd = it.get("cmd")
        if cmd:
            ev = ev_dir / f"{rid}.log"
            # Windows 上 shell=True 超时只杀外壳，孤儿命令进程仍持有管道（实测被扣 149s）。
            # 解法：新建进程组 + taskkill /T 杀整棵进程树，让执行器在超时后数秒内脱身。
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
            proc = subprocess.Popen(cmd, shell=True, cwd=ROOT, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, creationflags=creationflags)
            try:
                out, err_ = proc.communicate(timeout=CMD_TIMEOUT)
                rc = proc.returncode
                ev_head = f"$ {cmd}\nexit={rc}"
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                                   capture_output=True, timeout=15)
                else:
                    proc.kill()
                try:
                    out, err_ = proc.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    out, err_ = "", ""
                rc = -1
                ev_head = f"$ {cmd}\nexit=TIMEOUT after {CMD_TIMEOUT}s"
            ev.write_text(f"{ev_head}\n\n{out}\n{err_}", encoding="utf-8")
            status = "pass" if rc == 0 else "fail"
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

    retry = read_retry(cid, camp)
    if result == "fail" and not scoped:  # 仅【全量】运行的 fail 计入重试（T2.1 裁决；D12：scoped 诊断不烧熔断额度）
        retry["count"] = int(retry.get("count", 0)) + 1
    retry["tripped"] = retry["count"] >= int(retry.get("max", 3))
    # D12 波次左移：scoped 运行即便范围内全过也不得产生可开归档闸门的 pass——
    # 范围外项未验，result 封顶 pending_agent，终验必须跑全量
    scope_note = None
    if scoped:
        if result == "pass":
            result = "pending_agent"
        scope_note = f"scoped run（--only，范围外项未验；终验须全量重跑）"
    write_retry(cid, retry)

    n = next_run_no(acc_dir)
    record = {
        "campaign": {"competition_id": (bp.get("campaign") or {}).get("competition_id", "?"),
                     "blueprint_ref": git_ref(), "campaign_id": cid},
        "checklist": results,
        "result": result,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "retry_state": retry,
    }
    if scope_note:
        record["scope"] = scope_note
    out = acc_dir / f"run-{n}.json"
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for r in results:
        print(f"  [{r['status']:14s}] {r['id']}")
    print(f"[run_acceptance] 战役 {cid}：result={result} retry={retry['count']}/{retry['max']}"
          f"{' ⚠已熔断：停止自动重试，升级人工' if retry['tripped'] else ''}")
    print(f"[run_acceptance] 记录 → {out.relative_to(ROOT)}")
    if result == "fail":
        print(f"[run_acceptance] 下一步：acceptor 开失败工单 → init_state --campaign {cid} --phase deliver 修复 → 重跑")
    return {"pass": 0, "fail": 1}.get(result, 3)


if __name__ == "__main__":
    sys.exit(main())
