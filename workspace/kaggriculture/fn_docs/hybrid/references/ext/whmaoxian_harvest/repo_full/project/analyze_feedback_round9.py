"""Audit feedback 3 with official persistent loading and transparent instrumentation.

No engine files or submission files are modified. Observer wrappers call original
functions unchanged; final rewards and every replay observation must match.
"""
from collections import Counter
import argparse
import contextlib
import copy
import hashlib
import importlib
import io
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "research/round9"
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("--replay", default="反馈信息3/111485103.json")
parser.add_argument("--output", default="research/round7/feedback3_report.json")
parser.add_argument("--skip-parity", action="store_true")
parser.add_argument("--source", required=True)
parser.add_argument("--seat", type=int, choices=[0,1])
args = parser.parse_args()
replay_path = ROOT / args.replay
if replay_path.suffix == ".gz":
    import gzip
    GAME = json.loads(gzip.decompress(replay_path.read_bytes()))
else:
    GAME = json.loads(replay_path.read_text(encoding="utf-8"))
SOURCE = ROOT / args.source
with contextlib.redirect_stdout(io.StringIO()):
    import kaggle_environments
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def totals(private):
    total = Counter(private["shed"])
    for inv in private["inventories"]:
        total.update(inv)
    return total


parity = []
for p in ([] if args.skip_parity else ([args.seat] if args.seat is not None else range(2))):
    fn = get_last_callable(SOURCE.read_text(encoding="utf-8"), path=str(SOURCE))
    differences, durations, actual, expected = [], [], [], []
    for t in range(719):
        obs = copy.deepcopy(GAME["steps"][t][p]["observation"])
        obs["step"] = t
        start = time.perf_counter()
        a = fn(obs, GAME["configuration"])
        durations.append(time.perf_counter() - start)
        b = GAME["steps"][t+1][p]["action"]
        actual.append(a)
        expected.append(b)
        if a != b:
            differences.append({"step": t, "generated": a, "recorded": b})
    errors = {k:v for k,v in getattr(fn, "telemetry", {}).items()
              if "error" in k.lower() and isinstance(v, (int, float)) and v > 0}
    parity.append({"seat": p, "entrypoint": fn.__name__, "matching_actions": 719-len(differences),
                   "differences": differences[:5], "actual_action_sha256": hashlib.sha256(canonical(actual).encode()).hexdigest(),
                   "recorded_action_sha256": hashlib.sha256(canonical(expected).encode()).hexdigest(),
                   "max_local_seconds": max(durations), "exposed_nonzero_error_counters": errors})
    print("parity", p, parity[-1]["matching_actions"], flush=True)

metrics = [{"sales_units": Counter(), "sales_revenue": Counter(), "floor_sales_units": Counter(),
            "purchase_cost": Counter(), "purchase_units": Counter(), "operations": Counter(),
            "nonpass_unchanged_operations": Counter(), "overflow": Counter(), "overflow_events": [],
            "hire_cost": 0, "land_cost": 0, "hires": 0,
            "sales_by_day": {}, "nonpass_unchanged_examples": []} for _ in range(2)]
ctx = {"step": 0, "apply_seat": -1, "farms": {}, "private": {}}
original = {name: getattr(engine, name) for name in
            ("_apply_unit_action", "_process_market", "_commit_unit", "_drop_inventories_to_shed", "_do_hire", "_do_buy_land")}


