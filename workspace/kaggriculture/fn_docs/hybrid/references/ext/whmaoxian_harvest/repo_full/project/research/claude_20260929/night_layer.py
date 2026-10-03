
# ---------------------------------------------------------------------------
# NIGHT layer (2026-09-29): in the last hours of each day, if tonight's automatic drop
# (all carried goods) would overflow the 100-item shed, sell cheap shed stock first so
# the valuable carried harvest is kept.  Parent unit actions are unchanged.
_NGTX_PARENT = kaggle_submission_agent
_NGTX_CFG = dict(enabled=True, hours=(22, 23), cap=100, margin=0, order=("FERTILIZER", "WHEAT", "EGG", "CARROT", "TOMATO", "MILK", "WOOL", "STRAWBERRY", "MELON"))
_NGTX_REPORT = {"units": 0}


def ngtx_agent(observation, configuration=None):
    action = _NGTX_PARENT(observation, configuration)
    try:
        return _ngtx_apply(observation, action)
    except Exception:
        return action


def _ngtx_apply(obs, action):
    cfg = _NGTX_CFG
    if not cfg["enabled"] or not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    if step % 24 not in cfg["hours"] or step >= 718:
        return action
    seat = int(obs.get("player", 0) or 0)
    priv = obs.get("private") or {}
    shed = dict(priv.get("shed") or {})
    invs = [dict(i or {}) for i in (priv.get("inventories") or [])]
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    cmds = [action.get("farmer")] + list(action.get("hands") or [])
    adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
    for i, c in enumerate(cmds):
        if not (isinstance(c, list) and c) or i >= len(units) or i >= len(invs):
            continue
        pos = tuple(units[i] or ())
        if c[0] == "PICKUP" and len(c) >= 2 and pos in adj:
            n = min(int(c[2]) if len(c) >= 3 else 1, shed.get(c[1], 0))
            shed[c[1]] = shed.get(c[1], 0) - n
            invs[i][c[1]] = invs[i].get(c[1], 0) + n
        elif c[0] == "DROP" and pos in adj:
            for k, v in invs[i].items():
                shed[k] = shed.get(k, 0) + v
            invs[i] = {}
        elif c[0] == "PLACE" and len(c) >= 2 and pos in adj and c[1] in invs[i]:
            n = min(int(c[2]) if len(c) >= 3 else 1, invs[i].get(c[1], 0))
            shed[c[1]] = shed.get(c[1], 0) + n
            invs[i][c[1]] -= n
    market = [list(o) for o in (action.get("market") or []) if isinstance(o, list) and o]
    for o in market:
        if o[0] == "SELL" and len(o) >= 3:
            shed[o[1]] = max(0, shed.get(o[1], 0) - int(o[2]))
        elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
            shed[o[1]] = shed.get(o[1], 0) + int(o[2])
    carried = sum(sum(v for v in i.values()) for i in invs)
    over = sum(shed.values()) + carried - cfg["cap"] + cfg["margin"]
    if over <= 0:
        return action
    extra = []
    for it in cfg["order"]:
        if over <= 0:
            break
        q = min(over, shed.get(it, 0))
        if q > 0:
            extra.append(["SELL", it, q])
            over -= q
    if not extra or len(market) + len(extra) > 10:
        extra = extra[: max(0, 10 - len(market))]
    if not extra:
        return action
    action = dict(action)
    action["market"] = market + extra
    _NGTX_REPORT["units"] += sum(o[2] for o in extra)
    return action


ngtx_agent.telemetry = _NGTX_REPORT
kaggle_ngtx_submission_agent = ngtx_agent
