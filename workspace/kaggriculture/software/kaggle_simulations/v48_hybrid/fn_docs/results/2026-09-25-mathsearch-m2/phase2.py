# -*- coding: utf-8 -*-
"""Phase 2：排程轴 OFAT（双锚点：v2 默认触发 + phase1 最优触发）。"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/tmp/mathsearch")
import psearch as ps
from runner import run_configs

D = dict(ps.DEFAULT_CFG)
ABSORB = ps.HOURS_ABSORB

TRIGGERS = {
    "v2": {},                                   # v2 默认
    "best1": {"arms": "late_only", "D_B": 15, "L_B": 3000.0},  # phase1 最优
}


def cfg(name, trig, **kw):
    c = dict(D)
    c.update(TRIGGERS[trig])
    c.update(kw)
    c["name"] = name
    return c


CONFIGS = []
for t in ("v2", "best1"):
    CONFIGS.append(cfg(f"{t}-falling", t, line_sel="falling"))
    CONFIGS.append(cfg(f"{t}-high", t, line_sel="high"))
    CONFIGS.append(cfg(f"{t}-cap2", t, cap=2))
    CONFIGS.append(cfg(f"{t}-cap8", t, cap=8))
    CONFIGS.append(cfg(f"{t}-cap13", t, cap=13))
    CONFIGS.append(cfg(f"{t}-h6", t, hours=(6,)))
    CONFIGS.append(cfg(f"{t}-h18", t, hours=(18,)))
    CONFIGS.append(cfg(f"{t}-absorb", t, hours=ABSORB))
    CONFIGS.append(cfg(f"{t}-noskip", t, skip_tape=False))
    CONFIGS.append(cfg(f"{t}-high-cap13", t, line_sel="high", cap=13))
    CONFIGS.append(cfg(f"{t}-falling-cap2", t, line_sel="falling", cap=2))
    CONFIGS.append(cfg(f"{t}-absorb-cap2", t, hours=ABSORB, cap=2))

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
    with open("/tmp/mathsearch/phase2.json", "w") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    for row in sorted(table, key=lambda t: -t["dsum"]):
        print(f"{row['name']:24s} dsum={row['dsum']:9.1f} pos={row['pos']} "
              f"neg={row['neg']} armed={row['armed_games']:2d} "
              f"flips={row['flips']}")
    print("wall_s", wall)
