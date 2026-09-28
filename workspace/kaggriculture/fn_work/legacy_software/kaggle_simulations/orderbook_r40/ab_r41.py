# -*- coding: utf-8 -*-
"""build_ab_variant + run_route_ab_experiments（R24 v2 L1/L2）：路线 A/B 实验。

责任契约（fn_docs/hybrid/responsibility.md【R24 增补 v2】）：
实验臂设计 → build_ab_variant 产各臂实验件 → 配对跑局（phase1 control+
trace 取 face/pair/基线 margin；phase2+ 各臂同 seed+seat 配对）→ 逐单元
记录 {face, pair, margins} → 实验账本落盘（含每臂/每族样本数与效应）；
样本不足→账本先落盘后抛。

【臂口径】时间轴臂（B33 烟测后两轮设计修正，登记 batches.md 变更记录；
安慰剂臂实证强制机制零伤=delta 0.0，邻域臂巨损为真效应）：
  - control：基座店对路线不动（r40 字节恒等）；
  - generic/early/late：**时机常量臂**——分别强制 时机中位（基座表众数线）/
    最早卖货线 / 最晚卖货线（路线=卖货时机变体，实测跨路线加权卖货步
    1927-2045 共 118 步≈5 天谱）；闸门=基座路线≠强制线才生效（同线=零对照）；
  - alt：同店对邻域替代路线（保留臂；烟测证破坏性，默认不跑）。
  臂件=覆盖 `_route40_select`（命中臂条件→强制路线，否则透传底选路）；
  **末 callable 语义保持**（尾块零新增具名 callable），judge-side only。

【配对口径】路线于 step144 锁存才生效——step144 市场面为处理前观测，同
seed+seat 跨臂逐位同，臂间 margin 差=纯路线处理效应（因果对照）。
【假设】面孔（step144 市场面）预测价格轨迹→卖货时机应条件化：热面孔早卖、
冷面孔晚卖；库=face→时机臂 实测效应。
"""
from __future__ import annotations

import ast
import hashlib
import json
import multiprocessing
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_R40_MAIN = MODULE_DIR / "build" / "main.py"
AB_OUT_DIR = MODULE_DIR / "build" / "ab"
REVEAL_STEP = 144

RECORD_VERSION = "ab-r41/3.0"
N_SEEDS_DEFAULT = 160
SEED_BASE_DEFAULT = 550000     # 实验专属域（与 judge 510k/520k 域不撞）
WORKERS_DEFAULT = 16
MIN_PAIRED_DEFAULT = 60        # 配对单元下限（不足→账本落盘后抛）
LEDGER_PATH_DEFAULT = MODULE_DIR / "evidence" / "ab_ledger_realrun.json"
TREATMENT_ARMS = ("generic", "early", "late", "alt")
DEFAULT_ARMS = ("generic", "early", "late")
CONST_ARMS = ("generic", "early", "late")

_TAIL = """
# ===== R24 A/B 实验臂 %(mode)s（judge-side only；control 臂无此尾块） =====
_R41A_BASE = [globals().get("_route40_select")]
_R41A_MODE = %(mode)r
_R41A_ROUTE = %(route)r
_R41A_BASE_MAP = dict(%(basemap)s)
_R41A_ALT_TABLE = dict(%(alttable)s)


def _route40_select(observation, library=None):
    \"\"\"实验臂：step144 起按臂条件强制路线；否则透传底选路（fail-safe）。\"\"\"
    try:
        raw = observation.get("step")
        step = int(raw) if raw is not None else \\
            int(observation.get("day", 0)) * 24 + int(observation.get("hour", 0))
    except Exception:
        step = -1
    if step >= %(reveal)d:
        try:
            town = observation.get("town") or {}
            shops = sorted(str(s) for s in
                           list(town.get("unlocked_shops") or [])[:2])
            key = "+".join(shops)
            if _R41A_MODE == "const":
                b = _R41A_BASE_MAP.get(key)
                if b is not None and int(b) != int(_R41A_ROUTE):
                    return {"route": int(_R41A_ROUTE),
                            "family": "AB_CONST", "confidence": 1.0}
            else:
                alt = _R41A_ALT_TABLE.get(key)
                if alt is not None:
                    return {"route": int(alt), "family": "AB_ALT",
                            "confidence": 1.0}
        except Exception:
            pass
    base = (_R41A_BASE[0] if _R41A_BASE else None)
    if callable(base):
        return base(observation, library)
    return {"route": None, "family": None, "confidence": 0.0}
"""


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ----------------------------------------------------------- 路线表 --

