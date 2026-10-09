#!/usr/bin/env python3
"""S-06 战役归档（archive_campaign，v2 多战役，2026-10 git 拆分后口径）。

把单个战役根整体固化到 archive/<YYYY-MM>_<赛事名>_<主题>/，然后注销该战役
（v2 状态移除注册条目；v1 状态复位 idle）。其余战役不受影响。
git 口径：commit + tag 落**项目仓库**（.git 随目录搬移；无库则在目标位补建快照库），
主库零提交；项目库有 origin 时 push 分支与 tag（远程即归档证据链）。

安全前置（不满足即拒绝，--force 强制）：
  - <战役根>/blueprint.md 存在（归档名取自其 campaign 字段）
  - 最新 run-*.json：result=pass 可归档；pending_manual 需 --allow-manual；fail 拒绝
用法：
  python scripts/verify/archive_campaign.py [--campaign <cid>] [--dry-run] [--allow-manual] [--force]

v1/legacy 战役（root=workspace）归档后 workspace 复位为多战役容器（README 保留）；
v2 战役（root=workspace/<cid>）归档后删除该战役目录，容器与其余战役不动。
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "guard"))
import flow_state as fs  # noqa: E402

CONTAINER_README = """# workspace/ —— 多战役容器（v2）

每个战役一个子目录 `workspace/<战役id>/`（strategy/blueprint/JOURNAL/metrics +
software/hardware/docs/references/acceptance）。战役登记与注销：
  python scripts/guard/init_state.py --campaign <id> --phase decide   # 开新战役
  python scripts/guard/init_state.py --campaign <id> --phase deliver  # 阶段流转
  python scripts/guard/init_state.py --campaign <id> --close          # 注销

