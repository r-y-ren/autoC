"""ROUTENN1 -- trained crew dispatch on top of the day plan (flag `plan.ROUTE_NN_ON`, default False).

Reduced dispatch MDP (the day plan stays the planner's; the policy owns what the plan leaves idle):
  * HIRE decision, dawn of days [DAY0, 28]: delta in {-2..+2} on the planner's hire argmax (after the head's
    d_hire), re-clipped to the affordable prefix inside `plan` (`_residual_hire`), so routes/bills stay consistent.
  * DISPATCH decision, every turn: each unit whose remaining plan suffix is all PASS is FREE; the policy points at
    one engine-legal task from the observation (WATER / HARVEST / FEED / COLLECT_FERTILIZER / FERTILIZE / PLANT c)
    or PASS.  A chosen task is a job: the unit walks there (Manhattan steps) and issues the command, then is free
    again.  Tiles still owned by a cached route are excluded (never steal planned work).
Network (numpy here, JAX in the trainer through the same `forward`): global MLP g, hand embedding h(g, hand),
task embedding t_k, pointer logit_k = v . relu(W [t_k, h, t_k*h]); hire head on (g, onehot planner count);
value on g.  ~40k params, < 1 ms per decision.
"""
from __future__ import annotations

import numpy as np

from .. import spec
from ..core import plan as P
from ..core import projector as PJ
from . import parse as PA

K1 = 32                 # candidate rows per decision (row 0 = PASS)
F_T, F_H, F_G = 26, 8, 16
N_HIRE = 5              # delta -2..+2
HID = 64
DAY0 = 10
BUY_FLOOR = 1500        # cash the crew never spends on its own 1-unit seed rows
TYPES = ("PASS", "WATER", "HARVEST", "FEED", "COLLECT_FERTILIZER", "FERTILIZE", "PLANT", "CARE", "BUY_PLANT")
NT = len(TYPES)
_CI = {c: i for i, c in enumerate(spec.CROPS)}
_MOVES = {(0, -1): "NORTH", (0, 1): "SOUTH", (-1, 0): "WEST", (1, 0): "EAST"}

# ---- runtime hooks (set by the packaged agent or the trainer) ----
PARAMS = None           # dict of arrays
SAMPLE_RNG = None       # np.random.Generator -> sample; None -> greedy
HIRE_GREEDY = False     # gate split: argmax hire head while the dispatcher samples
HIRE_FROZEN = True      # ROUTENN2: hire head masked at delta 0 (no decision recorded) until dispatch alone is purse-positive
RECORD = None           # list -> decisions appended (training)
TRACK = False           # per-day route-quality reward + crew metrics (training / gate only; never in the package)
DAYR = {}               # day -> dense route-quality reward (coins) of OUR crew that day
MET = {}                # crew metrics d10-29 (see `observe`)
_OBS = {}               # dawn observation handed to the plan's hire hook


def init_params(seed=0):
    r = np.random.default_rng(seed)
    g = lambda i, o, s=1.0: (r.standard_normal((i, o)) * s / np.sqrt(i)).astype(np.float32)
    z = lambda o: np.zeros(o, np.float32)
    p = dict(wg=g(F_G, HID), bg=z(HID), wh=g(F_H + HID, HID), bh=z(HID), wt=g(F_T, HID), bt=z(HID),
             wc=g(3 * HID, HID), bc=z(HID), vo=g(HID, 1, 0.1)[:, 0], w_y=g(HID + 17, HID), b_y=z(HID),
             wy=g(HID, N_HIRE, 0.1), by=z(N_HIRE), wv1=g(F_G, HID), bv1=z(HID), wv=g(HID, 1, 0.1)[:, 0], bv=z(1))
    p["by"][2] = 3.0              # start at the planner's own count (delta 0)
    p["pass_b"] = np.array([3.0], np.float32)   # start at the plan's own PASS
    return p


def n_params(p):
    return int(sum(np.asarray(v).size for v in p.values()))


def _relu(xp, x):
    return xp.maximum(x, 0)


def glob_embed(xp, p, glob):
    return xp.tanh(glob @ p["wg"] + p["bg"])


def value(xp, p, glob):
    return _relu(xp, glob @ p["wv1"] + p["bv1"]) @ p["wv"] + p["bv"][0]


