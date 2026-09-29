# ---- 件 U1：统一求解核（何时卖+卖多少=单一决策核，全替换形态） ----------
# 形态：内层全替换 + 尾块注入件（build_unified_u1 拼进 oc_c3 提交源尾部）。
# 替换点=MODELPX 整个决策规则（p_next 计算 4 处 + 量帽 4 处同文），一个求解核
# 同时决定"何时卖+卖多少"（非 mpx/expx 双层叠加——合装已判负）。每拍对
# MILK/WOOL/STRAWBERRY：
#   ①模型投影：K=12 拍价格轨迹（引擎公式 price(inv) 全表+城镇排水表+R28 删失
#     口径对手流估计——expx 件同源）；
#   ②窗约束（mpx 语义内化为约束集）：可卖拍=step∈[144,648) ∧ (step%24)∈
#     {14..22}（step 时段语义同 mpx 胜者件字面量 range(_MX_H0,23)、h0=14、
#     step 144-695 守卫；648 起由胜位守卫①交还基线）；窗外不卖（抑制）；
#   ③统一决策：现在卖 iff 当前报价 ≥ 窗内剩余可卖拍（K 拍投影内）的投影峰值
#     价（门字面量 p_next<p_cur-0.5 不动=阈 0.5 封印旋钮），或窗将关闭（剩余
#     可卖拍集为空=末拍清剩余）；量=min(帽 3/6/10, MR≤0 截止量)——帽=mpx 钉死
#     三档语义，MR≤0 截止=逐件 即时报价 price(inv+shift) > 窗内持有值（剩余
#     可卖拍投影峰值，吸收曲线计自家出货边际冲击）即卖、≤即停；
#   ④胜位守卫沿 expx_v2：①窗收缩 648 后回基线（fire_x=fire_base+基线量帽，
#     零足迹）②滞留保险（MR 持有时模型窗内峰值出货容量清不掉该件投射仓存量
#     →立即按基线语义出货）。
# 非触发拍零足迹（影子基线决策并行台账）；异常回退基线语义；零跨拍挪量、
# 磁带 blob 零触碰；只挂卖自己投射仓存量（宿主守卫沿用）。
_U1_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
_U1_K = __U1_K__
_U1_WIN_END = __U1_WIN_END__
_U1_TERM = __U1_TERM__
_U1_H0 = __U1_H0__
_U1_WIN_START = 144
_U1_CAPS = (3, 6, 10)
_U1_MAX_BATCH = 40
_U1_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_U1_STATE = {}
_U1_DEC = {}
_U1_REPORT = {
    "calls": 0, "fires": 0, "holds": 0, "units": 0, "base_fires": 0,
    "mr_limited": 0, "cap_limited": 0, "censored_lo": 0, "errors": 0,
    "post_win_base": 0, "stranding_insured": 0, "window_suppressed": 0,
    "closing_fires": 0, "decision_diff_steps": [],
}


def _u1_reset():
    _U1_STATE.clear()
    _U1_DEC.clear()
    _U1_REPORT.update(
        calls=0, fires=0, holds=0, units=0, base_fires=0, mr_limited=0,
        cap_limited=0, censored_lo=0, errors=0, post_win_base=0,
        stranding_insured=0, window_suppressed=0, closing_fires=0)
    _U1_REPORT["decision_diff_steps"] = []


def _u1_diff(step):
    lst = _U1_REPORT["decision_diff_steps"]
    if step not in lst and len(lst) < 400:
        lst.append(int(step))
        lst.sort()


def _u1_price(item, inv, params):
    return float(_r37_market_price(item, int(inv), params))


def _u1_params(observation):
    try:
        params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
        for k, patch in (((observation or {}).get("market") or {})
                         .get("params") or {}).items():
            if k in params and isinstance(patch, dict):
                params[k].update(patch)
        return params
    except Exception:
        return None


def _u1_draw(item, step, shops):
    d = 0
    if step % 4 == 0:
        for s in shops or ():
            prods = _U1_SHOPS.get(s) or ()
            if item in prods:
                d += 2 if len(prods) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        d += 1
    return d


def _u1_rival(player, item):
    hist = (_U1_STATE.get(player) or {}).get("hist", {}).get(item) or []
    if not hist:
        return 0.0
    tail = hist[-4:]
    return max(0.0, sum(tail) / len(tail))


