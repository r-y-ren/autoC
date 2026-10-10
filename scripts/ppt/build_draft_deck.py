#!/usr/bin/env python3
"""PPT 初稿装配器（spec #9 / issue#15）：取材器数据 + 模板 → 答辩初稿 deck。

两段式产线的产稿段自动化：把 collect_deck_material.py 的 deck_material.json 按
config/templates/ppt/deck-template.marp.md 的注入标记装配成五段初稿；数字只来自
取材器数据表（保留来源标注），无来源数字不上片。
用法：python scripts/ppt/build_draft_deck.py --material D/deck_material.json
        [--template T] [--out draft_deck.md] [--title 标题]
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).resolve().parents[2] / "config/templates/ppt/deck-template.marp.md"
MARKERS = ("cover", "goals", "method", "measured", "compare", "summary")


def fill_goals(data: dict) -> str:
    if not data["goals"]:
        return "- （需求缺失：fn_docs/requirements.md 未取到 R 条目）"
    return "\n".join(f"- **{g['id']}** {g['title']}　`{g['src']}`" for g in data["goals"])


def fill_method(data: dict) -> str:
    out = []
    m = data["method"]
    if m.get("tree_excerpt"):
        out += ["```", m["tree_excerpt"], "```"]
    if m["functions"]:
        out += [f"- `{f['name']}`：**{f['status']}**　`{f['src']}`" for f in m["functions"]]
    else:
        out.append("- （实现状态缺失：implementation/functions.md 未取到）")
    return "\n".join(out)


def fill_measured(data: dict) -> str:
    if not data["measured"]:
        return "（实测为空——数据表无可用数值，禁用占位数字）"
    out = ["| 指标 | 值 | 来源 |", "|---|---|---|"]
    out += [f"| {m['key']} | {m['value']} | `{m['src']}` |" for m in data["measured"]]
    return "\n".join(out)


def fill_compare(data: dict) -> str:
    meas = {m["key"]: m for m in data["measured"]}
    rows = ["| 目标 | 对应实测 | 来源 |", "|---|---|---|"]
    used = set()
    for g in data["goals"]:
        hit = next((k for k in meas if k.lower() in g["title"].lower()
                    or g["title"].lower() in k.lower()), None)
        if hit:
            used.add(hit)
            rows.append(f"| {g['id']} {g['title']} | {hit}={meas[hit]['value']} | `{meas[hit]['src']}` |")
        else:
            rows.append(f"| {g['id']} {g['title']} | （无同名实测项） | — |")
    extra = [k for k in meas if k not in used]
    if extra:
        rows.append("| — 其他实测 — | " + "、".join(f"{k}={meas[k]['value']}" for k in extra[:6]) + " | 见实测页 |")
    return "\n".join(rows)


def fill_summary(data: dict) -> str:
    out = [f"- 结论（来自六道终检）：" if data["conclusion"] else "- （终检缺失：fn_docs/acceptance.md）"]
    out += [f"  - {c['line']}" for c in data["conclusion"][:6]]
    if data["missing"]:
        out.append("- **缺失注记**（不得用占位数字顶替）：")
        out += [f"  - {m}" for m in data["missing"]]
    return "\n".join(out)


def fill_cover(data: dict, title: str) -> str:
    today = datetime.date.today().isoformat()
    return (f"- 项目：**{data['project']}**｜日期：{today}\n"
            f"- 性质：答辩初稿（产稿段自动生成；数字均带来源标注，见各页脚注）\n"
            f"- 标题：{title}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--material", required=True, help="deck_material.json 路径")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--out", default="draft_deck.md")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    data = json.loads(Path(args.material).read_text(encoding="utf-8"))
    title = args.title or f"{data['project']} 答辩初稿"
    tpl = Path(args.template).read_text(encoding="utf-8")
    fills = {
        "cover": fill_cover(data, title),
        "goals": fill_goals(data),
        "method": fill_method(data),
        "measured": fill_measured(data),
        "compare": fill_compare(data),
        "summary": fill_summary(data),
    }
    out = tpl.replace("{{title}}", title)
    for name in MARKERS:
        out = out.replace(f"<!--@{name}-->", fills[name])
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"初稿已装配：{args.out}（五段注入完成，缺失 {len(data.get('missing', []))} 项）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
