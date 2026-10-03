"""事件/度量记录 JSON 行落盘（进程内保序）（shared 块）。"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_FILES = {"event": "events.jsonl", "metric": "metrics.jsonl"}
_seq: dict[str, int] = {}


def append_record(run_dir, kind: str, payload: dict) -> None:
    """kind ∈ {event, metric}；逐行追加 JSON（ts/seq 盖章）；磁盘失败抛 IOError。"""
    if kind not in _FILES:
        raise ValueError(f"记录类型非法: {kind}（须为 event|metric）")
    if not isinstance(payload, dict):
        raise ValueError("payload 必须为 dict")
    path = Path(run_dir) / _FILES[kind]
    key = f"{Path(run_dir).resolve()}::{kind}"
    _seq[key] = _seq.get(key, 0) + 1
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "seq": _seq[key], **payload}
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise IOError(f"记录落盘失败: {path}") from exc
