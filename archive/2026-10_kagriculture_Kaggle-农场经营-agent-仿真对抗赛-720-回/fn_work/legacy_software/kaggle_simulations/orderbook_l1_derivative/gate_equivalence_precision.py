"""gate_equivalence_precision（R10 门③）：等价面+精准性三合一裁决。

(a) 反应面+结果面双判据（2026-09-24 R10 验收③(a) 口径修订，用户裁决 A）：
    replay_action_diff 全量差异枚举（不首异即停）+逐形态分类——允许形态 =
    {BUY_SEED 消失（截断直接效应）/BUY_SEED 出现（基座回买反应）/SELL 单
    序列变化（基座少卖/改卖反应）}，全部差异步 ≥ layer_s_block._CXS_FROM
    同源阈值，且逐局终局资金 l1_final ≥ verbatim_final；原严格逐字节口径
    废止、留档为 identical_mod_seed_drop（(a') RED 诊断面）。
(b) precision_subset_check 子集判据（原样，零误杀可观察裁决）；
(c) constructed_invariant_cases 构造用例三件（原样）。"""
import gzip
import json
import os
import re
import sys
import time

# ---------------------------------------------------------------------------
# 门③(b) 常数（precision_subset_check 用）
# ---------------------------------------------------------------------------
# 我方队名（与 v48_hybrid/gates/lead_protection_gates.py 同口径：回放顶层
# teams / info.TeamNames 里定位我席；INDEX.md"我席"列同源交叉）。
TEAM_NAME = "renyxin"

# SEED 票价（BUY_SEED 单价，品项价估值用）：引擎常数表——kaggle-environments
# 1.32.7 kaggriculture CROPS[*]["seed"]（源 sha256 bc8a5487…；工程内镜像
# orderbook_derivative/main.py SEED_PRICE）。strip 语料的 market.prices 是
# 农产品"卖出价"（不含种子买价），故估值不取 strip、取本常数表。
SEED_PRICE = {
    "WHEAT": 10,
    "CARROT": 20,
    "TOMATO": 50,
    "STRAWBERRY": 100,
    "MELON": 80,
}

# 模式甲判定带（$）：审计基线（fn_docs/hybrid/analyses/09 + 2026-09-23 解剖）
# ——26 局中模式甲 10 局终局剩种 ≈$0-30、模式乙 ~16 局 CARROT×8+WHEAT×4-5
# /局（$200-260）。同带兼作"截断额 ≈0"容差：子集判据下模式甲局截断额天然
# ≤ 未种下额 ≤ 带，故 mode_a_games_near_zero 旗标是防漂移金丝雀（若旗标
# 翻红=模式识别或价值聚合与逐品项判据不自洽，fail-closed 拒绿）。
MODE_A_VALUE_BAND = 30

# ---------------------------------------------------------------------------
# 门③(a) 常数（2026-09-24 口径修订：反应面+结果面双判据）
# ---------------------------------------------------------------------------
# 允许差异形态（反应面）：layer S 纯减法截断的直接效应 + 基座闭环经济反应
# （回买/少卖/改卖）的可观察形态全集；任何其他差异形态（farmer/hands 单位
# 动作变化、非 BUY_SEED 非 SELL 的 market 单变化、动作结构异常、BUY_SEED
# 槽位重排）= violation。步界（全部差异步 ≥ _CXS_FROM 同源阈值）与结果面
# （逐局 l1_final ≥ verbatim_final）在 _adjudicate_game 局级裁决。
ALLOWED_DIVERGENCE_KINDS = (
    "buy_seed_disappear",  # verbatim 有 L1 无（截断直接效应）
    "buy_seed_appear",     # L1 有 verbatim 无（基座回买反应）
    "sell_order_change",   # SELL 单序列（品+量+序）变化（基座少卖/改卖反应）
)

# 步界阈值缓存（layer_s_block._CXS_FROM 同源；None=未装载）
_CXS_FROM_CACHE = None

# strip 语料默认目录（S3 门③ seated 重演最小输入；INDEX.md 登记来源与形态）。
_STRIP_DIR_DEFAULT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..",
    "fn_docs", "hybrid", "results", "replays-r30-26",
))


def _strip_unplanted_seeds(replay_path, seat=None, team_name=TEAM_NAME) -> dict:
    """读单件 strip 终局态 → {seat, seeds}：原局终局我方未种下种子（逐品项）。

    字段路径（2026-09-23 实读确认）：steps[-1] 的 seat0 槽携带共享最小观测
    （INDEX.md strip 形态：steps[t>=1] seat0={action+共享观测}），其
    observation.private 为**双席** private 列表，private[seat].seeds 即该席
    终局持有种子（= 未种下量：种子唯一去向是 PLANT 消耗）。与顶层
    final.private[seat].seeds 交叉核对，不一致=语料损坏 → ValueError。
    seat 缺省由 teams（回退 info.TeamNames）中 team_name 判；给定 seat 时与
    teams 交叉，不一致 → ValueError（fail-closed，防席位错读导致误判）。
    仅归一化五个种子品项（SEED_PRICE 键序），缺项补 0。
    """
    path = os.path.abspath(replay_path)
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as fh:
        replay = json.load(fh)
    names = replay.get("teams") or (replay.get("info") or {}).get("TeamNames") or []
    if team_name in names:
        resolved = names.index(team_name)
        if seat is None:
            seat = resolved
        elif seat != resolved:
            raise ValueError(
                f"seat cross-check failed: given {seat} != teams[{team_name!r}]"
                f" index {resolved} ({path})")
    elif seat is None:
        raise ValueError(
            f"team {team_name!r} not in replay teams {names!r} ({path})")
    steps = replay.get("steps") or []
    if not steps:
        raise ValueError(f"replay has no steps ({path})")
    obs = ((steps[-1] or [{}])[0] or {}).get("observation") or {}
    priv = obs.get("private")
    if not (isinstance(priv, list) and len(priv) > seat
            and isinstance(priv[seat], dict)):
        raise ValueError(
            f"final shared obs private[{seat}] missing/ill-typed ({path})")
    raw = priv[seat].get("seeds") or {}
    seeds = {crop: int(raw.get(crop) or 0) for crop in SEED_PRICE}
    fpriv = (replay.get("final") or {}).get("private")
    if isinstance(fpriv, list) and len(fpriv) > seat and isinstance(fpriv[seat], dict):
        fraw = fpriv[seat].get("seeds") or {}
        for crop in SEED_PRICE:
            if int(fraw.get(crop) or 0) != seeds[crop]:
                raise ValueError(
                    f"final.private vs last-step shared private mismatch on"
                    f" {crop}: {fraw.get(crop)} != {seeds[crop]} ({path})")
    return {"seat": seat, "seeds": seeds}