def _u1_update(observation, step):
    player = int((observation or {}).get("player", 0))
    market = (observation or {}).get("market") or {}
    inv_all = market.get("inventory") or {}
    prices = market.get("prices") or {}
    shops = ((observation or {}).get("town") or {}).get("unlocked_shops") or []
    st = _U1_STATE.setdefault(player, {"hist": {}})
    inv_now = {i: int(inv_all.get(i, 0)) for i in _U1_ITEMS}
    prev = st.get("inv_prev")
    own_prev = st.get("own_prev") or {}
    if prev is not None and st.get("step_prev") == step - 1:
        for i in _U1_ITEMS:
            slot = own_prev.get(i) or {}
            d = (inv_now[i] - int(prev.get(i, 0))
                 + _u1_draw(i, step - 1, shops) - int(slot.get("vis", 0)))
            hist = st["hist"].setdefault(i, [])
            hist.append(max(0, d))
            if len(hist) > 12:
                del hist[:6]
            if int(slot.get("floor", 0)) > 0 or int(prices.get(i, 0)) <= 1:
                _U1_REPORT["censored_lo"] += 1
    st["inv_prev"] = inv_now
    st["step_prev"] = step
    st["shops"] = shops


def _u1_note_own(observation, action):
    player = int((observation or {}).get("player", 0))
    prices = ((observation or {}).get("market") or {}).get("prices") or {}
    own = {}
    for o in (action or {}).get("market") or []:
        if not (isinstance(o, (list, tuple)) and len(o) >= 3
                and o[0] == "SELL" and str(o[1]) in _U1_ITEMS):
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
    st = _U1_STATE.setdefault(player, {"hist": {}})
    st["own_prev"] = own


def _u1_sellable(step):
    """窗约束（mpx 胜者件字面量语义）：可卖拍=step∈[144,648) ∧ hour∈{14..22}。"""
    s = int(step)
    return _U1_WIN_START <= s < _U1_WIN_END and (s % 24) in range(_U1_H0, 23)


def _u1_cap(p_now, step):
    """量帽钉死 (3,6,10)（mpx _mx_cap 字面量语义；帽位=已判死门旋钮）。"""
    c1, c2, c3 = _U1_CAPS
    if p_now >= 100:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 30:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 10:
        return c2
    return c1


def _u1_traj(item, step, inv, rival, shops, params, horizon=None):
    """K 拍（或指定 horizon 拍）inv 轨迹（expx 同源：inv+rival−town_draw）。"""
    k = int(horizon or _U1_K)
    cur = float(inv)
    traj = []
    for t in range(1, k + 1):
        cur = cur + rival - _u1_draw(item, step + t - 1, shops)
        traj.append(max(0.0, cur))
    return traj


