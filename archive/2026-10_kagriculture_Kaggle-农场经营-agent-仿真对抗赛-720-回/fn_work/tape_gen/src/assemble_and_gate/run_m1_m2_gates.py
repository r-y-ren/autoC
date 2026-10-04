"""run_m1_m2_gates（L1，R6）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

M1/M2 门禁（判据=梯任务书 + hybrid R9 五线同源）：

* **M1** = 候选包 vs 纯 v48 **整局对打**（官方真引擎，席位显式：候选落
  me_seat、纯 v48 落对席；8 种子 × AB/BA 席 ≥16 局）互胜率（平局计
  0.5）≥ 0.45。
* **M2 五线**（任一不过=未到线，如实分档）：
  1. h2h vs 纯 v48 同一局集互胜（严格胜比例）≥ 0.65（先例
     v48_hybrid/gates/structure_gates.py 线一同口径）；
  2. 巨人局 seated 对照：statma/fuxi/42 回放真值流各 ≥3 局打平或更好
     （margin≥0 宽限 ≥−1000；锚局+强对手扩展集 r26 败局 margin≤−20k
     按严重度轮转每巨人 2 局——语料实测三巨人各仅 1 局，先例同规则）；
  3. 胜局回归 ≥8 局双臂对照（候选臂 vs 纯 v48 臂同点注入全季）：
     margin(候选) ≥ margin(v48) − 1000（不翻负宽限）；回归集=我方 W
     局按原 margin 最窄 8 局；
  4. 发射四门：对候选包执行 v48_derivative_launch_check 四门（官方
     装载语义/双席自打整局/确定性/体积）——fourgate_v6b.py 同法
     importlib 装载重定向路径；
  5. 经济面：seated 全季注入对普通对手回放流 ≥6 局，日收入峰
     （步级正增量按日求和，income_selfcheck 同口径）≥ 12.7k 且落
     d14-17。

通道：引擎线走 kaggle_environments 直驱（fn_work/legacy_software
kgenv.arena.load_submission_agent 官方装载语义，每席每局全新装载）；
seated 线走 fn_work rollout_with_replay_opponent（显式 me_seat、注入点
0 全季接管；twin seat1 obs.step=None 以 day*24+hour 回填修复——
gate_common.structify_obs 同法）。语料=fn_docs/references/data/
online-replays（round26/27/28，我席=TeamNames 中 renyxin 位）。

分档：line.status ∈ PASS/FAIL（跑通、判据裁决）或 ERROR（管线不成）；
overall ∈ GATES_PASS / BELOW_LINE（未到线） / PIPELINE_BROKEN。
确定性：种子/选取规则固定、canonical 报告剥离墙钟与时间戳——双跑
逐字节一致；墙钟实测落 runtime 侧件。
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
_LEGACY = _CAMPAIGN_ROOT / "fn_work" / "legacy_software"
_ONLINE_REPLAYS = (_CAMPAIGN_ROOT / "fn_docs" / "references" / "data"
                   / "online-replays")

DEFAULT_PACKAGE_MAIN = _TAPE_GEN_ROOT / "candidate" / "main.py"
DEFAULT_PACKAGE_TAR = _TAPE_GEN_ROOT / "candidate" / "submission.tar.gz"
PURE_V48_MAIN = _LEGACY / "kaggle_simulations" / "v48_derivative" / "main.py"
LAUNCH_CHECK = _LEGACY / "scripts" / "v48_derivative_launch_check.py"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "candidate" / "gates"
FOURGATE_TMP = Path("/tmp/tapegen_lc_tmp")

DEFAULT_CORPUS_DIRS = (_ONLINE_REPLAYS / "round26",
                       _ONLINE_REPLAYS / "round27",
                       _ONLINE_REPLAYS / "round28")
TEAM_NAME = "renyxin"

#: 前门种子域（launch-check gate2 同种子域）× AB/BA 席 = 16 局。
H2H_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)
H2H_SEATS = (0, 1)

THRESHOLDS = {
    "m1_min": 0.45,            # M1 互胜率（平局 0.5）
    "m2_h2h_min": 0.65,        # M2 线一严格胜比例
    "giant_ok_margin": -1000.0,
    "reg_tolerance": 1000.0,
    "econ_gate": 12700.0,
}
COUNTS = {
    "h2h_min_games": 16,
    "giant_per_name_min": 3,
    "strong_ext_per_giant": 2,
    "reg_n": 8,
    "econ_n": 6,
}
GIANT_ANCHORS = (
    ("statma", 111653327),
    ("fuxi", 111877080),
    ("42", 111898825),
)
STRONG_EXT_MARGIN_LE = -20000.0
STRONG_EXT_POOL_FROM = "round26"
ECON_WINDOW = (14, 18)        # 天窗 [d14, d17]
FULL_STEPS = 720
ACT_TIMEOUT = 60.0

_LINE_TITLES = (("h2h", "h2h_v48_gate"), ("giants", "giant_seated"),
                ("regression", "win_regression"), ("fourgate",
                                                   "launch_fourgate"),
                ("econ", "economic_face"))

#: canonical 报告剥离键（墙钟/时间戳/计时遥测/逐步观测大对象——
#: 四门 gate2 的 max/mean/p99_step_ms 是墙钟派生测量，双跑必抖）。
_WALL_KEYS = {"wall_s", "wall_total_s", "wall_clock_s", "wall_clock_used_s",
              "driver_wall_s", "generated_utc", "obs_series",
              "_obs_series_seed101", "elapsed_s", "max_step_ms",
              "p99_step_ms", "mean_step_ms", "min_step_ms"}


# ---------------------------------------------------------------------------
# 通道基建（旧树只读消费；进程内一次）
# ---------------------------------------------------------------------------
def _legacy_paths():
    for p in (str(_LEGACY), str(_LEGACY / "kgenv"),
              str(_CAMPAIGN_ROOT / "fn_work" / "src"
                  / "run_official_bench")):
        if p not in sys.path:
            sys.path.insert(0, p)
    sys.dont_write_bytecode = True


def load_submission_agent(path):
    """官方提交语义装载（kgenv.arena，named `agent` 优先）。"""
    _legacy_paths()
    from kgenv.arena import load_submission_agent as _load
    return _load(str(path))


class _ObsStruct(dict):
    """dict+属性双视图（官方 obs 形态最小复刻）。"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e