def _resolve_strip_path(product, strip_dir) -> str:
    """从 replay_action_diff 产物取回放件路径：显式路径键优先，缺省按局号
    拼语料目录 episode-<ep>-strip.json.gz；两者皆缺/文件不存在即抛（→ 该局
    error，fail-closed）。"""
    for key in ("replay_path", "replay"):
        cand = product.get(key)
        if cand:
            return cand
    ep = product.get("episode")
    if ep is None:
        raise ValueError("product has neither replay path nor episode number")
    path = os.path.join(strip_dir, f"episode-{ep}-strip.json.gz")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"strip replay not found: {path}")
    return path


def precision_subset_check(replay_products, strip_dir=None) -> dict:
    """逐局逐品项：被截断购种量 ≤ 原版终局未种下量；violation 非空即门红。

    输入 replay_products = replay_action_diff 产物列表（同包接口，逐局
    {episode, seat, game_pass, divergences, identical_mod_seed_drop,
    dropped:[{step,crop,qty}…], l1_final, verbatim_final, replay 路径或
    episode 号, …}——本判据消费面=dropped/episode/seat/error/replay 定位，
    2026-09-24 口径修订只增键不删改）。子集语义（零误杀
    的可观察裁决）：layer S 只删"原局终局也没种下"的 BUY_SEED 单——逐局逐
    品项 dropped 汇总 ≤ 原局该品项终局未种下数；多删一颗=误杀=violation。
    原局终局未种下量取 strip 语料终局态（_strip_unplanted_seeds；产物内
    verbatim_final 形态属上游未定桩，不消费）。

    返回 {all_ok, per_game, per_crop, violations, errors, summary}：
    - per_game：逐局 {episode, seat, crops:{品项:{dropped,unplanted,ok}},
      dropped_value, unplanted_value, mode_a, ok}；error 局记 {episode,error}。
    - per_crop：五品项跨局汇总 {dropped, unplanted, ok}。
    - violations：[{episode, crop, dropped, unplanted}]。
    - errors：[{episode, error}]——上游重演失败或终局态读取失败；非空即
      all_ok=False（fail-closed：不因局缺失而静默放过）。
    - summary：{total_dropped_value_est（SEED 票价估值）, mode_a_games_near_zero,
      n_games, n_mode_a, n_violations, n_errors}。空输入=error（防空转绿灯）。
    """
    strip_dir = os.path.normpath(strip_dir or _STRIP_DIR_DEFAULT)
    products = list(replay_products or [])
    per_game, violations, errors = [], [], []
    per_crop = {c: {"dropped": 0, "unplanted": 0} for c in SEED_PRICE}
    mode_a_eps, total_dropped_value = [], 0
    if not products:
        errors.append({"episode": None,
                       "error": "replay_products is empty (fail-closed)"})
    for product in products:
        ep = product.get("episode")
        try:
            if product.get("error") is not None:
                raise ValueError(f"upstream replay failed: {product['error']!r}")
            dropped_agg = {}
            for entry in product.get("dropped") or []:
                crop, qty = entry.get("crop"), entry.get("qty")
                if crop not in SEED_PRICE:
                    raise ValueError(f"dropped entry unknown crop {crop!r}")
                if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
                    raise ValueError(f"dropped entry bad qty {qty!r} for {crop}")
                dropped_agg[crop] = dropped_agg.get(crop, 0) + qty
            unplanted = _strip_unplanted_seeds(
                _resolve_strip_path(product, strip_dir),
                seat=product.get("seat"))["seeds"]
            crops, game_ok, dropped_value, unplanted_value = {}, True, 0, 0
            for crop in SEED_PRICE:
                d, u = dropped_agg.get(crop, 0), unplanted[crop]
                ok = d <= u
                game_ok = game_ok and ok
                crops[crop] = {"dropped": d, "unplanted": u, "ok": ok}
                if not ok:
                    violations.append({"episode": ep, "crop": crop,
                                       "dropped": d, "unplanted": u})
                per_crop[crop]["dropped"] += d
                per_crop[crop]["unplanted"] += u
                dropped_value += d * SEED_PRICE[crop]
                unplanted_value += u * SEED_PRICE[crop]
            mode_a = unplanted_value <= MODE_A_VALUE_BAND
            if mode_a:
                mode_a_eps.append(ep)
            total_dropped_value += dropped_value
            per_game.append({"episode": ep, "seat": product.get("seat"),
                             "crops": crops, "dropped_value": dropped_value,
                             "unplanted_value": unplanted_value,
                             "mode_a": mode_a, "ok": game_ok})
        except Exception as exc:  # 单局失败=该局 error（fail-closed，不静默放过）
            errors.append({"episode": ep,
                           "error": f"{type(exc).__name__}: {exc}"})
            per_game.append({"episode": ep,
                             "error": f"{type(exc).__name__}: {exc}"})
    for meta in per_crop.values():
        meta["ok"] = meta["dropped"] <= meta["unplanted"]
    mode_a_near_zero = all(
        g["dropped_value"] <= MODE_A_VALUE_BAND
        for g in per_game if g.get("mode_a"))
    return {
        "all_ok": (not violations) and (not errors) and mode_a_near_zero,
        "per_game": per_game,
        "per_crop": per_crop,
        "violations": violations,
        "errors": errors,
        "summary": {
            "total_dropped_value_est": total_dropped_value,
            "mode_a_games_near_zero": mode_a_near_zero,
            "n_games": len(products),
            "n_mode_a": len(mode_a_eps),
            "mode_a_episodes": mode_a_eps,
            "n_violations": len(violations),
            "n_errors": len(errors),
        },
    }


