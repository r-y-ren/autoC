#!/usr/bin/env python3
"""S-10 run_acceptance 回归测试：cmd 执行/失败路径/超时捕获/仅 fail 计数/run-N.json 过 schema。

对应 T2.1 审查盲区：cmd 超时崩溃、pending 误计 retry。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/verify/run_acceptance.py"

BP_HEAD = """---
campaign: {competition_id: demo-cup, name: Demo Cup, theme: t}
scope: {deliverables: [demo], out_of_scope: []}
tech_stack:
  - {name: tech-a, kb_tech_ids: [x], rationale: r}
interface_contracts: []
milestones:
  - {id: m1, task: t, owner_role: software}
acceptance:
  checklist:
"""
BP_TAIL = "compliance: {ai_policy_reviewed: true}\n---\n正文\n"


def make_root() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_acc_test_"))
    shutil.copytree(SRC_ROOT, tmp, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".venv", "__pycache__", "node_modules"))
    (tmp / "workspace" / "acceptance").mkdir(parents=True, exist_ok=True)
    return tmp


def write_blueprint(root: Path, items_yaml: str) -> None:
    (root / "workspace" / "blueprint.md").write_text(BP_HEAD + items_yaml + BP_TAIL,
                                                     encoding="utf-8")


def run_acc(root: Path, extra_env: dict | None = None, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(root), **(extra_env or {}))
    return subprocess.run([sys.executable, str(root / SCRIPT), *(extra or [])], cwd=root,
                          capture_output=True, text=True, env=env, timeout=120)


def read_state(root: Path) -> dict:
    return json.loads((root / ".flow" / "state.json").read_text(encoding="utf-8"))


def main() -> int:
    passed = 0

    # 场景 A：混合清单（pass/fail/manual/pending）→ fail，retry 计数
    root = make_root()
    try:
        write_blueprint(root, "\n".join([
            '    - {id: a1, category: software, item: ok, method: m, cmd: "echo hello"}',
            '    - {id: a2, category: software, item: bad, method: m, cmd: "exit 1"}',
            '    - {id: a3, category: manual, item: 人工, method: 现场}',
            '    - {id: a4, category: document, item: 待核验, method: 读产物}']) + "\n")
        p1 = run_acc(root)
        run1 = json.loads((root / "workspace/acceptance/run-1.json").read_text(encoding="utf-8"))
        st = {c["id"]: c["status"] for c in run1["checklist"]}
        ok = (p1.returncode == 1 and run1["result"] == "fail"
              and st == {"a1": "pass", "a2": "fail", "a3": "pending_manual", "a4": "pending"}
              and (root / "workspace/acceptance/evidence/a1.log").is_file()
              and read_state(root)["retry"]["count"] == 1)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} A 混合清单：exit={p1.returncode} result={run1['result']} 状态={st} retry=1")
        p2 = run_acc(root)
        ok = p2.returncode == 1 and read_state(root)["retry"]["count"] == 2
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} A2 fail 重跑计数累计：retry={read_state(root)['retry']['count']}（期望 2）")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 场景 B：无 fail（pass+manual+pending）→ pending_manual，retry 不计数
    root = make_root()
    try:
        write_blueprint(root, "\n".join([
            '    - {id: b1, category: software, item: ok, method: m, cmd: "echo ok"}',
            '    - {id: b2, category: manual, item: 人工, method: 现场}',
            '    - {id: b3, category: document, item: 待核验, method: 读}']) + "\n")
        p = run_acc(root)
        ok = (p.returncode == 3 and read_state(root)["retry"]["count"] == 0)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} B pending 不计 retry：exit={p.returncode} retry={read_state(root)['retry']['count']}（期望 0）")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 场景 C：cmd 超时 → 记 fail 不崩溃，证据含 TIMEOUT
    root = make_root()
    try:
        write_blueprint(root, '    - {id: c1, category: software, item: 卡死, method: m, cmd: "ping -n 30 127.0.0.1 >nul"}\n')
        p = run_acc(root, {"AUTOC_CMD_TIMEOUT": "2"})
        ev = (root / "workspace/acceptance/evidence/c1.log").read_text(encoding="utf-8")
        run_ok = (root / "workspace/acceptance/run-1.json").is_file()
        ok = (p.returncode == 1 and "TIMEOUT" in ev and run_ok
              and read_state(root)["retry"]["count"] == 1)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} C 超时捕获：exit={p.returncode} 证据含TIMEOUT={'TIMEOUT' in ev} 记录落盘={run_ok}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 场景 D：run-N.json 通过 acceptance schema
    root = make_root()
    try:
        write_blueprint(root, '    - {id: d1, category: software, item: ok, method: m, cmd: "echo ok"}\n')
        run_acc(root)
        sys.path.insert(0, str(root / "scripts" / "kb"))
        for m in list(sys.modules):
            if m == "lint_kb":
                del sys.modules[m]
        import importlib
        lint = importlib.import_module("lint_kb")
        ok, msg = lint.validate_path(root / "workspace/acceptance/run-1.json")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} D run-1.json 过 schema：{msg}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 场景 E：retry.max 实时同步（T-audit 备忘项闭合）——中途改 budget 立即生效
    root = make_root()
    try:
        (root / ".flow").mkdir(parents=True, exist_ok=True)
        (root / ".flow/state.json").write_text(json.dumps({
            "phase": "idle", "retry": {"count": 1, "max": 3, "tripped": False}}), encoding="utf-8")
        bp = root / "config/budget.yaml"
        bp.write_text(bp.read_text(encoding="utf-8").replace("repair_max_retries: 3",
                                                             "repair_max_retries: 5"), encoding="utf-8")
        write_blueprint(root, '    - {id: e1, category: software, item: 失败, method: m, cmd: "exit 1"}\n')
        p = run_acc(root)
        st = read_state(root)
        ok = p.returncode == 1 and st["retry"]["max"] == 5 and st["retry"]["count"] == 2
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} E retry.max 实时同步：max={st['retry']['max']}（期望5） count={st['retry']['count']}（期望2）")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 场景 F（D12）：--only 波门左移——范围过滤生效、scoped 全过封顶 pending_agent、fail 不烧熔断
    root = make_root()
    try:
        (root / ".flow").mkdir(parents=True, exist_ok=True)
        (root / ".flow/state.json").write_text(json.dumps({
            "phase": "idle", "retry": {"count": 0, "max": 3, "tripped": False}}), encoding="utf-8")
        write_blueprint(root,
            "    - {id: m0-x, category: software, item: 骨架, method: m, cmd: \"exit 0\"}\n"
            "    - {id: m0-y, category: software, item: 骨架2, method: m, cmd: \"exit 0\"}\n"
            "    - {id: m2-z, category: software, item: 完整层, method: m, cmd: \"exit 0\"}\n")
        p = run_acc(root, extra=["--only", "m0-"])
        runs = sorted((root / "workspace/acceptance").glob("run-*.json"))
        rec = json.loads(runs[-1].read_text(encoding="utf-8"))
        ids = [r["id"] for r in rec["checklist"]]
        st = read_state(root)
        ok = (p.returncode == 3 and ids == ["m0-x", "m0-y"]
              and rec["result"] == "pending_agent" and "scope" in rec
              and st["retry"]["count"] == 0)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} F scoped 左移：exit={p.returncode} 范围={ids} "
              f"封顶={rec['result']} scope标记={'scope' in rec} retry不烧={st['retry']['count']}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    total = 7
    print(f"[test_acceptance] {passed}/{total} 通过")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
