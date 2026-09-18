# 【中文】planner_offline_bench.py —— DTSP 离线基准 harness（Track-B P2）
# ===========================================================================
# 用途（track-B 文档 §6 P2 离线裁决）：在官方回放（round20/21/22 + cmp-v92，
# references/data/online-replays/）的中局注入点上，对比三条轨迹的终局资金：
#   A) history 真值    —— 回放 rewards[me_seat]
#   B) twin 重演核验   —— P1 孪生按官方动作流重演（|B-A| = twin_noise）
#   C) 反应式基线      —— v13.8 源码 exec 装载（与 main.py 同语义）在孪生内
#                         驱动我方席、对手=回放真实动作（import 不可行时降级
#                         为"回放我方真实动作重放"代理并显式标注口径）
#   D) DTSP 规划器     —— enumerate_plans × Ω 对手模型投影打分 → 鲁棒选择
#                         → 选中计划的旋钮覆盖注入 v13.8 命名空间 → 同孪生
#                         同对手 rollout
# 判据（m7 修订双口径，2026-09-19——首轮"逐局 ≥history 且 ≥反应式"诚实
#   FAIL 1/14 后修订：执行器代差不应记到计划头上）：
#   主口径：逐局中位注入点 DTSP ≥ 反应式（同执行器单变量），≥9/14 局不劣
#     且全集合 mean Δ(DTSP−反应式)>0；
#   参考口径：DTSP 对 history 减执行器代差 offset（=同注入点反应式对
#     history）后 ≥9/14 局不劣。
#   败因归因逐局输出 twin_noise / opponent_model_gap / plan_space_gap
#   （归因用 oracle 重演：将投影排序 top-K 候选各按真实对手 rollout 一次，
#   若存在候选显著胜过选中者则 opponent_model_gap，否则 plan_space_gap）。
# 公平性口径：C 与 D 共享同一孪生与同一对手（回放真实动作）；对手模型 Ω
#   只作用于 D 的计划选择（J 矩阵），不改变轨迹对手——单变量对比。
# CLI：
#   --mode official  >=12 局 × >=3 注入步，全过 exit 0，有败 exit 1
#   --mode smoke     >=3 局 × 1 注入步快跑（harness 摇通；报告仍含判据行）
#   缺 twin（P1 未合流）→ exit 2 + 明确原因（不算 crash，P1 合流后复跑）
# 纪律：stdlib-only、全离线（不发任何网络请求）、确定性（排序显式键）；
#   输出只落 software/exports/probes/planner_bench/。
# 可测性：evaluate_injection 及其依赖组 deps 全部键注入——单测用 mini-stub
#   伪 twin 即可覆盖注入/对比/归因逻辑（真 twin 集成测试见
#   tests/test_planner_contract.py 的 skip-unless-importable 段）。
# ===========================================================================

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
AGENT_DIR = os.path.join(SOFTWARE, "kaggle_simulations", "agent")
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

# ---- late-bound twin import（模块顶部 try-import；缺 twin 在 main 里
#      exit 2 并打印明确原因——不算 crash，P1 合流后由协调者复跑）----
TWIN_IMPORT_ERROR = None
try:
    from kaggle_simulations.agent.planner import twin  # noqa: E402
    from kaggle_simulations.agent.planner import plans  # noqa: E402
    from kaggle_simulations.agent.planner import opponents  # noqa: E402
    from kaggle_simulations.agent.planner import select  # noqa: E402
except Exception as _exc:                                   # noqa: BLE001
    TWIN_IMPORT_ERROR = f"{type(_exc).__name__}: {_exc}"

DEFAULT_REPLAY_ROOT = os.path.join(
    SOFTWARE, "..", "references", "data", "online-replays")
OFFICIAL_ROUNDS = ("round20", "round21", "round22", "cmp-v92")
SMOKE_ROUNDS = ("round20",)
OFFICIAL_INJECTION_DAYS = (3, 10, 20)
SMOKE_INJECTION_DAYS = (10,)
ORACLE_TOP_K = 6            # 败因归因 oracle 重演的候选数（含选中者）
GATE_EPS = 1.0              # 终局资金比较容差（float 噪声）
TWIN_NOISE_EPS = 1.0        # 孪生重演 vs 真值的逐位一致容差
V13_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                    "mission", "solver", "executor", "market", "entry")
CROP_NAMES = ("STRAWBERRY", "WHEAT", "MELON", "CARROT", "TOMATO")
ANIMAL_NAMES = ("GOOSE", "COW", "SHEEP")


# --------------------------------------------------------------------------
# 纯函数（tests/test_planner_contract.py 直接覆盖的逻辑件）
# --------------------------------------------------------------------------
def select_injection_steps(n_steps, days):
    """注入步 = 各 dawn（day×24）；钳到可回放范围、去重升序。"""
    if n_steps < 2:
        raise ValueError(
            f"n_steps={n_steps!r} 太小，无法注入"
            f"（示例：720 步回放应传 len(steps)）")
    upper = n_steps - 2            # 留至少 1 步可 rollout
    return sorted({min(int(d) * 24, upper) for d in days if int(d) >= 0})


