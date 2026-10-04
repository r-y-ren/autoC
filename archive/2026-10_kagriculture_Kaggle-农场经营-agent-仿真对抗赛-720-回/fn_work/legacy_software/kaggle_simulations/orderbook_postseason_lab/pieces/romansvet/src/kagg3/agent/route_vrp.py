"""[SWITCH, ROUTE_VRP_ON] ROUTEOPT1: day crew VRP. At dawn the planner's own day table (unit_op/a/q + market
rows) is read back as a task set (tile stops, merged per tile in planner order), re-routed by a deterministic
insertion + relocate/2-opt + ruin-recreate search (pure python, ~0.7 s/day), and a smaller crew that still does every task
is written back into the SAME table (mode ii: the last HIRE rows are removed). The crew is a GREEDY heuristic (the last
hire is dropped while its stops still fit; the first failed drop ends the reduction), not a proven minimum; under
ROUTE_VRP_REPAIR_ON a failed drop gets a bounded repair (regret-2 insertion + 1-step ejection chain) [VRPREPAIR1]. Day 29 and any day the
search cannot complete keep the planner's table byte for byte. Research copy + tools: S/routeopt1/.
"""

import collections
import ctypes
import os
import shutil
import tempfile
import time
from array import array
import numpy as np
from .. import spec
from ..core import ops as O
from ..core import plan as _P   # eager: the engine harness drops kagg3 from sys.modules mid-game (ROUTEOPT1 §6)
from . import render

ACC = ((4, 4), (5, 4), (4, 5), (5, 5))
MV = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
NEED = {"FEED": "WHEAT", "FERTILIZE": "FERTILIZER"}
ANIMALS = ("CHICKEN", "COW", "SHEEP", "GOOSE", "PIG", "GOAT")
INF = 10 ** 6
RR_ITERS = 30   # fixed ruin-recreate iterations (deterministic); None = until the search deadline
# [RRDEPTH1] deeper search (ROUTERAUDIT1 rrmid arm): RR destroy size, the crew re-solve/drop loop after mode ii, and the
# last day the deep knobs apply (later days use the shipped (30, 8, off)). plan.ROUTE_VRP_RR_* (not None) override these.
RR_K = 8
RR_RESOLVE_ON = False
RR_DEEP_LAST_DAY = 29
_RR_SHIP = (30, 8, False)
# [RRSPEED1] clock-bounded deep search (LOAD-DEPENDENT, not deterministic): RR iterations past the shipped 30 and the
# re-solve/drop loop only run while < RR_WALL_S seconds have passed since apply() began; None = off (iteration count only).
RR_WALL_S = None
_T0 = [0.0]   # apply() start (_CLOCK)
ITERS_LOG = []
np.random.default_rng(0)   # [VRPDEADLINE1] warm numpy.random at import: its first call cost 0.06-0.33 s inside day 0's RR

# [ROUTERJIT1] compiled kernels (route_vrp_c.c -> route_vrp_c.so, no libc, loaded by ctypes): route_eval, best_insert and
# the intra-route 2-opt, exact ports (same routes byte for byte). JIT_ON False or a failed load = the Python path.
# The deep search knobs (RRDEPTH1) only apply while the kernels are live (DEEP_NEEDS_JIT), so a failed load falls back to
# the shipped (30, 8, off) search that fits the clock in Python.
JIT_ON = True
DEEP_NEEDS_JIT = True
_JMAXR, _JMAXU, _JMAXC, _JMAXI = 250, 64, 4000, 64


def _jit_load():
    here = os.path.dirname(os.path.abspath(__file__))
    so = os.path.join(here, "route_vrp_c.so")
    lib = None
    for path in (so, None):
        try:
            if path is None:   # noexec package mount: a private copy in the temp dir
                path = os.path.join(tempfile.mkdtemp(prefix="rvjit"), "route_vrp_c.so"); shutil.copyfile(so, path)
            lib = ctypes.CDLL(path)
            break
        except Exception:
            lib = None
    if lib is None:
        return None
    try:
        vp, ci = ctypes.c_void_p, ctypes.c_int
        lib.rv_eval.argtypes = (vp, vp, ci, ci, ci, ci, vp); lib.rv_eval.restype = ci
        lib.rv_best_insert.argtypes = (vp, vp, vp, vp); lib.rv_best_insert.restype = ci
        lib.rv_two_opt.argtypes = (vp, vp, ci, ci, ci, ci, vp); lib.rv_two_opt.restype = ci
        lib.rv_insert_seq.argtypes = (vp, vp, vp, ci, ci, vp, vp); lib.rv_insert_seq.restype = ci
        o = (ctypes.c_int * 6)(); c = (ctypes.c_double * 1)()
        ctx = array("i", [1, 0, 30, 0, 4, 4, 0, 1000000, 1, 0, 0, 0, 0]); r = array("i", [0])
        ok = lib.rv_eval(ctx.buffer_info()[0], r.buffer_info()[0], 1, 4, 4, 0, ctypes.addressof(o))
        if ok != 1 or list(o) != [1, 0, 0, -1, 0, 0]:   # self-test: one stop on the spawn tile, dur 1
            return None
    except Exception:
        return None
    return lib


_JL = _jit_load()
_JO = (ctypes.c_int * 6)(); _JOA = ctypes.addressof(_JO)
_JC = (ctypes.c_double * 1)(); _JCA = ctypes.addressof(_JC)
_JI = (ctypes.c_int * 2)(); _JIA = ctypes.addressof(_JI)
_JB = (ctypes.c_int * (_JMAXC + 2 * _JMAXU + 8))(); _JBA = ctypes.addressof(_JB)   # rv_insert_seq routes out
_JD = (ctypes.c_double * _JMAXU)(); _JDA = ctypes.addressof(_JD)                    # rv_insert_seq route costs out


def jit_live():
    return _JL is not None and JIT_ON


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dacc(p):
    return min(dist(p, a) for a in ACC)


class Stop:
    __slots__ = ("tile", "ops", "dur", "early", "late", "need", "give", "hours", "units", "harv", "mk", "opt", "val")

    def __init__(self, tile):
        self.tile = tile; self.ops = []; self.hours = []; self.units = set(); self.mk = []; self.opt = False; self.val = 0.0
        self.early = 0; self.late = INF; self.need = collections.Counter(); self.give = collections.Counter()
        self.harv = 0


def parse_day(hrs, last_hour):
    """hrs: {h: action dict}. Returns units (start pos, start hour, hire hour), per-unit op list [(h,pos,op)],
    market rows by hour, per-unit move/work/idle counts."""
    pos = {0: ACC[0]}; start = {0: 0}; hire_h = {0: -1}
    ops = collections.defaultdict(list); acc = collections.Counter()
    mk = collections.defaultdict(list)
    for h in range(last_hour + 1):
        act = hrs.get(h)
        if act is None:
            continue
        units = [act["farmer"]] + act["hands"]
        for u, a in enumerate(units):
            if u not in pos:
                continue
            k = a[0]
            if k in MV:
                dx, dy = MV[k]; x, y = pos[u]; nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    pos[u] = (nx, ny)
                acc[(u, "move")] += 1
            elif k == "PASS":
                acc[(u, "idle")] += 1
            else:
                acc[(u, "work")] += 1
                ops[u].append((h, pos[u], tuple(a)))
        for m in act["market"]:
            mk[h].append(tuple(m))
        for m in act["market"]:
            if m[0] == "HIRE":
                occ = [sum(1 for p in pos.values() if p == t) for t in ACC]
                j = int(np.argmin(occ)); u = len(pos)
                pos[u] = ACC[j]; start[u] = h + 1; hire_h[u] = h
    spawn = {}
    # recompute spawn tiles (positions at hire time)
    return start, hire_h, ops, mk, acc


def spawns(hrs, last_hour):
    pos = {0: ACC[0]}; sp = {0: ACC[0]}
    for h in range(last_hour + 1):
        act = hrs.get(h)
        if act is None:
            continue
        units = [act["farmer"]] + act["hands"]
        for u, a in enumerate(units):
            if u in pos and a[0] in MV:
                dx, dy = MV[a[0]]; x, y = pos[u]; nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    pos[u] = (nx, ny)
        for m in act["market"]:
            if m[0] == "HIRE":
                occ = [sum(1 for p in pos.values() if p == t) for t in ACC]
                j = int(np.argmin(occ)); u = len(pos); pos[u] = ACC[j]; sp[u] = ACC[j]
    return sp


def _sw(name):
    return bool(getattr(_P, name, False))


def _rr_knobs(day):
    """[RRDEPTH1] (iters, k, resolve) for this day: plan.ROUTE_VRP_RR_* when set, else the module knobs; days past
    RR_DEEP_LAST_DAY keep the shipped search."""
    g = lambda n, d: d if getattr(_P, n, None) is None else getattr(_P, n)
    if day > g("ROUTE_VRP_RR_DEEP_LAST_DAY", RR_DEEP_LAST_DAY):
        return _RR_SHIP
    if DEEP_NEEDS_JIT and not jit_live() and getattr(_P, "ROUTE_VRP_RR_ITERS", None) is not None:
        return _RR_SHIP   # [ROUTERJIT1] a deep search set by the switch string runs only on the compiled kernels
    return (g("ROUTE_VRP_RR_ITERS", RR_ITERS), g("ROUTE_VRP_RR_K", RR_K), bool(g("ROUTE_VRP_RR_RESOLVE_ON", RR_RESOLVE_ON)))


def _rr_wall():
    """[RRSPEED1] deep-search wall budget (s) since apply() start; None = unbounded."""
    return RR_WALL_S if getattr(_P, "ROUTE_VRP_RR_WALL_S", None) is None else _P.ROUTE_VRP_RR_WALL_S


def _deep_ok():
    w = _rr_wall()
    return w is None or _CLOCK() - _T0[0] < w


def plan_positions(hrs, last_hour):
    """engine replay of a day table: {unit: [position at the END of hour h]} (None before the unit exists)."""
    pos = {0: ACC[0]}; out = {0: [None] * (last_hour + 1)}
    for h in range(last_hour + 1):
        act = hrs.get(h)
        if act is not None:
            units = [act["farmer"]] + act["hands"]
            for u, a in enumerate(units):
                if u in pos and a[0] in MV:
                    dx, dy = MV[a[0]]; x, y = pos[u]; nx, ny = x + dx, y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        pos[u] = (nx, ny)
            for m in act["market"]:
                if m[0] == "HIRE":
                    occ = [sum(1 for p in pos.values() if p == t) for t in ACC]
                    j = int(np.argmin(occ)); u = len(pos); pos[u] = ACC[j]; out[u] = [None] * (last_hour + 1)
        for u in pos:
            out[u][h] = pos[u]
    return out