def dispatch_logits(xp, p, glob, hand, tasks, mask):
    """glob [..,F_G] hand [..,F_H] tasks [..,K1,F_T] mask [..,K1] -> logits [..,K1] (masked -1e9)."""
    g = glob_embed(xp, p, glob)
    h = xp.tanh(xp.concatenate([hand, g], -1) @ p["wh"] + p["bh"])
    t = xp.tanh(tasks @ p["wt"] + p["bt"])
    hb = xp.broadcast_to(h[..., None, :], t.shape)
    z = _relu(xp, xp.concatenate([t, hb, t * hb], -1) @ p["wc"] + p["bc"]) @ p["vo"]
    z = z + tasks[..., 0] * p["pass_b"][0]          # feature 0 = is-PASS row
    return xp.where(mask > 0, z, -1e9)


def hire_logits(xp, p, glob, hstar_oh):
    g = glob_embed(xp, p, glob)
    return _relu(xp, xp.concatenate([g, hstar_oh], -1) @ p["w_y"] + p["b_y"]) @ p["wy"] + p["by"]


def _pick(z):
    z = np.asarray(z, np.float64)
    z = z - z.max()
    pr = np.exp(z) / np.exp(z).sum()
    a = int(np.argmax(pr)) if SAMPLE_RNG is None else int(SAMPLE_RNG.choice(len(pr), p=pr))
    return a, float(np.log(pr[a] + 1e-30))


# ---------------------------------------------------------------- features
def _glob(obs, player, day, hour, n_free):
    farm = obs["farms"][player]
    opp = obs["farms"][1 - player] if len(obs["farms"]) > 1 else farm
    tiles = farm["tiles"]
    planted = vacant = unw = ripe = animals = 0
    for line in tiles:
        for t in line:
            if t is None:
                vacant += 1
            elif isinstance(t, dict):
                if t.get("kind") == "PLANT":
                    planted += 1
                    unw += int(not t.get("watered_today"))
                    ripe += int(t.get("yield_units", 0) > 0)
                elif "animal" in t:
                    animals += 1
                    ripe += int(t.get("yield_units", 0) > 0)
    priv = obs.get("private", {}) or {}
    shed = sum((priv.get("shed") or {}).values())
    seeds = sum((priv.get("seeds") or {}).values())
    m, o = float(farm["money"]), float(opp["money"])
    return np.array([day / 30, hour / 24, m / 1e5, o / 1e5, np.tanh((m - o) / 2e4), len(farm["hands"]) / 13,
                     planted / 40, vacant / 40, unw / 40, ripe / 40, shed / 100, seeds / 20, n_free / 13,
                     animals / 20, float(day >= 20), 1.0], np.float32)


def hire_delta(h_star):
    """Called from `plan` at dawn (numpy path only). Returns delta in -2..+2 (0 when not armed)."""
    o = _OBS.get("obs")
    if PARAMS is None or o is None or HIRE_FROZEN:
        return 0
    day = int(o.get("day", 0))
    if day < DAY0 or day > 28:
        return 0
    if _OBS.get("hire_day") == day:          # build_day may enumerate twice: one decision per dawn
        return _OBS["hire_d"]
    glob = _glob(o, int(o.get("player", 0)), day, 0, 0)
    oh = np.zeros(17, np.float32)
    oh[min(max(int(h_star), 0), 16)] = 1
    z = hire_logits(np, PARAMS, glob, oh)
    a, lp = _pick(z) if not HIRE_GREEDY else (int(np.argmax(z)), 0.0)
    if RECORD is not None:
        RECORD.append(dict(kind=1, day=day, hour=0, glob=glob, hoh=oh, a=a, logp=lp,
                           v=float(value(np, PARAMS, glob))))
    _OBS["hire_day"], _OBS["hire_d"] = day, a - 2
    return a - 2


