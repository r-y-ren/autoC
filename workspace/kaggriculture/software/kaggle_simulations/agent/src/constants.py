# ===========================================================================
# 【中文·模块导览】src/constants.py —— 引擎镜像常量 + 策略旋钮 + 共享基座
# ---------------------------------------------------------------------------
# v10.9 职责：官方引擎 1.32.7 的逐字段镜像（CROPS/ANIMALS/SHOPS/
#   MARKET_PARAMS_EMB 等，离线自主）+ 全部策略旋钮（每个值带实验出典，
#   调参历史见 exports/logs/iteration_gate_log.jsonl）+ 九模块共享的
#   无状态纯工具（_get/_dist/_step_towards/象限与仓口系列）。
# 新架构落位：四份设计文档共用的"物理常数层"。
# 文档符合性审查（2026-09-02，对照四文档）：
#   ✓ 保留资产在场——MARKET_PARAMS_EMB（官方表 99/99 校验镜像）、
#     DEAD_PRICE_FLOOR、LIQUIDITY_FLOOR、CROP_FLOOR、FEED_BUY_MAX_PRICE
#     （market_strategy §1 保留表五项全数存活，产物契约逐字保留）；
#   ✗ 待办——容量定律系数（最大资产单位≈24×(1+H)×0.75÷2.4）与资产
#     单位表（branch §5.3，M1 定标后回填）；_capacity_gate（branch §9）；
#   ✗ 待办——P0 纯小麦开局：OPENING_SHIFT 现仍为 d1{3羊}/d2{2牛} 的
#     tetsuya-v1 半步照搬，非 branch 计划 §3 的开局变体 C（d0 零畜零雇），
#     实施序 branch §9-①；
#   ✗ 待办——三重前置检查的曲线门地板值已在此（DEAD_PRICE_FLOOR/
#     CROP_FLOOR），但门本体待迁（见 strategy/market 审查）。
# ===========================================================================


# --------------------------------------------------------------------------
# Embedded game constants (mirror of kaggle-environments 1.32.7 kaggriculture)
# --------------------------------------------------------------------------
# 【中文】嵌入式游戏常量：官方引擎 1.32.7 的逐字段镜像（离线自主，运行
# 时不读引擎源码）。作物字段含义——seed 种子价；first/max_yield_day 首产/
# 满产日龄窗；interval 多次采收间隔；max_yield 一生最多采收事件数；
# ongoing 是否连续产型作物。动物字段——cost 购入价；structure 所需畜舍
# 类型；first_yield_day 首产日龄；interval 产仔间隔；max_held 单体累积
# 上限；product 产品名。BASE_PRICE 为市场曲线的基准价（非成交价——成交
# 价由下方 MARKET_PARAMS_EMB 曲线按库存偏移决定）。
CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

# ---- r4-P2 town-demand model (official engine constants) ----------------
# Each unlocked shop instance consumes 1 unit of every product it lists
# every townShopSellInterval=4 steps (6 draws/day), single-product shops
# draw 2x; the town center draws 1 of every non-fertilizer product per day
# (townCenterSellInterval=24).  The set of unlocked shops is OBSERVABLE in
# obs.town.unlocked_shops, so the market layer knows exactly how much the
# town will absorb per item per day -- the backbone of the P2 sell rule
# SELL <=> R_now >= E[R_future] - C_overflow - C_liquidity - C_terminal.
SHOPS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
SHOP_DRAWS_PER_DAY = 6      # 24 turns / townShopSellInterval 4
CENTER_DRAWS_PER_DAY = 1    # 24 turns / townCenterSellInterval 24

# 【中文】方向移动、赛季天数（30 天一季）。MOVES 是方向名到 (dx,dy) 的
# 映射；SEASON_DAYS 用于终局清算判定（day 29 只卖不买）。
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
SEASON_DAYS = 30

# ---- strategy knobs (every value carries its evidence in the comment;
# tuning changes are logged in exports/logs/iteration_gate_log.jsonl) ----
# 【中文】策略旋钮区：本文件所有可调参数集中在此。每个值旁的英文注释是
# 其实验证据（来自回放画像或迭代门控实测），调参历史记录在
# exports/logs/iteration_gate_log.jsonl；测试套件锁定多数常量，改值
# 必须过全套回归门禁。

# 【中文】劳动力旋钮：HANDS_RAMP 是"日期→雇工目标数"阶梯（tuples 按
# from_day 匹配最后一个生效档）；HANDS_CAP_R3 为畜群驱动下的上限 12；
# 雇工只能在一天的前 2 小时下单（引擎规则），HIRE_BURST 限单回合爆发量。
# FM-O2 labour: top-20 median 9.4 hires/day (282-295/season), leader 9.7-9.9
# (Crop Dusta land/labour series); 24 turns/day per unit, fib cost per day.
# R3-4: _crew_target tops this ramp up to HANDS_CAP_R3 following the herd
# (round-2 winners hold 12 hands from d7-11; top-20 9.4-9.9/day).
# V-T10 tetsuya labour series (08-31 shard, 6 games): d0 5, d1 7, d3 7,
# d4 8, d6-9 8-10, 12 by d12 -- flat-early beats our d1 6.
HANDS_RAMP = ((0, 5), (1, 7), (4, 8), (6, 9), (10, 11), (12, 12))
HANDS_CAP_R3 = 12        # r3: crew 12 once the herd plan reaches 12 head
HIRE_BURST = 5           # HIRE orders per dawn turn (burst, m2b fix)
HIRE_HOUR_MAX = 2        # dawn window (m2b fix: burst must fit hour <= 2)

# 【中文】土地旋钮：LAND_PLAN[当前象限数] = (最迟应购日, 保护基金额)；
# 买第 2/3 象限的官方地价在 LAND_PRICE；基金未凑齐的宽限天数内
# （LAND_PEND_WINDOW）畜群采购让位于买地，逾期则解除互锁防死锁。
# FM-O2 land: leader NE day 4+ / SW day 7+; top-20 3-quadrant consensus
# (100/101 seats); the 4th quadrant is almost never bought (skip SE).
# LAND_PLAN[quads_now] = (due_day, protected_fund); fund = price + reserve.
LAND_PLAN = {1: (4, 1700), 2: (7, 2700)}
LAND_PRICE = {1: 1000, 2: 2000, 3: 4000}
LAND_PEND_WINDOW = 4     # herd unblocks if land is this many days overdue

