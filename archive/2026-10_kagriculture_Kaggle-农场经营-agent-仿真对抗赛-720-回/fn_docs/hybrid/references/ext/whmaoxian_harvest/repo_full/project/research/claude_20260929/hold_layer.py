
# ---------------------------------------------------------------------------
# HOLD layer (2026-09-29): price-aware premium selling on top of the parent agent.
# The parent's farm actions and non-SELL market orders are untouched. Once cash is
# comfortable, SELL orders for managed products are replaced by a policy that sells
# right after town drains, holds units while the market is expected to recover,
# front-runs (index 0) when the market is drifting into a glut, keeps shed room for
# the night drop and liquidates gradually at the end.
import math as _h_math

_H_PARENT = agent
_H_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON", "TOMATO", "CARROT", "EGG")
_H_ALL = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
_H_SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_H_PARAMS = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20), "CARROT": (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO": (60, 200, "hinge", 0.40, "sqrt", 0.60), "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60), "EGG": (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60), "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
_H_CFG = dict(start_day=10, min_money=2500, theta=0.92, horizon=24, ema=0.08,
              cap=100, margin=4, end_window=30, first=True, enabled=True)
_H_STATE = {}


def _h_shape(f, x, T):
    x = max(0.0, x)
    if f == "linear": return x
    if f == "sq": return x * x
    if f == "sqrt": return _h_math.sqrt(x)
    if f == "log": return _h_math.log(1.0 + x)
    if f == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _h_price(item, inv):
    base, T, bf, bt, af, at = _H_PARAMS[item]
    if inv < 10000:
        p = base + bt * base / _h_shape(bf, T, T) * _h_shape(bf, 10000 - inv, T)
    else:
        p = base - at * base / _h_shape(af, T, T) * _h_shape(af, inv - 10000, T)
    return max(1, int(round(p)))


def _h_drain(shops, item):
    d = 1.0 / 24.0 if item != "FERTILIZER" else 0.0
    for s in shops:
        prods = _H_SHOPS.get(s, ())
        if item in prods:
            d += (2.0 if len(prods) == 1 else 1.0) / 4.0
    return d


def _h_projected(obs, action, seat):
    """Shed contents after this turn's unit actions (DROP / PLACE-to-shed)."""
    priv = obs["private"]
    shed = {k: int(v) for k, v in (priv.get("shed") or {}).items() if v}
    invs = priv.get("inventories") or []
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    acts = [action.get("farmer")] + list(action.get("hands") or [])
    adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
    for i, act in enumerate(acts):
        if i >= len(units) or i >= len(invs) or not isinstance(act, list) or not act:
            continue
        pos = tuple(units[i] or ())
        if pos not in adj:
            continue
        inv = invs[i] or {}
        if act[0] == "DROP":
            for k, v in inv.items():
                if v:
                    shed[k] = shed.get(k, 0) + int(v)
        elif act[0] == "PLACE" and len(act) >= 2 and act[1] in inv:
            n = int(act[2]) if len(act) >= 3 else 1
            shed[act[1]] = shed.get(act[1], 0) + min(n, int(inv.get(act[1], 0)))
        elif act[0] == "PICKUP" and len(act) >= 2:
            n = int(act[2]) if len(act) >= 3 else 1
            shed[act[1]] = max(0, shed.get(act[1], 0) - n)
    carried = 0
    for i, inv in enumerate(invs):
        act = acts[i] if i < len(acts) else None
        if isinstance(act, list) and act and act[0] == "DROP" and i < len(units) and tuple(units[i] or ()) in adj:
            continue
        carried += sum(int(v) for v in (inv or {}).values())
    return shed, carried


