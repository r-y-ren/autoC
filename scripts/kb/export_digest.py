#!/usr/bin/env python3
"""S-15 方向情报简报导出（export_digest）。

知识库交付层（D6 裁决：读者=自用·团队决策输入；每 3 天跑批末尾刷新，当月最后一次
跑批转正式版，D7 节奏）。**只重组不新增**：一切数字与结论来自条目层，导出物逐条回链条目 ID；
分析增量只允许发生在 kb/ 条目层，本脚本是纯投影。

产出：export/digest-<方向>-<YYYY-MM>.md
  - 赛事日历（关键日期倒计时，按最近日期排序）
  - 技术雷达速览（近期发表卡片 + 比赛映射）
  - 模式库要点（patterns.md 第五节"对 autoC 战役的启示"整段引用）
  - 合规提醒（各赛 AI 政策摘要）
用法：python scripts/kb/export_digest.py [--direction 名称] [--formal] [--interval-days 3] [--selftest]
版本判定：缺省自动——按跑批节奏（--interval-days，默认 3，对齐每 3 天 cron）推算，
下一次跑批已跨月 ⇒ 本次为当月最后一次跑批 ⇒ 正式版。
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
SECTION_RE = re.compile(r"^##\s+[一二三四五六七八九十]+\s*、\s*(.+)$", re.M)


def frontmatter_of(text: str) -> dict:
    import yaml
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:  # noqa: BLE001
        return {}
    # YAML 会把无引号日期解析为 date 对象（新方向条目实测踩坑）——与 lint_kb._normalize 同口径转 ISO
    def _norm(v):
        if isinstance(v, dict):
            return {k: _norm(x) for k, x in v.items()}
        if isinstance(v, list):
            return [_norm(x) for x in v]
        if isinstance(v, (datetime.date, datetime.datetime)):
            return v.isoformat()
        return v
    return _norm(data)


def load_meta(path: Path) -> dict:
    return frontmatter_of(path.read_text(encoding="utf-8"))


def days_until(date_str: str, today: datetime.date) -> int | None:
    m = DATE_RE.search(date_str or "")
    if not m:
        return None
    try:
        return (datetime.date.fromisoformat(m.group(1)) - today).days
    except ValueError:
        return None


def is_last_saturday(today: datetime.date) -> bool:
    """兼容保留：今天须为周六且下一周六跨月（旧的周六节奏判定）。"""
    if today.weekday() != 5:
        return False
    nxt = today + datetime.timedelta(days=7)
    return nxt.month != today.month


def is_last_run_of_month(today: datetime.date, interval_days: int) -> bool:
    """下一次跑批（today + interval）已跨月 ⇒ 本次为当月最后一次跑批（D7 节奏判定）。"""
    return (today + datetime.timedelta(days=interval_days)).month != today.month


def extract_section_five(text: str) -> str:
    """patterns.md 第五节（到下一个 ## 或文末），模板锚点见 patterns-template.md。"""
    m = re.search(r"^##\s*五\s*、.*?$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    body = rest[:nxt.start()] if nxt else rest
    return body.strip()


def build_digest(direction: str, today: datetime.date, formal: bool) -> str:
    comps_dir = ROOT / "kb" / "competitions"
    comps = []
    for meta in sorted(comps_dir.glob("*/meta.md")):
        fm = load_meta(meta)
        if direction in (fm.get("directions") or []):
            comps.append((meta.parent.name, fm))

    tech = []
    for card in sorted((ROOT / "kb" / "tech").glob("*.md")):
        fm = load_meta(card)
        if fm:
            tech.append(fm)

    lines: list[str] = []
    tag = "正式版（月度）" if formal else "草稿（每3天跑批刷新）"
    lines += [f"# 方向情报简报：{direction} —— {today.strftime('%Y-%m')}",
              "",
              f"> 版本：{tag}｜生成：{today.isoformat()}｜来源：kb/ 条目层纯投影（D6），"
              f"每条结论回链条目 ID；分析增量只进条目层。", ""]

    # ── 赛事日历 ──
    lines += ["## 赛事日历（按最近关键日期排序）", ""]
    cal = []
    for cid, fm in comps:
        items = []
        for label, v in (fm.get("key_dates") or {}).items():
            date_s = v.get("date", "") if isinstance(v, dict) else str(v)
            d = days_until(date_s, today)
            verified = isinstance(v, dict) and v.get("verified")
            mark = "" if (not verified and re.search(r"未核实|待公布", date_s)) else ("✓" if verified else "未核实")
            items.append((d if d is not None else 10**6, label, date_s, mark))
        items.sort()
        future = [d for d, *_ in items if 0 <= d < 10**6]
        # 有未来日期的按最近未来排；全过去的赛事沉底（10^5 段），其内部再按最近过去排序
        cal.append((min(future) if future else 10**5 + (items[0][0] if items else 0), cid, fm, items))
    cal.sort(key=lambda x: x[0])
    for _, cid, fm, items in cal:
        lines.append(f"### {fm.get('name', cid)}（`{cid}`｜{fm.get('status', '?')}｜"
                     f"核验 {fm.get('last_verified', '?')}）")
        for d, label, date_s, mark in items:
            dd = f"{d:+d}天" if d != 10**6 else ""
            lines.append(f"- {label}：{date_s}{f'（{mark}）' if mark else ''} {dd}")
        lines.append("")

    # ── 技术雷达 ──
    # 技术雷达：按方向过滤（tech-card.directions；旧卡未回填前不会出现在方向简报中）
    dir_tech = [t for t in tech if direction in (t.get("directions") or [])]
    recent = [t for t in dir_tech if days_until(t.get("published", ""), today) is not None
              and -60 <= days_until(t.get("published", ""), today) <= 60]
    lines += [f"## 技术雷达速览（本方向 {len(dir_tech)} 卡，近 60 天发表 {len(recent)} 张；库内共 {len(tech)} 卡）", "",
              "| ID | 领域 | 成熟度 | 比赛映射 |", "|---|---|---|---|"]
    for t in dir_tech:
        fits = "、".join(str(c.get("track")) for c in t.get("competition_fit") or [])
        lines.append(f"| {t.get('id')} | {('、'.join(t.get('field') or []))[:30]} "
                     f"| {t.get('maturity')} | {fits[:40]} |")
    lines.append("")

    # ── 模式库要点 ──
    lines += ["## 模式库要点（patterns 第五节原文）", ""]
    got = False
    for cid, _ in comps:
        p = comps_dir / cid / "patterns.md"
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        five = extract_section_five(text)
        if not five:
            continue
        got = True
        cov = re.search(r"^coverage:\s*(.+)$", text, re.M)
        conf = re.search(r"^confidence:\s*(.+)$", text, re.M)
        lines.append(f"### {cid}（coverage: {cov.group(1).strip() if cov else '?'}"
                     f"｜confidence: {conf.group(1).strip() if conf else '?'}）")
        lines += ["", five, ""]
    if not got:
        lines += ["（本方向暂无已解构 patterns——由每 3 天深度跑批推进）", ""]

    # ── 合规提醒 ──
    lines += ["## 合规提醒（AI 政策摘要，全文见各条目）", ""]
    for cid, fm in comps:
        pol = ((fm.get("ai_policy") or {}).get("summary") or "")[:120]
        lines.append(f"- **{cid}**：{pol}…")
    lines += ["", "---", f"生成者：scripts/kb/export_digest.py｜读者：团队自用（D6 裁决）",
              ""]
    return "\n".join(lines)


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        global ROOT
        old = ROOT
        try:
            ROOT = Path(td)
            (ROOT / "kb" / "competitions" / "demo" ).mkdir(parents=True)
            (ROOT / "kb" / "competitions" / "demo" / "meta.md").write_text(
                "---\nid: demo\nname: 演示赛\ndirections: [测试方向]\nstatus: active\n"
                "key_dates:\n  开赛:\n    {date: '2999-01-01 08:00', verified: true}\n"
                "ai_policy: {summary: 允许使用但须声明}\nlast_verified: '2026-08-27'\n---\n正文",
                encoding="utf-8")
            (ROOT / "kb" / "tech").mkdir(parents=True)
            today = datetime.date(2026, 8, 27)
            out = build_digest("测试方向", today, formal=False)
            ok = ("演示赛" in out and "2999-01-01" in out and "允许使用但须声明" in out
                  and "纯投影" in out and "暂无已解构 patterns" in out)
            # 月末判定（D7 每3天节奏，与星期无关）：08-29（周六，+3 跨月）与 08-30（周日，+3 跨月）
            # 都应为正式版日；08-27（+3=08-30 同月）为草稿日——证明判定只看跨月不看星期几
            ok = ok and is_last_run_of_month(datetime.date(2026, 8, 29), 3) \
                and is_last_run_of_month(datetime.date(2026, 8, 30), 3) \
                and not is_last_run_of_month(datetime.date(2026, 8, 27), 3)
            print(f"[export_digest][selftest] {'PASS' if ok else 'FAIL'} 简报聚合与月末判定")
            return 0 if ok else 1
        finally:
            ROOT = old


def main() -> int:
    ap = argparse.ArgumentParser(description="方向情报简报导出（D6 交付层）")
    ap.add_argument("--direction", default=None, help="限定方向（缺省=全部启用方向各一份）")
    ap.add_argument("--formal", action="store_true", help="强制正式版（缺省按月末最后一次跑批自动判定）")
    ap.add_argument("--interval-days", type=int, default=3,
                    help="跑批间隔天数（跨月判定用，对齐 cron 节奏；D7 合并为每 3 天）")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    import yaml
    names = []
    for f in sorted((ROOT / "config" / "directions").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        cfg = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if cfg.get("direction"):
            names.append(cfg["direction"])
    if args.direction:
        names = [d for d in names if d == args.direction]
    if not names:
        print("[export_digest] 无启用方向（config/directions/）", file=sys.stderr)
        return 2

    today = datetime.date.today()
    formal = args.formal or is_last_run_of_month(today, args.interval_days)
    outdir = ROOT / "export"
    outdir.mkdir(exist_ok=True)
    for d in names:
        out = outdir / f"digest-{d}-{today.strftime('%Y-%m')}.md"
        out.write_text(build_digest(d, today, formal), encoding="utf-8")
        print(f"[export_digest] {d} → {out.relative_to(ROOT)}（{'正式版' if formal else '草稿'}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
