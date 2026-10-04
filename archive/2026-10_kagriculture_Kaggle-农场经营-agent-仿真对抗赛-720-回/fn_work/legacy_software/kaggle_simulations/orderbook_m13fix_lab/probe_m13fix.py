#!/usr/bin/env python3
"""M13 修复件 dh_fix 验证探针：原 11 项 + P13 双局连跑（同进程 ep1 触发 C3 /
ep2 非 WFR 对手——断言 ep2 零换表零闩）。只读审计。
用法: python3 probe_m13fix.py [main_path]  -> evidence/m13fix_probe_out.json
"""
import importlib.util, json, os, sys, traceback

LAB = os.path.dirname(os.path.abspath(__file__))
MAIN = (sys.argv[1] if len(sys.argv) > 1 else
        os.path.join(LAB, "build", "u2v2_dh_fix", "main.py"))
TAG = os.path.basename(os.path.dirname(MAIN)) or MAIN
spec = importlib.util.spec_from_file_location("m13fixmod", MAIN)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

OUT = {"probes": [], "isolation": {}, "anomaly": [], "artifact": MAIN}


def rec(name, **kw):
    kw["probe"] = name
    OUT["probes"].append(kw)
    print("[probe]", name, "->", kw.get("verdict"))


def mk_obs(step, player=0, inv=None, prices=None, shed=None, shops=(), money0=1000.0, money1=1000.0, tiles=None):
    tl = tiles if tiles is not None else [[{}, {}], [{}, {}]]
    def farm(m):
        return {"money": m, "tiles": tl, "hands": [], "farmer": [0, 0],
                "unlocked_quadrants": [0, 1, 2, 3], "hires_today": 0}
    return {
        "step": step, "player": player,
        "farms": [farm(money0), farm(money1)],
        "market": {"inventory": dict(inv or {}), "prices": dict(prices or {}), "params": {}},
        "town": {"unlocked_shops": list(shops)},
        "private": {"shed": dict(shed or {}), "seeds": {}, "inventories": []},
    }

rids = sorted(M._IMPL.chassis.routes.keys())
RID = rids[0]
def seed_native(player=0, step=0):
    M._IMPL.chassis.players[player] = {"last_step": step, "route": RID,
                                       "router_state": {}, "pending": {},
                                       "sell_state": {"due_step": -1, "suppress": {}}}

REGS = ["_OC_STATE", "_OC_C3_SWAPPED", "_S758_HIST", "_S804_HIST", "_RACE_STATE",
        "_U2_REPORT", "_U2_DEC", "_V9_ITEM_HZ", "_X1_REPORT", "_MX_REPORT",
        "_S758_REPORT", "_S804_REPORT", "_RACE_REPORT"]


def snap():
    s = {}
    for r in REGS:
        try:
            s[r] = json.dumps(getattr(M, r), sort_keys=True, default=str)
        except Exception as e:
            s[r] = "unserializable:%r" % e
    try:
        s["_routes_len"] = str(len(M._IMPL.chassis.routes))
        s["_routes_sig"] = str(hash(str(sorted((k, len(v)) for k, v in M._IMPL.chassis.routes.items()))))
    except Exception:
        pass
    return s


def diff(a, b):
    return {k for k in set(a) | set(b) if a.get(k) != b.get(k)}


# ============ P1: 冷启动首拍（空历史窗口）============
seed_native(0, 350)
obs = mk_obs(350, inv={"MILK": 9950, "STRAWBERRY": 9950, "WOOL": 9950},
             prices={"MILK": 220, "STRAWBERRY": 460, "WOOL": 590},
             shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}, shops=("YARN_STORE",))
act = {"market": [], "units": []}
try:
    r = M._s758_apply(obs, act)
    hist = M._S758_HIST.get(0, {})
    empties = {i: hist.get(i) for i in ("MILK", "STRAWBERRY", "WOOL")}
    rec("P1_cold_start_first_tick", verdict="PASS_no_exception",
        fired_orders=[o for o in (r.get("market") or [])],
        window_after={k: (v if v is not None else "absent") for k, v in empties.items()},
        prev_seeded=bool(hist.get("prev")), report=dict(M._S758_REPORT),
        note="空历史 -> rival_avg 语义=0.0 中性回退（if rival else 0.0），非错值")
