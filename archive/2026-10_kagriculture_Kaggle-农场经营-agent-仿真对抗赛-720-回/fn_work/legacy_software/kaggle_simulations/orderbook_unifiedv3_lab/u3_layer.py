# ---- 件 U3：unified_v3 单核（柔窗+模型核+半量门；连续空间联合求解） --------
# 形态：内层全替换 + 尾块注入件（build_unified_v3 拼进 oc_c3 提交源尾部；
# 与 u1 同一手术面 8 站点：p_next 4 处 + 量帽 4 处）。单核每拍对
# MILK/STRAWBERRY/WOOL（CARROT 可选未启用，站点面 _S758_ITEMS 不动）做
# 卖时+卖量+窗联合决策。定理链（D4）：软（跌幅半量）>硬（全拦）>拼装；
# 取整丢分辨率→比较全用连续价（u1v2 件）；mpx 焦窗=对强枷锁→柔窗。
# 两形态同手术面对照（D5 推翻性发现并入）：
#   形态 peak（v3k，原设计）：柔窗=小时权重 h14-22 主权重 1.0、邻近小时
#     h10-13/23 权重 0.5（窗外 0=抑制）；触发=预测连续跌>$0.5→半量、
#     现价≥连续投影峰→全量（帽内）、窗将关闭末拍清剩余；MR≤0 截止
#     （平局破向卖出，u1v2 臂 B 同容差语义）；滞留保险沿 expx_v2。
#   形态 platform（v3p，D5 平台语义主形态）：顶强不做价峰择时（D5 实据：
#     卖单放行=有货即反应式分小单卖出、lot 沿帽 3/6/10 小批、价格分位是
#     结果非门槛、d12-24 平台持续投放非脉冲）→ 第三条款改平台语义：小单
#     持续放行不等峰；跌幅>$0.5 半量保留；柔窗权重=d12-24 平台（step
#     [288,576)）权重 1.0、其余 0.5（产线节奏对齐）；连续空间比较仅用于
#     跌幅判定（无峰比较、无 MR 坡道）。
# 共同：①胜位守卫 648 后回基线（fire_x=fire_base+基线量帽，零足迹）；
# 异常回退基线语义；非触发拍零足迹（影子基线决策并行台账）；零跨拍挪量；
# 磁带 blob 零触碰；只挂卖自己投射仓存量（宿主守卫沿用）。
_U3_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
_U3_K = __U3_K__
_U3_WIN_END = __U3_WIN_END__
_U3_TERM = __U3_TERM__
_U3_WIN_START = 144
_U3_PLATFORM_LO = 288
_U3_PLATFORM_HI = 576
_U3_CAPS = (3, 6, 10)
_U3_MAX_BATCH = 40
_U3_TOL = 0.5
_U3_FORM = __U3_FORM__
_U3_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_U3_STATE = {}
_U3_DEC = {}
_U3_REPORT = {
    "calls": 0, "fires": 0, "holds": 0, "units": 0, "base_fires": 0,
    "mr_limited": 0, "cap_limited": 0, "censored_lo": 0, "errors": 0,
    "post_win_base": 0, "stranding_insured": 0, "window_suppressed": 0,
    "closing_fires": 0, "half_fires": 0, "peak_fulls": 0,
    "platform_fires": 0, "decision_diff_steps": [],
}


def _u3_reset():
    _U3_STATE.clear()
    _U3_DEC.clear()
    _U3_REPORT.update(
        calls=0, fires=0, holds=0, units=0, base_fires=0, mr_limited=0,
        cap_limited=0, censored_lo=0, errors=0, post_win_base=0,
        stranding_insured=0, window_suppressed=0, closing_fires=0,
        half_fires=0, peak_fulls=0, platform_fires=0)
    _U3_REPORT["decision_diff_steps"] = []


def _u3_diff(step):
    lst = _U3_REPORT["decision_diff_steps"]
    if step not in lst and len(lst) < 400:
        lst.append(int(step))
        lst.sort()


def _u3_price(item, inv, params):
    """基座取整价（影子基线口径=保真；显示/结算价才取整）。"""
    return float(_r37_market_price(item, int(inv), params))


