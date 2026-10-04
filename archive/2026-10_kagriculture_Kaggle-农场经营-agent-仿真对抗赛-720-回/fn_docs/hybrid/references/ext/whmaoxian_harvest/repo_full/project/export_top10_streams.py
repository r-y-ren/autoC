"""Observe actual committed sales while reproducing study episodes exactly."""
from collections import Counter
import contextlib
import gzip
import importlib
import io
import json
from pathlib import Path
from benchmark_replays import tape_policy

with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
root = Path(__file__).parent / "research/top10"
items = ("MILK", "WOOL", "STRAWBERRY", "EGG", "MELON")
original_market, original_commit = engine._process_market, engine._commit_unit
context = {}


def observe_market(state, env):
    context["turn"] += 1
    context["farms"] = [id(f) for f in state[0].observation.farms]
    return original_market(state, env)


def observe_commit(op, item, price, farm, private, market, shed_capacity=100):
    ok = original_commit(op, item, price, farm, private, market, shed_capacity)
    if ok and op == "SELL" and item in items and price > 1:
        p = context["farms"].index(id(farm))
        context["events"][p][(context["turn"], items.index(item))] += 1
    return ok


engine._process_market, engine._commit_unit = observe_market, observe_commit
output, done = [], {}
for row in json.loads((root / "index.json").read_text()):
    if row["split"] != "study":
        continue
    eid, seat = row["episode_id"], row["seat"]
    data = json.loads(gzip.decompress((root / f"{eid}.json.gz").read_bytes()))
    if eid not in done:
        context.update(turn=-1, events=[Counter(), Counter()])
        config = dict(data["configuration"], seed=data["info"]["seed"])
        env = make("kaggriculture", configuration=config, debug=True)
        env.run([tape_policy([s[p]["action"] for s in data["steps"][1:]]) for p in range(2)])
        assert [s.reward for s in env.steps[-1]] == data["rewards"]
        assert context["turn"] == 718
        done[eid] = context["events"]
    profiles = {}
    for t in range(0, 720, 24):
        farm = data["steps"][t][seat]["observation"]["farms"][seat]
        profiles[t] = dict(Counter(x.get("animal") or x.get("crop") for r in farm["tiles"]
                                  for x in r if isinstance(x, dict) and (x.get("animal") or x.get("crop"))))
    shops = data["steps"][-1][seat]["observation"]["town"]["unlocked_shops"][:2]
    output.append({"episode": eid, "seat": seat, "team": row["team"], "shops": shops,
                   "events": [[t, i, q] for (t, i), q in sorted(done[eid][seat].items()) if q >= 2],
                   "profiles": profiles})
    (root / "study_market_streams.json").write_text(json.dumps(output), encoding="utf-8")
    print(row["team"], len(output[-1]["events"]), flush=True)
engine._process_market, engine._commit_unit = original_market, original_commit
