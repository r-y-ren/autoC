# -*- coding: utf-8 -*-
"""judge_spikeopt（尖拍追加量参数优化 lab）：s8a/s8b vs S8 本体池测（不发射/不提交）。

对象：A 档 lot 3-6（build/s8a）、B 档 lot 4-8（build/s8b），手术=spike_append
lot 帽单行（其余逐字不动）；对照=S8 本体（orderbook_s8spike_lab/build/s8）。
池测（12 fold 双席，块 674000+i*159，judge_r44._fold_arm 折叠，margin=farms[
obs.player] 终局钱差；每档预算 ≤250 局）：
  1. 配对增量 vs S8 本体（同 (seed,seat,opp) 逐 unit）：delta W-L-T+mean+
     flips_neg/pos——主判据；
  2. 捕获 KPI：spike 窗 capture_rate_qty/量缺口（同局重放口径 vs S8 对照，
     机制必须改善）+ 层 telemetry（skip_slot 槽压/append 形态）；
  3. 面板：vs {oc_c3,H1 王座锚, r40, A}（12 fold 双席 h2h）；
  4. 毒种 5 枚（674000/674141/674705/674987/675410，各 {mpx,oc_c3}×双席
     =4 局配对 S8）——不许回退（S8 毒种 20/20 核心 KPI）；
  5. 稳节奏对手（tetsutani/tetsu1009 件 8 fold 双席）——flips_neg=0。
全过判据：①配对 delta>0 ∧ flips_neg=0 ②capture_rate_qty↑ ③王座锚 ≥0.5
④弱锚 ≥0.8 ⑤毒种不回退 ⑥稳节奏 flips_neg=0。A/B 都过取小档 A（除非 B 显著
更优：delta 多 ≥50%）。工程面：五门已过（build_spikeopt）+确定性双跑抽查
2 局；证据 evidence/spikeopt_verdict.json（逐局行+捕获 KPI 对表）。
margin 口径=终局钱 farms[obs.player]（jsf.end_reads）；fold=judge_r44._fold_arm。
只写 orderbook_spikeopt_lab/。绝不在线提交。
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
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab"),
          str(KSIM_DIR / "orderbook_s1form_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用（Tracer/flip/fold）
from orderbook_r44 import judge_r44 as j44  # noqa: E402  _fold_arm 折叠口径

EVID_DIR = HERE / "evidence"
OUT_PATH = EVID_DIR / "spikeopt_verdict.json"

S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
ARMS = {"A": HERE / "build" / "s8a" / "main.py",
        "B": HERE / "build" / "s8b" / "main.py"}
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py",
    "H1": KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
}
THRONE = ("oc_c3", "H1")            # 王座锚
WEAK = ("r40", "A")                 # 弱锚
POISON_SEEDS = [674000, 674141, 674705, 674987, 675410]
POISON_OPPS = ("mpx", "oc_c3")
FOLDS_12 = [674000 + i * 159 for i in range(12)]
FOLDS_8 = [674000 + i * 159 for i in range(8)]
PAIRED_CYCLE = ("oc_c3", "mpx", "tetsutani", "V89", "r40", "A")
WORKERS = 12
BUDGET_CAP = 250                    # 每档

EV = {}
ANOMALIES = []
BUDGET = {}
_ROW_CACHE = {}                     # (arm_path,seed,seat,opp_path) -> row


def flush():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = {k: dict(v) for k, v in BUDGET.items()}
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")


# ================================================== 捕获 KPI 重放口径 ==
_ABS = {"WOOL": 144.0, "MILK": 124.0}
_FG = ("WHEAT", "MELON")
_FG_WIN = (528, 552)
_FG_Q, _FG_N = 0.75, 6


def _qty(raw):
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _sell_qty(act, item):
    tot = 0
    for e in (act or {}).get("market") or []:
        if isinstance(e, (list, tuple)) and len(e) >= 3 and e[0] == "SELL" \
                and e[1] == item:
            q = _qty(e[2])
            if q and q > 0:
                tot += q
    return tot


def spike_capture(sinks, our_seat, mirror_layer):
    """spike 窗捕获 KPI（声明单代理口径=线上体检同款）：
    capture_rate_qty=our/(our+opp)；miss=我 0 对手>0；under=我<对手；
    量缺口=miss_qty+under_units（件）+价值缺口（quote 计）。
    mirror_layer=True 时判定/直方图镜像层（step<712、逐日重置、含当拍）。"""
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for e in sinks.get(seat) or []:
            m[seat][int(e[0])] = (e[1], e[2])
    steps = sorted(set(m[0]) | set(m[1]))
    day, hist = -1, {}
    agg = {"spike_item_ticks": 0, "our_spike_qty": 0.0, "opp_spike_qty": 0.0,
           "miss_ticks": 0, "miss_qty": 0.0, "under_ticks": 0,
           "under_units": 0.0, "miss_value": 0.0, "under_value": 0.0,
           "per_item": {}}
    for s in steps:
        if mirror_layer and s >= 712:
            continue
        obs = m[our_seat].get(s, (None, None))[0] or \
            m[1 - our_seat].get(s, (None, None))[0] or {}
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        d = s // 24
        if day != d:
            day, hist = d, {}
        sp = {}
        for item, line in _ABS.items():
            try:
                q = float(prices.get(item))
            except (TypeError, ValueError):
                continue
            if q >= line:
                sp[item] = q
        for item in _FG:
            try:
                q = float(prices.get(item))
            except (TypeError, ValueError):
                continue
            h = hist.setdefault(item, [])
            h.append(q)
            if _FG_WIN[0] <= s < _FG_WIN[1] and len(h) >= _FG_N:
                srt = sorted(h)
                idx = -(-75 * len(srt) // 100) - 1
                line = srt[min(max(idx, 0), len(srt) - 1)]
                if q >= line:
                    sp[item] = q
        for item, q in sp.items():
            a_us = _sell_qty(m[our_seat].get(s, (None, None))[1], item)
            a_op = _sell_qty(m[1 - our_seat].get(s, (None, None))[1], item)
            agg["spike_item_ticks"] += 1
            agg["our_spike_qty"] += a_us
            agg["opp_spike_qty"] += a_op
            row = agg["per_item"].setdefault(
                item, {"ticks": 0, "our": 0.0, "opp": 0.0})
            row["ticks"] += 1
            row["our"] += a_us
            row["opp"] += a_op
            if a_us == 0 and a_op > 0:
                agg["miss_ticks"] += 1
                agg["miss_qty"] += a_op
                agg["miss_value"] += a_op * q
            elif 0 < a_us < a_op:
                agg["under_ticks"] += 1
                agg["under_units"] += a_op - a_us
                agg["under_value"] += (a_op - a_us) * q
    tot = agg["our_spike_qty"] + agg["opp_spike_qty"]
    agg["capture_rate_qty"] = round(agg["our_spike_qty"] / tot, 4) \
        if tot > 0 else None
    agg["gap_qty"] = round(agg["miss_qty"] + agg["under_units"], 1)
    agg["gap_value"] = round(agg["miss_value"] + agg["under_value"], 1)
    return agg


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱 farms[obs.player] + 捕获 KPI + 影子/lot/telemetry。"""
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
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec["our_seat"]), "arm": spec["arm"],
               "opponent": spec.get("opponent"), "block": spec.get("block"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "tm_us": None, "tm_opp": None,
               "telemetry": jsf._snap_telemetry(our) if our is not None
               else None,
               "capture": None, "capture_lt712": None,
               "shadow": None, "end": None, "lot": None}
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
                row["capture"] = spike_capture(sinks, row["seat"], False)
                row["capture_lt712"] = spike_capture(sinks, row["seat"], True)
            except Exception as exc:
                row["capture_error"] = repr(exc)[:100]
            try:
                row["shadow"] = jsf.shadow_books(sinks, int(spec["seed"]))
            except Exception as exc:
                row["shadow"] = {"error": repr(exc)[:120]}
            row["lot"] = jsf.lot_reads(sinks[row["seat"]])
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
    """去重跑口：同 (arm_path,seed,seat,opp_path) 只跑一次（A/B/S8 共享）。"""
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
            _ROW_CACHE[key] = row
            out.append(row)
    return out


