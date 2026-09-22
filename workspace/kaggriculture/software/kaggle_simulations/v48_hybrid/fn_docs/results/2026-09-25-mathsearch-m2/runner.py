# -*- coding: utf-8 -*-
"""并行 runner：fork 池，每 task 一配置（或基线），复用父进程引擎缓存。"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, "/tmp/mathsearch")
import psearch as ps  # noqa: E402


def _task(cfg):
    return ps.eval_config(cfg)


def _baseline_task(_):
    return ps.eval_baseline()


def warm():
    """父进程预热引擎/回放缓存（fork 后继承）。"""
    g = ps.GAMES[0]
    rep = ps.get_replay(g["ep"])
    deps = ps.rro.make_twin_deps()
    state = deps["build"](rep, g["inject"])
    del state


def run_configs(configs, workers=14):
    warm()
    results = []
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(_task, configs):
            res["wall_s"] = None
            results.append(res)
    return results, round(time.perf_counter() - t0, 1)


def run_baseline(workers=1):
    warm()
    t0 = time.perf_counter()
    out = ps.eval_baseline()
    out["wall_s"] = round(time.perf_counter() - t0, 1)
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "baseline":
        out = run_baseline()
        with open("/tmp/mathsearch/baseline.json", "w") as h:
            json.dump(out, h, ensure_ascii=False, indent=1)
        print(json.dumps(out, ensure_ascii=False))
    elif mode == "validate":
        out, wall = run_configs([ps.DEFAULT_CFG])
        out[0]["wall_s"] = wall
        with open("/tmp/mathsearch/validate.json", "w") as h:
            json.dump(out[0], h, ensure_ascii=False, indent=1)
        print(json.dumps({"margins": [g["margin"] for g in out[0]["games"]],
                          "wall_s": wall}))