def observed_apply(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
    if idx == 0:
        ctx["apply_seat"] += 1
    seat = ctx["apply_seat"]
    ctx["farms"][id(farm)] = seat
    ctx["private"][id(private)] = seat
    op = action[0] if isinstance(action, list) and action else "MALFORMED"
    row = metrics[seat]
    row["operations"][op] += 1
    pos = engine._farmer_position(farm, idx)
    tile = farm["tiles"][pos[1]][pos[0]] if pos else None
    before = canonical([pos, tile, private, farm["money"]]) if op != "PASS" else None
    carried_before = totals(private) if op == "DROP" else None
    result = original["_apply_unit_action"](farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
    if op != "PASS":
        after_pos = engine._farmer_position(farm, idx)
        after_tile = farm["tiles"][after_pos[1]][after_pos[0]] if after_pos else None
        after = canonical([after_pos, after_tile, private, farm["money"]])
        if before == after:
            row["nonpass_unchanged_operations"][op] += 1
            if len(row["nonpass_unchanged_examples"]) < 25:
                row["nonpass_unchanged_examples"].append({"step": ctx["step"], "unit": idx, "action": action, "position": pos})
    if carried_before is not None:
        lost = carried_before - totals(private)
        if lost:
            row["overflow"].update(lost)
            row["overflow_events"].append({"step": ctx["step"], "kind": "manual_drop", "unit": idx, "lost": dict(lost)})
    return result


def observed_market(state, env):
    ctx["farms"] = {id(f): p for p, f in enumerate(state[0].observation.farms)}
    ctx["private"] = {id(s.observation.private): p for p, s in enumerate(state)}
    return original["_process_market"](state, env)


def observed_commit(op, item, price, farm, private, market, shed_capacity=100):
    result = original["_commit_unit"](op, item, price, farm, private, market, shed_capacity)
    if result:
        row = metrics[ctx["farms"][id(farm)]]
        if op == "SELL":
            row["sales_units"][item] += 1
            row["sales_revenue"][item] += price
            if price == 1:
                row["floor_sales_units"][item] += 1
            day = str(ctx["step"] // 24)
            row["sales_by_day"][day] = row["sales_by_day"].get(day, 0) + price
        else:
            row["purchase_cost"][op+":"+item] += price
            row["purchase_units"][op+":"+item] += 1
    return result


def observed_drop(private, capacity):
    before = totals(private)
    result = original["_drop_inventories_to_shed"](private, capacity)
    lost = before - totals(private)
    if lost:
        row = metrics[ctx["private"][id(private)]]
        row["overflow"].update(lost)
        row["overflow_events"].append({"step": ctx["step"], "kind": "end_of_day", "lost": dict(lost)})
    return result


def observed_hire(farm, private, board_size, mult=1):
    before_money, before_hires = farm["money"], farm["hires_today"]
    result = original["_do_hire"](farm, private, board_size, mult)
    row = metrics[ctx["farms"][id(farm)]]
    row["hire_cost"] += before_money - farm["money"]
    row["hires"] += farm["hires_today"] - before_hires
    return result


def observed_land(farm, board_size):
    before = farm["money"]
    result = original["_do_buy_land"](farm, board_size)
    metrics[ctx["farms"][id(farm)]]["land_cost"] += before - farm["money"]
    return result


def tape(seat):
    def play(obs, cfg=None):
        ctx["step"] = int(obs.step)
        ctx["apply_seat"] = -1
        return GAME["steps"][int(obs.step)+1][seat]["action"]
    return play


for name, fn in (("_apply_unit_action", observed_apply), ("_process_market", observed_market),
                 ("_commit_unit", observed_commit), ("_drop_inventories_to_shed", observed_drop),
                 ("_do_hire", observed_hire), ("_do_buy_land", observed_land)):
    setattr(engine, name, fn)
try:
    env = make("kaggriculture", configuration=dict(GAME["configuration"], seed=GAME["info"]["seed"]), debug=True)
    env.run([tape(0), tape(1)])
finally:
    for name, fn in original.items():
        setattr(engine, name, fn)
assert [s.reward for s in env.steps[-1]] == GAME["rewards"]
assert len(env.steps) == len(GAME["steps"]) == 720
observation_mismatches = []
for t in range(720):
    for p in range(2):
        actual = dict(env.steps[t][p].observation)
        expected = dict(GAME["steps"][t][p]["observation"])
        for value in (actual, expected):
            value.pop("remainingOverageTime", None)
            value["step"] = t
        if actual != expected:
            observation_mismatches.append([t, p])
assert not observation_mismatches, observation_mismatches[:10]

for p, row in enumerate(metrics):
    snapshots = []
    for t in [0, 24, 72, 144, 240, 480, 696, 719]:
        obs = GAME["steps"][t][p]["observation"]
        farm = obs["farms"][p]
        mix = Counter(tile.get("animal") or tile.get("crop") or tile.get("kind") for line in farm["tiles"]
                      for tile in line if isinstance(tile, dict))
        snapshots.append({"step": t, "money": farm["money"], "land": len(farm["unlocked_quadrants"]),
                          "farm_mix": dict(mix), "shed": obs["private"]["shed"],
                          "carried": dict(totals(obs["private"])-Counter(obs["private"]["shed"]))})
    row["snapshots"] = snapshots
    row["final_inventory"] = dict(totals(GAME["steps"][-1][p]["observation"]["private"]))
    row["final_seeds"] = GAME["steps"][-1][p]["observation"]["private"]["seeds"]
    row["final_unharvested"] = dict(Counter())
    unharvested = Counter()
    for line in GAME["steps"][-1][p]["observation"]["farms"][p]["tiles"]:
        for tile in line:
            if isinstance(tile, dict) and tile.get("yield_units", 0) > 0:
                unharvested[tile.get("animal") or tile.get("crop")] += tile["yield_units"]
    row["final_unharvested"] = dict(unharvested)
    row["money_identity"] = 3000 + sum(row["sales_revenue"].values()) - sum(row["purchase_cost"].values()) - row["hire_cost"] - row["land_cost"]
    assert row["money_identity"] == GAME["rewards"][p]

logs = []
for p in range(2):
    log_path = replay_path.parent / f"{GAME['info']['EpisodeId']}-{p}.json"
    if not log_path.exists():
        continue
    raw = json.loads(log_path.read_text())
    flat = [v for row in raw for v in row]
    logs.append({"seat": p, "records": len(flat), "stderr_count": sum(bool(v.get("stderr", "").strip()) for v in flat),
                 "stdout_count": sum(bool(v.get("stdout", "").strip()) for v in flat),
                 "max_action_seconds": max(v["duration"] for v in flat),
                 "total_action_seconds": sum(v["duration"] for v in flat),
                 "seconds_above_one": sum(max(v["duration"]-1, 0) for v in flat)})
report = {"episode_id": GAME["info"]["EpisodeId"], "classification": "self_validation" if GAME["info"]["TeamNames"][0] == GAME["info"]["TeamNames"][1] else "public_ladder_game",
          "names": GAME["info"]["TeamNames"], "submission_id": None, "seed": GAME["info"]["seed"],
          "rewards": GAME["rewards"], "statuses": GAME["statuses"], "states": 720,
          "environment_version": kaggle_environments.__version__, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "persistent_official_entrypoint_parity": parity, "logs": logs,
          "instrumented_reproduction": {"unchanged_engine_functions_called": True,
                                       "all_1440_observations_equal_excluding_timing": True,
                                       "final_rewards_equal": True},
          "metrics": metrics,
          "limitations": ["A self validation episode cannot explain recent ladder rating changes.",
                          "Unchanged unit operations include harmless empty DROP/PICKUP and redundant WATER; not every such operation has a profitable replacement.",
                          "Final unharvested output is not recoverable coin value: reachability, remaining actions and marginal price matter."]}
(ROOT / args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"logs": logs, "metrics": [{k: v for k, v in m.items() if k not in {"snapshots", "nonpass_unchanged_examples", "sales_by_day"}} for m in metrics]}, ensure_ascii=False), flush=True)