def mk_specs(arm, arm_path, opp_path, opp_name, folds, block, seats=(0, 1)):
    return [{"game_id": "so-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
             "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
             "our_seat": seat, "opp_path": str(opp_path),
             "opponent": opp_name, "block": block, "kind": "ab",
             "trace": True}
            for seed in folds for seat in seats]


# ============================================================ 读数 ==
def pairs_from(rows_c, rows_v):
    key = lambda r: (r["seed"], r["seat"], r.get("opponent"))  # noqa: E731
    mc = {key(r): r for r in rows_c if r.get("margin_clean") is not None}
    mv = {key(r): r for r in rows_v if r.get("margin_clean") is not None}
    return [(float(mc[k]["margin_clean"]), float(mv[k]["margin_clean"]), k)
            for k in sorted(set(mc) & set(mv))]


def flip_table(pairs):
    agg = jsf.flip_stats([(a, b) for a, b, _ in pairs])
    agg["pairs_detail"] = [
        {"seed": k[0], "seat": k[1], "opp": k[2],
         "margin_s8": round(a, 1), "margin_arm": round(b, 1),
         "delta": round(b - a, 1)} for a, b, k in pairs]
    return agg


def fold_of(rows):
    """judge_r44._fold_arm 折叠（margin=farms[obs.player]）。"""
    rr = [{"seed": r["seed"], "margin": r.get("margin_clean")} for r in rows]
    f = j44._fold_arm(rr)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def cap_agg(rows, key="capture"):
    tot = {"games": 0, "spike_item_ticks": 0, "our_spike_qty": 0.0,
           "opp_spike_qty": 0.0, "miss_ticks": 0, "miss_qty": 0.0,
           "under_ticks": 0, "under_units": 0.0, "miss_value": 0.0,
           "under_value": 0.0}
    per_item = {}
    for r in rows:
        c = r.get(key)
        if not isinstance(c, dict):
            continue
        tot["games"] += 1
        for k in ("spike_item_ticks", "our_spike_qty", "opp_spike_qty",
                  "miss_ticks", "miss_qty", "under_ticks", "under_units",
                  "miss_value", "under_value"):
            tot[k] += float(c.get(k) or 0)
        for it, row in (c.get("per_item") or {}).items():
            d = per_item.setdefault(it, {"ticks": 0, "our": 0.0, "opp": 0.0})
            d["ticks"] += int(row.get("ticks") or 0)
            d["our"] += float(row.get("our") or 0)
            d["opp"] += float(row.get("opp") or 0)
    s = tot["our_spike_qty"] + tot["opp_spike_qty"]
    tot["capture_rate_qty"] = round(tot["our_spike_qty"] / s, 4) if s else None
    tot["gap_qty"] = round(tot["miss_qty"] + tot["under_units"], 1)
    tot["gap_value"] = round(tot["miss_value"] + tot["under_value"], 1)
    tot["per_item"] = {k: {**v, "our": round(v["our"], 1),
                           "opp": round(v["opp"], 1)}
                       for k, v in sorted(per_item.items())}
    for k in ("our_spike_qty", "opp_spike_qty", "miss_qty", "under_units",
              "miss_value", "under_value"):
        tot[k] = round(tot[k], 1)
    return tot


