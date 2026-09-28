# -*- coding: utf-8 -*-
"""ab_k2（iterk K2）：H1 step144 店对选路表因果 A/B（复用 R24 工具口径·不发射）。

责任口径（任务 K2）：复用 R24 仿真强制路线 A/B 工具（orderbook_r40/ab_r41.py
系）**改接** H1 的 step144 店对选路表（H 件 _router：step144 锁存
_R108_SHOP_ROUTES/_R110_OLD_SHOPS/_V92_TABLE + step648 换 route2）：
- control = H 自有表（h1_base 字节不动）；
- treatment = 邻域替代路线（alt：共享一店店对中非基座路线众数，ab_r41.
  build_alt_table 口径）+ 通用替代臂（generic：覆盖店对最多的基座路线，
  ab_r41.pick_generic_route 口径）——「任何替代臂」判据语义；
- ~60 配对单元（32 seeds × 双席=64 单元；对手轮转 j23.DEFAULT_OPPONENTS 4 件）；
- 判据=是否有任何替代臂净翻胜>0（win_arm−win_control>0；有→该臂候选；
  无→「H 表近最优」复证）。

臂件=尾块覆盖（_IMPL.chassis.router 换实验 router；step144 锁存按臂条件强制，
底 day27 换线保留=只替换 step144 店对表）；**末 callable 语义保持**（尾块出口
归一 _hs_agent）。配对因果口径：路线于 step144 锁存才生效——step144 市场面
为处理前观测，同 seed+seat 跨臂逐位同，臂间 margin 差=纯路线处理效应。

复用（不改写）：ab_r41.build_alt_table/pick_generic_route/_pair_key/
_face_pair_from_sinks/_ab_play_batch/_specs_for/_agg + judge_r23.DEFAULT_OPPONENTS
+ sim_bridge。只写 orderbook_iterk_lab/。
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

from orderbook_r40 import ab_r41 as ab  # noqa: E402  复用件
from orderbook_r40 import judge_r23 as j23  # noqa: E402

RECORD_VERSION = "ab-k2/1.0"
H1_MAIN = MODULE_DIR / "build" / "h1_base" / "main.py"
AB_OUT_DIR = MODULE_DIR / "ab"
EVID_DIR = MODULE_DIR / "evidence"
LEDGER_PATH = EVID_DIR / "ab_k2_ledger_realrun.json"
REVEAL_STEP = 144
N_SEEDS = 32                      # 32 seeds × 双席 = 64 配对单元（~60）
SEED_BASE = 556000                # 实验专属域（R24 550k 域不撞）
WORKERS = 2
ARMS = ("alt", "generic")         # alt=邻域替代（主）；generic=通用替代（副）
BUDGET_CAP = 400

_TAIL = """
# ===== iterk K2 A/B 实验臂 %(mode)s（judge-side only；control 臂无此尾块） =====
_K2_BASE_ROUTER = _IMPL.chassis.router
_K2_MODE = %(mode)r
_K2_ROUTE = %(route)r
_K2_BASE_MAP = dict(%(basemap)s)
_K2_ALT_TABLE = dict(%(alttable)s)


def _k2_router(observation, step, state):
    \"\"\"实验臂：step144 锁存按臂条件强制路线（H1 店对表替换）；底 day27 换线保留。\"\"\"
    r = _K2_BASE_ROUTER(observation, step, state)
    try:
        if int(step) >= %(reveal)d and not state.get('k2_latched'):
            state['k2_latched'] = True
            town = observation.get('town') or {}
            shops = sorted(str(s) for s in
                           list(town.get('unlocked_shops') or [])[:2])
            key = "+".join(shops)
            forced = None
            if _K2_MODE == "const":
                b = _K2_BASE_MAP.get(key)
                if b is not None and int(b) != int(_K2_ROUTE):
                    forced = int(_K2_ROUTE)
            else:
                alt = _K2_ALT_TABLE.get(key)
                if alt is not None:
                    forced = int(alt)
            if forced is not None:
                state['route'] = forced
                r = forced
    except Exception:
        pass
    return r


_IMPL.chassis.router = _k2_router