def _base_route_map() -> Dict[str, int]:
    """pair_str（排序归一）→基座路线（_latch_route 全对遍历，rkey=None）。"""
    from orderbook_r40 import route_library as rl  # noqa: WPS433
    latch = rl._load_latch({})
    if latch is None:
        raise ValueError("路由锁存表不可得")
    pairs = set(latch.get("shop_routes") or {}) | \
        set(latch.get("old_shops") or {}) | set(latch.get("v92") or {})
    out: Dict[str, int] = {}
    for pair in sorted(pairs):
        route = rl._latch_route(latch, list(pair), None)
        if isinstance(route, int):
            out["+".join(sorted(str(s) for s in pair))] = int(route)
    if not out:
        raise ValueError("基座路线表为空")
    return out


def pick_generic_route(base_map: Dict[str, int]) -> int:
    """通用路线=覆盖店对最多的基座路线（并列取小 route id）。"""
    counts: Dict[int, int] = {}
    for v in base_map.values():
        counts[int(v)] = counts.get(int(v), 0) + 1
    if not counts:
        raise ValueError("base_map 为空")
    return int(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0])


def route_timing_profiles(main_text: str,
                          base_map: Dict[str, int]) -> Dict[int, float]:
    """各路线卖货时机画像：step144 后 SELL 事件按量加权平均步（值小=早卖）。"""
    from orderbook_r37 import retape_sheep as rs  # noqa: WPS433
    pkg = rs._decode_routes(main_text)
    acts = pkg["actions"]
    out: Dict[int, float] = {}
    for rid in sorted({int(v) for v in base_map.values()}):
        events = pkg["routes"].get(str(rid))
        if not events:
            raise ValueError("路线缺失: %r" % rid)
        num = den = 0.0
        for i in events[REVEAL_STEP:]:
            a = acts[i] if isinstance(i, int) and 0 <= i < len(acts) else None
            if not isinstance(a, dict):
                continue
            for cmd in (a.get("market") or []):
                if isinstance(cmd, list) and len(cmd) >= 3 and \
                        cmd[0] == "SELL":
                    q = float(cmd[2])
                    num += i * q
                    den += q
        out[int(rid)] = round(num / den, 2) if den > 0 else float(i or 0)
    return out


def pick_timing_routes(main_text: str,
                       base_map: Dict[str, int]) -> Dict[str, int]:
    """时机两极：earliest=加权卖货步最小线、latest=最大线（并列取小 route id）。"""
    prof = route_timing_profiles(main_text, base_map)
    if not prof:
        raise ValueError("时机画像为空")
    items = sorted(prof.items(), key=lambda kv: (kv[1], kv[0]))
    return {"early": int(items[0][0]), "late": int(items[-1][0])}


def build_alt_table(base_map: Any = None) -> Dict[str, int]:
    """邻域替代路线表：共享一店的店对中非基座路线众数（并列取小 route id）；
    无邻域→弃样（不出表）。签名意图：输入: 基座表或 None / 输出: {pair_str:
    alt_route} / 错误: 基座表空→抛。
    """
    base = dict(base_map) if base_map is not None else _base_route_map()
    if not isinstance(base, dict) or not base:
        raise ValueError("base_map 须为非空 dict")
    base = {"+".join(sorted(str(s) for s in k.split("+"))): int(v)
            for k, v in base.items()}
    pairs = [tuple(k.split("+")) for k in base]
    out: Dict[str, int] = {}
    for p in pairs:
        key = "+".join(p)
        b = int(base[key])
        votes: Dict[int, int] = {}
        for q in pairs:
            if q == p:
                continue
            if len(set(p) & set(q)) == 1:
                r = int(base["+".join(q)])
                if r != b:
                    votes[r] = votes.get(r, 0) + 1
        if votes:
            out[key] = int(sorted(votes.items(),
                                  key=lambda kv: (-kv[1], kv[0]))[0][0])
    return out


