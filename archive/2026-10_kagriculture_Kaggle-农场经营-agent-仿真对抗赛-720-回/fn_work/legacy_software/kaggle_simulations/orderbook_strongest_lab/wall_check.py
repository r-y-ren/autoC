# -*- coding: utf-8 -*-
"""wall_check：墙存在性前置核查（任务步骤1）——量 H 件动作流的 d27+ 挂单形态。

只读跑 H（haodou V82）作我席追踪局，量 step>=624 窗的请求量/单均量/
qty>库存幻影单计数；并切 670-695 磁带片（r40 族 route2 幻影单墙签名
qty≈1000 且 clamp_sells 关）。产出 evidence/wall_check.json。
不改既有代码；只写 orderbook_strongest_lab/ 与 /tmp。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]

H_MAIN = os.path.join(KSIM, "orderbook_haodou_adopt", "submission_main.py")
A_MAIN = os.path.join(KSIM, "orderbook_r44_a", "main.py")


def _load_H():
    # H 从 tar 解出；此处直接读 lab 内复制件（同 sha）
    return os.path.join(ROOT, "evidence", "H_base_main.py.copy")


def phantom_stats(sink):
    """H 席 traced sink → 挂单形态 + qty>库存幻影单计数（step>=624 与 670-695 片）。"""
    rows = []  # (step, day, item, qty, held)
    for entry in (sink or []):
        step, obs, act = entry[0], entry[1], entry[2]
        step = int(step)
        if not isinstance(act, dict):
            continue
        shed = ((obs or {}).get("private") or {}).get("shed") or {}
        if not isinstance(shed, dict):
            shed = {}
        for cmd in (act.get("market") or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                try:
                    qty = float(cmd[2])
                except (TypeError, ValueError):
                    continue
                item = str(cmd[1])
                held = shed.get(item, 0)
                try:
                    held = float(held)
                except (TypeError, ValueError):
                    held = 0.0
                rows.append((step, step // 24, item, qty, held))

    def _agg(sel):
        n = len(sel)
        qty = sum(r[3] for r in sel)
        ph = [r for r in sel if r[3] > r[4]]          # qty>库存幻影单
        ph_qty_over = sum(r[3] - r[4] for r in ph)     # 超库存挂量
        qty_1000 = [r for r in sel if r[3] >= 500]     # 大单（≈1000 墙签名）
        return {
            "orders": n,
            "qty_total": round(qty, 1),
            "avg_qty_per_order": round(qty / n, 2) if n else None,
            "max_qty": round(max((r[3] for r in sel), default=0.0), 1),
            "phantom_orders_qty_gt_held": len(ph),
            "phantom_qty_over_held": round(ph_qty_over, 1),
            "big_orders_qty_ge_500": len(qty_1000),
            "big_orders_qty_ge_500_qty": round(sum(r[3] for r in qty_1000), 1),
        }

    win624 = [r for r in rows if r[0] >= 624]
    win670_695 = [r for r in rows if 670 <= r[0] <= 695]
    d27 = [r for r in rows if r[1] == 27]
    return {
        "all_days": _agg(rows),
        "step_ge_624": _agg(win624),
        "step_670_695": _agg(win670_695),
        "d27": _agg(d27),
    }


def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            metas.append((spec, {"build_error": repr(exc)[:120]}))
            games.append({"seed": int(spec["seed"]), "agents": []})
            continue
        metas.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        seat = int(spec.get("our_seat", 0))
        item = {"seed": int(spec["seed"]), "seat": seat,
                "banks": rr.get("banks"), "error": rr.get("error")}
        if isinstance(sinks, dict) and "build_error" in sinks:
            item["error"] = sinks["build_error"]
            item["wall"] = None
        else:
            sink = (sinks or {}).get(seat)
            item["wall"] = phantom_stats(sink) if sink is not None else None
        out.append(item)
    return {"rows": out, "engine": res.get("engine")}


def main():
    os.chdir(ROOT)
    h_main = _load_H()
    seeds = REPLAY_26[:8]           # 8 个回放种子（快速存在性核查）
    specs = []
    for seed in seeds:
        for seat in (0, 1):
            a = {"type": "python", "path": h_main}
            b = {"type": "python", "path": A_MAIN}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({"game_id": "wc-%d-s%d" % (seed, seat), "seed": seed,
                          "kind": "pair", "arm": "H", "our_seat": seat,
                          "trace": True, "agents": agents})
    t0 = time.perf_counter()
    # workers=2
    n = 2
    tasks = [{"specs": specs[i::n], "cfg": {"engine": "auto", "workers": 1}}
             for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    ctx = multiprocessing.get_context("fork")
    with ctx.Pool(processes=n) as pool:
        parts = pool.map(_chunk, tasks)
    rows = []
    for p in parts:
        rows.extend(p["rows"])
    # 聚合
    walls = [r["wall"] for r in rows if r.get("wall")]
    def _sum_win(key, sub, field):
        return sum((w[sub].get(field, 0) or 0) for w in walls)
    def _agg_win(sub):
        orders = _sum_win(None, sub, "orders")
        qty = _sum_win(None, sub, "qty_total")
        ph = _sum_win(None, sub, "phantom_orders_qty_gt_held")
        phq = _sum_win(None, sub, "phantom_qty_over_held")
        big = _sum_win(None, sub, "big_orders_qty_ge_500")
        bigq = _sum_win(None, sub, "big_orders_qty_ge_500_qty")
        mx = max((w[sub].get("max_qty", 0) or 0) for w in walls) if walls else 0
        return {"orders_total": orders, "qty_total": round(qty, 1),
                "avg_qty_per_order": round(qty / orders, 2) if orders else None,
                "max_qty": round(mx, 1),
                "phantom_orders_qty_gt_held": ph,
                "phantom_qty_over_held": round(phq, 1),
                "big_orders_qty_ge_500": big,
                "big_orders_qty_ge_500_qty": round(bigq, 1)}
    agg = {k: _agg_win(k) for k in ("all_days", "step_ge_624",
                                    "step_670_695", "d27")}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "wall-check/1.0",
        "source": {"commands": ["python3 orderbook_strongest_lab/wall_check.py"],
                   "seeds": seeds, "n_games": len(rows),
                   "h_main": h_main, "opp": A_MAIN, "workers": 2},
        "wall_present_signal": {
            "step_670_695_big_orders_qty_ge_500": agg["step_670_695"]["big_orders_qty_ge_500"],
            "step_670_695_max_qty": agg["step_670_695"]["max_qty"],
            "step_670_695_avg_qty": agg["step_670_695"]["avg_qty_per_order"],
            "step_ge_624_phantom_orders": agg["step_ge_624"]["phantom_orders_qty_gt_held"],
            "clamp_sells_setting": False,
        },
        "aggregate": agg,
        "per_game": rows,
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    open(os.path.join(ROOT, "evidence", "wall_check.json"), "w").write(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
    print("WALL aggregate:", json.dumps(agg, ensure_ascii=False, indent=1))
    print("signal:", json.dumps(out["wall_present_signal"], ensure_ascii=False))
    print("elapsed", out["elapsed_s"], "s")


if __name__ == "__main__":
    main()