def build(hrs, obs, day, last_hour, ua=None, freeze=()):
    start, hire_h, ops, mk, acc = parse_day(hrs, last_hour)
    sp = spawns(hrs, last_hour)
    priv = obs["private"]; seat = obs["player"]
    tiles = obs["farms"][seat]["tiles"]
    shed = priv["shed"]; seeds = priv["seeds"]
    # availability per item/crop
    buy_h = {}
    for h in sorted(mk):
        for m in mk[h]:
            if m[0] in ("BUY_PRODUCT", "BUY_ANIMAL", "BUY_SEED"):
                buy_h.setdefault((m[0] == "BUY_SEED", m[1]), h)
    land_h = next((h for h in sorted(mk) for m in mk[h] if m[0] == "BUY_LAND"), None)
    sell_early = collections.Counter()
    for h in sorted(mk):
        if h <= 2:
            for m in mk[h]:
                if m[0] == "SELL":
                    sell_early[m[1]] += int(m[2])
    picks = collections.Counter(); plants = collections.Counter()
    for u, lst in ops.items():
        for h, p, a in lst:
            if a[0] == "PICKUP":
                picks[a[1]] += int(a[2])
            elif a[0] == "PLANT":
                plants[a[1]] += 1

    def avail(item, seed=False):
        stock = seeds.get(item, 0) if seed else shed.get(item, 0) - sell_early.get(item, 0)
        use = plants[item] if seed else picks[item]
        if stock >= use:
            return 0
        bh = buy_h.get((seed, item))
        return 2 if bh is None else bh + 1

    item_av = {k: avail(k) for k in set(list(picks) + ["WHEAT", "FERTILIZER"])}
    if _sw("ROUTE_VRP_PIN_PICKUP"):          # [SALEPIN1] no pickup before the planner's own first one
        first = {}
        for u, lst in ops.items():
            for h, p, a in lst:
                if a[0] == "PICKUP":
                    first[a[1]] = min(first.get(a[1], h), h)
        for k, h in first.items():
            item_av[k] = max(item_av.get(k, 2), h)
    # frozen units: mid-day shed DROP / PLACE of a product on an access tile before h21
    frozen = set(u for u in freeze if u in start or u == 0)
    for u, lst in ops.items():
        for h, p, a in lst:
            if p in ACC and (a[0] == "DROP" or (a[0] == "PLACE" and a[1] not in ANIMALS)) and h < 21:
                frozen.add(u)
    stops = {}
    nfix = _sw("ROUTE_VRP_NEEDS_FIX_ON")
    fz_ops = collections.defaultdict(list)
    for u, lst in ops.items():
        for h, p, a in lst:
            if u in frozen:
                fz_ops[u].append((h, p, a)); continue
            if a[0] in ("PICKUP", "DROP") or (a[0] == "PLACE" and p in ACC and a[1] not in ANIMALS):
                continue  # regenerated
            s = stops.get(p)
            if s is None:
                s = stops[p] = Stop(p)
            s.ops.append(a); s.hours.append(h); s.units.add(u)
            s.mk.append(int(ua[u, h]) if ua is not None else 0)
            if a[0] in NEED:
                s.need[NEED[a[0]]] += 1
            if a[0] == "PLACE":
                s.need[a[1]] += int(a[2])
            if a[0] == "COLLECT_FERTILIZER":
                s.give["FERTILIZER"] += 1
            if a[0] == "PLANT":
                s.early = max(s.early, avail(a[1], seed=True))
            if a[0] == "HARVEST":
                s.harv += 1
                t = tiles[p[1]][p[0]]
                if nfix and isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == "WHEAT" \
                        and day - int(t.get("planted_day", day)) >= int(spec.CROP_FIRST_YIELD_DAY[spec.CROPS.index("WHEAT")]):
                    s.give["WHEAT"] += int(t.get("yield_units", 0))   # [VRPFALLBACK1] harvested wheat rides with the unit
                if isinstance(t, dict) and t.get("kind") == "PLANT" and 0 < t.get("max_lifespan_step", 0) < (day + 1) * 24:
                    s.late = min(s.late, h)
            t = tiles[p[1]][p[0]]
            if t == "LOCKED":
                s.early = max(s.early, land_h + 1 if land_h is not None else min(s.hours))
    for s in stops.values():
        s.dur = len(s.ops)
        if s.late < INF:
            # late bound on the stop start: first harvest op index offset
            off = next(i for i, a in enumerate(s.ops) if a[0] == "HARVEST")
            s.late = s.late - off
    if ua is not None:
        _label_optional(stops, obs, day, mk)
    units = sorted(set([0]) | set(start))
    fz_pos = plan_positions(hrs, last_hour) if frozen else {}
    return dict(start=start, hire_h=hire_h, sp=sp, sp0=dict(sp), stops=list(stops.values()), frozen=frozen, fz_ops=fz_ops,
                fz_pos=fz_pos, hrs=hrs,
                item_av=item_av, acc=acc, units=units, ops=ops, end=last_hour + 1)


def _label_optional(stops, obs, day, mk):
    """[ROUTEOPT2] a stop is optional when every op on it is a planner tail op (TAIL_CARE / TAIL_FILL /
    CARE_FILL mark in unit_a) and the runtime's own displaced-job value (overflow._job_cost, the V3 guard's
    price of an op left undone) is finite; its value is that sum."""
    OV = _OV
    m0 = int(_P.ROUTE_VRP_OPT_MARK)
    marks = (m0 + 1, m0 + 2, m0 + 3)
    if not any(m in marks for s in stops.values() for m in s.mk):
        return
    asked = np.zeros(spec.N_PRODUCTS, np.int32)
    for h in mk:
        for m in mk[h]:
            if m[0] == "SELL":
                asked[spec.PRODUCTS.index(m[1])] += int(m[2])
    inv = np.array([obs["market"]["inventory"][p] for p in spec.PRODUCTS], np.int32)
    marginal = _P.PJ.marginal_quote(np, _P.PJ.sell_quotes(np, _P.default_price_table(), inv), asked)
    marginal = np.maximum(np.asarray(marginal, np.float64), 0.0)
    tiles = obs["farms"][obs["player"]]["tiles"]
    for s in stops.values():
        if not s.mk or not all(m in marks for m in s.mk):
            continue
        x, y = s.tile; before = []; v = 0.0
        for a in s.ops:
            code = INV.get(a[0])
            if code is None:
                v = OV._INF; break
            v += OV._job_cost(code, 0, tiles[y][x], day, before, marginal)
            before.append(code)
            if v >= OV._INF:
                break
        if v < OV._INF:
            s.opt = True; s.val = float(v)


_ACC_CACHE = {}


def _best_acc(p, nxt):
    k = (p, nxt)
    a = _ACC_CACHE.get(k)
    if a is None:
        a = _ACC_CACHE[k] = min(ACC, key=lambda q: dist(p, q) + dist(q, nxt))
    return a


MOVE_W = 0.01   # [VRPOBJ1] moves tie-break weight. A route has <= 24 moves (one per hour), so 0.01 x moves < 1 hour:
                # elapsed + MOVE_W x moves orders a route by (elapsed, moves) lexicographically (crew sums: while the
                # move delta < 100). 1/1024 (exact floats) re-breaks float-noise ties on 61 % of dawns: VRPOBJ1 sec. 3.


def route_key(elapsed, moves):
    """[VRPOBJ1] the ONE route objective: elapsed hours first, moves as the tie-break. Used by route_eval's pickup
    placement, Solver.rcost (insertion / improve / 2-opt / ruin-recreate acceptance) and the checkpoint ranking."""
    return elapsed + MOVE_W * moves


def sol_key(dropped, route_cost):
    """[VRPOBJ1] solution objective, lexicographic: crew bill first (fib daily wage of the hires kept; the day's
    hires are fixed, so fewer = larger sum of fib over the dropped hands), route cost second."""
    return (-sum(FIB[u - 1] for u in dropped), route_cost)


def route_eval(r, s0, t0, item_av, end, stops):
    """r: list of stop idx. Returns (finish, moves, waits, pickup slot, n kinds, pickup avail) or None.
    One pickup visit per route: at the start or just before the first consuming stop (cheaper of the two)."""
    mdef = None; cum = None; first_c = None
    for i, j in enumerate(r):
        st = stops[j]
        if st.need or st.give:
            if cum is None:
                cum = {}; mdef = {}
            for k, v in st.need.items():
                c = cum.get(k, 0) - v; cum[k] = c
                if -c > mdef.get(k, 0):
                    mdef[k] = -c
                    if first_c is None:
                        first_c = i
            for k, v in st.give.items():
                cum[k] = cum.get(k, 0) + v
    if not mdef:
        v = _sim(r, s0, t0, None, 0, 0, end, stops)
        return None if v is None else v + (None, 0, 0)
    nk = len(mdef)
    pav = max(item_av.get(k, 2) for k in mdef)
    best = None
    for pi in ((0,) if first_c == 0 else (0, first_c)):
        v = _sim(r, s0, t0, pi, nk, pav, end, stops)
        if v is not None and (best is None or route_key(v[0], v[1]) < route_key(best[0], best[1])):   # [VRPOBJ1] was finish + moves
            best = v + (pi, nk, pav)
    return best


def _sim(r, s0, t0, pi, nk, pav, end, stops):
    t = t0; px, py = s0; moves = 0; waits = 0
    n = len(r)
    for i in range(n + 1):
        if i == pi:
            nxt = stops[r[i]].tile if i < n else (px, py)
            ax, ay = _best_acc((px, py), nxt)
            dd = abs(px - ax) + abs(py - ay); moves += dd; t += dd
            if t < pav:
                waits += pav - t; t = pav
            t += nk; px, py = ax, ay
        if i == n:
            break
        st = stops[r[i]]
        x, y = st.tile
        dd = abs(px - x) + abs(py - y); moves += dd; t += dd
        if t < st.early:
            waits += st.early - t; t = st.early
        if t > st.late:
            return None
        t += st.dur; px, py = x, y
    if t > end:
        return None
    return (t, moves, waits)


class _Timeout(Exception):
    pass


_DEADLINE = [float("inf")]   # [VRPDEADLINE1] ONE time.perf_counter() search deadline for the whole apply() path
SAFETY_S = 0.75   # total wall-clock budget of apply(): search + write-back + trim + VERIFY (+ checkpoint restore)
RESERVE_S = 0.1  # of SAFETY_S kept for write-back/trim/VERIFY: the search stops at SAFETY_S - RESERVE_S
_CLOCK = time.perf_counter   # tests swap in a fake clock


def _check():
    if _CLOCK() > _DEADLINE[0]:
        raise _Timeout()
INSERT_K = 10   # exact evaluations per insertion (candidates ranked by walk detour)


