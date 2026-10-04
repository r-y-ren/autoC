
# ---------------------------------------------------------------------------
# CARE layer (2026-09-29): a late-hired caretaker feeds and cares for animals the
# parent schedule skipped today, but only when the product price makes an extra
# fed+cared day worth more than a wheat ration plus the hire.  Parent actions for
# all other units are untouched; the caretaker is always the last hired hand.
_CRX_PARENT = kaggle_hold_submission_agent if "kaggle_hold_submission_agent" in globals() else kaggle_submission_agent
_CRX_CFG = dict(enabled=True, hire_hour=7, stop_hour=21, min_day=2, last_day=28,
               wool_min=90, milk_min=70, egg_min=999, max_hire_cost=400, min_targets=3, margin=40)
_CRX_STATE = {}
_CRX_PRODUCT = {"SHEEP": "WOOL", "COW": "MILK", "GOOSE": "EGG"}
_CRX_MIN = {"SHEEP": "wool_min", "COW": "milk_min", "GOOSE": "egg_min"}
_CRX_ADJ = ((4, 4), (5, 4), (4, 5), (5, 5))


def _crx_fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _crx_targets(obs, seat):
    farm = obs["farms"][seat]
    prices = obs["market"]["prices"]
    out = []
    for y in range(10):
        for x in range(10):
            t = farm["tiles"][y][x]
            if not (isinstance(t, dict) and t.get("animal")):
                continue
            a = t["animal"]
            if prices.get(_CRX_PRODUCT[a], 0) < _CRX_CFG[_CRX_MIN[a]]:
                continue
            if not t.get("fed_today") or not t.get("cared_today"):
                out.append(((x, y), not t.get("fed_today")))
    return out


def _crx_step(pos, tgt):
    x, y = pos
    tx, ty = tgt
    if x < tx: return ["EAST"]
    if x > tx: return ["WEST"]
    if y < ty: return ["SOUTH"]
    if y > ty: return ["NORTH"]
    return None


def care_agent(observation, configuration=None):
    action = _CRX_PARENT(observation, configuration)
    try:
        return _crx_layer(observation, action)
    except Exception:
        return action


def _crx_layer(obs, action):
    cfg = _CRX_CFG
    if not cfg["enabled"] or not isinstance(action, dict):
        return action
    step = int(obs.get("step", 0) or 0)
    seat = int(obs.get("player", 0) or 0)
    day, hour = step // 24, step % 24
    st = _CRX_STATE.get(seat)
    if st is None or step == 0 or step <= st.get("last", -1):
        st = {"last": -1, "day": -1, "idx": None, "requested": None, "report": {"hires": 0, "feeds": 0, "cares": 0}}
        _CRX_STATE[seat] = st
    st["last"] = step
    farm = obs["farms"][seat]
    hands = farm.get("hands") or []
    if st["day"] != day:
        st["day"] = day
        st["idx"] = None
        st["requested"] = None
    # confirm our hire from the previous step: the newest hand is ours
    if st["requested"] is not None and st["idx"] is None:
        req_step, before, parent_hires = st["requested"]
        if step == req_step + 1 and len(hands) >= before + parent_hires + 1:
            st["idx"] = before + parent_hires  # 0-based hand index of our caretaker
            st["report"]["hires"] += 1
        st["requested"] = None
    market = [o for o in (action.get("market") or []) if isinstance(o, list) and o]
    # ---- decide whether to hire
    if st["idx"] is None and st["requested"] is None and cfg["min_day"] <= day <= cfg["last_day"] \
            and cfg["hire_hour"] <= hour <= cfg["hire_hour"] + 2 and len(market) < 9:
        targets = _crx_targets(obs, seat)
        hungry = [t for t in targets if t[1]]
        parent_hires = sum(1 for o in market if o[0] == "HIRE")
        cost = _crx_fib(int(farm.get("hires_today", 0)) + parent_hires)
        wheat = obs["private"]["shed"].get("WHEAT", 0)
        need_wheat = max(0, len(hungry) - wheat)
        price_w = obs["market"]["prices"].get("WHEAT", 30) + 3
        spend = cost + need_wheat * price_w
        if len(targets) >= cfg["min_targets"] and cost <= cfg["max_hire_cost"] and farm["money"] > spend + 3000:
            extra = [["HIRE"]]
            if need_wheat:
                extra.append(["BUY_PRODUCT", "WHEAT", need_wheat])
            action = dict(action)
            action["market"] = market + extra
            st["requested"] = (step, len(hands), parent_hires)
        return action
    idx = st["idx"]
    if idx is None or idx >= len(hands):
        return action
    # ---- drive the caretaker
    pos = tuple(hands[idx])
    inv = (obs["private"].get("inventories") or [{}])[idx + 1] if len(obs["private"].get("inventories") or []) > idx + 1 else {}
    targets = _crx_targets(obs, seat)
    cmd = None
    home = min(_CRX_ADJ, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))
    hungry = [p for p, h in targets if h]
    if hour >= cfg["stop_hour"] or not targets:
        cargo = {k: v for k, v in inv.items() if v}
        if cargo and pos == home:
            cmd = ["DROP"]
        elif cargo:
            cmd = _crx_step(pos, home)
        else:
            cmd = ["PASS"]
    elif hungry and inv.get("WHEAT", 0) <= 0:
        if pos == home:
            k = min(len(hungry), obs["private"]["shed"].get("WHEAT", 0))
            cmd = ["PICKUP", "WHEAT", k] if k > 0 else ["PASS"]
        else:
            cmd = _crx_step(pos, home)
    else:
        doable = [(p, h) for p, h in targets if (not h) or inv.get("WHEAT", 0) > 0]
        if doable:
            p, h = min(doable, key=lambda v: abs(v[0][0] - pos[0]) + abs(v[0][1] - pos[1]))
            if p == pos:
                t = farm["tiles"][p[1]][p[0]]
                if not t.get("fed_today") and inv.get("WHEAT", 0) > 0:
                    cmd = ["FEED"]
                    st["report"]["feeds"] += 1
                elif not t.get("cared_today"):
                    cmd = ["CARE"]
                    st["report"]["cares"] += 1
                else:
                    cmd = ["PASS"]
            else:
                cmd = _crx_step(pos, p)
        else:
            cmd = ["PASS"]
    action = dict(action)
    hl = list(action.get("hands") or [])
    while len(hl) <= idx:
        hl.append(["PASS"])
    hl[idx] = cmd or ["PASS"]
    action["hands"] = hl
    return action


care_agent.telemetry = _CRX_STATE
kaggle_care_submission_agent = care_agent
