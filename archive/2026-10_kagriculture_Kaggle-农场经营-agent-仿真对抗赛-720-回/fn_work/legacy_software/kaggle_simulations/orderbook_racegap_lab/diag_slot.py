# -*- coding: utf-8 -*-
"""diag_slot：slot 臂单局诊断（判决辅助；不入证据主档）。

同 (seed,seat,opp) 跑 drop_half 与 slot 臂，逐拍比对我席动作流：
找出首个差异拍，输出两侧 market 槽位/单重集、分品成交读数、RGS 台账，
判定差异是重排本身还是执行崩坏（abort/洗仓腿/量漂移）。
"""
import hashlib
import importlib.util
import json
import sys
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
SLOT = str(MODULE_DIR / "build" / "slot" / "main.py")
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1825501814
SEAT = int(sys.argv[2]) if len(sys.argv) > 2 else 0
OPP = sys.argv[3] if len(sys.argv) > 3 else str(
    MODULE_DIR / "opponents" / "tetsu1009" / "main.py")


class Tracer:
    def __init__(self, inner, seat, sink):
        self.inner, self.seat, self.sink = inner, seat, sink

    def __call__(self, obs, configuration=None):
        act = JM._call_inner(self.inner, obs, configuration)
        self.sink.append((JM._obs_step(obs), JM._obs_dict(obs), act))
        return act


def run(path):
    sinks = {0: [], 1: []}
    agents = []
    for seat, p in ((0, path), (1, OPP)):
        inner, _ = JM._load_agent(p)
        agents.append(Tracer(inner, seat, sinks[seat]))
    if SEAT == 1:
        agents.reverse()
    res = sb.run_games([{"seed": SEED, "agents": agents}],
                       {"engine": "sim", "workers": 1})
    return res["games"][0], sinks


def main():
    ga, sa = run(DROP)
    gb, sb_ = run(SLOT)
    print("banks drop_half:", ga.get("banks"), " slot:", gb.get("banks"))
    for tag, g in (("drop_half", ga), ("slot", gb)):
        print(tag, "margin", g.get("banks"))
    # 首个差异拍
    diffs = []
    for s in range(max(len(sa[SEAT]), len(sb_[SEAT]))):
        a = sa[SEAT][s][2] if s < len(sa[SEAT]) else None
        b = sb_[SEAT][s][2] if s < len(sb_[SEAT]) else None
        if json.dumps(a, sort_keys=True, default=str) != \
                json.dumps(b, sort_keys=True, default=str):
            diffs.append(s)
    print("n_diff_steps:", len(diffs), "first:", diffs[:12])
    for s in diffs[:6]:
        a, b = sa[SEAT][s][2], sb_[SEAT][s][2]
        print("== step", s)
        print("  drop market:", a.get("market"))
        print("  slot  market:", b.get("market"))
        ka = sorted((str(o[0]), str(o[1]), o[2]) for o in (a.get("market") or [])
                    if isinstance(o, (list, tuple)) and len(o) >= 3)
        kb = sorted((str(o[0]), str(o[1]), o[2]) for o in (b.get("market") or [])
                    if isinstance(o, (list, tuple)) and len(o) >= 3)
        print("  multiset equal:", ka == kb)
    # RGS 台账
    for tag, sink in (("drop_half", sa), ("slot", sb_)):
        led = {}
        for entry in sink[SEAT]:
            tel = entry[2].get("market") if isinstance(entry[2], dict) else None
        print(tag, "steps:", len(sink[SEAT]))
    # 分品成交：影子引擎
    for tag, sink in (("drop_half", sa), ("slot", sb_)):
        sw = JM.shadow_window(sink, SEED)
        acc = sw.get("per_item_by_seat", {}).get(SEAT, {})
        print(tag, "per_item filled/value:",
              {k: (v["filled"], round(v["value"], 1)) for k, v in acc.items()})
        er = JM.end_reads(sink[SEAT])
        print(tag, "end:", {k: er.get(k) for k in
                            ("terminal_money", "stranding")})


if __name__ == "__main__":
    main()
