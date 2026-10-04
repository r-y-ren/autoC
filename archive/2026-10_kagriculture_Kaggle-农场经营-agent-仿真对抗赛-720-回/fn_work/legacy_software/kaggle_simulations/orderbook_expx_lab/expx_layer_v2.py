# ---- 件 EXPX-V2：MODELPX 预测核精确化 + 胜位守卫 ------------------------
# 形态：内层改造 + 尾块注入件（build_expx_v2 拼进 oc_c3 提交源尾部）。替换点
# =MODELPX 的 p_next 计算（4 处同文），与 v1 同式；在 v1 精确模型之上加**胜位
# 守卫**（v1 败因=尾部：2 翻负=同种子双席，回退点在窗外早局/末局滞留侧）：
#   ① 窗收缩：expx 仅 step 144-__EXPX_WIN_END__ 生效；其后全基线语义
#      （p_next/量帽回退基座公式，终局库存形态回归）；
#   ② 滞留保险：MR 持有时（本拍少卖）若投影自家模型窗内（step+1..647）的
#      局部峰值出货容量（峰值拍×基线帽，逐拍滚动扣减）清不掉该件投射仓
#      存量→立即按基线语义出货（防末局滞留；到 718 终局清算的强制出清面
#      由 ①交还基线+终局规划器接管，本保险保证不留到那一段）。
# 其余与 v1 同：精确价格投影（引擎公式全表+城镇排水表+R28 删失口径对手流）、
# 峰值拍出货门（p_next<p_cur-0.5 不动）、边际收益=0 定单量、异常回退基线
# 语义、非触发拍零足迹（影子基线并行决策台账）、零跨拍挪量、磁带零触碰。
_EXPX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
_EXPX_K = __EXPX_K__
_EXPX_WIN_END = __EXPX_WIN_END__
_EXPX_TERM = __EXPX_TERM__
_EXPX_MAX_BATCH = 40
_EXPX_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_EXPX_STATE = {}
_EXPX_DEC = {}
_EXPX_REPORT = {
    "calls": 0, "fires": 0, "holds": 0, "units": 0, "base_fires": 0,
    "mr_limited": 0, "cap_limited": 0, "censored_lo": 0, "errors": 0,
    "post_win_base": 0, "stranding_insured": 0,
    "decision_diff_steps": [],
}


def _expx_reset():
    _EXPX_STATE.clear()
    _EXPX_DEC.clear()
    _EXPX_REPORT.update(
        calls=0, fires=0, holds=0, units=0, base_fires=0, mr_limited=0,
        cap_limited=0, censored_lo=0, errors=0, post_win_base=0,
        stranding_insured=0)
    _EXPX_REPORT["decision_diff_steps"] = []


def _expx_diff(step):
    lst = _EXPX_REPORT["decision_diff_steps"]
    if step not in lst and len(lst) < 400:
        lst.append(int(step))
        lst.sort()


def _expx_price(item, inv, params):
    return float(_r37_market_price(item, int(inv), params))


def _expx_params(observation):
    try:
        params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
        for k, patch in (((observation or {}).get("market") or {})
                         .get("params") or {}).items():
            if k in params and isinstance(patch, dict):
                params[k].update(patch)
        return params
    except Exception:
        return None


def _expx_draw(item, step, shops):
    d = 0
    if step % 4 == 0:
        for s in shops or ():
            prods = _EXPX_SHOPS.get(s) or ()
            if item in prods:
                d += 2 if len(prods) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        d += 1
    return d


def _expx_rival(player, item):
    hist = (_EXPX_STATE.get(player) or {}).get("hist", {}).get(item) or []
    if not hist:
        return 0.0
    tail = hist[-4:]
    return max(0.0, sum(tail) / len(tail))


def _expx_update(observation, step):
    player = int((observation or {}).get("player", 0))
    market = (observation or {}).get("market") or {}
    inv_all = market.get("inventory") or {}
    prices = market.get("prices") or {}
    shops = ((observation or {}).get("town") or {}).get("unlocked_shops") or []
    st = _EXPX_STATE.setdefault(player, {"hist": {}})
    inv_now = {i: int(inv_all.get(i, 0)) for i in _EXPX_ITEMS}
    prev = st.get("inv_prev")
    own_prev = st.get("own_prev") or {}
    if prev is not None and st.get("step_prev") == step - 1:
        for i in _EXPX_ITEMS:
            slot = own_prev.get(i) or {}
            d = (inv_now[i] - int(prev.get(i, 0))
                 + _expx_draw(i, step - 1, shops) - int(slot.get("vis", 0)))
            hist = st["hist"].setdefault(i, [])
            hist.append(max(0, d))
            if len(hist) > 12:
                del hist[:6]
            if int(slot.get("floor", 0)) > 0 or int(prices.get(i, 0)) <= 1:
                _EXPX_REPORT["censored_lo"] += 1
    st["inv_prev"] = inv_now
    st["step_prev"] = step
    st["shops"] = shops


def _expx_note_own(observation, action):
    player = int((observation or {}).get("player", 0))
    prices = ((observation or {}).get("market") or {}).get("prices") or {}
    own = {}
    for o in (action or {}).get("market") or []:
        if not (isinstance(o, (list, tuple)) and len(o) >= 3
                and o[0] == "SELL" and str(o[1]) in _EXPX_ITEMS):
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
    st = _EXPX_STATE.setdefault(player, {"hist": {}})
    st["own_prev"] = own


