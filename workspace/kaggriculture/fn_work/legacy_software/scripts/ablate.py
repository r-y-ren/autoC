"""Paired ablation harness (campaign III r3-P0, layered build merge gate).

Runs a candidate against the champion on the SAME (opponent, seed, seat)
cells of the fixed evaluation grid.  The engine is deterministic for a given
(agent, agent, seed) triple and every opponent in the pool is a
deterministic local bot, so any difference between the candidate's game and
the champion's game in the same cell is attributable to the candidate alone
-- a paired design with the seed and seat as own controls.

Merge gate (three indicators, all relative to the champion):
  1. new-style pool win rate -- combined (W + 0.5T)/n over the five
     online-style opponents (crop_rotator, template_wheat, self_feed_ranch,
     near_band_diversified, scale_ranch); candidate must be >= champion.
  2. worst single-style win rate -- the minimum per-opponent win rate over
     every opponent in the pool (conservative: protects the non-style gate
     bots too); candidate must be >= champion.
  3. disaster loss rate -- share of games lost by more than DISASTER_MARGIN
     (margin < -15000); candidate must be <= champion.
A layer is mergeable only when all three hold.  champion-vs-champion
therefore always judges mergeable (every cell ties exactly).

The champion defaults to the frozen snapshot (r3_frozen_candidate.b64,
sha-checked against r3_frozen_manifest.json and decoded to a temp file);
the candidate is loaded from a working path.  Outputs go ONLY to
exports/ablations/<label>.json -- never to a formal export.

Usage:
    python scripts/ablate.py --candidate <path> [--champion <path|frozen>]
        [--seeds 101-104] [--pool required|name1,name2,...]
        [--out exports/ablations/<label>.json] [--label NAME]

Example (champion-vs-champion semantic smoke -- must end MERGEABLE with
every pair a tie):
    python scripts/ablate.py --candidate frozen --label champ-vs-champ
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import load_submission_agent, run_match  # noqa: E402
from kgenv.bots.baseline import baseline_wheat_agent  # noqa: E402
from kgenv.bots.cow_baron import cow_baron_agent  # noqa: E402
from kgenv.bots.expansionist import expansionist_agent  # noqa: E402
from kgenv.bots.melon_hoarder import melon_hoarder_agent  # noqa: E402
from kgenv.bots.online_pool import (  # noqa: E402
    crop_rotator_agent,
    near_band_diversified_agent,
    scale_ranch_agent,
    self_feed_ranch_agent,
    template_wheat_agent,
    wheat_straw_monster_agent,
    two_quad_denser_agent,
)
from kgenv.engine import FULL_EPISODE_STEPS  # noqa: E402
from kgenv.eval_contract import (  # noqa: E402
    ContractError,
    bytes_sha256,
    file_sha256,
    validate_seed_domain,
)

FROZEN_SNAPSHOT = os.path.join(SOFTWARE_ROOT, "r3_frozen_candidate.b64")
FROZEN_MANIFEST = os.path.join(SOFTWARE_ROOT, "r3_frozen_manifest.json")
ABLATIONS_DIR = os.path.join(SOFTWARE_ROOT, "exports", "ablations")

GATE_OPPONENTS = ["cow_baron", "melon_hoarder"]
GUARD_OPPONENTS = ["expansionist", "baseline_wheat"]
NEW_STYLE_POOL = [
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
]
# v7: wheat_straw_monster rides as a guard opponent (it is a calibrated
# archetype, not one of the five new-style pool members behind indicator 1)
REQUIRED_OPPONENTS = GATE_OPPONENTS + GUARD_OPPONENTS + NEW_STYLE_POOL + [
    "wheat_straw_monster",
    "two_quad_denser",
]
OPPONENTS = {
    "cow_baron": cow_baron_agent,
    "melon_hoarder": melon_hoarder_agent,
    "expansionist": expansionist_agent,
    "baseline_wheat": baseline_wheat_agent,
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "near_band_diversified": near_band_diversified_agent,
    "scale_ranch": scale_ranch_agent,
    "wheat_straw_monster": wheat_straw_monster_agent,
    "two_quad_denser": two_quad_denser_agent,
}
DISASTER_MARGIN = -15000
SCHEMA_VERSION = "1.0"


# --------------------------------------------------------------------------- #
# champion loading
# --------------------------------------------------------------------------- #
def decode_frozen_champion(snapshot_path: str = FROZEN_SNAPSHOT,
                           manifest_path: str = FROZEN_MANIFEST) -> tuple[str, str]:
    """Decode the frozen b64 snapshot to a temp file, sha-verified.

    Returns (temp_path, sha256).  The caller keeps the temp file alive for
    the whole run (module-level temp registry in main()).
    """
    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    expected = manifest["frozen_snapshot"]["decoded_sha256"]
    data = base64.b64decode(Path(snapshot_path).read_bytes())
    actual = bytes_sha256(data)
    if actual != expected:
        raise ContractError(
            f"frozen snapshot sha mismatch: {actual} != {expected}")
    handle = tempfile.NamedTemporaryFile(
        "wb", suffix="_champion_main.py", prefix="ablate_", delete=False)
    handle.write(data)
    handle.close()
    return handle.name, actual


def resolve_champion(spec: str) -> tuple[str, str, str]:
    """--champion 'frozen' (default) or a filesystem path.

    Returns (path, sha256, source_label).  For 'frozen' the temp file is
    tracked so it can be cleaned up at exit.
    """
    if spec == "frozen":
        path, sha = decode_frozen_champion()
        _TEMP_FILES.append(path)
        return path, sha, "r3_frozen_candidate.b64"
    path = os.path.abspath(spec)
    if not os.path.isfile(path):
        raise ContractError(f"champion file not found: {path}")
    return path, file_sha256(path), os.path.basename(path)


_TEMP_FILES: list[str] = []


def resolve_candidate(spec: str) -> tuple[str, str, str]:
    """--candidate path, or 'frozen' (champion-vs-champion smoke)."""
    if spec == "frozen":
        return resolve_champion("frozen")
    path = os.path.abspath(spec)
    if not os.path.isfile(path):
        raise ContractError(f"candidate file not found: {path}")
    return path, file_sha256(path), os.path.basename(path)


# --------------------------------------------------------------------------- #
# grid & pairing
# --------------------------------------------------------------------------- #
def parse_seeds(spec: str) -> list[int]:
    """'101-104' or '101,102' or '101' -> validated seed list."""
    seeds: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            seeds.extend(range(int(lo), int(hi) + 1))
        else:
            seeds.append(int(part))
    if not seeds:
        raise ContractError("empty seed list")
    if len(set(seeds)) != len(seeds):
        raise ContractError("duplicate seeds")
    try:
        validate_seed_domain(seeds, "development")
        return seeds
    except ContractError:
        pass
    try:
        validate_seed_domain(seeds, "regression")
        return seeds
    except ContractError as exc:
        raise ContractError(
            f"seeds must sit inside the development (101-104) or regression "
            f"(201-208) domain: {exc}") from exc


def parse_pool(spec: str) -> tuple[list[str], bool]:
    """--pool 'required' (default, 9 opponents) or a comma list."""
    if spec == "required":
        return list(REQUIRED_OPPONENTS), True
    names = [n.strip() for n in spec.split(",") if n.strip()]
    unknown = [n for n in names if n not in OPPONENTS]
    if unknown:
        raise ContractError(f"unknown opponents: {unknown}")
    if not names:
        raise ContractError("empty opponent pool")
    return names, False


def build_ablation_grid(opponents: list[str], seeds: list[int]) -> list[dict]:
    """Every (opponent, seed, seat) cell; each cell is played by BOTH sides."""
    grid = []
    for opponent in opponents:
        for seed in seeds:
            for seat in ("AB", "BA"):
                grid.append({"opponent": opponent, "seed": seed, "seat": seat})
    return grid


def validate_grid_completeness(games: list[dict], opponents: list[str],
                               seeds: list[int]) -> None:
    """Fail-closed: exactly one cand game and one champion game per cell."""
    expected = {(opp, seed, seat)
                for opp in opponents for seed in seeds
                for seat in ("AB", "BA")}
    seen: dict[tuple, set] = {}
    for game in games:
        key = (game["opponent"], game["seed"], game["seat"])
        side = game["side"]
        if key not in expected:
            raise ContractError(f"game outside the grid: {key}")
        bucket = seen.setdefault(key, set())
        if side in bucket:
            raise ContractError(f"duplicate {side} game in cell {key}")
        bucket.add(side)
    missing = sorted(k for k, b in seen.items() if b != {"cand", "champion"})
    absent = sorted(expected - set(seen))
    if missing:
        raise ContractError(f"incomplete cells: {missing[:5]}")
    if absent:
        raise ContractError(f"missing cells: {absent[:5]}")


def game_record(result: dict, side: str, opponent: str, seed: int,
                seat: str) -> dict:
    side_label = side if side != "champion" else "champ"
    side_index = result["players"].index(side_label)
    margin = result["rewards"][side_index] - result["rewards"][1 - side_index]
    return {
        "side": side,
        "opponent": opponent,
        "seed": seed,
        "seat": seat,
        "players": list(result["players"]),
        "rewards": list(result["rewards"]),
        "statuses": list(result["statuses"]),
        "turns": result["turns_played"],
        "margin": round(float(margin), 1),
        "outcome": "W" if margin > 0 else ("L" if margin < 0 else "T"),
        "contract_ok": result["contract_ok"],
    }


def run_ablation(candidate, champion, opponents: dict, seeds: list[int],
                 episode_steps: int = FULL_EPISODE_STEPS,
                 log=print) -> list[dict]:
    """Play both sides of every (opponent, seed, seat) cell."""
    games = []
    for cell in build_ablation_grid(list(opponents), seeds):
        opponent = opponents[cell["opponent"]]
        for side, agent in (("cand", candidate), ("champion", champion)):
            side_label = side if side != "champion" else "champ"
            if cell["seat"] == "AB":
                result = run_match(agent, opponent, seed=cell["seed"],
                                   label_a=side_label,
                                   label_b=cell["opponent"],
                                   episode_steps=episode_steps,
                                   collect_daily=False)
            else:
                result = run_match(opponent, agent, seed=cell["seed"],
                                   label_a=cell["opponent"],
                                   label_b=side_label,
                                   episode_steps=episode_steps,
                                   collect_daily=False)
            games.append(game_record(result, side, cell["opponent"],
                                     cell["seed"], cell["seat"]))
            log(f"[{len(games):03d}] {side:<8} vs {cell['opponent']:<20} "
                f"seed={cell['seed']} seat={cell['seat']} "
                f"margin={games[-1]['margin']}")
    return games


def pair_cells(games: list[dict]) -> list[dict]:
    """Pair cand/champion games per cell; determinism -> diff = strategy."""
    cells: dict[tuple, dict] = {}
    for game in games:
        key = (game["opponent"], game["seed"], game["seat"])
        cells.setdefault(key, {})[game["side"]] = game
    pairs = []
    for key in sorted(cells, key=lambda k: (k[0], k[1], k[2])):
        cand, champ = cells[key]["cand"], cells[key]["champion"]
        diff = round(cand["margin"] - champ["margin"], 1)
        pairs.append({
            "opponent": key[0], "seed": key[1], "seat": key[2],
            "cand_margin": cand["margin"], "champ_margin": champ["margin"],
            "pair_diff": diff,
            "outcome": "W" if diff > 0 else ("L" if diff < 0 else "T"),
        })
    return pairs


# --------------------------------------------------------------------------- #
# merge gate
# --------------------------------------------------------------------------- #
def _win_rate(games: list[dict]) -> float | None:
    if not games:
        return None
    score = sum(1.0 if g["outcome"] == "W" else 0.5 if g["outcome"] == "T"
                else 0.0 for g in games)
    return round(score / len(games), 4)


def side_gate_metrics(games: list[dict], side: str,
                      opponents: list[str]) -> dict:
    """Three merge-gate indicators for one side over its games."""
    mine = [g for g in games if g["side"] == side]
    if not mine:
        raise ContractError(f"no games for side {side}")
    per_opponent = {}
    for name in opponents:
        sel = [g for g in mine if g["opponent"] == name]
        per_opponent[name] = {
            "games": len(sel),
            "W": sum(1 for g in sel if g["outcome"] == "W"),
            "L": sum(1 for g in sel if g["outcome"] == "L"),
            "T": sum(1 for g in sel if g["outcome"] == "T"),
            "win_rate": _win_rate(sel),
            "avg_margin": round(sum(g["margin"] for g in sel) / len(sel), 1)
            if sel else None,
            "worst_margin": min((g["margin"] for g in sel), default=None),
        }
    style_games = [g for g in mine if g["opponent"] in NEW_STYLE_POOL]
    rates = [row["win_rate"] for row in per_opponent.values()
             if row["win_rate"] is not None]
    disasters = [g for g in mine if g["margin"] < DISASTER_MARGIN]
    return {
        "games": len(mine),
        "record": {
            "W": sum(1 for g in mine if g["outcome"] == "W"),
            "L": sum(1 for g in mine if g["outcome"] == "L"),
            "T": sum(1 for g in mine if g["outcome"] == "T"),
        },
        "new_style_pool_win_rate": _win_rate(style_games),
        "new_style_pool_games": len(style_games),
        "worst_opponent_win_rate": min(rates) if rates else None,
        "worst_opponent": min(per_opponent,
                              key=lambda n: per_opponent[n]["win_rate"]
                              if per_opponent[n]["win_rate"] is not None
                              else 2.0) if rates else None,
        "disaster_rate": round(len(disasters) / len(mine), 4),
        "disaster_games": len(disasters),
        "disaster_threshold": DISASTER_MARGIN,
        "per_opponent": per_opponent,
    }


def merge_verdict(cand_gate: dict, champ_gate: dict) -> dict:
    """Mergeable iff pool >= , worst >= , disaster <= (all vs champion)."""
    checks = {
        "new_style_pool_win_rate":
            cand_gate["new_style_pool_win_rate"]
            >= champ_gate["new_style_pool_win_rate"],
        "worst_opponent_win_rate":
            cand_gate["worst_opponent_win_rate"]
            >= champ_gate["worst_opponent_win_rate"],
        "disaster_rate":
            cand_gate["disaster_rate"] <= champ_gate["disaster_rate"],
    }
    return {
        "mergeable": all(checks.values()),
        "checks": checks,
        "rule": "candidate merges only if new-style pool WR >= champion, "
                "worst single-opponent WR >= champion, and disaster loss "
                f"rate (margin < {DISASTER_MARGIN}) <= champion",
    }


# --------------------------------------------------------------------------- #
# output plumbing
# --------------------------------------------------------------------------- #
def resolve_out_path(requested: str, label: str) -> Path:
    """Ablation products live ONLY under exports/ablations/."""
    base = Path(ABLATIONS_DIR).resolve()
    if requested:
        candidate = Path(requested)
        target = candidate if candidate.is_absolute() else base / candidate
    else:
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in label)
        target = base / f"{safe or 'ablation'}.json"
    target = target.resolve()
    if base not in target.parents:
        raise ContractError(
            f"ablation output must stay inside exports/ablations/: {target}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Paired candidate-vs-champion ablation with merge gate")
    parser.add_argument("--candidate", required=True,
                        help="path to the candidate main.py (or 'frozen')")
    parser.add_argument("--champion", default="frozen",
                        help="'frozen' (r3 snapshot, default) or a main.py path")
    parser.add_argument("--seeds", default="101-104",
                        help="seed range/list, e.g. 101-104 (default)")
    parser.add_argument("--pool", default="required",
                        help="'required' (9 fixed opponents, default) or a "
                             "comma list (exploratory subset)")
    parser.add_argument("--out", default="",
                        help="output path under exports/ablations/ "
                             "(default exports/ablations/<label>.json)")
    parser.add_argument("--label", default="ablation")
    parser.add_argument("--episode-steps", type=int,
                        default=FULL_EPISODE_STEPS)
    args = parser.parse_args()

    try:
        seeds = parse_seeds(args.seeds)
        opponents, formal = parse_pool(args.pool)
        cand_path, cand_sha, cand_label = resolve_candidate(args.candidate)
        champ_path, champ_sha, champ_label = resolve_champion(args.champion)
        candidate = load_submission_agent(cand_path)
        champion = load_submission_agent(champ_path)
        started = time.perf_counter()
        games = run_ablation(candidate, champion,
                             {name: OPPONENTS[name] for name in opponents},
                             seeds, episode_steps=args.episode_steps)
        validate_grid_completeness(games, opponents, seeds)
        pairs = pair_cells(games)
        cand_gate = side_gate_metrics(games, "cand", opponents)
        champ_gate = side_gate_metrics(games, "champion", opponents)
        verdict = merge_verdict(cand_gate, champ_gate)
        elapsed = round(time.perf_counter() - started, 2)

        paired_summary = {
            "pairs": len(pairs),
            "W": sum(1 for p in pairs if p["outcome"] == "W"),
            "L": sum(1 for p in pairs if p["outcome"] == "L"),
            "T": sum(1 for p in pairs if p["outcome"] == "T"),
            "net_pair_diff": round(sum(p["pair_diff"] for p in pairs), 1),
        }
        payload = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "kind": "paired-ablation",
            "label": args.label,
            "pairing": {
                "design": "same (opponent, seed, seat) cell played by both "
                          "the candidate and the champion; engine + pool are "
                          "deterministic, so the paired difference isolates "
                          "the candidate",
                "episode_steps": args.episode_steps,
            },
            "identity": {
                "candidate": {"path": cand_path, "sha256": cand_sha,
                              "label": cand_label},
                "champion": {"path": champ_path, "sha256": champ_sha,
                             "label": champ_label,
                             "manifest": os.path.basename(FROZEN_MANIFEST)
                             if args.champion == "frozen" else None},
                "identical_bytes": cand_sha == champ_sha,
            },
            "config": {
                "opponents": opponents,
                "seeds": seeds,
                "formal": formal,
                "expected_games": 2 * len(opponents) * len(seeds) * 2,
            },
            "games": games,
            "pairs": pairs,
            "paired_summary": paired_summary,
            "gate": {
                "candidate": cand_gate,
                "champion": champ_gate,
                "verdict": verdict,
            },
            "runtime_seconds": elapsed,
        }
        target = resolve_out_path(args.out, args.label)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
        tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        os.replace(tmp, target)

        print(f"=== paired ablation: {args.label} ===")
        print(f"  candidate {cand_sha[:8]} vs champion {champ_sha[:8]} "
              f"({champ_label})")
        print(f"  grid: {len(opponents)} opponents x {len(seeds)} seeds x "
              f"AB/BA x 2 sides = {len(games)} games ({elapsed}s)")
        print(f"  pairs: {paired_summary['W']}W-{paired_summary['L']}L-"
              f"{paired_summary['T']}T, net diff "
              f"{paired_summary['net_pair_diff']}")
        print(f"  cand : pool_wr={cand_gate['new_style_pool_win_rate']} "
              f"worst={cand_gate['worst_opponent_win_rate']} "
              f"@{cand_gate['worst_opponent']} "
              f"disaster={cand_gate['disaster_rate']}")
        print(f"  champ: pool_wr={champ_gate['new_style_pool_win_rate']} "
              f"worst={champ_gate['worst_opponent_win_rate']} "
              f"@{champ_gate['worst_opponent']} "
              f"disaster={champ_gate['disaster_rate']}")
        print(f"  VERDICT: {'MERGEABLE' if verdict['mergeable'] else 'NOT MERGEABLE'}")
        print(f"  wrote {os.path.relpath(target, SOFTWARE_ROOT)}")
        return 0 if verdict["mergeable"] else 3
    except (ContractError, RuntimeError, OSError, ValueError) as exc:
        print(f"ABLATION FAILED: {exc}", file=sys.stderr)
        return 1
    finally:
        for path in _TEMP_FILES:
            try:
                os.unlink(path)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
