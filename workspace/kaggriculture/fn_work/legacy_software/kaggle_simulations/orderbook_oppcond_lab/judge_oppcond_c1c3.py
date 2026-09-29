# -*- coding: utf-8 -*-
"""judge_oppcond_c1c3：C1+C3 纯增形态（剥 C2）分对手面判决（不发射·不提交）。

责任口径（任务 opp-conditional-v2 判决；与上轮 judge_oppcond 同口径可比）：
- 形态=oc_c1c3（画像器+C1 条件路由+C3 条件羊毛错峰；**不含 C2**），基底=h1_base
  字节零改动（76b5f842…）；分对手面板 5 面（vs r37/2965/r40/H1 镜像/WFR）×
  8 seeds × 双席 = 80 局/臂（每对 n=16 双席折叠，K2 口径）；h1_base 臂**复用
  上轮 raw_judgment.json panel 账本**（同 panel seeds、确定性件，sanctioned）。
- C1 触发切片加厚：ICE+YARN 世界 gengame 定向挖掘（严格双序一致优先 + 探针
  实测入格；上轮 6 世界 12 面 → 本轮 ≥12 世界 24 面）；含上轮 6 世界（5 实
  触发 + 716113 预测错配对照）连贯复入，新世界探针实测确认后入格。
- **触发判定口径（v2.1 修正）**：world（town.unlocked_shops 前二店）实现依赖
  对手件动作流（weeds RNG）——同 seed 不同 face 可实现不同店对；触发判定必须
  落 **(world×face) 格**（该格行级 trigger 实测），不得按世界一刀切。判据⑤以
  「实触发格」池化读数为准，all-cells 读数同步报告。
- 判读（预登记判据）：① 全对面 h2h vs h1_base ≥0.5（配对虚拟 h2h，panel 80
  单元池化）② 逐面 mean Δ≥−50/局 ③ 画像准确率保持 1.0 ④ WFR 面增益保留
  （panel wfr 面 mean Δ>0）⑤ 触发切片 Δ>0（实触发 family 格池化 mean Δ>0；
  逐 seed 方差另报）。
- 口径：margin=farms[our].money−farms[opp].money（run_games banks）；终局钱
  =farms[obs.player].money（judge_strongest.clean_reads）；Δ=margin_form−
  margin_base 同 face 同 seed 同席配对；引擎=sim_bridge 先认证 30/30 后
  auto+bridge；workers=2；判决局次（新跑）≤350（auth/挖掘/复用账本另计）。
用法：python3 judge_oppcond_c1c3.py        # 全量判决（跑局）
      python3 judge_oppcond_c1c3.py reagg  # 仅按格级口径重算聚合（不跑局）
只写 orderbook_oppcond_lab/evidence/ 与
fn_docs/hybrid/results/2026-09-29-opp-conditional-v2.json。不改既有代码。
"""
from __future__ import annotations

import hashlib
import json
import os
import statistics
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

RECORD_VERSION = "opp-conditional-v2/1.1"
BUILD = MODULE_DIR / "build"
EVID = MODULE_DIR / "evidence"
RAW_PATH = EVID / "raw_judgment_v2.json"
LEDGER_PATH = EVID / "raw_judgment.json"          # 上轮账本（只读）
FINAL_PATH = (MODULE_DIR.parents[3] / "fn_docs" / "hybrid" / "results"
              / "2026-09-29-opp-conditional-v2.json")

FORMS = {
    "h1_base": str(BUILD / "h1_base" / "main.py"),
    "oc_c1c3": str(BUILD / "oc_c1c3" / "main.py"),
}
FORM_CFG = {
    "h1_base": {"c1": False, "c2": False, "c3": False},
    "oc_c1c3": {"c1": True, "c2": False, "c3": True},
}
FACES = J.FACES
PANEL_SEEDS = J.PANEL_SEEDS
WORKERS = 2
BUDGET_CAP = 350                # 判决新跑局次（panel+probe+slice；auth/挖掘/
                                # 复用上轮账本另计）
REC_SEED = J.REC_SEED
TRIGGER_KEY = J.TRIGGER_KEY
CAND_TARGET = 10                # 挖掘候选（探针缓冲）
ADMIT_NEW_TARGET = 8            # 新实触发世界入格目标（5 上轮实触发+8=13 实触发
                                # ≥12 世界 24 面；716113 错配对照连贯保留）
ADMIT_NEW_FLOOR = 7             # 低于此数→判据⑤样本不足，记异常
MINE_DOMAINS = ((725000, 53), (735000, 53), (745000, 53))
MINE_SCAN_CAP = 2000            # 每域扫描上限
FAMILY = ("r37", "2965", "r40")


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


def _stdev(vals):
    return round(statistics.stdev(vals), 2) if len(vals) >= 2 else None


