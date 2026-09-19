# ===========================================================================
# 【中文·模块导览】planner/runtime.py —— DTSP bot 内运行时（Track-B P3）
# ---------------------------------------------------------------------------
# 职责（任务包 P3）：每天黎明（hour==0）用孪生规划剩余整季选计划 → 覆盖
#   注入当日执行。四条产品红线：
#     1) 预算内安全：时间治理器把规划压进 min(0.85s, 0.5s+池/黎明数×0.5)
#        的黎明预算（actTimeout=1s/回合 + remainingOverageTime 全局池），
#        rollout 循环逐时间片查 deadline，超时用当前最优；预算耗尽跳过
#        规划沿用上日计划。
#     2) 异常零风险：三道 fail-open（任意异常 / 引擎指纹不符 / 规划超限）
#        → 恢复 v13.8 原值快照 + PLANNER_ENABLED=False（粘性）→ 动作流与
#        旗关 golden 逐字节一致（tests/test_p3_integration.py 注入验证）。
#     3) 旗关零足迹：本模块只被提交入口 main.py 的 DTSP_RUNTIME_CONFIG
#        唤醒；裸命名空间（旗关黄金/多数单测）不含该名字，钩子死路——
#        src 九模块的旗关等价不因本文件存在而变。
#     4) 不写日志文件：遥测进进程内 _TRACE 结构（提交包零 I/O）。
# 选择管线（钉死默认 = P2.6 终局裁决配置 + 预算内的孪生精化段；v3 K1
#   近平守成：投影与 rollout 两段均带 identity tie-break，边际 <τ 不偏离
#   v13.8——round-24 法证终稿 §5 第 0 项）：
#   组装 obs 摘要 → enumerate_plans(≤120，含 identity) → 现任投影器 ×
#   Ω=4 压力打分（v3.1：悲观折扣=对手压力自适应 plans.pressure_discount
#   ——弱对手→1.0、强对手→0.75；rollout 余季延续段守 None→强端常数）→
#   robust_select(trimmed_mean@0.25, identity_key) → 投影排序 top-K
#   （identity 恒在）→ 孪生 rollout（K×Ω' 子集：沙盒命名空间驱动我方席 +
#   对手模型日计划逐回合滴灌；地平线 H 天；得分 = 地平线资金 + 投影器
#   余季延续）→ 完成者中 argmax（近平守成回落 identity）→
#   plan_to_knob_overrides 注入。
# K/H 由实测曲线裁剪：本机实测（exports/probes/p3_integration/）沙盒装载
#   37.6ms、投影全段 34.1ms、agent 逐步 1.5-2.1ms——全季 agent 驱动
#   rollout ≈1.2s 出不进 0.85s 预算，K≈15-25 全季先验按实测降为短地平线
#   阶梯 ((6,1),(4,2),(3,3),(2,4),(1,6))，估算成本 ×2（评审机余量）才启动。
# 对手模型运行时数据（PassiveExtrapolation 史）：obs 公开 farms/market
#   轻量记账——(库存日增 + 城镇期望消费) = 总入市量的对手侧归因（含我方
#   卖出 → 保守高估对手倾销，与钉死的悲观立场同向；我方精确卖出量在
#   本席观测里不可得，不做二次发明）；公开畜群日增量 = 买畜。不复用
#   observer.py 的 est_*：那是干扰模块的身份/归因影子估计（跨模块耦合
#   且格式不匹配），本账本只需公开量守恒一行式。
# 纪律：stdlib-only、无日志 I/O、无网络；时间只经 _now()（测试可注入
#   假时钟）；确定性：同进程同输入同输出（deadline 降级除外——那是
#   治理器的规定动作，测试用假时钟钉住）。
# ===========================================================================

import copy
import json
import os
import time
import traceback

from . import opponents as _opponents
from . import plans as _plans
from . import select as _select
from . import twin as _twin

SEASON_DAYS = 30            # 引擎整季天数（plans.project_season 同口径）
DAWN_TURNS_PER_DAY = 24     # turnsPerDay（引擎默认配置）

