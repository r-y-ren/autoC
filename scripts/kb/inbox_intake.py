#!/usr/bin/env python3
"""S-16 kb/inbox/ 外来资料消费器（升级票03，2026-09-16）。

模式：
  无参        扫描 kb/inbox/（README.md 与 *.meta.yaml 除外），分类路由，产出候选队列/线索并打印报告
  --dry-run   只报告，不动任何文件
分类路由（三分，并入既有候选队列流水线——分片/lint/索引全复用）：
  sidecar <文件名>.meta.yaml 的 kind 显式声明优先，否则按文件名关键词辅助。
  晋级为候选（可被分片消费建卡/建条目）的前提 = sidecar 携带 source_url（已溯源）：
    comp → kb/raw/candidates/inbox-comp-<stamp>.yaml（{title,url,found_on}，sync_competitions 队列口径）
    tech → kb/raw/candidates/inbox-tech-<stamp>.yaml（富字典，sync_tech 队列口径）
  其余（无 sidecar / 无 source_url / 不可归类）→ kb/raw/leads/ 线索区 + 报告点名催补
  （铁律 1：未溯源永不晋级可引用条目，"宁缺毋滥"只约束分析不约束暂存）。
配额：budget.yaml → quotas.inbox_files_per_run（默认 20），按 mtime 旧先消费，超出留存下轮（不删不拒）。
消费后的原件（含 sidecar）移 kb/raw/inbox-processed/<stamp>/ 留审计（kb/raw/ 均不入库）。
活跃战役提示：文件名/sidecar 命中活跃战役 id 时仅报告提示，不改动任何战役文件（慢快循环解耦）。
测试根覆盖：ZCODE_PROJECT_DIR 环境变量（scripts/kb/test_inbox.py 用）。
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path

COMP_KW = re.compile(r"章程|通知|规则|大赛|挑战赛|竞赛|比赛|杯赛|报名|hackathon|competition|contest|rules", re.I)
TECH_KW = re.compile(r"arxiv|论文|paper|预印本|综述|survey|技术", re.I)
DEFAULT_QUOTA = 20


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def load_yaml(path: Path):
    if not path.is_file():
        return None
    try:
        import yaml
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:  # noqa: BLE001
        print(f"[inbox_intake] ⚠ sidecar 不可读 {path.name}: {e}")
        return None


def quota(root: Path) -> int:
    try:
        import yaml
        cfg = yaml.safe_load((root / "config" / "budget.yaml").read_text(encoding="utf-8")) or {}
        return int((cfg.get("quotas") or {}).get("inbox_files_per_run", DEFAULT_QUOTA))
    except Exception:  # noqa: BLE001
        return DEFAULT_QUOTA


def classify(name: str, meta) -> str:
    """→ 路由 comp/tech/lead。晋级候选的前提 = sidecar 带 source_url（铁律 1）。"""
    meta = meta or {}
    kind = str(meta.get("kind", "")).lower()
    if kind in ("comp", "tech", "lead"):
        base = kind
    elif COMP_KW.search(name):
        base = "comp"
    elif TECH_KW.search(name):
        base = "tech"
    else:
        base = "lead"
    url = str(meta.get("source_url") or "").strip()
    if base in ("comp", "tech") and not url:
        return "lead"  # 未溯源降级线索
    return base


def active_cids(root: Path) -> list[str]:
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "guard"))
        import flow_state as fs  # noqa: PLC0415
        st = fs.load_state(root)
        if st is not None and fs.is_v2(st):
            return sorted(fs.campaigns(st).keys())
    except Exception:  # noqa: BLE001
        pass
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description="kb/inbox/ 外来资料消费器")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不动文件")
    args = ap.parse_args()

    root = project_root()
    inbox = root / "kb" / "inbox"
    if not inbox.is_dir():
        print("[inbox_intake] kb/inbox/ 不存在，跳过（约定见 kb/inbox/README.md）")
        return 0

    cids = active_cids(root)
    files = [p for p in sorted(inbox.iterdir(), key=lambda p: p.stat().st_mtime)
             if p.is_file() and p.name != "README.md" and not p.name.endswith(".meta.yaml")]
    if not files:
        print("[inbox_intake] 投递箱为空")
        return 0

    limit = quota(root)
    take, leftover = files[:limit], files[limit:]
    stamp = time.strftime("%Y%m%d-%H%M%S")
    comp_items, tech_items, leads, urges, hints = [], [], [], [], []
    processed_dir = root / "kb" / "raw" / "inbox-processed" / stamp
    leads_dir = root / "kb" / "raw" / "leads"

    for i, f in enumerate(take):
        meta = load_yaml(inbox / (f.name + ".meta.yaml"))
        route = classify(f.name, meta)
        m = meta or {}
        dropped = str(m.get("dropped_at") or stamp)
        blob = f.name + " " + str(m)
        for cid in cids:
            if cid.lower() in blob.lower():
                hints.append((f.name, cid))
        if route == "comp":
            comp_items.append({
                "title": str(m.get("title") or f.stem),
                "url": str(m.get("source_url")),
                "found_on": f"kb/inbox/{f.name}（人工投递 {dropped}）",
            })
            print(f"[inbox_intake] {f.name} → 赛事候选（已溯源）")
        elif route == "tech":
            cid_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", f.stem).strip("-").lower() or f"{stamp}-{i}"
            tech_items.append({
                "id": f"inbox-{cid_slug}",
                "kind": "inbox",
                "name": str(m.get("title") or f.stem),
                "urls": [str(m.get("source_url"))],
                "summary": str(m.get("note") or f"人工投递（kb/inbox/{f.name}，{dropped}）"),
                "suggested_fields": [],
                "directions": [str(m["intended"])] if m.get("intended") else [],
                "signal": {"venue": "inbox", "citations_90d": None, "stars": None, "runnable": False},
            })
            print(f"[inbox_intake] {f.name} → 技术卡候选（已溯源）")
        else:
            leads.append(f.name)
            if meta is None:
                urges.append(f.name)
            why = "缺 sidecar" if meta is None else "未溯源"
            print(f"[inbox_intake] {f.name} → raw/leads 线索（{why}，不晋级可引用条目）")
        if args.dry_run:
            continue
        dest_dir = leads_dir if route == "lead" else processed_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), str(dest_dir / f.name))
        sidecar = inbox / (f.name + ".meta.yaml")
        if sidecar.is_file():
            shutil.move(str(sidecar), str(dest_dir / sidecar.name))

    if not args.dry_run:
        import yaml
        cand = root / "kb" / "raw" / "candidates"
        cand.mkdir(parents=True, exist_ok=True)
        if comp_items:
            (cand / f"inbox-comp-{stamp}.yaml").write_text(
                yaml.safe_dump(comp_items, allow_unicode=True, sort_keys=False), encoding="utf-8")
        if tech_items:
            (cand / f"inbox-tech-{stamp}.yaml").write_text(
                yaml.safe_dump(tech_items, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print(f"[inbox_intake] 本轮：赛事候选 {len(comp_items)}｜技术候选 {len(tech_items)}｜"
          f"线索 {len(leads)}｜留存（超配额） {len(leftover)}")
    if urges:
        print(f"[inbox_intake] ⚠ 待补源（补 sidecar 后把文件放回 inbox 重投即可晋级；"
              f"leads 中的原件不会被自动重扫）：{', '.join(urges)}")
    for name, cid in hints:
        print(f"[inbox_intake] ⚠ {name} 与活跃战役 {cid} 相关——仅在战役会话人工裁决是否引用，本跑批未改动战役文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
