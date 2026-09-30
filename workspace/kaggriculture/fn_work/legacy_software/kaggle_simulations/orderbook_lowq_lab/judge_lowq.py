# -*- coding: utf-8 -*-
"""judge_lowq（lowq lab）：低报价世界双臂池测（只测不发/在线提交=硬禁令）。

对象：lowq_a（d29 全清申报校准）/ lowq_b（中盘买侧减负）vs S8 本体（a59208fe…）。
口径：judge_r44._fold_arm 双席折叠、margin=farms[obs.player]（终局钱差）、
块 674000+i*159（i=0..11）；低报价子集=fn_docs/hybrid/results/
2026-10-01-h1x-online-read.json 里 spike_ticks<900 的线上 seed（优先败局 seed）。

池测（每臂 112 局 + 共享 S8 本体对照 64 局；全局去重 288 局次）：
  1. 低报价子集配对 vs S8 本体（12 seed×2 席 vs oc_c3）——主判据
  2. 面板 12 fold 双席 vs {oc_c3 王座锚, r40, A}（弱锚 ≥0.8 门；oc_c3 另跑本体配对）
  3. 稳节奏对手 tetsutani(step1009 件) 8 fold 双席（flips_neg=0 门，配对本体）
  4. KPI 对表：A=d29 全清率/终局清算钱；B=采购成本+groove 门+饲料/种子预算不穿底

判据（两臂独立）：①配对 delta>0 ∧ flips_neg=0 ②KPI 改善 ③王座锚 h2h≥0.5
  ④弱锚 h2h≥0.8 ⑤稳节奏零翻负；B 另加 groove 门（step2 净麦恰 −5，破即 REJECT）
  与 anti 饿死 fail-closed（feed/seed 预算不穿底）。
证据 evidence/lowq_verdict.json（逐局行+KPI 对表）。不提交/不发射/不在线。
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

EVID_PATH = HERE / "evidence" / "lowq_verdict.json"
BODY = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
ARMS = {"a": HERE / "build" / "s8_a" / "main.py",
        "b": HERE / "build" / "s8_b" / "main.py"}
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
    / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
STEADY = (KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
          / "main.py")
ONLINE_READ = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-10-01-h1x-online-read.json"
FOLDS = [674000 + i * 159 for i in range(12)]
STEADY_FOLDS = FOLDS[:8]
WORKERS = 4
GROOVE = -5
SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}

EV = {}
ANOMALIES = []
BUDGET = {"cap_per_arm": 220}
_ROW_CACHE = {}


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ============================================================ 读数 ==
def low_quote_seeds():
    """低报价世界 seed 清单（spike_ticks<900，seed≠0）：败局 seed 优先。"""
    data = json.loads(ONLINE_READ.read_text(encoding="utf-8"))
    rows = data.get("per_game_rows") or []
    out = []
    for r in rows:
        seed = int(r.get("seed") or 0)
        ticks = int(((r.get("spike") or {}).get("spike_ticks_total")) or 0)
        if seed and ticks < 900:
            out.append({"seed": seed, "ep": r.get("episode_id"),
                        "result": r.get("result"),
                        "margin_online": r.get("margin"),
                        "spike_ticks_online": ticks})
    out.sort(key=lambda d: (d["result"] != "L", d["seed"]))
    return out


def _q(raw):
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)) and float(raw) == int(raw):
        return int(raw)
    return None


def trace_kpis(sink, seat):
    """轨迹口径 KPI（不依赖影子引擎）：groove/采购/d29 申报/尖拍 tick。"""
    groove = 0
    buy = {"orders": 0, "cost_products": 0.0, "qty_seed": 0, "qty_feed": 0,
           "qty_other_product": 0, "qty_animal": 0}
    feed_ops = 0
    d29 = {"declared_qty": 0, "declared_orders": 0, "silent_ticks_stock": 0}
    spike_ticks = 0
    fg_quotes = {"WHEAT": [], "MELON": []}
    herd_end = 0
    for step, obs, act in (sink or []):
        step = int(step)
        market = ((act or {}).get("market") or []) if isinstance(act, dict) \
            else []
        prices = ((obs.get("market") or {}).get("prices") or {}) \
            if isinstance(obs, dict) else {}
        day = step // 24
        # groove：step0..2 净麦 = ΣSELL(WHEAT) − ΣBUY_PRODUCT(WHEAT)
        if step <= 2:
            for e in market:
                if not isinstance(e, (list, tuple)) or len(e) < 3:
                    continue
                if e[0] == "SELL" and e[1] == "WHEAT":
                    groove += _q(e[2]) or 0
                if e[0] == "BUY_PRODUCT" and e[1] == "WHEAT":
                    groove -= _q(e[2]) or 0
        # 采购（申报口径：qty×当时报价）
        for e in market:
            if not isinstance(e, (list, tuple)) or len(e) < 3:
                continue
            op, item = e[0], e[1]
            q = _q(e[2]) or 0
            if op == "BUY_SEED":
                buy["orders"] += 1
                buy["qty_seed"] += q
                buy["cost_products"] += q * float(prices.get(item, 0) or 0)
            elif op == "BUY_PRODUCT":
                buy["orders"] += 1
                buy["cost_products"] += q * float(prices.get(item, 0) or 0)
                if item == "WHEAT":
                    buy["qty_feed"] += q
                else:
                    buy["qty_other_product"] += q
            elif op == "BUY_ANIMAL":
                buy["orders"] += 1
                buy["qty_animal"] += q
            elif op == "SELL" and 696 <= step < 712:
                d29["declared_qty"] += q
                d29["declared_orders"] += 1
        cmds = [((act or {}).get("farmer") or ["PASS"]) if isinstance(act, dict)
                else ["PASS"]]
        cmds += list((act or {}).get("hands") or []) if isinstance(act, dict) \
            else []
        for c in cmds:
            if isinstance(c, (list, tuple)) and c and c[0] == "FEED":
                feed_ops += 1
        # 尖拍 tick（分品绝对线 + d22 窗分位）
        shed = ((obs.get("private") or {}).get("shed") or {}) \
            if isinstance(obs, dict) else {}
        if 696 <= step < 712 and shed and not any(
                isinstance(e, (list, tuple)) and len(e) >= 3 and e[0] == "SELL"
                for e in market):
            d29["silent_ticks_stock"] += 1
        spiking = 0
        for item, line in (("WOOL", 144.0), ("MILK", 124.0)):
            if float(prices.get(item, 0) or 0) >= line:
                spiking += 1
        for item in ("WHEAT", "MELON"):
            q = float(prices.get(item, 0) or 0)
            if q > 0:
                fg_quotes[item].append(q)
            if 528 <= step < 552 and len(fg_quotes[item]) >= 6:
                srt = sorted(fg_quotes[item])
                idx = int(0.75 * (len(srt) - 1) + 0.9999) - 1
                if q >= srt[max(0, idx)]:
                    spiking += 1
        spike_ticks += spiking
        if isinstance(obs, dict):
            farm = (obs.get("farms") or [{}])[int(obs.get("player", 0) or 0)]
            tiles = (farm or {}).get("tiles") or []
            herd_end = sum(1 for row in tiles for t in row
                           if isinstance(t, dict) and "animal" in t)
    return {"groove_net_wheat_s2": groove, "buy": buy, "feed_ops": feed_ops,
            "d29": d29, "spike_ticks_local": spike_ticks,
            "herd_end": herd_end, "day_by_day": None}


def shadow_kpis(sinks, seed):
    """影子引擎逐单归因（decl 同源口径）：d29 全清率 + 终局清算钱。"""
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
        state = rp._s_snapshot(pre0, [pre0.get("private"), pre1.get("private")])
    except Exception as exc:
        return {"error": "snapshot: %r" % exc}
    agg = {p: {"d29_orders": 0, "d29_full": 0, "d29_req": 0.0,
               "d29_filled": 0.0, "d29_rev": 0.0, "end_rev": 0.0,
               "sell_rev_total": 0.0, "hire_spend": 0.0}
           for p in (0, 1)}
    for s in steps:
        acts = [m[0].get(s, (None, None))[1], m[1].get(s, (None, None))[1]]
        acts = [a if isinstance(a, dict) else
                {"farmer": ["PASS"], "hands": [], "market": []} for a in acts]
        try:
            _, attr = rp._s_step(state, acts, s, SHADOW_CFG, int(seed))
        except Exception:
            nxt = s + 1
            n0 = m[0].get(nxt, (None, None))[0]
            n1 = m[1].get(nxt, (None, None))[0]
            if n0 and n1:
                try:
                    state = rp._s_snapshot(n0, [n0.get("private"),
                                                n1.get("private")])
                except Exception:
                    pass
            continue
        for pl in (0, 1):
            try:
                face = attr["market"][pl]
            except Exception:
                continue
            agg[pl]["hire_spend"] += float((face.get("hire") or {})
                                           .get("spend") or 0)
            for o in (face.get("orders") or []):
                if o.get("type") != "SELL":
                    continue
                filled = float(o.get("filled") or 0)
                value = float(o.get("value") or 0)
                req = float(o.get("requested") or 0)
                agg[pl]["sell_rev_total"] += value
                if 696 <= s < 712:
                    agg[pl]["d29_orders"] += 1
                    agg[pl]["d29_req"] += req
                    agg[pl]["d29_filled"] += filled
                    agg[pl]["d29_rev"] += value
                    if req > 0 and abs(filled - req) < 1e-9:
                        agg[pl]["d29_full"] += 1
                if s >= 696:
                    agg[pl]["end_rev"] += value
        nxt = s + 1
        n0 = m[0].get(nxt, (None, None))[0]
        n1 = m[1].get(nxt, (None, None))[0]
        if n0 and n1:
            try:
                state = rp._s_snapshot(n0, [n0.get("private"),
                                            n1.get("private")])
            except Exception:
                pass
    out = {}
    for pl in (0, 1):
        a = agg[pl]
        a["d29_full_exec"] = round(a["d29_full"] / a["d29_orders"], 4) \
            if a["d29_orders"] else None
        a["d29_fill_ratio"] = round(a["d29_filled"] / a["d29_req"], 4) \
            if a["d29_req"] else None
        for k in ("d29_req", "d29_filled", "d29_rev", "end_rev",
                  "sell_rev_total", "hire_spend"):
            a[k] = round(a[k], 1)
        out[str(pl)] = a
    return out


# ============================================================ 跑口 ==
def _chunk_runs(payload):
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
        if row["margin_clean"] is None and row["banks"] is not None:
            try:
                b = row["banks"]
                row["margin_clean"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
        if our is not None:
            try:
                row["kpi"] = trace_kpis(sinks[row["seat"]], row["seat"])
                row["kpi"]["end"] = jsf.end_reads(sinks[row["seat"]])
            except Exception as exc:
                row["kpi_error"] = repr(exc)[:100]
            if spec.get("shadow", True):
                try:
                    sh = shadow_kpis(sinks, int(spec["seed"]))
                    row["shadow"] = sh
                    if isinstance(sh, dict) and not sh.get("error"):
                        row["kpi"]["shadow"] = sh.get(str(row["seat"]))
                except Exception as exc:
                    row["shadow_error"] = repr(exc)[:100]
        rows.append(row)
    return rows


def play(specs, cfg, shadow=True):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {}), "shadow": shadow}
             for i in range(n)]
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


def run_specs(specs, cfg, shadow=True):
    out, todo = [], []
    for spec in specs:
        key = (spec["arm_path"], int(spec["seed"]), int(spec["our_seat"]),
               spec["opp_path"])
        if key in _ROW_CACHE:
            out.append(_ROW_CACHE[key])
        else:
            todo.append((key, spec))
    if todo:
        rows = play([s for _, s in todo], cfg, shadow=shadow)
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


def mk_specs(arm, arm_path, opp_path, opp_name, seeds, block):
    specs = []
    for seed in seeds:
        for seat in (0, 1):
            specs.append({
                "game_id": "lowq-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "shadow": block in ("lq", "steady"),
                "trace": True})
    return specs


def pairs_from(rows_c, rows_v):
    key = lambda r: (r["seed"], r["seat"], r.get("opponent"))  # noqa: E731
    mc = {key(r): r for r in rows_c if r.get("margin_clean") is not None}
    mv = {key(r): r for r in rows_v if r.get("margin_clean") is not None}
    return [(float(mc[k]["margin_clean"]), float(mv[k]["margin_clean"]), k)
            for k in sorted(set(mc) & set(mv))]


def flip_table(pairs):
    agg = jsf.flip_stats([(a, b) for a, b, _ in pairs])
    agg["pairs_detail"] = [
        {"seed": k[0], "seat": k[1], "opp": k[2], "margin_body": round(a, 1),
         "margin_arm": round(b, 1), "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold(rows):
    try:
        return jsf.fold_stats(rows)
    except Exception as exc:
        return {"error": repr(exc)[:120]}


def mean_kpi(rows, path):
    vals = []
    for r in rows:
        node = r.get("kpi") or {}
        for part in path.split("."):
            node = (node or {}).get(part) if isinstance(node, dict) else None
        if isinstance(node, (int, float)) and not isinstance(node, bool):
            vals.append(float(node))
    return round(sum(vals) / len(vals), 4) if vals else None


def kpi_table(rows_body, rows_arm):
    """KPI 对表（同 (seed,seat,opp) 配对面均值；Δ=arm−body）。"""
    keys = ("groove_net_wheat_s2", "buy.cost_products", "buy.qty_feed",
            "buy.qty_seed", "buy.qty_other_product", "buy.qty_animal",
            "buy.orders", "feed_ops", "d29.declared_qty",
            "d29.declared_orders", "d29.silent_ticks_stock",
            "shadow.d29_full_exec", "shadow.d29_fill_ratio",
            "shadow.d29_req", "shadow.d29_filled", "shadow.d29_rev",
            "shadow.end_rev", "shadow.sell_rev_total", "shadow.hire_spend",
            "end.stranding", "end.terminal_money", "herd_end",
            "spike_ticks_local")
    out = {}
    for k in keys:
        b, a = mean_kpi(rows_body, k), mean_kpi(rows_arm, k)
        out[k] = {"body": b, "arm": a,
                  "delta": (round(a - b, 4) if (a is not None
                                                and b is not None) else None)}
    return out


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    lq = low_quote_seeds()
    lq_seeds = [d["seed"] for d in lq][:12]
    builds = {}
    for arm, path in ARMS.items():
        man = (path.parent / "build_manifest.json")
        builds[arm] = json.loads(man.read_text(encoding="utf-8")) \
            if man.is_file() else {}
    EV.update({
        "version": "lowq/1.0",
        "task": "低报价世界胜率两臂池测（A=d29 全清申报校准 / B=中盘买侧减负）；"
                "只测不发（在线提交=硬禁令）",
        "design": {
            "base": {"path": str(BODY), "sha256": "a59208fe…（构建门校验）"},
            "arms": {k: {"path": str(v),
                         "sha256": (builds.get(k) or {}).get("main", {})
                         .get("sha256")} for k, v in ARMS.items()},
            "low_quote_subset": {"online_world_split":
                                 "lo_spike_world(spiketicks<900) 15 局 8W/7L "
                                 "mean +918（vs 尖价世界 10W/2L +27.6k）",
                                 "seeds_used": lq_seeds, "rows": lq},
            "panel": "12 fold（674000+i*159）双席 vs {oc_c3 王座锚, r40, A}",
            "steady": "tetsutani(step1009 件) 8 fold 双席（flips_neg=0 门）",
            "caliber": {"margin": "终局钱 farms[obs.player] 差（干净口径）",
                        "fold": "judge_r44._fold_arm 双席折叠",
                        "flips": "同 (seed,seat,opp) 配对：body 胜而 arm 负="
                                 "flips_neg"},
        },
        "build_gates": {k: (v.get("checks") or {}) for k, v in builds.items()},
        "arms": {}, "criteria": {}, "verdict": {},
    })
    flush_evid()

    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    if auth_cache.is_file():
        auth = json.loads(auth_cache.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine",
                      "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth = sb.sim_bridge({"n_games": 30, "min_checked": 30}, FOLDS[:8])
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine")}
    EV["gates"] = {"sim_auth": auth_lite}
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 冒烟 2 局（确定性双跑：同 seed 同席重跑比 margin）----
    smoke = mk_specs("s8_b", ARMS["b"], PANEL["oc_c3"], "oc_c3",
                     [FOLDS[0]], "smoke")
    r1 = run_specs(smoke[:1], cfg)
    r2 = play(smoke[:1], cfg)          # 绕缓存重跑
    EV["gates"]["smoke"] = {
        "row1": {"margin": r1[0].get("margin_clean"), "error": r1[0].get("error")},
        "row2": {"margin": r2[0].get("margin_clean"), "error": r2[0].get("error")},
        "deterministic_ok": r1[0].get("margin_clean") == r2[0].get("margin_clean")
        and r1[0].get("error") is None}
    print("smoke", EV["gates"]["smoke"], flush=True)
    flush_evid()

    # ---- 本体对照行（共享）：低报价子集 + 稳节奏 + 面板 oc_c3 列 ----
    body_rows = {}
    body_rows["lq"] = run_specs(
        mk_specs("body", BODY, PANEL["oc_c3"], "oc_c3", lq_seeds, "lq"), cfg)
    print("body lq done", flush=True)
    flush_evid()
    body_rows["steady"] = run_specs(
        mk_specs("body", BODY, STEADY, "tetsutani", STEADY_FOLDS, "steady"),
        cfg)
    print("body steady done", flush=True)
    flush_evid()
    body_rows["panel_oc_c3"] = run_specs(
        mk_specs("body", BODY, PANEL["oc_c3"], "oc_c3", FOLDS, "panel"), cfg)
    print("body panel done", flush=True)
    flush_evid()

    for arm, apath in ARMS.items():
        t_arm = time.perf_counter()
        blk = {"path": str(apath), "lq_paired": {}, "panel": {}, "steady": {},
               "kpi": {}, "groove_gate": {}, "anti_starvation": {}}
        arm_rows = {}
        arm_rows["lq"] = run_specs(
            mk_specs(arm, apath, PANEL["oc_c3"], "oc_c3", lq_seeds, "lq"), cfg)
        pr = pairs_from(body_rows["lq"], arm_rows["lq"])
        blk["lq_paired"] = {"design": "低报价 seed 12×双席 vs oc_c3，同 "
                                      "(seed,seat) 配对 S8 本体",
                            "flips": flip_table(pr),
                            "fold_body": fold(body_rows["lq"]),
                            "fold_arm": fold(arm_rows["lq"])}
        print(arm, "lq paired", blk["lq_paired"]["flips"]["mean_delta"],
              flush=True)
        flush_evid()

        # 面板 12 fold × 3 对手
        for on, opath in PANEL.items():
            rows = run_specs(
                mk_specs(arm, apath, opath, on, FOLDS, "panel"), cfg)
            arm_rows["panel_" + on] = rows
            blk["panel"][on] = fold(rows)
            if on == "oc_c3":
                pr_p = pairs_from(body_rows["panel_oc_c3"], rows)
                blk["panel"]["oc_c3_paired_vs_body"] = flip_table(pr_p)
            print(arm, "panel", on, blk["panel"][on].get("h2h"), flush=True)
            flush_evid()

        # 稳节奏 8 fold
        arm_rows["steady"] = run_specs(
            mk_specs(arm, apath, STEADY, "tetsutani", STEADY_FOLDS, "steady"),
            cfg)
        pr_s = pairs_from(body_rows["steady"], arm_rows["steady"])
        blk["steady"] = {"fold_arm": fold(arm_rows["steady"]),
                         "fold_body": fold(body_rows["steady"]),
                         "flips": flip_table(pr_s)}
        print(arm, "steady", blk["steady"]["flips"]["flips_neg"], flush=True)
        flush_evid()

        # KPI 对表（低报价子集配对面）
        blk["kpi"] = kpi_table(body_rows["lq"], arm_rows["lq"])
        # groove 门：全局面 step2 净麦恰 −5
        grooves = []
        for rows in (arm_rows.values(),):
            for rr in rows:
                for r in rr:
                    g = ((r.get("kpi") or {}).get("groove_net_wheat_s2"))
                    if g is not None:
                        grooves.append(g)
        bad = [g for g in grooves if g != GROOVE]
        blk["groove_gate"] = {"rule": "step2 净麦（ΣSELL WHEAT − ΣBUY_PRODUCT "
                                      "WHEAT，step0..2）恰 −5", "n": len(grooves),
                              "n_bad": len(bad), "bad_values": bad[:5],
                              "passed": (not bad) and bool(grooves)}
        # anti 饿死 fail-closed：饲料/种子预算不穿底（vs 本体）
        feed_b, feed_a = mean_kpi(body_rows["lq"], "buy.qty_feed"), \
            mean_kpi(arm_rows["lq"], "buy.qty_feed")
        seed_b, seed_a = mean_kpi(body_rows["lq"], "buy.qty_seed"), \
            mean_kpi(arm_rows["lq"], "buy.qty_seed")
        fops_b, fops_a = mean_kpi(body_rows["lq"], "feed_ops"), \
            mean_kpi(arm_rows["lq"], "feed_ops")
        blk["anti_starvation"] = {
            "rule": "fail-closed：feed 采购量/FEED 供给量/种子采购量 vs 本体"
                    "不得穿底（A 臂应恒等；B 臂 feed≥本体 0.95 且 seed 恒等）",
            "feed_qty": {"body": feed_b, "arm": feed_a},
            "feed_ops": {"body": fops_b, "arm": fops_a},
            "seed_qty": {"body": seed_b, "arm": seed_a},
        }
        blk["anti_starvation"]["passed"] = bool(
            feed_a is not None and feed_b is not None
            and seed_a is not None and seed_b is not None
            and feed_a >= 0.95 * feed_b and fops_a >= 0.95 * fops_b
            and seed_a == seed_b)
        blk["rows"] = {"lq": arm_rows["lq"], "steady": arm_rows["steady"],
                       "panel": {k: v for k, v in arm_rows.items()
                                 if k.startswith("panel_")}}
        EV["arms"][arm] = blk
        blk["elapsed_s"] = round(time.perf_counter() - t_arm, 1)
        flush_evid()

    # ---- 判据（两臂独立）----
    crit = {}
    for arm, blk in EV["arms"].items():
        fl = blk["lq_paired"]["flips"]
        kpi = blk["kpi"]
        c1 = bool((fl.get("mean_delta") or 0) > 0 and fl.get("flips_neg") == 0)
        if arm == "a":
            fe_d = (kpi.get("shadow.d29_full_exec") or {}).get("delta")
            rv_d = (kpi.get("shadow.d29_rev") or {}).get("delta")
            ok_fe = fe_d is not None and fe_d >= 0
            ok_rv = rv_d is not None and rv_d > 0
            c2 = bool((ok_fe and ok_rv) or (fe_d is not None and fe_d > 0
                                            and rv_d is not None and rv_d >= 0))
            kpi_detail = {"d29_full_exec_delta": fe_d, "d29_rev_delta": rv_d,
                          "end_rev_delta": (kpi.get("shadow.end_rev") or {})
                          .get("delta")}
        else:
            cost_d = (kpi.get("buy.cost_products") or {}).get("delta")
            c2 = bool(cost_d is not None and cost_d < 0)
            kpi_detail = {"buy_cost_delta": cost_d,
                          "buy_qty_feed_delta": (kpi.get("buy.qty_feed") or {})
                          .get("delta"),
                          "buy_qty_other_delta": (kpi.get(
                              "buy.qty_other_product") or {}).get("delta"),
                          "buy_qty_animal_delta": (kpi.get(
                              "buy.qty_animal") or {}).get("delta")}
        h_oc = (blk["panel"].get("oc_c3") or {}).get("h2h")
        c3 = bool(h_oc is not None and h_oc >= 0.5)
        h_r40 = (blk["panel"].get("r40") or {}).get("h2h")
        h_a = (blk["panel"].get("A") or {}).get("h2h")
        c4 = bool(h_r40 is not None and h_a is not None and h_r40 >= 0.8
                  and h_a >= 0.8)
        c5 = bool(blk["steady"]["flips"].get("flips_neg") == 0)
        extra_ok = blk["groove_gate"]["passed"] and \
            blk["anti_starvation"]["passed"]
        full = bool(c1 and c2 and c3 and c4 and c5 and extra_ok)
        crit[arm] = {
            "rule": "①配对 delta>0 ∧ flips_neg=0 ②KPI 改善 ③王座锚 h2h≥0.5 "
                    "④弱锚 h2h≥0.8 ⑤稳节奏零翻负（B 另加 groove/anti 饿死门）",
            "c1_paired_delta_pos_flips0": {"mean_delta": fl.get("mean_delta"),
                                           "W": fl.get("W"), "L": fl.get("L"),
                                           "T": fl.get("T"),
                                           "flips_neg": fl.get("flips_neg"),
                                           "passed": c1},
            "c2_kpi_improved": {"detail": kpi_detail, "passed": c2},
            "c3_throne_anchor_ge_0.5": {"h2h_oc_c3": h_oc, "passed": c3},
            "c4_weak_anchors_ge_0.8": {"h2h_r40": h_r40, "h2h_A": h_a,
                                       "passed": c4},
            "c5_steady_flips_neg_0": {"flips_neg": blk["steady"]["flips"]
                                      .get("flips_neg"),
                                      "mean_delta": blk["steady"]["flips"]
                                      .get("mean_delta"), "passed": c5},
            "extra_groove_and_anti_starvation": {
                "groove": blk["groove_gate"], "anti": blk["anti_starvation"],
                "passed": extra_ok},
            "all_passed": full,
        }
    EV["criteria"] = crit
    passed = [a for a, c in crit.items() if c.get("all_passed")]
    kpi_up = [a for a, c in crit.items()
              if c["c2_kpi_improved"].get("passed")]
    EV["verdict"] = {
        "arms_passed": passed,
        "arms_kpi_improved": kpi_up,
        "port_to_h1x": passed or kpi_up,
        "summary": {a: {"all_passed": c["all_passed"],
                        "c1": c["c1_paired_delta_pos_flips0"]["passed"],
                        "c2": c["c2_kpi_improved"]["passed"],
                        "c3": c["c3_throne_anchor_ge_0.5"]["passed"],
                        "c4": c["c4_weak_anchors_ge_0.8"]["passed"],
                        "c5": c["c5_steady_flips_neg_0"]["passed"]}
                    for a, c in crit.items()},
        "launch": "只测不发（在线提交=硬禁令）；发射决策与 H1X 侧验证移交主会话",
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE)
    BUDGET["per_arm"] = {
        a: sum(1 for k in _ROW_CACHE
               if k[0].endswith("/s8_%s/main.py" % a)) for a in ARMS}
    BUDGET["body_control_games"] = sum(
        1 for k in _ROW_CACHE if k[0].endswith("/s8/main.py"))
    EV["body_rows"] = body_rows
    ANOMALIES.append("低报价 seed 来自线上 27 局世界分类（spike_ticks<900，"
                     "seed=0 验证局剔除）；对手换本地锚（线上对手不可复刻），"
                     "故为 seed 级加权而非对手匹配")
    ANOMALIES.append("d29 全清率/成交额口径=影子引擎逐单 requested/filled"
                     "（decl 同源，kgenv.replay_profile）；采购成本=申报口径 "
                     "qty×当时报价（动物单价不在报价表，另计 qty）")
    ANOMALIES.append("groove 口径沿 S3/tape1：step2 净麦=ΣSELL WHEAT − "
                     "ΣBUY_PRODUCT WHEAT（step0..2 累计，种子腿不计）")
    ANOMALIES.append("B 臂 WHEAT 采购纳入温和减负（'非饲料'落地为 fail-closed "
                     "门而非豁免；豁免口径会使可动面仅 FERTILIZER≈490/局）")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT", EV["verdict"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