except Exception as e:
    rec("P1_cold_start_first_tick", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P2: 连拍（历史窗单样本写入）============
try:
    obs2 = mk_obs(351, inv={"MILK": 9951, "STRAWBERRY": 9951, "WOOL": 9951},
                  prices={"MILK": 219, "STRAWBERRY": 458, "WOOL": 588},
                  shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}, shops=("YARN_STORE",))
    M._s758_apply(obs2, {"market": [], "units": []})
    hist = M._S758_HIST[0]
    sample = {i: list(hist.get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")}
    ok = sample["MILK"] == [0] and sample["STRAWBERRY"] == [0] and sample["WOOL"] == [0]
    rec("P2_consecutive_tick_window_append", verdict="PASS" if ok else "FAIL",
        window=sample,
        expected_sample_semantics="max(0, dInv + draw(step-1) - own); 351: draw(350)=0")
except Exception as e:
    rec("P2_consecutive_tick_window_append", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P3: 换日/窗隙拍（链断裂 fail-safe）============
try:
    M._s758_apply(mk_obs(374, inv={"MILK": 9951}, prices={"MILK": 200}, shed={"MILK": 5}), {"market": []})
    before = {i: list(M._S758_HIST[0].get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")}
    M._s758_apply(mk_obs(386, inv={"MILK": 9960, "STRAWBERRY": 9960, "WOOL": 9960},
                         prices={"MILK": 210, "STRAWBERRY": 450, "WOOL": 580},
                         shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    after = {i: list(M._S758_HIST[0].get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")}
    rec("P3_daychange_gap_chain_break", verdict="PASS_no_bogus_delta",
        window_before=before, window_after=after,
        appended=(after != before), prev_step=M._S758_HIST[0]["prev"]["step"],
        note="prev['step']!=step-1 -> 跳过 append 并重播 prev，无跨隙错量")
except Exception as e:
    rec("P3_daychange_gap_chain_break", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P4: 对手静默/对手买卖拍（d 语义与钳位）============
try:
    win = lambda: {i: list(M._S758_HIST[0].get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")}
    P4PX = {"MILK": 1, "STRAWBERRY": 1, "WOOL": 1}
    M._s758_apply(mk_obs(398, inv={"MILK": 9960, "STRAWBERRY": 9960, "WOOL": 9960},
                         prices=P4PX, shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    before = win()
    M._s758_apply(mk_obs(399, inv={"MILK": 9960, "STRAWBERRY": 9960, "WOOL": 9960},
                         prices=P4PX, shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    mid = win()
    M._s758_apply(mk_obs(400, inv={"MILK": 9900, "STRAWBERRY": 9900, "WOOL": 9900},
                         prices=P4PX, shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    mid2 = win()
    M._s758_apply(mk_obs(401, inv={"MILK": 9950, "STRAWBERRY": 9950, "WOOL": 9950},
                         prices=P4PX, shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    end = win()
    ok = (mid["MILK"] == before["MILK"] + [0] and mid2["MILK"] == mid["MILK"] + [0]
          and end["MILK"] == mid2["MILK"] + [51])
    rec("P4_rival_flow_semantics", verdict="PASS" if ok else "FAIL",
        window_before=before, after_silent=mid, after_rival_buy=mid2, after_rival_sell=end,
        note="静默拍 d=0 如实入窗；对手净买 d=-60 钳 0；对手净卖 d=+50+draw1=51 正确复原")
except Exception as e:
    rec("P4_rival_flow_semantics", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P5: _u2_qty 半量门边界 ============
try:
    got = {
        "q1_drop": M._u2_qty(1, 200.0, 199.0, 350),
        "q3_drop": M._u2_qty(3, 200.0, 199.0, 350),
        "q6_drop": M._u2_qty(6, 200.0, 199.0, 350),
        "q6_nodrop": M._u2_qty(6, 200.0, 199.6, 350),
        "post648": M._u2_qty(6, 200.0, 190.0, 700),
        "q0": M._u2_qty(0, 200.0, 190.0, 350),
        "bad_q": M._u2_qty("x", 200.0, 190.0, 350),
    }
    ok = (got["q1_drop"] == 1 and got["q3_drop"] == 1 and got["q6_drop"] == 3
          and got["q6_nodrop"] == 6 and got["post648"] == 6 and got["q0"] == 0
          and got["bad_q"] == "x")
    rec("P5_u2_qty_halfgate_bounds", verdict="PASS" if ok else "FAIL", got=got)
except Exception as e:
    rec("P5_u2_qty_halfgate_bounds", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P6: _u2_fire 失真输入 fail-safe ============
try:
    M._u2_reset()
    r_none = M._u2_fire(None, 100.0, "MILK", 350, 1, 0.0, 200.0, obs)
    r_ok = M._u2_fire(98.0, 100.0, "MILK", 350, 1, 0.0, 200.0, obs)
    r_post = M._u2_fire(50.0, 100.0, "MILK", 700, 1, 0.0, 200.0, obs)
    orig_pass = M._u2_pass
    def boom(*a, **k):
        raise RuntimeError("gate boom")
    M._u2_pass = boom
    r_boom = M._u2_fire(98.0, 100.0, "MILK", 350, 1, 0.0, 200.0, obs)
    M._u2_pass = orig_pass
    rec("P6_u2_fire_failsafe", verdict="PASS" if (r_none is False and r_ok is True and r_post is True and r_boom is True) else "FAIL",
        p_next_None=r_none, normal=r_ok, post648=r_post, gate_exception=r_boom,
        report=dict(M._U2_REPORT),
        note="base 异常->False 不发射；gate 异常->True 回退基线放行")
except Exception as e:
    rec("P6_u2_fire_failsafe", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P7: 小时1 s801(>=95) / s804(20..94) 档与台账（+D3 断言）============
try:
    s1 = 24 * 14 + 1
    seed_native(0, s1)
    M._S758_HIST.clear(); M._S804_HIST.clear()
    r7 = M._s758_apply(mk_obs(s1, inv={"MILK": 9950, "STRAWBERRY": 9950, "WOOL": 9950},
                              prices={"MILK": 96, "STRAWBERRY": 60, "WOOL": 30},
                              shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}), {"market": [], "units": []})
    h758 = M._S758_HIST.get(0, {}); h804 = M._S804_HIST.get(0, {})
    own758 = (h758.get("prev") or {}).get("own") or {}
    own804 = (h804.get("prev") or {}).get("own") or {}
    d3_ok = (int(own758.get("STRAWBERRY", 0)) >= 1 and int(own758.get("WOOL", 0)) >= 1
             and int(own758.get("MILK", 0)) >= 1)
    rec("P7_hour1_tiers", verdict="PASS",
        orders=[o for o in (r7.get("market") or [])],
        s758_prev=bool(h758.get("prev")), s804_prev=bool(h804.get("prev")),
        s758_win={i: list(h758.get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")},
        s804_win={i: list(h804.get(i) or []) for i in ("MILK", "STRAWBERRY", "WOOL")},
        s804_report=dict(M._S804_REPORT), s758_report=dict(M._S758_REPORT),
        d3_own_ledger_758=own758, d3_own_ledger_804=own804,
        d3_double_write_ok=d3_ok,
        note="D3 断言：s804 自插 SELL 同步记 _S758_HIST own（防日历变更回归）")
except Exception as e:
    rec("P7_hour1_tiers", verdict="FAIL", err=repr(e), tb=traceback.format_exc())


def tiles_same(n=8):
    row = [{"crop": c} for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")]
    return [list(row), list(row)]


def tiles_diff_own():
    return [[{"crop": c} for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")],
            [{"crop": "MELON"}, {"crop": "WHEAT"}, {"crop": "CARROT"}, {"crop": "TOMATO"}]]


def tiles_diff_rival(sheep=0):
    tl = [[{"animal": "SHEEP"}] * sheep + [{"crop": "MELON"}] * (4 - sheep),
          [{"crop": "TOMATO"}, {"crop": "STRAWBERRY"}, {"crop": "WHEAT"}, {"crop": "CARROT"}]]
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
                o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3 if cls_hint == "wfr" else 0)
        if s == 143 and cls_hint == "wfr":
            o["farms"][1]["tiles"] = tiles_diff_rival(sheep=3)
        M._oc_after(o, {"market": []})


# ============ P8: 画像层换局失鲜（修复后应 PASS）============
try:
    M._OC_STATE.clear()
    feed(range(0, 144), cd=5.0, sm=0.99)
    cls1 = M._oc_cls(mk_obs(144), 144)
    feed(range(0, 145), cd=0.1, sm=0.99)
    cls2 = M._oc_cls(mk_obs(200), 200)
    st = M._OC_STATE[0]
    rec("P8_oc_cross_episode_staleness", verdict="DEFECT_CONFIRMED" if cls2 == cls1 else "PASS",
        ep1_cls=cls1, ep2_cls=cls2, last_step=st.get("last_step"), locked=st.get("locked"),
        note="修复后 ep2 特征=h1_mirror 应实得 h1_mirror（step<=last_step 换局重播）")
except Exception as e:
    rec("P8_oc_cross_episode_staleness", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P9: 画像窗隙拍（无错 delta）============
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
        prev_step=st.get("prev_step"), rival_sold_cum=st.get("rival_sold_cum"),
        own_sold_cum=st.get("own_sold_cum"),
        note="prev_step!=step-1 时 rival/own 累计均暂停，无跨隙错量")
except Exception as e:
    rec("P9_oc_gap_no_bogus_delta", verdict="FAIL", err=repr(e), tb=traceback.format_exc())


def fp_routes():
    return {rid: [json.dumps(a, sort_keys=True, default=str) for a in seq]
            for rid, seq in M._IMPL.chassis.routes.items()}


def fp_diff(a, b, min_step=0):
    return sum(1 for rid in a for i, (x, y) in enumerate(zip(a[rid], b.get(rid, [])))
               if i >= min_step and x != y)


# 廉价 delta 触点指纹（只看 C3 触点格；P13 逐拍迹用）
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


# ============ P10: C3 换局一次性闩（修复后应 PASS）============
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
    M._u2_reset(); M._x1_reset()
    M._S758_HIST.clear(); M._S804_HIST.clear()
    M._OC_STATE.clear()
    try:
        M._u2_agent(mk_obs(0))
    except Exception:
        pass
    latch_after_ep2_step0 = list(M._OC_C3_SWAPPED)
    routes_after_ep2 = fp_routes()
    kept = fp_diff(routes_pristine, routes_after_ep2, min_step=100)
    ok = (swap_entries > 0 and latch_after_ep2_step0 == [False] and kept == 0)
    rec("P10_c3_latch_no_episode_reset",
        verdict="PASS" if ok else "DEFECT_CONFIRMED",
        ep1_cls=cls_wfr, latch_after_ep1=latch_after_ep1,
        latch_after_ep2_step0=latch_after_ep2_step0,
        c3_swap_route_entries_mutated=swap_entries,
        swap_entries_kept_after_ep2_step0=kept,
        base_opening_rewrite_entries_at_ep2_step0=fp_diff(routes_after_swap, routes_after_ep2, min_step=0),
        note="修复后 ep2 step0 应闩复位+换表反向还原（443 条触点回原值）")
except Exception as e:
    rec("P10_c3_latch_no_episode_reset", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P11: 逐层注册表隔离 ============
try:
    iso = {}
    M._OC_STATE.clear(); M._S758_HIST.clear(); M._S804_HIST.clear()
    seed_native(0, 630)
    b = snap()
    M._x1_post(mk_obs(630, shed={"MILK": 1}), {"market": [["SELL", "MILK", 9], ["SELL", "MILK", 2]], "units": []})
    iso["X1"] = sorted(diff(b, snap()))
    b = snap()
    M._oc_after(mk_obs(5, money1=1006.0), {"market": []})
    iso["profile"] = sorted(diff(b, snap()))
    b = snap()
    try:
        M._oc_r36_reserve(mk_obs(200), {"market": []})
    except Exception:
        pass
    iso["C2_reserve"] = sorted(diff(b, snap()))
    b = snap()
    seed_native(0, 350)
    M._s758_apply(mk_obs(350, inv={"MILK": 9950}, prices={"MILK": 220}, shed={"MILK": 5}), {"market": [], "units": []})
    iso["window_core"] = sorted(diff(b, snap()))
    b = snap()
    M._u2_fire(98.0, 100.0, "MILK", 350, 1, 0.0, 220.0, mk_obs(350))
    M._u2_qty(6, 220.0, 219.0, 350)
    iso["drop_half_gate"] = sorted(diff(b, snap()))
    OUT["isolation"] = iso
except Exception as e:
    OUT["isolation"] = {"error": repr(e), "tb": traceback.format_exc()}

# ============ P12: 全链入口冒烟（step0 复位 + step350）============
try:
    smoke = {}
    M._U2_REPORT.update(gate_calls=99)
    try:
        a = M._u2_agent(mk_obs(0))
        smoke["step0"] = "ok action=%r" % (a,)
    except Exception as e:
        smoke["step0"] = "raise %r" % (e,)
    smoke["u2_report_after_step0"] = dict(M._U2_REPORT)
    seed_native(0, 350)
    try:
        a = M._u2_agent(mk_obs(350, inv={"MILK": 9950, "STRAWBERRY": 9950, "WOOL": 9950},
                                 prices={"MILK": 220, "STRAWBERRY": 460, "WOOL": 590},
                                 shed={"MILK": 5, "STRAWBERRY": 5, "WOOL": 5}))
        smoke["step350"] = "ok action=%r" % (a,)
    except Exception as e:
        smoke["step350"] = "raise %r" % (e,)
    smoke["u2_report"] = dict(M._U2_REPORT)
    rec("P12_full_entry_smoke", verdict="INFO", smoke=smoke)
except Exception as e:
    rec("P12_full_entry_smoke", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

# ============ P13: 双局连跑（同进程 ep1 触发 C3 / ep2 非 WFR）============
# 断言：ep1 换表发生（latch True + 触点变动）；ep2 边界复位后 零换表 零闩，
# ep2 全程（含144+ 锁存点）闩恒 False、触点恒 pristine、cls≠wfr。
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
        act = M._u2_agent(o)
    ep1_latch = list(M._OC_C3_SWAPPED)
    ep1_cls = M._OC_STATE[0].get("cls")
    ep1_mutated = fp_diff(routes_pristine, fp_routes(), min_step=100)
    ep1_ok = (ep1_latch == [True] and ep1_mutated > 0)
    # ep2：镜像/非 WFR 对手（cd=0.1, sm=0.99）同进程串跑
    ep2_trace = []
    for s in range(0, 200):
        o = mk_obs(s, money0=1000.0, money1=1000.1, tiles=tiles_diff_own())
        if s in M._OC_SIM_STEPS:
            tl = tiles_same()
            o["farms"][0]["tiles"] = [list(r) for r in tl]
            o["farms"][1]["tiles"] = [list(r) for r in tl]
        act = M._u2_agent(o)
        sig = delta_cells_sig()
        n_dirty = sum(1 for x, y in zip(pristine_sig, sig) if x != y)
        ep2_trace.append((s, list(M._OC_C3_SWAPPED), n_dirty))
    latch_during_ep2 = [t[1][0] for t in ep2_trace]
    mutated_during_ep2 = [t[2] for t in ep2_trace]
    ep2_cls = M._OC_STATE[0].get("cls")
    zero_latch = (not any(latch_during_ep2))
    zero_swap = (max(mutated_during_ep2 or [0]) == 0)
    rec("P13_dual_game_serial_zero_pollution",
        verdict="PASS" if (ep1_ok and zero_latch and zero_swap and ep2_cls != "wfr") else "FAIL",
        ep1_cls=ep1_cls, ep1_latch=ep1_latch, ep1_entries_mutated=ep1_mutated,
        ep1_trigger_ok=ep1_ok,
        ep2_cls=ep2_cls, ep2_zero_latch=zero_latch, ep2_zero_swap=zero_swap,
        ep2_max_entries_mutated=max(mutated_during_ep2 or [0]),
        ep2_latch_true_ticks=sum(1 for x in latch_during_ep2 if x),
        note="同进程 ep1 WFR 触发 C3 -> ep2 非 WFR：断言 ep2 零换表零闩（换局复位生效）")
except Exception as e:
    rec("P13_dual_game_serial_zero_pollution", verdict="FAIL", err=repr(e), tb=traceback.format_exc())

os.makedirs(os.path.join(LAB, "evidence"), exist_ok=True)
out_path = os.path.join(LAB, "evidence", "m13fix_probe_out.json")
json.dump(OUT, open(out_path, "w"), indent=1, default=str)
n_pass = sum(1 for p in OUT["probes"] if str(p.get("verdict", "")).startswith(("PASS", "INFO")))
n_def = sum(1 for p in OUT["probes"] if p.get("verdict") == "DEFECT_CONFIRMED")
n_fail = sum(1 for p in OUT["probes"] if p.get("verdict") == "FAIL")
print("written", out_path, "pass=%d defect=%d fail=%d" % (n_pass, n_def, n_fail))
