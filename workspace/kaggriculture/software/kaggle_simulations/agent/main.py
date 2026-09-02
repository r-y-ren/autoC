# ===========================================================================
# 【中文总览】Kaggriculture 参赛作品 —— "轮作牧场"(rotation ranch) 策略
# ===========================================================================
# 本文件是自包含的 Kaggle 提交入口：仅用 Python 标准库，不依赖本地 kgenv
# 包，可直接上传：
#     kaggle competitions submit kaggriculture -f main.py
# 上传后位于 /kaggle_simulations/agent/main.py（官方 kit 约定）；文件中
# 最后一个可调用对象 agent(obs) 即引擎认定的入口。
#
# ── 策略四层架构（自上而下）───────────────────────────────────────────────
#   1) 宏观计划层  _decide_mode / _macro_plan
#      每天第一回合基于公开状态（价格、已解锁商铺、双方农场）做确定性门控，
#      在三种经济模式中选一个"建设什么"的计划：
#        DEFENSIVE   保守的 r4 轮作-牧场参数框架（默认/一切失败回退态）
#        VOLUME_CROP 96-110k 段的大田经济（42 格草莓 + SE 象限 + 15 人雇工）
#        SCALE_RANCH 13-17 头大家畜的扩栏经济（NPV 上限抬到 18）
#      另有 WHEAT_FARM 小麦专精实验模式（默认关闭，V9_WHEAT_FARM_ENABLED）。
#   2) 规划层      _field_alloc / _herd_target / _crew_target / _wheat_cap
#      牧场贴着每个已解锁象限的仓库口"环形"布局；田地按
#      （物候窗口, 价格红线, 每象限上限）三门控做作物轮作规划，小麦只是
#      "饲料底仓"，其余地块流向价格最高的轮作作物。
#   3) 任务与调度层 _build_tasks → _schedule_units(_v72)
#      先把本回合所有可做的事生成任务表（带价值 v 与红线标记 red），再由
#      两阶段调度器分派给农场主与雇工：
#        Phase A 红线一票否决 —— "今晚会死"的义务（断水植物/断粮牲畜/
#                        末日归还）由最近工人优先覆盖，不看权重；
#        Phase B 价值匹配    —— Score = V - 行走成本 - 跨象限惩罚
#                        + 载货亲和 + 粘滞奖励，全局贪心一对一认领。
#   4) 市场层      _market_orders + _market_gates + plan_market_orders
#      买地/买畜/买种/外购饲料按"资金门槛 + 确认步速 + 死价冻结"下单；
#      卖货遵循"选择性干预"三门态：强势需求→囤到门槛价、零吸收→分析性
#      止损、流动性压力→小批折价出清；最后经 plan_market_orders 按官方
#      引擎语义（逐件成交、当前曲线价、单日 10 单）做预算截断。
#
# ── 安全哲学（四条不可逾越的红线）─────────────────────────────────────────
#   * 生死红线：今晚不浇水就枯死/不喂食就逃走的任务永远优先于一切收益；
#   * 死价红线：产品曲线死了（价格低于地板）绝不扩产、绝不死扛囤货；
#   * 流动性底线：任何采购后钱包保留下一黎明雇工费 + 饲料裕量，
#     绝不重演"一回合 3256→16"的破产螺旋（线上 ep 103783585 实测）；
#   * 永不崩溃：入口整体 try/except，任何内部异常都返回合法 PASS 空单。
#
# ── 阅读指引 ──────────────────────────────────────────────────────────────
#   文中英文注释携带每个参数的实验证据（回放画像/迭代门控的实测数字），
#   是原始档案，请勿删改；本批中文注释是结构导览与机制解释，两者互补。
#   建议顺序：常量区(策略旋钮) → _decide_mode → _field_alloc →
#             _build_tasks → _market_orders/_market_gates →
#             _schedule_units_v72 → agent。
# ===========================================================================
# ---------------------------------------------------------------------------
# v7 candidate (weed-reclaim experiment tree, NOT the submission path).
#
# Round-1 single-variable gates (labels v7-c1/c3/h, seeds 101-102):
#   C1 all-day planned DIG   18W-22L -89.7k, one -92k cell where DIG
#                            measurably starved WATER (656->579, lapse
#                            17->34, escapes 3->6)  -> mechanism risk
#   C3 all-weed DIG          20W-20L -109.0k        -> REJECTED
#   H  plant-EOD guard       21W-19L -31.6k, pool_wr 1.0 but no stack gain
#                            -> EXCLUDED (minimal-change)
# Round-2 (seeds 101-104, 80 pairs each; paired diffs are chaos-dominated
# -- any day-0 perturbation reshuffles both seats +-30-90k, worst-cell
# forensics showed BETTER fundamentals with LOWER reward -- so the
# unpaired win indicators decide):
#   C2 late-window planned DIG (hour>=20, behind red lines):
#                            pool_wr 0.975 / worst 0.875 / disaster 0.0125
#   R  rotation-DIG of finished strawberries (+ stop watering/fertilizing
#      them; _crop_future_value had no max_yield cap and paid dead tiles
#      to the horizon):  tight +-2.5k band, indicators tie champion
#   C2R (THIS FILE):        pool_wr 1.0 / worst 0.875 @monster / disaster
#                            0.0 -- best indicators of any candidate
#   C2RH:                   identical indicators, more divergence -> H out
# v7.2-V1 (merged): VOLUME entry herd-readiness floor (>= 10 head).
#   Seed-103 forensics (both seats -32k/-46k vs two_quad_denser): the
#   entry fired on a 4-5-head ranch, ~4800 of field capex met a ~200
#   wallet, crew disbanded and animals starved (the P5 spiral class).
#   Ablation vs C2R: 20W-5L-63T net +319k (63/88 cells byte-identical --
#   surgical, not chaos), the 103 cells flipped to +32k/+40k; full gate
#   87W-1L with two_quad_denser 8-0.
# Everything else is the v6 submission byte-for-byte.
# ---------------------------------------------------------------------------
# v6 candidate (r5-P6 development tree, NOT the submission path).
#
# v6-1 (single variable F): strawberry per-quad cap 6 -> 8 under the
# UNCHANGED 18-tile total cap (a wider pre-SW field: 8/16 tiles at
# 1/2 quads, still 18 at 3 quads -- F2's 24-tile total measured
# -280k over 40 cells and was REJECTED; the total cap is load-bearing)
# from the round-3 monster cross-profile after five
# single-variable iteration gates vs the new wheat_straw_monster sparring
# partner (labels v6-*-vs-monster / v6-*-fullpool in
# exports/logs/iteration_gate_log.jsonl):
#   A crew-10-from-d0     3W-5L, -123.6k total  -> REJECTED (burns the d0
#     herd-burst cash; the r3 ramp is load-bearing)
#   B wheat-money 8/quad  byte-identical no-op  -> structural (the defensive
#     frame has no free tiles; the monster's wheat volume comes from
#     external-feed structure, not a quota knob)
#   F strawberry 8/quad   8W-0L vs monster (+83.0k), full pool 38W-2L,
#     paired vs r5 +78.8k over 40 cells              -> MERGED HERE
#   F2 total cap 24       -280k vs F (melon -62k x2, template -37k x2:
#     the 24-tile 3-quad field crashes joint markets)  -> REJECTED
#   D wheat-last-day 26   5W-3L (+58.1k, below baseline +66.4k) -> rejected
#   F+D                   identical to F on both gates      -> minimal-change
#     discipline keeps F only
# Everything else is the r5 submission byte-for-byte (the macro-plan layer,
# rollout safety net, red-line scheduler and market gates unchanged).
# ---------------------------------------------------------------------------
"""Kaggriculture submission agent -- "rotation ranch" strategy (r5, P4).

r5-P4 macro-plan layer: the round-3 public ladder's next band (96-110k
wheat-strawberry economies) is outside the r4 parameter frame, so a
deterministic daily gate now selects between three economy modes --
DEFENSIVE (the conservative r4 parameter frame), VOLUME_CROP (42-tile
strawberry ceiling + SE quadrant + crew 15) and SCALE_RANCH (NPV herd
ceiling 18) -- from public state only (prices, shops, both farms).  The
micro executor (red-line tasks, value matching, market gates, safety
shield) is unchanged; the plan widens WHAT economy may be built, not how
a turn is played.

Self-contained: standard library only, no imports from the local kgenv
package, so the file uploads as-is to
    kaggle competitions submit kaggriculture -f main.py
and lives at /kaggle_simulations/agent/main.py (official kit convention).
The last callable defined in this file is the entry point (that is how
kaggle_environments picks the agent from a file).

r3 timing redesign (campaign III round 3, sub-wave r3-2).  The round-2
online replays (3 winners, 6 episodes, .tmp-online/round2/) crossed with
the m1 top-20 corpus (58 episodes / 116 seat profiles) pinned the OPENING
AND MID-GAME TIMING as the next-tier ticket, not the ranch structure the
m3 engine already had (deep dive: exports/online/round2_winner_deep_dive.md).
Four phase changes, each with >=3-game profile evidence:

  R3-1 d0 capital allocation: 116/116 top-20 seats and 3/3 round-2 winners
      put 1800-2200 of the 3000 start into 4-5 head ON DAY 0 (2C+2S here,
      1800; arminhej96 5C/2000, 朝闻夕死 + Danila 3C+2S/2200), seeds from
      the leftovers.  First milk lands d8-9 instead of d10+ (measured m3:
      1 sheep on d0, first milk d10, d12 money ~0.4k vs winner band 1.5-8k).
  R3-2 herd deadline: >=12 head by d11 with a 14 ceiling (8C+6S -- winners
      peak 13-17; top-20 med 12 / p75 15).  The m3 plan (11 head, done
      d13-15) never reached 12 at all.  Counter-example checked: Anthaus
      hit 18 head but built d10-12 and lost -- timing, not size, is the
      ticket, so the cap stays 14 and the deadline does the work.
  R3-3 strawberry cadence: plant from day 5 (not day 0 -- the d0 cash
      belongs to the herd burst), 15-20 tiles by d11-13 (cap 6/quad on 3
      quadrants = 18; winners 16-23; top-20 peak med 36 starves the
      feed/care labour budget, so ~20 is the ceiling, not the target).
  R3-4 crew 12: winners hold 12 hands from d7-11 (Danila crew 12 @ d7;
      top-20 9.4-9.9 hires/day).  The m3 ramp peaked at 10.  _crew_target
      follows the herd (CARE/FEED/COLLECT_FERTILIZER scale with head):
      12 once the herd plan is >=12, the pinned m3 ramp as the floor.
      CARE discipline is unchanged full coverage (issue = head/day, no
      oversending -- CARE on a cared animal is an engine no-op).
  Kept from the winners' table deliberately: feed guardrail (gap-fill at
      <=36, ~15u/day cadence; winners 102-462u @ 33-34), 3 quadrants (NE
      d4 / SW d7 -- the m3 plan already sits inside the winner d5-11 band),
      d28+ stop-feed/stop-plant liquidation, milk clear-through gate 105
      and wool gate 150 (the milk/wool hoard-split is a low-confidence
      style item -- 3 winners, 3 different splits -- and the m2
      clear-through discipline measurably dominates the joint-dairy meta),
      daily fertilizer collection sold promptly (61-85 realised; winners
      9.8-18.5k/season -- an income line the m2 engine left on the table).

Online-feedback redesign (campaign III m3).  The m2b dairy engine won the
legacy pool 31W-1L but dropped the m2 online-style pool (dev eval seed 101:
template_wheat 0-2, self_feed_ranch 0-2, crop_rotator 1-1; evidence
exports/eval_results.dev.json).  The m1 replay profiles of 60 official
episodes (120 seat profiles, exports/replay_profiles/, captured 2026-08-29)
pin four structural gaps, addressed as FM-O1..O4:

  FM-O1 (crop revenue share 21% vs top-20 median 54%) -> the field engine
      is a PRICE-KEYED ROTATION over wheat/strawberry/melon/carrot.
      Every non-wheat tile decision is gated by a live price floor
      (CROP_FLOOR) and a calendar phase (CROP_PHASE) copied from the
      ladder #1 "Crop Dusta" frame (26 consistent games: melon early /
      strawberry days 0-14 / filler afterwards; each with a price trigger).
      Wheat is no longer the whole field: it is the crash-proof FEED FLOOR
      (log glut curve -- it cannot be strategically crashed) sized by
      _wheat_cap, and everything the floor does not need goes to the
      highest-priced rotation crop that passes its floor.  Wheat itself
      joins the rotation as a money crop at 30+ (the rank-1 adaptive
      ladder runs a 0.45-0.62 wheat share at 36-42+; measured: the
      volume-farming archetypes monetize 400-520u/season).
  FM-O2 (labour 4.07 hires/day vs top-20 median 9.4, leader 9.7-9.9;
      herd all-cow vs the ladder's mixed ranches) -> labour plan ramps to
      10 hands/day (top-20 100/101 games sit at 9.1-10.2; a flat crew
      from day 1 measured BETTER than the rank-1's quadrant-scaled crew
      because our rotation opening needs tending before quadrant two
      exists), the herd becomes a SMALL MIXED RANCH with sheep primary
      (6 sheep + 5 cows = 11 -- between Milan's 6c+6s and Crop Dusta's
      7c+4s+1g; a 12-head plan measurably crowded out tending and the
      day-8 cash floor), bought INTERLEAVED by relative deficit so cows
      reach the day-8+ premium-milk window on time; the quadrant plan
      buys the third quadrant (NE day 4+, SW day 7+ -- the leader's land
      series; top-20 consensus 3 quadrants, 4th almost nobody) with the
      purchase fund protected from herd buys while it is pending.
  FM-O3 (feed autarky burned half the field on wheat the ladder buys
      externally: top-20 feed purchases 414-2732u/season at avg 26-32) ->
      wheat is a floor, not the field; the herd's gap is filled by
      GUARDRAILED external buying (FEED_BUY_MAX_PRICE, starvation cap 85
      preserved) and the m2 autarky bound on the herd target is released
      (money gate + pace + HERD_CAP bound it instead).  The wheat surplus
      sells from WHEAT_SELL_GATE with a cash-flow fallback -- the gate
      must never starve the land/animal capex plan (measured: 42 wheat
      hoarded at $516 while the NE purchase window lapsed).
  FM-O4 (endgame gain +7.2% of final money vs top-20 median +13.0%) -> a
      48h endgame window: from day 26 wool and from ENDGAME_DAY (28) every
      other premium hoard dumps in per-turn tranches (banking at the
      recovered price beats the day-29 joint liquidation floor), and
      FEEDING STOPS for animals that can no longer repay their wheat
      (unfed animals still produce their base unit; only the care bonus
      needs feed -- measured engine rule), freeing both the wheat (sold)
      and the labour (dump logistics).

  RED LINE (dead-price curves, generalized from the m2b demand-drought
  freeze): production never scales into a dead price.  Sheep buys freeze
  when WOOL < 90, cow buys when MILK < 90 (the m2b rule), and each
  rotation crop's planting freezes under its CROP_FLOOR.  The hoard side
  of the same red line: wool follows its curve (sq glut, T=105 -- the
  fastest crasher) and CUTS LOSSES at WOOL_CUT_LOSS once the curve turns
  (no yarn-store draws), never riding a dead curve into the day-29 floor;
  fertilizer sacks bid 70+ are SOLD rather than spent on wheat/carrot
  boosts worth ~60-70 (only the ~200-230/unit strawberry/melon boosts
  keep the sack -- the self-feed archetype sells 158u for +12.8k).

m2b fixes preserved (tests/test_strategy_m2.py, 26 checks, must not
regress):
  FM-1 ring pastures / feed-pipeline-first  -> kept; herd composition is
      new but pastures still hug the shed ring in every unlocked quadrant.
  FM-2 glut-tolerance discipline -> melon/strawberry return UNDER price
      floors + phase windows + small tranches; wheat stays the feed floor.
  FM-3 capital staging -> wheat-first opening kept (day-0 wheat before any
      animal), money-gated buys with cash reserves; rotation seeds are
      additionally staged behind the pending land fund.
  FM-4 fertilizer -> generalized: animal fertilizer self-consumes on the
      premium rotation crops (strawberry before each production day,
      melon at age 2; wheat/carrot only when the sack is cheap), bounded
      hoard (FERT_STOCK_CAP), gated release.
  Behavioural fixes kept verbatim: last day is liquidation-only (no
      capex, carried goods returned and sold first, infeasible harvests
      skipped); animal purchases confirmed by observed herd deltas
      (_buy_pace/_note_buy_order, per-seat per-episode state); shed
      inventory reserved across carriers; every quantity order positive;
      dawn hire burst within hour <= 2.

Selective-intervention sell gates (decide explicitly WHEN to hoard, WHEN
to release, WHEN to defend -- see _market_gates; every rule commented with
its official MARKET_PARAMS curve rationale).

An OPTIONAL pluggable LLM consultant hook (LLM_PROVIDER, default None) is
provided for local A/B experiments only (scripts/run_llm_ab.py); disabled
by default, never blocks, falls back to the heuristic gate.
"""

