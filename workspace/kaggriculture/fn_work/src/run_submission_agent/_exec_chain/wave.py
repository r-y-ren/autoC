"""迁移登记——run_submission_agent · _exec_chain/wave（B13，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/src/wave.py（旧树冻结，零字节变更）
源 sha256: 905735fc33f86e7a99a9d995b947fd7a0f14aae021685dd593668832a1944953
剥离清单（R10 死码不迁）: 2 项——①WAVE_OPENING_EOD_CASH_MAX（开局过夜现金帽
  死旋钮，全库零消费）；②WAVE_OPENING_SEEDS 的 WHEAT 死种子值 9（全库唯一
  消费点 _wave_melon_quad_cap 只读 .get("MELON", 7)，WHEAT 键零读取，
  dict 收缩为 {"MELON": 7}）。剥离处各留原地注记。
形态: 本文件 = 旧模块的迁移副本，落位 _exec_chain/（下划线开头=非函数文件区：
  exec 链基座件）；装载序位次=wave（entry 之前，见 load_agent_modules 的
  _MODULE_ORDER 真值）。除本登记头与登记过的删改外源码逐字复制。
上游: R1, R10（fn_docs/responsibility.md 功能块 run_submission_agent）
"""

# ===========================================================================
# 【中文·模块导览】src/wave.py —— v15「点火重构」波次日历剧本引擎（M-A）
# ---------------------------------------------------------------------------
# 范式（战略裁决 2026-09-20）：验证过的波次日历剧本为脑、现役四层调度器
#   （mission/solver/executor/market）为手。本模块是"脑"：把 top-10 持榜
#   bot v48 的"离线波次日历 + 首店身份路由 + 终局清仓"翻译成我方语义——
#   剧本只产出【计划补丁】（走现役 _macro_plan 的 plan dict）与【市场事件】
#   （走现役 _market_orders 计划器/预算闸），自身不携带任何路由/寻路
#   （island-ga 教训"走路值一半"——执行仍全权归四层 solver）。
# 旗关等价（硬约束）：全部消费点走 _plan_knob("wave_mode", WAVE_ENABLED)
#   + globals().get 钩子模式（本模块不在命名空间时钩子死路）——
#   WAVE_ENABLED=False（默认）时与 v13.8/v14.2 逐字节等价
#   （scripts/planner_flagoff_golden.py 黄金动作哈希钉住）。
# 校准出处（全部 references/digests/ 已登记原件，逐条内嵌）：
#   * v48 default 路由逐日表（public-bot-reverse-eng-20260920.md §2.1/§3）：
#     d0 花到 ~190 过夜、4-5 头定时畜、瓜 7 株 d10 一次性 42 单、
#     d6 羊毛 flush→买地#1+牛、d10 瓜 flush→买地#2+crew12、crew 阶梯
#     6(d5)/8(d8)/12(d10)/13(d11)、d26-29 麦倾销+glut 清仓。
#   * island-ga envelope 基因组（MIT，opensource-bot-hunt-20260920.md §2A）：
#     d0 = COW×2+SHEEP×2、NW 即日播种、NE d6/SW d10 解锁、SE 不开、
#     雇人平台 12、hour0 卖/hour1 买、sellpol=hybrid。
#   * kaggri 一行开局实证（同 digest §2C）：d0-d3 现金周转速度 > 任务排满
#     ——少买麦种（9 档）、早卖（肥料 d1 起日结=现役原生）。
#   * gytdrop 终局（同 digest §2D，只学思路）：d29 hour14 起全员变现入棚
#     （现役 mission last-day 模板已覆盖，本模块只补市场侧清仓排序）。
#   * 2945 Farm 微机制（fresh-sweep-20260920.md §2.1）：day-11 放羊=5 次
#     剪毛（yarn 世界 d11 六羊承诺）；CARE 攒量由 crew 阶梯承载；
#     同序号 slot 锁步=下单顺序即价格顺序（flush 日 SELL 先于 BUY 融资）。
# 胜负口径：终局钱数定胜负（赢 $1=赢）——剧本优化目标是点火时点与资本
#   波次兑现，不追求 margin。
# ===========================================================================

# ---- 剧本日历常量（出处逐条内嵌；旗关默认不消费）--------------------------

