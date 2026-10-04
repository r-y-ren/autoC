# ---- 件 I1：番茄晚市放量门（e087 CXTB 语义移植） --------------------------------
# 形态：尾块注入件（构建时文本拼接进提交源，与基座同命名空间）；本文件为块体
# 片段，不含宿主捕获/入口（由 build_iter1.py 组装）。仅用基座裸名
# （_ix_projected 由共享段提供）；stdlib-only。
#
# 语义移植自 mooman e087（sha ccba51e1…）增量 = CXTB 番茄晚市门：
# 阈值 9000→7500 + 对手番茄供给预测 + 排水余量，d26-29 释放 ~80 单元。
# 原件是**投资门**（day18 是否买地+10 番茄种），磁带手术级不可整搬；本端口
# 抽取其市场面机制重实现为**释放门**：读公开面算"对手下批供给压力"，d26-29
# 窗内按门释放番茄卖量（放量/挂起），零跨拍挪量（R23/R26 红线）。
#
# 公开面三件（任务口径）：
# - 对手在田番茄 yield 之和（farms[1-player].tiles 的 TOMATO yield_units 和）
#   = 对手下批供给压力的即时项；另按源件实测率 0.75/株/日 结转至季末（源件
#   _CXTB_THEIR_UNITS 语义：对手 committed 会补种），宁紧勿松取保守方向；
# - 市场库存 obs.market.inventory.TOMATO；
# - 排水节奏 = 每 4 步每店 1 件（PIZZA_SHOP/FARMERS_MARKET 各 6 件/日）
#   + 24 步中心全品 1 件（1/日），减源件实测排水余量 _CXTB_DRAIN_SLACK=2.4。
#
# 投影（源件 _cxtb_expected_revenue 语义）：逐日结转库存至 d29，我方 20 单元/日
# （源件 _CXTB_OUR_UNITS=20，10 株量级，d26-29 合计 ~80）按引擎自身曲线
# （_r37_market_price TOMATO，T=200）逐单元计价 → 逐日释放均价。
#
# 门（触发条件宁紧勿松；原语料唯一触发局 −741 教训）：
# - 阈值取源件两档中的**紧档**：9000/80 = 112.5 每单元（e087 放宽档
#   7500/80 = 93.75 不用）；今日投影释放均价 >= 阈值 → 放量，否则挂起；
# - 对手压力不可读 → 门关（宁紧勿松）；
# - 放量节奏：每日 ≤20 单元 + 结转挂起量（源件量级 ~80/窗）；
# - 终局营救：step>=712（d29 h16 后）强制清仓（未卖即废）。
#
# 零足迹纪律：窗外/无番茄量/门不改单/异常 → 返回原动作对象（同对象）。
# 触发面：每拍记 open/closed、放量/挂起、释放量/挂起量（judge 汇总）。
_I1_REPORT = dict(calls=0, changed_turns=0, window_out=0, no_tomato=0,
                  gate_open_ticks=0, gate_closed_ticks=0, release_ticks=0,
                  hold_ticks=0, added_units=0, held_units=0, released_units=0.0,
                  forced_release_units=0.0, released_today_units=0.0,
                  pressure_sum=0.0, day_px_sum=0.0, revenue_checks=0,
                  gate_errors=0, errors=0)
_I1_STATE = {"day": -1, "released_today": 0.0, "held_carry": 0.0, "step": -1}

_I1_MIN_REVENUE = 9000.0        # 源件紧档（e085=9000 / e087=7500；端口取紧档）
_I1_UNIT_FLOOR = _I1_MIN_REVENUE / 80.0   # 112.5 每单元（80 单元全额口径）
_I1_HARVEST_DAYS = (26, 27, 28, 29)
_I1_OUR_UNITS = 20              # 源件 _CXTB_OUR_UNITS=20（每日放量节奏）
_I1_DRAIN_SLACK = 2.4           # 源件实测排水余量
_I1_THEIR_UNITS = 0.75          # 源件实测对手结转率（每在田番茄株每日）
_I1_PENDING = {22: 0.25, 24: 0.25}   # 店铺解锁期望（源件：番茄店 2/8 概率）
_I1_FORCE_STEP = 712            # d29 h16 后强制清仓