def _task_row(tp, dist, left, crop=-1, tile=None, day=0, price=0.0):
    f = np.zeros(F_T, np.float32)
    f[tp] = 1.0
    f[9] = dist / 10
    f[10] = (dist + 1) / max(left, 1)
    if crop >= 0:
        f[11 + crop] = 1.0
    f[16] = price / 100
    f[24] = float(dist == 0)
    if isinstance(tile, dict):
        if tile.get("kind") == "PLANT":
            c = _CI[tile["crop"]]
            f[11 + c] = 1.0
            f[17] = tile.get("yield_units", 0) / max(int(spec.CROP_MAX_YIELD[c]), 1)
            f[18] = (day - int(tile["planted_day"])) / max(int(spec.CROP_MAX_YIELD_DAY[c]), 1)
            f[19] = float(tile.get("consecutive_unwatered", 0))
            f[20] = float(tile.get("fertilized_until_day", -1) >= day)
            f[21] = float(int(spec.CROP_WINDOW_START[c]) <= day - int(tile["planted_day"])
                          <= int(spec.CROP_MAX_YIELD_DAY[c]))
        else:
            f[17] = tile.get("yield_units", 0) / 5
            f[19] = float(tile.get("consecutive_unfed", 0))
            f[25] = float(bool(tile.get("fed_today")))
    f[22] = float(day >= 29)
    f[23] = 1.0
    return f


def _claimed(plan, positions, hour):
    O = P.O
    mv = {O.OP_NORTH: (0, -1), O.OP_SOUTH: (0, 1), O.OP_WEST: (-1, 0), O.OP_EAST: (1, 0)}
    passive = (O.OP_PASS, O.OP_PICKUP, O.OP_DROP)
    out = set()
    ops = np.asarray(plan[0])
    for u, pos in enumerate(positions):
        if u >= ops.shape[0]:
            break
        x, y = map(int, pos)
        for op in ops[u, hour:]:
            op = int(op)
            if op in mv:
                x, y = x + mv[op][0], y + mv[op][1]
            elif op not in passive:
                out.add((x, y))
    return out


def _candidates(obs, player, u, pos, day, hour, claimed, used, spare_seeds, shed_room, can_buy=False, cash=0):
    farm = obs["farms"][player]
    priv = obs.get("private", {}) or {}
    inv = (priv.get("inventories") or [])
    bag = inv[u] if u < len(inv) else {}
    prices = (obs.get("market") or {}).get("prices", {}) or {}
    x, y = map(int, pos)
    left = spec.TURNS_PER_DAY - hour
    rows = []
    vacant = []
    for ty, line in enumerate(farm["tiles"]):
        for tx, t in enumerate(line):
            if (tx, ty) in claimed or (tx, ty) in used:
                continue
            d = abs(tx - x) + abs(ty - y)
            if d + 1 > left:
                continue
            if t is None:
                vacant.append((d, tx, ty))
                continue
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "PLANT":
                c = _CI[t["crop"]]
                pr = float(prices.get(t["crop"], 0))
                if not t.get("watered_today"):
                    rows.append((d, tx, ty, 1, -1, t, pr))
                if (t.get("yield_units", 0) > 0 and day - int(t["planted_day"]) >= int(spec.CROP_FIRST_YIELD_DAY[c])
                        and shed_room >= t.get("yield_units", 0)):
                    rows.append((d, tx, ty, 2, -1, t, pr))
                if bag.get("FERTILIZER", 0) > 0 and t.get("fertilized_until_day", -1) < day:
                    rows.append((d, tx, ty, 5, -1, t, pr))
            elif "animal" in t:
                if t.get("yield_units", 0) > 0 and shed_room >= t.get("yield_units", 0):
                    rows.append((d, tx, ty, 2, -1, t, 0.0))
                if not t.get("fed_today") and bag.get("WHEAT", 0) > 0:
                    rows.append((d, tx, ty, 3, -1, t, 0.0))
                if t.get("fertilizer_available"):
                    rows.append((d, tx, ty, 4, -1, t, 0.0))
                if not t.get("cared_today"):
                    rows.append((d, tx, ty, 7, -1, t, 0.0))
    vacant.sort()
    for c in range(spec.N_CROPS):
        if day + int(spec.CROP_FIRST_YIELD_DAY[c]) > 29:
            continue
        if spare_seeds[c] > 0:
            for d, tx, ty in vacant[:3]:
                rows.append((d, tx, ty, 6, c, None, float(prices.get(spec.CROPS[c], 0))))
        elif can_buy and cash >= int(spec.CROP_SEED_COST[c]):      # one seed bought this turn (DSM: 1 unit at a time)
            for d, tx, ty in vacant[:2]:
                if d + 2 <= left:
                    rows.append((d, tx, ty, 8, c, None, float(prices.get(spec.CROPS[c], 0))))
    rows.sort(key=lambda r: r[0])
    rows = rows[:K1 - 1]
    feats = np.zeros((K1, F_T), np.float32)
    mask = np.zeros(K1, np.float32)
    feats[0, 0] = 1.0
    feats[0, 23] = 1.0
    mask[0] = 1.0
    for i, (d, tx, ty, tp, c, t, pr) in enumerate(rows):
        feats[i + 1] = _task_row(tp, d, left, c, t, day, pr)
        mask[i + 1] = 1.0
    hand = np.array([hour / 24, left / 24, bag.get("WHEAT", 0) / 5, bag.get("FERTILIZER", 0) / 5,
                     sum(bag.values()) / 10, float(u == 0), x / spec.BOARD, y / spec.BOARD], np.float32)
    return rows, feats, mask, hand


