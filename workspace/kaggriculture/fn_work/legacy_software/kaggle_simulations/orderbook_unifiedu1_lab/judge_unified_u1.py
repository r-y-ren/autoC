# -*- coding: utf-8 -*-
"""judge_unified_u1：U1 统一求解核判决（全替换形态；判决先行·不发射不提交）。

责任口径（任务 unified-u1）：
- 形态=u1（基底 oc_c3 sha 3f8b57fd…；MODELPX 整个决策规则 8 站点全替换为
  单一求解核：何时卖=窗内剩余可卖拍投影峰值/末拍清剩余，卖多少=min(帽
  3/6/10, MR≤0 截止量)；mpx 窗语义内化=可卖拍 step∈[144,648)∧hour 14..22；
  胜位守卫沿 expx_v2=648 后回基线+滞留保险）。
- 门禁四门（load/health/determinism/identity，knee 范式；identity 适配内层
  手术=反替换回程封印+门字面量不动替代 h1 前缀恒等）+ 足迹审计门（轨道 2
  范式：非触发拍零足迹/首差异拍=首个决策差异拍/决策差异拍全落 [144,695]）。
- 主判=u1 vs mpx 胜者件 mpx_w24_p2_3_h14（sha f0101de9…）；参照=u1 vs oc_c3
  + mpx vs oc_c3（同语料复测 mpx 窗差）。语料=26 败局前 8 fold + 新中性
  673000+i*123×8，n=16 双席=32 (seed,seat) 单元/臂；对手 j23.DEFAULT_
  OPPONENTS 按 fold 轮转；h2h=u1 与 mpx 直接同局双席 32 格。
- 判据：h2h vs mpx ≥0.55 ∧ flips_neg==0 ∧ 实现价非负（配对 Δratio_fill 三品
  ∧全品均值≥0）∧ 窗差 ≥ mpx（d14-27 窗 step 336-648 fill 口径配对 Δ，u1 vs
  oc_c3 ≥ mpx vs oc_c3）。
- 读数：终局钱 farms[obs.player].money（干净口径）；margin=banks[our]−banks
  [opp]；实现价=Σ(filled×成交价)/Σ(filled×base)（膝点表口径）。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤300 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-30-unified-u1.json；账本落
orderbook_unifiedu1_lab/evidence/。复用（不改写）：judge_milkwin 读数/影子
引擎/配对聚合、judge_r23.DEFAULT_OPPONENTS、sim_bridge.run_games/sim_bridge、
gate_launch_fourgate_l1._redirect_check。只写 orderbook_unifiedu1_lab/ 与
该证据文件。
"""
from __future__ import annotations

import hashlib
import io
import json
import multiprocessing
import os
import statistics
import sys
import tarfile
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
L1_DIR = str(KSIM_DIR / "orderbook_l1_derivative")
for _p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_milkwin_lab"),
           str(MODULE_DIR), L1_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_milkwin as jm  # noqa: E402

RECORD_VERSION = "unified-u1/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24

LOSS_FOLDS = list(jm.REPLAY_26[:8])
NEUTRAL_FOLDS = [673000 + i * 123 for i in range(8)]   # 任务给定新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS                     # n=16 双席 fold

# d14-27 窗（mpx 胜者件口径 step 336-648）→ 影子引擎窗口径热替换
jm.WINDOW = (336, 648)
jm.WIN_DAYS = tuple(range(14, 27))
WINDOW_LABEL = "d14-27（step 336-648）"

MX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
BASE_PX = jm.BASE_PX

OC_C3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
                 / "main.py")
OC_C3_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d"
                      "39ba9bd23d")
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
               / "main.py")
MPX_SHA_EXPECTED = ("f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc7"
                    "2c3d84e44f")
U1_MAIN = str(MODULE_DIR / "build" / "u1" / "main.py")
ARMS = {"oc_c3": OC_C3_MAIN, "mpx_w24_p2_3_h14": MPX_MAIN, "u1": U1_MAIN}
RUN_FORMS = ("oc_c3", "mpx_w24_p2_3_h14", "u1")
ENTRY_NAME = "_u1_agent"
MODELPX_WINDOW = (144, 695)      # 足迹卫生台账口径（决策差异拍全落窗内）

