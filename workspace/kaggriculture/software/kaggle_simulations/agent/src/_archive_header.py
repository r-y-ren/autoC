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
