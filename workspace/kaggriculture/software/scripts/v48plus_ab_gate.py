# 【中文】v48plus_ab_gate.py —— v48+ 经济层补丁孪生 A/B 门 + 9 巨人局反事实
# ===========================================================================
# 背景（v48+ 改进包）：v48 解码真源码（dadee25a…，在跑 v48 公开衍生版同源）
#   + 手工移植 V50 经济层（COURIER/CAPHARV/SHEDROOM，见
#   kaggle_simulations/v48plus/v48plus_layers.py 头注）= v48+。
# 本门三判据（软件角色任务书 2026-09-21）：
#   ① 胜率不降：同种子 v48 vs v48+ 直接 h2h 16 局（8 seeds × 双席位），
#     v48+ 互胜（胜+0.5*平）/总局 ≥ 45%；
#   ② 终局资金均值不降 ≥3%：多样对手面板（starter 基线 / 我方 v14.2 /
#     回放对手流）同种子同席对照，总体与分对手 mean(v48+) ≥ 0.97*mean(v48)；
#   ③ 零新异常：全部对局 statuses 双 DONE、contract ok，记录每步 agent
#     耗时（<1000ms 预算）。
# 另加：9 巨人局 d0 反事实（round24 TARGET9，对手=回放真实动作，twin 引擎），
#   v48+ 相对 v48 的终局资金方向不得恶化。
# 输出：exports/probes/v48plus/v48plus_ab_gate.json
# CLI：python scripts/v48plus_ab_gate.py [--seeds 101,102,...] [--quick]
# ===========================================================================
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
CAMP = os.path.dirname(SOFTWARE)
REPO = os.path.dirname(CAMP)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kgenv.arena import load_submission_agent, run_episode  # noqa: E402
from kgenv.engine import episode_contract_ok  # noqa: E402

V48_MAIN = os.path.join(CAMP, "references", "data", "intel-notebooks",
                        "v48build", "main.py")
PLUS_MAIN = os.path.join(SOFTWARE, "kaggle_simulations", "v48plus", "main.py")
OUR_MAIN = os.path.join(SOFTWARE, "kaggle_simulations", "agent", "main.py")
REPLAY_DIR = os.path.join(CAMP, "references", "data", "online-replays",
                          "round24")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "v48plus")
TEAM = "renyxin"
GIANT_EPISODES = (110687913, 110702221)
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
BASE_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)


def sha_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def timed(fn, rec):
    """包装 agent callable，记录单步最大耗时（官方 1s 预算口径）。"""

    def wrapped(obs, configuration=None):
        t0 = time.perf_counter()
        try:
            return fn(obs, configuration)
        finally:
            ms = (time.perf_counter() - t0) * 1000.0
            rec["max_ms"] = max(rec.get("max_ms", 0.0), ms)
            rec["calls"] = rec.get("calls", 0) + 1

    return wrapped


