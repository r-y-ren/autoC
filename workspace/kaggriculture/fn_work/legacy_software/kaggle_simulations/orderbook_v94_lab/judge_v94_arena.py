# -*- coding: utf-8 -*-
"""judge_v94_arena（v94 lab）：haodou V94 紧急池测（判决先行·不发射/不提交）。

对手件零修改直跑（j23._load_entry 全新命名空间+末 callable 语义）；一切适配
只写本 harness 外部层。V94 本体=fn_docs/hybrid/references/ext/haodou_v94/main.py
（SHA 531a423a…，kaggle kernels pull 实抓 2026-09-30）。

面板（每对 n=12 fold 双席=24 局，中性块 674000+i*131）：
  v94 vs {oc_c3 冠军锚, c_final 主件(a37c0d34…), r40, A}
镜像场景（镜像门靶场景=同血脉，n=8 fold 双席=16 局，中性块 674000+i*159）：
  v94 vs haodou V82 本体（bdb82117…） 、v94 vs H1（76b5f842…）
口径：h2h=judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；缺席/红局
→该 seed 记负 fail-closed）；margin=farms[obs.player] 终局钱差（干净口径，
banks 交叉登记）；realized_px=Σ(qty×卖时价)/Σ(qty×base)（提交口径，BASE_PX
milkwin 表）；镜像触发读数=V94 镜像门谓词逐拍复算（同 shape 指纹∧|钱差|≤250，
谓词窗 144≤step<718∧step%24!=23）——只读 obs 复算，不改件。
判决三档：BEATS_CEILING（vs oc_c3 ≥0.5）/ COMPETITIVE（0.35-0.5）/
WEAK（<0.35）/ UNRUNNABLE。
证据 orderbook_v94_lab/evidence/v94_arena.json。只写本 lab。不改既有代码；
不提交；不发射。
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
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
EV_PATH = EVID_DIR / "v94_arena.json"

V94 = REPO / "fn_docs" / "hybrid" / "references" / "ext" / "haodou_v94" \
    / "main.py"
V82 = HERE / "build" / "haodou_v82" / "main.py"
H1 = KSIM_DIR / "orderbook_topform_lab" / "build" / "h1" / "main.py"
OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
CFINAL = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A = KSIM_DIR / "orderbook_r44_a" / "main.py"

PANEL = {"oc_c3": OC3, "c_final": CFINAL, "r40": R40, "A": A}
MIRROR = {"haodou_V82": V82, "H1": H1}
SHA = {
    "v94": "531a423a43184bc5864714189595ec1dbbe3c873de48691b0ebd32fa0a2359bb",
    "haodou_V82": "bdb821178ca73c0e8480f06c1887e20921caea0438398a5edb68bd9ad20b1de8",
    "H1": "76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764974b22f337",
    "oc_c3": "3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39ba9bd23d",
    "c_final": "a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b077016a92",
    "r40": "4ce951f088740e0b",
    "A": "b387307fc12e2610",
}
PANEL_FOLDS = [674000 + i * 131 for i in range(12)]     # 中性块 674000+i*131
MIRROR_FOLDS = [674000 + i * 159 for i in range(8)]     # 中性块 674000+i*159
WORKERS = 2

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    EV_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                  default=str) + "\n", encoding="utf-8")


# ==================================================== 镜像门谓词（复算） ==
def _shape(farm):
    """V94 镜像门 _shape 逐字复刻（只读 obs 诊断；不改件）。"""
    tiles = []
    for y, row in enumerate(farm.get('tiles', [])):
        for x, tile in enumerate(row):
            if isinstance(tile, dict):
                tiles.append((x, y, tile.get('kind'), tile.get('crop'),
                              tile.get('animal')))
    return (tuple(tiles), tuple(farm.get('unlocked_quadrants', [])),
            tuple(farm.get('farmer', [])),
            tuple(tuple(p) for p in farm.get('hands', [])))


def mirror_probe(sink):
    """逐拍复算镜像门触发谓词：谓词窗内 evaluated/true 计数 + 钱差读数。"""
    evaluated = true = 0
    gaps = []
    for step, obs, _act in (sink or []):
        try:
            step = int(step)
        except Exception:
            continue
        if not (144 <= step < 718) or step % 24 == 23:
            continue
        farms = obs.get('farms') or []
        if len(farms) != 2:
            continue
        player = int(obs.get('player', 0))
        mine, other = farms[player], farms[1 - player]
        evaluated += 1
        gap = abs(int(mine.get('money', 0)) - int(other.get('money', 0)))
        if _shape(mine) == _shape(other) and gap <= 250:
            true += 1
            gaps.append(gap)
    return {"evaluated": evaluated, "true": true,
            "trigger_rate": round(true / evaluated, 4) if evaluated else None,
            "true_gap_mean": round(sum(gaps) / len(gaps), 1) if gaps else None}


def realized_px(sink):
    """提交口径实现价：Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表）。"""
    val = 0.0
    base = 0.0
    for _step, obs, act in (sink or []):
        if not isinstance(act, dict):
            continue
        prices = ((obs.get('market') or {}) if isinstance(obs.get('market'),
                  dict) else {}).get('prices') or {}
        for cmd in (act.get('market') or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                item = str(cmd[1])
                px = prices.get(item)
                try:
                    q = float(cmd[2])
                except Exception:
                    continue
                b = float(BASE_PX.get(item, 0) or 0)
                if isinstance(px, (int, float)) and q > 0 and b > 0:
                    val += q * float(px)
                    base += q * b
    return round(val / base, 4) if base > 0 else None


# ============================================================ 跑口 ==
def _chunk(payload):
    """panel/mirror 共用 worker：双席 trace 局跑 run_games；干净口径 margin。"""
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
               "opponent": spec.get("opponent"), "group": spec.get("group"),
               "engine": res.get("engine"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None,
               "rpx_us": None, "rpx_opp": None, "mirror_us": None}
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
                row["rpx_us"] = realized_px(sinks[row["seat"]])
                row["rpx_opp"] = realized_px(sinks[1 - row["seat"]])
                row["mirror_us"] = mirror_probe(sinks[row["seat"]])
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
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(group, opp_name, opp_path, folds):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            specs.append({
                "game_id": "v94|%s|%s|%d-s%d" % (group, opp_name, seed, seat),
                "seed": int(seed), "arm": "v94", "arm_path": str(V94),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "group": group, "kind": "ab",
                "trace": True,
                "agents": [{"type": "python", "path": str(V94)},
                           {"type": "python", "path": str(opp_path)}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows
           if isinstance(r.get("tm_opp"), (int, float))]
    rpx_u = [r["rpx_us"] for r in rows
             if isinstance(r.get("rpx_us"), (int, float))]
    rpx_o = [r["rpx_opp"] for r in rows
             if isinstance(r.get("rpx_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin"] = round(sum(r["margin_clean"] for r in rows
                                 if r["margin_clean"] is not None)
                             / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["realized_px_us"] = round(sum(rpx_u) / len(rpx_u), 4) if rpx_u else None
    f["realized_px_opp"] = round(sum(rpx_o) / len(rpx_o), 4) if rpx_o else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def mirror_agg(rows):
    ev = sum((r.get("mirror_us") or {}).get("evaluated", 0) for r in rows)
    tr = sum((r.get("mirror_us") or {}).get("true", 0) for r in rows)
    gaps = [(r.get("mirror_us") or {}).get("true_gap_mean") for r in rows
            if (r.get("mirror_us") or {}).get("true_gap_mean") is not None]
    return {"n_units": len(rows), "predicate_evaluated_steps": ev,
            "predicate_true_steps": tr,
            "trigger_rate": round(tr / ev, 4) if ev else None,
            "true_gap_mean_of_units": round(sum(gaps) / len(gaps), 1)
            if gaps else None}


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"auth": 0, "panel": 0, "mirror": 0}

    EV.update({
        "version": "v94-arena/1.0",
        "task": "haodou092 harvest-ledger V94（Verified Spatial Mirror Gate，"
                "run 2026-09-30 15:56:57Z）紧急池测判决：值不值得进最后计分对"
                "（判决先行·只测不发·不提交）",
        "piece": {
            "v94_main": str(V94), "v94_sha256": SHA["v94"],
            "source_url": "https://www.kaggle.com/code/haodou092/"
                          "kaggriculture-harvest-ledger",
            "fetched": "2026-09-30", "self_reported_version": "V94",
            "diff_vs_v82": {
                "v82_sha256": SHA["haodou_V82"],
                "hunks": [
                    "+Spatial Mirror Gate（_s738_advance 内）：双农场 shape "
                    "指纹（tiles(kind,crop,animal)/unlocked_quadrants/farmer/"
                    "hands）全同 ∧ |money 差|≤250 → look 4→7（七拍提前卖窗），"
                    "否则 _S738_LOOK=4 保守视界",
                    "−PET_CAFE 胡萝卜倾斜（V82 pet_any_demand_agent 壳，"
                    "day10-23 已揭示 PET_CAFE 时 _CA_MARGIN -15→-22）整块删除",
                ],
                "production_policy_retained": True,
                "note": "diff 总输出 37 行=仅此两 hunk；V94=回滚 V82 PET 局部"
                        "实验+复装 V81 镜像门（与 V81 NOTICE 自述吻合）",
            },
            "self_reported_record": "32 屏 24W8L / 24 高带确认 17W1T6L（41.5/56"
                                    " 分）/ 动态双席 32 局 28W4L（自报口径，"
                                    "未迁移验证）",
        },
        "source": {
            "commands": ["python3 orderbook_v94_lab/judge_v94_arena.py"],
            "corpus": {
                "panel_folds": PANEL_FOLDS,
                "panel_spec": "中性块 674000+i*131（i=0..11）；每对 n=12 fold "
                              "双席=24 局",
                "mirror_folds": MIRROR_FOLDS,
                "mirror_spec": "中性块 674000+i*159（i=0..7）；每对 n=8 fold "
                               "双席=16 局（镜像门靶场景=同血脉）",
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/"
                       "余平；缺席/红局→该 seed 记负 fail-closed）",
                "margin": "farms[obs.player] 终局钱差（干净口径；banks 交叉"
                          "登记 margin_banks）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×base)（提交口径；"
                               "BASE_PX=milkwin 表）",
                "mirror_probe": "V94 镜像门谓词逐拍复算（同 shape 指纹∧"
                                "|钱差|≤250；谓词窗 144≤step<718∧step%24!=23）"
                                "——只读 obs，零修改",
                "hard_currency": "胜率=硬通货；margin/realized_px 只作参考",
                "zero_modification": "对手件 j23._load_entry 直跑（全新命名"
                                     "空间+末 callable）；适配仅本 harness 层",
            },
            "panel": {k: {"path": str(v), "sha": SHA.get(k)}
                      for k, v in PANEL.items()},
            "mirror": {k: {"path": str(v), "sha": SHA.get(k)}
                       for k, v in MIRROR.items()},
        },
        "panel": {}, "mirror": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 认证（复用 composite lab 09-30 认证缓存；同机同二进制）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = (KSIM_DIR / "orderbook_composite_lab" / "evidence"
                  / "sim_auth_cache.json")
    auth = None
    if AUTH_CACHE.is_file():
        try:
            auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        except Exception:
            auth = None
    if isinstance(auth, dict) and auth.get("loaded") and \
            auth.get("consistency_ok"):
        EV["source"]["sim_auth"] = {
            "reused_cache": True, "cache_path": str(AUTH_CACHE),
            "loaded": auth.get("loaded"),
            "consistency": auth.get("consistency"),
            "consistency_ok": auth.get("consistency_ok"),
            "engine": auth.get("engine"), "version": auth.get("version"),
            "wall_speedup": auth.get("wall_speedup")}
        budget["auth"] = 30
    else:
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")},
            [674000 + i * 131 for i in range(8)] + [2026093001])
        EV["source"]["sim_auth"] = {k: auth.get(k) for k in
                                    ("loaded", "consistency",
                                     "consistency_ok", "engine", "version",
                                     "wall_speedup")}
        EV["source"]["sim_auth"]["reused_cache"] = False
        budget["auth"] = 30
    if not (auth.get("loaded") and auth.get("consistency_ok")):
        EV["verdict"] = {"aborted": "sim_bridge 未过 30/30 认证",
                         "verdict": "UNRUNNABLE"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS,
               "record_path": str(EVID_DIR / "sim_bridge_degraded.json")}
    flush_evid()

    # ---- 面板：v94 vs {oc_c3, c_final, r40, A} ----
    panel = {}
    for on, opath in PANEL.items():
        rows = play(unit_specs("panel", on, opath, PANEL_FOLDS), run_cfg)
        budget["panel"] += len(rows)
        panel[on] = fold_stats(rows)
        panel[on]["mirror_probe_us"] = mirror_agg(rows)
        print("panel v94 vs", on, "h2h=", panel[on]["h2h"],
              "W/L/T=", panel[on]["wins"], panel[on]["losses"],
              panel[on]["ties"], flush=True)
        flush_evid()
    EV["panel"] = {
        "design": "v94 对 4 件面板：每对 n=12 fold 双席=24 局（中性块 "
                  "674000+i*131）；h2h=judge_r44._fold_arm；margin=farms"
                  "[obs.player]；胜率=硬通货",
        "pairs": panel}

    # ---- 镜像场景：v94 vs V82 / H1 ----
    mirror = {}
    for on, opath in MIRROR.items():
        rows = play(unit_specs("mirror", on, opath, MIRROR_FOLDS), run_cfg)
        budget["mirror"] += len(rows)
        mirror[on] = fold_stats(rows)
        mirror[on]["mirror_probe_us"] = mirror_agg(rows)
        print("mirror v94 vs", on, "h2h=", mirror[on]["h2h"],
              "trigger=", (mirror[on]["mirror_probe_us"] or {}).get(
                  "trigger_rate"), flush=True)
        flush_evid()
    EV["mirror"] = {
        "design": "镜像门靶场景=同血脉：每对 n=8 fold 双席=16 局（中性块 "
                  "674000+i*159）；镜像触发=V94 谓词逐拍复算（零修改）",
        "pairs": mirror}

    # ---- 判决三档 ----
    h_oc = (panel.get("oc_c3") or {}).get("h2h")
    n_err = sum((panel.get(o) or {}).get("n_errors", 0) for o in panel) + \
        sum((mirror.get(o) or {}).get("n_errors", 0) for o in mirror)
    n_tot = sum((panel.get(o) or {}).get("n_games", 0) for o in panel) + \
        sum((mirror.get(o) or {}).get("n_games", 0) for o in mirror)
    if h_oc is None or (n_tot and n_err / n_tot > 0.2):
        verdict = "UNRUNNABLE"
    elif h_oc >= 0.5:
        verdict = "BEATS_CEILING"
    elif h_oc >= 0.35:
        verdict = "COMPETITIVE"
    else:
        verdict = "WEAK"
    EV["verdict"] = {
        "verdict": verdict,
        "rule": "BEATS_CEILING=vs oc_c3 h2h≥0.5 / COMPETITIVE=0.35-0.5 / "
                "WEAK=<0.35 / UNRUNNABLE=装载失败或红局>20%",
        "vs_oc_c3_h2h": h_oc,
        "panel_h2h": {o: (panel.get(o) or {}).get("h2h") for o in PANEL},
        "mirror_h2h": {o: (mirror.get(o) or {}).get("h2h") for o in MIRROR},
        "mirror_trigger_rate": {o: (mirror.get(o) or {}).get(
            "mirror_probe_us", {}).get("trigger_rate") for o in MIRROR},
        "panel_trigger_rate_non_target": {o: (panel.get(o) or {}).get(
            "mirror_probe_us", {}).get("trigger_rate") for o in PANEL},
        "mean_margin_vs_oc_c3": (panel.get("oc_c3") or {}).get("mean_margin"),
        "realized_px_vs_oc_c3": {
            "us": (panel.get("oc_c3") or {}).get("realized_px_us"),
            "opp": (panel.get("oc_c3") or {}).get("realized_px_opp")},
        "n_games": n_tot, "n_errors": n_err,
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = budget["auth"] + budget["panel"] + budget["mirror"]
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货，margin/realized_px/"
                     "触发率只作参考；Never quote the peak")
    ANOMALIES.append("自报≠可迁移（六连败教训）：V94 自报 41.5/56 与动态 28W4L "
                     "不作判决依据，仅登记；判决只认本池实测")
    ANOMALIES.append("镜像读数注意：镜像门为同血脉靶场景特化，对非同血脉面板件"
                     "触发率预期≈0（谓词复算登记验证）")
    flush_evid()
    print("VERDICT:", verdict, "vs_oc_c3 h2h=", h_oc, flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
