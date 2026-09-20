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
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:  # E-17 trafilatura（D15）：autoc venv 运行时启用，无环境自动降级
    import trafilatura
except ImportError:
    trafilatura = None


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


def extract_main_text(page_html: str) -> str | None:
    """trafilatura 正文降噪（E-17，D15）：产出快照旁的 .extract.md sidecar；缺席/失败返回 None。"""
    if trafilatura is None:
        return None
    try:
        return trafilatura.extract(page_html, output_format="markdown",
                                   include_links=True) or None
    except Exception:  # noqa: BLE001
        return None


def selftest() -> int:
    page = ('<a href="/notice/1">关于举办2026年挑战杯的通知</a>'
            '<a href="https://other.com/c">Kaggle Competition X</a>'
            '<a href="/food">食堂菜单</a>')
    cands = extract_candidates(page, "https://edu.example.edu.cn/", DEFAULT_KEYWORDS)
    ok = len(cands) == 2 and cands[0]["url"].startswith("https://edu.example.edu.cn/")
    side = extract_main_text('<html><head><title>通知</title></head><body>'
                             '<main><h1>2026年挑战杯通知</h1><p>赛程正文。</p></main></body></html>')
    # trafilatura 在场必须抽出正文（集成损坏可见）；缺席则必须干净降级为 None
    side_ok = ("挑战杯" in side) if trafilatura is not None else (side is None)
    print(f"[sync_comp][selftest] {'PASS' if ok and side_ok else 'FAIL'} 提取 {len(cands)} 条（期望 2，含相对链接补全）；"
          f"sidecar 抽取={'trafilatura' if trafilatura else '缺席降级'}/{side_ok}")
    return 0 if ok and side_ok else 1


def same_host_interval() -> float:
    """同主机抓取间隔（秒），读 budget.yaml → rate_limit.same_host_interval_ms（落脚本，T-audit 项）。"""
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "config" / "budget.yaml").read_text(encoding="utf-8"))
        return float((((cfg or {}) or {}).get("rate_limit") or {}).get("same_host_interval_ms") or 0) / 1000.0
    except Exception:  # noqa: BLE001
        return 0.0


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
    extracted = 0

    interval = same_host_interval()
    last_hit: dict[str, float] = {}
    for cfg in cfgs:
        keywords = list(cfg.get("keywords") or []) + DEFAULT_KEYWORDS
        for src in (cfg.get("sources") or {}).get("web") or []:
            url = src.get("url")
            if not url:
                continue
            render = str(src.get("render") or "").lower()
            if render in ("spa", "api"):
                # SPA 锚点：urllib 只能拿到空壳；API 锚点：JSON 无链接可提取——
                # 两者均交主会话预抓/预处理（P1 机制），避免空壳快照污染 kb/raw/snapshots/
                print(f"[sync_comp][skip] {render} 锚点交主会话处理（catalog 规则）：{src.get('name') or url}",
                      file=sys.stderr)
                continue
            host = urllib.parse.urlparse(url).netloc
            wait = last_hit.get(host, 0.0) + interval - time.time()
            if wait > 0:
                time.sleep(wait)
            try:
                page = fetch(url)
            except Exception as e:  # noqa: BLE001
                warnings.append(f"{url} 抓取失败: {e}")
                last_hit[host] = time.time()
                continue
            last_hit[host] = time.time()
            host_file = host.replace(":", "_")
            digest = hashlib.md5(url.encode()).hexdigest()[:8]
            if not args.dry_run:
                snap_dir.mkdir(parents=True, exist_ok=True)
                snap = snap_dir / f"{today}_{host_file}_{digest}.html"
                snap.write_text(page, encoding="utf-8")
                main_text = extract_main_text(page)
                if main_text:
                    snap.with_suffix(".extract.md").write_text(main_text, encoding="utf-8")
                    extracted += 1
            for c in extract_candidates(page, url, keywords):
                if c["url"] in seen_urls:
                    continue
                seen_urls.add(c["url"])
                candidates.append(c)

    for w in warnings:
        print(f"[sync_comp][warn] {w}", file=sys.stderr)
    tail = f"正文 sidecar {extracted} 页（trafilatura）" if extracted else \
        "正文 sidecar 0（trafilatura 缺席，正则链路不受影响）"
    print(f"[sync_comp] 信源抓取完成 | 候选 {len(candidates)} | 快照目录 kb/raw/snapshots/ | {tail}")

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
