# ---- 件 X2：日新高簇补全（tetsutani step928/948 语义差补齐） ----------------
# 形态：尾块注入件（构建时文本拼接进提交源，与基座同命名空间）；本文件为块体
# 片段，不含宿主捕获/入口（由 build_d27.py 组装）。仅用基座裸名
# （quote_context/_DH_ITEMS/_DH_SPEND/_xd7_projected）；stdlib-only。
#
# 逐条 diff（对照 /tmp/a30-b1/tetsu_agent/main.py step928 L8728-8783 /
# step948 L8946-8987，只补缺的守卫，不重构既有层）：
# 1. "父链未在卖"口径（补缺）：A 件 detect_dayhigh 在父链已挂该品 SELL 时整品
#    跳过；928/948 的口径是 already 扣减后卖残量（avail=projected−already）。
#    本层补齐该残量变现（含父链在卖场景）；A 件既有层不动。
# 2. "当日 PICKUP 跳过"（补缺）：928/948 的 avail 基=projected_shed（同拍
#    PICKUP 减仓/DROP/PLACE 加仓后的投射仓）；A 件用裸 shed。本层残量计算用
#    投射仓基（同拍 PICKUP 使 avail<=0 即跳过）。
# 3. "追加单并首单"（补缺守卫）：950 口径=并入最早**qty>0**同品 SELL 槽；A 件
#    plan_dayhigh_sells 并最早同品槽但无 qty>0 过滤。本层追加按 950 口径。
# 4. 951 口径（A 件已覆盖）：无同品槽→插到首个花费单前（_DH_SPEND）。
# 5. quote<2 不触发（A 件既有守卫，保留沿用）；948 每拍 +1 单上限 vs 928 多单
#    （家族内不一致在册）——本层沿 A 件多单口径（price×avail 降序）。
# 6. step928/948 的 _RACE_STATE['prev_action'] 回写守卫：A 件缺，本层**不补**
#    （回写会经反克隆 _race_lost 状态链产生非触发拍级联足迹，与预登记
#    "非触发拍零足迹"判据冲突；残留语义差在报告列明）。
# 7. 跟踪器 step 回退复位（928/948 `step<=last` 守卫）：本层自带跟踪器补齐。
# 零足迹：触发条件不成立/无残量 → 原动作对象返回。
_X2_REPORT = dict(calls=0, triggers=0, added_orders=0, added_units=0,
                  merged=0, inserted=0, dropped_full=0, pickup_skip=0,
                  reset=0, errors=0)
_X2_TRACKER = {}


def _x2_reset():
    _X2_REPORT.update(calls=0, triggers=0, added_orders=0, added_units=0,
                      merged=0, inserted=0, dropped_full=0, pickup_skip=0,
                      reset=0, errors=0)
    _X2_TRACKER.clear()


def _x2_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _x2_post(observation, action):
    """日新高簇补全残量变现（同拍追加族；零跨拍挪量）。

    输入: 当前拍 observation+宿主动作 / 输出: 追加后动作（无追加=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _X2_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list):
            return action
        step = int((observation or {}).get("step", 0))
        st = _X2_TRACKER
        if not st or step <= int(st.get("last", -1)):
            _X2_TRACKER.clear()
            st = _X2_TRACKER
            _X2_REPORT["reset"] += 1
        st["last"] = step
        ctx = quote_context(observation, st)
        if not isinstance(ctx, dict):
            return action
        base_highs = ctx.get("day_highs")
        quotes = ctx.get("quote")
        if not isinstance(base_highs, dict) or not isinstance(quotes, dict):
            return action
        # 触发集：7 品严格新高 ∧ quote>=2（A 件既有守卫沿用）∧ 有基线
        trigs = []
        for item in _DH_ITEMS:
            price = quotes.get(item)
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                continue
            price = float(price)
            if price < 2.0:
                continue
            high = base_highs.get(item)
            if high is None:
                continue  # 当日/跟踪首见无基线→无严格新高（928/948 同口径）
            if not price > float(high):
                continue
            trigs.append((item, price))
        if not trigs:
            return action
        projected = dict(_xd7_projected(observation, action))
        # already 扣减（928/948 口径）：同品 SELL 已挂量（max(0,qty)；不确定→该品跳过）
        plans = []
        for item, price in trigs:
            already, unsure = 0, False
            for order in market:
                if not isinstance(order, (list, tuple)) or len(order) < 3:
                    continue
                if order[0] != "SELL" or order[1] != item:
                    continue
                q = _x2_qty(order[2])
                if q is None:
                    unsure = True
                    break
                already += max(0, q)
            if unsure:
                continue
            avail = int(projected.get(item, 0)) - already
            if avail <= 0:
                if already > 0:
                    _X2_REPORT["pickup_skip"] += 1  # 同拍 PICKUP/已挂满→跳过
                continue
            plans.append((item, price, avail, price * avail))
        if not plans:
            return action
        _X2_REPORT["triggers"] += 1
        plans.sort(key=lambda r: (-r[3], r[0]))  # price×avail 降序（A 件口径）
        work = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
        applied = 0
        for item, price, avail, _value in plans:
            target = -1
            for i, order in enumerate(work):
                if isinstance(order, (list, tuple)) and len(order) >= 3 \
                        and order[0] == "SELL" and order[1] == item:
                    q = _x2_qty(order[2])
                    if q is not None and q > 0:
                        target = i  # 950 口径：最早 qty>0 同品 SELL 槽
                        break
            if target >= 0:
                work[target] = ["SELL", item,
                                _x2_qty(work[target][2]) + avail]
                _X2_REPORT["merged"] += 1
                applied += 1
            elif len(work) < 10:
                pos = len(work)
                for i, order in enumerate(work):
                    if isinstance(order, (list, tuple)) and order \
                            and order[0] in _DH_SPEND:
                        pos = i  # 951 口径：首个花费单前
                        break
                work.insert(pos, ["SELL", item, avail])
                _X2_REPORT["inserted"] += 1
                applied += 1
            else:
                _X2_REPORT["dropped_full"] += 1  # 10 槽满弃追加（A 件口径）
                continue
            _X2_REPORT["added_orders"] += 1
            _X2_REPORT["added_units"] += avail
        if applied == 0:
            return action  # 同对象零足迹
        return dict(action, market=work)
    except Exception:
        _X2_REPORT["errors"] += 1
        return action  # 异常吞掉回退原动作（同对象零足迹）
