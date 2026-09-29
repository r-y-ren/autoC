# -*- coding: utf-8 -*-
"""judge_oppcond_c3：纯增量件 oc_c3（画像器+C3；无 C1 无 C2）分对手面判决。

责任口径（任务 opp-conditional-c3 判决；与前两轮同口径可比）：
- 形态=oc_c3（画像器+C3 条件羊毛错峰；**无 C1 无 C2**），基底=h1_base 字节
  零改动（76b5f842…）；分对手面板 5 面（vs r37/2965/r40/H1 镜像/WFR）×
  8 seeds × 双席 = 80 局/臂（每对 n=16 双席折叠，K2 口径；panel seeds 沿用
  前两轮 PANEL_SEEDS 可比）；h1_base 臂本轮**新跑**（零足迹逐字节比对需要
  双臂动作流）。
- ICE+YARN 世界格：v2 入格实触发世界取 3 个（727279/731413/736872）×
  5 面 × 双席 × 2 形态 = 60 局（C1 剥除后应与 H1 逐字节同=判据④主证）。
- 判读（预登记判据）：① 逐面 Δ≥0（panel 各面 mean Δ≥0）② WFR 面 Δ>0
  ③ 画像准确率 1.0 ④ 逐格零足迹（非 wfr 类格逐格 Δ=0 ∧ 动作流逐字节同；
  ICE+YARN 世界格全部零足迹）。
- 口径：margin=farms[our].money−farms[opp].money（run_games banks）；终局钱
  =farms[obs.player].money（judge_strongest.clean_reads）；Δ=margin_oc_c3−
  margin_base 同 face 同 seed 同席配对；引擎=sim_bridge 先认证 30/30 后
  auto+bridge；workers=2；判决局次（新跑）≤250（auth 另计）。
用法：python3 judge_oppcond_c3.py     # 全量判决（跑局）
只写 orderbook_oppcond_lab/evidence/ 与
fn_docs/hybrid/results/2026-09-29-opp-conditional-c3.json。不改既有代码。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
T1_DIR = str(KSIM_DIR / "orderbook_track1_lab")
if T1_DIR not in sys.path:
    sys.path.insert(0, T1_DIR)
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import judge_oppcond as J  # noqa: E402

RECORD_VERSION = "opp-conditional-c3/1.0"
BUILD = MODULE_DIR / "build"
EVID = MODULE_DIR / "evidence"
RAW_PATH = EVID / "raw_judgment_c3.json"
LEDGER_V1 = EVID / "raw_judgment.json"           # 前轮账本（只读交叉核对）
LEDGER_V2 = EVID / "raw_judgment_v2.json"        # 前轮账本（只读交叉核对）
FINAL_PATH = (MODULE_DIR.parents[3] / "fn_docs" / "hybrid" / "results"
              / "2026-09-29-opp-conditional-c3.json")

FORMS = {
    "h1_base": str(BUILD / "h1_base" / "main.py"),
    "oc_c3": str(BUILD / "oc_c3" / "main.py"),
}
FORM_CFG = {
    "h1_base": {"c1": False, "c2": False, "c3": False},
    "oc_c3": {"c1": False, "c2": False, "c3": True},
}
FACES = J.FACES
PANEL_SEEDS = J.PANEL_SEEDS
SLICE_SEEDS = (727279, 731413, 736872)   # v2 入格实触发 ICE+YARN 世界
WORKERS = 2
BUDGET_CAP = 250                         # 判决新跑局次（auth 另计）
WFR_CLASS = "wfr"
TRIGGER_KEY = J.TRIGGER_KEY
REVEAL_STEP = 144


# ------------------------------------------------------------ 工具 --
def _mk_spec(kind, form, face, seed, seat):
    agents = ([{"type": "python", "path": FORMS[form]},
               {"type": "python", "path": FACES[face]}] if seat == 0
              else [{"type": "python", "path": FACES[face]},
                    {"type": "python", "path": FORMS[form]}])
    return {"form": form, "face": face, "kind": kind, "spec": {
        "game_id": "%s-%s-%s-%d-%d" % (kind, form, face, seed, seat),
        "seed": int(seed), "kind": kind, "trace": True,
        "our_seat": seat, "agents": agents}}


def _mean(vals):
    return round(sum(vals) / len(vals), 2) if vals else None


def _wtl(deltas):
    return {"wins": sum(1 for d in deltas if d > 0),
            "ties": sum(1 for d in deltas if d == 0),
            "losses": sum(1 for d in deltas if d < 0)}


def _stream_sha(stream):
    try:
        return hashlib.sha256(
            json.dumps(stream, default=str).encode()).hexdigest()[:16]
    except Exception:
        return "err"


# ------------------------------------------------------------ 零足迹 --
def _zero_footprint(rows):
    """逐格零足迹：oc_c3 vs h1_base 同 (face,seed,seat) 格——margin Δ +
    我席逐拍动作 digest 对比（逐字节同口径=动作流 digest 逐拍相等）。"""
    idx = J._index(rows)
    cells = []
    for face in FACES:
        seeds = sorted({r["seed"] for r in rows
                        if r["face"] == face and r["form"] == "oc_c3"})
        for seed in seeds:
            for seat in (0, 1):
                r = idx.get(("oc_c3", face, seed, seat))
                b = idx.get(("h1_base", face, seed, seat))
                if not r or not b or r.get("margin") is None \
                        or b.get("margin") is None or r.get("stream") is None \
                        or b.get("stream") is None:
                    continue
                d = J._stream_diff(r["stream"], b["stream"])
                cells.append({
                    "face": face, "seed": seed, "seat": seat,
                    "cls": r.get("cls"), "trigger": bool(r.get("trigger")),
                    "world_pair": r.get("world_pair"),
                    "margin_oc_c3": r["margin"], "margin_base": b["margin"],
                    "delta": round(r["margin"] - b["margin"], 2),
                    "n_stream_diff": d["n_diff"],
                    "first_diff_step": d["first_diff_step"],
                    "stream_sha_oc_c3": _stream_sha(r["stream"]),
                    "stream_sha_h1_base": _stream_sha(b["stream"]),
                })
    expect_zero = [c for c in cells if c["cls"] != WFR_CLASS]
    ice = [c for c in cells if c["trigger"]]
    ice_zero = [c for c in ice if c["cls"] != WFR_CLASS]
    wfr_cells = [c for c in cells if c["cls"] == WFR_CLASS]

    def _viol(cs):
        return [c for c in cs if c["delta"] != 0 or c["n_stream_diff"] != 0]

    v1, v2 = _viol(expect_zero), _viol(ice_zero)
    return {
        "design": "同 face 同 seed 同席：oc_c3 vs h1_base 双臂新跑，margin Δ"
                  "+ 我席逐拍动作 digest 对比（逐字节同=720 拍 digest 全等）",
        "rule": "C3 仅 wfr 类触发（类门）；非 wfr 类格期望 Δ=0 ∧ 动作流"
                "逐字节同（C1/C2 剥除零足迹）；wfr 类格期望 C3 换表差异"
                "（首差异拍 ≥144=揭示锁存后）",
        "n_cells": len(cells),
        "zero_footprint_cells": {
            "n": len(expect_zero), "n_violations": len(v1),
            "violations": v1[:12],
            "mean_delta": _mean([c["delta"] for c in expect_zero]),
            "n_nonzero_delta": sum(1 for c in expect_zero if c["delta"] != 0),
            "n_stream_diff": sum(1 for c in expect_zero
                                 if c["n_stream_diff"] != 0),
        },
        "ice_yarn_world_cells": {
            "note": "ICE+YARN 世界格（trigger 行级实测）：C1 剥除后应与 H1"
                    "逐字节同（C1 在此格族曾换线 r105，oc_c3 无 C1→零足迹）",
            "n": len(ice_zero), "n_violations": len(v2),
            "violations": v2[:12],
            "mean_delta": _mean([c["delta"] for c in ice_zero]),
            "cells_lite": [{k: c[k] for k in
                            ("face", "seed", "seat", "trigger", "cls",
                             "delta", "n_stream_diff", "first_diff_step")}
                           for c in ice],
        },
        "wfr_class_cells_c3_readout": {
            "n": len(wfr_cells),
            "mean_delta": _mean([c["delta"] for c in wfr_cells]),
            **_wtl([c["delta"] for c in wfr_cells]),
            "all_first_diff_ge_reveal": all(
                (c["first_diff_step"] or 0) >= REVEAL_STEP
                for c in wfr_cells if c["n_stream_diff"] > 0),
            "min_first_diff_step": min(
                [c["first_diff_step"] for c in wfr_cells
                 if c["first_diff_step"] is not None], default=None),
            "cells_lite": [{k: c[k] for k in
                            ("face", "seed", "seat", "cls", "delta",
                             "n_stream_diff", "first_diff_step")}
                           for c in wfr_cells],
        },
        "cells": cells,
    }


# ------------------------------------------------------------ 判据 --
def _criteria_verdict(out):
    per_face = {}
    c1 = True
    for face in FACES:
        d = (out["pairs"][face]["oc_c3"].get("vs_base_paired", {})
             .get("mean_delta"))
        per_face[face] = d
        if d is None or d < 0:
            c1 = False
    wfr_d = per_face.get("wfr")
    c2 = wfr_d is not None and wfr_d > 0
    acc = out["profiler"]["confusion_oc_c3"]["accuracy"]
    c3 = acc == 1.0
    zf = out["zero_footprint"]
    c4 = (zf["zero_footprint_cells"]["n_violations"] == 0
          and zf["ice_yarn_world_cells"]["n_violations"] == 0)
    out["criteria"] = {
        "逐面 Δ≥0（panel 各面 mean Δ≥0，n=16 双席折叠/对）": {
            "passed": bool(c1), "per_face_mean_delta": per_face,
            "threshold": 0},
        "WFR 面 Δ>0（panel wfr 面 mean Δ>0）": {
            "passed": bool(c2), "reading": wfr_d},
        "画像准确率保持 1.0": {
            "passed": bool(c3), "reading": acc,
            "n_rows": out["profiler"]["confusion_oc_c3"]["n"]},
        "逐格零足迹（非 wfr 格 Δ=0∧逐字节同；ICE+YARN 世界格全零足迹）": {
            "passed": bool(c4),
            "zero_footprint_violations":
                zf["zero_footprint_cells"]["n_violations"],
            "n_zero_footprint_cells": zf["zero_footprint_cells"]["n"],
            "ice_yarn_violations": zf["ice_yarn_world_cells"]["n_violations"],
            "n_ice_yarn_cells": zf["ice_yarn_world_cells"]["n"],
            "ice_yarn_mean_delta": zf["ice_yarn_world_cells"]["mean_delta"]},
    }
    ok_all = all(v["passed"] for v in out["criteria"].values())
    out["verdict"] = {
        "verdict": ("OC_C3_PURE_INCREMENT_CONFIRMED: 画像器+C3 条件羊毛错峰"
                    "纯增量件（无 C1 无 C2）四判据全过" if ok_all
                    else "NOT_CONFIRMED（详见 criteria）"),
        "criteria_passed": ok_all,
        "form": "oc_c3",
        "layers": ["profiler", "c3_wool_phase"],
        "note": "判据预登记于任务书（opp-conditional-c3）：逐面 Δ≥0 ∧ WFR 面"
                " Δ>0 ∧ 画像 1.0 ∧ 逐格零足迹（ICE+YARN 世界格 Δ=0，C1 剥除"
                "后与 H1 逐字节同）",
    }
    return out


# ------------------------------------------------------------ 交叉核对 --
def _ledger_crosscheck(panel_rows, slice_rows):
    """前轮账本确定性交叉核对（只读）：h1_base 新跑 vs v1 账本；oc_c3 wfr 面
    vs v2 账本 oc_c1c3（C1/C2 对 wfr 类惰性→同 C3 差量等价）。"""
    out = {"design": "同 (form-equivalent,face,seed,seat) 新跑 margins vs "
                     "前轮账本 margins（确定性件应逐格相等）",
           "rows": [], "n_match": 0, "n_mismatch": 0, "n_missing": 0}
    led = {}
    try:
        v1 = json.loads(LEDGER_V1.read_text(encoding="utf-8"))
        for r in v1.get("panel", []):
            if r.get("form") == "h1_base" and r.get("margin") is not None:
                led[("h1_base", r["face"], r["seed"], r["seat"])] = r["margin"]
    except Exception:
        pass
    try:
        v2 = json.loads(LEDGER_V2.read_text(encoding="utf-8"))
        for r in v2.get("panel", []):
            if r.get("form") == "oc_c1c3" and r["face"] == "wfr" \
                    and r.get("margin") is not None:
                led[("oc_c3~oc_c1c3", r["face"], r["seed"], r["seat"])] = \
                    r["margin"]
    except Exception:
        pass
    for r in panel_rows:
        want = ("h1_base" if r["form"] == "h1_base"
                else "oc_c3~oc_c1c3" if r["face"] == "wfr" else None)
        if want is None or r.get("margin") is None:
            continue
        b = led.get((want, r["face"], r["seed"], r["seat"]))
        if b is None:
            out["n_missing"] += 1
            continue
        match = abs(float(r["margin"]) - float(b)) < 1e-9
        out["n_match" if match else "n_mismatch"] += 1
        if not match or len(out["rows"]) < 12:
            out["rows"].append({
                "form": r["form"], "face": r["face"], "seed": r["seed"],
                "seat": r["seat"], "margin_new": r["margin"],
                "margin_ledger": b, "ledger_form": want, "match": match})
    return out


# ------------------------------------------------------------ 全量跑局 --
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    budget = {"cap_局次": BUDGET_CAP, "auth_games_separate": 60,
              "panel_games": 0, "slice_games": 0, "judgment_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": [
                "python3 orderbook_oppcond_lab/build_oppcond_c3.py",
                "python3 orderbook_oppcond_lab/judge_oppcond_c3.py"],
            "base_main": FORMS["h1_base"],
            "base_main_sha256": hashlib.sha256(
                Path(FORMS["h1_base"]).read_bytes()).hexdigest(),
            "forms": FORMS, "form_cfg": FORM_CFG, "faces": FACES,
            "panel_seeds": PANEL_SEEDS,
            "slice_seeds": list(SLICE_SEEDS),
            "panel_corpus": "26 败局分层抽 4（REPLAY_26[:4]）+ 新中性块 "
                            "672000+i*59 抽 4（i=0..3）——同前两轮 panel seeds",
            "workers": WORKERS,
            "caliber": {
                "unit": "配对单元=(seed,seat)（K2 口径）；每对 n=16 双席折叠"
                        "=8 seeds × 2 席=16 局/臂/对",
                "margin": "farms[our].money−farms[opp].money（run_games banks "
                          "干净口径）",
                "terminal_money": "farms[obs.player].money（judge_strongest."
                                  "clean_reads 干净口径）",
                "delta": "margin_oc_c3−margin_base 同 face 同 seed 同席配对",
                "zero_footprint": "非 wfr 类格逐格 Δ=0 ∧ 我席逐拍动作 digest "
                                  "逐字节同；ICE+YARN 世界格全零足迹",
            },
        },
    }

    # ---- 0. 门禁读入（gates_c3 四门） ----
    gates_path = EVID / "gates_c3.json"
    gates = json.loads(gates_path.read_text(encoding="utf-8")) \
        if gates_path.is_file() else {"overall_passed": False,
                                      "error": "gates_c3.json 缺失"}
    out["gates"] = gates
    out["builds"] = {}
    for form in FORMS:
        mp = BUILD / form / "build_manifest.json"
        if mp.is_file():
            m = json.loads(mp.read_text(encoding="utf-8"))
            out["builds"][form] = {
                "main_sha256": m.get("main_sha256"),
                "main_bytes": m.get("main_bytes"),
                "tar_sha256": m.get("tar_sha256"),
                "layers": m.get("layers"),
                "cfg": m.get("cfg"),
                "byte_identical_to_H1_base": m.get("byte_identical_to_H1"),
                "probes_ok": True,
            }
    if not gates.get("overall_passed"):
        out["aborted"] = "四门未全过，判决中止"
        _write(out)
        return out

    # ---- 1. sim_bridge 对照认证 30/30（先认证） ----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_corpus = J.REPLAY_26 + [2026092901, 2026092902, 2026092903, 2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID / "sim_auth_record_c3.json")}, auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    (EVID / "sim_auth_c3.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    out["source"]["sim_auth"] = auth_lite
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["budget"] = budget
        _write(out)
        return out

    run_cfg = {"engine": "auto", "bridge": auth}

    # ---- 2. 面板（双臂新跑：oc_c3 + h1_base，5 面 × 8 seeds × 双席） ----
    panel_specs = [_mk_spec("panel", form, face, seed, seat)
                   for form in FORMS for face in FACES
                   for seed in PANEL_SEEDS for seat in (0, 1)]
    budget["panel_games"] = len(panel_specs)
    print("panel games:", len(panel_specs), flush=True)
    t1 = time.perf_counter()
    panel_rows, _eng = J._play(panel_specs, run_cfg)
    panel_rows.sort(key=lambda r: (r["face"], r["form"], r["seed"], r["seat"]))
    print("panel done", round(time.perf_counter() - t1, 1), "s", flush=True)

    # ---- 3. ICE+YARN 世界格切片（3 世界 × 5 面 × 双席 × 2 形态） ----
    slice_specs = [_mk_spec("slice", form, face, seed, seat)
                   for form in FORMS for face in FACES
                   for seed in SLICE_SEEDS for seat in (0, 1)]
    budget["slice_games"] = len(slice_specs)
    budget["judgment_games"] = budget["panel_games"] + budget["slice_games"]
    print("slice games:", len(slice_specs), "budget:",
          budget["judgment_games"], flush=True)
    if budget["judgment_games"] > BUDGET_CAP:
        out["aborted"] = "判决局次 %d 超预算 %d" % (budget["judgment_games"],
                                                   BUDGET_CAP)
        out["budget"] = budget
        _write(out)
        return out
    t2 = time.perf_counter()
    slice_rows, _e2 = J._play(slice_specs, run_cfg)
    slice_rows.sort(key=lambda r: (r["face"], r["form"], r["seed"], r["seat"]))
    print("slice done", round(time.perf_counter() - t2, 1), "s", flush=True)

    rows_all = panel_rows + slice_rows

    # ---- 4. 画像混淆矩阵（oc_c3 臂；合并读数另报） ----
    import profiler_core as _pc  # noqa: WPS433
    conf_oc = J._confusion([r for r in rows_all if r["form"] == "oc_c3"])
    conf_all = J._confusion(rows_all)
    out["profiler"] = {
        "calibration": "calib_fingerprints.json（36 局=6 件×3 seeds×双席；"
                       "阈值冻结；probe_expected 7/7）；profiler_core sha "
                       + hashlib.sha256(_pc.CORE_SRC.encode()).hexdigest()[:16],
        "classes": ["r37_2965_family", "h1_mirror", "wfr", "unknown"],
        "confusion_oc_c3": conf_oc,
        "confusion_all_rows": conf_all,
    }

    # ---- 5. 分对手面聚合（panel 主表；slice 参考） ----
    idx_all = J._index(rows_all)
    pairs = {}
    for face in FACES:
        pairs[face] = {form: J._face_agg(panel_rows, form, face, idx_all,
                                         "panel")
                       for form in FORMS}
    out["pairs"] = pairs
    slice_pairs = {}
    for face in FACES:
        slice_pairs[face] = {
            form: J._face_agg(slice_rows, form, face, idx_all, "slice")
            for form in FORMS}
    out["pairs_slice"] = slice_pairs

    pooled_d, pooled_w, pooled_t, pooled_l = [], 0, 0, 0
    for face in FACES:
        pp = pairs[face]["oc_c3"].get("vs_base_paired", {})
        pooled_d.extend(pp.get("deltas") or [])
        pooled_w += pp.get("wins", 0)
        pooled_t += pp.get("ties", 0)
        pooled_l += pp.get("losses", 0)
    n = len(pooled_d)
    out["all_faces_pooled"] = {
        "form": "oc_c3", "kind": "panel", "n_units": n,
        "mean_delta": _mean(pooled_d), "wins": pooled_w,
        "ties": pooled_t, "losses": pooled_l,
        "h2h_vs_base": round((pooled_w + 0.5 * pooled_t) / n, 4)
        if n else None}

    # ---- 6. 逐格零足迹 ----
    out["zero_footprint"] = _zero_footprint(rows_all)

    # ---- 7. 前轮账本交叉核对 ----
    out["ledger_crosscheck"] = _ledger_crosscheck(panel_rows, slice_rows)

    # ---- 8. 判据与 verdict（预登记） ----
    _criteria_verdict(out)

    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
        "harness 噪声：kaggle_environments 可选环境加载告警（open_spiel/cabt）"
        "——无关环境忽略",
        "r37/2965/r40 开局窗逐拍公开信号全同（route0[:144] 动作哈希 b518f3763802）"
        "→ 窗口内系谱级不可分；画像 family 级真值口径",
        "world（unlocked_shops 前二店）实现依赖对手件动作流（weeds RNG）：同 seed "
        "wfr 面可实现不同店对（如 727279：family/h1 格 ICE+YARN、wfr 格 "
        "BRUNCH+PET_CAFE）；ICE+YARN 世界格按 (world×face) 行级实测",
        "panel 世界族无 ICE+YARN 实现（v2 panel trigger 行=0）→ 判据④的 "
        "ICE+YARN 世界格证取自切片 3 世界（v2 入格实触发种子）",
        "C1 换线效应前轮为负（oc_c1c3 触发切片 family 格池化 −860/局）——本轮"
        "剥 C1 后 ICE+YARN 格应零足迹；C3 差量与全套形态同源（443 拍/34 路由）",
        "终局钱口径 farms[obs.player]（judge_strongest.clean_reads；避开 "
        "judge_r26 farms[0] 污染）",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)

    raw = {"panel": J._lite_rows(panel_rows),
           "slice": J._lite_rows(slice_rows)}
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    _write(out)
    print("verdict:", out["verdict"]["verdict"], flush=True)
    print("criteria:", json.dumps(out["criteria"], ensure_ascii=False,
                                  default=str), flush=True)
    print("per-face deltas:", {f: out["criteria"][
        "逐面 Δ≥0（panel 各面 mean Δ≥0，n=16 双席折叠/对）"]
        ["per_face_mean_delta"][f] for f in FACES}, flush=True)
    print("profiler acc:", conf_oc.get("accuracy"), flush=True)
    print("zero footprint:", out["zero_footprint"]["zero_footprint_cells"],
          flush=True)
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


def _write(out):
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