def _i1_reset():
    _I1_REPORT.update(calls=0, changed_turns=0, window_out=0, no_tomato=0,
                      gate_open_ticks=0, gate_closed_ticks=0, release_ticks=0,
                      hold_ticks=0, added_units=0, held_units=0,
                      released_units=0.0, forced_release_units=0.0,
                      released_today_units=0.0, pressure_sum=0.0,
                      day_px_sum=0.0, revenue_checks=0, gate_errors=0, errors=0)
    _I1_STATE.update(day=-1, released_today=0.0, held_carry=0.0, step=-1)


def _i1_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _i1_their_pressure(obs):
    """对手下批供给压力 = 对手在田番茄 yield 之和（公开面）+ 在田株数。

    返回 (即时批 yield 之和, 在田株数)；读不到→None（门关，宁紧勿松）。
    """
    try:
        player = int((obs or {}).get("player", 0))
        farms = (obs or {}).get("farms") or []
        them = farms[1 - player]
        batch = 0.0
        tiles = 0
        for row in (them.get("tiles") or []):
            for t in row:
                if isinstance(t, dict) and t.get("crop") == "TOMATO":
                    tiles += 1
                    batch += max(0.0, float(t.get("yield_units", 0) or 0))
        return batch, tiles
    except Exception:
        return None


def _i1_day_unit_px(obs, pressure):
    """投影逐日我方 20 单元释放均价（源件 revenue 循环语义移植）。

    返回 (今日均价, 逐日均价表)；异常→None（门关）。
    """
    try:
        inv = float((((obs or {}).get("market") or {}).get("inventory")
                     or {}).get("TOMATO", 0))
        day = int((obs or {}).get("step", 0)) // 24
        shops = float(sum(s in ("PIZZA_SHOP", "FARMERS_MARKET")
                          for s in (((obs or {}).get("town") or {})
                                    .get("unlocked_shops") or [])))
        batch, tiles = pressure
        last = max(_I1_HARVEST_DAYS)
        day_px = {}
        for d in range(day, last + 1):
            shops += _I1_PENDING.get(d, 0.0)
            # 排水节奏：每店每 4 步 1 件（6/日）+ 中心每 24 步全品 1 件（1/日）
            # - 源件实测排水余量
            inv -= 1.0 + 6.0 * shops - _I1_DRAIN_SLACK
            inv += _I1_THEIR_UNITS * tiles          # 对手在田结转（宁紧勿松）
            if d == day:
                inv += batch                        # 对手下批即时压力先入账
            if d in _I1_HARVEST_DAYS:
                rev = 0.0
                for _ in range(_I1_OUR_UNITS):
                    rev += float(_r37_market_price("TOMATO", int(round(max(0.0, inv)))))
                    inv += 1
                day_px[d] = rev / float(_I1_OUR_UNITS)
        return day_px.get(day, 0.0), day_px
    except Exception:
        return None