# --------------------------------------------------------------------------
# v9 local shadow telemetry (stdlib-only, action-transparent)
# --------------------------------------------------------------------------
# 【中文】本地"影子遥测"：只观测、不干预的纯旁路诊断通道。调用方可关闭
# 或注入 sink；sink 抛异常被吞掉，诊断永远不允许弄废一个提交回合。
# 以下 _telemetry_* 系列函数均服务于此目的，与策略决策完全解耦。
# Telemetry is deliberately a side channel.  It never mutates the observation,
# planner inputs, or returned action.  A caller may disable it or inject a
# process-local sink for replay tooling; a failing sink is ignored so a
# diagnostic cannot invalidate a submission turn.
import copy

TELEMETRY_ENABLED = True
_TELEMETRY_SINK = None
_TELEMETRY = {"players": {}}


def set_telemetry_enabled(enabled):
    """Enable/disable local shadow telemetry without changing strategy output."""
    global TELEMETRY_ENABLED
    TELEMETRY_ENABLED = bool(enabled)


def set_telemetry_sink(sink):
    """Inject a callable receiving one JSON-like turn event, or clear it."""
    global _TELEMETRY_SINK
    _TELEMETRY_SINK = sink if callable(sink) else None


def reset_telemetry():
    """Drop in-memory episode/day records and the optional sink reference."""
    global _TELEMETRY, _TELEMETRY_SINK
    _TELEMETRY = {"players": {}}
    _TELEMETRY_SINK = None


def telemetry_snapshot():
    """Return a detached snapshot suitable for local JSON serialization."""
    return copy.deepcopy(_TELEMETRY)


def _telemetry_day_template():
    return {
        "turns": 0,
        "moving_turns": 0,
        "effective_ops": 0,
        "valid_operations": 0,
        "movement_to_effective_ratio": 0.0,
        "pass_count": 0,
        "repeated_tasks": 0,
        "cross_quadrant_switches": 0,
        "cross_quadrant_choices": 0,
        "overdue": {"WATER": 0, "FEED": 0, "CARE": 0},
        "water_overdue": 0,
        "feed_overdue": 0,
        "care_overdue": 0,
        "zone_tasks_completed": {},
        "wheat_alive": 0,
        "wheat_harvested": 0,
        "external_feed_bought": 0,
        "minimum_cash": None,
        "shed_overflow": 0,
        "terminal_clearout": False,
    }


def _telemetry_player(player, day, hour):
    """Get a player-local telemetry state, resetting on a backwards clock."""
    key = str(player)
    state = _TELEMETRY["players"].get(key)
    if state is None or day < state.get("last_day", day) or (
            day == state.get("last_day", day) and
            hour < state.get("last_hour", hour)):
        state = {
            "episode": state.get("episode", 0) + 1 if state else 1,
            "last_day": day,
            "last_hour": hour,
            "last_task": {},
            "last_sector": {},
            "minimum_cash": None,
            "shed_overflow": 0,
            "wheat_harvested": 0,
            "external_feed_bought": 0,
            "days": {},
        }
        _TELEMETRY["players"][key] = state
    state["last_day"] = day
    state["last_hour"] = hour
    state["days"].setdefault(str(day), _telemetry_day_template())
    return state, state["days"][str(day)]


_TELEMETRY_UNIT_OPS = {
    "NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST",
    "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "FEED", "CARE",
    "COLLECT_FERTILIZER", "PICKUP", "DROP", "PLACE", "PASS",
}


def _telemetry_wheat_alive(farm):
    count = 0
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT" \
                    and _get(tile, "crop", "") == "WHEAT":
                count += 1
    return count


def _telemetry_inventory_total(private):
    total = 0
    for item, amount in (_get(private, "shed", {}) or {}).items():
        if isinstance(amount, (int, float)) and amount > 0:
            total += amount
    for inv in (_get(private, "inventories", []) or []):
        for item, amount in (inv or {}).items():
            if isinstance(amount, (int, float)) and amount > 0:
                total += amount
    return total


def _telemetry_units(farm):
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    units.extend(tuple(h) for h in (_get(farm, "hands", []) or []))
    return units, board


