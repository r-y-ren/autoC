# -*- coding: utf-8 -*-
"""judge_unified_u2v2：U2v2 软门判决（择优或全试；判决先行·不发射不提交）。

责任口径（任务 unified-u2 v2）：
- 软门形态：①容差门 tol=1%/3% 两档（p_now ≥ max(投影K=6)×(1−tol)）；
  ②跌幅门 drop_half（Wangyh666 形态：跌>$0.5 半量放行而非全拦）/
  drop1_block（字面：仅跌>$1 才拦）——两形态全试，择优作第三臂。
- 主判=各形态 vs mpx 胜者件配对（同 (seed,seat) 双席）；语料=26 败局前 8
  fold + 新中性 673000+i*127×8（n=16 双席=32 局/臂）。
- 判据沿四条：h2h vs mpx ≥0.55 ∧ flips_neg==0 ∧ 实现价非负 ∧ 窗差 ≥ mpx；
  +胜率口径附注（R27 重裁先例：胜率≥0.6 但钱面刀口级未达 → 单独标注）。
- sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤250 局次；
  终局钱 farms[obs.player]；margin=banks[our]−banks[opp]。
证据并入 fn_docs/hybrid/results/2026-09-30-unified-u2.json 的 v2 节；
账本落 orderbook_unified_u2_lab/evidence/。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

import build_unified_u2v2 as B2  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_unified_u2", MODULE_DIR / "judge_unified_u2.py")
J = importlib.util.module_from_spec(_spec)
sys.modules["judge_unified_u2"] = J
_spec.loader.exec_module(J)
JM = J.JM                                   # WINDOW 已置 d14-27（336,648）
G = J.G
G.ENTRY_NAME = "_u2_agent"

RECORD_VERSION = "unified-u2-v2/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]
NEUTRAL_FOLDS = [673000 + i * 127 for i in range(8)]   # 新中性 673000+i*127×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
               / "main.py")
MPX_SHA = B2.BASE_SHA_EXPECTED
FORMS = list(B2.FORMS)
WORKERS = 2
BUDGET_CAP = 250
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-unified-u2.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_u2v2_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        merged = json.loads(EVID_PATH.read_text(encoding="utf-8"))
    except Exception:
        merged = {}
    merged["v2"] = EV
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def make_units(folds):
    from orderbook_r40 import judge_r23 as j23
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(folds):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_673000_i127")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum, "tag": "all"})
    return units


def gate_identity_v2(pkg: Path, form: str):
    """identity 门：体积/成员/sha + 反提取回程逐字节=mpx 胜者件。"""
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = Path(man["base_main"]).read_bytes().decode("utf-8")
    tail = B2.TAIL_TMPL.replace("__U2_MODE__",
                                str(B2.FORMS[form]["mode"])) \
        .replace("__U2_TOL__", repr(float(B2.FORMS[form]["tol"])))
    stripped = main_bytes.decode("utf-8")
    extract_ok = stripped.endswith(tail)
    if extract_ok:
        stripped = stripped[:-len(tail)]
    for old, new, cnt in reversed(B2.SUBS):
        if stripped.count(new) != cnt:
            extract_ok = False
            break
        stripped = stripped.replace(new, old)
    extract_ok = extract_ok and stripped == base
    sha_ok = (main_sha == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest()
              == man.get("tar_sha256"))
    ok = all([len(tar_bytes) < 100 * 1024 * 1024, members == ["main.py"],
              inner == main_bytes, sha_ok, extract_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_members": members, "inner_matches_disk": inner == main_bytes,
            "sha_matches_manifest": sha_ok,
            "reverse_extract_byte_identical_to_mpx_base": extract_ok,
            "base_main_sha256": hashlib.sha256(
                base.encode("utf-8")).hexdigest()}


def run_gates(pkg: Path, form: str):
    gates = {}
    for name, fn in (("load", G._gate_load), ("health", G._gate_health),
                     ("determinism", G._gate_determinism)):
        try:
            gates[name] = fn(pkg)
        except Exception as exc:
            gates[name] = {"passed": False,
                           "error": "%s: %s" % (type(exc).__name__, exc)}
    try:
        gates["identity"] = gate_identity_v2(pkg, form)
    except Exception as exc:
        gates["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
    gates["overall"] = all(g.get("passed") for g in gates.values()
                           if isinstance(g, dict))
    return gates


def u2_ledger(row):
    mx = row.get("mx") or {}
    u2 = mx.get("u2") if isinstance(mx.get("u2"), dict) else None
    return dict(u2) if u2 else None


def footprint_audit(mpx_map, var_map, units):
    """足迹审计：门台账纯收紧/量整形只在触发拍 + 无干预局动作流恒等 mpx。"""
    keys = ("calls", "gate_calls", "base_fires", "gate_pass", "gate_blocked",
            "gate_err", "post648_pass", "fires", "half_fires")
    agg = {k: 0 for k in keys}
    stream_checked = stream_ok = 0
    violations = []
    for u in units:
        key = (u["seed"], u["seat"])
        rv, rc = var_map.get(key), mpx_map.get(key)
        led = u2_ledger(rv) if rv else None
        if led:
            for k in keys:
                agg[k] += int(led.get(k) or 0)
        if not rv or not rc or rv.get("error") or rc.get("error"):
            continue
        blocked = int((led or {}).get("gate_blocked") or 0)
        half = int((led or {}).get("half_fires") or 0)
        if rv.get("stream_sha_our") and rc.get("stream_sha_our"):
            stream_checked += 1
            same = rv["stream_sha_our"] == rc["stream_sha_our"]
            if blocked == 0 and half == 0:
                if same:
                    stream_ok += 1
                else:
                    violations.append("无干预局动作流漂移 seed=%s seat=%s" % key)
            elif not same:
                stream_ok += 1
    pure = (agg["gate_pass"] + agg["gate_blocked"] == agg["base_fires"]
            and agg["fires"] == agg["gate_pass"])
    return {"passed": bool(pure and not violations),
            "gate_ledger": agg, "pure_restriction": pure,
            "stream_checked": stream_checked, "stream_ok": stream_ok,
            "violations": violations[:10]}


def evaluate(ps, rp, win):
    n = max(1, int(ps.get("n") or 0))
    h2h = round((ps.get("W", 0) + 0.5 * ps.get("T", 0)) / n, 4)
    c = {
        "h2h_vs_mpx≥0.55": {"h2h": h2h, "W": ps.get("W"), "T": ps.get("T"),
                            "L": ps.get("L"), "passed": h2h >= 0.55},
        "flips_neg==0": {"flips_neg": ps.get("flips_neg"),
                         "passed": ps.get("flips_neg") == 0},
        "实现价非负": {"nonneg_both": rp.get("nonneg_both"),
                       "all_mean_delta": rp.get("all", {}).get("mean_delta"),
                       "milk_mean_delta": rp.get("milk", {}).get("mean_delta"),
                       "passed": bool(rp.get("nonneg_both"))},
        "窗差≥mpx": {"d14_27_fill_total_delta": win.get(
            "fill_total", {}).get("mean_delta"),
            "passed": (win.get("fill_total", {}).get("mean_delta") or 0) >= 0},
    }
    passed = all(v["passed"] for v in c.values())
    note = None
    if h2h >= 0.6 and not passed:
        money_fail = [k for k in ("实现价非负", "窗差≥mpx") if not c[k]["passed"]]
        note = ("胜率口径附注（R27 重裁先例）：h2h=%.4f≥0.6 但钱面刀口级未达"
                "（%s），胜率是天梯硬通货，单独标注供裁决"
                % (h2h, "、".join(money_fail)))
    return {"criteria": c, "criteria_passed": passed, "h2h": h2h,
            "win_rate_note": note}


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb
    t0 = time.perf_counter()
    base_sha = hashlib.sha256(Path(MPX_MAIN).read_bytes()).hexdigest()
    if base_sha != MPX_SHA:
        raise RuntimeError("基底 mpx 胜者件 sha 漂移：%s" % base_sha)

    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "judgment_局次": 0,
              "mpx_局次": 0, "gates_局次": 0,
              "cap_scope": "全部局次（认证 60 + 四门 4×形态 + 判决 32×臂）≤250"}
    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("U2v2 软门版（U2 硬门 h2h 0.656 正信号、钱面被锋利门拖负）"
                       "：①容差门 tol 1%/3% 两档；②跌幅门 drop_half（Wangyh666"
                       " 形态：跌>$0.5 半量放行而非全拦）/drop1_block（仅跌>$1 "
                       "才拦）全试择优；主判各形态 vs mpx 胜者件，判据沿四条+"
                       "胜率口径附注"),
        "source": {
            "commands": ["python3 orderbook_unified_u2_lab/build_unified_u2v2.py",
                         "python3 orderbook_unified_u2_lab/judge_unified_u2v2.py"],
            "base_main": MPX_MAIN, "base_sha256": base_sha,
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*127（i=0..7）",
                       "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）"},
            "workers": WORKERS,
            "caliber": {
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-27 窗 step 336-648；fill=影子引擎逐拍归因",
                "h2h": "同 (seed,seat) 配对 (W+0.5T)/n（margin Δ 口径）"},
        },
        "gate_design": B2.GATE_DESIGN,
        "forms": {f: B2.FORMS[f] for f in FORMS},
        "gates": {}, "footprint_audit": {}, "pairs": {}, "window_stats": {},
        "criteria": {}, "win_rate_notes": {}, "verdict": {}, "budget": budget,
    })

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(LOSS_FOLDS) + list(NEUTRAL_FOLDS) + \
        [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
         2026093006, 2026093007, 2026093008, 2026093009, 2026093010,
         2026093011, 2026093012, 2026093013, 2026093014]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" /
                            "sim_auth_record_v2.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 四门 × 形态 ----
    for form in FORMS:
        gates = run_gates(MODULE_DIR / "build" / form, form)
        EV["gates"][form] = gates
        budget["gates_局次"] += 4
        if not gates.get("overall"):
            ANOMALIES.append("%s 四门未全过：%r" % (
                form, {k: v.get("passed") for k, v in gates.items()
                       if isinstance(v, dict)}))
    flush_evid()

    # ---- 3) 对照 mpx + 形态臂 ----
    units_all = make_units(FOLDS_ALL)
    specs = JM.make_specs("mpx", MPX_MAIN, units_all)
    mpx_rows, _ = JM._play(specs, run_cfg)
    budget["mpx_局次"] += len(mpx_rows)
    budget["judgment_局次"] += len(mpx_rows)
    bad = [r for r in mpx_rows if r.get("error")]
    if bad:
        ANOMALIES.append("mpx: %d 局 error: %r" % (len(bad), bad[0].get("error")))
    mpx_map = J.rows_by_key(mpx_rows)
    form_rows, form_maps = {}, {}
    for form in FORMS:
        path = str(MODULE_DIR / "build" / form / "main.py")
        rows, _ = JM._play(JM.make_specs(form, path, units_all), run_cfg)
        budget["judgment_局次"] += len(rows)
        budget.setdefault(form + "_局次", 0)
        budget[form + "_局次"] += len(rows)
        bad = [r for r in rows if r.get("error")]
        if bad:
            ANOMALIES.append("%s: %d 局 error: %r"
                             % (form, len(bad), bad[0].get("error")))
        form_rows[form] = rows
        form_maps[form] = J.rows_by_key(rows)
    flush_evid()

    # ---- 4) 足迹审计 + 配对 + 判据 ----
    results = {}
    for form in FORMS:
        fp = footprint_audit(mpx_map, form_maps[form], units_all)
        EV["footprint_audit"][form] = fp
        if not fp["passed"]:
            ANOMALIES.append("%s 足迹审计未过：%r" % (form, fp["violations"]))
        ps = JM.pair_stats(mpx_map, form_maps[form], units_all)
        rp = JM.realized_paired(mpx_map, form_maps[form], units_all)
        win = JM.window_paired(mpx_map, form_maps[form], units_all)
        ev = evaluate(ps, rp, win)
        results[form] = {"pair": J.lite_pair(ps),
                         "rows_lite": ps.get("rows_lite"),
                         "window": J.win_lite(win),
                         "realized": {"nonneg_both": rp.get("nonneg_both"),
                                      "all": rp.get("all", {}).get("mean_delta"),
                                      "milk": rp.get("milk", {}).get(
                                          "mean_delta")},
                         "eval": ev,
                         "terminal_money_mean":
                             JM.end_agg(form_rows[form])["terminal_money_mean"],
                         "margin_mean": round(
                             sum(r["margin"] for r in form_rows[form]
                                 if r.get("margin") is not None)
                             / max(1, len(form_rows[form])), 2)}
        EV["pairs"][form] = {k: results[form][k] for k in
                             ("pair", "window", "realized", "margin_mean",
                              "terminal_money_mean")}
        EV["criteria"][form] = ev["criteria"]
        if ev["win_rate_note"]:
            EV["win_rate_notes"][form] = ev["win_rate_note"]
        print(form, "h2h", ev["h2h"], "dM", results[form]["pair"]["mean_delta"],
              "pass", ev["criteria_passed"], flush=True)
    EV["pairs"]["mpx_control"] = {
        "n_units": len(mpx_rows),
        "margin_mean": round(sum(r["margin"] for r in mpx_rows
                                 if r.get("margin") is not None)
                             / max(1, len(mpx_rows)), 2),
        "terminal_money_mean": JM.end_agg(mpx_rows)["terminal_money_mean"]}

    # ---- 5) 跌幅族择优 + verdict ----
    drop_forms = [f for f in FORMS if f.startswith("u2v2_drop")]

    def drop_score(f):
        ev = results[f]["eval"]
        return (sum(1 for v in ev["criteria"].values() if v["passed"]),
                ev["h2h"], results[f]["pair"].get("mean_delta") or -1e18)
    drop_best = max(drop_forms, key=drop_score)
    tol_best = max([f for f in FORMS if "tol" in f],
                   key=lambda f: drop_score(f))
    three_arm = ["u2v2_tol1", "u2v2_tol3", drop_best]
    EV["verdict"] = {
        "three_arm_table": three_arm,
        "drop_arm_selected": {"form": drop_best,
                              "desc": B2.FORMS[drop_best]["desc"],
                              "selection": "跌幅族两形态全试择优（判据过数→h2h"
                                           "→mean_delta）",
                              "other": {f: {
                                  "criteria_passed":
                                      results[f]["eval"]["criteria_passed"],
                                  "h2h": results[f]["eval"]["h2h"],
                                  "mean_delta": results[f]["pair"].get(
                                      "mean_delta")}
                                  for f in drop_forms if f != drop_best}},
        "tol_arm_selected": tol_best,
        "per_form": {f: {
            "criteria_passed": results[f]["eval"]["criteria_passed"],
            "h2h": results[f]["eval"]["h2h"],
            "mean_delta_vs_mpx": results[f]["pair"].get("mean_delta"),
            "flips_neg": results[f]["pair"].get("flips_neg"),
            "d14_27_fill_total_delta": results[f]["window"].get("fill_total"),
            "win_rate_note": results[f]["eval"]["win_rate_note"]}
            for f in FORMS},
        "positive_arm": any(results[f]["eval"]["criteria_passed"]
                            for f in FORMS),
        "launch": "不发射不提交（判决先行）；上线决策移交用户"}
    budget["total_局次"] = (budget["auth_局次"] + budget["gates_局次"]
                            + budget["judgment_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget,
         "per_form": {f: {"pair": results[f]["pair"],
                          "eval": results[f]["eval"]} for f in FORMS}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
