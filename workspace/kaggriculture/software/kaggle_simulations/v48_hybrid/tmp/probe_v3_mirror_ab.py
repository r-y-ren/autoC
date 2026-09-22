# -*- coding: utf-8 -*-
# 【中文】probe_v3_mirror_ab.py —— v3 冲刺镜像专项 A/B（临时探针，F3 补充判据）
# ===========================================================================
# 对照组（如实登记，全部既有实测、零重跑对局）：
#   * v2 = tmp/gates_v2_out/h2h_gate.json（v2 批次 hybrid_all_on vs pure_v48，
#     8 种子×双席，records 含逐局 me/opp/money/margin/result）；
#   * v3 = gates/out/h2h_gate.json（v3 批次同种子域同席位语义）。
# 对称种子 = v2 批次双席全 TIE 的种子（双方同路由互克隆 → 镜像局）。
# 判据（requirements.md 2026-09-23 行）：
#   * 新门：对 v48 互胜 ≥0.55（16 局）；8 平局中 ≥5 局翻胜；
#   * 镜像共振：对称种子上 v3 相对 v2 的资金边际（v3 混合席资金 -
#     v2 混合席资金）负局占比 > 1/3 → FAIL 风险（双重抢卖压价反噬）。
# 附加机制遥测：一个对称种子真引擎镜像局内，P1 近克隆接管帧数与
#   补发单数/件数（wrap v48h.p1_midgame_sell_layer.plan_midgame_sells 计数）。
# 产物：tmp/v3_mirror_ab.json。CLI：python tmp/probe_v3_mirror_ab.py
# ===========================================================================
from __future__ import annotations