# crew 阶梯（v48 default：6(d5)/8(d8)/12(d10)/13(d11)；gytdrop d0 雇 5；
# 2945 雇佣按边际 fib 定价——d10 的第 12 手全天 ≈$376 可负担）。
# d13 起持平 12（XRAY 雇佣共识 d13-30 12 手）；晚季降编仍归现役
# CREW_LATE_DAY/CREW_LATE_CAP 原生通道。
WAVE_CREW_LADDER = ((0, 5), (5, 6), (8, 8), (10, 12), (11, 13), (13, 12))

# d0 开局（island-ga 基因组主锚 + v48/任务包瓜量）：
#   畜：COW×2 + SHEEP×2（4 头定时畜：羊毛 d6 首产 + 牛奶 d8 首产双炸弹）；
#   瓜种 7（v48 default；3100+ 带 d0-4 人均 6.7）；
#   麦种 9（island-ga d0=9；kaggri 一行教训=少买，5-10 带内取 9）；
#   饲料保险 BUY_PRODUCT WHEAT×5（Z2M：必须第一批 slot——对手抢购抬价
#   只买得起 4 份→d2 死畜，4 大败平均 -13,606）。
WAVE_OPENING_HERD = {0: {"COW": 2, "SHEEP": 2}}
# 【R10 迁移剥离，详见文件头剥离清单】WHEAT 死种子值（9）不迁——
# 全库唯一消费点 _wave_melon_quad_cap 只读 .get("MELON", 7)。
WAVE_OPENING_SEEDS = {"MELON": 7}
WAVE_OPENING_WHEAT_INSURANCE = 5
# 【R10 迁移剥离，详见文件头剥离清单】原开局过夜现金帽死旋钮
# （全库零消费）不迁。

# 资本波次（剧本核心——点火=日历事件，不是现金阈值）：
#   d6 羊毛首产 flush（4 羊×6=24 单 ≈$4.8k）→ 当天买地#1(NE $1k)+5 牛；
#   d10 瓜 flush（7 株×6=42 单 ≈$9k+）→ 当天买地#2(SW $2k)+草莓×13+crew12；
#   奶 d8 起上市（d0 牛首产）；d11 yarn 世界六羊承诺（2945 VE1：day-11 放
#   羊=5 次剪毛 17/20/23/26/29）。第 4 象限永不买（island-ga se=None）。
WAVE_HERD_WAVES = {6: {"COW": 5}}
WAVE_HERD_WAVES_YARN = {11: {"SHEEP": 6}}
# land_plan_override 键=quads_now → (due_day, fund)：地#1 due d6（羊毛 flush
# 当天）、地#2 due d10（瓜 flush 当天）；fund=地价+300 工作垫。
WAVE_LAND_WAVES = {1: (6, 1300), 2: (10, 2300)}

# flush 变现窗（首产即卖、当日卖清——v48 清仓纪律；melons 越窗不再强卖，
# 归现役门控）。同序号 slot 锁步下 flush 日 SELL 先于 BUY 入队（同回合
# 变现融资买地/买畜——meta-notebook §5"SELL 排 BUY 前可即时融资"）。
WAVE_FLUSH_DAYS = {"WOOL": (6, 7, 8), "MELON": (10, 11)}
WAVE_MILK_FLUSH_FROM = 8
WAVE_SELL_FIRST_DAYS = (6, 10)

# 终局（v19_terminal 语义）：d26-29 麦倾销+glut 权重清仓；终局卖单排序分
# = (1+对手 exposure 份额) × glut 权重 × 现价 × log(1+q)（瓜 3.6/毛 3.2/
# 莓 2.0/奶 2.0/蛋 1.5 = above 曲线曲率排序，digest §4）。
WAVE_GLUT_WEIGHTS = {"MELON": 3.6, "WOOL": 3.2, "STRAWBERRY": 2.0,
                     "MILK": 2.0, "EGG": 1.5, "CARROT": 1.0, "FERTILIZER": 1.0}

# 首店身份路由（v48 router 语义：第一个解锁商店一次性定整局经济线）。
# 引擎每 3 天解锁一家（step72=d3 首家）。路由只在剧本模式内消费。
WAVE_ROUTE_BY_SHOP = {
    "YARN_STORE": "WOOL",        # 羊线：羊毛唯一商店 → d11 六羊承诺+羊倾斜
    "FARMERS_MARKET": "FIELD",   # 田线：近 default（v48 farm_fast）
    "BAKERY": "CAPITAL",         # 资本线：奶/蛋+麦（v48 bakery_capital）
    "PIZZA_SHOP": "CAPITAL",     # MILK/TOMATO/WHEAT → 资本（奶三店需求）
    "ICE_CREAM_SHOP": "FIELD",   # 莓/奶/麦 → 田线
    "BRUNCH_SPOT": "FIELD",      # 莓/蛋/麦 → 田线
    "SMOOTHIE_SHOP": "FIELD",    # 莓/奶 → 田线
    "PET_CAFE": "FIELD",         # 萝卜 → 田线
}