def compute_town_demand(shops, unlocked_shops, sell_interval=4,
                        towncenter_products=()):
    """城镇期望日吸收（引擎 §4 语义镜像，factsheet kaggriculture.py:736-747）：
    每 sell_interval 步每家已解锁商店各抽 1 件产品（单一产品店抽 2 件）、
    抽取在该店产品列表上均匀分布；镇中心每 24 步各抽 1 件非肥料品。
    返回 {item: 期望件/日}。"""
    demand = {}
    per_day = 24.0 / float(sell_interval)
    for shop in sorted(set(unlocked_shops or [])):
        products = (shops or {}).get(shop)
        if not products:
            continue
        draws = per_day * (2.0 if len(products) == 1 else 1.0)
        share = draws / float(len(products))
        for item in products:
            demand[item] = demand.get(item, 0.0) + share
    for item in towncenter_products or ():
        if item == "FERTILIZER":
            continue
        demand[item] = demand.get(item, 0.0) + 1.0
    return demand


def _seat_entry(step_entry, seat):
    """回放 steps[t] 的席位条目防御式读取（官方格式=list 按席索引；
    兼容 dict 按字符串键的变体）。"""
    if isinstance(step_entry, list):
        return step_entry[seat] or {}
    if isinstance(step_entry, dict):
        return step_entry.get(str(seat)) or step_entry.get(seat) or {}
    return {}


def extract_opponent_history(replay, opp_seat, up_to_step):
    """对手逐日已观测动作史（回放 steps[1..up_to_step] 的 opp 席 market）。

    返回 [{"day": d, "sells": {item: qty}, "animal_buys": n}, ...]
    （按日聚合、days 升序；口径：steps[t+1].action 驱动 t→t+1 转移，
    记账在 t//24 日——与 twin.replay_transition_actions 同一解读）。"""
    steps = replay.get("steps") or []
    per_day = {}
    for t in range(0, min(int(up_to_step), max(0, len(steps) - 1))):
        entry = _seat_entry(steps[t + 1], int(opp_seat))
        action = entry.get("action") or {}
        day = t // 24
        bucket = per_day.setdefault(day, {"sells": {}, "animal_buys": 0})
        for order in action.get("market") or []:
            if not isinstance(order, list) or not order:
                continue
            op = order[0]
            if op == "SELL" and len(order) >= 3:
                item, qty = order[1], int(order[2])
                bucket["sells"][item] = bucket["sells"].get(item, 0) + qty
            elif op == "BUY_ANIMAL" and len(order) >= 3:
                bucket["animal_buys"] += int(order[2])
    return [{"day": d, "sells": per_day[d]["sells"],
             "animal_buys": per_day[d]["animal_buys"]}
            for d in sorted(per_day)]


def attribute_failure(twin_noise, truth, reactive, dtsp, oracle_best,
                      oracle_key, dtsp_key, eps=GATE_EPS):
    """败因归因（判据失败时逐局输出；字段恒在、布尔值）。

    顺序：twin_noise 优先（孪生重演不逐位 => 其他 delta 不可信）；
    其次 oracle 重演若存在非选中候选显著胜过选中者且越过 reactive =>
    opponent_model_gap（对手模型误导排序）；否则 plan_space_gap
    （枚举面上没有计划能在真执行器上胜出/被选中者已是面内最优）。"""
    fail_d = (dtsp < truth - eps) or (dtsp < reactive - eps)
    result = {"judge_fail": fail_d, "twin_noise": False,
              "opponent_model_gap": False, "plan_space_gap": False,
              "reason": ""}
    if not fail_d:
        result["reason"] = "pass"
        return result
    if float(twin_noise) > TWIN_NOISE_EPS:
        result["twin_noise"] = True
        result["reason"] = (f"twin 重演偏差 {twin_noise:.1f} > "
                            f"{TWIN_NOISE_EPS}，孪生口径不可信")
        return result
    if oracle_best is not None and oracle_key != dtsp_key \
            and oracle_best > dtsp + eps and oracle_best > reactive + eps:
        result["opponent_model_gap"] = True
        result["reason"] = (f"oracle 候选 {oracle_key} 终局 {oracle_best:.0f}"
                            f" > 选中 {dtsp_key} {dtsp:.0f}：对手模型误导排序")
        return result
    result["plan_space_gap"] = True
    result["reason"] = ("枚举面内无候选在真执行器上显著越过选中者/反应式"
                        f"（oracle_best={oracle_best}）")
    return result


