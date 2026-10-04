# -*- coding: utf-8 -*-
"""diag_seq：对手同拍 SELL 单序观测（判决辅助；不入证据主档）。

对 1 局打出双方逐拍 market 单序：统计对手同拍多 SELL 的品序稳定性
（'对手同拍 SELL 单序稳定可预测' 假设的实证检验）。
"""
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM
_spec.loader.exec_module(JM)
from orderbook_r40 import sim_bridge as sb  # noqa: E402

DROP = str(KSIM_DIR / "orderbook_unified_u2_lab" / "build" / "u2v2_drop_half"
           / "main.py")
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1825501814
SEAT = int(sys.argv[2]) if len(sys.argv) > 2 else 0
OPP = sys.argv[3] if len(sys.argv) > 3 else str(
    MODULE_DIR / "opponents" / "tetsu1009" / "main.py")


class Tracer:
    def __init__(self, inner, sink):
        self.inner, self.sink = inner, sink

    def __call__(self, obs, configuration=None):
        act = JM._call_inner(self.inner, obs, configuration)
        self.sink.append((JM._obs_step(obs), act))
        return act


def sells_seq(act):
    return tuple(str(o[1]) for o in (act.get("market") or [])
                 if isinstance(o, (list, tuple)) and len(o) >= 3
                 and o[0] == "SELL" and int(o[2] or 0) > 0)


def main():
    sinks = {0: [], 1: []}
    agents = []
    for pos, p in ((0, DROP), (1, OPP)):
        inner, _ = JM._load_agent(p)
        agents.append(Tracer(inner, sinks[pos]))
    if SEAT == 1:
        agents.reverse()
    res = sb.run_games([{"seed": SEED, "agents": agents}],
                       {"engine": "sim", "workers": 1})
    print("banks:", res["games"][0].get("banks"))
    opp_seat = 1 - SEAT
    ours, theirs = Counter(), Counter()
    multi_theirs = []
    first_item = Counter()
    for s in range(min(len(sinks[SEAT]), len(sinks[opp_seat]))):
        so = sells_seq(sinks[SEAT][s][1])
        st = sells_seq(sinks[opp_seat][s][1])
        if so:
            ours[so] += 1
        if st:
            theirs[st] += 1
            first_item[st[0]] += 1
            if len(st) >= 2:
                multi_theirs.append((sinks[SEAT][s][0], st))
    print("opp multi-sell ticks:", len(multi_theirs))
    for row in multi_theirs[:25]:
        print("  step", row[0], row[1])
    print("opp seq top:", theirs.most_common(8))
    print("opp first-item dist:", first_item.most_common())
    print("our seq top:", ours.most_common(8))


if __name__ == "__main__":
    main()
