# -*- coding: utf-8 -*-
"""judge_godv7（godv7 lab）：leoprovorov god's-mode v7（flexonafft 重打包）紧急竞技池实测
（判决先行·不发射不提交·零修改原始件）。

件：fn_docs/hybrid/references/ext/godv7/agent/main.py（last-callable `agent(observation,
configuration=None)`；四 py sha 见 extract_manifest.json）。装载经外部 harness 适配层：
每局前清 sys.modules 的 base_agent/shop_overlay/shop_predictor → 重新 import=全新模块态
（对齐官方逐局全新解释器语义；单文件对手 j23._load_entry 本就逐局全新命名空间）。
第三方代码执行全程 bwrap 沙箱（根只读+/tmp+本 lab 可写+断网）。

面板（同块可比，每对 n=12 fold 双席=24 局，中性块 674000+i*131 i=0..11）：
  godv7 vs {oc_c3 冠军锚, c_final 主件(sha a37c0d34…), s8(sha a59208fe…), r40, A}
判决口径（任务）：对 oc_c3 ≥0.5=可能超天花板（BEATS_CEILING）；0.35-0.5=COMPETITIVE；
<0.35=WEAK；跑不起来=UNRUNNABLE。弱锚 {r40,A} ≥0.8=弱面正常。h2h=judge_r44._fold_arm
同 (seed,seat,opp) 双席折叠（≥1 胜/≤0 负/余平，fail-closed）；margin=farms[obs.player]
终局钱差（干净口径，banks 交叉登记）；mean_margin 与 realized_px 只作参考。
sim_bridge 认证 30/30×2 轮（godv7 侧在环，覆盖引擎对 godv7 的一致性）。
证据 fn_work/legacy_software/kaggle_simulations/orderbook_godv7_lab/evidence/godv7_arena.json。
只写本 lab 与上述证据路径；不改既有代码；不在线提交任何东西。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = EVID_DIR / "godv7_arena.json"

GODV7_MAIN = REPO / "fn_docs" / "hybrid" / "references" / "ext" / "godv7" \
    / "agent" / "main.py"
GODV7_MODULES = ("base_agent", "shop_overlay", "shop_predictor")
OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
CFINAL = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A_MAIN = KSIM_DIR / "orderbook_r44_a" / "main.py"

# 面板：c_final 为"主件"席（任务"s8 或 c_final 选一"选 c_final，sha 标注）；s8 为加测第 5 对
# （当前计分对 {C_final, S8} 两员都测，服务"值不值得进计分对"决策）。
PANEL = {
    "oc_c3": OC3,
    "c_final": CFINAL,
    "s8": S8,
    "r40": R40,
    "A": A_MAIN,
}
PANEL_ROLE = {"oc_c3": "冠军锚（H1/oc_c3 孪生，BT 天花板 528）",
              "c_final": "主件席（现计分对员，sha a37c0d34…）",
              "s8": "加测（现计分对员，sha a59208fe…）",
              "r40": "弱锚", "A": "弱锚"}
NEUTRAL_FOLDS = [674000 + i * 131 for i in range(12)]
WORKERS = 2

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 装载适配 ==
def load_entry(path):
    """harness 适配装载：godv7 多文件件=先清其模块缓存再走 last-callable 装载。
    对手单文件件直接 j23._load_entry（逐局全新命名空间）。零修改原始件。"""
    p = os.path.abspath(str(path))
    if Path(p).parent == GODV7_MAIN.parent:
        for m in GODV7_MODULES:
            sys.modules.pop(m, None)
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    return j23._load_entry(p)


def _build(spec):
    """局规格→(带追踪 agents, sinks)。口径照 judge_c_final._chunk_panel。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    sinks = {0: [], 1: []}
    out = []
    for seat, a in enumerate(spec["agents"]):
        inner = load_entry(a["path"])
        out.append(j23._Tracer(inner, seat, sinks[seat]))
    return out, sinks


def _chunk_panel(payload):
    """panel worker：终局钱 farms[obs.player]（干净口径）+ banks 交叉登记 +
    realized_px（参考）。单局红计入不短路。"""
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    specs = payload["specs"]
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = _build(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, repr(exc)[:160]))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None, "realized_px": None}
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
                row["realized_px"] = j44._realized_price_stats(
                    sinks[row["seat"]]).get("realized_px")
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
        out.append(row)
    return out