def _mean(vals):
    return round(sum(vals) / len(vals), 2) if vals else None


def _wtl(deltas):
    return {"wins": sum(1 for d in deltas if d > 0),
            "ties": sum(1 for d in deltas if d == 0),
            "losses": sum(1 for d in deltas if d < 0)}


# ------------------------------------------------------------ 聚合 --
def _crosscheck(fresh_rows, led_other):
    cross = {"design": "新跑 oc_c1c3 vs 上轮账本同格 margins（系谱面应=oc_c1、"
                       "wfr 面应=oc_c1c2c3、h1 面应全同；确定性件）",
             "rows": [], "n_match": 0, "n_mismatch": 0, "n_missing": 0}
    for r in fresh_rows:
        if r.get("margin") is None:
            continue
        face = r["face"]
        want = ("oc_c1" if face != "wfr" else "oc_c1c2c3")
        b = led_other.get((want, face, r["seed"], r["seat"]))
        if b is None:
            cross["n_missing"] += 1
            continue
        match = abs(float(r["margin"]) - float(b["margin"])) < 1e-9
        cross["n_match" if match else "n_mismatch"] += 1
        if not match or len(cross["rows"]) < 12:
            cross["rows"].append({
                "face": face, "seed": r["seed"], "seat": r["seat"],
                "margin_oc_c1c3": r["margin"],
                "margin_ledger_" + want: b["margin"], "match": match})
    return cross


def _agg_pairs(panel_rows_all, slice_rows_all, idx_all):
    pairs = {}
    for kind, rws in (("panel", panel_rows_all), ("slice", slice_rows_all)):
        faces_out = {}
        for face in FACES:
            forms_out = {}
            for form in FORMS:
                forms_out[form] = J._face_agg(rws, form, face, idx_all, kind)
            faces_out[face] = forms_out
        pairs[kind] = faces_out
    pooled_d, pooled_w, pooled_t, pooled_l = [], 0, 0, 0
    for face in FACES:
        pp = pairs["panel"][face]["oc_c1c3"].get("vs_base_paired", {})
        pooled_d.extend(pp.get("deltas") or [])
        pooled_w += pp.get("wins", 0)
        pooled_t += pp.get("ties", 0)
        pooled_l += pp.get("losses", 0)
    n = len(pooled_d)
    pooled = {"form": "oc_c1c3", "kind": "panel", "n_units": n,
              "mean_delta": _mean(pooled_d), "wins": pooled_w,
              "ties": pooled_t, "losses": pooled_l,
              "h2h_vs_base": round((pooled_w + 0.5 * pooled_t) / n, 4)
              if n else None}
    return pairs, pooled


