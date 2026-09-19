# 【中文】round23_dtsp_stepdiff_probe.py —— 逐步动作指纹接合判定（无反事实）
# ===========================================================================
# 原理：官方回放逐步记录了我方真实提交动作。把回放的 obs 原样喂给纯
#   v13.8 agent（与 main.py 同语义 exec 装载），逐步比对动作流：
#     * 匹配率≈100% → 该局线上就是纯 v13.8（DTSP 未改变任何动作）
#     * 出现稳定不匹配段 → DTSP 覆盖生效（计划改写了动作）
#   本口径零反事实（不用孪生重演、不引入对手轨迹失配），是接合判定的
#   最强证据；agent 确定性由旗关黄金逐字节测试背书。
# 输出：逐局匹配率 + 不匹配步定位（首个不匹配步/不匹配日分布）。
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402

REPLAY_DIR = os.path.join(SOFTWARE, "..", "references", "data",
                          "online-replays", "round23")
OUT = os.path.join(SOFTWARE, "exports", "probes", "round23_forensics",
                   "dtsp_stepdiff.json")
TEAM = "renyxin"


def norm_action(a):
    """动作结构规范化（list/dict 递归排序键，浮点定格）→ 可哈希串。"""
    if isinstance(a, (list, tuple)):
        return "[" + ",".join(norm_action(x) for x in a) + "]"
    if isinstance(a, dict):
        return "{" + ",".join(
            f"{k}:{norm_action(a[k])}" for k in sorted(a)) + "}"
    if isinstance(a, float):
        return f"{a:.4f}"
    return json.dumps(a, ensure_ascii=False, sort_keys=True)


def main():
    files = sorted(f for f in os.listdir(REPLAY_DIR)
                   if f.startswith("episode-") and f.endswith(".json"))
    rows = []
    for fn in files:
        # 每局全新命名空间（对齐官方每局独立进程语义；防跨局内部态污染）
        ns, _applied, _skipped = bench.build_v13_namespace(None)
        agent_fn = ns["agent"]
        with open(os.path.join(REPLAY_DIR, fn), "r", encoding="utf-8") as h:
            replay = json.load(h)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        if TEAM not in teams or teams[0] == teams[1]:
            continue
        me = teams.index(TEAM)
        steps = replay["steps"]
        total = match = 0
        first_mm = None
        mm_days = Counter()
        for t in range(len(steps) - 1):
            entry = steps[t + 1][me] if isinstance(steps[t + 1], list) \
                else steps[t + 1].get(str(me))
            online = (entry or {}).get("action")
            obs = steps[t][me].get("observation") if isinstance(
                steps[t], list) else steps[t].get(str(me), {}).get(
                "observation")
            if obs is None:
                continue
            mine = agent_fn(obs)
            total += 1
            if norm_action(mine) == norm_action(online):
                match += 1
            else:
                day = (obs.get("day") if isinstance(obs, dict)
                       else getattr(obs, "day", t // 24)) or t // 24
                mm_days[day] += 1
                if first_mm is None:
                    first_mm = {"step": t, "day": day}
        rate = match / total if total else 0.0
        rows.append({"episode": fn, "match_rate": round(rate, 4),
                     "n_steps": total, "first_mismatch": first_mm,
                     "mismatch_days": dict(mm_days)})
        print(f"{fn}: match {match}/{total} = {rate:.1%} "
              f"first_mm={first_mm} days={dict(sorted(mm_days.items())[:8])}")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(rows, h, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