def apply_knob_overrides(ns, overrides):
    """把 plan_to_knob_overrides 的映射打进 v13.8 命名空间（返回
    (applied, skipped)；PLANNER_LOCAL.*/PACK 为规划器本地/信息性键，
    按缺口清单口径跳过；"PLANNER_OVERRIDES.<键>" 点路径写入 constants
    的惰性旋钮寄存器（P2.5），"PLANNER_ENABLED" 置真后才生效——旗关
    通道恒回默认值，行为与 v13.8 逐字节等价）。"""
    applied, skipped = [], []
    for key in sorted(overrides):
        value = overrides[key]
        if key.startswith("PLANNER_LOCAL.") or key == "PACK":
            skipped.append((key, "planner-local/信息性（缺口清单口径）"))
            continue
        if "." in key:
            base, leaf = key.split(".", 1)
            container = ns.get(base)
            if not isinstance(container, dict):
                skipped.append((key, f"命名空间无 dict 容器 {base!r}"))
                continue
            if leaf.isdigit() and int(leaf) in container:
                container[int(leaf)] = value       # LAND_PLAN 用整数键
            else:
                container[leaf] = value
            applied.append(key)
            continue
        if key not in ns:
            skipped.append((key, "命名空间无此旋钮"))
            continue
        ns[key] = value
        applied.append(key)
    return applied, skipped


