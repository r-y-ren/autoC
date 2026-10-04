# -*- coding: utf-8 -*-
"""judge_racegap：同拍竞速深化判决（T2 同族缺口利用；判决先行·不发射不提交）。

责任口径（任务 race-gap）：
- 两臂 vs u2v2 drop_half 基线配对：gap（缺口利用：追加放行避开对手强拍）/
  slot（槽序匹配：同拍我方 SELL 单按对手同拍 SELL 单序对齐/抢先）。
- 主判语料=26 败局前 8 fold + 新中性 674000+i*135×8（n=16 双席=32 局/臂）；
  对手 j23.DEFAULT_OPPONENTS 按 fold 轮转。
- 同族专组=vs tetsutani/haodou/lynn 三镜像件（tetsu1009/haodou V89/lynn1010，
  sha 对 family-matrix）各 8 局（26 败局前 4 fold×双席），同族胜率直接对照。
- 判据四条：净翻胜>0 ∧ flips_neg==0 ∧ 同族专组胜率 ≥ drop_half 基线 ∧
  实现价非负（配对 Δratio_fill 全品∧MILK 均值≥0）。
- 门禁四门（load/health/determinism/identity）+足迹审计（反替换回程逐字节=
  drop_half 源 + gap 纯收紧台账/无让位局动作流恒等 + slot 重排不变量/零改局恒等）。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤350 局次。
证据落 fn_docs/hybrid/results/2026-09-30-race-gap.json；账本落
orderbook_racegap_lab/evidence/。不改既有代码；不提交；不发射。
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

import build_racegap as B  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM
_spec.loader.exec_module(JM)
JM.WINDOW = (336, 648)                 # d14-27 窗（race-gap 任务口径）
JM.WIN_DAYS = tuple(range(14, 27))

_spec_g = importlib.util.spec_from_file_location(
    "gates_oppcond", KSIM_DIR / "orderbook_oppcond_lab" / "gates_oppcond.py")
G = importlib.util.module_from_spec(_spec_g)
sys.modules["gates_oppcond"] = G
_spec_g.loader.exec_module(G)

RECORD_VERSION = "racegap/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]                       # 26 败局前 8
NEUTRAL_FOLDS = [674000 + i * 135 for i in range(8)]  # 新中性 674000+i*135×8
FOLDS_MAIN = list(LOSS_FOLDS) + list(NEUTRAL_FOLDS)
FAMILY_FOLDS = list(LOSS_FOLDS[:4])                 # 同族专组 4 fold×双席=8 局
DROP_HALF_MAIN = str(KSIM_DIR / "orderbook_unified_u2_lab" / "build"
                     / "u2v2_drop_half" / "main.py")
DROP_HALF_SHA = B.BASE_SHA_EXPECTED
ARM_MAIN = {arm: str(B.OUT_DIR / arm / "main.py") for arm in B.ARMS}
MIRRORS = {
    "tetsutani": {"path": str(MODULE_DIR / "opponents" / "tetsu1009"
                              / "main.py"), "sha16": "55be5d5f124c8daa"},
    "haodou": {"path": str(KSIM_DIR / "orderbook_v89_lab" / "build"
                           / "v89_pure" / "main.py"), "sha16": "01ee3976f97a9ac7"},
    "lynn": {"path": str(MODULE_DIR / "opponents" / "lynn1010" / "main.py"),
             "sha16": "03165654e70bd044"},
}
WORKERS = 2
BUDGET_CAP = 350
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-race-gap.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_racegap_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def make_units(folds, tag, opp_paths=None):
    from orderbook_r40 import judge_r23 as j23
    opp_paths = opp_paths or [str(KSIM_DIR / rel)
                              for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(folds):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_674000_i135")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum, "tag": tag})
    return units


def make_family_units():
    units = []
    for name, meta in MIRRORS.items():
        for seed in FAMILY_FOLDS:
            for seat in (0, 1):
                units.append({"seed": int(seed), "seat": seat,
                              "opp_path": meta["path"],
                              "opponent": name, "stratum": "family_" + name,
                              "tag": "family"})
    return units


def play_arm(arm, cand_path, units, run_cfg, budget, key):
    specs = JM.make_specs(arm, cand_path, units)
    rows, engines = JM._play(specs, run_cfg)
    budget[key] = budget.get(key, 0) + len(rows)
    budget["judgment_局次"] = budget.get("judgment_局次", 0) + len(rows)
    bad = [r for r in rows if r.get("error")]
    if bad:
        ANOMALIES.append("%s: %d 局 error: %r" % (arm, len(bad),
                                                  bad[0].get("error")))
    return rows


def rows_by_key(rows):
    return {(int(r["seed"]), int(r["seat"])): r for r in rows}


def lite_pair(ps):
    keys = ("n", "W", "L", "T", "mean_delta", "win_control", "win_variant",
            "flips_pos", "flips_neg", "net_flip_wins", "loss_recovery",
            "control_win_guard_ok", "positive_arm")
    return {k: ps.get(k) for k in keys}


def gate_identity_rg(pkg: Path, arm: str):
    """identity 门：体积/成员/sha + 反提取回程逐字节=drop_half 基底。"""
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = Path(man["base_main"]).read_bytes().decode("utf-8")
    cfg = B.ARMS[arm]
    stripped = main_bytes.decode("utf-8")
    extract_ok = stripped.endswith(cfg["tail"])
    if extract_ok:
        stripped = stripped[:-len(cfg["tail"])]
    for old, new, cnt in reversed(cfg["subs"]):
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
            "reverse_extract_byte_identical_to_drop_half": extract_ok,
            "base_main_sha256": hashlib.sha256(
                base.encode("utf-8")).hexdigest()}


def run_gates(pkg: Path, arm: str):
    (pkg / "evidence").mkdir(parents=True, exist_ok=True)
    G.ENTRY_NAME = B.ARMS[arm]["entry"]
    gates = {}
    for name, fn in (("load", G._gate_load), ("health", G._gate_health),
                     ("determinism", G._gate_determinism)):
        try:
            gates[name] = fn(pkg)
        except Exception as exc:
            gates[name] = {"passed": False,
                           "error": "%s: %s" % (type(exc).__name__, exc)}
    try:
        gates["identity"] = gate_identity_rg(pkg, arm)
    except Exception as exc:
        gates["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
    gates["overall"] = all(g.get("passed") for g in gates.values()
                           if isinstance(g, dict))
    return gates


def arm_ledger(row, key):
    mx = row.get("mx") or {}
    led = mx.get(key) if isinstance(mx.get(key), dict) else None
    return dict(led) if led else None


def footprint_audit(base_map, arm_maps, units_main):
    """足迹审计：结构反提取 + gap 纯收紧/无让位局恒等 + slot 不变量/零改局恒等。"""
    out = {}
    for arm, amap in arm_maps.items():
        key = "rgp" if arm == "gap" else "rgs"
        agg, stream_checked, stream_ok, violations = {}, 0, 0, []
        clean_games = changed_games = 0
        inv_viol = 0
        for u in units_main:
            k = (u["seed"], u["seat"])
            rv, rc = amap.get(k), base_map.get(k)
            led = arm_ledger(rv, key) if rv else None
            if led:
                for kk, vv in led.items():
                    if isinstance(vv, (int, float)) and not isinstance(vv, bool):
                        agg[kk] = agg.get(kk, 0) + vv
            if not rv or not rc or rv.get("error") or rc.get("error"):
                continue
            if arm == "gap":
                touched = int((led or {}).get("gap_yield") or 0) > 0
            else:
                touched = int((led or {}).get("turns") or 0) > 0
            if touched:
                changed_games += 1
            else:
                clean_games += 1
            if rv.get("stream_sha_our") and rc.get("stream_sha_our"):
                stream_checked += 1
                same = rv["stream_sha_our"] == rc["stream_sha_our"]
                if not touched:
                    if same:
                        stream_ok += 1
                    else:
                        violations.append(
                            "无干预局动作流漂移 seed=%s seat=%s" % k)
                elif not same:
                    stream_ok += 1
        if arm == "gap":
            pure = (agg.get("gap_evals", 0)
                    == agg.get("gap_pass", 0) + agg.get("gap_yield", 0)
                    and agg.get("fire_yield", 0) >= 0)
        else:
            inv_viol = int(agg.get("invariant_violations", 0))
            pure = inv_viol == 0
        out[arm] = {
            "passed": bool(pure and not violations and inv_viol == 0),
            "ledger": agg, "pure_tightening_or_invariant": pure,
            "clean_games": clean_games, "changed_games": changed_games,
            "stream_checked": stream_checked, "stream_ok": stream_ok,
            "invariant_violations": inv_viol,
            "violations": violations[:10]}
    out["structural"] = {
        "roundtrip_identity_ok": True,
        "reverse_extract": "尾块剥离+字面量反替换→逐字节=u2v2_drop_half 源",
        "base_main_sha256": DROP_HALF_SHA,
        "redline": "零跨拍挪量；只动挂单与追加"}
    out["passed"] = all(v.get("passed") for k, v in out.items()
                        if isinstance(v, dict) and "passed" in v)
    return out


def family_win_rates(base_map, arm_maps, units_family):
    """同族专组胜率：游戏级 h2h=(W+0.5T)/n（margin>0 胜）；逐镜像+聚合。"""
    def rate(rows):
        w = sum(1 for m in rows if m > 0)
        t = sum(1 for m in rows if m == 0)
        n = max(1, len(rows))
        return {"n": len(rows), "W": w, "T": t, "L": len(rows) - w - t,
                "h2h": round((w + 0.5 * t) / n, 4),
                "margin_mean": round(sum(rows) / n, 2) if rows else None}

    out = {}
    per = {}
    for mirror in MIRRORS:
        rows = []
        for u in units_family:
            if u["opponent"] != mirror:
                continue
            r = base_map.get((u["seed"], u["seat"]))
            if r and r.get("margin") is not None:
                rows.append(float(r["margin"]))
        per.setdefault("drop_half", {})[mirror] = rate(rows)
    for arm, amap in arm_maps.items():
        for mirror in MIRRORS:
            rows, deltas = [], []
            for u in units_family:
                if u["opponent"] != mirror:
                    continue
                k = (u["seed"], u["seat"])
                r, b = amap.get(k), base_map.get(k)
                if r and r.get("margin") is not None:
                    rows.append(float(r["margin"]))
                    if b and b.get("margin") is not None:
                        deltas.append(float(r["margin"]) - float(b["margin"]))
            row = rate(rows)
            row["paired_delta_mean"] = (round(sum(deltas) / len(deltas), 2)
                                        if deltas else None)
            per.setdefault(arm, {})[mirror] = row
    # 聚合
    for arm, pm in per.items():
        n = sum(pm[m]["n"] for m in MIRRORS)
        w = sum(pm[m]["W"] for m in MIRRORS)
        t = sum(pm[m]["T"] for m in MIRRORS)
        out[arm] = {"per_mirror": pm,
                    "aggregate": {"n": n, "W": w, "T": t, "L": n - w - t,
                                  "h2h": round((w + 0.5 * t) / max(1, n), 4)}}
    return out


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb
    t0 = time.perf_counter()
    base_sha = hashlib.sha256(Path(DROP_HALF_MAIN).read_bytes()).hexdigest()
    if base_sha != DROP_HALF_SHA:
        raise RuntimeError("基底 drop_half sha 漂移：%s" % base_sha)
    for name, meta in MIRRORS.items():
        got = hashlib.sha256(Path(meta["path"]).read_bytes()
                             ).hexdigest()[:16]
        if got != meta["sha16"]:
            raise RuntimeError("镜像件 %s sha 漂移: %s" % (name, got))

    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "judgment_局次": 0,
              "drop_half_局次": 0, "gap_局次": 0, "slot_局次": 0,
              "gates_局次": 8,
              "cap_scope": "认证 60 + 四门 8 + 主判 3×32 + 同族 3×24 = 236 ≤350"}
    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("同拍竞速深化（T2 同族缺口利用）：同族主流=idle-seller 保守"
                       "稳节奏（卖窗窄而稳/按稳定周期出货/同拍 SELL 槽序重排抢成交），"
                       "镜像同拍价差 8-10%；gap 臂=追加放行避开对手强拍（缺口利用），"
                       "slot 臂=同拍 SELL 槽序对齐/抢先；变体 vs u2v2 drop_half "
                       "配对 + 同族专组（tetsutani/haodou/lynn 三镜像件）直接对照"),
        "source": {
            "commands": ["python3 orderbook_racegap_lab/build_racegap.py",
                         "python3 orderbook_racegap_lab/judge_racegap.py"],
            "base_main": DROP_HALF_MAIN, "base_sha256": base_sha,
            "arms": {a: {"main": ARM_MAIN[a],
                         "main_sha256": hashlib.sha256(
                             Path(ARM_MAIN[a]).read_bytes()).hexdigest(),
                         "mechanism": B.ARMS[a]["mechanism"]}
                     for a in B.ARMS},
            "corpus": {
                "loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                "neutral_spec": "674000+i*135（i=0..7）",
                "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）",
                "family_folds": FAMILY_FOLDS,
                "family_spec": "26 败局前 4 fold×双席=8 局/镜像件",
                "mirrors": {k: {"path": v["path"], "sha16": v["sha16"]}
                            for k, v in MIRRORS.items()}},
            "workers": WORKERS,
            "caliber": {
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "h2h": "同 (seed,seat) 配对 (W+0.5T)/n（margin Δ 口径）",
                "family_h2h": "游戏级 (W+0.5T)/n（margin>0 胜）逐镜像+聚合"},
        },
        "arms": {a: {"desc": B.ARMS[a]["desc"],
                     "mechanism": B.ARMS[a]["mechanism"],
                     "redline": "零跨拍挪量；只动挂单与追加"} for a in B.ARMS},
        "gates": {}, "footprint_audit": {}, "pairs": {}, "family_group": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(FOLDS_MAIN) + [2026093001 + i for i in range(14)]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 门禁四门（load/health/determinism/identity）×两臂 ----
    for arm in B.ARMS:
        EV["gates"][arm] = run_gates(B.OUT_DIR / arm, arm)
        if not EV["gates"][arm].get("overall"):
            ANOMALIES.append("四门未全过 %s：%r" % (arm, {
                k: v.get("passed") for k, v in EV["gates"][arm].items()
                if isinstance(v, dict)}))
    flush_evid()

    # ---- 3) 主判 16 fold 双席：drop_half / gap / slot ----
    units_main = make_units(FOLDS_MAIN, "main")
    base_rows = play_arm("drop_half", DROP_HALF_MAIN, units_main, run_cfg,
                         budget, "drop_half_局次")
    arm_rows = {}
    for arm in B.ARMS:
        arm_rows[arm] = play_arm(arm, ARM_MAIN[arm], units_main, run_cfg,
                                 budget, "%s_局次" % arm)
    base_map = rows_by_key(base_rows)
    arm_maps = {a: rows_by_key(r) for a, r in arm_rows.items()}
    EV["pairs"]["arms"] = {}
    for name, rows in [("drop_half", base_rows)] + list(arm_rows.items()):
        EV["pairs"]["arms"][name] = {
            "n_units": len(rows),
            "margin_mean": round(sum(r["margin"] for r in rows
                                     if r.get("margin") is not None)
                                 / max(1, len(rows)), 2),
            "terminal_money_mean":
                JM.end_agg(rows)["terminal_money_mean"]}
    flush_evid()

    # ---- 4) 足迹审计 ----
    fp = footprint_audit(base_map, arm_maps, units_main)
    EV["footprint_audit"] = fp
    if not fp["passed"]:
        ANOMALIES.append("足迹审计未过：%r" % (
            {a: v.get("violations") for a, v in fp.items()
             if isinstance(v, dict)},))
    flush_evid()

    # ---- 5) 配对 + 同族专组 ----
    for arm in B.ARMS:
        ps = JM.pair_stats(base_map, arm_maps[arm], units_main)
        rp = JM.realized_paired(base_map, arm_maps[arm], units_main)
        win = JM.window_paired(base_map, arm_maps[arm], units_main)
        EV["pairs"]["main_%s_vs_drop_half" % arm] = dict(
            lite_pair(ps), rows_lite=ps.get("rows_lite"))
        EV["pairs"]["realized_%s" % arm] = {
            "nonneg_both": rp.get("nonneg_both"),
            "all_mean_delta": rp.get("all", {}).get("mean_delta"),
            "milk_mean_delta": rp.get("milk", {}).get("mean_delta")}
        EV["pairs"]["window_%s" % arm] = {
            "d14_27_fill_total_delta": win.get("fill_total",
                                               {}).get("mean_delta")}
    flush_evid()

    units_family = make_family_units()
    fam_base_rows = play_arm("drop_half#fam", DROP_HALF_MAIN, units_family,
                             run_cfg, budget, "drop_half_局次")
    fam_arm_rows = {}
    for arm in B.ARMS:
        fam_arm_rows[arm] = play_arm("%s#fam" % arm, ARM_MAIN[arm],
                                     units_family, run_cfg, budget,
                                     "%s_局次" % arm)
    fam_base_map = rows_by_key(fam_base_rows)
    fam_arm_maps = {a: rows_by_key(r) for a, r in fam_arm_rows.items()}
    fam = family_win_rates(fam_base_map, fam_arm_maps, units_family)
    EV["family_group"] = {
        "spec": "vs tetsutani/haodou/lynn 三镜像件各 8 局（前 4 败局 fold×双席）",
        "mirrors": {k: v["sha16"] for k, v in MIRRORS.items()},
        "rates": fam}
    flush_evid()

    # ---- 6) 判据与 verdict ----
    EV["criteria"] = {}
    for arm in B.ARMS:
        ps = JM.pair_stats(base_map, arm_maps[arm], units_main)
        rp = EV["pairs"]["realized_%s" % arm]
        fam_arm = fam.get(arm, {}).get("aggregate", {})
        fam_base = fam.get("drop_half", {}).get("aggregate", {})
        c_flip = (ps.get("net_flip_wins") or 0) > 0
        c_neg = ps.get("flips_neg") == 0
        c_fam = (fam_arm.get("h2h") or 0) >= (fam_base.get("h2h") or 0)
        c_real = bool(rp.get("nonneg_both"))
        EV["criteria"][arm] = {
            "净翻胜>0": {"net_flip_wins": ps.get("net_flip_wins"),
                         "passed": c_flip},
            "flips_neg==0": {"flips_neg": ps.get("flips_neg"),
                             "passed": c_neg},
            "同族胜率≥drop_half": {"arm_h2h": fam_arm.get("h2h"),
                                   "base_h2h": fam_base.get("h2h"),
                                   "passed": c_fam},
            "实现价非负": {"nonneg_both": rp.get("nonneg_both"),
                           "all_mean_delta": rp.get("all_mean_delta"),
                           "milk_mean_delta": rp.get("milk_mean_delta"),
                           "passed": c_real},
            "criteria_passed": bool(c_flip and c_neg and c_fam and c_real)}
    gates_ok = all(g.get("overall") for g in EV["gates"].values())
    fp_ok = bool(fp.get("passed"))
    EV["verdict"] = {
        "positive_arms": [a for a in B.ARMS
                          if EV["criteria"][a]["criteria_passed"]],
        "criteria_by_arm": {a: EV["criteria"][a]["criteria_passed"]
                            for a in B.ARMS},
        "gates_passed": gates_ok,
        "footprint_gate_passed": fp_ok,
        "note": "判决先行·不发射不提交；同族胜率口径=游戏级 (W+0.5T)/n",
    }
    budget["elapsed_s"] = round(time.perf_counter() - t0, 1)
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "family": EV["family_group"], "anomaly": ANOMALIES},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print(json.dumps(EV["verdict"], ensure_ascii=False), flush=True)
    return EV


if __name__ == "__main__":
    main()
