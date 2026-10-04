# -*- coding: utf-8 -*-
"""Track-C (BC) M0-1: 顶部选手官方回放抓取器.

从公榜快照 CSV 取 top-N 队（TeamId），经 kaggle CLI 三步取证：
  1) ``competitions team-submissions <team_id>``  -> 该队最新 submission ref；
  2) ``competitions episodes <ref>``              -> 该 ref 的 PUBLIC 局清单；
  3) ``competitions replay <eid>``                -> 回放 JSON 落 bc-top/ 目录。

产出：
  - references/data/online-replays/bc-top/episode-<eid>-replay.json
  - references/data/online-replays/bc-top/bc_harvest_manifest.json（引用纪律：
    来源命令 + 抓取时间 + 逐局 team/ref/时间；幂等：已存在文件跳过）。

用法：
  python bc_track/scripts/harvest_top_replays.py --top 30 --per-team 3 --max-games 72

只读 Kaggle（list/replay 下载），绝不提交。stdlib-only。
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[2]
CAMPAIGN = SOFTWARE.parent
DEFAULT_LB_CSV = (CAMPAIGN / "references" / "data" / "lb-snapshot-20260920"
                  / "kaggriculture-publicleaderboard-2026-09-20T02_21_40.csv")
DEST_DIR = (CAMPAIGN / "references" / "data" / "online-replays" / "bc-top")
MANIFEST = DEST_DIR / "bc_harvest_manifest.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _run_kaggle(args: list[str]) -> str:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        ["kaggle", *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"kaggle {' '.join(args)} failed ({proc.returncode}): "
            f"{(proc.stderr or proc.stdout).strip()[:400]}")
    return proc.stdout


def _parse_json_payload(text: str):
    start = text.find("[")
    if start < 0:
        start = text.find("{")
    if start < 0:
        raise RuntimeError(f"no JSON payload: {text[:200]!r}")
    value, _ = json.JSONDecoder().raw_decode(text[start:])
    return value


def load_top_teams(csv_path: Path, top: int) -> list[dict]:
    """公榜 CSV -> [{rank, team_id, team_name, score}]（升序 rank）。"""
    rows: list[dict] = []
    with open(csv_path, "r", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            try:
                rank = int(row["Rank"])
            except (KeyError, ValueError):
                continue
            if rank < 1:
                continue
            rows.append({"rank": rank, "team_id": row["TeamId"],
                         "team_name": row["TeamName"],
                         "score": row["Score"]})
            if len(rows) >= top:
                break
    return rows


def newest_submission(team_id: str) -> dict | None:
    raw = _run_kaggle(["competitions", "team-submissions", team_id,
                       "--format", "json"])
    subs = _parse_json_payload(raw)
    if not isinstance(subs, list) or not subs:
        return None
    subs.sort(key=lambda s: str(s.get("dateSubmitted", "")), reverse=True)
    return subs[0]


def latest_public_episodes(ref: int, n: int) -> list[dict]:
    raw = _run_kaggle(["competitions", "episodes", str(ref),
                       "--format", "json"])
    eps = _parse_json_payload(raw)
    public = [e for e in eps
              if "PUBLIC" in str(e.get("type", ""))
              and "COMPLETED" in str(e.get("state", ""))]
    public.sort(key=lambda e: str(e.get("createTime", "")), reverse=True)
    return public[:n]


def fetch_replay(dest: Path, eid) -> str:
    target = dest / f"episode-{eid}-replay.json"
    if target.exists() and target.stat().st_size > 100_000:
        return "skip"
    _run_kaggle(["competitions", "replay", str(eid), "-p", str(dest), "-q"])
    if not target.exists():
        # CLI 可能以不同文件名落盘——容错扫描
        cands = [p for p in dest.glob(f"*{eid}*.json")]
        if cands:
            cands[0].rename(target)
        else:
            return "missing"
    return "fetched"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", default=str(DEFAULT_LB_CSV))
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--per-team", type=int, default=3)
    ap.add_argument("--max-games", type=int, default=72)
    ap.add_argument("--sleep", type=float, default=1.0,
                    help="相邻 kaggle 调用间隔（秒），礼貌限速")
    args = ap.parse_args(argv)

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    done_eids: set[int] = set(manifest.get("episodes", {}))

    teams = load_top_teams(Path(args.csv), args.top)
    print(f"[harvest] top-{len(teams)} teams from {args.csv}")
    manifest.setdefault("source", {
        "channel": "kaggle-cli",
        "competition": "kaggriculture",
        "commands": [
            "kaggle competitions team-submissions <team_id> --format json",
            "kaggle competitions episodes <ref> --format json",
            "kaggle competitions replay <eid>",
        ],
        "lb_csv": str(DEFAULT_LB_CSV),
    })
    manifest.setdefault("captured_at_utc", _utc_now())
    manifest.setdefault("episodes", {})
    fetched = skipped = 0
    for team in teams:
        if fetched >= args.max_games:
            break
        label = f"#{team['rank']} {team['team_name']} ({team['team_id']})"
        try:
            sub = newest_submission(team["team_id"])
            time.sleep(args.sleep)
            if sub is None:
                print(f"[harvest] {label}: no submissions, skip")
                continue
            ref = int(sub["id"])
            eps = latest_public_episodes(ref, args.per_team)
            time.sleep(args.sleep)
        except Exception as exc:                       # noqa: BLE001
            print(f"[harvest] {label}: LIST FAIL {exc}")
            continue
        for ep in eps:
            eid = int(ep["id"])
            if eid in done_eids:
                skipped += 1
                continue
            if fetched >= args.max_games:
                break
            try:
                status = fetch_replay(DEST_DIR, eid)
            except Exception as exc:                   # noqa: BLE001
                status = f"failed: {str(exc)[:160]}"
            manifest["episodes"][str(eid)] = {
                "team": team["team_name"], "rank": team["rank"],
                "submission_ref": ref, "createTime": ep.get("createTime"),
                "fetch": status, "fetched_at": _utc_now(),
            }
            if status == "fetched":
                fetched += 1
                done_eids.add(eid)
            print(f"[harvest] {label}: ep {eid} -> {status}")
            time.sleep(args.sleep)
        MANIFEST.write_text(
            json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
    manifest["summary"] = {
        "teams_requested": len(teams),
        "games_target": args.max_games,
        "fetched_this_run": fetched,
        "skipped_existing": skipped,
        "total_unique_episodes": len(manifest["episodes"]),
        "finished_at": _utc_now(),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False)
                        + "\n", encoding="utf-8")
    print(f"[harvest] done: fetched={fetched} skipped={skipped} "
          f"total={len(manifest['episodes'])} -> {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
