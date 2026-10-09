#!/usr/bin/env python3
"""repo_split（git 拆分迁移器）回归测试：plan/apply/verify/adopt/snapshot 外部行为。

seam：脚本命令行层 + 临时多库 git fixture（spec #2 / issue#3 对齐，T1 测试基座）。
fixture 为合成微型库（不拷真实仓库）：两个战役 + 导出层 + 原始层 + 一个归档目录，
含被忽略大数据与"未跟踪未忽略"的归档遗留件，镜像真实布局的形态。
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

SRC_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/maint/repo_split.py"
REMOTE_BASE = "https://example.test/r"

FIXTURE_GITIGNORE = """\
# fixture .gitignore（镜像真实库形态）
.flow/
kb/raw/*
!kb/raw/.gitkeep
__pycache__/
.tmp/
workspace/demo-a/bigdata/
workspace/demo-b/bigdata/
workspace/demo-b/replays/episode-*-replay.json
"""

FIXTURE_FILES = {
    "workspace/README.md": "# workspace\n",
    "workspace/JOURNAL.md": "# journal\n",
    "workspace/demo-a/blueprint.md": "blueprint a\n",
    "workspace/demo-a/docs/notes.md": "notes\n",
    "workspace/demo-a/bigdata/huge.bin": "X" * 256,
    "workspace/demo-b/strategy.md": "strategy b\n",
    "workspace/demo-b/bigdata/blob.bin": "Y" * 256,
    "workspace/demo-b/replays/episode-1-replay.json": "{\"r\": 1}\n",
    "export/digest-2026-01.md": "digest\n",
    "kb/raw/raw-1.md": "raw doc\n",
    "kb/raw/.gitkeep": "",
    "archive/2026-01_demo/keep.md": "archived\n",
}


def run_rs(root: Path, *args: str, remote_base: str = REMOTE_BASE) -> subprocess.CompletedProcess:
    # CLI 契约：全局选项（--root/--remote-base）在子命令之前；身份走环境变量（测试自包含）
    import os
    env = dict(os.environ, GIT_AUTHOR_NAME="split-test", GIT_AUTHOR_EMAIL="split-test@example.test",
               GIT_COMMITTER_NAME="split-test", GIT_COMMITTER_EMAIL="split-test@example.test")
    return subprocess.run(
        [sys.executable, str(SRC_ROOT / SCRIPT), "--root", str(root),
         "--remote-base", remote_base, *args],
        capture_output=True, text=True, timeout=120, env=env)


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=60)


def make_fixture() -> Path:
    """合成微型主库：内容已全部提交（模拟拆分前世界）；归档遗留大数据提交后落盘、
    保持"未跟踪未忽略"（镜像真实 archive/ 的 ~600MB 未入库遗留）。"""
    tmp = Path(tempfile.mkdtemp(prefix="autoc_split_test_"))
    git(tmp, "init", "-q", "-b", "main")
    git(tmp, "config", "user.email", "split-test@example.test")
    git(tmp, "config", "user.name", "split-test")
    (tmp / ".gitignore").write_text(FIXTURE_GITIGNORE, encoding="utf-8")
    for rel, content in FIXTURE_FILES.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", "baseline")
    # 归档遗留：提交后落盘，不入库（真实 archive/ 的形态）
    leftover = tmp / "archive/2026-01_demo/bigdata/old.bin"
    leftover.parent.mkdir(parents=True, exist_ok=True)
    leftover.write_text("Z" * 256, encoding="utf-8")
    return tmp


def status_tracked_dirty(root: Path) -> str:
    """已跟踪文件的改动行（?? 未跟踪行不算）。"""
    out = git(root, "status", "--porcelain").stdout.splitlines()
    return "\n".join(l for l in out if not l.startswith("??"))


def main() -> int:
    passed = 0

    # ── 循环 1：plan 产出正确 manifest 且零副作用 ──────────────────────────
    root = make_fixture()
    try:
        mpath = root / "plan.json"
        before_ignore = (root / ".gitignore").read_text(encoding="utf-8")
        p = run_rs(root, "plan", "--json", str(mpath))
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} plan exit=0：rc={p.returncode} {p.stderr[-300:]}")

        m = json.loads(mpath.read_text(encoding="utf-8"))
        parts = {x["path"]: x for x in m["partitions"]}
        ok = set(parts) == {"workspace/demo-a", "workspace/demo-b", "export", "kb/raw"}
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} plan 分区齐全：{sorted(parts)}")

        ok = (parts["workspace/demo-a"]["repo"] == "autoC-demo-a"
              and parts["workspace/demo-a"]["remote"] == REMOTE_BASE + "/autoC-demo-a"
              and parts["workspace/demo-b"]["repo"] == "autoC-demo-b")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} plan 命名与远程：{parts['workspace/demo-a'].get('remote')}")

        files_a = set(parts["workspace/demo-a"]["files"])
        ok = ("workspace/demo-a/blueprint.md" in files_a
              and "workspace/demo-a/docs/notes.md" in files_a
              and "workspace/demo-a/bigdata/huge.bin" not in files_a
              and "workspace/demo-b/replays/episode-1-replay.json"
              not in set(parts["workspace/demo-b"]["files"]))
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} plan 大数据排除（a 计入 {len(files_a)} 件）")

        files_raw = set(parts["kb/raw"]["files"])
        ok = {"kb/raw/raw-1.md", "kb/raw/.gitkeep"} <= files_raw
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} kbraw 分区含 raw 文档与 .gitkeep")

        arch = {x["path"]: x for x in m["archive"]}
        a0 = arch.get("archive/2026-01_demo", {})
        ok = (a0.get("tag") == "archive/2026-01_demo"
              and "archive/2026-01_demo/keep.md" in set(a0.get("files", []))
              and "archive/2026-01_demo/bigdata/old.bin" not in set(a0.get("files", [])))
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 归档分区（tag={a0.get('tag')}，计入 {len(a0.get('files', []))} 件）")

        ok = (status_tracked_dirty(root) == ""
              and (root / ".gitignore").read_text(encoding="utf-8") == before_ignore
              and not (root / "workspace/demo-a" / ".git").exists()
              and "repo-split" not in before_ignore)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} plan 零副作用（ignore 未改、无新库、无脏改动）")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # ── 循环 2：apply 建库/主库摘除 + verify 全绿 ────────────────────────────
    root = make_fixture()
    try:
        mpath = root / "plan.json"
        assert run_rs(root, "plan", "--json", str(mpath)).returncode == 0
        m = json.loads(mpath.read_text(encoding="utf-8"))
        p = run_rs(root, "apply", "--manifest", str(mpath))
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} apply exit=0：rc={p.returncode} {p.stderr[-300:]}")

        repo_ok = True
        detail = []
        for e in m["partitions"]:
            d = root / e["path"]
            if not (d / ".git").is_dir():
                repo_ok = False
                detail.append(f"{e['path']} 无 .git")
                continue
            rel_expect = {f[len(e["path"]) + 1:]: f for f in e["files"]}
            got = set(git(d, "ls-files", "-z").stdout.split("\0")) - {""}
            if got != set(rel_expect) | {".gitignore"}:
                repo_ok = False
                detail.append(f"{e['path']} 清单漂移 -{(set(rel_expect) | {'.gitignore'}) - got} +{got - (set(rel_expect) | {'.gitignore'})}")
            for rel, full in rel_expect.items():
                if sha256_file(root / full) != e["sha256"][full]:
                    repo_ok = False
                    detail.append(f"{full} 校验和漂移")
            url = git(d, "remote", "get-url", "origin").stdout.strip()
            if url != e["remote"]:
                repo_ok = False
                detail.append(f"{e['path']} remote={url}")
        passed += repo_ok
        print(f"{'PASS' if repo_ok else 'FAIL'} 各库内容/校验和/remote 与 manifest 一致：{detail[:3]}")

        # 项目库忽略继承（行为级）：新增大数据不得入库
        (root / "workspace/demo-a/bigdata/new.bin").write_text("N" * 64, encoding="utf-8")
        git(root / "workspace/demo-a", "add", "-A")
        st = git(root / "workspace/demo-a", "status", "--porcelain").stdout
        ok = "new.bin" not in st
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 项目库忽略继承（大数据新增不入库）")

        main_tracked = git(root, "ls-files").stdout
        ok = ("workspace/demo-a/blueprint.md" not in main_tracked
              and "kb/raw/.gitkeep" not in main_tracked
              and "workspace/README.md" in main_tracked
              and "workspace/JOURNAL.md" in main_tracked
              and "archive/2026-01_demo/keep.md" in main_tracked)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 主库跟踪面收窄（分区摘除、容器/归档保留）")

        ok = ("repo-split" in (root / ".gitignore").read_text(encoding="utf-8")
              and status_tracked_dirty(root) == "")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 主库忽略块落位且提交后无脏改动")

        p = run_rs(root, "verify", "--manifest", str(mpath), "--skip-archive")
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} apply 后 verify 全绿：rc={p.returncode} {p.stdout[-300:]}{p.stderr[-200:]}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # ── 循环 3a：verify 对人为破坏必须报错并点名 ────────────────────────────
    root = make_fixture()
    try:
        mpath = root / "plan.json"
        assert run_rs(root, "plan", "--json", str(mpath)).returncode == 0
        assert run_rs(root, "apply", "--manifest", str(mpath)).returncode == 0

        bp = root / "workspace/demo-a/blueprint.md"
        orig = bp.read_text(encoding="utf-8")
        bp.write_text(orig + "tampered\n", encoding="utf-8")
        p = run_rs(root, "verify", "--manifest", str(mpath), "--skip-archive")
        ok = p.returncode == 1 and "blueprint.md" in p.stdout and "校验和漂移" in p.stdout
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} verify 抓改字节：rc={p.returncode} {p.stdout.splitlines()[:2]}")
        bp.write_text(orig, encoding="utf-8")

        notes = root / "workspace/demo-a/docs/notes.md"
        notes.unlink()
        p = run_rs(root, "verify", "--manifest", str(mpath), "--skip-archive")
        ok = p.returncode == 1 and "notes.md" in p.stdout and "文件缺失" in p.stdout
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} verify 抓删文件：rc={p.returncode} {p.stdout.splitlines()[:2]}")
        notes.write_text("notes\n", encoding="utf-8")

        git(root / "workspace/demo-a", "remote", "remove", "origin")
        p = run_rs(root, "verify", "--manifest", str(mpath), "--skip-archive")
        ok = p.returncode == 1 and "remote 不符" in p.stdout
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} verify 抓丢 remote：rc={p.returncode} {p.stdout.splitlines()[:2]}")
        git(root / "workspace/demo-a", "remote", "add", "origin", REMOTE_BASE + "/autoC-demo-a")

        p = run_rs(root, "verify", "--manifest", str(mpath), "--skip-archive")
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 修复后 verify 回绿：rc={p.returncode}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    # ── 循环 3b：push + adopt 跨机收敛（本地 bare 远程）──────────────────────
    rdir = Path(tempfile.mkdtemp(prefix="autoc_split_remotes_"))
    rb = str(rdir)
    root = make_fixture()
    root_b = None
    try:
        mpath = root / "plan.json"
        assert run_rs(root, "plan", "--json", str(mpath), remote_base=rb).returncode == 0
        assert run_rs(root, "apply", "--manifest", str(mpath), remote_base=rb).returncode == 0
        m = json.loads(mpath.read_text(encoding="utf-8"))
        for e in m["partitions"]:
            subprocess.run(["git", "init", "-q", "--bare", f"{rb}/{e['repo']}"], check=True)
        p = run_rs(root, "push", "--manifest", str(mpath), remote_base=rb)
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} push exit=0：rc={p.returncode} {p.stderr[-200:]}")

        e0 = next(x for x in m["partitions"] if x["path"] == "workspace/demo-a")
        rel0 = {f[len(e0["path"]) + 1:] for f in e0["files"]} | {".gitignore"}
        tree = subprocess.run(["git", f"--git-dir={rb}/autoC-demo-a", "ls-tree", "-r", "main", "--name-only"],
                              capture_output=True, text=True).stdout.split()
        ok = set(tree) == rel0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} push 后远端内容与 manifest 一致（{len(tree)} 件）")

        root_b = make_fixture()
        p = run_rs(root_b, "adopt", "--manifest", str(mpath), "--skip-archive", remote_base=rb)
        d_b = root_b / "workspace/demo-a"
        ok = (p.returncode == 0 and (d_b / ".git").is_dir()
              and set(git(d_b, "ls-files", "-z").stdout.split("\0")) - {""} == rel0)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} adopt 建库并收敛清单：rc={p.returncode} {p.stdout[-200:]}{p.stderr[-200:]}")

        huge = d_b / "bigdata/huge.bin"
        ok = (huge.is_file() and huge.read_text(encoding="utf-8") == "X" * 256
              and "bigdata/huge.bin" not in git(d_b, "ls-files").stdout
              and sha256_file(root_b / "workspace/demo-a/blueprint.md") == e0["sha256"]["workspace/demo-a/blueprint.md"])
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} adopt 未跟踪大件不丢且内容与基线一致")

        # 无 manifest 回退（第二台机器无 .flow 基线）：discover + remote-base 推导即收敛
        import shutil as _sh
        _sh.rmtree(d_b / ".git", ignore_errors=True)
        (d_b / "blueprint.md").unlink(missing_ok=True)
        p = run_rs(root_b, "adopt", "--skip-archive", remote_base=rb)  # 不带 --manifest
        ok = (p.returncode == 0 and "推导清单" in p.stdout and (d_b / ".git").is_dir()
              and sha256_file(d_b / "blueprint.md") == e0["sha256"]["workspace/demo-a/blueprint.md"])
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} adopt 无 manifest 回退收敛：rc={p.returncode} {p.stdout.splitlines()[:2]}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)
        if root_b:
            shutil.rmtree(root_b, ignore_errors=True)
        shutil.rmtree(rdir, ignore_errors=True)

    # ── 循环 3c：snapshot 归档补建（快照 + 冻结 ignore + tag + 主库摘除）────
    rdir = Path(tempfile.mkdtemp(prefix="autoc_split_remotes_"))
    rb = str(rdir)
    root = make_fixture()
    try:
        mpath = root / "plan.json"
        assert run_rs(root, "plan", "--json", str(mpath), remote_base=rb).returncode == 0
        assert run_rs(root, "apply", "--manifest", str(mpath), remote_base=rb).returncode == 0
        m = json.loads(mpath.read_text(encoding="utf-8"))
        a0 = next(x for x in m["archive"] if x["path"] == "archive/2026-01_demo")
        subprocess.run(["git", "init", "-q", "--bare", f"{rb}/{a0['repo']}"], check=True)
        p = run_rs(root, "snapshot", "--manifest", str(mpath), remote_base=rb)
        ok = p.returncode == 0
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} snapshot exit=0：rc={p.returncode} {p.stderr[-200:]}")

        d = root / "archive/2026-01_demo"
        tags = git(d, "tag", "-l").stdout.split()
        got = set(git(d, "ls-files", "-z").stdout.split("\0")) - {""}
        ok = ((d / ".git").is_dir() and a0["tag"] in tags
              and got == {"keep.md", ".gitignore"})
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 快照库 + tag + 清单一致：tags={tags} got={sorted(got)}")

        old = d / "bigdata/old.bin"
        ok = (old.is_file() and "old.bin" not in git(d, "ls-files").stdout
              and git(d, "status", "--porcelain").stdout == "")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 归档遗留不入库且冻结后 status 干净")

        ok = (git(root, "ls-files", "--", "archive").stdout.strip() == ""
              and (root / "archive/2026-01_demo/keep.md").is_file())
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 主库摘除 archive 且内容留存磁盘")

        for e in m["partitions"]:
            subprocess.run(["git", "init", "-q", "--bare", f"{rb}/{e['repo']}"], check=True)
        run_rs(root, "push", "--manifest", str(mpath), remote_base=rb)
        p = run_rs(root, "verify", "--manifest", str(mpath), remote_base=rb)
        tags_remote = subprocess.run(["git", "ls-remote", "--tags", f"{rb}/{a0['repo']}"],
                                     capture_output=True, text=True, check=True).stdout
        ok = p.returncode == 0 and a0["tag"] in tags_remote
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 全量 verify 绿 + 远端带 tag：rc={p.returncode}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(rdir, ignore_errors=True)

    # ── 循环 4：bootstrap 新战役建库收口 + push 体积预检 ─────────────────────
    root = make_fixture()
    try:
        camp = root / "workspace" / "new-camp"
        camp.mkdir(parents=True)
        (camp / "JOURNAL.md").write_text("j\n", encoding="utf-8")
        (camp / "__pycache__").mkdir()
        (camp / "__pycache__" / "junk.pyc").write_text("x", encoding="utf-8")
        p = run_rs(root, "bootstrap", "--path", "workspace/new-camp")
        inv = json.loads((root / "config/repo_split_repos.json").read_text(encoding="utf-8"))
        ok = (p.returncode == 0 and (camp / ".git").is_dir()
              and (camp / ".gitignore").is_file()
              and "JOURNAL.md" in git(camp, "ls-files").stdout
              and "__pycache__/junk.pyc" not in git(camp, "ls-files").stdout
              and any(r["path"] == "workspace/new-camp" for r in inv["repos"])
              and git(camp, "remote", "get-url", "origin").stdout.strip()
              == REMOTE_BASE + "/autoC-new-camp")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} bootstrap 新战役建库收口：rc={p.returncode} "
              f"{p.stdout[-120:]}{p.stderr[-120:]}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    root = make_fixture()
    try:
        (root / "workspace/demo-a/big.bin").write_bytes(b"\0" * (2 << 20))  # 2MB > 预检上限 1MB
        mpath = root / "plan.json"
        assert run_rs(root, "plan", "--json", str(mpath)).returncode == 0
        assert run_rs(root, "apply", "--manifest", str(mpath)).returncode == 0
        p = run_rs(root, "push", "--manifest", str(mpath), "--max-file-mb", "1")
        ok = p.returncode == 1 and "push 中止" in p.stderr and "big.bin" in p.stderr
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} push 单文件体积预检拦截：rc={p.returncode} {p.stderr.splitlines()[:2]}")
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    print(f"\n{passed}/29 PASS")
    return 0 if passed == 29 else 1


if __name__ == "__main__":
    sys.exit(main())
