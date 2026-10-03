
# ---------------------------------------------------------------------------
# ORDER layer (2026-09-29): reorder this turn's market orders.  Quantities are
# unchanged; only the processing index of SELL orders moves.
_ORDX_PARENT = endx_agent
_ORDX_CFG = dict(mode="value_desc", prio=("MILK", "WOOL", "STRAWBERRY", "MELON", "TOMATO", "EGG", "CARROT", "WHEAT", "FERTILIZER"), sells_first=True)


def _ordx_apply(obs, action):
    cfg = _ORDX_CFG
    if not isinstance(action, dict):
        return action
    market = [o for o in (action.get("market") or []) if isinstance(o, list) and o]
    sells = [o for o in market if o[0] == "SELL" and len(o) >= 3]
    if len(sells) < 2 and not cfg["sells_first"]:
        return action
    others = [o for o in market if not (o[0] == "SELL" and len(o) >= 3)]
    prices = (obs.get("market") or {}).get("prices") or {}
    mode = cfg["mode"]
    if mode == "value_desc":
        sells.sort(key=lambda o: -float(prices.get(o[1], 0)) * int(o[2]))
    elif mode == "value_asc":
        sells.sort(key=lambda o: float(prices.get(o[1], 0)) * int(o[2]))
    elif mode == "price_desc":
        sells.sort(key=lambda o: -float(prices.get(o[1], 0)))
    elif mode == "prio":
        pr = {k: i for i, k in enumerate(cfg["prio"])}
        sells.sort(key=lambda o: pr.get(o[1], 99))
    elif mode == "qty_asc":
        sells.sort(key=lambda o: int(o[2]))
    elif mode == "keep":
        pass
    elif mode in ("impact", "impact_asc"):
        inv = (obs.get("market") or {}).get("inventory") or {}
        def imp(o):
            it, q = o[1], int(o[2])
            p0 = float(prices.get(it, 0))
            try:
                p1 = _h_price_ordx(it, int(inv.get(it, 10000)) + q)
            except Exception:
                p1 = p0
            return q * max(0.0, p0 - p1)
        sells.sort(key=imp, reverse=(mode == "impact"))
    if cfg["sells_first"]:
        # keep HIRE / BUY_LAND ahead so money-sensitive atomic orders are unchanged
        atom = [o for o in others if o[0] in ("HIRE", "BUY_LAND")]
        rest = [o for o in others if o[0] not in ("HIRE", "BUY_LAND")]
        new = sells + atom + rest if False else atom[:0] + sells + others
    else:
        new = []
        it = iter(sells)
        for o in market:
            new.append(next(it) if (o[0] == "SELL" and len(o) >= 3) else o)
    if new == market:
        return action
    action = dict(action)
    action["market"] = new
    return action


_ORDX_PARAMS = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20), "CARROT": (35, 450, "hinge", 1.00, "sqrt", 0.70),
    "TOMATO": (60, 200, "hinge", 0.40, "sqrt", 0.60), "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60), "EGG": (50, 332, "hinge", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60), "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}


def _ordx_shape(f, x, T):
    import math
    x = max(0.0, x)
    if f == "linear": return x
    if f == "sq": return x * x
    if f == "sqrt": return math.sqrt(x)
    if f == "log": return math.log(1.0 + x)
    if f == "hinge":
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _h_price_ordx(item, inv):
    base, T, bf, bt, af, at = _ORDX_PARAMS[item]
    if inv < 10000:
        p = base + bt * base / _ordx_shape(bf, T, T) * _ordx_shape(bf, 10000 - inv, T)
    else:
        p = base - at * base / _ordx_shape(af, T, T) * _ordx_shape(af, inv - 10000, T)
    return max(1, int(round(p)))


def ordx_agent(observation, configuration=None):
    action = _ORDX_PARENT(observation, configuration)
    try:
        return _ordx_apply(observation, action)
    except Exception:
        return action


kaggle_ordx_submission_agent = ordx_agent
