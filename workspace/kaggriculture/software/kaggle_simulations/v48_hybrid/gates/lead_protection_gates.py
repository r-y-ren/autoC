# -*- coding: utf-8 -*-
"""R8 验收编排：重演门（14 局领先崩塌局，>=7/14）+ 等价面（>=8 局逐字节）+ 发射复检。
上游: R8 验收方式（fn_docs/requirements.md）；fail-closed。

F4c 实装（占位→真实，2026-09-22）。口径登记：

* 重演门 run_replay_gate(corpus_dir, v5_callable)
  - 语料 = 归档目录（fn_docs/results/replays-lead-collapse/，14 件最小投影
    + CORPUS.md 清单）；清单行/回放件缺失即 ValueError（fail-closed）。
  - 注入点口径 = 领先峰值日 d 的起始步 d*24（"从该日 step 起接管"：该日
    hour0 起我席由 v5 决策，此前按回放真值重演；峰值日资本口径 =
    loss-timelines 端日 hour23 资金差，即 CORPUS.md"峰值日"列）。
  - 对手侧 = 回放真值动作流（seated 通道 fn_work
    rollout_with_replay_opponent 同语义：theirs 注入对席）。
  - 成功 = 重演终局 margin>0；判据 wins>=7/14（REPLAY_WIN_MIN）。
  - 我席来源 = CORPUS.md"我席"列，与回放 info.TeamNames(renyxin) 交叉，
    不一致即 ValueError；orig_margin 以回放 rewards 实测为准并与清单行
    交叉。逐局附 P4 触发形态遥测（patches/lead_protection 同口径镜像：
    day>=24 且 est.lead>=3000 才算形态在场）。

* 等价面 run_equivalence_face(game_set, v5_callable, v4b_callable)
  - 非触发局 = 全程无 d24+ 领先>=3000 形态（v5 侧遥测 form==0）。
  - 构造局（kind=constructed）：合成季头（gate_common.synthetic_season_head
    同构）双席驱动；默认 4 局 = v5 对席 v4b 镜像自打（对称局资金差恒 0，
    天然无 d24+ 领先形态），候补种子池在触发形态误入时顺延。
  - 真实回放采样（kind=replay）：默认自 /tmp/r26full 取"无领先崩塌形态"
    局（loss-timelines 中 max_lead_day_amount<1000 或 None、且不属于语料
    14 局），全季注入（inject 0）对回放真值对手，v5 与 v4b 动作流比对。
  - 判据：可用局 >=8 且 n_identical==n（任一分叉即 fail）。

* 发射复检 run_launch_recheck(v5_package)
  - v5 冒烟四门真复跑（importlib 装载 software/scripts/
    v48_derivative_launch_check.py 后仅重定向路径，与 tmp/fourgate_v5.py
    同法，不做回填）：装载/自打/确定性/体积。
  - patches 单测真复跑（子进程 pytest patches -q）。
  - 与 F4b 既有冒烟产物（tmp/probes_v5/v5_smoke.json）身份一致性交叉。

* 裁决 verify_lead_protection(v5_package, corpus_dir)
  - 三门汇总 {overall, replay_gate, equivalence, launch}；任一门不可执行
    = 整体 FAIL（fail-closed 不抛，错误入 dict）。
  - 产物：gates/out/lead_protection_verdict.json（+ 三门分项 json）。

产物纪律：除本文件与其测试外不改任何现存文件；临时件落 v48_hybrid/tmp/；
gates/out/ 仅本编排产物。CLI：python gates/lead_protection_gates.py。
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

HYB = gc.HYB
CORPUS_DEFAULT = os.path.join(HYB, "fn_docs", "results",
                              "replays-lead-collapse")
V5_DIR_DEFAULT = os.path.join(HYB, "v5")
V4B_DIR_DEFAULT = os.path.join(HYB, "v4b")
V5_MAIN = os.path.join(V5_DIR_DEFAULT, "main.py")
V4B_MAIN = os.path.join(V4B_DIR_DEFAULT, "main.py")
TIMELINES_PATH = os.path.join(HYB, "fn_docs", "results",
                              "2026-09-24-loss-timelines.json")
R26FULL_DIR = "/tmp/r26full"
RECORDED_SMOKE = os.path.join(HYB, "tmp", "probes_v5", "v5_smoke.json")
TEAM_NAME = "renyxin"
STEPS_PER_DAY = 24
REPLAY_WIN_MIN = 7
REPLAY_N_EXPECTED = 14
EQUIV_MIN = 8
EQUIV_CONSTRUCTED_MIN = 4
EQUIV_REPLAY_MIN = 4
VERDICT_PATH = os.path.join(_HERE, "out", "lead_protection_verdict.json")

_LP_PATCH = None


# ---------------------------------------------------------------------------
# P4 触发形态遥测（patches/lead_protection.py 只读镜像，不改它）
# ---------------------------------------------------------------------------
def _load_lp_patch():
    global _LP_PATCH
    if _LP_PATCH is None:
        path = os.path.join(HYB, "patches", "lead_protection.py")
        spec = importlib.util.spec_from_file_location("r8_lp_patch_ro", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _LP_PATCH = mod
    return _LP_PATCH


def _new_meter() -> dict:
    return {"steps_seen": 0, "day_ge_24_calls": 0, "form_present_calls": 0,
            "max_lead": None, "first_form_step": None,
            "lead_at_first_form": None}


def _instrument(raw_fn, meter: dict):
    """包装决策 callable（吃 dict+attr 结构化 obs）：逐步镜像 P4 触发形态。"""
    patch = _load_lp_patch()
    cfg = patch.DEFAULT_CONFIG
    day_min = int(cfg["trigger_day_min"])
    lead_min = float(cfg["trigger_lead_min"])
    spd = int(cfg["steps_per_day"])

    def wrapped(obs):
        meter["steps_seen"] += 1
        try:
            step = obs.get("step", None)
        except AttributeError:
            step = None
        day = None
        if isinstance(step, (int, float)) and not isinstance(step, bool):
            day = int(step) // spd
        if day is not None and day >= day_min:
            meter["day_ge_24_calls"] += 1
            est = patch.estimate_lead_margin(obs, day)
            lead = est.get("lead") if isinstance(est, dict) else None
            if lead is not None:
                if meter["max_lead"] is None or lead > meter["max_lead"]:
                    meter["max_lead"] = float(lead)
                if float(lead) >= lead_min:
                    meter["form_present_calls"] += 1
                    if meter["first_form_step"] is None:
                        meter["first_form_step"] = int(step)
                        meter["lead_at_first_form"] = float(lead)
        return raw_fn(obs)

    wrapped.__name__ = getattr(raw_fn, "__name__", "agent")
    return wrapped


def _meter_public(meter: dict) -> dict:
    return dict(meter)


def _stream_sha(actions) -> str:
    payload = "\n".join(gc.norm_action(a) for a in actions)
    return gc.sha256_bytes(payload.encode("utf-8"))


# ---------------------------------------------------------------------------
# CORPUS.md 清单解析 + 我席交叉
# ---------------------------------------------------------------------------
_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|[^|]+\|\s*([01])\s*\|\s*(-?[\d.]+)\s*\|[^|]+\|[^|]+"
    r"\|\s*d(\d+)\s*\|\s*(-?[\d.]+)\s*\|")


def _parse_corpus_md(corpus_dir):
    path = os.path.join(corpus_dir, "CORPUS.md")
    if not os.path.isfile(path):
        raise ValueError(f"语料缺失: {path}")
    games = []
    with open(path, encoding="utf-8") as h:
        for line in h:
            m = _ROW_RE.match(line)
            if m:
                games.append({"ep": int(m.group(1)),
                              "me_seat": int(m.group(2)),
                              "orig_margin": float(m.group(3)),
                              "peak_day": int(m.group(4)),
                              "peak_amount": float(m.group(5))})
    if not games:
        raise ValueError(f"CORPUS.md 清单行为空: {path}")
    return games


def _me_seat_from_info(replay):
    info = replay.get("info") or {}
    names = info.get("TeamNames") or []
    for i, n in enumerate(names):
        if n == TEAM_NAME:
            return i
    for i, a in enumerate(info.get("Agents") or []):
        if (a or {}).get("Name") == TEAM_NAME:
            return i
    return None


def _load_replay(path):
    if not os.path.isfile(path):
        raise ValueError(f"语料回放件缺失: {path}")
    with open(path, encoding="utf-8") as h:
        replay = json.load(h)
    if not (replay.get("steps") or []):
        raise ValueError(f"回放无 steps: {path}")
    return replay


# ---------------------------------------------------------------------------
# seated 重演（记录我席动作流；rollout_with_replay_opponent 同语义）
# ---------------------------------------------------------------------------
def _replay_stream_run(replay, inject_step, structured_fn, me_seat):
    import rollout_with_replay_opponent as rro   # gate_common 已置路径
    deps = rro.make_twin_deps()
    start = int(inject_step)
    state = deps["build"](replay, start)
    opp_actions = deps["transition_actions"](replay)
    me = int(me_seat)
    stream = []
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while (not state.env.done and start + taken < len(opp_actions)
           and taken < max_steps):
        obs = state.seats[me].observation
        mine = structured_fn(gc.structify_obs(obs))
        pair = [opp_actions[start + taken][1 - me]] * 2
        pair[me] = mine
        deps["step"](state, pair)
        stream.append(mine)
        taken += 1
    return {"finals": deps["final"](state), "stream": stream,
            "steps": taken, "stream_sha256": _stream_sha(stream)}


def _fresh_v5():
    return gc.load_agent(V5_MAIN)


def _fresh_v4b():
    return gc.load_agent(V4B_MAIN)


# ---------------------------------------------------------------------------
# 门一：14 局重演
# ---------------------------------------------------------------------------
def run_replay_gate(corpus_dir, v5_callable=None):
    """14 局重演门：seated 通道，注入点=领先峰值日（口径登记义务）；成功=重演终局 margin>0。

    输入: 归档语料目录（fn_docs/results/replays-lead-collapse/）+ v5 callable / 输出: {wins,n,per_game} / 错误: 语料缺失 fail-closed。
    """
    t0 = time.perf_counter()
    corpus_dir = corpus_dir or CORPUS_DEFAULT
    table = _parse_corpus_md(corpus_dir)
    per_game = []
    wins = 0
    for row in table:
        path = os.path.join(corpus_dir, f"episode-{row['ep']}-replay.json")
        replay = _load_replay(path)
        rewards = replay.get("rewards")
        if not (isinstance(rewards, list) and len(rewards) == 2):
            raise ValueError(f"ep{row['ep']} rewards 缺失: {path}")
        me = int(row["me_seat"])
        seat_info = _me_seat_from_info(replay)
        if seat_info is not None and seat_info != me:
            raise ValueError(f"ep{row['ep']} 我席不一致: CORPUS.md={me} "
                             f"info={seat_info}")
        orig = float(rewards[me]) - float(rewards[1 - me])
        if abs(orig - float(row["orig_margin"])) > 1e-6:
            raise ValueError(f"ep{row['ep']} orig_margin 不一致: "
                             f"rewards={orig} CORPUS.md={row['orig_margin']}")
        agent = v5_callable if v5_callable is not None else _fresh_v5()
        meter = _new_meter()
        inject_step = int(row["peak_day"]) * STEPS_PER_DAY
        run = _replay_stream_run(
            replay, inject_step, _instrument(agent, meter), me)
        replay_margin = float(run["finals"][me]) - float(run["finals"][1 - me])
        win = replay_margin > 0.0
        wins += int(win)
        per_game.append({
            "ep": row["ep"], "me_seat": me, "opp": _opp_name(replay, 1 - me),
            "peak_day": row["peak_day"], "peak_amount": row["peak_amount"],
            "injection_step": inject_step,
            "orig_margin": round(orig, 2),
            "replay_margin": round(replay_margin, 2),
            "replay_finals": [round(float(x), 2) for x in run["finals"]],
            "win": win,
            "flipped": bool(orig <= 0.0 and replay_margin > 0.0),
            "steps_taken": run["steps"],
            "my_stream_sha256": run["stream_sha256"],
            "p4_trigger_meter": _meter_public(meter),
        })
    n = len(table)
    return {
        "protocol": "lead-protection-replay-gate/1.0",
        "injection_convention": ("领先峰值日 d 起始步 d*24（该日 hour0 起 "
                                 "v5 接管我席，此前按回放真值；对手侧恒为"
                                 "回放真值动作流）"),
        "criterion": f"wins >= {REPLAY_WIN_MIN}/{REPLAY_N_EXPECTED}",
        "wins": wins, "n": n,
        "passed": bool(wins >= REPLAY_WIN_MIN and n == REPLAY_N_EXPECTED),
        "per_game": per_game,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


def _opp_name(replay, opp_seat):
    info = replay.get("info") or {}
    names = info.get("TeamNames") or [a.get("Name") for a in
                                      (info.get("Agents") or [])]
    return names[opp_seat] if opp_seat < len(names) else None


# ---------------------------------------------------------------------------
# 门二：非触发局等价面
# ---------------------------------------------------------------------------
def _resolve_opp(opp_kind):
    """对手解析：None=v4b 镜像；'pool:NAME'=线上画像池；.py 路径=装载；callable=直用。"""
    if opp_kind is None:
        return lambda: _fresh_v4b()
    if isinstance(opp_kind, str) and opp_kind.startswith("pool:"):
        name = opp_kind.split(":", 1)[1]
        return lambda: gc.load_pool_bot(name)
    if isinstance(opp_kind, str) and opp_kind.endswith(".py"):
        return lambda: gc.load_agent(opp_kind)
    if callable(opp_kind):
        return lambda: opp_kind
    raise ValueError(f"未知对手规格: {opp_kind!r}")


def _default_replay_candidates(limit=8):
    if not os.path.isdir(R26FULL_DIR):
        raise ValueError(f"真实回放采样源缺失: {R26FULL_DIR}")
    if not os.path.isfile(TIMELINES_PATH):
        raise ValueError(f"loss-timelines 缺失: {TIMELINES_PATH}")
    with open(TIMELINES_PATH, encoding="utf-8") as h:
        timelines = json.load(h)
    losses = ((timelines.get("corpus") or {}).get("derivative")
              or {}).get("losses") or []
    corpus_eps = {g["ep"] for g in _parse_corpus_md(CORPUS_DEFAULT)}
    out = []
    for e in sorted(losses, key=lambda x: x.get("ep", 0)):
        m = e.get("max_lead_day_amount") or {}
        amt = m.get("amount")
        if e.get("ep") in corpus_eps:
            continue                      # 语料 14 局（领先崩塌形态）排除
        if amt is not None and float(amt) >= 1000.0:
            continue                      # 有实质领先形态，排除
        path = os.path.join(R26FULL_DIR,
                            f"episode-{e.get('ep')}-replay.json")
        if not os.path.isfile(path):
            continue
        out.append({"kind": "replay", "ep": e["ep"],
                    "me_seat": int(e["seat"]), "replay_path": path,
                    "inject_step": 0, "tape_max_lead": amt})
        if len(out) >= limit:
            break
    return out


def _default_game_set():
    """默认局集：构造 4（+候补）镜像自打 + 真实回放采样 4（+候补）。"""
    seeds = (4101, 4202, 4303, 4404, 4505, 4606, 4707, 4808)
    constructed = [{"kind": "constructed", "seed": s, "episode_steps": 720,
                    "opp_kind": None, "me_seat": i % 2}
                   for i, s in enumerate(seeds)]
    return constructed + _default_replay_candidates(limit=8)


def _run_constructed_game(entry, v5_fn, v4b_fn):
    seed = int(entry["seed"])
    steps = int(entry.get("episode_steps", 720))
    me_seat = int(entry.get("me_seat", 0))
    opp_loader = _resolve_opp(entry.get("opp_kind"))
    results = {}
    for tag, fn in (("v5", v5_fn), ("v4b", v4b_fn)):
        meter = _new_meter()

        def loader(fn=fn, meter=meter):
            return _instrument(fn, meter)

        loaders = [opp_loader, opp_loader]
        loaders[me_seat] = loader
        if steps >= gc.FULL_STEPS:
            res = gc.twin_selfplay(loaders, seed)
        else:                       # 短季（测试小样）兜底
            res = _twin_selfplay_steps(loaders, seed, steps)
        results[tag] = {"res": res, "meter": meter}
    return results


def _twin_selfplay_steps(loaders, seed, steps):
    """短季孪生自打（gate_common.twin_selfplay 同构，episodeSteps 可短）。"""
    head = gc.synthetic_season_head(seed, steps)
    from kaggle_simulations.agent.planner import twin
    state = twin.new_state_from_replay_head(head)
    agents = [gc.adapt_agent_for_twin(loader()) for loader in loaders]
    streams = [[], []]
    taken = 0
    while not state.env.done and taken < steps:
        pair = []
        for seat in (0, 1):
            action = agents[seat](state.seats[seat].observation)
            action = json.loads(json.dumps(action))
            streams[seat].append(action)
            pair.append(action)
        twin.step(state, pair)
        taken += 1
    finals = twin.final_money(state)
    return {"finals": finals, "streams": streams,
            "action_stream_sha256": gc.action_stream_sha256(streams),
            "transitions": taken}


def _run_replay_game(entry, v5_fn, v4b_fn):
    replay = _load_replay(entry["replay_path"])
    me = int(entry["me_seat"])
    inject = int(entry.get("inject_step", 0))
    results = {}
    for tag, fn in (("v5", v5_fn), ("v4b", v4b_fn)):
        meter = _new_meter()
        run = _replay_stream_run(replay, inject, _instrument(fn, meter), me)
        results[tag] = {"run": run, "meter": meter}
    return replay, results


def run_equivalence_face(game_set, v5_callable=None, v4b_callable=None):
    """非触发局等价面：构造>=4+真实回放>=4，v5 与 v4b 动作流逐字节一致。

    输入: 局集+两 callable / 输出: {n_identical,n} / 错误: 任一分叉即 fail。
    """
    t0 = time.perf_counter()
    auto = game_set is None
    entries = _default_game_set() if auto else list(game_set)
    per_game = []
    n_constructed = n_replay = 0          # 可用局（非触发）计数
    for entry in entries:
        kind = entry.get("kind")
        if auto and kind == "constructed" and n_constructed >= \
                EQUIV_CONSTRUCTED_MIN:
            continue
        if auto and kind == "replay" and n_replay >= EQUIV_REPLAY_MIN:
            continue
        v5_fn = v5_callable if v5_callable is not None else _fresh_v5()
        v4b_fn = v4b_callable if v4b_callable is not None else _fresh_v4b()
        if kind == "constructed":
            results = _run_constructed_game(entry, v5_fn, v4b_fn)
            sha = {t: results[t]["res"]["action_stream_sha256"]
                   for t in ("v5", "v4b")}
            streams = {t: results[t]["res"]["streams"] for t in ("v5", "v4b")}
            finals = {t: results[t]["res"]["finals"] for t in ("v5", "v4b")}
            diff = gc.first_stream_diff(streams["v5"], streams["v4b"])
            record = {"kind": "constructed", "seed": entry["seed"],
                      "me_seat": entry.get("me_seat", 0),
                      "episode_steps": entry.get("episode_steps", 720),
                      "opp_kind": entry.get("opp_kind") or "v4b-mirror"}
        elif kind == "replay":
            replay, results = _run_replay_game(entry, v5_fn, v4b_fn)
            sha = {t: results[t]["run"]["stream_sha256"]
                   for t in ("v5", "v4b")}
            diff = ([{"seat": entry["me_seat"], "step": i,
                      "a": gc.norm_action(a)[:160],
                      "b": gc.norm_action(b)[:160]}
                     for i, (a, b) in enumerate(zip(
                         results["v5"]["run"]["stream"],
                         results["v4b"]["run"]["stream"]))
                     if gc.norm_action(a) != gc.norm_action(b)][:3])
            finals = {t: results[t]["run"]["finals"] for t in ("v5", "v4b")}
            record = {"kind": "replay", "ep": entry.get("ep"),
                      "me_seat": entry.get("me_seat"),
                      "inject_step": entry.get("inject_step", 0),
                      "tape_max_lead": entry.get("tape_max_lead"),
                      "replay_path": entry.get("replay_path")}
        else:
            raise ValueError(f"未知局类型: {kind!r}")
        identical = bool(sha["v5"] == sha["v4b"])
        meter_v5 = _meter_public(results["v5"]["meter"])
        form_present = meter_v5["form_present_calls"] > 0
        usable = not form_present
        if usable:
            if kind == "constructed":
                n_constructed += 1
            else:
                n_replay += 1
        record.update({
            "stream_sha256_v5": sha["v5"],
            "stream_sha256_v4b": sha["v4b"],
            "identical": identical,
            "first_diffs": diff,
            "finals_v5": finals["v5"], "finals_v4b": finals["v4b"],
            "trigger_form_present": form_present,
            "p4_trigger_meter_v5": meter_v5,
            "usable_as_non_trigger": usable,
        })
        per_game.append(record)
    usable_games = [g for g in per_game if g["usable_as_non_trigger"]]
    n_identical = sum(1 for g in usable_games if g["identical"])
    return {
        "protocol": "lead-protection-equivalence/1.0",
        "criterion": (f"非触发局 >= {EQUIV_MIN} 且 v5/v4b 动作流逐字节一致"
                      f"（构造>={EQUIV_CONSTRUCTED_MIN}+真实回放采样"
                      f">={EQUIV_REPLAY_MIN}；触发形态误入=该局不可用）"),
        "n": len(usable_games), "n_identical": n_identical,
        "n_seen": len(per_game),
        "n_excluded_by_trigger": len(per_game) - len(usable_games),
        "n_constructed": n_constructed,
        "n_replay": n_replay,
        "passed": bool(len(usable_games) >= EQUIV_MIN
                       and n_identical == len(usable_games)
                       and n_constructed >= EQUIV_CONSTRUCTED_MIN
                       and n_replay >= EQUIV_REPLAY_MIN),
        "per_game": per_game,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 门三：发射复检（四门复跑 + patches 单测 + 既有冒烟产物身份交叉）
# ---------------------------------------------------------------------------
def _load_launch_check_module():
    path = os.path.join(gc.SOFTWARE, "scripts",
                        "v48_derivative_launch_check.py")
    if not os.path.isfile(path):
        raise ValueError(f"launch_check 脚本缺失: {path}")
    spec = importlib.util.spec_from_file_location("lp_launch_check_base",
                                                  path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_launch_recheck(v5_package):
    """v5 发射四门复检（装载/自打/确定性/体积身份）+patches 单测确认。

    输入: v5 包路径 / 输出: 四门结果 dict / 错误: 任一门红。
    """
    t0 = time.perf_counter()
    v5_package = v5_package or V5_DIR_DEFAULT
    v5_main = os.path.join(v5_package, "main.py")
    v5_tar = os.path.join(v5_package, "submission.tar.gz")
    if not (os.path.isfile(v5_main) and os.path.isfile(v5_tar)):
        raise ValueError(f"v5 包缺失: {v5_package}")
    main_sha = gc.sha256_file(v5_main)
    tar_sha = gc.sha256_file(v5_tar)

    smoke_consistent = None
    if os.path.isfile(RECORDED_SMOKE):
        with open(RECORDED_SMOKE, encoding="utf-8") as h:
            smoke = json.load(h)
        pkg = smoke.get("package") or {}
        smoke_consistent = bool(
            smoke.get("all_gates_pass")
            and pkg.get("tar_sha256") == tar_sha
            and pkg.get("main_sha256") == main_sha)

    check = _load_launch_check_module()
    lc_tmp = os.path.join(HYB, "tmp", "lp_launch_recheck")
    check.DERIV_DIR = v5_package
    check.DERIV_MAIN = v5_main
    check.DERIV_TAR = v5_tar
    check.TMP_DIR = lc_tmp
    try:
        g23 = check.gate2_gate3()
        obs_series = g23.pop("_obs_series_seed101", None)
        g1 = check.gate1(obs_series)
        gate4_ok = os.path.getsize(v5_tar) <= (100 << 20)
        fourgate_pass = bool(
            g1["gate1_official_load_ok"]
            and g23["gate2_full_episodes_ok"]
            and g23["gate3_determinism_ok"]
            and gate4_ok)
        fourgate = {
            "gate1_official_load": {
                "ok": g1["gate1_official_load_ok"],
                "last_callable_name":
                    (g1.get("evidence") or {}).get("last_callable_name"),
                "isolated_vs_local_action_mismatches":
                    g1.get("isolated_vs_local_action_mismatches"),
                "non_stdlib_imports":
                    (g1.get("evidence") or {}).get("non_stdlib_imports"),
                "n_obs_replayed": g1.get("n_obs_replayed"),
                "driver_wall_s": g1.get("driver_wall_s")},
            "gate2_full_episodes": {
                "ok": g23["gate2_full_episodes_ok"],
                "episodes": [
                    {"seed": ep["seed"], "statuses": ep["statuses"],
                     "rewards": ep["rewards"],
                     "turns_played": ep["turns_played"],
                     "max_step_ms": ep["max_step_ms"],
                     "p99_step_ms": ep["p99_step_ms"]}
                    for ep in g23.get("gate2_episodes", [])]},
            "gate3_determinism": {
                "ok": g23["gate3_determinism_ok"],
                "hashes": g23.get("gate3_hashes")},
            "gate4_size": {
                "ok": gate4_ok, "tar_bytes": os.path.getsize(v5_tar),
                "budget_bytes": 100 << 20},
        }
    finally:
        shutil.rmtree(lc_tmp, ignore_errors=True)

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "patches", "-q"],
        cwd=HYB, capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", proc.stdout)
    patches_summary = {
        "cmd": f"{os.path.basename(sys.executable)} -m pytest patches -q",
        "returncode": proc.returncode,
        "n_passed": int(m.group(1)) if m else 0,
        "tail": proc.stdout.strip().splitlines()[-1] if proc.stdout.strip()
        else proc.stderr.strip()[-200:],
    }
    patches_ok = bool(proc.returncode == 0 and m is not None)
    return {
        "protocol": "lead-protection-launch-recheck/1.0",
        "v5_identity": {"package": v5_package, "main_sha256": main_sha,
                        "tar_sha256": tar_sha,
                        "tar_bytes": os.path.getsize(v5_tar)},
        "fourgate_rerun": fourgate,
        "fourgate_pass": fourgate_pass,
        "patches_unit_tests": patches_summary,
        "patches_tests_pass": patches_ok,
        "recorded_smoke_artifact": {
            "path": RECORDED_SMOKE,
            "consistent_with_package": smoke_consistent},
        "passed": bool(fourgate_pass and patches_ok
                       and smoke_consistent is not False),
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 裁决编排
# ---------------------------------------------------------------------------
def _gate_pass(result):
    return bool(isinstance(result, dict) and result.get("passed") is True)


def _assemble_verdict(replay_res, equiv_res, launch_res, runnable, errors,
                      v5_identity, wall_s):
    replay_pass = runnable["replay_gate"] and _gate_pass(replay_res)
    equiv_pass = runnable["equivalence"] and _gate_pass(equiv_res)
    launch_pass = runnable["launch_recheck"] and _gate_pass(launch_res)
    verdict = {
        "protocol": "lead-protection-verdict/1.0",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "v5_identity": v5_identity,
        "replay_gate": {
            "runnable": runnable["replay_gate"],
            "error": errors.get("replay_gate"),
            "wins": replay_res.get("wins") if runnable["replay_gate"] else None,
            "n": replay_res.get("n") if runnable["replay_gate"] else None,
            "criterion": f"wins >= {REPLAY_WIN_MIN}/{REPLAY_N_EXPECTED}",
            "passed": replay_pass,
            "per_game": replay_res.get("per_game")
            if runnable["replay_gate"] else None},
        "equivalence": {
            "runnable": runnable["equivalence"],
            "error": errors.get("equivalence"),
            "n_identical": equiv_res.get("n_identical")
            if runnable["equivalence"] else None,
            "n": equiv_res.get("n") if runnable["equivalence"] else None,
            "criterion": f"非触发局>={EQUIV_MIN} 且逐字节一致",
            "passed": equiv_pass,
            "per_game": equiv_res.get("per_game")
            if runnable["equivalence"] else None},
        "launch_recheck": {
            "runnable": runnable["launch_recheck"],
            "error": errors.get("launch_recheck"),
            "fourgate_pass": launch_res.get("fourgate_pass")
            if runnable["launch_recheck"] else None,
            "patches_tests_pass": launch_res.get("patches_tests_pass")
            if runnable["launch_recheck"] else None,
            "passed": launch_pass},
        "overall": "PASS" if (replay_pass and equiv_pass and launch_pass)
        else "FAIL",
        "wall_s": round(wall_s, 1),
    }
    return verdict


def verify_lead_protection(v5_package=None, corpus_dir=None):
    """验收编排：三件汇总裁决 {overall, replay_gate, equivalence, launch}；任一门不可执行=整体 fail。

    输入: v5 包+语料 / 输出: 裁决 dict / 错误: fail-closed 不抛。
    """
    t0 = time.perf_counter()
    v5_package = v5_package or V5_DIR_DEFAULT
    v5_identity = {"package": v5_package}
    try:
        v5_identity.update({
            "main_sha256": gc.sha256_file(os.path.join(v5_package, "main.py")),
            "tar_sha256": gc.sha256_file(
                os.path.join(v5_package, "submission.tar.gz"))})
    except OSError as e:
        v5_identity["error"] = str(e)

    specs = (
        ("replay_gate", lambda: run_replay_gate(corpus_dir)),
        ("equivalence", lambda: run_equivalence_face(None)),
        ("launch_recheck", lambda: run_launch_recheck(v5_package)),
    )
    results, errors, runnable = {}, {}, {}
    for name, fn in specs:
        try:
            results[name] = fn()
            runnable[name] = True
        except Exception as e:                     # fail-closed：不抛
            results[name] = None
            errors[name] = f"{type(e).__name__}: {e}"
            runnable[name] = False

    verdict = _assemble_verdict(
        results.get("replay_gate"), results.get("equivalence"),
        results.get("launch_recheck"), runnable, errors, v5_identity,
        time.perf_counter() - t0)

    if runnable["replay_gate"]:
        gc.write_json(os.path.join(_HERE, "out",
                                   "lead_protection_replay_gate.json"),
                      results["replay_gate"])
    if runnable["equivalence"]:
        gc.write_json(os.path.join(_HERE, "out",
                                   "lead_protection_equivalence.json"),
                      results["equivalence"])
    if runnable["launch_recheck"]:
        gc.write_json(os.path.join(_HERE, "out",
                                   "lead_protection_launch_recheck.json"),
                      results["launch_recheck"])
    gc.write_json(VERDICT_PATH, verdict)
    verdict["_out_path"] = VERDICT_PATH
    return verdict


def _cli() -> int:
    verdict = verify_lead_protection()
    summary = {
        "overall": verdict["overall"],
        "replay_gate": {k: verdict["replay_gate"][k]
                        for k in ("runnable", "error", "wins", "n",
                                  "criterion", "passed")},
        "equivalence": {k: verdict["equivalence"][k]
                        for k in ("runnable", "error", "n_identical", "n",
                                  "criterion", "passed")},
        "launch_recheck": {k: verdict["launch_recheck"][k]
                           for k in ("runnable", "error", "fourgate_pass",
                                     "patches_tests_pass", "passed")},
        "verdict_path": verdict["_out_path"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0 if verdict["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(_cli())