import json
import os
import sys

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
_GATES = os.path.join(os.path.dirname(_HERE), "gates")
for _p in (_GATES, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_common as gc  # noqa: E402

V2_H2H = os.path.join(_HERE, "gates_v2_out", "h2h_gate.json")
V3_H2H = os.path.join(gc.OUT_DIR, "h2h_gate.json")
OUT = os.path.join(_HERE, "v3_mirror_ab.json")
SPRINT_WIN_FRACTION_FLOOR = 0.55
TIE_FLIP_FLOOR = 5
NEG_SHARE_CEILING = 1 / 3


def load_records(path):
    with open(path, encoding="utf-8") as h:
        rep = json.load(h)
    recs = rep["series"]["pure_v48"]["records"]
    return rep, {(r["seed"], r["me_seat"]): r for r in recs}


def mirror_telemetry(seed=101, me_seat=0):
    """单镜像局机制遥测：P1 近克隆接管帧 + 补发卖单数/件数（真引擎）。"""
    fn = gc.load_agent(gc.HYB_MAIN)
    mod = sys.modules["v48h.p1_midgame_sell_layer"]
    orig = mod.plan_midgame_sells
    tel = {"calls": 0, "takeover_frames": 0, "near_clone_takeover_frames": 0,
           "supplement_orders": 0, "supplement_units": 0,
           "supplement_examples": []}

    def wrapped(obs, tape, config=None):
        out = orig(obs, tape, config)
        tel["calls"] += 1
        try:
            tape_keys = {(o[1], o[2]) for o in (tape or [])
                         if isinstance(o, (list, tuple)) and len(o) >= 3
                         and o[0] == "SELL"}
            sup = [o for o in (out or [])
                   if isinstance(o, (list, tuple)) and len(o) >= 3
                   and o[0] == "SELL" and (o[1], o[2]) not in tape_keys]
            if sup:
                tel["takeover_frames"] += 1
                if mod.should_defer_to_tape(obs) and \
                        not mod.should_defer_to_tape_p1(obs):
                    tel["near_clone_takeover_frames"] += 1
                tel["supplement_orders"] += len(sup)
                tel["supplement_units"] += sum(o[2] for o in sup
                                               if isinstance(o[2], (int, float)))
                if len(tel["supplement_examples"]) < 6:
                    step = (obs.get("step") if isinstance(obs, dict)
                            else getattr(obs, "step", None))
                    tel["supplement_examples"].append(
                        {"step": step, "orders": [list(o) for o in sup]})
        except Exception as e:                    # noqa: BLE001
            tel.setdefault("telemetry_error", []).append(repr(e)[:120])
        return out

    mod.plan_midgame_sells = wrapped
    try:
        pair = [gc.load_agent(gc.BASE_MAIN), gc.load_agent(gc.BASE_MAIN)]
        pair[me_seat] = fn
        from kaggle_environments import make
        env = make("kaggriculture",
                   configuration={"episodeSteps": gc.FULL_STEPS,
                                  "seed": int(seed),
                                  "actTimeout": gc.ACT_TIMEOUT},
                   debug=True)
        env.run(pair)
        final = env.steps[-1]
        me_money = float(final[me_seat]["reward"])
        opp_money = float(final[1 - me_seat]["reward"])
    finally:
        mod.plan_midgame_sells = orig
    tel["game"] = {"seed": seed, "me_seat": me_seat,
                   "me_money": me_money, "opp_money": opp_money,
                   "margin": round(me_money - opp_money, 1)}
    return tel


def main() -> int:
    rep2, v2 = load_records(V2_H2H)
    rep3, v3 = load_records(V3_H2H)

    symmetric = sorted({s for (s, _), r in v2.items()
                        if r["result"] == "TIE"})
    symmetric = [s for s in symmetric
                 if all((s, seat) in v2 and (s, seat) in v3
                        for seat in (0, 1))]

    games = []
    for seed in symmetric:
        for seat in (0, 1):
            a, b = v2[(seed, seat)], v3[(seed, seat)]
            games.append({
                "seed": seed, "me_seat": seat,
                "v2": {"me": a["me_money"], "opp": a["opp_money"],
                       "margin": a["margin"], "result": a["result"]},
                "v3": {"me": b["me_money"], "opp": b["opp_money"],
                       "margin": b["margin"], "result": b["result"]},
                "delta_me_money": round(b["me_money"] - a["me_money"], 1),
                "delta_margin": round(b["margin"] - a["margin"], 1),
            })

    n = len(games)
    tie_flips = sum(1 for g in games
                    if g["v2"]["result"] == "TIE" and g["v3"]["result"] == "WIN")
    tie_backfires = sum(1 for g in games if g["v2"]["result"] == "TIE"
                        and g["v3"]["result"] == "LOSS")
    neg_games = [g for g in games if g["delta_me_money"] < 0]
    neg_share = round(len(neg_games) / n, 4) if n else None

    v3_series = rep3["series"]["pure_v48"]
    win_fraction = v3_series["win_fraction_strict"]
    sprint_gate = {
        "win_fraction_vs_v48": win_fraction,
        "win_fraction_floor": SPRINT_WIN_FRACTION_FLOOR,
        "win_fraction_ok": win_fraction >= SPRINT_WIN_FRACTION_FLOOR,
        "games_vs_v48": v3_series["games"],
        "v2_win_fraction_baseline": rep2["series"]["pure_v48"][
            "win_fraction_strict"],
        "tie_flip_count": tie_flips,
        "tie_flip_floor": TIE_FLIP_FLOOR,
        "tie_flip_ok": tie_flips >= TIE_FLIP_FLOOR,
        "mirror_resonance_neg_share": neg_share,
        "neg_share_ceiling": round(NEG_SHARE_CEILING, 4),
        "neg_share_ok": neg_share is not None
                        and neg_share <= NEG_SHARE_CEILING,
    }
    sprint_gate["passed"] = (sprint_gate["win_fraction_ok"]
                             and sprint_gate["tie_flip_ok"]
                             and sprint_gate["neg_share_ok"])

    print(f"-- 镜像机制遥测（seed=101 seat=0 真引擎单局）--", flush=True)
    tel = mirror_telemetry(101, 0)
    print(json.dumps(tel, ensure_ascii=False, indent=1))

    report = {
        "protocol": "v48h-v3-mirror-ab/1.0",
        "sources": {"v2": V2_H2H, "v3": V3_H2H,
                    "note": "既有 h2h 实测对照，零重跑；v2=快照批次，"
                            "v3=本批次"},
        "symmetric_seeds": symmetric,
        "symmetric_definition": "v2 批次双席全 TIE 的种子（镜像局）",
        "games": games,
        "mirror_summary": {
            "n_games": n,
            "tie_flipped_to_win": tie_flips,
            "tie_flipped_to_loss_backfire": tie_backfires,
            "tie_kept": n - tie_flips - tie_backfires,
            "neg_delta_me_games": len(neg_games),
            "neg_share": neg_share,
            "avg_delta_me_money": round(sum(g["delta_me_money"]
                                            for g in games) / max(1, n), 1),
            "avg_delta_margin": round(sum(g["delta_margin"]
                                          for g in games) / max(1, n), 1),
            "per_game_delta_me": {f"s{g['seed']}_seat{g['me_seat']}":
                                  g["delta_me_money"] for g in games},
        },
        "mechanism_telemetry": tel,
        "sprint_gate": sprint_gate,
    }
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(report, h, ensure_ascii=False, indent=1)
    print(json.dumps({"mirror_summary": report["mirror_summary"],
                      "sprint_gate": sprint_gate},
                     ensure_ascii=False, indent=1))
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
