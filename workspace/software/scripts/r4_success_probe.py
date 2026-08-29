"""r4 layer-build success-caliber probe (campaign III round-3, P1-P3).

Runs a candidate against pool bots on the OFFICIAL engine, converts each
episode into a replay-shaped dict (env.steps already carries per-step
actions + observations) and measures the r3-P0 SUCCESS-CALIBER axis via
kgenv.replay_profile.extract_success_metrics:

  weeds_lapse (care-lapse weed-outs on the field), escapes, capped
  tile-days, shed-overflow discards, per-animal realised yield, sell
  slippage, effective vs requested unit ops.

This is the per-layer development instrument behind the paired-ablation
merge gate (scripts/ablate.py).  NOT a gate itself.

Usage:
    python scripts/r4_success_probe.py --agent <path|frozen> \
        [--opponents scale_ranch,self_feed_ranch] [--seeds 101-104]
        [--out exports/ablations/<name>_success.json] [--label NAME]
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kaggle_environments import make  # noqa: E402

from kgenv.arena import load_submission_agent  # noqa: E402
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
)
from kgenv.engine import FULL_EPISODE_STEPS  # noqa: E402
from kgenv.eval_contract import bytes_sha256  # noqa: E402
from kgenv.replay_profile import extract_success_metrics  # noqa: E402

FROZEN_SNAPSHOT = os.path.join(SOFTWARE_ROOT, "r3_frozen_candidate.b64")
FROZEN_MANIFEST = os.path.join(SOFTWARE_ROOT, "r3_frozen_manifest.json")

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
}
NEW_STYLE_POOL = ["crop_rotator", "template_wheat", "self_feed_ranch",
                  "near_band_diversified", "scale_ranch"]

_TEMP: list[str] = []


def resolve_agent(spec: str):
    """'frozen' -> decoded r3 champion temp file; else a main.py path."""
    if spec == "frozen":
        with open(FROZEN_MANIFEST, "r", encoding="utf-8") as fh:
            expected = json.load(fh)["frozen_snapshot"]["decoded_sha256"]
        data = base64.b64decode(Path(FROZEN_SNAPSHOT).read_bytes())
        if bytes_sha256(data) != expected:
            raise RuntimeError("frozen snapshot sha mismatch")
        handle = tempfile.NamedTemporaryFile(
            "wb", suffix="_frozen_main.py", prefix="probe_", delete=False)
        handle.write(data)
        handle.close()
        _TEMP.append(handle.name)
        return handle.name
    return spec


def episode_replay(agent_path: str, opponent, seed: int, label_a: str):
    """Play one official episode and shape env.steps into a replay dict."""
    agent = load_submission_agent(agent_path)
    env = make("kaggriculture",
               configuration={"episodeSteps": FULL_EPISODE_STEPS,
                              "seed": int(seed), "actTimeout": 60.0},
               debug=True)
    env.run([agent, opponent])
    final = env.steps[-1]
    return {
        "info": {"TeamNames": [label_a, "opponent"], "EpisodeId": None,
                 "seed": int(seed)},
        "configuration": {"episodeSteps": FULL_EPISODE_STEPS, "seed": int(seed)},
        "rewards": [float(s["reward"]) for s in final],
        "statuses": [s["status"] for s in final],
        "steps": env.steps,
    }


def seat_success(success: dict, seat: int) -> dict:
    """Pull the r4 decision metrics for one seat of a success dump."""
    p = success["players"][seat]
    sells = p["market"]["SELL"]
    # average realised slippage per sold unit (first_price - realised mean)
    slip = 0.0
    slip_units = 0
    for _item, row in (sells.get("per_item") or {}).items():
        filled = row.get("filled_qty", 0)
        avg_first = row.get("avg_first_quoted_price")
        if filled and avg_first is not None:
            slip += (avg_first - row.get("avg_price", 0.0)) * filled
            slip_units += filled
    harvest = p.get("harvest_units_by_item", {}) or {}
    animals = p.get("animals", []) or []
    cows = sum(1 for a in animals if a.get("animal") == "COW")
    sheep = sum(1 for a in animals if a.get("animal") == "SHEEP")
    return {
        "reward": p.get("reward"),
        "weeds_care_lapse": p["weeds"]["care_lapse"],
        "weeds_decay": p["weeds"]["overripe_decay"],
        "escapes": p["escapes"]["count"],
        "capped_tile_days": p["animal_cap_waste"]["capped_tile_days"],
        "shed_overflow_units": p["shed_overflow"]["discarded_units"],
        "care_eff": p["ops"]["CARE"]["successes"],
        "feed_eff": p["ops"]["FEED"]["successes"],
        "feed_fail_nores": p["ops"]["FEED"]["failures"]["no_resource"],
        "water_eff": p["ops"]["WATER"]["successes"],
        "harvest_eff": p["ops"]["HARVEST"]["successes"],
        "sell_slippage_total": round(slip, 1),
        "sell_filled": sells.get("filled_qty", 0),
        "milk_harvested": harvest.get("MILK", 0),
        "wool_harvested": harvest.get("WOOL", 0),
        "cows_seen": cows,
        "sheep_seen": sheep,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="frozen")
    parser.add_argument("--opponents", default="scale_ranch,self_feed_ranch,"
                        "template_wheat")
    parser.add_argument("--seeds", default="101-102")
    parser.add_argument("--label", default="probe")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    agent_path = resolve_agent(args.agent)
    opponents = [o for o in args.opponents.split(",") if o]
    seeds: list[int] = []
    for part in args.seeds.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            seeds.extend(range(int(lo), int(hi) + 1))
        elif part:
            seeds.append(int(part))

    rows = []
    started = time.perf_counter()
    for opp_name in opponents:
        opponent = OPPONENTS[opp_name]
        for seed in seeds:
            replay = episode_replay(agent_path, opponent, seed, args.label)
            ok = replay["statuses"] == ["DONE", "DONE"]
            success = extract_success_metrics(replay, strict=False)
            row = {"opponent": opp_name, "seed": seed, "terminal": ok,
                   "reward": replay["rewards"][0],
                   "opponent_reward": replay["rewards"][1]}
            row.update(seat_success(success, 0))
            rows.append(row)
            print(f"[{len(rows):02d}] {args.label} vs {opp_name} seed={seed} "
                  f"r={row['reward']:.0f} ({'W' if row['reward'] > row['opponent_reward'] else 'L'}) "
                  f"weeds_lapse={row['weeds_care_lapse']} escapes={row['escapes']} "
                  f"capped={row['capped_tile_days']} overflow={row['shed_overflow_units']}u "
                  f"feed_nores={row['feed_fail_nores']} slip={row['sell_slippage_total']}")

    def agg(key):
        vals = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
        if not vals:
            return None
        return round(sum(vals) / len(vals), 2)

    summary = {
        "label": args.label,
        "agent": args.agent,
        "games": len(rows),
        "wins": sum(1 for r in rows if r["reward"] > r["opponent_reward"]),
        "avg_reward": round(sum(r["reward"] for r in rows) / len(rows), 1),
        "avg_weeds_care_lapse": agg("weeds_care_lapse"),
        "avg_weeds_decay": agg("weeds_decay"),
        "avg_escapes": agg("escapes"),
        "avg_capped_tile_days": agg("capped_tile_days"),
        "avg_shed_overflow_units": agg("shed_overflow_units"),
        "avg_feed_fail_nores": agg("feed_fail_nores"),
        "avg_sell_slippage": agg("sell_slippage_total"),
        "rows": rows,
        "runtime_seconds": round(time.perf_counter() - started, 1),
    }
    print(f"=== {args.label}: {summary['wins']}/{len(rows)} W, "
          f"avg weeds_lapse={summary['avg_weeds_care_lapse']} "
          f"escapes={summary['avg_escapes']} capped={summary['avg_capped_tile_days']} "
          f"overflow={summary['avg_shed_overflow_units']}u "
          f"slip={summary['avg_sell_slippage']}")

    if args.out:
        target = Path(SOFTWARE_ROOT) / args.out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(summary, ensure_ascii=False, indent=1),
                          encoding="utf-8")
        print(f"wrote {os.path.relpath(target, SOFTWARE_ROOT)}")
    for path in _TEMP:
        try:
            os.unlink(path)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