# ---- 进程内路由锁存（按玩家分键；时钟倒退=新对局自动重建）----------------
_WAVE_ROUTE_MEM = {}


def _wave_enabled():
    """剧本总闸：旗关（PLANNER_ENABLED=False / 无覆盖）恒 False →
    全部消费点与现役逐字节等价。"""
    return bool(_plan_knob("wave_mode", WAVE_ENABLED))


def _wave_route(player, obs):
    """首店身份路由（latched）：第一个解锁商店的身份一次性定线。
    返回 "WOOL"|"FIELD"|"CAPITAL"|None（None=商店尚未解锁）。"""
    shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    st = _WAVE_ROUTE_MEM.get(player)
    if st is None or day_of_obs(obs) < st.get("day", 1 << 30):
        st = {"day": day_of_obs(obs), "route": None}
        _WAVE_ROUTE_MEM[player] = st
    if st.get("route") is None and shops:
        st["route"] = WAVE_ROUTE_BY_SHOP.get(sorted(shops)[0], "FIELD")
    return st.get("route")


def day_of_obs(obs):
    """obs 当日（容错缺键）。"""
    return int(_get(obs, "day", 0) or 0)


# ---- 计划补丁（_macro_plan 消费；剧本→现役计划层的唯一入口）---------------

def _wave_overlay(player, obs, day, plan):
    """波次剧本的当日计划补丁。返回新 plan dict（绝不原地改）。

    补丁面（全部是现役计划层已消费的键）：
      land_plan_override   地#1/#2 的日历波次（d6/d10，见 WAVE_LAND_WAVES）
      opening_seq_override 开局+波次畜群（d0 2C+2S / d6 +5C / yarn d11 +6S）
      melon_total_cap      7 株 d10 一次性 42 单的瓜波（配合 _wave_melon_quad_cap）
      crew_cap             13（crew 阶梯的帽；阶梯值走 _wave_crew_target）
      wave_route           首店身份路由标签（遥测/测试消费，信息性）
    旗关恒原样返回（byte-identical）。
    """
    if not _wave_enabled():
        return plan
    out = dict(plan)
    route = _wave_route(player, obs)
    out["wave_route"] = route
    # 【v15 反事实二跑教训】买地不接管：native B2 的 land_plan_override
    # 已经 d1 起步（_b_branch_adjust {1:(1,1700)}），v48 的 d6/d10 地日程
    # 是它自家小农场的时间线——剧本若把 due 推迟到 d6/d10 反而比 native
    # 晚、少长地。WAVE_LAND_WAVES 保留为 v48 参照常数（校准互检用），
    # 不再写进计划补丁。剧本的资本波次 = 畜群波次（d6 五牛/d11 六羊，
    # 带 feed+cash 闸）+ flush 变现 + 卖单排序。
    herd_seq = {k: dict(v) for k, v in WAVE_OPENING_HERD.items()}
    for k, v in WAVE_HERD_WAVES.items():
        merged = dict(herd_seq.get(k, {}))
        merged.update(v)
        herd_seq[k] = merged
    if route == "WOOL":
        for k, v in WAVE_HERD_WAVES_YARN.items():
            merged = dict(herd_seq.get(k, {}))
            merged.update(v)
            herd_seq[k] = merged
    out["opening_seq_override"] = herd_seq
    # 【v15 反事实教训】瓜帽不缩：剧本不再写 melon_total_cap（首跑把
    # native 12 缩到 7 → 瓜 flush 资本事件减半）。_wave_melon_quad_cap
    # 只放开每象限帽，总量归 native 计划面。
    out["crew_cap"] = max(13, int(out.get("crew_cap") or 0))
    return out