class Solver:
    def __init__(self, B, budget=2.0):
        self.B = B; self.budget = budget
        self.stops = B["stops"]
        self.units = [u for u in B["units"] if u not in B["frozen"]]
        self.cache = {}
        self.seqsp = False  # [ROUTEOPT2] sequential spawn fixed point (retry days only)
        self.skip = set()   # [ROUTEOPT2] optional stops left undone (never re-inserted)
        self.ctx = None     # [VRPDEADLINE1] (units, dropped) of the solution being searched; None = no checkpoints
        self.ckpts = None   # [VRPDEADLINE1] shared checkpoint list (set by solve_plan)
        self.rep = [0, 0]   # [VRPREPAIR1] failed drops repaired: tried, feasible
        self.rep_day = True  # [VRPREPAIR3] day <= REPAIR_LAST_DAY (set by solve_plan)
        self.rr = None       # [RRDEPTH1] (iters, k, resolve) set by solve_plan; None = module RR_ITERS / RR_K / RR_RESOLVE_ON
        self._jk = None      # [ROUTERJIT1] (stops snapshot, ctx array, address) of the compiled stop table
        self.rep_c = [0, 0]  # [VRPMISS1] construct repairs failed, ok
        self.crep = False    # [VRPMISS1] construct misses go to _repair (ROUTE_VRP_MISS_ON retry of an unsolved day only)

    def _jctx(self):
        """[ROUTERJIT1] address of the int32 stop table for the kernels (rebuilt when the stop list changes: fill /
        sliver append and pop stops); None = not representable (the Python path is used)."""
        st = self.stops; n = len(st); jk = self._jk
        if jk is not None and len(jk[0]) == n and (n == 0 or jk[0][-1] is st[-1]):
            return jk[2]
        B = self.B; items = {}
        for s_ in st:
            for k in s_.need:
                items.setdefault(k, len(items))
            for k in s_.give:
                items.setdefault(k, len(items))
        iav = B["item_av"]
        for k in iav:
            items.setdefault(k, len(items))
        ni = len(items); addr = None
        try:
            if ni <= _JMAXI:
                av = [2] * ni
                for k, i in items.items():
                    av[i] = iav.get(k, 2)
                head = [n, ni, B["end"], 0] + av
                base = len(head) + 9 * n; rows = []; ent = []
                for s_ in st:
                    nd = [(items[k], v) for k, v in s_.need.items()]; gv = [(items[k], v) for k, v in s_.give.items()]
                    x, y = s_.tile
                    rows += [x, y, s_.early, s_.late, s_.dur, base + len(ent), len(nd), base + len(ent) + 2 * len(nd), len(gv)]
                    for kv in nd + gv:
                        ent += kv
                vals = head + rows + ent
                if all(type(v) is int for v in vals):
                    arr = array("i", vals)
                    addr = arr.buffer_info()[0]
        except (OverflowError, TypeError, ValueError):
            addr = None
        if addr is None:
            arr = None
        self._jk = (tuple(st), arr, addr)
        return addr

    def ev(self, u, r):
        key = (u, tuple(r))
        v = self.cache.get(key)
        if v is None and key not in self.cache:
            B = self.B
            cx = self._jctx() if _JL is not None and JIT_ON and len(r) <= _JMAXR else None
            if cx is not None:
                sp = B["sp"][u]; a = array("i", r)
                if _JL.rv_eval(cx, a.buffer_info()[0], len(r), sp[0], sp[1], B["start"][u], _JOA):
                    o = _JO; v = (o[0], o[1], o[2], None if o[3] < 0 else o[3], o[4], o[5])
            else:
                v = route_eval(r, B["sp"][u], B["start"][u], B["item_av"], B["end"], self.stops)
            self.cache[key] = v
        return v

    def _jbest_insert(self, routes, j, units):
        """[ROUTERJIT1] best_insert on the kernel; None = not representable (Python path)."""
        cx = self._jctx()
        if cx is None or len(units) > _JMAXU or not 1 <= INSERT_K <= 64:
            return None
        sp = self.B["sp"]; st = self.B["start"]
        q = [j, len(units), INSERT_K]; nc = 0
        for u in units:
            r = routes[u]; p = sp[u]; n = len(r)
            if n >= _JMAXR or u >= 4000:
                return None
            nc += n + 1
            q += (u, p[0], p[1], st[u], n); q += r
        if nc > _JMAXC:
            return None
        a = array("i", q)
        _JL.rv_best_insert(cx, a.buffer_info()[0], _JCA, _JIA)
        u = _JI[0]
        return (INF, None, None) if u < 0 else (_JC[0], u, _JI[1])

    def cost(self, v):
        return INF if v is None else route_key(v[0], v[1])

    def rcost(self, u, r):
        if not r:
            return 0.0
        v = self.ev(u, r)
        return INF if v is None else route_key(v[0] - self.B["start"][u], v[1])

    def _ckpt(self, routes):
        """[VRPDEADLINE1] record a complete solution of the current context (crew + dropped hires) with the spawns
        it was evaluated under; on the deadline apply() restores the best (sol_key: crew bill, then route cost; ties latest)
        one VERIFY accepts."""
        ctx = self.ctx
        if ctx is None or self.ckpts is None:
            return
        units, dropped = ctx
        if any(routes.get(u) and self.ev(u, routes[u]) is None for u in units):
            return
        ck = dict(S=self, routes={u: list(routes.get(u, [])) for u in units}, units=list(units),
                  dropped=list(dropped), sp=dict(self.B["sp"]), nst=len(self.stops),
                  key=sol_key(dropped, sum(self.rcost(u, routes.get(u, [])) for u in units)))
        if self.ckpts:
            last = self.ckpts[-1]
            if all(last[k] == ck[k] for k in ("routes", "units", "dropped", "sp", "nst")) and last["S"] is self:
                return
        self.ckpts.append(ck)

    def _jinsert_seq(self, routes, seq, units, stop_on_fail):
        """[ROUTERJIT1] the sequential best_insert loops on one kernel call: every stop of seq in order to its
        best_insert slot. None = not representable (Python path); else (complete, routes, costs, miss): costs are
        Solver.rcost of each unit's final route (0.0 empty, INF infeasible), routes a new dict in units order."""
        cx = self._jctx()
        if cx is None or len(units) > _JMAXU or not 1 <= INSERT_K <= 64:
            return None
        sp = self.B["sp"]; st = self.B["start"]
        q = [0, len(units), INSERT_K]; nc = len(seq)
        for u in units:
            r = routes[u]; p = sp[u]; n = len(r)
            if u >= 4000:
                return None
            nc += n + 1
            q += (u, p[0], p[1], st[u], n); q += r
        if nc > _JMAXC:
            return None
        a = array("i", q); b = array("i", seq)
        ok = _JL.rv_insert_seq(cx, a.buffer_info()[0], b.buffer_info()[0], len(seq), 1 if stop_on_fail else 0, _JBA, _JDA)
        if ok < 0:
            return None
        if ok == 0:
            return (False, None, None, None)
        o = _JB; nm = o[0]; miss = o[1:1 + nm]; k = 1 + nm; out = {}; costs = []; d = _JD
        for i, u in enumerate(units):
            n = o[k]; out[u] = o[k + 1:k + 1 + n]; k += 1 + n
            c = d[i]
            costs.append(INF if c >= INF / 2 else c)
        return (True, out, costs, miss)

    def best_insert(self, routes, j, units):
        _check()
        if _JL is not None and JIT_ON:
            b = self._jbest_insert(routes, j, units)
            if b is not None:
                return b
        stops = self.stops; jx, jy = stops[j].tile; sp = self.B["sp"]
        cand = []
        for u in units:
            r = routes[u]; px, py = sp[u]
            for pos in range(len(r) + 1):
                d1 = abs(px - jx) + abs(py - jy)
                if pos < len(r):
                    nx, ny = stops[r[pos]].tile
                    det = d1 + abs(jx - nx) + abs(jy - ny) - abs(px - nx) - abs(py - ny)
                    cand.append((det, u, pos))
                    px, py = nx, ny
                else:
                    cand.append((d1, u, pos))
        cand.sort()
        best = (INF, None, None); base = {}
        for det, u, pos in cand[:INSERT_K]:
            r = routes[u]
            if u not in base:
                base[u] = self.rcost(u, r)
            c = self.rcost(u, r[:pos] + [j] + r[pos:]) - base[u]
            if c < best[0] and c < INF / 2:
                best = (c, u, pos)
        if best[1] is None and len(cand) > INSERT_K:   # tight windows: fall back to the full scan
            for det, u, pos in cand[INSERT_K:]:
                r = routes[u]
                if u not in base:
                    base[u] = self.rcost(u, r)
                c = self.rcost(u, r[:pos] + [j] + r[pos:]) - base[u]
                if c < best[0] and c < INF / 2:
                    best = (c, u, pos)
        return best

    def construct(self, units):
        routes, miss = self._construct(units)
        if miss and self.crep and all(j >= 0 for j in miss):   # [VRPMISS1] regret-2 + ejection repair of the unplaced stops
            r2 = self._repair({u: list(routes[u]) for u in units}, list(miss), list(units), _DEADLINE[0])
            if r2 is not None:
                self.rep_c[1] += 1
                return r2, []
            self.rep_c[0] += 1
        return routes, miss

    def _construct(self, units):
        routes = {u: [] for u in units}
        order = sorted((j for j in range(len(self.stops)) if j not in self.skip), key=lambda j: (self.stops[j].late, min(self.stops[j].hours), -self.stops[j].dur))
        miss = []
        if _JL is not None and JIT_ON and order:
            _check()
            res = self._jinsert_seq(routes, order, units, False)
            if res is not None:
                return res[1], res[3]
        for j in order:
            c, u, pos = self.best_insert(routes, j, units)
            if u is None or c >= INF / 2:
                miss.append(j); continue
            routes[u].insert(pos, j)
        return routes, miss

    def improve(self, routes, units, t_end):
        improved = True
        while improved:
            improved = False
            for u in units:
                for j in list(routes[u]):
                    r = routes[u]; i = r.index(j)
                    rem = r[:i] + r[i + 1:]
                    gain = self.rcost(u, r) - self.rcost(u, rem)
                    routes[u] = rem
                    c, v, pos = self.best_insert(routes, j, units)
                    if v is not None and c < gain - 1e-9:
                        routes[v].insert(pos, j); improved = True
                    else:
                        routes[u] = r
            # intra 2-opt
            jit = _JL is not None and JIT_ON
            for u in units:
                r = routes[u]; n = len(r)
                if jit and n < _JMAXR:
                    cx = self._jctx()
                    if cx is not None:   # [ROUTERJIT1] the same first-improvement scan on the kernel
                        if n >= 2:
                            _check()
                            a = array("i", r); p = self.B["sp"][u]
                            if _JL.rv_two_opt(cx, a.buffer_info()[0], n, p[0], p[1], self.B["start"][u], _JCA):
                                routes[u] = a.tolist(); improved = True
                        continue
                bc = self.rcost(u, r)
                for a in range(n - 1):
                    _check()
                    for b in range(a + 1, n):
                        r2 = r[:a] + r[a:b + 1][::-1] + r[b + 1:]
                        c2 = self.rcost(u, r2)
                        if c2 < bc - 1e-9:
                            r, bc = r2, c2; improved = True
                routes[u] = r
            self._ckpt(routes)
        return routes

    def solve(self, units=None, init=None):
        units = self.units if units is None else units
        routes, miss = self._solve(units, init)
        if miss:
            return routes, miss
        routes, ok = self.fix_spawns(routes, units)
        return routes, ([] if ok else [-2])

    def fix_spawns(self, routes, units):
        fix = self.seqsp
        for it in range(5):
            _check()
            sp = (true_spawns_seq if fix else true_spawns)(self.B, self, routes, units)
            if sp.pop("_fzbad", False):
                return routes, False
            chk = list(units) + (sorted(self.B["frozen"]) if _sw("ROUTE_VRP_FIX_FROZEN") else [])
            if all(sp[u] == self.B["sp"][u] for u in chk):
                return routes, True
            self.B["sp"] = sp; self.cache = {}
            if fix and all(self.ev(u, routes[u]) is not None for u in units if routes[u]):
                return routes, True   # [ROUTEOPT2] sequential spawns are a fixed point of these routes
            if all(self.ev(u, routes[u]) is not None for u in units if routes[u]):
                routes = self.improve(routes, units, time.time() + self.budget / 4)
            else:
                routes, miss = self._solve(units, None)
                if miss:
                    return routes, False
        return routes, False

    def _solve(self, units=None, init=None):
        _check()
        t_end = time.time() + self.budget   # [VRPDEADLINE1] only RR_ITERS=None (research) reads it; the shipped bound is _DEADLINE
        routes = miss = None
        if init is not None and all(self.ev(u, init.get(u, [])) is not None for u in units if init.get(u)):
            routes = {u: list(init.get(u, [])) for u in units}; miss = []
        if routes is None:
            routes, miss = self.construct(units)
            if miss and init is not None:
                routes = {u: list(init.get(u, [])) for u in units}; miss = [-1]
                return routes, miss
        if not miss:
            self._ckpt(routes)
        routes = self.improve(routes, units, t_end)
        if not miss:
            routes = self.ruin_recreate(routes, units, t_end)
        return routes, miss

    def total(self, routes, units):
        return sum(self.rcost(u, routes[u]) for u in units)

    def ruin_recreate(self, routes, units, t_end, k=None, seed=0):
        iters, k0, _ = self.rr if self.rr is not None else (RR_ITERS, RR_K, RR_RESOLVE_ON)
        k = k0 if k is None else k
        rng = np.random.default_rng(seed)
        n = len(self.stops)
        if n < 3:
            return routes
        P = np.array([st.tile for st in self.stops])
        best = {u: list(routes[u]) for u in units}; bc = self.total(best, units)
        cur, cc = best, bc
        it = 0
        wall = _rr_wall() is not None and iters is not None and iters > _RR_SHIP[0]
        while (it < iters) if iters is not None else (time.time() < t_end):   # research knob None: time budget
            _check()
            if wall and it >= _RR_SHIP[0] and not _deep_ok():   # [RRSPEED1] past the wall: stop at the shipped 30
                break
            it += 1
            c0 = int(rng.integers(n)); kk = int(rng.integers(3, k + 1))
            near = np.argsort(np.abs(P - P[c0]).sum(1) + rng.random(n) * 0.5)[:kk]
            rem = set(int(x) for x in near if int(x) not in self.skip)
            r2 = {u: [j for j in cur[u] if j not in rem] for u in units}
            ok = True
            order = sorted(rem, key=lambda j: (self.stops[j].late, rng.random()))
            res = None
            if _JL is not None and JIT_ON and order:   # [ROUTERJIT1] one kernel call for the whole re-insertion
                _check()
                res = self._jinsert_seq(r2, order, units, True)
            if res is not None:
                if not res[0]:
                    continue
                r2 = res[1]; c2 = sum(res[2])
            else:
                for j in order:
                    c, v, pos = self.best_insert(r2, j, units)
                    if v is None or c >= INF / 2:
                        ok = False; break
                    r2[v].insert(pos, j)
                if not ok:
                    continue
                c2 = self.total(r2, units)
            if c2 < cc - 1e-9 or rng.random() < 0.02:
                cur, cc = r2, c2
                if c2 < bc - 1e-9:
                    best, bc = {u: list(r2[u]) for u in units}, c2
                    self._ckpt(best)
        ITERS_LOG.append(it)
        return best

    def metrics(self, routes):
        mv = wt = used = 0
        for u, r in routes.items():
            if not r:
                continue
            v = self.ev(u, r)
            used += v[0] - self.B["start"][u]; mv += v[1]; wt += v[2]
        return dict(moves=mv, waits=wt, used=used)

    def mode2(self, routes):
        if OPT_USE and getattr(_P, "ROUTE_VRP_OPT_ON", False) and any(st.opt for st in self.stops):
            return self.mode2_opt(routes)
        return self.mode2_ii(routes)

    def mode2_opt(self, routes):
        """[ROUTEOPT2] mode ii, but a hand whose mandatory stops fit the others is dropped also when the optional
        (tail filler) stops that no longer fit are worth less than its hire (fib)."""
        units = list(self.units); dropped = []; self.left = []
        hired = sorted([u for u in units if u != 0], key=lambda u: -u)
        stops = self.stops
        for u in hired:
            if u != max(x for x in units if x != 0) or any(f > u for f in self.B["frozen"]):
                break
            trial = [x for x in units if x != u]
            r2 = {x: list(routes[x]) for x in trial}
            ok = True
            for j in routes[u]:
                c, v, pos = self.best_insert(r2, j, trial)
                if v is None or c >= INF / 2:
                    ok = False; break
                r2[v].insert(pos, j)
            new_left = []
            if not ok:
                opts = sorted((j for x in units for j in routes[x] if stops[j].opt),
                              key=lambda j: (-stops[j].val, j))
                r2 = {x: [j for j in routes[x] if not stops[j].opt] for x in trial}
                ok = True
                for j in routes[u]:
                    if stops[j].opt:
                        continue
                    c, v, pos = self.best_insert(r2, j, trial)
                    if v is None or c >= INF / 2:
                        ok = False; break
                    r2[v].insert(pos, j)
                if not ok:
                    break
                for j in opts:
                    c, v, pos = self.best_insert(r2, j, trial)
                    if v is None or c >= INF / 2:
                        new_left.append(j); continue
                    r2[v].insert(pos, j)
                if sum(stops[j].val for j in new_left) >= FIB[u - 1] * float(OPT_COST_W):
                    break
            skip0 = set(self.skip)
            self.skip |= set(new_left)
            ctx0 = self.ctx; self.ctx = None   # optional stops left undone: VERIFY needs _OPT_LEFT, no checkpoint
            r2 = self.improve(r2, trial, time.time() + self.budget / 4)
            r2 = self.ruin_recreate(r2, trial, time.time() + self.budget / 2)
            sp0 = dict(self.B["sp"])
            r2, ok = self.fix_spawns(r2, trial)
            self.ctx = ctx0
            if not ok:
                self.B["sp"] = sp0; self.cache = {}; self.skip = skip0
                break
            units = trial; routes = r2; dropped.append(u); self.left += new_left
        return routes, units, dropped

    def mode2_ii(self, routes):
        """Greedy crew reduction (a heuristic, not a proven minimum crew): drop hands from the last hired down while
        every stop still fits (no unfinished tasks); the first drop that fails ends the reduction. [VRPREPAIR1] under
        ROUTE_VRP_REPAIR_ON a failed drop first gets a bounded repair (_repair: regret-2 re-insertion of the dropped
        hand's stops + 1-step ejection chain) before the reduction stops."""
        units = list(self.units); dropped = []
        hired = sorted([u for u in units if u != 0], key=lambda u: -u)
        for u in hired:
            if u != max(x for x in units if x != 0) or any(f > u for f in self.B["frozen"]):
                break
            trial = [x for x in units if x != u]
            r2 = {x: list(routes[x]) for x in trial}
            ok = True
            res = None
            if _JL is not None and JIT_ON and routes[u]:   # [ROUTERJIT1]
                _check()
                res = self._jinsert_seq(r2, routes[u], trial, True)
            if res is not None:
                ok = res[0]
                if ok:
                    r2 = res[1]
            else:
                for j in routes[u]:
                    c, v, pos = self.best_insert(r2, j, trial)
                    if v is None or c >= INF / 2:
                        ok = False; break
                    r2[v].insert(pos, j)
            if not ok:
                if not (routes[u] and _sw("ROUTE_VRP_REPAIR_ON") and self.rep_day):
                    break
                self.rep[0] += 1
                r2 = self._repair({x: routes[x] for x in trial}, routes[u], trial, _CLOCK() + REPAIR_MS / 1000.0)
                if r2 is None:
                    break
                self.rep[1] += 1
            ctx0 = self.ctx
            if ctx0 is not None:
                self.ctx = (trial, dropped + [u]); self._ckpt(r2)
            try:
                r2 = self.improve(r2, trial, time.time() + self.budget / 4)
                r2 = self.ruin_recreate(r2, trial, time.time() + self.budget / 2)
                sp0 = dict(self.B["sp"])
                r2, ok = self.fix_spawns(r2, trial)
            finally:
                self.ctx = ctx0
            if not ok:
                self.B["sp"] = sp0; self.cache = {}
                break
            units = trial; routes = r2; dropped.append(u)
            if ctx0 is not None:
                self.ctx = (units, list(dropped))
        if (self.rr if self.rr is not None else (0, 0, RR_RESOLVE_ON))[2] and _deep_ok():   # [RRSPEED1] wall gate
            routes, units, dropped = self._resolve_drop(routes, units, dropped)
        return routes, units, dropped

    def _resolve_drop(self, routes, units, dropped):
        """[RRDEPTH1] after the greedy reduction (ROUTERAUDIT1 rrmid arm): keep dropping the last hire while a full
        re-solve of the smaller crew from scratch places every stop; the first failure ends it."""
        while _deep_ok():   # [RRSPEED1] RR_WALL_S None: always True (RRDEPTH1 loop unchanged)
            hired = [u for u in units if u != 0]
            if not hired or any(f > max(hired) for f in self.B["frozen"]):
                break
            u = max(hired); trial = [x for x in units if x != u]
            sp0 = dict(self.B["sp"]); ctx0 = self.ctx
            if ctx0 is not None:
                self.ctx = (trial, dropped + [u])
            try:
                r2, miss = self._solve(trial, None)
                ok = not miss
                if ok:
                    r2, ok = self.fix_spawns(r2, trial)
            finally:
                self.ctx = ctx0
            if not ok:
                self.B["sp"] = sp0; self.cache = {}; break
            units = trial; routes = r2; dropped.append(u)
            if ctx0 is not None:
                self.ctx = (units, list(dropped))
        return routes, units, dropped

    def _unit_best(self, routes, j, u):
        """[VRPREPAIR1] exact cheapest feasible position of stop j in hand u's route: (delta cost, pos) / (INF, None).
        The new route itself must be feasible (a base route made infeasible by an ejection is never repaired)."""
        r = routes[u]; base = self.rcost(u, r); best = (INF, None)
        if base >= INF / 2:
            return best
        for pos in range(len(r) + 1):
            c = self.rcost(u, r[:pos] + [j] + r[pos:])
            if c < INF / 2 and c - base < best[0]:
                best = (c - base, pos)
        return best

    def _eject(self, r2, j, trial, t_lim):
        """[VRPREPAIR1] 1-step ejection chain for a stop j no hand can take: move one stop k of hand v (the
        REPAIR_EJECT_K of v's stops nearest j) to its cheapest feasible slot anywhere so j fits in v. Cheapest total."""
        stops = self.stops; jt = stops[j].tile; best = None
        for v in trial:
            rv = r2[v]; base_v = self.rcost(v, rv)
            for k in sorted(rv, key=lambda k: (dist(stops[k].tile, jt), k))[:REPAIR_EJECT_K]:
                _check()
                if _CLOCK() > t_lim:
                    return best
                i = rv.index(k); tmp = dict(r2); tmp[v] = rv[:i] + rv[i + 1:]
                cj, pj = self._unit_best(tmp, j, v)
                if pj is None:
                    continue
                tmp[v] = tmp[v][:pj] + [j] + tmp[v][pj:]
                dv = self.rcost(v, tmp[v]) - base_v
                for w in trial:
                    ck, pk = self._unit_best(tmp, k, w)
                    if pk is not None and (best is None or dv + ck < best[0]):
                        best = (dv + ck, v, list(tmp[v]), w, pk, k)
        return best

    def _repair(self, base, pend, trial, t_lim):
        """[VRPREPAIR1] bounded repair of a failed crew drop: re-insert the dropped hand's stops pend into the other
        hands' routes base by regret-2 order (the stop whose best and second-best hands differ most goes first); a
        stop with no feasible slot gets one ejection chain (_eject). Returns the routes or None (no fit / t_lim)."""
        r2 = {x: list(base[x]) for x in trial}
        pend = list(pend)
        tab = {j: {u: self._unit_best(r2, j, u) for u in trial} for j in pend}
        while pend:
            _check()
            if _CLOCK() > t_lim:
                return None
            pick = None
            for j in pend:
                cs = sorted(c for c, p in tab[j].values() if p is not None)
                if not cs:
                    pick = (0, 0, 0, j, False); break
                key = ((cs[1] - cs[0]) if len(cs) > 1 else INF, -cs[0], -j)
                if pick is None or key > pick[:3]:
                    pick = key + (j, True)
            j = pick[3]
            if pick[4]:
                u = min((u for u in trial if tab[j][u][1] is not None), key=lambda u: (tab[j][u][0], u))
                r2[u].insert(tab[j][u][1], j); ch = {u}
            else:
                e = self._eject(r2, j, trial, t_lim)
                if e is None:
                    return None
                _, v, rv, w, pk, k = e
                r2[v] = rv; r2[w] = r2[w][:pk] + [k] + r2[w][pk:]; ch = {v, w}
            pend.remove(j)
            for q in pend:
                for u in ch:
                    tab[q][u] = self._unit_best(r2, q, u)
        return r2


