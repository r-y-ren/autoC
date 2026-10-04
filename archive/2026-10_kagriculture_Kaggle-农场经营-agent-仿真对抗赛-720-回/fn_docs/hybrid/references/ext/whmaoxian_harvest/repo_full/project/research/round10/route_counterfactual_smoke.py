"""One-world, in-memory official-engine route counterfactual for mechanism diagnosis.

This deliberately does not construct a deployable agent or use Round 10 held-out
worlds. Both games use the same frozen V9 source and public DSM reconstruction;
only one Chassis router choice is changed before the day-6 route is committed.
"""

import contextlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V9 = ROOT / "submissions/release_v9/main.py"
OPP = ROOT / "experiments/round8_top2_dsm_strict.py"
SEED = 242588832  # Already-inspected Round 9 diagnostic world; not Round 10.


def run(force_route):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable

    candidate = get_last_callable(V9.read_text(encoding="utf-8"), path=str(V9))
    opponent = get_last_callable(OPP.read_text(encoding="utf-8"), path=str(OPP))
    chassis = candidate.__globals__["_IMPL"].chassis
    original_router = chassis.router
    route_log = []

    if force_route is not None:
        def choose(obs, step, state):
            route = original_router(obs, step, state)
            if step >= 144 and not state.get("day27") and not state.get("diagnostic_route_set"):
                shops = tuple(obs["town"]["unlocked_shops"][:2])
                assert route == 105, (shops, route)
                state["route"] = force_route
                state["diagnostic_route_set"] = True
                route_log.append({"step": step, "shops": shops, "native": route, "forced": force_route})
                return force_route
            return route
        chassis.router = choose

    env = make("kaggriculture", configuration={"seed": SEED, "episodeSteps": 720}, debug=True)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        env.run([candidate, opponent])
    out = {"seed": SEED, "route_log": route_log, "statuses": [x.status for x in env.steps[-1]],
           "money": [env.steps[-1][i].observation.farms[i]["money"] for i in (0, 1)],
           "shops": list(env.steps[-1][0].observation.town["unlocked_shops"]),
           "daily": []}
    for day in (6, 7, 10, 14, 17, 20, 23, 26, 29):
        obs = env.steps[day * 24 + 23][0].observation
        farm = obs.farms[0]
        animals = {}
        for row in farm["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and "animal" in tile:
                    k = tile["animal"]
                    animals[k] = animals.get(k, 0) + 1
        out["daily"].append({"day": day, "money": farm["money"], "animals": animals,
                             "shed": {k: obs.private["shed"].get(k, 0) for k in ("EGG", "MILK", "WHEAT")},
                             "prices": {k: obs.market["prices"].get(k, 0) for k in ("EGG", "MILK", "WHEAT")}})
    return out


if __name__ == "__main__":
    result = {"baseline_105": run(None), "forced_101": run(101)}
    path = ROOT / "research/round10/route_counterfactual_smoke.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: {"money": v["money"], "route_log": v["route_log"], "statuses": v["statuses"]}
                      for k, v in result.items()}, ensure_ascii=False))
