# -*- coding: utf-8 -*-
"""judge_s9（s9 同族提胜精修 lab）：精修件 vs s8 基底同块配对判决（不发射/不提交）。

S9 = s8（a59208fe…）+ 拍面精修尾块（build_s9.py 两形态）：
  s9a=③day-high 门（平台拍 topup 挪卖撤销）；
  s9b=s9a+实存量帽+果麦单拍追加帽 8。
判决面：
  1. A/B 选臂：同 (seed,seat,opp) 配对（混块 674000+i*159×6 对手轮转×双席，
     n=24 双席=48 对/臂）s9a/s9b vs s8——flips_neg=0 优先、mean_delta 次之；
  2. 家族专组（胜者 vs {H1,oc_c3,tetsutani,V89} 各 n=16 双席）：判据逐对 h2h
     ≥0.5；
  3. H 族大败带收敛：crown H1 大败 4 局（674710/674781/674355/674141）同键
     |margin| 对照 s8（大败局 |margin| 下降）；
  4. 判据=家族专组 ≥0.5 ∧ 对 s8 配对增量>0 ∧ flips_neg=0 ∧ 大败带收敛。
预算 ≤450 局次（auth 30 + smoke 2 + A/B 140 + 家族 128 + 大败 8 = 308；法证 28
+ 补针 2 已计入）。sim_bridge 先认证；workers=2；终局钱 farms[obs.player]。
证据 fn_docs/hybrid/results/2026-09-30-s9-family-refine.json。
只写 orderbook_s9fam_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
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
          str(KSIM_DIR / "orderbook_s1form_lab"), str(KSIM_DIR / "orderbook_r40")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用（flip/lot/折叠）

EVID_DIR = HERE / "evidence"
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-s9-family-refine.json"

S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
S9A = HERE / "build" / "s9a" / "main.py"
S9B = HERE / "build" / "s9b" / "main.py"
ARMS = {"s9a": S9A, "s9b": S9B}
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
H1 = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
FAMILY = {"H1": H1, "oc_c3": PANEL["oc_c3"], "tetsutani": PANEL["tetsutani"],
          "V89": PANEL["V89"]}
BLOWOUT_KEYS = [(674710, "H1"), (674781, "H1"), (674355, "H1"),
                (674141, "H1")]
FOLDS_159 = [674000 + i * 159 for i in range(24)]
F16_159 = FOLDS_159[:16]
WORKERS = 2
BUDGET_CAP = 450

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 30, "smoke": 0, "ab": 0,
          "family": 0, "blowout": 0, "forensics_prior": 30,
          "forensics_note": "法证 28 局（forensics_s9.py）+ 价格补针 2 局"
                            "（probe_prices.py）已跑，计入总账"}
_ROW_CACHE = {}
_EXECUTED = [0]


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """判决跑口：双席 + 终局钱 farms[obs.player] + telemetry（无影子，轻量）。"""
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
        rows.append(row)
    return rows


def play(specs, cfg):
    specs = list(specs)
    n = max(1, min(WORKERS * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if WORKERS <= 1 or len(tasks) <= 1:
        parts = [_chunk_runs(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_chunk_runs, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def run_specs(specs, cfg):
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
        _EXECUTED[0] += len(todo)
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
                "game_id": "s9-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


def pairs_from(rows_c, rows_v):
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
         "margin_s8": round(a, 1), "margin_s9": round(b, 1),
         "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold_h2h(rows):
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


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    builds = {f: json.load(open(HERE / "build" / f / "build_manifest.json"))
              for f in ("s9a", "s9b")}
    forensics = json.load(open(EVID_DIR / "forensics_raw.json"))
    forensics_full = json.load(open(EVID_DIR / "forensics_full_rows.json"))
    probe = json.load(open(EVID_DIR / "probe_prices.json"))
    # 法证行→复用缓存（同 (arm_path,seed,seat,opp_path) 不重跑）
    path_of = {"s8": str(S8), "s_append": str(
        KSIM_DIR / "orderbook_s1form_lab" / "build" / "s_append" / "main.py")}
    opp_of = {"H1": str(H1), "V89": str(PANEL["V89"]),
              "tetsutani": str(PANEL["tetsutani"])}
    for fr in forensics_full:
        ap = path_of.get(fr["arm"])
        op = opp_of.get(fr["opp"])
        if ap and op and fr.get("margin_clean") is not None:
            _ROW_CACHE[(ap, int(fr["seed"]), int(fr["seat"]), op)] = {
                "seed": int(fr["seed"]), "seat": int(fr["seat"]),
                "arm": fr["arm"], "opponent": fr["opp"], "block": "forensics",
                "margin_clean": float(fr["margin_clean"]),
                "tm_us": fr.get("tm_us"), "tm_opp": fr.get("tm_opp"),
                "telemetry": fr.get("telemetry"), "error": None,
                "reused_from": "forensics_s9"}

    EV.update({
        "version": "s9-family-refine/1.0",
        "task": "S8 尖拍层同族提胜精修：法证翻负 4 局+H 族大败带 4 局→精修臂≤2"
                "→同块配对判决（不改既有代码/不提交/不发射）",
        "forensics": {},
        "fix": {},
        "ab_pairs": {}, "family_group": {}, "blowout_stats": {},
        "criteria": {}, "verdict": {},
    })
    # ---- 法证两图（压缩入证据）----
    def _trim_game(g, keep=6):
        g = dict(g)
        if isinstance(g.get("append_ticks"), list):
            g["append_ticks"] = g["append_ticks"][:keep]
        return g
    EV["forensics"] = {
        "flip_4games": {
            "design": forensics["forensics_flip"]["design"],
            "games": [_trim_game(g) for g
                      in forensics["forensics_flip"]["games"]],
            "conclusion": (
                "①非槽位：追加单落位 col 0-3（宿主当拍列表短/空），append 拍"
                "对手同拍卖单=0（race n_same_tick=0 全 9 局）；②非量：fill_rate "
                "0.875/1.0；③伤在'挪卖+扰动'：③topup 平台拍补量无毛增益（V89 "
                "局 WOOL +8 件先进、分品营收净 −6）且 2 拍后闭链竞速反转——损失"
                "落在未触碰品（CARROT −344/+93、d23-26 流向反转 −443），翻负=同"
                "拍加量扰动稳节奏对手（step1009 族）后期竞速的混沌放大，非落位"
                "可修；另 no_stock 幻影追加 10/40 单空跑（投射可卖虚高）。"),
            "probe_px": probe,
        },
        "hbig_4games": {
            "design": forensics["forensics_hbig"]["design"],
            "games": [_trim_game(g) for g
                      in forensics["forensics_hbig"]["games"]],
            "conclusion": (
                "大败钱差结构=STRAWBERRY 单品崩（分品营收差 −530~−1058，微败局 "
                "−289）+ WOOL/FERT 常态缺口（−164~−585）；崩点集中 d21-27 自残"
                " dump 拍（step 550 d22 STRAWB 3×4 连列自压价 43→30→22 vs H1 "
                "单列 3 件@43；step 601/625 d25-26 同型）——我方多列大单吃自身"
                "价格冲击，对手少列小单取高价；与微败（STRAWB −289）量级差 2-4"
                " 倍=结构性跨拍卖时序伤（d7-13 WOOL 窗恒定缺口 −312 全 H1 局在"
                "）。同拍臂（槽位/拆并/量形）对该伤无杠杆（引擎逐单位 lockstep "
                "下同拍拆并价格中性，实测验证）；跨拍挪量为 R23/R26 红线→最小"
                "对症臂不存在，如实报。"),
        },
        "rows": forensics["rows"],
    }
    EV["fix"] = {
        "arms": {f: {"sha256": builds[f]["main"]["sha256"],
                     "semantics": builds[f]["semantics"],
                     "checks": builds[f]["checks"]} for f in builds},
        "design": {
            "s9a": "③day-high 门：topup 仅当日新高拍（q>当日 running max）保留"
                   "，平台拍补量=挪卖（WOOL 199@峰 218/221@峰 227）→还原宿主"
                   "申报；②追加沿 s8（WHEAT 分品毛增益 +92~+338 为实）",
            "s9b": "s9a+实存量帽（shed+Σ单位仓+同拍买腿−原生申报，消 no_stock "
                   "幻影空跑）+果麦单拍追加帽 8 件（tetsutani 单拍 15 件大dump "
                   "类）",
            "red_line": "纯同拍后处理、零跨拍挪量；只撤销/裁剪尖拍层自身加量；"
                        "异常回退；step≥712 零触碰",
            "not_arms": "尖拍追加前置=法证判无杠杆（append 拍对手同拍竞速为 0，"
                        "槽位 col 0-3 已占先）→不做；H 族 STRAWB 跨拍时序伤无"
                        "同拍最小臂（红线下）→如实报不动手",
        },
    }
    flush_evid()

    # ---- sim_bridge 先认证（复用 s1form 认证缓存）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    auth = json.loads(auth_cache.read_text(encoding="utf-8")) \
        if auth_cache.is_file() else None
    auth_lite = {k: (auth or {}).get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version", "wall_speedup")}
    auth_lite["reused_cache"] = True
    EV["gates"] = {"build": {f: builds[f]["checks"] for f in builds},
                   "sim_auth": auth_lite}
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 冒烟 2 局 ----
    _x0 = _EXECUTED[0]
    smoke = mk_specs("s9b", S9B, PANEL["oc_c3"], "oc_c3", [FOLDS_159[0]],
                     "smoke")[:2]
    run_specs(smoke, run_cfg)
    BUDGET["smoke"] = _EXECUTED[0] - _x0
    print("smoke done", flush=True)
    flush_evid()

    # ---- A/B 选臂：混块 n=24 双席，s9a/s9b vs s8 ----
    opp_cycle = list(PANEL.keys())
    ab_specs = {"s8": [], "s9a": [], "s9b": []}
    for j, seed in enumerate(FOLDS_159):
        on = opp_cycle[j % len(opp_cycle)]
        ab_specs["s8"] += mk_specs("s8", S8, PANEL[on], on, [seed], "grid159")
        for arm, apath in ARMS.items():
            ab_specs[arm] += mk_specs(arm, apath, PANEL[on], on, [seed],
                                      "grid159")
    rows_ab = {arm: run_specs(specs, run_cfg) for arm, specs in ab_specs.items()}
    BUDGET["ab"] = _EXECUTED[0] - BUDGET["smoke"] - _x0
    print("ab done", flush=True)

    ab = {"design": "同 (seed,seat,opp) 配对 margin（control=s8，variant=s9a/"
                    "s9b）；混块=674000+i*159（i=0..23×6 对手轮转×双席）n=24 "
                    "双席=48 对/臂；s8 侧 4 对复用法证行（同键同跑口）"}
    for arm in ("s9a", "s9b"):
        ab[arm] = flip_table(pairs_from(rows_ab["s8"], rows_ab[arm]))
    ab["per_opponent"] = {
        arm: {on: flip_table([p for p in pairs_from(rows_ab["s8"],
                                                    rows_ab[arm])
                              if p[2][2] == on])
              for on in sorted(set(p[2][2] for p in pairs_from(
                  rows_ab["s8"], rows_ab[arm])))}
        for arm in ("s9a", "s9b")}
    EV["ab_pairs"] = ab
    flush_evid()

    # ---- 选臂：flips_neg=0 优先，mean_delta 次之 ----
    def pick_key(arm):
        t = ab[arm]
        return (0 if (t.get("flips_neg") or 0) == 0 else 1,
                -(t.get("mean_delta") or 0))
    winner = sorted(("s9a", "s9b"), key=pick_key)[0]
    EV["ab_pairs"]["selection"] = {
        "rule": "flips_neg=0 优先、mean_delta 大者次之",
        "winner": winner,
        "runner_up": "s9b" if winner == "s9a" else "s9a",
    }
    print("winner", winner, flush=True)
    flush_evid()

    # ---- 家族专组（胜者 vs {H1,oc_c3,tetsutani,V89} 各 n=16 双席）----
    fam = {"design": "胜者 %s vs 家族 4 对手各 n=16 双席=32 局（674000+i*159）；"
                     "h2h=(opp,seed) 双席折叠；判据逐对 ≥0.5" % winner,
           "pairs": {}}
    _x1 = _EXECUTED[0]
    fam_rows = []
    for on, opath in FAMILY.items():
        rows = run_specs(mk_specs(winner, ARMS[winner], opath, on, F16_159,
                                  "family"), run_cfg)
        fam_rows.extend(rows)
        fam["pairs"][on] = fold_h2h(rows)
        fam["pairs"][on]["margins"] = [
            {"seed": r["seed"], "seat": r["seat"],
             "margin": r.get("margin_clean")} for r in rows]
        print("family", on, fam["pairs"][on]["h2h"], flush=True)
        flush_evid()
    BUDGET["family"] = _EXECUTED[0] - _x1
    EV["family_group"] = fam
    flush_evid()

    # ---- H 族大败带收敛（crown H1 大败 4 局同键 |margin| 对照）----
    blow = {"design": "crown H1 1k-5k 大败 4 局（674710/674781/674355/674141）"
                      "×双席：胜者 vs s8 同键 |margin| 对照（大败局 |margin| "
                      "下降=收敛）",
            "rows": []}
    bl_specs = []
    for seed, on in BLOWOUT_KEYS:
        bl_specs += mk_specs(winner, ARMS[winner], H1, on, [seed], "blowout")
    bl_rows = run_specs(bl_specs, run_cfg)
    BUDGET["blowout"] = _EXECUTED[0] - _x1 - BUDGET["family"]
    s8_bl = [r for r in rows_ab["s8"] if (r["seed"], r.get("opponent")) in
             BLOWOUT_KEYS]
    s8_bl += [r for r in _ROW_CACHE.values()
              if r.get("arm") == "s8" and (r["seed"], r.get("opponent"))
              in BLOWOUT_KEYS and r.get("block") == "forensics"]
    s8_map = {(r["seed"], r["seat"]): r for r in s8_bl
              if r.get("margin_clean") is not None}
    abs8 = abs9 = 0.0
    n_conv = 0
    for r in bl_rows:
        k = (r["seed"], r["seat"])
        rs = s8_map.get(k)
        m9 = r.get("margin_clean")
        m8 = rs.get("margin_clean") if rs else None
        row = {"seed": r["seed"], "seat": r["seat"], "opp": r.get("opponent"),
               "margin_s8": m8, "margin_s9": m9,
               "abs_s8": abs(m8) if m8 is not None else None,
               "abs_s9": abs(m9) if m9 is not None else None,
               "converged": bool(m8 is not None and m9 is not None
                                 and abs(m9) < abs(m8))}
        blow["rows"].append(row)
        if m8 is not None and m9 is not None:
            abs8 += abs(m8)
            abs9 += abs(m9)
            n_conv += 1
    blow["abs_margin_mean"] = {
        "s8": round(abs8 / max(1, n_conv), 1),
        "s9": round(abs9 / max(1, n_conv), 1),
        "n_pairs": n_conv}
    blow["converged_pairs"] = sum(1 for r in blow["rows"] if r["converged"])
    blow["convergence_ok"] = bool(n_conv and abs9 < abs8)
    EV["blowout_stats"] = blow
    flush_evid()

    # ---- 判据 + verdict ----
    fam_h2h = {on: (fam["pairs"].get(on) or {}).get("h2h") for on in FAMILY}
    c1 = bool(all((h or 0) >= 0.5 for h in fam_h2h.values())
              and len(fam_h2h) == 4)
    wtab = ab[winner]
    delta = wtab.get("mean_delta")
    c2 = bool((delta or 0) > 0)
    c3 = bool((wtab.get("flips_neg") or 0) == 0)
    c4 = bool(blow["convergence_ok"])
    full = bool(c1 and c2 and c3 and c4)
    fails = [name for name, ok in (("family_ge_0.5", c1), ("paired_delta_gt0", c2),
                                   ("flips_neg_zero", c3),
                                   ("blowout_convergence", c4)) if not ok]
    EV["criteria"] = {
        "rule": "判据=家族专组逐对 ≥0.5 ∧ 对 s8 配对增量>0 ∧ flips_neg=0 ∧ H 族"
                "大败带收敛（大败局 |margin| 下降）",
        "c1_family_all_ge_0.5": {"h2h": fam_h2h, "passed": c1},
        "c2_paired_delta_gt0": {"mean_delta_s9_minus_s8": delta,
                                "flips_pos": wtab.get("flips_pos"),
                                "flips_neg": wtab.get("flips_neg"),
                                "passed": c2},
        "c3_flips_neg_zero": {"flips_neg": wtab.get("flips_neg"), "passed": c3},
        "c4_blowout_convergence": {
            "abs_margin_mean": blow["abs_margin_mean"],
            "converged_pairs": blow["converged_pairs"],
            "passed": c4},
    }
    EV["verdict"] = {
        "winner": winner, "winner_sha256": builds[winner]["main"]["sha256"],
        "family_h2h": fam_h2h,
        "ab_paired": {"mean_delta": delta, "flips_pos": wtab.get("flips_pos"),
                      "flips_neg": wtab.get("flips_neg"),
                      "W": wtab.get("W"), "L": wtab.get("L"),
                      "T": wtab.get("T")},
        "blowout_abs_mean": blow["abs_margin_mean"],
        "criteria_passed": full,
        "verdict": ("S9_FAMILY_REFINE_FULL_PASS" if full else
                    "S9_FAMILY_REFINE_PARTIAL_FAIL[" + "+".join(fails) + "]"),
        "summary": "S9[%s=%s]：家族专组 %s；对 s8 配对增量 %s（flips +%s/-%s）；"
                   "大败带 |margin| 均值 %s→%s（收敛 %s/%s 对）；criterion %s" % (
                       winner, builds[winner]["main"]["sha256"][:8],
                       json.dumps(fam_h2h, default=str), delta,
                       wtab.get("flips_pos"), wtab.get("flips_neg"),
                       blow["abs_margin_mean"]["s8"],
                       blow["abs_margin_mean"]["s9"],
                       blow["converged_pairs"], blow["abs_margin_mean"][
                           "n_pairs"], full),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    BUDGET["total_局次"] = sum(BUDGET[k] for k in
                              ("auth", "smoke", "ab", "family", "blowout",
                               "forensics_prior"))
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP

    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货，"
        "margin/终局钱只作参考；翻负闭链混沌放大如实登记（法证①：损失落未触"
        "碰品 CARROT/流向，非落位可修）")
    ANOMALIES.append(
        "③day-high 门=撤销类干预（还原宿主申报量，同拍零跨拍）；②追加沿 s8"
        "（s9b 另裁量）；守恒口径不变（加卖非挪卖仍合法，本层只少加不挪）")
    ANOMALIES.append(
        "H 族大败带=STRAWB d21-27 跨拍卖时序伤（引擎 lockstep 同拍拆并价格中性"
        "已实证）；跨拍挪量 R23/R26 红线→同拍最小臂不存在，大败带收敛判据如实"
        "量测，不修饰")
    ANOMALIES.append(
        "断点续跑披露：法证 28 局+价格补针 2 局先前已跑（计账 30）；sim_bridge "
        "认证复用 s1form 缓存（consistency_ok）按 30 计账；s8 侧 4 对 A/B 复用"
        "法证行（同 (arm_path,seed,seat,opp_path) 去重）")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；家族专组以逐对 h2h 口径判")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s9_ledger.json").write_text(json.dumps(
        {"budget": BUDGET, "criteria": EV["criteria"],
         "ab": {a: {k: ab[a].get(k) for k in
                    ("n", "mean_delta", "flips_pos", "flips_neg", "W", "L",
                     "T")} for a in ("s9a", "s9b")},
         "selection": EV["ab_pairs"]["selection"],
         "family_h2h": fam_h2h, "blowout": blow["abs_margin_mean"]},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:800], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