守卫按最长 root 匹配路由到各战役自己的阶段；写入矩阵见 docs/DESIGN.md §6.2。
"""


def project_root() -> Path:
    import os
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()


def sanitize(s: str) -> str:
    # 2026-08-28 收紧：全角标点转连字符 + 按显示宽度截断（全角计 2，上限 40）——
    # 首次真实归档暴露旧版产出超长名且保留全角括号，tag 引用与 Windows 路径均不友好
    s = re.sub(r"[\\/:*?\"<>|\s（）【】《》，、；：！？。．·—]+", "-", (s or "").strip())
    s = re.sub(r"-{2,}", "-", s).strip("-")
    out, width = [], 0
    for ch in s:
        w = 2 if ord(ch) > 0x2E80 else 1
        if width + w > 40:
            break
        out.append(ch)
        width += w
    return "".join(out) or "unnamed"


def load_campaign(camp_root: Path) -> dict:
    bp = camp_root / "blueprint.md"
    if not bp.is_file():
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", bp.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}
    import yaml
    try:
        return (yaml.safe_load(m.group(1)) or {}).get("campaign") or {}
    except Exception:  # noqa: BLE001
        return {}


def latest_result(camp_root: Path) -> str | None:
    acc = camp_root / "acceptance"
    nums = [int(m.group(1)) for f in acc.glob("run-*.json")
            if (m := re.match(r"run-(\d+)\.json$", f.name))]
    if not nums:
        return None
    try:
        return json.loads((acc / f"run-{max(nums)}.json").read_text(encoding="utf-8")).get("result")
    except Exception:  # noqa: BLE001
        return None


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=120)


def git_in(path: Path, *args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=path, capture_output=True, text=True, timeout=timeout)


def main() -> int:
    ap = argparse.ArgumentParser(description="战役归档（多战役）")
    ap.add_argument("--campaign", default=None, help="目标战役 id（缺省=唯一登记战役）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-manual", action="store_true", help="允许 pending_manual 归档")
    ap.add_argument("--force", action="store_true", help="跳过全部安全检查（危险）")
    args = ap.parse_args()

    state = fs.load_state(ROOT)
    cid, camp, err = fs.resolve_campaign(ROOT, state, args.campaign)
    if err:
        print(f"[archive] {err}", file=sys.stderr)
        return 2
    camp_root = fs.campaign_dir(ROOT, camp)
    legacy_root = str(camp.get("root")) == "workspace"

    camp_meta = load_campaign(camp_root)
    if not camp_meta and not args.force:
        print(f"[archive] {camp_root.relative_to(ROOT)}/blueprint.md 缺失或无 campaign 字段，拒绝归档",
              file=sys.stderr)
        return 2
    result = latest_result(camp_root)
    if not args.force:
        if result in ("fail", "pending_agent"):
            print(f"[archive] 最新验收 result={result}（失败或存在未完成 agent 核验项），拒绝归档"
                  f"（修复/补验后重跑，或 --force 明确强制）", file=sys.stderr)
            return 2
        if result == "pending_manual" and not args.allow_manual:
            print("[archive] 最新验收含人工待测项（pending_manual），加 --allow-manual 确认或先完成人工项",
                  file=sys.stderr)
            return 2
        if result is None:
            print(f"[archive] {camp_root.relative_to(ROOT)}/acceptance/ 无验收记录，拒绝归档（先跑 /accept）",
                  file=sys.stderr)
            return 2

    month = datetime.date.today().strftime("%Y-%m")
    dirname = f"{month}_{sanitize(camp_meta.get('name', ''))}_{sanitize(camp_meta.get('theme', ''))}"
    dest = ROOT / "archive" / dirname

    print(f"[archive] 战役 {cid}（root={camp_root.relative_to(ROOT)}）")
    print(f"[archive] 归档名：{dirname}")
    print(f"[archive] 最新验收：{result}")
    entries = sorted(p for p in camp_root.iterdir())
    if legacy_root:
        # legacy 平铺根=workspace 本体：容器 README 留守
        entries = [p for p in entries if p.name != "README.md"]
    # 拆分后：.git/.gitignore 等点文件必须随目录搬移（否则项目库历史与远程被 rmtree 清场）
    if args.dry_run:
        for p in entries:
            print(f"  will move: {p.relative_to(ROOT)}")
        print(f"[archive] dry-run：目标 {dest.relative_to(ROOT)}，tag=archive/{dirname}（落项目仓库）")
        return 0

    if dest.exists():
        print(f"[archive] 目标已存在：{dest}，拒绝覆盖", file=sys.stderr)
        return 2

    dest.mkdir(parents=True)
    moved = []
    for p in entries:
        shutil.move(str(p), str(dest / p.name))
        moved.append(p.name)
    print(f"[archive] 移动 {len(moved)} 项 → {dest.relative_to(ROOT)}")

    if legacy_root:
        # workspace 复位为多战役容器（不再放单战役骨架——新战役经 init_state 登记）
        (camp_root / "README.md").write_text(CONTAINER_README, encoding="utf-8")
    else:
        shutil.rmtree(camp_root, ignore_errors=True)

    # git（拆分后口径）：commit+tag 落项目仓库（commit 必须先于 tag——T2.1 修复的 P2 缺陷语义保留）；
    # 主库零提交；有 origin 则 push 分支与 tag，远程即归档证据链。
    tag = f"archive/{dirname}"
    if not (dest / ".git").is_dir():
        git_in(dest, "init", "-q", "-b", "main")
    dirty = git_in(dest, "status", "--porcelain").stdout.strip()
    tagged = False
    if not dirty:
        tagged = True
    elif git_in(dest, "add", "-A").returncode == 0:
        c = git_in(dest, "-c", "commit.gpgsign=false", "commit", "-m", f"archive({cid}): {dirname}")
        if c.returncode == 0:
            tagged = True
        else:
            print(f"[archive][warn] 项目库 commit 失败（tag 跳过）：{c.stderr.strip()[:100]}", file=sys.stderr)
    else:
        print("[archive][warn] 项目库 git add 失败，仅完成文件移动（commit/tag 跳过）", file=sys.stderr)
    if tagged:
        if git_in(dest, "tag", tag).returncode == 0:
            print(f"[archive] 项目库 commit + tag → {tag}（tag 快照包含归档内容）")
        else:
            print(f"[archive][warn] tag 失败（可能重名）：{tag}", file=sys.stderr)
        if git_in(dest, "remote", "get-url", "origin").returncode == 0:
            p1 = git_in(dest, "push", "-q", "-u", "origin", "main", timeout=1800)
            p2 = git_in(dest, "push", "-q", "origin", tag, timeout=1800)
            if p1.returncode == 0 and p2.returncode == 0:
                print(f"[archive] 项目库已 push（main + {tag}）")
            else:
                print("[archive][warn] 项目库 push 失败（本地 tag 已就位，稍后手动 push）",
                      file=sys.stderr)

    # 状态复位：v2 注销该战役（其余战役不动）；v1 复位 idle
    init = ROOT / "scripts" / "guard" / "init_state.py"
    if fs.is_v2(fs.load_state(ROOT)) and cid != "(legacy)":
        subprocess.run([sys.executable, str(init), "--campaign", cid, "--close",
                        "--by", "archive_campaign"], capture_output=True, timeout=15)
        print(f"[archive] 完成：战役 {cid} 已注销，其余战役不受影响。")
    else:
        subprocess.run([sys.executable, str(init), "--phase", "idle", "--reset",
                        "--by", "archive_campaign"], capture_output=True, timeout=15)
        print("[archive] 完成：归档已提交并打 tag，状态复位 idle。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
