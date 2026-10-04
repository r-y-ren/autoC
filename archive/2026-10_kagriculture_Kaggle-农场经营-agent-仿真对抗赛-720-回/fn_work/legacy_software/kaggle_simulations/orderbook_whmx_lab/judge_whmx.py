# -*- coding: utf-8 -*-
"""judge_whmx（whmx lab）：WHmaoxian123 归档仓终件候选 12-fold 快筛判决
（判决先行·只测不发·不提交·零修改原始件）。

件（harvest 2026-10-03，repo_full HEAD ed63c7f6 clone；tar 内 main.py 与 loose
byte-identical 已核）：
  r3   = submissions/release_v10_r3（README 自报"未上传"；R5 README 称线上 56683134
         = R3 重交版）——main.py 44c46360；入口 kaggle_endx_submission_agent
  r4_2 = submissions/release_v10_r4_2（自报线上终席 56683114）——main.py b72c9a5b；
         入口 kaggle_hpx2_final_agent（last callable）
  r5   = submissions/release_v10_r5（README 自报"本地验证通过，Claude 未上传"、
         终两席=R4.2+R5；main.py sha 5f7e6ef3 与 README 自报逐字符一致）
         ——入口 kaggle_hpx2_final_agent（last callable）

面板（每对 n=12 fold 双席=24 局，中性块 674000+i*131 i=0..11）：
  件 vs {H1 王座锚（H1/oc_c3 行为孪生，BT 527.8）, mpx, r40（弱锚）, A（弱件锚）}
口径（同 pooltest_arena/exp066/godv7）：h2h=judge_r44._fold_arm 同 seed 双席折叠
（≥1 胜/≤0 负/余平，缺席/红局→该 seed 记负 fail-closed）；margin=farms[obs.player]
终局钱差（干净口径，banks 交叉登记）；realized_px=Σ(qty×卖时价)/Σ(qty×base)
（BASE_PX milkwin 表，参考）；胜率=硬通货。判决四档：BEATS_CEILING（vs 王座 H1
h2h≥0.5）/ COMPETITIVE（0.35-0.5）/ WEAK（<0.35）/ UNRUNNABLE（装载失败或红局>20%）。
sim_bridge 认证：composite 09-30 30/30 缓存附证 + 每件在环 30/30 一轮（件 vs r40）。
第三方代码执行全程 bwrap 沙箱（根只读+/tmp+本 lab 可写+断网）。证据
orderbook_whmx_lab/evidence/whmx_screen.json。只写本 lab。不改既有代码。
许可注：三件均在仓内逐件 Apache-2.0 LICENSE.txt 覆盖目录（submissions/*），快筛属
Apache-2.0 明示允许的执行/评估用途；裁定书另行（references/2026-10-03-whmaoxian-
license-harvest.md）。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
EV_PATH = EVID_DIR / "whmx_screen.json"
PIECES_DIR = HERE / "pieces"

# ============================================================ 面板件 ==
H1 = KSIM_DIR / "orderbook_topform_lab" / "build" / "h1" / "main.py"
MPX = (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
       / "main.py")
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A = KSIM_DIR / "orderbook_r44_a" / "main.py"

PANEL = {"H1": H1, "mpx": MPX, "r40": R40, "A": A}
PANEL_ROLE = {"H1": "王座锚（H1/oc_c3 行为孪生，BT 527.8）", "mpx": "面板强件",
              "r40": "弱锚", "A": "弱件锚"}

# ============================================================ 测件 ==
HARVEST = ("fn_docs/hybrid/references/ext/whmaoxian_harvest/repo_full "
           "(git clone --depth 1 HEAD ed63c7f6321198c310b80e0e86c131432c47f175, "
           "2026-10-03 ~06:1xZ)")
PIECES = {
    "r3": {
        "main": PIECES_DIR / "r3" / "main.py",
        "repo": "https://github.com/WHmaoxian123/kaggriculture",
        "path_in_repo": "project/submissions/release_v10_r3/main.py",
        "commit": "ed63c7f6321198c310b80e0e86c131432c47f175",
        "license": "Apache-2.0（submissions/release_v10_r3/LICENSE.txt 逐件）",
        "form": "整包单文件（main.py 1,103,4xxB，纯标准库 base64/copy/itertools/"
                "json/math/random/zlib；252 个顶层 def）",
        "self_reported": "自报未上传；R5 README 称线上 56683134=R3 重交版；"
                         "入口 endx_agent（末命名空间 kaggle_endx_submission_agent）",
        "load_mode": "direct",
    },
    "r4_2": {
        "main": PIECES_DIR / "r4_2" / "main.py",
        "repo": "https://github.com/WHmaoxian123/kaggriculture",
        "path_in_repo": "project/submissions/release_v10_r4_2/main.py",
        "commit": "ed63c7f6321198c310b80e0e86c131432c47f175",
        "license": "Apache-2.0（submissions/release_v10_r4_2/LICENSE.txt 逐件）",
        "form": "整包单文件（main.py 1,102,6xxB，纯标准库；258 个顶层 def）",
        "self_reported": "自报线上终席 56683114（R4.2）；固定商店重打 186 局 "
                         "113W73L（自报）",
        "load_mode": "direct",
    },
    "r5": {
        "main": PIECES_DIR / "r5" / "main.py",
        "repo": "https://github.com/WHmaoxian123/kaggriculture",
        "path_in_repo": "project/submissions/release_v10_r5/main.py",
        "commit": "ed63c7f6321198c310b80e0e86c131432c47f175",
        "license": "Apache-2.0（submissions/release_v10_r5/LICENSE.txt 逐件）",
        "form": "整包单文件（main.py 1,102,204B，纯标准库；258 个顶层 def；"
                "sha256 与仓 README 自报逐字符一致）",
        "self_reported": "自报'本地验证通过，Claude 未上传'；终两席=R4.2(56683114)"
                         "+R5（意图替换 56683134）",
        "load_mode": "direct",
    },
}

SHA_PANEL = {}
N_FOLDS = int(os.environ.get("WHMX_FOLDS", "12"))
PANEL_FOLDS = [674000 + i * 131 for i in range(N_FOLDS)]
WORKERS = int(os.environ.get("WHMX_WORKERS", "3"))
RUN_PIECES = [s for s in os.environ.get("WHMX_PIECES", "r3,r4_2,r5").split(",")
              if s]
DO_AUTH = os.environ.get("WHMX_AUTH", "1") == "1"

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    EV_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                  default=str) + "\n", encoding="utf-8")


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ==================================================== 局跑口 ==
def _chunk(payload):
    """worker：双席 trace 局；干净口径 margin（同 pooltest _chunk）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    out = []
    for spec in specs:
        load_s = {}
        try:
            agents, sinks = [], ({0: [], 1: []} if spec.get("trace") else None)
            for seat, a in enumerate(spec["agents"]):
                lt = time.perf_counter()
                inner = j23._load_entry(a.get("path"))
                if a.get("kind") == "piece":
                    load_s["piece_load_s"] = round(time.perf_counter() - lt, 2)
                if sinks is not None:
                    agents.append(j23._Tracer(inner, seat, sinks[seat]))
                else:
                    agents.append(inner)
            res = sb.run_games([{"seed": int(spec["seed"]),
                                 "agents": agents}], cfg)
            rr = (res.get("games") or [{}])[0]
            berr = None
        except Exception as exc:
            res, rr, sinks, berr = {"engine": None}, {}, None, \
                repr(exc)[:160]
        row = {"game_id": spec.get("game_id"), "piece": spec.get("piece"),
               "seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"), "group": spec.get("group"),
               "engine": res.get("engine"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None,
               "rpx_us": None, "rpx_opp": None}
        row.update(load_s)
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
                row["rpx_us"] = realized_px(sinks[row["seat"]])
                row["rpx_opp"] = realized_px(sinks[1 - row["seat"]])
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