def _telemetry_record_turn(obs, farm, private, actions, tasks, trace, orders):
    """Record one observed decision and its planner shadow facts.

    Values are intentionally marked by the observation/action boundary: order
    quantities and task completions are requests visible locally before the
    engine applies them; wheat survival, cash, and shed pressure are observed
    state values from the same observation.
    """
    if not TELEMETRY_ENABLED:
        return
    try:
        player = _get(obs, "player", 0)
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        state, daily = _telemetry_player(player, day, hour)
        units, board = _telemetry_units(farm)
        operations = 0
        moving = 0
        passes = 0
        completed = {}
        wheat_harvested = 0
        action_targets = (trace or {}).get("action_targets", {})
        assigned = (trace or {}).get("assign", {})
        for ui, action in enumerate(actions or []):
            if not action:
                continue
            op = action[0]
            if op in MOVES:
                moving += 1
            elif op == "PASS":
                passes += 1
            elif op in _TELEMETRY_UNIT_OPS:
                operations += 1
                position = action_targets.get(ui)
                if position is None and ui < len(units):
                    position = units[ui]
                if position is not None and board:
                    zone = _quadrant_of(position[0], position[1], board)
                    completed[zone] = completed.get(zone, 0) + 1
                    if op == "HARVEST" and 0 <= position[1] < len(
                            _get(farm, "tiles", [])):
                        tile = _get(farm, "tiles", [])[position[1]][position[0]]
                        if isinstance(tile, dict) and \
                                _get(tile, "crop", "") == "WHEAT":
                            wheat_harvested += max(1, int(
                                _get(tile, "yield_units", 0) or 0))
            task_key = assigned.get(ui)
            if task_key is not None and state["last_task"].get(str(ui)) == task_key:
                daily["repeated_tasks"] += 1
            if task_key is not None:
                state["last_task"][str(ui)] = task_key
            if ui < len(units) and board:
                sector = _quadrant_of(units[ui][0], units[ui][1], board)
                previous = state["last_sector"].get(str(ui))
                if previous is not None and previous != sector:
                    daily["cross_quadrant_switches"] += 1
                state["last_sector"][str(ui)] = sector
        daily["turns"] += 1
        daily["moving_turns"] += moving
        daily["effective_ops"] += operations
        daily["valid_operations"] += operations
        daily["pass_count"] += passes
        ratio = daily["moving_turns"] / float(max(1, daily["effective_ops"]))
        daily["movement_to_effective_ratio"] = ratio
        cross_choices = int((trace or {}).get("cross_quadrant", 0))
        daily["cross_quadrant_choices"] += cross_choices
        overdue = {"WATER": 0, "FEED": 0, "CARE": 0}
        for task in tasks or []:
            op = (task.get("act") or [None])[0]
            if op not in overdue:
                continue
            if task.get("red") or op == "CARE":
                overdue[op] += 1
        for op, count in overdue.items():
            daily["overdue"][op] += count
            daily[op.lower() + "_overdue"] += count
        for zone, count in completed.items():
            daily["zone_tasks_completed"][zone] = \
                daily["zone_tasks_completed"].get(zone, 0) + count

        money = _get(farm, "money", None)
        if isinstance(money, (int, float)):
            state["minimum_cash"] = money if state["minimum_cash"] is None \
                else min(state["minimum_cash"], money)
            daily["minimum_cash"] = state["minimum_cash"]
        overflow = max(0, _telemetry_inventory_total(private) - 100)
        state["shed_overflow"] = max(state["shed_overflow"], overflow)
        daily["shed_overflow"] = state["shed_overflow"]
        alive = _telemetry_wheat_alive(farm)
        state["wheat_harvested"] += wheat_harvested
        daily["wheat_alive"] = alive
        daily["wheat_harvested"] = state["wheat_harvested"]
        bought = 0
        for order in orders or []:
            if len(order) >= 3 and order[0] == "BUY_PRODUCT" \
                    and order[1] == "WHEAT" and isinstance(order[2], (int, float)):
                bought += order[2]
        state["external_feed_bought"] += bought
        daily["external_feed_bought"] = state["external_feed_bought"]
        terminal = day >= SEASON_DAYS - 1 and \
            _telemetry_inventory_total(private) <= 0 and \
            all(order and order[0] == "SELL" for order in (orders or []))
        daily["terminal_clearout"] = bool(terminal)
        episode = {
            "turns": sum(d.get("turns", 0) for d in state["days"].values()),
            "moving_turns": sum(d.get("moving_turns", 0) for d in state["days"].values()),
            "effective_ops": sum(d.get("effective_ops", 0) for d in state["days"].values()),
            "pass_count": sum(d.get("pass_count", 0) for d in state["days"].values()),
            "repeated_tasks": sum(d.get("repeated_tasks", 0) for d in state["days"].values()),
            "cross_quadrant_switches": sum(d.get("cross_quadrant_switches", 0)
                                             for d in state["days"].values()),
            "wheat_alive": alive,
            "wheat_harvested": state["wheat_harvested"],
            "external_feed_bought": state["external_feed_bought"],
            "minimum_cash": state["minimum_cash"],
            "shed_overflow": state["shed_overflow"],
            "terminal_clearout": bool(terminal),
        }
        event = {"kind": "turn", "player": player, "day": day,
                 "hour": hour, "metrics": copy.deepcopy(daily),
                 "episode": episode}
        sink = _TELEMETRY_SINK
        if sink is not None:
            try:
                sink(copy.deepcopy(event))
            except Exception:
                pass
    except Exception:
        # Diagnostics are fail-open by design.
        return


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
HANDS_RAMP = ((0, 5), (1, 6), (3, 8), (6, 9), (12, 10))
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
# 上限 14 = 8 牛 + 6 羊（HERD_COMPOSITION）；超出 14 的扩张走
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
OPENING_RESERVE = 800    # cash kept besides the day-0 burst (m2b cushion)
# V-T1 ablation copy (tetsuya 08-31 opening shift): the day-0 herd burst is
# replaced by a staged day1-3S / day2-2C sequence; day 0 keeps its cash for
# the wheat opening. Labour plan and the rest of the r3 ramp unchanged.
OPENING_SHIFT = True
OPENING_SHIFT_SEQ = {1: {"SHEEP": 3}, 2: {"COW": 2}}
HERD_CAP = 14            # total herd ceiling; m2b tests pin _herd_target
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
HERD_COMPOSITION = {"SHEEP": 6, "COW": 8, "GOOSE": 0}
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
CROP_PHASE = {"MELON": (0, 17), "STRAWBERRY": (5, 14), "CARROT": (15, 26)}
CROP_FLOOR = {"MELON": 150, "STRAWBERRY": 55, "CARROT": 28}
CROP_CAP_PER_QUAD = {"MELON": 3, "STRAWBERRY": 8, "CARROT": 6}  # v6-F; V-T2
PLANT_LAST_DAY = {"WHEAT": 24, "CARROT": 26, "MELON": 17, "STRAWBERRY": 14}

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
MODE_STR_QUAD_CAP = 14     # volume: strawberry tiles per unlocked quadrant
MODE_STR_TOTAL_CAP = 42    # volume: field ceiling (Renji's 42-tile field)
MODE_WHEAT_MONEY_QUAD = 8  # volume: wheat money tiles/quad (log glut curve)
MODE_CREW_CAP_VOL = 15     # volume: hands ceiling (42 tiles of daily water)
MODE_HERD_CAP_SCALE = 18   # scale: NPV ceiling (winners' 13-17 band + 1)
_DEFENSIVE_PLAN = {"mode": "DEFENSIVE", "volume": False, "scale": False,
                   "wheat_farm": False,
                   "straw_quad_cap": CROP_CAP_PER_QUAD["STRAWBERRY"],
                   "straw_total_cap": 18,
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
# V-T7: the carrot endgame line only CLAIMS tiles from this day (tetsuya
# plants d23-27; a d15 claim squatted the SW wheat field -- seed-102
# forensics).  CROP_PHASE keeps the planting legality window.
CARROT_ENDGAME_FROM = 22
# V-T3 watertight planting (forensics: ep 104585743 d8 -- a 10-seed NE pulse
# planted h8-14 left 18 tiles unwatered and 16 died; tetsuya's 6 replays all
# plant in the daytime band and never lose the batch).  Two task-generation
# guards: (a) same-day water window -- the nearest worker must still be able
# to walk to the tile, PLANT and WATER before hour 23; (b) a daily
# new-planting cap so an opening cheque can never compress a land+seed+plant
# expansion into one afternoon.
PLANT_DAILY_CAP = 8

# 【中文】模块级会话状态（按玩家 id 分键——自对局校验时框架可能把本文件
# 一份实例同时充当两个座位）。时钟倒退 = 新对局开始，各状态字典在访问
# 函数里自动重置。_STATE 跟踪"已确认"的当日买畜步速（订单只是请求，
# 只有点数观测里畜群真的增加才消耗步速——防止被拒单浪费当日配额）。
# Module-level state keyed by player id (the framework may exec one copy of
# this file for both seats in self-play validation episodes).  Tracks the
# per-day animal purchase pace by confirming actual herd-count changes in
# the next observation; orders themselves never consume pace.
_STATE = {}

# r4-P1 sticky per-worker target registry, keyed by player id and reset at
# each day roll (hour moves backwards).  Kept for compatibility with the
# champion task contract; v9 routes use the event-driven registry below.
_TARGETS = {}

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
CROSS_SECTOR_VALUE_EDGE = 260.0
CROSS_SECTOR_PENALTY_V9 = 18.0
ROUTE_BATCH_SIZE = 6
# Tour-following: the route head gets a continuity-magnitude bonus (the
# same scale as STICKY_BONUS) so a worker sweeps its sector's queue
# instead of globally re-chasing the highest-value task after every
# completion.  The baseline comparison (2026-08-30, 24 paired cells)
# measured the previous 0.01/rank bump as efficiency-inert: ratio
# 2.214 active vs 2.194 shadow.  Red-line tasks are exempt (phase A
# stays the hard safety veto) and eligibility graphs are untouched.
V9_TOUR_BONUS = 45.0
V9_TOUR_DECAY = 15.0
_ROUTE_STATE = {}
_SCHEDULER_TRACE = {}


def scheduler_trace():
    """Return the latest per-player routing decisions for local diagnostics."""
    return copy.deepcopy(_SCHEDULER_TRACE)


def _route_state(player, day, hour, units, board):
    state = _ROUTE_STATE.get(player)
    if state is None or state.get("day") != day or hour <= state.get("hour", -1):
        state = {"day": day, "hour": hour, "home": {}, "routes": {},
                 "targets": {}, "cargo": {}, "red_signature": (),
                 "replans": 0}
        _ROUTE_STATE[player] = state
    state["hour"] = hour
    for ui, (x, y) in enumerate(units):
        state["home"].setdefault(ui, _quadrant_of(x, y, board))
        state["routes"].setdefault(ui, [])
        state["cargo"].setdefault(ui, {"phase": "idle", "item": None,
                                       "target": None})
    return state


def _sticky_state(player, day, hour):
    st = _TARGETS.get(player)
    if st is None or st.get("day") != day or hour <= st.get("hour", -1):
        st = {"day": day, "hour": hour, "assign": {}}
        _TARGETS[player] = st
    st["hour"] = hour
    return st


# 【中文】城镇日吸收量模型：从观测到的已解锁商铺集合推算每件商品每天
# 能被城镇吃掉多少单位。规则（官方引擎常量）：每家商铺每天抽 6 次货，
# 单商品商铺每次抽 2 件、多商品商铺每件 1 件；镇中心每天对每件非肥料
# 商品抽 1 件。零吸收的高级产品没有任何变现机制——只能越囤越多，卖出
# 门控会把它划入止损区而非等回涨（P2 卖出三态判据的来源）。
def _town_daily_demand(unlocked_shops):
    """Daily town absorption per item from the observed shop set (P2).

    Returns {item: units/day}; every non-fertilizer product also gets the
    town-center 1/day draw.  A zero-demand premium product (no shop, no
    center interest beyond the base 1) has NO absorption mechanism: its
    inventory can only grow while anyone produces, so the sell rule treats
    it as cut-loss territory instead of hold-for-recovery.
    """
    demand = {}
    for shop in unlocked_shops or []:
        products = SHOPS.get(shop)
        if not products:
            continue
        mult = 2 if len(products) == 1 else 1
        for item in products:
            demand[item] = demand.get(item, 0) + SHOP_DRAWS_PER_DAY * mult
    for item in BASE_PRICE:
        if item != "FERTILIZER":
            demand[item] = demand.get(item, 0) + CENTER_DRAWS_PER_DAY
    return demand


# 【中文】生产"夜晚"三件套：引擎在每日末刷新时结算产出，day 28 之后的
# 夜晚来不及变现。_prod_evening_from 判断"从今天起是否还有一个生产夜
# 晚落在变现地平线内"（买畜/停喂决策用）；_ongoing_evenings_left 精确
# 计算连续产作物还欠几个夜晚（engine 精确口径，仅供 v7-R 轮作 DIG 触
# 发用）；_crop_future_value 是排名级的剩余终局价值估计（任务价值 v 的
# 主要来源，对连续产作物故意不含 max_yield 封顶——见其英文注释）。
def _prod_evening_from(day, placed_day, first_yield, interval):
    """True when another production EVENING lands in [day, PROD_HORIZON_DAY].

    The engine produces at the end-of-day refresh of day D where
    D+1 = placed + first_yield + k*interval (k >= 0), i.e. the first
    production evening is placed + first_yield - 1; the yield is harvestable
    on D+1, so evenings after day 28 never cash out.
    """
    d0 = placed_day + first_yield - 1
    if d0 >= day:
        next_d = d0
    else:
        step = ((day - d0 + interval - 1) // interval) * interval
        next_d = d0 + step
    return next_d <= PROD_HORIZON_DAY


def _ongoing_evenings_left(crop, tile, day):
    """Engine-exact production evenings an ongoing crop still owes.

    The k-th production lands at the EOD refresh of day
    planted + first_yield - 1 + (k-1)*interval (engine checks
    next_day - planted - first_yield % interval == 0 with a
    production_count <= max_yield cap).  _crop_future_value above is a
    ranking-grade approximation with NO max_yield cap -- it keeps paying
    for finished strawberries to PROD_HORIZON_DAY, which is exactly the
    water/fertilizer waste the v7-R rotation removes; this helper is the
    precise trigger, used only there.
    """
    cd = CROPS[crop]
    planted = _get(tile, "planted_day", day)
    interval = max(1, cd["interval"])
    first_ev = planted + cd["first_yield_day"] - 1
    last_ev = first_ev + (cd["max_yield"] - 1) * interval
    if day > last_ev:
        return 0
    produced = 0
    ev = first_ev
    while ev < day:
        produced += 1
        ev += interval
    return max(0, cd["max_yield"] - produced)


def _crop_future_value(crop, tile, day):
    """Remaining terminal value of one alive PLANT tile (ranking-grade)."""
    cd = CROPS[crop]
    price = BASE_PRICE[crop]
    if cd["ongoing"]:
        # strawberry/tomato: one production evening per interval until the
        # horizon; watered+fertilized evenings pay +2 instead of +1
        d0 = _get(tile, "planted_day", day) + cd["first_yield_day"] - 1
        interval = max(1, cd["interval"])
        probe = d0
        while probe < day:
            probe += interval
        evenings = 0
        while probe <= PROD_HORIZON_DAY:
            evenings += 1
            probe += interval
        return evenings * price * 1.3
    # one-time crop: expected units at harvest * price
    yu = _get(tile, "yield_units", 0)
    age = day - _get(tile, "planted_day", day)
    ws, we = _window(crop)
    window_left = max(0, we - max(age, ws - 1))
    expect = min(cd["max_yield"], yu + 2 * window_left)
    return expect * price


# 【中文】买畜"确认步速"记账：BUY_ANIMAL 只是请求，市场可能因现金/库
# 容不足拒单；_buy_pace 只把后续观测中畜群点数的正增量记为"已确认"，防
# 止被拒的订单白白消耗当日购买配额；_note_buy_order 只登记未确认请求。
# 时钟倒退视为新对局并清零。
def _buy_pace(player, day, hour, herd_total):
    """Return confirmed animal purchases for this day.

    A BUY_ANIMAL order is only a request.  The market may reject it for lack
    of cash or shed capacity, so pace is advanced only by a positive
    herd-count delta observed on a later turn.  A backwards clock denotes a
    new episode.
    """
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour <= st.get("hour", -1):
        _STATE[player] = {"day": day, "hour": hour,
                          "last_herd": herd_total, "confirmed": 0,
                          "pending": 0}
        return 0
    delta = max(0, int(herd_total) - int(st.get("last_herd", herd_total)))
    if delta:
        st["confirmed"] = st.get("confirmed", 0) + delta
        st["pending"] = max(0, st.get("pending", 0) - delta)
    st["hour"] = hour
    st["last_herd"] = herd_total
    return st.get("confirmed", 0)


def _note_buy_order(player, day, hour, n):
    """Record an unconfirmed request without consuming the daily pace."""
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour < st.get("hour", -1):
        st = {"day": day, "hour": hour, "last_herd": 0,
              "confirmed": 0, "pending": 0}
        _STATE[player] = st
    st["hour"] = hour
    st["pending"] = st.get("pending", 0) + max(0, int(n))


def _note_buys(player, day, hour, n):
    """Compatibility shim for callers from the pre-confirmation strategy."""
    _note_buy_order(player, day, hour, n)


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


def _hire_cost(n_already_today):
    """Engine fib schedule: 1, 1, 2, 3, 5, 8, ... for the (n+1)-th hire."""
    a, b = 1, 1
    for _ in range(max(0, n_already_today)):
        a, b = b, a + b
    return a


# 【中文】市场语义镜像三件套（官方 1.32.7 引擎的逐字节复刻）：
#   _market_price_emb    按嵌入曲线表精确计算"当前库存"下的成交价；
#   _market_order_priority 订单单日优先级（终日只卖 > 买饲料 > 卖货 >
#                          d0 买畜 > 买地 > 雇工 > 买麦种 > 买畜 > 其他）；
#   plan_market_orders   对整张订单队列做官方语义的预算仿真：选前 10
#                          单、逐件按当前曲线价成交、现金/库容/雇工价
#                          全程记账，返回"会被引擎接受"的子集——入口
#                          agent() 用它做最后一道预算截断，确保提交的
#                          订单在真实引擎里逐单可成交。
def _market_price_emb(item, inventory):
    """Exact mirror of official market_price on the embedded curve table.

    Official 1.32.7 (vendored kaggriculture.py): below I0 the price uses the
    below-curve, above I0 the above-curve, floored at 1.  MARKET_PARAMS_EMB
    is pinned to the official table (99/99 spot-check in the r4-P2 notes).
    """
    base, t, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    i0 = MARKET_I0_EMB
    if inventory < i0:
        amp = bt * base / max(_shape_val(bf, t, t), 1e-9)
        return max(PRICE_FLOOR_EMB,
                   int(round(base + amp * _shape_val(bf, i0 - inventory, t))))
    amp = at * base / max(_shape_val(af, t, t), 1e-9)
    return max(PRICE_FLOOR_EMB,
               int(round(base - amp * _shape_val(af, inventory - i0, t))))


def _market_order_priority(order, day):
    """Selection priority only; accepted orders retain engine queue order."""
    if not isinstance(order, list) or not order:
        return -1
    op = order[0]
    item = order[1] if len(order) > 1 else None
    if day >= SEASON_DAYS - 1:
        return 100 if op == "SELL" else -1
    if op == "BUY_PRODUCT" and item == "WHEAT":
        return 95                 # starvation red line
    if op == "SELL":
        return 90                 # liquidity / terminal recovery
    if day == 0 and op == "BUY_ANIMAL":
        return 85                 # opening herd timing
    if op == "BUY_LAND":
        return 80
    if op == "HIRE":
        return 75
    if op == "BUY_SEED" and item == "WHEAT":
        return 70                 # feed rotation floor
    if op == "BUY_ANIMAL":
        return 60
    if op in ("BUY_SEED", "BUY_PRODUCT"):
        return 40
    return -1


def plan_market_orders(orders, money, shed_count, *, day=0, max_orders=10,
                       shed_capacity=100, hires_today=0, hands_count=0,
                       quadrants_owned=1, land_costs=None, prices=None,
                       shed_stock=None, seed_stock=None, market_inventory=None):
    """Select and budget one official-engine-compatible market queue.

    Selection is priority based, but the selected indices stay in their original
    order. Semantics mirror vendored engine 1.32.7 exactly: atomic HIRE/BUY_LAND;
    SELL/BUY_* commit ONE unit per lockstep round with the CURRENT curve price
    (BUY_PRODUCT is quoted at post-buy inventory; SELL revenue rises per unit,
    frees shed capacity and only adds supply above the $1 floor); a failed unit
    ends only its current order, and later queue columns may run.
    """
    max_orders = max(1, int(max_orders))
    ranked = []
    for index, order in enumerate(orders or []):
        priority = _market_order_priority(order, day)
        if priority >= 0:
            ranked.append((-priority, index))
    chosen = {index for _priority, index in sorted(ranked)[:max_orders]}
    selected = [order for index, order in enumerate(orders or []) if index in chosen]

    wallet = float(money)
    occupied = max(0, int(shed_count))
    hire_index = max(0, int(hires_today))
    land_index = max(0, int(quadrants_owned) - 1)
    land_costs = list(land_costs or (1000, 2000, 4000))
    prices = prices or {}
    stock_supplied = shed_stock is not None
    stock = {item: 0 for item in tuple(BASE_PRICE) + tuple(ANIMALS)}
    stock.update(shed_stock or {})
    seeds = {crop: 0 for crop in CROPS}
    seeds.update(seed_stock or {})
    inv = {item: MARKET_I0_EMB for item in BASE_PRICE}
    for item, value in (market_inventory or {}).items():
        if item in inv:
            inv[item] = int(value)
    accepted = []
    details = []
    spend = 0.0
    revenue = 0.0

    for order in selected:
        op = order[0]
        if op == "HIRE":
            cost = _hire_cost(hire_index)
            if wallet >= cost:
                wallet -= cost
                spend += cost
                hire_index += 1
                accepted.append(["HIRE"])
                details.append({"order": list(order), "filled": 1, "abort": None})
            else:
                details.append({"order": list(order), "filled": 0,
                                "abort": "no_money"})
            continue
        if op == "BUY_LAND":
            cost = land_costs[land_index] if land_index < len(land_costs) else None
            if cost is None:
                details.append({"order": list(order), "filled": 0,
                                "abort": "no_land"})
            elif wallet < cost:
                details.append({"order": list(order), "filled": 0,
                                "abort": "no_money"})
            else:
                wallet -= cost
                spend += cost
                land_index += 1
                accepted.append(["BUY_LAND"])
                details.append({"order": list(order), "filled": 1, "abort": None})
            continue
        if op == "SELL":
            if len(order) < 3 or order[1] not in BASE_PRICE or \
                    not isinstance(order[2], (int, float)) or order[2] <= 0:
                continue
            item = order[1]
            available = stock.get(item, 0) if stock_supplied else int(order[2])
            filled = 0
            abort = None
            for _ in range(int(order[2])):
                if filled >= available:
                    abort = "no_stock"
                    break
                price = _market_price_emb(item, inv[item])
                wallet += price
                revenue += price
                filled += 1
                occupied = max(0, occupied - 1)
                stock[item] = stock.get(item, available) - 1
                if price > PRICE_FLOOR_EMB:
                    inv[item] += 1   # sales above $1 add market supply
            if filled > 0:
                accepted.append(["SELL", item, filled])
            details.append({"order": list(order), "filled": filled,
                            "abort": abort})
            continue
        if op not in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL") or len(order) < 3:
            continue
        try:
            requested = int(order[2])
        except (TypeError, ValueError):
            continue
        if requested <= 0:
            continue
        item = order[1]
        if op == "BUY_SEED":
            unit_cost = CROPS.get(item, {}).get("seed")
            uses_shed = False
        elif op == "BUY_ANIMAL":
            unit_cost = ANIMALS.get(item, {}).get("cost")
            uses_shed = True
        else:
            if item not in ("WHEAT", "FERTILIZER"):
                continue
            unit_cost = None   # BUY_PRODUCT reprices every unit (official)
            uses_shed = True
        if op != "BUY_PRODUCT" and \
                (not isinstance(unit_cost, (int, float)) or unit_cost <= 0):
            continue
        filled = 0
        abort = None
        for _ in range(requested):
            if uses_shed and occupied >= shed_capacity:
                abort = "shed_full"
                break
            price = unit_cost if op != "BUY_PRODUCT" else \
                _market_price_emb(item, inv[item] - 1)  # post-buy quote
            if wallet < price:
                abort = "no_money"
                break
            wallet -= price
            spend += price
            filled += 1
            if uses_shed:
                occupied += 1
                stock[item] = stock.get(item, 0) + 1
            if op == "BUY_SEED":
                seeds[item] = seeds.get(item, 0) + 1
            if op == "BUY_PRODUCT":
                inv[item] -= 1

        if filled > 0:
            accepted.append([op, item, filled])
        details.append({"order": list(order), "filled": filled, "abort": abort})

    return {"accepted": accepted, "orders": details,
            "committed_spend": spend, "revenue": revenue,
            "remaining_money": wallet,
            "shed_count": occupied, "shed_stock": stock,
            "seed_stock": seeds,
            "hands_count": int(hands_count) + hire_index - max(0, int(hires_today)),
            "quadrants_owned": land_index + 1,
            "remaining_capacity": max(0, int(shed_capacity) - occupied),
            "market_inventory": inv,
            "truncated": len(selected) < len(orders or [])}


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


# 【中文】公开农场经济扫描：象限数、草莓/小麦格数（含草莓种植日历）、
# 按物种的在栏牲畜、雇工数、现金。obs.farms 是共享公开状态（只有仓库/
# 背包是私有的），扫描对手农场属于合法观察——这是模式门控的输入。
def _farm_scan(farm):
    """Public-farm economy scan: quadrants, strawberry/wheat tiles (with
    the strawberry planting calendar), placed herd by species, hands,
    money.  obs.farms is shared state (only sheds/inventories are
    private), so scanning the opponent's farm is legal observation."""
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    straw = wheat = herd = 0
    straw_days = []
    species = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop == "STRAWBERRY":
                    straw += 1
                    straw_days.append(_get(tile, "planted_day", 0))
                elif crop == "WHEAT":
                    wheat += 1
            elif "animal" in tile:
                herd += 1
                animal = _get(tile, "animal", "")
                if animal in species:
                    species[animal] += 1
    return {"quads": quads, "straw": straw, "wheat": wheat, "herd": herd,
            "straw_days": straw_days, "cows": species["COW"],
            "sheep": species["SHEEP"], "geese": species["GOOSE"],
            "hands": len(_get(farm, "hands", []) or []),
            "money": _get(farm, "money", 0.0)}


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
    opp_contesting = opp is not None and opp["straw"] >= 12
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
               and not opp_contesting and mine["money"] >= 800
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
                "straw_quad_cap": CROP_CAP_PER_QUAD["STRAWBERRY"],
                "straw_total_cap": 18,
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
    _PLAN_MEM[player] = {"day": day, "plan": plan}
    return plan


# 【中文】牛奶逐日持有门槛（选择性干预）：基准 105——在双方都挤奶的
# 联合奶市里囤更高的价带只会把销售推迟成终盘压力倾销（实测变现 ~60/
# 件），日清 ≥105 完胜；赛季末段门槛递减（28 日 80）——第 29 天全场
# 清算地板价在等着所有人，低但为正的门槛优于囤进联合倾销。
def _milk_gate(day):
    """Milk hold-threshold by day (selective intervention, see _market_gates).

    Base 105: in a joint-dairy market (both players milking ~20+/day vs
    town consumption of ~5/day, measured mirror prices 97-135) holding for
    higher bands just deferred sales into eventual pressure dumps (measured
    realized ~60/unit).  Clearing daily at >= 105 dominates.  Decay
    late-season: the day-29 liquidation floor is coming for everyone, so
    clearing inventory at a lower-but-positive gate beats holding into the
    joint dump.
    """
    if day >= 28:
        return 80
    if day >= 26:
        return 90
    if day >= 24:
        return 100
    return 105


# 【中文】可选 LLM 顾问钩子：默认 None（关闭）时直接返回启发式门槛。
# 仅用于本地 A/B 实验（scripts/run_llm_ab.py）；任何失败/离谱回答都回
# 退启发式，绝不阻塞回合（合规的 Reasonableness Standard 由提供方自
# 律限流）。
def _llm_sell_gate(item, price, base_gate, context):
    """Optional LLM consultation for premium sell timing; default heuristic.

    The provider (if any) must answer with {"gate": int}. Any failure or
    absurd answer falls back to the heuristic gate. Never blocks the turn:
    providers are expected to enforce their own call budget/timeout
    (Reasonableness Standard).
    """
    if LLM_PROVIDER is None:
        return base_gate
    try:
        ans = LLM_PROVIDER.suggest(
            f"Item {item} trades at {price} (base {BASE_PRICE[item]}). "
            f"Return the minimum price we should accept for selling into a "
            f"glut-crashing market, as JSON {{\"gate\": int}}.", context)
        gate = int(_get(ans or {}, "gate", base_gate))
        if 1 <= gate <= BASE_PRICE[item] * 2:
            return gate
    except Exception:
        pass
    return base_gate


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
                if "animal" in tile:
                    n_animals += 1
                continue
            if kind == "COOP":
                n_coop += 1
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
    base_pasture_want = min(HERD_CAP + 1, herd_t + 2)
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
        for pos in empty_ring + weed_ring:
            if n_coop < min(HERD_COMPOSITION["GOOSE"], herd_t) and \
                    n_coop + n_pasture < pasture_want + 1:
                builds[pos] = "COOP"
                n_coop += 1
            elif n_pasture < pasture_want:
                builds[pos] = "PASTURE"
                n_pasture += 1
            else:
                field_extra.append(pos)

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

    for crop, descending in (("MELON", True), ("CARROT", False)):
        if not _crop_open(crop):
            continue
        if crop == "CARROT" and day < CARROT_ENDGAME_FROM:
            # V-T7: carrot is the ENDGAME rotation (tetsuya plants it
            # d23-27); claiming its 6/quad from d15 let it squat the SW
            # wheat field for 11 days (seed-102 forensics: feed floor
            # squeezed to 5 wheat tiles).
            continue
        room = CROP_CAP_PER_QUAD[crop] * len(quads) - len(crop_map[crop])
        order = sorted(empties, key=lambda p: ((-_shed_dist(p)) if descending
                                               else _shed_dist(p), p[1], p[0]))
        taken = 0
        for pos in order:
            if taken >= room:
                break
            crop_map[crop].add(pos)
            taken += 1
            empties.remove(pos)

    if _crop_open("STRAWBERRY"):
        room = min(plan["straw_quad_cap"] * len(quads),
                   plan["straw_total_cap"]) - len(crop_map["STRAWBERRY"])
        for qn in (q for q in ("NE", "SW", "SE", "NW") if q in quads):
            if room <= 0:
                break
            for pos in _quad_sorted(qn):
                if room <= 0:
                    break
                crop_map["STRAWBERRY"].add(pos)
                room -= 1
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


def _count_crops(farm):
    """Alive PLANT tiles per crop (for seed deficits)."""
    counts = {crop: 0 for crop in CROPS}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop in counts:
                    counts[crop] += 1
    return counts


def _species_counts(farm, private, herd_total):
    """Placed + shed + carried animals per species.  Herd totals handed in
    by abstract callers that carry no observable composition are attributed
    to the primary species (sheep) -- real observations never need this.
    """
    counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and "animal" in tile:
                animal = _get(tile, "animal", "")
                if animal in counts:
                    counts[animal] += 1
    shed = _get(private, "shed", {}) or {}
    for animal in counts:
        counts[animal] += _get(shed, animal, 0)
        for inv in (_get(private, "inventories", []) or []):
            if inv:
                counts[animal] += _get(inv, animal, 0)
    extra = int(herd_total) - sum(counts.values())
    if extra > 0:
        counts["SHEEP"] += extra
    return counts


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
import math  # noqa: E402  (stdlib only; placed at first analytic use)

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


def _shape_val(func, x, T):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return x ** 0.5
    if func == "log":
        return math.log(1.0 + x)
    if func == "hinge":
        u = x / T if T and T > 0 else x
        return u + HINGE_GAIN_EMB * max(0.0, u - 1.0) ** 2
    return x


def _price_at_offset(item, off):
    """Engine price for inventory I0+off (off signed, glut positive)."""
    base, T, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    if off < 0:
        amp = bt * base / max(_shape_val(bf, T, T), 1e-9)
        p = base + amp * _shape_val(bf, -off, T)
    else:
        amp = at * base / max(_shape_val(af, T, T), 1e-9)
        p = base - amp * _shape_val(af, off, T)
    return max(float(PRICE_FLOOR_EMB), p)


def _offset_from_price(item, price):
    """Inverse of _price_at_offset (ranking-grade; hinge linearized)."""
    base, T, bf, bt, af, at = MARKET_PARAMS_EMB[item]
    price = float(price)
    if price >= base:
        amp = bt * base / max(_shape_val(bf, T, T), 1e-9)
        y = max(0.0, (price - base) / max(amp, 1e-9))
        if bf == "linear":
            return -y
        if bf == "sqrt":
            return -(y * y)
        if bf == "log":
            return -math.expm1(min(y, 50.0))
        if bf == "sq":
            return -(y ** 0.5)
        # hinge: u + 8*(u-1)^2 = y (u = x/T); closed form past the knee
        if y <= 1.0:
            return -(y * T)
        u = (15.0 + math.sqrt(max(0.0, 32.0 * y - 31.0))) / 16.0
        return -(u * T)
    amp = at * base / max(_shape_val(af, T, T), 1e-9)
    y = max(0.0, (base - price) / max(amp, 1e-9))
    if af == "linear":
        return y
    if af == "sqrt":
        return y * y
    if af == "log":
        return math.expm1(min(y, 50.0))
    if af == "sq":
        return y ** 0.5
    return min(y, T)


# 【中文】市场记忆与投影：_market_flow 把逐日价格移动经曲线反解成每件
# 商品的净库存流 EMA（单位/天，正值=过剩在积累——已同时包含我方与对
# 手的产销量和城镇吸收）；_project_price 给出解析的 E[R_future] =
# 在偏移量上再推 flow×horizon 天后的曲线价。两者是止损判据"投影价低
# 于现价 → 曲线在死"的来源。
# per-player market memory: yesterday's prices -> observed net flow EMA
_MARKET_MEM = {}


def _market_flow(player, day, prices):
    """EMA of the observed net inventory flow per item (units/day).

    The day-over-day price move, inverted through the engine curve, IS the
    market's net supply-minus-demand (ours + the opponent's production and
    sales, minus town consumption).  Positive flow = glut building.
    """
    st = _MARKET_MEM.get(player)
    if st is None or st.get("day", -1) >= day:
        _MARKET_MEM[player] = {"day": day, "prices": dict(prices),
                               "flow": (st or {}).get("flow", {})}
        return {}
    prev = st.get("prices", {})
    flow = {}
    for item, p_now in prices.items():
        if item not in MARKET_PARAMS_EMB or item not in prev:
            continue
        delta = (_offset_from_price(item, p_now)
                 - _offset_from_price(item, prev[item]))
        if delta == 0:
            flow[item] = 0.0
        else:
            ema = st.get("flow", {}).get(item, 0.0)
            flow[item] = 0.55 * delta + 0.45 * ema
    _MARKET_MEM[player] = {"day": day, "prices": dict(prices), "flow": flow}
    return flow


def _project_price(item, price_now, flow, horizon):
    """Analytic E[R_future]: price at I0 + off + flow*horizon."""
    off = _offset_from_price(item, price_now)
    return _price_at_offset(item, off + flow * horizon)


# 【中文】═══ 选择性干预卖出门控（市场层核心）═══
# 每回合回答"现在卖什么、卖多少"，逐商品三态规则：
#   ① 强需求（有商铺在抽货）且价在门槛下 → 囤到门槛价再卖（城镇吸收
#      会让曲线均值回归；实测毛线店开抽时羊毛整季 240+）；
#   ② 零吸收（只剩镇中心 1/天）且观测到过剩流 → 止损出清，绝不把死
#      曲线扛到第 29 天清算地板价；
#   ③ 流动性/库容压力 → 0.5-0.6×base 的小批折价 tranche。
# r4-P2 升级：①倾销限速 cap() = 城镇吸收的 2×D+4（卖穿吸收只会砸崩
# 自己的下一批）；②解析投影 _project_price 参与止损判定。
# 决策框架：SELL <=> R_now ≥ E[R_future] - C_overflow - C_liquidity
#           - C_terminal（四项分别为：溢出成本/流动性成本/终局清算折价）。
# 各商品门槛/批量与曲线形状的对应关系见下方英文注释（原始证据）。
def _market_gates(day, prices, shed, herd, town_shops=None, money=None,
                  flow=None):
    """Selective-intervention sell decisions: what to SELL this turn, with
    the hoard / release / defend rule per item made explicit.

    r4-P2 upgrades (active when town_shops is provided -- the legacy
    4-argument call keeps the r3 semantics for the pinned tests):
      * DUMP-RATE LIMIT: every tranche is capped near the town's observed
        absorption (2*D + 4) -- selling far beyond what the shops redraw
        only crashes our own next tranche (P0 slippage -10.6..-35.9/u).
      * THREE-MODE rule per item:
          demand strong (shop draws) + price at/below gate -> HOLD for the
          gate (town absorption mean-reverts the curve; measured wool 240+
          all season whenever yarn stores draw);
          zero absorption (center 1/day only) + glut flow observed ->
          CUT-LOSS at max(0.35*base, low gate) instead of riding a dead
          curve into the day-29 floor;
          liquidity/overflow pressure -> small tranches at 0.5-0.6*base
          (C_liquidity/C_overflow in the SELL <=> R_now >= E[R_future]
          - costs rule).
      * ANALYTIC PROJECTION: E[R_future] from the embedded MARKET_PARAMS
        curves and the observed net-flow EMA (_market_flow).

    Curve rationale (official MARKET_PARAMS):
      * MILK base 160, LINEAR glut (T=122): hoard below _milk_gate, clear
        through at the band, big tranche at peaks, halve inside the band,
        drain before the 100-slot discard cliff (m2b logic, kept verbatim).
      * WOOL base 200, SQ glut (T=105: ~56 units above equilibrium reach
        the $1 floor -- the fastest crasher): realize in size at real bids
        (12 at 200+, 8 at the gate, 6 at 100+), CUT LOSSES down to a small
        buffer at WOOL_CUT_LOSS once the curve is dying (measured: yarn-
        store draws decide the whole wool market), dump tranches from
        day 26 (FM-O4).
      * STRAWBERRY base 120, LINEAR glut (T=100): gate 105, tranche 8,
        bounded hoard, endgame dump (the near-band premium: their held
        medians 221-250 come from hoarding, not from dumping daily).
      * MELON base 250, SQ glut (T=300): gate 180, tranche 8 -- realize
        BEFORE the volume farmers' 100+ unit flow floors the curve (the
        m1 engine's melon branch died holding for 250; cap stays 9 tiles
        because a 12-tile plan measurably crashed our own price).
      * CARROT base 35, SQRT glut (T=450, hinge below -- town spikes it
        when scarce): gate 28, generous tranche 15.
      * EGG base 50, LOG glut (crash-tolerant like wheat): gate 40,
        tranche 10.
      * FERTILIZER base 100, linear both sides, no town consumption (m2b):
        bounded hoard, gated release, unconditional from day 25.
      * WHEAT base 25, LOG glut: sell the surplus above the feed reserve
        from WHEAT_SELL_GATE (a real bid, not the floor).
    Returns a list of ["SELL", item, qty] market orders.
    """
    orders = []
    last_day = day >= SEASON_DAYS - 1
    endgame = day >= ENDGAME_DAY
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    demand = _town_daily_demand(town_shops) if town_shops is not None else None
    flow = flow or {}

    # V-T6 bankruptcy lifeline: a broke dawn cannot re-hire the crew that
    # earns it back (crash forensics ep 104594916: 12 hands -> 0 on d10 and
    # a 17-day stall while 8 wool sat in the shed behind shut gates).  Below
    # the emergency floor every tradable shed item dumps unconditionally --
    # hoard gates must never sit on the payroll.
    if money is not None and money < 200 and not last_day:
        for item in BASE_PRICE:
            n = shed.get(item, 0)
            if isinstance(n, (int, float)) and n > 0:
                orders.append(["SELL", item, int(n)])
        return orders

    def cap(qty, item):
        """Dump-rate limiter: town absorption 2*D + 4 (P2)."""
        if demand is None:
            return qty
        return max(4, min(qty, 2 * demand.get(item, 1) + 4))

    if last_day:
        # day 29: only bank money counts; liquidate every tradable shed item
        for item in BASE_PRICE:
            n = shed.get(item, 0)
            if isinstance(n, (int, float)) and n > 0:
                orders.append(["SELL", item, n])
        return orders

    # ---- MILK: hoard / release / defend (m2b, verbatim + P2 caps) --------
    milk = shed.get("MILK", 0)
    if milk > 0:
        gate = _llm_sell_gate("MILK", prices.get("MILK", BASE_PRICE["MILK"]),
                              _milk_gate(day), {"day": day, "shed": milk,
                                                "herd": herd})
        p = prices.get("MILK", BASE_PRICE["MILK"])
        if shed_count >= 70 and p >= 30:
            sell = max(0, milk - 15)
            if sell > 0:
                orders.append(["SELL", "MILK", cap(sell, "MILK")])
        elif p >= 145:
            orders.append(["SELL", "MILK", cap(min(milk, 24), "MILK")])
        elif p >= gate:
            orders.append(["SELL", "MILK", cap(min(milk, 20), "MILK")])
        elif demand is not None and money is not None and money < 1200 \
                and p >= 0.5 * BASE_PRICE["MILK"]:
            # C_liquidity: a broke dawn cannot hire the crew that earns it
            # back -- milk clears at a soft band when cash-starved
            orders.append(["SELL", "MILK", cap(min(milk, 6), "MILK")])

    # ---- WOOL: sq glut (T=105) -- follow the curve, never ride it down ---
    # Sheep flow (ours + the opponent's, 9-12 head across the pool) exceeds
    # base town consumption in most draws: wool either stays scarce (yarn
    # stores drawn -- observed 240+ all season) or floors (+56 units above
    # equilibrium is already $5).  P2: with a yarn store absorbing, the
    # 100-149 band HOLDS for the gate; with zero absorption the analytic
    # cut-loss fires as soon as the flow says the curve is dying.
    wool = shed.get("WOOL", 0)
    if isinstance(wool, (int, float)) and wool > 0:
        p = prices.get("WOOL", BASE_PRICE["WOOL"])
        yarn = demand is None or demand.get("WOOL", 1) >= 12
        if endgame or day >= 26:
            orders.append(["SELL", "WOOL", cap(min(wool, 12), "WOOL")])
        elif shed_count >= 78 and p >= 5:
            orders.append(["SELL", "WOOL", max(0, wool - 10)])
        elif wool > WOOL_HOARD_FLOOR:
            if p >= 200:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 12), "WOOL")])
            elif p >= WOOL_GATE:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 8), "WOOL")])
            elif p >= 100 and not yarn:
                orders.append(["SELL", "WOOL",
                               cap(min(wool - WOOL_HOARD_FLOOR, 6), "WOOL")])
            elif p >= WOOL_CUT_LOSS and (day >= 18 or wool > WOOL_HOARD_CAP):
                orders.append(["SELL", "WOOL", cap(min(wool - 4, 8), "WOOL")])
            elif demand is not None and not yarn and p >= 70 \
                    and _project_price("WOOL", p, flow.get("WOOL", 0.0), 7) < p:
                # zero absorption + dying curve: realize before the sq
                # cliff does it for us
                orders.append(["SELL", "WOOL", cap(min(wool - 4, 6), "WOOL")])

    # ---- premium rotation/herd goods: gated tranches + hoard bounds ------
    def premium(item, gate, tranche, hoard_floor, hoard_cap, low_gate,
                endgame_tranche):
        held = shed.get(item, 0)
        if not isinstance(held, (int, float)) or held <= hoard_floor:
            return
        p = prices.get(item, BASE_PRICE[item])
        if endgame:
            orders.append(["SELL", item, min(held, endgame_tranche)])
        elif shed_count >= 78 and p >= 5:
            # discard-cliff guard shared with milk
            orders.append(["SELL", item, max(0, held - 10)])
        elif p >= gate + 30:
            orders.append(["SELL", item, cap(min(held - hoard_floor,
                                                 tranche * 2), item)])
        elif p >= gate:
            orders.append(["SELL", item, cap(min(held - hoard_floor,
                                                 tranche), item)])
        elif held > hoard_cap and p >= low_gate:
            orders.append(["SELL", item, cap(min(held - hoard_cap,
                                                 tranche), item)])
        elif demand is not None:
            proj3 = _project_price(item, p, flow.get(item, 0.0), 3)
            if demand.get(item, 1) <= 1 and flow.get(item, 0.0) > 0 \
                    and proj3 < 0.9 * p and p >= low_gate:
                # zero absorption + measured glut: cut before the curve
                orders.append(["SELL", item,
                               cap(min(held - hoard_floor,
                                       max(4, tranche // 2)), item)])
            elif money is not None and money < 1200 \
                    and p >= 0.55 * BASE_PRICE[item]:
                orders.append(["SELL", item, cap(min(held - hoard_floor, 6),
                                                 item)])

    # v10 M-D: tranche 8 starved the premium band -- 4 town shops absorb
    # ~24u/day and the observed top-meta band sells 30-69u/day while still
    # realizing 175-206; the P2 cap() bound (2*D+4) still applies on top.
    premium("STRAWBERRY", STRAWBERRY_GATE, 16, STRAWBERRY_HOARD_FLOOR, 26,
            70, 12)
    premium("MELON", MELON_GATE, 8, MELON_HOARD_FLOOR, 14, 120, 8)
    premium("CARROT", CARROT_GATE, 15, CARROT_HOARD_FLOOR, 30, 22, 20)
    premium("EGG", EGG_GATE, 10, EGG_HOARD_FLOOR, 16, 30, 12)

    # ---- FERTILIZER: bounded hoard, gated release (m2b) ------------------
    # (v10 M-C continuous-monetization trial REVERTED: it sold the marginal
    # fertilizer the fields convert into strawberry/wheat units, collapsing
    # the dev paired net from +84k to +11.8k.  Manure monetization must
    # come from MORE COLLECTION, not from stripping the field reserve.)
    fert = shed.get("FERTILIZER", 0)
    if fert > 0:
        if day >= 25:
            orders.append(["SELL", "FERTILIZER", fert])
        elif fert > FERT_STOCK_CAP:
            orders.append(["SELL", "FERTILIZER", max(0, fert - FERT_FIELD_RESERVE)])
        elif prices.get("FERTILIZER", BASE_PRICE["FERTILIZER"]) >= FERT_GATE:
            sell = max(0, fert - FERT_FIELD_RESERVE)
            if sell > 0:
                orders.append(["SELL", "FERTILIZER", sell])
    return orders


# 【中文】═══ 任务构建（把"本回合所有可做的事"铺成任务表）═══
# 返回 (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)。
# 任务统一结构：w 粗权重 / v 价值估计（Phase B 评分用）/ red 红线标记
# （Phase A 一票否决通道）/ need 需携带物品 / units 限定可执行工人。
# 任务来源与优先级梗概（数字=典型 w/v）：
#   末日(day29)：归还背包 DROP 120·红 + 终局收割 110；
#   生存红线：今夜枯死的浇水 98·红、断粮/过时未喂的 FEED 88-100·红、
#             满载工人回仓 PICKUP 96；
#   收获：连续产 4+/2+ 件 85/70（满格 tile 正在丢产量）、一次性成熟 80/
#             烂前抢救 95、畜产 5+/3+ 件 92/70；
#   建设与安置：建舍 46、放置栏中牲畜 82（未安置牲畜不产且占库容）；
#   种植：轮作作物 32 / 小麦 30（今种今浇的红线义务在浇水分支）；
#   维护：浇水（窗口内 42 / 连续产 40 / 保命 24）、施肥 34-36、
#             CARE 56、收粪 44；
#   杂草/轮作 DIG 22-23（仅深夜窗口，见 v7 旋钮）；
#   后勤：从仓库取小麦/牲畜/肥料的 PICKUP 94/40。
# 第 29 天走独立的"只清算"分支（无 capex、先还后卖、跳过不可行收获）。
def _build_tasks(obs, farm, private, day, plan=None):
    """Return (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)."""
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    builds, crop_map, n_animals, capacity = _field_alloc(farm, day, prices,
                                                         plan)
    seeds = _get(private, "seeds", {}) or {}
    shed = _get(private, "shed", {}) or {}
    inventories = _get(private, "inventories", []) or []
    wheat_on_units = sum(_get(inv, "WHEAT", 0) for inv in inventories if inv)
    species_on_units = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    fert_on_units = 0
    for inv in inventories:
        if not inv:
            continue
        for animal in species_on_units:
            species_on_units[animal] += _get(inv, animal, 0)
        fert_on_units += _get(inv, "FERTILIZER", 0)
    animals_to_feed = 0

    tasks = []

    def add(w, x, y, act, key, need=None, units=None, v=None, red=False):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key,
                      "need": need, "units": units,
                      "v": w if v is None else v, "red": red})

    last_day = day >= SEASON_DAYS - 1
    stop_feed = day >= ENDGAME_DAY        # FM-O4: doomsday stop-feeding
    hour = _get(obs, "hour", 0)           # v7-H: PLANT needs the EOD window
    if last_day:
        positions = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
        positions.extend(tuple(hand) for hand in (_get(farm, "hands", []) or []))
        accesses = _shed_access(board, _get(farm, "unlocked_quadrants", ["NW"]))

        for ui, (ux, uy) in enumerate(positions):
            inv = inventories[ui] if ui < len(inventories) else {}
            if sum(n for n in inv.values() if isinstance(n, (int, float)) and n > 0) <= 0:
                continue
            sx, sy = min(accesses, key=lambda pos: (_dist(ux, uy, *pos), pos[1], pos[0]))
            add(120, sx, sy, ["DROP"], ("return", ui), units={ui},
                v=60 * sum(n for n in inv.values()
                           if isinstance(n, (int, float)) and n > 0),
                red=True)
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or _get(tile, "yield_units", 0) <= 0:
                    continue
                if _get(tile, "kind", "") != "PLANT" and "animal" not in tile:
                    continue
                eligible = set()
                return_distance = min(_dist(x, y, *pos) for pos in accesses)
                for ui, (ux, uy) in enumerate(positions):
                    inv = inventories[ui] if ui < len(inventories) else {}
                    if any(n > 0 for n in inv.values() if isinstance(n, (int, float))):
                        continue
                    turns_needed = _dist(ux, uy, x, y) + 1 + return_distance + 1
                    if turns_needed <= 23 - hour:
                        eligible.add(ui)
                if eligible:
                    item = _get(tile, "crop", None)
                    price = BASE_PRICE.get(item if item in BASE_PRICE else
                                           ANIMALS.get(_get(tile, "animal", ""),
                                                       {}).get("product", ""), 0)
                    add(110, x, y, ["HARVEST"], ("harvest", x, y),
                        units=eligible, v=_get(tile, "yield_units", 0) * price)
        herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
            + sum(species_on_units.values())
        return tasks, 0, herd_total, len(crop_map["WHEAT"]), capacity

    # species still waiting in the shed (place tasks need carriers)
    placeable = {"SHEEP": _get(shed, "SHEEP", 0) + species_on_units["SHEEP"],
                 "COW": _get(shed, "COW", 0) + species_on_units["COW"],
                 "GOOSE": _get(shed, "GOOSE", 0) + species_on_units["GOOSE"]}
    # shed-occupancy harvest discount (P1 mandate: HARVEST value includes
    # the shed occupancy): harvesting into a nearly-full shed whose sell
    # gates are shut just moves the discard cliff closer -- measured
    # bankruptcy mechanism on scale_ranch BA seed 102: wool hoard filled
    # the 100-slot shed, income stopped, no wheat, 12 escapes)
    shed_count = sum(v for v in shed.values()
                     if isinstance(v, (int, float)))
    # 【中文】库容折扣：奶/产品价低于 0.75×base 且仓库 ≥70 格时，收获
    # 价值打折——向卖出门全关的满仓收货只是把 100 格丢弃悬崖提前搬近
    # （scale_ranch BA seed102 实测破产机制：毛囤满仓→收入断流→无麦
    # →12 头逃亡）；gate 打开（真实出价）则不打折。
    def _shed_factor(item_price, item_base):
        if shed_count <= 70:
            return 1.0
        # gates open at a real bid -> the goods can leave the shed again
        if item_price >= 0.75 * item_base:
            return 1.0
        return max(0.35, 1.0 - (shed_count - 70) / 50.0)

    # V-T3 guard state: workers for the per-tile water-window test, and the
    # day's confirmed new plantings (planted_day == day in the observation)
    # for the daily cap.
    plant_units = [tuple(_get(farm, "farmer",
                             [board // 2 - 1, board // 2 - 1]))]
    plant_units.extend(tuple(h) for h in (_get(farm, "hands", []) or []))
    planted_today = 0
    for _row in tiles:
        for _t in _row:
            if isinstance(_t, dict) and _get(_t, "kind", "") == "PLANT" \
                    and _get(_t, "planted_day", -1) == day:
                planted_today += 1
    plant_budget = max(0, PLANT_DAILY_CAP - planted_today)

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if pos in builds:
                    op = "BUILD_COOP" if builds[pos] == "COOP" else "BUILD_PASTURE"
                    add(46, x, y, [op], ("build", x, y), v=180)
                    continue
                crop = None
                for c, positions in crop_map.items():
                    if pos in positions:
                        crop = c
                        break
                if crop is not None and seeds.get(crop, 0) > 0 \
                        and day <= PLANT_LAST_DAY.get(crop, 24) \
                        and (not PLANT_EOD_GUARD
                             or hour <= PLANT_HOUR_MAX) \
                        and plant_budget > 0 \
                        and hour + min(_dist(ux, uy, x, y)
                                       for ux, uy in plant_units) + 2 <= 23:
                    # terminal value of planting TODAY; fresh plants must be
                    # watered the same day -- that obligation is red-flagged
                    # in the PLANT branch below via planted_day == day.
                    # v7-H: a fresh plant starts at streak 1 and dies at the
                    # evening refresh unwatered, so hour > PLANT_HOUR_MAX
                    # just burns the seed and factories a weed.
                    # V-T3: the min-distance clause is the same-day water
                    # window (walk + plant + water must fit before h23);
                    # plant_budget is the daily pulse cap.
                    cd = CROPS[crop]
                    price = _get(prices, crop, BASE_PRICE[crop])
                    ws0, we0 = _window(crop)
                    expect = min(cd["max_yield"], 2 * max(1, we0 - ws0 + 1))
                    net = expect * price - cd["seed"]
                    add(30 if crop == "WHEAT" else 32, x, y,
                        ["PLANT", crop], ("plant", x, y), v=max(30, net * 0.6))
                    plant_budget -= 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                if (pos in builds or any(pos in s for s in crop_map.values())) \
                        and hour >= WEED_DIG_HOUR_MIN:
                    # v7-W: reachable again -- _field_alloc now reserves
                    # reclaimable weeds into builds/crop_map (mode != none);
                    # v7-C2: late-day window only (see knobs above)
                    add(22, x, y, ["DIG"], ("dig", x, y), v=50)
                elif WEED_RECLAIM_MODE == "all" and \
                        hour >= WEED_DIG_HOUR_MIN and \
                        _quadrant_of(x, y, len(tiles)) in (
                            _get(farm, "unlocked_quadrants", ["NW"])
                            or ["NW"]):
                    # C3 pressure-test variant only: DIG even unplanned
                    # weeds (blocks the tile, but no downstream use yet)
                    add(18, x, y, ["DIG"], ("dig", x, y), v=40)
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "WHEAT")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                planned = pos in crop_map.get(crop, ())
                age = day - _get(tile, "planted_day", day)
                yu = _get(tile, "yield_units", 0)
                ws, we = _window(crop)
                in_window = ws <= age <= we
                futval = _crop_future_value(crop, tile, day)
                if ROTATION_DIG and cd["ongoing"] and planned \
                        and _ongoing_evenings_left(crop, tile, day) <= 0 \
                        and yu == 0 \
                        and day >= ROTATION_DIG_DAY \
                        and hour >= WEED_DIG_HOUR_MIN:
                    # v7-R: a finished, fully-harvested ongoing crop is
                    # dead weight -- stop paying water/fertilizer into it
                    # (the two task branches below are gated on futval > 0
                    # for ongoing crops) and free the tile back into the
                    # alloc (top-20 d20-28 DIG pattern).  Late-day window
                    # only: never displaces a live production task.
                    add(23, x, y, ["DIG"], ("dig", x, y), v=45)
                    continue
                if not _get(tile, "watered_today", False):
                    price = _get(prices, crop, BASE_PRICE[crop])
                    if _get(tile, "consecutive_unwatered", 0) >= 1 or \
                            _get(tile, "planted_day", day) == day:
                        # dies tonight (streak 1, or planted today: the
                        # engine starts every fresh plant at streak 1)
                        add(98, x, y, ["WATER"], ("water", x, y),
                            v=futval, red=True)
                    elif planned and cd["ongoing"] and futval > 0:
                        # ongoing crops: watering doubles fertilized output
                        # and keeps the 2-day survival streak clear.  v7-R:
                        # a finished crop (futval 0) is no longer watered.
                        add(40, x, y, ["WATER"], ("water", x, y),
                            v=max(0.3 * futval, price))
                    elif in_window and planned:
                        add(42, x, y, ["WATER"], ("water", x, y),
                            v=2 * price + 0.1 * futval)
                    elif age % 2 == 1 and futval > 0:
                        add(24, x, y, ["WATER"], ("water", x, y),
                            v=0.3 * futval)   # survival
                # FM-4 generalized: animal fertilizer feeds the rotation.
                # One-time crops at age 2 (the +2 window then lands inside
                # the 3-day fertilizer window); strawberry refreshed
                # whenever the 3-day window lapses (each production day
                # pays +2 instead of +1 while watered).  v7-R: never
                # fertilizes a finished ongoing crop.
                if planned and (not cd["ongoing"] or futval > 0) and \
                        _get(tile, "fertilized_until_day", -1) < day:
                    # v10: the engine pays fertilizer only on WATERED days
                    # inside the bonus window (window_start..max_yield_day);
                    # a 3-day fert window must therefore START at the yield
                    # window, not at age 2.  wheat/carrot windows open at
                    # age 2 (unchanged); melon's opens at 6 -- the old
                    # age-2 shot covered ages 2-4 and could never apply.
                    if cd["ongoing"] or \
                            age == (cd["max_yield_day"] + 1) // 2:
                        premium_boost = crop == "STRAWBERRY"
                        fert_dear = _get(prices, "FERTILIZER",
                                         BASE_PRICE["FERTILIZER"]) >= FERT_VALUE_GATE
                        if premium_boost or not fert_dear:
                            add(36 if cd["ongoing"] else 34, x, y, ["FERTILIZE"],
                                ("fert", x, y), need="FERTILIZER",
                                v=190 if premium_boost else 60)
                if yu > 0:
                    price = _get(prices, crop, BASE_PRICE[crop])
                    if cd["ongoing"]:
                        # v10 M-D: an ongoing tile lives exactly
                        # max_yield production events and accumulation
                        # caps at max_yield (engine _daily_refresh_plants:
                        # min(max_yield, yu + bonus)) -- every event that
                        # lands on a full tile is +2 gone forever.  Collect
                        # at 2+, escalating capped tiles above the one-shot
                        # mature band (a capped strawberry tile is losing
                        # production right now).
                        if yu >= 4:
                            add(85, x, y, ["HARVEST"], ("harvest", x, y),
                                v=yu * price
                                * _shed_factor(price, BASE_PRICE[crop]))
                        elif yu >= 2:
                            add(70, x, y, ["HARVEST"], ("harvest", x, y),
                                v=yu * price
                                * _shed_factor(price, BASE_PRICE[crop]))
                    elif age >= cd["max_yield_day"] + 1 or last_day:
                        # rot emergency: one-time crops decay to a weed from
                        # hour 0 of this day, ~1 unit per 2 turns
                        # V-T5: escalated to RED -- a rotting crop is as
                        # time-critical as a thirsty one (the v10.5 crash
                        # class: harvest starved behind red water commutes)
                        add(95, x, y, ["HARVEST"], ("harvest", x, y),
                            v=yu * price + 40, red=True)
                    elif age >= cd["max_yield_day"] and (
                            _get(tile, "watered_today", False) or
                            _get(obs, "hour", 0) >= 18):
                        add(80, x, y, ["HARVEST"], ("harvest", x, y),
                            v=yu * price + 30)
            elif "animal" in tile:
                animal = _get(tile, "animal", "COW")
                spec = ANIMALS.get(animal) or ANIMALS["COW"]
                product = spec["product"]
                price = _get(prices, product, BASE_PRICE[product])
                placed = _get(tile, "placed_day", day)
                prod_remains = _prod_evening_from(day, placed,
                                                  spec["first_yield_day"],
                                                  spec["interval"])
                # r4-P4lite: an animal with no production evening left,
                # no held yield and no escape exposure worth preventing
                # (day 26+: an escape now cannot cost a future harvest)
                # repays nothing for its wheat -- stop feeding it
                terminal_idle = (day >= 26 and not prod_remains
                                 and _get(tile, "yield_units", 0) <= 0)
                if not stop_feed and not terminal_idle:
                    if not _get(tile, "fed_today", False):
                        animals_to_feed += 1
                        streak = _get(tile, "consecutive_unfed", 0) >= 1
                        # escape risk outranks everything: escalate by
                        # streak/hour (r3 escalation hour kept)
                        if streak or _get(obs, "hour", 0) >= FEED_RED_HOUR:
                            w = 100
                            v = spec["cost"] + 2.5 * price   # asset at stake
                            red = True
                        else:
                            w = 88
                            # feed cashes tonight's production bonus (base 1
                            # lands regardless; fed consumes the care bonus)
                            # and keeps every CARE option alive (P0: 0-escape
                            # red line) -- above every water, below harvest
                            v = price + 300
                            red = False
                        add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT",
                            v=v, red=red)
                    if day <= SEASON_DAYS - 3 and not _get(tile, "cared_today", False) \
                            and _get(tile, "fed_today", False):
                        # CARE only pays when another production evening
                        # remains to consume the bonus (else value 0: skip)
                        if prod_remains:
                            add(56, x, y, ["CARE"], ("care", x, y),
                                v=price + 100)
                yu = _get(tile, "yield_units", 0)
                if yu >= 5:
                    add(92, x, y, ["HARVEST"], ("harvest", x, y),
                        v=(yu * price + price)
                        * _shed_factor(price, BASE_PRICE[product]))
                elif yu >= 3 or (yu > 0 and (last_day or stop_feed)):
                    add(70, x, y, ["HARVEST"], ("harvest", x, y),
                        v=(yu * price + (price if prod_remains else 0))
                        * _shed_factor(price, BASE_PRICE[product]))
                if _get(tile, "fertilizer_available", False):
                    add(44, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y),
                        v=85)
            elif kind in ("PASTURE", "COOP") and "animal" not in tile:
                animal = None
                if kind == "COOP" and placeable["GOOSE"] > 0:
                    animal = "GOOSE"
                elif kind == "PASTURE":
                    for candidate in ("SHEEP", "COW"):
                        if placeable[candidate] > 0:
                            animal = candidate
                            break
                if animal is not None and _get(obs, "hour", 0) <= 18:
                    # urgent: an unplaced animal produces nothing and squats
                    # in the shed (a 100-slot shared resource)
                    placeable[animal] -= 1
                    add(82, x, y, ["PLACE", animal], ("place", x, y),
                        need=animal, v=ANIMALS[animal]["cost"] + 120)

    board_half = board // 2
    shed_tile = (board_half - 1, board_half - 1)
    shed_available = {item: max(0, int(n)) for item, n in shed.items()}
    # ---- feed logistics: distribute the wheat across several carriers ----
    # (one carrier cannot FEED a 10-animal ring within 24 turns; chunks of 5
    # are grabbed by different units because a loaded carrier is barred
    # from picking up another chunk -- see executable() below.  Chunks are
    # raised whenever carried wheat falls short of the mouths, so multiple
    # carriers restock throughout the day.)
    if animals_to_feed > 0 and shed_available.get("WHEAT", 0) > 0:
        shortfall = animals_to_feed + 2 - wheat_on_units
        i = 0
        while shortfall > 0 and i < 4 and shed_available.get("WHEAT", 0) > 0:
            n = min(5, shortfall, shed_available["WHEAT"])
            if n <= 0:
                break
            add(96 - 8 * i, shed_tile[0], shed_tile[1], ["PICKUP", "WHEAT", n],
                ("pickup_w", i), v=300 - 20 * i,
                red=(i == 0 and _get(obs, "hour", 0) >= FEED_RED_HOUR))
            shortfall -= n
            shed_available["WHEAT"] -= n
            i += 1
    # ---- animal logistics: carry bought animals onto empty structures ----
    for animal in ("SHEEP", "COW", "GOOSE"):
        if shed_available.get(animal, 0) > 0 and species_on_units[animal] < 2 \
                and any(t["key"][0] == "place" and t["act"][1] == animal
                        for t in tasks):
            n = min(2, shed_available[animal])
            add(94, shed_tile[0], shed_tile[1], ["PICKUP", animal, n],
                ("pickup_a", animal), v=340)
            shed_available[animal] -= n
    # ---- fertilizer logistics for the rotation's fertilize tasks --------
    if any(t["key"][0] == "fert" for t in tasks) and \
            shed_available.get("FERTILIZER", 0) > 0 and fert_on_units < 3:
        n = min(4, shed_available["FERTILIZER"])
        add(40, shed_tile[0], shed_tile[1], ["PICKUP", "FERTILIZER", n],
            ("pickup_f", 0), v=220)
        shed_available["FERTILIZER"] -= n
    herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
        + sum(species_on_units.values())
    return tasks, animals_to_feed, herd_total, len(crop_map["WHEAT"]), capacity


# 【中文】═══ 市场订单编排（本回合买什么、卖什么）═══
# 下单顺序即优先级链：① 买地（NE d4+/SW d7+，保护基金互锁畜群；SW
# 过 d18 不再买——草莓窗已关、旧栏已满，2000 只会买成流动性）；VOLUME
# 的 SE(d10-14)；② 饲料安全垫（系统麦 < 待喂+3 就外购，护栏价 36、
# 饥饿止损价 85；affordability 门控防"钱=8 仍连发 24 回合废单"）；
# ③ 种子（小麦底仓优先；v9.2 维护门：麦价 ≥30 时在 d8-14 衰减窗内
# 补种；草莓不排在买地基金后面——d5 种下 d15 起每件 ~200 回报）；
# ④ 畜群（d0 爆发 2C+2S；此后"资金门 + 确认步速 + 物种死价冻结 +
# NPV 吸收上限"四重门，按相对缺口交错物种让牛赶上 d8 高价奶窗）；
# ⑤ 卖单（_market_gates 三态门控 + 小麦余量在真实出价 ≥26 时出清，
# 现金 <1000 的现金流回退允许 ≥20 就卖——门槛绝不能饿死资本计划）。
# v10 M-E 贯穿全程：committed_spend 同回合花费台账，让后面的门读到
# "引擎视角"的钱包（防一回合地+畜+种三连掏空）。
def _market_orders(obs, farm, private, day, animals_to_feed, herd_total,
                   plan=None):
    money = _get(farm, "money", 0.0)
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    last_day = day >= SEASON_DAYS - 1
    town_shops = _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    if plan is None:
        plan = _DEFENSIVE_PLAN
    builds, crop_map, _placed, capacity = _field_alloc(farm, day, prices,
                                                       plan)

    orders = []
    # WHEAT_FARM keeps a conservative projected wallet while building the
    # same-turn queue.  The engine commits market orders sequentially, so
    # sizing later seeds/animals from the opening wallet can cross the hold
    # reserve after an earlier feed or land purchase succeeds.
    projected_money = money

    # ---- land plan (FM-O2): NE day 4+, SW day 7+; the fund is protected --
    # (working capital -- seeds/feed -- is never blocked: it pays for the
    # land; herd buys wait for the fund while it is pending).  The purchase
    # itself stays eligible every day after the due day -- the block on the
    # herd simply lapses so a slow season cannot deadlock the ranch.
    land_fund = 0
    land_pending = False
    # v10 M-E: same-turn spend ledger.  Every BUY_* order appended below
    # deducts here so later gates (feed, animals) price the wallet as the
    # engine will see it after this turn's queue, not the raw dawn money
    # (ep 103783585: land + 3 sheep + seeds in one turn drained 3256 to
    # 16 because the animal gate read the pre-land wallet).
    committed_spend = 0.0
    if quads in LAND_PLAN:
        due_day, fund = LAND_PLAN[quads]
        # r4-P3: SW after day 18 cannot deploy a repaying asset (strawberry
        # phase over, pasture ring of NW+NE already holds 17 head) -- the
        # 2000 buys liquidity instead
        if quads == 2 and day > LAND_LATE_CUTOFF:
            land_fund = 0
        elif day >= due_day:
            land_fund = fund
            if money >= fund:
                orders.append(["BUY_LAND"])
                committed_spend += LAND_PRICE[quads]
                if plan.get("wheat_farm"):
                    projected_money -= LAND_PRICE[quads]
            elif day < due_day + LAND_PEND_WINDOW:
                land_pending = True

    # r5-P4 volume quadrant: while the strawberry window is open, SE
    # (4000) becomes a buyable asset -- 25 more tiles at the 42-tile
    # strawberry field's realized band repay it several times over
    # (round-3 ledger: Renji's 42-tile field).  No herd-blocking fund:
    # the 14-head plan is already built by the day this can fire.
    if plan["volume"] and quads == 3 \
            and SE_DUE_DAY <= day <= SE_BUY_LAST_DAY and money >= SE_FUND:
        orders.append(["BUY_LAND"])
        committed_spend += LAND_PRICE[3]

    # ---- feed security (FM-O3 + m2b phantom guard): never let the herd
    # run short of wheat, counting what carriers already hold (a shed-only
    # check sees the morning pickup as a shortfall and re-buys what we just
    # sold -- measured -8k/season).  Guardrail: normal-state buys stop at
    # FEED_BUY_MAX_PRICE (profile avg 26-32); starvation cap 85 kept (dear
    # wheat is still cheaper than a lost animal).
    wheat_carried = sum(_get(inv, "WHEAT", 0)
                        for inv in (_get(private, "inventories", []) or []) if inv)
    sys_wheat = shed.get("WHEAT", 0) + wheat_carried
    if animals_to_feed > 0 and not last_day \
            and sys_wheat < animals_to_feed + 3:
        cap = 85 if sys_wheat < animals_to_feed else \
            plan.get("feed_max_price", FEED_BUY_MAX_PRICE)
        if prices.get("WHEAT", 25) <= cap:
            # r5-P4 volume: the 42-tile field leaves little room for feed
            # wheat, so the daily guardrailed buy widens (Renji bought
            # 1501u/season; profiles 414-2732u)
            want = min((24 if plan["volume"] or plan.get("wheat_farm") else 16),
                       animals_to_feed + 8 - sys_wheat)
            wheat_px = prices.get("WHEAT", 25)
            if plan.get("wheat_farm"):
                unit_budget = max(1, cap + 1)
                affordable = max(
                    0, int((projected_money - WHEAT_FARM_HOLD_CASH) //
                           unit_budget))
                want = min(want, affordable)
            else:
                # v10 M-E: affordability gate -- ep 103783585 re-issued
                # BUY_PRODUCT WHEAT 10 for 24 straight turns at money=8
                # (all rejected); the herd still starved two days later
                want = min(want, max(
                    0, int((money - committed_spend - 60) // wheat_px)))
            if want > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", want])
                committed_spend += want * wheat_px
                if plan.get("wheat_farm"):
                    projected_money -= want * unit_budget

    # ---- seeds: the wheat feed floor first (m2b), then rotation crops
    # staged behind the pending land fund (FM-3 staging).  R3-3 exception:
    # strawberry is NOT staged behind the land fund once its phase opens --
    # the winners plant 6+ tiles on d5-11 while the NE/SW purchases proceed
    # on their own fund-gated schedule (planting d5 pays from d15 at
    # ~200/u; the one-day land delay it can cost repays many times over).
    # v9-W1 (round-5 online forensics 2026-08-30): the legacy
    # seeds<6->buy-12 cadence let the feed floor decay to zero by d20 in
    # every round-5 game; the spiral only detonated in DEAR-wheat seasons
    # (JIlong Zhou game: wheat 37-41 all season, field dead, 1067u external
    # feed at ~39.5/u = 42.2k spend, d12 cash 4).  An ungated buy-to-cap
    # measured -837.8k / disaster 0.0455 / baseline_wheat 0.625 on the dev
    # gate (2026-08-31 v9_w1_port_dev): in cheap seasons the 18-tile
    # refill burns the thin d4-12 wallet and ~27 extra ops/day crowd the
    # strawberry/melon labour line.  So the refill is gated to the failure
    # condition and maintains the feed floor.
    # v9.2 (round-6 forensics 2026-08-31): wheat ramps 25 -> 50+ in EVERY
    # game while the field decays in the d8-14 window at prices 29-34 --
    # the >= 35 gate only opened at d14-16 with the field already dead and
    # the wallet at 28-2000 (wallet-scaled batches bought ~0 seeds).  The
    # maintenance gate moves down to 30 so the refill acts inside the
    # decay window, while the genuinely cheap bands (< 30) keep the v7.2
    # legacy cadence byte-identical (round-6 win 103422278 sat at wheat
    # 22-24 on d8-12 and won without any refill).
    alive = _count_crops(farm)
    wheat_price_now = _get(prices, "WHEAT", 25)
    if not plan.get("wheat_farm") and day <= SEASON_DAYS - 7 \
            and wheat_price_now >= 30:
        wheat_cap_now = _wheat_cap(day, wheat_price_now)
        want_w = wheat_cap_now - alive.get("WHEAT", 0) - seeds.get("WHEAT", 0)
        floor_w = 12 if seeds.get("WHEAT", 0) < 6 else 0
        batch_w = min(24, max(floor_w, want_w))
        if day <= 2:
            batch_w = min(batch_w, 12)   # the d0 budget belongs to the herd
        # working-capital class (like feed): scale to the wallet instead of
        # rejecting the whole order -- round-5 forensics showed d8-12
        # wallets of 4-629 cash starving a 10-coin seed under a flat 150
        # gate.
        batch_w = min(batch_w, max(0, int((money - 20) // 10)))
        if batch_w > 0:
            orders.append(["BUY_SEED", "WHEAT", batch_w])
            committed_spend += batch_w * CROPS["WHEAT"]["seed"]
    elif not plan.get("wheat_farm") and seeds.get("WHEAT", 0) < 6 \
            and day <= SEASON_DAYS - 7 and money >= 150:
        orders.append(["BUY_SEED", "WHEAT", 12])
        committed_spend += 12 * CROPS["WHEAT"]["seed"]
    if plan.get("wheat_farm") and not last_day \
            and day <= PLANT_LAST_DAY["WHEAT"]:
        alive_wheat = alive.get("WHEAT", 0)
        target_wheat = min(plan.get("wheat_total_cap", WHEAT_FARM_WHEAT_CAP),
                           WHEAT_FARM_WHEAT_CAP)
        wanted_wheat = max(0, target_wheat - alive_wheat -
                           seeds.get("WHEAT", 0))
        if wanted_wheat > 0 and \
                projected_money >= WHEAT_FARM_CASH_REDLINE + 10:
            batch = min(
                24, wanted_wheat,
                max(0, int((projected_money - WHEAT_FARM_CASH_REDLINE) //
                           CROPS["WHEAT"]["seed"])))
            if batch > 0:
                orders.append(["BUY_SEED", "WHEAT", batch])
                projected_money -= batch * CROPS["WHEAT"]["seed"]
    if not last_day:
        crop_seed_sequence = ("STRAWBERRY",) if plan.get("wheat_farm") else \
            ("STRAWBERRY", "MELON", "CARROT")
        # V-T3: premium seed ORDERS stay inside the daily planting budget,
        # derived from the OBSERVATION (tiles planted today) so the gate is
        # idempotent -- the deterministic-agent contract forbids cross-call
        # ledgers (d8 pulse: the first milk cheque bought 10 strawberry
        # seeds at once and the afternoon could not water them).
        planted_today_orders = 0
        for _row in (_get(farm, "tiles", []) or []):
            for _t in _row:
                if isinstance(_t, dict) and _get(_t, "kind", "") == "PLANT" \
                        and _get(_t, "planted_day", -1) == day:
                    planted_today_orders += 1
        room_budget = max(0, PLANT_DAILY_CAP - planted_today_orders)
        for crop in crop_seed_sequence:
            lo, hi = CROP_PHASE[crop]
            if not (lo <= day <= hi):
                continue
            if prices.get(crop, BASE_PRICE[crop]) < CROP_FLOOR[crop]:
                continue  # red line: dead-price freeze
            cap_for_crop = CROP_CAP_PER_QUAD[crop] * quads
            if crop == "STRAWBERRY":
                cap_for_crop = min(plan["straw_quad_cap"] * quads,
                                   plan["straw_total_cap"])
            want = cap_for_crop - alive[crop] - seeds.get(crop, 0)
            batch = min(6, max(0, want), room_budget)
            seed_gate = 250 if crop == "STRAWBERRY" else land_fund + 250
            wallet = projected_money if plan.get("wheat_farm") else money
            reserve_gate = max(seed_gate, WHEAT_FARM_HOLD_CASH) \
                if plan.get("wheat_farm") else seed_gate
            if plan.get("wheat_farm") or \
                    (crop == "STRAWBERRY" and plan["volume"]):
                # Opt-in wheat mode and VOLUME use wallet-scaled batches;
                # WHEAT_FARM also preserves its hold reserve after every
                # earlier same-turn purchase.
                batch = min(10 if plan["volume"] else 6, max(0, want),
                            room_budget,
                            max(0, int((wallet - reserve_gate) //
                                       CROPS[crop]["seed"])))
            if batch > 0 and wallet >= reserve_gate + \
                    CROPS[crop]["seed"] * batch:
                orders.append(["BUY_SEED", crop, batch])
                committed_spend += CROPS[crop]["seed"] * batch
                if plan.get("wheat_farm"):
                    projected_money -= CROPS[crop]["seed"] * batch

    # ---- herd (FM-O2 + R3-1/R3-2): mixed 14-head ranch, money-gated,
    # paced by CONFIRMED purchases (m2b), species-level dead-price freeze
    # (red line).  Day 0 is the r3 opening: the burst buys OPENING_HERD
    # outright (2C+2S = 1800 of the 3000 start; 116/116 top-20 seats and
    # 3/3 round-2 winners put 4-5 head on d0 -- the m3 1-sheep opening is
    # the fork the round-2 losses traced to), both species in one turn so
    # cows reach the day-8 milk window AND sheep the day-6 wool window.
    reserve = 800 if day <= 3 else (550 if day <= 7 else COW_BUY_RESERVE)
    if land_pending:
        reserve += land_fund
    pace = _animal_pace(day)
    target = _herd_target(day, 99)   # FM-O3: external feed releases autarky
    if plan.get("wheat_farm"):
        target = min(WHEAT_FARM_HERD_FLOOR, target)
    # r4-P3: state-driven ceiling above the plan when the marginal NPV,
    # market absorption and feed line all clear (cap 17 safety boundary)
    wheat_carried_early = sum(_get(inv, "WHEAT", 0)
                              for inv in (_get(private, "inventories", [])
                                          or []) if inv)
    sys_wheat_early = shed.get("WHEAT", 0) + wheat_carried_early
    absolute_ceiling = MODE_HERD_CAP_SCALE if plan.get("scale") \
        else HERD_CAP_NPV
    herd_ceiling = min(plan.get("herd_ceiling", absolute_ceiling),
                       absolute_ceiling)
    npv_ceiling = min(HERD_CAP, herd_ceiling)
    preferred_species = None
    if herd_total >= HERD_CAP and not plan.get("wheat_farm"):
        # r4-P3: the NPV ceiling EXTENDS the completed 14-head plan (never
        # accelerates it -- the day-0 burst and the r3 deadline stand)
        decision_ceiling, preferred_species = _npv_herd_decision(
            day, prices, herd_total,
            _species_counts(farm, private, herd_total),
            _town_daily_demand(town_shops), sys_wheat_early, plan=plan)
        npv_ceiling = min(herd_ceiling, decision_ceiling)
        target = max(target, npv_ceiling)
    bought = _buy_pace(_get(obs, "player", 0), day, _get(obs, "hour", 0),
                       herd_total)
    opening_bought = False
    _open_seq = OPENING_SHIFT_SEQ if OPENING_SHIFT else {0: OPENING_HERD}
    if not last_day and day in _open_seq:
        _species_pre = _species_counts(farm, private, herd_total)
        spend = 0
        for animal in ("COW", "SHEEP"):
            want = max(0, _open_seq[day].get(animal, 0) - 0)
            if OPENING_SHIFT:
                want = max(0, _open_seq[day].get(animal, 0)
                           - _species_pre.get(animal, 0))
            cost = ANIMALS[animal]["cost"]
            n = min(want, int((money - spend - OPENING_RESERVE) // cost)) \
                if money - spend > OPENING_RESERVE else 0
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
                spend += n * cost
                opening_bought = True
    # V-T1: under the opening shift the paced loop also stands down on
    # day 0 -- the whole day belongs to the wheat opening, no animals.
    _opening_shift_hold = OPENING_SHIFT and day == 0
    if not opening_bought and not _opening_shift_hold and not last_day \
            and herd_total < target \
            and shed_count < 88 and bought < pace:
        species = _species_counts(farm, private, herd_total)
        # interleave species by relative deficit so cows reach their day-8+
        # premium-milk window on time instead of queueing behind the sheep
        candidates = sorted((a for a in HERD_COMPOSITION if HERD_COMPOSITION[a] > 0),
                            key=lambda a: species[a] / float(HERD_COMPOSITION[a]))
        if npv_ceiling > HERD_CAP and preferred_species is not None:
            candidates = [preferred_species]
        for animal in candidates:
            comp_cap = HERD_COMPOSITION[animal]
            if npv_ceiling > HERD_CAP:
                # P3 NPV branch: extend the selected species from its current
                # count, including composition-skewed states.
                comp_cap = species[animal] + npv_ceiling - herd_total
            if species[animal] >= comp_cap:
                continue
            if day > ANIMAL_BUY_LAST_DAY[animal]:
                continue
            product = ANIMALS[animal]["product"]
            if day >= DEAD_PRICE_FROM_DAY:
                # r4-P2 shop-conditional scale-up: with a shop absorbing the
                # product the m2b 90-floor stands; with ZERO absorption (no
                # shop, center 1/day) the herd only scales at full base
                # price -- never into a market that cannot eat the flow
                demand = _town_daily_demand(town_shops)
                floor = DEAD_PRICE_FLOOR[product] \
                    if demand.get(product, 1) >= 2 \
                    else int(0.95 * BASE_PRICE[product])
                if prices.get(product, BASE_PRICE[product]) < floor:
                    continue  # dead-price freeze (demand-conditioned)
            cost = ANIMALS[animal]["cost"]
            # v10 M-E: price the wallet as the engine will see it after
            # this turn's earlier buys, and keep a post-purchase floor so
            # the dawn hire gate never loses the crew
            wallet = (projected_money if plan.get("wheat_farm")
                      else money) - (0.0 if plan.get("wheat_farm")
                                     else committed_spend)
            reserve_total = reserve + LIQUIDITY_FLOOR
            if wallet < cost + reserve_total:
                continue
            n = min(pace - bought, target - herd_total,
                    comp_cap - species[animal],
                    int((wallet - reserve_total) // cost))
            if npv_ceiling > HERD_CAP:
                demand = _town_daily_demand(town_shops)
                absorption_cap = int(
                    demand.get(product, 1) * ANIMALS[animal]["interval"] // 2)
                n = min(n, absorption_cap - species[animal])
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                if plan.get("wheat_farm"):
                    projected_money -= n * cost
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
            break   # one species per turn

    # ---- selling: selective-intervention gates (P2: town-conditioned) ----
    flow = _market_flow(_get(obs, "player", 0), day, prices)
    orders.extend(_market_gates(day, prices, shed, herd_total,
                                town_shops=town_shops, money=money,
                                flow=flow))
    if last_day:
        # Goods already carried can DROP before market processing in this turn,
        # so include them in liquidation. Failed/partial quantities remain legal
        # positive orders and simply commit up to actual shed availability.
        carried = {}
        for inv in (_get(private, "inventories", []) or []):
            for item, n in (inv or {}).items():
                if isinstance(n, (int, float)) and n > 0:
                    carried[item] = carried.get(item, 0) + n
        indexed = {order[1]: order for order in orders if order[0] == "SELL"}
        for item, n in carried.items():
            if item not in BASE_PRICE:
                continue
            if item in indexed:
                indexed[item][2] += n
            else:
                order = ["SELL", item, n]
                orders.append(order)
                indexed[item] = order
    # wheat: log glut curve; sell the surplus above the feed reserve at a
    # real bid (WHEAT_SELL_GATE), under the m2b pressure/late fallbacks
    if not last_day:
        reserve_w = animals_to_feed + WHEAT_FEED_RESERVE
        surplus = shed.get("WHEAT", 0) - reserve_w
        wheat_px = prices.get("WHEAT", 25)
        if surplus > 0 and (wheat_px >= WHEAT_SELL_GATE
                            or shed_count >= 70 or day >= 26
                            or (money < 1000 and wheat_px >= 20)):
            # money < 1000: cash-flow fallback -- the gate must never starve
            # the land/animal capex plan (measured: 42 wheat hoarded at $516
            # while the NE purchase window lapsed)
            orders.append(["SELL", "WHEAT", surplus])
    return orders


# 【中文】═══ r4-P1 状态价值调度器（冠军执行器）═══
# 两阶段分派（替代 r3 的 w/(1+dist) 贪心——实测它让远端红线格饿死：
# 每局 14-29 个 CARE 失误杂草全聚在距仓曼哈顿 6-9 格处，请求过的操作
# 全部成功、只是没人去远处）：
#   Phase A 红线一票否决：所有 red 任务按价值降序，逐个由"最近工人"
#     覆盖（缺载货的工人按"先绕仓库再过去"的距离计价+6）；不看权重、
#     每任务只认领一次；
#   Phase B 价值匹配：Score_ij = V_i - TRAVEL_MU×d - 跨象限惩罚
#     + 载货亲和（持有 need 物品的工人 +0.5V，缺货的 -0.5V）
#     + 粘滞奖励（延续上回合目标，抑制震荡），全局排序贪心认领。
# 执行段：走到目标格→执行；缺 need 物品先绕仓库取货（r4-P1 修复
# "空手走range喂料崩溃"）；没任务的工人做脚下免费操作否则 PASS；
# 末尾 R6 护栏：PLANT 数量永远 ≤ 手持种子数。
def _schedule_units_v72(obs, farm, private, day, tasks):
    """r4-P1 state-value scheduler.

    Two phases, replacing the r3 per-unit w/(1+dist) greedy that measurably
    starved distant red-line tiles (29 care-lapse weeds + escapes per game
    while every REQUESTED op succeeded):

      Phase A (red-line, one-vote veto, no weighting): death-tonight
      obligations -- FEED with streak >= 1 (or past FEED_RED_HOUR), WATER
      with streak >= 1 or planted today, last-day DROP returns -- are
      covered FIRST by a nearest-worker greedy in value order.  A
      wheatless worker assigned a red FEED still walks to the shed first
      (fetch detour priced into the distance below).

      Phase B (value matching): Score_ij = V_i - TRAVEL_MU*d_ij
      - CROSS_QUAD_PENALTY (zone stickiness) + item-carrier affinity
      + STICKY_BONUS for yesterday's-turn target (kills oscillation).
      Global greedy over (worker, task) pairs; each task claimed once so
      workers never pile onto one target.
    """
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    inventories = _get(private, "inventories", []) or []
    hour = _get(obs, "hour", 0)
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]
    sticky = _sticky_state(_get(obs, "player", 0), day, hour)["assign"]

    def unit_inv(i):
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    actions = []

    def executable(task, ui):
        eligible = task.get("units")
        if eligible is not None and ui not in eligible:
            return False
        need = task.get("need")
        if need and _get(unit_inv(ui), need, 0) <= 0:
            return False
        x, y = task["x"], task["y"]
        tile = tiles[y][x]
        kind = _get(tile, "kind", "") if isinstance(tile, dict) else None
        op = task["act"][0]
        if op in ("WATER", "FERTILIZE"):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            # engine DIG clears any non-animal tile; v7-R rotation-DIG
            # targets finished PLANTs (weeds remain the other target)
            return kind == "WEED" or kind == "PLANT"
        if op in ("BUILD_PASTURE", "BUILD_COOP"):
            return tile is None
        if op == "PLACE":
            structure = ANIMALS.get(task["act"][1], {}).get("structure")
            return isinstance(tile, dict) and _get(tile, "kind", "") == structure \
                and "animal" not in tile
        if op == "PICKUP":
            if not _shed_adjacent(units[ui][0], units[ui][1], board, quads):
                return False
            # a carrier holding a full chunk moves out to feed instead of
            # chain-grabbing every chunk at the shed (multi-carrier FEED)
            if task["act"][1:2] == ["WHEAT"] and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                return False
            return True
        if op == "DROP":
            return _shed_adjacent(units[ui][0], units[ui][1], board, quads) and any(
                n > 0 for n in unit_inv(ui).values()
                if isinstance(n, (int, float)))
        return True

    def tval(t):
        return t.get("v", t["w"])

    # ---------------- phase A: red-line nearest-match first ----------------
    claimed = set()
    assign = {}
    accesses = _shed_access(board, quads)
    reds = [t for t in tasks if t.get("red")]
    reds.sort(key=lambda t: -tval(t))
    by_key = {t["key"]: t for t in reds}
    # V-T4 red-line stickiness, V-T5 near-end hold: re-bind the previous
    # turn's red assignments first, but a held binding survives only while
    # the target is NEAR (d <= 4).  Forensics pair: ep 104585743 d8 h16-23
    # (no stickiness: nine workers oscillated between 18 red tiles for
    # eight hours, zero waterings) vs ep 104594916 d8-d11 (unconditional
    # stickiness: distant red bindings locked workers into long commutes,
    # the harvest starved, cash broke and all hands reset to zero).  The
    # distance cap keeps the anti-oscillation benefit without the commute
    # lock-in; far red targets still go to the nearest free worker each
    # turn.
    for ui, prev_key in list(sticky.items()):
        if ui in assign or ui >= len(units):
            continue
        t = by_key.get(prev_key)
        if t is None:
            continue
        if t.get("units") is not None and ui not in t["units"]:
            continue
        if _dist(units[ui][0], units[ui][1], t["x"], t["y"]) > 4:
            continue
        assign[ui] = t
        claimed.add(t["key"])
    for t in reds:
        if t["key"] in claimed:
            continue
        best = None
        for ui in range(len(units)):
            if ui in assign or (t.get("units") is not None
                                and ui not in t["units"]):
                continue
            ux, uy = units[ui]
            d = _dist(ux, uy, t["x"], t["y"])
            # a worker missing the carried item pays the shed detour it is
            # about to walk (route below); carriers keep their raw distance
            # so loaded units win red consumer tasks outright
            need = t.get("need")
            if need and _get(unit_inv(ui), need, 0) <= 0:
                via = min(_dist(ux, uy, ax, ay) + _dist(ax, ay, t["x"], t["y"])
                          for ax, ay in accesses)
                d = min(d, via) + 6
            if best is None or d < best[0]:
                best = (d, ui)
        if best is not None:
            assign[best[1]] = t
            claimed.add(t["key"])

    # ---------------- phase B: value matching with stickiness -------------
    # V-T5: home-sector soft penalty (tetsuya-style patrol continuity).  The
    # worker's first position of the day defines its home quadrant; work in
    # the OTHER quadrants pays the soft penalty on top of the distance
    # buckets below.  Red lines stay exempt (phase A above).
    home_quads = _route_state(_get(obs, "player", 0), day, hour, units,
                              board)["home"]
    pairs = []
    for ui in range(len(units)):
        if ui in assign:
            continue
        ux, uy = units[ui]
        uquad = _quadrant_of(ux, uy, board)
        home_quad = home_quads.get(ui) or uquad
        for t in tasks:
            if t["key"] in claimed:
                continue
            if t.get("units") is not None and ui not in t["units"]:
                continue
            d = _dist(ux, uy, t["x"], t["y"])
            # V-T5 distance buckets dominate value (see BUCKET_DOMINANCE):
            # near (0-1) / local (2-4) / far (5+).  A nearby modest task now
            # always beats a distant rich one; value ranks inside a bucket.
            bucket = 0 if d <= 1 else (1 if d <= 4 else 2)
            score = tval(t) - TRAVEL_MU * d - bucket * BUCKET_DOMINANCE
            if _quadrant_of(t["x"], t["y"], board) != uquad:
                score -= CROSS_QUAD_PENALTY
            if _quadrant_of(t["x"], t["y"], board) != home_quad:
                score -= CROSS_SECTOR_PENALTY_V9
            score += float(t.get("_v9_soft", {}).get(ui, 0.0))
            need = t.get("need")
            if need:
                if _get(unit_inv(ui), need, 0) > 0:
                    score += 0.5 * tval(t)   # carriers converge on consumers
                else:
                    score -= 0.5 * tval(t)   # wheatless units de-prioritized
            if t["act"][0] == "PICKUP" and t["act"][1:2] == ["WHEAT"] \
                    and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                score -= 0.5 * tval(t)       # loaded carriers leave the shed
            if sticky.get(ui) == t["key"]:
                score += STICKY_BONUS
            pairs.append((score, ui, t["key"]))
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    for score, ui, key in pairs:
        if ui in assign or key in claimed:
            continue
        for t in tasks:
            if t["key"] == key:
                assign[ui] = t
                claimed.add(key)
                break

    # ---------------- act --------------------------------------------------
    half = board // 2
    shed_avail = _get(private, "shed", {}) or {}
    for ui, (ux, uy) in enumerate(units):
        chosen = assign.get(ui)
        if chosen is None:
            # act on the current tile anyway when something is executable
            # here and unclaimed (free op, zero travel)
            best_here = None
            for t in tasks:
                if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                    continue
                if not executable(t, ui):
                    continue
                if best_here is None or tval(t) > tval(best_here):
                    best_here = t
            if best_here is not None:
                claimed.add(best_here["key"])
                sticky[ui] = None
                actions.append(list(best_here["act"]))
            else:
                sticky[ui] = None
                actions.append(["PASS"])
            continue
        sticky[ui] = chosen["key"]
        cx, cy = chosen["x"], chosen["y"]
        need = chosen.get("need")
        if (ux, uy) == (cx, cy):
            if executable(chosen, ui):
                actions.append(list(chosen["act"]))
                continue
        # missing the carried item: fetch it at the shed BEFORE walking out
        # (r4-P1 fix for the wheatless-walker churn that collapsed feeding)
        if need and _get(unit_inv(ui), need, 0) <= 0:
            near = min(accesses, key=lambda p: _dist(ux, uy, p[0], p[1]))
            if (ux, uy) != near:
                actions.append(_step_towards(ux, uy, near[0], near[1]))
                continue
            chunk = {"WHEAT": 5, "FERTILIZER": 4, "COW": 2, "SHEEP": 2,
                     "GOOSE": 2}.get(need, 1)
            n = min(chunk, _get(shed_avail, need, 0))
            if n > 0:
                actions.append(["PICKUP", need, n])
                continue
        if (ux, uy) != (cx, cy):
            actions.append(_step_towards(ux, uy, cx, cy))
        else:
            # standing on it, item fetched, but the op went stale this turn
            sx, sy = half - 1, half - 1
            actions.append(_step_towards(ux, uy, sx, sy))

    # R6 guard: never request more PLANTs of a crop than seeds held
    seeds = _get(private, "seeds", {}) or {}
    demand = {}
    for a in actions:
        if a and a[0] == "PLANT":
            demand[a[1]] = demand.get(a[1], 0) + 1
    for crop, n in demand.items():
        if n > seeds.get(crop, 0):
            keep = seeds.get(crop, 0)
            for i, a in enumerate(actions):
                if a and a[0] == "PLANT" and a[1] == crop:
                    if keep > 0:
                        keep -= 1
                    else:
                        actions[i] = ["PASS"]
    return actions


def _task_sector(task, board):
    try:
        return _quadrant_of(int(task["x"]), int(task["y"]), board)
    except (KeyError, TypeError, ValueError):
        return None


# 【中文】v9 主场象限影子路由：给每个任务按工人附加 _v9_soft 软分
# （同区 0 / 跨区 -惩罚；本区有活且远区价值未超出 CROSS_SECTOR_VALUE_EDGE
# 时再叠加惩罚）——只调分、绝不收窄资格图（硬过滤实测会淹没跨区高价值
# 工作、把经济困死）。路线批量按"距离优先"排序（价值优先实测是假巡逻，
# 破坏近端浇水节奏）。红线任务完全豁免，Phase A 仍是硬安全否决。
def _route_tasks(obs, farm, private, day, tasks):
    """Add v9 home-sector eligibility without changing task semantics.

    A worker with useful work in its home sector is not offered distant work
    unless the distant task beats the best local value by
    ``CROSS_SECTOR_VALUE_EDGE``.  Red-line tasks are intentionally exempt and
    keep their original eligibility so phase A remains a hard safety veto.
    """
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units, _ = _telemetry_units(farm)
    player = _get(obs, "player", 0)
    state = _route_state(player, day, _get(obs, "hour", 0), units, board)
    copies = [copy.deepcopy(task) for task in tasks]
    active = {task.get("key") for task in copies}
    red_signature = tuple(sorted(repr(task.get("key")) for task in copies
                                 if task.get("red")))
    previous_red = state.get("red_signature", ())
    target_missing = any(key is not None and key not in active
                         for route in state["routes"].values() for key in route)
    changed = red_signature != previous_red or target_missing
    if changed:
        state["replans"] += 1
        state["routes"] = {ui: [] for ui in range(len(units))}
    state["red_signature"] = red_signature

    home = state["home"]
    normal = [task for task in copies if not task.get("red")]
    # Preserve the champion's full eligibility graph.  Sector routing is a
    # soft preference in the downstream score; hard filtering here caused
    # cross-sector high-value work to disappear and stranded the economy.
    original_units = {
        id(task): (set(task["units"]) if task.get("units") is not None
                   else set(range(len(units))))
        for task in normal
    }
    for task in normal:
        task["units"] = set(original_units[id(task)])

    for ui, (ux, uy) in enumerate(units):
        sector = home.get(ui, _quadrant_of(ux, uy, board))
        local = [task for task in normal if _task_sector(task, board) == sector
                 and ui in original_units[id(task)]]
        if local:
            best_local = max(float(task.get("v", task.get("w", 0)))
                              for task in local)
        else:
            best_local = 0.0

        # Attach worker-local soft scores rather than narrowing task
        # eligibility.  The legacy matcher still sees every legal task.
        for task in normal:
            task.setdefault("_v9_soft", {})[ui] = (
                0.0 if _task_sector(task, board) == sector
                else -CROSS_SECTOR_PENALTY_V9)
            if local and task.get("v", task.get("w", 0)) <= \
                    best_local + CROSS_SECTOR_VALUE_EDGE:
                task["_v9_soft"][ui] -= CROSS_SECTOR_PENALTY_V9

        # Retain a useful same-sector batch order in the route registry.  The
        # active task list is updated only on a completion/invalidity signal,
        # not rebuilt merely because the clock advanced one turn.
        current = state["routes"].setdefault(ui, [])
        if changed or not current:
            same = [task for task in copies
                    if not task.get("red") and
                    _task_sector(task, board) == sector and
                    (task.get("units") is None or ui in task["units"])]
            # Distance-first: a value-first head sent workers to far
            # high-value sector tasks (a false sweep) and broke the nearby
            # watering cadence -- measured as template_wheat/cow_baron seed
            # 101 regressions of -20k..-25k on both seats with water
            # pressure +22% (routing_tour, 2026-08-30).  Nearest-first is
            # the actual patrol: short hops, water stays local.
            same.sort(key=lambda task: (_dist(ux, uy, task["x"], task["y"]),
                                        -float(task.get("v", task.get("w", 0))),
                                        repr(task.get("key"))))
            state["routes"][ui] = [task.get("key") for task in same[:ROUTE_BATCH_SIZE]]

    # Route order is a deterministic tie breaker, while red lines still win
    # through the legacy scheduler's phase A.
    route_rank = {}
    for ui, route in state["routes"].items():
        for rank, key in enumerate(route):
            route_rank[(ui, key)] = rank
    for task in copies:
        task.setdefault("_v9_rank", {})
        if task.get("red"):
            continue
        for ui in range(len(units)):
            rank = route_rank.get((ui, task.get("key")))
            task["_v9_rank"][ui] = rank
            if rank is not None:
                task["_v9_soft"][ui] = task["_v9_soft"].get(ui, 0.0) + \
                    max(0.0, V9_TOUR_BONUS - rank * V9_TOUR_DECAY)
    return copies, state


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
V9_SHADOW_ROUTING = True


# 【中文】调度入口：先跑 _route_tasks 生成影子路由推荐，但 V9_SHADOW_
# ROUTING=True 时执行权仍交冠军调度器 _schedule_units_v72（原任务表），
# 影子结果只进 _SCHEDULER_TRACE 供遥测对比。切换 False 才会用 routed
# 任务表执行——见上方 V9_SHADOW_ROUTING 处的回归证据（2026-08-30 确认
# 门禁撤销合并：88-0 属选择域运气，泛化域配对净 -258.9k）。
def _schedule_units(obs, farm, private, day, tasks):
    """Keep champion actions while collecting v9 route recommendations.

    The partitioned route is shadow-only until it passes outcome and efficiency
    gates.  The frozen scheduler remains the execution authority, so telemetry
    can be validated without risking the production behavior.
    """
    routed, state = _route_tasks(obs, farm, private, day, tasks)
    if V9_SHADOW_ROUTING:
        actions = _schedule_units_v72(obs, farm, private, day, tasks)
    else:
        actions = _schedule_units_v72(obs, farm, private, day, routed)
    player = _get(obs, "player", 0)
    tiles = _get(farm, "tiles", []) or []
    board = len(tiles)
    units, _ = _telemetry_units(farm)
    sticky = _TARGETS.get(player, {}).get("assign", {})
    by_key = {task.get("key"): task for task in routed}
    assign = {}
    action_targets = {}
    cross = 0
    for ui, task_key in sticky.items():
        task = by_key.get(task_key)
        if task is None:
            continue
        assign[ui] = task_key
        action_targets[ui] = (task["x"], task["y"])
        if ui < len(units) and _task_sector(task, board) != \
                state["home"].get(ui):
            cross += 1
        cargo = state["cargo"].setdefault(ui, {"phase": "idle", "item": None,
                                               "target": None})
        need = task.get("need")
        if need and _get((_get(private, "inventories", []) or [{}])[ui]
                         if ui < len((_get(private, "inventories", []) or []))
                         else {}, need, 0) <= 0:
            cargo.update({"phase": "pickup", "item": need,
                          "target": task_key})
        elif need:
            cargo.update({"phase": "deliver", "item": need,
                          "target": task_key})
        else:
            cargo.update({"phase": "idle", "item": None,
                          "target": task_key})
    state["last_assign"] = dict(assign)
    _SCHEDULER_TRACE[player] = {
        "day": day,
        "assign": dict(assign),
        "action_targets": action_targets,
        "home_sector": dict(state["home"]),
        "cross_quadrant": cross,
        "red_assignments": sum(1 for key in assign.values()
                               if by_key.get(key, {}).get("red")),
        "replans": state["replans"],
        "cargo": copy.deepcopy(state["cargo"]),
    }
    return actions


# 【中文】═══ 入口：每回合的动作编排 ═══
# 流水线：取当日宏观计划（缓存）→ _build_tasks 铺任务表 →
# _schedule_units 分派工人动作 → _market_orders 编排订单 →
# 黎明雇工（仅 hour≤2，逐单按斐波那契实价且留 60 现金垫）→
# 排序"雇工→买单→卖单"（丢一单卖下回合补，丢一单 HIRE/BUY 损失一整天
# 计划）→ 末日只留 SELL → 按本回合 DROP 动作预演库容 →
# plan_market_orders 官方语义预算截断到 10 单 → 返回
# {"farmer":…, "hands":[…], "market":[…]}；任何异常兜底返回合法空动作
# （提交永不崩溃）。
def agent(obs):
    """Entry point: one action dict per turn (official Quick-Start signature)."""
    try:
        player = _get(obs, "player", 0)
        farms = _get(obs, "farms", [])
        if not farms or player >= len(farms):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farm = farms[player]
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        tiles = _get(farm, "tiles", [])
        if not tiles:
            return {"farmer": ["PASS"], "hands": [], "market": []}

        # r5-P4: the daily macro plan (DEFENSIVE = conservative r4 frame) is
        # computed once per day-hour cache and threaded through every
        # planner; any failure inside the gate already fell back to it.
        plan = _macro_plan(player, obs, day)
        tasks, animals_to_feed, herd_total, wheat_tiles, capacity = \
            _build_tasks(obs, farm, private=_get(obs, "private", {}) or {},
                         day=day, plan=plan)
        actions = _schedule_units(obs, farm, _get(obs, "private", {}) or {},
                                  day, tasks)
        orders = _market_orders(obs, farm, _get(obs, "private", {}) or {},
                                day, animals_to_feed, herd_total, plan=plan)

        # FM-O2/R3-4 labour: hire up to the plan in a dawn burst (hands reset
        # every morning; one HIRE per order; only hour <= 2 can hire -- m2b
        # fix).  Each emitted HIRE is affordable at its exact fib price.
        hires = []
        if day < SEASON_DAYS - 1 and hour <= HIRE_HOUR_MAX:
            quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
            hands_t = _crew_target(day, herd_total, wheat_tiles, quads,
                                   plan)
            # r4-P3 drawdown: past CREW_LATE_DAY the field shrinks (crops
            # harvested, phases closed) -- the 12-hand crew's fib bill
            # (322/day) outruns the remaining queue value
            if day >= CREW_LATE_DAY:
                hands_t = min(hands_t, CREW_LATE_CAP)
            hands = len(_get(farm, "hands", []) or [])
            money = _get(farm, "money", 0.0)
            spend = 0
            for i in range(hands, hands_t):
                cost = _hire_cost(i)
                # keep a working-cash cushion: a broke dawn cannot hire the
                # crew that would earn it back (measured day-8 stall)
                if spend + cost > money - 60 or len(hires) >= HIRE_BURST:
                    break
                spend += cost
                hires.append(["HIRE"])

        # buys before sells (a dropped sell tranche simply repeats next
        # turn, while a dropped HIRE/BUY loses a whole day of the plan);
        # dawn hires lead the queue.
        buys = [o for o in orders if o[0] != "SELL"]
        sells = [o for o in orders if o[0] == "SELL"]
        orders = hires + buys + sells

        # Final defense and a single official-semantics budget pass. Priority
        # chooses which original columns survive max-10; accepted columns retain
        # their original order, so dawn HIRE/BUY_LAND and lockstep BUY/SELL stay
        # engine-compatible.
        orders = [o for o in orders
                  if len(o) < 3 or (isinstance(o[2], (int, float)) and o[2] > 0)]
        if day >= SEASON_DAYS - 1:
            orders = [o for o in orders if o[0] == "SELL"]
        private = _get(obs, "private", {}) or {}
        # The official step applies unit actions before market orders.  Model
        # only cargo that a carrier will actually DROP this turn so last-day
        # liquidation and capacity checks see the same post-unit shed state.
        prospective_shed = dict(_get(private, "shed", {}) or {})
        for ui, unit_action in enumerate(actions):
            if not unit_action or unit_action[0] != "DROP":
                continue
            inventories = _get(private, "inventories", []) or []
            carried = inventories[ui] if ui < len(inventories) else {}
            room = max(0, 100 - sum(prospective_shed.values()))
            for item, amount in carried.items():
                if room <= 0:
                    break
                if isinstance(amount, (int, float)) and amount > 0:
                    moved = min(int(amount), room)
                    prospective_shed[item] = prospective_shed.get(item, 0) + moved
                    room -= moved
        budget = plan_market_orders(
            orders, _get(farm, "money", 0.0),
            sum(v for v in (_get(private, "shed", {}) or {}).values()
                if isinstance(v, (int, float))),
            day=day, max_orders=10, shed_capacity=100,
            hires_today=_get(farm, "hires_today", 0),
            hands_count=len(_get(farm, "hands", []) or []),
            quadrants_owned=len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]),
            prices=_get(_get(obs, "market", {}) or {}, "prices", {}) or {},
            shed_stock=prospective_shed,
            market_inventory=_get(_get(obs, "market", {}) or {},
                                  "inventory", None) or None)
        orders = budget["accepted"]

        farmer = actions[0] if actions else ["PASS"]
        hands_actions = actions[1:]
        result = {"farmer": farmer, "hands": hands_actions,
                  "market": orders}
        _telemetry_record_turn(obs, farm, private, actions, tasks,
                               _SCHEDULER_TRACE.get(player, {}), orders)
        return result
    except Exception:
        # a submission must never crash: fall back to a safe legal action
        return {"farmer": ["PASS"], "hands": [], "market": []}