# ---- 治理器默认值（可被 DTSP_RUNTIME_CONFIG 覆盖；出处见模块头实测段）----
_DEFAULTS = {
    "enabled": True,
    "seed": 1,                    # 孪生伪种子（线上真种子对 agent 不可观测）
    "budget_cap_s": 0.85,         # 黎明规划预算硬帽（< actTimeout=1s）
    "pool_base_s": 0.5,           # 预算公式：min(cap, base+池/黎明数×0.5)
    "min_projector_budget_s": 0.15,   # 低于此只沿用上日计划
    "rollout_gate_budget_s": 0.35,    # 低于此只跑投影段（不开孪生段）
    "reserve_s": 0.06,            # 死线安全垫（回合其余工 + 调度噪声）
    "safety": 2.0,                # 评审机安全余量（速率未测时：估算 ×2 才启动）
    "safety_measured": 1.25,      # 进程内速率已实测后的余量（deadline 兜底）
    "rate_prior_s": 0.0025,       # 逐步 rollout 成本先验（实测 1.5-2.1ms）
    "sandbox_build_s": 0.038,     # 沙盒命名空间装载成本（实测 37.6ms）
    # 阶梯 (K, H)：投影 top-K × 地平线 H 天；按实测预算降级序排列
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
    # rollout Ω' 子集（P2.6 钉死搭档=悲观 0.75；键=opponents 模型名）
    "rollout_models": ("pessimistic_fill",),
    "trace_cap": 64,
}

# ---- 进程内运行态（一进程一局；测试经 reset_state() 复位）----
_TRACE = {"dawns": [], "failopens": [], "game_resets": 0}
_STATE = {
    "sticky_off": False,       # fail-open 后粘性关断（本局不再规划）
    "engine": None,            # EngineBundle 缓存
    "rate_ewma_s": None,       # 逐步 rollout 成本 EWMA（秒/步，不含沙盒装载）
    "ledger": {},              # player -> 记账状态
    "dawn_cache": {},          # (player, day, signature) -> {plan, overrides}
    "last_day": {},            # player -> 上次见到的 day（换局检测）
    "last_rung": None,         # 最近一次黎明实际执行的阶梯档 [K, H, 模型数]
    "last_rollout_wall_s": None,   # 最近一次黎明 rollout 段实耗（秒）
}


def reset_state():
    """清空进程内运行态（测试/多局隔离用；线上一进程一局不需要）。"""
    _TRACE["dawns"].clear()
    _TRACE["failopens"].clear()
    _TRACE["game_resets"] = 0
    _STATE["sticky_off"] = False
    _STATE["engine"] = None
    _STATE["rate_ewma_s"] = None
    _STATE["ledger"].clear()
    _STATE["dawn_cache"].clear()
    _STATE["last_day"].clear()
    _STATE["last_rung"] = None
    _STATE["last_rollout_wall_s"] = None


def trace():
    """遥测只读视图（不落盘；测试与 metrics 收集消费）。engaged=本局是否
    至少一个黎明完成过计划注入（接合判定位；P4.1 遥测通道）。"""
    return {"dawns": list(_TRACE["dawns"]),
            "failopens": list(_TRACE["failopens"]),
            "game_resets": _TRACE["game_resets"],
            "engaged": any(d.get("selected") for d in _TRACE["dawns"])}


def _now():
    """单调时钟（模块级出口：测试注入假时钟钉住降级路径）。"""
    return time.monotonic()


def _cfg(config, key):
    value = config.get(key, _DEFAULTS.get(key))
    return _DEFAULTS.get(key) if value is None else value


# --------------------------------------------------------------------------
# 引擎解析（提交包内置 scene 优先，回退 vendored wheel；指纹不符即抛）
# --------------------------------------------------------------------------
def resolve_engine():
    """进程内缓存的引擎装载：包内 planner/scene/ 两文件（build.py 从
    vendored wheel 抽取入包）→ twin.load_engine_from_scene（零磁盘写）；
    仓库开发环无 scene 目录 → twin.load_engine()（wheel 抽取缓存路径）。
    指纹不符时两者都抛 TwinFingerprintError（fail-closed），由调用方
    fail-open。"""
    if _STATE["engine"] is not None:
        return _STATE["engine"]
    scene_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "scene")
    scene_py = os.path.join(scene_dir, "kaggriculture.py")
    scene_json = os.path.join(scene_dir, "kaggriculture.json")
    if os.path.isfile(scene_py) and os.path.isfile(scene_json):
        bundle = _twin.load_engine_from_scene(scene_py, scene_json,
                                              source="bundled_scene")
    else:
        bundle = _twin.load_engine()
    _STATE["engine"] = bundle
    return bundle


# --------------------------------------------------------------------------
# obs → 局况摘要（plans.build_obs_summary 键契约；口径与离线基准
# build_obs_summary_from_state 逐字段对齐——P2.6 通过配置的排序面）
# --------------------------------------------------------------------------
_CROP_NAMES = ("STRAWBERRY", "WHEAT", "MELON", "CARROT", "TOMATO")
_ANIMAL_NAMES = ("GOOSE", "COW", "SHEEP")