def structify_obs(obs) -> _ObsStruct:
    """twin Observation → 官方 dict+attr 形态；seat1 step=None 按
    day*24+hour 回填（T3 发现的 legacy twin 缺陷，tape_gen 侧修复）。"""
    out = _ObsStruct()
    for k in ("farms", "market", "town", "day", "hour", "step", "player",
              "private", "remainingOverageTime"):
        v = getattr(obs, k, None)
        if v is not None or hasattr(obs, k):
            out[k] = v
    for k in getattr(obs, "__slots__", ()):
        if k not in out and hasattr(obs, k):
            out[k] = getattr(obs, k)
    if out.get("step") is None and out.get("day") is not None:
        out["step"] = int(out["day"]) * 24 + int(out.get("hour") or 0)
    return out


def engine_game(fn0, fn1, seed):
    """官方真引擎单局（gate_common.run_engine_game 同口径）。"""
    _legacy_paths()
    from kaggle_environments import make
    t0 = time.perf_counter()
    env = make("kaggriculture",
               configuration={"episodeSteps": FULL_STEPS, "seed": int(seed),
                              "actTimeout": ACT_TIMEOUT},
               debug=True)
    env.run([fn0, fn1])
    final = env.steps[-1]
    rewards = [float(s["reward"]) for s in final]
    statuses = [s["status"] for s in final]
    raw_logs = [str(line) for line in getattr(env, "logs", []) if line]
    suspicious = [s[:300] for s in raw_logs
                  if "ERROR" in s or "Timed out" in s or "Traceback" in s]
    return {
        "rewards": rewards,
        "statuses": statuses,
        "turns_played": len(env.steps),
        "suspicious_log_lines": suspicious,
        "wall_s": round(time.perf_counter() - t0, 2),
    }


class _ReplayCache:
    """回放按路径解析一次（单件 >30MB；seated 多线复用）。"""

    def __init__(self):
        self._map = {}

    def get(self, path):
        key = str(path)
        if key not in self._map:
            self._map[key] = json.loads(
                Path(key).read_text(encoding="utf-8"))
        return self._map[key]


def _count_sheep(farm) -> int:
    n = 0
    for row in farm.get("tiles") or []:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") == "SHEEP":
                n += 1
    return n


