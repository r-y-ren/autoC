# -*- coding: utf-8 -*-
"""judge_s8（s8 尖拍捕获+申报修复 lab）：S8 vs s_append 同块配对判决（不发射/不提交）。

S8 = s_append 构建件 + 尖拍层（build_s8.py）：
  ①尖拍判定（WOOL≥144/MILK≥124 绝对线；果麦 WHEAT/MELON d22 窗≥当日 0.75 分位）
  ②尖拍补卖（无原生卖单→lot2-4 追加至可卖上限）③同拍申报修复（有原生卖单→
  补至可卖上限）④anti-幻影（申报+追加≤投射可卖）⑤加卖守恒（可超原计划）。
判决面（教训：同块配对！）：
  1. 同块配对 A/B：S8 vs s_append（同 (seed,seat,opp)）——增量以配对面读；
     块=混块：674000+i*159（i=0..23，对手 6 名面板轮转）+ 26 败局（D8 法证
     语料 (opp,seed)×双席）；块间差异明示；
  2. 新标准面板（S8 vs {oc_c3 n=24, mpx/tetsutani/V89/r40/A n=16}，双席）：
     判据=对冠军 ≥0.5（≥0.7 碾压目标）∧ 强面板 ≥0.5 ∧ 弱锚 ≥0.8 ∧ flips_neg=0；
  3. 毒种专项：五毒种（674000/674141/674705/674987/675410）各 4 局
     （{mpx,oc_c3}×双席）配对翻正数（核心 KPI）；
  4. 毒种分层：判决按 seed 分层，五毒种单列。
预算 ≤500 局次（auth 30 + smoke 4 + A/B 200 + 毒种 24 + 面板 208 = 466）。
证据 fn_docs/hybrid/results/2026-09-30-s8-spike.json。sim_bridge 先认证；
workers=2；终局钱 farms[obs.player]。只写 orderbook_s8spike_lab/ 与证据路径。
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
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab"),
          str(KSIM_DIR / "orderbook_s1form_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用（shadow/lot/flip/折叠）
import judge_goose as jg   # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-s8-spike.json"

S8 = HERE / "build" / "s8" / "main.py"
APPEND = KSIM_DIR / "orderbook_s1form_lab" / "build" / "s_append" / "main.py"
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
# D8 法证 26 败局语料：(opp, seed, tag, d8_c_final_margin)
FORENSIC_26 = [
    ("mpx", 674000, "L", -461), ("mpx", 674705, "L", -142),
    ("mpx", 674423, "W", 508), ("drop_half", 674000, "L", -555),
    ("drop_half", 675410, "L", -394), ("drop_half", 674423, "W", 416),
    ("H1", 674710, "L-big", -1268), ("H1", 674141, "L", -1073),
    ("H1", 674213, "W", 139), ("H", 674000, "L", -446),
    ("H", 674705, "L", -260), ("H", 674423, "W", 75),
    ("r40", 674141, "W-worldpoison-ctrl", 671),
    ("mpx", 674141, "L", -987), ("mpx", 675410, "L", -545),
    ("mpx", 674846, "W", 385), ("drop_half", 674141, "L", -1060),
    ("drop_half", 675551, "L", -35), ("drop_half", 674846, "W", 419),
    ("H1", 674781, "L-big", -1307), ("H1", 675410, "L", -639),
    ("H1", 675065, "W", 61), ("H", 674141, "L", -1073),
    ("H", 675410, "L", -639), ("H", 674846, "W", 58),
    ("r40", 675410, "L-worldpoison", -87),
]
FORENSIC_ARMS = {
    "mpx": PANEL["mpx"],
    "drop_half": KSIM_DIR / "orderbook_unified_u2_lab" / "build"
    / "u2v2_drop_half" / "main.py",
    "H1": KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py",
    "H": Path("/tmp/arms_b/haodou_v82/main.py"),
    "r40": PANEL["r40"],
}
POISON_SEEDS = [674000, 674141, 674705, 674987, 675410]
POISON_OPPS = ("mpx", "oc_c3")
FOLDS_159 = [674000 + i * 159 for i in range(24)]
F16_159 = FOLDS_159[:16]
WORKERS = 2
BUDGET_CAP = 500

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 0, "smoke": 0, "ab": 0,
          "poison": 0, "panel": 0}
_ROW_CACHE = {}          # (arm_path, seed, seat, opp_path) -> row（去重省预算）


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱（farms[obs.player]）+ 影子归因 + 卖面统计。"""
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
               else None,
               "shadow": None, "end": None, "end_opp": None, "lot": None}
        if row["banks"] is not None and row["error"] is None:
            try:
                e_us = jsf.end_reads(sinks[row["seat"]])
                e_opp = jsf.end_reads(sinks[1 - row["seat"]])
                row["end"] = e_us
                row["end_opp"] = e_opp
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
    """去重跑口：同 (arm_path,seed,seat,opp_path) 只跑一次，行进缓存。"""
    out = []
    todo = []
    for spec in specs:
        key = (spec["arm_path"], int(spec["seed"]), int(spec["our_seat"]),
               spec["opp_path"])
        if key in _ROW_CACHE:
            out.append(_ROW_CACHE[key])
        else:
            todo.append((key, spec))
    if todo:
        rows = play([s for _, s in todo], cfg)
        # 行序=分块拼接序（非 spec 序）→按 (seed,seat,opponent) 回配（调用内唯一）
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
                "game_id": "s8-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


