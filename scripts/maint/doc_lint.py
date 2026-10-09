#!/usr/bin/env python3
"""doc_lint：工作流文档一致性检查（spec #9 / issue#10，prefactor 红灯基线）。

对命令/技能/agents/模板/docs/README/AGENTS 的文本做四类外部行为断言：
  R1 脚本引用存在性：文中引用的 scripts/.../*.py 必须真实存在
  R2 多战役调用：init_state 的战役阶段流转（decide/deliver/verify/archive）与 --reset
     必须带 --campaign（v2 多战役口径）
  R3 v1 平铺路径：workspace/ 直挂产物路径（容器说明 README/JOURNAL 除外）必须改
     战役根占位（workspace/<cid>/…）
  R4 旧插件名：document-skills 已更名拆分，不得再引用
用法：python scripts/maint/doc_lint.py [--root R] [--only <路径子串>]
输出每行 "VIOLATION <类别>:<文件>:<行>: [规则] 说明"；有违规 exit 1。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CATEGORIES = {
    "commands": ".zcode/commands",
    "skills": ".zcode/skills",
    "agents": ".zcode/agents",
    "templates": "config/templates",
    "docs": "docs",
    "readme": "README.md",
    "agentsmd": "AGENTS.md",
}

SCRIPT_REF = re.compile(r"scripts/[a-z_]+/[A-Za-z0-9_]+\.py")
INIT_LINE = re.compile(r"init_state")
PHASE = re.compile(r"--phase\s+(\w+)")
CAMPAIGN_PHASES = {"decide", "deliver", "verify", "archive"}
V1_PATH = re.compile(
    r"workspace/(?!README\.md\b|JOURNAL\.md\b|<cid>|<未登记id>|<战役id>)"
    r"(?:blueprint\.md\b|acceptance\b|software\b|hardware\b|docs\b|references\b|metrics\.json\b|strategy\b)")
OLD_PLUGIN = re.compile(r"document-skills")


def project_root(cli_root: str | None) -> Path:
    import os
    if cli_root:
        return Path(cli_root).resolve()
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def iter_files(root: Path, only: str | None):
    for cat, rel in CATEGORIES.items():
        base = root / rel
        if only and only not in rel and only not in cat:
            continue
        if base.is_file():
            yield cat, base
        elif base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file() and p.suffix in (".md", ".json", ".yaml", ".yml", ".typ", ".txt"):
                    yield cat, p


def check_line(root: Path, rel_file: str, lineno: int, line: str) -> list[str]:
    out: list[str] = []
    for m in SCRIPT_REF.finditer(line):
        if not (root / m.group(0)).is_file():
            out.append(f"[R1] 引用不存在的脚本 {m.group(0)}")
    if INIT_LINE.search(line):
        phases = PHASE.findall(line)
        need = any(p in CAMPAIGN_PHASES for p in phases) or "--reset" in line
        if need and "--campaign" not in line:
            out.append("[R2] 多战役调用缺 --campaign")
    for m in V1_PATH.finditer(line):
        out.append(f"[R3] v1 平铺路径 {m.group(0)}（应为 workspace/<cid>/…）")
    if OLD_PLUGIN.search(line):
        out.append("[R4] 旧插件名 document-skills（已更名拆分为 documents/pdf/presentations/spreadsheets）")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", help="主库根（默认 ZCODE_PROJECT_DIR 或脚本推断）")
    ap.add_argument("--only", help="只扫路径/类别含此子串的域，如 commands / templates / docs")
    args = ap.parse_args()
    root = project_root(args.root)
    total = 0
    for cat, path in iter_files(root, args.only):
        rel = str(path.relative_to(root))
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as e:
            print(f"VIOLATION {cat}:{rel}:0: [IO] 无法读取：{e}")
            total += 1
            continue
        for i, line in enumerate(lines, 1):
            for msg in check_line(root, rel, i, line):
                print(f"VIOLATION {cat}:{rel}:{i}: {msg}")
                total += 1
    if total:
        print(f"doc_lint：{total} 处违规")
        return 1
    print("doc_lint：全绿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
