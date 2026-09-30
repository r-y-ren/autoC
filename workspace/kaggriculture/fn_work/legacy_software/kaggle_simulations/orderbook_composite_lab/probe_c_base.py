#!/usr/bin/env python3
"""probe_c_base：C_base 双局连跑探针 P13（同进程 ep1 WFR -> ep2 镜像）。

断言：ep1 换表发生（闩 True + 443 触点变动）；ep2 边界复位后全程（含 144+ 锁存点）
零换表零闩（每拍 dirty==0、latch 恒 False），ep2_cls 实得镜像类（≠wfr）。
另附入口冒烟（P12 口径）。只读审计；用法: python3 probe_c_base.py [main_path]
-> evidence/c_base_probe_out.json
"""
import hashlib
import importlib.util
import json
import os
import sys
import traceback

LAB = os.path.dirname(os.path.abspath(__file__))
MAIN = (sys.argv[1] if len(sys.argv) > 1 else
        os.path.join(LAB, "build", "c_base", "main.py"))
TAG = os.path.basename(os.path.dirname(MAIN)) or MAIN
spec = importlib.util.spec_from_file_location("cbasemod", MAIN)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

OUT = {"probes": [], "anomaly": [], "artifact": MAIN,
       "artifact_sha256": hashlib.sha256(open(MAIN, "rb").read()).hexdigest()}


def rec(name, **kw):
    kw["probe"] = name
    OUT["probes"].append(kw)
    print("[probe]", name, "->", kw.get("verdict"))


def mk_obs(step, player=0, inv=None, prices=None, shed=None, shops=(),
           money0=1000.0, money1=1000.0, tiles=None):
    tl = tiles if tiles is not None else [[{}, {}], [{}, {}]]

    def farm(m):
        return {"money": m, "tiles": tl, "hands": [], "farmer": [0, 0],
                "unlocked_quadrants": [0, 1, 2, 3], "hires_today": 0}
    return {
        "step": step, "player": player,
        "farms": [farm(money0), farm(money1)],
        "market": {"inventory": dict(inv or {}), "prices": dict(prices or {}),
                   "params": {}},
        "town": {"unlocked_shops": list(shops)},
        "private": {"shed": dict(shed or {}), "seeds": {}, "inventories": []},
    }


rids = sorted(M._IMPL.chassis.routes.keys())
RID = rids[0]


def seed_native(player=0, step=0):
    M._IMPL.chassis.players[player] = {
        "last_step": step, "route": RID, "router_state": {}, "pending": {},
        "sell_state": {"due_step": -1, "suppress": {}}}


