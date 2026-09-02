# ===========================================================================
# 【中文·模块导览】src/strategy.py —— L1 宏观计划层（branch plan v1.3 宿主）
# ---------------------------------------------------------------------------
# v10.9 保留件：_decide_mode 三模式门控（DEFENSIVE/VOLUME_CROP/SCALE_RANCH
#   + 默认关闭 WHEAT_FARM）、_plan_rollout 偿付能力否决（只否决不放宽，
#   r5-P5 实测 -312.8k 教训）、目标函数族、_field_alloc 田地分配、fail-closed
#   与每日缓存。opp_contesting 已按用户裁决移除（§9-⑦，W1 波）。
# branch v1.3 落地件（W1 波 2026-09-02 + W2 完善波）：
#   §2/§4 阶段寄存器 _stage_plan（P0-P5）+ 分类器（burst/reduced/deferred/
#     melon_first，d1 检查点冻结）+ B1/B3 旋钮 + d6 五问检查点 + _MIXED_PLAN；
#   §5.3 容量门 _capacity_gate（定律 24×(1+H)×0.75/2.4，>0.85 拒购）+
#     LINE_CAPS 分线封顶包络（莓42/麦99/畜14=现值零行为差；瓜 12→6 需单
#     变量消融另排——V-T9 回归证据仍钉 12）+ 黎明不变式下界补线
#     _attach_backfill（util<0.65 → 兜底小麦线扩容，富线候选留后续）；
#   §5.4 曲线门 _curve_gate_ok / 现金门 _cash_gate_ok（计算落位在市场层
#     买点，market.py）；§8.1 d14 冻结守卫（frozen 后禁翻回宽田类）；
#   §8.2 熔断回退 _fuse_check（钱包<300 或当日逃亡 → 段内降 DEFENSIVE
#     运转参数包 + 计数进阶段寄存器/遥测）；
#   §9.1 检查点全席：d1（分类冻结）/d6（五问 C 分支）/d10（SE 窗就绪）/
#     d14（结构冻结快照）/d22（P4 est_opp_held 前置快照）。
# 延后项（单变量纪律，见 JOURNAL）：B1 全速追平步速、B2 d1 草莓探针+NE
#   即铺、B3 瓜 d3-5 小批、容量定律系数回填（M1 三锚定标已落盘）。
# ===========================================================================
_WHEAT_FARM_PLAN = None


def _wheat_farm_plan():
    """Build the opt-in plan from current module knobs for local scans."""
    return {
        "mode": "WHEAT_FARM", "volume": False, "scale": False,
        "wheat_farm": True,
        "straw_quad_cap": WHEAT_FARM_STRAW_CAP,
        "straw_total_cap": WHEAT_FARM_STRAW_CAP,
        "wheat_money_quad": 0,
        "wheat_total_cap": WHEAT_FARM_WHEAT_CAP,
        "herd_ceiling": WHEAT_FARM_HERD_FLOOR,
        "feed_max_price": WHEAT_FARM_FEED_MAX_PRICE,
    }


def _wheat_farm_entry_ok(day, mine, opp, prices, demand, prev_mode=None):
    """Fail-closed public-state gate for the opt-in wheat economy."""
    if prev_mode == "WHEAT_FARM":
        return (day <= PLANT_LAST_DAY["WHEAT"]
                and mine["herd"] >= WHEAT_FARM_ENTRY_HERD_MIN
                and mine["money"] >= WHEAT_FARM_HOLD_CASH
                and _get(prices, "WHEAT", BASE_PRICE["WHEAT"]) <=
                    WHEAT_FARM_FEED_MAX_PRICE)
    if not WHEAT_FARM_ENTRY_START <= day <= WHEAT_FARM_ENTRY_END:
        return False
    if mine["herd"] < WHEAT_FARM_ENTRY_HERD_MIN or \
            mine["money"] < WHEAT_FARM_CASH_REDLINE:
        return False
    if mine["wheat"] < WHEAT_FARM_ENTRY_WHEAT_MIN:
        return False
    wheat_price = _get(prices, "WHEAT", BASE_PRICE["WHEAT"])
    if wheat_price > WHEAT_FARM_FEED_MAX_PRICE:
        return False
    if opp is not None and opp["wheat"] > WHEAT_FARM_OPP_WHEAT_MAX:
        return False
    # A wheat shop draw plus the town center is the minimum observable
    # absorption needed before committing to the 28-32 tile line.
    return demand.get("WHEAT", 1) >= 2


# Keep a discoverable baseline object for local tests; selection uses the
# factory above so a scanner can vary one WHEAT_FARM knob per fresh module.
_WHEAT_FARM_PLAN = _wheat_farm_plan()



# ---- r5-P5 rollout evaluator ----------------------------------------------
# 【中文】r5-P5 展望评估器（_plan_rollout 用）：把候选计划按引擎自身
# 规则逐日前推，检查两件事才允许"拓宽"——
#   * 偿付能力 SOLVENCY：资金路径永不低于饲料/雇工安全线；
#   * 价值 VALUE：终局价值（已入账现金 + 未变现产量，按曲线投影价）
#     必须比 DEFENSIVE 框架高出 ROLLOUT_MIN_EDGE，而非孤立地看为正。
# 注意 VOLUME_ANTICIPATED_ENTRY = False：配对消融实测该"预判入场"
# 36 格灾难级 -312.8k（日级模型看不见对手供给响应），已禁用——此评估
# 器只作额外否决（veto），绝不放宽入场条件。
# The P4 ablations showed WHY a static widening gate fails: a wide template
# fired on a price snapshot either bankrupted the ranch line (-62k/-93k
# spirals: capex ate the feed/hire budget) or crashed its own curve
# (20u/day of strawberry into 4/day of absorption).  The evaluator rolls
# the candidate plan forward day by day with the engine's own rules and
# the embedded price curves and checks two things before widening:
#   * SOLVENCY -- the cash path never dips below the feed/hire security
#     line (spends are modelled the way the executor actually spends:
#     money-gated, self-limited);
#   * VALUE -- the terminal value (banked cash + unmonetized production,
#     at curve-projected prices under the P2 dump-rate limiter and a
#     labour-capacity constraint) must beat the DEFENSIVE frame by an
#     edge, not merely look positive in isolation.
ROLLOUT_HORIZON = 12       # days simulated forward from the plan decision
ROLLOUT_UTILIZATION = 0.5  # effective action share of 24 turns/worker
ROLLOUT_HAIRCUT = 0.9      # tranche-averaging haircut on projected prices
ROLLOUT_FEED_PRICE = 36    # guardrail buy basis per head/day
ROLLOUT_MIN_EDGE = 2000    # anticipated entry needs this terminal edge
# r5-P5 paired-ablation verdict (r5-p5-probe vs r5-p5-ablation-p4head,
# 36 cells): the rollout-gated ANTICIPATED entry measured catastrophic
# (-312.8k sum, worst cells -48.4k/-38.4k on expansionist/baseline_wheat
# seed 102) -- the day-level model cannot see opponent supply responses,
# the abandoned wheat money-crop line, or real tending capacity, so it
# approved entries that crash in play.  DISABLED until an evaluator with
# execution fidelity + opponent scenarios clears the same ablation.
VOLUME_ANTICIPATED_ENTRY = False


