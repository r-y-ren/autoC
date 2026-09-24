# -*- coding: utf-8 -*-
"""phase_v（R17 L1/L2）：Phase V 三件离线判决（羊链路/番茄门扫描/V93 路由表）。

责任契约（fn_docs/hybrid/responsibility.md【R17 增补】）：
- phase_v_adjudicate()：三件判决编排与汇总（每件 verdict+evidence JSON）；
  单件失败不阻断其余，记录 errors。
- probe_sheep_fertilizer_loop()：≥3 个高羊败局（opp SHEEP≥11）解剖
  羊→COLLECT_FERTILIZER→FERTILIZE 麦→麦产→FEED 链路（回放动作流计数+
  资金归因），闭环成立 → adopt 羊 6→8。
- scan_tomato_gate()：42 点粗网格（CROP_MIN_PRICE {50..110}×money 门
  {7000..18000}）twin 重演判决（语料=12 败局+6 胜局抽样 rng 20260925r17；
  每点 Δ=variant−r34a 同局同席）→ top-3 邻域（±5/±1000）细化；胜出=
  Δ 中位>0 且胜局不翻负；全负→保持 70/12000 不并入。
- expand_route_table()：86 局 step2 指纹→结局统计填密 _V93_ROUTE_BY_RIVAL
  （只加表项）→ 26 败局重演不翻负 → adopt。

回放口径（法证锚定，见 evidence.method_notes）：kaggle 回放 steps[t] 的
observation 为 step t 转移后的状态（obs.step==t）；故动作 a_t 的执行 tile
取 steps[t-1] 的 observation（=agent 决策所见、动作落点同格）。
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import statistics
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                # kaggle_simulations/
SOFTWARE = os.path.dirname(KSIM)                            # legacy_software/
CAMPAIGN = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(SOFTWARE))))                            # 战役根
R34A_DIR = os.path.join(KSIM, "orderbook_2965_adopt", "a")
R34A_MAIN = os.path.join(R34A_DIR, "main.py")
EVIDENCE_DIR = os.path.join(HERE, "evidence")

REPLAY_DIR = "/tmp/r33audit"                                # 86 局回放缓存
AUDIT_ROWS_CANDIDATES = (
    "/tmp/kagr_root/audit_rows.json",
    "/tmp/r33audit/audit_rows.json",
)
TEAM_NAME = "renyxin"

# 抽样种子（需求原文 rng 20260925r17 —— 材料串非整数，沿 R14 corpus 先例
# 推导：int(sha256(material).hexdigest()[:16], 16)）。
TOMATO_SEED_MATERIAL = "20260925r17"

# 番茄门粗网格（用户扩域 2026-09-25：六点→42 点）。
TOMATO_PRICE_GRID = (50, 60, 70, 80, 90, 100, 110)
TOMATO_MONEY_GRID = (7000, 9000, 11000, 13000, 15000, 18000)
TOMATO_BASELINE = (70, 12000)          # r34a 在值（=对照臂）
TOP_K_REFINE = 3
NEIGHBOR_PRICE_STEP = 5
NEIGHBOR_MONEY_STEP = 1000

# 早崩三局（R15 排除先例，败局池=29−3=26）。
EARLY_COLLAPSE = (112844424, 112846785, 112847952)

# 羊链路闭环判据（operationalization；qualitative 判词见 requirements R17 改2）。
SHEEP_MIN_LOSSES = 3
SHEEP_MIN_SHEEP = 11
SHEEP_FERT_COLLECTED_MIN = 20        # 肥料工厂下限：季内收集 ≥20 单位
SHEEP_WHEAT_FERT_MIN = 10            # FERTILIZE 落麦 ≥10 次
SHEEP_FERT_YIELD_LIFT = 0.5          # 施肥麦均产 − 未施麦均产 ≥0.5 单位
SHEEP_FEED_COST_CAP_RATIO = 0.25     # 麦购支出 ≤ 0.25×(羊毛+肥料收入)

# 路由表证据判据。
ROUTE_MIN_SAMPLES = 2                # 候选指纹最少样本局
ROUTE_MAX_ENTRIES = 5                # 填密上限（只加表项，保守）
ROUTE_DELTA_TOL = -0.5               # 重演不翻负容差（浮点；Δ ≥ tol 视为不翻负）

_WHEAT_FEED_CROPS = ("WHEAT",)


class PhaseVError(RuntimeError):
    """Phase V fail-closed：语料缺失/结构畸形即抛。"""


# ---------------------------------------------------------------------------
# 共用小件
# ---------------------------------------------------------------------------
def _sha_seed(material: str) -> int:
    return int(hashlib.sha256(material.encode("utf-8")).hexdigest()[:16], 16)


def _write_json(path: str, payload: Any) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def _load_audit_games() -> List[Dict[str, Any]]:
    for cand in AUDIT_ROWS_CANDIDATES:
        if os.path.isfile(cand):
            with open(cand, "r", encoding="utf-8") as fh:
                games = json.load(fh).get("games")
            if isinstance(games, list) and games:
                return games
    raise PhaseVError(f"audit_rows.json 缺失（尝试 {AUDIT_ROWS_CANDIDATES}）")


def _replay_path(replay_dir: str, episode: int) -> str:
    path = os.path.join(replay_dir, f"episode-{int(episode)}-replay.json")
    if not os.path.isfile(path):
        raise PhaseVError(f"回放缺失：{path}")
    return path


def _load_replay(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _seats_of(replay: Dict[str, Any]) -> Tuple[int, int]:
    names = (replay.get("info") or {}).get("TeamNames") or []
    if TEAM_NAME not in names:
        raise PhaseVError(f"renyxin 不在 TeamNames：{names!r}")
    me = names.index(TEAM_NAME)
    return me, 1 - me


def _games_by_episode(games: Sequence[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    return {int(g["episode"]): g for g in games}


# ---------------------------------------------------------------------------
# twin seated 重演（默认驱动；测试可注入假驱动）
# ---------------------------------------------------------------------------
_TWIN_REPLAY = None


def _seated_margin(replay: Dict[str, Any], agent_callable, seat: int) -> Dict[str, Any]:
    """surge lab replay_dual_seat 复用（只调用不改其源）。"""
    global _TWIN_REPLAY
    if _TWIN_REPLAY is None:
        if SOFTWARE not in __import__("sys").path:
            __import__("sys").path.insert(0, SOFTWARE)
        from orderbook_surge_lab import phase_b as _pb
        _TWIN_REPLAY = _pb.replay_dual_seat
    return _TWIN_REPLAY(replay, agent_callable, seat)


def _exec_namespace(text: str, tag: str) -> Dict[str, Any]:
    """内存 exec 装载（build_adopt._exec_last_callable 同款；不落 __pycache__）。"""
    import sys
    env: Dict[str, Any] = {"__name__": tag, "__file__": tag}
    sys.path.append(HERE)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        exec(compile(text, tag, "exec"), env)
    finally:
        sys.path.pop()
        sys.dont_write_bytecode = old
    return env


def _callable_from_text(text: str, tag: str):
    """官方 last-callable 语义的内存装载（namespace 末 callable）。"""
    env = _exec_namespace(text, tag)
    entries = [v for v in env.values()
               if callable(v) and not (getattr(v, "__name__", "").startswith("__")
                                       and getattr(v, "__name__", "").endswith("__"))]
    if not entries:
        raise PhaseVError(f"{tag} 装载后无 callable")
    return entries[-1]


# ---------------------------------------------------------------------------
# 回放动作/tile 解析（羊链路+路由指纹共用）
# ---------------------------------------------------------------------------
def _iter_actor_tiles(replay: Dict[str, Any], seat: int):
    """逐 (t, command, tile, farm) 产出 seat 的非移动指令与落点 tile。

    动作 a_t 的落点 tile 取 steps[t-1] 的 farm 观测（决策所见状态，见模块
    docstring 口径注）。yield (t, cmd, tile_or_None, farm)。
    """
    steps = replay.get("steps") or []
    for t in range(1, len(steps)):
        action = (steps[t][seat].get("action") or {}) if len(steps[t]) > seat else {}
        obs = steps[t - 1][0].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) <= seat:
            continue
        farm = farms[seat]
        tiles = farm.get("tiles") or []
        cmds = [action.get("farmer")] + list(action.get("hands") or [])
        poss = [farm.get("farmer")] + list(farm.get("hands") or [])
        for cmd, pos in zip(cmds, poss):
            if not cmd:
                continue
            tile = None
            if (isinstance(pos, (list, tuple)) and len(pos) == 2
                    and 0 <= int(pos[1]) < len(tiles)
                    and 0 <= int(pos[0]) < len(tiles[int(pos[1])])):
                tile = tiles[int(pos[1])][int(pos[0])]
            yield t, cmd, tile, farm


def _sheep_count_curve(replay: Dict[str, Any], seat: int) -> Dict[int, int]:
    """day → 该席在田 SHEEP 头数（取当日末观测）。"""
    curve: Dict[int, int] = {}
    steps = replay.get("steps") or []
    for t in range(0, len(steps)):
        obs = steps[t][0].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) <= seat:
            continue
        n = sum(1 for row in farms[seat].get("tiles") or []
                for tl in row
                if isinstance(tl, dict) and tl.get("animal") == "SHEEP")
        curve[t // 24] = n
    return curve


def _revenue_by_product(replay: Dict[str, Any], seat: int) -> Dict[str, float]:
    """该席 SELL 收入逐品（量×当步价，近似成交价=当步市场价，注记入 evidence）。"""
    rev: Dict[str, float] = {}
    steps = replay.get("steps") or []
    for t in range(1, len(steps)):
        action = (steps[t][seat].get("action") or {}) if len(steps[t]) > seat else {}
        obs = steps[t - 1][0].get("observation") or {}
        px = (obs.get("market") or {}).get("prices") or {}
        for order in action.get("market") or []:
            if order and order[0] == "SELL" and len(order) >= 3:
                try:
                    rev[order[1]] = rev.get(order[1], 0.0) + int(order[2]) * float(
                        px.get(order[1], 0) or 0)
                except (TypeError, ValueError):
                    continue
    return rev


# ---------------------------------------------------------------------------
# probe_sheep_fertilizer_loop（改2 前置判读）
# ---------------------------------------------------------------------------
def _dissect_one_sheep_game(replay: Dict[str, Any]) -> Dict[str, Any]:
    me, opp = _seats_of(replay)
    curve = _sheep_count_curve(replay, opp)
    metrics: Dict[str, Any] = {
        "episode": (replay.get("info") or {}).get("EpisodeId"),
        "opp_seat": opp,
        "peak_sheep": max(curve.values()) if curve else 0,
        "end_sheep": curve.get(max(curve), 0) if curve else 0,
        "collect_fertilizer_actions": 0,
        "fert_collected_units": 0,
        "fertilize_on_wheat": 0,
        "fertilize_on_other_crops": 0,
        "wheat_harvest_events": 0,
        "wheat_harvest_units": 0,
        "wheat_harvest_fert_units": 0,
        "wheat_harvest_fert_events": 0,
        "wheat_harvest_unfert_units": 0,
        "wheat_harvest_unfert_events": 0,
        "feed_on_sheep": 0,
        "feed_on_cow": 0,
        "wheat_buy_units": 0,
        "wheat_buy_cost": 0.0,
    }
    steps = replay.get("steps") or []
    for t, cmd, tile, _farm in _iter_actor_tiles(replay, opp):
        head = cmd[0]
        if head == "COLLECT_FERTILIZER":
            metrics["collect_fertilizer_actions"] += 1
            if isinstance(tile, dict) and tile.get("fertilizer_available"):
                metrics["fert_collected_units"] += 1
        elif head == "FERTILIZE":
            if isinstance(tile, dict) and tile.get("crop") == "WHEAT":
                metrics["fertilize_on_wheat"] += 1
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                metrics["fertilize_on_other_crops"] += 1
        elif head == "FEED":
            animal = tile.get("animal") if isinstance(tile, dict) else None
            if animal == "SHEEP":
                metrics["feed_on_sheep"] += 1
            elif animal == "COW":
                metrics["feed_on_cow"] += 1
        elif head == "HARVEST" and isinstance(tile, dict) and tile.get("crop") == "WHEAT":
            units = int(tile.get("yield_units", 0) or 0)
            fertilized = int(tile.get("fertilized_until_day", -1) or -1) >= t // 24
            metrics["wheat_harvest_events"] += 1
            metrics["wheat_harvest_units"] += units
            if fertilized:
                metrics["wheat_harvest_fert_events"] += 1
                metrics["wheat_harvest_fert_units"] += units
            else:
                metrics["wheat_harvest_unfert_events"] += 1
                metrics["wheat_harvest_unfert_units"] += units
    for t in range(1, len(steps)):
        action = (steps[t][opp].get("action") or {}) if len(steps[t]) > opp else {}
        obs = steps[t - 1][0].get("observation") or {}
        px = (obs.get("market") or {}).get("prices") or {}
        for order in action.get("market") or []:
            if (order and order[0] == "BUY_PRODUCT" and len(order) >= 3
                    and order[1] == "WHEAT"):
                try:
                    qty = int(order[2])
                except (TypeError, ValueError):
                    continue
                metrics["wheat_buy_units"] += qty
                metrics["wheat_buy_cost"] += qty * (float(px.get("WHEAT", 0) or 0) + 10)
    rev = _revenue_by_product(replay, opp)
    metrics["revenue"] = {k: round(v, 1) for k, v in sorted(rev.items())}
    metrics["wool_fert_revenue"] = round(rev.get("WOOL", 0.0) + rev.get("FERTILIZER", 0.0), 1)
    fm, um = metrics["wheat_harvest_fert_events"], metrics["wheat_harvest_unfert_events"]
    metrics["fert_wheat_mean_yield"] = (metrics["wheat_harvest_fert_units"] / fm) if fm else None
    metrics["unfert_wheat_mean_yield"] = (metrics["wheat_harvest_unfert_units"] / um) if um else None
    lift = None
    if metrics["fert_wheat_mean_yield"] is not None and metrics["unfert_wheat_mean_yield"] is not None:
        lift = round(metrics["fert_wheat_mean_yield"] - metrics["unfert_wheat_mean_yield"], 3)
    metrics["fert_yield_lift"] = lift
    criteria = {
        "fert_factory": metrics["fert_collected_units"] >= SHEEP_FERT_COLLECTED_MIN,
        "fert_to_wheat": metrics["fertilize_on_wheat"] >= SHEEP_WHEAT_FERT_MIN,
        "yield_lift": (lift is not None and lift >= SHEEP_FERT_YIELD_LIFT),
        "feed_economics": (metrics["wool_fert_revenue"] > 0
                           and metrics["wheat_buy_cost"]
                           <= SHEEP_FEED_COST_CAP_RATIO * metrics["wool_fert_revenue"]),
    }
    metrics["criteria"] = criteria
    metrics["loop_closed"] = all(criteria.values())
    return metrics


def probe_sheep_fertilizer_loop(replay_paths: Optional[Sequence[str]] = None,
                                replay_dir: str = REPLAY_DIR,
                                write_evidence: bool = True) -> Dict[str, Any]:
    """≥3 高羊败局解剖 羊→COLLECT_FERTILIZER→FERTILIZE 麦→FEED 链路。

    语料=audit_rows 里 res=L 且 opp_animals_end.SHEEP≥11 的败局（≥3 才可判）；
    闭环判据（四臂全过）：肥料工厂量级+FERTILIZE 落麦+施肥麦均产抬升+
    麦购支出经济性。adopt=闭环局数 ≥3。
    """
    t0 = time.perf_counter()
    try:
        games = _games_by_episode(_load_audit_games())
    except PhaseVError:
        if replay_paths is None:
            raise
        games = {}                      # 注入语料测试面：audit 缺失不阻断
    rows = [g for g in games.values()
            if g.get("res") == "L"
            and int((g.get("opp_animals_end") or {}).get("SHEEP", 0) or 0) >= SHEEP_MIN_SHEEP]
    rows.sort(key=lambda g: int(g["episode"]))
    paths = list(replay_paths) if replay_paths is not None else [
        _replay_path(replay_dir, g["episode"]) for g in rows]
    if len(paths) < SHEEP_MIN_LOSSES:
        result = {"games": [], "n_games": len(paths), "adopt": False,
                  "reason": f"高羊败局不足 {SHEEP_MIN_LOSSETS if False else SHEEP_MIN_LOSSES}",
                  "thresholds": None}
        if write_evidence:
            result["evidence_path"] = _write_json(
                os.path.join(EVIDENCE_DIR, "phase_v_sheep.json"), result)
        return result
    dissected, errors = [], []
    for path in paths:
        try:
            replay = _load_replay(path)
            m = _dissect_one_sheep_game(replay)
            row = games.get(int(m["episode"])) or {}
            m["audit_margin"] = row.get("margin")
            m["opp_name"] = row.get("opp")
            dissected.append(m)
        except Exception as exc:                      # 单局失败不阻断（记 errors）
            errors.append({"path": path, "error": f"{type(exc).__name__}: {exc}"})
    n_closed = sum(1 for m in dissected if m["loop_closed"])
    adopt = bool(n_closed >= SHEEP_MIN_LOSSES and not errors)
    result = {
        "probe": "sheep_fertilizer_loop",
        "n_games": len(dissected),
        "n_loop_closed": n_closed,
        "adopt": adopt,
        "params": {"sheep_buy": 8} if adopt else None,
        "criteria_thresholds": {
            "fert_collected_units_min": SHEEP_FERT_COLLECTED_MIN,
            "wheat_fertilize_min": SHEEP_WHEAT_FERT_MIN,
            "fert_yield_lift_min": SHEEP_FERT_YIELD_LIFT,
            "wheat_buy_cost_cap_ratio": SHEEP_FEED_COST_CAP_RATIO,
            "min_closed_games": SHEEP_MIN_LOSSES,
            "min_opp_sheep": SHEEP_MIN_SHEEP,
        },
        "games": dissected,
        "errors": errors,
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "phase_v_sheep.json"), result)
    return result


# ---------------------------------------------------------------------------
# scan_tomato_gate（改3 番茄门扫描）
# ---------------------------------------------------------------------------
def _tomato_variant_text(r34a_text: str, price: int, money: int) -> str:
    """两行受控替换：CROP_MIN_PRICE 与 _v219_qualifies 资金门（各恰一处）。"""
    old_price_line = "CROP_MIN_PRICE=70"
    old_money_frag = "if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:"
    if r34a_text.count(old_price_line) != 1:
        raise PhaseVError(f"CROP_MIN_PRICE 行定位数 {r34a_text.count(old_price_line)}")
    if r34a_text.count(old_money_frag) != 1:
        raise PhaseVError(f"资金门行定位数 {r34a_text.count(old_money_frag)}")
    text = r34a_text.replace(old_price_line, f"CROP_MIN_PRICE={int(price)}")
    text = text.replace(old_money_frag,
                        "if farm['money'] < %d or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:" % int(money))
    return text


def _tomato_corpus(replay_dir: str) -> Dict[str, Any]:
    """12 败局+6 胜局抽样（rng 20260925r17；败局池=26 排早崩，胜局池=r32/r33）。"""
    games = _load_audit_games()
    losses26 = sorted(int(g["episode"]) for g in games
                      if g.get("res") == "L" and int(g["episode"]) not in EARLY_COLLAPSE)
    wins_pool = sorted(int(g["episode"]) for g in games
                       if g.get("res") == "W" and g.get("tag") in ("r32", "r33"))
    rng = random.Random(_sha_seed(TOMATO_SEED_MATERIAL))
    losses12 = sorted(rng.sample(losses26, 12))
    wins6 = sorted(rng.sample(wins_pool, 6)) if len(wins_pool) >= 6 else list(wins_pool)
    by_ep = _games_by_episode(games)
    corpus = [{"episode": ep, "seat": int(by_ep[ep]["seat"]),
               "res": by_ep[ep]["res"], "margin": by_ep[ep]["margin"]}
              for ep in losses12 + wins6]
    note = {
        "seed_material": TOMATO_SEED_MATERIAL,
        "seed_derivation": "int(sha256(material).hexdigest()[:16], 16)",
        "losses26_pool": losses26,
        "wins_pool": wins_pool,
    }
    return {"games": corpus, "sampling": note}


def _median(values: Sequence[float]) -> Optional[float]:
    vals = [float(v) for v in values if v is not None]
    return round(statistics.median(vals), 2) if vals else None


def scan_tomato_gate(corpus: Optional[Dict[str, Any]] = None,
                     r34a_main_path: str = R34A_MAIN,
                     replay_dir: str = REPLAY_DIR,
                     replay_driver=None,
                     write_evidence: bool = True) -> Dict[str, Any]:
    """42 点粗网格→top-3 邻域细化；胜出=Δ 中位>0+胜局不翻负。

    每点 Δ = margin(variant(p,m)) − margin(r34a) 同局同席（twin 重演，对手
    =录像开环重放）。corpus 给定 games 清单（测试注入），缺省现场抽样。
    replay_driver(replay, callable, seat)→{margin,status}（默认 _seated_margin）。
    """
    t0 = time.perf_counter()
    driver = replay_driver or _seated_margin
    if corpus is None:
        corpus = _tomato_corpus(replay_dir)
    entries = corpus["games"]
    if not entries:
        raise PhaseVError("番茄扫描语料为空（fail-closed）")
    replays = []
    for e in entries:
        path = e.get("path") or _replay_path(replay_dir, e["episode"])
        replays.append({"episode": e["episode"], "seat": int(e["seat"]),
                        "res": e.get("res"), "margin": e.get("margin"),
                        "replay": _load_replay(path)})
    with open(r34a_main_path, "r", encoding="utf-8") as fh:
        r34a_text = fh.read()
    r34a_callable = _callable_from_text(r34a_text, "r34a_baseline")
    baseline = []
    for g in replays:
        res = driver(g["replay"], r34a_callable, g["seat"])
        baseline.append({"episode": g["episode"], "res": g["res"],
                         "seat": g["seat"], "margin": res["margin"],
                         "status": res.get("status")})
    base_margin = {b["episode"]: float(b["margin"]) for b in baseline}

    def _probe_point(price: int, money: int) -> Dict[str, Any]:
        variant = _callable_from_text(
            _tomato_variant_text(r34a_text, price, money), f"tomato_p{price}_m{money}")
        per_game, win_flipped = [], []
        for g in replays:
            res = driver(g["replay"], variant, g["seat"])
            delta = round(float(res["margin"]) - base_margin[g["episode"]], 2)
            per_game.append({"episode": g["episode"], "res": g["res"],
                             "margin": res["margin"], "delta": delta,
                             "status": res.get("status")})
            if g["res"] == "W" and float(res["margin"]) <= 0:
                win_flipped.append(g["episode"])
        deltas = [p["delta"] for p in per_game]
        loss_deltas = [p["delta"] for p in per_game if p["res"] == "L"]
        return {"price": price, "money": money, "per_game": per_game,
                "delta_median": _median(deltas),
                "loss_delta_median": _median(loss_deltas),
                "delta_mean": round(sum(deltas) / len(deltas), 2) if deltas else None,
                "win_flips_negative": win_flipped}

    tested: Dict[Tuple[int, int], Dict[str, Any]] = {}
    grid_results = []
    for price in TOMATO_PRICE_GRID:
        for money in TOMATO_MONEY_GRID:
            point = _probe_point(price, money)
            tested[(price, money)] = point
            grid_results.append({k: point[k] for k in
                                 ("price", "money", "delta_median",
                                  "loss_delta_median", "delta_mean",
                                  "win_flips_negative")})

    def _rank_key(point: Dict[str, Any]):
        med = point["delta_median"]
        return (-(med if med is not None else float("-inf")),
                -(point["delta_mean"] or 0.0),
                point["money"], point["price"])

    top3 = sorted(grid_results, key=_rank_key)[:TOP_K_REFINE]
    refine_results = []
    seen = set(tested)
    for top in top3:
        p0, m0 = top["price"], top["money"]
        for dp, dm in ((-NEIGHBOR_PRICE_STEP, 0), (NEIGHBOR_PRICE_STEP, 0),
                       (0, -NEIGHBOR_MONEY_STEP), (0, NEIGHBOR_MONEY_STEP)):
            key = (p0 + dp, m0 + dm)
            if key in seen:
                continue
            seen.add(key)
            point = _probe_point(*key)
            tested[key] = point
            refine_results.append({"price": point["price"],
                                   "money": point["money"],
                                   "delta_median": point["delta_median"],
                                   "loss_delta_median": point["loss_delta_median"],
                                   "delta_mean": point["delta_mean"],
                                   "win_flips_negative": point["win_flips_negative"],
                                   "around": [p0, m0]})

    def _qualifies(point: Dict[str, Any]) -> bool:
        med = point["delta_median"]
        return (med is not None and med > 0 and not point["win_flips_negative"])

    candidates = [p for p in tested.values() if _qualifies(p)]
    best = None
    if candidates:
        best = min(candidates, key=lambda p: (-p["delta_median"],
                                              -p["delta_mean"], p["money"], p["price"]))
    adopt = best is not None
    result = {
        "probe": "tomato_gate_scan",
        "baseline_params": {"CROP_MIN_PRICE": TOMATO_BASELINE[0],
                            "money_gate": TOMATO_BASELINE[1]},
        "corpus": {"games": [{k: g[k] for k in ("episode", "seat", "res", "margin")}
                             for g in replays],
                   "sampling": corpus.get("sampling")},
        "baseline_replay": baseline,
        "grid": {"prices": list(TOMATO_PRICE_GRID), "monies": list(TOMATO_MONEY_GRID),
                 "n_points": len(grid_results), "results": grid_results},
        "refine": {"top3": [{k: t[k] for k in ("price", "money", "delta_median")}
                            for t in top3],
                   "n_points": len(refine_results), "results": refine_results},
        "best": ({"price": best["price"], "money": best["money"],
                  "delta_median": best["delta_median"],
                  "loss_delta_median": best["loss_delta_median"],
                  "win_flips_negative": best["win_flips_negative"]}
                 if best else None),
        "adopt": adopt,
        "params": ({"CROP_MIN_PRICE": best["price"], "money_gate": best["money"]}
                   if best else None),
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "phase_v_tomato.json"), result)
    return result


# ---------------------------------------------------------------------------
# expand_route_table（改4 V93 敌指纹路由表填密）
# ---------------------------------------------------------------------------
def _route_tables_from_main(main_path: str) -> Dict[str, Any]:
    """exec r34a 取路由表常量（_V92_TABLE/_V93_ROUTE_BY_RIVAL/新旧 shop 表）。"""
    with open(main_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    ns = _exec_namespace(text, "r34a_route_tables")
    tables = {}
    for name in ("_R108_SHOP_ROUTES", "_R110_OLD_SHOPS", "_V92_TABLE",
                 "_V93_ROUTE_BY_RIVAL"):
        if name not in ns:
            raise PhaseVError(f"r34a 缺路由表 {name}")
        tables[name] = dict(ns[name])
    return tables


def _game_fingerprint(replay: Dict[str, Any]) -> Dict[str, Any]:
    """step2 指纹（rkey）+ day6 前二 shop + 我席结局。"""
    me, opp = _seats_of(replay)
    steps = replay.get("steps") or []
    rkey, shops2 = None, None
    for t in range(0, min(4, len(steps))):
        obs = steps[t][0].get("observation") or {}
        if int(obs.get("step", -1)) == 2:
            farms = obs.get("farms") or []
            inv = ((obs.get("market") or {}).get("inventory") or {}).get("WHEAT")
            if len(farms) > opp and inv is not None:
                rkey = (round(float(farms[opp]["money"]), 3), int(inv))
                break
    for t in range(144, min(200, len(steps))):
        obs = steps[t][0].get("observation") or {}
        if int(obs.get("step", -1)) >= 144:
            shops = (obs.get("town") or {}).get("unlocked_shops") or []
            if shops:
                shops2 = tuple(shops[:2])
                break
    rewards = replay.get("rewards") or []
    margin = (float(rewards[me]) - float(rewards[opp])
              if len(rewards) == 2 and rewards[0] is not None
              and rewards[1] is not None else None)
    return {"episode": (replay.get("info") or {}).get("EpisodeId"),
            "rkey": rkey, "shops2": shops2, "margin": margin,
            "res": ("W" if margin > 0 else "L" if margin < 0 else "T") if margin is not None else None}


def _route_chosen(tables: Dict[str, Any], shops2: Optional[Tuple[str, ...]],
                  rkey: Optional[Tuple[float, int]]) -> Optional[int]:
    """复刻 _router 的 day6 路由决策（只读复算，不改基座）。"""
    if not shops2:
        return None
    use_new = shops2.count("YARN_STORE") <= 0
    route = tables["_R108_SHOP_ROUTES"].get(shops2, 100) if use_new \
        else tables["_R110_OLD_SHOPS"].get(shops2, 0)
    route = tables["_V92_TABLE"].get(shops2, route)
    if "YARN_STORE" in shops2 and rkey in tables["_V93_ROUTE_BY_RIVAL"]:
        route = tables["_V93_ROUTE_BY_RIVAL"][rkey]
    return int(route)


def expand_route_table(corpus: Optional[Dict[str, Any]] = None,
                       route_table: Optional[Dict[str, Any]] = None,
                       r34a_main_path: str = R34A_MAIN,
                       replay_dir: str = REPLAY_DIR,
                       replay_driver=None,
                       write_evidence: bool = True) -> Dict[str, Any]:
    """86 局指纹→结局统计填密 _V93_ROUTE_BY_RIVAL（只加表项）→26 败局重演
    不翻负→adopt。

    证据规则（预绑定）：对 YARN 世界（表生效面）出现的指纹 rkey——若全语料
    （任意世界）中该指纹在替代路由 R 上的样本（≥2 局）结局严格优于默认路由
    9 的样本（均 margin 更高且胜率不更低），填 rkey→R（上限 5 条）。验证：
    26 败局 twin 重演（r34a+扩表 vs r34a）逐局 Δ≥容差；回归条目剔除重验。
    """
    t0 = time.perf_counter()
    driver = replay_driver or _seated_margin
    tables = dict(route_table) if route_table is not None else \
        _route_tables_from_main(r34a_main_path)
    v93 = dict(tables["_V93_ROUTE_BY_RIVAL"])

    games = corpus.get("games") if corpus else None
    if games is None:
        games = _load_audit_games()
    fingerprints = []
    for g in games:
        ep = int(g["episode"])
        path = _replay_path(replay_dir, ep)
        fp = _game_fingerprint(_load_replay(path))
        fp["seat"] = int(g.get("seat", 0))
        fingerprints.append(fp)

    # 指纹→(route→[margins]) 统计（route 由表复算；YARN 世界默认 9）。
    stats: Dict[Tuple[float, int], Dict[int, List[float]]] = {}
    yarn_rkeys = set()
    for fp in fingerprints:
        if fp["rkey"] is None or fp["margin"] is None:
            continue
        route = _route_chosen(tables, fp["shops2"], fp["rkey"])
        if route is None:
            continue
        stats.setdefault(fp["rkey"], {}).setdefault(route, []).append(fp["margin"])
        if fp["shops2"] and "YARN_STORE" in fp["shops2"]:
            yarn_rkeys.add(fp["rkey"])

    default_route = 9                      # _V92_TABLE 全 YARN 项=9（法证锚）
    candidates = []
    for rkey in sorted(yarn_rkeys):
        if rkey in v93:
            continue                        # 已在表：不动（只加不改）
        base_margins = stats.get(rkey, {}).get(default_route, [])
        if len(base_margins) < ROUTE_MIN_SAMPLES:
            continue
        base_mean = sum(base_margins) / len(base_margins)
        base_wr = sum(1 for m in base_margins if m > 0) / len(base_margins)
        best_alt = None
        for route, margins in sorted(stats.get(rkey, {}).items()):
            if route == default_route or len(margins) < ROUTE_MIN_SAMPLES:
                continue
            alt_mean = sum(margins) / len(margins)
            alt_wr = sum(1 for m in margins if m > 0) / len(margins)
            if alt_mean > base_mean and alt_wr >= base_wr:
                key = (alt_mean - base_mean, alt_wr, -route)
                if best_alt is None or key > best_alt[0]:
                    best_alt = (key, route, alt_mean, alt_wr, len(margins))
        if best_alt is not None:
            candidates.append({
                "rkey": rkey, "route": best_alt[1],
                "default_mean": round(base_mean, 1),
                "default_win_rate": round(base_wr, 3),
                "alt_mean": round(best_alt[2], 1),
                "alt_win_rate": round(best_alt[3], 3),
                "n_default": len(base_margins), "n_alt": best_alt[4],
            })
    candidates.sort(key=lambda c: (-(c["alt_mean"] - c["default_mean"]),
                                   c["rkey"]))
    candidates = candidates[:ROUTE_MAX_ENTRIES]

    # 26 败局重演验证（不翻负）：r34a+扩表 vs r34a 基线。
    losses26 = sorted(int(g["episode"]) for g in _load_audit_games()
                      if g.get("res") == "L"
                      and int(g["episode"]) not in EARLY_COLLAPSE)
    with open(r34a_main_path, "r", encoding="utf-8") as fh:
        r34a_text = fh.read()
    r34a_callable = _callable_from_text(r34a_text, "r34a_route_baseline")
    replay_cache = {}
    for ep in losses26:
        replay_cache[ep] = _load_replay(_replay_path(replay_dir, ep))
    by_ep = _games_by_episode(_load_audit_games())
    base_margins_26 = {}
    for ep in losses26:
        res = driver(replay_cache[ep], r34a_callable, int(by_ep[ep]["seat"]))
        base_margins_26[ep] = float(res["margin"])

    fp_cache = {ep: _game_fingerprint(replay_cache[ep]) for ep in losses26}
    table_line_old = "_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128}"

    def _variant_callable(entries: List[Dict[str, Any]]):
        table = dict(v93)
        for c in entries:
            table[c["rkey"]] = c["route"]
        rendered = "_V93_ROUTE_BY_RIVAL = " + repr(
            {k: v for k, v in sorted(table.items())})
        if r34a_text.count(table_line_old) != 1:
            raise PhaseVError("V93 表行定位数 != 1")
        return _callable_from_text(r34a_text.replace(table_line_old, rendered),
                                   "r34a_route_variant")

    def _verify(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not entries:
            return {"per_game": [], "regressions": [], "all_ok": True}
        variant = _variant_callable(entries)
        per_game, regressions = [], []
        for ep in losses26:
            res = driver(replay_cache[ep], variant, int(by_ep[ep]["seat"]))
            delta = round(float(res["margin"]) - base_margins_26[ep], 2)
            per_game.append({"episode": ep, "margin": res["margin"],
                             "delta": delta})
            if delta < ROUTE_DELTA_TOL:
                regressions.append(ep)
        return {"per_game": per_game, "regressions": regressions,
                "all_ok": not regressions}

    adopted_entries = list(candidates)
    verify = _verify(adopted_entries)
    verify_rounds = [{"entries": [str(c["rkey"]) for c in adopted_entries],
                      "regressions": verify["regressions"],
                      "per_game": verify["per_game"]}]
    rounds = 0
    while verify["regressions"] and adopted_entries and rounds < ROUTE_MAX_ENTRIES + 1:
        rounds += 1
        bad = set(verify["regressions"])
        # 剔除在回归局上生效的条目（指纹命中该局的），保守整条剔除
        drop = [c for c in adopted_entries
                if any(fp_cache[ep]["rkey"] == c["rkey"] for ep in bad)]
        if not drop:
            adopted_entries = adopted_entries[:-1]        # 无法定位→逐条回退
        else:
            adopted_entries = [c for c in adopted_entries if c not in drop]
        verify = _verify(adopted_entries)
        verify_rounds.append({"entries": [str(c["rkey"]) for c in adopted_entries],
                              "regressions": verify["regressions"],
                              "per_game": verify["per_game"]})

    adopt = bool(adopted_entries) and verify["all_ok"]
    result = {
        "probe": "route_table_expansion",
        "existing_entries": {str(k): v for k, v in sorted(v93.items())},
        "fingerprint_stats": {str(k): {str(r): [round(m, 1) for m in ms]
                                       for r, ms in routes.items()}
                              for k, routes in sorted(stats.items())},
        "candidates": candidates,
        "adopted_entries": (adopted_entries if adopt else []),
        "n_new_entries": len(adopted_entries) if adopt else 0,
        "replay_verification": {"losses26": losses26,
                                "baseline_margins": base_margins_26,
                                "per_game": verify["per_game"],
                                "regressions": verify["regressions"],
                                "verify_rounds": verify_rounds},
        "adopt": adopt,
        "params": ({"_V93_ROUTE_BY_RIVAL": {str(c["rkey"]): c["route"]
                                            for c in adopted_entries}}
                   if adopt else None),
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "phase_v_route.json"), result)
    return result


# ---------------------------------------------------------------------------
# phase_v_adjudicate（编排）
# ---------------------------------------------------------------------------
def phase_v_adjudicate(corpus: Optional[Dict[str, Any]] = None,
                       r34a_main_path: str = R34A_MAIN) -> Dict[str, Any]:
    """三件判决编排汇总：{sheep,tomato,route:{adopt,params}}；单件失败不阻断。"""
    t0 = time.perf_counter()
    summary: Dict[str, Any] = {"phase": "V", "errors": []}
    for name, thunk in (
            ("sheep", lambda: probe_sheep_fertilizer_loop()),
            ("tomato", lambda: scan_tomato_gate(corpus, r34a_main_path)),
            ("route", lambda: expand_route_table(corpus, None, r34a_main_path))):
        try:
            res = thunk()
            summary[name] = {
                "adopt": bool(res.get("adopt")),
                "params": res.get("params"),
                "evidence_path": res.get("evidence_path"),
            }
        except Exception as exc:
            summary["errors"].append({name: f"{type(exc).__name__}: {exc}"})
            summary[name] = {"adopt": False, "params": None, "error": str(exc)}
    summary["wall_s"] = round(time.perf_counter() - t0, 1)
    summary["evidence_path"] = _write_json(
        os.path.join(EVIDENCE_DIR, "phase_v_summary.json"), summary)
    return summary
