# ===== v48plus: hand-ported V50 economic layers on the v48 decoded source =====
# Base: references/data/intel-notebooks/v48build/main.py (sha256 dadee25a…),
# the byte-exact source of the running v48 public-derivative submission.  Every
# layer below is appended AFTER the base file; no base line is modified.
#
# Upstream sources (public notebooks, Apache-2.0, notices retained):
#   * V49 "kaggriculture-v49-funded-sale-timing-and-worker" (agent sha
#     ed89be8c…) carries the open economic layers of Thomas Tschinkel's
#     "The 2945 Farm" (v9/4): COURIER, CARROT/CARROT2, HERD, FERT, ORDERPRI2,
#     CAPHARV, SHEDROOM.
#   * V50 "kaggriculture-v50-early-yarn-commit" (agent sha 044a2660…) adds
#     weedlag (EXP338) and v233x (day-11 yarn commit + last-day skips).
# Ported here (subset chosen for substrate compatibility with this base):
#   * COURIER  — evening walk-and-drop of premium cargo with a same-day SELL.
#   * SHEDROOM — sell shed goods before the midnight auto-drop would discard
#     them at the shed capacity limit.
# Ported, measured, then removed (kept out of the shipping build):
#   * CAPHARV  — harvest-before-cap rescue.  On this base's six routes it never
#     found a swap candidate (the tapes already harvest animals before their
#     caps: 0 swaps across every tracked game, see
#     exports/probes/v48plus/v48plus_layer_ablation.json), so the layer was
#     dead code here and is left out of the build.
# Not ported, with reasons:
#   * weedlag (V50) — already carried by this base: scripts.v22_weed_repair
#     replays weed-blocked build/plant intents for the same bounded 8 steps.
#   * v233x day-11 yarn commit (V50) — no V233 substrate in this base: the
#     six-sheep V233 project, its per-day request/confirm state machine
#     (_v233_request/_v233_worker/_V233_STATES) and its day-12 expansion do not
#     exist here; this base's yarn routes already commit sheep on days 7-9 and
#     buy their second land on day 11 (step 265 of yarn_fast).  Accelerating a
#     tape expansion that does not exist would be a route rewrite, not an
#     economic layer, and upstream's +3,674 paired-margin claim is measured on
#     the V233 substrate only.
#   * CARROT/CARROT2/HERD/HERD2/COWSWAP/FERT/ORDERPRI2 (V49) — require the
#     upstream closed-loop chassis (_IMPL.chassis) or crop-yield simulation
#     hooks this base does not expose; porting them would rewrite validated
#     route behaviour rather than append layers.
# Engine facts this port relies on (verified in vendored kaggriculture.py):
#   * dawn reset: farmer respawns at the shed spawn, all hands are fired and
#     inventories auto-drop into the shed, so a courier detour cannot leak
#     position drift into later days;
#   * unit actions resolve before the market, so a DROP followed by a SELL in
#     the same action sells the dropped units the same step;
#   * the midnight auto-drop runs after the day's last market and discards
#     overflow above shed capacity;
#   * animal production on a fed night yields 1 + pending_care_bonus (one
#     bonus per cared+fed day), capped at the animal's max_held.
# All layers are pure functions of the observation plus per-seat state that
# resets on step 0 and on step rewind; every layer is individually guarded so
# a failure falls back to the unmodified base action.

from v19_terminal import MAX_ORDERS as _V48P_MAX_ORDERS
from v19_terminal import projected_shed as _v48p_projected_shed


def _v48p_standard(configuration):
    """True when the episode runs on the standard board the tapes assume."""
    if configuration is None or not isinstance(configuration, dict):
        return True
    for key, default in (
        ("boardSize", 10),
        ("turnsPerDay", 24),
        ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10),
    ):
        if key in configuration and configuration[key] != default:
            return False
    return True


def _v48p_access(board):
    half = board // 2
    return ((half - 1, half - 1), (half, half - 1),
            (half - 1, half), (half, half))


def _v48p_tape(seat):
    """The selected route tape for a seat (the planner replays it open-loop)."""
    try:
        name = _V48_POLICY.selected.get(1 if seat == 1 else 0) or "default"
    except Exception:
        name = "default"
    tape = _V48_ROUTES.get(name)
    if not isinstance(tape, list) or not tape:
        tape = _V48_ROUTES.get("default")
    return tape if isinstance(tape, list) else []


_V48P_REPORT = {
    "courier_trips": 0, "courier_units": 0, "courier_errors": 0,
    "sr_turns": 0, "sr_units": 0, "sr_errors": 0,
}


# ---------------------------------------------------------------------------
# COURIER (from The 2945 Farm v9 layer, as carried by V49): from hour 12 a
# tape worker carrying premium cargo whose every remaining command today is a
# PASS or a move walks to the nearest shed-access tile, drops, and the units
# are offered in the first market slot the same day.
# ---------------------------------------------------------------------------
_V48P_COURIER_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON")
_V48P_COURIER_FROM_HOUR = 12
_V48P_COURIER_IDLE = frozenset(
    {"PASS", "NORTH", "SOUTH", "EAST", "WEST", "DROP"})
