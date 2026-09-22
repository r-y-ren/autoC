# -*- coding: utf-8 -*-
# 【中文】gate_common.py —— v48_hybrid F3 离线门共享基建
# ===========================================================================
# 职责（verify_offline_gates / verify_patch_safety 共用，只读消费现有件）：
#   * 官方真引擎单局运行器（kaggle_environments.make 直驱，与 kgenv
#     engine.run_episode 同配置：episodeSteps=720 / actTimeout=60 /
#     debug=True），额外捕获双席完整动作流（launch-check norm_action
#     口径）与异常集（arena._abnormal_reason 口径 + 可疑日志行口径）；
#   * agent 装载：kgenv.arena.load_submission_agent（get_last_callable
#     同语义；named `agent` 优先），每席每局**全新装载**（P2 经济护栏带
#     模块级 streak 状态，_v48_load 每次装载生成新模块实例，天然按席
#     隔离——与官方每席独立装载语义一致）；
#   * 合成语料头构造（scripts/planner_flagoff_golden.synthetic_season_head
#     同构：NW 解锁/3000 起始/引擎 MARKET_PARAMS 初值，info.seed=固定
#     种子驱动杂草与商店随机）；
#   * 孪生整季自打驱动器（双席 agent 驱动 twin.step，逐步记录框架形态
#     回放 steps + 动作流 + 可选逐步回调 on_step(seat, obs, action) 供
#     P2/P3 触发遥测）。
# 产物纪律：本文件与其余 gate 脚本均为 v48_hybrid/ 新增产物；不修改任何
#   现存文件；临时件落 v48_hybrid/tmp/。
# ===========================================================================
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))            # gates/
HYB = os.path.dirname(HERE)                                   # v48_hybrid/
KSIM = os.path.dirname(HYB)                                   # kaggle_simulations/
SOFTWARE = os.path.dirname(KSIM)                              # software/
CAMP = os.path.dirname(SOFTWARE)                              # 战役根
FN_WORK_ROB = os.path.join(CAMP, "fn_work", "src",
                           "run_official_bench")

for _p in (SOFTWARE, FN_WORK_ROB):
    if _p not in sys.path:
        sys.path.insert(0, _p)

sys.dont_write_bytecode = True

FULL_STEPS = 720
ACT_TIMEOUT = 60.0

# 身份链（与 build_manifest.json 对齐，装载期再实测校验）
BASE_MAIN = os.path.join(KSIM, "v48_derivative", "main.py")
BASE_SHA256 = ("dadee25a9840313218384208c53b2c4752f82c3209"
               "cc654632e0b96c65e2664a")
HYB_MAIN = os.path.join(HYB, "main.py")
V72_MAIN = os.path.join(KSIM, "opponents", "v72_main.py")
TMP_DIR = os.path.join(HYB, "tmp")
OUT_DIR = os.path.join(HERE, "out")

AGENT_PATHS = {
    "hybrid_all_on": HYB_MAIN,
    "pure_v48": BASE_MAIN,
    "v72": V72_MAIN,
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_agent(path: str):
    """按官方提交语义全新装载一个 agent 实例（named `agent` 优先）。"""
    from kgenv.arena import load_submission_agent
    return load_submission_agent(path)


def load_pool_bot(name: str):
    from kgenv.bots import online_pool
    return online_pool.ONLINE_STYLE_OPPONENTS[name]


def norm_action(a) -> str:
    """动作规范化串（scripts/v48_derivative_launch_check.norm_action 同口径）。"""
    if isinstance(a, (list, tuple)):
        return "[" + ",".join(norm_action(x) for x in a) + "]"
    if isinstance(a, dict):
        return "{" + ",".join(f"{k}:{norm_action(a[k])}"
                              for k in sorted(a)) + "}"
    if isinstance(a, float):
        return f"{a:.4f}"
    return json.dumps(a, ensure_ascii=False, sort_keys=True)


def action_stream_sha256(seat_actions) -> str:
    parts = []
    for seat in (0, 1):
        for act in seat_actions[seat]:
            parts.append(norm_action(act))
    return sha256_bytes("\n".join(parts).encode("utf-8"))


def first_stream_diff(sa, sb, limit=3):
    """两动作流首个差异定位 [{seat, step, a, b}...]；一致返回 []。"""
    out = []
    for seat in (0, 1):
        aa, ab = sa[seat], sb[seat]
        for i in range(max(len(aa), len(ab))):
            va = aa[i] if i < len(aa) else "<missing>"
            vb = ab[i] if i < len(ab) else "<missing>"
            if norm_action(va) != norm_action(vb):
                out.append({"seat": seat, "step": i,
                            "a": norm_action(va)[:160],
                            "b": norm_action(vb)[:160]})
                if len(out) >= limit:
                    return out
    return out


# ---------------------------------------------------------------------------
# 官方真引擎单局（动作流捕获 + 异常集）
# ---------------------------------------------------------------------------
def game_anomalies(statuses, rewards, turns_played, suspicious_logs):
    """单局异常集（kind 列表）。口径=arena._abnormal_reason + launch-check
    可疑日志行（ERROR / Timed out / Traceback）。"""
    kinds = []
    if list(statuses) != ["DONE", "DONE"]:
        kinds.append("non_done_status")
    if not (isinstance(rewards, list) and len(rewards) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                    and math.isfinite(float(v)) for v in rewards)):
        kinds.append("nonfinite_reward")
    if turns_played != FULL_STEPS:
        kinds.append("turns_mismatch")
    if suspicious_logs:
        kinds.append("engine_error_log")
    return kinds