def build_v13_namespace(overrides=None):
    """按 main.py 同语义把 src/ 九模块 exec 进全新扁平命名空间，再应用
    旋钮覆盖（覆盖发生在 exec 之后：参数包 dict 内容逐字段替换，语义与
    测试侧 main.<KNOB> patch 契约一致；逐 rollout 全新装载防跨局串态）。"""
    if not os.path.isfile(os.path.join(AGENT_DIR, "src", "constants.py")):
        raise FileNotFoundError(f"现役 src/ 不存在: {AGENT_DIR}")
    ns = {}
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), ns)      # 与 main.py IMPORT_BLOCK 对齐
    for mod in V13_MODULE_ORDER:
        path = os.path.join(AGENT_DIR, "src", mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        exec(compile(source, path, "exec"), ns)
    if overrides:
        applied, skipped = apply_knob_overrides(ns, overrides)
    else:
        applied, skipped = [], []
    return ns, applied, skipped


def find_episodes(replay_root, rounds, limit, team):
    """确定性枚举可评局（rounds 固定序 × 目录内文件名排序；team 不在场
    的局带原因跳过）。返回 (evaluable, skipped)。"""
    evaluable, skipped = [], []
    for rnd in rounds:
        pattern = os.path.join(replay_root, rnd, "episode-*.json")
        for path in sorted(glob.glob(pattern)):
            episode_id = os.path.splitext(os.path.basename(path))[0]
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    info = (json.load(handle).get("info") or {})
            except (OSError, ValueError) as exc:
                skipped.append({"episode": episode_id,
                                "reason": f"回放不可读: {exc}"})
                continue
            teams = list(info.get("TeamNames") or [])
            seats = [i for i, t in enumerate(teams) if t == team]
            if not seats:
                skipped.append({"episode": episode_id,
                                "reason": f"{team} 不在场 {teams}"})
                continue
            evaluable.append({"episode": episode_id, "path": path,
                              "round": rnd, "me_seat": seats[0],
                              "mirror": len(seats) > 1,
                              "opponent": teams[1 - seats[0]]
                              if len(teams) == 2 else "?"})
            if len(evaluable) >= limit:
                return evaluable, skipped
    return evaluable, skipped


# --------------------------------------------------------------------------
# 孪生依赖组（真 twin 工厂 / 测试 mini-stub 同一形状）
#   deps 键契约：
#     build(replay, step) -> state            从回放重建注入态
#     transition_actions(replay) -> [a0,a1]   官方动作流（acts[i] 驱动 i→i+1）
#     run_to_end(state, actions) -> state     按动作流推进至终局
#     step(state, [a0, a1]) -> state          单步推进（原地）
#     final(state) -> [float, float]          双席终局资金
#     shops / towncenter                      引擎商店表（吸收计算）
#     v13_available: bool                     src/ 可装载与否
#     v13_factory(overrides|None) -> (agent_fn, applied, skipped)
# --------------------------------------------------------------------------


def make_twin_deps():
    """真孪生 + 真 v13.8 依赖组。"""
    bundle = twin.load_engine()
    module = bundle.module

    def v13_factory(overrides=None):
        ns, applied, skipped = build_v13_namespace(overrides)
        return ns["agent"], applied, skipped

    return {
        "build": twin.build_state_from_replay,
        "transition_actions": twin.replay_transition_actions,
        "run_to_end": twin.run_to_end,
        "step": twin.step,
        "final": twin.final_money,
        "shops": dict(getattr(module, "SHOPS", {}) or {}),
        "towncenter": tuple(getattr(module, "TOWN_CENTER_PRODUCTS", ())
                            or ()),
        "v13_available": os.path.isfile(
            os.path.join(AGENT_DIR, "src", "constants.py")),
        "v13_factory": v13_factory,
    }


def rollout_with_replay_opponent(deps, state, me_seat, agent_fn,
                                 opp_actions, start_step):
    """我方席 = agent_fn(obs)、对手席 = 回放动作，推进至终局。

    返回 (final_money_list, steps_taken)。公平性：C/D 两口径共用本函数
    （对手侧逐动作为回放真实动作——单变量对比口径，见模块头）。"""
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    while not state.env.done and start_step + taken < len(opp_actions) \
            and taken < max_steps:
        obs = state.seats[int(me_seat)].observation
        mine = agent_fn(obs) if agent_fn is not None else None
        theirs = opp_actions[start_step + taken][1 - int(me_seat)]
        deps["step"](state, [mine, theirs])
        taken += 1
    return deps["final"](state), taken


def scan_farm(farm):
    """公开农场 dict → (crops, herd, money, n_quadrants)。

    tile 语义（回放 schema 实测 2026-09-19）：None=空格；"LOCKED"=锁定；
    dict 含 crop=作物名 / animal=畜名 / kind=WEED|PASTURE|COOP...。"""
    crops = {name: 0 for name in CROP_NAMES}
    herd = 0
    for row in farm.get("tiles") or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            crop = tile.get("crop")
            if crop in crops:
                crops[crop] += 1
            if tile.get("animal") in ANIMAL_NAMES:
                herd += 1
    money = float(farm.get("money", 0) or 0)
    quads = len(farm.get("unlocked_quadrants") or ()) or 1
    return crops, herd, money, int(quads)


def build_obs_summary_from_state(deps, state, me_seat, day):
    """孪生态 → obs_summary（plans.build_obs_summary 键契约）。"""
    obs0 = state.seats[0].observation
    farms = obs0.farms
    market = obs0.market
    prices = dict(market.get("prices") or {}) if isinstance(market, dict) \
        else dict(getattr(market, "prices", {}) or {})
    town = obs0.town
    unlocked = list(town.get("unlocked_shops") or []) \
        if isinstance(town, dict) else \
        list(getattr(town, "unlocked_shops", None) or [])
    demand = compute_town_demand(deps["shops"], unlocked,
                                 towncenter_products=deps["towncenter"])
    mine_crops, mine_herd, mine_money, quads = scan_farm(farms[me_seat])
    opp_crops, opp_herd, opp_money, _ = scan_farm(farms[1 - me_seat])
    opp_class = plans.classify_opponent_opening(day, opp_herd, opp_crops)
    return plans.build_obs_summary(
        day=day, money=mine_money, herd=mine_herd, crops=mine_crops,
        unlocked_quadrants=quads, prices=prices, daily_demand=demand,
        opponent={"herd": opp_herd, "crops": opp_crops, "money": opp_money},
        opp_class=opp_class)


# --------------------------------------------------------------------------
# 单注入点评估
# --------------------------------------------------------------------------


def evaluate_injection(deps, replay, me_seat, inj_step, cfg):
    """单注入点评估：真值/孪生核验/反应式/DTSP 四口径 + 败因归因。

    返回行 dict（bench_report 的 rows 成员）。"""
    day = inj_step // 24
    acts = deps["transition_actions"](replay)
    truth = [float(x) for x in replay.get("rewards") or [0.0, 0.0]]

    # B) 孪生按官方动作流重演核验（twin_noise）
    state_b = deps["build"](replay, inj_step)
    deps["run_to_end"](state_b, acts[inj_step:])
    twin_final = deps["final"](state_b)
    twin_noise = abs(float(twin_final[me_seat]) - truth[me_seat])

    # 局况摘要 + 对手史 + Ω 模型 + 计划枚举与投影打分
    state_p = deps["build"](replay, inj_step)
    obs_summary = build_obs_summary_from_state(deps, state_p, me_seat, day)
    opp_seat = 1 - me_seat
    history = extract_opponent_history(replay, opp_seat, inj_step)
    models = opponents.build_default_models(
        history=history, profile_path=cfg.get("profile_path"),
        pessimistic=cfg.get("pessimistic"))
    model_notes = [m.describe() for m in models]
    candidate_plans = plans.enumerate_plans(obs_summary)
    if not candidate_plans:
        raise RuntimeError(
            f"enumerate_plans 返回空集（day={day}）")
    j_matrix = {}
    for spec in candidate_plans:
        scores = {}
        for model in models:
            scores[model.name] = plans.project_season(
                spec, obs_summary, model.supply_pressure(obs_summary))
        j_matrix[spec.key()] = scores
    selection = select.robust_select(
        j_matrix, strategy=cfg.get("strategy", "trimmed_mean"),
        weights=cfg.get("weights"),
        trim_fraction=cfg.get("trim_fraction",
                              select.DEFAULT_TRIM_FRACTION))
    best_key = selection["best"]
    best_spec = _spec_by_key(candidate_plans, best_key)

    # C) 反应式基线（v13.8 原样；对手=回放真实动作）
    reactive_final, reactive_proxy, _reactive_skipped = _run_configured(
        deps, replay, me_seat, inj_step, acts, None)

    # D) DTSP：选中计划的旋钮覆盖 → 同孪生同对手
    overrides = plans.plan_to_knob_overrides(best_spec)
    dtsp_final, _, dtsp_skipped = _run_configured(
        deps, replay, me_seat, inj_step, acts, overrides)

    # 败因归因（判据失败且孪生可信才花 oracle 预算）
    oracle_best, oracle_key = None, None
    attribution = attribute_failure(
        twin_noise, truth[me_seat], reactive_final[me_seat],
        dtsp_final[me_seat], oracle_best, oracle_key, best_key)
    if attribution["judge_fail"] and not attribution["twin_noise"] \
            and cfg.get("oracle", True):
        oracle_best, oracle_key = _oracle_rerun(
            deps, replay, me_seat, inj_step, acts, candidate_plans,
            selection, best_key, top_k=cfg.get("oracle_top_k",
                                               ORACLE_TOP_K))
        attribution = attribute_failure(
            twin_noise, truth[me_seat], reactive_final[me_seat],
            dtsp_final[me_seat], oracle_best, oracle_key, best_key)

    return {
        "episode": cfg.get("episode"), "step": inj_step, "day": day,
        "me_seat": me_seat,
        "truth_me": truth[me_seat],
        "twin_resim_me": float(twin_final[me_seat]),
        "twin_noise": twin_noise,
        "reactive_me": float(reactive_final[me_seat]),
        "dtsp_me": float(dtsp_final[me_seat]),
        "dtsp_vs_history": float(dtsp_final[me_seat]) - truth[me_seat],
        "dtsp_vs_reactive": float(dtsp_final[me_seat])
        - float(reactive_final[me_seat]),
        "reactive_proxy": reactive_proxy,
        "best_plan": best_key, "n_plans": len(candidate_plans),
        "plan_ranking_top3": [k for k, _ in selection["ranking"][:3]],
        "tie_break": selection["tie_break"],
        "opponent_models": model_notes,
        "overrides_skipped": dtsp_skipped,
        "oracle_best": oracle_best, "oracle_key": oracle_key,
        "judge_fail": attribution["judge_fail"],
        "twin_noise_flag": attribution["twin_noise"],
        "opponent_model_gap": attribution["opponent_model_gap"],
        "plan_space_gap": attribution["plan_space_gap"],
        "attribution_reason": attribution["reason"],
    }


def _spec_by_key(candidate_plans, key):
    for spec in candidate_plans:
        if spec.key() == key:
            return spec
    raise RuntimeError(f"排序键 {key!r} 不在候选集"
                       f"（示例：{candidate_plans[0].key()} 在集内）")


def _run_configured(deps, replay, me_seat, inj_step, acts, overrides):
    """v13.8（可选旋钮覆盖）在孪生内驱动我方席、对手=回放动作。

    src/ 装载失败 → 降级"回放我方真实动作重放"代理（显式标注口径，
    track-B §6 P2 允许的过渡口径；此时 C/D 与 B 同轨迹，报告照实写）。"""
    if not deps.get("v13_available", True):
        state = deps["build"](replay, inj_step)
        deps["run_to_end"](state, acts[inj_step:])
        return deps["final"](state), True, []
    try:
        agent_fn, _applied, skipped = deps["v13_factory"](overrides)
    except Exception as exc:                             # noqa: BLE001
        sys.stderr.write(f"[warn] v13.8 装载失败，降级回放代理: {exc}\n")
        state = deps["build"](replay, inj_step)
        deps["run_to_end"](state, acts[inj_step:])
        return deps["final"](state), True, []
    state = deps["build"](replay, inj_step)
    final, _taken = rollout_with_replay_opponent(
        deps, state, me_seat, agent_fn, acts, inj_step)
    return final, False, skipped


def _oracle_rerun(deps, replay, me_seat, inj_step, acts, candidate_plans,
                  selection, best_key, top_k):
    """败因归因 oracle：投影排序 top-K 候选各按真实对手 rollout 一次。"""
    top = [k for k, _ in selection["ranking"][:max(1, int(top_k))]]
    if best_key not in top:
        top = [best_key] + top[:max(0, int(top_k) - 1)]
    best_final, best_name = None, None
    for key in top:
        spec = _spec_by_key(candidate_plans, key)
        final, _, _ = _run_configured(
            deps, replay, me_seat, inj_step, acts,
            plans.plan_to_knob_overrides(spec))
        me = float(final[me_seat])
        if best_final is None or me > best_final:
            best_final, best_name = me, key
    return best_final, best_name


# --------------------------------------------------------------------------
# CLI 主流程
# --------------------------------------------------------------------------


def main(argv=None):
    # twin 缺失检查必须在 argparse 之前：--strategy 的 choices 引用
    # select.*，twin 未合流的机器上 select 未导入，先走 exit 2 干净退出。
    if TWIN_IMPORT_ERROR is not None:
        sys.stderr.write(
            "[exit 2] P1 孪生不可用，无法构建注入状态：\n  "
            f"{TWIN_IMPORT_ERROR}\n"
            "  原因：planner.twin 缺失或其 vendored 引擎指纹校验失败；\n"
            "  处置：等 P1 合流（software/kaggle_simulations/agent/planner/"
            "twin.py）后复跑。本退出码不算 crash。\n")
        return 2

    parser = argparse.ArgumentParser(
        description="DTSP 离线基准（history/反应式/DTSP 三口径终局资金对比）")
    parser.add_argument("--mode", choices=("official", "smoke"),
                        default="smoke")
    parser.add_argument("--replay-root", default=DEFAULT_REPLAY_ROOT)
    parser.add_argument("--team", default="renyxin")
    parser.add_argument("--rounds", default=None,
                        help="逗号分隔（缺省 official=round20,round21,"
                             "round22,cmp-v92；smoke=round20）")
    parser.add_argument("--injection-days", default=None,
                        help="逗号分隔（缺省 official=3,10,20；smoke=10）")
    parser.add_argument("--limit", type=int, default=None,
                        help="局数上限（缺省 official=14、smoke=3）")
    parser.add_argument("--strategy", default="trimmed_mean",
                        choices=tuple(select.AGGREGATION_STRATEGIES))
    parser.add_argument("--trim-fraction", type=float, default=None,
                        help="trimmed_mean 裁尾比例（缺省=select.DEFAULT_"
                             "TRIM_FRACTION；仅 trimmed_mean 消费）")
    parser.add_argument("--pessimistic-discount", type=float, default=0.75,
                        help="PessimisticFill 成交价折扣（0,1]；Ω 其余模型"
                             "不受影响（P2.6 选参轴）")
    parser.add_argument("--weights-preset", default="none",
                        choices=("none", "pessimistic_half"),
                        help="weighted 策略的权重预设：pessimistic_half="
                             "悲观模型半权、其余等权（P2.6 选参轴）")
    parser.add_argument("--out-dir",
                        default=os.path.join(SOFTWARE, "exports", "probes",
                                             "planner_bench"))
    parser.add_argument("--no-oracle", action="store_true",
                        help="判据失败时不跑 oracle 重演（快跑）")
    args = parser.parse_args(argv)

    official = args.mode == "official"
    trim_fraction = (args.trim_fraction if args.trim_fraction is not None
                     else select.DEFAULT_TRIM_FRACTION)
    weights = None
    if args.weights_preset == "pessimistic_half":
        weights = {"passive_extrapolation": 1.0,
                   "frozen_style_pool:winner_balanced": 1.0,
                   "frozen_style_pool:wheat_suppressor": 1.0,
                   "pessimistic_fill": 0.5}
    rounds = (tuple(args.rounds.split(",")) if args.rounds
              else (OFFICIAL_ROUNDS if official else SMOKE_ROUNDS))
    days = ([int(x) for x in args.injection_days.split(",")]
            if args.injection_days
            else list(OFFICIAL_INJECTION_DAYS if official
                      else SMOKE_INJECTION_DAYS))
    limit = args.limit if args.limit is not None else (14 if official else 3)
    min_episodes = 12 if official else 3
    if official and len(days) < 3:
        sys.stderr.write("[exit 2] official 模式要求 >=3 个注入步"
                         f"（当前 {days}）\n")
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    t_start = time.time()
    deps = make_twin_deps()

    evaluable, skipped = find_episodes(args.replay_root, rounds, limit,
                                       args.team)
    rows = []
    episode_rows = []
    for ep in evaluable:
        with open(ep["path"], "r", encoding="utf-8") as handle:
            replay = json.load(handle)
        n_steps = len(replay.get("steps") or [])
        inj_steps = select_injection_steps(n_steps, days)
        if len(inj_steps) < (3 if official else 1):
            skipped.append({"episode": ep["episode"],
                            "reason": f"注入步不足: steps={n_steps}"})
            continue
        ep_rows = []
        for inj in inj_steps:
            cfg = {"episode": ep["episode"], "strategy": args.strategy,
                   "trim_fraction": trim_fraction, "weights": weights,
                   "pessimistic": opponents.PessimisticFill(
                       price_discount=args.pessimistic_discount),
                   "profile_path": None,
                   "oracle": not args.no_oracle and official,
                   "oracle_top_k": ORACLE_TOP_K}
            row = evaluate_injection(deps, replay, ep["me_seat"], inj, cfg)
            row["round"] = ep["round"]
            row["mirror"] = ep["mirror"]
            row["opponent"] = ep["opponent"]
            ep_rows.append(row)
            rows.append(row)
        episode_rows.append((ep, ep_rows))
        del replay                                   # 22MB/局，即用即释

    # 汇总与判据（m7 修订双口径，2026-09-19：主口径=同执行器单变量；
    # 参考口径=对 history 做执行器代差修正。首轮判据"逐局 DTSP≥history
    # 且 ≥反应式"把执行器代差错记到计划头上——反应式本身就远落后 history
    # （首轮 mean Δhistory=-27.9k 而 Δ反应式=+444），故修订。）
    episode_summaries = []
    for ep, ep_rows in episode_rows:
        def mean(key, _rows=ep_rows):
            return sum(r[key] for r in _rows) / len(_rows) if _rows else 0.0
        d_hist = mean("dtsp_vs_history")
        d_react = mean("dtsp_vs_reactive")
        # 主口径：逐注入点 DTSP−反应式 的逐局中位数（对单注入灾难稳健）
        med_react = statistics.median(r["dtsp_vs_reactive"] for r in ep_rows)
        primary_pass = med_react >= -GATE_EPS
        # 参考口径：修正项 offset=同注入点（反应式−history）；修正后
        # = mean(DTSP−history) − mean(offset)。代数上等于 mean(DTSP−
        # 反应式)——两口径的对偶性如实注记，差别只在聚合统计（中位 vs
        # 均值）与归因框架（vs 反应式 / vs 修正后的 history）。
        mean_offset = mean("reactive_me") - mean("truth_me")
        corrected = d_hist - mean_offset
        reference_pass = corrected >= -GATE_EPS
        fails = [r for r in ep_rows if r["judge_fail"]]
        episode_summaries.append({
            "episode": ep["episode"], "round": ep["round"],
            "me_seat": ep["me_seat"], "opponent": ep["opponent"],
            "mirror": ep["mirror"], "n_injections": len(ep_rows),
            "mean_truth_me": mean("truth_me"),
            "mean_reactive_me": mean("reactive_me"),
            "mean_dtsp_me": mean("dtsp_me"),
            "dtsp_vs_history": d_hist, "dtsp_vs_reactive": d_react,
            "median_dtsp_vs_reactive": med_react,
            "primary_pass": primary_pass,
            "reactive_vs_history_offset": mean_offset,
            "dtsp_vs_history_corrected": corrected,
            "reference_pass": reference_pass,
            "gate_pass": primary_pass,      # 兼容键=主口径
            "fail_attribution": {
                "twin_noise": sum(1 for r in fails if r["twin_noise_flag"]),
                "opponent_model_gap": sum(1 for r in fails
                                          if r["opponent_model_gap"]),
                "plan_space_gap": sum(1 for r in fails
                                      if r["plan_space_gap"]),
            },
        })

    enough = len(episode_summaries) >= min_episodes
    n_primary = sum(1 for e in episode_summaries if e["primary_pass"])
    n_reference = sum(1 for e in episode_summaries if e["reference_pass"])
    pooled_mean_d_react = (sum(r["dtsp_vs_reactive"] for r in rows)
                           / len(rows)) if rows else 0.0
    # official 门禁（m7 修订主口径）：≥9/14 局中位不劣 且 全集合 mean Δ>0；
    # smoke 模式只摇通 harness，门禁值恒 False 但不影响退出码。
    all_pass = bool(official and enough and n_primary >= 9
                    and pooled_mean_d_react > 0.0)
    report = {
        "mode": args.mode, "team": args.team,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "wall_seconds": round(time.time() - t_start, 1),
        "configuration": {
            "rounds": list(rounds), "injection_days": days,
            "limit": limit, "min_episodes": min_episodes,
            "strategy": args.strategy, "trim_fraction": trim_fraction,
            "weights_preset": args.weights_preset,
            "pessimistic_discount": args.pessimistic_discount,
            "gate_eps": GATE_EPS,
            "twin_noise_eps": TWIN_NOISE_EPS, "oracle": not args.no_oracle,
            "oracle_top_k": ORACLE_TOP_K,
        },
        "criterion_note": (
            "m7 修订双口径（2026-09-19）：主口径=逐局中位注入点 DTSP≥反应式"
            "（同执行器单变量），≥9/14 局不劣且全集合 mean Δ(DTSP−反应式)>0；"
            "参考口径=DTSP 对 history 减执行器代差 offset（=同注入点反应式对 "
            "history）后 ≥9/14 局不劣。两口径在注入点层面代数同构"
            "（DTSP−history−(反应式−history)≡DTSP−反应式），差别只在聚合"
            "统计（主=中位数、参考=均值）与归因框架。"),
        "opponent_models": (rows[0]["opponent_models"] if rows else []),
        "episodes": episode_summaries,
        "skipped_episodes": skipped,
        "rows": rows,
        "summary": {
            "episodes_evaluated": len(episode_summaries),
            "episodes_passed": n_primary,
            "episodes_passed_reference": n_reference,
            "injections_evaluated": len(rows),
            "gates_all_pass": bool(all_pass),
            "enough_episodes": enough,
            "pooled_mean_dtsp_vs_reactive": pooled_mean_d_react,
            "mean_dtsp_vs_history": (sum(e["dtsp_vs_history"]
                                         for e in episode_summaries)
                                     / len(episode_summaries))
            if episode_summaries else 0.0,
            "mean_dtsp_vs_reactive": (sum(e["dtsp_vs_reactive"]
                                          for e in episode_summaries)
                                      / len(episode_summaries))
            if episode_summaries else 0.0,
            "attribution_totals": {
                key: sum(1 for r in rows
                         if r.get("judge_fail") and r[key])
                for key in ("twin_noise_flag", "opponent_model_gap",
                            "plan_space_gap")
            },
        },
    }

    report_path = os.path.join(args.out_dir, "bench_report.json")
    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2,
                  sort_keys=True)
    summary_path = os.path.join(args.out_dir, "bench_summary.md")
    with open(summary_path, "w", encoding="utf-8") as handle:
        handle.write(_summary_md(report))

    print(f"[bench] mode={args.mode} episodes={len(episode_summaries)} "
          f"injections={len(rows)} gates_all_pass={all_pass} "
          f"wall={report['wall_seconds']}s")
    print(f"[bench] report -> {report_path}")
    print(f"[bench] summary -> {summary_path}")

    if official:
        if not enough:
            sys.stderr.write(
                f"[exit 1] 可评局 {len(episode_summaries)} < 要求 "
                f"{min_episodes}（skip 原因见报告 skipped_episodes）\n")
            return 1
        if not all_pass:
            sys.stderr.write(
                "[exit 1] m7 修订主口径未过：逐局中位注入点 DTSP≥反应式 "
                f"{n_primary}/{len(episode_summaries)} 局（需 ≥9）且全集合 "
                f"mean Δ(DTSP−反应式)={pooled_mean_d_react:+.0f} 需 >0；"
                "参考口径 " f"{n_reference}/{len(episode_summaries)} 局。"
                "归因分布见报告（诚实记录，不放宽判据）\n")
            return 1
        print(f"[bench] 主口径过线：{n_primary}/{len(episode_summaries)} 局"
              f"中位不劣，全集合 mean Δ={pooled_mean_d_react:+.0f}；"
              f"参考口径 {n_reference}/{len(episode_summaries)} 局")
        return 0
    # smoke：harness 摇通即 0（判据行照实写进报告，不做门禁退出码）
    return 0