def _u3_price_c(item, inv, params):
    """连续价（price(inv) 曲线原值不取整，$1 地板仍生效）——决策比较专用。"""
    p = (params or _R37_MARKET_PARAMS)[item]
    base = p["base"]
    I0 = p["I0"]
    T = p["T"]
    if inv < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _r37_shape(f, T, T)
        price = base + amp * _r37_shape(f, I0 - inv, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _r37_shape(f, T, T)
        price = base - amp * _r37_shape(f, inv - I0, T)
    return max(float(_R37_PRICE_FLOOR), float(price))


def _u3_params(observation):
    try:
        params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
        for k, patch in (((observation or {}).get("market") or {})
                         .get("params") or {}).items():
            if k in params and isinstance(patch, dict):
                params[k].update(patch)
        return params
    except Exception:
        return None


def _u3_draw(item, step, shops):
    d = 0
    if step % 4 == 0:
        for s in shops or ():
            prods = _U3_SHOPS.get(s) or ()
            if item in prods:
                d += 2 if len(prods) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        d += 1
    return d


def _u3_rival(player, item):
    hist = (_U3_STATE.get(player) or {}).get("hist", {}).get(item) or []
    if not hist:
        return 0.0
    tail = hist[-4:]
    return max(0.0, sum(tail) / len(tail))


def _u3_update(observation, step):
    player = int((observation or {}).get("player", 0))
    market = (observation or {}).get("market") or {}
    inv_all = market.get("inventory") or {}
    prices = market.get("prices") or {}
    shops = ((observation or {}).get("town") or {}).get("unlocked_shops") or []
    st = _U3_STATE.setdefault(player, {"hist": {}})
    inv_now = {i: int(inv_all.get(i, 0)) for i in _U3_ITEMS}
    prev = st.get("inv_prev")
    own_prev = st.get("own_prev") or {}
    if prev is not None and st.get("step_prev") == step - 1:
        for i in _U3_ITEMS:
            slot = own_prev.get(i) or {}
            d = (inv_now[i] - int(prev.get(i, 0))
                 + _u3_draw(i, step - 1, shops) - int(slot.get("vis", 0)))
            hist = st["hist"].setdefault(i, [])
            hist.append(max(0, d))
            if len(hist) > 12:
                del hist[:6]
            if int(slot.get("floor", 0)) > 0 or int(prices.get(i, 0)) <= 1:
                _U3_REPORT["censored_lo"] += 1
    st["inv_prev"] = inv_now
    st["step_prev"] = step
    st["shops"] = shops


def _u3_note_own(observation, action):
    player = int((observation or {}).get("player", 0))
    prices = ((observation or {}).get("market") or {}).get("prices") or {}
    own = {}
    for o in (action or {}).get("market") or []:
        if not (isinstance(o, (list, tuple)) and len(o) >= 3
                and o[0] == "SELL" and str(o[1]) in _U3_ITEMS):
            continue
        try:
            q = int(o[2])
        except Exception:
            continue
        if q <= 0:
            continue
        slot = own.setdefault(str(o[1]), {"vis": 0, "floor": 0})
        if int(prices.get(str(o[1]), 0)) > 1:
            slot["vis"] += q
        else:
            slot["floor"] += q
    st = _U3_STATE.setdefault(player, {"hist": {}})
    st["own_prev"] = own


def _u3_w(step):
    """柔窗权重（卖时+卖量+窗联合优化的窗变量）。
    peak：h14-22 主权重 1.0、邻近小时 h10-13/23 权重 0.5、窗外 0（抑制）。
    platform：d12-24 平台 [288,576) 权重 1.0、其余 0.5（产线节奏对齐）。"""
    s = int(step)
    if _U3_FORM == "platform":
        if _U3_PLATFORM_LO <= s < _U3_PLATFORM_HI:
            return 1.0
        return 0.5
    h = s % 24
    if 14 <= h <= 22:
        return 1.0
    if h in (10, 11, 12, 13, 23):
        return 0.5
    return 0.0


def _u3_cap(p_now, step):
    """量帽钉死 (3,6,10)（mpx _mx_cap 字面量语义；帽位=已判死门旋钮）。"""
    c1, c2, c3 = _U3_CAPS
    if p_now >= 100:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 30:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 10:
        return c2
    return c1


def _u3_shape(q_lot, drop_c):
    """半量门（drop_half 语义并入单核）：预测连续跌>$0.5→半量（≥1）。"""
    if float(drop_c) > _U3_TOL:
        return max(1, int(q_lot) // 2), True
    return int(q_lot), False


def _u3_traj(item, step, inv, rival, shops, params, horizon=None):
    """K=12 拍 inv 轨迹（expx 同源：inv+rival−town_draw）。"""
    k = int(horizon or _U3_K)
    cur = float(inv)
    traj = []
    for t in range(1, k + 1):
        cur = cur + rival - _u3_draw(item, step + t - 1, shops)
        traj.append(max(0.0, cur))
    return traj


def _u3_mr_qty(item, inv, traj, sel, params, q_grant):
    """MR≤0 截止（平局破向卖出；连续空间增量坡道）。返回 (q, limited)。"""
    q = 0
    shift = 0
    while q < int(q_grant) and q < _U3_MAX_BATCH:
        now_c = _u3_price_c(item, inv + shift, params)
        if sel:
            hold_c = max(_u3_price_c(item, traj[t - 1] + shift, params)
                         for t in sel)
        else:
            hold_c = 0.0
        if now_c < hold_c:
            break
        q += 1
        if now_c > 1:
            shift += 1
    return q, bool(q < int(q_grant))


def _u3_pnext(item, step, inv, rival_avg, avail, p_now, planned, observation):
    """统一求解核·何时卖+卖多少（连续空间；哨兵过基座门，阈比较全在核内）。
    胜位守卫①648 后回基线；异常回退基线。"""
    try:
        p_cur = _u3_price(item, inv, None)
        inv_next = inv + rival_avg + planned - _s758_draw_units(item, step)
        p_next_base = _u3_price(item, max(0, int(inv_next)), None)
        fire_base = p_next_base < p_cur - 0.5
    except Exception:
        fire_base = False
        p_next_base = 1e18
        p_cur = 1e18
    try:
        _U3_REPORT["calls"] += 1
        if fire_base:
            _U3_REPORT["base_fires"] += 1
        step = int(step)
        if step >= _U3_WIN_END:
            _U3_REPORT["post_win_base"] += 1
            _U3_DEC[(step, str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "q": None, "traj": None,
                "rival": 0.0, "peak": None, "drop_c": None, "closing": False,
                "insured": False, "mode": "post_win_base"}
            return float(p_next_base)
        w_now = _u3_w(step)
        if w_now <= 0:
            _U3_REPORT["window_suppressed"] += 1
            _U3_DEC[(step, str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": False, "q": 0, "traj": None, "rival": 0.0,
                "peak": None, "drop_c": None, "closing": False,
                "insured": False, "mode": "window_suppressed"}
            if fire_base:
                _u3_diff(step)
            return 1e18
        params = _u3_params(observation)
        player = int((observation or {}).get("player", 0))
        st = _U3_STATE.get(player) or {}
        shops = st.get("shops") or []
        rival = _u3_rival(player, item)
        traj = _u3_traj(item, step, inv, rival, shops, params)
        cap = _u3_cap(p_now, step)
        p_cur_c = _u3_price_c(item, inv, params)
        inv_next_c = max(0.0, inv + rival_avg + planned
                         - _u3_draw(item, step, shops))
        p_next_c = _u3_price_c(item, inv_next_c, params)
        drop_c = p_cur_c - p_next_c
        if _U3_FORM == "platform":
            # 平台语义：小单持续放行不等峰（有货即反应式分小单卖出）；
            # 跌幅>$0.5 半量（软门保留）；连续空间比较仅用于跌幅判定。
            _U3_REPORT["platform_fires"] += 1
            q_lot = max(1, int(cap * w_now))
            q, half = _u3_shape(q_lot, drop_c)
            if half:
                _U3_REPORT["half_fires"] += 1
            q = min(int(avail), q)
            fire_x = True
            if q <= 0:
                fire_x = False
            _U3_DEC[(step, str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_x), "q": int(q), "traj": traj,
                "rival": rival, "peak": None, "drop_c": float(drop_c),
                "closing": False, "insured": False, "mode": "platform"}
            if bool(fire_base) != bool(fire_x):
                _u3_diff(step)
            if fire_x:
                _U3_REPORT["fires"] += 1
            else:
                _U3_REPORT["holds"] += 1
            return -1e18 if fire_x else 1e18
        sel = [t for t in range(1, _U3_K + 1)
               if step + t < _U3_WIN_END and _u3_w(step + t) > 0]
        closing = not sel
        peak_c = None
        q = 0
        insured = False
        cap_w = max(1, int(cap * w_now))
        if closing:
            _U3_REPORT["closing_fires"] += 1
            fire_x = True
            q = min(int(avail), cap)
        else:
            peak_c = max(_u3_price_c(item, traj[t - 1], params) for t in sel)
            if p_cur_c >= peak_c:
                _U3_REPORT["peak_fulls"] += 1
                fire_x = True
                q_grant = min(int(avail), cap_w)
            elif drop_c > _U3_TOL:
                fire_x = True
                q_grant = min(int(avail), max(1, cap_w // 2))
            else:
                fire_x = False
                q_grant = 0
            if fire_x:
                q_mr, limited = _u3_mr_qty(item, inv, traj, sel, params,
                                           q_grant)
                q = min(q_grant, max(1, q_mr))
                if drop_c > _U3_TOL and p_cur_c < peak_c:
                    _U3_REPORT["half_fires"] += 1
                if limited:
                    _U3_REPORT["mr_limited"] += 1
                else:
                    _U3_REPORT["cap_limited"] += 1
                # ②胜位守卫·滞留保险（连续价峰值判）
                if q < min(int(avail), q_grant) or limited:
                    until = _U3_WIN_END
                    stock = int(avail)
                    if step >= until - 1:
                        leftover = stock
                    else:
                        traj2 = _u3_traj(item, step, inv, rival, shops, params,
                                         horizon=until - 1 - step)
                        sel2 = [i2 + 1 for i2 in range(len(traj2))
                                if step + i2 + 1 < _U3_WIN_END
                                and _u3_w(step + i2 + 1) > 0]
                        quotes = {t: _u3_price_c(item, traj2[t - 1], params)
                                  for t in sel2}
                        leftover = stock
                        for t in sel2:
                            if leftover <= 0:
                                break
                            fwd = [quotes[u] for u in sel2 if t < u <= t + _U3_K]
                            is_peak = (not fwd) or (
                                quotes[t] >= max(fwd) - _U3_TOL)
                            if is_peak:
                                leftover -= min(cap, leftover)
                    if leftover > 0:
                        q = min(int(avail), cap)
                        insured = True
                        _U3_REPORT["stranding_insured"] += 1
            if fire_x and q <= 0:
                fire_x = False
        _U3_DEC[(step, str(item))] = {
            "p_cur": p_cur, "fire_base": bool(fire_base),
            "fire_x": bool(fire_x), "q": int(q), "traj": traj,
            "rival": rival, "peak": peak_c, "drop_c": float(drop_c),
            "closing": closing, "insured": insured, "mode": "peak"}
        if bool(fire_base) != bool(fire_x):
            _u3_diff(step)
        if fire_x:
            _U3_REPORT["fires"] += 1
        else:
            _U3_REPORT["holds"] += 1
        return -1e18 if fire_x else 1e18
    except Exception:
        _U3_REPORT["errors"] += 1
        try:
            _U3_DEC[(int(step), str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "q": None, "traj": None,
                "rival": 0.0, "peak": None, "drop_c": None, "closing": False,
                "insured": False, "mode": "fallback"}
        except Exception:
            pass
        return float(p_next_base)


def _u3_take(item, step, inv, p_now, cap_base, avail, observation):
    """统一求解核·卖多少回读（异常回退基线量帽）。"""
    dec = _U3_DEC.get((int(step), str(item))) or {}
    fire_base = bool(dec.get("fire_base"))
    base_posted = min(int(avail), int(cap_base)) if fire_base else 0
    try:
        if int(step) >= _U3_WIN_END:
            q = int(cap_base)
            _U3_REPORT["post_win_base"] += 1
        else:
            q = int(dec.get("q") or 0)
        x_posted = min(int(avail), q)
        if x_posted != base_posted:
            _u3_diff(step)
        if x_posted > 0:
            _U3_REPORT["units"] += x_posted
        return q
    except Exception:
        _U3_REPORT["errors"] += 1
        return int(cap_base)
