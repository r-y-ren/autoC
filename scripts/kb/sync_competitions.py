#!/usr/bin/env python3
"""S-02 赛事信源快照与候选提取（sync_competitions）。

职责边界（紧循环）：抓取方向配置中的 web 信源 → 快照存档 kb/raw/snapshots/ →
按关键词提取候选赛事链接 → 候选队列 kb/raw/candidates/comp-<时间戳>.yaml。
**不做任何判断性入库**（建条目/获奖解构属 Scraper 角色）。

用法：
  python scripts/kb/sync_competitions.py [--direction 名称] [--dry-run] [--selftest]
退出码：0=正常（含零候选）；2=配置错误。
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
DEFAULT_KEYWORDS = ["竞赛", "大赛", "挑战杯", "互联网+", "数学建模", "hackathon",
                    "kaggle", "challenge", "competition", "创青春", "大创"]


def load_directions(direction_name: str | None) -> list[dict]:
    import yaml
    out = []
    for f in sorted((ROOT / "config" / "directions").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        cfg = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if not cfg.get("direction"):
            continue
        if direction_name and cfg["direction"] != direction_name:
            continue
        out.append(cfg)
    return out


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "autoC/0.1 sync_competitions"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


LINK_RE = re.compile(r"<a[^>]+href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def extract_candidates(page_html: str, base_url: str, keywords: list[str]) -> list[dict]:
    out = []
    for href, text in LINK_RE.findall(page_html):
        text = html.unescape(TAG_RE.sub("", text)).strip()
        if not text or len(text) > 80:
            continue
        if not any(k.lower() in text.lower() for k in keywords):
            continue
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = urllib.parse.urljoin(base_url, href)
        elif not href.startswith("http"):
            continue
        out.append({"title": text, "url": href, "found_on": base_url})
    return out


def selftest() -> int:
    page = ('<a href="/notice/1">关于举办2026年挑战杯的通知</a>'
            '<a href="https://other.com/c">Kaggle Competition X</a>'
            '<a href="/food">食堂菜单</a>')
    cands = extract_candidates(page, "https://edu.example.edu.cn/", DEFAULT_KEYWORDS)
    ok = len(cands) == 2 and cands[0]["url"].startswith("https://edu.example.edu.cn/")
    print(f"[sync_comp][selftest] {'PASS' if ok else 'FAIL'} 提取 {len(cands)} 条（期望 2，含相对链接补全）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="赛事信源快照与候选提取")
    ap.add_argument("--direction", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    cfgs = load_directions(args.direction)
    if not cfgs:
        print("[sync_comp] config/directions/ 下没有启用的方向配置")
        return 2

    snap_dir = ROOT / "kb" / "raw" / "snapshots"
    today = datetime.date.today().isoformat()
    candidates: list[dict] = []
    warnings: list[str] = []
    seen_urls: set[str] = set()

    for cfg in cfgs:
        keywords = list(cfg.get("keywords") or []) + DEFAULT_KEYWORDS
        for src in (cfg.get("sources") or {}).get("web") or []:
            url = src.get("url")
            if not url:
                continue
            try:
                page = fetch(url)
            except Exception as e:  # noqa: BLE001
                warnings.append(f"{url} 抓取失败: {e}")
                continue
            host = urllib.parse.urlparse(url).netloc.replace(":", "_")
            digest = hashlib.md5(url.encode()).hexdigest()[:8]
            if not args.dry_run:
                snap_dir.mkdir(parents=True, exist_ok=True)
                (snap_dir / f"{today}_{host}_{digest}.html").write_text(page, encoding="utf-8")
            for c in extract_candidates(page, url, keywords):
                if c["url"] in seen_urls:
                    continue
                seen_urls.add(c["url"])
                candidates.append(c)

    for w in warnings:
        print(f"[sync_comp][warn] {w}", file=sys.stderr)
    print(f"[sync_comp] 信源抓取完成 | 候选 {len(candidates)} | 快照目录 kb/raw/snapshots/")

    if args.dry_run or not candidates:
        return 0

    cand_dir = ROOT / "kb" / "raw" / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = cand_dir / f"comp-{stamp}.yaml"
    import yaml
    out.write_text(yaml.safe_dump(candidates, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[sync_comp] 候选队列 → {out.relative_to(ROOT)}")
    print("[sync_comp] 下一步：K-01 kb-sync 派发 Scraper 消费候选（核实后建 kb/competitions/ 条目）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
