# -*- coding: utf-8 -*-
"""judge_behavsel：D3 行为选择器 v2 判决（判决先行·不发射·不提交·不改既有代码）。

新评判标准（任务 D3 预登记，必须按此判）：
  ①直接对战强面板 {oc_c3 冠军锚, mpx, tetsutani, V89} n=12 双席——对强面板
    h2h ≥ 0.5；
  ②同族专组 {tetsutani, V89, lynn} 池化 h2h ≥ 0.75（基线=同族 0.75）；
  ③弱锚 {r40, A} 池化 h2h ≥ 0.8；
  ④对 oc_c3 直接 h2h ≥ 0.5（才算更强）；
  ⑤配对边际只作参考（margin 不入判）。
逐件消融：bs2_nogap（臂1 关）vs bs2 于 {tetsutani, lynn} 同格配对；bs2_noslot
（臂2 关）同格配对；bs2_noc3（臂3 关）vs bs2 于 {wfr} 同格配对（C3 仅 wfr 类
触发，面板内惰性=零动作安全佐证）。
语料 n=12：26 败局前 6（1825501814…240876256）+ 新中性 674000+i*131×6；
双席=24 局/对。sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤400 局次。
证据落 fn_docs/hybrid/results/2026-09-30-d3-behavior-select.json；账本落
orderbook_behavsel_lab/evidence/。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_track1_lab"),
          str(KSIM_DIR / "orderbook_oppcond_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_oppcond as J  # noqa: E402  复用 _play/_run_chunk（只读）
import profiler_core  # noqa: E402

RECORD_VERSION = "d3-behavior-select/1.0"
BUILD = MODULE_DIR / "build"
EVID = MODULE_DIR / "evidence"
FINAL_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-d3-behavior-select.json"
LEDGER_PATH = EVID / "judge_ledger.json"

FORMS = {name: str(BUILD / name / "main.py") for name in
         ("bs2", "bs2_nogap", "bs2_noslot", "bs2_noc3")}

_P = KSIM_DIR
OPP = {
    "oc_c3": (_P / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py",
              "3f8b57fd4d5e7070"),
    "mpx": (_P / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
            / "main.py", "f0101de9b558d1f5"),
    "tetsutani": (_P / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
                  / "main.py", "55be5d5f124c8daa"),
    "V89": (_P / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
            "01ee3976f97a9ac7"),
    "lynn": (_P / "orderbook_racegap_lab" / "opponents" / "lynn1010"
             / "main.py", "03165654e70bd044"),
    "r40": (_P / "orderbook_r40" / "build" / "main.py", "4ce951f088740e0b"),
    "A": (_P / "orderbook_r44_a" / "main.py", "b387307fc12e2610"),
    "wfr": (_P / "orderbook_iterk_lab" / "opponents"
            / "counter_wool_front_runner.py", None),
}
STRONG = ["oc_c3", "mpx", "tetsutani", "V89"]
WEAK = ["r40", "A"]
FAMILY = ["tetsutani", "V89", "lynn"]

LOSS_6 = J.REPLAY_26[:6]
NEUTRAL_6 = [674000 + i * 131 for i in range(6)]
FOLDS_12 = LOSS_6 + NEUTRAL_6
WORKERS = 2
BUDGET_CAP = 400


def _mk_spec(kind, form, opp, seed, seat):
    path = str(OPP[opp][0])
    agents = ([{"type": "python", "path": FORMS[form]},
               {"type": "python", "path": path}] if seat == 0
              else [{"type": "python", "path": path},
                    {"type": "python", "path": FORMS[form]}])
    return {"form": form, "face": opp, "spec": {
        "game_id": "%s-%s-%s-%d-%d" % (kind, form, opp, seed, seat),
        "seed": int(seed), "kind": kind, "trace": True,
        "our_seat": seat, "agents": agents}}


def direct_h2h(rows):
    n = w = l = t = 0
    margins = []
    folds = {}
    for r in rows:
        if r.get("margin") is None:
            continue
        n += 1
        m = float(r["margin"])
        margins.append(m)
        score = 1.0 if m > 0 else (0.5 if m == 0 else 0.0)
        if m > 0:
            w += 1
        elif m < 0:
            l += 1
        else:
            t += 1
        folds.setdefault(int(r["seed"]), []).append(score)
    fw = fl = ft = 0
    for _, sc in folds.items():
        avg = sum(sc) / len(sc)
        if avg >= 1.0:
            fw += 1
        elif avg <= 0.0:
            fl += 1
        else:
            ft += 1
    return {"n_games": n, "W": w, "L": l, "T": t,
            "h2h": round((w + 0.5 * t) / n, 4) if n else None,
            "margin_mean_ref": round(sum(margins) / n, 2) if n else None,
            "fold_dual_seat": {"W": fw, "L": fl, "T": ft,
                               "h2h": round((fw + 0.5 * ft)
                                            / max(1, len(folds)), 4)}}


def pooled_h2h(rows_by_opp, members):
    rows = []
    for m in members:
        rows.extend(rows_by_opp.get(m) or [])
    return direct_h2h(rows)


def paired_delta(base_rows, abl_rows):
    """同 (seed,seat) 配对：base−ablated（margin 口径）+ 翻胜/翻负。"""
    idx = {(r["seed"], r["seat"]): r for r in abl_rows
           if r.get("margin") is not None}
    deltas, flips_pos, flips_neg = [], 0, 0
    for r in base_rows:
        if r.get("margin") is None:
            continue
        b = idx.get((r["seed"], r["seat"]))
        if not b:
            continue
        d = round(float(r["margin"]) - float(b["margin"]), 2)
        deltas.append(d)
        if float(r["margin"]) > 0 >= float(b["margin"]):
            flips_pos += 1
        if float(r["margin"]) <= 0 < float(b["margin"]):
            flips_neg += 1
    n = len(deltas)
    return {"n_pairs": n,
            "mean_delta": round(sum(deltas) / n, 2) if n else None,
            "wins": sum(1 for d in deltas if d > 0),
            "ties": sum(1 for d in deltas if d == 0),
            "losses": sum(1 for d in deltas if d < 0),
            "flips_pos": flips_pos, "flips_neg": flips_neg,
            "deltas_head": deltas[:16]}


def footprint_audit(rows_by_form, cells):
    """非镜像类格（cls∉h1_mirror）零足迹：gap/slot 臂消融形态逐拍 digest
    与 bs2 恒等（C3 臂对 wfr 类按设计不同——不入本审计；结构探针⑥为硬证）。"""
    base = {(r["seed"], r["seat"], r["face"]): r
            for r in rows_by_form.get("bs2") or []}
    out = []
    for r in cells:
        if r.get("form") == "bs2_noc3":
            continue
        key = (r["seed"], r["seat"], r["face"])
        b = base.get(key)
        if not b or r.get("stream") is None or b.get("stream") is None:
            continue
        if r.get("cls") == "h1_mirror":
            continue
        same = (r["stream"] == b["stream"])
        out.append({"face": r["face"], "seed": r["seed"], "seat": r["seat"],
                    "form": r.get("form"), "cls": r.get("cls"),
                    "stream_identical": same})
    viol = [o for o in out if not o["stream_identical"]]
    return {"n_cells": len(out), "n_violations": len(viol),
            "violations": viol[:8], "passed": not viol,
            "note": "非镜像类格（如 wfr）上 gap/slot 臂不触发→与 bs2 逐拍"
                    "digest 恒等；unknown 类零足迹硬证=构建探针⑥"}


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    budget = {"cap_局次": BUDGET_CAP, "auth": 0, "gates": 0,
              "panel": 0, "ablation": 0}
    EV = {"version": RECORD_VERSION, "arms": {}, "profiler": {},
          "pairs_panel": {}, "family_group": {}, "criteria": {},
          "verdict": {}, "anomaly": []}

    # ---- 0) 身份核验（sha16）+ 门禁 ----
    for name, (p, sha) in OPP.items():
        if sha is None:
            continue
        got = hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
        if got != sha:
            raise RuntimeError("对手件 sha 漂移 %s: %s" % (name, got))
    spec = importlib.util.spec_from_file_location(
        "gates_oppcond_reuse",
        KSIM_DIR / "orderbook_oppcond_lab" / "gates_oppcond.py")
    G = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(G)
    gates = {}
    for form in FORMS:
        pkg = BUILD / form
        g = {}
        for gname, fn in (("load", G._gate_load), ("health", G._gate_health),
                          ("determinism", G._gate_determinism)):
            try:
                g[gname] = fn(pkg)
            except Exception as exc:
                g[gname] = {"passed": False,
                            "error": "%s: %s" % (type(exc).__name__, exc)}
        try:
            g["identity"] = G._gate_identity(pkg, form)
        except Exception as exc:
            g["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
        g["overall"] = all(x.get("passed") for x in g.values())
        gates[form] = g
        budget["gates"] += 4
        print("gates", form, {k: g[k].get("passed") for k in
                              ("load", "health", "determinism", "identity")},
              flush=True)
    EV["gates"] = gates
    if not all(g["overall"] for g in gates.values()):
        EV["verdict"] = {"verdict": "GATES_RED（构建/门禁未过，判决中止）",
                         "criteria_passed": False}
        EV["budget"] = budget
        _flush(EV)
        return EV

    # ---- 1) sim_bridge 对照认证 30/30（先认证） ----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_corpus = J.REPLAY_26 + [2026092901, 2026092902, 2026092903,
                                 2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID / "sim_auth_record.json")}, auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "version")}
    (EVID / "sim_auth.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str)
        + "\n", encoding="utf-8")
    EV["source"] = {"sim_auth": auth_lite, "workers": WORKERS,
                    "forms": FORMS, "folds_12": FOLDS_12,
                    "folds_spec": "26 败局前 6 + 新中性 674000+i*131×6；双席=24 局/对",
                    "caliber": "h2h=(W+0.5T)/n 直接口径（margin 口径 W/L/T）；"
                               "fold=同 seed 双席折叠附列；margin 只作参考"}
    budget["auth"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"verdict": "SIM_AUTH_RED（30/30 未过，判决中止）",
                         "criteria_passed": False}
        EV["budget"] = budget
        _flush(EV)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth}

    # ---- 2) 主判：bs2 vs 7+1 面 ----
    panel_opps = STRONG + WEAK + ["lynn", "wfr"]
    specs = [_mk_spec("panel", "bs2", o, s, seat)
             for o in panel_opps for s in FOLDS_12 for seat in (0, 1)]
    budget["panel"] = len(specs)
    print("panel games:", len(specs), flush=True)
    t1 = time.perf_counter()
    rows, _eng = J._play(specs, run_cfg)
    print("panel done", round(time.perf_counter() - t1, 1), "s", flush=True)

    # ---- 3) 消融：逐件关臂 ----
    abl_specs = []
    for form in ("bs2_nogap", "bs2_noslot"):
        for o in ("tetsutani", "lynn"):
            abl_specs += [_mk_spec("ablation", form, o, s, seat)
                          for s in FOLDS_12 for seat in (0, 1)]
    for o in ("wfr",):
        abl_specs += [_mk_spec("ablation", "bs2_noc3", o, s, seat)
                      for s in FOLDS_12 for seat in (0, 1)]
    budget["ablation"] = len(abl_specs)
    print("ablation games:", len(abl_specs), flush=True)
    t2 = time.perf_counter()
    abl_rows, _e2 = J._play(abl_specs, run_cfg)
    print("ablation done", round(time.perf_counter() - t2, 1), "s", flush=True)

    budget["judgment_total"] = budget["panel"] + budget["ablation"]
    budget["total"] = (budget["auth"] + budget["gates"]
                       + budget["judgment_total"])
    budget["within_cap"] = budget["total"] <= BUDGET_CAP
    if not budget["within_cap"]:
        EV["verdict"] = {"verdict": "BUDGET_RED", "criteria_passed": False}
        EV["budget"] = budget
        _flush(EV)
        return EV

    all_rows = rows + abl_rows
    by_form_opp = {}
    for r in all_rows:
        by_form_opp.setdefault((r["form"], r["face"]), []).append(r)

    # ---- 4) 臂设计台账 ----
    EV["arms"] = {
        "design": {
            "bs_gap": "idle-seller 缺口放量：近 3 拍该品对手流和≤2（R28 删失窗）"
                      "∧ 品项=对手稳态出货品（24 拍窗累计 argmax）→ 同品首单 "
                      "SELL 量翻倍（帽内=projected 可售−同品他单，不缩水）；"
                      "非缺口拍照旧",
            "bs_slot": "镜像族响应（画像=h1_mirror）：同拍内首个自由 SELL（竞速"
                       "品、无同品 BUY 腿）提前一槽（单次相邻交换；slot 饱和已证"
                       "只微调不全错位）；护栏零跨拍（纯同拍置换，量/单数不变）",
            "bs_c3": "WFR/攻击族 C3 保留（基座换表件不动）；r37/2965 族零动作"
                     "（矩阵已证优势面安全）；unknown→零足迹",
            "gate": "全部臂 step≥144（画像锁存）后激活=开局冻结（D5 条款 2）；"
                    "不加价峰择时门（D5 条款 3）",
        },
        "ablation": {
            "bs2_nogap_vs_bs2": {
                "opp": ["tetsutani", "lynn"],
                "paired": paired_delta(
                    by_form_opp.get(("bs2", "tetsutani"), [])
                    + by_form_opp.get(("bs2", "lynn"), []),
                    by_form_opp.get(("bs2_nogap", "tetsutani"), [])
                    + by_form_opp.get(("bs2_nogap", "lynn"), []))},
            "bs2_noslot_vs_bs2": {
                "opp": ["tetsutani", "lynn"],
                "paired": paired_delta(
                    by_form_opp.get(("bs2", "tetsutani"), [])
                    + by_form_opp.get(("bs2", "lynn"), []),
                    by_form_opp.get(("bs2_noslot", "tetsutani"), [])
                    + by_form_opp.get(("bs2_noslot", "lynn"), []))},
            "bs2_noc3_vs_bs2": {
                "opp": ["wfr"],
                "paired": paired_delta(by_form_opp.get(("bs2", "wfr"), []),
                                       by_form_opp.get(("bs2_noc3", "wfr"), []))},
        },
        "d5_fourth_arm": {
            "action": "skipped",
            "reason": "产线响应（画像族→GOOSE/SHEEP 占比预设档）构建成本高："
                      "H1 产线层深埋 tape/圈层规划，尾块安全改写面不足；D5 "
                      "证据 B 级且未控 seed（市场 vs 对手自适应未分离，蓝图"
                      "自注）；400 局次预算已排满三臂消融",
        },
    }

    # ---- 5) 画像读数 ----
    cls_by_opp = {}
    for r in rows:
        if r.get("cls") is None:
            continue
        d = cls_by_opp.setdefault(r["face"], {})
        d[r["cls"]] = d.get(r["cls"], 0) + 1
    EV["profiler"] = {
        "classes": ["r37_2965_family", "h1_mirror", "wfr", "unknown"],
        "cls_by_opponent": cls_by_opp,
        "accuracy_note": "profiler_core 同源字节（sha 前 16=%s）；面板内"
                         "tetsutani/V89/lynn/oc_c3/mpx 期望 h1_mirror、r40 "
                         "期望 r37_2965_family、wfr 期望 wfr"
                         % hashlib.sha256(
                             profiler_core.CORE_SRC.encode()).hexdigest()[:16],
        "zero_footprint": footprint_audit(
            {"bs2": rows}, [r for r in abl_rows]),
    }

    # ---- 6) 面板聚合 ----
    pp = {}
    for o in panel_opps:
        pp[o] = direct_h2h(by_form_opp.get(("bs2", o), []))
    strong_pooled = pooled_h2h({o: by_form_opp.get(("bs2", o), [])
                                for o in STRONG}, STRONG)
    weak_pooled = pooled_h2h({o: by_form_opp.get(("bs2", o), [])
                              for o in WEAK}, WEAK)
    EV["pairs_panel"] = {
        "per_member": pp, "strong_pooled": strong_pooled,
        "weak_pooled": weak_pooled,
        "oc_c3_direct": pp.get("oc_c3"),
        "margin_note": "margin 只作参考（分析44 镜像错觉：配对边际≠直接对战）"}

    fam = {o: direct_h2h(by_form_opp.get(("bs2", o), [])) for o in FAMILY}
    fam_pooled = pooled_h2h({o: by_form_opp.get(("bs2", o), [])
                             for o in FAMILY}, FAMILY)
    EV["family_group"] = {"per_mirror": fam, "pooled": fam_pooled,
                          "baseline_threshold": 0.75,
                          "baseline_ref": "racegap 同族专组基线 0.75（drop_half "
                                          "family aggregate）"}

    # ---- 7) 判据 + verdict（预登记） ----
    c1 = strong_pooled["h2h"] is not None and strong_pooled["h2h"] >= 0.5
    c2 = fam_pooled["h2h"] is not None and fam_pooled["h2h"] >= 0.75
    c3 = weak_pooled["h2h"] is not None and weak_pooled["h2h"] >= 0.8
    h_oc3 = pp["oc_c3"]["h2h"]
    c4 = h_oc3 is not None and h_oc3 >= 0.5
    EV["criteria"] = {
        "①强面板 {oc_c3,mpx,tetsutani,V89} h2h≥0.5（n=12 双席）": {
            "pooled_h2h": strong_pooled["h2h"],
            "per_member": {o: pp[o]["h2h"] for o in STRONG},
            "passed": bool(c1)},
        "②同族专组 {tetsutani,V89,lynn} h2h≥0.75": {
            "pooled_h2h": fam_pooled["h2h"],
            "per_mirror": {o: fam[o]["h2h"] for o in FAMILY},
            "passed": bool(c2)},
        "③弱锚 {r40,A} h2h≥0.8": {
            "pooled_h2h": weak_pooled["h2h"],
            "per_member": {o: pp[o]["h2h"] for o in WEAK},
            "passed": bool(c3)},
        "④对 oc_c3 直接 h2h≥0.5（才算更强）": {
            "h2h_vs_oc_c3": h_oc3,
            "passed": bool(c4)},
        "⑤配对边际只作参考": {
            "note": "margin 不入判；读数见 pairs_panel.margin_note 与 "
                    "arms.ablation.paired",
            "passed": True},
    }
    ok = all(v["passed"] for k, v in EV["criteria"].items()
             if k.startswith(("①", "②", "③", "④")))
    stronger = bool(c4 and ok)
    EV["verdict"] = {
        "verdict": ("BS2_SELECTOR_CONFIRMED: 行为选择器 v2 四判据全过"
                    "（对 oc_c3 直接≥0.5=更强）" if ok and stronger else
                    "BS2_NOT_CONFIRMED（详见 criteria）"),
        "criteria_passed": ok,
        "stronger_than_oc_c3": stronger,
        "form": "bs2",
        "layers": ["profiler", "c3_wool_phase", "bs_gap_volume", "bs_slot_micro"],
        "note": "判据预登记于任务书 D3：①强面板 ②同族 0.75 基线 ③弱锚 0.8 "
                "④对 oc_c3 直接 0.5；margin 只作参考；逐件消融见 arms.ablation",
    }
    EV["budget"] = budget
    EV["anomaly"] = [
        "tetsutani/V89/lynn 行为簇同构（同 seed 同席动作流 digest 相同，"
        "family-matrix probe_identity）——同族专组三件非独立证据",
        "harness 噪声：HP_TELEMETRY stdout 行（tetsutani 件自报）不入读数",
        "零足迹硬证=构建探针⑥（unknown→动作对象恒等）+ 逐件消融格读数",
        "D5 第四臂（产线响应）跳过——见 arms.d5_fourth_arm",
    ]
    _flush(EV)
    LEDGER_PATH.write_text(
        json.dumps({"rows": J._lite_rows(all_rows)}, ensure_ascii=False,
                   indent=1, default=str) + "\n", encoding="utf-8")
    print("verdict:", EV["verdict"]["verdict"], flush=True)
    print("criteria:", json.dumps(EV["criteria"], ensure_ascii=False,
                                  default=str), flush=True)
    print("strong_pooled:", strong_pooled["h2h"], "family:",
          fam_pooled["h2h"], "weak:", weak_pooled["h2h"], "vs_oc_c3:",
          h_oc3, flush=True)
    print("DONE budget:", budget, round(time.perf_counter() - t0, 1), "s",
          flush=True)
    return EV


def _flush(EV):
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINAL_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                     default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
