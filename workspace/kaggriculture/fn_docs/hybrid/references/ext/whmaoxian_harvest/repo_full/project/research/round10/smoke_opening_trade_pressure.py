"""Two full official-engine mechanics games against a synthetic opening stress.

The rival uses the frozen V9 policy after two deliberately changed market
orders: step 0 BUY 10 / SELL 10, step 1 BUY 5.  This opponent is an artificial
stress case, not a league competitor or evidence about a ranked player.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V9 = ROOT / "submissions" / "release_v9" / "main.py"
V2 = ROOT / "experiments" / "round10_opening_cash_v2.py"
OUT = ROOT / "research" / "round10" / "opening_trade_pressure_smoke.json"
V9_SHA = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
V2_SHA = "2dd1f8a0ad6452cda35fd6b90423912e3bc38418ebef98bd876d8ead97021ba7"
SEED = int.from_bytes(hashlib.sha256(b"r10-opening-trade-pressure-only").digest()[:4], "big") % 2_000_000_000


def checkpoint(env, step):
    obs = env.steps[step][0].observation
    farm = obs.farms[0]
    return {
        "cash": farm["money"],
        "hands": len(farm["hands"]),
        "hires_today": farm["hires_today"],
        "wheat_shed": obs.private["shed"].get("WHEAT", 0),
    }


def main():
    assert hashlib.sha256(V9.read_bytes()).hexdigest() == V9_SHA
    assert hashlib.sha256(V2.read_bytes()).hexdigest() == V2_SHA
    seeds = json.loads((ROOT / "research" / "round10" / "league_seeds.json").read_text(encoding="utf-8"))
    assert SEED not in {s for values in seeds.values() for s in values}

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable

    output = {"seed": SEED, "opponent": "synthetic V9: step0 BUY10/SELL10, step1 extra BUY5", "games": {}}
    for label, file in (("v9", V9), ("v2_15_10", V2)):
        hero = get_last_callable(file.read_text(encoding="utf-8"), path=str(file))
        rival_core = get_last_callable(V9.read_text(encoding="utf-8"), path=str(V9))
        called = []

        def rival(obs, config=None):
            step = int(obs["step"])
            action = rival_core(obs, config)
            if step == 0:
                assert action["market"][:2] == [["BUY_PRODUCT", "WHEAT", 20], ["SELL", "WHEAT", 15]]
                action = copy.deepcopy(action)
                action["market"][:2] = [["BUY_PRODUCT", "WHEAT", 10], ["SELL", "WHEAT", 10]]
            elif step == 1:
                assert len(action["market"]) < 10
                action = copy.deepcopy(action)
                action["market"].insert(0, ["BUY_PRODUCT", "WHEAT", 5])
            if step < 2:
                called.append({"step": step, "market": action["market"]})
            return action

        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": SEED}, debug=True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env.run([hero, rival])
        final = env.steps[-1]
        assert all(s.status == "DONE" for s in final)
        output["games"][label] = {
            "rewards": [s.reward for s in final],
            "status": [s.status for s in final],
            "rival_opening": called,
            "hero_opening": [env.steps[i][0].action["market"] for i in (1, 2)],
            "hero_day1_first_market": env.steps[25][0].action["market"],
            "after_step_0": checkpoint(env, 1),
            "after_day_0": checkpoint(env, 24),
            "after_day_1_hour_0": checkpoint(env, 25),
            "after_day_1_hour_1": checkpoint(env, 26),
            "after_day_1": checkpoint(env, 48),
        }
    output["warning"] = "Synthetic rival and one fixed seed; mechanism smoke only, excluded from league scoring."
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
