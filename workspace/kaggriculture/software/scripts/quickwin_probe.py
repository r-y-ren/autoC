#!/usr/bin/env python
"""Phase-C quick-win probe: paired local A/B for single variables.

Runs the CURRENT built artifact self-play over fixed seeds and records
per-seed rewards / escapes / EOD-overflow / action hash into
exports/probes/quickwin_<tag>.json.  Compare two tags with --compare.

Local A/B is a SAFETY DIAGNOSTIC only (2026-09-02 ruling: the local pool
is not the adjudication axis) -- the verdict gates are catastrophe-class
guards (reward collapse >5%, escapes/overflow blowup, nondeterminism),
not strength claims.

Optional --set MODULE_ATTR=VALUE pairs override module constants in-process
(e.g. --set CAP_TURNS_PER_UNIT=3.3 --set CAP_UTIL=0.89).

Usage:
  python scripts/quickwin_probe.py --tag base --seeds 7,8,9,101
  python scripts/quickwin_probe.py --tag capA --seeds 7,8,9,101 --set ...
  python scripts/quickwin_probe.py --compare base capA
"""
import argparse
import json
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
sys.path.insert(0, str(SOFTWARE / "scripts"))

from m4_switchover_regression import (  # noqa: E402
    load_module, reset_module_state, run_episode_probe)


def _coerce(old, raw):
    if isinstance(old, bool):
        return raw.lower() in ("1", "true", "yes")
    if isinstance(old, int):
        return int(float(raw))
    if isinstance(old, float):
        return float(raw)
    return raw


def probe(tag, seeds, steps, overrides):
    module = load_module()
    applied = {}
    for pair in overrides or []:
        key, _, value = pair.partition("=")
        old = getattr(module, key, None)
        setattr(module, key, _coerce(old, value))
        applied[key] = {"old": old, "new": getattr(module, key)}
    episodes = []
    for seed in seeds:
        reset_module_state(module)
        m = run_episode_probe(module, seed, steps)
        episodes.append({"seed": seed, **m})
    mean_reward = sum(e["rewards"][0] + e["rewards"][1]
                      for e in episodes) / len(episodes)
    payload = {
        "schema": "quickwin-probe/1.0", "tag": tag, "seeds": seeds,
        "steps": steps, "overrides": applied,
        "mean_reward": round(mean_reward, 1),
        "escapes": sum(e["escapes"] for e in episodes),
        "overflow_max": max(e["overflow_max"] for e in episodes),
        "all_done": all("DONE" in e["statuses"] for e in episodes),
        "action_hash": {str(e["seed"]): e["action_hash"] for e in episodes},
    }
    dest = SOFTWARE / "exports" / "probes" / f"quickwin_{tag}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items()
                      if k != "action_hash"}, indent=1))
    print(f"[quickwin] {tag} -> {dest}")
    return payload


def compare(a, b):
    verdict = {
        "A": a["tag"], "B": b["tag"],
        "mean_reward_A": a["mean_reward"], "mean_reward_B": b["mean_reward"],
        "reward_delta_pct": round(
            (b["mean_reward"] - a["mean_reward"])
            / max(1.0, a["mean_reward"]) * 100, 2),
        "escapes_A": a["escapes"], "escapes_B": b["escapes"],
        "overflow_A": a["overflow_max"], "overflow_B": b["overflow_max"],
        "all_done": b["all_done"],
        "pass": (b["all_done"] and b["escapes"] <= a["escapes"]
                 and b["overflow_max"] <= a["overflow_max"]
                 and b["mean_reward"] >= a["mean_reward"] * 0.95),
    }
    print(json.dumps(verdict, indent=1))
    return verdict


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tag")
    ap.add_argument("--seeds", default="7,8,9,101")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--compare", nargs=2, metavar=("TAG_A", "TAG_B"))
    args = ap.parse_args()
    probes = SOFTWARE / "exports" / "probes"
    if args.compare:
        a = json.loads((probes / f"quickwin_{args.compare[0]}.json")
                       .read_text(encoding="utf-8"))
        b = json.loads((probes / f"quickwin_{args.compare[1]}.json")
                       .read_text(encoding="utf-8"))
        compare(a, b)
        return
    if not args.tag:
        ap.error("--tag required (or --compare A B)")
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    probe(args.tag, seeds, args.episode_steps, args.set)


if __name__ == "__main__":
    main()
