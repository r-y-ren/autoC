# -*- coding: utf-8 -*-
"""judge —— R14 判据级裁决（预绑定 v2，逐臂独立判）。

判据（需求 R14 验收②，不改动）：
  某臂 POSITIVE ⇔ 在"可处置显著局"中 Δmargin>0 的局数 ≥2/3
  且全语料（含胜局）Δ ≥ −100（无害带，逐局）。
  任一臂 POSITIVE → 整体 POSITIVE（记胜出臂）；全臂 NEGATIVE → NEGATIVE；
  KILLED_A=全语料零可处置 surge 日（run_judgment 短路给定）。
  附敏感度：Δ>0 vs Δ>50；2/3 vs 3/4；局级 Δ 聚合 min（双席位均改善，
  保守主口径）vs mean（席位均值，敏感度面）。
"""
from __future__ import annotations

HARM_FLOOR = -100.0     # 全语料无害带下界
ARMS = ("A1", "A2", "A3")


def _game_arm_deltas(game_rec):
    """单局单臂 → {'min': Δ_min_seat, 'mean': Δ_mean, 'seats': {...}, 'red': bool}。

    缺席/红标/对照失败 → None（该局该臂数据不可用）。
    """
    arms_out = {}
    seats = game_rec.get("arms") or {}
    if not seats or any("error" in seats.get(f"seat{s}", {"error": 1})
                        for s in (0, 1)):
        return {arm: None for arm in ARMS}
    for arm in ARMS:
        vals, usable = [], True
        for s in (0, 1):
            rec = (seats.get(f"seat{s}") or {}).get(arm) or {}
            if rec.get("red") or rec.get("error") or rec.get("delta") is None:
                usable = False
                break
            vals.append(float(rec["delta"]))
        if not usable:
            arms_out[arm] = None
        else:
            arms_out[arm] = {"min": min(vals), "mean": sum(vals) / len(vals),
                             "seats": vals}
    return arms_out


def _arm_stats(games, arm, delta_key="min"):
    """逐臂统计：显著局（可处置败局）n_sig/n_pos 与全语料无害带。"""
    sig_deltas, all_deltas, red_games = [], [], []
    for g in games:
        d = _game_arm_deltas(g).get(arm)
        if d is None:
            if g.get("res") == "L" and g.get("treatable") \
                    and not g.get("error"):
                red_games.append(g.get("episode"))
            continue
        all_deltas.append((g.get("episode"), d[delta_key]))
        if g.get("res") == "L" and g.get("treatable"):
            sig_deltas.append(d[delta_key])
    n_pos = sum(1 for v in sig_deltas if v > 0)
    harm = [{"episode": ep, "delta": v} for ep, v in all_deltas
            if v < HARM_FLOOR]
    return {"n_sig": len(sig_deltas), "n_pos": n_pos,
            "sig_deltas": [round(v, 1) for v in sig_deltas],
            "all_deltas": [(ep, round(v, 1)) for ep, v in all_deltas],
            "harm_violations": harm, "red_games": red_games}


def _positive(stat, frac_num=2, frac_den=3, pos_threshold=0.0):
    if stat["n_sig"] == 0:
        return False
    return (stat["n_pos"] * frac_den >= stat["n_sig"] * frac_num
            and not stat["harm_violations"])