# ----------------------------------------------------------- 臂件构建 --

def build_ab_variant(main_text: str, arm: str, alt_table: Any = None,
                     base_map: Any = None,
                     arm_route: Any = None) -> Dict[str, Any]:
    """实验臂件构建。签名意图：输入: r40 main 文本+臂名（control/generic/
    early/late/alt）+路线表 / 输出: {main_text, arm, arm_sha} / 错误: 构建
    失败即抛。
    """
    if not isinstance(main_text, str) or not main_text.strip():
        raise ValueError("main_text 非法")
    if arm == "control":
        return {"main_text": main_text, "arm": "control",
                "arm_sha": _sha(main_text)}
    if arm not in TREATMENT_ARMS:
        raise ValueError("arm 非法: %r（仅 %s）"
                         % (arm, ("control",) + TREATMENT_ARMS))
    base = dict(base_map) if base_map is not None else _base_route_map()
    base = {"+".join(sorted(str(s) for s in k.split("+"))): int(v)
            for k, v in base.items()}
    alt = dict(alt_table) if alt_table is not None else \
        (build_alt_table(base) if arm == "alt" else {})
    if arm == "alt":
        mode, route = "alt", 0
    else:
        mode = "const"
        if arm_route is not None:
            route = int(arm_route)
        elif arm == "generic":
            route = pick_generic_route(base)
        else:
            route = pick_timing_routes(main_text, base)[arm]
    tail = _TAIL % {"mode": mode, "route": route,
                    "basemap": repr(sorted(base.items())),
                    "alttable": repr(sorted((str(k), int(v))
                                            for k, v in alt.items())),
                    "reveal": REVEAL_STEP}
    text = main_text + tail
    compile(text, "<ab-%s>" % arm, "exec")
    if tail.count("\ndef ") + tail.startswith("def ") != 1:
        raise ValueError("臂尾块 def 数异常（末 callable 语义保护）")
    base_names = [n.name for n in ast.walk(ast.parse(main_text))
                  if isinstance(n, ast.FunctionDef)]
    names = [n.name for n in ast.walk(ast.parse(text))
             if isinstance(n, ast.FunctionDef)]
    if names.count("_route40_select") != \
            base_names.count("_route40_select") + 1:
        raise ValueError("_route40_select 重定义计数异常: %d vs %d"
                         % (names.count("_route40_select"),
                            base_names.count("_route40_select")))
    return {"main_text": text, "arm": arm, "arm_sha": _sha(text)}


# ----------------------------------------------------------- 跑局（并行） --

def _pair_key(obs: Dict[str, Any]) -> Optional[str]:
    """step144 观察→店对键（排序归一，防揭示序不稳漏配；账本记账用）。"""
    town = obs.get("town") or {}
    shops = sorted(str(s) for s in list(town.get("unlocked_shops") or [])[:2])
    return "+".join(shops) if shops else None


def _face_pair_from_sinks(sinks: Any,
                          our_seat: int) -> Tuple[Optional[str], Optional[str]]:
    """追踪槽→(face 签名, 店对键)（step144 帧）。"""
    from orderbook_r40 import fingerprint as fp  # noqa: WPS433
    seat_sink = sinks.get(our_seat) if isinstance(sinks, dict) else None
    for entry in (seat_sink or []):
        if not isinstance(entry, (list, tuple)) or len(entry) < 2:
            continue
        obs = entry[1]
        if not isinstance(obs, dict):
            continue
        try:
            if fp._step_label(obs) != REVEAL_STEP:
                continue
        except Exception:
            continue
        return fp.extract_world_fingerprint(obs), _pair_key(obs)
    return None, None


