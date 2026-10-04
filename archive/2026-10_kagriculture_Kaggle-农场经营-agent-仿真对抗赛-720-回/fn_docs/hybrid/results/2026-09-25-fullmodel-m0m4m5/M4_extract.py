#!/usr/bin/env python3
"""M4 winner-production-line structural extraction (research round, /tmp only).

Per episode, per seat, produces a full d0-d29 daily timeline:
  - investment: quadrant unlocks, animal buys (per species), hires (successes),
    pasture/coop builds, seed buys, external feed (BUY_PRODUCT WHEAT/FERT)
  - income: exact per-item sell revenue (lockstep-simulated, engine-exact),
    expenses by category, day-end money (from replay obs, ground truth)
Uses kgenv.replay_profile's validated engine re-simulation (_s_* functions).
"""
import sys, os, json, copy, glob, time
from collections import Counter, defaultdict

sys.path.insert(0, '/mnt/data/Code/autoC/workspace/kaggriculture/software')
import kgenv.replay_profile as rp

HOURS = 24
DAYS = 30
ANIMALS = {"COW", "SHEEP", "GOOSE"}
CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
PRODUCT_LINES = {  # product -> line
    "WHEAT": "crops", "CARROT": "crops", "TOMATO": "crops",
    "STRAWBERRY": "crops", "MELON": "crops",
    "MILK": "dairy", "WOOL": "wool", "EGG": "eggs", "FERTILIZER": "fertilizer",
}

def tile_counts(tiles):
    c = Counter()
    if not isinstance(tiles, list): return c
    for row in tiles:
        if not isinstance(row, list): continue
        for t in row:
            if isinstance(t, dict):
                k = t.get("kind")
                if k == "PLANT": c["crop:" + str(t.get("crop"))] += 1
                elif k in ("PASTURE", "COOP"): c[k] += 1
                elif k == "WEED": c["WEED"] += 1
                elif k == "SHED": c["SHED"] += 1
            elif t == "LOCKED": c["LOCKED"] += 1
    return c

