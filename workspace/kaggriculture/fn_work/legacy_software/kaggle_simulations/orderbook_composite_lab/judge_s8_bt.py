# -*- coding: utf-8 -*-
"""judge_s8_bt（composite lab）：S8 全场 BT 评级补测（只测不发/不提交）。

S8（orderbook_s8spike_lab/build/s8/main.py，sha a59208fe…）从未进过全场 BT 拟合，
只测过小面板（块 674000+i*159）。本判决按 crown-final 协议补全全场矩阵：
1. S8 vs 全场 13 件（champion-tourney 件单：H1/oc_c3/mpx/H/drop_half/tetsutani/
   V89/e087/prvsiyan/r40/A/r37/r34a）+ S8 vs C_final 直接对战，每对 12 fold 双席
   （块 674000+i*141，与 C_final crown_base 同块可比）；h2h=judge_r44._fold_arm
   双席折叠；margin=farms[obs.player] 终局钱差（banks 交叉登记）。
2. BT 合并拟合（口径经双向锚定复现验证：champion-tourney 13 件与 crown-final
   14 件重排均逐位复现）：
   - fit_s8_14：78 旧格 + S8 13 新格 → 14 件重排（与 C_final 324.3 同协议孪生）；
   - fit_full15：78 旧格 + C_final 13 格 + S8 13 格 + S8|C_final 1 格 → 15 件；
   - fit_s8_anchored：老 13 件 pi 冻结于 champion-tourney（H1=527.8 标度），
     解 S8 单参 pi → 直接与 528 天花板判读。
3. 判读三档：anchored bt ≥528 已达/超天花板；450-528 接近；<400 低于王座。
sim_bridge 认证缓存复用（30/30 先例）；workers=2；预算 ≤800 局次；
确定性双跑抽查；异常局 fail-closed 记录；H1/oc_c3 孪生对照零成本交叉核验。
证据 fn_docs/hybrid/results/2026-09-30-s8-bt-fullpanel.json（含逐局行）。
只测不发：不在线提交、不发射、不改既有代码。
"""
from __future__ import annotations

import hashlib
import json
import math
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for _p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-s8-bt-fullpanel.json"
CT_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-champion-tourney.json"
CF_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-crown-final.json"
ROW_CACHE = EVID_DIR / "s8_bt_rows.json"

S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
CFINAL = HERE / "build" / "c_final" / "main.py"
RESTORE = REPO / "fn_docs" / "references" / "data" / "arms-restore-20261001"

# 件单=champion-tourney 13 件（sha 前缀=crown-final.json versions 口径）
OPPS = {
    "H1": (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py",
           "76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764974b22f337"),
    "oc_c3": (KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py",
              "3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39ba9bd23d"),
    "mpx": (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
            / "main.py",
            "f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72c3d84e44f"),
    "H": (KSIM_DIR / "orderbook_v94_lab" / "build" / "haodou_v82" / "main.py",
          "bdb821178ca73c0e8480f06c1887e20921caea0438398a5edb68bd9ad20b1de8"),
    "drop_half": (KSIM_DIR / "orderbook_unified_u2_lab" / "build"
                  / "u2v2_drop_half" / "main.py",
                  "5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2ce7992df0"),
    "tetsutani": (KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
                  / "main.py",
                  "55be5d5f124c8daaaa63c1a29ba4aab096004909666f04748007603c67b7d2a8"),
    "V89": (KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
            "01ee3976f97a9ac71be40eff667b24c5a69cd86fce88bbbdf25ea1e10aecd60d"),
    "e087": (RESTORE / "mooman_e087" / "main.py",
             "ccba51e12d4d470b47eb3e38528aae7cb03caca7b09b5aa8739dc4a52942d6d7"),
    "prvsiyan": (RESTORE / "prvsiyan_melons" / "main.py",
                 "178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a"),
    "r40": (KSIM_DIR / "orderbook_r40" / "build" / "main.py",
            "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8"),
    "A": (KSIM_DIR / "orderbook_r44_a" / "main.py",
          "b387307fc12e26107c58ee604146fc621099ce88124fa0876fdd7cef28300bd9"),
    "r37": (KSIM_DIR / "orderbook_r37" / "build" / "main.py",
            "4b237e412d5101937ad66aa0751454721dec2d5a73fa2743d65768b286a2cb3f"),
    "r34a": (KSIM_DIR / "orderbook_2965_adopt" / "a" / "main.py",
             "51fc19dba2d0bcbf2d0a3720c26ff318541a0e6ce5800873bc863f612451aa5b"),
}
CF_SHA = "a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b077016a92"
S8_SHA = "a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae04e7c0a6"
PANEL_ORDER = ["H1", "oc_c3", "mpx", "H", "drop_half", "tetsutani", "V89",
               "e087", "prvsiyan", "r40", "A", "r37", "r34a", "C_final"]
