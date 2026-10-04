"""r3-2 development probe: day-by-day trajectory of the candidate vs a bot.

Fast (single-game, seconds) structural feedback for the r3 timing redesign:
d0 capital allocation, herd build deadline, strawberry cadence, crew ramp,
mid-game money lines.  NOT a gate -- the 72-game iterate_gate.py decides
pass/fail; this only points the next single-variable change.

Usage:
    python scripts/r3_trajectory_probe.py --seeds 101 202 303 [--opp pass]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.engine import FULL_EPISODE_STEPS
from kgenv.gym_env import KaggricultureGym
from kgenv.bots.online_pool import scale_ranch_agent


def load_candidate(path):
    spec = importlib.util.spec_from_file_location("r3_probe_candidate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def day_snapshot(obs, player=0):
    farm = obs["farms"][player]
    tiles = farm["tiles"]
    herd = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    placed = 0
    crops = {"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0, "MELON": 0}
    fed = cared = 0
    for row in tiles:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if "animal" in tile:
                herd[tile["animal"]] = herd.get(tile["animal"], 0) + 1
                placed += 1
                fed += 1 if tile.get("fed_today") else 0
                cared += 1 if tile.get("cared_today") else 0
            elif tile.get("kind") == "PLANT":
                crop = tile.get("crop", "?")
                crops[crop] = crops.get(crop, 0) + 1
    shed = (obs.get("private", {}) or {}).get("shed", {}) or {}
    return {
        "day": obs["day"],
        "money": round(farm["money"]),
        "hands": len(farm.get("hands", [])),
        "placed": placed,
        "herd": dict(herd),
        "shed_herd": {a: shed.get(a, 0) for a in ("COW", "SHEEP", "GOOSE")},
        "crops": dict(crops),
        "quads": len(farm.get("unlocked_quadrants", [])),
        "fed": fed,
        "cared": cared,
        "milk": shed.get("MILK", 0),
        "wool": shed.get("WOOL", 0),
        "fert": shed.get("FERTILIZER", 0),
    }


def probe(seed, agent, opponent):
    env = KaggricultureGym(opponent=opponent, episode_steps=FULL_EPISODE_STEPS)
    obs = env.reset(seed=seed)
    snaps = {}
    first_milk = None
    done = False
    while not done:
        action = agent(obs)
        obs, reward, done, info = env.step(action)
        d = obs["day"]
        if d not in snaps or obs["hour"] >= snaps[d].get("hour", 0):
            snap = day_snapshot(obs)
            snap["hour"] = obs["hour"]
            snaps[d] = snap
            if first_milk is None and snap["milk"] > 0:
                first_milk = d
    series = [snaps[d] for d in sorted(snaps)]
    return series, first_milk, env


def summarize(series, first_milk):
    def herd_at(day):
        best = None
        for s in series:
            if s["day"] <= day:
                best = s
        if best is None:
            return 0, {}
        return best["placed"] + sum(best["shed_herd"].values()), best["herd"]

    def crop_at(day, crop):
        best = None
        for s in series:
            if s["day"] <= day:
                best = s
        return (best or {}).get("crops", {}).get(crop, 0)

    def money_at(day):
        best = None
        for s in series:
            if s["day"] <= day:
                best = s
        return (best or {}).get("money", 0)

    peak_herd = max(s["placed"] + sum(s["shed_herd"].values()) for s in series)
    peak_straw = max(s["crops"]["STRAWBERRY"] for s in series)
    last = series[-1]
    return {
        "final_money": last["money"],
        "d0_herd": herd_at(0)[0],
        "d0_herd_species": herd_at(0)[1],
        "herd_d6": herd_at(6)[0],
        "herd_d11": herd_at(11)[0],
        "herd_d24": herd_at(24)[0],
        "first_12_day": next((s["day"] for s in series
                              if s["placed"] + sum(s["shed_herd"].values()) >= 12), None),
        "peak_herd": peak_herd,
        "peak_herd_species": max(series, key=lambda s: s["placed"])["herd"],
        "straw_d7": crop_at(7, "STRAWBERRY"),
        "straw_d11": crop_at(11, "STRAWBERRY"),
        "straw_d13": crop_at(13, "STRAWBERRY"),
        "peak_straw": peak_straw,
        "d12_money": money_at(12),
        "d24_money": money_at(24),
        "crew_d7": next((s["hands"] for s in series if s["day"] == 7), None),
        "crew_d10": next((s["hands"] for s in series if s["day"] == 10), None),
        "first_milk_day": first_milk,
        "quads": last["quads"],
        "final_care_ratio": last["cared"] / max(1, last["placed"]) if last["placed"] else 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default=os.path.join(
        SOFTWARE_ROOT, "kaggle_simulations", "agent", "main.py"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[101, 202, 303])
    parser.add_argument("--opp", default="pass",
                        help="'pass' or 'scale_ranch'")
    parser.add_argument("--json", default="", help="optional output path")
    args = parser.parse_args()

    agent = load_candidate(args.candidate)
    opponent = scale_ranch_agent if args.opp == "scale_ranch" else "pass"

    report = {"candidate": os.path.relpath(args.candidate, SOFTWARE_ROOT),
              "opponent": args.opp, "seeds": {}, "summary": {}}
    keys = None
    for seed in args.seeds:
        series, first_milk, env = probe(seed, agent, opponent)
        summ = summarize(series, first_milk)
        report["seeds"][str(seed)] = summ
        if keys is None:
            keys = list(summ.keys())
        for k in keys:
            report["summary"].setdefault(k, []).append(summ[k])
        print(f"seed {seed}: final={summ['final_money']} d0herd={summ['d0_herd']}"
              f"{summ['d0_herd_species']} herd@6/11={summ['herd_d6']}/{summ['herd_d11']}"
              f" 12@{summ['first_12_day']} peak={summ['peak_herd']}"
              f" straw@7/11/13={summ['straw_d7']}/{summ['straw_d11']}/{summ['straw_d13']}"
              f" peak={summ['peak_straw']} crew@7/10={summ['crew_d7']}/{summ['crew_d10']}"
              f" milk@{summ['first_milk_day']} d12={summ['d12_money']} d24={summ['d24_money']}"
              f" quads={summ['quads']} care={summ['final_care_ratio']:.2f}")
    for k, vals in report["summary"].items():
        nums = [v for v in vals if isinstance(v, (int, float))]
        if nums and len(nums) == len(vals):
            print(f"  {k}: med={sorted(nums)[len(nums)//2]} vals={vals}")
    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=1)
        print(f"wrote {args.json}")


if __name__ == "__main__":
    raise SystemExit(main())