def tiles_same(n=8):
    row = [{"crop": c} for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")]
    return [list(row), list(row)]


def tiles_diff_own():
    return [[{"crop": c} for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")],
            [{"crop": "MELON"}, {"crop": "WHEAT"}, {"crop": "CARROT"},
             {"crop": "TOMATO"}]]


def tiles_diff_rival(sheep=0):
    tl = [[{"animal": "SHEEP"}] * sheep + [{"crop": "MELON"}] * (4 - sheep),
          [{"crop": "TOMATO"}, {"crop": "STRAWBERRY"}, {"crop": "WHEAT"},
           {"crop": "CARROT"}]]
    return tl


def fp_routes():
    return {rid: [json.dumps(a, sort_keys=True, default=str) for a in seq]
            for rid, seq in M._IMPL.chassis.routes.items()}


def fp_diff(a, b, min_step=0):
    return sum(1 for rid in a
               for i, (x, y) in enumerate(zip(a[rid], b.get(rid, [])))
               if i >= min_step and x != y)


def _delta_cells():
    routes = M._IMPL.chassis.routes
    cells = []
    for rid, seq in routes.items():
        mp = M._OC_C3_DELTA.get(str(rid)) or {}
        for s in mp:
            cells.append((rid, int(s)))
    return cells


_DELTA_CELLS = _delta_cells()


def delta_cells_sig():
    out = []
    routes = M._IMPL.chassis.routes
    for rid, i in _DELTA_CELLS:
        seq = routes.get(rid)
        if seq is None or i >= len(seq):
            out.append(None)
        else:
            out.append(json.dumps(seq[i], sort_keys=True, default=str))
    return out


# ============ P12 口径入口冒烟 ============
try:
    smoke = {}
    seed_native(0, 0)
    try:
        a = M._hs_agent(mk_obs(0))
        smoke["step0"] = "ok action=%r" % (str(a)[:120],)
    except Exception as e:
        smoke["step0"] = "raise %r" % (e,)
    seed_native(0, 350)
    try:
        a = M._hs_agent(mk_obs(350, inv={"MILK": 9950, "STRAWBERRY": 9950,
                                         "WOOL": 9950},
                               prices={"MILK": 220, "STRAWBERRY": 460,
                                       "WOOL": 590},
                               shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}))
        smoke["step350"] = "ok action=%r" % (str(a)[:120],)
    except Exception as e:
        smoke["step350"] = "raise %r" % (e,)
    smoke["entry_last_callable"] = \
        [v for v in vars(M).values() if callable(v)][-1].__name__
    rec("P12_entry_smoke", verdict="INFO", smoke=smoke)
except Exception as e:
    rec("P12_entry_smoke", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())

# ============ P13: 双局连跑（同进程 ep1 触发 C3 / ep2 镜像） ============
try:
    routes_pristine = fp_routes()
    pristine_sig = delta_cells_sig()
    M._OC_STATE.clear()
    try:
        M._OC_C3_SWAPPED[0] = False
        M._M13_C3_BACKUP[0] = None
    except Exception:
        pass
    seed_native(0, 0)
    # ep1：wfr 对手（rm1=3000, sim<=0.5, sheep>=3）-> 换局前触发 C3
    for s in range(0, 200):
        o = mk_obs(s, money0=1000.0, money1=3000.0, tiles=tiles_diff_own())
        if s in M._OC_SIM_STEPS:
            o["farms"][0]["tiles"] = tiles_diff_own()
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        if s == 143:
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        act = M._hs_agent(o)
    ep1_latch = list(M._OC_C3_SWAPPED)
    ep1_cls = M._OC_STATE[0].get("cls")
    ep1_mutated = fp_diff(routes_pristine, fp_routes(), min_step=100)
    ep1_ok = (ep1_latch == [True] and ep1_mutated > 0)
    # ep2：镜像对手（cd=0.1, sm=0.99 -> h1_mirror）同进程串跑
    ep2_trace = []
    for s in range(0, 200):
        o = mk_obs(s, money0=1000.0, money1=1000.1, tiles=tiles_diff_own())
        if s in M._OC_SIM_STEPS:
            tl = tiles_same()
            o["farms"][0]["tiles"] = [list(r) for r in tl]
            o["farms"][1]["tiles"] = [list(r) for r in tl]
        act = M._hs_agent(o)
        sig = delta_cells_sig()
        n_dirty = sum(1 for x, y in zip(pristine_sig, sig) if x != y)
        ep2_trace.append((s, list(M._OC_C3_SWAPPED), n_dirty))
    latch_during_ep2 = [t[1][0] for t in ep2_trace]
    mutated_during_ep2 = [t[2] for t in ep2_trace]
    ep2_cls = M._OC_STATE[0].get("cls")
    zero_latch = (not any(latch_during_ep2))
    zero_swap = (max(mutated_during_ep2 or [0]) == 0)
    rec("P13_dual_game_serial_zero_pollution",
        verdict="PASS" if (ep1_ok and zero_latch and zero_swap
                           and ep2_cls != "wfr") else "FAIL",
        ep1_cls=ep1_cls, ep1_latch=ep1_latch,
        ep1_entries_mutated=ep1_mutated, ep1_trigger_ok=ep1_ok,
        ep2_cls=ep2_cls, ep2_zero_latch=zero_latch, ep2_zero_swap=zero_swap,
        ep2_max_entries_mutated=max(mutated_during_ep2 or [0]),
        ep2_latch_true_ticks=sum(1 for x in latch_during_ep2 if x),
        ep2_delta_cells=len(_DELTA_CELLS),
        note="同进程 ep1 WFR 触发 C3 -> ep2 镜像（h1_mirror）：断言 ep2 零换表"
             "零闩（换局复位生效）；逐拍迹每拍 dirty==0")
except Exception as e:
    rec("P13_dual_game_serial_zero_pollution", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())

os.makedirs(os.path.join(LAB, "evidence"), exist_ok=True)
out_path = os.path.join(LAB, "evidence", "c_base_probe_out.json")
json.dump(OUT, open(out_path, "w"), indent=1, default=str)
n_pass = sum(1 for p in OUT["probes"]
             if str(p.get("verdict", "")).startswith(("PASS", "INFO")))
n_fail = sum(1 for p in OUT["probes"] if p.get("verdict") == "FAIL")
print("probes done: pass=%d fail=%d -> %s" % (n_pass, n_fail, out_path))
sys.exit(0 if n_fail == 0 else 1)