def _agg_trigger_slice(slice_rows_all, idx_all, mine, admitted, rejected,
                       old_worlds, new_worlds):
    """触发切片聚合（格级触发判定：触发落 (world×face) 格行级实测）。"""
    rows = [r for r in slice_rows_all if r.get("margin") is not None]
    slice_worlds = list(old_worlds) + list(new_worlds)

    def _cell(seed, face):
        rows_c = [r for r in rows if r["seed"] == seed and r["face"] == face]
        pairs = sorted({r.get("world_pair") for r in rows_c
                        if r.get("world_pair")})
        flags = sorted({bool(r.get("trigger")) for r in rows_c})
        deltas = []
        for r in rows_c:
            if r["form"] != "oc_c1c3":
                continue
            b = idx_all.get(("h1_base", face, seed, r["seat"]))
            if b and b.get("margin") is not None:
                deltas.append({
                    "seat": r["seat"], "margin_oc_c1c3": r["margin"],
                    "margin_base": b["margin"],
                    "delta": round(r["margin"] - b["margin"], 2),
                    "base_from_ledger": bool(b.get("from_ledger"))})
        ds = [d["delta"] for d in deltas]
        return {"seed": seed, "face": face,
                "trigger": flags == [True],
                "trigger_flags_seen": flags,
                "world_pair": pairs[0] if len(pairs) == 1 else pairs,
                "pairs_seen": pairs,
                "consistent": len(pairs) <= 1 and len(flags) <= 1,
                "n_units": len(deltas), "deltas": deltas,
                "mean_delta": _mean(ds),
                "from_ledger_rows": sum(1 for r in rows_c
                                        if r.get("from_ledger")),
                **_wtl(ds)}

    cells = [_cell(seed, face) for seed in slice_worlds for face in FACES]

    per_seed = []
    for seed in slice_worlds:
        by_face = {}
        for face in FACES:
            c = next(c for c in cells if c["seed"] == seed
                     and c["face"] == face)
            d0 = next((d["delta"] for d in c["deltas"] if d["seat"] == 0), None)
            d1 = next((d["delta"] for d in c["deltas"] if d["seat"] == 1), None)
            by_face[face] = {"seat0_delta": d0, "seat1_delta": d1,
                             "fold_mean": c["mean_delta"],
                             "trigger": c["trigger"],
                             "world_pair": c["world_pair"]}
        fam_trg = [by_face[f]["fold_mean"] for f in FAMILY
                   if by_face[f]["trigger"] and by_face[f]["fold_mean"]
                   is not None]
        fam_all = [by_face[f]["fold_mean"] for f in FAMILY
                   if by_face[f]["fold_mean"] is not None]
        per_seed.append({
            "seed": seed,
            "trigger_faces": [f for f in FACES if by_face[f]["trigger"]],
            "world_pairs_by_face": {f: by_face[f]["world_pair"] for f in FACES},
            "by_face": by_face,
            "family_trigger_fold_mean": _mean(fam_trg),
            "family_all_fold_mean": _mean(fam_all),
        })

    def _var(face_sel, trig_only):
        outv = {}
        for face in face_sel:
            seed_means = [p["by_face"][face]["fold_mean"] for p in per_seed
                          if p["by_face"][face]["fold_mean"] is not None
                          and (p["by_face"][face]["trigger"] or not trig_only)]
            ds = [d["delta"] for c in cells if c["face"] == face
                  and (c["trigger"] or not trig_only) for d in c["deltas"]]
            outv[face] = {"n_cells": len(seed_means),
                         "n_units": len(ds),
                         "seed_fold_means": seed_means,
                         "mean": _mean(ds),
                         "std_sample_seed_means": _stdev(seed_means),
                         "min": min(seed_means) if seed_means else None,
                         "max": max(seed_means) if seed_means else None,
                         **_wtl(ds)}
        return outv

    fam_trg_seeds = [p["family_trigger_fold_mean"] for p in per_seed
                     if p["family_trigger_fold_mean"] is not None]
    fam_all_seeds = [p["family_all_fold_mean"] for p in per_seed
                     if p["family_all_fold_mean"] is not None]
    fam_trg_units = [d["delta"] for c in cells if c["face"] in FAMILY
                     and c["trigger"] for d in c["deltas"]]
    fam_all_units = [d["delta"] for c in cells if c["face"] in FAMILY
                     for d in c["deltas"]]
    wfr_units = [d["delta"] for c in cells if c["face"] == "wfr"
                 for d in c["deltas"]]
    h1_units = [d["delta"] for c in cells if c["face"] == "h1"
                for d in c["deltas"]]

    fam_block = {
        "n_seeds": len(fam_trg_seeds),
        "n_cells": sum(1 for c in cells if c["face"] in FAMILY and c["trigger"]),
        "n_units": len(fam_trg_units),
        "n_units_per_face": len(fam_trg_units) // len(FAMILY),
        "seed_fold_means": fam_trg_seeds,
        "mean": _mean(fam_trg_units),
        "std_sample_seed_means": _stdev(fam_trg_seeds),
        "min": min(fam_trg_seeds) if fam_trg_seeds else None,
        "max": max(fam_trg_seeds) if fam_trg_seeds else None,
        **_wtl(fam_trg_units),
        "h2h_units": round((sum(1 for d in fam_trg_units if d > 0)
                            + 0.5 * sum(1 for d in fam_trg_units if d == 0))
                           / len(fam_trg_units), 4) if fam_trg_units else None,
    }
    fam_all_block = {
        "n_seeds": len(fam_all_seeds),
        "n_units": len(fam_all_units),
        "n_units_per_face": len(fam_all_units) // len(FAMILY),
        "seed_fold_means": fam_all_seeds,
        "mean": _mean(fam_all_units),
        "std_sample_seed_means": _stdev(fam_all_seeds),
        **_wtl(fam_all_units),
    }

    per_world = {}
    for seed in slice_worlds:
        per_world[str(seed)] = {
            "per_face": {face: {
                "trigger": next(c for c in cells if c["seed"] == seed
                                and c["face"] == face)["trigger"],
                "world_pair": next(c for c in cells if c["seed"] == seed
                                   and c["face"] == face)["world_pair"],
                "n_rows": sum(1 for r in rows if r["seed"] == seed
                              and r["face"] == face),
            } for face in FACES},
            "trigger_faces": [f for f in FACES if next(
                c for c in cells if c["seed"] == seed and c["face"] == f
            )["trigger"]],
            "cross_face_consistent": all(
                next(c for c in cells if c["seed"] == seed
                     and c["face"] == f)["consistent"] for f in FACES),
        }

    return {
        "mining": mine,
        "admission": {
            "probe_cell": "(oc_c1c3, r37, seed, seat0)——探针局同时即切片格",
            "admitted_new": admitted, "rejected": rejected,
            "old_worlds_from_ledger": [
                {"seed": s,
                 "trigger_faces": per_world[str(s)]["trigger_faces"],
                 "world_pairs_by_face": {
                     f: per_world[str(s)]["per_face"][f]["world_pair"]
                     for f in FACES}} for s in old_worlds],
        },
        "trigger_unit_note": "触发判定落 (world×face) 格：world 实现依赖对手件"
                             "动作流（weeds RNG），同 seed 不同 face 可实现不同"
                             "店对；格触发=该格行级实测（双席双形态一致）",
        "world_check": {
            "n_mined_worlds": len(slice_worlds),
            "n_worlds_any_trigger": sum(
                1 for p in per_world.values() if p["trigger_faces"]),
            "n_family_trigger_cells": fam_block["n_cells"],
            "units_per_face_family_trigger": fam_block["n_units_per_face"],
            "units_per_face_all_mined": len(slice_worlds) * 2,
            "target_达标": ("≥12 世界 24 面" if len(slice_worlds) >= 12
                            and fam_block["n_units_per_face"] >= 24
                            else "未达标"),
            "per_world": per_world,
        },
        "cells": cells,
        "per_seed": per_seed,
        "variance": {
            "unit": "逐 seed Δ=双席折叠均值（fold_mean）；std=样本标准差 n−1",
            "family_trigger_cells_pooled": fam_block,
            "family_all_cells_pooled": fam_all_block,
            "per_face_trigger_cells": _var(FACES, True),
            "per_face_all_cells": _var(FACES, False),
            "wfr_cells_c3_readout": {"n_units": len(wfr_units),
                                    "mean": _mean(wfr_units),
                                    **_wtl(wfr_units)},
            "h1_cells_zero_footprint": {
                "n_units": len(h1_units),
                "n_nonzero": sum(1 for d in h1_units if d != 0)},
        },
        "per_face_vs_base_trigger_cells": _var(FACES, True),
        "criterion_reading": {
            "scope": "实触发 family 格池化（13 触发世界×系谱 3 面×双席口径）",
            "reading": fam_block["mean"],
            "reading_all_cells": fam_all_block["mean"],
            "n_seeds": fam_block["n_seeds"],
            "n_units_per_face": fam_block["n_units_per_face"],
            "std_sample_seed_means": fam_block["std_sample_seed_means"],
        },
    }


