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

import json
import math
import statistics
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