def _summary_md(report):
    lines = [
        "# DTSP 离线基准摘要（planner_offline_bench）", "",
        f"- 模式：`{report['mode']}`｜队伍：`{report['team']}`｜"
        f"生成：{report['generated_at_utc']}",
        f"- 注入日：{report['configuration']['injection_days']}｜"
        f"聚合策略：`{report['configuration']['strategy']}`",
        f"- {report.get('criterion_note', '')}",
        f"- 公平性口径：反应式与 DTSP 共享同一孪生与同一对手"
        f"（回放真实动作）；对手模型 Ω 只作用于 DTSP 的计划选择。", "",
        "| 局 | 对手 | 注入数 | mean 真值 | mean 反应式 | mean DTSP "
        "| 中位Δ反应式(主) | meanΔhistory | offset | 修正后(参考) "
        "| 主判 | 参考判 | 归因(tn/om/ps) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for e in report["episodes"]:
        attr = e["fail_attribution"]
        lines.append(
            f"| {e['episode']} | {e['opponent']} | {e['n_injections']} "
            f"| {e['mean_truth_me']:.0f} | {e['mean_reactive_me']:.0f} "
            f"| {e['mean_dtsp_me']:.0f} "
            f"| {e['median_dtsp_vs_reactive']:+.0f} "
            f"| {e['dtsp_vs_history']:+.0f} "
            f"| {e['reactive_vs_history_offset']:+.0f} "
            f"| {e['dtsp_vs_history_corrected']:+.0f} "
            f"| {'PASS' if e['primary_pass'] else 'FAIL'} "
            f"| {'PASS' if e['reference_pass'] else 'FAIL'} "
            f"| {attr['twin_noise']}/{attr['opponent_model_gap']}"
            f"/{attr['plan_space_gap']} |")
    s = report["summary"]
    lines += [
        "",
        f"**汇总（m7 修订双口径）**：主口径 "
        f"{s['episodes_passed']}/{s['episodes_evaluated']} 局中位不劣、"
        f"全集合 mean Δ(DTSP−反应式)="
        f"{s['pooled_mean_dtsp_vs_reactive']:+.0f}；"
        f"参考口径 {s['episodes_passed_reference']}/"
        f"{s['episodes_evaluated']} 局不劣；"
        f"mean Δhistory={s['mean_dtsp_vs_history']:+.0f}、"
        f"mean Δ反应式={s['mean_dtsp_vs_reactive']:+.0f}；"
        f"归因合计 tn/om/ps = "
        f"{s['attribution_totals']['twin_noise_flag']}"
        f"/{s['attribution_totals']['opponent_model_gap']}"
        f"/{s['attribution_totals']['plan_space_gap']}。",
        "",
        "对手模型口径：",
    ]
    for note in report["opponent_models"]:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
