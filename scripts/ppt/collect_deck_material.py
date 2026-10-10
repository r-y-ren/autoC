#!/usr/bin/env python3
"""PPT 取材器（spec #9 / issue#14）：读 fn-ladder 文件结构 → 内容简报 + 带来源标注的数据表。

针对 fn-ladder 产物布局取材（数据源改道：不再依赖 metrics.json 链）：
  fn_docs/requirements.md            → 目标段（R1..Rn）
  fn_docs/responsibility.md          → 方法段（职责树）
  fn_docs/implementation/functions.md→ 方法段（函数级状态）
  fn_work/runs/**、fn_docs/results/** → 实测数据表（数值逐项标注来源文件）
  fn_docs/acceptance.md              → 结论段（六道终检摘要）
缺失即降级点名（missing 清单）；--strict 下有缺失即 exit 1。
用法：python scripts/ppt/collect_deck_material.py --project <战役根> [--out-dir D] [--strict]
产物：deck_material.json（机器可读，供模板装配）+ deck_brief.md（人读简报）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQ_HEADING = re.compile(r"^#{1,3}\s*(R\d+)\s*(.*)$")
FUNC_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
FUNC_STATUS = re.compile(r"^(stub|implemented|tested|wired|blocked)\b")
NUM_PAIR = re.compile(r"([A-Za-z_][A-Za-z0-9_]{1,40})\s*[:=]\s*(-?\d+(?:\.\d+)?)(?![\w.])")


def parse_func_row(line: str) -> tuple[str, str] | None:
    """表格行 → (函数名, 状态)；兼容 2 列与 5 列（fn-implement 真实形态）布局。"""
    if not line.startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 2 or not FUNC_NAME.match(cells[0]):
        return None
    for c in cells[1:]:
        m = FUNC_STATUS.match(c)
        if m:
            return cells[0], m.group(1)
    return None


def project_root(cli_root: str | None) -> Path:
    import os
    if cli_root:
        return Path(cli_root).resolve()
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def collect_goals(docs: Path, missing: list[str]) -> list[dict]:
    p = docs / "requirements.md"
    if not p.is_file():
        missing.append("fn_docs/requirements.md")
        return []
    goals = []
    for line in read_text(p).splitlines():
        m = REQ_HEADING.match(line.strip())
        if m:
            goals.append({"id": m.group(1), "title": m.group(2).strip(),
                          "src": "fn_docs/requirements.md"})
    return goals


def collect_method(docs: Path, missing: list[str]) -> dict:
    tree_src = docs / "responsibility.md"
    funcs_src = docs / "implementation" / "functions.md"
    tracker_src = docs / "implementation" / "tracker.md"
    functions = []
    if funcs_src.is_file():
        for line in read_text(funcs_src).splitlines():
            m = parse_func_row(line)
            if m:
                functions.append({"name": m[0], "status": m[1],
                                  "src": "fn_docs/implementation/functions.md"})
    else:
        missing.append("fn_docs/implementation/functions.md")
    if not tree_src.is_file():
        missing.append("fn_docs/responsibility.md")
    tracker = None
    if tracker_src.is_file():
        text = read_text(tracker_src)
        done = len(re.findall(r"^\s*[-*]\s*\[x\]", text, re.I | re.M))
        todo = len(re.findall(r"^\s*[-*]\s*\[ \]", text, re.M))
        tracker = {"src": "fn_docs/implementation/tracker.md",
                   "steps_done": done, "steps_total": done + todo}
    return {"tree_src": "fn_docs/responsibility.md" if tree_src.is_file() else None,
            "tree_excerpt": "\n".join(read_text(tree_src).splitlines()[:12]) if tree_src.is_file() else "",
            "functions": functions, "tracker": tracker}


def collect_analyses(docs: Path) -> list[dict]:
    """fn_docs/analyses/ 三件套：分析报告与 registry（可选源，缺失不计 missing）。"""
    out: list[dict] = []
    adir = docs / "analyses"
    if adir.is_dir():
        for p in sorted(adir.glob("*.md")):
            head = next((ln.strip("# ").strip() for ln in read_text(p).splitlines()
                         if ln.strip().startswith("#")), p.stem)
            out.append({"title": head, "src": f"fn_docs/analyses/{p.name}"})
        reg = adir / "registry.jsonl"
        if reg.is_file():
            n = len([ln for ln in read_text(reg).splitlines() if ln.strip()])
            out.append({"title": f"分析台账 registry.jsonl（{n} 条）",
                        "src": "fn_docs/analyses/registry.jsonl"})
    return out


def collect_measured(proj: Path, missing: list[str]) -> list[dict]:
    out: list[dict] = []
    scan: list[Path] = []
    runs = proj / "fn_work" / "runs"
    results = proj / "fn_docs" / "results"
    for base in (runs, results):
        if base.is_dir():
            scan.extend(sorted(p for p in base.rglob("*") if p.is_file()))
    for p in scan:
        rel = str(p.relative_to(proj))
        if p.suffix == ".json":
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for k, v in _json_leaves(data):
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    out.append({"key": k, "value": v, "src": rel})
        elif p.suffix in (".log", ".txt", ".md"):
            for i, line in enumerate(read_text(p).splitlines(), 1):
                for m in NUM_PAIR.finditer(line):
                    out.append({"key": m.group(1), "value": float(m.group(2)),
                                "src": f"{rel}:{i}"})
    if not out:
        missing.append("实测为空（fn_work/runs 与 fn_docs/results 均无可提取数值）")
    return out


def _json_leaves(data, prefix: str = ""):
    if isinstance(data, dict):
        for k, v in data.items():
            yield from _json_leaves(v, f"{prefix}.{k}" if prefix else str(k))
    else:
        yield prefix, data


def collect_conclusion(docs: Path, missing: list[str]) -> list[dict]:
    p = docs / "acceptance.md"
    if not p.is_file():
        missing.append("fn_docs/acceptance.md")
        return []
    lines = [ln.strip() for ln in read_text(p).splitlines()
             if ln.strip() and not ln.strip().startswith("#")]
    return [{"line": ln, "src": "fn_docs/acceptance.md"} for ln in lines[:12]]


def render_brief(data: dict) -> str:
    out = [f"# 取材简报：{data['project']}", "",
           "> 由 collect_deck_material 生成；数字逐项标注来源文件，禁止引入来源外数字。", ""]
    out.append("## 目标")
    out += [f"- **{g['id']}** {g['title']}（{g['src']}）" for g in data["goals"]] or ["- （缺失）"]
    out.append("")
    out.append("## 方法")
    if data["method"]["tree_excerpt"]:
        out.append("```")
        out.append(data["method"]["tree_excerpt"])
        out.append("```")
    out += [f"- `{f['name']}`：{f['status']}（{f['src']}）" for f in data["method"]["functions"]] or ["- （缺失）"]
    out.append("")
    out.append("## 实测")
    out.append("| 指标 | 值 | 来源 |")
    out.append("|---|---|---|")
    out += [f"| {m['key']} | {m['value']} | {m['src']} |" for m in data["measured"]] or ["| — | — | （空） |"]
    out.append("")
    out.append("## 结论")
    out += [f"- {c['line']}（{c['src']}）" for c in data["conclusion"]] or ["- （缺失）"]
    out.append("")
    if data.get("analyses"):
        out.append("## 分析")
        out += [f"- {a['title']}　`{a['src']}`" for a in data["analyses"]]
        out.append("")
        if data["method"].get("tracker"):
            t = data["method"]["tracker"]
            out.append(f"> 步骤账本：{t['steps_done']}/{t['steps_total']} 步（`{t['src']}`）")
            out.append("")
    if data["missing"]:
        out.append("## 缺失")
        out += [f"- {m}" for m in data["missing"]]
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, help="项目/战役根（含 fn_docs/ 与 fn_work/）")
    ap.add_argument("--out-dir", help="产物输出目录（默认打印 JSON 到 stdout）")
    ap.add_argument("--strict", action="store_true", help="有缺失即 exit 1")
    args = ap.parse_args()

    proj = Path(args.project).resolve()
    if not proj.is_dir():
        print(f"取材失败：项目根不存在 {proj}", file=sys.stderr)
        return 1
    missing: list[str] = []
    data = {
        "project": proj.name,
        "goals": collect_goals(proj / "fn_docs", missing),
        "method": collect_method(proj / "fn_docs", missing),
        "measured": collect_measured(proj, missing),
        "conclusion": collect_conclusion(proj / "fn_docs", missing),
        "analyses": collect_analyses(proj / "fn_docs"),
        "missing": missing,
    }
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "deck_material.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out / "deck_brief.md").write_text(render_brief(data), encoding="utf-8")
        print(f"取材完成：{out}/deck_material.json + deck_brief.md（缺失 {len(missing)} 项）")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    if args.strict and missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