# 【中文】畜群旋钮组：day-0 开局爆发买 2 牛 + 2 羊（OPENING_HERD，
# 花掉 3000 启动资金的 1800，保留 OPENING_RESERVE）；HERD_CAP 是计划
# 上限 16 = 9 牛 + 7 羊（HERD_COMPOSITION，2026-09-04 校准）；超出 16 的扩张走
# _npv_herd_decision 的边际 NPV 判定，绝对安全上限 HERD_CAP_NPV = 17；
# LIQUIDITY_FLOOR 保证买畜后钱包付得起次日黎明雇工费（见安全哲学）。
# R3-1/R3-2 herd: the r3 opening.  Day 0 buys the mixed burst below outright
# (1800 of the 3000 start; 116/116 top-20 seats hold 4-5 head on d0, 3/3
# round-2 winners; the m3 engine's 1-sheep d0 is the fork the round-2
# losses traced to).  Ceiling 14 = 8C+6S (winners peak 13-17; top-20 med
# 12 / p75 15); with the 4+day target ramp the 12-head deadline lands
# d8-9 (< d11).  Cows interleave in early so they reach the day-8+
# premium-milk window on time; goose dropped (egg log-curve pays ~2.1k
# vs a cow's ~5k in the observed premium-milk meta).
OPENING_HERD = {"COW": 2, "SHEEP": 2}
OPENING_RESERVE = 500              # 800->500（top d4 现金 128 实测；FUSE 300 不变）    # cash kept besides the day-0 burst (m2b cushion)
# V-T1 ablation copy (tetsuya 08-31 opening shift): the day-0 herd burst is
# replaced by a staged day1-3S / day2-2C sequence; day 0 keeps its cash for
# the wheat opening. Labour plan and the rest of the r3 ramp unchanged.
OPENING_SHIFT = True
# V-C (tetsuya-true d0 opening, branch plan v1.3 / A-① probe).  Raw-replay
# audit 2026-09-02 (6/6 games, steps[1..24] direct parse, exports/online/
# tetsuya_v2_strategy_analysis.md correction section): his CURRENT day 0 is a
# SMALL burst -- 2 sheep + 1 cow (~1400) with 5 hires and 10 wheat seeds,
# end-of-d0 cash 478-483; the earlier "zero herd zero hires ~2900" reading of
# the v2 analysis is retracted.  This single variable moves our herd burst
# back TO day 0 in his smaller shape (variant B below was the d1/d2 deferral;
# the paced loop still owns d1+ at pace 1/day, and _opening_shift_hold keeps
# day 0 free of any further paced buys).
# 2026-09-04 畜群前置校准（0903 日集 44 席）：top d0 4-5 头（round-2
# 语料 116/116），d8 中位 12 头，奶/毛日收入是 d7-11 现金爆发的引擎
# （top d11 现金 13.7k vs 我方 946 的根源）。开局回到 4 头，预备金
# 800→500（top d4 现金 128 贴线运行；FUSE 300 仍是绝对红线）。
OPENING_SHIFT_SEQ = {0: {"SHEEP": 2, "COW": 2}}
HERD_CAP = 16            # 14->16（top 峰值中位 15.8，0903 日集）
                         # to the constant, not a literal
# r4-P3: STATE-DRIVEN herd ceiling.  Beyond the pinned 14-head plan,
# extra head is bought only on a positive marginal NPV (evenings x margin
# > cost + feed + service) with an ABSOLUTE safety ceiling of 17.
HERD_CAP_NPV = 17
HERD_NPV_LAST_DAY = 16   # an evening on day 17+ repays too little capex
HERD_NPV_MIN_MARGIN = 90  # per-evening product margin needed to expand
LAND_LATE_CUTOFF = 18    # no SW purchase after this day (P3 NPV rule)
CREW_LATE_DAY = 24       # P3 drawdown: fewer hands when the queue thins
CREW_LATE_CAP = 10
HERD_COMPOSITION = {"SHEEP": 7, "COW": 9, "GOOSE": 0}  # 16 = top 峰值 15.8 校准（胜者混样 5C+9S / 9C+4S / 8C+9S）
ANIMAL_BUY_LAST_DAY = {"SHEEP": 20, "COW": 20, "GOOSE": 24}
COW_BUY_RESERVE = 380    # cash kept besides an animal purchase (m2b)
                         # (v10 M-B trial at 300 REVERTED: combined gate
                         # dev +84k -> +11.8k, reg disaster 0.0227 ->
                         # 0.0455 -- cash reached animals before the
                         # manure loop could fund them)
LIQUIDITY_FLOOR = 350    # v10 M-E: post-purchase wallet floor on animal
                         # buys -- covers the next dawn's fib crew bill
                         # (~88 for 8 hands) plus a feed margin, so a
                         # same-turn land+animals+seeds burst can never
                         # take the wallet where the hire gate
                         # (money - 60) starts cutting the crew (online
                         # ep 103783585: 3256 -> 16 in one turn, hands
                         # 8 -> 2, field rotted, herd starved, bank 8.4k)
ANIMAL_PACE = ((8, 3), (4, 2))   # head/day from day: 1 before day 4, 2 to 7, 3 after
PASTURE_RING = 2         # structures within manhattan dist <= 2 of shed access

# 【中文】死价红线：从 DEAD_PRICE_FROM_DAY 起可读曲线后，某物种产品
# 价格跌破其地板价（奶/毛 90、蛋 30）即冻结该物种扩张——"绝不向死价
# 曲线扩产"（对局实测：牛奶崩盘局的榜首不扩牛栏）。买畜处还叠加
# 商铺吸收条件（见 _market_orders）。
# RED LINE dead-price freeze (generalized m2b demand-drought rule): no
# species scale-up when ITS product curve is dead (milk-crash leader does
# not expand cows -> applied per species/crop by glut shape).
DEAD_PRICE_FLOOR = {"MILK": 90, "WOOL": 90, "EGG": 30}
DEAD_PRICE_FROM_DAY = 10  # m2b gate: freezes apply once curves can be read

# 【中文】作物轮作旋钮：CROP_PHASE = 每种作物的物候窗口(起,止日)；
# CROP_FLOOR = 价格红线（现价低于则冻结种植）；CROP_CAP_PER_QUAD =
# 每象限种植上限；PLANT_LAST_DAY = 最晚种植日（再种无法回本）。
# 三个门同时开才会分配地块（见 _field_alloc）。FERT_VALUE_GATE 是
# 肥料袋"自用 vs 卖出"的分界价（高价时只留草莓/西瓜 Boost 用）。
# FM-O1 rotation: phase windows from the rank-1 frame (melon early /
# strawberry mid / late filler), price floors from the m2 online-pool
# archetypes (crop_rotator min_price 55/150, carrot base 35 minus margin).
# R3-3: strawberry phase opens day 5 (the d0-4 cash belongs to the herd
# burst; winners plant d7-11 and top-20 d4-7) and the per-quad cap rises
# to 6 (3 quads = 18 tiles by d11-13; winners 16-23, top-20 peak med 36
# starves the feed/care labour budget -- do not chase it).
FERT_VALUE_GATE = 70     # fert sack sold at 70+ beats a wheat/carrot boost
                         # (~60-70/unit); strawberry/melon boosts (~200-230)
                         # are always worth the sack (self_feed ledger: they
                         # never fertilize and sold 158u for +12.8k)
WHEAT_MONEY_GATE = 30   # wheat joins the rotation as a money crop at 30+
WHEAT_MONEY_CAP_PER_QUAD = 3
# V-T2 ablation copy (tetsuya endgame rotation): carrot endgame line with a
# wider 6/quad cap.  V-T6: the planting deadline returns to day 26 -- the
# d27 batches of rounds 9/10 all stranded unharvested (9-12 units/episode;
# a day-27 planting produces on the evening of 28 and the terminal
# feasibility check drops the far tiles on 29).
# V-T9 (tetsuya copy): melon 3 -> 6/quad (his seasons plant 9-18 melon on
# the far rim; our 3/quad = 9 total under-used the zoning).
CROP_PHASE = {"MELON": (0, 17), "STRAWBERRY": (5, 24), "CARROT": (15, 26),
              "TOMATO": (8, 26)}
