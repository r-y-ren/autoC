# -*- coding: utf-8 -*-
"""judge_mix —— R15 三出口判据（预绑定，不改判据）。

逐变体（开环主判据）：
  败局 ≥2/3 翻正（局级 Δ=双席位 min >0，保守主口径——R14 先例）
  + 胜局重损违例 ≤2（胜局 Δ < −100）
  + 败局 Δ 中位 >0
  → 开环 POSITIVE；
开环 POSITIVE 且闭环互胜 ≥0.5 且中位 margin ≥0（无系统性负） → 变体 POSITIVE。
任一变体 POSITIVE → R15=POSITIVE（记胜出变体）；全败 → NEGATIVE；
KILLED 由编排短路给定（本层仅透传 killed 标志）。
敏感度：2/3 vs 3/5；中位>0 vs 均值>0；min 席位 vs mean 席位聚合。
"""
from __future__ import annotations

HARM_FLOOR = -100.0        # 胜局重损违例阈：Δ < −100
FLIP_NUM, FLIP_DEN = 2, 3  # 翻正比例 2/3（敏感度面 3/5）
WIN_RATE_MIN = 0.5         # 闭环互胜 ≥0.5


def _median(vals):
    vs = sorted(vals or [])
    n = len(vs)
    if not n:
        return None
    if n % 2:
        return vs[n // 2]
    return round((vs[n // 2 - 1] + vs[n // 2]) / 2, 1)


def _variant_stats(games):
    """开环逐局 → 败局 Δ 列表（min 席位主口径/mean 席位敏感度）+ 胜局 Δ。"""
    loss_d, loss_d_mean, win_d, red_eps = [], [], [], []
    for ep, rec in (games or {}).items():
        if rec.get("red"):
            red_eps.append(int(ep))
        gd = rec.get("game_delta")
        seats = [s.get("delta") for s in (rec.get("seats") or {}).values()
                 if isinstance(s, dict) and s.get("delta") is not None]
        if gd is None or not seats:
            continue
        if rec.get("res") == "L":
            loss_d.append(gd)
            loss_d_mean.append(round(sum(seats) / len(seats), 1))
        elif rec.get("res") == "W":
            win_d.append(gd)
    return {"loss_deltas": loss_d, "loss_deltas_mean": loss_d_mean,
            "win_deltas": win_d, "red_episodes": red_eps}


def _openloop_positive(stat, num=FLIP_NUM, den=FLIP_DEN, center="median"):
    n = len(stat["loss_deltas"])
    if n == 0:
        return False, {"n_loss": 0}
    flips = sum(1 for v in stat["loss_deltas"] if v > 0)
    harm = [v for v in stat["win_deltas"] if v < HARM_FLOOR]
    center_fn = _median if center == "median" else (
        lambda vs: round(sum(vs) / len(vs), 1) if vs else None)
    cval = center_fn(stat["loss_deltas"])
    ok = (flips * den >= n * num and len(harm) <= 2
          and cval is not None and cval > 0)
    detail = {"n_loss": n, "n_flip": flips, "n_harm": len(harm),
              "center": cval, "center_kind": center}
    return ok, detail


def variant_openloop_positive(games):
    """单变体开环判据便捷面（编排层用于筛闭环副证对象）。"""
    ok, detail = _openloop_positive(_variant_stats(games))
    return ok, detail


def judge_mix_verdicts(openloop_result, closedloop_result=None,
                       killed=False):
    """三出口裁决。输出：{per_variant, overall, winning_variant,
    sensitivity, criteria, fail_closed}。语料缺失/红局/预算截断=fail_closed
    面（verdict 仍按可用数据计算并注记 degraded）。
    """
    closedloop_result = closedloop_result or {}
    per_variant = {}
    for vid, vrec in (openloop_result.get("per_variant") or {}).items():
        stat = _variant_stats(vrec.get("games"))
        ok, detail = _openloop_positive(stat)
        cl = closedloop_result.get("per_variant", {}).get(vid)
        entry = {
            "openloop_positive": ok,
            "n_loss": detail.get("n_loss"),
            "n_flip": detail.get("n_flip"),
            "flip_ratio": (round(detail["n_flip"] / detail["n_loss"], 3)
                           if detail.get("n_loss") else None),
            "loss_delta_median": _median(stat["loss_deltas"]),
            "loss_delta_mean": (round(sum(stat["loss_deltas"])
                                      / len(stat["loss_deltas"]), 1)
                                if stat["loss_deltas"] else None),
            "win_delta_median": _median(stat["win_deltas"]),
            "harm_violations": [{"delta": v} for v in stat["win_deltas"]
                                if v < HARM_FLOOR],
            "n_harm_violations": sum(1 for v in stat["win_deltas"]
                                     if v < HARM_FLOOR),
            "red_episodes": stat["red_episodes"],
            "loss_deltas": stat["loss_deltas"],
            "win_deltas": stat["win_deltas"],
        }
        if ok and cl is not None:
            rate = cl.get("rate")
            med = cl.get("median_margin")
            entry["closedloop"] = {
                "rate": rate, "median_margin": med,
                "wins": cl.get("wins"), "runs": cl.get("runs"),
                "red_runs": cl.get("red_runs"),
            }
            entry["variant_positive"] = bool(
                rate is not None and rate >= WIN_RATE_MIN
                and med is not None and med >= 0
                and not cl.get("red_runs"))
        elif ok:
            entry["variant_positive"] = False
            entry["closedloop"] = None
            entry["note"] = "开环 POSITIVE 但闭环副证缺席"
        else:
            entry["variant_positive"] = False
            entry["closedloop"] = cl and {
                "rate": cl.get("rate"), "median_margin": cl.get("median_margin")}
        per_variant[vid] = entry

    if killed:
        overall, winning = "KILLED", None
    elif any(v["variant_positive"] for v in per_variant.values()):
        overall = "POSITIVE"

        def _rank(e):
            return (e["flip_ratio"] or 0, e["loss_delta_median"] or 0,
                    e["n_harm_violations"] * -1)
        winning = max(per_variant, key=lambda k: _rank(per_variant[k]))
    else:
        overall, winning = "NEGATIVE", None

    sensitivity = {}
    for vid, vrec in (openloop_result.get("per_variant") or {}).items():
        stat = _variant_stats(vrec.get("games"))
        sensitivity[vid] = {
            "min_seat": {
                "f23_median": _openloop_positive(stat, 2, 3, "median")[0],
                "f35_median": _openloop_positive(stat, 3, 5, "median")[0],
                "f23_mean": _openloop_positive(stat, 2, 3, "mean")[0],
            },
            "mean_seat": (lambda s: {
                "f23_median": _openloop_positive(
                    {"loss_deltas": s["loss_deltas_mean"],
                     "win_deltas": s["win_deltas"]}, 2, 3, "median")[0],
                "f23_mean": _openloop_positive(
                    {"loss_deltas": s["loss_deltas_mean"],
                     "win_deltas": s["win_deltas"]}, 2, 3, "mean")[0],
            })(stat),
        }
    summary = openloop_result.get("summary") or {}
    fail_closed = bool(
        summary.get("budget_stopped")
        or any(v["red_episodes"] for v in per_variant.values()))
    return {
        "per_variant": per_variant, "overall": overall,
        "winning_variant": winning, "sensitivity": sensitivity,
        "fail_closed": fail_closed,
        "harm_floor": HARM_FLOOR, "win_rate_min": WIN_RATE_MIN,
        "criteria": ("逐变体：败局≥2/3 翻正[局级Δ=双席min>0]+胜局违例≤2"
                     "[Δ<−100]+败局Δ中位>0 → 开环 POSITIVE；且闭环互胜≥0.5"
                     "无系统性负[中位≥0] → 变体 POSITIVE"),
    }