def judge_verdicts(phase_b_result, phase_a_report, killed_a=False):
    """逐臂独立判据 + 敏感度 + 整体 verdict。

    输入：phase_b_four_arm_replay 产物 + Phase A 报告（treatable 标注）。
    输出：{per_arm, overall, winning_arm, sensitivity, fail_closed}。
    语料缺失局（Phase A 检出而 Phase B 缺席）= fail（fail_closed 面，
    verdict 仍按可用数据计算并在 degraded 注记）。
    """
    by_ep = {g.get("episode"): g for g in phase_a_report.get("per_game", [])}
    games = []
    missing = []
    for g in phase_b_result.get("per_game", []):
        pa = by_ep.get(g.get("episode")) or {}
        merged = dict(g)
        merged["treatable"] = pa.get("treatable")
        games.append(merged)
    expect_eps = set()
    pb_corpus = phase_b_result.get("_corpus") or {}
    for entry in (pb_corpus.get("losses", []) + pb_corpus.get("wins", [])):
        expect_eps.add(entry.get("episode"))
    have_eps = {g.get("episode") for g in games}
    missing = sorted(ep for ep in expect_eps if ep not in have_eps)

    per_arm = {}
    for arm in ARMS:
        stat = _arm_stats(games, arm, "min")
        per_arm[arm] = {
            "positive": _positive(stat),
            "n_sig": stat["n_sig"], "n_pos": stat["n_pos"],
            "n_harm_violations": len(stat["harm_violations"]),
            "harm_violations": stat["harm_violations"],
            "red_games": stat["red_games"],
            "sig_delta_min_seat": stat["sig_deltas"],
            "sig_delta_median": _median(stat["sig_deltas"]),
            "all_delta_min": min((v for _, v in stat["all_deltas"]),
                                 default=None),
            "all_delta_max": max((v for _, v in stat["all_deltas"]),
                                 default=None),
        }
    positives = [a for a in ARMS if per_arm[a]["positive"]]
    if killed_a:
        overall = "KILLED_A"
    elif positives:
        overall = "POSITIVE"
    else:
        overall = "NEGATIVE"
    winning_arm = None
    if positives:
        stat_mean = {a: _arm_stats(games, a, "mean") for a in ARMS}

        def _rank(a):
            s_min = _arm_stats(games, a, "min")
            s_mean = stat_mean[a]
            ratio = (s_min["n_pos"] / s_min["n_sig"]) if s_min["n_sig"] else 0
            mean_pos = (sum(s_min["sig_deltas"]) / len(s_min["sig_deltas"])
                        if s_min["sig_deltas"] else float("-inf"))
            mean_all = (sum(v for _, v in s_mean["all_deltas"])
                        / max(1, len(s_mean["all_deltas"])))
            return (ratio, mean_pos, mean_all)

        winning_arm = max(positives, key=_rank)
    sensitivity = {}
    for arm in ARMS:
        stat = _arm_stats(games, arm, "min")
        stat_mean = _arm_stats(games, arm, "mean")
        sensitivity[arm] = {
            "min_seat": {
                "d0_f23": _positive(stat, 2, 3, 0.0),
                "d0_f34": _positive(stat, 3, 4, 0.0),
                "d50_f23": _positive(stat, 2, 3, 50.0),
                "d50_f34": _positive(stat, 3, 4, 50.0),
            },
            "mean_seat": {
                "d0_f23": _positive(stat_mean, 2, 3, 0.0),
                "d0_f34": _positive(stat_mean, 3, 4, 0.0),
                "d50_f23": _positive(stat_mean, 2, 3, 50.0),
                "d50_f34": _positive(stat_mean, 3, 4, 50.0),
            },
        }
    fail_closed = bool(missing) or any(
        per_arm[a]["red_games"] for a in ARMS) or bool(
        phase_b_result.get("summary", {}).get("budget_stopped"))
    return {"per_arm": per_arm, "overall": overall,
            "winning_arm": winning_arm, "sensitivity": sensitivity,
            "missing_games": missing, "fail_closed": fail_closed,
            "harm_floor": HARM_FLOOR,
            "criteria": ("可处置显著局 ≥2/3 局 Δmargin>0（局级 Δ=双席位 min，"
                         "保守主口径）且全语料 Δ≥−100 → 该臂 POSITIVE")}


def _median(vals):
    vs = sorted(vals or [])
    n = len(vs)
    if n == 0:
        return None
    if n % 2:
        return vs[n // 2]
    return round((vs[n // 2 - 1] + vs[n // 2]) / 2, 1)