def _run_ab_chunk(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """worker：一批局跑 run_games（trace 局取 face/pair），红局计入不短路。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games: List[Dict[str, Any]] = []
    metas: List[Tuple[Dict[str, Any], Any]] = []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            agents, sinks = [], None
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, {"build_error":
                                 f"{type(exc).__name__}: {exc}"}))
            continue
        metas.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": []}
    run_rows = list(res.get("games") or [])
    out: List[Dict[str, Any]] = []
    for i, (spec, sinks) in enumerate(metas):
        rr = run_rows[i] if i < len(run_rows) else {}
        row: Dict[str, Any] = {
            "game_id": spec.get("game_id"), "seed": int(spec["seed"]),
            "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
            "opponent": spec.get("opponent"),
            "banks": rr.get("banks"), "error": rr.get("error"),
            "face": None, "pair": None,
        }
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
        if row["error"] is None and isinstance(sinks, dict):
            try:
                face, pair = _face_pair_from_sinks(sinks, row["seat"])
                row["face"], row["pair"] = face, pair
            except Exception as exc:
                row["error"] = f"face 提取异常: {type(exc).__name__}: {exc}"
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - \
                float(banks[1 - row["seat"]])
        else:
            row["margin"] = None
        out.append(row)
    return out


def _ab_play_batch(specs: Sequence[Dict[str, Any]],
                   cfg: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """并行跑口（fork Pool，_play_batch 同构）；红局计入不短路。"""
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS_DEFAULT))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    chunks = [c for c in chunks if c]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks]
    if workers <= 1 or len(tasks) <= 1:
        results = [_run_ab_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            results = pool.map(_run_ab_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    for part in results:
        rows.extend(part)
    return rows


# ----------------------------------------------------------- 实验编排 --

def _specs_for(rows_src: Sequence[Dict[str, Any]], arm: str, cand_path: str,
               trace: bool) -> List[Dict[str, Any]]:
    """局表：同 (seed, seat, opponent) 配对单元转 specs。"""
    specs: List[Dict[str, Any]] = []
    for r in rows_src:
        agents = [{"type": "python", "path": cand_path},
                  {"type": "python", "path": r["opp_path"]}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "ab-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "kind": "ab", "arm": arm,
            "our_seat": int(r["seat"]), "trace": bool(trace),
            "opponent": r.get("opponent"), "agents": agents})
    return specs


def _agg(f: Dict[str, Any]) -> Dict[str, Any]:
    n = max(1, int(f.get("n", 0)))
    return {"n": int(f.get("n", 0)),
            "mean_delta": round(f.get("delta_sum", 0.0) / n, 2),
            "mean_margin_control": round(
                f.get("margin_control_sum", 0.0) / n, 2),
            "mean_margin_arm": round(f.get("margin_arm_sum", 0.0) / n, 2),
            "win_rate_control": round(f.get("win_control", 0) / n, 4),
            "win_rate_arm": round(f.get("win_arm", 0) / n, 4)}


def run_route_ab_experiments(r40_main: Any = None,
                             config: Any = None) -> Dict[str, Any]:
    """路线 A/B 实验编排（control+两处理臂，同 seed+seat 配对）。
    签名意图：输入: r40 main 路径+实验配置 / 输出: {ledger, arm_stats} /
    错误: 臂构建失败或配对样本不足→账本落盘后抛。
    """
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    cfg = dict(config) if isinstance(config, dict) else {}
    main_path = Path(r40_main or cfg.get("r40_main") or DEFAULT_R40_MAIN)
    if not main_path.is_file():
        raise FileNotFoundError("r40 main 不存在: %s" % main_path)
    n_seeds = int(cfg.get("n_seeds", N_SEEDS_DEFAULT))
    seed_base = int(cfg.get("seed_base", SEED_BASE_DEFAULT))
    workers = int(cfg.get("workers", WORKERS_DEFAULT))
    min_paired = int(cfg.get("min_paired", MIN_PAIRED_DEFAULT))
    arms = tuple(cfg.get("arms") or DEFAULT_ARMS)
    for a in arms:
        if a not in TREATMENT_ARMS:
            raise ValueError("臂配置非法: %r" % (a,))
    opponents = list(cfg.get("opponents") or j23.DEFAULT_OPPONENTS)
    opp_paths = [str(rel) if Path(rel).is_file()
                 else str(MODULE_DIR.parent / rel) for rel in opponents]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)
    ledger_path = Path(cfg.get("ledger_path") or LEDGER_PATH_DEFAULT)

    main_text = main_path.read_text(encoding="utf-8")
    base_map = _base_route_map()
    timing = pick_timing_routes(main_text, base_map)
    arm_routes: Dict[str, int] = {"generic": pick_generic_route(base_map),
                                  "early": timing["early"],
                                  "late": timing["late"]}
    alt_table = build_alt_table(base_map)
    AB_OUT_DIR.mkdir(parents=True, exist_ok=True)
    arm_paths: Dict[str, str] = {}
    for arm in arms:
        built = build_ab_variant(main_text, arm, alt_table, base_map,
                                 arm_routes.get(arm))
        p = AB_OUT_DIR / ("ab_%s_main.py" % arm)
        p.write_text(built["main_text"], encoding="utf-8")
        compile(built["main_text"], str(p), "exec")
        arm_paths[arm] = str(p)

    # 单元计划：opponent 轮转×seed×双席
    per = max(1, n_seeds // len(opp_paths))
    units: List[Dict[str, Any]] = []
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
    p1_rows = _ab_play_batch(_specs_for(units, "control", str(main_path),
                                        True), run_cfg)
    by_key = {(int(r["seed"]), int(r["seat"])): r for r in p1_rows}

    def _applicable(arm: str, pair: Optional[str]) -> bool:
        if pair is None:
            return False
        if arm == "alt":
            return pair in alt_table
        r = arm_routes.get(arm)
        b = base_map.get(pair)
        return b is not None and r is not None and int(b) != int(r)

    # phase2+：各处理臂配对
    arm_rows: Dict[str, Dict[Tuple[int, int], Dict[str, Any]]] = {}
    for arm in arms:
        t_units = []
        for u in units:
            r1 = by_key.get((u["seed"], u["seat"]))
            if r1 is None or r1.get("error") is not None or \
                    r1.get("margin") is None:
                continue
            if _applicable(arm, r1.get("pair")):
                t_units.append(u)
        rows = _ab_play_batch(_specs_for(t_units, arm, arm_paths[arm],
                                         False), run_cfg)
        arm_rows[arm] = {(int(r["seed"]), int(r["seat"])): r for r in rows}

    # 账本：配对单元
    led_units: List[Dict[str, Any]] = []
    for u in units:
        r1 = by_key.get((u["seed"], u["seat"]))
        if r1 is None or r1.get("error") is not None or \
                r1.get("margin") is None:
            continue
        margins: Dict[str, Optional[float]] = {}
        for arm in arms:
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

    families: Dict[str, Dict[str, Any]] = {}
    for lu in led_units:
        fam = lu["face"] or "NONE"
        for arm in arms:
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
    arm_stats: Dict[str, Any] = {
        "arm_routes": {a: arm_routes.get(a) for a in arms},
        "families": {k: {a: _agg(v) for a, v in sorted(by_arm.items())}
                     for k, by_arm in sorted(families.items())},
        "overall": {},
    }
    for arm in arms:
        tot = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
               "margin_arm_sum": 0.0, "win_control": 0, "win_arm": 0}
        for by_arm in families.values():
            f = by_arm.get(arm)
            if f:
                for k in tot:
                    tot[k] += f[k]
        arm_stats["overall"][arm] = _agg(tot)

    ledger = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"n_seeds": n_seeds, "seed_base": seed_base,
                   "per_opp": per, "workers": workers, "arms": list(arms),
                   "opponents": opp_paths,
                   "main_sha": _sha(main_text),
                   "arm_routes": {a: arm_routes.get(a) for a in arms},
                   "timing_profiles_minmax": [min(timing.values()),
                                              max(timing.values())],
                   "alt_table_n": len(alt_table)},
        "n_units_planned": len(units),
        "n_units_paired": len(led_units),
        "n_units_treated": {a: sum(1 for lu in led_units
                                   if lu["margins"].get(a) is not None)
                            for a in arms},
        "units": led_units,
        "arm_stats": arm_stats,
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=1)
                           + "\n", encoding="utf-8")
    ledger["ledger_path"] = str(ledger_path)
    n_paired_arm = max((v for v in ledger["n_units_treated"].values()),
                       default=0)
    if n_paired_arm < min_paired:
        raise ValueError("配对样本不足: %d < %d（账本已落盘 %s）"
                         % (n_paired_arm, min_paired, ledger_path))
    return {"ledger": ledger, "arm_stats": arm_stats}
