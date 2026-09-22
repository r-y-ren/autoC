"""Pure per-episode, per-player profile extraction from Kaggriculture replays.

Input : a replay JSON as produced by kaggle-environments 1.32.7 kaggriculture
        (top-level ``info.TeamNames``/``rewards``/``statuses``/``steps``).
Output: a plain-dict profile (JSON-serialisable) describing each player's
        money curve, herd trajectory, crop rotation, hire intensity, external
        feed purchases, realised sell price distribution and endgame dump.

The module is pure: no network, no filesystem mutation, no global state.
Every monetary flow derived from actions uses the market price quoted at the
decision step (``observation.market.prices``) and is labelled as ``quoted_*``;
ground-truth cash flow comes from the ``money`` curve deltas (exact).

Documented game facts the extractor relies on (verified against the vendored
kaggle_environments 1.32.7 source):
  * 720 steps == 30 days x 24 hours; ``observation.day``/``hour``.
  * ``farms[pl].tiles`` is a 10x10 nested list; cells are ``null``,
    the string ``'LOCKED'`` or dicts with ``kind`` in
    {PLANT, PASTURE, COOP, WEED, SHED}.
  * market ops: BUY_SEED, BUY_PRODUCT, BUY_ANIMAL, SELL, HIRE, BUY_LAND.
  * animals eat WHEAT (FEED takes 1 WHEAT from inventory), so external feed
    purchases == ``BUY_PRODUCT`` of WHEAT.
"""

from __future__ import annotations

import copy
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROTOCOL = "replay-profile/1.0"

EXPECTED_STEPS = 720
HOURS_PER_DAY = 24
DAYS = EXPECTED_STEPS // HOURS_PER_DAY  # 30
ENDGAME_START_STEP = (DAYS - 2) * HOURS_PER_DAY  # final 48h dump window
CROP_ITEMS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMAL_PRODUCTS = {"MILK", "WOOL", "EGG"}
PRODUCTS = CROP_ITEMS | ANIMAL_PRODUCTS | {"FERTILIZER"}
FEED_ITEM = "WHEAT"


class IntegrityError(ValueError):
    """Raised by strict extraction when a replay fails integrity checks."""


# --------------------------------------------------------------------------- #
# loading & integrity
# --------------------------------------------------------------------------- #
def load_replay(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check_integrity(replay: dict) -> list[str]:
    """Return a list of integrity issues (empty list == clean episode).

    Clean means: both seats DONE, exactly EXPECTED_STEPS steps, both teams
    named, numeric rewards. Anything else disqualifies the episode from the
    profile corpus (the caller must log the exclusion reason).
    """
    issues: list[str] = []
    info = replay.get("info") or {}
    teams = info.get("TeamNames")
    if not isinstance(teams, list) or len(teams) != 2 or any(
        not isinstance(t, str) or not t for t in teams
    ):
        issues.append("bad TeamNames")
    statuses = replay.get("statuses")
    if not isinstance(statuses, list) or len(statuses) != 2 or any(
        s != "DONE" for s in statuses
    ):
        issues.append(f"statuses={statuses}")
    steps = replay.get("steps")
    if not isinstance(steps, list) or len(steps) != EXPECTED_STEPS:
        issues.append(f"steps={len(steps) if isinstance(steps, list) else 'missing'}")
    rewards = replay.get("rewards")
    if not isinstance(rewards, list) or len(rewards) != 2 or any(
        not isinstance(r, (int, float)) or math.isnan(r) for r in rewards
    ):
        issues.append(f"rewards={rewards}")
    if isinstance(steps, list) and steps:
        for pl in (0, 1):
            if len(steps[0]) <= pl or not isinstance(steps[0][pl], dict):
                issues.append(f"seat{pl} malformed")
    return issues


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def _tile_counts(tiles: Any) -> dict[str, int]:
    """Aggregate a 10x10 tile grid into kind counts (+crop/animal splits)."""
    counts: dict[str, int] = {}
    if not isinstance(tiles, list):
        return counts
    for row in tiles:
        if not isinstance(row, list):
            continue
        for cell in row:
            if cell is None:
                counts["EMPTY"] = counts.get("EMPTY", 0) + 1
            elif isinstance(cell, str):
                counts[cell] = counts.get(cell, 0) + 1
            elif isinstance(cell, dict):
                kind = cell.get("kind", "?")
                if kind == "PLANT":
                    crop = cell.get("crop", "?")
                    counts[f"PLANT:{crop}"] = counts.get(f"PLANT:{crop}", 0) + 1
                elif kind in ("PASTURE", "COOP"):
                    if "animal" in cell:
                        counts[f"{kind}:{cell['animal']}"] = (
                            counts.get(f"{kind}:{cell['animal']}", 0) + 1
                        )
                    else:
                        counts[kind] = counts.get(kind, 0) + 1
                else:
                    counts[kind] = counts.get(kind, 0) + 1
    return counts


def _herd_from_counts(counts: dict[str, int]) -> dict[str, int]:
    herd = {}
    for key, n in counts.items():
        if key.startswith(("PASTURE:", "COOP:")):
            animal = key.split(":", 1)[1]
            herd[animal] = herd.get(animal, 0) + n
        elif key in ("PASTURE", "COOP"):
            # built structure with no animal placed (awaiting PLACE, or the
            # animal escaped after >=2 unfed days - env keeps the structure)
            herd["EMPTY_STRUCTURE"] = herd.get("EMPTY_STRUCTURE", 0) + n
    return herd


def _crops_from_counts(counts: dict[str, int]) -> dict[str, int]:
    return {
        key.split(":", 1)[1]: n
        for key, n in counts.items()
        if key.startswith("PLANT:")
    }


def _pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, round(q * (len(s) - 1))))
    return float(s[idx])


