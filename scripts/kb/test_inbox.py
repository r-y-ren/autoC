#!/usr/bin/env python3
"""S-16b inbox_intake 回归测试（升级票03）：三分路由 / 未溯源降级 / 配额留存 / 活跃战役提示 / README 不消费。

每个用例独立临时根（ZCODE_PROJECT_DIR 覆盖），子进程跑 inbox_intake.py 后断言文件系统与 stdout。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "inbox_intake.py"

META = """kind: {kind}
title: {title}
source_url: https://example.com/src
dropped_at: "2026-09-16"
note: 测试投递
intended: 智慧农业
"""


def run_intake(root: Path) -> str:
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(root))
    r = subprocess.run([sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True)
    return r.stdout + r.stderr


def drop(root: Path, name: str, meta: str | None) -> None:
    inbox = root / "kb" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / name).write_text("x", encoding="utf-8")
    if meta is not None:
        (inbox / (name + ".meta.yaml")).write_text(meta, encoding="utf-8")


def check(cond: bool, note: str) -> bool:
    print(("PASS " if cond else "FAIL ") + note)
    return cond


def main() -> int:
    ok = 0
    total = 0

    # 用例组 1：comp 全 meta → 候选入队 + 原件移 processed；README 与 sidecar 不被当投递物
    with tempfile.TemporaryDirectory(prefix="autoc_inbox_t1_") as td:
        root = Path(td)
        drop(root, "2026-大数据大赛-章程.pdf", META.format(kind="comp", title="大数据大赛"))
        drop(root, "README.md", None)
        out = run_intake(root)
        cands = list((root / "kb/raw/candidates").glob("inbox-comp-*.yaml"))
        total += 2
        ok += check(bool(cands) and "https://example.com/src" in cands[0].read_text(encoding="utf-8"),
                    "comp 全 meta → inbox-comp 候选入队（含 source_url）")
        ok += check((root / "kb/raw/inbox-processed").exists()
                    and any("章程" in p.name for p in (root / "kb/raw/inbox-processed").rglob("*")),
                    "原件移入 inbox-processed；README.md 未被消费")

    # 用例组 2：tech 全 meta → 富字典候选；缺 meta → leads + 催补点名
    with tempfile.TemporaryDirectory(prefix="autoc_inbox_t2_") as td:
        root = Path(td)
        drop(root, "uav-mec-offloading-paper.pdf", META.format(kind="tech", title="UAV MEC Offloading"))
        drop(root, "随手记.md", None)
        out = run_intake(root)
        tech = list((root / "kb/raw/candidates").glob("inbox-tech-*.yaml"))
        total += 3
        ok += check(bool(tech) and "UAV MEC Offloading" in tech[0].read_text(encoding="utf-8")
                    and "智慧农业" in tech[0].read_text(encoding="utf-8"),
                    "tech 全 meta → inbox-tech 富字典候选（含 title/intended）")
        ok += check((root / "kb/raw/leads/随手记.md").is_file(), "缺 sidecar → raw/leads 线索区")
        ok += check("待补源" in out and "随手记.md" in out, "报告点名催补缺 meta 文件")

    # 用例组 3：无 source_url 的 comp → 降级线索（未溯源不晋级）
    with tempfile.TemporaryDirectory(prefix="autoc_inbox_t3_") as td:
        root = Path(td)
        drop(root, "新比赛-通知.pdf", "kind: comp\ntitle: 新比赛\n")
        out = run_intake(root)
        total += 2
        ok += check((root / "kb/raw/leads/新比赛-通知.pdf").is_file(), "comp 无 source_url → 降级线索")
        ok += check(not list((root / "kb/raw/candidates").glob("inbox-comp-*.yaml")), "未溯源 comp 不进候选队列")

    # 用例组 4：配额 25 投 20 消费 5 留存（默认 quota=20，临时根无 budget.yaml）
    with tempfile.TemporaryDirectory(prefix="autoc_inbox_t4_") as td:
        root = Path(td)
        for i in range(25):
            drop(root, f"paper-{i:02d}.pdf", META.format(kind="tech", title=f"P{i}"))
        out = run_intake(root)
        remain = [p for p in (root / "kb/inbox").iterdir() if p.suffix == ".pdf"]
        total += 2
        ok += check(len(remain) == 5, f"超配额留存 5 个（实际 {len(remain)}）")
        ok += check("留存（超配额） 5" in out, "报告明示留存数")

    # 用例组 5：活跃战役提示（临时 state 含 kaggriculture，文件名命中 cid）
    with tempfile.TemporaryDirectory(prefix="autoc_inbox_t5_") as td:
        root = Path(td)
        (root / ".flow").mkdir(parents=True, exist_ok=True)
        (root / ".flow/state.json").write_text(json.dumps({
            "schema_version": 2, "phase": "idle",
            "campaigns": {"kaggriculture": {"phase": "deliver", "root": "workspace/kaggriculture"}},
        }), encoding="utf-8")
        drop(root, "kaggriculture-赛制更新.pdf", META.format(kind="comp", title="赛制更新"))
        out = run_intake(root)
        total += 1
        ok += check("与活跃战役 kaggriculture 相关" in out and "未改动战役文件" in out,
                    "命中活跃战役 → 报告提示且声明未改战役文件")

    print(f"[test_inbox] {ok}/{total} 通过")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
