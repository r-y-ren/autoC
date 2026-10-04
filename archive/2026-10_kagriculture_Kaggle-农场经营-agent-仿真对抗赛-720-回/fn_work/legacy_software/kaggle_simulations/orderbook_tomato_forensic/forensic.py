# -*- coding: utf-8 -*-
"""forensic（R18 L1）：Phase T 两件法证 + cxtb 条件判决实验。

责任契约（fn_docs/hybrid/responsibility.md【R18 增补】）：
- forensic_cxtb_trigger()：86 局回放统计 _CXTB 触发率（cxtb_calls/opened/
  blocked、触发步、触发局番茄订单轨迹）、触发 vs 未触发结局差；face_alive
  判定（我方谱系是否实际走该面）。
- scan_wheat_step91()：麦簇阈值五点 {25,28,31,34,38} twin 重演（语料 12 败局
  +6 胜局 rng 20260925r18）+触发率统计；胜出=子集 Δ 中位>0+胜局不翻负。
- adjudicate_cxtb_variants()：条件判决实验——阶梯化（80 拆 2-3 批逐批过
  边际线，变体文本=build_r36.stepped_block_text 单一真源）+ 9000/0.75/2.4
  常数 OAT 扫描；face_alive 才有意义（face 不活→跳过，返回 skipped）。

方法口径：沿 phase_v——twin seated 重演（对手=录像开环重放），装载=官方
last-callable 内存 exec（每局全新命名空间，遥测可读且无跨局污染）。
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
KSIM = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(KSIM)
if KSIM not in __import__("sys").path:
    __import__("sys").path.insert(0, KSIM)

from orderbook_r35 import phase_v as _pv               # noqa: E402
from orderbook_tomato_forensic import build_r36 as _b36  # noqa: E402

R34A_MAIN = os.path.join(KSIM, "orderbook_2965_adopt", "a", "main.py")
EVIDENCE_DIR = os.path.join(HERE, "evidence")
REPLAY_DIR = "/tmp/r33audit"

# 语料抽样（rng 20260925r18；材料串非整数沿 R14/R17 先例 sha256 推导）。
SEED_MATERIAL = "20260925r18"
CORPUS_N_LOSSES = 12
CORPUS_N_WINS = 6
EARLY_COLLAPSE = (112844424, 112846785, 112847952)     # R15 排除先例

# 麦簇五点（含基线 31）。
WHEAT_POINTS = (25, 28, 31, 34, 38)
WHEAT_BASELINE = 31

# cxtb 常数 OAT 扫描点（基线含于各轴）。
CXTB_MINREV_POINTS = (7000, 8000, 9000, 10000, 11000)
CXTB_THEIR_POINTS = (0.6, 0.75, 0.9)
CXTB_SLACK_POINTS = (2.0, 2.4, 2.8)
# 判决敏感带：|投影收入−9000| ≤ 该宽度（常数扫描次级语料面）。
CXTB_SENSITIVE_BAND = 2000.0

# 阶梯化判决变体（80 单位拆批）。
STEPPED_VARIANTS = ((5, 5), (4, 3, 3))
STEPPED_DENSITY = 9000.0 / 80.0

# face_alive 判定：净局中 _v219_qualifies 实际被调用的比例下限。
FACE_ALIVE_CALL_SHARE = 0.5


class ForensicError(RuntimeError):
    """Phase T fail-closed：语料缺失/结构畸形即抛。"""


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


def _median(values: Sequence[float]) -> Optional[float]:
    vals = [float(v) for v in values if v is not None]
    return round(statistics.median(vals), 2) if vals else None


def _load_r34a_text(r34a_main_path: str) -> str:
    with open(r34a_main_path, "r", encoding="utf-8") as fh:
        return fh.read()


def _r18_corpus(replay_dir: str = REPLAY_DIR) -> Dict[str, Any]:
    """12 败局+6 胜局抽样（rng 20260925r18；败局池沿 R17=26 排早崩，胜局池
    =r32/r33 tag）。"""
    games = _pv._load_audit_games()
    losses_pool = sorted(int(g["episode"]) for g in games
                         if g.get("res") == "L"
                         and int(g["episode"]) not in EARLY_COLLAPSE)
    wins_pool = sorted(int(g["episode"]) for g in games
                       if g.get("res") == "W" and g.get("tag") in ("r32", "r33"))
    if len(losses_pool) < CORPUS_N_LOSSES:
        raise ForensicError(f"败局池不足：{len(losses_pool)}")
    rng = random.Random(_sha_seed(SEED_MATERIAL))
    losses = sorted(rng.sample(losses_pool, CORPUS_N_LOSSES))
    wins = sorted(rng.sample(wins_pool, CORPUS_N_WINS)) \
        if len(wins_pool) >= CORPUS_N_WINS else list(wins_pool)
    by_ep = _pv._games_by_episode(games)
    corpus = [{"episode": ep, "seat": int(by_ep[ep]["seat"]),
               "res": by_ep[ep]["res"], "margin": by_ep[ep]["margin"]}
              for ep in losses + wins]
    return {"games": corpus,
            "sampling": {"seed_material": SEED_MATERIAL,
                         "seed_derivation":
                             "int(sha256(material).hexdigest()[:16], 16)",
                         "losses_pool": losses_pool,
                         "wins_pool": wins_pool,
                         "note": "败局池沿 R17 先例排 3 早崩局（step-91 面"
                                 "不受早崩影响，口径一致性优先，记偏差）"}}


def _load_corpus_replays(corpus: Dict[str, Any],
                         replay_dir: str) -> List[Dict[str, Any]]:
    entries = corpus.get("games") if corpus else None
    if not entries:
        raise ForensicError("语料为空（fail-closed）")
    out = []
    for e in entries:
        path = e.get("path") or _pv._replay_path(replay_dir, e["episode"])
        out.append({"episode": int(e["episode"]), "seat": int(e["seat"]),
                    "res": e.get("res"), "margin": e.get("margin"),
                    "replay": _pv._load_replay(path)})
    return out


def _fresh_agent(text: str, tag: str) -> Tuple[Any, Dict[str, Any]]:
    """全新命名空间装载（官方 last-callable + 遥测命名空间引用）。"""
    ns = _pv._exec_namespace(text, tag)
    entries = [k for k, v in ns.items() if callable(v)]
    if not entries:
        raise ForensicError(f"{tag} 装载后无 callable")
    return ns[entries[-1]], ns


def _play_with_driver(driver, replay, agent, seat) -> Dict[str, Any]:
    res = driver(replay, agent, seat)
    if res is None or res.get("margin") is None:
        raise ForensicError("driver 返回缺 margin")
    return res


def _tomato_trajectory(stream: Sequence[Any]) -> List[Dict[str, Any]]:
    """我方动作流中全部 TOMATO 市场订单轨迹（step/订单/当日价近似=成交面）。"""
    out = []
    for t, action in enumerate(stream or []):
        if not isinstance(action, dict):
            continue
        for order in action.get("market") or []:
            if (isinstance(order, (list, tuple)) and len(order) >= 3
                    and order[0] in ("BUY_SEED", "BUY_PRODUCT", "SELL")
                    and order[1] == "TOMATO"):
                out.append({"step": t, "order": list(order)})
    return out


def _wheat_stream_mark(stream: Sequence[Any]) -> Dict[str, Any]:
    """step-91 面观测：当步 WHEAT 卖单与 _CL 交付量（外视角）。"""
    mark = {"step91_wheat_sells": 0, "step91_wheat_sell_qty": 0}
    if stream and len(stream) > 91 and isinstance(stream[91], dict):
        for order in stream[91].get("market") or []:
            if (isinstance(order, (list, tuple)) and len(order) >= 3
                    and order[0] == "SELL" and order[1] == "WHEAT"):
                mark["step91_wheat_sells"] += 1
                try:
                    mark["step91_wheat_sell_qty"] += int(order[2])
                except (TypeError, ValueError):
                    pass
    return mark


def _observant(agent, box: List[Dict[str, Any]]):
    """零行为差观测包装：记录 step-91 WHEAT 价与守卫后卖单（只读不改）。"""
    def wrapped(obs, configuration=None):
        act = agent(obs, configuration)
        try:
            if int(obs.get("step", -1)) == 91:
                px = float((obs.get("market") or {}).get("prices", {})
                           .get("WHEAT", 0) or 0)
                sells = sum(1 for o in (act.get("market") or [])
                            if o and o[0] == "SELL" and o[1] == "WHEAT")
                qty = sum(int(o[2]) for o in (act.get("market") or [])
                          if o and o[0] == "SELL" and o[1] == "WHEAT"
                          and len(o) > 2)
                box.append({"price91": px, "post_sells": sells,
                            "post_qty": qty})
        except Exception:
            pass
        return act
    return wrapped


# ---------------------------------------------------------------------------
# forensic_cxtb_trigger（Phase T ①）
# ---------------------------------------------------------------------------
def forensic_cxtb_trigger(replay_dir: str = REPLAY_DIR,
                          r34a_main_path: str = R34A_MAIN,
                          replay_driver=None,
                          write_evidence: bool = True) -> Dict[str, Any]:
    """86 局 _CXTB 触发率/轨迹/结局差法证；face_alive 判定。

    每局全新命名空间装载 r34a（官方 last-callable=_cxd_agent），twin seated
    重演后读 _CXTB_REPORT：cxtb_calls=step432 面实际调用数（face 活性）、
    cxtb_opened=80 单位承诺触发数（fire）、features=投影现场。单局失败记
    errors 不阻断。
    """
    t0 = time.perf_counter()
    driver = replay_driver or _pv._seated_margin
    games = _pv._load_audit_games()
    text = _load_r34a_text(r34a_main_path)
    per_game, errors = [], []
    for g in sorted(games, key=lambda x: int(x["episode"])):
        ep = int(g["episode"])
        try:
            agent, ns = _fresh_agent(text, f"cxtb_f_{ep}")
            report = ns["_CXTB_REPORT"]
            replay = _pv._load_replay(_pv._replay_path(replay_dir, ep))
            seat = int(g["seat"])
            res = _play_with_driver(driver, replay, agent, seat)
            features = [dict(f) for f in report.get("cxtb_features", [])]
            counters = {k: report.get(k) for k in
                        ("cxtb_calls", "cxtb_opened", "cxtb_blocked",
                         "cxtb_errors")}
            fired = bool(counters.get("cxtb_opened"))
            traj = _tomato_trajectory(res.get("stream"))
            entry = {
                "episode": ep, "res": g.get("res"), "audit_margin": g.get("margin"),
                "seat": seat, "twin_margin": float(res["margin"]),
                "status": res.get("status"),
                "counters": counters, "features": features, "fired": fired,
                "tomato_orders": traj,
                "tomato_sell_qty": sum(int(o["order"][2]) for o in traj
                                       if o["order"][0] == "SELL"),
                "tomato_seed_buys": sum(int(o["order"][2]) for o in traj
                                        if o["order"][0] == "BUY_SEED"),
            }
            if features:
                entry["trigger_steps"] = [432] * len(features)
            per_game.append(entry)
        except Exception as exc:                          # 单局失败不阻断
            errors.append({"episode": ep,
                           "error": f"{type(exc).__name__}: {exc}"})
    clean = [e for e in per_game if e["status"] == "DONE"]
    n = len(clean) or len(per_game)
    n_called = sum(1 for e in per_game if e["counters"].get("cxtb_calls"))
    n_fired = sum(1 for e in per_game if e["fired"])
    n_base = sum(1 for e in per_game
                 if any(f.get("base") for f in e["features"]))
    face_alive = bool(n) and n_called >= FACE_ALIVE_CALL_SHARE * n
    fired_games = [e for e in clean if e["fired"]]
    unfired = [e for e in clean if not e["fired"] and
               e["counters"].get("cxtb_calls")]
    outcome_diff = {
        "fired": {"n": len(fired_games),
                  "twin_margin_mean": round(sum(e["twin_margin"] for e in fired_games)
                                            / len(fired_games), 1) if fired_games else None,
                  "twin_margin_median": _median([e["twin_margin"] for e in fired_games]),
                  "res_counts": _res_counts(fired_games)},
        "called_not_fired": {"n": len(unfired),
                             "twin_margin_mean": round(sum(e["twin_margin"] for e in unfired)
                                                       / len(unfired), 1) if unfired else None,
                             "twin_margin_median": _median([e["twin_margin"] for e in unfired]),
                             "res_counts": _res_counts(unfired)},
        "never_called": {"n": sum(1 for e in per_game
                                  if not e["counters"].get("cxtb_calls"))},
    }
    # 触发面画像：投影收入分布 + 阻断归因（收入线 vs 结构条件）。
    revs = [f["revenue"] for e in per_game for f in e["features"]
            if f.get("revenue") is not None]
    opened_rev = [f["revenue"] for e in per_game for f in e["features"]
                  if f.get("opened")]
    revenue_profile = {
        "n_features": len(revs),
        "revenue_min": min(revs) if revs else None,
        "revenue_median": _median(revs),
        "revenue_max": max(revs) if revs else None,
        "n_revenue_ge_9000": sum(1 for r in revs if r >= 9000),
        "n_opened_with_rev": len(opened_rev),
        "n_sensitive_band_2k": sum(1 for r in revs if abs(r - 9000) <= CXTB_SENSITIVE_BAND),
        "base_face_would_commit": n_base,
    }
    result = {
        "probe": "cxtb_trigger_forensic",
        "n_games": len(per_game), "n_clean": len(clean), "errors": errors,
        "fire_rate": round(n_fired / n, 4) if n else None,
        "fired_games": [e["episode"] for e in per_game if e["fired"]],
        "call_rate": round(n_called / n, 4) if n else None,
        "face_alive": face_alive,
        "face_alive_rule": f"n_called >= {FACE_ALIVE_CALL_SHARE}*n_clean",
        "revenue_profile": revenue_profile,
        "outcome_diff": outcome_diff,
        "per_game": per_game,
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "forensic_cxtb.json"), result)
    return result


def _res_counts(entries: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for e in entries:
        counts[e.get("res") or "?"] = counts.get(e.get("res") or "?", 0) + 1
    return counts


# ---------------------------------------------------------------------------
# scan_wheat_step91（Phase T ②）
# ---------------------------------------------------------------------------
def scan_wheat_step91(corpus: Optional[Dict[str, Any]] = None,
                      r34a_main_path: str = R34A_MAIN,
                      replay_dir: str = REPLAY_DIR,
                      replay_driver=None,
                      write_evidence: bool = True) -> Dict[str, Any]:
    """麦簇阈值五点 {25,28,31,34,38} twin 重演+触发率；胜出=Δ 中位>0+胜局不翻负。

    Δ = margin(variant T) − margin(r34a=31) 同局同席。触发率=语料局中
    step-91 WHEAT 价 < T 的比例（守卫触发条件；各点在 step-91 前与基线
    逐字节同轨迹——守卫只在 step 91 行动）。单点异常重跑一次。
    """
    t0 = time.perf_counter()
    driver = replay_driver or _pv._seated_margin
    if corpus is None:
        corpus = _r18_corpus(replay_dir)
    replays = _load_corpus_replays(corpus, replay_dir)
    text = _load_r34a_text(r34a_main_path)

    price_box: List[Dict[str, Any]] = []
    agent0, _ns = _fresh_agent(text, "wheat_baseline")
    baseline = []
    for g in replays:
        res = _play_with_driver(driver, g["replay"],
                                _observant(agent0, price_box), g["seat"])
        baseline.append({"episode": g["episode"], "res": g["res"],
                         "seat": g["seat"], "margin": float(res["margin"]),
                         "status": res.get("status"),
                         **_wheat_stream_mark(res.get("stream"))})
    base_margin = {b["episode"]: b["margin"] for b in baseline}
    price91 = {b["episode"]: p["price91"] for b, p in zip(baseline, price_box)}

    def _probe_point(point: int) -> Dict[str, Any]:
        variant_text = _b36.apply_wheat_threshold(text, point)
        agent, _ = _fresh_agent(variant_text, f"wheat_t{point}")
        per_game, win_flipped = [], []
        for g in replays:
            attempts = 0
            while True:                                   # 单点异常重跑一次
                try:
                    res = _play_with_driver(driver, g["replay"], agent, g["seat"])
                    break
                except Exception:
                    attempts += 1
                    if attempts > 1:
                        raise
            delta = round(float(res["margin"]) - base_margin[g["episode"]], 2)
            per_game.append({"episode": g["episode"], "res": g["res"],
                             "margin": res["margin"], "delta": delta,
                             "status": res.get("status")})
            if g["res"] == "W" and float(res["margin"]) <= 0:
                win_flipped.append(g["episode"])
        deltas = [p["delta"] for p in per_game]
        triggered = [1 for ep, px in price91.items() if px < point]
        return {
            "threshold": point, "per_game": per_game,
            "delta_median": _median(deltas),
            "delta_mean": round(sum(deltas) / len(deltas), 2) if deltas else None,
            "win_flips_negative": win_flipped,
            "trigger_rate": round(len(triggered) / len(replays), 4),
            "n_triggered": len(triggered),
        }

    points = []
    for p in WHEAT_POINTS:
        points.append(_probe_point(p))
    qualifies = lambda p: (p["delta_median"] is not None
                           and p["delta_median"] > 0
                           and not p["win_flips_negative"])    # noqa: E731
    candidates = [p for p in points if p["threshold"] != WHEAT_BASELINE
                  and qualifies(p)]
    best = None
    if candidates:
        best = max(candidates, key=lambda p: (p["delta_median"],
                                              p["delta_mean"] or 0))
    result = {
        "probe": "wheat_step91_scan",
        "baseline_threshold": WHEAT_BASELINE,
        "corpus": {"games": [{k: g[k] for k in ("episode", "seat", "res", "margin")}
                             for g in replays],
                   "sampling": corpus.get("sampling")},
        "baseline_replay": baseline,
        "price91": {str(k): v for k, v in sorted(price91.items())},
        "points": [{k: p[k] for k in ("threshold", "delta_median",
                                      "delta_mean", "win_flips_negative",
                                      "trigger_rate", "n_triggered")}
                   for p in points],
        "best": ({"threshold": best["threshold"],
                  "delta_median": best["delta_median"],
                  "delta_mean": best["delta_mean"],
                  "win_flips_negative": best["win_flips_negative"]}
                 if best else None),
        "adopt": best is not None,
        "params": ({"threshold": best["threshold"]} if best else None),
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "forensic_wheat.json"), result)
    return result


# ---------------------------------------------------------------------------
# adjudicate_cxtb_variants（条件判决实验：阶梯化+常数扫描）
# ---------------------------------------------------------------------------
def _sensitive_corpus(forensic_result: Dict[str, Any],
                      replay_dir: str) -> Optional[Dict[str, Any]]:
    """敏感带语料：86 局中投影收入落在 |rev−9000|≤2k 的局（常数扫描次级面）。"""
    eps = sorted({e["episode"] for e in forensic_result.get("per_game", [])
                  for f in e.get("features", [])
                  if f.get("revenue") is not None
                  and abs(f["revenue"] - 9000) <= CXTB_SENSITIVE_BAND})
    if not eps:
        return None
    by_ep = _pv._games_by_episode(_pv._load_audit_games())
    return {"games": [{"episode": ep, "seat": int(by_ep[ep]["seat"]),
                       "res": by_ep[ep]["res"], "margin": by_ep[ep]["margin"]}
                      for ep in eps]}


def _baseline_margins(text: str, replays: List[Dict[str, Any]], driver,
                     tag: str) -> Dict[int, float]:
    """基线（r34a 原文）逐局 margin，一次计算全变体复用。"""
    agent, _ = _fresh_agent(text, f"{tag}_base")
    out = {}
    for g in replays:
        res = _play_with_driver(driver, g["replay"], agent, g["seat"])
        out[g["episode"]] = float(res["margin"])
    return out


def _delta_adjudicate(base_margins: Dict[int, float],
                      replays: List[Dict[str, Any]],
                      variant_text: str, tag: str, driver) -> Dict[str, Any]:
    """通用 twin Δ 判决（variant vs 基线同局同席；基线 margin 复用）。"""
    var_agent, _ = _fresh_agent(variant_text, f"{tag}_var")
    per_game, win_flipped = [], []
    for g in replays:
        v = _play_with_driver(driver, g["replay"], var_agent, g["seat"])
        delta = round(float(v["margin"]) - base_margins[g["episode"]], 2)
        per_game.append({"episode": g["episode"], "res": g["res"],
                         "base_margin": base_margins[g["episode"]],
                         "margin": v["margin"],
                         "delta": delta})
        if g["res"] == "W" and float(v["margin"]) <= 0:
            win_flipped.append(g["episode"])
    deltas = [p["delta"] for p in per_game]
    return {"per_game": per_game,
            "delta_median": _median(deltas),
            "delta_mean": round(sum(deltas) / len(deltas), 2) if deltas else None,
            "win_flips_negative": win_flipped,
            "n_nonzero": sum(1 for d in deltas if d != 0)}


def adjudicate_cxtb_variants(face_alive: bool,
                             forensic_result: Optional[Dict[str, Any]] = None,
                             corpus: Optional[Dict[str, Any]] = None,
                             r34a_main_path: str = R34A_MAIN,
                             replay_dir: str = REPLAY_DIR,
                             replay_driver=None,
                             write_evidence: bool = True) -> Dict[str, Any]:
    """阶梯化（2/3 批）+ 三常数 OAT 扫描判决；face 不活→跳过（cxtb 项出局）。

    胜出=Δ 中位>0 且胜局不翻负（沿 Phase T 判据）；阶梯化另要求 b1_cut 在
    语料中至少触发一次（触发面为零=变体惰性，不可并入）。
    """
    t0 = time.perf_counter()
    if not face_alive:
        result = {"probe": "cxtb_variant_adjudication", "skipped":
                  "face_not_alive（cxtb 项按 R18 条款出局）",
                  "stepped": None, "constants": None, "adopt_stepped": False,
                  "adopt_constants": None, "wall_s": round(time.perf_counter() - t0, 1)}
        if write_evidence:
            result["evidence_path"] = _write_json(
                os.path.join(EVIDENCE_DIR, "adjudicate_cxtb.json"), result)
        return result
    driver = replay_driver or _pv._seated_margin
    if corpus is None:
        corpus = _r18_corpus(replay_dir)
    replays = _load_corpus_replays(corpus, replay_dir)
    text = _load_r34a_text(r34a_main_path)
    base_margins = _baseline_margins(text, replays, driver, "cxtb_adj")

    # —— 阶梯化变体（惰性判据：Δ 全零=n_nonzero 0 → 不可并入） ——
    stepped_points = []
    for batches in STEPPED_VARIANTS:
        vtext = _b36.apply_cxtb_stepped(text, batches, STEPPED_DENSITY)
        adjud = _delta_adjudicate(base_margins, replays, vtext,
                                  f"step{'x'.join(map(str, batches))}", driver)
        stepped_points.append({"batches": list(batches), "density": STEPPED_DENSITY,
                               **adjud})
    stepped_ok = [p for p in stepped_points
                  if p["delta_median"] is not None and p["delta_median"] > 0
                  and not p["win_flips_negative"] and p["n_nonzero"] > 0]
    best_stepped = max(stepped_ok, key=lambda p: (p["delta_median"],
                                                  p["delta_mean"] or 0)) \
        if stepped_ok else None

    # —— 常数 OAT 扫描（主语料=r18；敏感带语料为次级面） ——
    def _scan_constants(reps: List[Dict[str, Any]],
                        rep_base: Dict[int, float], tag: str) -> List[Dict[str, Any]]:
        pts = []
        for v in CXTB_MINREV_POINTS:
            if v == 9000:
                continue
            vt = _b36.apply_cxtb_constants(text, v, 0.75, 2.4)
            pts.append({"axis": "min_revenue", "value": v,
                        **_delta_adjudicate(rep_base, reps, vt, f"c_mr{v}_{tag}", driver)})
        for v in CXTB_THEIR_POINTS:
            if v == 0.75:
                continue
            vt = _b36.apply_cxtb_constants(text, 9000, v, 2.4)
            pts.append({"axis": "their_units", "value": v,
                        **_delta_adjudicate(rep_base, reps, vt, f"c_tu{v}_{tag}", driver)})
        for v in CXTB_SLACK_POINTS:
            if v == 2.4:
                continue
            vt = _b36.apply_cxtb_constants(text, 9000, 0.75, v)
            pts.append({"axis": "drain_slack", "value": v,
                        **_delta_adjudicate(rep_base, reps, vt, f"c_ds{v}_{tag}", driver)})
        return pts

    const_points = _scan_constants(replays, base_margins, "r18")
    sensitive = None
    if forensic_result is not None:
        sensitive = _sensitive_corpus(forensic_result, replay_dir)
    const_sensitive_points = []
    if sensitive:
        band_reps = _load_corpus_replays(sensitive, replay_dir)
        band_base = _baseline_margins(text, band_reps, driver, "cxtb_adj_band")
        const_sensitive_points = _scan_constants(band_reps, band_base, "band")


    def _const_winner(points: Sequence[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        ok = [p for p in points if p["delta_median"] is not None
              and p["delta_median"] > 0 and not p["win_flips_negative"]
              and p["n_nonzero"] > 0]
        return max(ok, key=lambda p: (p["delta_median"], p["delta_mean"] or 0)) \
            if ok else None

    best_const_r18 = _const_winner(const_points)
    best_const_band = _const_winner(const_sensitive_points)
    best_const = best_const_r18 or best_const_band
    const_params = None
    if best_const:
        p = dict(min_revenue=9000, their_units=0.75, drain_slack=2.4)
        p[best_const["axis"]] = best_const["value"]
        if best_const["axis"] == "min_revenue":
            const_params = {"min_revenue": int(best_const["value"]),
                            "their_units": 0.75, "drain_slack": 2.4}
        elif best_const["axis"] == "their_units":
            const_params = {"min_revenue": 9000,
                            "their_units": float(best_const["value"]),
                            "drain_slack": 2.4}
        else:
            const_params = {"min_revenue": 9000, "their_units": 0.75,
                            "drain_slack": float(best_const["value"])}

    result = {
        "probe": "cxtb_variant_adjudication",
        "corpus": {"games": [{k: g[k] for k in ("episode", "seat", "res", "margin")}
                             for g in replays],
                   "sampling": corpus.get("sampling")},
        "stepped": {"variants": [{k: p[k] for k in
                                  ("batches", "delta_median", "delta_mean",
                                   "win_flips_negative", "n_nonzero")}
                                 for p in stepped_points],
                    "best": ({"batches": best_stepped["batches"],
                              "delta_median": best_stepped["delta_median"]}
                             if best_stepped else None)},
        "adopt_stepped": best_stepped is not None,
        "params_stepped": ({"batches": best_stepped["batches"],
                            "density": STEPPED_DENSITY}
                           if best_stepped else None),
        "constants": {"r18_points": [{k: p[k] for k in
                                      ("axis", "value", "delta_median",
                                       "delta_mean", "win_flips_negative",
                                       "n_nonzero")} for p in const_points],
                      "sensitive_band_episodes": (sensitive or {}).get("games"),
                      "band_points": [{k: p[k] for k in
                                      ("axis", "value", "delta_median",
                                       "delta_mean", "win_flips_negative",
                                       "n_nonzero")} for p in const_sensitive_points],
                      "best": ({"axis": best_const["axis"],
                                "value": best_const["value"],
                                "face": ("band" if best_const_band is not None
                                         and best_const_r18 is None else "r18")}
                               if best_const else None)},
        "adopt_constants": bool(best_const),
        "params_constants": const_params,
        "stepped_detail": stepped_points,
        "constants_detail": {"r18": const_points, "band": const_sensitive_points},
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    if write_evidence:
        result["evidence_path"] = _write_json(
            os.path.join(EVIDENCE_DIR, "adjudicate_cxtb.json"), result)
    return result
