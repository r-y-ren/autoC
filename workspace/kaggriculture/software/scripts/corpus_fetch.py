"""Corpus fetch channel for m1-replay-corpus (read-only network operations).

Sub-commands
------------
probe    : HTTP-range-probe the first 16 KiB of every episode file listed in a
           daily-shard file listing, extracting TeamNames / rewards / statuses
           without downloading full ~30 MB replays. Emits episode->teams map.
select   : classify probed episodes against the current leaderboard CSV into
           bands (top20 / top100) and emit a download plan (episode ids).
fetch    : download the selected episode files (single-file dataset endpoint).
stage    : register staged raw files into .tmp-corpus/manifest.json with
           sha256, byte size, source URL, capture date, teams and bands.

Network is read-only. Budget guard: refuses plans above MAX_TOTAL_FETCH_BYTES
or touching more than MAX_SHARDS distinct daily shards.

Usage examples (run from repo root):
  python workspace/kaggriculture/software/scripts/corpus_fetch.py probe \
      --filelist .tmp-corpus/shard-2026-08-28-filelist.json \
      --slug kaggle/kaggriculture-episodes-2026-08-28 \
      --out .tmp-corpus/shard-2026-08-28-teams.json
  python workspace/kaggriculture/software/scripts/corpus_fetch.py select \
      --probes .tmp-corpus/shard-2026-08-28-teams.json[,more.json] \
      --leaderboard .tmp-online/kaggriculture.zip \
      --plan-out .tmp-corpus/download-plan.json --max-per-band-top20 14
  python workspace/kaggriculture/software/scripts/corpus_fetch.py fetch \
      --plan .tmp-corpus/download-plan.json --dest .tmp-corpus/raw
  python workspace/kaggriculture/software/scripts/corpus_fetch.py stage \
      --corpus .tmp-corpus --leaderboard .tmp-online/kaggressure.zip  # see --help
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve()
while REPO != REPO.parent and not (REPO / ".git").exists():
    REPO = REPO.parent
SOFTWARE = REPO / "workspace" / "kaggriculture" / "software"
CAPTURE_DATE = "2026-08-29"  # provenance date for this milestone's captures
BAND_TOP20 = "top20"
BAND_TOP100 = "top100"
BAND_500_900 = "band_500_900"
BAND_BASELINE = "baseline"
BASELINE_TEAM = "renyxin"  # our submission seat
EPISODE_URL = "https://www.kaggle.com/competitions/kaggriculture/episodes/{eid}"
SHARD_FILE_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/{slug}/{fname}"
)
SHARD_URL = "https://www.kaggle.com/datasets/{slug}"
MAX_TOTAL_FETCH_BYTES = 3_000_000_000  # ~3 GB raw corpus budget
MAX_SHARDS = 2  # at most two distinct daily shards may be pulled from
PROBE_BYTES = 16 * 1024
TEAM_NAMES_RE = re.compile(r'"TeamNames":\s*(\[[^\]]*\])')
REWARDS_RE = re.compile(r'"rewards":\s*(\[[^\]]*\])')


def _load_token() -> str:
    for cand in ("~/.kaggle/credentials.json", "~/.kaggle/kaggle.json"):
        p = Path(os.path.expanduser(cand))
        if not p.exists():
            continue
        creds = json.loads(p.read_text(encoding="utf-8"))
        tok = creds.get("access_token") or creds.get("key")
        if tok:
            return tok
    raise SystemExit("no kaggle credentials found for probe/fetch")


def _get_range(url: str, first: int, last: int, token: str, tries: int = 6):
    """GET a byte range with 429-aware backoff (Kaggle throttles ~50 req/2min)."""
    import requests

    backoff = 5.0
    for attempt in range(tries):
        try:
            r = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Range": f"bytes={first}-{last}",
                },
                stream=True,
                timeout=180,
            )
            if r.status_code in (200, 206):
                data = r.raw.read(last - first + 1)
                r.close()
                return data, r.status_code
            if r.status_code == 401:
                raise SystemExit("token expired: re-authenticate kaggle CLI")
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After") or 30)
                r.close()
                print(f"  429; sleeping {wait:.0f}s", flush=True)
                time.sleep(min(wait, 130.0) + 1.0)
                continue
            r.close()
        except SystemExit:
            raise
        except Exception:
            pass
        time.sleep(backoff)
        backoff *= 2
    return b"", 0


def cmd_probe(args: argparse.Namespace) -> None:
    filelist = json.loads(Path(args.filelist).read_text(encoding="utf-8"))
    files = [f for f in filelist["files"] if f["name"].endswith(".json")]
    token = _load_token()
    out_path = Path(args.out)
    done: dict[str, dict] = {}
    if out_path.exists() and not args.overwrite:
        done = json.loads(out_path.read_text(encoding="utf-8")).get("episodes", {})
    lock_print = lambda msg: print(msg, flush=True)

    def probe_one(f: dict):
        eid = f["name"].removesuffix(".json")
        if eid in done:
            return None
        url = SHARD_FILE_URL.format(slug=args.slug, fname=f["name"])
        data, code = _get_range(url, 0, PROBE_BYTES - 1, token)
        if not data:
            return ("FAILED", f["name"], code)
        text = data.decode("utf-8", errors="replace")
        m = TEAM_NAMES_RE.search(text)
        if not m:
            return ("NOTEAMNAMES", f["name"], len(text))
        try:
            teams = json.loads(m.group(1))
        except json.JSONDecodeError:
            return ("BADJSON", f["name"], 0)
        rec = {
            "episode_id": int(eid),
            "teams": teams,
            "size_bytes": f["bytes"],
            "slug": args.slug,
            "file": f["name"],
        }
        rw = REWARDS_RE.search(text)
        if rw:
            try:
                rec["rewards_head"] = json.loads(rw.group(1))
            except json.JSONDecodeError:
                pass
        return ("OK", eid, rec)

    results = {"ok": 0, "failed": []}

    def probe_one(f: dict):
        eid = f["name"].removesuffix(".json")
        if eid in done:
            return None
        time.sleep(args.pace)  # stay under the ~50 req / 2 min API limit
        url = SHARD_FILE_URL.format(slug=args.slug, fname=f["name"])
        data, code = _get_range(url, 0, PROBE_BYTES - 1, token)
        if not data:
            return ("FAILED", f["name"], code)
        text = data.decode("utf-8", errors="replace")
        m = TEAM_NAMES_RE.search(text)
        if not m:
            return ("NOTEAMNAMES", f["name"], len(text))
        try:
            teams = json.loads(m.group(1))
        except json.JSONDecodeError:
            return ("BADJSON", f["name"], 0)
        rec = {
            "episode_id": int(eid),
            "teams": teams,
            "size_bytes": f["bytes"],
            "slug": args.slug,
            "file": f["name"],
        }
        rw = REWARDS_RE.search(text)
        if rw:
            try:
                rec["rewards_head"] = json.loads(rw.group(1))
            except json.JSONDecodeError:
                pass
        return ("OK", eid, rec)

    for f in files:
        res = probe_one(f)
        if res is None:
            continue
        kind, key, payload = res
        if kind == "OK":
            done[str(key)] = payload
            results["ok"] += 1
            if results["ok"] % 25 == 0:
                lock_print(f"  probed {results['ok']}")
                out_path.write_text(
                    json.dumps({"slug": args.slug, "episodes": done}, indent=1),
                    encoding="utf-8",
                )
        else:
            results["failed"].append([kind, key, payload])
    out_path.write_text(
        json.dumps({"slug": args.slug, "episodes": done}, indent=1), encoding="utf-8"
    )
    lock_print(
        f"probe done: ok={results['ok']} failed={len(results['failed'])} -> {out_path}"
    )
    if results["failed"]:
        print(json.dumps(results["failed"][:20], indent=1))


def _load_leaderboard(path: str) -> dict[str, dict]:
    p = Path(path)
    if p.suffix == ".zip":
        z = zipfile.ZipFile(p)
        name = next(n for n in z.namelist() if n.endswith(".csv"))
        stream = io.TextIOWrapper(z.open(name), encoding="utf-8-sig")
        rows = list(csv.DictReader(stream))
    else:
        rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    teams = {}
    for r in rows:
        teams[r["TeamName"]] = {
            "rank": int(r["Rank"]),
            "score": float(r["Score"]),
            "team_id": r.get("TeamId", ""),
        }
    return teams


def _band_of(rank: int, score: float) -> list[str]:
    bands = []
    if rank <= 20:
        bands.append(BAND_TOP20)
    elif rank <= 100:
        bands.append(BAND_TOP100)
    if 500 <= score <= 900:
        bands.append(BAND_500_900)
    return bands


def cmd_select(args: argparse.Namespace) -> None:
    board = _load_leaderboard(args.leaderboard)
    probes = {}
    for path in args.probes.split(","):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for eid, rec in data["episodes"].items():
            probes[int(eid)] = rec

    # episodes per team
    per_team: dict[str, list[int]] = {}
    for eid, rec in probes.items():
        for t in rec["teams"]:
            per_team.setdefault(t, []).append(eid)

    top20_teams = sorted(
        [(v["rank"], name) for name, v in board.items() if v["rank"] <= 20]
    )
    plan = {BAND_TOP20: [], BAND_TOP100: [], BAND_500_900: [], BAND_BASELINE: []}
    picked: set[int] = set()

    # top-20: up to max_per_team_top20 episodes per team, favour opponents also top-100
    for rank, name in top20_teams:
        if len(plan[BAND_TOP20]) >= args.max_band_top20:
            break
        eids = sorted(per_team.get(name, []))
        scored = []
        for eid in eids:
            rec = probes[eid]
            opp_rank = min(
                (
                    board[o]["rank"]
                    for o in rec["teams"]
                    if o != name and o in board
                ),
                default=99999,
            )
            scored.append((opp_rank, eid))
        scored.sort()
        take = [eid for _, eid in scored[: args.max_per_team_top20]]
        for eid in take:
            if eid not in picked:
                plan[BAND_TOP20].append(eid)
                picked.add(eid)

    # top-100 (ranks 21-100): episodes not already picked where opponent is also
    # rank<=100 (shards only contain top-vs-~top games anyway), capped total
    for rank, name in sorted(
        [(v["rank"], n) for n, v in board.items() if 20 < v["rank"] <= 100]
    ):
        eids = sorted(per_team.get(name, []))
        scored = []
        for eid in eids:
            rec = probes[eid]
            opp_rank = min(
                (
                    board[o]["rank"]
                    for o in rec["teams"]
                    if o != name and o in board
                ),
                default=99999,
            )
            scored.append((opp_rank, eid))
        scored.sort()
        for _, eid in scored[: args.max_per_team_top100]:
            if eid not in picked:
                plan[BAND_TOP100].append(eid)
                picked.add(eid)
        if len(plan[BAND_TOP100]) >= args.max_band_top100:
            break

    # 500-900 band: from probes (expected empty in top-rated shards) + local
    # episodes staged from our own match history are added by `stage`, not here.
    for eid, rec in probes.items():
        if eid in picked:
            continue
        if any(
            t in board and BAND_500_900 in _band_of(board[t]["rank"], board[t]["score"])
            for t in rec["teams"]
        ):
            plan[BAND_500_900].append(eid)
            picked.add(eid)

    entries = []
    total = 0
    for band, eids in plan.items():
        for eid in eids:
            rec = probes[eid]
            total += rec["size_bytes"]
            entries.append(
                {
                    "episode_id": eid,
                    "band": band,
                    "teams": rec["teams"],
                    "size_bytes": rec["size_bytes"],
                    "slug": rec["slug"],
                    "file": rec["file"],
                }
            )
    if total > MAX_TOTAL_FETCH_BYTES:
        raise SystemExit(
            f"plan exceeds fetch budget: {total} > {MAX_TOTAL_FETCH_BYTES}"
        )
    slugs = {e["slug"] for e in entries}
    if len(slugs) > MAX_SHARDS:
        raise SystemExit(f"plan touches {len(slugs)} shards > {MAX_SHARDS}")
    out = {
        "capture_date": CAPTURE_DATE,
        "total_bytes": total,
        "counts": {b: len(e) for b, e in plan.items()},
        "entries": entries,
    }
    Path(args.plan_out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"plan: counts={out['counts']} total={total/1e6:.1f}MB -> {args.plan_out}")


def cmd_fetch(args: argparse.Namespace) -> None:
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    token = _load_token()

    def fetch_one(e: dict):
        out = dest / f"episode-{e['episode_id']}-replay.json"
        if out.exists() and out.stat().st_size == e["size_bytes"]:
            return ("SKIP", e["episode_id"])
        time.sleep(args.pace)
        url = SHARD_FILE_URL.format(slug=e["slug"], fname=e["file"])
        data, code = _get_range(url, 0, e["size_bytes"] - 1, token)
        if not data or len(data) != e["size_bytes"]:
            return ("FAILED", e["episode_id"], code, len(data))
        tmp = out.with_suffix(".part")
        tmp.write_bytes(data)
        tmp.replace(out)
        return ("OK", e["episode_id"], len(data))

    ok = failed = skipped = 0
    for e in plan["entries"]:
        res = fetch_one(e)
        if res[0] == "OK":
            ok += 1
            print(f"  ok {res[1]} ({res[2]/1e6:.1f}MB)", flush=True)
        elif res[0] == "SKIP":
            skipped += 1
        else:
            failed += 1
            print(f"  FAILED {res}", flush=True)
    print(f"fetch done: ok={ok} skip={skipped} failed={failed}")
    if failed:
        raise SystemExit(1)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_stage(args: argparse.Namespace) -> None:
    corpus = Path(args.corpus)
    board = _load_leaderboard(args.leaderboard) if args.leaderboard else {}
    local_sources = json.loads(Path(args.local_sources).read_text(encoding="utf-8"))

    manifest = {
        "schema": "m1-replay-corpus-manifest/1.0",
        "capture_date": CAPTURE_DATE,
        "files": [],
        "notes": [
            "raw replays live under .tmp-corpus/raw (gitignored); only small",
            "profile archives are committed under workspace/kaggriculture/software/exports/",
        ],
    }
    for raw in sorted((corpus / "raw").glob("*.json")):
        m = re.match(r"episode-(\d+)-replay\.json", raw.name)
        if not m:
            continue
        eid = int(m.group(1))
        src = local_sources.get(str(eid))
        if src is None:
            raise SystemExit(f"no source registered for {raw.name}; add to local_sources")
        # read team names from the file head (cheap)
        with open(raw, "rb") as fh:
            head = fh.read(65536).decode("utf-8", errors="replace")
        tm = TEAM_NAMES_RE.search(head)
        teams = json.loads(tm.group(1)) if tm else []
        ranks = [board.get(t, {}).get("rank") for t in teams]
        scores = [board.get(t, {}).get("score") for t in teams]
        bands = set(src.get("bands", []))
        for t, rk, sc in zip(teams, ranks, scores):
            if rk is None:
                continue
            bands.update(_band_of(rk, sc))
            if t == BASELINE_TEAM:
                bands.add(BAND_BASELINE)
        manifest["files"].append(
            {
                "file": f"raw/{raw.name}",
                "episode_id": eid,
                "sha256": _sha256(raw),
                "bytes": raw.stat().st_size,
                "source_url": src["source_url"],
                "source_slug": src.get("source_slug", ""),
                "capture_date": CAPTURE_DATE,
                "teams": teams,
                "team_ranks": ranks,
                "team_scores": scores,
                "bands": sorted(bands),
            }
        )
    out = corpus / "manifest.json"
    out.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    total = sum(f["bytes"] for f in manifest["files"])
    print(
        f"manifest: {len(manifest['files'])} files, {total/1e6:.1f}MB -> {out}"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("probe")
    p.add_argument("--filelist", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--pace", type=float, default=0.5, help="seconds between requests")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("select")
    p.add_argument("--probes", required=True, help="comma-separated probe jsons")
    p.add_argument("--leaderboard", required=True)
    p.add_argument("--plan-out", required=True)
    p.add_argument("--max-per-team-top20", type=int, default=3)
    p.add_argument("--max-band-top20", type=int, default=42)
    p.add_argument("--max-per-team-top100", type=int, default=2)
    p.add_argument("--max-band-top100", type=int, default=14)
    p.set_defaults(func=cmd_select)

    p = sub.add_parser("fetch")
    p.add_argument("--plan", required=True)
    p.add_argument("--dest", default=".tmp-corpus/raw")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--pace", type=float, default=1.0, help="seconds between fetches")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("stage")
    p.add_argument("--corpus", default=".tmp-corpus")
    p.add_argument("--leaderboard")
    p.add_argument(
        "--local-sources",
        default=".tmp-corpus/local-sources.json",
        help="episode_id -> {source_url, source_slug?, bands?}",
    )
    p.set_defaults(func=cmd_stage)

    args = ap.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
