
# ---------------------------------------------------------------------------
# HIGH-PRICE release layer (2026-09-30): when WHEAT / FERTILIZER trade at a high
# price, sell the shed stock above a small reserve (the parent re-buys later when it
# needs feed / fertilizer, usually cheaper).  Parent unit actions are unchanged.
_HPX_PARENT = kaggle_cfg_final_agent
_HPX_CFG = dict(items={"WHEAT": (44, 0)}, first_day=0, last_step=717)
_HPX_REPORT = {"units": 0}


def _hpx_apply(obs, action):
    cfg = _HPX_CFG
    if not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    if step // 24 < cfg["first_day"] or step > cfg["last_step"]:
        return action
    seat = int(obs.get("player", 0) or 0)
    priv = obs.get("private") or {}
    shed = dict(priv.get("shed") or {})
    prices = (obs.get("market") or {}).get("prices") or {}
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    cmds = [action.get("farmer")] + list(action.get("hands") or [])
    invs = priv.get("inventories") or []
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
    market = [list(o) for o in (action.get("market") or []) if isinstance(o, list) and o]
    for o in market:
        if len(o) >= 3 and o[0] == "SELL":
            shed[o[1]] = shed.get(o[1], 0) - int(o[2])
        elif len(o) >= 3 and o[0] == "BUY_PRODUCT":
            # the parent wants this item now: do not sell it this turn
            shed[o[1]] = -10 ** 6
    extra = []
    for it, (thr, keep) in cfg["items"].items():
        if int(prices.get(it, 0)) < thr:
            continue
        q = shed.get(it, 0) - keep
        if q > 0:
            extra.append(["SELL", it, q])
    if not extra or len(market) + len(extra) > 10:
        return action
    action = dict(action)
    action["market"] = market + extra
    _HPX_REPORT["units"] += sum(o[2] for o in extra)
    return action


def hpx_agent(observation, configuration=None):
    action = _HPX_PARENT(observation, configuration)
    try:
        return _hpx_apply(observation, action)
    except Exception:
        return action


def kaggle_hpx_final_agent(observation, configuration=None):
    return hpx_agent(observation, configuration)