def _wave_burst_gate_ok(day, money, sys_wheat, herd_total, spec,
                        shed_count=None):
    """剧本畜群波次闸（d>0 的 opening_seq 波次消费前过滤）：
      * feed：系统小麦 ≥ 现 herd + 新增头数（买得起喂不起=逃亡死损，
        不是 island-ga 说的零成本静默失败——牲畜会饿逃）；
      * cash：money ≥ 采购额 + 600 过夜垫；
      * shed：棚位 + 2×新增 ≤ 88（买入的牲畜先落棚等 PLACE，一次 5 头
        =+10 棚位；满棚压力是 v15 注入回归 105375966 塌方的机制——
        EOD 满仓销毁静默吃库存）。
    d0 开局波次不过此闸（native OPENING_RESERVE 语义照旧）。
    旗关恒 True（不过滤——B1 native 步速语义不受影响）。"""
    if not _wave_enabled():
        return True
    if int(day) <= 0:
        return True                  # d0 开局波次走 native OPENING_RESERVE 语义
    spend = 0
    new_heads = 0
    for animal, n in (spec or {}).items():
        spec_meta = ANIMALS.get(animal)
        if spec_meta is None or n <= 0:
            continue
        spend += int(n) * int(spec_meta["cost"])
        new_heads += int(n)
    if new_heads <= 0:
        return True
    if int(sys_wheat) < int(herd_total) + new_heads:
        return False
    if float(money) < spend + 600.0:
        return False
    if shed_count is not None and \
            int(shed_count) + 2 * new_heads > 88:
        return False
    return True


def _wave_melon_quad_cap(native_cap):
    """_field_alloc 瓜每象限帽钩子：剧本模式放开到开局瓜波株数（NW 单象限
    也要种满 7 株——v48 default 瓜 7 全在首象限）；旗关恒回 native。"""
    if not _wave_enabled():
        return native_cap
    return max(int(native_cap), WAVE_OPENING_SEEDS.get("MELON", 7))


def _wave_crew_target(day, herd, cap, native_target):
    """_crew_target 钩子：剧本 crew 阶梯只【抬升】不缩减——
    target = max(阶梯(day), native_target) 再受帽约束。
    教训（v15 反事实首跑 2026-09-20）：v48 的 crew 数值是它自家小田的
    量（d0=2）；我方 native d1-4 已爬 7-8，剧本若把 d5-9 压到 6-8 会
    浇水饿荒、瓜 flush 全灭（melon 70/96 教科书复现）。阶梯的定位 =
    d10/d11 的 12/13 满编提前钉死 + CARE 覆盖地板。旗关恒回 native。"""
    if not _wave_enabled():
        return native_target
    ladder_target = 2
    for from_day, hands in WAVE_CREW_LADDER:
        if day >= from_day:
            ladder_target = hands
    target = max(ladder_target, int(native_target), int(herd))
    return min(int(cap), target)


# ---- 市场事件（_market_orders 消费；走现役预算闸/committed_spend 台账）----

def _wave_market_events(obs, farm, private, day, hour, shed, prices):
    """波次市场事件（剧本模式专属单据，append 进现役订单队列）：
      d0   饲料保险 BUY_PRODUCT WHEAT×5（第一批 slot，Z2M 死线保险）；
      d6-8 羊毛 flush：SELL 全部棚仓羊毛（首产即卖、当日卖清）；
      d10-11 瓜 flush：SELL 全部棚仓瓜（一次性资本事件；melon 曲线 T=300
           ——42 单仅压价 ~18/件，分批反而喂低自己的下一批）；
      d8+  奶 flush：SELL 全部棚仓奶（首产即卖；现役 _milk_gate 的 105 门
           在 production 日本来就开，这里只去掉批量节流）。
    全部钳到棚仓现货（没收割到棚就不卖——自然逐回合重试直到清空）；
    旗关恒 []。终局 d29 归现役清算+本模块 glut 排序，不在此重复。
    """
    if not _wave_enabled():
        return []
    events = []
    if day == 0 and hour <= 2:
        events.append(["BUY_PRODUCT", "WHEAT",
                       int(WAVE_OPENING_WHEAT_INSURANCE)])
    if day in WAVE_FLUSH_DAYS.get("WOOL", ()):
        n = _shed_int(shed, "WOOL")
        if n > 0:
            events.append(["SELL", "WOOL", n])
    if day in WAVE_FLUSH_DAYS.get("MELON", ()):
        n = _shed_int(shed, "MELON")
        if n > 0:
            events.append(["SELL", "MELON", n])
    if WAVE_MILK_FLUSH_FROM <= day < ENDGAME_DAY:
        n = _shed_int(shed, "MILK")
        if n > 0:
            events.append(["SELL", "MILK", n])
    return events


