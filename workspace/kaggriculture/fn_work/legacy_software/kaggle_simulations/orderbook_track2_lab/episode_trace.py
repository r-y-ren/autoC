# -*- coding: utf-8 -*-
"""episode_trace：官方引擎完整局追踪跑口（v48 run_full_episode 同款 + 动作流落盘）。

用途：四门门②③（双席 DONE+单步<1s / 确定性双跑逐字节）+ 内生版差异拍
足迹审计的动作流来源。每席记录 (step, action) 逐拍流（不改动作）；
装载=官方 last-callable 语义（judge_r23._load_entry 同款，全新命名空间），
同时保留命名空间以读取卫生台账（outer=_X1_REPORT / inner=_S1009_REPORT.hyg）。
只写 orderbook_track2_lab/。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

FULL_STEPS = 720
STEP_BUDGET_MS = 1000.0


def load_entry_env(path):
    """官方 last-callable 语义装载；返回 (entry, ns)（ns 供读卫生台账）。"""
    p = os.path.abspath(str(path))
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.pop()
        sys.dont_write_bytecode = old
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError("%s 装载后无 callable" % p)
    return entries[-1], ns


def _action_key(action):
    """动作的紧凑可比键（足迹审计用）。"""
    try:
        return json.dumps(action, sort_keys=True, default=repr)
    except Exception:
        return repr(action)


def stream_hashes(seat_streams):
    out = []
    for stream in seat_streams:
        h = hashlib.sha256()
        for step, action in stream:
            h.update(("%d|" % step).encode("utf-8"))
            h.update(_action_key(action).encode("utf-8"))
            h.update(b"\n")
        out.append(h.hexdigest())
    return out


def run_episode(main_path, seed, dump_path=None):
    """单局：双席自打（同一件装载两份命名空间），官方引擎 720 回合。"""
    from kaggle_environments import make

    entries = []
    envs = []
    for _ in range(2):
        entry, ns = load_entry_env(main_path)
        entries.append(entry)
        envs.append(ns)
    timings = ([], [])
    streams = ([], [])
    agents = []
    for seat in (0, 1):
        fn = entries[seat]

        def make_call(fn=fn, seat=seat):
            def call(obs, configuration=None):
                t0 = time.perf_counter()
                action = None
                try:
                    action = fn(obs, configuration)
                    return action
                finally:
                    timings[seat].append((time.perf_counter() - t0) * 1000.0)
                    try:
                        step = int((obs or {}).get("step", 0)) \
                            if isinstance(obs, dict) else -1
                    except Exception:
                        step = -1
                    streams[seat].append((step, action))
            return call
        agents.append(make_call())

    t0 = time.perf_counter()
    env = make("kaggriculture",
               configuration={"episodeSteps": FULL_STEPS, "seed": int(seed),
                              "actTimeout": 60.0},
               debug=True)
    env.run([agents[0], agents[1]])
    wall = time.perf_counter() - t0

    final = env.steps[-1]
    rewards = [float(s["reward"]) for s in final]
    statuses = [s["status"] for s in final]
    turns_played = len(env.steps)

    raw_logs = [str(line) for line in getattr(env, "logs", []) if line]
    suspicious = [s[:300] for s in raw_logs
                  if "ERROR" in s or "Timed out" in s or "Traceback" in s]

    all_t = sorted(timings[0] + timings[1])
    n_calls = len(all_t)

    def pct(p):
        return all_t[min(n_calls - 1, int(n_calls * p))] if n_calls else 0.0

    hashes = stream_hashes(streams)
    hyg = []
    for ns in envs:
        rep = ns.get("_X1_REPORT")
        if isinstance(rep, dict):
            hyg.append({"source": "_X1_REPORT",
                        **{k: v for k, v in rep.items()}})
            continue
        s1009 = ns.get("_S1009_REPORT")
        if isinstance(s1009, dict) and isinstance(s1009.get("hyg"), dict):
            hyg.append({"source": "_S1009_REPORT.hyg",
                        **{k: v for k, v in s1009["hyg"].items()}})
    out = {
        "seed": seed,
        "statuses": statuses,
        "rewards": rewards,
        "turns_played": turns_played,
        "agent_action_steps": turns_played - 1,
        "n_engine_log_lines": len(raw_logs),
        "suspicious_log_lines": suspicious,
        "wall_s": round(wall, 1),
        "agent_calls": n_calls,
        "max_step_ms": round(all_t[-1], 2) if all_t else None,
        "p99_step_ms": round(pct(0.99), 2),
        "mean_step_ms": round(sum(all_t) / n_calls, 2) if n_calls else None,
        "action_stream_sha256": hashlib.sha256(
            (hashes[0] + hashes[1]).encode("utf-8")).hexdigest(),
        "seat_stream_sha256": hashes,
        "hygiene_reports": hyg,
        "n_stream_rows": [len(s) for s in streams],
    }
    if dump_path:
        os.makedirs(os.path.dirname(dump_path), exist_ok=True)
        payload = {
            "seed": seed,
            "form_dump": os.path.basename(os.path.dirname(main_path)),
            "seats": [[[step, _action_key(action)] for step, action in s]
                      for s in streams],
        }
        with open(dump_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, default=repr)
    return out
