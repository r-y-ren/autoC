# ---- 件 EXPX：MODELPX 预测核精确化（引擎公式最优执行） ----------------
# 形态：内层改造 + 尾块注入件（build_expx 把本块拼进 oc_c3 提交源尾部，与宿主
# 同命名空间；块首捕获 _EXPX_HOST=oc_c3 件 _hs_agent，块尾末函数=_expx_agent）。
# 替换点=MODELPX 的 p_next 计算（基座 4 处同文替换）：启发式一步预报
#   inv_next=inv+rival_avg+planned-draw; p_next=price(inv_next)
# 换成精确投影核 _expx_pnext（K=__EXPX_K__ 拍价格轨迹峰值）；量帽表达式换
# _expx_take（边际收益定单量）。仅用基座裸名（_r37_market_price/
# _R37_MARKET_PARAMS/_s758_draw_units，影子基线口径用）；stdlib-only。
#
# 模型三件（任务 expx 口径）：
# 1) 精确价格投影：price(inv)=max(1,round(base±amp×shape(|inv-I0|,T)))（引擎
#    公式全表，_r37 同式）；inv 轨迹=对手流估计+城镇排水表（每 4 步每店每品
#    1 件、单品店 ×2；24 步中心全品 1 件），逐拍 inv_{t+1}=inv_t+rival-draw；
# 2) 最优出货点：轨迹局部峰值拍出货——门沿基座 p_next<p_cur-0.5，p_next 语义
#    改为 K 拍轨迹峰值价（峰值拍=未来 K 拍都拿不到更好价 → 现在卖）；
# 3) 边际收益定单量：吸收曲线=排水累计吸收；自家出货边际冲击=已卖 shift 件
#    对轨迹的平移（价>1 才进库存）；逐件比较 即时报价 price(inv+shift) 与
#    持有值 V=max_t price(inv_t+shift)，卖到边际收益=0（≤V 即停），预卖帽沿
#    基线（基座量帽表达式为上限）——避开自砸谷底（膝点教训的模型化正解）。
#
# 对手流估计（R28 删失口径）：rival_sold=inv'-inv+town_draw-own_sold($1 地板
# 件不计进库存→可见量)；$1 地板活动记下界（censored_lo 台账）。逐拍由入口
# 更新（跨 MODELPX 空窗不断档），尾 4 拍均值。
#
# 足迹（轨道 2 范式）：影子基线决策并行计算（同 rival_avg/planned/粗 draw/
# 基座量帽），与精确决策不一致才记 decision_diff_step；非触发拍零足迹
# （决策一致→动作流逐字节同）。异常回退基线语义。零跨拍挪量、磁带 blob
# 零触碰、只挂卖自己投射仓存量（宿主守卫沿用）。
_EXPX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
_EXPX_K = __EXPX_K__
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
    "decision_diff_steps": [],
}


def _expx_reset():
    _EXPX_STATE.clear()
    _EXPX_DEC.clear()
    _EXPX_REPORT.update(calls=0, fires=0, holds=0, units=0, base_fires=0,
                        mr_limited=0, cap_limited=0, censored_lo=0, errors=0)
    _EXPX_REPORT["decision_diff_steps"] = []


def _expx_diff(step):
    lst = _EXPX_REPORT["decision_diff_steps"]
    if step not in lst and len(lst) < 400:
        lst.append(int(step))
        lst.sort()


def _expx_price(item, inv, params):
    """引擎公式价（含 $1 地板；params=None 走基座默认表）。"""
    return float(_r37_market_price(item, int(inv), params))


def _expx_params(observation):
    """market.params 稀疏覆盖合并（_r37_quote_priority 同式）；异常→默认表。"""
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
    """城镇排水精确表：每 4 步每店每品 1 件（单品店 ×2）+ 24 步中心全品 1。"""
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
    """逐拍对手流估计滚动（入口在宿主调用前执行；跨空窗不断档）。"""
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
    """本拍我方 SELL 可见量入账（quote>1 记可见；$1 地板记下界件）。"""
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


def _expx_traj(item, step, inv, rival, shops, params):
    """K 拍 inv 轨迹（报价基准：step+t 拍报价=step+t-1 处理后 inv）。"""
    cur = float(inv)
    traj = []
    for t in range(1, _EXPX_K + 1):
        cur = cur + rival - _expx_draw(item, step + t - 1, shops)
        traj.append(max(0.0, cur))
    return traj


def _expx_pnext(item, step, inv, rival_avg, avail, p_now, planned, observation):
    """替换 MODELPX 预测核：返回 K 拍轨迹峰值价（精确投影）。

    影子基线（基座同式）并行算出 fire_base 供足迹审计；异常回退基线语义。
    """
    try:
        p_cur = _expx_price(item, inv, None)
        inv_next = inv + rival_avg + planned - _s758_draw_units(item, step)
        p_next_base = _expx_price(item, max(0, int(inv_next)), None)
        fire_base = p_next_base < p_cur - 0.5
    except Exception:
        fire_base = False
        p_next_base = 1e18
    try:
        _EXPX_REPORT["calls"] += 1
        if fire_base:
            _EXPX_REPORT["base_fires"] += 1
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
            "fire_x": bool(fire_x), "traj": traj, "rival": rival}
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
    """边际收益定单量：卖到 MR=price(inv+shift)-V_hold <= 0 为止；帽沿基线。

    V_hold=max_t price(inv_t+shift)（自家 shift 件冲击平移后的轨迹峰值=吸收
    曲线口径持有值）。返回 q（宿主外层 min(avail,·)）；异常回退基线量帽。
    """
    dec = _EXPX_DEC.get((int(step), str(item))) or {}
    fire_base = bool(dec.get("fire_base"))
    base_posted = min(int(avail), int(cap)) if fire_base else 0
    q = 0
    try:
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
        if q >= int(cap):
            _EXPX_REPORT["cap_limited"] += 1
        else:
            _EXPX_REPORT["mr_limited"] += 1
    except Exception:
        _EXPX_REPORT["errors"] += 1
        q = int(cap)  # 异常回退基线量帽（行为=基座）
    x_posted = min(int(avail), q)
    if x_posted != base_posted:
        _expx_diff(step)
    if x_posted > 0:
        _EXPX_REPORT["units"] += x_posted
    return q