def scan_farm(farm):
    """公开农场 dict → (crops, herd, money, n_quadrants)。tile 语义：
    None 空 / "LOCKED" 锁定 / dict{crop|animal|kind}（回放 schema 实测）。"""
    crops = {name: 0 for name in _CROP_NAMES}
    herd = 0
    for row in (farm or {}).get("tiles") or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            crop = tile.get("crop")
            if crop in crops:
                crops[crop] += 1
            if tile.get("animal") in _ANIMAL_NAMES:
                herd += 1
    money = float((farm or {}).get("money", 0) or 0)
    quads = len((farm or {}).get("unlocked_quadrants") or ()) or 1
    return crops, herd, money, int(quads)


def compute_town_demand(module, unlocked_shops):
    """城镇日吸收（引擎 §4 语义镜像；公式与
    scripts/planner_offline_bench.compute_town_demand 同源——商店每
    townShopSellInterval 步各抽 1 件（单品店 2 件）、镇中心每 24 步各抽
    1 件非肥料品；unlocked_shops 已观测故此值为逐日确定量）。"""
    demand = {}
    per_day = 24.0 / 4.0                     # townShopSellInterval=4
    for shop in sorted(set(unlocked_shops or [])):
        products = (getattr(module, "SHOPS", {}) or {}).get(shop)
        if not products:
            continue
        draws = per_day * (2.0 if len(products) == 1 else 1.0)
        share = draws / float(len(products))
        for item in products:
            demand[item] = demand.get(item, 0.0) + share
    for item in getattr(module, "TOWN_CENTER_PRODUCTS", ()) or ():
        if item != "FERTILIZER":
            demand[item] = demand.get(item, 0.0) + 1.0
    return demand


def build_obs_summary(module, obs, player, day):
    """线上 obs → plans 局况摘要（与离线基准同键面；opening_played /
    d6_checks / p4_tier 缺省 None——与 P2.6 通过配置的排序面一致）。"""
    farms = obs.get("farms") if isinstance(obs, dict) else obs.farms
    market = obs.get("market") if isinstance(obs, dict) else obs.market
    town = obs.get("town") if isinstance(obs, dict) else obs.town
    prices = dict((market or {}).get("prices") or {})
    unlocked = list((town or {}).get("unlocked_shops") or [])
    demand = compute_town_demand(module, unlocked)
    my_crops, my_herd, my_money, quads = scan_farm(farms[player])
    opp = farms[1 - player] if len(farms) > 1 else None
    opp_crops, opp_herd, opp_money, opp_quads = scan_farm(opp)
    opp_class = _plans.classify_opponent_opening(day, opp_herd, opp_crops)
    return _plans.build_obs_summary(
        day=day, money=my_money, herd=my_herd, crops=my_crops,
        unlocked_quadrants=quads, prices=prices, daily_demand=demand,
        opponent={"herd": opp_herd, "crops": opp_crops, "money": opp_money,
                  "quads": opp_quads},
        opp_class=opp_class)


# --------------------------------------------------------------------------
# 对手逐日记账（obs 公开量守恒；保守口径见模块头）
# --------------------------------------------------------------------------
def update_opponent_ledger(obs, player, day, summary):
    """黎明记账：总入市估计 = 库存日增 + 城镇期望消费（含我方卖出，保守
    高估对手倾销）；对手公开畜群日增 = 买畜。返回 (history, inflow_proxy)
    ——history 喂 PassiveExtrapolation，inflow_proxy 喂 PessimisticFill
    的 our_sell_plan（我方精确卖出量本席不可得，以总入市保守代理）。"""
    market = obs.get("market") if isinstance(obs, dict) else obs.market
    inv = {k: float(v) for k, v in ((market or {}).get("inventory") or {})
           .items() if isinstance(v, (int, float))}
    opp_herd = int((summary.get("opponent") or {}).get("herd", 0))
    demand = summary.get("daily_demand") or {}
    led = _STATE["ledger"].setdefault(player, {"prev": None, "history": [],
                                               "last_day": -1})
    if led["prev"] is None or day <= led["last_day"]:
        led["last_day"] = day
        led["prev"] = {"inv": inv, "herd": opp_herd, "day": day}
        return list(led["history"]), {}
    prev = led["prev"]
    inflow = {}
    for item, now in inv.items():
        delta = now - float(prev["inv"].get(item, 0.0))
        est = delta + float(demand.get(item, 0.0))   # +城镇消费 ≈ 总入市
        if est > 0.0:
            inflow[item] = round(est, 1)
    animal_buys = max(0, opp_herd - int(prev["herd"]))
    led["history"].append({"day": int(prev["day"]), "sells": dict(inflow),
                           "animal_buys": animal_buys})
    if len(led["history"]) > 32:             # 只留近窗（窗口模型消费 ≤3 日）
        del led["history"][:len(led["history"]) - 32]
    led["prev"] = {"inv": inv, "herd": opp_herd, "day": day}
    led["last_day"] = day
    return list(led["history"]), dict(inflow)


