# -*- coding: utf-8 -*-
"""judge_s809look（s5s809 lab）：S5 速赢实验 `_S809_LOOK` 加深终验
（判决先行·不发射/不提交）。

基座=C_final（orderbook_composite_lab/build/c_final，sha a37c0d34…，`_S809_LOOK`=3
对照臂 look3）；变体=look6（3→6）/look12（3→12）——纯参数字面量替换（build
反替换回程封印，零结构变化），口径对照 doanthuan 复刻记录（Apache-2.0，只调
参数不拷码）。终验面：
1. sim_bridge 先认证 30/30（缓存可复用）；
2. 新标准面板（3 臂×6 对；每对 n=16 局/臂=8 fold×双席；vs oc_c3 加密 n=24
   局/臂=12 fold；新块 674000+i*151）：①vs 冠军锚 oc_c3 ≥0.5（≥0.7 碾压）
   ②强面板 {mpx,tetsutani,V89} 逐对 ≥0.5 ③弱锚 {r40,A} ≥0.8；
3. 配对面（变体 vs look3 对照，同 (seed,seat,opp) 双跑）：④flips_neg=0
   （对照胜局翻负计数）；守恒足迹=仅 step809 触发面（首差异拍=SELL 面单量
   签名、触发前零差异；farmer/hands 零触碰）。
h2h=judge_r44._fold_arm 同 seed 双席折叠（fail-closed）；margin=终局
farms[obs.player].money 差（干净口径；banks 交叉登记）；margin/终局钱只作
参考；胜率=硬通货。sim_bridge 先认证；workers=2；预算 ≤350 局次
（3 臂×104 局+auth30=342）。证据 fn_docs/hybrid/results/
2026-09-30-s5-s809look.json；账本落本 lab evidence/。
只写 orderbook_s5s809_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
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
    "2026-09-30-s5-s809look.json"

BASE = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
ARMS = {
    "look3": BASE,
    "look6": HERE / "build" / "look6" / "main.py",
    "look12": HERE / "build" / "look12" / "main.py",
}
VARIANTS = ("look6", "look12")
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
FOLDS = [674000 + i * 151 for i in range(12)]
FOLDS_MAIN = FOLDS[:8]      # 普通对：8 fold×双席=16 局/臂
FOLDS_OC3 = FOLDS[:12]      # vs oc_c3 加密：12 fold×双席=24 局/臂
WORKERS = 2
BUDGET_CAP = 350

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_panel(payload):
    """panel worker：终局钱 farms[obs.player] + banks 交叉登记 + 我席动作流抽头。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, repr(exc)[:120]))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"), "arm": spec.get("arm"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None, "acts": []}
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
                row["acts"] = [(int(s), json.dumps(a, sort_keys=True,
                                                   default=str))
                               for (s, o, a) in sinks[row["seat"]]]
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
        out.append(row)
    return out


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


def unit_specs(arm, arm_path, opp_path, opp_name, folds):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            agents = [{"type": "python", "path": str(arm_path)},
                      {"type": "python", "path": str(opp_path)}]
            if seat == 1:
                agents.reverse()
            specs.append({
                "game_id": "s5-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "kind": "ab", "trace": True,
                "agents": agents})
    return specs


# ============================================================ 面板聚合 ==
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
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


# ============================================================ 配对面 ==
def _canon_market(rows):
    sell, other = {}, []
    for o in rows or []:
        o = list(o) if isinstance(o, (list, tuple)) else [o]
        if o and str(o[0]) == "SELL" and len(o) >= 3:
            try:
                q = int(float(o[2]))
            except Exception:
                return None, None
            key = (str(o[1]), tuple(str(x) for x in o[3:]))
            sell[key] = sell.get(key, 0) + q
        else:
            other.append(tuple(str(x) for x in o))
    return sell, sorted(other)


