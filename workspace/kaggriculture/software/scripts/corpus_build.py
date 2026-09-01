"""Build the m1 replay profile corpus from workspace/kaggriculture/references/data/replay-corpus raw replays.

Walks workspace/kaggriculture/references/data/replay-corpus/raw/episode-*-replay.json (registered in workspace/kaggriculture/references/data/replay-corpus/manifest.json),
runs integrity checks (both seats DONE + 720 steps + numeric rewards), extracts
per-player profiles via kgenv.replay_profile, and writes the small profile
archive to workspace/kaggriculture/software/exports/replay_profiles/:

  profiles/ep{eid}_seat{pl}.json   one profile per episode x player
  index.json                       episode index (bands, teams, integrity)
  exclusions.json                  abnormal episodes with rejection reason
  band_summary.md                  layered band summaries + cross-game
                                  consistency review (>=3 games -> consistent,
                                  otherwise exploratory)

Raw replays never enter the archive. Run from repo root:
  python workspace/kaggriculture/software/scripts/corpus_build.py
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve()
while REPO != REPO.parent and not (REPO / ".git").exists():
    REPO = REPO.parent
SOFTWARE = REPO / "workspace" / "kaggriculture" / "software"
sys.path.insert(0, str(SOFTWARE))

from kgenv.replay_profile import (  # noqa: E402
    IntegrityError,
    check_integrity,
    extract_episode_profiles,
    load_replay,
)

CORPUS = REPO / "workspace" / "kaggriculture" / "references" / "data" / "replay-corpus"
EXPORTS = (
    SOFTWARE / "exports" / "replay_profiles"
)
BANDS = ("top20", "top100", "band_500_900", "baseline")
BASELINE_TEAM = "renyxin"
MIN_GAMES_CONSISTENT = 3
PROFILE_SIZE_WARN = 250_000  # bytes; guards against accidental raw dumps


def _fmt(x, nd=1):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:,.{nd}f}"
    return f"{x:,}"


def build(corpus_dir: Path, exports_dir: Path) -> dict:
    manifest = json.loads((corpus_dir / "manifest.json").read_text(encoding="utf-8"))
    by_id = {f["episode_id"]: f for f in manifest["files"]}
    profiles_dir = exports_dir / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    index_entries = []
    exclusions = []
    n_profiles = 0
    t0 = time.time()
    for raw in sorted((corpus_dir / "raw").glob("episode-*-replay.json")):
        m = re.match(r"episode-(\d+)-replay\.json", raw.name)
        if not m:
            exclusions.append(
                {"file": raw.name, "reason": "unparseable filename"}
            )
            continue
        eid = int(m.group(1))
        meta = by_id.get(eid)
        if meta is None:
            exclusions.append(
                {"episode_id": eid, "reason": "not registered in manifest"}
            )
            continue
        try:
            replay = load_replay(raw)
        except Exception as exc:  # malformed json
            exclusions.append(
                {"episode_id": eid, "reason": f"json load failed: {exc!r}"}
            )
            continue
        issues = check_integrity(replay)
        if issues:
            exclusions.append(
                {
                    "episode_id": eid,
                    "teams": (replay.get("info") or {}).get("TeamNames"),
                    "reason": "; ".join(issues),
                }
            )
            continue
        try:
            res = extract_episode_profiles(
                replay,
                episode_id=eid,
                source_url=meta["source_url"],
                capture_date=meta["capture_date"],
                strict=True,
            )
        except IntegrityError as exc:
            exclusions.append({"episode_id": eid, "reason": str(exc)})
            continue
        bands = sorted(set(meta.get("bands") or []))
        for p in res["players"]:
            p["bands"] = bands
            p["exploratory"] = True  # single-episode evidence by definition
            out = profiles_dir / f"ep{eid}_seat{p['seat']}.json"
            payload = json.dumps(p, ensure_ascii=False, indent=1)
            if len(payload.encode("utf-8")) > PROFILE_SIZE_WARN:
                raise SystemExit(
                    f"profile {out.name} too large; raw replay leak suspected"
                )
            out.write_text(payload, encoding="utf-8")
            n_profiles += 1
        index_entries.append(
            {
                "episode_id": eid,
                "teams": res["episode"]["teams"],
                "rewards": res["episode"]["rewards"],
                "statuses": res["episode"]["statuses"],
                "steps": res["episode"]["steps"],
                "bands": bands,
                "source_url": meta["source_url"],
                "capture_date": meta["capture_date"],
                "raw_sha256": meta["sha256"],
                "raw_bytes": meta["bytes"],
            }
        )
    runtime = round(time.time() - t0, 1)

    index = {
        "schema": "m1-replay-profile-index/1.0",
        "episodes": index_entries,
        "excluded": exclusions,
        "counts": {
            "episodes": len(index_entries),
            "profiles": n_profiles,
            "excluded": len(exclusions),
        },
        "build_runtime_seconds": runtime,
    }
    (exports_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (exports_dir / "exclusions.json").write_text(
        json.dumps(
            {"schema": "m1-exclusions/1.0", "excluded": exclusions},
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    return index


def _team_games(index: dict) -> dict[str, list[dict]]:
    """team -> list of {episode, profile} from the profile archive."""
    games: dict[str, list[dict]] = defaultdict(list)
    for pf in sorted((EXPORTS / "profiles").glob("ep*_seat*.json")):
        p = json.loads(pf.read_text(encoding="utf-8"))
        games[p["team"]].append(p)
    return games


def write_band_summary(exports_dir: Path, index: dict, board: dict) -> str:
    games = _team_games(index)
    lines: list[str] = []
    ap = lines.append
    ap("# Kaggriculture m1 replay profile corpus - band summary")
    ap("")
    ap(
        f"Source: official Kaggle daily episode shards + own ladder episodes. "
        f"Capture date 2026-08-29. Episodes profiled: {index['counts']['episodes']}"
        f" ({index['counts']['profiles']} player profiles, "
        f"{index['counts']['excluded']} excluded as abnormal)."
    )
    ap("")
    ap(
        "All per-episode player conclusions are `exploratory` (single-game "
        "evidence). A team is marked `consistent` only with "
        f">= {MIN_GAMES_CONSISTENT} profiled episodes."
    )
    ap("")
    for band in BANDS:
        eps = [e for e in index["episodes"] if band in e["bands"]]
        teams = sorted({t for e in eps for t in e["teams"]})
        ap(f"## Band: {band} ({len(eps)} episodes, {len(teams)} teams)")
        ap("")
        if not eps:
            ap("_no episodes in this band_")
            ap("")
            continue
        for e in eps:
            ap(
                f"- ep {e['episode_id']}: {' vs '.join(e['teams'])} "
                f"rewards {e['rewards']} ({e['source_url']})"
            )
        ap("")
        # aggregate band medians over profiles of players who themselves
        # belong to this band (baseline = our own seat only)
        band_eps = {e["episode_id"] for e in eps}

        def _in_band(team: str) -> bool:
            info = board.get(team)
            if band == "baseline":
                return team == BASELINE_TEAM
            if info is None:
                return False
            rk, sc = info["rank"], info["score"]
            if band == "top20":
                return rk <= 20
            if band == "top100":
                return 20 < rk <= 100
            if band == "band_500_900":
                return 500 <= sc <= 900
            return False

        finals, hires, feeds, crop_rev_share, endgame_gains = [], [], [], [], []
        for team_profiles in games.values():
            for p in team_profiles:
                if p["episode_id"] not in band_eps:
                    continue
                if not _in_band(p["team"]):
                    continue
                if p["money"]["final"] is not None:
                    finals.append(p["money"]["final"])
                hires.append(p["hires"]["avg_per_day"])
                if p["external_buys"]["feed_qty"]:
                    feeds.append(p["external_buys"]["feed_qty"])
                tot = p["sells"]["total_quoted_revenue"] or 0
                if tot:
                    crop_rev_share.append(
                        p["sells"]["crop_quoted_revenue"] / tot
                    )
                if p["endgame"]["gain_pct_of_final"] is not None:
                    endgame_gains.append(p["endgame"]["gain_pct_of_final"])
        ap(
            f"- median final money: {_fmt(statistics.median(finals), 0)} | "
            f"median hires/day: {_fmt(statistics.median(hires), 1)} | "
            f"median crop revenue share: {_fmt(statistics.median(crop_rev_share) * 100 if crop_rev_share else None, 0)}% | "
            f"median endgame gain: {_fmt(statistics.median(endgame_gains), 1) if endgame_gains else '-'}% of final"
        )
        ap("")

    ap("## Cross-game consistency review (same team, >= 3 games)")
    ap("")
    consistent_teams = 0
    for team, profs in sorted(
        games.items(), key=lambda kv: (-len(kv[1]), kv[0])
    ):
        if len(profs) < MIN_GAMES_CONSISTENT:
            continue
        consistent_teams += 1
        finals = [p["money"]["final"] for p in profs]
        hire_avg = [p["hires"]["avg_per_day"] for p in profs]
        feed = [p["external_buys"]["feed_qty"] for p in profs]
        share = [
            p["crops"]["tile_day_share"].get("WHEAT", 0)
            for p in profs
        ]
        ap(
            f"- **{team}** (consistent, {len(profs)} games): "
            f"final money {[_fmt(f, 0) for f in finals]} "
            f"(cv {_fmt(_cv(finals) * 100 if len(finals) > 1 else None, 0)}%), "
            f"hires/day {[_fmt(h, 1) for h in hire_avg]}, "
            f"feed qty {feed}, "
            f"wheat field share {[_fmt(s * 100, 0) for s in share]}%"
        )
    if not consistent_teams:
        ap(
            f"_no team reached {MIN_GAMES_CONSISTENT} profiled games; "
            "all team-level conclusions stay exploratory._"
        )
    ap("")
    n_low = sum(1 for v in games.values() if len(v) < MIN_GAMES_CONSISTENT)
    ap(
        f"Teams with < {MIN_GAMES_CONSISTENT} profiled games (exploratory): "
        f"{n_low}. "
    )
    ranks = {
        t: f"rank {board[t]['rank']} ({board[t]['score']:.1f})"
        for t in games
        if t in board
    }
    ap("")
    ap("## Team leaderboard positions (2026-08-29 public leaderboard)")
    ap("")
    for t, r in sorted(ranks.items(), key=lambda kv: int(kv[1].split()[1])):
        ap(f"- {t}: {r}")
    md = "\n".join(lines) + "\n"
    (exports_dir / "band_summary.md").write_text(md, encoding="utf-8")
    return md


def _cv(xs: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    m = statistics.fmean(xs)
    return statistics.pstdev(xs) / m if m else None


def _load_board(path: str) -> dict:
    import csv
    import io
    import zipfile

    p = Path(path)
    if p.suffix == ".zip":
        z = zipfile.ZipFile(p)
        name = next(n for n in z.namelist() if n.endswith(".csv"))
        rows = list(
            csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8-sig"))
        )
    else:
        rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    return {r["TeamName"]: {"rank": int(r["Rank"]), "score": float(r["Score"])} for r in rows}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--exports", default=str(EXPORTS))
    ap.add_argument(
        "--leaderboard",
        default=str(REPO / "workspace" / "kaggriculture" / "references" / "data" / "online-replays" / "kaggriculture.zip"),
    )
    args = ap.parse_args(argv)
    exports_dir = Path(args.exports)
    exports_dir.mkdir(parents=True, exist_ok=True)
    index = build(Path(args.corpus), exports_dir)
    board = _load_board(args.leaderboard) if args.leaderboard else {}
    write_band_summary(exports_dir, index, board)
    print(
        f"built: {index['counts']} runtime={index['build_runtime_seconds']}s"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
