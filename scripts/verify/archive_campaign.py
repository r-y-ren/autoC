#!/usr/bin/env python3
"""S-06 战役归档（archive_campaign）。

workspace/ → archive/<YYYY-MM>_<赛事名>_<主题>/（git add + tag + 复位 workspace + idle）。

安全前置（不满足即拒绝，--force 强制）：
  - workspace/blueprint.md 存在（归档名取自其 campaign 字段）
  - 最新 run-*.json：result=pass 可归档；pending_manual 需 --allow-manual；fail 拒绝
用法：
  python scripts/verify/archive_campaign.py [--dry-run] [--allow-manual] [--force]
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

WORKSPACE_SKELETON_README = """# workspace/ —— 当前战役活跃开发区（v1 单战役约束）

**生命周期**：决策阶段生成 `strategy.md` + `blueprint.md` → 用户确认 → 交付阶段填充 `software/` `hardware/` `docs/` → 验收填充 `acceptance/` → `archive_campaign.py` 整体移入 `archive/` 并清空本目录，开启下一战役。

| 文件/目录 | 归属角色 | 说明 |
|---|---|---|
| `strategy.md` | Strategy | 对比矩阵 + 一鱼多吃路线（decide 态可写） |
| `blueprint.md` | Strategy | ★ 唯一蓝图契约，须过 blueprint.schema.json 校验 |
| `JOURNAL.md` | 协调者 | 阶段流转日志（提交入库，可审计） |
| `metrics.json` | merge_metrics.py | 分片汇总生成物（角色禁写；分片在 software//hardware/ 下） |
| `software/` | Software | 代码 + 沙箱测试 + metrics 分片 |
| `hardware/` | Hardware | BOM / 引脚表 / 固件 + metrics 分片 |
| `docs/` | Document | 报告（Typst）+ PPT（Marp）源码 |
| `acceptance/` | 验收 | 执行记录 / 失败工单 / 分析报告（交付期只读） |

守卫策略与写入矩阵见 `scripts/guard/guard_path.py` 与 `docs/DESIGN.md` §6.2。
"""


def project_root() -> Path:
    import os
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()


def sanitize(s: str) -> str:
    return re.sub(r"[\\/:*?\"<>|\s]+", "-", (s or "").strip())[:40] or "unnamed"


def load_campaign() -> dict:
    bp = ROOT / "workspace" / "blueprint.md"
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


def latest_result() -> str | None:
    acc = ROOT / "workspace" / "acceptance"
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


def main() -> int:
    ap = argparse.ArgumentParser(description="战役归档")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-manual", action="store_true", help="允许 pending_manual 归档")
    ap.add_argument("--force", action="store_true", help="跳过全部安全检查（危险）")
    args = ap.parse_args()

    camp = load_campaign()
    if not camp and not args.force:
        print("[archive] workspace/blueprint.md 缺失或无 campaign 字段，拒绝归档", file=sys.stderr)
        return 2
    result = latest_result()
    if not args.force:
        if result in ("fail", "pending_agent"):
            print(f"[archive] 最新验收 result={result}（失败或存在未完成 agent 核验项），拒绝归档"
                  f"（修复/补验后重跑，或 --force 明确强制）", file=sys.stderr)
            return 2
        if result == "pending_manual" and not args.allow_manual:
            print("[archive] 最新验收含人工待测项（pending_manual），加 --allow-manual 确认或先完成人工项", file=sys.stderr)
            return 2
        if result is None:
            print("[archive] workspace/acceptance/ 无验收记录，拒绝归档（先跑 /accept）", file=sys.stderr)
            return 2

    month = datetime.date.today().strftime("%Y-%m")
    dirname = f"{month}_{sanitize(camp.get('name', ''))}_{sanitize(camp.get('theme', ''))}"
    dest = ROOT / "archive" / dirname
    ws = ROOT / "workspace"

    print(f"[archive] 归档名：{dirname}")
    print(f"[archive] 最新验收：{result}")
    if args.dry_run:
        for p in sorted(ws.iterdir()):
            print(f"  will move: {p.relative_to(ROOT)}")
        print(f"[archive] dry-run：目标 {dest.relative_to(ROOT)}，tag=archive/{dirname}")
        return 0

    if dest.exists():
        print(f"[archive] 目标已存在：{dest}，拒绝覆盖", file=sys.stderr)
        return 2

    dest.mkdir(parents=True)
    moved = []
    for p in sorted(ws.iterdir()):
        if p.name.startswith("."):
            continue
        shutil.move(str(p), str(dest / p.name))
        moved.append(p.name)
    print(f"[archive] 移动 {len(moved)} 项 → {dest.relative_to(ROOT)}")

    # 复位 workspace 骨架
    (ws / "JOURNAL.md").write_text("# 战役日志\n\n| 时间 | 阶段 | 动作 | 结果 |\n|---|---|---|---|\n",
                                   encoding="utf-8")
    (ws / "README.md").write_text(WORKSPACE_SKELETON_README, encoding="utf-8")
    for d in ("software", "hardware", "docs", "acceptance"):
        (ws / d).mkdir(exist_ok=True)
        (ws / d / ".gitkeep").touch()

    # git：add → commit → tag（commit 必须先于 tag，否则 tag 指向归档前旧提交——T2.1 修复的 P2 缺陷）
    if git("add", "-A").returncode == 0:
        c = git("commit", "-m", f"archive: {dirname}")
        if c.returncode == 0:
            tag = f"archive/{dirname}"
            if git("tag", tag).returncode == 0:
                print(f"[archive] git commit + tag → {tag}（tag 快照包含归档内容）")
            else:
                print(f"[archive][warn] tag 失败（可能重名）：{tag}", file=sys.stderr)
        else:
            print(f"[archive][warn] git commit 失败（tag 跳过）：{c.stderr.strip()[:100]}", file=sys.stderr)
    else:
        print("[archive][warn] git add 失败，仅完成文件移动（commit/tag 跳过）", file=sys.stderr)

    init = ROOT / "scripts" / "guard" / "init_state.py"
    subprocess.run([sys.executable, str(init), "--phase", "idle", "--reset",
                    "--by", "archive_campaign"], capture_output=True, timeout=15)
    print("[archive] 完成：归档已提交并打 tag，workspace 已复位，状态回 idle。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
