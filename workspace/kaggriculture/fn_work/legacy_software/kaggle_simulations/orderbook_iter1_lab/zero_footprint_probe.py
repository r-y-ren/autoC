# -*- coding: utf-8 -*-
"""zero_footprint_probe：非触发拍零足迹逐拍验证（c3 补充仪器）。

方法：h1_base 对 r40 实跑取 (obs, act) 流（干净基座流），把 i1/i2 层函数
（从各注入形态装载命名空间取 _i1_post/_i2_post）逐拍回放同流，验证：
  ①层返回对象 is 输入动作对象 ⟺ 该拍台账未记 changed（零足迹拍恒等）；
  ②记 changed 的拍内容确实不同（不产生无谓拷贝）。
另附判决对折面 banks 恒等（judge_iter1.zero_footprint_check 主仪器）。
只写 orderbook_iter1_lab/evidence/ 与 /tmp。
"""
from __future__ import annotations

import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

H1_BASE = os.path.join(ROOT, "build", "h1_base", "main.py")
FORM_DIRS = {"i1": "i1", "i2": "i2", "i12": "i12"}
R40_MAIN = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
SEEDS = [1825501814, 841473039, 672000, 672029]


def _load_ns(path):
    ns = {}
    src = open(path, encoding="utf-8").read()
    exec(compile(src, path, "exec"), ns)
    return ns


def main():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    out = {"_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "version": "zero-footprint-probe/1.0", "seeds": list(SEEDS),
           "forms": {}}
    # ---- 基座流采集（h1_base 对 r40，官方引擎，双席追踪） ----
    streams = {}
    for seed in SEEDS:
        sinks = {0: [], 1: []}
        agents = []
        for seat, path in enumerate((H1_BASE, R40_MAIN)):
            entry = j23._load_entry(path)
            agents.append(j23._Tracer(entry, seat, sinks[seat]))
        sb.run_games([{"seed": seed, "agents": agents}], {"engine": "official"})
        streams[seed] = sinks[0]          # h1_base 席流
        print("stream", seed, len(sinks[0]), flush=True)

    # ---- 逐拍回放各形态层 ----
    for form, sub in FORM_DIRS.items():
        ns = _load_ns(os.path.join(ROOT, "build", sub, "main.py"))
        layers = [name for name in ("_i1_post", "_i2_post") if name in ns]
        total_ticks = same_ticks = changed_ticks = violations = spurious = 0
        per_seed = {}
        for seed, sink in streams.items():
            for name in ("_i1_reset", "_i2_reset"):
                if name in ns:
                    ns[name]()
            s_same = s_changed = s_viol = 0
            for (step, obs, act) in sink:
                if not isinstance(act, dict):
                    continue
                total_ticks += 1
                before = sum(int(ns[n].__globals__[n.replace("_post", "_REPORT")
                                                   .replace("_i1", "_I1")
                                                   .replace("_i2", "_I2")]
                                 .get("changed_turns", 0)) for n in layers)
                cur = act
                for n in layers:
                    cur = ns[n](obs, cur)
                after = sum(int(ns[n].__globals__[n.replace("_post", "_REPORT")
                                                  .replace("_i1", "_I1")
                                                  .replace("_i2", "_I2")]
                                .get("changed_turns", 0)) for n in layers)
                counted = after > before
                identical_obj = (cur is act)
                if identical_obj and not counted:
                    same_ticks += 1
                    s_same += 1
                elif (not identical_obj) and counted:
                    changed_ticks += 1
                    s_changed += 1
                    if cur == act:
                        spurious += 1        # 记了改动但内容相同=无谓拷贝
                else:
                    violations += 1
                    s_viol += 1
            per_seed[str(seed)] = {"same": s_same, "changed": s_changed,
                                   "violations": s_viol}
        out["forms"][form] = {
            "layers": layers,
            "total_ticks": total_ticks,
            "zero_footprint_ticks": same_ticks,
            "changed_ticks": changed_ticks,
            "violations": violations,
            "spurious_copies": spurious,
            "per_seed": per_seed,
            "passed": violations == 0,
        }
        print(form, out["forms"][form], flush=True)
    out["overall_passed"] = all(v["passed"] for v in out["forms"].values())
    path = os.path.join(ROOT, "evidence", "zero_footprint_probe.json")
    open(path, "w").write(json.dumps(out, ensure_ascii=False, indent=1,
                                     default=str) + "\n")
    print("->", path, flush=True)


if __name__ == "__main__":
    main()