def _expx_traj(item, step, inv, rival, shops, params, horizon=None):
    """K 拍（或指定 horizon 拍）inv 轨迹（报价基准同 v1）。"""
    k = int(horizon or _EXPX_K)
    cur = float(inv)
    traj = []
    for t in range(1, k + 1):
        cur = cur + rival - _expx_draw(item, step + t - 1, shops)
        traj.append(max(0.0, cur))
    return traj


def _expx_pnext(item, step, inv, rival_avg, avail, p_now, planned, observation):
    """替换 MODELPX 预测核：K 拍轨迹峰值价；胜位守卫①窗收缩后回退基线。"""
    try:
        p_cur = _expx_price(item, inv, None)
        inv_next = inv + rival_avg + planned - _s758_draw_units(item, step)
        p_next_base = _expx_price(item, max(0, int(inv_next)), None)
        fire_base = p_next_base < p_cur - 0.5
    except Exception:
        fire_base = False
        p_next_base = 1e18
        p_cur = 1e18
    try:
        _EXPX_REPORT["calls"] += 1
        if fire_base:
            _EXPX_REPORT["base_fires"] += 1
        if int(step) >= _EXPX_WIN_END:
            # ① 窗收缩：648 后全基线语义（fire_x=fire_base→零足迹）
            _EXPX_REPORT["post_win_base"] += 1
            _EXPX_DEC[(int(step), str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "traj": None, "rival": 0.0}
            return float(p_next_base)
        params = _expx_params(observation)
        player = int((observation or {}).get("player", 0))
        st = _EXPX_STATE.get(player) or {}
        shops = st.get("shops") or []
        rival = _expx_rival(player, item)
        traj = _expx_traj(item, step, inv, rival, shops, params)
        p_next_x = max(_expx_price(item, x, params) for x in traj)
        fire_x = p_next_x < p_cur - 0.5
        _EXPX_DEC[(int(step), str(item))] = {
            "p_cur": p_cur, "fire_base": bool(fire_base),
            "fire_x": bool(fire_x), "traj": traj, "rival": rival,
            "shops": shops}
        if bool(fire_base) != bool(fire_x):
            _expx_diff(step)
        if fire_x:
            _EXPX_REPORT["fires"] += 1
        else:
            _EXPX_REPORT["holds"] += 1
        return float(p_next_x)
    except Exception:
        _EXPX_REPORT["errors"] += 1
        try:
            _EXPX_DEC[(int(step), str(item))] = {
                "p_cur": p_cur, "fire_base": bool(fire_base),
                "fire_x": bool(fire_base), "traj": None, "rival": 0.0}
        except Exception:
            pass
        return float(p_next_base)


def _expx_take(item, step, inv, p_now, cap, avail, observation):
    """边际收益定单量（v1 同式）+ 胜位守卫②滞留保险。"""
    dec = _EXPX_DEC.get((int(step), str(item))) or {}
    fire_base = bool(dec.get("fire_base"))
    base_posted = min(int(avail), int(cap)) if fire_base else 0
    q = 0
    insured = False
    try:
        if int(step) >= _EXPX_WIN_END:
            q = int(cap)  # ① 窗收缩：基线语义量帽
            _EXPX_REPORT["post_win_base"] += 1
        else:
            traj = dec.get("traj")
            if not traj:
                raise ValueError("no_traj")
            params = _expx_params(observation)
            shift = 0
            while q < int(cap) and q < _EXPX_MAX_BATCH:
                now_px = _expx_price(item, inv + shift, params)
                v_hold = max(_expx_price(item, x + shift, params) for x in traj)
                if now_px <= v_hold:
                    break
                q += 1
                if now_px > 1:
                    shift += 1
            # ② 滞留保险：MR 持有（q<min(avail,cap)）且模型窗内峰值容量
            # 清不掉该件投射仓存量 → 立即按基线语义出货
            if q < min(int(avail), int(cap)):
                player = int((observation or {}).get("player", 0))
                st = _EXPX_STATE.get(player) or {}
                shops = dec.get("shops") or st.get("shops") or []
                rival = float(dec.get("rival") or 0.0)
                until = _EXPX_WIN_END
                stock = int(avail)
                if int(step) >= until - 1:
                    leftover = stock
                else:
                    traj2 = _expx_traj(item, step, inv, rival, shops, params,
                                       horizon=until - 1 - int(step))
                    quotes = [_expx_price(item, x, params) for x in traj2]
                    leftover = stock
                    for i2 in range(len(quotes)):
                        if leftover <= 0:
                            break
                        fwd = quotes[i2 + 1:i2 + 1 + _EXPX_K]
                        is_peak = (not fwd) or (
                            quotes[i2] >= max(fwd) - 0.5)
                        if is_peak:
                            leftover -= min(int(cap), leftover)
                if leftover > 0:
                    q = int(cap)
                    insured = True
                    _EXPX_REPORT["stranding_insured"] += 1
            if not insured:
                if q >= int(cap):
                    _EXPX_REPORT["cap_limited"] += 1
                else:
                    _EXPX_REPORT["mr_limited"] += 1
    except Exception:
        _EXPX_REPORT["errors"] += 1
        q = int(cap)  # 异常回退基线量帽
    x_posted = min(int(avail), q)
    if x_posted != base_posted:
        _expx_diff(step)
    if x_posted > 0:
        _EXPX_REPORT["units"] += x_posted
    return q
