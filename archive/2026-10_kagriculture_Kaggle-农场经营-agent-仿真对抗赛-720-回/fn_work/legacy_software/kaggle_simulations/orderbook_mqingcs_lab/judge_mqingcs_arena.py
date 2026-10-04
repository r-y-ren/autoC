# -*- coding: utf-8 -*-
"""judge_mqingcs_arena（mqingcs lab）：mqingcs 双策略包池测判决
（判决先行·只测不发·不提交·零修改原始件；dff20b-1）。

件（fn_docs/hybrid/references/ext/monitor-round2-probe/，Apache-2.0，2026-10-03 03:25Z 入库）：
  last_dance = policies/last_dance_56720309.py（11,351 行主策略；末 callable
               final_v40_risk_entry=risk_probation_entry；market 层=对手麦流观测
               +carry 仓位+执行成本下界+realized-loss 检测+有界试用期）
  ld_016/017/019 = 主策略内部组件（unit 语义/收尾规划器/H10 价值原语，
               被 main 以 publication_assets.source() exec 进子命名空间；
               非独立 agent 入口——只做装载验证，不烧局）
  observed* = policies/observed_56713902*.py（缺私有任务库
               KAGGRICULTURE_PRIVATE_ASSETS，预期 UNRUNNABLE——只做装载验证）

上游依赖（degnonguidi/best-agent-ranking kernel output，2026-10-03T06:06Z 实拉）：
  fn_docs/hybrid/references/ext/mqingcs_upstream/kernel_output/main.py
  （1,026,965B sha256 a16e0e9b...d82ab；dependency_spec 4 条 spec 全 UNIQUE-OK，
  见 PROVENANCE.md）。装载器注入 KAGGRICULTURE_UPSTREAM_MAIN；上游文件只被
  AST 解析、永不执行（README 明示语义）。

面板（每对 n=12 fold 双席=24 局，中性块 674000+i*131 i=0..11）：
  件 vs {H1 王座锚（H1/oc_c3 行为孪生，BT 527.8）, mpx, r40（弱锚）, A（弱件锚）}
口径（同 pooltest_arena/exp066/godv7）：h2h=judge_r44._fold_arm 同 seed 双席折叠
（≥1 胜/≤0 负/余平，缺席/红局→该 seed 记负 fail-closed）；margin=干净口径终局钱差；
胜率=硬通货。判决：BEATS_CEILING（vs 王座 H1 h2h≥0.5）/ COMPETITIVE（0.35-0.5）/
WEAK（<0.35）/ UNRUNNABLE（装载失败或红局>20%）。
sim_bridge 认证：composite lab 09-30 30/30 缓存附证 + last_dance 在环 30/30 一轮
（件 vs r40，双引擎逐局终局资金对照）。
第三方代码执行全程 bwrap 沙箱（根只读+/tmp+本 lab 可写+件/上游只读+断网）。
证据 orderbook_mqingcs_lab/evidence/mqingcs_arena.json。只写本 lab。不改既有代码。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
EV_PATH = EVID_DIR / "mqingcs_arena.json"

# ============================================================ 件与上游 ==
PKG_ROOT = REPO / "fn_docs" / "hybrid" / "references" / "ext" / "monitor-round2-probe"
UPSTREAM_MAIN = (PKG_ROOT.parent / "mqingcs_upstream" / "kernel_output"
                 / "main.py")

# ============================================================ 面板件 ==
H1 = KSIM_DIR / "orderbook_topform_lab" / "build" / "h1" / "main.py"
OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
MPX = (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
       / "main.py")
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A = KSIM_DIR / "orderbook_r44_a" / "main.py"

PANEL = {"H1": H1, "mpx": MPX, "r40": R40, "A": A}
PANEL_ROLE = {"H1": "王座锚（H1/oc_c3 行为孪生，BT 527.8）", "mpx": "面板强件",
              "r40": "弱锚", "A": "弱件锚"}

PIECES = {
    "last_dance": {
        "main": PKG_ROOT / "policies" / "last_dance_56720309.py",
        "ref": "mqingcs/kaggressulture-two-policy-source（monitor-round2-probe 包）",
        "license": "Apache-2.0",
        "form": "包内单文件主策略（11,351 行；末 callable "
                "final_v40_risk_entry；经 publication_assets 解析上游常量 "
                "+source() exec 内部组件 _016/_017/_019）",
        "self_reported": "README 明示 'IDs identify the implementations, not "
                         "their rank. No final competition score is claimed.'"
                         "（56720309=实现标识非名次；无自报终榜分）",
        "mode": "arena",
    },
    "ld_016": {
        "main": PKG_ROOT / "policies" / "last_dance_56720309_016.py",
        "ref": "同上（包内组件）",
        "license": "Apache-2.0",
        "form": "主策略内部组件：kaggle-environments 1.32.7 unit/decay 语义"
                "（333 行；被 main exec 进 _UNIT_NS；非 agent 入口）",
        "self_reported": "—（组件，无自报）",
        "mode": "probe",
    },
    "ld_017": {
        "main": PKG_ROOT / "policies" / "last_dance_56720309_017.py",
        "ref": "同上（包内组件）",
        "license": "Apache-2.0",
        "form": "主策略内部组件：E182 末 7 轮物理收尾规划器（392 行；依赖 "
                "_016 命名空间的 FARMER_MOVES；非 agent 入口）",
        "self_reported": "—（组件，无自报）",
        "mode": "probe",
    },
    "ld_019": {
        "main": PKG_ROOT / "policies" / "last_dance_56720309_019.py",
        "ref": "同上（包内组件）",
        "license": "Apache-2.0",
        "form": "主策略内部组件：有界 H10 价值原语（171 行；单细胞午夜规则；"
                "非 agent 入口）",
        "self_reported": "—（组件，无自报）",
        "mode": "probe",
    },
    "observed": {
        "main": PKG_ROOT / "policies" / "observed_56713902.py",
        "ref": "同上（包内策略）",
        "license": "Apache-2.0",
        "form": "两步选购包装器（57 行 contingent_two_step_roles：双专家隔离"
                "命名空间并行喂 obs，step2 按对手≥5 hands+farmer 原位选学习分支）",
        "self_reported": "README：归档对照 16 世界×2 席×16 对手 475/512 vs 成熟"
                         "参考 451/512（自报存档对照非现榜强度）；IDs not rank",
        "mode": "probe",
    },
    "observed_001": {
        "main": PKG_ROOT / "policies" / "observed_56713902_001.py",
        "ref": "同上（包内专家）",
        "license": "Apache-2.0",
        "form": "成熟生产专家（10,625 行；value 键 _001_002/_001_003/_001_006/"
                "_001_008 全可解析=或可装载）",
        "self_reported": "—（分支件，无独立自报）",
        "mode": "probe",
    },
    "observed_009": {
        "main": PKG_ROOT / "policies" / "observed_56713902_009.py",
        "ref": "同上（包内专家）",
        "license": "Apache-2.0",
        "form": "学习生产分支（1,209 行；value 键 observed_56713902_009_010 "
                "不在 policy_parameters 也不在 dependency_spec→预期缺任务库报错）",
        "self_reported": "—（分支件，无独立自报）",
        "mode": "probe",
    },
}

N_FOLDS = int(os.environ.get("MQINGCS_FOLDS", "12"))
PANEL_FOLDS = [674000 + i * 131 for i in range(N_FOLDS)]
WORKERS = int(os.environ.get("MQINGCS_WORKERS", "4"))
RUN_PIECES = [s for s in os.environ.get(
    "MQINGCS_PIECES", "last_dance").split(",") if s]
DO_AUTH = os.environ.get("MQINGCS_AUTH", "1") == "1"
SMOKE = os.environ.get("MQINGCS_SMOKE", "0") == "1"

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


# ==================================================== 装载适配层 ==
def _ensure_env():
    """mqingcs 包装载前置：环境变量注入 + publication_assets 可导入。

    harness 适配层（件本体零修改）：上游 main.py 只被 AST 解析不被执行；
    KAGGRICULTURE_PRIVATE_ASSETS 显式不设（预期 observed 分支报缺库）。
    """
    os.environ["KAGGRICULTURE_UPSTREAM_MAIN"] = str(UPSTREAM_MAIN)
    os.environ.pop("KAGGRICULTURE_PRIVATE_ASSETS", None)
    p = str(PKG_ROOT)
    if p not in sys.path:
        sys.path.insert(0, p)


def load_entry(path):
    """mqingcs 件装载（j23 官方 last-callable 语义 + 包根/环境注入）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    _ensure_env()
    return j23._load_entry(path)


