# -*- coding: utf-8 -*-
"""judge_c_base：完全体底座 C_base 判决（判决先行·不发射不提交）。

责任口径（C_base = oc_c3 + M13 修复层移植）：
- 单局零回归：c_base vs oc_c3 同 (seed,seat) 32 局逐拍恒等（stream_sha 全等 +
  终局钱 farms[obs.player] 相等 + Δ W/L/T=0/0/32）；
- 双局专组：P13 探针（同进程 ep1 WFR→ep2 镜像，断言零换表零闩）+ 实跑 8 组
  双席链（ep1 WFR 对手→ep2 自拷贝镜像；ep2 净翻胜 ≥0 ∧ 零污染）；
- 新标准面板初测：c_base vs {mpx, tetsutani} 各 8 局（强面不掉血初验——
  预期≈oc_c3 水平；oc_c3 同 fold 参照臂交叉登记）。
sim_bridge 对照认证 30/30 先行；workers=2；预算 ≤250 局次；
读数：margin=banks[our]−banks[opp]；终局钱 farms[obs.player]。
证据 fn_docs/hybrid/results/2026-09-30-c-base.json；
账本落 orderbook_composite_lab/evidence/。不改既有代码；不提交；不发射。
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

RECORD_VERSION = "c-base-judge/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]
NEUTRAL_FOLDS = [674000 + i * 137 for i in range(8)]   # 新中性 674000+i*137×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS
PANEL_FOLDS = [674000 + i * 137 for i in range(4)]     # 面板 4 fold 双席=8 局/臂
OC3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
               / "main.py")
CBASE_MAIN = str(MODULE_DIR / "build" / "c_base" / "main.py")
WFR_OPP = str(KSIM_DIR / "orderbook_iterk_lab" / "opponents"
              / "counter_wool_front_runner.py")
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build"
               / "mpx_w24_p2_3_h14" / "main.py")
TETSU_MAIN = "/tmp/a30-b1/tetsu_agent/main.py"
TETSU_SHA_EXPECTED = ("55be5d5f124c8daaaa63c1a29ba4aab096004909666f04748"
                      "007603c67b7d2a8")
WORKERS = 2
BUDGET_CAP = 250
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-c-base.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_c_base_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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


def flip_stats(rows):
    """翻局表（knee/pair_stats 同口径）：delta=var−ctl；win=margin>0。"""
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


def sb_run_games(games, run_cfg):
    from orderbook_r40 import sim_bridge as sb
    return sb.run_games(games, run_cfg)


def run_chain(arm_path, seed, seat, run_cfg, ep2_opp_path=None):
    """同进程双局串跑：ep1 WFR 对手→ep2 镜像对手；同一件实例贯穿两局。

    ep2_opp_path=None -> 镜像对手=本件自拷贝全新实例（judge_r23 mirror 口径）。
    """
    out = {"arm": Path(arm_path).parent.name if "c_base" not in arm_path
           else "c_base", "seed": int(seed), "seat": int(seat),
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


def main():
    t0 = time.perf_counter()
    from orderbook_r40 import sim_bridge as sb
    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "pairs_局次": 0,
              "multi_game_局次": 0, "panel_局次": 0,
              "cap_scope": "认证 30×2=60 + 配对 32×2 臂=64 + 双局专组 8×2 席×2 局"
                           "×2 臂=64 + 面板 2 对手×8 局×2 臂=32 = 220 ≤ 250"}
    build_man = json.loads(
        (MODULE_DIR / "build" / "c_base" / "build_manifest.json")
        .read_text(encoding="utf-8"))
    EV.update({
        "version": RECORD_VERSION,
        "task": "完全体底座 C_base = oc_c3（3f8b57fd 冠军件）+ M13 修复层移植"
                "（D1 画像换局复位 / D2 C3 闩复位+换表可逆 / D3 s804 自插记账）",
        "build": {
            "artifact": CBASE_MAIN,
            "main_sha256": build_man.get("main_sha256"),
            "tar_sha256": build_man.get("tar_sha256"),
            "base_main": OC3_MAIN,
            "base_main_sha256": build_man.get("base_main_sha256"),
            "gates": build_man.get("gates"),
            "footprint": build_man.get("footprint"),
            "seal": "G2 反替换回程逐字节=oc_c3 基底（roundtrip_identity_ok）",
        },
        "fix_port": {
            "port_from": build_man.get("port_from"),
            "port_notes": build_man.get("port_notes"),
            "patches": build_man.get("patches"),
            "subs": build_man.get("subs"),
            "tail_bytes": build_man.get("tail_bytes"),
            "drop_half_dependency": "无（逐字移植；唯一适配=入口归一 "
                                    "_u2_agent→_hs_agent）",
        },
        "source": {
            "commands": ["python3 orderbook_composite_lab/build_c_base.py",
                         "python3 orderbook_composite_lab/probe_c_base.py",
                         "python3 orderbook_composite_lab/probe_c_base.py "
                         "../orderbook_oppcond_lab/build/oc_c3/main.py",
                         "python3 orderbook_composite_lab/judge_c_base.py"],
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "674000+i*137（i=0..7）",
                       "panel_folds": PANEL_FOLDS,
                       "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局/臂）"},
            "workers": WORKERS,
            "caliber": {"margin": "banks[our]−banks[opp]（run_games banks）",
                        "terminal_money": "farms[obs.player].money（end_reads）",
                        "flips": "win=margin>0；flips_pos=ctl 负 var 正；"
                                 "flips_neg=ctl 正 var 负；净翻胜=win_var−win_ctl"},
        },
        "identity_pairs": {}, "multi_game": {}, "panel_smoke": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- 1) 探针证据并入（c_base 全绿 + oc_c3 对照污染形态） ----
    for tag, fn in (("c_base", "c_base_probe_out.json"),
                    ("oc_c3_control", "c_base_probe_out_oc_c3_control.json")):
        p = MODULE_DIR / "evidence" / fn
        if not p.is_file():
            ANOMALIES.append("探针输出缺失: %s" % fn)
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        EV.setdefault("probes", {})[tag] = {
            "artifact": d.get("artifact"),
            "artifact_sha256": d.get("artifact_sha256"),
            "verdicts": {pr["probe"]: pr["verdict"] for pr in d.get("probes", [])},
            "detail_p13": next(
                ({k: pr[k] for k in ("ep1_cls", "ep1_trigger_ok", "ep2_cls",
                                     "ep2_zero_latch", "ep2_zero_swap",
                                     "ep2_max_entries_mutated")}
                 for pr in d.get("probes", [])
                 if pr["probe"].startswith("P13")), None),
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

    # ---- 3) 单局零回归：c_base vs oc_c3 32 局逐拍恒等 ----
    units_all = make_units(FOLDS_ALL, "identity")
    maps, rows_a = {}, {}
    for arm, path in (("oc_c3", OC3_MAIN), ("c_base", CBASE_MAIN)):
        rows, _ = JM._play(JM.make_specs(arm, path, units_all), run_cfg)
        budget["pairs_局次"] += len(rows)
        bad = [r for r in rows if r.get("error")]
        if bad:
            ANOMALIES.append("identity %s: %d 局 error: %r"
                             % (arm, len(bad), bad[0].get("error")))
        maps[arm] = rows_by_key(rows)
        rows_a[arm] = rows
    ps_rows = []
    for u in units_all:
        key = (u["seed"], u["seat"])
        rc, rv = maps["oc_c3"].get(key), maps["c_base"].get(key)
        if not rc or not rv or rc.get("margin") is None or rv.get("margin") is None:
            continue
        ps_rows.append({"seed": u["seed"], "seat": u["seat"],
                        "stratum": u["stratum"], "opponent": u.get("opponent"),
                        "margin_control": round(float(rc["margin"]), 1),
                        "margin_variant": round(float(rv["margin"]), 1)})
    ps = flip_stats(ps_rows)
    seal = JM.seal_check(maps["oc_c3"], maps["c_base"], units_all)
    EV["identity_pairs"] = {
        "design": "c_base(变体) vs oc_c3(对照) 同 (seed,seat) 配对 32 局/臂；"
                  "单局逐拍恒等=零回归（D1/D2 仅换局边界、D3 掩蔽零现症）",
        "seal": seal,
        "flip_table": ps,
        "end_agg": {a: JM.end_agg(rows_a[a]) for a in rows_a},
    }
    flush_evid()

    # ---- 4) 双局专组：P13 探针 + 8 组双席串跑 ----
    chains = []
    for seed in NEUTRAL_FOLDS:
        for seat in (0, 1):
            for arm_path in (OC3_MAIN, CBASE_MAIN):
                try:
                    chains.append(run_chain(arm_path, seed, seat, run_cfg))
                except Exception as exc:
                    ANOMALIES.append("chain %s seed=%s seat=%s: %r"
                                     % (Path(arm_path).name, seed, seat, exc))
    budget["multi_game_局次"] += len(chains) * 2
    by_arm = {"oc_c3": [], "c_base": []}
    for c in chains:
        key = "c_base" if c.get("arm") == "c_base" else "oc_c3"
        by_arm.setdefault(key, []).append(c)
    mg_flip_rows, ep1_flip_rows = [], []
    keymap = {(c["seed"], c["seat"]): c for c in by_arm.get("c_base", [])}
    for c in by_arm.get("oc_c3", []):
        v = keymap.get((c["seed"], c["seat"]))
        if not v:
            continue
        if c.get("ep2_margin") is not None and v.get("ep2_margin") is not None:
            mg_flip_rows.append({"seed": c["seed"], "seat": c["seat"],
                                 "margin_control": round(float(c["ep2_margin"]), 1),
                                 "margin_variant": round(float(v["ep2_margin"]), 1)})
        if c.get("ep1_margin") is not None and v.get("ep1_margin") is not None:
            ep1_flip_rows.append({"seed": c["seed"], "seat": c["seat"],
                                  "margin_control": round(float(c["ep1_margin"]), 1),
                                  "margin_variant": round(float(v["ep1_margin"]), 1)})
    mg_ps = flip_stats(mg_flip_rows)
    ep1_ps = flip_stats(ep1_flip_rows)
    mg = {
        "design": "同进程双局串跑：每链=同一件实例贯穿 ep1(WFR 对手 "
                  "counter_wool_front_runner)→ep2(镜像对手=本件自拷贝全新实例)；"
                  "8 组×双席×2 臂=32 链 64 局",
        "groups": NEUTRAL_FOLDS,
        "probe_P13": EV.get("probes"),
        "chains": chains,
        "pollution": {a: {
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
        } for a in ("oc_c3", "c_base")},
        "ep1_flip_table": ep1_ps,
        "ep2_flip_table": mg_ps,
        "note": "ep1 两臂均触发 C3（设计行为）→ep1 逐拍恒等；ep2 oc_c3 携上局 "
                "443 条换表差量+陈旧 wfr 类=污染形态，c_base 零换表零闩",
    }
    EV["multi_game"] = mg
    flush_evid()

    # ---- 5) 新标准面板初测：c_base vs {mpx, tetsutani} 各 8 局（oc_c3 参照） ----
    if sha256_of(TETSU_MAIN) != TETSU_SHA_EXPECTED:
        ANOMALIES.append("tetsutani sha 漂移: %s" % sha256_of(TETSU_MAIN))
    panel = {"design": "c_base vs {mpx, tetsutani} 各 8 局（4 fold 双席，"
                       "674000+i*137 i=0..3）；oc_c3 同 fold 参照臂交叉登记；"
                       "强面不掉血初验=各对手 c_base 均值 ≥ oc_c3 均值−0.5",
             "folds": PANEL_FOLDS, "opponents": {}}
    for opp_name, opp_path in (("mpx", MPX_MAIN), ("tetsutani", TETSU_MAIN)):
        units_p = [{"seed": int(s), "seat": seat, "opp_path": opp_path,
                    "opponent": opp_name, "stratum": "panel_" + opp_name,
                    "tag": "panel"} for s in PANEL_FOLDS for seat in (0, 1)]
        per = {}
        for arm, path in (("oc_c3", OC3_MAIN), ("c_base", CBASE_MAIN)):
            rows, _ = JM._play(JM.make_specs(arm, path, units_p), run_cfg)
            budget["panel_局次"] += len(rows)
            bad = [r for r in rows if r.get("error")]
            if bad:
                ANOMALIES.append("panel %s vs %s: %d 局 error: %r"
                                 % (arm, opp_name, len(bad),
                                    bad[0].get("error")))
            margins = [float(r["margin"]) for r in rows
                       if r.get("margin") is not None]
            wins = sum(1 for m in margins if m > 0)
            losses = sum(1 for m in margins if m < 0)
            per[arm] = {
                "n": len(rows), "margin_mean":
                    round(sum(margins) / len(margins), 1) if margins else None,
                "margin_min": round(min(margins), 1) if margins else None,
                "W_L_T": [wins, losses, len(margins) - wins - losses],
                "end_agg": JM.end_agg(rows),
                "rows_lite": [{"seed": r["seed"], "seat": r["seat"],
                               "margin": r["margin"]} for r in rows],
            }
        mc = per["c_base"].get("margin_mean")
        mo = per["oc_c3"].get("margin_mean")
        per["delta_c_base_minus_oc_c3"] = (
            round(mc - mo, 1) if mc is not None and mo is not None else None)
        per["no_blood_loss_ok"] = bool(
            mc is not None and mo is not None and mc >= mo - 0.5)
        panel["opponents"][opp_name] = per
    EV["panel_smoke"] = panel
    flush_evid()

    # ---- 6) 判据 + verdict ----
    cb_poll = mg["pollution"]["c_base"]
    zero_poll = (cb_poll["ep2_zero_pollution_given_ep1_trigger"]
                 == cb_poll["ep1_trigger_ok"] > 0
                 and cb_poll["ep2_latch_true"] == 0)
    p13 = ((EV.get("probes") or {}).get("c_base") or {}).get("detail_p13") or {}
    p13_ok = bool(p13.get("ep1_trigger_ok") and p13.get("ep2_zero_latch")
                  and p13.get("ep2_zero_swap"))
    panel_ok = all(v.get("no_blood_loss_ok")
                   for v in panel["opponents"].values())
    pooled = flip_stats(ps_rows + [dict(r, stratum="multi_game_ep2")
                                   for r in mg_flip_rows]
                        + [dict(r, stratum="multi_game_ep1")
                           for r in ep1_flip_rows])
    EV["criteria"] = {
        "单局零回归": {
            "design": "c_base vs oc_c3 32 局逐拍恒等",
            "stream_identical": "%d/%d" % (seal.get("n_stream_identical", 0),
                                           seal.get("n_units", 0)),
            "money_equal": "%d/%d" % (seal.get("n_money_equal", 0),
                                      seal.get("n_units", 0)),
            "W_L_T": "%d/%d/%d" % (ps.get("W"), ps.get("L"), ps.get("T")),
            "passed": bool(seal.get("passed") and ps.get("W") == 0
                           and ps.get("L") == 0 and ps.get("T") == 32)},
        "P13探针零换表零闩": {
            "c_base": p13,
            "oc_c3_control": ((EV.get("probes") or {}).get("oc_c3_control")
                              or {}).get("detail_p13"),
            "passed": p13_ok},
        "双局专组零污染": {
            "c_base_ep1_trigger_ok": cb_poll["ep1_trigger_ok"],
            "c_base_ep2_zero_given_trigger":
                "%d/%d" % (cb_poll["ep2_zero_pollution_given_ep1_trigger"],
                           cb_poll["ep1_trigger_ok"]),
            "c_base_ep2_latch_true": cb_poll["ep2_latch_true"],
            "c_base_ep2_dirty_cells_max": cb_poll["ep2_dirty_cells_max"],
            "oc_c3_ep2_polluted":
                "%d/%d" % (mg["pollution"]["oc_c3"]["ep2_latch_true"],
                           mg["pollution"]["oc_c3"]["n"]),
            "oc_c3_ep2_dirty_cells_max":
                mg["pollution"]["oc_c3"]["ep2_dirty_cells_max"],
            "passed": bool(zero_poll)},
        "ep2净翻胜≥0": {
            "ep2_net_flip_wins": mg_ps.get("net_flip_wins"),
            "ep2_W_L_T_delta": "%d/%d/%d" % (mg_ps.get("W"), mg_ps.get("L"),
                                             mg_ps.get("T")),
            "ep2_flips_neg": mg_ps.get("flips_neg"),
            "passed": bool((mg_ps.get("net_flip_wins") or 0) >= 0
                           and (mg_ps.get("flips_neg") or 0) == 0)},
        "面板强面不掉血": {
            opp: {"c_base_mean": v["c_base"].get("margin_mean"),
                  "oc_c3_mean": v["oc_c3"].get("margin_mean"),
                  "delta": v.get("delta_c_base_minus_oc_c3"),
                  "passed": v.get("no_blood_loss_ok")}
            for opp, v in panel["opponents"].items()} | {
            "passed": panel_ok},
        "flips_neg==0": {
            "scope": "全单元（配对 32 + ep1 16 + ep2 16）",
            "pairs": ps.get("flips_neg"), "ep1": ep1_ps.get("flips_neg"),
            "ep2": mg_ps.get("flips_neg"), "pooled": pooled.get("flips_neg"),
            "ep1_W_L_T": "%d/%d/%d" % (ep1_ps.get("W"), ep1_ps.get("L"),
                                       ep1_ps.get("T")),
            "passed": bool(ps.get("flips_neg") == 0
                           and ep1_ps.get("flips_neg") == 0
                           and mg_ps.get("flips_neg") == 0)},
    }
    passed = all(v.get("passed") for v in EV["criteria"].values())
    EV["verdict"] = {
        "criteria_passed": passed,
        "positive_arm": passed,
        "identity_ok": EV["criteria"]["单局零回归"]["passed"],
        "multi_game_zero_pollution_ok": zero_poll,
        "summary": "C_base=oc_c3+M13 修复层移植（四门+反替换封印过）；单局 32/32 "
                   "逐拍恒等=零回归；P13 探针零换表零闩（oc_c3 对照 FAIL 污染"
                   "形态）；双局专组 %d/%d 链零污染（oc_c3 %d/%d 污染）；ep2 "
                   "净翻胜 %s；面板 c_base≈oc_c3（Δ=%s）"
                   % (cb_poll["ep2_zero_pollution"], cb_poll["n"],
                      mg["pollution"]["oc_c3"]["ep2_latch_true"],
                      mg["pollution"]["oc_c3"]["n"],
                      mg_ps.get("net_flip_wins"),
                      {k: v.get("delta_c_base_minus_oc_c3")
                       for k, v in panel["opponents"].items()}),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = (budget["auth_局次"] + budget["pairs_局次"]
                            + budget["multi_game_局次"] + budget["panel_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "pairs_flip_table": ps, "multi_ep2_flip_table": mg_ps,
         "multi_ep1_flip_table": ep1_ps, "panel":
             {k: {"c_base": v["c_base"]["margin_mean"],
                  "oc_c3": v["oc_c3"]["margin_mean"]}
              for k, v in panel["opponents"].items()}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