_V48P_COURIER_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1),
                       "EAST": (1, 0), "WEST": (-1, 0)}
_V48P_COURIER_STATE = {}


def _v48p_courier_walk(pos, target):
    x, y = pos
    tx, ty = target
    return ([["EAST"]] * max(0, tx - x) + [["WEST"]] * max(0, x - tx)
            + [["SOUTH"]] * max(0, ty - y) + [["NORTH"]] * max(0, y - ty))


def _v48p_courier_plan(tape, unit, pos, commands, step, end, board):
    """Walk-and-drop route for an idle tape worker, or None if it has work left today."""
    if commands[unit] and commands[unit][0] not in _V48P_COURIER_IDLE:
        return None
    for t in range(step + 1, end + 1):
        a = tape[t] if t < len(tape) else {}
        units = [a.get("farmer") or ["PASS"]] + list(a.get("hands") or [])
        command = units[unit] if unit < len(units) else ["PASS"]
        if command and command[0] not in _V48P_COURIER_IDLE:
            return None
    access = _v48p_access(board)
    target = min(access, key=lambda a: abs(a[0] - pos[0]) + abs(a[1] - pos[1]))
    walk = _v48p_courier_walk(pos, target)
    return walk + [["DROP"]] if len(walk) <= end - step else None


def _v48p_courier(obs, action, st):
    step = int(obs["step"])
    player = int(obs["player"])
    if step >= 718 or step % 24 < _V48P_COURIER_FROM_HOUR:
        return action
    day = step // 24
    if st.get("day") != day:
        st["day"] = day
        st["plans"] = {}
    tape = _v48p_tape(player)
    if not tape:
        return action
    farm = obs["farms"][player]
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
    inventories = obs["private"]["inventories"]
    commands = [list(action.get("farmer") or ["PASS"])] + [
        list(c) for c in (action.get("hands") or [])]
    commands += [["PASS"]] * (len(positions) - len(commands))
    end = day * 24 + 23
    plans = st["plans"]
    # Only tape workers: overlay-dedicated hands are appended after the crew.
    crew = 1 + max(len(tape[t].get("hands") or [])
                   for t in range(day * 24, min(len(tape), end + 1)))
    board = len(farm["tiles"])
    delivered = {}
    changed = False
    for unit, pos in enumerate(positions[:crew]):
        inventory = inventories[unit] if unit < len(inventories) else {}
        cargo = {k: int(v) for k, v in inventory.items()
                 if k in _V48P_COURIER_ITEMS and int(v) > 0}
        plan = plans.get(unit)
        if plan is None:
            if not cargo:
                continue
            route = _v48p_courier_plan(tape, unit, pos, commands,
                                       step, end, board)
            if route is None:
                continue
            plan = plans[unit] = {"route": route, "start": step}
            _V48P_REPORT["courier_trips"] += 1
        index = step - plan["start"]
        if index >= len(plan["route"]):
            continue
        command = plan["route"][index]
        if command == ["DROP"]:
            if pos not in _v48p_access(board):
                plans[unit] = {"route": [], "start": step}
                continue
            for item, n in cargo.items():
                delivered[item] = delivered.get(item, 0) + n
        commands[unit] = command
        changed = True
    if not changed:
        return action
    result = dict(action)
    result["farmer"], result["hands"] = commands[0], commands[1:]
    if delivered:
        market = [list(o) for o in action.get("market") or []]
        prices = obs["market"]["prices"]
        for item, n in sorted(delivered.items(),
                              key=lambda kv: -int(prices.get(kv[0], 0)) * kv[1]):
            if int(prices.get(item, 0)) < 2:
                continue
            existing = next(
                (o for o in market
                 if o and o[0] == "SELL" and len(o) >= 3 and o[1] == item),
                None)
            if existing is not None:
                existing[2] = int(existing[2]) + n
                market.remove(existing)
                market.insert(0, existing)
            elif len(market) < _V48P_MAX_ORDERS:
                market.insert(0, ["SELL", item, n])
            _V48P_REPORT["courier_units"] += n
        result["market"] = market
    return result


_V48P_COURIER_PARENT = agent


def agent(observation, configuration=None):
    action = _V48P_COURIER_PARENT(observation, configuration)
    try:
        player, step = int(observation["player"]), int(observation["step"])
        st = _V48P_COURIER_STATE.get(player)
        if st is None or step <= st["step"]:
            st = _V48P_COURIER_STATE[player] = {"step": -1}
        st["step"] = step
        if not _v48p_standard(configuration) or not isinstance(action, dict):
            return action
        if step == 0:
            _V48P_REPORT["courier_trips"] = 0
            _V48P_REPORT["courier_units"] = 0
            _V48P_REPORT["courier_errors"] = 0
        return _v48p_courier(observation, action, st)
    except Exception:
        _V48P_REPORT["courier_errors"] += 1
        return action