def load_probes():
    """组件/observed 各版本装载验证（不烧局）：exec+末 callable+一次调用探针。"""
    probes = {}
    dummy = {"step": 0, "player": 0, "farms": [], "private": {}, "market": {}}
    for name, meta in PIECES.items():
        if meta["mode"] != "probe":
            continue
        row = {"file": str(meta["main"]), "form": meta["form"],
               "load_s": None, "load_ok": False, "load_error": None,
               "entry": None, "entry_arity": None, "call_probe": None}
        t0 = time.perf_counter()
        try:
            _ensure_env()
            entry = load_entry(meta["main"])
            row["load_s"] = round(time.perf_counter() - t0, 2)
            row["load_ok"] = True
            row["entry"] = getattr(entry, "__name__", type(entry).__name__)
            code = getattr(entry, "__code__", None)
            row["entry_arity"] = (code.co_argcount
                                  if code is not None else None)
            try:
                entry(dummy, {})
                row["call_probe"] = "ok"
            except Exception as exc:
                row["call_probe"] = repr(exc)[:180]
            del entry
        except Exception as exc:
            row["load_s"] = round(time.perf_counter() - t0, 2)
            row["load_error"] = repr(exc)[:300]
            row["load_error_type"] = type(exc).__name__
        probes[name] = row
        print("PROBE:", name, "ok" if row["load_ok"] else "FAIL",
              row.get("load_error") or row.get("entry"), flush=True)
    return probes


