# -*- coding: utf-8 -*-
"""ab_t1a（track1 A）：H1 路线表逐店对邻域细扫——时机臂+结构邻域臂 因果 A/B。

责任口径（任务 track1-A，战后主攻 P2）：在 K2 线索（ICE_CREAM_SHOP+YARN_STORE
净 +2/臂 n=4 过薄）上做逐店对**邻域细扫**：
- 臂菜单（对每店对生成邻域替代路线，R24 口径）：时机变体 generic(r105)/
  early(r9)/late(r103) + 结构邻域（alt=共享一店店对非基座路线众数；本基座
  alt∈{9,105} 恰与 early/generic 重合，账本按强制路线记标签）+ 优先格结构
  邻域第二线 r122（ICE_CREAM+YARN 专属加密臂）。
- 格=店对（face/pair 逐单元账本）；**每格 n≥8 配对单元**（重点加密
  ICE_CREAM+YARN 及相邻格：挖掘定向选 seed 保证格密度）。
- 判据=任何臂净翻胜>0（win_arm−win_control）**且 n 达标（≥8）**的格。

臂件=尾块覆盖 _IMPL.chassis.router（step144 锁存按臂条件强制路线；底 day27
换线保留）；末 callable 语义保持（_hs_agent）。配对因果口径：step144 市场面
为处理前观测，同 seed+seat 跨臂逐位同，臂间 margin 差=纯路线处理效应。

seed 定向挖掘（mine_worlds）：world 非 seed 纯函数（weeds RNG），但 H1/对手
step<144 动作流磁带经 gengame 重放可**精确**预测店对（K2 32 seeds 实测 32/32），
据此挖目标格 seed；格归属以实跑 trace 为准（预测错配记 anomaly 不入目标格）。

复用（不改写）：orderbook_r40.ab_r41（_ab_play_batch/_specs_for/_agg/
_pair_key/_face_pair_from_sinks）+ judge_r23.DEFAULT_OPPONENTS + sim_bridge
+ orderbook_iterk_lab.ab_k2.h1_base_route_map。只写 orderbook_track1_lab/。
预算：≤250 局次（game 口径；fold 口径=games/2 同报）。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

from orderbook_r40 import ab_r41 as ab  # noqa: E402
from orderbook_r40 import judge_r23 as j23  # noqa: E402
from orderbook_iterk_lab import ab_k2 as k2  # noqa: E402  复用件（不改写）
import mine_worlds as mw  # noqa: E402  同 lab 挖掘件

RECORD_VERSION = "ab-t1a/1.0"
H1_MAIN = k2.H1_MAIN                       # build/h1_base/main.py == strongest h1
AB_OUT_DIR = MODULE_DIR / "ab"
EVID_DIR = MODULE_DIR / "evidence"
LEDGER_PATH = EVID_DIR / "ab_t1a_ledger_realrun.json"
PLAN_PATH = EVID_DIR / "t1a_seed_plan.json"
REVEAL_STEP = 144
WORKERS = 2
BUDGET_CAP_GAMES = 250
SEED_BASE = mw.MINE_SEED_BASE              # 780000 域
PRIORITY_CELL = "ICE_CREAM_SHOP+YARN_STORE"
N_MIN_CELL = 8                             # 每格 n≥8 配对单元（达标线）
PRIORITY_EXTRA_ROUTE = 122                 # 优先格结构邻域第二线（ICE+PIZZA 基座线）

# 臂菜单：强制路线→标签（R24 口径时机变体+结构邻域）
ARM_LABELS = {
    105: ["generic", "alt(struct-neighborhood-mode)"],
    9: ["early", "alt(struct-neighborhood-mode)"],
    103: ["late"],
    PRIORITY_EXTRA_ROUTE: ["nbr-extra(122)", "alt(struct-neighborhood-2nd)"],
}
ARMS = (9, 103, 105, PRIORITY_EXTRA_ROUTE)  # r122 仅优先格目标门

# 格配额：cell→[(opponent_idx 多样化)] combo 数（1 combo=1 seed 双席=2 单元）
CELL_QUOTA = {
    PRIORITY_CELL: 8,                  # 优先格加密：16 单元（8 folds）
    "ICE_CREAM_SHOP+ICE_CREAM_SHOP": 4,
    "ICE_CREAM_SHOP+PET_CAFE": 4,
    "ICE_CREAM_SHOP+PIZZA_SHOP": 4,
    "ICE_CREAM_SHOP+SMOOTHIE_SHOP": 4,
    "PET_CAFE+YARN_STORE": 4,
    "PIZZA_SHOP+YARN_STORE": 4,
    # 广度格（n=2 线索级，不入达标判据）
    "BAKERY+BAKERY": 1,
    "FARMERS_MARKET+FARMERS_MARKET": 1,
    "PET_CAFE+PET_CAFE": 1,
    "BRUNCH_SPOT+SMOOTHIE_SHOP": 1,
}
BREADTH_CELLS = ("BAKERY+BAKERY", "FARMERS_MARKET+FARMERS_MARKET",
                 "PET_CAFE+PET_CAFE", "BRUNCH_SPOT+SMOOTHIE_SHOP")

_TAIL = """
# ===== track1 A 实验臂 %(arm)r（judge-side only；control 臂无此尾块） =====
_T1_BASE_ROUTER = _IMPL.chassis.router
_T1_ROUTE = %(route)d
_T1_BASE_MAP = dict(%(basemap)s)
_T1_TARGET_PAIR = %(target)r