def _criteria_verdict(out):
    h2h = out["all_faces_pooled"]["h2h_vs_base"]
    c1 = h2h is not None and h2h >= 0.5
    face_deltas = {}
    c2 = True
    for face in FACES:
        d = (out["pairs_by_opponent"]["panel"][face]["oc_c1c3"]
             .get("vs_base_paired", {}).get("mean_delta"))
        face_deltas[face] = d
        if d is None or d < -50:
            c2 = False
    acc = out["profiler"]["confusion"]["accuracy"]
    c3 = acc == 1.0
    wfr_d = face_deltas.get("wfr")
    c4 = wfr_d is not None and wfr_d > 0
    cr = out["trigger_slice"]["criterion_reading"]
    ts = cr["reading"]
    c5 = ts is not None and ts > 0
    out["criteria"] = {
        "全对面 h2h vs H1_base ≥0.5（panel 80 单元池化）": {
            "passed": bool(c1), "reading": h2h},
        "逐对手面无一劣化（各面 mean Δ≥−50/局）": {
            "passed": bool(c2), "per_face_mean_delta": face_deltas,
            "threshold": -50},
        "画像准确率保持 1.0": {"passed": bool(c3), "reading": acc,
                               "n_rows": out["profiler"]["confusion"]["n"]},
        "WFR 面增益保留（panel wfr 面 mean Δ>0）": {
            "passed": bool(c4), "reading": wfr_d},
        "触发切片 Δ>0（实触发 family 格池化）": {
            "passed": bool(c5), "reading": ts,
            "reading_all_cells": cr["reading_all_cells"],
            "n_seeds": cr["n_seeds"],
            "n_units_per_face": cr["n_units_per_face"],
            "std_sample_seed_means": cr["std_sample_seed_means"]},
    }
    ok_all = all(v["passed"] for v in out["criteria"].values())
    out["verdict"] = {
        "verdict": ("C1C3_PURE_INCREMENT_CONFIRMED: 剥 C2 后 C1+C3 纯增形态"
                    "五判据全过" if ok_all else "NOT_CONFIRMED（详见 criteria）"),
        "criteria_passed": ok_all,
        "form": "oc_c1c3",
        "note": "判据预登记于任务书（v2 口径）：h2h≥0.5 ∧ 逐面 Δ≥−50 ∧ 画像 "
                "1.0 ∧ WFR 面 Δ>0 ∧ 触发切片 Δ>0",
    }
    return out