# 【中文】规划目标函数组——"建设多大规模"：
#   _wheat_cap   小麦饲料底仓规模（开局 16 格起步、满栏 18 格；麦价
#                35+/42+ 时按榜首自适应份额扩种——贵麦年景小麦本身
#                就是金钱作物，log 曲线不会崩）；
#   _herd_target 畜群总量计划（d0=4 开局爆发，d5 起加速让 12 头期限
#                落在 d6-8、14 头封顶 d8——胜者档 13-17 头的实测形态）；
#   _hands_target/_crew_target 雇工计划（m3 阶梯为地板，畜群 ≥12 时
#                顶到 12 人；VOLUME 模式抬到 15 并加大田地板 12+2）；
#   _animal_pace 当日确认购买步速（开局资本期 1/天 → 爬坡 2 → 后期 3）。
def _wheat_cap(day, wheat_price=25):
    """Wheat FEED-FLOOR size (m2b base values, test-pinned at 25/40): 16
    tiles fund the opening, 18 the full herd (18 fertilized tiles =
    21.6 wheat/day vs 10 animals eating 10).  Dear-wheat bands follow the
    rank-1 adaptive share (crop_rotator ladder 0.32/0.45/0.62 of a 3-quad
    field at 30/36/42 coins -- measured seed-102 economy: five wheat shops,
    wheat 33-45 all season, log curve = no crash risk): at 42+ wheat IS
    the money crop.  With FM-O3 the floor never has to cover the whole
    field: rotation crops take the remaining tiles.
    """
    cap = 16 if day <= 2 else 18
    if day > 2 and wheat_price >= 42:
        cap += 12
    elif day > 2 and wheat_price >= 35:
        cap += 4          # dear wheat: farm more of it (feed margin + cash)
    return min(cap, 30)


def _herd_target(day, feed_capacity):
    """Total-animal plan (m2b formula shape, test-pinned at d0/d8/d25):
    4 head on day 0 (the r3 opening burst), the build accelerates from
    day 5 so the 12-head deadline lands by d6-8 and the 14 ceiling by d8
    (R3-2: winners 13-17 by d8-11; top-20 med 12 by d6; the m3 plan never
    reached 12).  Feed capacity caps it as in m2b, though in r3 the
    autarky bound is normally slack (FM-O3 guardrailed external feed
    covers the gap) -- the money gate + daily pace + composition do the
    real limiting.
    """
    return min(HERD_CAP, 4 + day + max(0, day - 4), max(4, feed_capacity))


def _hands_target(day, herd, wheat_tiles, quads=3):
    """Labour plan (FM-O2): top-20 median 9.4 hires/day, leader 9.7-9.9
    (Crop Dusta labour series; our m2 engine ran 4.07 and lost the labour
    race -- fields went untended and weeded at 5 units).  Flat ramp to 10
    by day 12.  (A quadrant-scaled plan was measured WORSE: our rotation
    opening needs the full crew before the second quadrant exists.)
    """
    target = 2
    for from_day, hands in HANDS_RAMP:
        if day >= from_day:
            target = hands
    return max(2, min(target, 10))


def _crew_target(day, herd, wheat_tiles, quads=3, plan=None):
    """R3-4 crew plan: the m3 ramp above stays the FLOOR, and the crew
    follows the herd up to HANDS_CAP_R3 once the ranch plan needs it
    (round-2 winners hold 12 hands from d7-11 while milking 13-17 head;
    CARE + FEED + COLLECT_FERTILIZER all scale with head count).  A bad
    season (small herd) never overhires: the ramp alone is the target.
    r5-P4: VOLUME_CROP lifts the ceiling to MODE_CREW_CAP_VOL and adds a
    wide-field floor (12 + 2: the 42-tile strawberry field is a second
    daily water/harvest queue independent of the ranch ops); DEFENSIVE
    keeps the r4 formula exactly.
    """
    cap = MODE_CREW_CAP_VOL if plan is not None and plan["volume"] \
        else (plan.get("crew_cap", HANDS_CAP_R3)
              if plan is not None else HANDS_CAP_R3)
    floor = max(_hands_target(day, herd, wheat_tiles, quads), herd)
    if plan is not None and plan["volume"]:
        floor = max(floor, 12) + 2
    return min(cap, floor)


def _animal_pace(day):
    """Confirmed-purchase pace: 1/day through the capital-heavy opening,
    2/day while the herds ramp, 3/day later (m2b shape)."""
    for from_day, pace in ANIMAL_PACE:
        if day >= from_day:
            return pace
    return 1


def _new_animal_production_evenings(day, animal):
    """Engine-exact production evenings for an animal placed today."""
    spec = ANIMALS[animal]
    first = day + spec["first_yield_day"] - 1
    if first > PROD_HORIZON_DAY:
        return 0
    return 1 + (PROD_HORIZON_DAY - first) // spec["interval"]


# 【中文】NPV 扩栏决策组（r4-P3）：14 头计划完成后的额外购买必须同时
# 满足——① 日历：剩余生产夜晚 × 每晚毛利 > 购入成本 + 饲料开销；② 市
# 场：城镇吸收 ≥ 该物种新增流速的 2 倍（绝不向吃不掉的市场扩产）；③ 饲
# 料：小麦系统覆盖更多牲口；④ 现金安全由调用方的资金门控兜底。绝对上
# 限 17（SCALE 模式 18）。_npv_herd_decision 返回(有效上限, 最优物种)，
# _npv_herd_ceiling 是其纯上限投影。
def _npv_herd_decision(day, prices, herd_total, species_counts, daily_demand,
                       sys_wheat, plan=None):
    """Return the safe total ceiling and best profitable animal species."""
    ceil_cap = MODE_HERD_CAP_SCALE if plan is not None and plan["scale"] \
        else HERD_CAP_NPV
    if herd_total >= ceil_cap or day > HERD_NPV_LAST_DAY:
        return HERD_CAP, None
    best = None
    for animal in ("COW", "SHEEP"):
        spec = ANIMALS[animal]
        product = spec["product"]
        price = _get(prices, product, BASE_PRICE[product])
        prod_evenings = _new_animal_production_evenings(day, animal)
        margin = price - FEED_BUY_MAX_PRICE - TRAVEL_MU
        npv = prod_evenings * margin - spec["cost"]
        demand = daily_demand.get(product, 1)
        flow = (species_counts.get(animal, 0) + 1) / float(spec["interval"])
        if npv > 0 and margin >= HERD_NPV_MIN_MARGIN and demand >= 2 * flow:
            if best is None or npv > best[0]:
                best = (npv, animal)
    if best is None or (sys_wheat is not None and sys_wheat < herd_total + 4):
        return HERD_CAP, None
    return ceil_cap, best[1]


def _npv_herd_ceiling(day, prices, herd_total, species_counts, daily_demand,
                      sys_wheat, plan=None):
    """r4-P3 marginal-NPV herd ceiling in [herd plan, HERD_CAP_NPV].

    Extra head above the pinned 14-head plan is allowed only when EVERY
    condition holds:
      * calendar: enough production evenings remain to repay the capex
        (evenings * per-evening margin > cost + feed overhead);
      * market: the town can absorb the added flow (demand >= 2x the
        species' projected flow with one more head -- the r4-P2 lesson:
        scaling into an unabsorbed market crashes both sides);
      * feed: the wheat system covers the bigger mouth count;
      * liquidity/cash safety is the caller's (money-gated buy loop).
    r5-P4: SCALE_RANCH lifts the absolute ceiling to MODE_HERD_CAP_SCALE
    (18) under the same five conditions; DEFENSIVE keeps 17.
    Returns the effective total ceiling (14 when NPV says no).
    """
    ceiling, _animal = _npv_herd_decision(
        day, prices, herd_total, species_counts, daily_demand, sys_wheat,
        plan=plan)
    return ceiling


# r5-P4 macro-plan memory, keyed by player id (the framework may exec one
# copy of this file for both seats).  Recomputed on the first turn of each
# day; a backwards clock denotes a new episode and drops persistence.
_PLAN_MEM = {}


