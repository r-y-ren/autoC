#!/usr/bin/env python
"""Fetch official Kaggriculture episodes and close the online sampling gate.

Launch ledgers stay as submit-time PENDING snapshots. This script writes a
separate COMPLETE sampling record from Kaggle CLI episode lists + replay JSON.

Local quickwin / vendored self-play is refused as a sampling source.

Usage (repo root):
  python workspace/kaggriculture/software/scripts/sync_online_probe.py list --round 21
  python workspace/kaggriculture/software/scripts/sync_online_probe.py fetch --round 21
  python workspace/kaggriculture/software/scripts/sync_online_probe.py ingest --round 21
  python workspace/kaggriculture/software/scripts/sync_online_probe.py gate
  python workspace/kaggriculture/software/scripts/sync_online_probe.py close --round 21
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from kgenv.online_probe import (  # noqa: E402
    DEFAULT_TEAM,
    OnlineProbeError,
    build_sampling_payload,
    campaign_root_from_software,
    classify_replay,
    launch_ledger_dir,
    list_launch_rounds,
    load_json,
    next_round_gate,
    replay_dir,
    sampling_dir,
    submission_ref_of,
)


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_kaggle(args: list[str]) -> str:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        ["kaggle", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        raise OnlineProbeError(
            f"kaggle {' '.join(args)} failed ({proc.returncode}): "
            f"{(proc.stderr or proc.stdout).strip()[:800]}"
        )
    return proc.stdout


def _parse_json_payload(text: str) -> Any:
    start = text.find("[")
    if start < 0:
        start = text.find("{")
    if start < 0:
        raise OnlineProbeError(f"no JSON payload in kaggle output: {text[:240]!r}")
    return json.loads(text[start:])


def _launch(root: Path, round_no: int) -> tuple[Path, dict[str, Any]]:
    path = launch_ledger_dir(root) / f"round{round_no}_ledger.json"
    if not path.exists():
        raise OnlineProbeError(f"missing launch ledger {path}")
    return path, load_json(path)


def cmd_list(args: argparse.Namespace) -> int:
    _, ledger = _launch(SOFTWARE, args.round)
    ref = submission_ref_of(ledger)
    if ref is None:
        raise OnlineProbeError(f"round {args.round} has no submission_ref")
    raw = _run_kaggle(["competitions", "episodes", str(ref), "--format", "json"])
    episodes = _parse_json_payload(raw)
    dest = sampling_dir(SOFTWARE)
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"round{args.round}_episodes.json"
    out.write_text(json.dumps(episodes, indent=1), encoding="utf-8")
    public = [e for e in episodes if "PUBLIC" in str(e.get("type", ""))]
    validation = [e for e in episodes if "VALIDATION" in str(e.get("type", ""))]
    print(json.dumps({
        "round": args.round,
        "submission_ref": ref,
        "episodes": len(episodes),
        "public": len(public),
        "validation": len(validation),
        "ids": [e.get("id") for e in episodes],
        "wrote": str(out),
    }, indent=1))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    campaign = campaign_root_from_software(SOFTWARE)
    dest = replay_dir(campaign, args.round)
    dest.mkdir(parents=True, exist_ok=True)
    episode_list = sampling_dir(SOFTWARE) / f"round{args.round}_episodes.json"
    if not episode_list.exists():
        cmd_list(args)
    episodes = json.loads(episode_list.read_text(encoding="utf-8"))
    fetched = []
    skipped = []
    failed = []
    for rec in episodes:
        eid = rec.get("id")
        if eid is None:
            continue
        target = dest / f"episode-{eid}-replay.json"
        if target.exists() and not args.overwrite:
            skipped.append(eid)
            continue
        try:
            _run_kaggle(["competitions", "replay", str(eid), "-p", str(dest), "-q"])
            fetched.append(eid)
        except OnlineProbeError as exc:
            failed.append({"id": eid, "error": str(exc)})
    print(json.dumps({
        "round": args.round,
        "dest": str(dest),
        "fetched": fetched,
        "skipped_existing": skipped,
        "failed": failed,
    }, indent=1))
    return 1 if failed else 0


def _submission_public_score(ref: int) -> float | None:
    raw = _run_kaggle(["competitions", "submissions", "kaggriculture", "--format", "json"])
    rows = _parse_json_payload(raw)
    for row in rows:
        if int(row.get("ref") or 0) == int(ref):
            score = row.get("publicScore")
            try:
                return float(score)
            except (TypeError, ValueError):
                return None
    return None


def _ingest_from_dir(round_no: int, public_score: float | None,
                     captured_at_utc: str) -> dict[str, Any]:
    launch_path, ledger = _launch(SOFTWARE, round_no)
    ref = submission_ref_of(ledger)
    if ref is None:
        raise OnlineProbeError(f"round {round_no} has no submission_ref")
    campaign = campaign_root_from_software(SOFTWARE)
    dest = replay_dir(campaign, round_no)
    files = sorted(dest.glob("episode-*-replay.json"))
    if not files:
        raise OnlineProbeError(f"no official replays in {dest}")
    games = []
    for path in files:
        replay = json.loads(path.read_text(encoding="utf-8"))
        games.append(classify_replay(replay, our_team=DEFAULT_TEAM))
    rel_replay = dest.relative_to(campaign).as_posix()
    payload = build_sampling_payload(
        round_no=round_no,
        submission_ref=ref,
        launch_ledger=ledger,
        games=games,
        public_score=public_score,
        source={
            "channel": "kaggle-cli",
            "competition": "kaggriculture",
            "commands": [
                f"kaggle competitions episodes {ref}",
                "kaggle competitions replay <episode_id>",
            ],
            "replay_dir": rel_replay,
            "launch_ledger": launch_path.relative_to(SOFTWARE).as_posix(),
        },
        captured_at_utc=captured_at_utc,
    )
    out_dir = sampling_dir(SOFTWARE)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"round{round_no}_sampling.json"
    out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    summary = {
        "round": round_no,
        "submission_ref": ref,
        "status": payload["status"],
        "public_score": payload.get("public_score"),
        "record": payload["public_sampling"]["record"],
        "public_games": payload["public_sampling"]["public_games"],
        "wrote": str(out),
        "replay_dir": rel_replay,
    }
    print(json.dumps(summary, indent=1))
    return payload


def cmd_ingest(args: argparse.Namespace) -> int:
    score = args.public_score
    if score is None and not args.skip_score:
        _, ledger = _launch(SOFTWARE, args.round)
        ref = submission_ref_of(ledger)
        try:
            score = _submission_public_score(int(ref))
        except OnlineProbeError as exc:
            print(f"[warn] publicScore lookup failed: {exc}", file=sys.stderr)
    _ingest_from_dir(args.round, score, args.captured_at or _utc_now())
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    report = next_round_gate(SOFTWARE, min_public=args.min_public)
    print(json.dumps(report, indent=1))
    return 0 if report["pass"] else 1


def cmd_close(args: argparse.Namespace) -> int:
    rc = cmd_list(args)
    if rc != 0:
        return rc
    rc = cmd_fetch(args)
    if rc != 0:
        return rc
    rc = cmd_ingest(args)
    if rc != 0:
        return rc
    return cmd_gate(args)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--round", type=int, required=True)
    p_list = sub.add_parser("list", parents=[common])
    p_list.set_defaults(func=cmd_list)
    p_fetch = sub.add_parser("fetch", parents=[common])
    p_fetch.add_argument("--overwrite", action="store_true")
    p_fetch.set_defaults(func=cmd_fetch)
    p_ingest = sub.add_parser("ingest", parents=[common])
    p_ingest.add_argument("--public-score", type=float)
    p_ingest.add_argument("--skip-score", action="store_true")
    p_ingest.add_argument("--captured-at")
    p_ingest.set_defaults(func=cmd_ingest)
    p_gate = sub.add_parser("gate")
    p_gate.add_argument("--min-public", type=int, default=3)
    p_gate.set_defaults(func=cmd_gate)
    p_close = sub.add_parser("close", parents=[common])
    p_close.add_argument("--overwrite", action="store_true")
    p_close.add_argument("--public-score", type=float)
    p_close.add_argument("--skip-score", action="store_true")
    p_close.add_argument("--captured-at")
    p_close.add_argument("--min-public", type=int, default=3)
    p_close.set_defaults(func=cmd_close)
    args = ap.parse_args()
    try:
        return args.func(args)
    except OnlineProbeError as exc:
        print(f"[online-probe] FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