def _income_curve(money_series, n_days=30):
    """日收入=日内步级正增量求和（income_selfcheck 同口径）。"""
    curve = []
    for day in range(n_days):
        lo, hi = day * 24, min(day * 24 + 24, len(money_series) - 1)
        curve.append(round(sum(max(0.0, money_series[i + 1]
                                   - money_series[i])
                               for i in range(lo, hi)), 1))
    return curve


def seated_rollout(replay, me_seat, agent, track=False):
    """全季（注入点 0）seated 回放流 rollout（候选注入 me_seat、对手=
    回放真值流对席）。track=True 时记录我席资金序列（经济面计量）。"""
    _legacy_paths()
    from rollout_with_replay_opponent import make_twin_deps
    deps = make_twin_deps()
    start = 0
    state = deps["build"](replay, start)
    opp_actions = deps["transition_actions"](replay)
    me = int(me_seat)
    money_series = []

    def wrapped(obs):
        if track:
            farm = obs.farms[me]
            money_series.append(float(farm["money"]))
        return agent(structify_obs(obs))

    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while (not state.env.done and start + taken < len(opp_actions)
           and taken < max_steps):
        obs = state.seats[me].observation
        mine = wrapped(obs)
        pair = [opp_actions[start + taken][1 - me]] * 2
        pair[me] = mine
        deps["step"](state, pair)
        taken += 1
    finals = deps["final"](state)
    out = {
        "finals": [round(float(x), 1) for x in finals],
        "margin": round(float(finals[me]) - float(finals[1 - me]), 1),
        "steps": taken,
    }
    if track:
        series = money_series + [float(finals[me])]
        curve = _income_curve(series)
        lo, hi = ECON_WINDOW
        peak = max(curve[lo:hi]) if len(curve) >= hi else None
        out["income_curve"] = curve
        out["peak_d14_17"] = peak
        out["peak_day"] = lo + curve[lo:hi].index(peak) \
            if peak is not None else None
        out["season_peak"] = max(curve)
        out["season_peak_day"] = curve.index(max(curve))
    return out


# ---------------------------------------------------------------------------
# 语料扫描与选取（确定性纯函数）
# ---------------------------------------------------------------------------
def scan_corpus(dirs=None):
    """扫描回放目录 → 局记录（我席=TeamNames 中 TEAM_NAME 位）。"""
    dirs = DEFAULT_CORPUS_DIRS if dirs is None else dirs
    games = []
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            raise ValueError(f"语料目录缺失 (fail-closed): {d}")
        for name in sorted(os.listdir(d)):
            if not (name.startswith("episode-")
                    and name.endswith("-replay.json")):
                continue
            path = d / name
            with open(path, encoding="utf-8") as fh:
                replay = json.load(fh)
            ep = int(name.split("-")[1])
            info = replay.get("info") or {}
            names = info.get("TeamNames") or [
                (a or {}).get("Name") for a in (info.get("Agents") or [])]
            if TEAM_NAME not in names or len(names) != 2:
                continue
            me = names.index(TEAM_NAME)
            rw = replay.get("rewards")
            if not (isinstance(rw, list) and len(rw) == 2):
                raise ValueError(f"ep{ep} rewards 缺失: {path}")
            margin = float(rw[me]) - float(rw[1 - me])
            games.append({
                "ep": ep, "round": d.name, "me_seat": me,
                "opp": names[1 - me], "margin": margin,
                "result": "W" if margin > 0 else (
                    "L" if margin < 0 else "T"),
                "mirror": names[1 - me] == TEAM_NAME,
                "replay_path": str(path),
            })
    if not games:
        raise ValueError("语料扫描为空 (fail-closed)")
    return games


def select_strong_ext_pool(games):
    anchor_eps = {ep for _, ep in GIANT_ANCHORS}
    pool = [g for g in games
            if g["round"] == STRONG_EXT_POOL_FROM
            and g["result"] == "L"
            and g["margin"] <= STRONG_EXT_MARGIN_LE
            and g["ep"] not in anchor_eps]
    return sorted(pool, key=lambda g: (g["margin"], g["ep"]))


