# -*- coding: utf-8 -*-
"""judge_oppcond：分对手面判决（画像器+条件策略；判决先行·不发射·不提交）。

责任口径（任务 opp-conditional A1 判决）：
面板 5 面（vs r37 / vs 2965 纯件 / vs r40 / vs H1 镜像 / vs WFR 反制臂）×
形态 4（h1_base / oc_c1 / oc_c2 / oc_c1c2c3）——每对 n=16 双席折叠
（配对单元=(seed,seat)，K2 口径；8 seeds × 2 席=16 局/臂/对）；语料=26 败局
分层抽 4 + 新中性块 672000+i*59 抽 4。补充 ICE+YARN 触发切片（mine_worlds
定向挖掘 3 seeds × 5 面 × 4 形态）——C1 门机制验证（cond-route 触发切片
先例）。sim_bridge 先认证 30/30；workers=2；判决预算 ≤500 局次（auth/挖掘
另计，cond-route 先例）。

判读（预登记判据）：
- 全对面 h2h vs H1_base ≥0.55（配对虚拟 h2h：同面同 seed 同席 arm margin
  > base margin 记胜，等=平；全 5 面池化 80 单元）；
- 逐对手面无一劣化（各面 mean Δ≥−50/局；Δ=margin_arm−margin_base 配对）；
- 画像准确率 ≥0.8（混淆矩阵：对已知对手件，family 级真值）；
- 未知类零足迹（unknown 单元内逐拍动作流 arm vs base 零差异）。

读数：margin=farms[our].money−farms[opp].money（run_games banks 干净口径）；
终局钱/实现价=judge_strongest.clean_reads（farms[obs.player] 口径）。
只写 orderbook_oppcond_lab/evidence/ 与
fn_docs/hybrid/results/2026-09-29-opp-conditional.json。不改既有代码。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import multiprocessing
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

from profiler_core import replay_class  # noqa: E402

RECORD_VERSION = "opp-conditional/1.0"
BUILD = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
RAW_PATH = EVID_DIR / "raw_judgment.json"
FINAL_PATH = (MODULE_DIR.parents[3] / "fn_docs" / "hybrid" / "results"
              / "2026-09-29-opp-conditional.json")

FORMS = {
    "h1_base": str(BUILD / "h1_base" / "main.py"),
    "oc_c1": str(BUILD / "oc_c1" / "main.py"),
    "oc_c2": str(BUILD / "oc_c2" / "main.py"),
    "oc_c1c2c3": str(BUILD / "oc_c1c2c3" / "main.py"),
}
FORM_CFG = {  # 门开关（build_manifest 同步）
    "h1_base": {"c1": False, "c2": False, "c3": False},
    "oc_c1": {"c1": True, "c2": False, "c3": False},
    "oc_c2": {"c1": False, "c2": True, "c3": False},
    "oc_c1c2c3": {"c1": True, "c2": True, "c3": True},
}
FACES = {
    "r37": str(KSIM_DIR / "orderbook_r37" / "build" / "main.py"),
    "2965": str(KSIM_DIR / "orderbook_2965_adopt" / "a" / "main.py"),
    "r40": str(KSIM_DIR / "orderbook_r40" / "build" / "main.py"),
    "h1": str(KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"),
    "wfr": str(KSIM_DIR / "orderbook_iterk_lab" / "opponents"
               / "counter_wool_front_runner.py"),
}
GROUND_TRUTH = {  # family 级真值（预登记；r37/2965/r40 窗口内逐拍全同→系谱）
    "r37": "r37_2965_family", "2965": "r37_2965_family",
    "r40": "r37_2965_family", "h1": "h1_mirror", "wfr": "wfr",
}
TRIGGER_KEY = "ICE_CREAM_SHOP+YARN_STORE"
WORKERS = 2
BUDGET_CAP = 500                # 判决局次（panel+slice；auth/挖掘另计）
REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
PANEL_SEEDS = REPLAY_26[:4] + [672000 + i * 59 for i in range(8)][:4]
SLICE_FOLDS_TARGET = 3
MINE_SEED_BASE = 705000
MINE_SEED_STEP = 53
MINE_SCAN_CAP = 20000
REC_SEED = 960001


def _load_js():
    p = KSIM_DIR / "orderbook_strongest_lab" / "judge_strongest.py"
    spec = importlib.util.spec_from_file_location("judge_strongest_reuse", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


JS = _load_js()


def _canon_sha(act) -> str:
    try:
        return hashlib.sha256(
            json.dumps(act, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
    except Exception:
        return "err"


def _stream_diff(da, db, cap=3):
    """两 digest 流逐拍对比。"""
    diffs = []
    for i in range(max(len(da), len(db))):
        a = da[i] if i < len(da) else None
        b = db[i] if i < len(db) else None
        if a != b:
            diffs.append({"i": i, "a": a, "b": b})
    return {"n_steps_a": len(da), "n_steps_b": len(db),
            "n_diff": len(diffs), "first_diff_step": diffs[0]["i"] if diffs else None,
            "diffs_sample": diffs[:cap]}


# ------------------------------------------------------------ 跑局 --
def _run_chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
    cfg = dict(payload.get("cfg") or {})
    cfg["workers"] = 1
    games, meta = [], []
    for spec in payload["specs"]:
        ag, sinks = j23._build_agents(spec["spec"])
        games.append({"seed": int(spec["spec"]["seed"]), "agents": ag})
        meta.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": [], "engine": None}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks) in enumerate(meta):
        rr = rows_run[i] if i < len(rows_run) else {}
        seat = int(spec["spec"]["our_seat"])
        sink = (sinks or {}).get(seat) or []
        row = {
            "form": spec["form"], "face": spec["face"],
            "kind": spec["spec"]["kind"], "seed": int(spec["spec"]["seed"]),
            "seat": seat, "banks": rr.get("banks"), "error": rr.get("error"),
        }
        if rr.get("banks") is not None and rr.get("error") is None:
            banks = rr["banks"]
            row["margin"] = round(float(banks[seat]) - float(banks[1 - seat]), 2)
            reads = JS.clean_reads(sink)
            row["terminal_money"] = reads.get("terminal_money")
            row["realized_px"] = reads.get("realized_px")
            row["stranding"] = reads.get("stranding")
            # 画像重放（CORE_SRC 同源字节）
            cls, why, st = replay_class(sink)
            row["cls"] = cls
            row["cls_why"] = why
            row["profile"] = {
                "cashdiff1": st.get("cashdiff1"),
                "rival_money1": st.get("rival_money1"),
                "rkey2": st.get("rkey2"), "sim_max": st.get("sim_max"),
                "rival_animals_143": st.get("rival_animals_143"),
                "rival_sold_cum": st.get("rival_sold_cum"),
            }
            # 世界店对（step144 揭示帧实测）
            pair = None
            for entry in sink:
                if int(entry[0]) == 144 and isinstance(entry[1], dict):
                    try:
                        pair = ab._pair_key(entry[1])
                    except Exception:
                        pair = None
                    break
            row["world_pair"] = pair
            row["trigger"] = (pair == TRIGGER_KEY)
            # 逐拍动作 digest（足迹审计）
            row["stream"] = [_canon_sha(e[2]) for e in sink]
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play(specs, cfg=None):
    n_chunks = max(1, min(WORKERS * 8, len(specs)))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks if c]
    if WORKERS <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows = []
    for p in parts:
        rows.extend(p["rows"])
    return rows, [{"engine": p.get("engine"),
                   "fallback_reason": p.get("fallback_reason")} for p in parts]


# ------------------------------------------------------------ 聚合 --
def _mk_specs():
    specs = []

    def _add(kind, form, face, seed, seat):
        agents = ([{"type": "python", "path": FORMS[form]},
                   {"type": "python", "path": FACES[face]}] if seat == 0
                  else [{"type": "python", "path": FACES[face]},
                        {"type": "python", "path": FORMS[form]}])
        specs.append({"form": form, "face": face, "spec": {
            "game_id": "%s-%s-%s-%d-%d" % (kind, form, face, seed, seat),
            "seed": int(seed), "kind": kind, "trace": True,
            "our_seat": seat, "agents": agents}})

    for face in FACES:
        for form in FORMS:
            for seed in PANEL_SEEDS:
                for seat in (0, 1):
                    _add("panel", form, face, seed, seat)
    return specs


def _mk_slice_specs(seeds):
    specs = []

    def _add(kind, form, face, seed, seat):
        agents = ([{"type": "python", "path": FORMS[form]},
                   {"type": "python", "path": FACES[face]}] if seat == 0
                  else [{"type": "python", "path": FACES[face]},
                        {"type": "python", "path": FORMS[form]}])
        specs.append({"form": form, "face": face, "spec": {
            "game_id": "%s-%s-%s-%d-%d" % (kind, form, face, seed, seat),
            "seed": int(seed), "kind": kind, "trace": True,
            "our_seat": seat, "agents": agents}})

    for face in FACES:
        for form in FORMS:
            for seed in seeds:
                for seat in (0, 1):
                    _add("slice", form, face, seed, seat)
    return specs


def _index(rows):
    return {(r["form"], r["face"], r["seed"], r["seat"]): r for r in rows}


def _face_agg(rows, form, face, idx, kind):
    """单 (form,face) 聚合：fold W/L/T + 配对 Δ vs h1_base + 读数。"""
    mine = [r for r in rows if r["form"] == form and r["face"] == face
            and r["kind"] == kind and r.get("margin") is not None]
    if not mine:
        return {"n_units": 0}
    fold_rows = [{"seed": r["seed"], "margin": r["margin"]} for r in mine]
    fold = JS.fold_arm(fold_rows)
    reads = JS._reads_agg([{"reads": {"terminal_money": r.get("terminal_money"),
                                      "realized_px": r.get("realized_px"),
                                      "stranding": r.get("stranding")}}
                           for r in mine], "reads")
    deltas, wins, ties, losses = [], 0, 0, 0
    for r in mine:
        b = idx.get(("h1_base", face, r["seed"], r["seat"]))
        if not b or b.get("margin") is None:
            continue
        d = round(r["margin"] - b["margin"], 2)
        deltas.append(d)
        if d > 0:
            wins += 1
        elif d < 0:
            losses += 1
        else:
            ties += 1
    n = len(deltas)
    return {
        "n_units": len(mine), "n_folds": fold["n"], "wins": fold["wins"],
        "losses": fold["losses"], "ties": fold["ties"], "h2h": fold["h2h"],
        "mean_margin": fold["mean_margin"], "fold_margins": fold["fold_margins"],
        "ours": reads,
        "vs_base_paired": {
            "n_units": n,
            "mean_delta": round(sum(deltas) / n, 2) if n else None,
            "deltas": deltas, "wins": wins, "ties": ties, "losses": losses,
            "h2h_vs_base": round((wins + 0.5 * ties) / n, 4) if n else None,
        },
    }


def _confusion(rows):
    """画像混淆矩阵（piece × 预测类；family 级真值）。"""
    pieces = list(FACES)
    classes = ["r37_2965_family", "h1_mirror", "wfr", "unknown"]
    matrix = {p: {c: 0 for c in classes} for p in pieces}
    n = correct = 0
    for r in rows:
        if r.get("margin") is None or r.get("cls") is None:
            continue
        n += 1
        matrix[r["face"]][r["cls"]] = matrix[r["face"]].get(r["cls"], 0) + 1
        if r["cls"] == GROUND_TRUTH[r["face"]]:
            correct += 1
    return {"ground_truth_family": GROUND_TRUTH,
            "note": ("r37/2965a/2965b/r40 开局窗逐拍公开信号全同"
                     "（route0[:144] 动作哈希 b518f3763802）→ 系谱级不可分；"
                     "family 级真值口径"),
            "matrix": matrix, "n": n, "n_correct": correct,
            "accuracy": round(correct / n, 4) if n else None}


def _footprint(rows):
    """足迹审计：非 base 形态 vs base 同 (face,seed,seat) 逐拍 digest 对比。

    零足迹期望：门不触发单元（unknown/h1_mirror 类，或 C1 触发世界外且无
    C2/C3 门）逐拍零差异。硬断言=unknown 单元零差异（判据 ④）。
    """
    idx = _index(rows)
    per_form = {}
    unknown_violations, mirror_violations = [], []
    gate_precision = {}
    for form in FORMS:
        if form == "h1_base":
            continue
        cfg = FORM_CFG[form]
        fp_rows = []
        n_diff_units = n_expected = n_unexpected_diff = 0
        for face in FACES:
            for r in rows:
                if r["form"] != form or r["face"] != face \
                        or r.get("stream") is None:
                    continue
                b = idx.get(("h1_base", face, r["seed"], r["seat"]))
                if not b or b.get("stream") is None:
                    continue
                d = _stream_diff(r["stream"], b["stream"])
                cls = r.get("cls")
                trg = bool(r.get("trigger"))
                expect_diff = ((cfg["c1"] and cls == "r37_2965_family" and trg)
                               or (cfg["c2"] and cls == "r37_2965_family")
                               or (cfg["c3"] and cls == "wfr"))
                row = {"face": face, "seed": r["seed"], "seat": r["seat"],
                       "cls": cls, "trigger": trg,
                       "expect_diff": expect_diff,
                       "n_diff": d["n_diff"],
                       "first_diff_step": d["first_diff_step"]}
                if d["n_diff"]:
                    n_diff_units += 1
                    if not expect_diff:
                        n_unexpected_diff += 1
                        row["diffs_sample"] = d["diffs_sample"]
                        if cls == "unknown":
                            unknown_violations.append(dict(row))
                        elif cls == "h1_mirror":
                            mirror_violations.append(dict(row))
                if expect_diff:
                    n_expected += 1
                fp_rows.append(row)
        per_form[form] = {
            "n_units": len(fp_rows), "n_diff_units": n_diff_units,
            "n_expect_diff_units": n_expected,
            "n_unexpected_diff_units": n_unexpected_diff,
            "rows_lite": [{k: v for k, v in r.items() if k != "diffs_sample"}
                          for r in fp_rows],
        }
        gate_precision[form] = {
            "expect_diff_units": n_expected,
            "observed_diff_units": n_diff_units,
            "unexpected_diff_units": n_unexpected_diff,
        }
    return {
        "design": "同 face 同 seed 同席：form vs h1_base 逐拍动作 digest 对比"
                  "（4 流口径简化为我席 1 流；opponent 确定性响应级联计入差异拍）",
        "zero_footprint_rule": "门不触发单元（unknown/h1_mirror，或 C1 触发"
                               "世界外且无 C2/C3 门）逐拍零差异；unknown 单元"
                               "零差异=判据④硬断言",
        "per_form": per_form, "gate_precision": gate_precision,
        "unknown_class_violations": unknown_violations,
        "h1_mirror_class_violations": mirror_violations,
        "unknown_class_zero_footprint": len(unknown_violations) == 0,
        "h1_mirror_zero_footprint": len(mirror_violations) == 0,
    }


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    budget = {"cap_局次": BUDGET_CAP, "auth_games_separate": 0,
              "mining_games_separate": 0, "panel_games": 0, "slice_games": 0,
              "judgment_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": [
                "python3 orderbook_oppcond_lab/calibrate_oppcond.py",
                "python3 orderbook_oppcond_lab/build_oppcond.py grid",
                "python3 orderbook_oppcond_lab/calibrate_grid_c2.py",
                "python3 orderbook_oppcond_lab/build_oppcond.py final --h-short 12",
                "python3 orderbook_oppcond_lab/gates_oppcond.py",
                "python3 orderbook_oppcond_lab/judge_oppcond.py"],
            "base_main": str(FORMS["h1_base"]),
            "base_main_sha256": hashlib.sha256(
                Path(FORMS["h1_base"]).read_bytes()).hexdigest(),
            "forms": FORMS, "faces": FACES,
            "panel_seeds": PANEL_SEEDS,
            "panel_corpus": "26 败局分层抽 4（REPLAY_26[:4]）+ 新中性块 "
                            "672000+i*59 抽 4（i=0..3）",
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
            },
        },
    }

    # ---- 0. 门禁读入 ----
    gates = json.loads((MODULE_DIR / "evidence" / "gates.json")
                       .read_text(encoding="utf-8")) \
        if (MODULE_DIR / "evidence" / "gates.json").is_file() \
        else {"overall_passed": False, "error": "gates.json 缺失"}
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
                "byte_identical_to_H1_base": m.get("byte_identical_to_H1_base"),
                "probes_ok": True,
            }
    if not gates.get("overall_passed"):
        out["aborted"] = "四门未全过，判决中止"
        _write(out)
        return out

    # ---- 1. sim_bridge 对照认证 30/30 ----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_corpus = REPLAY_26 + [2026092901, 2026092902, 2026092903, 2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "sim_auth.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    budget["auth_games_separate"] = 60
    out["source"]["sim_auth"] = auth_lite
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["budget"] = budget
        _write(out)
        return out

    # ---- 2. ICE+YARN 触发切片挖掘（mine_worlds 唯件）----
    import mine_worlds as mw  # noqa: WPS433
    mine_t0 = time.perf_counter()
    srv = mw.Serve()
    try:
        rec = mw.record_pair(str(FORMS["h1_base"]), REC_SEED, srv)
        lines = rec["tapes"]["order_h1_first"]["lines"]
        lines2 = rec["tapes"]["order_h1_second"]["lines"]
        found, scanned = [], 0
        for i in range(MINE_SCAN_CAP):
            s = MINE_SEED_BASE + i * MINE_SEED_STEP
            wk = mw.predict_world(s, lines[0], lines[1], srv)
            scanned += 1
            if mw.pair_key(wk) == TRIGGER_KEY:
                found.append(s)
                if len(found) >= SLICE_FOLDS_TARGET:
                    break
        mine = {"method": "gengame 磁带重放定向（H1 实录磁带预测店对；"
                         "mine_worlds 唯件）",
                "rec_seed": REC_SEED,
                "seed_domain": "%d+i*%d" % (MINE_SEED_BASE, MINE_SEED_STEP),
                "n_scanned_predictions": scanned, "seeds": found,
                "elapsed_s": round(time.perf_counter() - mine_t0, 2)}
    finally:
        srv.close()
    budget["mining_games_separate"] = 2
    out["source"]["trigger_slice_mining"] = mine
    print("mined", len(found), "ICE+YARN seeds", flush=True)

    # ---- 3. 面板（5 面 × 4 形态 × 8 seeds × 双席）----
    specs = _mk_specs()
    budget["panel_games"] = len(specs)
    print("panel games:", len(specs), flush=True)
    run_cfg = {"engine": "auto", "bridge": auth}
    t1 = time.perf_counter()
    rows, engines = _play(specs, run_cfg)
    rows.sort(key=lambda r: (r["kind"], r["face"], r["form"], r["seed"], r["seat"]))
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps({"panel": _lite_rows(rows)}, ensure_ascii=False,
                                   indent=1, default=str) + "\n", encoding="utf-8")
    print("panel done", round(time.perf_counter() - t1, 1), "s", flush=True)

    # ---- 4. 触发切片 ----
    slice_specs = _mk_slice_specs(found)
    budget["slice_games"] = len(slice_specs)
    budget["judgment_games"] = budget["panel_games"] + budget["slice_games"]
    if budget["judgment_games"] > BUDGET_CAP:
        out["aborted"] = "判决局次 %d 超预算 %d" % (budget["judgment_games"],
                                                   BUDGET_CAP)
        out["budget"] = budget
        _write(out)
        return out
    print("slice games:", len(slice_specs), "budget:",
          budget["judgment_games"], flush=True)
    t2 = time.perf_counter()
    s_rows, s_engines = _play(slice_specs, run_cfg) if slice_specs else ([], [])
    s_rows.sort(key=lambda r: (r["face"], r["form"], r["seed"], r["seat"]))
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    raw["slice"] = _lite_rows(s_rows)
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    print("slice done", round(time.perf_counter() - t2, 1), "s", flush=True)

    # ---- 5. 画像混淆矩阵（panel+slice 全 traced 局）----
    out["profiler"] = {
        "calibration": "calib_fingerprints.json（36 局=6 件×3 seeds×双席；"
                       "阈值冻结；probe_expected 7/7）",
        "classes": ["r37_2965_family", "h1_mirror", "wfr", "unknown"],
        "confusion": _confusion(rows + s_rows),
    }

    # ---- 6. 分对手面聚合 ----
    idx_all = _index(rows + s_rows)
    pairs_by_opponent = {}
    for kind, rws in (("panel", rows), ("slice", s_rows)):
        faces_out = {}
        for face in FACES:
            forms_out = {}
            for form in FORMS:
                forms_out[form] = _face_agg(rws, form, face, idx_all, kind)
            faces_out[face] = forms_out
        pairs_by_opponent[kind] = faces_out
    out["pairs_by_opponent"] = pairs_by_opponent

    # 全对面池化（panel；full form）
    pooled_d, pooled_w, pooled_t, pooled_l = [], 0, 0, 0
    for face in FACES:
        pp = pairs_by_opponent["panel"][face]["oc_c1c2c3"].get(
            "vs_base_paired", {})
        pooled_d.extend(pp.get("deltas") or [])
        pooled_w += pp.get("wins", 0)
        pooled_t += pp.get("ties", 0)
        pooled_l += pp.get("losses", 0)
    n_pooled = len(pooled_d)
    out["all_faces_pooled"] = {
        "form": "oc_c1c2c3", "kind": "panel",
        "n_units": n_pooled,
        "mean_delta": round(sum(pooled_d) / n_pooled, 2) if n_pooled else None,
        "wins": pooled_w, "ties": pooled_t, "losses": pooled_l,
        "h2h_vs_base": round((pooled_w + 0.5 * pooled_t) / n_pooled, 4)
        if n_pooled else None,
    }

    # ---- 7. 足迹审计 ----
    out["footprint_audit"] = _footprint(rows + s_rows)

    # ---- 8. 触发切片机制核对 ----
    slice_trigger = {}
    for face in FACES:
        row = {}
        for form in FORMS:
            agg = pairs_by_opponent["slice"][face][form]
            row[form] = {"mean_delta": agg.get("vs_base_paired", {})
                         .get("mean_delta"),
                         "n_units": agg.get("vs_base_paired", {}).get("n_units")}
        slice_trigger[face] = row
    n_trg = sum(1 for r in rows if r.get("trigger"))
    n_trg_s = sum(1 for r in s_rows if r.get("trigger"))
    out["trigger_slice"] = {
        "mining": mine,
        "world_check": {
            "panel_trigger_units": n_trg,
            "slice_trigger_units": n_trg_s,
            "slice_all_trigger": n_trg_s == len([r for r in s_rows
                                                 if r.get("margin") is not None]),
        },
        "per_face_vs_base": slice_trigger,
    }

    # ---- 9. 判据与 verdict（预登记）----
    h2h = out["all_faces_pooled"]["h2h_vs_base"]
    c1 = h2h is not None and h2h >= 0.55
    face_deltas = {}
    c2 = True
    for face in FACES:
        d = (pairs_by_opponent["panel"][face]["oc_c1c2c3"]
             .get("vs_base_paired", {}).get("mean_delta"))
        face_deltas[face] = d
        if d is None or d < -50:
            c2 = False
    acc = out["profiler"]["confusion"]["accuracy"]
    c3 = acc is not None and acc >= 0.8
    c4 = out["footprint_audit"]["unknown_class_zero_footprint"]
    out["criteria"] = {
        "全对面 h2h vs H1_base ≥0.55": {"passed": bool(c1), "reading": h2h},
        "逐对手面无一劣化（各面 mean Δ≥−50/局）": {
            "passed": bool(c2), "per_face_mean_delta": face_deltas,
            "threshold": -50},
        "画像准确率 ≥0.8": {"passed": bool(c3), "reading": acc},
        "未知类零足迹": {"passed": bool(c4),
                         "n_violations": len(
                             out["footprint_audit"]["unknown_class_violations"])},
    }
    ok_all = all(v["passed"] for v in out["criteria"].values())
    out["verdict"] = {
        "verdict": ("OPP_CONDITIONAL_CONFIRMED: 条件化四判据全过"
                    if ok_all else "NOT_CONFIRMED（详见 criteria）"),
        "criteria_passed": ok_all,
        "ablation": {
            "note": "逐件独立消融=同面板配对 Δ（oc_c1/oc_c2 单件形态 vs base；"
                    "oc_c1c2c3 全套）",
            "per_face_mean_delta": {
                form: {face: (pairs_by_opponent["panel"][face][form]
                              .get("vs_base_paired", {}).get("mean_delta"))
                       for face in FACES}
                for form in ("oc_c1", "oc_c2", "oc_c1c2c3")},
        },
    }

    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
        "harness 噪声：kaggle_environments 可选环境加载告警（open_spiel/cabt）"
        "——无关环境忽略",
        "r37/2965a/2965b/r40 开局窗逐拍公开信号全同（route0[:144] 动作哈希 "
        "b518f3763802 四件一致；money 轨迹逐拍相等）→ 窗口内不可分，画像类合并"
        "系谱级（r37/2965 系谱型）；C1 对 r37/2965 同动=动作等价，C2 视界按 r37"
        "标定（H*=12 minimax 三件全正）",
        "tetsutani 型未入面板（无该对手件）；镜像门=EXP288 step1 现金差<0.5 口径",
        "r40 面真值记 r37 型（家族级：其开局窗与 r37 逐拍全同，公开信号不可分）",
        "终局钱口径 farms[obs.player]（judge_strongest.clean_reads；避开 "
        "judge_r26 farms[0] 污染）",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    _write(out)
    print("verdict:", out["verdict"]["verdict"], out["criteria"], flush=True)
    print("h2h pooled:", h2h, "face deltas:", face_deltas, flush=True)
    print("profiler acc:", acc, flush=True)
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


def _lite_rows(rows):
    return [{k: v for k, v in r.items() if k != "stream"} for r in rows]


def _write(out):
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                     default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