# 2026-09-04 种植规划校准（线上 09-03 日集 22 回放/44 席实测，证据
# planting_deep_stats.json + round19 analysis）：TOP 层（奖励 >=90k，
# n=18）全季种植 234 株 vs 我方 96 株；草莓 33-38 株持续补种到深季——
# 旧窗 (5,14) 在 d14 掐断是 d15-21 只种 top 28% 的直接原因；TOMATO 是
# 头部现役作物（Crop Dusta 18 格 ongoing），补入轮作。
CROP_FLOOR = {"MELON": 150, "STRAWBERRY": 55, "CARROT": 28, "TOMATO": 20}
CROP_CAP_PER_QUAD = {"MELON": 6, "STRAWBERRY": 12, "CARROT": 8,
                     "TOMATO": 4}  # 莓 8→12：top 33-38 株（3 象限）对齐
PLANT_LAST_DAY = {"WHEAT": 26, "CARROT": 26, "MELON": 17, "STRAWBERRY": 24}
# 小麦最晚日 24→26：top 晚季持续补麦（d22+ 层均 69.7 株），V-T6 的 d27
# 搁浅证据只否决 27，不否决 26。

# ---- r5-P4 macro-plan layer: strategy-space extension --------------------
# 【中文】宏观计划层（战役 III 第 5 轮 P4）：r4 框架本地 142W-2L，但公榜
# 下一档是 96-110k 的"小麦-草莓大田经济"，r4 参数框架表达不出来（框架内
# 任何优化都封顶 ~75k）。于是每天用确定性门控（_decide_mode）在三个计划
# 中选一个来"拓宽可建经济的空间"，而微观执行器（红线任务/价值匹配/市场
# 门控/安全网）完全不动——计划改变的是"允许建什么"，不是"怎么走一回合"。
# 三个计划对象 _DEFENSIVE_PLAN / _VOLUME_PLAN / SCALE 分支携带的参数：
# 草莓每象限与总上限、小麦金钱作物配额、雇工上限、畜群天花板。
# Round-3 line: r4 is locally 142W-2L but the public ladder's next band is
# the 96-110k wheat-strawberry economy (round3_ledger: Renji 109.7k with 42
# strawberry tiles + 1508u wheat sold / 1501u feed bought; DevilQ 96.6k
# with 31 strawberry + 14 cows).  The r4 frame (3 quads, strawberry cap
# 6/quad = 18 tiles, crew 12) cannot EXPRESS that economy -- any optimizer
# inside it plateaus near 75k.  The daily macro plan widens the space:
#
#   DEFENSIVE    the r4 rotation-ranch frame parameters (every plan failure
#                and every non-qualifying day uses this conservative frame)
#   VOLUME_CROP  the 96-110k band: SE quadrant becomes a buyable asset,
#                strawberry ceiling 42 tiles, wheat money-crop scaling,
#                crew 15; the herd stays on the 14-head plan + guardrailed
#                external feed (the Renji line: feed bought, not grown)
#   SCALE_RANCH  the 13-17 head winner band: NPV ceiling lifted to 18 when
#                the animal lines outbid crop expansion
#
# Mode choice is a deterministic daily gate on PUBLIC state only (prices,
# unlocked shops, both farms -- obs.farms is shared; only sheds are
# private).  The micro executor (red-line tasks, value matching, market
# gates, safety shield) is untouched: the plan changes WHAT economy the
# executor is allowed to build, not how a turn is played.
MODE_STR_QUAD_CAP = 16     # volume: strawberry tiles per unlocked quadrant
MODE_STR_TOTAL_CAP = 48    # volume: field ceiling (Renji's 42-tile field)
MODE_WHEAT_MONEY_QUAD = 8  # volume: wheat money tiles/quad (log glut curve)
MODE_CREW_CAP_VOL = 15     # volume: hands ceiling (42 tiles of daily water)
MODE_HERD_CAP_SCALE = 18   # scale: NPV ceiling (winners' 13-17 band + 1)
# sprint-A 经济域复刻（sprint_forensics_0919 §2）：DEFENSIVE 与 SCALE 共用
# 莓配额——658-663 分段赢家莓峰 18-24（v10.3 线）；28/36 系 0903 top 层
# 外推（与 VOLUME 的 16/48 同源校准，未随本次回收——条件模式防归因混杂）。
STRAW_QUAD_CAP_REGIME = 8
STRAW_TOTAL_CAP_REGIME = 24
_DEFENSIVE_PLAN = {"mode": "DEFENSIVE", "volume": False, "scale": False,
                   "wheat_farm": False,
                   "straw_quad_cap": STRAW_QUAD_CAP_REGIME,
                   "straw_total_cap": STRAW_TOTAL_CAP_REGIME,
                   "wheat_money_quad": WHEAT_MONEY_CAP_PER_QUAD,
                   "crew_cap": HANDS_CAP_R3,
                   "herd_ceiling": HERD_CAP_NPV}
_VOLUME_PLAN = {"mode": "VOLUME_CROP", "volume": True, "scale": False,
                "wheat_farm": False,
                "straw_quad_cap": MODE_STR_QUAD_CAP,
                "straw_total_cap": MODE_STR_TOTAL_CAP,
                "wheat_money_quad": MODE_WHEAT_MONEY_QUAD,
                "crew_cap": MODE_CREW_CAP_VOL,
                "herd_ceiling": HERD_CAP_NPV}
