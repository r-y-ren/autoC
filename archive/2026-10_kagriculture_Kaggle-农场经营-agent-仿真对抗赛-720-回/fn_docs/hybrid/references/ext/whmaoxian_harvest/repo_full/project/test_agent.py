import copy
import unittest

# These are legacy v4 heuristic tests, not contracts for an expert-route policy.
import runpy
from pathlib import Path

agent = runpy.run_path(str(Path(__file__).parent / "submissions/release_v4/main.py"))["agent"]


def observation():
    farm = {"money": 3000, "tiles": [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)],
            "farmer": [4, 4], "hands": [], "hires_today": 0, "unlocked_quadrants": ["NW"]}
    return {"player": 0, "day": 0, "hour": 0, "step": 0,
            "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
            "market": {"inventory": {c: 10000 for c in ("WHEAT", "CARROT", "MELON")}},
            "town": {"unlocked_shops": []}}


class AgentTests(unittest.TestCase):
    def test_observation_is_not_mutated(self):
        obs = observation()
        before = copy.deepcopy(obs)
        agent(obs)
        self.assertEqual(obs, before)

    def test_shared_seed_budget(self):
        obs = observation()
        obs["farms"][0]["farmer"] = [2, 4]
        obs["farms"][0]["hands"] = [[2, 3], [1, 4]]
        obs["private"]["inventories"] += [{}, {}]
        obs["private"]["seeds"] = {"MELON": 1}
        action = agent(obs)
        planted = [a for a in [action["farmer"], *action["hands"]] if a[0] == "PLANT"]
        self.assertEqual(len(planted), 1)

    def test_last_action_sells_same_turn_drop(self):
        obs = observation()
        obs.update(day=29, hour=22, step=718)
        obs["private"]["inventories"] = [{"MELON": 6}]
        obs["private"]["shed"] = {"MELON": 2}
        action = agent(obs)
        self.assertEqual(action["farmer"], ["DROP"])
        self.assertIn(["SELL", "MELON", 8], action["market"])
        self.assertTrue(all(a[0] == "SELL" for a in action["market"]))

    def test_planting_day_water_has_priority(self):
        obs = observation()
        obs.update(hour=22, step=22)
        obs["farms"][0]["farmer"] = [2, 4]
        obs["farms"][0]["tiles"][4][2] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0,
                                                 "watered_today": False, "yield_units": 1}
        self.assertEqual(agent(obs)["farmer"], ["WATER"])

    def test_peak_day_water_before_harvest(self):
        obs = observation()
        obs.update(day=4, step=96)
        obs["farms"][0]["farmer"] = [2, 4]
        obs["farms"][0]["tiles"][4][2] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
                                                 "watered_today": False, "yield_units": 3}
        self.assertEqual(agent(obs)["farmer"], ["WATER"])
        obs["farms"][0]["tiles"][4][2]["watered_today"] = True
        self.assertEqual(agent(obs)["farmer"], ["HARVEST"])

    def test_animal_pickup_does_not_double_reserve(self):
        obs = observation()
        obs["farms"][0]["hands"] = [[4, 4]]
        obs["private"]["inventories"] += [{}]
        obs["private"]["shed"] = {"GOOSE": 1}
        a = agent(obs)
        picks = [op for op in [a["farmer"], *a["hands"]] if op == ["PICKUP", "GOOSE", 1]]
        self.assertEqual(len(picks), 1)

    def test_feed_inventory_is_reserved_from_sales(self):
        obs = observation()
        obs["private"]["shed"] = {"WHEAT": 10}
        self.assertIn(["SELL", "WHEAT", 6], agent(obs)["market"])

    def test_feed_before_care(self):
        obs = observation()
        obs["farms"][0]["tiles"][4][4] = {"kind": "COOP", "animal": "GOOSE", "fed_today": False,
                                                 "cared_today": False, "yield_units": 0}
        obs["private"]["inventories"] = [{"WHEAT": 1}]
        self.assertEqual(agent(obs)["farmer"], ["FEED"])

    def test_final_day_liquidates_feed_reserve(self):
        obs = observation()
        obs.update(day=29, hour=0, step=696)
        obs["private"]["shed"] = {"WHEAT": 4}
        self.assertIn(["SELL", "WHEAT", 4], agent(obs)["market"])


if __name__ == "__main__":
    unittest.main()
