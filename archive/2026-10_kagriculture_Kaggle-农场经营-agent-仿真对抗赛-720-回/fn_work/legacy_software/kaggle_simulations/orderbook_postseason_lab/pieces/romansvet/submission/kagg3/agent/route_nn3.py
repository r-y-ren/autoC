"""ROUTENN3 -- per-hour pointer over the day plan's FULL task list (flag `plan.ROUTE_NN3_ON`, default False).

Every unit (farmer + hires, h0-2 included) is in one of two modes:
  * PLAN  : it replays its own planned ops (the planner's route) untouched;
  * QUEUE : it executes a queue of STOPS (tile, op, arg, qty, planned hour) by Manhattan navigation, skipping stops
            that became invalid / were taken by another unit; PLANT / PICKUP / PLACE / DROP / DIG / BUILD stops never
            fire before their planned hour (seeds / goods land on the plan's schedule).
A STOP is one non-move non-PASS op of the plan (extracted from the live plan at the unit's actual position).
DECISION points (days DAY0..28): a PLAN unit at the start of each leg / every waiting turn (hour 0 or its previous
planned op was not a move); a QUEUE unit whenever it has no current target.  Candidates (K1 rows):
  row 0 = KEEP (continue the plan / the next queue stop) -- init bias makes argmax == KEEP == the planner exactly;
  planner stops of every unit (other units' stops = re-assignment, own later stops = re-order), stealable ops only
  (WATER / HARVEST / FEED / COLLECT_FERTILIZER / FERTILIZE / PLANT / CARE), legal for THIS unit;
  unplanned legal jobs from the observation on unclaimed tiles (route_nn._candidates, no seed buys).
Taking a stop moves the chooser (and the stop's owner) to QUEUE mode.  Hire count = planner (ROUTE_NN_ON's hire head
is not involved).  Network = route_nn's pointer with wider task / hand features."""
from __future__ import annotations

import numpy as np

from .. import spec
from ..core import plan as P
from . import render
from . import route_nn as RN

O = P.O
K1 = 32
F_T, F_H, F_G = 30, 10, RN.F_G
HID = RN.HID
DAY0 = 10
KEEP_B0 = 8.5                  # init keep bias: P(deviate) ~ 0.4 % per decision at init (sampled): ~12 changes/game
MAX_PLAN_ROWS = 20
_MV = {O.OP_NORTH: (0, -1), O.OP_SOUTH: (0, 1), O.OP_WEST: (-1, 0), O.OP_EAST: (1, 0)}
_STEAL = {O.OP_WATER: 1, O.OP_HARVEST: 2, O.OP_FEED: 3, O.OP_COLLECT_FERT: 4, O.OP_FERTILIZE: 5, O.OP_PLANT: 6,
          O.OP_CARE: 7}
_TP2OP = {v: k for k, v in _STEAL.items()}
_WAIT = (O.OP_PLANT, O.OP_PICKUP, O.OP_PLACE, O.OP_DROP, O.OP_DIG, O.OP_BUILD_COOP, O.OP_BUILD_PASTURE)

PARAMS = None
SAMPLE_RNG = None
RECORD = None
DEBUG = None
FORCE_QUEUE = False            # test hook: every unit runs its own stops through the QUEUE executor (fidelity check)
STATS = {}                     # per game: decisions / changes by hour bucket + kind


def init_params(seed=0):
    r = np.random.default_rng(seed)
    g = lambda i, o, s=1.0: (r.standard_normal((i, o)) * s / np.sqrt(i)).astype(np.float32)
    z = lambda o: np.zeros(o, np.float32)
    p = dict(wg=g(F_G, HID), bg=z(HID), wh=g(F_H + HID, HID), bh=z(HID), wt=g(F_T, HID), bt=z(HID),
             wc=g(3 * HID, HID), bc=z(HID), vo=g(HID, 1, 0.1)[:, 0], wv1=g(F_G, HID), bv1=z(HID),
             wv=g(HID, 1, 0.1)[:, 0], bv=z(1))
    p["pass_b"] = np.array([KEEP_B0], np.float32)
    return p


def logits(xp, p, glob, hand, tasks, mask):
    return RN.dispatch_logits(xp, p, glob, hand, tasks, mask)


def value(xp, p, glob):
    return RN.value(xp, p, glob)


def stats_reset():
    STATS.clear()