def tel_agg(rows):
    tot = {}
    for r in rows:
        for k, v in (r.get("telemetry") or {}).items():
            if isinstance(v, (int, float)):
                tot[k] = tot.get(k, 0) + v
    return tot


def lot_of(rows):
    return jsf.lot_agg(rows)


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    builds = {f: json.load(open(HERE / "build" / ("s8%s" % f.lower())
                                / "build_manifest.json")) for f in ("A", "B")}
    s8_manifest = json.load(open(KSIM_DIR / "orderbook_s8spike_lab" / "build"
                                 / "s8" / "build_manifest.json"))
    EV.update({
        "version": "spikeopt/1.0",
        "task": "尖拍追加量参数上调（lot 2-4→A 3-6/B 4-8）池测：配对增量 vs S8 "
                "本体+捕获 KPI+面板+毒种+稳节奏（只测不发，在线提交=硬禁令）",
        "origin": "H1X 线上体检 2026-10-01-h1x-online-read.json：败局 "
                  "115945260（d16 尖价窗量缺口/漏捕 1122）、115948784（d26 尖价 "
                  "2877 vs 5265，量缺口 3590）→ lot 帽+topup 空间在高量竞速拍偏薄",
        "design": {
            "formula": "s8a = S8(a59208fe…) 单行手术 lot(2,4)→(3,6)；"
                       "s8b = 同手术 (4,8)；其余逐字不动（anti-幻影硬线/槽位 10 帽/"
                       "step≥712/加卖不挪卖/decl_topup）",
            "artifacts": {f: {"main_sha256": builds[f]["main"]["sha256"],
                              "tar_sha256": builds[f]["tar"]["sha256"],
                              "lot": builds[f]["spike_params"]["lot"],
                              "checks": builds[f]["checks"]}
                          for f in ("A", "B")},
            "s8_base": {"main_sha256": s8_manifest["main"]["sha256"]},
            "corpus": {
                "paired": "12 fold=674000+i*159 双席 vs 6 对手轮转"
                          "（oc_c3/mpx/tetsutani/V89/r40/A），同 (seed,seat,opp)"
                          " 逐 unit 配对 vs S8 本体",
                "panel": "vs {oc_c3,H1 王座锚, r40, A}×12 fold 双席",
                "poison": "五毒种各 {mpx,oc_c3}×双席=4 局配对 S8",
                "steady": "tetsutani/tetsu1009 8 fold 双席配对 S8"},
            "caliber": {
                "margin": "终局钱 farms[obs.player] 差（干净口径）",
                "fold": "judge_r44._fold_arm（双席折叠独立局）",
                "paired": "flip_stats：delta W-L-T+mean+flips_neg/pos（主判据）",
                "capture": "spike 窗声明单代理（线上体检同款）："
                           "capture_rate_qty=our/(our+opp)；miss=我 0 对手>0；"
                           "under=我<对手；量缺口=miss_qty+under_units（件）；"
                           "win_all=全区镜像线上口径，win_lt712=层窗（step<712）",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考"},
        },
        "gates": {"build_A": builds["A"]["checks"],
                  "build_B": builds["B"]["checks"]},
        "determinism_spotcheck": {},
        "paired": {}, "capture_kpi": {}, "panel": {}, "poison": {},
        "steady": {}, "criteria": {}, "verdict": {},
    })
    flush()

    # ---- sim_bridge 认证（复用 s1form 认证缓存）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    auth = json.loads(auth_cache.read_text(encoding="utf-8"))
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version", "wall_speedup")}
    auth_lite["reused_cache"] = True
    EV["gates"]["sim_auth"] = auth_lite
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证缓存未过"}
        flush()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 确定性双跑抽查 2 局（每档 1 局×2 次，bank 逐位一致）----
    det = {}
    for f, path in ARMS.items():
        spec = mk_specs(f, path, PANEL["oc_c3"], "oc_c3", [FOLDS_12[0]],
                        "det")[:1]
        r1 = play(spec, run_cfg)
        r2 = play(spec, run_cfg)
        same = (r1 and r2 and r1[0].get("banks") == r2[0].get("banks")
                and r1[0].get("margin_clean") == r2[0].get("margin_clean"))
        det[f] = {"game_id": spec[0]["game_id"],
                  "banks_run1": r1[0].get("banks") if r1 else None,
                  "banks_run2": r2[0].get("banks") if r2 else None,
                  "identical": bool(same)}
    EV["determinism_spotcheck"] = det
    flush()
    print("det spotcheck", det, flush=True)

    for f, path in ARMS.items():
        BUDGET[f] = {"paired": 0, "panel": 0, "poison": 0, "steady": 0,
                     "smoke_det": 2, "s8_shared": 0}
        arm_lbl = "s8%s" % f.lower()

        # ---- 冒烟 2 局（同 1 中前 2 局，纳入配对块缓存）----
        smoke = mk_specs(arm_lbl, path, PANEL["oc_c3"], "oc_c3",
                         [FOLDS_12[0]], "smoke")[:2]
        run_specs(smoke, run_cfg)
        print("smoke", f, flush=True)

        # ---- 1. 配对增量 vs S8 本体（12 fold 双席×6 对手轮转）----
        specs_v, specs_c = [], []
        for j, seed in enumerate(FOLDS_12):
            on = PAIRED_CYCLE[j % len(PAIRED_CYCLE)]
            specs_v += mk_specs(arm_lbl, path, PANEL[on], on, [seed],
                                "paired")
            specs_c += mk_specs("s8", S8, PANEL[on], on, [seed], "paired")
        rows_v = run_specs(specs_v, run_cfg)
        rows_c = run_specs(specs_c, run_cfg)
        BUDGET[f]["paired"] = len(specs_v)
        BUDGET[f]["s8_shared"] += len(specs_c)
        pairs = pairs_from(rows_c, rows_v)
        ft = flip_table(pairs)
        EV["paired"][f] = {
            "design": "同 (seed,seat,opp) 逐 unit 配对（control=S8 本体, "
                      "variant=s8%s）；12 fold 双席×6 对手轮转=24 局/臂" % f,
            "flip": ft,
            "fold_variant": fold_of(rows_v), "fold_s8": fold_of(rows_c)}
        print("paired", f, "mean_delta", ft["mean_delta"], "W/L/T",
              ft["W"], ft["L"], ft["T"], "flips_neg", ft["flips_neg"],
              flush=True)

        # ---- 2. 捕获 KPI（同局重放 vs S8 对照）----
        cap_v = cap_agg(rows_v)
        cap_c = cap_agg(rows_c)
        cap_v7 = cap_agg(rows_v, "capture_lt712")
        cap_c7 = cap_agg(rows_c, "capture_lt712")
        EV["capture_kpi"][f] = {
            "caliber": "spike 窗声明单代理（线上体检同款口径）；同 (seed,seat,"
                       "opp) 配对局双臂对照",
            "win_all": {"variant_s8%s" % f: cap_v, "control_s8": cap_c,
                        "delta_capture_rate": round(
                            (cap_v["capture_rate_qty"] or 0)
                            - (cap_c["capture_rate_qty"] or 0), 4),
                        "delta_gap_qty": round(
                            cap_v["gap_qty"] - cap_c["gap_qty"], 1)},
            "win_lt712_layer": {
                "variant_s8%s" % f: cap_v7, "control_s8": cap_c7,
                "delta_capture_rate": round(
                    (cap_v7["capture_rate_qty"] or 0)
                    - (cap_c7["capture_rate_qty"] or 0), 4),
                "delta_gap_qty": round(cap_v7["gap_qty"] - cap_c["gap_qty"],
                                       1)},
            "telemetry_variant": tel_agg(rows_v),
            "telemetry_s8": tel_agg(rows_c),
            "lot_variant": lot_of(rows_v), "lot_s8": lot_of(rows_c)}
        print("capture", f, cap_v["capture_rate_qty"], "vs",
              cap_c["capture_rate_qty"], "gap", cap_v["gap_qty"], "vs",
              cap_c["gap_qty"], flush=True)
        flush()

        # ---- 3. 面板：vs {oc_c3,H1,r40,A}×12 fold 双席 ----
        panel = {"design": "s8%s vs 4 对手（12 fold 双席）；h2h=judge_r44."
                           "_fold_arm 折叠" % f, "pairs": {}}
        for on in ("oc_c3", "H1", "r40", "A"):
            rows = run_specs(mk_specs(arm_lbl, path, PANEL[on], on,
                                      FOLDS_12, "panel"), run_cfg)
            panel["pairs"][on] = fold_of(rows)
            BUDGET[f]["panel"] += len(FOLDS_12) * 2
            print("panel", f, on, panel["pairs"][on]["h2h"], flush=True)
        EV["panel"][f] = panel

        # ---- 4. 毒种（5 枚×{mpx,oc_c3}×双席配对 S8）----
        po_v, po_c = [], []
        for seed in POISON_SEEDS:
            for on in POISON_OPPS:
                po_v += mk_specs(arm_lbl, path, PANEL[on], on, [seed],
                                 "poison")
                po_c += mk_specs("s8", S8, PANEL[on], on, [seed], "poison")
        rows_pov = run_specs(po_v, run_cfg)
        rows_poc = run_specs(po_c, run_cfg)
        BUDGET[f]["poison"] = len(po_v)
        BUDGET[f]["s8_shared"] += len(po_c)
        pairs_po = pairs_from(rows_poc, rows_pov)
        EV["poison"][f] = {
            "design": "五毒种各 4 局（{mpx,oc_c3}×双席）配对 S8 本体；不许回退",
            "flip": flip_table(pairs_po),
            "per_seed": {}}
        for seed in POISON_SEEDS:
            ps = [p for p in pairs_po if p[2][0] == seed]
            ft_po = flip_table(ps)
            EV["poison"][f]["per_seed"][str(seed)] = {
                "n_pairs": ft_po["n"], "W": ft_po["W"], "L": ft_po["L"],
                "T": ft_po["T"], "mean_delta": ft_po["mean_delta"],
                "flips_neg": ft_po["flips_neg"]}
        print("poison", f, flip_table(pairs_po)["mean_delta"], flush=True)

        # ---- 5. 稳节奏（tetsutani/tetsu1009 8 fold 双席配对 S8）----
        st_v = mk_specs(arm_lbl, path, PANEL["tetsutani"], "tetsutani",
                        FOLDS_8, "steady")
        st_c = mk_specs("s8", S8, PANEL["tetsutani"], "tetsutani", FOLDS_8,
                        "steady")
        rows_stv = run_specs(st_v, run_cfg)
        rows_stc = run_specs(st_c, run_cfg)
        BUDGET[f]["steady"] = len(st_v)
        BUDGET[f]["s8_shared"] += len(st_c)
        pairs_st = pairs_from(rows_stc, rows_stv)
        EV["steady"][f] = {
            "design": "tetsutani/tetsu1009 稳节奏对手 8 fold 双席配对 S8；"
                      "S9 扰动教训：加量不许伤稳节奏",
            "flip": flip_table(pairs_st),
            "fold_variant": fold_of(rows_stv)}
        print("steady", f, flip_table(pairs_st)["flips_neg"], flush=True)

        # ---- 逐局行（配对块+面板+毒种+稳节奏）----
        seen, per_game = set(), []
        for r in rows_v + rows_pov + rows_stv:
            key = (r["seed"], r["seat"], r.get("opponent"), r["arm"])
            if key in seen:
                continue
            seen.add(key)
            c = r.get("capture") or {}
            per_game.append({
                "game_id": r.get("game_id"), "block": r.get("block"),
                "seed": r["seed"], "seat": r["seat"], "arm": r["arm"],
                "opp": r.get("opponent"),
                "margin_clean": r.get("margin_clean"),
                "tm_us": r.get("tm_us"), "tm_opp": r.get("tm_opp"),
                "error": r.get("error"),
                "capture_rate_qty": c.get("capture_rate_qty"),
                "gap_qty": c.get("gap_qty"),
                "our_spike_qty": c.get("our_spike_qty"),
                "opp_spike_qty": c.get("opp_spike_qty")})
        EV.setdefault("per_game_rows", {})[f] = per_game
        BUDGET[f]["total_局次"] = (BUDGET[f]["paired"] + BUDGET[f]["panel"]
                                   + BUDGET[f]["poison"] + BUDGET[f]["steady"]
                                   + BUDGET[f]["smoke_det"])
        BUDGET[f]["total_with_s8_shared"] = (BUDGET[f]["total_局次"]
                                             + BUDGET[f]["s8_shared"])
        BUDGET[f]["within_cap"] = BUDGET[f]["total_with_s8_shared"] \
            <= BUDGET_CAP
        flush()

    # ---- 判据 + verdict（逐档六门）----
    for f in ARMS:
        ft = EV["paired"][f]["flip"]
        cap = EV["capture_kpi"][f]
        d_cr = cap["win_all"]["delta_capture_rate"]
        d_gap = cap["win_all"]["delta_gap_qty"]
        throne = {on: (EV["panel"][f]["pairs"].get(on) or {}).get("h2h")
                  for on in THRONE}
        weak = {on: (EV["panel"][f]["pairs"].get(on) or {}).get("h2h")
                for on in WEAK}
        po = EV["poison"][f]["flip"]
        st = EV["steady"][f]["flip"]
        c1 = bool((ft["mean_delta"] or 0) > 0 and ft["flips_neg"] == 0)
        c2 = bool(d_cr is not None and d_cr > 0)
        c3 = bool(all((h or 0) >= 0.5 for h in throne.values()))
        c4 = bool(all((h or 0) >= 0.8 for h in weak.values()))
        c5 = bool(po["flips_neg"] == 0 and (po["mean_delta"] or 0) >= 0)
        c6 = bool(st["flips_neg"] == 0)
        checks = {
            "c1_paired_delta_pos_flipsneg0": {
                "mean_delta": ft["mean_delta"], "W": ft["W"], "L": ft["L"],
                "T": ft["T"], "flips_pos": ft["flips_pos"],
                "flips_neg": ft["flips_neg"], "passed": c1},
            "c2_capture_rate_up": {
                "delta_capture_rate": d_cr, "delta_gap_qty": d_gap,
                "variant": cap["win_all"].get("variant_s8%s" % f),
                "s8": cap["win_all"].get("control_s8"), "passed": c2},
            "c3_throne_anchor_ge_0.5": {"h2h": throne, "passed": c3},
            "c4_weak_anchor_ge_0.8": {"h2h": weak, "passed": c4},
            "c5_poison_no_regression": {
                "mean_delta": po["mean_delta"], "W": po["W"], "L": po["L"],
                "flips_neg": po["flips_neg"],
                "passed": c5},
            "c6_steady_flipsneg0": {
                "mean_delta": st["mean_delta"], "W": st["W"], "L": st["L"],
                "flips_neg": st["flips_neg"], "passed": c6}}
        EV["criteria"][f] = {"checks": checks,
                             "achieved": sum(1 for c in checks.values()
                                             if c["passed"]),
                             "total": 6,
                             "verdict": "PASS" if all(c["passed"] for c in
                                                       checks.values())
                             else "FAIL"}

    passes = [f for f in ("A", "B") if EV["criteria"][f]["verdict"] == "PASS"]
    da = EV["paired"]["A"]["flip"]["mean_delta"] or 0
    db = EV["paired"]["B"]["flip"]["mean_delta"] or 0
    pick, rationale = None, ""
    if passes == ["A", "B"]:
        if db >= 1.5 * da and db > 0:
            pick, rationale = "B", ("双档全过；B 显著更优（delta %s ≥ 1.5×A %s）"
                                    % (db, da))
        else:
            pick, rationale = "A", ("双档全过；取小档 A（B delta %s 未达 A %s 的 "
                                    "1.5 倍）" % (db, da))
    elif passes:
        pick, rationale = passes[0], "仅 %s 档全过" % passes[0]
    else:
        pick, rationale = "A", "两档均未全过（移植仍取 A 档，见判读）"

    EV["verdict"] = {
        "arm_pass": {f: EV["criteria"][f]["verdict"] for f in ("A", "B")},
        "launch_candidate_arm": pick,
        "selection_rationale": rationale,
        "paired_mean_delta": {"A": da, "B": db},
        "launch_ready": bool(passes),
        "launch_note": ("发射候选成立（%s 档）；只测不发，在线提交=硬禁令，"
                        "上线决策移交用户" % pick) if passes else
                       "无全过档：机制结论如实登记，不构成发射候选",
        "transplant_h1x_arm": pick,
        "h1x_note": "用户裁决 2026-10-01：胜者档（或都不过则 A 档）同手术移植 "
                    "H1X（build/h1x_<arm>/），H1X 侧验证由主会话安排",
    }
    ANOMALIES.append("harness 噪声不修不管；margin=终局钱 farms[obs.player]；"
                     "胜率=硬通货，margin 只作参考；影子引擎 mismatch 留档不修")
    ANOMALIES.append("捕获 KPI 为声明单代理口径（线上体检同款）：真实成交异步结算；"
                     "同 (seed,seat,opp) 配对双臂对照读增量")
    ANOMALIES.append("手术=单行 lot 帽（_S8_LOT_MIN,_S8_LOT_MAX）；其余逐字不动"
                     "（anti-幻影硬线/槽位 10 帽/step≥712/加卖不挪卖/decl_topup）；"
                     "尾块 docstring 中 'lot 2-4' 字样为历史注释未改（参数以 "
                     "_S8_PARAMS['lot'] 为准）")
    ANOMALIES.append("每档预算≤250 局：S8 对照局按共享计账（A/B 共用缓存去重）")
    ANOMALIES.append("毒种判据=不回退（配对 vs S8 flips_neg=0 ∧ mean_delta≥0）；"
                     "S8 毒种 20/20（vs s_append）为核心 KPI 背景")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush()
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str), flush=True)
    print("CRITERIA:", json.dumps({f: EV["criteria"][f]["verdict"]
                                   for f in ("A", "B")}), flush=True)
    print("DONE", EV["elapsed_s"], "s", flush=True)
    return EV