def realized_px(sink):
    """提交口径实现价：Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表）。"""
    val = 0.0
    base = 0.0
    for _step, obs, act in (sink or []):
        if not isinstance(act, dict):
            continue
        prices = ((obs.get('market') or {}) if isinstance(obs.get('market'),
                  dict) else {}).get('prices') or {}
        for cmd in (act.get('market') or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                item = str(cmd[1])
                px = prices.get(item)
                try:
                    q = float(cmd[2])
                except Exception:
                    continue
                b = float(BASE_PX.get(item, 0) or 0)
                if isinstance(px, (int, float)) and q > 0 and b > 0:
                    val += q * float(px)
                    base += q * b
    return round(val / base, 4) if base > 0 else None


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(piece, piece_path, opp_name, opp_path, folds, group="panel"):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            specs.append({
                "game_id": "wx|%s|%s|%d-s%d" % (piece, opp_name, seed, seat),
                "seed": int(seed), "piece": piece, "our_seat": seat,
                "opponent": opp_name, "group": group,
                "trace": True,
                "agents": [{"type": "python", "path": str(piece_path),
                            "kind": "piece"},
                           {"type": "python", "path": str(opp_path),
                            "kind": "opp"}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows
           if isinstance(r.get("tm_opp"), (int, float))]
    rpx_u = [r["rpx_us"] for r in rows
             if isinstance(r.get("rpx_us"), (int, float))]
    rpx_o = [r["rpx_opp"] for r in rows
             if isinstance(r.get("rpx_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin"] = round(sum(r["margin_clean"] for r in rows
                                 if r["margin_clean"] is not None)
                             / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["realized_px_us"] = round(sum(rpx_u) / len(rpx_u), 4) if rpx_u else None
    f["realized_px_opp"] = round(sum(rpx_o) / len(rpx_o), 4) if rpx_o else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    loads = [r["piece_load_s"] for r in rows
             if isinstance(r.get("piece_load_s"), (int, float))]
    f["piece_load_s_mean"] = round(sum(loads) / len(loads), 2) if loads else None
    return f


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"auth_games": 0, "panel_games": 0}

    prior = None
    if os.environ.get("WHMX_RESUME") == "1" and EV_PATH.is_file():
        try:
            prior = json.loads(EV_PATH.read_text(encoding="utf-8"))
        except Exception:
            prior = None

    EV.update({
        "version": "whmx-screen/1.0",
        "task": "WHmaoxian123 归档仓终件候选 12-fold 快筛判决（dff20b-3 "
                "选择性收割·候选初筛）：自报≠可迁移，判决只认本池实测",
        "pieces": {k: {kk: (str(vv) if isinstance(vv, Path) else vv)
                       for kk, vv in v.items()} for k, v in PIECES.items()},
        "source": {
            "commands": ["bwrap 沙箱内: python3 orderbook_whmx_lab/"
                         "judge_whmx.py"],
            "sandbox": "bwrap --ro-bind / / --dev /dev --proc /proc --bind /tmp"
                       " /tmp --bind <lab> <lab> --unshare-net（第三方代码仅"
                       "沙箱内执行）",
            "harvest_ref": HARVEST + "; 报告 references/2026-10-03-whmaoxian-"
                                     "license-harvest.md",
            "corpus": {
                "panel_folds": PANEL_FOLDS,
                "panel_spec": "中性块 674000+i*131（i=0..%d）；每对 n=%d fold 双席"
                              "=%d 局" % (N_FOLDS - 1, N_FOLDS, 2 * N_FOLDS),
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "缺席/红局→该 seed 记负 fail-closed）",
                "margin": "farms[obs.player] 终局钱差（干净口径；banks 交叉登记）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表，"
                               "参考）",
                "hard_currency": "胜率=硬通货；margin/realized_px 只作参考",
                "zero_modification": "件本体零修改；pieces/ 为 repo_full 提交目录"
                                     "main.py 原样拷贝（tar 内 byte-identical 已核）",
                "fresh_ns_per_game": "每局全新命名空间装载（j23._load_entry；有"
                                     "状态件跨局不残留）",
            },
            "panel": {k: {"path": str(v), "sha": SHA_PANEL.get(k)}
                      for k, v in PANEL.items()},
            "panel_role": PANEL_ROLE,
        },
        "sim_auth": {}, "panel": {}, "verdicts": {}, "budget": budget,
        "panel_rows": [],
    })
    for k, v in PANEL.items():
        try:
            SHA_PANEL[k] = sha256_of(v)
        except Exception:
            SHA_PANEL[k] = None
    EV["source"]["panel"] = {k: {"path": str(v), "sha": SHA_PANEL.get(k)}
                            for k, v in PANEL.items()}
    # 件 sha
    EV["piece_sha256"] = {k: sha256_of(m["main"]) for k, m in PIECES.items()
                          if m.get("main")}
    if prior:
        EV["sim_auth"] = prior.get("sim_auth") or {}
        EV["panel"] = prior.get("panel") or {}
        EV["verdicts"] = prior.get("verdicts") or {}
        EV["panel_rows"] = prior.get("panel_rows") or []
        EV["piece_sha256"] = prior.get("piece_sha256") or EV["piece_sha256"]
        if isinstance(prior.get("budget"), dict):
            budget.update(prior["budget"])
        global RUN_PIECES
        RUN_PIECES = [p for p in RUN_PIECES if p not in EV["verdicts"]]
        ANOMALIES.append("WHMX_RESUME=1 断点续跑：并入既有证据，重跑 %s"
                         % (",".join(RUN_PIECES) or "无"))
    flush_evid()

    from orderbook_r40 import sim_bridge as sb  # noqa: E402
    AUTH_CACHE = (KSIM_DIR / "orderbook_composite_lab" / "evidence"
                  / "sim_auth_cache.json")
    base_auth = None
    if AUTH_CACHE.is_file():
        try:
            base_auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        except Exception:
            base_auth = None
    EV["sim_auth"]["baseline_cache"] = {
        "reused_cache": True, "cache_path": str(AUTH_CACHE),
        "loaded": (base_auth or {}).get("loaded"),
        "consistency": (base_auth or {}).get("consistency"),
        "consistency_ok": (base_auth or {}).get("consistency_ok"),
        "engine": (base_auth or {}).get("engine"),
        "version": (base_auth or {}).get("version"),
        "wall_speedup": (base_auth or {}).get("wall_speedup")}
    if not prior:
        budget["auth_games"] = 30
    flush_evid()

    all_rows = list(EV.get("panel_rows") or [])
    verdicts = dict(EV.get("verdicts") or {})
    for piece in RUN_PIECES:
        meta = PIECES[piece]
        p_t0 = time.perf_counter()

        try:
            t_load = time.perf_counter()
            inner = jg.__dict__  # noqa: F841 placeholder
            from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
            inner = j23._load_entry(meta["main"])
            preflight = {"ok": True,
                         "load_s": round(time.perf_counter() - t_load, 2),
                         "entry": getattr(inner, "__name__",
                                          type(inner).__name__)}
            del inner
        except Exception as exc:
            verdicts[piece] = {
                "verdict": "UNRUNNABLE",
                "rule": "装载失败或红局>20%",
                "reason": "装载失败: %s" % repr(exc)[:300],
                "load_form": meta["form"], "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交（判决先行）；上线决策移交用户",
            }
            EV["verdicts"] = verdicts
            flush_evid()
            print("LOAD-FAIL:", piece, repr(exc)[:120], flush=True)
            continue

        piece_auth = None
        if DO_AUTH:
            try:
                piece_auth = sb.sim_bridge(
                    {"n_games": 30, "min_checked": 30,
                     "agents": [{"type": "python", "path": str(meta["main"])},
                                {"type": "python", "path": str(R40)}],
                     "record_path": str(EVID_DIR / ("sim_auth_record_%s.json"
                                                    % piece))},
                    PANEL_FOLDS + [675000 + i * 131 for i in range(28)])
                budget["auth_games"] += 30
            except Exception as exc:
                piece_auth = {"loaded": False, "consistency_ok": False,
                              "error": repr(exc)[:200]}
            EV["sim_auth"]["per_piece"] = EV["sim_auth"].get("per_piece", {})
            EV["sim_auth"]["per_piece"][piece] = {
                k: piece_auth.get(k) for k in
                ("loaded", "consistency", "consistency_ok", "degraded",
                 "degraded_reason", "engine", "version", "wall_speedup")}
        auth = piece_auth if (piece_auth and piece_auth.get("loaded")
                              and piece_auth.get("consistency_ok")) \
            else base_auth
        run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS,
                   "record_path": str(EVID_DIR / "sim_bridge_degraded.json")}
        flush_evid()

        panel = {}
        piece_rows = []
        for on, opath in PANEL.items():
            rows = play(unit_specs(piece, meta["main"], on, opath,
                                   PANEL_FOLDS), run_cfg)
            budget["panel_games"] += len(rows)
            piece_rows.extend(rows)
            panel[on] = fold_stats(rows)
            print("panel %s vs %s h2h=%s W/L/T=%s/%s/%s err=%d" %
                  (piece, on, panel[on]["h2h"], panel[on]["wins"],
                   panel[on]["losses"], panel[on]["ties"],
                   panel[on]["n_errors"]), flush=True)
            flush_evid()
        all_rows.extend(piece_rows)
        EV["panel_rows"] = all_rows
        EV["panel"][piece] = {
            "design": "%s 对 4 件面板：每对 n=%d fold 双席=%d 局（中性块 "
                      "674000+i*131）" % (piece, N_FOLDS, 2 * N_FOLDS),
            "pairs": panel}

        h_h1 = (panel.get("H1") or {}).get("h2h")
        n_err = sum((panel.get(o) or {}).get("n_errors", 0) for o in PANEL)
        n_tot = sum((panel.get(o) or {}).get("n_games", 0) for o in PANEL)
        if h_h1 is None or (n_tot and n_err / n_tot > 0.2):
            verdict = "UNRUNNABLE"
        elif h_h1 >= 0.5:
            verdict = "BEATS_CEILING"
        elif h_h1 >= 0.35:
            verdict = "COMPETITIVE"
        else:
            verdict = "WEAK"
        verdicts[piece] = {
            "verdict": verdict,
            "rule": "BEATS_CEILING=vs 王座 H1 h2h≥0.5 / COMPETITIVE=0.35-0.5 / "
                    "WEAK=<0.35 / UNRUNNABLE=装载失败或红局>20%",
            "vs_H1_h2h": h_h1,
            "panel_h2h": {o: (panel.get(o) or {}).get("h2h") for o in PANEL},
            "panel_WLT": {o: [panel[o]["wins"], panel[o]["losses"],
                              panel[o]["ties"]] for o in PANEL},
            "mean_margin_vs_H1": (panel.get("H1") or {}).get("mean_margin"),
            "realized_px_vs_H1": {
                "us": (panel.get("H1") or {}).get("realized_px_us"),
                "opp": (panel.get("H1") or {}).get("realized_px_opp")},
            "n_games": n_tot, "n_errors": n_err,
            "preflight": preflight,
            "load_form": meta["form"],
            "self_reported": meta["self_reported"],
            "piece_elapsed_s": round(time.perf_counter() - p_t0, 1),
            "launch": "不发射不提交（判决先行）；上线决策移交用户",
        }
        EV["verdicts"] = verdicts
        flush_evid()
        print("VERDICT:", piece, verdict, "vs_H1 h2h=", h_h1, flush=True)

    EV["verdicts"] = verdicts
    n_pp_auth = len((EV.get("sim_auth") or {}).get("per_piece") or {})
    budget["auth_games"] = 30 + 30 * n_pp_auth
    budget["panel_games"] = len(all_rows)
    budget["total_局次"] = budget["auth_games"] + budget["panel_games"]
    budget["note"] = ("局次=终局实数重算（baseline 认证 30 + 每件在环认证 30×%d "
                      "+ 逐局行 %d）" % (n_pp_auth, len(all_rows)))
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货；Never quote the peak；"
                     "读数=本池实测，自报数字只登记")
    ANOMALIES.append("自报≠可迁移：WHmaoxian123 一切线上分数/提交号（1290.1/"
                     "56683114/56683134 等）均为自报，平台侧未核")
    ANOMALIES.append("面板口径与 pooltest_arena/exp066_arena/godv7_arena 同构"
                     "（674000+i*131、_fold_arm、干净 margin）")
    ANOMALIES.append("许可注：三件均来自仓内逐件 Apache-2.0 LICENSE.txt 覆盖目录；"
                     "根级无许可的裁定另行（license-harvest 报告）")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