def _u1_pnext(item, step, inv, rival_avg, avail, p_now, planned, observation):
    """统一求解核·何时卖：窗内剩余可卖拍投影峰值；返回值过基座门
    p_next<p_cur-0.5（阈 0.5 封印）。胜位守卫①648 后回基线；窗外抑制；
    异常回退基线语义。"""
    try:
        p_cur = _u1_price(item, inv, None)
        inv_next = inv + rival_avg + planned - _s758_draw_units(item, step)
        p_next_base = _u1_price(item, max(0, int(inv_next)), None)
        fire_base = p_next_base < p_cur - 0.5
    except Exception:
        fire_base = False
        p_next_base = 1e18
        p_cur = 1e18
    try:
        _U1_REPORT["calls"] += 1
        if fire_base:
            _U1_REPORT["base_fires"] += 1
        step = int(step)
        if step >= _U1_WIN_END:
            # ①窗收缩：648 后回基线（fire_x=fire_base→零足迹）
            _U1_REPORT["post_win_base"] += 1
            _U1_DEC[(step, str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "q": None, "traj": None,
                "rival": 0.0, "peak": None, "closing": False,
                "insured": False, "mode": "post_win_base"}
            return float(p_next_base)
        if not _u1_sellable(step):
            # ②窗约束：可卖拍=h14-22；窗外抑制不卖（mpx 语义内化）
            _U1_REPORT["window_suppressed"] += 1
            _U1_DEC[(step, str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": False, "q": 0, "traj": None, "rival": 0.0,
                "peak": None, "closing": False, "insured": False,
                "mode": "window_suppressed"}
            if fire_base:
                _u1_diff(step)
            return 1e18
        params = _u1_params(observation)
        player = int((observation or {}).get("player", 0))
        st = _U1_STATE.get(player) or {}
        shops = st.get("shops") or []
        rival = _u1_rival(player, item)
        traj = _u1_traj(item, step, inv, rival, shops, params)
        sel = [t for t in range(1, _U1_K + 1) if _u1_sellable(step + t)]
        closing = not sel
        peak_x = None
        q = 0
        insured = False
        cap = _u1_cap(p_now, step)
        if closing:
            # ③窗将关闭：末拍清剩余（MR 截止放行至帽位/存量）
            _U1_REPORT["closing_fires"] += 1
            fire_x = True
            q = min(int(avail), cap)
        else:
            peak_x = max(_u1_price(item, traj[t - 1], params) for t in sel)
            fire_x = bool(peak_x < p_cur - 0.5)
            if fire_x:
                # ③量=min(帽 3/6/10, MR≤0 截止量)
                shift = 0
                while q < cap and q < _U1_MAX_BATCH:
                    now_px = _u1_price(item, inv + shift, params)
                    v_hold = max(_u1_price(item, traj[t - 1] + shift, params)
                                 for t in sel)
                    if now_px <= v_hold:
                        break
                    q += 1
                    if now_px > 1:
                        shift += 1
                if q >= cap:
                    _U1_REPORT["cap_limited"] += 1
                else:
                    _U1_REPORT["mr_limited"] += 1
                # ④胜位守卫②滞留保险：MR 持有且窗内峰值容量清不掉投射仓存量
                if q < min(int(avail), cap):
                    until = _U1_WIN_END
                    stock = int(avail)
                    if step >= until - 1:
                        leftover = stock
                    else:
                        traj2 = _u1_traj(item, step, inv, rival, shops, params,
                                         horizon=until - 1 - step)
                        sel2 = [i2 + 1 for i2 in range(len(traj2))
                                if _u1_sellable(step + i2 + 1)]
                        quotes = {t: _u1_price(item, traj2[t - 1], params)
                                  for t in sel2}
                        leftover = stock
                        for t in sel2:
                            if leftover <= 0:
                                break
                            fwd = [quotes[u] for u in sel2
                                   if t < u <= t + _U1_K]
                            is_peak = (not fwd) or (
                                quotes[t] >= max(fwd) - 0.5)
                            if is_peak:
                                leftover -= min(cap, leftover)
                    if leftover > 0:
                        q = min(int(avail), cap)
                        insured = True
                        _U1_REPORT["stranding_insured"] += 1
        _U1_DEC[(step, str(item))] = {
            "p_cur": p_cur, "fire_base": bool(fire_base),
            "fire_x": bool(fire_x), "q": int(q), "traj": traj,
            "rival": rival, "peak": peak_x, "closing": closing,
            "insured": insured, "mode": "unified"}
        if bool(fire_base) != bool(fire_x):
            _u1_diff(step)
        if fire_x:
            _U1_REPORT["fires"] += 1
        else:
            _U1_REPORT["holds"] += 1
        if fire_x and closing:
            return -1e18
        return float(peak_x)
    except Exception:
        _U1_REPORT["errors"] += 1
        try:
            _U1_DEC[(int(step), str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "q": None, "traj": None,
                "rival": 0.0, "peak": None, "closing": False,
                "insured": False, "mode": "fallback"}
        except Exception:
            pass
        return float(p_next_base)


def _u1_take(item, step, inv, p_now, cap_base, avail, observation):
    """统一求解核·卖多少：min(帽 3/6/10, MR≤0 截止量)；异常回退基线量帽。"""
    dec = _U1_DEC.get((int(step), str(item))) or {}
    fire_base = bool(dec.get("fire_base"))
    base_posted = min(int(avail), int(cap_base)) if fire_base else 0
    try:
        if int(step) >= _U1_WIN_END:
            q = int(cap_base)          # ①窗收缩：基线语义量帽
            _U1_REPORT["post_win_base"] += 1
        else:
            q = int(dec.get("q") or 0)
        x_posted = min(int(avail), q)
        if x_posted != base_posted:
            _u1_diff(step)
        if x_posted > 0:
            _U1_REPORT["units"] += x_posted
        return q
    except Exception:
        _U1_REPORT["errors"] += 1
        return int(cap_base)