def validate_h1x_b():
    """H1X 侧快速验证（用户裁决 2026-10-01 重裁判据，B 档入候选）：
    h1x_b vs H1X 本体同块配对（12 fold 双席，674000+i*159，6 对手轮转）
    + 毒种 5 枚精简（每枚 2 局配对 H1X 对照，均值口径）+ 弱锚 r40/A（各 6 fold，
    基线=H1X 本体同读数）。判读：配对 delta>0 ∧ flips_neg=0 ∧ 毒种均值不回退
    ∧ 弱锚不低于 H1X 基线水平。预算 ≤180 局。只读/只测，绝不在线。"""
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    H1X = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
    H1XB = HERE / "build" / "h1x_b" / "main.py"
    bm = json.load(open(HERE / "build" / "h1x_b" / "build_manifest.json"))
    EV.setdefault("h1x_b_validation", {})
    out = EV["h1x_b_validation"] = {
        "version": "h1x-b-validate/1.0",
        "readjudication": "用户裁决 2026-10-01 终窗：毒种门重裁为均值不回退"
                          "（B +6.3 过）、弱锚门重裁为基线相对不回退（0.79=基线"
                          "水平过）→ B 档（lot 4-8）入发射候选",
        "design": {
            "arm": "h1x_b = H1X(9d073fba…) 单行手术 lot(2,4)→(4,8)；control=H1X 本体",
            "artifacts": {"main_sha256": bm["main"]["sha256"],
                          "tar_sha256": bm["tar"]["sha256"],
                          "lot": bm["spike_params"]["lot"],
                          "checks": bm["checks"]},
            "corpus": {"paired": "12 fold=674000+i*159 双席×6 对手轮转，同 "
                                 "(seed,seat,opp) 配对 vs H1X 本体",
                       "poison": "五毒种各 2 局（mpx×双席）配对 H1X 对照（均值口径）",
                       "weak": "r40/A 各 6 fold 双席；基线=H1X 本体同局"},
            "caliber": {"margin": "终局钱 farms[obs.player] 差",
                        "fold": "judge_r44._fold_arm（双席折叠）",
                        "paired": "flip_stats：delta W-L-T+mean+flips_neg/pos"},
        },
        "budget_cap_局次": 180,
    }
    flush()
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth = json.loads((KSIM_DIR / "orderbook_s1form_lab" / "evidence"
                       / "sim_auth_cache.json").read_text(encoding="utf-8"))
    if not auth.get("consistency_ok"):
        out["verdict"] = {"aborted": "sim_bridge 认证缓存未过"}
        flush()
        return out
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    budget = 0

    # ---- 1. 同块配对 vs H1X 本体（12 fold 双席×6 对手轮转）----
    specs_v, specs_c = [], []
    for j, seed in enumerate(FOLDS_12):
        on = PAIRED_CYCLE[j % len(PAIRED_CYCLE)]
        specs_v += mk_specs("h1x_b", H1XB, PANEL[on], on, [seed], "paired")
        specs_c += mk_specs("h1x_ctl", H1X, PANEL[on], on, [seed], "paired")
    rows_v = run_specs(specs_v, run_cfg)
    rows_c = run_specs(specs_c, run_cfg)
    budget += len(specs_v) + len(specs_c)
    pairs = pairs_from(rows_c, rows_v)
    ft = flip_table(pairs)
    out["paired"] = {"flip": ft,
                     "fold_h1x_b": fold_of(rows_v),
                     "fold_h1x_ctl": fold_of(rows_c)}
    print("h1xb paired mean_delta", ft["mean_delta"], "W/L/T", ft["W"],
          ft["L"], ft["T"], "flips_neg", ft["flips_neg"], flush=True)

    # ---- 2. 毒种 5 枚精简（每枚 2 局 mpx×双席，配对 H1X 对照，均值口径）----
    po_v, po_c = [], []
    for seed in POISON_SEEDS:
        po_v += mk_specs("h1x_b", H1XB, PANEL["mpx"], "mpx", [seed], "poison")
        po_c += mk_specs("h1x_ctl", H1X, PANEL["mpx"], "mpx", [seed], "poison")
    rows_pov = run_specs(po_v, run_cfg)
    rows_poc = run_specs(po_c, run_cfg)
    budget += len(po_v) + len(po_c)
    pairs_po = pairs_from(rows_poc, rows_pov)
    out["poison"] = {"flip": flip_table(pairs_po), "per_seed": {}}
    for seed in POISON_SEEDS:
        ps = [p for p in pairs_po if p[2][0] == seed]
        ftp = flip_table(ps)
        out["poison"]["per_seed"][str(seed)] = {
            "n_pairs": ftp["n"], "W": ftp["W"], "L": ftp["L"], "T": ftp["T"],
            "mean_delta": ftp["mean_delta"], "flips_neg": ftp["flips_neg"]}
    print("h1xb poison mean", out["poison"]["flip"]["mean_delta"], flush=True)

    # ---- 3. 弱锚 r40/A（各 6 fold 双席；基线=H1X 本体同局）----
    out["weak"] = {"design": "h1x_b 与 H1X 本体同 6 fold 双席 vs r40/A；"
                             "基线相对不回退", "pairs": {}}
    for on in ("r40", "A"):
        rv = run_specs(mk_specs("h1x_b", H1XB, PANEL[on], on, FOLDS_12[:6],
                                "weak"), run_cfg)
        rc = run_specs(mk_specs("h1x_ctl", H1X, PANEL[on], on, FOLDS_12[:6],
                                "weak"), run_cfg)
        budget += len(FOLDS_12[:6]) * 2 * 2
        fv, fc = fold_of(rv), fold_of(rc)
        out["weak"]["pairs"][on] = {
            "h2h_h1x_b": fv["h2h"], "h2h_h1x_ctl": fc["h2h"],
            "fold_h1x_b": fv, "fold_h1x_ctl": fc,
            "no_regression": (fv["h2h"] or 0) >= (fc["h2h"] or 0)}
        print("h1xb weak", on, fv["h2h"], "vs base", fc["h2h"], flush=True)

    # ---- 判读（重裁后口径）----
    c1a = bool((ft["mean_delta"] or 0) > 0)
    c1b = bool(ft["flips_neg"] == 0)
    c2 = bool((out["poison"]["flip"]["mean_delta"] or 0) >= 0)
    c3 = bool(all(v["no_regression"] for v in out["weak"]["pairs"].values()))
    checks = {
        "c1_paired_delta_pos": {"mean_delta": ft["mean_delta"],
                                "W": ft["W"], "L": ft["L"], "T": ft["T"],
                                "passed": c1a},
        "c1_paired_flipsneg0": {"flips_neg": ft["flips_neg"],
                                "flips_pos": ft["flips_pos"], "passed": c1b},
        "c2_poison_mean_no_regression": {
            "mean_delta": out["poison"]["flip"]["mean_delta"],
            "W": out["poison"]["flip"]["W"], "L": out["poison"]["flip"]["L"],
            "flips_neg": out["poison"]["flip"]["flips_neg"], "passed": c2},
        "c3_weak_anchor_baseline_no_regression": {
            "per": {on: {"h2h_b": v["h2h_h1x_b"], "h2h_base": v["h2h_h1x_ctl"],
                         "no_regression": v["no_regression"]}
                    for on, v in out["weak"]["pairs"].items()},
            "passed": c3}}
    full = all(c["passed"] for c in checks.values())
    out["checks"] = checks
    out["budget"] = {"used_局次": budget, "cap": 180,
                     "within_cap": budget <= 180}
    out["verdict"] = {
        "h1x_b_validation": "PASS" if full else "FAIL",
        "readjudicated_criteria_passed": full,
        "launch_candidate": ("B 档成立（s8b 机制 + h1x_b H1X 侧件）"
                             if full else "H1X 侧验证未过"),
        "note": "只测不发；在线提交=硬禁令；上线决策移交用户；证据含逐块配对表",
        "elapsed_s": round(time.perf_counter() - t0, 1)}
    # 逐局行（配对+毒种+弱锚，h1x_b 侧）
    seen, per_game = set(), []
    for r in rows_v + rows_pov:
        key = (r["seed"], r["seat"], r.get("opponent"))
        if key in seen:
            continue
        seen.add(key)
        per_game.append({"game_id": r.get("game_id"), "block": r.get("block"),
                         "seed": r["seed"], "seat": r["seat"],
                         "opp": r.get("opponent"),
                         "margin_clean": r.get("margin_clean"),
                         "tm_us": r.get("tm_us"), "tm_opp": r.get("tm_opp"),
                         "error": r.get("error")})
    out["per_game_rows"] = per_game
    out["elapsed_s"] = out["verdict"]["elapsed_s"]
    flush()
    print("H1X_B VERDICT:", json.dumps(out["verdict"], ensure_ascii=False,
                                       default=str), flush=True)
    return out


if __name__ == "__main__":
    main()
