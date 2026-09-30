# -*- coding: utf-8 -*-
"""judge_day2526：d25/26 窗内整形特调判决（vs drop_half 配对；判决先行·
不发射不提交）。

责任口径（任务 day2526-T1）：
- 修复臂（≤2，按 forensics 根因=半量整形 d25/26 产线窗扰动实现价/跨日节奏）：
  ①d2526_milkpass（窗内 MILK 特定品放行）②d2526_h70（窗内半量 50%→70%）。
- 主判=各臂 vs drop_half（sha 5d2d1246…）配对（同 (seed,seat) 双席）；
  语料=26 败局前 8 fold + 新中性 674000+i*133×8（n=16 双席=32 局/臂）。
- 判据（预登记四项）：净翻胜>0 ∧ flips_neg==0 ∧ d25/26 单日差转正（逐日
  fill 配对 Δ>0；d25=step 600-623、d26=step 624-647，step//24 口径=原 −33.6
  凹陷日；任务窗 576-624（d24+d25）合并差另报）∧ 实现价非负（配对 Δratio_fill
  全品∧MILK 均值≥0）。
- 等价封印：d2526_neutral（mode=off）vs drop_half 同 (seed,seat) 动作流 digest
  全等 + 终局钱相等（参数级手术行为保真）。
- sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤250 局次；
  读数：终局钱 farms[obs.player]；margin=banks[our]−banks[opp]。
证据并入 fn_docs/hybrid/results/2026-09-30-day2526.json（variants/pairs/
day_stats/criteria/verdict/anomaly）；账本落 orderbook_day2526_lab/evidence/。
不改既有代码；不提交；不发射。
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
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
import day2526_common as C  # noqa: E402
import build_day2526 as B  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM
_spec.loader.exec_module(JM)

# d14-27 窗（step 336-648）；逐日=step//24（14..26）
JM.WINDOW = (336, 648)
JM.WIN_DAYS = tuple(range(14, 27))

from orderbook_r40 import sim_bridge as sb  # noqa: E402
from orderbook_r40 import judge_r23 as j23  # noqa: E402

RECORD_VERSION = "day2526-judge/1.0"
LOSS_FOLDS = list(C.LOSS_FOLDS)
NEUTRAL_FOLDS = [674000 + i * 133 for i in range(8)]   # 新中性 674000+i*133×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS
CONTROL = "drop_half"
CONTROL_MAIN = C.DROP_HALF_MAIN
ARMS = ("d2526_milkpass", "d2526_h70")
SEAL_FORM = "d2526_neutral"
WORKERS = 2
BUDGET_CAP = 250
D25_KEY, D26_KEY = "25", "26"          # step 600-623 / 624-647（原 −33.6 日）

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = sorted(set(ANOMALIES))
    EV["_generated_at"] = C.now()
    C.EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged = {}
    if C.EVID_PATH.exists():
        try:
            merged = json.loads(C.EVID_PATH.read_text(encoding="utf-8"))
        except Exception:
            merged = {}
    merged.update(EV)
    C.EVID_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


def make_units():
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS_ALL):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_674000_i133")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum})
    return units


def rows_by_key(rows):
    return {(int(r["seed"]), int(r["seat"])): r for r in rows}


def play(arm, path, units, run_cfg, budget, key):
    specs = JM.make_specs(arm, path, units)
    rows, engines = JM._play(specs, run_cfg)
    budget[key] = budget.get(key, 0) + len(rows)
    budget["judgment_局次"] = budget.get("judgment_局次", 0) + len(rows)
    bad = [r for r in rows if r.get("error")]
    for r in bad[:3]:
        ANOMALIES.append("%s: seed=%s seat=%s error=%r"
                         % (arm, r.get("seed"), r.get("seat"),
                            r.get("error")))
    return rows


def identity_gate(pkg: Path):
    """identity 门：体积/成员/sha + 反提取回程逐字节=drop_half 基底。"""
    out = {}
    for form in list(ARMS) + [SEAL_FORM]:
        d = pkg / form
        main_bytes = (d / "main.py").read_bytes()
        tar_bytes = (d / "submission.tar.gz").read_bytes()
        man = json.loads((d / "build_manifest.json").read_text(
            encoding="utf-8"))
        main_sha = hashlib.sha256(main_bytes).hexdigest()
        import io as _io
        import tarfile as _tarfile
        with _tarfile.open(fileobj=_io.BytesIO(tar_bytes), mode="r:gz") as tar:
            members = tar.getnames()
            inner = tar.extractfile("main.py").read()
        stripped = main_bytes.decode("utf-8")
        tail = B.TAIL_TMPL.replace("__D2526_MODE__",
                                   str(B.FORMS[form]["mode"])) \
            .replace("__D2526_RATIO__", repr(float(B.FORMS[form]["ratio"])))
        extract_ok = stripped.endswith(tail)
        if extract_ok:
            stripped = stripped[:-len(tail)]
        for old, new, cnt in reversed(B.SUBS):
            if stripped.count(new) != cnt:
                extract_ok = False
                break
            stripped = stripped.replace(new, old)
        extract_ok = extract_ok and stripped.encode("utf-8") == \
            Path(man["base_main"]).read_bytes()
        sha_ok = (main_sha == man.get("main_sha256")
                  and hashlib.sha256(tar_bytes).hexdigest()
                  == man.get("tar_sha256"))
        ok = all([len(tar_bytes) < 100 * 1024 * 1024, members == ["main.py"],
                  inner == main_bytes, sha_ok, extract_ok])
        out[form] = {"overall": bool(ok), "sha_ok": bool(sha_ok),
                     "roundtrip_ok": bool(extract_ok),
                     "main_sha256": main_sha}
        if not ok:
            ANOMALIES.append("identity 门未过: %s" % form)
    out["overall"] = all(v.get("overall") for k, v in out.items()
                         if isinstance(v, dict))
    return out


def lite_pair(ps):
    keys = ("n", "W", "L", "T", "mean_delta", "win_control", "win_variant",
            "flips_pos", "flips_neg", "net_flip_wins", "loss_recovery",
            "control_win_guard_ok", "positive_arm")
    return {k: ps.get(k) for k in keys}


def main():
    t0 = time.time()
    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "seal_局次": 0,
              "judgment_局次": 0}

    # ---- 0) 构建 + identity 门 ----
    base_bytes = Path(B.BASE_MAIN).read_bytes()
    if hashlib.sha256(base_bytes).hexdigest() != B.BASE_SHA_EXPECTED:
        raise RuntimeError("基底 drop_half sha 漂移")
    for form, cfg in B.FORMS.items():
        B.build_one(form, cfg, base_bytes)
    gates = identity_gate(MODULE_DIR / "build")

    EV.update({
        "version": RECORD_VERSION,
        "experiment": "d25/26 单日凹陷修复判决：窗内整形特调两臂（MILK 特定"
                      "品放行 / 半量 50%→70%）vs drop_half 配对；根因=半量整形"
                      "在 MILK/WOOL 产线窗扰动实现价与跨日节奏（判决先行·不发射"
                      "不提交）",
        "source": {
            "commands": ["python3 judge_day2526.py"],
            "control": {"arm": CONTROL, "main": CONTROL_MAIN,
                        "sha256": hashlib.sha256(
                            Path(CONTROL_MAIN).read_bytes()).hexdigest()},
            "corpus": {
                "loss_folds": LOSS_FOLDS,
                "neutral_folds": NEUTRAL_FOLDS,
                "neutral_spec": "674000+i*133（i=0..7）",
                "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）"},
            "opponents": j23.DEFAULT_OPPONENTS,
            "workers": WORKERS,
            "caliber": {
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-27 窗 step 336-648 逐日=step//24（14..26）；"
                          "d25=step 600-623、d26=step 624-647（原 −33.6 凹陷"
                          "日）；任务窗 576-624=逐日键 24+25 合并另报",
                "fill": "影子引擎逐拍归因（kgenv.replay_profile）"},
        },
        "gates": gates,
        "variants": {"forms": B.FORMS},
        "pairs": {}, "day_stats": {}, "criteria": {}, "verdict": {},
        "budget": budget,
    })
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(FOLDS_ALL) + [2026093001, 2026093002, 2026093003,
                                     2026093004, 2026093005, 2026093006,
                                     2026093007, 2026093008, 2026093009,
                                     2026093010, 2026093011, 2026093012,
                                     2026093013, 2026093014]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(C.EVID_DIR / "sim_auth_record_judge.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    flush_evid()
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    units = make_units()
    units_seal = [u for u in units if u["seed"] == LOSS_FOLDS[0]][:2]

    # ---- 2) 控制臂 + 等价封印 ----
    ctl_rows = play(CONTROL, CONTROL_MAIN, units, run_cfg, budget,
                    "control_局次")
    ctl = rows_by_key(ctl_rows)
    seal_rows = play(SEAL_FORM, str(MODULE_DIR / "build" / SEAL_FORM /
                                    "main.py"), units_seal, run_cfg, budget,
                     "seal_局次")
    budget["judgment_局次"] -= len(seal_rows)      # 封印不计判决预算
    seal = JM.seal_check(ctl, rows_by_key(seal_rows), units_seal)
    seal["design"] = ("d2526_neutral（mode=off 恒回退 drop_half 原装 _u2_qty）"
                      "vs drop_half 同 (seed,seat)：我席逐拍动作流 digest 全等"
                      " + 终局钱相等（参数级手术行为保真封印）")
    EV["variants"]["equivalence_seal"] = seal
    if not seal.get("passed"):
        ANOMALIES.append("等价封印未过: %r" % (seal.get("violations"),))
    flush_evid()

    # ---- 3) 两臂判决 ----
    for arm in ARMS:
        print("play", arm, flush=True)
        var_rows = play(arm, str(MODULE_DIR / "build" / arm / "main.py"),
                        units, run_cfg, budget, "arm_局次")
        var = rows_by_key(var_rows)
        ps = JM.pair_stats(ctl, var, units)
        rp = JM.realized_paired(ctl, var, units)
        wp = JM.window_paired(ctl, var, units)
        EV["pairs"][arm] = {"pair_stats": ps, "realized_price": rp}
        day = {k: v for k, v in (wp.get("per_day_fill_total_delta") or {})
               .items()}
        day_milk = {k: v for k, v in
                    (wp.get("per_day_fill_milk_delta") or {}).items()}
        EV["day_stats"][arm] = {
            "window": "d14-27（step 336-648）逐日=step//24",
            "window_total_delta": {k: wp.get(k) for k in
                                   ("fill_total", "fill_milk", "submit_total",
                                    "submit_milk")},
            "per_day_fill_total_delta": day,
            "per_day_fill_milk_delta": day_milk,
            "task_window_576_624_combined_delta": round(
                sum(float((day.get(k) or {}).get("mean_delta") or 0)
                    for k in ("24", "25")), 2),
            "rows_lite": wp.get("rows_lite"),
        }
        d25 = float((day.get(D25_KEY) or {}).get("mean_delta") or 0)
        d26 = float((day.get(D26_KEY) or {}).get("mean_delta") or 0)
        crit = {
            "净翻胜>0": {"net_flip_wins": ps.get("net_flip_wins"),
                        "passed": bool((ps.get("net_flip_wins") or 0) > 0)},
            "flips_neg==0": {"flips_neg": ps.get("flips_neg"),
                             "passed": ps.get("flips_neg") == 0},
            "d25/26 单日差转正": {
                "d25_delta(600-623)": d25, "d26_delta(624-647)": d26,
                "d24_delta(576-599)": (day.get("24") or {}).get("mean_delta"),
                "passed": bool(d25 > 0 and d26 > 0)},
            "实现价非负": {"nonneg_both": rp.get("nonneg_both"),
                          "all_mean_delta": (rp.get("all") or {}).get(
                              "mean_delta"),
                          "milk_mean_delta": (rp.get("milk") or {}).get(
                              "mean_delta"),
                          "passed": bool(rp.get("nonneg_both"))},
        }
        crit["all_passed"] = all(v.get("passed") for v in crit.values()
                                 if isinstance(v, dict))
        EV["criteria"][arm] = crit
        EV["pairs"][arm]["pair_stats_lite"] = lite_pair(ps)
        print(arm, "crit", {k: v.get("passed") for k, v in crit.items()
                            if isinstance(v, dict)}, flush=True)
        flush_evid()

    positive = [a for a in ARMS if EV["criteria"][a]["all_passed"]]
    EV["verdict"] = {
        "criterion": "净翻胜>0 ∧ flips_neg==0 ∧ d25/26 单日差转正 ∧ 实现价非负",
        "positive_arms": positive,
        "selected": (positive[0] if positive else None),
        "verdict": ("正臂=%s（上线决策移交用户；不发射不提交）" % (positive,)
                    if positive else "无正臂（四判据未同过）；d25/26 修复维"
                                      "持观察，移交用户裁决"),
        "per_arm": {a: EV["criteria"][a] for a in ARMS},
        "note": "d25/26=step 600-623/624-647（step//24 口径，原 −33.6 凹陷"
                "日）；任务窗 576-624 合并差见 day_stats；根因与解剖见 "
                "forensics 节",
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    EV["budget"]["total_局次"] = (budget.get("auth_局次", 0)
                                + budget.get("seal_局次", 0)
                                + budget.get("judgment_局次", 0))
    EV["budget"]["within_cap"] = EV["budget"]["total_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.time() - t0, 1)
    flush_evid()
    (C.EVID_DIR / "judge_day2526_ledger.json").write_text(
        json.dumps({"pairs": {a: EV["pairs"][a]["pair_stats"]
                              for a in ARMS},
                    "criteria": EV["criteria"], "verdict": EV["verdict"],
                    "generated": C.now()}, ensure_ascii=False, indent=1,
                   default=str) + "\n", encoding="utf-8")
    print("verdict:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
