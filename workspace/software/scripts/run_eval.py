"""Seat-balanced local evaluation with fail-closed transactional publication."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(SOFTWARE_ROOT))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv import official_engine_version
from kgenv.arena import load_submission_agent, run_match
from kgenv.bots.baseline import baseline_wheat_agent, greedy_carrot_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.bots.online_pool import (crop_rotator_agent,
                                    near_band_diversified_agent,
                                    scale_ranch_agent,
                                    self_feed_ranch_agent,
                                    template_wheat_agent,
                                    wheat_straw_monster_agent)
from kgenv.elo import EloTable
from kgenv.engine import FULL_EPISODE_STEPS
from kgenv.eval_contract import (
    ContractError,
    STANDARD_MATRIX_ORDER,
    atomic_publish_bundle,
    build_ab_ba_schedule,
    candidate_snapshot,
    order_independent_standings,
    resolve_output_path,
    assert_games_normal,
    validate_eval_result,
)
from kgenv.regression import check_regression, format_verdict, frozen_games
from kgenv.variance import margin_stats, most_volatile_pair, wilson_ci

EXPORTS_DIR = os.path.join(SOFTWARE_ROOT, "exports")
SCHEMA_VERSION = "2.0"
MATRIX_ORDER = list(STANDARD_MATRIX_ORDER)
# m2 online-style opponents (campaign III) + r3-1 scale_ranch: certified
# ladder-archetype reconstructions.  The canonical STANDARD_MATRIX_ORDER is
# FROZEN (the published official_holdout export validates against it), so
# these join the pool as a development-run extension and as gate required
# opponents -- never inside the canonical official matrix.
ONLINE_STYLE_POOL = [
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
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


def build_players(candidate_path: str, extended_pool: bool = False):
    contenders = {
        "submission": load_submission_agent(candidate_path),
        "baseline_wheat": baseline_wheat_agent,
    }
    opponents = {
        "pass": "pass",
        "random": "random",
        "starter": "starter",
        "greedy_carrot": greedy_carrot_agent,
        "cow_baron": cow_baron_agent,
        "melon_hoarder": melon_hoarder_agent,
        "expansionist": expansionist_agent,
        # m2 online-style opponents (campaign III) + r3-1 scale_ranch:
        # always part of the available pool; scheduled by default via
        # --extended-pool
        "crop_rotator": crop_rotator_agent,
        "template_wheat": template_wheat_agent,
        "self_feed_ranch": self_feed_ranch_agent,
        "near_band_diversified": near_band_diversified_agent,
        "scale_ranch": scale_ranch_agent,
        "wheat_straw_monster": wheat_straw_monster_agent,
    }
    if not extended_pool:
        # canonical pool only: keep the historical run_eval opponent dict
        # identical to the frozen export's config.opponents
        frozen = {"pass", "random", "starter", "greedy_carrot", "cow_baron",
                  "melon_hoarder", "expansionist"}
        opponents = {k: v for k, v in opponents.items() if k in frozen}
    return contenders, opponents


def _perspective(game, name):
    index = game["players"].index(name)
    return game["rewards"][index] - game["rewards"][1 - index]


def _pair_games(games, a, b):
    return [game for game in games if set(game["players"]) == {a, b}]


def summarize_pair(games, a, b):
    selected = _pair_games(games, a, b)
    assert_games_normal(selected)
    wins = sum(game["winner_label"] == a for game in selected)
    losses = sum(game["winner_label"] == b for game in selected)
    ties = sum(game["winner_label"] is None for game in selected)
    count = len(selected)
    return {
        "pair": f"{a} vs {b}",
        "games": count,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate": round((wins + 0.5 * ties) / count, 4) if count else None,
        "avg_turns": (
            round(sum(game["turns_played"] for game in selected) / count, 1)
            if count
            else None
        ),
    }


def matchup_row(games, a, b):
    summary = summarize_pair(games, a, b)
    margins = [_perspective(game, a) for game in _pair_games(games, a, b)]
    return {
        "a": a,
        "b": b,
        "games": summary["games"],
        "wins_a": summary["wins"],
        "losses_a": summary["losses"],
        "ties": summary["ties"],
        "win_rate_a": summary["win_rate"],
        "avg_margin_a": margin_stats(margins)["mean"],
    }


def variance_row(games, a, b):
    selected = _pair_games(games, a, b)
    summary = summarize_pair(games, a, b)
    margins = [_perspective(game, a) for game in selected]
    lo, hi = wilson_ci(summary["wins"] + 0.5 * summary["ties"], len(selected))
    return {
        "pair": summary["pair"],
        "games": len(selected),
        "seeds": [game["seed"] for game in selected],
        "wins": summary["wins"],
        "losses": summary["losses"],
        "ties": summary["ties"],
        "win_rate": summary["win_rate"],
        "win_rate_ci95": [lo, hi] if lo is not None else None,
        "margin": margin_stats(margins),
        "outcome_flips_across_seeds": summary["wins"] > 0 and summary["losses"] > 0,
    }


def elo_table(games):
    table = EloTable(k=32.0, start=1200.0)
    for game in games:
        if game["winner_label"] == game["players"][0]:
            score = 1.0
        elif game["winner_label"] == game["players"][1]:
            score = 0.0
        else:
            score = 0.5
        table.record(game["players"][0], game["players"][1], score)
    return table


def _export_game(game):
    return {
        "players": list(game["players"]),
        "p0": game["players"][0],
        "p1": game["players"][1],
        "seed": game["seed"],
        "seed_domain": game["seed_domain"],
        "seat": game["seat"],
        "statuses": game["statuses"],
        "contract_ok": game["contract_ok"],
        "rewards": game["rewards"],
        "winner": game["winner_label"],
        "winner_label": game["winner_label"],
        "turns": game["turns_played"],
        "elapsed_seconds": game["elapsed_seconds"],
    }


def _schema_validate(payload):
    import jsonschema

    with open(os.path.join(EXPORTS_DIR, "schema.json"), encoding="utf-8") as stream:
        jsonschema.validate(payload, json.load(stream))
    return validate_eval_result(
        payload, require_official=payload.get("run_kind") == "official"
    )


def _replay_bytes(games):
    lines = []
    for game in games:
        lines.append(
            json.dumps(
                {
                    "players": game["players"],
                    "winner": game["winner_label"],
                    "seed": game["seed"],
                    "seed_domain": game["seed_domain"],
                    "seat": game["seat"],
                    "statuses": game["statuses"],
                    "contract_ok": game["contract_ok"],
                    "rewards": game["rewards"],
                    "turns": game["turns_played"],
                    "episode_steps": game["episode_steps"],
                    "elapsed_seconds": game["elapsed_seconds"],
                    "daily_money": [
                        row.get("money") for row in game.get("daily_money", [])
                    ],
                    "daily_prices": [
                        row.get("prices") for row in game.get("daily_money", [])
                    ],
                },
                ensure_ascii=False,
            )
        )
    return (("\n".join(lines) + "\n") if lines else "").encode("utf-8")


def _validate_replay_bytes(data, expected_games):
    lines = [line for line in data.decode("utf-8").splitlines() if line]
    if len(lines) != expected_games:
        raise ContractError("replay game count mismatch")
    for line in lines:
        row = json.loads(line)
        if row.get("statuses") != ["DONE", "DONE"] or row.get("contract_ok") is not True:
            raise ContractError("replay contains abnormal game")


def publish_evaluation(
    payload,
    games,
    official,
    requested="",
    exports_dir=EXPORTS_DIR,
    replay_validator=_validate_replay_bytes,
):
    target = resolve_output_path(official, requested, exports_dir)
    replay_name = "replay_log.jsonl" if official else "replay_log.dev.jsonl"
    replay_target = Path(exports_dir).resolve() / "logs" / replay_name
    export_data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    replay_data = _replay_bytes(games)

    def validate_staged():
        _schema_validate(payload)
        replay_validator(replay_data, len(games))

    atomic_publish_bundle(
        [(Path(target), export_data), (replay_target, replay_data)], validate_staged
    )
    return target, str(replay_target)


def _matrix_pairs(quick, matrix_order):
    if quick:
        return [("submission", name) for name in matrix_order[1:]]
    return [
        (matrix_order[i], matrix_order[j])
        for i in range(len(matrix_order))
        for j in range(i + 1, len(matrix_order))
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--assert-regression", action="store_true")
    parser.add_argument(
        "--extended-pool",
        action="store_true",
        help="development runs only: add the m2 online-style opponents to "
             "the evaluation matrix (cannot be combined with --official)",
    )
    parser.add_argument(
        "--official",
        action="store_true",
        help="publish the canonical full development export",
    )
    parser.add_argument(
        "--candidate",
        default=os.path.join(SOFTWARE_ROOT, "kaggle_simulations", "agent", "main.py"),
    )
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    rounds = 1 if args.quick else args.rounds
    if rounds < 1 or rounds > 4:
        print("development evaluation rounds must be 1..4", file=sys.stderr)
        return 2
    if args.official and (args.quick or rounds != 4 or not args.assert_regression):
        print(
            "--official requires --rounds 4, the full matrix, and --assert-regression",
            file=sys.stderr,
        )
        return 2
    if args.official and args.extended_pool:
        print(
            "--extended-pool is a development-run extension; the official "
            "export must keep the canonical matrix",
            file=sys.stderr,
        )
        return 2

    matrix_order = list(MATRIX_ORDER)
    if args.extended_pool:
        matrix_order += [name for name in ONLINE_STYLE_POOL
                         if name not in MATRIX_ORDER]
    run_kind = "official" if args.official else "development"
    seeds = list(range(101, 101 + rounds))
    pairs = _matrix_pairs(args.quick, matrix_order)
    evaluation_input = {
        "pairs": [list(pair) for pair in pairs],
        "seeds": seeds,
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
        "episode_steps": FULL_EPISODE_STEPS,
        "run_kind": run_kind,
    }
    schedule = build_ab_ba_schedule(pairs, seeds, "development")

    try:
        with candidate_snapshot(REPO_ROOT, args.candidate, evaluation_input) as snapshot:
            contenders, opponents = build_players(
                str(snapshot.snapshot_path), extended_pool=args.extended_pool)
            everyone = {**contenders, **opponents}
            games = []
            started = time.perf_counter()
            for item in schedule:
                result = run_match(
                    everyone[item["p0"]],
                    everyone[item["p1"]],
                    seed=item["seed"],
                    label_a=item["p0"],
                    label_b=item["p1"],
                    episode_steps=FULL_EPISODE_STEPS,
                    collect_daily=not args.quick,
                )
                result["seat"] = item["seat"]
                result["seed_domain"] = item["seed_domain"]
                games.append(result)
                print(
                    f"[{len(games):03d}/{len(schedule)}] {item['p0']} vs "
                    f"{item['p1']} seed={item['seed']} seat={item['seat']} "
                    f"winner={result['winner_label']}"
                )

            table = elo_table(games)
            ranked = table.ranked()
            head_to_head = [summarize_pair(games, a, b) for a, b in pairs]
            matchup_rows = [matchup_row(games, a, b) for a, b in pairs]
            variance_rows = [variance_row(games, a, b) for a, b in pairs]
            pool_names = [name for name in matrix_order if name != "submission"]
            pool_rows = [row for row in ranked if row["name"] in pool_names]
            pool_max = pool_rows[0] if pool_rows else None

            regression_report = None
            if args.assert_regression:
                frozen = frozen_games(games)
                frozen_standings = order_independent_standings(frozen)
                regression_rows = [
                    {"name": row["name"], "rating": row["score_rate"]}
                    for row in frozen_standings
                ]
                regression_report = check_regression(frozen, regression_rows)
                regression_report["method"] = "order-independent aggregate score rate"
                print(format_verdict(regression_report))
                if not regression_report["ok"]:
                    raise ContractError("regression gate failed")

            payload = {
                "schema_version": SCHEMA_VERSION,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "run_kind": run_kind,
                "seed_domain": "development",
                "identity": snapshot.identity,
                "evaluation_input": evaluation_input,
                "engine": {
                    "package": "kaggle-environments",
                    "version": official_engine_version(),
                    "scenario": "kaggriculture",
                    "episode_steps": FULL_EPISODE_STEPS,
                },
                "config": {
                    "rounds": rounds,
                    "seeds": seeds,
                    "contenders": list(contenders),
                    "opponents": list(opponents),
                    "matrix_order": matrix_order,
                    "pairs": [list(pair) for pair in pairs],
                    "seat_orders": ["AB", "BA"],
                    "expected_games": len(schedule),
                },
                "opponent_pool_names": [name for name in matrix_order
                                        if name != "submission"],
                "pool_max_elo": (
                    {"name": pool_max["name"], "rating": pool_max["rating"]}
                    if pool_max
                    else None
                ),
                "games": [_export_game(game) for game in games],
                "abnormal_games": 0,
                "integrity": {
                    "expected_games": len(schedule),
                    "actual_games": len(games),
                    "abnormal_games": 0,
                },
                "head_to_head": head_to_head,
                "matchup_win_rates": matchup_rows,
                "confirmatory": {
                    "method": "aggregate seat-balanced score rate and paired W/L/T",
                    "order_independent": True,
                    "standings": order_independent_standings(games),
                },
                "elo": {
                    "role": "descriptive_only",
                    "order_sensitive": True,
                    "k": 32.0,
                    "start": 1200.0,
                    "table": ranked,
                },
                "eval_variance_report": {
                    "method": "seat-balanced Wilson 95% and Student-t margin CI",
                    "per_pair": variance_rows,
                    "most_volatile_pair": most_volatile_pair(variance_rows),
                },
                "determinism_probes": None,
                "eval_audit_pass": {
                    "ref": "exports/eval_audit.md",
                    "pass_count": None,
                    "warn_count": None,
                    "fail_count": None,
                    "all_critical_pass": None,
                },
                "failure_modes": None,
                "m2": {key: None for key in M2_KEYS},
                "regression_gate": regression_report,
                "runtime_seconds": round(time.perf_counter() - started, 2),
            }

            snapshot.verify_unchanged()
            target, replay_target = publish_evaluation(
                payload, games, args.official, args.output
            )
            print(
                f"wrote {target} and {replay_target} transactionally "
                f"({len(games)} games, {payload['runtime_seconds']}s)"
            )
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"EVALUATION FAILED, published evidence preserved: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