def _i1_post(observation, action):
    """番茄晚市放量门（d26-29 同拍后处理）。

    输入: 当前拍 observation+宿主动作 / 输出: 门后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _I1_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return action
        try:
            step = int((observation or {}).get("step", 0))
        except Exception:
            step = 0
        day = step // 24
        if day < 26 or day > 29:
            _I1_REPORT["window_out"] += 1
            return action
        if _I1_STATE["step"] != step and step == 0:
            _i1_reset()          # 保险：直接调用层时也按局复位
        if _I1_STATE["day"] != day:
            _I1_STATE.update(day=day, released_today=0.0)
        # ---- 番茄量面：宿主卖出量 + 同拍动作后可卖仓 ----
        host_qty = 0.0
        unparsed = False
        for o in market:
            if isinstance(o, (list, tuple)) and len(o) >= 3 \
                    and o[0] == "SELL" and o[1] == "TOMATO":
                q = _i1_qty(o[2])
                if q is None:
                    unparsed = True
                    continue
                host_qty += max(0, q)
        shed = _ix_projected(observation, action)
        stock = max(0, int(shed.get("TOMATO", 0) or 0))
        if host_qty <= 0 and stock <= 0:
            _I1_REPORT["no_tomato"] += 1
            return action
        # ---- 门 ----
        forced = step >= _I1_FORCE_STEP
        gate_open = True
        day_px = None
        if not forced:
            pressure = _i1_their_pressure(observation)
            if pressure is None:
                _I1_REPORT["gate_errors"] += 1
                return action          # 门不可读→零足迹（宁紧勿松）
            got = _i1_day_unit_px(observation, pressure)
            if got is None:
                _I1_REPORT["gate_errors"] += 1
                return action
            day_px, _ = got
            _I1_REPORT["revenue_checks"] += 1
            _I1_REPORT["day_px_sum"] += float(day_px)
            _I1_REPORT["pressure_sum"] += float(pressure[0]) + \
                _I1_THEIR_UNITS * float(pressure[1])
            gate_open = float(day_px) >= _I1_UNIT_FLOOR
            _I1_REPORT["gate_open_ticks" if gate_open else "gate_closed_ticks"] += 1
        if forced:
            allowed = float("inf")          # 终局清仓
        elif gate_open:
            allowed = max(0.0, float(_I1_OUR_UNITS) - _I1_STATE["released_today"]) \
                + _I1_STATE["held_carry"]
        else:
            allowed = 0.0
        # ---- 重写卖单（放量≤allowed；其余挂起） ----
        kept_tomato = 0.0
        changed = False
        out = []
        budget = allowed
        for o in market:
            if not (isinstance(o, (list, tuple)) and len(o) >= 3
                    and o[0] == "SELL" and o[1] == "TOMATO"):
                out.append(o)
                continue
            q = _i1_qty(o[2])
            if q is None:
                out.append(o)               # 挂量不确定→原样保留（保守）
                continue
            q = max(0, q)
            keep = q if q <= budget else budget
            if keep < q:
                changed = True
                _I1_REPORT["held_units"] += q - keep
                _I1_STATE["held_carry"] += q - keep
            if keep > 0:
                budget -= keep
                kept_tomato += keep
                _I1_REPORT["released_units"] += keep
                _I1_STATE["released_today"] += keep
                if forced:
                    _I1_REPORT["forced_release_units"] += keep
                if keep != q:
                    out.append(["SELL", "TOMATO", int(keep)])
                else:
                    out.append(o)
            # keep==0 → 整条挂起移除
        # ---- 顶部补量：门开且仍有节奏额度+可卖仓，宿主没挂满 → 追加放量 ----
        topup_n = 0
        if (gate_open or forced) and budget > 0:
            spare = stock - kept_tomato
            if spare > 0 and len(out) < 10 and not unparsed:
                n = spare if budget == float("inf") else min(spare, int(budget))
                if n > 0:
                    out.append(["SELL", "TOMATO", int(n)])
                    topup_n = int(n)
                    kept_tomato += n
                    _I1_REPORT["added_units"] += n
                    _I1_REPORT["released_units"] += n
                    _I1_STATE["released_today"] += n
                    if forced:
                        _I1_REPORT["forced_release_units"] += n
                    changed = True
        if changed:
            _I1_REPORT["changed_turns"] += 1
            _I1_REPORT["released_today_units"] += kept_tomato
            if gate_open or forced:
                _I1_REPORT["release_ticks"] += 1
            else:
                _I1_REPORT["hold_ticks"] += 1
            return dict(action, market=out)
        if host_qty > 0 and (gate_open or forced):
            _I1_REPORT["release_ticks"] += 1      # 放量经原单透传（零改动）
        return action
    except Exception:
        _I1_REPORT["errors"] += 1
        return action          # 异常吞掉回退原动作（同对象零足迹）