# 【中文】日级现金流展望仿真：花钱方式复刻执行器真实行为（资金门控、
# 自限额——雇工按钱包走、种子按钱包批量、SE 只在保护基金之上买），
# 清算方式复刻市场真实清算（P2 限速 2*D+4 下的逐件曲线定价、库容溢出
# 丢弃）。输出两个数：min_cash 资金路径最低点（偿付能力否决线）与
# terminal 终局价值。P4 实测的两类扩产灾难（-62k/-93k 破产螺旋、自崩
# 曲线）会直接表现为这两个数字恶化。排名级模型：牧场价格平坦折价、
# 假设对手不在草莓线上（门控本就要求该线无竞争）。
def _plan_rollout(day, scan, plan, prices, demand, p_straw):
    """r5-P5 day-level cash-flow + labour-capacity rollout of one plan.

    Spends mirror the way the executor actually spends (money-gated and
    self-limited: hires stop at the wallet, seed batches are money-scaled,
    SE fires only above its protected fund); clearing mirrors the way the
    market actually clears (per-unit curve pricing under the P2 dump-rate
    limiter 2*D+4, shed overflow discarded).  The two measured P4 failure
    classes therefore show up as numbers:
      min_cash  the lowest cash the path ever touches (the ranch feed/hire
                security line -- the -62k/-93k spiral class dips under 0)
      terminal  banked cash + unmonetized production at horizon end (a
                wide field shipping into thin absorption crashes its own
                curve and collapses this)
    Ranking-grade by design: ranch prices are haircut flat, the opponent
    is assumed absent from the strawberry line (the gate already requires
    it uncontested), and existing tiles carry their real planting days.
    """
    cash = float(scan["money"])
    herd = int(scan["herd"])
    target = int(plan["straw_total_cap"])
    crew_target = int(plan["crew_cap"])
    ranch_units = (scan["cows"] * 1.5 * _get(prices, "MILK", BASE_PRICE["MILK"])
                   + scan["sheep"] * (4.0 / 3.0)
                   * _get(prices, "WOOL", BASE_PRICE["WOOL"])
                   + scan["geese"] * 2.0
                   * _get(prices, "EGG", BASE_PRICE["EGG"])) * 0.85
    fert_income = herd * 70.0
    feed_price = min(ROLLOUT_FEED_PRICE, _get(prices, "WHEAT", 25))

    plant = {}
    for s in scan["straw_days"]:
        plant[s] = plant.get(s, 0) + 1
    alive = scan["straw"]
    off = _offset_from_price("STRAWBERRY", p_straw)
    d_straw = demand.get("STRAWBERRY", 1)
    sell_cap = 2 * d_straw + 4
    shed_straw = 0
    min_cash = cash
    eff = 1.0
    se_done = False
    t_end = min(day + ROLLOUT_HORIZON, 29)

    for t in range(day, t_end):
        # crew: the executor hires greedily while money - 60 covers the
        # next fib price (the first hands cost almost nothing); the wide
        # crew is billed only as the field actually widens
        crew_t = crew_target
        if plan["volume"]:
            crew_t = min(crew_target, 12 + max(0, alive - 18) // 6)
        crew_eff = 0
        while crew_eff < crew_t and \
                _FIB_CUM[crew_eff + 1] <= max(0.0, cash - 60.0):
            crew_eff += 1
        cash -= _FIB_CUM[crew_eff]
        if t < 28:
            cash -= herd * feed_price
        if alive < target and t <= PLANT_LAST_DAY["STRAWBERRY"] \
                and cash >= 350:
            batch = min(10, target - alive, int((cash - 300) // 100))
            if batch > 0:
                cash -= batch * 100
                plant[t] = plant.get(t, 0) + batch
                alive += batch
        if plan["volume"] and not se_done and scan["quads"] == 3 \
                and SE_DUE_DAY <= t <= SE_BUY_LAST_DAY and cash >= SE_FUND:
            cash -= 4000
            se_done = True

        required = alive * 1.5 + herd * 3.2 + 9.0
        budget = crew_eff * 24 * ROLLOUT_UTILIZATION
        eff = 1.0 if required <= budget else budget / max(1.0, required)

        cash += ranch_units + fert_income
        prod = 2.0 * eff * sum(n for s, n in plant.items()
                               if (t - s) in (10, 12, 14, 16))
        sellable = min(shed_straw + prod, sell_cap)
        shed_straw = min(100.0, shed_straw + prod - sellable)
        off += sellable - d_straw
        price_t = _price_at_offset("STRAWBERRY", off) * ROLLOUT_HAIRCUT
        cash += sellable * price_t
        min_cash = min(min_cash, cash)

    price_h = max(_price_at_offset("STRAWBERRY", off), 5.0) \
        * ROLLOUT_HAIRCUT
    remaining = 0.0
    for s, n in plant.items():
        for pd in (10, 12, 14, 16):
            if s + pd >= t_end:
                remaining += n * 2.0
    terminal = cash + (shed_straw + remaining * eff) * price_h * 0.6
    return {"min_cash": min_cash, "terminal": terminal, "alive": alive,
            "eff": eff}


# 【中文】═══ 每日模式门控（宏观计划层的核心）═══
# 全部阈值追溯到 round-3 台账或 m1 语料，无任何在线学习。判定顺序：
#   ① WHEAT_FARM（若启用）：_wheat_farm_entry_ok 门控；
#   ② VOLUME_CROP 入场：day 6-12 ∧ 草莓价 ≥105 ∧ 城镇吸收 ≥4/天
#      ∧ 对手草莓 <12 格（作物型对手是"禁止镜像"信号——镜像触发实测
#      严格为负，联合过剩会双崩）∧ 现金 ≥800 ∧ 畜群就绪 ≥10 头
#      （v7.2-V1 破产级教训：~4800 扩产 capex 只能落在已建成的牧场
#      地板上）；已有 ≥6 格活草莓（已验证产线）时叠加展望偿付否决
#      min_cash ≥ 0。"预判入场"分支已被 r5-P5 消融禁用（默认 False）。
#      续期：前一日 VOLUME ∧ 价 ≥40 ∧ 现金 ≥300。
#   ③ SCALE_RANCH 入场：day 4-16 ∧ 14 头计划已建 ≥12 ∧ 奶或毛线
#      清过死价地板且有吸收——对手灌满作物线时的反向市场姿态。
#      续期：前一日 SCALE ∧ 活畜 ≥14。
#   ④ 否则/任何异常：DEFENSIVE（保守 r4 框架，永不抛异常）。
def _decide_mode(obs, day, prev_mode):
    """Deterministic daily mode gate (r5-P4/P5).  Every threshold traces
    to the round-3 ledger or the m1 corpus; nothing is learned online.

    VOLUME: the base conjunction is premium bid (>= 105) + real
    absorption (>= 4/day draws) + free line (opponent's strawberry field
    < 12 tiles -- a crop-heavy opponent is a DO-NOT-MIRROR signal: the
    paired ablation measured the mirror trigger strictly negative, joint
    glut crashes both sides) + cash >= 800 + HERD READINESS (>= 10 head:
    v7.2-V1, the seed-103 bankruptcy class -- the wide field's ~4800
    capex may only land on a finished ranch floor, never on the 4-5-head
    opening that still owes the herd its own build).  On top of the conjunction:
      * proven line (>= 6 alive tiles): the _plan_rollout acts as a
        SOLVENCY VETO (min_cash >= 0) -- the measured -62k/-93k spiral
        class must never fire;
      * anticipated entry (day <= 10, no proof yet): DISABLED by the
        r5-P5 paired ablation (rollout-approved entries measured
        -312.8k over 36 cells; the flag documents the machinery).
    Hold: price >= 40 and cash >= 300; the P2 zero-absorption cut-loss
    gates handle a curve that dies under later opponent supply.
    SCALE entry (day 4-16): the 14-head plan is built (>=12 placed) and a
    dairy/wool line clears its demand-conditioned dead-price floor --
    the counter-market posture when the opponent floods the crop lines.
    Hold while >=14 head stay alive.
    """
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    town_shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    demand = _town_daily_demand(town_shops)
    farms = _get(obs, "farms", []) or []
    player = _get(obs, "player", 0)
    if not 0 <= player < len(farms):
        return dict(_DEFENSIVE_PLAN)
    mine = _farm_scan(farms[player])
    opp = None
    for i, f in enumerate(farms):
        if i != player:
            opp = _farm_scan(f)
            break

    p_straw = _get(prices, "STRAWBERRY", BASE_PRICE["STRAWBERRY"])
    d_straw = demand.get("STRAWBERRY", 1)
    # branch plan §9-⑦ (user ruling 2026-09-02): opp_contesting removed from
    # the VOLUME entry -- mirroring is ACCEPTED as a timing war (sell-ahead
    # via the production calendar), not avoided; solvency veto stays.
    if V9_WHEAT_FARM_ENABLED and _wheat_farm_entry_ok(
            day, mine, opp, prices, demand, prev_mode):
        return _wheat_farm_plan()
    # P4's money >= 800 floor stays THE gate on the proven path: the
    # r5-p5-final ablation measured that substituting the rollout's
    # min_cash for it (money >= 300) re-opened early thin-wallet entries
    # and cost -127.8k over 36 cells -- the model's solvency check is
    # WEAKER than the crude cash floor it tried to replace.  The rollout
    # is an ADDITIONAL veto, never a relaxation.
    base_ok = (6 <= day <= 12 and p_straw >= 105 and d_straw >= 4
               and mine["money"] >= 800
               and mine["herd"] >= VOLUME_HERD_FLOOR)
    if base_ok:
        r_vol = _plan_rollout(day, mine, _VOLUME_PLAN, prices, demand,
                              p_straw)
        if mine["straw"] >= 6:
            # proven line + solvent rollout: enter (P4 semantics with a
            # safety net for pathological states the floor cannot see)
            if r_vol["min_cash"] >= 0:
                return dict(_VOLUME_PLAN)
        elif VOLUME_ANTICIPATED_ENTRY and day <= 10:
            # anticipated entry (the online-band ticket: be in the line by
            # d8-10, not after proof at d14): solvency AND a terminal
            # value edge over the DEFENSIVE frame under curve pricing
            r_def = _plan_rollout(day, mine, _DEFENSIVE_PLAN, prices,
                                  demand, p_straw)
            if r_vol["min_cash"] >= 0 and \
                    r_vol["terminal"] >= r_def["terminal"] + ROLLOUT_MIN_EDGE:
                return dict(_VOLUME_PLAN)
    volume_hold = prev_mode == "VOLUME_CROP" and p_straw >= 40 \
        and mine["money"] >= 300
    if volume_hold:
        return dict(_VOLUME_PLAN)

    p_milk = _get(prices, "MILK", BASE_PRICE["MILK"])
    p_wool = _get(prices, "WOOL", BASE_PRICE["WOOL"])
    animal_ok = ((p_milk >= DEAD_PRICE_FLOOR["MILK"]
                  and demand.get("MILK", 1) >= 2)
                 or (p_wool >= DEAD_PRICE_FLOOR["WOOL"]
                     and demand.get("WOOL", 1) >= 2))
    scale_entry = 4 <= day <= 16 and mine["herd"] >= 12 and animal_ok
    scale_hold = prev_mode == "SCALE_RANCH" and mine["herd"] >= 14
    if scale_entry or scale_hold:
        return {"mode": "SCALE_RANCH", "volume": False, "scale": True,
                "straw_quad_cap": 20,  # V-T9: the NE block wants 18-20
                "straw_total_cap": 24,   # V-T9 tetsuya copy: 18 -> 24
                "wheat_money_quad": WHEAT_MONEY_CAP_PER_QUAD,
                "crew_cap": HANDS_CAP_R3,
                "herd_ceiling": MODE_HERD_CAP_SCALE}
    return dict(_DEFENSIVE_PLAN)


# 【中文】每日计划缓存：每天第一回合算一次模式并缓存整天；门控内部任
# 何异常都回退 DEFENSIVE（fail-closed）；时钟倒退=新对局自动重置。
def _macro_plan(player, obs, day):
    """Cached daily macro plan (first turn of the day decides; the plan
    failure path is the r4 DEFENSIVE frame, never an exception)."""
    st = _PLAN_MEM.get(player)
    if st is not None and st["day"] == day:
        return st["plan"]
    prev_mode = None
    if st is not None and day > st["day"] >= 0:
        prev_mode = st["plan"].get("mode")
    try:
        plan = _decide_mode(obs, day, prev_mode)
    except Exception:
        plan = dict(_DEFENSIVE_PLAN)
    # branch plan v1.3 landing: stage register + B/C branch knobs ride on
    # the plan dict (additive keys only; every consumer reads .get()).
    try:
        plan = _stage_plan(player, obs, day, plan)
    except Exception:
        plan = dict(plan)
        plan["stage"] = _stage_of(day)
    _PLAN_MEM[player] = {"day": day, "plan": plan}
    return plan


# ===========================================================================
# 【中文】branch plan v1.3 落地层（2026-09-02 实装）
# ---------------------------------------------------------------------------
# 阶段寄存器 §2 / 对手开局分类器 §4.1 / d6 五问检查点 §5.1 / 容量门 §5.3 /
# 三重前置检查 §5.4 / _MIXED_PLAN（C2 DevilQ 混合，§5.2）。
# 设计约束：全部纯公开状态、确定性、fail-closed；行为接线经 plan dict 旋钮
# （p1_species_pref / melon_min / straw_early_claim），执行层照旧消费。
# ===========================================================================

# ---- C2 混合计划（DevilQ 96.6k 结构 × §5.3 分线封顶）----
_MIXED_PLAN = {"mode": "MIXED", "volume": False, "scale": True,
               "wheat_farm": False,
               "straw_quad_cap": 12,          # 33 格 / 3 象限
               "straw_total_cap": 33,          # DevilQ 33 莓（<Renji 42，
                                                # 奶年金对冲作物线）
               "wheat_money_quad": 4,
               "crew_cap": 11,                 # §5.3 初算 C2≈77 单位→10-11
               "herd_ceiling": 14,             # 14 头 = 28 资产单位（对冲主体）
               "melon_total_cap": LINE_CAPS["MELON"],  # §5.3 封顶 6（吸收
                                                # 优先于 DevilQ 原版 21 格）
               }

_STAGE_MEM = {}


def _stage_of(day):
    """P0-P5 阶段判定（branch §2 总表，纯日期函数）。"""
    if day <= 0:
        return "P0"
    if day <= STAGE_P1_DUE - 1:
        return "P1"
    if day <= STAGE_P2_FREEZE:
        return "P2"
    if day <= STAGE_P3_END:
        return "P3"
    if day <= STAGE_P4_END:
        return "P4"
    return "P5"


def _classify_opponent_opening(obs):
    """对手开局分类器（branch §4.1 v1.3 更新版，d1 晨可判，纯公开状态）。

    返回 burst / reduced / deferred / melon_first / unknown。
    """
    farms = _get(obs, "farms", []) or []
    player = _get(obs, "player", 0)
    opp = None
    for i, f in enumerate(farms):
        if i != player:
            opp = f
            break
    if opp is None:
        return "unknown"
    scan = _farm_scan(opp)
    if scan["herd"] >= OPP_CLASS_BURST_MIN:
        return "burst"
    if scan["herd"] >= OPP_CLASS_REDUCED_RANGE[0]:
        return "reduced"
    melon = 0
    for row in _get(opp, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT" \
                    and _get(tile, "crop", "") == "MELON":
                melon += 1
    if melon >= OPP_CLASS_MELON_MIN:
        return "melon_first"
    if scan["wheat"] >= OPP_CLASS_DEFERRED_WHEAT:
        return "deferred"
    return "unknown"


def _capacity_units(farm, private=None):
    """当前资产单位（容量定律分母）：莓/麦/瓜格=1，萝卜=0.5，头=2。"""
    comps = {"straw": 0, "wheat": 0, "melon": 0, "carrot": 0, "herd": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "PLANT":
                crop = _get(tile, "crop", "")
                if crop == "STRAWBERRY":
                    comps["straw"] += 1
                elif crop == "WHEAT":
                    comps["wheat"] += 1
                elif crop == "MELON":
                    comps["melon"] += 1
                elif crop == "CARROT":
                    comps["carrot"] += 1
            elif "animal" in tile:
                comps["herd"] += 1
    units = float(comps["straw"] + comps["wheat"] + comps["melon"]
                  + 0.5 * comps["carrot"] + 2 * comps["herd"])
    return units, comps


def _capacity_law_max(hands):
    """容量定律上界：24×(1+H)×CAP_UTIL÷CAP_TURNS_PER_UNIT（§5.3）。"""
    return 24.0 * (1 + max(0, int(hands))) * CAP_UTIL / CAP_TURNS_PER_UNIT


def _capacity_gate(farm, private=None, delta_units=0.0, day=None, plan=None):
    """三重前置检查·劳动力维（§5.3/§5.4）。

    返回 (ok, util)。ok=False 表示买后单位数超定律×CAP_USE_MAX——
    策略层应拒绝该 capex（黎明不变式：>0.85 拒购，<0.65 报 slack 补线）。
    劳力先行（§5.3 规则 1）：带 day 调用时按当日计划雇工评估——
    farm.hands 是昨日快照，黎明雇工在资产采购之前落地。
    """
    hands = len(_get(farm, "hands", []) or [])
    units, comps = _capacity_units(farm, private)
    if day is not None:
        planned = _crew_target(
            day, comps["herd"], comps["wheat"],
            len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]),
            plan)
        hands = max(hands, planned)
    cap = _capacity_law_max(hands)
    util = (units + delta_units) / cap if cap > 0 else 0.0
    return (util <= CAP_USE_MAX, util)


def _curve_gate_ok(item, player, day, prices):
    """三重前置检查·曲线维（§5.4）：投影价 ≥ 地板（升级自运行时死价红线，
    投影替代现货快照——"现在 95、3 天后 80"的线现在能看见）。"""
    if day < DEAD_PRICE_FROM_DAY:
        return True
    floor = DEAD_PRICE_FLOOR.get(item)
    if floor is None:
        floor = CROP_FLOOR.get(item)
    if floor is None:
        return True
    price = _get(prices, item, BASE_PRICE.get(item, 0))
    if price < floor:
        return False
    st = _MARKET_MEM.get(player) or {}
    # freshness window: yesterday-or-today EMA is the designed trend signal;
    # anything older or from the future is cross-episode noise -> ignored.
    flow = 0.0
    if day - 1 <= st.get("day", -10) <= day + 1:
        flow = (st.get("flow", {}) or {}).get(item, 0.0)
    proj = _project_price(item, price, flow, SELL_PLAN_LOOKAHEAD_DAYS)
    return proj >= floor


def _cash_gate_ok(farm, projected_spend=0.0):
    """三重前置检查·现金维（§5.4 黎明现金流不变式）：

    投影日终钱包 ≥ 次日黎明 crew fib 账单 + LIQUIDITY_FLOOR（饲料裕量
    已并入该常量语义——m2b 破产类的保险丝，v1.1 迁移裁决）。
    """
    money = _get(farm, "money", 0.0)
    hands = len(_get(farm, "hands", []) or [])
    next_bill = _FIB_CUM[hands] if hands < len(_FIB_CUM) else 0
    return (money - float(projected_spend)) >= (next_bill + LIQUIDITY_FLOOR)


def _first_market_day(farm, day):
    """本农场首个草莓上市日（planted+9；无格则 None）——首市日 KPI 输入。"""
    best = None
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT" \
                    and _get(tile, "crop", "") == "STRAWBERRY":
                ev = _get(tile, "planted_day", day) + \
                    CROPS["STRAWBERRY"]["first_yield_day"] - 1
                best = ev if best is None else min(best, ev)
    return best


def _d6_checkpoint(obs, day):
    """d6 五问检查点（branch §5.1）。返回 (questions, c_branch)。

    c_branch: "C1"（五问全过，宽田候选——仍须 _decide_mode 的价格/吸收/
    solvency 门）/ "C2"（草莓线弱或首市日落后但奶线活 → 混合）/
    "C3"（作物线全弱 → 畜牧）。
    """
    farms = _get(obs, "farms", []) or []
    player = _get(obs, "player", 0)
    farm = farms[player] if 0 <= player < len(farms) else None
    opp = None
    for i, f in enumerate(farms):
        if i != player:
            opp = f
            break
    if farm is None:
        return {"q1": False, "q2": False, "q3": False, "q4": False,
                "q5": False}, "C3"
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    demand = _town_daily_demand(shops)
    mine = _farm_scan(farm)
    q1 = mine["herd"] >= VOLUME_HERD_FLOOR
    q2 = mine["money"] >= 800
    p_straw = _get(prices, "STRAWBERRY", BASE_PRICE["STRAWBERRY"])
    q3 = p_straw >= 105 and demand.get("STRAWBERRY", 1) >= 4
    # q4 首市日 KPI：我方（含当日可种）≤ 对手（无格视为 +inf）
    our_first = _first_market_day(farm, day)
    if our_first is None and day <= PLANT_LAST_DAY["STRAWBERRY"]:
        our_first = day + CROPS["STRAWBERRY"]["first_yield_day"] - 1
    opp_first = _first_market_day(opp, day) if opp is not None else None
    q4 = (our_first is not None) and (opp_first is None
                                      or our_first <= opp_first)
    # q5 容量问：VOLUME 目标单位数 ≤ 定律 × 0.85
    hands = len(_get(farm, "hands", []) or [])
    target_units = 42 + 12 + 2 * mine["herd"]  # 莓42+麦12+畜群（§5.3 C1 初算）
    q5 = target_units <= _capacity_law_max(max(hands, 12)) * CAP_USE_MAX
    questions = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
    p_milk = _get(prices, "MILK", BASE_PRICE["MILK"])
    p_wool = _get(prices, "WOOL", BASE_PRICE["WOOL"])
    dairy_alive = (p_milk >= DEAD_PRICE_FLOOR["MILK"]
                   and demand.get("MILK", 1) >= 2) or \
                  (p_wool >= DEAD_PRICE_FLOOR["WOOL"]
                   and demand.get("WOOL", 1) >= 2)
    if q1 and q2 and q3 and q4 and q5:
        c_branch = "C1"
    elif q1 and dairy_alive and q5:
        c_branch = "C2"
    elif q1 and dairy_alive:
        c_branch = "C3"
    else:
        c_branch = "C3" if dairy_alive else "C1"
    return questions, c_branch


def _b_branch_adjust(plan, obs, day, st=None):
    """P1 分支调整（branch §4.2）：按对手分类给 plan 挂旋钮，执行层消费。

    分类在 d1 检查点冻结（§9.1：d1 晨对手 d0 分类一次定型，防 P1 内随
    对手施工漂移）；B1 burst：产品分化——YARN_STORE 未解锁则羊线换牛线；
    B2 reduced/deferred/unknown：标准序列（现有路径，零改动）；B3
    melon_first：瓜线最小化（melon_min——我方瓜只 d3-5 小批抢收）。
    """
    cls = (st or {}).get("opp_class_frozen") \
        or _classify_opponent_opening(obs)
    plan = dict(plan)
    plan["opp_class"] = cls
    if cls == "burst":
        shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        if "YARN_STORE" not in shops:
            plan["p1_species_pref"] = "COW"   # 不跟死吸收的毛线挤（§4.2 B1）
    elif cls == "melon_first":
        plan["melon_min"] = True              # §4.2 B3：瓜 d3-5 小批抢收
    return plan


def _stage_state(player, day):
    """Per-player persistent stage register（时钟倒退=新对局→重建）。"""
    st = _STAGE_MEM.get(player)
    if st is None or day < st.get("day", day):
        st = {"day": day}
        _STAGE_MEM[player] = st
    st["day"] = max(st["day"], day)
    return st


def _d1_checkpoint(obs, st):
    """d1 检查点（§9.1）：对手 d0 分类定型并冻结。"""
    st["opp_class_frozen"] = _classify_opponent_opening(obs)
    return st["opp_class_frozen"]


def _d10_checkpoint(farm):
    """d10 检查点（§5.1b SE 窗）：现金 ≥ SE_FUND(4600) 即 SE 就绪。"""
    money = _get(farm, "money", 0.0)
    return {"money": money, "se_ready": money >= SE_FUND}


def _d14_checkpoint(out, st):
    """d14 检查点（§5.1b/§8.1）：结构冻结——快照当前模式，此后禁翻回宽田。"""
    frozen = {"mode": out.get("mode"), "c_branch": st.get("c_branch")}
    st["frozen"] = frozen
    return frozen


def _d22_checkpoint():
    """d22 检查点（§7.5/§4.1）：P4 三档抢跑的 est_opp_held 前置快照。"""
    held = {}
    for item in ("STRAWBERRY", "MILK", "WOOL", "MELON", "WHEAT"):
        value = est_opp_held(item)
        held[item] = None if value is None else round(float(value), 1)
    return {"day": 22, "held": held}


def _fuse_check(st, farm, mine, stage):
    """§8.2 熔断回退：段内钱包 < FUSE_MONEY_FLOOR 或牲畜逃亡（畜群数只降
    不升——引擎无卖畜，减少即逃亡）→ 本阶段余下天降 DEFENSIVE 运行参数包；
    逐段计数（阶段切换重置 active）。"""
    escaped = (st.get("herd_prev") is not None
               and mine["herd"] < st["herd_prev"])
    st["herd_prev"] = mine["herd"]
    fuse = st.get("fuse") or {}
    tripped = _get(farm, "money", 0.0) < FUSE_MONEY_FLOOR or escaped
    if tripped and stage in ("P1", "P2", "P3", "P4"):
        if not fuse.get("active") or fuse.get("stage") != stage:
            fuse = {"count": int(fuse.get("count", 0)) + 1,
                    "stage": stage, "active": True, "escaped": bool(escaped)}
        else:
            fuse["escaped"] = fuse.get("escaped") or bool(escaped)
        st["fuse"] = fuse
    elif fuse.get("stage") == stage:
        fuse["active"] = False
    return bool((st.get("fuse") or {}).get("active")), bool(escaped)


def _attach_backfill(out, farm, day, st=None):
    """黎明不变式下界（§5.3）：util < CAP_USE_MIN → 补线候选按单位日收入
    降序（奶/毛 > 莓 > 瓜 > 萝卜 > 麦）；本轮只接线兜底小麦线（富线需
    三重门+市场耦合，留后续单变量步）。记录入阶段寄存器供遥测。"""
    if farm is None or out.get("fused"):
        return out
    _ok, util = _capacity_gate(farm, None, day=day, plan=out)
    if util >= CAP_USE_MIN:
        if st is not None:
            st["backfill"] = None
        return out
    units, _comps = _capacity_units(farm)
    law = _capacity_law_max(len(_get(farm, "hands", []) or []))
    room = int(law * CAP_USE_MIN - units)
    if room <= 0:
        if st is not None:
            st["backfill"] = None
        return out
    out["capacity_backfill"] = {"util": round(util, 3), "room_units": room,
                                "line": "WHEAT",
                                "candidates": ["DAIRY", "STRAWBERRY",
                                               "MELON", "CARROT", "WHEAT"]}
    if st is not None:
        st["backfill"] = {"room_units": room, "line": "WHEAT"}
    return out


def stage_state_snapshot(player):
    """Read-only stage-register getter（遥测/诊断消费）。"""
    st = _STAGE_MEM.get(player) or {}
    fuse = st.get("fuse") or {}
    return {"c_branch": st.get("c_branch"),
            "opp_class": st.get("opp_class_frozen"),
            "fused": bool(fuse.get("active")),
            "fuse_events": int(fuse.get("count", 0)),
            "frozen": st.get("frozen"),
            "backfill": st.get("backfill")}


def _stage_plan(player, obs, day, plan):
    """阶段×分支选择器（branch §2/§4/§5/§8 的组装点）。

    P1（d1-5）：d1 检查点冻结对手分类 + B 分支旋钮；P2（d6-14）：d6 五问
    C 分支裁决（缓存）+ d10 SE 窗就绪记录 + d14 结构冻结快照 + MIXED 注入
    （C2）+ 黎明不变式下界补线；P3/P4：冻结守卫（§8.1，frozen 后禁翻回宽
    田类）+ 补线 + d22 P4 前置快照；全程 §8.2 熔断回退（段内钱包<300 或
    逃亡 → DEFENSIVE 运行参数包）。
    """
    stage = _stage_of(day)
    out = dict(plan)
    out["stage"] = stage
    farms = _get(obs, "farms", []) or []
    farm = farms[player] if 0 <= player < len(farms) else None
    st = _stage_state(player, day)

    fused = False
    if farm is not None:
        mine = _farm_scan(farm)
        fused, _escaped = _fuse_check(st, farm, mine, stage)
        if stage == "P1" and day == 1 and st.get("opp_class_frozen") is None:
            _d1_checkpoint(obs, st)
        if stage == "P2":
            if st.get("decided_day") is None:
                if day == STAGE_P1_DUE:
                    questions, c_branch = _d6_checkpoint(obs, day)
                    st["decided_day"] = day
                    st["c_branch"] = c_branch
                    st["questions"] = questions
                else:
                    st["decided_day"] = day
                    st["c_branch"] = None
                    st["questions"] = None
            if day == 10 and st.get("d10") is None:
                st["d10"] = _d10_checkpoint(farm)
            if day == STAGE_P2_FREEZE and st.get("frozen") is None:
                _d14_checkpoint(out, st)
        if stage == "P4" and day == 22 and st.get("p4_snapshot") is None:
            try:
                st["p4_snapshot"] = _d22_checkpoint()
            except Exception:
                st["p4_snapshot"] = {"day": 22, "held": {}}

    if fused:
        out = dict(_DEFENSIVE_PLAN)
        out["stage"] = stage
        out["fused"] = True

    if stage == "P1":
        return _b_branch_adjust(out, obs, day, st)
    if stage == "P2":
        c_branch = st.get("c_branch")
        out["c_branch"] = c_branch
        if c_branch == "C2" and out.get("mode") == "DEFENSIVE" and not fused:
            # 草莓线弱/首市日落后 + 奶线活：注入 DevilQ 混合计划（§5.2）
            out = dict(_MIXED_PLAN)
            out["stage"] = stage
            out["c_branch"] = c_branch
        return _attach_backfill(out, farm, day, st)
    if stage in ("P3", "P4", "P5"):
        out["c_branch"] = st.get("c_branch")
        frozen = st.get("frozen") or {}
        # §8.1 冻结守卫：d14 时是 DEFENSIVE（窄类）的农场，此后禁止翻回
        # 宽田类（VOLUME/MIXED/SCALE/WHEAT_FARM 的新入场）；退出不受限。
        if frozen.get("mode") in ("DEFENSIVE", None) and not fused \
                and out.get("mode") not in ("DEFENSIVE", None):
            out = dict(_DEFENSIVE_PLAN)
            out["stage"] = stage
            out["c_branch"] = st.get("c_branch")
            out["freeze_guard"] = True
        if stage in ("P3", "P4"):
            _attach_backfill(out, farm, day, st)
        return out
    return out


# 【中文】═══ 结构与轮作规划（规划层核心）═══
# 输出四元组 (builds, crop_map, n_animals, wheat_capacity)：
#   builds   本回合要建的畜舍 {坐标: "PASTURE"/"COOP"}——牧场贴着每个
#            已解锁象限的仓库口成环（曼哈顿距离 ≤ PASTURE_RING），最
#            多超前畜群计划 2 座（FM-1 环形牧场的喂料动线依据）；
#   crop_map 各作物计划地块集合（活株 + 待种）——金钱作物按
#            （物候窗口 ∧ 价格红线 ∧ 象限上限）三门控从最靠近仓库的
#            空格向外 claim；小麦填满剩余至 _wheat_cap 饲料底仓；
#            VOLUME 计划放宽草莓上限至 14/格与 42 总量并扩小麦配额；
#   可回收杂草（v7-W "planned"）排在同类真空格之后：只有当框架真正
#   想要那块地时才规划"先 DIG 后 PLANT"的链条；
#   多余地保持休耕——劳动力才是稀缺资源（surplus tiles stay fallow）。
def _field_alloc(farm, day, prices, plan=None):
    """Deterministic structure + rotation plan (FM-O1/FM-O2).

    Structures: pastures (and one coop) on the manhattan ring
    (dist <= PASTURE_RING) around the shed-access tile of every unlocked
    quadrant, built at most 2 ahead of the herd plan (m2b FM-1).

    Field: money crops claim the empties nearest the shed while their
    (phase, price floor, cap) gates are open -- each gate is the red-line
    freeze for that crop; wheat fills the rest up to the _wheat_cap feed
    floor; surplus tiles stay fallow (labour is the binding resource).
    r5-P4: a VOLUME_CROP plan widens the strawberry ceiling (14/quad,
    42 tiles) and the wheat money-crop quota; DEFENSIVE (plan=None or
    DEFENSIVE) keeps the conservative r4 structure parameters.

    Returns (builds, crop_map, n_animals, wheat_capacity) where
      builds: {(x, y): "PASTURE"|"COOP"} to build,
      crop_map: {crop: set(positions)} planned tiles (alive + to-plant),
      n_animals: animals currently placed,
      wheat_capacity: wheat tiles * 1.2 (fertilized units/day).
    """
    if plan is None:
        plan = _DEFENSIVE_PLAN
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]
    accesses = _shed_access(board, quads)

    existing = {crop: set() for crop in CROPS}
    n_animals = 0
    n_pasture = 0
    n_coop = 0
    pasture_by_quad = {"NW": 0, "NE": 0, "SW": 0, "SE": 0}
    empty_ring, empty_field = [], []
    weed_ring, weed_field = [], []     # v7-W: reclaimable, behind empties
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if _quadrant_of(x, y, board) in quads and \
                        any(_dist(x, y, qx, qy) <= PASTURE_RING
                            for qx, qy in accesses) and \
                        not _shed_adjacent(x, y, board, quads):
                    empty_ring.append(pos)
                elif _quadrant_of(x, y, board) in quads:
                    empty_field.append(pos)
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                # v7-W "none" keeps the v6 skip (tile unplannable); the
                # other modes classify a weed exactly like an empty of the
                # same geometry so the plan can reserve it -- the DIG fires
                # from the planned branch in _build_tasks, never from here.
                if WEED_RECLAIM_MODE != "none" and \
                        _quadrant_of(x, y, board) in quads:
                    if any(_dist(x, y, qx, qy) <= PASTURE_RING
                           for qx, qy in accesses) and \
                            not _shed_adjacent(x, y, board, quads):
                        weed_ring.append(pos)
                    else:
                        weed_field.append(pos)
                continue
            if kind == "PASTURE":
                n_pasture += 1
                pasture_by_quad[_quadrant_of(x, y, board)] += 1
                if "animal" in tile:
                    n_animals += 1
                continue
            if kind == "COOP":
                n_coop += 1
                pasture_by_quad[_quadrant_of(x, y, board)] += 1
                if "animal" in tile:
                    n_animals += 1
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "WHEAT")
                if crop in existing:
                    existing[crop].add(pos)

    empty_ring.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in accesses), p[1], p[0]))
    builds = {}
    field_extra = []
    herd_t = _herd_target(day, 99)
    # V-T8: build lead is at most ONE structure ahead of the herd plan
    # (tetsuya builds batch-by-batch for the incoming animals).
    base_pasture_want = min(HERD_CAP + 1, herd_t + 1)
    pasture_want = plan.get("herd_ceiling", MODE_HERD_CAP_SCALE) \
        if plan.get("scale") else base_pasture_want
    if plan.get("scale"):
        used_structure_slots = set()
        for pos in empty_ring + empty_field + weed_ring + weed_field:
            if n_pasture >= pasture_want:
                break
            builds[pos] = "PASTURE"
            n_pasture += 1
            used_structure_slots.add(pos)
        field_extra = [pos for pos in empty_ring
                       if pos not in used_structure_slots]
        empty_field = [pos for pos in empty_field
                       if pos not in used_structure_slots]
        weed_field = [pos for pos in weed_ring + weed_field
                      if pos not in used_structure_slots]
    else:
        # V-T8 pasture zoning (tetsuya d25 forensics, two games identical:
        # NW 7 pastures hugging the shed access [0,1,1,2,2,2,3] beside the
        # wheat band -- the dairy home; NE only 2-3 at the access mouth so
        # the strawberry block keeps its near tiles; SW 5-6 as a CHAIN
        # [0,1,3,4,5,6] extending outward so the SW wheat field keeps its
        # near cells).  The old every-quadrant uniform ring fought the V-T7
        # crop zoning (NE strawberry lost its best cells, seed-103's NW
        # feed floor was squeezed to 2 wheat tiles by 8 pastures).  Build
        # lead is now at most ONE structure ahead of the herd plan
        # (tetsuya builds d0-3 for the d1-3 animals batch-by-batch; our
        # d0 batch of 5 sat mostly empty).
        planned_by_quad = {"NW": 0, "NE": 0, "SW": 0, "SE": 0}
        for pos in empty_ring + weed_ring:
            pq = _quadrant_of(pos[0], pos[1], board)
            if n_coop < min(HERD_COMPOSITION["GOOSE"], herd_t) and \
                    n_coop + n_pasture < pasture_want + 1:
                builds[pos] = "COOP"
                n_coop += 1
                planned_by_quad[pq] += 1
            elif n_pasture < pasture_want and \
                    pasture_by_quad[pq] + planned_by_quad[pq] < \
                    PASTURE_QUAD_CAP.get(pq, 99):
                builds[pos] = "PASTURE"
                n_pasture += 1
                planned_by_quad[pq] += 1
            else:
                field_extra.append(pos)
        # SW chain extension: if the herd plan still wants structures and
        # the rings are exhausted, the SIDE dairy quadrants may extend into
        # their own field tiles nearest-first (tetsuya's SW [3,4,5,6] tail).
        if n_pasture < pasture_want and (empty_field or weed_field):
            chain = sorted([p for p in empty_field + weed_field
                            if _quadrant_of(p[0], p[1], board) in ("SW", "SE")
                            and _quadrant_of(p[0], p[1], board) in quads],
                           key=lambda p: (min(_dist(p[0], p[1], *q)
                                              for q in accesses), p[1], p[0]))
            for pos in chain:
                if n_pasture >= pasture_want:
                    break
                pq = _quadrant_of(pos[0], pos[1], board)
                if pasture_by_quad[pq] + planned_by_quad[pq] >= \
                        PASTURE_QUAD_CAP.get(pq, 99):
                    continue
                builds[pos] = "PASTURE"
                n_pasture += 1
                planned_by_quad[pq] += 1
            field_extra += [p for p in empty_field if p not in builds]
            empty_field = []
            weed_field = [p for p in weed_field if p not in builds]

    empties = field_extra + empty_field
    empties.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in accesses), p[1], p[0]))
    if weed_field:
        # v7-W: reclaimed field weeds sit behind EVERY real empty, so a
        # weed is planned only when the phase wants more tiles than the
        # free field provides (the DIG-then-PLANT chain costs one day).
        weed_field.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in accesses), p[1], p[0]))
        empties = empties + weed_field
    crop_map = {crop: set(existing[crop]) for crop in CROPS}

    # V-T7 functional zoning (tetsuya d20 forensics, two games: NW = dairy
    # block + wheat, NE = one contiguous strawberry field (18-20 tiles),
    # SW = wheat + side pasture, melon parked at the FAR rim (median shed
    # distance 7-8).  Our old nearest-first order inverted the frequency/
    # distance law: melon sat at median 3 while wheat -- the highest-
    # frequency line (daily water + harvest + the FEED pickup source) --
    # was pushed to the rim at median 6, and strawberry fragmented across
    # NW+NE.  Claim order now: WHEAT nearest-first inside the dairy-side
    # quadrants (NW, then SW), STRAWBERRY one quadrant at a time (NE first,
    # the dairy home quadrant last) so its crew works a contiguous block,
    # MELON from the far rim inward (one-shot, lowest frequency), CARROT
    # nearest-first on whatever remains.
    def _shed_dist(p):
        return min(_dist(p[0], p[1], *q) for q in accesses)

    def _crop_open(crop):
        lo, hi = CROP_PHASE[crop]
        return lo <= day <= hi and \
            _get(prices, crop, BASE_PRICE[crop]) >= CROP_FLOOR[crop]

    def _quad_sorted(qn, reverse=False):
        return sorted((p for p in empties
                       if _quadrant_of(p[0], p[1], board) == qn),
                      key=lambda p: ((-_shed_dist(p)) if reverse
                                     else (_shed_dist(p), p[1], p[0])))

    wheat_room = _wheat_cap(day, _get(prices, "WHEAT", 25)) - len(crop_map["WHEAT"])
    if plan.get("wheat_farm"):
        wheat_room = max(0, min(plan["wheat_total_cap"],
                                WHEAT_FARM_WHEAT_CAP) -
                         len(crop_map["WHEAT"]))
    elif _get(prices, "WHEAT", 25) >= WHEAT_MONEY_GATE:
        wheat_room += plan["wheat_money_quad"] * len(quads)
    backfill = plan.get("capacity_backfill")
    if backfill and backfill.get("line") == "WHEAT" \
            and not plan.get("wheat_farm"):
        # §5.3 黎明不变式下界：idle 容量的兜底去向=小麦（剩余劳力去处；
        # 金钱作物两pass已在后面先 claim，补位只吃真正剩余的空格）
        wheat_room += int(backfill.get("room_units", 0))
    # wheat pass 1: the dairy home quadrant keeps a BAND of near tiles
    # (tetsuya d20: NW holds 12-15 wheat beside the pastures) -- bounded so
    # a single-quadrant farm still leaves the strawberry phase its near
    # cells (the r3 winner band needs 8 strawberry tiles by d11-13).
    wheat_nw_band = min(wheat_room, WHEAT_DAIRY_QUAD_BAND)
    for pos in (_quad_sorted("NW") if "NW" in quads else []):
        if wheat_nw_band <= 0:
            break
        crop_map["WHEAT"].add(pos)
        wheat_nw_band -= 1
        wheat_room -= 1
        empties.remove(pos)

    if _crop_open("STRAWBERRY"):
        # §5.3 分线封顶包络：LINE_CAPS 作跨计划上限（min(计划配额, 封顶)）
        room = min(plan["straw_quad_cap"] * len(quads),
                   plan["straw_total_cap"],
                   LINE_CAPS.get("STRAWBERRY", 99)) \
            - len(crop_map["STRAWBERRY"])
        for qn in (q for q in ("NE", "SW", "SE", "NW") if q in quads):
            if room <= 0:
                break
            for pos in _quad_sorted(qn):
                if room <= 0:
                    break
                crop_map["STRAWBERRY"].add(pos)
                room -= 1
                empties.remove(pos)

    for crop, descending in (("MELON", True), ("CARROT", False)):
        if not _crop_open(crop):
            continue
        if crop == "CARROT" and day < CARROT_ENDGAME_FROM:
            # V-T7: carrot is the ENDGAME rotation (tetsuya plants it
            # d23-27); claiming its 6/quad from d15 let it squat the SW
            # wheat field for 11 days (seed-102 forensics: feed floor
            # squeezed to 5 wheat tiles).
            continue
        # V-T9: the tetsuya melon band YIELDS -- under VOLUME_CROP the
        # 42-tile strawberry field owns the quadrant budgets, and in a
        # dear-wheat season the money-wheat tranche outranks the rim
        # melon (test_wheat_is_feed_floor_and_money_crop regression).
        crop_quad_cap = CROP_CAP_PER_QUAD[crop]
        if crop == "MELON" and (plan.get("volume") or
                                _get(prices, "WHEAT", 25) >= WHEAT_MONEY_GATE):
            crop_quad_cap = 3
        room = crop_quad_cap * len(quads) - len(crop_map[crop])
        if crop == "CARROT":
            # §5.3 分线封顶包络（萝卜终盘弹性线；瓜带收紧 12→6 需单变量
            # 消融另排——V-T9 回归证据仍钉 12，见 JOURNAL）
            room = min(room, max(0, LINE_CAPS.get("CARROT", 99)
                                 - len(crop_map[crop])))
        if crop == "MELON":
            # V-T9 fix: tetsuya's melon rim lives in the UPPER quadrants
            # (his SW is the wheat side field -- our far-rim-first filled
            # SW with 17-18 melon and starved the feed floor to 2-4 tiles,
            # -30k self-play).  Cap the season band near his median (12)
            # and prefer the NW/NE rim before the SW one.
            # Phase-C Var2: the 5.3 per-line cap binds (kill_table verified
            # melon absorption = town center only ~1/day)
            room = min(room, max(0, LINE_CAPS.get("MELON", 12)
                                 - len(crop_map[crop])))
        order = sorted(empties, key=lambda p: (
            (0 if crop == "MELON" and
             _quadrant_of(p[0], p[1], board) in ("NW", "NE") else 1),
            ((-_shed_dist(p)) if descending else _shed_dist(p)), p[1], p[0]))
        taken = 0
        for pos in order:
            if taken >= room:
                break
            crop_map[crop].add(pos)
            taken += 1
            empties.remove(pos)

    # wheat pass 2: whatever quota remains goes nearest-first over the rest
    # (SW is the tetsuya side dairy field at 12-13 tiles).
    wheat_rest = sorted(empties, key=lambda p: (_shed_dist(p), p[1], p[0]))
    for pos in wheat_rest:
        if wheat_room <= 0:
            break
        crop_map["WHEAT"].add(pos)
        wheat_room -= 1
        empties.remove(pos)

    capacity = int(len(crop_map["WHEAT"]) * 1.2)
    return builds, crop_map, n_animals, capacity
