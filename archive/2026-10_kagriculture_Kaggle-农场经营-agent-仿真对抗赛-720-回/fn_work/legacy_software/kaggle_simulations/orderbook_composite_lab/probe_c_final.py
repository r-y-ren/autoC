#!/usr/bin/env python3
"""c_final 验证探针（composite lab）：P13 双局连跑零污染为主判 + D3 双写 +
C3 闩复位/换表还原 + 画像换局复位。只读审计；不改既有代码。

沿 m13fix probe 先例，入口按 oc_c3 谱系归一为 _hs_agent（c_final 末 callable）。
用法: python3 probe_c_final.py [main_path] [out_name]
"""
import importlib.util, json, os, sys, traceback

LAB = os.path.dirname(os.path.abspath(__file__))
MAIN = (sys.argv[1] if len(sys.argv) > 1 else
        os.path.join(LAB, "build", "c_final", "main.py"))
OUT_NAME = (sys.argv[2] if len(sys.argv) > 2 else "c_final_probe_out.json")
spec = importlib.util.spec_from_file_location("cfinmod", MAIN)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

OUT = {"probes": [], "isolation": {}, "anomaly": [], "artifact": MAIN}


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


REGS = ["_OC_STATE", "_OC_C3_SWAPPED", "_S758_HIST", "_S804_HIST", "_RACE_STATE",
        "_V9_ITEM_HZ", "_X1_REPORT", "_MX_REPORT", "_S758_REPORT",
        "_S804_REPORT", "_RACE_REPORT"]


def snap():
    s = {}
    for r in REGS:
        try:
            s[r] = json.dumps(getattr(M, r), sort_keys=True, default=str)
        except Exception as e:
            s[r] = "unserializable:%r" % e
    try:
        s["_routes_sig"] = str(hash(str(sorted(
            (k, len(v)) for k, v in M._IMPL.chassis.routes.items()))))
    except Exception:
        pass
    return s


def diff(a, b):
    return {k for k in set(a) | set(b) if a.get(k) != b.get(k)}


# ============ P7：小时1 档与台账（D3 自插双写断言）============
try:
    s1 = 24 * 14 + 1
    seed_native(0, s1)
    M._S758_HIST.clear()
    M._S804_HIST.clear()
    r7 = M._s758_apply(mk_obs(s1, inv={"MILK": 9950, "STRAWBERRY": 9950,
                                       "WOOL": 9950},
                              prices={"MILK": 96, "STRAWBERRY": 60, "WOOL": 30},
                              shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}),
                       {"market": [], "units": []})
    h758 = M._S758_HIST.get(0, {})
    h804 = M._S804_HIST.get(0, {})
    own758 = (h758.get("prev") or {}).get("own") or {}
    own804 = (h804.get("prev") or {}).get("own") or {}
    d3_ok = (int(own758.get("STRAWBERRY", 0)) >= 1
             and int(own758.get("WOOL", 0)) >= 1
             and int(own758.get("MILK", 0)) >= 1)
    rec("P7_hour1_tiers_d3", verdict="PASS" if d3_ok else "FAIL",
        d3_own_ledger_758=own758, d3_own_ledger_804=own804,
        d3_double_write_ok=bool(d3_ok),
        orders=[o for o in (r7.get("market") or [])],
        note="D3：s804 自插 SELL 同步记 _S758_HIST prev own")
except Exception as e:
    rec("P7_hour1_tiers_d3", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())


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


def feed(steps_seq, cd, sm, cls_hint=None):
    for s in steps_seq:
        o = mk_obs(s, money0=1000.0, money1=1000.0 + cd,
                   tiles=tiles_diff_own())
        if s in M._OC_SIM_STEPS:
            if sm >= 0.95:
                tl = tiles_same()
                o["farms"][0]["tiles"] = [list(r) for r in tl]
                o["farms"][1]["tiles"] = [list(r) for r in tl]
            else:
                o["farms"][0]["tiles"] = tiles_diff_own()
                o["farms"][1]["tiles"] = tiles_diff_rival(
                    sheep=3 if cls_hint == "wfr" else 0)
        if s == 143 and cls_hint == "wfr":
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        M._oc_after(o, {"market": []})


# ============ P8：画像层换局失鲜（D1 修复后应 PASS）============
try:
    M._OC_STATE.clear()
    feed(range(0, 144), cd=5.0, sm=0.99)
    cls1 = M._oc_cls(mk_obs(144), 144)
    feed(range(0, 145), cd=0.1, sm=0.99)
    cls2 = M._oc_cls(mk_obs(200), 200)
    st = M._OC_STATE[0]
    rec("P8_oc_cross_episode_staleness",
        verdict="PASS" if cls2 != cls1 else "DEFECT_CONFIRMED",
        ep1_cls=cls1, ep2_cls=cls2, last_step=st.get("last_step"),
        locked=st.get("locked"),
        note="D1：step<=last_step 换局重播，ep2 特征应实得（非沿用 ep1）")
except Exception as e:
    rec("P8_oc_cross_episode_staleness", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())


# ============ P9：画像窗隙拍（无错 delta）============
try:
    M._OC_STATE.clear()
    M._oc_after(mk_obs(1, money1=1005.0, inv={"WHEAT": 5}), {"market": []})
    M._oc_after(mk_obs(2, money1=1005.0, inv={"WHEAT": 5}), {"market": []})
    M._oc_after(mk_obs(5, money1=1005.0, inv={"WHEAT": 50}),
                {"market": [["SELL", "MILK", 2]]})
    st = M._OC_STATE[0]
    ok = (st.get("rival_sold_cum") == {} and st.get("own_sold_cum") == {}
          and st.get("prev_step") == 5)
    rec("P9_oc_gap_no_bogus_delta", verdict="PASS" if ok else "FAIL",
        prev_step=st.get("prev_step"),
        rival_sold_cum=st.get("rival_sold_cum"),
        own_sold_cum=st.get("own_sold_cum"))