# ============================================================ 读数 ==
def pairs_from(rows_c, rows_v, seat_key="seat"):
    """同 (seed,seat,opponent) 配对 margin 面（control=s_append, variant=S8）。"""
    key = lambda r: (r["seed"], r[seat_key], r.get("opponent"))  # noqa: E731
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
         "margin_s_append": round(a, 1), "margin_s8": round(b, 1),
         "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold_h2h(rows):
    """(opponent, seed) 双席折叠 W/L/T + h2h（fail-closed）。"""
    groups = {}
    for r in rows:
        groups.setdefault((r.get("opponent"), r["seed"]), []).append(r)
    w = l = t = 0
    margins = []
    for k in sorted(groups, key=str):
        rs = groups[k]
        ms = [float(r["margin_clean"]) for r in rs
              if r.get("margin_clean") is not None]
        if len(rs) != 2 or len(ms) != 2:
            l += 1
            margins.extend(ms)
            continue
        score = sum(1.0 if m > 0 else 0.5 if m == 0 else 0.0 for m in ms) / 2.0
        margins.append(sum(ms) / 2.0)
        if score >= 1.0:
            w += 1
        elif score <= 0.0:
            l += 1
        else:
            t += 1
    n = len(groups)
    return {"n": n, "wins": w, "losses": l, "ties": t,
            "h2h": round((w + 0.5 * t) / n, 4) if n else None,
            "mean_margin": round(sum(margins) / len(margins), 1)
            if margins else None}