def _t1_router(observation, step, state):
    \"\"\"实验臂：step144 锁存按臂条件强制路线（const 门=基座≠强制线；
    目标门=店对==target）；底 day27 换线保留。\"\"\"
    r = _T1_BASE_ROUTER(observation, step, state)
    try:
        if int(step) >= %(reveal)d and not state.get('t1_latched'):
            state['t1_latched'] = True
            town = observation.get('town') or {}
            shops = sorted(str(s) for s in
                           list(town.get('unlocked_shops') or [])[:2])
            key = "+".join(shops)
            forced = None
            if _T1_TARGET_PAIR is not None:
                if key == _T1_TARGET_PAIR:
                    forced = int(_T1_ROUTE)
            else:
                b = _T1_BASE_MAP.get(key)
                if b is not None and int(b) != int(_T1_ROUTE):
                    forced = int(_T1_ROUTE)
            if forced is not None:
                state['route'] = forced
                r = forced
    except Exception:
        pass
    return r


_IMPL.chassis.router = _t1_router

# ---- 入口归一（末 callable 保持=_hs_agent） ----
_T1_ENTRY_TMP = _hs_agent
del _hs_agent
_hs_agent = _T1_ENTRY_TMP
del _T1_ENTRY_TMP
"""


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_arm_main(main_text: str, route: int, base_map: dict,
                   target_pair=None) -> dict:
    """实验臂件构建（const 门/目标门）；末 callable 语义校验同 K2。"""
    if not isinstance(main_text, str) or not main_text.strip():
        raise ValueError("main_text 非法")
    tail = _TAIL % {"arm": ("r%d" % route) + ("@%s" % target_pair
                                              if target_pair else ""),
                    "route": int(route),
                    "basemap": repr(sorted((str(k), int(v))
                                           for k, v in base_map.items())),
                    "target": target_pair, "reveal": REVEAL_STEP}
    text = main_text + tail
    compile(text, "<ab-t1a-r%d>" % route, "exec")
    if tail.count("\ndef ") + tail.startswith("def ") != 1:
        raise ValueError("臂尾块 def 数异常（末 callable 语义保护）")
    ns: dict = {}
    exec(compile(text, "<ab-t1a-entry:%d>" % route, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_hs_agent":
        raise RuntimeError("末 callable 归一红 r%d: got %r"
                           % (route, loaded[-1].__name__ if loaded else None))
    return {"main_text": text, "route": int(route),
            "target_pair": target_pair, "arm_sha": _sha(text)}


def mine_seed_plan(base_map: dict, recordings=None, srv=None) -> dict:
    """定向挖掘：为 CELL_QUOTA 收集 (seed, opponent) combo（目标格优先）。"""
    own = srv is None
    srv = srv or mw.Serve()
    try:
        if recordings is None:
            recordings = {}
            for j, opp in enumerate(mw.OPPONENTS):
                recordings[opp] = mw.record_pair(opp, mw.REC_SEED_BASE + j, srv)
        # 扫描：每对手独立 seed 流（域内偏移错开防对手×seed 撞格）
        want = dict(CELL_QUOTA)
        found = {c: [] for c in want}
        scanned = 0
        t0 = time.perf_counter()
        stop = False
        for j, opp in enumerate(mw.OPPONENTS):
            if stop:
                break
            rec = recordings.get(opp)
            if rec is None:
                continue
            l0 = rec["tapes"]["order_h1_first"]["lines"]
            for i in range(4000):
                s = SEED_BASE + j * 100000 + i
                wk = mw.predict_world(s, l0[0], l0[1], srv)
                scanned += 1
                pk = mw.pair_key(wk)
                if pk in want and len(found[pk]) < want[pk]:
                    # 对手多样性：每格每对手最多 ceil(quota/4)+1
                    per_opp = sum(1 for x in found[pk]
                                  if x["opponent"] == opp)
                    if per_opp <= (want[pk] + 3) // 4:
                        found[pk].append({"seed": s, "opponent": opp,
                                          "opp_path": str(KSIM_DIR / opp),
                                          "cell_pred": pk})
                if all(len(found[c]) >= want[c] for c in want):
                    stop = True
                    break
        plan = {
            "version": "t1a-seed-plan/1.0",
            "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "seed_domain": "780000+j*100000+i（j=对手序）",
            "n_scanned_predictions": scanned,
            "elapsed_s": round(time.perf_counter() - t0, 2),
            "quota": want,
            "found": found,
            "summary": {c: len(v) for c, v in found.items()},
        }
        PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
        PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=1)
                             + "\n", encoding="utf-8")
        return plan
    finally:
        if own:
            srv.close()


def run_route_scan_ab_t1a(config: dict = None) -> dict:
    """A 细扫编排：control+trace → 各臂（按实际格适用性）→ 逐格账本。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    workers = int(cfg.get("workers", WORKERS))
    opponents = list(cfg.get("opponents") or j23.DEFAULT_OPPONENTS)
    opp_paths = [str(rel) if Path(rel).is_file()
                 else str(KSIM_DIR / rel) for rel in opponents]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)

    main_text = H1_MAIN.read_text(encoding="utf-8")
    base_map = k2.h1_base_route_map()
    AB_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 臂件构建
    arm_paths = {}
    arm_meta = {}
    for route in ARMS:
        target = PRIORITY_CELL if route == PRIORITY_EXTRA_ROUTE else None
        built = build_arm_main(main_text, route, base_map, target)
        p = AB_OUT_DIR / ("ab_t1a_r%d_main.py" % route)
        p.write_text(built["main_text"], encoding="utf-8")
        arm_paths[route] = str(p)
        arm_meta[route] = {"path": str(p), "arm_sha": built["arm_sha"],
                           "target_pair": target,
                           "labels": ARM_LABELS[route]}

    # seed 计划（挖掘）
    plan = cfg.get("seed_plan") or mine_seed_plan(base_map)
    units = []
    for cell, combos in plan["found"].items():
        for c in combos:
            for seat in (0, 1):
                units.append({"seed": int(c["seed"]), "seat": seat,
                              "opp_path": c["opp_path"],
                              "opponent": Path(c["opp_path"]).parent.name,
                              "cell_pred": cell})
    run_cfg = {"engine": cfg.get("engine", "auto"), "workers": workers}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()

    # phase1：control+trace（face/pair/基线 margin；格归属实测）
    p1_rows = ab._ab_play_batch(
        ab._specs_for(units, "control", str(H1_MAIN), True), run_cfg)
    by_key = {(int(r["seed"]), int(r["seat"])): r for r in p1_rows}

    # phase2：按臂跑适用单元（const 门=实际格基座≠强制线；r122=优先格）
    arm_rows = {}
    arm_games = 0
    for route in ARMS:
        t_units = []
        for u in units:
            r1 = by_key.get((u["seed"], u["seat"]))
            if r1 is None or r1.get("error") is not None or \
                    r1.get("margin") is None:
                continue
            pair = r1.get("pair")
            if pair is None:
                continue
            b = base_map.get(pair)
            if route == PRIORITY_EXTRA_ROUTE:
                ok = pair == PRIORITY_CELL
            else:
                ok = b is not None and int(b) != int(route)
            if ok:
                t_units.append(u)
        if not t_units:
            arm_rows[route] = {}
            continue
        if 1 * len(units) + arm_games + len(t_units) > BUDGET_CAP_GAMES:
            # 预算硬闸（不应触发；触发即裁臂并记 anomaly）
            arm_rows[route] = {"__skipped_budget__": len(t_units)}
            continue
        rows = ab._ab_play_batch(
            ab._specs_for(t_units, "r%d" % route, arm_paths[route], False),
            run_cfg)
        arm_games += len(t_units)
        arm_rows[route] = {(int(r["seed"]), int(r["seat"])): r
                           for r in rows}

    # 账本：逐单元 face/arm/route/margin
    led_units = []
    for u in units:
        r1 = by_key.get((u["seed"], u["seat"]))
        if r1 is None or r1.get("error") is not None or \
                r1.get("margin") is None:
            continue
        pair = r1.get("pair")
        rec = {"seed": u["seed"], "seat": u["seat"],
               "opponent": u["opponent"], "face": r1.get("face"),
               "pair": pair, "cell_pred": u.get("cell_pred"),
               "cell_match": pair == u.get("cell_pred"),
               "route_control": base_map.get(pair),
               "margin_control": r1["margin"], "arms": {}}
        for route in ARMS:
            rows = arm_rows.get(route) or {}
            if isinstance(rows, dict) and "__skipped_budget__" in rows:
                continue
            r2 = rows.get((u["seed"], u["seat"]))
            if r2 is None or r2.get("error") is not None:
                continue
            if r2.get("margin") is None:
                continue
            b = base_map.get(pair)
            if route == PRIORITY_EXTRA_ROUTE:
                applies = pair == PRIORITY_CELL
            else:
                applies = b is not None and int(b) != int(route)
            if not applies:
                continue
            rec["arms"][str(route)] = {
                "route": int(route), "labels": ARM_LABELS[route],
                "margin_arm": r2["margin"],
                "delta": r2["margin"] - r1["margin"]}
        if rec["arms"]:
            led_units.append(rec)

    # 逐格×臂聚合（净翻胜=win_arm−win_control）
    cells = {}
    for lu in led_units:
        cell = lu["pair"] or "NONE"
        for rk, av in lu["arms"].items():
            c = cells.setdefault(cell, {}).setdefault(
                rk, {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
                     "margin_arm_sum": 0.0, "win_control": 0, "win_arm": 0,
                     "flips_pos": 0, "flips_neg": 0})
            c["n"] += 1
            c["delta_sum"] += av["delta"]
            c["margin_control_sum"] += lu["margin_control"]
            c["margin_arm_sum"] += av["margin_arm"]
            wc = 1 if lu["margin_control"] > 0 else 0
            wa = 1 if av["margin_arm"] > 0 else 0
            c["win_control"] += wc
            c["win_arm"] += wa
            if wc and not wa:
                c["flips_neg"] += 1
            if wa and not wc:
                c["flips_pos"] += 1

    cell_table = {}
    positive_cells = []
    for cell in sorted(cells):
        cell_table[cell] = {}
        for rk in sorted(cells[cell], key=int):
            v = cells[cell][rk]
            agg = ab._agg(v)
            agg["net_flip_wins"] = int(v["win_arm"]) - int(v["win_control"])
            agg["flips_pos"] = v["flips_pos"]
            agg["flips_neg"] = v["flips_neg"]
            agg["labels"] = ARM_LABELS[int(rk)]
            agg["route"] = int(rk)
            agg["n_folds"] = v["n"] // 2
            agg["n达标"] = bool(v["n"] >= N_MIN_CELL)
            cell_table[cell][rk] = agg
            if agg["net_flip_wins"] > 0 and agg["n达标"]:
                positive_cells.append({"cell": cell, "route": int(rk),
                                       "labels": agg["labels"],
                                       "net_flip_wins": agg["net_flip_wins"],
                                       "n": v["n"]})

    # 全量（臂级）
    overall = {}
    for route in ARMS:
        tot = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
               "margin_arm_sum": 0.0, "win_control": 0, "win_arm": 0}
        for by_arm in cells.values():
            f = by_arm.get(str(route))
            if f:
                for k in tot:
                    tot[k] += f[k]
        if tot["n"]:
            a = ab._agg(tot)
            a["net_flip_wins"] = int(tot["win_arm"]) - int(tot["win_control"])
            a["labels"] = ARM_LABELS[route]
            overall[str(route)] = a

    verdict = {
        "criterion": "任何臂净翻胜>0 且 n 达标（每格 n≥%d 配对单元）" % N_MIN_CELL,
        "positive_cells": positive_cells,
        "verdict": ("ALT_ARM_CANDIDATE: %s" % [
            "%s/%s" % (p["cell"], p["labels"][0]) for p in positive_cells])
        if positive_cells else
        "NO_POSITIVE_ARM_AT_N（n 达标格无正翻胜臂；未达标格仅线索级）",
    }

    n_control = len([u for u in led_units])
    games = {"control": len(units), "arms": arm_games,
             "total": len(units) + arm_games,
             "cap": BUDGET_CAP_GAMES}
    ledger = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"workers": workers, "opponents": opp_paths,
                   "arms": [{"route": r, **arm_meta[r]} for r in ARMS],
                   "main_sha": _sha(main_text),
                   "base_map_n": len(base_map),
                   "priority_cell": PRIORITY_CELL,
                   "priority_extra_route": PRIORITY_EXTRA_ROUTE,
                   "cell_quota": plan.get("quota"),
                   "seed_plan_summary": plan.get("summary"),
                   "n_min_cell": N_MIN_CELL},
        "games": games,
        "games_folds": {"folds_total": games["total"] // 2},
        "n_units_planned": len(units),
        "n_units_paired": n_control,
        "cell_match_rate": round(
            sum(1 for lu in led_units if lu["cell_match"]) /
            max(1, len(led_units)), 4),
        "units": led_units,
        "cell_table": cell_table,
        "overall": overall,
        "verdict": verdict,
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1)
                           + "\n", encoding="utf-8")
    ledger["ledger_path"] = str(LEDGER_PATH)
    return {"ledger": ledger, "cell_table": cell_table,
            "verdict": verdict, "games": games}