WORKERS = 2
BUDGET_CAP_GAMES = 300
EPISODE_SEEDS = (101, 102)
STEP_BUDGET_MS = 1000.0
SIZE_CAP_BYTES = 100 * 1024 * 1024
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-unified-u1.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_u1_ledger.json"

EV: Dict[str, Any] = {}
ANOMALIES: List[str] = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------ 装载/追踪 --
def _load_agent_u1(path):
    """单文件件装载（末 callable 语义）+ 台账报告（_U1_REPORT/_MX_REPORT）。"""
    p = os.path.abspath(str(path))
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns: Dict[str, Any] = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError("%s 装载后无 callable" % p)
    reports = {k: ns[k] for k in ("_U1_REPORT", "_MX_REPORT")
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


class _Tracer(jm._Tracer):
    pass


def _build_agents(spec):
    out = []
    sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        inner, reports = _load_agent_u1(a["path"])
        out.append(_Tracer(inner, seat, sinks[seat], reports))
    return out, sinks


def u1_reads(sink) -> Dict[str, Any]:
    """u1 台账末拍累计（step0 复位→末拍=局总量）。"""
    last = None
    for entry in (sink or []):
        tel = entry[3] if len(entry) > 3 else None
        if isinstance(tel, dict) and isinstance(tel.get("_U1_REPORT"), dict):
            last = tel["_U1_REPORT"]
    return dict(last) if isinstance(last, dict) else {"present": False}


# ------------------------------------------------------------ 局跑口 --
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
    rows: List[Dict[str, Any]] = []
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
                   else "neutral_673000_i123")
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
            "game_id": "u1-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


def make_specs_h2h(units):
    """h2h：u1 与 mpx 胜者件直接同局；双席对调。"""
    specs = []
    for r in units:
        agents = [{"type": "python", "path": U1_MAIN},
                  {"type": "python", "path": MPX_MAIN}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "u1h2h-%d-s%d" % (int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": "u1_h2h_vs_mpx",
            "our_seat": int(r["seat"]), "trace": True,
            "opponent": "mpx_w24_p2_3_h14", "stratum": r.get("stratum"),
            "agents": agents})
    return specs


