#!/usr/bin/env python3
"""S-11 archive_campaign 回归测试：闸门分支（fail/pending_agent/pending_manual/pass）+ tag 内容审计。

对应 T2.1 审查盲区：pending_agent 绕过闸门、tag 指向归档前提交（只验 tag 存在没验内容）。
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
SCRIPT = "scripts/verify/archive_campaign.py"

BLUEPRINT = """---
campaign: {competition_id: demo-cup, name: Demo Cup, theme: 巡检}
scope: {deliverables: [demo], out_of_scope: []}
tech_stack:
  - {name: tech-a, kb_tech_ids: [x], rationale: r}
interface_contracts: []
milestones:
  - {id: m1, task: t, owner_role: software}
acceptance:
  checklist:
    - {id: a1, category: software, item: i, method: m, cmd: "echo ok"}
compliance: {ai_policy_reviewed: true}
---
正文
"""

RUN_TMPL = """{{
  "campaign": {{"competition_id": "demo-cup"}},
  "checklist": [{{"id": "a1", "category": "software", "status": "{status}", "evidence": "e"}}],
  "result": "{result}",
  "generated_at": "2026-08-27T12:00:00"
}}
"""


def make_root(v2_state: dict | None = None) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_arch_test_"))
    # 夹具与真实库隔离：排除 .venv/缓存，并把真实 archive/ 清空重建（保留 .gitkeep）——
    # 否则真实归档条目会被拷进临时根，击穿"归档区无实体"与 tag 断言（2026-08-28 实际归档后暴露）
    shutil.copytree(SRC_ROOT, tmp, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".venv", "__pycache__", "node_modules"))
    real_arch = tmp / "archive"
    if real_arch.is_dir():
        shutil.rmtree(real_arch)
    real_arch.mkdir(parents=True)
    (real_arch / ".gitkeep").touch()
    # 状态钉死 + workspace 清空重建（真实库的 run-*.json/blueprint 会击穿闸门断言）
    (tmp / ".flow").mkdir(exist_ok=True)
    (tmp / ".flow" / "state.json").write_text(json.dumps(
        v2_state if v2_state else {"schema_version": 1, "phase": "idle", "campaign": None,
                                   "retry": {"count": 0, "max": 3, "tripped": False}}),
        encoding="utf-8")
    ws = tmp / "workspace"
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    (ws / "README.md").write_text("# workspace\n", encoding="utf-8")
    (ws / "acceptance").mkdir()
    (ws / "blueprint.md").write_text(BLUEPRINT, encoding="utf-8")
    (ws / "software").mkdir()
    (ws / "software" / "app.py").write_text("print('demo')\n", encoding="utf-8")
    return tmp


def set_result(root: Path, result: str, status: str = "pass") -> None:
    (root / "workspace/acceptance/run-1.json").write_text(
        RUN_TMPL.format(result=result, status=status), encoding="utf-8")


def run_arch(root: Path, *flags: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(root))
    return subprocess.run([sys.executable, str(root / SCRIPT), *flags], cwd=root,
                          capture_output=True, text=True, env=env, timeout=120)


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=60)


def real_arch_entries(root: Path) -> list[Path]:
    """归档实体会目（排除占位 .gitkeep，避免断言误判）。"""
    d = root / "archive"
    return [p for p in d.glob("*") if p.name != ".gitkeep"] if d.is_dir() else []


def main() -> int:
    passed = 0

    # 闸门 1：pending_agent 必须拒绝（T2.1 修复的 P1）
    root = make_root()
    try:
        set_result(root, "pending_agent", "pending")
        p = run_arch(root)
        ok = p.returncode == 2 and real_arch_entries(root) == []
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 闸门 pending_agent 拒绝：exit={p.returncode} 归档区无实体={real_arch_entries(root) == []}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 闸门 2：fail 拒绝
    root = make_root()
    try:
        set_result(root, "fail", "fail")
        p = run_arch(root)
        ok = p.returncode == 2
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 闸门 fail 拒绝：exit={p.returncode}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 闸门 3：pass 放行 → tag 快照必须包含归档内容（不只验 tag 存在）；
    # v1 legacy 归档后 workspace 复位为多战役容器（只剩 README.md，无单战役骨架）
    root = make_root()
    try:
        set_result(root, "pass")
        p = run_arch(root)
        arch_dirs = real_arch_entries(root)
        tag_ok = tree_ok = cont_ok = state_ok = False
        if p.returncode == 0 and len(arch_dirs) == 1:
            tag = f"archive/{arch_dirs[0].name}"
            tag_ok = git(root, "rev-parse", tag).returncode == 0
            # 关键断言：tag 指向的提交里真的有归档内容
            ls = git(root, "ls-tree", tag, "--name-only")
            tree_ok = "archive" in ls.stdout.splitlines()
            ws = root / "workspace"
            left = sorted(q.name for q in ws.iterdir())
            cont_ok = left == ["README.md"] and "多战役容器" in (ws / "README.md").read_text(encoding="utf-8")
            state_ok = json.loads((root / ".flow/state.json").read_text(encoding="utf-8"))["phase"] == "idle"
        ok = p.returncode == 0 and tag_ok and tree_ok and cont_ok and state_ok
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} pass 归档(v1)：tag存在={tag_ok} tag含归档内容={tree_ok} "
              f"容器复位={cont_ok} 状态idle={state_ok}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 闸门 4：pending_manual 无 flag 拒绝、带 --allow-manual 放行
    root = make_root()
    try:
        set_result(root, "pending_manual", "pending_manual")
        p1 = run_arch(root)
        p2 = run_arch(root, "--allow-manual")
        ok = p1.returncode == 2 and p2.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} pending_manual：无flag拒绝={p1.returncode == 2} "
              f"带flag放行={p2.returncode == 0}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 闸门 5（v2 多战役）：归档单个战役目录，其余战役与其目录不受影响，状态条目注销
    v2_state = {
        "schema_version": 2, "phase": "idle",
        "campaigns": {
            "demo": {"phase": "verify", "root": "workspace/demo",
                     "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []},
            "other": {"phase": "deliver", "root": "workspace/other",
                      "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []},
        },
    }
    root = make_root(v2_state=v2_state)
    try:
        # v2 布局：把 v1 夹具的平铺战役内容挪到 workspace/demo/，另建 other 战役占位
        ws = root / "workspace"
        demo = ws / "demo"
        demo.mkdir()
        for name in ("blueprint.md", "software", "acceptance"):
            shutil.move(str(ws / name), str(demo / name))
        (demo / "acceptance" / "run-1.json").write_text(
            RUN_TMPL.format(result="pass", status="pass"), encoding="utf-8")
        (ws / "other").mkdir()
        (ws / "other" / "keep.txt").write_text("keep", encoding="utf-8")
        p = run_arch(root, "--campaign", "demo")
        st = json.loads((root / ".flow/state.json").read_text(encoding="utf-8"))
        ok = (p.returncode == 0 and not demo.exists()
              and (ws / "other" / "keep.txt").is_file()
              and "demo" not in st.get("campaigns", {}) and "other" in st.get("campaigns", {})
              and len(real_arch_entries(root)) == 1
              and ((ws / "README.md").is_file()))  # 容器 README 仍在
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} v2 单战役归档：demo目录清除={not demo.exists()} "
              f"other保留={(ws / 'other' / 'keep.txt').is_file()} 注册表={sorted(st.get('campaigns', {}))}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    total = 5
    print(f"[test_archive] {passed}/{total} 通过")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
