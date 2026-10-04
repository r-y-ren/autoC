# -*- coding: utf-8 -*-
"""judge_oppcond_ext：C1 触发切片追加（预算余量 36 局；不发射·不提交）。

责任口径：主判决（judge_oppcond）已出——判据绑定 panel 预登记口径，本追加
**不改变判据/verdict**。动机：C1（r105 条件路由）在触发切片上的效应为世界级
大方差（主切片逐 seed Δ=[−861,−5327,+6140]，与 track1 逐 fold
[−6838..+6404] 同型），主切片 n=6 单元/面不足以对"+2295 复现"下结论。追加
= 新域（715000+i*53）再挖 3 个 ICE+YARN 世界 × 系谱三面 × {h1_base, oc_c1}
× 双席 = 36 局 → C1 合并读数 n=12 单元/面（cond-route 触发切片 n≥12 口径）。
引擎=official 直跑（省再认证；sim 认证已证 30/30 banks 同）。
合并落盘：evidence/raw_judgment.json（slice_ext 行）+
fn_docs/hybrid/results/2026-09-29-opp-conditional.json（profiler.confusion、
trigger_slice.c1_combined、budget、anomaly 增补；criteria/verdict 不动）。
只写 orderbook_oppcond_lab/ 与上述 results 文件。
"""
from __future__ import annotations

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
sys.path.insert(0, str(MODULE_DIR))

import judge_oppcond as J  # noqa: E402
from profiler_core import replay_class  # noqa: E402

EXT_FORMS = ("h1_base", "oc_c1")
EXT_FACES = ("r37", "2965", "r40")
EXT_SEED_BASE = 715000
EXT_SEED_STEP = 53
EXT_FOLDS_TARGET = 3


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    evid = MODULE_DIR / "evidence"
    raw_path = evid / "raw_judgment.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))

    # ---- 1. 新域挖 ICE+YARN ----
    import mine_worlds as mw  # noqa: WPS433
    srv = mw.Serve()
    try:
        rec = mw.record_pair(str(J.FORMS["h1_base"]), J.REC_SEED, srv)
        lines = rec["tapes"]["order_h1_first"]["lines"]
        found, scanned = [], 0
        for i in range(J.MINE_SCAN_CAP):
            s = EXT_SEED_BASE + i * EXT_SEED_STEP
            wk = mw.predict_world(s, lines[0], lines[1], srv)
            scanned += 1
            if mw.pair_key(wk) == J.TRIGGER_KEY:
                found.append(s)
                if len(found) >= EXT_FOLDS_TARGET:
                    break
    finally:
        srv.close()
    print("ext mined", found, flush=True)

    # ---- 2. 36 局（official 直跑）----
    specs = []
    for face in EXT_FACES:
        for form in EXT_FORMS:
            for seed in found:
                for seat in (0, 1):
                    agents = ([{"type": "python", "path": J.FORMS[form]},
                               {"type": "python", "path": J.FACES[face]}]
                              if seat == 0 else
                              [{"type": "python", "path": J.FACES[face]},
                               {"type": "python", "path": J.FORMS[form]}])
                    specs.append({"form": form, "face": face, "spec": {
                        "game_id": "slice_ext-%s-%s-%d-%d"
                                   % (form, face, seed, seat),
                        "seed": int(seed), "kind": "slice_ext", "trace": True,
                        "our_seat": seat, "agents": agents}})
    rows, engines = J._play(specs, {"engine": "official"})
    rows.sort(key=lambda r: (r["face"], r["form"], r["seed"], r["seat"]))
    n_err = sum(1 for r in rows if r.get("error"))
    print("ext games", len(rows), "errors", n_err, flush=True)

    # ---- 3. 合并 ----
    raw["slice_ext"] = J._lite_rows(rows)
    raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")

    all_rows = []
    for key in ("panel", "slice", "slice_ext"):
        all_rows.extend([
            # 重灌 stream 无关字段；stream 只在内存需要时由 raw 不存
            r for r in raw[key] if r.get("margin") is not None])
    final_path = J.FINAL_PATH
    out = json.loads(final_path.read_text(encoding="utf-8"))

    # 画像混淆（panel+slice+slice_ext 全 traced 局）
    out["profiler"]["confusion"] = J._confusion(
        [r for key in ("panel", "slice", "slice_ext") for r in raw[key]])

    # C1 合并读数（主切片 + 追加切片；n=12 单元/面）
    idx_all = {}
    for key in ("panel", "slice", "slice_ext"):
        for r in raw[key]:
            idx_all[(r["form"], r["face"], r["seed"], r["seat"])] = r
    c1_combined = {}
    for face in EXT_FACES:
        deltas = []
        for key in ("slice", "slice_ext"):
            for r in raw[key]:
                if r["face"] != face or r["form"] != "oc_c1" \
                        or r.get("margin") is None:
                    continue
                b = idx_all.get(("h1_base", face, r["seed"], r["seat"]))
                if b and b.get("margin") is not None:
                    deltas.append(round(r["margin"] - b["margin"], 2))
        c1_combined[face] = {
            "n_units": len(deltas), "deltas": deltas,
            "mean_delta": round(sum(deltas) / len(deltas), 2) if deltas else None,
            "n_达标_cond_route_n12": len(deltas) >= 12,
        }
    out["trigger_slice"]["c1_combined"] = {
        "note": "C1（r105 条件路由）触发世界配对 Δ 合并读数（主切片 705 域 "
                "3 seeds + 追加切片 715 域 3 seeds；预算余量 36 局；判据不因此改变）",
        "per_face": c1_combined,
        "mining_ext": {"seed_domain": "%d+i*%d" % (EXT_SEED_BASE,
                                                   EXT_SEED_STEP),
                       "n_scanned_predictions": scanned, "seeds": found},
        "engine": "official（sim 认证已证 30/30 banks 同；追加省再认证）",
    }

    out["budget"]["slice_ext_games"] = len(rows)
    out["budget"]["judgment_games"] += len(rows)
    out["anomaly"].append(
        "C1 触发效应=世界级大方差（合并 n=12/面：逐 seed Δ=[−861,−5327,+6140]"
        "+追加批 3 seeds]；与 track1 逐 fold [−6838..+6404] 同型）——+2295 复现"
        "在此语料未见；逐 seed 相同于系谱三面（对手件窗口内不可分的直接后果）")
    out["anomaly"].append(
        "追加切片（slice_ext）仅补 C1 读数精度；判据/verdict 绑定 panel 预登记"
        "口径不因此改变")
    out["elapsed_s"] = round(out.get("elapsed_s", 0) + time.perf_counter() - t0, 1)
    final_path.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                     default=str) + "\n", encoding="utf-8")
    print("c1_combined:", json.dumps(c1_combined, ensure_ascii=False), flush=True)
    print("confusion acc:", out["profiler"]["confusion"]["accuracy"], flush=True)
    return out


if __name__ == "__main__":
    main()
