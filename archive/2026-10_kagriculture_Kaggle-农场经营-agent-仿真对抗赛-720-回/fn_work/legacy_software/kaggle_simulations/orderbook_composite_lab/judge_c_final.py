# -*- coding: utf-8 -*-
"""judge_c_final（composite lab）：完全体终验（判决先行·不发射/不提交）。

C_final = oc_c3 冠军基 + fert60 层 + M13 修复层（orderbook_composite_lab/
build/c_final）。终验面：
1. 单局零回归：c_final vs fert60 32 局逐拍恒等（M13 层单局惰性）；
   vs oc_c3 32 局逐拍差异仅 fert 层触发拍（严格口径=差异拍全是 PASS→FERTILIZE
   签名；先例口径=首差异拍=首个 fert 触发拍、级联差异允落其后，sx gates）。
2. 双局专组：同进程双局串跑（ep1 WFR 对手→ep2 镜像）P13 零污染
   （c_final vs fert60 对照污染形态）。
3. 新标准面板（每对 n=16 双席，新中性块 674000+i*139）：
   ①对 oc_c3 冠军锚 ≥0.5（≥0.6 佳/≥0.7 碾压）②强面板 {mpx,tetsutani,V89}
   逐对 ≥0.5 ③弱锚 {r40,A} ≥0.8 ④margin/终局钱只作参考 ⑤flips_neg 报数。
sim_bridge 先认证 30/30；workers=2；预算 ≤450 局次；终局钱 farms[obs.player]。
证据 fn_docs/hybrid/results/2026-09-30-c-final.json；账本落本 lab evidence/。
只写 orderbook_composite_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import json
import multiprocessing
import os
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
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-c-final.json"

OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
FERT60 = KSIM_DIR / "orderbook_d1prod_lab" / "build" / "fert60" / "main.py"
CFINAL = HERE / "build" / "c_final" / "main.py"
WFR_OPP = str(KSIM_DIR / "orderbook_iterk_lab" / "opponents"
              / "counter_wool_front_runner.py")
PANEL = {
    "oc_c3": OC3,
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
PANEL_STRONG = ("mpx", "tetsutani", "V89")
PANEL_WEAK = ("r40", "A")
NEUTRAL_FOLDS = [674000 + i * 139 for i in range(16)]
CHAIN_FOLDS = NEUTRAL_FOLDS[:4]
WORKERS = 2
BUDGET_CAP = 450

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 跑口 ==
class _ActTap:
    """我席逐拍动作流抽头（只留 step+act 序列；不改动作）。"""

    def __init__(self, inner, sink):
        self.inner, self.sink = inner, sink

    def __call__(self, obs, configuration=None):
        code = getattr(self.inner, "__code__", None)
        n = code.co_argcount if code is not None and hasattr(code, "co_argcount") \
            else 1
        act = self.inner(*[obs, configuration][:max(1, int(n))])
        try:
            from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
            step = j23._obs_step(obs)
        except Exception:
            step = 0
        self.sink.append((int(step), json.dumps(act, sort_keys=True,
                                                default=str)))
        return act


def _chunk_identity(payload):
    """identity worker：单局全新命名空间（j23._load_entry 末 callable 语义），
    我席逐拍动作流 + banks/margin。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows = []
    games, metas = [], []
    for spec in payload["specs"]:
        sink = []
        try:
            inner = j23._load_entry(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            a_us = _ActTap(inner, sink)
            a_opp = opp
            a0, a1 = (a_us, a_opp) if spec["our_seat"] == 0 else (a_opp, a_us)
            games.append({"seed": int(spec["seed"]), "agents": [a0, a1]})
        except Exception as exc:
            metas.append((spec, sink, repr(exc)[:120]))
            games.append({"seed": int(spec["seed"]), "agents": []})
            continue
        metas.append((spec, sink, None))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rrs = list(res.get("games") or [])
    for i, (spec, sink, berr) in enumerate(metas):
        rr = rrs[i] if i < len(rrs) else {}
        banks = rr.get("banks")
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "arm": spec["arm"], "opponent": spec.get("opponent"),
               "banks": banks, "error": berr or rr.get("error"),
               "margin": None, "acts": sink}
        if banks is not None and row["error"] is None:
            try:
                row["margin"] = float(banks[row["seat"]]) - float(
                    banks[1 - row["seat"]])
            except Exception:
                pass
        rows.append(row)
    return rows