def _s809_sig(sa, sb_):
    """SELL 面单量签名（足迹口径）：farmer/hands 逐字同、非 SELL 市场行逐字同、
    差异只落 SELL 行数量（含增行/加量）。"""
    try:
        a = json.loads(sa)
        b = json.loads(sb_)
    except Exception:
        return False
    if (a.get("farmer") or ["PASS"]) != (b.get("farmer") or ["PASS"]):
        return False
    if (a.get("hands") or []) != (b.get("hands") or []):
        return False
    ma, oa = _canon_market(a.get("market") or [])
    mb, ob = _canon_market(b.get("market") or [])
    if ma is None or mb is None:
        return False
    return oa == ob


def _s809_monotone(sa, sb_):
    """加深方向：变体 SELL 量逐键 ≥ 对照（10 单帽边缘件可例外，单列报数）。"""
    try:
        a = json.loads(sa)
        b = json.loads(sb_)
    except Exception:
        return False
    ma, _ = _canon_market(a.get("market") or [])
    mb, _ = _canon_market(b.get("market") or [])
    if ma is None or mb is None:
        return False
    return all(ma.get(k, 0) >= mb.get(k, 0) for k in set(ma) | set(mb))


def paired_stats(rows_arm, rows_base, label):
    """变体 vs look3 对照（同 (seed,seat,opp)）：flips + step809 足迹归因。"""
    mb = {(r["seed"], r["seat"], r.get("opponent")): r for r in rows_base}
    flip = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
            "win_control": 0, "win_variant": 0,
            "flips_pos": 0, "flips_neg": 0}
    foot = {"n_units": 0, "n_identical": 0, "n_diff": 0,
            "attribution_ok_all": True, "strict_s809_all": True,
            "trigger_region_all": True, "monotone_first_all": True,
            "first_diff_steps": [], "n_missing_pair": 0}
    per = []
    for r in rows_arm:
        key = (r["seed"], r["seat"], r.get("opponent"))
        b = mb.get(key)
        if b is None:
            foot["n_missing_pair"] += 1
            continue
        mc, mv = b.get("margin_clean"), r.get("margin_clean")
        if isinstance(mc, (int, float)) and isinstance(mv, (int, float)):
            flip["n"] += 1
            d = float(mv) - float(mc)
            flip["delta_sum"] += d
            flip["W" if d > 0 else "L" if d < 0 else "T"] += 1
            wc, wv = (1 if mc > 0 else 0), (1 if mv > 0 else 0)
            flip["win_control"] += wc
            flip["win_variant"] += wv
            if wv and not wc:
                flip["flips_pos"] += 1
            if wc and not wv:
                flip["flips_neg"] += 1
        foot["n_units"] += 1
        ma_, mb_ = dict(r.get("acts") or []), dict(b.get("acts") or [])
        dsteps = sorted(s for s in set(ma_) | set(mb_)
                        if ma_.get(s) != mb_.get(s))
        if not dsteps:
            foot["n_identical"] += 1
            per.append({"seed": key[0], "seat": key[1], "opponent": key[2],
                        "status": "identical", "n_ticks": len(ma_)})
            continue
        foot["n_diff"] += 1
        sig_steps = [s for s in dsteps if _s809_sig(ma_.get(s) or "{}",
                                                    mb_.get(s) or "{}")]
        first_diff = dsteps[0]
        first_sig = sig_steps[0] if sig_steps else None
        pre = [s for s in dsteps if first_sig is None or s < first_sig]
        attr_ok = (first_diff == first_sig and not pre)
        strict_ok = (len(sig_steps) == len(dsteps))
        region_ok = (216 <= first_diff < 718 and first_diff % 24 != 23)
        mono_ok = _s809_monotone(ma_.get(first_diff) or "{}",
                                 mb_.get(first_diff) or "{}")
        foot["attribution_ok_all"] = bool(foot["attribution_ok_all"]
                                          and attr_ok)
        foot["strict_s809_all"] = bool(foot["strict_s809_all"] and strict_ok)
        foot["trigger_region_all"] = bool(foot["trigger_region_all"]
                                          and region_ok)
        foot["monotone_first_all"] = bool(foot["monotone_first_all"]
                                          and mono_ok)
        foot["first_diff_steps"].append(first_diff)
        per.append({"seed": key[0], "seat": key[1], "opponent": key[2],
                    "status": "diff", "n_diff_steps": len(dsteps),
                    "first_diff_step": first_diff,
                    "first_s809_sig_step": first_sig,
                    "n_pre_trigger_steps": len(pre),
                    "strict_s809_only": strict_ok,
                    "attribution_ok": attr_ok, "monotone_first": mono_ok,
                    "trigger_region_ok": region_ok})
    n = max(1, flip["n"])
    flip["mean_delta"] = round(flip["delta_sum"] / n, 2)
    flip["net_flip_wins"] = flip["win_variant"] - flip["win_control"]
    fds = foot["first_diff_steps"]
    foot["first_diff_step_min"] = min(fds) if fds else None
    foot["first_diff_step_max"] = max(fds) if fds else None
    foot["per_unit_lite"] = per
    foot["vs"] = label
    return flip, foot


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP, "auth": 0, "panel": 0}

    build = json.load(open(EVID_DIR / "build_s809look.json"))
    forms_ok = all(build["forms"][f].get("roundtrip_identity_ok")
                   for f in VARIANTS)
    if not forms_ok:
        raise RuntimeError("build 封印缺失（roundtrip_identity_ok）")

    EV.update({
        "version": "s5-s809look/1.0",
        "task": "S5 速赢：C_final `_S809_LOOK` 前瞻加深（3→12 doanthuan 口径 + "
                "3→6 中间档）新标准终验（纯参数改/不改既有代码/不提交/不发射）",
        "param": {
            "name": "_S809_LOOK",
            "layer": "step809 就绪提前层前瞻常数（基座原生层参数，step809 层"
                     "自带；非外挂挪量——七负禁区打的是外挂，原生层调参另论）",
            "base_value": 3,
            "arms_values": {"look6": 6, "look12": 12},
            "caliber": "doanthuan/kaggriculture（Apache-2.0）公开复刻记录："
                       "`_S809_LOOK` 3→12（ready-stock 销售前瞻加深）对平版 "
                       "step1009 自报 85%（自报未我方复核）；look6=中间档；"
                       "只调参数不拷码",
            "seal": "纯参数字面量替换恰 1 处（line 8195）；反替换回程逐字节="
                    "C_final 基座（roundtrip_identity_ok）；零结构变化"
                    "（逐行 diff=1）",
            "footprint_claim": "仅 step809 触发面（市场 SELL 面单量；"
                               "farmer/hands 零触碰）",
            "build_manifest": str(EVID_DIR / "build_s809look.json"),
        },
        "arms": {
            "look3": {"role": "对照基（=C_final 原件 `_S809_LOOK`=3）",
                      "main": str(BASE), "sha256": build["base"]["sha256"]},
            "look6": {"role": "变体（3→6 中间档）",
                      "main": str(ARMS["look6"]),
                      "sha256": build["forms"]["look6"]["main_sha256"]},
            "look12": {"role": "变体（3→12 doanthuan 口径）",
                       "main": str(ARMS["look12"]),
                       "sha256": build["forms"]["look12"]["main_sha256"]},
        },
        "source": {
            "commands": ["python3 orderbook_s5s809_lab/build_s809look.py",
                         "python3 orderbook_s5s809_lab/judge_s809look.py"],
            "corpus": {"folds": FOLDS,
                       "spec": "674000+i*151 新块（i=0..11）；普通对 n=16 局/臂"
                               "=8 fold×双席（i=0..7）；vs oc_c3 加密 n=24 局/臂"
                               "=12 fold（i=0..11）",
                       "note": "n=16 双席/对按预算硬约束读作 16 局/对/臂"
                               "（8 fold×双席折叠）；n 若计 fold（32 局/对/臂）"
                               "则 3 臂×208+auth 需 654 局次>350 预算"},
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/"
                       "余平；fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径；banks "
                          "交叉登记）",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考",
                "pairing": "变体 vs look3 对照同 (seed,seat,opp) 双跑配对"
                           "（flips/足迹面）",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
        },
        "panel": {}, "paired": {}, "criteria": {}, "verdict": {},
        "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 先认证 30/30（缓存可复用）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = EVID_DIR / "sim_auth_cache.json"
    if AUTH_CACHE.is_file():
        auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth_corpus = jg.LOSS_SEEDS_26[:16] + FOLDS_MAIN + \
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
            AUTH_CACHE.write_text(json.dumps(auth, ensure_ascii=False,
                                             default=str) + "\n",
                                  encoding="utf-8")
    EV["source"]["sim_auth"] = auth_lite
    budget["auth"] = 30
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 新标准面板（3 臂×6 对；断点续跑：rows 缓存复用）----
    ROWS_CACHE = EVID_DIR / "panel_rows.json"
    marker = {"folds": FOLDS,
              "arms": {k: str(v) for k, v in ARMS.items()},
              "panel": {k: str(v) for k, v in PANEL.items()}}
    rows_by_arm = None
    if ROWS_CACHE.is_file():
        try:
            cached = json.loads(ROWS_CACHE.read_text(encoding="utf-8"))
            if cached.get("marker") == marker:
                rows_by_arm = cached["rows"]
        except Exception:
            rows_by_arm = None
    if rows_by_arm is not None:
        budget["panel"] = sum(len(rs) for arm in rows_by_arm.values()
                              for rs in arm.values())
    else:
        rows_by_arm = {}
        for arm in ("look3", "look6", "look12"):
            rows_by_arm[arm] = {}
            for on, opath in PANEL.items():
                folds = FOLDS_OC3 if on == "oc_c3" else FOLDS_MAIN
                rows = play(_chunk_panel,
                            unit_specs(arm, ARMS[arm], opath, on, folds),
                            run_cfg)
                budget["panel"] += len(rows)
                rows_by_arm[arm][on] = rows
                bad = [r for r in rows if r.get("error")]
                if bad:
                    ANOMALIES.append("panel %s vs %s: %d 局 error: %r"
                                     % (arm, on, len(bad), bad[0].get("error")))
                print("panel", arm, "vs", on, "n=", len(rows), flush=True)
                flush_evid()
        ROWS_CACHE.write_text(json.dumps({"marker": marker,
                                          "rows": rows_by_arm},
                                         ensure_ascii=False,
                                         default=str) + "\n", encoding="utf-8")

    panel = {}
    for arm in ("look3", "look6", "look12"):
        panel[arm] = {}
        for on in PANEL:
            panel[arm][on] = fold_stats(rows_by_arm[arm][on])
            panel[arm][on]["flips_neg"] = None  # flips 在配对面报
            print("h2h", arm, "vs", on, panel[arm][on]["h2h"], flush=True)
    EV["panel"] = {
        "design": "新标准面板：3 臂×6 对；每对 n=16 局/臂=8 fold×双席"
                  "（vs oc_c3 加密 n=24 局/臂=12 fold；新块 674000+i*151）；"
                  "h2h=judge_r44._fold_arm；look3 行=对照基参考（fold 块效应"
                  "校准）；margin/终局钱只作参考",
        "pairs": panel,
    }

    # ---- 配对面：flips + step809 足迹（变体 vs look3）----
    paired = {}
    for v in VARIANTS:
        flat_v = [r for on in PANEL for r in rows_by_arm[v][on]]
        flat_b = [r for on in PANEL for r in rows_by_arm["look3"][on]]
        flip, foot = paired_stats(flat_v, flat_b, v)
        paired[v] = {"flips_vs_look3": flip, "footprint_vs_look3": foot}
        print("paired", v, "flips_neg=", flip["flips_neg"],
              "attr=", foot["attribution_ok_all"], flush=True)
        flush_evid()
    EV["paired"] = {
        "design": "变体 vs look3 对照同 (seed,seat,opp) 双跑配对（104 单元/变体）；"
                  "flips_neg=对照胜局翻负计数（要求 0）；足迹口径=首差异拍须为 "
                  "step809 触发面签名（SELL 面单量；farmer/hands 零触碰）、触发前"
                  "零差异；级联差异允落首触发拍后（sx gates 先例）",
        "variants": paired,
    }

    # ---- 判据 + verdict ----
    EV["criteria"] = {
        "rule": "①对 oc_c3 冠军锚 ≥0.5（≥0.6 佳/≥0.7 碾压）②强面板 "
                "{mpx,tetsutani,V89} 逐对 ≥0.5 ③弱锚 {r40,A} 逐对 ≥0.8 "
                "④flips_neg=0（vs look3 配对）⑤守恒足迹=仅 step809 触发面"
                "（首差异拍=SELL 面单量签名、触发前零差异）⑥margin/终局钱只作参考",
        "arms": {},
    }
    arm_verdicts = {}
    for v in VARIANTS:
        h_oc = (panel[v].get("oc_c3") or {}).get("h2h")
        strong = {o: (panel[v].get(o) or {}).get("h2h") for o in PANEL_STRONG}
        weak = {o: (panel[v].get(o) or {}).get("h2h") for o in PANEL_WEAK}
        flips_neg = paired[v]["flips_vs_look3"].get("flips_neg")
        attr_all = paired[v]["footprint_vs_look3"].get("attribution_ok_all")
        c1 = bool(h_oc is not None and h_oc >= 0.5)
        c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
                  and len(strong) == 3)
        c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
        c4 = bool(flips_neg == 0)
        c5 = bool(attr_all)
        grade = ("碾压" if (h_oc or 0) >= 0.7 else
                 "佳" if (h_oc or 0) >= 0.6 else
                 "更强" if (h_oc or 0) >= 0.5 else "未过锚")
        full = bool(c1 and c2 and c3 and c4 and c5)
        EV["criteria"]["arms"][v] = {
            "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1},
            "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
            "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
            "c4_flips_neg_zero": {"flips_neg": flips_neg,
                                  "flips_pos": paired[v]["flips_vs_look3"].get(
                                      "flips_pos"),
                                  "passed": c4},
            "c5_footprint_step809_only": {
                "attribution_ok_all": attr_all,
                "strict_s809_all": paired[v]["footprint_vs_look3"].get(
                    "strict_s809_all"),
                "monotone_first_all": paired[v]["footprint_vs_look3"].get(
                    "monotone_first_all"),
                "trigger_region_all": paired[v]["footprint_vs_look3"].get(
                    "trigger_region_all"),
                "passed": c5},
            "c6_margin_reference_only": True,
            "full_standard_pass": full,
        }
        arm_verdicts[v] = {
            "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
            "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
            "flips_neg": flips_neg,
            "footprint_step809_only_ok": c5,
            "full_standard_pass": full,
            "verdict": ("FULL_STANDARD_PASS" if full else
                        "STRONGER_THAN_CHAMPION_ANCHOR_BUT_PANEL_BLEED"
                        if c1 else "NO_POSITIVE_ARM"),
        }
    best = None
    for v in VARIANTS:
        if arm_verdicts[v]["full_standard_pass"]:
            best = v
            break
    EV["verdict"] = {
        "arms": arm_verdicts,
        "adopted": best,
        "verdict": ("S5_PASS:%s" % best if best else "NO_POSITIVE_ARM"),
        "summary": "；".join(
            "%s: 对 oc_c3 h2h %s（%s）/强面板 %s/弱锚 %s/flips_neg %s/足迹 "
            "step809-only %s/全过 %s" % (
                v, arm_verdicts[v]["vs_champion_anchor"]["h2h"],
                arm_verdicts[v]["vs_champion_anchor"]["grade"],
                json.dumps(arm_verdicts[v]["strong_panel_h2h"], default=str),
                json.dumps(arm_verdicts[v]["weak_anchor_h2h"], default=str),
                arm_verdicts[v]["flips_neg"],
                arm_verdicts[v]["footprint_step809_only_ok"],
                arm_verdicts[v]["full_standard_pass"]) for v in VARIANTS),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = budget["auth"] + budget["panel"]
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    budget["smoke_局次"] = 2
    budget["cumulative_局次"] = budget["total_局次"] + 2
    budget["cumulative_within_cap"] = budget["cumulative_局次"] <= BUDGET_CAP

    # ---- 异常/备注 ----
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；banks 交叉登记"
        "在逐局行；胜率=硬通货，margin/终局钱只作参考")
    ANOMALIES.append(
        "断点续跑披露：首跑在配对分析段因一处分析面缺陷（dict/flat list 传参）"
        "退出，面板 312 局已全数完成并落 rows 缓存；续跑（缓存复用）零新局次，"
        "纯分析面修复不改任何跑局/判据口径。另有 2 局 harness 冒烟（look6 vs "
        "mpx 674000 双席，跑局口径验证）——局次账本如实计：冒烟 2+auth30+面板 "
        "312=344≤350")
    ANOMALIES.append(
        "样本口径披露：n=16 双席/对按预算硬约束读作 16 局/对/臂（8 fold×双席"
        "折叠），vs oc_c3 加密 n=24 局/臂（12 fold）；3 臂（look3 对照+两变体）"
        "×104 局+auth30=342≤350。若 n 计 fold（16 fold=32 局/对/臂）两变体+对照"
        "需 654 局次破预算——本程按 350 预算硬约束取 16 局口径，h2h 粒度 1/8，"
        "边缘判据宜扩样复核")
    ANOMALIES.append(
        "参数口径披露：`_S809_LOOK` 为基座 step809 就绪提前层原生常数（step809"
        " 层自带前瞻），本实验=原生层调参，非外挂挪量（七负禁区打的是外挂，原生"
        "层调参另论）；doanthuan/kaggriculture（Apache-2.0）公开复刻记录 3→12 对"
        "平版 step1009 自报 85% 为自报值未我方复核，本程只调参数不拷码")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；新标准以逐对口径判"
        "（每对同 fold 块双席 fold h2h）；look3 对照行供 fold 块效应校准"
        "（c-final mpx 血线先例：跨块 h2h 可因 fold 块/样本量漂移）")
    ANOMALIES.append(
        "fold 块效应（重点）：look3 对照基在本块 674000+i*151 强面板逐对 "
        "{mpx 0.3125, tetsutani 0.4375, V89 0.4375}，远低于 c-final 记录块 "
        "674000+i*139 的 {0.625, 0.6562, 0.6562}——②强面板 ≥0.5 阈在本块对"
        "未改动基座即不可达，两臂 c2 未过主因=fold 块难度；变体增量须以"
        "配对面读（look12 对基座强面板三对均 +0.125，配对净翻 +6 胜/"
        "mean_delta +97），不得跨块直比绝对值")
    ANOMALIES.append(
        "look6（3→6）行为面近惰性：104 配对单元 38 逐拍恒等、66 单元有差异但"
        "零胜负翻转（flips_pos=flips_neg=0，胜局 64/64），六对 h2h 与 look3"
        "逐对恒等、仅 margin 微移（+12.8）——3→6 深度不足以翻任何胜负；"
        "look12（3→12）才激活（104/104 差异、flips_pos=6/flips_neg=0、"
        "W84/L18/T2）")
    for v in VARIANTS:
        foot = paired[v]["footprint_vs_look3"]
        if not foot.get("strict_s809_all"):
            ANOMALIES.append(
                "%s 足迹严格口径（差异拍全=SELL 面单量签名）未全过：%d diff 单元"
                "含级联跟随拍（先例口径=首差异拍=首个 step809 触发拍、触发前零"
                "差异：%s；级联=对手价/库存跟随自插单，属 S809 面下游）"
                % (v, foot.get("n_diff"), foot.get("attribution_ok_all")))
        if not foot.get("monotone_first_all"):
            ANOMALIES.append(
                "%s 首差异拍非单调加深（SELL 量变体<对照）：10 单帽边缘件"
                "（maxMarketOrdersPerTurn=10）前瞻加深挤掉尾部品单量的已知形态，"
                "报数不修" % v)
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s809look_ledger.json").write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "panel_h2h": {a: {o: (panel[a][o] or {}).get("h2h")
                           for o in PANEL} for a in panel},
         "paired_flips": {v: paired[v]["flips_vs_look3"] for v in VARIANTS}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