FOLDS = [674000 + i * 141 for i in range(12)]   # 与 crown-final base 同块
DET_SPOTS = [("H1", 674000, 0), ("H1", 674141, 1), ("oc_c3", 675269, 0),
             ("C_final", 674000, 1), ("mpx", 675551, 0), ("r34a", 674282, 1)]
WORKERS = 2
BUDGET_CAP = 800

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 0, "smoke": 0, "panel": 0,
          "det_check": 0}


def flush_evid():
    EV["budget"] = dict(BUDGET)
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ============================================================ 跑口 ==
def _chunk_panel(payload):
    """panel worker（crown-final _chunk_panel 同口径）：终局钱 farms[obs.player]
    + banks 交叉登记；每局全新命名空间（j23._load_entry）。"""
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
               "opponent": spec.get("opponent"), "variant": spec.get("arm"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None}
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


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk_panel(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk_panel, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(arm, arm_path, opp_path, opp_name, folds, seats=(0, 1)):
    specs = []
    for seed in folds:
        for seat in seats:
            specs.append({
                "game_id": "s8bt-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "kind": "ab", "trace": True,
                "agents": [{"type": "python", "path": str(arm_path)},
                           {"type": "python", "path": str(opp_path)}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def fold_stats(rows):
    """judge_r44._fold_arm 双席折叠（fail-closed：缺席/红局=负）。"""
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows
           if isinstance(r.get("tm_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin_clean"] = round(
        sum(r["margin_clean"] for r in rows if r["margin_clean"] is not None)
        / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(
        sum(r["margin_banks"] for r in rows
            if r.get("margin_banks") is not None) / max(1, len(rows)), 1)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


# ============================================================ BT 拟合 ==
def bt_rating(pi):
    return round(1000.0 * math.log10(pi), 1)


def mm_fit(names, cells, iters=20000, tol=1e-14):
    """BT-MM（平局各记 0.5 胜；pi 几何均值=1 归一）——champion-tourney /
    crown-final 拟合口径，已双向逐位复现验证。cells[(a,b)]=(W_a,L_a,T)。"""
    idx = {n: i for i, n in enumerate(names)}
    n = len(names)
    wins = [0.0] * n
    games = [[0.0] * n for _ in range(n)]
    for (a, b), (W, L, T) in cells.items():
        i, j = idx[a], idx[b]
        wins[i] += W + 0.5 * T
        wins[j] += L + 0.5 * T
        games[i][j] += W + L + T
        games[j][i] += W + L + T
    pi = [1.0] * n
    for _ in range(iters):
        new = []
        for i in range(n):
            denom = sum(games[i][j] / (pi[i] + pi[j])
                        for j in range(n) if i != j and games[i][j])
            new.append(wins[i] / denom if denom > 0 else pi[i])
        g = math.exp(sum(math.log(x) for x in new) / n)
        new = [x / g for x in new]
        if max(abs(a - b) for a, b in zip(new, pi)) < tol:
            pi = new
            break
        pi = new
    out = {name: round(pi[i], 4) for i, name in enumerate(names)}
    return out


def fit_row(name, pi_map):
    return {"name": name, "bt_pi": pi_map[name], "bt_rating": bt_rating(pi_map[name])}


def put_cell(cells, x, y, W_x, L_x, T):
    """以 x 视角 (W,L,T) 存入 canonical (a,b) 槽。"""
    key = (x, y) if x < y else (y, x)
    cells[key] = (W_x, L_x, T) if key == (x, y) else (L_x, W_x, T)


def anchored_place(s8_cells, frozen_pi):
    """老 13 件 pi 冻结（champion-tourney 标度，H1=527.8），解 S8 单参 pi。
    s8_cells: {opp: (W,L,T)}（S8 视角，fold 级）。"""
    x = 1.0
    for _ in range(20000):
        w = sum(W + 0.5 * T for (W, L, T) in s8_cells.values())
        denom = sum((W + L + T) / (x + frozen_pi[o])
                    for o, (W, L, T) in s8_cells.items())
        new = w / denom
        if abs(new - x) < 1e-15:
            x = new
            break
        x = new
    exp = {}
    for o, (W, L, T) in s8_cells.items():
        n = W + L + T
        exp[o] = {"n": n, "observed_h2h": round((W + 0.5 * T) / n, 4) if n else None,
                  "expected_h2h": round(x / (x + frozen_pi[o]), 4)}
    return {"bt_pi": round(x, 4), "bt_rating": bt_rating(x), "calibration": exp}


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    # ---- sha 核验（fail-closed）----
    versions = {}
    bad = []
    versions["S8"] = {"path": str(S8), "sha256": sha256_file(S8),
                      "bytes": S8.stat().st_size}
    if versions["S8"]["sha256"] != S8_SHA:
        bad.append("S8 sha mismatch")
    versions["C_final"] = {"path": str(CFINAL), "sha256": sha256_file(CFINAL),
                           "bytes": CFINAL.stat().st_size}
    if versions["C_final"]["sha256"] != CF_SHA:
        bad.append("C_final sha mismatch")
    for on, (opath, osha) in OPPS.items():
        versions[on] = {"path": str(opath), "sha256": sha256_file(opath),
                        "bytes": opath.stat().st_size}
        if versions[on]["sha256"] != osha:
            bad.append("%s sha mismatch" % on)
    if bad:
        EV.update({"version": "s8-bt-fullpanel/1.0",
                   "verdict": {"aborted": "sha 校验未过: %s" % bad}})
        flush_evid()
        return EV

    EV.update({
        "version": "s8-bt-fullpanel/1.0",
        "task": "S8 全场 BT 评级补测（终窗发射决策数据；只测不发/不在线提交）",
        "subject": {
            "arm": "S8", "sha256": S8_SHA, "bytes": versions["S8"]["bytes"],
            "path": str(S8),
            "provenance": "S8 = s_append(4608e9e0…)+尖拍尾块；小面板先读数见 "
                          "2026-09-30-s8-spike.json（块 674000+i*159，"
                          "oc_c3 0.5625/mpx 0.656/tetsutani 0.72/V89 0.72/"
                          "r40 0.78/A 0.91）",
        },
        "source": {
            "commands": ["python3 orderbook_composite_lab/judge_s8_bt.py"],
            "machine": "judge_r44._fold_arm / j23._load_entry + sim_bridge"
                       "（crown-final 同口径）",
            "corpus": {
                "base_folds": FOLDS,
                "base_spec": "674000+i*141（i=0..11，12 fold/对，与 C_final "
                             "crown_base 同块可比）",
                "pairs": "S8 vs 13 件全场矩阵 + S8 vs C_final 直接对战，"
                         "每对 12 fold 双席=24 局",
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm：同 seed 双席折叠（score=两席均分，"
                       "≥1 胜/≤0 负/余平），fail-closed（缺席/红局=负）",
                "margin": "farms[obs.player].money 终局钱差（jg.econ_face，"
                          "逐席干净口径；仅参考）",
                "margin_banks": "banks[a]−banks[b]（run_games banks 交叉登记）",
                "load": "j23._load_entry 官方 last-callable 语义，每局全新命名空间",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考",
            },
            "restore_note": "e087/prvsiyan 外部原件（/tmp/arms_e）已失：e087 经 "
                            "GitHub raw 重取、prvsiyan 经战役内 s_melon 去 1650B "
                            "署名头还原，均按 sha256 逐字节核验一致后直跑"
                            "（零修改）；H/tetsutani 用战役内 sha 同值副本直跑",
        },
        "versions": versions,
        "pairs": {}, "rows_all": [], "det_check": {}, "twin_check": {},
        "bt": {}, "verdict": {},
    })

    # ---- sim_bridge 认证缓存复用（30/30 先例）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = EVID_DIR / "sim_auth_cache.json"
    auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    auth_lite["reused_cache"] = True
    EV["source"]["sim_auth"] = auth_lite
    BUDGET["auth"] = 30
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证缓存未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- smoke 2 局（canary，不入判据）----
    smoke = play(unit_specs("S8", S8, OPPS["oc_c3"][0], "oc_c3",
                            [FOLDS[0]], seats=(0,)), run_cfg)
    BUDGET["smoke"] = len(smoke)
    if any(r.get("error") for r in smoke) or \
            any(r.get("margin_clean") is None for r in smoke):
        ANOMALIES.append("smoke canary 异常：%s" % json.dumps(smoke, default=str)[:300])
    flush_evid()

    # ---- 断点续跑缓存 ----
    marker = {"folds": FOLDS, "arm": str(S8), "arm_sha": S8_SHA,
              "opps": {k: str(v[0]) for k, v in OPPS.items()},
              "cfinal": str(CFINAL)}
    rows_by_key = {}
    if ROW_CACHE.is_file():
        try:
            cached = json.loads(ROW_CACHE.read_text(encoding="utf-8"))
            if cached.get("marker") == marker:
                for r in cached["rows"]:
                    rows_by_key[(r["opponent"], int(r["seed"]),
                                 int(r["seat"]))] = r
        except Exception:
            rows_by_key = {}

    def save_rows():
        ROW_CACHE.write_text(json.dumps(
            {"marker": marker, "rows": list(rows_by_key.values())},
            ensure_ascii=False, default=str) + "\n", encoding="utf-8")

    # ---- 全场矩阵：13 件 + C_final ----
    targets = [(on, OPPS[on][0]) for on in PANEL_ORDER if on != "C_final"]
    targets.append(("C_final", CFINAL))
    for on, opath in targets:
        specs = unit_specs("S8", S8, opath, on, FOLDS)
        todo = [s for s in specs
                if (on, int(s["seed"]), int(s["our_seat"])) not in rows_by_key]
        if todo:
            new_rows = play(todo, run_cfg)
            for r in new_rows:
                rows_by_key[(r["opponent"], int(r["seed"]), int(r["seat"]))] = r
            BUDGET["panel"] += len(new_rows)
            save_rows()
        rows = [rows_by_key[(on, s, seat)] for s in FOLDS for seat in (0, 1)]
        fs = fold_stats(rows)
        EV["pairs"][on] = dict(fs)
        print("S8 vs %-10s h2h=%s W%s L%s T%s n=%s margin=%s"
              % (on, fs["h2h"], fs["wins"], fs["losses"], fs["ties"],
                 fs["n"], fs["mean_margin"]), flush=True)
        flush_evid()

    # ---- 逐局行（证据内嵌）----
    EV["rows_all"] = [
        {"pair": "S8|%s" % k[0], "seed": k[1], "seat": k[2],
         "tm_us": r.get("tm_us"), "tm_opp": r.get("tm_opp"),
         "margin_clean": r.get("margin_clean"),
         "margin_banks": r.get("margin_banks"), "banks": r.get("banks"),
         "error": r.get("error")}
        for k, r in sorted(rows_by_key.items())]
    n_err = sum(1 for r in rows_by_key.values() if r.get("error"))
    n_cal_gap = sum(1 for r in rows_by_key.values()
                    if r.get("margin_clean") is not None
                    and r.get("margin_banks") is not None
                    and abs(float(r["margin_clean"]) - float(r["margin_banks"])) > 0)
    if n_err:
        ANOMALIES.append({"kind": "error_rows", "n": n_err,
                          "note": "fail-closed：红局 fold 记负，不修不管"})
    ANOMALIES.append({"kind": "caliber_gap_rows", "n": n_cal_gap,
                      "note": "farms 终局钱差 vs banks 差口径缝（crown-final 同款）；"
                              "主口径=farms 终局钱，banks 交叉登记于 rows_all"})

    # ---- 确定性双跑抽查 ----
    det = []
    for on, seed, seat in DET_SPOTS:
        opath = CFINAL if on == "C_final" else OPPS[on][0]
        orig = rows_by_key[(on, seed, seat)]
        re_rows = play(unit_specs("S8", S8, opath, on, [seed], seats=(seat,)),
                       run_cfg)
        rr = re_rows[0] if re_rows else {}
        same = (rr.get("banks") == orig.get("banks")
                and rr.get("margin_clean") == orig.get("margin_clean"))
        det.append({"pair": "S8|%s" % on, "seed": seed, "seat": seat,
                    "identical": bool(same),
                    "banks": orig.get("banks"), "banks_rerun": rr.get("banks"),
                    "margin_clean": orig.get("margin_clean"),
                    "margin_rerun": rr.get("margin_clean")})
    BUDGET["det_check"] = len(DET_SPOTS)
    EV["det_check"] = {
        "design": "同槽位双跑逐值恒等抽查（sim 确定性口径，crown-final "
                  "replay_consistency 先例）",
        "n": len(det), "n_identical": sum(1 for d in det if d["identical"]),
        "spots": det}
    if EV["det_check"]["n_identical"] != len(det):
        ANOMALIES.append({"kind": "det_check_fail",
                          "note": "确定性抽查未全同：%s" % [
                              d for d in det if not d["identical"]]})

    # ---- H1/oc_c3 孪生对照（零成本交叉核验）----
    tw_mis = 0
    tw_n = 0
    for seed in FOLDS:
        for seat in (0, 1):
            a = rows_by_key.get(("H1", seed, seat))
            b = rows_by_key.get(("oc_c3", seed, seat))
            if a and b:
                tw_n += 1
                if a.get("margin_clean") != b.get("margin_clean"):
                    tw_mis += 1
    EV["twin_check"] = {
        "design": "H1/oc_c3 行为孪生（champion-tourney behavioral_twins 先例）："
                  "S8 对两者同槽位读数应逐局同值",
        "n_slots": tw_n, "n_mismatch": tw_mis}
    if tw_mis:
        ANOMALIES.append({"kind": "twin_check_mismatch", "n": tw_mis,
                          "note": "H1/oc_c3 同槽位读数不等"})

    # ---- BT 合并拟合 ----
    ct = json.loads(CT_PATH.read_text(encoding="utf-8"))
    cf = json.loads(CF_PATH.read_text(encoding="utf-8"))
    names13 = [r["name"] for r in ct["bt_ratings"]]
    cells_old = {}
    for v in ct["pairs"].values():
        put_cell(cells_old, v["a"], v["b"], v["W"], v["L"], v["T"])
    cells_cf = {}
    for on, pv in cf["pairs"].items():
        c = pv["combined"]
        put_cell(cells_cf, "C_final", on, c["W"], c["L"], c["T"])
    cells_s8 = {}
    for on in PANEL_ORDER:
        if on == "C_final":
            continue
        f = EV["pairs"][on]
        put_cell(cells_s8, "S8", on, f["wins"], f["losses"], f["ties"])
    fs_cf = EV["pairs"]["C_final"]
    cell_s8_cf = (fs_cf["wins"], fs_cf["losses"], fs_cf["ties"])

    # 口径复现验证（双向锚定）
    repro13 = mm_fit(names13, cells_old)
    max13 = max(abs(repro13[r["name"]] - r["bt_pi"]) for r in ct["bt_ratings"])
    names14cf = [r["name"] for r in cf["bt_rankings"]["rows"]]
    repro14cf = mm_fit(names14cf, {**cells_old, **cells_cf})
    max14cf = max(abs(repro14cf[r["name"]] - r["bt_pi"])
                  for r in cf["bt_rankings"]["rows"])

    # fit_s8_14（与 crown-final 14 件重排同协议：78 旧格 + 新件 13 格）
    names14s8 = names13 + ["S8"]
    pi_s8_14 = mm_fit(names14s8, {**cells_old, **cells_s8})
    rows_s8_14 = [fit_row(n, pi_s8_14) for n in
                  sorted(names14s8, key=lambda n: -pi_s8_14[n])]
    for i, r in enumerate(rows_s8_14):
        r["rank"] = i + 1

    # fit_full15（78 旧格 + C_final 13 格 + S8 13 格 + S8|C_final）
    names15 = names13 + ["C_final", "S8"]
    cells15 = {**cells_old, **cells_cf, **cells_s8}
    put_cell(cells15, "S8", "C_final", *cell_s8_cf)
    pi_15 = mm_fit(names15, cells15)
    rows15 = [fit_row(n, pi_15) for n in sorted(names15, key=lambda n: -pi_15[n])]
    for i, r in enumerate(rows15):
        r["rank"] = i + 1

    # anchored（champion-tourney 标度：老 13 件 pi 冻结）
    frozen = {r["name"]: r["bt_pi"] for r in ct["bt_ratings"]}
    anc = anchored_place(
        {on: (EV["pairs"][on]["wins"], EV["pairs"][on]["losses"],
              EV["pairs"][on]["ties"]) for on in PANEL_ORDER
         if on != "C_final"}, frozen)

    EV["bt"] = {
        "design": "champion-tourney 78 旧格（13 件，块 674000+i*131）+ "
                  "crown-final C_final 13 格（combined 折叠）+ S8 14 新格"
                  "（块 674000+i*141）合并 Bradley-Terry MM（平局各记 0.5 胜，"
                  "pi 几何均值=1；rating=1000·log10(pi)）",
        "caliber_reproduction": {
            "champion_tourney_13": {
                "max_abs_pi_diff": round(max13, 6),
                "ref": "2026-09-30-champion-tourney.json bt_ratings（H1=527.8）",
                "reproduced": {"H1": repro13["H1"], "r34a": repro13["r34a"]}},
            "crown_final_14": {
                "max_abs_pi_diff": round(max14cf, 6),
                "ref": "2026-09-30-crown-final.json bt_rankings（H1=439.6/"
                       "C_final=324.3）",
                "reproduced": {"H1": repro14cf["H1"],
                               "C_final": repro14cf["C_final"]}},
            "ok": bool(max13 < 5e-4 and max14cf < 5e-4),
        },
        "fit_s8_14": {
            "design": "协议孪生：78 旧格 + S8 13 新格 → 14 件重排（C_final 的 "
                      "crown-final 同协议槽位）",
            "rows": rows_s8_14,
            "s8_bt_rating": bt_rating(pi_s8_14["S8"]),
            "cfinal_ref_rating_same_protocol": 324.3,
            "h1_ref_rating_same_protocol": 439.6,
        },
        "fit_full15": {
            "design": "全合并：78 旧格 + C_final 13 格 + S8 13 格 + S8|C_final "
                      "1 格 = 105 格 = C(15,2) 全矩阵",
            "rows": rows15,
            "s8_bt_rating": bt_rating(pi_15["S8"]),
            "s8_rank": next(r["rank"] for r in rows15 if r["name"] == "S8"),
        },
        "fit_s8_anchored": {
            "design": "锚定放置：老 13 件 pi 冻结于 champion-tourney 拟合"
                      "（H1=527.8 标度），S8 由 13 新格解单参 pi → 直接与 528 "
                      "天花板判读",
            "bt_pi": anc["bt_pi"], "bt_rating": anc["bt_rating"],
            "calibration": anc["calibration"],
        },
        "anchors": {
            "champion_tourney_scale": {"H1": 527.8, "oc_c3": 527.8,
                                       "mpx": 304.1, "C_final": None},
            "crown_final_refit_scale": {"H1": 439.6, "oc_c3": 439.6,
                                        "C_final": 324.3, "mpx": 297.6},
            "note": "rating=1000·log10(pi) 为固定变换；pi 随拟合成分漂移"
                    "（加入新件即重排），跨拟合比较以同拟合内相对位置与 "
                    "anchored（冻结标度）为准",
        },
    }
    flush_evid()

    # ---- 判读三档 ----
    r_anc = anc["bt_rating"]
    band = ("已达/超天花板（S8_bt≥528）" if r_anc >= 528 else
            "接近（450≤S8_bt<528）" if r_anc >= 450 else
            "过渡带（400≤S8_bt<450，低于接近带下缘）" if r_anc >= 400 else
            "低于王座（S8_bt<400，换对有必要）")
    anchor_h2h = None
    anchor_fold = None
    try:
        # 冠军锚合并（crown-final champion_anchor 口径）：H1+oc_c3 两对 fold 级
        # 合并（n=24）；注意不能按 seed 池化逐局行——孪生对同 seed 会 4 行/seed
        # 触发 _fold_arm fail-closed（首跑此处 0.0 系该口径缝，已修）。
        w = EV["pairs"]["H1"]["wins"] + EV["pairs"]["oc_c3"]["wins"]
        l = EV["pairs"]["H1"]["losses"] + EV["pairs"]["oc_c3"]["losses"]
        t = EV["pairs"]["H1"]["ties"] + EV["pairs"]["oc_c3"]["ties"]
        n = EV["pairs"]["H1"]["n"] + EV["pairs"]["oc_c3"]["n"]
        anchor_fold = {"n_folds": n, "W": w, "L": l, "T": t}
        anchor_h2h = round((w + 0.5 * t) / n, 4)
    except Exception:
        pass
    EV["verdict"] = {
        "question": "有没有比王座（H1/oc_c3，BT 527.8）更好的版本？现计分对 "
                    "{C_final, S8} 是否已含天花板？",
        "s8_anchored_bt_rating": r_anc,
        "s8_fit_s8_14_bt_rating": bt_rating(pi_s8_14["S8"]),
        "s8_fit_full15_bt_rating": bt_rating(pi_15["S8"]),
        "s8_fit_full15_rank": next(r["rank"] for r in rows15
                                  if r["name"] == "S8"),
        "s8_vs_cfinal_direct_h2h": fs_cf["h2h"],
        "s8_champion_anchor_h2h": anchor_h2h,
        "s8_champion_anchor_fold": anchor_fold,
        "band_三档": band,
        "decision": ("S8 已达/超天花板：现计分对 {C_final, S8} 已含天花板，"
                     "不需要换对" if r_anc >= 528 else
                     "S8 接近天花板：换对边际有限，终窗发射决策自裁" if r_anc >= 450 else
                     "S8 过渡带：低于王座但非地板，换对与否自裁" if r_anc >= 400 else
                     "S8 低于王座，换对有必要"),
        "launch": "只测不发（在线提交=硬禁令）；发射决策移交用户",
    }
    BUDGET["total_局次"] = (BUDGET["auth"] + BUDGET["smoke"] + BUDGET["panel"]
                           + BUDGET["det_check"])
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP
    n_cached = len(rows_by_key) - BUDGET["panel"]
    if n_cached > 0:
        BUDGET["panel_rows_cache_reused"] = n_cached
        ANOMALIES.append({
            "kind": "resume_disclosure",
            "note": "断点续跑：主矩阵 %d 局由本 lab evidence/s8_bt_rows.json 行缓存"
                    "复用（首跑 336 局+认证 30+smoke 1+抽查 6=373/800 见首跑账本）；"
                    "本程仅复算折叠/BT/复抽 %d 局，账本如实分列" % (
                        n_cached, BUDGET["total_局次"])})
    ANOMALIES.append({
        "kind": "corpus_note",
        "note": "S8 旧小面板读数（2026-09-30-s8-spike.json）块=674000+i*159，"
                "本矩阵块=674000+i*141（与 C_final crown_base 同块）；"
                "两批数字不同块不可直接对减，BT 以本矩阵 fold 格为准"})
    ANOMALIES.append({
        "kind": "bt_scale_note",
        "note": "champion-tourney 527.8 与 crown-final 重排 439.6/324.3 分属"
                "不同拟合成分（13 件 vs 14 件）；判读以 anchored（冻结 527.8 "
                "标度）为主口径，fit_s8_14/fits_full15 为同协议/全合并交叉口径"})
    ANOMALIES.append(
        "harness 噪声不修不管；胜率=硬通货，margin/终局钱只作参考；"
        "非传递性备忘：对冠军锚镜像专优≠全场更强")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s8_bt_ledger.json").write_text(json.dumps(
        {"budget": BUDGET,
         "pairs_h2h": {k: {"h2h": v["h2h"], "W": v["wins"], "L": v["losses"],
                           "T": v["ties"], "n_folds": v["n"],
                           "mean_margin": v["mean_margin"]}
                       for k, v in EV["pairs"].items()},
         "bt": {"s8_anchored": r_anc,
                "s8_fit_s8_14": bt_rating(pi_s8_14["S8"]),
                "s8_fit_full15": bt_rating(pi_15["S8"]),
                "s8_rank_full15": next(r["rank"] for r in rows15
                                       if r["name"] == "S8")},
         "verdict": EV["verdict"]}, ensure_ascii=False, indent=1,
        default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str), flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