def s8_telemetry(rows):
    tot = {}
    for r in rows:
        t = r.get("telemetry") or {}
        for k, v in t.items():
            if isinstance(v, (int, float)):
                tot[k] = tot.get(k, 0) + v
    return tot


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    build = json.load(open(HERE / "build" / "s8" / "build_manifest.json"))
    EV.update({
        "version": "s8-spike/1.0",
        "task": "s_append 形态上加尖拍捕获+申报修复层（S8），同块配对 A/B 冲 "
                "h2h 0.70+（不改既有代码/不提交/不发射）",
        "design": {
            "formula": "S8 = s_append(4608e9e0…)+尖拍尾块（a59208fe…）",
            "artifact": {"base": build["base"], "main": build["main"],
                         "entry": build["entry"], "host": build["host_entry"]},
            "layer": build["semantics"],
            "spike_params": {
                "abs_lines": {"WOOL": 144, "MILK": 124},
                "fruit_grain": {"items": ["WHEAT", "MELON"],
                                "window_steps": [528, 552],
                                "rule": "quote≥当日 0.75 分位（ceil 秩、样本≥6、"
                                        "含当拍）"},
                "note": "参数判决标定：绝对线沿 D8 尖价带下缘；果麦组取 WHEAT+"
                        "MELON（d22 果麦窗），分位为当日已见 quote 序列"},
            "corpus": {
                "ab_block": "混块=674000+i*159(i=0..23)×面板 6 名轮转×双席"
                            " + 26 败局(D8 法证 (opp,seed)×双席)",
                "panel": "S8 vs {oc_c3 n=24, mpx/tetsutani/V89/r40/A n=16} "
                         "双席（674000+i*159）",
                "poison": "五毒种各 4 局（{mpx,oc_c3}×双席）配对"},
            "workers": WORKERS,
            "caliber": {
                "margin": "终局钱 farms[obs.player] 差（干净口径）",
                "h2h": "(opp,seed) 双席折叠 W/L/T（fail-closed）",
                "flips": "同 (seed,seat,opp) 配对 margin：s_append 胜而 S8 负"
                         "记 flips_neg；负转正记 flips_pos（毒种翻正=核心 KPI）",
                "paired": "增量只读配对面（同块同 (seed,seat,opp)）——s3 教训",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考"},
        },
        "gates": {"build": build["checks"],
                  "s8_sha256": build["main"]["sha256"]},
        "ab_pairs": {}, "panel": {}, "poison_seeds": {}, "seed_strata": {},
        "criteria": {}, "verdict": {},
    })
    flush_evid()

    # ---- sim_bridge 先认证（复用 s1form 认证缓存，无缓存则现跑 30）----
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
        auth_corpus = jg.LOSS_SEEDS_26[:16] + FOLDS_159[:8] + \
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
            (EVID_DIR / "sim_auth_cache.json").write_text(
                json.dumps(auth, ensure_ascii=False, default=str) + "\n",
                encoding="utf-8")
    EV["gates"]["sim_auth"] = auth_lite
    BUDGET["auth"] = 30
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 冒烟 2 局（harness 噪声披露）----
    smoke = mk_specs("s8", S8, PANEL["oc_c3"], "oc_c3", [FOLDS_159[0]],
                     "smoke")[:2]
    run_specs(smoke, run_cfg)
    BUDGET["smoke"] = 2
    print("smoke done", flush=True)
    flush_evid()

    # ---- 同块配对 A/B（混块）----
    ab_specs_c, ab_specs_v = [], []
    # 子块 A：674000+i*159×6 面板对手轮转
    opp_cycle = list(PANEL.keys())
    for j, seed in enumerate(FOLDS_159):
        on = opp_cycle[j % len(opp_cycle)]
        ab_specs_c += mk_specs("s_append", APPEND, PANEL[on], on, [seed],
                               "grid159")
        ab_specs_v += mk_specs("s8", S8, PANEL[on], on, [seed], "grid159")
    # 子块 B：26 败局（D8 法证 (opp,seed)×双席）
    for on, seed, tag, ref in FORENSIC_26:
        ap = FORENSIC_ARMS[on]
        if not ap.is_file():
            ANOMALIES.append("forensics opp %s 文件缺失(%s)：跳过" % (on, ap))
            continue
        sc = mk_specs("s_append", APPEND, ap, on, [seed], "loss26")
        sv = mk_specs("s8", S8, ap, on, [seed], "loss26")
        for s in sc + sv:
            s["tag"] = tag
        ab_specs_c += sc
        ab_specs_v += sv
    rows_c = run_specs(ab_specs_c, run_cfg)
    rows_v = run_specs(ab_specs_v, run_cfg)
    BUDGET["ab"] = sum(1 for r in rows_c if r.get("block") in
                       ("grid159", "loss26")) + sum(
        1 for r in rows_v if r.get("block") in ("grid159", "loss26"))
    print("ab paired done", len(rows_c), len(rows_v), flush=True)

    pairs_all = pairs_from(rows_c, rows_v)
    pairs_grid = [p for p in pairs_all if _block_of(rows_c, rows_v, p) ==
                  "grid159"]
    pairs_loss = [p for p in pairs_all if _block_of(rows_c, rows_v, p) ==
                  "loss26"]
    ab = {
        "design": "同 (seed,seat,opp) 配对 margin（control=s_append, "
                  "variant=S8）；混块=674000+i*159(24 种子×6 对手轮转×双席)"
                  "+26 败局(D8 法证)×双席",
        "paired_all": flip_table(pairs_all),
        "paired_grid159": flip_table(pairs_grid),
        "paired_loss26": flip_table(pairs_loss),
        "fold_h2h": {
            "s_append": fold_h2h([r for r in rows_c if r.get("block")]),
            "s8": fold_h2h([r for r in rows_v if r.get("block")])},
        "per_opponent_paired": {
            on: flip_table([p for p in pairs_all if p[2][2] == on])
            for on in sorted(set(p[2][2] for p in pairs_all))},
        "block_delta_note": "块间差异明示：grid159=新块（参数外推），"
                            "loss26=D8 败局复打（漏拍值回收主靶）",
    }
    EV["ab_pairs"] = ab
    flush_evid()

    # ---- 毒种专项（配对翻正数=核心 KPI）----
    po_c, po_v = [], []
    for seed in POISON_SEEDS:
        for on in POISON_OPPS:
            po_c += mk_specs("s_append", APPEND, PANEL[on], on, [seed],
                             "poison")
            po_v += mk_specs("s8", S8, PANEL[on], on, [seed], "poison")
    rows_poc = run_specs(po_c, run_cfg)
    rows_pov = run_specs(po_v, run_cfg)
    BUDGET["poison"] = sum(1 for r in rows_poc if r.get("block") == "poison") \
        + sum(1 for r in rows_pov if r.get("block") == "poison")
    pairs_po = pairs_from(rows_poc, rows_pov)
    po = {"design": "五毒种各 4 局（{mpx,oc_c3}×双席）同 (seed,seat,opp) 配对；"
                    "翻正=flips_pos（s_append 负→S8 正）",
          "flips_total": flip_table(pairs_po), "per_seed": {}}
    for seed in POISON_SEEDS:
        ps = [p for p in pairs_po if p[2][0] == seed]
        ft = flip_table(ps)
        po["per_seed"][str(seed)] = {
            "n_pairs": ft["n"], "flips_pos_翻正": ft["flips_pos"],
            "flips_neg_翻负": ft["flips_neg"],
            "mean_delta": ft["mean_delta"],
            "margins": [{"opp": p[2][2], "seat": p[2][1],
                         "s_append": round(p[0], 1), "s8": round(p[1], 1)}
                        for p in ps]}
    EV["poison_seeds"] = po
    print("poison done", flush=True)
    flush_evid()

    # ---- 新标准面板（S8）----
    panel = {"design": "S8 vs 6 对手（674000+i*159）：oc_c3 n=24 双席=48 局，"
                       "余对 n=16 双席=32 局；h2h=(opp,seed) 双席折叠",
             "pairs": {}}
    panel_rows = []
    for on, opath in PANEL.items():
        folds = FOLDS_159 if on == "oc_c3" else F16_159
        rows = run_specs(mk_specs("s8", S8, opath, on, folds, "panel"),
                         run_cfg)
        panel_rows.extend(rows)
        panel["pairs"][on] = fold_h2h(rows)
        print("panel", on, panel["pairs"][on]["h2h"], flush=True)
        flush_evid()
    BUDGET["panel"] = sum(1 for r in panel_rows if r.get("block") == "panel")
    fe = jsf.full_exec_agg(panel_rows)
    lot = jsf.lot_agg(panel_rows)
    panel["full_exec"] = {k: fe[k] for k in
                          ("n_sell_orders", "full", "partial", "full_exec",
                           "requested_qty", "filled_qty", "gap_qty")}
    panel["lot"] = {"n_sell_orders": lot["n_sell_orders"],
                    "qty_sum": lot["qty_sum"], "mean_lot": lot["mean_lot"],
                    "d29_orders_per_game": lot.get("d29_orders_per_game")}
    EV["panel"] = panel

    # ---- 毒种分层（判决按 seed 分层，五毒种单列）----
    strata = {"caliber": "同块配对 delta=S8−s_append（配对面均值）+fold 结果；"
                         "五毒种单列", "rows": {}}
    for seed in sorted(set(r["seed"] for r in rows_c + rows_v
                           if r.get("block"))):
        ps = [p for p in pairs_all if p[2][0] == seed]
        if not ps:
            continue
        ft = flip_table(ps)
        strata["rows"][str(seed)] = {
            "poison": seed in POISON_SEEDS,
            "n_pairs": ft["n"], "flips_pos": ft["flips_pos"],
            "flips_neg": ft["flips_neg"], "mean_delta": ft["mean_delta"],
            "win_s_append": ft["win_control"], "win_s8": ft["win_variant"]}
    EV["seed_strata"] = strata

    # ---- telemetry（尖拍层触发面）----
    EV["s8_layer_telemetry"] = {
        "ab_s8": s8_telemetry(rows_v), "panel_s8": s8_telemetry(panel_rows),
        "poison_s8": s8_telemetry(rows_pov),
        "note": "spike_item_ticks=尖拍触发品·拍数；append/topup=②③ 收回量；"
                "skip_full_decl=本轮已满申报跳过；errors=异常回退"},
    # 加卖面（filled_by_item 差）
    inv_c = jsf.full_exec_agg(rows_c).get("filled_by_item") or {}
    inv_v = jsf.full_exec_agg(rows_v).get("filled_by_item") or {}
    EV["additive_sell"] = {
        "caliber": "影子引擎分品累计成交（filled）配对面合计；S8 加卖非挪卖"
                   "（可超原计划，A 件日新高先例合法）",
        "s_append": inv_c, "s8": inv_v,
        "delta_s8_minus_s_append": {
            it: round(float(inv_v.get(it, 0)) - float(inv_c.get(it, 0)), 1)
            for it in sorted(set(inv_c) | set(inv_v))},
    }

    # ---- 判据 + verdict ----
    h_oc = (panel["pairs"].get("oc_c3") or {}).get("h2h")
    strong = {o: (panel["pairs"].get(o) or {}).get("h2h")
              for o in PANEL_STRONG}
    weak = {o: (panel["pairs"].get(o) or {}).get("h2h") for o in PANEL_WEAK}
    flips_neg = ab["paired_all"].get("flips_neg", 0)
    c1 = bool(h_oc is not None and h_oc >= 0.5)
    c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
              and len(strong) == 3)
    c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
    c4 = bool(flips_neg == 0)
    grade = ("碾压" if (h_oc or 0) >= 0.7 else
             "强" if (h_oc or 0) >= 0.5 else "未过锚")
    full = bool(c1 and c2 and c3 and c4)
    poison_flip = po["flips_total"].get("flips_pos", 0)
    EV["criteria"] = {
        "rule": "①对冠军 oc_c3 ≥0.5（≥0.7 碾压目标）②强面板 {mpx,tetsutani,"
                "V89} 逐对 ≥0.5 ③弱锚 {r40,A} 逐对 ≥0.8 ④flips_neg=0（同块"
                "配对面）",
        "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1,
                               "target_crush_ge_0.7": bool((h_oc or 0) >= 0.7)},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
        "c4_flips_neg_zero": {"flips_neg": flips_neg,
                              "flips_pos_all": ab["paired_all"].get(
                                  "flips_pos"),
                              "passed": c4},
        "poison_flip_kpi": {"翻正数": poison_flip,
                            "翻负数": po["flips_total"].get("flips_neg"),
                            "per_seed": {k: v["flips_pos_翻正"] for k, v in
                                         po["per_seed"].items()}},
    }
    EV["verdict"] = {
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "ab_paired": {"mean_delta_all": ab["paired_all"].get("mean_delta"),
                      "flips_pos": ab["paired_all"].get("flips_pos"),
                      "flips_neg": flips_neg,
                      "grid159_mean_delta":
                          ab["paired_grid159"].get("mean_delta"),
                      "loss26_mean_delta":
                          ab["paired_loss26"].get("mean_delta"),
                      "loss26_h2h_s8": ab["fold_h2h"]["s8"],
                      "loss26_h2h_s_append": ab["fold_h2h"]["s_append"]},
        "poison_flips_pos": poison_flip,
        "criteria_passed": full,
        "verdict": ("S8_SPIKE_FULL_PASS" if full else
                    "S8_SPIKE_ANCHOR_STRONG_BUT_PANEL_BLEED" if c1 else
                    "S8_SPIKE_NO_POSITIVE_ARM"),
        "summary": "S8[%s]：对冠军锚 oc_c3 h2h %s（%s）；强面板 %s；弱锚 %s；"
                   "配对增量 mean_delta %s（flips +%s/-%s）；毒种翻正 %s/20；"
                   "criterion %s" % (
                       build["main"]["sha256"][:8], h_oc, grade,
                       json.dumps(strong, default=str),
                       json.dumps(weak, default=str),
                       ab["paired_all"].get("mean_delta"),
                       ab["paired_all"].get("flips_pos"), flips_neg,
                       poison_flip, full),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    BUDGET["total_局次"] = sum(BUDGET[k] for k in
                              ("auth", "smoke", "ab", "poison", "panel"))
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP

    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货，"
        "margin/终局钱只作参考；影子引擎 mismatch 计步留档不修")
    ANOMALIES.append(
        "尖拍参数判决标定：绝对线 WOOL≥144/MILK≥124（D8 尖价带下缘）；果麦组="
        "WHEAT+MELON、d22 窗 [528,552)、当日 0.75 分位（ceil 秩、样本≥6）——"
        "如触发面异常在后续轮次重标")
    ANOMALIES.append(
        "③申报修复=原单加量至可卖上限（只补申报不改时点，D8'全量申报'口径）"
        "——单量形态受冲击如实登记；②追加单为 lot 2-4 形态")
    ANOMALIES.append(
        "anti-幻影硬约束：申报+追加总量≤投射可卖（_xd7_projected 同序口径）；"
        "D8 败局幻影申报 +34~43 件为反例，S8 不学")
    ANOMALIES.append(
        "守恒口径变化：S8=加卖非挪卖（同品累计成交可超原计划，A 件日新高先例"
        "合法）；非触发拍零足迹（同对象返回）；异常回退；step≥712 零触碰")
    ANOMALIES.append(
        "块间差异：grid159=新块参数外推，loss26=D8 法证语料复打（H 臂="
        "/tmp/arms_b/haodou_v82 只读引用，缺失则回退登记）；同块配对读增量"
        "（s3 教训），跨块不比")
    ANOMALIES.append(
        "毒种分层：判决按 seed 分层，五毒种（674000/674141/674705/674987/"
        "675410）单列；毒种翻正数为核心 KPI")
    ANOMALIES.append(
        "断点续跑披露：冒烟 2 局计入预算；sim_bridge 认证复用 s1form 缓存"
        "（consistency_ok）按 30 计账")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；新标准以逐对口径判")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s8_ledger.json").write_text(json.dumps(
        {"budget": BUDGET, "criteria": EV["criteria"],
         "ab_paired": {k: {kk: ab[k].get(kk) for kk in
                           ("n", "mean_delta", "flips_pos", "flips_neg",
                            "W", "L", "T")}
                       for k in ("paired_all", "paired_grid159",
                                 "paired_loss26")},
         "panel_h2h": {k: v.get("h2h") for k, v in panel["pairs"].items()},
         "poison": po["per_seed"]},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


def _block_of(rows_c, rows_v, pair):
    _, _, k = pair
    for r in rows_c + rows_v:
        if (r["seed"], r.get("seat"), r.get("opponent")) == k:
            return r.get("block")
    return None


if __name__ == "__main__":
    main()