def select_giant_games(games):
    """每巨人 ≥3 局：其其他对局（若有）优先 → 锚局 → 强对手扩展集
    （败局 margin≤−20k 按严重度轮转每巨人 2 局）。"""
    pool = select_strong_ext_pool(games)
    need_ext = COUNTS["strong_ext_per_giant"]
    out = {}
    for idx, (name, anchor_ep) in enumerate(GIANT_ANCHORS):
        others = sorted([g for g in games
                         if g["opp"] == name and g["ep"] != anchor_ep],
                        key=lambda g: g["ep"])[:COUNTS[
                            "giant_per_name_min"] - 1]
        ext = pool[idx * need_ext:idx * need_ext + max(
            0, COUNTS["giant_per_name_min"] - 1 - len(others))]
        anchor = [g for g in games if g["ep"] == anchor_ep]
        if not anchor:
            raise ValueError(f"巨人锚局缺失 (fail-closed): {name} "
                             f"ep{anchor_ep}")
        picks = others + [anchor[0]] + ext
        if len(picks) < COUNTS["giant_per_name_min"]:
            raise ValueError(f"巨人 {name} 局数不足: {len(picks)}")
        out[name] = picks
    return out


def select_regression_games(games):
    """胜局回归集：W 局按原 margin 升序取最窄 COUNTS['reg_n'] 局。"""
    wins = sorted([g for g in games if g["result"] == "W"],
                  key=lambda g: (g["margin"], g["ep"]))
    if len(wins) < COUNTS["reg_n"]:
        raise ValueError(f"W 局不足 (fail-closed): {len(wins)}")
    return wins[:COUNTS["reg_n"]]


def select_economic_games(games):
    """经济面局集：普通对手局（剔巨人/强扩展/镜像/回归集）ep 升序取
    COUNTS['econ_n'] 局。"""
    taken_eps = ({ep for _, ep in GIANT_ANCHORS}
                 | {g["ep"] for g in select_strong_ext_pool(games)}
                 | {g["ep"] for g in select_regression_games(games)})
    giant_names = {name for name, _ in GIANT_ANCHORS}
    ordinary = sorted([g for g in games
                       if not g["mirror"] and g["opp"] not in giant_names
                       and g["ep"] not in taken_eps],
                      key=lambda g: g["ep"])
    if len(ordinary) < COUNTS["econ_n"]:
        raise ValueError(f"普通对手局不足 (fail-closed): {len(ordinary)}")
    return ordinary[:COUNTS["econ_n"]]


# ---------------------------------------------------------------------------
# 门线实现
# ---------------------------------------------------------------------------
def _play_h2h_series(package_main, base_main, seeds, seats, runners):
    """候选 vs 纯 v48（每局全新装载，候选显式落 me_seat 席）。"""
    engine = runners.get("engine_game") or engine_game
    loader = runners.get("load_agent") or load_submission_agent
    games = []
    for seed in seeds:
        for seat in seats:
            pair = [loader(base_main), loader(base_main)]
            pair[seat] = loader(package_main)
            rec = engine(pair[0], pair[1], seed)
            me, opp = rec["rewards"][seat], rec["rewards"][1 - seat]
            margin = me - opp
            games.append({
                "seed": seed, "me_seat": seat,
                "me_money": round(me, 1), "opp_money": round(opp, 1),
                "margin": round(margin, 1),
                "result": "WIN" if margin > 0 else (
                    "TIE" if margin == 0 else "LOSS"),
                "statuses": rec["statuses"],
                "turns": rec["turns_played"],
                "suspicious_log_lines": rec.get(
                    "suspicious_log_lines", []),
            })
    return games


def _summarize_h2h(games):
    n = len(games)
    w = sum(1 for g in games if g["result"] == "WIN")
    t = sum(1 for g in games if g["result"] == "TIE")
    margins = [g["margin"] for g in games]
    by_seat = {}
    for seat in (0, 1):
        sub = [g for g in games if g["me_seat"] == seat]
        by_seat[str(seat)] = {
            "games": len(sub),
            "wins": sum(1 for g in sub if g["result"] == "WIN"),
            "losses": sum(1 for g in sub if g["result"] == "LOSS"),
            "ties": sum(1 for g in sub if g["result"] == "TIE")}
    return {
        "games": n, "wins": w, "ties": t, "losses": n - w - t,
        "win_rate_half_ties": round((w + 0.5 * t) / n, 4) if n else None,
        "win_fraction_strict": round(w / n, 4) if n else None,
        "avg_margin": round(sum(margins) / max(1, n), 1),
        "margin_distribution": {
            "pos": sum(1 for m in margins if m > 0),
            "neg": sum(1 for m in margins if m < 0),
            "zero": sum(1 for m in margins if m == 0)},
        "by_seat": by_seat,
        "all_done": all(g["statuses"] == ["DONE", "DONE"] for g in games),
        "records": games,
    }


