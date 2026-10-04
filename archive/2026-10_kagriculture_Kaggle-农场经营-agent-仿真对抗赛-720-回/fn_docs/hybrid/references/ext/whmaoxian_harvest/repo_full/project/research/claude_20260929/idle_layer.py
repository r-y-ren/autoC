
# ---------------------------------------------------------------------------
# IDLE-FILL layer (2026-09-29): when a parent unit would PASS, perform a harmless
# in-place action on the tile it already stands on (CARE, COLLECT_FERTILIZER or
# WATER). No unit moves, so the parent schedule's positions are preserved; the
# parent's own later action on that tile simply becomes a no-op.
_IDF_PARENT = kaggle_submission_agent
_IDF_CFG = dict(enabled=True, care=True, collect=True, water=True, last_step=716)
_IDF_REPORT = {"CARE": 0, "COLLECT_FERTILIZER": 0, "WATER": 0}


def idle_fill_agent(observation, configuration=None):
    action = _IDF_PARENT(observation, configuration)
    try:
        return _idf_apply(observation, action)
    except Exception:
        return action


def _idf_apply(obs, action):
    cfg = _IDF_CFG
    if not cfg["enabled"] or not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    if step > cfg["last_step"]:
        return action
    seat = int(obs.get("player", 0) or 0)
    farm = obs["farms"][seat]
    units = [farm.get("farmer")] + list(farm.get("hands") or [])
    cmds = [action.get("farmer")] + list(action.get("hands") or [])
    changed = False
    touched = set()
    for i, c in enumerate(cmds):
        if i >= len(units) or not (isinstance(c, list) and c and c[0] == "PASS"):
            continue
        x, y = units[i]
        if (x, y) in touched:
            continue
        t = farm["tiles"][y][x]
        new = None
        if isinstance(t, dict) and t.get("animal"):
            if cfg["care"] and not t.get("cared_today"):
                new = ["CARE"]
            elif cfg["collect"] and t.get("fertilizer_available"):
                new = ["COLLECT_FERTILIZER"]
        elif isinstance(t, dict) and t.get("kind") == "PLANT":
            if cfg["water"] and not t.get("watered_today"):
                new = ["WATER"]
        if new:
            cmds[i] = new
            touched.add((x, y))
            _IDF_REPORT[new[0]] += 1
            changed = True
    if not changed:
        return action
    action = dict(action)
    action["farmer"] = cmds[0]
    action["hands"] = cmds[1:]
    return action


idle_fill_agent.telemetry = _IDF_REPORT
kaggle_idle_fill_submission_agent = idle_fill_agent