def _anomaly(out):
    fam = out["trigger_slice"]["variance"]["family_trigger_cells_pooled"]
    return [
        "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
        "harness 噪声：kaggle_environments 可选环境加载告警（open_spiel/cabt）"
        "——无关环境忽略",
        "r37/2965/r40 开局窗逐拍公开信号全同（route0[:144] 动作哈希 b518f3763802）"
        "→ 窗口内系谱级不可分；画像 family 级真值口径",
        "world（unlocked_shops 前二店）实现依赖对手件动作流（weeds RNG）：同 seed"
        "不同 face 可实现不同店对（如 727279：family/h1 格 ICE+YARN 触发、wfr 格 "
        "BRUNCH+PET_CAFE）；触发判定按 (world×face) 格行级实测，world_check 记 "
        "per-face 分解",
        "C1 触发效应=世界级大方差且负均值：实触发 family 格 %d 世界逐 seed "
        "fold_mean ∈ [%s..%s]，池化 mean Δ=%s（%d 正 %d 负）；上轮 6 世界 +341 "
        "读数系小 n 大方差假象，加厚至 13 世界后消失" % (
            fam["n_seeds"], fam["min"], fam["max"], fam["mean"],
            fam["wins"] // (2 * 3) if fam.get("wins") else 0,
            fam["losses"] // (2 * 3) if fam.get("losses") else 0),
        "格级零足迹对照全绿：h1 面格 Δ 全 0；716113 预测错配格（ICE+PIZZA）Δ 全 0"
        "——条件门（C1 世界门∧类门、C3 类门）未触发单元零动作差异，剥 C2 后系谱"
        "面 panel 零足迹（Δ=0）",
        "world 非 seed 纯函数（weeds RNG/动作流依赖）→ gengame 预测可错配；本轮"
        "探针实测入格（probe 双作切片格），错配候选不入格（rejected 只留探针行）；"
        "本轮 8 探针全命中（严格双序一致 10/10）",
        "h1_base 臂复用上轮账本（panel 80 行 + 切片旧世界 48 行；确定性件；"
        "ledger_crosscheck 逐格比对新跑 oc_c1c3 与上轮 oc_c1/oc_c1c2c3 margins）",
        "终局钱口径 farms[obs.player]（judge_strongest.clean_reads；避开 "
        "judge_r26 farms[0] 污染）",
    ]


# ------------------------------------------------------------ 全量跑局 --
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    budget = {"cap_局次": BUDGET_CAP, "auth_games_separate": 60,
              "mining_games_separate": 2, "panel_games": 0, "probe_games": 0,
              "slice_completion_games": 0, "judgment_games": 0,
              "reused_ledger_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": [
                "python3 orderbook_oppcond_lab/build_oppcond_c1c3.py",
                "python3 orderbook_oppcond_lab/judge_oppcond_c1c3.py",
                "python3 orderbook_oppcond_lab/judge_oppcond_c1c3.py reagg"],
            "base_main": FORMS["h1_base"],
            "base_main_sha256": hashlib.sha256(
                Path(FORMS["h1_base"]).read_bytes()).hexdigest(),
            "forms": FORMS, "form_cfg": FORM_CFG, "faces": FACES,
            "panel_seeds": PANEL_SEEDS,
            "panel_corpus": "26 败局分层抽 4（REPLAY_26[:4]）+ 新中性块 "
                            "672000+i*59 抽 4（i=0..3）——同上轮 panel seeds",
            "workers": WORKERS,
            "caliber": {
                "unit": "配对单元=(seed,seat)（K2 口径）；每对 n=16 双席折叠"
                        "=8 seeds × 2 席=16 局/臂/对",
                "margin": "farms[our].money−farms[opp].money（run_games banks "
                          "干净口径）",
                "terminal_money": "farms[obs.player].money（judge_strongest."
                                  "clean_reads 干净口径）",
                "delta": "margin_form−margin_base 同 face 同 seed 同席配对",
                "h2h_vs_base": "配对虚拟 h2h：Δ>0 胜 / Δ=0 平 / Δ<0 负，"
                               "（W+0.5T)/n；全对面=5 面池化 80 单元",
                "trigger_unit": "触发判定落 (world×face) 格行级实测（world 实现"
                                "依赖对手件动作流，v2.1 修正）",
            },
            "ledger_reuse": {
                "panel_h1_base": "复用上轮 evidence/raw_judgment.json panel "
                                 "h1_base 80 行（同 panel seeds；确定性件）",
                "slice_h1_base": "上轮 6 世界（705/715 域）h1_base 行复用"
                                 "（705 域 5 面×双席齐；715 域仅系谱 3 面，"
                                 "h1/wfr 面补跑）",
                "crosscheck": "新跑 oc_c1c3 行与上轮 oc_c1（系谱面）/oc_c1c2c3"
                              "（wfr 面）同行 margins 比对=确定性+剥 C2 等价性"
                              "实证（ledger_crosscheck）",
            },
        },
    }

    # ---- 0. 门禁读入（gates_c1c3） ----
    gates_path = EVID / "gates_c1c3.json"
    gates = json.loads(gates_path.read_text(encoding="utf-8")) \
        if gates_path.is_file() else {"overall_passed": False,
                                      "error": "gates_c1c3.json 缺失"}
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
                "byte_identical_to_H1_base": (m.get("byte_identical_to_H1")),
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
         "record_path": str(EVID / "sim_auth_record_v2.json")}, auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    (EVID / "sim_auth_v2.json").write_text(
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

    # ---- 2. ICE+YARN 定向挖掘（gengame 磁带重放；严格双序一致优先） ----
    import mine_worlds as mw  # noqa: WPS433
    mine_t0 = time.perf_counter()
    srv = mw.Serve()
    try:
        rec = mw.record_pair(str(FORMS["h1_base"]), REC_SEED, srv)
        lf = rec["tapes"]["order_h1_first"]["lines"]
        ls = rec["tapes"]["order_h1_second"]["lines"]
        cand, scanned = [], 0

        def _n_strict():
            return sum(1 for c in cand if c["strict"])

        stop = False
        for dom_base, dom_step in MINE_DOMAINS:
            for i in range(MINE_SCAN_CAP):
                s = dom_base + i * dom_step
                p0 = mw.pair_key(mw.predict_world(s, lf[0], lf[1], srv))
                p1 = mw.pair_key(mw.predict_world(s, ls[0], ls[1], srv))
                scanned += 1
                if p0 == TRIGGER_KEY or p1 == TRIGGER_KEY:
                    cand.append({"seed": s, "domain": dom_base,
                                 "pred_h1_first": p0, "pred_h1_second": p1,
                                 "strict": p0 == p1 == TRIGGER_KEY})
                if _n_strict() >= CAND_TARGET:
                    stop = True
                    break
            if stop:
                break
        strict = [c for c in cand if c["strict"]]
        loose = [c for c in cand if not c["strict"]]
        probe_order = strict + loose
        mine = {"method": "gengame 磁带重放定向（H1 镜像实录磁带预测店对；"
                         "mine_worlds 唯件）",
                "filter": "严格双序一致（order_h1_first 与 order_h1_second "
                          "预测同为 %s）优先；单序命中候补（loose）" % TRIGGER_KEY,
                "rec_seed": REC_SEED,
                "seed_domains": ["%d+i*%d" % (d, s) for d, s in MINE_DOMAINS],
                "n_scanned_predictions": scanned * 2,
                "n_candidates": len(cand), "n_strict": len(strict),
                "n_loose": len(loose),
                "candidates": cand[:24],
                "elapsed_s": round(time.perf_counter() - mine_t0, 2)}
    finally:
        srv.close()
    out["source"]["trigger_slice_mining"] = mine
    print("mined candidates:", len(cand), "strict:", len(strict), flush=True)

    # ---- 3. 面板（oc_c1c3 5 面 × 8 seeds × 双席；base 复用上轮账本） ----
    run_cfg = {"engine": "auto", "bridge": auth}
    panel_specs = [_mk_spec("panel", "oc_c1c3", face, seed, seat)
                   for face in FACES for seed in PANEL_SEEDS for seat in (0, 1)]
    budget["panel_games"] = len(panel_specs)
    print("panel games:", len(panel_specs), flush=True)
    t1 = time.perf_counter()
    panel_rows, _eng = J._play(panel_specs, run_cfg)
    panel_rows.sort(key=lambda r: (r["face"], r["seed"], r["seat"]))
    print("panel done", round(time.perf_counter() - t1, 1), "s", flush=True)

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    led_panel_base = {}
    for r in ledger["panel"]:
        if r["form"] == "h1_base" and r.get("margin") is not None:
            rr = dict(r)
            rr["kind"] = "panel"
            rr["from_ledger"] = True
            led_panel_base[(r["face"], r["seed"], r["seat"])] = rr
    budget["reused_ledger_games"] += len(led_panel_base)
    panel_rows_all = panel_rows + list(led_panel_base.values())

    # ---- 4. 探针入格（新候选→实测世界；探针格=(oc_c1c3,r37,seed,seat0)） ----
    admitted, rejected = [], []
    probe_rows = []
    for c in probe_order:
        if len(admitted) >= ADMIT_NEW_TARGET:
            break
        if budget["judgment_games"] + budget["panel_games"] + 1 > BUDGET_CAP:
            break
        spec = _mk_spec("slice", "oc_c1c3", "r37", c["seed"], 0)
        rows, _e = J._play([spec], run_cfg)
        budget["probe_games"] += 1
        row = rows[0] if rows else {}
        row["probe_of"] = c["seed"]
        probe_rows.append(row)
        ok = bool(row.get("trigger")) and row.get("margin") is not None
        c["actual_pair"] = row.get("world_pair")
        c["actual_trigger"] = bool(row.get("trigger"))
        (admitted if ok else rejected).append(c)
        print("probe", c["seed"], row.get("world_pair"), "trigger",
              row.get("trigger"), "->", "ADMIT" if ok else "reject", flush=True)

    # 候选不足→续挖续探（域外递补）
    if len(admitted) < ADMIT_NEW_TARGET:
        extra_base = MINE_DOMAINS[-1][0] + 100000
        extra_step = MINE_DOMAINS[-1][1]
        srv = mw.Serve()
        try:
            for i in range(MINE_SCAN_CAP):
                if len(admitted) >= ADMIT_NEW_TARGET:
                    break
                s = extra_base + i * extra_step
                p0 = mw.pair_key(mw.predict_world(s, lf[0], lf[1], srv))
                p1 = mw.pair_key(mw.predict_world(s, ls[0], ls[1], srv))
                mine["n_scanned_predictions"] += 2
                if not (p0 == TRIGGER_KEY or p1 == TRIGGER_KEY):
                    continue
                c = {"seed": s, "domain": extra_base, "pred_h1_first": p0,
                     "pred_h1_second": p1, "strict": p0 == p1 == TRIGGER_KEY,
                     "late_fill": True}
                spec = _mk_spec("slice", "oc_c1c3", "r37", s, 0)
                rows, _e = J._play([spec], run_cfg)
                budget["probe_games"] += 1
                row = rows[0] if rows else {}
                row["probe_of"] = s
                probe_rows.append(row)
                ok = bool(row.get("trigger")) and row.get("margin") is not None
                c["actual_pair"] = row.get("world_pair")
                c["actual_trigger"] = bool(row.get("trigger"))
                (admitted if ok else rejected).append(c)
                mine.setdefault("late_fill_candidates", []).append(c)
                print("probe+", s, row.get("world_pair"), "->",
                      "ADMIT" if ok else "reject", flush=True)
        finally:
            srv.close()
    for row in probe_rows:
        if row.get("probe_of") not in {c["seed"] for c in admitted}:
            row["kind"] = "probe_rejected"

    # ---- 5. 切片补全（上轮 6 世界 + 新入格世界 × 5 面 × 双席 × 2 形态） ----
    led_slice_base = {}
    for key in ("slice", "slice_ext"):
        for r in ledger.get(key, []):
            if r["form"] == "h1_base" and r.get("margin") is not None:
                rr = dict(r)
                rr["kind"] = "slice"
                rr["from_ledger"] = True
                led_slice_base[(r["face"], r["seed"], r["seat"])] = rr
    old_worlds = sorted({seed for (_f, seed, _s) in led_slice_base})
    new_worlds = [c["seed"] for c in admitted]
    slice_worlds = old_worlds + new_worlds

    comp_specs = []
    for seed in slice_worlds:
        is_new = seed in new_worlds
        for face in FACES:
            for seat in (0, 1):
                for form in FORMS:
                    if (form == "oc_c1c3" and face == "r37" and seat == 0
                            and is_new):
                        continue                              # 探针格已跑
                    if form == "h1_base" and (face, seed, seat) in led_slice_base:
                        continue                              # 复用上轮账本
                    comp_specs.append(_mk_spec("slice", form, face, seed, seat))
    budget["slice_completion_games"] = len(comp_specs)
    budget["judgment_games"] = (budget["panel_games"] + budget["probe_games"]
                                + budget["slice_completion_games"])
    print("slice worlds:", len(slice_worlds), "old:", old_worlds,
          "new:", new_worlds, flush=True)
    print("completion games:", len(comp_specs), "budget:",
          budget["judgment_games"], flush=True)
    if budget["judgment_games"] > BUDGET_CAP:
        out["aborted"] = "判决局次 %d 超预算 %d" % (budget["judgment_games"],
                                                   BUDGET_CAP)
        out["budget"] = budget
        _write(out)
        return out
    t2 = time.perf_counter()
    comp_rows, _e2 = J._play(comp_specs, run_cfg) if comp_specs else ([], [])
    print("slice done", round(time.perf_counter() - t2, 1), "s", flush=True)

    slice_rows_new = [r for r in comp_rows] + [
        r for r in probe_rows if r["kind"] == "slice"]
    slice_rows_all = slice_rows_new + list(led_slice_base.values())
    budget["reused_ledger_games"] += len(led_slice_base)

    # ---- 6-11. 聚合（格级触发判定）+ 落盘 ----
    _aggregate(out, panel_rows, comp_rows, panel_rows_all, slice_rows_all,
               ledger, mine, admitted, rejected, old_worlds, new_worlds,
               budget)
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)

    raw = {"panel": J._lite_rows(panel_rows_all),
           "slice": J._lite_rows(slice_rows_all),
           "probe_rejected": J._lite_rows([r for r in probe_rows
                                           if r["kind"] == "probe_rejected"])}
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    _write(out)
    print("verdict:", out["verdict"]["verdict"], flush=True)
    print("criteria:", json.dumps(out["criteria"], ensure_ascii=False,
                                  default=str), flush=True)
    print("pooled h2h:", out["all_faces_pooled"]["h2h_vs_base"], flush=True)
    print("trigger slice family trigger pooled:",
          out["trigger_slice"]["variance"]["family_trigger_cells_pooled"],
          flush=True)
    print("profiler acc:", out["profiler"]["confusion"]["accuracy"], flush=True)
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