REPAIR_MS = 100      # [VRPREPAIR1] wall budget (ms) of one failed-drop repair (also bounded by the apply() deadline)
REPAIR_EJECT_K = 4   # [VRPREPAIR1] stops per hand (nearest the unplaced stop) tried as the ejected stop
REPAIR_LAST_DAY = 20  # [VRPREPAIR3] repair only on days <= this (29 = every day; later days keep the plain greedy drop); SHIP_VRP5 = 20


def timeline(B, stops, u, r, v):
    """per-hour state list for unit u: 'm' move, 'w' work, 'i' idle (wait or after finish / before start)."""
    end = B["end"]; tl = ["i"] * end
    t0 = B["start"][u]; pi, nk, pav = v[3], v[4], v[5]
    t = t0; p = B["sp"][u]
    for i in range(len(r) + 1):
        if pi is not None and i == pi:
            nxt = stops[r[i]].tile if i < len(r) else p
            a = min(ACC, key=lambda q: dist(p, q) + dist(q, nxt))
            for k in range(dist(p, a)):
                tl[t] = "m"; t += 1
            t = max(t, pav)
            for k in range(nk):
                tl[t] = "w"; t += 1
            p = a
        if i == len(r):
            break
        st = stops[r[i]]
        for k in range(dist(p, st.tile)):
            tl[t] = "m"; t += 1
        t = max(t, st.early)
        for k in range(st.dur):
            tl[t] = "w"; t += 1
        p = st.tile
    for h in range(0, t0):
        tl[h] = "-"
    return tl