# --------------------------------------------------------------------------
# 时间治理器
# --------------------------------------------------------------------------
def dawn_budget(obs, day, config):
    """黎明规划预算（秒）：min(cap, base + 剩余池/剩余黎明数×0.5)。
    池不可读按满池 60 处理；池枯（≤base/2）→ 0=跳过规划沿用上日计划。"""
    cap = float(_cfg(config, "budget_cap_s"))
    base = float(_cfg(config, "pool_base_s"))
    pool = 60.0
    raw = obs.get("remainingOverageTime") if isinstance(obs, dict) else \
        getattr(obs, "remainingOverageTime", None)
    try:
        if raw is not None:
            pool = max(0.0, float(raw))
    except (TypeError, ValueError):
        pool = 60.0
    if pool <= base / 2.0:
        return 0.0, pool
    remaining_dawns = max(1, SEASON_DAYS - int(day))
    return min(cap, base + pool / remaining_dawns * 0.5), pool


# --------------------------------------------------------------------------
# 沙盒 rollout（逐 rollout 全新 src 装载，防跨局/跨规划串态——与离线
# 基准 build_v13_namespace 同语义；沙盒内无 DTSP_RUNTIME_CONFIG，钩子死路）
# --------------------------------------------------------------------------
_SRC_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                     "mission", "solver", "executor", "market", "entry")


