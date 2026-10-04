# -*- coding: utf-8 -*-
"""judge_expx：MODELPX 预测核精确化判决（引擎公式最优执行；判决先行·不发射
不提交）。

责任口径（任务 expx-model）：
- 机制=oc_c3 基座 MODELPX 的 p_next 计算内层替换（4 处同文）：启发式一步
  预报→K=12 拍引擎公式价格轨迹峰值投影（price(inv) 形状函数全表+城镇排水表
  +R28 删失口径对手流估计）；最优出货点=轨迹局部峰值拍（门沿基座
  p_next<p_cur-0.5）；边际收益=0 定单量（吸收曲线算自家出货边际冲击），
  预卖帽沿基线 3/6/10/10。MILK/WOOL/STRAWBERRY（CARROT 可选未启用）。
- 判决：expx vs oc_c3 配对（26 败局前 8 fold + 新中性 672000+i*117×8，
  n=16 双席=32 (seed,seat) 单元/臂；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转）。
- 判据（预登记）：净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（配对 Δratio_fill
  MILK/WOOL/STRAWBERRY 三品∧全品均值≥0）∧ d14-27 窗收入差转正（fill 口径
  总窗配对 Δ>0，step 336-672）；附分品实现价（vs base）对照（膝点表口径）。
- 足迹审计门（轨道 2 范式）：expx 影子基线决策台账 vs oc_c3 同 (seed,seat)
  动作流逐拍对比——非触发拍（决策一致拍）零足迹；首差异拍=首个决策差异拍；
  决策差异拍全落 MODELPX 窗 [144,695]。
- 读数：终局钱 farms[obs.player].money 干净口径；实现价=Σ(filled×成交价)/
  Σ(filled×base)（影子引擎逐拍归因）。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤350 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-expx-model.json；账本落
orderbook_expx_lab/evidence/。复用（不改写）：judge_milkwin 读数/影子引擎/
配对聚合、judge_r23.DEFAULT_OPPONENTS、sim_bridge.run_games/sim_bridge。
只写 orderbook_expx_lab/ 与 fn_docs/hybrid/results/2026-09-29-expx-model.json。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
for _p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_milkwin_lab"),
           str(MODULE_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_milkwin as jm  # noqa: E402

RECORD_VERSION = "expx-model/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24

LOSS_FOLDS = list(jm.REPLAY_26[:8])                 # 26 败局 canonical 前 8 fold
NEUTRAL_FOLDS = [672000 + i * 117 for i in range(8)]  # 任务给定新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS                  # n=16 双席 fold/变体

# d14-27 窗（任务口径）→ 影子引擎窗口径热替换
WINDOW = (336, 672)
WIN_DAYS = tuple(range(WINDOW[0] // DAY, WINDOW[1] // DAY))  # 14..27
jm.WINDOW = WINDOW
jm.WIN_DAYS = WIN_DAYS

MX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
BASE_PX = jm.BASE_PX

OC_C3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
                 / "main.py")
OC_C3_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d"
                      "39ba9bd23d")
EXPX_MAIN = str(MODULE_DIR / "build" / "expx" / "main.py")
ARMS = {"oc_c3": OC_C3_MAIN, "expx": EXPX_MAIN}
RUN_FORMS = ("oc_c3", "expx")
MODELPX_WINDOW = (144, 695)        # MODELPX 活动拍窗（足迹卫生台账口径）

WORKERS = 2
BUDGET_CAP_GAMES = 350
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-expx-model.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "expx_ab_ledger.json"

EV: Dict[str, Any] = {}
ANOMALIES: List[str] = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------ 装载/追踪 --
def _load_agent_x(path):
    """单文件件装载（末 callable 语义）+ _EXPX_REPORT 台账。"""
    p = os.path.abspath(str(path))
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns: Dict[str, Any] = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError("%s 装载后无 callable" % p)
    reports = {k: ns[k] for k in ("_EXPX_REPORT",)
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


def _build_agents_x(spec):
    out = []
    sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        inner, reports = _load_agent_x(a["path"])
        out.append(jm._Tracer(inner, seat, sinks[seat], reports))
    return out, sinks


def expx_reads(sink) -> Dict[str, Any]:
    """expx 台账末拍累计（step0 复位→末拍=局总量）。"""
    last = None
    for entry in (sink or []):
        tel = entry[3] if len(entry) > 3 else None
        if isinstance(tel, dict) and isinstance(tel.get("_EXPX_REPORT"), dict):
            last = tel["_EXPX_REPORT"]
    return dict(last) if isinstance(last, dict) else {"present": False}


# ------------------------------------------------------------ 局跑口 --
def _run_chunk(payload):
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = _build_agents_x(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "items": None, "shadow": None,
               "window": None, "expx": None, "stream_sha_our": None,
               "stream": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our, opp = sinks[row["seat"]], sinks[1 - row["seat"]]
            row["reads"] = jm.end_reads(our)
            row["items"] = jm.item_reads(our)
            row["expx"] = expx_reads(our)
            row["stream_sha_our"] = jm._stream_digest(our)
            row["stream"] = [e[2] for e in (our or [])]
            sw = jm.shadow_window(sinks, int(spec["seed"]))
            row["shadow"] = sw
            if isinstance(sw, dict) and "window_fill_by_seat" in sw:
                row["window"] = {
                    "fill": sw["window_fill_by_seat"].get(row["seat"]) or {},
                    "submit": sw["window_submit_by_seat"].get(row["seat"])
                    or {}}
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    chunks = [c for c in chunks if c]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    engines = []
    for part in parts:
        rows.extend(part["rows"])
        engines.append({"engine": part.get("engine"),
                        "fallback_reason": part.get("fallback_reason")})
    return rows, engines


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_672000_i117")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum})
    return units, opp_paths


def make_specs(arm, cand_path, units):
    specs = []
    for r in units:
        agents = [{"type": "python", "path": cand_path},
                  {"type": "python", "path": r["opp_path"]}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "expx-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


# ------------------------------------------------------------ 足迹审计 --
def footprint_audit(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """轨道 2 范式：expx vs oc_c3 同 (seed,seat) 逐拍动作流对比 + 影子基线
    决策台账（非触发拍零足迹；首差异拍=首个决策差异拍；级联差异允许）。"""
    cells = []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        if not rc or not rv or rc.get("stream") is None or rv.get("stream") is None:
            continue
        sc, sv = rc["stream"], rv["stream"]
        diffs = []
        for i in range(min(len(sc), len(sv))):
            if json.dumps(sc[i], default=str, sort_keys=True) != \
                    json.dumps(sv[i], default=str, sort_keys=True):
                diffs.append(i)
        first_diff = diffs[0] if diffs else None
        targets = sorted(int(s) for s in
                         ((rv.get("expx") or {}).get("decision_diff_steps")
                          or []))
        target_first = targets[0] if targets else None
        hygiene_ok = all(MODELPX_WINDOW[0] <= s <= MODELPX_WINDOW[1]
                         for s in targets)
        if targets:
            consistent = (first_diff == target_first)
            non_target_zero = bool(first_diff is not None
                                   and first_diff >= target_first)
        else:
            consistent = (first_diff is None)
            non_target_zero = (len(diffs) == 0)
        cells.append({
            "seed": u["seed"], "seat": u["seat"], "stratum": u.get("stratum"),
            "n_ticks": min(len(sc), len(sv)),
            "n_stream_diff": len(diffs),
            "first_diff_step": first_diff,
            "decision_diff_steps": targets[:20],
            "n_decision_diff_steps": len(targets),
            "first_decision_diff_step": target_first,
            "non_target_zero_footprint": bool(non_target_zero),
            "first_diff_matches_first_decision_diff": bool(consistent),
            "decision_steps_in_modelpx_window": bool(hygiene_ok),
            "stream_sha_expx": rv.get("stream_sha_our"),
            "stream_sha_oc_c3": rc.get("stream_sha_our"),
            "passed": bool(non_target_zero and consistent and hygiene_ok),
        })
    n_pass = sum(1 for c in cells if c["passed"])
    return {
        "design": "同 (seed,seat) 双臂新跑我席逐拍动作流对比 + expx 影子基线"
                  "决策台账（build 时同 rival_avg/planned/粗 draw/基座量帽并行"
                  "算基座决策）",
        "rule": "非触发拍零足迹（决策一致拍动作流逐字节同）；首差异拍=首个"
                "决策差异拍（级联差异允许落其后）；决策差异拍全落 MODELPX 窗"
                "[144,695]",
        "n_cells": len(cells), "n_passed": n_pass,
        "gate_passed": bool(cells and n_pass == len(cells)),
        "cells_lite": [{k: c[k] for k in
                        ("seed", "seat", "n_stream_diff", "first_diff_step",
                         "first_decision_diff_step", "n_decision_diff_steps",
                         "passed")}
                       for c in cells],
    }


# ------------------------------------------------------------ 分品对照 --
def realized_paired3(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """实现价配对 Δ（expx−oc_c3；fill 口径 ratio）：全品 + 三品逐品。"""
    out: Dict[str, Any] = {}
    for tag, item in (("all", None), ("MILK", "MILK"), ("WOOL", "WOOL"),
                      ("STRAWBERRY", "STRAWBERRY")):
        deltas, rows = [], []
        for u in units:
            key = (u["seed"], u["seat"])
            rc, rv = ctl.get(key), var.get(key)
            if not rc or not rv:
                continue
            vc, vv = jm._ratio_row(rc, item), jm._ratio_row(rv, item)
            if vc is None or vv is None:
                continue
            d = float(vv) - float(vc)
            deltas.append(d)
            rows.append({"seed": u["seed"], "seat": u["seat"],
                         "ratio_control": round(vc, 4),
                         "ratio_variant": round(vv, 4), "delta": round(d, 4)})
        out[tag] = {
            "n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 4) if deltas
            else UNKNOWN,
            "median_delta": round(statistics.median(deltas), 4) if deltas
            else UNKNOWN,
            "n_up": sum(1 for d in deltas if d > 0),
            "nonneg": bool(deltas and (sum(deltas) / len(deltas)) >= 0),
            "rows_lite": rows[:8]}
    out["nonneg_all_three"] = bool(
        out["all"]["nonneg"] and out["MILK"]["nonneg"] and out["WOOL"]["nonneg"]
        and out["STRAWBERRY"]["nonneg"])
    return out


def per_item_table(realized: Dict[str, Any]) -> Dict[str, Any]:
    """膝点表口径：分品实现价（fill/submit ratio + 成交量）expx vs oc_c3。"""
    arms = {a: (realized.get(a) or {}).get("per_item") or {}
            for a in RUN_FORMS}
    k_ctl, k_var = RUN_FORMS[0], RUN_FORMS[1]
    items = sorted(set(arms[k_ctl]) | set(arms[k_var]))
    out = {}
    for it in items:
        b = arms[k_ctl].get(it) or {}
        x = arms[k_var].get(it) or {}
        row = {"base_px": BASE_PX.get(it),
               k_ctl: {"ratio_fill": b.get("ratio_fill"),
                       "ratio_submit": b.get("ratio_submit"),
                       "filled_qty": b.get("filled_qty")},
               k_var: {"ratio_fill": x.get("ratio_fill"),
                       "ratio_submit": x.get("ratio_submit"),
                       "filled_qty": x.get("filled_qty")}}
        try:
            row["d_ratio_fill"] = round(
                float(x.get("ratio_fill")) - float(b.get("ratio_fill")), 4)
        except (TypeError, ValueError):
            row["d_ratio_fill"] = UNKNOWN
        try:
            row["d_ratio_submit"] = round(
                float(x.get("ratio_submit")) - float(b.get("ratio_submit")), 4)
        except (TypeError, ValueError):
            row["d_ratio_submit"] = UNKNOWN
        out[it] = row
    return out


def model_spec() -> Dict[str, Any]:
    return {
        "formula": {
            "price": "price(inv)=max(1, round(base ± amp×shape(|inv−I0|,T)))",
            "I0": 10000, "PRICE_FLOOR": 1,
            "amp": "target×base/shape(func,T,T)",
            "shapes": ["linear", "sqrt", "log", "sq", "hinge(线性 x/T + "
                       "8×max(0,x/T−1)^2)"],
            "params_table": {
                "WHEAT": "base25 T400 below sqrt→0.80 above log→0.20",
                "CARROT": "base35 T450 below hinge→1.00 above sqrt→0.70",
                "TOMATO": "base60 T200 below hinge→0.40 above sqrt→0.60",
                "STRAWBERRY": "base120 T100 below sqrt→0.70 above linear→1.60",
                "MELON": "base250 T300 below log→0.20 above sq→3.60",
                "EGG": "base50 T332 below hinge→0.40 above log→0.20",
                "MILK": "base160 T122 below sqrt→0.60 above linear→1.60",
                "WOOL": "base200 T105 below log→0.20 above sq→3.20",
                "FERTILIZER": "base100 T200 below linear→0.40 above linear→0.40",
            },
            "source": "kaggle-environments kaggriculture.py 源码直读 "
                      "（fn_docs/hybrid/references/2026-09-28-engine-pricing-"
                      "extraction.md，A 级一手）",
        },
        "projection": {
            "items": list(MX_ITEMS), "carrot_optional": "未启用（宿主循环面"
            "不动）",
            "horizon_K": 12,
            "inv_trajectory": "inv_{t+1}=inv_t+rival_flow−town_draw(step+t)；"
                              "报价基准 step+t 拍报价=step+t−1 处理后 inv",
            "town_draw_table": "每 4 步每已解锁店每品 1 件（单品店 YARN/"
            "PET_CAFE ×2）+ 每 24 步中心全品 1 件（除 FERTILIZER）；逐拍由 "
            "observation.town.unlocked_shops 精确计算",
            "rival_estimator": "R28 删失口径：rival_sold=inv'−inv+town_draw"
            "−own_sold(quote>1 可见量)；$1 地板件记下界（censored_lo 台账）；"
            "逐拍滚动跨空窗不断档，尾 4 拍均值",
            "fire_rule": "轨迹局部峰值拍出货：p_next=K 拍轨迹峰值价，门沿基座 "
            "p_next<p_cur−0.5（峰值=未来 K 拍拿不到更好价）",
            "sizing_rule": "边际收益=0 定单量：吸收曲线=排水累计吸收；自家出货"
            "边际冲击=已卖 shift 件对轨迹平移（价>1 才进库存）；逐件 即时报价 "
            "price(inv+shift) > 持有值 max_t price(inv_t+shift) 即卖，≤即停",
            "caps": "预卖帽沿基线（3/6/10/10 档表达式逐字节保留为上限）",
            "replacement_point": "MODELPX 的 p_next 计算（内层改造，4 处同文"
            "替换；门字面量不动）",
            "footprint": "影子基线决策并行计算；非触发拍零足迹（轨道 2 范式）",
            "fallback": "异常回退基线语义（投影/定单量均回退基座公式与量帽）",
            "constraints": ["零跨拍挪量（R23/R26 红线）", "磁带 blob 零触碰",
                            "守恒：只挂卖自己投射仓存量（宿主守卫沿用）"],
        },
    }


# ------------------------------------------------------------ main --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    man = json.loads((MODULE_DIR / "build" / "expx" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    expx_sha = hashlib.sha256(Path(EXPX_MAIN).read_bytes()).hexdigest()
    if expx_sha != man.get("main_sha256"):
        raise RuntimeError("expx main sha 漂移")

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES, "smoke_局次": 1, "auth_局次": 0,
              "judgment_局次": 0}

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("MODELPX 预测核精确化实验（expx-model；内层合法形态·"
                       "判决先行不发射）：窗内变现差根因=对手 MODELPX 预测更"
                       "准——把启发式 p_next 预测换成引擎公式精确模型最优执行"
                       "（K=12 拍价格投影+峰值拍出货+边际收益定单量）"),
        "model": model_spec(),
        "source": {
            "commands": ["python3 orderbook_expx_lab/build_expx.py",
                         "python3 orderbook_expx_lab/judge_expx.py"],
            "base_main": OC_C3_MAIN, "base_sha256": base_sha,
            "expx_main": EXPX_MAIN, "expx_sha256": expx_sha,
            "build_manifest": {k: man.get(k) for k in
                               ("subs_roundtrip_identity_ok",
                                "gate_literal_untouched", "horizon_k",
                                "entry_last_callable", "host_entry",
                                "replacements")},
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*117（任务给定新中性块 n=8）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局回放（canonical 前 8 fold）+ 新中性块"
                                 " 672000+i*117（i=0..7）；双席 fold n=16/臂"
                                 "=32 (seed,seat) 单元/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": {
                "unit": "配对单元=(seed,seat)；每臂 16 fold×双席=32 局",
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-27 窗 step 336-672 逐日=step//24（14..27）；"
                          "fill 口径=影子引擎逐拍归因 Σ(filled×成交价)；"
                          "submit 口径=挂单 qty×卖时市价",
                "realized_px": "Σ(filled×成交价)/Σ(filled×base)（影子引擎，"
                               "膝点表口径）",
            },
            "criterion": ("净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（配对 "
                          "Δratio_fill 三品∧全品均值≥0）∧ d14-27 窗收入差转正"
                          "（fill 口径总窗配对 Δ>0，对照 oc_c3）"),
        },
        "pairs": {},
        "window_stats": {},
        "per_item_realized": {},
        "per_item_table": {},
        "realized_px_paired": {},
        "terminal_money": {},
        "gates_footprint": {},
        "criteria": {},
        "verdict": {},
        "budget": budget,
    })
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(jm.REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                        2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 管线冒烟 1 局（非 fold 语料，不入配对） ----
    smoke_units = [{"seed": 2026092999, "seat": 0,
                    "opp_path": opp_paths[0], "opponent": "r37",
                    "stratum": "smoke"}]
    smoke_rows, _e0 = _play(make_specs("smoke", ARMS["expx"], smoke_units),
                            run_cfg)
    print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
          "expx:", {k: (smoke_rows[0].get("expx") or {}).get(k)
                    for k in ("fires", "units", "errors")},
          flush=True)
    if smoke_rows[0].get("error"):
        ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
    flush_evid()

    # ---- 3) 双臂实跑（oc_c3 对照 + expx） ----
    rows_by_arm: Dict[str, List[Dict[str, Any]]] = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget["judgment_局次"] += len(rows)
        EV["per_item_realized"][arm] = jm.realized_agg(rows)
        EV["terminal_money"][arm] = jm.end_agg(rows)
        EV["window_stats"][arm] = jm.window_agg(rows)
        EV["window_stats"][arm]["window"] = "d14-27（step 336-672）"
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d" % (arm, n_err, len(rows)))
        mism = EV["per_item_realized"][arm]["aggregate"].get(
            "shadow_mismatch_steps")
        if mism:
            ANOMALIES.append("%s 影子引擎不一致步 %s（窗收入 fill 口径见噪声）"
                             % (arm, mism))
        if arm == "expx":
            te = {"fires": 0, "units": 0, "errors": 0, "censored_lo": 0,
                  "decision_diffs": 0, "mr_limited": 0, "cap_limited": 0}
            for r in rows:
                x = r.get("expx") or {}
                te["fires"] += int(x.get("fires") or 0)
                te["units"] += int(x.get("units") or 0)
                te["errors"] += int(x.get("errors") or 0)
                te["censored_lo"] += int(x.get("censored_lo") or 0)
                te["decision_diffs"] += len(x.get("decision_diff_steps") or [])
                te["mr_limited"] += int(x.get("mr_limited") or 0)
                te["cap_limited"] += int(x.get("cap_limited") or 0)
            EV["expx_telemetry"] = te
        print(arm, "games", len(rows), "err", n_err,
              "tm", EV["terminal_money"][arm]["terminal_money_mean"],
              "win_fill_total", EV["window_stats"][arm]["mean_fill_total"],
              "shadow_mism", mism, round(time.perf_counter() - t2, 1), "s",
              flush=True)
        EV["budget"] = budget
        flush_evid()

    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    var = {(r["seed"], r["seat"]): r for r in rows_by_arm["expx"]}

    # ---- 4) 足迹审计门（轨道 2 范式；非触发拍零足迹） ----
    fp = footprint_audit(ctl, var, units)
    EV["gates_footprint"] = fp
    if not fp["gate_passed"]:
        ANOMALIES.append("足迹审计门未全过：%d/%d 格过"
                         % (fp["n_passed"], fp["n_cells"]))
    print("footprint:", fp["n_passed"], "/", fp["n_cells"], flush=True)
    flush_evid()

    # ---- 5) 配对判决 ----
    ps = jm.pair_stats(ctl, var, units)
    wp = jm.window_paired(ctl, var, units)
    rp = realized_paired3(ctl, var, units)
    EV["pairs"]["expx_vs_oc_c3"] = ps
    EV["window_stats"]["paired_expx_vs_oc_c3"] = wp
    EV["realized_px_paired"]["expx_vs_oc_c3"] = rp
    EV["per_item_table"] = per_item_table(EV["per_item_realized"])
    win_d = wp["fill_total"]["mean_delta"]
    crit = {
        "净翻胜>0": ps["net_flip_wins"] > 0,
        "flips_neg==0": ps["flips_neg"] == 0,
        "实现价非负（Δratio_fill 三品∧全品均值≥0）": rp["nonneg_all_three"],
        "d14-27窗收入差转正（fill 总窗配对 mean Δ>0）": is_num(win_d)
        and float(win_d) > 0,
    }
    EV["criteria"] = {
        "checks": crit,
        "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
        "W_L_T": "%s/%s/%s" % (ps["W"], ps["L"], ps["T"]),
        "mean_delta": ps["mean_delta"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
        "realized_px_nonneg_all_three": rp["nonneg_all_three"],
        "footprint_gate_passed": fp["gate_passed"],
        "positive_arm": all(crit.values())}
    print("expx vs oc_c3:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
          "dM", ps["mean_delta"], "netflip", ps["net_flip_wins"],
          "flips_neg", ps["flips_neg"], "dWin", win_d,
          "px_nonneg", rp["nonneg_all_three"], "crit", crit, flush=True)

    # ---- 6) verdict ----
    budget["total_局次"] = (budget["auth_局次"] + budget["judgment_局次"]
                           + budget["smoke_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES
    ok_all = all(crit.values())
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "criteria_passed": ok_all,
        "footprint_gate_passed": fp["gate_passed"],
        "per_item_ratio_fill_delta": {
            it: (EV["per_item_table"].get(it) or {}).get("d_ratio_fill")
            for it in MX_ITEMS},
        "verdict": ("EXPX_MODEL_POSITIVE: MODELPX 预测核精确化四判据全过"
                    "（足迹审计门%s）"
                    % ("过" if fp["gate_passed"] else "未过（详见 gates_foot"
                       "print）") if ok_all else
                    "NOT_CONFIRMED（详见 criteria）"),
        "form": "expx",
        "note": "判据预登记于任务书（expx-model）：净翻胜>0 ∧ flips_neg==0 ∧"
                " 实现价非负 ∧ d14-27 窗收入差转正；不发射不提交",
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行（件自报 "
                     "telemetry）；kaggle_environments 可选环境加载告警")
    ANOMALIES.append("模型近似备忘：自家 $1 地板件按提交报价>1 分可见/地板"
                     "（同拍内重报价漂移忽略）；未来商店解锁不入投影（用当前 "
                     "unlocked_shops 排水表）；hour-1 双站点同拍重复评估由 "
                     "(step,item) 台账去重")
    ANOMALIES.append("窗口径备忘：d14-27 窗=step 336-672（任务给定），逐日桶="
                     "step//24（14..27 共 14 桶）")
    LEDGER_PATH.write_text(json.dumps(
        {"pairs": {"expx_vs_oc_c3": {k: ps[k] for k in
                                     ("n", "W", "L", "T", "mean_delta",
                                      "net_flip_wins", "flips_neg")}},
         "window": {"fill_total_mean_delta": wp["fill_total"]["mean_delta"],
                    "fill_milk_mean_delta": wp["fill_milk"]["mean_delta"]},
         "per_item_table": EV["per_item_table"],
         "criteria": EV["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
