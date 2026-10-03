"""Read-only summary of harvested day-11 tranche in old public diagnostics."""

from collections import Counter, defaultdict
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parents[1]
files = (
    "research/round10/audit_dsm_1829941733.json.gz",
    "research/round10/audit_dsm_264393735.json.gz",
    "research/round10/audit_dsm_242588832.json.gz",
)

for name in files:
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        episode = json.load(stream)
    steps = episode["steps"]
    obs = steps[264][0]["observation"]
    seat = int(obs["player"])
    chosen = []
    for step in range(264, 288):
        entry = steps[step][seat]
        observation = entry["observation"]
        action = entry.get("action") or {}
        farm = observation["farms"][seat]
        positions = [farm["farmer"], *farm["hands"]]
        commands = [action.get("farmer"), *(action.get("hands") or [])]
        for j, command in enumerate(commands[:len(positions)]):
            if command == ["PLANT", "STRAWBERRY"]:
                chosen.append(tuple(positions[j]))
    by_day = defaultdict(Counter)
    crop_work = defaultdict(Counter)
    for step in range(288, 720):
        entry = steps[step][seat]
        observation = entry["observation"]
        action = entry.get("action") or {}
        farm = observation["farms"][seat]
        positions = [farm["farmer"], *farm["hands"]]
        commands = [action.get("farmer"), *(action.get("hands") or [])]
        for j, command in enumerate(commands[:len(positions)]):
            if command and command[0] in ("WATER", "FERTILIZE") and tuple(positions[j]) in chosen:
                crop_work[step // 24][command[0]] += 1
            if command != ["HARVEST"] or tuple(positions[j]) not in chosen:
                continue
            x, y = positions[j]
            tile = farm["tiles"][y][x]
            before = steps[step - 1][seat]["observation"]["farms"][seat]["tiles"][y][x]
            if isinstance(tile, dict) and tile.get("crop") == "STRAWBERRY" and tile.get("planted_day") == 11:
                by_day[step // 24]["harvest"] += int(before.get("yield_units", 0)) if isinstance(before, dict) else 0
                by_day[step // 24]["tiles"] += 1
    print(Path(name).stem, "day11_plants", len(chosen), "plant_positions", chosen)
    print("  harvest", {day: dict(values) for day, values in by_day.items()})
    print("  total", sum(day["harvest"] for day in by_day.values()))
    print("  care", {day: dict(values) for day, values in crop_work.items()})