# ---------------------------------------------------------------------------
# run 内部件（本叶私有，非责任面）
# ---------------------------------------------------------------------------
_EPISODE_NAME_RE = re.compile(r"episode-(\d+)-strip\.json\.gz")


def _cxs_from() -> int:
    """步界阈值：与 layer_s_block._CXS_FROM 同源（gate_launch_fourgate_l1
    ._truncation_only_diff 同款 import），不手拼 648 防两处漂移。进程内缓存；
    装载失败向上抛（→ 该局 error，fail-closed：步界是契约级判据，缺源即红）。"""
    global _CXS_FROM_CACHE
    if _CXS_FROM_CACHE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        if here not in sys.path:
            sys.path.append(here)
        import layer_s_block
        _CXS_FROM_CACHE = int(layer_s_block._CXS_FROM)
    return _CXS_FROM_CACHE


def _episode_from_path(path):
    """文件名 → 局号（int；非语料命名回退 basename 字符串）。"""
    match = _EPISODE_NAME_RE.fullmatch(os.path.basename(path))
    return int(match.group(1)) if match else os.path.basename(path)


def _discover_replays(episodes_dir, limit=None):
    """语料目录 → 回放件绝对路径列表：episode-<num>-strip.json.gz 按局号
    数值升序；limit 非 None 截前 N 局（真小子集冒烟用，全量局数不硬编码
    ——按目录 glob 自然支持子集：喂只含部分语料的目录即可）。目录不存在/
    非目录抛 OSError（→ run 侧折成全局面 error，fail-closed）。"""
    path = os.path.abspath(episodes_dir)
    if not os.path.isdir(path):
        raise NotADirectoryError(f"episodes_dir 不是目录: {path}")
    found = []
    for name in os.listdir(path):
        match = _EPISODE_NAME_RE.fullmatch(name)
        if match:
            found.append((int(match.group(1)), os.path.join(path, name)))
    found.sort(key=lambda item: item[0])
    paths = [p for _, p in found]
    if limit is not None:
        paths = paths[:max(int(limit), 0)]
    return paths


def _aggregate_verdict(products, subset_result, cases_result) -> dict:
    """(a)(b)(c) 三面汇总裁决（纯函数；合成产物裁决矩阵单测直接喂）。

    equiv = 全部局 game_pass 真且无任一 error（2026-09-24 双判据口径：局级
    裁决由 _adjudicate_game(divergences, l1_final, verbatim_final) 从产物面
    重算——单一真值源，与 replay_action_diff 产物自带 game_pass 同源一致；
    error 局 game_pass 记 False 并计 n_errors——fail-closed 不放宽，语料
    缺失/装载失败/重演异常同进 error 面，按契约严格裁决）；subset =
    subset_result.all_ok；
    cases = cases_result.all_pass；passed = 三者全真。per_game_summary 逐局
    一行：episode/seat/error/game_pass/identical_mod_seed_drop（(a') RED 诊断
    面，原样留档）/n_divergences/kind_counts/n_violations/first_divergence/
    n_dropped/dropped_value_est/l1_final/verbatim_final/final_delta/
    min_divergence_step/steps_boundary_ok/result_face_ok（error 局数值面记
    None/0）。"""
    products = list(products or [])
    per_game_summary, n_errors, n_game_pass = [], 0, 0
    for product in products:
        error = product.get("error")
        error = None if error is None else str(error)
        dropped = (product.get("dropped") or []) if error is None else []
        divergences = ((product.get("divergences") or [])
                       if error is None else [])
        try:
            dropped_value = sum(int(entry["qty"]) * SEED_PRICE[entry["crop"]]
                                for entry in dropped)
        except (KeyError, TypeError, ValueError):
            dropped_value = None  # 产物畸形：不崩编排面，数值面记 None
        l1_final = product.get("l1_final") if error is None else None
        vb_final = product.get("verbatim_final") if error is None else None
        final_delta = (l1_final - vb_final) if (
            isinstance(l1_final, (int, float))
            and isinstance(vb_final, (int, float))) else None
        if error is not None:
            n_errors += 1
            verdict = {"game_pass": False, "first_divergence": None,
                       "n_violations": 0, "steps_boundary_ok": None,
                       "result_face_ok": None, "min_divergence_step": None}
            kind_counts = {}
        else:
            verdict = _adjudicate_game(divergences, l1_final, vb_final)
            kind_counts = {}
            for entry in divergences:
                kind_counts[entry.get("kind")] = (
                    kind_counts.get(entry.get("kind"), 0) + 1)
        if verdict["game_pass"]:
            n_game_pass += 1
        per_game_summary.append({
            "episode": product.get("episode"),
            "seat": product.get("seat"),
            "error": error,
            "game_pass": verdict["game_pass"],
            "identical_mod_seed_drop": (
                False if error is not None else product.get(
                    "identical_mod_seed_drop")),
            "n_divergences": len(divergences),
            "kind_counts": kind_counts,
            "n_violations": verdict["n_violations"],
            "first_divergence": verdict["first_divergence"],
            "n_dropped": len(dropped),
            "dropped_value_est": dropped_value,
            "l1_final": l1_final,
            "verbatim_final": vb_final,
            "final_delta": final_delta,
            "min_divergence_step": verdict["min_divergence_step"],
            "steps_boundary_ok": verdict["steps_boundary_ok"],
            "result_face_ok": verdict["result_face_ok"],
        })
    equiv = bool(products) and n_errors == 0 and n_game_pass == len(products)
    subset = bool(subset_result.get("all_ok"))
    cases = bool(cases_result.get("all_pass"))
    return {
        "equiv": equiv,
        "subset": subset,
        "cases": cases,
        "passed": bool(equiv and subset and cases),
        "per_game_summary": per_game_summary,
        "n_errors": n_errors,
    }