def _cmd_for(job):
    tx, ty, tp, c = job
    if tp in (6, 8):
        return ["PLANT", spec.CROPS[c]]
    return [TYPES[tp]]


def _job_valid(job, farm, bag, day):
    tx, ty, tp, c = job
    t = farm["tiles"][ty][tx]
    if tp in (6, 8):
        return t is None
    if not isinstance(t, dict):
        return False
    if tp == 1:
        return t.get("kind") == "PLANT" and not t.get("watered_today")
    if tp == 2:
        return t.get("yield_units", 0) > 0
    if tp == 3:
        return "animal" in t and not t.get("fed_today") and bag.get("WHEAT", 0) > 0
    if tp == 4:
        return "animal" in t and bool(t.get("fertilizer_available"))
    if tp == 5:
        return t.get("kind") == "PLANT" and bag.get("FERTILIZER", 0) > 0
    if tp == 7:
        return "animal" in t and not t.get("cared_today")
    return False


def step(rt, obs, action, plan):
    """Runtime hook: rewrite the commands of FREE units. `rt` = Runtime (holds `_rnn_jobs`)."""
    if PARAMS is None:
        return action
    day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
    jobs = getattr(rt, "_rnn_jobs", None)
    if jobs is None or getattr(rt, "_rnn_day", -1) != day:
        jobs = rt._rnn_jobs = {}
        rt._rnn_day = day
    if day < DAY0 or day > 28:
        return action
    player = int(obs.get("player", 0))
    farm = obs["farms"][player]
    positions = [farm["farmer"], *farm["hands"]]
    commands = [action["farmer"], *action["hands"]]
    ops = np.asarray(plan[0])
    free = [u for u in range(len(positions)) if u < ops.shape[0] and commands[u] == ["PASS"]
            and np.all(ops[u, hour:] == P.O.OP_PASS)]
    for u in list(jobs):
        if u not in free:
            jobs.pop(u)
    if not free:
        return action
    priv = obs.get("private", {}) or {}
    inv = priv.get("inventories") or []
    claimed = _claimed(plan, positions, hour)
    used = {(j[0], j[1]) for j in jobs.values()}
    # seeds the plan still needs today are not spare
    fut = ops[:, hour:] == P.O.OP_PLANT
    crop_rows = np.asarray(plan[1])[:, hour:]
    seeds = priv.get("seeds") or {}
    spare = [int(seeds.get(c, 0)) - int(np.sum(fut & (crop_rows == i))) for i, c in enumerate(spec.CROPS)]
    for j in jobs.values():
        if j[2] == 6:
            spare[j[3]] -= 1
    carried = sum(sum(b.values()) for b in inv)
    shed_room = 100 - sum((priv.get("shed") or {}).values()) - carried
    market = list(action.get("market") or [])
    purchases = (P.O.MO_BUY_PRODUCT, P.O.MO_BUY_SEED, P.O.MO_BUY_ANIMAL, P.O.MO_BUY_LAND, P.O.MO_HIRE)
    can_buy = (hour >= 3 and not np.isin(np.asarray(plan[3])[hour:], purchases).any()
               and not any(o[0].startswith("BUY_") or o[0] == "HIRE" for o in market))
    cash = int(farm["money"]) - BUY_FLOOR
    bought = getattr(rt, "_rnn_bought", {})
    rt._rnn_bought = bought
    changed = False
    glob = None
    for u in free:
        bag = inv[u] if u < len(inv) else {}
        job = jobs.get(u)
        if job is not None and not _job_valid(job, farm, bag, day):
            jobs.pop(u)
            job = None
        if job is None:
            if glob is None:
                glob = _glob(obs, player, day, hour, len(free))
            rows, feats, mask, hand = _candidates(obs, player, u, positions[u], day, hour, claimed, used,
                                                  spare, shed_room, can_buy and len(market) < spec.MAX_MARKET_ORDERS,
                                                  cash)
            if len(rows) == 0:
                continue
            z = dispatch_logits(np, PARAMS, glob, hand, feats, mask)
            a, lp = _pick(z)
            if RECORD is not None:
                RECORD.append(dict(kind=0, day=day, hour=hour, glob=glob, hand=hand, tasks=feats, mask=mask,
                                   a=a, logp=lp, v=float(value(np, PARAMS, glob))))
            if a == 0:
                continue
            d, tx, ty, tp, c, _t, _p = rows[a - 1]
            job = (tx, ty, tp, c)
            jobs[u] = job
            used.add((tx, ty))
            if tp == 6:
                spare[c] -= 1
            if tp == 8:
                market.append(["BUY_SEED", spec.CROPS[c], 1])
                cash -= int(spec.CROP_SEED_COST[c])
                can_buy = False                 # one purchase row per turn from the crew
                jobs[u] = job = (tx, ty, 6, c)
                bought[u] = (day, hour)
            if tp == 2:
                shed_room -= int((_t or {}).get("yield_units", 0))
        tx, ty = job[0], job[1]
        x, y = map(int, positions[u])
        if (x, y) == (tx, ty) and bought.get(u) == (day, hour):
            cmd = ["PASS"]                      # the seed lands with this turn's market row
        elif (x, y) == (tx, ty):
            cmd = _cmd_for(job)
            jobs.pop(u)
        else:
            dx = (tx > x) - (tx < x)
            dy = (ty > y) - (ty < y)
            cmd = [_MOVES[(dx, 0)]] if dx else [_MOVES[(0, dy)]]
        commands[u] = cmd
        changed = True
    return dict(action, farmer=commands[0], hands=commands[1:], market=market) if changed else action


