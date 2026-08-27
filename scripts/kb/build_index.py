#!/usr/bin/env python3
"""S-04 KB 总索引重建（build_index）。

扫描 kb/competitions/*/meta.md 与 kb/tech/*.md 的 frontmatter，重建 kb/INDEX.md
的两张表；「跑批记录」表为 append-only，从既有 INDEX 原样保留。

用法：python scripts/kb/build_index.py [--selftest]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
INDEX = ROOT / "kb" / "INDEX.md"

HEADER = """# KB 总索引（瘦协调者唯一入口）

> 由慢循环跑批脚本（scripts/kb/build_index.py）自动重建。**主会话只读本文件做决策路由，不逐条读取条目正文**（分片派发时由子 agent 按需读）。

## KB-1 赛事库（交付物 1）

| ID | 赛事 | 方向 | 层级 | 状态 | 关键日期 | AI 政策 | 最近核验 | 条目路径 |
|---|---|---|---|---|---|---|---|---|
{comp_rows}

## KB-2 科技库（交付物 2）

| ID | 名称 | 领域 | 方向 | 成熟度 | 比赛映射 | 发表 | 最近核验 |
|---|---|---|---|---|---|---|---|
{tech_rows}

## 跑批记录

| 日期 | 类型 | 新增 | 更新 | 隔离 | 成本 | 说明 |
|---|---|---|---|---|---|---|
<!-- 成本列=分片数/token/墙钟（T4.3 起新行必填；旧行无此列属历史格式） -->
{run_rows}
"""


def frontmatter(path: Path) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}
    import yaml
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:  # noqa: BLE001
        return {}


def preserve_run_log() -> str:
    """从既有 INDEX 提取跑批记录表的数据行（append-only 语义）。

    逐行收集以 "|" 开头的表格行：正则惰性匹配会在数据行行首 "|" 处提前断开，
    多行记录只剩第一行（T2.1 修复的 P1 缺陷），故改为行级状态机。
    """
    if not INDEX.exists():
        return ""
    in_section = False
    table: list[str] = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("## 跑批记录"):
            in_section = True
            continue
        if not in_section:
            continue
        if s.startswith("|"):
            table.append(s)
        elif s.startswith("<!--"):
            continue  # 表头与数据行间的 HTML 注释（T4.3 成本列说明）不终止收集
        elif table and s:
            break  # 表格结束（遇到非表格正文或新章节）
    return "\n".join(table[2:])  # 跳过表头与分隔行，其余全部保留


def cell(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, list):
        return "、".join(str(x) for x in v)
    return str(v).replace("|", "\\|").replace("\n", " ")


def key_dates_compact(kd) -> str:
    """key_dates 自由对象 → 紧凑串，如 `报名:2026-09-01、初赛:2026-10-15`。超长按整条边界截断。"""
    if not isinstance(kd, dict) or not kd:
        return "-"
    parts = []
    for k, v in kd.items():
        d = v.get("date") if isinstance(v, dict) else v
        parts.append(f"{k}:{d if d is not None else '?'}")
    out = []
    for p in parts:  # 截断只发生在条目边界，不切半个日期
        if len("、".join(out + [p])) > 60:
            return "、".join(out) + "…"
        out.append(p)
    return "、".join(out)


def build() -> str:
    import yaml  # noqa: F401 （frontmatter 依赖）
    comp_rows, tech_rows = [], []
    comp_root = ROOT / "kb" / "competitions"
    if comp_root.is_dir():
        for d in sorted(comp_root.iterdir()):
            meta = d / "meta.md"
            if not meta.is_file():
                continue
            fm = frontmatter(meta)
            if not fm:
                continue
            comp_rows.append(
                f"| {cell(fm.get('id'))} | {cell(fm.get('name'))} | {cell(fm.get('directions'))} "
                f"| {cell(fm.get('tier'))} | {cell(fm.get('status'))} "
                f"| {cell(key_dates_compact(fm.get('key_dates')))} "
                f"| {cell((fm.get('ai_policy') or {}).get('summary', '-'))[:40]} "
                f"| {cell(fm.get('last_verified'))} | competitions/{d.name}/ |")
    tech_root = ROOT / "kb" / "tech"
    if tech_root.is_dir():
        for f in sorted(tech_root.glob("*.md")):
            fm = frontmatter(f)
            if not fm:
                continue
            fits = "、".join(str(c.get("track")) for c in fm.get("competition_fit") or [])
            tech_rows.append(
                f"| {cell(fm.get('id'))} | {cell(fm.get('name'))} | {cell(fm.get('field'))} "
                f"| {cell(fm.get('directions'))} "
                f"| {cell(fm.get('maturity'))} | {cell(fits)} "
                f"| {cell(fm.get('published'))} | {cell(fm.get('sources') and '已引' or '-')} |")
    return HEADER.format(
        comp_rows="\n".join(comp_rows) or "<!-- 暂无条目 -->",
        tech_rows="\n".join(tech_rows) or "<!-- 暂无条目 -->",
        run_rows=preserve_run_log() or "<!-- 慢循环每次跑批追加 -->")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        fm = frontmatter(Path(__file__))
        ok = fm == {}  # 本文件非 md，frontmatter 应返回空
        print(f"[build_index][selftest] {'PASS' if ok else 'FAIL'} frontmatter 解析健壮性")
        return 0 if ok else 1
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(build(), encoding="utf-8")
    print(f"[build_index] 索引重建 → {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