def _shed_int(shed, item):
    n = _get(shed, item, 0)
    return int(n) if isinstance(n, (int, float)) and n > 0 else 0


def _wave_sell_first(day):
    """flush 日同回合 SELL 先于 BUY 入队（同序号 slot 锁步：先卖回血再买
    ——当日 flush 现金直接融资买地/买畜）；旗关恒 False。"""
    if not _wave_enabled():
        return False
    return day in WAVE_SELL_FIRST_DAYS


# ---- 市场结构（M-B）：同回合 SELL 影响分排序 + 终局 glut 排序 -------------

def _wave_sell_impact_key(order, prices):
    """同回合 SELL 槽位影响分（v22_market_impact 语义）：先卖"跌得最快的"
    ——impact = q × (现价 − 卖后价)。同序号 slot 锁步下队列位置即成交顺序，
    高影响单排前=在自家洪水前落袋。返回 (−impact, item) 升序键。"""
    item = order[1]
    q = int(order[2] or 0)
    price = float(_get(prices, item, BASE_PRICE.get(item, 0)) or 0.0)
    if q <= 0 or price <= 1.0:
        return (0.0, item)
    try:
        off_now = _offset_from_price(item, price)
        price_after = _price_at_offset(item, off_now + q)
    except Exception:
        return (0.0, item)
    impact = q * max(0.0, price - price_after)
    return (-impact, item)


def _wave_opp_supply(obs):
    """对手公开供给签名（v19_terminal projected_shed 的公开代理）：
    对手 tiles 里作物格→作物、牲畜→产品 的计数。"""
    counts = {}
    farms = _get(obs, "farms", []) or []
    player = _get(obs, "player", 0)
    for i, f in enumerate(farms):
        if i == player:
            continue
        for row in _get(f, "tiles", []) or []:
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                if _get(tile, "kind", "") == "PLANT":
                    crop = _get(tile, "crop", "")
                    if crop in BASE_PRICE:
                        counts[crop] = counts.get(crop, 0) + 1
                elif "animal" in tile:
                    product = ANIMALS.get(_get(tile, "animal", ""), {}) \
                        .get("product", "")
                    if product in BASE_PRICE:
                        counts[product] = counts.get(product, 0) + 1
    return counts


def _wave_terminal_sort_key(order, prices, opp_supply):
    """终局（d29/718 语义）卖单排序分：全量替换式重排——
    score = (1 + 对手 exposure 份额) × glut 权重 × 现价 × log(1+q)，
    高分先卖（对手也在抛的、曲线崩得快的先落袋）。返回 (−score, item)。"""
    item = order[1]
    q = int(order[2] or 0)
    price = float(_get(prices, item, BASE_PRICE.get(item, 0)) or 0.0)
    glut = float(WAVE_GLUT_WEIGHTS.get(item, 1.0))
    ours = 1 + q
    theirs = 1 + int(opp_supply.get(item, 0))
    exposure = (theirs - 1.0) / float(ours + theirs)
    score = (1.0 + exposure) * glut * max(0.0, price) * math.log(1.0 + q)
    return (-score, item)


# ---- 消费点适配（供 strategy/market/entry 以 globals().get 钩子调用）------

def _wave_merge_sells(merged, prices, day, last_day, opp_supply):
    """sell 槽位排序入口（market._market_orders 合并步消费）：
      非 last_day：≥2 张 SELL 时按影响分降序重排 SELL 子集（非 SELL 单
        原序保留——plan_market_orders 保持原列序，重排因此是真实生效的）；
      last_day（718 语义）：glut×exposure×价×log(q) 全量排序替换。
    旗关恒原序返回。稳定键 (−score, item) 保证确定性。"""
    if not _wave_enabled():
        return merged
    sell_idx = [i for i, o in enumerate(merged)
                if isinstance(o, list) and o and o[0] == "SELL"]
    if len(sell_idx) < 2:
        return merged
    if last_day:
        keyed = sorted((merged[i] for i in sell_idx),
                       key=lambda o: _wave_terminal_sort_key(o, prices,
                                                             opp_supply))
    else:
        keyed = sorted((merged[i] for i in sell_idx),
                       key=lambda o: _wave_sell_impact_key(o, prices))
    out = list(merged)
    for i, order in zip(sell_idx, keyed):
        out[i] = order
    return out