def arm(obs):
    """Runtime, dawn: hand the observation to the hire hook; lazy-load the packaged params."""
    global PARAMS
    if PARAMS is None and getattr(P, "ROUTE_NN_PARAMS", None):
        PARAMS = load(P.ROUTE_NN_PARAMS)
    if _OBS.get("obs") is not None and int(_OBS["obs"].get("step", -1)) > int(obs.get("step", 0)):
        _OBS.pop("hire_day", None)           # new game in the same process
    _OBS["obs"] = obs
    if _OBS.get("hire_day") is not None and int(obs.get("day", 0)) < int(_OBS["hire_day"]):
        _OBS.pop("hire_day", None)


_T = {}
_PT = []                # lazily built engine price table (training / gate only)


def _product(t):
    if t.get("kind") == "PLANT":
        return t["crop"]
    a = spec.ANIMALS.index(t["animal"])
    return spec.ITEMS[int(spec.ANIMAL_PRODUCT[a])]


def track_reset():
    _T.clear(); DAYR.clear(); MET.clear()


def _exp_units(c, age, left, have):
    """units a plant of crop c, `age` days old, is expected to yield at harvest within `left` more days."""
    t = min(int(spec.CROP_MAX_YIELD_DAY[c]), age + left)
    if t < int(spec.CROP_FIRST_YIELD_DAY[c]):
        return have, 0
    w0 = int(spec.CROP_WINDOW_START[c]); mx = int(spec.CROP_MAX_YIELD[c]); md = int(spec.CROP_MAX_YIELD_DAY[c])
    u = mx * min(1.0, max(1, t - w0 + 1) / max(1, md - w0 + 1))
    return max(float(have), u), max(t - age, 0)