def positions(B, stops, u, r, v):
    """position of unit u at the END of each hour h (after its action), hours start..end-1."""
    end = B["end"]; t0 = B["start"][u]; p = B["sp"][u]
    pos = [None] * end
    t = t0
    if not r:
        for h in range(t0, end): pos[h] = p
        return pos
    pi, nk, pav = v[3], v[4], v[5]
    def step_to(p, q, t):
        x, y = p
        while (x, y) != tuple(q):
            if x != q[0]: x += 1 if q[0] > x else -1
            else: y += 1 if q[1] > y else -1
            pos[t] = (x, y); t += 1
        return (x, y), t
    def stay(p, t, n):
        for k in range(n):
            if t < end: pos[t] = p
            t += 1
        return t
    for i in range(len(r) + 1):
        if pi is not None and i == pi:
            nxt = stops[r[i]].tile if i < len(r) else p
            a = min(ACC, key=lambda q: dist(p, q) + dist(q, nxt))
            p, t = step_to(p, a, t)
            if t < pav: t = stay(p, t, pav - t)
            t = stay(p, t, nk)
        if i == len(r): break
        st = stops[r[i]]
        p, t = step_to(p, st.tile, t)
        if t < st.early: t = stay(p, t, st.early - t)
        t = stay(p, t, st.dur)
    while t < end:
        pos[t] = p; t += 1
    return pos


def true_spawns(B, S, routes, units):
    """engine spawn rule on the solver's own positions (E:533-541)."""
    fz = set(B["frozen"]) if _sw("ROUTE_VRP_FIX_FROZEN") else set()
    allu = sorted(set(units) | fz)
    hires = sorted([u for u in allu if u != 0], key=lambda u: (B["hire_h"][u], u))
    sp = dict(B["sp"]); cache = {}
    for u in hires:
        hh = B["hire_h"][u]
        occ = [0, 0, 0, 0]
        for w in allu:
            if w == u or (w != 0 and (B["hire_h"][w], w) >= (hh, u)):
                continue
            if w != 0 and B["hire_h"][w] == hh:
                p = sp[w]
            elif w in fz:
                p = B["fz_pos"][w][hh]
            else:
                key = w
                if key not in cache:
                    r = routes.get(w, [])
                    v = S.ev(w, r) if r else None
                    if r and v is None:
                        r = []
                    cache[key] = positions(B, S.stops, w, r, v)
                p = cache[key][hh]
            if p in ACC:
                occ[ACC.index(p)] += 1
        sp[u] = ACC[int(np.argmin(occ))]
    return sp


def _planner_pos(hrs, last):
    """{unit: {h: position at the end of hour h}} on the planner's own table."""
    pos = {0: ACC[0]}; out = collections.defaultdict(dict)
    for h in range(last + 1):
        act = hrs.get(h)
        if act is None:
            continue
        units = [act["farmer"]] + act["hands"]
        for u, a in enumerate(units):
            if u in pos and a[0] in MV:
                dx, dy = MV[a[0]]; x, y = pos[u]; nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    pos[u] = (nx, ny)
        for m in act["market"]:
            if m[0] == "HIRE":
                occ = [sum(1 for p in pos.values() if p == t) for t in ACC]
                pos[len(pos)] = ACC[int(np.argmin(occ))]
        for u, p in pos.items():
            out[u][h] = p
    return out


def true_spawns_seq(B, S, routes, units):
    """[ROUTEOPT2] engine spawn rule, hires in engine order, each earlier unit's positions evaluated with its OWN
    new spawn: for fixed routes the result is a fixed point (recomputing it returns the same spawns)."""
    hires = sorted([u for u in units if u != 0], key=lambda u: (B["hire_h"][u], u))
    sp = dict(B["sp"]); B2 = dict(B); B2["sp"] = sp
    cache = {}

    def pos_of(w):
        if w not in cache:
            r = routes.get(w, [])
            v = route_eval(r, sp[w], B["start"][w], B["item_av"], B["end"], S.stops) if r else None
            if r and v is None:
                r = []
            cache[w] = positions(B2, S.stops, w, r, v)
        return cache[w]
    fz = sorted(B["frozen"])
    if fz:
        pp = _planner_pos(B["hrs"], B["end"] - 1)
        hires = sorted(hires + [u for u in fz if u != 0], key=lambda u: (B["hire_h"][u], u))
    for u in hires:
        hh = B["hire_h"][u]
        occ = [0, 0, 0, 0]
        for w in list(units) + fz:
            if w == u or (w != 0 and (B["hire_h"][w], w) >= (hh, u)):
                continue
            if w in B["frozen"]:
                p = pp.get(w, {}).get(hh)
            else:
                p = sp[w] if (w != 0 and B["hire_h"][w] == hh) else pos_of(w)[hh]
            if p in ACC:
                occ[ACC.index(p)] += 1
        s_u = ACC[int(np.argmin(occ))]
        if u in B["frozen"]:
            if s_u != B["sp0"][u]:
                sp["_fzbad"] = True   # a frozen hand would spawn elsewhere: its planner rows would walk off
            continue
        sp[u] = s_u
    return sp


# ---------------------------------------------------------------- write-back

INV = {v: k for k, v in render._UNIT_SIMPLE.items()}
INV["COLLECT_FERTILIZER"] = O.OP_COLLECT_FERT


def encode(a):
    k = a[0]
    if k == "PLANT":
        return O.OP_PLANT, spec.CROPS.index(a[1]), 0
    if k == "PICKUP":
        return O.OP_PICKUP, spec.ITEMS.index(a[1]), int(a[2])
    if k == "PLACE":
        return O.OP_PLACE, spec.ITEMS.index(a[1]), int(a[2])
    return INV[k], 0, 0


def plan_hours(plan, last):
    MU = plan[0].shape[0]
    return {h: render.turn_action(plan, h, MU - 1) for h in range(last + 1)}


def solve_plan(plan, obs, day, mode, budget=1.5, stats=None, fstate=None, ckpts=None):
    if day >= spec.N_DAYS - 1:
        return 0  # d29: no dusk dump before the end; ENDROUTE drop + sale rows stay the planner's
    last = 23 if day < spec.N_DAYS - 1 else 22
    hrs = plan_hours(plan, last)
    B = build(hrs, obs, day, last, plan[1] if getattr(_P, "ROUTE_VRP_OPT_ON", False) else None)
    S = Solver(B, budget); S.rep_day = day <= REPAIR_LAST_DAY; S.rr = _rr_knobs(day)
    if ckpts is not None:
        S.ckpts = ckpts; S.ctx = (list(S.units), [])
    pr = collections.defaultdict(list)
    for j, st in enumerate(S.stops):
        pr[min(st.units)].append((min(st.hours), j))
    init = {u: [j for _, j in sorted(pr.get(u, []))] for u in S.units}
    routes, miss = S.solve(init=init)
    if miss and getattr(_P, "ROUTE_VRP_FIX_ON", False):
        B, S, routes, miss = _retry_frozen(hrs, obs, day, last, budget, plan, B, S, miss, stats, ckpts=ckpts)
    if miss and getattr(_P, "ROUTE_VRP_MISS_ON", False):   # [SWITCH, VRPMISS1] the day is still unsolved
        B, S, routes, miss = _miss_retry(hrs, obs, day, last, budget, plan, B, S, miss, stats, ckpts)
    if miss:
        if stats is not None: stats["miss"] = stats.get("miss", 0) + 1
        return 0
    units = S.units; dropped = []
    fmode = str(getattr(_P, "ROUTE_FILL_MODE", "ii"))
    fills = []
    if fmode != "ii":
        S.ctx = None   # [VRPDEADLINE1] fill modes: only the pre-fill solutions are checkpoints
    if fmode in ("i_fill", "hybrid") and mode == 2:
        routes, fills = fill(S, B, routes, obs, day, plan, fstate, stats)
        if fmode == "hybrid":
            routes, units, dropped = S.mode2(routes)
    elif fmode == "ii_fill" and mode == 2:     # drop first (full mode ii saving), then fill the (greedy) reduced crew's spare
        routes, units, dropped = S.mode2_ii(routes)
        keep = S.units; S.units = units
        try:
            routes, fills = fill(S, B, routes, obs, day, plan, fstate, stats)
        finally:
            S.units = keep
    elif mode == 2:
        routes, units, dropped = S.mode2(routes)
        if _sw("SLIVER_ON"):                    # [SWITCH, SLIVER1] fill route-end idle turns with plantings
            routes = sliver(S, B, routes, units, obs, day, plan, fstate, stats)
    if mode == 2 and _sw("EMPTY_ROUTE_UNHIRE_ON"):
        routes, units, dropped = _unhire_empty(S, routes, units, dropped, stats)
    uop, ua, uq, mop, ma, mq = plan
    for u in S.units:
        uop[u, :] = O.OP_PASS; ua[u, :] = 0; uq[u, :] = 0
    for u in units:
        r = routes.get(u, [])
        if not r:
            continue
        v = S.ev(u, r)
        _write(uop, ua, uq, u, B, S.stops, r, v)
    if dropped:
        k = len(dropped)
        for h in sorted({h for h in range(mop.shape[0])}, reverse=True):
            for s in range(mop.shape[1] - 1, -1, -1):
                if k and mop[h, s] == O.MO_HIRE:
                    mop[h, s] = O.MO_NONE; ma[h, s] = 0; mq[h, s] = 0; k -= 1
    if fills:
        _seed_rows(mop, ma, mq, fills)
    if _sw("ROUTE_VRP_NEEDS_FIX_ON") and _sw("ROUTE_VRP_NEEDS_TRIM"):
        nt = _trim_sells(plan, obs, B["hrs"], B["end"] - 1)
        if stats is not None and nt:
            stats["trim"] = stats.get("trim", 0) + nt
    for j in getattr(S, "left", []):
        for a_ in S.stops[j].ops:
            _OPT_LEFT[(S.stops[j].tile, tuple(a_))] += 1
    if stats is not None:
        for k in ("dropped", "drop_cost", "days"):
            stats.setdefault(k, 0)
        stats["fills"] = stats.get("fills", 0) + len(fills)
        if _sw("ROUTE_VRP_REPAIR_ON"):
            stats["rep_try"] = stats.get("rep_try", 0) + S.rep[0]; stats["rep_ok"] = stats.get("rep_ok", 0) + S.rep[1]
        stats["dropped"] += len(dropped); stats["drop_cost"] += sum(FIB[u - 1] for u in dropped); stats["days"] += 1
        bd = 0 if day < 10 else (1 if day < 20 else 2)
        stats["drop_b%d" % bd] = stats.get("drop_b%d" % bd, 0) + len(dropped)
        stats["cost_b%d" % bd] = stats.get("cost_b%d" % bd, 0) + sum(FIB[u - 1] for u in dropped)
        lf = getattr(S, "left", [])
        stats["n_opt"] = stats.get("n_opt", 0) + sum(1 for st in S.stops if st.opt)
        stats["opt_left_b%d" % bd] = stats.get("opt_left_b%d" % bd, 0) + len(lf)
        stats["opt_val_b%d" % bd] = stats.get("opt_val_b%d" % bd, 0) + sum(S.stops[j].val for j in lf)
    return len(dropped)


def _unhire_empty(S, routes, units, dropped, stats=None):
    """[LABOUR1] EMPTY_ROUTE_UNHIRE_ON: a kept hand with an empty final route is paid and never acts (IDLE1 (f)).
    The HIRE rows the write-back removes are the LAST ones, so the last-hired hand L is the one dropped: when L's
    own route is empty it just goes; otherwise L's route moves onto the lowest empty hand e (hired no later, so it
    starts no later) and the spawn fixed point is re-checked (fix_spawns). Any failure keeps the solution as is."""
    while True:
        hired = [u for u in units if u != 0]
        if not hired:
            break
        L = max(hired)
        if any(f > L for f in S.B["frozen"]):
            break
        empty = [u for u in hired if not routes.get(u)]
        if not empty:
            break
        trial = [x for x in units if x != L]
        r2 = {x: list(routes.get(x, [])) for x in trial}
        if L not in empty:
            e = min(empty)
            if S.B["hire_h"][e] > S.B["hire_h"][L]:
                break
            r2[e] = list(routes[L])
        sp0 = dict(S.B["sp"]); ctx0 = S.ctx
        if ctx0 is not None:
            S.ctx = (trial, dropped + [L])
        try:
            r3, ok = S.fix_spawns(r2, trial)
            ok = ok and all(S.ev(x, r3[x]) is not None for x in trial if r3.get(x))
        finally:
            S.ctx = ctx0
        if not ok:
            S.B["sp"] = sp0; S.cache = {}
            break
        units = trial; routes = r3; dropped = dropped + [L]
        if ctx0 is not None:
            S.ctx = (units, list(dropped))
        if stats is not None:
            stats["unhired"] = stats.get("unhired", 0) + 1
    return routes, units, dropped


