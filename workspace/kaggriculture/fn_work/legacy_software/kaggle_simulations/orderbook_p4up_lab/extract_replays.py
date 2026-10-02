# -*- coding: utf-8 -*-
"""extract_replays —— parquet 回放分片 → compact records JSONL（duckdb 沙箱抽取）。

数据源：fn_docs/hybrid/references/ext/fingerprint-scan/raw/ashok205-shards/
replays_YYYY-MM-DD.parquet（episode_id + replay_json 全量回放，georgymarin
kaggriculture-episodes v79 撤回前下载件，fingerprint-scan 在册）。

纪律：duckdb 是第三方代码，**执行恒在 bwrap 沙箱内**（断网、根只读、仅 /tmp
可写）；本脚本只拼命令、解析导出 JSON、调用 adapters.replay_to_record 归一。
抽取的 compact records 只落战役内（samples/ 或调用方指定），全量 blob 不落盘。

用法（kaggle_simulations/ 目录下）：
  python3 -m orderbook_p4up_lab.extract_replays \
      --feats-band <feats-band.jsonl> --team "THIRD FARM CLUB" \
      [--src replays_2026-09-23.parquet] [--limit 24] \
      --shards-dir <ashok205-shards/> \
      --out orderbook_p4up_lab/samples/cohort_tfc_20260923.jsonl
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM = os.path.dirname(_HERE)
if __name__ == "__main__" and _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

from orderbook_p4up_lab import adapters as A  # noqa: E402

DUCKDB = os.environ.get("P4UP_DUCKDB", "/home/renyxin/.local/bin/duckdb")


def build_bwrap_cmd(sql: str, duckdb: str = DUCKDB) -> list:
    """bwrap 沙箱模板（bwrap-run skill：根只读 + /tmp 可写 + 断网）。"""
    return ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--bind", "/tmp", "/tmp", "--unshare-net",
            duckdb, "-c", sql]


def build_extract_sql(parquet_paths, episode_ids, out_path: str) -> str:
    plist = ", ".join("'" + p.replace("'", "''") + "'" for p in parquet_paths)
    ids = ", ".join(str(int(i)) for i in episode_ids)
    return (f"COPY (SELECT episode_id, replay_json FROM read_parquet([{plist}]) "
            f"WHERE episode_id IN ({ids})) TO '{out_path}' (FORMAT JSON)")


def collect_episode_ids(feats_band: str, team: str, src: str = None,
                        limit: int = None) -> list:
    ids = []
    with open(feats_band, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if src and row.get("src") != src:
                continue
            if any(p.get("team") == team for p in (row.get("players") or [])):
                ids.append(row["episode_id"])
    if limit:
        ids = ids[:limit]
    return ids


def extract(parquet_paths, episode_ids, out_path: str, team: str = None,
            duckdb: str = DUCKDB, chunk: int = 6) -> dict:
    """沙箱导出 → 归一 → compact JSONL。返回统计。按 chunk 分批（单回放 ~30MB）。"""
    n_ok = n_skip = n_exported = 0
    ids = list(episode_ids)
    with open(out_path, "w", encoding="utf-8") as out:
        for start in range(0, len(ids), chunk):
            batch = ids[start:start + chunk]
            fd, tmp = tempfile.mkstemp(prefix="p4up_extract_", suffix=".json",
                                       dir="/tmp")
            os.close(fd)
            try:
                sql = build_extract_sql(parquet_paths, batch, tmp)
                cmd = build_bwrap_cmd(sql, duckdb)
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=560)
                if proc.returncode != 0:
                    raise RuntimeError(f"duckdb extract failed rc={proc.returncode}: "
                                       f"{proc.stderr[-800:]}")
                with open(tmp, encoding="utf-8") as fh:
                    # duckdb COPY (FORMAT JSON) = 每行一个 JSON 对象（JSONL）
                    exported = [json.loads(ln) for ln in fh if ln.strip()]
                n_exported += len(exported)
                for row in exported:
                    blob = row["replay_json"]
                    if isinstance(blob, str):
                        blob = json.loads(blob)
                    names = list((blob.get("info") or {}).get("TeamNames") or [])
                    seat = 0
                    if team and len(names) >= 2:
                        if names[1] == team:
                            seat = 1
                        elif names[0] != team:
                            n_skip += 1
                            continue
                    rec = A.replay_to_record(blob, episode=row["episode_id"],
                                             seat=seat)
                    out.write(json.dumps(rec.to_compact(), ensure_ascii=False)
                              + "\n")
                    n_ok += 1
            finally:
                try:
                    os.remove(tmp)
                except OSError:
                    pass
    return {"n_exported": n_exported, "n_written": n_ok,
            "n_skipped_team_mismatch": n_skip, "out": out_path}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="parquet 回放 → compact records（duckdb 走 bwrap）")
    ap.add_argument("--shards-dir", required=True)
    ap.add_argument("--feats-band", required=True)
    ap.add_argument("--team", required=True)
    ap.add_argument("--src", help="限定分片名（如 replays_2026-09-23.parquet）")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duckdb", default=DUCKDB)
    args = ap.parse_args(argv)

    shards = sorted(glob.glob(os.path.join(args.shards_dir, "*.parquet")))
    if args.src:
        shards = [p for p in shards if os.path.basename(p) == args.src]
    if not shards:
        print("no parquet shards matched", file=sys.stderr)
        return 2
    ids = collect_episode_ids(args.feats_band, args.team, args.src, args.limit)
    if not ids:
        print("no episode ids matched", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    stats = extract(shards, ids, args.out, team=args.team, duckdb=args.duckdb)
    stats["n_requested_ids"] = len(ids)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