def build_sandbox_agent(overrides, agent_dir):
    """装载全新扁平命名空间并应用计划覆盖，返回其 agent callable。"""
    ns = {}
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), ns)
    for mod in _SRC_MODULE_ORDER:
        path = os.path.join(agent_dir, "src", mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        exec(compile(source, path, "exec"), ns)
    for key in sorted(overrides):
        value = overrides[key]
        if key.startswith("PLANNER_LOCAL.") or key == "PACK":
            continue                         # 信息性键（缺口清单口径）
        if key == "PLANNER_ENABLED":
            ns[key] = True
            continue
        if key.startswith("PLANNER_OVERRIDES."):
            ns["PLANNER_OVERRIDES"][key.split(".", 1)[1]] = value
            continue
        if "." in key:
            base, leaf = key.split(".", 1)
            container = ns.get(base)
            if isinstance(container, dict):
                if leaf.isdigit() and int(leaf) in container:
                    container[int(leaf)] = value   # LAND_PLAN 整数键
                else:
                    container[leaf] = value
            continue
        if key in ns:
            ns[key] = value
    return ns["agent"]


def agent_dir():
    """含 src/ 的包根（包内 = 抽取目录；仓库 = agent/）。build_sandbox_
    agent 在其下拼接 "src/<mod>.py"——与 main.py 的 _find_root 语义一致。"""
    return os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def _drip_feed(day_action, first_turn):
    """对手模型"日计划" → 逐回合动作。引擎市场单逐回合执行完毕
    （per-unit 锁步，factsheet §3），故：SELL 日量 ÷24 滴灌到每回合；
    BUY 类（BUY_ANIMAL/BUY_SEED/BUY_PRODUCT，模型语义为每日一次）只在
    当日首回合以全量下发，其余回合不发——否则 1 买/日会放大成 24 买/日。
    farmer/hands 恒 PASS（对手模型只补市场侧耦合，opponents.py 契约）。"""
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    dripped = []
    for order in (day_action.get("market") or []):
        if not isinstance(order, list) or len(order) < 3:
            continue
        op = order[0]
        try:
            qty = int(order[2])
        except (TypeError, ValueError):
            continue
        if qty < 1:
            continue
        if op == "SELL":
            dripped.append(["SELL", order[1],
                            max(1, int(round(qty / DAWN_TURNS_PER_DAY)))])
        elif first_turn:
            dripped.append([op, order[1], qty])
    action["market"] = dripped[:10]          # 官方语义：超 10 静默丢弃
    return action


def _seat_farm(state, seat):
    """孪生状态里 seat 席的农场正本（farms 为 obs0 共享正本）。"""
    return state.seats[0].observation.farms[seat]


def _opp_shed_view(state, opp):
    """对手席棚仓（孪生内 = 合成满仓或回放真值；供模型钳制卖量）。"""
    private = state.seats[opp].observation.private or {}
    shed = private.get("shed") or {}
    return dict(shed)


def build_rollout_tail_summary(module, state, player):
    """地平线孪生态 → 投影器余季延续的 obs_summary（相对排序机器，
    与 dawn 摘要同键面；精化得分 = 地平线资金 + project_season 余季）。"""
    farms = state.seats[0].observation.farms
    market = state.seats[0].observation.market
    town = state.seats[0].observation.town
    prices = dict((market or {}).get("prices") or {})
    unlocked = list((town or {}).get("unlocked_shops") or [])
    demand = compute_town_demand(module, unlocked)
    my_crops, my_herd, my_money, quads = scan_farm(farms[player])
    opp = farms[1 - player] if len(farms) > 1 else None
    opp_crops, opp_herd, opp_money, opp_quads = scan_farm(opp)
    day = int(state.seats[0].observation.day)
    return _plans.build_obs_summary(
        day=day, money=my_money, herd=my_herd, crops=my_crops,
        unlocked_quadrants=quads, prices=prices, daily_demand=demand,
        opponent={"herd": opp_herd, "crops": opp_crops, "money": opp_money,
                  "quads": opp_quads},
        opp_class=None)


def _rollout_once(bundle, dawn_state, player, spec, model, our_sell_plan,
                  history, horizon_steps, deadline):
    """单次孪生 rollout：我方席 = 计划覆盖的沙盒 agent，对手席 = 模型
    日计划滴灌。地平线 horizon_steps 步（天数×24，钳到季末）。
    返回 (money_me, tail_summary, steps_done)。"""
    overrides = _plans.plan_to_knob_overrides(spec)
    agent = build_sandbox_agent(overrides, agent_dir())
    state = _twin.clone_state(dawn_state)
    opp = 1 - player
    steps = 0
    opp_day = None
    day_action = None
    while not state.env.done and steps < horizon_steps:
        obs_me = state.seats[player].observation
        if obs_me.day != opp_day or day_action is None:
            opp_day = obs_me.day
            _, opp_herd, opp_money, _ = _seat_scan(state, opp)
            day_action = model.propose_actions(
                {"history": list(history or []),
                 "our_sell_plan": dict(our_sell_plan or {}),
                 "shed": _opp_shed_view(state, opp), "herd": opp_herd,
                 "money": opp_money}, opp_day)
        mine = agent(obs_me)
        theirs = _drip_feed(day_action, steps % DAWN_TURNS_PER_DAY == 0)
        pair = [None, None]
        pair[player] = mine
        pair[opp] = theirs
        _twin.step(state, pair)
        steps += 1
        if steps % DAWN_TURNS_PER_DAY == 0 and _now() > deadline:
            break                            # 逐时间片查 deadline（日粒度）
    money = _twin.final_money(state)[player]
    tail = build_rollout_tail_summary(bundle.module, state, player)
    return float(money), tail, steps


def _seat_scan(state, seat):
    return scan_farm(_seat_farm(state, seat))


# --------------------------------------------------------------------------
# 覆盖注入 / 快照恢复（fail-open 的逐字节等价根基）
# --------------------------------------------------------------------------
def governed_keys(sample_spec):
    """governed 键面（计划无关：plan_to_knob_overrides 全名面发射）。"""
    return sorted(_plans.plan_to_knob_overrides(sample_spec))


def take_pristine_snapshot(ns, keys):
    """首次启用前抓 v13.8 原值快照（标量取值、容器整 deepcopy）。返回
    {名字: 原值}（容器为深拷贝；恢复时再拷贝一次，保证可重复恢复）。"""
    snapshot = {}
    for key in keys:
        if key.startswith("PLANNER_OVERRIDES.") or key == "PLANNER_ENABLED" \
                or key.startswith("PLANNER_LOCAL.") or key == "PACK":
            continue
        if "." in key:
            base = key.split(".", 1)[0]
            if base in ns:
                snapshot[base] = copy.deepcopy(ns[base])
            continue
        if key in ns:
            snapshot[key] = copy.deepcopy(ns[key])
    return snapshot


def apply_overrides(ns, overrides):
    """计划覆盖 → 活跃扁平命名空间（幂等：全绝对值写入，同键集覆盖）。"""
    for key in sorted(overrides):
        value = overrides[key]
        if key.startswith("PLANNER_LOCAL.") or key == "PACK":
            continue
        if key == "PLANNER_ENABLED":
            ns[key] = True
            continue
        if key.startswith("PLANNER_OVERRIDES."):
            ns["PLANNER_OVERRIDES"][key.split(".", 1)[1]] = value
            continue
        if "." in key:
            base, leaf = key.split(".", 1)
            container = ns.get(base)
            if isinstance(container, dict):
                if leaf.isdigit() and int(leaf) in container:
                    container[int(leaf)] = value
                else:
                    container[leaf] = value
            continue
        if key in ns:
            ns[key] = value


def restore_pristine(ns):
    """fail-open 恢复：v13.8 原值写回 + 旗关 + 寄存器清空。恢复后动作流
    与旗关 golden 逐字节一致（_plan_knob 旗关回默认 + 直写键回原值）。"""
    snapshot = ns.get("_DTSP_PRISTINE_SNAPSHOT")
    if snapshot:
        for name, value in sorted(snapshot.items()):
            ns[name] = copy.deepcopy(value)
    if isinstance(ns.get("PLANNER_OVERRIDES"), dict):
        ns["PLANNER_OVERRIDES"].clear()
    ns["PLANNER_ENABLED"] = False


# --------------------------------------------------------------------------
# 黎明决策主流程
# --------------------------------------------------------------------------
def _signature(day, player, summary, obs):
    """黎明决策缓存键（同 obs 重复调用复用已注入决策——确定性钉）。"""
    market = obs.get("market") if isinstance(obs, dict) else obs.market
    private = obs.get("private") if isinstance(obs, dict) else obs.private
    payload = {
        "day": int(day), "player": int(player),
        "money": round(float(summary.get("money", 0.0)), 3),
        "herd": int(summary.get("herd", 0)),
        "crew": int(summary.get("crew", 0)),
        "quads": int(summary.get("unlocked_quadrants", 1)),
        "crops": summary.get("crops") or {},
        "opp_herd": int((summary.get("opponent") or {}).get("herd", 0)),
        # v3.1：对手资金/象限进缓存键（压力折扣依赖这两个公开量——同
        #   day 同签名不同对手态的 obs 不得共享决策缓存）
        "opp_money": round(float((summary.get("opponent") or {})
                                 .get("money", 0.0) or 0.0), 3),
        "opp_quads": int((summary.get("opponent") or {}).get("quads", 1)),
        "prices": {k: round(float(v), 3)
                   for k, v in sorted((summary.get("prices") or {}).items())
                   if isinstance(v, (int, float))},
        "inv": {k: round(float(v), 1) for k, v in
                sorted(((market or {}).get("inventory") or {}).items())
                if isinstance(v, (int, float))},
        "shed": {k: v for k, v in sorted(((private or {}).get("shed") or {})
                                         .items())
                 if isinstance(v, (int, float))},
        "shops": sorted(((obs.get("town") if isinstance(obs, dict)
                          else obs.town) or {}).get("unlocked_shops") or []),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      default=repr)


def _models_for_rollout(config, models):
    """Ω' 子集解析：按名过滤 build_default_models 的实例（保序）。"""
    wanted = tuple(_cfg(config, "rollout_models") or ())
    picked = [m for m in models if m.name in wanted]
    return picked


def _pick_rung(config, usable_s, n_models):
    """按实测曲线选 (K, H, 模型数)。速率未实测（进程首个黎明）时用 2×
    先验余量——若阶梯仍无一能启动，降档"校准档"（1 计划 × 1 模型 ×
    1 天，≤0.1s 量级）先测出本机速率，解锁后续黎明的阶梯选择；速率
    实测后余量收窄到 safety_measured（deadline 逐时间片兜底墙钟）。"""
    measured = _STATE["rate_ewma_s"] is not None
    rate = _STATE["rate_ewma_s"] or float(_cfg(config, "rate_prior_s"))
    sandbox = float(_cfg(config, "sandbox_build_s"))
    safety = float(_cfg(config, "safety_measured" if measured else "safety"))
    for k_run, h_days in (_cfg(config, "ladder") or ()):
        est = k_run * n_models * (sandbox
                                  + h_days * DAWN_TURNS_PER_DAY * rate)
        if est * safety <= usable_s:
            return int(k_run), int(h_days), int(n_models)
    est_cal = sandbox + DAWN_TURNS_PER_DAY * rate
    if est_cal * safety <= usable_s:
        return 1, 1, 1                     # 校准档：只花一次测量钱
    return None


def _rollout_refinement(bundle, config, deadline, dawn_state, player,
                        ranked_specs, models, our_sell_plan, history):
    """预算内孪生精化段：投影 top-K × Ω' 子集 rollout。
    返回 {plan_key: {model_name: score}}（只含完成的 rollout）。"""
    n_models = max(1, len(models))
    rung = _pick_rung(config, max(0.0, deadline - _now()), n_models)
    _STATE["last_rung"] = [int(rung[0]), int(rung[1]), int(rung[2])] \
        if rung else None                      # 遥测：本黎明实际档位
    _STATE["last_rollout_wall_s"] = 0.0
    if rung is None:
        return {}, 0
    k_run, h_days, m_count = rung
    models = models[:m_count]              # 校准档只跑首个模型
    day_now = int(dawn_state.seats[0].observation.day)
    horizon = min(h_days * DAWN_TURNS_PER_DAY,
                  max(0, SEASON_DAYS - day_now) * DAWN_TURNS_PER_DAY)
    if horizon <= 0:
        return {}, 0
    done = {}
    steps_total = 0
    sandbox_s = float(_cfg(config, "sandbox_build_s"))
    for spec in ranked_specs[:k_run]:
        for model in models:
            if deadline - _now() <= float(_cfg(config, "reserve_s")):
                return done, steps_total       # 死线：用已完成的
            t0 = _now()
            money, tail, steps = _rollout_once(
                bundle, dawn_state, player, spec, model, our_sell_plan,
                history, horizon, deadline)
            dt = max(1e-6, _now() - t0)
            steps_total += steps
            _STATE["last_rollout_wall_s"] = \
                _STATE["last_rollout_wall_s"] + dt
            # 逐步成本 EWMA（剔除沙盒装载项；治理器下次选阶梯用）
            rate = max(1e-6, dt - sandbox_s) / max(1, steps)
            prev = _STATE["rate_ewma_s"] or float(_cfg(config,
                                                       "rate_prior_s"))
            _STATE["rate_ewma_s"] = 0.7 * prev + 0.3 * rate
            pressure = model.supply_pressure(None)
            tail_score = _plans.project_season(spec, tail, pressure) \
                if tail is not None else 0.0
            done.setdefault(spec.key(), {})[model.name] = \
                float(money) + float(tail_score)
    return done, steps_total


def dawn_hook(obs, ns, config, player=0, day=0, hour=0):
    """黎明钩子（entry 层唯一接线点；非黎明/关断路径零规划开销）。

    任何异常 → fail-open 三道：恢复 v13.8 快照 + 旗关（粘性）+ 遥测
    记因。返回 None（入口不消费返回值；注入经 ns 副作用生效）。"""
    if not _cfg(config, "enabled"):
        return None
    if _STATE["sticky_off"]:
        return None
    try:
        if int(hour) != 0 or not (0 <= int(day) < SEASON_DAYS):
            return None
        # 换局检测（同进程多局：day 回退即重置该席账本与决策缓存）
        if int(day) < _STATE["last_day"].get(player, -1):
            _STATE["ledger"].pop(player, None)
            for key in [k for k in _STATE["dawn_cache"] if k[0] == player]:
                del _STATE["dawn_cache"][key]
            _STATE["last_day"][player] = -1
            _TRACE["game_resets"] += 1
        t_start = _now()
        budget, pool = dawn_budget(obs, day, config)
        record = {"day": int(day), "player": int(player),
                  "budget_s": round(budget, 4), "pool": round(pool, 2),
                  "policy": "skip", "rollouts": 0, "steps": 0,
                  "switched": False}
        try:
            if budget < float(_cfg(config, "min_projector_budget_s")):
                record["policy"] = "keep_yesterday"
                return None                   # 预算耗尽：沿用上日计划
            module = resolve_engine().module
            summary = build_obs_summary(module, obs, player, day)
            signature = _signature(day, player, summary, obs)
            cache_key = (int(player), int(day), signature)
            cached = _STATE["dawn_cache"].get(cache_key)
            if cached is not None:
                # 同 obs 复用已定决策：幂等重放注入（防跨局陈旧覆盖残留），
                # 不重花规划预算（确定性钉 + 省预算）。
                record["policy"] = "cache_hit"
                apply_overrides(ns, cached["overrides"])
                ns["_DTSP_LAST_PLAN_KEY"] = cached["plan"]
                return None
            _STATE["last_day"][player] = int(day)

            # —— 投影段（P2.6 钉死配置：trimmed_mean@0.25 × 悲观 0.75；
            #     v3 K1：近平守成 tie-break 偏向 identity）——
            candidates = _plans.enumerate_plans(summary)
            models = _opponents.build_default_models()
            history, our_sells = update_opponent_ledger(obs, player, day,
                                                        summary)
            identity_key = _plans.identity_spec().key()
            j_matrix = {}
            for spec in candidates:
                scores = {}
                for model in models:
                    scores[model.name] = _plans.project_season(
                        spec, summary, model.supply_pressure(summary))
                j_matrix[spec.key()] = scores
            selection = _select.robust_select(
                j_matrix, strategy="trimmed_mean",
                trim_fraction=_select.DEFAULT_TRIM_FRACTION,
                identity_key=identity_key)
            proj_best = selection["best"]
            record["proj_best"] = proj_best
            record["n_plans"] = len(candidates)
            if selection["tie_break"] and "守成" in selection["tie_break"]:
                record["identity_tiebreak_proj"] = True
                record["identity_tiebreak_note"] = selection["tie_break"]

            # —— 孪生精化段（K×Ω' 子集，deadline 治理）——
            # v3 比较集：投影排序面（修复 v2 的键序残余——refinement 此前
            # 取"枚举序前 K"而非"投影 top-K"，与模块头文档不符）；K1：
            # identity 守成点恒在比较集（rollout 段同近平守成规则）。
            selected_key = proj_best
            if budget >= float(_cfg(config, "rollout_gate_budget_s")):
                spec_map = {s.key(): s for s in candidates}
                ranked = [spec_map[k] for k, _ in selection["ranking"]
                          if k in spec_map]
                if proj_best != identity_key:
                    ident = spec_map.get(identity_key)
                    if ident is not None and ident not in ranked[:1]:
                        if ident in ranked:
                            ranked.remove(ident)
                        ranked.insert(1, ident)
                roll_models = _models_for_rollout(config, models)
                deadline = t_start + budget - float(_cfg(config,
                                                         "reserve_s"))
                bundle = resolve_engine()
                seed = int(_cfg(config, "seed"))
                dawn_state = _twin.new_state_from_obs(
                    obs, player=player, seed=seed, bundle=bundle)
                done, steps = _rollout_refinement(
                    bundle, config, deadline, dawn_state, player, ranked,
                    roll_models, our_sells, history)
                record["rollouts"] = sum(len(v) for v in done.values())
                record["steps"] = steps
                record["policy"] = "rollout" if done else "projector_only"
                record["rung"] = _STATE.get("last_rung")
                record["rollout_wall_s"] = round(
                    float(_STATE.get("last_rollout_wall_s") or 0.0), 4)
                if done:
                    aggregates = {}
                    for key, per_model in done.items():
                        aggregates[key] = _select.aggregate_scores(
                            per_model, strategy="trimmed_mean",
                            trim_fraction=_select.DEFAULT_TRIM_FRACTION)
                    best_key = sorted(aggregates.items(),
                                      key=lambda kv: (-kv[1], kv[0]))[0][0]
                    # 终审 τ 闸（法证终稿 §4"拒收"语义）：rollout 改判
                    # proj_best 需决定性证据（边际 > τ×|proj_best|）——
                    # 1 日地平线对日程/时点类微差不可辨，非决定性边际的
                    # 改判=支付时点伪影驱动的选择抖动（official 复裁
                    # run2/3 实测 -27.9%/-40.9% 主动损伤的直接反义）。
                    if best_key != proj_best and proj_best in aggregates:
                        pv = float(aggregates[proj_best])
                        bv = float(aggregates[best_key])
                        if bv - pv < _select.IDENTITY_TIEBREAK_TAU * max(
                                1.0, abs(pv)):
                            record["rollout_switch_vetoed"] = round(
                                bv - pv, 1)
                            best_key = proj_best
                    # K1 近平守成（rollout 段同规则）：rollout 最优对
                    # identity 边际 < τ×|identity| → 回落守成点。
                    if best_key != identity_key \
                            and identity_key in aggregates:
                        iv = float(aggregates[identity_key])
                        bv = float(aggregates[best_key])
                        gate = _select.IDENTITY_TIEBREAK_TAU * max(
                            1.0, abs(iv))
                        if bv - iv < gate:
                            record["rollout_identity_tiebreak"] = round(
                                bv - iv, 1)
                            record["identity_tiebreak_rollout"] = True
                            best_key = identity_key
                    record["rollout_best"] = best_key
                    if best_key != proj_best:
                        record["switched"] = True
                    selected_key = best_key
            else:
                record["policy"] = "projector_only"

            # —— 注入（快照先行；幂等绝对值写入）——
            spec_by_key = {s.key(): s for s in candidates}
            chosen = spec_by_key[selected_key]
            chosen_overrides = _plans.plan_to_knob_overrides(chosen)
            keys = governed_keys(chosen)
            if "_DTSP_PRISTINE_SNAPSHOT" not in ns:
                ns["_DTSP_PRISTINE_SNAPSHOT"] = take_pristine_snapshot(
                    ns, keys)
            apply_overrides(ns, chosen_overrides)
            ns["_DTSP_LAST_PLAN_KEY"] = selected_key
            _STATE["dawn_cache"][cache_key] = {
                "plan": selected_key, "overrides": chosen_overrides}
            record["selected"] = selected_key
        except Exception as exc:              # noqa: BLE001 —— fail-open 一道
            record["policy"] = "failopen"
            record["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            record["elapsed_s"] = round(_now() - t_start, 4)
            if len(_TRACE["dawns"]) < int(_cfg(config, "trace_cap")):
                _TRACE["dawns"].append(record)
        return None
    except Exception:                          # noqa: BLE001 —— 兜底 fail-open
        _fail_open(ns, traceback.format_exc(limit=3))
        return None


def _fail_open(ns, reason):
    """三道 fail-open 的落点：恢复 v13.8 原值 + 旗关（粘性）+ 遥测记因。"""
    restore_pristine(ns)
    _STATE["sticky_off"] = True
    if len(_TRACE["failopens"]) < 16:
        _TRACE["failopens"].append(reason.strip().splitlines()[-1][:200])