FIX_ROUNDS = 0   # [ROUTEOPT2] freeze rounds after the same-crew sequential-spawn round


def _retry_frozen(hrs, obs, day, last, budget, plan, B, S, miss, stats, rounds=None, ckpts=None):
    """[ROUTEOPT2] a stop the search cannot place (same-tile chain merged across planner units overrunning the
    day, pickup/seed window): leave the planner units that own it on the planner's own rows (frozen) and
    re-solve the rest. Spawn failures ([-2]) retry the same way with the units the planner hired last frozen."""
    extra = set()
    rounds = FIX_ROUNDS if rounds is None else rounds
    for rd in range(rounds + 1):
        if rd == 0:
            add = set()     # round 0: same crew, sequential spawn fixed point
        elif miss == [-2] or miss == [-1]:
            cand = [u for u in B["units"] if u != 0 and u not in B["frozen"] and u not in extra]
            if not cand:
                break
            add = {max(cand)}
        else:
            add = set()
            for j in miss:
                add |= set(S.stops[j].units)
            add -= extra
            if not add:
                break
        extra |= add
        if rd > 0 and not add:
            break
        B2 = build(hrs, obs, day, last, plan[1] if getattr(_P, "ROUTE_VRP_OPT_ON", False) else None, extra)
        S2 = Solver(B2, budget); S2.seqsp = True; S2.rep_day = day <= REPAIR_LAST_DAY; S2.rr = _rr_knobs(day)
        if ckpts is not None:
            S2.ckpts = ckpts; S2.ctx = (list(S2.units), [])
        if not S2.units:
            break
        pr = collections.defaultdict(list)
        for j, st in enumerate(S2.stops):
            pr[min(st.units)].append((min(st.hours), j))
        init = {u: [j for _, j in sorted(pr.get(u, []))] for u in S2.units}
        r2, m2 = S2.solve(init=init)
        B, S, routes, miss = B2, S2, r2, m2
        if not miss:
            if stats is not None:
                stats["recovered"] = stats.get("recovered", 0) + 1
                stats["rec_frozen"] = stats.get("rec_frozen", 0) + len(extra)
            break
    return B, S, (routes if not miss else None), miss


MISS_SHIFT = 2   # [VRPMISS1] robust start shift: the 4 access tiles are a 2x2 block, so any access tile is <= 2 steps
                 # from any other; a route feasible from its planner spawn at start + 2 is feasible from ANY access tile at start
_EXTRA = [0.0]   # [VRPMISS1] extra apply() seconds granted on an unsolved day (search deadline + checkpoint-restore window)
MISSLOG = os.environ.get("KAGG3_VRP_MISSLOG", "")   # [VRPMISS1] judge counter: one line per unsolved day (day, cell, outcome)


def _mlog(day, what):
    if MISSLOG:
        with open(MISSLOG, "a") as fh:
            fh.write("%d\t%s\t%s\n" % (day, getattr(_P, "ROUTE_VRP_MISS_CELL", "M3"), what))


def _miss_cell():
    c = str(getattr(_P, "ROUTE_VRP_MISS_CELL", "M3"))
    return c in ("M1", "M3", "M4"), c in ("M2", "M3", "M4")


def _miss_retry(hrs, obs, day, last, budget, plan, B, S, miss, stats, ckpts):
    """[VRPMISS1] an unsolved day after the shipped search (+ ROUTEOPT2 retry). M1: re-solve with construct misses
    repaired (Solver._repair: regret-2 + one ejection chain); M2: spawn-ROBUST re-solve (_robust); M3 = M1 then M2;
    M4 = M3, then the partial fallback: the planner's rows kept for the last hires only (ROUTEOPT2 freeze rounds 1-2,
    frozen spawns checked), the rest routed. The apply deadline is raised by ROUTE_VRP_MISS_EXTRA_S on this day only."""
    rep, rob = _miss_cell()
    ex = float(getattr(_P, "ROUTE_VRP_MISS_EXTRA_S", 0.0) or 0.0)
    if ex > 0 and _EXTRA[0] == 0.0:
        _EXTRA[0] = ex; _DEADLINE[0] += ex
    if stats is not None:
        stats["miss_try"] = stats.get("miss_try", 0) + 1
    if rep:
        B2 = build(hrs, obs, day, last, plan[1] if getattr(_P, "ROUTE_VRP_OPT_ON", False) else None)
        S2 = Solver(B2, budget); S2.seqsp = True; S2.rep_day = day <= REPAIR_LAST_DAY; S2.rr = _rr_knobs(day)
        if ckpts is not None:
            S2.ckpts = ckpts; S2.ctx = (list(S2.units), [])
        if S2.units:
            init = _init_routes(S2)
            S2.crep = True
            try:
                r2, m2 = S2.solve(init=init)
            finally:
                S2.crep = False
            if not m2:
                if stats is not None:
                    stats["miss_rep"] = stats.get("miss_rep", 0) + 1
                _mlog(day, "rep")
                return B2, S2, r2, []
    if rob:
        out = _robust(hrs, obs, day, last, budget, plan, ckpts, rep, MISS_SHIFT)
        if out is not None:
            if stats is not None:
                stats["miss_rob"] = stats.get("miss_rob", 0) + 1
            _mlog(day, "rob")
            return out[0], out[1], out[2], []
    if str(getattr(_P, "ROUTE_VRP_MISS_CELL", "M3")) == "M4":
        B4, S4, r4, m4 = _retry_frozen(hrs, obs, day, last, budget, plan, B, S, miss, None, rounds=2, ckpts=ckpts)
        if not m4:
            if stats is not None:
                stats["miss_frz"] = stats.get("miss_frz", 0) + 1
            _mlog(day, "frz")
            return B4, S4, r4, []
    _mlog(day, "fail")
    return B, S, None, miss


def _init_routes(S):
    pr = collections.defaultdict(list)
    for j, st in enumerate(S.stops):
        pr[min(st.units)].append((min(st.hours), j))
    return {u: [j for _, j in sorted(pr.get(u, []))] for u in S.units}


def _robust(hrs, obs, day, last, budget, plan, ckpts, rep, sh):
    """[VRPMISS1] spawn-robust re-solve: every hire's route is searched from start + sh (so its engine spawn, whichever
    access tile, cannot make it late), then the true starts are restored, the sequential engine spawns computed once
    (a fixed point of the fixed routes: re-checked) and every route re-evaluated on them. None = no feasible solution."""
    B = build(hrs, obs, day, last, plan[1] if getattr(_P, "ROUTE_VRP_OPT_ON", False) else None)
    S = Solver(B, budget); S.seqsp = True; S.rep_day = day <= REPAIR_LAST_DAY; S.rr = _rr_knobs(day)
    if not S.units:
        return None
    orig = dict(B["start"])
    for u in S.units:
        if u != 0:
            B["start"][u] = orig[u] + sh
    S.cache = {}; S.crep = rep
    try:
        routes, miss = S._solve(S.units, _init_routes(S))
    finally:
        S.crep = False
        B["start"].clear(); B["start"].update(orig); S.cache = {}
    if miss:
        return None
    sp = true_spawns_seq(B, S, routes, S.units)
    if sp.pop("_fzbad", False):
        return None
    B["sp"] = sp; S.cache = {}
    if any(routes.get(u) and S.ev(u, routes[u]) is None for u in S.units):
        return None
    sp2 = true_spawns_seq(B, S, routes, S.units); sp2.pop("_fzbad", None)
    if any(sp2[u] != sp[u] for u in S.units):
        return None
    if ckpts is not None:
        S.ckpts = ckpts; S.ctx = (list(S.units), []); S._ckpt(routes)
    return B, S, routes


def _write(uop, ua, uq, u, B, stops, r, v):
    t = B["start"][u]; p = B["sp"][u]; pi, nk, pav = v[3], v[4], v[5]
    need = _needs(stops, r)

    def walk(p, q, t):
        x, y = p
        while x != q[0]:
            uop[u, t] = O.OP_EAST if q[0] > x else O.OP_WEST; x += 1 if q[0] > x else -1; t += 1
        while y != q[1]:
            uop[u, t] = O.OP_SOUTH if q[1] > y else O.OP_NORTH; y += 1 if q[1] > y else -1; t += 1
        return t
    for i in range(len(r) + 1):
        if pi is not None and i == pi:
            nxt = stops[r[i]].tile if i < len(r) else p
            a = min(ACC, key=lambda q: dist(p, q) + dist(q, nxt))
            t = walk(p, a, t); t = max(t, pav)
            for kname, qty in sorted(need.items()):
                uop[u, t], ua[u, t], uq[u, t] = O.OP_PICKUP, spec.ITEMS.index(kname), qty; t += 1
            p = a
        if i == len(r):
            break
        st = stops[r[i]]
        t = walk(p, st.tile, t); t = max(t, st.early)
        for a in st.ops:
            uop[u, t], ua[u, t], uq[u, t] = encode(a); t += 1
        p = st.tile


def _short_items(uop, ua, uq, mop, ma, mq, shed0, last):
    """engine order per hour (units by index, then market rows): per-item PICKUP shortfall + first short event."""
    shed = collections.Counter(shed0); short = collections.Counter(); first = {}
    MU = uop.shape[0]
    for h in range(last + 1):
        for u in range(MU):
            if int(uop[u, h]) == O.OP_PICKUP:
                k = spec.ITEMS[int(ua[u, h])]; q = int(uq[u, h]); got = min(q, shed[k]); shed[k] -= got
                if q > got:
                    short[k] += q - got; first.setdefault(k, h)
        for s_ in range(mop.shape[1]):
            o_ = int(mop[h, s_])
            if o_ == O.MO_SELL:
                k = spec.PRODUCTS[int(ma[h, s_])]; shed[k] -= min(int(mq[h, s_]), shed[k])
            elif o_ == O.MO_BUY_PRODUCT:
                shed[spec.PRODUCTS[int(ma[h, s_])]] += int(mq[h, s_])
    return short, first


def _trim_sells(plan, obs, hrs0, last):
    """[VRPFALLBACK1, ROUTE_VRP_NEEDS_FIX_ON] where the rewritten routes pick up more of a product than the shed
    holds after the planner's early SELL rows (the planner fed from wheat its own harvest stops carried), sell that
    many units fewer in the latest SELL row of it before the short PICKUP (the unit stays in the shed; the planner's
    harvested unit reaches the shed at dusk instead). Returns units trimmed."""
    uop, ua, uq, mop, ma, mq = plan
    base = collections.Counter(); shed0 = obs["private"]["shed"]
    sh = collections.Counter(shed0)
    for h in range(last + 1):                       # planner's own shortfall per item (same replay as _pick_short)
        act = hrs0.get(h)
        if act is None:
            continue
        for a in [act["farmer"]] + act["hands"]:
            if a[0] == "PICKUP":
                q = int(a[2]); got = min(q, sh[a[1]]); sh[a[1]] -= got; base[a[1]] += q - got
        for m in act["market"]:
            if m[0] == "SELL":
                sh[m[1]] -= min(int(m[2]), sh[m[1]])
            elif m[0] == "BUY_PRODUCT":
                sh[m[1]] += int(m[2])
    trimmed = 0
    for _ in range(12):
        short, first = _short_items(uop, ua, uq, mop, ma, mq, shed0, last)
        bad = [k for k in short if short[k] > base.get(k, 0) and k in spec.PRODUCTS]
        if not bad:
            break
        k = min(bad, key=lambda k: first[k]); h = first[k]; pi = spec.PRODUCTS.index(k)
        rows = [(hh, s_) for hh in range(h) for s_ in range(mop.shape[1])
                if int(mop[hh, s_]) == O.MO_SELL and int(ma[hh, s_]) == pi and int(mq[hh, s_]) > 0]
        if rows:
            hh, s_ = rows[-1]
            x = min(short[k] - base.get(k, 0), int(mq[hh, s_]))
            mq[hh, s_] -= x; trimmed += x
            if int(mq[hh, s_]) == 0:
                mop[hh, s_] = O.MO_NONE; ma[hh, s_] = 0
            continue
        buys = [(hh, s_) for hh in range(h) for s_ in range(mop.shape[1])
                if int(mop[hh, s_]) == O.MO_BUY_PRODUCT and int(ma[hh, s_]) == pi]
        if not buys or not BUY_TOPUP:
            break
        hh, s_ = buys[-1]                           # no sale left to trim: buy the unit the routes need in that row
        x = short[k] - base.get(k, 0)
        mq[hh, s_] += x; trimmed += x
    return trimmed