def run_engine_game(fn0, fn1, seed: int) -> dict:
    """官方引擎单局：返回 rewards/statuses/turns/双席动作流/异常集。"""
    from kaggle_environments import make
    t0 = time.perf_counter()
    env = make("kaggriculture",
               configuration={"episodeSteps": FULL_STEPS, "seed": int(seed),
                              "actTimeout": ACT_TIMEOUT},
               debug=True)
    env.run([fn0, fn1])
    elapsed = time.perf_counter() - t0
    final = env.steps[-1]
    rewards = [float(s["reward"]) for s in final]
    statuses = [s["status"] for s in final]
    seat_actions = [[], []]
    for index in range(1, len(env.steps)):
        for seat in (0, 1):
            seat_actions[seat].append(env.steps[index][seat].get("action")
                                      or {})
    raw_logs = [str(line) for line in getattr(env, "logs", []) if line]
    suspicious = [s[:300] for s in raw_logs
                  if "ERROR" in s or "Timed out" in s or "Traceback" in s]
    winner = None
    if rewards[0] > rewards[1]:
        winner = 0
    elif rewards[1] > rewards[0]:
        winner = 1
    return {
        "seed": int(seed),
        "rewards": rewards,
        "statuses": statuses,
        "winner": winner,
        "turns_played": len(env.steps),
        "seat_actions": seat_actions,
        "action_stream_sha256": action_stream_sha256(seat_actions),
        "suspicious_log_lines": suspicious,
        "anomaly_kinds": game_anomalies(statuses, rewards, len(env.steps),
                                        suspicious),
        "wall_s": round(elapsed, 2),
    }


def load_pair(me_kind: str, opp_kind: str, me_seat: int):
    """按席位装载 (fn_seat0, fn_seat1)：文件型 agent 每席全新装载。"""
    def _resolve(kind):
        if kind in AGENT_PATHS:
            return load_agent(AGENT_PATHS[kind])
        if kind.startswith("pool:"):
            return load_pool_bot(kind.split(":", 1)[1])
        raise KeyError(f"unknown agent kind: {kind}")

    pair = [_resolve(opp_kind), _resolve(opp_kind)]
    pair[me_seat] = _resolve(me_kind)
    return pair[0], pair[1]


def run_seated_h2h(me_kind: str, opp_kind: str, seed: int, me_seat: int) -> dict:
    """单局 seated h2h：me_kind 的 agent 显式落 me_seat 席。"""
    fn0, fn1 = load_pair(me_kind, opp_kind, me_seat)
    res = run_engine_game(fn0, fn1, seed)
    res["me_seat"] = me_seat
    res["me_kind"], res["opp_kind"] = me_kind, opp_kind
    res["me_money"] = res["rewards"][me_seat]
    res["opp_money"] = res["rewards"][1 - me_seat]
    res["me_win"] = (res["rewards"][me_seat] > res["rewards"][1 - me_seat])
    res["me_tie"] = (res["rewards"][me_seat] == res["rewards"][1 - me_seat])
    return res