def run(episodes_dir, l1_main, verbatim_main, limit=None,
        evidence_path=None) -> dict:
    """(a)重演双判据 (b)子集判据 (c)构造用例 →{equiv, subset, cases}；任一红即门红。

    编排（门③ L1）：① episodes_dir 内 episode-<num>-strip.json.gz 按局号
    升序逐局 replay_action_diff（limit 截前 N 局供小子集冒烟，全量局数不
    硬编码；两 callable 装载一次跨局复用，不逐局重装载——1MB 级 main 每
    局重装载会把 26 局拖到分钟级）；② 全产物喂 precision_subset_check；
    ③ constructed_invariant_cases()；④ _aggregate_verdict 汇总：equiv =
    全部局 game_pass（2026-09-24 反应面+结果面双判据：无 violation 形态 ∧
    全部差异步 ≥ _CXS_FROM 同源阈值 ∧ 逐局 l1_final ≥ verbatim_final）且
    无任一 error（任一局 error → equiv=False 并计 n_errors——fail-closed，
    语料缺失/装载失败/重演异常同进 error 面，按契约严格裁决不放宽）；门③
    passed = equiv ∧ subset（precision_subset_check.all_ok）∧ cases
    （all_pass）。

    evidence 落 <本包>/evidence/equivalence_evidence.json（evidence_path
    可覆写，供测试 tmp 隔离防覆写真台账）：per_game 逐局全产物（不截断，
    含 divergences 全量差异枚举与 game_pass 局裁决）+ subset/cases 全结果 +
    verdict + 输入登记 + 耗时。语料目录空/坏 → 单条全局面 error 产物
    （equiv/subset 俱红，防空转绿灯）。
    返回 {equiv, subset, cases, passed, per_game_summary, n_errors,
    evidence_path}。"""
    t0 = time.perf_counter()
    replays, discovery_note = [], None
    try:
        replays = _discover_replays(episodes_dir, limit)
    except OSError as exc:
        discovery_note = f"{type(exc).__name__}: {exc}"
    products = []
    if not replays:
        reason = discovery_note or (
            f"episodes_dir 无 episode-*-strip.json.gz 语料: "
            f"{os.path.abspath(episodes_dir)}")
        products.append({"episode": None, "error": f"语料发现失败: {reason}"})
    load_error = None
    if replays:
        try:
            l1_fn = _as_callable(l1_main)
            vb_fn = _as_callable(verbatim_main)
        except Exception as exc:
            load_error = f"装载/语料失败: {type(exc).__name__}: {exc}"
    for path in replays:
        if load_error is not None:  # 装载失败：逐局记 error（fail-closed 留痕）
            products.append({"episode": _episode_from_path(path),
                             "error": load_error})
            continue
        try:
            products.append(replay_action_diff(path, l1_fn, vb_fn))
        except Exception as exc:  # 叶内已自包 error；此处兜底防编排面逃逸
            products.append({"episode": _episode_from_path(path),
                             "error": f"{type(exc).__name__}: {exc}"})
    subset_result = precision_subset_check(products)
    try:
        cases_result = constructed_invariant_cases()
    except Exception as exc:  # import/夹具面逃逸 → cases 红（fail-closed）
        cases_result = {"all_pass": False,
                        "error": f"{type(exc).__name__}: {exc}"}
    aggregate = _aggregate_verdict(products, subset_result, cases_result)
    target = os.path.abspath(evidence_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "evidence",
        "equivalence_evidence.json"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    summary_rows = aggregate["per_game_summary"]
    evidence = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        # 1.1（2026-09-24）：③(a) 双判据口径——per_game 增 divergences 全量
        # 枚举/game_pass 局裁决；equiv_detail 改 n_game_pass/n_violation_games。
        "protocol": "orderbook-l1-equivalence-precision/1.1",
        "inputs": {
            "episodes_dir": os.path.abspath(episodes_dir),
            "n_replays": len(replays),
            "replays": [os.path.basename(p) for p in replays],
            "limit": limit,
            "l1_main": l1_main if isinstance(l1_main, str) else "<callable>",
            "verbatim_main": (verbatim_main if isinstance(verbatim_main, str)
                              else "<callable>"),
        },
        "equiv_detail": {
            "n_games": len(products),
            "n_game_pass": sum(1 for row in summary_rows
                               if row["game_pass"]),
            "n_divergent_games": sum(1 for row in summary_rows
                                     if row["n_divergences"] > 0),
            "n_violation_games": sum(1 for row in summary_rows
                                     if row["n_violations"] > 0),
            "n_errors": aggregate["n_errors"],
            "criteria": {
                "allowed_kinds": list(ALLOWED_DIVERGENCE_KINDS),
                "step_boundary": {"threshold": _cxs_from(),
                                  "source": "layer_s_block._CXS_FROM"},
                "result_face": "l1_final >= verbatim_final per game",
            },
        },
        "subset": subset_result,
        "cases": cases_result,
        "verdict": {
            "equiv": aggregate["equiv"],
            "subset": aggregate["subset"],
            "cases": aggregate["cases"],
            "passed": aggregate["passed"],
        },
        "per_game": products,  # 逐局全产物（divergences 全量），保留不截断
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    aggregate["evidence_path"] = target
    return aggregate


# ---------------------------------------------------------------------------
# replay_action_diff 内部件（本叶私有，非责任面）
# ---------------------------------------------------------------------------
_TWIN_MODULE = None


def _twin():
    """惰性导入 planner/twin（legacy_software 入 sys.path 自举；进程内缓存）。"""
    global _TWIN_MODULE
    if _TWIN_MODULE is None:
        software = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", ".."))
        if software not in sys.path:
            sys.path.insert(0, software)
        import kaggle_simulations.agent.planner.twin as twin
        _TWIN_MODULE = twin
    return _TWIN_MODULE


def _load_strip_replay(replay_path):
    """读 strip 语料（gzip 魔数识别 .json.gz，普通 .json 直读）。"""
    with open(replay_path, "rb") as handle:
        magic = handle.read(2)
    if magic == b"\x1f\x8b":
        with gzip.open(replay_path, "rt", encoding="utf-8") as handle:
            return json.load(handle)
    with open(replay_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _my_seat(replay):
    """局内我方席位：顶层 teams（缺则 info.TeamNames）里 TEAM_NAME 下标；
    不可判即抛（勿假设 seat0）。"""
    names = list(replay.get("teams")
                 or (replay.get("info") or {}).get("TeamNames") or [])
    if TEAM_NAME not in names:
        raise ValueError(f"teams 里找不到我方 {TEAM_NAME!r}: {names!r}")
    return names.index(TEAM_NAME)


def _load_last_callable(main_path):
    """按官方语义装载提交 callable：复刻 vendored kaggle_environments
    agent.get_last_callable（compile(path) -> exec_dir 进 sys.path -> 空 env
    exec -> pop -> 取 env 最后一个 callable）。

    刻意不用 kgenv.arena.load_submission_agent：它优先返回名为 `agent`
    的符号——本两 main 的 `agent` 是层链中途的 CL 包装器（L6616），官方
    入口是尾部 last-callable（verbatim=_cxd_agent / L1=_cxs_agent），用
    它会漏掉末端数层（对 L1 即漏掉 layer S 本身，门禁变空转）。"""
    path = os.path.abspath(main_path)
    with open(path, "r", encoding="utf-8") as handle:
        src = handle.read()
    env = {}
    exec_dir = os.path.dirname(path)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, path, "exec"), env)
    finally:
        sys.path.pop()
    callables = [v for v in env.values() if callable(v)]
    if not callables:
        raise ValueError(f"{path} 装载后无 callable")
    return callables[-1]