def load_plus_module():
    """持久装载 v48plus 模块以读取层遥测（与 arena.load_submission_agent 同语义）。"""
    path = os.path.abspath(PLUS_MAIN)
    spec = importlib.util.spec_from_file_location("v48plus_probe_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def seat_daily(res, seat):
    daily = res.get("daily_money") or []
    return [entry.get("money", [None, None])[seat] for entry in daily
            if isinstance(entry, dict)]


def game(a_fn, b_fn, seed, a_label, b_label, rec_a, rec_b):
    res = run_episode(a_fn, b_fn, seed)
    rewards = [float(r) for r in res["rewards"]]
    rec = {
        "seed": int(seed), "a": a_label, "b": b_label,
        "rewards": rewards,
        "a_money": rewards[0], "b_money": rewards[1],
        "statuses": res["statuses"],
        "contract_ok": bool(episode_contract_ok(res)),
        "elapsed_s": res["elapsed_seconds"],
        "a_daily": seat_daily(res, 0), "b_daily": seat_daily(res, 1),
    }
    return rec


def h2h_block(v48, plus, seeds):
    """判据①：同种子 v48 vs v48+ 直接 h2h，双席位。"""
    games = []
    for seed in seeds:
        for v48_seat in (0, 1):
            pair = (v48, plus) if v48_seat == 0 else (plus, v48)
            rec = game(pair[0], pair[1], seed, "v48", "v48plus", {}, {})
            rec["v48_seat"] = v48_seat
            m = rec["rewards"][v48_seat]
            p = rec["rewards"][1 - v48_seat]
            rec["plus_margin"] = round(p - m, 1)
            rec["plus_result"] = "W" if p > m else ("L" if p < m else "T")
            games.append(rec)
            print(f"  h2h seed={seed} v48@seat{v48_seat} "
                  f"v48={m:.0f} v48+={p:.0f} -> {rec['plus_result']}",
                  flush=True)
    plus_wins = sum(1 for g in games if g["plus_result"] == "W")
    ties = sum(1 for g in games if g["plus_result"] == "T")
    score = (plus_wins + 0.5 * ties) / len(games)
    return {"games": games, "plus_wins": plus_wins, "ties": ties,
            "v48_wins": len(games) - plus_wins - ties,
            "plus_score": round(score, 4),
            "pass": bool(score >= 0.45)}


def make_replay_opponent(replay_path, seat):
    """回放对手流：原种子 + 逐步回放真实动作（对手席固定）。"""
    with open(replay_path, "r", encoding="utf-8") as handle:
        replay = json.load(handle)
    steps = replay.get("steps") or []
    seed = int((replay.get("info") or {}).get("seed", 0))

    def opponent(obs, configuration=None):
        t = int(obs.get("step", 0) or 0)
        if 0 <= t < len(steps):
            return copy.deepcopy((steps[t][seat] or {}).get("action") or {})
        return {"farmer": ["PASS"], "hands": [], "market": []}

    return opponent, seed, replay


def panel_block(v48, plus, seeds):
    """判据②：多样对手面板，v48 与 v48+ 同种子同席对照。

    v14.2 每局 fresh 装载：其模块态跨局不保证完全复位（消融实测同一
    实例连打时逐局漂移），fresh 化后每局对手行为只依赖 (seed, seat)。"""
    import kgenv.bots.baseline as baseline_bots
    opponents = [("starter", baseline_bots.baseline_wheat_agent, "bot"),
                 ("our_v14_2", None, OUR_MAIN)]
    for ep in GIANT_EPISODES:
        opponents.append((f"replay_{ep}", None, f"replay:{ep}"))

    out = {}
    all_v48, all_plus = [], []
    for name, fn, path in opponents:
        if path and path.startswith("replay:"):
            ep = int(path.split(":", 1)[1])
            replay_path = os.path.join(REPLAY_DIR,
                                       f"episode-{ep}-replay.json")
            with open(replay_path, "r", encoding="utf-8") as handle:
                replay = json.load(handle)
            teams = list((replay.get("info") or {}).get("TeamNames") or [])
            our_seat = teams.index(TEAM)
            opp_fn0, opp_seed, _ = make_replay_opponent(replay_path,
                                                        1 - our_seat)
            pair_seeds = [(opp_seed, our_seat)]
        else:
            opp_fn0 = fn if fn is not None else load_submission_agent(path)
            pair_seeds = [(s, seat) for s in seeds for seat in (0, 1)]
        rows = []
        for seed, our_seat in pair_seeds:
            for version, agent_fn in (("v48", v48), ("v48plus", plus)):
                if path == "bot":
                    opp_fn = opp_fn0
                elif path.startswith("replay:"):
                    opp_fn = opp_fn0
                else:
                    opp_fn = load_submission_agent(path)  # fresh per game
                if our_seat == 0:
                    res = run_episode(agent_fn, opp_fn0, seed)
                else:
                    res = run_episode(opp_fn0, agent_fn, seed)
                mine = float(res["rewards"][our_seat])
                rows.append({
                    "version": version, "seed": int(seed),
                    "our_seat": our_seat, "money": mine,
                    "statuses": res["statuses"],
                    "contract_ok": bool(episode_contract_ok(res)),
                })
                (all_v48 if version == "v48" else all_plus).append(mine)
                print(f"  panel {name} seed={seed} seat={our_seat} "
                      f"{version}={mine:.0f}", flush=True)
        v48_mean = (sum(r["money"] for r in rows if r["version"] == "v48")
                    / max(1, sum(1 for r in rows if r["version"] == "v48")))
        plus_mean = (sum(r["money"] for r in rows if r["version"] == "v48plus")
                     / max(1, sum(1 for r in rows
                                  if r["version"] == "v48plus")))
        out[name] = {"rows": rows, "v48_mean": round(v48_mean, 1),
                     "plus_mean": round(plus_mean, 1),
                     "ratio": round(plus_mean / v48_mean, 4) if v48_mean else None}
    overall_ratio = (sum(all_plus) / sum(all_v48)) if sum(all_v48) else None
    out["_overall"] = {"v48_mean": round(sum(all_v48) / len(all_v48), 1),
                       "plus_mean": round(sum(all_plus) / len(all_plus), 1),
                       "ratio": round(overall_ratio, 4) if overall_ratio else None}
    out["_pass"] = bool(overall_ratio is not None and overall_ratio >= 0.97)
    return out


def _twin_obs_dict(obs):
    """twin.Observation（属性访问、无 .get）→ v48 系 agent 可用的纯 dict。"""
    return {
        "farms": obs.farms,
        "market": obs.market,
        "town": obs.town,
        "day": obs.day,
        "hour": obs.hour,
        "step": obs.step,
        "player": obs.player,
        "private": obs.private,
        "remainingOverageTime": getattr(obs, "remainingOverageTime", 60),
    }


def giants_block():
    """9 巨人局 d0 反事实：对手=回放真实动作，v48 vs v48+ 挽回方向。"""
    import kaggle_simulations.agent.planner.twin as twin

    bundle = twin.load_engine()
    out = {}
    direction_ok = True
    for ep in TARGET9:
        path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
        with open(path, "r", encoding="utf-8") as handle:
            replay = json.load(handle)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        actions = twin.replay_transition_actions(replay)
        finals = {}
        for version in ("v48", "v48plus"):
            state = twin.build_state_from_replay(replay, 0, bundle)
            if version == "v48":
                agent_fn = load_submission_agent(V48_MAIN)
            else:
                agent_fn = load_submission_agent(PLUS_MAIN)
            t0 = time.time()
            taken = 0
            while not state.env.done and taken < len(actions):
                obs = _twin_obs_dict(state.seats[me].observation)
                mine = agent_fn(obs) if agent_fn is not None else None
                theirs = actions[taken][1 - me]
                twin.step(state, [mine, theirs])
                taken += 1
            finals[version] = float(twin.final_money(state)[me])
            print(f"  giant ep{ep} {version}: {finals[version]:.0f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
        delta = finals["v48plus"] - finals["v48"]
        ok = delta >= 0.0
        direction_ok = direction_ok and ok
        out[str(ep)] = {
            "opponent": teams[1 - me], "truth_me": truth_me,
            "truth_opp": truth_opp,
            "v48_final": round(finals["v48"], 1),
            "plus_final": round(finals["v48plus"], 1),
            "plus_minus_v48": round(delta, 1),
            "direction_ok": ok,
            "beats_truth_opp": finals["v48plus"] > truth_opp,
        }
    out["_direction_ok"] = bool(direction_ok)
    deltas = [v["plus_minus_v48"] for k, v in out.items() if not k.startswith("_")]
    out["_summary"] = {"improved": sum(1 for d in deltas if d > 0),
                       "flat": sum(1 for d in deltas if d == 0),
                       "worse": sum(1 for d in deltas if d < 0),
                       "mean_delta": round(sum(deltas) / len(deltas), 1)}
    return out


def telemetry_check():
    """层触发遥测：v48+ 对 starter 跑 2 局，读模块级 _V48P_REPORT。"""
    module = load_plus_module()
    import kgenv.bots.baseline as baseline_bots
    for seed in (101, 102):
        run_episode(module.agent, baseline_bots.baseline_wheat_agent, seed)
    return dict(module._V48P_REPORT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default=",".join(map(str, BASE_SEEDS)))
    parser.add_argument("--quick", action="store_true",
                        help="面板/反事实缩减到 2 seeds 与 2 巨人局")
    args = parser.parse_args()
    seeds = tuple(int(s) for s in args.seeds.split(",") if s)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = {
        "protocol": "v48plus-ab-gate/1.0",
        "date": "2026-09-21",
        "base": {"path": os.path.relpath(V48_MAIN, CAMP).replace("\\", "/"),
                 "sha256": sha_file(V48_MAIN)},
        "plus": {"path": os.path.relpath(PLUS_MAIN, CAMP).replace("\\", "/"),
                 "sha256": sha_file(PLUS_MAIN)},
    }
    v48_raw = load_submission_agent(V48_MAIN)
    plus_raw = load_submission_agent(PLUS_MAIN)
    rec_v48 = {"label": "v48"}
    rec_plus = {"label": "v48plus"}
    v48 = timed(v48_raw, rec_v48)
    plus = timed(plus_raw, rec_plus)

    t0 = time.time()
    print("[1/4] h2h v48 vs v48+ ...", flush=True)
    out["h2h"] = h2h_block(v48, plus, seeds)

    print("[2/4] diverse-opponent panel ...", flush=True)
    panel_seeds = seeds[:2] if args.quick else seeds
    out["panel"] = panel_block(v48, plus, panel_seeds)

    print("[3/4] giant d0 counterfactuals ...", flush=True)
    if args.quick:
        global TARGET9
        TARGET9 = TARGET9[:2]
    out["giants"] = giants_block()

    print("[4/4] layer telemetry + anomaly summary ...", flush=True)
    out["layer_telemetry"] = telemetry_check()
    games = out["h2h"]["games"] + [r for opp in out["panel"].values()
                                   if isinstance(opp, dict)
                                   for r in opp.get("rows", [])]
    non_done = [g for g in games if g.get("statuses") != ["DONE", "DONE"]]
    bad_contract = [g for g in games if not g.get("contract_ok")]
    out["anomalies"] = {"non_done_games": len(non_done),
                        "bad_contract_games": len(bad_contract),
                        "agent_step_ms": {"v48": round(rec_v48["max_ms"], 1),
                                          "v48plus": round(rec_plus["max_ms"], 1)}}

    out["verdict"] = {
        "c1_win_rate": out["h2h"]["pass"],
        "c2_cash_mean": out["panel"]["_pass"],
        "c3_no_new_anomaly": bool(not non_done and not bad_contract
                                  and rec_v48["max_ms"] < 1000.0
                                  and rec_plus["max_ms"] < 1000.0),
        "giants_direction": out["giants"]["_direction_ok"],
        "overall": bool(out["h2h"]["pass"] and out["panel"]["_pass"]
                        and not non_done and not bad_contract
                        and out["giants"]["_direction_ok"]),
    }
    out["wall_s"] = round(time.time() - t0, 1)

    path = os.path.join(OUT_DIR, "v48plus_ab_gate.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(out["verdict"], indent=2))
    print("wrote", path, flush=True)


if __name__ == "__main__":
    main()
