# -*- coding: utf-8 -*-
"""judge_unified_u1_v2：U1-V2 统一求解核·缺陷修复判决（连续空间投影；
判决先行·不发射不提交）。

责任口径（任务 unified-u1 v2）：
- 形态=u1v2a（阈连续化：连续差>$0.5 才卖）/u1v2b（同值即卖·跌幅拦截形：
  持有上行>$0.5 才拦、平局破向卖出）——同一手术面 8 站点，v2 核比较全用未取
  整连续价（显示/结算价才取整）；门字面量不动哨兵过门；胜位守卫沿 expx_v2。
- 语料=26 败局前 8 fold + 新中性 673000+i*129×8，n=16 双席=32 格/臂；对手
  j23.DEFAULT_OPPONENTS 按 fold 轮转；h2h=v2 件与 mpx 胜者件直接同局双席。
- 判据沿四条 vs mpx 胜者件：h2h ≥0.55 ∧ flips_neg==0 ∧ 实现价非负 ∧ 窗差
  ≥mpx；附胜率口径附注（R27 重裁先例：胜率=天梯硬通货，单列胜率正信号）+
  遥测对照（中窗 fires 占比应从 v1 的 2/14 显著回升）。
- sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤300 局次。
证据并入 fn_docs/hybrid/results/2026-09-30-unified-u1.json 的 v2 节；账本落
orderbook_unifiedu1_lab/evidence/。只写 orderbook_unifiedu1_lab/ 与该文件。
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import statistics
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
L1_DIR = str(KSIM_DIR / "orderbook_l1_derivative")
for _p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_milkwin_lab"),
           str(MODULE_DIR), L1_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_milkwin as jm  # noqa: E402
import judge_unified_u1 as J1  # noqa: E402  （v1 机件复用）

RECORD_VERSION = "unified-u1-v2/1.0"
UNKNOWN = "UNKNOWN"

LOSS_FOLDS = list(jm.REPLAY_26[:8])
NEUTRAL_FOLDS = [673000 + i * 129 for i in range(8)]   # v2 新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS

jm.WINDOW = (336, 648)
jm.WIN_DAYS = tuple(range(14, 27))
WINDOW_LABEL = "d14-27（step 336-648）"

OC_C3_MAIN = J1.OC_C3_MAIN
OC_C3_SHA_EXPECTED = J1.OC_C3_SHA_EXPECTED
MPX_MAIN = J1.MPX_MAIN
MPX_SHA_EXPECTED = J1.MPX_SHA_EXPECTED
V2_MAINS = {"u1v2a": str(MODULE_DIR / "build" / "u1v2a" / "main.py"),
            "u1v2b": str(MODULE_DIR / "build" / "u1v2b" / "main.py")}
ARMS = {"oc_c3": OC_C3_MAIN, "mpx_w24_p2_3_h14": MPX_MAIN, **V2_MAINS}
RUN_FORMS = ("oc_c3", "mpx_w24_p2_3_h14", "u1v2a", "u1v2b")
V2_FORMS = ("u1v2a", "u1v2b")
ENTRY_NAME = "_u1_agent"
MODELPX_WINDOW = (144, 695)

WORKERS = 2
BUDGET_CAP_GAMES = 300
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-unified-u1.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_u1v2_ledger.json"

EV2 = {}
ANOMALIES = []
_load_agent_u1 = J1._load_agent_u1
_Tracer = J1._Tracer
u1_reads = J1.u1_reads
footprint_audit = J1.footprint_audit
realized_paired3 = J1.realized_paired3
_run_episode = J1._run_episode
is_num = J1.is_num


def flush_v2():
    """并入主 evidence JSON（v2 节；v1 节原样保留）。"""
    EV2["anomaly"] = list(ANOMALIES)
    EV2["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        doc = json.loads(EVID_PATH.read_text(encoding="utf-8"))
    except Exception:
        doc = {}
    doc["v2"] = EV2
    EVID_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def _build_agents(spec):
    out = []
    sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        inner, reports = _load_agent_u1(a["path"])
        out.append(_Tracer(inner, seat, sinks[seat], reports))
    return out, sinks


def _run_chunk(payload):
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = _build_agents(spec)
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
               "window": None, "u1": None, "stream_sha_our": None,
               "stream": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our = sinks[row["seat"]]
            row["reads"] = jm.end_reads(our)
            row["items"] = jm.item_reads(our)
            row["u1"] = u1_reads(our)
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
    import multiprocessing
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
    rows = []
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
                   else "neutral_673000_i129")
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
            "game_id": "u1v2-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


def make_specs_h2h(form, units):
    specs = []
    for r in units:
        agents = [{"type": "python", "path": V2_MAINS[form]},
                  {"type": "python", "path": MPX_MAIN}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "u1v2h2h-%s-%d-s%d" % (form, int(r["seed"]),
                                               int(r["seat"])),
            "seed": int(r["seed"]), "arm": "h2h_" + form,
            "our_seat": int(r["seat"]), "trace": True,
            "opponent": "mpx_w24_p2_3_h14", "stratum": r.get("stratum"),
            "agents": agents})
    return specs


def _gate_identity(pkg, form):
    main_bytes = open(os.path.join(pkg, "main.py"), "rb").read()
    tar_bytes = open(os.path.join(pkg, "submission.tar.gz"), "rb").read()
    man = json.load(open(os.path.join(pkg, "build_manifest.json")))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = open(OC_C3_MAIN, "rb").read()
    base_sha = hashlib.sha256(base).hexdigest()
    checks = {
        "size_lt_100mb": len(tar_bytes) < J1.SIZE_CAP_BYTES,
        "tar_members_exact": members == ["main.py"],
        "inner_matches_disk": inner == main_bytes,
        "sha_matches_manifest": main_sha == man.get("main_sha256"),
        "base_sha_ok": base_sha == OC_C3_SHA_EXPECTED
        and man.get("base_sha256") == OC_C3_SHA_EXPECTED,
        "subs_roundtrip_identity_ok": bool(
            man.get("subs_roundtrip_identity_ok")),
        "gate_literal_untouched": bool(man.get("gate_literal_untouched")),
        "injected_not_identity": main_bytes != base
        and len(main_bytes) > len(base),
        "entry_manifest_ok": man.get("entry") == ENTRY_NAME,
        "arm_manifest_ok": man.get("form") == form,
    }
    return {"passed": all(checks.values()), "checks": checks,
            "main_sha256": main_sha, "tar_size_mb": round(len(tar_bytes) / 1e6,
                                                          3),
            "base_main_sha256": base_sha}


def run_gates(form):
    pkg = str(MODULE_DIR / "build" / form)
    res = {}
    for gname, fn in (("load", lambda p=pkg: J1._gate_load(p)),
                      ("health", lambda p=pkg: J1._gate_health(p)),
                      ("determinism", lambda p=pkg: J1._gate_determinism(p))):
        try:
            res[gname] = fn()
        except Exception as exc:
            res[gname] = {"passed": False, "error": repr(exc)[:200]}
    try:
        res["identity"] = _gate_identity(pkg, form)
    except Exception as exc:
        res["identity"] = {"passed": False, "error": repr(exc)[:200]}
    res["overall"] = all(g.get("passed") for g in res.values())
    return res


def telemetry_agg(rows):
    te = {"fires": 0, "units": 0, "errors": 0, "mr_limited": 0,
          "cap_limited": 0, "stranding_insured": 0, "post_win_base": 0,
          "window_suppressed": 0, "closing_fires": 0, "decision_diffs": 0}
    for r in rows:
        x = r.get("u1") or {}
        for k in ("fires", "units", "errors", "mr_limited", "cap_limited",
                  "stranding_insured", "post_win_base", "window_suppressed",
                  "closing_fires"):
            te[k] += int(x.get(k) or 0)
        te["decision_diffs"] += len(x.get("decision_diff_steps") or [])
    te["mid_window_fires"] = te["fires"] - te["closing_fires"]
    te["mid_window_share"] = (round(te["mid_window_fires"] / te["fires"], 3)
                              if te["fires"] else UNKNOWN)
    return te


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移")
    if hashlib.sha256(Path(MPX_MAIN).read_bytes()).hexdigest() \
            != MPX_SHA_EXPECTED:
        raise RuntimeError("mpx 胜者件 sha 漂移")
    for form in V2_FORMS:
        man = json.loads((MODULE_DIR / "build" / form / "build_manifest.json")
                         .read_text(encoding="utf-8"))
        if hashlib.sha256(Path(V2_MAINS[form]).read_bytes()).hexdigest() \
                != man.get("main_sha256"):
            raise RuntimeError("%s main sha 漂移" % form)

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES, "auth_局次": 0, "gate_局次": 0,
              "smoke_局次": 1, "judgment_局次": 0}

    try:
        v1 = json.loads(EVID_PATH.read_text(encoding="utf-8"))
        v1_tel = v1.get("u1_telemetry") or {}
        v1_criterion = v1.get("criteria") or {}
    except Exception:
        v1_tel, v1_criterion = {}, {}

    EV2.update({
        "version": RECORD_VERSION,
        "experiment": ("U1-V2 统一求解核·缺陷修复（连续空间投影）：v1 败因="
                       "整数取整吃分辨率→投影峰值与现价同值→中窗保守（2/14）"
                       "→末拍堆积；修复=比较用未取整连续价+触发阈两臂（A 阈连"
                       "续化/B 同值即卖·跌幅拦截形）"),
        "source": {
            "commands": ["python3 orderbook_unifiedu1_lab/build_unified_u1_v2.py",
                         "python3 orderbook_unifiedu1_lab/judge_unified_u1_v2.py"],
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*129（v2 任务给定新中性块 n=8）",
                       "strata": "26 败局前 8 fold + 新中性 673000+i*129×8；"
                                 "n=16 双席=32 格/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": J1.EV["source"]["caliber"] if getattr(J1, "EV", None)
            else "同 v1（margin=banks 差；终局钱 farms[obs.player]；窗 d14-27 "
                 "step 336-648 fill 口径；实现价 ratio_fill）",
            "criterion": ("四判据沿 v1 vs mpx 胜者件：h2h ≥0.55 ∧ flips_neg==0 "
                          "∧ 实现价非负 ∧ 窗差 ≥mpx；附胜率口径附注（R27 重裁"
                          "先例：胜率=天梯硬通货，单列胜率正信号）"),
        },
        "arms": {f: (json.loads((MODULE_DIR / "build" / f /
                                 "build_manifest.json").read_text(
                                     encoding="utf-8")).get("arm_name"))
                 for f in V2_FORMS},
        "gates": {}, "pairs": {}, "window_stats": {}, "realized_px_paired": {},
        "telemetry": {"v1_reference": {"fires": v1_tel.get("fires"),
                                       "closing_fires":
                                           v1_tel.get("closing_fires"),
                                       "mid_window_fires": 2,
                                       "mid_window_share": "2/14"}},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_v2()

    # ---- 1) sim_bridge 对照认证 30/30 ----
    auth_corpus = list(jm.REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                        2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence"
                            / "sim_auth_record_v2.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV2["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV2["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_v2()
        return EV2
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_v2()

    # ---- 2) 门禁四门（两形态） ----
    for form in V2_FORMS:
        t1 = time.perf_counter()
        res = run_gates(form)
        EV2["gates"][form] = res
        budget["gate_局次"] += 4
        print(form, "gates:", {k: v.get("passed") for k, v in res.items()
                               if k != "overall"},
              round(time.perf_counter() - t1, 1), "s", flush=True)
        flush_v2()

    # ---- 3) 冒烟 ----
    smoke_units = [{"seed": 2026092999, "seat": 0, "opp_path": opp_paths[0],
                    "opponent": "r37", "stratum": "smoke"}]
    smoke_rows, _e0 = _play(make_specs("smoke", V2_MAINS["u1v2b"],
                                       smoke_units), run_cfg)
    print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
          flush=True)
    if smoke_rows[0].get("error"):
        ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
    flush_v2()

    # ---- 4) 四臂实跑 ----
    rows_by_arm = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, _eng = _play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget["judgment_局次"] += len(rows)
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d" % (arm, n_err, len(rows)))
        if arm in V2_FORMS:
            EV2["telemetry"][arm] = telemetry_agg(rows)
        print(arm, "games", len(rows), "err", n_err,
              "tm", jm.end_agg(rows)["terminal_money_mean"],
              round(time.perf_counter() - t2, 1), "s", flush=True)
        EV2["budget"] = budget
        flush_v2()

    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    mpx = {(r["seed"], r["seat"]): r for r in rows_by_arm["mpx_w24_p2_3_h14"]}

    # ---- 5) h2h（两形态 vs mpx 胜者件） ----
    for form in V2_FORMS:
        h2h_rows, _e1 = _play(make_specs_h2h(form, units), run_cfg)
        budget["judgment_局次"] += len(h2h_rows)
        n = len(h2h_rows)
        W = sum(1 for r in h2h_rows if (r.get("margin") or 0) > 0)
        L = sum(1 for r in h2h_rows if (r.get("margin") or 0) < 0)
        T = n - W - L
        rate = round((W + 0.5 * T) / max(1, n), 4)
        EV2["pairs"].setdefault("h2h_vs_mpx", {})[form] = {
            "design": "%s 与 mpx_w24_p2_3_h14 直接同局；16 fold×双席" % form,
            "n": n, "W": W, "L": L, "T": T, "win_rate": rate,
            "mean_margin": round(sum(r["margin"] for r in h2h_rows
                                     if r.get("margin") is not None)
                                 / max(1, n), 2),
            "terminal_money_mean":
                jm.end_agg(h2h_rows)["terminal_money_mean"]}
        print("h2h", form, "vs mpx:", "W%s/L%s/T%s" % (W, L, T), "rate", rate,
              flush=True)
        flush_v2()

    # ---- 6) 足迹审计 + 配对判决（逐形态） ----
    win_mpx = jm.window_paired(ctl, mpx, units)["fill_total"]["mean_delta"]
    for form in V2_FORMS:
        var = {(r["seed"], r["seat"]): r for r in rows_by_arm[form]}
        fp = footprint_audit(ctl, var, units)
        EV2["gates"].setdefault("footprint", {})[form] = fp
        if not fp["gate_passed"]:
            ANOMALIES.append("%s 足迹审计门未全过：%d/%d"
                             % (form, fp["n_passed"], fp["n_cells"]))
        ps_main = jm.pair_stats(mpx, var, units)
        ps_c3 = jm.pair_stats(ctl, var, units)
        wp_c3 = jm.window_paired(ctl, var, units)
        wp_main = jm.window_paired(mpx, var, units)
        rp_main = realized_paired3(mpx, var, units)
        EV2["pairs"][form] = {"vs_mpx": ps_main, "vs_oc_c3": ps_c3}
        EV2["window_stats"][form] = {
            "window": WINDOW_LABEL,
            "vs_oc_c3_fill_total": wp_c3["fill_total"]["mean_delta"],
            "vs_oc_c3_fill_milk": wp_c3["fill_milk"]["mean_delta"],
            "vs_mpx_fill_total": wp_main["fill_total"]["mean_delta"]}
        EV2["realized_px_paired"][form] = rp_main
        win_u = wp_c3["fill_total"]["mean_delta"]
        h2h_rate = EV2["pairs"]["h2h_vs_mpx"][form]["win_rate"]
        crit = {
            "h2h_vs_mpx>=0.55": h2h_rate >= 0.55,
            "flips_neg==0": ps_main.get("flips_neg") == 0,
            "实现价非负（Δratio_fill 三品∧全品均值≥0）":
                rp_main["nonneg_all_three"],
            "窗差>=mpx（u1v2 vs oc_c3 ≥ mpx vs oc_c3）":
                is_num(win_u) and is_num(win_mpx)
                and float(win_u) >= float(win_mpx),
        }
        EV2["criteria"][form] = {
            "checks": crit,
            "h2h_win_rate": h2h_rate,
            "flips_neg": ps_main.get("flips_neg"),
            "net_flip_wins": ps_main.get("net_flip_wins"),
            "mean_delta_vs_mpx": ps_main.get("mean_delta"),
            "mean_delta_vs_oc_c3": ps_c3.get("mean_delta"),
            "realized_px_nonneg_all_three": rp_main["nonneg_all_three"],
            "window_fill_total_delta_vs_oc_c3": win_u,
            "window_fill_total_delta_mpx_vs_oc_c3": win_mpx,
            "positive_arm": all(crit.values()),
            "胜率口径附注": ("R27 重裁先例：胜率=天梯硬通货，单列胜率正信号；"
                             "重裁三判据=胜率≥0.55∧钱差非负∧零足迹"),
            "win_rate_signal": bool(h2h_rate >= 0.55)}
        print(form, "vs mpx:", "W%s/L%s/T%s" % (ps_main["W"], ps_main["L"],
                                                ps_main["T"]),
              "dM", ps_main["mean_delta"], "flips_neg", ps_main["flips_neg"],
              "win_u", win_u, "crit", crit, flush=True)
        flush_v2()

    # ---- 7) verdict ----
    budget["total_局次"] = (budget["auth_局次"] + budget["gate_局次"]
                           + budget["smoke_局次"] + budget["judgment_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES
    positives = [f for f in V2_FORMS if EV2["criteria"][f]["positive_arm"]]
    EV2["verdict"] = {
        "criterion": EV2["source"]["criterion"],
        "positive_forms": positives,
        "per_form": {f: {"criteria_passed":
                         EV2["criteria"][f]["positive_arm"],
                         "h2h_win_rate":
                             EV2["criteria"][f]["h2h_win_rate"],
                         "win_rate_signal":
                             EV2["criteria"][f]["win_rate_signal"],
                         "mid_window_fires_share":
                             (EV2["telemetry"][f] or {}).get(
                                 "mid_window_share")}
                     for f in V2_FORMS},
        "telemetry_vs_v1": {
            "v1_mid_window_fires": "2/14",
            "u1v2a": (EV2["telemetry"]["u1v2a"] or {}).get(
                "mid_window_share"),
            "u1v2b": (EV2["telemetry"]["u1v2b"] or {}).get(
                "mid_window_share")},
        "verdict": ("U1V2_POSITIVE: %s 四判据全过" % ", ".join(positives)
                    if positives else
                    "NOT_CONFIRMED（四判据未全过；胜率口径信号见 per_form，"
                    "R27 重裁先例单列）"),
        "note": "判据沿 v1 预登记四条 vs mpx 胜者件；不发射不提交",
    }
    EV2["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV2["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行；"
                     "kaggle_environments 可选环境加载告警")
    ANOMALIES.append("口径备忘：连续价 _u1_price_c=price(inv) 曲线原值（$1 地"
                     "板生效）仅核内比较用，显示/结算价仍取整（引擎侧）；影子"
                     "基线仍按基座取整式（保真）；臂 B 容差 $0.5 贯穿何时卖与"
                     "卖多少（持有上行>$0.5 才拦，平局破向卖出）")
    LEDGER_PATH.write_text(json.dumps(
        {"h2h": {f: EV2["pairs"]["h2h_vs_mpx"][f] for f in V2_FORMS},
         "criteria": EV2["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_v2()
    print("DONE", EV2["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV2["verdict"]["verdict"], flush=True)
    return EV2


if __name__ == "__main__":
    main()
