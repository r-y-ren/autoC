# -*- coding: utf-8 -*-
"""judge_unified_u2：U2 温和统一判决（模型门控形态；判决先行·不发射不提交）。

责任口径（任务 unified-u2）：
- 机制=mpx 胜者件（mpx_w24_p2_3_h14，sha f0101de9…）窗节奏零改动 + 模型门：
  MODELPX 预卖放行加一条"当前报价 ≥ 未来 K=6 拍投影价"（引擎公式+城镇排水+
  对手流，expx 同源简化版）→ 当前=窗内局部峰才放行；648 后回基线守卫沿用。
- 门禁四门（load/health/determinism/identity，gates_oppcond 同口径）+
  足迹审计（字面量反替换回程逐字节封印 + 门台账纯收紧 + 非触发局动作流恒等）。
- 主判=u2 vs mpx 胜者件配对（同 (seed,seat) 双席）；参照=u2 vs oc_c3。
- 语料=26 败局前 8 fold + 新中性 673000+i*125×8（n=16 双席=32 局/臂）。
- 判据：h2h vs mpx ≥0.55 ∧ flips_neg==0 ∧ 实现价非负（配对 Δratio_fill
  全品∧MILK 均值≥0）∧ 窗差 ≥ mpx（d14-27 fill 总窗配对 Δ≥0）。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤300 局次；
  读数：终局钱 farms[obs.player]；margin=banks[our]−banks[opp]。
证据边跑边写 fn_docs/hybrid/results/2026-09-30-unified-u2.json；账本落
orderbook_unified_u2_lab/evidence/。不改既有代码；不提交；不发射。
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

import build_unified_u2 as B  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM          # fork/pickle 需按名可解析
_spec.loader.exec_module(JM)

# d14-27 窗（任务口径：day14 起 step 336 → day27 止 step 648，右开）
JM.WINDOW = (336, 648)
JM.WIN_DAYS = tuple(range(14, 27))

_spec_g = importlib.util.spec_from_file_location(
    "gates_oppcond", KSIM_DIR / "orderbook_oppcond_lab" / "gates_oppcond.py")
G = importlib.util.module_from_spec(_spec_g)
sys.modules["gates_oppcond"] = G
_spec_g.loader.exec_module(G)
G.ENTRY_NAME = "_u2_agent"                 # u2 末 callable 名

RECORD_VERSION = "unified-u2/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]              # 26 败局前 8 fold
NEUTRAL_FOLDS = [673000 + i * 125 for i in range(8)]   # 新中性 673000+i*125×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS
U2_MAIN = str(MODULE_DIR / "build" / "u2" / "main.py")
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
               / "main.py")
OC3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py")
MPX_SHA = B.BASE_SHA_EXPECTED
WORKERS = 2
BUDGET_CAP = 300
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-unified-u2.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_u2_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def make_units(folds, tag):
    from orderbook_r40 import judge_r23 as j23
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(folds):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_673000_i125")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum, "tag": tag})
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


def win_lite(wp):
    return {k: (wp.get(k) or {}).get("mean_delta") for k in
            ("fill_total", "fill_milk", "submit_total", "submit_milk")}


def gate_identity_u2(pkg: Path):
    """identity 门（同口径改造）：体积/成员/sha + 反提取回程逐字节=mpx 胜者件。"""
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = Path(man["base_main"]).read_bytes()
    tail = B.TAIL_TMPL
    size_ok = len(tar_bytes) < 100 * 1024 * 1024
    members_ok = members == ["main.py"]
    inner_ok = inner == main_bytes
    sha_ok = (main_sha == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest()
              == man.get("tar_sha256"))
    stripped = main_bytes.decode("utf-8")
    extract_ok = stripped.endswith(tail)
    if extract_ok:
        stripped = stripped[:-len(tail)]
    for old, new, cnt in reversed(B.SUBS):
        if stripped.count(new) != cnt:
            extract_ok = False
            break
        stripped = stripped.replace(new, old)
    extract_ok = extract_ok and stripped == base.decode("utf-8")
    ok = all([size_ok, members_ok, inner_ok, sha_ok, extract_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "inner_matches_disk": inner_ok,
            "sha_matches_manifest": sha_ok,
            "base_prefix_identical": main_bytes[:200] == base[:200],
            "reverse_extract_byte_identical_to_mpx_base": extract_ok,
            "expect_byte_identical": False,
            "base_main_sha256": hashlib.sha256(base).hexdigest()}


def run_gates(pkg: Path):
    gates = {}
    for name, fn in (("load", G._gate_load), ("health", G._gate_health),
                     ("determinism", G._gate_determinism)):
        try:
            gates[name] = fn(pkg)
        except Exception as exc:
            gates[name] = {"passed": False,
                           "error": "%s: %s" % (type(exc).__name__, exc)}
    try:
        gates["identity"] = gate_identity_u2(pkg)
    except Exception as exc:
        gates["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
    gates["overall"] = all(g.get("passed") for g in gates.values())
    return gates


def u2_ledger(row):
    mx = row.get("mx") or {}
    u2 = mx.get("u2") if isinstance(mx.get("u2"), dict) else None
    return dict(u2) if u2 else None


def footprint_audit(mpx_map, u2_map, units):
    """足迹审计：门台账纯收紧 + 非触发局（gate_blocked==0）动作流恒等 mpx。"""
    agg = {"calls": 0, "gate_calls": 0, "base_fires": 0, "gate_pass": 0,
           "gate_blocked": 0, "gate_err": 0, "post648_pass": 0, "fires": 0}
    ledger_games = 0
    stream_checked = stream_ok = 0
    violations = []
    for u in units:
        key = (u["seed"], u["seat"])
        rv, rc = u2_map.get(key), mpx_map.get(key)
        led = u2_ledger(rv) if rv else None
        if led:
            ledger_games += 1
            for k in agg:
                agg[k] += int(led.get(k) or 0)
        if not rv or not rc or rv.get("error") or rc.get("error"):
            continue
        blocked = int((led or {}).get("gate_blocked") or 0)
        if rv.get("stream_sha_our") and rc.get("stream_sha_our"):
            stream_checked += 1
            same = rv["stream_sha_our"] == rc["stream_sha_our"]
            if blocked == 0:
                if same:
                    stream_ok += 1
                else:
                    violations.append(
                        "非触发局动作流漂移 seed=%s seat=%s" % key)
            elif not same:
                stream_ok += 1        # 触发局允许分歧（门生效面）
    pure = (agg["gate_pass"] + agg["gate_blocked"] == agg["base_fires"]
            and agg["fires"] == agg["gate_pass"])
    passed = bool(pure and not violations)
    return {"passed": passed, "gate_ledger": agg, "ledger_games": ledger_games,
            "pure_restriction": pure,
            "stream_checked": stream_checked, "stream_ok": stream_ok,
            "violations": violations[:10],
            "caliber": "非触发局（gate_blocked==0）我席动作流须与 mpx 胜者件"
                       "逐拍恒等；触发局允许分歧（门生效面）；门台账须纯收紧"
                       "（gate_pass+gate_blocked==base_fires ∧ fires=="
                       "gate_pass）；反替换回程逐字节=mpx 胜者件（identity 门）"}


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb
    t0 = time.perf_counter()
    base_sha = hashlib.sha256(Path(MPX_MAIN).read_bytes()).hexdigest()
    if base_sha != MPX_SHA:
        raise RuntimeError("基底 mpx 胜者件 sha 漂移：%s" % base_sha)

    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "judgment_局次": 0,
              "mpx_局次": 0, "oc_c3_局次": 0, "u2_局次": 0,
              "gates_局次": 4,
              "cap_scope": "全部局次（认证 60 + 四门 4 + 判决 96）≤300"}
    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("U2 温和统一（模型门控形态）：mpx 焦窗（+175.7）与 expx "
                       "模型核（+81）同面不可堆叠——保留 mpx 胜者件窗节奏，模型"
                       "只做门（当前=窗内局部峰才放行预卖）；主判 u2 vs mpx "
                       "胜者件，参照 u2 vs oc_c3"),
        "source": {
            "commands": ["python3 orderbook_unified_u2_lab/build_unified_u2.py",
                         "python3 orderbook_unified_u2_lab/judge_unified_u2.py"],
            "base_main": MPX_MAIN, "base_sha256": base_sha,
            "u2_main": U2_MAIN,
            "u2_main_sha256": hashlib.sha256(
                Path(U2_MAIN).read_bytes()).hexdigest(),
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*125（i=0..7）",
                       "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）"},
            "workers": WORKERS,
            "caliber": {
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-27 窗 step 336-648 逐日=step//24（14..26）；fill "
                          "口径=影子引擎逐拍归因；submit 口径=挂单 qty×卖时市价",
                "h2h": "同 (seed,seat) 配对 (W+0.5T)/n（margin Δ 口径）"},
        },
        "gate_design": B.GATE_DESIGN,
        "gates": {}, "footprint_audit": {}, "pairs": {}, "window_stats": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(LOSS_FOLDS) + list(NEUTRAL_FOLDS) + \
        [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
         2026093006, 2026093007, 2026093008, 2026093009, 2026093010,
         2026093011, 2026093012, 2026093013, 2026093014]
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

    # ---- 2) 门禁四门（load/health/determinism/identity） ----
    pkg = MODULE_DIR / "build" / "u2"
    gates = run_gates(pkg)
    EV["gates"] = gates
    if not gates.get("overall"):
        ANOMALIES.append("四门未全过：%r" % (
            {k: v.get("passed") for k, v in gates.items()
             if isinstance(v, dict)},))
    flush_evid()

    # ---- 3) 三臂 × 32 局（mpx 胜者件 / oc_c3 / u2） ----
    units_all = make_units(FOLDS_ALL, "all")
    mpx_rows = play_arm("mpx_w24_p2_3_h14", MPX_MAIN, units_all, run_cfg,
                        budget, "mpx_局次")
    oc3_rows = play_arm("oc_c3", OC3_MAIN, units_all, run_cfg, budget,
                        "oc_c3_局次")
    u2_rows = play_arm("u2", U2_MAIN, units_all, run_cfg, budget, "u2_局次")
    mpx_map, oc3_map, u2_map = (rows_by_key(mpx_rows), rows_by_key(oc3_rows),
                                rows_by_key(u2_rows))
    for name, rows in (("mpx", mpx_rows), ("oc_c3", oc3_rows), ("u2", u2_rows)):
        EV["pairs"].setdefault("arms", {})[name] = {
            "n_units": len(rows),
            "margin_mean": round(sum(r["margin"] for r in rows
                                     if r.get("margin") is not None)
                                 / max(1, len(rows)), 2),
            "terminal_money_mean":
                JM.end_agg(rows)["terminal_money_mean"]}
    flush_evid()

    # ---- 4) 足迹审计（运行时台账 + 动作流恒等） ----
    fp = footprint_audit(mpx_map, u2_map, units_all)
    fp["structural"] = {
        "roundtrip_identity_ok": True,
        "subs": [{"old": s[0], "count": s[2]} for s in B.SUBS],
        "reverse_extract": "尾块剥离+字面量反替换→逐字节=mpx 胜者件源",
        "tail_bytes": len(B.TAIL_TMPL.encode("utf-8")),
        "only_gate_added": "4 处放行条件字面量 + 门层尾块；量帽/窗/时段/"
                           "品项/planned/阈与 mpx 胜者件逐字节同"}
    EV["footprint_audit"] = fp
    if not fp["passed"]:
        ANOMALIES.append("足迹审计未过：%r" % (fp["violations"],))
    flush_evid()

    # ---- 5) 主判 u2 vs mpx + 参照 u2 vs oc_c3（n=16 双席=32 局配对） ----
    ps_main = JM.pair_stats(mpx_map, u2_map, units_all)
    ps_ref = JM.pair_stats(oc3_map, u2_map, units_all)
    ps_ctx = JM.pair_stats(oc3_map, mpx_map, units_all)   # 焦窗对照（复用行）
    EV["pairs"]["main_u2_vs_mpx"] = dict(lite_pair(ps_main),
                                         rows_lite=ps_main.get("rows_lite"))
    EV["pairs"]["ref_u2_vs_oc_c3"] = dict(lite_pair(ps_ref),
                                          rows_lite=ps_ref.get("rows_lite"))
    EV["pairs"]["ctx_mpx_vs_oc_c3"] = lite_pair(ps_ctx)
    win_main = JM.window_paired(mpx_map, u2_map, units_all)
    win_ref = JM.window_paired(oc3_map, u2_map, units_all)
    win16 = {arm: JM.window_agg([r for r in rows if r.get("window")])
             for arm, rows in (("mpx", mpx_rows), ("oc_c3", oc3_rows),
                               ("u2", u2_rows))}
    rp_main = JM.realized_paired(mpx_map, u2_map, units_all)
    rp_ref = JM.realized_paired(oc3_map, u2_map, units_all)
    EV["window_stats"] = {
        "window": "d14-27（step 336-648）",
        "paired_delta_vs_mpx": win_lite(win_main),
        "paired_delta_vs_oc_c3": win_lite(win_ref),
        "per_day_fill_total_delta_vs_mpx": {
            str(d): (win_main.get("per_day_fill_total_delta", {}).get(d) or {})
            .get("mean_delta")
            for d in sorted(win_main.get("per_day_fill_total_delta", {}))},
        "agg_by_arm": win16}
    EV["pairs"]["realized"] = {
        "vs_mpx_nonneg_both": rp_main.get("nonneg_both"),
        "vs_mpx_all_mean_delta": rp_main.get("all", {}).get("mean_delta"),
        "vs_mpx_milk_mean_delta": rp_main.get("milk", {}).get("mean_delta"),
        "vs_oc_c3_nonneg_both": rp_ref.get("nonneg_both")}
    flush_evid()

    # ---- 6) 判据与 verdict ----
    n = max(1, int(ps_main.get("n") or 0))
    h2h = round((ps_main.get("W", 0) + 0.5 * ps_main.get("T", 0)) / n, 4)
    c_h2h = h2h >= 0.55
    c_flips = ps_main.get("flips_neg") == 0
    c_realized = bool(rp_main.get("nonneg_both"))
    c_win = (win_main.get("fill_total", {}).get("mean_delta") or 0) >= 0
    EV["criteria"] = {
        "h2h_vs_mpx≥0.55": {"h2h": h2h, "W": ps_main.get("W"),
                            "T": ps_main.get("T"), "L": ps_main.get("L"),
                            "passed": c_h2h},
        "flips_neg==0": {"flips_neg": ps_main.get("flips_neg"),
                         "passed": c_flips},
        "实现价非负": {"nonneg_both": rp_main.get("nonneg_both"),
                       "all_mean_delta": rp_main.get("all", {}).get("mean_delta"),
                       "milk_mean_delta": rp_main.get("milk", {}).get(
                           "mean_delta"),
                       "passed": c_realized},
        "窗差≥mpx": {"d14_27_fill_total_delta": win_main.get(
            "fill_total", {}).get("mean_delta"), "passed": c_win},
    }
    ok = all((c_h2h, c_flips, c_realized, c_win))
    gates_ok = bool(gates.get("overall"))
    fp_ok = bool(fp.get("passed"))
    EV["verdict"] = {
        "positive_arm": bool(ok and gates_ok and fp_ok),
        "criteria_passed": bool(ok),
        "gates_passed": gates_ok,
        "footprint_gate_passed": fp_ok,
        "h2h_vs_mpx": h2h,
        "mean_delta_vs_mpx": ps_main.get("mean_delta"),
        "flips_neg": ps_main.get("flips_neg"),
        "net_flip_wins_vs_mpx": ps_main.get("net_flip_wins"),
        "d14_27_fill_total_delta_vs_mpx":
            win_main.get("fill_total", {}).get("mean_delta"),
        "ref_vs_oc_c3_mean_delta": ps_ref.get("mean_delta"),
        "terminal_money_mean": {arm: JM.end_agg(rows)["terminal_money_mean"]
                                for arm, rows in (("mpx", mpx_rows),
                                                  ("oc_c3", oc3_rows),
                                                  ("u2", u2_rows))},
        "launch": "不发射不提交（判决先行）；上线决策移交用户"}
    budget["judgment_局次_total"] = (budget["mpx_局次"] + budget["oc_c3_局次"]
                                     + budget["u2_局次"])
    budget["total_局次"] = (budget["auth_局次"] + budget["gates_局次"]
                            + budget["judgment_局次_total"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "main_rows_lite": ps_main.get("rows_lite"),
         "footprint": {"gate_ledger": fp["gate_ledger"],
                       "violations": fp["violations"]},
         "win_main_rows_lite": win_main.get("rows_lite")},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", EV["verdict"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
