"""迁移登记——run_submission_agent · _exec_chain/entry（B13，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/src/entry.py（旧树冻结，零字节变更）
源 sha256: 27239a55d80b00509072b2e976b373d356f8f11aa1d8b53550bc7dc11f0fb1be
剥离清单（R10 死码不迁）: 无——entry.py 无 R10 清单内符号。本件零删改。
  整体 try/except → 合法 PASS 的 fail-open 第一道原样；DTSP 黎明钩子的
  三道 fail-open（restore_pristine+sticky_off+指纹不符）语义原样。
形态: 本文件 = 旧模块的迁移副本，落位 _exec_chain/（下划线开头=非函数文件区：
  exec 链基座件）；装载序位次=entry（十件之尾，见 load_agent_modules 的
  _MODULE_ORDER 真值；装载器随后的重绑把本件 agent 存为 _agent_impl）。
  新链语义注记：钩子优先消费装载期急切铸就的 DTSP_RUNTIME_MODULE（load_
  agent_modules 装载窗内完成，P4.1 红线），回合期 import planner.runtime
  回退支在新链不可达（DTSP_RUNTIME_MODULE 恒非 None）；该死支按原文保留
  ——不可达路径零行为面。除本登记头外源码逐字复制。
上游: R1, R10（fn_docs/responsibility.md 功能块 run_submission_agent）
"""

# ===========================================================================
# 【中文·模块导览】src/entry.py —— 提交入口（官方 get_last_callable 契约位）
# ---------------------------------------------------------------------------
# v10.9 职责：agent(obs) 每回合编排——当日宏观计划（缓存）→ _build_tasks
#   → _schedule_units → _market_orders → 黎明雇工 → 雇工/买/卖排序 →
#   末日只卖 → DROP 库容预演 → plan_market_orders 预算截断。恒最后合并
#   （构建器契约：文件最后 callable = agent）。
# 新架构落位：scheduler L4 就绪后，本入口收缩为"机械执行 + 市场层 +
#   断言"三件事（M4 切换点 ROUTE_EXECUTOR_ENABLED 在 executor.py）。
# 文档符合性审查：
#   ✓ 永不崩溃兜底（整体 try/except → 合法 PASS）与 10 单预算截断在场
#     （产品契约，四文档共同的"承重墙不动"项）；
#   ✗ 待办（M4）——_build_tasks/_schedule_units 调用替换为任务包+路线
#     +执行器三段；届时"何时必须有卖出"由卖出计划器供数（market
#     §2.5），本入口只保留编排与兜底。
# ===========================================================================


