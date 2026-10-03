"""Small official-engine probe of V9's day-11 expansion decision.

This is diagnostic only. It never edits the frozen V9 source.
"""
import contextlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    source = ROOT / "submissions/release_v9/main.py"
    entries = [get_last_callable(source.read_text(encoding="utf-8"), path=str(source)) for _ in range(2)]
    seeds = [248311050] if len(sys.argv) == 1 else json.loads(
        (ROOT / "research/round10/league_seeds.json").read_text(encoding="utf-8")
    )["development"][:int(sys.argv[1])]
    for seed in seeds:
      env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=True)
      env.run(entries)
      if len(seeds) > 1:
        step = 266
        obs = env.steps[step][0].observation
        farm = obs.farms[0]
        animal_count = {}
        for row in farm["tiles"]:
          for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
              name = tile["animal"]
              animal_count[name] = animal_count.get(name, 0) + 1
        late = env.steps[528][0].observation
        print(seed, "day11", "cash", farm["money"], "shops", obs.town["unlocked_shops"],
              "prices", {k:obs.market["prices"][k] for k in ("WOOL", "EGG", "CARROT", "STRAWBERRY", "MELON")},
              "animals", animal_count, "shed", sum(obs.private["shed"].values()),
              "day22_wool_price", late.market["prices"]["WOOL"],
              "day22_wool_inventory", late.market["inventory"]["WOOL"])
        continue
      for step in (240, 264, 265, 266, 267, 268, 276, 287, 288, 312, 336, 432, 504, 528, 552):
        obs = env.steps[step][0].observation
        farm = obs.farms[0]
        market = obs.market
        parent = env.steps[step][0].action
        print(step, "cash", farm["money"], "land", farm["unlocked_quadrants"],
              "hands", len(farm["hands"]), "shed", sum(obs.private["shed"].values()),
              "melon_price", market["prices"]["MELON"],
              "melon_inventory", market["inventory"]["MELON"],
              "orders", parent.get("market", []))


if __name__ == "__main__":
    main()