def _h_layer(obs, action):
    cfg = _H_CFG
    step = int(obs.get("step", 0) or 0)
    seat = int(obs.get("player", 0) or 0)
    st = _H_STATE.get(seat)
    if st is None or step == 0 or step <= st.get("last", -1):
        st = {"last": -1, "inv": None, "drift": {}}
        _H_STATE[seat] = st
    market = obs.get("market") or {}
    inv = {k: int(v) for k, v in (market.get("inventory") or {}).items()}
    # drift EMA of inventory change per step, net of known town drain
    shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
    if st["inv"] is not None and st["last"] == step - 1:
        for it in _H_ITEMS:
            if it in inv and it in st["inv"]:
                delta = inv[it] - st["inv"][it]
                # add back the drain that happened (drain is included in delta)
                dr = 0.0
                if (step - 1) % 4 == 0:
                    dr += (_h_drain(shops, it) - 1.0 / 24.0) * 4.0
                if (step - 1) % 24 == 0:
                    dr += 1.0
                sales = delta + dr
                old = st["drift"].get(it, 0.0)
                st["drift"][it] = old + cfg["ema"] * (max(0.0, sales) - old)
    st["inv"] = dict(inv)
    st["last"] = step
    if not cfg["enabled"] or not isinstance(action, dict):
        return action
    day = step // 24
    farm = obs["farms"][seat]
    money = float(farm.get("money", 0))
    if day < cfg["start_day"] or money < cfg["min_money"] or step >= 719:
        return action
    orders = [o for o in (action.get("market") or []) if isinstance(o, list) and o]
    keep = [o for o in orders if not (o[0] == "SELL" and len(o) >= 2 and o[1] in _H_ITEMS)]
    shed, carried = _h_projected(obs, action, seat)
    # the parent's other sells (wheat/fertilizer) reduce the shed
    for o in keep:
        if o[0] == "SELL" and len(o) >= 3:
            shed[o[1]] = max(0, shed.get(o[1], 0) - int(o[2]))
    remaining = 719 - step
    last = step >= 718
    sells = {}
    for it in _H_ITEMS:
        s = shed.get(it, 0)
        if s <= 0:
            continue
        cur = inv.get(it, 10000)
        if last:
            sells[it] = s
            continue
        drain = _h_drain(shops, it)
        supply = st["drift"].get(it, 0.0)
        H = min(cfg["horizon"], remaining)
        ref = _h_price(it, cur + (supply - drain) * H)
        thr = cfg["theta"] * ref
        if remaining <= cfg["end_window"]:
            # spread liquidation over the remaining drain ticks
            ticks = max(1, remaining // 4)
            quota = int(_h_math.ceil(s / float(ticks)))
            thr = 0
        else:
            quota = s
        k = 0
        while k < min(s, quota) and _h_price(it, cur + k) >= thr:
            k += 1
        if k:
            sells[it] = k
    # shed room valve: keep room for tonight's drop of carried goods
    total_after = sum(shed.values()) - sum(sells.values())
    need = total_after + carried + cfg["margin"] - cfg["cap"]
    if need > 0:
        cands = sorted((it for it in _H_ITEMS if shed.get(it, 0) - sells.get(it, 0) > 0),
                       key=lambda it: -_h_price(it, inv.get(it, 10000) + sells.get(it, 0)))
        for it in cands:
            if need <= 0:
                break
            extra = min(need, shed.get(it, 0) - sells.get(it, 0))
            sells[it] = sells.get(it, 0) + extra
            need -= extra
    ours = [["SELL", it, n] for it, n in sorted(sells.items(), key=lambda x: -_h_price(x[0], inv.get(x[0], 10000))) if n > 0]
    new = (ours + keep) if cfg["first"] else (keep + ours)
    if len(new) > 10:
        # never drop the parent's non-sell orders
        nonsell = [o for o in keep if o[0] != "SELL"]
        new = (ours + [o for o in keep if o[0] == "SELL"])[: max(0, 10 - len(nonsell))] + nonsell if cfg["first"] else new[:10]
    action = dict(action)
    action["market"] = new
    return action


def hold_agent(observation, configuration=None):
    action = _H_PARENT(observation, configuration)
    try:
        return _h_layer(observation, action)
    except Exception:
        return action


agent = hold_agent
kaggle_hold_submission_agent = hold_agent