def _as_callable(agent_or_path):
    """l1_main/verbatim_main 接受 main.py 路径或已装载 callable（差异
    注入测试直接喂假 callable 用；路径走官方 last-callable 装载）。"""
    if callable(agent_or_path):
        return agent_or_path
    return _load_last_callable(agent_or_path)


def _obs_dict(state, seat):
    """twin 席位观测 -> 提交 callable 可读纯 dict（v48plus_ab_gate
    ._twin_obs_dict 同款）。step 取 obs0——孪生只维护 seat0.step（线上
    双席皆有）；remainingOverageTime 缺省 60.0（两基座均不读此字段，
    2026-09-23 grep 复核）。"""
    obs0 = state.seats[0].observation
    mine = state.seats[seat].observation
    return {
        "farms": obs0.farms,
        "market": obs0.market,
        "town": obs0.town,
        "day": mine.day,
        "hour": mine.hour,
        "step": obs0.step,
        "player": seat,
        "private": mine.private,
        "remainingOverageTime": 60.0,
    }


def _seated_replay(replay, me, agent_fn, recorded):
    """席位正确 seated 重演（scripts/v143_sellrace_gates
    .rollout_with_replay_opponent_seated 同款）：对手席逐字重放 recorded
    动作流，我席 agent_fn(_obs_dict) 实驱，twin.step 逐步推进。
    返回 {stream, taken, final, first_exception, done}；agent 调用异常记
    first_exception=(step, repr) 并停（=行为面差异）；引擎步进/状态构建
    异常向上抛（=重演失败，fail-closed error）。"""
    twin = _twin()
    bundle = twin.load_engine()
    state = twin.build_state_from_replay(replay, 0, bundle)
    stream, first_exception, taken = [], None, 0
    while not state.env.done and taken < len(recorded):
        obs = _obs_dict(state, me)
        try:
            mine = agent_fn(obs)
        except Exception as exc:  # agent 异常属行为面（first_divergence）
            first_exception = (taken, f"{type(exc).__name__}: {exc}")
            break
        pair = [recorded[taken][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        stream.append(mine)
        taken += 1
    return {"stream": stream, "taken": taken,
            "final": twin.final_money(state),
            "first_exception": first_exception,
            "done": bool(state.env.done)}


def _canonical(value):
    """逐字节比较的规范化串（p41_official_load_probe.norm_action 同源
    口径：sort_keys+紧凑分隔符，元组/列表同形）。"""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _is_buy_seed(order):
    return (isinstance(order, (list, tuple)) and len(order) >= 3
            and order[0] == "BUY_SEED")


def _is_sell(order):
    return (isinstance(order, (list, tuple)) and order
            and order[0] == "SELL")


def _trunc(text, limit=200):
    text = str(text)
    return text if len(text) <= limit else text[:limit] + "..."


def _market_partition(market):
    """market 订单表（list）→ (buy_seed, sell, other) 三保序分卷。

    语料实测（2026-09-23 26 局统计）：market 单型 = BUY_SEED/SELL/HIRE/
    BUY_ANIMAL/BUY_PRODUCT/BUY_LAND/空槽；前两型入专属卷做形态判定，其余
    一律入 other 卷（任何增删改=violation，2026-09-24 口径：非 BUY_SEED 非
    SELL 的 market 单变化不在允许形态内）。"""
    buy_seed, sells, others = [], [], []
    for order in market:
        if _is_buy_seed(order):
            buy_seed.append(order)
        elif _is_sell(order):
            sells.append(order)
        else:
            others.append(order)
    return buy_seed, sells, others


def _multiset_minus(left, right):
    """left 侧有而 right 侧匹配不上的订单（canonical 多重集差，保 left 序；
    right 同名单逐个消耗）。BUY_SEED 改量单自然分解为 消失+出现 两形态。"""
    remaining = [_canonical(order) for order in right]
    unmatched = []
    for order in left:
        key = _canonical(order)
        try:
            remaining.remove(key)
        except ValueError:
            unmatched.append(order)
    return unmatched


def _seed_order_meta(order):
    """BUY_SEED 订单 → (crop, qty)；结构异常（qty 非可整数化等）→ None
    （调用方按 violation 市场结构异常处置，fail-closed）。"""
    try:
        return str(order[1]), int(order[2])
    except (TypeError, ValueError, IndexError):
        return None


def _classify_divergence(expected, got):
    """一步差异的全量形态分类（2026-09-24 反应面口径；不再首异即停）。

    返回该步全部差异记录列表 [{kind, detail, crop?, qty?}]（BUY_SEED 形态
    附结构化 crop/qty）：
    - 允许形态（ALLOWED_DIVERGENCE_KINDS）：buy_seed_disappear（verbatim
      有 L1 无，截断直接效应）/buy_seed_appear（L1 有 verbatim 无，基座
      回买反应）——多重集差逐单一条，改量单自然分解为消失+出现两条；
      sell_order_change（该步双方 market 里 SELL 单序列——品+量+序——任何
      差，基座少卖/改卖反应）——一步至多一条。BUY_SEED 差异与 SELL 差异
      同步出现拆多条 kind。
    - violation 形态（其他一切，不为过门放宽）：action_shape（非 dict）/
      action_keys（键集差）/<非 market 字段名>（farmer/hands 等单位动作
      变化）/market（非 BUY_SEED 非 SELL 订单增删改、market 非订单表、
      BUY_SEED 订单结构异常、BUY_SEED 槽位重排等不可归因差异）。
    本函数仅在两动作 canonical 不等时被调；分类零记录（如纯 BUY_SEED 重排
    ——多重集同而序变）→ fail-closed 记 violation market，不放过不可归因差。"""
    if not isinstance(expected, dict) or not isinstance(got, dict):
        return [{"kind": "action_shape", "detail": (
            f"exp={_trunc(_canonical(expected))} got={_trunc(_canonical(got))}")}]
    if set(expected) != set(got):
        return [{"kind": "action_keys", "detail": (
            f"exp_keys={sorted(expected)} got_keys={sorted(got)}")}]
    records = []
    for key in sorted(expected):
        if key == "market":
            continue
        if _canonical(expected[key]) != _canonical(got[key]):
            records.append({"kind": key, "detail": (
                f"exp={_trunc(_canonical(expected[key]))} "
                f"got={_trunc(_canonical(got[key]))}")})
    em, gm = expected.get("market"), got.get("market")
    if _canonical(em) != _canonical(gm):
        if not isinstance(em, list) or not isinstance(gm, list):
            records.append({"kind": "market", "detail": (
                f"market 非订单表: exp={_trunc(_canonical(em))} "
                f"got={_trunc(_canonical(gm))}")})
        else:
            e_bs, e_sell, e_other = _market_partition(em)
            g_bs, g_sell, g_other = _market_partition(gm)
            if _canonical(e_other) != _canonical(g_other):
                records.append({"kind": "market", "detail": (
                    "非 BUY_SEED/SELL 订单差异: "
                    f"exp={_trunc(_canonical(e_other), 120)} "
                    f"got={_trunc(_canonical(g_other), 120)}")})
            for order in _multiset_minus(e_bs, g_bs):
                meta = _seed_order_meta(order)
                if meta is None:
                    records.append({"kind": "market", "detail": (
                        "BUY_SEED 订单结构异常: "
                        f"{_trunc(_canonical(order), 120)}")})
                    continue
                records.append({
                    "kind": "buy_seed_disappear",
                    "crop": meta[0], "qty": meta[1],
                    "detail": f"{_trunc(_canonical(order), 120)}"
                              "（verbatim 有 L1 无）"})
            for order in _multiset_minus(g_bs, e_bs):
                meta = _seed_order_meta(order)
                if meta is None:
                    records.append({"kind": "market", "detail": (
                        "BUY_SEED 订单结构异常: "
                        f"{_trunc(_canonical(order), 120)}")})
                    continue
                records.append({
                    "kind": "buy_seed_appear",
                    "crop": meta[0], "qty": meta[1],
                    "detail": f"{_trunc(_canonical(order), 120)}"
                              "（L1 有 verbatim 无，基座回买反应）"})
            if _canonical(e_sell) != _canonical(g_sell):
                records.append({"kind": "sell_order_change", "detail": (
                    f"exp={_trunc(_canonical(e_sell), 160)} "
                    f"got={_trunc(_canonical(g_sell), 160)}")})
    if not records:
        records.append({"kind": "market", "detail": (
            "差异不可归入允许形态（如 BUY_SEED 槽位重排）: "
            f"exp={_trunc(_canonical(em), 120)} "
            f"got={_trunc(_canonical(gm), 120)}")})
    return records


def _adjudicate_game(divergences, l1_final, verbatim_final):
    """局级双判据裁决（纯函数，2026-09-24 口径）：

    game_pass = 反应面（无 violation 形态差异记录）∧ 步界（全部差异步 ≥
    layer_s_block._CXS_FROM 同源阈值）∧ 结果面（l1_final ≥ verbatim_final，
    1e-9 容差吸收浮点噪声）。first_divergence = 首个取消格差异（violation
    形态，或步界破缺的早差异——定位用；纯结果面破缺无步可指，记 None，
    final_delta 面自见）。返回 {game_pass, first_divergence, n_violations,
    n_divergences, steps_boundary_ok, result_face_ok, min_divergence_step,
    threshold}。l1/verbatim final 缺失或不可数值化 → 结果面 False
    （fail-closed）。"""
    threshold = _cxs_from()
    divergences = list(divergences or [])
    n_violations = sum(1 for entry in divergences
                       if entry.get("kind") not in ALLOWED_DIVERGENCE_KINDS)
    steps = [int(entry["step"]) for entry in divergences]
    steps_boundary_ok = all(step >= threshold for step in steps)
    try:
        result_face_ok = (float(l1_final) - float(verbatim_final)) >= -1e-9
    except (TypeError, ValueError):
        result_face_ok = False
    first = next((entry for entry in divergences
                  if entry.get("kind") not in ALLOWED_DIVERGENCE_KINDS
                  or int(entry["step"]) < threshold), None)
    return {
        "game_pass": (n_violations == 0 and steps_boundary_ok
                      and result_face_ok),
        "first_divergence": first,
        "n_violations": n_violations,
        "n_divergences": len(divergences),
        "steps_boundary_ok": steps_boundary_ok,
        "result_face_ok": result_face_ok,
        "min_divergence_step": min(steps) if steps else None,
        "threshold": threshold,
    }


def replay_action_diff(replay_path, l1_main, verbatim_main) -> dict:
    """单局 seated 重演 diff：全量差异枚举+形态分类+双判据局裁决。

    语义：按局内我方席位（strip teams/info.TeamNames 判，勿假设 seat0），
    对手席逐字重放原动作流，我席由 L1 callable 实驱（twin 逐步喂我席
    观测）；L1 实发动作流 vs 原局 verbatim 记录动作流（strip 我席 action
    流）逐步对齐比较。verbatim callable 同局自重演作保真对照——不自
    逐字节复现即孪生保真破、L1 差异不可归因 → error（fail-closed）。
    裁决（2026-09-24 R10 验收③(a) 口径修订，反应面+结果面双判据）：
    (a1) 全量枚举——不首异即停，逐差异步收集全部差异记录 divergences=
         [{step, kind, detail, crop?, qty?}…]（kind 见 _classify_divergence：
         允许={buy_seed_disappear, buy_seed_appear, sell_order_change}，
         其他=violation）；
    (a2) 步界——全部差异步 ≥ layer_s_block._CXS_FROM 同源阈值；
    (a3) 结果面——l1_final ≥ verbatim_final；
    game_pass = (a1)无 violation ∧ (a2) ∧ (a3)。first_divergence=首个
    取消格差异（violation 形态或步界破缺，定位用；纯结果面破缺记 None）。
    dropped=[{step, crop, qty}…] 语义不变（BUY_SEED 消失逐单汇总，
    precision_subset_check 消费面兼容）；identical_mod_seed_drop=(a')
    原严格逐字节口径留档的 RED 诊断面（全部差异恰为纯 BUY_SEED 消失才
    真，门禁不消费）。(c) 装载/语料/状态构建/重演异常 → {error: …}
    （上游 fail-closed 处置）。
    l1_main/verbatim_main 接受 main.py 路径或已装载 callable（路径按
    官方 last-callable 语义装载）。
    返回 {episode, seat, game_pass, divergences, n_divergences,
    n_violations, steps_boundary_ok, result_face_ok, min_divergence_step,
    identical_mod_seed_drop, dropped, first_divergence, l1_final,
    verbatim_final, steps_compared, replay_path}（steps_compared=已比较
    步数=全流长，全量枚举不提前停；l1/verbatim_final=各自重演终局我席
    资金；replay_path 供 precision_subset_check 回定位语料件）。"""
    try:
        replay = _load_strip_replay(replay_path)
        me = _my_seat(replay)
        recorded = _twin().replay_transition_actions(replay)
        if not recorded:
            raise ValueError("replay 无转移动作流")
        l1_fn = _as_callable(l1_main)
        vb_fn = _as_callable(verbatim_main)
    except Exception as exc:
        return {"error": f"装载/语料失败: {type(exc).__name__}: {exc}"}
    try:
        control = _seated_replay(replay, me, vb_fn, recorded)
    except Exception as exc:
        return {"error": f"verbatim 对照重演失败: {type(exc).__name__}: {exc}"}
    if control["first_exception"] is not None:
        return {"error": "verbatim 自重演 agent 异常（孪生保真破）: "
                f"step={control['first_exception'][0]} "
                f"{control['first_exception'][1]}"}
    for t, got in enumerate(control["stream"]):
        if _canonical(got) != _canonical(recorded[t][me]):
            return {"error": "verbatim 自重演不复现原局记录（孪生保真破，"
                    f"L1 差异不可归因）: 首个不一致 t={t}"}
    try:
        l1 = _seated_replay(replay, me, l1_fn, recorded)
    except Exception as exc:
        return {"error": f"L1 重演失败: {type(exc).__name__}: {exc}"}
    divergences, dropped = [], []
    for t, got_action in enumerate(l1["stream"]):
        expected = recorded[t][me]
        if _canonical(got_action) == _canonical(expected):
            continue
        for record in _classify_divergence(expected, got_action):
            entry = {"step": t, "kind": record["kind"],
                     "detail": record["detail"]}
            if "crop" in record:
                entry["crop"] = record["crop"]
            if "qty" in record:
                entry["qty"] = record["qty"]
            divergences.append(entry)
            if record["kind"] == "buy_seed_disappear":
                dropped.append({"step": t, "crop": record["crop"],
                                "qty": record["qty"]})
    if l1["first_exception"] is not None:  # agent 异常=行为面 violation
        step, detail = l1["first_exception"]
        divergences.append({"step": step, "kind": "agent_exception",
                            "detail": detail})
    verdict = _adjudicate_game(divergences, l1["final"][me],
                               control["final"][me])
    episode = (replay.get("episode_id")
               or (replay.get("info") or {}).get("EpisodeId")
               or os.path.splitext(os.path.basename(replay_path))[0])
    return {
        "episode": episode,
        "seat": me,
        "game_pass": verdict["game_pass"],
        "divergences": divergences,
        "n_divergences": verdict["n_divergences"],
        "n_violations": verdict["n_violations"],
        "steps_boundary_ok": verdict["steps_boundary_ok"],
        "result_face_ok": verdict["result_face_ok"],
        "min_divergence_step": verdict["min_divergence_step"],
        "identical_mod_seed_drop": all(
            entry["kind"] == "buy_seed_disappear"
            for entry in divergences),  # (a') 原严格口径留档（RED 诊断面）
        "dropped": dropped,
        "first_divergence": verdict["first_divergence"],
        "l1_final": l1["final"][me],
        "verbatim_final": control["final"][me],
        "steps_compared": len(l1["stream"]),
        "replay_path": os.path.abspath(replay_path),
    }


def constructed_invariant_cases() -> dict:
    """三构造用例：有机会不截/无机会截/s671 边界磁带确无后续种植才截。

    门③(c) 的可编程裁决面（verify_layer_s_gates 汇总用）：不重写夹具，复用
    test_layer_s 的构造夹具函数（同目录 import，不复制第二份逻辑——测试真值
    仍在 test_layer_s.test_invariant_cases，防漂移）。惰性 import：本门模块
    不在非裁决路径强依赖测试模块。夹具异常=该例失败（不向上传播，门级
    fail 语义由 all_pass=False 承载）。
    返回 {"c1_no_trunc_when_future_plant": {"pass", "evidence"},
    "c2_trunc_when_no_opportunity": {...}, "c3_s671_boundary": {"truncate_side",
    "keep_side", "pass"}, "all_pass": bool}。
    """
    import test_layer_s as tls

    def _verdict(case):
        ok = case["got"] == case["expected"]
        detail = case["evidence"] if ok else (
            f'{case["evidence"]}; FAIL got={case["got"]!r} expected={case["expected"]!r}')
        return {"pass": ok, "evidence": detail}

    def _adjudicate(fixture):
        # 单例夹具裁决；夹具异常=该例失败（evidence 记异常，不向上传播——
        # 门级红由 all_pass=False 承载）。
        try:
            return _verdict(fixture())
        except Exception as exc:
            return {"pass": False, "evidence": f"fixture raised {type(exc).__name__}: {exc}"}

    c1 = _adjudicate(tls._invariant_case_c1_no_trunc_when_future_plant)
    c2 = _adjudicate(tls._invariant_case_c2_trunc_when_no_opportunity)
    try:
        sides = tls._invariant_case_c3_s671_boundary()
        c3_trunc = _verdict(sides["truncate_side"])
        c3_keep = _verdict(sides["keep_side"])
    except Exception as exc:  # 双面夹具共享一次调用：异常=双面俱败
        evidence = f"fixture raised {type(exc).__name__}: {exc}"
        c3_trunc = {"pass": False, "evidence": evidence}
        c3_keep = {"pass": False, "evidence": evidence}
    return {
        "c1_no_trunc_when_future_plant": c1,
        "c2_trunc_when_no_opportunity": c2,
        "c3_s671_boundary": {
            "truncate_side": c3_trunc,
            "keep_side": c3_keep,
            "pass": c3_trunc["pass"] and c3_keep["pass"],
        },
        "all_pass": c1["pass"] and c2["pass"] and c3_trunc["pass"] and c3_keep["pass"],
    }