def extract(path):
    with open(path) as f:
        replay = json.load(f)
    steps = replay.get("steps") or []
    if len(steps) < rp.EXPECTED_STEPS:
        return None
    info = replay.get("info") or {}
    teams = list(info.get("TeamNames") or ["?", "?"])
    rewards = list(replay.get("rewards") or [None, None])
    statuses = list(replay.get("statuses") or [])
    ep = info.get("EpisodeId")
    cfg = rp._s_config(replay)
    seed = info.get("seed") or (replay.get("configuration") or {}).get("seed") or 0

    seats = []
    for pl in (0, 1):
        seats.append({
            "team": teams[pl] if pl < len(teams) else "?",
            "reward": rewards[pl] if pl < len(rewards) else None,
            "money_end": [None] * DAYS,
            "income_item": [defaultdict(float) for _ in range(DAYS)],   # exact sim
            "spend": [defaultdict(float) for _ in range(DAYS)],
            "animal_buys_day": [defaultdict(int) for _ in range(DAYS)],
            "hires_day": [0] * DAYS,
            "hire_spend_day": [0.0] * DAYS,
            "land_buy_day": {},          # quadrant -> day
            "quad_day": {},              # quadrant -> first-day-seen (obs)
            "herd_day": [None] * DAYS,   # {COW,SHEEP,GOOSE}
            "crop_tiles_day": [None] * DAYS,
            "build_day": [defaultdict(int) for _ in range(DAYS)],  # PASTURE/COOP builds
            "feed_day": [0] * DAYS,      # FEED successes
            "care_day": [0] * DAYS,
            "seed_buys_day": [defaultdict(int) for _ in range(DAYS)],
            "buy_wheat_day": [0] * DAYS,   # BUY_PRODUCT WHEAT units
            "buy_fert_day": [0] * DAYS,    # BUY_PRODUCT FERTILIZER units
            "sell_units_item": [defaultdict(int) for _ in range(DAYS)],
        })

    # --- observation scan: money curve, quadrants, day-end tiles ---
    quad_seen = [set(), set()]
    for t, step in enumerate(steps):
        obs = (step[0].get("observation") or {})
        day = t // HOURS
        hour = obs.get("hour")
        farms = obs.get("farms") or []
        for pl in (0, 1):
            if pl >= len(farms) or pl >= len(step): continue
            farm = farms[pl] or {}
            for q in farm.get("unlocked_quadrants") or []:
                if q not in quad_seen[pl]:
                    quad_seen[pl].add(q)
                    seats[pl]["quad_day"][q] = day
            if t % HOURS == HOURS - 1:  # hour 23 snapshot (pre-rollover)
                pass
        # day-end sample: obs at t=(d+1)*24 shows state after day d's last action
        # day 29 (last day) has no t=720; use the final obs t=719 (hour 23)
        if (t % HOURS == 0 and t > 0) or t == len(steps) - 1:
            d = (t // HOURS - 1) if t % HOURS == 0 else DAYS - 1
            for pl in (0, 1):
                if pl >= len(farms): continue
                farm = farms[pl] or {}
                m = farm.get("money")
                seats[pl]["money_end"][d] = float(m) if isinstance(m, (int, float)) else None
                tiles = farm.get("tiles")
                herd = Counter()
                crops = Counter()
                if isinstance(tiles, list):
                    for row in tiles:
                        if not isinstance(row, list): continue
                        for tt in row:
                            if isinstance(tt, dict):
                                if tt.get("kind") in ("PASTURE", "COOP"):
                                    herd[str(tt.get("animal"))] += 1
                                elif tt.get("kind") == "PLANT":
                                    crops[str(tt.get("crop"))] += 1
                seats[pl]["herd_day"][d] = dict(herd)
                seats[pl]["crop_tiles_day"][d] = dict(crops)
    # final money from rewards
    for pl in (0, 1):
        seats[pl]["money_end"][DAYS - 1] = float(rewards[pl]) if rewards[pl] is not None else seats[pl]["money_end"][DAYS - 2]

    # --- validated lockstep simulation for exact money flows ---
    state = rp._s_snapshot(
        steps[0][0].get("observation") or {},
        [steps[0][0].get("observation", {}).get("private"),
         steps[0][1].get("observation", {}).get("private")])
    drift = 0
    for t in range(1, len(steps)):
        actions = [steps[t][pl].get("action") or {} for pl in (0, 1)]
        pre_obs = steps[t - 1][0].get("observation") or {}
        step_index = int(pre_obs.get("step", t - 1))
        post_state, attr = rp._s_step(state, actions, step_index, cfg, seed)
        actual0 = steps[t][0].get("observation") or {}
        actual_priv = [steps[t][0].get("observation", {}).get("private"),
                       steps[t][1].get("observation", {}).get("private")]
        diff = rp._s_compare(post_state, actual0, actual_priv)
        if diff:
            drift += 1
            state = rp._s_snapshot(actual0, actual_priv)
        else:
            state = post_state
        day = step_index // HOURS
        for pl in (0, 1):
            s = seats[pl]
            # hire accounting
            h = attr["market"][pl]["hire"]
            if h["successes"]:
                s["hires_day"][day] += h["successes"]
                s["hire_spend_day"][day] += h["spend"]
            bl = attr["market"][pl]["buy_land"]
            if bl["successes"]:
                # record quadrant bought this day
                s["land_buy_day"][day] = s["land_buy_day"].get(day, 0) + bl["successes"]
            # orders
            for o in attr["market"][pl]["orders"]:
                typ, item = o["type"], o.get("item")
                filled, value = o.get("filled", 0), o.get("value", 0.0)
                if typ == "SELL" and filled:
                    s["income_item"][day][item] += value
                    s["sell_units_item"][day][item] += filled
                elif typ == "BUY_ANIMAL" and filled:
                    s["animal_buys_day"][day][item] += filled
                    s["spend"][day]["animals"] += value
                elif typ == "BUY_SEED" and filled:
                    s["seed_buys_day"][day][item] += filled
                    s["spend"][day]["seeds"] += value
                elif typ == "BUY_PRODUCT" and filled:
                    if item == "WHEAT":
                        s["buy_wheat_day"][day] += filled
                        s["spend"][day]["feed_wheat"] += value
                    else:
                        s["buy_fert_day"][day] += filled
                        s["spend"][day]["fert"] += value
                elif typ == "HIRE":
                    pass
            # unit ops: FEED/CARE successes, BUILD_*
            u = attr["unit"][pl]
            s["feed_day"][day] += u["success"].get("FEED", 0)
            s["care_day"][day] += u["success"].get("CARE", 0)
            s["build_day"][day]["PASTURE"] += u["success"].get("BUILD_PASTURE", 0)
            s["build_day"][day]["COOP"] += u["success"].get("BUILD_COOP", 0)
            s["spend"][day]["hire"] += attr["market"][pl]["hire"]["spend"]
            s["spend"][day]["land"] += attr["market"][pl]["buy_land"]["spend"]

    # --- derived curves ---
    for s in seats:
        s["income_total_day"] = [round(sum(v.values()), 1) for v in s["income_item"]]
        s["income_line_day"] = []
        for d in range(DAYS):
            lines = defaultdict(float)
            for item, v in s["income_item"][d].items():
                lines[PRODUCT_LINES.get(item, "other")] += v
            s["income_line_day"].append({k: round(v, 1) for k, v in lines.items()})
        s["income_cum"] = []
        run = 0.0
        for d in range(DAYS):
            run += s["income_total_day"][d]
            s["income_cum"].append(round(run, 1))
        s["cum_animals"] = []
        cums = defaultdict(int)
        for d in range(DAYS):
            for a, n in s["animal_buys_day"][d].items():
                cums[a] += n
            s["cum_animals"].append(dict(cums))
        s["cum_builds"] = []
        cb = defaultdict(int)
        for d in range(DAYS):
            for b, n in s["build_day"][d].items():
                cb[b] += n
            s["cum_builds"].append(dict(cb))
        s["cum_hires"] = []
        ch = 0
        for d in range(DAYS):
            ch += s["hires_day"][d]
            s["cum_hires"].append(ch)
        # cleanup non-serializable leftovers
        s.pop("income_item", None)

    return {
        "episode_id": ep, "teams": teams, "rewards": rewards,
        "statuses": statuses, "seed": seed, "sim_drift_steps": drift,
        "seats": seats,
    }

def main():
    srcs = sys.argv[1:-1]
    out = sys.argv[-1]
    results = []
    t0 = time.time()
    for path in srcs:
        try:
            r = extract(path)
        except Exception as e:
            print(f"ERR {path}: {e}", file=sys.stderr)
            continue
        if r is None:
            print(f"SKIP {path} (bad steps)", file=sys.stderr)
            continue
        r["source"] = path
        results.append(r)
        print(f"{r['episode_id']} drift={r['sim_drift_steps']} "
              f"rewards={r['rewards']} ({time.time()-t0:.0f}s)", flush=True)
    with open(out, "w") as f:
        json.dump(results, f)
    print(f"total {len(results)} games -> {out}, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
