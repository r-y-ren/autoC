# -*- coding: utf-8 -*-
"""judge_tomato2（T2 = H1X 基座 + TOMATO 微单滴灌层）：判决（只测不发/不在线提交）。

T2 = orderbook_h1x_lab/build/h1x/main.py（9d073fba…）+ 滴灌尾块
（build_tomato2.py；qty-1 粒度手术/价门 quote≥base/24 滴日/防幻影/
守恒零跨拍挪量/step≥712 零触碰），entry _t2_agent。

判决口径：judge_r44._fold_arm 双席折叠、margin=farms[obs.player]（终局钱差
干净口径）、块 674000+i*159（i=0..11；稳节奏面 i=0..7）：
  1. 面板（每对 12 fold 双席）：t2 vs {H1X 本体、H1（王座锚）、r40、A}；
     对照臂 h1x 本体 vs {H1,r40,A} 同 (seed,seat,opp) 配对→逐 unit delta；
  2. 稳节奏面（S9 扰动教训）：t2/h1x 双臂 vs tetsutani step1009 件，8 fold；
  3. KPI=tomato 实现价（逐局 settle-replay：双席市场单按引擎 per-index
     per-unit lockstep 复算成交价（同拍同快照报价、pid 序 commit、$1 地板
     不入库存）；实现价=Σ成交额/Σ成交量，本体对照）；
判读：①配对 delta>0 且 flips_neg=0 ②tomato 实现价>本体（机制验证）
③对王座锚 h2h≥0.5 ④弱锚（r40/A）≥0.8 ⑤稳节奏面无显著负。
全过→发射候选成立。预算 ≤400 局（auth 30 + 面板 96 + 对照 72 + 稳节奏 32
+ 冒烟 2 = 232）。sim_bridge 认证缓存复用。证据 evidence/tomato2_verdict.json。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_s1form_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用（Tracer/end_reads/flip/fold）

EVID_DIR = HERE / "evidence"
T2 = HERE / "build" / "t2" / "main.py"
H1X = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
H1 = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
PANEL = {
    "h1x0": H1X,
    "H1": H1,
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
CONTROL_OPPS = ("H1", "r40", "A")
STEADY = {"tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents"
          / "tetsu1009" / "main.py"}
FOLDS = [674000 + i * 159 for i in range(12)]
F8 = FOLDS[:8]
WORKERS = 3
BUDGET_CAP = 400

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 30, "smoke": 2,
          "panel_规格": 96, "control_规格": 72, "steady_规格": 32}
_ROW_CACHE = {}


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "tomato2_verdict.json").write_text(
        json.dumps(EV, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")


# ==================================================== tomato 实现价 KPI ==
# 价格曲线（market.rs/官方 1.32.7 逐式）：hinge = u + 8·max(0,u-1)²（u=x/T）
_T2_PARAM = {"base": 60.0, "i0": 10000.0, "t": 200.0, "below": "hinge",
             "below_target": 0.40, "above": "sqrt", "above_target": 0.60}
_HINGE_GAIN = 8.0


def _shape(f, x, t):
    x = max(0.0, float(x))
    if f == "linear":
        return x
    if f == "sq":
        return x * x
    if f == "sqrt":
        return x ** 0.5
    if f == "log":
        import math
        return math.log(1.0 + x)
    if f == "hinge":
        if t <= 0:
            return x
        u = x / t
        over = max(0.0, u - 1.0)
        return u + _HINGE_GAIN * (over * over)
    return x


def _t2_price(inv):
    p = _T2_PARAM
    if inv < p["i0"]:
        amp = p["below_target"] * p["base"] / _shape(p["below"], p["t"], p["t"])
        price = p["base"] + amp * _shape(p["below"], p["i0"] - inv, p["t"])
    else:
        amp = p["above_target"] * p["base"] / _shape(p["above"], p["t"], p["t"])
        price = p["base"] - amp * _shape(p["above"], inv - p["i0"], p["t"])
    return max(1, int(round(price)))


def _market_list(act):
    out = {}
    for entry in (act or {}).get("market") or []:
        if not isinstance(entry, (list, tuple)) or len(entry) < 3:
            continue
        if entry[0] != "SELL" or entry[1] != "TOMATO":
            continue
        q = entry[2]
        if isinstance(q, bool):
            continue
        try:
            q = int(q)
        except (TypeError, ValueError):
            continue
        if q > 0:
            out[len(out)] = out.get(len(out), 0)  # placeholder (unused)
    # 保序抽取：index→qty（跨品订单也占 index；只记番茄）
    res = {}
    for idx, entry in enumerate((act or {}).get("market") or []):
        if not isinstance(entry, (list, tuple)) or len(entry) < 3:
            continue
        if entry[0] == "SELL" and entry[1] == "TOMATO":
            q = entry[2]
            if isinstance(q, bool):
                continue
            try:
                q = int(q)
            except (TypeError, ValueError):
                continue
            if q > 0:
                res[idx] = res.get(idx, 0) + q
    return res


def _settle_tomato(my_map, opp_map, inv0, my_pid):
    """per-index per-unit lockstep 复算（pid 序 commit；同轮同快照报价）。

    返回 (my_turnover, my_vol, opp_turnover, opp_vol)。fill 口径=全成交近似
    （V219 申报=投射可卖、滴灌单 qty-1；对称误差）。"""
    inv = float(inv0)
    my_to = my_vo = opp_to = opp_vo = 0.0
    for idx in sorted(set(my_map) | set(opp_map)):
        rem = {0: my_map.get(idx, 0) if my_pid == 0 else opp_map.get(idx, 0),
               1: my_map.get(idx, 0) if my_pid == 1 else opp_map.get(idx, 0)}
        esc = 0
        while (rem[0] > 0 or rem[1] > 0) and esc < 100000:
            esc += 1
            quoted = {}
            for pid in (0, 1):
                if rem[pid] > 0:
                    quoted[pid] = _t2_price(inv)
            if not quoted:
                break
            commits = 0
            for pid in (0, 1):
                if pid not in quoted:
                    continue
                price = quoted[pid]
                rem[pid] -= 1
                commits += 1
                if pid == my_pid:
                    my_to += price
                    my_vo += 1
                else:
                    opp_to += price
                    opp_vo += 1
                if price > 1:      # $1 地板成交不入库存
                    inv += 1
            if not commits:
                break
    return my_to, my_vo, opp_to, opp_vo


def tomato_kpi(sink_us, sink_opp, seat):
    """逐局 tomato 实现价：双席 (step,obs,act) 序列→settle-replay。"""
    opp_by_step = {}
    for entry in (sink_opp or []):
        if len(entry) >= 3:
            opp_by_step[int(entry[0])] = entry[2]
    my_to = my_vo = opp_to = opp_vo = 0.0
    inv_trace = []
    for entry in (sink_us or []):
        if len(entry) < 3:
            continue
        step = int(entry[0])
        obsd = entry[1] if isinstance(entry[1], dict) else {}
        act = entry[2]
        inv0 = (((obsd.get("market") or {}).get("inventory") or {})
                .get("TOMATO"))
        if inv0 is None:
            continue
        my_map = _market_list(act)
        opp_map = _market_list(opp_by_step.get(step))
        if not my_map and not opp_map:
            continue
        a, b, c, d = _settle_tomato(my_map, opp_map, inv0, seat)
        my_to += a
        my_vo += b
        opp_to += c
        opp_vo += d
        inv_trace.append({"step": step, "inv0": inv0,
                          "my_qty": sum(my_map.values()),
                          "opp_qty": sum(opp_map.values())})
    out = {
        "my_turnover": round(my_to, 1), "my_vol": my_vo,
        "my_realized_px": round(my_to / my_vo, 2) if my_vo else None,
        "opp_realized_px": round(opp_to / opp_vo, 2) if opp_vo else None,
        "opp_vol": opp_vo,
        "n_tomato_ticks": len(inv_trace),
    }
    return out


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱 farms[obs.player] + tomato 实现价 settle-replay。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows, games, metas = [], [], []
    for spec in payload["specs"]:
        sinks = {0: [], 1: []}
        try:
            our = j23._load_entry(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            a_us = jsf._Tracer(our, spec["our_seat"], sinks[spec["our_seat"]])
            a_opp = jsf._Tracer(opp, 1 - spec["our_seat"],
                                sinks[1 - spec["our_seat"]])
            a0, a1 = (a_us, a_opp) if spec["our_seat"] == 0 else (a_opp, a_us)
            games.append({"seed": int(spec["seed"]), "agents": [a0, a1]})
            metas.append((spec, sinks, our, None))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, sinks, None, repr(exc)[:120]))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rrs = list(res.get("games") or [])
    for i, (spec, sinks, our, berr) in enumerate(metas):
        rr = rrs[i] if i < len(rrs) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "arm": spec["arm"], "opponent": spec.get("opponent"),
               "block": spec.get("block"), "tag": spec.get("tag"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "tm_us": None, "tm_opp": None,
               "telemetry": jsf._snap_telemetry(our) if our is not None
               else None}
        if row["banks"] is not None and row["error"] is None:
            try:
                e_us = jsf.end_reads(sinks[row["seat"]])
                e_opp = jsf.end_reads(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            try:
                row["tomato"] = tomato_kpi(sinks[row["seat"]],
                                           sinks[1 - row["seat"]],
                                           row["seat"])
            except Exception as exc:
                row["tomato_error"] = repr(exc)[:100]
        rows.append(row)
    return rows


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk_runs(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk_runs, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def run_specs(specs, cfg):
    """去重跑口：同 (arm_path,seed,seat,opp_path) 只跑一次。"""
    out, todo = [], []
    for spec in specs:
        key = (spec["arm_path"], int(spec["seed"]), int(spec["our_seat"]),
               spec["opp_path"])
        if key in _ROW_CACHE:
            out.append(_ROW_CACHE[key])
        else:
            todo.append((key, spec))
    if todo:
        rows = play([s for _, s in todo], cfg)
        by_key = {}
        for row in rows:
            by_key.setdefault((row.get("seed"), row.get("seat"),
                              row.get("opponent")), []).append(row)
        for key, spec in todo:
            cand = by_key.get((int(spec["seed"]), int(spec["our_seat"]),
                              spec.get("opponent"))) or []
            row = cand.pop(0) if cand else {
                "seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
                "arm": spec["arm"], "opponent": spec.get("opponent"),
                "error": "row_missing", "margin_clean": None}
            row.setdefault("block", spec.get("block"))
            row.setdefault("tag", spec.get("tag"))
            _ROW_CACHE[key] = row
            out.append(row)
    return out


def mk_specs(arm, arm_path, opp_path, opp_name, folds, block, seats=(0, 1)):
    specs = []
    for seed in folds:
        for seat in seats:
            specs.append({
                "game_id": "t2-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


# ============================================================ 读数 ==
def pairs_from(rows_c, rows_v):
    """同 (seed,seat,opponent) 配对 margin 面（control=h1x, variant=t2）。"""
    key = lambda r: (r["seed"], r["seat"], r.get("opponent"))  # noqa: E731
    mc = {key(r): r for r in rows_c if r.get("margin_clean") is not None}
    mv = {key(r): r for r in rows_v if r.get("margin_clean") is not None}
    out = []
    for k in sorted(set(mc) & set(mv)):
        out.append((float(mc[k]["margin_clean"]), float(mv[k]["margin_clean"]),
                    k))
    return out


def flip_table(pairs):
    agg = jsf.flip_stats([(a, b) for a, b, _ in pairs])
    agg["pairs_detail"] = [
        {"seed": k[0], "seat": k[1], "opp": k[2],
         "margin_h1x": round(a, 1), "margin_t2": round(b, 1),
         "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold(rows):
    try:
        return jsf.fold_stats(rows)
    except Exception as exc:
        return {"error": repr(exc)[:120]}


def tomato_table(rows_by_arm):
    """KPI 对表：按 arm 汇总 tomato 实现价 + 逐局行。"""
    out = {}
    for arm, rows in rows_by_arm.items():
        tot_to = tot_vo = 0.0
        per_game = []
        for r in rows:
            t = r.get("tomato") or {}
            vo = t.get("my_vol") or 0
            to = t.get("my_turnover") or 0.0
            tot_to += to
            tot_vo += vo
            per_game.append({
                "seed": r.get("seed"), "seat": r.get("seat"),
                "opponent": r.get("opponent"),
                "tomato_vol": vo, "tomato_turnover": round(to, 1),
                "tomato_realized_px": t.get("my_realized_px"),
                "opp_realized_px": t.get("opp_realized_px"),
                "n_tomato_ticks": t.get("n_tomato_ticks")})
        out[arm] = {"games": len(rows), "games_with_tomato":
                    sum(1 for r in per_game if r["tomato_vol"]),
                    "tomato_vol": tot_vo,
                    "tomato_turnover": round(tot_to, 1),
                    "tomato_realized_px": round(tot_to / tot_vo, 2)
                    if tot_vo else None,
                    "per_game": per_game}
    return out


def tomato_pairs(rows_c, rows_v):
    """同 (seed,seat,opp) 配对 tomato 实现价（有番茄流的单元）。"""
    key = lambda r: (r["seed"], r["seat"], r.get("opponent"))  # noqa: E731
    mc = {key(r): (r.get("tomato") or {}) for r in rows_c}
    mv = {key(r): (r.get("tomato") or {}) for r in rows_v}
    out = []
    for k in sorted(set(mc) & set(mv)):
        a, b = mc[k], mv[k]
        if (a.get("my_vol") or 0) > 0 or (b.get("my_vol") or 0) > 0:
            out.append({"seed": k[0], "seat": k[1], "opp": k[2],
                        "px_h1x": a.get("my_realized_px"),
                        "vol_h1x": a.get("my_vol"),
                        "px_t2": b.get("my_realized_px"),
                        "vol_t2": b.get("my_vol"),
                        "delta_px": (round(b["my_realized_px"]
                                           - a["my_realized_px"], 2)
                                     if a.get("my_realized_px") is not None
                                     and b.get("my_realized_px") is not None
                                     else None)})
    return out


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    build = json.load(open(HERE / "build" / "t2" / "build_manifest.json"))
    EV.update({
        "version": "tomato2/1.0",
        "task": "T2=H1X 基座+TOMATO 微单滴灌层：测 tomato 实现价机制与总 margin"
                "（只测不发/不在线提交）",
        "design": {
            "formula": "T2 = H1X(9d073fba…)+滴灌尾块（qty-1 粒度手术/价门 "
                       "quote≥base/24 滴日/防幻影/守恒零跨拍挪量/step≥712 零触碰）"
                       "挂 _h1x_agent",
            "artifact": {"base": build["base"], "main": build["main"],
                         "tar": build["tar"], "entry": build["entry"],
                         "host": build["host_entry"]},
            "drip_params": build["drip_params"],
            "corpus": {
                "panel": "t2 vs {h1x0,H1 王座锚,r40,A}，12 fold（674000+"
                         "i*159,i=0..11）双席",
                "paired": "h1x0 控制臂 vs {H1,r40,A} 同 (seed,seat,opp) "
                          "配对（逐 unit delta）+ t2 vs h1x0 头对头",
                "steady": "t2/h1x0 双臂 vs tetsutani step1009，8 fold 双席"
                          "（S9 扰动教训）"},
            "caliber": {
                "margin": "终局钱 farms[obs.player] 差（干净口径）",
                "fold": "judge_r44._fold_arm 双席折叠（缺席/红局记负）",
                "flips": "同 (seed,seat,opp) 配对：h1x0 胜而 t2 负记 flips_neg",
                "tomato_kpi": "settle-replay：双席市场单按引擎 per-index "
                              "per-unit lockstep 复算（同轮同快照报价/pid 序 "
                              "commit/$1 地板不入库存）；实现价=Σ成交额/Σ成交量；"
                              "fill=全成交近似（对称）"},
        },
        "gates": {"build": build["checks"],
                  "t2_sha256": build["main"]["sha256"],
                  "tar_sha256": build["tar"]["sha256"]},
        "panel": {}, "paired_vs_h1x0": {}, "steady": {},
        "tomato_kpi_table": {}, "criteria": {}, "verdict": {},
    })
    flush_evid()

    # ---- sim_bridge 认证（复用 s1form 认证缓存）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    if auth_cache.is_file():
        auth = json.loads(auth_cache.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth = sb.sim_bridge({"n_games": 30, "min_checked": 30},
                             F8 + [675590])
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine")}
    EV["gates"]["sim_auth"] = auth_lite
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 冒烟 2 局 ----
    smoke = mk_specs("t2", T2, PANEL["h1x0"], "h1x0", [FOLDS[0]], "smoke",
                     seats=(0,))
    run_specs(smoke, run_cfg)
    print("smoke done", flush=True)
    flush_evid()

    # ---- ① 面板：t2 vs 4 对手（12 fold 双席）----
    panel = {"design": "t2 vs {h1x0,H1,r40,A}，12 fold（674000+i*159）双席；"
                       "fold=judge_r44._fold_arm",
             "pairs": {}}
    panel_rows = {}
    for on, opath in PANEL.items():
        rows = run_specs(mk_specs("t2", T2, opath, on, FOLDS, "panel"),
                         run_cfg)
        panel_rows[on] = rows
        panel["pairs"][on] = fold(rows)
        print("panel", on, panel["pairs"][on].get("h2h"), flush=True)
        flush_evid()
    EV["panel"] = panel

    # ---- ② 同块配对增量（vs h1x0 本体逐 unit delta）----
    ctrl_rows, paired = {}, {"design": "h1x0 控制臂 vs {H1,r40,A} 同 "
                                       "(seed,seat,opp) 配对（12 fold 双席）；"
                                       "delta=t2−h1x0", "per_opp": {}}
    for on in CONTROL_OPPS:
        ctrl_rows[on] = run_specs(
            mk_specs("h1x0", H1X, PANEL[on], on, FOLDS, "control"), run_cfg)
    pr_all = []
    for on in CONTROL_OPPS:
        ps = pairs_from(ctrl_rows[on], panel_rows[on])
        pr_all.extend(ps)
        paired["per_opp"][on] = flip_table(ps)
        paired.setdefault("fold_h2h", {})[on] = {
            "h1x0": fold(ctrl_rows[on]), "t2": fold(panel_rows[on])}
        print("paired", on, paired["per_opp"][on]["mean_delta"], flush=True)
    paired["all"] = flip_table(pr_all)
    paired["h2h_vs_h1x0"] = panel["pairs"]["h1x0"]
    EV["paired_vs_h1x0"] = paired
    flush_evid()

    # ---- ③ 稳节奏面（tetsutani step1009，8 fold 双席，S9 教训）----
    steady = {"design": "t2/h1x0 双臂 vs tetsutani step1009（tetsu1009），"
                        "8 fold（674000+i*159,i=0..7）双席", "arms": {}}
    for on, opath in STEADY.items():
        rows_v = run_specs(mk_specs("t2", T2, opath, on, F8, "steady"),
                           run_cfg)
        rows_c = run_specs(mk_specs("h1x0", H1X, opath, on, F8, "steady"),
                           run_cfg)
        ps = pairs_from(rows_c, rows_v)
        steady["arms"][on] = {"t2": fold(rows_v), "h1x0": fold(rows_c),
                              "paired": flip_table(ps)}
        print("steady", on, steady["arms"][on]["t2"].get("h2h"), flush=True)
        flush_evid()
    EV["steady"] = steady

    # ---- ④ KPI：tomato 实现价对表 ----
    all_rows = {"t2": [r for rows in panel_rows.values() for r in rows],
                "h1x0": [r for rows in ctrl_rows.values() for r in rows]}
    steady_rows = {"t2": [], "h1x0": []}
    for on, arm in steady["arms"].items():
        pass
    EV["tomato_kpi_table"] = {
        "caliber": "settle-replay per-index per-unit lockstep；实现价=Σ成交额/"
                   "Σ成交量（本体对照）",
        "panel": tomato_table(all_rows),
        "per_pair": tomato_pairs(all_rows["h1x0"], all_rows["t2"]),
    }
    flush_evid()

    # ---- 判据 + verdict ----
    pa = paired["all"]
    mean_delta = pa.get("mean_delta")
    flips_neg = pa.get("flips_neg", 0)
    c1 = bool(mean_delta is not None and mean_delta > 0 and flips_neg == 0)
    kt = EV["tomato_kpi_table"]["panel"]
    px_t2 = (kt.get("t2") or {}).get("tomato_realized_px")
    px_base = (kt.get("h1x0") or {}).get("tomato_realized_px")
    tomato_flow = bool((kt.get("t2") or {}).get("tomato_vol"))
    base_flow = bool((kt.get("h1x0") or {}).get("tomato_vol"))
    c2 = bool(tomato_flow and base_flow and px_t2 is not None
              and px_base is not None and px_t2 > px_base)
    c2_note = ("机制验证：%s" % (
        "drip %.2f vs 本体 %.2f" % (px_t2, px_base) if (tomato_flow and base_flow)
        else "番茄流不足（t2 vol=%s 本体 vol=%s）→ 机制无从验证"
             % ((kt.get("t2") or {}).get("tomato_vol"),
                (kt.get("h1x0") or {}).get("tomato_vol"))))
    h_h1 = (panel["pairs"].get("H1") or {}).get("h2h")
    c3 = bool(h_h1 is not None and h_h1 >= 0.5)
    weak = {k: (panel["pairs"].get(k) or {}).get("h2h") for k in ("r40", "A")}
    c4 = bool(all(v is not None and v >= 0.8 for v in weak.values()))
    st = steady["arms"]["tetsutani"]
    st_h2h = (st.get("t2") or {}).get("h2h")
    st_delta = (st.get("paired") or {}).get("mean_delta")
    st_flips_neg = (st.get("paired") or {}).get("flips_neg", 0)
    # 判据⑤=稳节奏面 flips_neg=0（以判据为准；h2h/delta 只作读数）
    c5 = bool(st_flips_neg == 0)
    full = bool(c1 and c2 and c3 and c4 and c5)
    EV["criteria"] = {
        "rule": "配对 delta>0 且 flips_neg=0；tomato 实现价>本体（机制验证）；"
                "对王座锚 H1 h2h≥0.5；弱锚 r40/A≥0.8；稳节奏面 flips_neg=0"
                "→ 发射候选成立",
        "c1_paired_delta_pos_flips_neg0": {
            "mean_delta": mean_delta, "W": pa.get("W"), "L": pa.get("L"),
            "T": pa.get("T"), "flips_pos": pa.get("flips_pos"),
            "flips_neg": flips_neg, "passed": c1},
        "c2_tomato_realized_px": {"px_t2": px_t2, "px_h1x0": px_base,
                                  "vol_t2": (kt.get("t2") or {}).get("tomato_vol"),
                                  "vol_h1x0": (kt.get("h1x0") or {}).get("tomato_vol"),
                                  "note": c2_note, "passed": c2},
        "c3_vs_throne_H1_ge_0.5": {"h2h": h_h1, "passed": c3},
        "c4_weak_anchors_ge_0.8": {"r40": weak.get("r40"), "A": weak.get("A"),
                                   "passed": c4},
        "c5_steady_face_no_neg": {"tetsutani_h2h": st_h2h,
                                  "tetsutani_paired_delta": st_delta,
                                  "tetsutani_flips_neg": st_flips_neg,
                                  "passed": c5},
    }
    EV["verdict"] = {
        "panel_h2h": {k: v.get("h2h") for k, v in panel["pairs"].items()},
        "paired_vs_h1x0": {"W": pa.get("W"), "L": pa.get("L"), "T": pa.get("T"),
                           "mean_delta": mean_delta,
                           "flips_pos": pa.get("flips_pos"),
                           "flips_neg": flips_neg},
        "tomato_px": {"t2": px_t2, "h1x0": px_base, "c2_note": c2_note},
        "steady": {"t2_h2h": st_h2h, "h1x0_h2h": (st.get("h1x0") or {}).get("h2h"),
                   "paired_delta": st_delta},
        "criteria_passed": full,
        "verdict": ("发射候选成立" if full else
                    "未成立（如实报）：c1=%s c2=%s c3=%s c4=%s c5=%s"
                    % (c1, c2, c3, c4, c5)),
        "summary": "T2[%s]：面板 h2h %s；配对 W/L/T %s/%s/%s mean %s"
                   "（flips +%s/-%s）；tomato 实现价 t2 %s vs 本体 %s（%s）；"
                   "对 H1 %s；弱锚 %s；稳节奏 %s（delta %s）；判据 %s"
                   % (build["main"]["sha256"][:8],
                      json.dumps({k: v.get("h2h")
                                  for k, v in panel["pairs"].items()},
                                 default=str),
                      pa.get("W"), pa.get("L"), pa.get("T"), mean_delta,
                      pa.get("flips_pos"), flips_neg, px_t2, px_base, c2_note,
                      h_h1, weak, st_h2h, st_delta, full),
        "launch": "只测不发（在线提交=硬禁令）；发射决策移交用户",
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE)
    BUDGET["total_局次"] = 30 + len(_ROW_CACHE)
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货")
    ANOMALIES.append(
        "tomato 实现价=fill 全成交近似（V219 申报=投射可卖、滴灌单 qty-1，对称）；"
        "价格曲线按官方 1.32.7 hinge gain 8 逐式复算；$1 地板不入库存")
    ANOMALIES.append(
        "滴灌层口径：粒度手术（出货粒度 q→1）零跨拍挪量；未出量留仓宿主再计划"
        "（game-wide 守恒只改粒度）；V219 番茄模块为条件模块（step432 资格门），"
        "12 fold 中仅 675590 实测触发——番茄流覆盖稀疏是本判决的样本约束")
    ANOMALIES.append(
        "sim_bridge 认证复用 s1form 缓存（consistency_ok）按 30 计账；"
        "预算局次=auth+去重后实跑局数")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", EV["verdict"]["summary"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
