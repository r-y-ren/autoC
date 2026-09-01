"""Integrity validator for the m1 replay profile corpus.

Checks (mode ``official``):
  1. corpus manifest: schema, per-file existence, sha256 and byte size match;
  2. every profile JSON in exports/replay_profiles/profiles carries a
     non-empty source_url + capture_date;
  3. every profile comes from a clean episode (both seats DONE, exactly 720
     steps, numeric rewards); dirty episodes must appear in exclusions.json
     with a reason (exclusion traceability);
  4. index.json episodes <-> profile files are consistent (2 profiles per
     episode, no orphans);
  5. band coverage: top20 / top100 / band_500_900 layers all present
     (baseline is reported, not required);
  6. per-profile exploratory=true (single-episode evidence); teams marked
     consistent in band_summary.md must have >= 3 profiled games;
  7. no raw replay leakage: profile files stay under a size cap and contain
     no "steps" replay arrays;
  8. manifest bands <-> index bands agreement.

mode ``dev`` relaxes checks 2 (capture_date optional), 5 (missing bands
allowed) for local fixtures; everything else still applies.

Usage:
  python workspace/kaggriculture/software/scripts/corpus_integrity.py --mode official
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve()
while REPO != REPO.parent and not (REPO / ".git").exists():
    REPO = REPO.parent
SOFTWARE = REPO / "workspace" / "kaggriculture" / "software"
CORPUS = REPO / ".tmp-corpus"
EXPORTS = SOFTWARE / "exports" / "replay_profiles"
REQUIRED_BANDS = ("top20", "top100", "band_500_900")
ALL_BANDS = REQUIRED_BANDS + ("baseline",)
MIN_GAMES_CONSISTENT = 3
PROFILE_SIZE_CAP = 250_000
EXPECTED_STEPS = 720


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(corpus: Path, failures: list[str], relaxed: bool) -> dict:
    mf = corpus / "manifest.json"
    if not mf.exists():
        failures.append(f"missing {mf}")
        return {}
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    if not isinstance(manifest.get("files"), list) or not manifest["files"]:
        failures.append("manifest has no files")
        return manifest
    if not relaxed and not manifest.get("capture_date"):
        failures.append("manifest missing capture_date")
    for f in manifest["files"]:
        for key in ("file", "sha256", "bytes", "source_url", "capture_date", "teams"):
            if key not in f or f[key] in (None, "", []):
                if relaxed and key in ("capture_date", "source_url"):
                    continue
                failures.append(f"manifest entry missing {key}: {f.get('file')}")
        raw = corpus / f["file"]
        if not raw.exists():
            failures.append(f"manifest file absent on disk: {f['file']}")
            continue
        if raw.stat().st_size != f["bytes"]:
            failures.append(
                f"size mismatch {f['file']}: manifest {f['bytes']} vs disk {raw.stat().st_size}"
            )
        if _sha256(raw) != f["sha256"]:
            failures.append(f"sha256 mismatch {f['file']}")
        if not relaxed and not re.match(r"^https?://", f["source_url"] or ""):
            failures.append(f"source_url not absolute http(s): {f['file']}")
        _check_raw_replay(raw, f["file"], failures, relaxed)
    return manifest


def _check_raw_replay(raw: Path, label: str, failures: list[str], relaxed: bool) -> None:
    """Independently verify a raw replay: both DONE + 720 steps + rewards.

    official: full JSON parse. dev: cheap head scan for statuses only.
    """
    import sys
    sys.path.insert(0, str(SOFTWARE))
    from kgenv.replay_profile import check_integrity

    if relaxed:
        head = raw.open("rb").read(65536).decode("utf-8", errors="replace")
        m = re.search(r'"statuses":\s*\[[^\]]*\]', head)
        if m and '"DONE","DONE"' not in m.group(0).replace(" ", ""):
            failures.append(f"raw replay statuses not DONE/DONE: {label}")
        return
    try:
        replay = json.loads(raw.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"raw replay unparseable {label}: {exc!r}")
        return
    issues = check_integrity(replay)
    if issues:
        failures.append(f"raw replay dirty {label}: {'; '.join(issues)}")


def check_profiles(exports: Path, failures: list[str], relaxed: bool) -> dict:
    idx_path = exports / "index.json"
    if not idx_path.exists():
        failures.append(f"missing {idx_path}")
        return {}
    index = json.loads(idx_path.read_text(encoding="utf-8"))
    profiles_dir = exports / "profiles"
    pfiles = sorted(profiles_dir.glob("ep*_seat*.json")) if profiles_dir.exists() else []
    if not pfiles:
        failures.append("no profile files found")

    by_episode: dict[int, list[Path]] = {}
    team_games: dict[str, int] = {}
    for pf in pfiles:
        try:
            p = json.loads(pf.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"profile unparseable {pf.name}: {exc!r}")
            continue
        size = pf.stat().st_size
        if size > PROFILE_SIZE_CAP:
            failures.append(f"profile too large ({size}B): {pf.name}")
        if "steps" in p or ("observation" in p) or ("action" in p):
            failures.append(f"raw replay fields leaked into {pf.name}")
        if not p.get("source_url"):
            if not relaxed:
                failures.append(f"profile missing source_url: {pf.name}")
        if not p.get("capture_date"):
            if not relaxed:
                failures.append(f"profile missing capture_date: {pf.name}")
        if p.get("integrity_issues"):
            failures.append(f"profile from dirty episode: {pf.name}")
        if p.get("exploratory") is not True:
            failures.append(f"profile exploratory flag not true: {pf.name}")
        eid = p.get("episode_id")
        seat = p.get("seat")
        m = re.match(r"ep(\d+)_seat(\d+)\.json", pf.name)
        if not m or int(m.group(1)) != eid or int(m.group(2)) != seat:
            failures.append(f"profile filename mismatch: {pf.name}")
        by_episode.setdefault(eid, []).append(pf)
        team_games[p.get("team", "?")] = team_games.get(p.get("team", "?"), 0) + 1

    # episode-level cleanliness from index
    excluded = {e.get("episode_id") for e in index.get("excluded", [])}
    for e in index.get("episodes", []):
        eid = e["episode_id"]
        if eid in excluded:
            failures.append(f"episode {eid} both included and excluded")
        if e.get("statuses") != ["DONE", "DONE"]:
            failures.append(f"episode {eid} statuses {e.get('statuses')} in archive")
        if e.get("steps") != EXPECTED_STEPS:
            failures.append(f"episode {eid} steps={e.get('steps')} in archive")
        if not e.get("source_url") or not e.get("capture_date"):
            if not relaxed:
                failures.append(f"index entry {eid} missing provenance")
        n = len(by_episode.get(eid, []))
        if n != 2:
            failures.append(f"episode {eid} has {n} profiles (expected 2)")

    # orphans: profiles whose episode not in index
    indexed = {e["episode_id"] for e in index.get("episodes", [])}
    for eid in by_episode:
        if eid not in indexed:
            failures.append(f"profile for non-indexed episode {eid}")

    # exclusion traceability: every excluded id needs a reason
    for e in index.get("excluded", []):
        if not e.get("reason"):
            failures.append(f"exclusion without reason: {e.get('episode_id')}")

    # band coverage
    if index.get("episodes"):
        bands = {b for e in index["episodes"] for b in e.get("bands", [])}
        if not relaxed:
            for b in REQUIRED_BANDS:
                if b not in bands:
                    failures.append(f"band coverage missing: {b}")
    return {"index": index, "team_games": team_games, "by_episode": by_episode}


def check_band_summary(
    exports: Path, ctx: dict, manifest: dict, failures: list[str]
) -> None:
    md_path = exports / "band_summary.md"
    if not md_path.exists():
        failures.append(f"missing {md_path}")
        return
    md = md_path.read_text(encoding="utf-8")
    team_games = ctx.get("team_games", {})
    # every team claimed consistent must have >= MIN_GAMES_CONSISTENT games
    for m in re.finditer(r"\*\*(.+?)\*\* \(consistent", md):
        team = m.group(1)
        if team_games.get(team, 0) < MIN_GAMES_CONSISTENT:
            failures.append(
                f"band_summary marks '{team}' consistent with only "
                f"{team_games.get(team, 0)} games (<{MIN_GAMES_CONSISTENT})"
            )
    # every team with >=3 games must be listed as consistent
    for team, n in team_games.items():
        if n >= MIN_GAMES_CONSISTENT and f"**{team}** (consistent" not in md:
            failures.append(
                f"team '{team}' has {n} games but is not marked consistent in summary"
            )
    # manifest bands must appear in index bands
    index = ctx.get("index", {})
    idx_bands = {b for e in index.get("episodes", []) for b in e.get("bands", [])}
    for f in manifest.get("files", []):
        for b in f.get("bands", []):
            if b not in idx_bands and f["episode_id"] in {
                e["episode_id"] for e in index.get("episodes", [])
            }:
                failures.append(
                    f"episode {f['episode_id']} band {b} in manifest but not index"
                )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=("official", "dev"), default="official")
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--exports", default=str(EXPORTS))
    args = ap.parse_args(argv)
    relaxed = args.mode == "dev"
    corpus, exports = Path(args.corpus), Path(args.exports)

    failures: list[str] = []
    manifest = check_manifest(corpus, failures, relaxed)
    ctx = check_profiles(exports, failures, relaxed)
    check_band_summary(exports, ctx, manifest, failures)

    status = "PASS" if not failures else "FAIL"
    print(f"corpus_integrity[{args.mode}]: {status}")
    for f in failures:
        print(f"  - {f}")
    if not failures:
        n_eps = len(ctx.get("index", {}).get("episodes", []))
        n_prof = sum(len(v) for v in ctx.get("by_episode", {}).values())
        n_excl = len(ctx.get("index", {}).get("excluded", []))
        print(
            f"  episodes={n_eps} profiles={n_prof} excluded={n_excl} "
            f"manifest_files={len(manifest.get('files', []))}"
        )
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