def _stat(k, n=1):
    STATS[k] = STATS.get(k, 0) + n


def _stops(ops, arg, qty, u, pos, h0):
    x, y = map(int, pos)
    out = []
    for h in range(h0, ops.shape[1]):
        op = int(ops[u, h])
        if op in _MV:                          # the engine ignores a move off the board
            nx, ny = x + _MV[op][0], y + _MV[op][1]
            if 0 <= nx < spec.BOARD and 0 <= ny < spec.BOARD:
                x, y = nx, ny
        elif op != O.OP_PASS:
            out.append((x, y, op, int(arg[u, h]), int(qty[u, h]), h, u))
    return out


def _access():
    h = spec.BOARD // 2
    return [(h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h)]


def _key(s):
    return (s[0], s[1], s[2])


def _valid(s, farm, bag, seeds):
    x, y, op, a = s[0], s[1], s[2], s[3]
    if not (0 <= x < spec.BOARD and 0 <= y < spec.BOARD):
        return False
    t = farm["tiles"][y][x]
    if op == O.OP_PLANT:
        return t is None and int(seeds.get(spec.CROPS[a], 0)) > 0
    if op not in _STEAL:
        return True
    return RN._job_valid((x, y, _STEAL[op], a), farm, bag, 0)


def _row(s, pos, hour, left, farm, day, prices, own, keep):
    x, y, op = s[0], s[1], s[2]
    d = abs(x - pos[0]) + abs(y - pos[1])
    tp = _STEAL.get(op, 0)
    crop = s[3] if op == O.OP_PLANT else -1
    t = farm["tiles"][y][x] if 0 <= x < spec.BOARD and 0 <= y < spec.BOARD else None
    pr = float(prices.get(t["crop"], 0)) if isinstance(t, dict) and t.get("kind") == "PLANT" else 0.0
    f = np.zeros(F_T, np.float32)
    f[:RN.F_T] = RN._task_row(tp, d, left, crop, t, day, pr)
    if keep:
        f[0] = 1.0
    f[26] = 1.0
    f[27] = float(own)
    f[28] = (s[5] - hour) / 24
    f[29] = float(op not in _STEAL)
    return f, d


def _hand(u, pos, hour, bag, qlen, mode):
    left = spec.TURNS_PER_DAY - hour
    return np.array([hour / 24, left / 24, bag.get("WHEAT", 0) / 5, bag.get("FERTILIZER", 0) / 5,
                     sum(bag.values()) / 10, float(u == 0), pos[0] / spec.BOARD, pos[1] / spec.BOARD,
                     qlen / 10, float(mode == "q")], np.float32)


def _cmd(s):
    return render.unit_action(s[2], s[3], s[4])


