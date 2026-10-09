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
    # 夹具只拷工程面运行依赖；workspace/archive/.flow 现场重建，主库面另起全新 git——
    # 2026-10-09 git 拆分后真实 .git 2G + 产物树 8G，整拷代价失控且无必要。
    # 真实 .gitignore 已含 repo-split 忽略块 → 夹具主库按拆分后口径看待 workspace。
    shutil.copytree(SRC_ROOT, tmp, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(
                        ".venv", "__pycache__", "node_modules", ".git",
                        "workspace", "archive", "kb", "export", "tools",
                        "my_LLM_valut", ".flow", ".tmp"))
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
    git(tmp, "init", "-q", "-b", "main")
    git(tmp, "config", "user.email", "arch-test@example.test")
    git(tmp, "config", "user.name", "arch-test")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", "fixture baseline")
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
    # 拆分后口径：tag 落项目仓库（.git 随目录搬移/无库则在目标位补建），主库零提交
    root = make_root()
    try:
        set_result(root, "pass")
        head_before = git(root, "rev-parse", "HEAD").stdout.strip()
        p = run_arch(root)
        arch_dirs = real_arch_entries(root)
        tag_ok = tree_ok = cont_ok = state_ok = head_ok = False
        if p.returncode == 0 and len(arch_dirs) == 1:
            dest = arch_dirs[0]
            tag = f"archive/{dest.name}"
            tag_ok = git(dest, "rev-parse", tag).returncode == 0
            # 关键断言：tag 指向的提交里真的有归档内容（项目仓库视角）
            ls = git(dest, "ls-tree", tag, "--name-only")
            tree_ok = "blueprint.md" in ls.stdout.splitlines()
            ws = root / "workspace"
            left = sorted(q.name for q in ws.iterdir())
            cont_ok = left == ["README.md"] and "多战役容器" in (ws / "README.md").read_text(encoding="utf-8")
            state_ok = json.loads((root / ".flow/state.json").read_text(encoding="utf-8"))["phase"] == "idle"
            head_ok = git(root, "rev-parse", "HEAD").stdout.strip() == head_before
        ok = p.returncode == 0 and tag_ok and tree_ok and cont_ok and state_ok and head_ok
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} pass 归档(v1)：项目库tag={tag_ok} tag含战役内容={tree_ok} "
              f"容器复位={cont_ok} 状态idle={state_ok} 主库零提交={head_ok}")
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
        # 拆分后世界：demo 自带项目仓库 + 本地 bare 远程（归档 tag 应落项目库并 push）
        remotes = root / ".flow" / "remotes"
        remotes.mkdir(parents=True, exist_ok=True)
        bare = remotes / "demo.git"
        subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, timeout=60)
        git(demo, "init", "-q", "-b", "main")
        git(demo, "config", "user.email", "arch-test@example.test")
        git(demo, "config", "user.name", "arch-test")
        git(demo, "add", "-A")
        git(demo, "commit", "-q", "-m", "campaign state")
        git(demo, "remote", "add", "origin", str(bare))
        head_before = git(root, "rev-parse", "HEAD").stdout.strip()
        p = run_arch(root, "--campaign", "demo")
        st = json.loads((root / ".flow/state.json").read_text(encoding="utf-8"))
        dests = real_arch_entries(root)
        dest = dests[0] if len(dests) == 1 else None
        proj_ok = remote_ok = False
        if dest:
            proj_ok = ((dest / ".git").is_dir()
                       and git(dest, "rev-parse", f"archive/{dest.name}").returncode == 0)
            rt = subprocess.run(["git", "ls-remote", "--tags", str(bare)],
                                capture_output=True, text=True, timeout=60).stdout
            remote_ok = f"archive/{dest.name}" in rt
        head_ok = git(root, "rev-parse", "HEAD").stdout.strip() == head_before
        clean_ok = git(root, "status", "--porcelain").stdout == ""
        ok = (p.returncode == 0 and not demo.exists()
              and (ws / "other" / "keep.txt").is_file()
              and "demo" not in st.get("campaigns", {}) and "other" in st.get("campaigns", {})
              and len(dests) == 1
              and ((ws / "README.md").is_file())  # 容器 README 仍在
              and proj_ok and remote_ok and head_ok and clean_ok)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} v2 单战役归档：demo目录清除={not demo.exists()} "
              f"other保留={(ws / 'other' / 'keep.txt').is_file()} 项目库tag={proj_ok} "
              f"远端tag={remote_ok} 主库零提交={head_ok} 主库status净={clean_ok}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    total = 5
    print(f"[test_archive] {passed}/{total} 通过")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
