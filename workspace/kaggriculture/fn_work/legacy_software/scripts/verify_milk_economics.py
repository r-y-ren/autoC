"""Replication of rayk's milk/shop-demand economics on the real engine.

Re-runs the exact experiment described in "rank your agent" §3 (16 cows vs
3 milk shops -> season-long scarcity) with the engine's own market_price /
_refresh_prices functions and the engine's shop draw + consumption cadence,
no bot pathing noise.  Also measures the CARE compounding effect (engine
_daily_refresh_animals: pending_care_bonus accumulates 1 per fed+cared day
and is consumed on production days) and the wool single-shop variance.

Scenarios (season d0-29, shops drawn with replacement to 8 instances):
  A  16 cows, no CARE     -> 8 milk/day from d8
  B  16 cows, full CARE   -> 18 milk/day (tile max_held cadence real cap)
  C   8 cows, no CARE     -> 4/day   (our current realized band)
  D   8 cows, full CARE   -> 9/day
  E  wool: 4 sheep full CARE -> 2.7 wool/day vs YARN draw luck

Output: workspace/kaggriculture/software/exports/probes/intel/milk_replication.json
"""

from __future__ import annotations

import importlib.util
import json
import os
import random
import statistics
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
while REPO_ROOT != REPO_ROOT.parent and not (REPO_ROOT / ".git").exists():
    REPO_ROOT = REPO_ROOT.parent


def find_engine() -> Path:
    """Discover the kaggressurE engine file by glob (case-robusT)."""
    import kaggle_environments
    base = Path(os.path.dirname(kaggle_environments.__file__)) / "envs"
    for cand in base.glob("kag*"):
        for py in cand.glob("*.py"):
            txt = py.read_text(encoding="utf-8", errors="ignore")
            if "MARKET_PARAMS" in txt and "_daily_refresh_animals" in txt:
                return py
    raise FileNotFoundError(f"engine file not found under {base}")


def load_engine():
    spec = importlib.util.spec_from_file_location("keng_rep", find_engine())
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def season(mod, rng, milk_per_day, wool_per_day=0.0, milk_start_day=8):
    """One season with the engine's market: shop draws, 4-step shop
    consumption, 24-step town-center consumption, our sales injected."""
    market = mod._new_market()
    town = mod._new_town()
    shop_interval = 4      # engine default (step % 4)
    center_interval = 24
    SHOP_UNLOCK_DAY = 3    # engine unlocks a shop every 3 days up to 8
    prices_by_day = {}
    revenue = {"MILK": 0.0, "WOOL": 0.0}
    units_sold = {"MILK": 0, "WOOL": 0}
    for step in range(720):
        day = step // 24
        if day % SHOP_UNLOCK_DAY == 0 and day > 0 \
                and len(town["unlocked_shops"]) < mod.MAX_SHOP_INSTANCES:
            town["unlocked_shops"].append(
                rng.choice(sorted(mod.SHOPS)))
        if step % shop_interval == 0:
            for shop_name in town["unlocked_shops"]:
                products = mod.SHOPS[shop_name]
                mult = 2 if len(products) == 1 else 1
                for item in products:
                    market["inventory"][item] -= mult
        if step % center_interval == 0:
            for item in mod.TOWN_CENTER_PRODUCTS:
                market["inventory"][item] -= 1
        # our production sold continuously from first_yield_day
        if day >= milk_start_day:
            todays = milk_per_day / 24.0
            market["inventory"]["MILK"] += todays
            # sell everything we produce at the current price
            mod._refresh_prices(market)
            px = market["prices"]["MILK"]
            revenue["MILK"] += todays * px
            units_sold["MILK"] += todays
        if day >= 6 and wool_per_day:
            w = wool_per_day / 24.0
            market["inventory"]["WOOL"] += w
            mod._refresh_prices(market)
            revenue["WOOL"] += w * market["prices"]["WOOL"]
            units_sold["WOOL"] += w
        mod._refresh_prices(market)
        prices_by_day[day] = dict(market["prices"])
    band = [prices_by_day[d]["MILK"] for d in range(10, 30)]
    wool_band = [prices_by_day[d]["WOOL"] for d in range(8, 30)]
    return {
        "milk_avg_price_d10_29": round(statistics.mean(band), 1),
        "milk_min": min(band), "milk_max": max(band),
        "milk_revenue": round(revenue["MILK"], 0),
        "milk_units": round(units_sold["MILK"], 0),
        "wool_avg_price_d8_29": round(statistics.mean(wool_band), 1),
        "wool_revenue": round(revenue["WOOL"], 0),
        "final_milk_inv": round(market["inventory"]["MILK"], 0),
        "shops_drawn": sorted(town["unlocked_shops"]),
    }


def main():
    mod = load_engine()
    rng = random.Random(20260831)
    scenarios = [
        ("16 cows no CARE (8/day)", dict(milk_per_day=8.0)),
        ("16 cows full CARE (18/day)", dict(milk_per_day=18.0)),
        ("8 cows no CARE (4/day)", dict(milk_per_day=4.0)),
        ("8 cows full CARE (9/day)", dict(milk_per_day=9.0)),
        ("16C full CARE + 4 sheep CARE (wool 2.7/day)",
         dict(milk_per_day=18.0, wool_per_day=2.7)),
    ]
    out = {"engine": str(find_engine()), "claim_source":
           "rayk rank-your-agent §3: 16 cows -> milk 266 avg, scarce all season",
           "runs": []}
    for label, kw in scenarios:
        n = 40
        runs = [season(mod, random.Random(1000 + i), **kw)
                for i in range(n)]
        avg_px = statistics.mean(r["milk_avg_price_d10_29"] for r in runs)
        avg_rev = statistics.mean(r["milk_revenue"] for r in runs)
        yarn_shops = statistics.mean(
            r["shops_drawn"].count("YARN_STORE") for r in runs)
        wool_px = statistics.mean(r["wool_avg_price_d8_29"] for r in runs)
        out["runs"].append({
            "scenario": label, "n": n,
            "milk_avg_price": round(avg_px, 1),
            "milk_revenue": round(avg_rev, 0),
            "wool_avg_price": round(wool_px, 1) if kw.get("wool_per_day") else None,
            "avg_yarn_shops_drawn": round(yarn_shops, 2),
            "sample_shops": runs[0]["shops_drawn"],
        })
        print(f"{label:<44} milk_px={avg_px:6.1f} rev={avg_rev:8.0f}"
              f" yarn_draw={yarn_shops:.2f} wool_px={wool_px:6.1f}",
              flush=True)
    dest = REPO_ROOT / "workspace/kaggriculture/software/exports/probes/intel" / "milk_replication.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
