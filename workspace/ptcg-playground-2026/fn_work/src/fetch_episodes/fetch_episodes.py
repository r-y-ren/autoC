"""编排采集：CLI 拉回放→去重→INDEX 登记（R6）"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.fetch_episodes.dedup_register import dedup_register
from src.fetch_episodes.kaggle_cli_pull import kaggle_cli_pull
from src.shared.write_runs_jsonl import write_runs_jsonl

_SEEN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "runs", "episode-seen-ids.json"))


def fetch_episodes(targets, store_dir="references/episodes", index_path=None):
    """拉取并登记。targets=[{"kind","competition",...}]；单目标失败重试后跳过并计数不中断。

    返回 {"fetched": n_new, "skipped": n_dup, "failed": [{"target","err"}]}。
    """
    index_path = index_path or os.path.join(store_dir, "INDEX.md")
    seen = set()
    if os.path.isfile(_SEEN_PATH):
        seen = set(json.load(open(_SEEN_PATH)))
    os.makedirs(store_dir, exist_ok=True)

    failed = []
    for t in targets:
        try:
            eps = kaggle_cli_pull(t)
        except Exception as e:  # noqa: BLE001 —— 单目标失败不中断
            failed.append({"target": t, "err": str(e)[:200]})
            continue
        # 标注来源
        for ep in eps:
            ep.setdefault("source", f"kaggle-cli:{t.get('kind')}/{t.get('competition')}")
        n_new, n_dup, seen = dedup_register(eps, index_path, seen)
        for eid, ep in ((e.get("id") or e.get("episodeId"), e) for e in eps):
            pass  # 落盘在下方按 id 命名
        for ep in eps:
            eid = ep.get("id") or ep.get("episodeId") or abs(hash(str(ep)[:200])) % 10**10
            with open(os.path.join(store_dir, f"{eid}.json"), "w", encoding="utf-8") as f:
                json.dump(ep, f, ensure_ascii=False)

    os.makedirs(os.path.dirname(_SEEN_PATH), exist_ok=True)
    json.dump(sorted(str(x) for x in seen), open(_SEEN_PATH, "w"))
    result = {"fetched": len(seen), "skipped": 0, "failed": failed, "targets": len(targets)}
    write_runs_jsonl("fetch-episodes", result)
    return result