def _market_private_after_actions(private, actions):
    """Mirror unit actions that change private market-visible inventory."""
    market_private = dict(private or {})
    shed = dict(_get(private, "shed", {}) or {})
    inventories = [dict(inv or {})
                   for inv in (_get(private, "inventories", []) or [])]
    for ui, unit_action in enumerate(actions or []):
        if not unit_action or unit_action[0] != "DROP":
            continue
        carried = inventories[ui] if ui < len(inventories) else {}
        room = max(0, SHED_CAPACITY - sum(
            v for v in shed.values()
            if isinstance(v, (int, float)) and v > 0))
        for item, amount in list(carried.items()):
            if room <= 0:
                break
            if isinstance(amount, (int, float)) and amount > 0:
                moved = min(int(amount), room)
                shed[item] = shed.get(item, 0) + moved
                room -= moved
        if ui < len(inventories):
            inventories[ui] = {}
    market_private["shed"] = shed
    market_private["inventories"] = inventories
    return market_private


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

        # OBS bypass hook (fail-open, scheduler doc §3 / OBS v2 §3): the
        # day-account pass runs on the first action turn of each day and
        # never touches the decision path below.
        _opp_observer_update(obs, _get(obs, "private", {}) or {})

        # DTSP 黎明钩子（P3 最小接线；P4.1 导入解耦，2026-09-19；旗关零
        # 足迹有测试钉住）：只在提交入口 main.py 定义了 DTSP_RUNTIME_CONFIG
        # 的命名空间里活（旗关黄金/裸命名空间无此名字 → 死路，动作流与
        # v13.8 逐字节一致）。planner 运行时优先取 main.py 装载期急切导入
        # 的 DTSP_RUNTIME_MODULE（P4.1：官方 loader exec 后 pop 掉解包目录，
        # 回合期 sys.path 导入在线上必败——v1 零接合根因）；dev 命名空间
        # 无该名字时回退回合期导入。钩子自带三道 fail-open（恢复 v13.8
        # 快照 + PLANNER_ENABLED=False 粘性 + 遥测记因）；本 except 兜
        # runtime 模块本身不可用的包破损情形——旗关 + 清寄存器 + 记因
        # （_DTSP_HOOK_ERRORS：接合遥测的离线可观测通道），本回合照常走
        # v13.8 路径。
        _dtsp_cfg = globals().get("DTSP_RUNTIME_CONFIG")
        if _dtsp_cfg:
            try:
                _dtsp_runtime = globals().get("DTSP_RUNTIME_MODULE")
                if _dtsp_runtime is None:
                    import planner.runtime as _dtsp_runtime
                _dtsp_runtime.dawn_hook(obs, globals(), _dtsp_cfg,
                                        player=player, day=day, hour=hour)
            except Exception as _dtsp_exc:
                _dtsp_errs = globals().setdefault("_DTSP_HOOK_ERRORS", [])
                if isinstance(_dtsp_errs, list) and len(_dtsp_errs) < 16:
                    _dtsp_errs.append(f"{type(_dtsp_exc).__name__}: "
                                      f"{_dtsp_exc}")
                globals()["PLANNER_ENABLED"] = False
                if isinstance(globals().get("PLANNER_OVERRIDES"), dict):
                    globals()["PLANNER_OVERRIDES"].clear()

        # r5-P4: the daily macro plan (DEFENSIVE = conservative r4 frame) is
        # computed once per day-hour cache and threaded through every
        # planner; any failure inside the gate already fell back to it.
        plan = _macro_plan(player, obs, day)
        tasks, animals_to_feed, herd_total, wheat_tiles, capacity = \
            _build_tasks(obs, farm, private=_get(obs, "private", {}) or {},
                         day=day, plan=plan)

        # M2 (scheduler §2): the mission package stays the dawn
        # telemetry/M2-contract artifact (market consumes its EOD events).
        # M4/M5 (§3-§4): the four-layer dispatcher -- per-turn fresh tasks,
        # current-roster re-solve, mechanical execution -- is the ONLY
        # scheduling path; v72 and the execution flag were deleted with the
        # transition code.  The never-crash net is the product-contract
        # try/except around this whole function (safe PASS).
        mission = _mission_shadow_update(player, day, hour, obs, farm,
                                         _get(obs, "private", {}) or {},
                                         plan, tasks)
        private = _get(obs, "private", {}) or {}
        actions = _solve_and_execute(obs, farm, private, day, tasks)

        # Unit actions run before the market. Mirror successful DROP effects so
        # every market component sees one coherent post-unit shed/inventory
        # state. A HARVEST cannot also DROP in the same turn and is therefore
        # intentionally not made sellable here.
        market_private = _market_private_after_actions(private, actions)
        prospective_shed = market_private["shed"]

        # MK-2/3 (market §2, LIVE per the same ruling): the dawn sell plan
        # drives the day's sell batches at their planned hours; the gate
        # stack remains as a bounded overlay on top.
        sell_plan = _sell_plan_shadow_update(player, day, hour, obs, farm,
                                             market_private, plan)
        # §2.4 closure (aggressive wave B): the dawn sell plan is now
        # known -- rebuild today's mission with the real planned sell
        # volume so the EOD projection and its eod_budget SELL events
        # are exact, not the conservative planned_sell=0 snapshot.
        planned_total = 0
        for _line in ((sell_plan or {}).get("lines") or {}).values():
            _q = _line.get("qty_today", 0) if isinstance(_line, dict) else 0
            if isinstance(_q, (int, float)) and _q > 0:
                planned_total += int(_q)
        if planned_total > 0:
            _mission_refresh_planned_sell(player, day, hour, obs, farm,
                                          market_private, plan, tasks,
                                          planned_total)
        orders = _market_orders(obs, farm, market_private,
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
            # (322/day) outruns the remaining queue value.
            # DTSP 惰性旋钮（P2.5，缺口 6 P3 运行态姿态）：CATCHUP 类计划
            # 提前晚季降编/收紧帽，省日薪保流动性；旗关恒回冻结值。
            if day >= _plan_knob("crew_late_day", CREW_LATE_DAY):
                hands_t = min(hands_t, _plan_knob("crew_late_cap",
                                                  CREW_LATE_CAP))
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
        # v15 波次剧本例外（M-B）：flush 日（d6 羊毛/d10 瓜）同回合 SELL
        # 先于 BUY 入队——同序号 slot 锁步下先卖回血、当日 flush 现金直接
        # 融资买地/买畜（v48 资本波次的成交顺序语义）。旗关恒走原序。
        buys = [o for o in orders if o[0] != "SELL"]
        sells = [o for o in orders if o[0] == "SELL"]
        _wave_first_hook = globals().get("_wave_sell_first")
        if _wave_first_hook is not None and _wave_first_hook(day):
            orders = hires + sells + buys
        else:
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
        budget = plan_market_orders(
            orders, _get(farm, "money", 0.0),
            sum(v for v in prospective_shed.values()
                if isinstance(v, (int, float))),
            day=day, max_orders=10, shed_capacity=100,
            hires_today=_get(farm, "hires_today", 0),
            hands_count=len(_get(farm, "hands", []) or []),
            quadrants_owned=len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]),
            prices=_get(_get(obs, "market", {}) or {}, "prices", {}) or {},
            shed_stock=prospective_shed,
            market_inventory=_get(_get(obs, "market", {}) or {},
                                  "inventory", None) or None)
        _finalize_sell_plan_batches(player, day, orders, budget)
        orders = budget["accepted"]

        # OBS bypass hook: our accepted SELL/BUY_PRODUCT ledger (Ch0 input;
        # prices let the E1/E6 dual ledger split floor-price sells).
        _opp_note_orders(player, day, hour, orders,
                         _get(_get(obs, "market", {}) or {}, "prices", {})
                         or {})

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