# ------------------------------------------------------------ 足迹审计 --
def footprint_audit(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """轨道 2 范式：u1 vs oc_c3 同 (seed,seat) 逐拍动作流对比 + 影子基线决策
    台账（非触发拍零足迹；首差异拍=首个决策差异拍；级联差异允许）。"""
    cells = []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        if not rc or not rv or rc.get("stream") is None or rv.get("stream") \
                is None:
            continue
        sc, sv = rc["stream"], rv["stream"]
        diffs = []
        for i in range(min(len(sc), len(sv))):
            if json.dumps(sc[i], default=str, sort_keys=True) != \
                    json.dumps(sv[i], default=str, sort_keys=True):
                diffs.append(i)
        first_diff = diffs[0] if diffs else None
        targets = sorted(int(s) for s in
                         ((rv.get("u1") or {}).get("decision_diff_steps")
                          or []))
        target_first = targets[0] if targets else None
        hygiene_ok = all(MODELPX_WINDOW[0] <= s <= MODELPX_WINDOW[1]
                         for s in targets)
        if targets:
            consistent = (first_diff == target_first)
            non_target_zero = bool(first_diff is not None
                                   and first_diff >= target_first)
        else:
            consistent = (first_diff is None)
            non_target_zero = (len(diffs) == 0)
        cells.append({
            "seed": u["seed"], "seat": u["seat"], "stratum": u.get("stratum"),
            "n_ticks": min(len(sc), len(sv)),
            "n_stream_diff": len(diffs),
            "first_diff_step": first_diff,
            "decision_diff_steps": targets[:20],
            "n_decision_diff_steps": len(targets),
            "first_decision_diff_step": target_first,
            "non_target_zero_footprint": bool(non_target_zero),
            "first_diff_matches_first_decision_diff": bool(consistent),
            "decision_steps_in_modelpx_window": bool(hygiene_ok),
            "stream_sha_u1": rv.get("stream_sha_our"),
            "stream_sha_oc_c3": rc.get("stream_sha_our"),
            "passed": bool(non_target_zero and consistent and hygiene_ok),
        })
    n_pass = sum(1 for c in cells if c["passed"])
    return {
        "design": "同 (seed,seat) 双臂新跑我席逐拍动作流对比 + u1 影子基线决策"
                  "台账（同拍并行算基座 p_next/量帽决策）",
        "rule": "非触发拍零足迹（决策一致拍动作流逐字节同）；首差异拍=首个"
                "决策差异拍（级联差异允许落其后）；决策差异拍全落 MODELPX 窗"
                "[144,695]",
        "n_cells": len(cells), "n_passed": n_pass,
        "gate_passed": bool(cells and n_pass == len(cells)),
        "cells_lite": [{k: c[k] for k in
                        ("seed", "seat", "n_stream_diff", "first_diff_step",
                         "first_decision_diff_step", "n_decision_diff_steps",
                         "passed")}
                       for c in cells],
    }


# ------------------------------------------------------------ 实现价配对 --
def realized_paired3(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """实现价配对 Δ（var−ctl；fill 口径 ratio）：全品 + 三品逐品。"""
    out: Dict[str, Any] = {}
    for tag, item in (("all", None), ("MILK", "MILK"), ("WOOL", "WOOL"),
                      ("STRAWBERRY", "STRAWBERRY")):
        deltas = []
        for u in units:
            key = (u["seed"], u["seat"])
            rc, rv = ctl.get(key), var.get(key)
            if not rc or not rv:
                continue
            vc, vv = jm._ratio_row(rc, item), jm._ratio_row(rv, item)
            if vc is None or vv is None:
                continue
            deltas.append(float(vv) - float(vc))
        out[tag] = {
            "n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 4) if deltas
            else UNKNOWN,
            "median_delta": round(statistics.median(deltas), 4) if deltas
            else UNKNOWN,
            "n_up": sum(1 for d in deltas if d > 0),
            "nonneg": bool(deltas and (sum(deltas) / len(deltas)) >= 0)}
    out["nonneg_all_three"] = bool(
        out["all"]["nonneg"] and out["MILK"]["nonneg"] and out["WOOL"]["nonneg"]
        and out["STRAWBERRY"]["nonneg"])
    return out


# ------------------------------------------------------------ 四门门禁 --
def _gate_load(pkg):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(os.path.join(pkg, "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
    return {"passed": True, "entry": name}


def _run_episode(pkg, seed):
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(pkg)
    return check.run_full_episode(int(seed))


def _gate_health(pkg):
    eps = [_run_episode(pkg, s) for s in EPISODE_SEEDS]
    details = []
    ok = True
    for ep in eps:
        statuses = list(ep.get("statuses") or [])
        rewards = list(ep.get("rewards") or [])
        step_ms = ep.get("max_step_ms")
        turns = ep.get("turns_played")
        good = (statuses == ["DONE", "DONE"] and len(rewards) == 2
                and all(is_num(r) and abs(float(r)) < 1e12 for r in rewards)
                and is_num(step_ms) and float(step_ms) < STEP_BUDGET_MS
                and turns == 720)
        ok = ok and good
        details.append({"seed": ep.get("seed"), "statuses": statuses,
                        "turns_played": turns, "max_step_ms": step_ms,
                        "p99_step_ms": ep.get("p99_step_ms"),
                        "passed": good})
    return {"passed": ok, "step_budget_ms": STEP_BUDGET_MS,
            "episodes": details}


def _gate_determinism(pkg):
    e1 = _run_episode(pkg, EPISODE_SEEDS[0])
    e2 = _run_episode(pkg, EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": ok, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity(pkg):
    """identity（内层手术适配）：tar 完整性 + 反替换回程封印 + 门字面量不动。"""
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
        "size_lt_100mb": len(tar_bytes) < SIZE_CAP_BYTES,
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
    }
    return {"passed": all(checks.values()), "checks": checks,
            "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members, "base_main_sha256": base_sha,
            "injected_tail_bytes": len(main_bytes) - len(base)}


def run_gates() -> Dict[str, Any]:
    pkg = str(MODULE_DIR / "build" / "u1")
    res: Dict[str, Any] = {}
    for gname, fn in (("load", lambda p=pkg: _gate_load(p)),
                      ("health", lambda p=pkg: _gate_health(p)),
                      ("determinism", lambda p=pkg: _gate_determinism(p))):
        try:
            res[gname] = fn()
        except Exception as exc:
            res[gname] = {"passed": False, "error": repr(exc)[:200]}
    try:
        res["identity"] = _gate_identity(pkg)
    except Exception as exc:
        res["identity"] = {"passed": False, "error": repr(exc)[:200]}
    res["overall"] = all(g.get("passed") for g in res.values())
    return res


# ------------------------------------------------------------ main --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    mpx_sha = hashlib.sha256(Path(MPX_MAIN).read_bytes()).hexdigest()
    if mpx_sha != MPX_SHA_EXPECTED:
        raise RuntimeError("mpx 胜者件 sha 漂移：%s" % mpx_sha)
    man = json.loads((MODULE_DIR / "build" / "u1" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    u1_sha = hashlib.sha256(Path(U1_MAIN).read_bytes()).hexdigest()
    if u1_sha != man.get("main_sha256"):
        raise RuntimeError("u1 main sha 漂移")

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES, "auth_局次": 0, "gate_局次": 0,
              "smoke_局次": 1, "judgment_局次": 0}

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("U1 统一求解核（全替换形态）：mpx 焦窗（h14-22，+175.7）"
                       "与 expx 模型核（+81）同面不可堆叠（合装判负）→ 正解"
                       "=统一：一个决策核同时做何时卖+卖多少。内层把 MODELPX "
                       "整个决策规则（p_next 4 站点+量帽 4 站点）替换为单一求"
                       "解核；主判 u1 vs mpx 胜者件，参照 u1 vs oc_c3"),
        "kernel": {
            "form": "u1（基底 oc_c3 内层全替换 + 尾块注入统一求解核）",
            "sites": "MODELPX 整个决策规则 8 站点（p_next 计算 4 处同文 + 量帽"
                     "长式 1 处 + take=min(avail,10) 3 处）→ _u1_pnext/_u1_take",
            "projection": "K=12 拍价格轨迹（引擎公式 price(inv) 全表+城镇排水"
                          "表+R28 删失口径对手流估计——expx 件同源）",
            "window_constraint": "mpx 语义内化为约束集：可卖拍=step∈[144,648) ∧ "
                                 "(step%24)∈{14..22}（step 时段语义同 mpx 胜者"
                                 "件字面量 range(_MX_H0,23) h0=14）；窗外抑制",
            "when_to_sell": "现在卖 iff 当前报价 ≥ 窗内剩余可卖拍（K 拍投影内）"
                            "投影峰值价（门字面量 p_next<p_cur-0.5 不动=阈 0.5 "
                            "封印），或窗将关闭（剩余可卖拍集空=末拍清剩余）",
            "how_much": "量=min(帽 3/6/10, MR≤0 截止量)；帽=mpx 钉死三档语义；"
                        "MR 截止=逐件即时报价 price(inv+shift) > 窗内持有值"
                        "（剩余可卖拍投影峰值+吸收曲线边际冲击）即卖、≤即停",
            "win_guard": "沿 expx_v2：①648 后回基线（fire_x=fire_base+基线量"
                         "帽，零足迹）②滞留保险（MR 持有时窗内峰值出货容量清"
                         "不掉投射仓存量→立即基线语义出货）",
            "constraints": ["非触发拍零足迹（影子基线决策并行台账）",
                            "异常回退基线语义", "零跨拍挪量（R23/R26）",
                            "磁带 blob 零触碰", "只挂卖自己投射仓存量（宿主守卫"
                            "沿用）"],
        },
        "design": {
            "surgery": "3 组字面量 8 站点替换（计数台账 4/1/3 + 反替换回程逐字"
                       "节=基座源封印）；尾块注入（knee/expx append 先例）块首"
                       "捕获 _hs_agent、块尾末函数 _u1_agent",
            "build_manifest": {k: man.get(k) for k in
                               ("subs_roundtrip_identity_ok",
                                "gate_literal_untouched", "horizon_k",
                                "win_end", "term", "h0", "entry",
                                "host_entry", "replacements")},
            "u1_main_sha256": u1_sha, "mpx_main_sha256": mpx_sha,
            "base_sha256": base_sha,
        },
        "source": {
            "commands": ["python3 orderbook_unifiedu1_lab/build_unified_u1.py",
                         "python3 orderbook_unifiedu1_lab/judge_unified_u1.py"],
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*123（任务给定新中性块 n=8）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局前 8 fold + 新中性 673000+i*123×8；"
                                 "n=16 双席=32 (seed,seat) 单元/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": {
                "unit": "配对单元=(seed,seat)；h2h=u1 与 mpx 直接同局双席 32 格",
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": WINDOW_LABEL + " fill 口径=影子引擎逐拍归因",
                "realized_px": "Σ(filled×成交价)/Σ(filled×base)（膝点表口径）",
            },
            "criterion": ("h2h vs mpx ≥0.55 ∧ flips_neg==0 ∧ 实现价非负（配对 "
                          "Δratio_fill 三品∧全品均值≥0）∧ 窗差 ≥ mpx（d14-27 "
                          "窗 fill 总窗配对 Δ：u1 vs oc_c3 ≥ mpx vs oc_c3）"),
        },
        "gates": {}, "pairs": {}, "window_stats": {}, "realized_px_paired": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(jm.REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                        2026092904]
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
    t1 = time.perf_counter()
    gates = run_gates()
    EV["gates"]["four_gates"] = gates
    budget["gate_局次"] += 4
    print("gates:", {k: v.get("passed") for k, v in gates.items()
                     if k != "overall"}, round(time.perf_counter() - t1, 1),
          "s", flush=True)
    flush_evid()

    # ---- 3) 冒烟 1 局（非 fold 语料，不入配对） ----
    smoke_units = [{"seed": 2026092999, "seat": 0, "opp_path": opp_paths[0],
                    "opponent": "r37", "stratum": "smoke"}]
    smoke_rows, _e0 = _play(make_specs("smoke", U1_MAIN, smoke_units), run_cfg)
    print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
          "u1:", {k: (smoke_rows[0].get("u1") or {}).get(k)
                  for k in ("fires", "units", "errors", "window_suppressed")},
          flush=True)
    if smoke_rows[0].get("error"):
        ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
    flush_evid()

    # ---- 4) 三臂实跑（oc_c3 / mpx 胜者件 / u1；同语料同对手同席配对） ----
    rows_by_arm: Dict[str, List[Dict[str, Any]]] = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget["judgment_局次"] += len(rows)
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d" % (arm, n_err, len(rows)))
        if arm == "u1":
            te = {"fires": 0, "units": 0, "errors": 0, "censored_lo": 0,
                  "mr_limited": 0, "cap_limited": 0, "stranding_insured": 0,
                  "post_win_base": 0, "window_suppressed": 0,
                  "closing_fires": 0, "decision_diffs": 0}
            for r in rows:
                x = r.get("u1") or {}
                for k in ("fires", "units", "errors", "censored_lo",
                          "mr_limited", "cap_limited", "stranding_insured",
                          "post_win_base", "window_suppressed",
                          "closing_fires"):
                    te[k] += int(x.get(k) or 0)
                te["decision_diffs"] += len(x.get("decision_diff_steps") or [])
            EV["u1_telemetry"] = te
        print(arm, "games", len(rows), "err", n_err,
              "tm", jm.end_agg(rows)["terminal_money_mean"],
              round(time.perf_counter() - t2, 1), "s", flush=True)
        EV["budget"] = budget
        flush_evid()

    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    mpx = {(r["seed"], r["seat"]): r for r in rows_by_arm["mpx_w24_p2_3_h14"]}
    u1 = {(r["seed"], r["seat"]): r for r in rows_by_arm["u1"]}

    # ---- 5) h2h：u1 vs mpx 胜者件直接同局（n=16 双席=32 格） ----
    h2h_rows, _e1 = _play(make_specs_h2h(units), run_cfg)
    budget["judgment_局次"] += len(h2h_rows)
    n = len(h2h_rows)
    W = sum(1 for r in h2h_rows if (r.get("margin") or 0) > 0)
    L = sum(1 for r in h2h_rows if (r.get("margin") or 0) < 0)
    T = n - W - L
    h2h_rate = round((W + 0.5 * T) / max(1, n), 4)
    EV["pairs"]["h2h_u1_vs_mpx"] = {
        "design": "u1 与 mpx_w24_p2_3_h14 直接同局；16 fold×双席=32 格",
        "n": n, "W": W, "L": L, "T": T, "win_rate": h2h_rate,
        "mean_margin": round(sum(r["margin"] for r in h2h_rows
                                 if r.get("margin") is not None)
                             / max(1, n), 2),
        "terminal_money_mean": jm.end_agg(h2h_rows)["terminal_money_mean"],
        "rows_lite": [{"seed": r["seed"], "seat": r["seat"],
                       "margin": round(float(r["margin"]), 1)}
                      for r in h2h_rows[:12] if r.get("margin") is not None]}
    print("h2h u1 vs mpx:", "W%s/L%s/T%s" % (W, L, T), "rate", h2h_rate,
          flush=True)
    flush_evid()

    # ---- 6) 足迹审计门（轨道 2 范式；u1 vs oc_c3） ----
    fp = footprint_audit(ctl, u1, units)
    EV["gates"]["footprint"] = fp
    if not fp["gate_passed"]:
        ANOMALIES.append("足迹审计门未全过：%d/%d 格过"
                         % (fp["n_passed"], fp["n_cells"]))
    print("footprint:", fp["n_passed"], "/", fp["n_cells"], flush=True)
    flush_evid()

    # ---- 7) 配对判决（主判 u1 vs mpx；参照 u1/ mpx vs oc_c3） ----
    ps_main = jm.pair_stats(mpx, u1, units)          # ctl=mpx, var=u1
    ps_u1c3 = jm.pair_stats(ctl, u1, units)
    ps_mpxc3 = jm.pair_stats(ctl, mpx, units)
    wp_u1c3 = jm.window_paired(ctl, u1, units)
    wp_mpxc3 = jm.window_paired(ctl, mpx, units)
    wp_main = jm.window_paired(mpx, u1, units)
    rp_main = realized_paired3(mpx, u1, units)
    rp_u1c3 = realized_paired3(ctl, u1, units)
    EV["pairs"]["u1_vs_mpx"] = ps_main
    EV["pairs"]["u1_vs_oc_c3"] = ps_u1c3
    EV["pairs"]["mpx_vs_oc_c3"] = ps_mpxc3
    EV["window_stats"] = {
        "window": WINDOW_LABEL,
        "paired_u1_vs_oc_c3": {k: wp_u1c3[k] for k in
                               ("fill_total", "fill_milk")},
        "paired_mpx_vs_oc_c3": {k: wp_mpxc3[k] for k in
                                ("fill_total", "fill_milk")},
        "paired_u1_vs_mpx": {k: wp_main[k] for k in
                             ("fill_total", "fill_milk")},
        "agg_by_arm": {a: jm.window_agg(rows_by_arm[a]) for a in RUN_FORMS},
    }
    EV["realized_px_paired"] = {"u1_vs_mpx": rp_main, "u1_vs_oc_c3": rp_u1c3}
    EV["terminal_money"] = {a: jm.end_agg(rows_by_arm[a]) for a in RUN_FORMS}

    win_u1 = wp_u1c3["fill_total"]["mean_delta"]
    win_mpx = wp_mpxc3["fill_total"]["mean_delta"]
    win_ok = (is_num(win_u1) and is_num(win_mpx)
              and float(win_u1) >= float(win_mpx))
    crit = {
        "h2h_vs_mpx>=0.55": h2h_rate >= 0.55,
        "flips_neg==0": ps_main.get("flips_neg") == 0,
        "实现价非负（Δratio_fill 三品∧全品均值≥0）":
            rp_main["nonneg_all_three"],
        "窗差>=mpx（d14-27 fill 总窗配对 Δ u1 vs oc_c3 ≥ mpx vs oc_c3）":
            win_ok,
    }
    EV["criteria"] = {
        "checks": crit,
        "h2h_win_rate": h2h_rate, "h2h_W_L_T": "%s/%s/%s" % (W, L, T),
        "flips_neg": ps_main.get("flips_neg"),
        "net_flip_wins": ps_main.get("net_flip_wins"),
        "mean_delta_u1_minus_mpx": ps_main.get("mean_delta"),
        "realized_px_nonneg_all_three": rp_main["nonneg_all_three"],
        "window_fill_total_delta_u1_vs_oc_c3": win_u1,
        "window_fill_total_delta_mpx_vs_oc_c3": win_mpx,
        "four_gates_passed": gates.get("overall"),
        "footprint_gate_passed": fp["gate_passed"],
        "positive_arm": all(crit.values())}
    print("u1 vs mpx:", "W%s/L%s/T%s" % (ps_main["W"], ps_main["L"],
                                         ps_main["T"]),
          "dM", ps_main["mean_delta"], "flips_neg", ps_main["flips_neg"],
          "win_u1", win_u1, "win_mpx", win_mpx, "crit", crit, flush=True)

    # ---- 8) verdict ----
    budget["total_局次"] = (budget["auth_局次"] + budget["gate_局次"]
                           + budget["smoke_局次"] + budget["judgment_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES
    ok_all = all(crit.values())
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "criteria_passed": ok_all,
        "four_gates_passed": gates.get("overall"),
        "footprint_gate_passed": fp["gate_passed"],
        "h2h_win_rate_vs_mpx": h2h_rate,
        "window_fill_total_delta": {"u1_vs_oc_c3": win_u1,
                                    "mpx_vs_oc_c3": win_mpx},
        "verdict": ("U1_UNIFIED_POSITIVE: 统一求解核四判据全过（四门%s、足迹"
                    "审计门%s）" % ("过" if gates.get("overall") else "未过",
                                   "过" if fp["gate_passed"] else "未过")
                    if ok_all else "NOT_CONFIRMED（详见 criteria）"),
        "form": "u1",
        "note": "判据预登记于任务书（unified-u1）；不发射不提交；上线决策移交"
                "用户",
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行；"
                     "kaggle_environments 可选环境加载告警")
    ANOMALIES.append("口径备忘：门字面量 p_next<p_cur-0.5 不动（阈 0.5 封印）"
                     "→触发等价 当前报价≥投影峰值+0.5；末拍清剩余=MR 截止放行"
                     "至帽位/存量（帽 3/6/10=封印旋钮）；投影不含自家未来销售、"
                     "不含未来商店解锁；hour-1 多站点同拍重复评估由 (step,item) "
                     "台账去重")
    LEDGER_PATH.write_text(json.dumps(
        {"h2h": {"W": W, "L": L, "T": T, "win_rate": h2h_rate},
         "pairs": {k: {kk: EV["pairs"][k][kk] for kk in
                       ("n", "W", "L", "T", "mean_delta", "net_flip_wins",
                        "flips_neg")}
                   for k in ("u1_vs_mpx", "u1_vs_oc_c3", "mpx_vs_oc_c3")},
         "window": {"u1_vs_oc_c3": win_u1, "mpx_vs_oc_c3": win_mpx},
         "criteria": EV["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
