# -*- coding: utf-8 -*-
"""judge_s_form（s1 卖面结构重写 lab）：S_form 新标准终验（判决先行·不发射/不提交）。

S_form = C_final（sha a37c0d34…）+ 卖面重写尾块，两形态（build_s_form.py）：
  s_split  = lot 2-4 同拍拆发 + 申报背书 + d12-24 平台 + d29 分抛 + d0 粒度；
  s_append = 多拍小单追加回退形态（R26 线预案）：原单不拆，lot 形态由追加单承载。
终验面：
1. 构建门：compile/末 callable=_sf_agent/基底前缀恒等/反替换回程/宿主捕获/mode；
2. sim_bridge 先认证 30/30；
3. 配对面（control=c_final vs 两形态，n=16 双席=32 对/臂，新块 674000+i*143，
   轮转 4 对手）：形态对照（flips/full_exec/单均量/净卖总量恒等）+ R26 线判定
   （拆发形态配对判负→回退形态上主审）；
4. 新标准面板（胜出形态 vs {oc_c3,mpx,tetsutani,V89,r40,A}；vs oc_c3 加密 n=24
   双席，余 n=16 双席）：①对 oc_c3 ≥0.5 强/≥0.7 碾压（目标）②强面板逐对 ≥0.5
   ③弱锚 ≥0.8 ④flips_neg=0 ⑤full_exec 对照（目标 0.72-0.94）与单均量对照
   （目标 2-4）。
预算 ≤500 局次（auth 30 + 配对 96 + 面板 208 = 334）。
证据 fn_docs/hybrid/results/2026-09-30-s1-sellform.json；账本落本 lab evidence/。
只写 orderbook_s1form_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
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
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-s1-sellform.json"

BASE = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
SPLIT = HERE / "build" / "s_split" / "main.py"
APPEND = HERE / "build" / "s_append" / "main.py"
FORMS = {"s_split": SPLIT, "s_append": APPEND}
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py",
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
PANEL_STRONG = ("mpx", "tetsutani", "V89")
PANEL_WEAK = ("r40", "A")
FOLDS = [674000 + i * 143 for i in range(24)]
F16 = FOLDS[:16]
WORKERS = 2
BUDGET_CAP = 500

_SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 跑口 ==
class _Tracer:
    """逐拍追踪（step, obs, act）；结束后抽 telemetry 快照。"""

    def __init__(self, inner, seat, sink):
        self.inner, self.seat, self.sink = inner, seat, sink

    def __call__(self, obs, configuration=None):
        code = getattr(self.inner, "__code__", None)
        n = code.co_argcount if code is not None else 1
        act = self.inner(*[obs, configuration][:max(1, int(n))])
        try:
            from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
            step = j23._obs_step(obs)
            obsd = j23._obs_dict(obs)
        except Exception:
            step, obsd = 0, {}
        self.sink.append((int(step), obsd, act))
        return act


def _snap_telemetry(inner):
    tel = getattr(inner, "telemetry", None)
    if isinstance(tel, dict):
        return {k: (dict(v) if isinstance(v, dict) else v)
                for k, v in tel.items()}
    return None


def _chunk_runs(payload):
    """配对/面板 worker：双席追踪跑 + 影子归因 + 卖面统计。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows, games, metas = [], [], []
    for spec in payload["specs"]:
        sinks = {0: [], 1: []}
        try:
            our = j23._load_entry(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            a_us = _Tracer(our, spec["our_seat"], sinks[spec["our_seat"]])
            a_opp = _Tracer(opp, 1 - spec["our_seat"],
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
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None,
               "telemetry": _snap_telemetry(our) if our is not None else None,
               "shadow": None, "end": None, "lot": None}
        if row["banks"] is not None and row["error"] is None:
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            try:
                b = row["banks"]
                row["margin_banks"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
            try:
                row["shadow"] = shadow_books(sinks, int(spec["seed"]))
            except Exception as exc:
                row["shadow"] = {"error": repr(exc)[:120]}
            try:
                row["end"] = end_reads(sinks[row["seat"]])
            except Exception:
                row["end"] = None
            row["lot"] = lot_reads(sinks[row["seat"]])
        rows.append(row)
    return rows


def play(chunk_fn, specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [chunk_fn(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(chunk_fn, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


# ============================================================ 读数 ==
def shadow_books(sinks, seed):
    """影子引擎逐单成交归因（decl 同源口径）：全清率 + 分品累计成交。"""
    try:
        base = str(KSIM_DIR.parent)
        if base not in sys.path:
            sys.path.insert(0, base)
        from kgenv import replay_profile as rp  # noqa: WPS433
    except Exception as exc:
        return {"error": repr(exc)[:120]}
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            m[seat][int(entry[0])] = (entry[1], entry[2])
    steps = sorted(set(m[0]) | set(m[1]))
    if not steps:
        return {"error": "empty_traces"}
    first = steps[0]
    pre0 = m[0].get(first, (None, None))[0] or m[1].get(first, (None, None))[0]
    pre1 = m[1].get(first, (None, None))[0] or pre0
    try:
        state = rp._s_snapshot(pre0, [pre0.get("private"),
                                      pre1.get("private")])
    except Exception as exc:
        return {"error": "snapshot: %r" % exc}
    acc = {0: {}, 1: {}}
    ords = {0: {"orders": 0, "full": 0, "partial": 0, "requested_qty": 0.0,
                "filled_qty": 0.0, "value": 0.0},
            1: {"orders": 0, "full": 0, "partial": 0, "requested_qty": 0.0,
                "filled_qty": 0.0, "value": 0.0}}
    mism = 0
    for s in steps:
        acts = [m[0].get(s, (None, None))[1], m[1].get(s, (None, None))[1]]
        acts = [a if isinstance(a, dict) else
                {"farmer": ["PASS"], "hands": [], "market": []} for a in acts]
        try:
            post, attr = rp._s_step(state, acts, s, _SHADOW_CFG, int(seed))
        except Exception:
            mism += 1
            continue
        for pl in (0, 1):
            try:
                orders = attr["market"][pl]["orders"]
            except Exception:
                continue
            for o in orders:
                if o.get("type") != "SELL":
                    continue
                item = str(o.get("item"))
                filled = float(o.get("filled") or 0)
                value = float(o.get("value") or 0)
                req = float(o.get("requested") or 0)
                row = acc[pl].setdefault(item, {"filled": 0.0, "value": 0.0,
                                                "req": 0.0})
                row["filled"] += filled
                row["value"] += value
                row["req"] += req
                if req > 0:
                    oag = ords[pl]
                    oag["orders"] += 1
                    oag["requested_qty"] += req
                    oag["filled_qty"] += filled
                    oag["value"] += value
                    if abs(filled - req) < 1e-9:
                        oag["full"] += 1
                    else:
                        oag["partial"] += 1
        nxt = s + 1
        n0 = m[0].get(nxt, (None, None))[0]
        n1 = m[1].get(nxt, (None, None))[0]
        if n0 and n1:
            try:
                diff = rp._s_compare(post, n0,
                                     [n0.get("private"), n1.get("private")])
            except Exception:
                diff = ["compare_error"]
            if diff:
                mism += 1
                try:
                    state = rp._s_snapshot(n0, [n0.get("private"),
                                                n1.get("private")])
                except Exception:
                    state = post
            else:
                state = post
        else:
            state = post
    return {"per_item_by_seat": acc, "orders_by_seat": ords,
            "shadow_mismatch_steps": mism}


def end_reads(sink):
    last_obs = None
    for entry in (sink or []):
        if isinstance(entry[1], dict):
            last_obs = entry[1]
    if not isinstance(last_obs, dict):
        return {"terminal_money": None, "stranding": None, "shed_end": {}}
    try:
        player = int(last_obs.get("player", 0))
    except Exception:
        player = 0
    farms = last_obs.get("farms")
    tm = None
    if isinstance(farms, list) and player < len(farms) \
            and isinstance(farms[player], dict):
        try:
            tm = round(float(farms[player].get("money", 0.0)), 2)
        except (TypeError, ValueError):
            pass
    prices = ((last_obs.get("market") or {}) if isinstance(
        last_obs.get("market"), dict) else {}).get("prices") or {}
    shed = ((last_obs.get("private") or {}) if isinstance(
        last_obs.get("private"), dict) else {}).get("shed") or {}
    total = 0.0
    shed_end = {}
    for item, qty in (shed or {}).items():
        try:
            q = float(qty)
        except (TypeError, ValueError):
            continue
        try:
            v = float(prices.get(item, 0)) * q
        except (TypeError, ValueError):
            v = 0.0
        total += v
        shed_end[str(item)] = q
    return {"terminal_money": tm, "stranding": round(total, 2),
            "shed_end": shed_end}


def lot_reads(sink):
    """提交口径单量形态（我席）：正挂量 SELL 单 qty 直方图/均值 + d29 分抛对照。"""
    hist, n, tot = {}, 0, 0.0
    d29_orders = d29_qty = 0
    for entry in (sink or []):
        act = entry[2] if len(entry) > 2 else None
        step = int(entry[0]) if len(entry) > 0 else -1
        if not isinstance(act, dict):
            continue
        for cmd in (act.get("market") or []):
            if not (isinstance(cmd, (list, tuple)) and len(cmd) >= 3
                    and cmd[0] == "SELL"):
                continue
            raw = cmd[2]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                continue
            q = float(raw)
            if q <= 0:
                continue
            key = str(int(q)) if q.is_integer() else str(q)
            hist[key] = hist.get(key, 0) + 1
            n += 1
            tot += q
            if step >= 696:
                d29_orders += 1
                d29_qty += q
    return {"orders": n, "qty_sum": round(tot, 1),
            "mean_lot": round(tot / n, 3) if n else None,
            "d29_orders": d29_orders, "d29_qty": round(d29_qty, 1),
            "hist": hist}


def full_exec_agg(rows, seat_key="seat"):
    """全清率口径（decl 同源）：requested>0 SELL 单 filled==requested 记全清。"""
    tot = {"orders": 0, "full": 0, "partial": 0, "requested_qty": 0.0,
           "filled_qty": 0.0}
    filled_by_item = {}
    mism = 0
    for r in rows:
        sh = r.get("shadow") or {}
        if sh.get("error"):
            continue
        mism += int(sh.get("shadow_mismatch_steps") or 0)
        o = (sh.get("orders_by_seat") or {}).get(r[seat_key]) or {}
        for k in ("orders", "full", "partial"):
            tot[k] += int(o.get(k) or 0)
        tot["requested_qty"] += float(o.get("requested_qty") or 0)
        tot["filled_qty"] += float(o.get("filled_qty") or 0)
        per = (sh.get("per_item_by_seat") or {}).get(r[seat_key]) or {}
        for item, row in per.items():
            d = filled_by_item.setdefault(item, {"filled": 0.0, "req": 0.0})
            d["filled"] += float(row.get("filled") or 0)
            d["req"] += float(row.get("req") or 0)
    n = max(1, tot["orders"])
    return {
        "n_sell_orders": tot["orders"],
        "full": tot["full"], "partial": tot["partial"],
        "full_exec": round(tot["full"] / n, 4) if tot["orders"] else None,
        "requested_qty": round(tot["requested_qty"], 1),
        "filled_qty": round(tot["filled_qty"], 1),
        "gap_qty": round(tot["requested_qty"] - tot["filled_qty"], 1),
        "filled_by_item": {k: round(v["filled"], 1)
                           for k, v in sorted(filled_by_item.items())},
        "shadow_mismatch_steps": mism,
    }


def lot_agg(rows):
    hist, n, tot = {}, 0, 0.0
    for r in rows:
        lot = r.get("lot") or {}
        n += int(lot.get("orders") or 0)
        tot += float(lot.get("qty_sum") or 0)
        for k, v in (lot.get("hist") or {}).items():
            hist[k] = hist.get(k, 0) + int(v)
    keys = sorted(hist, key=lambda x: float(x))
    return {"n_sell_orders": n, "qty_sum": round(tot, 1),
            "mean_lot": round(tot / n, 3) if n else None,
            "d29_orders_per_game": round(sum(
                int((r.get("lot") or {}).get("d29_orders") or 0)
                for r in rows) / max(1, len(rows)), 1),
            "hist": {k: hist[k] for k in keys}}


def flip_stats(pairs):
    agg = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0}
    for mc, mv in pairs:
        d = mv - mc
        agg["n"] += 1
        agg["W" if d > 0 else "L" if d < 0 else "T"] += 1
        agg["delta_sum"] += d
        wc, wv = (1 if mc > 0 else 0), (1 if mv > 0 else 0)
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
    n = max(1, agg["n"])
    agg["mean_delta"] = round(agg["delta_sum"] / n, 2)
    agg["net_flip_wins"] = agg["win_variant"] - agg["win_control"]
    return agg


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows if isinstance(r.get("tm_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin_clean"] = round(sum(r["margin_clean"] for r in rows
                                       if r["margin_clean"] is not None)
                                   / max(1, len(rows)), 1)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def specs_for(arm, arm_path, opp_path, opp_name, folds):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    specs = []
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    for j, seed in enumerate(folds):
        for seat in (0, 1):
            opp = opp_path or opp_paths[j % len(opp_paths)]
            specs.append({
                "game_id": "sf-%s|%s|%d-s%d" % (
                    arm, opp_name or Path(opp).parent.name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp),
                "opponent": opp_name or Path(opp).parent.name,
                "kind": "ab", "trace": True,
                "agents": [{"type": "python", "path": str(arm_path)},
                           {"type": "python", "path": str(opp)}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def arm_stats(rows):
    fe = full_exec_agg(rows)
    lot = lot_agg(rows)
    tel = [r.get("telemetry") for r in rows
           if isinstance(r.get("telemetry"), dict)]
    tel_sum = {}
    for t in tel:
        for k, v in t.items():
            if isinstance(v, (int, float)):
                tel_sum[k] = tel_sum.get(k, 0) + v
    strd = [r["end"]["stranding"] for r in rows
            if r.get("end") and isinstance(r["end"].get("stranding"),
                                           (int, float))]
    margins = [float(r["margin_clean"]) for r in rows
               if r.get("margin_clean") is not None]
    return {
        "full_exec": fe, "lot": lot, "telemetry_sum": tel_sum,
        "stranding_mean": round(sum(strd) / len(strd), 1) if strd else None,
        "mean_margin": round(sum(margins) / len(margins), 1) if margins else None,
    }


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP, "auth": 0, "paired": 0, "panel": 0,
              "smoke_disclosed_extra": 8}

    builds = {f: json.load(open(HERE / "build" / f / "build_manifest.json"))
              for f in FORMS}
    EV.update({
        "version": "s1-sellform/1.0",
        "task": "C_final 卖面结构重写为顶强卖面形态（lot 2-4 小单粒度 + 申报背书"
                "+ d12-24 平台 + d29 终局分抛 + d0 开局粒度）并按新标准终验"
                "（不改既有代码/不提交/不发射）",
        "rewrite": {
            "formula": "S_form = C_final(a37c0d34…) + 卖面重写尾块（两形态）",
            "forms": {
                f: {"main": builds[f]["main"]["path"],
                    "sha256": builds[f]["main"]["sha256"],
                    "mode": builds[f]["mode"],
                    "semantics": builds[f]["semantics"]}
                for f in FORMS},
            "components": {
                "small_lot_granularity": (
                    "①小单清仓流：SELL 单量 3/6/10 帽位→lot 2-4 档。s_split="
                    "同拍拆发（同拍拆并语义·X1 量守恒同族；跨拍不拆=R23/R26 红线；"
                    "槽位 10 帽内拆发、超帽合并尾部保总量）；s_append=多拍小单"
                    "追加回退形态（R26 线预案：追加单量 ≤4/单、可多单承载 lot "
                    "形态）"),
                "decl_backing": (
                    "②申报背书：申报量=min(申报,投射可卖)（decl_m 同序口径；裁 0 "
                    "留占槽；decl 中立性=钱面无损实证；全清率→0.72-0.94 顶强形"
                    "=副产品）"),
                "platform_release": (
                    "③d12-24 平台投放（D6：d14-20 窗无差距、窗不动）：MSW×12..22"
                    " 时（C_final 焦窗窗权沿用）每拍小量（≤4/单、≤2 单/品/拍、"
                    "不等价峰、非脉冲）"),
                "d29_clearance": (
                    "④d29 终局分抛（D6 节奏点·顶强 38-45 张 vs 我方 22）：step "
                    "696-711 全品每拍小单分抛（追加 ≤4/单、可多单）——现行攒量"
                    "（S758 族 696 止火、718 整仓清算）改逐拍小单"),
                "d0_grain": (
                    "⑤d0 开局粒度（D6 节奏点·BUY5 d0 4-10 单 vs 我方 1）：step<24 "
                    "非原子买单拆 ≤4 小单（量守恒；HIRE/BUY_LAND 原子单不动）"
                    "——按订单粒度口径实现；若 D6 指开局买量扩张（产线面），"
                    "属净卖总量恒等禁区外议题，登记移交"),
            },
            "invariants": {
                "net_sold_identity": "净卖总量恒等（同品累计卖出量与基线一致："
                                     "拆发量守恒+追加只挂投射可卖余量+终局清算"
                                     "兜底；只改单量形态与频次——同拍内形态变化，"
                                     "零跨拍挪量）",
                "lot_sum_per_tick": "拆发前后同拍同品总量恒等（量守恒）",
                "tape_untouched": "磁带 blob 零触碰；非 SELL/不确定挂量原样保留",
                "anomaly_fallback": "异常回退宿主动作（同对象零足迹）",
            },
            "red_line": "跨拍卖量移动仍禁（R23 并单/R26 拆单七负实证）；同拍拆发"
                        "=同拍内形态变化；D6 订单粒度=唯一可抄主差距（lot med 4/"
                        "mean 6.17 → 顶强 2-4/3.68-5.04）",
            "d5_d6_target": {"lot_med": "2-4", "lot_mean": "3.68-5.04",
                             "full_exec": "0.72-0.94",
                             "d29_orders": "38-45", "d0_buy_orders": "4-10",
                             "window": "d14-20 同带（0.28-0.30）不动"},
        },
        "design": {
            "commands": ["python3 orderbook_s1form_lab/build_s_form.py",
                         "python3 orderbook_s1form_lab/judge_s_form.py"],
            "corpus": {"folds": FOLDS,
                       "spec": "674000+i*143 新块；配对面 control+2 形态 各 "
                               "n=16 双席=32 局/臂；面板 vs oc_c3 n=24 双席=48 "
                               "局、余对 n=16 双席=32 局（胜出形态）",
                       "paired_folds": F16},
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径）",
                "flips": "同 (seed,seat,对手) 配对 margin：control 胜而 variant "
                         "负记 flips_neg（判据 flips_neg=0）",
                "full_exec": "影子引擎逐单归因：requested>0 SELL 单 filled=="
                             "requested 记全清（decl 同源口径）",
                "lot": "提交口径正挂量 SELL 单 qty 直方图/均值",
                "net_sold": "影子引擎分品累计成交（filled）配对对照",
                "form_select": "配对面形态对照定主审形态：拆发形态判负（flips_neg>0"
                               " 或 mean_delta<0）→ R26 线预案启动，s_append 上主审",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
        },
        "gates": {"build": {
            f: {"checks": builds[f]["checks"],
                "sha256": builds[f]["main"]["sha256"],
                "base_sha256": builds[f]["base"]["sha256"]} for f in FORMS}},
        "panel": {}, "full_exec_stats": {}, "lot_stats": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 认证 30/30（先认证；断点缓存）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = EVID_DIR / "sim_auth_cache.json"
    if auth_cache.is_file():
        auth = json.loads(auth_cache.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth_corpus = jg.LOSS_SEEDS_26[:16] + FOLDS[:8] + \
            [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
             2026093006]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")},
            auth_corpus)
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        if auth_lite.get("consistency_ok"):
            auth_cache.write_text(json.dumps(auth, ensure_ascii=False,
                                             default=str) + "\n",
                                  encoding="utf-8")
    EV["gates"]["sim_auth"] = auth_lite
    budget["auth"] = 30
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 配对面：control + 两形态（形态对照 / R26 线判定）----
    arms = [("control", BASE)] + [(f, FORMS[f]) for f in ("s_split", "s_append")]
    rows_by_arm = {}
    for arm, path in arms:
        rows = play(_chunk_runs, specs_for(arm, path, None, None, F16), run_cfg)
        budget["paired"] += len(rows)
        rows_by_arm[arm] = rows
        bad = [r for r in rows if r.get("error")]
        if bad:
            ANOMALIES.append("paired %s: %d 局 error: %r"
                             % (arm, len(bad), bad[0].get("error")))
        print("paired", arm, "n=", len(rows), flush=True)
        flush_evid()
    key = lambda r: (r["seed"], r["seat"])  # noqa: E731
    ctl = {key(r): r for r in rows_by_arm["control"]}
    form_cmp = {}
    for form in ("s_split", "s_append"):
        var = {key(r): r for r in rows_by_arm[form]}
        pairs = []
        for k in sorted(set(ctl) | set(var)):
            rc, rv = ctl.get(k), var.get(k)
            if rc and rv and rc.get("margin_clean") is not None \
                    and rv.get("margin_clean") is not None:
                pairs.append((float(rc["margin_clean"]),
                              float(rv["margin_clean"])))
        form_cmp[form] = flip_stats(pairs)
    stats = {arm: arm_stats(rows_by_arm[arm]) for arm in rows_by_arm}
    # R26 线判定：拆发形态配对判负（flips_neg>0 或 mean_delta<0）→ 回退形态主审
    split_bad = bool(form_cmp["s_split"].get("flips_neg", 0) > 0
                     or (form_cmp["s_split"].get("mean_delta") or 0) < 0)
    winner = "s_append" if split_bad else "s_split"
    ANOMALIES.append(
        "形态对照（R26 线判定）：s_split 配对 flips_neg=%s mean_delta=%s → %s；"
        "主审形态=%s（s_split 判负即启动'多拍小单追加'预案）" % (
            form_cmp["s_split"].get("flips_neg"),
            form_cmp["s_split"].get("mean_delta"),
            "判负（回退形态上主审）" if split_bad else "未判负（主形态上主审）",
            winner))
    EV["rewrite"]["form_comparison"] = {
        "caliber": "同 (seed,seat,对手) 配对 margin（n=32 对/形态）；control="
                   "c_final",
        "flips": form_cmp,
        "stats": {a: {"full_exec": stats[a]["full_exec"]["full_exec"],
                      "mean_lot": stats[a]["lot"]["mean_lot"],
                      "n_sell_orders": stats[a]["lot"]["n_sell_orders"],
                      "d29_orders_per_game": stats[a]["lot"].get(
                          "d29_orders_per_game"),
                      "mean_margin": stats[a]["mean_margin"],
                      "stranding_mean": stats[a]["stranding_mean"]}
                  for a in stats},
        "r26_line_split_loses": split_bad,
        "panel_form": winner,
    }
    # 净卖总量恒等 + full_exec/lot 对照（按形态登记）
    inv = {}
    for form in ("control", "s_split", "s_append"):
        inv[form] = (stats[form]["full_exec"].get("filled_by_item") or {})
    inv_items = sorted(set().union(*[set(v) for v in inv.values()]))
    inv_table = {
        it: {a: inv[a].get(it, 0.0) for a in inv}
        | {"delta_split": round(inv["s_split"].get(it, 0.0)
                                - inv["control"].get(it, 0.0), 1),
           "delta_append": round(inv["s_append"].get(it, 0.0)
                                 - inv["control"].get(it, 0.0), 1)}
        for it in inv_items}
    inv_tot = {a: round(sum(inv[a].values()), 1) for a in inv}
    EV["gates"]["runtime_invariants"] = {
        "net_sold_identity": {
            "caliber": "影子引擎分品累计成交（filled）配对对照（n=32 局/臂）",
            "totals": inv_tot,
            "delta_split_vs_control": round(inv_tot["s_split"]
                                            - inv_tot["control"], 1),
            "delta_append_vs_control": round(inv_tot["s_append"]
                                             - inv_tot["control"], 1),
            "per_item": inv_table,
        },
        "stranding": {a: stats[a]["stranding_mean"] for a in stats},
        "sf_errors_total": {a: stats[a]["telemetry_sum"].get("errors", 0)
                            for a in ("s_split", "s_append")},
    }
    EV["full_exec_stats"] = {
        "caliber": "影子引擎逐单归因（decl 同源口径）；requested>0 SELL 单，"
                   "filled==requested 记全清",
        "target_band": [0.72, 0.94],
        "per_arm": {a: {k: stats[a]["full_exec"][k] for k in
                        ("n_sell_orders", "full", "partial", "full_exec",
                         "requested_qty", "filled_qty", "gap_qty")}
                    for a in stats},
        "delta_full_exec_split": (round(
            stats["s_split"]["full_exec"]["full_exec"]
            - stats["control"]["full_exec"]["full_exec"], 4)
            if stats["s_split"]["full_exec"]["full_exec"] is not None
            and stats["control"]["full_exec"]["full_exec"] is not None else None),
        "delta_full_exec_append": (round(
            stats["s_append"]["full_exec"]["full_exec"]
            - stats["control"]["full_exec"]["full_exec"], 4)
            if stats["s_append"]["full_exec"]["full_exec"] is not None
            and stats["control"]["full_exec"]["full_exec"] is not None else None),
        "shadow_mismatch_steps": {a: stats[a]["full_exec"].get(
            "shadow_mismatch_steps") for a in stats},
    }
    EV["lot_stats"] = {
        "target_band": [2, 4],
        "d5_d6_target": {"lot_med": "2-4", "lot_mean": "3.68-5.04",
                         "d29_orders": "38-45（顶强）vs 22（我方基线）"},
        "per_arm": {a: stats[a]["lot"] for a in stats},
        "sf_layer_telemetry": {a: stats[a]["telemetry_sum"]
                               for a in ("s_split", "s_append")},
    }
    flush_evid()

    # ---- 新标准面板（胜出形态）----
    panel = {}
    panel_rows = []
    for on, opath in PANEL.items():
        folds = FOLDS if on == "oc_c3" else F16
        rows = play(_chunk_runs,
                    specs_for(winner, FORMS[winner], opath, on, folds), run_cfg)
        budget["panel"] += len(rows)
        panel_rows.extend(rows)
        panel[on] = fold_stats(rows)
        print("panel", winner, "vs", on, "h2h=", panel[on]["h2h"], flush=True)
        flush_evid()
    fe_panel = full_exec_agg(panel_rows)
    lot_panel = lot_agg(panel_rows)
    EV["full_exec_stats"]["panel_form_vs_panel"] = {
        k: fe_panel[k] for k in ("n_sell_orders", "full", "partial",
                                 "full_exec", "requested_qty", "filled_qty",
                                 "gap_qty")}
    EV["lot_stats"]["panel_form_vs_panel"] = lot_panel
    EV["panel"] = {
        "design": "新标准面板：%s vs 6 对手；vs oc_c3 n=24 双席=48 局，余对 "
                  "n=16 双席=32 局（674000+i*143 新块）；h2h=judge_r44."
                  "_fold_arm；margin/终局钱只作参考" % winner,
        "form": winner,
        "pairs": panel,
    }

    # ---- 判据 + verdict ----
    h_oc = (panel.get("oc_c3") or {}).get("h2h")
    strong = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_STRONG}
    weak = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_WEAK}
    fe_v = stats[winner]["full_exec"]["full_exec"]
    fe_ctl = stats["control"]["full_exec"]["full_exec"]
    fe_band_ok = fe_v is not None and 0.72 <= fe_v <= 0.94
    mean_lot_v = stats[winner]["lot"]["mean_lot"]
    mean_lot_c = stats["control"]["lot"]["mean_lot"]
    lot_band_ok = mean_lot_v is not None and 2 <= mean_lot_v <= 4
    c1 = bool(h_oc is not None and h_oc >= 0.5)
    c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
              and len(strong) == 3)
    c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
    c4 = bool(form_cmp[winner].get("flips_neg") == 0)
    c5 = bool(fe_band_ok and lot_band_ok)
    grade = ("碾压" if (h_oc or 0) >= 0.7 else
             "强" if (h_oc or 0) >= 0.5 else "未过锚")
    full = bool(c1 and c2 and c3 and c4)
    ns_key = "delta_split_vs_control" if winner == "s_split" \
        else "delta_append_vs_control"
    ns_delta = EV["gates"]["runtime_invariants"]["net_sold_identity"][ns_key]
    EV["criteria"] = {
        "rule": "①对 oc_c3 冠军锚 ≥0.5 强/≥0.7 碾压（目标）②强面板 "
                "{mpx,tetsutani,V89} 逐对 ≥0.5 ③弱锚 {r40,A} 逐对 ≥0.8 "
                "④flips_neg=0 ⑤full_exec 对照 0.72-0.94 + 单均量对照 2-4",
        "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1,
                               "target_crush_ge_0.7": bool((h_oc or 0) >= 0.7)},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
        "c4_flips_neg_zero": {"flips": form_cmp[winner], "passed": c4},
        "c5_form_band": {
            "full_exec_variant": fe_v, "full_exec_control": fe_ctl,
            "full_exec_target": "0.72-0.94", "full_exec_in_band": fe_band_ok,
            "mean_lot_variant": mean_lot_v, "mean_lot_control": mean_lot_c,
            "mean_lot_target": "2-4", "mean_lot_in_band": lot_band_ok,
            "passed": c5},
    }
    EV["verdict"] = {
        "panel_form": winner,
        "form_sha256": builds[winner]["main"]["sha256"],
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "flips_neg": form_cmp[winner].get("flips_neg"),
        "full_exec": {"control": fe_ctl, "variant": fe_v,
                      "target": "0.72-0.94"},
        "mean_lot": {"control": mean_lot_c, "variant": mean_lot_v,
                     "target": "2-4"},
        "net_sold_identity_delta": ns_delta,
        "criteria_passed": full,
        "verdict": ("S1_SELLFORM_FULL_PASS" if full else
                    "S1_SELLFORM_ANCHOR_STRONG_BUT_PANEL_BLEED" if c1 else
                    "S1_SELLFORM_NO_POSITIVE_ARM"),
        "summary": "S_form[%s]=%s：对冠军锚 oc_c3 h2h %s（%s）；强面板 %s；弱锚 "
                   "%s；flips_neg=%s；full_exec %s→%s（目标 0.72-0.94）；单均量 "
                   "%s→%s（目标 2-4）；净卖总量 Δ=%s" % (
                       winner, builds[winner]["main"]["sha256"][:8], h_oc,
                       grade, json.dumps(strong, default=str),
                       json.dumps(weak, default=str),
                       form_cmp[winner].get("flips_neg"), fe_ctl, fe_v,
                       mean_lot_c, mean_lot_v, ns_delta),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = budget["auth"] + budget["paired"] + budget["panel"]
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP

    # ---- 异常/备注 ----
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货，"
        "margin/终局钱只作参考；影子引擎 mismatch 计步留档不修")
    ANOMALIES.append(
        "拆发=同拍内形态变化（同拍拆并语义·X1 量守恒同族）：同拍同品总量恒等；"
        "槽位 10 帽内拆发、超帽合并尾部保总量（slot_merge_* 台账）；机制备忘="
        "引擎逐单位 lockstep 按单序列对，拆发使我方后序 lot 滞后于对手同列长单"
        "余量（价格随库存下滑）——D6 粒度实证（顶强 lot 2-4）与本引擎撮合列效应"
        "存在张力，形态对照如实登记")
    ANOMALIES.append(
        "申报背书=decl_m 同序口径（钱面中立实证，2026-09-29-decl-match）：只裁"
        "虚申报（引擎断货即 abort 下的必然烂单）；全清率为副产品对照")
    ANOMALIES.append(
        "d29 分抛/平台只挂投射可卖余量（申报背书同口径）；净卖总量恒等=生产量"
        "上界+终局清算兜底（配对影子归因实测）；d29 分抛止于 711 拍（E182 终局"
        "规划器 712-718 窗零触碰，拆发量守恒亦不破其状态投影）")
    ANOMALIES.append(
        "d0 粒度按 D6'订单粒度'口径实现（开局买单拆 ≤4 小单·量守恒）；若 D6"
        "'BUY5 d0 4-10 单'实指开局买量扩张（产线面），属净卖总量恒等禁区外议题，"
        "登记移交不动手")
    if not fe_band_ok or not lot_band_ok:
        ANOMALIES.append(
            "形态副产品未全落目标带：full_exec=%s（目标 0.72-0.94）、单均量=%s"
            "（目标 2-4）；如实登记不修饰" % (fe_v, mean_lot_v))
    ANOMALIES.append(
        "断点续跑披露：正式跑前 harness 冒烟 8 局（官方引擎 2+2+2+2；含 s_split "
        "原型 vs oc_c3 fold674000 配对 −3965 边距 vs control −446——R26 线判据"
        "的前置信号，已入形态对照设计）；局次账本如实计")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；新标准以逐对口径判")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s_form_ledger.json").write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "form_comparison": EV["rewrite"]["form_comparison"],
         "panel_h2h": {k: v.get("h2h") for k, v in panel.items()},
         "full_exec": EV["full_exec_stats"],
         "lot": {k: EV["lot_stats"].get(k) for k in
                 ("per_arm", "panel_form_vs_panel")}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