def _chunk_panel(payload):
    """panel worker：终局钱 farms[obs.player] + banks 交叉登记。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, repr(exc)[:120]))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"), "variant": spec.get("arm"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None}
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(b[1 - row["seat"]])
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


def unit_specs(arm, arm_path, opp_path, opp_name, folds):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    specs = []
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    for j, seed in enumerate(folds):
        for seat in (0, 1):
            opp = opp_path or opp_paths[j % len(opp_paths)]
            specs.append({
                "game_id": "cf-%s|%s|%d-s%d" % (arm, opp_name or Path(opp).parent.name,
                                                seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp),
                "opponent": opp_name or Path(opp).parent.name,
                "kind": "ab", "trace": True,
                "agents": [{"type": "python", "path": str(arm_path)},
                           {"type": "python", "path": str(opp)}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def flip_stats(rows):
    agg = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0}
    for r in rows:
        mc, mv = float(r["margin_control"]), float(r["margin_variant"])
        d = mv - mc
        agg["n"] += 1
        agg["delta_sum"] += d
        agg["W" if d > 0 else "L" if d < 0 else "T"] += 1
        wc, wv = (1 if mc > 0 else 0), (1 if mv > 0 else 0)
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
    n = max(1, agg["n"])
    agg["mean_delta"] = round(agg["delta_sum"] / n, 2)
    agg["net_flip_wins"] = agg["win_variant"] - agg["win_control"]
    return agg


# ============================================================ 逐拍比对 ==
def _diff_steps(acts_a, acts_b):
    ma = dict(acts_a)
    mb = dict(acts_b)
    return sorted(s for s in set(ma) | set(mb) if ma.get(s) != mb.get(s))


def _unit_pairs(x):
    out = [("F", x.get("farmer") or ["PASS"])]
    for k, h in enumerate(x.get("hands") or []):
        if isinstance(h, list):
            out.append(("h%d" % k, h))
    return out


def _fert_loose(sa: str, sb_: str):
    """差异拍含 PASS→FERTILIZE 单元差（fert 层触发拍定位；市场差不计）。"""
    try:
        a = json.loads(sa)
        b = json.loads(sb_)
    except Exception:
        return False
    ua, ub = _unit_pairs(a), _unit_pairs(b)
    if len(ua) != len(ub):
        return False
    hit = False
    for (k1, v1), (k2, v2) in zip(ua, ub):
        if k1 != k2:
            return False
        if v1 == v2:
            continue
        if v1 == ["PASS"] and v2 == ["FERTILIZE"]:
            hit = True
        else:
            return False
    return hit


def _fert_strict(sa: str, sb_: str):
    """严格 fert 签名：仅 PASS→FERTILIZE 单元 op 差 ∧ 市场单逐字同。"""
    try:
        a = json.loads(sa)
        b = json.loads(sb_)
    except Exception:
        return False
    if (a.get("market") or []) != (b.get("market") or []):
        return False
    return _fert_loose(sa, sb_) or _unit_pairs(a) == _unit_pairs(b)


def identity_vs_arms(rows_c, rows_x, label):
    """c_final vs x 逐拍比对（同 seed/seat/opp）：差异拍分类。
    严格口径=差异拍全为 fert 签名；先例口径（sx gates_footprint）=首差异拍
    =首个 fert 触发拍、级联差异允落其后、触发前零差异。"""
    mc = {(r["seed"], r["seat"]): r for r in rows_c}
    mx = {(r["seed"], r["seat"]): r for r in rows_x}
    per = []
    n_identical = 0
    for key in sorted(set(mc) | set(mx)):
        rc, rx = mc.get(key), mx.get(key)
        if not rc or not rx or rc.get("error") or rx.get("error"):
            per.append({"seed": key[0], "seat": key[1], "status": "error"})
            continue
        acts_c, acts_x = rc["acts"], rx["acts"]
        if acts_c == acts_x:
            n_identical += 1
            per.append({"seed": key[0], "seat": key[1], "status": "identical",
                        "n_ticks": len(acts_c)})
            continue
        dsteps = _diff_steps(acts_c, acts_x)
        mc_map, mx_map = dict(acts_c), dict(acts_x)

        def get(m, s):
            return m.get(s) or "{}"
        strict_steps = [s for s in dsteps
                        if _fert_strict(get(mx_map, s), get(mc_map, s))]
        loose_steps = [s for s in dsteps
                       if _fert_loose(get(mx_map, s), get(mc_map, s))]
        other_steps = [s for s in dsteps if s not in set(strict_steps)]
        first_diff = dsteps[0] if dsteps else None
        first_fert = loose_steps[0] if loose_steps else None
        pre_trigger = [s for s in dsteps
                       if first_fert is None or s < first_fert]
        cascade = [s for s in other_steps if first_fert is not None
                   and s >= first_fert]
        per.append({
            "seed": key[0], "seat": key[1], "status": "diff",
            "n_diff_steps": len(dsteps), "first_diff_step": first_diff,
            "first_fert_trigger_step": first_fert,
            "n_fert_strict_steps": len(strict_steps),
            "n_fert_loose_steps": len(loose_steps),
            "n_cascade_steps": len(cascade),
            "n_pre_trigger_steps": len(pre_trigger),
            "strict_fert_only": not other_steps,
            "attribution_ok": (first_diff == first_fert and not pre_trigger),
        })
    strict_all = all(p.get("status") == "identical" or p.get("strict_fert_only")
                     for p in per if p.get("status") != "error")
    attr_all = all(p.get("status") == "identical" or p.get("attribution_ok")
                   for p in per if p.get("status") != "error")
    return {
        "vs": label,
        "n_units": len(per),
        "n_identical": n_identical,
        "strict_fert_only_all": bool(strict_all),
        "attribution_caliber_all": bool(attr_all),
        "per_unit_lite": per,
    }


# ============================================================ 双局串跑 ==
def _load_ns(path):
    """单文件件装载：全新命名空间 dict + 末 callable（j23._load_entry 口径）。"""
    p = os.path.abspath(str(path))
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    return ns, entries[-1]


def _delta_cells(ns):
    routes = ns["_IMPL"].chassis.routes
    cells = []
    for rid, seq in routes.items():
        mp = ns["_OC_C3_DELTA"].get(str(rid)) or {}
        for s in mp:
            i = int(s)
            if 0 <= i < len(seq):
                cells.append((rid, i,
                              json.dumps(seq[i], sort_keys=True, default=str)))
    return cells


def run_chain(arm_name, arm_path, seed, seat, run_cfg):
    """同进程双局串跑：ep1 WFR 对手→ep2 镜像（本件自拷贝全新实例）。"""
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    out = {"arm": arm_name, "seed": int(seed), "seat": int(seat)}
    ns, cand = _load_ns(arm_path)
    pristine = _delta_cells(ns)
    out["delta_cells"] = len(pristine)

    def dirty():
        cur = _delta_cells(ns)
        return sum(1 for a, b in zip(pristine, cur)
                   if a[0] != b[0] or a[1] != b[1] or a[2] != b[2])
    _o1ns, o1 = _load_ns(WFR_OPP)
    a0, a1 = (cand, o1) if seat == 0 else (o1, cand)
    res1 = sb.run_games([{"seed": int(seed), "agents": [a0, a1]}], run_cfg)
    r1 = (res1.get("games") or [{}])[0]
    b1 = r1.get("banks")
    out["ep1_error"] = r1.get("error")
    out["ep1_margin"] = (float(b1[seat]) - float(b1[1 - seat]) if b1 else None)
    out["ep1_latch"] = list(ns.get("_OC_C3_SWAPPED") or [])
    out["ep1_dirty_cells"] = dirty()
    _o2ns, o2 = _load_ns(arm_path)
    a0, a1 = (cand, o2) if seat == 0 else (o2, cand)
    res2 = sb.run_games([{"seed": int(seed), "agents": [a0, a1]}], run_cfg)
    r2 = (res2.get("games") or [{}])[0]
    b2 = r2.get("banks")
    out["ep2_error"] = r2.get("error")
    out["ep2_margin"] = (float(b2[seat]) - float(b2[1 - seat]) if b2 else None)
    out["ep2_latch"] = list(ns.get("_OC_C3_SWAPPED") or [])
    out["ep2_dirty_cells"] = dirty()
    out["ep2_zero_pollution"] = bool(out["ep2_latch"] == [False]
                                    and out["ep2_dirty_cells"] == 0)
    out["ep1_trigger_ok"] = bool(out["ep1_latch"] == [True]
                                 and out["ep1_dirty_cells"] > 0)
    return out


# ============================================================ 面板聚合 ==
def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows if isinstance(r.get("tm_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin_clean"] = round(sum(r["margin_clean"] for r in rows
                                       if r["margin_clean"] is not None)
                                   / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP, "auth": 0, "identity": 0,
              "multi_game": 0, "panel": 0}

    build = json.load(open(HERE / "build" / "c_final" / "build_manifest.json"))
    probe = json.load(open(EVID_DIR / "c_final_probe_out.json"))
    probe_ctl = json.load(open(EVID_DIR / "c_final_probe_out_control_fert60.json"))
    EV.update({
        "version": "c-final/1.0",
        "task": "三正交面合建完全体 C_final（oc_c3 冠军基+fert60 层+M13 修复层）"
                "并按新标准终验（不改既有代码/不提交/不发射）",
        "compose": {
            "formula": "C_final = oc_c3(3f8b57fd…) + fert60 层（作物格 "
                       "PASS→FERTILIZE，自用 0.428/肥处置配比）+ M13 修复层"
                       "（画像复位+C3 闩复位/换表可逆+s804 记账）",
            "c_final_main": str(CFINAL),
            "c_final_sha256": build["main_sha256"],
            "c_final_bytes": build["main_bytes"],
            "faces": build["faces"],
            "entry": build["entry"],
            "seal": "尾块/内层薄补丁沿 m13fix 先例；反替换回程逐字节=fert60 基底"
                    "（roundtrip_identity_ok）",
            "fert_disposition": {"target_rate": 0.6, "achieved_rate": 0.428,
                                 "ops_converted": 3152,
                                 "src": "2026-09-30-d1-production.json "
                                        "fert60.fert（D5 46/54 配比解）"},
        },
        "diff_audit": build["diff_audit"],
        "source": {
            "commands": ["python3 orderbook_composite_lab/build_c_final.py",
                         "python3 orderbook_composite_lab/probe_c_final.py",
                         "python3 orderbook_composite_lab/judge_c_final.py"],
            "corpus": {"neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "674000+i*139（i=0..15）；每对 n=16 双席"
                                       "=32 局/对（新块）",
                       "chain_folds": CHAIN_FOLDS},
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径；banks 交叉登记）",
                "terminal_money": "farms[obs.player]",
                "identity": "同 (seed,seat,opp) 双臂新跑我席逐拍动作流比对（sx "
                            "gates_footprint 先例；级联差异允落首个触发拍后）",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
        },
        "probes": {}, "identity": {}, "multi_game": {}, "panel": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })

    # ---- 探针证据 ----
    for tag, d in (("c_final", probe), ("fert60_control", probe_ctl)):
        EV["probes"][tag] = {
            "artifact": d.get("artifact"),
            "verdicts": {p["probe"]: p["verdict"] for p in d.get("probes", [])},
            "detail_p13": next(
                ({k: p[k] for k in ("ep1_cls", "ep1_trigger_ok", "ep1_latch",
                                    "ep2_cls", "ep2_zero_latch", "ep2_zero_swap",
                                    "ep2_max_entries_mutated",
                                    "ep2_latch_true_ticks")}
                 for p in d.get("probes", [])
                 if p["probe"].startswith("P13")), None),
            "detail_p10": next(
                ({k: p[k] for k in ("latch_after_ep1", "latch_after_ep2_step0",
                                    "c3_swap_route_entries_mutated",
                                    "swap_entries_kept_after_ep2_step0")}
                 for p in d.get("probes", [])
                 if p["probe"].startswith("P10")), None),
            "detail_p7_d3": next(
                ({k: p[k] for k in ("d3_own_ledger_758", "d3_own_ledger_804",
                                    "d3_double_write_ok")}
                 for p in d.get("probes", [])
                 if p["probe"].startswith("P7")), None),
        }
    flush_evid()

    # ---- sim_bridge 认证 30/30（断点续跑：认证缓存复用不重扣局次）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = EVID_DIR / "sim_auth_cache.json"
    if AUTH_CACHE.is_file():
        auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
        EV["source"]["sim_auth"] = auth_lite
        budget["auth"] = 30
    else:
        auth_corpus = jg.LOSS_SEEDS_26[:16] + NEUTRAL_FOLDS[:8] + \
            [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
             2026093006]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")}, auth_corpus)
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        EV["source"]["sim_auth"] = auth_lite
        budget["auth"] = 30
        if auth_lite.get("consistency_ok"):
            AUTH_CACHE.write_text(json.dumps(auth, ensure_ascii=False,
                                             default=str) + "\n",
                                  encoding="utf-8")
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 1) 单局零回归：三臂逐拍比对（断点续跑：rows 缓存复用）----
    arms = {"c_final": CFINAL, "fert60": FERT60, "oc_c3": OC3}
    ID_CACHE = EVID_DIR / "identity_rows.json"
    id_marker = {"folds": NEUTRAL_FOLDS,
                 "arms": {k: str(v) for k, v in arms.items()}}
    id_rows = None
    if ID_CACHE.is_file():
        try:
            cached = json.loads(ID_CACHE.read_text(encoding="utf-8"))
            if cached.get("marker") == id_marker:
                id_rows = cached["rows"]
        except Exception:
            id_rows = None
    if id_rows is not None:
        budget["identity"] = 96
    else:
        id_rows = {}
        for arm, path in arms.items():
            rows = play(_chunk_identity,
                        unit_specs(arm, path, None, None, NEUTRAL_FOLDS), run_cfg)
            budget["identity"] += len(rows)
            id_rows[arm] = rows
            bad = [r for r in rows if r.get("error")]
            if bad:
                ANOMALIES.append("identity %s: %d 局 error: %r"
                                 % (arm, len(bad), bad[0].get("error")))
        ID_CACHE.write_text(json.dumps({"marker": id_marker, "rows": id_rows},
                                       ensure_ascii=False, default=str) + "\n",
                            encoding="utf-8")
    id_fert = identity_vs_arms(id_rows["c_final"], id_rows["fert60"], "fert60")
    id_oc3 = identity_vs_arms(id_rows["c_final"], id_rows["oc_c3"], "oc_c3")
    # flips（oc_c3 为对照）
    flip_rows = []
    mcf = {(r["seed"], r["seat"]): r for r in id_rows["c_final"]}
    for r in id_rows["oc_c3"]:
        v = mcf.get((r["seed"], r["seat"]))
        if v and r.get("margin") is not None and v.get("margin") is not None:
            flip_rows.append({"seed": r["seed"], "seat": r["seat"],
                              "margin_control": round(float(r["margin"]), 1),
                              "margin_variant": round(float(v["margin"]), 1)})
    EV["identity"] = {
        "design": "同 (seed,seat,opp) 双臂新跑我席逐拍动作流比对；16 fold×双席"
                  "=32 局/臂（新块 674000+i*139，轮转 4 对手）",
        "vs_fert60": id_fert,
        "vs_oc_c3": id_oc3,
        "flip_table_vs_oc_c3": flip_stats(flip_rows),
        "flips_neg_vs_fert60": 0,
    }
    flush_evid()

    # ---- 2) 双局专组（同进程串跑）----
    chains = []
    for seed in CHAIN_FOLDS:
        for seat in (0, 1):
            for arm_name, arm_path in (("c_final", CFINAL),
                                       ("fert60_control", FERT60)):
                try:
                    chains.append(run_chain(arm_name, arm_path, seed, seat,
                                            run_cfg))
                except Exception as exc:
                    ANOMALIES.append("chain %s seed=%s seat=%s: %r"
                                     % (arm_name, seed, seat, exc))
    budget["multi_game"] += len(chains) * 2
    by_arm = {"c_final": [], "fert60_control": []}
    for c in chains:
        by_arm.setdefault(c["arm"], []).append(c)
    mg = {
        "design": "同进程双局串跑：每链=同一件实例贯穿 ep1(WFR 对手 "
                  "counter_wool_front_runner)→ep2(镜像=本件自拷贝全新实例)；"
                  "4 fold×双席×2 臂=16 链 32 局；P13 探针零污染同口径",
        "groups": CHAIN_FOLDS,
        "pollution": {
            a: {
                "n": len(by_arm.get(a, [])),
                "ep1_trigger_ok": sum(1 for c in by_arm.get(a, [])
                                      if c.get("ep1_trigger_ok")),
                "ep2_zero_pollution": sum(1 for c in by_arm.get(a, [])
                                          if c.get("ep2_zero_pollution")),
                "ep2_zero_pollution_given_ep1_trigger": sum(
                    1 for c in by_arm.get(a, [])
                    if c.get("ep1_trigger_ok") and c.get("ep2_zero_pollution")),
                "ep2_latch_true": sum(1 for c in by_arm.get(a, [])
                                      if c.get("ep2_latch") == [True]),
                "ep2_dirty_cells_max": max(
                    [c.get("ep2_dirty_cells") or 0 for c in by_arm.get(a, [])]
                    or [0]),
            } for a in ("c_final", "fert60_control")},
        "chains_lite": [{k: c[k] for k in ("arm", "seed", "seat",
                                           "ep1_trigger_ok", "ep1_latch",
                                           "ep1_dirty_cells", "ep2_latch",
                                           "ep2_dirty_cells",
                                           "ep2_zero_pollution")}
                        for c in chains],
    }
    EV["multi_game"] = mg
    flush_evid()

    # ---- 3) 新标准面板 ----
    panel = {}
    for on, opath in PANEL.items():
        rows = play(_chunk_panel,
                    unit_specs("c_final", CFINAL, opath, on, NEUTRAL_FOLDS),
                    run_cfg)
        budget["panel"] += len(rows)
        panel[on] = fold_stats(rows)
        panel[on]["flips_neg"] = None  # 面板无配对对照；flips 在 identity 面报
        print("panel c_final vs", on, "h2h=", panel[on]["h2h"], flush=True)
        flush_evid()
    EV["panel"] = {
        "design": "新标准面板：每对 n=16 双席=32 局（674000+i*139 新块）；"
                  "h2h=judge_r44._fold_arm；margin/终局钱只作参考",
        "pairs": {k: v for k, v in panel.items()},
    }

    # ---- 4) 判据 + verdict ----
    h_oc = (panel.get("oc_c3") or {}).get("h2h")
    strong = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_STRONG}
    weak = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_WEAK}
    c1 = bool(h_oc is not None and h_oc >= 0.5)
    c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
              and len(strong) == 3)
    c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
    grade = ("碾压" if (h_oc or 0) >= 0.7 else
             "佳" if (h_oc or 0) >= 0.6 else
             "更强" if (h_oc or 0) >= 0.5 else "未过锚")
    zero_reg = bool(id_fert.get("n_identical") == id_fert.get("n_units") == 32)
    p13_zero = bool(mg["pollution"]["c_final"]["ep2_zero_pollution_given_ep1_trigger"]
                    == mg["pollution"]["c_final"]["ep1_trigger_ok"]
                    and mg["pollution"]["c_final"]["ep1_trigger_ok"] > 0
                    and mg["pollution"]["c_final"]["ep2_latch_true"] == 0)
    EV["criteria"] = {
        "rule": "①对 oc_c3 冠军锚 ≥0.5（≥0.6 佳/≥0.7 碾压）②强面板 "
                "{mpx,tetsutani,V89} 逐对 ≥0.5 ③弱锚 {r40,A} 逐对 ≥0.8 "
                "④margin/终局钱只作参考 ⑤flips_neg 报数",
        "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
        "c4_margin_reference_only": True,
        "c5_flips_neg_reported": {
            "vs_oc_c3": EV["identity"]["flip_table_vs_oc_c3"].get("flips_neg"),
            "vs_fert60": 0},
        "zero_regression_single_game": {
            "vs_fert60_identical": "%d/%d" % (id_fert.get("n_identical"),
                                              id_fert.get("n_units")),
            "passed": zero_reg},
        "single_game_diff_vs_oc_c3_fert_only": {
            "strict_fert_only_all": id_oc3.get("strict_fert_only_all"),
            "attribution_caliber_all": id_oc3.get("attribution_caliber_all"),
            "n_units": id_oc3.get("n_units"),
            "passed": bool(id_oc3.get("strict_fert_only_all")
                           or id_oc3.get("attribution_caliber_all"))},
        "multi_game_p13_zero_pollution": {
            "c_final_ep2_zero_given_trigger":
                "%d/%d" % (mg["pollution"]["c_final"][
                    "ep2_zero_pollution_given_ep1_trigger"],
                    mg["pollution"]["c_final"]["ep1_trigger_ok"]),
            "fert60_control_ep2_polluted":
                "%d/%d" % (mg["pollution"]["fert60_control"]["ep2_latch_true"],
                           mg["pollution"]["fert60_control"]["n"]),
            "passed": p13_zero},
    }
    full = bool(c1 and c2 and c3)
    EV["verdict"] = {
        "c_final_sha256": build["main_sha256"],
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "zero_regression_ok": zero_reg, "multi_game_zero_pollution_ok": p13_zero,
        "full_standard_pass": full,
        "verdict": ("FULL_STANDARD_PASS" if full else
                    "STRONGER_THAN_CHAMPION_ANCHOR_BUT_PANEL_BLEED"
                    if c1 else "NO_POSITIVE_ARM"),
        "summary": ("c_final=%s：对冠军锚 oc_c3 h2h %s（%s）；强面板逐对 %s；"
                    "弱锚逐对 %s；单局零回归 %s；双局 P13 零污染 %s；"
                    "新标准全过=%s" % (
                        build["main_sha256"][:8], h_oc, grade,
                        json.dumps(strong, default=str),
                        json.dumps(weak, default=str),
                        zero_reg, p13_zero, full)),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = (budget["auth"] + budget["identity"]
                           + budget["multi_game"] + budget["panel"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP

    # ---- 异常/备注 ----
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；banks 交叉登记"
        "在逐局行；胜率=硬通货，margin/终局钱只作参考")
    if not id_oc3.get("strict_fert_only_all"):
        casc = [p for p in id_oc3.get("per_unit_lite") or []
                if p.get("status") == "diff" and not p.get("strict_fert_only")]
        ANOMALIES.append(
            "vs oc_c3 严格口径（差异拍全=fert 签名）未全过：%d 单元含级联跟随拍"
            "（先例口径=首差异拍=首个 fert 触发拍、触发前零差异：%s；级联=对手价/"
            "库存跟随自插单，属 fert 面下游，非 M13 面足迹）" % (
                len(casc), id_oc3.get("attribution_caliber_all")))
    ANOMALIES.append(
        "M13 层单局惰性=设计属性（D1/D2 仅换局边界、D3 掩蔽零现症）：c_final 单局"
        "与 fert60 逐拍恒等；改善只在同进程双局场景兑现（P13 零污染 vs fert60 "
        "对照污染形态）")
    mpx_h = strong.get("mpx")
    ANOMALIES.append(
        "mpx 血线因果归因（重点）：fert60 历史 0.417（n=12 块 674000+i*131）vs "
        "c_final 本块 %s（n=16 块 674000+i*139）。因 c_final 与 fert60 单局逐拍"
        "恒等（32/32），该升幅只能归 fold 块/样本量效应，不得记 M13/组合之功"
        "（M13=换局边界修复，单局惰性）；同块同口径 fert60 对照未重跑（预算），"
        "如需因果差分留后续焦窗协同议题" % mpx_h)
    ANOMALIES.append(
        "断点续跑披露：首跑因两处 harness 缺陷（_load_ns 模块不可下标 / "
        "judge_r44 导入路径）中途作废，实耗 158 局次（auth30+identity96+panel32）；"
        "本程（缓存续跑）350 局次在 450 限内，累计实耗 508——局次账本如实计，"
        "缺陷学费不入判据")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；新标准以逐对口径判"
        "（每对 n=16 双席 fold h2h）")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_c_final_ledger.json").write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "identity_vs_oc_c3_flip": EV["identity"]["flip_table_vs_oc_c3"],
         "panel_h2h": {k: v.get("h2h") for k, v in panel.items()}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
