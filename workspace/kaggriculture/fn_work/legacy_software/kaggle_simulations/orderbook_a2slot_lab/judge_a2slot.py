# -*- coding: utf-8 -*-
"""judge_a2slot（a2slot lab）：A2=终局窗 HIRE 让位 SELL 快测（只测不发/在线提交=硬禁令）。

对象：h1x_a2（step∈[696,712) 剔除 HIRE，keep=0）vs H1X 本体（9d073fba…）。
诊断产物：低报价判决（orderbook_lowq_lab/evidence/lowq_verdict.json）诊断节——
槽位竞速机制链验证（step696 10 槽被 1×SELL+9×HIRE 占满 → CARROT 32+FERT 9 压次拍）。

设计（≤150 局）：
  1. 配对 vs H1X 本体（对手 oc_c3）：12 fold 双席（块 674000+i*159）+ 低报价
     seed 子集加权（lowq_verdict 用过的 12 枚 spike_ticks<900 seed 优先）
     —— delta W-L-T / mean / flips_neg
  2. KPI=槽位竞速修复：step696-712 同拍 SELL 完成量（影子引擎 d29_filled）vs
     本体应显著上升；d29_rev/终局钱 vs 本体；HIRE 损失端（herd_end/劳力产出
     hands_ops）不显著恶化
  3. 面板 vs {oc_c3 王座锚, r40, A}（6 fold 精简）+ 稳节奏 tetsutani(step1009 件)
     6 fold 双席（flips_neg=0 门）

判据：①配对 delta>0 ∧ flips_neg=0 ②同拍 SELL 完成量↑（机制门）③终局钱非负
④王座锚 h2h≥0.5 ⑤弱锚不低于基线水平（S8/H1X 系基线 r40≈0.79-0.83，floor 0.79）
⑥稳节奏零翻负 ⑦损失端不显著恶化（herd_end 不降 ∧ hands_ops 降幅<20%）。
口径：margin=终局钱 farms[obs.player] 差（干净口径）；flips=同 (seed,seat,opp)
配对 body 胜而 arm 负=flips_neg。证据 evidence/a2_verdict.json。绝不在线提交。
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

EVID_PATH = HERE / "evidence" / "a2_verdict.json"
BODY = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
ARM = HERE / "build" / "h1x_a2" / "main.py"
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
    / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
STEADY = (KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
          / "main.py")
LOWQ_VERDICT = KSIM_DIR / "orderbook_lowq_lab" / "evidence" / \
    "lowq_verdict.json"
FOLDS = [674000 + i * 159 for i in range(12)]
PANEL_FOLDS = FOLDS[:6]
STEADY_FOLDS = FOLDS[:6]
WORKERS = 8
GROOVE = -5
BUDGET_CAP = 150
SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}

EV = {}
ANOMALIES = []
BUDGET = {"cap": BUDGET_CAP}
_ROW_CACHE = {}


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ============================================================ 读数 ==
def lowq_seeds():
    """低报价 seed 子集：lowq_verdict.json 用过的 12 枚 spike_ticks<900 seed。"""
    data = json.loads(LOWQ_VERDICT.read_text(encoding="utf-8"))
    used = ((data.get("design") or {}).get("low_quote_subset") or {})
    seeds = [int(s) for s in (used.get("seeds_used") or []) if int(s)]
    rows = used.get("rows") or []
    meta = {int(r.get("seed")): r for r in rows if r.get("seed")}
    return seeds[:12], [meta.get(s, {"seed": s}) for s in seeds[:12]]


def _q(raw):
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)) and float(raw) == int(raw):
        return int(raw)
    return None


def trace_kpis(sink, seat):
    """轨迹口径 KPI：groove/采购/d29 申报/尖拍 tick/槽位与 HIRE 计数/劳力产出。"""
    groove = 0
    buy = {"orders": 0, "cost_products": 0.0, "qty_seed": 0, "qty_feed": 0,
           "qty_other_product": 0, "qty_animal": 0}
    feed_ops = 0
    d29 = {"declared_qty": 0, "declared_orders": 0, "silent_ticks_stock": 0}
    spike_ticks = 0
    fg_quotes = {"WHEAT": [], "MELON": []}
    herd_end = 0
    slot = {"win_market_orders": 0, "win_hire_orders": 0, "win_ticks": 0,
            "win_sell_qty": 0, "win_slots_full_ticks": 0,
            "hire_orders_total": 0}
    labor = {"hands_ops": 0, "hands_ops_win": 0, "hands_max": 0}
    for step, obs, act in (sink or []):
        step = int(step)
        market = ((act or {}).get("market") or []) if isinstance(act, dict) \
            else []
        prices = ((obs.get("market") or {}).get("prices") or {}) \
            if isinstance(obs, dict) else {}
        in_win = 696 <= step < 712
        # groove：step0..2 净麦 = ΣSELL(WHEAT) − ΣBUY_PRODUCT(WHEAT)
        if step <= 2:
            for e in market:
                if not isinstance(e, (list, tuple)) or len(e) < 3:
                    continue
                if e[0] == "SELL" and e[1] == "WHEAT":
                    groove += _q(e[2]) or 0
                if e[0] == "BUY_PRODUCT" and e[1] == "WHEAT":
                    groove -= _q(e[2]) or 0
        for e in market:
            if not isinstance(e, (list, tuple)) or not e:
                continue
            if e[0] == "HIRE":
                slot["hire_orders_total"] += 1
                if in_win:
                    slot["win_hire_orders"] += 1
                continue
            if len(e) < 3:
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
            elif op == "SELL" and in_win:
                d29["declared_qty"] += q
                d29["declared_orders"] += 1
                slot["win_sell_qty"] += q
        if in_win:
            slot["win_ticks"] += 1
            slot["win_market_orders"] += len(market)
            if len(market) >= 10:
                slot["win_slots_full_ticks"] += 1
        cmds = [((act or {}).get("farmer") or ["PASS"]) if isinstance(act, dict)
                else ["PASS"]]
        cmds += list((act or {}).get("hands") or []) if isinstance(act, dict) \
            else []
        n_hands = len((act or {}).get("hands") or []) \
            if isinstance(act, dict) else 0
        labor["hands_max"] = max(labor["hands_max"], n_hands)
        for c in cmds:
            if isinstance(c, (list, tuple)) and c and c[0] == "FEED":
                feed_ops += 1
            if c not in (["PASS"], "PASS") and c and c[0] != "FEED":
                pass
        hand_ops = sum(1 for c in ((act or {}).get("hands") or [])
                       if isinstance(c, (list, tuple)) and c
                       and c[0] not in ("PASS",)) \
            if isinstance(act, dict) else 0
        labor["hands_ops"] += hand_ops
        if in_win:
            labor["hands_ops_win"] += hand_ops
        # 尖拍 tick（分品绝对线 + d22 窗分位）
        shed = ((obs.get("private") or {}).get("shed") or {}) \
            if isinstance(obs, dict) else {}
        if in_win and shed and not any(
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
    slot["win_market_orders_mean"] = round(
        slot["win_market_orders"] / slot["win_ticks"], 2) \
        if slot["win_ticks"] else None
    return {"groove_net_wheat_s2": groove, "buy": buy, "feed_ops": feed_ops,
            "d29": d29, "spike_ticks_local": spike_ticks,
            "herd_end": herd_end, "slot": slot, "labor": labor}


def shadow_kpis(sinks, seed):
    """影子引擎逐单归因（decl 同源口径）：d29 同拍完成量 + 终局清算钱。"""
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
               "sell_rev_total": 0.0, "hire_spend": 0.0, "hire_success": 0}
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
            agg[pl]["hire_success"] += int((face.get("hire") or {})
                                           .get("successes") or 0)
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
                "game_id": "a2-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "shadow": block in ("fold", "lowq", "steady"),
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
            "slot.win_market_orders_mean", "slot.win_hire_orders",
            "slot.win_sell_qty", "slot.win_slots_full_ticks",
            "slot.hire_orders_total", "labor.hands_ops", "labor.hands_ops_win",
            "labor.hands_max",
            "shadow.d29_full_exec", "shadow.d29_fill_ratio",
            "shadow.d29_req", "shadow.d29_filled", "shadow.d29_rev",
            "shadow.end_rev", "shadow.sell_rev_total", "shadow.hire_spend",
            "shadow.hire_success", "end.stranding", "end.terminal_money",
            "herd_end", "spike_ticks_local")
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
    lq_seeds, lq_rows_meta = lowq_seeds()
    man = ARM.parent / "build_manifest.json"
    man_d = json.loads(man.read_text(encoding="utf-8")) if man.is_file() else {}
    EV.update({
        "version": "a2slot/1.0",
        "task": "A2=终局窗 HIRE 让位 SELL（step∈[696,712) 剔除 HIRE，keep=0）"
                "快测——低报价判决诊断产物；只测不发（在线提交=硬禁令）",
        "diagnosis": {
            "mechanism": "step696（d29 起点）10 订单槽被 1×SELL+9×HIRE 占满 → "
                         "CARROT 32+FERT 9 压到次拍才出（槽位竞速败因）；引擎 "
                         "q[:max_orders]=10 截断（kgenv.replay_profile."
                         "_s_process_market），HIRE 在 d29 近乎纯浪费还占槽",
            "online_losses": [115945260, 115957548],
            "why_not_A_arm": "A 臂只加申报无法触及槽约束——本体 d29 申报已满，"
                             "问题是槽",
        },
        "design": {
            "base": {"path": str(BODY),
                     "sha256": (man_d.get("base") or {}).get("sha256")},
            "arm": {"path": str(ARM),
                    "sha256": (man_d.get("main") or {}).get("sha256"),
                    "tar_sha256": (man_d.get("tar") or {}).get("sha256"),
                    "surgery": "step∈[696,712) 剔除 HIRE 市场单（9→0），"
                               "其余逐字不动；step≥712 零触碰"},
            "pairing": "12 fold 双席（块 674000+i*159）+ 低报价 seed 子集加权"
                       "（lowq_verdict 用过 12 枚 spike_ticks<900 seed 优先），"
                       "对手 oc_c3，同 (seed,seat) 配对 H1X 本体",
            "lowq_seeds": lq_seeds,
            "lowq_seed_rows": lq_rows_meta,
            "panel": "6 fold 精简双席 vs {oc_c3 王座锚, r40, A}"
                     "（oc_c3=配对块 12 fold 复用）",
            "steady": "tetsutani(step1009 件) 6 fold 双席（flips_neg=0 门）",
            "caliber": {"margin": "终局钱 farms[obs.player] 差（干净口径）",
                        "fold": "judge_r44._fold_arm 双席折叠",
                        "flips": "同 (seed,seat,opp) 配对：body 胜而 arm 负="
                                 "flips_neg",
                        "d29_fill": "影子引擎逐单 requested/filled"
                                    "（decl 同源，kgenv.replay_profile）"},
        },
        "build_gates": man_d.get("checks") or {},
        "criteria": {}, "verdict": {},
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

    # ---- 冒烟+确定性双跑（judge 侧）：同 seed 同席重跑比 margin ----
    smoke = mk_specs("a2", ARM, PANEL["oc_c3"], "oc_c3", [FOLDS[0]], "smoke")
    r1 = run_specs(smoke[:1], cfg)
    r2 = play(smoke[:1], cfg)          # 绕缓存重跑
    EV["gates"]["smoke"] = {
        "row1": {"margin": r1[0].get("margin_clean"), "error": r1[0].get("error")},
        "row2": {"margin": r2[0].get("margin_clean"), "error": r2[0].get("error")},
        "deterministic_ok": r1[0].get("margin_clean") == r2[0].get("margin_clean")
        and r1[0].get("error") is None}
    print("smoke", EV["gates"]["smoke"], flush=True)
    flush_evid()

    # ---- 本体对照行（共享）：fold 块 + 低报价子集 + 稳节奏 ----
    body_rows = {}
    body_rows["fold"] = run_specs(
        mk_specs("body", BODY, PANEL["oc_c3"], "oc_c3", FOLDS, "fold"), cfg)
    print("body fold done", flush=True)
    flush_evid()
    body_rows["lowq"] = run_specs(
        mk_specs("body", BODY, PANEL["oc_c3"], "oc_c3", lq_seeds, "lowq"), cfg)
    print("body lowq done", flush=True)
    flush_evid()
    body_rows["steady"] = run_specs(
        mk_specs("body", BODY, STEADY, "tetsutani", STEADY_FOLDS, "steady"),
        cfg)
    print("body steady done", flush=True)
    flush_evid()

    t_arm = time.perf_counter()
    blk = {"path": str(ARM), "paired": {}, "panel": {}, "steady": {},
           "kpi": {}, "groove_gate": {}, "loss_side": {}}
    arm_rows = {}
    arm_rows["fold"] = run_specs(
        mk_specs("a2", ARM, PANEL["oc_c3"], "oc_c3", FOLDS, "fold"), cfg)
    arm_rows["lowq"] = run_specs(
        mk_specs("a2", ARM, PANEL["oc_c3"], "oc_c3", lq_seeds, "lowq"), cfg)
    pr_fold = pairs_from(body_rows["fold"], arm_rows["fold"])
    pr_lowq = pairs_from(body_rows["lowq"], arm_rows["lowq"])
    pr_all = pr_fold + pr_lowq
    blk["paired"] = {
        "design": "12 fold（674000+i*159）+ 低报价 12 seed 子集（加权优先），"
                  "双席 vs oc_c3，同 (seed,seat) 配对 H1X 本体",
        "fold_block": flip_table(pr_fold),
        "lowq_subset": flip_table(pr_lowq),
        "pooled": flip_table(pr_all),
        "fold_body": fold(body_rows["fold"]), "fold_arm": fold(arm_rows["fold"]),
        "lowq_body": fold(body_rows["lowq"]), "lowq_arm": fold(arm_rows["lowq"]),
    }
    print("paired pooled", blk["paired"]["pooled"]["mean_delta"],
          "flips_neg", blk["paired"]["pooled"]["flips_neg"], flush=True)
    flush_evid()

    # 面板：oc_c3=配对 fold 块 arm 行复用；r40 / A 6 fold
    blk["panel"]["oc_c3"] = blk["paired"]["fold_arm"]
    for on in ("r40", "A"):
        rows = run_specs(
            mk_specs("a2", ARM, PANEL[on], on, PANEL_FOLDS, "panel"), cfg)
        arm_rows["panel_" + on] = rows
        blk["panel"][on] = fold(rows)
        print("panel", on, blk["panel"][on].get("h2h"), flush=True)
        flush_evid()

    # 稳节奏 6 fold 双席
    arm_rows["steady"] = run_specs(
        mk_specs("a2", ARM, STEADY, "tetsutani", STEADY_FOLDS, "steady"), cfg)
    pr_s = pairs_from(body_rows["steady"], arm_rows["steady"])
    blk["steady"] = {"fold_arm": fold(arm_rows["steady"]),
                     "fold_body": fold(body_rows["steady"]),
                     "flips": flip_table(pr_s)}
    print("steady flips_neg", blk["steady"]["flips"]["flips_neg"], flush=True)
    flush_evid()

    # KPI 对表（配对块合并面）
    rows_body_all = body_rows["fold"] + body_rows["lowq"]
    rows_arm_all = arm_rows["fold"] + arm_rows["lowq"]
    blk["kpi"] = kpi_table(rows_body_all, rows_arm_all)
    blk["kpi_lowq_only"] = kpi_table(body_rows["lowq"], arm_rows["lowq"])
    # groove 门：step2 净麦恰 −5（全局 arm 行）
    grooves = []
    for rr in (arm_rows["fold"], arm_rows["lowq"], arm_rows["steady"],
               arm_rows.get("panel_r40") or [], arm_rows.get("panel_A") or []):
        for r in rr:
            g = ((r.get("kpi") or {}).get("groove_net_wheat_s2"))
            if g is not None:
                grooves.append(g)
    bad = [g for g in grooves if g != GROOVE]
    blk["groove_gate"] = {"rule": "step2 净麦（ΣSELL WHEAT − ΣBUY_PRODUCT "
                                  "WHEAT，step0..2）恰 −5", "n": len(grooves),
                          "n_bad": len(bad), "bad_values": bad[:5],
                          "passed": (not bad) and bool(grooves)}
    # HIRE 损失端（herd_end/劳力产出）不显著恶化
    kpi = blk["kpi"]
    herd_b, herd_a = kpi["herd_end"]["body"], kpi["herd_end"]["arm"]
    lab_b, lab_a = kpi["labor.hands_ops"]["body"], kpi["labor.hands_ops"]["arm"]
    blk["loss_side"] = {
        "rule": "fail-closed：herd_end 不降 ∧ 劳力产出 hands_ops 降幅 <20% 本体",
        "herd_end": {"body": herd_b, "arm": herd_a,
                     "delta": kpi["herd_end"]["delta"]},
        "hands_ops": {"body": lab_b, "arm": lab_a,
                      "delta": kpi["labor.hands_ops"]["delta"]},
        "hire_spend": kpi["shadow.hire_spend"],
        "passed": bool(herd_b is not None and herd_a is not None
                       and lab_b is not None and lab_a is not None
                       and herd_a >= herd_b and lab_a >= 0.8 * lab_b),
    }
    blk["rows"] = {"fold": arm_rows["fold"], "lowq": arm_rows["lowq"],
                   "steady": arm_rows["steady"],
                   "panel_r40": arm_rows.get("panel_r40"),
                   "panel_A": arm_rows.get("panel_A")}
    blk["elapsed_s"] = round(time.perf_counter() - t_arm, 1)
    EV["arms"] = {"a2": blk}
    flush_evid()

    # ---- 判据 ----
    fl_all = blk["paired"]["pooled"]
    c1 = bool((fl_all.get("mean_delta") or 0) > 0
              and fl_all.get("flips_neg") == 0)
    fill_d = (kpi.get("shadow.d29_filled") or {}).get("delta")
    rev_d = (kpi.get("shadow.d29_rev") or {}).get("delta")
    tm_d = (kpi.get("end.terminal_money") or {}).get("delta")
    c2 = bool(fill_d is not None and fill_d > 0)
    c3 = bool(tm_d is not None and tm_d >= 0)
    h_oc = (blk["panel"].get("oc_c3") or {}).get("h2h")
    c4 = bool(h_oc is not None and h_oc >= 0.5)
    h_r40 = (blk["panel"].get("r40") or {}).get("h2h")
    h_a = (blk["panel"].get("A") or {}).get("h2h")
    c5 = bool(h_r40 is not None and h_a is not None
              and h_r40 >= 0.79 and h_a >= 0.79)
    c6 = bool(blk["steady"]["flips"].get("flips_neg") == 0)
    c7 = bool(blk["loss_side"]["passed"])
    extra_ok = blk["groove_gate"]["passed"]
    full = bool(c1 and c2 and c3 and c4 and c5 and c6 and c7 and extra_ok)
    EV["criteria"] = {
        "rule": "①配对 delta>0 ∧ flips_neg=0 ②同拍 SELL 完成量↑（机制门）"
                "③终局钱非负 ④王座锚 h2h≥0.5 ⑤弱锚≥基线 floor0.79 "
                "⑥稳节奏零翻负 ⑦损失端不显著恶化",
        "c1_paired_delta_pos_flips0": {
            "pooled": {"mean_delta": fl_all.get("mean_delta"),
                       "W": fl_all.get("W"), "L": fl_all.get("L"),
                       "T": fl_all.get("T"),
                       "flips_neg": fl_all.get("flips_neg")},
            "fold_block": {"mean_delta": blk["paired"]["fold_block"]
                           .get("mean_delta"),
                           "W": blk["paired"]["fold_block"].get("W"),
                           "L": blk["paired"]["fold_block"].get("L"),
                           "T": blk["paired"]["fold_block"].get("T"),
                           "flips_neg": blk["paired"]["fold_block"]
                           .get("flips_neg")},
            "lowq_subset": {"mean_delta": blk["paired"]["lowq_subset"]
                            .get("mean_delta"),
                            "W": blk["paired"]["lowq_subset"].get("W"),
                            "L": blk["paired"]["lowq_subset"].get("L"),
                            "T": blk["paired"]["lowq_subset"].get("T"),
                            "flips_neg": blk["paired"]["lowq_subset"]
                            .get("flips_neg")},
            "passed": c1},
        "c2_same_tick_sell_filled_up": {
            "d29_filled": kpi.get("shadow.d29_filled"),
            "d29_rev": kpi.get("shadow.d29_rev"),
            "d29_full_exec": kpi.get("shadow.d29_full_exec"),
            "win_sell_qty_trace": kpi.get("slot.win_sell_qty"),
            "passed": c2},
        "c3_terminal_money_nonneg": {"end.terminal_money": kpi.get(
            "end.terminal_money"), "passed": c3},
        "c4_throne_anchor_ge_0.5": {"h2h_oc_c3": h_oc, "passed": c4},
        "c5_weak_anchors_baseline": {"h2h_r40": h_r40, "h2h_A": h_a,
                                     "floor": 0.79,
                                     "baseline_band": "0.79-0.83",
                                     "passed": c5},
        "c6_steady_flips_neg_0": {"flips_neg": blk["steady"]["flips"]
                                  .get("flips_neg"),
                                  "mean_delta": blk["steady"]["flips"]
                                  .get("mean_delta"), "passed": c6},
        "c7_hire_loss_side": {"detail": blk["loss_side"], "passed": c7},
        "extra_groove_gate": {"groove": blk["groove_gate"],
                              "passed": extra_ok},
        "all_passed": full,
    }
    EV["verdict"] = {
        "all_passed": full,
        "mechanism_confirmed": c2,
        "slot_race_fix": {"win_hire_orders": kpi.get("slot.win_hire_orders"),
                          "win_slots_full_ticks": kpi.get(
                              "slot.win_slots_full_ticks"),
                          "win_market_orders_mean": kpi.get(
                              "slot.win_market_orders_mean"),
                          "d29_filled": kpi.get("shadow.d29_filled")},
        "summary": {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5,
                    "c6": c6, "c7": c7, "groove": extra_ok},
        "launch": "只测不发（在线提交=硬禁令）；诊断产物=低报价判决诊断节，"
                  "发射决策移交主会话",
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE) + 1  # +1 = 绕缓存确定性重跑
    BUDGET["within_cap"] = BUDGET["unique_games_run"] <= BUDGET_CAP
    EV["body_rows"] = {"fold": body_rows["fold"], "lowq": body_rows["lowq"],
                       "steady": body_rows["steady"]}
    ANOMALIES.append("低报价 seed 来自 lowq_verdict.json 用过的 12 枚 "
                     "spike_ticks<900 seed（线上败局优先）；对手换本地锚 oc_c3"
                     "（线上对手不可复刻），故为 seed 级加权而非对手匹配")
    ANOMALIES.append("d29 同拍完成量/成交额口径=影子引擎逐单 requested/filled"
                     "（decl 同源，kgenv.replay_profile）；trace 侧 slot 计数=最终"
                     "行动市场单（post-处理后），body 窗内 HIRE>0 / arm=0 互证")
    ANOMALIES.append("槽位机制：引擎 q[:maxOrders]=10 截断，行动列表顺序即槽位"
                     "优先级；剔除 HIRE 后尾部 SELL 前移进 10 槽窗")
    ANOMALIES.append("groove 口径沿 S3/tape1：step2 净麦=ΣSELL WHEAT − "
                     "ΣBUY_PRODUCT WHEAT（step0..2 累计，种子腿不计）")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT", EV["verdict"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