# v7.2-V1 herd-readiness floor for the VOLUME entry.  Seed-103 forensics
# (both seats lost to two_quad_denser by 32-46k): the entry fired on a
# 4-5-head ranch, then 28 strawberry tiles + the SW purchase (~4800
# capex) met a ~200 wallet -- crew disbanded 12->0, animals starved
# 5->0, fields lapsed to 26-49 weeds (the bankruptcy spiral the P5
# ablations predicted for unproven widenings).  The winner ticket list
# (r3-1 cross-profile) puts >=12 head by d11 BEFORE the wide-field
# economics; our frame realistically completes 10 by the d6-12 entry
# window in live seasons, so the floor is 10.
VOLUME_HERD_FLOOR = 10
SE_DUE_DAY = 10            # volume: earliest SE buy (SW settled, cash back)
SE_BUY_LAST_DAY = 14       # later than this 25 new tiles cannot repay
SE_FUND = 4600             # SE price 4000 + working-cash cushion
# ---- v9 WHEAT_FARM conditional mode ---------------------------------------
# 【中文】v9 小麦专精条件模式：第 5 轮战略评审测得目标档的形态是"12 头
# 畜 + 28-32 格持续补种小麦 + ~8 格草莓副业"。这是可选实验（默认 False，
# v9 首波影子候选保持 DEFENSIVE/VOLUME/SCALE 行为逐字节不变）；入口
# 门控 _wheat_farm_entry_ok 复用 v7.2 验证过的 day 6-12 窗口，续期仅
# 到小麦种植截止日。各阈值含义见各行英文证据注释。
# Round-5 strategic review (2026-08-30) measured the target band as herd
# around 12, 28-32 continuously replanted wheat tiles, about 8 strawberry
# tiles, and no melon/carrot.  This is an opt-in experiment: the default is
# deliberately false so v9's first-wave shadow candidate keeps its exact
# DEFENSIVE/VOLUME/SCALE planning behavior.
V9_WHEAT_FARM_ENABLED = False
WHEAT_FARM_HERD_FLOOR = 12       # round5 review + JOURNAL: top-band peak herd median 12
WHEAT_FARM_WHEAT_FLOOR = 28      # round5 review: high-band wheat field 28-35 tiles
WHEAT_FARM_WHEAT_CAP = 32        # round5 review: target band is 28-32 for this mode
WHEAT_FARM_STRAW_CAP = 8         # JOURNAL v7.1 Sam Scott: strawberry side line 6-8
WHEAT_FARM_CASH_REDLINE = OPENING_RESERVE  # v7.2/VOLUME cash floor: 800 reserve
WHEAT_FARM_FEED_MAX_PRICE = 36    # v7.2 external-feed guardrail
WHEAT_FARM_OPP_WHEAT_MAX = 10    # v8 W3 no-contest gate: opponent wheat <=10
# Entry reuses the proven v7.2 VOLUME day 6-12 gate; continuation lasts only
# through the existing wheat planting deadline, so late capex/seed bets do not
# reopen after the measured production window.
WHEAT_FARM_ENTRY_START = 6
WHEAT_FARM_ENTRY_END = 12
WHEAT_FARM_ENTRY_WHEAT_MIN = 12  # v7.2 starts near 16; mode must extend a live line
WHEAT_FARM_HOLD_CASH = 400       # hold floor; entry still keeps the proven 800
# Entry floor is NOT the 12-head profile ceiling: the champion's PLACED herd
# completes ~d13-14 (probe 2026-08-30, 20 real games: on-tiles medians
# d6-12 = 4/4/6/6/6/8/8), and the d7 SW purchase drains cash exactly when
# the wheat line is still alive -- a 12-head entry gate is unreachable in
# any window (the r1 paired ablation measured 88 byte-identical ties, zero
# firings).  Entry instead requires the day-0 burst to be PLACED (>= 4
# head: the dairy annuity is live, feed demand is small); the mode still
# builds toward the 12-head ceiling.  Unlike the VOLUME bankruptcy class,
# the capex here is 10/coin wheat seed bought in cash-gated batches under
# the 800 redline -- no 100/coin strawberry widening, no SE 4000 buy.
WHEAT_FARM_ENTRY_HERD_MIN = 4
_FIB_CUM = [0] * 17        # _FIB_CUM[n] = one day's cost of n hires
_a, _b, _acc = 1, 1, 0
for _i in range(1, 17):
    _acc += _a
    _FIB_CUM[_i] = _acc
    _a, _b = _b, _a + _b

# 【中文】饲料/肥料/终局/卖出门槛旋钮组：
#   * FEED_BUY_MAX_PRICE 外购饲料常规护栏价（实测档位 26-32）；85 是
#     饥饿止损价（贵小麦仍比饿死牲畜便宜）；WHEAT_FEED_RESERVE 是
#     出售小麦前保留的饲料天数；WHEAT_SELL_GATE 是小麦"真实出价"门槛。
#   * FERT_* 肥料限囤/放货两档价 + 库存上限 + 田间保留量。
#   * ENDGAME_DAY = 28 起进入 48 小时终局窗口：囤货分批倾销 + 停喂。
#   * 各高级产品 GATE（达到才卖）/HOARD_FLOOR（低于不卖的安全库存）；
#     曲线形状决定批量：sq 曲线崩得最快→羊毛批量最小，log 曲线抗崩
#     →小麦/蛋最从容。WOOL_CUT_LOSS 是羊毛曲线已死时的止损线。
# FM-O3 feed: guardrailed external buying (profiles: avg buy price 26-32,
# 414-2732u/season across top-20); 85 = starvation cap (dear wheat is still
# cheaper than a lost animal -- m2b).
FEED_BUY_MAX_PRICE = 36
WHEAT_FEED_RESERVE = 8   # feed days kept before selling wheat (measured: a
                         # 4-day buffer forced sell-at-33 / rebuy-at-37 churn)
WHEAT_SELL_GATE = 26     # log glut curve; hold for a real bid, but never
                         # starve capex (money-fallback below)

# FM-4 fertilizer (m2b, generalized to rotation crops)
FERT_GATE = 50           # fertilizer: hold below, release above
FERT_SELL_FLOOR = 20     # v10 M-C: monetize surplus manure above this price
FERT_STOCK_CAP = 6       # hoard bound: shed slots belong to the products
FERT_FIELD_RESERVE = 4   # keep some fertilizer for the fields

# FM-O4 endgame 48h window (top-20 median endgame gain +13.0% of final)
ENDGAME_DAY = 28         # dump tranches + stop feeding from here

# premium sell gates / tranches (curve shapes: wool/melon sq, milk/straw
# linear, wheat/egg log -- tranche size inversely follows crash speed)
WOOL_GATE = 150
WOOL_HOARD_FLOOR = 8
WOOL_HOARD_CAP = 34
WOOL_CUT_LOSS = 45      # curve dying (no yarn store drawn): realize fast
STRAWBERRY_GATE = 105
STRAWBERRY_HOARD_FLOOR = 8
MELON_GATE = 180
MELON_HOARD_FLOOR = 4
CARROT_GATE = 28
CARROT_HOARD_FLOOR = 6
EGG_GATE = 40
EGG_HOARD_FLOOR = 4

LLM_PROVIDER = None      # optional consultant, default off; local A/B only

# ---- r4-P1 state-value scheduling knobs --------------------------------
# 【中文】r4-P1 状态价值调度旋钮：任务优先级 = 终局价值 V - 行走成本
# (TRAVEL_MU/格) - 跨象限惩罚(CROSS_QUAD_PENALTY) + 粘滞奖励
# (STICKY_BONUS, 抑制震荡)。`red` 标记的任务走 Phase A 一票否决通道：
# "今晚会死"的义务（断水/断粮/末日归还）由最近工人在价值阶段之前
# 覆盖。FEED_RED_HOUR 是断粮升级为红线的小时数。
# Priority(i) = dV_terminal - C_travel - C_setup - C_opportunity; every task
# carries a `v` (estimated terminal value) and optional `red` (one-vote
# veto: death-tonight obligations covered by the nearest worker BEFORE the
# value phase, regardless of competing weights).  r3-P0 shadow-replay
# measurement: the r3 scheduler's w/(1+dist) greedy STARVED far red-line
# tiles -- 14-29 care-lapse weeds/game clustered at manhattan 6-9 from the
# shed (all requested waters succeeded; the lapsed tiles never received a
# request because a nearby w=30 task always outscored a distant w=98 one),
# and 5 animals escaped in 6 games the same way.  Death-tonight facts from
# the engine source: a plant enters the day with consecutive_unwatered >= 1
# OR was planted today (planting counts as unwatered) and dies at the
# evening refresh if still unwatered; an animal with consecutive_unfed >= 1
# escapes at the evening refresh if still unfed.
TRAVEL_MU = 25.0            # value charged per walking turn (marginal op)
CROSS_QUAD_PENALTY = 40.0   # zone stickiness: leaving the current quadrant
STICKY_BONUS = 45.0         # continuity bonus for the previous target
FEED_RED_HOUR = 16          # unfed-by-now escalates to red (r3 escalation)
PROD_HORIZON_DAY = 28       # production evenings after this never cash out

