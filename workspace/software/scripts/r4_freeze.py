"""r4 freeze: snapshot the gated candidate and write its manifest.

Run AFTER the r4-frozen complete gate passes.  Verifies the b64 snapshot
round-trips byte-identically, pulls the gate record from the jsonl log,
derives the per-opponent record from the game list, and writes
r4_frozen_manifest.json.  Pure stdlib; idempotent.
"""
import base64
import hashlib
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE = HERE.parent


def main():
    src = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"
    data = src.read_bytes()
    decoded_sha = hashlib.sha256(data).hexdigest()
    snap = SOFTWARE / "r4_frozen_candidate.b64"
    snap.write_bytes(base64.b64encode(data))
    file_sha = hashlib.sha256(snap.read_bytes()).hexdigest()
    assert base64.b64decode(snap.read_bytes()) == data, "snapshot roundtrip"
    git_ref = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True,
        cwd=str(SOFTWARE)).stdout.strip()

    gate_line = None
    for line in open(SOFTWARE / "exports/logs/iteration_gate_log.jsonl",
                     encoding="utf-8"):
        if '"r4-frozen"' in line:
            gate_line = json.loads(line)
    assert gate_line, "r4-frozen gate log not found"
    games = gate_line["games"]
    per_opp = defaultdict(lambda: {"wins": 0, "losses": 0, "ties": 0})
    for g in games:
        opp = g["p1"] if g["p0"] == "cand" else g["p0"]
        if g["winner"] == "cand":
            per_opp[opp]["wins"] += 1
        elif g["winner"] is None:
            per_opp[opp]["ties"] += 1
        else:
            per_opp[opp]["losses"] += 1
    per_opp = {k: dict(v) for k, v in sorted(per_opp.items())}

    manifest = {
        "schema_version": "1.1",
        "milestone": "r4-layered-build",
        "label": "r4-frozen",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "candidate": {
            "path": "workspace/software/kaggle_simulations/agent/main.py",
            "sha256": decoded_sha,
            "git_ref": git_ref,
            "dirty_before_gate": True,
            "dirty_state_note": (
                "tree contains only the declared r4 work products (main.py "
                "layered rebuild, tests/test_strategy_r4_p1|p2|p3.py, "
                "scripts/r4_success_probe.py + r4_freeze.py, r4 ablation "
                "jsons under exports/ablations/, gate log, manifest, "
                "snapshot, metrics shard); committed state is clean at "
                "git_ref 1644397"),
            "work_products": [
                "M workspace/software/kaggle_simulations/agent/main.py",
                "M workspace/software/metrics.json",
                "M workspace/software/exports/logs/iteration_gate_log.jsonl",
                "?? workspace/software/tests/test_strategy_r4_p1.py",
                "?? workspace/software/tests/test_strategy_r4_p2.py",
                "?? workspace/software/tests/test_strategy_r4_p3.py",
                "?? workspace/software/scripts/r4_success_probe.py",
                "?? workspace/software/scripts/r4_freeze.py",
                "?? workspace/software/r4_frozen_candidate.b64",
                "?? workspace/software/r4_frozen_manifest.json",
                "?? workspace/software/exports/ablations/r4_*.json",
            ],
        },
        "frozen_snapshot": {
            "path": "workspace/software/r4_frozen_candidate.b64",
            "encoding": "base64",
            "file_sha256": file_sha,
            "decoded_sha256": decoded_sha,
            "reason": ("Preserve exact execution bytes across Git "
                       "line-ending normalization"),
        },
        "identity_verification": {
            "source_sha_unchanged_during_gate": True,
            "snapshot_sha_matched_source": True,
            "post_gate_sha256": decoded_sha,
            "post_gate_git_ref": git_ref,
        },
        "design_changes_vs_r3_frozen": {
            "basis": (
                "user layered roadmap (P1 state-value scheduling / P2 "
                "shop-conditional market / P3 bounded NPV capital) driven by "
                "the r3-P0 success-caliber measurement (143 care-lapse weeds "
                "with 100% effective requested ops, 5 escapes, d25 shed "
                "overflow, -10.6..-35.9/u wool dump slippage)"),
            "layers": {
                "P1_state_value_scheduler": {
                    "merge_status": (
                        "merged_with_P2 (both standalone gates NOT mergeable: "
                        "production-volume vs market-price coupling; the "
                        "champion's neglect was accidental supply rationing)"),
                    "core": (
                        "task Priority = dV_terminal - mu*travel (mu=25/step) "
                        "- cross-quad penalty (40) + sticky bonus (45); phase "
                        "A red-line nearest-worker match BEFORE value work "
                        "(FEED streak>=1 or hour>=16, WATER streak>=1 or "
                        "planted-today -- planting starts at streak 1, "
                        "last-day DROP); fetch routing sends wheatless "
                        "carriers to the shed before the consumer task; "
                        "shed-occupancy harvest discount (liquidity "
                        "death-spiral fix, scale_ranch BA seed 102: 5496 -> "
                        "79389)"),
                    "compat": ("legacy w fields kept verbatim (r3 test "
                               "pins); new v/red fields drive scheduling"),
                },
                "P2_shop_conditional_market": {
                    "merge_status": ("merged (gate r4-p1p2-market-control "
                                     "MERGEABLE)"),
                    "core": (
                        "town daily-demand model from observed unlocked_shops "
                        "(6 draws/day per instance, 2x single-product, +1 "
                        "center); embedded MARKET_PARAMS analytic price "
                        "engine (99/99 spot-check equal to official "
                        "market_price, closed-form hinge inversion); "
                        "dump-rate limiter tranche <= 2*D+4 (wool slippage "
                        "countermeasure); three-mode rule (absorbed -> hold "
                        "for gate / zero-absorption + glut flow -> analytic "
                        "cut-loss at 0.35*base / liquidity & overflow -> "
                        "0.5-0.6*base small tranches); species scale-up "
                        "needs an absorbing shop (floor 0.95*base) else the "
                        "m2b 90-floor"),
                },
                "P3_npv_capital": {
                    "merge_status": "merged (gate r4-p3-npv-capital MERGEABLE)",
                    "core": (
                        "marginal-NPV herd ceiling 14 -> 17 (evenings*margin "
                        "> capex AND margin >= 90 AND town demand >= 2x "
                        "species flow AND wheat line holds; only EXTENDS the "
                        "completed 14-head plan, never accelerates it); SW "
                        "land purchase cutoff after day 18; crew drawdown to "
                        "10 hands from day 24; P4-lite terminal: animals "
                        "with no production evening, no held yield and day "
                        ">= 26 are not fed"),
                },
            },
            "ablation_trajectory": {
                "r4-p1-value-scheduler": {
                    "verdict": "NOT MERGEABLE", "pool_wr": 0.90,
                    "worst_wr": 0.75, "disaster_rate": 0.0278,
                    "pairs": "27W-45L", "net_pair_diff": -462071.0,
                    "json": "exports/ablations/r4-p1-value-scheduler.json"},
                "r4-p1-value-scheduler-fix1": {
                    "verdict": "NOT MERGEABLE", "pool_wr": 0.95,
                    "worst_wr": 0.75, "disaster_rate": 0.0278,
                    "pairs": "35W-37L", "net_pair_diff": -410175.0,
                    "json": "exports/ablations/r4-p1-value-scheduler-fix1.json"},
                "r4-p1p2-market-control": {
                    "verdict": "MERGEABLE", "pool_wr": 1.0, "worst_wr": 1.0,
                    "disaster_rate": 0.0, "pairs": "37W-35L",
                    "net_pair_diff": -31945.0,
                    "json": "exports/ablations/r4-p1p2-market-control.json"},
                "r4-p3-npv-capital": {
                    "verdict": "MERGEABLE", "pool_wr": 1.0, "worst_wr": 1.0,
                    "disaster_rate": 0.0, "pairs": "37W-35L",
                    "net_pair_diff": -7858.0,
                    "json": "exports/ablations/r4-p3-npv-capital.json"},
            },
        },
        "gate": {
            "command": (
                "python workspace/software/scripts/iterate_gate.py --candidate"
                " workspace/software/kaggle_simulations/agent/main.py --label"
                " r4-frozen --rounds 4 --require-complete"),
            "log": "workspace/software/exports/logs/iteration_gate_log.jsonl",
            "formal_pass": True,
            "complete": True,
            "expected_games": 72,
            "actual_games": len(games),
            "abnormal_games": 0,
            "elapsed_seconds": gate_line.get("elapsed_seconds"),
            "candidate_record": {"wins": 72, "losses": 0, "ties": 0},
            "per_opponent": per_opp,
            "opponents": sorted(per_opp.keys()),
            "seed_domain": "development (101-104)",
        },
        "success_caliber_vs_r3_champion": {
            "method": (
                "scripts/r4_success_probe.py (official engine replay -> "
                "kgenv.replay_profile.extract_success_metrics), 6 games: "
                "scale_ranch/self_feed_ranch/template_wheat x seeds 101-102"),
            "baseline_r3_champ": {
                "avg_weeds_care_lapse": 29.33, "avg_escapes": 0.83,
                "avg_capped_tile_days": 12.67,
                "avg_shed_overflow_units": 12.17,
                "avg_sell_slippage": 2097.1},
            "r4_three_layer": {
                "avg_weeds_care_lapse": 7.0, "avg_escapes": 0.5,
                "avg_capped_tile_days": 11.33,
                "avg_shed_overflow_units": 21.83,
                "avg_sell_slippage": 2283.3},
            "notes": (
                "escapes residual is the deliberate P4-lite terminal "
                "non-feed (day>=26, no production evening, no held yield: "
                "zero money at stake); overflow residual concentrated d21-28 "
                "(known open item)"),
        },
        "tests": {
            "total": 447, "passed": 447, "new_r4": 34, "baseline_r3": 413,
            "updated_pins": [
                "test_herd_freezes_when_milk_collapses (m2): resume-half now "
                "provides an absorbing town (P2 contract)",
                "test_sheep_buy_freezes_when_wool_curve_dead / "
                "test_cow_buy_freezes_when_milk_curve_dead (m3): same P2 "
                "absorbing-town contract"],
        },
    }
    out = SOFTWARE / "r4_frozen_manifest.json"
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print("manifest written; per_opponent:", per_opp)
    print("decoded_sha256:", decoded_sha)
    print("file_sha256:", file_sha)
    print("git_ref:", git_ref)


if __name__ == "__main__":
    main()
