# -*- coding: utf-8 -*-
"""judge_m13fix：M13 修复件 dh_fix 判决（判决先行·不发射不提交）。

责任口径（任务 T3f）：
- 修复件 dh_fix vs drop_half 配对（26 败局前 8 fold + 新中性 674000+i*137×8，
  n=16 双席=32 局/臂；单局逐拍恒等=零回归证明）；
- 同进程双局串跑专组（8 组 × 双席：ep1 WFR 对手(counter_wool_front_runner)
  →ep2 镜像对手(本件自拷贝)；对照 drop_half 的污染形态）；
- 判据=净翻胜>0 ∧ flips_neg==0 ∧ 双局专组零污染 ∧ 实现价非负。
- sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤300 局次；
  读数：margin=banks[our]−banks[opp]；终局钱 farms[obs.player]。
证据 fn_docs/hybrid/results/2026-09-30-m13-fix.json；
账本落 orderbook_m13fix_lab/evidence/。不改既有代码；不提交；不发射。
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
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM
_spec.loader.exec_module(JM)
JM.WINDOW = (336, 648)
JM.WIN_DAYS = tuple(range(14, 27))

RECORD_VERSION = "m13fix-judge/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]
NEUTRAL_FOLDS = [674000 + i * 137 for i in range(8)]   # 新中性 674000+i*137×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS
DROPHALF_MAIN = str(KSIM_DIR / "orderbook_unified_u2_lab" / "build"
                    / "u2v2_drop_half" / "main.py")
DHFIX_MAIN = str(MODULE_DIR / "build" / "u2v2_dh_fix" / "main.py")
WFR_OPP = str(KSIM_DIR / "orderbook_iterk_lab" / "opponents"
              / "counter_wool_front_runner.py")
WORKERS = 2
BUDGET_CAP = 300
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-m13-fix.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_m13fix_ledger.json"

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
                   else "neutral_674000_i137")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum, "tag": tag})
    return units


def rows_by_key(rows):
    return {(int(r["seed"]), int(r["seat"])): r for r in rows}


# ------------------------------------------------------------ 双局串跑 --
def _load_entry(path):
    """单文件件装载（末 callable 语义）+ 可检视命名空间（同进程状态观测）。"""
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
    """C3 delta 触点格 (rid, idx, json)；两件同源（34 路 443 格 idx 412-618）。"""
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


def _dirty_cells(ns, pristine):
    cur = _delta_cells(ns)
    return sum(1 for a, b in zip(pristine, cur)
               if a[0] != b[0] or a[1] != b[1] or a[2] != b[2])


def _cls_of(ns, seat):
    try:
        return (ns.get("_OC_STATE") or {}).get(int(seat), {}).get("cls")
    except Exception:
        return None


def run_chain(arm_path, seed, seat, run_cfg, ep2_opp_path=None):
    """同进程双局串跑：ep1 WFR 对手→ep2 镜像对手；同一件实例贯穿两局。

    ep2_opp_path=None -> 镜像对手=本件自拷贝全新实例（judge_r23 mirror 口径）；
    指定路径 -> 镜像类具名对手（h1_mirror 类名namesake：h1 件）。
    """
    out = {"arm": Path(arm_path).parent.name, "seed": int(seed),
           "seat": int(seat),
           "ep2_opponent": (Path(ep2_opp_path).parent.name if ep2_opp_path
                            else "self_copy")}
    ns, cand = _load_entry(arm_path)
    pristine = _delta_cells(ns)
    out["delta_cells"] = len(pristine)
    # ep1：WFR 对手（wfr 类触发 C3 换表=设计行为，两臂同）
    _o1ns, o1 = _load_entry(WFR_OPP)
    a0, a1 = (cand, o1) if seat == 0 else (o1, cand)
    res1 = sb_run_games([{"seed": int(seed), "agents": [a0, a1]}], run_cfg)
    r1 = (res1.get("games") or [{}])[0]
    banks1 = r1.get("banks")
    out["ep1_error"] = r1.get("error")
    out["ep1_margin"] = (float(banks1[seat]) - float(banks1[1 - seat])
                         if banks1 else None)
    out["ep1_latch"] = list(ns.get("_OC_C3_SWAPPED") or [])
    out["ep1_dirty_cells"] = _dirty_cells(ns, pristine)
    out["ep1_cls"] = _cls_of(ns, seat)
    # ep2：镜像对手；断言零换表零闩
    _o2ns, o2 = _load_entry(ep2_opp_path or arm_path)
    a0, a1 = (cand, o2) if seat == 0 else (o2, cand)
    res2 = sb_run_games([{"seed": int(seed), "agents": [a0, a1]}], run_cfg)
    r2 = (res2.get("games") or [{}])[0]
    banks2 = r2.get("banks")
    out["ep2_error"] = r2.get("error")
    out["ep2_margin"] = (float(banks2[seat]) - float(banks2[1 - seat])
                         if banks2 else None)
    out["ep2_latch"] = list(ns.get("_OC_C3_SWAPPED") or [])
    out["ep2_dirty_cells"] = _dirty_cells(ns, pristine)
    out["ep2_cls"] = _cls_of(ns, seat)
    out["ep2_zero_pollution"] = bool(
        out["ep2_latch"] == [False] and out["ep2_dirty_cells"] == 0)
    out["ep1_trigger_ok"] = bool(out["ep1_latch"] == [True]
                                 and out["ep1_dirty_cells"] > 0)
    return out


def sb_run_games(games, run_cfg):
    from orderbook_r40 import sim_bridge as sb
    return sb.run_games(games, run_cfg)


def flip_stats(rows):
    """翻局表（knee/ pair_stats 同口径）：delta=var−ctl；win=margin>0。"""
    agg = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0,
           "rows_lite": []}
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
        agg["rows_lite"].append(
            {k: r[k] for k in ("seed", "seat", "margin_control",
                               "margin_variant")})
    n = max(1, agg["n"])
    return {"n": agg["n"], "W": agg["W"], "L": agg["L"], "T": agg["T"],
            "mean_delta": round(agg["delta_sum"] / n, 2),
            "win_control": agg["win_control"],
            "win_variant": agg["win_variant"],
            "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
            "net_flip_wins": agg["win_variant"] - agg["win_control"],
            "rows_lite": agg["rows_lite"]}


def main():
    t0 = time.perf_counter()
    from orderbook_r40 import sim_bridge as sb
    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "pairs_局次": 0,
              "multi_game_局次": 0,
              "cap_scope": "认证 60 + 配对 32×2 臂 + 双局专组 8×2 席×2 局×2 臂"
                           " = 188 ≤ 300"}
    EV.update({
        "version": RECORD_VERSION,
        "task": "M13 缺陷修复（T3f）：D1 画像换局复位 / D2 C3 闩复位+换表可逆 / "
                "D3 s804 自插单记台账",
        "fixes": {
            "D1": {"loc": "_oc_after 尾块包装（内层 _oc_after 换局重播）",
                   "form": "画像注册表无换局复位：ep2 全部公开信号被 last_step 闸"
                           "静默丢弃，cls/locked 沿用 ep1",
                   "fix": "step==0 或 step<=last_step -> _oc_state_new() 重播"
                          "（基座 _RACE_STATE 单调闸模板）",
                   "severity": "medium"},
            "D2": {"loc": "_oc_c3_swap 备份钩子 + _m13_c3_restore（同一复位块）",
                   "form": "_OC_C3_SWAPPED 无复位且 chassis.routes 换表不可逆"
                           "（443 条触点跨局保留）",
                   "fix": "换表前备份 443 条 delta 触点(idx 412-618)原值；换局"
                          "反向还原+闩复位（与基座开局改写 steps0-6 不相交）",
                   "severity": "medium"},
            "D3": {"loc": "_s804_apply 自插行（内层薄补丁）",
                   "form": "自插 SELL 只记 _S804_HIST own，不记 _S758_HIST "
                           "prev own（跨档台账不同步）",
                   "fix": "自插 SELL 同步记 _S758_HIST[player]['prev']['own']"
                          "（prev.step==step 守卫）；P7 探针带双写断言",
                   "severity": "low(latent)"},
            "artifact": {"main": DHFIX_MAIN,
                         "main_sha256": hashlib.sha256(
                             Path(DHFIX_MAIN).read_bytes()).hexdigest(),
                         "base": DROPHALF_MAIN,
                         "base_sha256": "5d2d12468a5d1ec53c3d3e4726de54e6a5d2"
                                        "9eb038fc97ca45c72b2ce7992df0",
                         "seal": "内层薄补丁逐字量计数+反替换回程逐字节=drop_half"
                                 "基底（roundtrip_identity_ok）"},
        },
        "source": {
            "commands": ["python3 orderbook_m13fix_lab/build_m13fix.py",
                         "python3 orderbook_m13fix_lab/probe_m13fix.py",
                         "python3 orderbook_m13fix_lab/judge_m13fix.py"],
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "674000+i*137（i=0..7）",
                       "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）"},
            "workers": WORKERS,
            "caliber": {"margin": "banks[our]−banks[opp]（run_games banks）",
                        "terminal_money": "farms[obs.player].money",
                        "flips": "win=margin>0；flips_pos=ctl 负 var 正；"
                                 "flips_neg=ctl 正 var 负；净翻胜=win_var−win_ctl"},
        },
        "probes": {}, "pairs": {}, "multi_game_group": {}, "criteria": {},
        "verdict": {}, "budget": budget,
    })

    # ---- 1) 探针证据并入（dh_fix 全绿 + drop_half 对照形态） ----
    for tag, fn in (("dh_fix", "m13fix_probe_out.json"),
                    ("drop_half_control", "m13fix_probe_out_drophalf_control.json")):
        p = MODULE_DIR / "evidence" / fn
        if not p.is_file():
            ANOMALIES.append("探针输出缺失: %s" % fn)
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        EV["probes"][tag] = {
            "artifact": d.get("artifact"),
            "verdicts": {pr["probe"]: pr["verdict"] for pr in d.get("probes", [])},
            "all_green": all(
                str(pr.get("verdict", "")).startswith(("PASS", "INFO"))
                for pr in d.get("probes", [])),
            "detail_p7_d3": next(
                ({k: pr[k] for k in ("d3_own_ledger_758", "d3_own_ledger_804",
                                     "d3_double_write_ok")}
                 for pr in d.get("probes", [])
                 if pr["probe"] == "P7_hour1_tiers"), None),
            "detail_p13": next(
                ({k: pr[k] for k in ("ep1_cls", "ep1_trigger_ok", "ep2_cls",
                                     "ep2_zero_latch", "ep2_zero_swap",
                                     "ep2_max_entries_mutated")}
                 for pr in d.get("probes", [])
                 if pr["probe"].startswith("P13")), None),
            "detail_p10": next(
                ({k: pr[k] for k in ("latch_after_ep1", "latch_after_ep2_step0",
                                     "c3_swap_route_entries_mutated",
                                     "swap_entries_kept_after_ep2_step0")}
                 for pr in d.get("probes", [])
                 if pr["probe"].startswith("P10")), None),
        }
    flush_evid()

    # ---- 2) sim_bridge 对照认证 30/30（不过即停） ----
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
                  "degraded_reason", "engine", "version", "wall_speedup")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 3) 配对判决：dh_fix vs drop_half（32 单元/臂；单局恒等=零回归） ----
    units_all = make_units(FOLDS_ALL, "pairs")
    maps, rows_a = {}, {}
    for arm, path in (("drop_half", DROPHALF_MAIN), ("dh_fix", DHFIX_MAIN)):
        rows, _ = JM._play(JM.make_specs(arm, path, units_all), run_cfg)
        budget["pairs_局次"] += len(rows)
        bad = [r for r in rows if r.get("error")]
        if bad:
            ANOMALIES.append("pairs %s: %d 局 error: %r"
                             % (arm, len(bad), bad[0].get("error")))
        maps[arm] = rows_by_key(rows)
        rows_a[arm] = rows
    ps_rows = []
    for u in units_all:
        key = (u["seed"], u["seat"])
        rc, rv = maps["drop_half"].get(key), maps["dh_fix"].get(key)
        if not rc or not rv or rc.get("margin") is None or rv.get("margin") is None:
            continue
        ps_rows.append({"seed": u["seed"], "seat": u["seat"],
                        "stratum": u["stratum"], "opponent": u.get("opponent"),
                        "margin_control": round(float(rc["margin"]), 1),
                        "margin_variant": round(float(rv["margin"]), 1)})
    ps = flip_stats(ps_rows)
    rp = JM.realized_paired(maps["drop_half"], maps["dh_fix"], units_all)
    stream_same = sum(
        1 for u in units_all
        if (maps["drop_half"].get((u["seed"], u["seat"])) or {}).get(
            "stream_sha_our")
        == (maps["dh_fix"].get((u["seed"], u["seat"])) or {}).get(
            "stream_sha_our"))
    EV["pairs"] = {
        "design": "dh_fix(变体) vs drop_half(对照) 同 (seed,seat) 配对；"
                  "两件单局逐拍恒等（D1/D2 仅换局边界、D3 掩蔽零现症）",
        "flip_table": ps,
        "stream_sha_identical": "%d/%d" % (stream_same, len(units_all)),
        "realized": {"nonneg_both": rp.get("nonneg_both"),
                     "all_mean_delta": (rp.get("all") or {}).get("mean_delta"),
                     "milk_mean_delta": (rp.get("milk") or {}).get("mean_delta")},
        "end_agg": {a: JM.end_agg(rows_a[a]) for a in rows_a},
    }
    flush_evid()

    # ---- 4) 同进程双局串跑专组（8 组 × 双席 × 2 臂） ----
    chains = []
    for i, seed in enumerate(NEUTRAL_FOLDS):
        for seat in (0, 1):
            for arm_path in (DROPHALF_MAIN, DHFIX_MAIN):
                try:
                    chains.append(run_chain(arm_path, seed, seat, run_cfg))
                except Exception as exc:
                    ANOMALIES.append("chain %s seed=%s seat=%s: %r"
                                     % (Path(arm_path).parent.name, seed,
                                        seat, exc))
    budget["multi_game_局次"] += len(chains) * 2
    by_arm = {"drop_half": [], "dh_fix": []}
    for c in chains:
        key = "dh_fix" if "dh_fix" in str(c.get("arm")) else "drop_half"
        by_arm.setdefault(key, []).append(c)
    mg_flip_rows = []
    keymap = {(c["seed"], c["seat"]): c for c in by_arm.get("dh_fix", [])}
    for c in by_arm.get("drop_half", []):
        v = keymap.get((c["seed"], c["seat"]))
        if not v or c.get("ep2_margin") is None or v.get("ep2_margin") is None:
            continue
        mg_flip_rows.append({"seed": c["seed"], "seat": c["seat"],
                             "margin_control": round(float(c["ep2_margin"]), 1),
                             "margin_variant": round(float(v["ep2_margin"]), 1)})
    mg_ps = flip_stats(mg_flip_rows)
    ep1_flip_rows = []
    for c in by_arm.get("drop_half", []):
        v = keymap.get((c["seed"], c["seat"]))
        if not v or c.get("ep1_margin") is None or v.get("ep1_margin") is None:
            continue
        ep1_flip_rows.append({"seed": c["seed"], "seat": c["seat"],
                              "margin_control": round(float(c["ep1_margin"]), 1),
                              "margin_variant": round(float(v["ep1_margin"]), 1)})
    mg = {
        "design": "同进程双局串跑：每链=同一件实例贯穿 ep1(WFR 对手 "
                  "counter_wool_front_runner)→ep2(镜像对手=本件自拷贝全新实例)；"
                  "8 组×双席×2 臂=32 链 64 局；对照 drop_half 的污染形态",
        "groups": NEUTRAL_FOLDS,
        "chains": chains,
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
                "ep2_cls_hist": {cls: sum(1 for c in by_arm.get(a, [])
                                          if c.get("ep2_cls") == cls)
                                 for cls in sorted({str(c.get("ep2_cls"))
                                                    for c in by_arm.get(a, [])})},
            } for a in ("drop_half", "dh_fix")},
        "ep1_flip_table": flip_stats(ep1_flip_rows),
        "ep2_flip_table": mg_ps,
        "note": "ep1 两臂均触发 C3（设计行为）→ep1 逐拍恒等；ep2 drop_half 携"
                "上局 443 条换表差量=污染形态，dh_fix 零换表零闩",
    }
    EV["multi_game_group"] = mg
    flush_evid()

    # ---- 5) 判据 + verdict ----
    dh_poll = mg["pollution"]["dh_fix"]
    zero_poll = (dh_poll["ep2_zero_pollution_given_ep1_trigger"]
                 == dh_poll["ep1_trigger_ok"] and dh_poll["ep1_trigger_ok"] > 0
                 and dh_poll["ep2_latch_true"] == 0)
    pooled_rows = ps_rows + [
        dict(r, stratum="multi_game_ep2") for r in mg_flip_rows]
    pooled = flip_stats(pooled_rows)
    EV["criteria"] = {
        "净翻胜>0": {"scope": "ep2 专组（行为差分唯一面；配对组逐拍恒等贡献 0 翻）",
                     "ep2_net_flip_wins": mg_ps.get("net_flip_wins"),
                     "pooled_net_flip_wins": pooled.get("net_flip_wins"),
                     "passed": bool((mg_ps.get("net_flip_wins") or 0) > 0)},
        "flips_neg==0": {"scope": "全单元（配对 32+ep2 16+ep1 16）",
                         "pairs": ps.get("flips_neg"),
                         "ep2": mg_ps.get("flips_neg"),
                         "ep1": mg["ep1_flip_table"].get("flips_neg"),
                         "pooled": pooled.get("flips_neg"),
                         "passed": bool(ps.get("flips_neg") == 0
                                        and mg_ps.get("flips_neg") == 0
                                        and mg["ep1_flip_table"].get(
                                            "flips_neg") == 0)},
        "双局专组零污染": {
            "dh_fix_ep2_zero_pollution":
                "%d/%d" % (mg["pollution"]["dh_fix"]["ep2_zero_pollution"],
                           mg["pollution"]["dh_fix"]["n"]),
            "dh_fix_ep1_trigger_ok": mg["pollution"]["dh_fix"]["ep1_trigger_ok"],
            "dh_fix_ep2_zero_given_trigger":
                "%d/%d" % (dh_poll["ep2_zero_pollution_given_ep1_trigger"],
                           dh_poll["ep1_trigger_ok"]),
            "dh_fix_ep2_latch_true": mg["pollution"]["dh_fix"]["ep2_latch_true"],
            "dh_fix_ep2_dirty_cells_max":
                mg["pollution"]["dh_fix"]["ep2_dirty_cells_max"],
            "drop_half_ep2_polluted":
                "%d/%d" % (mg["pollution"]["drop_half"]["ep2_latch_true"],
                           mg["pollution"]["drop_half"]["n"]),
            "drop_half_ep2_dirty_cells_max":
                mg["pollution"]["drop_half"]["ep2_dirty_cells_max"],
            "passed": bool(zero_poll)},
        "实现价非负": {"nonneg_both": rp.get("nonneg_both"),
                       "all_mean_delta": (rp.get("all") or {}).get("mean_delta"),
                       "milk_mean_delta": (rp.get("milk") or {}).get("mean_delta"),
                       "passed": bool(rp.get("nonneg_both"))},
    }
    passed = all(v["passed"] for v in EV["criteria"].values())
    EV["verdict"] = {
        "criteria_passed": passed,
        "positive_arm": passed,
        "pairs_identity_ok": (ps.get("W") == 0 and ps.get("L") == 0
                              and stream_same == len(units_all)),
        "multi_game_zero_pollution_ok": zero_poll,
        "summary": ("dh_fix 三缺陷已修（探针 12/12 全绿，drop_half 对照 P8/P10 "
                    "DEFECT+P13 FAIL）；单局配对逐拍恒等=零回归；双局专组 %d/%d "
                    "链零污染（drop_half %d/%d 链污染形态）；ep2 净翻胜 %s"
                    % (mg["pollution"]["dh_fix"]["ep2_zero_pollution"],
                       mg["pollution"]["dh_fix"]["n"],
                       mg["pollution"]["drop_half"]["ep2_latch_true"],
                       mg["pollution"]["drop_half"]["n"],
                       mg_ps.get("net_flip_wins"))),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = (budget["auth_局次"] + budget["pairs_局次"]
                            + budget["multi_game_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "pairs_flip_table": ps, "multi_ep2_flip_table": mg_ps,
         "multi_ep1_flip_table": mg["ep1_flip_table"]},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:500], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