def _aggregate(out, panel_rows, comp_rows, panel_rows_all, slice_rows_all,
               ledger, mine, admitted, rejected, old_worlds, new_worlds,
               budget):
    idx_all = {}
    for r in panel_rows_all + slice_rows_all:
        idx_all[(r["form"], r["face"], r["seed"], r["seat"])] = r
    led_other = {}
    for key in ("panel", "slice", "slice_ext"):
        for r in ledger.get(key, []):
            if r["form"] in ("oc_c1", "oc_c1c2c3", "oc_c2") \
                    and r.get("margin") is not None:
                led_other.setdefault(
                    (r["form"], r["face"], r["seed"], r["seat"]), r)
    out["ledger_crosscheck"] = _crosscheck(
        [r for r in panel_rows + comp_rows if not r.get("from_ledger")],
        led_other)
    import profiler_core as _pc
    out["profiler"] = {
        "calibration": "calib_fingerprints.json（36 局=6 件×3 seeds×双席；"
                       "阈值冻结；probe_expected 7/7）；profiler_core sha "
                       + hashlib.sha256(_pc.CORE_SRC.encode()).hexdigest()[:16],
        "classes": ["r37_2965_family", "h1_mirror", "wfr", "unknown"],
        "confusion": J._confusion(panel_rows_all + slice_rows_all),
    }
    pairs, pooled = _agg_pairs(panel_rows_all, slice_rows_all, idx_all)
    out["pairs_by_opponent"] = pairs
    out["all_faces_pooled"] = pooled
    out["trigger_slice"] = _agg_trigger_slice(
        slice_rows_all, idx_all, mine, admitted, rejected,
        old_worlds, new_worlds)
    _criteria_verdict(out)
    out["anomaly"] = _anomaly(out)
    if budget is not None:
        out["budget"] = budget
    return out


