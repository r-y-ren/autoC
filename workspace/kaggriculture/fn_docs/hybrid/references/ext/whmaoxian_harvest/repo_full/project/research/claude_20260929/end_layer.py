
# ---------------------------------------------------------------------------
# END layer (2026-09-29): from the afternoon of day 28 on, feed wheat and fertilizer
# have no further use (production and care bonuses after that point pay out only after
# the season ends), so sell the shed's wheat and fertilizer instead of carrying them
# into an overflowing night drop.  Parent unit actions are unchanged.
_ENDX_PARENT = kaggle_submission_agent
_ENDX_CFG = dict(enabled=True, day=28, hour=12, items=("WHEAT", "FERTILIZER"), keep=0)
_ENDX_REPORT = {"orders": 0}


def endx_agent(observation, configuration=None):
    action = _ENDX_PARENT(observation, configuration)
    try:
        return _endx_apply(observation, action)
    except Exception:
        return action


def _endx_apply(obs, action):
    cfg = _ENDX_CFG
    if not cfg["enabled"] or not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    day, hour = step // 24, step % 24
    if day < cfg["day"] or (day == cfg["day"] and hour < cfg["hour"]):
        return action
    seat = int(obs.get("player", 0) or 0)
    shed = dict((obs.get("private") or {}).get("shed") or {})
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    cmds = [action.get("farmer")] + list(action.get("hands") or [])
    invs = (obs.get("private") or {}).get("inventories") or []
    adj = {(4, 4), (5, 4), (4, 5), (5, 5)}
    # account for this turn's pickups / drops
    for i, c in enumerate(cmds):
        if not (isinstance(c, list) and c) or i >= len(units):
            continue
        if c[0] == "PICKUP" and len(c) >= 2:
            n = int(c[2]) if len(c) >= 3 else 1
            shed[c[1]] = max(0, shed.get(c[1], 0) - n)
        elif c[0] == "DROP" and tuple(units[i] or ()) in adj and i < len(invs):
            for k, v in (invs[i] or {}).items():
                shed[k] = shed.get(k, 0) + v
    market = [list(o) for o in (action.get("market") or []) if isinstance(o, list) and o]
    planned = {}
    for o in market:
        if o[0] == "SELL" and len(o) >= 3:
            planned[o[1]] = planned.get(o[1], 0) + int(o[2])
    extra = []
    for it in cfg["items"]:
        q = shed.get(it, 0) - planned.get(it, 0) - cfg["keep"]
        if q > 0:
            extra.append(["SELL", it, q])
    if not extra or len(market) >= 10:
        return action
    action = dict(action)
    action["market"] = (market + extra)[:10]
    _ENDX_REPORT["orders"] += len(extra)
    return action


endx_agent.telemetry = _ENDX_REPORT
kaggle_endx_submission_agent = endx_agent