def worth(obs, player):
    """(cash, projected value) of OUR farm: cash + field (expected harvest units x the planner's projected price
    at the harvest day: projector.inv_at_day on the engine price table) + animal yield, shed and bags at spot
    + seeds at seed cost. Nothing is worth anything after the last turn (the purse is the score)."""
    if not _PT:
        _PT.append(spec.build_price_table())
    pt = _PT[0]
    farm = obs["farms"][player]
    day = int(obs.get("day", 0))
    left = 29 - day
    mkt, spot = PA.parse_market(obs)
    shops = PA.parse_town(obs)
    pi = {n: i for i, n in enumerate(spec.PRODUCTS)}
    cache = {}

    def proj(p, ahead):
        if (p, ahead) not in cache:
            inv = PJ.inv_at_day(np, mkt, shops, ahead)
            cache[(p, ahead)] = float(pt[p, int(np.clip(inv[p] - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1))])
        return cache[(p, ahead)]
    v = 0.0
    for line in farm["tiles"]:
        for t in line:
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "PLANT":
                c = _CI[t["crop"]]
                u, ahead = _exp_units(c, day - int(t["planted_day"]), left, int(t.get("yield_units", 0)))
                if u > 0:
                    v += u * proj(pi[t["crop"]], ahead)
            elif "animal" in t:
                p = pi.get(_product(t))
                if p is not None:
                    v += int(t.get("yield_units", 0)) * float(spot[p])
    priv = obs.get("private", {}) or {}
    goods = dict(priv.get("shed") or {})
    for b in priv.get("inventories") or []:
        for k, n in (b or {}).items():
            goods[k] = goods.get(k, 0) + n
    for k, n in goods.items():
        if k in pi:
            v += n * float(spot[pi[k]])
    for k, n in (priv.get("seeds") or {}).items():
        if k in _CI:
            v += n * float(spec.CROP_SEED_COST[_CI[k]])
    return float(farm["money"]), v


def finish(final_money):
    """after the game: the last day's reward closes on the final purse (the score), so sum(DAYR) telescopes to
    final purse - worth at the first tracked dawn."""
    d = _T.get("wday")
    if d is not None:
        DAYR[d] = DAYR.get(d, 0.0) + float(final_money) - _T["w"]


def observe(obs, action):
    """Every turn, OUR seat (TRACK only). ROUTENN2 coin-consistent dense day reward:
    DAYR[d] = W(dawn d+1) - W(dawn d), W = cash + projected value (`worth`): a planting is credited its projected
    sale value at harvest minus the seed it spent, a death / rot / shed overflow debits the same value, the hire
    bill is the engine's own cash debit, h23 harvests move field value into the shed; the last day closes on the
    final purse (`finish`). The trainer subtracts the same board's OFF DAYR (paired baseline).
    Metrics d10-29: PASS per unit by hour bucket, hand-days, work ops (non-move non-PASS), dry deaths."""
    day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
    player = int(obs.get("player", 0))
    farm = obs["farms"][player]
    if _T.get("wday") != day:
        m, v = worth(obs, player)
        w = m + v
        if _T.get("wday") is not None:
            DAYR[_T["wday"]] = DAYR.get(_T["wday"], 0.0) + w - _T["w"]
        _T["wday"], _T["w"] = day, w
    prev = _T.get("tiles")
    if prev is not None and _T.get("day") != day and 10 <= day <= 29:
        for y, line in enumerate(farm["tiles"]):
            for x, t in enumerate(line):
                p = prev[y][x]
                if (isinstance(p, dict) and p.get("kind") == "PLANT" and isinstance(t, dict) and t.get("kind") == "WEED"
                        and int(p.get("consecutive_unwatered", 0)) >= 1 and not p.get("watered_today")):
                    MET["dry"] = MET.get("dry", 0) + 1
    if hour == spec.TURNS_PER_DAY - 1 or prev is None:
        _T["tiles"] = [[(dict(t) if isinstance(t, dict) else t) for t in line] for line in farm["tiles"]]
    _T["day"] = day
    if 10 <= day <= 29:
        cmds = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
        b = "p02" if hour <= 2 else ("p320" if hour <= 20 else "p2123")
        for c in cmds:
            op = (c or ["PASS"])[0]
            if op == "PASS":
                MET[b] = MET.get(b, 0) + 1
            elif op not in ("NORTH", "SOUTH", "EAST", "WEST"):
                MET["work"] = MET.get("work", 0) + 1
        if hour == spec.TURNS_PER_DAY - 1:
            MET["unit_days"] = MET.get("unit_days", 0) + len(cmds)
            MET["hand_days"] = MET.get("hand_days", 0) + len(farm["hands"])


P.ROUTE_NN_HIRE_FN = hire_delta


def load(path):
    z = np.load(path)
    return {k: np.asarray(z[k], np.float32) for k in z.files}


def save(path, p):
    np.savez(path, **{k: np.asarray(v, np.float32) for k, v in p.items()})