def step(rt, obs, action, plan):
    arm()
    if PARAMS is None:
        return action
    day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
    st = getattr(rt, "_rn3", None)
    if st is None or st["day"] != day:
        st = rt._rn3 = dict(day=day, mode={}, queue={}, job={}, taken=set(), start={})
    if day < DAY0 or day > 28:
        return action
    player = int(obs.get("player", 0))
    farm = obs["farms"][player]
    positions = [tuple(map(int, p)) for p in [farm["farmer"], *farm["hands"]]]
    commands = [action["farmer"], *action["hands"]]
    ops, arg, qty = (np.asarray(plan[i]) for i in range(3))
    nu = min(len(positions), ops.shape[0])
    start = st["start"]

    def ppos(u, h):         # where unit u stands at hour h had it followed the plan from its (assumed) start
        h0, (x, y) = start[u]
        for hh in range(h0, h):
            op = int(ops[u, hh])
            if op in _MV:
                nx, ny = x + _MV[op][0], y + _MV[op][1]
                if 0 <= nx < spec.BOARD and 0 <= ny < spec.BOARD:
                    x, y = nx, ny
        return (x, y)
    new = [u for u in range(nu) if u not in start]
    if new:
        # the plan routed today's hires from the spawn the ENGINE rule gives on the PLANNED positions
        # (first free shed-access tile, NWSE, ties by occupancy): deviations must not move a hire's route
        occ = [ppos(v, hour) for v in range(nu) if v in start]
        acc = _access()
        for u in new:
            if u == 0 or hour == 0:
                start[u] = (hour, positions[u])
            else:
                cnt = {t: sum(1 for q in occ if q == t) for t in acc}
                sp = sorted(acc, key=lambda t: (cnt[t], acc.index(t)))[0]
                start[u] = (hour, sp)
            occ.append(start[u][1])
    if hour == 0:           # h0 occupancy decides where today's hires spawn (h1): plan at h0
        return action
    priv = obs.get("private", {}) or {}
    inv = priv.get("inventories") or []
    seeds = dict(priv.get("seeds") or {})
    prices = (obs.get("market") or {}).get("prices", {}) or {}
    mode, queue, job, taken = st["mode"], st["queue"], st["job"], st["taken"]
    left = spec.TURNS_PER_DAY - hour

    def rem(u):             # remaining stops of unit u (plan mode: from the live plan; queue mode: its queue)
        if mode.get(u, "p") == "p":
            return [s for s in _stops(ops, arg, qty, u, ppos(u, hour), hour) if _key(s) not in taken]
        return [s for s in queue.get(u, []) if _key(s) not in taken]

    def to_queue(u):
        if mode.get(u, "p") == "p":
            queue[u] = [s for s in _stops(ops, arg, qty, u, ppos(u, hour), hour) if _key(s) not in taken]
            mode[u] = "q"
            job[u] = None

    for u in range(nu):                        # a plan unit whose stop was taken leaves the plan
        if FORCE_QUEUE:
            to_queue(u)
        if mode.get(u, "p") == "p" and (ppos(u, hour) != positions[u]
                                        or any(_key(s) in taken for s in _stops(ops, arg, qty, u, positions[u], hour))):
            to_queue(u)             # off its planned tile (spawned elsewhere) or a stop was taken: leave the plan
    glob = None
    changed = False
    for u in range(nu):
        bag = inv[u] if u < len(inv) else {}
        m = mode.get(u, "p")
        if m == "p":
            decide = int(ops[u, hour - 1]) not in _MV
        else:
            decide = job.get(u) is None
        if decide:
            if glob is None:
                glob = RN._glob(obs, player, day, hour, nu)
            mine = rem(u)
            # KEEP target (for its feature row): plan -> next own stop; queue -> next valid queued stop
            nxt = mine[0] if mine else None
            rows, feats = [], []
            if nxt is not None:
                f0, _ = _row(nxt, positions[u], hour, left, farm, day, prices, True, True)
            else:
                f0 = np.zeros(F_T, np.float32); f0[0] = 1.0; f0[23] = 1.0
            cand = []
            claimed = set()
            for v in range(nu):
                for s in rem(v):
                    claimed.add((s[0], s[1]))
                    if s == nxt or s[2] not in _STEAL:
                        continue
                    if not _valid(s, farm, bag, seeds):
                        continue
                    d = abs(s[0] - positions[u][0]) + abs(s[1] - positions[u][1])
                    if d + 1 > left:
                        continue
                    cand.append((d, s, v == u))
            cand.sort(key=lambda c: c[0])
            for d, s, own in cand[:MAX_PLAN_ROWS]:
                f, _ = _row(s, positions[u], hour, left, farm, day, prices, own, False)
                rows.append(("s", s)); feats.append(f)
            for jj in job.values():
                if jj is not None:
                    claimed.add((jj[0], jj[1]))
            spare = [int(seeds.get(c, 0)) for c in spec.CROPS]
            for v in range(nu):
                for s in rem(v):
                    if s[2] == O.OP_PLANT:
                        spare[s[3]] -= 1
            xr, xf, _xm, _h = RN._candidates(obs, player, u, positions[u], day, hour, claimed, set(), spare, 0,
                                             False, 0)
            for i, r in enumerate(xr[:K1 - 1 - len(rows)]):
                d, tx, ty, tp, c, _t, _p = r
                if tp not in _TP2OP:
                    continue
                f = np.zeros(F_T, np.float32); f[:RN.F_T] = xf[i + 1]
                s = (tx, ty, _TP2OP[tp], max(c, 0), 1, hour, -1)
                rows.append(("x", s)); feats.append(f)
            if rows:
                T = np.zeros((K1, F_T), np.float32); M = np.zeros(K1, np.float32)
                T[0] = f0; M[0] = 1.0
                T[1:len(rows) + 1] = np.stack(feats); M[1:len(rows) + 1] = 1.0
                hd = _hand(u, positions[u], hour, bag, len(mine), m)
                z = logits(np, PARAMS, glob, hd, T, M)
                a, lp = _pick(z)
                hb = "h0_2" if hour <= 2 else ("h3_20" if hour <= 20 else "h21_23")
                _stat("dec_" + hb)
                if RECORD is not None:
                    RECORD.append(dict(kind=0, day=day, hour=hour, glob=glob, hand=hd, tasks=T, mask=M, a=a, logp=lp,
                                       v=float(value(np, PARAMS, glob))))
                if a > 0:
                    kind, s = rows[a - 1]
                    if RECORD is not None:
                        RECORD[-1]["ck"] = "extra" if kind == "x" else ("own" if s[6] == u else "steal")
                        RECORD[-1]["op"] = int(s[2])
                    _stat("chg_" + hb); _stat("chg_" + kind + ("own" if kind == "s" and s[6] == u else ""))
                    _stat(f"chgop_{s[2]}")
                    to_queue(u)
                    if kind == "s":
                        owner = s[6]
                        if owner != u:
                            to_queue(owner)
                            queue[owner] = [q for q in queue.get(owner, []) if _key(q) != _key(s)]
                            if job.get(owner) is not None and _key(job[owner]) == _key(s):
                                job[owner] = None
                        else:
                            queue[u] = [q for q in queue.get(u, []) if _key(q) != _key(s)]
                    taken.add(_key(s))
                    job[u] = (*s[:5], hour, s[6])
                    m = "q"
        if mode.get(u, "p") == "p":
            continue
        # ---- QUEUE execution: a queued plan stop fires AT its planned hour (never earlier: the plan's cross-unit
        # dependencies -- placed animals, landed seeds, picked-up goods -- hold), late stops fire on arrival; a stop
        # that is invalid once due is dropped.  Pointer jobs carry hour = the decision hour (asap).
        cmd = None
        if commands[u] and commands[u][0] == "PLACE":     # overflow-guard rows edited into the live plan: keep
            cmd = commands[u]
            if job.get(u) is not None and job[u][2] == O.OP_PLACE and job[u][5] == hour:
                job[u] = None
            queue[u] = [q for q in queue.get(u, []) if not (q[2] == O.OP_PLACE and q[5] == hour)]
        for _ in range(8 if cmd is None else 0):
            j = job.get(u)
            if j is None:
                q = queue.get(u, [])
                while q:
                    s_ = q.pop(0)
                    if _key(s_) in taken:
                        continue
                    if abs(s_[0] - positions[u][0]) + abs(s_[1] - positions[u][1]) + 1 > left:
                        _stat(f"skipfar_{s_[2]}")
                        continue
                    j = job[u] = s_
                    break
            if j is None:
                cmd = ["PASS"]
                break
            x, y = positions[u]
            if (x, y) != (j[0], j[1]):
                dx = (j[0] > x) - (j[0] < x)
                dy = (j[1] > y) - (j[1] < y)
                cmd = [RN._MOVES[(dx, 0)]] if dx else [RN._MOVES[(0, dy)]]
                break
            if hour < j[5]:
                cmd = ["PASS"]
                break
            if j[2] in _STEAL and j[2] != O.OP_PLANT and not _valid(j, farm, bag, seeds):
                _stat(f"skipinv_{j[2]}")
                if DEBUG is not None:
                    DEBUG.append((day, hour, u, j, farm["tiles"][j[1]][j[0]], dict(bag)))
                job[u] = None
                continue
            cmd = _cmd(j)
            job[u] = None
            if j[2] == O.OP_PLANT:
                seeds[spec.CROPS[j[3]]] = int(seeds.get(spec.CROPS[j[3]], 0)) - 1
            break
        if cmd is None:
            cmd = ["PASS"]
        if cmd != commands[u]:
            _stat("cmd_diff")
        commands[u] = cmd
        changed = True
    return dict(action, farmer=commands[0], hands=commands[1:]) if changed else action


def _pick(z):
    z = np.asarray(z, np.float64)
    z = z - z.max()
    pr = np.exp(z) / np.exp(z).sum()
    a = int(np.argmax(pr)) if SAMPLE_RNG is None else int(SAMPLE_RNG.choice(len(pr), p=pr))
    return a, float(np.log(pr[a] + 1e-30))


def arm():
    global PARAMS
    if PARAMS is None and getattr(P, "ROUTE_NN3_PARAMS", None):
        PARAMS = RN.load(P.ROUTE_NN3_PARAMS)


load, save, n_params = RN.load, RN.save, RN.n_params
