# -*- coding: utf-8 -*-
"""Phase 1：触发轴粗网格（排程=v2 默认）。"""
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


CONFIGS = []
# -- 臂组合隔离 ------------------------------------------------------------
CONFIGS.append(cfg("arm-dd-only", arms="dd_only"))
CONFIGS.append(cfg("arm-late-only", arms="late_only"))
# -- A 臂（回撤臂）OFAT ----------------------------------------------------
for v in (18, 21, 24):
    CONFIGS.append(cfg(f"A-D{v}", D_A=v))
for v in (1000.0, 3000.0):
    CONFIGS.append(cfg(f"A-DD{int(v)}", DD=v))
for v in (3000.0, 5000.0):
    CONFIGS.append(cfg(f"A-L{int(v)}", L_A=v))
# -- B 臂（终局臂）OFAT ----------------------------------------------------
for v in (15, 18, 21):
    CONFIGS.append(cfg(f"B-D{v}", D_B=v))
for v in (1500.0, 5000.0):
    CONFIGS.append(cfg(f"B-L{int(v)}", L_B=v))
# -- 组合探针：早触发宽保护 --------------------------------------------------
CONFIGS.append(cfg("late-only-15-1500", arms="late_only", D_B=15, L_B=1500.0))
CONFIGS.append(cfg("late-only-15-3000", arms="late_only", D_B=15, L_B=3000.0))
CONFIGS.append(cfg("late-only-18-1500", arms="late_only", D_B=18, L_B=1500.0))
CONFIGS.append(cfg("uni-B15-1500", D_B=15, L_B=1500.0))
CONFIGS.append(cfg("uni-B18-1500", D_B=18, L_B=1500.0))
CONFIGS.append(cfg("dd-only-DD1000-D15", arms="dd_only", DD=1000.0))
CONFIGS.append(cfg("dd-only-DD1000-D18", arms="dd_only", DD=1000.0, D_A=18))
CONFIGS.append(cfg("uni-A1000-B15-1500", DD=1000.0, D_B=15, L_B=1500.0))
CONFIGS.append(cfg("uni-A3000-5k-B24-5k", L_A=5000.0, DD=3000.0, L_B=5000.0))

if __name__ == "__main__":
    with open("/tmp/mathsearch/baseline.json") as h:
        base = {g["ep"]: g["margin"] for g in json.load(h)["games"]}
    results, wall = run_configs(CONFIGS)
    table = []
    for r in results:
        deltas = {g["ep"]: round(g["margin"] - base[g["ep"]], 2)
                  for g in r["games"]}
        armed = sum(1 for g in r["games"] if g["armed_frames"] > 0)
        table.append({
            "name": r["cfg"]["name"], "dsum": round(sum(deltas.values()), 2),
            "pos": sum(1 for v in deltas.values() if v > 0),
            "neg": sum(1 for v in deltas.values() if v < 0),
            "armed_games": armed,
            "flips": sum(1 for g in r["games"] if g["margin"] > 0),
            "deltas": deltas,
            "margins": {g["ep"]: g["margin"] for g in r["games"]},
            "telemetry": {g["ep"]: {k: g[k] for k in
                                    ("armed_frames", "emit_frames",
                                     "emit_units", "first_armed_step")}
                          for g in r["games"]}})
    out = {"wall_s": wall, "n_configs": len(CONFIGS), "table": table}
    with open("/tmp/mathsearch/phase1.json", "w") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    for row in sorted(table, key=lambda t: -t["dsum"]):
        print(f"{row['name']:24s} dsum={row['dsum']:9.1f} pos={row['pos']} "
              f"neg={row['neg']} armed={row['armed_games']:2d} "
              f"flips={row['flips']}")
    print("wall_s", wall)
