#!/usr/bin/env python3
"""S-01 KB/契约条目校验器（lint_kb）。

模式：
  --hook              PostToolUse 钩子模式：stdin 读钩子输入，校验单个文件，
                      stderr 反馈结果，恒 exit 0（即时反馈不阻断；强制校验在 kb-sync 流程内）
  --file PATH         校验单个文件（按路径标记自动选择 schema）
  无参                 全量扫描 kb/competitions/*/meta.md 与 kb/tech/*.md
  --quarantine        全量模式下将不合格条目移入 kb/quarantine/（附 .reason 文件）

schema 判定（按路径标记，temp fixture 同样适用）：
  *blueprint.md*                          → blueprint.schema.json（YAML frontmatter）
  *acceptance*/*.json                     → acceptance.schema.json（JSON）
  */tech/* 或 tech/ 开头                   → tech-card.schema.json（YAML frontmatter）
  *competitions*                          → kb-meta.schema.json（YAML frontmatter）
  其余                                     → 跳过（exit 0）

退出码（CLI 模式）：0=全部通过/跳过；1=存在不合格。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "config" / "templates"
QUARANTINE = ROOT / "kb" / "quarantine"


def load_schema(name: str) -> dict:
    return json.loads((TEMPLATES / name).read_text(encoding="utf-8"))


def schema_for(path: str):
    p = path.replace("\\", "/").lower()
    if "blueprint.md" in p:
        return load_schema("blueprint.schema.json"), "yaml"
    if "acceptance" in p and p.endswith(".json"):
        return load_schema("acceptance.schema.json"), "json"
    if "/tech/" in p or p.startswith("tech/"):
        return load_schema("tech-card.schema.json"), "yaml"
    if "competitions" in p:
        return load_schema("kb-meta.schema.json"), "yaml"
    return None, None


def parse_frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return None, "缺少 frontmatter（--- YAML --- 分隔块）"
    import yaml
    try:
        return _normalize(yaml.safe_load(m.group(1))), None
    except Exception as e:  # noqa: BLE001
        return None, f"YAML 解析失败: {e}"


def _normalize(data):
    """YAML 会把无引号日期解析为 date 对象；schema 声明为 string，统一转 ISO 字符串。"""
    import datetime
    if isinstance(data, dict):
        return {k: _normalize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_normalize(v) for v in data]
    if isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()
    return data


def validate_path(path: Path) -> tuple[bool, str]:
    schema, kind = schema_for(str(path))
    if schema is None:
        return True, "skip（无对应 schema）"
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return False, f"读取失败: {e}"
    if kind == "json":
        try:
            data = json.loads(raw)
        except Exception as e:  # noqa: BLE001
            return False, f"JSON 解析失败: {e}"
    else:
        data, err = parse_frontmatter(raw)
        if err:
            return False, err
    import jsonschema
    try:
        jsonschema.validate(data, schema)
        return True, "OK"
    except jsonschema.ValidationError as e:
        loc = "/".join(str(x) for x in e.absolute_path) or "<root>"
        return False, f"schema 校验失败 @ {loc}: {e.message}"


def scan_targets() -> list[Path]:
    targets: list[Path] = []
    comp_root = ROOT / "kb" / "competitions"
    if comp_root.is_dir():
        targets += sorted(comp_root.glob("*/meta.md"))
    tech_root = ROOT / "kb" / "tech"
    if tech_root.is_dir():
        targets += sorted(p for p in tech_root.glob("*.md") if p.name != "README.md")
    return targets


def quarantine(path: Path, reason: str) -> Path:
    # kb/ 内的条目相对 kb/ 取路径（隔离区本身已在 kb/ 下），其余相对工程根
    try:
        rel = path.relative_to(ROOT / "kb")
    except ValueError:
        rel = path.relative_to(ROOT)
    dest = QUARANTINE / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest = dest.with_name(dest.name + f".{path.stat().st_mtime_ns}")
    shutil.move(str(path), str(dest))
    dest.with_suffix(dest.suffix + ".reason").write_text(
        reason + "\n", encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="autoC KB/契约条目校验器")
    ap.add_argument("--hook", action="store_true", help="PostToolUse 钩子模式")
    ap.add_argument("--file", type=str, default=None, help="校验单个文件")
    ap.add_argument("--quarantine", action="store_true", help="全量模式下隔离不合格条目")
    args = ap.parse_args()

    if args.hook:
        try:
            payload = json.load(sys.stdin)
            file_path = (payload.get("tool_input") or {}).get("file_path") or ""
        except Exception:  # noqa: BLE001
            return 0
        if not file_path:
            return 0
        ok, msg = validate_path(Path(file_path))
        if not ok:
            print(f"[lint_kb] 该文件未通过契约校验：{msg}\n"
                  f"[lint_kb] 请修复后重写；连续不合格会在全量 lint 时被移入 kb/quarantine/。",
                  file=sys.stderr)
        else:
            print(f"[lint_kb] 校验通过：{msg}", file=sys.stderr)
        return 0

    if args.file:
        ok, msg = validate_path(Path(args.file))
        print(("PASS " if ok else "FAIL ") + str(args.file) + f"  [{msg}]")
        return 0 if ok else 1

    targets = scan_targets()
    if not targets:
        print("[lint_kb] kb/ 下暂无条目，无事可校验")
        return 0
    failures = 0
    for t in targets:
        ok, msg = validate_path(t)
        rel = t.relative_to(ROOT)
        if ok:
            print(f"PASS {rel}")
        else:
            failures += 1
            print(f"FAIL {rel}  [{msg}]")
            if args.quarantine:
                dest = quarantine(t, msg)
                print(f"     ↳ 已隔离 → {dest.relative_to(ROOT)}")
    print(f"[lint_kb] {len(targets)} 条目，{failures} 不合格")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
