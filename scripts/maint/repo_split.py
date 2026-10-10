#!/usr/bin/env python3
"""repo_split：git 拆分迁移器（一次性工具，spec #2 / issue#3）。

把"产物出主库、各建独立仓库"做成可演练、可验证的动作：
  plan     dry-run：产 manifest（分区/归档快照/主库动作 + 逐文件 sha256 基线），零副作用
  apply    按 manifest 建库、配 remote、首提交，并把分区从主库摘除（--no-main-commit 可演练主库面）
  verify   post-condition 校验：对照 manifest 查逐文件校验和、remote、主库跟踪面
  adopt    第二台机器收敛：init + fetch + reset 到远程状态，保留未跟踪大文件
  snapshot 归档目录补建独立库 + archive/… tag（T3）
  push     各库推送（含 tag）

约定：
  - manifest 基线在任何变更前采集（plan 先行），apply 前重算并要求一致（防 TOCTOU）
  - 项目库 .gitignore = 主库通用规则 + 自身路径前缀改写（大数据例外随库继承）
  - 快照库只收主库已跟踪内容（归档遗留大件维持本地留存，不入快照）
用法：
  python scripts/maint/repo_split.py [--root R] [--remote-base URL] <plan|apply|verify|adopt|snapshot|push> [...]
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

MANIFEST_VERSION = 1
PUSH_TIMEOUT = 1800
INVENTORY_REL = "config/repo_split_repos.json"  # 主库随库清单（新机器 adopt 的事实源）

IGNORE_BLOCK = """\
# >>> repo-split >>>（git 拆分：产物分区出主库，见 spec r-y-ren/contest-compass#2）
workspace/*
!workspace/README.md
!workspace/JOURNAL.md
archive/
export/
kb/raw/
# <<< repo-split <<<
"""

PARTITION_PREFIXES = ("workspace/", "archive/", "export/", "kb/")


def project_root(cli_root: str | None) -> Path:
    import os
    if cli_root:
        return Path(cli_root).resolve()
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def git(root: Path, *args: str, check: bool = True, timeout: int = 120) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=timeout)
    if check and p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失败：{p.stderr.strip()[:400]}")
    return p


JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def git_ls(root: Path, path: str, mode: str = "versionable") -> list[str]:
    """主库视角的内容清单：
      versionable = tracked + 未跟踪未忽略（大数据例外被排除）；
      tracked     = 仅已跟踪（归档快照基线）；
      all         = tracked + 全部未跟踪（kbraw 基线：原始文档正是主库忽略对象）。"""
    args = ["ls-files", "-z"]
    if mode == "versionable":
        args += ["--cached", "--others", "--exclude-standard"]
    elif mode == "all":
        args += ["--cached", "--others"]
    elif mode != "tracked":
        raise ValueError(mode)
    args += ["--", path]
    out = git(root, *args).stdout
    return sorted(x for x in out.split("\0")
                  if x and Path(x).name not in JUNK_NAMES)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:40] or "unnamed"


def discover(root: Path) -> tuple[list[dict], list[dict]]:
    """分区：workspace/<cid> 各战役 + export + kb/raw；归档：archive/<dir> 快照。"""
    parts: list[dict] = []
    ws = root / "workspace"
    if ws.is_dir():
        for d in sorted(p for p in ws.iterdir() if p.is_dir()):
            parts.append({"kind": "campaign", "path": f"workspace/{d.name}",
                          "repo": f"contest-compass-{d.name}"})
    if (root / "export").is_dir():
        parts.append({"kind": "export", "path": "export", "repo": "contest-compass-export"})
    if (root / "kb" / "raw").is_dir():
        parts.append({"kind": "kbraw", "path": "kb/raw", "repo": "contest-compass-kbraw"})
    arch: list[dict] = []
    ad = root / "archive"
    if ad.is_dir():
        for d in sorted(p for p in ad.iterdir() if p.is_dir()):
            arch.append({"path": f"archive/{d.name}", "repo": f"contest-compass-{slugify(d.name)}",
                         "tag": f"archive/{d.name}"})
    # slugify 会吞中文造成同名冲突（同月两个中文赛事 → 同一 repo 名互覆）：冲突即加路径指纹
    used = {p["repo"] for p in parts}
    for a in arch:
        if a["repo"] in used:
            a["repo"] = f"{a['repo']}-{hashlib.sha1(a['path'].encode()).hexdigest()[:6]}"
        used.add(a["repo"])
    return parts, arch


def fill_entries(root: Path, entries: list[dict], remote_base: str | None,
                 mode: str) -> None:
    for e in entries:
        # 嵌套库会让 ls-files --others 把整个子库塌缩成一个目录条目，只收常规文件
        e["files"] = [f for f in git_ls(root, e["path"], mode=mode) if (root / f).is_file()]
        e["sha256"] = {f: sha256_file(root / f) for f in e["files"]}
        e["remote"] = f"{remote_base.rstrip('/')}/{e['repo']}" if remote_base else None


def build_manifest(root: Path, remote_base: str | None) -> dict:
    parts, arch = discover(root)
    for e in parts:
        # kbraw 的使命是给主库忽略的原始文档上版本 → 全量基线；其余分区沿用主库可入库口径
        fill_entries(root, [e], remote_base, mode="all" if e["kind"] == "kbraw" else "versionable")
    fill_entries(root, arch, remote_base, mode="tracked")
    return {
        "version": MANIFEST_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "remote_base": remote_base,
        "partitions": parts,
        "archive": arch,
        "main": {"untrack": [p["path"] for p in parts],
                 "ignore_block": IGNORE_BLOCK},
    }


def project_gitignore(root: Path, path: str) -> str:
    """项目库 .gitignore：主库通用规则继承 + 自身路径前缀改写（大数据例外随库）。"""
    src = root / ".gitignore"
    prefix = path + "/"
    out = ["# 由 repo_split 生成：继承主库忽略规则（自身路径前缀已改写）"]
    if src.is_file():
        for line in src.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            neg = s.startswith("!")
            body = s[1:] if neg else s
            if body.startswith(prefix):
                body = body[len(prefix):]
                if body in ("", "*"):
                    continue
                out.append(("!" if neg else "") + body)
            elif body.startswith(PARTITION_PREFIXES):
                continue  # 其他分区的锚定规则不随库
            else:
                out.append(line)
    return "\n".join(out) + "\n"


def load_manifest(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def default_manifest_path(root: Path) -> Path:
    return root / ".flow" / "repo_split" / "manifest.json"


def assert_baseline(root: Path, m: dict, section: str = "all") -> None:
    """TOCTOU 防护：任何变更前重算当前内容并与 plan 基线比对，漂移即中止。"""
    cur = build_manifest(root, m.get("remote_base"))
    keys = {"partitions", "archive"} if section == "all" else {section}
    cur_map = {x["path"]: x for x in cur["partitions"] + cur["archive"]}
    old_list = ([*m["partitions"], *m["archive"]] if section == "all"
                else m[section])
    for old in old_list:
        new = cur_map.get(old["path"])
        if new is None:
            raise SystemExit(f"基线漂移：{old['path']} 已不存在，重跑 plan")
        if new["files"] != old["files"] or new["sha256"] != old["sha256"]:
            raise SystemExit(f"基线漂移：{old['path']} 自 plan 后内容有变化，重跑 plan")


def ensure_remote(d: Path, url: str) -> None:
    cur = git(d, "remote", "get-url", "origin", check=False)
    if cur.returncode != 0:
        git(d, "remote", "add", "origin", url)
    elif cur.stdout.strip() != url:
        git(d, "remote", "set-url", "origin", url)


def repo_files(d: Path) -> set[str]:
    return set(git(d, "ls-files", "-z").stdout.split("\0")) - {""}


# ── 子命令 ──────────────────────────────────────────────────────────────────

def cmd_plan(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    m = build_manifest(root, args.remote_base)
    for e in m["partitions"] + m["archive"]:
        print(f"plan: {e['path']} -> {e['repo']}（{len(e['files'])} 件"
              + (f"，remote={e['remote']}" if e.get("remote") else "") + "）")
    print(f"plan: 主库摘除 {m['main']['untrack']} + 忽略块；零副作用")
    if args.json:
        Path(args.json).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"plan: manifest -> {args.json}")
    else:
        print(json.dumps(m, ensure_ascii=False, indent=2))
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    m = load_manifest(Path(args.manifest) if args.manifest else default_manifest_path(root))
    assert_baseline(root, m)
    date = datetime.date.today().isoformat()
    for e in m["partitions"]:
        d = root / e["path"]
        gi = d / ".gitignore"
        if not gi.exists():
            gi.write_text(project_gitignore(root, e["path"]), encoding="utf-8")
        if not (d / ".git").is_dir():
            git(root, "init", "-q", "-b", "main", e["path"])
        if e.get("remote"):
            ensure_remote(d, e["remote"])
        rel_files = [f[len(e["path"]) + 1:] for f in e["files"]]
        if rel_files:
            pf = root / ".flow" / "repo_split" / (e["repo"] + ".paths")
            pf.parent.mkdir(parents=True, exist_ok=True)
            pf.write_text("\n".join(rel_files) + "\n", encoding="utf-8")
            git(d, "add", "-f", f"--pathspec-from-file={pf}")
            git(d, "add", "--", ".gitignore")  # 生成的忽略规则随首提交入库
            git(d, "-c", "commit.gpgsign=false", "commit", "-q",
                "-m", f"chore(repo-split): 首次提交（主库迁移快照 {date}）")
        print(f"apply: {e['path']} -> {e['repo']}（{len(rel_files)} 件入库）")
    gi = root / ".gitignore"
    txt = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if "repo-split" not in txt:
        gi.write_text(txt + ("\n" if txt and not txt.endswith("\n") else "") + IGNORE_BLOCK,
                      encoding="utf-8")
    git(root, "add", "--", ".gitignore")
    for path in m["main"]["untrack"]:
        git(root, "rm", "-r", "-q", "--cached", "-f", "--", path)
    if not args.no_main_commit:
        git(root, "-c", "commit.gpgsign=false", "commit", "-q",
            "-m", "chore(repo-split): 产物分区出主库（spec r-y-ren/contest-compass#2）")
    print(f"apply: 主库摘除 {m['main']['untrack']} + 忽略块落位"
          + ("（未提交，--no-main-commit）" if args.no_main_commit else "并提交"))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    m = load_manifest(Path(args.manifest) if args.manifest else default_manifest_path(root))
    fails: list[str] = []
    entries = m["partitions"] + ([] if args.skip_archive else m["archive"])
    for e in entries:
        d = root / e["path"]
        if not (d / ".git").is_dir():
            fails.append(f"{e['path']}：无 .git")
            continue
        rel_expect = {f[len(e["path"]) + 1:]: f for f in e["files"]}
        got = repo_files(d)
        expect_set = set(rel_expect) | {".gitignore"}  # 生成的忽略规则随首提交入库
        if got != expect_set:
            fails.append(f"{e['path']}：清单漂移（缺{sorted(expect_set - got)[:3]}"
                         f" 多{sorted(got - expect_set)[:3]}）")
        for rel, full in rel_expect.items():
            p = root / full
            if not p.is_file():
                fails.append(f"{full}：文件缺失")
            elif sha256_file(p) != e["sha256"][full]:
                fails.append(f"{full}：校验和漂移")
        head = git(d, "ls-tree", "-r", "HEAD", "--name-only", check=False)
        head_set = set(head.stdout.splitlines()) - {""} if head.returncode == 0 else set()
        if head_set != expect_set:
            fails.append(f"{e['path']}：HEAD 提交内容与 manifest 不符（缺{sorted(expect_set - head_set)[:3]}"
                         f" 多{sorted(head_set - expect_set)[:3]}）")
        if e.get("remote"):
            cur = git(d, "remote", "get-url", "origin", check=False)
            if cur.returncode != 0 or cur.stdout.strip() != e["remote"]:
                fails.append(f"{e['path']}：remote 不符（{cur.stdout.strip() or '缺'}）")
    for path in m["main"]["untrack"]:
        if git(root, "ls-files", "--", path).stdout.strip():
            fails.append(f"主库仍跟踪 {path}")
    if not args.skip_archive and git(root, "ls-files", "--", "archive").stdout.strip():
        fails.append("主库仍跟踪 archive（快照未收尾）")
    mt = git(root, "ls-files").stdout
    for keep in ("workspace/README.md", "workspace/JOURNAL.md"):
        if keep not in mt:
            fails.append(f"主库丢失 {keep}")
    gi = root / ".gitignore"
    if "repo-split" not in (gi.read_text(encoding="utf-8") if gi.exists() else ""):
        fails.append("主库 .gitignore 缺 repo-split 忽略块")
    if fails:
        for f in fails:
            print(f"FAIL {f}")
        return 1
    print(f"verify: 全绿（{len(entries)} 库 + 主库面）")
    return 0


def cmd_adopt(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    mp = Path(args.manifest) if args.manifest else default_manifest_path(root)
    if mp.is_file():
        m = load_manifest(mp)
    elif (root / INVENTORY_REL).is_file():
        # 第二台机器：主库随库清单是事实源（.flow 基线不随库走）
        inv = json.loads((root / INVENTORY_REL).read_text(encoding="utf-8"))
        m = {"partitions": [r for r in inv["repos"] if "tag" not in r],
             "archive": [r for r in inv["repos"] if "tag" in r]}
        print(f"adopt: 无 manifest，改用主库清单 {INVENTORY_REL}（{len(inv['repos'])} 库）")
    else:
        # 兜底：discover + 远程基址推导（可能漏库，务必对照 docs/repo-split-handoff.md 核对）
        m = build_manifest(root, args.remote_base)
        print("adopt: 无 manifest/清单，按 discover + remote-base 推导清单（可能漏库，对照交接清单核对）")
    entries = m["partitions"] + ([] if args.skip_archive else m["archive"])
    for e in entries:
        d = root / e["path"]
        if not e.get("remote"):
            print(f"adopt: 跳过 {e['path']}（无远程）")
            continue
        d.mkdir(parents=True, exist_ok=True)
        if not (d / ".git").is_dir():
            git(root, "init", "-q", "-b", "main", e["path"])
        ensure_remote(d, e["remote"])
        git(d, "fetch", "-q", "origin", timeout=PUSH_TIMEOUT)
        git(d, "reset", "-q", "--hard", "origin/main")  # 未跟踪大件不受影响
        print(f"adopt: {e['path']} <- {e['remote']}（收敛到 origin/main）")
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    m = load_manifest(Path(args.manifest) if args.manifest else default_manifest_path(root))
    assert_baseline(root, m, section="archive")
    date = datetime.date.today().isoformat()
    for e in m["archive"]:
        d = root / e["path"]
        if not (d / ".git").is_dir():
            git(root, "init", "-q", "-b", "main", e["path"])
        if e.get("remote"):
            ensure_remote(d, e["remote"])
        rel = [f[len(e["path"]) + 1:] for f in e["files"]]
        if rel:
            pf = root / ".flow" / "repo_split" / (e["repo"] + ".paths")
            pf.parent.mkdir(parents=True, exist_ok=True)
            pf.write_text("\n".join(rel) + "\n", encoding="utf-8")
            git(d, "add", "-f", f"--pathspec-from-file={pf}")
            if ".gitignore" not in rel:
                # 归档冻结：已入库内容外忽略一切（遗留大件不入库、status 干净）
                (d / ".gitignore").write_text("# 归档冻结：除已入库内容外忽略一切（repo_split）\n*\n",
                                             encoding="utf-8")
                git(d, "add", "-f", "--", ".gitignore")
            git(d, "-c", "commit.gpgsign=false", "commit", "-q",
                "-m", f"chore(repo-split): 归档快照（主库迁移 {date}）")
            if e["tag"] not in git(d, "tag", "-l").stdout.split():
                git(d, "tag", e["tag"])
        print(f"snapshot: {e['path']} -> {e['repo']}（{len(rel)} 件 + tag {e['tag']}）")
    git(root, "rm", "-r", "-q", "--cached", "-f", "--", "archive")
    if not args.no_main_commit:
        git(root, "-c", "commit.gpgsign=false", "commit", "-q",
            "-m", "chore(repo-split): 归档产物出主库（快照补建，spec r-y-ren/contest-compass#2）")
    print("snapshot: 主库摘除 archive 并提交" if not args.no_main_commit
          else "snapshot: 主库摘除 archive（未提交）")
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    m = load_manifest(Path(args.manifest) if args.manifest else default_manifest_path(root))
    limit = int(args.max_file_mb) * 1024 * 1024
    for e in m["partitions"] + m["archive"]:
        d = root / e["path"]
        if not (d / ".git").is_dir():
            print(f"push: 跳过 {e['path']}（无库）")
            continue
        if not e.get("remote"):
            print(f"push: 跳过 {e['path']}（无远程）")
            continue
        if git(d, "rev-parse", "HEAD", check=False).returncode != 0:
            print(f"push: 跳过 {e['path']}（无提交）")
            continue
        # 推送前单文件体积预检（GitHub 单文件 100MB 硬上限，超限推送必被拒）
        overs = [f for f in e.get("files", [])
                 if (root / f).is_file() and (root / f).stat().st_size > limit]
        if overs:
            raise SystemExit(f"push 中止：{e['path']} 存在 >{args.max_file_mb}MB 单文件：{overs[:3]}"
                             "（大件应留在本机不入库）")
        ensure_remote(d, e["remote"])
        git(d, "push", "-q", "-u", "origin", "main", timeout=PUSH_TIMEOUT)
        if git(d, "tag", "-l").stdout.split():
            git(d, "push", "-q", "origin", "--tags", timeout=PUSH_TIMEOUT)
        print(f"push: {e['path']} -> {e['remote']}")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    """新战役建库收口：init_state 登记后即建项目库（忽略规则继承/remote/首提交）并入主库清单。"""
    root = project_root(args.root)
    rel = args.path.strip().strip("/")
    d = root / rel
    if not d.is_dir():
        raise SystemExit(f"bootstrap：{rel} 不存在")
    if (d / ".git").is_dir():
        raise SystemExit(f"bootstrap：{rel} 已有项目库")
    repo = f"contest-compass-{Path(rel).name}"
    remote = f"{args.remote_base.rstrip('/')}/{repo}" if args.remote_base else None
    if not (d / ".gitignore").exists():
        (d / ".gitignore").write_text(project_gitignore(root, rel), encoding="utf-8")
    git(root, "init", "-q", "-b", "main", rel)
    if remote:
        ensure_remote(d, remote)
    git(d, "add", "-A")
    git(d, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty",
        "-m", f"chore(repo-split): 新战役建库 {rel}")
    inv_path = root / INVENTORY_REL
    inv = json.loads(inv_path.read_text(encoding="utf-8")) if inv_path.is_file() else {"version": 1, "repos": []}
    if not any(r.get("path") == rel for r in inv["repos"]):
        inv["repos"].append({"path": rel, "repo": repo, "remote": remote, "kind": "campaign"})
        inv["repos"].sort(key=lambda r: r["path"])
        inv_path.parent.mkdir(parents=True, exist_ok=True)
        inv_path.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.push and remote:
        git(d, "push", "-q", "-u", "origin", "main", timeout=PUSH_TIMEOUT)
    print(f"bootstrap: {rel} -> {repo}" + (f"（remote={remote}，已推送）" if args.push and remote else "")
          + f"；清单已更新 {INVENTORY_REL}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="主库根（默认 ZCODE_PROJECT_DIR 或脚本推断）")
    ap.add_argument("--remote-base", help="远程基址，如 https://github.com/r-y-ren")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="dry-run 产 manifest")
    p.add_argument("--json", help="manifest 输出路径")
    p.set_defaults(fn=cmd_plan)
    for name, fn, desc in [("apply", cmd_apply, "按 manifest 执行拆分"),
                           ("verify", cmd_verify, "post-condition 校验"),
                           ("adopt", cmd_adopt, "第二台机器收敛"),
                           ("snapshot", cmd_snapshot, "归档目录补建独立库"),
                           ("push", cmd_push, "各库推送")]:
        sp = sub.add_parser(name, help=desc)
        sp.add_argument("--manifest", help="manifest 路径（apply/verify/adopt 默认 .flow/repo_split/manifest.json）")
        if name == "verify":
            sp.add_argument("--skip-archive", action="store_true",
                            help="跳过归档快照段（T2 阶段快照未做时用）")
        if name == "adopt":
            sp.add_argument("--skip-archive", action="store_true",
                            help="跳过归档快照段")
        if name == "apply":
            sp.add_argument("--no-main-commit", action="store_true",
                            help="主库改动仅暂存不提交（演练用）")
        if name == "snapshot":
            sp.add_argument("--no-main-commit", action="store_true",
                            help="主库改动仅暂存不提交（演练用）")
        if name == "push":
            sp.add_argument("--max-file-mb", type=int, default=100,
                            help="单文件体积预检上限（MB，默认 100=GitHub 硬上限）")
        sp.set_defaults(fn=fn)
    bp = sub.add_parser("bootstrap", help="新战役建库收口（init_state 登记后调用）")
    bp.add_argument("--path", required=True, help="战役根相对路径，如 workspace/<cid>")
    bp.add_argument("--push", action="store_true", help="建库后立即推送")
    bp.set_defaults(fn=cmd_bootstrap)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