# ==================================================== 局跑口 ==
def _chunk(payload):
    """worker：双席 trace 局；干净口径 margin（同 pooltest _chunk）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: E402
    from orderbook_r40 import sim_bridge as sb  # noqa: E402
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    out = []
    for spec in specs:
        load_s = {}
        try:
            agents, sinks = [], ({0: [], 1: []} if spec.get("trace") else None)
            for seat, a in enumerate(spec["agents"]):
                lt = time.perf_counter()
                if a.get("kind") == "piece":
                    inner = load_entry(a.get("path"))
                    load_s["piece_load_s"] = round(time.perf_counter() - lt, 2)
                else:
                    inner = j23._load_entry(a.get("path"))
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
                "game_id": "mq|%s|%s|%d-s%d" % (piece, opp_name, seed, seat),
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
    budget = {"auth_games": 0, "panel_games": 0, "probe_games": 0}
    _ensure_env()

    EV.update({
        "version": "mqingcs-arena/1.0",
        "task": "mqingcs 双策略包池测判决（dff20b-1）：README 明示 IDs not rank、"
                "无自报终榜分——判决只认本池实测（判决先行·只测不发·不提交）",
        "pieces": {k: {kk: (str(vv) if isinstance(vv, Path) else vv)
                       for kk, vv in v.items()}
                   for k, v in PIECES.items()},
        "source": {
            "commands": ["bwrap 沙箱内: python3 orderbook_mqingcs_lab/"
                         "judge_mqingcs_arena.py"],
            "sandbox": "bwrap --ro-bind / / --dev /dev --proc /proc --bind "
                       "/tmp /tmp --bind <mq_lab> <mq_lab> --ro-bind "
                       "<monitor-round2-probe> <monitor-round2-probe> "
                       "--ro-bind <mqingcs_upstream> <mqingcs_upstream> "
                       "--unshare-net（第三方代码仅沙箱内执行；上游 main.py "
                       "只 AST 解析不执行）",
            "env_injection": {
                "KAGGRICULTURE_UPSTREAM_MAIN": str(UPSTREAM_MAIN),
                "KAGGRICULTURE_PRIVATE_ASSETS": "显式不设（包未随私有任务库；"
                                                "observed 分支预期缺库报错）",
                "upstream_sha256": sha256_of(UPSTREAM_MAIN),
                "upstream_provenance": "fn_docs/hybrid/references/ext/"
                                       "mqingcs_upstream/PROVENANCE.md"
                                       "（拉取 2026-10-03T06:06Z；dependency_"
                                       "spec 4 条 UNIQUE-OK）",
            },
            "package_provenance": {
                "path": str(PKG_ROOT),
                "ref": "mqingcs/kaggressulture-two-policy-source",
                "license": "Apache-2.0",
                "archived": "2026-10-03 03:25Z（monitor-round2-probe 入库时间）",
            },
            "corpus": {
                "panel_folds": PANEL_FOLDS,
                "panel_spec": "中性块 674000+i*131（i=0..%d）；每对 n=%d fold"
                              " 双席=%d 局" % (N_FOLDS - 1, N_FOLDS, 2 * N_FOLDS),
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "缺席/红局→该 seed 记负 fail-closed）",
                "margin": "farms[obs.player] 终局钱差（干净口径；banks 交叉登记）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表，"
                               "参考）",
                "hard_currency": "胜率=硬通货；margin/realized_px 只作参考",
                "zero_modification": "件本体零修改；适配仅 harness 层（包根 "
                                     "sys.path 注入+环境变量注入；上游只 AST "
                                     "解析）",
                "fresh_ns_per_game": "每局全新命名空间装载（j23._load_entry；"
                                     "有状态件跨局不残留；publication_assets "
                                     "常量缓存为纯常量、确定性）",
            },
            "panel": {k: {"path": str(v), "sha": sha256_of(v)}
                      for k, v in PANEL.items()},
            "panel_role": PANEL_ROLE,
        },
        "sim_auth": {}, "panel": {}, "verdicts": {}, "load_probes": {},
        "budget": budget, "panel_rows": [],
    })
    flush_evid()

    # ---- 装载验证（组件 + observed 各版本；不烧局）----
    try:
        EV["load_probes"] = load_probes()
    except Exception:
        ANOMALIES.append("load_probes 顶层异常: %s" % traceback.format_exc()[-300:])
    flush_evid()

    if SMOKE:
        # 烟测：last_dance vs r40 单局（official 引擎），计时读数
        rows = play(unit_specs("last_dance", PIECES["last_dance"]["main"],
                               "r40", R40, [PANEL_FOLDS[0]],
                               group="smoke")[:1],
                    {"workers": 1, "engine": "official"})
        budget["probe_games"] += len(rows)
        EV["smoke"] = rows
        flush_evid()
        print("SMOKE:", json.dumps(rows, ensure_ascii=False)[:400], flush=True)
        return EV

    # ---- sim_bridge 认证：composite 30/30 缓存附证 ----
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
    budget["auth_games"] = 30
    flush_evid()

    # sim_bridge 装载适配（mqingcs 件→env/包根注入，进程内 harness 层）
    _orig_load = sb._load_agent_file

    def _env_load(path):
        p = os.path.abspath(str(path))
        for name, meta in PIECES.items():
            if meta.get("main") and p == os.path.abspath(str(meta["main"])):
                _ensure_env()
                break
        return _orig_load(path)

    sb._load_agent_file = _env_load

    all_rows = list(EV.get("panel_rows") or [])
    for piece in RUN_PIECES:
        meta = PIECES[piece]
        p_t0 = time.perf_counter()

        # ---- 装载 preflight ----
        try:
            t_load = time.perf_counter()
            inner = load_entry(meta["main"])
            preflight = {"ok": True,
                         "load_s": round(time.perf_counter() - t_load, 2),
                         "entry": getattr(inner, "__name__",
                                          type(inner).__name__)}
            del inner
        except Exception as exc:
            EV["verdicts"][piece] = {
                "verdict": "UNRUNNABLE",
                "rule": "装载失败或红局>20%",
                "reason": "装载失败: %s" % repr(exc)[:300],
                "load_form": meta["form"], "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交（判决先行）；上线决策移交用户",
            }
            flush_evid()
            print("LOAD-FAIL:", piece, repr(exc)[:120], flush=True)
            continue

        # ---- sim_bridge 在环认证 30/30（件 vs r40，双引擎）----
        piece_auth = None
        if DO_AUTH:
            try:
                piece_auth = sb.sim_bridge(
                    {"n_games": 30, "min_checked": 30,
                     "agents": [{"type": "python",
                                 "path": str(meta["main"])},
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

        # ---- 面板 ----
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
            EV["panel_rows"] = all_rows + piece_rows
            flush_evid()
        all_rows.extend(piece_rows)
        EV["panel_rows"] = all_rows
        EV["panel"][piece] = {
            "design": "%s 对 4 件面板：每对 n=%d fold 双席=%d 局（中性块 "
                      "674000+i*131）" % (piece, N_FOLDS, 2 * N_FOLDS),
            "pairs": panel}

        # ---- 判决 ----
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
        EV["verdicts"][piece] = {
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
        flush_evid()
        print("VERDICT:", piece, verdict, "vs_H1 h2h=", h_h1, flush=True)

    # ---- probe 件判决登记（组件/observed：装载验证即判决，不烧局）----
    for name, probe in (EV.get("load_probes") or {}).items():
        if name in EV["verdicts"]:
            continue
        meta = PIECES[name]
        if not probe.get("load_ok"):
            EV["verdicts"][name] = {
                "verdict": "UNRUNNABLE",
                "rule": "装载失败或红局>20%",
                "reason": "装载失败（缺私有任务库/组件非入口）: %s"
                          % probe.get("load_error"),
                "load_form": meta["form"],
                "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交；observed 分支需授权任务库（DATA_ACCESS）"
                          "方可复现，非本池可裁",
            }
        elif "observed" in name:
            EV["verdicts"][name] = {
                "verdict": "LOAD_OK_UNTESTED",
                "rule": "装载验证通过但按任务纪律不烧局（判决只覆盖 "
                        "last_dance 主版）",
                "reason": "装载通过（%s，arity=%s，调用探针=%s）——可装载但未入池"
                          "测（预算纪律；observed 提交形态=包装器，缺任务库 "
                          "UNRUNNABLE）" % (probe.get("entry"),
                                            probe.get("entry_arity"),
                                            probe.get("call_probe")),
                "load_form": meta["form"],
                "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交；是否补池测移交用户决策",
            }
        else:
            EV["verdicts"][name] = {
                "verdict": "UNRUNNABLE",
                "rule": "组件模块非 agent 入口（被主策略 exec 复用；独立无游戏"
                        "语义）",
                "reason": "装载通过但末 callable=%s（arity=%s）非 "
                          "agent(obs, configuration) 入口；调用探针=%s"
                          % (probe.get("entry"), probe.get("entry_arity"),
                             probe.get("call_probe")),
                "load_form": meta["form"],
                "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "组件件不单独判决；机制已随 last_dance 主版整体入池",
            }
    EV["verdicts"] = dict(EV["verdicts"])
    n_pp_auth = len((EV.get("sim_auth") or {}).get("per_piece") or {})
    budget["auth_games"] = 30 + 30 * n_pp_auth
    budget["panel_games"] = len(all_rows)
    budget["total_局次"] = budget["auth_games"] + budget["panel_games"] \
        + budget["probe_games"]
    budget["note"] = ("局次=终局实数重算（baseline 认证 30 + last_dance 在环认证 "
                      "30×%d + 逐局行 %d + 烟测/探针 %d）"
                      % (n_pp_auth, len(all_rows), budget["probe_games"]))
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货，margin/realized_px 只作"
                     "参考；Never quote the peak；读数=本池实测")
    ANOMALIES.append("自报≠可迁移：README 明示 'IDs identify the implementations, "
                     "not their rank'（56720309/56713902=实现标识非名次，无自报"
                     "终榜分）；归档对照 475/512 为自报存档数、只登记")
    ANOMALIES.append("面板口径与 pooltest_arena/exp066/godv7 同构（674000+i*131、"
                     "_fold_arm、干净 margin、H1 王座锚）——与 syx/taeyan/"
                     "romansvet 判决可直接横比")
    ANOMALIES.append("装载语义=官方 last-callable（全新命名空间逐局装载）+harness "
                     "层包根 sys.path 与 KAGGRICULTURE_UPSTREAM_MAIN 注入（件本体"
                     "零修改）；上游 main.py 只 AST 解析不执行")
    ANOMALIES.append("last_dance 内部组件 _016/_017/_019 非独立 agent（被主文件 "
                     "source() exec）；observed 缺私有任务库 KAGGRICULTURE_"
                     "PRIVATE_ASSETS——均只做装载验证不烧局")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