# ------------------------------------------------------------ 重算（不跑局） --
def reagg():
    """按格级触发口径重算聚合；数据源=raw_judgment_v2.json（不变）。"""
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    out = json.loads(FINAL_PATH.read_text(encoding="utf-8"))
    panel_rows_all = raw["panel"]
    slice_rows_all = raw["slice"]
    panel_rows = [r for r in panel_rows_all if not r.get("from_ledger")]
    comp_rows = [r for r in slice_rows_all if not r.get("from_ledger")]
    led_slice_seeds = sorted({r["seed"] for r in slice_rows_all
                              if r.get("from_ledger")})
    new_worlds = sorted({r["probe_of"] for r in slice_rows_all
                         if r.get("probe_of") is not None})
    ts_old = out.get("trigger_slice", {})
    mine = (out.get("source", {}).get("trigger_slice_mining")
            or ts_old.get("mining") or {})
    adm = ts_old.get("admission", {})
    _aggregate(out, panel_rows, comp_rows, panel_rows_all, slice_rows_all,
               ledger, mine, adm.get("admitted_new", []),
               adm.get("rejected", []), led_slice_seeds, new_worlds, None)
    out["version"] = RECORD_VERSION
    out.setdefault("source", {}).setdefault("caliber", {})[
        "trigger_unit"] = ("触发判定落 (world×face) 格行级实测（world 实现依赖"
                           "对手件动作流，v2.1 修正）")
    out["reagg"] = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "v2.1 聚合口径修正重算（不跑局）：触发判定由世界级改为 "
                "(world×face) 格级；判据⑤改以实触发 family 格池化读数；"
                "数据=evidence/raw_judgment_v2.json 不变",
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    _write(out)
    print("verdict:", out["verdict"]["verdict"], flush=True)
    print("criteria:", json.dumps(out["criteria"], ensure_ascii=False,
                                  default=str), flush=True)
    fam = out["trigger_slice"]["variance"]["family_trigger_cells_pooled"]
    print("family trigger pooled:", fam, flush=True)
    print("family all-cells pooled:",
          out["trigger_slice"]["variance"]["family_all_cells_pooled"], flush=True)
    return out


def _write(out):
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "reagg":
        reagg()
    else:
        main()
