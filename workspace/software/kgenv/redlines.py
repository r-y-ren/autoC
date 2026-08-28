"""Mechanic red-line checklist for Kaggriculture.

Every rule below is transcribed from the official How-to-Play page
(captured 2026-08-28) and cross-checked against the engine source
(kaggle_environments 1.32.7, kaggriculture.py):

  R1 watering   -- a plant not watered for TWO successive days turns into a
                   weed at end-of-day refresh.  A fresh seed starts with
                   consecutive_unwatered = 1, so an unwatered fresh planting
                   dies the very first night ("no grace period").
  R2 feeding    -- an animal not fed (wheat) for two successive days escapes
                   and is unrecoverable.  A newly placed animal starts at 0.
  R3 production -- tomato/strawberry are capped at 4 scheduled productions,
                   then decay to a weed; one-time crops decay one day after
                   max_yield_day.  Standing on a finished plant loses yield.
  R4 shed       -- shed holds 100 non-seed items; overflow at the end-of-day
                   inventory drop is DISCARDED (not held).
  R5 deadlines  -- crops planted too late cannot reach their yield window
                   before the season ends (money is all that counts).
  R6 plant      -- if units request more PLANTs of a crop than seeds held,
                   ALL of that crop's PLANT requests this turn are dropped.

The checker is pure: given a farm/private/day snapshot it returns violations.
It is used by tests and by the arena replay analyzer; agents may also call it
for defensive planning.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from .economy import CROPS, ANIMALS, SEASON_DAYS, latest_planting_day, last_production_day

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}


@dataclass
class Violation:
    code: str
    severity: str          # critical | warning | info
    tile: Optional[List[int]]  # [x, y] when tied to a tile
    detail: str

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def check_farm(farm: Dict, private: Dict, day: int,
               season_days: int = SEASON_DAYS) -> List[Violation]:
    """Check one player's farm snapshot against the red lines.

    `farm` follows the official observation format (tiles[y][x], ...);
    `private` carries shed/seeds.  `day` is the current 0-indexed day.
    """
    out: List[Violation] = []
    tiles = farm.get("tiles", [])
    if not tiles:
        return out

    n_animals = 0
    pending_feed_need = 0

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")

            if kind == "PLANT":
                crop = tile.get("crop")
                cd = CROPS.get(crop)
                if cd is None:
                    continue
                unwatered = tile.get("consecutive_unwatered", 0)
                watered = bool(tile.get("watered_today", False))
                age = day - tile.get("planted_day", day)

                # R1: dies tonight if unwatered streak hits 2 at refresh
                if not watered and unwatered >= 1:
                    sev = "critical" if unwatered >= 1 else "warning"
                    out.append(Violation(
                        "PLANT_DIES_TONIGHT", sev, [x, y],
                        f"{crop} at age {age}: consecutive_unwatered={unwatered}, "
                        f"not yet watered today; becomes a weed at end-of-day refresh"))
                elif not watered:
                    out.append(Violation(
                        "PLANT_UNWATERED_TODAY", "info", [x, y],
                        f"{crop} not yet watered today (streak {unwatered})"))

                # R3: ongoing crops -- final production passed, harvest now
                if cd["ongoing"]:
                    lpd = last_production_day(tile.get("planted_day", day), crop)
                    if day >= lpd and tile.get("yield_units", 0) > 0:
                        out.append(Violation(
                            "ONGOING_HARVEST_NOW", "warning", [x, y],
                            f"{crop} finished its {cd['max_yield']} productions; "
                            f"{tile.get('yield_units', 0)} units will decay from day {lpd + 1}"))
                else:
                    if age > cd["max_yield_day"]:
                        out.append(Violation(
                            "ONE_TIME_PAST_WINDOW", "warning", [x, y],
                            f"{crop} at age {age} > max_yield_day {cd['max_yield_day']}; "
                            f"yield is decaying every other turn"))
                    if tile.get("fertilized_until_day", -1) >= day and age < cd["max_yield_day"]:
                        # fertilizer must land inside the bonus window to pay
                        pass

            elif kind in ("COOP", "PASTURE"):
                if "animal" in tile:
                    n_animals += 1
                    unfed = tile.get("consecutive_unfed", 0)
                    fed = bool(tile.get("fed_today", False))
                    # R2: escapes tonight if unfed streak hits 2 at refresh
                    if not fed and unfed >= 1:
                        out.append(Violation(
                            "ANIMAL_ESCAPES_TONIGHT", "critical", [x, y],
                            f"{tile['animal']} consecutive_unfed={unfed}, not fed today; "
                            f"escapes at end-of-day refresh and is unrecoverable"))
                    elif not fed:
                        pending_feed_need += 1
                        out.append(Violation(
                            "ANIMAL_UNFED_TODAY", "warning", [x, y],
                            f"{tile['animal']} not yet fed today (streak {unfed})"))
                    if tile.get("yield_units", 0) >= ANIMALS.get(tile.get("animal", ""), {}).get("max_held", 99):
                        out.append(Violation(
                            "ANIMAL_AT_MAX_HELD", "warning", [x, y],
                            f"{tile['animal']} at max_held; further production is lost until harvested"))
                    if tile.get("fertilizer_available", False):
                        out.append(Violation(
                            "FERTILIZER_UNCOLLECTED", "info", [x, y],
                            "fertilizer_available=True; uncollected fertilizer does not accumulate"))

            elif kind == "WEED":
                out.append(Violation("WEED_TILE", "info", [x, y],
                                     "weed blocks the tile until DIGged"))

    # R4: shed overflow
    shed = private.get("shed", {}) or {}
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    if shed_count >= 95:
        out.append(Violation("SHED_OVERFLOW_RISK", "critical", None,
                             f"shed holds {shed_count}/100; end-of-day overflow is discarded"))

    # R2 supply: wheat on hand vs animals still needing feed
    wheat_supply = shed.get("WHEAT", 0)
    if pending_feed_need > wheat_supply:
        out.append(Violation("FEED_SUPPLY_SHORT", "critical", None,
                             f"{pending_feed_need} animals unfed today but shed has only "
                             f"{wheat_supply} wheat; buy WHEAT or they risk escaping"))

    # R5: seeds that can no longer mature
    seeds = private.get("seeds", {}) or {}
    for crop, n in seeds.items():
        if isinstance(n, int) and n > 0 and day > latest_planting_day(crop, season_days):
            out.append(Violation("SEED_PAST_DEADLINE", "warning", None,
                                 f"{n} {crop} seed(s) held on day {day} but latest viable "
                                 f"planting day was {latest_planting_day(crop, season_days)}"))

    out.sort(key=lambda v: SEVERITY_ORDER.get(v.severity, 3))
    return out


def summary(violations: List[Violation]) -> Dict[str, int]:
    s = {"critical": 0, "warning": 0, "info": 0}
    for v in violations:
        s[v.severity] = s.get(v.severity, 0) + 1
    return s