def play(chunk_fn, specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [chunk_fn(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(chunk_fn, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(arm_path, opp_path, opp_name, folds):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            a_us = {"type": "python", "path": str(arm_path)}
            a_opp = {"type": "python", "path": str(opp_path)}
            agents = [a_us, a_opp] if seat == 0 else [a_opp, a_us]
            specs.append({
                "game_id": "gv7|%s|%d-s%d" % (opp_name, seed, seat),
                "seed": int(seed), "arm": "godv7", "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "kind": "ab", "trace": True,
                "agents": agents})
    return specs


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows if isinstance(r.get("tm_opp"),
                                                   (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin"] = round(sum(r["margin_clean"] for r in rows
                                 if r["margin_clean"] is not None)
                             / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    pxs = [float(r["realized_px"]) for r in rows
           if isinstance(r.get("realized_px"), (int, float))]
    f["realized_px_median"] = round(statistics.median(pxs), 4) if pxs else None
    f["realized_px_mean"] = round(sum(pxs) / len(pxs), 4) if pxs else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    diffs = [abs(float(r["margin_clean"]) - float(r["margin_banks"])) for r in rows
             if r.get("margin_clean") is not None
             and r.get("margin_banks") is not None]
    f["banks_crosscheck"] = {
        "n_compared": len(diffs),
        "n_material_diff_gt_1000": sum(1 for d in diffs if d > 1000),
        "max_abs_diff": round(max(diffs), 1) if diffs else None,
        "note": "margin_clean=farms[obs.player] 日29 现金差（判决口径）；"
                "margin_banks=引擎终局钱差（交叉登记）；正常小幅背离（day29 窗 vs 终局）"}
    return f


# ============================================================ 主流程 ==
def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    import hashlib

    def sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()

    EV.update({
        "version": "godv7-arena/1.0",
        "task": "leoprovorov god's-mode v7（flexonafft 重打包）放进本地竞技池实测强度"
                "（判决先行·不发射不提交·零修改原始件）",
        "arm": {
            "name": "godv7",
            "origin": "leoprovorov/god-s-mode-hacked-stores scriptVersionId=351167531"
                      "（经 flexonafft/kaggriculture-multi-route-farming-agent 重打包）",
            "main_path": str(GODV7_MAIN),
            "main_sha256": sha(GODV7_MAIN),
            "files_sha256": {p.name: sha(p) for p in sorted(
                GODV7_MAIN.parent.iterdir()) if p.is_file()},
            "entry": "main.py 末 callable agent(observation, configuration=None)"
                     "（GodModeShopOverlay 包 base_agent.agent）",
            "structure": "main.py 14 行包装 + base_agent.py 5874 行（public V39 系谱"
                         "+RACEPX/RACE/COURIER/CARROT/HERD 尾补层）+ shop_predictor.py "
                         "282 行（hour-23/0 观测→RNG 种子后验→预测未来商店进货）+ "
                         "shop_overlay.py 354 行（种子盲有界改卖单覆盖层）",
            "self_reported_public_score": 2604.3,
            "self_report_note": "上游存档版自报（cell 0），未复核，不引作实测数",
            "license_claim": "Apache-2.0（cell 0 声明；base_agent.py 头含 Apache-2.0 全文"
                             "+thomastschinkel/yhay81/destbreso/aurax7/tetsutani/prvsiyan/"
                             "Gluzdov/Ozer 署名）",
        },
        "source": {
            "commands": [
                "kaggle kernels pull flexonafft/kaggriculture-multi-route-farming-agent"
                " -p /tmp/godv7_pull",
                "（离线解码载荷→fn_docs/hybrid/references/ext/godv7/ 归档，见 provenance.md）",
                "bwrap 沙箱内: python3 orderbook_godv7_lab/judge_godv7.py",
            ],
            "pull_at": "2026-09-30T16:39Z（kernels list 实查 lastRunTime=2026-09-30 "
                       "11:40:14，123 票，id_no 129367546）",
            "sandbox": "bwrap --ro-bind / / --dev /dev --proc /proc --bind /tmp /tmp "
                       "--bind <lab> <lab> --unshare-net（第三方代码仅沙箱内执行）",
            "corpus": {"neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "674000+i*131（i=0..11）；每对 n=12 fold 双席"
                                       "=24 局；同块全对可比",
                       "stagger_note": "任务给定 674000+i*131 与 674000+i*159 二选一，"
                                       "取 131 口径"},
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（两席均分≥1 胜/≤0 负/余平；"
                       "缺席/红局→该 seed 记负 fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径；banks 交叉登记）",
                "terminal_money": "farms[obs.player]",
                "realized_px": "judge_r44._realized_price_stats（挂单量×挂时价/日均价加权，"
                               "参考）",
                "hard_currency": "胜率=硬通货；mean_margin/realized_px 只作参考",
                "loader": "godv7 每局前清 sys.modules{base_agent,shop_overlay,"
                          "shop_predictor}=全新模块态（官方逐局全新解释器语义）；"
                          "对手单文件 j23._load_entry 全新命名空间",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
            "panel_sha256": {k: sha(v) for k, v in PANEL.items()},
            "panel_role": PANEL_ROLE,
        },
        "sim_auth": {},
        "panel": {},
        "criteria": {},
        "verdict": {},
        "budget": {"cap_note": "5 对×12 fold×2 席=120 局 + auth 30×2 轮×2 引擎",
                   "panel_games": 0, "auth_games": 0},
    })
    flush_evid()

    # ---- sim_bridge 认证 30/30 ×2 轮（godv7 侧在环）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    _orig_load = sb._load_agent_file

    def _purging_load(path):
        if Path(os.path.abspath(str(path))).parent == GODV7_MAIN.parent:
            for m in GODV7_MODULES:
                sys.modules.pop(m, None)
        return _orig_load(path)

    sb._load_agent_file = _purging_load   # 进程内 harness 适配（防跨局模块态）
    auth_reports = {}
    auth_ok = True
    for tag, opp in (("godv7_vs_r40", R40), ("godv7_vs_oc_c3", OC3)):
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "agents": [{"type": "python", "path": str(GODV7_MAIN)},
                        {"type": "python", "path": str(opp)}],
             "record_path": str(EVID_DIR / ("sim_auth_record_%s.json" % tag))},
            NEUTRAL_FOLDS + [675000 + i * 131 for i in range(28)])
        lite = {k: auth.get(k) for k in
                ("loaded", "consistency", "consistency_ok", "degraded",
                 "degraded_reason", "engine", "version", "wall_speedup")}
        lite["games_detail"] = auth.get("games")
        auth_reports[tag] = lite
        auth_ok = auth_ok and bool(lite.get("consistency_ok"))
        EV["budget"]["auth_games"] += 30
        flush_evid()
    EV["sim_auth"] = {"rounds": auth_reports,
                      "note": "30/30 对照=官方引擎 vs Rust sim 终局资金一致；"
                              "godv7 两轮均在环（vs r40 与 vs oc_c3），"
                              "引擎对 godv7 的一致性由此覆盖"}
    if not auth_ok:
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未全过 30/30（见 sim_auth）"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "workers": WORKERS,
               "bridge": auth_reports["godv7_vs_oc_c3"]}
    flush_evid()

    # ---- 面板：godv7 vs 5 对手 × 12 fold 双席 ----
    panel_rows = {}
    for on, opath in PANEL.items():
        rows = play(_chunk_panel,
                    unit_specs(GODV7_MAIN, opath, on, NEUTRAL_FOLDS), run_cfg)
        EV["budget"]["panel_games"] += len(rows)
        panel_rows[on] = rows
        st = fold_stats(rows)
        st["pair"] = "godv7 vs %s" % on
        st["role"] = PANEL_ROLE[on]
        EV["panel"][on] = st
        print("panel godv7 vs", on, "h2h=", st["h2h"], "n=", st["n"],
              "err=", st["n_errors"], flush=True)
        flush_evid()
    EV["panel_rows"] = panel_rows

    # ---- 判据 + verdict ----
    h_oc = (EV["panel"].get("oc_c3") or {}).get("h2h")
    h_weak = {o: (EV["panel"].get(o) or {}).get("h2h") for o in ("r40", "A")}
    h_pair = {o: (EV["panel"].get(o) or {}).get("h2h") for o in ("c_final", "s8")}
    n_broken = sum(st["n_errors"] for st in EV["panel"].values())
    if n_broken > 0 and (EV["panel"].get("oc_c3") or {}).get("n_errors", 0) \
            == EV["panel"]["oc_c3"]["n_games"]:
        tier = "UNRUNNABLE"
    elif h_oc is None:
        tier = "UNRUNNABLE"
    elif h_oc >= 0.5:
        tier = "BEATS_CEILING"
    elif h_oc >= 0.35:
        tier = "COMPETITIVE"
    else:
        tier = "WEAK"
    EV["criteria"] = {
        "rule": "对冠军锚 oc_c3 ≥0.5=可能超天花板（BEATS_CEILING）；0.35-0.5="
                "COMPETITIVE；<0.35=WEAK；跑不起来=UNRUNNABLE。弱锚 {r40,A} ≥0.8="
                "弱面正常。mean_margin/realized_px 只作参考。",
        "vs_oc_c3_h2h": h_oc,
        "weak_anchors_h2h": h_weak,
        "weak_face_normal": bool(all((h or 0) >= 0.8 for h in h_weak.values())),
        "vs_current_pair_h2h": h_pair,
        "n_errors_total": n_broken,
    }
    EV["verdict"] = {
        "tier": tier,
        "vs_champion_anchor": {"h2h": h_oc,
                               "read": "≥0.5 可能超天花板 / 0.35-0.5 竞争力 / <0.35 弱"},
        "summary": "godv7 对冠军锚 oc_c3 h2h=%s（n=12 折双席）；弱锚 {%s}；"
                   "现计分对员 {%s}；errors=%d"
                   % (h_oc,
                      ", ".join("%s=%s" % (k, v) for k, v in h_weak.items()),
                      ", ".join("%s=%s" % (k, v) for k, v in h_pair.items()),
                      n_broken),
        "launch": "不发射不提交（判决先行）；发射决策移交用户",
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", tier, EV["verdict"]["summary"], flush=True)
    return EV


if __name__ == "__main__":
    main()