# ---------------------------------------------------------------------------
# SHEDROOM (V49 layer): in the last two hours of the day, sell shed goods that
# the midnight auto-drop would discard at the shed capacity limit (with a
# small safety margin), keeping the tape's next-day feed and fertilizer.
# ---------------------------------------------------------------------------
_V48P_SR_MARGIN = 4
_V48P_SR_HOURS = (22, 23)
_V48P_SR_PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                     "EGG", "MILK", "WOOL", "FERTILIZER")


def _v48p_sr_tape(seat, t):
    tape = _v48p_tape(seat)
    if t < 0 or t >= len(tape) or not isinstance(tape[t], dict):
        return {}
    return tape[t]


_V48P_SR_PARENT = agent


def agent(observation, configuration=None):
    action = _V48P_SR_PARENT(observation, configuration)
    try:
        step = int(observation["step"])
        if step == 0:
            for key in ("sr_turns", "sr_units", "sr_errors"):
                _V48P_REPORT[key] = 0
        if not _v48p_standard(configuration) or not isinstance(action, dict):
            return action
        if step % 24 not in _V48P_SR_HOURS or step >= 717:
            return action
        seat = int(observation["player"])
        farm = observation["farms"][seat]
        priv = observation["private"]
        board = len(farm["tiles"])
        access = _v48p_access(board)
        proj = _v48p_projected_shed(observation, action)
        market = [list(o) for o in (action.get("market") or [])]
        left = dict(proj)
        night_shed = sum(max(0, int(v)) for v in proj.values())
        for o in market:
            if len(o) >= 3 and o[0] == "SELL":
                got = min(max(0, int(o[2])), max(0, int(left.get(o[1], 0))))
                left[o[1]] = left.get(o[1], 0) - got
                night_shed -= got
            elif len(o) >= 3 and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL"):
                night_shed += max(0, int(o[2]))
        units = [action.get("farmer") or ["PASS"]] + list(
            action.get("hands") or [])
        carried = 0
        all_positions = [tuple(farm["farmer"])] + [
            tuple(p) for p in farm["hands"]]
        for i, pos in enumerate(all_positions):
            inv = priv["inventories"][i] if i < len(priv["inventories"]) else {}
            held = sum(max(0, int(v)) for v in inv.values())
            cmd = units[i] if i < len(units) and units[i] else ["PASS"]
            tile = (farm["tiles"][pos[1]][pos[0]]
                    if isinstance(pos, (list, tuple))
                    and 0 <= pos[1] < board and 0 <= pos[0] < len(farm["tiles"][pos[1]])
                    else None)
            op = cmd[0] if cmd else "PASS"
            if op == "DROP" and tuple(pos) in access:
                held = 0
            elif op == "HARVEST" and isinstance(tile, dict):
                held += max(0, int(tile.get("yield_units", 0)))
            elif (op == "COLLECT_FERTILIZER" and isinstance(tile, dict)
                    and tile.get("fertilizer_available")):
                held += 1
            elif op in ("FEED", "FERTILIZE") and held > 0:
                held -= 1
            elif op == "PICKUP" and len(cmd) >= 2 and tuple(pos) in access:
                held += max(1, int(cmd[2]) if len(cmd) >= 3 else 1)
            carried += held
        cap = 100
        if isinstance(configuration, dict):
            cap = int(configuration.get("shedCapacity", 100))
        overflow = night_shed + carried - cap + _V48P_SR_MARGIN
        if overflow <= 0:
            return action
        need = {"WHEAT": 0, "FERTILIZER": 0}
        for t in range(step + 1, min(719, step + 25)):
            act = _v48p_sr_tape(seat, t)
            for c in [act.get("farmer") or ["PASS"]] + list(
                    act.get("hands") or []):
                if not c:
                    continue
                if c[0] == "FEED":
                    need["WHEAT"] += 1
                elif c[0] == "FERTILIZE":
                    need["FERTILIZER"] += 1
        prices = observation["market"]["prices"]
        cands = []
        for item in _V48P_SR_PRODUCTS:
            spare = int(left.get(item, 0)) - need.get(item, 0)
            if spare > 0 and int(prices.get(item, 0)) >= 2:
                cands.append((int(prices.get(item, 0)), item, spare))
        cands.sort()
        sold_now = 0
        for price, item, spare in cands:
            if overflow <= 0:
                break
            q = min(spare, overflow)
            for o in market:
                if len(o) >= 3 and o[:2] == ["SELL", item]:
                    o[2] = int(o[2]) + q
                    break
            else:
                if len(market) >= _V48P_MAX_ORDERS:
                    continue
                market.append(["SELL", item, q])
            overflow -= q
            sold_now += q
        if sold_now:
            _V48P_REPORT["sr_turns"] += 1
            _V48P_REPORT["sr_units"] += sold_now
            action = dict(action)
            action["market"] = market
    except Exception:
        _V48P_REPORT["sr_errors"] += 1
    return action


def _v48plus_entrypoint(observation, configuration=None):
    return agent(observation, configuration)


agent.telemetry = _V48P_REPORT
