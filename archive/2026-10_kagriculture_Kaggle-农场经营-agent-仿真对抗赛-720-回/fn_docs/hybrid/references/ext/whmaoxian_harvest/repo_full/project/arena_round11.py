"""Frozen, paired-seat Kaggriculture arena for prospective Round 11 work.

The official 720-step game runner is league_round9.run_job. This module adds
source/seed manifests, family-level matched comparisons, and held-out gates.
Importing it never starts a game or opens a held-out split.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import random
import re
import statistics
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import league_round9

ROOT = Path(__file__).resolve().parent
SEED_PATH = ROOT / "research/round11/league_seeds.json"
RESULTS = ROOT / "results/round11"
BASELINE_CACHE = RESULTS / "baseline_cache_v2"
FROZEN = ROOT / "research/round11/frozen"
COUNTS = {"development": 24, "confirmation": 48, "reserve": 48}
CORE = (
    ("self_v9", "submissions/release_v9/main.py", "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"),
    ("frontier", "external/round9/frontier/main.py", "178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a"),
    ("master", "external/round8/master2965/main.py", "93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f"),
    ("dsm_proxy", "experiments/round8_top2_dsm_strict.py", "8340cedac73c4a54ca6f1a440385514ef2a9c4fd613c6c86cf14312fc19b9e3f"),
)
PRIOR_SEEDS = (
    ROOT / "research/round8/league_seeds.json",
    ROOT / "research/round9/league_seeds.json",
    ROOT / "research/round10/league_seeds.json",
)
ENGINE_VERSION = "1.32.7"
GAME_RUNNER = ROOT / "league_round9.py"
NAME = re.compile(r"[a-z][a-z0-9_-]{1,47}\Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_path(raw: str) -> tuple[str, Path]:
    path = (ROOT / raw).resolve()
    relative = path.relative_to(ROOT).as_posix()
    if not path.is_file() or path.suffix != ".py":
        raise ValueError(f"Agent source must be a Python file within the workspace: {raw}")
    return relative, path


def expected_seeds() -> dict[str, list[int]]:
    return {
        split: [
            int.from_bytes(
                hashlib.sha256(f"kaggriculture-r11-prospective-{split}-{i}".encode()).digest()[:4],
                "big",
            ) % 2_000_000_000
            for i in range(count)
        ]
        for split, count in COUNTS.items()
    }


def check_seed_separation(seeds: dict[str, list[int]]) -> dict[str, int]:
    current = [seed for split in COUNTS for seed in seeds[split]]
    if len(current) != sum(COUNTS.values()) or len(current) != len(set(current)):
        raise ValueError("Round 11 seeds collide across splits")
    prior = set()
    for path in PRIOR_SEEDS:
        old = json.loads(path.read_text(encoding="utf-8"))
        prior.update(seed for group in old.values() for seed in group)
    if prior.intersection(current):
        raise ValueError("Round 11 seeds collide with earlier league manifests")
    return {"round11_worlds": len(current), "earlier_league_worlds": len(prior), "overlap": 0}


def frozen_seeds(create: bool = False) -> dict[str, list[int]]:
    expected = expected_seeds()
    check_seed_separation(expected)
    if not SEED_PATH.exists():
        if not create:
            raise FileNotFoundError("Initialize the prospective seeds first: python arena_round11.py init")
        SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
        SEED_PATH.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    if json.loads(SEED_PATH.read_text(encoding="utf-8")) != expected:
        raise ValueError("The frozen Round 11 seed manifest changed")
    return expected


def source(raw: str, locked_sha: str | None = None) -> dict[str, str]:
    relative, path = canonical_path(raw)
    current = sha(path)
    if locked_sha and current != locked_sha:
        raise ValueError(f"Frozen source changed: {relative}")
    return {"path": relative, "sha256": current}


def opponents(extras: list[str]) -> list[dict[str, str]]:
    roster = [{"family": family, **source(path, digest)} for family, path, digest in CORE]
    seen = {(entry["family"], entry["path"]) for entry in roster}
    seen_paths = {entry["path"] for entry in roster}
    for spec in extras:
        if "=" not in spec:
            raise ValueError("Use --extra-opponent FAMILY=relative/path.py")
        family, path = spec.split("=", 1)
        if not NAME.fullmatch(family):
            raise ValueError(f"Invalid opponent family: {family}")
        if family in {entry[0] for entry in CORE}:
            raise ValueError("Core opponent families are frozen; extras need a distinct diagnostic family")
        entry = {"family": family, **source(path)}
        key = (family, entry["path"])
        if key in seen or entry["path"] in seen_paths:
            raise ValueError(f"Duplicate opponent: {spec}")
        seen.add(key)
        seen_paths.add(entry["path"])
        roster.append(entry)
    return roster


def manifest(candidate: str, extras: list[str], split: str, run_name: str) -> dict:
    if not NAME.fullmatch(run_name):
        raise ValueError("--run-name needs 2-48 lowercase letters, digits, _ or -")
    seeds = frozen_seeds()
    engine = importlib.metadata.version("kaggle-environments")
    if engine != ENGINE_VERSION:
        raise ValueError(f"Official engine version changed: {engine} != {ENGINE_VERSION}")
    return {
        "schema": "kaggriculture-arena-r11-v2",
        "run_name": run_name,
        "split": split,
        "seeds": seeds[split],
        "seed_manifest_sha256": sha(SEED_PATH),
        "engine_version": engine,
        "episode_steps": 720,
        "seats": [0, 1],
        "candidate": source(candidate),
        "baseline": source(CORE[0][1], CORE[0][2]),
        "opponents": opponents(extras),
        "arena_sha256": sha(Path(__file__)),
        "game_runner_sha256": sha(GAME_RUNNER),
    }


def paths(run_name: str, split: str) -> dict[str, Path]:
    base = RESULTS / f"{run_name}-{split}"
    return {"manifest": base.with_suffix(".manifest.json"),
            "ledger": base.with_suffix(".jsonl"),
            "report": base.with_suffix(".summary.json")}


def jobs(m: dict, count: int | None = None) -> list[dict]:
    selected = m["seeds"][:count]
    result = []
    for seed in selected:
        for opp in m["opponents"]:
            for participant in ("candidate", "baseline"):
                actor = m[participant]
                for seat in (0, 1):
                    job = {
                        "candidate": str(ROOT / actor["path"]),
                        "candidate_sha256": actor["sha256"],
                        "opponent": str(ROOT / opp["path"]),
                        "opponent_sha256": opp["sha256"],
                        "participant": participant,
                        "family": opp["family"],
                        "seed": seed,
                        "seat": seat,
                        "split": m["split"],
                        "engine_version": m["engine_version"],
                        "episode_steps": m["episode_steps"],
                        "arena_sha256": m["arena_sha256"],
                        "game_runner_sha256": m["game_runner_sha256"],
                    }
                    job["id"] = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()[:24]
                    result.append(job)
    return result


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def baseline_cache_inputs(job: dict) -> dict:
    if job["participant"] != "baseline" or job["split"] != "development":
        raise ValueError("Baseline cache is development-only")
    if job["candidate_sha256"] != CORE[0][2]:
        raise ValueError("Only frozen V9 may populate the baseline cache")
    return {key: job[key] for key in (
        "split", "engine_version", "episode_steps", "seed", "seat",
        "candidate", "candidate_sha256", "opponent", "opponent_sha256",
        "arena_sha256", "game_runner_sha256")}


def baseline_cache_key(job: dict) -> str:
    return hashlib.sha256(canonical_json(baseline_cache_inputs(job))).hexdigest()


def game_result_errors(row: dict, job: dict) -> list[str]:
    problems = []
    if row.get("valid") is not True or row.get("invalid_reasons", []) != []:
        problems.append("invalid_result")
    if any(row.get(key) != value for key, value in job.items()):
        problems.append("job_metadata_mismatch")
    if row.get("environment_version") != job["engine_version"]:
        problems.append("engine_version_mismatch")
    if row.get("states") != job["episode_steps"] or row.get("statuses") != ["DONE", "DONE"]:
        problems.append("incomplete_game")
    if row.get("stderr") != [] or row.get("exception"):
        problems.append("agent_or_engine_error")
    telemetry = row.get("telemetry")
    if (not isinstance(telemetry, list) or len(telemetry) != 2
            or any(not isinstance(item, dict) or item.get("nonzero") != {} for item in telemetry)):
        problems.append("agent_telemetry_error")
    values = [row.get(field) for field in ("money", "opponent_money", "delta", "points")]
    if any(isinstance(value, bool) or not isinstance(value, (int, float))
           or not math.isfinite(value) for value in values):
        problems.append("nonfinite_or_missing_result")
    else:
        money, opponent_money, delta, points = values
        expected_points = 1 if delta > 0 else 0 if delta < 0 else .5
        if not math.isclose(delta, money - opponent_money, rel_tol=0, abs_tol=1e-9):
            problems.append("money_delta_mismatch")
        if points != expected_points:
            problems.append("win_points_mismatch")
    return problems


def read_baseline_cache(job: dict, cache_dir: Path = BASELINE_CACHE) -> dict | None:
    key = baseline_cache_key(job)
    target = cache_dir / f"{key}.json"
    if not target.exists():
        return None
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("payload_type")
        if payload.get("schema") != "kaggriculture-v9-baseline-cache-v2":
            raise ValueError("schema")
        if payload.get("key") != key or payload.get("inputs") != baseline_cache_inputs(job):
            raise ValueError("cache_key_or_inputs")
        row = payload["row"]
        if not isinstance(row, dict):
            raise ValueError("row_type")
        if hashlib.sha256(canonical_json(row)).hexdigest() != payload.get("row_sha256"):
            raise ValueError("row_checksum")
        problems = game_result_errors(row, job)
        if problems:
            raise ValueError(",".join(problems))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"Malformed baseline cache {target}: {exc}") from exc
    if sha(Path(job["candidate"])) != job["candidate_sha256"]:
        raise ValueError(f"Frozen V9 bytes changed before cache reuse: {target}")
    if sha(Path(job["opponent"])) != job["opponent_sha256"]:
        raise ValueError(f"Opponent bytes changed before cache reuse: {target}")
    if sha(GAME_RUNNER) != job["game_runner_sha256"] or sha(Path(__file__)) != job["arena_sha256"]:
        raise ValueError(f"Runner bytes changed before cache reuse: {target}")
    return {**row, "baseline_cache_key": key, "baseline_cache_hit": True}


def write_baseline_cache(job: dict, row: dict, cache_dir: Path = BASELINE_CACHE) -> str:
    key = baseline_cache_key(job)
    problems = game_result_errors(row, job)
    if problems:
        raise ValueError(f"Refusing to cache invalid V9 game {key}: {problems}")
    for path_key, hash_key in (("candidate", "candidate_sha256"), ("opponent", "opponent_sha256")):
        if sha(Path(job[path_key])) != job[hash_key]:
            raise ValueError(f"Source changed during V9 baseline game: {job[path_key]}")
    if sha(GAME_RUNNER) != job["game_runner_sha256"] or sha(Path(__file__)) != job["arena_sha256"]:
        raise ValueError("Runner changed during V9 baseline game")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{key}.json"
    if target.exists():
        prior = read_baseline_cache(job, cache_dir)
        if any(prior.get(field) != row.get(field) for field in
               ("money", "opponent_money", "delta", "points", "shops")):
            raise ValueError(f"V9 baseline is nondeterministic for cache key {key}")
        return key
    payload = {"schema": "kaggriculture-v9-baseline-cache-v2", "key": key,
               "inputs": baseline_cache_inputs(job), "row": row,
               "row_sha256": hashlib.sha256(canonical_json(row)).hexdigest()}
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", prefix=f"{key}.", suffix=".tmp",
                                         dir=cache_dir, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(canonical_json(payload) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            prior = read_baseline_cache(job, cache_dir)
            if any(prior.get(field) != row.get(field) for field in
                   ("money", "opponent_money", "delta", "points", "shops")):
                raise ValueError(f"V9 baseline is nondeterministic for cache key {key}")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return key


def plan_pending(m: dict, pending: list[dict], cache_dir: Path = BASELINE_CACHE) -> tuple[list[dict], list[dict]]:
    cached, to_run = [], []
    for job in pending:
        if m["split"] == "development" and job["participant"] == "baseline":
            row = read_baseline_cache(job, cache_dir)
            if row is not None:
                cached.append(row)
                continue
        to_run.append(job)
    return cached, to_run


def load_ledger(path: Path, m: dict) -> list[dict]:
    expected = {j["id"]: j for j in jobs(m)}
    rows = []
    ids = set()
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        job = expected.get(row.get("id"))
        if job is None or row["id"] in ids or any(row.get(k) != v for k, v in job.items()):
            raise ValueError(f"Ledger contains an unknown, duplicate, or modified job: {row.get('id')}")
        ids.add(row["id"])
        rows.append(row)
    return rows


def run_checked(job: dict) -> dict:
    if sha(GAME_RUNNER) != job["game_runner_sha256"] or sha(Path(__file__)) != job["arena_sha256"]:
        return {**job, "valid": False, "invalid_reasons": ["runner_changed_before_game"]}
    row = league_round9.run_job(job)
    reasons = game_result_errors(row, job)
    if sha(GAME_RUNNER) != job["game_runner_sha256"] or sha(Path(__file__)) != job["arena_sha256"]:
        reasons.append("runner_changed_during_game")
    row["valid"] = not reasons
    row["invalid_reasons"] = reasons
    return row


def record_stats(group: list[dict]) -> dict:
    if not group:
        return {"games": 0, "wins": 0, "losses": 0, "ties": 0,
                "win_points": None, "mean_margin": None, "median_margin": None}
    margins = [row["delta"] for row in group]
    return {
        "games": len(group),
        "wins": sum(x > 0 for x in margins),
        "losses": sum(x < 0 for x in margins),
        "ties": sum(x == 0 for x in margins),
        "win_points": statistics.mean(row["points"] for row in group),
        "mean_margin": statistics.mean(margins),
        "median_margin": statistics.median(margins),
    }


def bootstrap_world(values: list[float], draws: int = 3000) -> list[float] | None:
    if not values:
        return None
    rng = random.Random(20260923)
    sample = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(draws))
    return [sample[int(0.025 * draws)], sample[int(0.975 * draws) - 1]]


def summarize(m: dict, rows: list[dict]) -> dict:
    all_jobs = jobs(m)
    valid = [row for row in rows if row.get("valid")]
    complete = len(rows) == len(all_jobs)
    report = {
        "schema": "kaggriculture-arena-r11-summary-v1",
        "run_name": m["run_name"], "split": m["split"],
        "expected_games": len(all_jobs), "recorded_games": len(rows),
        "valid_games": len(valid), "invalid_games": len(rows) - len(valid),
        "baseline_cache_hits": sum(row.get("baseline_cache_hit") is True for row in rows),
        "fresh_baseline_games": sum(row.get("participant") == "baseline" and
                                    row.get("baseline_cache_hit") is False for row in rows),
        "complete_and_valid": complete and len(rows) == len(valid),
        "families": {}, "paired_by_family": {}, "promotion_pool": {},
    }
    for family in sorted({opp["family"] for opp in m["opponents"]}):
        entries = [row for row in valid if row["family"] == family]
        report["families"][family] = {
            participant: record_stats([row for row in entries if row["participant"] == participant])
            for participant in ("candidate", "baseline")
        }
        report["families"][family]["opponents"] = {
            opp["path"]: {
                participant: record_stats([row for row in entries
                                           if row["opponent"] == str(ROOT / opp["path"])
                                           and row["participant"] == participant])
                for participant in ("candidate", "baseline")
            }
            for opp in m["opponents"] if opp["family"] == family
        }
    pairs: dict[tuple[int, str, int], dict[str, dict]] = {}
    for row in valid:
        key = (row["seed"], row["opponent"], row["seat"])
        pairs.setdefault(key, {})[row["participant"]] = row
    paired_by_seed_family: dict[tuple[int, str], list[tuple[float, float]]] = {}
    for (seed, _, _), pair in pairs.items():
        if set(pair) != {"candidate", "baseline"}:
            continue
        c, b = pair["candidate"], pair["baseline"]
        paired_by_seed_family.setdefault((seed, c["family"]), []).append(
            (c["points"] - b["points"], c["delta"] - b["delta"]))
    families = sorted(report["families"])
    for family in families:
        values = [statistics.mean(x[0] for x in paired_by_seed_family[(seed, family)])
                  for seed in m["seeds"] if (seed, family) in paired_by_seed_family]
        margins = [statistics.mean(x[1] for x in paired_by_seed_family[(seed, family)])
                   for seed in m["seeds"] if (seed, family) in paired_by_seed_family]
        report["paired_by_family"][family] = {
            "paired_worlds": len(values), "mean_point_gain": statistics.mean(values) if values else None,
            "mean_margin_gain": statistics.mean(margins) if margins else None,
            "point_gain_world_bootstrap_95": bootstrap_world(values),
        }
    nonself = [family for family in ("frontier", "master", "dsm_proxy")]
    complete_world_values = []
    complete_world_margins = []
    expected_per_family = {family: 2 * sum(opp["family"] == family for opp in m["opponents"])
                           for family in nonself}
    for seed in m["seeds"]:
        if all(len(paired_by_seed_family.get((seed, family), [])) == expected_per_family[family]
               for family in nonself):
            complete_world_values.append(statistics.mean(
                statistics.mean(pair[0] for pair in paired_by_seed_family[(seed, family)])
                for family in nonself))
            complete_world_margins.append(statistics.mean(
                statistics.mean(pair[1] for pair in paired_by_seed_family[(seed, family)])
                for family in nonself))
    report["promotion_pool"] = {
        "families_excluding_self": nonself,
        "diagnostic_families": [family for family in families if family not in nonself and family != "self_v9"],
        "complete_paired_worlds": len(complete_world_values),
        "mean_point_gain": statistics.mean(complete_world_values) if complete_world_values else None,
        "mean_margin_gain": statistics.mean(complete_world_margins) if complete_world_margins else None,
        "point_gain_world_bootstrap_95": bootstrap_world(complete_world_values),
        "note": "The three frozen non-self core families receive equal weight; self-play and optional diagnostic opponents cannot inflate promotion points. Both seats remain one world cluster.",
    }
    if m["split"] == "confirmation":
        report["promotion_gate"] = confirmation_gate(report)
    return report


def get_existing(run_name: str, split: str) -> tuple[dict, list[dict], dict]:
    loc = paths(run_name, split)
    m = json.loads(loc["manifest"].read_text(encoding="utf-8"))
    if m["run_name"] != run_name or m["split"] != split or m["seed_manifest_sha256"] != sha(SEED_PATH):
        raise ValueError("Manifest, run name, split, or seed SHA changed")
    if m["seeds"] != frozen_seeds()[split]:
        raise ValueError("Run seeds differ from frozen split")
    for spec in (m["candidate"], m["baseline"], *m["opponents"]):
        source(spec["path"], spec["sha256"])
    rows = load_ledger(loc["ledger"], m)
    return m, rows, summarize(m, rows)


def freeze_path(run_name: str) -> Path:
    return FROZEN / f"{run_name}.json"


def check_heldout(m: dict, args: argparse.Namespace) -> None:
    split = m["split"]
    if split == "development":
        return
    flag = "unlock_confirmation" if split == "confirmation" else "unlock_reserve"
    if not getattr(args, flag):
        raise ValueError(f"{split} is sealed; pass --{flag.replace('_', '-')} after freezing the candidate")
    frozen = json.loads(freeze_path(m["run_name"]).read_text(encoding="utf-8"))
    if frozen["candidate"] != m["candidate"] or frozen["opponents"] != m["opponents"]:
        raise ValueError("Held-out candidate or opponent roster differs from the frozen development selection")
    if any(frozen[key] != m[key] for key in
           ("arena_sha256", "game_runner_sha256", "engine_version", "episode_steps")):
        raise ValueError("Held-out runner or official engine differs from frozen development")
    development = paths(m["run_name"], "development")
    if (sha(development["manifest"]) != frozen["development_manifest_sha256"]
            or sha(development["ledger"]) != frozen["development_ledger_sha256"]):
        raise ValueError("Frozen development evidence changed")
    if split == "reserve":
        confirmed_manifest, _, confirmed = get_existing(m["run_name"], "confirmation")
        if (confirmed_manifest["candidate"] != m["candidate"]
                or confirmed_manifest["opponents"] != m["opponents"]):
            raise ValueError("Reserve candidate or roster differs from the confirmed candidate")
        if not confirmation_gate(confirmed)["passed"]:
            raise ValueError("Reserve remains sealed until complete, valid, positive confirmation")


def confirmation_gate(report: dict) -> dict:
    """Conservative held-out pass; self-play is a veto, never positive evidence."""
    problems = []
    if not report["complete_and_valid"]:
        problems.append("incomplete_or_invalid_games")
    pool = report["promotion_pool"]
    if pool["complete_paired_worlds"] != COUNTS["confirmation"]:
        problems.append("incomplete_nonself_pairs")
    interval = pool["point_gain_world_bootstrap_95"]
    if interval is None or interval[0] <= 0:
        problems.append("nonself_paired_gain_lower_bound_not_positive")
    for family in pool["families_excluding_self"]:
        gain = report["paired_by_family"][family]["mean_point_gain"]
        if gain is None or gain < -0.05:
            problems.append(f"family_regression_{family}")
    direct = report["families"]["self_v9"]["candidate"]["win_points"]
    if direct is None or direct < 0.5:
        problems.append("loses_to_v9_reference")
    return {"passed": not problems, "reasons": problems,
            "rule": "all games valid; 48 complete paired worlds; frozen non-self core macro 95% world-bootstrap lower bound > 0; each core family gain >= -0.05; direct V9 points >= 0.5"}


def command_run(args: argparse.Namespace) -> None:
    m = manifest(args.candidate, args.extra_opponent, args.split, args.run_name)
    check_heldout(m, args)
    if args.split != "development" and args.count is not None:
        raise ValueError("Held-out splits must run in full; --count is development-only")
    count = args.count if args.count is not None else COUNTS[args.split]
    if not 1 <= count <= COUNTS[args.split]:
        raise ValueError("--count is outside the split")
    loc = paths(args.run_name, args.split)
    if loc["manifest"].exists() and json.loads(loc["manifest"].read_text(encoding="utf-8")) != m:
        raise ValueError("Existing run manifest differs; use a fresh --run-name")
    existing = load_ledger(loc["ledger"], m)
    done = {row["id"] for row in existing}
    pending = [job for job in jobs(m, count) if job["id"] not in done]
    cached, to_run = plan_pending(m, pending)
    print(json.dumps({"run": args.run_name, "split": args.split, "pending": len(pending),
                      "existing": len(existing), "selected_worlds": count,
                      "baseline_cache_hits": len(cached), "game_runs_required": len(to_run),
                      "baseline_cache_misses": sum(job["participant"] == "baseline" for job in to_run)}))
    if args.dry_run:
        return
    RESULTS.mkdir(parents=True, exist_ok=True)
    if not loc["manifest"].exists():
        loc["manifest"].write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    rows = existing[:]
    with loc["ledger"].open("a", encoding="utf-8") as handle:
        for row in cached:
            rows.append(row)
            handle.write(json.dumps(row) + "\n")
            handle.flush()
        if to_run:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(run_checked, job): job for job in to_run}
                for future in as_completed(futures):
                    row = future.result()
                    if m["split"] == "development" and row["participant"] == "baseline" and row.get("valid"):
                        key = write_baseline_cache(futures[future], row)
                        row["baseline_cache_key"] = key
                        row["baseline_cache_hit"] = False
                    rows.append(row)
                    handle.write(json.dumps(row) + "\n")
                    handle.flush()
                    print(json.dumps({key: row.get(key) for key in
                                      ("seed", "seat", "participant", "family", "delta", "valid")} ), flush=True)
    report = summarize(m, rows)
    loc["report"].write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_and_valid": report["complete_and_valid"],
                      "promotion_pool": report["promotion_pool"]}))


def command_freeze(args: argparse.Namespace) -> None:
    m, rows, report = get_existing(args.run_name, "development")
    if m["arena_sha256"] != sha(Path(__file__)) or m["game_runner_sha256"] != sha(GAME_RUNNER):
        raise ValueError("Arena runner changed after development; rerun under a new name")
    if not report["complete_and_valid"] or len(rows) != len(jobs(m)):
        raise ValueError("Complete and valid development league required before freeze")
    pool = report["promotion_pool"]
    if pool["complete_paired_worlds"] != COUNTS["development"] or pool["mean_point_gain"] <= 0:
        raise ValueError("Candidate needs positive non-self paired development gain")
    self_points = report["families"]["self_v9"]["candidate"]["win_points"]
    if self_points is None or self_points < 0.5:
        raise ValueError("Candidate loses to the frozen V9 reference")
    loc = paths(args.run_name, "development")
    item = {
        "schema": "kaggriculture-arena-r11-freeze-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "run_name": args.run_name,
        "candidate": m["candidate"], "opponents": m["opponents"],
        "arena_sha256": m["arena_sha256"], "game_runner_sha256": m["game_runner_sha256"],
        "engine_version": m["engine_version"], "episode_steps": m["episode_steps"],
        "development_manifest_sha256": sha(loc["manifest"]),
        "development_ledger_sha256": sha(loc["ledger"]),
        "development_nonself_point_gain": pool["mean_point_gain"],
        "development_v9_direct_points": self_points,
    }
    target = freeze_path(args.run_name)
    if target.exists():
        raise ValueError("A candidate is already frozen under this run name")
    FROZEN.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"frozen": str(target), "candidate_sha256": m["candidate"]["sha256"]}))


def command_smoke() -> None:
    seeds = frozen_seeds()
    separation = check_seed_separation(seeds)
    m = manifest(CORE[0][1], [], "development", "arena-smoke")
    assert len(jobs(m)) == 24 * len(CORE) * 2 * 2
    assert len({job["id"] for job in jobs(m)}) == len(jobs(m))
    heldout = manifest(CORE[0][1], [], "confirmation", "arena-smoke")
    try:
        check_heldout(heldout, argparse.Namespace(unlock_confirmation=False, unlock_reserve=False))
    except ValueError as exc:
        assert "sealed" in str(exc)
    else:
        raise AssertionError("Confirmation was accidentally unlocked")
    assert {opp["family"] for opp in m["opponents"]} == {x[0] for x in CORE}
    first_world_jobs = jobs(m, 1)
    baseline_job = next(job for job in first_world_jobs if job["participant"] == "baseline")
    synthetic = {**baseline_job, "valid": True, "invalid_reasons": [],
                 "environment_version": ENGINE_VERSION, "states": 720,
                 "statuses": ["DONE", "DONE"], "money": 100, "opponent_money": 100,
                 "delta": 0, "points": .5, "stderr": [],
                 "telemetry": [{"nonzero": {}}, {"nonzero": {}}], "shops": []}
    with tempfile.TemporaryDirectory(prefix="arena-r11-cache-smoke-") as temporary:
        cache_dir = Path(temporary)
        key = write_baseline_cache(baseline_job, synthetic, cache_dir)
        cached, to_run = plan_pending(m, first_world_jobs, cache_dir)
        assert len(cached) == 1 and len(to_run) == 15
        alternate = manifest(CORE[1][1], [], "development", "arena-smoke-alt")
        alternate_cached, alternate_to_run = plan_pending(alternate, jobs(alternate, 1), cache_dir)
        assert len(alternate_cached) == 1 and len(alternate_to_run) == 15
        target = cache_dir / f"{key}.json"
        payload = json.loads(target.read_text(encoding="utf-8"))
        payload["row"]["delta"] = 1
        payload["row_sha256"] = hashlib.sha256(canonical_json(payload["row"])).hexdigest()
        target.write_bytes(canonical_json(payload) + b"\n")
        try:
            plan_pending(m, first_world_jobs, cache_dir)
        except ValueError as exc:
            assert "Malformed baseline cache" in str(exc)
        else:
            raise AssertionError("Corrupted baseline cache was accepted")
    print(json.dumps({**separation, "development_jobs": len(jobs(m)),
                      "heldout_locked_by_default": True, "synthetic_cache_hits": 1,
                      "synthetic_game_runs_required": 15, "cross_candidate_cache_hit": True,
                      "malformed_cache_rejected": True, "agent_games_run": 0}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Create only the immutable prospective seed manifest")
    sub.add_parser("smoke", help="Check seeds and manifest without running any games")
    run = sub.add_parser("run", help="Run official 720-step paired-seat games")
    run.add_argument("--candidate", required=True)
    run.add_argument("--run-name", required=True)
    run.add_argument("--extra-opponent", action="append", default=[], metavar="FAMILY=PATH")
    run.add_argument("--split", choices=tuple(COUNTS), default="development")
    run.add_argument("--count", type=int, help="Use first N development worlds, then resume to 24")
    run.add_argument("--workers", type=int, default=3)
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--unlock-confirmation", action="store_true")
    run.add_argument("--unlock-reserve", action="store_true")
    freeze = sub.add_parser("freeze", help="Freeze one fully tested development candidate")
    freeze.add_argument("--run-name", required=True)
    report = sub.add_parser("report", help="Validate and print an existing report")
    report.add_argument("--run-name", required=True)
    report.add_argument("--split", choices=tuple(COUNTS), default="development")
    args = parser.parse_args()
    if args.command == "init":
        seeds = frozen_seeds(create=True)
        print(json.dumps({"seed_manifest": str(SEED_PATH), "sha256": sha(SEED_PATH),
                          **check_seed_separation(seeds)}))
    elif args.command == "smoke":
        command_smoke()
    elif args.command == "run":
        if args.workers < 1:
            raise ValueError("--workers must be positive")
        command_run(args)
    elif args.command == "freeze":
        command_freeze(args)
    else:
        m, rows, result = get_existing(args.run_name, args.split)
        paths(args.run_name, args.split)["report"].write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result))


if __name__ == "__main__":
    main()
