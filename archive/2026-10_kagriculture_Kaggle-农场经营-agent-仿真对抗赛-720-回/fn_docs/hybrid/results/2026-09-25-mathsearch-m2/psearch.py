# -*- coding: utf-8 -*-
"""M2 参数空间搜索 harness（研究轮，只写 /tmp/mathsearch/）。

对 P4 家族（patches/lead_protection.py R8-v2）参数化，在 14 局领先崩塌语料
（v48_hybrid/fn_docs/results/replays-lead-collapse/）上做双臂对照重演：
P4 臂（参数化 P4 包 v4b）vs 复用的无 P4 基线臂（v4b），Δ=margin(P4)−margin(基线)。
注入点=CORPUS.md 峰值日 d*24；对手=回放真值流（seated 通道 rro 同语义）。

参数面：
  触发轴：A 臂（回撤臂）D_A∈{15,18,21,24} L_A∈{1500,3000,5000} DD∈{1000,2000,3000}
          B 臂（终局领先臂）D_B∈{15,18,21,24} L_B∈{1500,3000,5000}
          组合 arms∈{dd_only, late_only, union}
  排程轴：line_sel∈{falling, all, high}；cap∈{2,4,8,13}（单帧发射帽，跨时点复发拆批；
          13=单产品线城镇日吸收下界）；hours∈{(6,),(12,),(18,),(6,12,18),absorb=(0,4,8,12,16,20)}；
          skip_tape∈{True,False}（是否跳过当帧已在卖的线）
只读消费仓库文件；不改 ladder/任何仓库文件。
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time

V48 = ("/mnt/data/Code/autoC/workspace/kaggriculture/software/"
       "kaggle_simulations/v48_hybrid")
GATES = os.path.join(V48, "gates")
CORPUS = os.path.join(V48, "fn_docs", "results", "replays-lead-collapse")
V4B_MAIN = os.path.join(V48, "v4b", "main.py")

for _p in (GATES,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_common as gc  # noqa: E402
import rollout_with_replay_opponent as rro  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "lp_base_mod", os.path.join(V48, "patches", "lead_protection.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

TERMINAL = 717
MAX_ORDERS = 10
MAX_LINES = 4

_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|[^|]+\|\s*([01])\s*\|\s*(-?[\d.]+)\s*\|[^|]+\|[^|]+"
    r"\|\s*d(\d+)\s*\|\s*(-?[\d.]+)\s*\|")


def parse_corpus():
    games = []
    with open(os.path.join(CORPUS, "CORPUS.md"), encoding="utf-8") as h:
        for line in h:
            m = _ROW_RE.match(line)
            if m:
                games.append({"ep": int(m.group(1)), "me_seat": int(m.group(2)),
                              "orig_margin": float(m.group(3)),
                              "peak_day": int(m.group(4)),
                              "peak_amount": float(m.group(5)),
                              "inject": int(m.group(4)) * 24})
    return games


GAMES = parse_corpus()
_REPLAYS = {}


def get_replay(ep):
    if ep not in _REPLAYS:
        with open(os.path.join(CORPUS, f"episode-{ep}-replay.json"),
                  encoding="utf-8") as h:
            _REPLAYS[ep] = json.load(h)
    return _REPLAYS[ep]


# ---------------------------------------------------------------------------
# 参数化 P4（编排面与 v5 缝一致：P2 否决后的 market 面追加补发）
# ---------------------------------------------------------------------------
DEFAULT_CFG = {
    "arms": "union",          # union | dd_only | late_only
    "D_A": 15, "L_A": 1500.0, "DD": 2000.0,    # A 臂（回撤臂）
    "D_B": 24, "L_B": 3000.0,                   # B 臂（终局领先臂）
    "line_sel": "all",        # falling | all | high
    "cap": 4,                 # 单线单帧发射帽（13=日吸收下界）
    "hours": (6, 12, 18),     # 保护时点
    "skip_tape": True,        # 跳过当帧已在卖线
}

HOURS_ABSORB = (0, 4, 8, 12, 16, 20)


def _shed_view(obs):
    private = lp._get(obs, "private", {}) or {}
    shed = lp._get(obs, "shed", None)
    if not isinstance(shed, dict):
        shed = lp._get(private, "shed", None)
    return shed if isinstance(shed, dict) else None


def param_build(obs, day, current, cfg, register, meter):
    """v2 build 的参数化镜像（语义面逐条对齐 patches/lead_protection.py）。"""
    step = lp._get(obs, "step", None)
    if not isinstance(step, (int, float)) or isinstance(step, bool):
        return current
    step_i = int(step)
    if step_i >= TERMINAL:
        return current
    day_i = int(day)
    est = lp.estimate_lead_margin(obs, day_i)
    lead = est.get("lead") if isinstance(est, dict) else None
    lead_f = float(lead) if lead is not None else None

    peak = lp._num(register.get("peak_lead", None))
    if lead_f is not None:
        peak = lead_f if peak is None or lead_f > peak else peak
        register["peak_lead"] = peak
    drawdown = (peak - lead_f) if (peak is not None and lead_f is not None) \
        else None

    arm_a = (day_i >= int(cfg["D_A"]) and lead_f is not None
             and lead_f >= float(cfg["L_A"]) and drawdown is not None
             and drawdown >= float(cfg["DD"]))
    arm_b = (day_i >= int(cfg["D_B"]) and lead_f is not None
             and lead_f >= float(cfg["L_B"]))
    mode = cfg["arms"]
    armed = {"dd_only": arm_a, "late_only": arm_b,
             "union": arm_a or arm_b, "none": False}[mode]
    if not armed:
        return current
    meter["armed_frames"] += 1
    if meter["first_armed_step"] is None:
        meter["first_armed_step"] = step_i

    hour = step_i % 24
    hours = tuple(cfg["hours"])
    if hour not in hours:
        return current
    shed = _shed_view(obs)
    if not shed:
        return current
    projection = lp._build_price_projection(obs, lp.DEFAULT_CONFIG)
    selling_now = {o[1] for o in (current or [])
                   if isinstance(o, (list, tuple)) and len(o) >= 3
                   and o[0] == "SELL"}
    cands = []
    for item, qty in shed.items():
        if cfg["skip_tape"] and item in selling_now:
            continue
        if item not in lp.BASE_PRICE:
            continue
        q = lp._num(qty)
        if not q or q <= 0:
            continue
        pair = projection.get(item)
        falling = False
        price = None
        if isinstance(pair, (list, tuple)) and len(pair) >= 2:
            p_now, p_fut = lp._num(pair[0]), lp._num(pair[1])
            if p_now is not None and p_fut is not None:
                falling = p_fut < p_now
                price = p_now
        if price is None:
            price = float(lp.BASE_PRICE[item])
        sel = cfg["line_sel"]
        if sel == "falling" and not falling:
            continue
        if sel == "all" and (not falling) and hour != max(hours):
            continue
        cands.append((item, int(q), float(price)))
    if not cands:
        return current
    if cfg["line_sel"] == "high":
        cands.sort(key=lambda t: (-t[2], -t[1], t[0]))
    else:
        cands.sort(key=lambda t: (-t[1], t[0]))
    room = max(0, min(MAX_LINES, MAX_ORDERS - len(current or [])))
    emits = [["SELL", it, int(min(q, int(cfg["cap"])))]
             for it, q, _p in cands[:room]]
    if not emits:
        return current
    meter["emit_frames"] += 1
    meter["emit_units"] += sum(e[2] for e in emits)
    return list(current or []) + emits


def make_param_agent(cfg):
    """fresh v4b 装载 + 参数化 P4 缝（P2 streak 每局隔离=每 run 重装载）。"""
    base = gc.load_agent(V4B_MAIN)
    register = {"peak_lead": None}
    meter = {"armed_frames": 0, "emit_frames": 0, "emit_units": 0,
             "first_armed_step": None}

    def agent(obs):
        out = base(obs)
        try:
            if isinstance(out, dict):
                step = lp._get(obs, "step", None)
                day = (int(step) // 24) if isinstance(
                    step, (int, float)) and not isinstance(step, bool) \
                    else None
                if day is not None:
                    mkt = out.get("market")
                    if isinstance(mkt, list):
                        out["market"] = param_build(obs, day, mkt, cfg,
                                                    register, meter)
        except Exception:
            pass
        return out

    agent.__name__ = "param_p4_agent"
    return agent, meter


def make_baseline_agent():
    base = gc.load_agent(V4B_MAIN)

    def agent(obs):
        return base(obs)

    agent.__name__ = "baseline_v4b"
    return agent


# ---------------------------------------------------------------------------
# seated 重演（gates._replay_stream_run 同构）
# ---------------------------------------------------------------------------
def run_arm(ep, inject, me_seat, structured_fn):
    replay = get_replay(ep)
    deps = rro.make_twin_deps()
    state = deps["build"](replay, int(inject))
    opp = deps["transition_actions"](replay)
    me = int(me_seat)
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while (not state.env.done and int(inject) + taken < len(opp)
           and taken < max_steps):
        obs = state.seats[me].observation
        mine = structured_fn(gc.structify_obs(obs))
        pair = [opp[int(inject) + taken][1 - me]] * 2
        pair[me] = mine
        deps["step"](state, pair)
        taken += 1
    finals = deps["final"](state)
    return finals, taken


def cfg_public(cfg):
    out = dict(cfg)
    out["hours"] = list(cfg["hours"])
    return out


def eval_config(cfg):
    """单配置：14 局 P4 臂重演 → 每局 margin + 遥测。"""
    res = {"cfg": cfg_public(cfg), "games": []}
    for g in GAMES:
        agent, meter = make_param_agent(cfg)
        finals, taken = run_arm(g["ep"], g["inject"], g["me_seat"], agent)
        margin = float(finals[g["me_seat"]]) - float(finals[1 - g["me_seat"]])
        res["games"].append({"ep": g["ep"], "margin": round(margin, 2),
                             "taken": taken,
                             "armed_frames": meter["armed_frames"],
                             "emit_frames": meter["emit_frames"],
                             "emit_units": meter["emit_units"],
                             "first_armed_step": meter["first_armed_step"]})
    return res


def eval_baseline():
    res = {"games": []}
    for g in GAMES:
        agent = make_baseline_agent()
        finals, taken = run_arm(g["ep"], g["inject"], g["me_seat"], agent)
        margin = float(finals[g["me_seat"]]) - float(finals[1 - g["me_seat"]])
        res["games"].append({"ep": g["ep"], "margin": round(margin, 2),
                             "taken": taken})
    return res


if __name__ == "__main__":
    t0 = time.perf_counter()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if mode == "baseline":
        out = eval_baseline()
        out["wall_s"] = round(time.perf_counter() - t0, 1)
        with open("/tmp/mathsearch/baseline.json", "w") as h:
            json.dump(out, h, ensure_ascii=False, indent=1)
        print(json.dumps(out, ensure_ascii=False))
    elif mode == "validate":
        # v2 默认参数复现：应与 gates/out/lead_protection_v2_replay_gate.json
        # 的 p4_margin 逐局一致（参数化面正确性验证）
        out = eval_config(DEFAULT_CFG)
        out["wall_s"] = round(time.perf_counter() - t0, 1)
        with open("/tmp/mathsearch/validate.json", "w") as h:
            json.dump(out, h, ensure_ascii=False, indent=1)
        print(json.dumps({"margins": [g["margin"] for g in out["games"]],
                          "wall_s": out["wall_s"]}))
    elif mode == "smoke":
        g = GAMES[0]
        agent, meter = make_param_agent(DEFAULT_CFG)
        finals, taken = run_arm(g["ep"], g["inject"], g["me_seat"], agent)
        margin = float(finals[g["me_seat"]]) - float(finals[1 - g["me_seat"]])
        print(json.dumps({"ep": g["ep"], "margin": margin, "taken": taken,
                          "meter": meter,
                          "wall_s": round(time.perf_counter() - t0, 2)}))