# ---------------------------------------------------------------------------
# 合成语料（孪生引擎，双席 agent 驱动）
# ---------------------------------------------------------------------------
def synthetic_season_head(seed: int,
                          episode_steps: int = FULL_STEPS) -> dict:
    """合成整季回放头（planner_flagoff_golden.synthetic_season_head 同构：
    NW 象限解锁、3000 起始资金、零棚零种、market 初值=引擎 MARKET_PARAMS
    的 I0/base 全品表；info.seed=seed 驱动杂草/商店随机）。"""
    from kaggle_simulations.agent.planner import twin
    module = twin.load_engine().module
    board = 10
    tiles = []
    for y in range(board):
        row = []
        for x in range(board):
            quadrant = ("N" if y < board // 2 else "S") + \
                       ("W" if x < board // 2 else "E")
            row.append(None if quadrant == "NW" else "LOCKED")
        tiles.append(row)

    def farm():
        return {"money": 3000.0,
                "tiles": json.loads(json.dumps(tiles)),
                "farmer": [board // 2 - 1, board // 2 - 1], "hands": [],
                "unlocked_quadrants": ["NW"], "hires_today": 0}

    def private():
        return {"shed": dict.fromkeys(list(module.PRODUCTS)
                                      + list(module.ANIMALS), 0),
                "seeds": dict.fromkeys(module.CROPS, 0),
                "inventories": [{}]}

    market = {
        "inventory": {item: module.MARKET_PARAMS[item]["I0"]
                      for item in module.PRODUCTS},
        "prices": {item: module.MARKET_PARAMS[item]["base"]
                   for item in module.PRODUCTS},
    }
    head = []
    for player in (0, 1):
        obs = {"farms": [farm() for _ in range(2)],
               "market": json.loads(json.dumps(market)),
               "town": {"unlocked_shops": []},
               "day": 0, "hour": 0, "step": 0 if player == 0 else None,
               "player": player, "private": private(),
               "remainingOverageTime": 60}
        head.append({"action": None, "status": "ACTIVE", "reward": 0,
                     "observation": obs})
    cfg = {"episodeSteps": episode_steps, "actTimeout": 1, "boardSize": board,
           "startingMoney": 3000, "maxMarketOrdersPerTurn": 10,
           "turnsPerDay": 24, "shedCapacity": 100, "weedSpawnChance": 0.005,
           "townShopUnlockInterval": 3, "townShopSellInterval": 4,
           "townCenterSellInterval": 24, "seed": None, "farmHandCostMult": 1,
           "marketParams": {}}
    return {"steps": [head], "configuration": cfg, "info": {"seed": seed}}


def _jsonify(action):
    return json.loads(json.dumps(action))


class ObsStruct(dict):
    """dict+属性双视图（kaggle_environments.utils.Struct 读取语义最小
    复刻）——v48 系策略链内有直接 obs.get(...) 调用，孪生 Observation
    仅属性视图；官方引擎喂给 agent 的 obs 即 dict+attr 形态，故在 agent
    边界把孪生观测包成本视图（浅包装，嵌套 farms/market/town/private
    为纯 dict，两种访问语义皆可）。"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e


def structify_obs(obs) -> ObsStruct:
    """孪生 Observation -> 官方 dict+attr 形态（顶层浅包装）。

    step 回填：官方框架运行期对**双席**都注入 step（实测探针：两席
    Struct 均含 step；回放 JSON 只是记录层省略 seat1 的 step）。孪生
    Observation 只给 seat0 维护 step；解释器恒保持 day*24+hour==step
    （每次转移末 obs0.day/hour 按 next_step 折算），故 seat1 缺失时按
    day*24+hour 回填——与线上喂给 agent 的形态逐位一致。"""
    keys = ("farms", "market", "town", "day", "hour", "step", "player",
            "private", "remainingOverageTime")
    out = ObsStruct()
    for k in keys:
        v = getattr(obs, k, None)
        if v is not None or hasattr(obs, k):
            out[k] = v
    for k in getattr(obs, "__slots__", ()):     # 未来字段兜底
        if k not in out and hasattr(obs, k):
            out[k] = getattr(obs, k)
    if out.get("step") is None and out.get("day") is not None:
        out["step"] = int(out["day"]) * 24 + int(out.get("hour") or 0)
    return out


def adapt_agent_for_twin(agent_fn):
    """把 agent callable 适配到孪生通道：obs 包成 dict+attr 视图。"""
    def wrapped(obs):
        return agent_fn(structify_obs(obs))
    wrapped.__name__ = getattr(agent_fn, "__name__", "agent")
    return wrapped


def twin_selfplay(agent_loaders, seed: int, on_step=None) -> dict:
    """孪生整季自打：agent_loaders=[seat0装载器, seat1装载器]（零参可调用，
    返回该席 agent callable）。逐 transition 记录框架形态 steps（head +
    每步双席动作），返回 {replay, finals, streams, transitions, wall_s}。
    on_step(seat, obs, action) 在引擎推进前逐席回调（P2/P3 触发遥测用，
    obs 为当时的真实观测对象）。"""
    from kaggle_simulations.agent.planner import twin
    t0 = time.perf_counter()
    replay = synthetic_season_head(seed)
    state = twin.new_state_from_replay_head(replay)
    agents = [adapt_agent_for_twin(loader()) for loader in agent_loaders]
    streams = [[], []]
    taken = 0
    while not state.env.done and taken < FULL_STEPS:
        pair = []
        for seat in (0, 1):
            obs = state.seats[seat].observation
            action = _jsonify(agents[seat](obs))
            if on_step is not None:
                on_step(seat, obs, action)
            streams[seat].append(action)
            pair.append(action)
        twin.step(state, pair)
        replay["steps"].append([{"action": pair[0]}, {"action": pair[1]}])
        taken += 1
    finals = twin.final_money(state)
    replay["rewards"] = finals
    return {"replay": replay, "finals": finals, "streams": streams,
            "transitions": taken,
            "action_stream_sha256": action_stream_sha256(streams),
            "wall_s": round(time.perf_counter() - t0, 2)}


def load_rollout_channel():
    """装载 fn_work 的 seated 回放注入通道（显式 me_seat 语义）。"""
    import rollout_with_replay_opponent as rro
    return rro


def jsonify_report(obj):
    """报告瘦身：动作流等大对象不落盘。"""
    return obj


def write_json(path: str, payload) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as h:
        json.dump(payload, h, ensure_ascii=False, indent=1)
    return path
