# -*- coding: utf-8 -*-
"""Phase 3b：最优点邻域细探 + top-5 精评（复跑确认确定性）。"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/tmp/mathsearch")
import psearch as ps
from runner import run_configs

D = dict(ps.DEFAULT_CFG)


def cfg(name, **kw):
    c = dict(D)
    c.update(kw)
    c["name"] = name
    return c


PROBES = [
    cfg("L15-1500-h18-cap2-noskip", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=2, skip_tape=False),
    cfg("L15-1500-h12-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=(12,), cap=2),
    cfg("L15-1500-h6-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=(6,), cap=2),
    cfg("L15-1500-absorb-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=ps.HOURS_ABSORB, cap=2),
    cfg("v2trig-h18-cap2", hours=(18,), cap=2),
    cfg("dd2000-h18-cap2", arms="dd_only", DD=2000.0, hours=(18,), cap=2),
    cfg("dd3000-h18-cap2", arms="dd_only", DD=3000.0, hours=(18,), cap=2),
    cfg("L15-1500-h18-cap8", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=8),
    cfg("L15-1500-h18-cap13", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=13),
    cfg("dd1000-h18-fall-cap2", arms="dd_only", DD=1000.0, hours=(18,),
        line_sel="falling", cap=2),
    cfg("dd1000-h18-cap2-noskip", arms="dd_only", DD=1000.0, hours=(18,),
        cap=2, skip_tape=False),
    cfg("dd1000-D18-h18-cap2", arms="dd_only", DD=1000.0, D_A=18, hours=(18,),
        cap=2),
    cfg("dd1000-L3000-h18-cap2", arms="dd_only", DD=1000.0, L_A=3000.0,
        hours=(18,), cap=2),
    cfg("L15-1500-h18-cap2-high", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=2, line_sel="high"),
]

TOP5 = [
    cfg("TOP1-L15-1500-h18-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=2),
    cfg("TOP2-uni-A1000-B15-3000-h18-cap2", DD=1000.0, D_B=15, L_B=3000.0,
        hours=(18,), cap=2),
    cfg("TOP3-L15-3000-h18-cap2", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), cap=2),
    cfg("TOP4-dd1000-h18", arms="dd_only", DD=1000.0, hours=(18,)),
    cfg("TOP5-dd1000-h18-cap2", arms="dd_only", DD=1000.0, hours=(18,), cap=2),
]


def summarize(r, base):
    deltas = {g["ep"]: round(g["margin"] - base[g["ep"]], 2) for g in r["games"]}
    return {
        "name": r["cfg"]["name"], "dsum": round(sum(deltas.values()), 2),
        "pos": sum(1 for v in deltas.values() if v > 0),
        "neg": sum(1 for v in deltas.values() if v < 0),
        "armed_games": sum(1 for g in r["games"] if g["armed_frames"] > 0),
        "flips": sum(1 for g in r["games"] if g["margin"] > 0),
        "deltas": deltas,
        "margins": {g["ep"]: g["margin"] for g in r["games"]},
        "telemetry": {g["ep"]: {k: g[k] for k in
                                ("armed_frames", "emit_frames",
                                 "emit_units", "first_armed_step")}
                      for g in r["games"]}}


if __name__ == "__main__":
    with open("/tmp/mathsearch/baseline.json") as h:
        base = {g["ep"]: g["margin"] for g in json.load(h)["games"]}
    res_probe, wall1 = run_configs(PROBES)
    res_top, wall2 = run_configs(TOP5)
    probes = [summarize(r, base) for r in res_probe]
    tops = [summarize(r, base) for r in res_top]
    with open("/tmp/mathsearch/phase3b.json", "w") as h:
        json.dump({"probes": {"wall_s": wall1, "table": probes},
                   "top5_precise": {"wall_s": wall2, "table": tops}},
                  h, ensure_ascii=False, indent=1)
    print("== probes ==")
    for row in sorted(probes, key=lambda t: -t["dsum"]):
        print(f"{row['name']:28s} dsum={row['dsum']:9.1f} pos={row['pos']} "
              f"neg={row['neg']} armed={row['armed_games']:2d} "
              f"flips={row['flips']}")
    print("== top5 precise (rerun) ==")
    for row in tops:
        print(f"{row['name']:34s} dsum={row['dsum']:9.1f} pos={row['pos']} "
              f"neg={row['neg']} armed={row['armed_games']:2d} "
              f"flips={row['flips']}")
    print("wall_s", wall1, wall2)