# ---- v7 weed-reclaim knobs ----------------------------------------------
# 【中文】v7 杂草回收旋钮：v6 的缺陷是规划完全跳过 WEED 格，导致每棵
# 杂草永久占格（线上 12/12 局 DIG=0，而 top-20 选手 DIG 23-68 次/局）。
# WEED_RECLAIM_MODE 三态——"none" 复现 v6（消融对照）；"planned"（当前
# 值）可回收杂草排在真空格之后进入规划，只为真正想要该格时才安排 DIG；
# "all" 压力测试变体。WEED_DIG_HOUR_MIN=20：DIG 只在深夜闲置窗口执行
# （白天先保 WATER/FEED 红线——C1 探针实测全天 DIG 会饿死红线任务）。
# ROTATION_DIG：对"已收完的连续产作物"（草莓产完 yield=0）执行轮作
# DIG，停止对死格浇水施肥并还给轮作分配。PLANT_EOD_GUARD 已排除
# （未合并，保留旋钮供消融重跑）。
# v7-W.  The v6 chain is broken: _field_alloc skipped WEED tiles entirely,
# so builds/crop_map never contained them and the planned-DIG branch in
# _build_tasks (`pos in builds or in crop_map`) was UNREACHABLE -- every
# weed (care-lapse, random spawn, overripe decay) permanently blocked its
# tile (round-3/4 online replays: v6 DIG=0 in 12/12 games while 118/120
# top-20 seats DIG 23-68 times).  Modes:
#   "none"    reproduces v6 byte-for-byte (ablation control)
#   "planned" reclaimable weeds enter the alloc preference lists BEHIND
#             real empties (ring weeds after ring empties, field weeds
#             after all field empties) -- a weed is only planned when the
#             frame genuinely wants its tile, and the existing planned-DIG
#             branch fires for exactly those positions
#   "all"     "planned" plus a low-value DIG for every other unlocked
#             weed (pressure-test variant, not a merge default)
WEED_RECLAIM_MODE = "planned"
# v7-C2: the C1 probe (DIG at any hour, v=50) measurably STARVED the red
# lines in labour-scarce games (near_band s101 BA: WATER 656->579, lapse
# 17->34, escapes 3->6, 104k->16k) -- Phase-B DIG displaced same-day
# watering.  Round-2 admission: DIG (planned-weed AND rotation) only in
# the late-day slack window, after the FEED (>=16) and WATER red lines
# own Phase A; 0 reproduces the all-day C1 behaviour.
WEED_DIG_HOUR_MIN = 20
# v7-R rotation-DIG: top-20 replays DIG 23-68x/game concentrated d11-12
# and d21-28, and the d20+ targets are FINISHED strawberries (yield 0, no
# production evening left), not weeds.  v6 kept watering those tiles (the
# planned-ongoing WATER task, futval 0) and they never re-entered the
# alloc -- dead weight paying water and blocking the wheat rotation.
ROTATION_DIG = True
ROTATION_DIG_DAY = 18
# v7-H (EXCLUDED from the frozen v7: no stack indicator gain, more
# divergence -- kept as a knob for ablation reruns).  A fresh plant
# enters at consecutive_unwatered=1 and turns WEED at the evening
# refresh unless watered the same day (engine source); a PLANT issued
# after hour 21 leaves no reliable WATER window.
PLANT_EOD_GUARD = False
PLANT_HOUR_MAX = 21
# V-T5 tetsuya-style spatial greed (forensics 2026-09-02: his adjacent-cell
# operation continuity is 78% vs our 48%, his idle-PASS 13% vs our ~50% --
# global value matching lets a distant 300-value task outrank a nearby
# 100-value one EVERY turn, fragmenting worker trajectories; d8-d11 of the
# crash episode ep104594916 this starved the harvest, cash flow broke and
# all 12 hands reset to zero for 17 days).  Distance BUCKETS soften the
# value race in phase B: near (0-1 cells), local (2-4), far (5+).  The
# bucket charge is deliberately MODERATE (crossing one bucket costs about
# as much as walking ~5 extra cells): a 600-point dominance measured
# continuity 62-65% but starved distant rich harvests and cost -16k in
# the seed-101 self-play -- tetsuya's continuity is half LAYOUT (his rich
# crops sit beside the workers), so the scheduler must prefer near work
# without forbidding far work.
BUCKET_DOMINANCE = 120.0
# V-T7 functional zoning: wheat band inside the dairy home quadrant (NW)
# before the rotation claims its cells -- tetsuya holds 10 wheat in NW
# during the single-quadrant opening (9 leaves room for melon 3 +
# strawberry 8 in the ~20 free NW cells) and 12-15 beside the pastures on
# the multi-quadrant d20 snapshots (the pass-2 claim tops the band back
# up to the full _wheat_cap once other quadrants exist).
WHEAT_DAIRY_QUAD_BAND = 9
# V-T7: the carrot endgame line only CLAIMS tiles from this day.  sprint-A
# 复刻（2026-09-19 forensics）：22 只留 4-5 天窗口，线上 v13.x 萝卜线死绝
# （峰 0-0.1）而 v9.2/v10.3 档萝卜峰 11-12；sprint-A 顺序翻转后小麦底仓
# 在萝卜之前 claim，V-T7 当年"萝卜蹲死麦田"的前提已消——恢复 d15 中局
# 窗（CROP_PHASE (15,26) 的起点）。CROP_PHASE keeps the planting legality.
CARROT_ENDGAME_FROM = 15
# V-T8 pasture zoning caps (tetsuya d25 forensics: NW 7 / NE 2-3 at the
# access mouth / SW unlimited via the outward chain).
PASTURE_QUAD_CAP = {"NW": 7, "NE": 3}
# V-T3 watertight planting (forensics: ep 104585743 d8 -- a 10-seed NE pulse
# planted h8-14 left 18 tiles unwatered and 16 died; tetsuya's 6 replays all
# plant in the daytime band and never lose the batch).  Two task-generation
# guards: (a) same-day water window -- the nearest worker must still be able
# to walk to the tile, PLANT and WATER before hour 23; (b) a daily
# new-planting cap so an opening cheque can never compress a land+seed+plant
# expansion into one afternoon.  V-T9 (tetsuya copy): 8 -> 16 -- his d7
# batch plants 15-18 in one day with zero losses because every planting
# passes the water window; our guard (a) provides exactly that gate.
# 2026-09-04 激进模式：16 -> 24（tetsuya 实测 15-18/日零损失；水窗守卫
# (a) 仍是逐格硬门，脉冲上限只封顶不放宽逐格可行性）。
PLANT_DAILY_CAP = 24

