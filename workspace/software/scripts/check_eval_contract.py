#!/usr/bin/env python3
"""Executable m2a gate, export-safety, and official-result checks."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.eval_contract import (
    ContractError,
    canonical_sha256,
    resolve_output_path,
    validate_eval_result,
    validate_gate_run,
)
from scripts import run_eval

REQUIRED_OPPONENTS = [
    "cow_baron",
    "melon_hoarder",
    "expansionist",
    "baseline_wheat",
]
M2_KEYS = [
    "llm_ab_win_rate",
    "llm_ab_games",
    "llm_ab_budget_gate_hits",
    "llm_ab_fallback_count",
    "iteration_gate_log",
    "online_ladder_games",
    "online_skill_rating",
    "online_feedback_calibration",
    "final_submission_commits",
]


def _game(p0, p1, seed, seat, *, normal=True, domain="development"):
    return {
        "players": [p0, p1],
        "p0": p0,
        "p1": p1,
        "seed": seed,
        "seed_domain": domain,
        "seat": seat,
        "statuses": ["DONE", "DONE"] if normal else ["INVALID", "DONE"],
        "contract_ok": normal,
        "winner_label": p0,
        "winner": p0,
        "rewards": [2.0, 1.0],
        "turns_played": 720,
        "turns": 720,
        "episode_steps": 720,
        "elapsed_seconds": 0.0,
        "daily_money": [],
    }


def _gate_games():
    games = []
    for opponent in REQUIRED_OPPONENTS:
        for seed in (101, 102, 103, 104):
            games.extend(
                [
                    _game("cand", opponent, seed, "AB"),
                    _game(opponent, "cand", seed, "BA"),
                ]
            )
    return games


def _must_reject(label, callable_):
    try:
        callable_()
    except Exception as exc:  # Expected rejection may come from jsonschema or contract code.
        print(f"PASS rejects {label}: {exc}")
        return
    raise ContractError(f"accepted invalid case: {label}")


def _development_payload():
    evaluation_input = {
        "pairs": [["submission", "cow_baron"]],
        "seeds": [101],
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
        "episode_steps": 720,
        "run_kind": "development",
    }
    games = [
        _game("submission", "cow_baron", 101, "AB"),
        _game("cow_baron", "submission", 101, "BA"),
    ]
    variance = {
        "pair": "submission vs cow_baron",
        "games": 2,
        "seeds": [101, 101],
        "wins": 1,
        "losses": 1,
        "ties": 0,
        "win_rate": 0.5,
        "win_rate_ci95": [0.0945, 0.9055],
        "margin": {
            "n": 2,
            "mean": 0.0,
            "std": 1.4142,
            "ci95_lo": -12.706,
            "ci95_hi": 12.706,
            "min": -1.0,
            "max": 1.0,
        },
        "outcome_flips_across_seeds": True,
    }
    return {
        "schema_version": "2.0",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "run_kind": "development",
        "seed_domain": "development",
        "identity": {
            "submission_path": "main.py",
            "submission_sha256": "a" * 64,
            "git_ref": "deadbeef",
            "dirty": False,
            "input_sha256": canonical_sha256(evaluation_input),
        },
        "evaluation_input": evaluation_input,
        "engine": {
            "package": "kaggle-environments",
            "version": "test",
            "scenario": "kaggriculture",
            "episode_steps": 720,
        },
        "config": {
            "rounds": 1,
            "seeds": [101],
            "contenders": ["submission"],
            "opponents": ["cow_baron", "dummy-a", "dummy-b"],
            "matrix_order": ["submission", "cow_baron"],
            "pairs": [["submission", "cow_baron"]],
            "seat_orders": ["AB", "BA"],
            "expected_games": 2,
        },
        "opponent_pool_names": ["cow_baron", "dummy-a", "dummy-b"],
        "pool_max_elo": None,
        "games": [run_eval._export_game(game) for game in games],
        "abnormal_games": 0,
        "integrity": {"expected_games": 2, "actual_games": 2, "abnormal_games": 0},
        "head_to_head": [
            {
                "pair": "submission vs cow_baron",
                "games": 2,
                "wins": 1,
                "losses": 1,
                "ties": 0,
                "win_rate": 0.5,
                "avg_turns": 720.0,
            }
        ],
        "matchup_win_rates": [
            {
                "a": "submission",
                "b": "cow_baron",
                "games": 2,
                "wins_a": 1,
                "losses_a": 1,
                "ties": 0,
                "win_rate_a": 0.5,
                "avg_margin_a": 0.0,
            }
        ],
        "confirmatory": {"method": "paired W/L/T", "order_independent": True, "standings": []},
        "elo": {
            "role": "descriptive_only",
            "order_sensitive": True,
            "k": 32.0,
            "start": 1200.0,
            "table": [],
        },
        "eval_variance_report": {"method": "test", "per_pair": [variance], "most_volatile_pair": variance},
        "determinism_probes": None,
        "eval_audit_pass": {
            "ref": "test",
            "pass_count": None,
            "warn_count": None,
            "fail_count": None,
            "all_critical_pass": None,
        },
        "failure_modes": None,
        "m2": {key: None for key in M2_KEYS},
        "regression_gate": None,
        "runtime_seconds": 0.0,
    }, games


def check_gate() -> None:
    games = _gate_games()
    seeds = [101, 102, 103, 104]
    report = validate_gate_run(games, REQUIRED_OPPONENTS, seeds, True, REQUIRED_OPPONENTS)
    if not report["formal_pass"] or report["expected_games"] != 32:
        raise ContractError("complete gate fixture did not formally pass")
    _must_reject(
        "missing opponent",
        lambda: validate_gate_run(games[:24], REQUIRED_OPPONENTS[:3], seeds, True, REQUIRED_OPPONENTS),
    )
    _must_reject(
        "single seat",
        lambda: validate_gate_run(games[:-1], REQUIRED_OPPONENTS, seeds, True, REQUIRED_OPPONENTS),
    )
    abnormal = list(games)
    abnormal[0] = _game("cand", REQUIRED_OPPONENTS[0], 101, "AB", normal=False)
    _must_reject(
        "abnormal game",
        lambda: validate_gate_run(abnormal, REQUIRED_OPPONENTS, seeds, True, REQUIRED_OPPONENTS),
    )
    fake_tie = _game("cand", "cow_baron", 101, "AB")
    fake_tie.update(winner=None, winner_label=None)
    _must_reject(
        "malformed tie",
        lambda: validate_gate_run([fake_tie], ["cow_baron"], [101], False, REQUIRED_OPPONENTS),
    )
    wrong_domain = _game("cand", "cow_baron", 101, "AB", domain="holdout")
    _must_reject(
        "seed domain mismatch",
        lambda: validate_gate_run([wrong_domain], ["cow_baron"], [101], False, REQUIRED_OPPONENTS),
    )
    subset = validate_gate_run(games[:2], [REQUIRED_OPPONENTS[0]], [101], False, REQUIRED_OPPONENTS)
    if subset["formal_pass"] or subset["mode"] != "exploratory":
        raise ContractError("exploratory subset returned formal PASS")
    print("PASS gate production invariants")


def check_export() -> None:
    payload, games = _development_payload()
    run_eval._schema_validate(payload)
    with tempfile.TemporaryDirectory(prefix="m2a_export_") as temp:
        exports = Path(temp)
        logs = exports / "logs"
        logs.mkdir()
        formal = exports / "eval_results.json"
        replay = logs / "replay_log.jsonl"
        formal.write_text('{"old": true}\n', encoding="utf-8")
        replay.write_text("old-replay\n", encoding="utf-8")
        old_export, old_replay = formal.read_bytes(), replay.read_bytes()

        _must_reject(
            "case alias to official export",
            lambda: resolve_output_path(False, str(exports / "EVAL_RESULTS.JSON"), exports),
        )
        bad_payload = dict(payload)
        bad_payload.pop("identity")
        _must_reject(
            "schema failure",
            lambda: run_eval.publish_evaluation(bad_payload, games, True, exports_dir=exports),
        )
        if formal.read_bytes() != old_export or replay.read_bytes() != old_replay:
            raise ContractError("schema failure changed official evidence")

        def replay_failure(data, expected):
            raise ContractError("injected replay validation failure")

        _must_reject(
            "replay failure",
            lambda: run_eval.publish_evaluation(
                payload, games, True, exports_dir=exports, replay_validator=replay_failure
            ),
        )
        if formal.read_bytes() != old_export or replay.read_bytes() != old_replay:
            raise ContractError("replay failure changed official evidence")

        target, dev_replay = run_eval.publish_evaluation(
            payload, games, False, exports_dir=exports
        )
        if Path(target).name != "eval_results.dev.json" or Path(dev_replay).name != "replay_log.dev.jsonl":
            raise ContractError("development evidence is not isolated")
        if formal.read_bytes() != old_export or replay.read_bytes() != old_replay:
            raise ContractError("development publish changed official evidence")
    print("PASS production schema, path, replay, and transaction safety")


def check_official(input_path: Path) -> None:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    run_eval._schema_validate(payload)
    report = validate_eval_result(payload, require_official=True)
    print(
        f"PASS official export: expected={report['expected_games']} "
        f"actual={report['actual_games']} abnormal={report['abnormal_games']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("gate", "export", "official"), required=True)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    try:
        if args.mode == "gate":
            check_gate()
        elif args.mode == "export":
            check_export()
        elif args.input is None:
            raise ContractError("--mode official requires --input")
        else:
            check_official(args.input.resolve())
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL {args.mode}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