def _run_h2h(payload, runners):
    package_main = payload.get("package_main") or DEFAULT_PACKAGE_MAIN
    base_main = payload.get("base_main") or PURE_V48_MAIN
    seeds = tuple(payload.get("h2h_seeds") or H2H_SEEDS)
    seats = tuple(payload.get("h2h_seats") or H2H_SEATS)
    t0 = time.perf_counter()
    games = _play_h2h_series(package_main, base_main, seeds, seats, runners)
    summary = _summarize_h2h(games)
    m1 = dict(summary)
    m1.update({
        "protocol": "m1-h2h-v48/1.0",
        "criterion": (f"候选包 vs 纯 v48 官方引擎整局对打 ≥"
                      f"{COUNTS['h2h_min_games']} 局（种子×AB/BA 席），"
                      f"互胜率（平局 0.5）≥ {THRESHOLDS['m1_min']}"),
        "opponent": {"kind": "pure_v48", "path": str(base_main)},
        "passed": bool(
            summary["games"] >= COUNTS["h2h_min_games"]
            and summary["win_rate_half_ties"] >= THRESHOLDS["m1_min"]),
    })
    line1 = {k: v for k, v in summary.items() if k != "records"}
    line1.update({
        "protocol": "m2-h2h-v48-gate/1.0",
        "criterion": (f"同局集严格互胜 wins/n ≥ "
                      f"{THRESHOLDS['m2_h2h_min']}（先例线一同口径）"),
        "passed": bool(
            summary["games"] >= COUNTS["h2h_min_games"]
            and summary["win_fraction_strict"] >= THRESHOLDS["m2_h2h_min"]),
    })
    m1["wall_s"] = line1["wall_s"] = round(time.perf_counter() - t0, 1)
    return m1, line1


