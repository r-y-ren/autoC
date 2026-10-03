
# ---------------------------------------------------------------------------
# LOW-WHEAT layer (2026-09-30): when wheat is cheap, keep (and optionally buy) a feed
# stock in the shed instead of selling it; the parent's wheat supply logic buys only
# the shortage beyond shed stock, so later (dearer) purchases shrink.
_LWX_PARENT = kaggle_hpx2_final_agent
_LWX_CFG = dict(low=32, stock=30, buy=False, first_step=144, last_step=640, room=12)
_LWX_REPORT = {"kept": 0, "bought": 0}


def _lwx_apply(obs, action):
    cfg = _LWX_CFG
    if not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    if step < cfg["first_step"] or step > cfg["last_step"] or step % 24 >= 21:
        return action
    prices = (obs.get("market") or {}).get("prices") or {}
    px = int(prices.get("WHEAT", 99))
    if px > cfg["low"]:
        return action
    seat = int(obs.get("player", 0) or 0)
    priv = obs.get("private") or {}
    shed = dict(priv.get("shed") or {})
    invs = priv.get("inventories") or []
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    cmds = [action.get("farmer")] + list(action.get("hands") or [])
    adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
    for i, c in enumerate(cmds):
        if not (isinstance(c, list) and c) or i >= len(units):
            continue
        pos = tuple(units[i] or ())
        if c[0] == "PICKUP" and len(c) >= 2 and pos in adj:
            n = int(c[2]) if len(c) >= 3 else 1
            shed[c[1]] = max(0, shed.get(c[1], 0) - n)
        elif c[0] == "DROP" and pos in adj and i < len(invs):
            for k, v in (invs[i] or {}).items():
                shed[k] = shed.get(k, 0) + v
    carried = sum(sum(int(v) for v in (inv or {}).values()) for inv in invs)
    market = [list(o) for o in (action.get("market") or []) if isinstance(o, list) and o]
    sold = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["SELL", "WHEAT"])
    bought = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["BUY_PRODUCT", "WHEAT"])
    held = shed.get("WHEAT", 0) - sold + bought
    want = cfg["stock"] - held
    if want <= 0:
        return action
    total = sum(v for v in shed.values()) - sold + bought + carried
    room = 100 - cfg["room"] - total
    changed = False
    # 1) keep: shrink this turn's wheat sales (latest orders first)
    for o in reversed(market):
        if want <= 0 or room <= 0:
            break
        if len(o) >= 3 and o[:2] == ["SELL", "WHEAT"] and int(o[2]) > 0:
            k = min(int(o[2]), want, room)
            o[2] = int(o[2]) - k
            want -= k; room -= k
            _LWX_REPORT["kept"] += k
            changed = True
    market = [o for o in market if not (len(o) >= 3 and o[0] == "SELL" and int(o[2]) <= 0)]
    # 2) optionally buy up to the stock target
    if cfg["buy"] and want > 0 and room > 0 and len(market) < 10:
        k = min(want, room)
        if float(farm.get("money", 0)) > 1500 + k * (px + 3):
            market.append(["BUY_PRODUCT", "WHEAT", k])
            _LWX_REPORT["bought"] += k
            changed = True
    if not changed:
        return action
    action = dict(action)
    action["market"] = market
    return action


def lwx_agent(observation, configuration=None):
    action = _LWX_PARENT(observation, configuration)
    try:
        return _lwx_apply(observation, action)
    except Exception:
        return action