BUY_TOPUP = True


def _needs(stops, r):
    cum = collections.Counter(); mdef = collections.Counter()
    for j in r:
        st = stops[j]
        for k, v in st.need.items():
            cum[k] -= v; mdef[k] = max(mdef[k], -cum[k])
        for k, v in st.give.items():
            cum[k] += v
    return {k: v for k, v in mdef.items() if v > 0}


import os as _os
TLOG = _os.environ.get("KAGG3_VRP_TLOG", "")
OPT_USE = True      # [ROUTEOPT2] recorder override: marks on, mode ii kept
OPT_COST_W = 1.0    # optional value left must be < OPT_COST_W x fib(hand)
BUDGET = 0.7
MODE = 2


class _Shim:
    """route evaluation on a checkpoint's own spawns (the solver's cache belongs to its latest spawns)."""
    def __init__(self, B, stops):
        self.B = B; self.stops = stops

    def ev(self, u, r):
        B = self.B
        return route_eval(r, B["sp"][u], B["start"][u], B["item_av"], B["end"], self.stops)


def _restore(plan, obs, day, ck):
    """[VRPDEADLINE1] write checkpoint ck into a copy of the planner table; None unless its spawns are the engine's
    (a fixed point of its routes) and VERIFY accepts it."""
    S = ck["S"]; B = dict(S.B); B["sp"] = dict(ck["sp"]); stops = S.stops[:ck["nst"]]
    sh = _Shim(B, stops); units = ck["units"]; routes = ck["routes"]
    chk = list(units) + (sorted(B["frozen"]) if _sw("ROUTE_VRP_FIX_FROZEN") else [])
    for it in range(RESTORE_SPAWN_IT + 1):     # the routes kept, spawns settled to the engine's (fix_spawns sans search)
        vs = {}
        for u in units:
            if routes.get(u):
                vs[u] = sh.ev(u, routes[u])
                if vs[u] is None:
                    return None
        sp = (true_spawns_seq if S.seqsp else true_spawns)(B, sh, routes, units)
        if sp.pop("_fzbad", False):
            return None
        if all(sp[u] == B["sp"][u] for u in chk):
            break
        if it == RESTORE_SPAWN_IT:
            return None
        B["sp"] = sp
    new = tuple(np.array(x) for x in plan)
    uop, ua, uq, mop, ma, mq = new
    for u in S.units:
        uop[u, :] = O.OP_PASS; ua[u, :] = 0; uq[u, :] = 0
    for u in units:
        if routes.get(u):
            _write(uop, ua, uq, u, B, stops, routes[u], vs[u])
    k = len(ck["dropped"])
    for h in range(mop.shape[0] - 1, -1, -1):
        for s in range(mop.shape[1] - 1, -1, -1):
            if k and mop[h, s] == O.MO_HIRE:
                mop[h, s] = O.MO_NONE; ma[h, s] = 0; mq[h, s] = 0; k -= 1
    if _sw("ROUTE_VRP_NEEDS_FIX_ON") and _sw("ROUTE_VRP_NEEDS_TRIM"):
        _trim_sells(new, obs, B["hrs"], B["end"] - 1)
    _OPT_LEFT.clear()
    return new if verify(plan, new, obs, day) else None


RESTORE_SPAWN_IT = 3   # [VRPDEADLINE1] spawn settling rounds on a restored checkpoint
CKPT_TRIES = 64   # [VRPDEADLINE1] checkpoints (latest first) tried on a timeout, each only while inside SAFETY_S (a spawn reject costs ~0.5 ms)


def apply(plan, obs, day, stats=None, fstate=None):
    """Rewrite the day's plan (numpy copies). Returns the new plan; on the safety break the last complete solution
    VERIFY accepts [VRPDEADLINE1], else the planner's own.
    fstate: per-game fill ledger [ROUTEFILL1] (dict; only committed when the day's rewrite is kept)."""
    global JIT_ON
    if getattr(_P, "ROUTE_VRP_JIT_ON", True) is False:   # [ROUTERJIT1] switch-string kill switch (Python path)
        JIT_ON = False
    new = tuple(np.array(x) for x in plan)
    _OPT_LEFT.clear()
    t0 = _T0[0] = _CLOCK()
    _DEADLINE[0] = t0 + SAFETY_S - RESERVE_S
    st0 = dict(stats) if stats is not None else None
    tmp = {"ledger": list(fstate.get("ledger", []))} if fstate is not None else None
    ckpts = []
    try:
        solve_plan(new, obs, int(day), MODE, BUDGET, stats, tmp, ckpts)
        if _sw("ROUTE_VRP_VERIFY") and not verify(plan, new, obs, int(day), (tmp or {}).get("new")):
            if stats is not None:
                stats.clear(); stats.update(st0); stats["verify_fail"] = stats.get("verify_fail", 0) + 1
            return tuple(np.array(x) for x in plan)
    except _Timeout:
        _DEADLINE[0] = float("inf")
        if stats is not None:
            stats.clear(); stats.update(st0); stats["timeout"] = stats.get("timeout", 0) + 1
        order = sorted(range(len(ckpts)), key=lambda i: (ckpts[i]["key"], -i))   # [VRPOBJ1] best sol_key first, ties latest
        for ck in [ckpts[i] for i in order][:CKPT_TRIES]:
            if _CLOCK() > t0 + SAFETY_S + _EXTRA[0]:
                break
            out = _restore(plan, obs, int(day), ck)
            if out is not None:
                if stats is not None:
                    dr = ck["dropped"]
                    stats["ckpt"] = stats.get("ckpt", 0) + 1
                    stats["dropped"] = stats.get("dropped", 0) + len(dr); stats["days"] = stats.get("days", 0) + 1
                    stats["drop_cost"] = stats.get("drop_cost", 0) + sum(FIB[u - 1] for u in dr)
                return out
        return tuple(np.array(x) for x in plan)
    finally:
        _DEADLINE[0] = float("inf"); _EXTRA[0] = 0.0
    if fstate is not None:
        fstate["ledger"] = tmp["ledger"]
        if tmp.get("new"):
            fstate.setdefault("all", []).extend(tmp["new"])
    return new


_OPT_LEFT = collections.Counter()   # [ROUTEOPT2] (tile, op) of the optional stops left undone by the last solve


def _work_ops(hrs, last):
    out = collections.Counter()
    for u, lst in parse_day(hrs, last)[2].items():
        for h, p, a in lst:
            if a[0] in ("PICKUP", "DROP") or (a[0] == "PLACE" and p in ACC and a[1] not in ANIMALS):
                out[("acc", p in ACC)] += 1
            else:
                out[(p, a)] += 1
    return out


def _pick_short(hrs, obs, last):
    """PICKUP units the shed cannot serve: unit actions first (unit order), then the hour's market rows."""
    shed = collections.Counter(obs["private"]["shed"]); short = 0
    for h in range(last + 1):
        act = hrs.get(h)
        if act is None:
            continue
        for a in [act["farmer"]] + act["hands"]:
            if a[0] == "PICKUP":
                q = int(a[2]); got = min(q, shed[a[1]]); shed[a[1]] -= got; short += q - got
        for m in act["market"]:
            if m[0] == "SELL":
                shed[m[1]] -= min(int(m[2]), shed[m[1]])
            elif m[0] == "BUY_PRODUCT":
                shed[m[1]] += int(m[2])
    return short


def verify(plan, new, obs, day, fills=None):
    """[SALEPIN1, ROUTE_VRP_VERIFY] the rewritten table, replayed under the engine spawn rule, does every planner
    (tile, op), issues no PICKUP/DROP off an access tile, and is no shorter on PICKUP stock than the planner's.
    fills [TOMATOFILL1]: the day's committed ROUTEFILL1 fills [(day, crop, tile)]; their own DIG/PLANT/WATER (one
    each on the fill tile) are the only extra ops allowed (before this, VERIFY rejected every fill day)."""
    last = 23 if day < spec.N_DAYS - 1 else 22
    h0, h1 = plan_hours(plan, last), plan_hours(new, last)
    w0, w1 = _work_ops(h0, last), _work_ops(h1, last)
    for _d, c, p in (fills or []):
        p = tuple(p)
        for a in (("DIG",), ("PLANT", c), ("WATER",)):
            if w1.get((p, a), 0) > w0.get((p, a), 0):
                w1[(p, a)] -= 1
                if not w1[(p, a)]:
                    del w1[(p, a)]
    if w1.get(("acc", False), 0) > w0.get(("acc", False), 0):
        return False
    k0 = {k: v for k, v in w0.items() if k[0] != "acc"}; k1 = {k: v for k, v in w1.items() if k[0] != "acc"}
    if _OPT_LEFT:
        # [ROUTEOPT2] only the labelled optional (tail) ops the solver chose to leave may be missing
        if any(v > k0.get(k, 0) for k, v in k1.items()):
            return False
        if any(k0[k] - k1.get(k, 0) > _OPT_LEFT.get(k, 0) for k in k0):
            return False
        return _pick_short(h1, obs, last) <= _pick_short(h0, obs, last)
    if k0 != k1:
        return False
    return _pick_short(h1, obs, last) <= _pick_short(h0, obs, last)


# ---------------------------------------------------------------- ROUTEFILL1: fill the freed turns with plantings
from ..core import plan as _P  # noqa: E402
from . import overflow as _OV  # noqa: E402  [ROUTEOPT2] eager: the engine harness drops kagg3 from sys.modules mid-game

LIFE = {"WHEAT": 4, "CARROT": 3, "TOMATO": 10}   # max_yield_day: harvest day = plant day + LIFE
# [TOMATOFILL1] tomato (ongoing, first yield age 8, 4 productions at ages 8-11 -> nights pd+7..pd+10): LIFE 10 keeps
# every fill planted <= d18 through its 4th production night (<= d28); its later-day tend adds fert + harvest turns
EXTRA = {"TOMATO": 1.0}


def _fill_load(fills, d, tend):
    """expected turns the ledger's fill plantings need on day d (water + move; harvest day +1)."""
    n = 0.0
    for pd, c, _t in fills:
        L = LIFE[c]
        if pd < d <= pd + L:
            n += tend + EXTRA.get(c, 0.0) + (1 if d == pd + L else 0)
    return n


def _spare(B, S, routes, units):
    """idle unit-turns of the solved day (after each unit's start)."""
    tot = 0
    for u in units:
        r = routes.get(u, [])
        if not r:
            tot += B["end"] - B["start"][u]; continue
        v = S.ev(u, r)
        if v is None:
            continue
        tot += B["end"] - v[0] + v[2]
    return tot


