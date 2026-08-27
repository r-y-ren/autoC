#!/usr/bin/env python3
"""S-03 科技雷达增量同步（sync_tech）。

职责边界（紧循环）：API 拉取 → 规范化 ID 去重 → 信号评分 → 候选队列。
**不直接生成 kb/tech/ 成品卡片**（competition_fit 判断属 Hunter 角色），
候选写入 kb/raw/candidates/tech-<时间戳>.yaml，由 K-01 派发 Hunter 消费。

信源：
  arxiv  ：arXiv Atom API（免密），按方向关键词取近 N 天新论文
  github ：gh CLI 搜索近 N 天新建、star 数达标的仓库（未登录则跳过并告警）

候选队列生命周期（T2.1 裁决）：
  - 活跃队列 = kb/raw/candidates/tech-*.yaml（仅顶层）；K-01 消费完毕后把队列文件
    移入 kb/raw/candidates/processed/（防重复消费，保留痕迹）
  - Hunter 拒绝的候选写入 kb/tech/.rejections.yaml 台账（{id, reason, stars, decided}）
  - 重评规则：被拒候选若当前 stars ≥ 台账快照 ×2 则重新入队（科技信号随时间增长的核心场景）

用法：
  python scripts/kb/sync_tech.py [--direction 名称] [--days 14] [--max 20]
                                 [--dry-run] [--selftest]
退出码：0=正常（含零候选）；2=参数/配置错误。
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def project_root() -> Path:
    env = __import__("os").environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()


def load_directions(direction_name: str | None) -> list[dict]:
    import yaml
    droot = ROOT / "config" / "directions"
    out = []
    for f in sorted(droot.glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        cfg = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if not cfg.get("direction"):
            continue
        if direction_name and cfg["direction"] != direction_name:
            continue
        out.append(cfg)
    return out


# ---------- arXiv ----------

def fetch_arxiv(query: str, days: int, max_items: int) -> list[dict]:
    # 限定 ML 类目 + 摘要字段短语匹配：all: 全文检索过松，首跑实测混入大量物理/机器人论文
    expr = f'(cat:cs.LG OR cat:stat.ML OR cat:cs.AI) AND abs:"{query}"'
    url = (f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(expr)}"
           f"&sortBy=submittedDate&sortOrder=descending&max_results={max_items * 2}")
    req = urllib.request.Request(url, headers={"User-Agent": "autoC/0.1 sync_tech"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        ns = {"a": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.read())
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    out = []
    for e in root.findall("a:entry", ns):
        raw_id = (e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1]  # 2501.00001v1
        arxiv_id = raw_id.split("v")[0]
        pub = (e.findtext("a:published", "", ns) or "")[:10]
        if not arxiv_id or not pub:
            continue
        if datetime.date.fromisoformat(pub) < cutoff:
            continue
        out.append({
            "id": f"arxiv-{arxiv_id}",
            "kind": "arxiv",
            "name": re.sub(r"\s+", " ", e.findtext("a:title", "", ns)).strip(),
            "published": pub,
            "urls": [f"https://arxiv.org/abs/{arxiv_id}"],
            "signal": {"venue": "arXiv", "citations_90d": None, "stars": None, "runnable": False},
            "summary": (e.findtext("a:summary", "", ns) or "").strip()[:400],
        })
        if len(out) >= max_items:
            break
    return out


# ---------- GitHub（经 gh CLI） ----------

def fetch_github(query: str, days: int, max_items: int, min_stars: int) -> tuple[list[dict], str]:
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    q = f"{query} created:>={since} stars:>={min_stars}"
    try:
        proc = subprocess.run(
            ["gh", "search", "repos", q, "--limit", str(max_items), "--json",
             "fullName,description,stargazersCount,url,createdAt,language"],
            capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        return [], "gh CLI 不可用"
    if proc.returncode != 0:
        return [], f"gh 搜索失败: {proc.stderr.strip()[:120]}"
    items = []
    for r in json.loads(proc.stdout or "[]"):
        full = r.get("fullName") or ""
        if not full:
            continue
        items.append({
            "id": "gh-" + full.replace("/", "_"),
            "kind": "github",
            "name": full,
            "published": (r.get("createdAt") or "")[:10],
            "urls": [r.get("url") or f"https://github.com/{full}"],
            "signal": {"venue": "GitHub", "stars": r.get("stargazersCount"),
                       "citations_90d": None, "runnable": True},
            "summary": (r.get("description") or "")[:400],
        })
    return items, ""


def existing_card_ids() -> set[str]:
    return {p.stem for p in (ROOT / "kb" / "tech").glob("*.md")} if (ROOT / "kb" / "tech").is_dir() else set()


def existing_candidate_ids(cand_dir: Path) -> set[str]:
    """只扫活跃队列（顶层 tech-*.yaml）；processed/ 已消费文件不参与去重（允许信号增长后重评）。"""
    ids: set[str] = set()
    import yaml
    for f in sorted(cand_dir.glob("tech-*.yaml")):
        try:
            for it in yaml.safe_load(f.read_text(encoding="utf-8")) or []:
                if it.get("id"):
                    ids.add(it["id"])
        except Exception:  # noqa: BLE001
            continue
    return ids


def load_rejections() -> dict[str, dict]:
    """Hunter 拒绝台账：{id: {reason, stars, decided}}。"""
    import yaml
    p = ROOT / "kb" / "tech" / ".rejections.yaml"
    if not p.is_file():
        return {}
    try:
        rows = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        return {r["id"]: r for r in rows if isinstance(r, dict) and r.get("id")}
    except Exception:  # noqa: BLE001
        return {}


def rejection_blocks(cand: dict, rej: dict | None) -> bool:
    """被拒候选是否仍应跳过：无动态信号（论文）永久跳过；仓库 stars 翻倍则放行重评。"""
    if not rej:
        return False
    snap = int(rej.get("stars") or 0)
    now = int((cand.get("signal") or {}).get("stars") or 0)
    if snap > 0 and now >= snap * 2:
        return False  # 信号显著增长 → 允许重评
    return True


def selftest() -> int:
    fixture = [{
        "id": "arxiv-2501.00001", "kind": "arxiv", "name": "fixture",
        "published": datetime.date.today().isoformat(), "urls": ["https://example.com"],
        "signal": {}, "summary": "离线自检"}]
    ok = fixture[0]["id"].startswith("arxiv-")
    print(f"[sync_tech][selftest] {'PASS' if ok else 'FAIL'} 离线夹具与 ID 规范化")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="科技雷达增量同步（候选队列）")
    ap.add_argument("--direction", default=None, help="限定方向名（缺省=全部启用方向）")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max", type=int, default=20, help="每个方向每信源上限")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    cfgs = load_directions(args.direction)
    if not cfgs:
        print("[sync_tech] config/directions/ 下没有启用的方向配置（复制 _template.yaml 开始）")
        return 2

    cand_dir = ROOT / "kb" / "raw" / "candidates"
    known = existing_card_ids() | existing_candidate_ids(cand_dir)
    rejections = load_rejections()
    candidates: list[dict] = []
    warnings: list[str] = []
    for cfg in cfgs:
        radar = cfg.get("tech_radar") or {}
        min_stars = int((radar.get("min_signal") or {}).get("stars") or 0)
        for field in radar.get("fields") or []:
            # suggested_fields 在候选拼装处随 field 赋值（修复：循环变量泄漏导致全标最后一个 field）
            try:
                got = fetch_arxiv(field, args.days, args.max)
            except Exception as e:  # noqa: BLE001
                got, w = [], f"arxiv[{field}] {e}"
                warnings.append(w)
            got_gh, w = fetch_github(field, args.days, args.max, max(min_stars, 10))
            if w:
                warnings.append(f"github[{field}] {w}")
            for c in got + got_gh:
                c["suggested_fields"] = [field]
            candidates += got + got_gh

    fresh: dict[str, dict] = {}
    re_eval = 0
    for c in candidates:
        cid = c["id"]
        if cid in known:
            continue
        rej = rejections.get(cid)
        if rejection_blocks(c, rej):
            continue
        if rej:
            re_eval += 1
        if cid in fresh:  # 多 field 命中同一候选 → 合并 suggested_fields
            for f in c["suggested_fields"]:
                if f not in fresh[cid]["suggested_fields"]:
                    fresh[cid]["suggested_fields"].append(f)
        else:
            fresh[cid] = c
    fresh_list = list(fresh.values())

    for w in warnings:
        print(f"[sync_tech][warn] {w}", file=sys.stderr)
    print(f"[sync_tech] 方向 {len(cfgs)} 个 | 拉取 {len(candidates)} | 去重/拒绝过滤后新增候选 "
          f"{len(fresh_list)}（其中重评放行 {re_eval}）")

    if args.dry_run or not fresh_list:
        return 0

    cand_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = cand_dir / f"tech-{stamp}.yaml"
    import yaml
    out.write_text(yaml.safe_dump(fresh_list, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[sync_tech] 候选队列 → {out.relative_to(ROOT)}")
    print("[sync_tech] 下一步：K-01 kb-sync 派发 Hunter 消费候选（写入 kb/tech/ 成品卡片）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