def ensure_auth(auth_corpus=None):
    """sim_bridge 认证 30/30（本 lab 留档；不达标→官方引擎降级返回）。"""
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_path = EVID_DIR / "sim_auth.json"
    if auth_path.is_file():
        prev = json.loads(auth_path.read_text(encoding="utf-8"))
        if prev.get("consistency_ok"):
            return {"loaded": prev.get("loaded", True),
                    "consistency_ok": True, "reused": True}
    corpus = list(auth_corpus or
                  [880000 + i for i in range(32)])
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, corpus)
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    auth_path.write_text(json.dumps(
        {k: auth.get(k) for k in
         ("loaded", "consistency", "wall_speedup", "consistency_ok",
          "engine", "timing", "version")}, ensure_ascii=False, indent=1,
        default=str) + "\n", encoding="utf-8")
    return auth


def main():
    os.chdir(KSIM_DIR)
    auth = ensure_auth()
    print("auth:", auth.get("consistency"), auth.get("consistency_ok"),
          flush=True)
    if not auth.get("consistency_ok"):
        print("ABORT: sim_bridge 对照认证未过 30/30", flush=True)
        return {"aborted": "sim_bridge 对照认证未过 30/30"}
    res = run_route_scan_ab_t1a({
        "workers": WORKERS, "engine": "auto", "bridge": auth})
    print("A verdict:", res["verdict"], flush=True)
    print("A games:", res["games"], flush=True)
    return res


if __name__ == "__main__":
    main()