def fill(S, B, routes, obs, day, plan, fstate, stats):
    """[ROUTEFILL1] admit fill plantings (PLANT + same-day WATER; DIG first on a weed tile) into the solved
    same-crew routes while (a) the solver still completes every stop inside its window and (b) the ledger of fill
    plantings alive on each later day of the new planting's life stays within ROUTE_FILL_FRAC x today's gross
    spare turns (spare measured on the solved routes, not the planner's estimate)."""
    d0, d1 = _P.ROUTE_FILL_DAYS
    crop = str(_P.ROUTE_FILL_CROP).upper()
    L = LIFE[crop]
    if not (d0 <= day <= min(d1, spec.N_DAYS - 2 - L)) or int(_P.ROUTE_FILL_CAP) <= 0:
        return routes, []
    ledger = [] if fstate is None else fstate.setdefault("ledger", [])
    seat = obs["player"]; tiles = obs["farms"][seat]["tiles"]
    # keep ledger entries whose tile still carries that planting
    alive = []
    for pd, c, t in ledger:
        x = tiles[t[1]][t[0]]
        if isinstance(x, dict) and x.get("kind") == "PLANT" and x.get("crop") == c and int(x.get("planted_day", -1)) == pd:
            alive.append((pd, c, t))
    ledger[:] = alive
    units = S.units
    tend = float(_P.ROUTE_FILL_TEND)
    gross = _spare(B, S, routes, units) + _fill_load(alive, day, tend)
    cap_turns = float(_P.ROUTE_FILL_FRAC) * gross
    busy = {st.tile for st in S.stops}
    for u, lst in B["fz_ops"].items():
        busy |= {p for _h, p, _a in lst}
    cands = []
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            p = (x, y); t = tiles[y][x]
            if p in busy or p in ACC:
                continue
            if t is None:
                cands.append((dacc(p), 0, p))
            elif isinstance(t, dict) and t.get("kind") == "WEED" and _P.ROUTE_FILL_WEED:
                cands.append((dacc(p) + 1, 1, p))
    cands.sort()
    if stats is not None:
        stats["fill_call"] = stats.get("fill_call", 0) + 1
    if not cands:
        if stats is not None:
            stats["fill_nocand"] = stats.get("fill_nocand", 0) + 1
        return routes, []
    # seeds: dawn pool minus the planner's own PLANTs of the crop today
    used = sum(1 for st in S.stops for a in st.ops if a[0] == "PLANT" and a[1] == crop)
    for lst in B["fz_ops"].values():
        used += sum(1 for _h, _p, a in lst if a[0] == "PLANT" and a[1] == crop)
    have = int(obs["private"]["seeds"].get(crop, 0)) - used
    fills = []; new = []
    fut = list(alive)
    buy_row = _seed_slot(plan[3], plan[4], spec.CROPS.index(crop))
    routes0 = {u: list(r) for u, r in routes.items()}; n0 = len(S.stops); sp0 = dict(B["sp"])
    for _k, weed, p in cands[:int(_P.ROUTE_FILL_SCAN)]:
        if len(fills) >= int(_P.ROUTE_FILL_CAP):
            break
        trial = fut + [(day, crop, p)]
        if any(_fill_load(trial, dd, tend) > cap_turns for dd in range(day + 1, day + L + 1)):
            if stats is not None:
                stats["fill_capbrk"] = stats.get("fill_capbrk", 0) + 1
            break
        st = Stop(p)
        st.ops = ([("DIG",)] if weed else []) + [("PLANT", crop), ("WATER",)]
        st.dur = len(st.ops); st.hours = [23]; st.units = {0}
        buy = have - len(fills) <= 0
        if buy and buy_row is None:
            if stats is not None:
                stats["fill_seedbrk"] = stats.get("fill_seedbrk", 0) + 1
            break
        st.early = buy_row[0] + 1 if buy else 0
        S.stops.append(st); j = len(S.stops) - 1
        c, v, pos = S.best_insert(routes, j, units)
        if v is None or c >= INF / 2:
            if stats is not None:
                stats["fill_noins"] = stats.get("fill_noins", 0) + 1
            S.stops.pop(); continue
        routes[v].insert(pos, j)
        fills.append((crop, p, buy)); new.append(j); fut = trial
    if not fills:
        return routes, []
    routes = S.improve(routes, units, time.time() + S.budget / 4)
    routes, ok = S.fix_spawns(routes, units)
    if not ok or any(S.ev(u, routes[u]) is None for u in units if routes.get(u)):
        # infeasible once the spawns settle: drop the fills, keep the same-crew solution
        del S.stops[n0:]; B["sp"] = sp0; S.cache = {}
        if stats is not None:
            stats["fill_fail"] = stats.get("fill_fail", 0) + 1
        return routes0, []
    if stats is not None:
        stats["fill_spare"] = stats.get("fill_spare", 0) + gross
    ledger.extend((day, crop, p) for crop, p, _b in fills)
    if fstate is not None:
        fstate["new"] = [(day, crop, p) for crop, p, _b in fills]
    return routes, fills


def _seed_slot(mop, ma, ci):
    """(hour, slot, new) for the fill seed buy: the planner's own earliest BUY_SEED row of the crop (qty bumped,
    lockstep order unchanged), else a new row after the last used slot of the first hour 0-3 that has one."""
    for h in range(mop.shape[0]):
        for s in range(mop.shape[1]):
            if mop[h, s] == O.MO_BUY_SEED and int(ma[h, s]) == ci:
                return (h, s, False)
    for h in range(4):
        used = [s for s in range(mop.shape[1]) if mop[h, s] != O.MO_NONE]
        s = max(used) + 1 if used else 0
        if s < mop.shape[1]:
            return (h, s, True)
    return None


def _seed_rows(mop, ma, mq, fills):
    need = collections.Counter(c for c, _p, b in fills if b)
    for c, n in need.items():
        ci = spec.CROPS.index(c)
        r = _seed_slot(mop, ma, ci)
        if r is None:
            continue
        h, s, new = r
        if new:
            mop[h, s] = O.MO_BUY_SEED; ma[h, s] = ci; mq[h, s] = n
        else:
            mq[h, s] += n



# ---------------------------------------------------------------- SLIVER1: plantings in the route-end idle turns
_NONGO = tuple(c for i, c in enumerate(spec.CROPS) if not int(spec.CROP_ONGOING[i]))
_NOT_WITH = ("PLANT", "DIG", "PLACE")


def _stop_copy(st):
    s2 = Stop(st.tile)
    s2.ops = list(st.ops); s2.hours = list(st.hours); s2.units = set(st.units); s2.mk = list(st.mk)
    s2.need = collections.Counter(st.need); s2.give = collections.Counter(st.give)
    s2.dur, s2.early, s2.late, s2.harv, s2.opt, s2.val = st.dur, st.early, st.late, st.harv, st.opt, st.val
    return s2


def _sliver_crop(day):
    if str(_P.SLIVER_CROP).upper() != "BEST":
        return "WHEAT"
    if day <= 16:
        return "STRAWBERRY"    # first yield age 10, interval 2: two yields by d28
    if day <= 26:
        return "CARROT"        # 3-day life: harvest by d29
    return "WHEAT"


def _sliver_slot(mop, ma, ci):
    """(hour, slot, new) of the dawn seed buy: the planner's own BUY_SEED row of the crop at hour 0-3 (qty bumped),
    else a new row after the last used slot of the first hour 0-3 that has room; None = no room."""
    for h in range(min(4, mop.shape[0])):
        for s in range(mop.shape[1]):
            if mop[h, s] == O.MO_BUY_SEED and int(ma[h, s]) == ci:
                return (h, s, False)
    for h in range(min(4, mop.shape[0])):
        used = [s for s in range(mop.shape[1]) if mop[h, s] != O.MO_NONE]
        s = max(used) + 1 if used else 0
        if s < mop.shape[1]:
            return (h, s, True)
    return None


def sliver(S, B, routes, units, obs, day, plan, fstate, stats):
    """[SLIVER1, SLIVER_ON] after the crew is fixed: for each hand (index order) with >= SLIVER_K free turns after its
    last stop, add PLANT + WATER of the day's sliver crop -- "same": on a non-ongoing crop tile the hand's own route
    harvests and nothing replants (the harvest stop's ops extended in place, a copied Stop so checkpoints keep the
    old one); "near": on the nearest dawn-empty untouched owned tile (or an own-route harvested tile), appended after
    the last stop. Each fill must keep its route feasible (route_eval: windows, seed availability, end); after all
    fills the engine spawn rule must reproduce every solved spawn, else all of the day's fills roll back.
    Seeds: dawn stock minus the day's planned PLANTs, then one BUY_SEED row at hour 0-3 (_sliver_slot)."""
    if not (int(_P.SLIVER_DAY0) <= day <= int(_P.SLIVER_DAY1)):
        return routes
    crop = _sliver_crop(day); ci = spec.CROPS.index(crop)
    k = max(int(_P.SLIVER_K), 2); near = str(_P.SLIVER_MODE) == "near"
    seat = obs["player"]; tiles = obs["farms"][seat]["tiles"]; end = B["end"]
    used = sum(1 for st in S.stops for a in st.ops if a[0] == "PLANT" and a[1] == crop)
    for lst in B["fz_ops"].values():
        used += sum(1 for _h, _p, a in lst if a[0] == "PLANT" and a[1] == crop)
    have = int(obs["private"]["seeds"].get(crop, 0)) - used
    mop, ma, mq = plan[3], plan[4], plan[5]
    slot = _sliver_slot(mop, ma, ci)
    n0 = len(S.stops)
    harv = {}                                   # tile -> unit whose route harvests it (non-ongoing, not replanted)
    for u in units:
        for j in routes.get(u, []):
            st = S.stops[j]; x, y = st.tile; t = tiles[y][x]
            kinds = [a[0] for a in st.ops]
            if ("HARVEST" in kinds and not any(a in kinds for a in _NOT_WITH) and st.tile not in ACC
                    and isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") in _NONGO):
                harv[st.tile] = u
    empty = []
    if near:
        busy = {st.tile for st in S.stops}
        for lst in B["fz_ops"].values():
            busy |= {p for _h, p, _a in lst}
        empty = [(x, y) for y in range(len(tiles)) for x in range(len(tiles[y]))
                 if tiles[y][x] is None and (x, y) not in busy and (x, y) not in ACC]
    routes2 = {u: list(r) for u, r in routes.items()}
    fills = []; done = set()
    for u in sorted(units):
        r = routes2.get(u)
        if u == 0 or not r:
            continue
        v = S.ev(u, r)
        if v is None:
            continue
        while end - v[0] >= k:
            buy = have - len(fills) <= 0
            if buy and slot is None:
                break
            early = slot[0] + 1 if buy else 0
            if not near:
                cand = [i for i, j in enumerate(r) if j < n0 and harv.get(S.stops[j].tile) == u
                        and S.stops[j].tile not in done]
                if not cand:
                    break
                i = cand[0]; st2 = _stop_copy(S.stops[r[i]])
                st2.ops += [("PLANT", crop), ("WATER",)]; st2.dur += 2; st2.early = max(st2.early, early)
                S.stops.append(st2); r2 = r[:i] + [len(S.stops) - 1] + r[i + 1:]
            else:
                pos = S.stops[r[-1]].tile; free = end - v[0]
                pool = [p for p in empty if p not in done] + [p for p, w in harv.items() if w == u and p not in done]
                pool = sorted((dist(pos, p), p) for p in pool if dist(pos, p) + 2 <= free)
                if not pool:
                    break
                st2 = Stop(pool[0][1]); st2.ops = [("PLANT", crop), ("WATER",)]; st2.dur = 2
                st2.hours = [23]; st2.units = {u}; st2.early = early
                S.stops.append(st2); r2 = r + [len(S.stops) - 1]
            done.add(st2.tile)
            v2 = S.ev(u, r2)
            if v2 is None:
                S.cache.pop((u, tuple(r2)), None); S.stops.pop()
                if stats is not None:
                    stats["sliver_infeas"] = stats.get("sliver_infeas", 0) + 1
                continue
            r = r2; routes2[u] = r; v = v2; fills.append((crop, st2.tile, buy))
    if not fills:
        return routes
    sp = (true_spawns_seq if S.seqsp else true_spawns)(B, S, routes2, units)
    bad = sp.pop("_fzbad", False)
    chk = list(units) + (sorted(B["frozen"]) if _sw("ROUTE_VRP_FIX_FROZEN") else [])
    if bad or any(sp[u] != B["sp"][u] for u in chk):
        del S.stops[n0:]; S.cache = {}
        if stats is not None:
            stats["sliver_rb"] = stats.get("sliver_rb", 0) + 1
        return routes
    nb = sum(1 for _c, _p, b in fills if b)
    if nb:
        h, s, new = slot
        if new:
            mop[h, s] = O.MO_BUY_SEED; ma[h, s] = ci; mq[h, s] = nb
        else:
            mq[h, s] += nb
    if fstate is not None:
        fstate["new"] = [(day, c, p) for c, p, _b in fills]
    if stats is not None:
        stats["sliver"] = stats.get("sliver", 0) + len(fills)
        stats["sliver_buy"] = stats.get("sliver_buy", 0) + nb
    return routes2
