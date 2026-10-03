"""metrics 分片→汇总引用表（含一致性校验，不写顶层 metrics.json）（build_materials 块）。"""
from __future__ import annotations

import json
from pathlib import Path


class MaterialError(Exception):
    """冲突/缺失键。"""


def export_metrics_table(run_dirs: list) -> dict:
    """读各 run_dir/metrics.jsonl → {key: [{value, run, ts}]}+一致性校验+双格式表。"""
    table: dict[str, list] = {}
    for rd in run_dirs:
        fp = Path(rd) / "metrics.jsonl"
        if not fp.exists():
            raise MaterialError(f"运行目录缺 metrics 分片: {rd}")
        for line in fp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = row.get("key")
            if not key:
                raise MaterialError(f"{rd} 存在无 key 的度量行")
            table.setdefault(key, []).append(
                {"value": row.get("value"), "run": str(rd), "ts": row.get("ts"),
                 "note": row.get("note", "")})
    conflicts = {k: v for k, v in table.items()
                 if len({x["value"] for x in v if v[0]["value"] is not None
                         and x["value"] is not None}) > 1 and k.endswith("/final")}
    return {"by_key": table, "conflicts_final": sorted(conflicts),
            "keys": sorted(table), "n_runs": len(run_dirs)}
