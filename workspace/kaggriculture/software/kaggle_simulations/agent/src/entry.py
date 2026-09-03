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

        # r5-P4: the daily macro plan (DEFENSIVE = conservative r4 frame) is
        # computed once per day-hour cache and threaded through every
        # planner; any failure inside the gate already fell back to it.
        plan = _macro_plan(player, obs, day)
        tasks, animals_to_feed, herd_total, wheat_tiles, capacity = \
            _build_tasks(obs, farm, private=_get(obs, "private", {}) or {},
                         day=day, plan=plan)

        # M2/M4 (scheduler §2-§4, LIVE per user ruling 2026-09-02 "no local
        # evidence gates -- deploy and validate online"): the mission package
        # is the primary pipeline.  _schedule_units (v72) stays as a
        # single-turn bridge for executor replan turns (assertion failed ->
        # the old authority covers the red lines while the day rebuild
        # lands) and remains fully in charge when the flag is off.
        mission = _mission_shadow_update(player, day, hour, obs, farm,
                                         _get(obs, "private", {}) or {},
                                         plan, tasks)
        actions = None
        if ROUTE_EXECUTOR_ENABLED and mission is not None:
            try:
                solved = _solve_routes(
                    farm, _get(obs, "private", {}) or {}, day,
                    mission.get("tasks") or [])
                # M5 fix: _solve_routes returns {"routes": [...], ...} --
                # the pre-fix wiring passed the RESULT DICT, so the
                # executor iterated its string keys and excepted on ~97%
                # of turns (fail-open back to v72; only the d29 template
                # path ran -- the online 625.1 candidate was effectively
                # v72 + strategy-layer changes)
                cand, replan = _execute_routes(obs, farm,
                                                _get(obs, "private", {}) or {},
                                                day, solved.get("routes"))
                if replan:
                    # assertion failed (D1 ETA / EOD projection): rebuild is
                    # the doc's answer, but this turn's red lines cannot
                    # wait -- bridge to the proven scheduler once
                    actions = _schedule_units(
                        obs, farm, _get(obs, "private", {}) or {}, day,
                        tasks)
                else:
                    actions = cand
            except Exception:
                actions = None          # fall through to v72 (fail-open)
        if actions is None:
            actions = _schedule_units(obs, farm,
                                      _get(obs, "private", {}) or {},
                                      day, tasks)
        # MK-2/3 (market §2, LIVE per the same ruling): the dawn sell plan
        # drives the day's sell batches at their planned hours; the gate
        # stack remains as a bounded overlay on top.
        _sell_plan_shadow_update(player, day, hour, obs, farm,
                                 _get(obs, "private", {}) or {}, plan)
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
