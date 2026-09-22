#!/usr/bin/env python
"""M1 capacity-law calibration (scheduler §2.6 / branch §5.3; S-M1 gate).

Measures the two empirical coefficients of the capacity law
    max_units(d) ~= 24 x (1+H) x CAP_UTIL / CAP_TURNS_PER_UNIT
from real play:
  * turns_per_unit -- labour turns (moves + ops, non-PASS) per asset-unit
    per day  -> calibrates CAP_TURNS_PER_UNIT (currently 2.4);
  * eff_share    -- labour turns / (24 x (1+H))  -> calibrates CAP_UTIL
    (currently 0.75).

Two sources:
  local   : self-play episodes through the local engine (default);
  --replays GLOB : official replay JSONs (steps[].action + observation),
        e.g. the v10.9 / tetsuya / top-20 corpora (cross-validation, doc
        requires the reference-replay cross-check before backfilling).

Reports medians over ALL days and over HIGH-LOAD days only (eff_share >=
0.5 -- the regime the law models).  Never edits constants: the backfill
decision is a JOURNAL-recorded ruling on this output.

Usage:
  python scripts/capacity_calibration.py [--seeds 7,8] [--episode-steps 720]
      [--replays "refs/replay-corpus/*.json"] [--out exports/probes/...]
"""
import argparse
import glob
import importlib.util
import json
import statistics
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
from kgenv.engine import run_episode  # noqa: E402

AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"
ASSET_CROPS = {"STRAWBERRY", "WHEAT", "MELON"}


def load_module(path=AGENT_MAIN):
    spec = importlib.util.spec_from_file_location("calib_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# pure aggregation (unit-tested)
# --------------------------------------------------------------------------

def day_rows(turn_rows):
    """Collapse per-turn rows into per-day rows.

    turn_rows: {source, episode, seat, day, hands, labor, units} per turn
    ->       [{..., hands=max, labor=sum, units=last}] per (day, seat).
    """
    acc = {}
    order = []
    for row in turn_rows:
        key = (row["source"], row["episode"], row["seat"], row["day"])
        if key not in acc:
            acc[key] = {"source": row["source"], "episode": row["episode"],
                        "seat": row["seat"], "day": row["day"],
                        "hands": 0, "labor": 0, "units": 0.0}
            order.append(key)
        st = acc[key]
        st["hands"] = max(st["hands"], int(row["hands"]))
        st["labor"] += int(row["labor"])
        st["units"] = float(row["units"])
    return [acc[k] for k in order]


def calibrate(rows, high_load_min=0.5):
    """Coefficient statistics from per-day rows (hands/labor/units)."""
    def stats(values):
        if not values:
            return None
        ordered = sorted(values)
        return {"n": len(values),
                "median": round(statistics.median(values), 3),
                "p25": round(ordered[len(ordered) // 4], 3),
                "p75": round(ordered[3 * len(ordered) // 4], 3)}

    def one(sample):
        tpu = [r["labor"] / r["units"] for r in sample if r["units"] > 0]
        eff = [r["labor"] / (24.0 * (1 + r["hands"]))
               for r in sample if r["hands"] >= 0]
        return {"turns_per_unit": stats(tpu), "eff_share": stats(eff)}

    high = [r for r in rows
            if r["units"] > 0 and r["hands"] >= 0
            and r["labor"] / max(1e-9, 24.0 * (1 + r["hands"])) >= high_load_min]
    return {"all_days": one(rows), "high_load": one(high),
            "n_days": len(rows), "n_high_load": len(high)}


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

def collect_local(module, seeds, episode_steps):
    rows = []
    for seed in seeds:
        for name in ("_MISSION_SHADOW", "_ROUTE_STATE", "_STATE", "_TARGETS",
                     "_PLAN_MEM", "_STAGE_MEM", "_MARKET_MEM",
                     "_OPP_OBSERVER", "_INTERFERENCE_LOG"):
            st = getattr(module, name, None)
            if isinstance(st, dict):
                st.clear()
            elif isinstance(st, list):
                del st[:]

        def make_wrapped(module=module, seed=seed):
            # single-arg signature (kaggle runner sizes calls by arity)
            def wrapped(obs):
                action = module.agent(obs)
                try:
                    player = module._get(obs, "player", 0)
                    farm = module._get(obs, "farms",
                                       [{}] * (player + 1))[player]
                    units, _c = module._capacity_units(farm)
                    unit_actions = [action.get("farmer")] + \
                        list(action.get("hands") or [])
                    labor = sum(1 for a in unit_actions
                                if a and a[0] != "PASS")
                    rows.append({"source": f"local-seed{seed}",
                                 "episode": seed, "seat": player,
                                 "day": module._get(obs, "day", 0),
                                 "hands": len(module._get(farm, "hands", [])
                                              or []),
                                 "labor": labor, "units": units})
                except Exception:
                    pass
                return action
            return wrapped

        wrapped = make_wrapped()
        run_episode(wrapped, wrapped, seed, episode_steps=episode_steps)
    return rows


def collect_replays(pattern):
    rows = []
    for path in sorted(glob.glob(pattern)):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        steps = data.get("steps") or []
        for index in range(1, len(steps)):
            step = steps[index]
            obs = (step[0] or {}).get("observation") or {}
            farms = obs.get("farms") or []
            day = int(obs.get("day", 0) or 0)
            for seat in (0, 1):
                if seat >= len(farms) or seat >= len(step):
                    continue
                farm = farms[seat] or {}
                action = (step[seat] or {}).get("action") or {}
                unit_actions = [action.get("farmer")] + \
                    list(action.get("hands") or [])
                labor = sum(1 for a in unit_actions if a and a[0] != "PASS")
                units = 0.0
                for row_tiles in farm.get("tiles") or []:
                    for tile in row_tiles or []:
                        if not isinstance(tile, dict):
                            continue
                        if tile.get("kind") == "PLANT":
                            if tile.get("crop") in ASSET_CROPS:
                                units += 1.0
                            elif tile.get("crop") == "CARROT":
                                units += 0.5
                        elif "animal" in tile:
                            units += 2.0
                rows.append({"source": Path(path).stem,
                             "episode": Path(path).stem,
                             "seat": seat, "day": day,
                             "hands": len(farm.get("hands") or []),
                             "labor": labor, "units": units})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default="7,8")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--replays", default=None,
                    help="glob of official replay JSONs (cross-validation)")
    ap.add_argument("--out", default=str(
        SOFTWARE / "exports" / "probes" / "capacity_calibration.json"))
    args = ap.parse_args()

    sources = {}
    module = load_module()
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    sources["local"] = collect_local(module, seeds, args.episode_steps)
    if args.replays:
        sources["replays"] = collect_replays(args.replays)

    payload = {"schema": "capacity-calibration/1.0",
               "constants_current": {
                   "CAP_TURNS_PER_UNIT": module.CAP_TURNS_PER_UNIT,
                   "CAP_UTIL": module.CAP_UTIL},
               "sources": {}}
    for name, rows in sources.items():
        payload["sources"][name] = calibrate(day_rows(rows))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"[capacity-calibration] -> {out}")


if __name__ == "__main__":
    main()