def _sell_summary(events: list[dict]) -> dict:
    """Per-item sell stats over a list of {item, qty, price} events."""
    per_item: dict[str, list[dict]] = {}
    for e in events:
        per_item.setdefault(e["item"], []).append(e)
    out = {}
    for item, evs in per_item.items():
        qty = sum(e["qty"] for e in evs)
        prices = [e["price"] for e in evs]
        out[item] = {
            "orders": len(evs),
            "qty": qty,
            "quoted_revenue": round(sum(e["qty"] * e["price"] for e in evs), 1),
            "price_avg": round(statistics.fmean(prices), 1),
            "price_min": min(prices),
            "price_median": round(statistics.median(prices), 1),
            "price_max": max(prices),
        }
    return out


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #
def extract_episode_profiles(
    replay: dict,
    episode_id: int | None = None,
    source_url: str = "",
    capture_date: str = "",
    strict: bool = True,
) -> dict:
    """Extract both players' profiles from one replay dict.

    strict=True raises IntegrityError when check_integrity finds issues;
    strict=False still extracts but marks ``integrity_issues`` in the output
    (used for diagnostic/dump inspection, never for the official corpus).
    """
    issues = check_integrity(replay)
    if issues and strict:
        raise IntegrityError("; ".join(issues))

    info = replay.get("info") or {}
    teams = list(info.get("TeamNames") or ["?", "?"])
    statuses = list(replay.get("statuses") or [])
    rewards = list(replay.get("rewards") or [None, None])
    steps = replay["steps"]
    if episode_id is None:
        episode_id = info.get("EpisodeId")

    players = [_init_player(pl, teams, statuses, rewards) for pl in (0, 1)]
    quadrant_days: list[dict[str, int]] = [{}, {}]
    seen_quadrants: list[set[str]] = [set(), set()]

    for t, step in enumerate(steps):
        for pl in (0, 1):
            entry = step[pl]
            obs = entry.get("observation") or {}
            farms = obs.get("farms") or []
            if len(farms) <= pl:
                continue
            farm = farms[pl] or {}
            p = players[pl]
            money = farm.get("money")
            if isinstance(money, (int, float)):
                p["money_curve"].append((t, float(money)))
            # quadrant unlocks (record first day seen)
            for q in farm.get("unlocked_quadrants") or []:
                if q not in seen_quadrants[pl]:
                    seen_quadrants[pl].add(q)
                    quadrant_days[pl][q] = t // HOURS_PER_DAY
            # day-end sampling (hour==23 or final step)
            hour = obs.get("hour")
            is_day_end = hour == HOURS_PER_DAY - 1 or t == len(steps) - 1
            if is_day_end:
                day = obs.get("day", t // HOURS_PER_DAY)
                counts = _tile_counts(farm.get("tiles"))
                p["herd_by_day"].append((day, _herd_from_counts(counts)))
                p["crops_by_day"].append((day, _crops_from_counts(counts)))
                p["hires_by_day"].append((day, int(farm.get("hires_today") or 0)))
            # market actions
            prices = (obs.get("market") or {}).get("prices") or {}
            for act in (entry.get("action") or {}).get("market") or []:
                if not isinstance(act, list) or not act:
                    continue
                op = act[0]
                p["op_counts"][op] = p["op_counts"].get(op, 0) + 1
                if op == "SELL" and len(act) >= 3 and act[1] in prices:
                    item, qty = act[1], int(act[2])
                    p["sell_events"].append(
                        {"t": t, "item": item, "qty": qty, "price": float(prices[item])}
                    )
                elif op == "BUY_PRODUCT" and len(act) >= 3 and act[1] in prices:
                    item, qty = act[1], int(act[2])
                    p["buy_product_events"].append(
                        {"t": t, "item": item, "qty": qty, "price": float(prices[item])}
                    )
                elif op == "BUY_SEED" and len(act) >= 3:
                    p["seed_buys"][act[1]] = p["seed_buys"].get(act[1], 0) + int(act[2])
                elif op == "BUY_ANIMAL" and len(act) >= 3:
                    p["animal_buys"][act[1]] = p["animal_buys"].get(act[1], 0) + int(
                        act[2]
                    )

    profiles = []
    for pl in (0, 1):
        profiles.append(
            _finalise_player(
                players[pl],
                quadrant_days[pl],
                steps,
                episode_id,
                teams,
                rewards,
                source_url,
                capture_date,
                issues,
            )
        )
    return {
        "protocol": PROTOCOL,
        "episode": {
            "episode_id": episode_id,
            "teams": teams,
            "rewards": rewards,
            "statuses": statuses,
            "steps": len(steps),
            "seed": info.get("seed"),
            "source_url": source_url,
            "capture_date": capture_date,
            "integrity_issues": issues,
        },
        "players": profiles,
    }


def _init_player(pl: int, teams, statuses, rewards) -> dict:
    return {
        "seat": pl,
        "team": teams[pl] if pl < len(teams) else "?",
        "opponent": teams[1 - pl] if 1 - pl < len(teams) else "?",
        "status": statuses[pl] if pl < len(statuses) else None,
        "reward": rewards[pl] if pl < len(rewards) else None,
        "money_curve": [],
        "herd_by_day": [],
        "crops_by_day": [],
        "hires_by_day": [],
        "sell_events": [],
        "buy_product_events": [],
        "seed_buys": {},
        "animal_buys": {},
        "op_counts": {},
    }


def _finalise_player(
    p: dict,
    quadrant_days: dict[str, int],
    steps: list,
    episode_id,
    teams,
    rewards,
    source_url,
    capture_date,
    issues: list[str],
) -> dict:
    money = p["money_curve"]
    final_money = money[-1][1] if money else None
    opening_money = money[0][1] if money else None
    min_money = min((m for _, m in money), default=None)

    # daily net cash flow (money delta per day index)
    day_last: dict[int, float] = {}
    for t, m in money:
        day_last[t // HOURS_PER_DAY] = m
    net_by_day = {}
    prev = opening_money
    for d in sorted(day_last):
        net_by_day[d] = round(day_last[d] - (prev if prev is not None else day_last[d]), 1)
        prev = day_last[d]

    sells = p["sell_events"]
    sells_endgame = [e for e in sells if e["t"] >= ENDGAME_START_STEP]
    sell_all = _sell_summary(sells)
    sell_end = _sell_summary(sells_endgame)
    total_quoted = sum(v["quoted_revenue"] for v in sell_all.values())
    end_quoted = sum(v["quoted_revenue"] for v in sell_end.values())

    # revenue split crops vs animal products (quoted)
    crop_rev = sum(
        v["quoted_revenue"] for k, v in sell_all.items() if k in CROP_ITEMS
    )
    animal_rev = sum(
        v["quoted_revenue"] for k, v in sell_all.items() if k in ANIMAL_PRODUCTS
    )
    fert_rev = sell_all.get("FERTILIZER", {}).get("quoted_revenue", 0)

    buys = p["buy_product_events"]
    feed_events = [e for e in buys if e["item"] == FEED_ITEM]
    feed_qty = sum(e["qty"] for e in feed_events)
    feed_avg = round(statistics.fmean([e["price"] for e in feed_events]), 1) if feed_events else None

    # crop field occupancy integral (tile-days) -> rotation share
    crop_tile_days: dict[str, int] = {}
    for _day, crops in p["crops_by_day"]:
        for c, n in crops.items():
            crop_tile_days[c] = crop_tile_days.get(c, 0) + n
    total_tile_days = sum(crop_tile_days.values())

    hires = [h for _, h in p["hires_by_day"]]
    end_counts_day = p["crops_by_day"][-1][1] if p["crops_by_day"] else {}
    # rebuild full end tile composition needs raw counts; approximate from herd+crops
    won = None
    if (
        p["reward"] is not None
        and isinstance(rewards[1 - p["seat"]], (int, float))
    ):
        won = p["reward"] > rewards[1 - p["seat"]]

    money_at_dump_start = None
    for t, m in money:
        if t >= ENDGAME_START_STEP:
            money_at_dump_start = m
            break
    endgame_gain = (
        round(final_money - money_at_dump_start, 1)
        if final_money is not None and money_at_dump_start is not None
        else None
    )
    if final_money:
        endgame_gain_pct = (
            round(100.0 * endgame_gain / final_money, 1)
            if endgame_gain is not None
            else None
        )
    else:
        endgame_gain_pct = None

    return {
        "protocol": PROTOCOL,
        "episode_id": episode_id,
        "seat": p["seat"],
        "team": p["team"],
        "opponent": p["opponent"],
        "status": p["status"],
        "reward": p["reward"],
        "won": won,
        "source_url": source_url,
        "capture_date": capture_date,
        "integrity_issues": issues,
        # --- money ---
        "money": {
            "opening": opening_money,
            "final": final_money,
            "min": min_money,
            "curve_step_money": [[t, round(m, 1)] for t, m in money[::HOURS_PER_DAY]],
            "net_cash_by_day": net_by_day,
        },
        # --- herd ---
        "herd": {
            "by_day": [
                {"day": d, **herd} for d, herd in p["herd_by_day"]
            ],
            "final": p["herd_by_day"][-1][1] if p["herd_by_day"] else {},
            "animal_buys": p["animal_buys"],
        },
        # --- crops ---
        "crops": {
            "by_day": [{"day": d, **c} for d, c in p["crops_by_day"]],
            "final": end_counts_day,
            "tile_day_share": {
                c: round(n / total_tile_days, 3)
                for c, n in sorted(
                    crop_tile_days.items(), key=lambda kv: -kv[1]
                )
            }
            if total_tile_days
            else {},
            "seed_buys": p["seed_buys"],
        },
        # --- labour ---
        "hires": {
            "by_day": [h for _, h in p["hires_by_day"]],
            "total": sum(hires),
            "avg_per_day": round(statistics.fmean(hires), 2) if hires else 0.0,
            "max_day": max(hires) if hires else 0,
        },
        # --- external inputs ---
        "external_buys": {
            "feed_item": FEED_ITEM,
            "feed_qty": feed_qty,
            "feed_avg_price": feed_avg,
            "buy_product_qty_by_item": _buy_qty_summary(buys),
            "fertilizer_qty": sum(
                e["qty"] for e in buys if e["item"] == "FERTILIZER"
            ),
        },
        # --- selling ---
        "sells": {
            "per_item": sell_all,
            "endgame_per_item": sell_end,
            "total_quoted_revenue": round(total_quoted, 1),
            "crop_quoted_revenue": round(crop_rev, 1),
            "animal_quoted_revenue": round(animal_rev, 1),
            "fertilizer_quoted_revenue": round(fert_rev, 1),
            "endgame_quoted_revenue": round(end_quoted, 1),
            "endgame_revenue_share": round(end_quoted / total_quoted, 3)
            if total_quoted
            else 0.0,
            "orders_total": len(sells),
        },
        # --- endgame dump ---
        "endgame": {
            "start_step": ENDGAME_START_STEP,
            "money_at_start": money_at_dump_start,
            "money_final": final_money,
            "gain": endgame_gain,
            "gain_pct_of_final": endgame_gain_pct,
        },
        # --- land ---
        "land": {
            "quadrant_unlock_day": quadrant_days,
            "quadrants_final": len(quadrant_days),
        },
        "op_counts": p["op_counts"],
    }


def _buy_qty_summary(buys: list[dict]) -> dict:
    out: dict[str, dict] = {}
    for e in buys:
        s = out.setdefault(e["item"], {"qty": 0, "price_avg": []})
        s["qty"] += e["qty"]
        s["price_avg"].append(e["price"])
    return {
        k: {
            "qty": v["qty"],
            "price_avg": round(statistics.fmean(v["price_avg"]), 1),
        }
        for k, v in out.items()
    }


def extract_profiles_from_file(
    path: str | Path,
    episode_id: int | None = None,
    source_url: str = "",
    capture_date: str = "",
    strict: bool = True,
) -> dict:
    return extract_episode_profiles(
        load_replay(path),
        episode_id=episode_id,
        source_url=source_url,
        capture_date=capture_date,
        strict=strict,
    )


# =========================================================================== #
# Success-caliber measurement (campaign III r3-P0)
# =========================================================================== #
#
# Request caliber (previous sections + replay_deep_stats.py) counts what the
# agent ASKED for; the engine silently no-ops illegal or unaffordable requests.
# This section measures what actually HAPPENED, from observation state
# transitions, not from the action list.
#
# Method: for every recorded step t (kaggle replay semantics: steps[t].action
# is the action the agent chose from steps[t-1].observation, and steps[t].
# observation is the state AFTER the interpreter applied it), we replay the
# interpreter semantics locally on a copy of the pre-state ("shadow"), which
# yields exact per-request attribution (which CARE flipped cared_today, which
# SELL unit committed at which price, which HIRE was silently rejected).  The
# shadow's predicted post-state is then compared field-by-field against the
# REAL post observation; any mismatch is recorded as an integrity issue and
# the shadow resynchronises from the real state.  Success counts therefore
# always trace back to observed state transitions - the shadow only
# attributes them - and every episode carries an integrity verdict
# (attribution_valid == mismatches == 0).
#
# The port below mirrors the vendored kaggle-environments 1.32.7
# kaggriculture interpreter (unit action application order, per-column market
# lockstep with per-column price refresh, town consumption, plant decay,
# end-of-day refresh with the seeded RNG, shed-capacity discards).  It is
# pure stdlib; tests/test_replay_success.py cross-validate it against real
# engine-generated replays (zero tolerated mismatches).
#
# Engine facts this section relies on (vendored 1.32.7 source):
#   * unit ops: farmer first, then hands in order; invalid actions are no-ops.
#   * CARE/FEED/WATER flip a per-day tile flag; a second op on the same tile
#     the same day is a no-op ("already served").
#   * FEED additionally consumes 1 WHEAT from that unit's inventory.
#   * HARVEST moves yield_units into the acting unit's inventory (0 units ->
#     no-op).
#   * HIRE cost = fib(hires_today) (1,1,2,3,5,...); silently rejected when
#     money < cost; hands are cleared and re-hired every day.
#   * market: per order-column, HIRE/BUY_LAND resolve first (player order),
#     then SELL/BUY_* fill ONE unit per lockstep round at live prices
#     (market impact within a single order), aborting the order on the first
#     rejected unit; prices refresh after every column.
#   * animal with consecutive_unfed >= 2 escapes at end-of-day (structure
#     remains); plant with consecutive_unwatered >= 2 weeds out; non-ongoing
#     crops also decay to WEED past max_lifespan_step (yield -1 per 2 steps).
#   * end-of-day drops every unit inventory into the shed up to
#     shedCapacity=100; the overflow is silently discarded.
#   * rng: random.Random((seed * 1_000_003) ^ day) drives weed spawns and the
#     town shop draw, shared across both players in player order.

SUCCESS_PROTOCOL = "replay-success/1.0"

S_CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
S_ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
S_PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
S_PRICE_FLOOR = 1
S_HINGE_GAIN = 8.0
S_MARKET_I0 = 10000
S_MARKET_PARAMS = {
    "WHEAT":      {"base": 25,  "I0": S_MARKET_I0, "T": 400, "below_func": "sqrt",  "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":     {"base": 35,  "I0": S_MARKET_I0, "T": 450, "below_func": "hinge", "below_target": 1.00, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":     {"base": 60,  "I0": S_MARKET_I0, "T": 200, "below_func": "hinge", "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": S_MARKET_I0, "T": 100, "below_func": "sqrt",  "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "I0": S_MARKET_I0, "T": 300, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":        {"base": 50,  "I0": S_MARKET_I0, "T": 332, "below_func": "hinge", "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":       {"base": 160, "I0": S_MARKET_I0, "T": 122, "below_func": "sqrt",  "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "I0": S_MARKET_I0, "T": 105, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": S_MARKET_I0, "T": 200, "below_func": "linear","below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}
S_FARMER_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
S_LAND_ORDER = ["NE", "SW", "SE"]
S_LAND_PRICES = [1000, 2000, 4000]
S_SHOPS = {
    "BAKERY": ["EGG", "WHEAT"],
    "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
S_TOWN_CENTER_PRODUCTS = [p for p in S_PRODUCTS if p != "FERTILIZER"]
S_MAX_SHOP_INSTANCES = 8
S_DEFAULT_CONFIG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}
# failure classes used across the op tables
S_FAILS = {
    "CARE": ("already_served", "wrong_target"),
    "FEED": ("already_served", "wrong_target", "no_resource"),
    "WATER": ("already_served", "wrong_target"),
    "HARVEST": ("no_yield", "wrong_target"),
    "PLANT": ("no_resource", "wrong_target"),
    "DIG": ("wrong_target",),   # v7: weed-reclaim calibre needs DIG visible
}
S_UNIT_OPS_TRACKED = ("CARE", "FEED", "WATER", "HARVEST", "PLANT", "DIG",
                      "PLACE", "BUILD_COOP", "BUILD_PASTURE", "FERTILIZE",
                      "COLLECT_FERTILIZER", "PICKUP", "DROP")


def _s_shape(func: str, x, T=None):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "log10":
        return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + S_HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def _s_market_price(item: str, inventory) -> int:
    p = S_MARKET_PARAMS[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _s_shape(f, T, T)
        price = base + amp * _s_shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _s_shape(f, T, T)
        price = base - amp * _s_shape(f, inventory - I0, T)
    return max(S_PRICE_FLOOR, int(round(price)))


def _s_refresh_prices(market: dict) -> None:
    for item in S_PRODUCTS:
        market["prices"][item] = _s_market_price(item, market["inventory"][item])


def _s_fib(n: int) -> int:
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _s_hire_cost(n_already_today: int, mult: int = 1) -> int:
    return mult * _s_fib(n_already_today)


def _s_quadrant_of(x: int, y: int, board_size: int) -> str:
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _s_shed_access_tiles(board_size: int):
    half = board_size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _s_is_shed_adjacent(pos, board_size: int) -> bool:
    return tuple(pos) in {t for t in _s_shed_access_tiles(board_size)}


def _s_default_spawn(board_size: int):
    for tile in _s_shed_access_tiles(board_size):
        if _s_quadrant_of(tile[0], tile[1], board_size) == "NW":
            return tile
    return (0, 0)


def _s_new_plant(crop: str, day: int, turns_per_day: int) -> dict:
    cd = S_CROPS[crop]
    return {
        "kind": "PLANT", "crop": crop, "planted_day": day,
        "watered_today": False, "consecutive_unwatered": 1,
        "yield_units": 0 if cd["ongoing"] else 1,
        "max_lifespan_step": (-1 if cd["ongoing"]
                              else (day + cd["max_yield_day"] + 1) * turns_per_day),
        "fertilized_until_day": -1,
    }


def _s_new_animal(animal: str, day: int) -> dict:
    return {
        "kind": S_ANIMALS[animal]["structure"], "animal": animal,
        "placed_day": day, "yield_units": 0, "consecutive_unfed": 0,
        "fed_today": False, "cared_today": False,
        "fertilizer_available": False, "pending_care_bonus": 0,
    }


def _s_spawn_hand(farm: dict, board_size: int):
    tiles = _s_shed_access_tiles(board_size)
    occupants = {tile: 0 for tile in tiles}
    for pos in [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]:
        if pos in occupants:
            occupants[pos] += 1
    best = sorted(occupants.items(),
                  key=lambda kv: (kv[1], tiles.index(kv[0])))
    return list(best[0][0])


# --------------------------------------------------------------------------- #
# state snapshots & comparison
# --------------------------------------------------------------------------- #
def _s_snapshot(obs0: dict, privates) -> dict:
    """Plain-dict working state from an observation pair."""
    return {
        "farms": copy.deepcopy(obs0.get("farms") or []),
        "market": copy.deepcopy(obs0.get("market") or {}),
        "town": copy.deepcopy(obs0.get("town") or {}),
        "privates": [copy.deepcopy(p or {}) for p in privates],
    }


def _s_compare(predicted: dict, actual_obs0: dict, actual_privates) -> list[str]:
    """Field names where the shadow prediction diverges from the replay."""
    out = []
    farms_a = actual_obs0.get("farms") or []
    for pl, farm_p in enumerate(predicted["farms"]):
        if pl >= len(farms_a):
            out.append(f"farms[{pl}].missing")
            continue
        farm_a = farms_a[pl] or {}
        if farm_p.get("money") != farm_a.get("money"):
            out.append(f"farms[{pl}].money")
        if farm_p.get("farmer") != farm_a.get("farmer"):
            out.append(f"farms[{pl}].farmer")
        if farm_p.get("hands") != farm_a.get("hands"):
            out.append(f"farms[{pl}].hands")
        if farm_p.get("unlocked_quadrants") != farm_a.get("unlocked_quadrants"):
            out.append(f"farms[{pl}].quadrants")
        if farm_p.get("hires_today") != farm_a.get("hires_today"):
            out.append(f"farms[{pl}].hires_today")
        if farm_p.get("tiles") != farm_a.get("tiles"):
            out.append(f"farms[{pl}].tiles")
    market_a = actual_obs0.get("market") or {}
    if predicted["market"].get("inventory") != market_a.get("inventory"):
        out.append("market.inventory")
    if predicted["market"].get("prices") != market_a.get("prices"):
        out.append("market.prices")
    if predicted["town"].get("unlocked_shops") != (actual_obs0.get("town") or {}).get("unlocked_shops"):
        out.append("town.shops")
    for pl, private_p in enumerate(predicted["privates"]):
        private_a = actual_privates[pl] or {}
        if private_p.get("shed") != private_a.get("shed"):
            out.append(f"private[{pl}].shed")
        if private_p.get("seeds") != private_a.get("seeds"):
            out.append(f"private[{pl}].seeds")
        if private_p.get("inventories") != private_a.get("inventories"):
            out.append(f"private[{pl}].inventories")
    return out


def _s_config(replay: dict) -> dict:
    cfg = dict(S_DEFAULT_CONFIG)
    for key in cfg:
        value = (replay.get("configuration") or {}).get(key)
        if value is not None:
            cfg[key] = value
    return cfg


# --------------------------------------------------------------------------- #
# unit action application (engine order), with per-request attribution
# --------------------------------------------------------------------------- #
def _s_apply_unit_action(farm, private, idx, action, board_size, day,
                         turns_per_day, shed_capacity, uacc):
    """Mirror of the engine _apply_unit_action + request accounting.

    uacc = per-unit accumulator dict ({"requests": Counter, "success":
    Counter, "fail": {op: Counter}, "units_harvested": Counter}); action
    classification follows the engine's guard order exactly, so each request
    lands in exactly one bucket.
    """

    def req(op):
        uacc["requests"][op] += 1

    def ok(op):
        uacc["success"][op] += 1

    def fail(op, reason):
        uacc["fail"].setdefault(op, Counter())[reason] += 1

    if action is None or (isinstance(action, list) and not action):
        return
    if not isinstance(action, list):
        uacc["requests"]["MALFORMED"] += 1
        return
    op = action[0]
    pos = farm["farmer"] if idx == 0 else (
        farm["hands"][idx - 1] if idx - 1 < len(farm["hands"]) else None)
    if pos is None:
        return
    fx, fy = pos[0], pos[1]
    inv = private["inventories"][idx] if idx < len(private["inventories"]) else None
    if inv is None:
        while len(private["inventories"]) <= idx:
            private["inventories"].append({})
        inv = private["inventories"][idx]

    def _inv_add(item, n=1):
        inv[item] = inv.get(item, 0) + n

    def _inv_take(item, n=1):
        if inv.get(item, 0) < n:
            return False
        inv[item] -= n
        if inv[item] == 0:
            del inv[item]
        return True

    if op in S_FARMER_MOVES:
        req(op)
        dx, dy = S_FARMER_MOVES[op]
        nx, ny = fx + dx, fy + dy
        if not (0 <= nx < board_size and 0 <= ny < board_size):
            fail(op, "off_board")
            return
        if idx == 0:
            farm["farmer"] = [nx, ny]
        else:
            farm["hands"][idx - 1] = [nx, ny]
        ok(op)
        return

    if op == "PASS":
        uacc["pass"] += 1
        return

    tile = farm["tiles"][fy][fx]

    if op == "DROP":
        req(op)
        if not _s_is_shed_adjacent((fx, fy), board_size):
            fail(op, "wrong_target")
            return
        shed = private["shed"]
        for item, n in list(inv.items()):
            if n <= 0:
                del inv[item]
                continue
            room = max(0, shed_capacity - sum(shed.values()))
            take = min(n, room)
            if take > 0:
                shed[item] = shed.get(item, 0) + take
            del inv[item]
            if take < n:
                uacc["overflow"].setdefault(item, 0)
                uacc["overflow"][item] += n - take
        ok(op)
        return

    if op == "PICKUP":
        req(op)
        if not _s_is_shed_adjacent((fx, fy), board_size):
            fail(op, "wrong_target")
            return
        if len(action) < 2:
            fail(op, "malformed")
            return
        item = action[1]
        n = int(action[2]) if len(action) >= 3 else 1
        if n <= 0:
            fail(op, "malformed")
            return
        available = private["shed"].get(item, 0)
        n = min(n, available)
        if n <= 0:
            fail(op, "no_stock")
            return
        private["shed"][item] -= n
        _inv_add(item, n)
        ok(op)
        return

    if op == "PLACE":
        req(op)
        if len(action) < 2:
            fail(op, "malformed")
            return
        item = action[1]
        if (item in S_ANIMALS and isinstance(tile, dict)
                and tile.get("kind") == S_ANIMALS[item]["structure"]
                and "animal" not in tile):
            if _inv_take(item, 1):
                farm["tiles"][fy][fx] = _s_new_animal(item, day)
                ok(op)
                return
            fail(op, "no_resource")
            return
        if _s_is_shed_adjacent((fx, fy), board_size):
            n = int(action[2]) if len(action) >= 3 else 1
            if n <= 0:
                fail(op, "malformed")
                return
            n = min(n, inv.get(item, 0))
            if n <= 0:
                fail(op, "no_resource")
                return
            current = sum(private["shed"].values())
            room = max(0, shed_capacity - current)
            n = min(n, room)
            if n <= 0:
                fail(op, "shed_full")
                return
            inv[item] -= n
            if inv[item] == 0:
                del inv[item]
            private["shed"][item] = private["shed"].get(item, 0) + n
            ok(op)
            return
        fail(op, "wrong_target")
        return

    if tile == "LOCKED":
        req(op)
        fail(op, "locked_tile")
        return

    if op == "PLANT":
        req(op)
        if len(action) < 2:
            fail(op, "malformed")
            return
        crop = action[1]
        if crop not in S_CROPS:
            fail(op, "malformed")
            return
        if tile is not None:
            fail(op, "wrong_target")
            return
        if private["seeds"].get(crop, 0) <= 0:
            fail(op, "no_resource")
            return
        private["seeds"][crop] -= 1
        farm["tiles"][fy][fx] = _s_new_plant(crop, day, turns_per_day)
        ok(op)
        return

    if op == "WATER":
        req(op)
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            fail(op, "wrong_target")
            return
        if tile["watered_today"]:
            fail(op, "already_served")
            return
        tile["watered_today"] = True
        crop_data = S_CROPS[tile["crop"]]
        if not crop_data["ongoing"]:
            age_days = day - tile["planted_day"]
            window_start = (crop_data["max_yield_day"] + 1) // 2
            if window_start <= age_days <= crop_data["max_yield_day"]:
                bonus = 2 if tile["fertilized_until_day"] >= day else 1
                tile["yield_units"] = min(crop_data["max_yield"],
                                          tile["yield_units"] + bonus)
        ok(op)
        return

    if op == "HARVEST":
        req(op)
        if not isinstance(tile, dict):
            fail(op, "wrong_target")
            return
        if tile.get("yield_units", 0) <= 0:
            fail(op, "no_yield")
            return
        if tile.get("kind") == "PLANT":
            crop_data = S_CROPS[tile["crop"]]
            if day - tile["planted_day"] < crop_data["first_yield_day"]:
                fail(op, "no_yield")
                return
            units = tile["yield_units"]
            tile["yield_units"] = 0
            _inv_add(tile["crop"], units)
            if not crop_data["ongoing"]:
                farm["tiles"][fy][fx] = None
        elif "animal" in tile:
            units = tile["yield_units"]
            tile["yield_units"] = 0
            item = S_ANIMALS[tile["animal"]]["product"]
            _inv_add(item, units)
            uacc["harvest_units"][item] = \
                uacc["harvest_units"].get(item, 0) + units
            ok(op)
            return
        else:
            fail(op, "wrong_target")
            return
        item = tile.get("crop", "?")
        uacc["harvest_units"][item] = uacc["harvest_units"].get(item, 0) + units
        ok(op)
        return

    if op == "FERTILIZE":
        req(op)
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            fail(op, "wrong_target")
            return
        if not _inv_take("FERTILIZER", 1):
            fail(op, "no_resource")
            return
        tile["fertilized_until_day"] = max(tile.get("fertilized_until_day", -1), day + 2)
        ok(op)
        return

    if op == "DIG":
        req(op)
        if tile is None:
            fail(op, "wrong_target")
            return
        if isinstance(tile, dict) and "animal" in tile:
            fail(op, "wrong_target")
            return
        farm["tiles"][fy][fx] = None
        ok(op)
        return

    if op == "BUILD_COOP":
        req(op)
        if tile is not None:
            fail(op, "wrong_target")
            return
        farm["tiles"][fy][fx] = {"kind": "COOP"}
        ok(op)
        return

    if op == "BUILD_PASTURE":
        req(op)
        if tile is not None:
            fail(op, "wrong_target")
            return
        farm["tiles"][fy][fx] = {"kind": "PASTURE"}
        ok(op)
        return

    if op == "FEED":
        req(op)
        if not (isinstance(tile, dict) and "animal" in tile):
            fail(op, "wrong_target")
            return
        if tile["fed_today"]:
            fail(op, "already_served")
            return
        if not _inv_take("WHEAT", 1):
            fail(op, "no_resource")
            return
        tile["fed_today"] = True
        ok(op)
        return

    if op == "COLLECT_FERTILIZER":
        req(op)
        if not (isinstance(tile, dict) and "animal" in tile):
            fail(op, "wrong_target")
            return
        if not tile["fertilizer_available"]:
            fail(op, "already_served")
            return
        tile["fertilizer_available"] = False
        _inv_add("FERTILIZER", 1)
        ok(op)
        return

    if op == "CARE":
        req(op)
        if not (isinstance(tile, dict) and "animal" in tile):
            fail(op, "wrong_target")
            return
        if tile["cared_today"]:
            fail(op, "already_served")
            return
        tile["cared_today"] = True
        ok(op)
        return

    req(op)
    fail(op, "malformed")


# --------------------------------------------------------------------------- #
# market lockstep (engine column semantics) with fill accounting
# --------------------------------------------------------------------------- #
def _s_parse_order(order):
    if not isinstance(order, list) or not order:
        return None
    op = order[0]
    if op == "HIRE":
        return {"type": "HIRE"}
    if op == "BUY_LAND":
        return {"type": "BUY_LAND"}
    if op in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"):
        if len(order) < 3:
            return None
        try:
            n = int(order[2])
        except (TypeError, ValueError):
            return None
        if n <= 0:
            return None
        return {"type": op, "item": order[1], "remaining": n}
    return None


def _s_commit_unit(op, item, price, farm, private, market, shed_capacity):
    """Mirror of _commit_unit; returns (ok, abort_reason)."""
    if op == "SELL":
        if private["shed"].get(item, 0) <= 0:
            return False, "no_stock"
        private["shed"][item] -= 1
        farm["money"] += price
        if price > 1:
            market["inventory"][item] += 1
        return True, None
    if op == "BUY_PRODUCT":
        if farm["money"] < price:
            return False, "no_money"
        if sum(private["shed"].values()) >= shed_capacity:
            return False, "shed_full"
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        market["inventory"][item] -= 1
        return True, None
    if op == "BUY_SEED":
        if farm["money"] < price:
            return False, "no_money"
        farm["money"] -= price
        private["seeds"][item] = private["seeds"].get(item, 0) + 1
        return True, None
    if op == "BUY_ANIMAL":
        if farm["money"] < price:
            return False, "no_money"
        if sum(private["shed"].values()) >= shed_capacity:
            return False, "shed_full"
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        return True, None
    return False, "malformed"


def _s_process_market(state, actions, cfg, macc):
    """Per-column lockstep market resolution + per-order fill records."""
    market = state["market"]
    farms, privates = state["farms"], state["privates"]
    max_orders = max(1, int(cfg["maxMarketOrdersPerTurn"]))
    hire_mult = int(cfg["farmHandCostMult"])
    shed_capacity = int(cfg["shedCapacity"])

    queues = []
    for pl in (0, 1):
        act = actions[pl] if isinstance(actions[pl], dict) else {}
        m = act.get("market", [])
        q = list(m) if isinstance(m, list) else []
        queues.append(q[:max_orders])

    max_len = max((len(q) for q in queues), default=0)
    for i in range(max_len):
        order_states = []
        records = []
        for pl, q in enumerate(queues):
            ostate = None
            if i < len(q):
                ostate = _s_parse_order(q[i])
                if ostate is not None and "item" in ostate:
                    ostate["requested"] = ostate["remaining"]
                    ostate["filled"] = 0
                    ostate["value"] = 0.0
                    ostate["first_price"] = None
                    ostate["abort"] = None
                    ostate["column"] = i
                    records.append((pl, ostate))
            order_states.append(ostate)

        for pl, ostate in enumerate(order_states):
            if ostate is None:
                continue
            op = ostate["type"]
            if op == "HIRE":
                macc[pl]["hire"]["requests"] += 1
                cost = _s_hire_cost(farms[pl]["hires_today"], hire_mult)
                if farms[pl]["money"] < cost:
                    macc[pl]["hire"]["no_money"] += 1
                    macc[pl]["hire"]["failed_cost"] += cost
                else:
                    farms[pl]["money"] -= cost
                    farms[pl]["hires_today"] += 1
                    farms[pl]["hands"].append(
                        _s_spawn_hand(farms[pl], int(cfg["boardSize"])))
                    privates[pl]["inventories"].append({})
                    macc[pl]["hire"]["successes"] += 1
                    macc[pl]["hire"]["spend"] += cost
                order_states[pl] = None
            elif op == "BUY_LAND":
                macc[pl]["buy_land"]["requests"] += 1
                n_unlocked = len(farms[pl]["unlocked_quadrants"]) - 1
                if n_unlocked >= len(S_LAND_ORDER):
                    macc[pl]["buy_land"]["no_land"] += 1
                else:
                    cost = S_LAND_PRICES[n_unlocked]
                    if farms[pl]["money"] < cost:
                        macc[pl]["buy_land"]["no_money"] += 1
                    else:
                        farms[pl]["money"] -= cost
                        quadrant = S_LAND_ORDER[n_unlocked]
                        farms[pl]["unlocked_quadrants"].append(quadrant)
                        board = len(farms[pl]["tiles"])
                        for y in range(board):
                            for x in range(board):
                                if (_s_quadrant_of(x, y, board) == quadrant
                                        and farms[pl]["tiles"][y][x] == "LOCKED"):
                                    farms[pl]["tiles"][y][x] = None
                        macc[pl]["buy_land"]["successes"] += 1
                        macc[pl]["buy_land"]["spend"] += cost
                order_states[pl] = None

        idx_esc = 0
        while True:
            idx_esc += 1
            if idx_esc >= 100_000:
                break
            quoted = [None, None]
            for pl, ostate in enumerate(order_states):
                if ostate is None or ostate["remaining"] <= 0:
                    continue
                op, item = ostate["type"], ostate["item"]
                if op == "SELL" and item in S_PRODUCTS:
                    quoted[pl] = ("SELL", item,
                                  _s_market_price(item, market["inventory"][item]))
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    quoted[pl] = ("BUY_PRODUCT", item,
                                  _s_market_price(item, market["inventory"][item] - 1))
                elif op == "BUY_SEED" and item in S_CROPS:
                    quoted[pl] = ("BUY_SEED", item, S_CROPS[item]["seed"])
                elif op == "BUY_ANIMAL" and item in S_ANIMALS:
                    quoted[pl] = ("BUY_ANIMAL", item, S_ANIMALS[item]["cost"])
                else:
                    ostate["abort"] = "malformed"
                    order_states[pl] = None
            if all(q is None for q in quoted):
                break
            committed_any = False
            for pl, q in enumerate(quoted):
                if q is None:
                    continue
                op, item, price = q
                ostate = order_states[pl]
                if ostate["first_price"] is None:
                    ostate["first_price"] = price
                committed, reason = _s_commit_unit(
                    op, item, price, farms[pl], privates[pl], market,
                    shed_capacity)
                if committed:
                    ostate["remaining"] -= 1
                    ostate["filled"] += 1
                    ostate["value"] += price
                    committed_any = True
                else:
                    ostate["abort"] = reason
                    order_states[pl] = None
            if not committed_any:
                break

        _s_refresh_prices(market)
        # records keep aborted orders too (fills recorded before the abort
        # stay visible; order_states drops them per the engine's semantics)
        for pl, ostate in records:
            macc[pl]["orders"].append(ostate)


# --------------------------------------------------------------------------- #
# world ticks: town consumption, plant decay, end-of-day refresh
# --------------------------------------------------------------------------- #
def _s_town_consume(state, step_index, cfg):
    market, town = state["market"], state["town"]
    if step_index % max(1, int(cfg["townShopSellInterval"])) == 0:
        for shop_name in town.get("unlocked_shops", []):
            products = S_SHOPS[shop_name]
            multiplier = 2 if len(products) == 1 else 1
            for item in products:
                market["inventory"][item] -= multiplier
    if step_index % max(1, int(cfg["townCenterSellInterval"])) == 0:
        for item in S_TOWN_CENTER_PRODUCTS:
            market["inventory"][item] -= 1
    _s_refresh_prices(market)


def _s_decay_plants(farm, step_index, events):
    board = len(farm["tiles"])
    for y in range(board):
        for x in range(board):
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            mls = tile["max_lifespan_step"]
            if mls < 0 or step_index < mls:
                continue
            if (step_index - mls) % 2 != 0:
                continue
            tile["yield_units"] -= 1
            if tile["yield_units"] <= 0:
                farm["tiles"][y][x] = {"kind": "WEED"}
                events.append({"type": "weed_decay", "crop": tile["crop"],
                               "x": x, "y": y})


def _s_daily_refresh_plants(farm, day, turns_per_day, events):
    board = len(farm["tiles"])
    next_day = day + 1
    for y in range(board):
        for x in range(board):
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            was_watered = tile["watered_today"]
            if was_watered:
                tile["consecutive_unwatered"] = 0
            else:
                tile["consecutive_unwatered"] += 1
            tile["watered_today"] = False
            if tile["consecutive_unwatered"] >= 2:
                farm["tiles"][y][x] = {"kind": "WEED"}
                events.append({"type": "weed_care_lapse", "crop": tile["crop"],
                               "x": x, "y": y,
                               "unwatered_days": tile["consecutive_unwatered"]})
                continue
            cd = S_CROPS[tile["crop"]]
            if not cd["ongoing"]:
                continue
            days_since_first = next_day - tile["planted_day"] - cd["first_yield_day"]
            if days_since_first < 0:
                continue
            if days_since_first % cd["interval"] != 0:
                continue
            production_count = days_since_first // cd["interval"] + 1
            if production_count > cd["max_yield"]:
                continue
            fertilized = was_watered and tile.get("fertilized_until_day", -1) >= day
            tile["yield_units"] = min(cd["max_yield"],
                                      tile["yield_units"] + (2 if fertilized else 1))
            if production_count == cd["max_yield"]:
                tile["max_lifespan_step"] = (next_day + 1) * turns_per_day


def _s_daily_refresh_animals(farm, day, events):
    board = len(farm["tiles"])
    next_day = day + 1
    for y in range(board):
        for x in range(board):
            tile = farm["tiles"][y][x]
            if not (isinstance(tile, dict) and "animal" in tile):
                continue
            if tile["fed_today"]:
                tile["consecutive_unfed"] = 0
            else:
                tile["consecutive_unfed"] += 1
            if tile["consecutive_unfed"] >= 2:
                events.append({"type": "escape", "animal": tile["animal"],
                               "x": x, "y": y,
                               "unfed_days": tile["consecutive_unfed"],
                               "yield_units_lost": tile["yield_units"],
                               "loss_est": S_ANIMALS[tile["animal"]]["cost"]})
                farm["tiles"][y][x] = {"kind": S_ANIMALS[tile["animal"]]["structure"]}
                continue
            a = S_ANIMALS[tile["animal"]]
            days_since_first = next_day - tile["placed_day"] - a["first_yield_day"]
            if days_since_first >= 0 and days_since_first % a["interval"] == 0:
                base = 1
                bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
                tile["yield_units"] = min(a["max_held"],
                                          tile["yield_units"] + base + bonus)
                tile["pending_care_bonus"] = 0
            if tile["cared_today"] and tile["fed_today"]:
                tile["pending_care_bonus"] = tile.get("pending_care_bonus", 0) + 1
            tile["fertilizer_available"] = True
            tile["fed_today"] = False
            tile["cared_today"] = False


def _s_spawn_weeds(farm, board_size, weed_chance, rng, events):
    for y in range(board_size):
        for x in range(board_size):
            if farm["tiles"][y][x] is None and rng.random() < weed_chance:
                farm["tiles"][y][x] = {"kind": "WEED"}
                events.append({"type": "weed_spawn", "x": x, "y": y})


def _s_drop_inventories(private, capacity, overflow):
    """End-of-day drop; overflow beyond shed capacity is discarded."""
    shed = private["shed"]
    for inv in private["inventories"]:
        for item, n in list(inv.items()):
            if n <= 0:
                del inv[item]
                continue
            current = sum(shed.values())
            room = max(0, capacity - current)
            take = min(n, room)
            if take > 0:
                shed[item] = shed.get(item, 0) + take
            del inv[item]
            if take < n:
                overflow[item] = overflow.get(item, 0) + (n - take)


def _s_end_of_day(state, day, cfg, seed, events, overflow):
    rng = random.Random((seed * 1_000_003) ^ day)
    board = int(cfg["boardSize"])
    turns_per_day = max(1, int(cfg["turnsPerDay"]))
    weed_chance = float(cfg["weedSpawnChance"])
    shed_cap = int(cfg["shedCapacity"])
    shop_interval = max(1, int(cfg["townShopUnlockInterval"]))
    for pl, farm in enumerate(state["farms"]):
        private = state["privates"][pl]
        ev = []
        _s_daily_refresh_plants(farm, day, turns_per_day, ev)
        _s_daily_refresh_animals(farm, day, ev)
        for e in ev:
            e["player"] = pl
        events.extend(ev)
        spawn_ev = []
        _s_spawn_weeds(farm, board, weed_chance, rng, spawn_ev)
        for e in spawn_ev:
            e["player"] = pl
        events.extend(spawn_ev)
        _s_drop_inventories(private, shed_cap, overflow[pl])
        farm["farmer"] = list(_s_default_spawn(board))
        farm["hands"] = []
        farm["hires_today"] = 0
        private["inventories"] = [{}]
    next_day = day + 1
    town = state["town"]
    if next_day > 0 and next_day % shop_interval == 0:
        if len(town.get("unlocked_shops", [])) < S_MAX_SHOP_INSTANCES:
            town.setdefault("unlocked_shops", []).append(
                rng.choice(sorted(S_SHOPS)))


# --------------------------------------------------------------------------- #
# one full interpreter step (shadow)
# --------------------------------------------------------------------------- #
def _s_new_uacc() -> dict:
    return {"requests": Counter(), "success": Counter(),
            "fail": {}, "pass": 0, "overflow": {},
            "harvest_units": {}}


def _s_new_macc(pl_count=2) -> list:
    return [{"hire": {"requests": 0, "successes": 0, "no_money": 0,
                      "spend": 0, "failed_cost": 0},
             "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                          "no_land": 0, "spend": 0},
             "orders": []} for _ in range(pl_count)]


def _s_step(pre_state: dict, actions, step_index: int, cfg: dict, seed: int):
    """Replay one interpreter call; returns (post_state, attribution)."""
    st = copy.deepcopy(pre_state)
    attr = {"unit": [_s_new_uacc(), _s_new_uacc()],
            "market": _s_new_macc(),
            "events": [], "overflow": [{}, {}]}
    day = step_index // max(1, int(cfg["turnsPerDay"]))
    board = int(cfg["boardSize"])
    turns_per_day = max(1, int(cfg["turnsPerDay"]))
    shed_capacity = int(cfg["shedCapacity"])

    for pl in (0, 1):
        act = actions[pl] if isinstance(actions[pl], dict) else {}
        farmer_action = act.get("farmer", ["PASS"])
        hands_actions = act.get("hands", [])
        if not isinstance(hands_actions, list):
            hands_actions = []
        farm, private = st["farms"][pl], st["privates"][pl]
        unit_actions = [farmer_action, *hands_actions]
        plant_demand = {}
        for a in unit_actions:
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT":
                plant_demand[a[1]] = plant_demand.get(a[1], 0) + 1
        blocked = {crop for crop, n in plant_demand.items()
                   if n > private.get("seeds", {}).get(crop, 0)}

        def _allowed(a):
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT" and a[1] in blocked:
                # engine drops the whole crop's PLANT requests this turn
                # (atomic validation); keep it visible as a failed request
                uacc = attr["unit"][pl]
                uacc["requests"]["PLANT"] += 1
                uacc["fail"].setdefault("PLANT", Counter())["no_resource"] += 1
                return ["PASS"]
            return a

        _s_apply_unit_action(farm, private, 0, _allowed(farmer_action),
                             board, day, turns_per_day, shed_capacity,
                             attr["unit"][pl])
        for h_idx, hand_action in enumerate(hands_actions):
            _s_apply_unit_action(farm, private, h_idx + 1,
                                 _allowed(hand_action), board, day,
                                 turns_per_day, shed_capacity,
                                 attr["unit"][pl])

    _s_process_market(st, actions, cfg, attr["market"])
    _s_town_consume(st, step_index, cfg)
    for farm in st["farms"]:
        _s_decay_plants(farm, step_index, attr["events"])
    if (step_index + 1) % turns_per_day == 0:
        _s_end_of_day(st, day, cfg, seed, attr["events"], attr["overflow"])
    return st, attr


# --------------------------------------------------------------------------- #
# aggregation
# --------------------------------------------------------------------------- #
def _s_op_row(uacc_series) -> dict:
    """Aggregate a list of per-step unit accumulators into one op table."""
    rows = {}
    for op in ("CARE", "FEED", "WATER", "HARVEST", "PLANT", "DIG"):
        req = sum(u["requests"][op] for u in uacc_series)
        succ = sum(u["success"][op] for u in uacc_series)
        fails = Counter()
        for u in uacc_series:
            fails.update(u["fail"].get(op, Counter()))
        failure_dict = {reason: int(fails.get(reason, 0))
                        for reason in S_FAILS[op]}
        for reason, n in fails.items():
            if reason not in failure_dict and n:
                failure_dict[reason] = int(n)
        rows[op] = {
            "requests": req, "successes": succ,
            "success_rate": round(succ / req, 4) if req else None,
            "failures": failure_dict,
        }
    return rows


def _s_sell_rows(orders) -> dict:
    """Per-op/per-item fill + slippage summary over market order records."""
    out = {}
    for op in ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL"):
        sel = [o for o in orders if o["type"] == op]
        if not sel:
            out[op] = {"orders": 0, "requested_qty": 0, "filled_qty": 0,
                       "fill_rate": None, "per_item": {}}
            continue
        per_item = {}
        for o in sel:
            row = per_item.setdefault(o["item"], {
                "orders": 0, "requested_qty": 0, "filled_qty": 0,
                "value": 0.0, "first_price_sum": 0.0, "first_price_n": 0,
                "partial_orders": 0, "unfilled_orders": 0, "abort": Counter()})
            row["orders"] += 1
            row["requested_qty"] += o["requested"]
            row["filled_qty"] += o["filled"]
            row["value"] += o["value"]
            row["first_price_sum"] += o["first_price"] or 0
            row["first_price_n"] += 1 if o["first_price"] is not None else 0
            if 0 < o["filled"] < o["requested"]:
                row["partial_orders"] += 1
            if o["filled"] == 0:
                row["unfilled_orders"] += 1
            if o["abort"]:
                row["abort"][o["abort"]] += 1
        req = sum(o["requested"] for o in sel)
        filled = sum(o["filled"] for o in sel)
        out[op] = {
            "orders": len(sel), "requested_qty": req, "filled_qty": filled,
            "fill_rate": round(filled / req, 4) if req else None,
            "unfilled_orders": sum(1 for o in sel if o["filled"] == 0),
            "partial_orders": sum(1 for o in sel if 0 < o["filled"] < o["requested"]),
            "per_item": {
                item: {
                    "orders": row["orders"],
                    "requested_qty": row["requested_qty"],
                    "filled_qty": row["filled_qty"],
                    "fill_rate": round(row["filled_qty"] / row["requested_qty"], 4)
                    if row["requested_qty"] else None,
                    "value": round(row["value"], 1),
                    "avg_price": round(row["value"] / row["filled_qty"], 2)
                    if row["filled_qty"] else None,
                    "avg_first_quoted_price": round(
                        row["first_price_sum"] / row["first_price_n"], 2)
                    if row["first_price_n"] else None,
                    "slippage_per_unit": round(
                        row["value"] / row["filled_qty"]
                        - row["first_price_sum"] / row["first_price_n"], 2)
                    if row["filled_qty"] and row["first_price_n"] else None,
                    "unfilled_orders": row["unfilled_orders"],
                    "partial_orders": row["partial_orders"],
                    "abort_reasons": dict(row["abort"]),
                }
                for item, row in per_item.items()
            },
        }
    return out


def _s_worker_row(uacc) -> dict:
    moves = sum(u["requests"][m] for u in uacc for m in S_FARMER_MOVES)
    move_ok = sum(u["success"][m] for u in uacc for m in S_FARMER_MOVES)
    passes = sum(u["pass"] for u in uacc)
    op_req = sum(u["requests"][op] for u in uacc for op in S_UNIT_OPS_TRACKED)
    op_ok = sum(u["success"][op] for u in uacc for op in S_UNIT_OPS_TRACKED)
    total_turns = moves + passes + op_req
    return {
        "turns": total_turns,
        "move_requests": moves, "move_successes": move_ok,
        "move_blocked": moves - move_ok,
        "op_requests": op_req, "op_successes": op_ok,
        "op_failures": op_req - op_ok,
        "pass_turns": passes,
        "movement_share": round(moves / total_turns, 4) if total_turns else None,
        "effective_op_share": round(op_ok / total_turns, 4) if total_turns else None,
        "moves_per_effective_op": round(moves / op_ok, 3) if op_ok else None,
        "wasted_turns": (moves - move_ok) + (op_req - op_ok),
    }


def _s_animal_registry(tiles_history) -> list:
    """Per-animal placement registry from day-end tile snapshots.

    tiles_history: list of (day, tiles) sampled at every end-of-day; animals
    are identified by (x, y), which is stable for the lifetime of a placement
    (animals never move; a disappearing (x, y) animal = escape).
    """
    registry = []
    live: dict = {}
    for day, tiles in tiles_history:
        seen = set()
        if not isinstance(tiles, list):
            continue
        for y, row in enumerate(tiles):
            if not isinstance(row, list):
                continue
            for x, cell in enumerate(row):
                if isinstance(cell, dict) and "animal" in cell:
                    seen.add((x, y))
                    key = (x, y)
                    if key not in live:
                        live[key] = {"animal": cell["animal"],
                                     "first_seen_day": day, "x": x, "y": y,
                                     "yield_units": 0}
                    live[key]["yield_units"] = cell.get("yield_units", 0)
        for key in list(live):
            if key not in seen:
                rec = live.pop(key)
                rec["end_day"] = day
                rec["end_reason"] = "escaped"
                registry.append(rec)
    for rec in live.values():
        rec["end_day"] = tiles_history[-1][0] if tiles_history else None
        rec["end_reason"] = "season_end"
        registry.append(rec)
    registry.sort(key=lambda r: (r["first_seen_day"], r["y"], r["x"]))
    return registry


def extract_success_metrics(
    replay: dict,
    episode_id: int | None = None,
    source_url: str = "",
    capture_date: str = "",
    strict: bool = True,
) -> dict:
    """Success-caliber metrics for both seats of one replay.

    Returns a JSON-serialisable dict; see SUCCESS_PROTOCOL.  strict=True
    propagates integrity errors (mirrors extract_episode_profiles).
    """
    issues = check_integrity(replay)
    if issues and strict:
        raise IntegrityError("; ".join(issues))
    info = replay.get("info") or {}
    if episode_id is None:
        episode_id = info.get("EpisodeId")
    teams = list(info.get("TeamNames") or ["?", "?"])
    rewards = list(replay.get("rewards") or [None, None])
    steps = replay["steps"]
    cfg = _s_config(replay)
    seed = info.get("seed")
    if seed is None:
        seed = (replay.get("configuration") or {}).get("seed") or 0

    # per-player step-level accumulators
    per_player = []
    for pl in (0, 1):
        per_player.append({
            "uacc": [],            # per-step unit accumulators
            "macc": {"hire": {"requests": 0, "successes": 0, "no_money": 0,
                              "spend": 0, "failed_cost": 0},
                     "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                                  "no_land": 0, "spend": 0},
                     "orders": []},
            "day_events": defaultdict(list),   # day -> events for that player
            "day_overflow": defaultdict(dict),  # day -> {item: discarded units}
            "harvest_units": Counter(),
            "tiles_history": [],               # (day, tiles) day-end samples
            "money_by_day": {},
        })

    state = _s_snapshot(
        steps[0][0].get("observation") or {},
        [steps[0][0].get("observation", {}).get("private"),
         steps[0][1].get("observation", {}).get("private")])
    mismatches = []
    attributed_steps = 0
    turns_per_day = max(1, int(cfg["turnsPerDay"]))

    for t in range(1, len(steps)):
        actions = [steps[t][pl].get("action") or {} for pl in (0, 1)]
        pre_obs = steps[t - 1][0].get("observation") or {}
        step_index = int(pre_obs.get("step", t - 1))
        post_state, attr = _s_step(state, actions, step_index, cfg, seed)
        actual0 = steps[t][0].get("observation") or {}
        actual_priv = [steps[t][0].get("observation", {}).get("private"),
                       steps[t][1].get("observation", {}).get("private")]
        diff = _s_compare(post_state, actual0, actual_priv)
        if diff:
            mismatches.append({"t": t, "day": step_index // turns_per_day,
                               "fields": diff[:10]})
            state = _s_snapshot(actual0, actual_priv)
        else:
            attributed_steps += 1
            state = post_state

        day = step_index // turns_per_day
        for pl in (0, 1):
            pp = per_player[pl]
            pp["uacc"].append(attr["unit"][pl])
            for key in ("hire", "buy_land"):
                src = attr["market"][pl][key]
                for field in src:
                    pp["macc"][key][field] += src[field]
            pp["macc"]["orders"].extend(
                {k: o[k] for k in ("type", "item", "requested", "filled",
                                   "value", "first_price", "abort", "column")}
                for o in attr["market"][pl]["orders"])
            for event in attr["events"]:
                if event.get("player") == pl:
                    event = dict(event)
                    event.pop("player", None)
                    pp["day_events"][day].append(event)
            pp["day_overflow"][day].update(attr["overflow"][pl])
            # day-end sampling from the REAL observation (money + tiles)
            if (step_index + 1) % turns_per_day == 0:
                farm = (actual0.get("farms") or [{}] * 2)[pl] or {}
                money = farm.get("money")
                if isinstance(money, (int, float)):
                    pp["money_by_day"][day] = round(float(money), 1)
                pp["tiles_history"].append((day, copy.deepcopy(farm.get("tiles"))))

    players_out = []
    for pl in (0, 1):
        pp = per_player[pl]
        uacc = pp["uacc"]
        macc = pp["macc"]
        all_events = [e for d in sorted(pp["day_events"]) for e in pp["day_events"][d]]
        escapes = [e for e in all_events if e["type"] == "escape"]
        weed_lapse = [e for e in all_events if e["type"] == "weed_care_lapse"]
        weed_decay = [e for e in all_events if e["type"] == "weed_decay"]
        weed_spawn = [e for e in all_events if e["type"] == "weed_spawn"]
        overflow_total = Counter()
        for _d, ov in pp["day_overflow"].items():
            overflow_total.update(ov)
        # capped tile-days: animal tiles at max_held in day-end snapshots
        cap_counter = Counter()
        for _day, tiles in pp["tiles_history"]:
            if not isinstance(tiles, list):
                continue
            for row in tiles:
                if not isinstance(row, list):
                    continue
                for cell in row:
                    if isinstance(cell, dict) and "animal" in cell:
                        if cell.get("yield_units", 0) >= \
                                S_ANIMALS[cell["animal"]]["max_held"]:
                            cap_counter[cell["animal"]] += 1
        op_rows = _s_op_row(uacc)
        for u in uacc:
            pp["harvest_units"].update(u["harvest_units"])
        day_rows = []
        steps_per_day = turns_per_day
        for day in range((len(steps) - 1 + steps_per_day - 1) // steps_per_day):
            lo, hi = day * steps_per_day, (day + 1) * steps_per_day
            day_uacc = uacc[lo:hi]
            ev = pp["day_events"].get(day, [])
            day_rows.append({
                "day": day,
                "care_req": sum(u["requests"]["CARE"] for u in day_uacc),
                "care_ok": sum(u["success"]["CARE"] for u in day_uacc),
                "feed_req": sum(u["requests"]["FEED"] for u in day_uacc),
                "feed_ok": sum(u["success"]["FEED"] for u in day_uacc),
                "water_req": sum(u["requests"]["WATER"] for u in day_uacc),
                "water_ok": sum(u["success"]["WATER"] for u in day_uacc),
                "harvest_req": sum(u["requests"]["HARVEST"] for u in day_uacc),
                "harvest_ok": sum(u["success"]["HARVEST"] for u in day_uacc),
                "invalid_unit_ops": sum(
                    u["requests"][op] - u["success"][op]
                    for u in day_uacc for op in S_UNIT_OPS_TRACKED),
                "escapes": sum(1 for e in ev if e["type"] == "escape"),
                "weed_lapse": sum(1 for e in ev if e["type"] == "weed_care_lapse"),
                "overflow_units": sum(pp["day_overflow"].get(day, {}).values()),
                "money_end": pp["money_by_day"].get(day),
            })
        won = None
        if (isinstance(rewards[pl], (int, float))
                and isinstance(rewards[1 - pl], (int, float))):
            won = rewards[pl] > rewards[1 - pl]
        players_out.append({
            "protocol": SUCCESS_PROTOCOL,
            "episode_id": episode_id,
            "seat": pl,
            "team": teams[pl] if pl < len(teams) else "?",
            "opponent": teams[1 - pl] if 1 - pl < len(teams) else "?",
            "reward": rewards[pl] if pl < len(rewards) else None,
            "won": won,
            "source_url": source_url,
            "capture_date": capture_date,
            "ops": op_rows,
            "harvest_units_by_item": dict(pp["harvest_units"]),
            "hire": {
                "requests": macc["hire"]["requests"],
                "successes": macc["hire"]["successes"],
                "no_money_rejects": macc["hire"]["no_money"],
                "spend": round(macc["hire"]["spend"], 1),
                "success_rate": round(macc["hire"]["successes"]
                                      / macc["hire"]["requests"], 4)
                if macc["hire"]["requests"] else None,
            },
            "buy_land": dict(macc["buy_land"]),
            "market": _s_sell_rows(macc["orders"]),
            "escapes": {
                "count": len(escapes),
                "asset_loss_est": sum(e["loss_est"] for e in escapes),
                "events": escapes,
            },
            "weeds": {
                "care_lapse": len(weed_lapse),
                "overripe_decay": len(weed_decay),
                "random_spawn": len(weed_spawn),
                "care_lapse_events": weed_lapse,
                "loss_est": sum(
                    S_CROPS.get(e.get("crop"), {}).get("seed", 0)
                    for e in weed_lapse),
            },
            "shed_overflow": {
                "discarded_units": sum(overflow_total.values()),
                "by_item": dict(overflow_total),
            },
            "animal_cap_waste": {
                "capped_tile_days": sum(cap_counter.values()),
                "by_animal": dict(cap_counter),
            },
            "workers": _s_worker_row(uacc),
            "animals": _s_animal_registry(pp["tiles_history"]),
            "by_day": day_rows,
            "integrity": {
                "steps_total": len(steps) - 1,
                "steps_attributed": attributed_steps,
                "mismatch_steps": len(mismatches),
                "attribution_valid": not mismatches,
            },
        })

    return {
        "protocol": SUCCESS_PROTOCOL,
        "episode": {
            "episode_id": episode_id,
            "teams": teams,
            "rewards": rewards,
            "seed": seed,
            "engine_config": {k: cfg[k] for k in
                              ("turnsPerDay", "shedCapacity",
                               "maxMarketOrdersPerTurn")},
            "source_url": source_url,
            "capture_date": capture_date,
            "integrity_issues": issues,
            "mismatches": mismatches[:50],
            "mismatch_steps": len(mismatches),
            "attribution_valid": not mismatches,
        },
        "players": players_out,
    }