# 【中文】v9 分区巡逻状态（影子路由）：工人当日首次站位决定其"主场
# 象限"；路线只在目标完成/消失、资格变化或红线义务集合变化时重建。
# CROSS_SECTOR_* 是跨区软惩罚与价值优势门槛；V9_TOUR_* 是路线头部的
# 巡逻连续性奖励（让工人顺着本区队列扫过去，而不是每次全局追最高分
# 任务）。当前 V9_SHADOW_ROUTING=True：路由仅作影子采集，执行权仍在
# 冠军调度器 _schedule_units_v72（见文件尾部的回归证据）。
# v9 partitioned patrol state.  Home sectors are assigned from the worker's
# first position of the day and retained while a route is valid.  A route is
# rebuilt only when its target completes/disappears, eligibility changes, or
# the set of red-line obligations changes.
# same scale as STICKY_BONUS) so a worker sweeps its sector's queue
# instead of globally re-chasing the highest-value task after every
# completion.  The baseline comparison (2026-08-30, 24 paired cells)
# measured the previous 0.01/rank bump as efficiency-inert: ratio
# 2.214 active vs 2.194 shadow.  Red-line tasks are exempt (phase A
# stays the hard safety veto) and eligibility graphs are untouched.
V9_TOUR_BONUS = 45.0
V9_TOUR_DECAY = 15.0


