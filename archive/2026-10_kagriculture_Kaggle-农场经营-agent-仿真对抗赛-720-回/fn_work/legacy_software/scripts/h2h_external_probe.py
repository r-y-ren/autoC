"""Generate formal external black-box H2H evidence.

This harness is development-only.  Its output is ineligible for promotion and
is never holdout evidence.  External opponent bytes remain isolated under
kaggle_simulations/opponents and never enter the submission path.

Example:
    python workspace/kaggriculture/software/scripts/h2h_external_probe.py \
      --out workspace/kaggriculture/software/exports/external/v48-smoke.json \
      --opponents v48 --seeds 101
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
REPO_ROOT = SOFTWARE_ROOT
while REPO_ROOT != REPO_ROOT.parent and not (REPO_ROOT / ".git").exists():
    REPO_ROOT = REPO_ROOT.parent
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv import official_engine_version  # noqa: E402
from kgenv.arena import AbnormalMatchError, load_submission_agent, run_match  # noqa: E402
from kgenv.engine import FULL_EPISODE_STEPS  # noqa: E402
from kgenv.eval_contract import ContractError, atomic_publish_json, canonical_sha256, file_sha256  # noqa: E402
from kgenv.external_h2h_contract import (  # noqa: E402
    canonical_external_digest,
    schema_validate_external,
    summarize_external_games,
    validate_external_h2h,
    _canonical_paths,
    RUNTIME_CLOSURE_KEYS,
    RUNTIME_ENGINE_MEMBERS,
)

_CANONICAL = _canonical_paths(REPO_ROOT)
_RUNTIME_CLOSURE_KEYS = RUNTIME_CLOSURE_KEYS

OPPONENTS_DIR = SOFTWARE_ROOT / "kaggle_simulations" / "opponents"
SUBMISSION_MAIN = SOFTWARE_ROOT / "kaggle_simulations" / "agent" / "main.py"
ACTIVE_CANDIDATE = SOFTWARE_ROOT / "active_candidate.json"
WHEEL_PATH = SOFTWARE_ROOT / "vendor" / "kaggle_environments-1.32.7+nodeps-py3-none-any.whl"
SCHEMA_PATH = SOFTWARE_ROOT / "exports" / "external_h2h_schema.json"
DEV_SEEDS = [101, 102, 103, 104]
REG_SEEDS = [201, 202, 203, 204]

OPPONENT_METADATA = {
    "v48": {
        "filename": "v48_main.py",
        "provenance": {
            "author": "kaitofukami",
            "source": "40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes Kaggle notebook snapshot",
            "source_url": "https://www.kaggle.com/",
            "acquired_at": "2026-08-31",
        },
        "license": {"status": "no-explicit-reuse-license", "spdx": None},
        "use_restriction": "read-only black-box stress opponent; not-for-submission",
    },
    "v72": {
        "filename": "v72_main.py",
        "provenance": {
            "author": "autoC team",
            "source": "historical v7.2 online champion snapshot from repository commit fdd5b87",
            "source_url": "https://github.com/",
            "acquired_at": "2026-08-31",
        },
        "license": {"status": "internal-historical-snapshot", "spdx": None},
        "use_restriction": "evaluation-only historical anchor; not copied into current submission",
    },
}


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _active_identity(candidate_path: Path) -> dict:
    active = json.loads(ACTIVE_CANDIDATE.read_text(encoding="utf-8"))
    resolved = candidate_path.resolve()
    for role, key in (("working", "working"), ("frozen", "last_promoted_frozen")):
        entry = active.get(key, {})
        raw_path = entry.get("path") or entry.get("snapshot_path")
        if raw_path and (SOFTWARE_ROOT / raw_path).resolve() == resolved:
            return {"id": role, "path": _rel(resolved), "sha256": file_sha256(resolved),
                    "role": role, "status": entry["status"],
                    "active_candidate_contract": _rel(ACTIVE_CANDIDATE)}
        if role == "working" and entry.get("sha256") == file_sha256(resolved):
            return {"id": role, "path": _rel(resolved), "sha256": entry["sha256"],
                    "role": role, "status": entry["status"],
                    "active_candidate_contract": _rel(ACTIVE_CANDIDATE)}
    raise ContractError("candidate does not match working/frozen active_candidate contract")


def _provenance_entry(opponent_id: str, sha256: str) -> dict:
    text = (OPPONENTS_DIR / "PROVENANCE.md").read_text(encoding="utf-8")
    heading = re.search(rf"^##\s+{re.escape(opponent_id)}_main\.py\s*$", text, re.MULTILINE)
    if not heading:
        raise ContractError(f"provenance has no entry for opponent {opponent_id}")
    section = text[heading.end():].split("\n## ", 1)[0]
    def field(label: str) -> str:
        match = re.search(rf"^-\s+{label}:\s*(.+?)\s*$", section, re.MULTILINE)
        if not match:
            raise ContractError(f"provenance missing {label} for opponent {opponent_id}")
        return match.group(1)
    actual_sha = field("SHA-256").split("（", 1)[0].strip()
    if actual_sha != sha256:
        raise ContractError(f"provenance SHA mismatch for opponent {opponent_id}")
    return {"author": field("Author"), "source": field("Source"),
            "source_url": field("Source URL"), "acquired_at": field("Acquired at"),
            "use_restriction": field("Use restriction")}


def _opponent_identity(opponent_id: str) -> dict:
    try:
        metadata = OPPONENT_METADATA[opponent_id]
    except KeyError as exc:
        raise ContractError(f"unknown external opponent {opponent_id!r}") from exc
    path = OPPONENTS_DIR / metadata["filename"]
    sha256 = file_sha256(path)
    provenance = _provenance_entry(opponent_id, sha256)
    return {"id": opponent_id, "path": _rel(path), "sha256": sha256,
            "provenance": {key: provenance[key] for key in ("author", "source", "source_url", "acquired_at")},
            "license": metadata["license"], "use_restriction": provenance["use_restriction"]}


def _closure(candidate: dict, opponents: list[dict]) -> dict:
    paths = [candidate["path"], *(row["path"] for row in opponents)]
    paths.extend(_rel(_CANONICAL[key]) for key in _RUNTIME_CLOSURE_KEYS if key != "candidate")
    files = {path: file_sha256(REPO_ROOT / path if not Path(path).is_absolute() else path)
             for path in sorted(set(paths))}
    return {"files": files, "sha256": canonical_sha256(files)}


def _external_activity(activity: dict) -> dict:
    """Normalize engine diagnostics into the externally auditable shape."""
    policy = activity.get("policy", {})
    seats = []
    for seat in activity.get("seats", []):
        reasons = list(seat.get("failure_reasons", []))
        evidence_values = {"action_count": int(activity.get("decisions", 0)),
                           "non_pass_action_count": int(seat.get("non_pass_decisions", 0)),
                           "state_change_count": int(seat.get("effective_state_changes", 0)),
                           "state_count": int(activity.get("states", 0)),
                           "reward_delta": float(seat.get("reward_delta", 0.0)),
                           "non_pass_trace": list(seat.get("non_pass_trace", [])),
                           "state_change_trace": list(seat.get("state_change_trace", []))}
        seats.append({
            "decisions": int(activity.get("decisions", 0)),
            "non_pass_decisions": int(seat.get("non_pass_decisions", 0)),
            "effective_commands": int(seat.get("effective_state_changes", 0)),
            "max_pass_streak": int(seat.get("longest_pass_streak", 0)),
            "non_pass_trace": list(seat.get("non_pass_trace", [])),
            "state_change_trace": list(seat.get("state_change_trace", [])),
            "reward_delta": float(seat.get("reward_delta", 0.0)),
            "pass_only": bool(seat.get("pass_only", False)),
            "reasons": reasons,
            "policy": dict(policy),
            "evidence": {**evidence_values,
                         "evidence_digest": canonical_sha256(evidence_values)},
        })
    return {"states": int(activity.get("states", 0)),
            "decisions": int(activity.get("decisions", 0)),
            "starting_money": float(activity.get("starting_money", 3000.0)),
            "completion_ok": bool(activity.get("completion_ok", False)),
            "activity_ok": bool(activity.get("activity_ok", False)),
            "ok": bool(activity.get("ok", False)),
            "contract_status": "producer_attested", "independently_recomputed": False,
            "seats": seats}


def _export_game(result: dict, item: dict, candidate_id: str, opponent_id: str,
                 elapsed: float) -> dict:
    players = result["players"]
    candidate_seat = players.index(candidate_id)
    return {
        "game_id": f"{candidate_id}--{opponent_id}--{item['seed']}--{item['seat']}",
        "opponent_id": opponent_id, "seed": item["seed"], "seat": item["seat"],
        "players": players, "candidate_seat": candidate_seat,
        "statuses": result["statuses"], "contract_ok": result["contract_ok"],
        "rewards": [float(value) for value in result["rewards"]],
        "winner": result["winner_label"],
        "margin": float(result["rewards"][candidate_seat] - result["rewards"][1 - candidate_seat]),
        "episode_steps": result["episode_steps"], "states": result["turns_played"],
        "completion_ok": result["activity"]["completion_ok"], "activity": _external_activity(result["activity"]),
        "abnormal_reason": None, "elapsed_seconds": round(elapsed, 3),
    }


def play(candidate: dict, opponents: list[dict], seeds: list[int]) -> list[dict]:
    candidate_agent = load_submission_agent(str(REPO_ROOT / candidate["path"]))
    games = []
    for opponent in opponents:
        opponent_agent = load_submission_agent(str(REPO_ROOT / opponent["path"]))
        for seed in seeds:
            for seat in ("AB", "BA"):
                started = time.perf_counter()
                if seat == "AB":
                    result = run_match(candidate_agent, opponent_agent, seed,
                                       label_a=candidate["id"], label_b=opponent["id"])
                else:
                    result = run_match(opponent_agent, candidate_agent, seed,
                                       label_a=opponent["id"], label_b=candidate["id"])
                games.append(_export_game(result, {"seed": seed, "seat": seat},
                                          candidate["id"], opponent["id"],
                                          time.perf_counter() - started))
                print(f"[{len(games)}] {opponent['id']} seed={seed} seat={seat} "
                      f"winner={result['winner_label']}", flush=True)
    return games


def _runtime_engine_attestation() -> dict:
    import kaggle_environments

    package_root = Path(kaggle_environments.__file__).resolve().parent
    members = RUNTIME_ENGINE_MEMBERS
    with zipfile.ZipFile(WHEEL_PATH) as archive:
        files = {}
        for member in members:
            runtime_sha = hashlib.sha256((package_root / member).read_bytes()).hexdigest()
            wheel_sha = hashlib.sha256(
                archive.read(f"kaggle_environments/{member}")).hexdigest()
            if runtime_sha != wheel_sha:
                raise ContractError(f"runtime engine source differs from vendored wheel: {member}")
            files[member] = runtime_sha
    return {"package_root": str(package_root), "files": files,
            "matches_vendored_wheel": True}


def build_payload(candidate_path: Path, opponent_ids: list[str], seeds: list[int],
                  seed_domain: str, argv: list[str], output_path: Path | None = None) -> dict:
    if not seeds or len(set(seeds)) != len(seeds):
        raise ContractError("external seeds must be non-empty and unique")
    if seed_domain.lower() == "holdout":
        raise ContractError("external H2H cannot use the holdout seed domain")
    candidate = _active_identity(candidate_path)
    opponents = [_opponent_identity(name) for name in opponent_ids]
    before = _closure(candidate, opponents)
    if output_path is not None:
        _reject_output_alias(output_path, candidate, opponents, before)
    games = play(candidate, opponents, seeds)
    after = _closure(candidate, opponents)
    if before != after:
        raise ContractError("external H2H input closure changed during run")
    payload = {
        "schema_version": "external-h2h/2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_scope": {
            "kind": "external_black_box_stress", "development_only": True,
            "formal_promotion_eligible": False, "holdout_evidence": False,
            "limitations": ["external opponents are distribution-stress evidence only",
                            "not a promotion gate or holdout generalization claim"],
        },
        "engine": {"name": "kaggle-environments", "version": official_engine_version(),
                   "scenario": "kaggriculture", "wheel_path": _rel(WHEEL_PATH),
                   "wheel_sha256": file_sha256(WHEEL_PATH),
                   "runtime_attestation": _runtime_engine_attestation()},
        "candidate": candidate, "opponents": opponents,
        "seed_domain": {"name": seed_domain, "seeds": seeds, "holdout": False},
        "schedule": {"policy": "paired_ab_ba", "seat_orders": ["AB", "BA"],
                     "opponent_ids": opponent_ids, "expected_games": len(opponents) * len(seeds) * 2},
        "games": games, "summary": summarize_external_games(games, candidate["id"]),
        "input_closure": {"algorithm": "sha256-path-map-v1", "before": before,
                          "after": after, "unchanged": True},
        "command": {"argv": argv, "cwd": str(REPO_ROOT),
                    "parameters": {"candidate": candidate["path"], "opponents": opponent_ids,
                                   "seeds": seeds, "seed_domain": seed_domain}},
        "digests": {"algorithm": "canonical-json-sha256", "canonical_payload_sha256": ""},
    }
    payload["digests"]["canonical_payload_sha256"] = canonical_external_digest(payload)
    return payload


def _reject_repository_output(output: Path) -> None:
    target = output.resolve()
    external_root = (SOFTWARE_ROOT / "exports" / "external").resolve()
    try:
        inside_repo = target.is_relative_to(REPO_ROOT.resolve())
        inside_external = target.is_relative_to(external_root)
    except AttributeError:
        inside_repo = str(target).startswith(str(REPO_ROOT.resolve()) + os.sep)
        inside_external = str(target).startswith(str(external_root) + os.sep)
    if inside_repo and not inside_external:
        raise ContractError("repository output must stay under the campaign software exports/external directory")


def _reject_output_alias(output: Path, candidate: dict, opponents: list[dict], closure: dict) -> None:
    _reject_repository_output(output)
    target = output.resolve()
    source_paths = [candidate["path"], *(row["path"] for row in opponents)]
    source_paths.extend(closure.get("files", {}))
    for raw_path in source_paths:
        source = Path(raw_path)
        resolved_source = source.resolve() if source.is_absolute() else (REPO_ROOT / source).resolve()
        if target == resolved_source:
            raise ContractError("output target must not resolve to an external H2H input or canonical source")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", default=",".join(str(seed) for seed in DEV_SEEDS + REG_SEEDS))
    parser.add_argument("--seed-domain", default="external-development-v1")
    parser.add_argument("--opponents", default="v48", help="comma-separated: v48,v72")
    parser.add_argument("--candidate", type=Path, default=SUBMISSION_MAIN)
    parser.add_argument("--candidates", default=None,
                        help="legacy alias; exactly one candidate path is accepted")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    candidate = args.candidate
    if args.candidates:
        values = [value.strip() for value in args.candidates.split(",") if value.strip()]
        if len(values) != 1:
            print("formal external artifacts require exactly one candidate", file=sys.stderr)
            return 2
        candidate = Path(values[0])
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve()
    opponent_ids = [value.strip() for value in args.opponents.split(",") if value.strip()]
    try:
        seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]
        target = args.out if args.out.is_absolute() else REPO_ROOT / args.out
        payload = build_payload(candidate, opponent_ids, seeds, args.seed_domain,
                                ["python", _rel(Path(__file__)), *raw_argv], target)
        schema_validate_external(payload, SCHEMA_PATH)
        atomic_publish_json(target, payload,
                            lambda value: validate_external_h2h(value, software_root=REPO_ROOT))
    except (OSError, ValueError, ContractError, AbnormalMatchError) as exc:
        print(f"external H2H failed; no evidence published: {exc}", file=sys.stderr)
        return 1
    print(f"wrote validated external evidence {target} "
          f"sha256={file_sha256(target)} canonical={payload['digests']['canonical_payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
