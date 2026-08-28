"""Local evaluation: FULL matchup matrix over the whole bot pool (m1 wave 2).

Usage (from workspace/software or repo root):
    python scripts/run_eval.py [--rounds 4] [--quick]
    python scripts/run_eval.py --rounds 2 --assert-regression

Plays every unordered pair of the pool (submission + 3 m1 strong opponents
+ baseline_wheat + the frozen weak pool) at N fixed seeds per pairing,
plus the m0 head-to-head extra seeds (submission vs baseline_wheat, +500
offsets).  Computes:

  * the full-pool Elo table (k=32, win/loss/tie only -- official ladder
    semantics; order-sensitive stream),
  * a win-rate matrix (matchup_win_rates) and head_to_head summaries,
  * a seed-variance report (Wilson 95% CIs on win rates, Student-t CIs on
    money margins, most-volatile pairing),
  * determinism probes (same pairing + seed played twice; deterministic
    pairs must be reward-identical, the engine "random" agent may drift --
    a declared boundary),
  * schema v1.1 contract fields aligned with workspace/docs/metrics-keys.md
    (B-group m1 keys + nullable m2 placeholders).

Writes exports/eval_results.json (validated against exports/schema.json
BEFORE the write) and exports/logs/replay_log.jsonl (per-game daily money
+ shared-market daily prices for failure-mode analysis).

--assert-regression is the frozen regression gate: the two m0 invariants
are evaluated on the FROZEN-SUBSET stream only (games between the six
frozen-pool players, Elo recomputed on that subset), so the m1 strong
opponents stress the submission without redefining the frozen line.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import (SOFTWARE_ROOT as ARENA_ROOT, load_submission_agent,
                         run_match, summarize_games, write_replay_log)
from kgenv.bots.baseline import baseline_wheat_agent, greedy_carrot_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.elo import EloTable
from kgenv.engine import FULL_EPISODE_STEPS
from kgenv.regression import (check_regression, format_verdict,
                              frozen_games)
from kgenv.variance import (margin_stats, most_volatile_pair, pair_variance,
                            wilson_ci)
from kgenv import official_engine_version

EXPORTS_DIR = os.path.join(SOFTWARE_ROOT, "exports")
SCHEMA_VERSION = "1.1"

# Play order for the matrix (also fixes pair enumeration and the Elo stream).
MATRIX_ORDER = [
    "submission",                                  # our contender
    "cow_baron", "melon_hoarder", "expansionist",  # m1 wave-2 strong pool
    "baseline_wheat",                              # our A/B comparator
    "greedy_carrot", "starter", "random", "pass",  # frozen weak pool
]

# m2 placeholder keys (workspace/docs/metrics-keys.md B group) -- null until
# the LLM A/B wave measures them; defined here so the contract is stable.
M2_KEYS = [
    "llm_ab_win_rate", "llm_ab_games", "llm_ab_budget_gate_hits",
    "llm_ab_fallback_count", "iteration_gate_log", "online_ladder_games",
    "online_skill_rating", "online_feedback_calibration",
    "final_submission_commits",
]


def build_players():
    """Everyone in the matrix: our contenders + the opponent pool."""
    submission = load_submission_agent()
    contenders = {
        "submission": submission,        # enhanced bot (main.py)
        "baseline_wheat": baseline_wheat_agent,
    }
    opponents = {
        "pass": "pass",                  # engine built-ins
        "random": "random",
        "starter": "starter",            # official deterministic carrot loop
        "greedy_carrot": greedy_carrot_agent,
        "cow_baron": cow_baron_agent,        # m1: dairy baron (milk engine)
        "melon_hoarder": melon_hoarder_agent,  # m1: melon waves, hoard gates
        "expansionist": expansionist_agent,    # m1: land+labour wheat estate
    }
    return contenders, opponents


def _load_json_if_exists(path):
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def _matchup_rows(games, order):
    """Win-rate matrix rows for every unordered pair (i<j in order)."""
    rows = []
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            margins = []
            w = l = t = 0
            for g in games:
                if g.get("players") != [a, b]:
                    continue
                if g["winner_label"] == a:
                    w += 1
                elif g["winner_label"] == b:
                    l += 1
                else:
                    t += 1
                rw = g["rewards"]
                margins.append(rw[0] - rw[1])
            n = w + l + t
            if n == 0:
                continue
            ms = margin_stats(margins)
            rows.append({
                "a": a, "b": b, "games": n,
                "wins_a": w, "losses_a": l, "ties": t,
                "win_rate_a": round((w + 0.5 * t) / n, 4),
                "avg_margin_a": ms["mean"],
            })
    return rows


def _determinism_probes(everyone):
    """Same (pairing, seed) played twice; deterministic pair must match.

    The engine's built-in "random" agent is NOT fully pinned by the episode
    seed (it seeds from OS entropy), so its rewards may drift between runs
    -- a declared, known boundary (m0 cross-session evidence: 32/40 games
    reward-identical, all 8 drifters were vs "random").
    """
    probes = []
    for a, b, expect in (
            ("greedy_carrot", "starter", "identical"),
            ("greedy_carrot", "random", "may_drift")):
        runs = []
        for _ in range(2):
            res = run_match(everyone[a], everyone[b], seed=101,
                            label_a=a, label_b=b,
                            episode_steps=FULL_EPISODE_STEPS,
                            collect_daily=False)
            runs.append([round(r, 2) for r in res["rewards"]])
        probes.append({
            "pair": f"{a} vs {b}", "seed": 101, "expectation": expect,
            "run_rewards": runs, "identical": runs[0] == runs[1],
        })
    note = ("deterministic agents replay reward-identically for a fixed "
            "(pairing, seed); the engine 'random' agent may drift because "
            "it is not fully pinned by the episode seed (declared boundary, "
            "see eval_audit.md)")
    return {"note": note, "probes": probes}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=4,
                    help="seeds per matrix pairing")
    ap.add_argument("--quick", action="store_true",
                    help="tiny matrix for smoke tests")
    ap.add_argument("--assert-regression", action="store_true",
                    help="assert the frozen regression line after the run "
                         "(evaluated on the frozen-subset stream); exits 1 "
                         "with a diff table on violation")
    args = ap.parse_args()

    contenders, opponents = build_players()
    everyone = dict(contenders)
    everyone.update(opponents)

    rounds = 1 if args.quick else max(1, args.rounds)
    seeds = list(range(101, 101 + rounds))

    # pair enumeration: full matrix (quick mode: submission vs pool only)
    if args.quick:
        pairs = [("submission", o) for o in MATRIX_ORDER[1:]]
    else:
        pairs = [(MATRIX_ORDER[i], MATRIX_ORDER[j])
                 for i in range(len(MATRIX_ORDER))
                 for j in range(i + 1, len(MATRIX_ORDER))]

    games = []
    t0 = time.perf_counter()

    for a, b in pairs:
        for s in seeds:
            res = run_match(everyone[a], everyone[b], seed=s,
                            label_a=a, label_b=b,
                            episode_steps=FULL_EPISODE_STEPS,
                            collect_daily=True)
            games.append(res)
            print(f"[{len(games):03d}] {a} vs {b} seed={s}: "
                  f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
                  f"winner={res['winner_label']}")

    # m0 protocol continuity: extra head-to-head seeds (+500 offset)
    if not args.quick:
        for s in [x + 500 for x in seeds]:
            res = run_match(contenders["submission"],
                            contenders["baseline_wheat"], seed=s,
                            label_a="submission", label_b="baseline_wheat",
                            episode_steps=FULL_EPISODE_STEPS,
                            collect_daily=True)
            games.append(res)
            print(f"[{len(games):03d}] submission vs baseline_wheat seed={s}: "
                  f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
                  f"winner={res['winner_label']}")

    probes = None if args.quick else _determinism_probes(everyone)

    runtime = time.perf_counter() - t0

    # ---- Elo: full pool over the recorded stream (play order) -------------
    def elo_table(stream):
        table = EloTable(k=32.0, start=1200.0)
        for g in stream:
            if g["winner_label"] == g["players"][0]:
                score = 1.0
            elif g["winner_label"] == g["players"][1]:
                score = 0.0
            else:
                score = 0.5
            table.record(g["players"][0], g["players"][1], score)
        return table

    table = elo_table(games)
    ranked = table.ranked()

    # ---- matrix / variance --------------------------------------------------
    matchup_rows = _matchup_rows(games, MATRIX_ORDER)
    head_to_head = [summarize_games(games, r["a"], r["b"])
                    for r in matchup_rows]
    var_reports = [pair_variance(games, r["a"], r["b"])
                   for r in matchup_rows]
    volatile = most_volatile_pair(var_reports)

    pool_names = [n for n in MATRIX_ORDER if n != "submission"]
    pool_rated = [row for row in ranked if row["name"] in pool_names]
    pool_max = pool_rated[0] if pool_rated else None

    # ---- embed authored summaries when present ------------------------------
    audit_summary = _load_json_if_exists(
        os.path.join(EXPORTS_DIR, "eval_audit_summary.json"))
    failure_summary = _load_json_if_exists(
        os.path.join(EXPORTS_DIR, "failure_modes_summary.json"))

    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "engine": {
            "package": "kaggle-environments",
            "version": official_engine_version(),
            "scenario": "kaggriculture",
            "episode_steps": FULL_EPISODE_STEPS,
        },
        "config": {
            "rounds": rounds, "seeds": seeds,
            "contenders": list(contenders), "opponents": list(opponents),
            "matrix_order": MATRIX_ORDER,
        },
        "opponent_pool_names": pool_names,
        "pool_max_elo": ({"name": pool_max["name"],
                          "rating": pool_max["rating"]}
                         if pool_max else None),
        "games": [{
            "p0": g["players"][0], "p1": g["players"][1], "seed": g["seed"],
            "rewards": g["rewards"], "winner": g["winner_label"],
            "turns": g["turns_played"], "elapsed_seconds": g["elapsed_seconds"],
        } for g in games],
        "head_to_head": head_to_head,
        "matchup_win_rates": matchup_rows,
        "elo": {"k": 32.0, "start": 1200.0, "table": ranked},
        "eval_variance_report": {
            "method": ("per pairing across seeds: win rate with Wilson 95% CI "
                       "(ties = 0.5 win); money margins (a-b) with mean/std "
                       "and Student-t 95% CI"),
            "per_pair": var_reports,
            "most_volatile_pair": volatile,
        },
        "determinism_probes": probes,
        "eval_audit_pass": {
            "ref": "exports/eval_audit.md",
            "pass_count": (audit_summary or {}).get("pass_count"),
            "warn_count": (audit_summary or {}).get("warn_count"),
            "fail_count": (audit_summary or {}).get("fail_count"),
            "all_critical_pass": (audit_summary or {}).get("all_critical_pass"),
        },
        "failure_modes": (None if failure_summary is None else {
            "ref": "exports/failure_modes.md",
            "count": failure_summary.get("count"),
            "top": failure_summary.get("top"),
        }),
        "m2": {k: None for k in M2_KEYS},
        "runtime_seconds": round(runtime, 2),
    }

    # ---- validate against the shipped schema BEFORE writing -----------------
    schema_path = os.path.join(EXPORTS_DIR, "schema.json")
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    try:
        import jsonschema
        jsonschema.validate(result, schema)
    except Exception as exc:  # noqa: BLE001
        print(f"SCHEMA VALIDATION FAILED, not writing eval_results.json: {exc}")
        return 1

    os.makedirs(EXPORTS_DIR, exist_ok=True)
    out_path = os.path.join(EXPORTS_DIR, "eval_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log_path = write_replay_log(os.path.join(EXPORTS_DIR, "logs"), games)

    # ---- console report ------------------------------------------------------
    print(f"\n=== Elo table ({len(games)} games, "
          f"{result['runtime_seconds']}s) ===")
    for row in ranked:
        print(f"  {row['name']:<16} rating={row['rating']:7.1f} "
              f"record W{row['record']['W']} L{row['record']['L']} "
              f"T{row['record']['T']}")
    print(f"\npool max Elo: {pool_max['name']} = {pool_max['rating']}")
    print("\n=== submission vs pool ===")
    for row in matchup_rows:
        if row["a"] != "submission" and row["b"] != "submission":
            continue
        opp = row["b"] if row["a"] == "submission" else row["a"]
        sign = 1.0 if row["a"] == "submission" else -1.0
        wr = row["win_rate_a"] if row["a"] == "submission" \
            else round(1.0 - row["win_rate_a"], 4)
        print(f"  vs {opp:<16} games={row['games']} "
              f"win_rate={wr:.2f} avg_margin={sign * row['avg_margin_a']:+.0f}")
    if volatile:
        print(f"\nmost volatile pairing: {volatile['pair']} "
              f"win_rate={volatile['win_rate']} "
              f"CI95={volatile['win_rate_ci95']} "
              f"flips={volatile['outcome_flips_across_seeds']}")
    if probes:
        for p in probes["probes"]:
            print(f"determinism probe {p['pair']} seed={p['seed']}: "
                  f"identical={p['identical']} ({p['expectation']}) "
                  f"rewards={p['run_rewards']}")
    print(f"\nwrote {out_path}")
    print(f"wrote {log_path}")

    # ---- frozen regression gate ----------------------------------------------
    if args.assert_regression:
        frozen = frozen_games(games)
        frozen_table = elo_table(frozen)
        report = check_regression(frozen, frozen_table.ranked())
        print(f"\n=== regression gate on frozen subset "
              f"({len(frozen)}/{len(games)} games; seeds {seeds} + "
              f"{[x + 500 for x in seeds]}) ===")
        for line in report["diff_table"]:
            print(f"  {line}")
        print(f"  {format_verdict(report)}")
        if not report["ok"]:
            print("  regression gate FAILED -- diff table above")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
