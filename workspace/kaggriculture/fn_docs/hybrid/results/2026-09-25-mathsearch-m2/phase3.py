# -*- coding: utf-8 -*-
"""Phase 3：交互组合（围绕 phase1/2 最优轴组合）。"""
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


CONFIGS = [
    # 锚点：late 臂 + h18（phase2 最优）
    cfg("L15-3000-h18-cap2", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), cap=2),
    cfg("L15-3000-h18-falling", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), line_sel="falling"),
    cfg("L15-3000-h18-fall-cap2", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), line_sel="falling", cap=2),
    cfg("L15-1500-h18", arms="late_only", D_B=15, L_B=1500.0, hours=(18,)),
    cfg("L15-1500-h18-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), cap=2),
    cfg("L18-3000-h18", arms="late_only", D_B=18, L_B=3000.0, hours=(18,)),
    cfg("L18-3000-h18-cap2", arms="late_only", D_B=18, L_B=3000.0,
        hours=(18,), cap=2),
    cfg("L21-3000-h18", arms="late_only", D_B=21, L_B=3000.0, hours=(18,)),
    cfg("L24-3000-h18", arms="late_only", D_B=24, L_B=3000.0, hours=(18,)),
    cfg("L15-5000-h18", arms="late_only", D_B=15, L_B=5000.0, hours=(18,)),
    cfg("L15-3000-h12", arms="late_only", D_B=15, L_B=3000.0, hours=(12,)),
    cfg("L15-3000-h12-cap2", arms="late_only", D_B=15, L_B=3000.0,
        hours=(12,), cap=2),
    cfg("L15-1500-h18-fall-cap2", arms="late_only", D_B=15, L_B=1500.0,
        hours=(18,), line_sel="falling", cap=2),
    cfg("L18-1500-h18-cap2", arms="late_only", D_B=18, L_B=1500.0,
        hours=(18,), cap=2),
    cfg("uni-A1000-B15-3000-h18", DD=1000.0, D_B=15, L_B=3000.0,
        hours=(18,)),
    cfg("uni-A1000-B15-3000-h18-cap2", DD=1000.0, D_B=15, L_B=3000.0,
        hours=(18,), cap=2),
    cfg("dd1000-h18", arms="dd_only", DD=1000.0, hours=(18,)),
    cfg("dd1000-h18-cap2", arms="dd_only", DD=1000.0, hours=(18,), cap=2),
    cfg("L15-3000-h18-cap8", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), cap=8),
    cfg("L15-3000-h18-cap2-noskip", arms="late_only", D_B=15, L_B=3000.0,
        hours=(18,), cap=2, skip_tape=False),
    cfg("L15-3000-h6-18", arms="late_only", D_B=15, L_B=3000.0,
        hours=(6, 18)),
    cfg("arms-none", arms="none"),
]

if __name__ == "__main__":
    with open("/tmp/mathsearch/baseline.json") as h:
        base = {g["ep"]: g["margin"] for g in json.load(h)["games"]}
    results, wall = run_configs(CONFIGS)
    table = []
    for r in results:
        deltas = {g["ep"]: round(g["margin"] - base[g["ep"]], 2)
                  for g in r["games"]}
        table.append({
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
                          for g in r["games"]}})
    out = {"wall_s": wall, "n_configs": len(CONFIGS), "table": table}
    with open("/tmp/mathsearch/phase3.json", "w") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    for row in sorted(table, key=lambda t: -t["dsum"]):
        print(f"{row['name']:28s} dsum={row['dsum']:9.1f} pos={row['pos']} "
              f"neg={row['neg']} armed={row['armed_games']:2d} "
              f"flips={row['flips']}")
    print("wall_s", wall)