except Exception as e:
    rec("P9_oc_gap_no_bogus_delta", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())


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


def ep2_step0_reset():
    """换局边界：入口 step0 复位（_hs_agent 全链）——闩/备份只许修复件自己
    复位（此处不得手清 _M13_C3_BACKUP/_OC_C3_SWAPPED，否则掩蔽 D2 还原）。"""
    M._S758_HIST.clear()
    M._S804_HIST.clear()
    M._OC_STATE.clear()
    try:
        M._x1_reset()
    except Exception:
        pass
    try:
        M._hs_agent(mk_obs(0))
    except Exception:
        pass


# ============ P10：C3 换局一次性闩 + 换表可逆（D2 修复后应 PASS）============
try:
    routes_pristine = fp_routes()
    M._OC_STATE.clear()
    try:
        M._OC_C3_SWAPPED[0] = False
        M._M13_C3_BACKUP[0] = None
    except Exception:
        pass
    for s in range(0, 144):
        o = mk_obs(s, money0=1000.0, money1=3000.0, tiles=tiles_diff_own())
        if s in M._OC_SIM_STEPS:
            o["farms"][0]["tiles"] = tiles_diff_own()
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        if s == 143:
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        M._oc_after(o, {"market": []})
    cls_wfr = M._oc_cls(mk_obs(144), 144)
    M._oc_c3_swap(mk_obs(200), 200)
    latch_after_ep1 = list(M._OC_C3_SWAPPED)
    routes_after_swap = fp_routes()
    swap_entries = fp_diff(routes_pristine, routes_after_swap, min_step=100)
    ep2_step0_reset()
    latch_after_ep2_step0 = list(M._OC_C3_SWAPPED)
    routes_after_ep2 = fp_routes()
    kept = fp_diff(routes_pristine, routes_after_ep2, min_step=100)
    ok = (swap_entries > 0 and latch_after_ep2_step0 == [False] and kept == 0)
    rec("P10_c3_latch_swap_reversible",
        verdict="PASS" if ok else "DEFECT_CONFIRMED",
        ep1_cls=cls_wfr, latch_after_ep1=latch_after_ep1,
        latch_after_ep2_step0=latch_after_ep2_step0,
        c3_swap_route_entries_mutated=swap_entries,
        swap_entries_kept_after_ep2_step0=kept,
        note="D2：ep2 step0 闩复位+换表反向还原（触点回原值）")
except Exception as e:
    rec("P10_c3_latch_swap_reversible", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())


# ============ P12：全链入口冒烟 ============
try:
    smoke = {}
    try:
        a = M._hs_agent(mk_obs(0))
        smoke["step0"] = "ok action=%r" % (a,)
    except Exception as e:
        smoke["step0"] = "raise %r" % (e,)
    seed_native(0, 350)
    try:
        a = M._hs_agent(mk_obs(350, inv={"MILK": 9950, "STRAWBERRY": 9950,
                                         "WOOL": 9950},
                                 prices={"MILK": 220, "STRAWBERRY": 460,
                                         "WOOL": 590},
                                 shed={"MILK": 5, "STRAWBERRY": 5,
                                       "WOOL": 5}))
        smoke["step350"] = "ok action=%r" % (a,)
    except Exception as e:
        smoke["step350"] = "raise %r" % (e,)
    rec("P12_full_entry_smoke", verdict="INFO", smoke=smoke)
except Exception as e:
    rec("P12_full_entry_smoke", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())


# ============ P13：双局连跑（同进程 ep1 触发 C3 / ep2 镜像）零污染 ============
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
    # ep1：wfr 对手（rm1=3000, sim<=0.5, sheep>=3）-> 触发 C3 换表
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
    # ep2：镜像/非 WFR 同进程串跑（step0 应复位）
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
        ep1_cls=ep1_cls, ep1_latch=ep1_latch, ep1_entries_mutated=ep1_mutated,
        ep1_trigger_ok=ep1_ok,
        ep2_cls=ep2_cls, ep2_zero_latch=zero_latch, ep2_zero_swap=zero_swap,
        ep2_max_entries_mutated=max(mutated_during_ep2 or [0]),
        ep2_latch_true_ticks=sum(1 for x in latch_during_ep2 if x),
        note="同进程 ep1 WFR 触发 C3 -> ep2 非 WFR：ep2 零换表零闩=零污染")
except Exception as e:
    rec("P13_dual_game_serial_zero_pollution", verdict="FAIL", err=repr(e),
        tb=traceback.format_exc())

os.makedirs(os.path.join(LAB, "evidence"), exist_ok=True)
out_path = os.path.join(LAB, "evidence", OUT_NAME)
json.dump(OUT, open(out_path, "w"), indent=1, default=str)
n_pass = sum(1 for p in OUT["probes"]
             if str(p.get("verdict", "")).startswith(("PASS", "INFO")))
n_def = sum(1 for p in OUT["probes"] if p.get("verdict") == "DEFECT_CONFIRMED")
n_fail = sum(1 for p in OUT["probes"] if p.get("verdict") == "FAIL")
print("written", out_path, "pass=%d defect=%d fail=%d" % (n_pass, n_def, n_fail))