def _run_giant_seated(payload, runners, cache):
    t0 = time.perf_counter()
    games = payload.get("corpus") or scan_corpus(
        payload.get("corpus_dirs"))
    by_name = select_giant_games(games)
    loader = runners.get("load_agent") or load_submission_agent
    seated = runners.get("seated") or None
    per_name = {}
    for name, picks in by_name.items():
        rows = []
        for g in picks:
            agent = loader(payload.get("package_main")
                           or DEFAULT_PACKAGE_MAIN)
            if seated is not None:
                run = seated(cache.get(g["replay_path"]),
                             g["me_seat"], agent)
            else:
                run = seated_rollout(cache.get(g["replay_path"]),
                                     g["me_seat"], agent)
            ok = run["margin"] >= THRESHOLDS["giant_ok_margin"]
            rows.append({
                "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
                "role": ("anchor" if g["ep"] in {
                    ep for _, ep in GIANT_ANCHORS}
                    else "other" if g["opp"] == name else "strong_ext"),
                "orig_margin": round(g["margin"], 1),
                "cand_margin": run["margin"],
                "cand_finals": run["finals"],
                "delta_vs_orig": round(run["margin"] - g["margin"], 1),
                "steps": run["steps"], "ok": ok})
        per_name[name] = {
            "games": len(rows),
            "all_ok": all(r["ok"] for r in rows),
            "best_margin": max(r["cand_margin"] for r in rows),
            "records": rows}
    passed = all(v["games"] >= COUNTS["giant_per_name_min"] and v["all_ok"]
                 for v in per_name.values())
    return {
        "protocol": "m2-giant-seated-gate/1.0",
        "criterion": (f"对 statma/fuxi/42 回放真值流各 ≥"
                      f"{COUNTS['giant_per_name_min']} 局打平或更好"
                      f"（margin≥0 宽限 ≥"
                      f"{THRESHOLDS['giant_ok_margin']:.0f}）"),
        "corpus_rule": ("三巨人各自其他对局优先（语料实测均无）→ 锚局 + "
                        f"{STRONG_EXT_POOL_FROM} 强对手扩展集（败局 "
                        f"margin≤{STRONG_EXT_MARGIN_LE:.0f} 按严重度轮转"
                        f"每巨人 {COUNTS['strong_ext_per_giant']} 局）"),
        "per_giant": per_name,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


def _run_win_regression(payload, runners, cache):
    t0 = time.perf_counter()
    games = payload.get("corpus") or scan_corpus(
        payload.get("corpus_dirs"))
    picks = select_regression_games(games)
    loader = runners.get("load_agent") or load_submission_agent
    seated = runners.get("seated")
    per_game = []
    for g in picks:
        replay = cache.get(g["replay_path"])
        if seated is not None:
            cand = seated(replay, g["me_seat"],
                          loader(payload.get("package_main")
                                 or DEFAULT_PACKAGE_MAIN))
            base = seated(replay, g["me_seat"],
                          loader(payload.get("base_main")
                                 or PURE_V48_MAIN))
        else:
            cand = seated_rollout(replay, g["me_seat"],
                                  loader(payload.get("package_main")
                                         or DEFAULT_PACKAGE_MAIN))
            base = seated_rollout(replay, g["me_seat"],
                                  loader(payload.get("base_main")
                                         or PURE_V48_MAIN))
        delta = cand["margin"] - base["margin"]
        ok = cand["margin"] >= base["margin"] - THRESHOLDS[
            "reg_tolerance"]
        per_game.append({
            "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
            "orig_margin": round(g["margin"], 1),
            "margin_v48_arm": base["margin"],
            "margin_cand_arm": cand["margin"],
            "delta": round(delta, 1), "ok": ok,
            "flipped_negative": bool(base["margin"] > 0
                                     and cand["margin"] < 0),
            "cand_finals": cand["finals"], "v48_finals": base["finals"]})
    n_ok = sum(1 for r in per_game if r["ok"])
    passed = bool(len(per_game) >= COUNTS["reg_n"] and n_ok == len(per_game))
    return {
        "protocol": "m2-win-regression-gate/1.0",
        "criterion": (f"胜局回归 ≥{COUNTS['reg_n']} 局（原 margin 最窄"
                      f"选取）双臂对照，逐局 margin(候选) ≥ margin(v48) − "
                      f"{THRESHOLDS['reg_tolerance']:.0f}"),
        "selection_rule": "全语料我方 W 局按原 margin 升序取最窄 8 局",
        "games": len(per_game), "n_ok": n_ok,
        "flipped_negative_games": [r["ep"] for r in per_game
                                   if r["flipped_negative"]],
        "per_game": per_game,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


def _run_fourgate(payload, runners):
    """发射四门（launch-check 重定向至候选包；fourgate_v6b 同法）。"""
    t0 = time.perf_counter()
    if "fourgate" in runners:
        result = runners["fourgate"](payload)
        result.setdefault("passed", result.get("all_gates_pass"))
        result["wall_s"] = round(time.perf_counter() - t0, 1)
        return result
    package_main = Path(payload.get("package_main") or DEFAULT_PACKAGE_MAIN)
    package_tar = Path(payload.get("package_tar") or DEFAULT_PACKAGE_TAR)
    out_dir = Path(payload.get("fourgate_out")
                   or (DEFAULT_OUTPUT_DIR / "fourgate"))
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location(
        "tapegen_launch_check", str(LAUNCH_CHECK))
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    check.DERIV_DIR = str(package_main.parent)
    check.DERIV_MAIN = str(package_main)
    check.DERIV_TAR = str(package_tar)
    check.OUT_DIR = str(out_dir)
    check.TMP_DIR = str(FOURGATE_TMP)

    g23 = check.gate2_gate3()
    obs_seed101 = g23.pop("_obs_series_seed101", None)
    g1 = check.gate1(obs_seed101)
    tar_bytes = package_tar.stat().st_size
    size_ok = tar_bytes <= (100 << 20)
    result = {
        "protocol": "m2-launch-fourgate/1.0",
        "criterion": ("官方装载语义（干净 -I 子进程）/ 双席自打整局 DONE"
                      "/ 确定性重跑一致 / tar ≤ 100MB"),
        "gate1_official_load": g1,
        "gate2_gate3": g23,
        "gate4_size": {"tar_bytes": tar_bytes, "ok": size_ok},
        "package": {
            "main_sha256": check.sha256_bytes(
                package_main.read_bytes()),
            "tar_sha256": check.sha256_bytes(package_tar.read_bytes()),
        },
    }
    result["all_gates_pass"] = bool(
        g1["gate1_official_load_ok"]
        and g23["gate2_full_episodes_ok"]
        and g23["gate3_determinism_ok"] and size_ok)
    result["passed"] = result["all_gates_pass"]
    result["wall_s"] = round(time.perf_counter() - t0, 1)
    return result


def _run_economic_face(payload, runners, cache):
    t0 = time.perf_counter()
    games = payload.get("corpus") or scan_corpus(
        payload.get("corpus_dirs"))
    picks = select_economic_games(games)
    loader = runners.get("load_agent") or load_submission_agent
    seated = runners.get("seated")
    per_game = []
    for g in picks:
        agent = loader(payload.get("package_main")
                       or DEFAULT_PACKAGE_MAIN)
        if seated is not None:
            run = seated(cache.get(g["replay_path"]), g["me_seat"],
                         agent, track=True)
        else:
            run = seated_rollout(cache.get(g["replay_path"]),
                                 g["me_seat"], agent, track=True)
        peak = run.get("peak_d14_17")
        ok = bool(peak is not None and peak >= THRESHOLDS["econ_gate"])
        per_game.append({
            "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
            "orig_margin": round(g["margin"], 1),
            "cand_margin": run["margin"],
            "peak_d14_17": peak, "peak_day": run.get("peak_day"),
            "season_peak": run.get("season_peak"),
            "season_peak_day": run.get("season_peak_day"),
            "final_money": run["finals"][g["me_seat"]],
            "ok": ok})
    best = max((r["peak_d14_17"] or 0.0) for r in per_game) \
        if per_game else 0.0
    passed = bool(len(per_game) >= COUNTS["econ_n"]
                  and best >= THRESHOLDS["econ_gate"])
    return {
        "protocol": "m2-economic-face/1.0",
        "criterion": (f"≥{COUNTS['econ_n']} 局 seated 普通对手回放流，"
                      f"日收入峰 ≥{THRESHOLDS['econ_gate']:.0f} 且落 "
                      f"d{ECON_WINDOW[0]}-d{ECON_WINDOW[1] - 1}"),
        "selection_rule": "普通对手局（剔巨人/强扩展/镜像/回归集）ep 升序",
        "measurement": ("资金序列=我席决策步 obs.farms[me].money+终局；"
                        "日收入=日内步级正增量求和；峰=max(d14..d17)"),
        "games": len(per_game), "best_peak_d14_17": round(best, 1),
        "per_game": per_game,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
def _strip_walls(obj):
    """canonical 化：剥离墙钟/时间戳/大对象（双跑一致比较面）。"""
    if isinstance(obj, dict):
        return {k: _strip_walls(v) for k, v in obj.items()
                if k not in _WALL_KEYS}
    if isinstance(obj, list):
        return [_strip_walls(v) for v in obj]
    if isinstance(obj, tuple):
        return [_strip_walls(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def run_m1_m2_gates(payload=None):
    """意图级签名；真值在责任文档。

    payload：{package_main, package_tar, base_main, output_dir,
    h2h_seeds, h2h_seats, corpus_dirs, corpus（预扫结果）,
    runners（可注入：engine_game/load_agent/seated/fourgate）,
    lines（子集选择）, write=True}。
    返回 {m1, m2:{lines,...}, grading, paths}；任一线 ERROR 分档
    PIPELINE_BROKEN（不抛，错误入 dict——R6 如实分档语义）。
    """
    payload = dict(payload or {})
    runners = dict(payload.get("runners") or {})
    cache = _ReplayCache()
    wanted = payload.get("lines")
    results = {"m1": None, "h2h": None, "giants": None,
               "regression": None, "fourgate": None, "econ": None}
    errors = {}

    specs = [
        ("m1+h2h", lambda: _run_h2h(payload, runners)),
        ("giants", lambda: _run_giant_seated(payload, runners, cache)),
        ("regression", lambda: _run_win_regression(payload, runners,
                                                   cache)),
        ("fourgate", lambda: _run_fourgate(payload, runners)),
        ("econ", lambda: _run_economic_face(payload, runners, cache)),
    ]
    for name, fn in specs:
        if wanted and name not in wanted and not (
                name == "m1+h2h" and ("m1" in wanted or "h2h" in wanted)):
            continue
        try:
            out = fn()
            if name == "m1+h2h":
                results["m1"], results["h2h"] = out
            else:
                results[name] = out
        except Exception as exc:                    # noqa: BLE001
            errors[name] = f"{type(exc).__name__}: {exc}"

    m1 = results.pop("m1")
    lines = {}
    for key, title in _LINE_TITLES:
        r = results.get(key)
        err_key = "m1+h2h" if key == "h2h" else key
        lines[key] = {
            "title": title,
            "runnable": r is not None,
            "error": errors.get(err_key),
            "result": r,
            "passed": bool(r is not None and r.get("passed") is True),
        }

    line_errors = [f"{k}: {lines[k]['error']}" for k in lines
                   if lines[k]["error"]]
    m2_pass = all(v["passed"] for v in lines.values())
    m1_pass = bool(m1 is not None and m1.get("passed"))
    if line_errors or m1 is None:
        grading = {"m1": "ERROR" if m1 is None else
                   ("PASS" if m1_pass else "FAIL"),
                   "m2": "ERROR", "overall": "PIPELINE_BROKEN",
                   "errors": line_errors or ["m1: not run"]}
    elif m1_pass and m2_pass:
        grading = {"m1": "PASS", "m2": "PASS", "overall": "GATES_PASS"}
    else:
        grading = {"m1": "PASS" if m1_pass else "FAIL",
                   "m2": "PASS" if m2_pass else "FAIL",
                   "overall": "BELOW_LINE",
                   "failed_lines": [k for k, v in lines.items()
                                    if not v["passed"]] +
                   ([] if m1_pass else ["m1"])}

    report = {
        "protocol": "m1m2-gates/1.0",
        "under_test": {
            "package_main": str(payload.get("package_main")
                                or DEFAULT_PACKAGE_MAIN),
            "package_tar": str(payload.get("package_tar")
                               or DEFAULT_PACKAGE_TAR),
            "baseline_pure_v48": str(payload.get("base_main")
                                     or PURE_V48_MAIN),
        },
        "thresholds": dict(THRESHOLDS),
        "counts": dict(COUNTS),
        "m1": m1,
        "m2": {"lines": lines, "passed": m2_pass},
        "grading": grading,
    }

    paths = {}
    if payload.get("write", True):
        out_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = out_dir / "m1m2_report.json"
        report_path.write_text(json.dumps(
            _strip_walls(report), ensure_ascii=False, indent=1,
            sort_keys=True) + "\n", encoding="utf-8")
        runtime_path = out_dir / "m1m2_runtime.json"
        runtime_path.write_text(json.dumps(
            {"walls": {
                "m1": (m1 or {}).get("wall_s"),
                **{k: ((v.get("result") or {}).get("wall_s")
                       if isinstance(v.get("result"), dict) else None)
                   for k, v in lines.items()}}},
            ensure_ascii=False, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
        paths = {"report": str(report_path),
                 "runtime": str(runtime_path), "output_dir": str(out_dir)}
    report["paths"] = paths
    return report


def _cli() -> int:
    report = run_m1_m2_gates()
    slim = {"grading": report["grading"],
            "m1": {k: report["m1"][k] for k in
                   ("games", "wins", "ties", "losses",
                    "win_rate_half_ties", "win_fraction_strict",
                    "by_seat", "avg_margin", "passed")},
            "m2": {k: {"passed": v["passed"], "error": v["error"],
                       "summary": _line_slim(k, v["result"])}
                   for k, v in report["m2"]["lines"].items()}}
    print(json.dumps(slim, ensure_ascii=False, indent=1))
    return 0 if report["grading"]["overall"] == "GATES_PASS" else 1


def _line_slim(key, r):
    if not isinstance(r, dict):
        return None
    if key == "h2h":
        return {k: r[k] for k in ("games", "wins",
                                  "win_fraction_strict", "avg_margin")}
    if key == "giants":
        return {n: {"games": v["games"], "all_ok": v["all_ok"],
                    "best_margin": v["best_margin"]}
                for n, v in r["per_giant"].items()}
    if key == "regression":
        return {"games": r["games"], "n_ok": r["n_ok"],
                "flipped_negative_games": r["flipped_negative_games"]}
    if key == "econ":
        return {"games": r["games"], "best_peak_d14_17":
                r["best_peak_d14_17"]}
    if key == "fourgate":
        return {"all_gates_pass": r.get("all_gates_pass")}
    return None


if __name__ == "__main__":
    raise SystemExit(_cli())
