#!/usr/bin/env python3
"""S-01 KB/契约条目校验器（lint_kb）。

模式：
  --hook              PostToolUse 钩子模式：stdin 读钩子输入，校验单个文件，
                      stderr 反馈结果，恒 exit 0（即时反馈不阻断；强制校验在 kb-sync 流程内）
  --file PATH         校验单个文件（按路径标记自动选择 schema）
  无参                 全量扫描 kb/competitions/*/meta.md 与 kb/tech/*.md
  --quarantine        全量模式下将不合格条目移入 kb/quarantine/（附 .reason 文件）

schema 判定（精确结构匹配，任意路径前缀下按尾部结构识别）：
  .../competitions/<id>/meta.md     → kb-meta.schema.json（YAML frontmatter）
  .../tech/<id>.md                  → tech-card.schema.json（YAML frontmatter，仅直接子文件）
  .../blueprint.md                  → blueprint.schema.json（YAML frontmatter）
  .../acceptance/<file>.json        → acceptance.schema.json（JSON）
明确跳过（不校验，正文/原料类文件暂无 schema，需要时另立）：
  kb/raw/**、competitions/<id>/winners/**、patterns.md、各级 README.md、其余一切不匹配者
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

# (正则, schema 文件, 数据形态) —— 在小写正斜杠路径上匹配尾部结构
RULES = [
    (re.compile(r"(?:^|/)competitions/[^/]+/meta\.md$"), "kb-meta.schema.json", "yaml"),
    (re.compile(r"(?:^|/)tech/[^/]+\.md$"), "tech-card.schema.json", "yaml"),
    (re.compile(r"(?:^|/)blueprint\.md$"), "blueprint.schema.json", "yaml"),
    (re.compile(r"(?:^|/)acceptance/[^/]+\.json$"), "acceptance.schema.json", "json"),
]


def load_schema(name: str) -> dict:
    return json.loads((TEMPLATES / name).read_text(encoding="utf-8"))


def schema_for(path: str):
    p = path.replace("\\", "/").lower()
    if p.endswith("readme.md"):
        return None, None
    for rx, name, kind in RULES:
        if rx.search(p):
            return load_schema(name), kind
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
        # FormatChecker 启用 "format": "date" 等格式校验（默认不校验，错误日期会漏过）
        jsonschema.validate(data, schema, format_checker=jsonschema.FormatChecker())
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


# ---------- 正文层轻结构检查（--structure；WARN 级，不隔离） ----------
# 正文层（winners/patterns/surveys）无 schema，结构合规靠模板；此处只验三件事：
# frontmatter 存在且可解析、必备键齐、模板必备节存在。历史遗留（如旧五节 patterns）会如实 WARN。

def _fm_ok(text: str) -> tuple[bool, dict]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return False, {}
    try:
        import yaml
        return True, yaml.safe_load(m.group(1)) or {}
    except Exception:  # noqa: BLE001
        return False, {}


def check_structure(path: Path) -> tuple[bool, str]:
    """返回 (结构完好, 说明)。目标：winners/<年>.md、patterns.md、tech/_surveys/*.md。"""
    rel = path.relative_to(ROOT).as_posix().lower()
    text = path.read_text(encoding="utf-8", errors="replace")
    ok, fm = _fm_ok(text)
    if not ok:
        return False, "正文层：frontmatter 缺失或不可解析（检查闭合 --- ）"
    if re.search(r"(?:^|/)winners/[^/]+\.md$", rel):
        need = ["competition_id", "year", "sources"]
        miss = [k for k in need if k not in fm]
        if miss:
            return False, f"winners：frontmatter 缺 {miss}"
        if "数据缺口" not in text:
            return False, "winners：缺『数据缺口声明』节（模板第三节）"
        if "骨架" in text and "不足与可改进点" not in text:
            return False, "winners：含深构条目但缺『不足与可改进点』必备节"
        return True, "winners 结构 OK"
    if re.search(r"(?:^|/)patterns\.md$", rel):
        need = ["competition_id", "last_verified", "coverage", "confidence"]
        miss = [k for k in need if k not in fm]
        if miss:
            return False, f"patterns：frontmatter 缺 {miss}"
        secs = ["评审偏好", "方法论分布", "差异化点", "反面观察", "赛点检查表", "启示"]
        miss_s = [s for s in secs if s not in text]
        if miss_s:
            return False, f"patterns：缺必备节 {miss_s}（六节模板）"
        return True, "patterns 结构 OK"
    if "_surveys/" in rel:
        need = ["family", "cards", "last_verified", "confidence"]
        miss = [k for k in need if k not in fm]
        if miss:
            return False, f"survey：frontmatter 缺 {miss}"
        if "对比矩阵" not in text or "选型结论" not in text:
            return False, "survey：缺『对比矩阵』或『选型结论』节"
        return True, "survey 结构 OK"
    return True, "非结构检查目标"


def structure_targets() -> list[Path]:
    targets: list[Path] = []
    comp_root = ROOT / "kb" / "competitions"
    if comp_root.is_dir():
        targets += sorted(comp_root.glob("*/winners/*.md"))
        targets += sorted(comp_root.glob("*/patterns.md"))
    surv = ROOT / "kb" / "tech" / "_surveys"
    if surv.is_dir():
        targets += sorted(surv.glob("*.md"))
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
    ap.add_argument("--structure", action="store_true", help="只跑正文层结构检查（WARN 级）")
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
        st_ok, st_msg = check_structure(Path(args.file))
        line = ("PASS " if ok else "FAIL ") + str(args.file) + f"  [{msg}]"
        if not st_ok:
            line += f"  [WARN {st_msg}]"
        print(line)
        return 0 if ok else 1

    # --structure：只跑正文层结构检查（WARN 级，不隔离、不返回非零）
    if args.structure:
        stargets = structure_targets()
        warns = 0
        for t in stargets:
            ok, msg = check_structure(t)
            rel = t.relative_to(ROOT)
            print(f"{'PASS' if ok else 'WARN'} {rel}  [{msg}]")
            warns += 0 if ok else 1
        print(f"[lint_kb][structure] {len(stargets)} 个正文层文件，{warns} 结构告警")
        return 0

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
    # 全量模式顺带跑正文层结构（WARN 级——不隔离、不影响退出码；待升格项如实亮出）
    for t in structure_targets():
        ok, msg = check_structure(t)
        if not ok:
            print(f"WARN {t.relative_to(ROOT)}  [{msg}]")
    print(f"[lint_kb] {len(targets)} 条目，{failures} 不合格")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
