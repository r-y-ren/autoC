# -*- coding: utf-8 -*-
"""calibrate_grid_c2：C2 条件视界小网格标定（H_SHORT 冻结；判决先行·不发射）。

责任口径（任务 opp-conditional A1）："r37 型→视界缩短吃其前跑、参数由小网格
标定"。网格=H_SHORT∈{8,12,16,24}（build/grid_h*/，仅 C2 门生效）；标定面=
系谱三件（r37/2965a/r40——C2 类门命中面；H1/未知零改动不入网格）；每格
2 seeds × 双席配对（h1_base 同 seed 同席对照，Δ=margin_grid−margin_base）。
选择规则（预登记）：H*=argmax_H min_对手 mean_Δ（minimax 护逐面无劣化），
并列取大 H（贴 40 档默认更稳）。与判决语料隔离（throwaway 673000+i*37）。
只写 orderbook_oppcond_lab/。不改既有代码。不发射。
"""
from __future__ import annotations

import json
import multiprocessing
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

BUILD = MODULE_DIR / "build"
BASE = BUILD / "h1_base" / "main.py"
GRID_H = (8, 12, 16, 24)
OPPONENTS = {
    "r37": str(KSIM_DIR / "orderbook_r37" / "build" / "main.py"),
    "2965a": str(KSIM_DIR / "orderbook_2965_adopt" / "a" / "main.py"),
    "r40": str(KSIM_DIR / "orderbook_r40" / "build" / "main.py"),
}
GRID_SEEDS = [673000, 673037]        # throwaway 域（判决语料零交集）
WORKERS = 2
RECORD_VERSION = "oppcond-grid-c2/1.0"


def _run_chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    games, meta = [], []
    for g in payload["games"]:
        ag, sinks = j23._build_agents(g["spec"])
        games.append({"seed": int(g["spec"]["seed"]), "agents": ag})
        meta.append(g)
    res = sb.run_games(games, {"engine": "auto", "workers": 1}) \
        if games else {"games": [], "engine": None}
    rows = list(res.get("games") or [])
    out = []
    for i, g in enumerate(meta):
        rr = rows[i] if i < len(rows) else {}
        seat = int(g["spec"]["our_seat"])
        row = {"tag": g["tag"], "opponent": g["opponent"], "seed": g["spec"]["seed"],
               "seat": seat, "banks": rr.get("banks"), "error": rr.get("error")}
        if rr.get("banks") is not None and rr.get("error") is None:
            banks = rr["banks"]
            row["margin"] = round(float(banks[seat]) - float(banks[1 - seat]), 2)
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def main():
    t0 = time.perf_counter()
    specs = []

    def _add(tag, arm_path, opp, seed, seat):
        agents = ([{"type": "python", "path": arm_path},
                   {"type": "python", "path": OPPONENTS[opp]}] if seat == 0
                  else [{"type": "python", "path": OPPONENTS[opp]},
                        {"type": "python", "path": arm_path}])
        specs.append({"tag": tag, "opponent": opp, "spec": {
            "game_id": "grid-%s-%s-%d-%d" % (tag, opp, seed, seat),
            "seed": seed, "kind": "grid", "trace": False, "our_seat": seat,
            "agents": agents}})

    for opp in OPPONENTS:
        for seed in GRID_SEEDS:
            for seat in (0, 1):
                _add("base", str(BASE), opp, seed, seat)
                for h in GRID_H:
                    _add("h%d" % h, str(BUILD / ("grid_h%d" % h) / "main.py"),
                         opp, seed, seat)
    chunks = [specs[i::WORKERS] for i in range(WORKERS)]
    tasks = [{"games": c} for c in chunks if c]
    if WORKERS <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows = []
    for p in parts:
        rows.extend(p["rows"])

    # 配对 Δ
    idx = {(r["tag"], r["opponent"], r["seed"], r["seat"]): r for r in rows}
    table = {}
    for h in GRID_H:
        per_opp = {}
        for opp in OPPONENTS:
            deltas = []
            for seed in GRID_SEEDS:
                for seat in (0, 1):
                    a = idx.get(("h%d" % h, opp, seed, seat), {})
                    b = idx.get(("base", opp, seed, seat), {})
                    if a.get("margin") is not None and b.get("margin") is not None:
                        deltas.append(round(a["margin"] - b["margin"], 2))
            per_opp[opp] = {
                "n_units": len(deltas),
                "deltas": deltas,
                "mean_delta": round(sum(deltas) / len(deltas), 2) if deltas else None,
            }
        means = [v["mean_delta"] for v in per_opp.values()
                 if v["mean_delta"] is not None]
        table[str(h)] = {"per_opponent": per_opp,
                         "min_mean_delta": min(means) if means else None,
                         "pooled_mean_delta": (round(sum(
                             d for v in per_opp.values()
                             for d in v["deltas"]) / max(1, sum(
                                 v["n_units"] for v in per_opp.values())), 2)
                             if means else None)}
    cand = [(h, table[str(h)]["min_mean_delta"], table[str(h)]["pooled_mean_delta"])
            for h in GRID_H if table[str(h)]["min_mean_delta"] is not None]
    # minimax 护逐面；并列取大 H
    cand.sort(key=lambda x: (x[1], x[2], x[0]), reverse=True)
    h_star = int(cand[0][0]) if cand else None

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_oppcond_lab/build_oppcond.py grid",
                         "python3 orderbook_oppcond_lab/calibrate_grid_c2.py"],
            "grid": list(GRID_H), "opponents": list(OPPONENTS),
            "grid_seeds": GRID_SEEDS,
            "seed_isolation": "throwaway 域 673000+i*37（判决语料零交集）",
            "selection_rule": "H*=argmax_H min_对手 mean_Δ（minimax 护逐面无劣化），"
                              "并列取大 H（贴 40 档默认更稳）",
            "workers": WORKERS,
        },
        "table": table, "h_short_selected": h_star,
        "n_games": len(rows),
        "n_error_games": sum(1 for r in rows if r.get("error")),
        "engines": [p.get("engine") for p in parts],
        "elapsed_s": round(time.perf_counter() - t0, 1),
        "rows": rows,
    }
    evid = MODULE_DIR / "evidence"
    evid.mkdir(parents=True, exist_ok=True)
    (evid / "grid_c2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print(json.dumps({"table": table, "h_short_selected": h_star},
                     ensure_ascii=False, indent=1, default=str))
    print("elapsed", out["elapsed_s"], "s errors", out["n_error_games"])
    return out


if __name__ == "__main__":
    main()