# ---- 入口归一（末 callable 保持=_hs_agent） ----
_K2_ENTRY_TMP = _hs_agent
del _hs_agent
_hs_agent = _K2_ENTRY_TMP
del _K2_ENTRY_TMP
"""


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def h1_base_route_map() -> dict:
    """H1 step144 店对→路线表（_router 全店对遍历；rkey=None 口径）。"""
    src = H1_MAIN.read_text(encoding="utf-8")
    ns: dict = {}
    exec(compile(src, str(H1_MAIN), "exec"), ns)
    router = ns["_router"]
    pairs = set()
    for tbl in ("_R108_SHOP_ROUTES", "_R110_OLD_SHOPS", "_V92_TABLE"):
        for pair in (ns.get(tbl) or {}):
            pairs.add(tuple(str(s) for s in pair))
    out = {}
    for pair in sorted(pairs):
        obs = {"step": REVEAL_STEP, "player": 0,
               "town": {"unlocked_shops": list(pair)},
               "farms": [{"money": 1000.0}],
               "market": {"inventory": {"WHEAT": 0}}}
        route = router(obs, REVEAL_STEP, {})
        if isinstance(route, int):
            out["+".join(sorted(str(s) for s in pair))] = int(route)
    if not out:
        raise ValueError("H1 店对路线表为空")
    return out


def build_ab_variant_h1(main_text: str, arm: str, alt_table: dict,
                        base_map: dict, arm_route: int = None) -> dict:
    """H1 实验臂件构建（control=原样；alt/generic=尾块覆盖选路）。"""
    if not isinstance(main_text, str) or not main_text.strip():
        raise ValueError("main_text 非法")
    if arm == "control":
        return {"main_text": main_text, "arm": "control",
                "arm_sha": _sha(main_text)}
    if arm not in ARMS:
        raise ValueError("arm 非法: %r" % (arm,))
    if arm == "generic":
        mode, route = "const", int(
            arm_route if arm_route is not None
            else ab.pick_generic_route(base_map))
    else:
        mode, route = "alt", 0
    tail = _TAIL % {"mode": mode, "route": route,
                    "basemap": repr(sorted(base_map.items())),
                    "alttable": repr(sorted((str(k), int(v))
                                            for k, v in alt_table.items())),
                    "reveal": REVEAL_STEP}
    text = main_text + tail
    compile(text, "<ab-k2-%s>" % arm, "exec")
    if tail.count("\ndef ") + tail.startswith("def ") != 1:
        raise ValueError("臂尾块 def 数异常（末 callable 语义保护）")
    return {"main_text": text, "arm": arm, "arm_sha": _sha(text)}


def _check_entry(text: str, arm: str) -> None:
    ns: dict = {}
    exec(compile(text, "<ab-k2-entry:%s>" % arm, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_hs_agent":
        raise RuntimeError("末 callable 归一红 %s: got %r"
                           % (arm, loaded[-1].__name__ if loaded else None))


def run_route_ab_k2(config: dict = None) -> dict:
    """K2 A/B 编排（control+alt+generic，同 seed+seat 配对）。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    n_seeds = int(cfg.get("n_seeds", N_SEEDS))
    seed_base = int(cfg.get("seed_base", SEED_BASE))
    workers = int(cfg.get("workers", WORKERS))
    opponents = list(cfg.get("opponents") or j23.DEFAULT_OPPONENTS)
    opp_paths = [str(rel) if Path(rel).is_file()
                 else str(KSIM_DIR / rel) for rel in opponents]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)

    main_text = H1_MAIN.read_text(encoding="utf-8")
    base_map = h1_base_route_map()
    alt_table = ab.build_alt_table(base_map)
    generic_route = ab.pick_generic_route(base_map)
    AB_OUT_DIR.mkdir(parents=True, exist_ok=True)

    arm_paths = {"control": str(H1_MAIN)}
    for arm in ARMS:
        built = build_ab_variant_h1(
            main_text, arm, alt_table, base_map,
            generic_route if arm == "generic" else None)
        _check_entry(built["main_text"], arm)
        p = AB_OUT_DIR / ("ab_k2_%s_main.py" % arm)
        p.write_text(built["main_text"], encoding="utf-8")
        arm_paths[arm] = str(p)

    # 单元计划：opponent 轮转×seed×双席
    per = max(1, n_seeds // len(opp_paths))
    units = []
    for j, opp_path in enumerate(opp_paths):
        for i in range(per):
            seed = seed_base + j * 1000 + i
            for seat in (0, 1):
                units.append({"seed": seed, "seat": seat,
                              "opp_path": opp_path,
                              "opponent": Path(opp_path).parent.name})
    run_cfg = {"engine": cfg.get("engine", "auto"), "workers": workers}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()

    # phase1：control+trace（face/pair/基线）
    p1_rows = ab._ab_play_batch(
        ab._specs_for(units, "control", arm_paths["control"], True), run_cfg)
    by_key = {(int(r["seed"]), int(r["seat"])): r for r in p1_rows}

    def _applicable(arm, pair):
        if pair is None:
            return False
        if arm == "alt":
            return pair in alt_table
        r = generic_route
        b = base_map.get(pair)
        return b is not None and r is not None and int(b) != int(r)

    # phase2+：各处理臂配对
    arm_rows = {}
    for arm in ARMS:
        t_units = []
        for u in units:
            r1 = by_key.get((u["seed"], u["seat"]))
            if r1 is None or r1.get("error") is not None or \
                    r1.get("margin") is None:
                continue
            if _applicable(arm, r1.get("pair")):
                t_units.append(u)
        rows = ab._ab_play_batch(
            ab._specs_for(t_units, arm, arm_paths[arm], False), run_cfg)
        arm_rows[arm] = {(int(r["seed"]), int(r["seat"])): r for r in rows}

    # 账本：配对单元（ab_r41 口径）
    led_units = []
    for u in units:
        r1 = by_key.get((u["seed"], u["seat"]))
        if r1 is None or r1.get("error") is not None or \
                r1.get("margin") is None:
            continue
        margins = {}
        for arm in ARMS:
            r2 = arm_rows.get(arm, {}).get((u["seed"], u["seat"]))
            margins[arm] = (r2.get("margin") if r2 is not None and
                            r2.get("error") is None else None)
        if all(v is None for v in margins.values()):
            continue
        led_units.append({
            "seed": u["seed"], "seat": u["seat"], "opponent": u["opponent"],
            "face": r1.get("face"), "pair": r1.get("pair"),
            "margin_control": r1["margin"], "margins": margins,
        })

    families = {}
    for lu in led_units:
        fam = lu["face"] or "NONE"
        for arm in ARMS:
            m = lu["margins"].get(arm)
            if m is None:
                continue
            f = families.setdefault(fam, {}).setdefault(
                arm, {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
                      "margin_arm_sum": 0.0, "win_control": 0, "win_arm": 0})
            f["n"] += 1
            f["delta_sum"] += m - lu["margin_control"]
            f["margin_control_sum"] += lu["margin_control"]
            f["margin_arm_sum"] += m
            f["win_control"] += 1 if lu["margin_control"] > 0 else 0
            f["win_arm"] += 1 if m > 0 else 0
    arm_stats = {
        "arm_routes": {"generic": generic_route,
                       "alt": "per-pair neighborhood substitute"},
        "families": {k: {a: ab._agg(v) for a, v in sorted(by_arm.items())}
                     for k, by_arm in sorted(families.items())},
        "overall": {},
        "net_flip_wins": {},
    }
    for arm in ARMS:
        tot = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
               "margin_arm_sum": 0.0, "win_control": 0, "win_arm": 0}
        for by_arm in families.values():
            f = by_arm.get(arm)
            if f:
                for k in tot:
                    tot[k] += f[k]
        arm_stats["overall"][arm] = ab._agg(tot)
        # 净翻胜（R24 口径）：win_arm − win_control（配对单元计数）
        arm_stats["net_flip_wins"][arm] = int(tot["win_arm"]) - int(tot["win_control"])

    # 判据：是否有任何替代臂净翻胜>0
    verdict_arms = [a for a in ARMS if arm_stats["net_flip_wins"][a] > 0]
    verdict = {
        "criterion": "任何替代臂净翻胜>0（win_arm−win_control）",
        "net_flip_wins": dict(arm_stats["net_flip_wins"]),
        "positive_arms": verdict_arms,
        "verdict": ("ALT_ARM_CANDIDATE: %s" % verdict_arms) if verdict_arms
        else "H_TABLE_NEAR_OPTIMAL（复证 R24 口径：无正翻胜格）",
    }

    ledger = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"n_seeds": n_seeds, "seed_base": seed_base,
                   "per_opp": per, "workers": workers, "arms": list(ARMS),
                   "opponents": opp_paths,
                   "main_sha": _sha(main_text),
                   "h1_base_map_n": len(base_map),
                   "generic_route": generic_route,
                   "alt_table_n": len(alt_table)},
        "n_units_planned": len(units),
        "n_units_paired": len(led_units),
        "n_units_treated": {a: sum(1 for lu in led_units
                                   if lu["margins"].get(a) is not None)
                            for a in ARMS},
        "units": led_units,
        "arm_stats": arm_stats,
        "verdict": verdict,
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1)
                           + "\n", encoding="utf-8")
    ledger["ledger_path"] = str(LEDGER_PATH)
    return {"ledger": ledger, "arm_stats": arm_stats, "verdict": verdict}


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    # sim_bridge 认证：复用 judge_k1 认证记录；缺则现跑 30/30。
    auth_path = EVID_DIR / "sim_auth.json"
    bridge = None
    if auth_path.is_file():
        prev = json.loads(auth_path.read_text(encoding="utf-8"))
        if prev.get("consistency_ok"):
            bridge = {"loaded": prev.get("loaded", True),
                      "consistency_ok": True}
    if bridge is None:
        auth_corpus = [556000 + i for i in range(4)] + \
            [2026092901, 2026092902, 2026092903, 2026092904]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")},
            auth_corpus)
        if not auth.get("consistency_ok"):
            print("ABORT: sim_bridge 对照认证未过", flush=True)
            return {"aborted": "sim_bridge 对照认证未过 30/30"}
        auth_path.write_text(json.dumps(
            {k: auth.get(k) for k in
             ("loaded", "consistency", "wall_speedup", "consistency_ok",
              "engine", "timing", "version")},
            ensure_ascii=False, indent=1, default=str) + "\n",
            encoding="utf-8")
        bridge = auth
    res = run_route_ab_k2({
        "n_seeds": N_SEEDS, "seed_base": SEED_BASE, "workers": WORKERS,
        "bridge": bridge, "engine": "auto"})
    print("K2 verdict:", res["verdict"], flush=True)
    return res


if __name__ == "__main__":
    main()