# 【中文】基础小工具组：_get 容错取值（dict 属性皆可）；_dist 曼哈顿
# 距离（本作唯一距离度量）；_step_towards 朝目标走一格（先横后纵）；
# _shed_access 返回四个中心仓库口格（引擎规则：仓库操作先于 LOCKED 判
# 定，所以四个中心格永远可用）；_quadrant_of 由坐标算象限名（NW/NE/
# SW/SE）；_window 作物浇水增益的日龄窗口；_hire_cost 第 n 次雇工的
# 斐波那契价格表（1,1,2,3,5,8,...）。
def _get(obj, key, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _dist(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx, fy, tx, ty):
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _shed_access(board_size, unlocked_quadrants=None):
    """Official 1.32.7 shed-access tiles (NWSE inner corners).

    The engine resolves PICKUP/DROP *before* its LOCKED guard (vendored
    kaggriculture.py: "Shed operations resolve before the LOCKED guard"),
    so all four center tiles are always usable -- even the three that
    start LOCKED.  The unlocked_quadrants argument is accepted for call-site
    compatibility and deliberately ignored.
    """
    half = board_size // 2
    return ((half - 1, half - 1), (half, half - 1),
            (half - 1, half), (half, half))


def _shed_adjacent(x, y, board_size, unlocked_quadrants=None):
    return (x, y) in _shed_access(board_size)


def _quadrant_shed_tile(x, y, board_size):
    """The shed-access tile of the quadrant (x, y) sits in."""
    half = board_size // 2
    qx = half - 1 if x < half else half
    qy = half - 1 if y < half else half
    return (qx, qy)


def _quadrant_of(x, y, board_size):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _window(crop):
    cd = CROPS[crop]
    return (cd["max_yield_day"] + 1) // 2, cd["max_yield_day"]




# ---- r4-P2 analytic price engine (official MARKET_PARAMS mirror) --------
# 【中文】r4-P2 解析价格引擎（官方 MARKET_PARAMS 的镜像）。官方定价：
#     price(inv) = base ± amp * f(|inv - I0|)
# 其中 I0 = 10000 均衡库存，T 是"一块田 24 天的产量"尺度，曲线形状 f
# 分 linear/sq/sqrt/log/hinge 五种。季节内库存围绕 I0 摆动 ±30..400，
# 曲线很陡——所以卖出规则可以直接从观测到的"日间价格移动"反推出净流量，
# 再前推投影未来价格，而不需要整场仿真。每件商品的 (base, T, 下侧形状,
# 下侧幅度, 上侧形状, 上侧幅度) 见下表：上侧=过剩压价侧（过剩越多价越
# 低），下侧=稀缺抬价侧。例如羊毛上侧是 sq（崩得最快）、小麦上侧是
# log（最抗崩）——卖货批量的快慢节奏就按各商品的崩盘速度排的。
# price(inv) = base + sign * amp * f(|inv - I0|); T = one field's 24-day
# production.  Inventory swings over a season are +-30..400 around I0, so
# these curves are steep: the sell rule can PROJECT price from the observed
# net flow instead of simulating.  Net flow per item is inferred from the
# day-over-day price move (inverted through the curve), which already nets
# our production + the opponent's + town absorption.

MARKET_PARAMS_EMB = {   # item: (base, T, below_f, below_t, above_f, above_t)
    "WHEAT":      (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT":     (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO":     (60, 200, "hinge", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON":      (250, 300, "log", 0.20, "sq", 3.60),
    "EGG":        (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK":       (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL":       (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
MARKET_I0_EMB = 10000
HINGE_GAIN_EMB = 8.0
PRICE_FLOOR_EMB = 1


# REVERTED TO SHADOW 2026-08-30 by the confirmation gate
# v9_routing_confirm1 (regression-domain seeds 201-204, 176 games): the
# selection-domain result (v9_routing_distfirst_r1: 88-0 vs the pool on
# seeds 101-104, MERGEABLE) did NOT generalize -- pool WR 0.925 (lost
# cells, worst crop_rotator 0.75), disaster 0.0341 vs champion 0.0227,
# paired net -258.9k.  Attribution: one matchup mega-win (two_quad_denser
# +164.7k, seed 201 ~ +88k/seat) against broad margin losses on 8 of 11
# opponents (template_wheat 1W-7L).  The router as-shipped is a variance
# amplifier; the 88-0 was selection-domain luck on a margin-eroding
# mechanism.  The efficiency harness numbers (ratio 2.194 -> 2.152, ops
# +3.4%) remain real but do not buy win-rate generalization.  Future
# activation attempts must pre-register BOTH seed domains (101-104 AND
# 201-204) as the gate.

# ===========================================================================
# 【中文】branch plan v1.2/v1.3 落地旋钮（2026-09-02 实装：容量门 §5.3、
# 三重前置检查 §5.4、对手开局分类器 §4.1、阶段寄存器 §2、分线封顶表）
# ---------------------------------------------------------------------------
# ---- 容量定律（§5.3；系数为经验初值，M1 telemetry 定标后回填）----
# 最大资产单位(d) ≈ 24 × (1+H) × CAP_UTIL / CAP_TURNS_PER_UNIT
# 资产单位：莓/麦/瓜格=1，萝卜格=0.5，牲畜头=2；定标锚 Renji~81/DevilQ~92/
# tetsuya~91 单位同收敛于 crew 12（branch plan §5.3 定标锚表）。
# M1 三锚定标回填（2026-09-02 Phase-C，quickwin A/B 裁决）：top-20 语料
# 3600 席日 tpu 中位 3.29 / eff 0.89。A/B（4 种子全季）：base(2.4/0.75)
# → 124.0k/逃亡41/溢出1；capA(3.3/0.89) → 133.1k/逃亡0/溢出0（+7.3% 全指
# 标胜出）；capB(4.4/0.93 本地锚) → 136.9k 但溢出 13 爆表被拒。本地为安
# 全诊断，线上探针为最终裁决轴。
CAP_UTIL = 0.89                 # 有效利用率（top-20 锚实测）
CAP_TURNS_PER_UNIT = 2.0        # 2026-09-04 重定标：top 现实 d12 存量
                                # 58.7 格/5 人手（≈67 单位）远超旧 3.3
                                # 系数给出的 ~39 单位——3.3 把田地上限
                                # 压到 top 的一半，是 d8-14 扩张断崖的
                                # 根因；2.0 对齐 top 实测吞吐
CAP_USE_MAX = 0.95              # 黎明不变式上界（2026-09-04 激进模式：
                                # 0.85→0.95，几乎贴容量定律满界投建；定律
                                # 系数 3.3/0.89 本身不动，§5.3 语义不变）
CAP_USE_MIN = 0.65              # 下界：<此值报 slack（补线，兜底=小麦）
CAP_RESERVE_FRACTION = 0.15     # 峰值日检查的不可侵占余量（规则 4）
# ---- 分线封顶 = min(劳动力配额, 吸收上限)（§5.3 表）----
LINE_CAPS = {
    "MELON": 12,       # 回归 V-T9 回归证据钉住的 12（6 的收紧从未被消融
                       # 支持过；2026-09-04 激进模式按证据值复位）
    "STRAWBERRY": 48,  # Renji 线；48 = 0903 日集 top 校准后的宽计划身份（VOLUME 模式内另有 MODE_STR_TOTAL_CAP）
    "CARROT": 30,      # 终盘弹性线（相位窗口另管）
    "WHEAT": 99,       # log 抗崩+高吸收 = 剩余容量兜底（99=不限）
    "HERD": 16,        # 年金对冲线（14->16，top 峰值 15.8 校准）
}
# ---- 对手 d0 分类器（§4.1，v1.3 更正版：增"减档型"）----
OPP_CLASS_BURST_MIN = 4        # 爆发型：d0 已放 ≥4 头（top-20 116/116）
OPP_CLASS_REDUCED_RANGE = (2, 3)  # 减档型：2-3 头（tetsuya-true，v1.3 更正）
OPP_CLASS_DEFERRED_WHEAT = 8   # 延后型：0 头且小麦 ≥8 格
OPP_CLASS_MELON_MIN = 6        # 瓜先行：d1-3 瓜格 ≥6
# ---- 阶段窗口（§2 总表；P0-P5 由 _stage_of(day) 计算，无需状态存储）----
STAGE_P1_DUE = 6               # d6 检查点（五问）
STAGE_P2_FREEZE = 14           # d14 结构冻结
STAGE_P3_END = 21
STAGE_P4_END = 27
# ---- 干扰模块（market §3；MK-4 影子/MK-5 带闸，触发器先影子）----
INTERFERENCE_ARMED = True      # MK-5 武装（2026-09-02 Phase-D）：载体 1
                                # （现有库存倾销，零 capex/当天/可逆）带三闸
                                # 上线；载体 2-4（萝卜伏击/一次性羊群/镜像
                                # 种植）需 capex 窗口，留线上裁决后启用
INTERFERENCE_MARGIN = 2000     # R_opp > R_us + 此值 才触发（连续 2 天）
INTERFERENCE_CONFIRM_DAYS = 2
INTERFERENCE_BUDGET_FRAC = 0.15   # 干扰预算 ≤ 容量 15%（§3.5 闸 2）
INTERFERENCE_EXPOSURE_RATIO = 2.0  # 杀伤/暴露 ≥2（§3.5 闸 1）
# ---- 卖出计划器（market §2；囤vs清判据替代静态门槛的参数）----
SELL_PLAN_LOOKAHEAD_DAYS = 2   # 投影地平线（天）
SELL_PLAN_HOLD_EDGE = 1.05     # 囤的条件：E[p_future] ≥ 现价×此值 且线未争议
# ---- 机会性买入（market §5 小件 1；Danila 98.7k 出典 d1-2 囤 256u@低价）----
OPPORTUNE_WHEAT_PRICE = 26     # 价 <26 且库容+现金允许 → 囤至 N 天用量
OPPORTUNE_WHEAT_DAYS = 4       # 囤到的饲料天数上限
# ---- 买侧大单分批（market §5 小件 2；BUY 抽货推高曲线）----
BUY_CHUNK_MAX_UNITS = 40       # 单回合 BUY_PRODUCT 最大件数（超出跨回合分批）
# ---- P4 三档出清（branch §6；观测器 est_opp_held 驱动，缺数据回退门控）----
P4_HEAVY_HELD = 40             # 对手囤货 ≥40u → d25 抢跑档
P4_MID_HELD = 15               # 15-40 → d26-27 标准档；<15 从容档

# ===========================================================================
# 【中文】DTSP 惰性旋钮层（2026-09-19 P2.5；蓝图 m7 修订，用户授权）
# ---------------------------------------------------------------------------
# 背景：P2 首轮 official 基准诚实 FAIL（1/14 局过线，plan_space_gap 34/42）
#   ——根因是执行器分支激活门槛不随计划变、部分杠杆无旋钮，规划覆盖常成
#   no-op。本块为 DTSP 规划器（planner/plans.py 的 PlanSpec）开惰性旋钮
#   通道，改"常量默认值，可被计划覆盖"。
# 机制：全局旗 PLANNER_ENABLED（默认 False）+ 计划覆盖寄存器
#   PLANNER_OVERRIDES（agent 入口外可注入：离线基准在 exec 装载后写
#   ns["PLANNER_ENABLED"]=True 并按 "PLANNER_OVERRIDES.<键>" 点路径灌入
#   寄存器，见 scripts/planner_offline_bench.apply_knob_overrides）。
#   读取纪律：任何计划可覆盖的门槛/杠杆读取点一律走
#   _plan_knob(键, 默认值)——旗关时恒返回默认值。
# 旗关等价不变式（硬约束，黄金动作哈希测试钉住）：
#   * PLANNER_ENABLED=False（含线上提交路径——本键从不被线上代码置真）
#     时 _plan_knob 恒返回第二参，全部读取点与现役 v13.8 逐字节等价
#     （scripts/planner_flagoff_golden.py 6 种子全季动作流 sha256 校验）；
#   * 本块不新增任何 I/O、随机源或时钟读取；寄存器键名即
#     planner.plans.plan_to_knob_overrides 的点路径叶子名。
# 键面（31 键，分组与 plans.py 轴的对应关系见其【缺口清单】）：
#   模式激活（_decide_mode）：mode_volume_day_start/end、mode_volume_price_min、
#     mode_volume_demand_min、mode_volume_herd_floor、mode_volume_hold_price_min、
#     mode_volume_hold_cash_min、mode_scale_day_start/end、mode_scale_entry_herd、
#     mode_scale_hold_herd；
#   d6 容量分支门（_d6_checkpoint）：d6_herd_floor、d6_cash_min、
#     d6_straw_price_min、d6_straw_demand_min；
#   阶段窗（_stage_of）：stage_p1_due、stage_p2_freeze、stage_p3_end、
#     stage_p4_end；
#   P3 运行态姿态（熔断/晚季雇工）：fuse_money_floor、crew_late_day、
#     crew_late_cap；
#   卖出杠杆（market 卖出计划器）：sell_price_discount、sell_batch_mult、
#     p4_force_tier；
#   钱包门档（v3 K2，2026-09-20；read-site：strategy._cash_gate_ok 黎明
#     现金门 + market 买畜环 reserve_total + market COW_BUY_RESERVE 尾段
#     d8+——前段 800/550 早起动日程冻结）：liquidity_floor、cow_buy_reserve；
#   买畜时点（strategy._herd_target + market 买畜环）：herd_day_shift、
#     herd_start_day、animal_buy_last_day_shift；
#   P1 分支强制（_b_branch_adjust）：b_branch_force。
# ===========================================================================
PLANNER_ENABLED = False        # DTSP 总旗：False=与 v13.8 逐字节等价（默认）
PLANNER_OVERRIDES = {}         # 计划覆盖寄存器（旗开时 _plan_knob 消费）


# ===========================================================================
# 【中文】v15 波次剧本模式旋钮（2026-09-20「点火重构」M-A）
# ---------------------------------------------------------------------------
# 波次剧本引擎（src/wave.py）的总闸：默认 False=全部消费点与现役
#   v13.8/v14.2 逐字节等价（旗关黄金动作哈希钉住）；DTSP 计划经
#   "PLANNER_OVERRIDES.wave_mode" 键开启（planner/wave_script.py 发射）。
# 消费点清单（全部走 _plan_knob / globals().get 钩子，wave.py 缺席时死路）：
#   strategy._macro_plan  计划补丁（地/畜/crew/瓜波日历）
#   strategy._crew_target crew 阶梯（d5=6/d8=8/d10=12/d11=13）
#   strategy._field_alloc 瓜每象限帽（开局 7 株）
#   market._market_orders 波次市场事件 + SELL 影响分/终局 glut 排序
#   entry.agent           flush 日 SELL 先于 BUY（同回合变现融资）
# ===========================================================================
WAVE_ENABLED = False


# ===========================================================================
# 【中文】v14.3-sellrace 售卖竞速旋钮（2026-09-20「最后一刀」；round-24 近
# 失带直击）。全部默认值=旗关，与 v14.2 逐字节等价（旗关黄金钉住）；离线
# 实验/发射态经 "PLANNER_OVERRIDES.sellrace_mode" 等键开启。**不加新轴进
# DTSP 计划空间**（plans.py 键面不动——这些键不在 governed 全名面内，逐黎
# 明 apply_overrides 不触碰预置值，fail-open restore_pristine 清寄存器即
# 安全回落）。
# 校准出处（references/digests/ 已登记原件）：
#   * V16-RC5 premium-market-lead（meta-notebook-mining-20260920.md §3.3）：
#     对 MELON/MILK/STRAWBERRY/WOOL 在"本回合无匹配城镇需求"时把下回合
#     计划卖单的一部分前移一回合（两回合总量守恒）；notebook 实证本地
#     60/60、对 Kaito V27 24-0（+18,993）。本回合城镇需求=引擎逐字镜像
#     （商店每 4 步抽、单产品店 2 件；镇中心每 24 步每非肥料品 1 件）。
#   * Z2M c94/c95：fertilizer-only 前插 cap 10（held-out 900 局 96.7%
#     WR）；一回合肥料预售 ≈5,300-5,700 币翻转近镜像。WHEAT 明确不前插
#     （对手会买）。
#   * 2945 Farm VE1（fresh-sweep-20260920.md §2.1）：day-11 放羊=5 次剪毛
#     （17/20/23/26/29）而非 day-12+ 的 4 次。CARE 攒量（牛 3 奶/羊 4 毛）
#     经核对为我方 v14.2 在役语义（mission.py 对每头已喂且有剩余生产夜晚
#     的牲畜逐日 CARE——引擎 pending_care_bonus 自动攒 1/天、生产夜晚
#     1+bonus 兑现，牛 interval2→3 奶、羊 interval3→4 毛），不另改码。
# 消费点（全部走 _plan_knob，旗关恒回默认值）：
#   market._sellrace_leads      售卖前移（premium 四品 ≤50%/批 + 肥料 cap10）
#   market._market_orders 买畜环 day-11 放羊承诺（仅加快慢季羊日程）
# ===========================================================================
SELLRACE_MODE = False         # v14.3 总闸：False=与 v14.2 逐字节等价
SELLRACE_LEAD_FRAC = 0.5      # 前移量上限 = 当回合已计划卖量 × 此值（≤50%/批）
SELLRACE_ZERO_DEMAND_CAP = 18  # 零吸收线当日出清帽（件/回合；melon 类校日界）
SELLRACE_FERT_CAP = 10        # 肥料预售单回合上限（Z2M c94 口径）
D11_SHEEP_COMMIT = 0          # day-11 放羊承诺头数（0=旗关；值域 0-2）



def _plan_knob(name, default):
    """DTSP 计划旋钮惰性读取：旗关恒回默认值（v13.8 等价路径）。

    寄存器值显式 None 视为"未覆盖"回默认（plans 侧禁止发 None，此处
    双保险防规划器 bug 把现役行为改坏）。"""
    if not PLANNER_ENABLED:
        return default
    value = PLANNER_OVERRIDES.get(name, default)
    return default if value is None else value


# ===========================================================================
# 【中文】scheduler v1.3 §2-§4 实施旋钮（2026-09-02 W2：任务包全规格/求解器
# 抛光与喂食腿/执行器断言与幂等闸）——全部只服务影子件，执行权威仍在 v72
# ---------------------------------------------------------------------------
SHED_CAPACITY = 100            # 引擎镜像 shedCapacity（EOD 预算不等式的界）
LAND_PRICES_EMB = (1000, 2000, 4000)   # 引擎镜像 LAND_PRICES（Ch2 钱账分解）
# ---- §3.2 成路与喂食腿（Phase-A v2：簇-LPT 分区/溢出已由 EDF+预算制取代，
# OVERFLOW_IMBALANCE_TASKS 随之退役）----
FEED_LEG_CHUNK = 5             # 喂食腿：一次 PICKUP 携带的小麦数（拆腿粒度）
TWO_OPT_MAX_PASSES = 16        # 无死线尾段 2-opt 抛光的迭代上限
# ---- §4 执行器断言 ----
EXECUTOR_EOD_ASSERT = True     # EOD 投影断言（棚仓+随身 > 100 → REPLAN）
EXECUTOR_D1_ASSERT = True      # D1 站点 ETA 断言（ETA > deadline → REPLAN）
# ---- branch §8.2 熔断回退 ----
FUSE_MONEY_FLOOR = 300         # 段内钱包 < 此值 → 立即降 DEFENSIVE 运转参数包
# ---- OBS 置信帽（退役，2026-09-04 激进模式裁定）----
# V0 时代的静态帽（WHEAT/FERT/MILK/STRAW=0.4）把 P4 三档对四品类永久
# 钉死在回退态。v13.3 观察器重构后离线实测（60 局/31,320 样本）：
# validated fill Ch0 exact 0.9733、拐点滞后 0d、量级误差 0.0——静态帽
# 的存在依据消失。置信度回归 observer 自身的动态降信链（Ch1 残差连续
# 异常 ×0.75、EOD 不可归因 ≤0.4、异常归零）：那才是理想的"校准置信"。
# requested 口径 0.9241 的残余误差由消费方 conf≥0.5 门自担，不再静态
# 封顶（空 dict => est_opp_conf 直接返回动态 conf）。
OBS_HELD_CONF_CAP = {}
