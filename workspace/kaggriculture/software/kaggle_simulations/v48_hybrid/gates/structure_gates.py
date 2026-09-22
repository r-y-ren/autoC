# -*- coding: utf-8 -*-
"""R9-G3 结构五线终审（verify_structure_gates）。

上游契约: fn_docs/responsibility.md R9 增补段（功能块 verify_structure_gates
← R9）+ fn_docs/requirements.md R9 验收方式（五线全过）。

五线（判据=requirements R9）：
1. run_h2h_v48_gate      v6b vs 纯 v48 ≥16 局（8 种子 AB/BA）互胜 ≥0.65
                        （官方真引擎 seated，席位显式）。
2. run_giant_seated_gate v6b 全季注入 vs statma/fuxi/42 回放真值流各 ≥3 局
                        打平或更好（margin≥0，宽限差距≤1k）。
                        语料=hybrid 败局中三巨人锚局（各自其他对局不足时用
                        其对局本身+r26full 强对手扩展集：败局 margin≤-20k
                        按严重度排序，每巨人补 2 局）。
3. run_win_regression_gate 胜局回归 ≥8 局双臂对照（v6b 臂 vs 原 v48 臂同点
                        注入）；不翻负=margin(v6b) ≥ margin(v48) − 1k。
                        回归集=r26full+r27full 我方 W 局取原 margin 最窄 8 局
                        （最易翻负面）。
4. run_fourgate_reference 发射四门引用（G2b 已 PASS，tmp/probes_v6b/
                        v6b_smoke.json 交叉）+ 装载复检一次（身份 sha +
                        官方装载语义 callable 一步应答）。
5. run_economic_face    seated 口径：v6b 全季注入对普通对手回放流 ≥6 局，
                        日收入峰（SELL 侧步级正增量按日求和，G2b
                        income_selfcheck 同口径）≥12.7k 且落 d14-17。

通道语义：seated 线全部走 fn_work rollout_with_replay_opponent（显式
me_seat 注入、对手=回放真值动作流、注入点=0 全季接管）；通道有效性已由
"纯 v48 注入 r26full 复现原局 rewards（±13 内）"金标准锚定。

yarn2 种子漂移说明（G2b 遗留）：G3 五线不含构造 yarn2 局（巨人/回归/经济
面全为回放流 seated，h2h 为官方引擎固定种子域 101-104/201-204），回放的
info.seed 随件固定故无逐构建重扫义务。

产物纪律：本文件与其测试为 gates/ 新增；不改任何现存文件；裁决落
gates/out/structure_verdict.json + 分线 JSON；临时件落 v48_hybrid/tmp/。
CLI：python gates/structure_gates.py [--line h2h|giants|regression|econ]
（默认全五线编排水到渠成落盘）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

HYB = gc.HYB
V6B_DIR = os.path.join(HYB, "v6b")
V6B_MAIN = os.path.join(V6B_DIR, "main.py")
V6B_TAR = os.path.join(V6B_DIR, "submission.tar.gz")
G2B_SMOKE = os.path.join(HYB, "tmp", "probes_v6b", "v6b_smoke.json")

R26FULL = "/tmp/r26full"
R27FULL = "/tmp/r27full"
CORPUS_DIRS = (R26FULL, R27FULL)

TEAM_NAME = "renyxin"
H2H_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)   # 前门同种子域
H2H_GAMES_MIN = 16
H2H_WIN_MIN = 0.65

GIANT_ANCHORS = (                                # (名字, ep, 语料目录)
    ("statma", 111653327, R26FULL),
    ("fuxi", 111877080, R27FULL),
    ("42", 111898825, R27FULL),
)
GIANT_PER_NAME_MIN = 3
GIANT_OK_MARGIN = -1000.0        # 打平或更好：margin≥0，宽限差距≤1k
STRONG_EXT_POOL_FROM = R26FULL   # 强对手扩展集只取 r26full
STRONG_EXT_MARGIN_LE = -20000.0  # 强对手局=败局 margin≤-20k（锚局除外）
STRONG_EXT_PER_GIANT = 2

REG_N = 8                         # 胜局回归局数
REG_TOLERANCE = 1000.0            # 不翻负宽限：margin(v6b)≥margin(v48)−1k

ECON_N = 6                        # 经济面局数
ECON_GATE = 12700.0               # 收入峰 ≥12.7k@d14-17
ECON_WINDOW = (14, 18)            # 天窗 [d14, d17]

VERDICT_PATH = os.path.join(gc.OUT_DIR, "structure_verdict.json")
LINE_OUT = {name: os.path.join(gc.OUT_DIR, f"structure_{name}.json")
            for name in ("h2h", "giants", "regression", "econ",
                         "fourgate")}


def _v6b_sha_expected() -> str:
    """build_manifest 登记的期望 sha（防本文件手抄漂移，以包内登记为准）。"""
    with open(os.path.join(V6B_DIR, "build_manifest.json"),
              encoding="utf-8") as h:
        m = json.load(h)
    return (m["main_py"]["sha256"],
            m["submission_tar_gz"]["sha256"])


# ---------------------------------------------------------------------------
# 语料扫描与选取（确定性：同一语料状态必得同一局集）
# ---------------------------------------------------------------------------
def scan_corpus(dirs=None) -> list:
    """扫描回放目录 → 局记录 [{ep,dir,me_seat,opp,margin,result,replay_path}]。

    我席=info.TeamNames 中 TEAM_NAME 位；镜像局（对手同名）标记 mirror。
    dirs=None 时取模块级 CORPUS_DIRS（调用期解析，可被测试替换）。
    """
    if dirs is None:
        dirs = CORPUS_DIRS
    games = []
    for d in dirs:
        if not os.path.isdir(d):
            raise ValueError(f"语料目录缺失: {d}")
        for name in sorted(os.listdir(d)):
            if not (name.startswith("episode-") and name.endswith(
                    "-replay.json")):
                continue
            path = os.path.join(d, name)
            with open(path, encoding="utf-8") as h:
                replay = json.load(h)
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
                "ep": ep, "dir": d, "me_seat": me,
                "opp": names[1 - me],
                "margin": margin,
                "result": "W" if margin > 0 else ("L" if margin < 0 else "T"),
                "mirror": names[1 - me] == TEAM_NAME,
                "replay_path": path,
            })
    if not games:
        raise ValueError("语料扫描为空")
    return games


def select_strong_ext_pool(games) -> list:
    """强对手扩展集：r26full 败局 margin≤STRONG_EXT_MARGIN_LE（锚局除外），
    按严重度（最负优先）稳定排序。"""
    anchor_eps = {ep for _, ep, _ in GIANT_ANCHORS}
    pool = [g for g in games
            if g["dir"] == STRONG_EXT_POOL_FROM
            and g["result"] == "L"
            and g["margin"] <= STRONG_EXT_MARGIN_LE
            and g["ep"] not in anchor_eps]
    return sorted(pool, key=lambda g: (g["margin"], g["ep"]))


def select_giant_games(games) -> dict:
    """每巨人 ≥3 局：先取其**其他对局**（同对手名非锚局），不足则锚局本身
    + 强对手扩展集补足（池按严重度轮转分配，锚局优先）。"""
    pool = select_strong_ext_pool(games)
    out = {}
    for idx, (name, anchor_ep, _dir) in enumerate(GIANT_ANCHORS):
        others = sorted([g for g in games
                         if g["opp"] == name and g["ep"] != anchor_ep],
                        key=lambda g: g["ep"])
        need = GIANT_PER_NAME_MIN - 1 - len(others[:GIANT_PER_NAME_MIN - 1])
        ext = pool[idx * STRONG_EXT_PER_GIANT:
                   idx * STRONG_EXT_PER_GIANT + max(0, need)]
        anchor = [g for g in games if g["ep"] == anchor_ep]
        if not anchor:
            raise ValueError(f"巨人锚局缺失: {name} ep{anchor_ep}")
        picks = others[:GIANT_PER_NAME_MIN - 1] + [anchor[0]] + ext
        if len(picks) < GIANT_PER_NAME_MIN:
            raise ValueError(f"巨人 {name} 局数不足: {len(picks)}")
        out[name] = picks
    return out


def select_regression_games(games) -> list:
    """胜局回归集：两语料我方 W 局按原 margin 升序取最窄 REG_N 局。"""
    wins = [g for g in games if g["result"] == "W"]
    wins.sort(key=lambda g: (g["margin"], g["ep"]))
    if len(wins) < REG_N:
        raise ValueError(f"W 局不足: {len(wins)} < {REG_N}")
    return wins[:REG_N]


def select_economic_games(games) -> list:
    """经济面局集：普通对手局（剔除巨人/强扩展/镜像/回归集）按 ep 升序取
    ECON_N 局（与回归集不相交，避免两线耦合同一局）。"""
    taken_eps = ({ep for _, ep, _ in GIANT_ANCHORS}
                 | {g["ep"] for g in select_strong_ext_pool(games)}
                 | {g["ep"] for g in select_regression_games(games)})
    giant_names = {name for name, _, _ in GIANT_ANCHORS}
    ordinary = [g for g in games
                if not g["mirror"] and g["opp"] not in giant_names
                and g["ep"] not in taken_eps]
    ordinary.sort(key=lambda g: g["ep"])
    if len(ordinary) < ECON_N:
        raise ValueError(f"普通对手局不足: {len(ordinary)} < {ECON_N}")
    return ordinary[:ECON_N]


# ---------------------------------------------------------------------------
# seated 回放流 runner（fn_work 通道 + 收入/畜群遥测）
# ---------------------------------------------------------------------------
def _count_sheep(farm) -> int:
    n = 0
    for row in farm.get("tiles") or []:
        for t in row:
            if isinstance(t, dict) and t.get("animal") == "SHEEP":
                n += 1
    return n


def _income_curve(money_series, n_days=30) -> list:
    """G2b income_selfcheck 同口径：日内步级正增量求和（SELL 侧毛收入）。"""
    inc = []
    for d in range(n_days):
        lo, hi = d * 24, min(d * 24 + 24, len(money_series) - 1)
        inc.append(round(sum(max(0.0, money_series[i + 1] - money_series[i])
                             for i in range(lo, hi)), 1))
    return inc


def _instrument(agent_fn, me_seat, tracker):
    """包装决策 callable：记录我席资金序列与日末羊数。"""
    def wrapped(obs):
        o = gc.structify_obs(obs)
        farm = o.farms[me_seat]
        tracker["money"].append(float(farm["money"]))
        step = o.get("step")
        if isinstance(step, (int, float)) and int(step) % 24 == 23:
            tracker["sheep_eod"].append(
                {"day": int(step) // 24, "sheep": _count_sheep(farm)})
        return agent_fn(o)
    wrapped.__name__ = getattr(agent_fn, "__name__", "agent")
    return wrapped


def seated_rollout(replay_path, me_seat, agent_loader, track=False) -> dict:
    """全季（注入点 0）seated 回放流 rollout。

    agent_loader=零参装载器（每局全新装载，官方每席装载语义）；track=True
    时记录资金序列/收入曲线/日末羊数。返回 {finals, margin, steps,
    income?, peak_d14_17?, peak_day?, sheep_eod?, stream_sha256}。
    """
    import rollout_with_replay_opponent as rro
    with open(replay_path, encoding="utf-8") as h:
        replay = json.load(h)
    deps = rro.make_twin_deps()
    start = 0
    state = deps["build"](replay, start)
    opp_actions = deps["transition_actions"](replay)
    me = int(me_seat)
    agent = agent_loader()
    tracker = {"money": [], "sheep_eod": []}
    stream = []
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    fn = _instrument(agent, me, tracker)   # 遥测恒开（开销可忽略）
    while (not state.env.done and start + taken < len(opp_actions)
           and taken < max_steps):
        obs = state.seats[me].observation
        mine = fn(obs)
        pair = [opp_actions[start + taken][1 - me]] * 2
        pair[me] = mine
        deps["step"](state, pair)
        stream.append(mine)
        taken += 1
    finals = deps["final"](state)
    out = {"finals": [round(float(x), 1) for x in finals],
           "margin": round(float(finals[me]) - float(finals[1 - me]), 1),
           "steps": taken,
           "stream_sha256": gc.sha256_bytes(
               "\n".join(gc.norm_action(a) for a in stream).encode("utf-8"))}
    if track:
        series = tracker["money"] + [float(finals[me])]
        inc = _income_curve(series)
        out["income_curve"] = inc
        lo, hi = ECON_WINDOW
        peak = max(inc[lo:hi]) if len(inc) >= hi else None
        out["peak_d14_17"] = peak
        out["peak_day"] = lo + inc[lo:hi].index(peak) if peak is not None \
            else None
        out["season_peak"] = max(inc)
        out["season_peak_day"] = inc.index(max(inc))
        out["sheep_eod"] = tracker["sheep_eod"]
    return out


def _v6b_loader():
    return lambda: gc.load_agent(V6B_MAIN)


def _v48_loader():
    return lambda: gc.load_agent(gc.BASE_MAIN)


# ---------------------------------------------------------------------------
# 线一：h2h vs 纯 v48（官方真引擎，seated AB/BA）
# ---------------------------------------------------------------------------
def _play_h2h_series(v6b_path, v48_path, seeds, seats=(0, 1)) -> list:
    games = []
    for seed in seeds:
        for seat in seats:
            t0 = time.perf_counter()
            pair = [gc.load_agent(v48_path), gc.load_agent(v48_path)]
            pair[seat] = gc.load_agent(v6b_path)      # v6b 显式落 seat 席
            rec = gc.run_engine_game(pair[0], pair[1], seed)
            me_money, opp_money = rec["rewards"][seat], rec["rewards"][1 - seat]
            margin = me_money - opp_money
            result = "WIN" if margin > 0 else (
                "TIE" if margin == 0 else "LOSS")
            games.append({
                "seed": seed, "me_seat": seat,
                "me_money": round(me_money, 1),
                "opp_money": round(opp_money, 1),
                "margin": round(margin, 1), "result": result,
                "statuses": rec["statuses"],
                "turns": rec["turns_played"],
                "anomaly_kinds": rec["anomaly_kinds"],
                "wall_s": round(time.perf_counter() - t0, 1),
            })
            print(f"  [v6b vs v48] seed={seed} seat={seat} "
                  f"me={games[-1]['me_money']:9.1f} "
                  f"opp={games[-1]['opp_money']:9.1f} "
                  f"margin={games[-1]['margin']:+10.1f} {result:4s} "
                  f"[{games[-1]['wall_s']}s]", flush=True)
    return games


def run_h2h_v48_gate(v6b_main=None, seeds=H2H_SEEDS) -> dict:
    """线一：v6b vs 纯 v48 ≥16 局（8 种子 AB/BA）互胜（严格胜比例）≥0.65。"""
    print("== 线一 run_h2h_v48_gate（官方引擎，8 种子 AB/BA）==", flush=True)
    t0 = time.perf_counter()
    v6b_main = v6b_main or V6B_MAIN
    base_sha = gc.sha256_file(gc.BASE_MAIN)
    if base_sha != gc.BASE_SHA256:
        raise ValueError(f"基线 v48 sha 漂移: {base_sha}")
    games = _play_h2h_series(v6b_main, gc.BASE_MAIN, seeds)
    n = len(games)
    w = sum(1 for g in games if g["result"] == "WIN")
    t = sum(1 for g in games if g["result"] == "TIE")
    l = sum(1 for g in games if g["result"] == "LOSS")
    frac = round(w / n, 4) if n else None
    by_seat = {}
    for seat in (0, 1):
        sub = [g for g in games if g["me_seat"] == seat]
        by_seat[str(seat)] = {
            "games": len(sub),
            "wins": sum(1 for g in sub if g["result"] == "WIN"),
            "losses": sum(1 for g in sub if g["result"] == "LOSS"),
            "ties": sum(1 for g in sub if g["result"] == "TIE")}
    margins = [g["margin"] for g in games]
    passed = bool(frac is not None and frac >= H2H_WIN_MIN
                  and n >= H2H_GAMES_MIN)
    return {
        "protocol": "structure-h2h-v48-gate/1.0",
        "criterion": f"vs pure_v48 严格互胜 wins/n >= {H2H_WIN_MIN}；"
                     f"局数 >= {H2H_GAMES_MIN}（8 种子 AB/BA）",
        "baseline_pure_v48": {"path": gc.BASE_MAIN, "sha256": base_sha},
        "games": n, "wins": w, "losses": l, "ties": t,
        "win_fraction_strict": frac,
        "win_rate_half_ties": round((w + 0.5 * t) / n, 4) if n else None,
        "avg_margin": round(sum(margins) / max(1, n), 1),
        "margin_distribution": {
            "pos": sum(1 for m in margins if m > 0),
            "neg": sum(1 for m in margins if m < 0),
            "zero": sum(1 for m in margins if m == 0)},
        "by_seat": by_seat,
        "all_done": all(g["statuses"] == ["DONE", "DONE"] for g in games),
        "anomaly_kinds_seen": sorted({k for g in games
                                      for k in g["anomaly_kinds"]}),
        "records": games,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 线二：巨人局 seated 对照
# ---------------------------------------------------------------------------
def run_giant_seated_gate(games=None, v6b_loader=None) -> dict:
    """线二：v6b 全季注入 vs statma/fuxi/42 回放流各 ≥3 局打平或更好
    （margin≥0 或差距≤1k=margin≥-1000）。"""
    print("== 线二 run_giant_seated_gate（seated 回放流，注入点=0）==",
          flush=True)
    t0 = time.perf_counter()
    games = scan_corpus() if games is None else games
    by_name = select_giant_games(games)
    loader = v6b_loader or _v6b_loader()
    per_name = {}
    for name, picks in by_name.items():
        print(f"-- 巨人 {name}: {[g['ep'] for g in picks]}", flush=True)
        rows = []
        for g in picks:
            run = seated_rollout(g["replay_path"], g["me_seat"], loader)
            ok = run["margin"] >= GIANT_OK_MARGIN
            rows.append({
                "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
                "role": ("anchor" if g["ep"] in {
                    ep for _, ep, _ in GIANT_ANCHORS}
                    else "other" if g["opp"] == name else "strong_ext"),
                "orig_margin": round(g["margin"], 1),
                "v6b_margin": run["margin"],
                "v6b_finals": run["finals"],
                "delta_vs_orig": round(run["margin"] - g["margin"], 1),
                "steps": run["steps"],
                "ok": ok})
            print(f"  ep{g['ep']} ({rows[-1]['role']}) orig="
                  f"{g['margin']:+10.1f} v6b={run['margin']:+10.1f} "
                  f"Δ={rows[-1]['delta_vs_orig']:+11.1f} "
                  f"ok={ok}", flush=True)
        per_name[name] = {
            "games": len(rows),
            "all_ok": all(r["ok"] for r in rows),
            "best_margin": max(r["v6b_margin"] for r in rows),
            "records": rows}
    all_ok = all(v["games"] >= GIANT_PER_NAME_MIN and v["all_ok"]
                 for v in per_name.values())
    return {
        "protocol": "structure-giant-seated-gate/1.0",
        "criterion": (f"对 statma/fuxi/42 回放流各 ≥{GIANT_PER_NAME_MIN} 局，"
                      f"逐局打平或更好（margin≥0，宽限 margin≥"
                      f"{GIANT_OK_MARGIN:.0f}）"),
        "corpus_rule": ("三巨人各自其他对局优先（本语料均无）→ 锚局本身 + "
                        f"r26full 强对手扩展集（败局 margin≤"
                        f"{STRONG_EXT_MARGIN_LE:.0f}，按严重度轮转每巨人 "
                        f"{STRONG_EXT_PER_GIANT} 局）"),
        "per_giant": per_name,
        "passed": all_ok,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 线三：胜局回归（双臂对照）
# ---------------------------------------------------------------------------
def run_win_regression_gate(games=None, v6b_loader=None,
                            v48_loader=None) -> dict:
    """线三：胜局回归 ≥8 局双臂对照；v6b 臂不翻负=margin(v6b)≥margin(v48)−1k。"""
    print("== 线三 run_win_regression_gate（seated 双臂：v6b vs 纯 v48）==",
          flush=True)
    t0 = time.perf_counter()
    games = scan_corpus() if games is None else games
    picks = select_regression_games(games)
    v6 = v6b_loader or _v6b_loader()
    v48 = v48_loader or _v48_loader()
    per_game = []
    for g in picks:
        run_v6 = seated_rollout(g["replay_path"], g["me_seat"], v6)
        run_48 = seated_rollout(g["replay_path"], g["me_seat"], v48)
        delta = run_v6["margin"] - run_48["margin"]
        ok = run_v6["margin"] >= run_48["margin"] - REG_TOLERANCE
        flipped_negative = (run_48["margin"] > 0
                            and run_v6["margin"] < 0)
        per_game.append({
            "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
            "orig_margin": round(g["margin"], 1),
            "margin_v48_arm": run_48["margin"],
            "margin_v6b_arm": run_v6["margin"],
            "delta": round(delta, 1), "ok": ok,
            "flipped_negative": bool(flipped_negative),
            "v6b_finals": run_v6["finals"],
            "v48_finals": run_48["finals"]})
        print(f"  ep{g['ep']} orig={g['margin']:+8.1f} "
              f"v48臂={run_48['margin']:+10.1f} "
              f"v6b臂={run_v6['margin']:+10.1f} Δ={delta:+11.1f} "
              f"ok={ok}", flush=True)
    n = len(per_game)
    n_ok = sum(1 for r in per_game if r["ok"])
    passed = bool(n >= REG_N and n_ok == n)
    return {
        "protocol": "structure-win-regression-gate/1.0",
        "criterion": (f"胜局回归 ≥{REG_N} 局（原 margin 最窄选取），逐局 "
                      f"margin(v6b) >= margin(v48) − {REG_TOLERANCE:.0f}"),
        "selection_rule": "r26full+r27full 我方 W 局按原 margin 升序取最窄 8 局",
        "games": n, "n_ok": n_ok,
        "flipped_negative_games": [r["ep"] for r in per_game
                                   if r["flipped_negative"]],
        "per_game": per_game,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 线四：发射四门引用 + 装载复检
# ---------------------------------------------------------------------------
def run_fourgate_reference(v6b_main=None, v6b_tar=None) -> dict:
    """线四：G2b 四门已 PASS 的引用复检——包身份 sha 与登记一致、冒烟产物
    一致性交叉、官方装载语义 callable 复检装载一次并一步应答。"""
    print("== 线四 run_fourgate_reference（G2b 引用 + 装载复检一次）==",
          flush=True)
    t0 = time.perf_counter()
    v6b_main = v6b_main or V6B_MAIN
    v6b_tar = v6b_tar or V6B_TAR
    main_sha, tar_sha = _v6b_sha_expected()
    cur_main = gc.sha256_file(v6b_main)
    cur_tar = gc.sha256_file(v6b_tar)
    identity_ok = (cur_main == main_sha and cur_tar == tar_sha
                   and gc.sha256_file(gc.BASE_MAIN) == gc.BASE_SHA256)

    smoke = None
    smoke_consistent = None
    if os.path.isfile(G2B_SMOKE):
        with open(G2B_SMOKE, encoding="utf-8") as h:
            smoke = json.load(h)
        pkg = smoke.get("package") or {}
        smoke_consistent = bool(
            smoke.get("all_gates_pass")
            and pkg.get("main_sha256") == cur_main
            and pkg.get("tar_sha256") == cur_tar)

    # 装载复检一次：官方装载语义 + 一步应答冒烟（不整局）
    load_ok, answer_ok, answer_shape = False, False, None
    try:
        agent = gc.load_agent(v6b_main)
        load_ok = True
        head = gc.synthetic_season_head(101)
        obs0 = gc.ObsStruct(head["steps"][0][0]["observation"])
        act = agent(obs0)
        answer_shape = type(act).__name__
        answer_ok = isinstance(act, dict)
    except Exception as e:                          # noqa: BLE001
        answer_shape = f"{type(e).__name__}: {e}"

    manifest_gate = None
    mpath = os.path.join(V6B_DIR, "build_manifest.json")
    with open(mpath, encoding="utf-8") as h:
        manifest_gate = ((json.load(h).get("gate_results") or {})
                         .get("launch_fourgate") or {})
    g2b_recorded_pass = bool(manifest_gate.get("passed"))

    passed = bool(identity_ok and smoke_consistent is not False
                  and g2b_recorded_pass and load_ok and answer_ok)
    return {
        "protocol": "structure-fourgate-reference/1.0",
        "criterion": ("G2b 四门 PASS 引用有效（build_manifest+冒烟产物一致）"
                      "+ 包身份 sha 一致 + 装载复检一次应答"),
        "identity": {"v6b_main_sha256": cur_main,
                     "v6b_main_sha_expected": main_sha,
                     "v6b_tar_sha256": cur_tar,
                     "v6b_tar_sha_expected": tar_sha,
                     "identity_ok": identity_ok},
        "g2b_smoke_artifact": {"path": G2B_SMOKE,
                               "exists": os.path.isfile(G2B_SMOKE),
                               "all_gates_pass":
                                   (smoke or {}).get("all_gates_pass"),
                               "consistent": smoke_consistent},
        "build_manifest_launch_fourgate": {
            "passed": g2b_recorded_pass,
            "artifact": manifest_gate.get("artifact"),
            "note": manifest_gate.get("note")},
        "load_recheck": {"load_ok": load_ok, "answer_ok": answer_ok,
                         "answer_type": answer_shape},
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 线五：经济面（seated 口径收入峰）
# ---------------------------------------------------------------------------
def run_economic_face(games=None, v6b_loader=None) -> dict:
    """线五：seated 口径经济面——v6b 全季注入对普通对手回放流 ≥6 局，
    日收入峰 ≥12.7k 且落 d14-17（income_selfcheck 同口径）。"""
    print("== 线五 run_economic_face（seated 普通对手回放流收入峰）==",
          flush=True)
    t0 = time.perf_counter()
    games = scan_corpus() if games is None else games
    picks = select_economic_games(games)
    loader = v6b_loader or _v6b_loader()
    per_game = []
    for g in picks:
        run = seated_rollout(g["replay_path"], g["me_seat"], loader,
                             track=True)
        peak = run["peak_d14_17"]
        ok = bool(peak is not None and peak >= ECON_GATE)
        per_game.append({
            "ep": g["ep"], "opp": g["opp"], "me_seat": g["me_seat"],
            "orig_margin": round(g["margin"], 1),
            "v6b_margin": run["margin"],
            "peak_d14_17": peak, "peak_day": run["peak_day"],
            "season_peak": run["season_peak"],
            "season_peak_day": run["season_peak_day"],
            "final_money": run["finals"][g["me_seat"]],
            "sheep_peak": max((e["sheep"] for e in run["sheep_eod"]),
                              default=None),
            "ok": ok})
        print(f"  ep{g['ep']} peak_d14_17={peak:8.1f}@d{run['peak_day']} "
              f"season_peak={run['season_peak']:8.1f}@d"
              f"{run['season_peak_day']} final="
              f"{run['finals'][g['me_seat']]:9.1f} ok={ok}", flush=True)
    n = len(per_game)
    best_peak = max((r["peak_d14_17"] or 0.0) for r in per_game) if n else 0.0
    passed = bool(n >= ECON_N and best_peak >= ECON_GATE)
    return {
        "protocol": "structure-economic-face/1.0",
        "criterion": (f"≥{ECON_N} 局 seated 普通对手回放流，收入峰 "
                      f"（日 SELL 毛收入，G2b 同口径）≥{ECON_GATE:.0f} 且落 "
                      f"d{ECON_WINDOW[0]}-d{ECON_WINDOW[1] - 1}"),
        "selection_rule": ("普通对手局（剔除巨人/强扩展/镜像/回归集）按 ep "
                           "升序取 6 局"),
        "measurement": ("资金序列=我席决策步 obs.farms[me].money+终局；日收入"
                        "=日内步级正增量求和；峰=max(d14..d17)"),
        "games": n, "best_peak_d14_17": round(best_peak, 1),
        "all_season_peaks_in_window": all(
            r["season_peak_day"] is not None
            and ECON_WINDOW[0] <= r["season_peak_day"] < ECON_WINDOW[1]
            for r in per_game),
        "per_game": per_game,
        "passed": passed,
        "wall_s": round(time.perf_counter() - t0, 1),
    }


# ---------------------------------------------------------------------------
# 编排裁决
# ---------------------------------------------------------------------------
def _gate_pass(result) -> bool:
    return bool(isinstance(result, dict) and result.get("passed") is True)


def _assemble_verdict(results, runnable, errors, identity, wall_s) -> dict:
    lines = {}
    for key, title in (("h2h", "h2h_v48_gate"), ("giants", "giant_seated"),
                       ("regression", "win_regression"),
                       ("econ", "economic_face"),
                       ("fourgate", "fourgate_reference")):
        r = results.get(key)
        lines[key] = {
            "title": title,
            "runnable": runnable[key],
            "error": errors.get(key),
            "passed": bool(runnable[key] and _gate_pass(r)),
            "summary": _line_summary(key, r) if runnable[key] else None}
    overall = "PASS" if all(v["passed"] for v in lines.values()) else "FAIL"
    return {
        "protocol": "structure-verdict/1.0",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "under_test": identity,
        "yarn2_note": ("G3 五线无构造 yarn2 局（全 seated 回放流+固定种子域"
                       " h2h），G2b 逐构建重扫义务不适用"),
        "lines": lines,
        "overall": overall,
        "wall_s": round(wall_s, 1),
    }


def _line_summary(key, r):
    if not isinstance(r, dict):
        return None
    if key == "h2h":
        return {"games": r["games"], "wins": r["wins"],
                "losses": r["losses"], "ties": r["ties"],
                "win_fraction_strict": r["win_fraction_strict"],
                "avg_margin": r["avg_margin"],
                "margin_distribution": r["margin_distribution"]}
    if key == "giants":
        return {name: {"games": v["games"], "all_ok": v["all_ok"],
                       "best_margin": v["best_margin"]}
                for name, v in r["per_giant"].items()}
    if key == "regression":
        return {"games": r["games"], "n_ok": r["n_ok"],
                "flipped_negative_games": r["flipped_negative_games"]}
    if key == "econ":
        return {"games": r["games"],
                "best_peak_d14_17": r["best_peak_d14_17"]}
    if key == "fourgate":
        return {"identity_ok": r["identity"]["identity_ok"],
                "g2b_smoke_consistent":
                    r["g2b_smoke_artifact"]["consistent"],
                "load_recheck": r["load_recheck"]}
    return None


def verify_structure_gates(lines=None) -> dict:
    """五线编排裁决（fail-closed：任一线不可执行=整体 FAIL，错误入 dict）。"""
    t0 = time.perf_counter()
    main_sha, tar_sha = _v6b_sha_expected()
    identity = {
        "v6b_package": V6B_DIR,
        "main_sha256": gc.sha256_file(V6B_MAIN),
        "tar_sha256": gc.sha256_file(V6B_TAR),
        "tar_sha_expected": tar_sha,
        "baseline_pure_v48_sha256": gc.sha256_file(gc.BASE_MAIN),
        "channel_validity_anchor": ("纯 v48 注入 r26full ep111653327/"
                                    "111302976/111324195 复现原局 rewards "
                                    "±13 内（G3 实施前金标准实测）"),
    }
    corpus = None
    try:
        corpus = scan_corpus()
    except Exception as e:                          # noqa: BLE001
        corpus = None
        print(f"[warn] 语料扫描失败（seated 三线将 fail-closed）: {e}",
              flush=True)

    def _g():
        return corpus if corpus is not None else scan_corpus()

    specs = (
        ("h2h", lambda: run_h2h_v48_gate()),
        ("giants", lambda: run_giant_seated_gate(_g())),
        ("regression", lambda: run_win_regression_gate(_g())),
        ("econ", lambda: run_economic_face(_g())),
        ("fourgate", lambda: run_fourgate_reference()),
    )
    if lines:
        specs = tuple(s for s in specs if s[0] in lines)
    results, runnable, errors = {}, {}, {}
    for name, fn in specs:
        try:
            results[name] = fn()
            runnable[name] = True
        except Exception as e:                      # fail-closed：不抛
            results[name] = None
            errors[name] = f"{type(e).__name__}: {e}"
            runnable[name] = False
            print(f"[fail-closed] 线 {name}: {errors[name]}", flush=True)
    verdict = _assemble_verdict(results, runnable, errors, identity,
                                time.perf_counter() - t0)
    for key, res in results.items():
        if res is not None:
            gc.write_json(LINE_OUT[key], res)
    gc.write_json(VERDICT_PATH, verdict)
    verdict["_out_path"] = VERDICT_PATH
    return verdict


def _cli() -> int:
    ap = argparse.ArgumentParser(description="R9-G3 结构五线终审")
    ap.add_argument("--line", action="append",
                    choices=("h2h", "giants", "regression", "econ",
                             "fourgate"),
                    help="只跑指定线（可多次；默认全五线）")
    args = ap.parse_args()
    verdict = verify_structure_gates(lines=args.line or None)
    slim = {"overall": verdict["overall"],
            "under_test": {k: verdict["under_test"][k]
                           for k in ("main_sha256", "tar_sha256")},
            "lines": {}}
    for key, v in verdict["lines"].items():
        slim["lines"][key] = {k: v[k] for k in ("runnable", "error",
                                                "passed", "summary")}
    print(json.dumps(slim, ensure_ascii=False, indent=1))
    return 0 if verdict["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(_cli())
